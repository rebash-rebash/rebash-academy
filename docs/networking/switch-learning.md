---
title: "Switch Learning"
description: "Learn how Ethernet switches learn, flood, and forward frames — Learn → Lookup → Forward, unknown unicast, broadcast, and MAC table updates."
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
  - rebash-networking-mastery
comments: false
status: ready
---

# Switch Learning — How Ethernet Switches Learn, Flood, and Forward Frames

> An **Ethernet Switch** is an intelligent Layer 2 device that automatically learns where devices are connected by examining the **Source MAC Address** of incoming Ethernet frames. This process is called **Switch Learning**. Every frame received by a switch follows a simple workflow: **Learn → Lookup → Forward (or Flood)**. This learning mechanism allows switches to build their MAC Address Tables dynamically and efficiently deliver traffic only to the correct destination. Understanding Switch Learning is essential for Linux administrators, DevOps engineers, Cloud Architects, Platform Engineers, Site Reliability Engineers (SREs), and Network Engineers.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 4: Switching → Lesson 3</p>

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

<div markdown>**Lesson:** 3 of 8</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Switch Learning
- Learn the Learn → Lookup → Forward process
- Understand frame forwarding decisions
- Learn flooding behaviour
- Understand unknown unicast forwarding
- Learn MAC table updates
- Troubleshoot switching behaviour

---

# Prerequisites

Complete:

- [Ethernet](ethernet-switching-and-vlans.md)
- [MAC Address Table](mac-address-table.md)

---

# Why Learn Switch Learning?

Suppose a switch has just been powered on.

Its MAC Address Table is empty.

```text
MAC Table

↓

Empty
```

Now three computers connect to the switch.

How does the switch learn where each computer is connected?

The answer is:

```text
Switch Learning
```

---

# What is Switch Learning?

Switch Learning is the automatic process where an Ethernet switch learns:

```text
Source MAC Address

↓

Incoming Port
```

Every incoming frame teaches the switch something new.

---

# The Three-Step Process

Every Ethernet frame follows the same workflow.

```text
Learn

↓

Lookup

↓

Forward
```

This happens for every frame received by the switch.

---

# Step 1 — Learn

The switch receives an Ethernet frame.

Example:

```text
Source MAC

AA:AA:AA:AA:AA:01
```

Received on:

```text
Port 1
```

The switch stores:

| MAC Address | Port |
|-------------|------|
| AA:AA:AA:AA:AA:01 | Port 1 |

---

# Step 2 — Lookup

The switch examines:

```text
Destination MAC
```

Example:

```text
BB:BB:BB:BB:BB:02
```

The switch searches the MAC Address Table.

---

# Step 3A — Forward

If the destination MAC exists:

```text
MAC Found

↓

Port 2
```

The frame is sent only through:

```text
Port 2
```

No other devices receive the frame.

---

# Step 3B — Flood

If the destination MAC is **not** in the table:

```text
Unknown Destination
```

The switch performs:

```text
Flood

↓

All Ports

↓

Except Incoming Port
```

This is called **Unknown Unicast Flooding**.

---

# Learning Example

Initial MAC Table:

```text
Empty
```

---

PC1 sends a frame.

```text
Source

AA:AA:AA:AA:AA:01
```

Switch learns:

| MAC | Port |
|------|------|
| AA:AA:AA:AA:AA:01 | 1 |

---

PC2 replies.

```text
Source

BB:BB:BB:BB:BB:02
```

Updated table:

| MAC | Port |
|------|------|
| AA:AA:AA:AA:AA:01 | 1 |
| BB:BB:BB:BB:BB:02 | 2 |

Now future communication is forwarded directly.

---

# Complete Example

```text
PC1

↓

Switch

↓

PC2
```

Frame arrives:

```text
Source

AA

Destination

BB
```

Switch:

```text
Learn AA

↓

Lookup BB

↓

Known?

↓

No

↓

Flood
```

---

PC2 responds.

```text
Source

BB

Destination

AA
```

Switch:

```text
Learn BB

↓

Lookup AA

↓

Known

↓

Forward
```

Now both devices are fully learned.

---

# Learning Workflow

```text
Receive Frame

↓

Read Source MAC

↓

Update MAC Table

↓

Read Destination MAC

↓

Search Table

↓

Found?

↓

Yes

↓

Forward

↓

No

↓

Flood
```

---

# Broadcast Frames

Destination:

```text
FF:FF:FF:FF:FF:FF
```

Switch action:

```text
Forward

↓

Every Port

↓

Except Incoming Port
```

Broadcast frames are never looked up in the MAC table because they are intended for all devices within the Virtual Local Area Network (VLAN).

---

# Multicast Frames

Destination:

```text
01:00:5E...

or

33:33...
```

Behaviour depends on switch capabilities.

Basic switches may flood multicast traffic.

Managed switches often use:

- Internet Group Management Protocol (IGMP) Snooping (IPv4)
- Multicast Listener Discovery (MLD) Snooping (IPv6)

to forward multicast only where needed.

---

# Unknown Unicast

Example:

```text
Destination

DD:DD:DD:DD:DD:04
```

Not in table.

Switch:

```text
Flood
```

Once the destination replies:

```text
Learn

↓

Update Table
```

Future traffic is forwarded directly.

---

# MAC Address Move

Suppose a computer is unplugged from Port 2 and connected to Port 5.

When the switch receives a frame from the new port:

```text
MAC Address

↓

Move Entry

↓

Update Port
```

The MAC table is automatically updated.

---

# MAC Aging

If no traffic is received for a period of time:

```text
Entry

↓

Age Timer

↓

Expired

↓

Remove Entry
```

This keeps the MAC table accurate.

---

# Learning Timeline

```text
Switch Starts

↓

MAC Table Empty

↓

PC Sends Frame

↓

Learn MAC

↓

Destination Unknown

↓

Flood

↓

Reply Received

↓

Learn Destination

↓

Future Frames

↓

Forward Directly
```

---

# Enterprise Example

Office Network:

```text
Laptop

↓

Switch

↓

File Server
```

The first communication teaches the switch both MAC addresses.

Subsequent communication:

```text
Direct Forwarding
```

No unnecessary flooding occurs.

---

# Cloud Perspective

Virtual switches inside hypervisors also perform MAC learning.

Examples:

- VMware vSwitch
- Hyper-V Virtual Switch
- Open vSwitch (OVS)

These virtual switches dynamically learn virtual machine MAC addresses just like physical switches.

---

# Kubernetes Perspective

Container networking solutions rely on virtual switching technologies.

Worker Nodes:

```text
Pod

↓

Virtual Switch

↓

Physical Switch
```

MAC learning enables efficient communication between workloads.

---

# Linux Perspective

Display MAC address.

```bash
ip link
```

Display neighbour cache.

```bash
ip neigh
```

Capture Ethernet frames.

```bash
sudo tcpdump -i <interface> -e
```

The `-e` option displays Ethernet headers, including source and destination MAC addresses.

---

# Frame Processing Diagram

```text
Ethernet Frame

↓

Read Source MAC

↓

Update MAC Table

↓

Read Destination MAC

↓

Known?

↓

Forward

OR

Flood
```

---

# Hands-on Lab

## Task 1

Display your MAC address.

```bash
ip link
```

---

## Task 2

Display the neighbour cache.

```bash
ip neigh
```

---

## Task 3

Capture Ethernet frames.

```bash
sudo tcpdump -i <interface> -e
```

Observe the Source and Destination MAC addresses.

---

## Task 4

Draw the complete Switch Learning process from receiving a frame to forwarding it.

---

## Task 5

Explain what happens when:

- MAC is known
- MAC is unknown
- Broadcast frame arrives

---

## Task 6

Create a MAC table after four computers send frames to a switch.

---

## Task 7

Research MAC address aging on a managed switch.

---

## Task 8

Compare:

- Hub
- Switch
- Managed Switch

Explain how learning behaviour differs.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip link` | Display MAC addresses |
| `ip neigh` | Display ARP/Neighbor cache |
| `tcpdump -e` | Capture Ethernet headers |
| `hostname` | Display hostname |

---

# Common Mistakes

❌ Thinking switches know every MAC address immediately.

✅ Switches learn dynamically from incoming frames.

---

❌ Confusing flooding with broadcasting.

✅ Unknown unicast flooding and broadcast forwarding are different behaviours.

---

❌ Assuming MAC entries never change.

✅ Switches update entries when devices move or age out.

---

❌ Forgetting MAC aging.

✅ Dynamic entries are removed after inactivity.

---

❌ Assuming virtual switches behave differently.

✅ Virtual switches follow the same learning principles.

---

# Best Practices

- Allow switches to learn MAC addresses dynamically.
- Monitor excessive flooding, which may indicate network issues.
- Verify MAC table entries during troubleshooting.
- Understand MAC aging timers.
- Secure switch ports using features like Port Security where appropriate.
- Document important static MAC assignments.

---

# Interview Questions

## Beginner

1. What is Switch Learning?
2. How does a switch learn MAC addresses?
3. What happens when the destination MAC is unknown?
4. What is the first thing a switch does after receiving a frame?

---

## Intermediate

1. Explain the Learn → Lookup → Forward process.
2. What is Unknown Unicast Flooding?
3. How does MAC address aging work?
4. What happens when a device changes switch ports?

---

## Architect Level

1. How would you troubleshoot excessive unknown unicast flooding?
2. Explain MAC learning in virtual switches.
3. How does switch learning improve network performance?

---

# Summary

In this lesson, you learned:

- Switch Learning
- Learn → Lookup → Forward workflow
- Unknown unicast flooding
- Broadcast forwarding
- MAC address updates
- MAC address movement
- MAC aging
- Linux tools for observing Layer 2 behaviour

Switch Learning is the core intelligence behind Ethernet switching. Every incoming frame helps the switch build and maintain its MAC Address Table. As the table becomes populated, switches forward traffic directly to the correct destination, minimising unnecessary traffic and maximising network performance.

---

## Key Takeaways

- Switches learn MAC addresses from the **Source MAC** field.
- Every frame follows the **Learn → Lookup → Forward** process.
- Unknown destinations are flooded within the VLAN.
- Broadcast frames are sent to all ports except the incoming port.
- MAC tables automatically update when devices move.
- Dynamic MAC entries age out after inactivity.

---

## What's Next?

**[VLAN](vlan.md)**

In the next lesson, you'll learn about **VLAN (Virtual Local Area Network)**.

You'll explore:

- What VLANs are
- Why VLANs are used
- VLAN IDs
- Access Ports
- Broadcast Domains
- VLAN segmentation
- Enterprise VLAN design

By the end of the lesson, you'll understand how VLANs logically divide a single physical switch into multiple isolated networks, improving security, scalability, and network performance.
