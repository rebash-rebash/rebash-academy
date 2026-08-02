---
title: "Platform Engineering on Kubernetes"
description: "Build internal platforms with Operators, CRDs, admission controllers, custom controllers, and multi-tenant namespace patterns."
difficulty: advanced
estimated_time: "50–70 min"
technology: kubernetes
category: kubernetes
module: "Module 16 · Platform Engineering"
career_paths:
  - platform-engineer
  - kubernetes-engineer
  - devops-engineer
  - site-reliability-engineer
skills:
  - kubernetes
  - operators
  - crds
  - platform-engineering
prerequisites:
  - kubernetes/gitops-and-cicd-with-kubernetes
next:
  - kubernetes/kubernetes-production-operations
related:
  - platform-engineering/index
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKA
tags:
  - kubernetes
  - operators
  - crd
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Platform Engineering on Kubernetes

## Overview







Explain CRDs and Operators as the extension model, outline admission webhooks, and design namespace-based multi-tenancy with quotas and RBAC.

Platform teams expose paved roads: templates, Operators (extend the API), policy (OPA/Kyverno via admission), and self-service namespaces.

This is a core tutorial in **Module 16 · Platform Engineering** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [GitOps](gitops-and-cicd-with-kubernetes.md) · [RBAC](rbac-and-kubernetes-security-basics.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Define CRD vs custom controller / Operator  
- [ ] Place validating/mutating admission  
- [ ] Sketch soft multi-tenancy (ns + quota + RBAC)  
- [ ] List what not to put in a shared cluster

## Architecture







This topic’s control points and relationships are shown below.

![Production / platform](../assets/excalidraw/k8s-production-cluster.svg)

## Theory







### What it is

**Platform engineering** on Kubernetes means building paved roads so product teams ship without becoming full-time cluster experts. The extension model is the **Operator pattern**: **Custom Resource Definitions (CRDs)** add new API types; **controllers** reconcile those types into Pods, buckets, databases, or policies. **Admission webhooks** (mutating/validating) and policy engines (Kyverno, OPA Gatekeeper) enforce standards at create time. Multi-tenancy usually starts with namespaces, RBAC, and quotas.

### Why it matters

Handing every team a raw cluster creates snowflake YAML and security drift. A platform productises golden paths: templates, service catalogues, shared ingress/observability, and self-service namespaces. Operators encode operational knowledge (backup, failover) into software that reconciles continuously — the same control-loop idea as Deployments, applied to higher-level services.

### How it works (mental model)

1. Define a CRD (`Widget`) describing desired intent.
2. An Operator watches Widget objects and creates Deployments, Services, PVCs, etc.
3. Admission policies validate labels, block `:latest`, or inject sidecars.
4. Tenants get a namespace with RoleBindings and ResourceQuotas; platform owns cluster add-ons.
5. GitOps delivers both platform components and tenant apps.

If reconciliation fails, the custom resource shows conditions — debug like any controller.

### Key concepts / comparisons

| Concept | Meaning |
|---------|---------|
| CRD | Schema for a custom API object |
| Controller / Operator | Reconcile custom resources |
| Admission | Mutate/validate before persist |
| Soft multi-tenancy | Shared cluster, ns isolation |
| Hard multi-tenancy | Separate clusters / stronger isolation |

| Shared cluster OK | Prefer isolation |
|-------------------|------------------|
| Stateless apps with NetworkPolicy | Untrusted code execution |
| Internal tools | Hostile multi-tenant SaaS without extra controls |

### Common pitfalls

- Building Operators before documenting the paved path — golden paths beat custom CRDs for many apps.
- Cluster-admin bindings for every tenant “to unblock”.
- Admission webhooks that deadlock the API (fail closed without care during outages).
- CRDs without status/conditions — users cannot see why reconcile stalled.
- Assuming namespaces equal security isolation without NetworkPolicy and PSA.

## Hands-on Lab



### Objective

Build and verify a working Kubernetes solution for **Platform Engineering on Kubernetes** that you can inspect, prove, and tear down safely.

### Prerequisites

- kubectl configured against a lab cluster (kind/minikube preferred)
- Cluster-admin or namespace-create rights in the lab cluster
- Writable workspace at `~/rebash-k8s/module-16`

### Lab environment

Workspace: `~/rebash-k8s/module-16`

Local kind/minikube or a dedicated sandbox cluster. Never target a shared production API server.

```bash
mkdir -p ~/rebash-k8s/module-16 && cd ~/rebash-k8s/module-16
```

### Real-world scenario

Your platform team is rolling out **Platform Engineering on Kubernetes** for a new microservice. You must apply the change in an isolated namespace, prove it works with kubectl, and leave evidence for the on-call handover.

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

- Applied a real cluster change for Platform Engineering on Kubernetes
- Used describe/Events for verification
- Destroyed lab resources cleanly

### Cleanup

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Keep ~/rebash-kubernetes/ for later tutorials
```

## Validation







- [ ] Lab commands run under `~/rebash-k8s/module-16/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Platform Engineering on Kubernetes** always combines:

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







!!! warning "Building Operators before documenting the paved path — golden paths beat custom CRDs for m"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Cluster-admin bindings for every tenant “to unblock”."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Platform Engineering on Kubernetes changes as code and review them in pull requests
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







**Platform Engineering on Kubernetes** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions






1. What is a golden path in platform engineering?
2. How do templates or Helm charts reduce cognitive load for product teams?
3. What should a platform expose as self-service versus keep as a ticket?
4. How do you prevent golden paths from becoming unchangeable constraints?
5. Which Kubernetes APIs commonly underpin an internal developer platform?

!!! tip "Sample answer — question 2"
    Golden paths encode defaults for Deployments, networking, observability, and security so teams ship without reinventing cluster details.

!!! tip "Sample answer — question 4"
    Offer escape hatches, versioned templates, and feedback loops. Rigid platforms that block legitimate needs drive shadow IT; measure adoption and iterate with users.

## Related Tutorials







- [Course overview](index.md)
- [Kubernetes Production Operations](kubernetes-production-operations.md)

## References







- [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) · [Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
