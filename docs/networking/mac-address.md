---
title: "MAC Address"
description: "Learn Media Access Control (MAC) addresses — structure, OUI, switch learning, ARP, unicast/broadcast/multicast, and Linux Layer 2 troubleshooting."
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
  - mac
  - ethernet
  - layer-2
  - fundamentals
  - rebash-networking-mastery
comments: false
status: ready
---

# MAC Address — The Physical Address of a Network Device

> Every device connected to a local network has a unique identifier known as a **MAC (Media Access Control) Address**. Unlike an IP address, which can change depending on the network, a MAC address identifies a network interface at **Layer 2 (Data Link Layer)** of the OSI Model. Switches use MAC addresses to forward Ethernet frames efficiently within a Local Area Network (LAN). Understanding MAC addresses is essential for Linux administrators, DevOps engineers, Cloud Architects, Platform Engineers, Site Reliability Engineers (SREs), and Network Engineers.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 1: Networking Fundamentals → Lesson 7</p>

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

<div markdown>**Lesson:** 7 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand what a MAC Address is
- Explain the structure of a MAC Address
- Differentiate MAC Addresses from IP Addresses
- Understand how switches use MAC Addresses
- Explain MAC learning
- Understand MAC Address types
- Identify MAC spoofing
- Troubleshoot Layer 2 communication

---

# Prerequisites

Complete:

- [What is Networking?](introduction-to-networking.md)
- [Types of Networks](types-of-networks.md)
- [Network Topologies](network-topologies.md)
- [OSI Model](osi-model.md)
- [TCP/IP Model](tcp-ip-model.md)
- [Data Encapsulation](data-encapsulation.md)

---

# Why Learn MAC Addresses?

Suppose two computers are connected to the same switch.

How does the switch know where to send the Ethernet frame?

The answer is:

**MAC Addresses**

Every Ethernet frame contains source and destination MAC addresses that allow switches to forward traffic correctly.

---

# What is a MAC Address?

A **MAC Address (Media Access Control Address)** is a **48-bit hardware identifier** assigned to a network interface.

It uniquely identifies a device on a local network.

Unlike IP addresses, MAC addresses operate at the **Data Link Layer (Layer 2)**.

---

# Real-Life Analogy

Think of:

- **IP Address** → Home address
- **MAC Address** → Person's fingerprint

A home address may change.

A fingerprint uniquely identifies a person.

Similarly:

- IP addresses can change.
- MAC addresses identify the network interface.

---

# MAC Address Format

A MAC Address consists of **48 bits (6 bytes)**.

Example:

```text
00:1A:2B:3C:4D:5E
```

Other common formats:

```text
00-1A-2B-3C-4D-5E

001A.2B3C.4D5E
```

All three represent the same MAC address.

---

# MAC Address Structure

```text
00 : 1A : 2B : 3C : 4D : 5E

│────────────│────────────│

Vendor (OUI)     Device Identifier
```

The address is divided into two parts.

---

# Organizationally Unique Identifier (OUI)

The first **24 bits** identify the manufacturer.

Examples:

- Intel
- Dell
- Cisco
- HP
- Apple
- Lenovo

The OUI is assigned by the Institute of Electrical and Electronics Engineers (IEEE).

Example:

```text
00:1A:2B
```

This identifies the hardware vendor.

---

# Device Identifier

The last **24 bits** uniquely identify the network interface manufactured by that vendor.

Example:

```text
3C:4D:5E
```

---

# MAC Address Example

```text
00:1A:2B:3C:4D:5E

Vendor

↓

Intel

Device

↓

Specific Network Card
```

---

# Where is the MAC Address Stored?

Traditionally, the MAC address is programmed into the Network Interface Card (NIC) by the manufacturer.

Modern operating systems can temporarily override (spoof) the address for testing or privacy.

---

# MAC Address vs IP Address

| MAC Address | IP Address |
|-------------|------------|
| Layer 2 | Layer 3 |
| Physical Identifier | Logical Identifier |
| Used inside LAN | Used across networks |
| Usually permanent | Can change |
| Switches use MAC | Routers use IP |

---

# How Switches Use MAC Addresses

Suppose:

```text
Laptop A

↓

Switch

↓

Laptop B
```

When Laptop A sends data:

```text
Source MAC

↓

Destination MAC

↓

Ethernet Frame
```

The switch reads the destination MAC and forwards the frame to the correct port.

---

# MAC Address Table

Switches maintain a **MAC Address Table**.

Example:

| MAC Address | Port |
|--------------|------|
| 00:11:22:33:44:55 | Port 1 |
| AA:BB:CC:DD:EE:FF | Port 2 |
| 11:22:33:44:55:66 | Port 3 |

This allows efficient frame forwarding.

---

# MAC Learning

When a switch receives a frame:

1. Reads the source MAC.
2. Associates it with the incoming port.
3. Stores the mapping in the MAC table.
4. Uses the table for future forwarding.

This process is called **MAC Learning**.

---

# Unknown Destination

If the destination MAC is unknown:

```text
Switch

↓

Flood Frame

↓

All Ports

↓

Destination Responds

↓

Switch Learns MAC
```

This behaviour occurs only until the switch learns the correct MAC address.

---

# Types of MAC Addresses

There are three primary types.

---

## Unicast

Communication between one sender and one receiver.

```text
Laptop

↓

Server
```

Most Ethernet traffic is unicast.

---

## Broadcast

One sender communicates with every device in the LAN.

Broadcast MAC:

```text
FF:FF:FF:FF:FF:FF
```

Every device processes the frame.

Used by:

- Address Resolution Protocol (ARP)
- Dynamic Host Configuration Protocol (DHCP) Discovery

---

## Multicast

Communication between one sender and a selected group of receivers.

Used by:

- IPTV
- Video Streaming
- Routing Protocols

Only subscribed devices receive the traffic.

---

# MAC Address Example

```text
Laptop

↓

Switch

↓

Printer

↓

Server
```

Each device has its own unique MAC address.

---

# ARP and MAC Addresses

Suppose a computer knows the destination IP address but not the MAC address.

It sends an **ARP Request**:

```text
Who has

192.168.1.20?
```

The destination replies:

```text
I do.

My MAC is

00:1A:2B:3C:4D:5E
```

Communication can now proceed.

---

# MAC Address Spoofing

Operating systems can temporarily change the MAC address.

Example:

```bash
ip link set dev eth0 address 02:11:22:33:44:55
```

Reasons include:

- Privacy
- Security testing
- Penetration testing
- Network troubleshooting

---

# MAC Address Security

Common attacks include:

- MAC Spoofing
- MAC Flooding
- ARP Spoofing

Enterprise switches mitigate these using:

- Port Security
- Dynamic ARP Inspection
- 802.1X Authentication

---

# Viewing MAC Addresses in Linux

Display interfaces.

```bash
ip link
```

Example:

```text
link/ether

00:1A:2B:3C:4D:5E
```

---

Display interface details.

```bash
ip addr
```

---

Traditional command:

```bash
ifconfig
```

---

# Production Perspective

MAC addresses are widely used for:

- Ethernet switching
- ARP communication
- DHCP reservations
- Access control
- Network inventory
- Security monitoring
- Device identification

Every Ethernet network depends on MAC addressing.

---

# Cloud Perspective

Although cloud networking is largely virtualised, MAC addresses still exist.

Examples:

- Virtual Machines
- Kubernetes Nodes
- Virtual Network Interfaces
- Cloud Load Balancers

Cloud platforms assign virtual MAC addresses behind the scenes.

---

# Kubernetes Perspective

Pods typically communicate using virtual Ethernet interfaces.

These interfaces also have MAC addresses, although Kubernetes networking abstracts most Layer 2 operations from users.

---

# Hands-on Lab

## Task 1

Display MAC addresses.

```bash
ip link
```

---

## Task 2

Display interface details.

```bash
ip addr
```

---

## Task 3

Display the ARP table.

```bash
ip neigh
```

---

## Task 4

Ping another device.

```bash
ping <ip-address>
```

Observe changes in the ARP table.

---

## Task 5

Capture ARP packets.

```bash
sudo tcpdump arp
```

---

## Task 6

Identify the vendor of your MAC address using the first three bytes (OUI).

---

## Task 7

List every network interface on your system and record its MAC address.

---

## Task 8

Draw a network diagram showing:

- Two laptops
- One switch
- One router

Label the MAC address used at each Ethernet connection and explain how the switch forwards frames.

---

# Linux Commands

| Command | Purpose |
|----------|---------|
| `ip link` | Display MAC addresses |
| `ip addr` | Display interface information |
| `ip neigh` | Display ARP table |
| `arp -a` | Display ARP cache (legacy) |
| `tcpdump arp` | Capture ARP packets |

---

# Common Mistakes

❌ Confusing MAC and IP addresses.

✅ MAC operates at Layer 2; IP operates at Layer 3.

---

❌ Thinking MAC addresses route across the Internet.

✅ MAC addresses are used only within the local network.

---

❌ Assuming MAC addresses never change.

✅ They can be spoofed or assigned virtually.

---

❌ Believing routers forward MAC addresses between networks.

✅ Routers replace Layer 2 headers at each network hop.

---

❌ Ignoring ARP.

✅ ARP maps IP addresses to MAC addresses on a LAN.

---

# Best Practices

- Understand the difference between MAC and IP addresses.
- Learn how switches build MAC address tables.
- Use `ip link` instead of deprecated tools where possible.
- Monitor ARP activity when troubleshooting LAN issues.
- Protect enterprise networks against MAC spoofing and ARP attacks.

---

# Interview Questions

## Beginner

1. What is a MAC Address?
2. Which OSI layer uses MAC addresses?
3. How many bits are in a MAC Address?
4. What is the broadcast MAC address?

---

## Intermediate

1. Explain MAC learning.
2. How does a switch forward Ethernet frames?
3. What is the purpose of the OUI?
4. Compare MAC and IP addresses.

---

## Architect Level

1. How does ARP interact with MAC addresses?
2. Explain how virtual machines and containers use MAC addresses.
3. How would you secure an enterprise network against MAC spoofing attacks?

---

# Summary

In this lesson, you learned:

- What a MAC Address is
- MAC Address structure
- OUI and device identifier
- MAC learning
- MAC address tables
- Unicast, Broadcast, and Multicast communication
- ARP interaction
- MAC spoofing
- Linux commands for viewing MAC addresses

MAC addresses provide the foundation for Layer 2 communication. Switches rely on MAC addresses to forward Ethernet frames efficiently within a LAN, while ARP bridges the gap between Layer 3 IP addresses and Layer 2 MAC addresses. Understanding MAC addressing is essential before moving on to IP addressing and routing.

---

## Key Takeaways

- A MAC Address is a unique 48-bit identifier for a network interface.
- MAC addresses operate at Layer 2 of the OSI Model.
- Switches use MAC tables to forward frames.
- Broadcast MAC addresses reach every device on the local network.
- ARP maps IP addresses to MAC addresses for local communication.

---

## What's Next?

**[IP Address](ip-addressing.md)**
