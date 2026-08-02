---
title: "Helm Package Management"
description: "Install and manage applications with Helm charts, repositories, values, dependencies, and chart development for Kubernetes DevOps."
difficulty: intermediate
estimated_time: "45–60 min"
technology: kubernetes
category: kubernetes
module: "Module 14 · Package Management"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
skills:
  - kubernetes
  - helm
prerequisites:
  - kubernetes/kubernetes-autoscaling
next:
  - kubernetes/gitops-and-cicd-with-kubernetes
related:
  - helm/index
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKAD
tags:
  - kubernetes
  - helm
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Helm Package Management

## Overview









Install a chart from a repo with custom values, list/upgrade/rollback a release, and sketch chart structure (`Chart.yaml`, templates, values).

**Helm** packages Kubernetes manifests as **charts**. Releases track installed instances. Prefer pinned chart versions in production.

This is a core tutorial in **Module 14 · Package Management** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites









- [Kubernetes Autoscaling](kubernetes-autoscaling.md)
- Helm 3 CLI installed

## Learning Objectives









By the end of this tutorial, you will be able to:

- [ ] `helm repo add` / `install` / `upgrade` / `rollback`  
- [ ] Override with `-f values.yaml`  
- [ ] Inspect `helm template` output  
- [ ] Outline chart dependencies

## Architecture









This topic’s control points and relationships are shown below.

![Helm architecture](../assets/excalidraw/k8s-helm-architecture.svg)

## Theory









### What it is

**Helm** is the common package manager for Kubernetes. A **chart** is a versioned bundle of templates and default values. A **release** is a named instance of a chart installed into a cluster (and usually a namespace). Helm 3 stores release metadata in Secrets/ConfigMaps in-cluster; there is no Tiller.

### Why it matters

Hand-maintaining dozens of raw manifests per environment does not scale. Charts parameterise images, replicas, and ingress hosts via **values**, so the same package deploys to lab and production with different `-f` files. Platforms and GitOps tools often render or deliver Helm charts as the unit of install.

### How it works (mental model)

1. `helm repo add` / `pull` obtains chart packages (or you `helm create` locally).
2. Templates under `templates/` plus `values.yaml` render to Kubernetes YAML (`helm template` to preview).
3. `helm install` / `upgrade` applies the rendered objects and records a release revision.
4. `helm rollback` reverts to a previous revision’s manifest set.
5. Dependencies in `Chart.yaml` pull subcharts; OCI registries increasingly host charts alongside images.

Helm does not replace controllers — it ships the desired-state objects those controllers reconcile.

### Key concepts / comparisons

| Piece | Role |
|-------|------|
| Chart | Package (Chart.yaml, values, templates) |
| Release | Installed instance + history |
| Values | Configuration overlays |
| Repo / OCI | Distribution |

| Command | Use |
|---------|-----|
| `helm install` | Create release |
| `helm upgrade` | Move to new chart/values |
| `helm rollback` | Restore prior revision |
| `helm template` | Client-side render / debug |

Prefer pinned chart versions in production; floating `latest` charts are supply-chain risk.

### Common pitfalls

- Upgrading with incomplete values and accidentally resetting replicas or resources to chart defaults.
- Editing live objects that Helm owns — next upgrade overwrites them (use values or `lookup` patterns carefully).
- Ignoring `helm template` diffs in CI — broken YAML ships unnoticed.
- Mixing `kubectl apply` and Helm on the same resources without ownership rules.
- Trusting unverified third-party charts with cluster-admin RBAC inside.

## Hands-on Lab



### Objective

Build and verify a working Kubernetes solution for **Helm Package Management** that you can inspect, prove, and tear down safely.

### Prerequisites

- kubectl configured against a lab cluster (kind/minikube preferred)
- Cluster-admin or namespace-create rights in the lab cluster
- Writable workspace at `~/rebash-k8s/module-14`

### Lab environment

Workspace: `~/rebash-k8s/module-14`

Local kind/minikube or a dedicated sandbox cluster. Never target a shared production API server.

```bash
mkdir -p ~/rebash-k8s/module-14 && cd ~/rebash-k8s/module-14
```

### Real-world scenario

Your platform team is rolling out **Helm Package Management** for a new microservice. You must apply the change in an isolated namespace, prove it works with kubectl, and leave evidence for the on-call handover.

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

- Applied a real cluster change for Helm Package Management
- Used describe/Events for verification
- Destroyed lab resources cleanly

### Cleanup

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Keep ~/rebash-kubernetes/ for later tutorials
```

## Validation









- [ ] Lab commands run under `~/rebash-k8s/module-14/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough









Production practice for **Helm Package Management** always combines:

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









!!! warning "Upgrading with incomplete values and accidentally resetting replicas or resources to chart"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Editing live objects that Helm owns — next upgrade overwrites them (use values or `lookup`"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices









- Encode Helm Package Management changes as code and review them in pull requests
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









**Helm Package Management** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions








1. What is a Helm chart, and what problem does it solve?
2. What is the difference between `helm install` and `helm upgrade --install`?
3. Where does Helm store release metadata in modern Helm 3?
4. What risks come from installing charts with default values in production?
5. How do values files help manage environment differences?

!!! tip "Sample answer — question 2"
    `helm upgrade --install` creates the release if missing or upgrades it if present, which is convenient for CI idempotency. Plain `helm install` fails if the release already exists.

!!! tip "Sample answer — question 4"
    Default values often enable broad permissions, public images, or weak resource settings. Production needs reviewed values, pinned versions, least privilege, and secret handling outside plain values where possible.

## Related Tutorials









- [Course overview](index.md)
- [GitOps and CI/CD with Kubernetes](gitops-and-cicd-with-kubernetes.md)

## References









- [Helm docs](https://helm.sh/docs/) · [REBASH Helm track](../helm/index.md)
