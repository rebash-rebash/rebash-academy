---
title: "Routing Issues"
description: "Learn how to diagnose routing issues — missing routes, loops, asymmetric routing, route tables, and troubleshooting in cloud and Kubernetes."
difficulty: advanced
estimated_time: "220 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 12 · Network Troubleshooting"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - troubleshooting
  - routing
  - traceroute
  - rebash-networking-mastery
comments: false
status: ready
---

# Routing Issues — Diagnosing and Resolving Network Routing Problems

> **Routing Issues** occur when network devices cannot correctly determine the path that packets should take to reach their destination. These problems can result in **unreachable hosts, packet loss, high latency, routing loops, asymmetric routing, intermittent connectivity, and application failures**. Troubleshooting routing requires understanding **routing tables, static routes, dynamic routing protocols, default gateways, route selection, and packet forwarding**. Every Network Engineer, Linux Administrator, DevOps Engineer, SRE, Cloud Architect, and Kubernetes Administrator should be proficient in diagnosing routing issues.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 12: Network Troubleshooting → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Advanced</div>

<div markdown>**Reading Time:** 220 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Network Troubleshooting</div>

<div markdown>**Lesson:** 6 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand routing failures
- Diagnose missing routes
- Identify routing loops
- Troubleshoot asymmetric routing
- Analyze routing tables
- Verify dynamic routing protocols
- Troubleshoot routing in cloud and Kubernetes environments

---

# Prerequisites

Complete:

- IPv4
- Routing Fundamentals
- Static Routing
- Dynamic Routing
- [Ping](ping.md)
- [traceroute](traceroute-troubleshooting.md)

Basic understanding of:

- Routers
- Routing Tables
- Default Gateway

---

# Why Do Routing Issues Occur?

Imagine users report:

```text
Server

Cannot

Be

Reached
```

Ping fails.

DNS works.

The server is online.

Possible causes:

- Missing Route
- Wrong Gateway
- Routing Loop
- Incorrect Route Advertisement
- Firewall
- Asymmetric Routing

---

# What is Routing?

Routing is:

```text
The

Process

Of

Forwarding

Packets

Between

Networks
```

Routers examine the destination IP address and choose the best path.

---

# Normal Packet Flow

```text
Client

↓

Gateway

↓

Router

↓

Router

↓

Server
```

Every router forwards the packet based on its routing table.

---

# Routing Decision Process

For every incoming packet:

```text
Destination IP

↓

Routing Table Lookup

↓

Best Route

↓

Forward Packet
```

If no matching route exists:

```text
Packet

Dropped
```

---

# Routing Table

Every router maintains a routing table.

Example:

```text
Destination

↓

Next Hop

↓

Interface
```

Example entry:

```text
10.0.0.0/24

↓

192.168.1.1

↓

eth0
```

---

# View Routing Table

Linux:

```bash
ip route
```

Older command:

```bash
route -n
```

Windows:

```powershell
route print
```

---

# Default Route

When no specific route matches:

```text
0.0.0.0/0

↓

Default Gateway
```

Example:

```bash
ip route
```

Output:

```text
default via 192.168.1.1
```

---

# Missing Route

Example:

```text
Client

↓

Router

↓

Unknown Network
```

↓

```text
No Route

↓

Packet Dropped
```

Symptoms:

- Destination Unreachable
- Timeouts

---

# Wrong Default Gateway

Example:

```text
Client

↓

Incorrect Gateway

↓

Packet Lost
```

The packet never reaches the intended network.

Verify:

```bash
ip route
```

---

# Routing Loop

Example:

```text
Router A

↓

Router B

↓

Router A

↓

Router B
```

Packets circulate until:

```text
TTL

Expires
```

Symptoms:

- High Latency
- Packet Loss
- ICMP Time Exceeded

---

# Detecting Routing Loops

Run:

```bash
traceroute destination
```

Repeated routers indicate a routing loop.

Example:

```text
A

↓

B

↓

A

↓

B
```

---

# Asymmetric Routing

Forward path:

```text
Client

↓

Router A

↓

Server
```

Return path:

```text
Server

↓

Router B

↓

Client
```

Different paths can cause:

- Firewall Problems
- Session Failures
- Load Balancer Issues

---

# Route Advertisement Problems

Dynamic routing protocols advertise routes.

Possible issues:

- Missing Advertisement
- Incorrect Network
- Route Filtering
- Authentication Failure

Affected protocols:

- Open Shortest Path First (OSPF)
- Enhanced Interior Gateway Routing Protocol (EIGRP)
- Border Gateway Protocol (BGP)

---

# Static Route Problems

Example:

```bash
ip route add 10.0.0.0/24 via 192.168.1.10
```

Incorrect next-hop:

```text
Packets

Lost
```

Always verify:

- Destination Network
- Next Hop
- Interface

---

# Longest Prefix Match

Routers always choose:

```text
Most

Specific

Route
```

Example:

```text
10.0.0.0/8
```

and

```text
10.1.1.0/24
```

Destination:

```text
10.1.1.50
```

The router selects:

```text
10.1.1.0/24
```

because it is the most specific match.

---

# Dynamic Routing Issues

Possible causes:

- Neighbor Down
- Authentication Failure
- Route Flapping
- Incorrect Metrics
- Area Misconfiguration
- Network Statement Errors

Always verify routing protocol health.

---

# Cloud Routing Issues

Cloud platforms use virtual route tables.

Examples:

- AWS Route Tables
- Azure Route Tables
- Google Cloud Routes

Verify:

- Subnet Association
- Internet Gateway
- NAT Gateway
- VPN Gateway
- Peering Routes

---

# Kubernetes Routing Issues

Verify:

- Container Network Interface (CNI)
- Pod CIDR
- Node CIDR
- Service CIDR
- kube-proxy
- Network Policies

Common commands:

```bash
kubectl get nodes
```

```bash
kubectl get pods -o wide
```

---

# Enterprise Routing Workflow

```text
Client

↓

Gateway

↓

Core Router

↓

Distribution Router

↓

Internet

↓

Server
```

Each hop must have a valid route to the destination.

---

# Troubleshooting Workflow

Step 1

Verify connectivity.

```bash
ping
```

---

Step 2

View the path.

```bash
traceroute
```

---

Step 3

Check routing table.

```bash
ip route
```

---

Step 4

Capture traffic.

```bash
tcpdump
```

---

Step 5

Analyze packets.

```text
Wireshark
```

---

# Common Routing Problems

| Problem | Symptom |
|----------|----------|
| Missing Route | Destination Unreachable |
| Wrong Gateway | No Connectivity |
| Routing Loop | TTL Expired |
| Asymmetric Routing | Session Problems |
| Incorrect Route Metric | Suboptimal Path |
| Route Flapping | Intermittent Connectivity |

---

# CLI Examples

View routing table.

```bash
ip route
```

Show interface addresses.

```bash
ip addr
```

Trace packet path.

```bash
traceroute example.com
```

Capture routing traffic.

```bash
sudo tcpdump icmp
```

Test gateway.

```bash
ping 192.168.1.1
```

---

# Hands-on Lab

## Task 1

Display the routing table.

```bash
ip route
```

---

## Task 2

Identify:

- Default Gateway
- Local Routes
- Static Routes

---

## Task 3

Run:

```bash
traceroute google.com
```

Identify each router.

---

## Task 4

Remove a static route in a lab environment.

Observe:

- Packet Loss
- Connectivity Failure

Restore the route and verify recovery.

---

## Task 5

Capture packets while testing routing.

```bash
sudo tcpdump icmp
```

---

## Task 6

Compare routing tables on two Linux servers.

Identify missing routes.

---

## Task 7

Verify routing in a Kubernetes cluster by checking Pod-to-Pod communication across nodes.

---

## Task 8

Draw the packet path:

```text
Client

↓

Gateway

↓

Core Router

↓

ISP

↓

Internet

↓

Cloud Router

↓

Server
```

Explain how each router selects the next hop using the routing table.

---

# Production Troubleshooting

Problem:

```text
Server

Unreachable
```

Check:

- Gateway
- Routing Table
- Static Routes
- Dynamic Routes
- Route Advertisements
- Firewall
- Network Address Translation (NAT)
- Packet Capture

Workflow:

```text
Ping

↓

Traceroute

↓

Routing Table

↓

Packet Capture

↓

Root Cause
```

---

# Static Routing vs Dynamic Routing

| Static Routing | Dynamic Routing |
|----------------|-----------------|
| Manual Configuration | Automatic Learning |
| Simple Networks | Large Networks |
| Low Overhead | Protocol Overhead |
| Manual Updates | Automatic Updates |
| Limited Scalability | Highly Scalable |

---

# Routing Issues vs DNS Issues

| Routing Issue | DNS Issue |
|---------------|-----------|
| IP Unreachable | Hostname Fails |
| Ping by IP Fails | Ping by IP Works |
| traceroute Shows Failure | DNS Query Fails |
| Route Table Problem | Resolver Problem |
| Network Layer | Application Support Layer |

---

# Common Mistakes

❌ Assuming every connectivity problem is a routing issue.

✅ Verify DNS and firewall configuration first.

---

❌ Ignoring the default route.

✅ Confirm the default gateway is correct.

---

❌ Overlooking asymmetric routing.

✅ Verify both forward and return paths.

---

❌ Trusting traceroute alone.

✅ Validate routing tables and packet captures.

---

❌ Forgetting longest prefix match.

✅ Check for more specific routes overriding expected paths.

---

# Best Practices

- Verify the routing table before changing routes.
- Check the default gateway first.
- Use traceroute to identify routing failures.
- Document static routes.
- Monitor routing protocol neighbors.
- Validate cloud route tables after infrastructure changes.
- Capture packets when routing behavior is unclear.
- Test both forward and return paths.

---

# Interview Questions

## Beginner

1. What is routing?
2. What is a routing table?
3. What is a default route?
4. What is a routing loop?

---

## Intermediate

1. Explain longest prefix matching.
2. What is asymmetric routing?
3. How do you troubleshoot missing routes?
4. Compare static and dynamic routing.

---

## Architect Level

1. Design a routing troubleshooting workflow for an enterprise network.
2. Explain how routing loops occur and how to identify them.
3. How would you troubleshoot intermittent routing problems across multiple cloud regions?

---

# Summary

In this lesson, you learned:

- Routing Issues
- Routing Tables
- Default Routes
- Missing Routes
- Routing Loops
- Asymmetric Routing
- Longest Prefix Match
- Static and Dynamic Routing
- Cloud Routing
- Kubernetes Routing

Routing is the foundation of IP networking. When routing problems occur, applications may experience connectivity failures, packet loss, or high latency even though the underlying hosts are healthy. By systematically verifying routing tables, gateways, traceroute output, and packet captures, engineers can efficiently isolate and resolve routing issues across enterprise networks, cloud platforms, and Kubernetes clusters.

---

## Key Takeaways

- Every router forwards packets using its **routing table**.
- The **default route** is used when no more specific route exists.
- **Longest prefix match** determines the preferred route.
- Common routing problems include **missing routes**, **routing loops**, and **asymmetric routing**.
- Use **Ping**, **traceroute**, **ip route**, **tcpdump**, and **Wireshark** together for comprehensive troubleshooting.
- Cloud and Kubernetes environments rely on correct routing just as traditional networks do.

---

## What's Next?

**[MTU Problems](mtu-problems.md)**

In the next lesson, you'll learn about **MTU Problems**.

You'll explore:

- What MTU is
- Maximum Transmission Unit
- IP Fragmentation
- Path MTU Discovery (PMTUD)
- Jumbo Frames
- MTU Mismatch
- Production MTU Troubleshooting

By the end of the lesson, you'll understand how MTU affects network performance and how to diagnose fragmentation, black-hole connections, and MTU mismatches in enterprise, cloud, and Kubernetes environments.
