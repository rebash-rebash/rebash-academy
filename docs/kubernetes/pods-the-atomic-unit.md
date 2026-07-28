---
title: Pods — The Atomic Unit
description: Understand Pod anatomy, multi-container patterns, lifecycle phases, restart policies, resource fields, and hands-on Pod manifest authoring in Kubernetes.
difficulty: beginner
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: kubernetes
tags:
  - kubernetes
  - pods
  - workloads
  - containers
  - sidecar
prerequisites:
  - kubectl Essentials and Workflows
  - Installing Kubernetes and kubectl
  - From Docker to Kubernetes
comments: false
---

# Pods — The Atomic Unit

## Overview

A **Pod** is the smallest deployable unit in Kubernetes — not a container, but a wrapper around one or more containers that share network and storage. Every Deployment, StatefulSet, Job, and DaemonSet ultimately creates Pods. Understanding Pod anatomy, lifecycle, and multi-container patterns is essential before managing replicas, Services, or storage.

This tutorial explains what Pods are, how they differ from Docker containers, when to use multi-container Pods, and how to author Pod manifests for labs — while emphasizing that **Deployments** manage Pods in production.

This is **Tutorial 5** in **Module 2: Workloads** of the REBASH Academy Kubernetes series. Complete [kubectl Essentials and Workflows](kubectl-essentials-and-workflows.md) and have a running cluster from [Installing Kubernetes and kubectl](installing-kubernetes-and-kubectl.md). Review [From Docker to Kubernetes](../docker/from-docker-to-kubernetes.md) for the Docker-to-Pod mapping.

## Prerequisites

- [kubectl Essentials and Workflows](kubectl-essentials-and-workflows.md)
- [Installing Kubernetes and kubectl](installing-kubernetes-and-kubectl.md)
- [From Docker to Kubernetes](../docker/from-docker-to-kubernetes.md)
- [Running Your First Container](../docker/running-your-first-container.md) — container basics
- Running local cluster (minikube or kind) with kubectl configured

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain what a Pod is and why Kubernetes wraps containers in Pods
- [ ] Author a Pod manifest with containers, ports, env vars, and resource requests
- [ ] Describe Pod lifecycle phases and container restart policies
- [ ] Implement sidecar and init container patterns at a basic level
- [ ] Debug Pod failures using kubectl describe, logs, and events
- [ ] Articulate why bare Pods are for labs — Deployments for production
- [ ] Map Docker run flags to Pod spec fields

## Architecture

A Pod creates a shared execution environment: one IP address, one set of network namespaces, optional shared volumes.

```d2
direction: down

POD: "Pod — shared context" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        NET: "Network namespace\nIP: 10.244.1.15"
        VOL: "Shared volumes\nemptyDir / config"
        MAIN: "Primary container" {
          style: {
            fill: "#dcfce7"
            stroke: "#16a34a"
          }
            APP: "app :8080"
        }
        SIDE: "Sidecar container" {
          style: {
            fill: "#ffedd5"
            stroke: "#ea580c"
          }
            LOG: log-shipper
        }
        INIT: "Init containers\nrun sequentially first" {
          style: {
            fill: "#f3e8ff"
            stroke: "#9333ea"
          }
            INITC: fetch-config
        }
    }
    NODE: "Worker Node\nkubelet + containerd"
    SVC: "Service selector\napp=web"
    POD: POD
    NODE -> POD
    POD.INIT.INITC -> POD.MAIN.APP
    POD.MAIN.APP -> POD.VOL
    POD.SIDE.LOG -> POD.VOL
    SVC -> POD.NET
```

## Theory

### What Is a Pod?

A **Pod** is a group of one or more containers with:

- **Shared network namespace** — one Pod IP; containers communicate via `localhost`
- **Shared storage volumes** — mount the same files (logs, config, sockets)
- **Co-scheduled placement** — always on the same node

The Pod is ephemeral. When it dies, it is replaced with a **new Pod** (new UID, often new IP). Stable identity requires higher-level controllers (Deployment, StatefulSet).

### Pod vs Docker Container

| Aspect | Docker container | Kubernetes Pod |
|--------|------------------|----------------|
| **Unit of scheduling** | Single container | Pod (1+ containers) |
| **Networking** | Bridge network, published ports | Pod IP via CNI; Service for stable access |
| **Lifecycle manager** | dockerd restart policy | kubelet + controller (Deployment) |
| **Naming** | Container name | Pod name; containers have `name` field |
| **Multi-container** | `docker run` + `--network container:` hack | Native sidecar pattern |

Docker equivalent from [From Docker to Kubernetes](../docker/from-docker-to-kubernetes.md):

```bash
docker run -d --name api -e DB_HOST=db -p 3000:3000 myapi:1.2.0
```

Maps to a Pod spec with `containers`, `env`, and `ports` — but without `-p` on the Pod; use a Service for exposure.

### Pod Manifest Structure

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: my-app
spec:
  containers:
    - name: app
      image: myapp:1.0.0
      ports:
        - containerPort: 8080
      env:
        - name: LOG_LEVEL
          value: info
      resources:
        requests:
          memory: "64Mi"
          cpu: "100m"
        limits:
          memory: "128Mi"
          cpu: "200m"
  restartPolicy: Always
```

| Field | Purpose |
|-------|---------|
| `metadata.labels` | Service selectors, monitoring, affinity |
| `spec.containers[].image` | OCI image — same as Docker |
| `spec.containers[].ports.containerPort` | Documentation + probe target; does not publish externally |
| `spec.restartPolicy` | `Always`, `OnFailure`, `Never` |
| `spec.nodeName` | Bypass scheduler (rare; debugging only) |
| `spec.serviceAccountName` | Identity for API access (RBAC module later) |

### Pod Lifecycle Phases

| Phase | Meaning |
|-------|---------|
| **Pending** | Accepted but not running — scheduling, image pull |
| **Running** | At least one container started |
| **Succeeded** | All containers terminated successfully (Jobs) |
| **Failed** | At least one container failed; none running |
| **Unknown** | Node communication lost |

Container states: **Waiting** (reason: `ContainerCreating`, `ImagePullBackOff`), **Running**, **Terminated**.

```d2
direction: right

PEND: Pending
    RUN: Running
    SUCC: Succeeded
    FAIL: Failed
    PEND -> RUN
    RUN -> SUCC
    RUN -> FAIL
    PEND -> FAIL
```

### Restart Policies

| Policy | Behaviour | Typical use |
|--------|----------|-------------|
| **Always** | Restart on any exit | Long-running apps (default for Deployments) |
| **OnFailure** | Restart only on non-zero exit | Batch, init-heavy Pods |
| **Never** | No restart | One-shot debug Pods |

Bare Pod with `restartPolicy: Always` restarts on the **same node** — but if the node fails, the Pod is gone unless a Deployment recreates it.

### Multi-Container Patterns

#### Sidecar

Helper container alongside main app — log shipping, proxy, config sync:

```yaml
containers:
  - name: app
    image: myapp:1.0
    volumeMounts:
      - name: logs
        mountPath: /var/log/app
  - name: log-shipper
    image: fluent/fluent-bit:2.2
    volumeMounts:
      - name: logs
        mountPath: /var/log/app
volumes:
  - name: logs
    emptyDir: {}
```

Both containers share `emptyDir` volume at `/var/log/app`.

#### Init Containers

Run **sequentially** before app containers start — wait for dependencies, download assets, migrate DB schema:

```yaml
initContainers:
  - name: wait-for-db
    image: busybox:1.36
    command: ['sh', '-c', 'until nc -z db 5432; do sleep 2; done']
containers:
  - name: app
    image: myapp:1.0
```

Init failure blocks Pod startup — kubelet retries per restart policy.

### Resource Requests and Limits

| Field | Effect |
|-------|------|
| **requests** | Scheduler uses for placement; guaranteed minimum |
| **limits** | cgroup cap — OOM kill if memory exceeded; CPU throttled |

Without requests, scheduler may overcommit nodes — worse than missing Docker `--memory` limits (see [From Docker to Kubernetes](../docker/from-docker-to-kubernetes.md)).

CPU units: `100m` = 0.1 core. Memory: `128Mi`, `1Gi`.

### Why Not Bare Pods in Production?

| Bare Pod issue | Deployment solution |
|----------------|---------------------|
| Deleted Pod never returns | ReplicaSet maintains replica count |
| No rolling updates | Deployment strategy manages rollouts |
| No revision history | `rollout history` / undo |
| Manual scaling | `kubectl scale deployment` |

Use bare Pods for **learning**, **one-off debug**, and **Job** patterns — not for stateless web apps.

### Pod Networking Recap

- Each Pod gets a cluster-routable IP from the CNI plugin
- Containers in Pod share IP — bind to different ports on `localhost`
- Other Pods reach this Pod via Service ClusterIP or direct Pod IP (discouraged)
- `hostNetwork: true` uses node network — rare, security-sensitive

## Hands-on Lab

### Step 1 – Create a single-container Pod

**Command:**

```bash
mkdir -p ~/k8s-lab/module2/pods
cat <<'EOF' > ~/k8s-lab/module2/pods/nginx-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
    tier: frontend
spec:
  containers:
    - name: nginx
      image: nginx:1.27-alpine
      ports:
        - containerPort: 80
      resources:
        requests:
          memory: "32Mi"
          cpu: "50m"
        limits:
          memory: "64Mi"
          cpu: "100m"
  restartPolicy: Never
EOF
kubectl apply -f ~/k8s-lab/module2/pods/nginx-pod.yaml
kubectl get pod nginx-pod -w
# Ctrl+C when Running
```

**Explanation:** `restartPolicy: Never` suits lab Pods you manage manually. Observe phase transition Pending → Running.

**Expected output:**

```text
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   1/1     Running   0          15s
```

### Step 2 – Inspect Pod details and IP

**Command:**

```bash
kubectl describe pod nginx-pod
kubectl get pod nginx-pod -o jsonpath='{.status.podIP}{"\n"}{.status.phase}{"\n"}'
kubectl exec nginx-pod -- curl -s -o /dev/null -w "%{http_code}\n" http://localhost:80
```

**Explanation:** Pod IP is reachable from other Pods in the cluster. localhost works inside the container because it shares the Pod network namespace.

**Expected output:**

```text
10.244.x.x
Running
200
```

### Step 3 – Environment variables and commands

**Command:**

```bash
cat <<'EOF' > ~/k8s-lab/module2/pods/env-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-demo
spec:
  containers:
    - name: shell
      image: busybox:1.36
      command: ["sh", "-c", "echo HOST=$HOST VERSION=$VERSION && sleep 3600"]
      env:
        - name: HOST
          value: rebash-lab
        - name: VERSION
          value: "1.0"
  restartPolicy: Never
EOF
kubectl apply -f ~/k8s-lab/module2/pods/env-pod.yaml
kubectl logs env-demo
```

**Explanation:** Maps Docker `-e` flags to `env` list. `command` overrides image entrypoint — same as Docker `CMD`.

**Expected output:**

```text
HOST=rebash-lab VERSION=1.0
```

### Step 4 – Init container pattern

**Command:**

```bash
cat <<'EOF' > ~/k8s-lab/module2/pods/init-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: init-demo
spec:
  initContainers:
    - name: init-myservice
      image: busybox:1.36
      command: ['sh', '-c', 'echo prepared > /work/data.txt']
      volumeMounts:
        - name: workdir
          mountPath: /work
  containers:
    - name: app
      image: busybox:1.36
      command: ['sh', '-c', 'cat /work/data.txt && sleep 3600']
      volumeMounts:
        - name: workdir
          mountPath: /work
  volumes:
    - name: workdir
      emptyDir: {}
  restartPolicy: Never
EOF
kubectl apply -f ~/k8s-lab/module2/pods/init-pod.yaml
kubectl get pod init-demo -w
kubectl logs init-demo
```

**Explanation:** Init container writes to shared `emptyDir`; main container reads it. Init runs to completion before app starts.

**Expected output:**

```text
prepared
```

### Step 5 – Sidecar pattern (shared volume)

**Command:**

```bash
cat <<'EOF' > ~/k8s-lab/module2/pods/sidecar-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: sidecar-demo
spec:
  containers:
    - name: writer
      image: busybox:1.36
      command: ['sh', '-c', 'while true; do date >> /var/log/app.log; sleep 5; done']
      volumeMounts:
        - name: logs
          mountPath: /var/log
    - name: reader
      image: busybox:1.36
      command: ['sh', '-c', 'tail -f /var/log/app.log']
      volumeMounts:
        - name: logs
          mountPath: /var/log
  volumes:
    - name: logs
      emptyDir: {}
  restartPolicy: Never
EOF
kubectl apply -f ~/k8s-lab/module2/pods/sidecar-pod.yaml
sleep 8
kubectl logs sidecar-demo -c reader --tail=3
```

**Explanation:** Classic sidecar: writer appends logs; reader tails the same file via shared volume — mimics log shipping without a separate daemonset.

**Expected output:**

```text
Tue Jul 28 ... UTC 2026
Tue Jul 28 ... UTC 2026
```

### Step 6 – Simulate failure and observe restart policy

**Command:**

```bash
cat <<'EOF' > ~/k8s-lab/module2/pods/crash-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: crash-demo
spec:
  containers:
    - name: flaky
      image: busybox:1.36
      command: ['sh', '-c', 'echo starting; exit 1']
  restartPolicy: OnFailure
EOF
kubectl apply -f ~/k8s-lab/module2/pods/crash-pod.yaml
sleep 5
kubectl get pod crash-demo
kubectl describe pod crash-demo | grep -A6 "Containers:" | head -10
```

**Explanation:** Container exits with code 1; `OnFailure` triggers kubelet restart. Compare with `restartPolicy: Never` where Pod stays Failed.

**Expected output:**

```text
NAME         READY   STATUS   RESTARTS      AGE
crash-demo   0/1     Error    3 (30s ago)   45s
```

### Step 7 – Clean up lab Pods

**Command:**

```bash
kubectl delete -f ~/k8s-lab/module2/pods/ --ignore-not-found
kubectl get pods
```

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
| `kubectl apply -f pod.yaml` | Create/update Pod | `kubectl apply -f nginx-pod.yaml` |
| `kubectl get pod -o yaml` | Export live Pod spec | `kubectl get pod NAME -o yaml` |
| `kubectl describe pod` | Events, conditions, container state | `kubectl describe pod NAME` |
| `kubectl logs -c` | Logs from specific container | `kubectl logs POD -c sidecar` |
| `kubectl exec -c` | Exec into specific container | `kubectl exec POD -c app -- sh` |
| `kubectl delete pod` | Remove Pod | `kubectl delete pod NAME` |
| `kubectl explain pod.spec` | Field documentation | `kubectl explain pod.spec.initContainers` |
| `kubectl get pod -w` | Watch status changes | `kubectl get pods -w` |

### Pod quick-debug alias

```bash
# Usage: kdebug my-pod
kdebug() {
  kubectl describe pod "$1"
  echo "--- logs ---"
  kubectl logs "$1" --all-containers=true --tail=30
}
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Deploying bare Pods for production web apps"
    A deleted Pod is not recreated. Always use Deployments for stateless apps — covered in the next tutorial in this module.

!!! warning "Expecting containerPort to publish externally"
    `containerPort` documents the port; it does not bind host ports. Use Services or Ingress for access — unlike `docker run -p`.

!!! warning "Putting unrelated services in one Pod"
    Pods scale as a unit. Do not co-locate unrelated apps — you cannot scale them independently.

!!! warning "Omitting resource requests"
    Pods without requests may schedule on overloaded nodes and get OOMKilled. Always set requests; set limits for production.

!!! warning "Using latest image tag"
    Same anti-pattern as Docker — pin semver or digest; unexpected pulls break reproducibility.

## Best Practices

!!! tip "Use labels on every Pod template"
    `app`, `version`, and `component` labels enable Service selectors and observability queries.

!!! tip "Prefer Deployments over bare Pods"
    Even in dev, practice `Deployment → Pod` workflow to build production habits early.

!!! tip "Use init containers for startup ordering"
    Replace brittle `sleep 30` entrypoints with init containers that probe dependencies.

!!! tip "Keep sidecars lightweight"
    Sidecars consume Pod resource quotas — account for their CPU/memory in requests and limits.

!!! tip "Debug with describe first"
    Pod **Events** reveal ImagePullBackOff, failed mounts, and probe failures faster than guessing from STATUS column alone.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Pending | No schedulable node, resources, taints | `kubectl describe pod`; check node capacity |
| ImagePullBackOff | Wrong tag, private registry | Verify image name; add imagePullSecrets |
| CrashLoopBackOff | App exits on start | `kubectl logs --previous`; fix command/config |
| Init:Error | Init container failed | `kubectl logs POD -c INIT_NAME` |
| OOMKilled | Memory limit exceeded | Increase limit or fix memory leak |
| Invalid manifest | YAML indentation, wrong apiVersion | `kubectl apply --dry-run=server -f` |
| Pod Running but no response | App listens wrong port | Check `containerPort` vs app bind address |
| Two containers port conflict | Same port in shared network | Bind different ports on localhost |

## Summary

- A **Pod** wraps one or more containers sharing network and volumes — the **atomic unit** of scheduling in Kubernetes
- **Pod lifecycle** phases: Pending → Running → Succeeded/Failed; container states include Waiting, Running, Terminated
- **Init containers** run sequentially before app containers; **sidecars** run alongside the main container sharing volumes
- **restartPolicy** controls kubelet restarts; **Deployments** provide replica management and self-healing across node failures
- **resource requests/limits** affect scheduling and cgroup enforcement — always set requests in production
- Bare Pods are for learning and Jobs; next in the track: Deployments for replicated workloads
- Continue to **Deployments — Managing Replicated Pods** when published in this module

## Interview Questions

1. What is a Pod, and why does Kubernetes use Pods instead of scheduling containers directly?
2. How do containers within a Pod communicate with each other?
3. Explain the difference between init containers and sidecar containers.
4. What are Pod phases, and what does Pending indicate?
5. Compare restartPolicy values: Always, OnFailure, Never.
6. What is the purpose of resource requests vs limits?
7. Why should production apps avoid bare Pods?
8. How does a Pod get its IP address?
9. Map Docker `-e`, `-p`, and `--restart` to Pod spec fields.
10. What happens to Pod data when a Pod is deleted?

??? tip "Sample Answers (Questions 1, 3, and 7)"

    **Q1 — Pod definition:** A Pod is the smallest deployable unit in Kubernetes — a group of one or more containers that share a network namespace (one IP), IPC, and optional volumes. Kubernetes schedules Pods, not individual containers, to enable co-located helper patterns (sidecars, init) and simplify networking. Containers in a Pod always run on the same node.

    **Q3 — Init vs sidecar:** **Init containers** run to completion in sequence before any app container starts — ideal for setup tasks like waiting for a database or downloading config. **Sidecar containers** run concurrently with the main app container for the Pod's entire lifecycle — ideal for log shipping, proxies, or sync loops. Both share volumes and localhost networking within the Pod.

    **Q7 — Bare Pods in production:** Bare Pods have no controller to recreate them if deleted or evicted. Node failure permanently removes them until manual intervention. Deployments (via ReplicaSets) maintain desired replica count, support rolling updates, and provide rollback history — essential for production availability and release management.

## Related Tutorials

- [kubectl Essentials and Workflows](kubectl-essentials-and-workflows.md) *(previous)*
- [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md) *(next in Module 2)*
- [From Docker to Kubernetes](../docker/from-docker-to-kubernetes.md)
- [Installing Kubernetes and kubectl](installing-kubernetes-and-kubectl.md)
- [Kubernetes – Category Overview](index.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [Kubernetes – Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Kubernetes – Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [Kubernetes – Init Containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)
- [Kubernetes – Sidecar Containers](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/)
- [Kubernetes – Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Kubernetes – Pod Networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
