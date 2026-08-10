---
title: "AWS Virtual Private Cloud (VPC)"
description: "Learn AWS VPC — design secure cloud networks with CIDR, public and private subnets, route tables, Internet and NAT Gateways, Security Groups, and NACLs."
difficulty: intermediate
estimated_time: "180 min"
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
  - aws
  - vpc
  - cloud
  - rebash-networking-mastery
comments: false
status: ready
---

# AWS Virtual Private Cloud (VPC) — Building Secure Networks in AWS

> **Amazon Virtual Private Cloud (AWS VPC)** is a logically isolated virtual network within AWS where you can launch and manage cloud resources securely. A VPC provides complete control over **IP addressing, subnets, routing, Internet connectivity, security, and network isolation**. Every EC2 instance, RDS database, Load Balancer, ECS task, and EKS cluster runs inside a VPC. Understanding AWS VPC is fundamental for Cloud Architects, DevOps Engineers, Platform Engineers, Site Reliability Engineers (SRE), Network Engineers, and Security Engineers.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 10: Cloud Networking → Lesson 1</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 180 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Cloud Networking</div>

<div markdown>**Lesson:** 1 of 10</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand AWS VPC
- Design secure cloud networks
- Create public and private subnets
- Configure route tables
- Understand Internet and NAT Gateways
- Secure workloads using Security Groups and Network Access Control Lists (NACLs)
- Design production-ready AWS network architectures

---

# Prerequisites

Complete:

- Networking Fundamentals
- Routing
- Subnetting
- Network Address Translation (NAT)
- Firewalls
- [Linux Networking](module-9-linux-networking-summary.md)

Basic understanding of:

- IPv4 Addressing
- Classless Inter-Domain Routing (CIDR)
- Routing
- Cloud Computing

---

# Why Learn AWS VPC?

Imagine launching a server in AWS.

Questions immediately arise:

- Which IP address should it receive?
- Should it be accessible from the Internet?
- How will it communicate with databases?
- How will workloads in different Availability Zones communicate?
- How do we secure the network?

AWS solves these challenges using:

```text
Virtual Private Cloud

(VPC)
```

---

# What is AWS VPC?

A VPC is:

```text
Your

Private

Network

Inside

AWS
```

It behaves similarly to an on-premises data centre network, but is fully managed by AWS.

Inside a VPC you can create:

- Subnets
- Route Tables
- Internet Gateways
- NAT Gateways
- Security Groups
- Network ACLs
- Load Balancers
- VPN Connections

---

# AWS Global Infrastructure

Networking exists within AWS Regions.

Example:

```text
AWS Region

↓

VPC

↓

Availability Zones

↓

Subnets

↓

Resources
```

A VPC belongs to **one AWS Region**, but can span **multiple Availability Zones**.

---

# VPC Components

A production VPC typically contains:

- CIDR Block
- Public Subnets
- Private Subnets
- Route Tables
- Internet Gateway
- NAT Gateway
- Security Groups
- Network ACLs

---

# VPC Architecture

```text
AWS Region

↓

VPC (10.0.0.0/16)

↓

AZ-A

↓

Public Subnet

↓

Private Subnet

↓

AZ-B

↓

Public Subnet

↓

Private Subnet
```

This architecture provides high availability.

---

# VPC CIDR Block

Every VPC requires a CIDR block.

Example:

```text
10.0.0.0/16
```

Maximum:

```text
65,536

Addresses
```

Example subnet allocation:

```text
10.0.1.0/24

Public
```

```text
10.0.2.0/24

Private
```

---

# Public Subnet

A subnet becomes **public** when:

- It has a route to an Internet Gateway
- Instances may have Public IP addresses

Typical resources:

- Bastion Hosts
- Load Balancers
- NAT Gateways
- Public Web Servers

---

# Private Subnet

A private subnet:

- Has no direct Internet route
- Uses a NAT Gateway for outbound Internet access
- Hosts internal workloads

Typical resources:

- Databases
- Application Servers
- Kubernetes Worker Nodes
- Internal APIs

---

# Availability Zones

High availability is achieved by deploying resources across multiple Availability Zones (AZs).

Example:

```text
AZ-A

↓

Web

↓

App

↓

Database
```

```text
AZ-B

↓

Web

↓

App

↓

Database
```

If one Availability Zone becomes unavailable, workloads in the other zone continue serving traffic.

---

# Route Tables

A Route Table determines where packets are forwarded.

Example:

```text
Destination

0.0.0.0/0

↓

Internet Gateway
```

Private subnet:

```text
Destination

0.0.0.0/0

↓

NAT Gateway
```

---

# Internet Gateway (IGW)

Internet Gateway provides:

- Internet Access
- Public IP Connectivity
- Inbound Internet Traffic
- Outbound Internet Traffic

Example:

```text
Internet

↓

Internet Gateway

↓

Public Subnet
```

---

# NAT Gateway

Private resources often need outbound Internet access.

Example:

```text
Private EC2

↓

NAT Gateway

↓

Internet
```

Inbound Internet connections remain blocked.

---

# Security Groups

Security Groups are:

```text
Stateful

Virtual Firewalls
```

Applied to:

- EC2
- RDS
- ECS
- EKS
- Elastic Network Interfaces (ENIs)

Example:

Allow:

```text
TCP 443

HTTPS
```

Deny all other inbound traffic by default.

---

# Network ACL (NACL)

NACLs operate at the subnet level.

Characteristics:

- Stateless
- Allow Rules
- Deny Rules
- Applied to Entire Subnets

---

# Security Groups vs NACL

| Security Group | Network ACL |
|---------------|-------------|
| Stateful | Stateless |
| Instance Level | Subnet Level |
| Allow Rules Only | Allow and Deny Rules |
| Easier Management | More Granular Control |

---

# Elastic IP

An Elastic IP is a static public IPv4 address.

Used for:

- Bastion Hosts
- NAT Gateways
- Public Services

It remains allocated until released.

---

# Elastic Network Interface (ENI)

An ENI is a virtual network interface.

It contains:

- Private IP Addresses
- Security Groups
- MAC Address
- Elastic IP Association

Instances can have multiple ENIs.

---

# VPC Peering

Allows communication between two VPCs.

Example:

```text
VPC A

⇄

VPC B
```

Requirements:

- Non-overlapping CIDR ranges
- Route updates
- Security rule configuration

---

# VPC Endpoints

VPC Endpoints provide private connectivity to AWS services.

Examples:

- Amazon S3
- DynamoDB
- Systems Manager (SSM)

Traffic remains on the AWS network instead of traversing the public Internet.

---

# Enterprise Architecture

```text
Internet

↓

Internet Gateway

↓

Public Subnet

↓

Application Load Balancer

↓

Private Application Servers

↓

Private Database

↓

NAT Gateway
```

This architecture separates Internet-facing components from internal services.

---

# Kubernetes Perspective

Amazon EKS uses VPC networking.

Each Pod receives:

- VPC IP Address
- Security Group (optional with advanced networking)
- Route Table Integration

Networking is provided through the AWS VPC Container Network Interface (CNI) plugin.

---

# Cloud Perspective

AWS VPC provides:

- Isolation
- Scalability
- High Availability
- Fine-Grained Security
- Hybrid Connectivity

It is the networking foundation for nearly all AWS services.

---

# AWS CLI Examples

List VPCs.

```bash
aws ec2 describe-vpcs
```

List subnets.

```bash
aws ec2 describe-subnets
```

List route tables.

```bash
aws ec2 describe-route-tables
```

List Internet Gateways.

```bash
aws ec2 describe-internet-gateways
```

List Security Groups.

```bash
aws ec2 describe-security-groups
```

---

# Common AWS Networking Components

| Component | Purpose |
|-----------|----------|
| VPC | Virtual Network |
| Subnet | Network Segment |
| Route Table | Packet Routing |
| Internet Gateway | Public Internet Access |
| NAT Gateway | Private Internet Access |
| Security Group | Stateful Firewall |
| NACL | Stateless Firewall |
| ENI | Network Interface |
| Elastic IP | Static Public IP |

---

# Hands-on Lab

## Task 1

List VPCs.

```bash
aws ec2 describe-vpcs
```

---

## Task 2

List subnets.

```bash
aws ec2 describe-subnets
```

---

## Task 3

List route tables.

```bash
aws ec2 describe-route-tables
```

---

## Task 4

List Internet Gateways.

```bash
aws ec2 describe-internet-gateways
```

---

## Task 5

List Security Groups.

```bash
aws ec2 describe-security-groups
```

---

## Task 6

Design a VPC containing:

- 2 Public Subnets
- 2 Private Subnets
- Internet Gateway
- NAT Gateway
- Application Load Balancer

---

## Task 7

Deploy a web application architecture where:

- Web servers are in public subnets.
- Application servers are in private subnets.
- Databases remain private.
- Only HTTPS traffic is exposed to the Internet.

---

## Task 8

Draw a production-ready AWS VPC architecture including:

- Multi-AZ deployment
- Public and Private Subnets
- Route Tables
- Security Groups
- Internet Gateway
- NAT Gateway
- Application Load Balancer
- Database Tier

Explain how traffic flows from an Internet user to the database.

---

# Production Troubleshooting

Problem:

```text
EC2

Cannot

Access

Internet
```

Check:

- Public or Private Subnet?
- Route Table
- Internet Gateway
- NAT Gateway
- Security Group
- Network ACL
- Public IP Assignment

Common troubleshooting workflow:

```text
Instance

↓

Subnet

↓

Route Table

↓

Gateway

↓

Security

↓

Connectivity
```

---

# Common Mistakes

❌ Deploying databases in public subnets.

✅ Keep databases in private subnets.

---

❌ Using one Availability Zone.

✅ Deploy across multiple AZs.

---

❌ Overlapping VPC CIDR ranges.

✅ Plan IP addressing carefully.

---

❌ Relying only on Security Groups.

✅ Combine Security Groups with NACLs where appropriate.

---

❌ Forgetting route table entries.

✅ Verify routes after network changes.

---

# Best Practices

- Use private subnets for backend services.
- Deploy workloads across multiple Availability Zones.
- Apply the principle of least privilege in Security Groups.
- Keep databases isolated from the Internet.
- Plan CIDR ranges for future expansion.
- Use VPC Endpoints for AWS service access.
- Enable VPC Flow Logs for network monitoring.
- Design highly available NAT and Load Balancer architectures.

---

# Interview Questions

## Beginner

1. What is an AWS VPC?
2. What is the difference between a public and private subnet?
3. What is an Internet Gateway?
4. What is a NAT Gateway?

---

## Intermediate

1. Compare Security Groups and Network ACLs.
2. Explain VPC Peering.
3. What is an Elastic Network Interface (ENI)?
4. How do Route Tables work?

---

## Architect Level

1. Design a highly available multi-tier AWS VPC architecture.
2. How would you connect multiple VPCs securely?
3. Explain how you would design networking for a production EKS cluster.

---

# Summary

In this lesson, you learned:

- AWS Virtual Private Cloud (VPC)
- CIDR Blocks
- Public and Private Subnets
- Availability Zones
- Route Tables
- Internet Gateway
- NAT Gateway
- Security Groups
- Network ACLs
- VPC Peering
- VPC Endpoints
- Enterprise AWS Networking

AWS VPC is the foundation of networking in Amazon Web Services. It provides isolated virtual networks where organisations securely deploy applications, databases, Kubernetes clusters, and cloud services. By combining subnets, routing, gateways, and security controls, VPC enables scalable, highly available, and secure cloud architectures.

---

## Key Takeaways

- A **VPC** is a logically isolated virtual network in AWS.
- Use **public subnets** for Internet-facing resources and **private subnets** for backend workloads.
- **Internet Gateways** enable public connectivity, while **NAT Gateways** provide outbound Internet access for private resources.
- **Security Groups** are stateful firewalls and **Network ACLs** are stateless subnet-level firewalls.
- Multi-AZ deployments improve availability and resilience.
- AWS VPC is the networking foundation for EC2, RDS, EKS, ECS, and many other AWS services.

---

## What's Next?

**[Azure Virtual Network (Azure VNet)](azure-vnet.md)**

In the next lesson, you'll learn about **Azure Virtual Network (Azure VNet)**.

You'll explore:

- What Azure VNet is
- Address Spaces
- Subnets
- Network Security Groups (NSGs)
- User-Defined Routes (UDRs)
- Azure Load Balancer
- VNet Peering

By the end of the lesson, you'll understand how Microsoft Azure implements virtual networking and how it compares with AWS VPC.
