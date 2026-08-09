---
title: "IP Configuration — Configuring Network Interfaces in Linux"
description: "Configure Linux network interfaces — view and assign IP addresses, understand DHCP and CIDR, manage gateways and routes, and verify connectivity with the ip command."
difficulty: intermediate
estimated_time: "70 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 8 · Networking"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - networking
  - ip
  - dhcp
  - netplan
  - rebash-linux-mastery
comments: false
status: ready
---

# IP Configuration — Configuring Network Interfaces in Linux

> **IP Configuration** is the process of assigning and managing IP addresses, subnet masks, gateways, DNS servers, and network interfaces. Every Linux server, cloud virtual machine, Kubernetes node, and container requires proper IP configuration to communicate with other systems. Understanding IP configuration is a fundamental skill for Linux administrators, DevOps engineers, Cloud Architects, Network Engineers, and Site Reliability Engineers (SREs).

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 8: Networking → Lesson 2</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 70 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Networking</div>

<div markdown>**Lesson:** 2 of 13</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand network interfaces
- View IP configurations
- Configure static IP addresses
- Understand DHCP
- Manage network interfaces
- Configure gateways
- Verify network connectivity
- Apply IP configuration in production

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management
- Module 5 – Users and Groups
- Module 6 – Process Management
- Module 7 – Package Management
- Module 8 Lesson 1 – TCP/IP Basics

---

# Why Learn IP Configuration?

Imagine:

- A new cloud server cannot reach the Internet.
- A Kubernetes node cannot join the cluster.
- SSH access stops working.
- Two servers cannot communicate.

In many cases, the root cause is an incorrect IP configuration.

---

# What is IP Configuration?

IP configuration defines how a device communicates on a network.

Typical configuration includes:

- IP Address
- Subnet Mask (or Prefix Length)
- Default Gateway
- DNS Server
- Network Interface

Without proper configuration, network communication is not possible.

---

# Network Configuration Components

```text
Network Interface
        │
        ▼
IP Address
        │
        ▼
Subnet Mask
        │
        ▼
Default Gateway
        │
        ▼
DNS Server
```

Each component plays a specific role in network communication.

---

# Network Interfaces

A **network interface** connects the operating system to a network.

Common interface names:

```text
eth0

ens33

ens160

enp0s3

wlan0
```

Modern Linux systems use predictable network interface names such as `ens160` or `enp0s3`.

---

# View Network Interfaces

Display all interfaces.

```bash
ip link
```

Example:

```text
lo

ens160
```

---

# Loopback Interface

Linux includes a special interface:

```text
lo
```

Loopback address:

```text
127.0.0.1
```

Purpose:

- Local communication
- Testing
- Internal services

---

# View IP Addresses

Display configured IP addresses.

```bash
ip addr
```

Example:

```text
192.168.1.100/24
```

Show a specific interface.

```bash
ip addr show ens160
```

---

# Understanding CIDR Notation

Example:

```text
192.168.1.100/24
```

Meaning:

- IP Address:

```text
192.168.1.100
```

- Prefix Length:

```text
24
```

Equivalent subnet mask:

```text
255.255.255.0
```

---

# Static IP Address

A static IP address remains the same until changed manually.

Example:

```text
192.168.1.100
```

Advantages:

- Predictable
- Ideal for servers
- Required for many production workloads

---

# Dynamic IP Address (DHCP)

DHCP stands for:

```text
Dynamic Host Configuration Protocol
```

A DHCP server automatically assigns:

- IP Address
- Gateway
- DNS Server
- Lease Time

Commonly used for:

- Laptops
- Desktops
- Home networks
- Cloud instances (during initial provisioning)

---

# Assign a Temporary IP Address

Assign an IP address to an interface.

```bash
sudo ip addr add 192.168.1.100/24 dev ens160
```

Verify:

```bash
ip addr show ens160
```

> This change is temporary and will be lost after a reboot or interface reset.

---

# Remove an IP Address

```bash
sudo ip addr del 192.168.1.100/24 dev ens160
```

---

# Enable a Network Interface

```bash
sudo ip link set ens160 up
```

---

# Disable a Network Interface

```bash
sudo ip link set ens160 down
```

Use with caution on remote systems, as it may disconnect your session.

---

# View Routing Information

Display the routing table.

```bash
ip route
```

Example:

```text
default via 192.168.1.1
```

---

# Default Gateway

The default gateway is the router used to reach networks outside the local subnet.

Example:

```text
192.168.1.1
```

View the default gateway.

```bash
ip route
```

---

# Add a Temporary Default Gateway

```bash
sudo ip route add default via 192.168.1.1
```

Delete the default gateway.

```bash
sudo ip route del default
```

---

# Test Connectivity

Ping the gateway.

```bash
ping 192.168.1.1
```

Ping an external IP.

```bash
ping 8.8.8.8
```

Ping a domain.

```bash
ping google.com
```

---

# Persistent Configuration

Temporary changes made with the `ip` command are not preserved after a reboot.

Persistent configuration depends on the Linux distribution.

Common tools include:

| Distribution | Common Configuration Method |
|--------------|-----------------------------|
| Ubuntu Server | Netplan |
| RHEL / Rocky / AlmaLinux | NetworkManager (`nmcli`) or network configuration files |
| Fedora | NetworkManager |

---

# Common Commands

View interfaces.

```bash
ip link
```

View IP addresses.

```bash
ip addr
```

View routing table.

```bash
ip route
```

Bring interface up.

```bash
sudo ip link set ens160 up
```

Bring interface down.

```bash
sudo ip link set ens160 down
```

---

# Real Production Examples

Display server IP.

```bash
ip addr
```

Verify default route.

```bash
ip route
```

Test gateway.

```bash
ping 192.168.1.1
```

Enable interface.

```bash
sudo ip link set ens160 up
```

---

# Production Perspective

IP configuration is required for:

- Cloud virtual machines
- Kubernetes nodes
- Docker hosts
- Database servers
- Web servers
- VPN gateways
- Firewalls
- Enterprise networks

Incorrect IP configuration is one of the most common causes of network connectivity issues.

---

# Hands-on Lab

## Task 1

List network interfaces.

```bash
ip link
```

---

## Task 2

Display IP addresses.

```bash
ip addr
```

---

## Task 3

View the routing table.

```bash
ip route
```

---

## Task 4

Identify the default gateway.

```bash
ip route
```

---

## Task 5

Test gateway connectivity.

```bash
ping <gateway-ip>
```

Replace `<gateway-ip>` with the gateway shown in your routing table.

---

## Task 6

Display the loopback interface.

```bash
ip addr show lo
```

---

## Task 7

Bring a non-production interface down and back up (if available).

```bash
sudo ip link set <interface> down

sudo ip link set <interface> up
```

> Do **not** perform this on a remote production server or on the interface you're currently using.

---

## Task 8

Display the IP configuration for a specific interface.

```bash
ip addr show <interface>
```

Replace `<interface>` with your network interface name (for example, `ens160`).

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `ip addr` | View IP addresses | Verify server configuration |
| `ip link` | View network interfaces | Interface management |
| `ip route` | Display routing table | Routing verification |
| `ip addr add` | Assign temporary IP | Testing |
| `ip addr del` | Remove temporary IP | Cleanup |
| `ip link set up` | Enable interface | Restore connectivity |
| `ip link set down` | Disable interface | Maintenance |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A newly provisioned cloud virtual machine cannot access the Internet.

Investigation:

Check the IP address.

```bash
ip addr
```

Verify the routing table.

```bash
ip route
```

Check connectivity to the gateway.

```bash
ping <gateway-ip>
```

The default route is missing.

Temporarily add the gateway.

```bash
sudo ip route add default via <gateway-ip>
```

Verify Internet access.

```bash
ping 8.8.8.8
```

The server can now reach external networks. A persistent configuration is then applied using the distribution's network management tools.

---

# Best Practices

- Use static IP addresses for production servers.
- Use DHCP where automatic configuration is appropriate.
- Verify the default gateway after configuration changes.
- Use the `ip` command instead of the deprecated `ifconfig`.
- Test connectivity after making network changes.
- Apply persistent configuration using the distribution's supported network management tools.

---

# Common Mistakes

❌ Forgetting that `ip` command changes are temporary.

✅ Remember to that `ip` command changes are temporary.

---

❌ Bringing down the active network interface on a remote server.

✅ Avoid this mistake: bringing down the active network interface on a remote server.

---

❌ Configuring an incorrect subnet or gateway.

✅ Avoid this mistake: configuring an incorrect subnet or gateway.

---

❌ Forgetting to verify routing after assigning an IP address.

✅ Remember to to verify routing after assigning an IP address.

---

# Interview Questions
## Beginner

1. What is an IP address?
2. What is the difference between a static IP address and DHCP?
3. Which command displays IP addresses?
4. What is the purpose of the loopback interface?

---

## Intermediate

1. What is CIDR notation?
2. How do you temporarily assign an IP address?
3. How do you view the routing table?
4. Why is the default gateway important?

---

## Architect Level

1. How would you configure networking for production Linux servers?
2. How would you troubleshoot a server that cannot reach the Internet?
3. Why are static IP addresses commonly used for infrastructure services?

---

# Summary

In this lesson, you learned:

- IP configuration
- Network interfaces
- Static and dynamic addressing
- DHCP
- Routing
- Default gateways
- Temporary network configuration
- Production networking best practices

Proper IP configuration is the foundation of Linux networking. Every server, container, and cloud instance depends on correctly configured network interfaces, IP addresses, gateways, and routing information to communicate reliably.

---

## Key Takeaways

- Every network interface requires proper IP configuration.
- Static IP addresses are preferred for production servers.
- DHCP automatically assigns network settings.
- The `ip` command is the standard tool for Linux network configuration.
- The default gateway enables communication outside the local network.
- Changes made with the `ip` command are temporary unless made persistent.

---

## What's Next?

**[DNS (Domain Name System) — Translating Domain Names into IP Addresses](dns-on-linux.md)**

You'll explore:

- How DNS works
- DNS records
- Name resolution
- DNS configuration
- DNS troubleshooting
- Common DNS tools
- Production DNS best practices

Understanding DNS is essential because nearly every network application depends on reliable name resolution.
