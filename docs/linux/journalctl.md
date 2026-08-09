---
title: "journalctl — Viewing and Analyzing System Logs"
description: "Use journalctl to query systemd journal logs — filter by service, boot, time, and priority, follow live logs, and manage journal retention."
difficulty: intermediate
estimated_time: "90 min"
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
  - logging
  - journalctl
  - systemd
  - troubleshooting
  - rebash-linux-mastery
comments: false
status: ready
---

# journalctl — Viewing and Analyzing System Logs

> **journalctl** is the command-line utility used to view logs collected by **systemd-journald**. It provides a centralized way to access system logs, kernel messages, service logs, boot logs, authentication events, and application logs. Unlike traditional log files stored in `/var/log`, the systemd journal collects logs from multiple sources into a searchable database. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, and Site Reliability Engineer (SRE) should know how to use `journalctl` to troubleshoot production systems.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 12: Monitoring & Logs → Lesson 1</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Monitoring & Logs</div>

<div markdown>**Lesson:** 1 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand systemd journaling
- View system logs
- Filter logs efficiently
- Search logs by service
- View boot logs
- Monitor logs in real time
- Export journal data
- Apply production troubleshooting techniques

---

# Prerequisites

Complete:

- Modules 1–11

---

# Why Learn journalctl?

Imagine a production web server suddenly stops responding.

Without logs:

```text
Application Failed

↓

Unknown Cause

↓

Long Downtime
```

With `journalctl`:

```text
Application Failed

↓

journalctl

↓

Error Identified

↓

Problem Fixed
```

Logs provide the information needed to quickly identify and resolve problems.

---

# What is systemd-journald?

`systemd-journald` is the logging service provided by **systemd**.

It collects logs from:

- Kernel
- System services
- Applications
- User processes
- Boot events
- Authentication services

These logs are stored in the **systemd journal**.

---

# What is journalctl?

`journalctl` is the utility used to read and search the systemd journal.

It allows administrators to:

- View logs
- Search logs
- Filter logs
- Monitor logs
- Troubleshoot services

---

# View All Logs

Display the complete journal.

```bash
journalctl
```

Because the journal can be very large, output is displayed using a pager.

---

# View Recent Logs

Display the latest entries.

```bash
journalctl -n 20
```

Example:

```text
Last 20 log entries
```

---

# Follow Logs in Real Time

Similar to:

```bash
tail -f
```

Command:

```bash
journalctl -f
```

Useful while troubleshooting running applications.

---

# View Logs for a Service

Example:

```bash
journalctl -u nginx
```

Another example:

```bash
journalctl -u ssh
```

or

```bash
journalctl -u sshd
```

(depending on the Linux distribution)

---

# View Current Boot Logs

```bash
journalctl -b
```

Displays logs generated since the current system boot.

---

# View Previous Boot Logs

List available boots.

```bash
journalctl --list-boots
```

View the previous boot.

```bash
journalctl -b -1
```

---

# Filter by Time

View logs since a specific time.

```bash
journalctl --since "1 hour ago"
```

Example:

```bash
journalctl --since "today"
```

View logs between two times.

```bash
journalctl --since "09:00" --until "10:00"
```

---

# Filter by Priority

View only error messages.

```bash
journalctl -p err
```

Common priorities:

| Priority | Description |
|----------|-------------|
| `emerg` | System unusable |
| `alert` | Immediate action required |
| `crit` | Critical condition |
| `err` | Error |
| `warning` | Warning |
| `notice` | Normal but significant |
| `info` | Informational |
| `debug` | Debugging |

---

# View Kernel Messages

```bash
journalctl -k
```

Useful for hardware and driver troubleshooting.

---

# View Logs for a Process

Search by process ID.

```bash
journalctl _PID=1234
```

---

# View User Logs

Display logs for the current user.

```bash
journalctl --user
```

---

# Disable the Pager

Print directly to the terminal.

```bash
journalctl --no-pager
```

---

# Export Logs

Save logs to a file.

```bash
journalctl > system.log
```

---

# Disk Usage

Check journal size.

```bash
journalctl --disk-usage
```

Example:

```text
Archived and active journals take up 250M.
```

---

# Clean Old Logs

Keep only recent logs.

```bash
sudo journalctl --vacuum-time=7d
```

Or limit by size.

```bash
sudo journalctl --vacuum-size=500M
```

---

# Common Commands

View logs.

```bash
journalctl
```

Follow logs.

```bash
journalctl -f
```

View service logs.

```bash
journalctl -u nginx
```

Current boot.

```bash
journalctl -b
```

View errors.

```bash
journalctl -p err
```

---

# Real Production Examples

Check failed SSH logins.

```bash
journalctl -u ssh
```

Monitor Kubernetes service.

```bash
journalctl -u kubelet -f
```

Investigate boot problems.

```bash
journalctl -b
```

View system errors.

```bash
journalctl -p err
```

---

# Production Perspective

`journalctl` is used daily for:

- Linux troubleshooting
- Service debugging
- Kubernetes node analysis
- Cloud server monitoring
- Security investigations
- Boot failure analysis
- Production incident response
- System health monitoring

It is one of the most important troubleshooting tools on modern Linux systems.

---

# Hands-on Lab

## Task 1

Display the entire journal.

```bash
journalctl
```

---

## Task 2

Display the latest 20 log entries.

```bash
journalctl -n 20
```

---

## Task 3

Monitor logs in real time.

```bash
journalctl -f
```

---

## Task 4

View logs for the SSH service.

```bash
journalctl -u ssh
```

or

```bash
journalctl -u sshd
```

---

## Task 5

Display logs from the current boot.

```bash
journalctl -b
```

---

## Task 6

View only error messages.

```bash
journalctl -p err
```

---

## Task 7

Check journal disk usage.

```bash
journalctl --disk-usage
```

---

## Task 8

Remove journal entries older than seven days.

```bash
sudo journalctl --vacuum-time=7d
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `journalctl` | View all logs | Troubleshooting |
| `journalctl -f` | Follow logs | Live monitoring |
| `journalctl -u` | Service logs | Application debugging |
| `journalctl -b` | Boot logs | Startup troubleshooting |
| `journalctl -p err` | Error logs | Incident analysis |
| `journalctl --disk-usage` | Check journal size | Storage management |

---

# Common journalctl Mistakes

| Mistake | Solution |
|----------|----------|
| Viewing all logs without filters | Use time or service filters |
| Ignoring previous boot logs | Check `-b -1` |
| Not monitoring logs during troubleshooting | Use `-f` |
| Allowing journal files to grow indefinitely | Configure retention and vacuum old logs |
| Looking only at application logs | Review system and kernel logs as well |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A production web server fails immediately after a reboot.

Investigation:

```bash
journalctl -b
```

The logs show:

```text
nginx.service

↓

Configuration Error

↓

Startup Failed
```

The administrator corrects the configuration, restarts the service, and confirms success using:

```bash
journalctl -u nginx
```

The service starts successfully, minimizing downtime.

---

# Best Practices

- Filter logs by service, boot, or time.
- Monitor logs in real time during troubleshooting.
- Review error-level logs first during incidents.
- Configure journal retention to control disk usage.
- Archive important logs before cleanup.
- Restrict access to logs because they may contain sensitive information.
- Use `journalctl` together with application logs for complete troubleshooting.

---

# Common Mistakes

❌ Searching the entire journal instead of filtering results.

✅ Prefer filtering results rather than searching the entire journal.

---

❌ Ignoring boot logs after startup failures.

✅ Always review boot logs after startup failures.

---

❌ Allowing journals to consume excessive disk space.

✅ Do not allow journals to consume excessive disk space.

---

❌ Deleting logs before completing an investigation.

✅ Do not delete logs before completing an investigation until it is safe to do so.

---

❌ Assuming all applications write only to traditional log files.

✅ Verify all applications write only to traditional log files instead of assuming it.

---

# Interview Questions
## Beginner

1. What is `journalctl`?
2. What is `systemd-journald`?
3. Which command displays the current boot logs?
4. How do you follow logs in real time?

---

## Intermediate

1. How do you display logs for a specific service?
2. How do you filter logs by time?
3. What does `journalctl -p err` display?
4. How do you check journal disk usage?

---

## Architect Level

1. How would you troubleshoot a production service using `journalctl`?
2. How would you manage journal retention across hundreds of Linux servers?
3. How would you integrate `journalctl` logs with centralized logging platforms?

---

# Summary

In this lesson, you learned:

- systemd journal fundamentals
- Viewing logs with `journalctl`
- Filtering logs
- Monitoring services
- Boot log analysis
- Real-time log monitoring
- Journal maintenance
- Production troubleshooting best practices

`journalctl` is the primary tool for viewing and analyzing logs on modern Linux systems that use systemd. It provides powerful filtering, searching, and monitoring capabilities that enable administrators to diagnose service failures, investigate system events, analyze boot problems, and maintain healthy production environments.

---

## Key Takeaways

- `journalctl` provides centralized access to systemd journal logs.
- Use filters such as service name, time, boot, and priority to narrow results.
- Monitor logs in real time using `journalctl -f`.
- Review previous boot logs when troubleshooting startup issues.
- Manage journal storage with retention and cleanup options.
- Make `journalctl` a core part of your Linux troubleshooting workflow.

---

## What's Next?

**[syslog — Traditional Linux System Logging](syslog.md)**

You'll explore:

- What syslog is
- Syslog architecture
- Common log files
- Syslog facilities and priorities
- Viewing and searching syslog entries
- Centralized logging
- Production logging best practices

By the end of the lesson, you'll understand how traditional Linux syslog works, how it complements the systemd journal, and how to use syslog for monitoring, troubleshooting, and centralized log management.
