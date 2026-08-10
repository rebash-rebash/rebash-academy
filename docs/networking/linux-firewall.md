---
title: "Linux Firewall"
description: "Learn Linux host firewalls — Netfilter, iptables, nftables, UFW, firewalld, connection tracking, and practical hardening rules."
difficulty: intermediate
estimated_time: "120 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 7 · NAT and Firewalls"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - firewall
  - iptables
  - nftables
  - ufw
  - firewalld
  - rebash-networking-mastery
comments: false
status: ready
---

# Linux Firewall — Securing Linux Systems with Netfilter, iptables, nftables, UFW, and firewalld

> A **Linux Firewall** is a host-based security mechanism that controls inbound, outbound, and forwarded network traffic on a Linux system. Modern Linux distributions implement firewall functionality through the **Netfilter** framework in the Linux kernel, while user-space tools such as **iptables**, **nftables**, **Uncomplicated Firewall (UFW)**, and **firewalld** provide interfaces for configuring firewall rules. Linux firewalls are widely used to secure servers, virtual machines, containers, Kubernetes nodes, and cloud workloads. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand Linux firewalls.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 7: NAT & Firewalls → Lesson 8</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 120 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** NAT & Firewalls</div>

<div markdown>**Lesson:** 8 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Linux Firewall architecture
- Learn Netfilter
- Understand iptables
- Learn nftables
- Configure UFW
- Configure firewalld
- Troubleshoot Linux firewall issues

---

# Prerequisites

Complete:

- [NAT](nat-and-port-forwarding.md)
- [PAT](pat.md)
- [Static NAT](static-nat.md)
- [Dynamic NAT](dynamic-nat.md)
- [ACL](acl.md)
- [Firewall Basics](firewalls-and-access-control.md)
- [Stateful Firewalls](stateful-firewalls.md)

---

# Why Learn Linux Firewalls?

Imagine a Linux server hosting:

- Web Application
- SSH
- Database
- API

Without a firewall:

```text
Internet

↓

Everything

Accessible

❌
```

With a firewall:

```text
Internet

↓

Firewall

↓

Only Required

Ports

↓

Allowed
```

---

# What is a Linux Firewall?

A Linux Firewall filters:

- Incoming Traffic
- Outgoing Traffic
- Forwarded Traffic

using rules configured through the Linux networking stack.

---

# Netfilter

At the core of Linux firewalling is:

```text
Netfilter
```

Netfilter is built into the Linux kernel.

Responsibilities include:

- Packet Filtering
- Network Address Translation (NAT)
- Connection Tracking
- Packet Modification
- Logging

---

# Linux Firewall Architecture

```text
Applications

↓

Socket

↓

Netfilter

↓

Firewall Rules

↓

Network Interface

↓

Network
```

All packets pass through Netfilter before entering or leaving the system.

---

# Netfilter Hooks

Packets pass through several processing stages.

```text
PREROUTING

↓

INPUT

↓

FORWARD

↓

OUTPUT

↓

POSTROUTING
```

Each hook allows firewall rules to inspect or modify packets.

---

# INPUT Chain

Used for:

```text
Traffic

↓

Destined

For

This Server
```

Example:

SSH

```text
Client

↓

Server
```

---

# OUTPUT Chain

Used for:

```text
Traffic

↓

Generated

By

This Server
```

Example:

```text
Linux Server

↓

Internet
```

---

# FORWARD Chain

Used when the Linux system acts as:

- Router
- Gateway
- Firewall Appliance

Traffic passes:

```text
Client

↓

Linux Router

↓

Internet
```

---

# iptables

For many years, Linux firewall management was performed using:

```text
iptables
```

Example:

Display rules.

```bash
sudo iptables -L -n -v
```

Allow SSH.

```bash
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

Allow HTTPS.

```bash
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

Block Telnet.

```bash
sudo iptables -A INPUT -p tcp --dport 23 -j DROP
```

---

# Default Policy

Display policies.

```bash
sudo iptables -L
```

Set default INPUT policy.

```bash
sudo iptables -P INPUT DROP
```

Set OUTPUT policy.

```bash
sudo iptables -P OUTPUT ACCEPT
```

---

# Save iptables Rules

On Debian/Ubuntu:

```bash
sudo apt install iptables-persistent
```

Save rules.

```bash
sudo netfilter-persistent save
```

---

# nftables

Modern Linux distributions increasingly use:

```text
nftables
```

Advantages:

- Simpler Syntax
- Better Performance
- Unified IPv4/IPv6 Rules
- Improved Scalability

Display rules.

```bash
sudo nft list ruleset
```

---

# Create nftables Table

```bash
sudo nft add table inet filter
```

Create INPUT chain.

```bash
sudo nft add chain inet filter input { type filter hook input priority 0 \; policy drop \; }
```

Allow SSH.

```bash
sudo nft add rule inet filter input tcp dport 22 accept
```

---

# UFW (Uncomplicated Firewall)

Ubuntu provides:

```text
UFW
```

Check status.

```bash
sudo ufw status
```

Enable firewall.

```bash
sudo ufw enable
```

Allow SSH.

```bash
sudo ufw allow ssh
```

Allow HTTPS.

```bash
sudo ufw allow 443/tcp
```

Deny Telnet.

```bash
sudo ufw deny 23/tcp
```

---

# firewalld

Many Red Hat-based distributions use:

```text
firewalld
```

Check status.

```bash
sudo firewall-cmd --state
```

List active zones.

```bash
sudo firewall-cmd --get-active-zones
```

Allow HTTP.

```bash
sudo firewall-cmd --permanent --add-service=http
```

Reload configuration.

```bash
sudo firewall-cmd --reload
```

---

# Firewall Zones (firewalld)

Common zones:

- public
- internal
- trusted
- dmz
- work
- home
- drop

Each zone applies different trust levels.

---

# Connection Tracking

Linux firewalls use:

```text
conntrack
```

View active sessions.

```bash
sudo conntrack -L
```

Example rule:

```bash
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```

---

# Logging

Log dropped packets.

```bash
sudo iptables -A INPUT -j LOG
```

View logs.

```bash
journalctl -k
```

or

```bash
dmesg
```

---

# Enterprise Example

Linux Web Server:

```text
Internet

↓

Firewall

↓

HTTPS

↓

Allowed
```

SSH:

```text
Admin Network

↓

Allowed
```

Everything else:

```text
Blocked
```

---

# Cloud Perspective

Linux firewalls provide **host-level protection** inside cloud virtual machines.

Cloud environments often use multiple layers:

- Cloud Security Groups
- Network Access Control Lists (ACLs)
- Linux Firewall

All layers work together to provide defence in depth.

---

# Kubernetes Perspective

Linux firewalls are used on:

- Kubernetes Worker Nodes
- Control Plane Nodes
- Bastion Hosts

Container networking solutions and Kubernetes Network Policies complement, but do not replace, host firewall protection.

---

# Linux Firewall Packet Flow

```text
Internet

↓

Network Interface

↓

Netfilter

↓

Firewall Rules

↓

Application
```

---

# iptables vs nftables vs UFW vs firewalld

| Tool | Purpose |
|------|----------|
| iptables | Traditional firewall configuration |
| nftables | Modern Linux firewall framework |
| UFW | Simplified firewall for Ubuntu |
| firewalld | Dynamic firewall management for RHEL-based systems |

---

# Advantages of Linux Firewalls

- Host-Level Protection
- Flexible Rule Management
- Stateful Packet Inspection
- NAT Support
- Logging
- Integration with Enterprise Security

---

# Limitations

- Incorrect rules can block legitimate traffic
- Complex configurations require careful management
- Rules must be persisted across reboots if not handled automatically
- Multiple firewall management tools should not be configured independently on the same host without understanding their interaction

---

# Hands-on Lab

## Task 1

Display firewall rules.

```bash
sudo iptables -L -n -v
```

---

## Task 2

Display nftables configuration.

```bash
sudo nft list ruleset
```

---

## Task 3

Check UFW status.

```bash
sudo ufw status
```

---

## Task 4

Check firewalld status.

```bash
sudo firewall-cmd --state
```

---

## Task 5

Display active firewall sessions.

```bash
sudo conntrack -L
```

---

## Task 6

Allow SSH using UFW.

```bash
sudo ufw allow ssh
```

---

## Task 7

Allow HTTP using firewalld.

```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
```

---

## Task 8

Design firewall rules for a Linux server hosting:

- SSH
- HTTPS
- Domain Name System (DNS)
- PostgreSQL

Only expose services that require external access.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `iptables -L -n -v` | Display iptables rules |
| `iptables -A` | Add iptables rule |
| `nft list ruleset` | Display nftables rules |
| `ufw status` | Display UFW status |
| `ufw allow ssh` | Allow SSH |
| `firewall-cmd --state` | Display firewalld status |
| `firewall-cmd --reload` | Reload firewalld |
| `conntrack -L` | Display tracked connections |
| `journalctl -k` | Display kernel firewall logs |

---

# Common Mistakes

❌ Locking yourself out of SSH.

✅ Allow SSH before enabling restrictive firewall rules.

---

❌ Forgetting to persist firewall rules.

✅ Save rules or use firewall management tools that support persistence.

---

❌ Running multiple firewall managers without understanding their interaction.

✅ Standardise on the appropriate tool for the distribution.

---

❌ Allowing unnecessary ports.

✅ Follow the principle of least privilege.

---

❌ Ignoring firewall logs.

✅ Review logs regularly to identify blocked traffic and suspicious activity.

---

# Best Practices

- Allow only required services.
- Set restrictive default policies.
- Use stateful inspection.
- Keep firewall rules simple and documented.
- Regularly audit open ports.
- Log important firewall events.
- Test firewall changes before production deployment.
- Combine host firewalls with network firewalls for layered security.

---

# Interview Questions

## Beginner

1. What is Netfilter?
2. What is iptables?
3. What is nftables?
4. What is UFW?

---

## Intermediate

1. Compare iptables and nftables.
2. What is firewalld?
3. Explain Netfilter hooks.
4. How do you allow SSH while blocking other unnecessary services?

---

## Architect Level

1. Design firewall rules for a production Linux web server.
2. Explain layered security using cloud firewalls and host-based firewalls.
3. How would you troubleshoot an application that is unreachable because of Linux firewall rules?

---

# Summary

In this lesson, you learned:

- Linux Firewall
- Netfilter
- Netfilter Hooks
- iptables
- nftables
- UFW
- firewalld
- Connection Tracking
- Firewall Logging
- Enterprise Linux Firewall Design

Linux firewalls provide host-level security by filtering network traffic before it reaches applications. Powered by the Netfilter framework and managed through tools such as iptables, nftables, UFW, and firewalld, Linux firewalls are an essential component of securing servers, cloud workloads, Kubernetes nodes, and enterprise infrastructure.

---

## Key Takeaways

- **Netfilter** is the Linux kernel framework for firewalling and packet processing.
- **iptables** and **nftables** are powerful tools for configuring firewall rules.
- **UFW** simplifies firewall management on Ubuntu systems.
- **firewalld** provides dynamic firewall management on Red Hat-based systems.
- Linux firewalls support **stateful packet inspection**, **NAT**, and **connection tracking**.
- A host-based firewall should complement network and cloud firewalls as part of a layered security strategy.

---

## What's Next?

**[Cloud Firewalls](cloud-firewalls.md)**

In the next lesson, you'll learn about **Cloud Firewalls**.

You'll explore:

- Cloud-Native Firewall Concepts
- Amazon Web Services (AWS) Security Groups
- Microsoft Azure Network Security Groups (NSGs)
- Google Cloud Virtual Private Cloud (VPC) Firewall Rules
- Distributed Firewall Architectures
- Zero Trust Networking
- Cloud Firewall Best Practices

By the end of the lesson, you'll understand how cloud providers secure workloads using virtual firewall technologies and how these integrate with host-based firewalls and enterprise security architectures.
