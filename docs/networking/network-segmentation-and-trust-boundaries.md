---
title: "Network Segmentation"
description: "Learn network segmentation — VLANs, physical vs logical isolation, micro-segmentation, East-West traffic control, and Zero Trust alignment."
difficulty: intermediate
estimated_time: "120 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 8 · Network Security"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - segmentation
  - vlan
  - micro-segmentation
  - rebash-networking-mastery
comments: false
status: ready
---

# Network Segmentation — Dividing Networks for Better Security and Performance

> **Network Segmentation** is the practice of dividing a computer network into smaller, isolated segments to improve **security, performance, availability, and manageability**. Instead of allowing unrestricted communication across the entire network, segmentation limits traffic between network zones based on business and security requirements. Modern enterprises use network segmentation to reduce attack surfaces, prevent lateral movement, improve compliance, and implement Zero Trust architectures. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand network segmentation.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 8: Network Security → Lesson 8</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 120 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Network Security</div>

<div markdown>**Lesson:** 8 of 9</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Network Segmentation
- Compare Physical and Logical Segmentation
- Learn VLAN-Based Segmentation
- Understand Micro-Segmentation
- Control East-West Traffic
- Design secure enterprise networks
- Apply segmentation in cloud and Kubernetes environments

---

# Prerequisites

Complete:

- [VPN](vpn-and-tunneling-basics.md)
- [IPSec](ipsec.md)
- [SSL/TLS](ssl-tls.md)
- [SSH](ssh-networking.md)
- [Network Hardening](network-security-hardening.md)
- [IDS/IPS](ids-ips.md)
- [Zero Trust](zero-trust.md)

---

# Why Learn Network Segmentation?

Imagine an enterprise where:

- Finance
- HR
- Engineering
- Database Servers
- User PCs

all share one network.

```text
Single Flat Network

↓

Everyone

Can Reach

Everything

❌
```

If one computer is compromised:

```text
Attacker

↓

Entire Network

At Risk
```

With segmentation:

```text
Finance

↓

Separate Network
```

```text
Engineering

↓

Separate Network
```

```text
Database

↓

Separate Network
```

Attackers cannot freely move across the organisation.

---

# What is Network Segmentation?

Network Segmentation divides a network into:

```text
Smaller

Independent

Network Segments
```

Each segment has:

- Security Policies
- Access Controls
- Firewall Rules
- Traffic Restrictions

---

# Goals of Network Segmentation

Segmentation provides:

- Better Security
- Reduced Attack Surface
- Improved Performance
- Regulatory Compliance
- Easier Troubleshooting
- Better Traffic Control

---

# Flat Network vs Segmented Network

## Flat Network

```text
All Devices

↓

Same Broadcast Domain
```

Problems:

- Large Broadcast Traffic
- Easy Lateral Movement
- Poor Security

---

## Segmented Network

```text
Users

↓

Application

↓

Database

↓

Management
```

Each network is isolated.

---

# Types of Segmentation

Organisations commonly use:

- Physical Segmentation
- Logical Segmentation
- VLAN Segmentation
- Micro-Segmentation

---

# Physical Segmentation

Uses:

- Separate Switches
- Separate Routers
- Separate Firewalls
- Separate Cabling

Example:

```text
Finance Network

↓

Dedicated Switch
```

Highly secure but more expensive.

---

# Logical Segmentation

Uses:

- Virtual Local Area Networks (VLANs)
- Subnets
- Routing
- Access Control Lists (ACLs)
- Firewalls

No additional physical hardware is required.

---

# VLAN-Based Segmentation

Example:

```text
VLAN 10

Finance
```

```text
VLAN 20

Engineering
```

```text
VLAN 30

HR
```

Communication between VLANs requires routing and can be controlled using firewalls or ACLs.

---

# Subnet Segmentation

Example:

```text
Finance

10.10.10.0/24
```

```text
Engineering

10.10.20.0/24
```

```text
Database

10.10.30.0/24
```

Each subnet represents a separate network segment.

---

# Security Zones

Networks are often divided into security zones.

Example:

```text
Internet

↓

Demilitarised Zone (DMZ)

↓

Application

↓

Database

↓

Management
```

Each zone has its own security policy.

---

# East-West Traffic

Traffic between internal systems is called:

```text
East-West Traffic
```

Example:

```text
Web Server

↓

Application Server

↓

Database
```

Modern security solutions inspect this internal traffic to prevent lateral movement.

---

# North-South Traffic

Traffic entering or leaving the organisation.

```text
Internet

↓

Firewall

↓

Internal Network
```

Traditional firewalls primarily inspect North-South traffic.

---

# Micro-Segmentation

Micro-segmentation applies security policies at the workload level.

Example:

```text
Web Server

↓

Application Server

↓

Database
```

Each communication path is independently controlled.

Benefits:

- Reduced Lateral Movement
- Fine-Grained Security
- Zero Trust Support

---

# Enterprise Example

```text
Internet

↓

Firewall

↓

DMZ

↓

Web Tier

↓

Application Tier

↓

Database Tier

↓

Management Network
```

Each layer is isolated with dedicated security controls.

---

# Healthcare Example

Separate networks for:

- Medical Devices
- Patient Records
- Administration
- Guest Wi-Fi

This limits access and helps meet compliance requirements.

---

# Financial Institution Example

Separate segments for:

- Customer Banking Systems
- Payment Processing
- Internal Applications
- Administrative Systems
- Security Operations Centre (SOC)

Strict firewall policies control communication between each segment.

---

# Cloud Perspective

Cloud segmentation uses:

- Virtual Private Clouds (VPCs)
- Virtual Networks (VNets)
- Subnets
- Security Groups
- Network ACLs
- Cloud Firewalls

Each application environment can be isolated.

---

# Kubernetes Perspective

Segmentation in Kubernetes uses:

- Namespaces
- Network Policies
- Service Mesh
- Role-Based Access Control (RBAC)
- Pod Security Standards

Pods communicate only when explicitly permitted.

---

# Linux Perspective

Useful commands:

Display IP addresses.

```bash
ip addr
```

Display routing table.

```bash
ip route
```

Display firewall rules.

```bash
sudo iptables -L
```

Display nftables rules.

```bash
sudo nft list ruleset
```

Display listening ports.

```bash
ss -tuln
```

---

# Segmentation Workflow

```text
User

↓

Firewall

↓

Web Tier

↓

Firewall

↓

Application Tier

↓

Firewall

↓

Database
```

Each security boundary enforces access policies.

---

# Physical vs Logical Segmentation

| Physical Segmentation | Logical Segmentation |
|-----------------------|----------------------|
| Separate Hardware | Shared Hardware |
| Higher Cost | Lower Cost |
| Strong Isolation | Flexible Deployment |
| More Complex Expansion | Easier to Scale |

---

# Advantages of Network Segmentation

- Improved Security
- Reduced Lateral Movement
- Better Performance
- Easier Compliance
- Better Traffic Visibility
- Simplified Troubleshooting
- Supports Zero Trust

---

# Limitations

- Requires careful planning
- Additional routing and firewall policies
- Misconfiguration can interrupt communication
- Ongoing maintenance is required

---

# Hands-on Lab

## Task 1

Display IP configuration.

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

Display firewall rules.

```bash
sudo iptables -L
```

---

## Task 4

Draw an enterprise segmented network including:

- Internet
- DMZ
- Web Tier
- Application Tier
- Database Tier
- Management Network

---

## Task 5

Compare:

- Physical Segmentation
- Logical Segmentation

---

## Task 6

Design VLANs for:

- Finance
- HR
- Engineering
- Guest Network

---

## Task 7

Design Kubernetes segmentation using:

- Namespaces
- Network Policies
- RBAC

---

## Task 8

Research segmentation strategies for:

- Enterprise Data Centres
- Cloud Environments
- Kubernetes Clusters

Compare how each environment implements workload isolation.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip addr` | Display IP configuration |
| `ip route` | Display routing table |
| `iptables -L` | Display firewall rules |
| `nft list ruleset` | Display nftables rules |
| `ss -tuln` | Display listening ports |
| `ping` | Test connectivity |
| `traceroute` | Trace network path |

---

# Common Mistakes

❌ Creating one large flat network.

✅ Divide networks into security zones.

---

❌ Allowing unrestricted communication between segments.

✅ Use firewalls and ACLs to control traffic.

---

❌ Ignoring East-West traffic.

✅ Inspect internal communication as well as Internet traffic.

---

❌ Overcomplicating segmentation.

✅ Balance security with operational simplicity.

---

❌ Not documenting network segments.

✅ Maintain accurate diagrams and policies.

---

# Best Practices

- Segment networks based on business functions.
- Apply the principle of least privilege.
- Protect inter-segment traffic with firewalls.
- Inspect East-West traffic.
- Use VLANs and subnets effectively.
- Implement micro-segmentation for critical workloads.
- Monitor traffic between network segments.
- Regularly review segmentation policies.
- Align segmentation with Zero Trust principles.

---

# Interview Questions

## Beginner

1. What is Network Segmentation?
2. Why is network segmentation important?
3. What is the difference between a flat network and a segmented network?
4. What is a VLAN?

---

## Intermediate

1. Compare Physical and Logical Segmentation.
2. What is East-West traffic?
3. What is Micro-Segmentation?
4. How does segmentation improve security?

---

## Architect Level

1. Design a segmented enterprise network for a financial institution.
2. Explain segmentation in Kubernetes and cloud environments.
3. How would you implement Zero Trust using network segmentation?

---

# Summary

In this lesson, you learned:

- Network Segmentation
- Physical Segmentation
- Logical Segmentation
- VLAN Segmentation
- Subnet Segmentation
- Security Zones
- East-West Traffic
- Micro-Segmentation
- Enterprise Network Design

Network segmentation is one of the most effective ways to improve security and reduce the impact of cyber attacks. By dividing networks into isolated segments and controlling communication between them, organisations limit lateral movement, improve performance, simplify compliance, and strengthen Zero Trust architectures across enterprise, cloud, and Kubernetes environments.

---

## Key Takeaways

- Network segmentation divides networks into **secure, isolated segments**.
- **Physical segmentation** uses dedicated hardware, while **logical segmentation** uses VLANs, subnets, and routing.
- **Micro-segmentation** protects individual workloads.
- **East-West traffic** should be monitored and controlled.
- Segmentation reduces the attack surface and limits lateral movement.
- Network segmentation is a foundational component of **Zero Trust security**.

---

## What's Next?

**[DDoS Protection](ddos-protection.md)**

In the next lesson, you'll learn about **DDoS Protection**.

You'll explore:

- What Distributed Denial of Service (DDoS) attacks are
- Types of DDoS Attacks
- Volumetric, Protocol, and Application-Layer Attacks
- DDoS Detection
- DDoS Mitigation Techniques
- Cloud DDoS Protection Services
- Enterprise Incident Response

By the end of the lesson, you'll understand how organisations detect, mitigate, and defend against DDoS attacks to maintain the availability and resilience of critical services.
