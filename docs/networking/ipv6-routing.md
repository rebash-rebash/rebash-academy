---
title: "IPv6 Routing"
description: "Learn IPv6 routing — routing tables, longest prefix match, static and dynamic routes, OSPFv3, RIPng, MP-BGP, and Linux IPv6 route management."
difficulty: intermediate
estimated_time: "90 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 3 · IPv6"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - ipv6
  - routing
  - ospf
  - bgp
  - rebash-networking-mastery
comments: false
status: ready
---

# IPv6 Routing — Understanding How IPv6 Packets Travel Across Networks

> **IPv6 Routing** is the process of forwarding IPv6 packets between different networks. Just like IPv4 routing, IPv6 routers examine the destination address, consult the routing table, and forward packets toward their destination. However, IPv6 introduces improvements such as simplified packet headers, hierarchical addressing, efficient route aggregation, and modern routing protocols like **OSPFv3**, **IS-IS for IPv6**, and **MP-BGP**. Understanding IPv6 routing is essential for Linux administrators, DevOps engineers, Cloud Architects, Platform Engineers, Site Reliability Engineers (SREs), and Network Engineers.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 3: IPv6 → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** IPv6</div>

<div markdown>**Lesson:** 6 of 7</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand IPv6 routing fundamentals
- Learn how routers forward IPv6 packets
- Understand IPv6 routing tables
- Configure static IPv6 routes
- Learn about dynamic IPv6 routing protocols
- Understand default IPv6 routes
- View IPv6 routes in Linux
- Apply IPv6 routing in enterprise and cloud environments

---

# Prerequisites

Complete:

- [Why IPv6](why-ipv6.md)
- [IPv6 Structure](ipv6-structure.md)
- [Types of IPv6 Addresses](ipv6-address-types.md)
- [SLAAC](slaac.md)
- [Neighbor Discovery](neighbor-discovery.md)

---

# Why Learn IPv6 Routing?

Suppose your laptop has the address:

```text
2001:db8:1::10
```

A web server has:

```text
2001:db8:100::20
```

Since they belong to different networks:

```text
Direct Communication

❌ Not Possible
```

A router forwards packets between them.

---

# What is Routing?

Routing is the process of selecting the best path for packets to travel between networks.

Example:

```text
Laptop

↓

Router

↓

Internet

↓

Server
```

The router determines where to send each packet based on its routing table.

---

# IPv6 Routing Process

```text
Packet Arrives

↓

Destination Address Examined

↓

Routing Table Lookup

↓

Best Route Selected

↓

Packet Forwarded
```

---

# IPv6 Routing Table

Every IPv6 router maintains a routing table.

Example:

| Destination | Next Hop |
|--------------|----------|
| `2001:db8:1::/64` | Direct |
| `2001:db8:2::/64` | Router A |
| `2001:db8:3::/64` | Router B |
| `::/0` | Internet Gateway |

---

# Longest Prefix Match

IPv6 routers always choose the **most specific matching route**.

Example:

Destination:

```text
2001:db8:1:10::5
```

Available routes:

```text
2001:db8::/32

2001:db8:1::/48

2001:db8:1:10::/64
```

The router selects:

```text
2001:db8:1:10::/64
```

because it has the longest matching prefix.

---

# Direct Routing

If the destination belongs to the same subnet:

```text
Host A

↓

Host B
```

No router is required.

Neighbor Discovery resolves the destination's Media Access Control (MAC) address.

---

# Indirect Routing

If the destination is on another network:

```text
Host

↓

Default Router

↓

Remote Network

↓

Destination
```

The packet is forwarded to the default gateway.

---

# Default Route

The IPv6 default route is:

```text
::/0
```

Equivalent in IPv4:

```text
0.0.0.0/0
```

This route matches all destinations that are not found elsewhere in the routing table.

---

# Static Routing

Static routes are manually configured.

Example:

```text
Destination

2001:db8:50::/64

↓

Next Hop

2001:db8:1::1
```

Advantages:

- Simple
- Predictable
- No routing protocol overhead

Disadvantages:

- Manual updates
- Limited scalability

---

# Dynamic Routing

Large networks use routing protocols to exchange routing information automatically.

Common IPv6 routing protocols include:

- OSPFv3
- IS-IS for IPv6
- RIPng
- Multiprotocol Border Gateway Protocol (MP-BGP)

These protocols adapt automatically when network topology changes.

---

# OSPFv3

**OSPFv3** is the IPv6 version of the Open Shortest Path First (OSPF) routing protocol.

Features:

- Link-State Routing
- Fast Convergence
- Hierarchical Design
- Enterprise Routing

Commonly used in enterprise networks.

---

# RIPng

**RIPng (Routing Information Protocol next generation)** is the IPv6 version of Routing Information Protocol (RIP).

Characteristics:

- Simple configuration
- Small networks
- Hop-count based routing
- Maximum 15 hops

Less common in large production environments.

---

# MP-BGP

**Multiprotocol BGP (MP-BGP)** enables Border Gateway Protocol (BGP) to carry IPv6 routes.

Used by:

- Internet Service Providers
- Cloud Providers
- Large Enterprises
- Global Wide Area Networks (WANs)

It is the standard protocol for exchanging IPv6 routes across the Internet.

---

# Route Aggregation

IPv6 supports route summarisation.

Example:

Instead of:

```text
2001:db8:1::/64

2001:db8:2::/64

2001:db8:3::/64

2001:db8:4::/64
```

Summarise as:

```text
2001:db8::/62
```

Benefits:

- Smaller routing tables
- Faster lookups
- Better scalability

---

# Enterprise Example

Company:

```text
Head Office

↓

2001:db8:100::/48
```

Branch Offices:

```text
2001:db8:100:1::/64

2001:db8:100:2::/64

2001:db8:100:3::/64
```

Core routers summarise routes for improved efficiency.

---

# Cloud Perspective

Cloud providers support IPv6 routing for:

- Virtual Private Clouds (VPCs)
- Virtual Networks (VNets)
- Internet Gateways
- Transit Gateways
- Virtual Private Network (VPN) Connections
- Load Balancers

IPv6 routes are managed similarly to IPv4 routes.

---

# Kubernetes Perspective

In IPv6-enabled Kubernetes clusters:

- Nodes route Pod traffic
- Container Network Interface (CNI) plugins manage IPv6 routing
- Services advertise reachable IPv6 addresses
- Dual-stack clusters support both IPv4 and IPv6

Proper routing is essential for Pod-to-Pod and Pod-to-Service communication.

---

# Linux Perspective

Display IPv6 routes.

```bash
ip -6 route
```

Example output:

```text
default via fe80::1 dev eth0

2001:db8:1::/64 dev eth0
```

---

# Add a Static IPv6 Route

Example:

```bash
sudo ip -6 route add 2001:db8:50::/64 via 2001:db8:1::1
```

---

# Delete a Static Route

```bash
sudo ip -6 route del 2001:db8:50::/64
```

---

# Show IPv6 Neighbor Cache

```bash
ip -6 neigh
```

Useful when troubleshooting next-hop reachability.

---

# IPv6 Routing Workflow

```text
Host Creates Packet

↓

Neighbor Discovery

↓

Default Router

↓

Routing Table Lookup

↓

Best Route Selected

↓

Forward Packet

↓

Destination Network
```

---

# Hands-on Lab

## Task 1

Display IPv6 routes.

```bash
ip -6 route
```

Identify:

- Default Route
- Directly Connected Networks

---

## Task 2

Display IPv6 neighbours.

```bash
ip -6 neigh
```

---

## Task 3

Identify the default IPv6 gateway on your Linux system.

---

## Task 4

Research IPv6 routing support in your cloud provider.

---

## Task 5

Draw a network showing:

- Client
- Router
- Internet
- Server

Illustrate how IPv6 packets travel.

---

## Task 6

Research the differences between:

- OSPFv3
- RIPng
- MP-BGP

Summarise where each protocol is commonly used.

---

## Task 7

Add and remove a static IPv6 route in a lab environment.

---

## Task 8

Create an IPv6 routing design for an enterprise with:

- Headquarters
- Two Branch Offices
- Cloud Environment

Include summarised prefixes where appropriate.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip -6 route` | Display IPv6 routing table |
| `ip -6 addr` | Display IPv6 addresses |
| `ip -6 neigh` | Display Neighbor Cache |
| `ping -6` | Test IPv6 connectivity |
| `traceroute -6` | Trace IPv6 packet path |

---

# Common Mistakes

❌ Forgetting the default route.

✅ Verify `::/0` exists when Internet connectivity is required.

---

❌ Assuming IPv6 routing differs completely from IPv4.

✅ The routing principles are similar, but IPv6 uses different protocols and addressing.

---

❌ Ignoring route summarisation.

✅ Aggregate routes whenever practical.

---

❌ Using static routes in large dynamic environments.

✅ Prefer dynamic routing protocols for scalability.

---

❌ Blocking ICMPv6.

✅ Essential ICMPv6 messages are required for proper IPv6 operation.

---

# Best Practices

- Use route summarisation to reduce routing table size.
- Deploy dynamic routing in enterprise environments.
- Keep static routes limited to simple or specialised scenarios.
- Monitor routing tables regularly.
- Allow required ICMPv6 traffic.
- Document IPv6 routing policies and network topology.

---

# Interview Questions

## Beginner

1. What is IPv6 routing?
2. What is the IPv6 default route?
3. What is the purpose of a routing table?
4. What is the difference between direct and indirect routing?

---

## Intermediate

1. Explain the longest prefix match rule.
2. Compare static and dynamic IPv6 routing.
3. What is OSPFv3?
4. Why is route aggregation important?

---

## Architect Level

1. Design an IPv6 routing architecture for a global enterprise.
2. Explain how IPv6 routing works in cloud environments.
3. How would you troubleshoot IPv6 routing failures across multiple sites?

---

# Summary

In this lesson, you learned:

- IPv6 routing fundamentals
- Routing tables
- Longest prefix matching
- Default routes
- Static routing
- Dynamic routing
- OSPFv3
- RIPng
- MP-BGP
- Linux IPv6 routing

IPv6 routing follows the same core principles as IPv4 routing while benefiting from hierarchical addressing, efficient route aggregation, and modern routing protocols. Understanding IPv6 routing is essential for building scalable enterprise networks, cloud infrastructures, and next-generation Internet connectivity.

---

## Key Takeaways

- IPv6 routers forward packets using routing tables.
- `::/0` represents the IPv6 default route.
- Longest prefix match determines the best route.
- Static routes are simple but not highly scalable.
- Dynamic routing protocols automatically exchange route information.
- Route aggregation improves routing efficiency and scalability.

---

## What's Next?

**[IPv4 vs IPv6](ipv4-vs-ipv6.md)**

In the next lesson, you'll learn about **IPv4 vs IPv6**.

You'll explore:

- Feature-by-feature comparison
- Address size
- Header format
- Routing differences
- Security improvements
- Performance considerations
- Enterprise adoption
- Cloud networking comparisons

By the end of the lesson, you'll clearly understand the differences between IPv4 and IPv6 and know when and why each protocol is used in modern networking environments.
