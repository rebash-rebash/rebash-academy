---
title: "The htop Command — Interactive Process Monitoring in Linux"
description: "Monitor Linux interactively with htop — search and filter processes, use tree view, manage processes with function keys, and troubleshoot production systems."
difficulty: intermediate
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 6 · Process Management"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - htop
  - monitoring
  - processes
  - performance
  - rebash-linux-mastery
comments: false
status: ready
---

# The `htop` Command — Interactive Process Monitoring in Linux

> `htop` is an advanced, interactive process monitoring tool for Linux. It provides all the capabilities of the `top` command with a more user-friendly interface, color-coded resource usage, mouse support, process searching, tree views, and interactive process management. It is one of the most popular tools used by Linux administrators, DevOps engineers, SREs, and Cloud Architects for monitoring production systems.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 6: Process Management → Lesson 5</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 55 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Process Management</div>

<div markdown>**Lesson:** 5 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `htop` command
- Install `htop`
- Monitor system resources
- Search running processes
- Display process trees
- Manage processes interactively
- Filter process lists
- Troubleshoot production systems

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management and Permissions
- Module 5 – Users and Groups
- Module 6 Lessons 1–4

---

# Why Learn htop?

Imagine your production server has:

- Hundreds of processes
- High CPU utilization
- Memory pressure
- Multiple users

Using:

```bash
top
```

works well.

However:

- Navigation is keyboard-driven
- Searching is limited
- Process hierarchy isn't always obvious

`htop` provides a much more intuitive interface.

---

# What is htop?

`htop` is an interactive system monitor that displays:

- Running processes
- CPU usage
- Memory usage
- Swap usage
- Process tree
- Process owner
- CPU utilization per core

Unlike `top`, `htop` supports:

- Mouse interaction
- Color display
- Scrolling
- Searching
- Filtering

---

# Installing htop

Ubuntu/Debian:

```bash
sudo apt install htop
```

RHEL/Rocky/AlmaLinux:

```bash
sudo dnf install htop
```

Older CentOS:

```bash
sudo yum install htop
```

Arch Linux:

```bash
sudo pacman -S htop
```

---

# Starting htop

Run:

```bash
htop
```

Example:

```text
CPU

Memory

Swap

PID USER CPU% MEM% COMMAND
```

Exit:

```text
F10

or

q
```

---

# Interface Overview

The screen contains:

```text
CPU Usage

↓

Memory Usage

↓

Swap Usage

↓

Running Processes
```

Unlike `top`, resource usage is displayed using colored progress bars.

---

# CPU Monitoring

Displays:

- CPU usage
- Individual CPU cores
- Percentage utilization

Example:

```text
CPU0

CPU1

CPU2

CPU3
```

Useful on multi-core servers.

---

# Memory Monitoring

Displays:

- Total memory
- Used memory
- Cached memory
- Buffers
- Available memory

Memory usage is color-coded for easier interpretation.

---

# Process List

Typical columns:

| Column | Description |
|----------|-------------|
| PID | Process ID |
| USER | Process owner |
| PRI | Priority |
| NI | Nice value |
| VIRT | Virtual memory |
| RES | Resident memory |
| SHR | Shared memory |
| S | Process state |
| CPU% | CPU usage |
| MEM% | Memory usage |
| TIME+ | CPU time |
| COMMAND | Executable |

---

# Search for a Process

Press:

```text
F3
```

Search:

```text
nginx
```

or

```text
java
```

Matching processes are highlighted instantly.

---

# Filter Processes

Press:

```text
F4
```

Enter:

```text
python
```

Only matching processes remain visible.

---

# Display Process Tree

Press:

```text
F5
```

Example:

```text
systemd

└── sshd

     └── bash

          └── python
```

Tree view helps identify parent-child relationships.

---

# Kill a Process

Select a process.

Press:

```text
F9
```

Choose a signal.

Example:

```text
SIGTERM

SIGKILL
```

Confirm.

---

# Renice a Process

Select a process.

Press:

```text
F7

F8
```

Adjust:

```text
Nice Value
```

---

# Sort Processes

Click a column header with the mouse, or use keyboard shortcuts depending on your version of `htop`.

Common sorts include:

- CPU%
- MEM%
- PID
- USER
- TIME

---

# Function Keys

| Key | Purpose |
|------|----------|
| F1 | Help |
| F2 | Setup |
| F3 | Search |
| F4 | Filter |
| F5 | Tree View |
| F6 | Sort |
| F7 | Increase priority (lower nice value, requires appropriate privileges) |
| F8 | Decrease priority (higher nice value) |
| F9 | Kill process |
| F10 | Quit |

---

# Common Commands

Start `htop`.

```bash
htop
```

Display version.

```bash
htop --version
```

Run as root.

```bash
sudo htop
```

---

# Real Production Examples

Monitor Kubernetes.

```bash
htop
```

Search Java.

```text
F3

java
```

Filter Docker.

```text
F4

docker
```

View process tree.

```text
F5
```

Kill a stuck process.

```text
F9
```

---

# htop vs top

| Feature | top | htop |
|----------|-----|------|
| Real-time monitoring | ✅ | ✅ |
| Color interface | ❌ | ✅ |
| Mouse support | ❌ | ✅ |
| Process search | Limited | ✅ |
| Process filtering | Limited | ✅ |
| Tree view | Limited | ✅ |
| Easy navigation | ❌ | ✅ |

---

# Production Perspective

`htop` is commonly used for:

- Linux servers
- Kubernetes nodes
- Docker hosts
- Database servers
- CI/CD servers
- Performance troubleshooting
- Incident response

Many administrators prefer `htop` because it provides more information with less effort.

---

# Hands-on Lab

## Task 1

Install `htop`.

```bash
sudo apt install htop
```

---

## Task 2

Start `htop`.

```bash
htop
```

---

## Task 3

Observe:

- CPU
- Memory
- Swap
- Running processes

---

## Task 4

Search for:

```text
bash
```

Press:

```text
F3
```

---

## Task 5

Filter:

```text
python
```

Press:

```text
F4
```

---

## Task 6

Display tree view.

```text
F5
```

---

## Task 7

Sort processes.

```text
F6
```

Choose:

```text
CPU%
```

---

## Task 8

Exit.

```text
F10
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `htop` | Interactive monitoring | Daily administration |
| `sudo htop` | View all processes | Troubleshooting |
| `F3` | Search | Locate applications |
| `F4` | Filter | Analyze specific processes |
| `F5` | Tree view | Process hierarchy |
| `F9` | Kill process | Process management |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A Kubernetes worker node is responding slowly.

Investigation:

```bash
htop
```

Findings:

- One container runtime process is consuming excessive CPU.
- Memory utilization is normal.
- Process tree shows multiple child processes created by the container runtime.

Next steps:

- Identify the affected workload.
- Review container and application logs.
- Optimize or restart the workload if appropriate.

`htop` provides a quick visual overview that helps identify performance bottlenecks.

---

# Best Practices

- Use `htop` for interactive monitoring and troubleshooting.
- Sort processes by CPU or memory usage.
- Use tree view to understand process relationships.
- Search and filter processes to focus on specific applications.
- Confirm process ownership before terminating processes.

---

# Common Mistakes

❌ Killing system processes without understanding their purpose.

✅ Avoid this mistake: killing system processes without understanding their purpose.

---

❌ Assuming high memory usage always indicates a problem.

✅ Linux often uses free memory for caching.

---

❌ Ignoring parent-child relationships during troubleshooting.

✅ Tree view often reveals the source of unexpected processes.

---

# Interview Questions
## Beginner

1. What is `htop`?
2. How does `htop` differ from `top`?
3. Which key exits `htop`?
4. Which key searches for a process?

---

## Intermediate

1. How do you display the process tree?
2. How do you filter processes?
3. How do you terminate a process from `htop`?
4. Why do many administrators prefer `htop` over `top`?

---

## Architect Level

1. When would you use `htop` instead of `top`?
2. How would you investigate high CPU utilization on a production server using `htop`?
3. How does tree view help troubleshoot complex applications?

---

# Summary

In this lesson, you learned:

- Installing `htop`
- Interactive process monitoring
- CPU and memory analysis
- Process searching
- Process filtering
- Tree view
- Interactive process management
- Production troubleshooting

`htop` is one of the most user-friendly process monitoring tools available for Linux. It combines real-time system monitoring with powerful interactive features, making it an essential utility for administrators and DevOps professionals.

---

## Key Takeaways

- `htop` is an enhanced alternative to `top`.
- It provides color-coded, real-time monitoring.
- Use `F3` to search and `F4` to filter processes.
- Use `F5` to display the process tree.
- Use `F9` to terminate processes interactively.
- `htop` is ideal for troubleshooting production systems.

---

## What's Next?

**[nice and renice — Managing Process Priorities in Linux](nice.md)**

You'll explore:

- Process priorities
- Nice values
- Changing process priority
- CPU scheduling
- Performance optimization
- Production workload management

Understanding process priorities will help you control how Linux allocates CPU time among competing processes.
