---
title: "NAT Gateway"
description: "Learn NAT Gateway — Source Network Address Translation (SNAT), private subnet outbound Internet access, and managed NAT across AWS, Azure, and Google Cloud."
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
  - nat
  - nat-gateway
  - rebash-networking-mastery
comments: false
status: ready
---

# NAT Gateway — Secure Internet Access for Private Cloud Resources

> A **NAT Gateway (Network Address Translation Gateway)** is a managed cloud networking service that enables **resources in private subnets to access the Internet without allowing inbound Internet connections**. It performs **Source Network Address Translation (SNAT)** by replacing private IP addresses with a public IP address for outbound traffic. NAT Gateways are widely used in **AWS, Microsoft Azure, and Google Cloud** to securely provide software updates, API access, package downloads, and cloud service connectivity for private workloads. Every Cloud Architect, DevOps Engineer, Platform Engineer, Site Reliability Engineer (SRE), Network Engineer, and Security Engineer should understand NAT Gateway architecture.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 10: Cloud Networking → Lesson 6</p>

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

<div markdown>**Lesson:** 6 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand NAT Gateway
- Learn Source Network Address Translation (SNAT)
- Differentiate inbound and outbound Internet access
- Configure private subnet Internet access
- Compare NAT Gateway implementations across AWS, Azure, and GCP
- Design highly available NAT architectures
- Troubleshoot NAT connectivity issues

---

# Prerequisites

Complete:

- NAT Fundamentals
- [Route Tables](route-tables.md)
- [AWS VPC](cloud-networking-vpc-and-subnets.md)
- [Azure VNet](azure-vnet.md)
- [Google Cloud VPC](gcp-vpc.md)

---

# Why Do We Need NAT Gateway?

Imagine a database server running in a private subnet.

It needs to:

- Download operating system updates
- Pull Docker images
- Access cloud APIs
- Install application packages

However:

```text
Database

Should

Never

Be

Accessible

From

The Internet
```

A NAT Gateway solves this problem.

---

# What is a NAT Gateway?

A NAT Gateway is:

```text
A

Managed

Source

Network

Address

Translation

Service
```

It allows:

```text
Private Resources

↓

Internet
```

while preventing:

```text
Internet

↓

Private Resources
```

---

# How NAT Works

Without NAT:

```text
Private IP

10.0.2.10

↓

Internet

❌
```

Private IP addresses are not routable on the public Internet.

With NAT:

```text
10.0.2.10

↓

NAT Gateway

↓

203.0.113.20

↓

Internet
```

The destination sees the public IP of the NAT Gateway.

---

# Source Network Address Translation (SNAT)

When a private VM sends traffic:

Before NAT:

```text
Source:

10.0.2.10
```

After NAT:

```text
Source:

203.0.113.20
```

The destination replies to the public IP, and the NAT Gateway translates the response back to the private IP.

---

# NAT Traffic Flow

```text
Private VM

↓

Private Subnet

↓

Route Table

↓

NAT Gateway

↓

Internet
```

Return traffic follows the reverse path.

---

# NAT Gateway Placement

A NAT Gateway is deployed in a:

```text
Public Subnet
```

because it requires Internet connectivity.

Architecture:

```text
Internet

↓

Internet Gateway

↓

Public Subnet

↓

NAT Gateway

↓

Private Subnet
```

---

# Public vs Private Subnets

| Public Subnet | Private Subnet |
|--------------|----------------|
| Internet Gateway | NAT Gateway |
| Public IP Allowed | Private IP Only |
| Internet Facing | Internal Workloads |
| Accepts Inbound Traffic | Outbound Only |

---

# Route Table Configuration

Private subnet:

| Destination | Target |
|-------------|--------|
| 10.0.0.0/16 | Local |
| 0.0.0.0/0 | NAT Gateway |

Public subnet:

| Destination | Target |
|-------------|--------|
| 10.0.0.0/16 | Local |
| 0.0.0.0/0 | Internet Gateway |

---

# AWS NAT Gateway

AWS provides:

```text
Managed NAT Gateway
```

Features:

- High Availability within an Availability Zone
- Elastic IP
- Automatic Scaling
- Fully Managed

Best practice:

Deploy one NAT Gateway per Availability Zone for resilience.

---

# Azure NAT Gateway

Azure NAT Gateway provides:

- Outbound Internet Connectivity
- Static Public IP
- High Throughput
- Managed Service

Associated with one or more subnets.

---

# Google Cloud NAT

Google Cloud provides:

```text
Cloud NAT
```

Features:

- No Public IP Required on VMs
- Managed NAT Service
- Works with Cloud Router
- Supports Compute Engine and Google Kubernetes Engine (GKE)

---

# Enterprise Architecture

```text
Internet

↓

Internet Gateway

↓

Public Subnet

↓

NAT Gateway

↓

Private Application

↓

Private Database
```

Only outbound Internet access is permitted from the private subnet.

---

# Kubernetes Perspective

Private Kubernetes clusters use NAT for:

- Pulling container images
- Accessing package repositories
- Downloading updates
- Connecting to external APIs

Examples:

- Amazon EKS
- Azure AKS
- Google GKE

---

# Cloud Perspective

NAT Gateways enable:

- Software Updates
- Cloud API Access
- External Service Communication
- Secure Internet Connectivity

without exposing workloads to inbound Internet traffic.

---

# AWS CLI Example

List NAT Gateways.

```bash
aws ec2 describe-nat-gateways
```

---

# Azure CLI Example

List NAT Gateways.

```bash
az network nat gateway list
```

---

# Google Cloud CLI Example

List Cloud NAT configurations.

```bash
gcloud compute routers nats list \
--router=my-router \
--region=asia-south1
```

---

# NAT Gateway Workflow

```text
Private Server

↓

Route Table

↓

NAT Gateway

↓

Internet

↓

Response

↓

NAT Gateway

↓

Private Server
```

The private IP address is never exposed externally.

---

# Common NAT Use Cases

| Use Case | Benefit |
|----------|----------|
| Operating System Updates | Secure outbound access |
| Package Installation | Download software safely |
| Docker Image Pulls | Access container registries |
| Cloud APIs | Connect to managed services |
| Third-Party APIs | Secure outbound communication |
| Kubernetes Nodes | Pull images without public IPs |

---

# Hands-on Lab

## Task 1

List AWS NAT Gateways.

```bash
aws ec2 describe-nat-gateways
```

---

## Task 2

List Azure NAT Gateways.

```bash
az network nat gateway list
```

---

## Task 3

List Google Cloud NAT.

```bash
gcloud compute routers nats list \
--router=my-router \
--region=asia-south1
```

---

## Task 4

Create a private subnet route:

```text
0.0.0.0/0

↓

NAT Gateway
```

---

## Task 5

Deploy:

- Public Subnet
- NAT Gateway
- Private EC2/VM

Verify outbound Internet access.

---

## Task 6

Design a highly available NAT architecture using two Availability Zones.

---

## Task 7

Explain how a private Kubernetes node downloads container images using a NAT Gateway.

---

## Task 8

Draw a production cloud architecture showing:

- Internet Gateway
- Public Subnet
- NAT Gateway
- Private Application Tier
- Private Database Tier
- Route Tables

Explain the outbound packet flow from a private server to the Internet.

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

- Route Table
- NAT Gateway Status
- Internet Gateway
- Security Rules
- Firewall Rules
- Domain Name System (DNS) Resolution

Workflow:

```text
Private VM

↓

Route Table

↓

NAT Gateway

↓

Internet Gateway

↓

Internet
```

---

# NAT Gateway vs Internet Gateway

| NAT Gateway | Internet Gateway |
|-------------|------------------|
| Outbound Only | Inbound & Outbound |
| Private Subnets | Public Subnets |
| Performs SNAT | No Address Translation |
| Protects Internal Resources | Connects Public Resources |
| Requires Route Table | Requires Route Table |

---

# Cloud Comparison

| AWS | Azure | Google Cloud |
|------|--------|--------------|
| NAT Gateway | NAT Gateway | Cloud NAT |
| Elastic IP | Public IP | Cloud NAT IP |
| Managed Service | Managed Service | Managed Service |
| AZ-based Deployment | Regional Service | Regional Service |

---

# Common Mistakes

❌ Deploying NAT Gateway in a private subnet.

✅ Always deploy NAT Gateway in a public subnet.

---

❌ Forgetting the default route to the NAT Gateway.

✅ Configure `0.0.0.0/0` in the private subnet route table.

---

❌ Assuming NAT allows inbound connections.

✅ NAT Gateway supports outbound connections only.

---

❌ Using one NAT Gateway for multiple AZs.

✅ Deploy one NAT Gateway per Availability Zone for resilience.

---

❌ Ignoring monitoring.

✅ Monitor NAT throughput and connection limits.

---

# Best Practices

- Deploy one NAT Gateway per Availability Zone.
- Keep backend servers in private subnets.
- Use managed NAT services instead of self-managed NAT instances where appropriate.
- Monitor NAT Gateway metrics and logs.
- Minimise unnecessary outbound Internet traffic.
- Use Private Endpoints or Service Endpoints where supported to reduce Internet dependency.
- Plan for high availability and fault tolerance.

---

# Interview Questions

## Beginner

1. What is a NAT Gateway?
2. Why do private subnets need NAT?
3. What is Source Network Address Translation (SNAT)?
4. Can inbound Internet traffic reach a private VM through a NAT Gateway?

---

## Intermediate

1. Compare NAT Gateway and Internet Gateway.
2. Explain how a private EC2 instance accesses the Internet.
3. Compare AWS NAT Gateway, Azure NAT Gateway, and Google Cloud NAT.
4. Why should a NAT Gateway be deployed in a public subnet?

---

## Architect Level

1. Design a highly available NAT architecture for a production cloud environment.
2. Explain outbound Internet connectivity for a private Kubernetes cluster.
3. How would you reduce NAT Gateway costs while maintaining security and availability?

---

# Summary

In this lesson, you learned:

- NAT Gateway
- Source Network Address Translation (SNAT)
- Outbound Internet Connectivity
- Route Table Configuration
- AWS NAT Gateway
- Azure NAT Gateway
- Google Cloud NAT
- Production NAT Architectures

A NAT Gateway enables private cloud resources to access the Internet securely without exposing them to inbound Internet traffic. By translating private IP addresses into public addresses for outbound connections, NAT Gateways provide a secure and scalable solution for software updates, cloud API access, and external communications across AWS, Azure, and Google Cloud.

---

## Key Takeaways

- A **NAT Gateway** provides secure outbound Internet access for private resources.
- NAT Gateways perform **Source Network Address Translation (SNAT)**.
- They are deployed in **public subnets** and used by **private subnets**.
- NAT Gateways do **not** allow unsolicited inbound Internet connections.
- AWS, Azure, and Google Cloud all provide fully managed NAT services.
- Deploy **one NAT Gateway per Availability Zone** for production high availability.

---

## What's Next?

**[Internet Gateway](internet-gateway.md)**

In the next lesson, you'll learn about **Internet Gateway**.

You'll explore:

- What an Internet Gateway is
- Public Internet Connectivity
- Inbound and Outbound Traffic
- Public IP Addresses
- Route Table Integration
- Cloud Internet Architecture
- Best Practices for Internet-Facing Workloads

By the end of the lesson, you'll understand how cloud resources securely communicate with the public Internet and how Internet Gateways work together with route tables, public subnets, and NAT Gateways.
