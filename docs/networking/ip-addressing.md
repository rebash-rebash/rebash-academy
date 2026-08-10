---
title: "IP Address"
description: "Learn Internet Protocol (IP) addressing — IPv4 and IPv6, public vs private, static vs dynamic, network/host portions, and Linux IP troubleshooting."
difficulty: beginner
estimated_time: "90 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 1 · Networking Fundamentals"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - kubernetes-engineer
  - platform-engineer
tags:
  - networking
  - ip
  - ipv4
  - ipv6
  - fundamentals
  - rebash-networking-mastery
comments: false
status: ready
---

# IP Address — The Logical Address of a Network Device

> Every device connected to a network requires a unique **IP (Internet Protocol) Address** to communicate with other devices. Just as a postal address helps deliver letters to the correct house, an IP address enables network devices to send and receive data across local networks and the Internet. Whether you're browsing a website, accessing cloud services, connecting to a Kubernetes cluster, or managing Linux servers, IP addressing is the foundation of all network communication. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer must understand IP addressing.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 1: Networking Fundamentals → Lesson 8</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Networking Fundamentals</div>

<div markdown>**Lesson:** 8 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand what an IP Address is
- Differentiate between IPv4 and IPv6
- Understand public and private IP addresses
- Explain static and dynamic IP addressing
- Identify network and host portions
- Understand how devices communicate using IP addresses
- View and troubleshoot IP configuration in Linux

---

# Prerequisites

Complete:

- [What is Networking?](introduction-to-networking.md)
- [Types of Networks](types-of-networks.md)
- [Network Topologies](network-topologies.md)
- [OSI Model](osi-model.md)
- [TCP/IP Model](tcp-ip-model.md)
- [Data Encapsulation](data-encapsulation.md)
- [MAC Address](mac-address.md)

---

# Why Learn IP Addresses?

Imagine sending a parcel without a destination address.

The courier would never know where to deliver it.

Similarly, without an IP address:

- Computers cannot communicate.
- Routers cannot forward packets.
- Websites cannot be accessed.
- Cloud services become unreachable.

Every network communication depends on IP addressing.

---

# What is an IP Address?

An **IP Address (Internet Protocol Address)** is a **logical address** assigned to a network device.

It uniquely identifies a device on a network and enables communication between devices.

Unlike Media Access Control (MAC) addresses, IP addresses can change depending on the network configuration.

---

# Real-Life Analogy

Think of:

- **MAC Address** → Fingerprint
- **IP Address** → Home Address

Your fingerprint identifies you.

Your home address tells others where to find you.

Similarly:

- MAC identifies the device.
- IP identifies the device's network location.

---

# Why Do Devices Need IP Addresses?

IP addresses allow devices to:

- Send data
- Receive data
- Identify remote devices
- Communicate across different networks
- Access the Internet

Without IP addresses, routers would not know where to forward packets.

---

# IPv4 and IPv6

There are two versions of IP currently in use.

| Version | Address Length |
|----------|----------------|
| IPv4 | 32-bit |
| IPv6 | 128-bit |

IPv4 remains the most widely deployed, while IPv6 is increasingly adopted due to IPv4 address exhaustion.

---

# IPv4 Address

An IPv4 address contains **32 bits** divided into four octets.

Example:

```text
192.168.1.10
```

Each octet ranges from:

```text
0–255
```

Another example:

```text
10.0.0.15
```

---

# IPv4 Structure

```text
192 . 168 . 1 . 10

│      │     │    │

8      8     8    8 Bits
```

Total:

```text
32 Bits
```

---

# IPv6 Address

An IPv6 address contains **128 bits** represented in hexadecimal.

Example:

```text
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

Compressed representation:

```text
2001:db8:85a3::8a2e:370:7334
```

IPv6 supports an enormous address space.

---

# Logical Address

Unlike a MAC address, an IP address can change.

Examples:

Home Wi-Fi:

```text
192.168.1.20
```

Office Wi-Fi:

```text
10.10.20.35
```

Cloud VM:

```text
172.31.10.5
```

The same device may receive different IP addresses on different networks.

---

# Public IP Address

A **Public IP Address** is globally unique and reachable over the Internet.

Example:

```text
142.250.183.110
```

Public IPs are assigned by Internet Service Providers (ISPs) or cloud providers.

Used by:

- Websites
- Cloud servers
- Internet-facing services

---

# Private IP Address

Private IP addresses are used within internal networks and are **not directly routable on the Internet**.

Private IPv4 ranges:

```text
10.0.0.0/8

172.16.0.0 – 172.31.255.255

192.168.0.0/16
```

Examples:

```text
192.168.1.50

10.1.2.100

172.20.5.10
```

---

# Public vs Private IP

| Public IP | Private IP |
|------------|------------|
| Internet Routable | Local Network Only |
| Globally Unique | Reusable |
| Assigned by ISP/Cloud | Assigned by Local Network |
| Accessible from Internet | Protected Behind NAT |

---

# Static IP Address

A **Static IP Address** remains the same until it is manually changed.

Commonly used for:

- Servers
- Routers
- Firewalls
- Domain Name System (DNS) Servers
- Kubernetes Control Plane Nodes

Advantages:

- Predictable
- Reliable
- Easy to manage

---

# Dynamic IP Address

A **Dynamic IP Address** is assigned automatically by a Dynamic Host Configuration Protocol (DHCP) server.

Commonly used for:

- Laptops
- Smartphones
- Tablets
- Home devices

Advantages:

- Automatic configuration
- Efficient address management

---

# Network and Host Portions

Every IP address consists of:

- Network Portion
- Host Portion

Example:

```text
192.168.1.25/24
```

Network:

```text
192.168.1
```

Host:

```text
25
```

The subnet mask determines where the network ends and the host begins.

---

# How Communication Works

Suppose:

Laptop:

```text
192.168.1.10
```

Server:

```text
192.168.1.20
```

Communication:

```text
Laptop

↓

Switch

↓

Server
```

Both devices communicate directly because they belong to the same network.

---

# Different Networks

Suppose:

Laptop:

```text
192.168.1.10
```

Web Server:

```text
8.8.8.8
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

Web Server
```

The router forwards packets between networks.

---

# IP Address Assignment

Devices obtain IP addresses through:

- Static configuration
- DHCP
- Cloud automation
- Kubernetes networking

We'll explore DHCP in detail later in the course.

---

# Viewing IP Addresses in Linux

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

Display interface details.

```bash
ip link
```

---

Traditional command:

```bash
ifconfig
```

---

# DNS and IP Addresses

Humans prefer names.

Example:

```text
google.com
```

Computers use IP addresses.

Example:

```text
142.250.183.110
```

DNS translates domain names into IP addresses.

---

# IP Address vs MAC Address

| IP Address | MAC Address |
|-------------|-------------|
| Layer 3 | Layer 2 |
| Logical Address | Physical Address |
| Can Change | Usually Permanent |
| Used by Routers | Used by Switches |
| Internet Communication | Local Network Communication |

---

# Production Perspective

IP addressing is used in:

- Enterprise Networks
- Kubernetes Clusters
- Cloud Virtual Private Clouds (VPCs)
- Load Balancers
- Firewalls
- Virtual Private Networks (VPNs)
- Virtual Machines
- Containers

Every production environment relies on proper IP address planning.

---

# Cloud Perspective

Cloud platforms assign IP addresses to:

- Virtual Machines
- Kubernetes Nodes
- Load Balancers
- Databases
- Storage Services

Examples:

- AWS Elastic IP
- Azure Public IP
- Google Cloud External IP

Cloud networking is built around IP communication.

---

# Kubernetes Perspective

Every Kubernetes object communicates using IP addresses.

Examples:

- Pods
- Nodes
- Services
- Ingress Controllers

Kubernetes automatically manages IP allocation within the cluster.

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

Display network interfaces.

```bash
ip link
```

---

## Task 4

Test connectivity.

```bash
ping google.com
```

---

## Task 5

Display your public IP address.

```bash
curl ifconfig.me
```

---

## Task 6

Identify whether your local IP address is public or private.

---

## Task 7

Determine the network and host portions of the following address:

```text
192.168.100.25/24
```

---

## Task 8

Create a simple network diagram containing:

- Laptop
- Switch
- Router
- Internet
- Web Server

Label the IP address used at each stage and explain how the packet reaches the destination.

---

# Linux Commands

| Command | Purpose |
|----------|---------|
| `ip addr` | Display IP addresses |
| `ip route` | Display routing table |
| `ip link` | Display interfaces |
| `ping` | Test connectivity |
| `hostname -I` | Display assigned IP addresses |
| `curl ifconfig.me` | Display public IP address |

---

# Common Mistakes

❌ Confusing MAC and IP addresses.

✅ MAC identifies the device; IP identifies its network location.

---

❌ Assuming private IPs work directly on the Internet.

✅ Private IPs require Network Address Translation (NAT) to access the Internet.

---

❌ Believing static IPs never change automatically.

✅ They remain fixed only until manually modified.

---

❌ Ignoring subnet information.

✅ Always consider the subnet when determining communication.

---

❌ Assuming DNS replaces IP addresses.

✅ DNS translates names into IP addresses; communication still uses IPs.

---

# Best Practices

- Use static IPs for servers and infrastructure devices.
- Use DHCP for client devices where appropriate.
- Document IP address assignments.
- Avoid IP address conflicts.
- Plan IP address allocation before deploying large environments.
- Understand the difference between public and private IP addresses.

---

# Interview Questions

## Beginner

1. What is an IP address?
2. What is the difference between IPv4 and IPv6?
3. What is the difference between a public and private IP address?
4. Why do devices need IP addresses?

---

## Intermediate

1. Compare static and dynamic IP addressing.
2. Explain the difference between MAC and IP addresses.
3. What happens when two devices are on different networks?
4. How does DNS relate to IP addresses?

---

## Architect Level

1. How would you design an IP addressing scheme for a large enterprise?
2. Explain IP address management in cloud environments.
3. How does Kubernetes allocate IP addresses to Pods and Services?

---

# Summary

In this lesson, you learned:

- What an IP Address is
- IPv4 and IPv6
- Public and private IP addresses
- Static and dynamic IP assignment
- Network and host portions
- IP communication
- Linux commands for viewing IP configuration
- Cloud and Kubernetes IP addressing

IP addresses provide the logical foundation of networking. While MAC addresses identify devices within a local network, IP addresses allow communication across networks and the Internet. Every modern application, cloud platform, and enterprise infrastructure depends on accurate IP addressing and routing.

---

## Key Takeaways

- An IP address is a logical network identifier.
- IPv4 uses 32-bit addresses; IPv6 uses 128-bit addresses.
- Public IP addresses are Internet routable; private IP addresses are used within local networks.
- Static IPs are fixed; dynamic IPs are assigned automatically.
- Routers use IP addresses to forward packets between networks.

---

## What's Next?

**[Ports and Protocols](ports-and-protocols.md)**
