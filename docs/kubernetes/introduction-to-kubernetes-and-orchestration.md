---
title: "Introduction to Kubernetes and Orchestration"
description: "Understand why Kubernetes exists, what orchestration solves for DevOps, and the core vocabulary before you touch a cluster."
difficulty: intermediate
estimated_time: "35–50 min"
technology: kubernetes
category: kubernetes
module: "Module 1 · Kubernetes Fundamentals"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - cloud-engineer
skills:
  - kubernetes
  - orchestration
prerequisites:
  - docker/index
  - linux/index
next:
  - kubernetes/kubernetes-architecture-and-components
related:
  - docker/from-docker-to-kubernetes
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - KCNA
  - CKA
tags:
  - kubernetes
  - orchestration
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Introduction to Kubernetes and Orchestration

## Overview



Explain what Kubernetes orchestrates, why single-host Docker is not enough for production fleets, and use cluster vocabulary correctly.

**Kubernetes** schedules containers across machines, keeps desired state, and exposes stable networking. This course is **Kubernetes for Cloud & DevOps Engineers** — operate clusters, not slide-deck trivia.

This is a core tutorial in **Module 1 · Kubernetes Fundamentals** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Docker](../docker/index.md) · [Linux](../linux/index.md) · networking basics



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] State problems orchestration solves  
- [ ] Define cluster, node, Pod, control plane  
- [ ] Contrast Compose vs Kubernetes  
- [ ] Name CKA/CKAD-relevant domains



## Architecture



This topic’s control points and relationships are shown below.

![Kubernetes architecture](../assets/excalidraw/k8s-architecture.svg)



## Theory



### What it is

**Kubernetes** (often abbreviated **K8s**) is an open-source **container orchestration** platform. You declare the desired state of workloads — how many replicas, which image, which ports — and the cluster continuously works to make reality match that declaration. It is not a replacement for Docker as a build tool; it schedules and operates containers that you already package as images.

### Why it matters

A single Docker host is fine for a laptop or a tiny demo. Production DevOps faces many hosts, rolling updates, failed nodes, and the need for a stable network identity when Pods come and go. Orchestration answers those operational problems so teams stop hand-placing containers and start managing fleets through an API.

### How it works (mental model)

Think of Kubernetes as a control loop:

1. You (or CI/GitOps) write API objects (YAML or JSON).
2. The **API server** validates and stores them in **etcd**.
3. **Controllers** watch desired state and reconcile — create Pods, replace crashed ones, roll out new images.
4. The **scheduler** picks a node; the **kubelet** on that node pulls images and runs containers.

Desired state is the source of truth. If a Pod dies, a controller recreates it. If you scale replicas from two to five, the Deployment controller adds Pods until the count matches.

### Key concepts / comparisons

| Need | Kubernetes answer |
|------|-------------------|
| Many hosts | Scheduler + kubelet |
| Self-heal | Controllers reconcile |
| Stable address | Service / Ingress |
| Declarative ops | API objects in etcd |

| Concept | Meaning |
|---------|---------|
| Cluster | Control plane + worker nodes |
| Node | Machine (VM or bare metal) running kubelet |
| Pod | Smallest deployable unit (one or more containers) |
| Control plane | API, etcd, scheduler, controllers |

**Docker Compose** is excellent locally for a few services on one host. **Kubernetes** is the portable control plane for multi-node cloud production. Compose does not give you cross-host scheduling, rolling updates with health gates, or cluster-wide RBAC out of the box.

### Common pitfalls

- Treating Kubernetes as “Docker with YAML” and ignoring controllers — bare Pods do not self-heal on node loss.
- Expecting Compose skills alone to map one-to-one; Services, Deployments, and namespaces are new primitives.
- Confusing the container runtime (containerd) with orchestration — Kubernetes orchestrates; the runtime only runs containers.
- Jumping into production clusters before learning desired-state mental models and kubectl inspection habits.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-01 && cd ~/rebash-k8s/module-01
```

**Focus:** Run your first workload and contrast it with a single container process

### Step 1 – Create a namespace and run a Pod

```bash
kubectl create namespace rebash-lab
kubectl -n rebash-lab run hello --image=nginx:1.27-alpine --port=80
kubectl -n rebash-lab wait --for=condition=Ready pod/hello --timeout=60s
kubectl -n rebash-lab get pods -o wide
```

### Step 2 – Inspect orchestration metadata

```bash
kubectl -n rebash-lab describe pod hello | head -n 40
kubectl -n rebash-lab get pod hello -o jsonpath='{.status.podIP}{"
"}{.spec.nodeName}{"
"}'
kubectl -n rebash-lab delete pod hello
# Note: a bare Pod is not recreated — Deployments restore desired replicas
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-k8s/module-01/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Introduction to Kubernetes and Orchestration** always combines:

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



!!! warning "Treating Kubernetes as “Docker with YAML” and ignoring controllers — bare Pods do not self"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Expecting Compose skills alone to map one-to-one; Services, Deployments, and namespaces ar"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Introduction to Kubernetes and Orchestration changes as code and review them in pull requests
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



**Introduction to Kubernetes and Orchestration** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. What problem does container orchestration solve beyond running a single container?
2. What is a Pod, and why is it the smallest deployable unit?
3. How does desired state reconciliation differ from imperative scripting?
4. What operational risks appear if you only run containers with Docker on one host in production?
5. Name three capabilities Kubernetes provides out of the box for applications.

!!! tip "Sample answer — question 2"
    A Pod is one or more containers sharing network and storage namespaces. Kubernetes schedules and restarts Pods as units, so the Pod—not the container—is the atomic deployable object.

!!! tip "Sample answer — question 4"
    A single host lacks automated rescheduling, rolling updates, and cluster-wide service discovery. Failures of that host take everything down, and scaling is manual and error-prone.



## Related Tutorials



- [Course overview](index.md)
- [Kubernetes Architecture and Components](kubernetes-architecture-and-components.md)



## References



- [Kubernetes overview](https://kubernetes.io/docs/concepts/overview/)
