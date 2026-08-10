---
title: "Network Policies"
description: "Learn Kubernetes Network Policies — ingress/egress rules, Pod isolation, default deny, Zero Trust networking, and CNI policy enforcement with Calico and Cilium."
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
  - network-policies
  - security
  - rebash-networking-mastery
comments: false
status: ready
---

# Network Policies — Securing Pod-to-Pod Communication in Kubernetes

> **Network Policies** are Kubernetes resources that control **how Pods communicate with each other and with external networks**. By default, Kubernetes allows all Pods to communicate freely within the cluster. Network Policies introduce **fine-grained network access control**, enabling organisations to implement **Zero Trust networking**, isolate workloads, and enforce least-privilege communication. Network Policies are implemented by **CNI plugins** such as **Calico**, **Cilium**, and **Antrea**. Every Kubernetes Administrator, DevOps Engineer, Platform Engineer, Site Reliability Engineer (SRE), Cloud Architect, and Security Engineer should understand Network Policies.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 11: Kubernetes Networking → Lesson 5</p>

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

<div markdown>**Lesson:** 5 of 9</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Kubernetes Network Policies
- Configure Ingress and Egress rules
- Isolate workloads using labels
- Implement Zero Trust networking
- Understand CNI support for Network Policies
- Design secure Kubernetes architectures
- Troubleshoot network access issues

---

# Prerequisites

Complete:

- [CNI](kubernetes-networking-fundamentals.md)
- [Pod Networking](pod-networking.md)
- [Service Networking](service-networking.md)
- [Ingress](ingress.md)
- Kubernetes Fundamentals

Basic understanding of:

- IP Routing
- Firewalls
- Network Security

---

# Why Do We Need Network Policies?

Imagine a Kubernetes cluster containing:

- Frontend Pods
- Backend Pods
- Database Pods
- Monitoring Pods

By default:

```text
Every Pod

Can Talk

To Every

Other Pod
```

Problems:

- Poor Security
- Lateral Movement
- Increased Attack Surface

Instead:

```text
Only

Required

Communication

Is Allowed
```

---

# What is a Network Policy?

A Network Policy is:

```text
A

Firewall

For

Pods
```

It controls:

- Incoming Traffic (Ingress)
- Outgoing Traffic (Egress)

using Pod labels, namespaces, and IP blocks.

---

# Default Kubernetes Behavior

Without Network Policies:

```text
Pod A

⇄

Pod B

⇄

Pod C

⇄

Pod D
```

Everything is allowed.

---

# Zero Trust Model

With Network Policies:

```text
Frontend

↓

Backend

↓

Database
```

Blocked:

```text
Frontend

✖

Database
```

Only explicitly allowed communication is permitted.

---

# Network Policy Components

A Network Policy defines:

- Pod Selector
- Policy Types
- Ingress Rules
- Egress Rules

---

# Pod Selector

Policies apply to Pods selected by labels.

Example:

```yaml
podSelector:
  matchLabels:
    app: backend
```

Only Pods labeled:

```text
app=backend
```

are affected.

---

# Policy Types

Network Policies support:

```yaml
policyTypes:
- Ingress
- Egress
```

Ingress controls incoming traffic.

Egress controls outgoing traffic.

---

# Ingress Rules

Allow traffic **to** selected Pods.

Example:

```text
Frontend

↓

Backend
```

Allowed.

```text
Database

↓

Backend
```

Blocked unless explicitly permitted.

---

# Egress Rules

Allow traffic **from** selected Pods.

Example:

```text
Backend

↓

Database
```

Allowed.

```text
Backend

↓

Internet
```

Blocked unless permitted.

---

# Default Deny Policy

A common security practice.

Example:

```yaml
podSelector: {}
policyTypes:
- Ingress
```

Result:

```text
All

Ingress

Blocked
```

Until explicit allow rules are added.

---

# Allow Specific Traffic

Example:

```text
Frontend

↓

Backend
```

Allowed.

Everything else remains blocked.

This follows the principle of least privilege.

---

# Namespace Isolation

Policies can restrict communication between namespaces.

Example:

```text
Production

↓

Production
```

Allowed.

```text
Development

↓

Production
```

Blocked.

---

# IP Block Rules

Allow traffic from specific networks.

Example:

```yaml
ipBlock:
  cidr: 10.10.0.0/16
```

Useful for:

- On-Premises Systems
- Monitoring Servers
- External Gateways

---

# Label-Based Security

Example:

Frontend Pods:

```yaml
labels:
  role: frontend
```

Backend Pods:

```yaml
labels:
  role: backend
```

Policy:

```text
Frontend

↓

Backend
```

Only matching Pods communicate.

---

# Example Network Policy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-policy
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
```

Only Pods labeled:

```text
app=frontend
```

can access backend Pods.

---

# CNI Support

Not every Container Network Interface (CNI) plugin enforces Network Policies.

Popular implementations:

| CNI | Network Policy Support |
|-----|------------------------|
| Calico | Yes |
| Cilium | Yes |
| Antrea | Yes |
| Weave Net | Yes |
| Flannel | No (requires an additional policy engine) |

Always verify CNI capabilities before relying on Network Policies.

---

# Kubernetes Perspective

Network Policies apply to:

- Pod-to-Pod Traffic
- Namespace-to-Namespace Traffic
- External Traffic
- Internet Access

They do **not** replace:

- Ingress Controllers
- Service Mesh
- Cloud Firewalls

They complement them.

---

# Enterprise Architecture

```text
Internet

↓

Ingress

↓

Frontend Pods

↓

Backend Pods

↓

Database Pods
```

Allowed:

```text
Frontend

↓

Backend
```

```text
Backend

↓

Database
```

Blocked:

```text
Frontend

✖

Database
```

```text
Monitoring

✖

Database
```

unless explicitly allowed.

---

# Zero Trust Architecture

```text
Default

Deny

↓

Explicit

Allow

↓

Least

Privilege
```

Every connection must be intentionally permitted.

---

# Cloud Provider Perspective

## Amazon EKS

Common options:

- Amazon VPC CNI + Network Policy support
- Calico
- Cilium

---

## Azure AKS

Supports:

- Azure CNI
- Cilium
- Calico (supported configurations)

---

## Google GKE

Supports:

- Network Policy using Calico (Standard)
- Dataplane V2 with Cilium/eBPF

---

# Production Workflow

```text
Request

↓

Network Policy

↓

Allowed?

↓

Yes

↓

Destination Pod
```

Otherwise:

```text
Denied
```

---

# CLI Examples

List Network Policies.

```bash
kubectl get networkpolicy
```

Describe a policy.

```bash
kubectl describe networkpolicy backend-policy
```

Display YAML.

```bash
kubectl get networkpolicy backend-policy -o yaml
```

---

# Common Network Policy Components

| Component | Purpose |
|-----------|----------|
| Pod Selector | Select Target Pods |
| Ingress | Incoming Rules |
| Egress | Outgoing Rules |
| Namespace Selector | Namespace Filtering |
| IP Block | CIDR-Based Rules |
| Policy Types | Ingress/Egress Control |

---

# Hands-on Lab

## Task 1

List Network Policies.

```bash
kubectl get networkpolicy
```

---

## Task 2

Create a default deny policy.

---

## Task 3

Allow:

```text
Frontend

↓

Backend
```

communication.

---

## Task 4

Allow:

```text
Backend

↓

Database
```

communication.

---

## Task 5

Verify that:

```text
Frontend

✖

Database
```

traffic is blocked.

---

## Task 6

Allow monitoring Pods to scrape application metrics while denying all other unsolicited traffic.

---

## Task 7

Implement namespace isolation between:

- Development
- Staging
- Production

---

## Task 8

Draw a production Kubernetes security architecture including:

- Ingress
- Frontend Pods
- Backend Pods
- Database Pods
- Monitoring
- Network Policies

Explain which traffic is allowed and which traffic is denied.

---

# Production Troubleshooting

Problem:

```text
Pod

Cannot

Reach

Another Pod
```

Check:

- Network Policy
- Pod Labels
- Namespace Labels
- CNI Plugin
- Domain Name System (DNS)
- Service Configuration
- Application Logs

Workflow:

```text
Source Pod

↓

Network Policy

↓

Service

↓

Destination Pod
```

---

# Network Policies vs Security Groups

| Network Policies | Cloud Security Groups |
|------------------|-----------------------|
| Pod Level | VM / Instance Level |
| Kubernetes Native | Cloud Native |
| Label Based | IP / Instance Based |
| Cluster Internal | Infrastructure Level |
| Micro-Segmentation | Network Perimeter |

---

# Common Mistakes

❌ Assuming Network Policies work without CNI support.

✅ Verify the CNI plugin supports policy enforcement.

---

❌ Forgetting egress rules.

✅ Secure both inbound and outbound traffic.

---

❌ Using incorrect labels.

✅ Validate Pod and Namespace labels carefully.

---

❌ Creating allow rules without a default deny policy.

✅ Start with default deny and explicitly allow required traffic.

---

❌ Ignoring DNS traffic.

✅ Allow access to CoreDNS if workloads require name resolution.

---

# Best Practices

- Begin with a **default deny** policy.
- Allow only required communication.
- Use meaningful labels for workload grouping.
- Separate environments using namespaces.
- Monitor policy violations and connectivity.
- Test policies in staging before production.
- Combine Network Policies with Role-Based Access Control (RBAC) and cloud firewalls.
- Follow Zero Trust principles throughout the cluster.

---

# Interview Questions

## Beginner

1. What is a Kubernetes Network Policy?
2. What are Ingress and Egress rules?
3. Why are Network Policies required?
4. What is a default deny policy?

---

## Intermediate

1. Explain how Pod Selectors work.
2. Compare Network Policies with cloud Security Groups.
3. Which CNI plugins support Network Policies?
4. How do Namespace Selectors improve security?

---

## Architect Level

1. Design a Zero Trust networking architecture for Kubernetes.
2. Explain how to isolate production workloads using Network Policies.
3. How would you troubleshoot application failures caused by overly restrictive Network Policies?

---

# Summary

In this lesson, you learned:

- Kubernetes Network Policies
- Pod Selectors
- Ingress Rules
- Egress Rules
- Namespace Isolation
- IP Block Rules
- Default Deny Policies
- Zero Trust Networking
- CNI Policy Enforcement

Network Policies provide fine-grained control over Pod communication in Kubernetes. By implementing least-privilege access and default-deny strategies, organisations can significantly reduce lateral movement, improve workload isolation, and strengthen the overall security posture of their Kubernetes clusters.

---

## Key Takeaways

- **Network Policies** act as firewalls for Kubernetes Pods.
- Policies control both **Ingress** and **Egress** traffic.
- **Default deny** followed by explicit allow rules is a security best practice.
- Policies rely on **labels**, **namespaces**, and **IP blocks** for traffic selection.
- Enforcement depends on a **CNI plugin** that supports Network Policies.
- Network Policies are a key building block of **Zero Trust Kubernetes security**.

---

## What's Next?

**[CoreDNS](coredns.md)**

In the next lesson, you'll learn about **CoreDNS**.

You'll explore:

- What CoreDNS is
- Kubernetes DNS Architecture
- Service Discovery
- DNS Resolution
- DNS Records
- DNS Forwarding
- Troubleshooting DNS in Kubernetes

By the end of the lesson, you'll understand how Kubernetes automatically provides DNS-based service discovery and how CoreDNS enables reliable communication between applications in the cluster.
