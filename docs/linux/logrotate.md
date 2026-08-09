---
title: "logrotate — Managing and Rotating Log Files"
description: "Configure Linux logrotate — rotation schedules, compression, retention, custom rules, postrotate hooks, and production log management."
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
  - logrotate
  - disk-space
  - operations
  - rebash-linux-mastery
comments: false
status: ready
---

# logrotate — Managing and Rotating Log Files

> **logrotate** is a Linux utility that automatically manages log files by rotating, compressing, archiving, and removing old logs. Without log rotation, log files can grow indefinitely, consuming disk space and eventually causing applications or the operating system to fail. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, and Site Reliability Engineer (SRE) should understand how to configure `logrotate` to maintain healthy production systems and ensure long-term log management.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 12: Monitoring & Logs → Lesson 4</p>

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

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand log rotation
- Learn how `logrotate` works
- Configure rotation policies
- Compress archived logs
- Configure log retention
- Create custom rotation rules
- Test logrotate configurations
- Apply production logging best practices

---

# Prerequisites

Complete:

- Modules 1–11
- Module 12 Lessons 1–3

---

# Why Learn logrotate?

Imagine a busy production web server.

Without log rotation:

```text
Application Logs

↓

Grow Continuously

↓

Disk Full

↓

Application Failure
```

With `logrotate`:

```text
Application Logs

↓

Rotate Automatically

↓

Compress Old Logs

↓

Delete Expired Logs

↓

Healthy System
```

Proper log rotation prevents disk space issues while preserving valuable historical logs.

---

# What is logrotate?

`logrotate` is a utility that automatically manages log files.

It can:

- Rotate logs
- Compress old logs
- Archive logs
- Remove old logs
- Create new log files
- Execute scripts before or after rotation

---

# How logrotate Works

```text
Log File

↓

Rotation Policy

↓

Archive Old Log

↓

Compress

↓

Create New Log

↓

Continue Logging
```

Applications continue writing to the newly created log file.

---

# Default Configuration

Main configuration file:

```text
/etc/logrotate.conf
```

Application-specific configurations:

```text
/etc/logrotate.d/
```

Each application typically has its own configuration file.

---

# View Configuration

Display the main configuration.

```bash
cat /etc/logrotate.conf
```

List application configurations.

```bash
ls /etc/logrotate.d/
```

---

# Basic Configuration Example

```text
/var/log/myapp.log {

    weekly

    rotate 4

    compress

    missingok

    notifempty

}
```

Meaning:

- Rotate weekly
- Keep four archived logs
- Compress old logs
- Ignore missing logs
- Skip empty logs

---

# Rotation Frequency

Common options:

```text
daily

weekly

monthly

yearly
```

Example:

```text
weekly
```

Rotate once every week.

---

# Number of Rotations

Keep:

```text
rotate 7
```

Example:

```text
Current Log

↓

7 Archived Logs

↓

Older Logs Deleted
```

---

# Compression

Enable compression.

```text
compress
```

Compressed logs:

```text
app.log.1.gz

app.log.2.gz
```

Compression saves disk space.

---

# Delay Compression

```text
delaycompress
```

The most recently rotated log remains uncompressed until the next rotation.

Useful for applications that may continue writing briefly after rotation.

---

# Missing Logs

Ignore missing files.

```text
missingok
```

No error is generated if the log file does not exist.

---

# Skip Empty Logs

```text
notifempty
```

Do not rotate empty log files.

---

# Create New Log File

Automatically create a new log.

```text
create 640 root adm
```

Meaning:

- Permissions: `640`
- Owner: `root`
- Group: `adm`

---

# Rotate Based on Size

Rotate when a log reaches a specified size.

```text
size 100M
```

Rotate when the file reaches 100 MB.

---

# Maximum Size

Example:

```text
maxsize 500M
```

The log is rotated if it exceeds the specified maximum size.

---

# Execute Commands After Rotation

Example:

```text
postrotate

systemctl reload nginx

endscript
```

The application reloads after log rotation.

---

# Execute Commands Before Rotation

Example:

```text
prerotate

echo "Starting Rotation"

endscript
```

---

# Test Configuration

Validate configuration without rotating logs.

```bash
sudo logrotate -d /etc/logrotate.conf
```

Debug mode shows what would happen.

---

# Force Rotation

Immediately rotate logs.

```bash
sudo logrotate -f /etc/logrotate.conf
```

Useful for testing.

---

# Status File

`logrotate` tracks previous rotations.

Default:

```text
/var/lib/logrotate/status
```

---

# Automatic Scheduling

Most Linux distributions run `logrotate` automatically using:

- `cron`
- `systemd` timers

Administrators typically do not need to execute it manually.

---

# Common Commands

View configuration.

```bash
cat /etc/logrotate.conf
```

Debug configuration.

```bash
logrotate -d /etc/logrotate.conf
```

Force rotation.

```bash
logrotate -f /etc/logrotate.conf
```

View application rules.

```bash
ls /etc/logrotate.d/
```

---

# Real Production Examples

Rotate web server logs.

```text
weekly

rotate 8

compress
```

Rotate logs larger than 100 MB.

```text
size 100M
```

Reload service after rotation.

```text
postrotate

systemctl reload nginx

endscript
```

---

# Production Perspective

`logrotate` is essential for:

- Web servers
- Database servers
- Kubernetes nodes
- Cloud virtual machines
- CI/CD servers
- Security appliances
- Enterprise Linux systems
- Long-term log retention

Proper log management prevents disk exhaustion and preserves historical logs for troubleshooting and compliance.

---

# Hands-on Lab

## Task 1

View the main configuration.

```bash
cat /etc/logrotate.conf
```

---

## Task 2

List application configurations.

```bash
ls /etc/logrotate.d/
```

---

## Task 3

Review the configuration for an application such as Nginx or Apache.

```bash
cat /etc/logrotate.d/nginx
```

---

## Task 4

Run `logrotate` in debug mode.

```bash
sudo logrotate -d /etc/logrotate.conf
```

---

## Task 5

Force log rotation.

```bash
sudo logrotate -f /etc/logrotate.conf
```

---

## Task 6

Inspect the status file.

```bash
cat /var/lib/logrotate/status
```

---

## Task 7

Locate compressed log files.

```bash
ls /var/log/*.gz
```

---

## Task 8

Create a custom `logrotate` configuration for a test application and verify it using debug mode.

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `logrotate -d` | Debug configuration | Configuration testing |
| `logrotate -f` | Force rotation | Manual rotation |
| `cat /etc/logrotate.conf` | View global configuration | Administration |
| `ls /etc/logrotate.d/` | View application rules | Configuration review |
| `cat /var/lib/logrotate/status` | View rotation history | Troubleshooting |
| `gzip` | Compress archived logs | Storage optimization |

---

# Common logrotate Mistakes

| Mistake | Solution |
|----------|----------|
| Never rotating logs | Configure automatic rotation |
| Keeping logs forever | Define an appropriate retention policy |
| Forgetting compression | Enable `compress` |
| Never testing configurations | Use debug mode before deployment |
| Forgetting to reload services after rotation | Use `postrotate` scripts where required |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A production server reports:

```text
Disk Usage

↓

100%

↓

Applications Unable to Write Logs
```

Investigation:

```bash
du -sh /var/log/*
```

One application log has grown to 40 GB because log rotation was not configured.

Solution:

1. Configure `logrotate`.
2. Set weekly rotation.
3. Compress archived logs.
4. Retain only the required number of log files.
5. Verify automatic scheduling.

The server returns to normal operation with controlled log growth.

---

# Best Practices

- Rotate logs automatically.
- Compress archived logs to save disk space.
- Define an appropriate retention policy.
- Test new configurations using debug mode.
- Reload applications after rotation when necessary.
- Monitor disk usage regularly.
- Archive logs according to organizational retention requirements.
- Integrate log rotation with centralized logging solutions.

---

# Common Mistakes

❌ Allowing log files to grow without limits.

✅ Do not allow log files to grow without limits.

---

❌ Never compressing archived logs.

✅ Always compressing archived logs.

---

❌ Retaining logs indefinitely without a business requirement.

✅ Avoid this mistake: retaining logs indefinitely without a business requirement.

---

❌ Editing production configurations without testing.

✅ Edit production configurations without testing only when appropriate and with a backup.

---

❌ Forgetting to reload services after log rotation.

✅ Remember to to reload services after log rotation.

---

# Interview Questions
## Beginner

1. What is `logrotate`?
2. Why is log rotation important?
3. Where is the main `logrotate` configuration stored?
4. Which directive enables log compression?

---

## Intermediate

1. What is the difference between `compress` and `delaycompress`?
2. What does the `rotate` directive control?
3. How do you test a `logrotate` configuration?
4. What is the purpose of the `postrotate` section?

---

## Architect Level

1. How would you design log retention policies for enterprise applications?
2. How would you manage log rotation across thousands of Linux servers?
3. How would you integrate `logrotate` with centralized logging platforms?

---

# Summary

In this lesson, you learned:

- Log rotation fundamentals
- The `logrotate` utility
- Rotation schedules
- Compression and retention
- Custom rotation rules
- Testing configurations
- Automatic scheduling
- Production log management best practices

`logrotate` is an essential Linux utility for maintaining healthy systems by preventing log files from consuming excessive disk space. Proper log rotation ensures continuous application logging, preserves historical records for troubleshooting and compliance, and supports reliable long-term system operations.

---

## Key Takeaways

- `logrotate` automatically manages log files.
- Rotate logs regularly based on time or size.
- Compress archived logs to reduce disk usage.
- Use `logrotate -d` to validate configurations safely.
- Reload applications after rotation when necessary.
- Combine log rotation with centralized logging and monitoring for production environments.

---

## What's Next?

**[Disk Monitoring — Monitoring Storage Usage and Disk Health](disk-monitoring.md)**

You'll explore:

- Monitoring disk usage
- Understanding disk space and inode usage
- Using `df`, `du`, and related tools
- Identifying large files and directories
- Monitoring disk I/O
- Troubleshooting storage issues
- Production storage monitoring best practices

By the end of the lesson, you'll be able to monitor disk health, identify storage bottlenecks, manage disk capacity, and prevent storage-related outages in production Linux environments.
