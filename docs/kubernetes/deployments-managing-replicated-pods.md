---
title: "Deployments — Managing Replicated Pods"
description: "Manage Deployments — scaling, rolling updates, rollbacks, and rollout strategy for production DevOps workloads."
difficulty: intermediate
estimated_time: "45–60 min"
technology: kubernetes
category: kubernetes
module: "Module 4 · Workload Management"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - kubernetes
  - deployments
prerequisites:
  - kubernetes/kubernetes-objects-labels-and-namespaces
next:
  - kubernetes/workload-controllers-statefulset-daemonset-jobs
related:
  - kubernetes/health-checks-probes-and-self-healing
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKAD
  - CKA
tags:
  - kubernetes
  - deployments
  - rollout
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Deployments — Managing Replicated Pods

## Overview

Create a Deployment, scale it, perform a rolling update, and roll back when a bad image ships.

A **Deployment** owns ReplicaSets and provides declarative updates. Default strategy is RollingUpdate — control `maxUnavailable` / `maxSurge`.

This is a core tutorial in **Module 4 · Workload Management** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Labels, Selectors, and Namespaces](kubernetes-objects-labels-and-namespaces.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Write a Deployment manifest  
- [ ] Scale replicas  
- [ ] Roll out a new image  
- [ ] `rollout undo` / history

## Architecture

This topic’s control points and relationships are shown below.

![Pod lifecycle](../assets/excalidraw/k8s-pod-lifecycle.svg)

## Theory

### What it is

A **Deployment** is the standard controller for **stateless** replicated applications. You declare a pod template and a replica count; the Deployment owns one or more **ReplicaSets** and performs **rolling updates** (or recreate) when the template changes. Scaling, pause/resume, and rollback are first-class operations.

### Why it matters

Bare Pods and hand-managed ReplicaSets do not give you safe image rollouts. Deployments let DevOps ship new versions with controlled surge and unavailability, then undo quickly when a bad image lands. Almost every web API and frontend in Kubernetes sits behind a Deployment (often plus HPA later).

### How it works (mental model)

1. You set `spec.replicas` and `spec.template` (containers, labels, probes, resources).
2. The Deployment controller ensures a ReplicaSet matches the current template.
3. On template change, a new ReplicaSet scales up while the old one scales down (**RollingUpdate**), governed by `maxSurge` and `maxUnavailable`.
4. Pod readiness gates traffic: not-ready Pods leave Service endpoints so users avoid half-started containers.
5. `kubectl rollout undo` moves desired state back to a previous ReplicaSet revision.

Controllers reconcile continuously: if a Pod is deleted, the ReplicaSet creates another until the count matches.

### Key concepts / comparisons

| Strategy | Behaviour |
|----------|-----------|
| RollingUpdate | Gradual replace (default) |
| Recreate | Kill all, then create new (downtime) |

| Concept | Role |
|---------|------|
| Deployment | Declarative updates + scale |
| ReplicaSet | Maintain identical Pod count |
| Revision history | Enables rollback |

Prefer changing the image via the Deployment (`set image` or edit YAML + apply), not by editing live Pods.

### Common pitfalls

- Selectors that do not match the pod template labels — create fails or orphans Pods.
- `maxUnavailable: 1` with a single replica and no surge — brief outages during rollout.
- Shipping without readiness probes — broken Pods receive traffic mid-rollout.
- Expecting in-place container upgrades; Pods are replaced, not mutated in place.
- Forgetting `rollout status` in CI — pipelines proceed before the new revision is healthy.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-04 && cd ~/rebash-k8s/module-04
```

**Focus:** hands-on practice for Deployments — Managing Replicated Pods

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Deployments — Managing Replicated Pods"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-k8s/module-04 && cd ~/rebash-k8s/module-04
cat > deploy.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rebash-api
spec:
  replicas: 2
  selector:
    matchLabels: { app: rebash-api }
  strategy:
    type: RollingUpdate
    rollingUpdate: { maxUnavailable: 0, maxSurge: 1 }
  template:
    metadata:
      labels: { app: rebash-api }
    spec:
      containers:
        - name: api
          image: nginx:1.25-alpine
          ports: [{ containerPort: 80 }]
EOF
kubectl apply -f deploy.yaml
kubectl scale deploy/rebash-api --replicas=3
kubectl set image deploy/rebash-api api=nginx:1.26-alpine
kubectl rollout status deploy/rebash-api
kubectl rollout history deploy/rebash-api
kubectl rollout undo deploy/rebash-api
kubectl delete -f deploy.yaml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-kubernetes/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-k8s/module-04/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Deployments — Managing Replicated Pods** always combines:

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

!!! warning "Selectors that do not match the pod template labels — create fails or orphans Pods."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "`maxUnavailable: 1` with a single replica and no surge — brief outages during rollout."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Deployments — Managing Replicated Pods changes as code and review them in pull requests
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

**Deployments — Managing Replicated Pods** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Deployments — Managing Replicated Pods** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Workload Controllers — StatefulSet, DaemonSet, Jobs](workload-controllers-statefulset-daemonset-jobs.md)

## References

- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
