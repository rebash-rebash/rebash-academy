---
title: "Capstone Project 3 — Build a DNS Server"
description: "Build a production-ready BIND9 DNS server — forward/reverse zones, records, forwarders, clients, security, and DNS troubleshooting."
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
  - dns
  - bind9
  - production
  - rebash-networking-mastery
comments: false
status: ready
---

# Capstone Project 3 — Build a DNS Server

> In this capstone project, you'll build a **production-ready DNS (Domain Name System) server** using Linux. You'll install and configure a DNS server, create forward and reverse lookup zones, manage DNS records, configure client systems, enable caching, secure the server, and troubleshoot DNS resolution. DNS is one of the most critical services in every enterprise because almost every application depends on reliable name resolution. Every Network Engineer, DevOps Engineer, SRE, Platform Engineer, Cloud Engineer, and Cloud Architect should know how to deploy and manage DNS infrastructure.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 15: Capstone Projects → Project 3</p>

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

<div markdown>**Project:** 3 of 8</div>

</div>

</div>

---

# Project Objectives

By completing this project, you'll be able to:

- Deploy a Linux DNS server
- Configure forward lookup zones
- Configure reverse lookup zones
- Create DNS records
- Configure DNS clients
- Secure DNS infrastructure
- Troubleshoot DNS issues

---

# Skills Covered

This project combines concepts from:

- DNS
- Linux Networking
- TCP/IP
- Routing
- DHCP
- Firewalls
- Monitoring
- Network Troubleshooting

---

# Project Scenario

Your organization currently accesses servers using IP addresses.

Example:

```text
192.168.20.10
```

Instead, users should access services using:

```text
server.company.local
```

Your task is to build an enterprise DNS infrastructure.

---

# Target Architecture

```text
Clients
     │
     │
DNS Queries
     │
DNS Server
     │
Forwarders
     │
Internet DNS
```

Internal names are resolved locally.

External names are forwarded to public DNS servers.

---

# Lab Requirements

Software:

- Ubuntu Server
- Debian
- Rocky Linux

Recommended:

- Ubuntu Server LTS

---

# Network Design

| Device | IP Address |
|---------|------------|
| DNS Server | 192.168.20.10 |
| Client | 192.168.20.100 |
| Gateway | 192.168.20.1 |

---

# Step 1 — Install BIND9

Ubuntu:

```bash
sudo apt update

sudo apt install bind9 bind9utils dnsutils -y
```

Verify installation.

---

# Step 2 — Check Service Status

```bash
sudo systemctl status bind9
```

Enable:

```bash
sudo systemctl enable bind9
```

Start:

```bash
sudo systemctl start bind9
```

---

# Step 3 — Configure Forward Zone

Example domain:

```text
company.local
```

Create:

```text
Forward

Lookup

Zone
```

---

# Step 4 — Configure Reverse Zone

Create reverse lookup for:

```text
192.168.20.0/24
```

This enables IP-to-hostname resolution.

---

# Step 5 — Create DNS Records

Example:

| Record | Value |
|---------|-------|
| server | 192.168.20.10 |
| web | 192.168.20.20 |
| db | 192.168.20.30 |
| git | 192.168.20.40 |

---

# Step 6 — Configure Reverse Records

Example:

```text
192.168.20.10

↓

server.company.local
```

Reverse lookups help with troubleshooting and logging.

---

# Step 7 — Configure Forwarders

Example public DNS:

```text
8.8.8.8
```

```text
1.1.1.1
```

Unknown domains will be forwarded automatically.

---

# Step 8 — Restart DNS Service

```bash
sudo systemctl restart bind9
```

Verify:

```bash
sudo systemctl status bind9
```

---

# Step 9 — Validate Configuration

Check syntax.

```bash
named-checkconf
```

Validate zones.

```bash
named-checkzone company.local
```

Fix all configuration errors before continuing.

---

# Step 10 — Configure Client

Edit:

```text
/etc/resolv.conf
```

Example:

```text
nameserver 192.168.20.10
```

Clients now use the internal DNS server.

---

# Step 11 — Test Name Resolution

Forward lookup:

```bash
dig server.company.local
```

Reverse lookup:

```bash
dig -x 192.168.20.10
```

Both should return correct results.

---

# Step 12 — Configure Firewall

Allow DNS.

UDP:

```text
53
```

TCP:

```text
53
```

Verify connectivity from client systems.

---

# Step 13 — Enable DNS Logging

Monitor queries.

Example:

```bash
journalctl -u bind9
```

Review:

- Queries
- Errors
- Startup Messages

---

# Step 14 — Configure DNS Caching

Benefits:

- Faster Resolution
- Lower Internet Traffic
- Better Performance

Verify repeated queries complete more quickly.

---

# Step 15 — Configure Secondary DNS (Optional)

Architecture:

```text
Primary DNS

↓

Zone Transfer

↓

Secondary DNS
```

Provides redundancy and higher availability.

---

# Enterprise DNS Architecture

```text
Clients
      │
      │
Primary DNS
      │
Secondary DNS
      │
Internet DNS
```

Production environments typically deploy multiple DNS servers.

---

# Security Improvements

Implement:

- Restrict Zone Transfers
- Disable Recursive Queries for External Clients
- Limit Management Access
- Firewall Protection
- DNS Logging
- Backup Configuration Files

---

# Validation Checklist

| Item | Status |
|------|--------|
| BIND Installed | ☐ |
| DNS Service Running | ☐ |
| Forward Zone Created | ☐ |
| Reverse Zone Created | ☐ |
| Records Added | ☐ |
| Forwarders Configured | ☐ |
| Client Configured | ☐ |
| Firewall Updated | ☐ |
| DNS Queries Working | ☐ |
| Documentation Updated | ☐ |

---

# Common Problems

| Problem | Solution |
|----------|----------|
| Service Not Starting | Check Configuration Syntax |
| DNS Query Fails | Verify Zone File |
| Reverse Lookup Failure | Verify PTR Record |
| External Domains Fail | Check Forwarders |
| Client Cannot Resolve | Verify `/etc/resolv.conf` |

---

# Troubleshooting Commands

Check configuration.

```bash
named-checkconf
```

Check zone.

```bash
named-checkzone company.local
```

Forward lookup.

```bash
dig server.company.local
```

Reverse lookup.

```bash
dig -x 192.168.20.10
```

View service logs.

```bash
journalctl -u bind9
```

---

# Bonus Challenges

Extend the project by:

- Deploying a Secondary DNS Server
- Configuring Split-Horizon DNS
- Enabling DNSSEC
- Creating Wildcard DNS Records
- Configuring Dynamic DNS
- Monitoring DNS with Prometheus
- Automating DNS Record Creation

---

# Learning Outcomes

After completing this project, you'll be able to:

- Deploy enterprise DNS infrastructure
- Configure forward and reverse lookup zones
- Manage DNS records
- Configure Linux DNS clients
- Troubleshoot DNS problems
- Build highly available DNS environments

---

# Project Deliverables

By the end of this project, you should have:

- Working BIND9 DNS Server
- Forward Lookup Zone
- Reverse Lookup Zone
- A Records
- PTR Records
- Forwarders
- Client Configuration
- Firewall Configuration
- DNS Documentation

---

# Self-Assessment

Before moving to the next project, confirm:

- [ ] Can you install and configure BIND9?
- [ ] Can you create forward lookup zones?
- [ ] Can you create reverse lookup zones?
- [ ] Can you configure DNS clients?
- [ ] Can you troubleshoot DNS failures?
- [ ] Can you secure a DNS server?
- [ ] Can you document the DNS architecture?

---

# Summary

In this capstone project, you built a production-style DNS server using Linux and BIND9. You configured forward and reverse lookup zones, created DNS records, enabled client name resolution, configured DNS forwarding, secured the service, and validated the complete deployment.

This project mirrors the DNS infrastructure used in enterprise data centers, cloud environments, and production Kubernetes clusters where reliable name resolution is essential for application communication.

---

## Key Takeaways

- DNS translates **hostnames into IP addresses** and is a foundational network service.
- Configure both **forward** and **reverse lookup zones** for complete DNS functionality.
- Validate every configuration using `named-checkconf` and `named-checkzone`.
- Protect DNS with firewalls, restricted zone transfers, and logging.
- Deploy **secondary DNS servers** for redundancy and high availability.
- Monitor and document your DNS infrastructure to simplify operations and troubleshooting.

---

## What's Next?

**[Configure a DHCP Server](configure-dhcp-server.md)**

In the next capstone project, you'll learn how to **Configure a DHCP Server**.

You'll deploy an enterprise DHCP server, configure address pools and reservations, manage lease times, integrate DHCP with DNS, support multiple subnets, and automate IP address management for client systems.
