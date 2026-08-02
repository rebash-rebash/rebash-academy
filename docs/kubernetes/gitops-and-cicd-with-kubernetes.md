---
title: "GitOps and CI/CD with Kubernetes"
description: "Implement GitOps with Argo CD or Flux — progressive delivery, rollbacks, and how CI builds images while Git drives cluster state."
difficulty: advanced
estimated_time: "50–70 min"
technology: kubernetes
category: kubernetes
module: "Module 15 · GitOps"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - kubernetes
  - gitops
  - argo-cd
prerequisites:
  - kubernetes/helm-package-management
  - git/gitops-fundamentals
next:
  - kubernetes/platform-engineering-on-kubernetes
related:
  - argocd/index
  - git/index
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKA
tags:
  - kubernetes
  - gitops
  - argocd
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# GitOps and CI/CD with Kubernetes

## Overview









Separate CI (build/push images) from GitOps (desired cluster state in Git) and sketch an Argo CD Application sync/rollback flow.

**GitOps**: Git is source of truth; a reconciler (Argo CD / Flux) syncs the cluster. Progressive delivery (Argo Rollouts / Flagger) gates traffic.

This is a core tutorial in **Module 15 · GitOps** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites









- [Helm](helm-package-management.md) · [GitOps fundamentals](../git/gitops-fundamentals.md)

## Learning Objectives









By the end of this tutorial, you will be able to:

- [ ] State GitOps principles  
- [ ] Contrast push CI deploy vs pull GitOps  
- [ ] Describe Argo CD sync / rollback  
- [ ] Layout app vs config repos

## Architecture









This topic’s control points and relationships are shown below.

![GitOps workflow](../assets/excalidraw/k8s-gitops-workflow.svg)

## Theory









### What it is

**GitOps** keeps the desired cluster state in Git and uses a reconciler (**Argo CD**, **Flux**) to make the cluster match that state. **CI** still builds and tests images; it pushes artefacts to a registry and often opens a PR that bumps an image tag in the config repo. Progressive delivery tools (Argo Rollouts, Flagger) add traffic shifting and automated rollback on bad metrics.

### Why it matters

Push-from-CI `kubectl apply` works until credentials sprawl, drifts accumulate, and nobody knows what production *should* look like. GitOps gives auditability (Git history), pull-based credentials on the cluster side, and a single rollback story: revert the commit or hard-sync a previous revision. Platform teams standardise Application/Kustomization objects per environment.

### How it works (mental model)

1. Developers merge app code → CI builds/pushes image → updates manifest/Helm values in Git.
2. Argo CD/Flux detects the commit (webhook or poll) and **syncs** (apply/prune per policy).
3. Kubernetes controllers reconcile Deployments and friends as usual.
4. If health checks or metrics fail, roll back Git or disable auto-sync and fix forward.
5. Drift (manual `kubectl edit`) is either corrected on next sync or blocked by policy.

Desired state lives in Git; the cluster is a projection. Controllers still own runtime reconciliation.

### Key concepts / comparisons

| Model | Flow |
|-------|------|
| Push CI deploy | Pipeline kubeconfig applies YAML |
| Pull GitOps | In-cluster agent syncs from Git |

| Concern | Practice |
|---------|----------|
| App repo | Source code + Dockerfile |
| Config repo | Manifests / Helm / Kustomize per env |
| Secrets | Sealed Secrets, SOPS, ESO — not plain Git |

### Common pitfalls

- Storing plaintext Secrets in Git.
- Auto-sync with prune in a shared folder that deletes unrelated resources.
- CI and GitOps both deploying the same app — fight over image tags.
- Monorepo paths without directory-scoped Applications — one bad sync affects all.
- Treating sync success as user-success without app health/metrics gates.

## Hands-on Lab



### Objective

Build and verify a working Kubernetes solution for **GitOps and CI/CD with Kubernetes** that you can inspect, prove, and tear down safely.

### Prerequisites

- kubectl configured against a lab cluster (kind/minikube preferred)
- Cluster-admin or namespace-create rights in the lab cluster
- Writable workspace at `~/rebash-k8s/module-15/{apps/demo,clusters/dev}`

### Lab environment

Workspace: `~/rebash-k8s/module-15/{apps/demo,clusters/dev}`

Local kind/minikube or a dedicated sandbox cluster. Never target a shared production API server.

```bash
mkdir -p ~/rebash-k8s/module-15/{apps/demo,clusters/dev} && cd ~/rebash-k8s/module-15/{apps/demo,clusters/dev}
```

### Real-world scenario

Your platform team is rolling out **GitOps and CI/CD with Kubernetes** for a new microservice. You must apply the change in an isolated namespace, prove it works with kubectl, and leave evidence for the on-call handover.

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

- Applied a real cluster change for GitOps and CI/CD with Kubernetes
- Used describe/Events for verification
- Destroyed lab resources cleanly

### Cleanup

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Keep ~/rebash-kubernetes/ for later tutorials
```

## Validation









- [ ] Lab commands run under `~/rebash-k8s/module-15/{apps/demo,clusters/dev}/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough









Production practice for **GitOps and CI/CD with Kubernetes** always combines:

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









!!! warning "Storing plaintext Secrets in Git."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Auto-sync with prune in a shared folder that deletes unrelated resources."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices









- Encode GitOps and CI/CD with Kubernetes changes as code and review them in pull requests
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









**GitOps and CI/CD with Kubernetes** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions








1. What is GitOps in the context of Kubernetes delivery?
2. Why is the Git repository treated as the source of truth rather than imperative kubectl changes?
3. What is the difference between push-based CI deploy jobs and pull-based GitOps agents?
4. What security trade-offs exist when CI pipelines hold kubeconfig credentials versus a cluster-side reconciler?
5. How do you detect and remediate configuration drift?

!!! tip "Sample answer — question 2"
    Git records the desired state, enabling review, audit, and rollback through normal version control. Imperative cluster edits are easy to lose and hard to reproduce across environments.

!!! tip "Sample answer — question 4"
    CI push models concentrate powerful credentials in the pipeline. Pull-based controllers keep credentials in-cluster with narrower RBAC, reducing blast radius if the CI system is compromised, at the cost of another in-cluster component to operate.

## Related Tutorials









- [Course overview](index.md)
- [Platform Engineering on Kubernetes](platform-engineering-on-kubernetes.md)

## References









- [Argo CD](https://argo-cd.readthedocs.io/) · [OpenGitOps](https://opengitops.dev/)
