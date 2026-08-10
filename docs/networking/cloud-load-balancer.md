---
title: "Load Balancer"
description: "Learn cloud load balancers — Layer 4 vs Layer 7, health checks, SSL termination, Auto Scaling, and AWS, Azure, and Google Cloud load balancing services."
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
  - cloud
  - load-balancer
  - high-availability
  - rebash-networking-mastery
comments: false
status: ready
---

# Load Balancer — Distributing Traffic for High Availability and Scalability

> A **Load Balancer** is a networking service that distributes incoming client requests across multiple servers, virtual machines, containers, or Kubernetes Pods. By spreading traffic intelligently, load balancers improve **availability, scalability, fault tolerance, performance, and reliability**. Modern cloud platforms such as **AWS, Microsoft Azure, and Google Cloud** provide fully managed load balancing services that automatically handle traffic distribution, health monitoring, SSL termination, and failover. Every Cloud Architect, DevOps Engineer, Platform Engineer, Site Reliability Engineer (SRE), Network Engineer, and Security Engineer should understand load balancing concepts.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 10: Cloud Networking → Lesson 8</p>

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

<div markdown>**Lesson:** 8 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Load Balancers
- Compare Layer 4 and Layer 7 Load Balancing
- Learn traffic distribution algorithms
- Configure health checks
- Understand high availability
- Compare cloud load balancing services
- Design production-ready load-balanced architectures

---

# Prerequisites

Complete:

- Routing
- [NAT Gateway](nat-gateway.md)
- [Internet Gateway](internet-gateway.md)
- DNS Fundamentals
- Cloud Networking Basics

---

# Why Do We Need a Load Balancer?

Imagine your application runs on one server.

```text
Users

↓

Server 1
```

As traffic grows:

- Slow Performance
- Server Overload
- Downtime
- Single Point of Failure

Instead:

```text
Users

↓

Load Balancer

↓

Server 1

↓

Server 2

↓

Server 3
```

Traffic is distributed automatically.

---

# What is a Load Balancer?

A Load Balancer is:

```text
A

Traffic

Distribution

Service
```

It receives client requests and forwards them to healthy backend servers.

Benefits:

- High Availability
- Scalability
- Fault Tolerance
- Improved Performance

---

# Basic Architecture

```text
Users

↓

Internet

↓

Load Balancer

↓

Application Servers

↓

Database
```

The client communicates only with the Load Balancer.

---

# Load Balancing Workflow

```text
Client Request

↓

Load Balancer

↓

Healthy Server

↓

Response

↓

Client
```

The backend server is selected according to a routing algorithm.

---

# Layer 4 Load Balancer

Operates at:

```text
OSI Layer 4

Transport Layer
```

Uses:

- Transmission Control Protocol (TCP)
- User Datagram Protocol (UDP)

Decisions are based on:

- Source IP
- Destination IP
- Port Numbers

Examples:

- AWS Network Load Balancer
- Azure Load Balancer
- Google Cloud TCP/UDP Load Balancer

---

# Layer 7 Load Balancer

Operates at:

```text
OSI Layer 7

Application Layer
```

Routes traffic based on:

- URL Path
- Host Header
- HTTP Headers
- Cookies
- HTTP Methods

Examples:

- AWS Application Load Balancer
- Azure Application Gateway
- Google Cloud HTTP(S) Load Balancer

---

# Layer 4 vs Layer 7

| Layer 4 | Layer 7 |
|----------|----------|
| TCP/UDP | HTTP/HTTPS |
| Faster | Smarter Routing |
| IP & Port Based | Content Based |
| Lower Latency | Advanced Features |

---

# Traffic Distribution Algorithms

Common algorithms include:

## Round Robin

```text
Request 1 → Server 1

Request 2 → Server 2

Request 3 → Server 3
```

Even distribution.

---

## Least Connections

Traffic goes to the server with the fewest active connections.

Useful for:

- Long-lived Sessions
- APIs
- Databases

---

## Least Response Time

Chooses the backend responding the fastest.

Useful for:

- Performance Optimization
- Dynamic Workloads

---

## IP Hash

Client IP determines the backend.

Useful for:

- Session Persistence
- Stateful Applications

---

# Health Checks

Load Balancers continuously monitor backend health.

Example:

```text
GET /health
```

Healthy:

```text
200 OK
```

Unhealthy:

```text
500 Error
```

Unhealthy servers are automatically removed from traffic rotation.

---

# SSL/TLS Termination

Instead of every server handling Transport Layer Security (TLS):

```text
Client

↓

HTTPS

↓

Load Balancer

↓

HTTP

↓

Backend
```

Benefits:

- Reduced CPU Usage
- Centralised Certificate Management
- Simpler Backend Configuration

---

# Session Persistence (Sticky Sessions)

Some applications require clients to reach the same backend.

Example:

```text
User A

↓

Server 2
```

Subsequent requests continue going to Server 2 until the session expires.

---

# High Availability

Without Load Balancer:

```text
Server Failure

↓

Application Down
```

With Load Balancer:

```text
Server Failure

↓

Traffic Redirected

↓

Healthy Servers
```

No manual intervention is required.

---

# Auto Scaling Integration

Modern cloud load balancers integrate with Auto Scaling.

```text
Traffic Increase

↓

Auto Scaling

↓

More Servers

↓

Load Balancer

↓

Traffic Distributed
```

---

# AWS Load Balancers

AWS Elastic Load Balancing (ELB) includes:

- Application Load Balancer (ALB)
- Network Load Balancer (NLB)
- Gateway Load Balancer (GWLB)
- Classic Load Balancer (Legacy)

---

## Application Load Balancer (ALB)

Supports:

- HTTP
- HTTPS
- Path-Based Routing
- Host-Based Routing
- Web Applications
- Microservices
- Kubernetes Ingress

---

## Network Load Balancer (NLB)

Supports:

- TCP
- UDP
- TLS
- High Performance
- Static IP Addresses

---

## Gateway Load Balancer (GWLB)

Designed for:

- Network Appliances
- Firewalls
- Intrusion Detection System / Intrusion Prevention System (IDS/IPS)
- Security Inspection

---

# Azure Load Balancers

Azure provides:

- Azure Load Balancer (Layer 4)
- Azure Application Gateway (Layer 7)
- Azure Front Door (Global Layer 7)

---

# Google Cloud Load Balancers

Google Cloud provides:

- Global HTTP(S) Load Balancer
- Regional HTTP(S) Load Balancer
- TCP Load Balancer
- SSL Proxy Load Balancer
- Internal Load Balancer

One major advantage:

```text
Global

Anycast

IP
```

Clients connect to the nearest Google edge location.

---

# Kubernetes Perspective

Kubernetes uses Load Balancers for:

- Service Type: LoadBalancer
- Ingress Controllers
- External APIs
- Multi-Service Routing

Example:

```text
Internet

↓

Cloud Load Balancer

↓

Ingress Controller

↓

Services

↓

Pods
```

---

# Enterprise Architecture

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

Traffic is distributed across multiple application servers.

---

# Cloud Perspective

Load Balancers provide:

- High Availability
- Automatic Failover
- SSL Offloading
- Health Monitoring
- Horizontal Scaling
- Global Traffic Distribution

---

# AWS CLI Example

List Load Balancers.

```bash
aws elbv2 describe-load-balancers
```

---

# Azure CLI Example

List Load Balancers.

```bash
az network lb list
```

---

# Google Cloud CLI Example

List forwarding rules.

```bash
gcloud compute forwarding-rules list
```

---

# Common Load Balancer Types

| Type | Use Case |
|------|----------|
| Layer 4 | TCP/UDP Applications |
| Layer 7 | HTTP/HTTPS Applications |
| Internal | Private Services |
| External | Internet Applications |
| Global | Multi-Region Applications |

---

# Hands-on Lab

## Task 1

List AWS Load Balancers.

```bash
aws elbv2 describe-load-balancers
```

---

## Task 2

List Azure Load Balancers.

```bash
az network lb list
```

---

## Task 3

List Google Cloud forwarding rules.

```bash
gcloud compute forwarding-rules list
```

---

## Task 4

Design:

- Public Load Balancer
- Three Application Servers

using Round Robin distribution.

---

## Task 5

Configure health checks for:

```text
/health
```

---

## Task 6

Compare:

- Layer 4
- Layer 7

routing decisions.

---

## Task 7

Design a Kubernetes architecture using:

- Cloud Load Balancer
- Ingress Controller
- Multiple Services
- Pods

---

## Task 8

Draw a production architecture including:

- Internet
- Load Balancer
- Auto Scaling Group
- Application Servers
- Database
- Monitoring

Explain how traffic flows when one application server becomes unavailable.

---

# Production Troubleshooting

Problem:

```text
Users

Receive

503 Service Unavailable
```

Check:

- Backend Health
- Health Check Endpoint
- Target Registration
- Security Rules
- Domain Name System (DNS)
- Application Logs

Workflow:

```text
Client

↓

Load Balancer

↓

Health Check

↓

Backend

↓

Application
```

---

# Cloud Comparison

| AWS | Azure | Google Cloud |
|------|--------|--------------|
| ALB | Application Gateway | HTTP(S) Load Balancer |
| NLB | Azure Load Balancer | TCP Load Balancer |
| GWLB | Azure Firewall Integration | Internal Load Balancer |
| ELB | Azure Front Door | Global Anycast Load Balancer |

---

# Common Mistakes

❌ Using one backend server.

✅ Deploy multiple backend instances.

---

❌ Poor health check configuration.

✅ Use lightweight, reliable health endpoints.

---

❌ Exposing backend servers directly.

✅ Route traffic through the Load Balancer.

---

❌ Ignoring SSL certificate management.

✅ Centralise certificates on the Load Balancer when appropriate.

---

❌ Using sticky sessions unnecessarily.

✅ Design stateless applications whenever possible.

---

# Best Practices

- Deploy multiple backend servers.
- Enable health checks.
- Use HTTPS for all public services.
- Terminate SSL/TLS at the Load Balancer when appropriate.
- Prefer stateless applications.
- Integrate with Auto Scaling.
- Monitor latency, error rates, and backend health.
- Deploy across multiple Availability Zones or regions.

---

# Interview Questions

## Beginner

1. What is a Load Balancer?
2. Why is a Load Balancer needed?
3. What is a health check?
4. What is Round Robin?

---

## Intermediate

1. Compare Layer 4 and Layer 7 Load Balancers.
2. Explain SSL termination.
3. What are sticky sessions?
4. How does Auto Scaling work with Load Balancers?

---

## Architect Level

1. Design a highly available web application using cloud load balancers.
2. Explain global load balancing for a multi-region application.
3. How would you troubleshoot intermittent 503 errors from a production Load Balancer?

---

# Summary

In this lesson, you learned:

- Load Balancers
- Layer 4 and Layer 7 Load Balancing
- Traffic Distribution Algorithms
- Health Checks
- SSL/TLS Termination
- Session Persistence
- High Availability
- Auto Scaling Integration
- AWS ELB
- Azure Load Balancer
- Google Cloud Load Balancer

Load Balancers are essential components of modern cloud architectures. They distribute client requests across multiple backend resources, improve availability, enable horizontal scaling, and provide intelligent traffic management. Combined with Auto Scaling, health checks, and cloud-native services, load balancers ensure applications remain highly available and responsive under varying workloads.

---

## Key Takeaways

- A **Load Balancer** distributes traffic across multiple backend resources.
- **Layer 4** load balancers route based on TCP/UDP information, while **Layer 7** load balancers route based on application-layer information such as URLs and HTTP headers.
- Health checks automatically remove unhealthy servers from service.
- SSL/TLS termination simplifies certificate management and reduces backend overhead.
- Load Balancers work closely with **Auto Scaling** to handle changing traffic.
- Managed cloud load balancers improve **availability, scalability, and resilience**.

---

## What's Next?

**[Private Connectivity](private-connectivity.md)**

In the next lesson, you'll learn about **Private Connectivity**.

You'll explore:

- What Private Connectivity is
- Site-to-Site VPN
- Dedicated Private Links
- AWS Direct Connect
- Azure ExpressRoute
- Google Cloud Interconnect
- Hybrid Cloud Networking

By the end of the lesson, you'll understand how organisations securely connect on-premises data centres with cloud environments without sending sensitive traffic across the public Internet.
