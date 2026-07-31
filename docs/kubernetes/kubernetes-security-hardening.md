---
title: "Kubernetes Security Hardening"
description: "Harden clusters with securityContexts, Pod Security Admission, NetworkPolicies, and image policy practices for CKS-level DevOps."
difficulty: advanced
estimated_time: "50–70 min"
technology: kubernetes
category: kubernetes
module: "Module 10 · Security"
career_paths:
  - kubernetes-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - kubernetes
  - security
  - network-policy
prerequisites:
  - kubernetes/rbac-and-kubernetes-security-basics
next:
  - kubernetes/kubernetes-networking-deep-dive
related:
  - docker/docker-security-hardening
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKS
tags:
  - kubernetes
  - psa
  - networkpolicy
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Kubernetes Security Hardening

## Overview

Run a Pod with a restrictive securityContext, enable Pod Security Admission labels on a namespace, and draft a default-deny NetworkPolicy pattern.

Defence in depth: RBAC + **securityContext** + **Pod Security Admission (PSA)** + **NetworkPolicy** + signed/scanned images + Secrets hygiene.

This is a core tutorial in **Module 10 · Security** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Set `runAsNonRoot`, drop capabilities  
- [ ] Label ns for PSA (`restricted`/`baseline`)  
- [ ] Explain NetworkPolicy default-deny  
- [ ] List image policy controls

## Architecture

This topic’s control points and relationships are shown below.

![RBAC](../assets/excalidraw/k8s-rbac-model.svg)

## Theory

### What it is

**Hardening** layers controls beyond basic RBAC. **securityContext** settings run containers as non-root, drop Linux capabilities, and disallow privilege escalation. **Pod Security Admission (PSA)** enforces baseline/restricted profiles per namespace. **NetworkPolicies** restrict Pod-to-Pod and egress traffic (enforced by the CNI). Image hygiene — digests, scanning, admission policies — reduces supply-chain risk. Secrets encryption and audit logging complete the picture.

### Why it matters

A cluster with open RBAC but privileged Pods and unrestricted east-west traffic is one CVE away from lateral movement. CKS-oriented DevOps treats defence in depth as normal: identity, workload, network, and supply chain each fail closed where practical.

### How it works (mental model)

1. **Workload**: Pod/container `securityContext` + PSA labels (`enforce=restricted` when apps allow).
2. **Network**: default-deny NetworkPolicy, then allow only needed ingress/egress.
3. **Identity**: dedicated SAs, no unnecessary secret mounts, short-lived tokens where possible.
4. **Supply chain**: pin digests, scan in CI, optional admission (Kyverno/OPA Gatekeeper) to block `:latest` or unsigned images.
5. Controllers still reconcile — hardening constrains *what* may run, not the reconcile loop itself.

PSA replaces the older PodSecurityPolicy API; learn labels, not PSP.

### Key concepts / comparisons

| Control | Layer |
|---------|-------|
| RBAC | API access |
| securityContext | Process privileges |
| PSA | Admission of Pod specs |
| NetworkPolicy | East-west / egress |
| Image policy | What may be pulled/run |

| PSA level | Strictness |
|-----------|------------|
| privileged | No restriction |
| baseline | Minimally opinionated |
| restricted | Hardened defaults |

### Common pitfalls

- Labelling `enforce=restricted` without fixing images that require root — mass Pending/reject.
- Writing NetworkPolicies when the CNI does not enforce them — false sense of safety.
- Dropping `ALL` capabilities but adding back dangerous ones casually.
- Leaving `hostNetwork` / `hostPID` enabled on ordinary apps.
- Scanning images once and never again — rebuild pipelines must re-scan.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-10-hard && cd ~/rebash-k8s/module-10-hard
```

**Focus:** hands-on practice for Kubernetes Security Hardening

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Kubernetes Security Hardening"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-k8s/module-10-hard && cd ~/rebash-k8s/module-10-hard
kubectl create ns rebash-sec
kubectl label ns rebash-sec pod-security.kubernetes.io/enforce=baseline --overwrite
cat > secure-pod.yaml << 'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: secure
  namespace: rebash-sec
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    seccompProfile: { type: RuntimeDefault }
  containers:
    - name: app
      image: nginxinc/nginx-unprivileged:alpine
      securityContext:
        allowPrivilegeEscalation: false
        capabilities: { drop: ["ALL"] }
        readOnlyRootFilesystem: true
      volumeMounts:
        - name: tmp
          mountPath: /tmp
  volumes:
    - name: tmp
      emptyDir: {}
EOF
kubectl apply -f secure-pod.yaml
kubectl get pod secure -n rebash-sec
kubectl delete ns rebash-sec
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-kubernetes/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-k8s/module-10-hard/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Kubernetes Security Hardening** always combines:

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

!!! warning "Labelling `enforce=restricted` without fixing images that require root — mass Pending/reje"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Writing NetworkPolicies when the CNI does not enforce them — false sense of safety."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Kubernetes Security Hardening changes as code and review them in pull requests
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

**Kubernetes Security Hardening** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Kubernetes Security Hardening** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Kubernetes Networking Deep Dive](kubernetes-networking-deep-dive.md)

## References

- [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/) · [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
