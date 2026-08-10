---
title: "Capstone Project 4 — Configure a DHCP Server"
description: "Build a production-ready ISC DHCP server — scopes, reservations, leases, multi-subnet/VLAN support, DNS integration, and DHCP relay."
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
  - dhcp
  - ip-addressing
  - production
  - rebash-networking-mastery
comments: false
status: ready
---

# Capstone Project 4 — Configure a DHCP Server

> In this capstone project, you'll build a **production-ready DHCP (Dynamic Host Configuration Protocol) server** that automatically assigns IP addresses and network configuration to client devices. You'll configure DHCP scopes, reservations, lease times, multiple subnets, DHCP relay, and integrate DHCP with DNS. DHCP is one of the most important infrastructure services because it automates network configuration and simplifies device management. Every Network Engineer, DevOps Engineer, Platform Engineer, Cloud Engineer, and System Administrator should understand how to deploy and manage DHCP services.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 15: Capstone Projects → Project 4</p>

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

<div markdown>**Project:** 4 of 8</div>

</div>

</div>

---

# Project Objectives

By completing this project, you'll be able to:

- Deploy a Linux DHCP server
- Configure DHCP scopes
- Create IP reservations
- Configure lease times
- Support multiple VLANs and subnets
- Integrate DHCP with DNS
- Troubleshoot DHCP issues

---

# Skills Covered

This project combines concepts from:

- DHCP
- IP Addressing
- DNS
- VLANs
- Routing
- Linux Networking
- Firewalls
- Network Troubleshooting

---

# Project Scenario

Currently, every workstation is configured manually.

Problems include:

- IP conflicts
- Incorrect gateway settings
- DNS configuration errors
- High administrative effort

Your task is to automate IP address assignment using DHCP.

---

# Target Architecture

```text
                Internet
                    │
                 Router
                    │
               Core Switch
                    │
      ┌─────────────┴─────────────┐
      │                           │
 DHCP Server                 Client Devices
      │
 DNS Server
```

Clients automatically receive network configuration.

---

# Lab Requirements

Software:

- Ubuntu Server LTS
- Debian
- Rocky Linux

Recommended:

- Ubuntu Server LTS

---

# Network Design

| Device | IP Address |
|---------|------------|
| DHCP Server | 192.168.20.10 |
| DNS Server | 192.168.20.20 |
| Gateway | 192.168.20.1 |
| Clients | Dynamic |

---

# Step 1 — Install DHCP Server

Ubuntu:

```bash
sudo apt update

sudo apt install isc-dhcp-server -y
```

Verify installation.

---

# Step 2 — Configure Network Interface

Identify interface:

```bash
ip addr
```

Configure DHCP service to listen on:

```text
eth0
```

(or your active interface)

---

# Step 3 — Configure DHCP Scope

Example subnet:

```text
192.168.20.0/24
```

DHCP Pool:

```text
192.168.20.100

↓

192.168.20.200
```

Reserved addresses remain available for servers and infrastructure.

---

# Step 4 — Configure Gateway

Default gateway:

```text
192.168.20.1
```

Clients automatically receive the correct gateway.

---

# Step 5 — Configure DNS

Provide:

```text
192.168.20.20
```

Clients automatically use the internal DNS server.

---

# Step 6 — Configure Domain Name

Example:

```text
company.local
```

Clients receive:

```text
server.company.local
```

for internal name resolution.

---

# Step 7 — Configure Lease Time

Example:

Default Lease:

```text
8 Hours
```

Maximum Lease:

```text
24 Hours
```

Lease durations should balance network efficiency and address availability.

---

# Step 8 — Restart DHCP Service

```bash
sudo systemctl restart isc-dhcp-server
```

Verify:

```bash
sudo systemctl status isc-dhcp-server
```

---

# Step 9 — Configure Client

Release current lease:

```bash
sudo dhclient -r
```

Request a new lease:

```bash
sudo dhclient
```

Verify:

```bash
ip addr
```

---

# Step 10 — Verify Assigned Configuration

Check:

- IP Address
- Gateway
- DNS Server
- Lease Duration

Verify connectivity.

---

# Step 11 — Configure DHCP Reservation

Reserve an address for a server.

Example:

```text
MAC Address

↓

192.168.20.50
```

Critical systems should receive consistent IP addresses.

---

# Step 12 — Configure Multiple Subnets

Example:

| VLAN | Network |
|------|---------|
| Users | 192.168.10.0/24 |
| Servers | 192.168.20.0/24 |
| DevOps | 192.168.30.0/24 |
| Guest | 192.168.40.0/24 |

Create a DHCP scope for each subnet.

---

# Step 13 — Configure DHCP Relay

When DHCP server and clients are on different VLANs:

```text
Client

↓

Relay Agent

↓

DHCP Server
```

The relay forwards DHCP requests across routed networks.

---

# Step 14 — Configure Firewall

Allow DHCP traffic.

Ports:

| Protocol | Port |
|----------|------|
| UDP | 67 |
| UDP | 68 |

Verify clients can communicate with the server.

---

# Step 15 — Verify Logs

View logs:

```bash
journalctl -u isc-dhcp-server
```

Confirm:

- Lease Requests
- Lease Assignments
- Errors
- Service Startup

---

# Enterprise DHCP Architecture

```text
Clients
     │
     │
Core Switch
     │
DHCP Relay
     │
DHCP Server
     │
DNS Server
```

Large organizations commonly centralize DHCP services.

---

# DHCP and DNS Integration

Workflow:

```text
Client

↓

DHCP

↓

IP Assigned

↓

DNS Registration

↓

Name Resolution
```

This enables automatic hostname registration.

---

# Security Improvements

Implement:

- DHCP Reservations for Critical Systems
- DHCP Snooping
- Restrict Unauthorized DHCP Servers
- Firewall Protection
- Logging
- Backup DHCP Configuration

---

# Validation Checklist

| Item | Status |
|------|--------|
| DHCP Installed | ☐ |
| Scope Configured | ☐ |
| Gateway Configured | ☐ |
| DNS Configured | ☐ |
| Lease Times Configured | ☐ |
| Client Receives Address | ☐ |
| Reservation Tested | ☐ |
| Firewall Updated | ☐ |
| Logs Verified | ☐ |
| Documentation Updated | ☐ |

---

# Common Problems

| Problem | Solution |
|----------|----------|
| No IP Assigned | Verify DHCP Service |
| Incorrect Gateway | Check Scope Configuration |
| DNS Missing | Verify DHCP Options |
| Duplicate IP | Review Reservations |
| Cross-VLAN Failure | Verify DHCP Relay |

---

# Troubleshooting Commands

Check interface.

```bash
ip addr
```

Restart DHCP.

```bash
sudo systemctl restart isc-dhcp-server
```

View logs.

```bash
journalctl -u isc-dhcp-server
```

Renew lease.

```bash
sudo dhclient
```

Release lease.

```bash
sudo dhclient -r
```

---

# Bonus Challenges

Extend the project by:

- Configuring High Availability DHCP
- Deploying DHCP Failover
- Integrating with Active Directory
- Automating DHCP Configuration
- Deploying Multiple DHCP Servers
- Monitoring DHCP Leases with Prometheus
- Implementing DHCP Snooping on Switches

---

# Learning Outcomes

After completing this project, you'll be able to:

- Deploy enterprise DHCP infrastructure
- Configure multiple DHCP scopes
- Create IP reservations
- Integrate DHCP with DNS
- Configure DHCP relay
- Troubleshoot DHCP services

---

# Project Deliverables

By the end of this project, you should have:

- Working DHCP Server
- DHCP Scope
- Gateway Configuration
- DNS Configuration
- Lease Policies
- Static Reservations
- DHCP Relay (Optional)
- Firewall Rules
- Documentation

---

# Self-Assessment

Before moving to the next project, confirm:

- [ ] Can you install and configure a DHCP server?
- [ ] Can you create DHCP scopes?
- [ ] Can you configure lease durations?
- [ ] Can you configure DHCP reservations?
- [ ] Can you support multiple VLANs?
- [ ] Can you troubleshoot DHCP issues?
- [ ] Can you document the DHCP infrastructure?

---

# Summary

In this capstone project, you deployed a production-ready DHCP server and automated IP address assignment for client systems. You configured DHCP scopes, reservations, lease policies, DNS integration, multiple subnets, and DHCP relay while validating client connectivity and service availability.

This project reflects real-world enterprise environments where DHCP automates network configuration, reduces administrative overhead, and ensures consistent, scalable IP address management.

---

## Key Takeaways

- DHCP automates **IP address assignment** and client network configuration.
- Configure separate DHCP scopes for each **subnet** or **VLAN**.
- Use **reservations** for servers, printers, and network infrastructure.
- Deploy **DHCP relay** when clients and servers are separated by routers.
- Integrate DHCP with DNS for seamless hostname resolution.
- Protect DHCP infrastructure with logging, firewall rules, and DHCP snooping where supported.

---

## What's Next?

**[Build a VPN Server](build-vpn-server.md)**

In the next capstone project, you'll learn how to **Build a VPN Server**.

You'll deploy a secure remote access VPN using Linux, configure encrypted tunnels, manage user authentication, implement firewall rules, enable secure access to internal resources, and troubleshoot VPN connectivity in a production-style environment.
