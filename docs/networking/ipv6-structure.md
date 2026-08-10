---
title: "IPv6 Structure"
description: "Learn IPv6 address structure — 128-bit format, hexadecimal notation, compression rules, prefix lengths, and network versus interface identifiers."
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
  - kubernetes-engineer
  - platform-engineer
tags:
  - networking
  - ipv6
  - addressing
  - hexadecimal
  - rebash-networking-mastery
comments: false
status: ready
---

# IPv6 Structure — Understanding the Format of IPv6 Addresses

> Unlike IPv4, which uses **32-bit addresses**, **IPv6 uses 128-bit addresses**, providing an enormous address space for the future Internet. IPv6 addresses are written in **hexadecimal notation**, making them appear very different from IPv4 addresses. Understanding the structure of an IPv6 address is the first step toward learning IPv6 networking, routing, cloud networking, Kubernetes, and enterprise infrastructure. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand IPv6 address structure.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 3: IPv6 → Lesson 2</p>

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

<div markdown>**Lesson:** 2 of 7</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand IPv6 address structure
- Read IPv6 addresses
- Understand hexadecimal notation
- Learn IPv6 address compression
- Understand prefix lengths
- Identify network and interface portions
- Display IPv6 addresses on Linux

---

# Prerequisites

Complete:

- Module 2: IPv4 Addressing
- [Why IPv6](why-ipv6.md)

---

# Why Learn IPv6 Structure?

Suppose you see this address:

```text
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

At first glance it looks confusing.

However, once you understand its structure, reading IPv6 addresses becomes straightforward.

---

# IPv6 Address Size

IPv4:

```text
32 Bits
```

IPv6:

```text
128 Bits
```

This fourfold increase in address length enables a vastly larger address space.

---

# IPv6 Address Format

An IPv6 address contains:

```text
8 Groups
```

Each group contains:

```text
4 Hexadecimal Digits
```

Example:

```text
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

---

# IPv6 Layout

```text
2001 : 0db8 : 85a3 : 0000 : 0000 : 8a2e : 0370 : 7334

  |      |      |      |      |      |      |      |

Group1 Group2 Group3 Group4 Group5 Group6 Group7 Group8
```

There are:

- 8 Groups
- 16 Bits per Group
- 128 Bits Total

---

# Hexadecimal Numbers

IPv6 uses **Hexadecimal (Base-16)** instead of decimal.

Hexadecimal digits are:

```text
0 1 2 3 4 5 6 7 8 9 A B C D E F
```

Each hexadecimal digit represents:

```text
4 Bits
```

---

# Hexadecimal Example

Binary:

```text
1111
```

Hexadecimal:

```text
F
```

Another example:

```text
1010

↓

A
```

Using hexadecimal makes long binary addresses much easier to read.

---

# IPv6 Group Size

Each group contains:

```text
16 Bits
```

Example:

```text
2001
```

Binary:

```text
0010000000000001
```

---

# Total Structure

```text
8 Groups

×

16 Bits

=

128 Bits
```

---

# Network Prefix and Interface Identifier

An IPv6 address is commonly divided into:

```text
Network Prefix

↓

64 Bits
```

```text
Interface Identifier

↓

64 Bits
```

Example:

```text
2001:db8:abcd:1000

↓

Network Prefix
```

```text
0000:0000:1234:5678

↓

Interface Identifier
```

---

# Prefix Length

Just like IPv4 uses Classless Inter-Domain Routing (CIDR):

```text
192.168.1.0/24
```

IPv6 also uses prefix notation.

Example:

```text
2001:db8::/64
```

Meaning:

```text
64 Network Bits

64 Host Bits
```

---

# Leading Zero Suppression

Leading zeros within a group may be omitted.

Example:

Before:

```text
2001:0db8:0000:0000:0000:ff00:0042:8329
```

After:

```text
2001:db8:0:0:0:ff00:42:8329
```

Only **leading** zeros may be removed.

---

# Zero Compression

If one or more consecutive groups contain only zeros, they can be replaced with:

```text
::
```

Example:

Before:

```text
2001:db8:0:0:0:0:0:1
```

After:

```text
2001:db8::1
```

---

# Compression Rule

The double colon (`::`) can be used:

```text
Only Once
```

within a single IPv6 address.

Incorrect:

```text
2001::abcd::1234
```

Correct:

```text
2001:0:0:abcd:0:0:0:1234

↓

2001:0:0:abcd::1234
```

---

# Full vs Compressed Address

Full:

```text
2001:0db8:0000:0000:0000:0000:0000:0001
```

Compressed:

```text
2001:db8::1
```

Both represent exactly the same IPv6 address.

---

# Another Example

Full:

```text
fe80:0000:0000:0000:021a:2bff:fe3c:4d5e
```

Compressed:

```text
fe80::21a:2bff:fe3c:4d5e
```

---

# IPv6 Prefix Examples

| Prefix | Meaning |
|---------|---------|
| /32 | Large Network Allocation |
| /48 | Enterprise Site |
| /56 | Small Organisation |
| /64 | Standard LAN Subnet |
| /128 | Single Interface Address |

The **/64** prefix is the most common subnet size in IPv6.

---

# Why is /64 Common?

IPv6 was designed so that:

```text
64 Bits

↓

Network
```

```text
64 Bits

↓

Interface Identifier
```

Many IPv6 features, including Stateless Address Autoconfiguration (SLAAC), assume a `/64` subnet.

---

# Example Address Breakdown

Address:

```text
2001:db8:abcd:10::15/64
```

Network Prefix:

```text
2001:db8:abcd:10
```

Host Portion:

```text
::15
```

---

# IPv4 vs IPv6 Structure

| IPv4 | IPv6 |
|------|------|
| 32 Bits | 128 Bits |
| Decimal | Hexadecimal |
| 4 Octets | 8 Groups |
| Dots (`.`) | Colons (`:`) |
| Maximum 255 per Octet | Four Hex Digits per Group |

---

# Enterprise Example

Company Network:

```text
2001:db8:1000::/48
```

Departments:

```text
HR

2001:db8:1000:1::/64
```

```text
Finance

2001:db8:1000:2::/64
```

```text
Engineering

2001:db8:1000:3::/64
```

Each department receives its own `/64` subnet.

---

# Cloud Perspective

Cloud providers assign IPv6 prefixes to:

- Virtual Private Clouds (VPCs)
- Virtual Networks (VNets)
- Virtual Machines
- Kubernetes Clusters
- Load Balancers

Example:

```text
2001:db8:5000::/56
```

Subnets:

```text
2001:db8:5000:1::/64

2001:db8:5000:2::/64

2001:db8:5000:3::/64
```

---

# Kubernetes Perspective

Modern Kubernetes clusters support IPv6.

Example:

```text
Pod

↓

2001:db8:100::10
```

Service:

```text
2001:db8:200::20
```

IPv6 networking works similarly to IPv4 but with a much larger address space.

---

# Linux Perspective

Display IPv6 addresses.

```bash
ip -6 addr
```

Display IPv6 routes.

```bash
ip -6 route
```

Ping localhost over IPv6.

```bash
ping -6 ::1
```

---

# Hands-on Lab

## Task 1

Display IPv6 addresses.

```bash
ip -6 addr
```

---

## Task 2

Display IPv6 routing information.

```bash
ip -6 route
```

---

## Task 3

Compress the following IPv6 address:

```text
2001:0db8:0000:0000:0000:0000:0000:0001
```

---

## Task 4

Expand the following IPv6 address:

```text
2001:db8::1
```

---

## Task 5

Identify:

- Network Prefix
- Interface Identifier

for:

```text
2001:db8:1000:20::15/64
```

---

## Task 6

Explain why the following address is invalid:

```text
2001::abcd::1234
```

---

## Task 7

Create a comparison table showing the differences between IPv4 and IPv6 address structures.

---

## Task 8

Research the IPv6 prefix assigned by your Internet Service Provider (ISP) or cloud provider (if available) and identify its prefix length.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip -6 addr` | Display IPv6 addresses |
| `ip -6 route` | Display IPv6 routes |
| `ping -6` | Test IPv6 connectivity |
| `hostname` | Display hostname |

---

# Common Mistakes

❌ Treating IPv6 like IPv4.

✅ Learn hexadecimal notation and IPv6 grouping.

---

❌ Using `::` more than once.

✅ A double colon can appear only once in an IPv6 address.

---

❌ Removing trailing zeros.

✅ Only leading zeros within a group may be omitted.

---

❌ Forgetting prefix lengths.

✅ Always evaluate IPv6 addresses together with their prefix length.

---

❌ Assuming `/64` is optional.

✅ `/64` is the standard subnet size for most IPv6 LANs.

---

# Best Practices

- Practice reading IPv6 addresses daily.
- Learn hexadecimal numbers thoroughly.
- Use compressed notation where appropriate.
- Understand both expanded and compressed formats.
- Standardise on `/64` for IPv6 LAN subnets unless a specific design requires otherwise.
- Document IPv6 addressing plans clearly.

---

# Interview Questions

## Beginner

1. How many bits are in an IPv6 address?
2. Why does IPv6 use hexadecimal?
3. How many groups are in an IPv6 address?
4. What does `/64` represent?

---

## Intermediate

1. Explain IPv6 address compression.
2. Why can `::` only appear once?
3. Compare IPv4 and IPv6 address structures.
4. What is the difference between the network prefix and the interface identifier?

---

## Architect Level

1. Design an IPv6 addressing scheme for an enterprise.
2. Explain why `/64` is the standard subnet size.
3. How would you allocate IPv6 prefixes for cloud and Kubernetes environments?

---

# Summary

In this lesson, you learned:

- IPv6 address structure
- 128-bit addressing
- Hexadecimal notation
- Eight-group format
- Prefix lengths
- Leading zero suppression
- Zero compression
- Network prefix and interface identifier
- Linux IPv6 commands

IPv6 addresses are significantly larger than IPv4 addresses but follow a logical and consistent structure. Understanding hexadecimal notation, prefix lengths, and compression rules makes IPv6 addresses much easier to read and manage. These concepts form the foundation for IPv6 routing, address types, and automatic address configuration.

---

## Key Takeaways

- IPv6 addresses are **128 bits** long.
- An IPv6 address contains **8 groups** of **4 hexadecimal digits**.
- Leading zeros may be omitted within a group.
- Consecutive zero groups may be compressed using `::` **once per address**.
- `/64` is the standard subnet size for most IPv6 networks.
- IPv6 uses hexadecimal notation to represent large binary values efficiently.

---

## What's Next?

**[Types of IPv6 Addresses](ipv6-address-types.md)**

In the next lesson, you'll learn about **Types of IPv6 Addresses**.

You'll explore:

- Unicast Addresses
- Multicast Addresses
- Anycast Addresses
- Global Unicast
- Link-Local Addresses
- Unique Local Addresses (ULA)
- Special IPv6 addresses

By the end of the lesson, you'll understand the different IPv6 address types, when each is used, and how they enable communication in enterprise, cloud, and Kubernetes environments.
