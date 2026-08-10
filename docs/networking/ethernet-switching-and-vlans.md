---
title: "Ethernet"
description: "Learn Ethernet fundamentals — frames, MAC addressing, EtherType, FCS, speeds, duplex modes, collision domains, and IEEE 802.3 standards."
difficulty: beginner
estimated_time: "90 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 4 · Switching"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - ethernet
  - switching
  - lan
  - mac-address
  - rebash-networking-mastery
comments: false
status: ready
---

# Ethernet — The Foundation of Modern Local Area Networks (LANs)

> **Ethernet** is the world's most widely used **Local Area Network (LAN)** technology. It defines how devices communicate over wired networks using standardised frame formats, Media Access Control (MAC) addresses, and transmission methods. Whether you're connecting Linux servers, enterprise switches, cloud infrastructure, Kubernetes worker nodes, or home computers, Ethernet is the technology that makes communication possible. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand how Ethernet works.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 4: Switching → Lesson 1</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Switching</div>

<div markdown>**Lesson:** 1 of 8</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Ethernet
- Learn how Ethernet communication works
- Understand Ethernet frames
- Identify Ethernet standards
- Learn Ethernet speeds
- Understand collision domains
- Understand duplex modes
- Apply Ethernet concepts in enterprise and cloud environments

---

# Prerequisites

Complete:

- Module 1: Networking Fundamentals
- Module 2: IPv4 Addressing
- Module 3: IPv6

---

# Why Learn Ethernet?

Imagine a Linux server communicating with another server.

The communication path is:

```text
Application

↓

TCP

↓

IP

↓

Ethernet

↓

Cable

↓

Switch

↓

Destination
```

Although IP identifies the destination, **Ethernet** is responsible for delivering frames across the local network.

---

# What is Ethernet?

Ethernet is a **Layer 2 (Data Link Layer)** technology that defines how devices communicate within a Local Area Network (LAN).

It specifies:

- Frame Format
- MAC Addressing
- Error Detection
- Media Access
- Physical Cabling Standards

Ethernet operates together with Layer 1 (Physical Layer).

---

# Ethernet in the OSI Model

```text
Layer 7

Application
```

↓

```text
Layer 6

Presentation
```

↓

```text
Layer 5

Session
```

↓

```text
Layer 4

Transport
```

↓

```text
Layer 3

Network (IP)
```

↓

```text
Layer 2

Ethernet
```

↓

```text
Layer 1

Physical Cable
```

---

# Ethernet Communication

Suppose:

Computer A wants to send data to Computer B.

Process:

```text
Create Data

↓

Add IP Header

↓

Add Ethernet Header

↓

Send Frame

↓

Switch

↓

Destination
```

The transmitted unit is called an **Ethernet Frame**.

---

# What is an Ethernet Frame?

Ethernet does not transmit raw data.

Instead, it packages data into a structured format called a **Frame**.

Example:

```text
Destination MAC

↓

Source MAC

↓

EtherType

↓

Payload

↓

FCS
```

---

# Ethernet Frame Structure

| Field | Purpose |
|--------|----------|
| Destination MAC | Identifies receiver |
| Source MAC | Identifies sender |
| EtherType | Identifies Layer 3 protocol |
| Payload | Actual data |
| FCS | Error detection |

---

# Destination MAC Address

Example:

```text
00:11:22:33:44:55
```

The switch forwards the frame toward this destination.

---

# Source MAC Address

Example:

```text
AA:BB:CC:DD:EE:FF
```

Identifies the sender of the frame.

---

# EtherType

The EtherType field tells the receiver which Layer 3 protocol is encapsulated.

Examples:

| EtherType | Protocol |
|-----------|----------|
| `0x0800` | IPv4 |
| `0x86DD` | IPv6 |
| `0x0806` | Address Resolution Protocol (ARP) |

---

# Payload

Contains the Layer 3 packet.

Examples:

- IPv4 Packet
- IPv6 Packet
- ARP Packet

---

# Frame Check Sequence (FCS)

The FCS is used for **error detection**.

Sender:

```text
Calculate FCS

↓

Transmit Frame
```

Receiver:

```text
Calculate Again

↓

Match?

↓

Yes

↓

Accept Frame
```

If the values differ:

```text
Discard Frame
```

---

# Ethernet Frame Size

Standard Ethernet frame:

| Field | Size |
|--------|------|
| Minimum Frame | 64 Bytes |
| Maximum Frame | 1518 Bytes |

Some environments support **Jumbo Frames**, which allow larger payloads, commonly around **9000 bytes**, depending on the network equipment.

---

# Ethernet Speeds

Common Ethernet speeds include:

| Standard | Speed |
|-----------|------:|
| Ethernet | 10 Mbps |
| Fast Ethernet | 100 Mbps |
| Gigabit Ethernet | 1 Gbps |
| 10 Gigabit Ethernet | 10 Gbps |
| 25 Gigabit Ethernet | 25 Gbps |
| 40 Gigabit Ethernet | 40 Gbps |
| 100 Gigabit Ethernet | 100 Gbps |
| 400 Gigabit Ethernet | 400 Gbps |

Modern data centres commonly use 10G, 25G, 40G, 100G, and increasingly 400G links.

---

# Ethernet Cabling

Common Ethernet media:

- Cat5e
- Cat6
- Cat6a
- Cat7
- Fibre Optic

Choice depends on required speed and distance.

---

# Half Duplex vs Full Duplex

### Half Duplex

Communication:

```text
Send

OR

Receive
```

Not both simultaneously.

Example:

```text
Walkie-Talkie
```

---

### Full Duplex

Communication:

```text
Send

AND

Receive
```

At the same time.

Example:

```text
Telephone Call
```

Modern Ethernet switch ports typically operate in **Full Duplex** mode.

---

# Collision Domain

A collision occurs when two devices transmit simultaneously on a shared medium.

Old Ethernet:

```text
Hub

↓

Collisions
```

Modern switched Ethernet:

```text
Switch

↓

Dedicated Link

↓

No Collisions
```

Each switch port represents its own collision domain.

---

# Broadcast Domain

Ethernet switches forward broadcast frames to all ports within the same Virtual Local Area Network (VLAN).

Example:

```text
Broadcast Frame

↓

Switch

↓

All Devices
```

Later in this module, you'll learn how **VLANs** create separate broadcast domains.

---

# Ethernet Standards

Ethernet is standardised by:

```text
IEEE 802.3
```

Examples:

- 10BASE-T
- 100BASE-TX
- 1000BASE-T
- 10GBASE-T

These standards define transmission speeds, media, and signaling methods.

---

# Enterprise Example

Office Network:

```text
Linux Server

↓

Ethernet

↓

Switch

↓

Database Server
```

Communication occurs entirely using Ethernet frames.

---

# Cloud Perspective

Although cloud networking is virtualised, the underlying physical infrastructure still relies heavily on Ethernet.

Examples:

- Hypervisors
- Top-of-Rack Switches
- Storage Networks
- Data Centre Fabrics

Ethernet remains the dominant Layer 2 technology.

---

# Kubernetes Perspective

Kubernetes worker nodes communicate over Ethernet-based infrastructure.

Example:

```text
Pod

↓

Node

↓

Ethernet

↓

Switch

↓

Another Node
```

Even overlay networks ultimately rely on Ethernet at the physical layer.

---

# Linux Perspective

Display network interfaces.

```bash
ip link
```

Display interface statistics.

```bash
ip -s link
```

Display interface speed (requires `ethtool`).

```bash
ethtool eth0
```

Replace `eth0` with your actual interface name if different.

---

# Ethernet Communication Workflow

```text
Application

↓

TCP

↓

IP Packet

↓

Ethernet Frame

↓

Network Interface Card (NIC)

↓

Switch

↓

Destination Device
```

---

# Hands-on Lab

## Task 1

Display network interfaces.

```bash
ip link
```

---

## Task 2

Display interface statistics.

```bash
ip -s link
```

---

## Task 3

Display interface speed.

```bash
ethtool <interface>
```

Replace `<interface>` with your interface name (for example, `eth0` or `ens33`).

---

## Task 4

Identify whether your network interface is operating in Full Duplex or Half Duplex.

---

## Task 5

Research the Ethernet standard used by your network adapter.

---

## Task 6

Draw an Ethernet frame and label:

- Destination MAC
- Source MAC
- EtherType
- Payload
- FCS

---

## Task 7

Compare:

- Hub
- Switch

Explain why switches eliminate collisions on individual ports.

---

## Task 8

Research which Ethernet speeds are supported by your organisation or cloud environment.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip link` | Display network interfaces |
| `ip -s link` | Display interface statistics |
| `ethtool <interface>` | Display Ethernet link information |
| `hostname -I` | Display assigned IP addresses |

---

# Common Mistakes

❌ Confusing IP addresses with MAC addresses.

✅ Ethernet uses MAC addresses at Layer 2; IP operates at Layer 3.

---

❌ Assuming Ethernet transmits IP packets directly.

✅ Ethernet encapsulates Layer 3 packets inside frames.

---

❌ Thinking collisions occur on modern switched networks.

✅ Full-duplex switched Ethernet eliminates collisions on individual links.

---

❌ Ignoring interface speed and duplex mismatches.

✅ Verify link settings during troubleshooting.

---

❌ Assuming Ethernet only exists in office LANs.

✅ Ethernet underpins enterprise networks, cloud infrastructure, and data centres.

---

# Best Practices

- Use Full Duplex whenever supported.
- Match interface speeds appropriately.
- Monitor interface statistics for errors.
- Use high-quality cabling for higher speeds.
- Verify Ethernet link health during troubleshooting.
- Document interface speeds and physical connections.

---

# Interview Questions

## Beginner

1. What is Ethernet?
2. Which OSI layer does Ethernet operate on?
3. What is an Ethernet frame?
4. What is the purpose of the FCS?

---

## Intermediate

1. Explain the structure of an Ethernet frame.
2. What is the difference between Half Duplex and Full Duplex?
3. What is a collision domain?
4. What is the purpose of the EtherType field?

---

## Architect Level

1. Explain why Ethernet remains the dominant LAN technology.
2. How does Ethernet support cloud and Kubernetes infrastructure?
3. How would you troubleshoot Ethernet connectivity issues in a production environment?

---

# Summary

In this lesson, you learned:

- What Ethernet is
- Ethernet frame structure
- MAC-based communication
- EtherType
- Frame Check Sequence (FCS)
- Ethernet speeds
- Duplex modes
- Collision domains
- IEEE 802.3 standards
- Linux Ethernet commands

Ethernet is the foundation of modern wired networking. It provides reliable Layer 2 communication through standardised frame formats, MAC addressing, and error detection. Every packet transmitted across a LAN is carried inside an Ethernet frame, making Ethernet one of the most important technologies in enterprise networking, cloud infrastructure, and data centres.

---

## Key Takeaways

- Ethernet operates at **OSI Layer 2**.
- Ethernet transmits data using **frames**.
- Frames contain **Source MAC**, **Destination MAC**, **EtherType**, **Payload**, and **FCS**.
- Modern switched Ethernet operates in **Full Duplex**, eliminating collisions on individual links.
- Ethernet is standardised by **IEEE 802.3**.
- Enterprise, cloud, and Kubernetes infrastructure all rely on Ethernet at the physical network layer.

---

## What's Next?

**[MAC Address Table](mac-address-table.md)**

In the next lesson, you'll learn about the **MAC Address Table**.

You'll explore:

- What a MAC Address Table is
- How switches learn MAC addresses
- Dynamic vs Static MAC entries
- MAC address aging
- Unknown unicast forwarding
- Switch forwarding decisions
- Linux tools for viewing MAC information

By the end of the lesson, you'll understand how Ethernet switches intelligently forward frames by building and maintaining MAC address tables.
