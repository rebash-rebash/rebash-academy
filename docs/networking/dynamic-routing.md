---
title: "Dynamic Routing"
description: "Learn dynamic routing — routing protocols, route advertisements, metrics, convergence, IGP vs EGP, and when to use dynamic routing in enterprise and cloud."
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
  - dynamic-routing
  - ospf
  - bgp
  - rebash-networking-mastery
comments: false
status: ready
---

# Dynamic Routing — Automatically Learning and Updating Network Routes

> **Dynamic Routing** is a routing method where routers automatically learn, exchange, and update routing information using **routing protocols**. Unlike static routing, where every route must be configured manually, dynamic routing allows routers to discover network changes, calculate the best path, and automatically update routing tables. Dynamic routing is essential for enterprise networks, cloud environments, Internet Service Providers (ISPs), and large-scale data centres. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand dynamic routing fundamentals.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 5: Routing → Lesson 3</p>

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

<div markdown>**Lesson:** 3 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Dynamic Routing
- Learn why dynamic routing is needed
- Understand routing protocols
- Learn route advertisements
- Understand convergence
- Learn routing metrics
- Compare static and dynamic routing
- Apply dynamic routing in enterprise environments

---

# Prerequisites

Complete:

- [Routing Basics](routing-fundamentals.md)
- [Static Routing](static-routing.md)

---

# Why Learn Dynamic Routing?

Imagine a company with:

- Headquarters
- Five Branch Offices
- Cloud Data Centre
- Disaster Recovery Site

Each location is connected through multiple routers.

```text
HQ

↓

Router

↓

Branches

↓

Cloud

↓

DR Site
```

If every route had to be configured manually:

```text
Hundreds of Static Routes

↓

Manual Updates

↓

High Maintenance
```

Dynamic routing solves this problem.

---

# What is Dynamic Routing?

Dynamic Routing is a process where routers automatically exchange routing information using routing protocols.

Instead of manually configuring routes:

```text
Router A

↓

Shares Routes

↓

Router B

↓

Updates Routing Table
```

Routes are learned and maintained automatically.

---

# Static vs Dynamic Routing

| Static Routing | Dynamic Routing |
|----------------|-----------------|
| Manual Configuration | Automatic Learning |
| No Route Exchange | Routers Exchange Routes |
| Best for Small Networks | Best for Large Networks |
| Low Resource Usage | Higher CPU and Memory Usage |
| No Automatic Recovery | Automatic Topology Updates |

---

# Why Dynamic Routing?

Advantages include:

- Automatic Route Discovery
- Automatic Failover
- Better Scalability
- Faster Network Expansion
- Reduced Administrative Effort
- Automatic Recovery After Failures

---

# How Dynamic Routing Works

```text
Router Starts

↓

Discover Neighbours

↓

Exchange Routes

↓

Build Routing Table

↓

Forward Traffic

↓

Monitor Network Changes

↓

Update Routes Automatically
```

---

# Routing Protocol

A **Routing Protocol** defines how routers:

- Discover Networks
- Exchange Routes
- Calculate Best Paths
- Detect Failures
- Update Routing Tables

Examples include:

- Routing Information Protocol (RIP)
- Open Shortest Path First (OSPF)
- Enhanced Interior Gateway Routing Protocol (EIGRP)
- Intermediate System to Intermediate System (IS-IS)
- Border Gateway Protocol (BGP)

---

# Route Advertisement

Routers periodically or event-driven share information about reachable networks.

Example:

Router A:

```text
I Know

192.168.10.0/24
```

Router B:

```text
I Know

192.168.20.0/24
```

Both routers exchange this information.

---

# Routing Table Updates

After exchanging routes:

Router A learns:

```text
192.168.20.0/24
```

Router B learns:

```text
192.168.10.0/24
```

Communication becomes possible without manually adding routes.

---

# Neighbor Relationship

Most routing protocols establish relationships with neighbouring routers.

Example:

```text
Router A

⇄

Router B
```

These neighbouring routers exchange routing information.

---

# Routing Metrics

When multiple paths exist, routers select the best path using a **Metric**.

Common metrics include:

- Hop Count
- Bandwidth
- Delay
- Cost
- Reliability
- Load

Different routing protocols use different metrics.

---

# Convergence

**Convergence** is the process by which all routers agree on the current network topology.

Example:

```text
Link Failure

↓

Detect Failure

↓

Exchange Updates

↓

Recalculate Routes

↓

Network Stable
```

Faster convergence means less downtime.

---

# Route Selection

Suppose two paths exist.

Path 1:

```text
3 Hops
```

Path 2:

```text
7 Hops
```

The routing protocol selects the preferred path according to its metric.

For RIP, the lower hop count is preferred.

For OSPF, the lower cost is preferred.

---

# Dynamic Routing Workflow

```text
Router Boots

↓

Start Routing Protocol

↓

Discover Neighbours

↓

Exchange Routes

↓

Calculate Best Paths

↓

Install Routes

↓

Forward Packets

↓

React to Network Changes
```

---

# Interior vs Exterior Routing

Routing protocols are grouped into two major categories.

### Interior Gateway Protocols (IGPs)

Used **within one organisation**.

Examples:

- RIP
- OSPF
- EIGRP
- IS-IS

---

### Exterior Gateway Protocols (EGPs)

Used **between different organisations**.

Example:

- BGP

BGP powers routing across the Internet.

---

# Dynamic Routing Protocol Comparison

| Protocol | Metric | Typical Use |
|-----------|---------|-------------|
| RIP | Hop Count | Small Networks |
| OSPF | Cost | Enterprise Networks |
| EIGRP | Composite Metric | Enterprise (Primarily Cisco) |
| IS-IS | Cost | Service Providers |
| BGP | Policy-Based | Internet & ISPs |

---

# Enterprise Example

Company:

```text
Head Office

↓

Router

↓

Branches

↓

Cloud

↓

Data Centre
```

OSPF automatically shares routing information between all locations.

If a WAN link fails:

```text
Detect Failure

↓

Find Alternate Path

↓

Update Routing Tables
```

No manual intervention is required.

---

# Cloud Perspective

Cloud providers use dynamic routing for:

- VPN Gateways
- Cloud Routers
- Hybrid Connectivity
- Dedicated Interconnects
- Multi-Region Networks

Protocols such as BGP are commonly used to exchange routes between on-premises and cloud environments.

---

# Kubernetes Perspective

Traditional Kubernetes clusters rely on routing managed by the Container Network Interface (CNI).

Some advanced networking solutions use routing protocols or BGP to advertise Pod and Service networks to the surrounding infrastructure.

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

Check reachability.

```bash
ping 192.168.1.1
```

Trace routing path.

```bash
traceroute google.com
```

Linux itself does not provide dynamic routing by default, but routing software such as **FRRouting (FRR)** or **BIRD** can implement protocols like OSPF and BGP.

---

# Dynamic Routing Example

```text
Router A

↓

OSPF

↓

Router B

↓

OSPF

↓

Router C
```

Each router exchanges routing information and automatically builds its routing table.

---

# Advantages of Dynamic Routing

- Automatic Route Learning
- Automatic Topology Updates
- High Availability
- Better Scalability
- Supports Large Networks
- Faster Recovery

---

# Disadvantages of Dynamic Routing

- More Complex
- Higher CPU Usage
- Higher Memory Usage
- Protocol Configuration Required
- Convergence Time

---

# Hands-on Lab

## Task 1

Display your routing table.

```bash
ip route
```

---

## Task 2

Display IPv6 routes.

```bash
ip -6 route
```

---

## Task 3

Compare:

- Static Routing
- Dynamic Routing

List at least ten differences.

---

## Task 4

Draw a network with:

- Three Routers
- Three LANs

Show how routes are exchanged dynamically.

---

## Task 5

Research:

- RIP
- OSPF
- EIGRP
- BGP

Summarise when each protocol is commonly used.

---

## Task 6

Explain the concept of convergence.

---

## Task 7

Create a table showing routing metrics used by different protocols.

---

## Task 8

Research how dynamic routing is implemented in a cloud environment using BGP.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip route` | Display routing table |
| `ip -6 route` | Display IPv6 routing table |
| `ip addr` | Display IP configuration |
| `ping` | Test connectivity |
| `traceroute` | Trace packet path |

---

# Common Mistakes

❌ Assuming dynamic routing requires no configuration.

✅ Routing protocols still require proper configuration.

---

❌ Using dynamic routing in a tiny network unnecessarily.

✅ Static routing may be simpler for small environments.

---

❌ Ignoring convergence time.

✅ Choose protocols with convergence characteristics that match your environment.

---

❌ Confusing routing protocols with routing tables.

✅ Routing protocols build and maintain routing tables.

---

❌ Forgetting protocol metrics.

✅ Understand how each protocol selects the best path.

---

# Best Practices

- Use dynamic routing in medium and large networks.
- Choose the routing protocol that fits your network size and requirements.
- Monitor routing convergence after topology changes.
- Keep routing designs simple and well documented.
- Summarise routes whenever appropriate.
- Secure routing protocol communications where supported.

---

# Interview Questions

## Beginner

1. What is dynamic routing?
2. Why is dynamic routing used?
3. What is a routing protocol?
4. What is convergence?

---

## Intermediate

1. Compare static and dynamic routing.
2. Explain route advertisements.
3. What is a routing metric?
4. Compare Interior Gateway Protocols and Exterior Gateway Protocols.

---

## Architect Level

1. Design a dynamic routing solution for a multi-site enterprise.
2. How would you choose between OSPF and BGP?
3. How would you troubleshoot slow routing convergence?

---

# Summary

In this lesson, you learned:

- Dynamic Routing
- Routing Protocols
- Route Advertisements
- Neighbor Relationships
- Routing Metrics
- Convergence
- Interior and Exterior Routing
- Enterprise Routing
- Linux Routing Commands

Dynamic routing enables routers to automatically discover networks, exchange routing information, and adapt to topology changes without manual intervention. It is the preferred routing method for medium and large enterprise networks because it provides scalability, resilience, and automatic recovery from failures.

---

## Key Takeaways

- Dynamic routing automatically builds and updates routing tables.
- Routers exchange routes using routing protocols.
- Metrics determine the preferred path.
- Convergence ensures routers share a consistent view of the network.
- IGPs are used within an organisation; BGP is used between organisations.
- Dynamic routing is ideal for scalable and resilient enterprise networks.

---

## What's Next?

**[RIP](rip.md)**

In the next lesson, you'll learn about **RIP (Routing Information Protocol)**.

You'll explore:

- What RIP is
- RIP versions
- Hop count metric
- Maximum hop limit
- Route advertisements
- RIP timers
- Advantages and limitations

By the end of the lesson, you'll understand how RIP works, how it exchanges routes, and why it is primarily used in small networks and educational environments.
