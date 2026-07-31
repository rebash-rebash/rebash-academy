---
title: "Pods — The Atomic Unit"
description: "Create and understand Pods — containers, probes basics, resource requests, and why controllers own Pods in production."
difficulty: intermediate
estimated_time: "40–55 min"
technology: kubernetes
category: kubernetes
module: "Module 3 · Kubernetes Objects"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
skills:
  - kubernetes
  - pods
prerequisites:
  - kubernetes/kubectl-essentials-and-workflows
next:
  - kubernetes/kubernetes-objects-labels-and-namespaces
related:
  - kubernetes/health-checks-probes-and-self-healing
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKAD
tags:
  - kubernetes
  - pods
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Pods — The Atomic Unit

## Overview

Deploy a Pod with resource requests, understand lifecycle phases, and know why bare Pods are rare in production.

A **Pod** is one or more containers sharing network/storage namespaces. Controllers (Deployments) recreate Pods; bare Pods do not self-heal on node loss.

This is a core tutorial in **Module 3 · Kubernetes Objects** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [kubectl Essentials](kubectl-essentials-and-workflows.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Write a Pod manifest  
- [ ] Explain Pending → Running → Succeeded/Failed  
- [ ] Set requests/limits  
- [ ] Prefer Deployments for apps

## Architecture

This topic’s control points and relationships are shown below.

![Pod lifecycle](../assets/excalidraw/k8s-pod-lifecycle.svg)

## Theory

### What it is

A **Pod** is the smallest deployable object in Kubernetes: one or more containers that share a network namespace (same Pod IP and `localhost`) and optional shared volumes. Containers inside a Pod are co-scheduled onto the same node. Applications almost always run as a single main container plus optional sidecars (proxy, log shipper).

### Why it matters

Everything else — Deployments, Services, Jobs — ultimately creates or selects Pods. If you misunderstand Pod lifecycle, resource requests, or why bare Pods are fragile, later modules feel like magic. Production systems rarely create Pods by hand; controllers own them so lost nodes and crashed containers recover automatically.

### How it works (mental model)

1. A Pod object appears in the API (created by you or a controller).
2. While **Pending**, the scheduler finds a node that fits resources and constraints; kubelet pulls images.
3. Containers start → Pod becomes **Running** (if at least the required containers are up).
4. On success for batch work → **Succeeded**; on unrecoverable failure → **Failed**; communication loss → **Unknown**.
5. When a controller-owned Pod dies, the controller creates a replacement. A bare Pod deleted with its node is gone.

Resource **requests** influence scheduling; **limits** cap usage. Probes (liveness, readiness, startup) are covered in related depth — set readiness before Services send traffic.

### Key concepts / comparisons

| Phase | Meaning |
|-------|---------|
| Pending | Accepted, not yet fully running (schedule/pull) |
| Running | Bound to a node; containers active |
| Succeeded / Failed | Terminal for run-to-completion Pods |
| Unknown | Node status unclear |

| Approach | Use |
|----------|-----|
| Bare Pod | Labs, one-off debug |
| Deployment-owned Pod | Stateless apps (default) |
| Multi-container Pod | Tightly coupled sidecars |

### Common pitfalls

- Running production apps as bare Pods — no replica repair on node failure.
- Omitting CPU/memory requests — noisy neighbours and surprise Pending states.
- Assuming containers in different Pods share `localhost` — they do not; use Services.
- Putting tightly coupled processes in separate Pods when they need shared volumes or localhost.
- Ignoring `describe` Events when stuck in Pending (image pull, taints, PVC).

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-03 && cd ~/rebash-k8s/module-03
```

**Focus:** hands-on practice for Pods — The Atomic Unit

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Pods — The Atomic Unit"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-k8s/module-03 && cd ~/rebash-k8s/module-03
cat > pod.yaml << 'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: rebash-pod
  labels:
    app: rebash
spec:
  containers:
    - name: web
      image: nginx:alpine
      ports:
        - containerPort: 80
      resources:
        requests:
          cpu: 50m
          memory: 64Mi
        limits:
          memory: 128Mi
EOF
kubectl apply -f pod.yaml
kubectl get pod rebash-pod -w &
sleep 3; kill %1 2>/dev/null || true
kubectl describe pod rebash-pod | sed -n '/Events/,$p' | head -n 20
kubectl delete -f pod.yaml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-kubernetes/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-k8s/module-03/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Pods — The Atomic Unit** always combines:

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

!!! warning "Running production apps as bare Pods — no replica repair on node failure."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Omitting CPU/memory requests — noisy neighbours and surprise Pending states."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Pods — The Atomic Unit changes as code and review them in pull requests
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

**Pods — The Atomic Unit** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Pods — The Atomic Unit** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Labels, Selectors, and Namespaces](kubernetes-objects-labels-and-namespaces.md)

## References

- [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
