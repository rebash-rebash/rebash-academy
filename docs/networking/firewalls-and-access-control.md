---
title: "Firewall Basics"
description: "Learn firewall fundamentals — packet filtering, security zones, DMZ, inbound/outbound policies, and Linux iptables, nftables, and UFW basics."
difficulty: beginner
estimated_time: "100 min"
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
  - dmz
  - packet-filtering
  - rebash-networking-mastery
comments: false
status: ready
---

# Firewall Basics — Protecting Networks from Unauthorized Access

> A **Firewall** is a network security device or software application that **monitors, filters, and controls network traffic** based on predefined security rules. It acts as a protective barrier between trusted and untrusted networks, deciding which traffic is allowed and which should be blocked. Firewalls are a fundamental component of cybersecurity and are used in enterprise networks, data centres, cloud platforms, Kubernetes clusters, and personal computers. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand firewall fundamentals.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 7: NAT & Firewalls → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 100 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** NAT & Firewalls</div>

<div markdown>**Lesson:** 6 of 10</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Firewalls
- Learn packet filtering
- Understand firewall architectures
- Learn network security zones
- Understand firewall deployment models
- Apply firewalls in enterprise and cloud environments
- Troubleshoot basic firewall issues

---

# Prerequisites

Complete:

- [NAT](nat-and-port-forwarding.md)
- [PAT](pat.md)
- [Static NAT](static-nat.md)
- [Dynamic NAT](dynamic-nat.md)
- [ACL](acl.md)

---

# Why Learn Firewalls?

Imagine a company has:

- Internal Applications
- Databases
- Employee Laptops
- Internet Access

Without a firewall:

```text
Internet

↓

Direct Access

↓

Internal Servers

❌
```

With a firewall:

```text
Internet

↓

Firewall

↓

Inspect Traffic

↓

Allow

OR

Block
```

---

# What is a Firewall?

A **Firewall** is a security system that inspects network traffic and applies security rules.

It decides whether traffic should be:

```text
Permit

OR

Deny
```

based on configured policies.

---

# Firewall Objectives

Firewalls help:

- Prevent Unauthorised Access
- Protect Internal Networks
- Block Malicious Traffic
- Control Network Communication
- Enforce Security Policies
- Log Network Activity

---

# Firewall Workflow

```text
Packet Arrives

↓

Firewall

↓

Inspect Rules

↓

Allow

OR

Block

↓

Forward

OR

Drop
```

---

# Packet Filtering

A firewall examines packet information such as:

- Source IP Address
- Destination IP Address
- Protocol
- Source Port
- Destination Port
- Interface
- Direction

Based on this information, the firewall applies its rules.

---

# Firewall Rule Example

Rule:

```text
Allow

HTTPS

TCP 443
```

Traffic:

```text
Client

↓

HTTPS

↓

Allowed
```

Another rule:

```text
Block

Telnet

TCP 23
```

Traffic:

```text
Client

↓

Telnet

↓

Blocked
```

---

# Firewall Placement

A firewall is commonly placed:

```text
Internet

↓

Firewall

↓

Internal Network
```

or

```text
Internet

↓

Firewall

↓

DMZ

↓

Internal Network
```

This ensures all inbound and outbound traffic passes through security controls.

---

# Network Security Zones

Firewalls often separate networks into security zones.

Common zones include:

- Internet (Untrusted)
- Demilitarised Zone (DMZ)
- Internal Network (Trusted)
- Management Network

Example:

```text
Internet

↓

DMZ

↓

Internal Local Area Network (LAN)
```

---

# Trusted vs Untrusted Networks

Trusted:

- Internal LAN
- Corporate Servers
- Management Network

Untrusted:

- Public Internet
- Unknown External Networks

Firewalls enforce different policies between these zones.

---

# DMZ (Demilitarised Zone)

A DMZ is a network segment for publicly accessible services.

Examples:

- Web Server
- Mail Server
- Reverse Proxy
- API Gateway

Architecture:

```text
Internet

↓

Firewall

↓

DMZ

↓

Firewall

↓

Internal Network
```

Even if a DMZ server is compromised, the internal network remains protected.

---

# Inbound Traffic

Traffic entering the network.

Example:

```text
Internet

↓

Firewall

↓

Web Server
```

The firewall determines whether the request should be allowed.

---

# Outbound Traffic

Traffic leaving the network.

Example:

```text
Employee Laptop

↓

Firewall

↓

Internet
```

Organisations often restrict outbound traffic to approved services.

---

# Firewall Policies

A firewall policy consists of:

- Source
- Destination
- Protocol
- Port
- Action

Example:

```text
Source:

Internal LAN

↓

Destination:

Internet

↓

HTTPS

↓

Allow
```

---

# Types of Firewalls

Common firewall categories include:

- Packet Filtering Firewalls
- Stateful Firewalls
- Next-Generation Firewalls (NGFW)
- Web Application Firewalls (WAF)
- Host-Based Firewalls

The next lesson focuses on Stateful Firewalls.

---

# Enterprise Example

Company:

```text
Internet

↓

Firewall

↓

DMZ

↓

Application Server

↓

Database
```

Firewall rules allow:

- HTTPS to the Web Server
- Application Server to Database

Direct Internet access to the database is denied.

---

# Branch Office Example

```text
Branch Office

↓

Firewall

↓

Virtual Private Network (VPN)

↓

Head Office
```

The firewall protects branch users while allowing secure VPN communication.

---

# Cloud Perspective

Cloud platforms provide firewall functionality through:

- Virtual Firewalls
- Network Security Policies
- Security Groups
- Network Access Control Lists (ACLs)

Firewalls protect:

- Virtual Machines
- Load Balancers
- Databases
- Kubernetes Clusters

---

# Kubernetes Perspective

Kubernetes security uses multiple layers.

Examples:

- Network Policies
- Ingress Controllers
- Service Mesh
- Cloud Firewalls

Together they help control communication between workloads and external systems.

---

# Linux Perspective

Linux provides host-based firewall solutions.

View nftables rules.

```bash
sudo nft list ruleset
```

View iptables rules.

```bash
sudo iptables -L -n -v
```

View Uncomplicated Firewall (UFW) status (Ubuntu).

```bash
sudo ufw status
```

Allow SSH.

```bash
sudo ufw allow 22/tcp
```

Enable UFW.

```bash
sudo ufw enable
```

---

# Firewall Packet Flow

```text
Client

↓

Firewall

↓

Inspect Rules

↓

Permit?

↓

Yes

↓

Server

OR

No

↓

Drop Packet
```

---

# Advantages of Firewalls

- Improved Security
- Controlled Network Access
- Reduced Attack Surface
- Centralised Policy Enforcement
- Traffic Monitoring
- Event Logging

---

# Limitations

- Incorrect rules can block legitimate traffic
- Firewalls cannot stop every attack
- Misconfiguration creates security risks
- Performance may be affected under heavy traffic if undersized

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

Allow SSH.

```bash
sudo ufw allow 22/tcp
```

---

## Task 5

Enable UFW.

```bash
sudo ufw enable
```

---

## Task 6

Draw a firewall architecture showing:

- Internet
- Firewall
- DMZ
- Internal Network

---

## Task 7

Design firewall rules for:

- Web Server
- Mail Server
- SSH Administration
- Database Server

---

## Task 8

Compare:

- ACL
- Firewall

Explain where each is typically used.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `iptables -L -n -v` | Display iptables rules |
| `nft list ruleset` | Display nftables rules |
| `ufw status` | Display UFW status |
| `ufw allow 22/tcp` | Allow SSH |
| `ufw enable` | Enable UFW |
| `ss -tuln` | Display listening ports |

---

# Common Mistakes

❌ Allowing unnecessary services.

✅ Permit only required traffic.

---

❌ Blocking SSH before verifying alternate access.

✅ Test firewall changes carefully.

---

❌ Assuming firewalls replace endpoint security.

✅ Use layered security controls.

---

❌ Ignoring outbound traffic filtering.

✅ Restrict outbound access where appropriate.

---

❌ Never reviewing firewall rules.

✅ Regularly audit and remove unused rules.

---

# Best Practices

- Follow the principle of least privilege.
- Deny traffic by default and explicitly allow required services.
- Separate networks using security zones.
- Log important firewall events.
- Review firewall policies regularly.
- Keep firewall software and firmware updated.

---

# Interview Questions

## Beginner

1. What is a firewall?
2. Why are firewalls used?
3. What is packet filtering?
4. What is a DMZ?

---

## Intermediate

1. Explain firewall security zones.
2. What is the difference between inbound and outbound firewall rules?
3. Compare ACLs and firewalls.
4. Why should databases not be directly exposed to the Internet?

---

## Architect Level

1. Design a firewall architecture for a three-tier enterprise application.
2. Explain firewall deployment in hybrid cloud environments.
3. How would you troubleshoot an application that is inaccessible due to firewall rules?

---

# Summary

In this lesson, you learned:

- Firewall Fundamentals
- Packet Filtering
- Security Policies
- Network Security Zones
- DMZ
- Inbound and Outbound Filtering
- Firewall Architectures
- Enterprise Firewalls
- Linux Firewall Tools

Firewalls are one of the most important components of network security. They inspect network traffic, enforce security policies, protect trusted networks from untrusted ones, and provide centralised control over communication between systems. Firewalls play a critical role in securing enterprise networks, cloud environments, and modern applications.

---

## Key Takeaways

- A firewall **monitors and filters network traffic**.
- Firewall rules determine whether traffic is **allowed or blocked**.
- Firewalls commonly separate **trusted** and **untrusted** networks.
- A **DMZ** protects internal systems while exposing public services.
- Linux provides host-based firewall tools such as **iptables**, **nftables**, and **UFW**.
- Firewalls should follow the **principle of least privilege** and be reviewed regularly.

---

## What's Next?

**[Stateful Firewalls](stateful-firewalls.md)**

In the next lesson, you'll learn about **Stateful Firewalls**.

You'll explore:

- Stateful vs Stateless Firewalls
- Connection Tracking
- Session Tables
- TCP State Inspection
- Dynamic Rule Handling
- Enterprise Firewall Design
- Performance and Security Benefits

By the end of the lesson, you'll understand how stateful firewalls intelligently track active connections and make more informed security decisions than simple packet-filtering firewalls.
