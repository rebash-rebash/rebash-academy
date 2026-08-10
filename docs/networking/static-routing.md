---
title: "Static Routing"
description: "Learn static routing — next-hop and exit-interface routes, default routes, recursive and floating static routes, administrative distance, and Linux configuration."
difficulty: beginner
estimated_time: "90 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 5 · Routing"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - routing
  - static-routing
  - ip-route
  - rebash-networking-mastery
comments: false
status: ready
---

# Static Routing — Manually Defining Paths Between Networks

> **Static Routing** is a routing method where network administrators manually configure routes in a router or Linux system. Unlike dynamic routing protocols, static routes do not change automatically when the network topology changes. They are simple, predictable, secure, and ideal for small networks, branch offices, default routes, and specific routing requirements. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand when and how to use static routing.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 5: Routing → Lesson 2</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Routing</div>

<div markdown>**Lesson:** 2 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Static Routing
- Configure static routes
- Learn default static routes
- Understand next-hop routing
- Learn recursive routing
- Understand floating static routes
- Configure static routes in Linux
- Apply static routing in enterprise environments

---

# Prerequisites

Complete:

- [Routing Basics](routing-fundamentals.md)

---

# Why Learn Static Routing?

Imagine two office networks:

```text
Office A

192.168.10.0/24
```

↓

```text
Router A
```

↓

```text
Router B
```

↓

```text
Office B

192.168.20.0/24
```

Router A must know:

```text
How do I reach

192.168.20.0/24?
```

One solution is:

```text
Static Route
```

---

# What is Static Routing?

A **Static Route** is a manually configured route that tells a router how to reach a destination network.

Example:

```text
Destination

192.168.20.0/24

↓

Next Hop

192.168.1.2
```

The router always forwards traffic using this path.

---

# Static Routing Workflow

```text
Packet Arrives

↓

Routing Table Lookup

↓

Static Route Found

↓

Forward Packet

↓

Next Hop
```

---

# Example Network

```text
LAN A

↓

Router A

↓

Router B

↓

LAN B
```

Networks:

```text
LAN A

192.168.10.0/24
```

```text
LAN B

192.168.20.0/24
```

Router A requires a route to LAN B.

---

# Static Route Entry

Example:

| Destination | Next Hop |
|-------------|----------|
| 192.168.20.0/24 | 192.168.1.2 |

When packets are destined for:

```text
192.168.20.x
```

Router A forwards them to:

```text
192.168.1.2
```

---

# Direct vs Static Routes

Direct Route:

```text
Connected Interface

↓

Automatically Added
```

Static Route:

```text
Administrator

↓

Manually Configured
```

---

# Next-Hop Address

The **Next Hop** is the IP address of the next router in the path.

Example:

```text
Destination

10.1.1.0/24

↓

Next Hop

172.16.0.2
```

The router forwards the packet to `172.16.0.2`.

---

# Exit Interface

Some platforms allow a route to reference an interface instead of a next-hop address.

Example:

```text
Destination

192.168.30.0/24

↓

Exit Interface

eth1
```

The router sends packets out through `eth1`.

---

# Recursive Routing

Example:

```text
Destination

192.168.20.0/24

↓

Next Hop

192.168.1.2
```

Before forwarding, the router must determine:

```text
How do I reach

192.168.1.2?
```

This additional lookup is called **Recursive Routing**.

---

# Default Static Route

Instead of configuring many individual routes:

```text
192.168.x.x

10.x.x.x

172.x.x.x
```

Use one default route:

```text
0.0.0.0/0
```

Everything not matched elsewhere follows the default route.

---

# IPv6 Static Route

IPv6 uses the same concept.

Default Route:

```text
::/0
```

Example:

```text
Destination

2001:db8:20::/64

↓

Next Hop

2001:db8:1::2
```

---

# Floating Static Route

A **Floating Static Route** acts as a backup route.

Example:

Primary Route:

```text
Dynamic Routing

Administrative Distance

110
```

Backup Static Route:

```text
Administrative Distance

200
```

The backup route is used only if the primary route becomes unavailable.

---

# Administrative Distance

Administrative Distance (AD) measures the trustworthiness of a route source.

Common examples:

| Route Type | Administrative Distance |
|-------------|------------------------:|
| Connected | 0 |
| Static | 1 |
| OSPF | 110 |
| RIP | 120 |

Lower values are preferred.

> Note: Default administrative distances may vary slightly between vendors.

---

# Advantages of Static Routing

- Simple
- Predictable
- Low CPU Usage
- No Routing Protocol Traffic
- Better Security
- Full Administrative Control

---

# Disadvantages of Static Routing

- Manual Configuration
- Difficult to Scale
- No Automatic Failover
- High Maintenance
- Not Suitable for Large Networks

---

# Enterprise Example

Branch Office:

```text
Small Office

↓

Router

↓

Head Office
```

Only one path exists.

A static default route is sufficient.

---

# Cloud Perspective

Cloud platforms commonly use static routes inside:

- Virtual Private Cloud (VPC) Route Tables
- Virtual Networks
- Transit Gateways
- Virtual Private Network (VPN) Connections
- Hybrid Cloud Networks

Administrators define routes manually to control traffic flow.

---

# Kubernetes Perspective

Kubernetes nodes automatically receive routes from the Container Network Interface (CNI).

However, static routes may still be used for:

- Hybrid Clusters
- External Storage Networks
- On-Premises Connectivity
- Specialised Network Integrations

---

# Linux Perspective

Display routing table.

```bash
ip route
```

Add a static route.

```bash
sudo ip route add 192.168.20.0/24 via 192.168.1.2
```

Add a default route.

```bash
sudo ip route add default via 192.168.1.1
```

Delete a route.

```bash
sudo ip route del 192.168.20.0/24
```

Display IPv6 routes.

```bash
ip -6 route
```

Add an IPv6 static route.

```bash
sudo ip -6 route add 2001:db8:20::/64 via 2001:db8:1::2
```

---

# Static Routing Workflow

```text
Packet Arrives

↓

Read Destination IP

↓

Lookup Static Route

↓

Forward to Next Hop

↓

Destination Network
```

---

# Static Routing Example

```text
Client

↓

Router A

↓

Router B

↓

Server
```

Router A:

```text
192.168.20.0/24

↓

192.168.1.2
```

Router B:

```text
192.168.10.0/24

↓

192.168.1.1
```

Communication succeeds in both directions.

---

# Hands-on Lab

## Task 1

Display your routing table.

```bash
ip route
```

---

## Task 2

Add a static route.

```bash
sudo ip route add 192.168.20.0/24 via 192.168.1.2
```

---

## Task 3

Verify the route.

```bash
ip route
```

---

## Task 4

Delete the route.

```bash
sudo ip route del 192.168.20.0/24
```

---

## Task 5

Display IPv6 routes.

```bash
ip -6 route
```

---

## Task 6

Add an IPv6 static route.

```bash
sudo ip -6 route add 2001:db8:20::/64 via 2001:db8:1::2
```

---

## Task 7

Draw a network containing:

- Two Routers
- Two LANs

Show how static routes enable communication.

---

## Task 8

Compare:

- Connected Routes
- Static Routes
- Dynamic Routes

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip route` | Display IPv4 routing table |
| `ip route add` | Add static route |
| `ip route del` | Delete static route |
| `ip -6 route` | Display IPv6 routing table |
| `ip -6 route add` | Add IPv6 static route |

---

# Common Mistakes

❌ Forgetting the return route.

✅ Configure routes in both directions when required.

---

❌ Incorrect next-hop address.

✅ Verify the next hop is reachable.

---

❌ Using static routes in large dynamic networks.

✅ Prefer dynamic routing protocols for scalability.

---

❌ Forgetting the default route.

✅ Configure a default route for Internet access.

---

❌ Ignoring route verification.

✅ Always verify routing tables after configuration.

---

# Best Practices

- Use static routes for small, stable networks.
- Use default routes for Internet-bound traffic.
- Document all static routes.
- Use floating static routes for backup paths.
- Verify route reachability after deployment.
- Prefer dynamic routing for large enterprise environments.

---

# Interview Questions

## Beginner

1. What is a static route?
2. What is a next-hop address?
3. What is a default route?
4. What is the difference between a connected route and a static route?

---

## Intermediate

1. Explain recursive routing.
2. What is a floating static route?
3. What is Administrative Distance?
4. When should static routing be used?

---

## Architect Level

1. Design a branch office network using static routing.
2. When would you choose static routing instead of dynamic routing?
3. How would you implement backup routing using floating static routes?

---

# Summary

In this lesson, you learned:

- Static Routing
- Next-Hop Routing
- Exit Interfaces
- Recursive Routing
- Default Routes
- Floating Static Routes
- Administrative Distance
- Linux Static Route Configuration
- Enterprise Static Routing

Static routing provides a simple, reliable, and predictable method of forwarding packets between networks. While it requires manual configuration and maintenance, it is highly effective for small, stable environments, default routes, and backup routing scenarios.

---

## Key Takeaways

- Static routes are **manually configured**.
- Static routing is simple, secure, and predictable.
- A **next-hop address** tells the router where to forward packets.
- The default IPv4 route is **0.0.0.0/0**.
- The default IPv6 route is **::/0**.
- Floating static routes provide backup connectivity.
- Static routing is ideal for small or stable network environments.

---

## What's Next?

**[Dynamic Routing](dynamic-routing.md)**

In the next lesson, you'll learn about **Dynamic Routing**.

You'll explore:

- What dynamic routing is
- Why dynamic routing is needed
- Routing protocols
- Route exchange
- Convergence
- Metrics
- Enterprise routing design

By the end of the lesson, you'll understand how routers automatically learn, update, and optimise routes across large enterprise and cloud networks.
