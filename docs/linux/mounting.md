---
title: "Mounting and Unmounting Filesystems — Accessing Storage in Linux"
description: "Mount and unmount Linux filesystems — mount points, umount, /etc/fstab, UUIDs, mount options, and production troubleshooting for persistent storage."
difficulty: intermediate
estimated_time: "80 min"
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
  - mount
  - fstab
  - uuid
  - rebash-linux-mastery
comments: false
status: ready
---

# Mounting and Unmounting Filesystems — Accessing Storage in Linux

> **Mounting** is the process of attaching a filesystem to the Linux directory hierarchy so that users and applications can access the files stored on it. A filesystem cannot be used until it is mounted. **Unmounting** safely detaches the filesystem, ensuring that all pending data is written to disk before the storage device is removed. Understanding mounting is a fundamental skill for Linux administrators, DevOps engineers, Cloud Architects, Platform Engineers, and Site Reliability Engineers (SREs).

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 9: Storage Management → Lesson 4</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 80 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Storage Management</div>

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand mounting and unmounting
- Learn about mount points
- Mount filesystems manually
- Unmount filesystems safely
- Configure persistent mounts
- Understand `/etc/fstab`
- Troubleshoot mount issues
- Apply storage best practices

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
- Module 9 Lessons 1–3

---

# Why Learn Mounting?

Imagine:

- A new SSD is attached to a Linux server.
- A cloud block storage volume is added.
- A USB drive is connected.
- A backup disk needs to be mounted.
- A Kubernetes Persistent Volume is attached to a node.

The storage cannot be used until it is mounted.

---

# What is Mounting?

Mounting is the process of attaching a filesystem to a directory.

Example:

```text
Filesystem

↓

Mount Point

↓

Accessible Files
```

Linux makes all storage accessible through a single directory tree.

---

# What is a Mount Point?

A **mount point** is an empty directory where a filesystem is attached.

Example:

```text
/

├── home

├── var

├── data

└── backup
```

If `/dev/sdb1` is mounted on `/data`, its contents become available under:

```text
/data
```

---

# Linux Directory Tree

Unlike Windows, Linux does not assign drive letters.

Instead:

```text
/

├── home

├── var

├── data

├── boot

└── media
```

Everything is attached somewhere under the root (`/`) directory.

---

# View Mounted Filesystems

Display all mounted filesystems.

```bash
mount
```

---

# Display Mounted Filesystems with Usage

```bash
df -Th
```

Example:

```text
Filesystem

Type

Size

Mounted on
```

---

# View Block Devices

```bash
lsblk
```

Example:

```text
NAME

sda

└── sda1 /

sdb

└── sdb1
```

The **MOUNTPOINT** column shows where a filesystem is mounted.

---

# Create a Mount Point

Create a directory.

```bash
sudo mkdir /data
```

---

# Mount a Filesystem

Basic syntax:

```bash
sudo mount device mountpoint
```

Example:

```bash
sudo mount /dev/sdb1 /data
```

---

# Verify the Mount

```bash
df -Th
```

or

```bash
mount
```

or

```bash
lsblk
```

---

# Access Files

After mounting:

```bash
cd /data

ls
```

Files stored on the partition are now accessible.

---

# Unmount a Filesystem

```bash
sudo umount /data
```

or

```bash
sudo umount /dev/sdb1
```

> Notice the command is **`umount`**, not `unmount`.

---

# Why Unmount?

Unmounting ensures:

- Cached data is written to disk
- Files are closed properly
- Filesystem corruption is avoided
- Devices can be removed safely

---

# Device Busy Error

Example:

```text
umount:

target is busy
```

Possible causes:

- Open files
- Active processes
- Current working directory inside the mount

Find processes using the filesystem.

```bash
sudo lsof +D /data
```

or

```bash
sudo fuser -vm /data
```

---

# Force Unmount

If absolutely necessary:

```bash
sudo umount -f /data
```

> Force unmount is generally intended for specific situations, such as unreachable network filesystems. Use it carefully.

---

# Lazy Unmount

```bash
sudo umount -l /data
```

Lazy unmount detaches the filesystem immediately and completes the unmount after active references are released.

---

# Persistent Mounts

Manual mounts disappear after reboot.

Persistent mounts are configured in:

```text
/etc/fstab
```

---

# Understanding /etc/fstab

Example:

```text
UUID=1234-5678

/data

ext4

defaults

0

2
```

Fields:

| Field | Description |
|---------|-------------|
| Device/UUID | Filesystem identifier |
| Mount Point | Directory where it will be mounted |
| Filesystem | ext4, xfs, etc. |
| Options | Mount options |
| Dump | Backup utility flag |
| Pass | Filesystem check order |

---

# View UUID

```bash
blkid
```

Example:

```text
UUID="abcd-1234"
```

Using UUIDs is preferred because device names can change after reboot.

---

# Test fstab

After editing:

```bash
sudo mount -a
```

If no errors appear, the configuration is valid.

---

# Common Mount Options

| Option | Description |
|----------|-------------|
| `defaults` | Standard mount options |
| `ro` | Read-only |
| `rw` | Read-write |
| `noexec` | Prevent execution of binaries |
| `nosuid` | Ignore SUID/SGID bits |
| `nodev` | Ignore device files |

Example:

```text
defaults,noexec,nodev
```

---

# Common Commands

Mount filesystem.

```bash
sudo mount /dev/sdb1 /data
```

Unmount filesystem.

```bash
sudo umount /data
```

Display mounted filesystems.

```bash
mount
```

Display filesystem usage.

```bash
df -Th
```

Display block devices.

```bash
lsblk
```

Test `fstab`.

```bash
sudo mount -a
```

---

# Real Production Examples

Mount a cloud volume.

```bash
sudo mount /dev/nvme1n1p1 /data
```

Verify mount.

```bash
df -Th
```

View UUID.

```bash
blkid
```

Test persistent configuration.

```bash
sudo mount -a
```

---

# Production Perspective

Mounting is essential for:

- Database storage
- Application data
- Backup volumes
- Kubernetes Persistent Volumes
- NFS shares
- SAN storage
- Cloud block storage
- External storage devices

Correct mount configuration ensures storage remains available after system reboots.

---

# Hands-on Lab

## Task 1

Display mounted filesystems.

```bash
mount
```

---

## Task 2

Display filesystem usage.

```bash
df -Th
```

---

## Task 3

Create a mount point.

```bash
sudo mkdir /data
```

---

## Task 4

Mount a **test partition**.

```bash
sudo mount /dev/sdb1 /data
```

---

## Task 5

Verify the mount.

```bash
lsblk

df -Th
```

---

## Task 6

Display the UUID.

```bash
blkid
```

---

## Task 7

Unmount the filesystem.

```bash
sudo umount /data
```

---

## Task 8

Test `/etc/fstab`.

```bash
sudo mount -a
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `mount` | Mount filesystem | Storage activation |
| `umount` | Unmount filesystem | Safe removal |
| `df -Th` | Display mounted filesystems | Capacity monitoring |
| `lsblk` | View mount points | Storage inventory |
| `blkid` | Display UUIDs | Persistent mounting |
| `mount -a` | Test `/etc/fstab` | Configuration verification |

---

# Common Mount Errors

| Error | Possible Cause |
|--------|----------------|
| `wrong fs type` | Missing or incorrect filesystem |
| `mount point does not exist` | Directory not created |
| `device is busy` | Filesystem in use |
| `permission denied` | Insufficient privileges |
| `special device does not exist` | Incorrect device name |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A new cloud storage volume does not appear after reboot.

Investigation:

Check mounted filesystems.

```bash
df -Th
```

The storage is missing.

Review `/etc/fstab`.

```bash
cat /etc/fstab
```

The administrator used:

```text
/dev/sdb1
```

Instead of the filesystem UUID.

Retrieve the UUID.

```bash
blkid
```

Update `/etc/fstab`.

```text
UUID=abcd-1234

/data

ext4

defaults

0

2
```

Test:

```bash
sudo mount -a
```

The storage mounts successfully and will persist across reboots.

---

# Best Practices

- Always use UUIDs in `/etc/fstab`.
- Test `/etc/fstab` with `mount -a` before rebooting.
- Create dedicated mount points.
- Unmount removable devices before disconnecting them.
- Verify successful mounts using `df -Th` or `lsblk`.
- Avoid force unmount unless absolutely necessary.

---

# Common Mistakes

❌ Forgetting to create the mount point.

✅ Remember to to create the mount point.

---

❌ Editing `/etc/fstab` without testing.

✅ Edit `/etc/fstab` without testing only when appropriate and with a backup.

---

❌ Removing storage without unmounting.

✅ Avoid this mistake: removing storage without unmounting.

---

❌ Using device names instead of UUIDs.

✅ Prefer UUIDs rather than using device names.

---

❌ Unmounting a filesystem while applications are actively using it.

✅ Avoid this mistake: unmounting a filesystem while applications are actively using it.

---

# Interview Questions
## Beginner

1. What is mounting?
2. What is a mount point?
3. Which command mounts a filesystem?
4. Which command unmounts a filesystem?

---

## Intermediate

1. Why are UUIDs preferred over device names?
2. What is the purpose of `/etc/fstab`?
3. How do you identify processes preventing an unmount?
4. What does `mount -a` do?

---

## Architect Level

1. How would you design persistent storage for production Linux servers?
2. How would you troubleshoot a server that fails to boot because of an incorrect `/etc/fstab` entry?
3. What mount options would you use to improve the security of a shared storage volume?

---

# Summary

In this lesson, you learned:

- Mounting and unmounting filesystems
- Mount points
- The `mount` and `umount` commands
- Persistent mounts
- `/etc/fstab`
- UUIDs
- Mount troubleshooting
- Production storage best practices

Mounting connects a filesystem to the Linux directory tree, making stored data accessible to users and applications. Proper mount configuration, especially using UUIDs and `/etc/fstab`, is essential for reliable and maintainable Linux storage management.

---

## Key Takeaways

- A filesystem must be mounted before it can be used.
- Mount points are directories where filesystems are attached.
- Use `mount` to attach and `umount` to detach filesystems.
- Configure persistent mounts using `/etc/fstab`.
- Use UUIDs instead of device names for reliable mounting.
- Always test `/etc/fstab` with `mount -a` before rebooting.

---

## What's Next?

**[LVM (Logical Volume Manager) — Flexible Storage Management in Linux](lvm-swap-and-disk-monitoring.md)**

You'll explore:

- Physical Volumes (PV)
- Volume Groups (VG)
- Logical Volumes (LV)
- Creating and extending volumes
- Online storage expansion
- Snapshots
- Enterprise storage management

LVM provides flexible storage management and is widely used in enterprise Linux environments for scalable and easily expandable storage.
