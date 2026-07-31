---
title: "Troubleshooting Kubernetes Workloads"
description: "Debug CrashLoopBackOff, ImagePullBackOff, Pending Pods, DNS, scheduling, storage, and networking failures systematically."
difficulty: advanced
estimated_time: "50–70 min"
technology: kubernetes
category: kubernetes
module: "Module 18 · Troubleshooting"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - kubernetes
  - troubleshooting
prerequisites:
  - kubernetes/kubernetes-production-operations
next:
  - kubernetes/managed-kubernetes-eks-aks-gke
related:
  - kubernetes/kubectl-essentials-and-workflows
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKA
  - CKAD
tags:
  - kubernetes
  - troubleshooting
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Troubleshooting Kubernetes Workloads

## Overview

Apply a fixed playbook: Events → describe → logs → previous logs → exec → node/network — for the common Pending / CrashLoop / ImagePull failures.

Most “cluster down” tickets are workload config. Read **Events** before changing YAML randomly.

This is a core tutorial in **Module 18 · Troubleshooting** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Production Operations](kubernetes-production-operations.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Diagnose CrashLoopBackOff  
- [ ] Fix ImagePullBackOff (tag/auth)  
- [ ] Explain Pending (resources/affinity/PVC)  
- [ ] Debug Service/DNS connectivity

## Architecture

This topic’s control points and relationships are shown below.

![Pod lifecycle](../assets/excalidraw/k8s-pod-lifecycle.svg)

## Theory

### What it is

**Troubleshooting** is a disciplined path from symptom to cause using the Kubernetes API: object status, **Events**, logs, and previous container instances. Most tickets labelled “cluster down” are workload misconfiguration — bad images, probes, resources, selectors, or mounts. The cluster’s controllers are usually doing exactly what you asked; the job is to discover what you asked for.

### Why it matters

Random restarts and YAML churn lengthen outages. A fixed playbook — Events → describe → logs → previous logs → exec → node/network — cuts mean time to recovery and teaches juniors transferable habits. CKA scenarios reward this order under time pressure.

### How it works (mental model)

1. **Reproduce scope**: one Pod, one Deployment, one namespace, or many nodes?
2. **Read status**: `get` Ready/Restarts; `describe` for Conditions and Events.
3. **Logs**: current and `--previous` for CrashLoop; check init containers too.
4. **Dependencies**: Secrets/ConfigMaps exist? PVC Bound? Service has endpoints?
5. **Platform layer**: node NotReady, CNI, CoreDNS, admission webhooks denying creates.

Controllers reconcile desired state — if desired state is wrong, they will faithfully keep failing.

### Key concepts / comparisons

| Symptom | First checks |
|---------|----------------|
| CrashLoopBackOff | `logs`, `logs --previous`, probes, CMD |
| ImagePullBackOff | image name, pull secret, registry |
| Pending | `describe` Events, resources, taints |
| DNS | CoreDNS pods, NetworkPolicy |
| PVC Pending | StorageClass, provisioner |
| Service empty | Selector vs Pod labels, readiness |

| Layer | Examples |
|-------|----------|
| App | Exit code, config, migrations |
| Manifest | Probes, resources, mounts |
| Cluster | Scheduler, CNI, DNS, webhooks |

### Common pitfalls

- Deleting Pods before capturing Events and previous logs.
- Fixating on Deployment status while the PVC is Pending.
- Ignoring init container failures.
- Assuming NetworkPolicy cannot be the cause of “DNS broken”.
- Changing three things at once — lose the causal link.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-18 && cd ~/rebash-k8s/module-18
```

**Focus:** hands-on practice for Troubleshooting Kubernetes Workloads

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Troubleshooting Kubernetes Workloads"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-k8s/module-18 && cd ~/rebash-k8s/module-18
kubectl run boom --image=busybox:1.36 --restart=Always -- /bin/false
sleep 5
kubectl get pod boom
kubectl describe pod boom | sed -n '/Events/,$p'
kubectl logs boom --previous 2>/dev/null || kubectl logs boom
kubectl delete pod boom
kubectl run badpull --image=ghcr.io/rebash/does-not-exist:latest --restart=Never || true
sleep 3
kubectl describe pod badpull 2>/dev/null | sed -n '/Events/,$p' | head -n 20
kubectl delete pod badpull --ignore-not-found
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-kubernetes/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-k8s/module-18/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Troubleshooting Kubernetes Workloads** always combines:

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

!!! warning "Deleting Pods before capturing Events and previous logs."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Fixating on Deployment status while the PVC is Pending."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Troubleshooting Kubernetes Workloads changes as code and review them in pull requests
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

**Troubleshooting Kubernetes Workloads** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Troubleshooting Kubernetes Workloads** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Managed Kubernetes — EKS, AKS, GKE](managed-kubernetes-eks-aks-gke.md)

## References

- [Debug Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
