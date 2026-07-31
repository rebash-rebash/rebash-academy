---
title: "Workload Controllers — StatefulSet, DaemonSet, Jobs"
description: "Choose StatefulSets, DaemonSets, Jobs, and CronJobs for stateful, node-agent, and batch workloads on Kubernetes."
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
  - statefulset
  - jobs
prerequisites:
  - kubernetes/deployments-managing-replicated-pods
next:
  - kubernetes/services-and-cluster-networking
related:
  - kubernetes/persistent-volumes-and-storage
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKAD
  - CKA
tags:
  - kubernetes
  - statefulset
  - daemonset
  - cronjob
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Workload Controllers — StatefulSet, DaemonSet, Jobs

## Overview

Pick the right controller: Deployment vs StatefulSet vs DaemonSet vs Job/CronJob — and run a Job to completion.

| Controller | Use |
|------------|-----|
| Deployment | Stateless apps |
| StatefulSet | Stable identity + storage (DBs, queues) |
| DaemonSet | One Pod per node (agents, CNI helpers) |
| Job / CronJob | Batch / scheduled batch |

This is a core tutorial in **Module 4 · Workload Management** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Deployments](deployments-managing-replicated-pods.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Contrast identity of StatefulSet Pods  
- [ ] Explain DaemonSet scheduling  
- [ ] Run a Job and CronJob schedule basics

## Architecture

This topic’s control points and relationships are shown below.

![Architecture](../assets/excalidraw/k8s-architecture.svg)

## Theory

### What it is

Beyond Deployments, Kubernetes offers specialised controllers. A **StatefulSet** gives Pods stable network identity and ordered, sticky storage — suited to databases and queues. A **DaemonSet** runs (roughly) one Pod per eligible node — agents, log collectors, CNI helpers. **Jobs** run Pods to completion; **CronJobs** create Jobs on a schedule.

### Why it matters

Using a Deployment for a database loses stable identity and volume binding semantics. Using a StatefulSet for a stateless API adds complexity you do not need. Choosing the wrong controller causes painful data and networking bugs. Batch work belongs in Jobs so failures retry with backoff instead of CrashLoop forever.

### How it works (mental model)

- **StatefulSet**: Pods named `name-0`, `name-1`, …; each can get a PVC from `volumeClaimTemplates`; updates and scale often respect ordinal order; pair with a **headless Service** for per-Pod DNS.
- **DaemonSet**: scheduler places a Pod on every node matching the template (respecting taints/tolerations); node join adds a Pod; node drain removes it.
- **Job**: runs until `completions` succeed; `parallelism` controls concurrency; failed Pods retry per `backoffLimit`.
- **CronJob**: controller creates Jobs from a cron expression; concurrency policies control overlap.

All still reconcile desired vs actual state through the API.

### Key concepts / comparisons

| Controller | Use |
|------------|-----|
| Deployment | Stateless apps |
| StatefulSet | Stable identity + storage |
| DaemonSet | One Pod per node |
| Job / CronJob | Batch / scheduled batch |

| Identity | Deployment | StatefulSet |
|----------|------------|-------------|
| Pod name | Random suffix | Stable ordinal |
| Storage | Usually ephemeral or shared PVC patterns | Per-Pod claims typical |

### Common pitfalls

- Deleting a StatefulSet without understanding PVC retention — data may remain or vanish depending on policy.
- Expecting DaemonSets to schedule onto control-plane nodes without tolerations.
- Jobs with wrong restart policy or infinite retries flooding the cluster.
- Using Deployments for Kafka/ZooKeeper-style workloads without understanding identity and peer discovery.
- CronJobs in the wrong timezone mental model — schedules use the controller’s interpretation; document clearly.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-04-ctl && cd ~/rebash-k8s/module-04-ctl
```

**Focus:** hands-on practice for Workload Controllers — StatefulSet, DaemonSet, Jobs

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Workload Controllers — StatefulSet, DaemonSet, Jobs"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-k8s/module-04-ctl && cd ~/rebash-k8s/module-04-ctl
cat > job.yaml << 'EOF'
apiVersion: batch/v1
kind: Job
metadata:
  name: rebash-job
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: hi
          image: busybox:1.36
          command: ["sh", "-c", "echo done && sleep 2"]
  backoffLimit: 1
EOF
kubectl apply -f job.yaml
kubectl wait --for=condition=complete job/rebash-job --timeout=60s
kubectl logs job/rebash-job
kubectl delete -f job.yaml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-kubernetes/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-k8s/module-04-ctl/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Workload Controllers — StatefulSet, DaemonSet, Jobs** always combines:

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

!!! warning "Deleting a StatefulSet without understanding PVC retention — data may remain or vanish dep"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Expecting DaemonSets to schedule onto control-plane nodes without tolerations."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Workload Controllers — StatefulSet, DaemonSet, Jobs changes as code and review them in pull requests
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

**Workload Controllers — StatefulSet, DaemonSet, Jobs** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Workload Controllers — StatefulSet, DaemonSet, Jobs** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Services and Cluster Networking](services-and-cluster-networking.md)

## References

- [Workload resources](https://kubernetes.io/docs/concepts/workloads/controllers/)
