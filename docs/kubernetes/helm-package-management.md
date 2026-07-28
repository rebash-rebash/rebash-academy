---
title: Helm Package Management
description: Package, version, and deploy Kubernetes applications with Helm charts, values files, releases, and templating for repeatable production deployments.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: kubernetes
tags:
  - kubernetes
  - helm
  - charts
  - package-management
  - gitops
  - templating
prerequisites:
  - Complete [Troubleshooting Kubernetes Workloads](troubleshooting-kubernetes-workloads.md)
  - Working kubectl and a Kubernetes cluster
  - Familiarity with Deployments, Services, Ingress, ConfigMaps, and Secrets
comments: false
---

# Helm Package Management

## Overview

Raw YAML manifests do not scale. A microservice platform might deploy hundreds of objects — Deployments, Services, Ingress rules, HPAs, ServiceAccounts, and ConfigMaps — across environments with slightly different values. **Helm** is the CNCF package manager for Kubernetes: it bundles manifests into **charts**, parameterizes them with **values**, and tracks **releases** with version history, rollback, and upgrade semantics.

Platform and DevOps engineers use Helm to ship internal platforms, deploy third-party software (Prometheus, ingress-nginx, cert-manager), and enforce consistent labels, probes, and resource limits. GitOps workflows (Argo CD, Flux) often render Helm charts as the deployment source of truth. This tutorial teaches chart structure, templating, release lifecycle, and production patterns.

This is **Tutorial 15** in **Module 5: Security & Tooling** of the REBASH Academy Kubernetes series. Complete [Troubleshooting Kubernetes Workloads](troubleshooting-kubernetes-workloads.md) first.

## Prerequisites

- Completed [Troubleshooting Kubernetes Workloads](troubleshooting-kubernetes-workloads.md)
- kubectl configured against a running cluster
- Helm 3 installed (`helm version` shows v3.x)
- Understanding of YAML, Deployments, Services, and Ingress from prior tutorials
- Optional: Helm repos accessible from your network (Artifact Hub, Bitnami)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain Helm charts, releases, revisions, and values files
- [ ] Install, upgrade, rollback, and uninstall Helm releases
- [ ] Create a chart with `helm create` and customize templates
- [ ] Use Go templating, conditionals, and `values.yaml` overrides
- [ ] Manage environment-specific configs with `-f values-dev.yaml` layering
- [ ] Lint and dry-run charts before applying to production clusters
- [ ] Install charts from public repositories and inspect rendered manifests
- [ ] Apply Helm best practices for secrets, labels, and chart versioning

## Architecture

Helm client renders chart templates + values into manifests, then applies them to the cluster as a tracked release.

```d2
direction: right

DEV: "Developer / CI"
    CHART: "Helm Chart\ntemplates + values"
    HELM: "Helm CLI"
    API: "Kubernetes API"
    REL: "Release\nrevision history"
    DEV -> HELM: "helm upgrade --install"
    CHART -> HELM
    HELM -> API: "render + apply"
    HELM -> REL: "store metadata"
    REL -> HELM: "helm rollback"
```

## Theory

### Helm 3 Architecture

Helm 3 removed Tiller — the server-side component from Helm 2. Today:

| Component | Role |
|-----------|------|
| **Helm CLI** | Local client; renders templates and calls Kubernetes API |
| **Chart** | Directory of templates, values, and metadata |
| **Release** | Named instance of a chart deployed to a cluster |
| **Revision** | Numbered snapshot of a release on upgrade |

Release metadata lives in Secrets (default) or ConfigMaps in the release namespace — `helm history` reads this store.

### Chart Structure

```text
mychart/
├── Chart.yaml          # Chart metadata (name, version, appVersion)
├── values.yaml         # Default configuration values
├── charts/             # Dependent subcharts
├── templates/          # Kubernetes manifests with Go templates
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── _helpers.tpl    # Named template partials
│   └── NOTES.txt       # Post-install notes
└── .helmignore
```

**Chart.yaml** version follows SemVer — increment on chart changes. **appVersion** tracks the application image version for documentation; it does not auto-update images unless templates reference it.

### Values and Overrides

`values.yaml` provides defaults. Override at install time:

```bash
helm upgrade --install myapp ./mychart \
  -f values.yaml \
  -f values-prod.yaml \
  --set replicaCount=5 \
  --set image.tag=v2.1.0 \
  -n production --create-namespace
```

Later files and `--set` take precedence. This layering supports dev/staging/prod without duplicating charts.

### Templating Basics

Templates use Go `text/template` with Sprig functions:

{% raw %}
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          {{- if .Values.resources }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          {{- end }}
```
{% endraw %}

Key concepts:

| Syntax | Meaning |
|--------|---------|
| `{{ "{{" }} .Values.replicaCount {{ "}}" }}` | Value from values.yaml |
| `{{ "{{" }} .Chart.Name {{ "}}" }}` | Chart metadata |
| `{{ "{{" }} .Release.Name {{ "}}" }}` | Release name from install command |
| `{{ "{{- if .Values.ingress.enabled }}" }}` | Conditional resource |
| `{{ "{{- include \"mychart.labels\" . }}" }}` | Reusable partial from `_helpers.tpl` |

### Release Lifecycle

```bash
helm install myrelease ./chart      # revision 1
helm upgrade myrelease ./chart      # revision 2
helm history myrelease
helm rollback myrelease 1           # back to revision 1
helm uninstall myrelease
```

`helm upgrade --install` (alias `helm upgrade -i`) is idempotent — creates if missing, upgrades if exists. CI/CD pipelines should always use upgrade --install.

### Chart Repositories

Helm charts publish to HTTP repositories or OCI registries:

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo nginx
helm install my-nginx bitnami/nginx -n web --create-namespace
```

Artifact Hub (artifacthub.io) indexes public charts. Verify publisher trust before production installs.

### Dependencies (Subcharts)

**Chart.yaml** dependencies:

```yaml
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
```

Run `helm dependency update` to vendor subcharts into `charts/`. Parent values pass to subcharts under the dependency key: `postgresql.auth.password`.

### Helm vs kubectl apply vs Kustomize

| Tool | Strength | Weakness |
|------|----------|----------|
| **kubectl apply** | Simple, native | No release history or parameterization |
| **Kustomize** | Patch-based overlays, built into kubectl | Less packaging ecosystem |
| **Helm** | Releases, rollback, chart sharing | Template complexity; drift if CLI and GitOps diverge |

Many teams render Helm in CI and commit manifests, or use GitOps operators with native Helm support.

### Secrets Management

Never commit plaintext production secrets to `values.yaml`. Options:

- External Secrets Operator syncing from Vault/AWS SM
- Sealed Secrets or SOPS-encrypted values files
- CI-injected `--set` from secret store at deploy time
- Helm secrets plugins (community)

Use `helm template` or `helm install --dry-run=server` to validate without persisting.

## Hands-on Lab

### Step 1 – Verify Helm installation

**Command:**

```bash
helm version
kubectl cluster-info | head -3
helm env | grep HELM_
```

**Explanation:** Helm 3 communicates directly with Kubernetes API using kubeconfig credentials — no cluster-admin Tiller required.

**Expected output:**

```text
version.BuildInfo{Version:"v3.x.x", ...}
Kubernetes control plane is running at ...
HELM_NAMESPACE="default"
```

### Step 2 – Create a chart from scratch

**Command:**

```bash
mkdir -p ~/helm-lab && cd ~/helm-lab
helm create web-app
tree web-app -L 2 2>/dev/null || find web-app -maxdepth 2 -type f
cat web-app/Chart.yaml
head -20 web-app/values.yaml
```

**Explanation:** `helm create` scaffolds a standard chart with Deployment, Service, Ingress templates, and helpers. Customize rather than writing from zero.

**Expected output:**

```text
web-app/
├── Chart.yaml
├── values.yaml
├── charts/
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ...
```

### Step 3 – Customize values and dry-run

**Command:**

```bash
cd ~/helm-lab/web-app
cat >> values.yaml <<'EOF'

# Lab overrides
replicaCount: 2
ingress:
  enabled: false
resources:
  requests:
    cpu: 50m
    memory: 64Mi
  limits:
    cpu: 200m
    memory: 128Mi
EOF

helm lint .
helm template web-preview . --namespace helm-lab | head -60
```

**Explanation:** `helm lint` catches syntax errors and best-practice warnings. `helm template` renders locally without cluster access — ideal for CI and code review.

**Expected output:**

```text
==> Linting .
[INFO] Chart.yaml: icon is recommended
1 chart(s) linted, 0 failure(s)
---
# Source: web-app/templates/service.yaml
apiVersion: v1
kind: Service
...
```

### Step 4 – Install release

**Command:**

```bash
helm upgrade --install web-app . \
  --namespace helm-lab \
  --create-namespace \
  --wait --timeout 120s

helm list -n helm-lab
kubectl get deploy,svc,pods -n helm-lab
helm status web-app -n helm-lab
```

**Explanation:** `--wait` blocks until pods are Ready — surfaces probe and scheduling failures immediately.

**Expected output:**

```text
NAME     NAMESPACE  REVISION  STATUS    CHART          APP VERSION
web-app  helm-lab   1         deployed  web-app-0.1.0  1.16.0
```

### Step 5 – Upgrade with new values

**Command:**

```bash
helm upgrade web-app . \
  -n helm-lab \
  --set replicaCount=3 \
  --set resources.limits.memory=256Mi \
  --wait

helm history web-app -n helm-lab
kubectl get deploy web-app -n helm-lab -o jsonpath='{.spec.replicas}{"\n"}'
```

**Explanation:** Each upgrade increments revision number. History enables rollback without re-running CI.

**Expected output:**

```text
REVISION  UPDATED                   STATUS      CHART
1         ...                       superseded  web-app-0.1.0
2         ...                       deployed    web-app-0.1.0
3
```

### Step 6 – Rollback a release

**Command:**

```bash
helm rollback web-app 1 -n helm-lab --wait
helm history web-app -n helm-lab
kubectl get deploy web-app -n helm-lab -o jsonpath='{.spec.replicas}{"\n"}'
```

**Explanation:** Rollback creates a new revision (3) with spec from revision 1 — not a destructive revert. Audit trail remains intact.

**Expected output:**

```text
REVISION  STATUS
1         superseded
2         superseded
3         deployed   # content matches revision 1
2
```

### Step 7 – Install from a public repository

**Command:**

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo bitnami/nginx --versions | head -5
helm upgrade --install demo-nginx bitnami/nginx \
  -n helm-lab \
  --set replicaCount=1 \
  --set service.type=ClusterIP \
  --wait --timeout 120s

kubectl get pods -n helm-lab -l app.kubernetes.io/name=nginx
```

**Explanation:** Third-party charts accelerate standard software deployment. Always review default values and security settings before production.

**Expected output:**

```text
NAME        CHART VERSION  APP VERSION
bitnami/nginx  18.x.x       1.27.x
demo-nginx-...  1/1  Running  0  30s
```

### Step 8 – Uninstall and clean up

**Command:**

```bash
helm uninstall web-app -n helm-lab
helm uninstall demo-nginx -n helm-lab
kubectl delete namespace helm-lab --wait=false
cd ~ && rm -rf ~/helm-lab
helm list -A | grep helm-lab || echo "All helm-lab releases removed"
```

**Explanation:** `helm uninstall` removes release-tracked resources. Resources created outside Helm labels may orphan — use consistent labeling.

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

| Command | Description | Example |
|---------|-------------|---------|
| `helm create` | Scaffold new chart | `helm create mychart` |
| `helm lint` | Validate chart | `helm lint ./mychart` |
| `helm template` | Render locally | `helm template rel ./mychart -f prod.yaml` |
| `helm upgrade --install` | Idempotent deploy | `helm upgrade -i app ./chart -n prod` |
| `helm rollback` | Revert to revision | `helm rollback app 2 -n prod` |
| `helm uninstall` | Remove release | `helm uninstall app -n prod` |

### Minimal custom chart values

`values.yaml` for a production web app:

```yaml
replicaCount: 3

image:
  repository: ghcr.io/myorg/web
  tag: "v2.4.1"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: web.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

Environment override `values-staging.yaml`:

```yaml
replicaCount: 1
ingress:
  hosts:
    - host: web.staging.example.com
      paths:
        - path: /
          pathType: Prefix
autoscaling:
  enabled: false
```

Deploy: `helm upgrade -i web ./chart -f values.yaml -f values-staging.yaml -n staging`

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Pinning chart version but not image tag"
    `helm upgrade bitnami/nginx` without `--version` pulls latest chart — behaviour may change. Pin both chart version and `image.tag` in values.

!!! warning "Storing secrets in values.yaml committed to Git"
    Plaintext passwords in charts leak via Git history. Use External Secrets, SOPS, or CI-injected overrides.

!!! warning "Editing live manifests outside Helm"
    `kubectl edit` on Helm-managed resources causes **drift** — next upgrade overwrites or conflicts. Change values and upgrade.

!!! warning "Skipping helm lint and dry-run in CI"
    Template errors discovered in production are expensive. Run `helm lint` and `helm template` on every PR.

## Best Practices

!!! tip "One release name per app per namespace"
    Convention: `<app>-<env>` — `payments-prod`. Document in runbooks for rollback commands.

!!! tip "Use _helpers.tpl for standard labels"
    Include `app.kubernetes.io/name`, `instance`, `managed-by: Helm` for consistency with ecosystem tools.

!!! tip "SemVer chart versions on every change"
    Bump `Chart.yaml` version on template changes — even patch bumps help history correlation.

!!! tip "Integrate with GitOps"
    Argo CD and Flux support Helm natively. Single source of truth in Git; cluster reconciles continuously.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Error: rendered manifests contain a resource that already exists` | Orphan resource without Helm labels | Adopt with `helm upgrade --install` and matching labels or delete orphan |
| Upgrade hangs on `--wait` | Pods not Ready | `kubectl get pods`; fix probes; increase `--timeout` |
| Wrong config after upgrade | Values precedence | Check `-f` order; `--set` overrides last |
| `helm rollback` doesn't fix issue | Bad revision rolled forward | Identify good revision via `helm history`; rollback to known good |
| Template renders empty | Condition false | Verify `{{ "{{- if .Values.feature.enabled }}" }}` and values |
| Chart not found | Repo not added or stale | `helm repo add && helm repo update` |

## Summary

- **Helm** packages Kubernetes manifests as **charts** with parameterized **values** and tracked **releases**
- **helm upgrade --install** is the idempotent deploy pattern; **history** and **rollback** provide safe iteration
- **Templates** use Go templating with values, conditionals, and shared partials in `_helpers.tpl`
- Layer **values files** per environment; never commit plaintext production secrets
- **helm lint**, **helm template**, and **--dry-run** validate charts before cluster apply
- Helm complements GitOps — charts are the packaging layer; Git remains the source of truth

## Interview Questions

1. What problem does Helm solve compared to raw kubectl apply?
2. Explain the difference between a Helm chart, a release, and a revision.
3. What changed in Helm 3 compared to Helm 2 regarding cluster security?
4. How do you override default values at install time?
5. What is the purpose of `_helpers.tpl` in a chart?
6. How does `helm rollback` work — does it delete revision history?
7. Why should you avoid `kubectl edit` on Helm-managed resources?
8. Compare Helm with Kustomize — when would you choose each?
9. How do chart dependencies (subcharts) receive configuration from the parent?
10. What commands validate a chart before deploying to production?

??? tip "Sample Answers (Questions 1, 4, and 7)"

    **Q1 — Helm vs kubectl apply:** Raw YAML lacks parameterization, release tracking, and rollback. Helm templating parameterizes manifests for multiple environments from one chart. Releases store revision history — upgrade and rollback are first-class operations. Charts publish to repositories for reuse across teams and clusters.

    **Q4 — Value overrides:** Provide `-f values.yaml` files (later files override earlier), `--set key=value` for individual overrides, and `--set-file` for file content. Precedence: chart defaults < `-f` files left to right < `--set`. Example: `helm upgrade -i app ./chart -f values.yaml -f values-prod.yaml --set replicaCount=5`.

    **Q7 — kubectl edit drift:** Helm tracks managed resources via release metadata and labels. Manual edits change live state without updating release values — the next `helm upgrade` may overwrite edits or fail on three-way merge conflicts. Always change `values.yaml` and run `helm upgrade` to maintain consistent desired state.

## Related Tutorials

- [Kubernetes – Category Overview](index.md)
- [Troubleshooting Kubernetes Workloads](troubleshooting-kubernetes-workloads.md) *(previous — Module 5)*
- [GitOps and CI/CD with Kubernetes](gitops-and-cicd-with-kubernetes.md) *(next — Module 6 Production)*
- [Ingress and External Access](ingress-and-external-access.md)
- [ConfigMaps and Secrets](configmaps-and-secrets.md)
- Cheat sheet: [Kubernetes Cheat Sheet](../cheatsheets/kubernetes.md)
- Interview prep: [Kubernetes Interview Prep](../interview/kubernetes.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [Helm Documentation](https://helm.sh/docs/)
- [Helm Charts Guide](https://helm.sh/docs/topics/charts/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Chart Template Guide](https://helm.sh/docs/chart_template_guide/)
- [Helm Release Management](https://helm.sh/docs/intro/using_helm/#helm-install-and-helm-upgrade)
- [Kubernetes Packaging with Helm (concept)](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- [Artifact Hub — Helm charts](https://artifacthub.io/)
