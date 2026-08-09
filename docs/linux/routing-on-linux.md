---
title: "Routing — How Linux Sends Network Traffic"
description: "Learn Linux routing — routing tables, default gateways, static routes, ip route lookup, IP forwarding, and troubleshooting connectivity across networks."
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
  - routing
  - gateway
  - ip-route
  - rebash-linux-mastery
comments: false
status: ready
---

# Routing — How Linux Sends Network Traffic

> **Routing** is the process of determining the best path for network packets to travel from a source to a destination. Every Linux server, cloud instance, Kubernetes node, and network device relies on routing tables to decide where packets should be sent. Understanding routing is essential for Linux administrators, DevOps engineers, Cloud Architects, Network Engineers, and Site Reliability Engineers (SREs).

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 8: Networking → Lesson 4</p>

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

<div markdown>**Lesson:** 4 of 13</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand routing
- Learn how routing tables work
- Understand default gateways
- Configure static routes
- View routing information
- Troubleshoot routing issues
- Apply routing concepts in production

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
- Module 8 Lessons 1–3

---

# Why Learn Routing?

Imagine:

- A Linux server cannot reach another network.
- A Kubernetes node cannot communicate with another node.
- SSH works locally but fails across subnets.
- A cloud VM has Internet access but cannot reach a private network.

In many cases, the cause is an incorrect routing configuration.

---

# What is Routing?

Routing is the process of forwarding network packets from one network to another.

A router or a Linux system examines the destination IP address and determines the next hop based on its routing table.

---

# How Routing Works

```text
Application
      │
      ▼
Destination IP
      │
      ▼
Routing Table Lookup
      │
      ▼
Next Hop Selected
      │
      ▼
Packet Sent
```

---

# What is a Routing Table?

A routing table is a list of routes that tells the operating system how to reach different networks.

Each route typically contains:

- Destination network
- Gateway (next hop)
- Network interface
- Metric (priority)

---

# View the Routing Table

Display all routes.

```bash
ip route
```

Example:

```text
default via 192.168.1.1 dev ens160

192.168.1.0/24 dev ens160 proto kernel
```

---

# Understanding a Route

Example:

```text
192.168.10.0/24 via 192.168.1.1 dev ens160
```

Meaning:

- Destination network:

```text
192.168.10.0/24
```

- Next hop:

```text
192.168.1.1
```

- Interface:

```text
ens160
```

---

# Default Route

The default route is used when no more specific route matches the destination.

Example:

```text
default via 192.168.1.1
```

Without a default route, a system typically cannot communicate with external networks such as the Internet.

---

# Routing Decision Process

Linux searches the routing table using the **longest prefix match**.

Example:

```text
Destination

↓

192.168.1.50

↓

Matches

192.168.1.0/24

↓

Forward Packet
```

The most specific matching route is selected.

---

# Add a Temporary Route

Add a route to another network.

```bash
sudo ip route add 10.10.0.0/16 via 192.168.1.1
```

Verify:

```bash
ip route
```

> This route is temporary and will not survive a reboot.

---

# Delete a Route

```bash
sudo ip route del 10.10.0.0/16
```

---

# Replace the Default Route

```bash
sudo ip route replace default via 192.168.1.254
```

---

# Persistent Routes

Routes added with the `ip` command are temporary.

Persistent routes are configured using the operating system's networking tools.

Examples:

- Ubuntu: Netplan
- RHEL / Rocky / AlmaLinux: NetworkManager (`nmcli`) or network configuration files

---

# Route Lookup

Check which route Linux will use.

```bash
ip route get 8.8.8.8
```

Example:

```text
8.8.8.8 via 192.168.1.1 dev ens160
```

This command is extremely useful when troubleshooting routing decisions.

---

# Enable IP Forwarding

Linux can act as a router by forwarding packets.

Temporarily enable IP forwarding.

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Verify:

```bash
sysctl net.ipv4.ip_forward
```

For permanent configuration, update the appropriate `sysctl` configuration file.

---

# Common Commands

Display routing table.

```bash
ip route
```

View a specific route.

```bash
ip route get 8.8.8.8
```

Add route.

```bash
sudo ip route add 10.10.0.0/16 via 192.168.1.1
```

Delete route.

```bash
sudo ip route del 10.10.0.0/16
```

Enable IP forwarding.

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

---

# Real Production Examples

Verify default gateway.

```bash
ip route
```

Check Internet route.

```bash
ip route get 8.8.8.8
```

Add a route to a private subnet.

```bash
sudo ip route add 172.16.0.0/16 via 192.168.1.1
```

Enable packet forwarding on a gateway server.

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

---

# Production Perspective

Routing is essential for:

- Cloud virtual machines
- Kubernetes clusters
- VPN gateways
- Firewalls
- Load balancers
- Multi-subnet environments
- Hybrid cloud networks
- Enterprise data centers

Incorrect routing is one of the most common causes of network connectivity problems.

---

# Hands-on Lab

## Task 1

Display the routing table.

```bash
ip route
```

---

## Task 2

Identify the default route.

```bash
ip route
```

---

## Task 3

Determine the route to Google's DNS server.

```bash
ip route get 8.8.8.8
```

---

## Task 4

Add a temporary static route.

```bash
sudo ip route add 10.10.0.0/16 via 192.168.1.1
```

Replace the gateway with one appropriate for your network.

---

## Task 5

Verify the new route.

```bash
ip route
```

---

## Task 6

Delete the temporary route.

```bash
sudo ip route del 10.10.0.0/16
```

---

## Task 7

Check whether IP forwarding is enabled.

```bash
sysctl net.ipv4.ip_forward
```

---

## Task 8

Enable IP forwarding temporarily.

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `ip route` | Display routing table | Verify routes |
| `ip route get` | Show route to a destination | Troubleshooting |
| `ip route add` | Add static route | Multi-network connectivity |
| `ip route del` | Delete route | Cleanup |
| `ip route replace` | Replace default route | Gateway updates |
| `sysctl net.ipv4.ip_forward` | Check IP forwarding | Router verification |

---

# Static vs Dynamic Routing

| Feature | Static Routing | Dynamic Routing |
|----------|----------------|-----------------|
| Configuration | Manual | Automatic |
| Scalability | Small networks | Large networks |
| Maintenance | Higher | Lower |
| Complexity | Simple | More complex |
| Common Use | Small LANs, cloud VMs | Enterprise networks |

Dynamic routing commonly uses protocols such as:

- OSPF
- BGP
- RIP
- EIGRP (Cisco)

Linux servers typically use static routes unless participating in a routing infrastructure.

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A Linux application server cannot communicate with a database located in another subnet.

Investigation:

Check the routing table.

```bash
ip route
```

Verify the route.

```bash
ip route get 10.20.30.40
```

Output:

```text
Network unreachable
```

Add the required route.

```bash
sudo ip route add 10.20.30.0/24 via 192.168.1.1
```

Verify:

```bash
ip route get 10.20.30.40
```

The route now exists, and the application can communicate with the database.

A permanent route is then configured using the operating system's network management tools.

---

# Best Practices

- Use the `ip` command instead of the deprecated `route` command.
- Verify the routing table before troubleshooting applications.
- Configure persistent routes through supported network management tools.
- Use static routes only when necessary.
- Document custom routes in production environments.
- Verify routing after network configuration changes.

---

# Common Mistakes

❌ Forgetting that routes added with `ip route add` are temporary.

✅ Remember to that routes added with `ip route add` are temporary.

---

❌ Configuring an incorrect default gateway.

✅ Avoid this mistake: configuring an incorrect default gateway.

---

❌ Adding overlapping or conflicting routes.

✅ Avoid this mistake: adding overlapping or conflicting routes.

---

❌ Ignoring routing when troubleshooting connectivity issues.

✅ Always review routing when troubleshooting connectivity issues.

---

# Interview Questions
## Beginner

1. What is routing?
2. What is a routing table?
3. What is the purpose of a default gateway?
4. Which command displays the routing table?

---

## Intermediate

1. What is the difference between a static route and a dynamic route?
2. How do you add a temporary route?
3. What does `ip route get` do?
4. What is IP forwarding?

---

## Architect Level

1. How would you design routing for a multi-subnet cloud environment?
2. How would you troubleshoot communication between Kubernetes worker nodes?
3. Why is the longest prefix match important in routing decisions?

---

# Summary

In this lesson, you learned:

- Routing fundamentals
- Routing tables
- Default gateways
- Static routes
- Route lookup
- IP forwarding
- Route troubleshooting
- Production networking best practices

Routing determines how Linux systems send packets across networks. A solid understanding of routing tables, gateways, and static routes enables administrators to build reliable, scalable, and well-connected infrastructure.

---

## Key Takeaways

- Routing determines the path packets take to reach their destination.
- The routing table contains information about reachable networks.
- The default gateway handles traffic for unknown networks.
- Use `ip route` to view and manage routes.
- Use `ip route get` to understand routing decisions.
- Routes added with the `ip` command are temporary unless configured persistently.

---

## What's Next?

**[ping — Testing Network Connectivity in Linux](ping.md)**

You'll explore:

- How ICMP works
- Testing network connectivity
- Measuring latency
- Understanding packet loss
- Common `ping` options
- Troubleshooting network issues
- Production best practices

The `ping` command is one of the most widely used tools for verifying network connectivity and diagnosing communication problems.
