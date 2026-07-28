---
title: Troubleshooting Kubernetes Workloads
description: Systematically diagnose failing pods, scheduling issues, networking problems, and rollout failures using kubectl, events, logs, and a production-grade troubleshooting methodology.
difficulty: advanced
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: kubernetes
tags:
  - kubernetes
  - troubleshooting
  - debugging
  - kubectl
  - sre
  - operations
prerequisites:
  - Complete [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md)
  - Solid understanding of Pods, Deployments, Services, Ingress, probes, and namespaces
  - kubectl access to a cluster where you can intentionally break workloads for lab exercises
comments: false
---

# Troubleshooting Kubernetes Workloads

## Overview

When a Deployment fails at 2 AM, you need a **systematic method** — not random `kubectl` commands. Kubernetes exposes rich diagnostic signals: **Pod status**, **Events**, **container logs**, **probe results**, **endpoint state**, and **node conditions**. Advanced troubleshooting connects these layers: is the Pod scheduled? Is the container starting? Is the app healthy? Is the Service routing traffic? Is Ingress configured correctly?

This tutorial teaches the **REBASH troubleshooting funnel** — start broad (namespace events), narrow to the failing object (Pod → container), then verify dependencies (Service, DNS, RBAC). You will practice on deliberately broken workloads and build reflexes that SRE and platform engineers use daily.

This is **Tutorial 14** in **Module 5: Security & Tooling** of the REBASH Academy Kubernetes series. Complete [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md) first.

## Prerequisites

- Completed [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md)
- Familiarity with all Module 4 topics: Ingress, namespaces, quotas, and health probes
- Cluster access (minikube, kind, k3s, or cloud) where you can create failing workloads
- Comfort with `kubectl describe`, `kubectl logs`, and YAML editing
- Optional: [Networking Troubleshooting Methodology](../networking/network-troubleshooting-methodology.md) for L3/L4 correlation

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply a structured troubleshooting funnel from symptom to root cause
- [ ] Interpret Pod phases, conditions, and container waiting/terminated reasons
- [ ] Use Events and `kubectl describe` to diagnose scheduling and admission failures
- [ ] Debug CrashLoopBackOff, ImagePullBackOff, and probe-induced restart loops
- [ ] Verify Service → Endpoints → Pod connectivity with kubectl and in-cluster tests
- [ ] Use `kubectl debug`, ephemeral containers, and port-forward effectively
- [ ] Correlate Deployment rollout failures with ReplicaSet and revision history
- [ ] Document incidents with evidence suitable for postmortems

## Architecture

Troubleshooting flows from the user-visible symptom down through Kubernetes layers to the container process.

```d2
direction: down

SYM: "Symptom\n502 / CrashLoop / Pending"
    ING: "Ingress / LoadBalancer"
    SVC: Service
    EP: "Endpoints / EndpointSlice"
    POD: "Pod Status"
    CTR: "Container State"
    APP: "Application Logs"
    SYM -> ING
    ING -> SVC: "route OK?"
    SVC -> EP: "endpoints exist?"
    EP -> POD: "targets ready?"
    POD -> CTR: "scheduled? probes?"
    CTR -> APP: "exit code / OOM"
    EVT: Events
    EVT -> POD: {
      style.stroke-dash: 3
    }
    EVT -> ING: {
      style.stroke-dash: 3
    }
    NODE: "Node Conditions"
    NODE -> POD: {
      style.stroke-dash: 3
    }
```

## Theory

### The Troubleshooting Funnel

Follow this order to avoid chasing red herrings:

| Step | Check | Key commands |
|------|-------|--------------|
| 1 | **Scope** — namespace, time, blast radius | `kubectl get pods -A`, alerts |
| 2 | **Workload status** — Deployment, ReplicaSet | `kubectl rollout status`, `kubectl get rs` |
| 3 | **Pod phase** — Pending, Running, Failed | `kubectl get pods`, `kubectl describe pod` |
| 4 | **Container state** — waiting, running, terminated | `describe`, `logs --previous` |
| 5 | **Networking** — Service, Endpoints, DNS | `kubectl get endpoints`, `nslookup` |
| 6 | **Node / cluster** — capacity, taints, CNI | `kubectl describe node`, `kubectl get events` |

Document findings at each step before diving deeper.

### Pod Phases and Conditions

| Phase | Meaning |
|-------|---------|
| **Pending** | Not yet scheduled or waiting for volumes |
| **Running** | At least one container started |
| **Succeeded** | All containers terminated successfully (Jobs) |
| **Failed** | At least one container failed |
| **Unknown** | Node communication lost |

**Conditions** (Ready, PodScheduled, Initialized, ContainersReady) appear in `kubectl describe pod`. `Ready=False` with `Running` phase often indicates readiness probe failure — not a crash.

### Container Waiting Reasons

| Reason | Typical cause |
|--------|---------------|
| **ContainerCreating** | Pulling image, mounting volumes |
| **ImagePullBackOff** | Wrong tag, missing registry auth, rate limit |
| **CrashLoopBackOff** | App exits; liveness restart loop |
| **CreateContainerConfigError** | Missing Secret/ConfigMap reference |
| **InvalidImageName** | Malformed image reference in spec |

### Container Terminated Reasons

| Reason | Typical cause |
|--------|---------------|
| **OOMKilled** | Memory limit exceeded |
| **Error** | Non-zero exit code |
| **Completed** | Normal exit (Jobs, init containers) |
| **Evicted** | Node pressure; see Events for message |

Check `lastState.terminated.exitCode` in Pod JSON for application-specific codes.

### Events: The First Place to Look

Events are time-ordered, TTL-garbage-collected messages attached to objects:

```bash
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
kubectl describe pod <name> -n <namespace>  # Events at bottom
```

Common event messages:

- `FailedScheduling` — insufficient CPU/memory, taints, affinity rules
- `FailedMount` — PVC not bound, wrong secret name
- `Unhealthy` — probe failures
- `BackOff` — restarting failed container with exponential delay

### Scheduling Failures

When Pods stay **Pending**, the scheduler could not place them:

```bash
kubectl describe pod <pending-pod> | grep -A5 Events
kubectl describe nodes | grep -A10 "Allocated resources"
kubectl get pods -A --field-selector=status.phase=Pending
```

Causes: resource requests exceed node capacity, **taints** without tolerations, **nodeSelector** / **affinity** mismatches, **ResourceQuota** exhaustion, PVC unbound.

### CrashLoopBackOff Investigation

```bash
kubectl logs <pod> -c <container> --previous
kubectl describe pod <pod> | grep -A3 "Last State"
```

Workflow:

1. Read `--previous` logs from last crashed instance
2. Check exit code (1 = app error, 137 = SIGKILL/OOM, 143 = SIGTERM)
3. Verify command, args, env vars, mounted Secrets
4. Temporarily disable liveness probe to distinguish crash vs probe kill
5. Run interactively: `kubectl run debug --rm -it --image=<same-image> -- sh`

### Networking Troubleshooting

Traffic path: **Ingress → Service → Endpoints → Pod IP:port**

```bash
kubectl get ingress,svc,endpoints -n <ns>
kubectl run tmp --rm -it --image=busybox:1.36 --restart=Never -- \
  wget -qO- http://<service>.<ns>.svc.cluster.local
```

| Symptom | Check |
|---------|-------|
| Connection refused | Pod not listening on `targetPort` |
| No endpoints | Readiness failing or label selector mismatch |
| 404 from Ingress | Path/host rule mismatch |
| DNS failure | CoreDNS; verify `ndots` and search paths |

Label selector mismatches between Service and Pod are a frequent subtle bug — `app` vs `app.kubernetes.io/name`.

### Deployment Rollout Failures

```bash
kubectl rollout status deployment/<name> -n <ns>
kubectl rollout history deployment/<name> -n <ns>
kubectl get rs -n <ns> -l app=<label>
```

`ProgressDeadlineExceeded` means new ReplicaSet pods never became Ready within `progressDeadlineSeconds`. Compare old vs new Pod events and image tags.

Rollback: `kubectl rollout undo deployment/<name> -n <ns>`

### Advanced Debug Techniques

| Technique | Use case |
|-----------|----------|
| `kubectl debug -it pod/<name> --image=busybox` | Ephemeral debug container (K8s 1.23+) |
| `kubectl cp` | Copy files from crashed pod before garbage collection |
| `kubectl port-forward svc/<name> 8080:80` | Local access without Ingress |
| `kubectl exec -it <pod> -- sh` | Live container inspection |
| `kubectl get pod <name> -o yaml` | Full spec for diff against working revision |

For distroless images without shell, use debug containers or copy binary with `kubectl debug` node features.

### RBAC and Admission Denials

`Forbidden` errors when applying manifests or from in-cluster clients:

```bash
kubectl auth can-i create deployments -n <ns> --as=<identity>
kubectl get validatingwebhookconfigurations
kubectl get mutatingwebhookconfigurations
```

Webhook timeouts manifest as intermittent apply failures — check API server logs on managed clusters via cloud console.

## Hands-on Lab

Create a dedicated namespace and break things intentionally.

### Step 1 – Set up troubleshooting namespace

**Command:**

```bash
kubectl create namespace troubleshoot-lab
kubectl config set-context --current --namespace=troubleshoot-lab
kubectl get events --sort-by='.lastTimestamp' | tail -5
```

**Explanation:** Start every incident by confirming namespace context and scanning recent events.

**Expected output:**

```text
namespace/troubleshoot-lab created
LAST SEEN   TYPE     REASON    OBJECT   MESSAGE
```

### Step 2 – Diagnose ImagePullBackOff

**Command:**

```bash
kubectl run bad-image --image=nginx:does-not-exist-tag
sleep 20
kubectl get pod bad-image
kubectl describe pod bad-image | tail -20
kubectl get events --field-selector involvedObject.name=bad-image
```

**Explanation:** Image pull failures show in container `waiting.reason` and Events with registry error details.

**Expected output:**

```text
STATUS    REASON             MESSAGE
Waiting   ImagePullBackOff   Back-off pulling image "nginx:does-not-exist-tag"
Warning   Failed             Failed to pull image ...
```

**Fix:**

```bash
kubectl set image pod/bad-image bad-image=nginx:1.25-alpine
# Or delete and recreate — pod spec image is immutable on existing pod
kubectl delete pod bad-image --force --grace-period=0
kubectl run bad-image --image=nginx:1.25-alpine
```

### Step 3 – Diagnose CrashLoopBackOff

**Command:**

```bash
kubectl run crasher --image=busybox:1.36 -- sh -c "echo starting && exit 1"
sleep 25
kubectl get pod crasher
kubectl logs crasher --previous 2>/dev/null || kubectl logs crasher
kubectl describe pod crasher | grep -A8 "Last State"
```

**Explanation:** Exit code 1 in logs confirms application failure. `--previous` captures the crashed instance during BackOff.

**Expected output:**

```text
starting
State:     Waiting
  Reason:  CrashLoopBackOff
Last State: Terminated
  Reason:   Error
  Exit Code: 1
```

### Step 4 – Diagnose Pending (resource pressure)

**Command:**

```bash
kubectl run hungry --image=nginx:1.25-alpine \
  --requests=cpu=999,memory=999Gi \
  --limits=cpu=999,memory=999Gi
sleep 10
kubectl get pod hungry
kubectl describe pod hungry | grep -A10 Events
```

**Explanation:** Unschedulable pods emit `FailedScheduling` events with exact resource shortfall.

**Expected output:**

```text
Warning  FailedScheduling  0/1 nodes are available: 1 Insufficient cpu, 1 Insufficient memory
```

**Fix:**

```bash
kubectl delete pod hungry
kubectl run hungry --image=nginx:1.25-alpine --requests=cpu=50m,memory=64Mi
```

### Step 5 – Diagnose Service selector mismatch

**Command:**

```bash
kubectl create deployment web --image=nginx:1.25-alpine --replicas=2
kubectl expose deployment web --port=80 --target-port=80
kubectl patch svc web -p '{"spec":{"selector":{"app":"wrong-label"}}}'
kubectl get endpoints web
kubectl run curl-test --image=curlimages/curl:8.5.0 --restart=Never -- \
  curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 http://web/ || true
sleep 5
kubectl logs curl-test 2>/dev/null; kubectl describe svc web | grep -A3 Selector
```

**Explanation:** Empty endpoints mean no Pod matches Service selector — traffic has nowhere to go.

**Expected output:**

```text
Selector:  app=wrong-label
Endpoints: <none>
000  # curl connection failed
```

**Fix:**

```bash
kubectl patch svc web -p '{"spec":{"selector":{"app":"web"}}}'
kubectl get endpoints web
```

### Step 6 – Diagnose readiness probe failure

**Command:**

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: probe-fail
spec:
  replicas: 1
  selector:
    matchLabels:
      app: probe-fail
  template:
    metadata:
      labels:
        app: probe-fail
    spec:
      containers:
        - name: nginx
          image: nginx:1.25-alpine
          readinessProbe:
            httpGet:
              path: /nonexistent
              port: 80
            periodSeconds: 3
            failureThreshold: 1
EOF

sleep 15
kubectl get pods -l app=probe-fail
kubectl describe pod -l app=probe-fail | grep -A2 Unhealthy
kubectl get endpoints -l app=probe-fail 2>/dev/null || kubectl get endpoints
```

**Explanation:** Running but NotReady pods fail readiness — excluded from endpoints despite healthy process.

**Expected output:**

```text
probe-fail-xxxxx   0/1   Running   0   15s
Warning  Unhealthy  Readiness probe failed: HTTP probe failed with statuscode: 404
```

**Fix:** Change probe path to `/` or implement `/ready` endpoint.

### Step 7 – Practice rollback after bad rollout

**Command:**

```bash
kubectl set image deployment/web web=nginx:1.25-alpine
kubectl rollout status deployment/web
kubectl set image deployment/web web=nginx:bad-tag-xyz
sleep 30
kubectl rollout status deployment/web --timeout=20s || true
kubectl get rs -l app=web
kubectl rollout undo deployment/web
kubectl rollout status deployment/web
```

**Explanation:** Failed rollouts leave old ReplicaSet scaled down but available. `rollout undo` reverts to previous revision.

**Expected output:**

```text
error: deployment "web" exceeded its progress deadline
deployment.apps/web rolled back
deployment "web" successfully rolled out
```

### Step 8 – Clean up and document

**Command:**

```bash
kubectl delete namespace troubleshoot-lab --wait=false
kubectl config set-context --current --namespace=default
echo "Incident template: Symptom → Scope → Pod → Container → Network → Root cause → Fix"
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
| `kubectl describe` | Detailed object state + events | `kubectl describe pod <name>` |
| `kubectl logs --previous` | Logs from crashed container | `kubectl logs <pod> -c app --previous` |
| `kubectl get events` | Namespace events sorted by time | `kubectl get events --sort-by='.lastTimestamp'` |
| `kubectl rollout undo` | Revert failed deployment | `kubectl rollout undo deploy/web` |
| `kubectl debug` | Attach ephemeral debug container | `kubectl debug -it pod/<name> --image=busybox` |
| `kubectl top pod` | Live CPU/memory (metrics-server) | `kubectl top pod -n prod` |

### Troubleshooting checklist script

Save as `~/bin/k8s-triage.sh`:

```bash
#!/usr/bin/env bash
# k8s-triage.sh — quick workload triage
set -euo pipefail
NS="${1:-default}"
APP="${2:-}"

section() { printf '\n=== %s ===\n' "$1"; }

section "Context"
kubectl config current-context
kubectl config view --minify -o jsonpath='{.contexts[0].context.namespace}{"\n"}' 2>/dev/null || echo "default"

section "Recent Events ($NS)"
kubectl get events -n "$NS" --sort-by='.lastTimestamp' | tail -15

section "Problem Pods ($NS)"
kubectl get pods -n "$NS" --field-selector=status.phase!=Running,status.phase!=Succeeded 2>/dev/null || \
  kubectl get pods -n "$NS" | grep -vE 'Running|Completed' || echo "None"

if [ -n "$APP" ]; then
  section "Deployment ($APP)"
  kubectl get deploy,rs,pods,svc,endpoints -n "$NS" -l "app=$APP" 2>/dev/null || true
fi
```

Usage: `chmod +x ~/bin/k8s-triage.sh && ~/bin/k8s-triage.sh troubleshoot-lab web`

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Skipping Events and going straight to logs"
    Events explain *why* a Pod is Pending or FailedMount — logs are empty when the container never started.

!!! warning "Debugging the wrong namespace"
    Always verify `kubectl config view --minify` context. Cross-namespace Service DNS mistakes waste hours.

!!! warning "Ignoring label selector mismatches"
    Deployment labels, Service selectors, and NetworkPolicy selectors must align. Typos cause empty endpoints silently.

!!! warning "Restarting pods without capturing --previous logs"
    CrashLoopBackOff garbage-collects old container logs quickly. Capture evidence before delete or restart.

## Best Practices

!!! tip "Run a pre-incident checklist under calm conditions"
    Practice `k8s-triage.sh` on healthy clusters so muscle memory exists during outages.

!!! tip "Fix forward with rollout undo only after root cause"
    Undo restores service but hides the bad change. Capture failing image tag and config diff first.

!!! tip "Use field selectors and labels consistently"
    Standardize on `app.kubernetes.io/name` and `app.kubernetes.io/instance` — reduces selector drift.

!!! tip "Write postmortems with kubectl evidence"
    Paste Events timestamps, exit codes, and quota messages — not just "pod crashed."

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Pod Pending forever | Scheduling constraints | `describe pod` Events; check quota, taints, affinity |
| Empty endpoints | Selector mismatch or NotReady | Verify labels; fix readiness probe |
| Intermittent 502 | Rolling update + bad readiness | Tune probes; check `maxUnavailable` |
| OOMKilled | Memory limit too low | Increase limit; profile app memory |
| Forbidden on apply | RBAC | `kubectl auth can-i`; fix RoleBinding |
| Works via port-forward, not Ingress | Ingress misconfiguration | `describe ingress`; verify host/path/backend |
| No logs available | Container never started | Check Events for mount/pull errors |

## Summary

- Use a **structured funnel**: scope → workload → pod → container → network → cluster
- **Events** and `kubectl describe` reveal scheduling, mount, and probe failures before logs help
- **CrashLoopBackOff** requires `--previous` logs and exit code analysis; distinguish OOM from app errors
- **Empty endpoints** usually mean label selector mismatch or readiness failure — not Ingress issues
- **Rollout undo** restores service; always capture failing revision for root cause analysis
- Advanced tools (`kubectl debug`, port-forward, triage scripts) accelerate diagnosis under pressure

## Interview Questions

1. What is the first command or information source you check when a Deployment is failing?
2. Explain the difference between Pod phase `Running` and condition `Ready=False`.
3. How do you retrieve logs from a container that crashed and restarted?
4. What causes ImagePullBackOff and how do you diagnose it?
5. A Service exists but has no endpoints. List three possible causes.
6. What does exit code 137 typically indicate in a terminated container?
7. Describe the traffic path from Ingress to Pod and where to inspect each hop.
8. What is ProgressDeadlineExceeded on a Deployment?
9. When would you use `kubectl debug` instead of `kubectl exec`?
10. How do ResourceQuota and scheduling failures appear in Pod Events?

??? tip "Sample Answers (Questions 3, 5, and 7)"

    **Q3 — Crashed container logs:** Use `kubectl logs <pod-name> -c <container-name> --previous`. The `--previous` flag returns logs from the last terminated instance of the container — essential during CrashLoopBackOff. If the container never started (ImagePullBackOff), logs are unavailable; use Events instead.

    **Q5 — No endpoints:** (1) Service selector does not match any Pod labels. (2) All matching Pods fail readiness probes and are excluded. (3) No Pods exist — Deployment scaled to zero or ReplicaSet failed to create pods. Verify with `kubectl get pods --show-labels` and compare to `kubectl describe svc`.

    **Q7 — Ingress to Pod path:** Client hits Ingress controller → controller matches Ingress rules → forwards to Service ClusterIP:port → kube-proxy or CNI routes to Pod IP:targetPort on a Ready endpoint. Inspect: `kubectl describe ingress`, `kubectl get endpoints`, `kubectl get pods -o wide`, and in-cluster curl to Service DNS.

## Related Tutorials

- [Kubernetes – Category Overview](index.md)
- [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md) *(previous — Module 5)*
- [Helm Package Management](helm-package-management.md) *(next in Module 5)*
- [Health Checks, Probes, and Self-Healing](health-checks-probes-and-self-healing.md)
- [Networking – Network Troubleshooting Methodology](../networking/network-troubleshooting-methodology.md)
- Cheat sheet: [Kubernetes Cheat Sheet](../cheatsheets/kubernetes.md)
- Interview prep: [Kubernetes Interview Prep](../interview/kubernetes.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)
- [Debug Init Containers](https://kubernetes.io/docs/tasks/debug/debug-application/debug-init-containers/)
- [Determine Pod Failure Reason](https://kubernetes.io/docs/tasks/debug/debug-application/determine-reason-pod-failure/)
- [Troubleshoot Applications](https://kubernetes.io/docs/tasks/debug/debug-application/)
- [kubectl Reference – logs, describe, events](https://kubernetes.io/docs/reference/kubectl/)
- [Deployment – Rolling Back](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment)
