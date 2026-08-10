---
title: "VLAN"
description: "Learn Virtual Local Area Networks (VLANs) — broadcast domains, VLAN IDs, access ports, isolation, enterprise design, and Linux VLAN interfaces."
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
  - vlan
  - switching
  - ethernet
  - segmentation
  - rebash-networking-mastery
comments: false
status: ready
---

# VLAN (Virtual Local Area Network) — Segmenting Networks for Security and Efficiency

> A **VLAN (Virtual Local Area Network)** is a logical method of dividing a physical network into multiple isolated broadcast domains. Instead of requiring separate physical switches for different departments, VLANs allow a single managed switch to create multiple virtual networks. VLANs improve **security**, **performance**, **network management**, and **scalability**, making them a fundamental technology in enterprise networking, cloud infrastructure, and modern data centres. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand VLANs.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 4: Switching → Lesson 4</p>

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

<div markdown>**Lesson:** 4 of 8</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand VLANs
- Learn why VLANs are used
- Understand broadcast domains
- Learn VLAN IDs
- Configure Access Ports
- Understand VLAN communication
- Design enterprise VLAN architectures

---

# Prerequisites

Complete:

- [Ethernet](ethernet-switching-and-vlans.md)
- [MAC Address Table](mac-address-table.md)
- [Switch Learning](switch-learning.md)

---

# Why Learn VLANs?

Imagine a company with three departments:

- HR
- Finance
- Engineering

All employees are connected to the same switch.

```text
HR

↓

Switch

↓

Finance

↓

Engineering
```

Without VLANs:

- Everyone belongs to the same network.
- Broadcast traffic reaches every device.
- Security is limited.

VLANs solve these problems.

---

# What is a VLAN?

A **Virtual Local Area Network (VLAN)** is a logical grouping of devices that creates separate Layer 2 networks on the same physical switch.

Instead of one large network:

```text
One Switch

↓

One Network
```

We can create:

```text
One Switch

↓

Multiple Virtual Networks
```

---

# VLAN Example

One switch:

```text
24 Ports
```

Configured as:

```text
Ports 1–8

↓

VLAN 10 (HR)
```

```text
Ports 9–16

↓

VLAN 20 (Finance)
```

```text
Ports 17–24

↓

VLAN 30 (Engineering)
```

Although physically connected to the same switch, each department is isolated.

---

# Broadcast Domain

Without VLANs:

```text
Broadcast

↓

Entire Switch
```

Every device receives the broadcast frame.

With VLANs:

```text
Broadcast

↓

Only Same VLAN
```

Each VLAN is its own **broadcast domain**.

---

# VLAN Isolation

Example:

HR Computer:

```text
VLAN 10
```

Finance Computer:

```text
VLAN 20
```

Can they communicate directly?

```text
No
```

Layer 2 communication is isolated between VLANs.

Inter-VLAN communication requires a Layer 3 device, which you'll learn later in this module.

---

# VLAN IDs

Each VLAN is identified by a **VLAN ID (VID)**.

Valid VLAN IDs:

```text
1–4094
```

Examples:

| VLAN ID | Department |
|----------|------------|
| 10 | HR |
| 20 | Finance |
| 30 | Engineering |
| 40 | Servers |
| 50 | Management |

---

# Default VLAN

By default, switch ports belong to:

```text
VLAN 1
```

Best practice:

Avoid using VLAN 1 for production user traffic whenever possible.

Create dedicated VLANs instead.

---

# Access Ports

An **Access Port** belongs to **one VLAN only**.

Example:

```text
PC

↓

Access Port

↓

VLAN 10
```

Frames entering an access port are associated with that VLAN.

---

# VLAN Membership

Example:

| Device | VLAN |
|---------|------|
| HR Laptop | VLAN 10 |
| HR Printer | VLAN 10 |
| Finance PC | VLAN 20 |
| Database Server | VLAN 40 |

Devices communicate freely within the same VLAN.

---

# VLAN Communication

Within the same VLAN:

```text
PC1

↓

Switch

↓

PC2

✔ Allowed
```

Different VLANs:

```text
VLAN 10

↓

VLAN 20

❌ Blocked
```

A router or Layer 3 switch is required for communication between VLANs.

---

# Benefits of VLANs

VLANs provide:

- Better Security
- Reduced Broadcast Traffic
- Easier Network Management
- Logical Network Separation
- Improved Scalability
- Better Performance

---

# Security Benefits

Example:

Guest Network:

```text
VLAN 100
```

Internal Servers:

```text
VLAN 40
```

Guests cannot directly access internal servers without routing policies.

---

# Enterprise Example

Company:

```text
HR

↓

VLAN 10
```

```text
Finance

↓

VLAN 20
```

```text
Engineering

↓

VLAN 30
```

```text
Servers

↓

VLAN 40
```

```text
Management

↓

VLAN 50
```

Each department operates within its own logical network.

---

# Cloud Perspective

Although cloud providers do not usually expose traditional VLAN configuration to customers, similar concepts exist through:

- Virtual Networks (VNets)
- Virtual Private Clouds (VPCs)
- Subnets
- Network Segmentation

These technologies provide logical isolation similar to VLANs.

---

# Kubernetes Perspective

Kubernetes itself does not use VLANs internally, but Kubernetes worker nodes often connect to physical networks that use VLANs.

Example:

```text
Worker Nodes

↓

VLAN 30
```

```text
Storage Network

↓

VLAN 40
```

```text
Management Network

↓

VLAN 50
```

Separating traffic improves security and operational efficiency.

---

# Linux Perspective

Display network interfaces.

```bash
ip link
```

Display VLAN interfaces (if configured).

```bash
ip -d link
```

Create a VLAN interface (example).

```bash
sudo ip link add link eth0 name eth0.10 type vlan id 10
```

Bring the interface up.

```bash
sudo ip link set eth0.10 up
```

Assign an IP address.

```bash
sudo ip addr add 192.168.10.10/24 dev eth0.10
```

Replace `eth0` with your actual interface name if necessary.

---

# VLAN Communication Diagram

```text
HR PC

↓

VLAN 10

↓

Switch

↓

HR Printer

✔ Communication
```

---

```text
HR PC

↓

VLAN 10

↓

Finance PC

↓

VLAN 20

❌ No Communication
```

---

# VLAN Workflow

```text
Frame Arrives

↓

Access Port

↓

Assign VLAN

↓

Switch Looks Up MAC Table

↓

Forward Only Within Same VLAN
```

---

# VLAN Best Practices

- Create separate VLANs for departments.
- Separate servers from user devices.
- Isolate guest networks.
- Use dedicated management VLANs.
- Document VLAN IDs consistently.
- Avoid unnecessary use of the default VLAN.

---

# Hands-on Lab

## Task 1

Display Linux interfaces.

```bash
ip link
```

---

## Task 2

Check whether VLAN interfaces exist.

```bash
ip -d link
```

---

## Task 3

Create VLAN 10.

```bash
sudo ip link add link eth0 name eth0.10 type vlan id 10
```

---

## Task 4

Bring VLAN online.

```bash
sudo ip link set eth0.10 up
```

---

## Task 5

Assign an IP address.

```bash
sudo ip addr add 192.168.10.10/24 dev eth0.10
```

---

## Task 6

Draw a company network with:

- HR
- Finance
- Engineering
- Servers
- Management

Assign VLAN IDs for each department.

---

## Task 7

Explain why VLANs reduce broadcast traffic.

---

## Task 8

Research how VLANs are implemented on your preferred switch vendor (Cisco, Juniper, Aruba, MikroTik, etc.).

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip link` | Display interfaces |
| `ip -d link` | Display VLAN information |
| `ip addr` | Display IP configuration |
| `ip link add` | Create VLAN interface |
| `ip link set` | Enable VLAN interface |

---

# Common Mistakes

❌ Assuming VLANs are physical networks.

✅ VLANs are logical Layer 2 networks.

---

❌ Believing devices in different VLANs can communicate directly.

✅ Inter-VLAN routing is required.

---

❌ Using VLAN 1 for everything.

✅ Create dedicated VLANs for production traffic.

---

❌ Forgetting to assign ports to the correct VLAN.

✅ Verify switch port configuration.

---

❌ Mixing user, server, and management devices in the same VLAN.

✅ Separate networks based on function and security requirements.

---

# Best Practices

- Assign meaningful VLAN IDs.
- Separate departments into different VLANs.
- Use dedicated management VLANs.
- Isolate guest and production traffic.
- Document VLAN assignments.
- Review VLAN design as the organisation grows.

---

# Interview Questions

## Beginner

1. What is a VLAN?
2. Why are VLANs used?
3. What is an Access Port?
4. What is a Broadcast Domain?

---

## Intermediate

1. Explain VLAN isolation.
2. Why can't devices in different VLANs communicate directly?
3. What is the default VLAN?
4. What are the advantages of VLANs?

---

## Architect Level

1. Design a VLAN architecture for a 500-user enterprise.
2. How would you separate production, management, storage, and guest traffic?
3. Explain VLAN implementation in virtualised environments.

---

# Summary

In this lesson, you learned:

- What VLANs are
- VLAN IDs
- Broadcast domains
- Access Ports
- VLAN isolation
- VLAN communication
- Enterprise VLAN design
- Linux VLAN interfaces

VLANs allow a single physical switch to operate as multiple logical networks. They improve security, reduce broadcast traffic, simplify management, and provide scalable network segmentation for enterprise, cloud, and data centre environments.

---

## Key Takeaways

- VLANs create **logical Layer 2 networks**.
- Each VLAN is a separate **broadcast domain**.
- Access ports belong to **one VLAN**.
- Devices in different VLANs require **Inter-VLAN Routing** to communicate.
- VLANs improve security, scalability, and network performance.
- Proper VLAN design is a cornerstone of enterprise networking.

---

## What's Next?

**[Trunking](trunking.md)**

In the next lesson, you'll learn about **Trunking**.

You'll explore:

- What a Trunk Port is
- IEEE 802.1Q VLAN tagging
- Native VLAN
- Tagged vs Untagged frames
- Trunk links between switches
- VLAN transport across multiple switches
- Linux VLAN trunk concepts

By the end of the lesson, you'll understand how multiple VLANs are carried across a single physical link, enabling scalable enterprise network designs.
