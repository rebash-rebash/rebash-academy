---
title: "Route Tables"
description: "Learn cloud route tables — default and local routes, longest prefix match, Internet and NAT routing, and production routing across AWS, Azure, and GCP."
difficulty: intermediate
estimated_time: "170 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 10 · Cloud Networking"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - cloud
  - routing
  - route-tables
  - rebash-networking-mastery
comments: false
status: ready
---

# Route Tables — Directing Network Traffic in Cloud Environments

> A **Route Table** is a collection of routing rules that determines **where network traffic should be forwarded**. Every packet that enters or leaves a subnet is evaluated against a route table to determine its next destination. Route tables are fundamental to cloud networking in **AWS, Microsoft Azure, and Google Cloud**, enabling communication between subnets, the Internet, VPNs, hybrid networks, and cloud services. Every Cloud Architect, DevOps Engineer, Platform Engineer, Site Reliability Engineer (SRE), Network Engineer, and Security Engineer should understand how route tables work.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 10: Cloud Networking → Lesson 5</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 170 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Cloud Networking</div>

<div markdown>**Lesson:** 5 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand route tables
- Learn how routing decisions are made
- Configure default routes
- Route traffic to the Internet
- Connect private subnets using Network Address Translation (NAT)
- Understand cloud routing across AWS, Azure, and GCP
- Design production-ready routing architectures

---

# Prerequisites

Complete:

- Routing Basics
- Static Routing
- [AWS VPC](cloud-networking-vpc-and-subnets.md)
- [Azure VNet](azure-vnet.md)
- [Google Cloud VPC](gcp-vpc.md)
- [Subnets](cloud-subnets.md)

---

# Why Are Route Tables Important?

Imagine a web server wants to reach:

```text
www.example.com
```

The server asks:

```text
Where

Should

I Send

This Packet?
```

The answer comes from:

```text
Route Table
```

Without routing:

```text
Packets

Cannot

Reach

Their Destination
```

---

# What is a Route Table?

A Route Table is:

```text
A

List

Of

Routing Rules
```

Each rule tells the network:

```text
Destination Network

↓

Next Hop
```

---

# How Routing Works

Packet arrives:

```text
Packet

↓

Route Table

↓

Matching Route

↓

Next Hop

↓

Destination
```

Every packet follows this process.

---

# Route Entry Structure

Every route contains:

| Field | Description |
|--------|-------------|
| Destination | Target network |
| Next Hop | Where packets should go |
| Priority | Determines which route is selected (platform dependent) |

Example:

| Destination | Next Hop |
|-------------|----------|
| 10.0.0.0/16 | Local |
| 0.0.0.0/0 | Internet Gateway |

---

# Local Route

Every cloud network automatically creates a local route.

Example:

```text
10.0.0.0/16

↓

Local
```

This enables communication between resources inside the same virtual network.

---

# Default Route

The default route matches:

```text
0.0.0.0/0
```

Meaning:

```text
Any

Unknown

Destination
```

Example:

```text
0.0.0.0/0

↓

Internet Gateway
```

---

# Public Subnet Routing

```text
Public Subnet

↓

Route Table

↓

Internet Gateway

↓

Internet
```

Resources with public IP addresses can communicate with the Internet.

---

# Private Subnet Routing

Private resources usually cannot reach the Internet directly.

Instead:

```text
Private Subnet

↓

Route Table

↓

NAT Gateway

↓

Internet
```

Inbound Internet traffic remains blocked.

---

# Multiple Route Tables

Large environments often use different route tables.

Example:

```text
Public Route Table
```

```text
Private Route Table
```

```text
Database Route Table
```

Each subnet can be associated with the appropriate routing policy.

---

# Longest Prefix Match

When multiple routes match a destination, the most specific route is selected.

Example:

| Destination | Next Hop |
|-------------|----------|
| 10.0.0.0/16 | Local |
| 10.0.1.0/24 | Firewall |
| 0.0.0.0/0 | Internet Gateway |

Traffic to:

```text
10.0.1.25
```

uses:

```text
10.0.1.0/24
```

because it is the most specific match.

---

# AWS Route Tables

AWS Route Tables can forward traffic to:

- Local Network
- Internet Gateway
- NAT Gateway
- VPC Peering
- Transit Gateway
- Virtual Private Gateway
- Network Interfaces

Example:

| Destination | Target |
|-------------|--------|
| 10.0.0.0/16 | Local |
| 0.0.0.0/0 | Internet Gateway |

---

# Azure Route Tables

Azure supports:

- System Routes
- User-Defined Routes (UDRs)

Traffic can be directed to:

- Internet
- Virtual Appliance
- VPN Gateway
- Virtual Network
- Azure Firewall

---

# Google Cloud Routes

Google Cloud automatically creates:

- Local Routes
- Default Internet Route

Custom routes can forward traffic to:

- Cloud VPN
- Cloud Router
- Internal Load Balancers
- Network Appliances

---

# Hybrid Routing

Example:

```text
Cloud

↓

VPN Gateway

↓

On-Premises
```

Route Table:

```text
192.168.0.0/16

↓

VPN Gateway
```

Traffic for the on-premises network follows the VPN tunnel.

---

# Multi-Region Routing

Example:

```text
Region A

↓

Route

↓

VPN

↓

Region B
```

or

```text
Region A

↓

Cloud Backbone

↓

Region B
```

depending on the cloud provider and architecture.

---

# Enterprise Architecture

```text
Internet

↓

Internet Gateway

↓

Public Subnet

↓

Application

↓

Database

↓

VPN Gateway

↓

On-Premises
```

Each network segment uses route tables to determine packet forwarding.

---

# Kubernetes Perspective

In Kubernetes:

- Nodes maintain routing information.
- Container Network Interface (CNI) plugins configure Pod routes.
- Services rely on routing for communication.
- Cloud route tables integrate with cluster networking.

Understanding route tables helps troubleshoot Pod connectivity and hybrid networking.

---

# Cloud Perspective

Route tables determine traffic flow between:

- Subnets
- Virtual Networks
- Internet
- VPNs
- Cloud Services
- Load Balancers
- Hybrid Networks

Proper routing is essential for scalable cloud architectures.

---

# CLI Examples

## AWS

List route tables.

```bash
aws ec2 describe-route-tables
```

---

## Azure

List route tables.

```bash
az network route-table list
```

---

## Google Cloud

List routes.

```bash
gcloud compute routes list
```

---

# Common Route Destinations

| Destination | Next Hop |
|-------------|----------|
| Local Network | Local |
| Internet | Internet Gateway |
| Private Internet Access | NAT Gateway |
| VPN Network | VPN Gateway |
| Another VPC/VNet | Peering |
| Shared Services | Transit Gateway / Hub |

---

# Hands-on Lab

## Task 1

List AWS Route Tables.

```bash
aws ec2 describe-route-tables
```

---

## Task 2

List Azure Route Tables.

```bash
az network route-table list
```

---

## Task 3

List Google Cloud Routes.

```bash
gcloud compute routes list
```

---

## Task 4

Design:

- Public Route Table
- Private Route Table

for a three-tier application.

---

## Task 5

Add a default route to:

```text
Internet Gateway
```

---

## Task 6

Add a private subnet route to:

```text
NAT Gateway
```

---

## Task 7

Design routing for a hybrid environment connecting:

- AWS
- Azure
- Google Cloud
- On-Premises

---

## Task 8

Draw a production routing architecture including:

- Public Subnets
- Private Subnets
- Internet Gateway
- NAT Gateway
- VPN Gateway
- Route Tables

Explain how traffic is routed from:

- Internet User
- Web Server
- Application Server
- Database

---

# Production Troubleshooting

Problem:

```text
EC2

Cannot

Reach

Internet
```

Check:

- Route Table Association
- Default Route
- Internet Gateway
- NAT Gateway
- Security Rules
- Network Access Control Lists (NACLs)
- Firewall Rules

Workflow:

```text
Instance

↓

Subnet

↓

Route Table

↓

Gateway

↓

Destination
```

---

# Cloud Comparison

| AWS | Azure | Google Cloud |
|------|--------|--------------|
| Route Tables | Route Tables + UDRs | Global Routes |
| Internet Gateway | Internet System Route | Default Internet Gateway |
| NAT Gateway | NAT Gateway | Cloud NAT |
| Transit Gateway | Virtual WAN | Network Connectivity Center |

---

# Common Mistakes

❌ Forgetting the default route.

✅ Verify `0.0.0.0/0` configuration.

---

❌ Associating the wrong route table with a subnet.

✅ Validate subnet associations.

---

❌ Overlooking longest prefix matching.

✅ Review route specificity.

---

❌ Missing routes to hybrid networks.

✅ Configure VPN or interconnect routes.

---

❌ Assuming firewall issues when routing is incorrect.

✅ Verify routes before debugging security policies.

---

# Best Practices

- Use separate route tables for different subnet types.
- Keep routing simple and predictable.
- Use least-privilege network design.
- Document every custom route.
- Verify route propagation in hybrid environments.
- Avoid overlapping CIDR ranges.
- Test routing after every infrastructure change.
- Monitor routing using cloud network monitoring tools.

---

# Interview Questions

## Beginner

1. What is a Route Table?
2. What is a default route?
3. What is a local route?
4. Why are route tables required?

---

## Intermediate

1. Explain longest prefix matching.
2. Compare AWS, Azure, and GCP routing.
3. How does a private subnet reach the Internet?
4. What is a User-Defined Route (UDR)?

---

## Architect Level

1. Design routing for a multi-tier cloud application.
2. Explain routing in a hybrid cloud architecture.
3. How would you troubleshoot routing issues across multiple cloud providers?

---

# Summary

In this lesson, you learned:

- Route Tables
- Routing Decisions
- Default Routes
- Local Routes
- Longest Prefix Match
- Internet Routing
- Private Routing
- Hybrid Routing
- Cloud Routing Best Practices

Route tables are the decision-making engine of cloud networking. Every packet relies on routing rules to reach its destination. By combining local routes, default routes, NAT, VPNs, and cloud gateways, organisations can build secure, scalable, and highly available cloud network architectures across AWS, Azure, and Google Cloud.

---

## Key Takeaways

- A **Route Table** determines where network traffic is forwarded.
- Every subnet is associated with a route table.
- The **default route (`0.0.0.0/0`)** handles traffic destined for external networks.
- **Longest prefix matching** selects the most specific route.
- Public subnets route traffic through an **Internet Gateway**, while private subnets typically use a **NAT Gateway**.
- Well-designed routing improves **security, scalability, and reliability**.

---

## What's Next?

**[NAT Gateway](nat-gateway.md)**

In the next lesson, you'll learn about **NAT Gateway**.

You'll explore:

- What a NAT Gateway is
- Source Network Address Translation (SNAT)
- Public vs Private Internet Access
- Outbound Connectivity
- High Availability
- Cloud NAT Services
- Production Best Practices

By the end of the lesson, you'll understand how private cloud resources securely access the Internet without exposing themselves to inbound Internet traffic.
