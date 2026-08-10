---
title: "Network Topologies"
description: "Learn physical and logical network topologies — Bus, Star, Ring, Mesh, Tree, and Hybrid — with enterprise, cloud, and Kubernetes use cases."
difficulty: beginner
estimated_time: "90 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 1 · Networking Fundamentals"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - kubernetes-engineer
  - platform-engineer
tags:
  - networking
  - topology
  - fundamentals
  - rebash-networking-mastery
comments: false
status: ready
---

# Network Topologies — Understanding How Devices Are Connected

> A **Network Topology** defines the physical or logical arrangement of devices and communication links within a network. Choosing the right topology directly affects network performance, reliability, scalability, fault tolerance, and maintenance. From small office networks to global cloud data centres, network topologies play a critical role in infrastructure design. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand these fundamental network layouts.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 1: Networking Fundamentals → Lesson 3</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Networking Fundamentals</div>

<div markdown>**Lesson:** 3 of 10</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand network topology
- Differentiate between physical and logical topology
- Explain major network topologies
- Compare advantages and disadvantages
- Identify enterprise use cases
- Choose appropriate topologies for different environments

---

# Prerequisites

Complete:

- [Lesson 1: What is Networking?](introduction-to-networking.md)
- [Lesson 2: Types of Networks (LAN, WAN, MAN, PAN)](types-of-networks.md)

---

# Why Learn Network Topologies?

The way devices are connected affects:

- Performance
- Reliability
- Cost
- Scalability
- Fault tolerance
- Troubleshooting

Example:

```text
Server Failure

↓

Network Design

↓

Business Impact
```

Good network design minimises downtime.

---

# What is a Network Topology?

A network topology is the **layout of devices and communication links** in a network.

It describes:

- How devices connect
- How data travels
- How failures affect communication
- How the network grows

---

# Physical vs Logical Topology

## Physical Topology

Describes the actual physical connections.

Examples:

- Ethernet cables
- Fibre cables
- Wireless links

---

## Logical Topology

Describes how data flows between devices, regardless of physical layout.

Example:

A switched Ethernet network may physically use a **Star Topology**, while data logically flows according to switching rules.

---

# Types of Network Topologies

The most common network topologies are:

- Bus
- Star
- Ring
- Mesh
- Tree
- Hybrid

---

# Bus Topology

In a Bus Topology, all devices connect to a single shared communication cable called the **backbone**.

```text
PC1

 │

PC2

 │

=======================

 │

PC3

 │

PC4
```

Every device shares the same transmission medium.

---

# Advantages of Bus Topology

- Simple design
- Low cost
- Minimal cabling
- Easy for very small networks

---

# Disadvantages of Bus Topology

- Single cable failure affects the entire network
- Difficult troubleshooting
- Poor scalability
- Performance decreases as devices increase
- Rarely used today

---

# Real-World Usage

Historically used in early Ethernet networks.

Modern enterprise networks rarely use Bus Topology.

---

# Star Topology

Every device connects to a central switch or hub.

```text
          Switch

      /    |    \

PC1   PC2   PC3

      \    |    /

        Server
```

This is the most common topology in modern Local Area Networks (LANs).

---

# Advantages of Star Topology

- Easy troubleshooting
- High performance
- Easy expansion
- Failure of one cable affects only one device
- Centralised management

---

# Disadvantages of Star Topology

- Central switch is a single point of failure
- Requires more cabling
- Higher deployment cost

---

# Real-World Usage

Used in:

- Offices
- Data centres
- Schools
- Universities
- Cloud environments

Nearly every enterprise LAN uses Star Topology.

---

# Ring Topology

Devices connect in a circular path.

```text
PC1

↓

PC2

↓

PC3

↓

PC4

↓

Back to PC1
```

Data travels around the ring.

---

# Advantages of Ring Topology

- Predictable communication
- No collisions in traditional token-based implementations
- Equal access for all devices

---

# Disadvantages of Ring Topology

- Single cable failure may interrupt communication
- Difficult maintenance
- Limited scalability

---

# Real-World Usage

Previously used in technologies such as Token Ring and Fibre Distributed Data Interface (FDDI).

Rare in modern enterprise networks.

---

# Mesh Topology

Every device connects to multiple other devices.

```text
      A

    / | \

   B--C--D

    \ | /

      E
```

Mesh provides multiple communication paths.

---

# Types of Mesh

## Full Mesh

Every device connects directly to every other device.

---

## Partial Mesh

Only critical devices have multiple connections.

Most enterprise environments use Partial Mesh.

---

# Advantages of Mesh Topology

- Excellent redundancy
- High availability
- Fault tolerance
- Multiple communication paths
- No single point of failure

---

# Disadvantages of Mesh Topology

- Expensive
- Complex
- Large number of cables
- Difficult management

---

# Real-World Usage

Used in:

- Internet backbone
- Cloud provider networks
- Enterprise Wide Area Networks (WANs)
- Data centre interconnections

---

# Tree Topology

A Tree Topology combines multiple Star Topologies in a hierarchical structure.

```text
            Core Switch

          /            \

Distribution     Distribution

      /   \           /   \

Access Access   Access Access
```

This resembles an organisational hierarchy.

---

# Advantages of Tree Topology

- Highly scalable
- Easy management
- Structured design
- Supports large networks

---

# Disadvantages of Tree Topology

- Core device failure affects many systems
- More expensive
- Complex configuration

---

# Real-World Usage

Used in:

- Enterprise campuses
- Universities
- Large office buildings
- Corporate LANs

---

# Hybrid Topology

A Hybrid Topology combines two or more different topologies.

Example:

```text
Office LAN

↓

Star

↓

Corporate WAN

↓

Mesh

↓

Cloud
```

Most modern enterprise networks are hybrid.

---

# Advantages of Hybrid Topology

- Flexible
- Highly scalable
- Reliable
- Optimised for different requirements

---

# Disadvantages of Hybrid Topology

- Complex design
- Higher implementation cost
- Requires experienced administrators

---

# Real-World Usage

Hybrid Topology is used in:

- Cloud platforms
- Banks
- Government organisations
- Large enterprises
- Data centres
- Internet Service Providers (ISPs)

---

# Comparison

| Topology | Scalability | Reliability | Cost | Modern Usage |
|-----------|------------|------------|------|--------------|
| Bus | Low | Low | Low | Rare |
| Star | High | High | Medium | Very Common |
| Ring | Medium | Medium | Medium | Rare |
| Mesh | Very High | Very High | High | Common |
| Tree | Very High | High | High | Very Common |
| Hybrid | Very High | Very High | High | Most Common |

---

# Enterprise Example

Modern enterprises often use multiple topologies together.

```text
Cloud WAN (Mesh)

        │

Core Data Center (Tree)

        │

Office LAN (Star)

        │

Employees
```

Different parts of the infrastructure use different topologies depending on requirements.

---

# Cloud Perspective

Cloud providers use:

- Mesh Topology for backbone networks
- Tree Topology inside data centres
- Star Topology within racks
- Hybrid designs across global infrastructure

Cloud networking is built on combinations of multiple topologies.

---

# Kubernetes Perspective

Kubernetes clusters commonly use:

- Star Topology inside worker nodes
- Tree Topology across data centre switches
- Mesh networking between clusters (service mesh)
- Hybrid architectures across cloud regions

---

# Production Perspective

Large production environments prioritise:

- Redundancy
- Scalability
- Fault tolerance
- High availability

As a result, modern enterprises primarily use **Star**, **Tree**, **Mesh**, and **Hybrid** topologies.

---

# Hands-on Lab

## Task 1

Draw a Star Topology with:

- One switch
- Four laptops
- One printer

---

## Task 2

Draw a Bus Topology connecting five computers.

---

## Task 3

Draw a Ring Topology connecting six computers.

---

## Task 4

Create a Partial Mesh connecting four routers.

---

## Task 5

Identify the topology used in your home network.

---

## Task 6

Visit your office network (or imagine one) and identify whether it uses Star or Tree Topology.

---

## Task 7

Create an enterprise network diagram using:

- LAN
- WAN
- Star
- Tree
- Mesh

---

## Task 8

Compare all six topologies and recommend the best choice for:

- Home
- School
- Enterprise office
- Cloud provider
- Data centre

Explain your reasoning.

---

# Common Networking Devices by Topology

| Topology | Primary Device |
|-----------|----------------|
| Bus | Shared Cable |
| Star | Switch |
| Ring | Token Ring/FDDI Equipment |
| Mesh | Routers |
| Tree | Core & Distribution Switches |
| Hybrid | Combination of Multiple Devices |

---

# Common Mistakes

❌ Assuming every network uses the same topology.

✅ Different environments use different designs.

---

❌ Believing Mesh is always the best.

✅ Balance redundancy, complexity, and cost.

---

❌ Ignoring scalability.

✅ Choose a topology that supports future growth.

---

❌ Confusing physical and logical topology.

✅ Understand both concepts separately.

---

❌ Using Bus Topology for modern enterprise networks.

✅ Prefer Star, Tree, or Hybrid designs.

---

# Best Practices

- Use Star Topology for small and medium LANs.
- Use Tree Topology for campus and enterprise networks.
- Use Mesh for critical WAN links and backbone networks.
- Design for redundancy and high availability.
- Document network topology using diagrams.
- Avoid unnecessary complexity while maintaining reliability.

---

# Interview Questions

## Beginner

1. What is a network topology?
2. What is the difference between physical and logical topology?
3. Which topology is most common in modern LANs?
4. Why is Bus Topology rarely used today?

---

## Intermediate

1. Compare Star and Mesh Topologies.
2. What are the advantages of Tree Topology?
3. Why do enterprises prefer Hybrid Topology?
4. Which topology provides the highest fault tolerance?

---

## Architect Level

1. Design a network topology for a multinational enterprise.
2. Explain how cloud providers combine different topologies.
3. How would you eliminate single points of failure in a large enterprise network?

---

# Summary

In this lesson, you learned:

- Physical and logical topologies
- Bus Topology
- Star Topology
- Ring Topology
- Mesh Topology
- Tree Topology
- Hybrid Topology
- Enterprise networking designs

Network topology forms the foundation of network architecture. Selecting the appropriate topology ensures scalability, reliability, fault tolerance, and efficient communication. Modern enterprises typically combine multiple topologies to create resilient and highly available infrastructures.

---

## Key Takeaways

- Network topology defines how devices are connected.
- Physical topology describes actual connections; logical topology describes data flow.
- Star Topology is the most common choice for LANs.
- Mesh Topology provides the highest redundancy.
- Tree and Hybrid Topologies dominate enterprise and cloud environments.

---

## What's Next?

**[OSI Model](osi-model.md)**
