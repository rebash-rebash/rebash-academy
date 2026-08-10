---
title: "CIDR"
description: "Learn Classless Inter-Domain Routing (CIDR) — prefix notation, host calculations, subnet masks, route summarisation, and cloud/Kubernetes CIDR design."
difficulty: intermediate
estimated_time: "90 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 2 · IPv4 Addressing"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - kubernetes-engineer
  - platform-engineer
tags:
  - networking
  - cidr
  - ipv4
  - subnetting
  - rebash-networking-mastery
comments: false
status: ready
---

# CIDR (Classless Inter-Domain Routing) — Modern IP Addressing and Network Design

> **CIDR (Classless Inter-Domain Routing)** is the modern method of allocating IP addresses and defining network boundaries. Unlike the old class-based addressing system (Class A, B, and C), CIDR allows network administrators to create networks of almost any size by specifying the number of network bits using **prefix notation** (such as **/24**, **/16**, or **/28**). Today, CIDR is used everywhere—from enterprise data centres and cloud platforms to Kubernetes clusters and home networks. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should master CIDR.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 2: IPv4 Addressing → Lesson 7</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** IPv4 Addressing</div>

<div markdown>**Lesson:** 7 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand what CIDR is
- Read CIDR notation
- Understand prefix lengths
- Calculate network and host bits
- Determine the number of hosts in a subnet
- Understand why CIDR replaced classful addressing
- Apply CIDR in cloud and enterprise networking

---

# Prerequisites

Complete:

- [Binary Numbers](binary-numbers.md)
- [IPv4 Address Structure](ipv4-address-structure.md)
- [IPv4 Classes](ipv4-classes.md)
- [Private vs Public IP](private-vs-public-ip.md)
- [Loopback](loopback.md)
- [APIPA](apipa.md)

---

# Why Learn CIDR?

Suppose your organisation needs:

```text
500 Hosts
```

Using classful addressing:

Class C:

```text
254 Hosts

❌ Too Small
```

Class B:

```text
65,534 Hosts

❌ Too Large
```

Most addresses would be wasted.

CIDR solves this problem by allowing network sizes that closely match actual requirements.

---

# What is CIDR?

**CIDR (Classless Inter-Domain Routing)** is a method of allocating IP addresses without relying on predefined address classes.

Instead of using:

```text
Class A

Class B

Class C
```

CIDR uses:

```text
/8

/16

/24

/26

/28

/30
```

This provides flexible network sizing.

---

# CIDR Notation

Example:

```text
192.168.1.0/24
```

The number after the slash indicates:

```text
24 Network Bits
```

Remaining bits:

```text
8 Host Bits
```

---

# CIDR Format

```text
IP Address

/

Prefix Length
```

Example:

```text
10.0.0.0/16
```

Meaning:

```text
16 Network Bits

16 Host Bits
```

---

# Prefix Length

The prefix length tells us how many bits belong to the network.

Example:

```text
/24
```

Binary:

```text
11111111

11111111

11111111

00000000
```

Equivalent subnet mask:

```text
255.255.255.0
```

---

# CIDR and Subnet Mask

| CIDR | Subnet Mask |
|------|-------------|
| /8 | 255.0.0.0 |
| /16 | 255.255.0.0 |
| /24 | 255.255.255.0 |
| /25 | 255.255.255.128 |
| /26 | 255.255.255.192 |
| /27 | 255.255.255.224 |
| /28 | 255.255.255.240 |
| /29 | 255.255.255.248 |
| /30 | 255.255.255.252 |
| /31 | 255.255.255.254 |
| /32 | 255.255.255.255 |

---

# Network Bits vs Host Bits

Example:

```text
192.168.1.0/24
```

Binary:

```text
11111111

11111111

11111111

00000000
```

Network:

```text
24 Bits
```

Host:

```text
8 Bits
```

---

# Host Calculation

Formula:

```text
2^(Host Bits)

−

2
```

The subtraction accounts for the network and broadcast addresses.

---

# Example: /24

Host bits:

```text
8
```

Calculation:

```text
2⁸

−

2

=

254 Hosts
```

---

# Example: /26

Host bits:

```text
6
```

Calculation:

```text
2⁶

−

2

=

62 Hosts
```

---

# Example: /30

Host bits:

```text
2
```

Calculation:

```text
2²

−

2

=

2 Hosts
```

A `/30` network is commonly used for point-to-point links.

---

# Common CIDR Blocks

| CIDR | Hosts |
|------|-------|
| /30 | 2 |
| /29 | 6 |
| /28 | 14 |
| /27 | 30 |
| /26 | 62 |
| /25 | 126 |
| /24 | 254 |
| /23 | 510 |
| /22 | 1022 |
| /21 | 2046 |
| /20 | 4094 |
| /16 | 65,534 |

---

# CIDR Example

Network:

```text
192.168.10.0/26
```

Network Address:

```text
192.168.10.0
```

Usable Hosts:

```text
192.168.10.1

↓

192.168.10.62
```

Broadcast:

```text
192.168.10.63
```

---

# Another Example

CIDR:

```text
10.0.0.0/20
```

Network bits:

```text
20
```

Host bits:

```text
12
```

Hosts:

```text
2¹²

−

2

=

4094
```

---

# Why CIDR Replaced Classful Addressing

Classful addressing:

```text
Class C

↓

254 Hosts
```

Suppose a company needs:

```text
300 Hosts
```

Class C:

```text
Too Small
```

Class B:

```text
65,534 Hosts

Too Large
```

CIDR allows:

```text
/23

↓

510 Hosts
```

Much more efficient.

---

# Route Summarisation

CIDR also supports **Route Summarisation**, where multiple networks are represented by a single route.

Example:

Instead of:

```text
192.168.0.0/24

192.168.1.0/24

192.168.2.0/24

192.168.3.0/24
```

Summarise as:

```text
192.168.0.0/22
```

Benefits:

- Smaller routing tables
- Faster routing decisions
- Reduced memory usage

---

# CIDR in Cloud Computing

Cloud providers require CIDR blocks when creating virtual networks.

Examples:

AWS VPC:

```text
10.0.0.0/16
```

Azure VNet:

```text
10.1.0.0/16
```

Google Cloud VPC:

```text
172.16.0.0/20
```

Administrators choose the prefix length based on expected network size.

---

# CIDR in Kubernetes

Kubernetes uses CIDR extensively.

Examples:

Pod Network:

```text
10.244.0.0/16
```

Service Network:

```text
10.96.0.0/12
```

Each node receives a smaller CIDR block for Pod allocation.

---

# CIDR in Enterprise Networks

Enterprise environments use CIDR for:

- Virtual Local Area Networks (VLANs)
- Branch Offices
- Virtual Private Network (VPN) Networks
- Server Networks
- Storage Networks
- Demilitarised Zones (DMZs)

Example:

```text
Servers

10.10.10.0/24

Users

10.10.20.0/23

DMZ

10.10.30.0/27
```

---

# CIDR Calculation Shortcut

| Prefix | Host Bits |
|---------|-----------|
| /24 | 8 |
| /25 | 7 |
| /26 | 6 |
| /27 | 5 |
| /28 | 4 |
| /29 | 3 |
| /30 | 2 |

Remember:

```text
Host Bits

=

32

−

Prefix
```

---

# Hands-on Lab

## Task 1

Determine the subnet mask for:

```text
/24

/26

/28

/30
```

---

## Task 2

Calculate the number of usable hosts for:

```text
/25

/26

/27

/28

/29
```

---

## Task 3

Convert the following subnet masks into CIDR notation:

```text
255.255.255.0

255.255.255.192

255.255.255.240

255.255.0.0
```

---

## Task 4

Determine the network and broadcast addresses for:

```text
192.168.1.0/26
```

---

## Task 5

Research the CIDR block used in your cloud lab or home network.

---

## Task 6

Create a VPC design for:

- Web Tier
- Application Tier
- Database Tier

Assign appropriate CIDR blocks to each subnet.

---

## Task 7

Use the `ip addr` command and identify the prefix length assigned to your network interface.

```bash
ip addr
```

---

## Task 8

For each of the following CIDR blocks, calculate:

- Subnet mask
- Total addresses
- Usable host addresses

```text
10.0.0.0/24

172.16.0.0/20

192.168.100.0/28
```

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip addr` | Display IP address and prefix |
| `ip route` | Display routing table |
| `hostname -I` | Display assigned IP addresses |
| `ping` | Test connectivity |

---

# Common Mistakes

❌ Confusing CIDR with subnet masks.

✅ Learn both representations and convert between them.

---

❌ Forgetting the network and broadcast addresses.

✅ Subtract two usable addresses for most IPv4 subnets.

---

❌ Memorising host counts without understanding the formula.

✅ Practice using `2^(host bits) - 2`.

---

❌ Assuming larger prefixes mean larger networks.

✅ Larger prefix numbers mean smaller networks.

---

❌ Ignoring future growth.

✅ Allocate CIDR blocks with room for expansion.

---

# Best Practices

- Plan address space before deployment.
- Leave room for future growth.
- Use route summarisation where appropriate.
- Document all CIDR allocations.
- Avoid overlapping CIDR blocks.
- Choose subnet sizes based on actual requirements.

---

# Interview Questions

## Beginner

1. What is CIDR?
2. What does `/24` mean?
3. What is the subnet mask for `/26`?
4. Why was CIDR introduced?

---

## Intermediate

1. Calculate the number of hosts in a `/27` network.
2. Explain the relationship between prefix length and subnet mask.
3. Why does CIDR improve address utilisation?
4. What is route summarisation?

---

## Architect Level

1. Design a CIDR plan for a multi-tier cloud application.
2. Explain how CIDR reduces routing table size.
3. How would you allocate CIDR blocks for a Kubernetes cluster and a cloud VPC?

---

# Summary

In this lesson, you learned:

- What CIDR is
- CIDR notation
- Prefix lengths
- Network and host bits
- Host calculations
- CIDR-to-subnet mask conversion
- Route summarisation
- Cloud and Kubernetes networking with CIDR

CIDR is the foundation of modern IP networking. It provides flexible address allocation, minimises address wastage, enables efficient routing, and supports scalable enterprise and cloud network designs. Mastering CIDR is essential before learning subnetting and advanced IPv4 planning.

---

## Key Takeaways

- CIDR replaces the old classful addressing system.
- The prefix length defines the network portion of an IP address.
- Host bits are calculated as **32 − Prefix Length**.
- Usable hosts are calculated using **2^(Host Bits) − 2** (for traditional IPv4 subnets).
- CIDR enables efficient address allocation and route summarisation.

---

## What's Next?

**[Subnetting](subnetting-and-vlsm.md)**
