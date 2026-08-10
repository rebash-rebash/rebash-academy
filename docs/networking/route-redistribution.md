---
title: "Route Redistribution"
description: "Learn route redistribution — sharing routes between OSPF, EIGRP, RIP, BGP, and static routing, seed metrics, filtering, tagging, and loop prevention."
difficulty: advanced
estimated_time: "120 min"
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
  - redistribution
  - ospf
  - bgp
  - rebash-networking-mastery
comments: false
status: ready
---

# Route Redistribution — Sharing Routes Between Different Routing Protocols

> **Route Redistribution** is the process of exchanging routes between **different routing protocols**. In large enterprise networks, organisations often run multiple routing protocols such as **Open Shortest Path First (OSPF)**, **Enhanced Interior Gateway Routing Protocol (EIGRP)**, **Routing Information Protocol (RIP)**, **Static Routing**, and **Border Gateway Protocol (BGP)**. Since each protocol maintains its own routing information, routers must redistribute routes to allow communication across the entire network. Route redistribution is one of the most advanced routing topics and is widely used during network migrations, mergers, hybrid cloud deployments, and multi-vendor enterprise environments. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand the fundamentals of route redistribution.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 5: Routing → Lesson 10</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Advanced</div>

<div markdown>**Reading Time:** 120 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Routing</div>

<div markdown>**Lesson:** 10 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Route Redistribution
- Learn why redistribution is needed
- Redistribute between routing protocols
- Understand seed metrics
- Prevent routing loops
- Learn route filtering
- Understand enterprise migration strategies
- Apply redistribution in hybrid cloud environments

---

# Prerequisites

Complete:

- [Routing Basics](routing-fundamentals.md)
- [Static Routing](static-routing.md)
- [Dynamic Routing](dynamic-routing.md)
- [RIP](rip.md)
- [OSPF](ospf.md)
- [EIGRP Concepts](eigrp-concepts.md)
- [BGP Introduction](bgp-introduction.md)
- [Default Routes](default-routes.md)
- [Route Summarization](route-summarization.md)

---

# Why Learn Route Redistribution?

Imagine a company has grown over many years.

Old Branches:

```text
RIP
```

Core Network:

```text
OSPF
```

Internet Edge:

```text
BGP
```

Data Centre:

```text
Static Routes
```

Each routing protocol knows only its own routes.

Without redistribution:

```text
RIP

❌

Cannot Learn

OSPF Routes
```

Communication fails.

---

# What is Route Redistribution?

Route Redistribution is the process of importing routes learned from one routing protocol into another routing protocol.

Example:

```text
OSPF

↓

Redistribute

↓

BGP
```

or

```text
Static Routes

↓

Redistribute

↓

OSPF
```

---

# Why is Redistribution Needed?

Organisations commonly require redistribution during:

- Enterprise Mergers
- Network Upgrades
- Routing Protocol Migration
- Multi-Vendor Deployments
- Hybrid Cloud Integration
- ISP Connectivity

---

# Example Network

```text
Branch Office

↓

RIP

↓

Core Router

↓

OSPF

↓

Internet Edge

↓

BGP
```

The Core Router performs redistribution between the routing domains.

---

# Redistribution Router

A router participating in multiple routing protocols is called a:

```text
Redistribution Router
```

Example:

```text
OSPF

⇄

Redistribution Router

⇄

BGP
```

It exchanges routing information between protocols.

---

# Common Redistribution Scenarios

- Static → OSPF
- Static → EIGRP
- OSPF → BGP
- BGP → OSPF
- RIP → OSPF
- OSPF → EIGRP
- EIGRP → BGP

---

# Seed Metric

Different routing protocols use different metrics.

Examples:

| Protocol | Metric |
|-----------|--------|
| RIP | Hop Count |
| OSPF | Cost |
| EIGRP | Composite Metric |
| BGP | Path Attributes |

When redistributing routes, the receiving protocol often requires a:

```text
Seed Metric
```

This provides an initial metric for the redistributed routes.

---

# Example

Static Route:

```text
192.168.50.0/24
```

Redistributed into:

```text
OSPF
```

OSPF assigns an appropriate metric before advertising the route.

---

# One-Way Redistribution

Routes move in only one direction.

```text
OSPF

↓

BGP
```

OSPF routes appear in BGP.

BGP routes are **not** imported into OSPF.

---

# Two-Way Redistribution

Routes move in both directions.

```text
OSPF

⇄

EIGRP
```

Both routing protocols exchange routing information.

This design requires careful planning to avoid routing loops.

---

# Routing Loops

Improper redistribution can create:

```text
Routing Loop
```

Example:

```text
OSPF

↓

EIGRP

↓

OSPF

↓

Repeated Route
```

The same route circulates continuously.

---

# Loop Prevention

Common techniques include:

- Route Filtering
- Route Tagging
- Administrative Distance
- Summarisation
- Careful Redistribution Design

---

# Route Tagging

A redistributed route can be assigned a:

```text
Tag
```

Example:

```text
Route

↓

Tag

100
```

If the route returns through another protocol:

```text
Already Tagged

↓

Ignore
```

This prevents routing loops.

---

# Route Filtering

Not every route should be redistributed.

Filtering allows administrators to control:

- Imported Routes
- Exported Routes
- Prefixes
- Network Ranges

Benefits:

- Smaller Routing Tables
- Better Security
- Reduced Complexity

---

# Administrative Distance

When multiple routing protocols advertise the same destination:

```text
OSPF

110
```

```text
Static

1
```

The route with the lower Administrative Distance is preferred.

---

# Redistribution Workflow

```text
Learn Route

↓

Apply Policy

↓

Assign Seed Metric

↓

Advertise

↓

Receiving Protocol

↓

Routing Table
```

---

# Enterprise Example

Company:

```text
Legacy Network

↓

RIP
```

↓

```text
Migration Router
```

↓

```text
Modern Network

OSPF
```

During migration:

```text
Redistribution

↓

Users Continue Working
```

The migration can occur without a complete network redesign.

---

# Cloud Perspective

Hybrid cloud environments often require redistribution between:

- BGP
- OSPF
- Static Routes

Examples:

- On-Premises Network
- Virtual Private Network (VPN) Gateway
- Cloud Router
- Data Centre

Redistribution enables seamless communication across different routing domains.

---

# Kubernetes Perspective

Traditional Kubernetes clusters do not perform route redistribution directly.

However, enterprise infrastructure may redistribute:

- Pod Networks
- Service Networks
- Cloud Routes

between BGP and internal routing protocols.

---

# Linux Perspective

Linux itself forwards packets using the routing table.

Route redistribution is performed by routing software such as:

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

Routing daemon configuration determines how redistribution occurs.

---

# Advantages of Route Redistribution

- Supports Multiple Routing Protocols
- Enables Gradual Network Migration
- Improves Interoperability
- Connects Legacy and Modern Networks
- Supports Hybrid Cloud Designs

---

# Challenges

- Routing Loops
- Metric Translation
- Administrative Complexity
- Increased CPU Usage
- Troubleshooting Complexity

---

# Hands-on Lab

## Task 1

Display your routing table.

```bash
ip route
```

---

## Task 2

Draw a network containing:

- RIP
- OSPF
- BGP

Identify where redistribution occurs.

---

## Task 3

Compare:

- One-Way Redistribution
- Two-Way Redistribution

---

## Task 4

Research Seed Metrics.

Explain why they are required.

---

## Task 5

Explain Route Tagging.

Show how it prevents routing loops.

---

## Task 6

Research Administrative Distance values for:

- Connected
- Static
- RIP
- OSPF
- EIGRP
- BGP

---

## Task 7

Design a migration from RIP to OSPF using route redistribution.

---

## Task 8

Research how hybrid cloud environments use BGP and route redistribution.

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

❌ Redistributing all routes without filtering.

✅ Apply route filters and policies.

---

❌ Ignoring seed metrics.

✅ Configure appropriate metrics for redistributed routes.

---

❌ Creating two-way redistribution without loop prevention.

✅ Use route tagging and careful design.

---

❌ Forgetting administrative distance.

✅ Verify route preference during troubleshooting.

---

❌ Using redistribution when simpler designs are possible.

✅ Keep routing architectures as simple as practical.

---

# Best Practices

- Redistribute only necessary routes.
- Use route filtering to limit advertisements.
- Configure appropriate seed metrics.
- Use route tagging to prevent loops.
- Document redistribution policies.
- Test redistribution thoroughly before production deployment.

---

# Interview Questions

## Beginner

1. What is Route Redistribution?
2. Why is redistribution needed?
3. What is a seed metric?
4. What is a redistribution router?

---

## Intermediate

1. Explain one-way and two-way redistribution.
2. Why can redistribution create routing loops?
3. What is route filtering?
4. What is route tagging?

---

## Architect Level

1. Design a routing migration from RIP to OSPF.
2. Explain redistribution between OSPF and BGP in a hybrid cloud.
3. How would you troubleshoot routing loops caused by redistribution?

---

# Summary

In this lesson, you learned:

- Route Redistribution
- Redistribution Routers
- Seed Metrics
- One-Way Redistribution
- Two-Way Redistribution
- Route Tagging
- Route Filtering
- Administrative Distance
- Hybrid Cloud Routing
- Enterprise Migration Strategies

Route redistribution enables different routing protocols to exchange routing information, making it possible to connect legacy and modern networks, integrate cloud environments, and migrate between routing technologies without disrupting connectivity. Proper planning, filtering, tagging, and metric management are essential to prevent routing loops and maintain a stable network.

---

## Key Takeaways

- Route Redistribution shares routes between **different routing protocols**.
- Seed metrics translate routing information between protocols.
- One-way redistribution is simpler and less prone to routing loops.
- Two-way redistribution requires careful loop prevention.
- Route filtering and route tagging improve stability and security.
- Redistribution is commonly used during enterprise migrations and hybrid cloud deployments.

---

# Module 5 Complete!

Congratulations! You have successfully completed **Module 5: Routing**.

You now understand:

- Routing Basics
- Static Routing
- Dynamic Routing
- RIP
- OSPF
- EIGRP Concepts
- BGP Introduction
- Default Routes
- Route Summarization
- Route Redistribution

You now have a solid understanding of Layer 3 routing concepts, from simple static routes to enterprise-scale dynamic routing and Internet connectivity.

---

## What's Next?

**[Module 5 Summary — Routing](module-5-routing-summary.md)**
