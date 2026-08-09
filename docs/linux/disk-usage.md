---
title: "Disk Usage in Linux — Monitoring Storage and Filesystem Space"
description: "Monitor Linux disk usage with df, du, and find — track filesystem and inode space, locate large files, and troubleshoot No space left on device."
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 4 · File Management and Permissions"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - df
  - du
  - disk-usage
  - inodes
  - storage
  - rebash-linux-mastery
comments: false
status: ready
---

# Disk Usage in Linux — Monitoring Storage and Filesystem Space

> Disk space is one of the most critical resources on any Linux system. Running out of disk space can cause application failures, database crashes, Kubernetes pod failures, CI/CD pipeline errors, and even prevent a server from booting. Linux provides several powerful utilities to monitor and analyze disk usage effectively.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 4: File Management and Permissions → Lesson 10</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 50 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** File Management and Permissions</div>

<div markdown>**Lesson:** 10 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand disk usage concepts
- Monitor filesystem usage
- Measure directory sizes
- Identify large files
- Analyze storage consumption
- Troubleshoot full disks
- Monitor production servers
- Apply storage best practices

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Command Line Essentials
- Module 3 – Text Processing
- Module 4 Lessons 1–9

---

# Why Learn Disk Usage?

Imagine it's **2:00 AM**.

Your production application suddenly crashes.

Logs show:

```text
No space left on device
```

Questions:

- Which filesystem is full?
- Which directory is consuming the space?
- Which files are the largest?
- How can you recover safely?

Every Linux administrator eventually encounters this scenario.

---

# Understanding Disk Usage

Linux storage consists of:

```text
Disk

↓

Partition

↓

Filesystem

↓

Directories

↓

Files
```

Disk usage tools help you understand where storage is being consumed.

---

# Filesystem Usage

Display filesystem usage.

```bash
df -h
```

Example:

```text
Filesystem      Size Used Avail Use% Mounted on

/dev/sda1        50G 32G 15G 69% /

/dev/sdb1       500G 90G 385G 19% /data
```

---

# Understanding df Output

| Column | Description |
|----------|-------------|
| Filesystem | Storage device |
| Size | Total size |
| Used | Used space |
| Avail | Free space |
| Use% | Percentage used |
| Mounted on | Mount point |

---

# Human Readable Output

Without:

```bash
df
```

Displays bytes.

Better:

```bash
df -h
```

Units:

```text
K

M

G

T
```

---

# Display Specific Filesystem Type

```bash
df -Th
```

Example:

```text
Filesystem Type Size Used Mounted on

/dev/sda1 ext4 50G 30G /
```

---

# Inode Usage

Filesystems have two limits:

- Storage space
- Inodes

Display inode usage.

```bash
df -i
```

Example:

```text
Filesystem

Inodes

IUsed

IFree

IUse%
```

A filesystem can run out of inodes even when disk space is available.

---

# Directory Usage

Use:

```bash
du
```

Example:

```bash
du Documents
```

---

# Human Readable

```bash
du -h Documents
```

---

# Display Total Size

```bash
du -sh Documents
```

Example:

```text
2.3G Documents
```

---

# Show Subdirectories

```bash
du -h --max-depth=1
```

Example:

```text
200M Downloads

3G Videos

500M Documents
```

---

# Find Largest Directories

```bash
du -sh * | sort -hr
```

Example:

```text
15G backups

8G videos

2G downloads
```

---

# Find Large Files

```bash
find . -type f -size +100M
```

Find files larger than:

1 GB.

```bash
find . -type f -size +1G
```

---

# Largest Files

```bash
find . -type f -exec du -h {} + | sort -hr | head
```

---

# Check Current Directory

```bash
du -sh .
```

---

# Display Mounted Filesystems

```bash
findmnt
```

---

# Display Block Devices

```bash
lsblk
```

---

# Disk Free Summary

```bash
df -h /
```

---

# Common Commands

Filesystem usage.

```bash
df -h
```

Directory size.

```bash
du -sh
```

Largest directories.

```bash
du -sh * | sort -hr
```

Large files.

```bash
find . -size +500M
```

Block devices.

```bash
lsblk
```

Mounted filesystems.

```bash
findmnt
```

---

# Real Production Examples

Check Kubernetes node storage.

```bash
df -h
```

Docker storage.

```bash
du -sh /var/lib/docker
```

System logs.

```bash
du -sh /var/log
```

Database storage.

```bash
du -sh /var/lib/mysql
```

Jenkins workspace.

```bash
du -sh /var/lib/jenkins
```

---

# Production Perspective

Disk monitoring is essential for:

- Linux servers
- Databases
- Docker
- Kubernetes
- CI/CD
- Backup servers
- Cloud VMs
- Log management

Regular monitoring prevents outages caused by storage exhaustion.

---

# Hands-on Lab

## Task 1

Display filesystem usage.

```bash
df -h
```

---

## Task 2

Display filesystem types.

```bash
df -Th
```

---

## Task 3

Display inode usage.

```bash
df -i
```

---

## Task 4

Display your home directory size.

```bash
du -sh ~
```

---

## Task 5

Display subdirectory sizes.

```bash
du -h --max-depth=1 ~
```

---

## Task 6

Sort directories by size.

```bash
du -sh ~/* | sort -hr
```

---

## Task 7

Find files larger than 100 MB.

```bash
find ~ -type f -size +100M
```

---

## Task 8

Display the 10 largest files in your home directory.

```bash
find ~ -type f -exec du -h {} + | sort -hr | head -10
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `df -h` | Filesystem usage | Capacity monitoring |
| `df -i` | Inode usage | Troubleshooting |
| `du -sh` | Directory size | Storage analysis |
| `find` | Locate large files | Cleanup |
| `sort -hr` | Sort by size | Reporting |
| `lsblk` | Storage inventory | Administration |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A Kubernetes node becomes **NotReady**.

Pods cannot start.

Investigation:

```bash
df -h

du -sh /var/lib/containerd

du -sh /var/log

find /var/log -type f -size +500M
```

Findings:

- Container images consume 40 GB.
- Old logs consume 15 GB.
- Disk usage reaches 98%.

Solution:

- Remove unused container images.
- Rotate or archive old logs.
- Expand storage if required.
- Configure log rotation and monitoring.

---

# Best Practices

- Monitor disk usage regularly.
- Investigate filesystems above 80% usage.
- Clean temporary files periodically.
- Rotate logs using log rotation tools.
- Monitor inode usage in addition to disk space.
- Automate storage alerts using monitoring platforms.

---

# Common Mistakes

❌ Monitoring only free disk space.

✅ A filesystem may run out of **inodes** before storage space.

---

❌ Deleting application logs without understanding their purpose.

✅ Verify retention requirements before cleanup.

---

❌ Ignoring growth trends.

✅ Track storage usage over time to plan capacity before problems occur.

---

# Interview Questions
## Beginner

1. What does `df` display?
2. What is the difference between `df` and `du`?
3. Why is `-h` commonly used?
4. Which command shows inode usage?

---

## Intermediate

1. Why can a filesystem report "No space left on device" even when free space exists?
2. How do you identify the largest directories?
3. How do you locate files larger than 1 GB?
4. Why should inode usage be monitored?

---

## Architect Level

1. How would you design storage monitoring for hundreds of Linux servers?
2. How would you investigate a filesystem that suddenly reaches 100% usage?
3. What storage metrics would you collect for Kubernetes worker nodes?

---

# Summary

In this lesson, you learned:

- Filesystem usage
- Directory usage
- Inode usage
- Finding large files
- Storage analysis
- Production troubleshooting
- Capacity planning
- Storage best practices

Disk usage monitoring is one of the most important operational tasks in Linux administration. Regularly monitoring filesystems, directories, and inodes helps prevent outages, improves capacity planning, and keeps production systems healthy.

---

## Key Takeaways

- Use `df -h` to monitor filesystem usage.
- Use `du -sh` to measure directory sizes.
- Use `df -i` to monitor inode usage.
- Use `find` to locate large files.
- Investigate filesystems before they become full.
- Automate storage monitoring and alerts for production systems.

---

## What's Next?

**[Module 4 Summary — File Management and Permissions](module-4-file-management-and-permissions-summary.md)**

Review the module, complete the mini project and assessment, then continue to **Module 5 – Users and Groups**.
