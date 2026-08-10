---
title: "EIGRP Concepts"
description: "Learn Enhanced Interior Gateway Routing Protocol (EIGRP) — DUAL, Successor and Feasible Successor routes, composite metrics, neighbors, and enterprise use cases."
difficulty: intermediate
estimated_time: "100 min"
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
  - eigrp
  - dual
  - rebash-networking-mastery
comments: false
status: ready
---

# EIGRP Concepts — Fast, Intelligent, and Efficient Enterprise Routing

> **Enhanced Interior Gateway Routing Protocol (EIGRP)** is an advanced dynamic routing protocol originally developed by Cisco. It combines many advantages of both **Distance Vector** and **Link-State** routing, which is why it is often described as an **Advanced Distance Vector** or **Hybrid Routing Protocol**. EIGRP provides **fast convergence**, **efficient bandwidth usage**, and **intelligent route selection** using the **Diffusing Update Algorithm (DUAL)**. Although modern enterprise environments frequently use Open Shortest Path First (OSPF) as an open standard, understanding EIGRP is valuable because it is still widely deployed in Cisco-based enterprise networks. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand the core concepts of EIGRP.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 5: Routing → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 100 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Routing</div>

<div markdown>**Lesson:** 6 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand EIGRP fundamentals
- Learn the Diffusing Update Algorithm (DUAL)
- Understand EIGRP metrics
- Learn Successor and Feasible Successor routes
- Understand neighbour relationships
- Learn EIGRP packet types
- Compare EIGRP with Routing Information Protocol (RIP) and OSPF
- Understand enterprise EIGRP deployments

---

# Prerequisites

Complete:

- [Routing Basics](routing-fundamentals.md)
- [Static Routing](static-routing.md)
- [Dynamic Routing](dynamic-routing.md)
- [RIP](rip.md)
- [OSPF](ospf.md)

---

# Why Learn EIGRP?

Imagine an enterprise with:

- Headquarters
- Regional Offices
- Branch Offices
- Data Centres

```text
HQ

↓

Regional Offices

↓

Branches

↓

Data Centre
```

When a WAN link fails:

```text
Failure

↓

Alternative Path

↓

Minimal Downtime
```

The routing protocol should quickly select an alternate route.

EIGRP was designed to do exactly that.

---

# What is EIGRP?

**Enhanced Interior Gateway Routing Protocol (EIGRP)** is an Interior Gateway Protocol (IGP) designed for enterprise routing.

Characteristics:

- Fast Convergence
- Efficient Route Calculation
- Incremental Updates
- Loop-Free Routing
- Supports IPv4 and IPv6

---

# Advanced Distance Vector Protocol

Unlike traditional Distance Vector protocols such as RIP:

```text
RIP

↓

Periodic Full Updates
```

EIGRP:

```text
Neighbor Discovery

↓

Partial Updates

↓

Triggered Updates
```

Only changes are transmitted, reducing bandwidth usage.

---

# DUAL Algorithm

The heart of EIGRP is:

```text
DUAL

Diffusing Update Algorithm
```

DUAL ensures:

- Loop-Free Routing
- Fast Convergence
- Backup Route Selection
- Efficient Route Calculation

---

# EIGRP Topology Table

Unlike RIP, EIGRP maintains multiple tables.

### Neighbor Table

Stores neighbouring routers.

---

### Topology Table

Stores all learned routes.

---

### Routing Table

Stores only the best routes used for forwarding.

---

# Neighbor Discovery

Routers discover neighbours using:

```text
Hello Packets
```

Example:

```text
Router A

⇄ Hello ⇄

Router B
```

After becoming neighbours:

```text
Exchange Routes
```

---

# Successor Route

The **Successor** is:

```text
Best Route
```

Chosen by DUAL.

Installed in:

```text
Routing Table
```

Traffic always uses the Successor route.

---

# Feasible Successor

A **Feasible Successor** is:

```text
Backup Route
```

Characteristics:

- Already Calculated
- Loop-Free
- Immediately Available

If the primary route fails:

```text
Successor

↓

Failure

↓

Feasible Successor

↓

Immediately Active
```

No complete recalculation is required.

---

# Feasibility Condition

A backup route qualifies as a **Feasible Successor** only if it satisfies the **Feasibility Condition (FC)**.

This ensures that the backup path is loop-free before it is used.

---

# EIGRP Metrics

Unlike RIP:

```text
Hop Count
```

EIGRP uses a **Composite Metric**.

By default, the calculation is primarily based on:

- Bandwidth
- Delay

Other optional metric components include:

- Reliability
- Load
- Maximum Transmission Unit (MTU) (recorded but not directly included in the default metric calculation)

---

# Metric Example

Path A:

```text
Bandwidth

1 Gbps

Delay

Low
```

Path B:

```text
Bandwidth

100 Mbps

Delay

Higher
```

EIGRP selects:

```text
Path A
```

---

# Partial Updates

Instead of sending the complete routing table:

```text
Only Changed Routes

↓

Neighbors
```

Benefits:

- Lower Bandwidth Usage
- Faster Updates
- Better Performance

---

# Triggered Updates

Suppose:

```text
Link Failure
```

Instead of waiting for a timer:

```text
Immediately Notify

Neighbors
```

This results in rapid convergence.

---

# EIGRP Packet Types

EIGRP uses five packet types.

| Packet | Purpose |
|----------|----------|
| Hello | Neighbor Discovery |
| Update | Route Exchange |
| Query | Request Alternate Route |
| Reply | Respond to Query |
| Acknowledgment (ACK) | Confirm Reliable Delivery |

---

# Reliable Transport Protocol (RTP)

EIGRP uses:

```text
Reliable Transport Protocol

(RTP)
```

RTP ensures that important routing updates are delivered reliably without relying on Transmission Control Protocol (TCP).

---

# Load Balancing

EIGRP supports:

- Equal-Cost Load Balancing
- Unequal-Cost Load Balancing

Unequal-cost load balancing is made possible through the **Variance** feature.

This is one of EIGRP's unique capabilities.

---

# Convergence

Example:

```text
Primary Link

↓

Failure

↓

Feasible Successor

↓

Immediately Used
```

Convergence is typically very fast.

---

# Enterprise Example

Enterprise WAN:

```text
HQ

↓

MPLS

↓

Branches

↓

Data Centres
```

EIGRP dynamically exchanges routes while maintaining backup paths for rapid failover.

---

# Cloud Perspective

Major cloud providers do not typically run EIGRP within their managed cloud networks.

However, organisations may encounter EIGRP in:

- Legacy Cisco Enterprise Networks
- Hybrid Cloud Deployments
- On-Premises Data Centres

Cloud connectivity usually relies on Border Gateway Protocol (BGP) rather than EIGRP.

---

# Kubernetes Perspective

Kubernetes does not use EIGRP.

Instead, container networking relies on:

- Container Network Interface (CNI) Plugins
- Linux Routing
- BGP (in some networking solutions)

However, Kubernetes worker nodes may connect to enterprise networks where EIGRP provides the underlying routing.

---

# Linux Perspective

Linux does not include native EIGRP support in the kernel.

Some third-party routing software has provided EIGRP support historically, but it is far less common than OSPF or BGP implementations.

Useful Linux commands include:

Display routing table.

```bash
ip route
```

Display interfaces.

```bash
ip addr
```

Test connectivity.

```bash
ping 192.168.1.1
```

---

# EIGRP Workflow

```text
Router Starts

↓

Hello Packets

↓

Neighbor Table

↓

Exchange Routes

↓

Topology Table

↓

DUAL

↓

Successor Route

↓

Routing Table
```

---

# Advantages of EIGRP

- Fast Convergence
- Loop-Free Routing
- Incremental Updates
- Backup Routes
- Efficient Bandwidth Usage
- Unequal-Cost Load Balancing
- Scalable Enterprise Routing

---

# Limitations of EIGRP

- Historically associated with Cisco environments
- Less commonly used than OSPF in multi-vendor networks
- More complex than RIP
- Requires proper planning and configuration

---

# RIP vs OSPF vs EIGRP

| Feature | RIP | OSPF | EIGRP |
|----------|------|------|--------|
| Type | Distance Vector | Link-State | Advanced Distance Vector |
| Metric | Hop Count | Cost | Composite Metric |
| Convergence | Slow | Fast | Very Fast |
| Scalability | Small | Large | Large |
| Updates | Periodic | Event-Driven | Partial & Triggered |

---

# Hands-on Lab

## Task 1

Display routing table.

```bash
ip route
```

---

## Task 2

Draw an enterprise network containing:

- Headquarters
- Branches
- Data Centre

Show:

- Successor Routes
- Feasible Successor Routes

---

## Task 3

Compare:

- RIP
- OSPF
- EIGRP

Create a feature comparison table.

---

## Task 4

Explain how DUAL prevents routing loops.

---

## Task 5

Research:

- Successor
- Feasible Successor
- Feasibility Condition

Explain each concept.

---

## Task 6

Explain why partial updates reduce bandwidth usage.

---

## Task 7

Research EIGRP packet types.

Describe the purpose of each.

---

## Task 8

Explain when EIGRP is a suitable choice for an enterprise network.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip route` | Display routing table |
| `ip addr` | Display IP configuration |
| `ping` | Test connectivity |
| `traceroute` | Trace packet path |

---

# Common Mistakes

❌ Assuming EIGRP uses hop count.

✅ EIGRP uses a composite metric.

---

❌ Confusing Successor with Feasible Successor.

✅ One is the active route; the other is the backup route.

---

❌ Ignoring DUAL.

✅ DUAL is the core of EIGRP operation.

---

❌ Assuming EIGRP sends full routing tables continuously.

✅ EIGRP sends partial, triggered updates.

---

❌ Choosing EIGRP for a multi-vendor environment without evaluating compatibility.

✅ OSPF is often preferred where open standards are required.

---

# Best Practices

- Use EIGRP primarily in Cisco-centric enterprise environments.
- Understand DUAL before deploying EIGRP.
- Monitor neighbour relationships regularly.
- Keep routing designs simple and hierarchical.
- Document Successor and backup paths.
- Test failover behaviour in production-like environments.

---

# Interview Questions

## Beginner

1. What is EIGRP?
2. What type of routing protocol is EIGRP?
3. What is DUAL?
4. What is a Successor Route?

---

## Intermediate

1. Explain the Topology Table.
2. What is a Feasible Successor?
3. How does EIGRP achieve fast convergence?
4. What metrics does EIGRP use?

---

## Architect Level

1. Compare OSPF and EIGRP for enterprise deployments.
2. Explain how DUAL guarantees loop-free routing.
3. Design an enterprise routing architecture using EIGRP with redundant WAN links.

---

# Summary

In this lesson, you learned:

- EIGRP fundamentals
- DUAL
- Neighbor Discovery
- Topology Table
- Routing Table
- Successor Routes
- Feasible Successor Routes
- Composite Metrics
- Partial Updates
- Triggered Updates
- RTP
- Enterprise EIGRP design

EIGRP is a powerful enterprise routing protocol that provides rapid convergence, efficient bandwidth usage, and intelligent route selection. Through DUAL, Successor routes, and Feasible Successor routes, EIGRP quickly adapts to network changes while maintaining loop-free routing.

---

## Key Takeaways

- EIGRP is an **Advanced Distance Vector Routing Protocol**.
- **DUAL** is responsible for route calculation and loop prevention.
- **Successor** routes are active paths.
- **Feasible Successor** routes provide immediate backup paths.
- EIGRP uses a **Composite Metric** based primarily on bandwidth and delay.
- Partial and triggered updates reduce bandwidth usage.
- EIGRP remains important in many Cisco enterprise environments.

---

## What's Next?

**[BGP Introduction](bgp-introduction.md)**

In the next lesson, you'll learn about **BGP (Border Gateway Protocol) Introduction**.

You'll explore:

- What BGP is
- Autonomous Systems (AS)
- eBGP vs iBGP
- Path Selection
- AS Path
- Internet Routing
- BGP attributes
- Enterprise and cloud use cases

By the end of the lesson, you'll understand why BGP is the routing protocol that powers the Internet and how it connects organisations, cloud providers, and service providers worldwide.
