---
title: "Kubernetes Networking Deep Dive"
description: "Understand CNI, CoreDNS, kube-proxy, NetworkPolicies, and service discovery DNS resolution for production Kubernetes."
difficulty: advanced
estimated_time: "45–60 min"
technology: kubernetes
category: kubernetes
module: "Module 11 · Networking Deep Dive"
career_paths:
  - kubernetes-engineer
  - platform-engineer
  - site-reliability-engineer
  - cloud-engineer
skills:
  - kubernetes
  - cni
  - dns
  - network-policy
prerequisites:
  - kubernetes/kubernetes-security-hardening
  - kubernetes/services-and-cluster-networking
next:
  - kubernetes/monitoring-and-logging-in-kubernetes
related:
  - networking/index
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKA
tags:
  - kubernetes
  - cni
  - coredns
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Kubernetes Networking Deep Dive

## Overview



Explain the Pod network (CNI), CoreDNS service discovery, kube-proxy modes, and how NetworkPolicies enforce east-west rules.

Every Pod gets an IP via **CNI** (Calico, Cilium, kindnet…). **CoreDNS** answers `svc.ns.svc.cluster.local`. **NetworkPolicies** are enforced by the CNI plugin — not by kube-apiserver alone.

This is a core tutorial in **Module 11 · Networking Deep Dive** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Services](services-and-cluster-networking.md) · [Security Hardening](kubernetes-security-hardening.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Name your cluster’s CNI  
- [ ] Resolve Service DNS from a debug Pod  
- [ ] Outline iptables vs IPVS vs eBPF  
- [ ] Write a simple NetworkPolicy



## Architecture



This topic’s control points and relationships are shown below.

![Service networking](../assets/excalidraw/k8s-service-networking.svg)



## Theory



### What it is

Kubernetes networking rests on a few guarantees: every Pod gets an IP; Pods can reach each other without NAT (within the cluster model); agents on nodes implement that fabric via a **CNI** plugin. **CoreDNS** provides service discovery. **kube-proxy** (iptables/IPVS) or eBPF dataplanes implement Services. **NetworkPolicies** express allow/deny rules enforced by the CNI — not by the API server alone.

### Why it matters

Most “it works on my laptop” failures in production are DNS, NetworkPolicy, or CNI MTU/routing issues. DevOps engineers who can name their CNI, query CoreDNS, and read EndpointSlices debug faster than those who only restart Pods. Security teams need NetworkPolicies that actually enforce.

### How it works (mental model)

1. CNI assigns Pod IPs and programmes routes/overlays/eBPF maps.
2. kubelet and runtime attach the Pod to the network namespace.
3. Services select Pods; EndpointSlices list ready backends; the dataplane DNAT/load-balances to Pod IPs.
4. Pods resolve `service.namespace.svc.cluster.local` via CoreDNS (kube-dns Service).
5. NetworkPolicy objects are watched by the CNI agent; non-matching traffic is dropped when policies select a Pod.

Flat Pod network + Services + DNS is the mental model; overlays and cloud routing are implementation details.

### Key concepts / comparisons

| Layer | Component |
|-------|-----------|
| Pod IP fabric | CNI (Calico, Cilium, kindnet, …) |
| Service VIP | kube-proxy / eBPF |
| DNS | CoreDNS |
| Policy | NetworkPolicy (+ CiliumNetworkPolicy etc.) |

| kube-proxy mode | Trait |
|-----------------|-------|
| iptables | Common default |
| IPVS | Better scale characteristics |
| eBPF (Cilium) | Often replaces kube-proxy |

### Common pitfalls

- Assuming NetworkPolicies work without a supporting CNI — they become no-ops.
- DNS failures from CoreDNS Pending/CrashLoop — check `kube-system` first.
- Debugging Service traffic without checking endpoints emptiness.
- Overlapping NetworkPolicies that unintentionally isolate CoreDNS (egress to DNS must remain).
- Confusing NodePort exposure with Pod network reachability from outside.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-11 && cd ~/rebash-k8s/module-11
```

**Focus:** Trace ClusterIP Service DNS and Pod-to-Pod connectivity

### Step 1 – Create two Pods and a Service

```bash
kubectl create namespace rebash-lab
kubectl -n rebash-lab run server --image=nginx:1.27-alpine --port=80 --labels=app=server
kubectl -n rebash-lab expose pod server --port=80 --name=server
kubectl -n rebash-lab run client --image=busybox:1.36 --restart=Never --command -- sleep 3600
kubectl -n rebash-lab wait --for=condition=Ready pod/server pod/client --timeout=90s
```

### Step 2 – Resolve DNS and curl across the Service

```bash
kubectl -n rebash-lab get svc server -o wide
kubectl -n rebash-lab exec client -- nslookup server.rebash-lab.svc.cluster.local
kubectl -n rebash-lab exec client -- wget -qO- http://server.rebash-lab.svc.cluster.local/ | head -n 5
kubectl -n rebash-lab get endpoints server -o yaml | head -n 30
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-k8s/module-11/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Kubernetes Networking Deep Dive** always combines:

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



!!! warning "Assuming NetworkPolicies work without a supporting CNI — they become no-ops."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "DNS failures from CoreDNS Pending/CrashLoop — check `kube-system` first."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Kubernetes Networking Deep Dive changes as code and review them in pull requests
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



**Kubernetes Networking Deep Dive** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. How does Pod networking typically work regarding IP addresses?
2. How does CoreDNS resolve a Service name inside a cluster?
3. What is the difference between ClusterIP, NodePort, and LoadBalancer?
4. How can NetworkPolicy restrict east-west traffic, and what must the CNI support?
5. What symptoms suggest a CNI or kube-proxy problem rather than an application bug?

!!! tip "Sample answer — question 2"
    Services get a stable DNS name like `name.namespace.svc.cluster.local` that resolves to the ClusterIP. kube-dns/CoreDNS answers these queries for in-cluster clients.

!!! tip "Sample answer — question 4"
    NetworkPolicy only enforces if the CNI implements it. Policies default-deny unused paths, allow needed namespaces/pods/ports, and should be tested so you do not lock out DNS or probes accidentally.



## Related Tutorials



- [Course overview](index.md)
- [Monitoring and Logging in Kubernetes](monitoring-and-logging-in-kubernetes.md)



## References



- [Cluster networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/) · [DNS for Services](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
