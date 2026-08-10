---
title: "SLAAC"
description: "Learn Stateless Address Autoconfiguration (SLAAC) — Router Advertisements, Interface Identifiers, Duplicate Address Detection, and SLAAC vs DHCPv6."
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
  - slaac
  - dhcpv6
  - rebash-networking-mastery
comments: false
status: ready
---

# SLAAC (Stateless Address Autoconfiguration) — Automatic IPv6 Address Configuration

> One of the most powerful features of **IPv6** is its ability to automatically configure network addresses without requiring manual configuration or a Dynamic Host Configuration Protocol (DHCP) server. This capability is known as **SLAAC (Stateless Address Autoconfiguration)**. Using SLAAC, an IPv6-enabled device can generate its own IPv6 address, discover the default gateway, and begin communicating on the network automatically. SLAAC greatly simplifies network administration and is widely used in enterprise networks, cloud environments, and modern operating systems.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 3: IPv6 → Lesson 4</p>

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

<div markdown>**Lesson:** 4 of 7</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand what SLAAC is
- Explain how IPv6 devices configure themselves
- Understand Router Advertisements (RA)
- Learn Interface Identifiers
- Understand Duplicate Address Detection (DAD)
- Compare SLAAC and DHCPv6
- Configure and verify SLAAC on Linux

---

# Prerequisites

Complete:

- [Why IPv6](why-ipv6.md)
- [IPv6 Structure](ipv6-structure.md)
- [Types of IPv6 Addresses](ipv6-address-types.md)

---

# Why Learn SLAAC?

Imagine connecting your laptop to a network.

With IPv4:

```text
Connect

↓

DHCP Request

↓

DHCP Server

↓

IP Address Assigned
```

With IPv6:

```text
Connect

↓

Router Advertisement

↓

Generate IPv6 Address

↓

Ready
```

No DHCP server is required for basic address configuration.

---

# What is SLAAC?

**Stateless Address Autoconfiguration (SLAAC)** is an IPv6 mechanism that allows devices to automatically generate their own IPv6 addresses using information received from routers.

The device does not need:

- Manual configuration
- A DHCP server (for basic addressing)
- Static IP assignment

---

# Why is it Called "Stateless"?

The router does **not** keep a database of assigned IPv6 addresses.

Instead:

```text
Router

↓

Advertises Network Prefix

↓

Device Generates Address
```

Each device configures itself independently.

---

# SLAAC Process

```text
Device Connects

↓

Creates Link-Local Address

↓

Performs Duplicate Address Detection

↓

Receives Router Advertisement

↓

Learns Network Prefix

↓

Generates Global IPv6 Address

↓

Network Ready
```

---

# Step 1 — Link-Local Address

Every IPv6 device first creates a Link-Local address.

Example:

```text
fe80::1234:5678:abcd:1
```

This address allows communication with nearby devices before a Global Unicast address is assigned.

---

# Step 2 — Duplicate Address Detection (DAD)

Before using an address, the device verifies that no other device is already using it.

Process:

```text
Generate Address

↓

Check Network

↓

Address Already Exists?

↓

No

↓

Use Address
```

If another device is already using the address, a different Interface Identifier is generated.

---

# Step 3 — Router Advertisement (RA)

IPv6 routers periodically send:

```text
Router Advertisements
```

These messages contain:

- Network Prefix
- Prefix Length
- Default Gateway Information
- Network Configuration Flags
- Additional Parameters

---

# Example Router Advertisement

Router sends:

```text
Prefix

2001:db8:1000:1::/64
```

The device now knows the network prefix.

---

# Step 4 — Interface Identifier

The device creates the second half of the IPv6 address.

Example:

Router Prefix:

```text
2001:db8:1000:1::/64
```

Interface Identifier:

```text
021a:2bff:fe3c:4d5e
```

Final Address:

```text
2001:db8:1000:1:21a:2bff:fe3c:4d5e
```

---

# Modern Interface Identifier Generation

Originally, many operating systems generated the Interface Identifier using the network interface's Media Access Control (MAC) address (modified EUI-64 format).

Today, most modern operating systems prefer:

- Randomized interface identifiers
- Temporary privacy addresses (RFC 4941 and related standards)
- Stable but non-MAC-derived addresses

This improves user privacy and reduces device tracking.

---

# Duplicate Address Detection (DAD)

Before using the new IPv6 address:

```text
Send Neighbor Solicitation

↓

Any Reply?

↓

No

↓

Address Valid
```

If another device responds, the address cannot be used.

---

# Default Gateway

The Router Advertisement also provides:

```text
Default Gateway
```

Unlike IPv4, the gateway information comes from the router advertisement rather than being manually configured or necessarily delivered by DHCP.

---

# SLAAC Without DHCP

Using SLAAC alone, devices receive:

- Global IPv6 Address
- Link-Local Address
- Default Gateway
- Prefix Information

However, some information may still require DHCPv6 depending on network configuration.

---

# SLAAC vs DHCPv6

| SLAAC | DHCPv6 |
|--------|---------|
| Self-configured | Server assigns information |
| No address database | Server tracks leases |
| Uses Router Advertisements | Uses DHCPv6 messages |
| Simple deployment | Centralised management |

---

# SLAAC + DHCPv6

Many enterprise networks use both:

```text
Router Advertisement

↓

IPv6 Address
```

```text
DHCPv6

↓

DNS Servers

↓

Domain Name

↓

Other Configuration
```

This provides automatic addressing with centralised management of additional settings.

---

# Benefits of SLAAC

- Automatic configuration
- No manual IP assignment
- Reduced administration
- Fast deployment
- Simplified large-scale networking
- Built into IPv6

---

# Enterprise Example

Employee Laptop:

```text
Connect to Network

↓

Receive Router Advertisement

↓

Generate IPv6 Address

↓

Ready for Use
```

No administrator needs to manually assign an address.

---

# Cloud Perspective

Many cloud providers support:

- SLAAC
- DHCPv6
- Static IPv6 Assignment

The available options depend on the cloud provider and network configuration.

---

# Kubernetes Perspective

Kubernetes clusters can operate on IPv6 or Dual Stack networks.

While Kubernetes networking itself typically relies on the Container Network Interface (CNI) plugin, the underlying Linux nodes may use SLAAC to obtain their IPv6 addresses depending on the network environment.

---

# Linux Perspective

Display IPv6 addresses.

```bash
ip -6 addr
```

Display IPv6 routes.

```bash
ip -6 route
```

Display router information (if supported).

```bash
ip -6 route show default
```

---

# Example Output

```text
inet6

2001:db8:1000:1::15/64
```

Link-Local:

```text
fe80::21a:2bff:fe3c:4d5e
```

---

# SLAAC Workflow

```text
System Boots

↓

Create Link-Local Address

↓

Duplicate Address Detection

↓

Receive Router Advertisement

↓

Generate Global Address

↓

Configure Default Gateway

↓

Ready
```

---

# Hands-on Lab

## Task 1

Display IPv6 addresses.

```bash
ip -6 addr
```

Identify:

- Link-Local Address
- Global Address (if available)

---

## Task 2

Display IPv6 routes.

```bash
ip -6 route
```

Locate the default route.

---

## Task 3

Determine whether your system obtained its IPv6 address automatically or through static configuration.

---

## Task 4

Research how your Linux distribution enables or disables SLAAC.

---

## Task 5

Draw the complete SLAAC process from system startup to successful IPv6 configuration.

---

## Task 6

Create a comparison table for:

- SLAAC
- DHCPv6
- Static IPv6 Configuration

---

## Task 7

Research how your preferred cloud provider supports IPv6 automatic address configuration.

---

## Task 8

Explain why Duplicate Address Detection is necessary and describe what happens if a duplicate address is detected.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip -6 addr` | Display IPv6 addresses |
| `ip -6 route` | Display IPv6 routes |
| `ping -6` | Test IPv6 connectivity |
| `hostname` | Display hostname |

---

# Common Mistakes

❌ Assuming SLAAC requires DHCP.

✅ SLAAC can assign IPv6 addresses without DHCP.

---

❌ Believing routers assign addresses directly.

✅ Routers advertise the prefix; hosts generate their own addresses.

---

❌ Ignoring Duplicate Address Detection.

✅ DAD prevents IPv6 address conflicts.

---

❌ Assuming SLAAC always provides DNS information.

✅ Additional configuration may come from DHCPv6 or Router Advertisements, depending on the network.

---

❌ Thinking SLAAC replaces every DHCP feature.

✅ DHCPv6 may still provide centralised configuration options.

---

# Best Practices

- Use SLAAC for automatic IPv6 deployment where appropriate.
- Enable Duplicate Address Detection.
- Combine SLAAC with DHCPv6 when centralised management is needed.
- Monitor Router Advertisements.
- Use privacy extensions on client devices when appropriate.
- Document IPv6 addressing policies.

---

# Interview Questions

## Beginner

1. What is SLAAC?
2. What does "Stateless" mean?
3. What information does a Router Advertisement provide?
4. Why is Duplicate Address Detection required?

---

## Intermediate

1. Explain the complete SLAAC process.
2. Compare SLAAC and DHCPv6.
3. Why does every IPv6 device first create a Link-Local address?
4. What is the purpose of the Interface Identifier?

---

## Architect Level

1. When would you choose SLAAC instead of DHCPv6?
2. How would you deploy IPv6 automatic addressing in a large enterprise?
3. Explain how SLAAC supports scalable cloud and enterprise networking.

---

# Summary

In this lesson, you learned:

- What SLAAC is
- Stateless IPv6 address configuration
- Router Advertisements
- Link-Local addresses
- Interface Identifiers
- Duplicate Address Detection
- SLAAC vs DHCPv6
- Linux IPv6 configuration

SLAAC is one of IPv6's most powerful features. It enables devices to automatically configure their own IPv6 addresses using information advertised by routers, reducing administrative effort while supporting scalable and efficient network deployments.

---

## Key Takeaways

- SLAAC automatically configures IPv6 addresses.
- Devices first generate a Link-Local address.
- Router Advertisements provide the network prefix and gateway information.
- Duplicate Address Detection helps prevent address conflicts.
- SLAAC can operate independently or alongside DHCPv6.
- Modern operating systems typically generate privacy-friendly Interface Identifiers instead of deriving them directly from MAC addresses.

---

## What's Next?

**[Neighbor Discovery](neighbor-discovery.md)**

In the next lesson, you'll learn about **Neighbor Discovery Protocol (NDP)**.

You'll explore:

- What Neighbor Discovery is
- Neighbor Solicitation (NS)
- Neighbor Advertisement (NA)
- Router Solicitation (RS)
- Router Advertisement (RA)
- Address Resolution in IPv6
- NDP vs ARP

By the end of the lesson, you'll understand how IPv6 devices discover neighbours, resolve addresses, locate routers, and communicate efficiently without using Address Resolution Protocol (ARP).
