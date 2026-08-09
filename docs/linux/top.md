---
title: "The top Command — Real-Time Process Monitoring in Linux"
description: "Monitor Linux in real time with top — interpret CPU, memory, load average, sort processes, and troubleshoot production performance issues."
difficulty: intermediate
estimated_time: "60 min"
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
  - top
  - monitoring
  - performance
  - cpu
  - rebash-linux-mastery
comments: false
status: ready
---

# The `top` Command — Real-Time Process Monitoring in Linux

> The `top` command is one of the most powerful Linux monitoring tools. Unlike the `ps` command, which displays a snapshot of running processes, `top` provides a **real-time, continuously updating view** of system activity. It allows administrators to monitor CPU usage, memory consumption, load averages, running processes, and system performance from a single interactive interface.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 6: Process Management → Lesson 4</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 60 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Process Management</div>

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `top` command
- Monitor system performance in real time
- Interpret CPU and memory usage
- Analyze running processes
- Sort processes interactively
- Identify resource-intensive applications
- Manage processes from `top`
- Troubleshoot production performance issues

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management and Permissions
- Module 5 – Users and Groups
- Module 6 Lessons 1–3

---

# Why Learn top?

Imagine users report:

- The server is slow.
- Applications are hanging.
- CPU usage is very high.
- Memory is almost full.

The first command many Linux administrators execute is:

```bash
top
```

It immediately shows which processes are consuming system resources.

---

# What is top?

`top` is a real-time system monitoring utility.

It continuously displays:

- Running processes
- CPU usage
- Memory usage
- Load averages
- Process states
- System uptime

The display refreshes automatically every few seconds.

---

# Starting top

Run:

```bash
top
```

Example:

```text
top - 10:45:12

Tasks: 245 total

Cpu(s): 12.5% us

Mem: 16 GB

PID USER %CPU %MEM COMMAND
```

Exit by pressing:

```text
q
```

---

# Understanding the Header

The top section provides an overview of system health.

Example:

```text
top - 10:45:12 up 5 days, 3 users

Tasks: 215 total

%Cpu(s): 12 us, 3 sy, 85 id

MiB Mem : 16000 total

MiB Swap: 4096 total
```

---

# Load Average

Example:

```text
load average:

0.42

0.50

0.61
```

These values represent the average system load over:

- Last 1 minute
- Last 5 minutes
- Last 15 minutes

Generally:

- A value close to the number of CPU cores indicates normal utilization.
- Values significantly higher than the available CPU cores may indicate CPU contention.

---

# CPU Usage

Example:

```text
%Cpu(s)

us

sy

ni

id

wa

hi

si

st
```

Meaning:

| Field | Description |
|--------|-------------|
| us | User processes |
| sy | Kernel (system) processes |
| ni | Nice processes |
| id | Idle CPU time |
| wa | Waiting for I/O |
| hi | Hardware interrupts |
| si | Software interrupts |
| st | Stolen CPU time (virtualized environments) |

---

# Memory Usage

Example:

```text
MiB Mem :

16000 total

4200 used

9800 free

2000 buff/cache
```

Key fields:

| Field | Description |
|--------|-------------|
| Total | Installed memory |
| Used | Memory currently in use |
| Free | Unused memory |
| Buff/Cache | Memory used for buffers and filesystem cache |

Linux intentionally uses available RAM for caching to improve performance.

---

# Swap Usage

Example:

```text
Swap

4096 total

120 used

3976 free
```

Heavy swap usage may indicate memory pressure.

---

# Process Table

Typical columns:

| Column | Description |
|----------|-------------|
| PID | Process ID |
| USER | Process owner |
| PR | Priority |
| NI | Nice value |
| VIRT | Virtual memory |
| RES | Physical memory used |
| SHR | Shared memory |
| S | Process state |
| %CPU | CPU usage |
| %MEM | Memory usage |
| TIME+ | CPU time |
| COMMAND | Executable |

---

# Interactive Commands

While `top` is running:

| Key | Action |
|-----|--------|
| `q` | Quit |
| `P` | Sort by CPU usage |
| `M` | Sort by memory usage |
| `T` | Sort by CPU time |
| `k` | Kill a process |
| `r` | Change process priority (renice) |
| `h` | Display help |
| `1` | Show CPU usage per core |

---

# Search for a Process

Press:

```text
L
```

Enter:

```text
nginx
```

or

```text
java
```

This highlights matching processes.

---

# Display Per-CPU Statistics

Press:

```text
1
```

Example:

```text
CPU0

CPU1

CPU2

CPU3
```

Useful for multi-core systems.

---

# Batch Mode

Capture `top` output without the interactive interface.

```bash
top -b -n 1
```

Useful for:

- Scripts
- Logs
- Automation

---

# Common Commands

Start `top`.

```bash
top
```

Batch mode.

```bash
top -b -n 1
```

Monitor a specific PID.

```bash
top -p 1234
```

Monitor multiple PIDs.

```bash
top -p 1234,5678
```

---

# Real Production Examples

Monitor Kubernetes.

```bash
top
```

Monitor Docker.

```bash
top -p <PID>
```

Identify high CPU usage.

```text
Press P
```

Identify memory usage.

```text
Press M
```

---

# Production Perspective

The `top` command is widely used for:

- Performance troubleshooting
- CPU monitoring
- Memory analysis
- Capacity planning
- Database monitoring
- Kubernetes worker nodes
- Cloud virtual machines
- Production incident response

It provides a quick health check for almost every Linux system.

---

# Hands-on Lab

## Task 1

Start `top`.

```bash
top
```

Exit with:

```text
q
```

---

## Task 2

Observe:

- CPU usage
- Memory usage
- Load average
- Running tasks

---

## Task 3

Sort by CPU.

Press:

```text
P
```

---

## Task 4

Sort by memory.

Press:

```text
M
```

---

## Task 5

Display individual CPU cores.

Press:

```text
1
```

---

## Task 6

Search for a process.

Press:

```text
L
```

Enter:

```text
bash
```

---

## Task 7

Run in batch mode.

```bash
top -b -n 1
```

---

## Task 8

Monitor your current shell.

First:

```bash
echo $$
```

Then:

```bash
top -p <PID>
```

Replace `<PID>` with the value displayed by `echo $$`.

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `top` | Real-time monitoring | Performance analysis |
| `top -b -n 1` | Batch mode | Automation |
| `top -p PID` | Monitor a process | Application diagnostics |
| `P` | Sort by CPU | CPU troubleshooting |
| `M` | Sort by memory | Memory troubleshooting |
| `1` | Per-core CPU view | Multi-core analysis |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A production server becomes slow.

Investigation:

```bash
top
```

Findings:

- CPU utilization is above 95%.
- One Java process is consuming most of the CPU.
- Memory usage is normal.
- Load average is significantly higher than the number of CPU cores.

Next steps:

- Identify the application.
- Review application logs.
- Investigate the workload.
- Optimize or restart the application if appropriate.

The `top` command quickly identifies the source of the performance issue.

---

# Best Practices

- Use `top` as the first step in performance troubleshooting.
- Monitor CPU, memory, and load average together.
- Sort by CPU or memory to identify resource-intensive processes.
- Verify process ownership before terminating processes.
- Use batch mode for automation and reporting.

---

# Common Mistakes

❌ Assuming high memory usage always indicates a problem.

✅ Linux uses free memory for filesystem caching, which is generally beneficial.

---

❌ Confusing CPU utilization with load average.

✅ Load average includes processes waiting for CPU time or uninterruptible resources such as disk I/O.

---

❌ Terminating high CPU processes without understanding their purpose.

✅ Always investigate the root cause first.

---

# Interview Questions
## Beginner

1. What is the purpose of the `top` command?
2. How do you exit `top`?
3. What is the difference between `top` and `ps`?
4. Which key sorts processes by CPU usage?

---

## Intermediate

1. What does load average represent?
2. How do you monitor a specific process using `top`?
3. What is batch mode?
4. Why is Linux cache memory usually not a problem?

---

## Architect Level

1. How would you investigate a server experiencing high CPU utilization?
2. Why should CPU usage, memory usage, and load average be analyzed together?
3. How would you use `top` during a production incident involving performance degradation?

---

# Summary

In this lesson, you learned:

- The `top` command
- Real-time process monitoring
- CPU utilization
- Memory usage
- Load averages
- Interactive process management
- Process sorting
- Production troubleshooting

The `top` command is one of the most valuable Linux administration tools. It provides a live view of system performance, making it indispensable for diagnosing resource bottlenecks, identifying runaway processes, and monitoring production systems.

---

## Key Takeaways

- `top` provides a real-time view of system performance.
- Monitor CPU, memory, swap, and load average together.
- Use `P` to sort by CPU usage.
- Use `M` to sort by memory usage.
- Use `top -p` to monitor a specific process.
- Use batch mode (`top -b -n 1`) for scripts and automation.

---

## What's Next?

**[The htop Command — Interactive Process Monitoring in Linux](htop.md)**

You'll explore:

- Installing `htop`
- Interactive process management
- Mouse support
- Tree view
- Process filtering
- Easier navigation
- Advanced monitoring features

`htop` builds on the capabilities of `top` with a more user-friendly interface and powerful interactive features for Linux administrators and DevOps engineers.
