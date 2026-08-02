---
title: "Kubernetes Scheduling"
description: "Control Pod placement with nodeSelectors, affinity, anti-affinity, taints, tolerations, and topology spread constraints."
difficulty: advanced
estimated_time: "45–60 min"
technology: kubernetes
category: kubernetes
module: "Module 9 · Scheduling"
career_paths:
  - kubernetes-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - kubernetes
  - scheduling
  - affinity
prerequisites:
  - kubernetes/resource-quotas-and-limit-ranges
next:
  - kubernetes/rbac-and-kubernetes-security-basics
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
  - affinity
  - taints
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Kubernetes Scheduling

## Overview









Place Pods intentionally using nodeSelector, affinity/anti-affinity, taints/tolerations, and topology spread — and diagnose Pending schedule failures.

The **scheduler** binds Pods to nodes that satisfy predicates (resources, affinity, taints). Pending + `FailedScheduling` events mean constraints or capacity.

This is a core tutorial in **Module 9 · Scheduling** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites









- [Resource Quotas and LimitRanges](resource-quotas-and-limit-ranges.md)

## Learning Objectives









By the end of this tutorial, you will be able to:

- [ ] Use nodeSelector / node affinity  
- [ ] Spread replicas with pod anti-affinity or topologySpread  
- [ ] Taint a node and tolerate it  
- [ ] Read scheduling events

## Architecture









This topic’s control points and relationships are shown below.

![Architecture](../assets/excalidraw/k8s-architecture.svg)

## Theory









### What it is

**Scheduling** is how the control plane chooses a node for each Pod. The **kube-scheduler** filters nodes that cannot run the Pod (resources, taints, affinity, volume constraints), scores the remainder, and binds the winner. You influence placement with **nodeSelector**, **node/pod affinity**, **taints and tolerations**, and **topology spread constraints**.

### Why it matters

Default scheduling spreads work opportunistically. Production needs intentional placement: GPUs only on labelled nodes, replicas across zones, batch jobs on spot pools, and system agents on tainted control planes. Pending Pods with `FailedScheduling` events are among the most common tickets — reading them correctly saves hours.

### How it works (mental model)

1. Pod created without `nodeName` → enters scheduling queue.
2. **Predicates / filters**: enough CPU/memory, match selectors, tolerate taints, volume zone limits.
3. **Priorities / scores**: prefer balanced nodes, honour soft affinity and spread.
4. Bind Pod to a node; kubelet admits and starts it.
5. If no node fits, Pod stays **Pending**; Events explain the reason.

Taints repel Pods unless they **tolerate** the taint. Affinity attracts Pods to nodes or to/away from other Pods.

### Key concepts / comparisons

| Mechanism | Purpose |
|-----------|---------|
| nodeSelector | Simple label match |
| Node affinity | Required/preferred node rules |
| Pod affinity / anti-affinity | Co-locate or separate Pods |
| Taints / tolerations | Reserve nodes / allow exceptions |
| topologySpreadConstraints | Even spread across zones/hosts |

| Hard rule | Soft rule |
|-----------|-----------|
| `requiredDuringScheduling…` | `preferredDuringScheduling…` |
| Must satisfy or Pending | Best-effort scoring |

### Common pitfalls

- Required anti-affinity on a single-node lab — permanent Pending.
- Labelling nodes inconsistently (`disk=ssd` vs `disk-type=ssd`).
- Tainting all nodes without matching tolerations on workloads.
- Ignoring PVC zone constraints when using regional disks.
- Overusing affinity until the scheduler has no legal packing — always check Events.

## Hands-on Lab



### Objective

Build and verify a working Kubernetes solution for **Kubernetes Scheduling** that you can inspect, prove, and tear down safely.

### Prerequisites

- kubectl configured against a lab cluster (kind/minikube preferred)
- Cluster-admin or namespace-create rights in the lab cluster
- Writable workspace at `~/rebash-k8s/module-09`

### Lab environment

Workspace: `~/rebash-k8s/module-09`

Local kind/minikube or a dedicated sandbox cluster. Never target a shared production API server.

```bash
mkdir -p ~/rebash-k8s/module-09 && cd ~/rebash-k8s/module-09
```

### Real-world scenario

Your platform team is rolling out **Kubernetes Scheduling** for a new microservice. You must apply the change in an isolated namespace, prove it works with kubectl, and leave evidence for the on-call handover.

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

- Applied a real cluster change for Kubernetes Scheduling
- Used describe/Events for verification
- Destroyed lab resources cleanly

### Cleanup

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Keep ~/rebash-kubernetes/ for later tutorials
```

## Validation









- [ ] Lab commands run under `~/rebash-k8s/module-09/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough









Production practice for **Kubernetes Scheduling** always combines:

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









!!! warning "Required anti-affinity on a single-node lab — permanent Pending."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Labelling nodes inconsistently (`disk=ssd` vs `disk-type=ssd`)."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices









- Encode Kubernetes Scheduling changes as code and review them in pull requests
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









**Kubernetes Scheduling** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions








1. What inputs does the kube-scheduler consider when placing a Pod?
2. What is the difference between nodeSelector and node affinity?
3. When would you use taints and tolerations?
4. How can poor affinity rules reduce utilisation or availability?
5. What does Pending with FailedScheduling usually indicate?

!!! tip "Sample answer — question 2"
    nodeSelector is a simple required label match. Node affinity supports required/preferred rules and richer operators, giving more expressive placement control.

!!! tip "Sample answer — question 4"
    Overly strict anti-affinity or scarce node labels can leave Pods Pending or pack unevenly. Preferred rules soften constraints; required rules must match capacity planning.

## Related Tutorials









- [Course overview](index.md)
- [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md)

## References









- [Assigning Pods to nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
