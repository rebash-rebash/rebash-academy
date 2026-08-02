---
title: "Resource Quotas and LimitRanges"
description: "Enforce namespace ResourceQuotas and LimitRanges so multi-tenant Kubernetes clusters stay fair and safe."
difficulty: intermediate
estimated_time: "35–50 min"
technology: kubernetes
category: kubernetes
module: "Module 8 · Configuration"
career_paths:
  - kubernetes-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - kubernetes
  - resource-quotas
prerequisites:
  - kubernetes/configmaps-and-secrets
next:
  - kubernetes/kubernetes-scheduling
related:
  - kubernetes/namespaces-and-resource-management
  - kubernetes/platform-engineering-on-kubernetes
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKA
tags:
  - kubernetes
  - quota
  - limitrange
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Resource Quotas and LimitRanges

## Overview







Apply a namespace ResourceQuota and LimitRange so Pods cannot starve the cluster or run without requests.

**ResourceQuota** caps aggregate usage in a namespace. **LimitRange** sets default/min/max per container. Together they enable soft multi-tenancy.

This is a core tutorial in **Module 8 · Configuration** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [ConfigMaps and Secrets](configmaps-and-secrets.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Create ResourceQuota  
- [ ] Create LimitRange defaults  
- [ ] See admission reject over-quota creates

## Architecture







This topic’s control points and relationships are shown below.

![Architecture](../assets/excalidraw/k8s-architecture.svg)

## Theory







### What it is

**ResourceQuota** sets aggregate ceilings for a namespace — total CPU, memory, object counts (Pods, Services, PVCs), and sometimes hugepages or ephemeral storage. **LimitRange** constrains or defaults resources on individual containers/Pods (min, max, default request/limit, max ratio). Together they implement fair sharing and guardrails for multi-team clusters.

### Why it matters

Without quotas, one noisy namespace can schedule enough Pods to starve everyone else. Without LimitRanges, Pods with no requests are hard to schedule fairly and may burst unbounded. Platform and SRE teams rely on these objects for soft multi-tenancy before stronger isolation (separate clusters, vCluster, etc.).

### How it works (mental model)

1. Create a namespace for a team or environment.
2. Apply a ResourceQuota — admission tracks usage against the caps.
3. Apply a LimitRange — when users omit requests/limits, defaults are injected; invalid sizes are rejected.
4. On `create`/`update`, the API server admission plugin checks quota; over-budget requests fail immediately with a clear error.
5. Controllers still reconcile inside the budget; scale-ups that would exceed quota fail until capacity frees.

Quotas count **requests** (and sometimes limits, depending on the resource name). Design requests thoughtfully.

### Key concepts / comparisons

| Object | Scope | Effect |
|--------|-------|--------|
| ResourceQuota | Namespace aggregate | Caps total usage / counts |
| LimitRange | Per Pod/container | Defaults and bounds |

| Example resource name | Meaning |
|-----------------------|---------|
| `requests.cpu` | Sum of CPU requests |
| `limits.memory` | Sum of memory limits |
| `pods` | Number of Pods |

### Common pitfalls

- Quota on `requests.cpu` while teams set only limits — usage accounting surprises.
- LimitRange defaults that are too large — few Pods fit under the quota.
- Forgetting that system DaemonSets in other namespaces are unaffected; focus on app namespaces.
- Expecting quotas to stop runtime CPU spikes alone — they govern scheduling admission, not CFS throttling by themselves.
- Creating quotas in `kube-system` accidentally and breaking cluster components.

## Hands-on Lab



### Objective

Build and verify a working Kubernetes solution for **Resource Quotas and LimitRanges** that you can inspect, prove, and tear down safely.

### Prerequisites

- kubectl configured against a lab cluster (kind/minikube preferred)
- Cluster-admin or namespace-create rights in the lab cluster
- Writable workspace at `~/rebash-k8s/module-08-quota`

### Lab environment

Workspace: `~/rebash-k8s/module-08-quota`

Local kind/minikube or a dedicated sandbox cluster. Never target a shared production API server.

```bash
mkdir -p ~/rebash-k8s/module-08-quota && cd ~/rebash-k8s/module-08-quota
```

### Real-world scenario

Your platform team is rolling out **Resource Quotas and LimitRanges** for a new microservice. You must apply the change in an isolated namespace, prove it works with kubectl, and leave evidence for the on-call handover.

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

- Applied a real cluster change for Resource Quotas and LimitRanges
- Used describe/Events for verification
- Destroyed lab resources cleanly

### Cleanup

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Keep ~/rebash-kubernetes/ for later tutorials
```

## Validation







- [ ] Lab commands run under `~/rebash-k8s/module-08-quota/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Resource Quotas and LimitRanges** always combines:

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







!!! warning "Quota on `requests.cpu` while teams set only limits — usage accounting surprises."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "LimitRange defaults that are too large — few Pods fit under the quota."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Resource Quotas and LimitRanges changes as code and review them in pull requests
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







**Resource Quotas and LimitRanges** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions






1. What fields commonly appear under ResourceQuota hard limits?
2. How does LimitRange set defaults differently from forcing every manifest to declare resources?
3. Can a LimitRange max block a Pod that a quota would otherwise allow?
4. How do memory limits interact with OOMKilled behaviour?
5. What governance process should surround quota changes?

!!! tip "Sample answer — question 2"
    LimitRange can inject default request/limit values at admission, reducing boilerplate while still enforcing maxima. Teams can override within allowed bounds.

!!! tip "Sample answer — question 4"
    Exceeding a memory limit triggers OOMKill of the container. Set limits from observed usage plus headroom; too low causes restarts, too high wastes node capacity.

## Related Tutorials







- [Course overview](index.md)
- [Kubernetes Scheduling](kubernetes-scheduling.md)

## References







- [Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
