---
title: "Cloud Subnets"
description: "Learn cloud subnets — CIDR planning, public vs private subnets, multi-AZ design, and subnet best practices across AWS, Azure, and Google Cloud."
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
  - subnets
  - cidr
  - rebash-networking-mastery
comments: false
status: ready
---

# Cloud Subnets — Designing Scalable and Secure Network Segments

> A **Subnet (Subnetwork)** is a logical subdivision of a network that divides a larger IP address space into smaller, manageable network segments. In cloud platforms such as **AWS, Microsoft Azure, and Google Cloud**, subnets are used to organise workloads, improve security, optimize routing, and build highly available architectures. Every Virtual Machine, Kubernetes Node, Database, Load Balancer, and Application is deployed inside a subnet. Understanding subnet design is one of the most important networking skills for Cloud Architects, DevOps Engineers, Platform Engineers, Site Reliability Engineers (SRE), Network Engineers, and Security Engineers.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 10: Cloud Networking → Lesson 4</p>

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

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand cloud subnets
- Design subnet architectures
- Calculate subnet sizes
- Differentiate public and private subnets
- Plan IP addressing for cloud environments
- Build highly available network designs
- Apply subnet best practices across AWS, Azure, and Google Cloud

---

# Prerequisites

Complete:

- IPv4 Addressing
- Classless Inter-Domain Routing (CIDR)
- Subnetting
- [AWS VPC](cloud-networking-vpc-and-subnets.md)
- [Azure VNet](azure-vnet.md)
- [Google Cloud VPC](gcp-vpc.md)

---

# Why Are Subnets Needed?

Imagine a VPC with:

```text
10.0.0.0/16
```

containing:

- Web Servers
- Databases
- Kubernetes
- Monitoring
- Bastion Hosts

Without subnets:

```text
Everything

Shares

One Network
```

Problems:

- Difficult Security
- Large Broadcast Domains
- Poor Organization
- Complex Routing

Subnets solve these problems.

---

# What is a Subnet?

A subnet is:

```text
A

Smaller

Network

Inside

A Larger Network
```

Example:

```text
VPC

10.0.0.0/16

↓

10.0.1.0/24

Web
```

```text
10.0.2.0/24

Application
```

```text
10.0.3.0/24

Database
```

---

# Why Divide Networks?

Benefits include:

- Better Security
- Simplified Management
- Traffic Isolation
- Easier Troubleshooting
- Scalable Architecture
- High Availability

---

# CIDR Review

Example:

```text
10.0.0.0/16
```

Contains:

```text
65,536 Addresses
```

Create smaller subnets:

```text
10.0.1.0/24
```

Contains:

```text
256 Addresses
```

---

# Common Subnet Sizes

| CIDR | Total Addresses |
|------|----------------:|
| /24 | 256 |
| /25 | 128 |
| /26 | 64 |
| /27 | 32 |
| /28 | 16 |

> **Note:** Cloud providers reserve some IP addresses in every subnet, so the number of usable addresses is lower than the total.

---

# Public Subnet

A public subnet:

- Has a route to the Internet
- Can host Internet-facing resources
- May contain public IP addresses

Typical resources:

- Web Servers
- Bastion Hosts
- Public Load Balancers
- Network Address Translation (NAT) Gateways

Architecture:

```text
Internet

↓

Internet Gateway

↓

Public Subnet
```

---

# Private Subnet

A private subnet:

- Has no direct Internet route
- Cannot receive unsolicited Internet traffic
- Uses NAT for outbound connectivity when required

Typical resources:

- Databases
- Application Servers
- Kubernetes Worker Nodes
- Internal APIs
- Cache Servers

Architecture:

```text
Private Subnet

↓

NAT

↓

Internet
```

---

# Multi-Tier Architecture

```text
Internet

↓

Web Subnet

↓

Application Subnet

↓

Database Subnet
```

Each tier has:

- Separate Security Policies
- Separate Routes
- Separate Access Controls

---

# Multi-AZ Design

Production deployments span multiple Availability Zones (AZs).

```text
AZ-1

↓

Public

↓

Private
```

```text
AZ-2

↓

Public

↓

Private
```

Benefits:

- High Availability
- Fault Tolerance
- Disaster Recovery

---

# IP Planning

Poor IP planning creates problems later.

Good example:

```text
10.10.0.0/16
```

```text
10.10.1.0/24

Web
```

```text
10.10.2.0/24

App
```

```text
10.10.3.0/24

Database
```

Leave unused ranges for future expansion.

---

# Production Subnet Layout

```text
10.0.1.0/24

Public Web
```

```text
10.0.2.0/24

Application
```

```text
10.0.3.0/24

Database
```

```text
10.0.4.0/24

Management
```

```text
10.0.5.0/24

Monitoring
```

---

# Reserved IP Addresses

Cloud providers reserve IP addresses within every subnet.

Examples include:

- Network Address
- Default Gateway
- Internal Cloud Services
- Broadcast Address (where applicable)

Always consider reserved addresses during subnet planning.

---

# AWS Perspective

AWS subnets:

- Belong to a single Availability Zone
- Can be Public or Private
- Use Route Tables
- Use Security Groups and Network Access Control Lists (NACLs)

Example:

```text
VPC

↓

Subnet

↓

EC2
```

---

# Azure Perspective

Azure subnets:

- Exist inside a VNet
- Use Network Security Groups (NSGs)
- Support User-Defined Routes (UDRs)
- Integrate with Azure Firewall

Example:

```text
VNet

↓

Subnet

↓

Virtual Machine
```

---

# Google Cloud Perspective

Google Cloud:

- Uses Regional Subnets
- Global VPC
- Firewall Rules
- Cloud NAT
- Shared VPC

Example:

```text
Global VPC

↓

Regional Subnet

↓

Compute Engine
```

---

# Kubernetes Perspective

Production Kubernetes clusters often use dedicated subnets.

Example:

```text
Control Plane

↓

Private Subnet
```

```text
Worker Nodes

↓

Private Subnet
```

```text
Load Balancer

↓

Public Subnet
```

This improves isolation and security.

---

# Enterprise Example

```text
Internet

↓

Load Balancer

↓

Web Tier

↓

Application Tier

↓

Database Tier
```

Each tier resides in its own subnet.

---

# Cloud Architecture Example

```text
VPC / VNet

↓

Public Subnets

↓

Application Load Balancer

↓

Private Application Subnets

↓

Private Database Subnets

↓

Backup Subnet
```

This architecture is commonly used across AWS, Azure, and Google Cloud.

---

# Common Subnet Designs

| Subnet | Purpose |
|----------|----------|
| Public | Internet-facing workloads |
| Private | Internal applications |
| Database | Databases |
| Management | Administrative access |
| Monitoring | Monitoring and logging |
| Kubernetes | Worker nodes and Pods |

---

# Hands-on Lab

## Task 1

Create a subnet plan for:

```text
10.0.0.0/16
```

using:

- Public
- Application
- Database
- Management

subnets.

---

## Task 2

Calculate usable addresses for:

```text
10.0.1.0/24
```

---

## Task 3

Design a multi-AZ architecture with:

- Two Public Subnets
- Two Application Subnets
- Two Database Subnets

---

## Task 4

Plan subnet allocation for a Kubernetes cluster.

---

## Task 5

Create a subnet layout supporting:

- 500 Web Servers
- 300 Application Servers
- 100 Databases

Select appropriate CIDR ranges.

---

## Task 6

Compare subnet implementation across:

- AWS
- Azure
- Google Cloud

---

## Task 7

Design a hybrid cloud subnet plan connecting an on-premises data centre with cloud resources.

---

## Task 8

Draw a production cloud architecture showing:

- Public Subnets
- Private Subnets
- Route Tables
- NAT Gateway
- Internet Gateway
- Load Balancer
- Database Tier

Explain how traffic flows between each subnet.

---

# Production Troubleshooting

Problem:

```text
Application

Cannot

Reach

Database
```

Verify:

- Both workloads are in the expected subnets.
- Route tables allow communication.
- Firewall or security rules permit traffic.
- Network ACLs or NSGs are not blocking access.
- Domain Name System (DNS) resolves the correct private address.

Workflow:

```text
Application

↓

Subnet

↓

Route

↓

Security

↓

Database
```

---

# Cloud Comparison

| AWS | Azure | Google Cloud |
|------|--------|--------------|
| AZ-specific Subnets | Regional Subnets | Regional Subnets |
| Route Tables | Route Tables + UDRs | Global Routes |
| Security Groups | NSGs | Firewall Rules |
| NAT Gateway | NAT Gateway | Cloud NAT |

---

# Common Mistakes

❌ Using one subnet for every workload.

✅ Separate workloads by function.

---

❌ Creating very small subnets.

✅ Leave room for future growth.

---

❌ Overlapping CIDR ranges.

✅ Plan address spaces carefully.

---

❌ Placing databases in public subnets.

✅ Always keep databases private.

---

❌ Ignoring cloud-reserved IP addresses.

✅ Account for reserved addresses during planning.

---

# Best Practices

- Design subnet layouts before deployment.
- Separate application tiers into different subnets.
- Use private subnets for backend services.
- Deploy across multiple Availability Zones.
- Leave unused IP space for future expansion.
- Use consistent naming conventions.
- Document subnet allocations.
- Review subnet utilization regularly.

---

# Interview Questions

## Beginner

1. What is a subnet?
2. Why do we divide networks into subnets?
3. What is the difference between a public and private subnet?
4. Why are subnets important in cloud networking?

---

## Intermediate

1. Explain subnet planning for a production application.
2. Compare AWS, Azure, and GCP subnet implementations.
3. How do you determine the correct subnet size?
4. Why should databases be deployed in private subnets?

---

## Architect Level

1. Design a highly available subnet architecture for a multi-region application.
2. Explain how subnet design impacts scalability and security.
3. How would you plan IP addressing for an enterprise cloud migration?

---

# Summary

In this lesson, you learned:

- Cloud Subnets
- CIDR Planning
- Public and Private Subnets
- Multi-Tier Architecture
- Multi-AZ Design
- IP Address Planning
- Cloud Provider Differences
- Enterprise Network Design

Subnets are the foundation of cloud network design. They provide logical separation, improve security, simplify routing, and enable scalable architectures across AWS, Microsoft Azure, and Google Cloud. Well-designed subnet layouts are essential for building resilient, secure, and production-ready cloud environments.

---

## Key Takeaways

- A **subnet** is a logical subdivision of a larger network.
- **Public subnets** host Internet-facing resources.
- **Private subnets** protect backend services and databases.
- Plan **CIDR ranges** carefully to support future growth.
- Deploy workloads across **multiple Availability Zones** for high availability.
- Effective subnet design improves **security, scalability, and operational efficiency**.

---

## What's Next?

**[Route Tables](route-tables.md)**

In the next lesson, you'll learn about **Route Tables**.

You'll explore:

- What Route Tables are
- Static and Dynamic Routes
- Default Routes
- Internet Routing
- Private Routing
- Route Priorities
- Cloud Routing Best Practices

By the end of the lesson, you'll understand how cloud platforms determine where network traffic is forwarded and how to design efficient routing for production cloud environments.
