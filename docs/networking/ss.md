---
title: "Linux ss Command"
description: "Learn the Linux ss command — socket statistics, TCP/UDP connections, listening ports, process ownership, and production troubleshooting."
difficulty: beginner
estimated_time: "120 min"
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
  - ss
  - sockets
  - rebash-networking-mastery
comments: false
status: ready
---

# Linux `ss` Command — Inspecting Network Connections and Socket Statistics

> The **`ss` (Socket Statistics)** command is a modern Linux utility used to inspect **network sockets, active connections, listening ports, Transmission Control Protocol (TCP) states, User Datagram Protocol (UDP) sockets, Unix sockets, and process information**. It is part of the **iproute2** package and is the recommended replacement for the legacy **netstat** command. The `ss` command is significantly faster because it reads socket information directly from the Linux kernel instead of parsing multiple files. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should master the `ss` command.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 9: Linux Networking → Lesson 2</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 120 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Linux Networking</div>

<div markdown>**Lesson:** 2 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `ss` command
- View active TCP and UDP connections
- Display listening ports
- Analyze socket states
- Identify processes using network ports
- Troubleshoot Linux networking
- Monitor production servers

---

# Prerequisites

Complete:

- [Linux `ip` Command](linux-networking-toolkit.md)

Basic understanding of:

- TCP/IP
- Ports
- Network Connections

---

# Why Learn the `ss` Command?

Suppose users report:

- Website Not Accessible
- Database Connection Failure
- SSH Not Working
- High Network Usage
- Unknown Open Ports

One of the first commands every Linux engineer executes is:

```bash
ss
```

It immediately answers questions such as:

- Which ports are open?
- Which process owns a port?
- Which TCP connections are active?
- How many clients are connected?
- What TCP states exist?

---

# What is `ss`?

`ss` stands for:

```text
Socket Statistics
```

It displays:

- TCP Connections
- UDP Connections
- Unix Domain Sockets
- Listening Services
- Socket States
- Process Information

---

# Why Replace netstat?

Older systems used:

```bash
netstat
```

Modern Linux recommends:

```bash
ss
```

Advantages:

- Faster
- More Accurate
- Reads Kernel Data Directly
- Better Performance
- Actively Maintained

---

# Basic Syntax

```bash
ss [options]
```

Examples:

```bash
ss
```

```bash
ss -t
```

```bash
ss -l
```

---

# Display All Connections

```bash
ss
```

Displays:

- TCP
- UDP
- Unix Sockets

---

# Display TCP Connections

```bash
ss -t
```

Example:

```text
ESTAB

192.168.1.10:22

192.168.1.50:50520
```

---

# Display UDP Connections

```bash
ss -u
```

---

# Display Listening Ports

```bash
ss -l
```

Shows services waiting for incoming connections.

Example:

```text
22

SSH
```

```text
80

HTTP
```

---

# Display TCP Listening Ports

```bash
ss -lt
```

---

# Display UDP Listening Ports

```bash
ss -lu
```

---

# Display Listening Ports with Process Names

```bash
sudo ss -ltnp
```

Example:

```text
LISTEN

0.0.0.0:22

sshd
```

```text
LISTEN

0.0.0.0:443

nginx
```

---

# Display Process Information

```bash
sudo ss -p
```

Shows:

- PID
- Process Name

Associated with each socket.

---

# Display Numeric Addresses

```bash
ss -n
```

Disables Domain Name System (DNS) resolution.

Useful for:

- Faster Output
- Troubleshooting

---

# Combine Options

Common example:

```bash
sudo ss -tunlp
```

Meaning:

| Option | Purpose |
|----------|----------|
| `-t` | TCP |
| `-u` | UDP |
| `-n` | Numeric Output |
| `-l` | Listening |
| `-p` | Process Information |

---

# Display Established Connections

```bash
ss -t state established
```

Shows active TCP sessions.

---

# Display Listening State

```bash
ss -t state listening
```

---

# Display Specific Port

Example:

```bash
ss -ltn '( sport = :22 )'
```

Shows only SSH.

---

# Display HTTP Connections

```bash
ss -tn '( dport = :80 )'
```

---

# Display HTTPS Connections

```bash
ss -tn '( dport = :443 )'
```

---

# Display SSH Sessions

```bash
ss -tn '( dport = :22 )'
```

---

# Display Unix Domain Sockets

```bash
ss -x
```

Useful for:

- Docker
- MySQL
- PostgreSQL
- Local Inter-Process Communication (IPC)

---

# TCP States

Common TCP states:

- LISTEN
- ESTABLISHED
- SYN-SENT
- SYN-RECV
- FIN-WAIT-1
- FIN-WAIT-2
- CLOSE-WAIT
- LAST-ACK
- TIME-WAIT
- CLOSED

Example:

```bash
ss -tan
```

Displays socket states.

---

# Connection Example

```text
Client

↓

TCP 443

↓

Web Server

↓

ESTABLISHED
```

Displayed by:

```bash
ss -t
```

---

# Enterprise Example

Production Web Server

```text
Internet

↓

Load Balancer

↓

Nginx

↓

Application
```

Troubleshooting:

```bash
sudo ss -ltnp
```

Questions answered:

- Is Nginx listening?
- Is port 443 open?
- Is SSH running?
- Which process owns the port?

---

# Cloud Perspective

Cloud engineers frequently use:

```bash
ss -tuln
```

to verify:

- VM Services
- Load Balancer Health
- Open Ports
- Application Availability

---

# Kubernetes Perspective

On Kubernetes worker nodes:

```bash
ss -tuln
```

helps inspect:

- kubelet
- kube-proxy
- Container Runtime
- Ingress Controller
- NodePort Services

Useful during cluster troubleshooting.

---

# Linux Perspective

Common commands:

Display all listening ports.

```bash
ss -tuln
```

Display process names.

```bash
sudo ss -tulnp
```

Display established TCP sessions.

```bash
ss -t state established
```

Display Unix sockets.

```bash
ss -x
```

---

# Common `ss` Commands

| Command | Purpose |
|----------|----------|
| `ss` | Display sockets |
| `ss -t` | Display TCP connections |
| `ss -u` | Display UDP connections |
| `ss -l` | Display listening sockets |
| `ss -tuln` | Display listening TCP/UDP ports |
| `ss -p` | Display process information |
| `ss -x` | Display Unix sockets |
| `ss -tan` | Display TCP states |

---

# Hands-on Lab

## Task 1

Display all sockets.

```bash
ss
```

---

## Task 2

Display TCP connections.

```bash
ss -t
```

---

## Task 3

Display UDP connections.

```bash
ss -u
```

---

## Task 4

Display listening ports.

```bash
ss -tuln
```

---

## Task 5

Display process information.

```bash
sudo ss -tulnp
```

---

## Task 6

Display SSH connections.

```bash
ss -tn '( dport = :22 )'
```

---

## Task 7

Display HTTPS connections.

```bash
ss -tn '( dport = :443 )'
```

---

## Task 8

Create a troubleshooting checklist using:

- `ss`
- `ip addr`
- `ip route`
- `ping`
- `traceroute`

---

# Production Troubleshooting

Problem:

```text
Website

Not Working
```

Check:

```bash
sudo ss -ltnp
```

↓

Port 443 Listening?

↓

Yes

↓

Check Connections

```bash
ss -tn state established
```

↓

Many Clients?

↓

Investigate Logs

This workflow quickly confirms whether the application is listening and accepting connections.

---

# Common Mistakes

❌ Forgetting `sudo` when viewing process information.

✅ Use elevated privileges to view owning processes.

---

❌ Confusing listening sockets with established connections.

✅ Use the correct filters and TCP states.

---

❌ Assuming every open port is a security issue.

✅ Verify which service owns the port.

---

❌ Ignoring TCP state information.

✅ Analyse connection states during troubleshooting.

---

❌ Resolving hostnames unnecessarily.

✅ Use `-n` for faster output and clearer diagnostics.

---

# Best Practices

- Use `ss` instead of `netstat` on modern Linux systems.
- Always verify which process owns an open port.
- Use numeric output during troubleshooting.
- Monitor established connections on production systems.
- Regularly audit listening ports.
- Combine `ss` with `ip`, `tcpdump`, and `journalctl` for complete network analysis.
- Restrict unnecessary listening services.

---

# Interview Questions

## Beginner

1. What is the `ss` command?
2. How do you display listening ports?
3. How do you display TCP connections?
4. What does `ss -tuln` show?

---

## Intermediate

1. Why is `ss` preferred over `netstat`?
2. How do you determine which process owns a port?
3. Explain common TCP connection states.
4. How would you identify all active SSH sessions?

---

## Architect Level

1. Explain how you would troubleshoot a production web server using `ss`.
2. Design a Linux networking troubleshooting workflow using `ss` and `ip`.
3. How would you identify abnormal network activity using socket statistics?

---

# Summary

In this lesson, you learned:

- The `ss` command
- TCP Connections
- UDP Connections
- Listening Ports
- Socket States
- Process Information
- Unix Domain Sockets
- Linux Network Troubleshooting

The `ss` command is one of the most powerful networking tools available on Linux. It provides fast and detailed visibility into active connections, listening services, socket states, and process ownership. Mastering `ss` enables engineers to troubleshoot connectivity problems, identify open ports, monitor production workloads, and analyse network behaviour efficiently.

---

## Key Takeaways

- `ss` is the **modern replacement** for `netstat`.
- Use **`ss -t`** to view TCP connections.
- Use **`ss -u`** to view UDP connections.
- Use **`ss -tuln`** to display listening ports.
- Use **`sudo ss -tulnp`** to identify which process owns a port.
- Understanding **TCP states** is essential for network troubleshooting.
- `ss` is a core diagnostic tool for Linux servers, Kubernetes nodes, and cloud infrastructure.

---

## What's Next?

**[netstat](netstat.md)**

In the next lesson, you'll learn about **`netstat`**.

You'll explore:

- What `netstat` is
- Active Connections
- Routing Tables
- Interface Statistics
- Listening Ports
- Process Information
- Legacy Network Diagnostics

By the end of the lesson, you'll understand how `netstat` works, how it compares with `ss`, and why it remains useful when working with legacy Linux systems and troubleshooting older environments.
