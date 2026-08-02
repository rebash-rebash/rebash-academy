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
last_updated: "2026-07-31"
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

Build and verify a working Kubernetes solution for **Monitoring and Logging in Kubernetes** that you can inspect, prove, and tear down safely.

### Prerequisites

- kubectl configured against a lab cluster (kind/minikube preferred)
- Cluster-admin or namespace-create rights in the lab cluster
- Writable workspace at `~/rebash-k8s/module-12`

### Lab environment

Workspace: `~/rebash-k8s/module-12`

Local kind/minikube or a dedicated sandbox cluster. Never target a shared production API server.

```bash
mkdir -p ~/rebash-k8s/module-12 && cd ~/rebash-k8s/module-12
```

### Real-world scenario

Your platform team is rolling out **Monitoring and Logging in Kubernetes** for a new microservice. You must apply the change in an isolated namespace, prove it works with kubectl, and leave evidence for the on-call handover.

### Step-by-step tasks

#### Task 1 – Apply a topic workload

Create a namespace and a small Deployment to practise **What it is** against a live API.

```bash
kubectl create namespace rebash-lab --dry-run=client -o yaml | kubectl apply -f -
kubectl create deployment topic --image=nginx:1.27-alpine -n rebash-lab
kubectl rollout status deployment/topic -n rebash-lab
kubectl get all -n rebash-lab
```

**Expected output:** Deployment Ready; Pods listed under the namespace.

#### Task 2 – Inspect and gather evidence

Production changes always leave an audit trail of describe/Events.

```bash
kubectl describe deploy topic -n rebash-lab | tee describe.txt
kubectl get events -n rebash-lab --sort-by=.lastTimestamp | tail -n 15 | tee events.txt
```

**Expected output:** describe.txt and events.txt capture healthy Objects/Events.

### Validation steps

- [ ] Namespace `rebash-lab` contains the expected Ready objects
- [ ] You can explain each Task command from the Theory section
- [ ] Cleanup deletes the namespace without leftover workloads

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| ImagePullBackOff | Wrong tag or registry auth | Fix image reference; check pull secrets |
| Pending Pod | Scheduling / quota / PVC | `kubectl describe pod` and read Events |
| Empty Endpoints | Selector or readiness mismatch | Compare Service selector to Pod labels and Ready |

### Challenge exercise

Add a readinessProbe and a ResourceQuota to the namespace, then show that over-quota creates are rejected.

### Learning outcomes

- Applied a real cluster change for Monitoring and Logging in Kubernetes
- Used describe/Events for verification
- Destroyed lab resources cleanly

### Cleanup

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Keep ~/rebash-kubernetes/ for later tutorials
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
