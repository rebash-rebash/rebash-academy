---
title: "CoreDNS"
description: "Learn CoreDNS in Kubernetes — service discovery, DNS naming, ClusterIP and headless resolution, Corefile plugins, forwarding, and production DNS troubleshooting."
difficulty: advanced
estimated_time: "210 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 11 · Kubernetes Networking"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - kubernetes
  - coredns
  - dns
  - rebash-networking-mastery
comments: false
status: ready
---

# CoreDNS — DNS-Based Service Discovery in Kubernetes

> **CoreDNS** is the default **Domain Name System (DNS)** server used in Kubernetes to provide **service discovery and name resolution**. Instead of applications communicating using constantly changing Pod IP addresses, CoreDNS allows workloads to communicate using **stable DNS names**. It automatically creates DNS records for Kubernetes Services and Pods, enabling reliable communication across the cluster. Every Kubernetes Administrator, DevOps Engineer, Platform Engineer, Site Reliability Engineer (SRE), Cloud Architect, and Network Engineer should understand CoreDNS.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 11: Kubernetes Networking → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Advanced</div>

<div markdown>**Reading Time:** 210 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Kubernetes Networking</div>

<div markdown>**Lesson:** 6 of 9</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand CoreDNS
- Learn Kubernetes DNS architecture
- Understand Service Discovery
- Learn DNS record creation
- Configure DNS forwarding
- Troubleshoot Kubernetes DNS issues
- Design production-ready DNS architectures

---

# Prerequisites

Complete:

- DNS Fundamentals
- DNS Records
- DNS Resolution
- [Service Networking](service-networking.md)
- Kubernetes Fundamentals

Basic understanding of:

- DNS
- TCP/IP
- Kubernetes Services

---

# Why Do We Need CoreDNS?

Imagine an application with:

- Frontend Pods
- Backend Pods
- Database Pods

Pod IPs change whenever Pods are recreated.

Example:

```text
Backend Pod

10.244.2.15
```

After restart:

```text
Backend Pod

10.244.5.23
```

Applications cannot rely on changing IP addresses.

Instead, applications use:

```text
backend.default.svc.cluster.local
```

This is made possible by:

```text
CoreDNS
```

---

# What is CoreDNS?

CoreDNS is:

```text
The

DNS

Server

Inside

Kubernetes
```

It provides:

- Service Discovery
- Name Resolution
- DNS Forwarding
- External DNS Resolution

---

# Kubernetes DNS Architecture

```text
Application

↓

DNS Query

↓

CoreDNS

↓

Service

↓

Pod
```

Applications communicate using DNS names instead of IP addresses.

---

# How CoreDNS Works

When an application performs:

```text
backend.default.svc.cluster.local
```

CoreDNS:

```text
Receives Query

↓

Looks Up Service

↓

Returns ClusterIP
```

The application then connects to the Service.

---

# CoreDNS Workflow

```text
Application

↓

DNS Request

↓

CoreDNS

↓

Service Lookup

↓

ClusterIP

↓

Service

↓

Pods
```

This process is transparent to the application.

---

# CoreDNS Deployment

CoreDNS runs as Pods inside:

```text
kube-system
```

namespace.

Example:

```bash
kubectl get pods -n kube-system
```

Typical output:

```text
coredns-xxxxx
```

Two or more replicas are usually deployed for high availability.

---

# Service Discovery

Every Kubernetes Service automatically receives:

```text
DNS Name
```

Example:

```text
frontend.default.svc.cluster.local
```

Applications use this name instead of Pod IP addresses.

---

# DNS Naming Convention

A fully qualified Service name follows:

```text
service-name

↓

namespace

↓

svc

↓

cluster.local
```

Example:

```text
api.production.svc.cluster.local
```

---

# Namespace Awareness

Services with the same name can exist in different namespaces.

Example:

```text
frontend.dev.svc.cluster.local
```

```text
frontend.prod.svc.cluster.local
```

CoreDNS resolves each name correctly.

---

# DNS Resolution Process

Application:

```text
curl backend
```

↓

Resolver expands:

```text
backend.default.svc.cluster.local
```

↓

CoreDNS

↓

Returns:

```text
10.96.15.20
```

↓

Application connects to the Service.

---

# ClusterIP Resolution

Example:

```text
backend.default.svc.cluster.local

↓

10.96.20.15
```

CoreDNS returns the Service ClusterIP rather than individual Pod IPs.

---

# Headless Service Resolution

Headless Services use:

```yaml
clusterIP: None
```

Instead of returning one IP:

```text
10.244.1.5
```

```text
10.244.2.8
```

```text
10.244.3.4
```

CoreDNS returns all Pod IP addresses.

Useful for:

- StatefulSets
- Databases
- Distributed Systems

---

# External DNS Resolution

If the requested domain is not inside Kubernetes:

```text
google.com
```

CoreDNS forwards the request to:

```text
Upstream

DNS

Server
```

such as the node's configured resolver or enterprise DNS infrastructure.

---

# Corefile

CoreDNS configuration is stored in:

```text
ConfigMap

↓

coredns
```

View configuration:

```bash
kubectl -n kube-system get configmap coredns -o yaml
```

The configuration is defined in the **Corefile**.

---

# Common CoreDNS Plugins

CoreDNS uses plugins to extend functionality.

Popular plugins include:

| Plugin | Purpose |
|----------|----------|
| kubernetes | Kubernetes Service Discovery |
| forward | Forward External DNS Queries |
| cache | Cache DNS Responses |
| health | Health Endpoint |
| ready | Readiness Endpoint |
| reload | Reload Configuration |
| errors | Error Logging |
| prometheus | Metrics |

---

# DNS Cache

CoreDNS caches responses.

Benefits:

- Faster Resolution
- Reduced Upstream Queries
- Improved Performance

Applications receive quicker DNS responses.

---

# Enterprise Architecture

```text
Frontend

↓

CoreDNS

↓

Backend Service

↓

Backend Pods

↓

Database Service

↓

Database Pods
```

Every application communicates using DNS names.

---

# Kubernetes Perspective

CoreDNS resolves:

- Services
- Pods (when enabled)
- Headless Services
- External Domains

It is one of the core system components of Kubernetes.

---

# Cloud Provider Perspective

## Amazon EKS

CoreDNS runs by default.

Integrated with:

- Amazon VPC CNI
- Kubernetes Services

---

## Azure AKS

CoreDNS is installed automatically.

Works with:

- Azure CNI
- Kubernetes Service Discovery

---

## Google GKE

CoreDNS provides DNS resolution for:

- Services
- Pods
- VPC-native clusters

Managed automatically by GKE.

---

# Production DNS Flow

```text
Application

↓

CoreDNS

↓

Service

↓

ClusterIP

↓

kube-proxy

↓

Pod
```

Every service request begins with DNS resolution.

---

# CLI Examples

List CoreDNS Pods.

```bash
kubectl get pods -n kube-system
```

Describe CoreDNS Pods.

```bash
kubectl describe pod -n kube-system
```

View CoreDNS logs.

```bash
kubectl logs -n kube-system deployment/coredns
```

View CoreDNS configuration.

```bash
kubectl get configmap coredns -n kube-system -o yaml
```

Test DNS resolution.

```bash
kubectl exec -it busybox -- nslookup kubernetes.default
```

---

# Common CoreDNS Components

| Component | Purpose |
|-----------|----------|
| CoreDNS | DNS Server |
| Corefile | Configuration |
| Kubernetes Plugin | Service Discovery |
| Cache | Performance |
| Forward Plugin | External DNS |
| ClusterIP | Service Resolution |

---

# Hands-on Lab

## Task 1

List CoreDNS Pods.

```bash
kubectl get pods -n kube-system
```

---

## Task 2

View CoreDNS logs.

```bash
kubectl logs -n kube-system deployment/coredns
```

---

## Task 3

Display the CoreDNS ConfigMap.

```bash
kubectl get configmap coredns -n kube-system -o yaml
```

---

## Task 4

Deploy a BusyBox Pod and test:

```bash
nslookup kubernetes.default
```

---

## Task 5

Create a Service and verify that CoreDNS resolves its DNS name.

---

## Task 6

Deploy a Headless Service and observe that multiple Pod IPs are returned.

---

## Task 7

Configure DNS forwarding to an enterprise DNS server in a test environment.

---

## Task 8

Draw a Kubernetes DNS architecture showing:

- Application Pod
- CoreDNS
- Service
- ClusterIP
- kube-proxy
- Backend Pods
- External DNS Server

Explain how the request:

```text
backend.default.svc.cluster.local
```

is resolved from the application to the destination Service.

---

# Production Troubleshooting

Problem:

```text
Application

Cannot

Resolve

Service Name
```

Check:

- CoreDNS Pods
- CoreDNS Logs
- CoreDNS ConfigMap
- Service Existence
- Namespace
- DNS Policies
- Network Policies
- Container Network Interface (CNI) Connectivity

Workflow:

```text
Application

↓

DNS Query

↓

CoreDNS

↓

Service

↓

ClusterIP

↓

Pod
```

---

# CoreDNS vs Traditional DNS

| Traditional DNS | CoreDNS |
|-----------------|----------|
| Internet Domains | Kubernetes Services |
| Static Records | Dynamic Records |
| Manual Updates | Automatic Discovery |
| External Infrastructure | Cluster Internal |
| General Purpose | Kubernetes Native |

---

# Common Mistakes

❌ Using Pod IPs instead of Service names.

✅ Always communicate through Service DNS names.

---

❌ Modifying the Corefile without validation.

✅ Test configuration changes before production rollout.

---

❌ Ignoring DNS caching behaviour.

✅ Consider cache expiration during troubleshooting.

---

❌ Assuming CoreDNS resolves every Pod by default.

✅ Understand the cluster's DNS configuration and policies.

---

❌ Forgetting namespace-qualified names.

✅ Use fully qualified names when accessing Services across namespaces.

---

# Best Practices

- Always access workloads using Service DNS names.
- Deploy multiple CoreDNS replicas.
- Monitor DNS latency and error rates.
- Enable Prometheus metrics for CoreDNS.
- Keep the CoreDNS configuration simple.
- Protect CoreDNS using Network Policies.
- Test DNS resolution after every cluster upgrade.
- Avoid hardcoding IP addresses in applications.

---

# Interview Questions

## Beginner

1. What is CoreDNS?
2. Why is CoreDNS required in Kubernetes?
3. What is Service Discovery?
4. What is a ClusterIP?

---

## Intermediate

1. Explain how Kubernetes DNS resolution works.
2. What is the Corefile?
3. Compare CoreDNS with traditional DNS servers.
4. How does a Headless Service affect DNS resolution?

---

## Architect Level

1. Design a highly available DNS architecture for Kubernetes.
2. Explain how CoreDNS integrates with Services and kube-proxy.
3. How would you troubleshoot intermittent DNS failures in a production Kubernetes cluster?

---

# Summary

In this lesson, you learned:

- CoreDNS
- Kubernetes DNS Architecture
- Service Discovery
- DNS Naming Convention
- ClusterIP Resolution
- Headless Services
- DNS Forwarding
- Corefile
- CoreDNS Plugins
- Production DNS Troubleshooting

CoreDNS is the DNS foundation of Kubernetes. It provides automatic service discovery, dynamic DNS records, and seamless name resolution for applications running inside the cluster. By abstracting changing Pod IP addresses behind stable DNS names, CoreDNS enables reliable communication, simplifies application development, and supports scalable cloud-native architectures.

---

## Key Takeaways

- **CoreDNS** is the default DNS server in Kubernetes.
- Every **Service** automatically receives a DNS name.
- Applications should communicate using **Service DNS names**, not Pod IP addresses.
- **Headless Services** return individual Pod IP addresses instead of a ClusterIP.
- CoreDNS uses plugins for Kubernetes integration, caching, forwarding, and monitoring.
- High availability, monitoring, and careful configuration are essential for production DNS services.

---

## What's Next?

**[kube-proxy](kube-proxy.md)**

In the next lesson, you'll learn about **kube-proxy**.

You'll explore:

- What kube-proxy is
- Service Networking
- iptables Mode
- IPVS Mode
- Packet Forwarding
- Load Balancing
- Traffic Flow

By the end of the lesson, you'll understand how kube-proxy implements Kubernetes Service networking and routes traffic efficiently between Services and Pods.
