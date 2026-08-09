---
title: "Swap Space — Extending Memory in Linux"
description: "Configure Linux swap space — create swap files and partitions, enable persistent swap, monitor usage, and tune swappiness for production workloads."
difficulty: intermediate
estimated_time: "75 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 9 · Storage Management"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - storage
  - swap
  - memory
  - swappiness
  - rebash-linux-mastery
comments: false
status: ready
---

# Swap Space — Extending Memory in Linux

> **Swap Space** is a reserved area on disk that Linux uses as virtual memory when physical RAM becomes full. It allows the operating system to move inactive memory pages from RAM to disk, helping prevent out-of-memory (OOM) situations and improving system stability. Although swap is significantly slower than RAM, it plays an important role in enterprise Linux systems, cloud environments, virtualization platforms, and Kubernetes worker nodes.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 9: Storage Management → Lesson 7</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 75 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Storage Management</div>

<div markdown>**Lesson:** 7 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand swap space
- Learn how virtual memory works
- Create swap partitions and swap files
- Enable and disable swap
- Monitor swap usage
- Configure swap persistence
- Tune swap behavior
- Apply swap best practices in production

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
- Module 8 – Networking
- Module 9 Lessons 1–6

---

# Why Learn Swap?

Imagine:

- A database server temporarily runs out of RAM.
- A Kubernetes node experiences memory pressure.
- Multiple virtual machines share limited memory.
- An application suddenly consumes excessive RAM.

Without swap:

```text
RAM Full

↓

Out Of Memory (OOM)

↓

Processes Killed
```

With swap:

```text
RAM Full

↓

Inactive Pages Moved to Disk

↓

System Continues Running
```

---

# What is Swap?

Swap is disk space used as an extension of physical memory (RAM).

Memory hierarchy:

```text
CPU Cache

↓

RAM

↓

Swap

↓

Storage
```

RAM is much faster than swap, but swap provides additional virtual memory when needed.

---

# How Swap Works

```text
Applications

↓

RAM

↓

RAM Full

↓

Inactive Pages

↓

Swap Space
```

Frequently used data stays in RAM, while less frequently used pages may be moved to swap.

---

# Types of Swap

Linux supports two types:

- Swap Partition
- Swap File

---

# Swap Partition

A dedicated partition created specifically for swap.

Example:

```text
/dev/sda2

Type: Linux Swap
```

Advantages:

- Better performance
- Common in enterprise deployments
- Traditional approach

---

# Swap File

A regular file used as swap.

Example:

```text
/swapfile
```

Advantages:

- Easy to create
- Easy to resize
- Common in cloud virtual machines

---

# View Swap Information

Display swap usage.

```bash
swapon --show
```

Example:

```text
NAME

TYPE

SIZE

USED
```

---

# View Memory Usage

```bash
free -h
```

Example:

```text
Mem

Swap
```

---

# Create a Swap File

Create a 2 GB swap file.

```bash
sudo fallocate -l 2G /swapfile
```

If `fallocate` is unavailable:

```bash
sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
```

---

# Set Secure Permissions

```bash
sudo chmod 600 /swapfile
```

Only the root user should have access.

---

# Format as Swap

```bash
sudo mkswap /swapfile
```

Example output:

```text
Setting up swapspace...
```

---

# Enable Swap

```bash
sudo swapon /swapfile
```

Verify:

```bash
swapon --show
```

---

# Disable Swap

```bash
sudo swapoff /swapfile
```

---

# Configure Persistent Swap

Add the following entry to:

```text
/etc/fstab
```

```text
/swapfile none swap sw 0 0
```

After reboot, the swap file will be enabled automatically.

---

# Create a Swap Partition

Format the partition.

```bash
sudo mkswap /dev/sdb2
```

Enable it.

```bash
sudo swapon /dev/sdb2
```

---

# View Swap UUID

```bash
blkid
```

Example:

```text
UUID="abcd-1234"

TYPE="swap"
```

Persistent `/etc/fstab` entry:

```text
UUID=abcd-1234

none

swap

sw

0

0
```

---

# Swappiness

Linux uses the **swappiness** parameter to determine how aggressively it moves memory pages to swap.

View current value.

```bash
cat /proc/sys/vm/swappiness
```

Example:

```text
60
```

Temporarily change it.

```bash
sudo sysctl vm.swappiness=20
```

Persist the setting.

Edit:

```text
/etc/sysctl.conf
```

Add:

```text
vm.swappiness=20
```

Typical values:

| Value | Behavior |
|---------|-----------|
| 0 | Avoid swap unless absolutely necessary |
| 10–20 | Preferred for database servers |
| 60 | Linux default on many distributions |
| 100 | Use swap aggressively |

---

# Common Commands

View swap.

```bash
swapon --show
```

View memory.

```bash
free -h
```

Create swap.

```bash
mkswap /swapfile
```

Enable swap.

```bash
swapon /swapfile
```

Disable swap.

```bash
swapoff /swapfile
```

---

# Real Production Examples

Check swap usage.

```bash
free -h
```

Enable swap.

```bash
sudo swapon /swapfile
```

Monitor memory.

```bash
vmstat 2
```

Adjust swappiness.

```bash
sudo sysctl vm.swappiness=10
```

---

# Production Perspective

Swap is commonly used for:

- Linux servers
- Cloud virtual machines
- Kubernetes worker nodes
- Virtualization hosts
- Development environments
- Desktop systems
- Memory-intensive workloads

Swap improves system stability but should not replace adequate physical RAM.

---

# Hands-on Lab

## Task 1

View current memory usage.

```bash
free -h
```

---

## Task 2

Display active swap.

```bash
swapon --show
```

---

## Task 3

Create a 1 GB swap file.

```bash
sudo fallocate -l 1G /swapfile
```

---

## Task 4

Set permissions.

```bash
sudo chmod 600 /swapfile
```

---

## Task 5

Format the swap file.

```bash
sudo mkswap /swapfile
```

---

## Task 6

Enable swap.

```bash
sudo swapon /swapfile
```

---

## Task 7

Verify swap.

```bash
free -h

swapon --show
```

---

## Task 8

Disable swap.

```bash
sudo swapoff /swapfile
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `free -h` | View memory usage | Capacity monitoring |
| `swapon --show` | Display active swap | Memory management |
| `mkswap` | Format swap area | Storage preparation |
| `swapon` | Enable swap | Virtual memory |
| `swapoff` | Disable swap | Maintenance |
| `sysctl` | Configure swappiness | Performance tuning |

---

# Swap Partition vs Swap File

| Feature | Swap Partition | Swap File |
|----------|----------------|-----------|
| Performance | Slightly Better | Very Good |
| Easy to Resize | No | Yes |
| Easy to Create | No | Yes |
| Cloud Friendly | Limited | Excellent |
| Enterprise Usage | Common | Increasingly Common |

---

# Common Swap Errors

| Error | Possible Cause |
|--------|----------------|
| `Permission denied` | Incorrect file permissions |
| `Invalid argument` | Swap not formatted |
| `Device or resource busy` | Swap already active |
| `No such file` | Incorrect path |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A production application is terminated unexpectedly.

Logs show:

```text
Out of memory
```

Investigation:

Check memory.

```bash
free -h
```

Output:

```text
RAM: 100% Used

Swap: 0B
```

The server has no configured swap space.

Solution:

Create a swap file.

```bash
sudo fallocate -l 4G /swapfile

sudo chmod 600 /swapfile

sudo mkswap /swapfile

sudo swapon /swapfile
```

The server now has additional virtual memory, reducing the likelihood of future OOM events.

---

# Best Practices

- Configure swap on production Linux servers unless there is a specific reason not to.
- Prefer swap files on cloud virtual machines for easier management.
- Use secure permissions (`600`) on swap files.
- Monitor swap usage regularly.
- Tune swappiness based on workload.
- Remember that swap complements RAM but does not replace it.

---

# Common Mistakes

❌ Assuming swap is a replacement for physical RAM.

✅ Verify swap is a replacement for physical RAM instead of assuming it.

---

❌ Forgetting to add swap to `/etc/fstab`.

✅ Remember to to add swap to `/etc/fstab`.

---

❌ Creating swap files with insecure permissions.

✅ Avoid this mistake: creating swap files with insecure permissions.

---

❌ Ignoring frequent swap usage, which may indicate insufficient RAM.

✅ Always review frequent swap usage, which may indicate insufficient RAM.

---

❌ Setting swappiness too high for memory-sensitive workloads such as databases.

✅ Avoid this mistake: setting swappiness too high for memory-sensitive workloads such as databases.

---

# Interview Questions
## Beginner

1. What is swap space?
2. What is the difference between RAM and swap?
3. Which command enables swap?
4. How do you view active swap?

---

## Intermediate

1. What is the difference between a swap partition and a swap file?
2. What is swappiness?
3. How do you create a persistent swap file?
4. Why should swap files have `600` permissions?

---

## Architect Level

1. How would you configure swap for a production Kubernetes node?
2. How would you tune swappiness for a database server?
3. What are the advantages and disadvantages of swap in cloud environments?

---

# Summary

In this lesson, you learned:

- Swap fundamentals
- Swap partitions and swap files
- Creating and enabling swap
- Persistent swap configuration
- Swappiness tuning
- Monitoring swap usage
- Production best practices

Swap extends physical memory by providing virtual memory on disk. Although it is much slower than RAM, it improves system stability by preventing out-of-memory conditions and providing additional memory capacity during peak workloads.

---

## Key Takeaways

- Swap extends RAM using disk space.
- Linux supports both swap partitions and swap files.
- Use `mkswap` to prepare swap space.
- Use `swapon` and `swapoff` to enable and disable swap.
- Configure persistent swap in `/etc/fstab`.
- Monitor swap usage to identify memory pressure.

---

## What's Next?

**[Disk Quotas — Controlling Storage Usage in Linux](quotas.md)**

You'll explore:

- User and group disk quotas
- Soft and hard limits
- Enabling quotas
- Monitoring disk usage
- Managing quota violations
- Enterprise storage policies

Disk quotas help administrators control storage consumption and prevent users or applications from exhausting available disk space.
