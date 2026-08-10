---
title: "Kubernetes Networking"
description: "Learn Kubernetes networking for DevOps — Pod IPs, Services, CNI, CoreDNS, kube-proxy, Ingress, Network Policies, and production cluster traffic flow."
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
  - kubernetes
  - devops
  - cni
  - rebash-networking-mastery
comments: false
status: ready
---

# Kubernetes Networking — Networking for Cloud-Native Applications

> **Kubernetes Networking** enables seamless communication between **Pods, Services, Nodes, and external clients** in a Kubernetes cluster. Unlike traditional virtualization, Kubernetes assumes that every Pod can communicate with every other Pod without Network Address Translation (NAT). This simple but powerful networking model allows microservices to communicate efficiently while supporting scalability, security, service discovery, and load balancing. Every DevOps Engineer, Platform Engineer, SRE, Cloud Engineer, and Kubernetes Administrator should master Kubernetes networking.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 13: DevOps Networking → Lesson 2</p>

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

<div markdown>**Lesson:** 2 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Kubernetes networking architecture
- Learn the Kubernetes networking model
- Understand Pod-to-Pod communication
- Configure Service networking
- Learn CNI plugins
- Troubleshoot Kubernetes networking
- Design production-ready Kubernetes networks

---

# Prerequisites

Complete:

- [Docker Networking](docker-networking.md)
- Linux Networking
- Routing
- DNS
- Kubernetes Basics

Basic understanding of:

- Containers
- Pods
- Services
- Linux Network Namespaces

---

# Why Do We Need Kubernetes Networking?

Imagine a Kubernetes cluster running:

```text
Frontend Pods

↓

Backend Pods

↓

Database Pods
```

Questions arise:

- How do Pods communicate?
- How do Services discover Pods?
- How does a user access the application?
- How do Pods on different nodes communicate?

Kubernetes Networking provides the answers.

---

# Kubernetes Networking Model

Kubernetes follows four fundamental rules:

- Every Pod gets its own IP address.
- Pods communicate directly without NAT.
- Nodes can communicate with every Pod.
- Pods can communicate across different nodes.

This model simplifies application development because applications do not need to be aware of the underlying network topology.

---

# High-Level Architecture

```text
Internet

↓

Load Balancer

↓

Ingress

↓

Service

↓

Pods

↓

Container
```

Each networking component has a specific responsibility.

---

# Pod Networking

Every Pod receives:

- Unique IP Address
- Network Namespace
- Network Interface
- Routing Table

Example:

```text
Pod A

↓

10.244.1.10
```

```text
Pod B

↓

10.244.2.15
```

Pods communicate directly using these IP addresses.

---

# Pod-to-Pod Communication

Same node:

```text
Pod A

↓

Linux Bridge

↓

Pod B
```

Different nodes:

```text
Pod A

↓

Node A

↓

Cluster Network

↓

Node B

↓

Pod B
```

The Container Network Interface (CNI) manages routing between nodes.

---

# Kubernetes CNI

Kubernetes itself does not implement networking.

Instead, it uses:

```text
Container

Network

Interface

(CNI)
```

Popular CNI plugins:

- Calico
- Cilium
- Flannel
- Weave Net
- Antrea

Each plugin implements the Kubernetes networking model differently.

---

# Service Networking

Pods are temporary.

Services provide:

- Stable Virtual IP
- DNS Name
- Load Balancing

Example:

```text
Frontend

↓

backend.default.svc.cluster.local
```

instead of individual Pod IPs.

---

# Service Types

Common Service types:

- ClusterIP
- NodePort
- LoadBalancer
- ExternalName

Each serves a different access requirement.

---

# ClusterIP

Internal communication only.

```text
Pod

↓

ClusterIP

↓

Backend Pods
```

Default Service type.

---

# NodePort

Expose the Service on every node.

```text
Client

↓

NodeIP:30080

↓

Service

↓

Pods
```

Useful for testing and small environments.

---

# LoadBalancer

Cloud provider creates an external load balancer.

```text
Internet

↓

Cloud Load Balancer

↓

Service

↓

Pods
```

Recommended for production.

---

# Ingress

Ingress provides HTTP and HTTPS routing.

```text
Internet

↓

Ingress Controller

↓

Service

↓

Pods
```

Supports:

- Host-Based Routing
- Path-Based Routing
- TLS Termination

---

# DNS in Kubernetes

CoreDNS provides service discovery.

Example:

```text
backend.default.svc.cluster.local
```

Pods communicate using DNS names instead of IP addresses.

---

# kube-proxy

kube-proxy manages Service networking.

Responsibilities:

- Service Routing
- Load Balancing
- Endpoint Selection

Implementation modes:

- iptables
- IP Virtual Server (IPVS)
- nftables
- eBPF (through supported CNIs such as Cilium)

---

# Network Policies

By default:

```text
All Pods

Can

Communicate
```

Network Policies restrict traffic.

Example:

```text
Frontend

↓

Backend

✓
```

```text
Frontend

↓

Database

✖
```

Only permitted communication is allowed.

---

# External Access

Typical request flow:

```text
User

↓

Load Balancer

↓

Ingress

↓

Service

↓

Pod
```

External traffic never connects directly to individual Pods.

---

# Internal Service Discovery

Example:

```text
Frontend

↓

backend

↓

Database
```

No IP management is required.

CoreDNS resolves Service names automatically.

---

# Multi-Node Networking

```text
Node 1

↓

Pod A

↓

Cluster Network

↓

Node 2

↓

Pod B
```

The CNI plugin ensures connectivity between Pods on different nodes.

---

# Kubernetes Networking in Cloud

Supported on:

- Amazon EKS
- Azure AKS
- Google GKE
- Red Hat OpenShift

Cloud providers integrate Kubernetes networking with:

- VPC/VNet
- Load Balancers
- Security Groups
- Route Tables

---

# Kubernetes Networking in CI/CD

Example deployment:

```text
Git Commit

↓

CI Pipeline

↓

Container Image

↓

Kubernetes Deployment

↓

Service

↓

Ingress
```

Networking automatically connects newly deployed Pods to existing Services.

---

# Troubleshooting Kubernetes Networking

Check Pods.

```bash
kubectl get pods -o wide
```

View Services.

```bash
kubectl get svc
```

View Endpoints.

```bash
kubectl get endpoints
```

Check DNS.

```bash
kubectl exec -it busybox -- nslookup kubernetes.default
```

Verify connectivity.

```bash
kubectl exec -it pod-name -- ping service-name
```

---

# Production Architecture

```text
Internet

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

Database Service

↓

Database Pods
```

Protected by:

- Network Policies
- CoreDNS
- CNI
- kube-proxy
- Cloud Firewalls

---

# Security Best Practices

- Use Network Policies.
- Avoid exposing unnecessary Services.
- Use Ingress instead of multiple LoadBalancer Services.
- Restrict communication between namespaces.
- Enable TLS for external traffic.
- Monitor CoreDNS and kube-proxy.
- Use a production-grade CNI plugin.
- Audit network policies regularly.

---

# Common Problems

| Problem | Possible Cause |
|----------|----------------|
| Pod Cannot Reach Another Pod | CNI Issue |
| Service Not Working | Missing Endpoints |
| DNS Failure | CoreDNS Problem |
| External Access Fails | Ingress or Load Balancer Issue |
| Pod Communication Blocked | Network Policy |

---

# CLI Examples

List Pods.

```bash
kubectl get pods -o wide
```

List Services.

```bash
kubectl get svc
```

List Endpoints.

```bash
kubectl get endpoints
```

Check DNS.

```bash
kubectl exec -it busybox -- nslookup kubernetes.default
```

Test Service connectivity.

```bash
kubectl exec -it pod-name -- curl http://backend
```

---

# Hands-on Lab

## Task 1

Deploy two Pods.

Verify Pod-to-Pod communication.

---

## Task 2

Create a ClusterIP Service.

Access it from another Pod.

---

## Task 3

Deploy an Ingress Controller.

Expose an application through Ingress.

---

## Task 4

Inspect CoreDNS.

```bash
kubectl get pods -n kube-system
```

---

## Task 5

Deploy a Network Policy.

Allow only frontend Pods to access backend Pods.

Verify that unauthorized Pods cannot connect.

---

## Task 6

Deploy a LoadBalancer Service in a cloud Kubernetes cluster.

Verify external access.

---

## Task 7

Simulate a CoreDNS failure.

Troubleshoot and restore service discovery.

---

## Task 8

Draw the following architecture:

```text
Internet

↓

Load Balancer

↓

Ingress

↓

Service

↓

Frontend Pods

↓

Backend Pods

↓

Database Pods
```

Explain how a request travels from the user to the application.

---

# Docker Networking vs Kubernetes Networking

| Docker | Kubernetes |
|----------|------------|
| Single Host Focus | Multi-Node Cluster |
| Bridge Network | CNI Network |
| Container IP | Pod IP |
| Docker DNS | CoreDNS |
| Port Mapping | Services & Ingress |
| Simple Networking | Cloud-Native Networking |

---

# Common Mistakes

❌ Accessing Pods directly.

✅ Use Services for stable access.

---

❌ Hardcoding Pod IPs.

✅ Use Service DNS names.

---

❌ Ignoring Network Policies.

✅ Apply least-privilege networking.

---

❌ Exposing every Service externally.

✅ Use Ingress for HTTP/HTTPS applications.

---

❌ Not monitoring CoreDNS.

✅ Continuously monitor cluster DNS health.

---

# Interview Questions

## Beginner

1. What is Kubernetes networking?
2. What is a Pod IP?
3. What is a Service?
4. What is CoreDNS?

---

## Intermediate

1. Explain the Kubernetes networking model.
2. Compare ClusterIP and LoadBalancer Services.
3. What is a CNI plugin?
4. How does kube-proxy work?

---

## Architect Level

1. Design networking for a production Kubernetes cluster.
2. Explain how traffic flows from the Internet to a Pod.
3. How would you troubleshoot communication failures between Pods across multiple nodes?

---

# Summary

In this lesson, you learned:

- Kubernetes Networking Model
- Pod Networking
- Service Networking
- CNI Plugins
- CoreDNS
- kube-proxy
- Network Policies
- Ingress
- Multi-Node Networking
- Production Kubernetes Networking

Kubernetes networking provides a unified communication model for cloud-native applications. By combining Pods, Services, CoreDNS, CNI plugins, kube-proxy, Ingress, and Network Policies, Kubernetes enables scalable, secure, and reliable communication across distributed applications running on multiple nodes.

---

## Key Takeaways

- Every **Pod** receives its own IP address.
- **Services** provide stable endpoints for dynamic Pods.
- **CoreDNS** enables automatic service discovery.
- **CNI plugins** implement the Kubernetes networking model.
- **Ingress** manages external HTTP and HTTPS traffic.
- **Network Policies** enforce secure communication between workloads.

---

## What's Next?

**[CI/CD Networking](cicd-networking.md)**

In the next lesson, you'll learn about **CI/CD Networking**.

You'll explore:

- Networking in CI/CD Pipelines
- GitLab Runner Networking
- Jenkins Networking
- Container Registry Communication
- Artifact Repository Access
- Kubernetes Deployment Networking
- Production CI/CD Best Practices

By the end of the lesson, you'll understand how networking supports automated software delivery pipelines from source code to production deployments.
