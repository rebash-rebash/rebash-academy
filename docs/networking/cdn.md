---
title: "CDN"
description: "Learn Content Delivery Networks — edge caching, cache hits/misses, invalidation, HTTPS, DDoS/WAF, and production CDN architecture."
difficulty: intermediate
estimated_time: "220 min"
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
  - cdn
  - caching
  - devops
  - rebash-networking-mastery
comments: false
status: ready
---

# CDN (Content Delivery Network) — Accelerating Content Delivery Worldwide

> A **Content Delivery Network (CDN)** is a globally distributed network of servers that delivers content to users from the **nearest geographic location**, reducing latency and improving application performance. Instead of serving every request from the origin server, a CDN caches content at edge locations around the world. CDNs improve **website speed, application performance, scalability, availability, and security**, making them a critical component of modern DevOps and cloud-native architectures. Every DevOps Engineer, Platform Engineer, SRE, Cloud Engineer, and Cloud Architect should understand CDN architecture and operation.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 13: DevOps Networking → Lesson 8</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 220 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** DevOps Networking</div>

<div markdown>**Lesson:** 8 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand CDN architecture
- Learn how edge caching works
- Differentiate static and dynamic content
- Configure cache policies
- Understand CDN security features
- Troubleshoot CDN issues
- Design production CDN architectures

---

# Prerequisites

Complete:

- DNS
- HTTP
- HTTPS
- [Reverse Proxy](reverse-proxy-and-ingress-basics.md)
- [Load Balancing](load-balancing-fundamentals.md)

Basic understanding of:

- Web Applications
- TCP/IP
- Browser Caching

---

# Why Do We Need a CDN?

Imagine your application is hosted in:

```text
Singapore
```

Users connect from:

- India
- USA
- Germany
- Australia
- Brazil

Without a CDN:

```text
User

↓

Internet

↓

Origin Server
```

Every request travels across the globe.

This results in:

- Higher Latency
- Slower Page Loads
- Increased Server Load

---

# What is a CDN?

A CDN is:

```text
Global

Network

Of

Edge

Servers
```

that stores copies of content closer to users.

---

# CDN Architecture

```text
User

↓

Nearest Edge Server

↓

Origin Server
```

If content is already cached, the edge server responds immediately.

---

# How a CDN Works

Step 1

User requests:

```text
logo.png
```

↓

Edge server checks cache.

---

Step 2

If cached:

```text
Cache Hit

↓

Return Content
```

---

Step 3

If not cached:

```text
Cache Miss

↓

Origin Server

↓

Edge Cache

↓

User
```

Future requests are served from the edge.

---

# Edge Locations

CDNs operate:

```text
Worldwide
```

Example:

```text
India

USA

Germany

Australia

Japan
```

Users automatically connect to the closest edge location.

---

# Origin Server

The original application server.

```text
CDN

↓

Origin
```

Only uncached requests reach the origin.

---

# Static Content

Excellent CDN candidates:

- Images
- CSS
- JavaScript
- Fonts
- Videos
- PDFs

Static assets are cached efficiently.

---

# Dynamic Content

Examples:

- Login
- Shopping Cart
- User Dashboard
- Payment APIs

Dynamic content is typically forwarded to the origin, though many CDNs can optimize or selectively cache it based on application logic.

---

# Cache Hit

```text
User

↓

CDN

↓

Response
```

Origin server is **not** contacted.

Benefits:

- Faster Response
- Lower Origin Load

---

# Cache Miss

```text
User

↓

CDN

↓

Origin

↓

CDN

↓

User
```

Content is retrieved from the origin and cached.

---

# Cache Expiration

Content remains cached for a defined period.

Common mechanisms:

- Cache-Control
- Expires Header
- Time-To-Live (TTL)

After expiration:

```text
Refresh

From

Origin
```

---

# Cache-Control Header

Example:

```text
Cache-Control:

max-age=3600
```

Meaning:

```text
Cache

For

1 Hour
```

---

# Cache Invalidation

After deploying a new version:

```text
Old Cache

↓

Invalidate

↓

New Content
```

Methods:

- Purge
- Invalidate Path
- Versioned URLs

---

# Browser Cache vs CDN Cache

| Browser Cache | CDN Cache |
|---------------|-----------|
| Stored on User Device | Stored at Edge Server |
| Individual User | Shared by Many Users |
| Local Access | Global Access |
| Controlled by Browser | Controlled by CDN |

---

# CDN and DNS

Workflow:

```text
User

↓

DNS

↓

Nearest Edge

↓

Content
```

DNS directs users to the nearest CDN edge location.

---

# CDN and HTTPS

CDNs support:

- TLS Certificates
- HTTPS
- HTTP/2
- HTTP/3 (QUIC)

Encrypted communication is maintained between clients and CDN edge servers.

---

# Compression

CDNs compress content.

Example:

```text
1 MB

↓

250 KB
```

Algorithms:

- Gzip
- Brotli

Benefits:

- Faster Downloads
- Lower Bandwidth Usage

---

# Image Optimization

Many CDNs automatically:

- Resize Images
- Compress Images
- Convert Formats
- Optimize Delivery

This improves website performance.

---

# DDoS Protection

CDNs absorb large traffic volumes.

```text
Attack

↓

CDN

↓

Application
```

The origin server is protected from many volumetric attacks.

---

# Web Application Firewall (WAF)

Many CDNs provide integrated WAF capabilities.

Features:

- SQL Injection Protection
- Cross-Site Scripting (XSS) Protection
- Bot Detection
- Rate Limiting
- IP Filtering

---

# CDN in DevOps

Deployment workflow:

```text
CI/CD

↓

Deploy

↓

Invalidate Cache

↓

Users Receive New Content
```

Automated cache invalidation is a common pipeline step.

---

# CDN in Kubernetes

Architecture:

```text
Internet

↓

CDN

↓

Load Balancer

↓

Ingress

↓

Pods
```

Static content is served by the CDN, while dynamic requests reach the Kubernetes cluster.

---

# Popular CDN Providers

Examples:

- Amazon CloudFront
- Cloudflare
- Google Cloud CDN
- Azure CDN
- Fastly
- Akamai

---

# Production Architecture

```text
Users

↓

DNS

↓

CDN

↓

Load Balancer

↓

Reverse Proxy

↓

Application

↓

Database
```

The CDN becomes the first layer serving client requests.

---

# Security Best Practices

- Enable HTTPS.
- Cache only appropriate content.
- Configure cache-control headers correctly.
- Use cache invalidation during deployments.
- Enable WAF protection.
- Enable Distributed Denial of Service (DDoS) mitigation.
- Monitor cache hit ratios.
- Restrict direct access to the origin server where possible.

---

# Troubleshooting CDN

Verify headers.

```bash
curl -I https://example.com
```

Look for:

- Cache-Control
- Age
- Via

Verify DNS.

```bash
dig example.com
```

Check response time.

```bash
curl -w "%{time_total}\n" https://example.com
```

---

# Common Problems

| Problem | Possible Cause |
|----------|----------------|
| Old Content | Cache Not Invalidated |
| Slow Response | Cache Miss |
| Origin Overload | Low Cache Hit Ratio |
| HTTPS Error | Certificate Misconfiguration |
| 404 at Edge | Origin Content Missing |

---

# CLI Examples

View response headers.

```bash
curl -I https://example.com
```

Measure response time.

```bash
curl -w "%{time_total}\n" https://example.com
```

Resolve DNS.

```bash
dig example.com
```

Test HTTPS.

```bash
openssl s_client -connect example.com:443
```

---

# Hands-on Lab

## Task 1

Deploy a static website.

Serve it through a CDN.

---

## Task 2

Upload:

- Images
- CSS
- JavaScript

Verify caching.

---

## Task 3

Inspect response headers.

```bash
curl -I https://example.com
```

Identify:

- Cache-Control
- Age
- Via

---

## Task 4

Modify a static file.

Invalidate the CDN cache.

Verify updated content is delivered.

---

## Task 5

Enable HTTPS.

Verify secure delivery.

---

## Task 6

Enable compression.

Compare response sizes before and after.

---

## Task 7

Deploy an application on Kubernetes.

Serve static assets through a CDN while routing API requests to the cluster.

---

## Task 8

Draw the following architecture:

```text
Users

↓

DNS

↓

CDN

↓

Load Balancer

↓

Reverse Proxy

↓

Application

↓

Database
```

Explain how requests flow and identify where caching occurs.

---

# CDN vs Reverse Proxy

| CDN | Reverse Proxy |
|------|---------------|
| Global Edge Network | Single Entry Point |
| Geographic Distribution | Local Infrastructure |
| Content Caching | Request Routing |
| DDoS Protection | TLS Termination |
| Performance Optimization | Backend Security |

---

# CDN vs Browser Cache

| CDN | Browser Cache |
|------|---------------|
| Shared Cache | User-Specific Cache |
| Global | Local Device |
| Edge Locations | Browser Storage |
| Reduces Origin Load | Reduces Repeat Downloads |
| Managed Centrally | Managed by Client |

---

# Common Mistakes

❌ Caching dynamic content without validation.

✅ Cache only appropriate responses.

---

❌ Forgetting cache invalidation after deployment.

✅ Automate cache purging in CI/CD.

---

❌ Allowing direct origin access.

✅ Restrict origin access to the CDN where possible.

---

❌ Ignoring cache headers.

✅ Configure Cache-Control and TTL correctly.

---

❌ Not monitoring cache hit ratio.

✅ Track CDN metrics continuously.

---

# Interview Questions

## Beginner

1. What is a CDN?
2. Why do websites use CDNs?
3. What is a cache hit?
4. What is an edge server?

---

## Intermediate

1. Compare cache hit and cache miss.
2. Explain cache invalidation.
3. How does a CDN improve performance?
4. How do CDNs protect against DDoS attacks?

---

## Architect Level

1. Design a global CDN architecture for a high-traffic application.
2. Explain how a CDN integrates with Kubernetes.
3. How would you troubleshoot stale content being served from a CDN?

---

# Summary

In this lesson, you learned:

- CDN Architecture
- Edge Locations
- Origin Server
- Cache Hit
- Cache Miss
- Cache-Control
- Cache Invalidation
- DDoS Protection
- WAF
- Production CDN Design

Content Delivery Networks significantly improve application performance by serving content from geographically distributed edge servers. They reduce latency, decrease origin server load, improve availability, and provide integrated security features such as DDoS protection and Web Application Firewalls. CDNs are an essential component of modern DevOps and cloud-native architectures.

---

## Key Takeaways

- CDNs cache content at **edge locations** close to users.
- **Cache hits** reduce latency and origin server load.
- Configure **Cache-Control** headers and TTL values appropriately.
- Automate **cache invalidation** during deployments.
- Modern CDNs provide **HTTPS**, **compression**, **DDoS protection**, and **WAF** capabilities.
- Combine CDNs with load balancers and reverse proxies for highly scalable architectures.

---

## What's Next?

**[API Gateways](api-gateways.md)**

In the next lesson, you'll learn about **API Gateways**.

You'll explore:

- API Gateway Architecture
- API Routing
- Authentication and Authorization
- Rate Limiting
- Request Transformation
- API Versioning
- Production API Management

By the end of the lesson, you'll understand how API Gateways manage, secure, and route API traffic across modern microservices and cloud-native applications.
