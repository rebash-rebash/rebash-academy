---
title: "Monitoring and Logging in Kubernetes"
description: "Observe clusters with Metrics Server, Prometheus, Grafana, kube-state-metrics, logging stacks, and Kubernetes Events."
difficulty: intermediate
estimated_time: "45–60 min"
technology: kubernetes
category: kubernetes
module: "Module 12 · Observability"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - kubernetes
  - prometheus
  - observability
prerequisites:
  - kubernetes/kubernetes-networking-deep-dive
next:
  - kubernetes/kubernetes-autoscaling
related:
  - monitoring/index
  - prometheus/index
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKA
tags:
  - kubernetes
  - prometheus
  - logging
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---


# Monitoring and Logging in Kubernetes

## Overview







Use Metrics Server for `kubectl top`, explain the Prometheus/Grafana path, and debug with Events and container logs.

**Metrics Server** → HPA resource metrics. **Prometheus** + **kube-state-metrics** → deep metrics. Logs: node agents (Fluent Bit) or cloud logging. Always start with `kubectl describe` Events.

This is a core tutorial in **Module 12 · Observability** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Kubernetes Networking Deep Dive](kubernetes-networking-deep-dive.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] `kubectl top nodes/pods` (if Metrics Server present)  
- [ ] Map Prometheus scrape targets  
- [ ] Use Events for failures  
- [ ] Stream Pod logs

## Architecture







This topic’s control points and relationships are shown below.

![Production observability](../assets/excalidraw/k8s-production-cluster.svg)

## Theory







### What it is

**Observability** on Kubernetes combines metrics, logs, and Events (plus traces in mature platforms). **Metrics Server** supplies resource metrics for `kubectl top` and resource-based **Horizontal Pod Autoscaler (HPA)**. **Prometheus** scrapes application and cluster targets; **kube-state-metrics** exposes object state as metrics; **Grafana** visualises. Logs ship via node agents (Fluent Bit, Fluentd) or cloud collectors. **Events** are the API’s short-lived narrative of scheduling and failures.

### Why it matters

You cannot operate what you cannot see. Autoscaling, capacity planning, and incident response depend on golden signals (latency, traffic, errors, saturation) and on Pod-level CPU/memory. Starting with Events and logs avoids premature dashboard archaeology.

### How it works (mental model)

1. Kubelet exposes summary metrics → Metrics Server aggregates → `kubectl top` / HPA.
2. Prometheus discovers targets (Service monitors, annotations, or scrape configs) and stores time series.
3. Containers write stdout/stderr → kubelet log files → agents forward to a store (Loki, Elasticsearch, cloud logging).
4. Controllers emit Events (`FailedScheduling`, `Pulled`, `Killing`) — read with `describe` / `get events`.
5. Alerts fire on PromQL (or cloud) rules; runbooks start from symptom → Events → logs → metrics.

Control loops still reconcile without Prometheus; observability tells *you* when reconciliation is unhealthy.

### Key concepts / comparisons

| Signal | Source |
|--------|--------|
| Resource metrics | Metrics Server / cAdvisor path |
| Cluster object metrics | kube-state-metrics |
| App metrics | `/metrics` scraped by Prometheus |
| Logs | Container stdout + agents |
| Events | Kubernetes API |

| Tool | Role |
|------|------|
| Metrics Server | Lightweight resource API |
| Prometheus + Grafana | Deep metrics & dashboards |
| Log stack | Searchable history |

### Common pitfalls

- Expecting `kubectl top` without Metrics Server installed.
- Using only node CPU graphs while apps OOM — watch working set and restarts.
- Log pipelines that drop crash logs — always keep `kubectl logs --previous` in the playbook.
- Cardinality explosions from high-unique label values in Prometheus.
- Treating Events as long-term audit — they are retained briefly; use audit logs for compliance.

## Hands-on Lab

### Objective

Deploy a logging workload, collect Events and container logs into evidence files, and attempt `kubectl top` with a documented fallback when Metrics Server is absent.

### Prerequisites

- kubectl configured against a lab cluster (kind or minikube)
- Writable workspace at `~/rebash-k8s/module-12`

### Lab environment

Workspace: `~/rebash-k8s/module-12` on a disposable lab cluster.

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-k8s/module-12 && cd ~/rebash-k8s/module-12
```

### Real-world scenario

During a production incident, the first questions are: *What did the Pod log?* and *What did the control plane record?* You will deploy a sample app that emits structured log lines, capture Events and logs, and check whether Metrics Server is installed for resource usage.

### Step-by-step tasks

#### Task 1 – Namespace and logging Deployment

Create `namespace.yaml`:

```yaml title="namespace.yaml"
apiVersion: v1
kind: Namespace
metadata:
  name: rebash-m12
```

Create `deployment.yaml`:

```yaml title="deployment.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: log-demo
  namespace: rebash-m12
spec:
  replicas: 1
  selector:
    matchLabels:
      app: log-demo
  template:
    metadata:
      labels:
        app: log-demo
    spec:
      containers:
        - name: logger
          image: busybox:1.36.1
          command:
            - sh
            - -c
            - |
              i=0
              while true; do
                i=$((i+1))
                echo "level=info msg=demo-tick count=$i ts=$(date -Iseconds)"
                sleep 5
              done
          resources:
            requests:
              cpu: 10m
              memory: 32Mi
```

Apply:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-k8s/module-12
kubectl apply -f namespace.yaml -f deployment.yaml
kubectl rollout status deployment/log-demo -n rebash-m12 --timeout=120s
kubectl get pods -n rebash-m12 -l app=log-demo | tee pods-m12.txt
```

!!! example "Expected output"
    `log-demo` Pod is Running.


#### Task 2 – Collect Events and logs

Create `collect-evidence.sh`:

```bash title="collect-evidence.sh"
#!/usr/bin/env bash
set -euo pipefail
NS="rebash-m12"
APP="log-demo"
OUT="${1:-.}"

kubectl get events -n "$NS" --sort-by=.lastTimestamp | tail -n 20 > "$OUT/events-m12.txt"
POD="$(kubectl get pod -n "$NS" -l app="$APP" -o jsonpath='{.items[0].metadata.name}')"
kubectl logs -n "$NS" "$POD" --tail=10 > "$OUT/logs-m12.txt"
kubectl describe pod -n "$NS" "$POD" > "$OUT/describe-m12.txt"
echo "wrote evidence to $OUT"
```

Run the script:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-k8s/module-12
chmod +x collect-evidence.sh
./collect-evidence.sh .
grep -q 'demo-tick' logs-m12.txt
grep -q 'log-demo' describe-m12.txt
```

!!! example "Expected output"
    `logs-m12.txt` contains `demo-tick` lines; `events-m12.txt` lists recent namespace Events.


#### Task 3 – Metrics Server check with fallback

Create `check-metrics.sh`:

```bash title="check-metrics.sh"
#!/usr/bin/env bash
set -euo pipefail
if kubectl top nodes >/dev/null 2>&1; then
  kubectl top nodes | tee metrics-nodes-m12.txt
  kubectl top pods -n rebash-m12 | tee metrics-pods-m12.txt
  echo "metrics-server: available"
else
  echo "metrics-server: not installed — install metrics-server for HPA and kubectl top" | tee metrics-fallback-m12.txt
  kubectl get deployment -n kube-system 2>/dev/null | grep -i metrics || true
fi
```

Run:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-k8s/module-12
chmod +x check-metrics.sh
./check-metrics.sh
test -s metrics-nodes-m12.txt || test -s metrics-fallback-m12.txt
```

!!! example "Expected output"
    Either node/pod usage tables, or `metrics-fallback-m12.txt` explaining Metrics Server is missing.


### Validation steps

- [ ] Deployment Pod is Ready and emitting log lines
- [ ] `collect-evidence.sh` produced logs, Events, and describe output
- [ ] Metrics check documented availability or fallback clearly
- [ ] You can explain difference between logs, Events, and metrics

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Empty logs | Pod not Ready yet | Wait for rollout; re-run script |
| `error: Metrics API not available` | No metrics-server | Document fallback; install for production |
| No Events | Very new namespace | Trigger rollout restart and re-fetch |
| Script permission denied | Missing execute bit | `chmod +x collect-evidence.sh` |

### Challenge exercise

Simulate a crash: change the container command to `exit 1`, re-apply, then capture `kubectl logs --previous` into `logs-previous-m12.txt`.

### Learning outcomes

- Deployed a workload that produces observable log output
- Automated collection of logs, Events, and describe evidence
- Checked Metrics Server availability with an honest fallback path
- Built an incident triage habit: logs + Events + metrics

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
kubectl delete namespace rebash-m12 --ignore-not-found
```

## Validation







- [ ] Lab commands run under `~/rebash-k8s/module-12/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Monitoring and Logging in Kubernetes** always combines:

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







!!! warning "Expecting `kubectl top` without Metrics Server installed."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Using only node CPU graphs while apps OOM — watch working set and restarts."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Monitoring and Logging in Kubernetes changes as code and review them in pull requests
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







**Monitoring and Logging in Kubernetes** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions






1. Where do container logs go by default on a node?
2. How does `kubectl logs` retrieve application output?
3. What cluster components are needed for `kubectl top` to work?
4. What privacy and security concerns apply to centralised log pipelines?
5. How would you alert on CrashLoopBackOff versus high latency?

!!! tip "Sample answer — question 2"
    kubectl logs reads the container runtime log stream for a Pod/container via the API server and kubelet. It shows stdout/stderr, not arbitrary files inside the filesystem unless you exec.

!!! tip "Sample answer — question 4"
    Logs may contain secrets, personal data, or tokens. Scrub sensitive fields, encrypt in transit and at rest, restrict access, and set retention aligned with compliance.

## Related Tutorials







- [Course overview](index.md)
- [Kubernetes Autoscaling](kubernetes-autoscaling.md)

## References







- [Metrics Server](https://github.com/kubernetes-sigs/metrics-server) · [Prometheus on K8s](https://prometheus.io/docs/prometheus/latest/getting_started/)
