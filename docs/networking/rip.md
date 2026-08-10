---
title: "RIP"
description: "Learn Routing Information Protocol (RIP) — hop count, RIPv1/RIPv2/RIPng, timers, distance-vector updates, loop prevention, and when RIP is appropriate."
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
  - rip
  - distance-vector
  - rebash-networking-mastery
comments: false
status: ready
---

# RIP (Routing Information Protocol) — The Simplest Dynamic Routing Protocol

> **Routing Information Protocol (RIP)** is one of the oldest and simplest **dynamic routing protocols**. It automatically exchanges routing information between routers and uses **Hop Count** as its routing metric. RIP is easy to configure and understand, making it an excellent protocol for learning routing fundamentals. However, because of its limited scalability and slower convergence, RIP is primarily used in small networks, lab environments, and educational settings rather than large enterprise networks. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand RIP as the foundation of dynamic routing.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 5: Routing → Lesson 4</p>

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

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand RIP
- Learn RIP versions
- Understand Hop Count
- Learn RIP timers
- Understand route advertisements
- Learn RIP convergence
- Compare RIP with modern routing protocols

---

# Prerequisites

Complete:

- [Routing Basics](routing-fundamentals.md)
- [Static Routing](static-routing.md)
- [Dynamic Routing](dynamic-routing.md)

---

# Why Learn RIP?

Imagine three routers connected together.

```text
LAN A

↓

Router A

↓

Router B

↓

Router C

↓

LAN B
```

Without dynamic routing:

Every router must be manually configured.

With RIP:

```text
Routers

↓

Exchange Routes

↓

Automatically Learn Networks
```

---

# What is RIP?

**Routing Information Protocol (RIP)** is a **Distance Vector Routing Protocol**.

It automatically exchanges routing information between neighbouring routers.

Characteristics:

- Simple
- Easy to Configure
- Uses Hop Count
- Best for Small Networks

---

# Distance Vector Protocol

RIP routers know:

- Destination Network
- Distance (Hop Count)
- Direction (Next Hop)

Example:

```text
Destination

192.168.20.0/24

↓

Hop Count

2

↓

Next Hop

192.168.1.2
```

---

# What is Hop Count?

A **Hop** represents one router crossed by a packet.

Example:

```text
PC

↓

Router A

↓

Router B

↓

Router C

↓

Server
```

Hop Count:

```text
3
```

RIP always prefers the route with the **lowest hop count**.

---

# Maximum Hop Limit

RIP supports a maximum of:

```text
15 Hops
```

Hop Count:

```text
16

↓

Unreachable
```

Because of this limitation, RIP is unsuitable for large networks.

---

# RIP Versions

There are two primary IPv4 versions.

### RIP Version 1 (RIPv1)

Characteristics:

- Classful Routing
- No Subnet Mask Information
- Broadcast Updates
- No Variable Length Subnet Masking (VLSM) Support

---

### RIP Version 2 (RIPv2)

Characteristics:

- Classless Routing
- Supports Classless Inter-Domain Routing (CIDR)
- Supports VLSM
- Multicast Updates
- Authentication Support

RIPv2 is the version used in modern IPv4 networks when RIP is required.

---

# RIPng

For IPv6:

```text
RIPng

(RIP Next Generation)
```

Features:

- Supports IPv6
- Uses IPv6 Addresses
- Similar Operation to RIPv2

---

# Route Advertisement

RIP routers periodically advertise their routing tables.

Example:

Router A:

```text
Knows

192.168.10.0/24
```

Router B:

```text
Learns

192.168.10.0/24
```

Each router gradually builds a complete routing table.

---

# RIP Update Interval

By default:

```text
Every

30 Seconds
```

Routers send routing updates to their neighbours.

This periodic update mechanism contributes to RIP's simplicity but also to its slower convergence.

---

# RIP Timers

Common RIP timers include:

| Timer | Default |
|--------|---------|
| Update Timer | 30 Seconds |
| Invalid Timer | 180 Seconds |
| Hold-down Timer | 180 Seconds |
| Flush Timer | 240 Seconds |

These timers determine how long routes remain valid and when they are removed.

---

# Route Selection

Example:

Path A:

```text
2 Hops
```

Path B:

```text
5 Hops
```

RIP chooses:

```text
2-Hop Route
```

Only hop count is considered—RIP does not account for bandwidth, latency, or link quality.

---

# Convergence

Suppose a link fails.

```text
Failure

↓

Wait for Update

↓

Exchange Routes

↓

Update Routing Tables
```

RIP convergence is relatively slow compared to protocols like Open Shortest Path First (OSPF).

---

# Count-to-Infinity Problem

A classic challenge with Distance Vector routing.

Example:

```text
Route Fails

↓

Routers Continue Advertising Old Route

↓

Hop Count Increases

↓

Eventually Reaches

16

↓

Route Removed
```

This process can delay convergence.

---

# Loop Prevention Techniques

RIP includes several mechanisms to reduce routing loops.

### Split Horizon

Prevents advertising a route back out of the interface from which it was learned.

---

### Route Poisoning

Marks failed routes with:

```text
Hop Count

16
```

to indicate they are unreachable.

---

### Poison Reverse

Advertises an unreachable route back to the neighbour that originally advertised it, reinforcing that the path is no longer valid.

---

### Hold-Down Timer

Temporarily ignores potentially incorrect routing updates while the network stabilises.

---

# RIP Workflow

```text
Router Starts

↓

Discover Neighbours

↓

Send Routing Table

↓

Receive Updates

↓

Calculate Hop Count

↓

Install Best Routes

↓

Repeat Every 30 Seconds
```

---

# Enterprise Example

Small Business:

```text
Office

↓

Router

↓

Warehouse

↓

Branch Office
```

Three routers exchange routes automatically using RIP.

Simple and easy to manage.

---

# Cloud Perspective

Major cloud providers rarely use RIP internally.

Modern cloud environments typically rely on:

- Border Gateway Protocol (BGP)
- Static Routes
- Cloud Route Tables

However, RIP may still appear in legacy hybrid environments.

---

# Kubernetes Perspective

Kubernetes networking does not use RIP.

Instead, routing is managed by the Container Network Interface (CNI), and some advanced networking solutions use BGP for route advertisement.

---

# Linux Perspective

Linux supports RIP through routing software such as:

- FRRouting (FRR)
- BIRD
- Quagga (legacy)

Display routing table.

```bash
ip route
```

Display IPv6 routes.

```bash
ip -6 route
```

Routing daemon configuration depends on the software being used.

---

# RIP Example

```text
Router A

↓

1 Hop

↓

Router B

↓

1 Hop

↓

Router C
```

Router A reaches Router C with:

```text
Hop Count

2
```

---

# RIP Advantages

- Easy to Learn
- Easy to Configure
- Low Administrative Overhead
- Suitable for Small Networks
- Excellent for Learning Routing Concepts

---

# RIP Limitations

- Maximum 15 Hops
- Slow Convergence
- Limited Scalability
- Hop Count Only
- Not Suitable for Large Enterprises

---

# RIP vs OSPF

| RIP | OSPF |
|------|------|
| Distance Vector | Link-State |
| Hop Count | Cost |
| 15-Hop Limit | No Practical Hop Limit |
| Slower Convergence | Faster Convergence |
| Small Networks | Enterprise Networks |

---

# Hands-on Lab

## Task 1

Display routing table.

```bash
ip route
```

---

## Task 2

Display IPv6 routing table.

```bash
ip -6 route
```

---

## Task 3

Draw three routers connected using RIP.

Show how routing tables are exchanged.

---

## Task 4

Calculate hop counts for multiple network paths.

Determine which route RIP selects.

---

## Task 5

Compare:

- RIPv1
- RIPv2
- RIPng

---

## Task 6

Research:

- Split Horizon
- Route Poisoning
- Hold-Down Timer

Explain how each reduces routing loops.

---

## Task 7

Create a table showing all RIP timers and their purposes.

---

## Task 8

Compare RIP with OSPF and explain why enterprises generally prefer OSPF.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip route` | Display IPv4 routing table |
| `ip -6 route` | Display IPv6 routing table |
| `ip addr` | Display IP addresses |
| `ping` | Test connectivity |
| `traceroute` | Trace packet path |

---

# Common Mistakes

❌ Using RIP in large enterprise networks.

✅ Prefer OSPF or other scalable routing protocols.

---

❌ Assuming RIP considers bandwidth.

✅ RIP uses only hop count.

---

❌ Forgetting the 15-hop limit.

✅ RIP cannot route beyond 15 hops.

---

❌ Ignoring RIP timers.

✅ Understand how timers affect convergence.

---

❌ Using RIPv1 with modern subnetting.

✅ Prefer RIPv2 for IPv4 networks.

---

# Best Practices

- Use RIPv2 instead of RIPv1 for IPv4 deployments.
- Reserve RIP for small or educational networks.
- Monitor routing updates during troubleshooting.
- Understand RIP's convergence limitations.
- Consider OSPF or Enhanced Interior Gateway Routing Protocol (EIGRP) for larger environments.
- Document RIP-enabled interfaces and networks.

---

# Interview Questions

## Beginner

1. What is RIP?
2. What metric does RIP use?
3. What is the maximum hop count in RIP?
4. What is the difference between RIPv1 and RIPv2?

---

## Intermediate

1. Explain Distance Vector routing.
2. What is convergence in RIP?
3. What are RIP timers?
4. Explain Split Horizon and Route Poisoning.

---

## Architect Level

1. Why is RIP rarely used in modern enterprise networks?
2. Compare RIP and OSPF for a multi-site organisation.
3. How would you migrate from RIP to OSPF?

---

# Summary

In this lesson, you learned:

- RIP fundamentals
- Distance Vector routing
- Hop Count
- RIPv1
- RIPv2
- RIPng
- Route advertisements
- RIP timers
- Loop prevention techniques
- Enterprise considerations

RIP is one of the simplest dynamic routing protocols and provides an excellent introduction to automatic route exchange. While its simplicity makes it ideal for learning and small networks, its hop-count limitation and slower convergence make it unsuitable for most modern enterprise environments, where protocols such as OSPF and BGP are preferred.

---

## Key Takeaways

- RIP is a **Distance Vector Routing Protocol**.
- RIP uses **Hop Count** as its routing metric.
- The maximum supported path length is **15 hops**.
- RIPv2 supports **CIDR**, **VLSM**, and authentication.
- RIP exchanges routing updates every **30 seconds** by default.
- Loop prevention mechanisms include **Split Horizon**, **Route Poisoning**, and **Hold-Down Timers**.
- RIP is best suited for small networks and educational environments.

---

## What's Next?

**[OSPF](ospf.md)**

In the next lesson, you'll learn about **OSPF (Open Shortest Path First)**.

You'll explore:

- Link-State Routing
- OSPF Areas
- Link-State Advertisements (LSAs)
- Cost Metric
- Designated Router (DR)
- Backup Designated Router (BDR)
- Fast Convergence
- Enterprise OSPF Design

By the end of the lesson, you'll understand why OSPF is one of the most widely used dynamic routing protocols in enterprise networks.
