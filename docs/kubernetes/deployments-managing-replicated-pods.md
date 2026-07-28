---
title: Deployments — Managing Replicated Pods
description: Use Deployments and ReplicaSets to scale stateless workloads, perform rolling updates, roll back failed releases, and manage Pod lifecycle in production.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
category: kubernetes
tags:
  - kubernetes
  - deployments
  - replicasets
  - rollouts
  - scaling
  - workloads
prerequisites:
  - Pods — The Atomic Unit
  - kubectl Essentials and Workflows
  - Installing Kubernetes and kubectl
comments: false
---

# Deployments — Managing Replicated Pods

## Overview

A single Pod is ephemeral — delete it and it is gone. Production workloads need **replicated**, **self-healing**, and **updatable** application tiers. **Deployments** are the standard Kubernetes controller for stateless applications. They declare how many Pod replicas you want, continuously reconcile actual state to desired state, and orchestrate **rolling updates** and **rollbacks** without downtime.

When an SRE scales an API from 3 to 30 replicas during a traffic spike, or a DevOps engineer ships version `2.1.0` with a controlled rollout, they use Deployments. When a bad image tag takes down every replica, `kubectl rollout undo` restores the previous ReplicaSet in seconds.

This is **Tutorial 6** in **Module 2: Workloads** of the REBASH Academy Kubernetes series. Complete [Pods — The Atomic Unit](pods-the-atomic-unit.md) and [kubectl Essentials and Workflows](kubectl-essentials-and-workflows.md) first.

## Prerequisites

- Completed [Installing Kubernetes and kubectl](installing-kubernetes-and-kubectl.md) — a working cluster (minikube, kind, k3s, or cloud)
- Completed [kubectl Essentials and Workflows](kubectl-essentials-and-workflows.md) — apply, get, describe, logs, exec
- Completed [Pods — The Atomic Unit](pods-the-atomic-unit.md) — Pod spec fields, labels, selectors, restart policies
- Familiarity with [From Docker to Kubernetes](../docker/from-docker-to-kubernetes.md) — Docker Compose services map to Deployments
- Optional: [Linux Foundations](../linux/index.md) for reading YAML and shell scripting

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the relationship between Deployments, ReplicaSets, and Pods
- [ ] Create and scale Deployments declaratively with YAML and imperatively with kubectl
- [ ] Perform rolling updates and understand `maxSurge` and `maxUnavailable`
- [ ] Roll back a failed deployment to a previous revision
- [ ] Inspect rollout history and diagnose stuck rollouts
- [ ] Apply production patterns: resource requests/limits, probes, and label selectors
- [ ] Know when to use Deployments vs StatefulSets, DaemonSets, or bare Pods

## Architecture Diagram

Deployments own ReplicaSets; ReplicaSets own Pods. Each rollout creates a new ReplicaSet while phasing out the old one.

```d2
direction: down

Control: "Control Plane" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        DEP: "Deployment\nreplicas: 3"
        RS1: "ReplicaSet v1\ndesired: 0"
        RS2: "ReplicaSet v2\ndesired: 3"
    }
    Data: "Worker Nodes" {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        P1: "Pod v2"
        P2: "Pod v2"
        P3: "Pod v2"
    }
    Control.DEP -> Control.RS1
    Control.DEP -> Control.RS2
    Control.RS2 -> Data.P1
    Control.RS2 -> Data.P2
    Control.RS2 -> Data.P3
    Control.RS1 -> Control.DEP: "scaled to 0\nafter rollout" {
      style.stroke-dash: 3
    }
```

## Theory

### Why Deployments Exist

Bare Pods have no built-in replication or update strategy. If a node fails, Kubernetes does not recreate a standalone Pod unless a controller manages it. **ReplicaSets** ensure a specified number of Pod replicas exist and match label selectors. **Deployments** wrap ReplicaSets with declarative updates, revision history, and rollback.

| Object | Responsibility |
|--------|----------------|
| **Pod** | Run one or more containers; smallest schedulable unit |
| **ReplicaSet** | Maintain N identical Pods via label selector |
| **Deployment** | Manage ReplicaSets; rolling updates, rollbacks, scaling |

### Deployment Spec Essentials

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  labels:
    app: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: nginx
          image: nginx:1.25-alpine
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: "100m"
              memory: "64Mi"
            limits:
              cpu: "250m"
              memory: "128Mi"
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 3
            periodSeconds: 5
```

| Field | Purpose |
|-------|---------|
| `replicas` | Desired Pod count |
| `selector.matchLabels` | Must match Pod template labels — immutable after creation |
| `strategy.type` | `RollingUpdate` (default) or `Recreate` |
| `maxSurge` | Extra Pods above desired count during rollout |
| `maxUnavailable` | Pods that can be unavailable during rollout |
| `template` | Pod spec for every replica |

!!! note "Selector immutability"
    You cannot change a Deployment's `selector` after creation. Plan labels (`app`, `version`, `tier`) before the first apply.

### Rolling Update Mechanics

When you change the Pod template (typically the container image), the Deployment:

1. Creates a **new ReplicaSet** with the updated template
2. Scales up the new ReplicaSet according to `maxSurge`
3. Scales down the old ReplicaSet according to `maxUnavailable`
4. Repeats until all Pods run the new version

With `replicas: 3`, `maxSurge: 1`, and `maxUnavailable: 0`, Kubernetes never drops below 3 ready Pods during the rollout — ideal for production.

**Recreate** strategy kills all old Pods before starting new ones. Use only when the app cannot run two versions simultaneously (rare for stateless services).

### Rollback and Revision History

Each template change creates a new ReplicaSet. Old ReplicaSets are retained (scaled to zero) for rollback:

```bash
kubectl rollout history deployment/web
kubectl rollout undo deployment/web
kubectl rollout undo deployment/web --to-revision=2
```

By default, Kubernetes keeps 10 old ReplicaSets. Tune with `revisionHistoryLimit`.

### Scaling

Horizontal scaling changes `replicas`:

```bash
kubectl scale deployment/web --replicas=5
kubectl autoscale deployment web --cpu-percent=70 --min=2 --max=10  # requires metrics-server
```

For production autoscaling, use a **HorizontalPodAutoscaler (HPA)** — covered in [Production Patterns](production-patterns-hpa-pdb-and-affinity.md).

### Deployment vs Other Controllers

| Controller | Use case |
|------------|----------|
| **Deployment** | Stateless apps, web APIs, workers |
| **StatefulSet** | Stable network identity, ordered rollout, persistent storage per Pod |
| **DaemonSet** | One Pod per node — log agents, CNI plugins |
| **Job / CronJob** | Run-to-completion batch work |

### Labels and Selectors

Services, NetworkPolicies, and HPAs route traffic or apply rules using **labels**. Standard pattern:

```yaml
labels:
  app: web
  version: "1.2.0"
  tier: frontend
```

The Deployment `selector` must be a subset of template labels. Avoid putting unique values (like Pod name) in the selector.

## Hands-on Lab

These labs use a local cluster. Adjust namespace flags if your environment differs.

### Step 1 – Create a Deployment

**Command:**

```bash
kubectl create namespace lab-deployments
kubectl create deployment web \
  --image=nginx:1.25-alpine \
  --replicas=3 \
  -n lab-deployments
kubectl get deployment,rs,pods -n lab-deployments -o wide
```

**Explanation:** `kubectl create deployment` generates a Deployment with default rolling update strategy. Observe one ReplicaSet and three Pods.

**Expected output:**

```text
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
web    3/3     3            3           30s

NAME             DESIRED   CURRENT   READY   AGE
web-7d4b8c9f6d    3         3         3       30s

NAME                    READY   STATUS    RESTARTS   AGE
web-7d4b8c9f6d-xxxxx    1/1     Running   0          25s
...
```

### Step 2 – Apply a declarative manifest

**Command:**

Save as `web-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: lab-deployments
  labels:
    app: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: nginx
          image: nginx:1.25-alpine
          ports:
            - containerPort: 80
          readinessProbe:
            httpGet:
              path: /
              port: 80
            periodSeconds: 5
```

```bash
kubectl apply -f web-deployment.yaml
kubectl describe deployment web -n lab-deployments | tail -20
```

**Explanation:** Declarative manifests are the production standard — version-controlled, reviewable, and GitOps-ready.

### Step 3 – Perform a rolling update

**Command:**

```bash
kubectl set image deployment/web nginx=nginx:1.26-alpine -n lab-deployments
kubectl rollout status deployment/web -n lab-deployments
kubectl get rs -n lab-deployments
```

**Explanation:** Image changes trigger a rolling update. Two ReplicaSets appear briefly — old scaling down, new scaling up.

**Expected output:**

```text
deployment "web" successfully rolled out

NAME             DESIRED   CURRENT   READY   AGE
web-7d4b8c9f6d    0         0         0       5m
web-9a2f1e8b7c    3         3         3       1m
```

### Step 4 – Roll back a bad release

**Command:**

```bash
# Simulate a bad image
kubectl set image deployment/web nginx=nginx:does-not-exist -n lab-deployments
kubectl rollout status deployment/web -n lab-deployments --timeout=60s || true
kubectl get pods -n lab-deployments

kubectl rollout undo deployment/web -n lab-deployments
kubectl rollout status deployment/web -n lab-deployments
```

**Explanation:** Failed rollouts leave Pods in `ImagePullBackOff` or `CrashLoopBackOff`. `rollout undo` reverts to the previous ReplicaSet.

### Step 5 – Scale and inspect history

**Command:**

```bash
kubectl scale deployment/web --replicas=5 -n lab-deployments
kubectl rollout history deployment/web -n lab-deployments
kubectl rollout history deployment/web -n lab-deployments --revision=2
```

**Explanation:** History records each template change. Use `--revision` to inspect the manifest diff before undoing to a specific version.

### Step 6 – Pause and resume rollouts

**Command:**

```bash
kubectl rollout pause deployment/web -n lab-deployments
kubectl set image deployment/web nginx=nginx:1.27-alpine -n lab-deployments
kubectl get rs -n lab-deployments
kubectl rollout resume deployment/web -n lab-deployments
kubectl rollout status deployment/web -n lab-deployments
```

**Explanation:** Pausing lets you apply multiple template changes before a single coordinated rollout — useful for complex updates.

### Step 7 – Clean up

**Command:**

```bash
kubectl delete namespace lab-deployments
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `kubectl create deployment` | Imperative Deployment creation | `kubectl create deployment web --image=nginx --replicas=3` |
| `kubectl scale` | Change replica count | `kubectl scale deployment/web --replicas=5` |
| `kubectl set image` | Update container image | `kubectl set image deployment/web nginx=nginx:1.26` |
| `kubectl rollout status` | Watch rollout progress | `kubectl rollout status deployment/web` |
| `kubectl rollout history` | List revision history | `kubectl rollout history deployment/web` |
| `kubectl rollout undo` | Roll back to previous revision | `kubectl rollout undo deployment/web --to-revision=2` |
| `kubectl rollout pause/resume` | Control rollout timing | `kubectl rollout pause deployment/web` |

### Production-ready Deployment template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  labels:
    app: api
spec:
  replicas: 3
  revisionHistoryLimit: 5
  selector:
    matchLabels:
      app: api
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: registry.example.com/api:1.4.2
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "200m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
```

## Common Mistakes

!!! warning "Deploying bare Pods in production"
    Standalone Pods are not rescheduled with the same name, have no replication, and no rollout strategy. Always use a Deployment (or appropriate controller) for long-running stateless apps.

!!! warning "Changing selector labels after creation"
    Deployment selectors are immutable. Changing `matchLabels` requires deleting and recreating the Deployment — causing downtime. Plan label keys before first deploy.

!!! warning "Setting maxUnavailable too high on small replica counts"
    With `replicas: 2` and `maxUnavailable: 50%`, one Pod can be down during rollout — cutting capacity in half. For low replica counts, set `maxUnavailable: 0` and `maxSurge: 1`.

!!! warning "Skipping readiness probes during rollouts"
    Without readiness probes, Kubernetes marks Pods ready as soon as the container starts — sending traffic before the app accepts connections. Always define readiness for services fronting Deployments.

## Best Practices

!!! tip "Use declarative YAML in Git"
    Store Deployment manifests in version control. Pair with CI/CD or GitOps (Argo CD, Flux) so every production change is auditable.

!!! tip "Pin image tags, not :latest"
    Use semantic version tags or digest pins (`image@sha256:...`). `:latest` makes rollbacks and debugging unpredictable.

!!! tip "Set resource requests and limits"
    Unbounded Pods starve neighbors and get OOMKilled unpredictably. Requests drive scheduling; limits cap burst usage.

!!! tip "Keep revisionHistoryLimit intentional"
    Retain enough revisions for rollback (5–10) without cluttering etcd with stale ReplicaSets.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Rollout stuck | Image pull failure, crash loop, failed probe | `kubectl describe rs`, `kubectl logs`; fix image or probes |
| `ImagePullBackOff` | Wrong tag, missing registry credentials | Verify image name; add `imagePullSecrets` |
| Old ReplicaSets accumulate | Normal behavior | Old RS scale to 0; tune `revisionHistoryLimit` |
| Selector mismatch error | Template labels don't match selector | Align `spec.selector.matchLabels` with template metadata labels |
| Rollout undo fails | Revision pruned | Check `rollout history`; redeploy known-good manifest from Git |
| Pods pending after scale-up | Insufficient cluster resources | `kubectl describe pod`; add nodes or reduce requests |

## Summary

- **Deployments** manage stateless, replicated applications through **ReplicaSets** and **Pods**
- **Rolling updates** replace Pods incrementally using `maxSurge` and `maxUnavailable`
- **Rollout history** enables fast rollback when a release fails
- **Labels and selectors** connect Deployments to Services, HPAs, and NetworkPolicies
- Production Deployments need **pinned images**, **resource limits**, and **readiness/liveness probes**
- Next: expose Deployments with stable networking in [Services and Cluster Networking](services-and-cluster-networking.md)

## Interview Questions

1. What is the relationship between a Deployment, ReplicaSet, and Pod?
2. Explain rolling update strategy and the purpose of `maxSurge` and `maxUnavailable`.
3. How do you roll back a Deployment to a previous version?
4. Why are Deployment selectors immutable?
5. When would you choose `Recreate` over `RollingUpdate`?
6. What happens to old ReplicaSets after a successful rollout?
7. How does `kubectl scale` differ from a HorizontalPodAutoscaler?
8. Why should you avoid deploying bare Pods in production?
9. What is the purpose of `revisionHistoryLimit`?
10. How do readiness probes affect rolling updates?

??? tip "Sample Answers (Questions 1, 2, and 3)"

    **Q1 — Relationship:** A Deployment declares desired state (replica count, Pod template, update strategy). It creates and manages ReplicaSets. Each ReplicaSet ensures a specified number of Pods matching its label selector are running. Pods are the actual workload instances running containers.

    **Q2 — Rolling update:** RollingUpdate replaces Pods incrementally rather than all at once. `maxSurge` allows extra Pods above the desired count during the rollout (e.g., 4 Pods when desired is 3). `maxUnavailable` allows Pods to be temporarily unavailable (e.g., 2 ready when desired is 3). Together they control rollout speed and availability.

    **Q3 — Rollback:** Run `kubectl rollout undo deployment/<name>` to revert to the previous ReplicaSet. Use `kubectl rollout history` to list revisions and `--to-revision=N` to target a specific version. Kubernetes scales up the old ReplicaSet and scales down the failed one.

## Related Tutorials

- [Kubernetes – Category Overview](index.md)
- [Pods — The Atomic Unit](pods-the-atomic-unit.md) *(previous in Module 2)*
- [kubectl Essentials and Workflows](kubectl-essentials-and-workflows.md)
- [Services and Cluster Networking](services-and-cluster-networking.md) *(next in series)*
- [From Docker to Kubernetes](../docker/from-docker-to-kubernetes.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [Kubernetes Deployments documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Performing a Rolling Update](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)
- [kubectl rollout reference](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/)
- [REBASH Academy – Docker Overview](../docker/index.md)
