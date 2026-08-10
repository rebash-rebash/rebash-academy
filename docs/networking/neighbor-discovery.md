---
title: "Neighbor Discovery"
description: "Learn Neighbor Discovery Protocol (NDP) — Neighbor Solicitation, Neighbor Advertisement, Router Discovery, DAD, and how IPv6 replaces ARP."
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
  - ndp
  - icmpv6
  - arp
  - rebash-networking-mastery
comments: false
status: ready
---

# Neighbor Discovery Protocol (NDP) — IPv6 Neighbor Discovery and Address Resolution

> **Neighbor Discovery Protocol (NDP)** is one of the most important protocols in IPv6. It replaces several IPv4 protocols, including **ARP (Address Resolution Protocol)**, **ICMP Router Discovery**, and parts of **ICMP Redirect**. NDP enables IPv6 devices to discover neighbouring devices, identify routers, resolve link-layer (MAC) addresses, perform Duplicate Address Detection (DAD), and automatically configure themselves. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand how Neighbor Discovery works.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 3: IPv6 → Lesson 5</p>

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

<div markdown>**Lesson:** 5 of 7</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Neighbor Discovery Protocol (NDP)
- Explain how IPv6 replaces ARP
- Understand Neighbor Solicitation (NS)
- Understand Neighbor Advertisement (NA)
- Learn Router Solicitation (RS)
- Learn Router Advertisement (RA)
- Understand Duplicate Address Detection (DAD)
- Compare ARP and NDP

---

# Prerequisites

Complete:

- [Why IPv6](why-ipv6.md)
- [IPv6 Structure](ipv6-structure.md)
- [Types of IPv6 Addresses](ipv6-address-types.md)
- [SLAAC](slaac.md)

---

# Why Learn Neighbor Discovery?

Suppose your computer wants to communicate with another IPv6 device.

Questions that must be answered include:

- What is the destination MAC address?
- Is the destination on the same network?
- Who is the default router?
- Is the IPv6 address already in use?

In IPv4, different protocols answered these questions.

In IPv6:

```text
Neighbor Discovery Protocol

↓

Handles Everything
```

---

# What is Neighbor Discovery Protocol?

**Neighbor Discovery Protocol (NDP)** is an IPv6 protocol based on **ICMPv6**.

It performs several important networking functions:

- Neighbor Discovery
- Address Resolution
- Router Discovery
- Prefix Discovery
- Duplicate Address Detection
- Neighbor Reachability Detection
- Redirects

---

# Why Was ARP Removed?

IPv4 uses:

```text
ARP

↓

Find MAC Address
```

IPv6 does **not** use ARP.

Instead:

```text
Neighbor Discovery

↓

Uses ICMPv6
```

This creates a more efficient and integrated networking protocol.

---

# Functions of NDP

Neighbor Discovery provides:

- Router Discovery
- Prefix Discovery
- Address Resolution
- Neighbor Discovery
- Duplicate Address Detection
- Reachability Detection
- Router Redirects

---

# NDP Messages

Neighbor Discovery uses five primary ICMPv6 message types:

```text
Router Solicitation (RS)

↓

Router Advertisement (RA)

↓

Neighbor Solicitation (NS)

↓

Neighbor Advertisement (NA)

↓

Redirect
```

---

# Router Solicitation (RS)

When a device joins a network, it can immediately request router information.

Device:

```text
Who is my router?
```

Router:

```text
Here I am.
```

The device sends a **Router Solicitation (RS)** message.

---

# Router Advertisement (RA)

Routers periodically send **Router Advertisements**.

They contain:

- Network Prefix
- Prefix Length
- Default Gateway Information
- Maximum Transmission Unit (MTU) Information
- Configuration Flags

These advertisements are also used by Stateless Address Autoconfiguration (SLAAC).

---

# Neighbor Solicitation (NS)

Neighbor Solicitation replaces the ARP Request.

Example:

```text
Who owns

2001:db8::25 ?
```

Instead of broadcasting the request to every device, IPv6 sends it to a **Solicited-Node Multicast Address**, greatly reducing unnecessary traffic.

---

# Neighbor Advertisement (NA)

The destination device replies:

```text
I own

2001:db8::25

My MAC is

00:11:22:33:44:55
```

This replaces the ARP Reply used in IPv4.

---

# Duplicate Address Detection (DAD)

Before using an IPv6 address:

```text
Generate Address

↓

Neighbor Solicitation

↓

Any Reply?

↓

No

↓

Address Valid
```

If another device responds, the address is already in use and cannot be assigned.

---

# Neighbor Reachability Detection (NUD)

IPv6 continuously verifies whether neighbouring devices are still reachable.

Example:

```text
Server

↓

Still Reachable?

↓

Yes

↓

Continue Communication
```

If a neighbour becomes unreachable, the operating system updates its neighbour cache accordingly.

---

# Redirect Messages

Suppose:

```text
Host

↓

Wrong Router
```

The router replies:

```text
Better Route Available

↓

Use Another Router
```

This improves routing efficiency within the local network.

---

# NDP Workflow

```text
System Boots

↓

Create Link-Local Address

↓

Duplicate Address Detection

↓

Router Solicitation

↓

Router Advertisement

↓

Generate Global Address

↓

Neighbor Solicitation

↓

Neighbor Advertisement

↓

Communication Begins
```

---

# ARP vs NDP

| ARP (IPv4) | NDP (IPv6) |
|------------|------------|
| Uses ARP Protocol | Uses ICMPv6 |
| Broadcast Requests | Multicast Requests |
| Resolves MAC Addresses | Resolves MAC Addresses |
| Address Resolution Only | Multiple Network Functions |

---

# Broadcast vs Multicast

IPv4:

```text
ARP Request

↓

Broadcast

↓

Every Device Receives Packet
```

IPv6:

```text
Neighbor Solicitation

↓

Solicited-Node Multicast

↓

Only Relevant Devices Receive Packet
```

This significantly reduces unnecessary network traffic.

---

# Enterprise Example

Employee Laptop:

```text
Connect Network

↓

Router Solicitation

↓

Router Advertisement

↓

SLAAC

↓

Neighbor Discovery

↓

Ready
```

No manual configuration is required.

---

# Cloud Perspective

Cloud environments use Neighbor Discovery for:

- Virtual Machine Communication
- IPv6 Address Resolution
- Router Discovery
- Default Gateway Discovery

Many cloud platforms optimise or virtualise Neighbor Discovery to improve scalability.

---

# Kubernetes Perspective

Linux nodes participating in IPv6 Kubernetes clusters use Neighbor Discovery for:

- Node Networking
- Gateway Discovery
- Neighbor Reachability

The underlying Linux networking stack performs NDP automatically.

---

# Linux Perspective

Display IPv6 neighbours.

```bash
ip -6 neigh
```

Example:

```text
2001:db8::20

lladdr

00:11:22:33:44:55

REACHABLE
```

---

Display IPv6 addresses.

```bash
ip -6 addr
```

---

Display IPv6 routes.

```bash
ip -6 route
```

---

# Neighbor Cache

Linux maintains a Neighbor Cache similar in purpose to the ARP cache.

Display:

```bash
ip -6 neigh
```

Example states:

```text
REACHABLE

STALE

DELAY

PROBE
```

These states help Linux determine neighbour availability.

---

# Hands-on Lab

## Task 1

Display IPv6 neighbours.

```bash
ip -6 neigh
```

---

## Task 2

Display IPv6 addresses.

```bash
ip -6 addr
```

---

## Task 3

Display IPv6 routing information.

```bash
ip -6 route
```

---

## Task 4

Draw the Neighbor Discovery workflow from system startup to successful communication.

---

## Task 5

Create a comparison table for:

- ARP
- Neighbor Discovery

---

## Task 6

Research the ICMPv6 message types used by Neighbor Discovery.

---

## Task 7

Explain why IPv6 uses multicast instead of broadcast for address resolution.

---

## Task 8

Observe the Neighbor Cache on your Linux system before and after communicating with another IPv6-enabled host (if available). Note how the neighbour state changes.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip -6 neigh` | Display IPv6 Neighbor Cache |
| `ip -6 addr` | Display IPv6 addresses |
| `ip -6 route` | Display IPv6 routes |
| `ping -6` | Test IPv6 connectivity |
| `ip link` | Display network interfaces |

---

# Common Mistakes

❌ Assuming IPv6 uses ARP.

✅ IPv6 uses Neighbor Discovery based on ICMPv6.

---

❌ Confusing Router Advertisement with Neighbor Advertisement.

✅ RA provides network information; NA responds to Neighbor Solicitation.

---

❌ Believing IPv6 uses broadcast.

✅ IPv6 replaces broadcast with multicast.

---

❌ Ignoring Duplicate Address Detection.

✅ DAD prevents duplicate IPv6 addresses on the network.

---

❌ Assuming NDP only resolves MAC addresses.

✅ NDP performs multiple functions beyond address resolution.

---

# Best Practices

- Understand all major NDP message types.
- Monitor the Neighbor Cache during troubleshooting.
- Allow required ICMPv6 traffic through firewalls.
- Verify Router Advertisements in IPv6 deployments.
- Understand Neighbor Discovery before deploying SLAAC-based networks.
- Use multicast efficiently by avoiding unnecessary filtering of essential ICMPv6 messages.

---

# Interview Questions

## Beginner

1. What is Neighbor Discovery Protocol?
2. Which protocol replaced ARP in IPv6?
3. What is Neighbor Solicitation?
4. What is Neighbor Advertisement?

---

## Intermediate

1. Explain the Neighbor Discovery workflow.
2. Compare ARP and NDP.
3. Why does IPv6 use multicast instead of broadcast?
4. What is Duplicate Address Detection?

---

## Architect Level

1. Explain how Neighbor Discovery supports SLAAC.
2. How would you troubleshoot IPv6 neighbour discovery failures?
3. Why is ICMPv6 essential for IPv6 operation?

---

# Summary

In this lesson, you learned:

- Neighbor Discovery Protocol
- Router Solicitation
- Router Advertisement
- Neighbor Solicitation
- Neighbor Advertisement
- Duplicate Address Detection
- Neighbor Reachability Detection
- ARP vs NDP
- Linux Neighbor Cache

Neighbor Discovery is one of the core technologies that enables IPv6 networking. By replacing multiple IPv4 protocols with a unified ICMPv6-based framework, NDP simplifies address resolution, router discovery, reachability detection, and automatic configuration while reducing unnecessary network traffic through multicast communication.

---

## Key Takeaways

- Neighbor Discovery replaces ARP in IPv6.
- NDP is built on **ICMPv6**.
- Neighbor Solicitation replaces ARP Requests.
- Neighbor Advertisement replaces ARP Replies.
- Router Advertisements enable SLAAC.
- Duplicate Address Detection prevents address conflicts.
- IPv6 uses multicast instead of broadcast for greater efficiency.

---

## What's Next?

**[IPv6 Routing](ipv6-routing.md)**

In the next lesson, you'll learn about **IPv6 Routing**.

You'll explore:

- IPv6 routing fundamentals
- Static and dynamic IPv6 routing
- Default routes
- Routing tables
- OSPFv3 and other IPv6 routing protocols
- Linux IPv6 routing
- Enterprise and cloud routing design

By the end of the lesson, you'll understand how IPv6 packets are routed across local networks, enterprise infrastructures, cloud environments, and the Internet.
