---
title: "Pod Networking"
description: "Learn Kubernetes Pod networking — Pod IPs, same-node and cross-node communication, Pod CIDR, Cluster CIDR, overlay vs native routing, and production troubleshooting."
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
  - pods
  - cni
  - rebash-networking-mastery
comments: false
status: ready
---

# Pod Networking — How Pods Communicate in Kubernetes

> **Pod Networking** is the networking model that enables Kubernetes Pods to communicate with each other, regardless of whether they run on the same node or different nodes. Kubernetes follows a **flat network model**, where every Pod receives its own unique IP address and can communicate directly with every other Pod without requiring Network Address Translation (NAT). This networking model is implemented by the **Container Network Interface (CNI)** plugin and forms the foundation of Kubernetes communication. Every Kubernetes Administrator, DevOps Engineer, Platform Engineer, Site Reliability Engineer (SRE), Cloud Architect, and Network Engineer should understand Pod networking.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 11: Kubernetes Networking → Lesson 2</p>

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

<div markdown>**Lesson:** 2 of 9</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Kubernetes Pod networking
- Learn how Pods receive IP addresses
- Understand same-node and cross-node communication
- Explore Pod CIDR and Cluster CIDR
- Learn routing between Pods
- Troubleshoot Pod networking issues
- Design production-ready Kubernetes networking

---

# Prerequisites

Complete:

- Linux Networking
- Routing
- [Container Network Interface (CNI)](kubernetes-networking-fundamentals.md)
- Kubernetes Fundamentals

Basic understanding of:

- Network Namespaces
- Virtual Ethernet (veth)
- IP Routing

---

# Why Do We Need Pod Networking?

Imagine a Kubernetes cluster with:

- 20 Nodes
- 500 Pods
- 100 Services

Questions arise:

- How does one Pod reach another?
- What IP address does each Pod receive?
- How do Pods communicate across nodes?
- Who configures the routes?

These are solved through:

```text
Pod

Networking
```

---

# Kubernetes Networking Model

Kubernetes defines four core networking principles:

- Every Pod receives a unique IP address.
- Pods communicate directly without NAT.
- Nodes can communicate with all Pods.
- Pods can communicate across nodes.

These principles make application communication simple and consistent.

---

# What is Pod Networking?

Pod Networking is:

```text
The

Communication

Between

Pods

Using

Unique

Pod IPs
```

Every Pod behaves like an independent host on the cluster network.

---

# Pod IP Address

Each Pod receives:

```text
One

Unique

IP Address
```

Example:

```text
Frontend Pod

10.244.1.12
```

```text
Backend Pod

10.244.2.18
```

Applications communicate using these Pod IPs.

---

# Network Namespace

Each Pod runs inside its own:

```text
Network

Namespace
```

Every namespace contains:

- Network Interface
- Routing Table
- IP Address
- Loopback Interface

This provides network isolation between Pods.

---

# Virtual Ethernet (veth)

Each Pod connects to the node through a:

```text
veth Pair
```

Architecture:

```text
Pod

↓

veth

↓

Host Network
```

One interface resides inside the Pod.

The other resides on the Kubernetes node.

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

Assign Pod IP

↓

Configure Routes

↓

Pod Ready
```

Networking is configured before the Pod becomes available.

---

# Same-Node Communication

Pods on the same node communicate directly.

Example:

```text
Pod A

↓

Linux Bridge

↓

Pod B
```

Traffic never leaves the node.

Benefits:

- Low Latency
- High Performance

---

# Cross-Node Communication

Pods on different nodes communicate through the cluster network.

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

The CNI plugin configures routes or overlay tunnels to make this communication possible.

---

# Pod CIDR

Each node receives a range of Pod IP addresses.

Example:

Node 1

```text
10.244.1.0/24
```

Node 2

```text
10.244.2.0/24
```

Every Pod on a node receives an IP from that node's Pod CIDR.

---

# Cluster CIDR

The Cluster CIDR defines the complete Pod address space.

Example:

```text
10.244.0.0/16
```

Subdivided into:

```text
Node 1

10.244.1.0/24
```

```text
Node 2

10.244.2.0/24
```

```text
Node 3

10.244.3.0/24
```

---

# Routing Between Nodes

When Pod A communicates with Pod B:

```text
Pod

↓

Node Route

↓

Cluster Route

↓

Destination Node

↓

Destination Pod
```

Depending on the CNI, routing may use:

- Native Layer 3 Routing
- VXLAN
- Geneve
- IP-in-IP

---

# Overlay Networking

Some CNI plugins create an overlay network.

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

- Easy Deployment
- Works Across Existing Networks

Disadvantages:

- Encapsulation Overhead
- Slightly Higher Latency

---

# Native Routing

Other CNI plugins use direct routing.

```text
Pod

↓

Node Router

↓

Destination Node

↓

Pod
```

Advantages:

- Lower Latency
- Better Throughput
- Simpler Packet Processing

---

# Kubernetes DNS and Pod Communication

Although Pods can communicate using IP addresses:

```text
10.244.1.12
```

this is not recommended because Pod IPs are ephemeral.

Instead, Kubernetes Services and Domain Name System (DNS) provide stable endpoints.

---

# Pod Lifecycle and IP Addresses

When a Pod is deleted:

```text
Old Pod

↓

Deleted

↓

New Pod

↓

New IP Address
```

Applications should not depend on Pod IPs remaining constant.

---

# Kubernetes Perspective

Pods communicate:

- Same Node
- Different Nodes
- Across Availability Zones
- Across Regions (depending on cluster architecture)

The networking model remains consistent.

---

# Cloud Provider Perspective

## Amazon EKS

Uses:

- Amazon VPC CNI
- Calico
- Cilium

Pods may receive VPC IP addresses.

---

## Azure AKS

Uses:

- Azure CNI
- Cilium (in supported configurations)

Pod networking integrates with Azure Virtual Networks.

---

## Google GKE

Uses:

- VPC-native Networking
- Alias IPs
- Dataplane V2

Pods communicate using Google Cloud VPC networking.

---

# Enterprise Architecture

```text
Frontend Pod

↓

Service

↓

Backend Pod

↓

Database Pod
```

Communication occurs over the Kubernetes network without requiring manual route configuration by the application.

---

# Pod Communication Example

```text
Frontend

10.244.1.5

↓

Backend

10.244.2.8

↓

Database

10.244.3.4
```

Each Pod communicates using its assigned cluster IP.

---

# CLI Examples

Display Pods with IP addresses.

```bash
kubectl get pods -o wide
```

Describe a Pod.

```bash
kubectl describe pod nginx
```

View node information.

```bash
kubectl get nodes -o wide
```

View Pod CIDRs.

```bash
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.podCIDR}{"\n"}{end}'
```

---

# Common Networking Components

| Component | Purpose |
|----------|----------|
| Pod IP | Unique Pod Address |
| Pod CIDR | IP Range for One Node |
| Cluster CIDR | Cluster-wide Pod Address Space |
| Network Namespace | Pod Isolation |
| veth Pair | Pod-to-Host Connectivity |
| CNI Plugin | Network Configuration |

---

# Hands-on Lab

## Task 1

List Pods with IP addresses.

```bash
kubectl get pods -o wide
```

---

## Task 2

Display Pod details.

```bash
kubectl describe pod nginx
```

---

## Task 3

Display node Pod CIDRs.

```bash
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.podCIDR}{"\n"}{end}'
```

---

## Task 4

Deploy two Pods on the same node and verify connectivity using:

```bash
ping
```

---

## Task 5

Deploy two Pods on different nodes and verify communication.

---

## Task 6

Capture Pod traffic using:

```bash
tcpdump
```

inside the node.

---

## Task 7

Compare:

- Native Routing
- VXLAN Overlay

for a production Kubernetes cluster.

---

## Task 8

Draw a Kubernetes networking architecture showing:

- Pod
- Network Namespace
- veth Pair
- Node
- Cluster Network
- Remote Node
- Destination Pod

Explain how a packet travels from one Pod to another on a different node.

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

- Pod IP Address
- CNI Plugin Health
- Pod CIDR Configuration
- Node Routes
- Network Policies
- Firewall Rules
- CNI Logs

Workflow:

```text
Source Pod

↓

Network Namespace

↓

veth Pair

↓

Node

↓

Cluster Route

↓

Destination Node

↓

Destination Pod
```

---

# Pod Networking vs Traditional VM Networking

| Traditional VM | Kubernetes Pod |
|----------------|----------------|
| VM IP Address | Pod IP Address |
| Virtual NIC | veth Pair |
| Physical Network | CNI Plugin |
| Static Infrastructure | Dynamic Workloads |
| Manual Configuration | Automated Networking |

---

# Common Mistakes

❌ Using Pod IPs for long-term communication.

✅ Use Kubernetes Services for stable endpoints.

---

❌ Assuming Pod IPs never change.

✅ Design applications to tolerate Pod recreation.

---

❌ Ignoring Pod CIDR planning.

✅ Allocate sufficient address space before deployment.

---

❌ Overlooking CNI health.

✅ Monitor CNI components and networking logs.

---

❌ Debugging applications before checking networking.

✅ Verify Pod IPs, routes, and connectivity first.

---

# Best Practices

- Never hardcode Pod IP addresses.
- Use Services for stable communication.
- Plan Cluster CIDR and Pod CIDR carefully.
- Select a production-ready CNI plugin.
- Monitor Pod networking continuously.
- Enable Network Policies for security.
- Use observability tools to inspect network traffic.
- Test cross-node communication regularly.

---

# Interview Questions

## Beginner

1. What is Pod Networking?
2. Why does every Pod receive its own IP address?
3. What is a Pod CIDR?
4. What is a Cluster CIDR?

---

## Intermediate

1. Explain same-node and cross-node Pod communication.
2. Compare overlay networking and native routing.
3. Why should applications avoid using Pod IP addresses directly?
4. How does the CNI plugin enable Pod communication?

---

## Architect Level

1. Design networking for a large multi-node Kubernetes cluster.
2. Explain Pod networking across Availability Zones.
3. How would you troubleshoot intermittent Pod-to-Pod communication failures in production?

---

# Summary

In this lesson, you learned:

- Kubernetes Pod Networking
- Pod IP Addressing
- Network Namespaces
- veth Pairs
- Same-Node Communication
- Cross-Node Communication
- Pod CIDR
- Cluster CIDR
- Overlay Networking
- Native Routing

Pod networking is the foundation of communication within Kubernetes. Every Pod receives a unique IP address, enabling direct communication across the cluster without traditional NAT. Combined with CNI plugins, routing, and network namespaces, Kubernetes provides a simple yet powerful networking model that scales from small development clusters to large enterprise environments.

---

## Key Takeaways

- Every **Pod** receives a **unique IP address**.
- Pods communicate directly without traditional NAT.
- **Pod CIDR** defines the IP range for Pods on a node.
- **Cluster CIDR** defines the overall Pod address space.
- Same-node communication uses local networking, while cross-node communication relies on the CNI plugin.
- Applications should communicate through **Kubernetes Services** instead of relying on Pod IP addresses.

---

## What's Next?

**[Service Networking](service-networking.md)**

In the next lesson, you'll learn about **Service Networking**.

You'll explore:

- Kubernetes Services
- ClusterIP
- NodePort
- LoadBalancer
- ExternalName
- Service Discovery
- kube-proxy
- Traffic Flow

By the end of the lesson, you'll understand how Kubernetes Services provide stable networking for dynamic Pods and enable reliable communication within and outside the cluster.
