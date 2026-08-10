---
title: "Binary Numbers"
description: "Learn binary numbers for networking — bits, bytes, place values, decimal conversion, and how binary underpins IPv4 addressing and subnetting."
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
  - binary
  - ipv4
  - subnetting
  - rebash-networking-mastery
comments: false
status: ready
---

# Binary Numbers — The Foundation of Computer Networking

> Every computer, smartphone, router, switch, cloud server, and network device understands only **binary numbers**—a language made up of **0s and 1s**. Although humans use the decimal number system (Base 10), computers use the binary number system (Base 2) because electronic circuits have only two stable states: **ON** and **OFF**. Understanding binary numbers is essential for mastering IPv4 addressing, subnetting, Classless Inter-Domain Routing (CIDR), routing, and network design. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer must understand binary arithmetic.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 2: IPv4 Addressing → Lesson 1</p>

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

<div markdown>**Lesson:** 1 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the binary number system
- Explain bits and bytes
- Convert decimal numbers to binary
- Convert binary numbers to decimal
- Understand binary place values
- Apply binary to IPv4 addressing
- Prepare for subnetting calculations

---

# Prerequisites

Complete:

- [Module 1: Networking Fundamentals](module-1-networking-fundamentals-summary.md)

---

# Why Learn Binary Numbers?

Every IPv4 address is stored in binary.

Example:

```text
192.168.1.10
```

The computer actually stores it as:

```text
11000000.10101000.00000001.00001010
```

Networking devices never process decimal addresses directly—they process binary values.

Without binary, subnetting and routing become impossible to understand.

---

# What is Binary?

Binary is a number system that uses only **two digits**:

```text
0

1
```

It is called a **Base-2 Number System**.

---

# Why Do Computers Use Binary?

Electronic circuits have only two stable states.

```text
OFF

↓

0
```

```text
ON

↓

1
```

Because of this, every piece of digital information is ultimately represented using binary digits.

---

# Number Systems

| Number System | Base | Digits |
|---------------|------|---------|
| Decimal | 10 | 0–9 |
| Binary | 2 | 0–1 |
| Octal | 8 | 0–7 |
| Hexadecimal | 16 | 0–9, A–F |

Networking primarily uses:

- Decimal (human-readable)
- Binary (computer-readable)

---

# What is a Bit?

A **Bit** (Binary Digit) is the smallest unit of digital information.

Possible values:

```text
0

or

1
```

Examples:

```text
0

1
```

---

# What is a Byte?

A **Byte** consists of **8 Bits**.

Example:

```text
10101010
```

One byte can represent:

```text
0 – 255
```

This is why each IPv4 octet ranges from **0 to 255**.

---

# Binary Place Values

Each bit position has a value.

```text
128 64 32 16 8 4 2 1
```

Example:

```text
1  0  1  0  1 0 1 0
```

Calculation:

```text
128

+

32

+

8

+

2

=

170
```

Therefore:

```text
10101010

=

170
```

---

# Binary Value Table

| Binary | Decimal |
|---------|---------|
| 00000000 | 0 |
| 00000001 | 1 |
| 00000010 | 2 |
| 00000011 | 3 |
| 00000100 | 4 |
| 00000101 | 5 |
| 00000110 | 6 |
| 00000111 | 7 |

---

# Decimal to Binary Conversion

Example:

Convert:

```text
13
```

Step 1:

Write place values.

```text
128 64 32 16 8 4 2 1
```

Step 2:

Determine which values add up to 13.

```text
8

+

4

+

1

=

13
```

Step 3:

Write the binary digits.

```text
00001101
```

Therefore:

```text
13

↓

00001101
```

---

# Another Example

Convert:

```text
25
```

Calculation:

```text
16

+

8

+

1

=

25
```

Binary:

```text
00011001
```

---

# Binary to Decimal Conversion

Example:

```text
11001010
```

Place values:

```text
128 64 32 16 8 4 2 1
```

Calculation:

```text
128

+

64

+

8

+

2

=

202
```

Therefore:

```text
11001010

=

202
```

---

# Practice Conversions

Convert the following to binary:

```text
5
```

Answer:

```text
00000101
```

---

Convert:

```text
15
```

Answer:

```text
00001111
```

---

Convert:

```text
100
```

Answer:

```text
01100100
```

---

Convert:

```text
255
```

Answer:

```text
11111111
```

---

# Binary in IPv4

IPv4 addresses consist of **four bytes**.

Example:

```text
192.168.1.10
```

Binary:

```text
11000000

10101000

00000001

00001010
```

Each section is called an **octet**.

---

# Why Binary Matters in Networking

Binary is used for:

- IPv4 addresses
- Subnet masks
- CIDR notation
- Routing
- Access Control Lists (ACLs)
- Firewall rules
- Network calculations

Every subnetting calculation depends on binary.

---

# Binary and Subnetting

Suppose:

```text
255.255.255.0
```

Binary:

```text
11111111

11111111

11111111

00000000
```

These binary values determine:

- Network portion
- Host portion

Subnetting is simply binary mathematics.

---

# Real-World Example

IP Address:

```text
192.168.10.50
```

Subnet Mask:

```text
255.255.255.0
```

Routers compare these values in binary to determine:

- Local network
- Remote network
- Routing decisions

---

# Binary Memory Trick

Remember the place values:

```text
128

64

32

16

8

4

2

1
```

Always calculate from **left to right**.

---

# Production Perspective

Binary calculations occur continuously in:

- Routers
- Firewalls
- Cloud Platforms
- Kubernetes
- Linux Networking
- Load Balancers
- Virtual Private Networks (VPNs)
- Switches

Although administrators usually see decimal addresses, networking devices always process binary values internally.

---

# Cloud Perspective

Cloud providers use binary calculations when:

- Allocating Virtual Private Cloud (VPC) subnets
- Creating route tables
- Configuring firewall rules
- Assigning IP ranges

Understanding binary simplifies cloud networking.

---

# Kubernetes Perspective

Kubernetes networking relies heavily on binary when allocating:

- Pod CIDRs
- Service CIDRs
- Node CIDRs

Every cluster network uses binary-based subnet calculations.

---

# Hands-on Lab

## Task 1

Convert the following decimal numbers to binary:

```text
8

15

32

64

128

255
```

---

## Task 2

Convert the following binary numbers to decimal:

```text
00001111

11111111

10000000

01100100
```

---

## Task 3

Write the binary representation of your computer's IPv4 address.

Display your IP:

```bash
ip addr
```

Convert each octet into binary.

---

## Task 4

Memorise the binary place values:

```text
128

64

32

16

8

4

2

1
```

---

## Task 5

Write the binary equivalent of:

```text
192.168.1.100
```

---

## Task 6

Identify which bits are set in:

```text
11010110
```

Calculate its decimal value.

---

## Task 7

Use an online calculator to verify your manual binary conversions.

---

## Task 8

Create a conversion table for every decimal number from **0 to 32** showing its binary representation.

---

# Binary Reference Table

| Decimal | Binary |
|----------|---------|
| 0 | 00000000 |
| 1 | 00000001 |
| 2 | 00000010 |
| 4 | 00000100 |
| 8 | 00001000 |
| 16 | 00010000 |
| 32 | 00100000 |
| 64 | 01000000 |
| 128 | 10000000 |
| 255 | 11111111 |

---

# Common Mistakes

❌ Forgetting place values.

✅ Memorise 128, 64, 32, 16, 8, 4, 2, 1.

---

❌ Reading binary from right to left.

✅ Always evaluate from left to right using place values.

---

❌ Confusing bits and bytes.

✅ 1 Byte = 8 Bits.

---

❌ Ignoring leading zeros.

✅ IPv4 octets always contain 8 bits.

---

❌ Memorising conversions without understanding.

✅ Practice manual calculations regularly.

---

# Best Practices

- Learn binary before studying subnetting.
- Practice decimal-to-binary conversions daily.
- Always write all eight bits for IPv4 octets.
- Verify manual calculations until you're confident.
- Understand the logic instead of relying only on calculators.

---

# Interview Questions

## Beginner

1. What is binary?
2. Why do computers use binary?
3. How many bits are in one byte?
4. Why does an IPv4 octet range from 0 to 255?

---

## Intermediate

1. Convert 45 to binary.
2. Convert `11001010` to decimal.
3. Explain binary place values.
4. Why is binary important in subnetting?

---

## Architect Level

1. How do routers use binary when making forwarding decisions?
2. Explain how binary affects CIDR and VPC subnet design.
3. Why is binary knowledge essential for cloud networking and Kubernetes?

---

# Summary

In this lesson, you learned:

- The binary number system
- Bits and bytes
- Binary place values
- Decimal-to-binary conversion
- Binary-to-decimal conversion
- Binary representation of IPv4 addresses
- Binary's role in subnetting and routing

Binary is the language of networking. Every IP address, subnet mask, routing table, and firewall rule is ultimately processed as binary. Mastering binary arithmetic makes advanced networking topics such as subnetting, CIDR, Variable Length Subnet Masking (VLSM), and route summarisation much easier to understand.

---

## Key Takeaways

- Binary uses only **0** and **1**.
- One byte contains **8 bits**.
- IPv4 addresses consist of **32 bits (4 bytes)**.
- Binary place values are **128, 64, 32, 16, 8, 4, 2, 1**.
- Binary forms the foundation of IPv4 addressing and subnetting.

---

## What's Next?

**[IPv4 Address Structure](ipv4-address-structure.md)**
