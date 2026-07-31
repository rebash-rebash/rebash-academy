---
title: "kubectl Essentials and Workflows"
description: "Use kubectl for day-to-day DevOps — get, describe, apply, logs, exec, port-forward, and safe declarative workflows."
difficulty: intermediate
estimated_time: "40–55 min"
technology: kubernetes
category: kubernetes
module: "Module 2 · Cluster Setup"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - kubernetes
  - kubectl
prerequisites:
  - kubernetes/installing-kubernetes-and-kubectl
next:
  - kubernetes/pods-the-atomic-unit
related:
  - kubernetes/troubleshooting-kubernetes-workloads
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKAD
  - CKA
tags:
  - kubernetes
  - kubectl
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# kubectl Essentials and Workflows

## Overview

Operate a cluster with declarative `kubectl apply`, inspect objects, stream logs, and exec for debugging — without guessing flags under pressure.

Prefer **apply** + Git over imperative create for anything lasting. Imperative commands are fine for labs and break-glass.

This is a core tutorial in **Module 2 · Cluster Setup** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- Working cluster from [Installing Kubernetes](installing-kubernetes-and-kubectl.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] `get`, `describe`, `apply`, `delete`  
- [ ] `logs`, `exec`, `port-forward`  
- [ ] Use `-n` / contexts safely  
- [ ] Dry-run client/server

## Architecture

This topic’s control points and relationships are shown below.

![Control plane path](../assets/excalidraw/k8s-control-plane.svg)

## Theory

### What it is

**kubectl** is how DevOps engineers inspect and change cluster state day to day. It speaks the Kubernetes API: create or update objects, read status, stream logs, open a shell in a container, and forward ports for local debugging. Mastery is less about memorising every flag and more about a reliable workflow under pressure.

### Why it matters

Incidents are won by disciplined inspection: Events before guesswork, `describe` before delete-and-recreate, declarative **apply** before snowflake imperative edits. Teams that standardise on Git + `kubectl apply` (or GitOps) reduce configuration drift. Imperative commands remain useful for labs and break-glass fixes.

### How it works (mental model)

Prefer a loop:

1. **Orient** — `kubectl config current-context`, `kubectl get ns`, confirm the right place.
2. **List** — `get` with labels and namespaces (`-n`, `-A`, `-l`).
3. **Explain** — `describe` for Events and conditions; `get -o yaml` for full object.
4. **Change** — edit manifests, `apply -f`, watch rollout; use `--dry-run=client|server` to preview.
5. **Observe** — `logs`, `exec`, `port-forward` for live behaviour.

Server-side apply and field managers matter in advanced teams; for this course, treat apply as “merge this desired state into the API”.

### Key concepts / comparisons

| Task | Command pattern |
|------|-----------------|
| List | `kubectl get pods -A` |
| Detail | `kubectl describe pod NAME` |
| Apply | `kubectl apply -f app.yaml` |
| Logs | `kubectl logs deploy/NAME -f` |
| Shell | `kubectl exec -it POD -- sh` |
| Local port | `kubectl port-forward svc/NAME 8080:80` |
| Preview | `kubectl apply --dry-run=server -f app.yaml` |

| Style | When |
|-------|------|
| Declarative (`apply -f`) | Anything that should last |
| Imperative (`create`, `run`, `expose`) | Labs, exploration, emergencies |

### Common pitfalls

- Forgetting `-n` and operating in `default` while the app lives elsewhere.
- Using `kubectl edit` on live objects with no Git record — drift accumulates.
- Relying on `logs` alone; CrashLoop often needs `logs --previous` and Events.
- `port-forward` is a debug tunnel, not a production exposure path.
- Running `delete` without confirming selectors — label mistakes wipe the wrong workloads.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-02-kubectl && cd ~/rebash-k8s/module-02-kubectl
```

**Focus:** hands-on practice for kubectl Essentials and Workflows

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: kubectl Essentials and Workflows"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-k8s/module-02-kubectl && cd ~/rebash-k8s/module-02-kubectl
kubectl create deployment rebash-web --image=nginx:alpine --dry-run=client -o yaml > deploy.yaml
kubectl apply -f deploy.yaml
kubectl rollout status deploy/rebash-web
kubectl get pods -l app=rebash-web -o wide
kubectl expose deploy/rebash-web --port=80 --target-port=80 --name=rebash-web
kubectl port-forward svc/rebash-web 8080:80 &
sleep 1; curl -sI http://127.0.0.1:8080 | head -n 3
kill %1 2>/dev/null || true
kubectl delete -f deploy.yaml
kubectl delete svc rebash-web --ignore-not-found
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-kubernetes/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-k8s/module-02-kubectl/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **kubectl Essentials and Workflows** always combines:

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

!!! warning "Forgetting `-n` and operating in `default` while the app lives elsewhere."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Using `kubectl edit` on live objects with no Git record — drift accumulates."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode kubectl Essentials and Workflows changes as code and review them in pull requests
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

**kubectl Essentials and Workflows** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **kubectl Essentials and Workflows** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Pods — The Atomic Unit](pods-the-atomic-unit.md)

## References

- [kubectl cheat sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
