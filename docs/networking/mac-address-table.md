---
title: "MAC Address Table"
description: "Learn how Ethernet switches use the MAC Address Table (CAM table) — learning, aging, unknown unicast flooding, and frame forwarding decisions."
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
  - mac-address
  - cam
  - rebash-networking-mastery
comments: false
status: ready
---

# MAC Address Table — How Switches Learn and Forward Ethernet Frames

> An **Ethernet Switch** intelligently forwards frames by maintaining a **MAC Address Table** (also called the **CAM Table** or **Forwarding Table**). Instead of sending every frame to every device, the switch learns which Media Access Control (MAC) addresses are connected to each port and forwards frames only to the correct destination. This improves performance, reduces unnecessary traffic, and enables efficient communication within a Local Area Network (LAN). Understanding the MAC Address Table is fundamental for Linux administrators, DevOps engineers, Cloud Architects, Platform Engineers, Site Reliability Engineers (SREs), and Network Engineers.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 4: Switching → Lesson 2</p>

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

<div markdown>**Lesson:** 2 of 8</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the MAC Address Table
- Learn how switches store MAC addresses
- Understand dynamic and static MAC entries
- Learn MAC address aging
- Understand unknown unicast forwarding
- Learn frame forwarding decisions
- Troubleshoot MAC table issues

---

# Prerequisites

Complete:

- [Ethernet](ethernet-switching-and-vlans.md)

---

# Why Learn MAC Address Tables?

Suppose three computers are connected to a switch.

```text
PC1

↓

Switch

↓

PC2

↓

PC3
```

When PC1 sends data to PC2:

How does the switch know where PC2 is connected?

The answer is:

```text
MAC Address Table
```

---

# What is a MAC Address Table?

A **MAC Address Table** is a database maintained by a switch that maps:

```text
MAC Address

↓

Switch Port
```

Example:

| MAC Address | Port |
|-------------|------|
| AA:AA:AA:AA:AA:01 | Port 1 |
| BB:BB:BB:BB:BB:02 | Port 2 |
| CC:CC:CC:CC:CC:03 | Port 3 |

This allows the switch to forward frames efficiently.

---

# Why is it Needed?

Without a MAC table:

```text
Every Frame

↓

Every Port
```

This would create unnecessary traffic.

With a MAC table:

```text
Frame

↓

Correct Port Only
```

Much more efficient.

---

# MAC Address Learning

Switches automatically learn MAC addresses by examining the **Source MAC Address** of every incoming Ethernet frame.

Process:

```text
Receive Frame

↓

Read Source MAC

↓

Record Port

↓

Update Table
```

No manual configuration is required.

---

# Learning Example

PC1 sends a frame.

Source MAC:

```text
AA:AA:AA:AA:AA:01
```

Received on:

```text
Port 1
```

Switch stores:

| MAC Address | Port |
|-------------|------|
| AA:AA:AA:AA:AA:01 | Port 1 |

---

# Second Device

PC2 sends a frame.

Source MAC:

```text
BB:BB:BB:BB:BB:02
```

Received on:

```text
Port 2
```

Updated table:

| MAC Address | Port |
|-------------|------|
| AA:AA:AA:AA:AA:01 | Port 1 |
| BB:BB:BB:BB:BB:02 | Port 2 |

---

# Third Device

PC3 sends a frame.

Source:

```text
CC:CC:CC:CC:CC:03
```

Received on:

```text
Port 3
```

Table becomes:

| MAC Address | Port |
|-------------|------|
| AA:AA:AA:AA:AA:01 | Port 1 |
| BB:BB:BB:BB:BB:02 | Port 2 |
| CC:CC:CC:CC:CC:03 | Port 3 |

---

# Forwarding Process

Suppose:

PC1 sends data to:

```text
BB:BB:BB:BB:BB:02
```

Switch searches:

```text
MAC Table
```

Finds:

```text
Port 2
```

Result:

```text
Forward

↓

Port 2 Only
```

---

# Unknown Unicast

Suppose destination MAC is:

```text
DD:DD:DD:DD:DD:04
```

Not found in the table.

Switch performs:

```text
Flood

↓

All Ports

↓

Except Incoming Port
```

Once the destination replies, the switch learns its MAC address.

---

# Broadcast Frames

Broadcast destination:

```text
FF:FF:FF:FF:FF:FF
```

Switch behaviour:

```text
Forward

↓

All Ports

↓

Except Incoming Port
```

Broadcast traffic remains within the same Virtual Local Area Network (VLAN).

---

# Multicast Frames

Multicast destination:

```text
01:00:5E:...
```

Depending on switch capabilities and multicast configuration, frames may:

- Be flooded within the VLAN
- Be forwarded selectively using multicast snooping (such as Internet Group Management Protocol (IGMP) Snooping)

---

# Dynamic MAC Entries

Most MAC table entries are:

```text
Dynamic
```

Characteristics:

- Learned automatically
- Removed after inactivity
- Updated automatically

---

# Static MAC Entries

Administrators can manually configure:

```text
Static MAC Entries
```

Characteristics:

- Never age out
- Fixed to specific ports
- Useful for security or specialised deployments

---

# MAC Address Aging

Switches remove inactive entries after an aging timer expires.

Example:

```text
No Traffic

↓

Aging Timer Expires

↓

Entry Removed
```

Many enterprise switches use a default aging time of approximately **300 seconds (5 minutes)**, although this is configurable and may vary by vendor.

---

# MAC Table Workflow

```text
Receive Frame

↓

Read Source MAC

↓

Update MAC Table

↓

Lookup Destination MAC

↓

Known?

↓

Yes

↓

Forward to Specific Port

↓

No

↓

Flood Frame
```

---

# CAM Table

The MAC Address Table is often stored in specialised hardware called:

```text
CAM

(Content Addressable Memory)
```

Benefits:

- Extremely fast lookups
- High forwarding performance
- Wire-speed switching

---

# Enterprise Example

Office Network:

```text
Employee Laptop

↓

Switch

↓

Server
```

Switch learns:

```text
Laptop MAC

↓

Port 5
```

```text
Server MAC

↓

Port 12
```

Future traffic is forwarded directly.

---

# Cloud Perspective

Although cloud networks are virtualised, virtual switches (vSwitches) also maintain MAC forwarding tables to deliver traffic between virtual machines and containers efficiently.

---

# Kubernetes Perspective

Worker nodes communicate through virtual and physical switches.

MAC tables help deliver traffic between:

- Nodes
- Virtual Machines
- Physical Switches

Overlay networking solutions still rely on underlying Ethernet switching.

---

# Linux Perspective

Display MAC address.

```bash
ip link
```

Example:

```text
link/ether

00:11:22:33:44:55
```

Display neighbour cache (Layer 3 to Layer 2 mapping).

```bash
ip neigh
```

While Linux hosts do not maintain a switch MAC table, they maintain Address Resolution Protocol (ARP) (IPv4) or Neighbor Discovery (IPv6) caches for address resolution.

---

# MAC Table Example

| MAC Address | VLAN | Port | Type |
|-------------|------|------|------|
| AA:AA:AA:AA:AA:01 | 10 | Port 1 | Dynamic |
| BB:BB:BB:BB:BB:02 | 10 | Port 2 | Dynamic |
| CC:CC:CC:CC:CC:03 | 20 | Port 5 | Static |

Enterprise switches typically maintain separate MAC tables for each VLAN.

---

# Hands-on Lab

## Task 1

Display your Linux MAC address.

```bash
ip link
```

---

## Task 2

Display the ARP/Neighbor cache.

```bash
ip neigh
```

---

## Task 3

Draw a switch connected to four computers.

Show how the MAC Address Table is populated as each computer sends its first frame.

---

## Task 4

Explain what happens when a switch receives a frame with an unknown destination MAC address.

---

## Task 5

Research the default MAC aging timer used by your preferred switch vendor.

---

## Task 6

Create a table showing:

- MAC Address
- Port
- VLAN
- Entry Type

---

## Task 7

Explain the difference between:

- Dynamic MAC Entries
- Static MAC Entries

---

## Task 8

Research how virtual switches in VMware, Hyper-V, or cloud platforms maintain MAC forwarding information.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip link` | Display MAC addresses |
| `ip neigh` | Display ARP/Neighbor cache |
| `hostname` | Display hostname |
| `ip addr` | Display IP and MAC information |

---

# Common Mistakes

❌ Confusing the MAC table with the ARP table.

✅ MAC tables exist on switches; ARP/Neighbor caches exist on hosts.

---

❌ Assuming switches know all MAC addresses immediately.

✅ Switches learn MAC addresses dynamically from incoming frames.

---

❌ Forgetting MAC entries age out.

✅ Understand aging timers and dynamic learning.

---

❌ Assuming broadcasts use the MAC table.

✅ Broadcasts are flooded to all ports within the VLAN.

---

❌ Ignoring VLAN separation.

✅ MAC tables are maintained separately for each VLAN on managed switches.

---

# Best Practices

- Allow switches to learn MAC addresses dynamically unless static entries are required.
- Monitor MAC table size in large networks.
- Use static MAC entries only when necessary.
- Configure appropriate MAC aging timers.
- Secure switch ports against unauthorised devices using features such as Port Security.
- Document important static MAC assignments.

---

# Interview Questions

## Beginner

1. What is a MAC Address Table?
2. How does a switch learn MAC addresses?
3. What is a dynamic MAC entry?
4. What happens when the destination MAC is unknown?

---

## Intermediate

1. Explain MAC address learning.
2. What is the purpose of the aging timer?
3. Compare dynamic and static MAC entries.
4. What is CAM memory?

---

## Architect Level

1. How would you troubleshoot incorrect MAC learning in a production network?
2. Why do enterprise switches maintain separate MAC tables for VLANs?
3. How do virtual switches implement MAC forwarding?

---

# Summary

In this lesson, you learned:

- What a MAC Address Table is
- MAC address learning
- Frame forwarding
- Unknown unicast flooding
- Broadcast forwarding
- Dynamic and static MAC entries
- MAC aging
- CAM memory
- Linux MAC-related commands

The MAC Address Table is the intelligence behind Ethernet switching. By learning source MAC addresses and mapping them to switch ports, switches can forward frames efficiently, reduce unnecessary traffic, and provide high-performance communication across local networks.

---

## Key Takeaways

- Switches build MAC Address Tables automatically.
- Source MAC addresses are used for learning.
- Destination MAC addresses determine forwarding.
- Unknown destination MAC addresses are flooded.
- Dynamic MAC entries age out after inactivity.
- CAM memory enables high-speed MAC lookups.
- Managed switches maintain MAC tables separately for each VLAN.

---

## What's Next?

**[Switch Learning](switch-learning.md)**

In the next lesson, you'll learn about **Switch Learning**.

You'll explore:

- The switch learning process
- Learning, Flooding, and Forwarding
- Frame processing lifecycle
- Unknown unicast behaviour
- Broadcast forwarding
- MAC table updates
- Real-world switching examples

By the end of the lesson, you'll understand exactly how an Ethernet switch learns device locations and makes forwarding decisions in real time.
