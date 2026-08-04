---
title: "Progressive Delivery and Sync Windows"
description: "Control when Argo CD syncs with sync windows, roll back safely, tune health checks, and integrate Argo Rollouts for canary and blue-green."
difficulty: advanced
estimated_time: "55–70 min"
technology: argocd
category: argocd
module: "Module 13 · Progressive Delivery"
learning_paths:
  - kubernetes-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - argocd
  - progressive-delivery
  - gitops
prerequisites:
  - argocd/argo-cd-notifications
next:
  - argocd/ci-cd-integration-with-argo-cd
related:
  - kubernetes/health-checks-probes-and-self-healing
  - helm/helm-releases-and-lifecycle
labs: []
projects: []
interview: interview/argocd
certifications:
  - CKA
  - CKAD
tags:
  - argocd
  - sync-windows
  - rollouts
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---

# Progressive Delivery and Sync Windows

## Overview

Not every Git merge should sync to production immediately. **Sync windows** block or allow automated sync during maintenance, change freezes, or business hours. **Rollback** returns an Application to a known-good Git revision or previous live state. **Health checks** tell Argo CD when synced resources are truly ready. For traffic shifting, **Argo Rollouts** implements canary and blue-green — Argo CD syncs the Rollout custom resource; Rollouts owns replica sets and traffic weights.

This is **Tutorial 1** in **Module 13 · Progressive Delivery** of the REBASH Academy **Argo CD for Cloud & DevOps Engineers** series — written for Platform, DevOps, and SRE engineers governing release timing and safety.

## Prerequisites

- [Argo CD Notifications](argo-cd-notifications.md)
- [Health checks and probes](../kubernetes/health-checks-probes-and-self-healing.md)
- **kind** cluster with Argo CD installed ([Installing Argo CD](installing-argo-cd.md))

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Define allow/deny sync windows on AppProject or global ConfigMap
- [ ] Roll back an Application using Git revision or `argocd app rollback`
- [ ] Explain how Argo CD health maps to Deployment, Service, and Rollout status
- [ ] Clarify the split of responsibility between Argo CD and Argo Rollouts
- [ ] Apply sync windows, break health with a bad image, and roll back on a kind cluster

## Architecture

Argo CD governs *when* Git state reaches the cluster; Argo Rollouts governs *how* new versions receive traffic after sync.

![Release lifecycle](../assets/excalidraw/helm-release-lifecycle.svg)

## Theory

### What it is

**Sync windows** are cron-like schedules with `kind: allow` or `deny`, optional duration, manual sync override flags, and scope (applications, namespaces, clusters). Define them on **AppProject** `spec.syncWindows` or globally in `argocd-cm`.

**Rollback** options:

- **Git revert** — preferred GitOps path; merge revert commit, let auto-sync apply.
- **`argocd app rollback`** — selects a previous live revision recorded in Application history.
- **Pin `targetRevision`** — temporary freeze to a tag or SHA.

**Health** uses built-in Lua health scripts per resource kind. Deployments become Healthy when updated replicas are available; Ingresses need load balancer status; Rollouts report Healthy when the canary/stable promotion completes.

**Argo Rollouts** is a separate controller. Argo CD treats `Rollout` like Deployment — syncs manifest from Git. Rollouts performs canary steps, analysis runs, and traffic weight changes via service mesh or ingress.

### Why it matters

Change freezes prevent Friday-evening surprises. Rollback discipline separates “sync succeeded” from “users are safe”. Teams adopting canary without Rollouts often hack replica counts in Git — Rollouts provides a first-class CR with pause, analysis, and promotion.

### How it works

1. Developer merges manifest bump (Deployment or Rollout).
2. Sync window evaluates — auto-sync may queue or skip.
3. Argo CD applies manifests; Rollout controller starts canary if configured.
4. Health transitions Progressing → Healthy (or Degraded on failure).
5. On failure, operator rolls back Git or uses `app rollback`; notifications fire.

### Key concepts and comparisons

| Tool | Responsibility |
|------|----------------|
| Argo CD | Desired state from Git; sync; health aggregation |
| Argo Rollouts | Progressive traffic shift; analysis; promotion |
| Deployment | Rolling update only (no weighted traffic) |

| Rollback method | GitOps purity | Speed |
|-----------------|---------------|-------|
| Git revert | High | Depends on pipeline |
| `argocd app rollback` | Medium | Fast |
| Manual kubectl | Low | Fastest but drifts Git |

### Common pitfalls

- Deny window blocking emergency fixes — allow manual sync override with audit.
- Assuming Healthy Deployment means successful canary — check Rollout status.
- Auto-sync + prune during rollback testing — can delete resources unexpectedly.
- Missing health overrides for custom CRDs — apps stuck Progressing forever.

## Hands-on Lab

### Objective

Deploy a health-aware Application on a **kind** cluster with an AppProject sync window, break health with a bad container image, capture rollback history, roll back with `argocd app rollback`, and prove Synced/Healthy recovery.

### Prerequisites

- **kind** cluster with Argo CD installed ([Installing Argo CD](installing-argo-cd.md))
- `kubectl` and `argocd` CLI logged in
- [Health checks and probes](../kubernetes/health-checks-probes-and-self-healing.md)

### Lab environment

Runtime: **kind** cluster with Argo CD — offline scripts alone are not sufficient for this lab.

``` {.bash .ra-terminal title="Terminal"}
kind create cluster --name rebash-argocd 2>/dev/null || true
export KUBECONFIG="$(kind get kubeconfig --name rebash-argocd)"
mkdir -p ~/rebash-argocd/module-13/{windows,manifests,apps} && cd ~/rebash-argocd/module-13
```

Namespace: `rebash-argocd-m13`.

### Real-world scenario

Production apps auto-sync only outside business hours, but manual sync must remain available for emergencies. A bad image tag merged to Git degraded health in `rebash-argocd-m13`. You apply a sync-window AppProject, sync a good Deployment, introduce a broken image update, capture history, roll back to the last good revision, and prove health recovery.

### Step-by-step tasks

#### Task 1 – Create AppProject with sync window

Create `windows/platform-project.yaml`:

```yaml title="platform-project.yaml"
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: platform-prod
  namespace: argocd
spec:
  description: Production platform apps — weekday change freeze
  sourceRepos:
    - file:///tmp/rebash-argocd/module-13/manifests
    - https://github.com/argoproj/argocd-example-apps.git
    - https://github.com/argoproj/argocd-example-apps
  destinations:
    - namespace: rebash-argocd-m13
      server: https://kubernetes.default.svc
  syncWindows:
    - kind: deny
      schedule: "0 9 * * 1-5"
      duration: 8h
      timeZone: "Asia/Kolkata"
      applications:
        - demo-api-prod
      manualSync: true
    - kind: allow
      schedule: "0 0 * * *"
      duration: 24h
      applications:
        - demo-api-prod
```

Apply and verify sync window configuration:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-argocd/module-13
kubectl apply -f windows/platform-project.yaml | tee project-apply-m13.txt
kubectl get appproject platform-prod -n argocd \
  -o jsonpath='{.spec.syncWindows[0].kind}{" manualSync="}{.spec.syncWindows[0].manualSync}{"\n"}' \
  | tee sync-window-m13.txt
grep -q 'deny manualSync=true' sync-window-m13.txt
```

!!! example "Expected output"
    AppProject applied; deny window allows manual sync override.


#### Task 2 – Create local manifests and Application

Create `manifests/deployment-demo.yaml`:

```yaml title="deployment-demo.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-api
  namespace: rebash-argocd-m13
  labels:
    app: demo-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: demo-api
  template:
    metadata:
      labels:
        app: demo-api
    spec:
      containers:
        - name: api
          image: nginxinc/nginx-unprivileged:1.27-alpine
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /
              port: 8080
            initialDelaySeconds: 2
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
```

Create `manifests/service-demo.yaml`:

```yaml title="service-demo.yaml"
apiVersion: v1
kind: Service
metadata:
  name: demo-api
  namespace: rebash-argocd-m13
spec:
  selector:
    app: demo-api
  ports:
    - port: 80
      targetPort: 8080
```

Create `apps/demo-api-prod.yaml`:

```yaml title="demo-api-prod.yaml"
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: demo-api-prod
  namespace: argocd
spec:
  project: platform-prod
  source:
    repoURL: file:///tmp/rebash-argocd/module-13/manifests
    targetRevision: HEAD
    path: .
  destination:
    server: https://kubernetes.default.svc
    namespace: rebash-argocd-m13
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

Register local repo path and apply:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-argocd/module-13
cp -a ~/rebash-argocd/module-13 /tmp/rebash-argocd/ 2>/dev/null || true
kubectl apply -f apps/demo-api-prod.yaml | tee app-apply-m13.txt
argocd repo add file:///tmp/rebash-argocd/module-13/manifests --name module-13-local --insecure-skip-server-verification 2>/dev/null || true
kubectl wait --for=jsonpath='{.status.sync.status}'=Synced \
  application/demo-api-prod -n argocd --timeout=300s | tee wait-initial-m13.txt
kubectl get deploy,pods -n rebash-argocd-m13 | tee workloads-good-m13.txt
```

!!! example "Expected output"
    Application Synced; `demo-api` Deployment with 2 ready pods in `rebash-argocd-m13`.


#### Task 3 – Break health with bad image and capture history

Create `manifests/deployment-demo-broken.yaml`:

```yaml title="deployment-demo-broken.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-api
  namespace: rebash-argocd-m13
  labels:
    app: demo-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: demo-api
  template:
    metadata:
      labels:
        app: demo-api
    spec:
      containers:
        - name: api
          image: nginxinc/nginx-unprivileged:invalid-tag-999
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /
              port: 8080
            initialDelaySeconds: 2
            periodSeconds: 5
```

Replace the good manifest and sync:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-argocd/module-13
cp manifests/deployment-demo-broken.yaml manifests/deployment-demo.yaml
cp -a ~/rebash-argocd/module-13 /tmp/rebash-argocd/ 2>/dev/null || true
argocd app sync demo-api-prod --prune | tee sync-broken-m13.txt
sleep 30
kubectl get application demo-api-prod -n argocd \
  -o jsonpath='Sync={.status.sync.status} Health={.status.health.status}{"\n"}' \
  | tee broken-health-m13.txt
argocd app history demo-api-prod | tee history-before-rollback-m13.txt
grep -Ei 'Degraded|Progressing|Missing|Invalid' broken-health-m13.txt
```

!!! example "Expected output"
    Health shows Degraded or Progressing; history lists at least two revisions.


#### Task 4 – Roll back and prove recovery

Roll back to the first (good) revision in history:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-argocd/module-13
argocd app history demo-api-prod | tee history-before-rollback-m13.txt
argocd app rollback demo-api-prod 0 | tee rollback-action-m13.txt
argocd app wait demo-api-prod --health --timeout 300 | tee rollback-wait-m13.txt
kubectl get application demo-api-prod -n argocd \
  -o jsonpath='Sync={.status.sync.status} Health={.status.health.status}{"\n"}' \
  | tee rollback-after-m13.txt
kubectl get pods -n rebash-argocd-m13 | tee pods-after-rollback-m13.txt
grep -q 'Healthy' rollback-after-m13.txt
```

!!! example "Expected output"
    After rollback, Application Health returns to Healthy and pods are Running.


### Validation steps

- [ ] AppProject sync window applied with `manualSync: true` on deny window
- [ ] Good Deployment syncs with probes and reaches Healthy
- [ ] Bad image tag degrades Application health
- [ ] `argocd app history` captures revision before rollback
- [ ] Rollback restores Synced and Healthy status

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Auto-sync blocked | Active deny window | Use manual sync if permitted: `argocd app sync demo-api-prod` |
| Stuck Progressing | CRD lacks health script | Add custom health lua or ignore status field |
| Rollback re-syncs bad commit | Git still on broken HEAD | Revert manifest in repo path, then sync |
| Rollout not progressing | Argo Rollouts not installed | Install Rollouts controller; Argo CD only syncs CR |
| file:// repo not found | Path not copied to /tmp | Run `cp -a ~/rebash-argocd/module-13 /tmp/rebash-argocd/` |

### Challenge exercise

Add an Argo Rollout manifest stub under `manifests/rollout-demo.yaml` (canary strategy with `nginxinc/nginx-unprivileged:1.27-alpine`) and note in a one-line comment that Argo CD syncs the CR while Rollouts owns traffic weights. Apply only if the Rollouts controller is installed in your cluster.

### Learning outcomes

- Applied sync windows with manual override on a live AppProject
- Synced a probe-backed Deployment and observed health transitions
- Broke health with an invalid image tag and captured sync history
- Rolled back with `argocd app rollback` and proved recovery

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
kubectl delete application demo-api-prod -n argocd --ignore-not-found
kubectl delete appproject platform-prod -n argocd --ignore-not-found
kubectl delete namespace rebash-argocd-m13 --ignore-not-found
argocd repo rm file:///tmp/rebash-argocd/module-13/manifests 2>/dev/null || true
rm -rf ~/rebash-argocd/module-13 /tmp/rebash-argocd/module-13
```

## Validation

- [ ] Sync window and rollback proven on a live kind cluster
- [ ] You can name two rollback strategies and trade-offs
- [ ] You understand Rollout CR sync vs traffic management split

## Code Walkthrough

1. **Sync windows** — cron schedule + timezone + duration; `manualSync: true` preserves break-glass path.
2. **Application history** — each sync records revision; rollback selects prior entry.
3. **Health** — built-in scripts; custom resources may need overrides in `argocd-cm`.
4. **Rollouts** — Git holds `Rollout` manifest; mesh/ingress weights change outside Argo CD sync loop.

## Security Considerations

- Restrict who may manual-sync during deny windows; audit overrides.
- Rollback without Git revert creates drift — document temporary ops and follow up with revert PR.
- Sync windows are not a substitute for approval policies — combine with PR reviews.
- Protect rollback permissions via Argo CD RBAC — not every developer should rollback prod.
- Validate timezone on sync windows — UTC vs local errors cause accidental blocks.

## Common Mistakes

!!! warning "Treating sync success as release success"
    Health Degraded or failed Rollout analysis still hurts users. Watch health and metrics, not only Synced.

!!! warning "Permanent deny windows without manual override"
    Blocks legitimate emergency fixes. Always allow audited manual sync.

!!! warning "Installing Rollouts without updating health checks"
    Application may show Healthy while canary is mid-flight if only Deployment existed before.

## Best Practices

- Prefer Git revert for durable rollback; use CLI rollback for speed then revert Git.
- Pair sync windows with notification triggers for blocked auto-sync events.
- Document change-freeze calendar in AppProject description.
- Use Rollouts analysis templates tied to Prometheus or Datadog metrics.
- Test rollback scripts quarterly in staging.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auto-sync skipped | Deny sync window active | Check AppProject `syncWindows` and timezone |
| Health Degraded | Failed probes or crash loop | `kubectl describe pod`; fix manifest in Git |
| Rollback button greyed | RBAC or no history | Check permissions; ensure prior sync recorded |
| Rollout paused forever | Analysis metric failing | Inspect Rollout status; fix metric query or abort |
| Window ignored | Wrong application selector | Match `applications` glob to Application name |

## Summary

**Progressive delivery with Argo CD** combines sync windows for timing, health for readiness, rollback for recovery, and optional **Argo Rollouts** for traffic-safe releases. Argo CD syncs desired manifests including Rollout CRs; Rollouts executes canary and blue-green logic after sync.

## Interview Questions

**1. What is an Argo CD sync window?**

??? success "Reveal answer"
    A scheduled allow or deny rule that controls whether automated sync may run for matching applications. Defined on AppProject or globally, with optional timezone, duration, and manual sync override during deny periods.

**2. What is the GitOps-preferred rollback approach?**

??? success "Reveal answer"
    Revert the breaking commit in Git (or pin `targetRevision` to a known-good tag) and let Argo CD sync forward. This keeps the repository as source of truth. CLI `app rollback` is faster but should be followed by a Git revert to avoid drift.

**3. How does Argo CD relate to Argo Rollouts?**

??? success "Reveal answer"
    Argo CD syncs Rollout manifests from Git like any other resource. Argo Rollouts controller manages canary/stable ReplicaSets, traffic weights, and analysis runs. CD answers “is Git applied?”; Rollouts answers “is the new version safely receiving traffic?”

**4. When is an Application Healthy vs Synced?**

??? success "Reveal answer"
    Synced means live cluster state matches Git. Healthy means aggregated resource health scripts report ready (e.g. Deployment has available replicas, probes pass). An app can be Synced but Degraded if pods crash.

**5. Why allow manualSync during a deny window?**

??? success "Reveal answer"
    Emergency fixes (security patch, outage) may need immediate deploy outside change freeze. Manual sync with RBAC audit preserves control while avoiding automatic merges during restricted hours.

## Related Tutorials

- [CI/CD Integration with Argo CD](ci-cd-integration-with-argo-cd.md)
- [Health checks and probes](../kubernetes/health-checks-probes-and-self-healing.md)

## References

- [Sync windows](https://argo-cd.readthedocs.io/en/stable/user-guide/sync_windows/)
- [Health assessment](https://argo-cd.readthedocs.io/en/stable/operator-manual/health/)
- [Argo Rollouts](https://argo-rollouts.readthedocs.io/)
