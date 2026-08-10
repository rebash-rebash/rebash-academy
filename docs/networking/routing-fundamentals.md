---
title: "Routing Basics"
description: "Learn routing fundamentals — routers, routing tables, next-hop forwarding, default gateways, longest prefix match, and Linux routing commands."
difficulty: beginner
estimated_time: "90 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 5 · Routing"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - routing
  - ip-route
  - gateway
  - rebash-networking-mastery
comments: false
status: ready
---

# Routing Basics — Understanding How Routers Connect Networks

> **Routing** is the process of forwarding packets between different networks. Unlike switches, which forward Ethernet frames using **MAC addresses**, routers make forwarding decisions using **IP addresses** and **routing tables**. Every time you access a website, connect to a cloud service, communicate between subnets, or browse the Internet, routers determine the best path for your packets. Routing is the foundation of enterprise networking, cloud computing, data centres, and the Internet. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand routing fundamentals.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 5: Routing → Lesson 1</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Routing</div>

<div markdown>**Lesson:** 1 of 10</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand routing fundamentals
- Learn the role of routers
- Understand routing tables
- Learn how packets are forwarded
- Understand next-hop routing
- Learn direct and indirect routing
- Apply routing concepts in enterprise and cloud environments

---

# Prerequisites

Complete:

- Module 1: Networking Fundamentals
- Module 2: IPv4 Addressing
- Module 3: IPv6
- Module 4: Switching

---

# Why Learn Routing?

Imagine two computers located in different networks.

Computer A:

```text
192.168.10.100
```

Computer B:

```text
192.168.20.50
```

Since they belong to different networks:

```text
Direct Communication

❌ Not Possible
```

A router is required.

---

# What is Routing?

Routing is the process of moving packets from one network to another.

Example:

```text
Laptop

↓

Router

↓

Internet

↓

Web Server
```

The router determines the best path toward the destination.

---

# What is a Router?

A **Router** is a **Layer 3 (Network Layer)** device.

Its primary responsibilities are:

- Connect Different Networks
- Forward Packets
- Maintain Routing Tables
- Select Best Paths
- Separate Broadcast Domains

---

# Switch vs Router

| Switch | Router |
|---------|---------|
| Layer 2 | Layer 3 |
| Uses MAC Addresses | Uses IP Addresses |
| Forwards Frames | Routes Packets |
| Connects Devices in Same Network | Connects Different Networks |

---

# When is Routing Required?

Routing is needed whenever traffic must leave the local network.

Examples:

- Different Virtual Local Area Networks (VLANs)
- Different Subnets
- Branch Offices
- Cloud Networks
- Internet Access

---

# Packet Journey

Suppose a user accesses:

```text
www.example.com
```

The packet travels:

```text
Application

↓

TCP

↓

IP Packet

↓

Default Gateway

↓

Router

↓

Internet

↓

Destination
```

Every router along the path forwards the packet closer to its destination.

---

# Routing Table

A router makes decisions using a:

```text
Routing Table
```

Example:

| Destination Network | Next Hop |
|---------------------|----------|
| 192.168.10.0/24 | Direct |
| 192.168.20.0/24 | Router A |
| 10.0.0.0/8 | Router B |
| 0.0.0.0/0 | Internet Gateway |

---

# Directly Connected Network

Example:

Router Interface:

```text
192.168.10.1/24
```

Any destination inside:

```text
192.168.10.0/24
```

is reached directly.

No additional router is required.

---

# Indirect Network

Suppose the destination is:

```text
172.16.50.20
```

Not directly connected.

Router:

```text
Lookup Routing Table

↓

Find Next Hop

↓

Forward Packet
```

---

# Next Hop

The **Next Hop** is the next router that should receive the packet.

Example:

```text
Destination

10.10.10.0/24

↓

Next Hop

192.168.1.2
```

The packet moves from router to router until it reaches the destination network.

---

# Default Gateway

Every host has a:

```text
Default Gateway
```

Example:

Computer:

```text
192.168.10.100
```

Gateway:

```text
192.168.10.1
```

If the destination is outside the local network:

```text
Send Packet

↓

Default Gateway
```

---

# Default Route

Routers also use a:

```text
Default Route
```

IPv4:

```text
0.0.0.0/0
```

IPv6:

```text
::/0
```

If no specific route exists, packets follow the default route.

---

# Longest Prefix Match

Routers always choose the **most specific matching route**.

Example:

Destination:

```text
10.10.20.15
```

Available routes:

```text
10.0.0.0/8

10.10.0.0/16

10.10.20.0/24
```

Selected route:

```text
10.10.20.0/24
```

because it has the longest matching prefix.

---

# Routing Workflow

```text
Packet Arrives

↓

Read Destination IP

↓

Search Routing Table

↓

Best Match Found

↓

Forward Packet

↓

Next Hop
```

---

# Routing Decision Example

Host:

```text
192.168.10.100
```

Destination:

```text
8.8.8.8
```

Host determines:

```text
Different Network

↓

Send to Gateway

↓

Router Routes Packet

↓

Internet
```

---

# Enterprise Example

Company Network:

```text
HR

192.168.10.0/24
```

↓

```text
Core Router
```

↓

```text
Finance

192.168.20.0/24
```

↓

```text
Engineering

192.168.30.0/24
```

The router enables communication between all departments.

---

# Cloud Perspective

Cloud providers use routing to connect:

- Virtual Machines
- Subnets
- Virtual Networks
- Internet Gateways
- Virtual Private Network (VPN) Connections
- Hybrid Networks

Routing tables determine how cloud traffic flows between resources.

---

# Kubernetes Perspective

Routing is essential for:

- Pod-to-Pod Communication
- Pod-to-Service Communication
- Node-to-Node Traffic
- Ingress Traffic
- Egress Traffic

Container Network Interface (CNI) plugins install routes automatically on Kubernetes nodes.

---

# Linux Perspective

Display routing table.

```bash
ip route
```

Display IPv6 routing table.

```bash
ip -6 route
```

Display network interfaces.

```bash
ip addr
```

Test routing.

```bash
traceroute google.com
```

Display the default gateway.

```bash
ip route | grep default
```

---

# Routing Example

```text
PC

↓

Default Gateway

↓

Router

↓

ISP Router

↓

Internet

↓

Web Server
```

Every router performs a routing table lookup before forwarding the packet.

---

# Hands-on Lab

## Task 1

Display your routing table.

```bash
ip route
```

---

## Task 2

Display your IPv6 routing table.

```bash
ip -6 route
```

---

## Task 3

Find your default gateway.

```bash
ip route | grep default
```

---

## Task 4

Run:

```bash
traceroute google.com
```

Observe how packets travel through multiple routers.

---

## Task 5

Draw a network showing:

- Client
- Router
- ISP
- Internet
- Server

Illustrate packet flow.

---

## Task 6

Create a routing table for:

- HR Network
- Finance Network
- Engineering Network
- Internet

---

## Task 7

Explain the difference between:

- Direct Route
- Indirect Route
- Default Route

---

## Task 8

Research routing tables in your preferred cloud provider (AWS, Azure, or GCP).

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip route` | Display IPv4 routing table |
| `ip -6 route` | Display IPv6 routing table |
| `ip addr` | Display IP addresses |
| `traceroute` | Trace packet path |
| `ping` | Test connectivity |

---

# Common Mistakes

❌ Confusing switching with routing.

✅ Switches forward frames; routers forward packets.

---

❌ Forgetting the default gateway.

✅ Configure the correct gateway for every subnet.

---

❌ Assuming routers use MAC addresses for routing.

✅ Routers make forwarding decisions using IP addresses.

---

❌ Ignoring the routing table.

✅ Always verify routes during troubleshooting.

---

❌ Misunderstanding longest prefix matching.

✅ Routers choose the most specific matching route.

---

# Best Practices

- Keep routing tables simple and well documented.
- Use meaningful IP addressing plans.
- Verify default gateways on all hosts.
- Monitor routing changes in production environments.
- Prefer route summarisation where appropriate.
- Regularly test end-to-end connectivity.

---

# Interview Questions

## Beginner

1. What is routing?
2. What is a router?
3. What is a routing table?
4. What is a default gateway?

---

## Intermediate

1. Explain how a router forwards packets.
2. What is a next hop?
3. What is the difference between direct and indirect routing?
4. Explain longest prefix matching.

---

## Architect Level

1. Design a routing architecture for a multi-site enterprise.
2. How would you troubleshoot a routing issue between two data centres?
3. Explain routing in hybrid cloud environments.

---

# Summary

In this lesson, you learned:

- Routing fundamentals
- Routers
- Routing tables
- Direct routing
- Indirect routing
- Default gateways
- Default routes
- Next-hop routing
- Longest prefix matching
- Linux routing commands

Routing is the foundation of Layer 3 networking. Routers examine destination IP addresses, consult routing tables, and forward packets toward their destination using the best available path. Every enterprise network, cloud platform, and Internet connection depends on efficient routing to deliver data reliably.

---

## Key Takeaways

- Routing connects **different IP networks**.
- Routers operate at **OSI Layer 3**.
- Routing decisions are based on **IP addresses**.
- Routing tables determine where packets are forwarded.
- The **default gateway** allows hosts to reach remote networks.
- Routers use **longest prefix matching** to select the most specific route.

---

## What's Next?

**[Static Routing](static-routing.md)**

In the next lesson, you'll learn about **Static Routing**.

You'll explore:

- What static routes are
- How to configure static routes
- Default static routes
- Recursive next-hop routing
- Floating static routes
- Linux static route configuration
- Enterprise use cases

By the end of the lesson, you'll understand how to manually configure routes and when static routing is the right choice for production networks.
