---
title: "Static NAT"
description: "Learn Static Network Address Translation — permanent one-to-one private-to-public mapping, inbound access, DMZ use cases, and Linux DNAT basics."
difficulty: beginner
estimated_time: "90 min"
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
  - static-nat
  - dnat
  - rebash-networking-mastery
comments: false
status: ready
---

# Static NAT — Permanent One-to-One IP Address Translation

> **Static Network Address Translation (Static NAT)** is a type of NAT that creates a **permanent one-to-one mapping** between a private IP address and a public IP address. Unlike Port Address Translation (PAT), where multiple devices share a public IP, Static NAT ensures that a specific internal device is always reachable using the same public IP address. Static NAT is commonly used for web servers, mail servers, Virtual Private Network (VPN) gateways, firewalls, and other services that must be accessible from the Internet. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand Static NAT.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 7: NAT & Firewalls → Lesson 3</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** NAT & Firewalls</div>

<div markdown>**Lesson:** 3 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Static NAT
- Learn One-to-One Address Translation
- Understand Permanent Address Mapping
- Learn inbound and outbound communication
- Apply Static NAT in enterprise and cloud environments
- Troubleshoot Static NAT issues

---

# Prerequisites

Complete:

- [NAT](nat-and-port-forwarding.md)
- [PAT](pat.md)

---

# Why Learn Static NAT?

Imagine a company hosts:

- Website
- Mail Server
- VPN Gateway

Users from the Internet must always connect to:

```text
One

Public IP Address
```

The server itself uses:

```text
Private IP
```

The solution is:

```text
Static NAT
```

---

# What is Static NAT?

Static NAT creates a permanent mapping between:

```text
Private IP

↓

Public IP
```

Example:

```text
192.168.10.20

↓

203.0.113.20
```

Every packet follows the same translation.

---

# One-to-One Mapping

Static NAT always maintains:

```text
One Private IP

↓

One Public IP
```

Unlike PAT:

```text
Many Devices

↓

One Public IP
```

Static NAT reserves a dedicated public IP for each mapped device.

---

# Why Use Static NAT?

Common use cases include:

- Public Web Servers
- Mail Servers
- VPN Gateways
- Domain Name System (DNS) Servers
- Application Servers
- Remote Access Systems

These systems require predictable, permanent public addresses.

---

# Static NAT Workflow

```text
Internet User

↓

Public IP

↓

Static NAT

↓

Private Server
```

Responses return through the same translation.

---

# Example

Internal Web Server:

```text
192.168.1.50
```

Mapped to:

```text
198.51.100.50
```

Internet users connect to:

```text
https://198.51.100.50
```

The NAT device forwards traffic to:

```text
192.168.1.50
```

---

# Translation Table

| Private IP | Public IP |
|------------|-----------|
| 192.168.1.50 | 198.51.100.50 |
| 192.168.1.60 | 198.51.100.60 |
| 192.168.1.70 | 198.51.100.70 |

These mappings remain fixed until changed by the administrator.

---

# Outbound Traffic

Server:

```text
192.168.1.50
```

Requests:

```text
google.com
```

NAT translates:

```text
192.168.1.50

↓

198.51.100.50
```

The server always uses the same public IP.

---

# Inbound Traffic

Internet Client:

```text
198.51.100.50
```

↓

```text
Static NAT
```

↓

```text
192.168.1.50
```

External users never see the private IP address.

---

# Static NAT vs PAT

| Static NAT | PAT |
|------------|-----|
| One-to-One | Many-to-One |
| Dedicated Public IP | Shared Public IP |
| Permanent Mapping | Dynamic Port Mapping |
| Supports Inbound Access Easily | Primarily Outbound Access |

---

# Static NAT vs Dynamic NAT

| Static NAT | Dynamic NAT |
|------------|-------------|
| Permanent Mapping | Temporary Mapping |
| Fixed Public IP | Public IP Assigned from a Pool |
| Manual Configuration | Automatic Allocation |
| Best for Servers | Best for Client Devices |

---

# Enterprise Example

Company Network:

```text
Internet

↓

Firewall

↓

203.0.113.25

↓

Static NAT

↓

192.168.10.25

↓

Web Server
```

Customers always access the same public IP address.

---

# DMZ Example

A company places public-facing servers in a Demilitarised Zone (DMZ).

```text
Internet

↓

Firewall

↓

DMZ

↓

Web Server

↓

Private Network
```

Each server has a Static NAT mapping from a public IP to its private IP.

---

# Cloud Perspective

Cloud platforms commonly provide:

- Public IP Addresses
- Elastic IPs
- Reserved Public IPs
- Static Public IP Assignments

These services behave similarly to Static NAT by permanently associating a public IP with a virtual machine or network interface.

---

# Kubernetes Perspective

Kubernetes Services typically expose applications using:

- Load Balancers
- Ingress Controllers

Behind the scenes, cloud providers may use static public IP mappings so external users can consistently reach the service.

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

Display NAT rules.

```bash
sudo iptables -t nat -L -n -v
```

Display nftables configuration.

```bash
sudo nft list ruleset
```

Example Destination NAT (DNAT) rule (iptables):

```bash
sudo iptables -t nat -A PREROUTING -d 198.51.100.50 -j DNAT --to-destination 192.168.1.50
```

---

# Static NAT Packet Flow

```text
Internet User

↓

Public IP

↓

Firewall

↓

Static NAT

↓

Private Server

↓

Response

↓

Firewall

↓

Internet User
```

The mapping remains constant throughout the life of the configuration.

---

# Advantages of Static NAT

- Permanent Address Mapping
- Predictable Connectivity
- Supports Public Services
- Simple Troubleshooting
- Ideal for Servers
- Stable Public Identity

---

# Limitations

- Requires one public IP address for each mapped device
- Consumes more public IPv4 addresses
- Requires manual configuration
- Not suitable for large numbers of client devices

---

# Hands-on Lab

## Task 1

Display IP configuration.

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

Display NAT rules.

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

Draw a Static NAT diagram showing:

- Internet
- Firewall
- Public IP
- Private Server

---

## Task 6

Compare:

- Static NAT
- PAT

---

## Task 7

Compare:

- Static NAT
- Dynamic NAT

---

## Task 8

Design a Static NAT plan for:

- Web Server
- Mail Server
- VPN Gateway
- DNS Server

Assign one public IP address to each service.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip addr` | Display IP configuration |
| `ip route` | Display routing table |
| `iptables -t nat -L -n -v` | Display NAT rules |
| `nft list ruleset` | Display nftables configuration |
| `ping` | Test connectivity |
| `ss -tuln` | Display listening ports |

---

# Common Mistakes

❌ Using Static NAT for every client device.

✅ Reserve Static NAT for systems requiring inbound access.

---

❌ Forgetting firewall rules.

✅ Allow only the required ports through the firewall.

---

❌ Mapping multiple servers to the same public IP without appropriate port forwarding.

✅ Use unique public IPs or carefully configured destination NAT rules.

---

❌ Exposing unnecessary services.

✅ Publish only services that must be accessible from the Internet.

---

❌ Not documenting NAT mappings.

✅ Maintain an inventory of all static translations.

---

# Best Practices

- Use Static NAT only for publicly accessible services.
- Combine Static NAT with stateful firewall rules.
- Restrict exposed ports to the minimum required.
- Monitor public-facing servers.
- Document all static mappings.
- Regularly review exposed services and remove unused mappings.

---

# Interview Questions

## Beginner

1. What is Static NAT?
2. Why is Static NAT used?
3. What is a one-to-one NAT mapping?
4. Which systems typically use Static NAT?

---

## Intermediate

1. Compare Static NAT and PAT.
2. Compare Static NAT and Dynamic NAT.
3. Why is Static NAT suitable for web servers?
4. What are the advantages of Static NAT?

---

## Architect Level

1. Design Internet access for an enterprise web application using Static NAT.
2. Explain how Static NAT works with firewalls and DMZs.
3. How would you troubleshoot inbound connectivity issues to a server using Static NAT?

---

# Summary

In this lesson, you learned:

- Static NAT
- One-to-One Address Translation
- Permanent Address Mapping
- Inbound and Outbound Communication
- Translation Tables
- Enterprise Static NAT
- Cloud Public IP Mapping
- Linux NAT Commands

Static NAT provides a permanent mapping between private and public IP addresses, making it ideal for servers and services that must be consistently accessible from the Internet. Although it consumes more public IPv4 addresses than PAT, its predictability and simplicity make it an essential technology for enterprise and cloud networking.

---

## Key Takeaways

- Static NAT provides a **permanent one-to-one** mapping between private and public IP addresses.
- Each internal server receives a **dedicated public IP address**.
- Static NAT is commonly used for **web servers, mail servers, VPN gateways, and DNS servers**.
- It supports reliable inbound and outbound communication.
- Static NAT should be combined with **firewall policies** to secure exposed services.
- Cloud platforms offer similar functionality through **reserved or static public IP assignments**.

---

## What's Next?

**[Dynamic NAT](dynamic-nat.md)**

In the next lesson, you'll learn about **Dynamic NAT**.

You'll explore:

- Address Pools
- Dynamic Address Allocation
- One-to-One Temporary Mappings
- NAT Pools
- Translation Lifecycles
- Enterprise Use Cases
- Dynamic NAT vs Static NAT vs PAT

By the end of the lesson, you'll understand how Dynamic NAT automatically assigns public IP addresses from a pool to private devices and when it is appropriate to use this approach.
