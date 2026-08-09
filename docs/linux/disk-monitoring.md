---
title: "Disk Monitoring — Monitoring Storage Usage and Disk Health"
description: "Monitor Linux disk usage — df, du, inodes, iostat, SMART health, large-file cleanup, and production storage capacity practices."
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
  - disk
  - storage
  - df
  - iostat
  - rebash-linux-mastery
comments: false
status: ready
---

# Disk Monitoring — Monitoring Storage Usage and Disk Health

> **Disk Monitoring** is the process of tracking disk space, filesystem usage, inode consumption, disk I/O performance, and storage health to ensure Linux systems continue operating reliably. Running out of disk space or experiencing storage performance issues can cause application failures, database corruption, logging problems, and even system crashes. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, and Site Reliability Engineer (SRE) should know how to monitor storage resources proactively in production environments.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 12: Monitoring & Logs → Lesson 5</p>

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

<div markdown>**Lesson:** 5 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Monitor disk space usage
- Analyze filesystem utilization
- Monitor inode usage
- Identify large files and directories
- Understand disk I/O
- Monitor storage performance
- Troubleshoot disk space issues
- Apply production monitoring best practices

---

# Prerequisites

Complete:

- Modules 1–11
- Module 12 Lessons 1–4

---

# Why Learn Disk Monitoring?

Imagine a production database server.

Without monitoring:

```text
Disk Becomes Full

↓

Database Stops Writing

↓

Application Failure

↓

Downtime
```

With proactive monitoring:

```text
Disk Usage

↓

Alert at 80%

↓

Cleanup or Expand Storage

↓

No Downtime
```

Monitoring storage prevents many production outages.

---

# What is Disk Monitoring?

Disk monitoring involves tracking:

- Disk capacity
- Filesystem usage
- Inode usage
- Disk I/O
- Storage performance
- Disk health
- Storage growth

---

# Disk Monitoring Architecture

```text
Disk

↓

Filesystem

↓

Linux Monitoring Tools

↓

Administrator

↓

Corrective Action
```

---

# Check Disk Space

The most common command:

```bash
df -h
```

Example:

```text
Filesystem      Size Used Avail Use%

/dev/sda2       100G 60G 40G 60%
```

Options:

- `-h` → Human-readable
- `-T` → Display filesystem type

---

# Check Filesystem Types

```bash
df -Th
```

Example:

```text
ext4

xfs
```

---

# Monitor Inode Usage

Sometimes disk space is available, but no new files can be created because all inodes are used.

Check inode usage:

```bash
df -i
```

Example:

```text
IUsed

IFree

IUse%
```

---

# Find Large Directories

Use:

```bash
du -sh /*
```

Check a specific directory.

```bash
du -sh /var/*
```

Example:

```text
15G /var/log
```

---

# Find Large Files

Example:

```bash
find / -type f -size +500M
```

Find files larger than 500 MB.

---

# Sort Directory Sizes

```bash
du -ah /var | sort -rh | head -20
```

Shows the largest files and directories first.

---

# Check Mounted Filesystems

```bash
mount
```

Or:

```bash
findmnt
```

Useful for verifying storage mounts.

---

# Disk Usage by Filesystem

```bash
lsblk
```

Example:

```text
Disk

↓

Partition

↓

Mount Point
```

Display filesystem information.

```bash
lsblk -f
```

---

# Monitor Disk I/O

Install `sysstat` if needed.

```bash
iostat
```

Extended statistics.

```bash
iostat -x
```

Shows:

- Read operations
- Write operations
- Utilization
- Wait times

---

# Monitor Real-Time I/O

```bash
iotop
```

Displays processes performing disk I/O.

Requires root privileges on many systems.

---

# Check Open Files

Sometimes a deleted file still consumes disk space because a process keeps it open.

View open files.

```bash
lsof
```

Deleted files:

```bash
lsof | grep deleted
```

---

# Check Disk Usage of a Directory

```bash
du -sh /home
```

Human-readable summary.

---

# Check Available Space

```bash
df -h /
```

Monitor the root filesystem regularly.

---

# Filesystem Health

For ext4 filesystems:

```bash
sudo fsck /dev/sda1
```

!!! warning "Warning"

    Run `fsck` only on unmounted filesystems or in maintenance mode unless the filesystem specifically supports online checking.

For XFS:

```bash
xfs_repair
```

Run only on an unmounted filesystem unless instructed otherwise.

---

# SMART Disk Health

Install SMART tools.

```bash
smartctl -H /dev/sda
```

Displays disk health.

Detailed information.

```bash
smartctl -a /dev/sda
```

Requires:

```text
smartmontools
```

---

# Common Commands

Check disk space.

```bash
df -h
```

Directory usage.

```bash
du -sh
```

Monitor inodes.

```bash
df -i
```

Largest files.

```bash
find / -size +500M
```

Disk I/O.

```bash
iostat -x
```

---

# Real Production Examples

Check root filesystem.

```bash
df -h /
```

Find large log files.

```bash
find /var/log -type f -size +100M
```

Monitor I/O.

```bash
iostat -x
```

View deleted open files.

```bash
lsof | grep deleted
```

---

# Production Perspective

Disk monitoring is essential for:

- Database servers
- Kubernetes nodes
- Web servers
- Logging servers
- CI/CD systems
- Virtual machines
- Cloud infrastructure
- Enterprise storage systems

Storage issues are among the most common causes of production outages.

---

# Hands-on Lab

## Task 1

Check filesystem usage.

```bash
df -h
```

---

## Task 2

Check inode usage.

```bash
df -i
```

---

## Task 3

Display the largest directories under `/var`.

```bash
du -sh /var/*
```

---

## Task 4

Find files larger than 500 MB.

```bash
find / -type f -size +500M
```

---

## Task 5

Display mounted filesystems.

```bash
findmnt
```

---

## Task 6

Display block devices.

```bash
lsblk -f
```

---

## Task 7

Monitor disk I/O.

```bash
iostat -x
```

---

## Task 8

Check disk SMART health (if supported).

```bash
smartctl -H /dev/sda
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `df -h` | Display filesystem usage | Capacity planning |
| `du -sh` | Directory usage | Storage analysis |
| `df -i` | Monitor inode usage | Filesystem troubleshooting |
| `find` | Locate large files | Disk cleanup |
| `iostat -x` | Monitor disk I/O | Performance analysis |
| `smartctl` | Check disk health | Hardware monitoring |

---

# Common Disk Monitoring Mistakes

| Mistake | Solution |
|----------|----------|
| Monitoring only disk space | Monitor inode usage and I/O as well |
| Ignoring log growth | Configure log rotation |
| Never checking disk health | Monitor SMART status |
| Waiting until disks are full | Configure alerts before capacity limits |
| Deleting files without checking open file handles | Use `lsof` to verify deleted files are not still in use |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A production application reports:

```text
No Space Left on Device
```

Investigation:

```bash
df -h
```

Disk usage:

```text
100%
```

Next:

```bash
du -sh /var/*
```

Findings:

```text
/var/log

↓

Large Log Files
```

The administrator archives old logs, verifies `logrotate` is functioning correctly, and restores normal disk usage.

---

# Best Practices

- Monitor disk space continuously.
- Configure alerts before disks become full (for example, at 80% usage).
- Monitor inode usage in addition to disk capacity.
- Rotate and archive logs regularly.
- Review disk I/O performance.
- Monitor SMART health for physical disks.
- Plan storage expansion before capacity limits are reached.
- Include storage monitoring in centralized monitoring platforms such as Prometheus and Grafana.

---

# Common Mistakes

❌ Monitoring only available disk space.

✅ Avoid this mistake: monitoring only available disk space.

---

❌ Ignoring inode exhaustion.

✅ Always review inode exhaustion.

---

❌ Never reviewing disk I/O performance.

✅ Always reviewing disk I/O performance.

---

❌ Allowing log files to consume all available storage.

✅ Do not allow log files to consume all available storage.

---

❌ Ignoring SMART warnings from storage devices.

✅ Always review SMART warnings from storage devices.

---

# Interview Questions
## Beginner

1. What does `df -h` display?
2. What is the difference between `df` and `du`?
3. Why are inodes important?
4. Which command lists mounted filesystems?

---

## Intermediate

1. How do you identify large files consuming disk space?
2. What information does `iostat -x` provide?
3. Why can "No space left on device" occur even when free disk space exists?
4. How do you check whether deleted files are still open?

---

## Architect Level

1. How would you monitor storage across hundreds of Linux servers?
2. How would you design alert thresholds for production storage monitoring?
3. How would you troubleshoot a Kubernetes node experiencing high disk I/O?

---

# Summary

In this lesson, you learned:

- Disk space monitoring
- Filesystem usage
- Inode monitoring
- Large file identification
- Disk I/O analysis
- Filesystem health
- SMART monitoring
- Production storage monitoring best practices

Disk monitoring is essential for maintaining healthy Linux systems. By continuously monitoring storage capacity, inode utilization, disk performance, and hardware health, administrators can prevent outages, improve performance, and ensure reliable operation of production workloads.

---

## Key Takeaways

- Use `df -h` to monitor filesystem capacity.
- Use `du` to identify large directories and files.
- Monitor inode usage with `df -i`.
- Analyze disk performance using `iostat`.
- Monitor physical disk health using SMART tools.
- Configure proactive alerts and capacity planning to prevent storage-related outages.

---

## What's Next?

**[Memory Monitoring — Monitoring RAM and Swap Usage in Linux](memory-monitoring.md)**

You'll explore:

- Understanding Linux memory management
- Physical memory and swap usage
- Monitoring memory consumption
- Using `free`, `vmstat`, and related tools
- Identifying memory-intensive processes
- Troubleshooting memory issues
- Production memory monitoring best practices

By the end of the lesson, you'll be able to monitor memory utilization, identify memory bottlenecks, troubleshoot out-of-memory conditions, and optimize memory usage in production Linux environments.
