---
title: "Subnetting"
description: "Learn IPv4 subnetting — dividing networks, calculating network/broadcast/host addresses, subnet increments, and enterprise, cloud, and Kubernetes design."
difficulty: intermediate
estimated_time: "120 min"
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
  - subnetting
  - ipv4
  - cidr
  - rebash-networking-mastery
comments: false
status: ready
---

# Subnetting — Dividing Networks into Smaller, Efficient Networks

> **Subnetting** is the process of dividing a large IP network into multiple smaller, manageable networks called **subnets**. It improves network performance, enhances security, simplifies management, and optimises IP address utilisation. Subnetting is one of the most important skills in networking and is frequently tested in networking certifications and technical interviews. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should master subnetting.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 2: IPv4 Addressing → Lesson 8</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 120 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** IPv4 Addressing</div>

<div markdown>**Lesson:** 8 of 10</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand what subnetting is
- Explain why subnetting is required
- Divide networks into smaller subnets
- Calculate network, broadcast, and host addresses
- Determine the number of hosts and subnets
- Perform manual subnetting calculations
- Design enterprise subnetting schemes

---

# Prerequisites

Complete:

- [Binary Numbers](binary-numbers.md)
- [IPv4 Address Structure](ipv4-address-structure.md)
- [IPv4 Classes](ipv4-classes.md)
- [Private vs Public IP](private-vs-public-ip.md)
- [Loopback](loopback.md)
- [APIPA](apipa.md)
- [CIDR](cidr.md)

---

# Why Learn Subnetting?

Suppose an organisation has:

```text
192.168.1.0/24
```

This network supports:

```text
254 Hosts
```

But the company has three departments:

- HR
- Finance
- Engineering

Should all 254 hosts be in the same network?

```text
No
```

Instead, we divide the network into smaller subnetworks.

This process is called **Subnetting**.

---

# What is Subnetting?

Subnetting is the process of dividing a larger network into multiple smaller networks.

Example:

Before:

```text
192.168.1.0/24
```

After:

```text
192.168.1.0/26

192.168.1.64/26

192.168.1.128/26

192.168.1.192/26
```

One large network becomes four smaller networks.

---

# Why Do We Need Subnetting?

Subnetting provides several benefits:

- Better IP address utilisation
- Reduced broadcast traffic
- Improved security
- Easier network management
- Better performance
- Simplified troubleshooting
- Logical separation of departments

---

# Real-World Example

An office contains:

- HR
- Finance
- Engineering
- Management

Instead of placing everyone in one network:

```text
192.168.1.0/24
```

Create separate subnets:

```text
HR

192.168.1.0/26
```

```text
Finance

192.168.1.64/26
```

```text
Engineering

192.168.1.128/26
```

```text
Management

192.168.1.192/26
```

Each department has its own subnet.

---

# Important Terms

Before learning subnetting, understand these terms:

- Network Address
- Broadcast Address
- Host Address
- Subnet Mask
- Prefix Length

---

# Network Address

The first address in every subnet.

Example:

```text
192.168.1.0/26
```

Network Address:

```text
192.168.1.0
```

It identifies the subnet and cannot be assigned to a host.

---

# Broadcast Address

The last address in every subnet.

Example:

```text
192.168.1.0/26
```

Broadcast:

```text
192.168.1.63
```

Packets sent to this address reach all hosts within the subnet.

---

# Host Addresses

The addresses between the network and broadcast addresses.

Example:

```text
Network

192.168.1.0
```

Usable Hosts:

```text
192.168.1.1

↓

192.168.1.62
```

Broadcast:

```text
192.168.1.63
```

---

# How Subnetting Works

Subnetting borrows bits from the **host portion** of an IP address.

Original:

```text
192.168.1.0/24
```

Network Bits:

```text
24
```

Host Bits:

```text
8
```

Borrow 2 bits:

```text
/26
```

Now:

```text
Network Bits

26
```

Host Bits

```text
6
```

---

# Number of Subnets

Formula:

```text
2^(Borrowed Bits)
```

Borrow:

```text
2 Bits
```

Calculation:

```text
2²

=

4 Subnets
```

---

# Number of Hosts

Formula:

```text
2^(Host Bits)

−

2
```

Host Bits:

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

# Subnetting Example

Original Network:

```text
192.168.1.0/24
```

Borrow:

```text
2 Bits
```

Result:

```text
192.168.1.0/26

192.168.1.64/26

192.168.1.128/26

192.168.1.192/26
```

---

# Subnet 1

```text
Network

192.168.1.0
```

Hosts:

```text
192.168.1.1

↓

192.168.1.62
```

Broadcast:

```text
192.168.1.63
```

---

# Subnet 2

```text
Network

192.168.1.64
```

Hosts:

```text
192.168.1.65

↓

192.168.1.126
```

Broadcast:

```text
192.168.1.127
```

---

# Subnet 3

```text
Network

192.168.1.128
```

Hosts:

```text
192.168.1.129

↓

192.168.1.190
```

Broadcast:

```text
192.168.1.191
```

---

# Subnet 4

```text
Network

192.168.1.192
```

Hosts:

```text
192.168.1.193

↓

192.168.1.254
```

Broadcast:

```text
192.168.1.255
```

---

# Subnet Increment

The increment is calculated as:

```text
256

−

Subnet Mask Value
```

Example:

```text
255.255.255.192
```

Calculation:

```text
256

−

192

=

64
```

Subnet increments:

```text
0

64

128

192
```

---

# Common CIDR Values

| CIDR | Mask | Hosts |
|------|------|-------|
| /24 | 255.255.255.0 | 254 |
| /25 | 255.255.255.128 | 126 |
| /26 | 255.255.255.192 | 62 |
| /27 | 255.255.255.224 | 30 |
| /28 | 255.255.255.240 | 14 |
| /29 | 255.255.255.248 | 6 |
| /30 | 255.255.255.252 | 2 |

---

# Manual Subnetting Steps

Given:

```text
192.168.10.0/27
```

Step 1:

Determine subnet mask:

```text
255.255.255.224
```

Step 2:

Calculate increment:

```text
256

−

224

=

32
```

Step 3:

Network addresses:

```text
0

32

64

96

128

160

192

224
```

Each network supports:

```text
30 Hosts
```

---

# Enterprise Example

Company:

```text
10.10.0.0/16
```

Subnets:

```text
HR

10.10.1.0/24
```

```text
Finance

10.10.2.0/24
```

```text
Engineering

10.10.3.0/23
```

```text
Servers

10.10.10.0/25
```

Each department receives an appropriately sized subnet.

---

# Cloud Perspective

Cloud providers require subnetting when designing networks.

Example:

VPC:

```text
10.0.0.0/16
```

Subnets:

```text
Public

10.0.1.0/24
```

```text
Private

10.0.2.0/24
```

```text
Database

10.0.3.0/24
```

---

# Kubernetes Perspective

Kubernetes clusters divide large Classless Inter-Domain Routing (CIDR) blocks into smaller node-level subnets.

Example:

Cluster:

```text
10.244.0.0/16
```

Node 1:

```text
10.244.1.0/24
```

Node 2:

```text
10.244.2.0/24
```

Each node manages its own Pod IP range.

---

# Linux Perspective

Display IP addresses and subnet prefixes.

```bash
ip addr
```

Example:

```text
192.168.1.10/24
```

Display routing information.

```bash
ip route
```

---

# Hands-on Lab

## Task 1

Determine the subnet mask for:

```text
/25

/26

/27

/28
```

---

## Task 2

Subnet:

```text
192.168.1.0/24
```

into:

```text
4 Networks
```

Write:

- Network Address
- First Host
- Last Host
- Broadcast Address

---

## Task 3

Calculate the usable hosts for:

```text
/25

/26

/27

/28

/29
```

---

## Task 4

Calculate the increment for:

```text
255.255.255.128

255.255.255.192

255.255.255.224

255.255.255.240
```

---

## Task 5

Design subnetworks for:

- HR (40 Hosts)
- Finance (25 Hosts)
- Engineering (100 Hosts)
- Servers (10 Hosts)

---

## Task 6

Use:

```bash
ip addr
```

Identify the CIDR notation of your Linux interface.

---

## Task 7

Draw a network diagram showing four departments connected through a router, each using its own subnet.

---

## Task 8

Given:

```text
192.168.100.0/24
```

Divide it into **8 equal subnets** and list:

- Network Address
- First Host
- Last Host
- Broadcast Address

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip addr` | Display IP address and prefix |
| `ip route` | Display routing table |
| `hostname -I` | Display assigned IP address |
| `ping` | Test connectivity |

---

# Common Mistakes

❌ Assigning the network address to a host.

✅ Reserve the first address for the network.

---

❌ Assigning the broadcast address to a host.

✅ Reserve the last address for broadcasts.

---

❌ Forgetting the subnet increment.

✅ Always calculate the block size first.

---

❌ Using oversized subnets.

✅ Choose subnet sizes based on actual host requirements.

---

❌ Overlapping subnet ranges.

✅ Ensure every subnet has a unique address range.

---

# Best Practices

- Allocate subnets based on current and future requirements.
- Reserve space for network growth.
- Document all subnet allocations.
- Avoid overlapping networks.
- Separate departments using dedicated subnets.
- Use private address ranges for internal networks.

---

# Interview Questions

## Beginner

1. What is subnetting?
2. Why is subnetting required?
3. What is a network address?
4. What is a broadcast address?

---

## Intermediate

1. How do you calculate the number of hosts in a subnet?
2. Explain how subnet increments are determined.
3. Divide a `/24` network into four equal subnets.
4. Why does subnetting reduce broadcast traffic?

---

## Architect Level

1. Design a subnetting plan for a company with multiple departments.
2. Explain subnetting strategies for cloud VPCs.
3. How would you subnet a Kubernetes cluster network?

---

# Summary

In this lesson, you learned:

- What subnetting is
- Why subnetting is important
- Network, broadcast, and host addresses
- Borrowing host bits
- Subnet calculations
- Subnet increments
- Enterprise, cloud, and Kubernetes subnet design

Subnetting is one of the most valuable networking skills. It enables efficient IP address allocation, improves performance by reducing broadcast domains, enhances security through network segmentation, and forms the basis of enterprise, cloud, and Kubernetes network design.

---

## Key Takeaways

- Subnetting divides a large network into smaller subnetworks.
- Borrowing host bits creates additional subnets.
- Every subnet has a network address and a broadcast address.
- Usable hosts are calculated using **2^(Host Bits) − 2**.
- Proper subnetting improves scalability, security, and network efficiency.

---

## What's Next?

**[VLSM](vlsm.md)**
