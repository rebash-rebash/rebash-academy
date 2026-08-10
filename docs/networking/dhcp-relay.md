---
title: "DHCP Relay"
description: "Learn DHCP Relay — broadcast limitations, relay agents, GIADDR, centralised DHCP across VLANs, and Linux dhcrelay basics."
difficulty: intermediate
estimated_time: "90 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 6 · DNS and DHCP"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - dhcp
  - dhcp-relay
  - vlan
  - rebash-networking-mastery
comments: false
status: ready
---

# DHCP Relay — Delivering DHCP Across Multiple Networks

> **DHCP Relay** is a mechanism that allows Dynamic Host Configuration Protocol (DHCP) clients to obtain IP addresses from a DHCP server located on a **different subnet**. Since DHCP Discover messages are broadcast packets and routers do not forward broadcasts by default, a **DHCP Relay Agent** receives the broadcast request, converts it into a unicast message, and forwards it to the DHCP server. DHCP Relay enables organisations to deploy **centralised DHCP servers** while supporting multiple Virtual Local Area Networks (VLANs), branch offices, and enterprise networks. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand DHCP Relay.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 6: DNS & DHCP → Lesson 5</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** DNS & DHCP</div>

<div markdown>**Lesson:** 5 of 7</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand DHCP Relay
- Learn why DHCP Relay is needed
- Understand broadcast limitations
- Learn the DHCP Relay process
- Understand Relay Agents
- Configure DHCP Relay
- Troubleshoot DHCP Relay issues

---

# Prerequisites

Complete:

- [DNS Fundamentals](dns-fundamentals.md)
- [DNS Records](dns-records-and-troubleshooting.md)
- [DNS Resolution](dns-resolution.md)
- [DHCP Process](icmp-arp-dhcp-and-network-services.md)

---

# Why Learn DHCP Relay?

Imagine an enterprise with:

- 20 VLANs
- 15 Branch Offices
- One Central DHCP Server

Without DHCP Relay:

```text
Every VLAN

↓

Needs Its Own

DHCP Server

❌ Expensive
```

Instead:

```text
One DHCP Server

↓

DHCP Relay

↓

All Networks
```

---

# What is DHCP Relay?

A **DHCP Relay Agent** forwards DHCP messages between clients and a DHCP server located on another subnet.

Instead of:

```text
Client

↓

Broadcast

↓

Lost at Router
```

The relay agent performs:

```text
Broadcast

↓

Relay Agent

↓

Unicast

↓

DHCP Server
```

---

# Why is DHCP Relay Needed?

DHCP clients send:

```text
DHCP Discover

↓

Broadcast
```

Broadcast packets:

```text
Do NOT Cross

Routers
```

Without a relay:

```text
Different Subnet

↓

No DHCP Response
```

---

# Broadcast Limitation

Example:

Client:

```text
192.168.10.0/24
```

DHCP Server:

```text
192.168.20.10
```

Separated by a router.

Broadcast:

```text
Discover

↓

Router

↓

Dropped
```

The DHCP server never receives the request.

---

# DHCP Relay Solution

Router configured as:

```text
DHCP Relay Agent
```

Workflow:

```text
Client

↓

Broadcast

↓

Relay Agent

↓

Unicast

↓

DHCP Server
```

---

# DHCP Relay Agent

A DHCP Relay Agent is typically:

- Router
- Layer 3 Switch
- Firewall
- Gateway

Responsibilities:

- Receive Broadcast
- Add Relay Information
- Forward to DHCP Server
- Return Reply to Client

---

# DHCP Relay Workflow

```text
Client

↓

DHCP Discover (Broadcast)

↓

Relay Agent

↓

DHCP Discover (Unicast)

↓

DHCP Server

↓

DHCP Offer

↓

Relay Agent

↓

Client
```

The remaining Discover, Offer, Request, Acknowledgment (DORA) steps follow the same path.

---

# Complete DORA with Relay

```text
Client

↓

Discover (Broadcast)

↓

Relay Agent

↓

Discover (Unicast)

↓

DHCP Server

↓

Offer

↓

Relay Agent

↓

Client

↓

Request

↓

Relay Agent

↓

Server

↓

ACK

↓

Relay Agent

↓

Client
```

---

# GIADDR (Gateway IP Address)

When forwarding the request, the relay agent inserts:

```text
GIADDR

Gateway IP Address
```

Example:

```text
192.168.10.1
```

The DHCP server uses this information to determine:

```text
Which DHCP Scope

Should Be Used
```

---

# Scope Selection

Example:

GIADDR:

```text
192.168.30.1
```

DHCP Server selects:

```text
Scope

192.168.30.0/24
```

The correct IP address is assigned to the client.

---

# Enterprise Example

Network:

```text
VLAN 10

↓

Router

↓

DHCP Server
```

```text
VLAN 20

↓

Router

↓

DHCP Server
```

```text
VLAN 30

↓

Router

↓

DHCP Server
```

A single DHCP server provides addresses for every VLAN.

---

# Branch Office Example

```text
Branch Office

↓

Router

↓

VPN

↓

Head Office

↓

DHCP Server
```

The branch router relays DHCP requests to headquarters.

---

# Cloud Perspective

Traditional DHCP Relay is less common in public cloud environments because cloud platforms provide managed DHCP services for virtual networks.

However, DHCP Relay may still be used in:

- Hybrid Cloud
- VMware Environments
- Private Clouds
- Enterprise Data Centres

---

# Kubernetes Perspective

Kubernetes Pods typically receive IP addresses from the Container Network Interface (CNI), not DHCP.

Worker nodes, however, often obtain their network configuration through DHCP or cloud-managed networking.

---

# Linux Perspective

Linux can function as a DHCP Relay using software such as:

- ISC DHCP Relay (`dhcrelay`)
- Kea DHCP Relay

Display network interfaces.

```bash
ip addr
```

Display routing table.

```bash
ip route
```

Check listening ports.

```bash
ss -tuln
```

Example (ISC DHCP Relay):

```bash
sudo dhcrelay eth0
```

Relay to a specific DHCP server:

```bash
sudo dhcrelay -i eth0 192.168.20.10
```

> Actual command-line options may vary depending on the DHCP relay implementation.

---

# DHCP Relay Example

```text
Laptop

↓

Switch

↓

Router (Relay)

↓

DHCP Server

↓

Offer

↓

Laptop
```

The client receives an address even though the server is on another subnet.

---

# Advantages of DHCP Relay

- Centralised DHCP Management
- Lower Infrastructure Cost
- Supports Multiple VLANs
- Easier Administration
- Better Scalability
- Simplified Branch Office Design

---

# Limitations

- Requires Layer 3 device configuration
- Relay failure affects DHCP for connected networks
- Incorrect GIADDR configuration can result in wrong address assignments
- Relay depends on connectivity to the DHCP server

---

# Hands-on Lab

## Task 1

Display network interfaces.

```bash
ip addr
```

---

## Task 2

Display routing table.

```bash
ip route
```

---

## Task 3

Check listening network services.

```bash
ss -tuln
```

---

## Task 4

Draw a network containing:

- Client
- Switch
- Router (Relay Agent)
- DHCP Server

Show the DORA process.

---

## Task 5

Explain why DHCP broadcasts cannot cross routers.

---

## Task 6

Explain the purpose of the GIADDR field.

---

## Task 7

Design a DHCP architecture for:

- Five VLANs
- One Central DHCP Server

---

## Task 8

Research DHCP Relay configuration on:

- Cisco IOS
- Linux
- Windows Server

Compare the approaches.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip addr` | Display network interfaces |
| `ip route` | Display routing table |
| `ss -tuln` | Display listening network ports |
| `dhcrelay` | Run DHCP Relay (if installed) |

---

# Common Mistakes

❌ Assuming routers forward DHCP broadcasts.

✅ Configure a DHCP Relay Agent.

---

❌ Forgetting to configure the relay destination.

✅ Specify the correct DHCP server address.

---

❌ Incorrect DHCP scope selection.

✅ Verify the GIADDR matches the correct subnet.

---

❌ Blocking DHCP traffic with firewalls.

✅ Allow DHCP and relay communication.

---

❌ Running separate DHCP servers unnecessarily.

✅ Use centralised DHCP with relay where appropriate.

---

# Best Practices

- Centralise DHCP servers whenever practical.
- Configure DHCP Relay on Layer 3 gateways.
- Verify GIADDR values during troubleshooting.
- Create separate DHCP scopes for each subnet.
- Monitor DHCP lease usage.
- Document relay configurations and DHCP scopes.

---

# Interview Questions

## Beginner

1. What is DHCP Relay?
2. Why is DHCP Relay required?
3. What is a Relay Agent?
4. Why can't DHCP broadcasts cross routers?

---

## Intermediate

1. Explain the DHCP Relay workflow.
2. What is GIADDR?
3. How does a DHCP server select the correct scope?
4. Compare DHCP Relay with deploying multiple DHCP servers.

---

## Architect Level

1. Design a centralised DHCP architecture for a company with 50 VLANs.
2. How would you troubleshoot clients that fail to obtain addresses through a relay?
3. Explain DHCP Relay in hybrid enterprise and cloud environments.

---

# Summary

In this lesson, you learned:

- DHCP Relay
- Broadcast Limitations
- Relay Agents
- GIADDR
- Centralised DHCP
- Multi-Subnet DHCP
- Enterprise DHCP Design
- Linux DHCP Relay Commands

DHCP Relay enables clients on different subnets to receive IP addresses from a centralised DHCP server. By forwarding DHCP broadcasts as unicast messages and identifying the originating subnet through the GIADDR field, relay agents simplify network management, reduce infrastructure costs, and support scalable enterprise network designs.

---

## Key Takeaways

- DHCP broadcasts **do not cross routers**.
- A **DHCP Relay Agent** forwards client requests to remote DHCP servers.
- The relay agent inserts the **GIADDR** to identify the client's subnet.
- Centralised DHCP reduces administrative overhead.
- DHCP Relay is widely used in VLAN-based enterprise networks.
- Proper relay configuration ensures clients receive addresses from the correct scope.

---

## What's Next?

**[Split DNS](split-dns.md)**

In the next lesson, you'll learn about **Split DNS**.

You'll explore:

- What Split DNS is
- Internal vs External DNS
- Private and Public DNS Zones
- Enterprise DNS Architecture
- Hybrid Cloud DNS
- Security Benefits
- Best Practices

By the end of the lesson, you'll understand how organisations provide different DNS responses for internal and external users while improving security, performance, and manageability.
