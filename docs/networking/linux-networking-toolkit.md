---
title: "Linux ip Command"
description: "Learn the Linux ip command — interfaces, addresses, routes, neighbor tables, VLANs, namespaces, and a practical connectivity troubleshooting workflow."
difficulty: beginner
estimated_time: "140 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 9 · Linux Networking"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - linux
  - ip
  - iproute2
  - rebash-networking-mastery
comments: false
status: ready
---

# Linux `ip` Command — Managing and Troubleshooting Network Configuration

> The **`ip` command** is the modern Linux networking utility used to configure, manage, and troubleshoot **network interfaces, IP addresses, routing tables, ARP/Neighbor tables, tunnels, Virtual Local Area Networks (VLANs), and network namespaces**. It replaces legacy networking tools such as **ifconfig**, **route**, **arp**, and **netstat** for many networking tasks. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should master the `ip` command.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 9: Linux Networking → Lesson 1</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 140 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Linux Networking</div>

<div markdown>**Lesson:** 1 of 10</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `ip` command
- Manage network interfaces
- Configure IP addresses
- Manage routing tables
- View neighbor tables
- Troubleshoot Linux networking
- Work with VLANs and network namespaces

---

# Prerequisites

Complete:

- Module 1–8

Basic understanding of:

- IP Addressing
- Routing
- Linux Commands

---

# Why Learn the `ip` Command?

Almost every networking problem on Linux starts with one question:

```text
Does the machine have

Network Connectivity?
```

The first tool every Linux engineer uses is:

```bash
ip
```

Whether you're troubleshooting:

- No Internet
- Wrong IP Address
- Routing Issues
- Kubernetes Networking
- Docker Networking
- Cloud VM Connectivity

the `ip` command is one of the first diagnostic tools.

---

# What is the `ip` Command?

The `ip` command belongs to the:

```text
iproute2
```

package.

It manages:

- Network Interfaces
- IP Addresses
- Routes
- Neighbor Tables
- Tunnels
- VLANs
- Network Namespaces

---

# Why Replace ifconfig?

Older Linux systems used:

```bash
ifconfig
route
arp
```

Modern Linux uses:

```bash
ip
```

Advantages:

- Unified Tool
- IPv4 & IPv6 Support
- More Features
- Better Performance
- Active Development

---

# Basic Syntax

```bash
ip OBJECT COMMAND
```

Examples:

```bash
ip addr
```

```bash
ip route
```

```bash
ip link
```

---

# Display Interfaces

Show all network interfaces.

```bash
ip link
```

Example output:

```text
1: lo
2: eth0
3: ens5
```

---

# Display IP Addresses

```bash
ip addr
```

Shortcut:

```bash
ip a
```

Example:

```text
eth0

192.168.1.10/24
```

---

# Display IPv4 Only

```bash
ip -4 addr
```

---

# Display IPv6 Only

```bash
ip -6 addr
```

---

# Show Specific Interface

```bash
ip addr show eth0
```

or

```bash
ip a show eth0
```

---

# Bring Interface Up

```bash
sudo ip link set eth0 up
```

---

# Bring Interface Down

```bash
sudo ip link set eth0 down
```

---

# Assign IP Address

```bash
sudo ip addr add 192.168.1.100/24 dev eth0
```

---

# Remove IP Address

```bash
sudo ip addr del 192.168.1.100/24 dev eth0
```

---

# Display Routing Table

```bash
ip route
```

Shortcut:

```bash
ip r
```

Example:

```text
default via 192.168.1.1

192.168.1.0/24 dev eth0
```

---

# Add Default Route

```bash
sudo ip route add default via 192.168.1.1
```

---

# Delete Default Route

```bash
sudo ip route del default
```

---

# Add Static Route

```bash
sudo ip route add 10.10.10.0/24 via 192.168.1.1
```

---

# Delete Static Route

```bash
sudo ip route del 10.10.10.0/24
```

---

# Neighbor Table

Display ARP/Neighbor entries.

```bash
ip neigh
```

Example:

```text
192.168.1.1

aa:bb:cc:dd:ee:ff
```

---

# Flush Neighbor Cache

```bash
sudo ip neigh flush all
```

---

# Interface Statistics

```bash
ip -s link
```

Displays:

- RX Packets
- TX Packets
- Errors
- Dropped Packets

---

# Monitor Network Changes

```bash
ip monitor
```

Displays changes in real time.

Useful for:

- Interface State Changes
- Address Changes
- Route Updates

---

# Display Routing Rules

```bash
ip rule
```

Useful for:

- Policy-Based Routing
- Multiple Routing Tables

---

# Display Routing Tables

```bash
ip route show table all
```

---

# Create VLAN Interface

Example:

```bash
sudo ip link add link eth0 name eth0.100 type vlan id 100
```

Bring it up.

```bash
sudo ip link set eth0.100 up
```

Assign an address.

```bash
sudo ip addr add 192.168.100.10/24 dev eth0.100
```

---

# Network Namespaces

List namespaces.

```bash
ip netns list
```

Create namespace.

```bash
sudo ip netns add lab1
```

Delete namespace.

```bash
sudo ip netns del lab1
```

Run command inside namespace.

```bash
sudo ip netns exec lab1 ip addr
```

Network namespaces will be covered in detail later in this module.

---

# Tunnel Interfaces

Display tunnel interfaces.

```bash
ip tunnel
```

Examples include:

- GRE
- SIT
- IPIP

---

# Enterprise Example

Production server:

```text
Internet

↓

Router

↓

Linux Server
```

Troubleshooting steps:

```bash
ip addr

↓

ip route

↓

ip neigh

↓

ping Gateway
```

---

# Cloud Perspective

Cloud engineers frequently use:

```bash
ip addr
```

to verify:

- Private IP
- Secondary IPs
- IPv6 Address

Use:

```bash
ip route
```

to troubleshoot:

- Cloud Routing
- VPN
- Network Address Translation (NAT)
- Load Balancer Issues

---

# Kubernetes Perspective

On Kubernetes nodes:

```bash
ip addr
```

shows:

- Pod Interfaces
- Container Network Interface (CNI) Interfaces
- Bridge Interfaces

Example:

```text
cni0

flannel.1

vxlan.calico
```

Routes can be inspected using:

```bash
ip route
```

---

# Linux Networking Workflow

```text
Application

↓

Socket

↓

Network Interface

↓

Routing

↓

Gateway

↓

Internet
```

The `ip` command helps inspect each stage of this path.

---

# Common `ip` Commands

| Command | Purpose |
|----------|----------|
| `ip addr` | Show IP addresses |
| `ip link` | Show interfaces |
| `ip route` | Show routing table |
| `ip neigh` | Show ARP/Neighbor table |
| `ip -s link` | Show interface statistics |
| `ip monitor` | Monitor network changes |
| `ip rule` | Show routing rules |
| `ip netns list` | List network namespaces |

---

# Hands-on Lab

## Task 1

Display interfaces.

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

Display routing table.

```bash
ip route
```

---

## Task 4

Display neighbor table.

```bash
ip neigh
```

---

## Task 5

Display interface statistics.

```bash
ip -s link
```

---

## Task 6

Create a temporary IP address.

```bash
sudo ip addr add 192.168.10.100/24 dev eth0
```

Verify:

```bash
ip addr
```

Remove it:

```bash
sudo ip addr del 192.168.10.100/24 dev eth0
```

---

## Task 7

Create a network namespace.

```bash
sudo ip netns add demo
```

Verify:

```bash
ip netns list
```

Delete it:

```bash
sudo ip netns del demo
```

---

## Task 8

Create a troubleshooting checklist using:

- `ip addr`
- `ip link`
- `ip route`
- `ip neigh`
- `ping`
- `traceroute`

---

# Common Troubleshooting Workflow

When a Linux server has no network connectivity:

Step 1

```bash
ip link
```

Interface up?

↓

Step 2

```bash
ip addr
```

IP assigned?

↓

Step 3

```bash
ip route
```

Default gateway exists?

↓

Step 4

```bash
ip neigh
```

Gateway reachable?

↓

Step 5

```bash
ping Gateway
```

↓

Step 6

```bash
ping 8.8.8.8
```

↓

Step 7

```bash
ping google.com
```

This systematic approach quickly identifies Layer 2, Layer 3, or Domain Name System (DNS) issues.

---

# Common Mistakes

❌ Forgetting `sudo` for configuration changes.

✅ Use elevated privileges when modifying network settings.

---

❌ Bringing down the wrong interface.

✅ Verify interface names before making changes.

---

❌ Adding duplicate IP addresses.

✅ Check existing configuration first.

---

❌ Removing the default route accidentally.

✅ Verify routing before deleting entries.

---

❌ Assuming `ip` changes are persistent.

✅ Use your distribution's network configuration tools to make permanent changes.

---

# Best Practices

- Use `ip` instead of legacy networking commands.
- Verify interface status before troubleshooting applications.
- Always check routing after IP configuration changes.
- Monitor interface statistics for packet drops and errors.
- Document production network changes.
- Use network namespaces for testing isolated network configurations.
- Avoid modifying production routes without a rollback plan.

---

# Interview Questions

## Beginner

1. What is the `ip` command?
2. How do you display IP addresses?
3. How do you display the routing table?
4. How do you bring an interface up?

---

## Intermediate

1. Explain the difference between `ip addr` and `ip link`.
2. How do you add a static route?
3. What is the Neighbor table?
4. What are Network Namespaces?

---

## Architect Level

1. Explain how you would troubleshoot a Linux server with no network connectivity using the `ip` command.
2. Design a Linux networking troubleshooting workflow.
3. Explain how the `ip` command is used in Kubernetes and cloud networking.

---

# Summary

In this lesson, you learned:

- The `ip` command
- Network Interfaces
- IP Address Management
- Routing Tables
- Neighbor Tables
- Interface Statistics
- VLAN Configuration
- Network Namespaces
- Linux Network Troubleshooting

The `ip` command is the most important networking utility on modern Linux systems. It provides a unified interface for managing network interfaces, IP addresses, routing, neighbor discovery, VLANs, tunnels, and namespaces. Mastering this command is essential for troubleshooting Linux servers, cloud infrastructure, Kubernetes nodes, and enterprise networks.

---

## Key Takeaways

- `ip` is the **modern replacement** for `ifconfig`, `route`, and `arp`.
- Use **`ip addr`** to view and manage IP addresses.
- Use **`ip link`** to manage network interfaces.
- Use **`ip route`** to inspect and configure routing.
- Use **`ip neigh`** to view ARP and Neighbor Discovery information.
- Network namespaces provide isolated networking environments.
- The `ip` command is one of the first tools used for Linux network troubleshooting.

---

## What's Next?

**[ss](ss.md)**

In the next lesson, you'll learn about **`ss` (Socket Statistics)**.

You'll explore:

- What `ss` is
- Viewing TCP and UDP Connections
- Listening Ports
- Socket States
- Process Information
- Network Troubleshooting
- Performance Analysis

By the end of the lesson, you'll understand how to inspect sockets, active connections, listening services, and network activity using one of the fastest and most powerful networking diagnostic tools available on Linux.
