---
title: "Azure Virtual Network (Azure VNet)"
description: "Learn Azure VNet — address spaces, subnets, NSGs, UDRs, NAT Gateway, Azure Firewall, Bastion, VNet Peering, and production Azure networking."
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
  - azure
  - vnet
  - cloud
  - rebash-networking-mastery
comments: false
status: ready
---

# Azure Virtual Network (Azure VNet) — Building Secure Networks in Microsoft Azure

> **Azure Virtual Network (Azure VNet)** is Microsoft's cloud networking service that enables you to build **secure, isolated, and scalable virtual networks** in Azure. A VNet allows Azure resources such as Virtual Machines, AKS clusters, App Services, Load Balancers, and Databases to communicate securely with each other, the Internet, and on-premises networks. Azure VNet is comparable to **AWS VPC**, providing complete control over **IP addressing, subnets, routing, security, DNS, and hybrid connectivity**. Every Cloud Architect, DevOps Engineer, Platform Engineer, Site Reliability Engineer (SRE), Network Engineer, and Security Engineer should understand Azure Virtual Networks.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 10: Cloud Networking → Lesson 2</p>

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

<div markdown>**Lesson:** 2 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Azure Virtual Network (VNet)
- Design Azure virtual networks
- Create address spaces and subnets
- Configure Network Security Groups (NSGs)
- Understand User-Defined Routes (UDRs)
- Implement VNet Peering
- Design production-ready Azure networking

---

# Prerequisites

Complete:

- Networking Fundamentals
- Routing
- Subnetting
- Network Address Translation (NAT)
- Firewalls
- [AWS VPC](cloud-networking-vpc-and-subnets.md)

Basic understanding of:

- Classless Inter-Domain Routing (CIDR)
- IPv4 Addressing
- Cloud Computing

---

# Why Learn Azure VNet?

When deploying resources in Azure, questions immediately arise:

- How should IP addresses be assigned?
- Which workloads should be publicly accessible?
- How do application servers reach databases?
- How can multiple VNets communicate?
- How do we connect Azure with on-premises infrastructure?

Azure answers these questions with:

```text
Azure

Virtual Network

(VNet)
```

---

# What is Azure VNet?

Azure Virtual Network is:

```text
Your

Private

Virtual

Network

Inside Azure
```

It provides secure communication between:

- Virtual Machines
- Azure Kubernetes Service (AKS)
- Azure Load Balancer
- Azure SQL
- Storage Accounts
- App Services
- On-Premises Networks

---

# Azure Networking Architecture

```text
Azure Region

↓

Virtual Network

↓

Subnets

↓

Azure Resources
```

A VNet belongs to a single Azure region.

---

# VNet Components

A production VNet typically contains:

- Address Space
- Subnets
- Route Tables
- Network Security Groups
- Azure Firewall
- Load Balancer
- Public IP Addresses
- NAT Gateway
- Bastion Host
- Domain Name System (DNS) Configuration

---

# Address Space

Each VNet requires an address space.

Example:

```text
10.0.0.0/16
```

Subnets are created within this address space.

Example:

```text
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

# Subnets

A subnet divides the VNet into smaller network segments.

Typical production subnets include:

- Web
- Application
- Database
- Management
- AKS Nodes
- Azure Firewall

Each subnet can have its own routing and security policies.

---

# Public and Private Resources

Azure resources can have:

- Public IP Address
- Private IP Address

Public resources:

- Bastion Hosts
- Public Load Balancers
- VPN Gateway

Private resources:

- Virtual Machines
- Databases
- Internal Applications

---

# Network Security Groups (NSGs)

NSGs are Azure's primary virtual firewall.

They filter:

- Inbound Traffic
- Outbound Traffic

Rules can be applied to:

- Network Interfaces
- Subnets

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

# NSG Processing

```text
Internet

↓

NSG

↓

Virtual Machine
```

Every packet is evaluated against NSG rules before reaching the destination.

---

# Application Security Groups (ASGs)

Application Security Groups simplify security management.

Instead of using IP addresses:

```text
Web Servers

↓

ASG-Web
```

```text
Application Servers

↓

ASG-App
```

NSGs reference ASGs instead of individual IP addresses.

---

# Route Tables

Azure Route Tables determine how traffic is forwarded.

Default routes include:

```text
Virtual Network

↓

Local
```

```text
Internet

↓

Internet
```

Custom routes can direct traffic through:

- Azure Firewall
- Virtual Appliances
- VPN Gateways

---

# User-Defined Routes (UDRs)

Custom routing rules are called:

```text
User-Defined Routes

(UDRs)
```

Example:

```text
0.0.0.0/0

↓

Azure Firewall
```

Instead of sending traffic directly to the Internet.

---

# Azure NAT Gateway

Private Virtual Machines often require outbound Internet access.

Example:

```text
Private VM

↓

NAT Gateway

↓

Internet
```

Inbound Internet traffic remains blocked.

---

# Public IP Addresses

Azure Public IP resources provide:

- Static Public IP
- Dynamic Public IP

Commonly used for:

- Load Balancers
- Bastion
- VPN Gateway
- Virtual Machines

---

# Azure Load Balancer

Azure Load Balancer distributes traffic across multiple instances.

```text
Internet

↓

Load Balancer

↓

VM1

↓

VM2

↓

VM3
```

Benefits:

- High Availability
- Scalability
- Fault Tolerance

---

# Azure Bastion

Azure Bastion enables secure VM access.

Instead of exposing SSH or RDP to the Internet:

```text
Administrator

↓

Azure Bastion

↓

Private VM
```

No public IP is required on the virtual machine.

---

# Azure Firewall

Azure Firewall is a managed Layer 3–Layer 7 firewall.

Provides:

- Network Filtering
- Application Rules
- Threat Intelligence
- Logging

Often used as the central security point for enterprise VNets.

---

# VNet Peering

VNet Peering connects two Azure VNets.

```text
VNet A

⇄

VNet B
```

Benefits:

- Low Latency
- High Bandwidth
- Private Communication

Requirements:

- Non-overlapping Address Spaces
- Peering Configuration

---

# Hybrid Connectivity

Azure supports hybrid networking through:

- VPN Gateway
- ExpressRoute

Architecture:

```text
On-Premises

↓

VPN

↓

Azure VNet
```

or

```text
On-Premises

↓

ExpressRoute

↓

Azure VNet
```

---

# Enterprise Architecture

```text
Internet

↓

Azure Load Balancer

↓

Web Subnet

↓

Application Subnet

↓

Database Subnet

↓

Azure Firewall

↓

VPN Gateway

↓

On-Premises
```

This architecture separates Internet-facing services from internal workloads.

---

# Kubernetes Perspective

Azure Kubernetes Service (AKS) integrates with VNets.

AKS uses:

- VNet Subnets
- Network Security Groups
- Azure Container Network Interface (CNI) or Kubenet
- Load Balancers

Pods and nodes communicate securely inside the VNet.

---

# Cloud Perspective

Azure VNet provides:

- Network Isolation
- Security
- Scalability
- Hybrid Connectivity
- High Availability

It is the networking foundation for nearly every Azure workload.

---

# Azure CLI Examples

List VNets.

```bash
az network vnet list
```

List subnets.

```bash
az network vnet subnet list \
--resource-group MyRG \
--vnet-name MyVNet
```

List NSGs.

```bash
az network nsg list
```

List route tables.

```bash
az network route-table list
```

List public IPs.

```bash
az network public-ip list
```

---

# Common Azure Networking Components

| Component | Purpose |
|-----------|----------|
| VNet | Virtual Network |
| Address Space | IP Range |
| Subnet | Network Segment |
| NSG | Stateful Packet Filtering |
| ASG | Application-Based Security Grouping |
| Route Table | Packet Routing |
| UDR | Custom Routes |
| NAT Gateway | Outbound Internet Access |
| Azure Firewall | Managed Firewall |
| VNet Peering | Connect VNets |

---

# Hands-on Lab

## Task 1

List VNets.

```bash
az network vnet list
```

---

## Task 2

List subnets.

```bash
az network vnet subnet list \
--resource-group MyRG \
--vnet-name MyVNet
```

---

## Task 3

List Network Security Groups.

```bash
az network nsg list
```

---

## Task 4

List route tables.

```bash
az network route-table list
```

---

## Task 5

List public IP addresses.

```bash
az network public-ip list
```

---

## Task 6

Design an Azure VNet containing:

- Web Subnet
- Application Subnet
- Database Subnet
- Azure Firewall
- NAT Gateway
- Azure Load Balancer

---

## Task 7

Design a hybrid architecture connecting:

- On-Premises Data Centre
- Azure VNet
- VPN Gateway
- Azure Firewall

---

## Task 8

Draw a production Azure networking architecture including:

- VNet
- Multiple Subnets
- NSGs
- Azure Firewall
- Azure Bastion
- Load Balancer
- VPN Gateway

Explain how traffic flows from an Internet user to a private database.

---

# Production Troubleshooting

Problem:

```text
Virtual Machine

Cannot

Reach

Internet
```

Check:

- NSG Rules
- Route Table
- NAT Gateway
- Public IP
- Azure Firewall
- DNS Resolution

Workflow:

```text
VM

↓

Subnet

↓

NSG

↓

Route Table

↓

Gateway

↓

Internet
```

---

# AWS VPC vs Azure VNet

| AWS | Azure |
|------|--------|
| VPC | VNet |
| Security Group | NSG |
| NACL | NSG + UDR + Firewall |
| Internet Gateway | Default Internet Route |
| NAT Gateway | NAT Gateway |
| VPC Peering | VNet Peering |

---

# Common Mistakes

❌ Placing sensitive workloads in public subnets.

✅ Keep backend services private.

---

❌ Forgetting NSG rules.

✅ Verify inbound and outbound rules.

---

❌ Overlapping address spaces.

✅ Plan CIDR ranges before deployment.

---

❌ Missing UDR configuration.

✅ Validate custom routing paths.

---

❌ Exposing management ports directly to the Internet.

✅ Use Azure Bastion or VPN access.

---

# Best Practices

- Separate workloads into dedicated subnets.
- Protect subnets with NSGs.
- Use Azure Bastion for secure administration.
- Deploy workloads across Availability Zones when supported.
- Use Azure Firewall for centralised inspection.
- Plan address spaces for future growth.
- Enable Network Watcher and NSG Flow Logs.
- Use VNet Peering instead of public communication where possible.

---

# Interview Questions

## Beginner

1. What is Azure Virtual Network?
2. What is an NSG?
3. What is the purpose of a subnet?
4. What is Azure Bastion?

---

## Intermediate

1. Compare Azure NSGs and AWS Security Groups.
2. What are User-Defined Routes?
3. Explain VNet Peering.
4. How does Azure NAT Gateway work?

---

## Architect Level

1. Design a secure multi-tier Azure network architecture.
2. Explain how you would connect Azure with an on-premises data centre.
3. Design networking for a production AKS cluster.

---

# Summary

In this lesson, you learned:

- Azure Virtual Network (VNet)
- Address Spaces
- Subnets
- Network Security Groups (NSGs)
- Application Security Groups (ASGs)
- Route Tables
- User-Defined Routes (UDRs)
- NAT Gateway
- Azure Firewall
- Azure Bastion
- VNet Peering
- Enterprise Azure Networking

Azure Virtual Network is the core networking service in Microsoft Azure. It enables organisations to build secure, isolated, and highly available cloud networks by combining subnets, routing, firewalls, load balancers, and hybrid connectivity. Azure VNets provide the networking foundation for virtual machines, Kubernetes clusters, databases, and enterprise applications.

---

## Key Takeaways

- **Azure VNet** is the primary networking service in Microsoft Azure.
- **Address Spaces** and **Subnets** organise network resources.
- **Network Security Groups (NSGs)** secure subnets and network interfaces.
- **User-Defined Routes (UDRs)** provide custom traffic routing.
- **VNet Peering** enables private communication between VNets.
- Azure networking supports secure hybrid architectures using **VPN Gateway** and **ExpressRoute**.

---

## What's Next?

**[Google Cloud VPC](gcp-vpc.md)**

In the next lesson, you'll learn about **Google Cloud Virtual Private Cloud (GCP VPC)**.

You'll explore:

- What GCP VPC is
- Global VPC Architecture
- Subnets
- Routes
- Firewall Rules
- Cloud NAT
- Cloud Router
- Shared VPC

By the end of the lesson, you'll understand how Google Cloud's global networking model differs from AWS VPC and Azure VNet, and how to design scalable cloud networks in Google Cloud.
