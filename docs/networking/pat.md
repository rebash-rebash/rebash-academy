---
title: "Port Address Translation (PAT)"
description: "Learn Port Address Translation (PAT / NAT Overload) — port translation, many-to-one mapping, translation tables, and Linux NAT inspection."
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
  - pat
  - nat-overload
  - rebash-networking-mastery
comments: false
status: ready
---

# Port Address Translation (PAT) — Allowing Thousands of Devices to Share One Public IP

> **Port Address Translation (PAT)**, also known as **NAT Overload**, is a type of Network Address Translation that allows **multiple private devices to share a single public IP address** by translating both the **IP address and the Transmission Control Protocol (TCP) / User Datagram Protocol (UDP) port numbers**. PAT is the most commonly used form of NAT in home networks, enterprise environments, cloud platforms, and Internet gateways. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand how PAT works.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 7: NAT & Firewalls → Lesson 2</p>

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

<div markdown>**Lesson:** 2 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Port Address Translation (PAT)
- Learn how PAT differs from NAT
- Understand Port Overloading
- Learn PAT translation tables
- Understand TCP and UDP port translation
- Apply PAT in enterprise and cloud environments
- Troubleshoot PAT issues

---

# Prerequisites

Complete:

- [NAT](nat-and-port-forwarding.md)

---

# Why Learn PAT?

Imagine an office with:

- 2,000 Employees
- 2,000 Laptops

The company owns only:

```text
One

Public IP Address
```

Can everyone access the Internet?

```text
Yes
```

Using:

```text
PAT

(NAT Overload)
```

---

# What is PAT?

**Port Address Translation (PAT)** translates:

- Source IP Address
- Source Port Number

Example:

```text
192.168.1.10:50000

↓

198.51.100.25:10001
```

Another device:

```text
192.168.1.20:50000

↓

198.51.100.25:10002
```

Although both devices use the same public IP address, the translated port numbers keep each connection unique.

---

# Why is PAT Needed?

Without PAT:

```text
One Public IP

↓

One Device
```

With PAT:

```text
One Public IP

↓

Thousands

of Devices
```

PAT dramatically conserves IPv4 addresses.

---

# NAT vs PAT

| NAT | PAT |
|------|-----|
| Translates IP Address | Translates IP Address and Port |
| May require multiple public IPs | Usually uses one public IP |
| One-to-One or Many-to-Many | Many-to-One |
| Less efficient for Internet access | Ideal for Internet access |

---

# What is Port Overloading?

PAT is often called:

```text
NAT Overload
```

Because:

```text
One Public IP

↓

Many Port Numbers

↓

Many Devices
```

Each connection is uniquely identified by its translated port.

---

# Example

Laptop A:

```text
192.168.1.10

Port 50000
```

Laptop B:

```text
192.168.1.20

Port 50000
```

PAT translates:

```text
198.51.100.25

Port 10001
```

and

```text
198.51.100.25

Port 10002
```

No conflict occurs because the public source ports differ.

---

# PAT Workflow

```text
Private Device

↓

Private IP + Port

↓

PAT Router

↓

Public IP + New Port

↓

Internet
```

---

# Translation Example

Before PAT:

```text
192.168.1.100:49152
```

After PAT:

```text
198.51.100.25:30001
```

The destination server replies to the translated public IP and port.

---

# Return Traffic

Server responds:

```text
198.51.100.25:30001
```

PAT Router checks its translation table.

```text
30001

↓

192.168.1.100:49152
```

The packet is delivered to the correct client.

---

# PAT Translation Table

| Private Address | Public Address |
|-----------------|----------------|
| 192.168.1.10:50000 | 198.51.100.25:10001 |
| 192.168.1.20:50000 | 198.51.100.25:10002 |
| 192.168.1.30:52010 | 198.51.100.25:10003 |

The translated port uniquely identifies each active session.

---

# TCP and UDP Ports

PAT works with:

- TCP
- UDP

Examples:

```text
HTTP

TCP 80
```

```text
HTTPS

TCP 443
```

```text
DNS

UDP 53
```

PAT changes the **source port**, not the well-known destination service port.

---

# PAT in Home Networks

Typical home network:

```text
Laptop

↓

Wi-Fi Router

↓

PAT

↓

Internet Service Provider (ISP)

↓

Internet
```

All devices share the single public IP assigned by the ISP.

---

# Enterprise Example

Company:

```text
Employees

↓

Firewall

↓

PAT

↓

Internet
```

Thousands of users browse the Internet using one or a small number of public IP addresses.

---

# Cloud Perspective

Cloud providers implement PAT through managed services such as:

- NAT Gateway
- Cloud NAT
- Internet Gateway integrations

Private virtual machines can:

- Download software updates
- Access external APIs
- Reach Internet services

without having public IP addresses.

---

# Kubernetes Perspective

Private Kubernetes worker nodes often use PAT for:

- Pulling container images
- Accessing cloud APIs
- Downloading packages
- Communicating with external services

This allows nodes to remain private while maintaining outbound Internet connectivity.

---

# Linux Perspective

Display IP configuration.

```bash
ip addr
```

Display routing table.

```bash
ip route
```

Display NAT rules (iptables).

```bash
sudo iptables -t nat -L -n -v
```

Display nftables rules.

```bash
sudo nft list ruleset
```

Display active TCP connections.

```bash
ss -tn
```

---

# PAT Packet Flow

```text
Laptop

↓

PAT Router

↓

Public Internet

↓

Web Server

↓

PAT Router

↓

Laptop
```

The PAT device tracks every active connection using its translation table.

---

# Advantages of PAT

- Conserves Public IPv4 Addresses
- Supports Thousands of Devices
- Simple Internet Access
- Widely Supported
- Easy to Deploy
- Cost Effective

---

# Limitations

- Not a substitute for a firewall
- Adds translation overhead
- Some protocols require additional NAT traversal mechanisms
- Troubleshooting is more complex due to port translation
- Inbound connections require additional configuration such as port forwarding

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

View NAT rules.

```bash
sudo iptables -t nat -L -n -v
```

---

## Task 4

Display nftables rules.

```bash
sudo nft list ruleset
```

---

## Task 5

Display active TCP connections.

```bash
ss -tn
```

---

## Task 6

Draw a PAT translation table showing:

- Three private clients
- One public IP
- Three translated ports

---

## Task 7

Compare:

- NAT
- PAT

---

## Task 8

Research how Amazon Web Services (AWS) NAT Gateway, Microsoft Azure NAT Gateway, or Google Cloud Cloud NAT uses PAT to provide outbound Internet access.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip addr` | Display IP configuration |
| `ip route` | Display routing table |
| `iptables -t nat -L -n -v` | Display NAT rules |
| `nft list ruleset` | Display nftables rules |
| `ss -tn` | Display active TCP connections |
| `ping` | Test connectivity |

---

# Common Mistakes

❌ Confusing NAT with PAT.

✅ PAT translates both IP addresses and ports.

---

❌ Assuming PAT provides firewall protection.

✅ Use firewall policies in addition to PAT.

---

❌ Ignoring translated port numbers during troubleshooting.

✅ Check the PAT translation table.

---

❌ Expecting inbound access to work automatically.

✅ Configure port forwarding or appropriate NAT rules.

---

❌ Assuming PAT changes destination service ports.

✅ PAT normally changes only the source port for outbound connections.

---

# Best Practices

- Use PAT for general outbound Internet access.
- Combine PAT with stateful firewalls.
- Monitor NAT translation usage.
- Keep translation tables within capacity limits.
- Document NAT and PAT configurations.
- Regularly review firewall and NAT policies.

---

# Interview Questions

## Beginner

1. What is PAT?
2. What does NAT Overload mean?
3. What is the difference between NAT and PAT?
4. Why does PAT use port numbers?

---

## Intermediate

1. Explain the PAT translation process.
2. How does PAT distinguish multiple client connections?
3. What are the advantages of PAT?
4. Why is PAT commonly used in enterprise networks?

---

## Architect Level

1. Design Internet access for an enterprise using PAT.
2. Explain how cloud NAT services use PAT.
3. How would you troubleshoot outbound connectivity issues related to PAT?

---

# Summary

In this lesson, you learned:

- Port Address Translation (PAT)
- NAT Overload
- Port Translation
- Translation Tables
- TCP and UDP Port Translation
- Enterprise PAT
- Cloud NAT
- Linux NAT Commands

PAT is the most widely used form of Network Address Translation. By translating both IP addresses and port numbers, it enables thousands of devices to share a single public IPv4 address while maintaining unique network sessions. PAT is a critical technology in enterprise, home, and cloud networking.

---

## Key Takeaways

- PAT is also known as **NAT Overload**.
- PAT translates both **IP addresses and port numbers**.
- Multiple devices can share a **single public IP address**.
- Translation tables map private connections to unique public ports.
- PAT is widely used for Internet access in enterprise and cloud environments.
- PAT conserves IPv4 addresses while supporting large numbers of simultaneous connections.

---

## What's Next?

**[Static NAT](static-nat.md)**

In the next lesson, you'll learn about **Static NAT**.

You'll explore:

- One-to-One Address Translation
- Static NAT Configuration
- Internal and External Servers
- Port Forwarding Concepts
- Enterprise Use Cases
- Cloud Public IP Mapping

By the end of the lesson, you'll understand how Static NAT provides permanent mappings between private and public IP addresses, enabling external users to access internal services securely.
