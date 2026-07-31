---
title: "Kubernetes Networking Fundamentals"
description: "Pod networking, CNI, Services (ClusterIP, NodePort, LoadBalancer), Ingress, Gateway API, CoreDNS, and NetworkPolicies for Cloud and DevOps engineers."
difficulty: intermediate
estimated_time: "60–75 min"
technology: networking
category: networking
module: "Module 14 · Kubernetes Networking"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - cloud-engineer
skills:
  - kubernetes-networking
  - cni
  - services
  - ingress
prerequisites:
  - networking/linux-networking-toolkit
  - networking/load-balancing-fundamentals
next:
  - networking/cloud-networking-vpc-and-subnets
related:
  - kubernetes/services-and-cluster-networking
interview: interview/networking
certifications:
  - CKA
  - CKAD
tags:
  - networking
  - kubernetes
  - cni
  - ingress
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Kubernetes Networking Fundamentals

## Overview

Explain how packets move between pods, Services, and Ingress/Gateway, and verify DNS and connectivity with `kubectl` and in-cluster tools.

Kubernetes networking answers four questions: How do pods get IPs? How do pods talk? How do clients find pods? How do you restrict traffic? This module covers CNI, Services, Ingress/Gateway API, CoreDNS, and NetworkPolicies — as required by the Networking course definition.

This is a core tutorial in **Module 14 · Kubernetes Networking** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- Comfortable with Modules 1–13 networking ideas  
- Access to a cluster (kind/minikube/k3s or cloud) preferred; theory-only readers can still complete validation checklists

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Describe pod networking and CNI’s role  
- [ ] Contrast ClusterIP, NodePort, and LoadBalancer  
- [ ] Explain Ingress vs Gateway API at a practical level  
- [ ] Query CoreDNS behaviour  
- [ ] State what NetworkPolicies allow/deny

## Architecture

This topic’s control points and relationships are shown below.

![Kubernetes networking overview](../assets/excalidraw/kubernetes-networking.svg)

## Theory

### Pod networking & CNI

Every pod gets an IP from the cluster network. The **CNI** plugin (Calico, Cilium, Flannel, cloud CNIs) wires interfaces, routes, and policy hooks.

### Services

| Type | Purpose |
|------|---------|
| ClusterIP | Stable virtual IP inside the cluster |
| NodePort | Expose on each node IP:port |
| LoadBalancer | Provision external LB (cloud) |

kube-proxy / dataplane implements service routing (iptables, IPVS, or eBPF).

### Ingress & Gateway API

- **Ingress** — L7 HTTP routing (host/path) via an Ingress controller  
- **Gateway API** — newer, more expressive, role-oriented APIs for the same job  

### CoreDNS

Cluster DNS for `service.namespace.svc.cluster.local` and optional external recursion.

### NetworkPolicies

Pod-level firewall rules (identity via labels). Default-allow unless a policy selects the pod — design carefully.

## Hands-on Lab

**Focus:** practise the core workflow for Kubernetes Networking Fundamentals

```bash
mkdir -p ~/rebash-networking/module-14
cd ~/rebash-networking/module-14
command -v kubectl >/dev/null || echo "Install kubectl to run cluster labs"
```

### Step 1 — API reachability

```bash
kubectl get nodes -o wide || echo "No cluster — continue with theory validation"
kubectl get ns
```

### Step 2 — Workloads & Services

```bash
kubectl get pods -A -o wide | head
kubectl get svc -A | head
```

### Step 3 — DNS

```bash
kubectl -n kube-system get pods -l k8s-app=kube-dns -o wide 2>/dev/null || \
kubectl -n kube-system get pods -l app.kubernetes.io/name=coredns -o wide
```

### Step 4 — Optional debug pod

```bash
kubectl run netcheck --rm -it --restart=Never --image=nicolaka/netshoot -- \
  bash -lc 'set -e; dig kubernetes.default.svc.cluster.local +short; curl -sI https://kubernetes.default.svc || true'
```

### Step 5 — Policy awareness

```bash
kubectl get networkpolicies -A || true
```

## Validation

- [ ] Explain CNI in one sentence  
- [ ] Contrast three Service types  
- [ ] Describe Ingress vs Service  
- [ ] Know where CoreDNS runs  
- [ ] Know NetworkPolicy default behaviour

## Code Walkthrough

Production practice for **Kubernetes Networking Fundamentals** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for networking as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Skipping fundamentals for Kubernetes Networking Fundamentals"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Kubernetes Networking Fundamentals"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Kubernetes Networking Fundamentals changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Checks |
|---------|--------|
| DNS fail in pod | CoreDNS pods, `/etc/resolv.conf`, NetworkPolicy |
| Service no endpoints | Selector vs pod labels |
| Ingress 502 | Upstream Service/Endpoints, probes |
| Pod not reachable | CNI, routes, policies, hostNetwork misconceptions |

## Summary

Kubernetes networking is still TCP/IP — with CNI, virtual Services, DNS, and optional L7 gateways. Debug with the same layered discipline as Linux hosts.

## Interview Questions

1. How does **Kubernetes Networking Fundamentals** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md)

## References

- [Kubernetes Network Model](https://kubernetes.io/docs/concepts/cluster-administration/networking/)  
- [Service](https://kubernetes.io/docs/concepts/services-networking/service/)  
- [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)  
- [Gateway API](https://gateway-api.sigs.k8s.io/)  
- [NetworkPolicies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
