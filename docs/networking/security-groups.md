---
title: "Security Groups"
description: "Learn Security Groups — stateful instance-level cloud firewalls, inbound/outbound rules, comparison with Network ACLs, and multi-tier design."
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
  - security-groups
  - cloud
  - firewall
  - rebash-networking-mastery
comments: false
status: ready
---

# Security Groups — Instance-Level Virtual Firewalls in Cloud Computing

> A **Security Group** is a **stateful virtual firewall** that controls inbound and outbound network traffic for cloud resources such as virtual machines, containers, databases, and load balancers. Unlike traditional network firewalls that protect entire networks, Security Groups are attached directly to cloud resources and enforce security policies at the **instance or workload level**. Security Groups are widely used in Amazon Web Services (AWS), Microsoft Azure, Google Cloud, and other cloud platforms to implement least-privilege access and Zero Trust networking. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand Security Groups.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 7: NAT & Firewalls → Lesson 10</p>

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

<div markdown>**Lesson:** 10 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Security Groups
- Learn inbound and outbound rules
- Understand stateful filtering
- Compare Security Groups with Network Access Control Lists (ACLs)
- Design Security Groups for cloud workloads
- Apply Security Groups in enterprise cloud environments
- Troubleshoot Security Group issues

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
- [Linux Firewall](linux-firewall.md)
- [Cloud Firewalls](cloud-firewalls.md)

---

# Why Learn Security Groups?

Imagine deploying:

- Web Server
- Application Server
- Database

Should every server communicate with every other server?

```text
No
```

Instead:

```text
Security Groups

↓

Allow

Only Required

Traffic
```

---

# What is a Security Group?

A **Security Group** is a **stateful virtual firewall** attached to a cloud resource.

It controls:

- Inbound Traffic
- Outbound Traffic

based on configured rules.

Unlike traditional firewalls:

```text
Applied

Per Resource
```

rather than per network.

---

# Security Group Architecture

```text
Internet

↓

Security Group

↓

Virtual Machine

↓

Application
```

Every packet is evaluated before reaching the workload.

---

# Why Use Security Groups?

Security Groups provide:

- Instance-Level Protection
- Stateful Filtering
- Least Privilege Access
- Easy Management
- Cloud Integration
- Scalability

---

# Inbound Rules

Inbound rules determine:

```text
Who

Can Connect

To

The Resource
```

Example:

```text
Allow

HTTPS

TCP 443

From Internet
```

---

# Outbound Rules

Outbound rules determine:

```text
Where

The Resource

Can Connect
```

Example:

```text
Allow

HTTPS

To Internet
```

---

# Stateful Behavior

Security Groups are:

```text
Stateful
```

If inbound traffic is allowed:

```text
Request

↓

Allowed
```

Return traffic:

```text
Automatically

Allowed
```

No additional outbound rule is required for the response.

---

# Rule Components

Each rule typically contains:

- Protocol
- Port
- Source or Destination
- Action (Allow)

Most Security Group implementations allow only **allow** rules; traffic not explicitly allowed is implicitly denied.

---

# Example

Web Server

Inbound:

```text
TCP 443

↓

Internet
```

SSH:

```text
TCP 22

↓

Admin Network
```

Everything else:

```text
Implicitly

Denied
```

---

# Multi-Tier Application

Architecture:

```text
Internet

↓

Web Server

↓

Application Server

↓

Database
```

Security Groups:

Web Server:

- HTTPS from Internet

Application Server:

- HTTPS only from Web Server

Database:

- Database Port only from Application Server

No direct Internet access to the database.

---

# Security Groups vs Network ACLs

| Security Groups | Network ACLs |
|-----------------|--------------|
| Stateful | Usually Stateless |
| Applied to Resource | Applied to Subnet |
| Allow Rules | Allow and Deny Rules |
| Instance-Level Protection | Network-Level Protection |

---

# AWS Perspective

Security Groups protect:

- EC2 Instances
- Load Balancers
- RDS Databases
- ECS Tasks
- EKS Worker Nodes

Security Groups can reference other Security Groups, simplifying application-tier communication.

---

# Azure Perspective

Azure uses:

```text
Network Security Groups

(NSGs)
```

NSGs are associated with:

- Network Interfaces
- Subnets

They support both allow and deny rules and are stateful.

---

# Google Cloud Perspective

Google Cloud uses:

```text
VPC Firewall Rules
```

Rules can target:

- VM Instances
- Network Tags
- Service Accounts

These provide workload-level traffic control similar in purpose to Security Groups.

---

# Enterprise Example

Application:

```text
Internet

↓

Load Balancer

↓

Web Tier

↓

Application Tier

↓

Database
```

Each tier has its own Security Group.

Only necessary communication is permitted.

---

# Hybrid Cloud Example

```text
On-Premises

↓

Virtual Private Network (VPN)

↓

Cloud

↓

Security Groups

↓

Application
```

Cloud resources remain protected even when connected to enterprise networks.

---

# Kubernetes Perspective

In managed Kubernetes services:

- Worker Nodes
- Control Plane Endpoints
- Load Balancers

are often protected using Security Groups or equivalent cloud firewall rules.

Within the cluster, Kubernetes Network Policies provide additional workload isolation.

---

# Linux Perspective

Security Groups filter traffic before it reaches the Linux operating system.

Linux host firewalls provide another security layer.

Useful commands:

Display listening ports.

```bash
ss -tuln
```

Display firewall rules.

```bash
sudo iptables -L -n -v
```

Display nftables configuration.

```bash
sudo nft list ruleset
```

---

# Security Group Packet Flow

```text
Internet

↓

Security Group

↓

Linux Firewall

↓

Application
```

Both cloud and host-level firewalls inspect traffic.

---

# Common Security Group Design

| Resource | Allowed Traffic |
|----------|-----------------|
| Web Server | HTTPS (443) from Internet, SSH (22) from Admin Network |
| Application Server | HTTPS from Web Server only |
| Database Server | Database Port from Application Server only |
| Bastion Host | SSH from Admin Network |

---

# Advantages of Security Groups

- Stateful Filtering
- Instance-Level Protection
- Easy to Manage
- Highly Scalable
- Cloud Native
- Supports Least Privilege
- Integrates with Cloud Services

---

# Limitations

- Provider-specific implementations differ
- Misconfigured rules can expose workloads
- Large environments require careful rule management
- Security Groups should be combined with host-based security controls

---

# Hands-on Lab

## Task 1

Design Security Groups for:

- Web Server
- Application Server
- Database

---

## Task 2

Allow:

- HTTPS from Internet
- SSH only from Admin Network

---

## Task 3

Block direct Internet access to the database.

---

## Task 4

Compare:

- Security Groups
- Network ACLs

---

## Task 5

Draw a three-tier application protected by Security Groups.

---

## Task 6

Design Security Groups for a Kubernetes cluster.

Include:

- Worker Nodes
- Load Balancer
- API Server

---

## Task 7

Research Security Group implementations in:

- AWS
- Azure
- Google Cloud

---

## Task 8

Create a layered security architecture using:

- Security Groups
- Linux Firewall
- Application Authentication

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ss -tuln` | Display listening ports |
| `iptables -L -n -v` | Display host firewall rules |
| `nft list ruleset` | Display nftables rules |
| `ip addr` | Display IP configuration |
| `ip route` | Display routing table |

---

# Common Mistakes

❌ Allowing SSH from anywhere (`0.0.0.0/0`).

✅ Restrict SSH to trusted administrator IP addresses.

---

❌ Exposing databases to the Internet.

✅ Allow database access only from application servers.

---

❌ Using overly broad rules.

✅ Grant only the minimum required access.

---

❌ Ignoring outbound rules.

✅ Review outbound access based on business requirements.

---

❌ Forgetting periodic audits.

✅ Regularly review and remove unused rules.

---

# Best Practices

- Follow the principle of least privilege.
- Create separate Security Groups for each application tier.
- Restrict administrative access.
- Document Security Group rules.
- Review rules regularly.
- Use layered security with cloud firewalls and Linux firewalls.
- Avoid exposing unnecessary ports.
- Automate Security Group management using Infrastructure as Code (IaC).

---

# Interview Questions

## Beginner

1. What is a Security Group?
2. Why are Security Groups stateful?
3. What are inbound and outbound rules?
4. Where are Security Groups applied?

---

## Intermediate

1. Compare Security Groups and Network ACLs.
2. Explain how Security Groups protect cloud workloads.
3. Why should databases have separate Security Groups?
4. How do Security Groups support least-privilege access?

---

## Architect Level

1. Design Security Groups for a three-tier cloud application.
2. Explain layered security using Security Groups and Linux firewalls.
3. How would you troubleshoot connectivity problems caused by Security Group rules?

---

# Summary

In this lesson, you learned:

- Security Groups
- Stateful Filtering
- Inbound Rules
- Outbound Rules
- Cloud Workload Protection
- Security Groups vs Network ACLs
- Enterprise Security Group Design
- Kubernetes Security
- Layered Cloud Security

Security Groups provide instance-level, stateful firewall protection for cloud workloads. By controlling inbound and outbound traffic based on least-privilege principles, they play a critical role in securing virtual machines, databases, containers, and Kubernetes clusters. When combined with cloud firewalls and Linux host firewalls, Security Groups form an essential part of a defence-in-depth security strategy.

---

## Key Takeaways

- Security Groups are **stateful virtual firewalls** attached to cloud resources.
- They control **inbound and outbound** traffic.
- Security Groups are applied at the **resource level**, unlike subnet-level Network ACLs.
- Each application tier should have its own Security Group.
- Security Groups are a key component of **Zero Trust** and **least-privilege** architectures.
- Combine Security Groups with Linux host firewalls and cloud firewalls for comprehensive protection.

---

# Module 7 Complete!

Congratulations! You have successfully completed **Module 7: NAT & Firewalls**.

You now understand:

- NAT
- PAT
- Static NAT
- Dynamic NAT
- Access Control Lists (ACLs)
- Firewall Basics
- Stateful Firewalls
- Linux Firewalls
- Cloud Firewalls
- Security Groups

You now have a solid understanding of modern network address translation, traffic filtering, host security, cloud-native firewalls, and workload protection used in enterprise, cloud, and hybrid environments.

---

## What's Next?

**[Module 7 Summary — NAT & Firewalls](module-7-nat-firewalls-summary.md)**
