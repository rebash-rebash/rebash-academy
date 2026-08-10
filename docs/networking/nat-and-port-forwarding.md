---
title: "Network Address Translation (NAT)"
description: "Learn Network Address Translation (NAT) — private vs public IP, translation tables, Inside Local/Global addressing, and Linux iptables/nftables NAT views."
difficulty: beginner
estimated_time: "100 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 7 · NAT and Firewalls"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - nat
  - ipv4
  - iptables
  - rebash-networking-mastery
comments: false
status: ready
---

# Network Address Translation (NAT) — Connecting Private Networks to the Internet

> **Network Address Translation (NAT)** is a networking technology that allows devices using **private IP addresses** to communicate with networks that use **public IP addresses**, such as the Internet. NAT modifies the source or destination IP address of packets as they pass through a router or firewall. Because IPv4 public addresses are limited, NAT has become one of the most widely used technologies in enterprise networks, home routers, cloud environments, and data centres. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand NAT.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 7: NAT & Firewalls → Lesson 1</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 100 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** NAT & Firewalls</div>

<div markdown>**Lesson:** 1 of 10</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Network Address Translation (NAT)
- Learn why NAT is needed
- Understand Private and Public IP addresses
- Learn how NAT works
- Understand Inside and Outside Networks
- Apply NAT in enterprise and cloud environments
- Troubleshoot NAT issues

---

# Prerequisites

Complete:

- Module 1: Networking Fundamentals
- Module 2: IPv4 Addressing
- Module 3: IPv6
- Module 4: Switching
- Module 5: Routing
- Module 6: DNS & DHCP

---

# Why Learn NAT?

Imagine a company has:

- 5,000 Employees
- 5,000 Computers

Should every computer receive a public IP address?

```text
No
```

Instead:

```text
Private Network

↓

NAT

↓

Internet
```

One or more public IP addresses allow thousands of private devices to access the Internet.

---

# What is NAT?

**Network Address Translation (NAT)** modifies IP addresses in packets as they pass through a router or firewall.

Example:

```text
Private IP

↓

Public IP
```

NAT allows:

- Internet Access
- Address Conservation
- Network Isolation

---

# Why is NAT Needed?

IPv4 provides approximately:

```text
4.3 Billion

Addresses
```

The Internet contains:

- Billions of Devices
- Servers
- Smartphones
- Internet of Things (IoT) Devices
- Virtual Machines

Without NAT:

```text
Public IP

Required

For Every Device

❌ Impossible
```

---

# Private IP Addresses

Private IPv4 address ranges:

```text
10.0.0.0/8
```

```text
172.16.0.0/12
```

```text
192.168.0.0/16
```

Private addresses:

- Are not routable on the public Internet
- Can be reused by any organisation

---

# Public IP Addresses

Public IP addresses:

- Are globally unique
- Are assigned by Internet Registries or Internet Service Providers (ISPs)
- Can communicate across the Internet

Example:

```text
203.0.113.10
```

---

# NAT Example

Laptop:

```text
192.168.1.100
```

Accesses:

```text
google.com
```

Router performs:

```text
192.168.1.100

↓

198.51.100.25
```

The website only sees the public IP address.

---

# NAT Workflow

```text
Client

↓

Private IP

↓

NAT Router

↓

Public IP

↓

Internet
```

Responses follow the reverse path.

---

# NAT Translation

Before NAT:

```text
Source

192.168.1.100
```

After NAT:

```text
Source

198.51.100.25
```

Destination remains unchanged.

---

# Return Traffic

Internet Server:

```text
Response

↓

198.51.100.25
```

Router checks its NAT table.

```text
198.51.100.25

↓

192.168.1.100
```

The packet is delivered to the original client.

---

# NAT Translation Table

Example:

| Private IP | Public IP |
|------------|-----------|
| 192.168.1.100 | 198.51.100.25 |
| 192.168.1.101 | 198.51.100.25 |
| 192.168.1.102 | 198.51.100.25 |

The router tracks each translation internally.

---

# NAT Terminology

Common terms include:

### Inside Local

Private IP address.

Example:

```text
192.168.1.100
```

---

### Inside Global

Public IP address representing the internal device.

Example:

```text
198.51.100.25
```

---

### Outside Global

Public IP address of the external server.

Example:

```text
142.250.x.x
```

---

### Outside Local

The external address as seen from the internal network. In many deployments, it is identical to the Outside Global address.

---

# NAT Types

The most common NAT implementations are:

- Static NAT
- Dynamic NAT
- Port Address Translation (PAT)

These are covered in the following lessons.

---

# Enterprise Example

Company Network:

```text
Employees

↓

Private Network

↓

Firewall

↓

NAT

↓

Internet
```

Thousands of employees access the Internet using a limited number of public IP addresses.

---

# Home Network Example

Home Router:

```text
Laptop

↓

Wi-Fi Router

↓

ISP

↓

Internet
```

All household devices share the public IP assigned by the ISP.

---

# Cloud Perspective

Cloud providers use NAT for:

- Private Subnets
- Outbound Internet Access
- Managed NAT Gateways
- Secure Application Access

Virtual machines in private networks can access software updates and external APIs without exposing private IP addresses directly to the Internet.

---

# Kubernetes Perspective

Pods running in private networks often access external services through NAT.

Examples:

- Download Container Images
- Access External APIs
- Reach Cloud Services

Cloud-managed Kubernetes clusters frequently use NAT Gateways for outbound connectivity from private nodes.

---

# Linux Perspective

Display IP addresses.

```bash
ip addr
```

Display routing table.

```bash
ip route
```

Display firewall NAT table (iptables).

```bash
sudo iptables -t nat -L -n -v
```

Display NAT rules (nftables).

```bash
sudo nft list ruleset
```

---

# NAT Packet Flow

```text
Private Device

↓

NAT Router

↓

Public Internet

↓

Web Server

↓

NAT Router

↓

Private Device
```

The NAT device maintains the translation state throughout the connection.

---

# Advantages of NAT

- Conserves Public IPv4 Addresses
- Hides Internal Network Structure
- Simplifies Private Addressing
- Enables Internet Access
- Supports Large Enterprise Networks
- Widely Supported

---

# Limitations

- Not a replacement for a firewall
- Adds processing overhead
- Some protocols require additional NAT handling
- Can complicate troubleshooting
- End-to-end connectivity is reduced

---

# Hands-on Lab

## Task 1

Display IP addresses.

```bash
ip addr
```

---

## Task 2

Display routing table.

```bash
ip route
```

---

## Task 3

View NAT rules (iptables).

```bash
sudo iptables -t nat -L -n -v
```

---

## Task 4

View nftables rules.

```bash
sudo nft list ruleset
```

---

## Task 5

Identify:

- Private IP Address
- Public IP Address

on your network.

---

## Task 6

Draw a NAT workflow showing:

- Laptop
- Router
- Internet
- Web Server

---

## Task 7

Compare:

- Private IP
- Public IP

---

## Task 8

Research how Amazon Web Services (AWS) NAT Gateway, Microsoft Azure NAT Gateway, or Google Cloud Cloud NAT enables outbound Internet access for private resources.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip addr` | Display IP configuration |
| `ip route` | Display routing table |
| `iptables -t nat -L -n -v` | Display iptables NAT rules |
| `nft list ruleset` | Display nftables configuration |
| `ping` | Test connectivity |
| `traceroute` | Trace network path |

---

# Common Mistakes

❌ Assuming NAT provides complete security.

✅ Use a firewall in addition to NAT.

---

❌ Confusing private and public IP addresses.

✅ Understand RFC 1918 private address ranges.

---

❌ Forgetting NAT rules during troubleshooting.

✅ Verify translation tables and firewall policies.

---

❌ Assuming IPv6 always requires NAT.

✅ IPv6 is generally designed for end-to-end addressing without traditional NAT.

---

❌ Ignoring outbound connectivity requirements.

✅ Ensure proper routing and NAT configuration.

---

# Best Practices

- Use private IP addresses for internal networks.
- Limit public IP usage where appropriate.
- Combine NAT with firewall policies.
- Monitor NAT translation usage.
- Document NAT architecture.
- Regularly review NAT rules and routing.

---

# Interview Questions

## Beginner

1. What is NAT?
2. Why is NAT required?
3. What is the difference between private and public IP addresses?
4. What does a NAT router do?

---

## Intermediate

1. Explain the NAT translation process.
2. What are Inside Local and Inside Global addresses?
3. What are the advantages and limitations of NAT?
4. How does NAT conserve IPv4 addresses?

---

## Architect Level

1. Design Internet connectivity for an enterprise using NAT.
2. Explain NAT implementation in hybrid cloud environments.
3. How would you troubleshoot Internet access failures caused by NAT?

---

# Summary

In this lesson, you learned:

- Network Address Translation (NAT)
- Private and Public IP Addresses
- NAT Workflow
- NAT Translation Table
- Inside Local
- Inside Global
- Outside Global
- Enterprise NAT
- Cloud NAT
- Linux NAT Commands

NAT is a foundational networking technology that enables private networks to communicate with the public Internet while conserving scarce IPv4 addresses. By translating private addresses into public addresses, NAT supports scalable enterprise networks, home routers, cloud infrastructures, and Kubernetes environments.

---

## Key Takeaways

- NAT translates **private IP addresses** into **public IP addresses**.
- NAT conserves the limited IPv4 address space.
- Private IP addresses are **not routable** on the public Internet.
- NAT devices maintain translation tables for active connections.
- NAT is widely used in enterprise, home, and cloud environments.
- NAT improves address efficiency but should be combined with firewalls for security.

---

## What's Next?

**[PAT (Port Address Translation)](pat.md)**

In the next lesson, you'll learn about **PAT (Port Address Translation)**.

You'll explore:

- What PAT is
- NAT vs PAT
- Port Translation
- Overloading
- Translation Tables
- Enterprise Internet Access
- Cloud NAT

By the end of the lesson, you'll understand how thousands of devices can share a single public IP address by using different Transmission Control Protocol (TCP) and User Datagram Protocol (UDP) port numbers.
