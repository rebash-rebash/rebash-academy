---
title: "VLSM"
description: "Learn Variable Length Subnet Masking (VLSM) — allocate different-sized subnets, reduce IPv4 waste, and design enterprise and cloud addressing plans."
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
  - vlsm
  - subnetting
  - ipv4
  - cidr
  - rebash-networking-mastery
comments: false
status: ready
---

# VLSM (Variable Length Subnet Masking) — Efficient IP Address Allocation

> **Variable Length Subnet Masking (VLSM)** is an advanced subnetting technique that allows you to create **subnets of different sizes** within the same network. Unlike traditional fixed-length subnetting, where every subnet is identical in size, VLSM allocates IP addresses based on actual requirements, reducing address wastage and improving scalability. Modern enterprise networks, cloud platforms, Internet Service Providers (ISPs), and Kubernetes environments rely heavily on VLSM. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should master VLSM.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 2: IPv4 Addressing → Lesson 9</p>

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

<div markdown>**Lesson:** 9 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand what VLSM is
- Explain why VLSM is needed
- Compare VLSM with fixed-length subnetting
- Design networks using different subnet sizes
- Allocate IP addresses efficiently
- Plan enterprise and cloud network addressing
- Solve real-world VLSM problems

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
- [Subnetting](subnetting-and-vlsm.md)

---

# Why Learn VLSM?

Suppose a company has one network:

```text
192.168.10.0/24
```

Departments:

```text
Engineering

120 Hosts
```

```text
Finance

30 Hosts
```

```text
HR

10 Hosts
```

```text
Management

5 Hosts
```

If we use fixed-size subnetting:

```text
All departments receive /25

126 Hosts each
```

This wastes a large number of IP addresses.

Instead, VLSM allows each department to receive only the addresses it actually needs.

---

# What is VLSM?

**Variable Length Subnet Masking (VLSM)** is the practice of assigning **different subnet masks** within the same network based on host requirements.

Example:

```text
Engineering

/25
```

```text
Finance

/27
```

```text
HR

/28
```

```text
Management

/29
```

Each subnet has an appropriate size.

---

# Why VLSM Was Introduced

Traditional subnetting creates subnets of equal size.

Example:

```text
192.168.1.0/24

↓

4 × /26
```

Each subnet:

```text
62 Hosts
```

If a department only requires:

```text
10 Hosts
```

then:

```text
52 Addresses

↓

Unused
```

VLSM minimises this waste.

---

# Fixed-Length vs Variable-Length Subnetting

| Fixed-Length Subnetting | VLSM |
|--------------------------|------|
| All subnets are the same size | Subnets have different sizes |
| Simpler | More efficient |
| Wastes addresses | Optimises address usage |
| Limited flexibility | Highly flexible |

---

# VLSM Planning Rule

Always allocate subnets in **descending order of host requirements**.

Example:

```text
120 Hosts

↓

30 Hosts

↓

10 Hosts

↓

5 Hosts
```

Allocate the largest subnet first.

---

# Step-by-Step Example

Available Network:

```text
192.168.10.0/24
```

Requirements:

| Department | Hosts |
|------------|------:|
| Engineering | 120 |
| Finance | 30 |
| HR | 10 |
| Management | 5 |

---

# Step 1 — Engineering

Needs:

```text
120 Hosts
```

Required subnet:

```text
/25
```

Provides:

```text
126 Hosts
```

Assignment:

```text
192.168.10.0/25
```

Range:

```text
192.168.10.1

↓

192.168.10.126
```

Broadcast:

```text
192.168.10.127
```

---

# Step 2 — Finance

Remaining network:

```text
192.168.10.128/25
```

Needs:

```text
30 Hosts
```

Required subnet:

```text
/27
```

Assignment:

```text
192.168.10.128/27
```

Range:

```text
192.168.10.129

↓

192.168.10.158
```

Broadcast:

```text
192.168.10.159
```

---

# Step 3 — HR

Needs:

```text
10 Hosts
```

Required subnet:

```text
/28
```

Assignment:

```text
192.168.10.160/28
```

Range:

```text
192.168.10.161

↓

192.168.10.174
```

Broadcast:

```text
192.168.10.175
```

---

# Step 4 — Management

Needs:

```text
5 Hosts
```

Required subnet:

```text
/29
```

Assignment:

```text
192.168.10.176/29
```

Range:

```text
192.168.10.177

↓

192.168.10.182
```

Broadcast:

```text
192.168.10.183
```

---

# Final VLSM Plan

| Department | Network | CIDR | Usable Hosts |
|------------|---------|------|-------------:|
| Engineering | 192.168.10.0 | /25 | 126 |
| Finance | 192.168.10.128 | /27 | 30 |
| HR | 192.168.10.160 | /28 | 14 |
| Management | 192.168.10.176 | /29 | 6 |

Notice that each department receives only the address space it needs.

---

# How to Choose the Correct Prefix

| Required Hosts | Recommended CIDR | Usable Hosts |
|---------------:|------------------|-------------:|
| 2 | /30 | 2 |
| 6 | /29 | 6 |
| 14 | /28 | 14 |
| 30 | /27 | 30 |
| 62 | /26 | 62 |
| 126 | /25 | 126 |
| 254 | /24 | 254 |

Always choose the **smallest subnet** that can accommodate the required number of hosts.

---

# Benefits of VLSM

- Efficient IP utilisation
- Reduced address wastage
- Flexible network design
- Supports organisational growth
- Simplifies enterprise network planning
- Ideal for cloud and ISP environments

---

# Enterprise Example

Company Network:

```text
10.20.0.0/16
```

Allocation:

```text
Engineering

10.20.0.0/22
```

```text
Finance

10.20.4.0/24
```

```text
HR

10.20.5.0/26
```

```text
Management

10.20.5.64/28
```

Each department receives a subnet based on its actual needs.

---

# Cloud Perspective

Suppose a cloud Virtual Private Cloud (VPC) uses:

```text
10.0.0.0/16
```

Subnets:

```text
Public

10.0.1.0/24
```

```text
Application

10.0.2.0/23
```

```text
Database

10.0.4.0/26
```

Using VLSM avoids allocating unnecessarily large subnets.

---

# Kubernetes Perspective

Cluster CIDR:

```text
10.244.0.0/16
```

Node allocations:

```text
Node 1

10.244.1.0/24
```

```text
Node 2

10.244.2.0/25
```

```text
Node 3

10.244.2.128/26
```

Although Kubernetes implementations often allocate fixed Pod CIDRs, VLSM principles are widely used in designing surrounding infrastructure networks.

---

# VLSM Design Process

```text
List Host Requirements

↓

Sort Largest to Smallest

↓

Choose Correct CIDR

↓

Allocate Largest Subnet

↓

Allocate Remaining Subnets

↓

Verify No Overlap
```

---

# Linux Perspective

Display interface information:

```bash
ip addr
```

Display routes:

```bash
ip route
```

Although Linux does not calculate VLSM automatically, administrators use these commands to verify configured subnet prefixes.

---

# Hands-on Lab

## Task 1

Given:

```text
192.168.100.0/24
```

Allocate subnets for:

- Sales – 100 Hosts
- HR – 20 Hosts
- IT – 10 Hosts
- Management – 5 Hosts

---

## Task 2

Determine the correct CIDR block for:

- 8 Hosts
- 50 Hosts
- 200 Hosts
- 500 Hosts

---

## Task 3

Create a VLSM table containing:

- Department
- Required Hosts
- Assigned CIDR
- Network Address
- Broadcast Address

---

## Task 4

Design an office network using VLSM for:

- Guest Wi-Fi
- Employee LAN
- Servers
- Printers
- Security Cameras

---

## Task 5

Create a VPC subnet plan for:

- Public Subnet
- Application Subnet
- Database Subnet
- Management Subnet

Use VLSM to minimise unused addresses.

---

## Task 6

Display your current subnet prefix.

```bash
ip addr
```

Identify the CIDR notation assigned to your primary interface.

---

## Task 7

Verify that your proposed VLSM plan contains no overlapping address ranges.

---

## Task 8

Draw a network diagram showing four departments connected to a router, each using a different subnet size.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip addr` | Display IP address and subnet prefix |
| `ip route` | Display routing table |
| `hostname -I` | Display assigned IP address |
| `ping` | Test connectivity |

---

# Common Mistakes

❌ Allocating small subnets before large ones.

✅ Always allocate the largest subnet first.

---

❌ Choosing a subnet smaller than required.

✅ Select a subnet that supports future growth.

---

❌ Creating overlapping address ranges.

✅ Verify every network boundary carefully.

---

❌ Wasting addresses with fixed-size subnetting.

✅ Use VLSM whenever subnet sizes differ.

---

❌ Ignoring documentation.

✅ Record every subnet allocation and purpose.

---

# Best Practices

- Allocate subnets based on current and expected growth.
- Assign the largest networks first.
- Reserve unused address space for future expansion.
- Document all VLSM allocations.
- Validate calculations before deployment.
- Keep management and infrastructure networks separate.

---

# Interview Questions

## Beginner

1. What is VLSM?
2. Why is VLSM better than fixed-length subnetting?
3. Why should the largest subnet be allocated first?
4. What is the benefit of variable subnet sizes?

---

## Intermediate

1. Design a VLSM plan for departments with different host requirements.
2. Explain how VLSM reduces IP address wastage.
3. How do you determine the correct prefix length for a subnet?
4. What problems occur if subnets overlap?

---

## Architect Level

1. Design a VLSM addressing scheme for a multi-site enterprise.
2. How would you allocate VLSM subnets in a cloud VPC?
3. Explain how VLSM supports scalable network growth.

---

# Summary

In this lesson, you learned:

- What VLSM is
- Why VLSM is required
- Fixed-length vs variable-length subnetting
- VLSM planning methodology
- Efficient IP address allocation
- Enterprise, cloud, and Kubernetes applications
- Real-world VLSM design

VLSM is an essential networking technique that maximises IPv4 address utilisation by allocating subnet sizes based on actual needs. It is widely used in enterprise networks, cloud platforms, and service provider environments to create scalable, efficient, and well-organised IP addressing schemes.

---

## Key Takeaways

- VLSM allows different subnet sizes within the same network.
- Always allocate the largest subnet first.
- VLSM minimises IP address wastage.
- Proper planning prevents overlapping networks.
- VLSM is a fundamental skill for enterprise and cloud network design.

---

## What's Next?

**[Supernetting](supernetting.md)**
