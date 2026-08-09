---
title: "syslog — Traditional Linux System Logging"
description: "Understand Linux syslog — rsyslog, common log files, facilities, severity levels, searching logs, and centralized logging practices."
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
  - syslog
  - rsyslog
  - troubleshooting
  - rebash-linux-mastery
comments: false
status: ready
---

# syslog — Traditional Linux System Logging

> **syslog** is the traditional logging system used by Linux and Unix operating systems to collect, categorize, store, and forward log messages from the kernel, operating system, services, and applications. While many modern Linux distributions use **systemd-journald**, syslog remains widely used in enterprise environments for centralized logging, log forwarding, compliance, and long-term log retention. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, and Site Reliability Engineer (SRE) should understand how syslog works and how to analyze syslog data.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 12: Monitoring & Logs → Lesson 2</p>

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

<div markdown>**Lesson:** 2 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the syslog architecture
- Learn how Linux logging works
- Identify common log files
- Understand facilities and severity levels
- Search and filter syslog entries
- Configure centralized logging
- Troubleshoot production issues
- Apply logging best practices

---

# Prerequisites

Complete:

- Modules 1–11
- Module 12 Lesson 1 – journalctl

---

# Why Learn syslog?

Imagine a production application crashes.

Without logs:

```text
Application Failed

↓

Unknown Cause

↓

Extended Downtime
```

With syslog:

```text
Application Failed

↓

Log Entry

↓

Root Cause Found

↓

Service Restored
```

System logs provide valuable information for troubleshooting and security investigations.

---

# What is syslog?

Syslog is a standardized logging system that collects messages from:

- Linux kernel
- System services
- Applications
- Network devices
- Security software
- User processes

These messages are stored locally or forwarded to remote log servers.

---

# How syslog Works

```text
Applications

↓

syslog Service

↓

Log Files

↓

Administrator
```

Or

```text
Applications

↓

syslog Service

↓

Remote Log Server
```

---

# Common syslog Implementations

Several syslog implementations are available.

Most common:

- rsyslog
- syslog-ng

Many Linux distributions use **rsyslog** by default.

---

# Common Log Files

Depending on the Linux distribution:

| Log File | Purpose |
|----------|----------|
| `/var/log/syslog` | General system log (Ubuntu/Debian) |
| `/var/log/messages` | General system log (RHEL-based systems) |
| `/var/log/auth.log` | Authentication logs (Ubuntu/Debian) |
| `/var/log/secure` | Authentication logs (RHEL-based systems) |
| `/var/log/kern.log` | Kernel messages |
| `/var/log/cron` | Scheduled job logs |
| `/var/log/boot.log` | Boot messages |

---

# Viewing Log Files

Display an entire log.

```bash
cat /var/log/syslog
```

Better option:

```bash
less /var/log/syslog
```

---

# View Recent Entries

```bash
tail /var/log/syslog
```

View the last 20 lines.

```bash
tail -n 20 /var/log/syslog
```

---

# Monitor Logs in Real Time

```bash
tail -f /var/log/syslog
```

Useful while troubleshooting running applications.

---

# Search Log Entries

Use:

```bash
grep
```

Example:

```bash
grep ssh /var/log/syslog
```

Search for errors.

```bash
grep ERROR /var/log/syslog
```

---

# Facilities

A **facility** identifies the source of a log message.

Common facilities:

| Facility | Description |
|----------|-------------|
| `auth` | Authentication |
| `authpriv` | Private authentication |
| `daemon` | System services |
| `kern` | Kernel |
| `mail` | Mail services |
| `cron` | Scheduled jobs |
| `user` | User applications |
| `local0-local7` | Custom applications |

---

# Severity Levels

Syslog assigns a priority to each message.

| Level | Meaning |
|--------|----------|
| Emergency | System unusable |
| Alert | Immediate action required |
| Critical | Critical condition |
| Error | Error occurred |
| Warning | Warning |
| Notice | Important informational event |
| Info | Informational |
| Debug | Debugging details |

Severity helps administrators prioritize issues.

---

# rsyslog Configuration

Main configuration file:

```text
/etc/rsyslog.conf
```

Additional configuration:

```text
/etc/rsyslog.d/
```

After changes:

```bash
sudo systemctl restart rsyslog
```

---

# Check syslog Service

Ubuntu/Debian:

```bash
systemctl status rsyslog
```

RHEL-based systems:

```bash
systemctl status rsyslog
```

---

# Centralized Logging

Instead of storing logs on every server:

```text
Server A

↓

Server B

↓

Server C

↓

Central Log Server
```

Benefits:

- Easier troubleshooting
- Security monitoring
- Compliance
- Long-term storage

---

# Log Rotation

Syslog files continuously grow.

Linux uses:

```text
logrotate
```

to archive, compress, and remove old logs.

(This topic is covered in the next lesson.)

---

# Common Commands

View logs.

```bash
less /var/log/syslog
```

Monitor logs.

```bash
tail -f /var/log/syslog
```

Search logs.

```bash
grep ssh /var/log/syslog
```

Check service.

```bash
systemctl status rsyslog
```

Restart service.

```bash
sudo systemctl restart rsyslog
```

---

# Real Production Examples

Monitor authentication logs.

Ubuntu:

```bash
tail -f /var/log/auth.log
```

RHEL:

```bash
tail -f /var/log/secure
```

Search SSH activity.

```bash
grep ssh /var/log/syslog
```

Monitor cron jobs.

```bash
tail -f /var/log/cron
```

---

# Production Perspective

Syslog remains important for:

- Enterprise Linux
- Cloud virtual machines
- Security monitoring
- Compliance reporting
- SIEM integration
- Centralized logging
- Application troubleshooting
- Infrastructure monitoring

Many organizations forward syslog messages to centralized platforms such as Splunk, ELK Stack, Graylog, or cloud logging services.

---

# Hands-on Lab

## Task 1

View the system log.

Ubuntu:

```bash
less /var/log/syslog
```

RHEL:

```bash
less /var/log/messages
```

---

## Task 2

Display the last 20 log entries.

```bash
tail -n 20 /var/log/syslog
```

---

## Task 3

Monitor logs in real time.

```bash
tail -f /var/log/syslog
```

---

## Task 4

Search for SSH log entries.

```bash
grep ssh /var/log/syslog
```

---

## Task 5

View authentication logs.

Ubuntu:

```bash
less /var/log/auth.log
```

RHEL:

```bash
less /var/log/secure
```

---

## Task 6

Check the rsyslog service.

```bash
systemctl status rsyslog
```

---

## Task 7

Locate the rsyslog configuration file.

```bash
ls /etc/rsyslog.conf
```

---

## Task 8

Restart rsyslog.

```bash
sudo systemctl restart rsyslog
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `less` | View log files | Log analysis |
| `tail -f` | Monitor logs | Live troubleshooting |
| `grep` | Search log entries | Error investigation |
| `systemctl status rsyslog` | Check logging service | Service verification |
| `systemctl restart rsyslog` | Reload configuration | Apply changes |
| `cat` | Display log contents | Quick inspection |

---

# Common syslog Mistakes

| Mistake | Solution |
|----------|----------|
| Ignoring authentication logs | Review login activity regularly |
| Allowing logs to consume all disk space | Configure log rotation |
| Storing logs only locally | Forward logs to a centralized server |
| Never reviewing error messages | Monitor logs proactively |
| Editing configuration without testing | Validate and restart the service carefully |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    Users report intermittent SSH login failures.

Investigation:

```bash
grep ssh /var/log/auth.log
```

The log shows:

```text
Authentication Failure

↓

Incorrect Password

↓

Repeated Attempts
```

The administrator identifies the issue, verifies whether the attempts are legitimate, and confirms that Fail2Ban is blocking malicious IP addresses.

---

# Best Practices

- Monitor logs regularly.
- Forward logs to a centralized logging platform.
- Protect log files from unauthorized modification.
- Configure log rotation to manage disk usage.
- Review authentication and security logs daily.
- Use consistent timestamps across servers with NTP or Chrony.
- Restrict access to sensitive log files.

---

# Common Mistakes

❌ Never reviewing authentication logs.

✅ Always reviewing authentication logs.

---

❌ Allowing log files to fill the filesystem.

✅ Do not allow log files to fill the filesystem.

---

❌ Storing logs only on local servers.

✅ Avoid this mistake: storing logs only on local servers.

---

❌ Ignoring repeated warning messages.

✅ Always review repeated warning messages.

---

❌ Deleting logs before completing an investigation.

✅ Do not delete logs before completing an investigation until it is safe to do so.

---

# Interview Questions
## Beginner

1. What is syslog?
2. Where are system logs commonly stored?
3. Which command displays the end of a log file?
4. What is rsyslog?

---

## Intermediate

1. What is the difference between a facility and a severity level?
2. How do you monitor a log file in real time?
3. Why is centralized logging important?
4. Which files store authentication logs on Ubuntu and RHEL?

---

## Architect Level

1. How would you design centralized logging for hundreds of Linux servers?
2. How would you integrate syslog with a SIEM platform?
3. How would you ensure log integrity and long-term retention in an enterprise environment?

---

# Summary

In this lesson, you learned:

- Syslog fundamentals
- Syslog architecture
- Common log files
- Facilities and severity levels
- Searching and monitoring logs
- Centralized logging
- rsyslog configuration
- Production logging best practices

Syslog remains a core component of Linux logging infrastructure. Understanding how log messages are collected, categorized, stored, and forwarded enables administrators to troubleshoot issues, investigate security incidents, support compliance, and maintain reliable production environments.

---

## Key Takeaways

- Syslog collects logs from the operating system, services, and applications.
- Learn the purpose of common log files such as `/var/log/syslog` and `/var/log/messages`.
- Use `tail -f` and `grep` to monitor and search logs efficiently.
- Protect logs and configure log rotation.
- Forward logs to centralized logging systems for monitoring and compliance.
- Combine syslog with `journalctl` for comprehensive Linux troubleshooting.

---

## What's Next?

**[dmesg — Viewing Linux Kernel Messages](dmesg.md)**

You'll explore:

- What `dmesg` is
- Understanding kernel messages
- Hardware detection
- Driver initialization
- Boot diagnostics
- Troubleshooting hardware issues
- Production debugging techniques

By the end of the lesson, you'll be able to use `dmesg` to investigate kernel events, diagnose hardware problems, troubleshoot driver issues, and analyze Linux system startup behavior.
