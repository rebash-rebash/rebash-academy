---
title: "Memory Monitoring — Monitoring RAM and Swap Usage in Linux"
description: "Monitor Linux RAM and swap — free, vmstat, top, htop, OOM events, process memory analysis, and production memory monitoring practices."
difficulty: intermediate
estimated_time: "95 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 12 · Monitoring and Logs"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - monitoring
  - memory
  - ram
  - swap
  - oom
  - rebash-linux-mastery
comments: false
status: ready
---

# Memory Monitoring — Monitoring RAM and Swap Usage in Linux

> **Memory Monitoring** is the process of tracking RAM utilization, swap usage, memory allocation, cache usage, and memory-intensive processes to ensure Linux systems operate efficiently. Insufficient available memory can lead to application slowdowns, excessive swapping, Out of Memory (OOM) events, and system instability. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, and Site Reliability Engineer (SRE) should understand how to monitor memory usage and troubleshoot memory-related issues in production environments.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 12: Monitoring & Logs → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 95 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Monitoring & Logs</div>

<div markdown>**Lesson:** 6 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Linux memory management
- Monitor RAM and swap usage
- Interpret memory statistics
- Identify memory-intensive processes
- Monitor memory performance
- Detect memory bottlenecks
- Troubleshoot memory issues
- Apply production monitoring best practices

---

# Prerequisites

Complete:

- Modules 1–11
- Module 12 Lessons 1–5

---

# Why Learn Memory Monitoring?

Imagine a production application server.

Without monitoring:

```text
Memory Usage Increases

↓

RAM Exhausted

↓

OOM Killer Terminates Process

↓

Application Downtime
```

With monitoring:

```text
Memory Usage

↓

Alert at 80%

↓

Investigate

↓

Optimize

↓

Stable Application
```

Monitoring memory helps prevent application failures.

---

# Linux Memory Overview

Linux uses memory for:

- Running applications
- Kernel operations
- File system cache
- Buffers
- Shared memory
- Swap

Unused memory is often used for caching to improve performance.

---

# Memory Architecture

```text
Applications

↓

RAM

↓

Cache/Buffers

↓

Swap (If Needed)

↓

Disk
```

RAM is significantly faster than swap storage.

---

# Check Memory Usage

The most common command:

```bash
free -h
```

Example:

```text
              total   used   free  shared  buff/cache  available

Mem:          16Gi   6Gi    2Gi     1Gi       8Gi         9Gi

Swap:          4Gi     0B     4Gi
```

---

# Understanding free Output

| Column | Description |
|----------|-------------|
| total | Total RAM |
| used | Memory currently in use |
| free | Completely unused RAM |
| shared | Shared memory |
| buff/cache | Memory used for buffers and filesystem cache |
| available | Estimated memory available for new applications |

!!! note "Important"

    On Linux, a low **free** value is normal. Focus on the **available** column, which better represents how much memory can be allocated without swapping.

---

# Check Memory in Megabytes

```bash
free -m
```

---

# Check Memory in Gigabytes

```bash
free -g
```

---

# Monitor Memory Continuously

Refresh every two seconds.

```bash
watch free -h
```

Useful during troubleshooting.

---

# View Memory Statistics

Use:

```bash
vmstat
```

Example:

```bash
vmstat 2
```

Refresh every two seconds.

Important columns:

- Free memory
- Buffers
- Cache
- Swap activity
- CPU usage

---

# Monitor Memory with top

```bash
top
```

Memory summary:

```text
MiB Mem

MiB Swap
```

Press:

```text
Shift + M
```

Sort processes by memory usage.

---

# Monitor Memory with htop

```bash
htop
```

Benefits:

- Colorized display
- Memory graphs
- Interactive interface
- Easy process management

---

# Find Memory-Intensive Processes

Using `ps`:

```bash
ps aux --sort=-%mem
```

Top memory consumers:

```bash
ps aux --sort=-rss | head
```

---

# View Process Memory Usage

Use:

```bash
pmap
```

Example:

```bash
pmap <PID>
```

Summary only.

```bash
pmap -x <PID>
```

---

# Monitor Swap Usage

Display swap.

```bash
swapon --show
```

Or:

```bash
free -h
```

Excessive swap usage often indicates memory pressure.

---

# Check OOM Events

The Linux kernel logs Out of Memory events.

View:

```bash
dmesg | grep -i oom
```

Or:

```bash
journalctl -k | grep -i oom
```

---

# Virtual Memory Statistics

Detailed information.

```bash
cat /proc/meminfo
```

Example:

```text
MemTotal

MemFree

Cached

Buffers

SwapTotal
```

---

# Common Commands

Memory usage.

```bash
free -h
```

Memory statistics.

```bash
vmstat
```

Process monitoring.

```bash
top
```

Largest memory consumers.

```bash
ps aux --sort=-%mem
```

Kernel OOM messages.

```bash
dmesg | grep -i oom
```

---

# Real Production Examples

Check available memory.

```bash
free -h
```

Monitor every second.

```bash
watch free -h
```

Find top memory consumers.

```bash
ps aux --sort=-rss | head
```

Check OOM events.

```bash
journalctl -k | grep -i oom
```

---

# Production Perspective

Memory monitoring is essential for:

- Kubernetes nodes
- Database servers
- Java applications
- Python services
- Web servers
- Cloud virtual machines
- CI/CD servers
- Enterprise applications

Memory exhaustion is one of the most common causes of application instability.

---

# Hands-on Lab

## Task 1

Display memory usage.

```bash
free -h
```

---

## Task 2

Refresh memory usage continuously.

```bash
watch free -h
```

---

## Task 3

Display virtual memory statistics.

```bash
vmstat 2
```

---

## Task 4

Open `top`.

```bash
top
```

Press:

```text
Shift + M
```

Sort by memory usage.

---

## Task 5

Identify the largest memory-consuming processes.

```bash
ps aux --sort=-%mem | head
```

---

## Task 6

Display detailed memory information.

```bash
cat /proc/meminfo
```

---

## Task 7

Display swap usage.

```bash
swapon --show
```

---

## Task 8

Search for Out of Memory events.

```bash
journalctl -k | grep -i oom
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `free -h` | Display memory usage | Capacity monitoring |
| `vmstat` | Virtual memory statistics | Performance analysis |
| `top` | Real-time process monitoring | Troubleshooting |
| `htop` | Interactive monitoring | System administration |
| `ps aux --sort=-%mem` | Largest memory consumers | Memory leak detection |
| `cat /proc/meminfo` | Detailed memory information | Low-level diagnostics |

---

# Common Memory Monitoring Mistakes

| Mistake | Solution |
|----------|----------|
| Focusing only on the `free` column | Monitor the `available` column as well |
| Ignoring swap usage | Investigate sustained swap activity |
| Never checking OOM events | Review kernel logs regularly |
| Looking only at total memory | Identify individual memory-consuming processes |
| Assuming high cache usage is always a problem | Linux uses available RAM efficiently for caching |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A production API server becomes slow.

Investigation:

```bash
free -h
```

Result:

```text
Available Memory

↓

Very Low
```

Next:

```bash
ps aux --sort=-rss | head
```

A Java process is consuming most of the RAM.

Further investigation confirms a memory leak.

After tuning the application and restarting the service:

```text
Memory Usage

↓

Normal

↓

Performance Restored
```

---

# Best Practices

- Monitor available memory instead of only free memory.
- Configure alerts before memory usage becomes critical.
- Monitor swap usage regularly.
- Investigate repeated OOM events immediately.
- Identify long-running memory-intensive processes.
- Monitor application memory trends over time.
- Combine memory monitoring with CPU and disk metrics.
- Use centralized monitoring tools such as Prometheus and Grafana for historical analysis.

---

# Common Mistakes

❌ Assuming low free memory always indicates a problem.

✅ Verify low free memory always indicates a problem instead of assuming it.

---

❌ Ignoring swap activity.

✅ Always review swap activity.

---

❌ Never checking kernel OOM events.

✅ Always checking kernel OOM events.

---

❌ Monitoring only total memory usage.

✅ Avoid this mistake: monitoring only total memory usage.

---

❌ Ignoring gradual memory growth that may indicate a memory leak.

✅ Always review gradual memory growth that may indicate a memory leak.

---

# Interview Questions
## Beginner

1. What does `free -h` display?
2. What is swap memory?
3. Which command displays virtual memory statistics?
4. What is the purpose of `vmstat`?

---

## Intermediate

1. What is the difference between `used`, `free`, and `available` memory?
2. How do you identify memory-intensive processes?
3. What causes Linux to use swap?
4. How do you investigate an OOM event?

---

## Architect Level

1. How would you monitor memory across hundreds of Linux servers?
2. How would you troubleshoot a Kubernetes node experiencing memory pressure?
3. How would you distinguish between normal cache usage and an application memory leak?

---

# Summary

In this lesson, you learned:

- Linux memory management
- RAM and swap monitoring
- Memory statistics
- Process memory analysis
- OOM event investigation
- Memory troubleshooting
- Performance monitoring
- Production best practices

Memory monitoring is a critical part of maintaining healthy Linux systems. By tracking RAM usage, swap activity, memory-intensive processes, and kernel OOM events, administrators can identify bottlenecks early, optimize application performance, and prevent production outages caused by memory exhaustion.

---

## Key Takeaways

- Use `free -h` to monitor memory utilization.
- Focus on the **available** memory column rather than only **free** memory.
- Monitor swap usage and investigate sustained swapping.
- Use `vmstat`, `top`, and `htop` for deeper analysis.
- Identify high-memory processes using `ps`.
- Review OOM events to diagnose memory-related failures.

---

## What's Next?

**[CPU Monitoring — Monitoring Processor Performance in Linux](cpu-monitoring.md)**

You'll explore:

- Understanding CPU utilization
- Monitoring CPU performance
- Load average
- Using `top`, `uptime`, `vmstat`, and related tools
- Identifying CPU-intensive processes
- Troubleshooting CPU bottlenecks
- Production CPU monitoring best practices

By the end of the lesson, you'll be able to monitor CPU performance, analyze system load, identify resource-intensive processes, and troubleshoot CPU-related performance issues in production Linux environments.
