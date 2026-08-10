---
title: "IPv4 Classes"
description: "Learn IPv4 classful addressing — Classes A–E, default masks, host capacity, binary patterns, and why CIDR replaced classful networking."
difficulty: beginner
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
  - ipv4
  - classes
  - cidr
  - rebash-networking-mastery
comments: false
status: ready
---

# IPv4 Classes — Understanding Classful IP Addressing

> In the early days of the Internet, IPv4 addresses were divided into predefined **classes** known as **Class A, B, C, D, and E**. Each class was designed to support networks of different sizes, from small organisations to global enterprises. Although modern networks primarily use **CIDR (Classless Inter-Domain Routing)**, understanding IPv4 classes remains important because they are frequently discussed in networking courses, certification exams, and technical interviews. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand IPv4 classes and their historical significance.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 2: IPv4 Addressing → Lesson 3</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** IPv4 Addressing</div>

<div markdown>**Lesson:** 3 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand IPv4 classful addressing
- Identify Class A, B, C, D, and E addresses
- Explain default subnet masks
- Calculate network and host capacities
- Understand why CIDR replaced classful networking
- Recognise IPv4 classes in real-world scenarios

---

# Prerequisites

Complete:

- [Binary Numbers](binary-numbers.md)
- [IPv4 Address Structure](ipv4-address-structure.md)

---

# Why Learn IPv4 Classes?

Before CIDR was introduced, routers determined the network size based on the **first octet** of an IP address.

Example:

```text
10.20.30.40
```

Immediately tells us:

```text
Class A
```

Similarly,

```text
172.16.5.10

↓

Class B
```

```text
192.168.1.50

↓

Class C
```

Although modern networking uses CIDR, understanding these classes makes subnetting and IP planning much easier.

---

# What is Classful Addressing?

**Classful Addressing** divides the IPv4 address space into five predefined classes.

```text
Class A

Class B

Class C

Class D

Class E
```

Each class has:

- A specific address range
- A default subnet mask
- A different number of networks
- A different number of hosts

---

# IPv4 Class Overview

| Class | First Octet | Default Mask | Purpose |
|--------|-------------|--------------|---------|
| A | 1–126 | 255.0.0.0 (/8) | Very Large Networks |
| B | 128–191 | 255.255.0.0 (/16) | Medium Networks |
| C | 192–223 | 255.255.255.0 (/24) | Small Networks |
| D | 224–239 | N/A | Multicast |
| E | 240–255 | N/A | Experimental |

---

# Class A

Range:

```text
1.0.0.0

↓

126.255.255.255
```

Default subnet mask:

```text
255.0.0.0

(/8)
```

Network bits:

```text
8
```

Host bits:

```text
24
```

---

## Binary Pattern

Class A addresses always begin with:

```text
0
```

Example:

```text
10.10.20.30
```

Binary (first octet):

```text
00001010
```

Leading bit:

```text
0
```

---

## Capacity

| Item | Value |
|------|-------|
| Networks | 126 |
| Hosts per Network | 16,777,214 |

Formula:

```text
2²⁴ − 2

=

16,777,214
```

(Two addresses are reserved: network and broadcast.)

---

## Common Example

```text
10.0.0.0/8
```

Widely used in:

- Large enterprises
- Cloud networks
- Data centres

---

# Class B

Range:

```text
128.0.0.0

↓

191.255.255.255
```

Default subnet mask:

```text
255.255.0.0

(/16)
```

Network bits:

```text
16
```

Host bits:

```text
16
```

---

## Binary Pattern

Class B addresses begin with:

```text
10
```

Example:

```text
172.16.10.5
```

Binary (first octet):

```text
10101100
```

Leading bits:

```text
10
```

---

## Capacity

| Item | Value |
|------|-------|
| Networks | 16,384 |
| Hosts per Network | 65,534 |

Formula:

```text
2¹⁶ − 2

=

65,534
```

---

## Common Example

```text
172.16.0.0/16
```

Often used by medium-sized organisations.

---

# Class C

Range:

```text
192.0.0.0

↓

223.255.255.255
```

Default subnet mask:

```text
255.255.255.0

(/24)
```

Network bits:

```text
24
```

Host bits:

```text
8
```

---

## Binary Pattern

Class C addresses begin with:

```text
110
```

Example:

```text
192.168.1.10
```

Binary (first octet):

```text
11000000
```

Leading bits:

```text
110
```

---

## Capacity

| Item | Value |
|------|-------|
| Networks | 2,097,152 |
| Hosts per Network | 254 |

Formula:

```text
2⁸ − 2

=

254
```

---

## Common Example

```text
192.168.1.0/24
```

Used in:

- Homes
- Small businesses
- Labs

---

# Class D

Range:

```text
224.0.0.0

↓

239.255.255.255
```

Purpose:

```text
Multicast
```

Used for:

- Video streaming
- IPTV
- Routing protocols
- Group communication

Class D addresses are **not assigned to individual hosts**.

---

# Class E

Range:

```text
240.0.0.0

↓

255.255.255.255
```

Purpose:

```text
Experimental

Research
```

These addresses are generally not used in normal production networks.

---

# Reserved Addresses

Some IPv4 addresses are reserved.

| Address | Purpose |
|----------|---------|
| 0.0.0.0 | Default/Unspecified |
| 127.0.0.0/8 | Loopback |
| 255.255.255.255 | Limited Broadcast |

These ranges have special meanings and cannot be assigned as normal host addresses.

---

# Class Comparison

| Class | Network Bits | Host Bits | Default Mask |
|--------|--------------|-----------|--------------|
| A | 8 | 24 | /8 |
| B | 16 | 16 | /16 |
| C | 24 | 8 | /24 |

---

# Why Did Classful Addressing Fail?

Suppose a company needed:

```text
500 Hosts
```

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

This caused significant IP address wastage.

---

# Introduction of CIDR

To solve address wastage, **CIDR (Classless Inter-Domain Routing)** was introduced.

Instead of:

```text
Class A

Class B

Class C
```

CIDR allows:

```text
/22

/26

/19

/30

/27
```

Networks can now be sized according to actual requirements.

---

# Real-World Examples

| IP Address | Class |
|-------------|-------|
| 10.5.10.20 | A |
| 172.20.15.8 | B |
| 192.168.1.100 | C |
| 230.10.20.5 | D |
| 245.1.2.3 | E |

---

# Production Perspective

Modern enterprise networks rarely use classful routing.

Instead, they rely on:

- CIDR
- Variable Length Subnet Masking (VLSM)
- Route Summarisation

However, understanding IPv4 classes helps interpret default masks and recognise private address ranges.

---

# Cloud Perspective

Cloud providers use CIDR instead of classes.

Example Virtual Private Clouds (VPCs):

```text
10.0.0.0/16

172.20.0.0/20

192.168.100.0/24
```

Although these ranges originate from Class A, B, and C private spaces, cloud networking treats them as flexible CIDR blocks.

---

# Kubernetes Perspective

Kubernetes clusters also use CIDR.

Examples:

```text
10.244.0.0/16

10.96.0.0/12
```

Classful boundaries are ignored in favour of CIDR notation.

---

# Hands-on Lab

## Task 1

Identify the class of the following IP addresses:

```text
10.5.20.30

172.16.10.5

192.168.100.10

224.0.0.5

245.10.20.30
```

---

## Task 2

Write the default subnet mask for:

- Class A
- Class B
- Class C

---

## Task 3

Determine the network and host bits for each class.

---

## Task 4

Display your IPv4 address.

```bash
ip addr
```

Identify which historical class it belongs to.

---

## Task 5

Convert the first octet of these addresses to binary and identify the class using the leading bits.

---

## Task 6

Calculate the maximum number of hosts for:

- Class A
- Class B
- Class C

---

## Task 7

Research why CIDR replaced classful addressing and summarise the advantages.

---

## Task 8

Create a comparison table showing Classes A–E, including:

- Address Range
- Default Mask
- Purpose
- Host Capacity

---

# Binary Patterns

| Class | Leading Bits |
|--------|--------------|
| A | 0 |
| B | 10 |
| C | 110 |
| D | 1110 |
| E | 1111 |

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip addr` | Display IP addresses |
| `hostname -I` | Display assigned IPs |
| `ip route` | Display routing table |
| `ping` | Test connectivity |

---

# Common Mistakes

❌ Thinking classes are used for modern routing.

✅ Modern routing uses CIDR.

---

❌ Confusing private ranges with classes.

✅ A class defines address structure; private ranges are reserved blocks.

---

❌ Memorising ranges without understanding default masks.

✅ Learn how masks relate to network and host bits.

---

❌ Assuming Class D hosts can be assigned to devices.

✅ Class D is reserved for multicast.

---

❌ Ignoring historical significance.

✅ Many certifications and interviews still reference IPv4 classes.

---

# Best Practices

- Understand IPv4 classes before learning CIDR.
- Memorise the first-octet ranges for Classes A, B, and C.
- Learn the default subnet masks.
- Understand why CIDR replaced classful networking.
- Focus on concepts rather than memorisation alone.

---

# Interview Questions

## Beginner

1. What are IPv4 address classes?
2. What is the default subnet mask for Class C?
3. Which class is used for multicast?
4. Which class contains the address 172.16.10.5?

---

## Intermediate

1. Compare Class A, B, and C addressing.
2. Why was Classful Addressing inefficient?
3. Explain the purpose of Classes D and E.
4. How many hosts can a Class C network support?

---

## Architect Level

1. Why did the Internet transition from classful addressing to CIDR?
2. How does CIDR improve address utilisation?
3. Why is understanding IPv4 classes still valuable in enterprise networking?

---

# Summary

In this lesson, you learned:

- IPv4 Classes A–E
- Address ranges
- Default subnet masks
- Network and host capacities
- Binary class identification
- Limitations of classful addressing
- Why CIDR replaced classful networking

Although modern networking uses CIDR, IPv4 classes remain an important foundational concept. Understanding how addresses were historically divided helps explain subnet masks, private address ranges, and the evolution of IP addressing.

---

## Key Takeaways

- IPv4 originally used five address classes.
- Class A, B, and C were used for host addressing.
- Class D is reserved for multicast.
- Class E is reserved for experimental purposes.
- CIDR replaced classful addressing to improve IP address utilisation.

---

## What's Next?

**[Private vs Public IP](private-vs-public-ip.md)**
