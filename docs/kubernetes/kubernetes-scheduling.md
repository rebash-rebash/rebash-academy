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

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-09 && cd ~/rebash-k8s/module-09
```

**Focus:** hands-on practice for Kubernetes Scheduling

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-k8s/module-09 && cd ~/rebash-k8s/module-09
NODE=$(kubectl get nodes -o jsonpath='{.items[0].metadata.name}')
kubectl label node "$NODE" disk=ssd --overwrite
cat > affinity.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rebash-sched
spec:
  replicas: 2
  selector:
    matchLabels: { app: rebash-sched }
  template:
    metadata:
      labels: { app: rebash-sched }
    spec:
      nodeSelector: { disk: ssd }
      containers:
        - name: app
          image: nginx:alpine
          resources:
            requests: { cpu: 50m, memory: 64Mi }
EOF
kubectl apply -f affinity.yaml
kubectl get pods -l app=rebash-sched -o wide
kubectl describe pod -l app=rebash-sched | sed -n '/Events/,$p' | head -n 15
kubectl delete -f affinity.yaml
kubectl label node "$NODE" disk-
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-kubernetes/ for later tutorials; destroy disposable cloud resources from this lab
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

1. How does **Kubernetes Scheduling** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md)

## References

- [Assigning Pods to nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
