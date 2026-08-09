---
title: "Partitions — Organizing Storage Devices in Linux"
description: "Learn Linux disk partitions — MBR vs GPT, primary and logical partitions, lsblk, fdisk, parted, partprobe, and production partitioning practices."
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
  - partitions
  - gpt
  - fdisk
  - rebash-linux-mastery
comments: false
status: ready
---

# Partitions — Organizing Storage Devices in Linux

> A **partition** is a logical division of a physical storage device that allows a single disk to be divided into multiple independent sections. Each partition can contain its own filesystem, operating system, application data, or swap space. Proper partitioning improves organization, security, performance, and storage management. Understanding partitions is an essential skill for Linux administrators, DevOps engineers, Cloud Architects, Platform Engineers, and Site Reliability Engineers (SREs).

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 9: Storage Management → Lesson 1</p>

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

<div markdown>**Lesson:** 1 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand disk partitions
- Learn partition table types
- View existing partitions
- Create and delete partitions
- Understand primary, extended, and logical partitions
- Work with GPT and MBR
- Prepare disks for filesystems
- Apply partitioning best practices in production

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

---

# Why Learn Partitions?

Imagine:

- Installing Linux on a new server.
- Adding a new SSD to a cloud virtual machine.
- Creating separate storage for databases.
- Isolating application logs from the operating system.
- Preparing disks before configuring LVM or RAID.

The first step in all these scenarios is partitioning the storage device.

---

# What is a Partition?

A partition is a logical section of a physical storage device.

Example:

```text
Physical Disk

/dev/sda
│
├── /dev/sda1
├── /dev/sda2
└── /dev/sda3
```

Each partition behaves like an independent storage device.

It can contain:

- A filesystem
- Swap space
- LVM Physical Volume
- Database storage
- Application data

---

# Why Use Partitions?

Partitions help:

- Separate operating system files from user data
- Improve storage organization
- Simplify backups
- Improve security
- Reduce the impact of filesystem corruption
- Prepare storage for enterprise workloads

Example:

```text
Disk

├── /
├── /boot
├── /home
├── /var
└── swap
```

Each partition serves a different purpose.

---

# Partition Tables

A partition table describes how partitions are organized on a disk.

Linux primarily supports:

- MBR (Master Boot Record)
- GPT (GUID Partition Table)

---

# MBR (Master Boot Record)

Characteristics:

- Supports disks up to **2 TB**
- Maximum **4 primary partitions**
- Used by legacy BIOS systems

Example:

```text
Disk

├── Primary
├── Primary
├── Primary
└── Primary
```

Limitations:

- Maximum disk size of 2 TB
- Limited number of partitions

---

# Extended and Logical Partitions

Because MBR supports only four primary partitions, one primary partition can be converted into an **Extended Partition**.

Example:

```text
Primary

Primary

Primary

Extended
        │
        ├── Logical
        ├── Logical
        ├── Logical
        └── Logical
```

Logical partitions exist only inside the extended partition.

---

# GPT (GUID Partition Table)

GPT is the modern partitioning standard.

Advantages:

- Supports disks larger than **2 TB**
- Typically supports **128 partitions**
- Better reliability
- Redundant partition table
- Required for UEFI boot systems

GPT is recommended for almost all modern Linux installations.

---

# Device Naming

Linux names storage devices as follows:

SATA/SCSI disks:

```text
/dev/sda

/dev/sdb
```

NVMe disks:

```text
/dev/nvme0n1
```

Partitions:

```text
/dev/sda1

/dev/sda2

/dev/nvme0n1p1
```

---

# View Available Disks

Display storage devices.

```bash
lsblk
```

Example:

```text
NAME

sda

├── sda1

├── sda2

└── sda3
```

---

# View Partition Details

```bash
sudo fdisk -l
```

Displays:

- Disk size
- Partition table type
- Partition sizes
- Bootable partitions

---

# View Filesystem Information

```bash
blkid
```

Example:

```text
UUID

TYPE

LABEL
```

---

# View Partition Table

Using `parted`:

```bash
sudo parted /dev/sda print
```

Shows:

- Partition table type
- Partition layout
- Start/end sectors
- Partition sizes

---

# Create a Partition Using fdisk

Open the disk.

```bash
sudo fdisk /dev/sdb
```

Common interactive commands:

```text
n
```

Create a new partition.

```text
p
```

Primary partition (MBR only).

```text
w
```

Write changes to disk.

---

# Create a GPT Partition Using parted

Start `parted`.

```bash
sudo parted /dev/sdb
```

Create GPT.

```bash
mklabel gpt
```

Create partition.

```bash
mkpart primary ext4 1MiB 20GiB
```

Exit.

```bash
quit
```

---

# Reload Partition Table

Inform the kernel about partition changes.

```bash
sudo partprobe
```

If necessary, reboot the system.

---

# Delete a Partition

Using `fdisk`:

```text
d
```

Delete selected partition.

Save changes.

```text
w
```

> **Warning:** Deleting a partition removes it from the partition table. The filesystem becomes inaccessible and data recovery may not be possible without specialized tools.

---

# Common Commands

Display disks.

```bash
lsblk
```

Display partitions.

```bash
sudo fdisk -l
```

Show UUIDs.

```bash
blkid
```

Partition management.

```bash
sudo fdisk /dev/sdb
```

Modern partition management.

```bash
sudo parted /dev/sdb
```

Reload partition table.

```bash
sudo partprobe
```

---

# Real Production Examples

Inspect a new cloud volume.

```bash
lsblk
```

View partition details.

```bash
sudo fdisk -l
```

Create a GPT partition.

```bash
sudo parted /dev/nvme0n1
```

Reload partition table.

```bash
sudo partprobe
```

---

# Production Perspective

Partitions are commonly used for:

- Linux installations
- Database storage
- Application data
- Log storage
- Backup volumes
- Cloud virtual machines
- LVM Physical Volumes
- RAID configurations

Proper partition planning makes storage easier to manage and expand.

---

# Hands-on Lab

## Task 1

Display storage devices.

```bash
lsblk
```

---

## Task 2

View partition information.

```bash
sudo fdisk -l
```

---

## Task 3

Display UUIDs.

```bash
blkid
```

---

## Task 4

Display the partition table.

```bash
sudo parted /dev/sda print
```

---

## Task 5

Create a partition on a **test disk**.

```bash
sudo fdisk /dev/sdb
```

> Never perform this exercise on a production disk.

---

## Task 6

Reload the partition table.

```bash
sudo partprobe
```

---

## Task 7

Verify the new partition.

```bash
lsblk
```

---

## Task 8

Review the updated partition layout.

```bash
sudo fdisk -l
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `lsblk` | View disks and partitions | Storage inventory |
| `fdisk -l` | Display partition information | Capacity planning |
| `blkid` | View filesystem UUIDs | Mount configuration |
| `fdisk` | Create or modify partitions | Disk preparation |
| `parted` | GPT partition management | Enterprise storage |
| `partprobe` | Reload partition table | Apply changes |

---

# MBR vs GPT

| Feature | MBR | GPT |
|----------|-----|-----|
| Maximum Disk Size | 2 TB | Greater than 2 TB |
| Maximum Partitions | 4 Primary | Typically 128 |
| UEFI Support | No | Yes |
| Redundant Metadata | No | Yes |
| Recommended Today | Legacy Systems | Modern Systems |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A new 8 TB storage volume is attached to a Linux server.

Running:

```bash
sudo fdisk -l
```

shows the disk, but only 2 TB is usable.

Investigation reveals that the disk uses an MBR partition table.

Solution:

Create a GPT partition table.

```bash
sudo parted /dev/sdb

mklabel gpt
```

Create a partition.

```bash
mkpart primary ext4 1MiB 100%
```

Reload the partition table.

```bash
sudo partprobe
```

The full disk capacity is now available.

---

# Best Practices

- Use GPT for modern Linux systems.
- Separate operating system and application data when appropriate.
- Verify the target disk before modifying partitions.
- Back up important data before changing partition layouts.
- Use UUIDs when mounting filesystems.
- Leave room for future storage expansion.

---

# Common Mistakes

❌ Partitioning the wrong disk.

✅ Avoid this mistake: partitioning the wrong disk.

---

❌ Using MBR on disks larger than 2 TB.

✅ Avoid using MBR on disks larger than 2 TB when a safer approach exists.

---

❌ Forgetting to reload the partition table.

✅ Remember to to reload the partition table.

---

❌ Modifying production disks without backups.

✅ Avoid this mistake: modifying production disks without backups.

---

❌ Poor partition planning leading to storage shortages.

✅ Avoid this mistake: poor partition planning leading to storage shortages.

---

# Interview Questions
## Beginner

1. What is a partition?
2. What is the purpose of a partition table?
3. What is the difference between MBR and GPT?
4. Which command lists disk partitions?

---

## Intermediate

1. Why is GPT preferred over MBR?
2. What is the purpose of `partprobe`?
3. How do you create a partition using `fdisk`?
4. What are logical partitions?

---

## Architect Level

1. How would you partition storage for a production database server?
2. How would you migrate from MBR to GPT?
3. How would you design partition layouts for enterprise Linux servers?

---

# Summary

In this lesson, you learned:

- Disk partitions
- Partition tables
- MBR and GPT
- Primary, extended, and logical partitions
- Partition management tools
- Creating and deleting partitions
- Production storage best practices

Partitions divide physical storage into logical sections, allowing Linux systems to organize data efficiently, improve reliability, and simplify storage management. Understanding partitioning is the foundation for working with filesystems, LVM, RAID, and enterprise storage solutions.

---

## Key Takeaways

- Partitions divide physical disks into logical storage areas.
- GPT is the recommended partition table for modern Linux systems.
- `lsblk`, `fdisk`, and `parted` are essential partition management tools.
- Always verify the correct disk before making changes.
- Reload the partition table after modifications using `partprobe`.
- Proper partition planning simplifies future storage management.

---

## What's Next?

**[Filesystems — Organizing and Managing Data on Linux Storage](filesystems.md)**

You'll explore:

- What a filesystem is
- Common Linux filesystem types
- Creating filesystems
- Formatting partitions
- Filesystem labels and UUIDs
- Choosing the right filesystem
- Production best practices

Understanding filesystems is the next step toward managing Linux storage efficiently.
