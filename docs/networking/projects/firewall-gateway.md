---
title: "Capstone Project 6 — Create a Firewall Gateway"
description: "Build a production-ready Linux firewall gateway — packet filtering, NAT, port forwarding, DMZ, logging, and secure enterprise policies."
difficulty: advanced
estimated_time: "6–10 hours"
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
  - firewall
  - nat
  - security
  - rebash-networking-mastery
comments: false
status: ready
---

# Capstone Project 6 — Create a Firewall Gateway

> In this capstone project, you'll build a **production-ready Linux Firewall Gateway** that protects an enterprise network from unauthorized access while securely allowing approved traffic. You'll configure packet filtering, Network Address Translation (NAT), port forwarding, logging, routing, network segmentation, and firewall policies. This project reflects how organizations secure their internal infrastructure using dedicated firewall gateways. Every Network Engineer, DevOps Engineer, SRE, Platform Engineer, Cloud Engineer, and Cloud Architect should know how to deploy and manage firewall gateways.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 15: Capstone Projects → Project 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Advanced</div>

<div markdown>**Estimated Completion Time:** 6–10 Hours</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Capstone Projects</div>

<div markdown>**Project:** 6 of 8</div>

</div>

</div>

---


# Project Objectives

By completing this project, you'll be able to:

- Build a Linux firewall gateway
- Configure packet filtering
- Implement Network Address Translation (NAT)
- Configure port forwarding
- Secure internal networks
- Enable firewall logging
- Troubleshoot firewall policies

---

# Skills Covered

This project combines concepts from:

- Firewalls
- iptables
- nftables
- NAT
- Routing
- VPN
- Linux Networking
- Security
- Network Troubleshooting

---

# Project Scenario

Your company currently connects directly to the Internet.

Problems:

- No centralized security
- Public exposure of internal systems
- No traffic filtering
- No logging
- No access control

Your task is to deploy a firewall gateway that protects the entire network.

---

# Target Architecture

```text
                Internet
                    │
             Public Interface
                    │
           Linux Firewall Gateway
          ┌─────────┴─────────┐
          │                   │
   Internal Network      DMZ Network
          │                   │
      Workstations       Public Servers
```

All traffic passes through the firewall before reaching internal resources.

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

| Interface | Network |
|-----------|---------|
| WAN | Public IP |
| LAN | 192.168.20.0/24 |
| DMZ | 192.168.30.0/24 |
| VPN | 10.100.0.0/24 |

---

# Step 1 — Install Firewall Server

Install Ubuntu Server.

Assign two network interfaces:

```text
eth0

↓

Internet
```

```text
eth1

↓

LAN
```

(Optional)

```text
eth2

↓

DMZ
```

---

# Step 2 — Update the System

```bash
sudo apt update

sudo apt upgrade -y
```

---

# Step 3 — Enable IP Forwarding

Temporary:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Permanent:

Edit:

```text
/etc/sysctl.conf
```

Enable:

```text
net.ipv4.ip_forward=1
```

Reload:

```bash
sudo sysctl -p
```

---

# Step 4 — Configure NAT

Enable internal systems to access the Internet.

Traffic flow:

```text
LAN

↓

Firewall

↓

Internet
```

Verify outbound connectivity after enabling NAT.

---

# Step 5 — Configure Default Firewall Policy

Recommended defaults:

```text
Inbound

↓

Deny
```

```text
Forward

↓

Deny
```

```text
Outbound

↓

Allow
```

Adopt a default-deny approach for better security.

---

# Step 6 — Allow Essential Services

Permit only required services.

Examples:

| Service | Port |
|----------|-----:|
| SSH | 22 |
| HTTP | 80 |
| HTTPS | 443 |
| DNS | 53 |
| VPN | 51820 (UDP) |

---

# Step 7 — Configure Port Forwarding

Example:

```text
Internet

↓

HTTPS

↓

Web Server

192.168.30.10
```

Only expose necessary services.

---

# Step 8 — Create DMZ Rules

Allow:

```text
Internet

↓

DMZ
```

Block:

```text
Internet

↓

LAN
```

DMZ systems remain isolated from the internal network.

---

# Step 9 — Restrict Internal Access

Example:

Allow:

```text
LAN

↓

Internet
```

Block:

```text
Guest VLAN

↓

Servers
```

Implement the Principle of Least Privilege.

---

# Step 10 — Configure Logging

Log:

- Blocked Connections
- Firewall Drops
- Invalid Packets
- Port Scans
- Unauthorized Access

Logs support monitoring and incident investigations.

---

# Step 11 — Verify Firewall Rules

List active rules.

Using iptables:

```bash
sudo iptables -L -v
```

Using nftables:

```bash
sudo nft list ruleset
```

Review rule order carefully.

---

# Step 12 — Test Connectivity

Verify:

```bash
ping
```

HTTP:

```bash
curl http://example.com
```

DNS:

```bash
dig google.com
```

VPN:

Verify secure access to internal resources.

---

# Step 13 — Configure SSH Protection

Allow SSH only from:

- Management VLAN
- VPN Clients
- Trusted IP Addresses

Disable direct public administrative access.

---

# Step 14 — Enable Firewall Persistence

Ensure firewall rules survive reboot.

For iptables:

```bash
sudo apt install iptables-persistent
```

Save configuration.

---

# Step 15 — Monitor Firewall Activity

View logs.

```bash
journalctl
```

Capture traffic.

```bash
sudo tcpdump
```

Monitor:

- Connection Attempts
- Blocked Packets
- Active Sessions

---

# Enterprise Firewall Architecture

```text
Internet
      │
Firewall
 ┌────┴─────┐
 │          │
LAN        DMZ
 │          │
Servers   Public Apps
```

This architecture is common in enterprise environments.

---

# Security Improvements

Implement:

- Default Deny Policy
- Network Segmentation
- VPN for Administration
- Logging
- IDS/IPS Integration
- Geo-IP Blocking (Optional)
- Rate Limiting
- Regular Rule Reviews

---

# Validation Checklist

| Item | Status |
|------|--------|
| Firewall Installed | ☐ |
| IP Forwarding Enabled | ☐ |
| NAT Configured | ☐ |
| Default Policies Applied | ☐ |
| Port Forwarding Working | ☐ |
| DMZ Protected | ☐ |
| Firewall Logs Working | ☐ |
| SSH Restricted | ☐ |
| Internet Access Verified | ☐ |
| Documentation Updated | ☐ |

---

# Common Problems

| Problem | Solution |
|----------|----------|
| No Internet Access | Verify NAT and Default Route |
| Port Forwarding Failure | Check Forwarding Rules |
| VPN Cannot Reach LAN | Verify Forwarding Policy |
| Firewall Blocks DNS | Allow UDP/TCP Port 53 |
| SSH Access Lost | Verify Management Rules Before Applying |

---

# Troubleshooting Commands

Check interfaces.

```bash
ip addr
```

View routes.

```bash
ip route
```

View firewall rules.

```bash
sudo iptables -L -v
```

or

```bash
sudo nft list ruleset
```

Capture packets.

```bash
sudo tcpdump
```

Check listening ports.

```bash
ss -tuln
```

---

# Bonus Challenges

Extend the project by:

- Deploying High Availability Firewalls
- Implementing IDS/IPS
- Integrating Suricata
- Configuring Geo-IP Filtering
- Enabling Web Filtering
- Deploying Firewall Monitoring Dashboards
- Automating Firewall Rules with Ansible

---

# Learning Outcomes

After completing this project, you'll be able to:

- Deploy an enterprise firewall gateway
- Configure NAT and routing
- Build secure firewall policies
- Protect internal networks
- Configure DMZ architectures
- Troubleshoot firewall issues

---

# Project Deliverables

By the end of this project, you should have:

- Linux Firewall Gateway
- NAT Configuration
- Port Forwarding
- DMZ Network
- Secure Firewall Policies
- Logging Configuration
- VPN Integration
- Network Documentation

---

# Self-Assessment

Before moving to the next project, confirm:

- [ ] Can you configure a Linux firewall gateway?
- [ ] Can you enable NAT and IP forwarding?
- [ ] Can you create secure firewall rules?
- [ ] Can you configure port forwarding?
- [ ] Can you isolate a DMZ from the LAN?
- [ ] Can you troubleshoot firewall connectivity?
- [ ] Can you document the firewall architecture?

---

# Summary

In this capstone project, you built a production-ready Linux firewall gateway that protects an enterprise network from unauthorized access. You configured packet filtering, NAT, routing, port forwarding, DMZ segmentation, logging, and secure administrative access while validating connectivity and security.

This project mirrors the firewall architectures commonly deployed in enterprise data centers, cloud environments, and hybrid infrastructures where centralized security and controlled traffic flow are critical.

---

## Key Takeaways

- A firewall gateway acts as the **first line of defense** for enterprise networks.
- Use a **default-deny** policy and explicitly allow only required traffic.
- Configure **NAT** to provide Internet access for private networks.
- Isolate publicly accessible services in a **DMZ**.
- Enable comprehensive **logging** for monitoring, auditing, and incident response.
- Regularly review, test, and document firewall rules to maintain a secure environment.

---

## What's Next?

**[Cloud VPC Design](cloud-vpc-design.md)**

In the next capstone project, you'll learn about **Cloud VPC Design**.

You'll design production-grade cloud networking architectures for AWS, Azure, and Google Cloud, including VPCs, subnets, routing, Internet Gateways, NAT Gateways, load balancers, hybrid connectivity, and highly available multi-region network designs.
