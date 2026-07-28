---
title: Health Checks, Probes, and Self-Healing
description: Configure liveness, readiness, and startup probes so Kubernetes detects unhealthy containers, routes traffic safely, and automatically restarts failed workloads.
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: kubernetes
tags:
  - kubernetes
  - probes
  - liveness
  - readiness
  - startup
  - self-healing
  - reliability
prerequisites:
  - Complete [Namespaces and Resource Management](namespaces-and-resource-management.md)
  - Working cluster with kubectl; familiarity with Deployments and Services
  - Basic HTTP and TCP networking concepts
comments: false
---

# Health Checks, Probes, and Self-Healing

## Overview

Deploying a Pod is only the beginning. Production clusters must answer: **Is this container alive?** **Is it ready to receive traffic?** **Has it finished starting up?** Kubernetes answers these questions through **probes** — periodic health checks the kubelet runs against each container. Failed **liveness** probes trigger restarts; failed **readiness** probes remove the Pod from Service endpoints; **startup** probes protect slow-booting applications from premature liveness kills.

Combined with ReplicaSet controllers and node health monitoring, probes enable **self-healing**: crashed processes restart, unhealthy instances drain from load balancers, and the declared desired state converges without manual intervention. This is why Kubernetes replaces static "restart the service" runbooks with declarative health policies.

This is **Tutorial 12** in **Module 4: Networking & Operations** of the REBASH Academy Kubernetes series. Complete [Namespaces and Resource Management](namespaces-and-resource-management.md) first.

## Prerequisites

- Completed [Namespaces and Resource Management](namespaces-and-resource-management.md)
- Ability to deploy nginx or a simple HTTP app and expose it via a Service
- Understanding of Deployment rollouts and Pod lifecycle (Pending → Running → Terminating)
- Optional: `curl` inside the cluster or port-forward for probe verification
- Familiarity with YAML editing and `kubectl apply`

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Distinguish liveness, readiness, and startup probes and when to use each
- [ ] Configure HTTP, TCP, and exec probe handlers in Pod specs
- [ ] Tune probe timing: `initialDelaySeconds`, `periodSeconds`, `failureThreshold`, `timeoutSeconds`
- [ ] Explain how readiness failures affect Service endpoints and Ingress routing
- [ ] Diagnose crash loops and probe-induced restart storms
- [ ] Design probe endpoints that reflect application health, not just process existence
- [ ] Relate probe behaviour to Deployment rolling update success criteria

## Architecture

The kubelet runs probes locally on each node. Readiness state flows to the endpoints controller; liveness failures trigger container restarts.

```d2
direction: down

Node: "Worker Node" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        KL: kubelet
        Pod: "Pod: web" {
          style: {
            fill: "#dcfce7"
            stroke: "#16a34a"
          }
            C: "Container nginx"
            LP: "Liveness Probe"
            RP: "Readiness Probe"
            SP: "Startup Probe"
        }
        KL -> LP
        KL -> RP
        KL -> SP
        LP -> C: "HTTP GET /healthz"
        RP -> C: "HTTP GET /ready"
        SP -> C: "TCP :8080"
    }
    API: "API Server"
    EP: "Endpoints Controller"
    SVC: "Service web-svc"
    ING: Ingress
    Node.Pod.RP -> API: "Ready=true/false"
    API -> EP
    EP -> SVC
    SVC -> ING
    RESTART: "Container Restart"
    Node.Pod.LP -> RESTART: "Fail threshold"
    RESTART -> Node.Pod.C
```

## Theory

### Why Probes Exist

Without probes, Kubernetes assumes a running process is healthy. A deadlocked Java application, a nginx master with zero workers, or a database still replaying WAL all appear "Running" to the container runtime. Probes give the control plane **application-level signals**:

| Signal | Question answered | Action on failure |
|--------|-------------------|-------------------|
| **Liveness** | Should this container be restarted? | Kill and restart container |
| **Readiness** | Should this Pod receive traffic? | Remove from Service endpoints |
| **Startup** | Has the container finished booting? | Disable liveness until success |

### Liveness Probes

**Liveness** detects dead containers. When failures exceed `failureThreshold`, the kubelet **restarts** the container. Use liveness for unrecoverable states — deadlock, corrupted in-memory state, hung event loops.

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 10
  failureThreshold: 3
  timeoutSeconds: 2
```

!!! warning "Misconfigured liveness kills healthy pods"
    If liveness checks a dependency that is temporarily unavailable (database, cache), Kubernetes restarts pods in a loop. Liveness should verify **the container itself** can recover — not external services.

### Readiness Probes

**Readiness** determines traffic eligibility. A Pod can be Running but NotReady — for example, during warmup, cache loading, or leader election. The endpoints controller excludes NotReady pods from Service EndpointSlices; Ingress controllers stop routing to them.

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  periodSeconds: 5
  failureThreshold: 2
```

Readiness failures **do not** restart the container. The Pod stays Running until it passes again or is terminated by a rollout.

### Startup Probes

**Startup** probes address slow-starting containers — large JVM heaps, database migrations, model loading. While startup is failing, liveness probes are **disabled**. Once startup succeeds, liveness takes over.

```yaml
startupProbe:
  httpGet:
    path: /healthz
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
  # Allows up to 300 seconds to start
```

Without startup probes, you might set a large `initialDelaySeconds` on liveness — delaying crash detection for fast-fail scenarios. Startup probes decouple boot time from liveness sensitivity.

### Probe Handler Types

| Handler | Use case | Example |
|---------|----------|---------|
| **httpGet** | HTTP services with health endpoints | `GET /healthz` on port 8080 |
| **tcpSocket** | Services without HTTP (Redis, gRPC over TCP) | TCP connect to port 6379 |
| **exec** | Custom checks via script | `pg_isready -U postgres` |
| **grpc** | Native gRPC health protocol (K8s 1.24+) | gRPC health service |

HTTP probes support `httpHeaders`, `scheme` (HTTP/HTTPS), and success on status codes 200–399 by default.

### Probe Timing Parameters

| Field | Default | Meaning |
|-------|---------|---------|
| `initialDelaySeconds` | 0 | Wait before first probe (liveness/readiness) |
| `periodSeconds` | 10 | Interval between probes |
| `timeoutSeconds` | 1 | Probe must respond within this window |
| `successThreshold` | 1 | Consecutive successes to mark healthy |
| `failureThreshold` | 3 | Consecutive failures before action |

Total time before restart (liveness): roughly `initialDelaySeconds + (periodSeconds × failureThreshold)`.

### Self-Healing Mechanisms Beyond Probes

Probes are one layer of resilience:

```d2
direction: right

RS: ReplicaSet
    POD: Pods
    RS -> POD: "desired replicas"
    KL: kubelet
    RESTART: "Restart container"
    KL -> RESTART: "liveness fail"
    NC: "Node Controller"
    RESCH: "Reschedule pods"
    NC -> RESCH: "node NotReady"
    DC: "Deployment Controller"
    DC -> RS: rollout
    PDB: PodDisruptionBudget
    PDB -> RS: "min available"
```

- **ReplicaSet** recreates deleted pods to match `replicas`
- **Node controller** evicts pods when nodes fail
- **Deployment** rolls out new versions with `maxUnavailable` / `maxSurge` controls
- **PodDisruptionBudget** limits voluntary disruptions during maintenance

Probes ensure individual instances are healthy; controllers maintain desired count and rollout safety.

### Designing Health Endpoints

Production `/healthz` and `/ready` endpoints should differ:

| Endpoint | Checks | Should fail when |
|----------|--------|------------------|
| `/healthz` (liveness) | Process responsive, no deadlock | Unrecoverable internal state |
| `/ready` (readiness) | Can serve requests; dependencies OK | DB down, migration running, draining |

Avoid expensive checks on liveness (full DB query across shards). Keep liveness fast and local; readiness can check dependencies with timeouts.

## Hands-on Lab

### Step 1 – Deploy nginx without probes (baseline)

**Command:**

```bash
kubectl create namespace probe-lab
kubectl create deployment web \
  --image=nginx:1.25-alpine \
  --replicas=2 \
  -n probe-lab
kubectl expose deployment web --port=80 -n probe-lab
kubectl get pods -n probe-lab -o wide
kubectl get endpoints web -n probe-lab
```

**Explanation:** Without readiness probes, pods join endpoints as soon as containers start — potentially before nginx binds port 80.

**Expected output:**

```text
NAME                   READY   STATUS    RESTARTS   AGE
web-xxxxxxxxxx-xxxxx   1/1     Running   0          15s
web-xxxxxxxxxx-yyyyy   1/1     Running   0          15s
```

### Step 2 – Add HTTP liveness and readiness probes

**Command:**

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: probe-lab
spec:
  replicas: 2
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
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 10
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /
              port: 80
            periodSeconds: 5
            failureThreshold: 2
EOF

kubectl rollout status deployment/web -n probe-lab
kubectl describe pod -n probe-lab -l app=web | grep -A6 "Liveness\|Readiness"
```

**Explanation:** nginx serves `/` on port 80 — suitable for lab probes. Production apps expose dedicated `/healthz` endpoints.

**Expected output:**

```text
Liveness:   http-get http://:80/ delay=5s timeout=1s period=10s #success=1 #failure=3
Readiness:  http-get http://:80/ delay=0s timeout=1s period=5s #success=1 #failure=2
```

### Step 3 – Observe readiness during rollout

**Command:**

```bash
kubectl set image deployment/web nginx=nginx:1.25-alpine -n probe-lab
kubectl get pods -n probe-lab -w &
sleep 2
kubectl get endpoints web -n probe-lab -o yaml | grep -A3 addresses
kill %1 2>/dev/null || true
```

**Explanation:** During rollout, new pods may show `0/1 Ready` briefly. Endpoints update only for Ready pods — zero-downtime depends on readiness passing before old pods terminate.

**Expected output:**

```text
web-aaa   0/1   Running   0   5s
web-aaa   1/1   Running   0   8s
```

### Step 4 – Simulate liveness failure

**Command:**

```bash
POD=$(kubectl get pod -n probe-lab -l app=web -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n probe-lab "$POD" -- sh -c 'kill 1'
sleep 15
kubectl get pod -n probe-lab "$POD"
kubectl describe pod -n probe-lab "$POD" | tail -15
```

**Explanation:** Killing PID 1 in a container triggers liveness failure. The kubelet restarts the container — RESTARTS count increments.

**Expected output:**

```text
NAME          READY   STATUS    RESTARTS      AGE
web-xxxxx     1/1     Running   1 (10s ago)   5m
Warning  Unhealthy  Liveness probe failed...
Normal   Killing    Container nginx failed liveness probe, will be restarted
Normal   Started    Started container nginx
```

### Step 5 – Configure a startup probe for slow boot

**Command:**

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: slow-app
  namespace: probe-lab
spec:
  replicas: 1
  selector:
    matchLabels:
      app: slow-app
  template:
    metadata:
      labels:
        app: slow-app
    spec:
      containers:
        - name: app
          image: busybox:1.36
          command: ["sh", "-c", "sleep 30 && while true; do echo ok | nc -l -p 8080; done"]
          ports:
            - containerPort: 8080
          startupProbe:
            tcpSocket:
              port: 8080
            periodSeconds: 5
            failureThreshold: 12
          livenessProbe:
            tcpSocket:
              port: 8080
            periodSeconds: 10
            failureThreshold: 3
EOF

kubectl get pods -n probe-lab -l app=slow-app -w &
sleep 35
kill %1 2>/dev/null || true
kubectl get pods -n probe-lab -l app=slow-app
```

**Explanation:** The app sleeps 30 seconds before listening. Startup probe allows 60 seconds (`12 × 5s`) without liveness killing the container during boot.

**Expected output:**

```text
slow-app-xxxxx   0/1   Running   0   10s
slow-app-xxxxx   1/1   Running   0   35s
```

### Step 6 – Use exec probe (optional pattern)

**Command:**

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: exec-probe-demo
  namespace: probe-lab
spec:
  containers:
    - name: demo
      image: busybox:1.36
      command: ["sh", "-c", "touch /tmp/healthy && sleep 3600"]
      livenessProbe:
        exec:
          command:
            - cat
            - /tmp/healthy
        periodSeconds: 5
EOF

kubectl get pod exec-probe-demo -n probe-lab
kubectl exec -n probe-lab exec-probe-demo -- rm /tmp/healthy
sleep 20
kubectl get pod exec-probe-demo -n probe-lab
```

**Explanation:** Exec probes run commands inside the container. Removing `/tmp/healthy` simulates an unhealthy state — kubelet restarts the container.

**Expected output:**

```text
exec-probe-demo   1/1   Running   1 (5s ago)   45s
```

### Step 7 – Clean up

**Command:**

```bash
kubectl delete namespace probe-lab --wait=false
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
| `kubectl describe pod` | View probe configuration and events | `kubectl describe pod <name>` |
| `kubectl get endpoints` | See which pods receive traffic | `kubectl get endpoints web -n prod` |
| `kubectl logs --previous` | Logs from crashed container | `kubectl logs pod -c app --previous` |
| `kubectl rollout restart` | Force new pods (re-run probes) | `kubectl rollout restart deploy/web` |
| `kubectl debug` | Attach debug container to running pod | `kubectl debug -it pod/name --image=busybox` |

### Production probe template

```yaml
containers:
  - name: api
    image: myorg/api:v2.4.1
    ports:
      - containerPort: 8080
    startupProbe:
      httpGet:
        path: /healthz
        port: 8080
      failureThreshold: 30
      periodSeconds: 10
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      periodSeconds: 10
      failureThreshold: 3
      timeoutSeconds: 2
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      periodSeconds: 5
      failureThreshold: 2
      timeoutSeconds: 3
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Using the same endpoint for liveness and readiness"
    Readiness should gate traffic including dependency checks. Liveness should be minimal — checking external DBs on liveness causes restart loops during outages.

!!! warning "Too-aggressive liveness timing"
    `periodSeconds: 1` with `failureThreshold: 1` restarts on any transient blip. Allow headroom for GC pauses and brief CPU starvation.

!!! warning "HTTPS probe without proper scheme"
    Probes default to HTTP. For TLS-only ports, set `scheme: HTTPS` or probe a separate admin HTTP port.

!!! warning "Ignoring readiness during rollouts"
    If readiness never passes, Deployment rollouts stall with `ProgressDeadlineExceeded`. Monitor rollout status and probe endpoints in CI.

## Best Practices

!!! tip "Implement /healthz and /ready in application code"
    Frameworks like Spring Boot Actuator, ASP.NET health checks, and Go `net/http` handlers make this straightforward. Document what each checks.

!!! tip "Log probe failures at warn level"
    Correlate kubelet Unhealthy events with application logs to distinguish probe misconfiguration from real failures.

!!! tip "Use startup probes for JVM and ML workloads"
    Boot times over 30 seconds are common. Startup probes avoid choosing between long `initialDelaySeconds` and false-positive liveness kills.

!!! tip "Test probes under load"
    Health endpoints must respond during peak traffic. Slow probes cause unnecessary NotReady states and uneven load balancing.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| CrashLoopBackOff | Liveness fails immediately on start | Add startup probe; increase `initialDelaySeconds` |
| Pod Running but no traffic | Readiness failing | Check `/ready` endpoint; verify dependencies |
| Frequent restarts under load | Liveness timeout too short | Increase `timeoutSeconds`; optimise health handler |
| Rollout stuck | New pods never Ready | `kubectl describe pod`; fix readiness probe path/port |
| 502 from Ingress during deploy | Old pods terminated before new Ready | Tune `maxUnavailable`; fix readiness timing |
| Probe works locally, fails in cluster | Wrong port or network policy | Verify `containerPort`; check NetworkPolicy |

## Summary

- **Liveness** probes restart unhealthy containers; **readiness** probes control Service traffic; **startup** probes protect slow boot sequences
- Probe handlers include **HTTP**, **TCP**, **exec**, and **gRPC** — choose based on application protocol
- Timing parameters (`periodSeconds`, `failureThreshold`, `timeoutSeconds`) determine sensitivity vs stability
- Self-healing combines probes with ReplicaSets, node monitoring, and Deployment rollouts
- Design separate health endpoints: liveness checks internal recovery; readiness checks request-serving ability
- Misconfigured probes cause restart storms — test under failure and load conditions before production

## Interview Questions

1. What is the difference between a liveness probe and a readiness probe?
2. When would you use a startup probe instead of increasing `initialDelaySeconds` on liveness?
3. What happens to Service endpoints when a Pod fails its readiness probe?
4. Name three probe handler types and give a use case for each.
5. How does the kubelet act on consecutive liveness probe failures?
6. Why should liveness probes avoid checking external dependencies like databases?
7. Explain how readiness probes enable zero-downtime Deployments.
8. What is CrashLoopBackOff and how can probes contribute to it?
9. What HTTP status codes does Kubernetes consider successful for httpGet probes?
10. How do probes interact with PodDisruptionBudgets during node drains?

??? tip "Sample Answers (Questions 1, 3, and 7)"

    **Q1 — Liveness vs readiness:** A liveness probe asks whether the container is alive and should be restarted if broken. Failure causes the kubelet to kill and restart the container. A readiness probe asks whether the Pod should receive traffic. Failure removes the Pod from Service endpoints but does not restart it — useful during startup, dependency outages, or graceful shutdown.

    **Q3 — Readiness and endpoints:** When readiness fails, the Pod's IP is removed from EndpointSlice objects backing the Service. kube-proxy and Ingress controllers stop forwarding traffic to that Pod. When readiness passes again, the IP is re-added. Other Ready pods continue receiving traffic.

    **Q7 — Zero-downtime rollouts:** During a rolling update, new Pods must pass readiness before old Pods are terminated (subject to `maxUnavailable`/`maxSurge`). Readiness ensures traffic only routes to instances that can handle requests. Combined with graceful termination (`preStop` hooks), this avoids sending requests to starting or shutting-down containers.

## Related Tutorials

- [Kubernetes – Category Overview](index.md)
- [Namespaces and Resource Management](namespaces-and-resource-management.md) *(previous — Module 4)*
- [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md) *(next — Module 5)*
- [Ingress and External Access](ingress-and-external-access.md)
- [Troubleshooting Kubernetes Workloads](troubleshooting-kubernetes-workloads.md)

## References

- [Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes)
- [Pod Disruption Budgets](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)
- [Deployment – Rolling Update](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment)
- [gRPC Health Checking Protocol](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-a-grpc-liveness-probe)
