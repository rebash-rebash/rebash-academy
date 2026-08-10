---
title: "Linux traceroute Command"
description: "Learn Linux traceroute — discover hop-by-hop network paths, measure latency, understand TTL, and troubleshoot routing in enterprise and cloud environments."
difficulty: beginner
estimated_time: "130 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 9 · Linux Networking"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - linux
  - traceroute
  - routing
  - rebash-networking-mastery
comments: false
status: ready
---

# Linux `traceroute` Command — Discovering Network Paths and Troubleshooting Routing

> **`traceroute`** is a Linux networking utility used to discover the **path that network packets take from a source to a destination**. It identifies every router (hop) along the route and measures the time required to reach each hop. `traceroute` is one of the most valuable tools for diagnosing **routing issues, network latency, packet loss, ISP problems, cloud connectivity, VPN routing, and Internet reachability**. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should master the `traceroute` command.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 9: Linux Networking → Lesson 5</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 130 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Linux Networking</div>

<div markdown>**Lesson:** 5 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand `traceroute`
- Learn how packet forwarding works
- Understand Time To Live (TTL)
- Discover hop-by-hop network paths
- Measure network latency
- Troubleshoot routing problems
- Analyse enterprise and cloud connectivity

---

# Prerequisites

Complete:

- [Linux `ip` Command](linux-networking-toolkit.md)
- [Linux `ss` Command](ss.md)
- [Linux `netstat` Command](netstat.md)
- [Linux `tcpdump` Command](packet-analysis-tcpdump-wireshark.md)

Basic understanding of:

- IP Routing
- Routers
- Internet Control Message Protocol (ICMP)
- TTL

---

# Why Learn `traceroute`?

Imagine users report:

- Website Not Reachable
- VPN Not Working
- High Network Latency
- Cloud Connectivity Problems
- Slow Internet Access

Ping only tells you:

```text
Reachable

OR

Not Reachable
```

It does **not** tell you:

- Where packets stop
- Which router is slow
- Which network is failing

That's where:

```bash
traceroute
```

becomes invaluable.

---

# What is `traceroute`?

`traceroute` discovers:

```text
Every Router

Between

Source

↓

Destination
```

It also measures:

- Hop Count
- Round Trip Time (RTT)
- Network Delay

---

# How Does `traceroute` Work?

`traceroute` relies on:

```text
Time To Live (TTL)
```

Each packet contains a TTL value.

Every router:

```text
TTL - 1
```

When TTL reaches:

```text
0
```

The router discards the packet and returns an:

```text
ICMP Time Exceeded
```

message.

By gradually increasing the TTL value, `traceroute` discovers every hop along the path.

---

# Packet Flow

Example:

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

`traceroute` identifies each router individually.

---

# Basic Syntax

```bash
traceroute destination
```

Example:

```bash
traceroute google.com
```

---

# Install traceroute

Ubuntu/Debian

```bash
sudo apt install traceroute
```

RHEL/CentOS

```bash
sudo dnf install traceroute
```

---

# Trace by Hostname

```bash
traceroute google.com
```

Example output:

```text
1 192.168.1.1

2 ISP Router

3 Regional Router

4 Google
```

---

# Trace by IP Address

```bash
traceroute 8.8.8.8
```

---

# Numeric Output

Disable Domain Name System (DNS) lookups.

```bash
traceroute -n 8.8.8.8
```

Benefits:

- Faster Execution
- Easier Troubleshooting

---

# Limit Maximum Hops

```bash
traceroute -m 10 google.com
```

Limits tracing to ten hops.

---

# Change Initial TTL

```bash
traceroute -f 5 google.com
```

Starts tracing from hop 5.

Useful for troubleshooting long network paths.

---

# Change Number of Probes

Default:

```text
3 Probes

Per Hop
```

Example:

```bash
traceroute -q 5 google.com
```

Sends five probes per hop.

---

# Set Wait Time

```bash
traceroute -w 2 google.com
```

Waits two seconds for each reply.

---

# Use ICMP Instead of UDP

Some Linux implementations default to User Datagram Protocol (UDP) probes.

To use ICMP:

```bash
traceroute -I google.com
```

Useful when UDP traffic is filtered.

---

# Use TCP Probes

Some firewalls block UDP and ICMP.

Use Transmission Control Protocol (TCP) probes:

```bash
traceroute -T google.com
```

This can provide more accurate results in restrictive environments.

---

# Understanding Output

Example:

```text
1 192.168.1.1 1 ms

2 10.1.0.1 4 ms

3 203.0.113.1 10 ms

4 8.8.8.8 15 ms
```

Columns:

- Hop Number
- Router Address
- Response Time

---

# What Does `* * *` Mean?

Example:

```text
7 * * *
```

Possible reasons:

- Firewall Blocking ICMP
- Router Configured Not to Respond
- Packet Loss
- Network Congestion

It does **not always** indicate that traffic cannot continue beyond that hop.

---

# Measuring Latency

Example:

```text
Hop 1

1 ms
```

```text
Hop 5

120 ms
```

Large increases in latency may indicate:

- Congestion
- Long-Distance Links
- Overloaded Routers

---

# Routing Problem Example

```text
Client

↓

Router 1

↓

Router 2

↓

X
```

Packets stop at:

```text
Router 2
```

`traceroute` helps identify where the path fails.

---

# Enterprise Example

User cannot reach:

```text
Internal Application
```

Administrator runs:

```bash
traceroute app.company.local
```

Finds:

```text
Traffic Stops

At

Firewall
```

Problem identified quickly.

---

# VPN Troubleshooting

```text
Laptop

↓

VPN Gateway

↓

Corporate Router

↓

Application
```

Use:

```bash
traceroute
```

to verify whether traffic enters the VPN tunnel correctly.

---

# Cloud Perspective

Cloud engineers use `traceroute` to troubleshoot:

- Hybrid Connectivity
- VPN
- Cloud Interconnect
- Load Balancers
- Internet Gateways
- Regional Connectivity

---

# Kubernetes Perspective

Use `traceroute` from:

- Worker Nodes
- Bastion Hosts
- Pods (where available)

to verify:

- Service Reachability
- External Connectivity
- Ingress Paths
- Hybrid Cloud Networking

Some minimal container images may not include `traceroute` by default.

---

# Linux Perspective

Trace a destination.

```bash
traceroute google.com
```

Numeric output.

```bash
traceroute -n 8.8.8.8
```

Use ICMP.

```bash
traceroute -I google.com
```

Use TCP.

```bash
traceroute -T google.com
```

---

# traceroute Workflow

```text
Source

↓

Hop 1

↓

Hop 2

↓

Hop 3

↓

Destination
```

Each hop returns its response time.

---

# Common traceroute Commands

| Command | Purpose |
|----------|----------|
| `traceroute host` | Trace route to host |
| `traceroute IP` | Trace route to IP address |
| `traceroute -n` | Numeric output |
| `traceroute -I` | Use ICMP probes |
| `traceroute -T` | Use TCP probes |
| `traceroute -m` | Maximum hops |
| `traceroute -q` | Number of probes |
| `traceroute -w` | Wait timeout |

---

# Hands-on Lab

## Task 1

Trace route to Google DNS.

```bash
traceroute 8.8.8.8
```

---

## Task 2

Trace using a hostname.

```bash
traceroute google.com
```

---

## Task 3

Disable DNS lookups.

```bash
traceroute -n 8.8.8.8
```

---

## Task 4

Trace using ICMP.

```bash
traceroute -I google.com
```

---

## Task 5

Trace using TCP.

```bash
traceroute -T google.com
```

---

## Task 6

Limit to 10 hops.

```bash
traceroute -m 10 google.com
```

---

## Task 7

Trace the route to a cloud virtual machine or internal server and compare the path with an Internet destination.

---

## Task 8

Create a troubleshooting checklist using:

- `ping`
- `traceroute`
- `ip route`
- `ss`
- `tcpdump`

---

# Production Troubleshooting

Problem:

```text
Application

Unreachable
```

Step 1

```bash
ping Destination
```

↓

Reachable?

↓

No

↓

Run:

```bash
traceroute Destination
```

↓

Identify:

- Last Reachable Router
- High Latency Hop
- Routing Loop
- Packet Drop

↓

Investigate:

- Router
- Firewall
- ISP
- VPN

---

# traceroute vs ping

| ping | traceroute |
|------|------------|
| Tests Reachability | Discovers Network Path |
| Measures RTT | Measures RTT Per Hop |
| No Routing Information | Displays Every Hop |
| Simple Connectivity Test | Advanced Routing Diagnostics |

---

# Common Mistakes

❌ Assuming `* * *` always indicates failure.

✅ Some routers intentionally ignore traceroute probes.

---

❌ Forgetting DNS resolution delays.

✅ Use `-n` for numeric output.

---

❌ Using only UDP probes.

✅ Try ICMP or TCP if traffic is filtered.

---

❌ Ignoring latency spikes.

✅ Compare response times across hops.

---

❌ Relying only on traceroute.

✅ Combine with `ping`, `tcpdump`, and routing information.

---

# Best Practices

- Use numeric output during troubleshooting.
- Compare traceroute results from multiple locations.
- Combine traceroute with `ping` and `tcpdump`.
- Investigate sudden latency increases.
- Document normal routing paths for production systems.
- Verify firewall policies when traceroute fails.
- Test both IPv4 and IPv6 connectivity where applicable.

---

# Interview Questions

## Beginner

1. What is `traceroute`?
2. What is TTL?
3. How does `traceroute` discover routers?
4. What does `* * *` mean in traceroute output?

---

## Intermediate

1. Compare `ping` and `traceroute`.
2. Why would you use TCP probes instead of UDP?
3. How do you troubleshoot high latency using `traceroute`?
4. Why does each hop return an ICMP Time Exceeded message?

---

## Architect Level

1. Explain how you would troubleshoot a hybrid cloud routing problem using `traceroute`.
2. Design a network troubleshooting workflow using `ping`, `traceroute`, and `tcpdump`.
3. How would you investigate intermittent routing failures between two data centres?

---

# Summary

In this lesson, you learned:

- The `traceroute` command
- Time To Live (TTL)
- Hop-by-Hop Path Discovery
- Network Latency Analysis
- Routing Troubleshooting
- ICMP Responses
- Enterprise Connectivity Diagnostics

`traceroute` is one of the most valuable network troubleshooting tools available on Linux. By revealing every hop between a source and destination, it helps engineers identify routing problems, measure latency, locate network bottlenecks, and troubleshoot connectivity across enterprise, cloud, VPN, and Internet environments.

---

## Key Takeaways

- `traceroute` discovers the **path packets take** across a network.
- It works by increasing the **TTL** value of probe packets.
- Each router returns an **ICMP Time Exceeded** message when the TTL expires.
- Use **`-n`** for faster numeric output.
- Use **`-I`** for ICMP probes and **`-T`** for TCP probes when needed.
- `traceroute` complements `ping` by showing **where** connectivity problems occur.

---

## What's Next?

**[dig (Domain Information Groper)](dig.md)**

In the next lesson, you'll learn about **`dig` (Domain Information Groper)**.

You'll explore:

- What `dig` is
- DNS Queries
- DNS Record Types
- Authoritative vs Recursive DNS
- Reverse DNS Lookups
- DNS Troubleshooting
- Production DNS Diagnostics

By the end of the lesson, you'll be able to query DNS servers, inspect DNS records, troubleshoot name resolution issues, and diagnose DNS-related problems in enterprise, cloud, and Kubernetes environments.
