---
title: "Crash Investigation — Diagnosing Linux System and Application Failures"
description: "Investigate Linux crashes — kernel panics, OOM events, core dumps, boot failures, journalctl, dmesg, and production incident investigation practices."
difficulty: advanced
estimated_time: "110 min"
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
  - crash
  - kernel-panic
  - oom
  - core-dump
  - incident-response
  - rebash-linux-mastery
comments: false
status: ready
---

# Crash Investigation — Diagnosing Linux System and Application Failures

> **Crash Investigation** is the process of identifying, analyzing, and resolving unexpected failures in Linux systems, applications, services, or the Linux kernel. Crashes can result from software bugs, hardware failures, resource exhaustion, kernel panics, filesystem corruption, or configuration issues. A structured crash investigation helps minimize downtime, identify the root cause, and prevent similar incidents in the future. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, and Site Reliability Engineer (SRE) should know how to investigate crashes in production environments.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 12: Monitoring & Logs → Lesson 9</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Advanced</div>

<div markdown>**Reading Time:** 110 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Monitoring & Logs</div>

<div markdown>**Lesson:** 9 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Linux system crashes
- Investigate application crashes
- Analyze kernel panics
- Understand core dumps
- Investigate boot failures
- Use crash investigation tools
- Perform root cause analysis
- Apply production incident investigation best practices

---

# Prerequisites

Complete:

- Modules 1–11
- Module 12 Lessons 1–8

---

# Why Learn Crash Investigation?

Imagine a production application.

Without investigation:

```text
Application Crashed

↓

Restart Service

↓

Crash Happens Again
```

With proper investigation:

```text
Application Crashed

↓

Collect Logs

↓

Analyze Evidence

↓

Find Root Cause

↓

Fix Problem

↓

Stable System
```

Understanding *why* a crash occurred is more valuable than simply restarting a service.

---

# What is a Crash?

A crash occurs when a system component unexpectedly stops functioning.

Examples:

- Application crash
- Service failure
- Kernel panic
- Operating system crash
- Hardware failure
- Filesystem corruption

---

# Common Causes of Crashes

Linux crashes commonly occur because of:

- Memory exhaustion
- Software bugs
- Invalid configuration
- Disk failures
- Hardware faults
- Filesystem corruption
- Driver failures
- Kernel bugs
- Resource exhaustion

---

# Crash Investigation Workflow

```text
Crash Occurs

↓

Collect Evidence

↓

Review Logs

↓

Analyze Metrics

↓

Identify Root Cause

↓

Implement Fix

↓

Validate Resolution
```

---

# Step 1: Check Service Status

Example:

```bash
systemctl status nginx
```

Look for:

- Failed state
- Exit code
- Error messages
- Restart attempts

---

# Step 2: Review System Logs

```bash
journalctl
```

Recent logs:

```bash
journalctl -n 100
```

Errors only:

```bash
journalctl -p err
```

---

# Step 3: Review Kernel Messages

```bash
dmesg
```

Kernel errors:

```bash
dmesg --level=err
```

---

# Step 4: Check Resource Usage

CPU:

```bash
top
```

Memory:

```bash
free -h
```

Disk:

```bash
df -h
```

Storage I/O:

```bash
iostat -x
```

---

# Step 5: Check for OOM Events

Applications may terminate when the Linux Out of Memory (OOM) Killer runs.

Search kernel logs.

```bash
dmesg | grep -i oom
```

Or:

```bash
journalctl -k | grep -i oom
```

Example:

```text
Out of Memory

↓

OOM Killer

↓

Process Terminated
```

---

# Step 6: Check Application Logs

Most applications maintain dedicated log files.

Examples:

```text
/var/log/nginx/

/var/log/httpd/

/var/log/mysql/

/var/log/postgresql/
```

Application logs often provide more detail than system logs.

---

# Kernel Panic

A **kernel panic** occurs when the Linux kernel encounters an unrecoverable error.

Example:

```text
Kernel

↓

Fatal Error

↓

Kernel Panic

↓

System Halt
```

Common causes:

- Faulty drivers
- Hardware failures
- Kernel bugs
- Corrupted memory
- Filesystem corruption

---

# Boot Failure Investigation

Review previous boot logs.

```bash
journalctl -b -1
```

Current boot:

```bash
journalctl -b
```

---

# Core Dumps

A **core dump** is a snapshot of an application's memory at the time of a crash.

It helps developers analyze:

- Call stack
- Variables
- Threads
- Memory state

---

# Enable Core Dumps

Check the current limit.

```bash
ulimit -c
```

Enable core dumps.

```bash
ulimit -c unlimited
```

---

# Analyze Core Dumps

Common tool:

```bash
gdb
```

Example:

```bash
gdb application core
```

Useful commands inside GDB:

```text
bt

info threads

quit
```

---

# Review Service Restart History

```bash
systemctl status service-name
```

Look for:

```text
Restart Count

↓

Repeated Failures
```

---

# Check Filesystem Health

For ext4:

```bash
sudo fsck /dev/sda1
```

Only run on an unmounted filesystem or in maintenance mode.

---

# Check Disk Health

```bash
smartctl -H /dev/sda
```

Detects hardware issues.

---

# Network-Related Crashes

Verify connectivity.

```bash
ping
```

Listening ports.

```bash
ss -tuln
```

---

# Common Commands

System logs.

```bash
journalctl
```

Kernel messages.

```bash
dmesg
```

Service status.

```bash
systemctl status
```

Memory.

```bash
free -h
```

Core dumps.

```bash
gdb
```

---

# Real Production Examples

Check previous boot.

```bash
journalctl -b -1
```

View kernel errors.

```bash
dmesg --level=err
```

Check OOM events.

```bash
journalctl -k | grep -i oom
```

Verify service status.

```bash
systemctl status nginx
```

---

# Production Perspective

Crash investigation is critical for:

- Cloud infrastructure
- Kubernetes clusters
- Database servers
- Enterprise Linux
- API services
- Web servers
- Financial systems
- High-availability platforms

A structured investigation reduces Mean Time to Resolution (MTTR) and improves system reliability.

---

# Hands-on Lab

## Task 1

Check the status of a system service.

```bash
systemctl status ssh
```

or

```bash
systemctl status sshd
```

---

## Task 2

Review the latest system logs.

```bash
journalctl -n 100
```

---

## Task 3

Display kernel errors.

```bash
dmesg --level=err
```

---

## Task 4

Search for OOM events.

```bash
journalctl -k | grep -i oom
```

---

## Task 5

Check memory usage.

```bash
free -h
```

---

## Task 6

Review the previous boot logs.

```bash
journalctl -b -1
```

---

## Task 7

Check whether core dumps are enabled.

```bash
ulimit -c
```

---

## Task 8

Create a crash investigation report that includes:

- Service status
- System logs
- Kernel messages
- Memory usage
- Disk usage
- CPU usage
- OOM events
- Root cause
- Resolution steps

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `journalctl` | Review system logs | Incident investigation |
| `dmesg` | View kernel messages | Hardware diagnostics |
| `systemctl status` | Check service health | Service troubleshooting |
| `free -h` | Review memory usage | OOM investigation |
| `gdb` | Analyze core dumps | Application debugging |
| `journalctl -b -1` | Review previous boot | Boot failure analysis |

---

# Common Crash Investigation Mistakes

| Mistake | Solution |
|----------|----------|
| Restarting services immediately | Collect logs first |
| Ignoring kernel messages | Review `dmesg` and kernel journal |
| Deleting logs before analysis | Preserve evidence |
| Investigating only one component | Review CPU, memory, disk, network, and applications |
| Fixing symptoms instead of the root cause | Perform structured root cause analysis |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A production Java application crashes repeatedly.

Investigation:

```bash
systemctl status application
```

Shows repeated failures.

Next:

```bash
journalctl -u application
```

Application logs show:

```text
OutOfMemoryError
```

Further investigation:

```bash
free -h
```

Available memory is nearly exhausted.

Kernel logs:

```bash
journalctl -k | grep -i oom
```

Confirm the OOM Killer terminated the Java process.

Resolution:

- Increase application heap size appropriately.
- Optimize memory usage.
- Add system memory if required.
- Configure monitoring and alerts for memory pressure.

The application remains stable after remediation.

---

# Best Practices

- Preserve logs before restarting services.
- Investigate both system and application logs.
- Collect CPU, memory, disk, and network metrics.
- Review previous boot logs after system crashes.
- Enable core dumps for critical applications when appropriate.
- Document investigation findings and corrective actions.
- Perform post-incident reviews to prevent recurrence.
- Automate monitoring and alerting for critical resources.

---

# Common Mistakes

❌ Restarting systems before collecting evidence.

✅ Avoid this mistake: restarting systems before collecting evidence.

---

❌ Ignoring application logs.

✅ Always review application logs.

---

❌ Never checking kernel messages.

✅ Always checking kernel messages.

---

❌ Assuming every crash has the same cause.

✅ Verify every crash has the same cause instead of assuming it.

---

❌ Failing to document investigation results.

✅ Avoid this mistake: failing to document investigation results.

---

# Interview Questions
## Beginner

1. What is a crash investigation?
2. What is a kernel panic?
3. Which command displays kernel messages?
4. How do you review previous boot logs?

---

## Intermediate

1. How would you investigate a repeatedly crashing Linux service?
2. What is a core dump?
3. How do you identify an OOM event?
4. Which logs should be reviewed during an application crash?

---

## Architect Level

1. How would you build an enterprise incident response workflow for Linux crashes?
2. How would you reduce MTTR during production incidents?
3. How would you combine monitoring, logging, and core dump analysis to improve reliability?

---

# Summary

In this lesson, you learned:

- Crash investigation fundamentals
- Service failure analysis
- Kernel panic investigation
- Core dumps
- Boot failure analysis
- OOM investigation
- Root cause analysis
- Production incident response best practices

Crash investigation is a critical operational skill for Linux administrators. By systematically collecting evidence, reviewing logs, analyzing system resources, and identifying the root cause, administrators can restore services quickly, prevent recurring failures, and improve the reliability of production environments.

---

## Key Takeaways

- Always collect evidence before restarting services.
- Review both system and application logs.
- Investigate kernel messages and OOM events.
- Use core dumps for application crash analysis.
- Perform structured root cause analysis.
- Document findings and preventive actions after every significant incident.

---

## What's Next?

**[Monitoring Best Practices — Building Reliable Linux Monitoring Strategies](monitoring-best-practices.md)**

You'll explore:

- Building an effective monitoring strategy
- Selecting key performance indicators (KPIs)
- Configuring alerts and thresholds
- Centralized monitoring
- Monitoring dashboards
- Capacity planning
- Production monitoring best practices

By the end of the lesson, you'll understand how to design a comprehensive monitoring strategy that improves system reliability, reduces downtime, and supports proactive operations in production Linux environments.
