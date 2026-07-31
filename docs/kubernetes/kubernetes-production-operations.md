---
title: "Kubernetes Production Operations"
description: "Operate production clusters — upgrades, etcd backup and restore, disaster recovery, high availability, and maintenance windows."
difficulty: advanced
estimated_time: "50–70 min"
technology: kubernetes
category: kubernetes
module: "Module 17 · Production Operations"
career_paths:
  - kubernetes-engineer
  - platform-engineer
  - site-reliability-engineer
  - cloud-engineer
skills:
  - kubernetes
  - etcd
  - disaster-recovery
prerequisites:
  - kubernetes/platform-engineering-on-kubernetes
next:
  - kubernetes/troubleshooting-kubernetes-workloads
related:
  - kubernetes/managed-kubernetes-eks-aks-gke
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKA
tags:
  - kubernetes
  - etcd
  - upgrades
  - dr
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Kubernetes Production Operations

## Overview



Plan control-plane upgrades, document etcd backup/restore, and define HA and maintenance practices for self-managed or managed clusters.

Day-2 ops: version skew policy, drain/cordon workers, etcd snapshots (self-managed), and DR runbooks. Managed services shift etcd ownership to the cloud — still test restore of **workloads and data**.

This is a core tutorial in **Module 17 · Production Operations** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Platform Engineering on Kubernetes](platform-engineering-on-kubernetes.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Follow Kubernetes version skew rules  
- [ ] Cordon/drain a node safely  
- [ ] Outline etcd snapshot (kubeadm)  
- [ ] Write a DR checklist



## Architecture



This topic’s control points and relationships are shown below.

![Production cluster](../assets/excalidraw/k8s-production-cluster.svg)



## Theory



### What it is

**Production operations** (day-2) covers keeping clusters alive over time: upgrades, node maintenance, etcd backup/restore (self-managed), disaster recovery (DR), and high availability (HA). Managed Kubernetes shifts control-plane ownership to the cloud provider, but you still own node pools, add-ons, workloads, and data recovery drills.

### Why it matters

A cluster that deploys well on day one still fails on day 200 without upgrade discipline and tested backups. Version skew between kubelets and control plane is constrained by Kubernetes policy — ignoring it breaks nodes. DR that exists only in slides fails when etcd or a region dies.

### How it works (mental model)

1. **HA**: multiple control-plane/API endpoints (or managed HA); workers across zones; PDBs for apps.
2. **Maintenance**: `cordon` to stop scheduling → `drain` to evict Pods (respects PDBs) → patch/reboot → `uncordon`.
3. **Upgrades**: control plane first (within skew), then kubelets/nodes in waves; validate workloads between waves.
4. **etcd** (self-managed): periodic snapshots, encrypted off-box storage, documented restore; managed clouds: rely on provider control-plane SLAs plus *your* app/data backups.
5. **DR**: rebuild cluster from GitOps + restore volumes/databases; rehearse regularly.

Controllers keep reconciling during maintenance if capacity remains; drains are voluntary disruptions.

### Key concepts / comparisons

| Concern | Self-managed | Managed (EKS/AKS/GKE) |
|---------|--------------|------------------------|
| etcd backup | Your runbook | Provider control plane |
| Control-plane upgrade | kubeadm/kops process | Cloud upgrade API |
| Node upgrade | Your pools | Managed node groups / surge |
| Workload/data DR | Always yours | Always yours |

| Skew idea | Practice |
|-----------|----------|
| kubelet vs API | Stay within supported minor skew |
| kubectl | Prefer close to cluster version |

### Common pitfalls

- Draining without PDBs — simultaneous replica loss.
- Skipping etcd restore tests on self-managed clusters.
- Upgrading all nodes at once; no surge capacity.
- Assuming managed control-plane backup restores your PVCs and databases.
- Running ancient add-ons (CNI, Ingress) incompatible with the new Kubernetes version.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-17 && cd ~/rebash-k8s/module-17
```

**Focus:** Practise operational hygiene: rollouts, events, and resource snapshots

### Step 1 – Deploy and capture operational baseline

```bash
kubectl create namespace rebash-lab
kubectl -n rebash-lab create deployment ops --image=nginx:1.27-alpine --replicas=2
kubectl -n rebash-lab rollout status deploy/ops
kubectl -n rebash-lab get events --sort-by=.lastTimestamp | tail -n 15
```

### Step 2 – Perform a controlled change and inspect history

```bash
kubectl -n rebash-lab set resources deploy/ops -c=nginx --requests=cpu=50m,memory=64Mi
kubectl -n rebash-lab rollout status deploy/ops
kubectl -n rebash-lab rollout history deploy/ops
kubectl -n rebash-lab get deploy ops -o jsonpath='{.spec.template.spec.containers[0].resources}{"
"}'
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-k8s/module-17/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Kubernetes Production Operations** always combines:

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



!!! warning "Draining without PDBs — simultaneous replica loss."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Skipping etcd restore tests on self-managed clusters."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Kubernetes Production Operations changes as code and review them in pull requests
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



**Kubernetes Production Operations** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. What operational signals do you check first when a Deployment misbehaves?
2. How do you perform a safe configuration change in production?
3. What is the value of recording rollout history?
4. How do you balance change velocity with change safety in a shared cluster?
5. Which cluster upgrades are typically your responsibility on a managed service?

!!! tip "Sample answer — question 2"
    Prefer declarative apply, staged environments, rollouts with probes, and quick rollback via rollout undo. Avoid unreviewed imperative edits on live production objects.

!!! tip "Sample answer — question 4"
    Use progressive delivery, RBAC separation, quotas, PDBs, and change windows for risky work. Automate checks so velocity does not skip validation.



## Related Tutorials



- [Course overview](index.md)
- [Troubleshooting Kubernetes Workloads](troubleshooting-kubernetes-workloads.md)



## References



- [Cluster upgrades](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/) · [etcd backup](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)
