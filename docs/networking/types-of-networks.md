---
title: "Types of Networks (LAN, WAN, MAN, PAN)"
description: "Learn how networks are classified by coverage — PAN, LAN, MAN, and WAN — with enterprise examples for Linux, Cloud, DevOps, and Kubernetes engineers."
difficulty: beginner
estimated_time: "75 min"
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
  - lan
  - wan
  - man
  - pan
  - fundamentals
  - rebash-networking-mastery
comments: false
status: ready
---

# Types of Networks (LAN, WAN, MAN, PAN) — Understanding Network Classifications

> Networks are classified based on their **geographical coverage**, **ownership**, and **purpose**. Understanding different network types helps you design, troubleshoot, and manage enterprise infrastructures efficiently. From connecting devices inside a room to linking data centres across continents, each network type serves a unique purpose. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand these fundamental networking concepts.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 1: Networking Fundamentals → Lesson 2</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 75 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Networking Fundamentals</div>

<div markdown>**Lesson:** 2 of 10</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand different network types
- Explain LAN, WAN, MAN, and PAN
- Compare network characteristics
- Identify real-world use cases
- Understand enterprise networking architectures
- Choose appropriate network types for different scenarios

---

# Prerequisites

Complete:

- [Lesson 1: What is Networking?](introduction-to-networking.md)

---

# Why Learn Network Types?

Every organisation uses multiple network types.

For example:

```text
Bluetooth Mouse

↓

Laptop

↓

Office LAN

↓

Corporate WAN

↓

Cloud Data Center
```

Understanding how these networks connect helps you troubleshoot and design reliable infrastructure.

---

# Network Classification

Networks are commonly classified by their coverage area.

```text
PAN

↓

LAN

↓

MAN

↓

WAN
```

As coverage increases, the network typically becomes larger, more complex, and more expensive to operate.

---

# Overview of Network Types

| Network | Full Form | Coverage |
|----------|-----------|----------|
| PAN | Personal Area Network | A few metres |
| LAN | Local Area Network | Building or office |
| MAN | Metropolitan Area Network | City |
| WAN | Wide Area Network | Country or worldwide |

---

# Personal Area Network (PAN)

A **Personal Area Network (PAN)** connects devices belonging to a single person within a short distance.

Typical range:

- 1–10 metres

Examples:

- Smartphone ↔ Smartwatch
- Laptop ↔ Wireless Mouse
- Laptop ↔ Bluetooth Keyboard
- Mobile ↔ Wireless Earbuds

---

# PAN Architecture

```text
          Bluetooth

Smartphone

      │

Laptop ───── Smartwatch

      │

Wireless Headset
```

Most PANs use wireless technologies.

---

# PAN Technologies

Common technologies include:

- Bluetooth
- Near Field Communication (NFC)
- Infrared
- Universal Serial Bus (USB)

---

# Advantages of PAN

- Easy to configure
- Low power consumption
- Low cost
- Portable
- Ideal for personal devices

---

# Limitations of PAN

- Very short range
- Limited bandwidth
- Small number of devices
- Not suitable for enterprise communication

---

# Local Area Network (LAN)

A **Local Area Network (LAN)** connects devices within a limited geographical area such as:

- Home
- Office
- School
- University
- Laboratory
- Data Centre

Typical range:

- A single room
- One building
- Multiple nearby buildings

---

# LAN Architecture

```text
          Internet

              │

           Router

              │

          +--------+
          | Switch |
          +--------+

      │      │      │

   Laptop  Server  Printer
```

Most enterprise offices operate one or more LANs.

---

# LAN Technologies

Common technologies:

- Ethernet
- Wi-Fi
- Fibre Ethernet

Typical speeds:

- 100 Mbps
- 1 Gbps
- 10 Gbps
- 40 Gbps
- 100 Gbps

---

# Advantages of LAN

- High speed
- Low latency
- Easy resource sharing
- Centralised management
- Low operational cost

---

# Limitations of LAN

- Limited geographic coverage
- Requires local infrastructure
- Internal network failures can affect many users

---

# Metropolitan Area Network (MAN)

A **Metropolitan Area Network (MAN)** connects multiple LANs across a city or metropolitan area.

Examples:

- University campuses
- Government offices
- Banking branches
- Hospital networks

Typical coverage:

- 5–50 kilometres

---

# MAN Architecture

```text
Office A

     │

Campus Fiber Network

     │

Office B

     │

Office C
```

MANs commonly use high-speed fibre optic networks.

---

# Advantages of MAN

- Connects multiple LANs
- High-speed connectivity
- Suitable for city-wide organisations
- Centralised management

---

# Limitations of MAN

- Higher deployment cost
- More complex management
- Requires dedicated infrastructure

---

# Wide Area Network (WAN)

A **Wide Area Network (WAN)** connects LANs and MANs across countries or the entire world.

Examples:

- The Internet
- Global enterprise networks
- Cloud provider networks
- Banking networks

Coverage:

- National
- International
- Global

---

# WAN Architecture

```text
Office A

      │

Internet/MPLS/VPN

      │

Office B

      │

Cloud Data Center
```

WANs rely on service providers and long-distance communication technologies.

---

# WAN Technologies

Examples:

- Multiprotocol Label Switching (MPLS)
- Virtual Private Network (VPN)
- Internet
- Leased Lines
- Software-Defined Wide Area Network (SD-WAN)
- Satellite
- Fibre Optics

---

# Advantages of WAN

- Global connectivity
- Supports remote offices
- Cloud integration
- Business continuity
- Remote work

---

# Limitations of WAN

- Higher latency
- Higher cost
- More complex troubleshooting
- Depends on service providers

---

# Enterprise Example

Imagine a multinational company.

```text
London Office

      │

Corporate WAN

      │

Singapore Office

      │

New York Office

      │

Cloud Infrastructure
```

Each office has its own LAN, while all offices communicate through the WAN.

---

# Comparison

| Feature | PAN | LAN | MAN | WAN |
|----------|-----|-----|-----|-----|
| Coverage | Personal | Building | City | Global |
| Speed | Medium | High | High | Varies |
| Cost | Low | Low | Medium | High |
| Ownership | Individual | Organisation | Organisation/ISP | ISP/Enterprise |
| Example | Bluetooth | Office Network | University Network | Internet |

---

# Real-World Examples

## PAN

- Smartwatch connected to a phone
- Bluetooth headphones
- Wireless keyboard

---

## LAN

- Office network
- School computer lab
- Home Wi-Fi network

---

## MAN

- City-wide university network
- Municipal government offices
- Hospital campuses

---

## WAN

- Internet
- AWS Global Network
- Google Cloud Network
- Enterprise MPLS network

---

# Production Perspective

Enterprise organisations commonly use all four network types together.

Example:

```text
Bluetooth Mouse

↓

Laptop (PAN)

↓

Office Switch (LAN)

↓

City Data Center (MAN)

↓

Cloud Platform (WAN)
```

Modern enterprises build layered network architectures using multiple network types.

---

# Networking in Cloud Computing

Cloud providers rely heavily on WAN technologies.

Examples:

- Global backbone networks
- Multi-region connectivity
- Dedicated fibre links
- Private WANs

Your cloud Virtual Private Cloud (VPC) is typically connected through WAN infrastructure.

---

# Networking in Kubernetes

Kubernetes clusters often span:

- Multiple LANs
- Multiple Availability Zones
- Multiple Regions

Communication may traverse LANs and WANs depending on deployment architecture.

---

# Hands-on Lab

## Task 1

Identify all PAN devices you use daily.

---

## Task 2

Draw your home LAN.

Include:

- Router
- Laptop
- Smartphone
- Printer

---

## Task 3

Identify the WAN connection used by your Internet provider.

---

## Task 4

Research how your university or workplace connects multiple buildings.

Determine whether it uses a MAN.

---

## Task 5

Display your network interfaces.

```bash
ip addr
```

---

## Task 6

Display your default gateway.

```bash
ip route
```

---

## Task 7

Test Internet connectivity.

```bash
ping google.com
```

---

## Task 8

Create a network diagram showing:

- PAN
- LAN
- MAN
- WAN

and explain how they interact in a modern enterprise.

---

# Command Deep Dive

| Command | Purpose | Example |
|----------|----------|---------|
| `ip addr` | Display network interfaces | View assigned IP addresses |
| `ip route` | Display routing table | Identify default gateway |
| `ping` | Test connectivity | Verify Internet access |
| `hostnamectl` | Display system information | Confirm hostname |
| `ss -tuln` | Display listening ports | Verify network services |
| `curl` | Test web connectivity | Verify HTTP communication |

---

# Common Mistakes

❌ Confusing LAN with WAN.

✅ Remember LAN is local; WAN connects distant networks.

---

❌ Assuming Wi-Fi means Internet.

✅ Wi-Fi provides LAN connectivity; Internet access depends on a WAN connection.

---

❌ Thinking PAN is only Bluetooth.

✅ PAN includes USB, NFC, and Infrared connections.

---

❌ Believing the Internet is a LAN.

✅ The Internet is the world's largest WAN.

---

❌ Ignoring network scale.

✅ Always consider coverage when selecting a network type.

---

# Best Practices

- Use LANs for local communication.
- Use WANs to connect geographically separated locations.
- Keep PAN devices secure by disabling unused wireless connections.
- Document network architecture using diagrams.
- Design networks according to organisational requirements and future growth.

---

# Interview Questions

## Beginner

1. What is a LAN?
2. What is the difference between LAN and WAN?
3. What devices commonly form a PAN?
4. Give examples of a MAN.

---

## Intermediate

1. Why are LANs generally faster than WANs?
2. How does a multinational company connect branch offices?
3. What technologies are commonly used in WANs?
4. Explain when a MAN is preferred over a WAN.

---

## Architect Level

1. How would you design networking for an organisation with offices in multiple cities?
2. How do cloud providers use WAN infrastructure?
3. Explain how LAN, MAN, WAN, and PAN work together in a modern enterprise.

---

# Summary

In this lesson, you learned:

- Personal Area Networks (PAN)
- Local Area Networks (LAN)
- Metropolitan Area Networks (MAN)
- Wide Area Networks (WAN)
- Real-world applications
- Enterprise networking architectures
- Advantages and limitations of each network type

Understanding network classifications provides the foundation for designing scalable, secure, and efficient infrastructures. Modern organisations combine multiple network types to connect personal devices, offices, campuses, data centres, and cloud platforms into a unified enterprise network.

---

## Key Takeaways

- PAN connects personal devices over short distances.
- LAN connects devices within a building or local area.
- MAN connects multiple LANs across a city.
- WAN connects networks across countries and continents.
- Enterprise and cloud environments often use all four network types together.

---

## What's Next?

**[Network Topologies](network-topologies.md)**
