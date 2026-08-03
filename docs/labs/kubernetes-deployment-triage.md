---
title: "Lab — Kubernetes Deployment Triage"
description: "Debug a CrashLoopBackOff Deployment with bad probes and image tags, restore Ready pods, and verify via port-forward — a realistic Kubernetes on-call lab."
difficulty: intermediate
estimated_time: "70 min"
category: labs
author: Shaik Basha
last_updated: "2026-08-03"
tags:
  - labs
  - kubernetes
  - deployments
  - troubleshooting
comments: false
---

# Lab — Kubernetes Deployment Triage

## Lab Overview

**Purpose:** Practise the standard kubectl triage loop for a failing Deployment.

**Scenario:** `web` in namespace `rebash-triage-lab` is not Ready. Events show probe or image failures. You must restore a healthy rollout without deleting the namespace blindly.

**Expected outcome:** Deployment Available, Pods Ready, HTTP 200 through port-forward.

!!! tip "This is a lab, not a tutorial"
    Use evidence from `describe`, `logs`, and Events before changing manifests.

## Business Scenario

A platform team runs a demo status API on **kind** or **minikube** for stakeholder demos. After a manifest edit, the Deployment entered probe failures. The demo is in 30 minutes. You must recover the workload with clear validation.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Triage Pods with `get`, `describe`, `logs`, and Events
- [ ] Distinguish image pull errors from probe misconfiguration
- [ ] Apply a fixed manifest safely and watch rollout status
- [ ] Expose and verify with Service + port-forward
- [ ] Clean up namespaces completely

## Prerequisites

### Knowledge

- [Installing Kubernetes and kubectl](../kubernetes/installing-kubernetes-and-kubectl.md)
- [Pods — The Atomic Unit](../kubernetes/pods-the-atomic-unit.md)
- [Deployments](../kubernetes/deployments-managing-replicated-pods.md)
- [Health Checks — Probes](../kubernetes/health-checks-probes-and-self-healing.md)
- [Services and Cluster Networking](../kubernetes/services-and-cluster-networking.md)
- [Troubleshooting Kubernetes Workloads](../kubernetes/troubleshooting-kubernetes-workloads.md)

### Software

| Tool | Notes |
|------|--------|
| kubectl | configured context |
| kind **or** minikube | local cluster |
| Docker (for kind) | image runtime |

**Estimated cost:** £0 locally.

## Architecture

![Kubernetes deployment triage from CrashLoopBackOff through describe/logs to fix and verify](../assets/images/lab-kubernetes-deployment-triage.svg)

## Environment

Local Kubernetes (kind/minikube). Confirm:

``` {.bash .ra-terminal title="Terminal"}
kubectl cluster-info
kubectl get nodes
```

Workspace:

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-lab-k8s && cd ~/rebash-lab-k8s
```

## Real-world scenario

On-call receives an alert: `web` Deployment in `rebash-triage-lab` has zero Ready replicas. Stakeholder demo is imminent. You reproduce the failure, gather describe/logs/events evidence, apply a corrected manifest, and prove HTTP 200 before handover.

## Step-by-step tasks

### Task 1 — Create namespace and broken workload

Create `namespace.yaml`:

```yaml title="namespace.yaml"
apiVersion: v1
kind: Namespace
metadata:
  name: rebash-triage-lab
  labels:
    app.kubernetes.io/managed-by: rebash-lab
```

Create `web-broken.yaml`:

```yaml title="web-broken.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: rebash-triage-lab
  labels:
    app: web
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
        - name: web
          image: nginx:1.27-alpine
          ports:
            - containerPort: 80
          readinessProbe:
            httpGet:
              path: /healthz
              port: 80
            initialDelaySeconds: 2
            periodSeconds: 3
          livenessProbe:
            httpGet:
              path: /healthz
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: web
  namespace: rebash-triage-lab
spec:
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 80
```

Apply and confirm failure:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-lab-k8s
kubectl apply -f namespace.yaml
kubectl apply -f web-broken.yaml
kubectl rollout status deployment/web -n rebash-triage-lab --timeout=60s || true
kubectl get pods -n rebash-triage-lab -l app=web
```

!!! example "Expected output"
    Pods `0/1 Ready` or restarting; Events will mention probe failures (nginx has no `/healthz`).


### Task 2 — Triage with kubectl

Gather evidence before patching.

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-lab-k8s
kubectl get deploy,po,svc -n rebash-triage-lab -o wide | tee before-resources.txt
kubectl describe deploy web -n rebash-triage-lab | tee before-describe.txt
kubectl describe po -n rebash-triage-lab -l app=web | tee before-pod-describe.txt
kubectl logs -n rebash-triage-lab -l app=web --tail=30 | tee before-logs.txt || true
kubectl get events -n rebash-triage-lab --sort-by=.lastTimestamp | tail -n 20 | tee before-events.txt
grep -Ei 'probe|healthz|unhealthy' before-events.txt before-pod-describe.txt
```

!!! example "Expected output"
    Readiness/liveness failures on `/healthz`.


### Task 3 — Apply fixed manifest and roll out

Create `web-fixed.yaml`:

```yaml title="web-fixed.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: rebash-triage-lab
  labels:
    app: web
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
        - name: web
          image: nginx:1.27-alpine
          ports:
            - containerPort: 80
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 2
            periodSeconds: 3
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
```

Apply and verify Ready:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-lab-k8s
kubectl apply -f web-fixed.yaml
kubectl rollout status deploy/web -n rebash-triage-lab --timeout=120s
kubectl get po -n rebash-triage-lab -l app=web | tee after-pods.txt
```

!!! example "Expected output"
    `successfully rolled out`; Pods `1/1 Ready`.


### Task 4 — Verify via Service and port-forward

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-lab-k8s
kubectl port-forward -n rebash-triage-lab svc/web 18081:80 &
PF_PID=$!
sleep 2
curl -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1:18081/ | tee http-code.txt
curl -sS http://127.0.0.1:18081/ | head -c 200 | tee http-body.txt
kill "${PF_PID}" 2>/dev/null || true
grep -q '200' http-code.txt
```

!!! example "Expected output"
    HTTP 200 and nginx welcome HTML.


### Task 5 — Optional second failure (bad image tag)

Create `web-bad-image.yaml` (same as `web-fixed.yaml` but with a bad image tag):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: rebash-triage-lab
  labels:
    app: web
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
        - name: web
          image: nginx:this-tag-does-not-exist
          ports:
            - containerPort: 80
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 2
            periodSeconds: 3
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
```

Apply, triage, and restore:
cd ~/rebash-lab-k8s
kubectl apply -f web-bad-image.yaml
kubectl rollout status deploy/web -n rebash-triage-lab --timeout=30s || true
kubectl describe po -n rebash-triage-lab -l app=web | grep -i image | tee image-error.txt
kubectl apply -f web-fixed.yaml
kubectl rollout status deploy/web -n rebash-triage-lab --timeout=120s
```

!!! example "Expected output"
    Image pull errors in Events, then recovery after restoring a real tag.


Archive evidence:

```bash
cd ~/rebash-lab-k8s
tar -czf triage-evidence.tgz namespace.yaml web-broken.yaml web-fixed.yaml before-*.txt after-pods.txt http-code.txt
ls -l triage-evidence.tgz
```

## Validation steps

- [ ] Broken Deployment fails on `/healthz` probe path
- [ ] describe/events identify root cause before fix
- [ ] Fixed manifest reaches Ready
- [ ] port-forward curl returns HTTP 200
- [ ] Evidence tarball contains before/after files

## Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Probe failed HTTP 404 | Path not served | Probe `/` for default nginx |
| ImagePullBackOff | Bad tag / registry auth | Restore pinned tag `nginx:1.27-alpine` |
| Pending Pod | Quota / scheduling | `kubectl describe pod` |
| Endpoints empty | Pods not Ready | Fix probes first |
| port-forward refused | Service missing | Apply Service from `web-broken.yaml` |

## Challenge exercise

Add a ConfigMap with custom `index.html`, mount it in `web-fixed.yaml`, and verify the body through port-forward contains your custom text.

## Learning outcomes

- Executed describe → logs → events triage on a failing Deployment
- Separated probe misconfiguration from image pull failures
- Applied declarative fixes and verified with port-forward
- Packaged before/after evidence for handover

## Cleanup

```bash
kubectl delete namespace rebash-triage-lab --wait=true --ignore-not-found
rm -rf ~/rebash-lab-k8s
```

## Production Discussion

Production clusters use GitOps for manifests, PDB/HPA for resilience, resource quotas, and image digests. Probes must match the real application contract — never copy `/healthz` blindly.

## Best Practices

- Always set requests/limits on demo workloads too
- Prefer `kubectl apply` of files over one-off patches for lasting fixes
- Watch Events sorted by time during incidents
- Use `rollout undo` when a change worsens availability

## Success Criteria

You restored Ready Pods from probe/image failures, verified HTTP 200, and archived evidence.

## Related Tutorials

- [Kubernetes](../kubernetes/index.md)
- [Health Checks — Probes](../kubernetes/health-checks-probes-and-self-healing.md)
- [Troubleshooting Kubernetes Workloads](../kubernetes/troubleshooting-kubernetes-workloads.md)
- Previous lab: [Docker Compose Stack Recovery](docker-compose-stack-recovery.md)
- Project: [Status API Portfolio Build](../projects/status-api-portfolio.md)

## References

1. [Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
2. [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
3. [Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)
