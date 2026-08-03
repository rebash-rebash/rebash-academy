---
title: Kubernetes Capstone and Next Steps
description: Capstone project — deploy VoteStack on Kubernetes with GitOps, HPA, observability, and security hardening; roadmap to Terraform and GitLab CI/CD.
difficulty: advanced
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-08-03"
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

## Architecture









![Production cluster](../assets/excalidraw/k8s-production-cluster.svg)

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

## Theory









Core ideas for this tutorial appear inline in the lab steps and Code Walkthrough. Read each step explanation before running commands.


### Capstone production checklist

A Kubernetes capstone should demonstrate Deployments with probes, Services, Ingress with TLS (or a documented local substitute), ConfigMaps/Secrets, resource requests/limits, and a clear teardown path. Add NetworkPolicies and restricted Pod Security if your cluster supports them. Document how you promote images (digest pins) and how you would recover from a bad rollout — interviewers care about operability as much as YAML fluency.


### Practice mindset

As you work through this tutorial, narrate *why* each control or command exists — not only *how* to type it. Production incidents are rarely solved by memorising flags; they are solved by connecting symptoms to the architecture (daemon vs kubelet, image vs running container, Service vs Endpoints, volume vs writable layer). After the lab, write three bullet notes in your own words: what you verified, what would break in production if skipped, and what you would monitor next.


### Connecting the lab to production reviews

When a teammate asks “is this ready?”, answer with evidence from this tutorial’s controls: image provenance, privilege level, network exposure, health signals, and teardown/rollback. Copy-pasting a working lab snippet into production without those answers is how quiet misconfigurations become incidents. Prefer small, reviewable changes — one Dockerfile improvement, one RBAC binding, one probe — over large untested stacks.

### Observability while you learn

Get into the habit of watching state while commands run: `docker events` / `kubectl get events`, resource usage, and logs in a second pane. Many failures are timing issues (probes, readiness, volume attach) that disappear if you only look at the final steady state. Capturing a short timeline of what you saw will also make your Troubleshooting section notes far more valuable later.


### Checklist before you leave the lab

1. Resources created in this tutorial are deleted or clearly labelled for retention.
2. No secrets, kubeconfigs, or registry passwords were written into Git.
3. You can explain the Architecture diagram without reading the caption.
4. Validation pass criteria in this page are satisfied on your machine.
5. You noted one question to revisit in the next tutorial of the series.

### Common production failure modes this topic prevents

Misconfiguration here usually shows up as intermittent outages rather than clean errors: restart loops without log shipping, services that listen but never become Ready, volumes that work on one node only, or credentials that leak into image history. Use the Hands-on Lab as a rehearsal for the failure mode — break something on purpose, watch the signal, then apply the fix documented in Troubleshooting.

## Hands-on Lab

### Objective

Build and apply a multi-manifest mini platform in `~/rebash-k8s/capstone` — namespace, ConfigMap, Deployment, Service, and NetworkPolicy — prove end-to-end Ready, and archive an evidence tarball.

### Prerequisites

- kubectl configured against **kind** or **minikube**
- CNI with NetworkPolicy support (kind default)
- Namespace-create rights on the lab cluster
- Writable workspace at `~/rebash-k8s/capstone`

### Lab environment

Workspace: `~/rebash-k8s/capstone`

```bash title="Terminal"
mkdir -p ~/rebash-k8s/capstone && cd ~/rebash-k8s/capstone
```

### Real-world scenario

You deliver a capstone demo for stakeholders: a small API platform in namespace `rebash-capstone` with configuration from a ConfigMap, a secured Deployment behind a ClusterIP Service, and a default-deny NetworkPolicy. Success means all Pods Ready, Service Endpoints populated, and a tarball you can attach to a portfolio README.

### Step-by-step tasks

#### Task 1 – Create namespace and ConfigMap

Create `namespace.yaml`:

```yaml title="namespace.yaml"
apiVersion: v1
kind: Namespace
metadata:
  name: rebash-capstone
  labels:
    app.kubernetes.io/part-of: rebash-capstone
    app.kubernetes.io/managed-by: rebash-lab
```

Create `configmap.yaml`:

```yaml title="configmap.yaml"
apiVersion: v1
kind: ConfigMap
metadata:
  name: capstone-config
  namespace: rebash-capstone
data:
  APP_NAME: rebash-capstone
  LOG_LEVEL: info
  index.html: |
    <!DOCTYPE html>
    <html><body><h1>REBASH Capstone API</h1></body></html>
```

Apply:

```bash title="Terminal"
cd ~/rebash-k8s/capstone
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl get configmap capstone-config -n rebash-capstone
```

!!! example "Expected output"
    ConfigMap `capstone-config` with three data keys.


#### Task 2 – Create Deployment and Service

Create `deployment.yaml`:

```yaml title="deployment.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: capstone-api
  namespace: rebash-capstone
  labels:
    app: capstone-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: capstone-api
  template:
    metadata:
      labels:
        app: capstone-api
    spec:
      containers:
        - name: api
          image: nginx:1.27-alpine
          ports:
            - containerPort: 80
          env:
            - name: APP_NAME
              valueFrom:
                configMapKeyRef:
                  name: capstone-config
                  key: APP_NAME
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: capstone-config
                  key: LOG_LEVEL
          volumeMounts:
            - name: html
              mountPath: /usr/share/nginx/html/index.html
              subPath: index.html
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 2
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
      volumes:
        - name: html
          configMap:
            name: capstone-config
            items:
              - key: index.html
                path: index.html
```

Create `service.yaml`:

```yaml title="service.yaml"
apiVersion: v1
kind: Service
metadata:
  name: capstone-api
  namespace: rebash-capstone
spec:
  selector:
    app: capstone-api
  ports:
    - port: 80
      targetPort: 80
```

Apply and wait for Ready:

```bash title="Terminal"
cd ~/rebash-k8s/capstone
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl rollout status deployment/capstone-api -n rebash-capstone --timeout=120s
kubectl get deploy,po,svc -n rebash-capstone
```

!!! example "Expected output"
    Deployment Available; 2/2 Pods Ready; Service exists.


#### Task 3 – Add NetworkPolicy and verify traffic path

Create `networkpolicy.yaml`:

```yaml title="networkpolicy.yaml"
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: capstone-default-deny
  namespace: rebash-capstone
spec:
  podSelector: {}
  policyTypes:
    - Ingress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: capstone-allow-internal
  namespace: rebash-capstone
spec:
  podSelector:
    matchLabels:
      app: capstone-api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector: {}
      ports:
        - protocol: TCP
          port: 80
```

Apply and test from an in-cluster curl Pod:

```bash title="Terminal"
cd ~/rebash-k8s/capstone
kubectl apply -f networkpolicy.yaml
kubectl run curl-test --rm -it --restart=Never -n rebash-capstone --image=curlimages/curl:8.5.0 -- \
  curl -sS http://capstone-api/ | grep -q 'REBASH Capstone API'
kubectl get endpoints capstone-api -n rebash-capstone | tee endpoints.txt
```

!!! example "Expected output"
    curl returns HTML containing `REBASH Capstone API`; Endpoints show Pod IPs.


#### Task 4 – Package capstone evidence tarball

```bash title="Terminal"
cd ~/rebash-k8s/capstone
kubectl get all,configmap,networkpolicy -n rebash-capstone | tee capstone-status.txt
kubectl describe deploy capstone-api -n rebash-capstone | tee capstone-describe.txt
tar -czf capstone-evidence.tgz namespace.yaml configmap.yaml deployment.yaml service.yaml networkpolicy.yaml capstone-status.txt capstone-describe.txt endpoints.txt
ls -l capstone-evidence.tgz
```

!!! example "Expected output"
    `capstone-evidence.tgz` lists all manifests and status files.


### Validation steps

- [ ] Namespace `rebash-capstone` contains ConfigMap-backed Deployment
- [ ] Two replicas reach Ready with probes passing
- [ ] Service Endpoints populated
- [ ] In-cluster curl reaches custom index.html through NetworkPolicy
- [ ] Evidence tarball created under `~/rebash-k8s/capstone`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| ConfigMap mount empty | Wrong subPath or key | Match `items.key` to ConfigMap data key |
| curl timeout | NetworkPolicy too strict | Allow ingress from same namespace |
| Pods NotReady | Probe before mount ready | Increase `initialDelaySeconds` slightly |
| Endpoints empty | Label selector mismatch | Align Service selector with Pod labels |
| Wrong workspace path | Old `rebash-kubernetes` path | Use `~/rebash-k8s/capstone` |

### Challenge exercise

Add a `PodDisruptionBudget` with `minAvailable: 1` and verify `kubectl get pdb -n rebash-capstone` before adding it to the evidence tarball.

### Learning outcomes

- Composed a multi-object platform from namespace through NetworkPolicy
- Wired ConfigMap data into a running Deployment
- Verified in-cluster connectivity with probes and curl
- Produced a portfolio-ready evidence tarball

### Cleanup

```bash title="Terminal"
kubectl delete namespace rebash-capstone --ignore-not-found --wait=true
rm -f ~/rebash-k8s/capstone/*.txt ~/rebash-k8s/capstone/capstone-evidence.tgz
```

## Validation









Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Deploy | Capstone app Deployments/Services are Ready |
| Ingress | External access works via Ingress/port-forward as designed |
| Hardening | Security contexts, probes, and resource limits present |
| Cleanup | Namespace torn down or clearly labelled as a retained demo |

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

If your organisation standardizes on GitLab, port the VoteStack CI workflow — build, scan, update GitOps manifest — to `.gitlab-ci.yml`.

### Recommended learning path

![GitOps workflow](../assets/excalidraw/k8s-gitops-workflow.svg)


1. Deploy VoteStack capstone as portfolio project
2. Begin [Terraform – Introduction](../terraform/index.md) — provision a lab EKS cluster
3. Migrate VoteStack GitOps target from kind/minikube to Terraform-managed EKS
4. Optional: [GitLab CI/CD Overview](../gitlab/index.md) — enterprise pipeline patterns
5. Follow [DevOps Engineer Learning Path](../learning-paths/index.md) for role certification goals

## Code Walkthrough









```bash title="Terminal"
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

## Security Considerations









- Apply restricted Pod Security, NetworkPolicies, and resource quotas on the capstone namespace
- Keep registry credentials and DB passwords in Secrets/ESO — not in Helm values committed to Git
- Use least-privilege CI and GitOps identities for deploy
- Expose the app only via TLS Ingress; keep databases ClusterIP-only
- Scan images and fail the pipeline on critical CVEs before promoting tags
- Tear down or lock the lab namespace when finished so demos do not remain internet-facing

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








1. Which Kubernetes primitives form a minimal production-ready web service?
2. How would you decide the next skills to learn after core workloads?
3. What evidence shows a Deployment is healthy beyond Pods being Running?
4. What security baseline would you require before calling a cluster production-ready?
5. How do managed Kubernetes services change what you operate versus what the vendor operates?

!!! tip "Sample answer — question 2"
    Ready replicas, passing probes, populated Endpoints, and recent events without CrashLoopBackOff are stronger signals than phase Running alone.

!!! tip "Sample answer — question 4"
    Production readiness needs RBAC least privilege, network policy, secret hygiene, resource requests, observability, backup/upgrade plans, and restricted privileged workloads—not only green Deployments.

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

If your organisation standardizes on GitLab, port the VoteStack CI workflow — build, scan, update GitOps manifest — to `.gitlab-ci.yml`.

### Recommended learning path

![Production cluster design](../assets/excalidraw/k8s-production-cluster.svg)


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
- Cheat sheet: [Kubernetes Cheat Sheet](../cheatsheets/kubernetes.md)
- Interview prep: [Kubernetes Interview Prep](../interview/kubernetes.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

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
