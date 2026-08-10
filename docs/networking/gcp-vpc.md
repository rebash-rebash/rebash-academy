---
title: "Google Cloud Virtual Private Cloud (GCP VPC)"
description: "Learn Google Cloud VPC — global VPC architecture, regional subnets, firewall rules, Cloud NAT, Cloud Router, Shared VPC, and production GCP networking."
difficulty: intermediate
estimated_time: "190 min"
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
  - gcp
  - vpc
  - cloud
  - rebash-networking-mastery
comments: false
status: ready
---

# Google Cloud Virtual Private Cloud (GCP VPC) — Building Global Cloud Networks

> **Google Cloud Virtual Private Cloud (VPC)** is Google Cloud's fully managed networking service that enables organisations to create **secure, scalable, and globally distributed virtual networks**. Unlike AWS VPC and Azure VNet, a **GCP VPC is global**, allowing resources across multiple regions to communicate within the same virtual network. GCP VPC provides complete control over **IP addressing, subnets, routing, firewall rules, NAT, private connectivity, and hybrid networking**. Every Cloud Architect, DevOps Engineer, Platform Engineer, Site Reliability Engineer (SRE), Network Engineer, and Security Engineer should understand GCP VPC.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 10: Cloud Networking → Lesson 3</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 190 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Cloud Networking</div>

<div markdown>**Lesson:** 3 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Google Cloud VPC
- Learn the global VPC architecture
- Create regional subnets
- Configure firewall rules
- Understand routes and Cloud Router
- Configure Cloud NAT
- Design production-ready Google Cloud networks

---

# Prerequisites

Complete:

- Networking Fundamentals
- Routing
- Firewalls
- [AWS VPC](cloud-networking-vpc-and-subnets.md)
- [Azure Virtual Network](azure-vnet.md)

Basic understanding of:

- Classless Inter-Domain Routing (CIDR)
- IPv4 Addressing
- Cloud Computing

---

# Why Learn GCP VPC?

Imagine deploying an application across:

- India
- Singapore
- Europe
- United States

Questions arise:

- Should every region have its own network?
- How do workloads communicate securely?
- How are routes managed?
- How do private resources access the Internet?

Google Cloud solves these challenges with:

```text
Global

Virtual Private Cloud

(VPC)
```

---

# What is GCP VPC?

A Google Cloud VPC is:

```text
Your

Private

Global

Network

Inside

Google Cloud
```

Unlike AWS and Azure:

- One VPC can span multiple regions.
- Resources communicate using Google's private backbone network.

---

# Global Architecture

```text
Global VPC

↓

Region 1

↓

Subnet
```

```text
Global VPC

↓

Region 2

↓

Subnet
```

```text
Global VPC

↓

Region 3

↓

Subnet
```

One VPC.

Multiple Regions.

Multiple Regional Subnets.

---

# Global vs Regional

| Component | Scope |
|-----------|-------|
| VPC | Global |
| Subnet | Regional |
| Firewall Rule | Global |
| Route | Global |
| Cloud Router | Regional |

This is one of the biggest architectural differences between GCP and other cloud providers.

---

# VPC Components

A production VPC typically contains:

- Global VPC
- Regional Subnets
- Routes
- Firewall Rules
- Cloud Router
- Cloud NAT
- Private Google Access
- Load Balancers
- VPN
- Interconnect

---

# VPC Modes

Google Cloud supports three VPC modes.

## Default Mode

Google automatically creates:

- One VPC
- Multiple Regional Subnets

Useful for learning but not recommended for production.

---

## Auto Mode

Automatically creates one subnet per region.

Example:

```text
us-central1

10.128.0.0/20
```

```text
asia-south1

10.160.0.0/20
```

Easy to use, but less flexible.

---

## Custom Mode

Administrators create:

- Address Spaces
- Regional Subnets
- IP Planning

Recommended for production environments.

---

# Regional Subnets

Each subnet belongs to one region.

Example:

```text
asia-south1

10.10.1.0/24
```

```text
us-central1

10.20.1.0/24
```

Resources in different regions can communicate privately through the same VPC.

---

# Routes

Every VPC contains routes.

Default route:

```text
0.0.0.0/0

↓

Default Internet Gateway
```

Custom routes can direct traffic to:

- Cloud VPN
- Cloud Router
- Network Appliances
- Hybrid Networks

---

# Firewall Rules

Unlike AWS Security Groups, GCP uses **VPC Firewall Rules**.

Firewall rules are:

- Stateful
- Global
- Applied using network tags or service accounts

Example:

Allow:

```text
TCP 443
```

Deny:

```text
All Other Inbound
```

---

# Network Tags

Firewall rules commonly target:

```text
web-server
```

```text
database
```

```text
application
```

Instead of individual VM IP addresses.

---

# Cloud Router

Cloud Router provides:

- Dynamic Routing
- Border Gateway Protocol (BGP)
- VPN Routing
- Interconnect Routing

Example:

```text
On-Premises

↓

Cloud Router

↓

VPC
```

Cloud Router automatically exchanges routes using BGP.

---

# Cloud NAT

Private virtual machines often require Internet access.

Example:

```text
Private VM

↓

Cloud NAT

↓

Internet
```

Benefits:

- No Public IP Required
- Secure Outbound Connectivity

---

# Private Google Access

Private Google Access allows virtual machines **without public IP addresses** to access Google-managed services privately.

Examples:

- Cloud Storage
- Artifact Registry
- BigQuery
- Cloud Logging

Traffic stays on Google's private network.

---

# Cloud Load Balancer

Google Cloud offers global and regional load balancers.

Example:

```text
Users

↓

Global Load Balancer

↓

Region 1
```

```text
↓

Region 2
```

Benefits:

- Global Anycast IP
- High Availability
- Automatic Failover

---

# Shared VPC

Shared VPC enables multiple Google Cloud projects to use the same VPC.

Example:

```text
Host Project

↓

Shared VPC

↓

Project A

↓

Project B

↓

Project C
```

Useful for large enterprises with centralised networking.

---

# VPC Peering

Connects two VPCs privately.

```text
VPC A

⇄

VPC B
```

Requirements:

- Non-overlapping CIDR ranges
- Peering Configuration
- Route Exchange

---

# Hybrid Connectivity

Google Cloud supports:

- Cloud VPN
- Dedicated Interconnect
- Partner Interconnect

Architecture:

```text
On-Premises

↓

Cloud VPN

↓

GCP VPC
```

or

```text
On-Premises

↓

Interconnect

↓

GCP VPC
```

---

# Enterprise Architecture

```text
Internet

↓

Global Load Balancer

↓

Web Subnet

↓

Application Subnet

↓

Database Subnet

↓

Cloud NAT

↓

Cloud Router

↓

On-Premises
```

This architecture supports highly available global deployments.

---

# Kubernetes Perspective

Google Kubernetes Engine (GKE) integrates tightly with VPC.

Each node receives:

- VPC IP Address

Each Pod receives:

- Alias IP Address

Networking features include:

- VPC-native Clusters
- Alias IPs
- Private Clusters
- Cloud NAT
- Internal Load Balancers

---

# Cloud Perspective

Google Cloud VPC provides:

- Global Networking
- Private Backbone
- Automatic Routing
- High Availability
- Enterprise Security
- Hybrid Connectivity

It is the networking foundation for Compute Engine, GKE, Cloud SQL, and many other Google Cloud services.

---

# Google Cloud CLI Examples

List VPCs.

```bash
gcloud compute networks list
```

List subnets.

```bash
gcloud compute networks subnets list
```

List firewall rules.

```bash
gcloud compute firewall-rules list
```

List routes.

```bash
gcloud compute routes list
```

List Cloud Routers.

```bash
gcloud compute routers list
```

---

# Common GCP Networking Components

| Component | Purpose |
|-----------|----------|
| VPC | Global Virtual Network |
| Regional Subnet | Network Segment |
| Route | Packet Routing |
| Firewall Rule | Stateful Firewall |
| Cloud NAT | Outbound Internet Access |
| Cloud Router | Dynamic Routing (BGP) |
| Private Google Access | Private Access to Google Services |
| Shared VPC | Centralised Enterprise Networking |
| VPC Peering | Private VPC Connectivity |

---

# Hands-on Lab

## Task 1

List VPC networks.

```bash
gcloud compute networks list
```

---

## Task 2

List subnets.

```bash
gcloud compute networks subnets list
```

---

## Task 3

List firewall rules.

```bash
gcloud compute firewall-rules list
```

---

## Task 4

List routes.

```bash
gcloud compute routes list
```

---

## Task 5

List Cloud Routers.

```bash
gcloud compute routers list
```

---

## Task 6

Design a GCP VPC containing:

- Global VPC
- Two Regional Subnets
- Cloud NAT
- Cloud Router
- Global Load Balancer

---

## Task 7

Design a production GKE architecture using:

- Private Cluster
- Alias IPs
- Cloud NAT
- Private Google Access

---

## Task 8

Draw a production-ready Google Cloud networking architecture including:

- Global VPC
- Regional Subnets
- Firewall Rules
- Cloud NAT
- Cloud Router
- Shared VPC
- Global Load Balancer
- Hybrid VPN

Explain how traffic flows from an Internet user to a private application running in GKE.

---

# Production Troubleshooting

Problem:

```text
Private VM

Cannot

Access

Internet
```

Check:

- Subnet
- Route
- Firewall Rule
- Cloud NAT
- Domain Name System (DNS)
- Private Google Access (if accessing Google services)

Workflow:

```text
VM

↓

Subnet

↓

Firewall

↓

Route

↓

Cloud NAT

↓

Internet
```

---

# AWS vs Azure vs GCP

| AWS | Azure | Google Cloud |
|------|--------|--------------|
| VPC | VNet | VPC |
| Regional VPC | Regional VNet | Global VPC |
| Security Groups | NSGs | Firewall Rules |
| NAT Gateway | NAT Gateway | Cloud NAT |
| Route Table | Route Table | Routes |
| Transit Gateway | Virtual WAN | Network Connectivity Center / Hybrid Connectivity |

---

# Common Mistakes

❌ Using Auto Mode in production.

✅ Use Custom Mode for better IP planning.

---

❌ Overlapping subnet ranges.

✅ Design CIDR allocations carefully.

---

❌ Forgetting firewall rules.

✅ Verify ingress and egress policies.

---

❌ Deploying private VMs without Cloud NAT.

✅ Configure Cloud NAT for outbound Internet access.

---

❌ Ignoring regional subnet placement.

✅ Create subnets in the regions where workloads run.

---

# Best Practices

- Use **Custom Mode VPCs** in production.
- Plan CIDR blocks for future growth.
- Separate workloads into dedicated regional subnets.
- Use **Cloud NAT** instead of assigning public IPs to backend servers.
- Protect workloads with least-privilege firewall rules.
- Use **Private Google Access** for Google-managed services.
- Use **Shared VPC** for enterprise environments.
- Enable **VPC Flow Logs** for monitoring and troubleshooting.

---

# Interview Questions

## Beginner

1. What is a GCP VPC?
2. What is the difference between a global VPC and a regional subnet?
3. What is Cloud NAT?
4. What is Private Google Access?

---

## Intermediate

1. Compare GCP VPC with AWS VPC.
2. What is Shared VPC?
3. Explain Cloud Router.
4. How do firewall rules work in Google Cloud?

---

## Architect Level

1. Design a global multi-region GCP network architecture.
2. Explain networking for a production GKE cluster.
3. How would you connect an on-premises data centre to Google Cloud using dynamic routing?

---

# Summary

In this lesson, you learned:

- Google Cloud VPC
- Global VPC Architecture
- Regional Subnets
- Routes
- Firewall Rules
- Cloud NAT
- Cloud Router
- Private Google Access
- Shared VPC
- VPC Peering
- Enterprise GCP Networking

Google Cloud VPC provides a **global networking model** that simplifies communication across regions while maintaining secure isolation and centralised management. Combined with Cloud NAT, Cloud Router, firewall rules, and Shared VPC, it enables organisations to build scalable, highly available, and secure cloud infrastructures for Compute Engine, GKE, Cloud SQL, and hybrid environments.

---

## Key Takeaways

- **GCP VPC is global**, unlike AWS VPC and Azure VNet.
- **Subnets are regional**, while firewall rules and routes are managed globally.
- **Cloud NAT** provides outbound Internet access for private workloads.
- **Cloud Router** enables dynamic routing using BGP.
- **Private Google Access** allows private communication with Google-managed services.
- **Shared VPC** is the preferred architecture for large enterprise environments.

---

## What's Next?

**[Subnets](cloud-subnets.md)**

In the next lesson, you'll learn about **Subnets**.

You'll explore:

- What a Subnet is
- CIDR Notation
- Public vs Private Subnets
- IP Address Planning
- Subnet Sizing
- High Availability Design
- Best Practices Across AWS, Azure, and Google Cloud

By the end of the lesson, you'll understand how to design efficient subnet layouts that support scalable, secure, and highly available cloud architectures.
