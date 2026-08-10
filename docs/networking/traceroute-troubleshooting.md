---
title: "traceroute"
description: "Learn traceroute for network path discovery — TTL-based hops, latency per hop, routing loops, packet loss, and troubleshooting in Linux, cloud, and Kubernetes."
difficulty: intermediate
estimated_time: "190 min"
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
  - traceroute
  - icmp
  - rebash-networking-mastery
comments: false
status: ready
---

# traceroute — Discovering the Network Path Between Two Systems

> **traceroute** is a network diagnostic tool used to identify the **path (route)** that packets take from a source system to a destination. Unlike Ping, which only confirms whether a destination is reachable, traceroute reveals **every intermediate router (hop)** along the path and measures the time taken to reach each hop. It is one of the most important tools for diagnosing **routing problems, latency issues, packet loss, routing loops, ISP problems, and cloud networking issues**. Every Network Engineer, Linux Administrator, DevOps Engineer, SRE, Cloud Engineer, and Kubernetes Administrator should understand traceroute.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 12: Network Troubleshooting → Lesson 2</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 190 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Network Troubleshooting</div>

<div markdown>**Lesson:** 2 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand how traceroute works
- Learn TTL-based path discovery
- Identify network hops
- Detect routing problems
- Measure latency at each hop
- Troubleshoot packet loss and routing loops
- Use traceroute in Linux, cloud, and Kubernetes environments

---

# Prerequisites

Complete:

- [Ping](ping.md)
- TCP/IP
- IPv4
- Routing
- Internet Control Message Protocol (ICMP)

Basic understanding of:

- Routers
- Time To Live (TTL)
- IP Packets

---

# Why Do We Need traceroute?

Imagine users report:

```text
Application

Is

Very

Slow
```

Ping shows:

```text
Host Reachable
```

But:

- Which router is slow?
- Where is packet loss occurring?
- Is traffic taking the wrong path?

The answer is:

```bash
traceroute
```

---

# What is traceroute?

Traceroute is:

```text
A

Network

Path

Discovery

Tool
```

It identifies:

- Every Router (Hop)
- Network Delay
- Routing Path
- Routing Failures

between the source and destination.

---

# How traceroute Works

Traceroute uses:

```text
TTL

(Time To Live)
```

Each probe starts with a small TTL value.

Example:

```text
TTL = 1
```

The first router decreases TTL to:

```text
0
```

The router discards the packet and returns an:

```text
ICMP

Time Exceeded
```

message.

Traceroute records the router's address.

---

# TTL Discovery Process

```text
TTL = 1

↓

Router 1

↓

ICMP Reply
```

Then:

```text
TTL = 2

↓

Router 1

↓

Router 2

↓

ICMP Reply
```

This continues until the destination is reached.

---

# Packet Flow

```text
Client

↓

Router 1

↓

Router 2

↓

Router 3

↓

Destination
```

Traceroute displays every router along this path.

---

# Sample Output

```text
1 192.168.1.1 1 ms
2 10.10.0.1 5 ms
3 203.0.113.5 14 ms
4 8.8.8.8 18 ms
```

Meaning:

- Hop 1 → Local Gateway
- Hop 2 → ISP Router
- Hop 3 → Internet Backbone
- Hop 4 → Destination

---

# Understanding Hops

Each line represents:

```text
One

Router
```

that forwards the packet.

Example:

```text
Hop 1

↓

Gateway
```

```text
Hop 2

↓

ISP
```

```text
Hop 3

↓

Cloud Provider
```

```text
Hop 4

↓

Destination
```

---

# Response Times

Traceroute usually sends three probes per hop.

Example:

```text
2 ms

3 ms

2 ms
```

These values represent the round-trip time for each probe.

High values may indicate:

- Congestion
- Slow Router
- Long-Distance Links

---

# Asterisk (*) Responses

Example:

```text
5  * * *
```

Possible reasons:

- ICMP Filtering
- Firewall
- Router Drops Probes
- Rate Limiting

Asterisks do **not** always indicate a network failure.

---

# Routing Loops

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

Traceroute repeatedly displays the same routers.

This indicates a routing loop.

---

# High Latency Detection

Example:

```text
1 2 ms

2 3 ms

3 150 ms

4 151 ms
```

Latency increases significantly at Hop 3.

This suggests the delay begins there.

---

# Packet Loss Detection

If several hops display:

```text
* * *
```

or inconsistent response times:

Possible causes:

- Router Overload
- Packet Filtering
- Network Congestion
- Faulty Links

Confirm with additional tools such as Ping or My Traceroute (MTR).

---

# Linux traceroute

Install if necessary:

```bash
sudo apt install traceroute
```

Run:

```bash
traceroute google.com
```

---

# Windows tracert

Windows command:

```powershell
tracert google.com
```

The functionality is similar to Linux traceroute.

---

# macOS traceroute

```bash
traceroute google.com
```

Available by default.

---

# TCP vs UDP vs ICMP

Different implementations use different probe types.

Linux (default):

```text
UDP
```

Windows:

```text
ICMP
```

Some tools support:

```text
TCP
```

TCP probes are useful when ICMP or UDP is filtered.

---

# Kubernetes Perspective

Run traceroute inside a Pod.

```bash
kubectl exec -it pod-name -- traceroute service-name
```

Useful for diagnosing:

- Pod Connectivity
- Service Reachability
- Network Policies
- Container Network Interface (CNI) Issues

---

# Cloud Perspective

Traceroute helps diagnose:

- AWS VPC Routing
- Azure VNet Routing
- GCP VPC Routing
- VPN Connectivity
- Hybrid Networking

---

# Enterprise Troubleshooting Workflow

```text
Ping

↓

traceroute

↓

tcpdump

↓

Wireshark
```

Each tool provides additional detail.

---

# Common traceroute Responses

| Response | Meaning |
|-----------|----------|
| Router IP | Hop Reached |
| * * * | No Response |
| Destination Reached | Successful Trace |
| Time Exceeded | TTL Expired |
| Network Unreachable | Routing Failure |

---

# CLI Examples

Trace a hostname.

```bash
traceroute google.com
```

Trace an IP address.

```bash
traceroute 8.8.8.8
```

Use ICMP probes (Linux).

```bash
traceroute -I google.com
```

Use TCP probes.

```bash
traceroute -T google.com
```

Limit maximum hops.

```bash
traceroute -m 20 google.com
```

---

# Hands-on Lab

## Task 1

Run traceroute to a public website.

```bash
traceroute google.com
```

---

## Task 2

Run traceroute to:

```bash
8.8.8.8
```

Compare the path with the hostname trace.

---

## Task 3

Identify:

- Local Gateway
- ISP Router
- Cloud Provider
- Destination

---

## Task 4

Measure latency for every hop.

Identify the slowest hop.

---

## Task 5

Run traceroute from:

- Local Machine
- Cloud VM
- Kubernetes Pod

Compare the paths.

---

## Task 6

Use TCP-based traceroute where ICMP or UDP probes are blocked.

---

## Task 7

Investigate a simulated routing loop and explain how traceroute reveals it.

---

## Task 8

Draw the complete packet journey:

```text
Laptop

↓

Switch

↓

Router

↓

ISP

↓

Internet

↓

Cloud

↓

Server
```

Explain how TTL changes at every router.

---

# Production Troubleshooting

Problem:

```text
Application

Slow
```

Check:

- Ping
- traceroute
- DNS
- Routing
- Firewall
- Cloud Routes
- VPN
- ISP

Workflow:

```text
Ping

↓

Traceroute

↓

Find Slow Hop

↓

Investigate Router

↓

Resolve
```

---

# Ping vs traceroute

| Ping | traceroute |
|------|------------|
| Reachability | Path Discovery |
| Uses ICMP | Uses TTL-Based Probes |
| Measures End-to-End RTT | Measures RTT Per Hop |
| No Routing Information | Displays Every Hop |
| Basic Connectivity | Routing Diagnostics |

---

# traceroute vs MTR

| traceroute | MTR |
|-------------|-----|
| One-Time Trace | Continuous Monitoring |
| Static Snapshot | Live Statistics |
| Basic Latency | Latency + Packet Loss |
| Simple | More Comprehensive |

---

# Common Mistakes

❌ Assuming `* * *` always means failure.

✅ Consider ICMP filtering or rate limiting.

---

❌ Investigating only the destination.

✅ Analyze latency and behavior at every hop.

---

❌ Ignoring asymmetric routing.

✅ Remember that return traffic may follow a different path.

---

❌ Using only traceroute.

✅ Combine with Ping, tcpdump, and application logs.

---

❌ Assuming the slowest responding router is the root cause.

✅ Check whether subsequent hops also show increased latency.

---

# Best Practices

- Run Ping before traceroute.
- Compare traces from multiple locations.
- Record latency for each hop.
- Use TCP probes if ICMP is blocked.
- Compare successful and failed traces.
- Use traceroute together with tcpdump and Wireshark.
- Validate routing after network changes.
- Document normal network paths for production systems.

---

# Interview Questions

## Beginner

1. What is traceroute?
2. How does traceroute work?
3. What is TTL?
4. What does a hop represent?

---

## Intermediate

1. Why does traceroute use increasing TTL values?
2. What does `* * *` mean in traceroute output?
3. Compare Ping and traceroute.
4. How do you identify the source of network latency?

---

## Architect Level

1. Design a production troubleshooting workflow using Ping and traceroute.
2. Explain how traceroute identifies routing loops.
3. How would you troubleshoot intermittent latency between two cloud regions?

---

# Summary

In this lesson, you learned:

- traceroute
- TTL-Based Path Discovery
- Network Hops
- Routing Analysis
- Latency Measurement
- Packet Loss Detection
- Routing Loops
- ICMP Time Exceeded Messages
- Cloud and Kubernetes Troubleshooting

Traceroute is an essential network troubleshooting tool that reveals the complete path packets take across a network. By identifying every intermediate hop and measuring latency at each stage, it helps engineers isolate routing problems, locate delays, detect loops, and understand how traffic flows through complex enterprise, cloud, and Kubernetes environments.

---

## Key Takeaways

- **traceroute** discovers the path packets take to a destination.
- It works by increasing the **TTL** value for successive probes.
- Each router returns an **ICMP Time Exceeded** message when TTL reaches zero.
- traceroute helps identify **routing issues**, **latency**, **packet loss**, and **routing loops**.
- Different operating systems may use **UDP**, **ICMP**, or **TCP** probes.
- Combine traceroute with **Ping**, **tcpdump**, and **Wireshark** for comprehensive troubleshooting.

---

## What's Next?

**[tcpdump](tcpdump-troubleshooting.md)**

In the next lesson, you'll learn about **tcpdump**.

You'll explore:

- Packet Capture Fundamentals
- Network Interface Monitoring
- Capture Filters
- Protocol Analysis
- TCP Handshake Inspection
- DNS and HTTP Packet Analysis
- Production Packet Troubleshooting

By the end of the lesson, you'll be able to capture and analyse live network traffic directly from Linux systems, cloud instances, and Kubernetes nodes to diagnose real-world networking issues.
