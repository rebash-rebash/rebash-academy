---
title: "Production Kubernetes Excellence"
description: "Operate production Kubernetes with multi-cluster strategy, policy enforcement, cost optimisation, scaling, and operational excellence."
difficulty: advanced
estimated_time: "50–70 min"
technology: kubernetes
category: kubernetes
module: "Module 20 · Production Kubernetes"
career_paths:
  - kubernetes-engineer
  - platform-engineer
  - site-reliability-engineer
  - cloud-engineer
skills:
  - kubernetes
  - production-practices
  - finops
prerequisites:
  - kubernetes/managed-kubernetes-eks-aks-gke
  - kubernetes/kubernetes-security-hardening
next:
  - kubernetes/kubernetes-capstone-and-next-steps
related:
  - kubernetes/gitops-and-cicd-with-kubernetes
  - kubernetes/kubernetes-production-operations
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKA
  - CKS
tags:
  - kubernetes
  - production
  - multi-cluster
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Production Kubernetes Excellence

## Overview

Assemble a production excellence checklist: multi-cluster posture, policy, cost controls, observability SLOs, and scaling — ready for a platform review.

Excellence is boring consistency: GitOps everywhere, PSA/NetworkPolicy defaults, scanned images, HPA + PDB, backup tested, and cost visibility (requests right-sizing).

This is a core tutorial in **Module 20 · Production Kubernetes** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- Modules 15–19 complete

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Choose single vs multi-cluster (blast radius)  
- [ ] List policy engines (Kyverno/OPA Gatekeeper)  
- [ ] Name FinOps levers (requests, bin-pack, spot)  
- [ ] Complete an ops excellence checklist

## Architecture

This topic’s control points and relationships are shown below.

![Production cluster](../assets/excalidraw/k8s-production-cluster.svg)

## Theory

### What it is

**Production Kubernetes excellence** is the operating standard that ties earlier modules into a coherent platform: GitOps delivery, hardened defaults, observability with SLOs, autoscaling with disruption budgets, tested backups, multi-cluster strategy, and FinOps visibility. It is less a new API than a checklist of non-negotiables that keep clusters boring — in the best sense — under real traffic.

### Why it matters

Individual features (HPA, RBAC, Ingress) fail in combination when teams skip integration: scale without PDBs, GitOps without policy, multi-cluster without identity federation. Excellence is how platform and SRE leaders review readiness before calling a service production. Certifications test pieces; production demands the whole system.

### How it works (mental model)

1. **Blast radius**: decide single cluster vs multi-cluster (prod/stage isolation, regional HA).
2. **Desired state**: everything durable lives in Git; controllers and GitOps reconcilers converge reality.
3. **Guardrails**: PSA, NetworkPolicy defaults, Kyverno/OPA Gatekeeper, image scanning.
4. **Operate**: SLOs on golden signals, HPA + PDB, node/pool strategy, upgrade waves.
5. **Economics**: right-size requests, bin-pack efficiently, use spot/preemptible where safe, turn down idle envs.

Review the checklist regularly; excellence decays without ownership.

### Key concepts / comparisons

| Domain | Excellence signal |
|--------|-------------------|
| Delivery | GitOps + progressive delivery |
| Security | Least privilege, PSA, policies |
| Reliability | SLOs, PDBs, tested DR |
| Scale | HPA/CA + capacity headroom |
| Cost | Requests accuracy, idle cleanup |

| Single cluster | Multi-cluster |
|----------------|---------------|
| Simpler ops | Stronger isolation / region HA |
| Larger blast radius | More federation complexity |

### Common pitfalls

- Multi-cluster sprawl without a platform story — N snowflake clusters.
- Policy theatre: engines installed, enforce mode never enabled.
- Over-requesting CPU “for safety” until bin-packing collapses and bills soar.
- Backups never restored; DR untested.
- Calling the platform done when observability still lacks actionable alerts.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-20 && cd ~/rebash-k8s/module-20
```

**Focus:** hands-on practice for Production Kubernetes Excellence

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Production Kubernetes Excellence"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-k8s/module-20 && cd ~/rebash-k8s/module-20
cat > excellence-checklist.md << 'EOF'
- [ ] GitOps for all envs
- [ ] PSA + NetworkPolicy defaults
- [ ] Image scan + immutable tags
- [ ] RBAC least privilege / no cluster-admin for apps
- [ ] HPA + PDB on critical Deployments
- [ ] Ingress TLS + cert automation
- [ ] Metrics, logs, traces wired
- [ ] etcd/workload backup tested quarterly
- [ ] Upgrade cadence documented
- [ ] Cost: requests ≈ usage; idle namespaces reviewed
- [ ] Multi-cluster: DR / region strategy written
EOF
kubectl get ns
kubectl get deploy -A | head
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-kubernetes/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-k8s/module-20/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Production Kubernetes Excellence** always combines:

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

!!! warning "Multi-cluster sprawl without a platform story — N snowflake clusters."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Policy theatre: engines installed, enforce mode never enabled."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Production Kubernetes Excellence changes as code and review them in pull requests
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

You can design and operate production Kubernetes platforms end to end — from first Pod to multi-cluster GitOps with security and DR.

## Interview Questions

1. How does **Production Kubernetes Excellence** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Kubernetes Capstone and Next Steps](kubernetes-capstone-and-next-steps.md)
- [Kubernetes Engineer path](../career-paths/kubernetes-engineer/index.md)

## References

- [Production environment checklist](https://kubernetes.io/docs/setup/best-practices/)
