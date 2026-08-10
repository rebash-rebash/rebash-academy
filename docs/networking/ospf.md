---
title: "OSPF"
description: "Learn Open Shortest Path First (OSPF) — link-state routing, areas, LSAs, SPF algorithm, cost metric, DR/BDR, and enterprise OSPF design."
difficulty: intermediate
estimated_time: "110 min"
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
  - ospf
  - link-state
  - rebash-networking-mastery
comments: false
status: ready
---

# OSPF (Open Shortest Path First) — Enterprise Link-State Routing Protocol

> **Open Shortest Path First (OSPF)** is a **Link-State Dynamic Routing Protocol** designed for medium and large enterprise networks. Unlike Routing Information Protocol (RIP), which uses **Hop Count**, OSPF builds a complete map of the network topology and calculates the **shortest path** using **Dijkstra's Shortest Path First (SPF) Algorithm**. OSPF provides **fast convergence**, **excellent scalability**, and **efficient route calculation**, making it one of the most widely deployed Interior Gateway Protocols (IGPs) in enterprise data centres, cloud environments, and service provider networks. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand OSPF.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 5: Routing → Lesson 5</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 110 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Routing</div>

<div markdown>**Lesson:** 5 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand OSPF
- Learn Link-State Routing
- Understand OSPF Areas
- Learn Link-State Advertisements (LSAs)
- Understand the SPF Algorithm
- Learn OSPF Cost Metric
- Understand Designated Router (DR) and Backup Designated Router (BDR) Elections
- Design enterprise OSPF networks

---

# Prerequisites

Complete:

- [Routing Basics](routing-fundamentals.md)
- [Static Routing](static-routing.md)
- [Dynamic Routing](dynamic-routing.md)
- [RIP](rip.md)

---

# Why Learn OSPF?

Imagine a company with:

- Headquarters
- 25 Branch Offices
- Cloud Infrastructure
- Multiple Data Centres

```text
HQ

↓

Core Network

↓

Branches

↓

Cloud

↓

Data Centres
```

Using RIP:

```text
Slow

Limited

15-Hop Maximum
```

Not suitable.

Solution:

```text
OSPF
```

---

# What is OSPF?

**Open Shortest Path First (OSPF)** is a **Link-State Interior Gateway Protocol (IGP)**.

Characteristics:

- Open Standard
- Fast Convergence
- Highly Scalable
- Loop-Free Routing
- Classless Routing
- Supports Classless Inter-Domain Routing (CIDR) and Variable Length Subnet Masking (VLSM)

---

# Link-State Routing

Unlike RIP:

```text
Distance Vector

↓

Only Knows Next Hop
```

OSPF:

```text
Knows Entire Network Topology
```

Each router builds a complete map of the network.

---

# OSPF Topology Database

Every OSPF router maintains a:

```text
Link-State Database (LSDB)
```

The LSDB contains:

- Routers
- Links
- Costs
- Neighbor Relationships
- Network Topology

All routers within the same OSPF area maintain synchronised LSDBs.

---

# SPF Algorithm

OSPF uses:

```text
Dijkstra's

Shortest Path First

(SPF)
```

Algorithm:

```text
LSDB

↓

SPF Calculation

↓

Shortest Path Tree

↓

Routing Table
```

The best route is installed automatically.

---

# OSPF Metric

OSPF uses:

```text
Cost
```

Cost is typically based on interface bandwidth.

Example:

| Link | Cost |
|------|------:|
| 10 Gbps | 1 |
| 1 Gbps | 10 |
| 100 Mbps | 100 |

> Actual cost values depend on the configured reference bandwidth.

OSPF always prefers the path with the **lowest total cost**.

---

# Neighbor Discovery

OSPF routers discover neighbouring routers by sending:

```text
Hello Packets
```

Example:

```text
Router A

⇄ Hello ⇄

Router B
```

If parameters match, they become neighbours.

---

# Hello Packet

A Hello packet contains information such as:

- Router ID
- Area ID
- Hello Timer
- Dead Timer
- Authentication Information (if configured)

These parameters must be compatible for adjacency formation.

---

# Neighbor States

OSPF routers progress through several neighbour states.

Common states include:

```text
Down

↓

Init

↓

2-Way

↓

ExStart

↓

Exchange

↓

Loading

↓

Full
```

At the **Full** state, routers have synchronised databases.

---

# Link-State Advertisement (LSA)

Routers advertise topology information using:

```text
LSA

(Link-State Advertisement)
```

LSAs describe:

- Networks
- Routers
- Links
- Costs

Routers flood LSAs throughout an OSPF area.

---

# OSPF Areas

Large OSPF networks are divided into:

```text
Areas
```

Benefits:

- Better Scalability
- Smaller LSDB
- Reduced CPU Usage
- Faster Convergence

---

# Backbone Area

Every OSPF network contains:

```text
Area 0
```

Also called:

```text
Backbone Area
```

All other areas connect to Area 0.

---

# Example OSPF Design

```text
Area 1

↓

Area 0

↓

Area 2
```

Traffic between Area 1 and Area 2 passes through the backbone.

---

# Router Types

OSPF defines several router roles.

### Internal Router

All interfaces belong to the same area.

---

### Backbone Router

Has at least one interface in:

```text
Area 0
```

---

### Area Border Router (ABR)

Connects:

```text
Area 0

↓

Other Areas
```

Responsible for exchanging routing information between areas.

---

### Autonomous System Boundary Router (ASBR)

Redistributes routes from another routing domain into OSPF.

Examples include:

- Static Routes
- Border Gateway Protocol (BGP)
- RIP

---

# DR and BDR

On multi-access networks (such as Ethernet), OSPF elects:

```text
Designated Router

(DR)
```

and

```text
Backup Designated Router

(BDR)
```

Purpose:

- Reduce LSA flooding
- Improve efficiency
- Reduce network overhead

---

# DR Election

Election priority:

1. Highest OSPF Interface Priority
2. Highest Router ID (if priorities are equal)

---

# Router ID

Every OSPF router has a unique:

```text
Router ID
```

Example:

```text
1.1.1.1
```

The Router ID identifies the router within the OSPF domain.

---

# OSPF Packet Types

OSPF defines five packet types.

| Packet | Purpose |
|----------|----------|
| Hello | Neighbor Discovery |
| Database Description (DBD) | Summarise LSDB |
| Link-State Request (LSR) | Request Missing LSAs |
| Link-State Update (LSU) | Send LSAs |
| Link-State Acknowledgment (LSAck) | Confirm Receipt |

---

# OSPF Workflow

```text
Router Starts

↓

Send Hello Packets

↓

Neighbor Discovery

↓

Exchange LSDB

↓

Run SPF Algorithm

↓

Install Routes

↓

Forward Traffic
```

---

# Convergence

Suppose a link fails.

```text
Failure

↓

New LSA

↓

Flood Area

↓

SPF Recalculation

↓

Updated Routes
```

OSPF converges much faster than RIP.

---

# Enterprise Example

Large Enterprise:

```text
Head Office

↓

Area 0

↓

Regional Offices

↓

Branches

↓

Data Centres
```

OSPF automatically calculates the most efficient routes.

---

# Cloud Perspective

Cloud providers commonly use OSPF for:

- Hybrid Cloud Connectivity
- VPN Gateways
- Enterprise WAN Integration
- Multi-Site Networks

Although BGP is often used between organisations, OSPF is frequently used inside enterprise networks connected to cloud environments.

---

# Kubernetes Perspective

Most Kubernetes clusters do not run OSPF directly.

However, OSPF may be used in the underlying physical network connecting:

- Worker Nodes
- Storage Networks
- Load Balancers
- Data Centre Fabrics

---

# Linux Perspective

Linux supports OSPF through routing software such as:

- FRRouting (FRR)
- BIRD

Display routing table.

```bash
ip route
```

Display interfaces.

```bash
ip addr
```

Routing protocol configuration is managed by the routing daemon rather than the Linux kernel itself.

---

# OSPF Advantages

- Fast Convergence
- Highly Scalable
- Loop-Free Routing
- Supports CIDR
- Supports VLSM
- Hierarchical Design
- Efficient Bandwidth Usage

---

# OSPF Limitations

- More Complex Than RIP
- Requires Proper Area Design
- Higher CPU Usage
- More Memory Usage
- More Planning Required

---

# RIP vs OSPF

| RIP | OSPF |
|------|------|
| Distance Vector | Link-State |
| Hop Count | Cost |
| 15-Hop Limit | No Practical Hop Limit |
| Periodic Full Updates | Event-Driven LSAs |
| Slower Convergence | Faster Convergence |
| Small Networks | Enterprise Networks |

---

# Hands-on Lab

## Task 1

Display your routing table.

```bash
ip route
```

---

## Task 2

Display network interfaces.

```bash
ip addr
```

---

## Task 3

Draw an OSPF network with:

- Area 0
- Area 1
- Area 2

Identify:

- ABRs
- Backbone Routers
- Internal Routers

---

## Task 4

Explain how OSPF neighbours become fully adjacent.

---

## Task 5

Compare:

- RIP
- OSPF

List at least ten differences.

---

## Task 6

Research the five OSPF packet types and explain their purpose.

---

## Task 7

Explain how the SPF algorithm selects the best path.

---

## Task 8

Design an OSPF topology for a company with:

- Headquarters
- Three Regional Offices
- Two Data Centres
- Cloud Connectivity

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

❌ Designing too many OSPF areas unnecessarily.

✅ Keep the design simple and hierarchical.

---

❌ Ignoring Area 0 requirements.

✅ Ensure all non-backbone areas connect to Area 0.

---

❌ Misconfiguring Hello or Dead timers.

✅ Neighbor parameters must match.

---

❌ Confusing DR with the Root Bridge.

✅ DR is an OSPF concept; Root Bridge belongs to Spanning Tree Protocol (STP).

---

❌ Forgetting Router ID uniqueness.

✅ Every OSPF router must have a unique Router ID.

---

# Best Practices

- Use OSPF for medium and large enterprise networks.
- Keep Area 0 stable and well designed.
- Minimise unnecessary area complexity.
- Assign meaningful Router IDs.
- Use route summarisation at Area Border Routers where appropriate.
- Monitor OSPF neighbour relationships and convergence.

---

# Interview Questions

## Beginner

1. What is OSPF?
2. What type of routing protocol is OSPF?
3. What metric does OSPF use?
4. What is Area 0?

---

## Intermediate

1. Explain Link-State routing.
2. What is an LSA?
3. What is an ABR?
4. Why are DR and BDR elected?

---

## Architect Level

1. Design an enterprise OSPF network for multiple locations.
2. How would you divide an OSPF network into areas?
3. How would you troubleshoot an OSPF adjacency that never reaches the Full state?

---

# Summary

In this lesson, you learned:

- OSPF fundamentals
- Link-State routing
- LSDB
- SPF Algorithm
- OSPF Cost
- Neighbor Discovery
- Hello Packets
- LSAs
- Areas
- Area 0
- ABRs
- ASBRs
- DR and BDR
- OSPF packet types
- Enterprise OSPF design

OSPF is one of the most powerful and widely used Interior Gateway Protocols. By maintaining a synchronised topology database and calculating the shortest path using Dijkstra's algorithm, OSPF provides fast convergence, high scalability, and reliable routing for enterprise and cloud networks.

---

## Key Takeaways

- OSPF is a **Link-State Routing Protocol**.
- OSPF uses **Cost** as its routing metric.
- Routers maintain a synchronised **Link-State Database (LSDB)**.
- The **SPF Algorithm** calculates the shortest path.
- **Area 0** is the backbone of every OSPF deployment.
- **DR** and **BDR** reduce routing overhead on multi-access networks.
- OSPF is the preferred IGP for most enterprise environments.

---

## What's Next?

**[EIGRP Concepts](eigrp-concepts.md)**

In the next lesson, you'll learn about **EIGRP Concepts**.

You'll explore:

- What EIGRP is
- Diffusing Update Algorithm (DUAL)
- Composite Metrics
- Successor and Feasible Successor Routes
- Neighbor Relationships
- Fast Convergence
- Enterprise use cases

By the end of the lesson, you'll understand the core concepts behind Enhanced Interior Gateway Routing Protocol (EIGRP) and how it achieves fast, efficient, and reliable routing in enterprise networks.
