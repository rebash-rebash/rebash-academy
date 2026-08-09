---
title: "ss (Socket Statistics) — Viewing Network Connections in Linux"
description: "Use ss to inspect Linux network sockets — view listening ports, TCP/UDP connections, processes, socket states, and replace netstat for modern diagnostics."
difficulty: intermediate
estimated_time: "65 min"
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
  - ss
  - sockets
  - troubleshooting
  - rebash-linux-mastery
comments: false
status: ready
---

# ss (Socket Statistics) — Viewing Network Connections in Linux

> The **ss (Socket Statistics)** command is the modern Linux utility for displaying network sockets, active connections, listening ports, and protocol statistics. It is significantly faster and more powerful than the legacy `netstat` command and is the preferred tool for network diagnostics on modern Linux systems. Every Linux administrator, DevOps engineer, Cloud Architect, Network Engineer, and Site Reliability Engineer (SRE) should be proficient with `ss`.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 8: Networking → Lesson 7</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 65 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Networking</div>

<div markdown>**Lesson:** 7 of 13</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand network sockets
- View active network connections
- Display listening ports
- Filter TCP and UDP connections
- Identify services using ports
- Monitor network activity
- Troubleshoot production networking issues

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
- Module 8 Lessons 1–6

---

# Why Learn ss?

Imagine:

- A web server isn't accepting connections.
- SSH suddenly stops working.
- A database port appears closed.
- An application is listening on the wrong port.

One of the first commands an administrator uses is:

```bash
ss
```

It quickly shows:

- Active connections
- Listening ports
- Socket states
- Associated processes

---

# What is a Socket?

A **socket** is a communication endpoint identified by:

```text
IP Address

+

Port Number

+

Protocol
```

Example:

```text
192.168.1.10:22
```

Applications communicate through sockets.

---

# What is ss?

`ss` stands for:

```text
Socket Statistics
```

It displays:

- TCP connections
- UDP sockets
- UNIX domain sockets
- Listening services
- Connection states
- Network statistics

---

# Basic ss Command

Display all sockets.

```bash
ss
```

Example:

```text
Netid

State

Recv-Q

Send-Q
```

---

# Display Listening Ports

```bash
ss -l
```

Shows services waiting for incoming connections.

---

# Display TCP Connections

```bash
ss -t
```

---

# Display UDP Connections

```bash
ss -u
```

---

# Display Listening TCP Ports

```bash
ss -lt
```

---

# Display Listening UDP Ports

```bash
ss -lu
```

---

# Display All Listening Ports

```bash
ss -tuln
```

Options:

| Option | Meaning |
|---------|----------|
| `-t` | TCP |
| `-u` | UDP |
| `-l` | Listening sockets |
| `-n` | Show numeric addresses (don't resolve hostnames or service names) |

Example:

```text
22

80

443

3306
```

---

# Show Processes Using Ports

```bash
sudo ss -tulpn
```

Example:

```text
LISTEN

0

128

*:22

users:(("sshd",pid=900))
```

Displays:

- Process name
- Process ID (PID)
- Listening port

---

# Filter by Port

View connections on port 22.

```bash
ss -tuln | grep :22
```

---

# View Established Connections

```bash
ss -t state established
```

Displays active TCP sessions.

---

# View Connection Statistics

```bash
ss -s
```

Example:

```text
TCP

Established

Closed

Timewait
```

Useful for obtaining a quick summary of socket usage.

---

# Display UNIX Domain Sockets

```bash
ss -x
```

UNIX sockets are commonly used for communication between processes on the same machine.

---

# Common Socket States

| State | Description |
|--------|-------------|
| LISTEN | Waiting for incoming connections |
| ESTAB | Connection established |
| TIME-WAIT | Waiting before closing completely |
| CLOSE-WAIT | Waiting for application to close |
| SYN-SENT | Connection request sent |
| SYN-RECV | Connection request received |

Understanding these states helps diagnose connection issues.

---

# Common Commands

Display all sockets.

```bash
ss
```

Display listening ports.

```bash
ss -l
```

Display listening TCP and UDP ports.

```bash
ss -tuln
```

Show processes.

```bash
sudo ss -tulpn
```

Connection summary.

```bash
ss -s
```

---

# Real Production Examples

Check SSH.

```bash
sudo ss -tulpn | grep :22
```

Verify NGINX.

```bash
sudo ss -tulpn | grep :80
```

Verify HTTPS.

```bash
sudo ss -tulpn | grep :443
```

Check PostgreSQL.

```bash
sudo ss -tulpn | grep :5432
```

Verify MySQL.

```bash
sudo ss -tulpn | grep :3306
```

---

# Production Perspective

`ss` is widely used for:

- Linux servers
- Cloud virtual machines
- Kubernetes nodes
- Containers
- Database servers
- Load balancers
- API servers
- Security investigations

It is one of the first commands used to verify whether a service is actually listening on the expected port.

---

# Hands-on Lab

## Task 1

Display all sockets.

```bash
ss
```

---

## Task 2

Display listening ports.

```bash
ss -l
```

---

## Task 3

Display all listening TCP and UDP ports.

```bash
ss -tuln
```

---

## Task 4

Show listening services and associated processes.

```bash
sudo ss -tulpn
```

---

## Task 5

Check whether SSH is listening.

```bash
sudo ss -tulpn | grep :22
```

---

## Task 6

Display established TCP connections.

```bash
ss -t state established
```

---

## Task 7

Display socket statistics.

```bash
ss -s
```

---

## Task 8

Display UNIX domain sockets.

```bash
ss -x
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `ss` | Display sockets | Network diagnostics |
| `ss -l` | Show listening sockets | Service verification |
| `ss -t` | Show TCP sockets | TCP analysis |
| `ss -u` | Show UDP sockets | UDP analysis |
| `ss -tuln` | Show listening TCP/UDP ports | Port verification |
| `ss -tulpn` | Show ports with processes | Service identification |
| `ss -s` | Display socket summary | Performance monitoring |
| `ss -x` | Show UNIX sockets | Local IPC troubleshooting |

---

# ss vs netstat

| Feature | ss | netstat |
|----------|----|----------|
| Performance | Faster | Slower |
| Default on Modern Linux | ✅ | ❌ |
| Displays Socket Statistics | ✅ | Limited |
| Shows Listening Ports | ✅ | ✅ |
| Shows Active Connections | ✅ | ✅ |
| Shows Processes | ✅ | ✅ (with options) |

`ss` is the recommended replacement for `netstat` on modern Linux systems.

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    Users report they cannot access a web application.

Investigation:

Check whether NGINX is listening.

```bash
sudo ss -tulpn | grep :80
```

No output.

Check the service.

```bash
systemctl status nginx
```

NGINX is stopped.

Start the service.

```bash
sudo systemctl start nginx
```

Verify again.

```bash
sudo ss -tulpn | grep :80
```

Output:

```text
LISTEN

*:80
```

The application is now reachable.

---

# Best Practices

- Use `ss` instead of the deprecated `netstat`.
- Verify that services are listening before troubleshooting firewalls.
- Use `-n` for faster output by avoiding DNS resolution.
- Use `-p` to identify the process associated with a socket.
- Monitor connection states during performance troubleshooting.

---

# Common Mistakes

❌ Forgetting to use `sudo` when viewing process information.

✅ Remember to to use `sudo` when viewing process information.

---

❌ Assuming a running service is listening on the expected port.

✅ Verify a running service is listening on the expected port instead of assuming it.

---

❌ Ignoring connection states such as `TIME-WAIT` and `CLOSE-WAIT`.

✅ Always review connection states such as `TIME-WAIT` and `CLOSE-WAIT`.

---

❌ Using `netstat` on systems where `ss` is available.

✅ Avoid using `netstat` on systems where `ss` is available when a safer approach exists.

---

# Interview Questions
## Beginner

1. What does `ss` stand for?
2. Which command displays listening TCP and UDP ports?
3. What is a socket?
4. What does the `-l` option do?

---

## Intermediate

1. What is the purpose of the `-p` option?
2. What is the difference between TCP and UDP sockets?
3. How do you display established TCP connections?
4. What does the `LISTEN` state indicate?

---

## Architect Level

1. How would you troubleshoot a production service that is not accepting connections?
2. Why is `ss` preferred over `netstat`?
3. How would you identify which process is using a specific network port?

---

# Summary

In this lesson, you learned:

- Network sockets
- The `ss` command
- Listening ports
- TCP and UDP sockets
- Connection states
- Process identification
- Socket statistics
- Production troubleshooting

The `ss` command is the modern standard for inspecting network sockets on Linux. It provides fast, detailed information about active connections, listening services, and socket states, making it an essential tool for diagnosing networking and application issues.

---

## Key Takeaways

- `ss` is the preferred replacement for `netstat`.
- Use `ss -tuln` to view listening TCP and UDP ports.
- Use `ss -tulpn` to identify which process owns a listening port.
- Socket states provide valuable troubleshooting information.
- Always verify that a service is listening before investigating network connectivity issues.
- `ss` is an essential tool for production Linux administration.

---

## What's Next?

**[netstat — Viewing Network Statistics and Connections in Linux](netstat.md)**

You'll explore:

- Legacy network statistics
- Viewing network connections
- Routing tables
- Interface statistics
- Differences between `netstat` and `ss`
- When `netstat` is still useful
- Production troubleshooting techniques

Although `ss` is the preferred tool today, understanding `netstat` remains valuable because it is still encountered in legacy Linux systems and documentation.
