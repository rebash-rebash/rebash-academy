---
title: "ConfigMaps and Secrets"
description: "Inject configuration with ConfigMaps, Secrets, environment variables, and the Downward API for Kubernetes applications."
difficulty: intermediate
estimated_time: "40–55 min"
technology: kubernetes
category: kubernetes
module: "Module 8 · Configuration"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
skills:
  - kubernetes
  - configmaps
  - secrets
prerequisites:
  - kubernetes/persistent-volumes-and-storage
next:
  - kubernetes/resource-quotas-and-limit-ranges
related:
  - kubernetes/kubernetes-security-hardening
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKAD
  - CKS
tags:
  - kubernetes
  - configmap
  - secrets
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# ConfigMaps and Secrets

## Overview










Mount ConfigMaps and Secrets into a Pod (env and volume) and use Downward API for pod metadata — without baking config into images.

**ConfigMap** = non-sensitive config. **Secret** = sensitive data (still base64 in etcd — enable encryption at rest and prefer external secret stores in production).

This is a core tutorial in **Module 8 · Configuration** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites










- [Persistent Volumes and Storage](persistent-volumes-and-storage.md)

## Learning Objectives










By the end of this tutorial, you will be able to:

- [ ] Create ConfigMap / Secret  
- [ ] Inject via `envFrom` and volume mounts  
- [ ] Use Downward API fields  
- [ ] State Secret limitations

## Architecture










This topic’s control points and relationships are shown below.

![Architecture](../assets/excalidraw/k8s-architecture.svg)

## Theory










### What it is

**ConfigMaps** hold non-sensitive configuration (files, key/value settings). **Secrets** hold sensitive material (tokens, passwords, TLS keys). Both inject into Pods as environment variables or mounted files. The **Downward API** exposes Pod metadata (name, namespace, labels, resource values) without hard-coding. The goal is twelve-factor style config: images stay generic; environment-specific data lives in the cluster (or an external store).

### Why it matters

Baking config into images forces rebuilds for every environment and leaks secrets into registries. Separating config enables the same artefact across dev/stage/prod. Understanding Secret limitations matters for CKS-level security: etcd contents, RBAC read access, and encryption at rest are operational concerns, not optional polish.

### How it works (mental model)

1. Create ConfigMap/Secret objects (literals, files, or YAML).
2. Reference them from a Pod/Deployment via `env`, `envFrom`, or `volumes` + `volumeMounts`.
3. Kubelet materialises values into the container environment or filesystem.
4. Updates to ConfigMaps/Secrets mounted as volumes can appear as file changes (depending on projection); env vars typically need a Pod restart.
5. Downward API `fieldRef` / `resourceFieldRef` populate fields from the running Pod object.

Prefer external secret managers (cloud SM, Vault, ESO) for production credentials.

### Key concepts / comparisons

| Object | Use |
|--------|-----|
| ConfigMap | Non-sensitive config |
| Secret | Sensitive data (still base64 in API) |
| Downward API | Pod/cluster metadata injection |

| Injection | Pros | Cons |
|-----------|------|------|
| Environment variables | Simple | Restart to refresh; visible in process listings |
| Volume mounts | Good for files; can update | App must reload files |

### Common pitfalls

- Believing Secrets are encrypted by default — they are base64-encoded, not ciphertext, unless encryption at rest is enabled.
- Wide RBAC allowing `get secrets` cluster-wide.
- Huge ConfigMaps (1 MiB object limits) or embedding binaries.
- Committing Secret YAML with real credentials into Git.
- Expecting env-injected values to hot-reload after ConfigMap edits.

## Hands-on Lab



### Objective

Build and verify a working Kubernetes solution for **ConfigMaps and Secrets** that you can inspect, prove, and tear down safely.

### Prerequisites

- kubectl configured against a lab cluster (kind/minikube preferred)
- Cluster-admin or namespace-create rights in the lab cluster
- Writable workspace at `~/rebash-k8s/module-08`

### Lab environment

Workspace: `~/rebash-k8s/module-08`

Local kind/minikube or a dedicated sandbox cluster. Never target a shared production API server.

```bash
mkdir -p ~/rebash-k8s/module-08 && cd ~/rebash-k8s/module-08
```

### Real-world scenario

Your platform team is rolling out **ConfigMaps and Secrets** for a new microservice. You must apply the change in an isolated namespace, prove it works with kubectl, and leave evidence for the on-call handover.

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

- Applied a real cluster change for ConfigMaps and Secrets
- Used describe/Events for verification
- Destroyed lab resources cleanly

### Cleanup

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Keep ~/rebash-kubernetes/ for later tutorials
```

## Validation










- [ ] Lab commands run under `~/rebash-k8s/module-08/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough










Production practice for **ConfigMaps and Secrets** always combines:

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










!!! warning "Believing Secrets are encrypted by default — they are base64-encoded, not ciphertext, unle"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Wide RBAC allowing `get secrets` cluster-wide."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices










- Encode ConfigMaps and Secrets changes as code and review them in pull requests
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










**ConfigMaps and Secrets** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions








1. What is the difference between a ConfigMap and a Secret in Kubernetes?
2. How can applications consume ConfigMap and Secret data at runtime?
3. What happens to running Pods when you update a ConfigMap that is mounted as a volume?
4. Why should Secrets not be treated as strong encryption at rest by default, and what controls improve their security?
5. When would you prefer environment variables versus volume mounts for configuration?

!!! tip "Sample answer — question 2"
    Applications can inject keys as environment variables, mount them as files via volumes, or use the Kubernetes API. Environment variables suit simple scalars; volume mounts suit files and live updates for many volume-mounted ConfigMaps.

!!! tip "Sample answer — question 4"
    etcd may store Secrets only base64-encoded unless encryption at rest is enabled. Improve security with encryption providers, least-privilege RBAC, external secret managers, short-lived credentials, and avoiding logging Secret values.

## Related Tutorials










- [Course overview](index.md)
- [Resource Quotas and LimitRanges](resource-quotas-and-limit-ranges.md)

## References










- [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/) · [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
