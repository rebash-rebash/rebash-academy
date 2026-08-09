---
title: "netstat — Viewing Network Statistics and Connections in Linux"
description: "Use netstat for legacy Linux network diagnostics — view connections, listening ports, routing tables, interface stats, and compare with modern ss."
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
  - netstat
  - net-tools
  - troubleshooting
  - rebash-linux-mastery
comments: false
status: ready
---

# netstat — Viewing Network Statistics and Connections in Linux

> **netstat (Network Statistics)** is a classic Linux networking utility used to display active network connections, listening ports, routing tables, interface statistics, and protocol information. Although **ss** has replaced `netstat` on most modern Linux distributions due to better performance, `netstat` is still widely used on legacy systems, older documentation, and enterprise environments.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 8: Networking → Lesson 8</p>

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

<div markdown>**Lesson:** 8 of 13</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `netstat` command
- View active network connections
- Display listening ports
- View routing tables
- Monitor interface statistics
- Compare `netstat` with `ss`
- Troubleshoot network problems

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
- Module 8 Lessons 1–7

---

# Why Learn netstat?

Imagine:

- You're working on an older RHEL server.
- A troubleshooting guide instructs you to use `netstat`.
- You need to verify if a service is listening on a specific port.

Understanding `netstat` allows you to work confidently with legacy Linux systems.

---

# What is netstat?

`netstat` stands for:

```text
Network Statistics
```

It displays:

- Active TCP connections
- UDP connections
- Listening ports
- Routing tables
- Network interface statistics
- Protocol statistics

---

# Install netstat

On most modern Linux systems, `netstat` is provided by the **net-tools** package.

Ubuntu/Debian:

```bash
sudo apt install net-tools
```

RHEL/Rocky/AlmaLinux:

```bash
sudo dnf install net-tools
```

---

# Display Active Connections

```bash
netstat
```

Example:

```text
Proto

Recv-Q

Send-Q

Local Address

Foreign Address

State
```

---

# Display Listening Ports

```bash
netstat -l
```

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

# Display Listening TCP and UDP Ports

```bash
netstat -tuln
```

Options:

| Option | Meaning |
|----------|----------|
| `-t` | TCP |
| `-u` | UDP |
| `-l` | Listening sockets |
| `-n` | Numeric addresses |

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
sudo netstat -tulpn
```

Example:

```text
tcp

0

0

0.0.0.0:22

LISTEN

900/sshd
```

Displays:

- Process name
- Process ID
- Listening port

---

# View Routing Table

```bash
netstat -r
```

Equivalent modern command:

```bash
ip route
```

---

# View Interface Statistics

```bash
netstat -i
```

Displays:

- Interface name
- Packets received
- Packets transmitted
- Errors
- Drops

---

# Display Protocol Statistics

```bash
netstat -s
```

Shows statistics for:

- TCP
- UDP
- ICMP
- IP

Useful when diagnosing protocol-level problems.

---

# Common Commands

Display all connections.

```bash
netstat
```

Listening ports.

```bash
netstat -tuln
```

Show processes.

```bash
sudo netstat -tulpn
```

Routing table.

```bash
netstat -r
```

Interface statistics.

```bash
netstat -i
```

Protocol statistics.

```bash
netstat -s
```

---

# Real Production Examples

Check SSH.

```bash
sudo netstat -tulpn | grep :22
```

Verify HTTP.

```bash
sudo netstat -tulpn | grep :80
```

Verify HTTPS.

```bash
sudo netstat -tulpn | grep :443
```

Check PostgreSQL.

```bash
sudo netstat -tulpn | grep :5432
```

Display routing table.

```bash
netstat -r
```

---

# Production Perspective

Although `ss` is the preferred tool today, `netstat` is still found in:

- Legacy Linux servers
- Older enterprise environments
- Existing automation scripts
- Technical documentation
- Training materials

Understanding both tools is valuable for supporting diverse Linux environments.

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

Display listening services with processes.

```bash
sudo netstat -tulpn
```

---

## Task 4

Verify SSH.

```bash
sudo netstat -tulpn | grep :22
```

---

## Task 5

View routing table.

```bash
netstat -r
```

---

## Task 6

Display interface statistics.

```bash
netstat -i
```

---

## Task 7

Display protocol statistics.

```bash
netstat -s
```

---

## Task 8

Compare output with the modern `ss` command.

```bash
ss -tuln
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `netstat` | Display connections | Network diagnostics |
| `netstat -tuln` | Show listening ports | Verify services |
| `netstat -tulpn` | Show ports with processes | Process identification |
| `netstat -r` | Display routing table | Routing verification |
| `netstat -i` | Interface statistics | Network troubleshooting |
| `netstat -s` | Protocol statistics | Performance analysis |

---

# netstat vs ss

| Feature | netstat | ss |
|----------|----------|----|
| Performance | Slower | Faster |
| Default on Modern Linux | ❌ | ✅ |
| Socket Statistics | Basic | Advanced |
| Shows Active Connections | ✅ | ✅ |
| Shows Listening Ports | ✅ | ✅ |
| Displays Processes | ✅ | ✅ |
| Recommended Tool | Legacy systems | Modern Linux |

`ss` is the preferred tool for modern Linux systems because it provides faster and more detailed information.

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    Users cannot connect to a web application.

Investigation:

Check listening ports.

```bash
sudo netstat -tulpn | grep :80
```

No output.

Check service status.

```bash
systemctl status nginx
```

NGINX is not running.

Start the service.

```bash
sudo systemctl start nginx
```

Verify again.

```bash
sudo netstat -tulpn | grep :80
```

Output:

```text
tcp

0

0

0.0.0.0:80

LISTEN
```

The web server is now accepting connections.

---

# Best Practices

- Prefer `ss` for modern Linux systems.
- Learn `netstat` for compatibility with legacy environments.
- Verify that services are listening before troubleshooting firewalls.
- Use numeric output (`-n`) for faster results.
- Combine `netstat` with `ping`, `traceroute`, and `curl` during troubleshooting.

---

# Common Mistakes

❌ Assuming `netstat` is installed on every Linux distribution.

✅ Verify `netstat` is installed on every Linux distribution instead of assuming it.

---

❌ Ignoring the `LISTEN` state.

✅ Always review the `LISTEN` state.

---

❌ Forgetting to use `sudo` when viewing process information.

✅ Remember to to use `sudo` when viewing process information.

---

❌ Using `netstat` when `ss` provides better performance.

✅ Avoid using `netstat` when `ss` provides better performance when a safer approach exists.

---

# Interview Questions
## Beginner

1. What is `netstat` used for?
2. Which command displays listening TCP and UDP ports?
3. How do you display the routing table?
4. Which package provides `netstat`?

---

## Intermediate

1. What is the difference between `netstat` and `ss`?
2. How do you display protocol statistics?
3. How do you identify the process listening on a port?
4. Why is `ss` preferred on modern Linux systems?

---

## Architect Level

1. How would you troubleshoot a production server using both `netstat` and `ss`?
2. Why should administrators understand legacy networking tools?
3. How would you migrate operational documentation from `netstat` to `ss`?

---

# Summary

In this lesson, you learned:

- The `netstat` command
- Viewing active connections
- Displaying listening ports
- Viewing routing tables
- Monitoring interface and protocol statistics
- Comparing `netstat` with `ss`
- Production troubleshooting

Although `netstat` has largely been replaced by `ss`, it remains an important utility for supporting legacy Linux systems and understanding older documentation. Knowing both commands ensures you can troubleshoot networking issues across a wide range of Linux environments.

---

## Key Takeaways

- `netstat` displays network connections and statistics.
- Use `netstat -tuln` to view listening TCP and UDP ports.
- Use `netstat -tulpn` to identify the process using a port.
- Use `netstat -r` to display the routing table.
- `ss` is the modern replacement for `netstat`.
- Understanding both tools is valuable for production support.

---

## What's Next?

**[curl — Transferring Data and Testing APIs from the Command Line](curl.md)**

You'll explore:

- Making HTTP and HTTPS requests
- Testing REST APIs
- Downloading web content
- Sending headers and request data
- Authentication
- Debugging web services
- Production troubleshooting

The `curl` command is one of the most powerful and widely used tools for interacting with web services and APIs from the Linux command line.
