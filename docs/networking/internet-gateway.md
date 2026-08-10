---
title: "Internet Gateway"
description: "Learn Internet Gateway — public Internet connectivity, public IPs, route tables, public vs private subnets, and Internet-facing architectures across AWS, Azure, and GCP."
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
  - internet-gateway
  - public-subnet
  - rebash-networking-mastery
comments: false
status: ready
---

# Internet Gateway — Connecting Cloud Networks to the Internet

> An **Internet Gateway (IGW)** is a cloud networking component that enables communication between a **virtual network and the public Internet**. It provides **bidirectional connectivity**, allowing resources in **public subnets** to send traffic to the Internet and receive traffic from external clients. Internet Gateways are a fundamental part of networking in **AWS, Microsoft Azure, and Google Cloud**, enabling web applications, APIs, load balancers, bastion hosts, and other Internet-facing services. Every Cloud Architect, DevOps Engineer, Platform Engineer, Site Reliability Engineer (SRE), Network Engineer, and Security Engineer should understand how Internet Gateways work.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 10: Cloud Networking → Lesson 7</p>

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

<div markdown>**Lesson:** 7 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Internet Gateways
- Learn how public Internet connectivity works
- Configure Internet access for cloud resources
- Understand public IP addressing
- Configure route tables for Internet access
- Compare Internet Gateway implementations across cloud providers
- Design secure Internet-facing cloud architectures

---

# Prerequisites

Complete:

- [Route Tables](route-tables.md)
- [NAT Gateway](nat-gateway.md)
- [AWS VPC](cloud-networking-vpc-and-subnets.md)
- [Azure VNet](azure-vnet.md)
- [Google Cloud VPC](gcp-vpc.md)

---

# Why Do We Need an Internet Gateway?

Imagine deploying a web application.

Users should be able to access:

```text
https://company.com
```

Without an Internet Gateway:

```text
Internet

↓

Cannot Reach

Your Cloud
```

The Internet Gateway provides the connection between your cloud network and the Internet.

---

# What is an Internet Gateway?

An Internet Gateway is:

```text
A

Managed

Gateway

Between

Your Cloud

And

The Internet
```

It enables:

- Outbound Internet Access
- Inbound Internet Traffic
- Public IP Communication

---

# Internet Gateway Architecture

```text
Internet

↓

Internet Gateway

↓

Virtual Network

↓

Public Subnet

↓

Virtual Machine
```

Traffic flows through the Internet Gateway in both directions.

---

# How Internet Gateway Works

A packet from a public VM:

```text
VM

↓

Route Table

↓

Internet Gateway

↓

Internet
```

A response returns through:

```text
Internet

↓

Internet Gateway

↓

VM
```

---

# Public IP Requirement

An Internet Gateway alone is **not enough**.

Resources typically require:

- Public IPv4 Address
- Public IPv6 Address (where applicable)

Without a public IP:

```text
Internet

↓

Cannot Reach

The Resource
```

---

# Route Table Configuration

Public subnet route table:

| Destination | Target |
|-------------|--------|
| Local Network | Local |
| `0.0.0.0/0` | Internet Gateway |

This default route sends Internet-bound traffic to the Internet Gateway.

---

# Public Subnet

A subnet is considered **public** when:

- It has a default route to an Internet Gateway.
- Resources are assigned public IP addresses (when Internet access is required).

Typical resources include:

- Web Servers
- Load Balancers
- Bastion Hosts
- NAT Gateways

---

# Private Subnet

Private subnets:

- Do not route directly to the Internet Gateway.
- Typically use a NAT Gateway for outbound Internet access.
- Protect backend services from direct Internet exposure.

Architecture:

```text
Private VM

↓

NAT Gateway

↓

Internet Gateway

↓

Internet
```

---

# Inbound Traffic

Example:

```text
User

↓

Internet

↓

Internet Gateway

↓

Public Load Balancer

↓

Web Server
```

The Internet Gateway allows inbound traffic only if:

- A valid route exists.
- The resource has a public IP.
- Security rules allow the traffic.

---

# Outbound Traffic

Example:

```text
Public VM

↓

Internet Gateway

↓

Software Repository
```

Used for:

- Software Updates
- Package Downloads
- API Calls
- External Services

---

# AWS Internet Gateway

AWS Internet Gateway:

- Managed Service
- Highly Available
- Horizontally Scalable
- Attached to a VPC

Architecture:

```text
VPC

↓

Internet Gateway

↓

Internet
```

---

# Azure Internet Connectivity

Azure does not require attaching a separate Internet Gateway resource.

Instead:

- System routes provide Internet connectivity.
- Public IP resources enable Internet access.
- Network Security Groups (NSGs) and Azure Firewall control traffic.

Conceptually, Azure provides Internet access through its managed networking infrastructure.

---

# Google Cloud Internet Connectivity

Google Cloud provides Internet connectivity through:

- Default Internet Gateway
- Global Routing
- Firewall Rules

Resources with external IP addresses can communicate with the Internet.

---

# Internet Gateway vs NAT Gateway

| Internet Gateway | NAT Gateway |
|------------------|-------------|
| Public Subnets | Private Subnets |
| Inbound + Outbound | Outbound Only |
| No Address Translation | Performs Source Network Address Translation (SNAT) |
| Public Resources | Private Resources |
| Requires Public IP | Uses NAT Public IP |

---

# Internet Gateway vs VPN Gateway

| Internet Gateway | VPN Gateway |
|------------------|-------------|
| Connects to Internet | Connects to Private Networks |
| Public Connectivity | Hybrid Connectivity |
| Public Applications | Enterprise Networks |
| Web Traffic | Private Corporate Traffic |

---

# Enterprise Architecture

```text
Internet

↓

Internet Gateway

↓

Public Load Balancer

↓

Web Servers

↓

Application Servers

↓

Database
```

Only Internet-facing resources are deployed in public subnets.

---

# Kubernetes Perspective

In managed Kubernetes services:

- Public Load Balancers use Internet connectivity.
- Ingress Controllers expose applications.
- Worker Nodes are often placed in private subnets.
- NAT Gateways provide outbound access for private nodes.

Internet Gateway supports:

- Public Services
- Ingress Traffic
- External APIs

---

# Cloud Perspective

Internet Gateways enable:

- Public Websites
- REST APIs
- Software as a Service (SaaS) Platforms
- Public Load Balancers
- Bastion Hosts
- Developer Access

They are the primary entry point for Internet-facing workloads.

---

# AWS CLI Example

List Internet Gateways.

```bash
aws ec2 describe-internet-gateways
```

---

# Azure CLI Example

List Public IP resources.

```bash
az network public-ip list
```

---

# Google Cloud CLI Example

List external IP addresses.

```bash
gcloud compute addresses list
```

---

# Internet Traffic Flow

```text
User

↓

Internet

↓

Internet Gateway

↓

Load Balancer

↓

Web Server

↓

Application

↓

Database
```

Only the public-facing components communicate directly through the Internet Gateway.

---

# Common Internet Gateway Use Cases

| Use Case | Purpose |
|----------|----------|
| Web Applications | Public Access |
| REST APIs | Client Connectivity |
| Load Balancers | Traffic Distribution |
| Bastion Hosts | Secure Administration |
| Public Kubernetes Services | External Access |
| Static Websites | Internet Hosting |

---

# Hands-on Lab

## Task 1

List AWS Internet Gateways.

```bash
aws ec2 describe-internet-gateways
```

---

## Task 2

List Azure Public IP resources.

```bash
az network public-ip list
```

---

## Task 3

List Google Cloud external IP addresses.

```bash
gcloud compute addresses list
```

---

## Task 4

Create a public subnet route:

```text
0.0.0.0/0

↓

Internet Gateway
```

---

## Task 5

Deploy:

- Public Subnet
- Internet Gateway
- Public VM

Verify Internet connectivity.

---

## Task 6

Deploy a public web server and verify access from a browser.

---

## Task 7

Compare Internet Gateway and NAT Gateway by tracing packet flow for:

- Public VM
- Private VM

---

## Task 8

Draw a production cloud architecture including:

- Internet
- Internet Gateway
- Public Subnets
- Private Subnets
- NAT Gateway
- Load Balancer
- Application Servers
- Database

Explain how inbound and outbound traffic flows through the environment.

---

# Production Troubleshooting

Problem:

```text
Public VM

Cannot

Access

Internet
```

Check:

- Public IP Address
- Route Table
- Internet Gateway
- Security Group / NSG / Firewall Rule
- Network Access Control List (ACL)
- Domain Name System (DNS) Resolution

Workflow:

```text
VM

↓

Public IP

↓

Route Table

↓

Internet Gateway

↓

Internet
```

---

# Cloud Comparison

| AWS | Azure | Google Cloud |
|------|--------|--------------|
| Internet Gateway | Managed Internet Connectivity | Default Internet Gateway |
| Attached to VPC | System Route | Global Internet Routing |
| Public IP Required | Public IP Required | External IP Required |

---

# Common Mistakes

❌ Forgetting the default route.

✅ Add `0.0.0.0/0` pointing to the Internet Gateway.

---

❌ Deploying Internet-facing services in private subnets.

✅ Use public subnets for Internet-facing resources.

---

❌ Missing public IP addresses.

✅ Assign public IPs where required.

---

❌ Blocking traffic with security rules.

✅ Verify firewall, Security Group, or NSG rules.

---

❌ Assuming Internet Gateway provides security.

✅ Combine with firewalls and least-privilege access controls.

---

# Best Practices

- Expose only resources that must be publicly accessible.
- Place databases and backend services in private subnets.
- Use HTTPS for all public applications.
- Protect public workloads with Web Application Firewalls (WAFs).
- Use Load Balancers instead of exposing individual servers.
- Monitor Internet traffic using flow logs and cloud monitoring tools.
- Apply least-privilege firewall rules.

---

# Interview Questions

## Beginner

1. What is an Internet Gateway?
2. Why is a public IP address required?
3. What makes a subnet public?
4. Can a private subnet use an Internet Gateway directly?

---

## Intermediate

1. Compare Internet Gateway and NAT Gateway.
2. Explain inbound and outbound Internet traffic.
3. How does a public EC2 instance reach the Internet?
4. Why are route tables required for Internet access?

---

## Architect Level

1. Design a secure Internet-facing cloud architecture.
2. Explain how you would expose a Kubernetes application to the Internet.
3. How would you minimise the attack surface of public cloud workloads?

---

# Summary

In this lesson, you learned:

- Internet Gateway
- Public Internet Connectivity
- Public IP Addresses
- Route Table Configuration
- Public and Private Subnets
- AWS Internet Gateway
- Azure Internet Connectivity
- Google Cloud Internet Access
- Enterprise Internet Architecture

An Internet Gateway is the primary component that connects cloud networks to the public Internet. It enables inbound and outbound communication for Internet-facing resources while working with route tables, public IP addresses, and security controls. Proper Internet Gateway design is essential for building secure, scalable, and highly available cloud applications.

---

## Key Takeaways

- An **Internet Gateway** connects cloud networks to the public Internet.
- Public subnets require a **default route** to the Internet Gateway.
- Internet-facing resources generally require **public IP addresses**.
- Internet Gateways support **both inbound and outbound** communication.
- Backend services should remain in **private subnets** and use **NAT Gateways** for outbound Internet access.
- Combine Internet Gateways with firewalls, load balancers, and least-privilege security policies.

---

## What's Next?

**[Load Balancer](cloud-load-balancer.md)**

In the next lesson, you'll learn about **Load Balancers**.

You'll explore:

- What a Load Balancer is
- Layer 4 vs Layer 7 Load Balancing
- Health Checks
- Traffic Distribution Algorithms
- High Availability
- AWS Elastic Load Balancer (ELB)
- Azure Load Balancer
- Google Cloud Load Balancer

By the end of the lesson, you'll understand how load balancers distribute traffic, improve application availability, and scale cloud workloads across multiple servers and regions.
