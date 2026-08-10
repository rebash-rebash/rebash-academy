---
title: "STP"
description: "Learn Spanning Tree Protocol (STP) — switching loops, broadcast storms, Root Bridge election, port roles and states, BPDUs, and RSTP."
difficulty: intermediate
estimated_time: "100 min"
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
  - stp
  - rstp
  - switching
  - ethernet
  - rebash-networking-mastery
comments: false
status: ready
---

# STP (Spanning Tree Protocol) — Preventing Switching Loops in Ethernet Networks

> **Spanning Tree Protocol (STP)** is a Layer 2 protocol that prevents **switching loops** in Ethernet networks. While redundant links improve network availability, they can also create loops that cause **broadcast storms**, **MAC address table instability**, and **multiple frame copies**. STP intelligently detects these loops and blocks redundant paths while keeping them available as backups. If the active path fails, STP automatically activates a backup path, ensuring a loop-free and highly available network. Understanding STP is essential for Linux administrators, DevOps engineers, Cloud Architects, Platform Engineers, Site Reliability Engineers (SREs), and Network Engineers.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 4: Switching → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 100 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Switching</div>

<div markdown>**Lesson:** 6 of 8</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Spanning Tree Protocol (STP)
- Learn why switching loops occur
- Understand broadcast storms
- Learn Root Bridge election
- Understand STP port roles
- Learn STP port states
- Understand Rapid Spanning Tree Protocol (RSTP)
- Troubleshoot STP-related issues

---

# Prerequisites

Complete:

- [Ethernet](ethernet-switching-and-vlans.md)
- [MAC Address Table](mac-address-table.md)
- [Switch Learning](switch-learning.md)
- [VLAN](vlan.md)
- [Trunking](trunking.md)

---

# Why Learn STP?

Imagine connecting two switches with two cables.

```text
Switch A

⇄

Switch B
```

This provides redundancy.

If one cable fails:

```text
Other Cable

↓

Still Works
```

Sounds great!

But there is a serious problem.

---

# The Switching Loop Problem

Suppose a broadcast frame enters the network.

```text
Broadcast

↓

Switch A

↓

Switch B

↓

Switch A

↓

Switch B

↓

Forever...
```

The frame never stops circulating.

This is called a:

```text
Layer 2 Loop
```

---

# Problems Caused by Switching Loops

Loops can cause:

- Broadcast Storms
- Multiple Frame Copies
- MAC Address Table Instability
- High CPU Utilisation
- Network Congestion
- Complete Network Outage

Even a single loop can severely impact an enterprise network.

---

# Broadcast Storm

A broadcast frame is forwarded repeatedly.

```text
Broadcast

↓

Switch

↓

Loop

↓

More Broadcasts

↓

Network Saturation
```

Eventually, legitimate traffic cannot be transmitted.

---

# MAC Address Instability

Switches continuously relearn MAC addresses from different ports.

Example:

```text
MAC

AA

↓

Port 1
```

Moments later:

```text
MAC

AA

↓

Port 2
```

Then:

```text
MAC

AA

↓

Port 1
```

The MAC table constantly changes.

This is known as:

```text
MAC Flapping
```

---

# Multiple Frame Copies

Because frames loop continuously:

```text
One Frame

↓

Multiple Copies

↓

Destination Receives Duplicates
```

Applications may experience degraded performance or unexpected behaviour.

---

# What is STP?

**Spanning Tree Protocol (STP)** prevents switching loops by creating a **loop-free logical topology**.

It works by:

- Detecting redundant links
- Selecting the best path
- Blocking unnecessary paths
- Automatically recovering after failures

---

# IEEE Standard

Classic STP is defined by:

```text
IEEE 802.1D
```

A faster version called **Rapid Spanning Tree Protocol (RSTP)** is defined by:

```text
IEEE 802.1w
```

---

# How STP Works

Consider this topology:

```text
Switch A

⇄

Switch B

⇄

Switch C

⇄

Switch A
```

STP detects the loop and blocks one redundant link.

Result:

```text
Loop-Free Network
```

---

# Root Bridge

STP begins by electing one switch as the:

```text
Root Bridge
```

The Root Bridge becomes the reference point for the entire spanning tree.

---

# Root Bridge Election

The switch with the **lowest Bridge ID (Bridge Priority + MAC Address)** becomes the Root Bridge.

Example:

| Switch | Priority | MAC | Result |
|----------|---------|------|--------|
| Switch A | 32768 | Lowest | ✅ Root |
| Switch B | 32768 | Higher | Non-Root |
| Switch C | 32768 | Highest | Non-Root |

If priorities are equal, the lowest MAC address wins.

---

# Root Port

Every non-root switch selects one:

```text
Root Port
```

Characteristics:

- Best path to the Root Bridge
- Forwarding state
- One Root Port per non-root switch

---

# Designated Port

Each network segment elects one:

```text
Designated Port
```

Responsibilities:

- Forwards traffic toward the segment
- One Designated Port per segment
- Always in the Forwarding state

---

# Blocking Port

Redundant links become:

```text
Blocking Ports
```

Characteristics:

- Prevent loops
- Do not forward user traffic
- Can become active if another link fails

---

# STP Port Roles

| Port Role | Function |
|------------|----------|
| Root Port | Best path to Root Bridge |
| Designated Port | Forwards traffic for the segment |
| Alternate Port (RSTP) | Backup path |
| Blocking Port (Classic STP) | Prevents loops |

---

# STP Port States (Classic STP)

Classic STP defines five port states.

| State | Purpose |
|--------|----------|
| Blocking | Prevent loops |
| Listening | Processing BPDUs, preparing topology |
| Learning | Learning MAC addresses |
| Forwarding | Forwarding traffic |
| Disabled | Administratively or operationally down |

Only ports in the **Forwarding** state send user traffic.

---

# RSTP Port States

Rapid STP simplifies the process.

| RSTP State | Description |
|-------------|-------------|
| Discarding | Not forwarding traffic |
| Learning | Learning MAC addresses |
| Forwarding | Forwarding traffic |

RSTP converges much faster than classic STP.

---

# BPDU (Bridge Protocol Data Unit)

Switches exchange special control messages called:

```text
BPDU
```

BPDUs contain information such as:

- Root Bridge ID
- Path Cost
- Bridge ID
- Timers

These messages allow switches to build and maintain the spanning tree.

---

# Path Cost

STP chooses the path with the:

```text
Lowest Cost
```

Higher-speed links generally have lower path costs.

Example:

| Link Speed | Relative Cost |
|------------|---------------|
| 100 Mbps | Higher |
| 1 Gbps | Lower |
| 10 Gbps | Even Lower |

---

# Link Failure Recovery

Suppose the active link fails.

```text
Forwarding Link

↓

Failure
```

STP recalculates the topology.

```text
Blocked Link

↓

Forwarding
```

The network remains operational without manual intervention.

---

# STP Workflow

```text
Switches Start

↓

Exchange BPDUs

↓

Elect Root Bridge

↓

Calculate Best Paths

↓

Assign Port Roles

↓

Block Redundant Links

↓

Loop-Free Network
```

---

# Enterprise Example

Campus Network:

```text
Access Switches

↓

Distribution Switches

↓

Core Switches
```

Multiple redundant uplinks exist.

STP ensures:

- No Layer 2 loops
- Automatic failover
- High availability

---

# Cloud Perspective

Traditional STP is rarely exposed to cloud users because cloud providers use highly virtualised data centre fabrics.

However, the underlying physical infrastructure still uses loop prevention mechanisms and redundancy principles.

---

# Kubernetes Perspective

Kubernetes itself does not implement STP.

However, Kubernetes worker nodes connected to physical enterprise networks benefit from STP running on the underlying switches, preventing Layer 2 loops between nodes and upstream infrastructure.

---

# Linux Perspective

Linux servers generally do not participate in STP unless configured as bridges.

Display network interfaces.

```bash
ip link
```

Display bridge information (if Linux bridge is configured).

```bash
bridge link
```

Display STP status for Linux bridges.

```bash
bridge vlan
```

Some Linux bridge configurations also expose STP settings through:

```bash
brctl show
```

(`brctl` is deprecated on many modern distributions but may still be encountered.)

---

# STP Topology Example

Without STP:

```text
      Switch A
      /      \
     /        \
Switch B ---- Switch C

❌ Loop
```

With STP:

```text
      Switch A
      /      \
     /        X
Switch B ---- Switch C

✔ One Link Blocked
```

---

# Hands-on Lab

## Task 1

Display Linux network interfaces.

```bash
ip link
```

---

## Task 2

If using Linux bridges, display bridge information.

```bash
bridge link
```

---

## Task 3

Draw a topology containing three switches connected in a triangle.

Identify:

- Root Bridge
- Root Ports
- Designated Ports
- Blocking Port

---

## Task 4

Explain what happens if the forwarding link fails.

---

## Task 5

Compare:

- STP
- RSTP

List at least five differences.

---

## Task 6

Research BPDU Guard, Root Guard, and Loop Guard.

Explain where each feature should be deployed.

---

## Task 7

Create a table showing STP port states and their purposes.

---

## Task 8

Research STP implementation on Cisco, Juniper, or Aruba switches.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip link` | Display interfaces |
| `bridge link` | Display Linux bridge ports |
| `bridge vlan` | Display VLAN information on Linux bridges |
| `brctl show` | Display bridge information (legacy) |

---

# Common Mistakes

❌ Connecting redundant links without STP.

✅ Always enable a loop prevention protocol in Layer 2 networks.

---

❌ Assuming blocked ports are broken.

✅ Blocked ports are backup paths waiting for failures.

---

❌ Confusing Root Port with Root Bridge.

✅ The Root Bridge is a switch; the Root Port is a port on a non-root switch.

---

❌ Ignoring BPDUs.

✅ BPDUs are essential for STP operation.

---

❌ Using default bridge priorities everywhere.

✅ Configure the intended Root Bridge explicitly in production networks.

---

# Best Practices

- Enable STP or RSTP on Layer 2 switching environments.
- Prefer RSTP for faster convergence.
- Configure the Root Bridge intentionally.
- Enable BPDU Guard on end-user access ports.
- Use Root Guard where appropriate.
- Regularly verify STP topology after network changes.
- Avoid creating unnecessary Layer 2 loops.

---

# Interview Questions

## Beginner

1. What is STP?
2. Why is STP needed?
3. What is a broadcast storm?
4. What is the Root Bridge?

---

## Intermediate

1. Explain the STP election process.
2. Compare STP and RSTP.
3. What are Root Ports and Designated Ports?
4. What is MAC address flapping?

---

## Architect Level

1. Design a highly available Layer 2 network using STP.
2. How would you troubleshoot an STP loop in production?
3. Explain when to use BPDU Guard, Root Guard, and Loop Guard.

---

# Summary

In this lesson, you learned:

- Why switching loops occur
- Broadcast storms
- MAC address instability
- Spanning Tree Protocol
- Root Bridge election
- Port roles
- Port states
- BPDUs
- RSTP
- Linux bridge commands

STP is one of the most important Layer 2 protocols in enterprise networking. It prevents switching loops while preserving redundant links for failover. By electing a Root Bridge, assigning port roles, and blocking unnecessary paths, STP creates a stable, loop-free Ethernet network that supports high availability.

---

## Key Takeaways

- STP prevents **Layer 2 switching loops**.
- **IEEE 802.1D** defines classic STP.
- **IEEE 802.1w** defines Rapid STP (RSTP).
- The **Root Bridge** is the central reference point.
- **BPDUs** are exchanged to build the spanning tree.
- Blocked ports remain available as backup links.
- RSTP provides significantly faster convergence than classic STP.

---

## What's Next?

**[EtherChannel](etherchannel.md)**

In the next lesson, you'll learn about **EtherChannel**.

You'll explore:

- What EtherChannel is
- Link Aggregation
- Load Balancing
- Link Aggregation Control Protocol (LACP)
- Port Aggregation Protocol (PAgP)
- EtherChannel configuration
- High availability with bundled links

By the end of the lesson, you'll understand how multiple physical Ethernet links can be combined into a single logical connection to increase bandwidth and improve redundancy.
