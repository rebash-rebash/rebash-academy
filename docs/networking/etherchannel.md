---
title: "EtherChannel"
description: "Learn EtherChannel and link aggregation — LACP, PAgP, load balancing, redundancy, Port-Channels, and Linux bonding."
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
  - etherchannel
  - lacp
  - bonding
  - switching
  - rebash-networking-mastery
comments: false
status: ready
---

# EtherChannel — Combining Multiple Links for Higher Bandwidth and Redundancy

> **EtherChannel** is a Layer 2 technology that combines multiple physical Ethernet links into a **single logical link**. Instead of using one cable between switches, EtherChannel allows multiple cables to work together, increasing bandwidth while also providing redundancy. If one physical link fails, traffic automatically continues across the remaining links without disrupting network connectivity. EtherChannel is widely used in enterprise networks, data centres, virtualisation platforms, and cloud infrastructure. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand EtherChannel.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 4: Switching → Lesson 7</p>

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

<div markdown>**Lesson:** 7 of 8</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand EtherChannel
- Learn Link Aggregation
- Understand Load Balancing
- Learn Link Aggregation Control Protocol (LACP) and Port Aggregation Protocol (PAgP)
- Understand redundancy
- Learn EtherChannel design
- Configure Linux Bonding

---

# Prerequisites

Complete:

- [Ethernet](ethernet-switching-and-vlans.md)
- [MAC Address Table](mac-address-table.md)
- [Switch Learning](switch-learning.md)
- [VLAN](vlan.md)
- [Trunking](trunking.md)
- [STP](spanning-tree-protocol.md)

---

# Why Learn EtherChannel?

Suppose two switches are connected.

Single cable:

```text
Switch A

↓

1 Gbps

↓

Switch B
```

Bandwidth:

```text
1 Gbps
```

Need more bandwidth?

Adding another cable creates a Layer 2 loop.

```text
Switch A

⇄

Switch B

❌ Loop
```

Spanning Tree Protocol (STP) blocks one link.

Bandwidth remains:

```text
1 Gbps
```

EtherChannel solves this problem.

---

# What is EtherChannel?

EtherChannel combines multiple physical Ethernet links into one logical connection.

Example:

```text
4 × 1 Gbps Links

↓

One Logical Link

↓

4 Gbps Aggregate Bandwidth
```

To higher-layer protocols such as STP, the bundle appears as a single interface.

---

# Benefits of EtherChannel

EtherChannel provides:

- Higher Bandwidth
- Redundancy
- Load Balancing
- Simplified Management
- Fast Failover
- Better Network Utilisation

---

# Without EtherChannel

```text
Switch A

↓

1 Gbps

↓

Switch B
```

Maximum throughput:

```text
1 Gbps
```

Adding extra links:

```text
↓

STP Blocks Them
```

---

# With EtherChannel

```text
Switch A

⇄⇄⇄⇄

Switch B
```

All links become:

```text
One Logical Link
```

No STP blocking occurs **within the EtherChannel bundle** because STP treats the entire bundle as a single logical interface.

---

# Link Aggregation

EtherChannel is also known as:

```text
Link Aggregation
```

Other common terms include:

- Port Channel
- Link Bundle
- Bonded Interface

---

# Logical View

Physical Links:

```text
eth1

eth2

eth3

eth4
```

↓

Logical Interface:

```text
Port-Channel1
```

Applications see one interface rather than multiple separate links.

---

# Load Balancing

EtherChannel distributes traffic across member links using a hashing algorithm.

Traffic may be balanced based on values such as:

- Source MAC
- Destination MAC
- Source IP
- Destination IP
- Layer 4 ports

The exact algorithm depends on the switch vendor and configuration.

---

# Important Note

EtherChannel does **not** split a single network flow across multiple links.

Example:

```text
Single TCP Connection

↓

One Physical Link
```

Multiple independent conversations can be distributed across different member links, increasing aggregate throughput.

---

# Redundancy

Suppose:

```text
4 Links
```

One fails.

Remaining:

```text
3 Links

↓

Still Active
```

Traffic continues without interrupting the logical connection.

---

# EtherChannel Protocols

Two major negotiation protocols exist.

### LACP

```text
IEEE 802.3ad

(now incorporated into IEEE 802.1AX)
```

Features:

- Open Standard
- Multi-vendor Support
- Widely Used

---

### PAgP

```text
Port Aggregation Protocol
```

Features:

- Cisco Proprietary
- Switch-to-Switch Communication
- Used mainly in Cisco environments

---

# LACP Modes

Common LACP modes:

| Mode | Description |
|--------|-------------|
| Active | Actively negotiates LACP |
| Passive | Responds to LACP requests |

Successful negotiation requires at least one side to operate in **Active** mode.

---

# EtherChannel Requirements

Member interfaces should have matching:

- Speed
- Duplex
- VLAN Configuration
- Trunk/Access Mode
- Allowed VLANs (if trunk)
- Maximum Transmission Unit (MTU)

Mismatched settings prevent a successful EtherChannel.

---

# EtherChannel with Trunks

Example:

```text
Switch A

↓

Port-Channel1

↓

Switch B
```

The Port-Channel itself operates as:

```text
802.1Q Trunk
```

All VLANs traverse the aggregated logical link.

---

# STP and EtherChannel

Without EtherChannel:

```text
4 Links

↓

STP Blocks 3
```

With EtherChannel:

```text
4 Links

↓

One Logical Link

↓

No Internal Blocking
```

STP sees only the logical Port-Channel.

---

# Enterprise Example

Core Switch:

```text
Port-Channel1

↓

Distribution Switch
```

Bandwidth:

```text
4 × 10 Gbps

=

40 Gbps Aggregate
```

One cable failure does not interrupt connectivity.

---

# Cloud Perspective

Cloud providers typically abstract physical EtherChannel configuration.

However, similar link aggregation technologies are heavily used within:

- Data Centres
- Hypervisors
- Storage Networks
- Spine-Leaf Fabrics

---

# Kubernetes Perspective

Worker nodes with multiple network interfaces may use Linux bonding or teaming for redundancy and increased throughput.

Example:

```text
Node

↓

bond0

↓

eth0

+

eth1
```

This provides a single resilient logical interface.

---

# Linux Perspective

Display interfaces.

```bash
ip link
```

Display bonding information.

```bash
cat /proc/net/bonding/bond0
```

Create a bond (distribution-specific configuration varies).

Example:

```bash
sudo modprobe bonding
```

Display bond interface.

```bash
ip addr show bond0
```

Modern Linux systems may also use **NetworkManager** or **systemd-networkd** to configure bonded interfaces.

---

# EtherChannel Workflow

```text
Multiple Physical Links

↓

LACP Negotiation

↓

Create Port-Channel

↓

Load Balance Traffic

↓

Automatic Failover
```

---

# Enterprise Topology

```text
Access Switches

↓

Port-Channel

↓

Distribution Switches

↓

Port-Channel

↓

Core Switch
```

High bandwidth and redundancy are achieved simultaneously.

---

# Hands-on Lab

## Task 1

Display interfaces.

```bash
ip link
```

---

## Task 2

If Linux bonding is configured:

```bash
cat /proc/net/bonding/bond0
```

---

## Task 3

Research:

- LACP
- PAgP

Create a comparison table.

---

## Task 4

Draw two switches connected by:

- Four physical cables
- One Port-Channel

---

## Task 5

Explain what happens if one member link fails.

---

## Task 6

List the configuration requirements for EtherChannel.

---

## Task 7

Compare:

- STP
- EtherChannel

Explain how they work together.

---

## Task 8

Research how EtherChannel (or Link Aggregation) is configured on Cisco, Juniper, Aruba, or another enterprise switch platform.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip link` | Display interfaces |
| `ip addr` | Display IP addresses |
| `cat /proc/net/bonding/bond0` | Display bonding information |
| `modprobe bonding` | Load bonding module |

---

# Common Mistakes

❌ Assuming EtherChannel increases the speed of a single connection.

✅ It increases aggregate bandwidth across multiple flows.

---

❌ Mixing interfaces with different speeds.

✅ All member interfaces should match.

---

❌ Forgetting trunk configuration consistency.

✅ Ensure VLAN settings match on all members.

---

❌ Using PAgP in non-Cisco environments.

✅ Prefer LACP for multi-vendor compatibility.

---

❌ Expecting STP to treat each member separately.

✅ STP treats the Port-Channel as one logical link.

---

# Best Practices

- Use **LACP** whenever possible.
- Ensure all member ports have identical configurations.
- Bundle high-speed uplinks between switches.
- Monitor Port-Channel health.
- Document member interfaces.
- Test failover after deployment.

---

# Interview Questions

## Beginner

1. What is EtherChannel?
2. Why is EtherChannel used?
3. What is Link Aggregation?
4. What is LACP?

---

## Intermediate

1. Compare LACP and PAgP.
2. How does EtherChannel improve bandwidth?
3. How does EtherChannel interact with STP?
4. Why must all member links have matching configurations?

---

## Architect Level

1. Design an enterprise core network using EtherChannel.
2. Explain load balancing in EtherChannel.
3. How would you troubleshoot an EtherChannel that fails to form?

---

# Summary

In this lesson, you learned:

- EtherChannel
- Link Aggregation
- Port Channels
- Load Balancing
- LACP
- PAgP
- Redundancy
- Linux Bonding
- Enterprise EtherChannel design

EtherChannel combines multiple physical Ethernet links into one logical interface, providing increased aggregate bandwidth, redundancy, and simplified management. By working alongside STP, EtherChannel allows organisations to utilise multiple physical links efficiently without creating Layer 2 loops.

---

## Key Takeaways

- EtherChannel combines multiple physical links into **one logical interface**.
- **LACP (IEEE 802.1AX)** is the preferred standards-based negotiation protocol.
- PAgP is Cisco proprietary.
- EtherChannel provides redundancy and aggregate bandwidth.
- A single traffic flow typically uses one member link; multiple flows are distributed across the bundle.
- STP treats an EtherChannel as a single logical connection.

---

## What's Next?

**[Inter-VLAN Routing](inter-vlan-routing.md)**

In the next lesson, you'll learn about **Inter-VLAN Routing**.

You'll explore:

- Why Inter-VLAN Routing is required
- Router-on-a-Stick
- Layer 3 Switches
- Switched Virtual Interfaces (SVIs)
- Default Gateways for VLANs
- Packet flow between VLANs
- Enterprise routing design

By the end of the lesson, you'll understand how devices in different VLANs communicate securely and efficiently using Layer 3 routing.
