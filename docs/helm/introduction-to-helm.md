---
title: "Introduction to Helm"
description: "Understand what Helm is, why Kubernetes teams use charts, and how package management fits Cloud and DevOps delivery."
difficulty: intermediate
estimated_time: "30–45 min"
technology: helm
category: helm
module: "Module 1 · Helm Fundamentals"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - helm
  - kubernetes
prerequisites:
  - kubernetes/index
next:
  - helm/helm-architecture-and-components
related:
  - kubernetes/helm-package-management
labs: []
projects: []
interview: interview/helm
certifications:
  - CKAD
  - CKA
tags:
  - helm
  - kubernetes
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---


# Introduction to Helm

## Overview







Explain what Helm solves for Kubernetes teams and define chart, release, and repository in ops language.

**Helm** is the package manager for Kubernetes. A **chart** is a versioned bundle of templates and defaults; a **release** is an installed instance. This course is **Helm for Kubernetes Engineers** — production charts, not toy demos.

This is a core tutorial in **Module 1 · Helm Fundamentals** of the REBASH Academy **Helm for Kubernetes Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Kubernetes](../kubernetes/index.md) — Deployments, Services, kubectl apply basics

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] State problems Helm solves vs raw YAML  
- [ ] Define chart, release, repository  
- [ ] Contrast imperative apply vs packaged releases  
- [ ] Name when *not* to use Helm

## Architecture







This topic’s control points and relationships are shown below.

![Helm architecture](../assets/excalidraw/helm-architecture.svg)

## Theory







### What it is

**Helm** is the de facto package manager for Kubernetes. Instead of applying loose YAML files by hand, you install a **chart** — a versioned directory (or `.tgz` archive) that contains templates, default values, and metadata. An installed instance of a chart is a **release**: a named deployment in a namespace with history you can upgrade or roll back. Charts are published from **repositories** (classic HTTP indexes) or **OCI** registries (container-style references such as `oci://…`).

Three words you will use every day:

| Term | Meaning |
|------|---------|
| Chart | Packaged templates + `values.yaml` + `Chart.yaml` |
| Release | One installed instance of a chart (name + namespace + revisions) |
| Repository / OCI | Where teams discover and pull charts |

### Why it matters

Raw `kubectl apply` works for a single environment. It breaks down when you need the same app shape in dev, staging, and production with different replicas, images, and ingress hosts. Helm gives you parameterisation (`values`), a shared package teams can reuse, and release history for rollback. Platform teams publish “golden” charts so product squads do not reinvent Deployments and Services. In GitOps workflows, controllers such as Argo CD and Flux treat Helm charts as first-class deployable units.

### How it works

You (or CI/GitOps) run the Helm CLI against a cluster kubeconfig. Helm fetches the chart, merges default values with your overrides, renders Go templates into plain Kubernetes manifests, and applies them through the API server. Helm 3 stores release metadata in the cluster (Secrets or ConfigMaps in the release namespace). Each upgrade creates a new **revision**; `helm rollback` re-applies an earlier revision’s rendered set.

### Key concepts and comparisons

| Pain without Helm | Helm answer |
|-------------------|-------------|
| Copy-paste YAML per env | Values overrides (`-f`, `--set`) |
| No versioned app package | Chart `version` + informational `appVersion` |
| Manual rollback | `helm rollback` or GitOps revert of values/chart |
| Hard to share standards | Reusable application charts and library charts |

**Helm vs Kustomize vs plain YAML:** use plain YAML or Kustomize when a small, mostly static set of manifests is enough. Prefer Helm when you need rich parameterisation, dependency composition, and release lifecycle across many environments.

### Common pitfalls

- Helm is not a second control plane — Kubernetes still owns Pods and Deployments after apply.
- A chart is not a running app; the **release** is what you operate day to day.
- Helm does not replace GitOps; production teams usually let a controller run Helm, not laptops.
- Over-templating every field makes charts unreadable — keep defaults sensible and overrides intentional.

## Hands-on Lab

### Objective

Author a minimal Helm chart by hand, lint and render it offline, then install a **release** and capture evidence that distinguishes the **chart** (source package) from the **release** (named cluster instance).

### Prerequisites

- Helm 3.x (`helm version`)
- kubectl configured against kind or minikube (optional for install)
- Writable workspace at `~/rebash-helm/module-01`

### Lab environment

Workspace: `~/rebash-helm/module-01` on your workstation; cluster optional until Task 4.

```bash title="Terminal"
mkdir -p ~/rebash-helm/module-01/rebash-app/templates && cd ~/rebash-helm/module-01
```

### Real-world scenario

Your platform team ships internal services as small Helm charts. Before merging, you must prove the chart lints cleanly, renders expected Kubernetes kinds, and — when a cluster is available — installs as a named release in an isolated namespace.

### Step-by-step tasks

#### Task 1 – Chart metadata and defaults

Create `rebash-app/Chart.yaml`:

```yaml title="Chart.yaml"
apiVersion: v2
name: rebash-app
description: Minimal REBASH introduction chart
type: application
version: 0.1.0
appVersion: "1.27"
```

Create `rebash-app/values.yaml`:

```yaml title="values.yaml"
replicaCount: 1
image:
  repository: nginxinc/nginx-unprivileged
  tag: "1.27-alpine"
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8080
```

#### Task 2 – Deployment and Service templates

Create `rebash-app/templates/_helpers.tpl`:

{% raw %}
```
{{- define "rebash-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "rebash-app.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
```
{% endraw %}

Create `rebash-app/templates/deployment.yaml`:

{% raw %}
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "rebash-app.fullname" . }}
  labels:
    app.kubernetes.io/name: {{ include "rebash-app.name" . }}
    app.kubernetes.io/instance: {{ .Release.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ include "rebash-app.name" . }}
      app.kubernetes.io/instance: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {{ include "rebash-app.name" . }}
        app.kubernetes.io/instance: {{ .Release.Name }}
    spec:
      containers:
        - name: web
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.service.port }}
```
{% endraw %}

Create `rebash-app/templates/service.yaml`:

{% raw %}
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "rebash-app.fullname" . }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.port }}
  selector:
    app.kubernetes.io/name: {{ include "rebash-app.name" . }}
    app.kubernetes.io/instance: {{ .Release.Name }}
```
{% endraw %}

#### Task 3 – Lint and render (offline)

```bash title="Terminal"
cd ~/rebash-helm/module-01
helm lint rebash-app | tee lint-m01.txt
helm template demo rebash-app --namespace rebash-helm-m01 | tee render-m01.yaml
grep -E '^kind:' render-m01.yaml | sort | uniq -c | tee kinds-m01.txt
grep -q 'kind: Deployment' render-m01.yaml
grep -q 'kind: Service' render-m01.yaml
grep -q 'nginxinc/nginx-unprivileged:1.27-alpine' render-m01.yaml
```

!!! example "Expected output"
    `lint-m01.txt` shows 0 chart(s) failed; `kinds-m01.txt` lists Deployment and Service; rendered image uses the pinned tag.


#### Task 4 – Install release and prove chart vs release

Create `namespace.yaml`:

```yaml title="namespace.yaml"
apiVersion: v1
kind: Namespace
metadata:
  name: rebash-helm-m01
```

```bash title="Terminal"
cd ~/rebash-helm/module-01
if command -v helm >/dev/null && kubectl cluster-info >/dev/null 2>&1; then
  kubectl apply -f namespace.yaml
  helm upgrade --install demo rebash-app -n rebash-helm-m01 --wait --timeout 120s | tee install-m01.txt
  helm list -n rebash-helm-m01 | tee list-m01.txt
  helm get metadata demo -n rebash-helm-m01 | tee metadata-m01.txt
  grep -E '^name:|^version:|^app_version:' metadata-m01.txt | tee chart-vs-release-m01.txt
  kubectl get deploy,svc -n rebash-helm-m01 | tee objects-m01.txt
else
  echo "Skipping install — helm or cluster unavailable; offline lint/template is sufficient" | tee install-m01.txt
fi
```

!!! example "Expected output"
    `list-m01.txt` shows release name `demo` with chart `rebash-app-0.1.0`; `chart-vs-release-m01.txt` shows chart metadata (`name`, `version`, `app_version`) distinct from the release name `demo`.


### Validation steps

- [ ] Chart directory contains `Chart.yaml`, `values.yaml`, and templates
- [ ] `helm lint` passes with no failures
- [ ] `helm template` renders Deployment and Service with pinned image
- [ ] Evidence files distinguish chart package version from release name (when install runs)
- [ ] Optional install completes in namespace `rebash-helm-m01`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `helm lint` template undefined | Missing `_helpers.tpl` | Add `rebash-app.name` and `rebash-app.fullname` helpers |
| Rendered YAML invalid | Bad indentation in template | Re-run `helm template` and inspect `render-m01.yaml` |
| Install watch timeout | Image pull or readiness | `kubectl describe pod -n rebash-helm-m01` |
| Confusing chart and release | Same string used for both | Release name is `demo`; chart name is `rebash-app` — compare `helm list` vs `Chart.yaml` |

### Challenge exercise

Bump `replicaCount` to `2` in a separate `values-scale.yaml` file, re-run `helm template demo rebash-app -f values-scale.yaml`, and assert `replicas: 2` appears in the rendered Deployment.

### Learning outcomes

- Built a minimal chart without `helm create` scaffolding noise
- Ran offline validation with `helm lint` and `helm template`
- Explained the difference between chart (package) and release (installed instance)
- Installed a pinned-image release into an isolated namespace when a cluster is available

### Cleanup

```bash title="Terminal"
helm uninstall demo -n rebash-helm-m01 2>/dev/null || true
kubectl delete namespace rebash-helm-m01 --ignore-not-found
```

## Validation







- [ ] Lab commands run under `~/rebash-helm/module-01/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Introduction to Helm** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations







- Treat credentials and tokens for helm as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes







!!! warning "Helm is not a second control plane — Kubernetes still owns Pods and Deployments after appl"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "A chart is not a running app; the **release** is what you operate day to day."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Introduction to Helm changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting







| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |

## Summary







**Introduction to Helm** is essential for Cloud and DevOps engineers working with helm. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions






1. What problem does Helm solve for Kubernetes packaging?
2. What is a release in Helm 3?
3. How do charts differ from raw manifests?
4. What risks come from installing untrusted charts?
5. What is the difference between `helm template` and `helm install`?

!!! tip "Sample answer — question 2"
    A release is a named instance of a chart running in a cluster (with revision history). Helm tracks it via release metadata stored as Secrets (or ConfigMaps) in the namespace.

!!! tip "Sample answer — question 4"
    Untrusted charts can create privileged workloads, ClusterRoles, or exfiltrate secrets. Always render and review, pin versions, and install into least-privilege namespaces.

## Related Tutorials







- [Course overview](index.md)
- [Helm Architecture and Components](helm-architecture-and-components.md)

## References







- [Helm docs — introduction](https://helm.sh/docs/intro/using_helm/)
