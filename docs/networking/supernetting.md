---
title: "Supernetting"
description: "Learn Supernetting and route summarisation — combine contiguous networks, reduce routing tables, and apply CIDR aggregation in enterprise and cloud networks."
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
  - supernetting
  - cidr
  - routing
  - ipv4
  - rebash-networking-mastery
comments: false
status: ready
---

# Supernetting — Combining Multiple Networks into Larger Networks

> **Supernetting** is the process of combining multiple smaller IP networks into one larger network. Also known as **Route Aggregation** or **Route Summarisation**, Supernetting reduces routing table size, improves routing efficiency, and simplifies network management. Modern enterprise networks, Internet Service Providers (ISPs), cloud platforms, and large-scale data centres use Supernetting extensively to optimise routing. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand Supernetting.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 2: IPv4 Addressing → Lesson 10</p>

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

<div markdown>**Lesson:** 10 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand what Supernetting is
- Explain route summarisation
- Combine multiple networks into a larger network
- Reduce routing table entries
- Understand CIDR-based aggregation
- Apply Supernetting in enterprise and cloud environments
- Understand the relationship between subnetting and supernetting

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
- [VLSM](vlsm.md)

---

# Why Learn Supernetting?

Imagine a router connected to four networks:

```text
192.168.0.0/24

192.168.1.0/24

192.168.2.0/24

192.168.3.0/24
```

Without Supernetting:

The router stores:

```text
4 Routes
```

Using Supernetting:

These four networks become:

```text
192.168.0.0/22
```

Now the router stores:

```text
1 Route
```

This makes routing faster and simpler.

---

# What is Supernetting?

**Supernetting** is the process of combining multiple contiguous networks into one larger network using a shorter prefix length.

Example:

Before:

```text
192.168.0.0/24

192.168.1.0/24
```

After:

```text
192.168.0.0/23
```

Two networks become one summarised network.

---

# Other Names

Supernetting is also known as:

- Route Aggregation
- Route Summarisation
- Prefix Aggregation

These terms are often used interchangeably.

---

# Why is Supernetting Needed?

Large organisations may have thousands of networks.

Without summarisation:

```text
Thousands of Routes
```

Problems include:

- Large routing tables
- Slower route lookups
- Higher memory usage
- Increased CPU utilisation

Supernetting reduces these problems.

---

# Relationship Between Subnetting and Supernetting

| Subnetting | Supernetting |
|------------|--------------|
| Divides one large network into smaller networks | Combines multiple smaller networks into one larger network |
| Uses longer prefixes | Uses shorter prefixes |
| Creates more routing entries | Reduces routing entries |

---

# Example 1

Networks:

```text
192.168.0.0/24

192.168.1.0/24
```

Summary:

```text
192.168.0.0/23
```

---

# Example 2

Networks:

```text
192.168.0.0/24

192.168.1.0/24

192.168.2.0/24

192.168.3.0/24
```

Summary:

```text
192.168.0.0/22
```

---

# Binary View

Consider:

```text
192.168.0.0/24

↓

11000000.10101000.00000000.00000000
```

```text
192.168.1.0/24

↓

11000000.10101000.00000001.00000000
```

The first **23 bits** are identical.

Therefore:

```text
192.168.0.0/23
```

is the summarised route.

---

# Supernet Rules

Networks must be:

- Contiguous
- Equal in size
- Properly aligned
- Consecutive

Otherwise, summarisation is not possible.

---

# Route Summarisation Example

Instead of:

```text
10.1.0.0/24

10.1.1.0/24

10.1.2.0/24

10.1.3.0/24
```

Advertise:

```text
10.1.0.0/22
```

One route replaces four.

---

# Benefits of Supernetting

- Smaller routing tables
- Faster routing decisions
- Lower CPU utilisation
- Reduced memory consumption
- Improved scalability
- Simpler network management

---

# Enterprise Example

Regional office networks:

```text
10.10.1.0/24

10.10.2.0/24

10.10.3.0/24

10.10.4.0/24
```

Core router advertises:

```text
10.10.0.0/21
```

instead of multiple individual routes (assuming the summarised block correctly covers the allocated networks).

---

# ISP Example

Internet Service Providers commonly allocate:

```text
203.0.113.0/24

203.0.114.0/24

203.0.115.0/24

203.0.116.0/24
```

Instead of advertising each network individually, they summarise where address allocation allows.

This significantly reduces Internet routing table size.

---

# Cloud Perspective

Cloud providers summarise routes within:

- Virtual Private Clouds (VPCs)
- Virtual Networks (VNets)
- Transit Gateways
- Cloud Routers

Example:

```text
10.0.0.0/24

10.0.1.0/24

10.0.2.0/24

10.0.3.0/24
```

may be summarised as:

```text
10.0.0.0/22
```

when appropriate.

---

# Kubernetes Perspective

Large Kubernetes environments often summarise routes between clusters or data centres to reduce routing complexity.

Example:

```text
Cluster A

10.244.0.0/16
```

```text
Cluster B

10.245.0.0/16
```

Higher-level routing infrastructure may summarise larger address blocks when network design permits.

---

# Route Aggregation Process

```text
Multiple Networks

↓

Find Common Prefix

↓

Reduce Prefix Length

↓

Create Summary Route

↓

Advertise Single Route
```

---

# Supernetting Example

Original routes:

```text
172.16.0.0/24

172.16.1.0/24

172.16.2.0/24

172.16.3.0/24
```

Summary:

```text
172.16.0.0/22
```

Instead of:

```text
4 Routes
```

Router stores:

```text
1 Route
```

---

# Linux Perspective

Linux routing table:

```bash
ip route
```

Example:

```text
10.0.0.0/16

via 192.168.1.1
```

Administrators can configure summarised static routes where appropriate to simplify routing.

---

# Hands-on Lab

## Task 1

Summarise the following networks:

```text
192.168.0.0/24

192.168.1.0/24
```

---

## Task 2

Summarise:

```text
192.168.4.0/24

192.168.5.0/24

192.168.6.0/24

192.168.7.0/24
```

---

## Task 3

Display your routing table.

```bash
ip route
```

Identify summarised routes if present.

---

## Task 4

Draw a diagram showing four branch offices connected to a headquarters router.

Show both:

- Individual routes
- Summarised route

---

## Task 5

Research route summarisation support in your preferred cloud provider.

---

## Task 6

Create an enterprise network using:

- Headquarters
- Branch Offices
- Data Center

Use summarised routes between locations.

---

## Task 7

Determine whether the following networks can be summarised:

```text
10.1.0.0/24

10.1.1.0/24

10.1.2.0/24

10.1.3.0/24
```

If yes, identify the summarised CIDR block.

---

## Task 8

Compare subnetting and supernetting by creating two diagrams:

- One showing a large network divided into smaller subnets
- One showing multiple smaller networks combined into a summarised route

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip route` | Display routing table |
| `ip addr` | Display interface configuration |
| `ping` | Test connectivity |
| `traceroute` | Verify routing path |

---

# Common Mistakes

❌ Summarising non-contiguous networks.

✅ Only summarise contiguous address ranges.

---

❌ Ignoring alignment requirements.

✅ Verify that network boundaries align correctly.

---

❌ Advertising an overly broad summary.

✅ Ensure the summary does not include networks you do not own or manage.

---

❌ Confusing subnetting with supernetting.

✅ Subnetting divides; supernetting combines.

---

❌ Assuming every network can be summarised.

✅ Verify binary prefixes before aggregating.

---

# Best Practices

- Use route summarisation wherever practical.
- Summarise only contiguous networks.
- Validate summaries before deployment.
- Keep routing tables as small as possible.
- Document summarised routes.
- Test routing after implementing aggregation.

---

# Interview Questions

## Beginner

1. What is Supernetting?
2. What is route summarisation?
3. Why is Supernetting useful?
4. How does Supernetting differ from subnetting?

---

## Intermediate

1. Summarise four `/24` networks into a single route.
2. Explain why contiguous networks are required.
3. How does Supernetting improve router performance?
4. What is the relationship between CIDR and Supernetting?

---

## Architect Level

1. Design a route summarisation strategy for a multi-site enterprise.
2. Explain how ISPs use Supernetting.
3. How would you reduce routing table size in a large cloud environment?

---

# Summary

In this lesson, you learned:

- What Supernetting is
- Route summarisation
- CIDR-based aggregation
- Combining multiple networks
- Enterprise and ISP routing
- Cloud networking applications
- Linux routing concepts

Supernetting is a critical technique for building scalable networks. By combining multiple contiguous networks into a single summarised route, organisations reduce routing complexity, improve router performance, conserve resources, and simplify network management.

---

## Key Takeaways

- Supernetting combines multiple smaller networks into one larger network.
- Route summarisation reduces routing table size.
- Only contiguous, properly aligned networks can be summarised.
- Supernetting improves routing performance and scalability.
- Modern enterprise, ISP, and cloud networks rely heavily on route aggregation.

---

# Module 2 Complete

Congratulations — you have successfully completed **Module 2: IPv4 Addressing**.

You now understand:

- Binary Numbers
- IPv4 Address Structure
- IPv4 Classes
- Private vs Public IP Addresses
- Loopback Addresses
- Automatic Private IP Addressing (APIPA)
- Classless Inter-Domain Routing (CIDR)
- Subnetting
- Variable Length Subnet Masking (VLSM)
- Supernetting

These concepts provide the foundation for designing IPv4 networks, performing subnet calculations, planning enterprise address spaces, and troubleshooting real-world networking issues.

---

## What's Next?

**[Module 2 Summary — IPv4 Addressing](module-2-ipv4-addressing-summary.md)**
