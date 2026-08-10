---
title: "Ingress"
description: "Learn Kubernetes Ingress — Ingress Controllers, host and path routing, TLS termination, virtual hosting, and production HTTP/HTTPS exposure architectures."
difficulty: advanced
estimated_time: "220 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 11 · Kubernetes Networking"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - kubernetes
  - ingress
  - http
  - rebash-networking-mastery
comments: false
status: ready
---

# Ingress — Exposing HTTP and HTTPS Applications in Kubernetes

> **Ingress** is a Kubernetes API resource that manages **external HTTP and HTTPS access** to applications running inside a Kubernetes cluster. Instead of exposing every application with its own LoadBalancer or NodePort Service, an Ingress provides **a single entry point** that intelligently routes requests to different backend Services based on **hostnames, URL paths, headers, or other HTTP rules**. Combined with an **Ingress Controller**, it enables SSL/TLS termination, virtual hosting, load balancing, authentication, and advanced traffic management. Every Kubernetes Administrator, DevOps Engineer, Platform Engineer, Site Reliability Engineer (SRE), Cloud Architect, and Network Engineer should understand Kubernetes Ingress.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 11: Kubernetes Networking → Lesson 4</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Advanced</div>

<div markdown>**Reading Time:** 220 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Kubernetes Networking</div>

<div markdown>**Lesson:** 4 of 9</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Kubernetes Ingress
- Learn the role of an Ingress Controller
- Configure Host-Based Routing
- Configure Path-Based Routing
- Enable HTTPS using Transport Layer Security (TLS)
- Compare Ingress with LoadBalancer Services
- Design production-ready Kubernetes ingress architectures

---

# Prerequisites

Complete:

- [Pod Networking](pod-networking.md)
- [Service Networking](service-networking.md)
- DNS Fundamentals
- Load Balancers
- Kubernetes Fundamentals

---

# Why Do We Need Ingress?

Imagine a Kubernetes cluster hosting:

- Frontend
- Backend API
- Authentication Service
- Admin Portal

Without Ingress:

```text
Frontend

↓

LoadBalancer
```

```text
API

↓

LoadBalancer
```

```text
Admin

↓

LoadBalancer
```

Problems:

- Multiple Public IPs
- Higher Cost
- Complex Domain Name System (DNS) Management
- Difficult SSL Management

Instead:

```text
One

Ingress

↓

Multiple Applications
```

---

# What is Ingress?

Ingress is:

```text
A

Kubernetes

HTTP/HTTPS

Routing

Resource
```

It routes external traffic to Kubernetes Services.

Ingress works only with an **Ingress Controller**.

---

# Ingress Architecture

```text
Internet

↓

Load Balancer

↓

Ingress Controller

↓

Ingress Rules

↓

Services

↓

Pods
```

The Ingress resource defines the routing rules.

The Ingress Controller enforces those rules.

---

# What is an Ingress Controller?

An Ingress resource contains only configuration.

The actual traffic handling is performed by an:

```text
Ingress

Controller
```

Popular controllers include:

- NGINX Ingress Controller
- HAProxy Ingress
- Traefik
- AWS Load Balancer Controller
- Kong
- Istio Ingress Gateway

Without an Ingress Controller:

```text
Ingress

Does

Nothing
```

---

# Traffic Flow

```text
User

↓

DNS

↓

Load Balancer

↓

Ingress Controller

↓

Service

↓

Pods
```

Every HTTP request follows this path.

---

# Host-Based Routing

Example:

```text
app.company.com

↓

Frontend Service
```

```text
api.company.com

↓

API Service
```

The hostname determines which backend Service receives the request.

---

# Path-Based Routing

Example:

```text
company.com/

↓

Frontend
```

```text
company.com/api

↓

API
```

```text
company.com/admin

↓

Admin
```

The URL path determines the destination.

---

# Example Ingress Rule

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
spec:
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

The Ingress routes requests for `app.example.com` to the `frontend` Service.

---

# TLS Termination

Instead of every application managing certificates:

```text
Client

↓

HTTPS

↓

Ingress Controller

↓

HTTP

↓

Application
```

Benefits:

- Centralised Certificate Management
- Easier HTTPS Deployment
- Reduced Backend Complexity

---

# TLS Secret

Certificates are stored as Kubernetes Secrets.

Example:

```yaml
tls:
- hosts:
  - app.example.com
  secretName: tls-secret
```

The Ingress Controller uses the certificate during the TLS handshake.

---

# Virtual Hosting

A single Ingress can host multiple domains.

Example:

```text
shop.company.com

↓

Shopping Service
```

```text
blog.company.com

↓

Blog Service
```

```text
api.company.com

↓

API Service
```

---

# Default Backend

If no rule matches:

```text
Request

↓

Default Backend
```

This usually returns:

```text
404 Not Found
```

or a custom error page.

---

# Load Balancing

The Ingress Controller forwards traffic to the Service.

The Service then distributes requests across healthy Pods.

```text
Ingress

↓

Service

↓

Pod A
```

```text
↓

Pod B
```

```text
↓

Pod C
```

---

# Authentication

Ingress Controllers can integrate with:

- OAuth
- OpenID Connect (OIDC)
- Lightweight Directory Access Protocol (LDAP)
- Basic Authentication

This allows authentication before traffic reaches the application.

---

# Rate Limiting

Ingress Controllers can limit requests.

Example:

```text
100 Requests

Per Minute
```

Benefits:

- API Protection
- Distributed Denial of Service (DDoS) Mitigation
- Fair Resource Usage

---

# URL Rewriting

Example:

Client requests:

```text
/api/users
```

Ingress rewrites to:

```text
/users
```

before forwarding the request.

Useful when backend applications expect different URL structures.

---

# Kubernetes Perspective

Ingress is designed for:

- HTTP
- HTTPS

Protocols such as:

- Transmission Control Protocol (TCP)
- User Datagram Protocol (UDP)

typically require alternative solutions or controller-specific configurations.

---

# Cloud Provider Perspective

## Amazon EKS

Common options:

- AWS Load Balancer Controller
- NGINX Ingress Controller

Creates AWS Application Load Balancers (ALBs) when configured.

---

## Azure AKS

Common options:

- NGINX Ingress Controller
- Azure Application Gateway Ingress Controller (AGIC)

Integrates with Azure networking services.

---

## Google GKE

Supports:

- GKE Ingress
- NGINX Ingress Controller

Can automatically provision Google Cloud HTTP(S) Load Balancers.

---

# Enterprise Architecture

```text
Internet

↓

DNS

↓

Cloud Load Balancer

↓

Ingress Controller

↓

Frontend Service

↓

Frontend Pods

↓

Backend Service

↓

Backend Pods

↓

Database
```

This architecture supports multiple applications through a single public endpoint.

---

# Ingress vs LoadBalancer Service

| Ingress | LoadBalancer Service |
|----------|----------------------|
| Layer 7 | Layer 4 |
| HTTP/HTTPS | TCP/UDP |
| Multiple Applications | One Service |
| Host Routing | No Host Routing |
| Path Routing | No Path Routing |
| TLS Termination | Limited |

---

# CLI Examples

List Ingress resources.

```bash
kubectl get ingress
```

Describe an Ingress.

```bash
kubectl describe ingress web-ingress
```

Display Ingress YAML.

```bash
kubectl get ingress web-ingress -o yaml
```

View Ingress Controller Pods.

```bash
kubectl get pods -n ingress-nginx
```

---

# Common Ingress Components

| Component | Purpose |
|-----------|----------|
| Ingress | Routing Rules |
| Ingress Controller | Traffic Processing |
| Service | Backend Endpoint |
| Pod | Application |
| TLS Secret | SSL Certificate |
| DNS | Name Resolution |

---

# Hands-on Lab

## Task 1

List Ingress resources.

```bash
kubectl get ingress
```

---

## Task 2

Describe an Ingress.

```bash
kubectl describe ingress web-ingress
```

---

## Task 3

Deploy:

- Frontend Service
- Backend Service
- Ingress

Verify routing.

---

## Task 4

Configure:

- Host-Based Routing
- Path-Based Routing

for multiple applications.

---

## Task 5

Enable HTTPS using a TLS Secret.

---

## Task 6

Deploy the NGINX Ingress Controller and expose multiple applications through a single public IP.

---

## Task 7

Implement rate limiting and basic authentication for an API exposed through Ingress.

---

## Task 8

Draw a production Kubernetes ingress architecture showing:

- Internet
- DNS
- Cloud Load Balancer
- Ingress Controller
- Ingress
- Services
- Pods

Explain how a request for:

```text
https://api.company.com/users
```

travels through the Kubernetes cluster.

---

# Production Troubleshooting

Problem:

```text
User

Receives

404

From

Ingress
```

Check:

- DNS Resolution
- Ingress Rules
- Hostname
- Path Configuration
- Service Availability
- Endpoints
- Ingress Controller Logs
- TLS Configuration

Workflow:

```text
Client

↓

DNS

↓

Load Balancer

↓

Ingress Controller

↓

Service

↓

Pod
```

---

# Common Mistakes

❌ Creating an Ingress without an Ingress Controller.

✅ Install and verify an Ingress Controller.

---

❌ Incorrect host or path rules.

✅ Validate routing configuration carefully.

---

❌ Missing TLS Secret.

✅ Create and reference the correct certificate Secret.

---

❌ Exposing every Service with a LoadBalancer.

✅ Use a shared Ingress for HTTP/HTTPS applications.

---

❌ Ignoring controller logs.

✅ Review Ingress Controller logs during troubleshooting.

---

# Best Practices

- Use one Ingress to expose multiple web applications.
- Enable HTTPS for all external endpoints.
- Store certificates in Kubernetes Secrets.
- Use Host-Based Routing for multiple domains.
- Use Path-Based Routing for microservices.
- Enable authentication and rate limiting where appropriate.
- Monitor Ingress latency, errors, and controller health.
- Deploy multiple Ingress Controller replicas for high availability.

---

# Interview Questions

## Beginner

1. What is Kubernetes Ingress?
2. Why do we need an Ingress Controller?
3. What is Host-Based Routing?
4. What is Path-Based Routing?

---

## Intermediate

1. Compare Ingress and LoadBalancer Services.
2. Explain TLS termination in Kubernetes.
3. What is the role of the Ingress Controller?
4. How does an Ingress route requests to backend Services?

---

## Architect Level

1. Design a production Ingress architecture for a microservices platform.
2. Explain how to expose multiple applications through a single public IP.
3. How would you troubleshoot intermittent 404 or 502 errors from an Ingress Controller?

---

# Summary

In this lesson, you learned:

- Kubernetes Ingress
- Ingress Controllers
- Host-Based Routing
- Path-Based Routing
- TLS Termination
- Virtual Hosting
- Authentication
- Rate Limiting
- Cloud Ingress Integrations

Ingress provides a centralised Layer 7 entry point for Kubernetes applications. By combining routing rules, TLS termination, authentication, and cloud load balancers, Ingress simplifies application exposure while improving scalability, security, and operational efficiency.

---

## Key Takeaways

- **Ingress** provides Layer 7 HTTP/HTTPS routing in Kubernetes.
- An **Ingress Controller** is required to process Ingress resources.
- **Host-Based** and **Path-Based Routing** allow multiple applications to share one public endpoint.
- TLS termination centralises HTTPS certificate management.
- Ingress integrates with cloud load balancers and Kubernetes Services.
- Production deployments should include authentication, rate limiting, monitoring, and high availability.

---

## What's Next?

**[Network Policies](network-policies.md)**

In the next lesson, you'll learn about **Network Policies**.

You'll explore:

- What Network Policies are
- Ingress and Egress Rules
- Pod Isolation
- Label-Based Security
- Default Deny Policies
- CNI Support
- Zero Trust Networking

By the end of the lesson, you'll understand how to secure communication between Kubernetes workloads using fine-grained network access controls.
