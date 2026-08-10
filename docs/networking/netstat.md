---
title: "Linux netstat Command"
description: "Learn the Linux netstat command — active connections, listening ports, routing tables, interface statistics, and how it compares with ss and ip."
difficulty: beginner
estimated_time: "110 min"
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
  - netstat
  - sockets
  - rebash-networking-mastery
comments: false
status: ready
---

# Linux `netstat` Command — Legacy Network Monitoring and Troubleshooting

> The **`netstat` (Network Statistics)** command is a classic Linux networking utility used to display **active network connections, listening ports, routing tables, interface statistics, multicast memberships, and protocol statistics**. Although modern Linux distributions recommend using the **`ss`** command for socket information and the **`ip`** command for routing and interface management, `netstat` remains widely used on legacy systems and is still encountered in enterprise environments, documentation, and interview questions. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand `netstat`.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 9: Linux Networking → Lesson 3</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 110 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Linux Networking</div>

<div markdown>**Lesson:** 3 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `netstat` command
- Display active network connections
- View listening ports
- Display routing tables
- Monitor interface statistics
- Compare `netstat` with `ss`
- Troubleshoot Linux networking

---

# Prerequisites

Complete:

- [Linux `ip` Command](linux-networking-toolkit.md)
- [Linux `ss` Command](ss.md)

---

# Why Learn `netstat`?

Although newer Linux systems recommend:

```bash
ss
```

many enterprise environments still use:

```bash
netstat
```

You'll frequently encounter it in:

- Legacy Linux Servers
- Interview Questions
- Documentation
- Troubleshooting Guides
- Older Automation Scripts

Understanding `netstat` helps you work confidently across both modern and legacy environments.

---

# What is `netstat`?

`netstat` stands for:

```text
Network Statistics
```

It displays:

- Active Connections
- Listening Ports
- Routing Tables
- Network Interfaces
- Protocol Statistics
- Process Information

---

# Package

On many Linux distributions:

```text
netstat
```

is provided by:

```text
net-tools
```

Example installation:

Ubuntu/Debian

```bash
sudo apt install net-tools
```

RHEL/CentOS

```bash
sudo dnf install net-tools
```

---

# Basic Syntax

```bash
netstat [options]
```

Examples:

```bash
netstat
```

```bash
netstat -t
```

```bash
netstat -r
```

---

# Display Active Connections

```bash
netstat
```

Shows:

- Transmission Control Protocol (TCP) Connections
- User Datagram Protocol (UDP) Connections
- Unix Sockets

---

# Display TCP Connections

```bash
netstat -t
```

---

# Display UDP Connections

```bash
netstat -u
```

---

# Display Listening Ports

```bash
netstat -l
```

Shows services waiting for incoming connections.

---

# Display TCP Listening Ports

```bash
netstat -lt
```

---

# Display UDP Listening Ports

```bash
netstat -lu
```

---

# Display All Listening Ports

```bash
netstat -tuln
```

Meaning:

| Option | Purpose |
|----------|----------|
| `-t` | TCP |
| `-u` | UDP |
| `-l` | Listening |
| `-n` | Numeric Output |

Example output:

```text
22

SSH
```

```text
443

HTTPS
```

---

# Display Process Information

```bash
sudo netstat -tulnp
```

Example:

```text
0.0.0.0:22

sshd
```

```text
0.0.0.0:443

nginx
```

---

# Display Numeric Addresses

```bash
netstat -n
```

Prevents hostname resolution.

Benefits:

- Faster Output
- Easier Troubleshooting

---

# Display Routing Table

```bash
netstat -r
```

Equivalent modern command:

```bash
ip route
```

Example:

```text
Destination

Gateway

Interface
```

---

# Display Interface Statistics

```bash
netstat -i
```

Displays:

- RX Packets
- TX Packets
- Errors
- Dropped Packets

Modern alternative:

```bash
ip -s link
```

---

# Display Protocol Statistics

```bash
netstat -s
```

Displays:

- TCP Statistics
- UDP Statistics
- Internet Control Message Protocol (ICMP) Statistics
- Internet Protocol (IP) Statistics

Useful for performance analysis.

---

# Display Multicast Groups

```bash
netstat -g
```

Shows multicast memberships.

---

# Display Unix Domain Sockets

```bash
netstat -x
```

Used for:

- Docker
- Databases
- Local Inter-Process Communication (IPC)

---

# Common TCP States

Typical output includes:

- LISTEN
- ESTABLISHED
- SYN_SENT
- SYN_RECV
- FIN_WAIT_1
- FIN_WAIT_2
- CLOSE_WAIT
- LAST_ACK
- TIME_WAIT

These states help troubleshoot TCP connectivity.

---

# Enterprise Example

Production Web Server:

```text
Users

↓

Load Balancer

↓

Nginx

↓

Application
```

Administrator checks:

```bash
sudo netstat -tulnp
```

Questions answered:

- Is SSH running?
- Is HTTPS listening?
- Which process owns port 443?
- Are required services active?

---

# Cloud Perspective

Legacy cloud virtual machines may still use:

```bash
netstat -tulnp
```

to verify:

- Open Ports
- Running Services
- Listening Applications
- Load Balancer Connectivity

---

# Kubernetes Perspective

Older Kubernetes worker nodes may use:

```bash
netstat
```

to inspect:

- kubelet
- kube-proxy
- Container Runtime
- NodePort Services

Although `ss` is preferred, many operational guides still reference `netstat`.

---

# Linux Perspective

Display listening ports.

```bash
netstat -tuln
```

Display process information.

```bash
sudo netstat -tulnp
```

Display routing table.

```bash
netstat -r
```

Display protocol statistics.

```bash
netstat -s
```

---

# netstat vs ss

| netstat | ss |
|----------|----|
| Older Utility | Modern Utility |
| Part of net-tools | Part of iproute2 |
| Slower | Faster |
| Legacy Systems | Modern Linux |
| Still Widely Known | Recommended for Production |

---

# netstat vs ip

| netstat | ip |
|----------|----|
| Routing Information | Routing Management |
| Interface Statistics | Interface Configuration |
| Legacy Tool | Modern Tool |
| Limited Configuration | Full Network Management |

---

# Common `netstat` Commands

| Command | Purpose |
|----------|----------|
| `netstat` | Display connections |
| `netstat -t` | TCP connections |
| `netstat -u` | UDP connections |
| `netstat -tuln` | Listening ports |
| `netstat -tulnp` | Listening ports with processes |
| `netstat -r` | Routing table |
| `netstat -i` | Interface statistics |
| `netstat -s` | Protocol statistics |
| `netstat -x` | Unix sockets |

---

# Hands-on Lab

## Task 1

Display active connections.

```bash
netstat
```

---

## Task 2

Display listening ports.

```bash
netstat -tuln
```

---

## Task 3

Display process information.

```bash
sudo netstat -tulnp
```

---

## Task 4

Display routing table.

```bash
netstat -r
```

---

## Task 5

Display protocol statistics.

```bash
netstat -s
```

---

## Task 6

Display interface statistics.

```bash
netstat -i
```

---

## Task 7

Compare output from:

```bash
netstat
```

and

```bash
ss
```

Identify the differences in speed, formatting, and available information.

---

## Task 8

Create a troubleshooting checklist using:

- `netstat`
- `ss`
- `ip`
- `ping`
- `traceroute`

---

# Production Troubleshooting

Problem:

```text
Application

Not Reachable
```

Step 1

```bash
sudo netstat -tulnp
```

↓

Is the application listening?

↓

Yes

↓

Check:

```bash
netstat -r
```

↓

Correct Route?

↓

Yes

↓

Check:

```bash
ping Gateway
```

↓

Check:

```bash
traceroute Destination
```

This approach helps isolate whether the issue is related to the application, routing, or network connectivity.

---

# Common Mistakes

❌ Using `netstat` on minimal Linux installations without `net-tools`.

✅ Install `net-tools` or use `ss` instead.

---

❌ Forgetting `sudo` for process information.

✅ Use elevated privileges when viewing process ownership.

---

❌ Relying only on `netstat` for routing changes.

✅ Use the `ip` command for configuration tasks.

---

❌ Confusing listening sockets with active connections.

✅ Use appropriate options such as `-l` and `-t`.

---

❌ Ignoring protocol statistics.

✅ Review `netstat -s` when troubleshooting network performance.

---

# Best Practices

- Prefer `ss` and `ip` on modern Linux systems.
- Learn `netstat` because it is common in legacy environments.
- Always use numeric output during troubleshooting.
- Verify which process owns a listening port.
- Compare routing information using both `netstat` and `ip`.
- Use protocol statistics to investigate network issues.
- Update legacy automation scripts to use modern tools where practical.

---

# Interview Questions

## Beginner

1. What is the `netstat` command?
2. How do you display listening ports?
3. How do you display the routing table?
4. What package provides `netstat`?

---

## Intermediate

1. Compare `netstat` and `ss`.
2. Compare `netstat` and `ip`.
3. How do you display protocol statistics?
4. How do you determine which process owns a network port?

---

## Architect Level

1. Explain how you would troubleshoot a production server using `netstat`.
2. Why has `netstat` largely been replaced by `ss`?
3. How would you modernize a legacy monitoring environment that relies on `netstat`?

---

# Summary

In this lesson, you learned:

- The `netstat` command
- Active Network Connections
- Listening Ports
- Routing Tables
- Interface Statistics
- Protocol Statistics
- Unix Domain Sockets
- Legacy Network Diagnostics

Although `netstat` is considered a legacy networking utility, it remains valuable for understanding older Linux systems, enterprise environments, and historical documentation. Modern Linux distributions recommend using **`ss`** for socket information and **`ip`** for interface and routing management, but familiarity with `netstat` remains an important skill for Linux professionals.

---

## Key Takeaways

- `netstat` is a **legacy network monitoring tool**.
- Use **`netstat -tuln`** to display listening ports.
- Use **`sudo netstat -tulnp`** to identify the owning process.
- Use **`netstat -r`** to display routing information.
- Use **`netstat -s`** to view protocol statistics.
- Modern Linux systems recommend **`ss`** and **`ip`**, but `netstat` remains common on older systems and in documentation.

---

## What's Next?

**[tcpdump](packet-analysis-tcpdump-wireshark.md)**

In the next lesson, you'll learn about **`tcpdump`**.

You'll explore:

- What `tcpdump` is
- Packet Capture
- Network Traffic Analysis
- Packet Filtering
- Protocol Inspection
- Troubleshooting Network Issues
- Production Packet Analysis

By the end of the lesson, you'll understand how to capture, inspect, and analyse network packets at a low level, making `tcpdump` one of the most valuable tools for Linux network troubleshooting and security investigations.
