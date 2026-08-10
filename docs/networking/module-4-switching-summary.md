---
title: "Module 4 Summary — Switching"
description: "Review Module 4 of Networking Mastery — Ethernet, MAC tables, switch learning, VLANs, trunking, STP, EtherChannel, and Inter-VLAN Routing."
difficulty: intermediate
estimated_time: "30 min"
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
  - switching
  - vlan
  - summary
  - rebash-networking-mastery
comments: false
status: ready
---

# Module 4 Summary — Switching

> Congratulations! You have successfully completed **Module 4: Switching**.

Switching is one of the most important concepts in computer networking. Every communication inside a Local Area Network (LAN) depends on switches making intelligent forwarding decisions using Media Access Control (MAC) addresses. Modern enterprise networks, cloud data centres, Kubernetes clusters, and campus infrastructures all rely on switching technologies to provide high-speed, secure, and scalable connectivity.

In this module, you learned how Ethernet switches operate, how they learn MAC addresses, how Virtual Local Area Networks (VLANs) segment networks, how trunks carry multiple VLANs, how Spanning Tree Protocol (STP) prevents loops, how EtherChannel increases bandwidth, and how Layer 3 devices enable communication between VLANs.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 4: Switching → Summary</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 30 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Switching</div>

<div markdown>**Lesson:** Summary</div>

</div>

</div>

---

# What You Learned

Throughout this module, you explored the complete lifecycle of Layer 2 switching—from Ethernet frame forwarding to enterprise switching architectures.

---

## Lesson 1 — Ethernet

You learned:

- Ethernet Fundamentals
- IEEE 802.3 Standards
- Ethernet Frames
- MAC Addresses
- EtherType
- Frame Check Sequence (FCS)
- Duplex Modes
- Collision Domains
- Ethernet Speeds

Key takeaway:

> Ethernet is the foundation of modern wired networking and provides reliable Layer 2 communication using Ethernet frames.

---

## Lesson 2 — MAC Address Table

You explored:

- MAC Address Tables
- Content Addressable Memory (CAM) Tables
- Dynamic MAC Learning
- Static MAC Entries
- MAC Aging
- Unknown Unicast
- Broadcast Forwarding

You learned how switches maintain forwarding information for efficient frame delivery.

---

## Lesson 3 — Switch Learning

You studied:

- Learn → Lookup → Forward Process
- Source MAC Learning
- Destination MAC Lookup
- Flooding
- Forwarding
- MAC Table Updates
- MAC Address Movement

You now understand how switches automatically discover connected devices and make forwarding decisions.

---

## Lesson 4 — VLAN

You learned:

- Virtual Local Area Networks
- VLAN IDs
- Access Ports
- Broadcast Domains
- VLAN Isolation
- Network Segmentation
- Enterprise VLAN Design

You now understand how a single physical switch can be divided into multiple logical networks.

---

## Lesson 5 — Trunking

You explored:

- Trunk Ports
- IEEE 802.1Q
- VLAN Tagging
- Native VLAN
- Tagged Frames
- Untagged Frames
- Allowed VLANs

You learned how multiple VLANs are transported across a single physical connection.

---

## Lesson 6 — STP (Spanning Tree Protocol)

You studied:

- Layer 2 Loops
- Broadcast Storms
- MAC Address Flapping
- Root Bridge Election
- Port Roles
- Port States
- Bridge Protocol Data Units (BPDUs)
- Rapid Spanning Tree Protocol (RSTP)

You learned how STP creates a loop-free Ethernet topology while preserving redundancy.

---

## Lesson 7 — EtherChannel

You explored:

- Link Aggregation
- Port Channels
- Link Aggregation Control Protocol (LACP)
- Port Aggregation Protocol (PAgP)
- Load Balancing
- Redundancy
- Linux Bonding

You learned how multiple physical links can be combined into a single logical connection for higher bandwidth and resilience.

---

## Lesson 8 — Inter-VLAN Routing

You learned:

- Layer 3 Routing Between VLANs
- Router-on-a-Stick
- Layer 3 Switches
- Switched Virtual Interfaces (SVIs)
- Default Gateways
- Packet Flow Between VLANs

You now understand how isolated VLANs communicate through Layer 3 routing.

---

# Skills You Have Acquired

After completing this module, you can now:

- Explain how Ethernet works
- Understand Ethernet frame structure
- Read and interpret MAC addresses
- Explain how switches learn MAC addresses
- Troubleshoot MAC table issues
- Design VLAN-based enterprise networks
- Configure VLAN segmentation
- Explain IEEE 802.1Q trunking
- Understand STP and RSTP
- Design redundant switched networks
- Implement EtherChannel concepts
- Explain Inter-VLAN Routing
- Design scalable Layer 2 enterprise networks

---

# Linux Commands Covered

```bash
ip link

ip -d link

ip addr

ip route

ip neigh

bridge link

bridge vlan

ethtool <interface>

tcpdump -e

cat /proc/net/bonding/bond0

modprobe bonding
```

These commands help inspect Ethernet interfaces, VLANs, Linux bridges, routing information, MAC-related data, and bonded interfaces.

---

# Switching Concepts Covered

You now understand:

- Ethernet
- Ethernet Frames
- MAC Addresses
- CAM Tables
- Switch Learning
- Frame Forwarding
- Unknown Unicast Flooding
- Broadcast Domains
- VLANs
- Access Ports
- Trunk Ports
- IEEE 802.1Q
- Native VLAN
- STP
- RSTP
- Root Bridge
- BPDUs
- EtherChannel
- LACP
- PAgP
- Link Aggregation
- Router-on-a-Stick
- Layer 3 Switching
- Switched Virtual Interfaces (SVIs)

These technologies form the backbone of modern Layer 2 networking.

---

# Enterprise Perspective

Switching technologies are used extensively in:

- Enterprise LANs
- Campus Networks
- Data Centres
- Financial Institutions
- Government Networks
- Healthcare Organisations
- Universities
- Manufacturing Environments

Reliable switching is essential for high availability, scalability, and security.

---

# Cloud Perspective

Although cloud networking abstracts many physical details, the underlying infrastructure relies on switching technologies such as:

- Ethernet Fabrics
- VLAN Segmentation
- Link Aggregation
- High-Speed Switching
- Virtual Switches

Understanding switching fundamentals helps engineers design and troubleshoot hybrid and cloud-native environments.

---

# Kubernetes Perspective

Modern Kubernetes clusters depend on switching concepts through:

- Worker Node Connectivity
- Physical Network Infrastructure
- Virtual Switches
- Overlay Networks
- Storage Networks
- Management Networks

Even when overlay networking is used, physical Ethernet switching remains the foundation.

---

# Module 4 Learning Map

```text
Ethernet

↓

MAC Address Table

↓

Switch Learning

↓

VLAN

↓

Trunking

↓

STP

↓

EtherChannel

↓

Inter-VLAN Routing
```

Each lesson built upon the previous one, progressing from basic Ethernet communication to enterprise-grade switched network design.

---

# Self-Assessment Checklist

Before moving to Module 5, ensure you can confidently answer the following:

- [ ] Can you explain how Ethernet frames are transmitted?
- [ ] Can you identify the fields of an Ethernet frame?
- [ ] Do you understand how switches learn MAC addresses?
- [ ] Can you explain how a MAC Address Table works?
- [ ] Can you distinguish between access ports and trunk ports?
- [ ] Can you explain why VLANs are used?
- [ ] Do you understand IEEE 802.1Q VLAN tagging?
- [ ] Can you explain how STP prevents Layer 2 loops?
- [ ] Do you understand the purpose of EtherChannel?
- [ ] Can you explain how devices in different VLANs communicate?

If you answered **Yes** to all of these, you're ready to move into routing technologies.

---

# Interview Readiness

You are now prepared to answer common interview questions such as:

- What is Ethernet?
- What is a MAC Address Table?
- How does Switch Learning work?
- What is a VLAN?
- What is the difference between an Access Port and a Trunk Port?
- What is IEEE 802.1Q?
- What is STP and why is it needed?
- What is a Broadcast Storm?
- What is EtherChannel?
- What is LACP?
- What is Inter-VLAN Routing?
- What is a Switched Virtual Interface (SVI)?

These topics are commonly asked in Networking, Linux, DevOps, Cloud, Platform Engineering, and Cybersecurity interviews.

---

# Best Practices

As you continue learning networking:

- Design networks using VLANs for logical separation.
- Restrict VLANs on trunk links to only those required.
- Enable STP or RSTP to prevent Layer 2 loops.
- Use LACP for standards-based link aggregation.
- Monitor MAC tables and interface statistics during troubleshooting.
- Document VLAN IDs, trunk links, and switch topology.
- Use Layer 3 switches for high-performance Inter-VLAN Routing in enterprise environments.

---

# Key Takeaways

- Ethernet is the foundation of wired networking.
- Switches learn MAC addresses dynamically and forward frames intelligently.
- VLANs create isolated Layer 2 broadcast domains.
- IEEE 802.1Q enables multiple VLANs to share a single trunk link.
- STP prevents Layer 2 loops while maintaining redundant paths.
- EtherChannel combines multiple links into one logical interface for higher bandwidth and resilience.
- Inter-VLAN Routing enables communication between separate VLANs using Layer 3 devices.

---

# Congratulations!

You have successfully completed **Module 4: Switching**.

You now have a strong understanding of enterprise switching technologies and are prepared to build scalable, secure, and highly available Layer 2 networks.

---

## What's Next?

**[Routing Basics](routing-fundamentals.md)**

In **Module 5: Routing**, you'll learn how routers connect different networks and make forwarding decisions based on IP addresses.

You'll explore:

- Routing Basics
- Static Routing
- Dynamic Routing
- Routing Information Protocol (RIP)
- Open Shortest Path First (OSPF)
- Enhanced Interior Gateway Routing Protocol (EIGRP) Concepts
- Border Gateway Protocol (BGP) Introduction
- Default Routes
- Route Summarisation
- Route Redistribution

By the end of Module 5, you'll understand how packets travel across enterprise networks, cloud environments, data centres, and the Internet using modern Layer 3 routing technologies.
