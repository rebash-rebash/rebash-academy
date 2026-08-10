---
title: "Trunking"
description: "Learn VLAN trunking — IEEE 802.1Q tagging, access vs trunk ports, native VLAN, tagged/untagged frames, and Linux VLAN trunk interfaces."
difficulty: intermediate
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
  - vlan
  - trunking
  - 802.1q
  - switching
  - rebash-networking-mastery
comments: false
status: ready
---

# Trunking — Carrying Multiple VLANs Across a Single Link

> A **Trunk** is a network link that carries traffic for **multiple VLANs** simultaneously between switches, routers, or servers. Instead of requiring one physical cable for each Virtual Local Area Network (VLAN), **IEEE 802.1Q Trunking** allows a single Ethernet connection to transport frames from many VLANs by adding a **VLAN Tag** to each frame. Trunking is one of the most important concepts in enterprise networking, cloud infrastructure, virtualisation, and data centre design. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand trunking.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 4: Switching → Lesson 5</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Switching</div>

<div markdown>**Lesson:** 5 of 8</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Trunking
- Learn IEEE 802.1Q VLAN tagging
- Understand Access vs Trunk Ports
- Learn Native VLAN
- Understand Tagged and Untagged Frames
- Design trunk links
- Configure VLAN trunks on Linux

---

# Prerequisites

Complete:

- [Ethernet](ethernet-switching-and-vlans.md)
- [MAC Address Table](mac-address-table.md)
- [Switch Learning](switch-learning.md)
- [VLAN](vlan.md)

---

# Why Learn Trunking?

Imagine two switches.

Each switch contains:

- VLAN 10
- VLAN 20
- VLAN 30

Without trunking:

```text
Switch A

↓

3 Separate Cables

↓

Switch B
```

One cable would be required for each VLAN.

With trunking:

```text
Switch A

↓

One Trunk Link

↓

Switch B
```

One physical cable carries traffic for all VLANs.

---

# What is a Trunk?

A **Trunk Port** is a switch port that carries traffic for **multiple VLANs**.

Example:

```text
VLAN 10

↓

VLAN 20

↓

VLAN 30

↓

Single Ethernet Link
```

---

# Access Port vs Trunk Port

| Access Port | Trunk Port |
|--------------|------------|
| One VLAN | Multiple VLANs |
| Connects End Devices | Connects Switches, Routers, Servers |
| Frames Usually Untagged | Frames Usually Tagged |
| Simple Configuration | Carries Multiple VLANs |

---

# Why VLAN Tags are Needed

Suppose VLAN 10 and VLAN 20 both use the same trunk cable.

Without VLAN tags:

```text
Frame

↓

Which VLAN?
```

Impossible to determine.

Solution:

```text
802.1Q VLAN Tag
```

---

# IEEE 802.1Q

The standard used for VLAN trunking is:

```text
IEEE 802.1Q
```

It inserts a VLAN tag into the Ethernet frame.

---

# Tagged Ethernet Frame

Normal Ethernet Frame:

```text
Destination MAC

↓

Source MAC

↓

EtherType

↓

Payload
```

802.1Q Tagged Frame:

```text
Destination MAC

↓

Source MAC

↓

802.1Q Tag

↓

EtherType

↓

Payload
```

The receiving switch reads the VLAN tag before forwarding the frame.

---

# VLAN Tag

The VLAN tag contains information including:

- VLAN ID (VID)
- Priority (802.1p)
- Tag Protocol Identifier (TPID)

The **VLAN ID** identifies the VLAN to which the frame belongs.

Example:

```text
VLAN ID

20
```

---

# Native VLAN

The **Native VLAN** is the VLAN whose traffic is sent **without an 802.1Q tag** on a trunk link.

Example:

```text
Native VLAN

1
```

Frames belonging to the native VLAN are transmitted untagged.

**Best Practice**

Many organisations change the native VLAN from VLAN 1 to an unused VLAN to reduce the risk of VLAN hopping attacks and configuration mistakes.

---

# Tagged vs Untagged Frames

Tagged:

```text
Frame

↓

802.1Q Tag

↓

VLAN 20
```

Untagged:

```text
Frame

↓

No Tag

↓

Native VLAN
```

---

# Trunk Example

Switch A:

```text
VLAN 10

VLAN 20

VLAN 30
```

↓

```text
802.1Q Trunk
```

↓

Switch B:

```text
VLAN 10

VLAN 20

VLAN 30
```

All VLANs are transported over one cable.

---

# Allowed VLANs

Administrators can restrict which VLANs are allowed on a trunk.

Example:

```text
Allow

10

20

30
```

Block:

```text
40

50
```

Limiting allowed VLANs improves security and reduces unnecessary traffic.

---

# Trunk Workflow

```text
Frame Arrives

↓

Identify VLAN

↓

Insert 802.1Q Tag

↓

Transmit Across Trunk

↓

Receiving Switch Reads Tag

↓

Forward Within Correct VLAN
```

---

# Enterprise Example

Head Office:

```text
Floor 1

↓

Switch
```

↓

```text
802.1Q Trunk
```

↓

```text
Core Switch
```

All departmental VLANs are transported over a single high-speed uplink.

---

# Cloud Perspective

Cloud providers generally hide physical trunk configuration from customers.

However, similar concepts exist internally within:

- Hypervisors
- Virtual Switches
- Data Centre Fabrics
- Network Virtualisation Platforms

Trunking remains a fundamental technology in the underlying infrastructure.

---

# Kubernetes Perspective

A Kubernetes node may connect to a trunk port when hosting workloads from multiple VLANs.

Example:

```text
Node

↓

Trunk Port

↓

Management VLAN

↓

Storage VLAN

↓

Application VLAN
```

The Linux host creates separate VLAN interfaces for each tagged network.

---

# Linux Perspective

Display interfaces.

```bash
ip link
```

Create VLAN interface.

```bash
sudo ip link add link eth0 name eth0.20 type vlan id 20
```

Enable interface.

```bash
sudo ip link set eth0.20 up
```

Assign IP.

```bash
sudo ip addr add 192.168.20.10/24 dev eth0.20
```

Display VLAN information.

```bash
ip -d link
```

---

# Linux VLAN Trunk Example

Physical Interface:

```text
eth0
```

Logical Interfaces:

```text
eth0.10

↓

VLAN 10
```

```text
eth0.20

↓

VLAN 20
```

```text
eth0.30

↓

VLAN 30
```

Each logical interface communicates with its corresponding VLAN across the same physical link.

---

# Access vs Trunk Example

Access Port:

```text
PC

↓

Switch

↓

VLAN 10
```

Trunk Port:

```text
Switch

↓

802.1Q Trunk

↓

Switch
```

---

# Hands-on Lab

## Task 1

Display interfaces.

```bash
ip link
```

---

## Task 2

Create VLAN 20.

```bash
sudo ip link add link eth0 name eth0.20 type vlan id 20
```

---

## Task 3

Bring interface online.

```bash
sudo ip link set eth0.20 up
```

---

## Task 4

Assign IP address.

```bash
sudo ip addr add 192.168.20.10/24 dev eth0.20
```

---

## Task 5

Display VLAN interfaces.

```bash
ip -d link
```

---

## Task 6

Draw two switches connected by a trunk carrying:

- VLAN 10
- VLAN 20
- VLAN 30

---

## Task 7

Compare:

- Access Port
- Trunk Port

List at least five differences.

---

## Task 8

Research how 802.1Q trunking is configured on your preferred switch vendor.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip link` | Display interfaces |
| `ip -d link` | Display VLAN details |
| `ip addr` | Display IP addresses |
| `ip link add` | Create VLAN interface |
| `ip link set` | Enable interface |

---

# Common Mistakes

❌ Using an access port where a trunk is required.

✅ Verify port mode before deployment.

---

❌ Forgetting VLAN tags.

✅ Ensure 802.1Q tagging is enabled on trunk links.

---

❌ Allowing every VLAN across every trunk.

✅ Restrict trunks to only required VLANs.

---

❌ Leaving the native VLAN as the production VLAN.

✅ Use a dedicated native VLAN that carries no user traffic where appropriate.

---

❌ Assuming end-user devices need trunk ports.

✅ Most client devices connect to access ports.

---

# Best Practices

- Use IEEE 802.1Q for VLAN trunking.
- Restrict allowed VLANs on trunk links.
- Use a dedicated native VLAN instead of VLAN 1 when practical.
- Document trunk connections.
- Verify trunk status during troubleshooting.
- Use high-speed links for trunk ports between switches.

---

# Interview Questions

## Beginner

1. What is a trunk port?
2. What is IEEE 802.1Q?
3. Why is VLAN tagging required?
4. What is the native VLAN?

---

## Intermediate

1. Compare access ports and trunk ports.
2. Explain how VLAN tags work.
3. Why should allowed VLANs be restricted?
4. What happens when a tagged frame reaches a switch?

---

## Architect Level

1. Design a trunking architecture for a campus network.
2. Explain trunking in virtualised environments.
3. How would you troubleshoot VLAN traffic not crossing a trunk link?

---

# Summary

In this lesson, you learned:

- Trunking
- IEEE 802.1Q
- VLAN tagging
- Access vs Trunk Ports
- Native VLAN
- Tagged and Untagged Frames
- Linux VLAN interfaces
- Enterprise trunk design

Trunking allows multiple VLANs to share a single physical connection by using IEEE 802.1Q tags. This enables scalable, efficient, and manageable enterprise networks while reducing cabling requirements and supporting large Layer 2 infrastructures.

---

## Key Takeaways

- A **Trunk Port** carries traffic for multiple VLANs.
- **IEEE 802.1Q** is the standard for VLAN tagging.
- Access ports carry one VLAN; trunk ports carry many.
- Tagged frames include a VLAN ID.
- Native VLAN traffic is transmitted without an 802.1Q tag.
- Restrict allowed VLANs to improve security and efficiency.

---

## What's Next?

**[STP](spanning-tree-protocol.md)**

In the next lesson, you'll learn about **STP (Spanning Tree Protocol)**.

You'll explore:

- Why switching loops occur
- Broadcast storms
- MAC address instability
- STP operation
- Root Bridge election
- Port states and roles
- Rapid Spanning Tree Protocol (RSTP)

By the end of the lesson, you'll understand how STP prevents Layer 2 loops and ensures a stable, loop-free Ethernet network.
