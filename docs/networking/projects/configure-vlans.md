---
title: "Capstone Project 2 — Configure VLANs"
description: "Build a production-style segmented network with VLANs — access/trunk ports, Router-on-a-Stick, inter-VLAN routing, security, and validation."
difficulty: advanced
estimated_time: "5–8 hours"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 15 · Capstone Projects"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - capstone
  - vlan
  - switching
  - production
  - rebash-networking-mastery
comments: false
status: ready
---

# Capstone Project 2 — Configure VLANs

> In this capstone project, you'll build a **production-style segmented network** using **Virtual Local Area Networks (VLANs)**. You'll divide a single physical network into multiple logical networks, configure trunk and access ports, enable inter-VLAN routing, and implement basic security controls. VLANs are widely used in enterprises to improve **security, performance, scalability, and network management**. Every Network Engineer, DevOps Engineer, Platform Engineer, Cloud Engineer, and System Administrator should know how to design and configure VLANs.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 15: Capstone Projects → Project 2</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Advanced</div>

<div markdown>**Estimated Completion Time:** 5–8 Hours</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Capstone Projects</div>

<div markdown>**Project:** 2 of 8</div>

</div>

</div>

---


# Project Objectives

By completing this project, you'll be able to:

- Design a VLAN-based enterprise network
- Configure VLANs on managed switches
- Configure access and trunk ports
- Enable inter-VLAN routing
- Verify VLAN communication
- Implement VLAN security
- Troubleshoot VLAN issues

---

# Skills Covered

This project integrates concepts from:

- Ethernet Switching
- VLANs
- IEEE 802.1Q
- Trunking
- Access Ports
- Routing
- DHCP
- DNS
- Linux Networking
- Network Troubleshooting

---

# Project Scenario

Your company has one large flat network.

Problems:

- Too much broadcast traffic
- Poor security
- Difficult management
- No department isolation

Your task is to divide the network into multiple VLANs.

---

# Enterprise Network Design

```text
                Router
                   │
             Trunk Connection
                   │
          Managed Layer-2 Switch
 ┌──────────┬──────────┬──────────┬──────────┐
 │          │          │          │
VLAN10    VLAN20    VLAN30    VLAN40
Users     Servers   DevOps    Guest
```

Each department receives its own isolated network.

---

# Lab Requirements

Hardware:

- Managed Switch (or Virtual Switch)
- Linux Router (Optional)
- Multiple Virtual Machines

Software:

- Ubuntu Server
- VirtualBox / VMware / Proxmox
- Docker (Optional)

---

# VLAN Design

| VLAN ID | Name | Network |
|---------|------|---------|
| 10 | Users | 192.168.10.0/24 |
| 20 | Servers | 192.168.20.0/24 |
| 30 | DevOps | 192.168.30.0/24 |
| 40 | Guest | 192.168.40.0/24 |
| 99 | Management | 192.168.99.0/24 |

---

# Network Diagram

```text
                Router
                   │
               Trunk Port
                   │
          Managed Switch
     ┌──────┬──────┬──────┐
     │      │      │
 VLAN10  VLAN20  VLAN30
```

---

# Step 1 — Create VLANs

Create:

```text
VLAN 10

Users
```

```text
VLAN 20

Servers
```

```text
VLAN 30

DevOps
```

```text
VLAN 40

Guest
```

```text
VLAN 99

Management
```

Verify VLAN creation.

---

# Step 2 — Configure Access Ports

Example:

| Port | VLAN |
|------|------|
| 1 | VLAN10 |
| 2 | VLAN10 |
| 3 | VLAN20 |
| 4 | VLAN20 |
| 5 | VLAN30 |
| 6 | VLAN40 |

Devices connected to an access port belong to a single VLAN.

---

# Step 3 — Configure Trunk Port

Configure the uplink as:

```text
802.1Q

Trunk
```

Allow:

- VLAN10
- VLAN20
- VLAN30
- VLAN40
- VLAN99

The trunk carries traffic for multiple VLANs.

---

# Step 4 — Configure Router-on-a-Stick

One physical interface:

```text
eth0
```

Subinterfaces:

```text
eth0.10
```

```text
eth0.20
```

```text
eth0.30
```

```text
eth0.40
```

Each subinterface acts as the gateway for its VLAN.

---

# Step 5 — Configure IP Addresses

Example:

| VLAN | Gateway |
|------|---------|
| 10 | 192.168.10.1 |
| 20 | 192.168.20.1 |
| 30 | 192.168.30.1 |
| 40 | 192.168.40.1 |
| 99 | 192.168.99.1 |

---

# Step 6 — Configure Client Systems

Example:

```text
PC1

192.168.10.10
```

```text
Server1

192.168.20.20
```

```text
DevOps VM

192.168.30.10
```

Verify each device belongs to the correct VLAN.

---

# Step 7 — Enable Inter-VLAN Routing

Verify:

```text
Users

↓

Servers
```

Communication occurs only through the router or Layer-3 switch.

---

# Step 8 — Configure DHCP (Optional)

Provide separate DHCP scopes.

Example:

```text
VLAN10

↓

192.168.10.100

-

192.168.10.200
```

Repeat for every VLAN.

---

# Step 9 — Configure DNS

All VLANs should resolve:

```text
server.company.local
```

Verify DNS from every VLAN.

---

# Step 10 — Configure Firewall Rules

Example:

Allow:

```text
Users

↓

Servers
```

Block:

```text
Guest

↓

Servers
```

Restrict traffic according to business requirements.

---

# Step 11 — Verify Connectivity

Within VLAN:

```bash
ping
```

Across VLANs:

```bash
ping
```

DNS:

```bash
dig server.company.local
```

---

# Step 12 — Verify VLAN Tags

Capture packets.

```bash
sudo tcpdump
```

Verify:

```text
802.1Q

Tags
```

Tagged frames should appear on trunk links.

---

# Enterprise VLAN Architecture

```text
Internet
     │
Firewall
     │
Router
     │
Trunk
     │
Managed Switch
 ┌────┼────┬────┐
 │    │    │
V10  V20  V30
```

---

# Security Improvements

Implement:

- Separate Guest VLAN
- Management VLAN
- Restrict Inter-VLAN Access
- Disable Unused Ports
- Enable Port Security
- Limit Management Access

---

# Validation Checklist

| Item | Status |
|------|--------|
| VLANs Created | ☐ |
| Access Ports Configured | ☐ |
| Trunk Port Working | ☐ |
| Router Configured | ☐ |
| Inter-VLAN Routing Working | ☐ |
| DNS Working | ☐ |
| Firewall Rules Applied | ☐ |
| Guest Isolation Verified | ☐ |
| Documentation Updated | ☐ |

---

# Common Problems

| Problem | Solution |
|----------|----------|
| Devices Cannot Communicate | Check VLAN Assignment |
| Trunk Failure | Verify Allowed VLANs |
| No Inter-VLAN Routing | Verify Router Configuration |
| DHCP Not Working | Check VLAN Scope |
| DNS Failure | Verify Gateway & DNS Server |

---

# Troubleshooting Commands

View interfaces.

```bash
ip addr
```

View routes.

```bash
ip route
```

Verify connectivity.

```bash
ping
```

Resolve DNS.

```bash
dig server.company.local
```

Capture packets.

```bash
sudo tcpdump
```

---

# Bonus Challenges

Extend the project by:

- Configuring a Layer-3 Switch
- Implementing Dynamic Routing
- Deploying Kubernetes across VLANs
- Configuring HA Firewalls
- Creating a Dedicated Storage VLAN
- Configuring QoS between VLANs
- Automating VLAN creation with Ansible

---

# Learning Outcomes

After completing this project, you'll be able to:

- Design VLAN architectures
- Configure access and trunk ports
- Implement inter-VLAN routing
- Secure enterprise networks
- Troubleshoot VLAN communication
- Build segmented production networks

---

# Project Deliverables

By the end of this project, you should have:

- Multiple VLANs
- Trunk Configuration
- Access Port Configuration
- Router-on-a-Stick
- Inter-VLAN Routing
- DHCP (Optional)
- DNS Connectivity
- Firewall Rules
- Updated Network Documentation

---

# Self-Assessment

Before moving to the next project, confirm:

- [ ] Can you create VLANs on a managed switch?
- [ ] Can you configure access and trunk ports?
- [ ] Can you implement Router-on-a-Stick?
- [ ] Can you configure inter-VLAN routing?
- [ ] Can you isolate guest traffic?
- [ ] Can you troubleshoot VLAN issues?
- [ ] Can you document the VLAN design?

---

# Summary

In this capstone project, you designed and deployed a production-style VLAN architecture. You segmented the network into logical departments, configured trunk and access ports, enabled inter-VLAN routing, applied security controls, and validated communication across the enterprise network.

This project reflects common enterprise networking practices used in corporate offices, data centers, educational institutions, and cloud-connected environments.

---

## Key Takeaways

- VLANs logically separate networks without requiring additional physical infrastructure.
- Use **access ports** for end devices and **trunk ports** between network devices.
- Inter-VLAN communication requires a **router** or **Layer-3 switch**.
- Apply firewall rules to control communication between VLANs.
- Always document VLAN IDs, IP ranges, gateways, and port assignments.
- Network segmentation improves **security**, **performance**, and **manageability**.

---

## What's Next?

**[Build a DNS Server](build-dns-server.md)**

In the next capstone project, you'll learn how to **Build a DNS Server**.

You'll install and configure a production-style DNS server, create forward and reverse lookup zones, manage DNS records, configure client name resolution, and troubleshoot DNS issues in an enterprise environment.
