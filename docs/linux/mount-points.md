---
title: "Mount Points in Linux — Understanding Filesystems and Storage Mounting"
description: "Mount and manage Linux storage — use mount, umount, findmnt, lsblk, and /etc/fstab with UUIDs for persistent production mounts."
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
  - mount
  - fstab
  - storage
  - filesystem
  - rebash-linux-mastery
comments: false
status: ready
---

# Mount Points in Linux — Understanding Filesystems and Storage Mounting

> A **mount point** is a directory where a storage device, partition, or remote filesystem becomes accessible in the Linux filesystem hierarchy. Unlike Windows, which uses drive letters (C:, D:, E:), Linux integrates all storage devices into a single directory tree using mount points. Understanding mount points is essential for Linux administration, cloud computing, Kubernetes, Docker, storage management, and production infrastructure.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 4: File Management and Permissions → Lesson 9</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 50 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** File Management and Permissions</div>

<div markdown>**Lesson:** 9 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand mount points
- Learn the Linux filesystem hierarchy
- Mount and unmount filesystems
- View mounted filesystems
- Configure persistent mounts
- Understand `/etc/fstab`
- Troubleshoot mount failures
- Manage storage in production

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Command Line Essentials
- Module 3 – Text Processing
- Module 4 Lessons 1–8

---

# Why Learn Mount Points?

Imagine your production server has:

- 1 SSD for the operating system
- 2 SSDs for databases
- 1 NFS share for backups
- 1 cloud storage volume

How does Linux make all these devices appear as one unified filesystem?

The answer is **mount points**.

---

# Linux Storage Philosophy

Unlike Windows:

```text
C:\

D:\

E:\
```

Linux has only **one filesystem tree**.

```text
/
```

Every storage device becomes part of this tree after it is mounted.

---

# What is a Mount Point?

A mount point is simply a directory where another filesystem is attached.

Example:

```text
/

├── home

├── var

├── opt

└── data
```

Suppose:

```text
/dev/sdb1
```

is mounted on:

```text
/data
```

Now all files stored on `/dev/sdb1` are accessed through:

```text
/data
```

---

# Visual Representation

Before mounting:

```text
Filesystem

/

└── data (empty directory)
```

After mounting:

```text
/

└── data

      │

      ▼

   SSD Disk
```

The contents of the mounted filesystem become visible through the mount point.

---

# Viewing Mounted Filesystems

Display mounted filesystems.

```bash
mount
```

Example:

```text
/dev/sda1 on / type ext4

/dev/sdb1 on /data type ext4
```

---

# Better View

```bash
findmnt
```

Example:

```text
TARGET    SOURCE

/         /dev/sda1

/data     /dev/sdb1
```

---

# Display Disk Usage

```bash
df -h
```

Example:

```text
Filesystem      Size Used Avail Mounted on

/dev/sda1        40G 20G 18G /

/dev/sdb1       500G 100G 400G /data
```

---

# Display Block Devices

```bash
lsblk
```

Example:

```text
NAME

sda

├─sda1

sdb

└─sdb1
```

Include mount points.

```bash
lsblk -f
```

---

# Mounting a Filesystem

Create a mount point.

```bash
sudo mkdir /data
```

Mount.

```bash
sudo mount /dev/sdb1 /data
```

Verify.

```bash
df -h

mount

findmnt
```

---

# Access Files

Once mounted:

```bash
cd /data

ls
```

You are now working directly with the mounted filesystem.

---

# Unmounting

Syntax:

```bash
sudo umount /data
```

or

```bash
sudo umount /dev/sdb1
```

Verify.

```bash
findmnt
```

---

# Why Unmount?

Always unmount removable storage before disconnecting it.

This ensures:

- Pending writes are completed
- Filesystem corruption is avoided
- Metadata is synchronized to disk

---

# Busy Filesystem

Error:

```text
target is busy
```

Determine which process is using the mount.

```bash
lsof +D /data
```

or

```bash
fuser -vm /data
```

After stopping the processes, unmount again.

---

# Temporary vs Persistent Mounts

Temporary:

```bash
mount
```

Valid until reboot.

Persistent:

```text
/etc/fstab
```

Automatically mounted during system startup.

---

# Understanding /etc/fstab

Display.

```bash
cat /etc/fstab
```

Example:

```text
UUID=xxxx-xxxx

/data

ext4

defaults

0

2
```

Fields:

| Field | Description |
|--------|-------------|
| Device | UUID or device name |
| Mount Point | Directory |
| Filesystem | ext4, xfs, etc. |
| Options | Mount options |
| Dump | Backup flag |
| Pass | Filesystem check order |

---

# Why Use UUID?

Instead of:

```text
/dev/sdb1
```

Use:

```text
UUID=4A8F...
```

Device names can change between reboots, but UUIDs remain consistent.

View UUIDs.

```bash
blkid
```

or

```bash
lsblk -f
```

---

# Test fstab

After editing:

```bash
sudo mount -a
```

If there are no errors, the configuration is valid.

---

# Mount Options

Common options.

| Option | Meaning |
|----------|----------|
| defaults | Standard options |
| ro | Read Only |
| rw | Read/Write |
| noexec | Prevent execution |
| nosuid | Ignore SUID bits |
| nodev | Ignore device files |
| noatime | Don't update access time |

Example:

```text
UUID=xxxx

/data

ext4

defaults,noatime

0

2
```

---

# Mounting ISO Images

```bash
sudo mount -o loop ubuntu.iso /mnt
```

---

# Network Filesystems

NFS.

```bash
sudo mount server:/backup /mnt/backup
```

SMB/CIFS.

```bash
sudo mount -t cifs
```

---

# Common Commands

View mounts.

```bash
mount

findmnt
```

Disk usage.

```bash
df -h
```

Block devices.

```bash
lsblk
```

Mount.

```bash
mount
```

Unmount.

```bash
umount
```

Filesystem IDs.

```bash
blkid
```

---

# Real Production Examples

Mount database storage.

```text
/data
```

Mount application storage.

```text
/opt/app
```

Mount backup storage.

```text
/backup
```

Mount Kubernetes persistent volume.

```text
/var/lib/kubelet
```

Mount Docker storage.

```text
/var/lib/docker
```

---

# Production Perspective

Mount points are used extensively in:

- Linux servers
- Cloud VMs
- Kubernetes Persistent Volumes
- Docker volumes
- NAS devices
- SAN storage
- NFS servers
- Backup systems

Understanding mount points is critical for storage administration and troubleshooting.

---

# Hands-on Lab

## Task 1

Display mounted filesystems.

```bash
mount
```

---

## Task 2

Display block devices.

```bash
lsblk
```

---

## Task 3

Display UUIDs.

```bash
blkid
```

---

## Task 4

Display mounted tree.

```bash
findmnt
```

---

## Task 5

Display disk usage.

```bash
df -h
```

---

## Task 6

Create a mount point.

```bash
sudo mkdir /mnt/demo
```

*(Do not mount a production device unless you understand the impact.)*

---

## Task 7

Inspect `/etc/fstab`.

```bash
cat /etc/fstab
```

---

## Task 8

Validate fstab configuration.

```bash
sudo mount -a
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `mount` | Display or mount filesystems | Storage management |
| `umount` | Unmount filesystems | Safe removal |
| `findmnt` | Show mount tree | Troubleshooting |
| `df -h` | Filesystem usage | Capacity planning |
| `lsblk` | Display block devices | Storage inventory |
| `blkid` | Display UUIDs | Persistent mounts |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A production application fails after a reboot because its data volume is missing.

Investigation:

```bash
findmnt

lsblk -f

cat /etc/fstab

journalctl -b | grep mount
```

The storage volume was configured using:

```text
/dev/sdb1
```

After reboot, the kernel assigned it:

```text
/dev/sdc1
```

Solution:

Replace the device name with its UUID in `/etc/fstab`.

Validate:

```bash
sudo mount -a
```

The application now finds the correct storage regardless of device naming.

---

# Best Practices

- Prefer UUIDs over device names in `/etc/fstab`.
- Always test `/etc/fstab` with `mount -a`.
- Unmount removable media before disconnecting.
- Create meaningful mount point names.
- Monitor disk usage with `df -h`.

---

# Common Mistakes

❌ Using `/dev/sdb1` in `/etc/fstab` when a UUID is more reliable.

✅ Avoid using `/dev/sdb1` in `/etc/fstab` when a UUID is more reliable when a safer approach exists.

---

❌ Editing `/etc/fstab` without testing.

✅ A mistake can prevent the system from mounting filesystems correctly at boot.

---

❌ Removing a mounted USB drive without unmounting it first.

✅ This may lead to data loss or filesystem corruption.

---

# Interview Questions
## Beginner

1. What is a mount point?
2. Which command displays mounted filesystems?
3. What does `df -h` show?
4. What is `/etc/fstab` used for?

---

## Intermediate

1. Why should UUIDs be used instead of device names?
2. What is the difference between `mount` and `findmnt`?
3. How do you troubleshoot a "target is busy" error?
4. What does `mount -a` do?

---

## Architect Level

1. How would you design persistent storage for a production application server?
2. Why is correct mount configuration important for Kubernetes worker nodes?
3. How would you troubleshoot storage failures after a server reboot?

---

# Summary

In this lesson, you learned:

- Linux mount points
- Viewing mounted filesystems
- Mounting and unmounting storage
- Persistent mounts with `/etc/fstab`
- UUIDs
- Mount options
- Production storage management
- Troubleshooting mount failures

Mount points are a fundamental part of Linux storage management. They allow multiple local and remote filesystems to appear as a single unified directory tree, simplifying administration and enabling scalable storage architectures.

---

## Key Takeaways

- Linux uses a single filesystem hierarchy rooted at `/`.
- A mount point is a directory where a filesystem is attached.
- Use `mount`, `findmnt`, `df`, and `lsblk` to inspect storage.
- Configure persistent mounts in `/etc/fstab`.
- Prefer UUIDs over device names.
- Always unmount removable storage before disconnecting it.

---

## What's Next?

**[Disk Usage in Linux — Monitoring Storage and Filesystem Space](disk-usage.md)**

In the next lesson, you'll learn:

- Monitoring filesystem usage with `df`
- Measuring directory sizes with `du`
- Tracking inode usage
- Finding large files
- Troubleshooting full disks in production
