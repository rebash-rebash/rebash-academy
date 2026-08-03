---
title: "Labels, Selectors, and Namespaces"
description: "Organise Kubernetes objects with labels, selectors, annotations, ReplicaSets, and namespaces for multi-team DevOps clusters."
difficulty: intermediate
estimated_time: "35–50 min"
technology: kubernetes
category: kubernetes
module: "Module 3 · Kubernetes Objects"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
skills:
  - kubernetes
  - labels
  - namespaces
prerequisites:
  - kubernetes/pods-the-atomic-unit
next:
  - kubernetes/deployments-managing-replicated-pods
related:
  - kubernetes/namespaces-and-resource-management
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKAD
tags:
  - kubernetes
  - labels
  - namespaces
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---


# Labels, Selectors, and Namespaces

## Overview









Use labels/selectors to group objects, separate workloads with namespaces, and understand ReplicaSets as the replication layer under Deployments.

**Labels** are queryable key/value metadata. **Selectors** bind Services and controllers to Pods. **Namespaces** partition names and often tenancy. **Annotations** hold non-identifying metadata (tooling, checksums).

This is a core tutorial in **Module 3 · Kubernetes Objects** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites









- [Pods — The Atomic Unit](pods-the-atomic-unit.md)

## Learning Objectives









By the end of this tutorial, you will be able to:

- [ ] Apply and query labels  
- [ ] Explain selector matching  
- [ ] Create and use a namespace  
- [ ] Relate ReplicaSet to Deployment

## Architecture









This topic’s control points and relationships are shown below.

![Architecture](../assets/excalidraw/k8s-architecture.svg)

## Theory









### What it is

Kubernetes objects carry **metadata**. **Labels** are identifying key/value pairs you can query (`app=api`, `tier=frontend`). **Selectors** match those labels so Services and controllers know which Pods belong together. **Namespaces** partition names inside a cluster (soft multi-tenancy). **Annotations** hold non-identifying metadata for tools (checksums, build IDs). A **ReplicaSet** keeps a stable set of Pod replicas; Deployments own ReplicaSets for rolling updates.

### Why it matters

Without consistent labels, Services point at nothing, NetworkPolicies cannot target apps, and `kubectl get -l` is useless. Namespaces keep team A from colliding with team B on object names and are the usual boundary for quotas and RBAC. Understanding ReplicaSets explains why deleting a Pod under a Deployment does not permanently shrink the app.

### How it works (mental model)

- Controllers and Services declare `selector.matchLabels` (or set-based selectors).
- The API indexes Pods by labels; matching Pods become endpoints / managed replicas.
- Namespaces scope most namespaced resources; `default`, `kube-system`, and custom app namespaces are typical.
- Deployment creates a ReplicaSet with a pod template hash; scaling changes the ReplicaSet’s desired count; the ReplicaSet creates or deletes Pods.

Labels identify; annotations annotate. Do not put large config in labels — use ConfigMaps.

### Key concepts / comparisons

| Mechanism | Purpose |
|-----------|---------|
| Label | Queryable identity for grouping |
| Selector | Match labels (equality or set-based) |
| Annotation | Opaque metadata for tooling |
| Namespace | Name and policy boundary |
| ReplicaSet | Maintain N identical Pods |

| Equality selector | Set-based selector |
|-------------------|--------------------|
| `app=api` | `environment in (prod, staging)` |

### Common pitfalls

- Changing Deployment selector labels after creation — selectors are mostly immutable.
- Using spaces or upper-case inconsistently in label values; prefer simple DNS-safe keys.
- Putting secrets in annotations or labels — they are visible to many readers.
- Operating without `-n` and wondering why “nothing exists”.
- Treating namespaces as hard security isolation — you still need RBAC, NetworkPolicy, and quotas.

## Hands-on Lab

### Objective

Create a namespace and two Deployments with distinct label sets, then filter workloads with `kubectl get -l` selectors exactly as Services and controllers do.

### Prerequisites

- A working Kubernetes cluster (**kind**, **minikube**, or any lab cluster)
- **kubectl** with namespace-create rights
- Writable workspace at `~/rebash-k8s/module-03-labels`

### Lab environment

Workspace: `~/rebash-k8s/module-03-labels`

```bash title="Terminal"
mkdir -p ~/rebash-k8s/module-03-labels && cd ~/rebash-k8s/module-03-labels
```

### Real-world scenario

Two squads share a staging namespace: payments runs `api` tier Pods; storefront runs `web` tier Pods. You apply both Deployments with consistent labels and prove operators can list only one tier with label selectors— the same mechanism Services use for endpoints.

### Step-by-step tasks

#### Task 1 – Namespace and payments Deployment

Create `namespace.yaml`:

```yaml title="namespace.yaml"
apiVersion: v1
kind: Namespace
metadata:
  name: rebash-m03-labels
  labels:
    environment: lab
    lab: module-03-labels
```

Create `payments-deploy.yaml`:

```yaml title="payments-deploy.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payments-api
  namespace: rebash-m03-labels
  labels:
    app: payments-api
    team: payments
    tier: api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: payments-api
  template:
    metadata:
      labels:
        app: payments-api
        team: payments
        tier: api
    spec:
      containers:
        - name: nginx
          image: nginx:1.27-alpine
          ports:
            - containerPort: 80
```

Apply and wait:

```bash title="Terminal"
cd ~/rebash-k8s/module-03-labels
kubectl apply -f namespace.yaml
kubectl apply -f payments-deploy.yaml
kubectl rollout status deployment/payments-api -n rebash-m03-labels --timeout=120s
```

!!! example "Expected output"
    Deployment `payments-api` becomes Available.


#### Task 2 – Storefront Deployment with different labels

Create `storefront-deploy.yaml`:

```yaml title="storefront-deploy.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: storefront-web
  namespace: rebash-m03-labels
  labels:
    app: storefront-web
    team: storefront
    tier: web
spec:
  replicas: 1
  selector:
    matchLabels:
      app: storefront-web
  template:
    metadata:
      labels:
        app: storefront-web
        team: storefront
        tier: web
    spec:
      containers:
        - name: nginx
          image: nginx:1.27-alpine
          ports:
            - containerPort: 80
```

Apply and list all Pods:

```bash title="Terminal"
cd ~/rebash-k8s/module-03-labels
kubectl apply -f storefront-deploy.yaml
kubectl rollout status deployment/storefront-web -n rebash-m03-labels --timeout=120s
kubectl get pods -n rebash-m03-labels --show-labels | tee all-pods.txt
grep -c Running all-pods.txt | tee running-count.txt
test "$(cat running-count.txt)" -ge 2
```

!!! example "Expected output"
    At least two Running Pods with different `team` and `tier` labels.


#### Task 3 – Filter with label selectors

```bash title="Terminal"
cd ~/rebash-k8s/module-03-labels
kubectl get pods -n rebash-m03-labels -l team=payments | tee selector-payments.txt
kubectl get pods -n rebash-m03-labels -l tier=web | tee selector-web.txt
kubectl get deploy -n rebash-m03-labels -l 'team in (payments,storefront)' | tee selector-teams.txt
grep payments-api selector-payments.txt
grep storefront selector-web.txt
grep -E 'payments-api|storefront-web' selector-teams.txt
```

!!! example "Expected output"
    Each selector returns only matching workloads; `team=payments` lists payments Pods only.


### Validation steps

- [ ] Namespace `rebash-m03-labels` contains two Deployments
- [ ] Label selectors return distinct subsets
- [ ] Pod template labels match Deployment selectors
- [ ] Evidence files captured under the lab directory

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Selector returns nothing | Label typo or wrong namespace | `kubectl get pods --show-labels -n rebash-m03-labels` |
| Create fails on selector change | Deployment selector immutable | Delete Deployment and re-apply |
| Both teams in one result | Over-broad `-l` expression | Narrow to `team=payments` or `tier=web` |
| Forbidden | RBAC | Use lab cluster with create rights |

### Challenge exercise

Add `environment: lab` to both pod templates, then list every Pod with `-l 'environment=lab,team=payments'`. Create a third Deployment `canary-web` with `tier=web,track=canary` and list canaries with `-l track=canary`.

### Learning outcomes

- Applied consistent label taxonomies across Deployments
- Used equality and set-based selectors with kubectl
- Connected label selectors to how Services choose endpoints

### Cleanup

```bash title="Terminal"
kubectl delete namespace rebash-m03-labels --ignore-not-found --wait=true
```

## Validation









- [ ] Lab commands run under `~/rebash-k8s/module-03-labels/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough









Production practice for **Labels, Selectors, and Namespaces** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations









- Treat credentials and tokens for kubernetes as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes









!!! warning "Changing Deployment selector labels after creation — selectors are mostly immutable."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Using spaces or upper-case inconsistently in label values; prefer simple DNS-safe keys."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices









- Encode Labels, Selectors, and Namespaces changes as code and review them in pull requests
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









**Labels, Selectors, and Namespaces** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions








1. What is a Kubernetes namespace used for?
2. How do labels differ from annotations?
3. How do selectors use labels to group Pods for Services and Deployments?
4. What security benefit do namespaces provide, and what do they not isolate by themselves?
5. Give an example of a useful label taxonomy for multi-team clusters.

!!! tip "Sample answer — question 2"
    Labels are identifying metadata for selection; annotations hold non-identifying tool or descriptive data. Controllers and Services select on labels, not annotations.

!!! tip "Sample answer — question 4"
    Namespaces scope names and RBAC subjects, but they do not provide network or node isolation alone. Combine with NetworkPolicy, quotas, and Pod security controls for stronger tenancy.

## Related Tutorials









- [Course overview](index.md)
- [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md)

## References









- [Labels and selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) · [Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
