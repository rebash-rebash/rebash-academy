---
title: "Services and Cluster Networking"
description: "Expose Pods with ClusterIP, NodePort, LoadBalancer, ExternalName, and headless Services — EndpointSlices and kube-proxy for DevOps."
difficulty: intermediate
estimated_time: "45–60 min"
technology: kubernetes
category: kubernetes
module: "Module 5 · Services & Networking"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - kubernetes
  - services
  - networking
prerequisites:
  - kubernetes/workload-controllers-statefulset-daemonset-jobs
next:
  - kubernetes/ingress-and-external-access
related:
  - kubernetes/kubernetes-networking-deep-dive
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKA
  - CKAD
tags:
  - kubernetes
  - services
  - clusterip
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Services and Cluster Networking

## Overview

Create a ClusterIP Service that load-balances to Deployment Pods and explain NodePort, LoadBalancer, ExternalName, and headless modes.

A **Service** gives a stable virtual IP and DNS name. Selectors bind to Pod labels; **EndpointSlices** track backends. **kube-proxy** (or eBPF dataplanes) implement distribution.

This is a core tutorial in **Module 5 · Services & Networking** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Workload Controllers](workload-controllers-statefulset-daemonset-jobs.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Create ClusterIP Service  
- [ ] Contrast service types  
- [ ] Use DNS `svc.namespace.svc.cluster.local`  
- [ ] Inspect endpoints / EndpointSlices

## Architecture

This topic’s control points and relationships are shown below.

![Service networking](../assets/excalidraw/k8s-service-networking.svg)

## Theory

### What it is

A **Service** provides a stable virtual IP (ClusterIP) and DNS name in front of a changing set of Pods. You select Pods with labels; **EndpointSlices** track ready backends. Clients connect to the Service; the dataplane (**kube-proxy**, or eBPF alternatives) distributes connections to Pod IPs and ports.

### Why it matters

Pods are mortal — their IPs change on every reschedule. Applications and other microservices need a durable address. Services also abstract exposure modes: internal only, node ports, cloud load balancers, or external DNS aliases. Without Services, Deployments alone cannot offer reliable in-cluster discovery.

### How it works (mental model)

1. Create a Service with a selector and port mapping (`port` → `targetPort`).
2. Controllers populate EndpointSlices for matching ready Pods.
3. CoreDNS resolves `my-svc.my-ns.svc.cluster.local` (short names work inside the same namespace).
4. Traffic to the ClusterIP is load-balanced across backends.
5. Change Pods underneath freely; the Service name stays constant.

**Headless** Services (`clusterIP: None`) return Pod DNS/IPs directly — common with StatefulSets.

### Key concepts / comparisons

| Type | Typical use |
|------|-------------|
| ClusterIP | Default in-cluster access |
| NodePort | Lab / on-prem node exposure |
| LoadBalancer | Cloud LB integration |
| ExternalName | CNAME to external DNS |
| Headless | Direct Pod discovery |

| Piece | Role |
|-------|------|
| Service | Stable VIP + DNS |
| EndpointSlice | Backend inventory |
| kube-proxy / eBPF | Dataplane programming |

### Common pitfalls

- Selector labels that do not match the Pod template — empty endpoints, silent failures.
- Confusing Service `port` with container `containerPort` / `targetPort`.
- Expecting LoadBalancer to allocate an address on kind without metalLB or similar.
- Testing with `curl` to a Pod IP from outside the cluster network — use Service DNS from a debug Pod.
- Ignoring readiness: not-ready Pods should drop from endpoints; missing probes keep bad Pods in the pool.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-05 && cd ~/rebash-k8s/module-05
```

**Focus:** hands-on practice for Services and Cluster Networking

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-k8s/module-05 && cd ~/rebash-k8s/module-05
kubectl create deploy rebash-svc --image=nginx:alpine
kubectl expose deploy/rebash-svc --port=80 --target-port=80 --name=rebash-svc
kubectl get svc rebash-svc -o wide
kubectl get endpointslices -l kubernetes.io/service-name=rebash-svc
kubectl run curl --rm -it --restart=Never --image=curlimages/curl -- \
  curl -sI http://rebash-svc.default.svc.cluster.local/ | head -n 5
kubectl delete deploy/rebash-svc svc/rebash-svc
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-kubernetes/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-k8s/module-05/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Services and Cluster Networking** always combines:

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

!!! warning "Selector labels that do not match the Pod template — empty endpoints, silent failures."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Confusing Service `port` with container `containerPort` / `targetPort`."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Services and Cluster Networking changes as code and review them in pull requests
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

**Services and Cluster Networking** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Services and Cluster Networking** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Ingress and External Access](ingress-and-external-access.md)

## References

- [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
