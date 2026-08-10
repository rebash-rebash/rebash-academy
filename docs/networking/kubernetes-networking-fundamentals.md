---
title: "Container Network Interface (CNI)"
description: "Learn Container Network Interface (CNI) — Kubernetes Pod networking, veth pairs, IPAM, overlay vs native routing, and popular CNI plugins such as Calico, Flannel, and Cilium."
difficulty: advanced
estimated_time: "200 min"
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
  - cni
  - containers
  - rebash-networking-mastery
comments: false
status: ready
---

# Container Network Interface (CNI) — The Foundation of Kubernetes Networking

> **Container Network Interface (CNI)** is an open standard that defines how networking is configured for containers. In Kubernetes, the CNI plugin is responsible for **creating Pod network interfaces, assigning IP addresses, configuring routing, and enabling communication between Pods, Nodes, Services, and external networks**. Without a CNI plugin, Kubernetes Pods cannot communicate with each other. Every Kubernetes Administrator, DevOps Engineer, Platform Engineer, Site Reliability Engineer (SRE), Cloud Architect, and Network Engineer must understand how CNI works.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 11: Kubernetes Networking → Lesson 1</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Advanced</div>

<div markdown>**Reading Time:** 200 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Kubernetes Networking</div>

<div markdown>**Lesson:** 1 of 9</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the Container Network Interface (CNI)
- Learn how Kubernetes networking works
- Understand Pod IP assignment
- Explore CNI plugins
- Learn networking architectures
- Compare popular CNI implementations
- Troubleshoot Kubernetes networking

---

# Prerequisites

Complete:

- [Linux Network Namespaces](network-namespaces.md)
- Virtual Ethernet (veth)
- Routing
- [Cloud Networking](module-10-cloud-networking-summary.md)
- Kubernetes Fundamentals

Basic understanding of:

- Containers
- Linux Networking
- IP Routing

---

# Why Do We Need CNI?

Imagine a Kubernetes cluster with:

- 100 Nodes
- 2,000 Pods

Questions arise:

- How does each Pod receive an IP address?
- How do Pods communicate across nodes?
- Who creates virtual interfaces?
- How is routing configured?

The answer is:

```text
Container

Network

Interface

(CNI)
```

---

# What is CNI?

Container Network Interface is:

```text
A

Standard

For

Container

Networking
```

It defines how network plugins configure networking for containers.

CNI is maintained by the **Cloud Native Computing Foundation (CNCF)** as part of the broader cloud-native ecosystem.

---

# Kubernetes Networking Model

Kubernetes networking follows these principles:

- Every Pod gets its own IP address.
- Pods communicate directly without Network Address Translation (NAT).
- Pods on different nodes communicate seamlessly.
- Nodes communicate with Pods.
- External clients can access Services.

These requirements are implemented by the CNI plugin.

---

# High-Level Architecture

```text
Application

↓

Pod

↓

Network Namespace

↓

veth Pair

↓

CNI Plugin

↓

Node Network

↓

Cluster Network
```

---

# How CNI Works

When Kubernetes creates a Pod:

```text
Pod Created

↓

Container Runtime

↓

Calls CNI

↓

Create Network

↓

Assign IP

↓

Configure Routes

↓

Pod Ready
```

The kubelet invokes the container runtime, which in turn executes the configured CNI plugin.

---

# Pod Creation Workflow

```text
kubectl apply

↓

API Server

↓

Scheduler

↓

Node

↓

kubelet

↓

Container Runtime

↓

CNI Plugin

↓

Pod Running
```

The CNI plugin performs all required networking tasks before the Pod starts communicating.

---

# Responsibilities of CNI

A CNI plugin performs:

- Create Network Namespace
- Create veth Pair
- Assign IP Address
- Configure Routing
- Connect to Bridge or Overlay
- Configure Network Policies (plugin dependent)
- Clean Up Networking on Pod Deletion

---

# Network Namespace

Each Pod receives:

```text
Dedicated

Network

Namespace
```

Inside the namespace:

- Network Interfaces
- Routing Table
- Loopback Interface
- IP Address

are isolated from other Pods.

---

# Virtual Ethernet (veth)

A virtual Ethernet pair connects:

```text
Pod

↓

veth

↓

Node
```

One end stays inside the Pod namespace.

The other remains on the host node.

---

# IP Address Allocation

Every Pod receives:

```text
Unique

IP Address
```

Example:

```text
Pod A

10.244.1.5
```

```text
Pod B

10.244.2.8
```

Pods communicate directly using these IP addresses.

---

# Pod-to-Pod Communication

Example:

```text
Pod A

↓

Node A

↓

Cluster Network

↓

Node B

↓

Pod B
```

The CNI plugin configures the routing required for this communication.

---

# Overlay Networking

Some CNI plugins create overlay networks.

Example:

```text
Pod

↓

VXLAN Tunnel

↓

Remote Node

↓

Pod
```

Advantages:

- Simpler Cross-Node Networking
- Works Across Different Networks

Trade-off:

- Additional Encapsulation Overhead

---

# Native Routing

Some CNIs use direct Layer 3 routing.

Example:

```text
Pod

↓

Node Router

↓

Node Router

↓

Pod
```

Advantages:

- Higher Performance
- Lower Latency

Requires appropriate routing between nodes.

---

# Popular CNI Plugins

## Calico

Features:

- Layer 3 Routing
- Border Gateway Protocol (BGP)
- VXLAN
- Network Policies
- eBPF Support

Common in enterprise Kubernetes clusters.

---

## Flannel

Features:

- Simple Setup
- VXLAN Overlay
- Lightweight

Ideal for learning environments and smaller clusters.

---

## Cilium

Features:

- eBPF
- High Performance
- Advanced Security
- Observability
- Service Mesh Integration

Increasingly popular for production environments.

---

## Weave Net

Features:

- Overlay Networking
- Automatic Peer Discovery
- Encryption Support

Suitable for straightforward deployments.

---

## Antrea

Built on:

```text
Open vSwitch

(OVS)
```

Features:

- Network Policies
- Traffic Visibility
- Enterprise Networking

---

# CNI Comparison

| Plugin | Networking | Strength |
|---------|------------|----------|
| Calico | Routing / VXLAN | Enterprise Networking |
| Flannel | VXLAN | Simplicity |
| Cilium | eBPF | Performance & Security |
| Weave Net | Overlay | Easy Deployment |
| Antrea | OVS | Advanced Networking |

---

# Cloud Provider CNIs

## Amazon EKS

Common options:

- Amazon VPC CNI
- Calico
- Cilium

Pods can receive VPC IP addresses using the Amazon VPC CNI.

---

## Azure AKS

Supports:

- Azure CNI
- Kubenet (legacy in many scenarios)
- Cilium (depending on cluster configuration)

---

## Google GKE

Supports:

- GKE Dataplane V2 (built on Cilium/eBPF)
- VPC-native networking
- Alias IPs

---

# Enterprise Architecture

```text
Application

↓

Pod

↓

Network Namespace

↓

veth

↓

CNI Plugin

↓

Node

↓

Cluster Network

↓

Internet
```

The CNI plugin bridges the gap between Pods and the cluster network.

---

# Kubernetes Perspective

Without a CNI plugin:

```text
Pods

Cannot

Communicate
```

The CNI plugin is therefore an essential component of every Kubernetes cluster.

---

# CLI Examples

Display Pods.

```bash
kubectl get pods -o wide
```

Display Nodes.

```bash
kubectl get nodes -o wide
```

List CNI configuration.

```bash
ls /etc/cni/net.d/
```

List CNI binaries.

```bash
ls /opt/cni/bin/
```

View CNI Pods.

```bash
kubectl get pods -n kube-system
```

---

# Common CNI Components

| Component | Purpose |
|----------|----------|
| Network Namespace | Pod Isolation |
| veth Pair | Pod-to-Node Connection |
| IPAM | IP Address Management |
| Routing | Packet Forwarding |
| Overlay | Cross-Node Networking |
| Network Policy | Traffic Control |

---

# Hands-on Lab

## Task 1

List Kubernetes Pods.

```bash
kubectl get pods -o wide
```

---

## Task 2

View Node IP addresses.

```bash
kubectl get nodes -o wide
```

---

## Task 3

Inspect CNI configuration.

```bash
ls /etc/cni/net.d/
```

---

## Task 4

List installed CNI binaries.

```bash
ls /opt/cni/bin/
```

---

## Task 5

Identify the CNI plugin running in your cluster.

```bash
kubectl get pods -n kube-system
```

---

## Task 6

Deploy two Pods on different nodes and verify Pod-to-Pod communication using their IP addresses.

---

## Task 7

Compare:

- Calico
- Flannel
- Cilium

for an enterprise Kubernetes deployment.

---

## Task 8

Draw a Kubernetes networking diagram showing:

- Node
- Pod
- Network Namespace
- veth Pair
- CNI Plugin
- Cluster Network

Explain how packets travel from one Pod to another on a different node.

---

# Production Troubleshooting

Problem:

```text
Pod

Cannot

Reach

Another Pod
```

Check:

- Pod IP Assignment
- CNI Plugin Status
- Node Routes
- Network Policies
- Firewall Rules
- CNI Logs

Workflow:

```text
Pod

↓

Network Namespace

↓

veth

↓

CNI

↓

Node

↓

Remote Node

↓

Destination Pod
```

---

# CNI vs Docker Bridge

| Docker Bridge | Kubernetes CNI |
|---------------|----------------|
| Single Host | Multi-Node |
| Simple Bridge | Cluster Networking |
| Basic Networking | Advanced Networking |
| Docker-Specific | Kubernetes Standard |
| Limited Scalability | Enterprise Scale |

---

# Common Mistakes

❌ Assuming Kubernetes provides networking by itself.

✅ Install and configure a supported CNI plugin.

---

❌ Choosing a CNI without understanding networking requirements.

✅ Evaluate routing, performance, security, and policy needs.

---

❌ Ignoring Pod CIDR planning.

✅ Design Pod IP ranges before cluster deployment.

---

❌ Overlooking Network Policies.

✅ Implement least-privilege communication rules.

---

❌ Skipping CNI health monitoring.

✅ Monitor CNI components and logs regularly.

---

# Best Practices

- Select a CNI plugin that matches your production requirements.
- Plan Pod CIDR ranges before cluster deployment.
- Enable Network Policies for workload isolation.
- Monitor CNI plugin health continuously.
- Prefer native routing where appropriate for better performance.
- Evaluate eBPF-based networking for modern Kubernetes platforms.
- Keep CNI plugins updated with Kubernetes versions.

---

# Interview Questions

## Beginner

1. What is CNI?
2. Why does Kubernetes require a CNI plugin?
3. What is a veth pair?
4. What is a Network Namespace?

---

## Intermediate

1. Compare Calico, Flannel, and Cilium.
2. Explain how Pod networking works.
3. How does a Pod receive its IP address?
4. What is overlay networking?

---

## Architect Level

1. Design networking for a production Kubernetes cluster.
2. Explain how CNI enables communication across multiple nodes.
3. How would you troubleshoot Pod-to-Pod communication failures in a production environment?

---

# Summary

In this lesson, you learned:

- Container Network Interface (CNI)
- Kubernetes Networking Model
- Network Namespaces
- veth Pairs
- Pod IP Assignment
- Overlay Networking
- Native Routing
- Calico
- Flannel
- Cilium
- Enterprise Kubernetes Networking

CNI is the networking foundation of Kubernetes. It connects Pods to the cluster network by creating network namespaces, assigning IP addresses, configuring routing, and enabling secure communication between workloads. Different CNI plugins provide different capabilities, allowing organisations to choose the networking model that best fits their performance, security, and scalability requirements.

---

## Key Takeaways

- **CNI** is the standard interface for container networking in Kubernetes.
- Every Pod receives its own **network namespace** and **unique IP address**.
- **veth pairs** connect Pods to the host network.
- Popular CNI plugins include **Calico**, **Flannel**, **Cilium**, **Weave Net**, and **Antrea**.
- CNI plugins manage routing, IP allocation, and connectivity across Kubernetes clusters.
- Choosing the right CNI is critical for **performance, security, and scalability**.

---

## What's Next?

**[Pod Networking](pod-networking.md)**

In the next lesson, you'll learn about **Pod Networking**.

You'll explore:

- Pod IP Addressing
- Pod-to-Pod Communication
- Same-Node Networking
- Cross-Node Networking
- Pod CIDR
- Cluster CIDR
- Kubernetes Networking Best Practices

By the end of the lesson, you'll understand how Pods communicate across Kubernetes clusters and how the Kubernetes networking model enables seamless communication without traditional NAT between Pods.
