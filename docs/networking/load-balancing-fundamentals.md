---
title: "Load Balancing"
description: "Learn load balancing — Layer 4 vs Layer 7, algorithms, health checks, sticky sessions, cloud/Kubernetes balancers, and high-availability design."
difficulty: advanced
estimated_time: "230 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 13 · DevOps Networking"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - load-balancing
  - devops
  - high-availability
  - rebash-networking-mastery
comments: false
status: ready
---

# Load Balancing — Distributing Traffic for High Availability and Scalability

> **Load Balancing** is the process of distributing incoming network traffic across multiple servers, containers, or application instances to ensure **high availability, fault tolerance, scalability, and optimal performance**. Instead of sending all requests to a single server, a load balancer intelligently selects a healthy backend, preventing overload and improving user experience. Modern DevOps platforms, cloud-native applications, Kubernetes clusters, and microservices rely heavily on load balancing. Every DevOps Engineer, Platform Engineer, SRE, Cloud Engineer, and Cloud Architect should master load balancing.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 13: DevOps Networking → Lesson 7</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Advanced</div>

<div markdown>**Reading Time:** 230 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** DevOps Networking</div>

<div markdown>**Lesson:** 7 of 10</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand load balancing fundamentals
- Learn Layer 4 and Layer 7 load balancing
- Explore load balancing algorithms
- Configure health checks
- Understand session persistence
- Troubleshoot load balancers
- Design highly available production architectures

---

# Prerequisites

Complete:

- [Reverse Proxy](reverse-proxy-and-ingress-basics.md)
- [Kubernetes Networking](kubernetes-networking-devops.md)
- [Docker Networking](docker-networking.md)
- DNS
- HTTP
- HTTPS

Basic understanding of:

- TCP/IP
- Web Applications
- Cloud Infrastructure

---

# Why Do We Need Load Balancing?

Imagine one application server.

```text
Users

↓

Application Server
```

As traffic increases:

- Slow Response
- Server Overload
- Application Crash
- Downtime

Instead, use multiple servers.

```text
Users

↓

Load Balancer

↓

Server A

↓

Server B

↓

Server C
```

Traffic is distributed automatically.

---

# What is Load Balancing?

Load balancing is:

```text
Distributing

Incoming

Requests

Across

Multiple

Healthy

Servers
```

This improves:

- Availability
- Scalability
- Reliability
- Performance

---

# Load Balancer Architecture

```text
Internet

↓

Load Balancer

↓

Application Servers

↓

Database
```

Clients communicate only with the load balancer.

---

# Request Flow

```text
Client

↓

Load Balancer

↓

Server

↓

Response
```

The load balancer selects the best backend server for each request.

---

# Benefits of Load Balancing

Load balancing provides:

- High Availability
- Horizontal Scaling
- Fault Tolerance
- Better Performance
- Simplified Maintenance
- Zero-Downtime Deployments

---

# Types of Load Balancers

Common categories:

- Layer 4 Load Balancer
- Layer 7 Load Balancer
- Hardware Load Balancer
- Software Load Balancer
- Cloud Load Balancer

---

# Layer 4 Load Balancer

Operates at:

```text
Transport Layer
```

Makes decisions using:

- Source IP
- Destination IP
- TCP Port
- UDP Port

Fast and efficient.

---

# Layer 7 Load Balancer

Operates at:

```text
Application Layer
```

Can inspect:

- URL Path
- HTTP Headers
- Cookies
- Hostname
- HTTP Method

Ideal for modern web applications.

---

# Layer 4 vs Layer 7

| Layer 4 | Layer 7 |
|----------|----------|
| TCP/UDP | HTTP/HTTPS |
| Fast | Intelligent Routing |
| Port-Based | URL-Based |
| Lower Overhead | Rich Features |
| Limited Inspection | Deep Request Analysis |

---

# Load Balancing Algorithms

Common algorithms:

- Round Robin
- Least Connections
- Least Response Time
- Weighted Round Robin
- IP Hash
- Random

Each balances traffic differently.

---

# Round Robin

Requests are distributed sequentially.

```text
Request 1

↓

Server A
```

```text
Request 2

↓

Server B
```

```text
Request 3

↓

Server C
```

Simple and widely used.

---

# Least Connections

Traffic is sent to the server with:

```text
Fewest

Active

Connections
```

Useful when request durations vary.

---

# Weighted Round Robin

Servers receive traffic based on capacity.

Example:

```text
Server A

Weight 3
```

```text
Server B

Weight 1
```

Server A receives more requests.

---

# IP Hash

Client IP determines backend selection.

```text
Client IP

↓

Hash

↓

Server
```

Useful for session persistence.

---

# Health Checks

Load balancers continuously monitor backend health.

Healthy:

```text
Receive Traffic
```

Unhealthy:

```text
Removed

From

Rotation
```

---

# Health Check Types

Examples:

- TCP Health Check
- HTTP Health Check
- HTTPS Health Check
- Custom Endpoint

Typical endpoint:

```text
/health
```

or

```text
/ready
```

---

# Session Persistence

Also called:

```text
Sticky

Sessions
```

Example:

```text
User

↓

Server A
```

Future requests continue reaching Server A.

Methods:

- Cookies
- Source IP
- Session ID

---

# SSL/TLS Termination

Clients connect using HTTPS.

```text
HTTPS

↓

Load Balancer

↓

HTTP

↓

Backend
```

Benefits:

- Reduced Backend CPU Usage
- Centralized Certificate Management

---

# Autoscaling

As traffic increases:

```text
Users

↓

Load Balancer

↓

2 Servers

↓

4 Servers

↓

8 Servers
```

Load balancing works together with autoscaling.

---

# Load Balancing in Docker

Example:

```text
NGINX

↓

Container A

↓

Container B

↓

Container C
```

Traffic is distributed across multiple containers.

---

# Load Balancing in Kubernetes

Architecture:

```text
Internet

↓

Cloud Load Balancer

↓

Ingress

↓

Service

↓

Pods
```

Kubernetes Services balance traffic across Pods automatically.

---

# Cloud Load Balancers

Examples:

- AWS Application Load Balancer (ALB)
- AWS Network Load Balancer (NLB)
- Azure Load Balancer
- Azure Application Gateway
- Google Cloud Load Balancer

Cloud providers manage infrastructure automatically.

---

# Internal vs External Load Balancer

### External

```text
Internet

↓

Load Balancer

↓

Application
```

Public-facing.

---

### Internal

```text
Application

↓

Internal Load Balancer

↓

Database
```

Private communication inside the infrastructure.

---

# Blue-Green Deployment

Traffic switching:

```text
Blue

↓

Production
```

↓

After deployment:

```text
Green

↓

Production
```

The load balancer redirects traffic with minimal downtime.

---

# Canary Deployment

Traffic split:

```text
90%

↓

Old Version
```

```text
10%

↓

New Version
```

Gradually increase traffic after validation.

---

# Production Architecture

```text
Internet

↓

DNS

↓

CDN

↓

Load Balancer

↓

Reverse Proxy

↓

Application Servers

↓

Database
```

Every layer contributes to scalability and reliability.

---

# Security Best Practices

- Enable HTTPS.
- Configure health checks.
- Restrict management access.
- Protect against Distributed Denial of Service (DDoS) attacks.
- Enable request logging.
- Remove unhealthy servers automatically.
- Monitor backend response times.
- Keep load balancer software updated.

---

# Troubleshooting Load Balancers

Verify backend health.

```bash
curl http://backend:8080/health
```

Verify application.

```bash
curl https://app.company.com
```

Inspect DNS.

```bash
dig app.company.com
```

Check TLS.

```bash
openssl s_client -connect app.company.com:443
```

Review load balancer logs and metrics.

---

# Common Problems

| Problem | Possible Cause |
|----------|----------------|
| 502 Bad Gateway | Backend Failure |
| 503 Service Unavailable | No Healthy Servers |
| Uneven Traffic Distribution | Incorrect Algorithm |
| Session Loss | Sticky Sessions Disabled |
| Slow Response | Backend Overloaded |

---

# CLI Examples

Test backend.

```bash
curl http://backend:8080/health
```

Test application.

```bash
curl https://app.company.com
```

Verify DNS.

```bash
dig app.company.com
```

Verify TLS.

```bash
openssl s_client -connect app.company.com:443
```

---

# Hands-on Lab

## Task 1

Deploy three web servers.

Configure a load balancer.

Verify requests are distributed.

---

## Task 2

Enable Round Robin.

Refresh the application repeatedly.

Observe backend selection.

---

## Task 3

Configure health checks.

Stop one backend.

Verify it is automatically removed.

---

## Task 4

Enable sticky sessions.

Verify repeated requests from the same client reach the same backend.

---

## Task 5

Enable HTTPS termination.

Verify secure client communication.

---

## Task 6

Deploy an application in Kubernetes.

Expose it using a LoadBalancer Service.

Verify traffic reaches multiple Pods.

---

## Task 7

Perform a rolling deployment.

Observe uninterrupted application availability.

---

## Task 8

Draw the following architecture:

```text
Internet

↓

DNS

↓

CDN

↓

Load Balancer

↓

Reverse Proxy

↓

Application Servers

↓

Database
```

Explain how traffic flows through each component.

---

# Popular Load Balancers

| Solution | Type |
|-----------|------|
| NGINX | Software |
| HAProxy | Software |
| Envoy | Software |
| Traefik | Software |
| AWS ALB | Cloud |
| AWS NLB | Cloud |
| Azure Load Balancer | Cloud |
| Google Cloud Load Balancer | Cloud |

---

# Load Balancer vs Reverse Proxy

| Load Balancer | Reverse Proxy |
|---------------|---------------|
| Distributes Traffic | Routes Requests |
| Health Checks | URL Routing |
| High Availability | TLS Termination |
| Horizontal Scaling | Authentication |
| Session Persistence | Caching & Compression |

> Many modern solutions such as **NGINX**, **HAProxy**, **Envoy**, and **Traefik** provide both reverse proxy and load balancing capabilities.

---

# Common Mistakes

❌ Not configuring health checks.

✅ Continuously verify backend health.

---

❌ Using a single backend server.

✅ Deploy multiple instances for redundancy.

---

❌ Ignoring session persistence requirements.

✅ Enable sticky sessions when required.

---

❌ Exposing backend servers directly.

✅ Route all traffic through the load balancer.

---

❌ Not monitoring backend response times.

✅ Continuously collect performance metrics.

---

# Interview Questions

## Beginner

1. What is load balancing?
2. Why do we use a load balancer?
3. What is Round Robin?
4. What is a health check?

---

## Intermediate

1. Compare Layer 4 and Layer 7 load balancing.
2. Explain sticky sessions.
3. How does Kubernetes perform load balancing?
4. What is SSL termination?

---

## Architect Level

1. Design a highly available load balancing architecture for a global application.
2. Explain how autoscaling and load balancing work together.
3. How would you troubleshoot uneven traffic distribution across backend servers?

---

# Summary

In this lesson, you learned:

- Load Balancing Fundamentals
- Layer 4 and Layer 7 Load Balancing
- Load Balancing Algorithms
- Health Checks
- Session Persistence
- TLS Termination
- Kubernetes Load Balancing
- Cloud Load Balancers
- Blue-Green and Canary Deployments
- Production High Availability

Load balancing is a fundamental building block of modern distributed systems. It improves application availability, scalability, and reliability by intelligently distributing traffic across healthy backend servers. Combined with reverse proxies, autoscaling, and cloud-native infrastructure, load balancers enable resilient, production-ready DevOps platforms.

---

## Key Takeaways

- Load balancers distribute requests across multiple healthy backends.
- **Layer 4** operates at the transport layer, while **Layer 7** understands application protocols.
- Health checks prevent traffic from reaching unhealthy servers.
- Sticky sessions maintain user affinity when required.
- Cloud platforms provide fully managed load balancing services.
- Load balancing enables high availability, scalability, and zero-downtime deployments.

---

## What's Next?

**[CDN](cdn.md)**

In the next lesson, you'll learn about **CDN (Content Delivery Network)**.

You'll explore:

- CDN Fundamentals
- Edge Locations
- Content Caching
- Cache Invalidation
- Static vs Dynamic Content
- CDN Security
- Production CDN Architecture

By the end of the lesson, you'll understand how CDNs improve application performance, reduce latency, and deliver content efficiently to users around the world.
