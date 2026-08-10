---
title: "kube-proxy"
description: "Learn kube-proxy — Kubernetes Service routing, iptables and IPVS modes, EndpointSlices, load balancing, and production Service networking troubleshooting."
difficulty: advanced
estimated_time: "220 min"
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
  - kube-proxy
  - services
  - rebash-networking-mastery
comments: false
status: ready
---

# kube-proxy — The Traffic Router for Kubernetes Services

> **kube-proxy** is a Kubernetes networking component that runs on every cluster node and implements **Service networking**. It is responsible for routing traffic from **Kubernetes Services** to the appropriate backend Pods by configuring the node's networking stack using **iptables**, **IPVS**, or **nftables** (depending on the operating system and Kubernetes configuration). Although kube-proxy does not forward packets itself, it programs the operating system's packet filtering and routing rules so that traffic reaches the correct destination. Every Kubernetes Administrator, DevOps Engineer, Platform Engineer, Site Reliability Engineer (SRE), Cloud Architect, and Network Engineer should understand how kube-proxy works.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 11: Kubernetes Networking → Lesson 7</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Advanced</div>

<div markdown>**Reading Time:** 220 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Kubernetes Networking</div>

<div markdown>**Lesson:** 7 of 9</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand kube-proxy
- Learn how Kubernetes Services work internally
- Compare iptables and IPVS modes
- Understand packet forwarding
- Learn Service load balancing
- Troubleshoot Service networking
- Design scalable Kubernetes networking

---

# Prerequisites

Complete:

- [CNI](kubernetes-networking-fundamentals.md)
- [Pod Networking](pod-networking.md)
- [Service Networking](service-networking.md)
- [CoreDNS](coredns.md)
- Linux Networking

Basic understanding of:

- iptables
- TCP/IP
- Routing

---

# Why Do We Need kube-proxy?

Imagine a Kubernetes Service:

```text
frontend-service

↓

Pod A
```

```text
↓

Pod B
```

```text
↓

Pod C
```

Questions:

- Which Pod receives the request?
- How is traffic distributed?
- How does the Service IP reach the Pods?

The answer is:

```text
kube-proxy
```

---

# What is kube-proxy?

kube-proxy is:

```text
The

Service

Traffic

Manager

Of

Kubernetes
```

It watches the Kubernetes API Server for changes to:

- Services
- Endpoints
- EndpointSlices

and updates the node's networking rules accordingly.

---

# High-Level Architecture

```text
Client

↓

ClusterIP

↓

kube-proxy

↓

Pod A
```

```text
↓

Pod B
```

```text
↓

Pod C
```

Traffic is transparently forwarded to one of the healthy backend Pods.

---

# How kube-proxy Works

Workflow:

```text
Service Created

↓

API Server

↓

kube-proxy

↓

Configure Node Rules

↓

Traffic Ready
```

kube-proxy continuously synchronizes networking rules with the current cluster state.

---

# kube-proxy Architecture

Runs on:

```text
Every

Kubernetes

Node
```

Typically deployed as a:

```text
DaemonSet
```

Each node has its own kube-proxy instance.

---

# Traffic Flow

```text
Application

↓

Service IP

↓

Node

↓

kube-proxy

↓

Selected Pod
```

Applications simply connect to the Service.

kube-proxy handles the routing.

---

# Service Load Balancing

Given:

```text
Service
```

↓

```text
Pod 1
```

↓

```text
Pod 2
```

↓

```text
Pod 3
```

kube-proxy selects one healthy Pod based on the configured networking mode.

---

# kube-proxy Modes

kube-proxy supports:

- iptables
- IPVS
- nftables (supported on newer Linux systems and Kubernetes versions)
- Userspace (legacy and no longer recommended)

---

# iptables Mode

The default mode in many Kubernetes deployments.

Workflow:

```text
Packet

↓

iptables Rule

↓

Destination Pod
```

Advantages:

- Simple
- Stable
- Widely Supported

Disadvantages:

- Rule lookup becomes less efficient as the number of Services grows.

---

# IPVS Mode

Uses the Linux IP Virtual Server subsystem.

Workflow:

```text
Packet

↓

IPVS Table

↓

Destination Pod
```

Advantages:

- Higher Performance
- Better Scalability
- Efficient Connection Handling

Recommended for:

- Large Kubernetes Clusters
- High Traffic Environments

---

# nftables Mode

Modern Linux distributions increasingly support:

```text
nftables
```

Benefits:

- Modern packet filtering framework
- Improved rule management
- Better maintainability

Support depends on Kubernetes version, operating system, and configuration.

---

# Userspace Mode

Early Kubernetes versions supported:

```text
Userspace Proxy
```

Characteristics:

- Slower
- Higher Overhead
- Mostly obsolete

Modern clusters generally use iptables or IPVS.

---

# Service Routing

Example:

```text
ClusterIP

10.96.10.20

↓

Pod

10.244.1.8
```

The application only knows:

```text
10.96.10.20
```

kube-proxy performs the translation.

---

# Endpoint Updates

Suppose:

```text
Pod B

↓

Deleted
```

Kubernetes updates:

```text
EndpointSlice
```

↓

kube-proxy updates:

```text
Routing Rules
```

Traffic immediately stops flowing to the removed Pod.

---

# Session Affinity

By default:

```text
Client

↓

Any Healthy Pod
```

Optionally:

```text
Client

↓

Same Pod
```

using:

```yaml
sessionAffinity: ClientIP
```

Useful for stateful applications.

---

# kube-proxy and CoreDNS

Request flow:

```text
Application

↓

CoreDNS

↓

ClusterIP

↓

kube-proxy

↓

Pod
```

CoreDNS resolves the Service name.

kube-proxy routes traffic to the backend Pods.

---

# kube-proxy and CNI

Responsibilities:

**Container Network Interface (CNI)**

- Pod Networking
- IP Assignment
- Routing Between Nodes

**kube-proxy**

- Service Networking
- ClusterIP Routing
- Load Balancing

Together they provide complete Kubernetes networking.

---

# Enterprise Architecture

```text
Internet

↓

Ingress

↓

Service

↓

kube-proxy

↓

Frontend Pods

↓

Backend Service

↓

kube-proxy

↓

Backend Pods

↓

Database Service

↓

kube-proxy

↓

Database Pods
```

Every Service request passes through kube-proxy.

---

# Kubernetes Perspective

kube-proxy enables:

- ClusterIP Services
- NodePort Services
- LoadBalancer Services
- Session Affinity
- Service Discovery Integration

Without kube-proxy (or an alternative implementation), Kubernetes Services cannot function correctly.

---

# Cloud Provider Perspective

## Amazon EKS

Uses:

- kube-proxy
- Amazon VPC CNI

Can also integrate with eBPF-based networking solutions.

---

## Azure AKS

Uses:

- kube-proxy
- Azure CNI

Optimized for Azure networking.

---

## Google GKE

Uses:

- kube-proxy in standard configurations
- Dataplane V2 can replace parts of kube-proxy functionality using eBPF

---

# Production Traffic Flow

```text
Client

↓

DNS

↓

ClusterIP

↓

kube-proxy

↓

EndpointSlice

↓

Pod
```

Every Service request follows this sequence.

---

# CLI Examples

List kube-proxy Pods.

```bash
kubectl get pods -n kube-system
```

View kube-proxy logs.

```bash
kubectl logs -n kube-system daemonset/kube-proxy
```

Describe kube-proxy.

```bash
kubectl describe daemonset kube-proxy -n kube-system
```

View Services.

```bash
kubectl get svc
```

View EndpointSlices.

```bash
kubectl get endpointslices
```

---

# Common kube-proxy Components

| Component | Purpose |
|-----------|----------|
| ClusterIP | Virtual Service IP |
| kube-proxy | Service Traffic Routing |
| EndpointSlice | Backend Discovery |
| iptables | Packet Rules |
| IPVS | High-Performance Load Balancing |
| DaemonSet | Runs kube-proxy on Every Node |

---

# Hands-on Lab

## Task 1

List kube-proxy Pods.

```bash
kubectl get pods -n kube-system
```

---

## Task 2

View kube-proxy logs.

```bash
kubectl logs -n kube-system daemonset/kube-proxy
```

---

## Task 3

List Kubernetes Services.

```bash
kubectl get svc
```

---

## Task 4

Display EndpointSlices.

```bash
kubectl get endpointslices
```

---

## Task 5

Inspect iptables rules on a Kubernetes node.

```bash
sudo iptables -t nat -L
```

---

## Task 6

Determine whether kube-proxy is running in iptables or IPVS mode.

---

## Task 7

Deploy multiple backend Pods and observe traffic distribution through a ClusterIP Service.

---

## Task 8

Draw a Kubernetes Service networking architecture including:

- Client
- CoreDNS
- Service
- ClusterIP
- kube-proxy
- EndpointSlice
- Backend Pods

Explain how a request reaches the selected Pod.

---

# Production Troubleshooting

Problem:

```text
Service

Not

Reachable
```

Check:

- Service
- EndpointSlices
- kube-proxy
- Pod Health
- Network Policies
- CoreDNS
- CNI Plugin
- Node Connectivity

Workflow:

```text
Application

↓

CoreDNS

↓

ClusterIP

↓

kube-proxy

↓

EndpointSlice

↓

Pod
```

---

# iptables vs IPVS

| iptables | IPVS |
|----------|------|
| Packet Filtering Rules | Virtual Server Framework |
| Simpler | More Scalable |
| Good for Small/Medium Clusters | Better for Large Clusters |
| Widely Used | Higher Performance |
| Linear Rule Evaluation | Efficient Lookup Structures |

---

# kube-proxy vs CNI

| kube-proxy | CNI |
|------------|-----|
| Service Networking | Pod Networking |
| ClusterIP Routing | Pod IP Assignment |
| Load Balancing | Cross-Node Connectivity |
| Watches Services | Configures Network Interfaces |
| Works at Service Layer | Works at Pod Layer |

---

# Common Mistakes

❌ Assuming kube-proxy assigns Pod IPs.

✅ Pod IPs are assigned by the CNI plugin.

---

❌ Ignoring EndpointSlices during troubleshooting.

✅ Verify backend endpoints first.

---

❌ Using Userspace mode in production.

✅ Prefer IPVS or iptables.

---

❌ Assuming kube-proxy is a packet-forwarding application.

✅ It programs kernel networking rules rather than forwarding packets directly.

---

❌ Overlooking kube-proxy logs.

✅ Review logs when diagnosing Service connectivity issues.

---

# Best Practices

- Prefer **IPVS** for large production clusters.
- Monitor kube-proxy health continuously.
- Keep EndpointSlices synchronized.
- Use readiness probes to prevent routing to unhealthy Pods.
- Monitor Service latency and connection failures.
- Keep kube-proxy updated with Kubernetes releases.
- Consider eBPF-based dataplanes where appropriate.

---

# Interview Questions

## Beginner

1. What is kube-proxy?
2. Why is kube-proxy required?
3. What is a ClusterIP?
4. What is an EndpointSlice?

---

## Intermediate

1. Compare iptables and IPVS modes.
2. How does kube-proxy implement Service networking?
3. What happens when a backend Pod is deleted?
4. How does kube-proxy interact with CoreDNS?

---

## Architect Level

1. Design Service networking for a high-scale Kubernetes platform.
2. Compare kube-proxy with eBPF-based Service implementations.
3. How would you troubleshoot intermittent Service connectivity failures in production?

---

# Summary

In this lesson, you learned:

- kube-proxy
- Service Routing
- ClusterIP
- EndpointSlices
- iptables
- IPVS
- nftables
- Session Affinity
- Service Load Balancing
- Production Troubleshooting

kube-proxy is a core Kubernetes networking component that implements Service networking by programming the node's networking stack. It enables stable Service access, distributes traffic across healthy Pods, and keeps routing rules synchronized with the current cluster state, allowing applications to communicate reliably despite constantly changing Pods.

---

## Key Takeaways

- **kube-proxy** implements Kubernetes Service networking.
- It runs on **every node** as a DaemonSet.
- kube-proxy watches **Services**, **Endpoints**, and **EndpointSlices**.
- **iptables** is widely used, while **IPVS** provides better scalability and performance.
- kube-proxy works alongside **CoreDNS** and the **CNI plugin** to provide complete Kubernetes networking.
- Modern Kubernetes environments increasingly adopt **eBPF-based dataplanes** to optimize or replace parts of kube-proxy functionality.

---

## What's Next?

**[Service Mesh](service-mesh.md)**

In the next lesson, you'll learn about **Service Mesh**.

You'll explore:

- What a Service Mesh is
- Sidecar Proxy Architecture
- Data Plane and Control Plane
- Traffic Management
- Mutual TLS (mTLS)
- Observability
- Popular Service Mesh platforms such as Istio and Linkerd

By the end of the lesson, you'll understand how Service Mesh extends Kubernetes networking with advanced traffic control, security, and observability for microservices.
