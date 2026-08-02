---
title: "RBAC and Kubernetes Security Basics"
description: "Implement Kubernetes RBAC with Roles, ClusterRoles, bindings, and ServiceAccounts for least-privilege DevOps access."
difficulty: intermediate
estimated_time: "45–60 min"
technology: kubernetes
category: kubernetes
module: "Module 10 · Security"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - kubernetes
  - rbac
  - security
prerequisites:
  - kubernetes/kubernetes-scheduling
next:
  - kubernetes/kubernetes-security-hardening
related:
  - kubernetes/platform-engineering-on-kubernetes
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKA
  - CKS
tags:
  - kubernetes
  - rbac
  - serviceaccount
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# RBAC and Kubernetes Security Basics

## Overview







Create a ServiceAccount with a Role that can only list Pods in one namespace — least privilege in practice.

**RBAC** answers: who (Subject) can do what (verbs) on which resources. Prefer Roles + RoleBindings for namespace scope; ClusterRoles for cluster-wide.

This is a core tutorial in **Module 10 · Security** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Kubernetes Scheduling](kubernetes-scheduling.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Create ServiceAccount, Role, RoleBinding  
- [ ] Test with `kubectl auth can-i`  
- [ ] Contrast Role vs ClusterRole  
- [ ] Avoid default SA over-privilege

## Architecture







This topic’s control points and relationships are shown below.

![RBAC model](../assets/excalidraw/k8s-rbac-model.svg)

## Theory







### What it is

**Role-Based Access Control (RBAC)** authorises API requests after authentication. You bind a **subject** (User, Group, or **ServiceAccount**) to a **Role** or **ClusterRole** that lists allowed **verbs** on **resources**. Namespace-scoped **RoleBinding** grants a Role inside one namespace; **ClusterRoleBinding** grants cluster-wide (or reuses a ClusterRole in a namespace via RoleBinding).

### Why it matters

Every `kubectl` call and every in-Pod client uses some identity. Over-powered ServiceAccounts turn a single compromised Pod into cluster-admin. Least privilege is the foundation of CKA/CKS practice and of platform multi-tenancy. RBAC does not replace NetworkPolicy or Pod security — it gates the API.

### How it works (mental model)

1. Request arrives at the API server with credentials.
2. Authentication establishes the user/SA identity.
3. Authorisation (RBAC) checks bindings for matching verb/resource/namespace.
4. Admission may still mutate or reject; then etcd persistence occurs.
5. Controllers and apps should run as dedicated ServiceAccounts with minimal Roles — not `cluster-admin`.

Test with `kubectl auth can-i` as the subject before deploying.

### Key concepts / comparisons

| Object | Scope |
|--------|-------|
| Role | Rules in one namespace |
| ClusterRole | Cluster-wide rules (or reusable set) |
| RoleBinding | Bind in a namespace |
| ClusterRoleBinding | Bind cluster-wide |
| ServiceAccount | Pod identity for the API |

| Verb examples | Resources |
|---------------|-----------|
| get, list, watch | Read paths |
| create, update, patch, delete | Write paths |

### Common pitfalls

- Binding `cluster-admin` to application SAs “temporarily” and never removing it.
- Using the `default` ServiceAccount with mounted tokens for app Pods.
- Creating a Role but forgetting the RoleBinding — silent 403s.
- Confusing authentication (who are you?) with authorisation (what may you do?).
- Granting `*` verbs on `*` resources in a namespace that still includes Secrets and Roles.

## Hands-on Lab



### Objective

Build and verify a working Kubernetes solution for **RBAC and Kubernetes Security Basics** that you can inspect, prove, and tear down safely.

### Prerequisites

- kubectl configured against a lab cluster (kind/minikube preferred)
- Cluster-admin or namespace-create rights in the lab cluster
- Writable workspace at `~/rebash-k8s/module-10`

### Lab environment

Workspace: `~/rebash-k8s/module-10`

Local kind/minikube or a dedicated sandbox cluster. Never target a shared production API server.

```bash
mkdir -p ~/rebash-k8s/module-10 && cd ~/rebash-k8s/module-10
```

### Real-world scenario

Your platform team is rolling out **RBAC and Kubernetes Security Basics** for a new microservice. You must apply the change in an isolated namespace, prove it works with kubectl, and leave evidence for the on-call handover.

### Step-by-step tasks

#### Task 1 – Create ServiceAccount, Role, RoleBinding

Least privilege starts with namespaced RBAC objects.

```bash
kubectl create namespace rebash-lab --dry-run=client -o yaml | kubectl apply -f -
kubectl create serviceaccount viewer -n rebash-lab
cat > rbac.yaml << EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: rebash-lab
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: viewer-pods
  namespace: rebash-lab
subjects:
  - kind: ServiceAccount
    name: viewer
    namespace: rebash-lab
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
EOF
kubectl apply -f rbac.yaml
```

**Expected output:** Role and RoleBinding created without error.

#### Task 2 – Prove allow and deny with auth can-i

Never guess permissions — ask the API.

```bash
kubectl auth can-i list pods -n rebash-lab --as=system:serviceaccount:rebash-lab:viewer
kubectl auth can-i delete pods -n rebash-lab --as=system:serviceaccount:rebash-lab:viewer || true
```

**Expected output:** `yes` for list; `no` (or non-zero) for delete.

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

- Applied a real cluster change for RBAC and Kubernetes Security Basics
- Used describe/Events for verification
- Destroyed lab resources cleanly

### Cleanup

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Keep ~/rebash-kubernetes/ for later tutorials
```

## Validation







- [ ] Lab commands run under `~/rebash-k8s/module-10/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **RBAC and Kubernetes Security Basics** always combines:

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







!!! warning "Binding `cluster-admin` to application SAs “temporarily” and never removing it."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Using the `default` ServiceAccount with mounted tokens for app Pods."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode RBAC and Kubernetes Security Basics changes as code and review them in pull requests
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







**RBAC and Kubernetes Security Basics** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions






1. What are Role, ClusterRole, RoleBinding, and ClusterRoleBinding?
2. How do you test whether a ServiceAccount can list Pods in a namespace?
3. Why prefer RoleBinding in a single namespace over ClusterRoleBinding?
4. What is the danger of binding users to cluster-admin for convenience?
5. How should applications authenticate to the API from inside a Pod?

!!! tip "Sample answer — question 2"
    Use `kubectl auth can-i` with `--as=system:serviceaccount:ns:name` to evaluate RBAC without guessing. It reflects the authorisation rules currently applied.

!!! tip "Sample answer — question 4"
    cluster-admin bypasses least privilege and turns any credential leak into full cluster compromise. Scope Roles narrowly and use Just-In-Time elevation where possible.

## Related Tutorials







- [Course overview](index.md)
- [Kubernetes Security Hardening](kubernetes-security-hardening.md)

## References







- [Using RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
