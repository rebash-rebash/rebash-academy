---
title: "IPv4 vs IPv6"
description: "Compare IPv4 and IPv6 — address space, headers, ARP vs NDP, SLAAC, NAT, routing, Dual Stack migration, and Linux verification commands."
difficulty: beginner
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
  - ipv4
  - ipv6
  - dual-stack
  - rebash-networking-mastery
comments: false
status: ready
---

# IPv4 vs IPv6 — Understanding the Differences Between Internet Protocol Versions

> **IPv4** and **IPv6** are the two versions of the Internet Protocol used to identify devices and enable communication across networks. IPv4 has powered the Internet for decades, while IPv6 was developed to overcome IPv4 limitations such as address exhaustion and to support the growing number of Internet-connected devices. Today, most organisations operate in **Dual Stack** mode, where both IPv4 and IPv6 coexist. Understanding the differences between IPv4 and IPv6 is essential for Linux administrators, DevOps engineers, Cloud Architects, Platform Engineers, Site Reliability Engineers (SREs), and Network Engineers.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 3: IPv6 → Lesson 7</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** IPv6</div>

<div markdown>**Lesson:** 7 of 7</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Compare IPv4 and IPv6
- Understand major architectural differences
- Compare addressing methods
- Compare routing mechanisms
- Understand security improvements
- Learn migration strategies
- Identify where each protocol is used today

---

# Prerequisites

Complete:

- [Why IPv6](why-ipv6.md)
- [IPv6 Structure](ipv6-structure.md)
- [Types of IPv6 Addresses](ipv6-address-types.md)
- [SLAAC](slaac.md)
- [Neighbor Discovery](neighbor-discovery.md)
- [IPv6 Routing](ipv6-routing.md)

---

# Why Compare IPv4 and IPv6?

Most production environments today support both protocols.

Examples:

- Enterprise Networks
- Cloud Platforms
- Kubernetes Clusters
- Linux Servers
- Data Centres
- Internet Service Providers

Understanding both protocols is essential for modern infrastructure management.

---

# High-Level Comparison

| IPv4 | IPv6 |
|------|------|
| Internet Protocol Version 4 | Internet Protocol Version 6 |
| Introduced in 1981 | Standardised in the late 1990s |
| 32-bit Address | 128-bit Address |
| Limited Address Space | Massive Address Space |

---

# Address Length

IPv4:

```text
32 Bits
```

Example:

```text
192.168.1.10
```

IPv6:

```text
128 Bits
```

Example:

```text
2001:db8:100::10
```

---

# Address Format

IPv4:

```text
Decimal

192.168.1.10
```

IPv6:

```text
Hexadecimal

2001:db8::10
```

---

# Address Space

IPv4:

```text
2³²

=

4.3 Billion Addresses
```

IPv6:

```text
2¹²⁸

=

340 Undecillion Addresses
```

IPv6 provides enough addresses for future Internet growth.

---

# Address Representation

IPv4:

```text
4 Octets

Separated by Dots
```

Example:

```text
10.0.0.1
```

IPv6:

```text
8 Groups

Separated by Colons
```

Example:

```text
2001:db8::1
```

---

# Header Size

IPv4:

```text
Variable Header

20–60 Bytes
```

IPv6:

```text
Fixed Header

40 Bytes
```

The simplified IPv6 header improves forwarding efficiency.

---

# Broadcast

IPv4:

```text
Broadcast

Supported
```

IPv6:

```text
Broadcast

Not Used
```

IPv6 replaces broadcast with:

```text
Multicast

Anycast
```

---

# Address Resolution

IPv4:

```text
ARP
```

IPv6:

```text
Neighbor Discovery Protocol (NDP)
```

NDP is built on ICMPv6 and performs multiple networking functions.

---

# Address Configuration

IPv4:

- Static Configuration
- Dynamic Host Configuration Protocol (DHCP)

IPv6:

- Static Configuration
- Stateless Address Autoconfiguration (SLAAC)
- DHCPv6

IPv6 offers more flexible automatic configuration options.

---

# NAT

IPv4:

```text
Widely Used
```

Because of address shortages, Network Address Translation (NAT) is common.

IPv6:

```text
Generally Not Required
```

The large address space reduces the need for NAT, although it may still be used in specialised environments.

---

# Security

IPv4:

Security is optional and often implemented using additional technologies such as IPsec or Virtual Private Networks (VPNs).

IPv6:

Designed with native support for IPsec standards, although using IPsec is **optional**, not mandatory.

Both protocols can be secured effectively with proper design.

---

# Routing

IPv4:

- Static Routing
- Routing Information Protocol (RIP)
- Open Shortest Path First (OSPF)
- Enhanced Interior Gateway Routing Protocol (EIGRP)
- Border Gateway Protocol (BGP)

IPv6:

- Static Routing
- RIPng
- OSPFv3
- Intermediate System to Intermediate System (IS-IS)
- Multiprotocol BGP (MP-BGP)

The routing principles remain similar.

---

# Fragmentation

IPv4:

Routers and hosts may fragment packets.

IPv6:

Only the sending host performs fragmentation.

Routers do not fragment packets in transit.

---

# Packet Header Comparison

| IPv4 | IPv6 |
|------|------|
| Variable Header | Fixed Header |
| Header Checksum | No Header Checksum |
| Fragmentation by Routers | Fragmentation by Hosts Only |
| Options in Header | Extension Headers |

This simplifies packet processing.

---

# DNS Records

IPv4:

```text
A Record
```

IPv6:

```text
AAAA Record
```

Example:

```text
example.com

↓

AAAA

↓

2001:db8::10
```

---

# Loopback Address

IPv4:

```text
127.0.0.1
```

IPv6:

```text
::1
```

---

# Unspecified Address

IPv4:

```text
0.0.0.0
```

IPv6:

```text
::
```

---

# Private Addressing

IPv4:

```text
10.0.0.0/8

172.16.0.0/12

192.168.0.0/16
```

IPv6:

```text
fd00::/8

(Unique Local Address)
```

---

# Address Configuration Example

IPv4:

```text
DHCP

↓

Assign Address
```

IPv6:

```text
Router Advertisement

↓

SLAAC

↓

Automatic Configuration
```

---

# Cloud Perspective

Modern cloud providers support:

- IPv4
- IPv6
- Dual Stack

Examples:

- Virtual Machines
- Kubernetes
- Load Balancers
- Virtual Networks

Dual-stack deployments remain common during the transition to IPv6.

---

# Kubernetes Perspective

Kubernetes supports:

```text
IPv4 Only
```

```text
IPv6 Only
```

```text
Dual Stack
```

This enables organisations to gradually migrate workloads.

---

# Enterprise Perspective

Typical enterprise deployment:

```text
Internal IPv4

+

Public IPv4

+

IPv6

↓

Dual Stack
```

Organisations migrate gradually while maintaining compatibility.

---

# Linux Perspective

Display IPv4 addresses.

```bash
ip -4 addr
```

Display IPv6 addresses.

```bash
ip -6 addr
```

Display all addresses.

```bash
ip addr
```

Display routing tables.

```bash
ip route

ip -6 route
```

---

# Feature Comparison

| Feature | IPv4 | IPv6 |
|----------|------|------|
| Address Size | 32-bit | 128-bit |
| Address Space | 4.3 Billion | 340 Undecillion |
| Address Format | Decimal | Hexadecimal |
| Header | Variable | Fixed |
| Broadcast | Yes | No |
| Multicast | Yes | Yes |
| Anycast | No | Yes |
| ARP | Yes | No |
| Neighbor Discovery | No | Yes |
| NAT | Common | Rarely Required |
| SLAAC | No | Yes |
| DHCP | DHCP | DHCPv6 (Optional) |
| DNS Record | A | AAAA |

---

# Migration to IPv6

Organisations commonly migrate using:

```text
IPv4

+

IPv6

↓

Dual Stack
```

Transition technologies include:

- Dual Stack
- Tunneling
- Translation (such as NAT64)

This allows gradual adoption without disrupting existing services.

---

# Hands-on Lab

## Task 1

Display IPv4 addresses.

```bash
ip -4 addr
```

---

## Task 2

Display IPv6 addresses.

```bash
ip -6 addr
```

---

## Task 3

Compare:

```bash
ip route
```

and

```bash
ip -6 route
```

---

## Task 4

Create a comparison table showing at least 15 differences between IPv4 and IPv6.

---

## Task 5

Research whether your Internet Service Provider (ISP) supports IPv6.

---

## Task 6

Research IPv6 support for your preferred cloud provider.

---

## Task 7

Draw a Dual Stack network diagram showing devices using both IPv4 and IPv6 simultaneously.

---

## Task 8

Create a migration plan for an organisation transitioning from IPv4-only to Dual Stack networking.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip addr` | Display all IP addresses |
| `ip -4 addr` | Display IPv4 addresses |
| `ip -6 addr` | Display IPv6 addresses |
| `ip route` | Display IPv4 routing table |
| `ip -6 route` | Display IPv6 routing table |
| `ping` | Test IPv4 connectivity |
| `ping -6` | Test IPv6 connectivity |

---

# Common Mistakes

❌ Thinking IPv6 completely replaces IPv4 today.

✅ Most organisations run Dual Stack environments.

---

❌ Assuming IPv6 is difficult.

✅ Learn the address structure and practice regularly.

---

❌ Believing IPv6 requires NAT.

✅ IPv6 generally avoids NAT due to its large address space.

---

❌ Ignoring ICMPv6.

✅ ICMPv6 is essential for IPv6 operation.

---

❌ Assuming IPv4 knowledge is no longer useful.

✅ Both protocols remain important in production environments.

---

# Best Practices

- Learn both IPv4 and IPv6.
- Deploy Dual Stack where appropriate.
- Test IPv6 connectivity regularly.
- Document IPv6 addressing plans.
- Allow required ICMPv6 traffic.
- Design new networks with IPv6 support from the beginning.

---

# Interview Questions

## Beginner

1. What is the difference between IPv4 and IPv6?
2. How many bits are used in IPv6?
3. Why was IPv6 introduced?
4. What is Dual Stack?

---

## Intermediate

1. Compare SLAAC and DHCP.
2. Explain Neighbor Discovery.
3. Why is NAT less common in IPv6?
4. Compare IPv4 and IPv6 routing.

---

## Architect Level

1. Design a migration strategy from IPv4 to IPv6.
2. Explain IPv6 deployment in cloud environments.
3. Compare IPv4 and IPv6 for enterprise networking.

---

# Summary

In this lesson, you learned:

- IPv4 vs IPv6 architecture
- Address size and format
- Header differences
- Routing improvements
- Address configuration
- Neighbor Discovery
- Security considerations
- Enterprise and cloud deployment
- Linux networking commands

IPv4 and IPv6 share the same goal—enabling communication between devices—but IPv6 introduces a much larger address space, simplified packet processing, improved scalability, and modern networking capabilities. Understanding both protocols is essential because modern production environments commonly operate in Dual Stack mode while transitioning toward broader IPv6 adoption.

---

## Key Takeaways

- IPv4 uses **32-bit** addresses; IPv6 uses **128-bit** addresses.
- IPv6 eliminates broadcast and uses multicast and anycast.
- Neighbor Discovery replaces Address Resolution Protocol (ARP).
- SLAAC enables automatic IPv6 address configuration.
- IPv6 generally reduces the need for NAT.
- Most enterprises and cloud providers support Dual Stack networking.

---

# Module 3 Complete!

Congratulations! You have successfully completed **Module 3: IPv6**.

You now understand:

- Why IPv6
- IPv6 Structure
- Types of IPv6 Addresses
- SLAAC
- Neighbor Discovery Protocol (NDP)
- IPv6 Routing
- IPv4 vs IPv6

You now have a solid understanding of modern Internet Protocols and are ready to build, manage, and troubleshoot IPv6-enabled enterprise and cloud networks.

---

## What's Next?

**[Module 3 Summary — IPv6](module-3-ipv6-summary.md)**
