---
title: "Types of IPv6 Addresses"
description: "Learn IPv6 address types — Unicast, Multicast, Anycast, Global Unicast, Link-Local, Unique Local Addresses (ULA), loopback, and unspecified."
difficulty: beginner
estimated_time: "90 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 3 · IPv6"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - kubernetes-engineer
  - platform-engineer
tags:
  - networking
  - ipv6
  - unicast
  - multicast
  - anycast
  - rebash-networking-mastery
comments: false
status: ready
---

# Types of IPv6 Addresses — Understanding IPv6 Address Categories

> Unlike IPv4, where communication primarily relies on **Unicast**, **Broadcast**, and **Multicast**, IPv6 introduces a more efficient addressing model. IPv6 eliminates **Broadcast** completely and instead uses **Unicast**, **Multicast**, and **Anycast** addressing. In addition, IPv6 defines several special-purpose address types such as **Global Unicast**, **Link-Local**, **Unique Local**, and **Loopback** addresses. Understanding these address types is essential for Linux administration, cloud networking, Kubernetes, and enterprise network design.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 3: IPv6 → Lesson 3</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** IPv6</div>

<div markdown>**Lesson:** 3 of 7</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand IPv6 address types
- Differentiate Unicast, Multicast, and Anycast
- Identify Global Unicast addresses
- Understand Link-Local addresses
- Learn about Unique Local Addresses (ULA)
- Recognise special IPv6 addresses
- Apply IPv6 address types in enterprise and cloud environments

---

# Prerequisites

Complete:

- [Why IPv6](why-ipv6.md)
- [IPv6 Structure](ipv6-structure.md)

---

# Why Learn IPv6 Address Types?

Consider these scenarios:

- A web server communicating with a client
- A router discovering neighbouring devices
- Multiple devices receiving the same streaming traffic
- A Kubernetes service accessible from multiple nodes

Each uses a different IPv6 address type.

Understanding these address types is fundamental to IPv6 networking.

---

# IPv6 Address Categories

IPv6 defines three primary communication types:

```text
Unicast

Multicast

Anycast
```

Unlike IPv4:

```text
Broadcast

❌ Not Used
```

IPv6 completely eliminates broadcast traffic.

---

# IPv6 Address Hierarchy

```text
IPv6 Addresses

│

├── Unicast

├── Multicast

└── Anycast
```

Within Unicast, there are several important address types.

---

# Unicast Addresses

A **Unicast** address identifies:

```text
One Device
```

Communication:

```text
One Sender

↓

One Receiver
```

This is the most common IPv6 communication type.

---

# Global Unicast Address (GUA)

Global Unicast addresses are the IPv6 equivalent of public IPv4 addresses.

Characteristics:

- Globally unique
- Internet routable
- Assigned by Internet Service Providers (ISPs) or organisations
- Used for Internet communication

Prefix:

```text
2000::/3
```

Example:

```text
2001:db8:1000:1::10
```

---

# Where Global Unicast is Used

Examples:

- Websites
- Cloud Virtual Machines
- Public APIs
- Internet-facing Load Balancers
- Enterprise Networks

---

# Link-Local Address

Every IPv6-enabled interface automatically receives a **Link-Local Address**.

Characteristics:

- Automatically assigned
- Valid only on the local network segment
- Never routed
- Used for local communication

Prefix:

```text
fe80::/10
```

Example:

```text
fe80::21a:2bff:fe3c:4d5e
```

---

# Why Link-Local Addresses Matter

IPv6 routers use Link-Local addresses for:

- Neighbor Discovery
- Router Discovery
- Default Gateway Communication

Even if no Global Unicast address exists, devices can still communicate locally using Link-Local addresses.

---

# Unique Local Address (ULA)

A **Unique Local Address** is similar in purpose to IPv4 private addresses.

Characteristics:

- Internal networks only
- Not Internet routable
- Used inside organisations

Prefix:

```text
fc00::/7
```

Most implementations use:

```text
fd00::/8
```

Example:

```text
fd12:3456:789a::100
```

---

# ULA vs Private IPv4

| IPv4 | IPv6 |
|------|------|
| 10.0.0.0/8 | fd00::/8 |
| 172.16.0.0/12 | fd00::/8 |
| 192.168.0.0/16 | fd00::/8 |

Both are intended for internal communication.

---

# Loopback Address

IPv6 has one loopback address:

```text
::1
```

Equivalent IPv4 address:

```text
127.0.0.1
```

Used for:

- Local testing
- Application development
- TCP/IP stack verification

---

# Unspecified Address

IPv6 defines:

```text
::
```

Meaning:

```text
No Address Assigned
```

Equivalent IPv4 address:

```text
0.0.0.0
```

Used during initialisation before an interface receives an address.

---

# Multicast Address

A **Multicast** address identifies:

```text
A Group of Devices
```

Communication:

```text
One Sender

↓

Multiple Receivers
```

Prefix:

```text
ff00::/8
```

---

# Multicast Example

Router Advertisement:

```text
Router

↓

Multicast

↓

All IPv6 Hosts
```

Instead of sending separate packets to each host, a single multicast packet reaches every interested device.

---

# Common Multicast Addresses

| Address | Purpose |
|----------|----------|
| `ff02::1` | All Nodes |
| `ff02::2` | All Routers |
| `ff02::5` | OSPF Routers |
| `ff02::a` | EIGRP Routers |

These addresses support efficient network communication.

---

# Anycast Address

An **Anycast** address is assigned to:

```text
Multiple Devices
```

Communication:

```text
One Sender

↓

Nearest Receiver
```

The routing infrastructure delivers packets to the closest instance based on routing metrics.

---

# Anycast Example

Multiple Domain Name System (DNS) servers share the same Anycast address.

Client:

```text
User

↓

Nearest DNS Server
```

Benefits:

- Reduced latency
- High availability
- Load distribution

---

# Why IPv6 Removed Broadcast

IPv4:

```text
Broadcast

↓

Every Device Receives Packet
```

Problems:

- Network congestion
- Higher CPU usage
- Unnecessary traffic

IPv6 replaces broadcast with targeted multicast communication, improving efficiency.

---

# IPv4 vs IPv6 Address Types

| IPv4 | IPv6 |
|------|------|
| Unicast | Unicast |
| Broadcast | ❌ Not Used |
| Multicast | Multicast |
| — | Anycast |

---

# Enterprise Example

Company Network:

```text
Global Unicast

↓

Internet Access
```

```text
Link-Local

↓

Neighbor Discovery
```

```text
ULA

↓

Internal Services
```

Each address type serves a different purpose.

---

# Cloud Perspective

Cloud providers assign:

Global Unicast:

```text
Public VM
```

Link-Local:

```text
Internal Communication
```

ULA:

```text
Private Internal Networks
```

Modern cloud environments commonly use multiple IPv6 address types simultaneously.

---

# Kubernetes Perspective

Kubernetes environments use:

Global Unicast:

```text
External Services
```

Link-Local:

```text
Node Communication
```

Multicast is generally **not** used for Kubernetes Service discovery. Kubernetes relies on its own networking model (such as kube-proxy, eBPF implementations, or DNS-based service discovery).

---

# Linux Perspective

Display IPv6 addresses.

```bash
ip -6 addr
```

Example output:

```text
inet6 2001:db8::10

inet6 fe80::21a:2bff:fe3c:4d5e
```

Notice that interfaces often have:

- Global Unicast
- Link-Local

addresses simultaneously.

---

Display IPv6 routes.

```bash
ip -6 route
```

---

# Hands-on Lab

## Task 1

Display IPv6 addresses.

```bash
ip -6 addr
```

Identify:

- Global Unicast
- Link-Local

---

## Task 2

Ping IPv6 localhost.

```bash
ping -6 ::1
```

---

## Task 3

Identify the type of each address:

```text
2001:db8::15

fe80::1234

fd12:3456::1

ff02::1

::1

::
```

---

## Task 4

Create a comparison table for:

- Global Unicast
- Link-Local
- ULA
- Multicast
- Anycast

---

## Task 5

Research how your cloud provider assigns IPv6 addresses to virtual machines.

---

## Task 6

Draw a diagram showing:

- Client
- Router
- Server

Label which IPv6 address types are used during communication.

---

## Task 7

Research common IPv6 multicast addresses used by routing protocols.

---

## Task 8

Compare IPv4 and IPv6 addressing models, highlighting why IPv6 removed broadcast.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip -6 addr` | Display IPv6 addresses |
| `ip -6 route` | Display IPv6 routes |
| `ping -6 ::1` | Test loopback |
| `hostname` | Display hostname |

---

# Common Mistakes

❌ Assuming IPv6 has broadcast addresses.

✅ IPv6 uses multicast instead of broadcast.

---

❌ Confusing Link-Local with Global Unicast.

✅ Link-Local addresses are valid only on the local link.

---

❌ Treating ULA as Internet-routable.

✅ ULAs are intended for private internal networks.

---

❌ Forgetting that every interface has a Link-Local address.

✅ IPv6 automatically assigns one to every enabled interface.

---

❌ Assuming Anycast is a separate address format.

✅ Anycast uses standard unicast addresses assigned to multiple devices.

---

# Best Practices

- Use Global Unicast for Internet-reachable systems.
- Use ULA for private internal services.
- Never manually remove Link-Local addresses.
- Learn common multicast addresses.
- Use Anycast for highly available distributed services such as DNS where appropriate.
- Understand the purpose of each IPv6 address type before deployment.

---

# Interview Questions

## Beginner

1. What are the three primary IPv6 address types?
2. Does IPv6 use broadcast?
3. What is a Link-Local address?
4. What is the IPv6 loopback address?

---

## Intermediate

1. Compare Global Unicast and Unique Local addresses.
2. Why was broadcast removed in IPv6?
3. Explain the purpose of multicast.
4. How does Anycast improve availability?

---

## Architect Level

1. Design an enterprise IPv6 addressing scheme using Global Unicast Address (GUA) and ULA.
2. Explain how cloud providers use different IPv6 address types.
3. Describe how Link-Local addresses support Neighbor Discovery.

---

# Summary

In this lesson, you learned:

- IPv6 address categories
- Unicast
- Global Unicast
- Link-Local
- Unique Local Addresses
- Loopback
- Unspecified addresses
- Multicast
- Anycast

IPv6 introduces a cleaner and more efficient addressing model than IPv4. By eliminating broadcast and using specialised address types for different communication patterns, IPv6 improves scalability, routing efficiency, and network performance. Understanding these address types is essential before learning automatic address configuration and Neighbor Discovery.

---

## Key Takeaways

- IPv6 defines **Unicast**, **Multicast**, and **Anycast** communication.
- IPv6 **does not use broadcast**.
- Global Unicast addresses are Internet routable.
- Link-Local addresses are automatically assigned and used only on the local network.
- Unique Local Addresses (ULA) provide private internal addressing.
- `::1` is the IPv6 loopback address.
- `::` is the unspecified address.

---

## What's Next?

**[SLAAC](slaac.md)**

In the next lesson, you'll learn about **SLAAC (Stateless Address Autoconfiguration)**.

You'll explore:

- What SLAAC is
- How IPv6 devices automatically configure addresses
- Router Advertisements (RA)
- Interface Identifiers
- Duplicate Address Detection (DAD)
- SLAAC vs DHCPv6
- Enterprise and cloud deployment scenarios

By the end of the lesson, you'll understand how IPv6 devices automatically obtain addresses without manual configuration and how SLAAC simplifies network administration.
