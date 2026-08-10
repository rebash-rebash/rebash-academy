---
title: "IPv4 Address Structure"
description: "Learn how IPv4 addresses are organised — octets, network and host portions, subnet masks, CIDR, gateways, and broadcast addresses."
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
  - addressing
  - subnetting
  - rebash-networking-mastery
comments: false
status: ready
---

# IPv4 Address Structure — Understanding How IPv4 Addresses Are Organised

> Every device connected to an IPv4 network requires an **IPv4 Address** to communicate. An IPv4 address is much more than four decimal numbers separated by dots—it is a carefully structured **32-bit logical address** that identifies both the **network** and the **host**. Understanding the IPv4 address structure is essential before learning subnetting, Classless Inter-Domain Routing (CIDR), routing, Variable Length Subnet Masking (VLSM), and enterprise network design. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should master IPv4 addressing.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 2: IPv4 Addressing → Lesson 2</p>

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

<div markdown>**Lesson:** 2 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the structure of an IPv4 address
- Explain octets and bytes
- Identify network and host portions
- Understand subnet masks
- Explain default gateways
- Read IPv4 addresses in binary and decimal
- Understand how IPv4 addresses enable communication

---

# Prerequisites

Complete:

- [Module 1: Networking Fundamentals](module-1-networking-fundamentals-summary.md)
- [Binary Numbers](binary-numbers.md)

---

# Why Learn IPv4 Address Structure?

Every network device needs an IPv4 address.

Examples:

- Laptop
- Mobile Phone
- Linux Server
- Router
- Firewall
- Kubernetes Node
- Virtual Machine

Without understanding IPv4 structure, it is impossible to learn:

- Subnetting
- CIDR
- Routing
- VLSM
- Supernetting

---

# What is an IPv4 Address?

An **IPv4 Address** is a **32-bit logical address** assigned to a network interface.

Example:

```text
192.168.1.10
```

It uniquely identifies a device within an IPv4 network.

---

# IPv4 Address Format

An IPv4 address consists of **four decimal numbers** separated by periods.

Example:

```text
192.168.1.10
```

Each number is called an **Octet**.

---

# Structure of an IPv4 Address

```text
192 . 168 . 1 . 10

 │      │     │     │

Octet Octet Octet Octet
```

There are:

- 4 Octets
- 32 Bits
- 4 Bytes

---

# Why is it Called an Octet?

Each section contains **8 bits**.

Example:

```text
192

↓

11000000
```

Since:

```text
8 Bits

=

1 Octet
```

The address contains four octets.

---

# IPv4 in Binary

Example:

```text
192.168.1.10
```

Binary representation:

```text
11000000

10101000

00000001

00001010
```

Total:

```text
32 Bits
```

Networking devices process this binary representation internally.

---

# IPv4 Layout

```text
+--------+--------+--------+--------+
| Octet1 | Octet2 | Octet3 | Octet4 |
+--------+--------+--------+--------+

8 Bits    8 Bits   8 Bits   8 Bits
```

Total:

```text
32 Bits
```

---

# Valid IPv4 Range

Each octet can have a decimal value from:

```text
0

to

255
```

Examples of valid addresses:

```text
10.0.0.1

172.16.10.25

192.168.1.100
```

Examples of invalid addresses:

```text
300.1.1.1

192.168.500.10

10.-1.5.8
```

---

# Why 0–255?

Each octet contains 8 bits.

Maximum binary value:

```text
11111111
```

Decimal equivalent:

```text
255
```

Minimum value:

```text
00000000

=

0
```

---

# Total Number of IPv4 Addresses

Since IPv4 uses **32 bits**:

```text
2³²

=

4,294,967,296
```

Approximately **4.3 billion** unique addresses are available (before accounting for reserved ranges).

---

# Network and Host Portions

Every IPv4 address consists of:

- Network Portion
- Host Portion

Example:

```text
192.168.1.25/24
```

Representation:

```text
192.168.1 | 25

 Network   Host
```

The network identifies the subnet.

The host identifies the specific device.

---

# Why Split the Address?

Suppose:

```text
Office A

↓

192.168.1.0
```

Every computer belongs to the same network.

Individual hosts:

```text
192.168.1.10

192.168.1.20

192.168.1.30
```

The network portion remains the same while the host portion changes.

---

# Subnet Mask

The **Subnet Mask** determines which bits belong to:

- Network
- Host

Example:

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

Meaning:

```text
Network

↓

24 Bits

Host

↓

8 Bits
```

---

# CIDR Notation

Instead of writing:

```text
255.255.255.0
```

Modern networks use:

```text
/24
```

Meaning:

```text
24 Network Bits

8 Host Bits
```

CIDR notation simplifies subnet representation.

---

# Example Address

```text
IP Address

192.168.1.50

Subnet

255.255.255.0

Gateway

192.168.1.1
```

This device belongs to the:

```text
192.168.1.0/24
```

network.

---

# Default Gateway

A **Default Gateway** is the router used to reach other networks.

Example:

```text
Laptop

↓

192.168.1.10

↓

Gateway

192.168.1.1

↓

Internet
```

If the destination is outside the local network, packets are sent to the gateway.

---

# Broadcast Address

Every subnet has a broadcast address.

Example:

```text
Network

192.168.1.0/24
```

Broadcast:

```text
192.168.1.255
```

Broadcast packets are delivered to every host in the subnet.

---

# Network Address

The network address identifies the subnet itself.

Example:

```text
192.168.1.0/24
```

This address is reserved and cannot be assigned to a host.

---

# Host Address

Host addresses identify individual devices.

Examples:

```text
192.168.1.10

192.168.1.20

192.168.1.50
```

Each host must have a unique address within the subnet.

---

# IPv4 Communication Example

Suppose:

Laptop:

```text
192.168.1.10
```

Server:

```text
192.168.1.100
```

Both belong to:

```text
192.168.1.0/24
```

Communication:

```text
Laptop

↓

Switch

↓

Server
```

No router is required because both devices are on the same network.

---

# Communication Across Networks

Suppose:

Laptop:

```text
192.168.1.10
```

Website:

```text
142.250.183.110
```

Communication:

```text
Laptop

↓

Switch

↓

Router

↓

Internet

↓

Website
```

The router forwards packets to another network.

---

# Viewing IPv4 Information in Linux

Display IP addresses.

```bash
ip addr
```

---

Display routing table.

```bash
ip route
```

---

Display hostname and IP.

```bash
hostname -I
```

---

Legacy command.

```bash
ifconfig
```

---

# Production Perspective

Every enterprise network uses IPv4 addressing for:

- Servers
- Firewalls
- Routers
- Switch Management
- Cloud Virtual Machines
- Databases
- Kubernetes Nodes
- Storage Systems

Accurate IP planning prevents conflicts and simplifies troubleshooting.

---

# Cloud Perspective

Cloud providers assign IPv4 addresses to:

- Virtual Machines
- Load Balancers
- Network Address Translation (NAT) Gateways
- Kubernetes Nodes
- Managed Databases

Private IP addresses are commonly used inside cloud Virtual Private Clouds (VPCs), while public IP addresses are assigned to Internet-facing resources.

---

# Kubernetes Perspective

Kubernetes uses IPv4 addresses for:

- Nodes
- Pods
- Services
- Ingress Controllers

Cluster networking depends on proper IP allocation and routing.

---

# Hands-on Lab

## Task 1

Display IPv4 addresses.

```bash
ip addr
```

---

## Task 2

Display the routing table.

```bash
ip route
```

---

## Task 3

Display assigned IP addresses.

```bash
hostname -I
```

---

## Task 4

Write the binary representation of:

```text
192.168.10.25
```

---

## Task 5

Identify:

- Network Address
- Host Address
- Broadcast Address

for:

```text
192.168.1.50/24
```

---

## Task 6

Determine whether the following addresses are valid or invalid:

```text
192.168.1.256

10.0.0.15

172.20.5.100

300.1.1.1
```

---

## Task 7

Identify the default gateway on your Linux system.

---

## Task 8

Draw a network containing:

- Router
- Switch
- Three computers

Assign IPv4 addresses and identify:

- Network
- Hosts
- Gateway

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip addr` | Display IP addresses |
| `hostname -I` | Display assigned IPv4 addresses |
| `ip route` | Display routing table |
| `ping` | Test connectivity |
| `ip link` | Display interfaces |

---

# Common Mistakes

❌ Assuming every number is a separate address.

✅ The four octets together form one IPv4 address.

---

❌ Confusing the network address with a host address.

✅ Network addresses identify the subnet, not individual devices.

---

❌ Assigning the broadcast address to a host.

✅ Broadcast addresses are reserved.

---

❌ Ignoring the subnet mask.

✅ Always evaluate an IP address together with its subnet mask.

---

❌ Forgetting the default gateway.

✅ Devices need a gateway to reach other networks.

---

# Best Practices

- Always document IP addressing schemes.
- Use consistent subnet sizes where practical.
- Avoid duplicate IP addresses.
- Reserve static IP addresses for infrastructure devices.
- Verify network and broadcast addresses before assigning hosts.
- Understand both decimal and binary representations.

---

# Interview Questions

## Beginner

1. What is an IPv4 address?
2. How many bits are in an IPv4 address?
3. What is an octet?
4. What is the valid range of an IPv4 octet?

---

## Intermediate

1. Explain the difference between the network and host portions of an IP address.
2. What is the purpose of a subnet mask?
3. What is the default gateway?
4. Why can't the network or broadcast address be assigned to a host?

---

## Architect Level

1. How would you design an IPv4 addressing scheme for a large enterprise?
2. Explain how subnet masks influence routing decisions.
3. Why is understanding IPv4 structure essential for cloud networking and Kubernetes?

---

# Summary

In this lesson, you learned:

- The structure of an IPv4 address
- Octets and bytes
- Binary representation
- Network and host portions
- Subnet masks
- CIDR notation
- Default gateways
- Network and broadcast addresses
- Linux commands for viewing IPv4 configuration

Understanding the IPv4 address structure is the foundation of subnetting, routing, and enterprise network design. Every IPv4 address combines a network identifier and a host identifier, allowing devices to communicate efficiently across local networks and the Internet.

---

## Key Takeaways

- An IPv4 address consists of **32 bits (4 octets)**.
- Each octet contains **8 bits** and ranges from **0 to 255**.
- Every IPv4 address contains a **network portion** and a **host portion**.
- The subnet mask determines where the network ends and the host begins.
- Routers use IPv4 addresses to forward packets between networks.

---

## What's Next?

**[IPv4 Classes](ipv4-classes.md)**
