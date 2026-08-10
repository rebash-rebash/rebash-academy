---
title: "Access Control Lists (ACLs)"
description: "Learn Access Control Lists (ACLs) — standard vs extended filtering, permit/deny, implicit deny, inbound/outbound rules, and Linux iptables/nftables basics."
difficulty: intermediate
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
  - acl
  - firewall
  - packet-filtering
  - rebash-networking-mastery
comments: false
status: ready
---

# Access Control Lists (ACLs) — Controlling Network Traffic

> An **Access Control List (ACL)** is a set of rules used by routers, switches, and firewalls to **permit or deny network traffic** based on defined criteria such as **source IP address, destination IP address, protocol, and port number**. ACLs are one of the most fundamental security mechanisms in networking and are used to enforce security policies, restrict unauthorised access, and control packet forwarding. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand ACLs.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 7: NAT & Firewalls → Lesson 5</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 100 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** NAT & Firewalls</div>

<div markdown>**Lesson:** 5 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Access Control Lists (ACLs)
- Differentiate Standard and Extended ACLs
- Understand packet filtering
- Learn inbound and outbound ACLs
- Understand ACL processing order
- Apply ACLs in enterprise and cloud environments
- Troubleshoot ACL-related connectivity issues

---

# Prerequisites

Complete:

- [NAT](nat-and-port-forwarding.md)
- [PAT](pat.md)
- [Static NAT](static-nat.md)
- [Dynamic NAT](dynamic-nat.md)

---

# Why Learn ACLs?

Imagine a company wants:

- Employees to access the Internet
- HR servers accessible only by HR staff
- Database servers protected from public access

Without ACLs:

```text
Everyone

Can Access

Everything

❌
```

With ACLs:

```text
Only

Authorized Users

↓

Allowed
```

---

# What is an ACL?

An **Access Control List** is an ordered list of rules that determines whether network traffic is:

```text
Permit

OR

Deny
```

Each packet is checked against the ACL before being forwarded.

---

# ACL Workflow

```text
Packet Arrives

↓

Check ACL

↓

Rule Match?

↓

Permit

↓

Forward Packet

OR

Deny

↓

Drop Packet
```

---

# Why Use ACLs?

ACLs provide:

- Network Security
- Traffic Filtering
- Access Control
- Policy Enforcement
- Reduced Attack Surface
- Segmentation

---

# Types of ACLs

The two primary ACL types are:

- Standard ACL
- Extended ACL

---

# Standard ACL

A Standard ACL filters traffic based only on:

```text
Source IP Address
```

Example:

```text
Allow

192.168.10.0/24
```

It cannot filter based on:

- Destination IP
- Protocol
- Port Number

---

# Extended ACL

An Extended ACL can filter using:

- Source IP
- Destination IP
- Protocol
- Transmission Control Protocol (TCP) Port
- User Datagram Protocol (UDP) Port
- Internet Control Message Protocol (ICMP)

Example:

```text
Allow

HTTPS

To

Web Server
```

Extended ACLs provide much finer control.

---

# Permit and Deny

ACL rules are based on two actions:

```text
Permit
```

Traffic is allowed.

or

```text
Deny
```

Traffic is blocked.

---

# Implicit Deny

Every ACL ends with an invisible rule:

```text
Deny All
```

If traffic does not match any permit rule:

```text
Packet

Dropped
```

This is known as the **implicit deny**.

---

# ACL Processing Order

ACLs are evaluated:

```text
Top

↓

Bottom
```

The first matching rule is applied.

Example:

```text
Rule 1

Permit
```

↓

```text
Rule 2

Deny
```

If Rule 1 matches, Rule 2 is never evaluated.

---

# Inbound ACL

Applied to:

```text
Incoming Traffic
```

Workflow:

```text
Packet Arrives

↓

ACL

↓

Routing Decision
```

If denied, the packet is discarded before routing.

---

# Outbound ACL

Applied to:

```text
Outgoing Traffic
```

Workflow:

```text
Routing Decision

↓

ACL

↓

Forward Packet
```

The packet is filtered after the routing decision but before leaving the interface.

---

# Example Standard ACL

Requirement:

Allow only:

```text
192.168.10.0/24
```

All other sources:

```text
Denied
```

---

# Example Extended ACL

Requirement:

Allow HTTPS:

```text
TCP

443
```

to:

```text
Web Server
```

Block everything else.

---

# Enterprise Example

Company:

```text
Users

↓

Router

↓

ACL

↓

Database Server
```

Only:

```text
Application Servers

↓

Database
```

Direct user access is denied.

---

# Branch Office Example

Branch Users:

```text
Internet

↓

Allowed
```

Access to:

```text
Head Office

Finance Server

↓

Denied
```

ACLs enforce organisational security policies.

---

# Cloud Perspective

Cloud providers implement ACL-like functionality through:

- Network ACLs
- Route-Based Filtering
- Security Policies

ACLs can control traffic between:

- Subnets
- Virtual Networks
- Internet Gateways

---

# Kubernetes Perspective

Kubernetes uses **Network Policies** to control communication between Pods.

Although implemented differently, Network Policies serve a similar purpose to ACLs by controlling which workloads can communicate.

---

# Linux Perspective

Linux uses firewall frameworks to implement packet filtering.

Display nftables rules.

```bash
sudo nft list ruleset
```

Display iptables rules.

```bash
sudo iptables -L -n -v
```

Allow SSH using iptables.

```bash
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

Block ICMP using iptables.

```bash
sudo iptables -A INPUT -p icmp -j DROP
```

---

# ACL Packet Flow

```text
Client

↓

Router

↓

ACL

↓

Permit?

↓

Yes

↓

Server
```

If denied:

```text
Packet

Dropped
```

---

# Standard vs Extended ACL

| Standard ACL | Extended ACL |
|--------------|--------------|
| Filters Source IP | Filters Source and Destination IP |
| No Port Filtering | Supports Port Filtering |
| Simple | Granular |
| Basic Security | Advanced Security |

---

# Advantages of ACLs

- Improved Security
- Simple Traffic Filtering
- Low Resource Usage
- Policy Enforcement
- Network Segmentation
- Reduced Unauthorised Access

---

# Limitations

- Rule order is critical
- Large ACLs can become difficult to manage
- Traditional ACLs do not track connection state
- Incorrect rules can block legitimate traffic

---

# Hands-on Lab

## Task 1

Display iptables rules.

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

Allow SSH.

```bash
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

---

## Task 4

Block ICMP.

```bash
sudo iptables -A INPUT -p icmp -j DROP
```

---

## Task 5

Compare:

- Standard ACL
- Extended ACL

---

## Task 6

Draw an ACL processing diagram showing:

- Packet Arrival
- Rule Evaluation
- Permit
- Deny

---

## Task 7

Design ACL rules for:

- Web Server
- Database Server
- SSH Administration
- DNS Server

---

## Task 8

Research ACL implementations in:

- Cisco IOS
- Linux
- Cloud Platforms

Compare their capabilities.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `iptables -L -n -v` | Display iptables rules |
| `iptables -A` | Add firewall rule |
| `nft list ruleset` | Display nftables configuration |
| `ss -tuln` | Display listening ports |
| `ip addr` | Display IP configuration |

---

# Common Mistakes

❌ Forgetting the implicit deny rule.

✅ Add explicit permit rules for required traffic.

---

❌ Placing rules in the wrong order.

✅ Place the most specific rules before broader ones.

---

❌ Blocking management access.

✅ Test ACLs before applying them remotely.

---

❌ Using Standard ACLs when port filtering is required.

✅ Use Extended ACLs for protocol and port-based filtering.

---

❌ Leaving unused ACL rules in production.

✅ Periodically review and remove obsolete rules.

---

# Best Practices

- Follow the principle of least privilege.
- Keep ACLs as simple as possible.
- Place specific rules before general rules.
- Document every ACL.
- Test ACL changes in a non-production environment when possible.
- Regularly audit ACLs for unnecessary or outdated entries.

---

# Interview Questions

## Beginner

1. What is an ACL?
2. Why are ACLs used?
3. What is the difference between Permit and Deny?
4. What is the implicit deny rule?

---

## Intermediate

1. Compare Standard and Extended ACLs.
2. Explain inbound and outbound ACLs.
3. Why is ACL rule order important?
4. How do ACLs improve network security?

---

## Architect Level

1. Design ACLs for a multi-tier enterprise application.
2. Explain how ACLs integrate with firewalls and cloud security.
3. How would you troubleshoot connectivity issues caused by an ACL?

---

# Summary

In this lesson, you learned:

- Access Control Lists (ACLs)
- Standard ACLs
- Extended ACLs
- Packet Filtering
- Permit and Deny Rules
- Implicit Deny
- Inbound and Outbound ACLs
- ACL Processing Order
- Enterprise ACL Design
- Linux Packet Filtering

ACLs are one of the most important network security mechanisms. They provide a simple yet effective way to control network traffic, enforce security policies, and reduce unauthorised access. Proper ACL design, rule ordering, and regular reviews are essential for maintaining secure and reliable enterprise and cloud networks.

---

## Key Takeaways

- ACLs control whether network traffic is **permitted or denied**.
- **Standard ACLs** filter based on source IP addresses.
- **Extended ACLs** filter by source, destination, protocol, and ports.
- ACLs are processed **top to bottom**, and the first matching rule is applied.
- Every ACL has an **implicit deny** at the end.
- Well-designed ACLs improve network security and reduce the attack surface.

---

## What's Next?

**[Firewall Basics](firewalls-and-access-control.md)**

In the next lesson, you'll learn about **Firewall Basics**.

You'll explore:

- What a Firewall is
- Packet Filtering
- Firewall Architectures
- Network Zones
- Stateful vs Stateless Filtering
- Firewall Deployment Models
- Enterprise Security Best Practices

By the end of the lesson, you'll understand how firewalls inspect, filter, and protect network traffic across enterprise, cloud, and hybrid environments.
