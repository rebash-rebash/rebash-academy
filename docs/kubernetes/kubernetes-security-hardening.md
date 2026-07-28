---
title: Kubernetes Security Hardening
description: Harden Kubernetes clusters with Pod Security Standards, NetworkPolicies, admission control, RBAC least privilege, and supply-chain security.
difficulty: advanced
estimated_time: "55 min"
author: Shaik Basha
category: kubernetes
tags:
  - kubernetes
  - security
  - rbac
  - networkpolicy
  - admission
prerequisites:
  - Monitoring and Logging in Kubernetes
  - RBAC and Kubernetes Security Basics
  - ConfigMaps and Secrets
comments: false
---

# Kubernetes Security Hardening

## Overview

Kubernetes defaults prioritize developer velocity over maximum security. Production clusters require deliberate hardening: **Pod Security Standards** restrict dangerous pod capabilities, **NetworkPolicies** enforce micro-segmentation, **admission controllers** block non-compliant resources at the API gate, and **RBAC** grants least-privilege access. Supply-chain controls ensure only trusted, scanned images run in the cluster.

This tutorial builds a defense-in-depth security model for the VoteStack application and cluster infrastructure — the capstone security layer before full production deployment.

This is **Tutorial 19** in **Module 6: Production** of the REBASH Academy Kubernetes series.

## Prerequisites

- [Monitoring and Logging in Kubernetes](monitoring-and-logging-in-kubernetes.md)
- [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md)
- [ConfigMaps and Secrets](configmaps-and-secrets.md)
- [Namespaces and Resource Management](namespaces-and-resource-management.md)
- [GitOps and CI/CD with Kubernetes](gitops-and-cicd-with-kubernetes.md)
- Cluster admin access for policy installation
- Optional: [Docker Security Hardening](../docker/docker-security-hardening.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply Pod Security Standards (restricted, baseline, privileged) at namespace level
- [ ] Write NetworkPolicies that default-deny and allow explicit traffic paths
- [ ] Configure admission policies with Kyverno or OPA Gatekeeper
- [ ] Implement RBAC least privilege for users, CI, and GitOps agents
- [ ] Secure secrets with External Secrets Operator or Sealed Secrets
- [ ] Enforce image provenance and vulnerability thresholds in the deploy pipeline

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Perimeter
        ING[Ingress + TLS]
        WAF["WAF / rate limit"]
    end

    subgraph Admission
        API[Kubernetes API]
        KYV["Kyverno / Gatekeeper"]
        API --> KYV
    end

    subgraph Namespace["votestack namespace"]
        NETP[NetworkPolicy]
        PSS["Pod Security: restricted"]
        WEB[web]
        APIP[api]
        WORK[worker]
        WEB --> NETP
        APIP --> NETP
        WORK --> NETP
    end

    subgraph Data
        PG["(postgres")]
        RD["(redis")]
    end

    ING --> WEB
    ING --> APIP
    APIP --> RD
    APIP --> PG
    WORK --> RD
    WORK --> PG
    KYV --> Namespace
```

## Theory

### Defense in depth for Kubernetes

| Layer | Control | Blocks |
|-------|---------|--------|
| **Identity** | RBAC, OIDC | Unauthorized API access |
| **Admission** | Kyverno, Gatekeeper | Non-compliant manifests |
| **Pod** | PSS, seccomp, AppArmor | Privileged containers, hostPath |
| **Network** | NetworkPolicy | Lateral movement |
| **Secrets** | External Secrets, encryption at rest | Credential leakage |
| **Supply chain** | Image signing, Trivy, admission | Vulnerable or untrusted images |
| **Audit** | Audit logs, Falco | Forensics and runtime threats |

No single layer is sufficient — assume breach and limit blast radius.

### Pod Security Standards

Replace deprecated PodSecurityPolicy with **Pod Security Admission** (built-in):

| Profile | Restrictions |
|---------|--------------|
| **privileged** | Unrestricted — system namespaces only |
| **baseline** | Blocks known privilege escalations |
| **restricted** | Hardened — non-root, drop caps, no host namespaces |

Apply via namespace labels:

```yaml
metadata:
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

Pods violating `enforce` are rejected; `warn` surfaces issues in audit logs.

### NetworkPolicy fundamentals

Without policies, all pods communicate freely (default allow). Production uses **default deny**:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

Then add explicit allow rules — ingress controller → web/api; api → postgres/redis only.

Requires a CNI that enforces NetworkPolicy (Calico, Cilium, Weave).

### Admission control

**Validating** policies reject bad resources. **Mutating** policies inject defaults (labels, sidecars).

Kyverno example — require resource limits:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-requests-limits
spec:
  validationFailureAction: Enforce
  rules:
    - name: validate-resources
      match:
        any:
          - resources:
              kinds: [Pod]
      validate:
        message: "CPU and memory requests/limits required"
        pattern:
          spec:
            containers:
              - resources:
                  requests:
                    memory: "?*"
                    cpu: "?*"
                  limits:
                    memory: "?*"
                    cpu: "?*"
```

### RBAC least privilege

| Actor | Scope | Permissions |
|-------|-------|-------------|
| Developer | Namespace | get/list pods, logs — no secrets |
| CI bot | None on cluster | Push images only |
| Argo CD | App namespaces | apply/sync specific resources |
| On-call | Namespace or cluster | escalate via break-glass role |

Avoid cluster-admin bindings except for bootstrap automation with audited access.

### Secrets management

Never commit plaintext Secrets to Git. Options:

| Tool | Pattern |
|------|---------|
| **Sealed Secrets** | Encrypt Secret into SealedSecret CRD — only cluster decrypts |
| **External Secrets Operator** | Sync from Vault, AWS SM, GCP SM |
| **SOPS** | Encrypt YAML in Git — decrypted at deploy time |

Enable **encryption at rest** for etcd Secret resources via KMS provider.

## Hands-on Lab

### Lab 1 — Apply Pod Security Standards

Label the votestack namespace:

```bash
kubectl label namespace votestack \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted \
  --overwrite
```

Update VoteStack api Deployment for restricted compliance:

```yaml
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: api
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: [ALL]
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
```

Apply and verify: `kubectl apply -f api-deployment.yaml`

Test rejection — this pod should fail:

```yaml
# bad-pod.yaml — privileged
securityContext:
  privileged: true
```

```bash
kubectl apply -f bad-pod.yaml -n votestack
# Expected: forbidden by PodSecurity
```

### Lab 2 — Default-deny NetworkPolicies

```yaml
# 01-default-deny.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: votestack
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
---
# 02-allow-api-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-ingress
  namespace: votestack
spec:
  podSelector:
    matchLabels:
      app: votestack-api
  policyTypes: [Ingress]
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
        - podSelector:
            matchLabels:
              app: votestack-web
      ports:
        - protocol: TCP
          port: 8080
---
# 03-allow-api-egress-data.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-egress-data
  namespace: votestack
spec:
  podSelector:
    matchLabels:
      app: votestack-api
  policyTypes: [Egress]
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - podSelector:
            matchLabels:
              app: redis
      ports:
        - protocol: TCP
          port: 6379
    - to:   # DNS
        - namespaceSelector: {}
      ports:
        - protocol: UDP
          port: 53
```

```bash
kubectl apply -f networkpolicies/
kubectl run -it debug --rm --image=busybox -n votestack -- wget -qO- http://votestack-api:8080/health
# Should succeed from allowed paths; fail from unauthorized pods
```

### Lab 3 — Install Kyverno and enforce policies

```bash
helm repo add kyverno https://kyverno.github.io/kyverno/
helm install kyverno kyverno/kyverno -n kyverno --create-namespace --wait
kubectl get clusterpolicies
```

Apply policies from Theory section plus disallow `:latest` tag:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
spec:
  validationFailureAction: Enforce
  rules:
    - name: require-image-tag
      match:
        any:
          - resources:
              kinds: [Pod]
      validate:
        message: "Using ':latest' tag is not allowed"
        pattern:
          spec:
            containers:
              - image: "!*:latest"
```

Test: deploy pod with `nginx:latest` — should be blocked.

### Lab 4 — Sealed Secrets for database credentials

```bash
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm install sealed-secrets sealed-secrets/sealed-secrets -n kube-system --wait

kubectl create secret generic postgres-credentials \
  --from-literal=username=voteapp \
  --from-literal=password='super-secret' \
  -n votestack --dry-run=client -o yaml | \
  kubeseal --format yaml > sealed-postgres.yaml

kubectl apply -f sealed-postgres.yaml
# Safe to commit sealed-postgres.yaml to GitOps repo
```

Reference in Deployment:

```yaml
envFrom:
  - secretRef:
      name: postgres-credentials
```

### Lab 5 — RBAC for GitOps agent

Argo CD should not use cluster-admin. Create scoped Role:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: argocd-votestack
  namespace: votestack
rules:
  - apiGroups: ["", "apps", "networking.k8s.io"]
    resources: ["*"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: argocd-votestack
  namespace: votestack
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: argocd-votestack
subjects:
  - kind: ServiceAccount
    name: argocd-application-controller
    namespace: argocd
```

### Lab 6 — Image scanning in CI + admission

CI gate (GitHub Actions):

{% raw %}
```yaml
- name: Trivy scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/org/votestack-api:${{ github.sha }}
    severity: CRITICAL,HIGH
    exit-code: 1
```
{% endraw %}

Kyverno verifyImages (with cosign signatures in mature setups):

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-signature
spec:
  validationFailureAction: Enforce
  rules:
    - name: verify-signature
      match:
        any:
          - resources:
              kinds: [Pod]
      verifyImages:
        - imageReferences:
            - "ghcr.io/org/votestack-*"
          attestors:
            - count: 1
              entries:
                - keys:
                    publicKeys: |-
                      -----BEGIN PUBLIC KEY-----
                      ...
                      -----END PUBLIC KEY-----
```

## Commands & Code

```bash
# Pod Security
kubectl label namespace votestack pod-security.kubernetes.io/enforce=restricted
kubectl auth can-i create pods --as=system:serviceaccount:votestack:default -n votestack

# NetworkPolicy debug
kubectl run nettest --rm -it --image=nicolaka/netshoot -n votestack
# curl, nc, traceroute between services

# RBAC audit
kubectl auth can-i --list --as=developer@corp.com -n votestack
kubectl get rolebindings,clusterrolebindings -A | grep argocd

# Audit logs (enable on api-server)
# --audit-log-path=/var/log/k8s-audit.log

# Runtime security (optional)
helm install falco falcosecurity/falco -n falco --create-namespace
```

| Control | Verify command |
|---------|----------------|
| PSS enforced | Deploy privileged pod — expect rejection |
| NetworkPolicy | Connect from unauthorized pod — expect timeout |
| Kyverno | `kubectl get policyreport -A` |
| Sealed Secret | `kubectl get sealedsecret -n votestack` |

## Common Mistakes

!!! warning "Pod Security privileged in app namespaces"
    Running `privileged` profile in application namespaces negates container isolation — reserve for kube-system only.

!!! warning "NetworkPolicy without DNS egress"
    Default-deny egress blocks CoreDNS — pods fail name resolution. Always allow UDP 53.

!!! warning "cluster-admin for Argo CD"
    Compromised GitOps repo becomes full cluster takeover — scope RBAC per namespace.

!!! warning "Secrets in ConfigMaps"
    ConfigMaps are not encrypted differently from Secrets but are widely readable — never store passwords in ConfigMaps.

!!! warning "Admission policies without exemptions"
    System namespaces (kube-system, monitoring) need exemptions or bootstrap breaks.

## Best Practices

!!! tip "Start baseline, move to restricted"
    Migrate workloads incrementally — baseline first, fix violations, then enforce restricted.

!!! tip "NetworkPolicy as code in GitOps"
    Version policies alongside app manifests — review traffic changes in PRs.

!!! tip "Break-glass cluster-admin"
    Emergency role with MFA, time-limited, fully audited — not daily driver.

!!! tip "Rotate secrets automatically"
    External Secrets with short TTL beats manual rotation quarterly.

!!! tip "CIS Kubernetes Benchmark"
    Run kube-bench periodically against node configuration — complement app-layer controls.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Pod rejected by PSS | Non-root, caps, volumes | Fix securityContext; add emptyDir for /tmp |
| Service unreachable after NetworkPolicy | Missing ingress rule | Trace path; add allow rule for source labels |
| Kyverno blocks deploy | Policy mismatch | `kubectl describe clusterpolicy`; check PolicyReport |
| SealedSecret won't decrypt | Wrong cluster cert | Re-seal with current cluster public key |
| Image pull fails after policy | Unsigned image | Sign in CI or adjust verifyImages policy |
| Argo CD sync forbidden | RBAC too narrow | Expand Role verbs or resource list |

## Summary

- **Defense in depth** combines RBAC, admission control, pod hardening, network segmentation, and supply-chain verification
- **Pod Security Standards** enforce restricted profiles in application namespaces
- **NetworkPolicies** implement default-deny with explicit allow paths for VoteStack tiers
- **Kyverno/Gatekeeper** block non-compliant manifests before pods are scheduled
- **Sealed Secrets or External Secrets** keep credentials out of plaintext Git
- Next: [Kubernetes Capstone and Next Steps](kubernetes-capstone-and-next-steps.md)

## Interview Questions

1. What are the three Pod Security Standard profiles and when use each?
2. Why implement default-deny NetworkPolicies?
3. How does admission control differ from RBAC?
4. Explain the blast radius if Argo CD has cluster-admin and the GitOps repo is compromised.
5. What is seccomp RuntimeDefault and why enable it?
6. Compare Sealed Secrets vs External Secrets Operator.
7. How do you allow DNS in a default-deny egress NetworkPolicy?
8. What supply-chain controls apply before an image runs in Kubernetes?
9. How would you audit who deleted a production Deployment?
10. What is the difference between Pod Security Admission and Kyverno?

??? tip "Sample Answers (Questions 2, 4, and 10)"

    **Q2 — Default-deny NetworkPolicy:** Without policies, any compromised pod can reach any service — lateral movement to postgres, redis, or the Kubernetes API. Default-deny blocks all traffic; explicit allow rules document and enforce the intended architecture (ingress → api only; api → data tier only). Principle of least privilege at network layer.

    **Q4 — GitOps cluster-admin blast radius:** Attacker merges malicious manifest to GitOps repo → Argo CD syncs → attacker gets any cluster resource including Secrets cluster-wide, persistent volumes, or crypto-mining DaemonSets. Scoped namespace Role limits damage to votestack namespace even if repo is compromised.

    **Q10 — PSA vs Kyverno:** Pod Security Admission is built into Kubernetes — enforces pod-level standards (restricted/baseline) via namespace labels. Kyverno is a flexible admission webhook — custom policies (image tags, labels, resource limits, signature verification). PSA is baseline pod hardening; Kyverno extends to organizational policy-as-code.

## Related Tutorials

- [Monitoring and Logging in Kubernetes](monitoring-and-logging-in-kubernetes.md) *(previous)*
- [Kubernetes Capstone and Next Steps](kubernetes-capstone-and-next-steps.md) *(next)*
- [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md)
- [ConfigMaps and Secrets](configmaps-and-secrets.md)
- [Docker Security Hardening](../docker/docker-security-hardening.md)
- [Network Security Hardening](../networking/network-security-hardening.md)
- [Kubernetes – Category Overview](index.md)

## References

- [Kubernetes – Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Kubernetes – Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Kyverno – Policies](https://kyverno.io/policies/)
- [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/)
- [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [NSA/CISA Kubernetes Hardening Guide](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.1_20220829.PDF)
