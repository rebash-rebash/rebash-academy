---
title: "traceroute — Discovering the Network Path to a Destination"
description: "Use traceroute to map network hops — understand TTL, interpret latency per hop, apply ICMP/TCP options, and troubleshoot routing and path delays on Linux."
difficulty: intermediate
estimated_time: "60 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 8 · Networking"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - networking
  - traceroute
  - ttl
  - troubleshooting
  - rebash-linux-mastery
comments: false
status: ready
---

# traceroute — Discovering the Network Path to a Destination

> **traceroute** is a Linux networking tool that identifies the path packets take from a source system to a destination. It displays every intermediate router (hop) along the route, helping administrators locate network delays, routing problems, and connectivity failures. It is one of the most valuable tools for Linux administrators, DevOps engineers, Cloud Architects, Network Engineers, and Site Reliability Engineers (SREs).

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 8: Networking → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 60 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Networking</div>

<div markdown>**Lesson:** 6 of 13</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand how `traceroute` works
- Discover network paths
- Identify routing issues
- Measure network latency
- Interpret traceroute output
- Use common traceroute options
- Troubleshoot production network problems

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management
- Module 5 – Users and Groups
- Module 6 – Process Management
- Module 7 – Package Management
- Module 8 Lessons 1–5

---

# Why Learn traceroute?

Imagine:

- A website loads slowly.
- SSH connections time out.
- Cloud servers cannot communicate.
- A Kubernetes cluster has network latency.

`ping` only tells you whether a host is reachable.

`traceroute` tells you:

> **Where the packets are traveling and where they stop or slow down.**

---

# What is traceroute?

`traceroute` is a diagnostic tool that displays every network device (hop) between your computer and the destination.

It helps answer:

- Which routers are involved?
- Where is the delay?
- Which hop is unreachable?

---

# How traceroute Works

`traceroute` sends packets with gradually increasing **TTL (Time To Live)** values.

Example:

```text
TTL = 1

↓

Router 1 replies
```

```text
TTL = 2

↓

Router 2 replies
```

```text
TTL = 3

↓

Router 3 replies
```

This continues until the destination is reached.

---

# What is TTL?

TTL stands for:

```text
Time To Live
```

It limits how many routers (hops) a packet can pass through.

Each router decreases the TTL by **1**.

When TTL reaches **0**:

- The router discards the packet.
- It sends an ICMP "Time Exceeded" message back.

`traceroute` uses these replies to identify each hop.

---

# Basic traceroute Command

Trace the route to Google.

```bash
traceroute google.com
```

Example output:

```text
1 192.168.1.1

2 10.20.0.1

3 203.0.113.1

4 google.com
```

Each numbered line represents one network hop.

---

# Understanding the Output

Example:

```text
3 203.0.113.1 15.4 ms 16.2 ms 15.8 ms
```

Meaning:

| Field | Description |
|--------|-------------|
| `3` | Hop number |
| `203.0.113.1` | Router IP address |
| `15.4 ms` | First response time |
| `16.2 ms` | Second response time |
| `15.8 ms` | Third response time |

Multiple response times help identify latency variations.

---

# Install traceroute

Ubuntu/Debian:

```bash
sudo apt install traceroute
```

RHEL/Rocky/AlmaLinux:

```bash
sudo dnf install traceroute
```

---

# Trace Using an IP Address

```bash
traceroute 8.8.8.8
```

---

# Numeric Output Only

Avoid DNS lookups.

```bash
traceroute -n google.com
```

This is faster because hostnames are not resolved.

---

# Limit Maximum Hops

```bash
traceroute -m 10 google.com
```

Stops tracing after **10 hops**.

---

# Set Probe Count

Send two probes per hop.

```bash
traceroute -q 2 google.com
```

Default:

```text
3 probes
```

---

# Use ICMP Instead of UDP

Some firewalls block UDP-based traceroute.

Use ICMP:

```bash
traceroute -I google.com
```

---

# Use TCP Probes

Useful when ICMP or UDP traffic is filtered.

```bash
sudo traceroute -T google.com
```

---

# Common Commands

Basic trace.

```bash
traceroute google.com
```

Numeric output.

```bash
traceroute -n google.com
```

Limit hops.

```bash
traceroute -m 15 google.com
```

Use ICMP.

```bash
traceroute -I google.com
```

Use TCP.

```bash
sudo traceroute -T google.com
```

---

# Real Production Examples

Trace a Kubernetes API server.

```bash
traceroute api.example.com
```

Trace a cloud server.

```bash
traceroute 34.120.x.x
```

Trace a database server.

```bash
traceroute db.example.com
```

Trace Google DNS.

```bash
traceroute 8.8.8.8
```

---

# Production Perspective

`traceroute` is widely used for:

- Network troubleshooting
- Cloud networking
- Kubernetes clusters
- VPN diagnostics
- WAN connectivity
- Internet routing
- ISP troubleshooting
- Performance analysis

It helps identify the location of routing failures or excessive latency.

---

# Hands-on Lab

## Task 1

Trace the route to Google.

```bash
traceroute google.com
```

---

## Task 2

Trace to Google's DNS server.

```bash
traceroute 8.8.8.8
```

---

## Task 3

Disable DNS resolution.

```bash
traceroute -n google.com
```

---

## Task 4

Limit the trace to 10 hops.

```bash
traceroute -m 10 google.com
```

---

## Task 5

Use ICMP probes.

```bash
traceroute -I google.com
```

---

## Task 6

Use TCP probes.

```bash
sudo traceroute -T google.com
```

---

## Task 7

Compare routes to two different websites.

```bash
traceroute google.com

traceroute cloudflare.com
```

---

## Task 8

Observe:

- Number of hops
- Latency at each hop
- Final destination

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `traceroute host` | Display network path | Connectivity troubleshooting |
| `traceroute -n` | Skip DNS resolution | Faster diagnostics |
| `traceroute -m` | Limit maximum hops | Controlled tracing |
| `traceroute -q` | Set probes per hop | Latency analysis |
| `traceroute -I` | Use ICMP | Firewall testing |
| `traceroute -T` | Use TCP probes | Production troubleshooting |

---

# Common traceroute Symbols

| Symbol | Meaning |
|---------|---------|
| `*` | No response received |
| `ms` | Response time in milliseconds |
| Hop Number | Router sequence in the path |

Example:

```text
5 * * *
```

This may indicate:

- Firewall filtering
- Router not responding to traceroute probes
- Network congestion

It does **not** necessarily mean traffic cannot pass through that router.

---

# traceroute vs ping

| Feature | ping | traceroute |
|----------|------|------------|
| Tests Connectivity | ✅ | ✅ |
| Measures Latency | ✅ | ✅ |
| Shows Network Path | ❌ | ✅ |
| Displays Each Hop | ❌ | ✅ |
| Detects Routing Problems | Limited | Excellent |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    Users report that a web application hosted in the cloud is slow.

Investigation:

Verify connectivity.

```bash
ping app.example.com
```

Connectivity is successful.

Trace the network path.

```bash
traceroute app.example.com
```

Output:

```text
Hop 8

250 ms
```

All previous hops show latency below **20 ms**.

This indicates a significant delay beginning at hop 8.

The network team investigates the corresponding router and resolves the issue, restoring normal application performance.

---

# Best Practices

- Use `ping` first to verify basic connectivity.
- Use `traceroute` to locate routing or latency problems.
- Use `-n` for faster troubleshooting.
- Compare traces from multiple locations when diagnosing distributed systems.
- Remember that some routers intentionally ignore traceroute probes.
- Combine `traceroute` with tools such as `ping`, `ss`, and `curl` for comprehensive diagnostics.

---

# Common Mistakes

❌ Assuming `*` always means the network is broken.

✅ Verify `*` always means the network is broken instead of assuming it.

---

❌ Confusing latency at an intermediate hop with the destination's performance.

✅ Distinguish clearly between latency at an intermediate hop with the destination's performance.

---

❌ Ignoring firewall policies that block traceroute traffic.

✅ Always review firewall policies that block traceroute traffic.

---

❌ Using only one network diagnostic tool.

✅ Avoid using only one network diagnostic tool when a safer approach exists.

---

# Interview Questions
## Beginner

1. What is the purpose of `traceroute`?
2. What does TTL stand for?
3. What does each hop represent?
4. Which command traces the path to a destination?

---

## Intermediate

1. How does `traceroute` discover each router?
2. What does `* * *` indicate?
3. Why would you use `traceroute -n`?
4. What is the difference between `ping` and `traceroute`?

---

## Architect Level

1. How would you troubleshoot intermittent latency between two cloud regions?
2. Why might traceroute show high latency at one hop while the destination remains fast?
3. How would you diagnose routing issues in a hybrid cloud environment?

---

# Summary

In this lesson, you learned:

- How `traceroute` works
- TTL and hop discovery
- Reading traceroute output
- Measuring latency
- Identifying routing issues
- Common traceroute options
- Production troubleshooting

`traceroute` is an essential networking tool that reveals the path packets take across networks. By identifying each hop and measuring response times, it helps administrators diagnose routing problems, locate network bottlenecks, and troubleshoot connectivity issues in production environments.

---

## Key Takeaways

- `traceroute` displays the path packets take to reach a destination.
- It works by sending packets with increasing TTL values.
- Each router along the path is displayed as a hop.
- Use `-n` to skip DNS lookups and speed up troubleshooting.
- `*` responses do not always indicate a failure.
- Combine `traceroute` with other networking tools for effective diagnostics.

---

## What's Next?

**[ss (Socket Statistics) — Viewing Network Connections in Linux](ss.md)**

You'll explore:

- Viewing active network connections
- Checking listening ports
- Inspecting TCP and UDP sockets
- Filtering network connections
- Monitoring services
- Replacing the legacy `netstat` command
- Production troubleshooting techniques

The `ss` command is the modern and preferred tool for inspecting network sockets and active connections on Linux.
