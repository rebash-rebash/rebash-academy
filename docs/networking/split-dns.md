---
title: "Split DNS"
description: "Learn Split-Horizon DNS — internal vs external views, private and public zones, hybrid cloud patterns, and dig-based verification."
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
  - dns
  - split-dns
  - split-horizon
  - rebash-networking-mastery
comments: false
status: ready
---

# Split DNS — Providing Different DNS Answers for Internal and External Users

> **Split DNS** (also called **Split-Horizon DNS**, **Split-Brain DNS**, or **Split-View DNS**) is a Domain Name System (DNS) architecture where the **same domain name returns different DNS responses depending on where the request originates**. Internal users receive private IP addresses and internal services, while external users receive public IP addresses and Internet-facing services. Split DNS improves **security**, **performance**, and **network management** by separating internal and external DNS views. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand Split DNS.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 6: DNS & DHCP → Lesson 6</p>

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

<div markdown>**Lesson:** 6 of 7</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Split DNS
- Learn why Split DNS is needed
- Differentiate Internal and External DNS
- Understand Public and Private DNS Zones
- Apply Split DNS in enterprise and cloud environments
- Troubleshoot Split DNS issues

---

# Prerequisites

Complete:

- [DNS Fundamentals](dns-fundamentals.md)
- [DNS Records](dns-records-and-troubleshooting.md)
- [DNS Resolution](dns-resolution.md)
- [DHCP Process](icmp-arp-dhcp-and-network-services.md)
- [DHCP Relay](dhcp-relay.md)

---

# Why Learn Split DNS?

Imagine a company owns:

```text
company.com
```

Employees access:

```text
portal.company.com
```

from inside the office.

Customers access:

```text
www.company.com
```

from the Internet.

Should both users receive the same IP address?

Usually:

```text
No
```

Internal users often need private services, while external users should only reach public services.

---

# What is Split DNS?

Split DNS provides:

```text
Same Domain Name

↓

Different DNS Answers
```

Depending on:

- Internal Network
- External Internet

---

# Example

Internal User:

```text
portal.company.com

↓

10.10.20.15
```

External User:

```text
portal.company.com

↓

203.0.113.25
```

Same hostname.

Different IP addresses.

---

# Internal DNS

Internal DNS servers resolve:

- File Servers
- Active Directory
- Internal Applications
- Databases
- Monitoring Systems
- Kubernetes Services

Example:

```text
db.company.com

↓

10.10.30.15
```

---

# External DNS

Public DNS servers resolve:

- Company Website
- Public APIs
- Email Services
- Virtual Private Network (VPN) Gateway
- Customer Portals

Example:

```text
www.company.com

↓

198.51.100.25
```

---

# Internal DNS Zone

Example:

```text
company.com

↓

portal

↓

10.10.10.20
```

Accessible only from the internal network.

---

# External DNS Zone

Example:

```text
company.com

↓

www

↓

198.51.100.25
```

Accessible from anywhere on the Internet.

---

# Split DNS Architecture

```text
Internal Users

↓

Internal DNS

↓

Private Zone

↓

Private IP
```

```text
Internet Users

↓

Public DNS

↓

Public Zone

↓

Public IP
```

---

# Internal Resolution

Employee:

```text
portal.company.com
```

Workflow:

```text
Laptop

↓

Internal DNS

↓

Private Zone

↓

10.10.10.20
```

Traffic never leaves the internal network.

---

# External Resolution

Customer:

```text
portal.company.com
```

Workflow:

```text
Browser

↓

Public DNS

↓

Public Zone

↓

198.51.100.25
```

The customer reaches the Internet-facing application.

---

# Why Use Split DNS?

Benefits include:

- Improved Security
- Internal Resource Protection
- Better Performance
- Reduced Internet Traffic
- Easier Management
- Simplified Hybrid Cloud Access

---

# Enterprise Example

Company Services:

Internal:

```text
git.company.com

↓

10.10.20.50
```

External:

```text
www.company.com

↓

198.51.100.20
```

Developers access internal Git servers while customers access only public services.

---

# Active Directory Example

Microsoft Active Directory commonly uses internal DNS.

Example:

```text
dc01.company.local
```

or

```text
dc01.company.com
```

These records are typically not exposed on the public Internet.

---

# Cloud Perspective

Cloud environments frequently implement Split DNS.

Examples:

- Private DNS Zones
- Public DNS Zones
- Private Endpoints
- Internal Load Balancers
- Public Load Balancers

Applications inside the cloud resolve private addresses, while Internet users receive public addresses.

---

# Hybrid Cloud Example

```text
On-Premises

↓

Private DNS

↓

VPN

↓

Cloud

↓

Private Endpoint
```

External users:

```text
Internet

↓

Public DNS

↓

Public Website
```

The same domain can support both environments.

---

# Kubernetes Perspective

Kubernetes commonly uses internal DNS.

Example:

```text
api.default.svc.cluster.local
```

External users access:

```text
api.company.com
```

using public DNS.

Internal cluster services remain private.

---

# Linux Perspective

Query DNS.

```bash
dig company.com
```

Query a specific DNS server.

```bash
dig @10.10.10.10 company.com
```

Query a public resolver.

```bash
dig @8.8.8.8 company.com
```

Display configured DNS servers.

```bash
cat /etc/resolv.conf
```

---

# Split DNS Example

Internal:

```text
mail.company.com

↓

10.10.10.50
```

External:

```text
mail.company.com

↓

198.51.100.50
```

Users receive different answers based on where the query originates.

---

# Advantages of Split DNS

- Stronger Security
- Better Performance
- Private Resource Protection
- Reduced Wide Area Network (WAN) Traffic
- Flexible Network Design
- Improved User Experience

---

# Limitations

- More complex DNS administration
- Internal and external zones must remain synchronised where appropriate
- Incorrect configuration can cause inconsistent DNS responses
- Troubleshooting requires checking both DNS views

---

# Hands-on Lab

## Task 1

Display configured DNS servers.

```bash
cat /etc/resolv.conf
```

---

## Task 2

Query a domain.

```bash
dig company.com
```

---

## Task 3

Query a specific internal DNS server.

```bash
dig @10.10.10.10 company.com
```

---

## Task 4

Query a public DNS server.

```bash
dig @8.8.8.8 company.com
```

---

## Task 5

Compare:

- Internal DNS
- External DNS

---

## Task 6

Design Split DNS for:

- Public Website
- Employee Portal
- Git Server
- VPN Gateway

---

## Task 7

Draw the Split DNS architecture showing:

- Internal Users
- Internal DNS
- External Users
- Public DNS

---

## Task 8

Research how Split DNS is implemented in:

- Amazon Web Services (AWS)
- Microsoft Azure
- Google Cloud

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `dig domain.com` | Query DNS |
| `dig @server domain.com` | Query a specific DNS server |
| `nslookup domain.com` | Perform DNS lookup |
| `host domain.com` | Display DNS information |
| `cat /etc/resolv.conf` | View configured DNS servers |

---

# Common Mistakes

❌ Publishing internal IP addresses in public DNS.

✅ Keep private records only in internal DNS zones.

---

❌ Forgetting to update both DNS views.

✅ Synchronise shared records carefully.

---

❌ Using public DNS for internal services.

✅ Configure clients to use internal DNS resolvers.

---

❌ Assuming Split DNS replaces firewalls.

✅ Continue enforcing network security controls.

---

❌ Troubleshooting only one DNS view.

✅ Verify both internal and external responses.

---

# Best Practices

- Maintain separate internal and external DNS zones.
- Publish only necessary public records.
- Protect internal DNS servers from Internet access.
- Monitor DNS consistency between zones.
- Document internal and external DNS architectures.
- Test name resolution from both internal and external networks.

---

# Interview Questions

## Beginner

1. What is Split DNS?
2. Why is Split DNS used?
3. What is the difference between internal and external DNS?
4. What is a private DNS zone?

---

## Intermediate

1. Explain how Split DNS improves security.
2. How does Split DNS work?
3. Compare public and private DNS zones.
4. What are common Split DNS use cases?

---

## Architect Level

1. Design a Split DNS architecture for a hybrid cloud enterprise.
2. How would you secure internal DNS infrastructure?
3. How would you troubleshoot inconsistent DNS responses between internal and external users?

---

# Summary

In this lesson, you learned:

- Split DNS
- Internal DNS
- External DNS
- Public DNS Zones
- Private DNS Zones
- Enterprise DNS Architecture
- Hybrid Cloud DNS
- Kubernetes DNS Integration
- Linux DNS Query Commands

Split DNS allows organisations to return different DNS responses based on the source of the request. Internal users receive private addresses and access internal services, while external users receive public addresses for Internet-facing applications. This architecture improves security, simplifies management, and supports modern enterprise and hybrid cloud deployments.

---

## Key Takeaways

- Split DNS provides **different DNS responses** for internal and external users.
- Internal DNS resolves **private services** using private IP addresses.
- External DNS resolves **public services** using public IP addresses.
- Split DNS enhances security by hiding internal infrastructure.
- Private and public DNS zones should be managed carefully.
- Split DNS is widely used in enterprise, cloud, and hybrid environments.

---

## What's Next?

**[DNS Troubleshooting](dns-troubleshooting.md)**

In the next lesson, you'll learn about **DNS Troubleshooting**.

You'll explore:

- Common DNS Problems
- DNS Resolution Failures
- DNS Cache Issues
- DNS Propagation
- Diagnostic Tools
- Linux DNS Troubleshooting Commands
- Enterprise Troubleshooting Methodology

By the end of the lesson, you'll be able to diagnose and resolve common DNS issues using systematic troubleshooting techniques and Linux networking tools.
