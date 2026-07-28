---
title: GitOps and CI/CD with Kubernetes
description: Deliver Kubernetes workloads with GitOps — Argo CD and Flux, CI pipelines that build and scan images, and declarative cluster reconciliation.
difficulty: advanced
estimated_time: "50 min"
author: Shaik Basha
category: kubernetes
tags:
  - kubernetes
  - gitops
  - cicd
  - argocd
  - flux
prerequisites:
  - Helm Package Management
  - RBAC and Kubernetes Security Basics
  - ConfigMaps and Secrets
comments: false
---

# GitOps and CI/CD with Kubernetes

## Overview

Building container images in CI and applying manifests by hand does not scale. **GitOps** treats Git as the single source of truth: every cluster change is a commit, every deployment is a reconciliation loop, and drift is automatically corrected or flagged. Combined with CI pipelines that build, test, scan, and push images, you get repeatable delivery from laptop to production.

This tutorial covers the GitOps mental model, Argo CD and Flux patterns, separating CI from CD, and wiring a pipeline that updates a manifest repository consumed by your cluster.

This is **Tutorial 16** in **Module 6: Production** of the REBASH Academy Kubernetes series.

## Prerequisites

- [Helm Package Management](helm-package-management.md)
- [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md)
- [ConfigMaps and Secrets](configmaps-and-secrets.md)
- [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md)
- [Ingress and External Access](ingress-and-external-access.md)
- A Kubernetes cluster (kind, minikube, or cloud) with `kubectl` configured
- Git hosting (GitHub or GitLab) and container registry access
- Optional: [Git in CI/CD and DevOps](../git/git-in-ci-cd-and-devops.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain GitOps principles and how they differ from imperative `kubectl apply`
- [ ] Design a repository layout separating application code, container builds, and cluster manifests
- [ ] Configure Argo CD (or Flux) to sync Helm charts or Kustomize overlays from Git
- [ ] Wire CI to build, scan, and push images — updating manifest tags without direct cluster access
- [ ] Implement promotion flows across dev, staging, and production environments
- [ ] Handle rollbacks, drift detection, and secrets in a GitOps workflow

## Architecture Diagram

```d2
direction: right

Dev: "Developer workflow" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        DEV: Developer
        APP: "App repo"
        DEV -> APP: "PR + merge"
    }
    CI: "Continuous Integration" {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        BUILD: "Build + test"
        SCAN: "Trivy scan"
        PUSH: "Push to registry"
        APP -> BUILD
        BUILD -> SCAN
        SCAN -> PUSH
    }
    GitOps: "GitOps repo" {
      style: {
        fill: "#ffedd5"
        stroke: "#ea580c"
      }
        MANI: "Manifests / Helm values"
        PUSH -> MANI: "update image tag"
    }
    Cluster: "Kubernetes cluster" {
      style: {
        fill: "#f3e8ff"
        stroke: "#9333ea"
      }
        ARGO: "Argo CD / Flux"
        K8S: Workloads
        MANI -> ARGO
        ARGO -> K8S: reconcile
    }
    REG: "Container registry"
    CI.PUSH -> REG
    Cluster.K8S -> REG: pull
```

## Theory

### What is GitOps?

**GitOps** is an operational model where:

1. **Declarative** — desired state lives in Git (YAML, Helm, Kustomize)
2. **Versioned** — every change has author, timestamp, and review history
3. **Automated** — an agent in the cluster pulls and applies changes
4. **Continuously reconciled** — the agent detects and fixes drift

| Imperative deploy | GitOps deploy |
|-------------------|---------------|
| `kubectl set image ...` from CI | CI commits new tag to Git; agent syncs |
| Cluster state unknown vs repo | Agent compares live vs Git |
| Rollback = re-run old pipeline | Rollback = `git revert` |
| Credentials in CI for cluster | CI never needs kubeconfig |

The [OpenGitOps](https://opengitops.dev/) principles formalize this model adopted by platform teams at scale.

### CI vs CD separation

| Phase | Responsibility | Tools |
|-------|----------------|-------|
| **CI** | Compile, test, build image, scan, push | GitHub Actions, GitLab CI, Jenkins |
| **CD (GitOps)** | Apply manifests, health checks, sync status | Argo CD, Flux, Fleet |

CI outputs **immutable artifacts** (image digests). CD consumes **manifest updates** pointing to those artifacts. Never let CI run `kubectl apply` against production with long-lived cluster-admin credentials.

### Repository strategies

**Monorepo:** application code and `deploy/` manifests in one repository. Simple for small teams.

**Polyrepo (recommended at scale):**

| Repository | Contents |
|------------|----------|
| `votestack-app` | Source code, Dockerfiles, unit tests |
| `votestack-gitops` | Helm charts, environment values, Argo CD Applications |
| `platform-charts` | Shared library charts (optional) |

Environment promotion updates image tags in `values-staging.yaml` → `values-prod.yaml` via PR, not by retagging images.

### Argo CD vs Flux

| Feature | Argo CD | Flux |
|---------|---------|------|
| UI | Rich web UI | Minimal (use Weave GitOps or CLI) |
| Helm | Native support | HelmRelease CRD |
| Multi-tenancy | Projects + RBAC | Namespace-scoped |
| Image automation | Image Updater (optional) | Image Automation controllers |
| CNCF status | Graduated | Graduated |

Both are production-grade. This tutorial uses **Argo CD** for labs; Flux patterns translate directly.

### Sync policies and health

Argo CD Application spec controls behavior:

| Policy | Effect |
|--------|--------|
| `automated.prune: true` | Delete resources removed from Git |
| `automated.selfHeal: true` | Revert manual kubectl edits |
| `syncOptions: CreateNamespace=true` | Create target namespace if missing |

Health assessment uses built-in rules (Deployment available replicas) and custom resources (CRDs).

## Hands-on Lab

These labs use a **VoteStack** GitOps layout — the same poll app from the [Docker capstone](../docker/docker-capstone-and-next-steps.md), now deployed via Helm and Argo CD.

### Lab 1 — Scaffold the GitOps repository

Create `votestack-gitops/` with this structure:

```text
votestack-gitops/
├── apps/
│   └── votestack/
│       └── application.yaml      # Argo CD Application
├── charts/
│   └── votestack/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       └── templates/
│           ├── deployment-api.yaml
│           ├── service-api.yaml
│           └── ingress.yaml
└── README.md
```

`charts/votestack/values.yaml` (excerpt):

```yaml
api:
  image:
    repository: ghcr.io/org/votestack-api
    tag: "abc1234"
  replicas: 2
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 256Mi

ingress:
  enabled: true
  host: votestack.local
```

Commit and push to GitHub.

### Lab 2 — Install Argo CD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f \
  https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl -n argocd wait --for=condition=available deployment/argocd-server --timeout=300s

# Port-forward UI (or configure Ingress)
kubectl port-forward svc/argocd-server -n argocd 8080:443 &
ARGO_PASS=$(kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath='{.data.password}' | base64 -d)
echo "Login: admin / $ARGO_PASS"
```

Change the admin password after first login.

### Lab 3 — Register the Application

`apps/votestack/application.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: votestack
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

Apply from the GitOps repo (bootstrap pattern) or paste in UI:

```bash
kubectl apply -f apps/votestack/application.yaml
argocd app get votestack
argocd app sync votestack
```

Verify pods: `kubectl get pods -n votestack`

### Lab 4 — CI pipeline updates image tag

GitHub Actions workflow in the **application** repo (`.github/workflows/ci.yml`):

{% raw %}
```yaml
name: CI
on:
  push:
    branches: [main]
jobs:
  build-api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push
        env:
          IMAGE: ghcr.io/${{ github.repository_owner }}/votestack-api
        run: |
          docker build -t "$IMAGE:${{ github.sha }}" ./api
          echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u "${{ github.actor }}" --password-stdin
          docker push "$IMAGE:${{ github.sha }}"
      - name: Update GitOps manifest
        env:
          GITOPS_TOKEN: ${{ secrets.GITOPS_PAT }}
        run: |
          git clone https://x-access-token:${GITOPS_TOKEN}@github.com/org/votestack-gitops.git
          cd votestack-gitops
          yq -i '.api.image.tag = "${{ github.sha }}"' charts/votestack/values-dev.yaml
          git config user.email "ci@org.com"
          git config user.name "CI Bot"
          git commit -am "deploy(api): ${{ github.sha }}"
          git push
```
{% endraw %}

Argo CD detects the commit within ~3 minutes and syncs automatically.

### Lab 5 — Promotion to staging

Never copy tags manually in prod. Open a PR in `votestack-gitops`:

```bash
# After dev soak, promote tag
cp charts/votestack/values-dev.yaml charts/votestack/values-staging.yaml
# Edit staging-specific overrides (replicas, ingress host)
git checkout -b promote/abc1234-to-staging
git commit -am "promote: api abc1234 to staging"
git push -u origin HEAD
```

Merge after review. Staging Application uses `values-staging.yaml`.

### Lab 6 — Rollback via Git

Bad deployment? Revert the manifest commit:

```bash
cd votestack-gitops
git revert HEAD
git push
# Argo CD syncs previous tag automatically
argocd app history votestack
argocd app rollback votestack <revision>
```

## Commands & Code

```bash
# Argo CD CLI essentials
argocd login localhost:8080 --username admin --password "$ARGO_PASS" --insecure
argocd app list
argocd app diff votestack
argocd app sync votestack --prune
kubectl -n argocd get applications

# Flux equivalent (if using Flux)
flux install
flux create source git votestack --url=https://github.com/org/votestack-gitops --branch=main
flux create helmrelease votestack --source=GitRepository/votestack --chart=./charts/votestack
flux get helmreleases -A
```

| Command | Description |
|---------|-------------|
| `argocd app diff` | Show live vs Git drift |
| `argocd app sync` | Trigger manual reconciliation |
| `kubectl apply -k` | Kustomize apply (alternative to Helm) |

## Common Mistakes

!!! warning "CI with cluster-admin kubeconfig"
    Pipelines that `kubectl apply` directly bypass Git audit trails and store powerful credentials in CI. Use GitOps agents with scoped RBAC instead.

!!! warning "Mutable `:latest` tags in Git"
    Always pin image tags or digests in values files. `:latest` makes rollbacks and forensics impossible.

!!! warning "Automated prune on first sync"
    Test `prune: true` in dev first — a wrong manifest path can delete production resources.

!!! warning "Secrets committed to Git"
    Never commit plaintext Secrets. Use Sealed Secrets, External Secrets Operator, or SOPS-encrypted files.

!!! warning "Skipping manifest review in promotion PRs"
    Treat GitOps repo changes with the same rigor as application code — include diff of values and resource impact.

## Best Practices

!!! tip "One Application per environment"
    Separate Argo CD Applications for dev/staging/prod with different value files and sync policies — prod may require manual sync approval.

!!! tip "Sign and scan in CI, verify in cluster"
    Trivy/Grype in CI; admission policies (OPA Gatekeeper, Kyverno) in cluster reject unsigned or critical CVE images.

!!! tip "Use ApplicationSets for multi-cluster"
    ApplicationSet generators deploy the same chart to many clusters with cluster-specific values.

!!! tip "Observability on sync status"
    Alert when Argo CD app is `Degraded` or `OutOfSync` beyond threshold — sync failures are production incidents.

!!! tip "Document bootstrap procedure"
    First cluster install requires applying the root Application manually — document this chicken-and-egg step in runbooks.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| App stuck OutOfSync | Manual kubectl edit | Enable selfHeal or revert manual change |
| ImagePullBackOff after sync | Tag not pushed or wrong registry | Verify CI push; check imagePullSecrets |
| Helm template error | Invalid values | `helm template` locally before commit |
| Permission denied on sync | Argo CD RBAC | Grant project role for namespace |
| Slow sync loop | Large chart / many resources | Split apps; use sync waves |
| CI cannot push to GitOps repo | Token scope | PAT needs `contents: write` on gitops repo |

## Summary

- **GitOps** makes Git the source of truth — cluster agents reconcile desired state continuously
- **Separate CI from CD** — CI builds and pushes images; CD updates manifests; never apply prod from CI with admin creds
- **Argo CD and Flux** are CNCF-graduated GitOps controllers supporting Helm, Kustomize, and raw YAML
- **Promotion** flows through PRs updating environment-specific values files
- **Rollbacks** are Git reverts or Argo CD history rollbacks — fast and auditable
- Next: [Production Patterns — HPA, PDB, and Affinity](production-patterns-hpa-pdb-and-affinity.md)

## Interview Questions

1. What are the four core principles of GitOps?
2. Why should CI not run `kubectl apply` against production?
3. How does Argo CD detect and handle configuration drift?
4. Explain the difference between promoting an image tag and rebuilding for each environment.
5. What is the bootstrap problem in GitOps, and how do teams solve it?
6. Compare monorepo vs polyrepo strategies for GitOps.
7. How do you manage secrets in a GitOps workflow?
8. What does `automated.prune: true` do, and what risk does it carry?
9. How would you roll back a bad deployment using GitOps?
10. When would you choose Flux over Argo CD?

??? tip "Sample Answers (Questions 1, 3, and 9)"

    **Q1 — GitOps principles:** (1) Declarative — desired state described in Git; (2) Versioned and immutable — every change is a commit with audit history; (3) Pulled automatically — agents in the cluster pull changes; (4) Continuously reconciled — agents compare live vs desired and correct drift.

    **Q3 — Drift detection:** Argo CD continuously compares live cluster resources with the rendered manifest from Git. Status shows `Synced` or `OutOfSync`. With `selfHeal: true`, it re-applies Git state when someone kubectl-edits resources. `argocd app diff` shows the exact field-level differences.

    **Q9 — Rollback:** Option A: `git revert` the commit that bumped the bad image tag — Argo CD syncs the previous tag. Option B: `argocd app rollback votestack <revision>` to a known-good deployment history entry. Option A is preferred for audit trail in Git.

## Related Tutorials

- [Helm Package Management](helm-package-management.md) *(previous)*
- [Production Patterns — HPA, PDB, and Affinity](production-patterns-hpa-pdb-and-affinity.md) *(next)*
- [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md)
- [ConfigMaps and Secrets](configmaps-and-secrets.md)
- [Git in CI/CD and DevOps](../git/git-in-ci-cd-and-devops.md)
- [Docker in CI/CD Pipelines](../docker/docker-in-ci-cd-pipelines.md)
- [Kubernetes – Category Overview](index.md)

## References

- [OpenGitOps Principles](https://opengitops.dev/)
- [Argo CD – Getting Started](https://argo-cd.readthedocs.io/en/stable/getting_started/)
- [Flux – Documentation](https://fluxcd.io/flux/)
- [CNCF GitOps Working Group](https://github.com/cncf/tag-app-delivery/tree/main/gitops)
- [Google SRE – Release Engineering](https://sre.google/sre-book/release-engineering/)
- [REBASH Academy – GitLab CI/CD Overview](../gitlab/index.md)
