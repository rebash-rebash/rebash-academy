---
title: "Capstone Project 5 — Build a VPN Server"
description: "Build a production-ready WireGuard VPN server — encrypted tunnels, routing, NAT, firewall rules, DNS, and secure remote access."
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
  - vpn
  - wireguard
  - security
  - rebash-networking-mastery
comments: false
status: ready
---

# Capstone Project 5 — Build a VPN Server

> In this capstone project, you'll build a **production-ready VPN (Virtual Private Network) server** that allows users to securely access internal resources over the Internet. You'll deploy a Linux VPN server, configure encrypted tunnels, manage user authentication, implement firewall rules, configure routing, and verify secure remote connectivity. VPNs are widely used by enterprises to provide secure remote access for employees, administrators, and hybrid cloud environments. Every Network Engineer, DevOps Engineer, Platform Engineer, Cloud Engineer, SRE, and Cloud Architect should know how to deploy and manage VPN infrastructure.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 15: Capstone Projects → Project 5</p>

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

<div markdown>**Project:** 5 of 8</div>

</div>

</div>

---


# Project Objectives

By completing this project, you'll be able to:

- Deploy a Linux VPN server
- Configure encrypted VPN tunnels
- Manage VPN users
- Configure routing and firewall rules
- Secure remote access
- Verify VPN connectivity
- Troubleshoot VPN issues

---

# Skills Covered

This project combines concepts from:

- VPN
- WireGuard
- OpenVPN
- Routing
- Firewalls
- DNS
- Linux Networking
- Security
- Network Troubleshooting

---

# Project Scenario

Employees need secure access to internal resources while working remotely.

Current situation:

```text
Internet

↓

No Secure Access

↓

Internal Servers
```

Your task is to build a secure VPN gateway that allows authenticated users to access internal services safely.

---

# Target Architecture

```text
              Internet
                  │
             Public IP
                  │
            VPN Server
                  │
          Internal Network
      ┌───────────┴───────────┐
      │                       │
 Application Server      Database Server
```

Remote users connect through the VPN server before accessing internal resources.

---

# Recommended VPN Solutions

Popular enterprise VPN solutions:

- WireGuard
- OpenVPN
- IPSec
- StrongSwan

Recommended for this project:

```text
WireGuard
```

Because it is:

- Fast
- Secure
- Lightweight
- Easy to Configure

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

| Component | Address |
|-----------|---------|
| VPN Server | 192.168.20.10 |
| Internal LAN | 192.168.20.0/24 |
| VPN Network | 10.100.0.0/24 |
| Gateway | 192.168.20.1 |

---

# Step 1 — Install WireGuard

Ubuntu:

```bash
sudo apt update

sudo apt install wireguard -y
```

Verify installation.

---

# Step 2 — Generate Server Keys

Generate private key:

```bash
wg genkey
```

Generate public key:

```bash
wg pubkey
```

Store keys securely.

---

# Step 3 — Configure VPN Interface

Example interface:

```text
wg0
```

VPN Network:

```text
10.100.0.1/24
```

This interface acts as the VPN gateway.

---

# Step 4 — Enable IP Forwarding

Enable routing.

Temporary:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Permanent:

Edit:

```text
/etc/sysctl.conf
```

Set:

```text
net.ipv4.ip_forward=1
```

Reload:

```bash
sudo sysctl -p
```

---

# Step 5 — Configure Firewall

Allow VPN traffic.

Example:

```text
UDP

51820
```

Enable forwarding between:

- VPN Network
- Internal Network

---

# Step 6 — Configure NAT

Allow VPN clients to access internal resources.

Verify routing between:

```text
10.100.0.0/24

↓

192.168.20.0/24
```

---

# Step 7 — Create VPN Client

Generate client keys.

Assign:

```text
10.100.0.2
```

Repeat for additional users.

---

# Step 8 — Configure Client

Install WireGuard.

Import:

- Private Key
- Server Public Key
- Endpoint
- Allowed IPs

Activate the VPN connection.

---

# Step 9 — Start VPN Service

Enable:

```bash
sudo systemctl enable wg-quick@wg0
```

Start:

```bash
sudo systemctl start wg-quick@wg0
```

Verify:

```bash
sudo systemctl status wg-quick@wg0
```

---

# Step 10 — Verify VPN Tunnel

Check interface.

```bash
ip addr
```

Check peers.

```bash
sudo wg show
```

Confirm handshake and traffic statistics.

---

# Step 11 — Test Connectivity

Verify:

```bash
ping 10.100.0.1
```

Access an internal server:

```bash
ping 192.168.20.20
```

Verify HTTP:

```bash
curl http://192.168.20.20
```

---

# Step 12 — Configure DNS

Provide internal DNS server.

Example:

```text
192.168.20.20
```

Clients should resolve:

```text
server.company.local
```

---

# Step 13 — Add Multiple Users

Example:

| User | VPN Address |
|------|-------------|
| Alice | 10.100.0.2 |
| Bob | 10.100.0.3 |
| Charlie | 10.100.0.4 |

Each client receives a unique configuration.

---

# Step 14 — Configure Split Tunnel (Optional)

Internal traffic:

```text
VPN
```

Internet traffic:

```text
Local ISP
```

Split tunneling reduces VPN bandwidth usage.

---

# Step 15 — Configure Full Tunnel (Optional)

All traffic:

```text
Internet

↓

VPN

↓

Firewall

↓

Internet
```

This provides centralized security and traffic inspection.

---

# Enterprise VPN Architecture

```text
Remote Users
       │
Internet
       │
Firewall
       │
VPN Gateway
       │
Core Network
       │
Internal Servers
```

---

# Security Improvements

Implement:

- Strong Encryption
- Public Key Authentication
- MFA (if supported)
- Firewall Restrictions
- Logging
- Least Privilege Access
- Key Rotation
- Secure Configuration Backups

---

# Validation Checklist

| Item | Status |
|------|--------|
| WireGuard Installed | ☐ |
| Server Keys Generated | ☐ |
| Client Keys Generated | ☐ |
| VPN Interface Configured | ☐ |
| Firewall Updated | ☐ |
| IP Forwarding Enabled | ☐ |
| VPN Tunnel Established | ☐ |
| Internal Network Reachable | ☐ |
| DNS Working | ☐ |
| Documentation Updated | ☐ |

---

# Common Problems

| Problem | Solution |
|----------|----------|
| VPN Not Connecting | Verify Keys and Endpoint |
| No Handshake | Check Firewall and Port |
| Cannot Reach Internal Network | Verify Routing and NAT |
| DNS Not Working | Check Client DNS Configuration |
| Slow Performance | Verify MTU and Network Quality |

---

# Troubleshooting Commands

View interface.

```bash
ip addr
```

View routes.

```bash
ip route
```

View VPN peers.

```bash
sudo wg show
```

Check listening ports.

```bash
ss -tuln
```

Capture VPN traffic.

```bash
sudo tcpdump -i wg0
```

---

# Bonus Challenges

Extend the project by:

- Deploying High Availability VPN Servers
- Configuring Site-to-Site VPN
- Integrating LDAP Authentication
- Deploying VPN Monitoring
- Automating User Provisioning
- Configuring Dynamic DNS
- Integrating with Cloud VPC Networks

---

# Learning Outcomes

After completing this project, you'll be able to:

- Deploy enterprise VPN infrastructure
- Configure secure remote access
- Manage VPN users
- Configure routing and NAT
- Secure VPN services
- Troubleshoot VPN connectivity

---

# Project Deliverables

By the end of this project, you should have:

- Working VPN Server
- Secure VPN Tunnel
- Client Configuration
- Firewall Rules
- Routing Configuration
- DNS Integration
- Multiple VPN Users
- Network Documentation

---

# Self-Assessment

Before moving to the next project, confirm:

- [ ] Can you install and configure WireGuard?
- [ ] Can you generate and manage VPN keys?
- [ ] Can you configure routing and NAT?
- [ ] Can you securely connect remote users?
- [ ] Can you troubleshoot VPN connectivity?
- [ ] Can you integrate VPN with internal DNS?
- [ ] Can you document the VPN architecture?

---

# Summary

In this capstone project, you deployed a production-ready VPN server using WireGuard. You configured encrypted tunnels, secure user authentication, routing, NAT, DNS integration, firewall rules, and validated secure remote access to internal resources.

This project reflects modern enterprise VPN deployments used by organizations to provide secure remote access for employees, contractors, and administrators while protecting internal infrastructure from unauthorized access.

---

## Key Takeaways

- VPNs provide **secure, encrypted remote access** to private networks.
- **WireGuard** offers a simple, modern, and high-performance VPN solution.
- Enable **IP forwarding** and configure **NAT** for access to internal resources.
- Protect VPN services with strong authentication, firewall rules, and key management.
- Verify connectivity using routing, DNS, and application-level testing.
- Document VPN users, address assignments, firewall rules, and recovery procedures.

---

## What's Next?

**[Create a Firewall Gateway](firewall-gateway.md)**

In the next capstone project, you'll learn how to **Create a Firewall Gateway**.

You'll build a Linux-based firewall gateway, configure packet filtering, NAT, port forwarding, traffic logging, network segmentation, and security policies to protect an enterprise network from unauthorized access while enabling controlled communication between internal and external networks.
