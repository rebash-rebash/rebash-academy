---
title: "Kubernetes Autoscaling"
description: "Configure HPA, understand VPA, Cluster Autoscaler, and KEDA for scaling workloads and nodes in production Kubernetes."
difficulty: advanced
estimated_time: "45–60 min"
technology: kubernetes
category: kubernetes
module: "Module 13 · Autoscaling"
career_paths:
  - kubernetes-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - kubernetes
  - hpa
  - autoscaling
prerequisites:
  - kubernetes/monitoring-and-logging-in-kubernetes
  - kubernetes/deployments-managing-replicated-pods
next:
  - kubernetes/helm-package-management
related:
  - kubernetes/production-patterns-hpa-pdb-and-affinity
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKA
  - CKAD
tags:
  - kubernetes
  - hpa
  - keda
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Kubernetes Autoscaling

## Overview









Create a Horizontal Pod Autoscaler (HPA) on CPU and explain VPA, Cluster Autoscaler, and KEDA event-driven scaling.

| Scaler | Scales |
|--------|--------|
| HPA | Pod replicas (CPU/mem/custom) |
| VPA | Pod resource requests |
| Cluster Autoscaler | Nodes |
| KEDA | Replicas from events/queues |

Requests must be set for resource-based HPA. Pair with PodDisruptionBudgets in production.

This is a core tutorial in **Module 13 · Autoscaling** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites









- [Observability](monitoring-and-logging-in-kubernetes.md) (Metrics Server for resource HPA)

## Learning Objectives









By the end of this tutorial, you will be able to:

- [ ] Create an HPA on CPU  
- [ ] Explain why resource requests are required  
- [ ] Contrast HPA, VPA, Cluster Autoscaler, and KEDA  
- [ ] Note PDB pairing for production scale-down

## Architecture









This topic’s control points and relationships are shown below.

![Architecture](../assets/excalidraw/k8s-architecture.svg)

## Theory









### What it is

**Autoscaling** adjusts capacity to load. **Horizontal Pod Autoscaler (HPA)** changes replica counts from CPU, memory, or custom metrics. **Vertical Pod Autoscaler (VPA)** recommends or sets container requests/limits. **Cluster Autoscaler** (or cloud equivalents / Karpenter) adds or removes nodes when Pods are unschedulable or nodes are underused. **KEDA** scales from event sources (queues, lag, cron).

### Why it matters

Fixed replica counts waste money at night and melt under spikes. Autoscaling ties capacity to demand, but only if metrics exist and requests are honest. Misconfigured HPA either never scales or flaps. Production pairs scaling with **Pod Disruption Budgets (PDBs)** so voluntary drains and scale-down stay safe.

### How it works (mental model)

1. Metrics Server (or custom metrics API / Prometheus adapter) publishes signals.
2. HPA controller computes desired replicas from target utilisation or metric value.
3. It updates the Deployment/ReplicaSet/StatefulSet scale subresource.
4. If Pods stay Pending for lack of node capacity, Cluster Autoscaler / Karpenter provisions nodes.
5. Scale-down waits for stabilisation windows; PDBs limit simultaneous voluntary evictions.

Controllers reconcile desired replica counts continuously — HPA writes the desired number; the workload controller creates Pods.

### Key concepts / comparisons

| Scaler | Scales |
|--------|--------|
| HPA | Pod replicas (CPU/mem/custom) |
| VPA | Pod resource requests |
| Cluster Autoscaler | Nodes |
| KEDA | Replicas from events/queues |

| Requirement | Why |
|-------------|-----|
| Resource requests | HPA CPU/memory % needs a denominator |
| Metrics Server | Resource metrics path |
| Custom metrics API | Non-resource signals |

Avoid running VPA auto mode and HPA on CPU/memory against the same container without understanding interactions — use documented patterns.

### Common pitfalls

- HPA with no requests — utilisation is undefined or useless.
- Min=max replicas — “autoscaler” that never moves.
- Scaling on CPU when the app is queue-bound — use KEDA or custom metrics.
- Cluster Autoscaler disabled while HPA creates unschedulable Pods.
- Aggressive scale-down without PDBs during deploys — accidental outages.

## Hands-on Lab



### Objective

Build and verify a working Kubernetes solution for **Kubernetes Autoscaling** that you can inspect, prove, and tear down safely.

### Prerequisites

- kubectl configured against a lab cluster (kind/minikube preferred)
- Cluster-admin or namespace-create rights in the lab cluster
- Writable workspace at `~/rebash-k8s/module-13`

### Lab environment

Workspace: `~/rebash-k8s/module-13`

Local kind/minikube or a dedicated sandbox cluster. Never target a shared production API server.

```bash
mkdir -p ~/rebash-k8s/module-13 && cd ~/rebash-k8s/module-13
```

### Real-world scenario

Your platform team is rolling out **Kubernetes Autoscaling** for a new microservice. You must apply the change in an isolated namespace, prove it works with kubectl, and leave evidence for the on-call handover.

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

- Applied a real cluster change for Kubernetes Autoscaling
- Used describe/Events for verification
- Destroyed lab resources cleanly

### Cleanup

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Keep ~/rebash-kubernetes/ for later tutorials
```

## Validation









- [ ] Lab commands run under `~/rebash-k8s/module-13/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough









Production practice for **Kubernetes Autoscaling** always combines:

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









!!! warning "HPA with no requests — utilisation is undefined or useless."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Min=max replicas — “autoscaler” that never moves."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices









- Encode Kubernetes Autoscaling changes as code and review them in pull requests
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









**Kubernetes Autoscaling** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions








1. What does the Horizontal Pod Autoscaler adjust?
2. Why do resource requests matter for CPU-based HPA?
3. What is the difference between HPA and Cluster Autoscaler?
4. What risks arise from autoscaling without PodDisruptionBudgets and readiness probes?
5. When would you choose custom metrics over CPU utilisation?

!!! tip "Sample answer — question 2"
    HPA scales Pod replica counts from metrics. Requests define the baseline for utilisation percentages; without requests, CPU targets are unreliable or unavailable.

!!! tip "Sample answer — question 4"
    Rapid scale-down can terminate Pods mid-request if PDBs and readiness are weak. Scale-up can overwhelm dependencies. Pair HPA with sensible limits, PDBs, and dependency capacity planning.

## Related Tutorials









- [Course overview](index.md)
- [Helm Package Management](helm-package-management.md)

## References









- [Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) · [KEDA](https://keda.sh/)
