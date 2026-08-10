---
title: "BGP Introduction"
description: "Learn Border Gateway Protocol (BGP) — Autonomous Systems, eBGP vs iBGP, AS Path, attributes, best-path selection, and Internet and cloud routing."
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
  - bgp
  - autonomous-system
  - rebash-networking-mastery
comments: false
status: ready
---

# BGP (Border Gateway Protocol) Introduction — The Routing Protocol of the Internet

> **Border Gateway Protocol (BGP)** is the routing protocol that powers the **Internet**. Unlike routing protocols such as Routing Information Protocol (RIP), Open Shortest Path First (OSPF), and Enhanced Interior Gateway Routing Protocol (EIGRP) that operate **within an organisation**, BGP is designed to exchange routing information **between different organisations**, known as **Autonomous Systems (AS)**. Every Internet Service Provider (ISP), major cloud provider, large enterprise, and content delivery network relies on BGP to exchange millions of routes across the global Internet. Understanding BGP is essential for Cloud Architects, Network Engineers, DevOps Engineers, Site Reliability Engineers (SREs), and Platform Engineers working with enterprise networking or cloud connectivity.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 5: Routing → Lesson 7</p>

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

<div markdown>**Lesson:** 7 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand BGP fundamentals
- Learn Autonomous Systems (AS)
- Understand eBGP and iBGP
- Learn BGP path selection
- Understand BGP attributes
- Learn AS Path
- Understand Internet routing
- Explore enterprise and cloud BGP deployments

---

# Prerequisites

Complete:

- [Routing Basics](routing-fundamentals.md)
- [Static Routing](static-routing.md)
- [Dynamic Routing](dynamic-routing.md)
- [RIP](rip.md)
- [OSPF](ospf.md)
- [EIGRP Concepts](eigrp-concepts.md)

---

# Why Learn BGP?

Imagine accessing:

```text
www.google.com
```

Your request travels through:

- Your ISP
- Regional ISP
- Internet Backbone
- Cloud Provider
- Google's Network

How do thousands of independent networks know where to send your traffic?

The answer is:

```text
BGP
```

---

# What is BGP?

**Border Gateway Protocol (BGP)** is an **Exterior Gateway Protocol (EGP)** used to exchange routing information between different Autonomous Systems.

Characteristics:

- Internet Routing Protocol
- Policy-Based Routing
- Highly Scalable
- Loop Prevention
- Supports Millions of Routes

---

# Interior vs Exterior Routing

Interior Routing:

```text
One Organisation

↓

OSPF

↓

EIGRP

↓

RIP
```

Exterior Routing:

```text
Organisation A

↓

BGP

↓

Organisation B
```

---

# What is an Autonomous System?

An **Autonomous System (AS)** is a network or group of networks managed by a single administrative organisation with a common routing policy.

Examples:

- Internet Service Providers
- Cloud Providers
- Universities
- Large Enterprises

Each Autonomous System is assigned a unique:

```text
ASN

Autonomous System Number
```

---

# Autonomous System Number (ASN)

Example:

```text
Company A

↓

AS65001
```

```text
ISP

↓

AS64512
```

```text
Cloud Provider

↓

AS15169
```

Routers use ASNs to identify routing domains.

---

# eBGP

**External BGP (eBGP)** is used between different Autonomous Systems.

Example:

```text
Enterprise

AS65001

↓

ISP

AS64512
```

Routes are exchanged across organisational boundaries.

---

# iBGP

**Internal BGP (iBGP)** is used within the same Autonomous System.

Example:

```text
Data Centre A

↓

iBGP

↓

Data Centre B
```

All routers belong to the same ASN.

---

# BGP Neighbors

BGP routers establish:

```text
Neighbor Relationships
```

Unlike OSPF, neighbours are manually configured.

Example:

```text
Router A

⇄

Router B
```

Once connected:

```text
Exchange Routes
```

---

# Transport Protocol

Unlike most routing protocols:

```text
OSPF

↓

Own Protocol
```

BGP uses:

```text
TCP

Port 179
```

Transmission Control Protocol (TCP) provides reliable delivery of routing updates.

---

# Path Vector Protocol

BGP is classified as a:

```text
Path Vector Routing Protocol
```

Instead of only selecting the shortest path, BGP evaluates:

- Policies
- Attributes
- AS Paths
- Administrative Preferences

---

# AS Path

One of the most important BGP attributes is:

```text
AS Path
```

Example:

```text
AS65001

↓

AS64512

↓

AS15169
```

The AS Path records the sequence of Autonomous Systems a route has traversed.

Benefits:

- Loop Prevention
- Path Selection

Generally, shorter AS paths are preferred, although other attributes may influence the final decision.

---

# BGP Attributes

BGP uses multiple attributes to select the best route.

Common attributes include:

- AS Path
- Next Hop
- Local Preference
- Multi-Exit Discriminator (MED)
- Origin
- Weight (Vendor-specific, e.g., Cisco)

---

# Local Preference

Used **inside an Autonomous System**.

Higher Local Preference is preferred.

Example:

```text
ISP A

↓

Local Preference

200
```

```text
ISP B

↓

Local Preference

100
```

Traffic exits through ISP A.

---

# MED (Multi-Exit Discriminator)

Used to suggest a preferred entry point into an Autonomous System when multiple links exist.

Lower MED is generally preferred.

---

# Next Hop

Every BGP route contains:

```text
Next Hop
```

The next-hop router must be reachable before the route can be used.

---

# BGP Best Path Selection

BGP evaluates multiple attributes before selecting the preferred route.

A simplified decision process includes:

- Highest Weight (vendor-specific)
- Highest Local Preference
- Locally Originated Routes
- Shortest AS Path
- Lowest Origin Type
- Lowest MED
- eBGP over iBGP
- Lowest IGP Cost to Next Hop

The complete algorithm varies slightly by implementation.

---

# Route Advertisement

Example:

Cloud Provider:

```text
10.100.0.0/16
```

Advertises:

```text
Enterprise

↓

BGP Neighbor

↓

Routing Table
```

The enterprise router learns how to reach the cloud network.

---

# Internet Routing Example

```text
Home Network

↓

ISP

↓

Internet Backbone

↓

Cloud Provider

↓

Google
```

Every step relies on BGP exchanging routing information between Autonomous Systems.

---

# BGP Workflow

```text
Router Starts

↓

TCP Connection

↓

Neighbor Established

↓

Exchange Routes

↓

Apply Policies

↓

Select Best Path

↓

Install Route

↓

Forward Traffic
```

---

# Enterprise Example

Company:

```text
Head Office

↓

ISP A

↓

Internet
```

```text
↓

ISP B

↓

Internet
```

Using BGP:

- Primary ISP
- Backup ISP
- Load Sharing
- Redundant Internet Connectivity

---

# Cloud Perspective

BGP is widely used in cloud networking for:

- AWS Direct Connect
- Azure ExpressRoute
- Google Cloud Interconnect
- VPN Gateways
- Hybrid Cloud Connectivity
- Multi-Cloud Routing

BGP enables dynamic route exchange between on-premises and cloud networks.

---

# Kubernetes Perspective

Some Kubernetes networking solutions use BGP to advertise:

- Pod Networks
- Service Networks
- Load Balancer IPs

Examples include:

- Calico
- Cilium (optional configurations)

This allows seamless integration with enterprise routing infrastructure.

---

# Linux Perspective

Linux supports BGP through routing software such as:

- FRRouting (FRR)
- BIRD
- GoBGP

Display routing table.

```bash
ip route
```

Display interfaces.

```bash
ip addr
```

Routing daemon configuration is handled by the chosen BGP software.

---

# Advantages of BGP

- Internet Scale
- Policy-Based Routing
- Highly Scalable
- Supports Redundant Providers
- Loop Prevention
- Flexible Traffic Engineering

---

# Limitations of BGP

- Complex Configuration
- Slower Convergence than IGPs
- Policy Management Required
- Requires Careful Planning
- Large Routing Tables

---

# OSPF vs BGP

| OSPF | BGP |
|------|-----|
| Interior Gateway Protocol | Exterior Gateway Protocol |
| Link-State | Path Vector |
| Cost Metric | Multiple Attributes |
| Enterprise Internal Routing | Internet Routing |
| Fast Convergence | Policy-Based Routing |

---

# Hands-on Lab

## Task 1

Display routing table.

```bash
ip route
```

---

## Task 2

Research the ASN used by:

- Your ISP
- Google
- Amazon
- Microsoft

---

## Task 3

Draw:

- Enterprise
- ISP
- Cloud Provider

Show:

- eBGP Sessions
- iBGP Sessions

---

## Task 4

Explain:

- eBGP
- iBGP

List five differences.

---

## Task 5

Research BGP attributes.

Explain:

- AS Path
- Local Preference
- MED
- Next Hop

---

## Task 6

Design a dual-ISP enterprise Internet connection using BGP.

---

## Task 7

Explain why BGP uses TCP instead of its own transport protocol.

---

## Task 8

Research how AWS Direct Connect, Azure ExpressRoute, or Google Cloud Interconnect uses BGP.

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

❌ Assuming BGP always selects the shortest AS Path.

✅ Multiple attributes influence route selection.

---

❌ Confusing iBGP with eBGP.

✅ Remember that iBGP operates within an AS, while eBGP operates between ASes.

---

❌ Ignoring routing policies.

✅ BGP is policy-driven, not purely shortest-path based.

---

❌ Expecting BGP to converge as quickly as OSPF.

✅ BGP prioritises scalability and stability over rapid convergence.

---

❌ Misconfiguring BGP neighbours.

✅ Verify neighbour IPs, ASNs, and TCP connectivity.

---

# Best Practices

- Use BGP for Internet and multi-provider connectivity.
- Apply routing policies carefully.
- Filter incoming and outgoing routes appropriately.
- Monitor BGP sessions continuously.
- Document Autonomous System relationships.
- Test failover in dual-ISP environments.

---

# Interview Questions

## Beginner

1. What is BGP?
2. What is an Autonomous System?
3. What is an ASN?
4. What port does BGP use?

---

## Intermediate

1. Compare eBGP and iBGP.
2. Explain AS Path.
3. What are BGP attributes?
4. How does BGP prevent routing loops?

---

## Architect Level

1. Design a multi-cloud network using BGP.
2. How would you implement redundant Internet connectivity with two ISPs?
3. Explain BGP best-path selection in a production environment.

---

# Summary

In this lesson, you learned:

- BGP fundamentals
- Autonomous Systems
- AS Numbers
- eBGP
- iBGP
- Path Vector routing
- AS Path
- BGP attributes
- Best-path selection
- Enterprise and cloud BGP deployments

BGP is the routing protocol that connects the world's networks. By exchanging routes between Autonomous Systems and applying flexible routing policies, BGP enables reliable, scalable communication across the global Internet while supporting hybrid cloud, multi-cloud, and enterprise connectivity.

---

## Key Takeaways

- BGP is an **Exterior Gateway Protocol (EGP)**.
- BGP is a **Path Vector Routing Protocol**.
- BGP exchanges routes between **Autonomous Systems (AS)**.
- **eBGP** operates between ASes; **iBGP** operates within an AS.
- BGP uses **TCP Port 179**.
- **AS Path** helps prevent routing loops and influences path selection.
- BGP is the foundation of Internet routing and hybrid cloud connectivity.

---

## What's Next?

**[Default Routes](default-routes.md)**

In the next lesson, you'll learn about **Default Routes**.

You'll explore:

- What a Default Route is
- Default Gateway vs Default Route
- IPv4 and IPv6 Default Routes
- Route Lookup Process
- Internet Routing
- Static and Dynamic Default Routes
- Enterprise best practices

By the end of the lesson, you'll understand how default routes simplify routing tables and enable devices and routers to reach unknown destinations efficiently.
