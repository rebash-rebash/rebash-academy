---
title: Kubernetes Capstone and Next Steps
description: Capstone project — deploy VoteStack on Kubernetes with GitOps, HPA, observability, and security hardening; roadmap to Terraform and GitLab CI/CD.
difficulty: advanced
estimated_time: "45 min"
author: Shaik Basha
category: kubernetes
tags:
  - kubernetes
  - capstone
  - gitops
  - project
  - next-steps
prerequisites:
  - Kubernetes Security Hardening
  - GitOps and CI/CD with Kubernetes
  - Monitoring and Logging in Kubernetes
comments: false
---

# Kubernetes Capstone and Next Steps

## Overview

You have progressed from your first Pod to GitOps delivery, autoscaling, observability, and cluster hardening. This capstone deploys **VoteStack** — the multi-service poll application from the [Docker capstone](../docker/docker-capstone-and-next-steps.md) — on a production-style Kubernetes cluster. You will wire every layer from the Module 6 tutorials into one cohesive project and document a roadmap to [Terraform](../terraform/index.md) for infrastructure and [GitLab CI/CD](../gitlab/index.md) for enterprise pipelines.

This is **Tutorial 20** — the finale of **Module 6: Production** and the complete REBASH Academy **Kubernetes track**.

## Prerequisites

- [Kubernetes Security Hardening](kubernetes-security-hardening.md)
- [GitOps and CI/CD with Kubernetes](gitops-and-cicd-with-kubernetes.md)
- [Production Patterns — HPA, PDB, and Affinity](production-patterns-hpa-pdb-and-affinity.md)
- [Monitoring and Logging in Kubernetes](monitoring-and-logging-in-kubernetes.md)
- [Helm Package Management](helm-package-management.md)
- [Ingress and External Access](ingress-and-external-access.md)
- [Persistent Volumes and Storage](persistent-volumes-and-storage.md)
- Cluster with ingress controller, metrics-server, and Helm 3
- Container images from Docker track or GitOps CI pipeline

## Learning Objectives

By the end of this capstone, you will be able to:

- [ ] Deploy VoteStack on Kubernetes using a Helm chart and Argo CD
- [ ] Configure HPA, PDB, and topology spread for api and worker tiers
- [ ] Expose the app via Ingress with TLS and internal NetworkPolicies
- [ ] Instrument services with Prometheus metrics and centralized logging
- [ ] Apply Pod Security Standards and Kyverno policies to the stack
- [ ] Document operational runbooks and a learning path to Terraform and GitLab

## Architecture Diagram

```d2
direction: down

External: External {
        USER: Browser
        DNS: votestack.example.com
    }
    IngressLayer: ingress-nginx {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        ING: "Ingress + TLS"
    }
    Votestack: "namespace: votestack" {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        WEB: "web Deployment"
        API: "api Deployment + HPA"
        WORK: "worker Deployment + HPA"
        REDIS: "redis StatefulSet"
        PG: "postgres StatefulSet + PVC"
    }
    Platform: Platform {
        ARGO: "Argo CD"
        PROM: "Prometheus / Grafana"
        KYV: Kyverno
    }
    External.USER -> External.DNS
    External.DNS -> IngressLayer.ING
    IngressLayer.ING -> Votestack.WEB
    IngressLayer.ING -> Votestack.API
    Votestack.API -> Votestack.REDIS
    Votestack.API -> Votestack.PG
    Votestack.WORK -> Votestack.REDIS
    Votestack.WORK -> Votestack.PG
    Votestack: Votestack
    Platform.ARGO -> Votestack: sync {
      style.stroke-dash: 3
    }
    Platform.PROM -> Votestack.API: scrape {
      style.stroke-dash: 3
    }
    Platform.KYV -> Votestack: enforce {
      style.stroke-dash: 3
    }
```

## Project Overview — VoteStack on Kubernetes

VoteStack mirrors the Docker capstone with Kubernetes-native primitives:

| Service | Kubernetes resource | Notes |
|---------|---------------------|-------|
| **web** | Deployment + Service | Static UI; 2 replicas |
| **api** | Deployment + Service + HPA + PDB | REST API; `/health`, `/ready`, `/metrics` |
| **worker** | Deployment + HPA | Queue consumer; scales on Redis depth |
| **redis** | StatefulSet + headless Service | Persistent queue (dev lab); use ElastiCache in prod |
| **postgres** | StatefulSet + PVC | Dev lab; use RDS/Cloud SQL in prod |
| **edge** | Ingress | TLS via cert-manager |

Same container images built in the Docker track — only deployment manifests change.

## Project Structure

```text
votestack-gitops/
├── apps/
│   ├── root-app.yaml              # App-of-Apps bootstrap
│   └── votestack/
│       └── application.yaml
├── charts/
│   └── votestack/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       ├── values-prod.yaml
│       └── templates/
│           ├── namespace.yaml
│           ├── web/
│           ├── api/
│           ├── worker/
│           ├── redis/
│           ├── postgres/
│           ├── ingress.yaml
│           ├── hpa.yaml
│           ├── pdb.yaml
│           ├── networkpolicy.yaml
│           └── servicemonitor.yaml
├── policies/
│   └── kyverno/
│       ├── require-limits.yaml
│       └── disallow-latest.yaml
└── README.md
```

## Hands-on Lab

### Lab 1 — Bootstrap GitOps (App of Apps)

`apps/root-app.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: votestack-root
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/votestack-gitops.git
    targetRevision: main
    path: charts/votestack
    helm:
      valueFiles:
        - values-dev.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: votestack
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

```bash
kubectl apply -f apps/root-app.yaml
argocd app sync votestack-root
kubectl get all -n votestack
```

### Lab 2 — Stateful data tier

Postgres StatefulSet excerpt (`templates/postgres/statefulset.yaml`):

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: votestack
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      securityContext:
        fsGroup: 999
      containers:
        - name: postgres
          image: postgres:16-alpine
          envFrom:
            - secretRef:
                name: postgres-credentials
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: [ReadWriteOnce]
        resources:
          requests:
            storage: 10Gi
```

Apply SealedSecret for credentials (see [Kubernetes Security Hardening](kubernetes-security-hardening.md)).

Verify: `kubectl get pvc -n votestack`

### Lab 3 — Ingress with TLS

Install cert-manager (once per cluster):

```bash
helm repo add jetstack https://charts.jetstack.io
helm install cert-manager jetstack/cert-manager \
  -n cert-manager --create-namespace \
  --set crds.enabled=true
```

Ingress template:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: votestack
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts: [votestack.example.com]
      secretName: votestack-tls
  rules:
    - host: votestack.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: votestack-api
                port:
                  number: 8080
          - path: /
            pathType: Prefix
            backend:
              service:
                name: votestack-web
                port:
                  number: 3000
```

Smoke test:

```bash
curl -sf https://votestack.example.com/api/health
curl -sf https://votestack.example.com/ -o /dev/null
```

### Lab 4 — HPA, PDB, and spread (production patterns)

Enable in `values-dev.yaml`:

```yaml
api:
  replicas: 2
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 8
    targetCPUUtilization: 70
  pdb:
    minAvailable: 1
  topologySpread:
    enabled: true

worker:
  autoscaling:
    enabled: true
    minReplicas: 1
    maxReplicas: 5
```

Sync and validate:

```bash
kubectl get hpa,pdb -n votestack
kubectl get pods -n votestack -o wide
```

### Lab 5 — Observability stack integration

Add ServiceMonitor to Helm chart (see [Monitoring and Logging](monitoring-and-logging-in-kubernetes.md)). Import VoteStack Grafana dashboard. Confirm alerts:

```bash
kubectl port-forward svc/kube-prometheus-grafana -n monitoring 3000:80
# Dashboard: error rate, p99 latency, pod restarts
```

Log query in Loki:

```logql
{namespace="votestack"} | json | level="error"
```

### Lab 6 — Security hardening checklist

Apply the full security stack from Tutorial 19:

```bash
# Pod Security
kubectl label namespace votestack \
  pod-security.kubernetes.io/enforce=restricted --overwrite

# NetworkPolicies
kubectl apply -f charts/votestack/templates/networkpolicy.yaml

# Kyverno policies
kubectl apply -f policies/kyverno/

# Verify
kubectl run bad --rm -it --image=nginx:latest -n votestack
# Expected: blocked by admission policy
```

### Lab 7 — Operations runbook

```bash
# Backup postgres
kubectl exec -n votestack postgres-0 -- \
  pg_dump -U voteapp votes > "backups/votes-$(date +%Y%m%d).sql"

# Rollback via GitOps
cd votestack-gitops
git revert HEAD && git push
argocd app sync votestack-root

# Scale manually (temporary — prefer HPA)
kubectl scale deployment votestack-api -n votestack --replicas=5

# Node drain simulation (respects PDB)
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data
```

Document results in `README.md` — architecture diagram, deploy steps, rollback procedure.

## Commands & Code

```bash
# End-to-end status
kubectl get deploy,sts,svc,ingress,hpa,pdb -n votestack
argocd app get votestack-root

# End-to-end smoke
curl -sf https://votestack.example.com/api/health
curl -sf https://votestack.example.com/api/polls | jq .

# Debug chain
kubectl logs -n votestack deploy/votestack-api --tail=50
kubectl describe pod -n votestack -l app=votestack-api
kubectl get events -n votestack --sort-by='.lastTimestamp' | tail -10
```

## Common Mistakes

!!! warning "Running postgres/redis in prod without backups"
    StatefulSets need backup automation and tested restore — or use managed databases.

!!! warning "Skipping TLS on Ingress"
    `allowInsecure` is for dev only — prod requires cert-manager or cloud LB certs.

!!! warning "Capstone without NetworkPolicies"
    A complete stack demo that ignores segmentation fails security interviews.

!!! warning "Manual kubectl edits in GitOps workflow"
    selfHeal reverts them — always change Git, not live cluster.

!!! warning "No resource requests on any tier"
    HPA and scheduling break — every container needs requests.

## Best Practices

!!! tip "Portfolio README"
    Include architecture diagram, tech stack, and `kubectl get` screenshot — strong interview artifact.

!!! tip "Managed services in real prod"
    Replace in-cluster postgres/redis with RDS and ElastiCache — keep StatefulSets for learning labs.

!!! tip "Environment parity"
    Same Helm chart, different values files — dev/staging/prod differ only in replicas, hosts, and secrets backend.

!!! tip "Chaos exercise"
    Delete api pods during load test — observe HPA, PDB, and Ingress recovery.

!!! tip "Continue the platform path"
    Kubernetes completes orchestration — [Terraform](../terraform/index.md) provisions the cluster itself.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Ingress 502 | api not ready | Check probes; postgres/redis connectivity |
| TLS not issued | cert-manager misconfig | `kubectl describe certificate -n votestack` |
| HPA no scale | Missing metrics-server | Install metrics-server; verify requests |
| Argo OutOfSync loop | Helm hook or ignored diff | Add ignoreDifferences for known fields |
| NetworkPolicy blocks traffic | Missing DNS/ingress rule | Add egress UDP 53; allow ingress namespace |
| PVC Pending | No StorageClass | `kubectl get sc`; set default class |

## Summary

- The **VoteStack Kubernetes capstone** combines Helm, GitOps, Ingress, StatefulSets, HPA, PDB, observability, and security hardening
- **Same images** from the Docker track — Kubernetes adds scheduling, scaling, segmentation, and declarative delivery
- **GitOps** is the deployment interface — runbooks center on Git revert, Argo sync, and backup/restore
- **Production reality** swaps in-cluster databases for managed services and clusters for Terraform-provisioned infrastructure
- You have finished all **20 Kubernetes tutorials** — continue to [Terraform](../terraform/index.md), [GitLab CI/CD](../gitlab/index.md), and [Learning Paths](../learning-paths/index.md)

## Interview Questions

1. Walk through VoteStack architecture on Kubernetes — from Ingress to postgres.
2. Why use StatefulSet for postgres instead of Deployment?
3. How does GitOps rollback differ from `kubectl rollout undo`?
4. What would you change moving from dev cluster to production AWS EKS?
5. Explain how HPA, PDB, and topology spread work together during a node upgrade.
6. How do NetworkPolicies map to the Docker Compose internal network model?
7. What metrics and alerts would you define for VoteStack in production?
8. Why seal secrets instead of using Kubernetes Secrets directly in Git?
9. How does this capstone demonstrate the full Kubernetes track skills?
10. What is the natural next skill after completing Kubernetes?

??? tip "Sample Answers (Questions 1, 4, and 10)"

    **Q1 — K8s VoteStack flow:** Browser resolves `votestack.example.com` → Ingress (TLS) routes `/api` to api Service → api pods (HPA-scaled, PDB-protected) validate and enqueue votes to redis. worker pods consume queue, write to postgres StatefulSet. web pods serve UI. NetworkPolicies restrict api to redis/postgres only. Prometheus scrapes `/metrics`; logs flow to Loki. Argo CD syncs all resources from Git.

    **Q4 — Dev to EKS prod:** Provision EKS with Terraform (VPC, node groups, IRSA). Replace in-cluster postgres/redis with RDS and ElastiCache. Use ALB Ingress Controller and ACM certs. External Secrets for credentials. Multi-AZ node groups; Cluster Autoscaler. Centralized observability (AMP/Grafana or Datadog). GitOps with prod approval gates; separate AWS accounts for envs.

    **Q10 — After Kubernetes:** **Terraform** for infrastructure-as-code — VPC, EKS/GKE, IAM, RDS. **GitLab CI/CD** for enterprise pipeline patterns. **Service mesh** (Istio/Linkerd) for advanced traffic management. **Platform engineering** — Internal Developer Platforms (Backstage, Crossplane). Return to [Learning Paths](../learning-paths/index.md) for role-specific roadmaps.

## Next Steps — Terraform and GitLab

### Terraform track

Kubernetes clusters do not appear by magic. The [Terraform track](../terraform/index.md) teaches:

| Topic | Delivers |
|-------|----------|
| HCL fundamentals | Variables, modules, state |
| AWS/GCP/Azure providers | VPC, subnets, security groups |
| EKS/GKE modules | Managed control plane + node pools |
| IAM and IRSA | Pod-level AWS permissions without static keys |

VoteStack prod target architecture:

```text
Terraform → EKS cluster + RDS + ElastiCache + ECR
     ↓
GitOps repo → Helm deploys VoteStack to EKS
     ↓
CI pipeline → builds images, updates tags
```

### GitLab CI/CD track

The [GitLab track](../gitlab/index.md) complements GitHub Actions patterns from Tutorial 16:

- Multi-environment deploy pipelines with manual approval gates
- Container registry integrated with CI
- GitLab Agent for Kubernetes (agent-based deploy alternative)
- Compliance frameworks and audit trails

If your organization standardizes on GitLab, port the VoteStack CI workflow — build, scan, update GitOps manifest — to `.gitlab-ci.yml`.

### Recommended learning path

```d2
direction: right

DOCKER: "Docker track ✓"
    K8S: "Kubernetes track ✓"
    TF: "Terraform track"
    GL: "GitLab CI/CD"
    LP: "Learning Paths"
    DOCKER -> K8S
    K8S -> TF
    K8S -> GL
    TF -> LP
    GL -> LP
```

1. Deploy VoteStack capstone as portfolio project
2. Begin [Terraform – Introduction](../terraform/index.md) — provision a lab EKS cluster
3. Migrate VoteStack GitOps target from kind/minikube to Terraform-managed EKS
4. Optional: [GitLab CI/CD Overview](../gitlab/index.md) — enterprise pipeline patterns
5. Follow [DevOps Engineer Learning Path](../learning-paths/index.md) for role certification goals

## Related Tutorials

- [Kubernetes Security Hardening](kubernetes-security-hardening.md) *(previous)*
- [GitOps and CI/CD with Kubernetes](gitops-and-cicd-with-kubernetes.md)
- [Production Patterns — HPA, PDB, and Affinity](production-patterns-hpa-pdb-and-affinity.md)
- [Monitoring and Logging in Kubernetes](monitoring-and-logging-in-kubernetes.md)
- [Docker Capstone and Next Steps](../docker/docker-capstone-and-next-steps.md)
- [From Docker to Kubernetes](../docker/from-docker-to-kubernetes.md)
- [Kubernetes – Category Overview](index.md) — track complete
- [Terraform – Category Overview](../terraform/index.md) — **next track**
- [GitLab CI/CD Overview](../gitlab/index.md)
- [Learning Paths](../learning-paths/index.md)

## References

- [Kubernetes – Production Best Practices](https://kubernetes.io/docs/setup/best-practices/)
- [CNCF – Trail Map](https://github.com/cncf/trail-map)
- [The Twelve-Factor App](https://12factor.net/)
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [REBASH Academy – Terraform Overview](../terraform/index.md)
- [REBASH Academy – GitLab Overview](../gitlab/index.md)
- [REBASH Academy – Roadmap](../roadmap.md)

## Congratulations

You have completed all **20 tutorials** in the REBASH Academy Kubernetes track — from orchestration fundamentals through GitOps delivery, autoscaling, observability, security hardening, and the VoteStack capstone. Return to the [Kubernetes Overview](index.md) to review the curriculum, publish VoteStack as a portfolio project, and begin the [Terraform track](../terraform/index.md) when you are ready to provision cloud infrastructure that runs your clusters.
