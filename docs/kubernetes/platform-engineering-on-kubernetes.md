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

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-16 && cd ~/rebash-k8s/module-16
```

**Focus:** hands-on practice for Platform Engineering on Kubernetes

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-k8s/module-16 && cd ~/rebash-k8s/module-16
kubectl api-resources | head -n 20
kubectl get crd 2>/dev/null | head || echo "No CRDs yet — Operators add them"
cat > tenant-checklist.md << 'EOF'
- Namespace per team/app
- ResourceQuota + LimitRange
- RoleBinding to team group
- NetworkPolicy default deny
- PSA enforce=baseline|restricted
- GitOps Application per env
EOF
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-kubernetes/ for later tutorials; destroy disposable cloud resources from this lab
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

1. How does **Platform Engineering on Kubernetes** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Kubernetes Production Operations](kubernetes-production-operations.md)

## References

- [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) · [Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
