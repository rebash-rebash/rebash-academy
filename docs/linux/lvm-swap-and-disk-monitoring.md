---
title: "LVM (Logical Volume Manager) — Flexible Storage Management in Linux"
description: "Manage Linux storage with LVM — create PVs, VGs, and LVs, extend volumes online, use snapshots, and apply enterprise storage best practices."
difficulty: advanced
estimated_time: "95 min"
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
  - lvm
  - logical-volumes
  - snapshots
  - rebash-linux-mastery
comments: false
status: ready
---

# LVM (Logical Volume Manager) — Flexible Storage Management in Linux

> **Logical Volume Manager (LVM)** is a storage management framework that provides flexibility beyond traditional disk partitioning. Instead of being limited by fixed partition sizes, LVM allows administrators to create, resize, extend, reduce, and manage storage dynamically. LVM is widely used in enterprise Linux servers, cloud environments, databases, virtualization platforms, and Kubernetes worker nodes because it enables scalable and efficient storage management.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 9: Storage Management → Lesson 5</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Advanced</div>

<div markdown>**Reading Time:** 95 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Storage Management</div>

<div markdown>**Lesson:** 5 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand LVM architecture
- Create Physical Volumes (PV)
- Create Volume Groups (VG)
- Create Logical Volumes (LV)
- Extend storage online
- Reduce logical volumes safely
- Create LVM snapshots
- Troubleshoot LVM
- Apply LVM best practices in production

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
- Module 9 Lessons 1–4

---

# Why Learn LVM?

Imagine:

- Your database suddenly needs 500 GB of additional storage.
- Your application log partition becomes full.
- A cloud VM receives a new disk.
- You need to take a snapshot before upgrading a production application.

Traditional partitions are difficult to resize.

LVM solves these problems with flexible storage management.

---

# What is LVM?

LVM stands for:

```text
Logical Volume Manager
```

It provides an abstraction layer between physical disks and filesystems.

Instead of using partitions directly:

```text
Disk

↓

Partition

↓

Filesystem
```

LVM introduces additional layers:

```text
Disk

↓

Physical Volume (PV)

↓

Volume Group (VG)

↓

Logical Volume (LV)

↓

Filesystem

↓

Mount Point
```

---

# LVM Architecture

```text
Physical Disk
      │
      ▼
Physical Volume (PV)
      │
      ▼
Volume Group (VG)
      │
      ▼
Logical Volume (LV)
      │
      ▼
Filesystem
      │
      ▼
Mount Point
```

---

# Physical Volume (PV)

A **Physical Volume** is a storage device prepared for use by LVM.

Examples:

```text
/dev/sdb1

/dev/sdc1

/dev/nvme1n1p1
```

Create a Physical Volume:

```bash
sudo pvcreate /dev/sdb1
```

View Physical Volumes:

```bash
sudo pvs
```

Detailed information:

```bash
sudo pvdisplay
```

---

# Volume Group (VG)

A **Volume Group** combines one or more Physical Volumes into a storage pool.

Example:

```text
Disk1 (500GB)

+

Disk2 (500GB)

↓

VG (1TB)
```

Create a Volume Group:

```bash
sudo vgcreate data_vg /dev/sdb1
```

View Volume Groups:

```bash
sudo vgs
```

Detailed information:

```bash
sudo vgdisplay
```

---

# Logical Volume (LV)

A **Logical Volume** is a virtual partition created from a Volume Group.

Example:

```text
Volume Group

↓

Logical Volume

↓

Filesystem
```

Create a Logical Volume:

```bash
sudo lvcreate -L 100G -n app_lv data_vg
```

Options:

| Option | Meaning |
|---------|----------|
| `-L` | Size |
| `-n` | Logical volume name |

---

# View Logical Volumes

```bash
sudo lvs
```

Detailed information:

```bash
sudo lvdisplay
```

---

# Create a Filesystem

```bash
sudo mkfs.ext4 /dev/data_vg/app_lv
```

---

# Mount the Logical Volume

Create mount point.

```bash
sudo mkdir /app
```

Mount:

```bash
sudo mount /dev/data_vg/app_lv /app
```

Verify:

```bash
df -Th
```

---

# Extend a Logical Volume

Increase by 50 GB.

```bash
sudo lvextend -L +50G /dev/data_vg/app_lv
```

Extend the filesystem.

For ext4:

```bash
sudo resize2fs /dev/data_vg/app_lv
```

For XFS:

```bash
sudo xfs_growfs /app
```

The storage is now larger without recreating the filesystem.

---

# Reduce a Logical Volume

Reducing storage requires additional care.

Example for ext4:

```bash
sudo umount /app

sudo e2fsck -f /dev/data_vg/app_lv

sudo resize2fs /dev/data_vg/app_lv 80G

sudo lvreduce -L 80G /dev/data_vg/app_lv

sudo mount /app
```

> **Warning:** Reducing a logical volume incorrectly can cause permanent data loss. Always back up data before shrinking filesystems or logical volumes.

---

# Extend a Volume Group

Add another disk.

Create PV.

```bash
sudo pvcreate /dev/sdc1
```

Extend VG.

```bash
sudo vgextend data_vg /dev/sdc1
```

The Volume Group now has additional storage.

---

# Remove a Logical Volume

```bash
sudo lvremove /dev/data_vg/app_lv
```

---

# Remove a Volume Group

```bash
sudo vgremove data_vg
```

---

# Remove a Physical Volume

```bash
sudo pvremove /dev/sdb1
```

---

# LVM Snapshots

Create a snapshot before performing upgrades.

```bash
sudo lvcreate \
-L 10G \
-s \
-n app_snapshot \
/dev/data_vg/app_lv
```

Snapshots allow administrators to restore data to an earlier state if necessary.

---

# Common Commands

Create PV.

```bash
pvcreate /dev/sdb1
```

Create VG.

```bash
vgcreate data_vg /dev/sdb1
```

Create LV.

```bash
lvcreate -L 100G -n app_lv data_vg
```

Display LVM.

```bash
pvs

vgs

lvs
```

Extend LV.

```bash
lvextend
```

---

# Real Production Examples

Create cloud storage.

```bash
pvcreate /dev/nvme1n1p1
```

Create storage pool.

```bash
vgcreate prod_vg /dev/nvme1n1p1
```

Create application storage.

```bash
lvcreate -L 200G -n db_lv prod_vg
```

Create filesystem.

```bash
mkfs.xfs /dev/prod_vg/db_lv
```

Mount.

```bash
mount /dev/prod_vg/db_lv /database
```

---

# Production Perspective

LVM is widely used for:

- Enterprise Linux servers
- Cloud virtual machines
- Database storage
- Kubernetes worker nodes
- Virtualization platforms
- Backup servers
- Disaster recovery
- Storage expansion

It enables administrators to expand storage without repartitioning disks.

---

# Hands-on Lab

## Task 1

Display available disks.

```bash
lsblk
```

---

## Task 2

Create a Physical Volume.

```bash
sudo pvcreate /dev/sdb1
```

---

## Task 3

Create a Volume Group.

```bash
sudo vgcreate lab_vg /dev/sdb1
```

---

## Task 4

Create a Logical Volume.

```bash
sudo lvcreate -L 5G -n lab_lv lab_vg
```

---

## Task 5

Create an ext4 filesystem.

```bash
sudo mkfs.ext4 /dev/lab_vg/lab_lv
```

---

## Task 6

Mount the Logical Volume.

```bash
sudo mkdir /lab

sudo mount /dev/lab_vg/lab_lv /lab
```

---

## Task 7

Extend the Logical Volume.

```bash
sudo lvextend -L +1G /dev/lab_vg/lab_lv

sudo resize2fs /dev/lab_vg/lab_lv
```

---

## Task 8

Display LVM information.

```bash
pvs

vgs

lvs
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `pvcreate` | Create Physical Volume | Prepare new disk |
| `vgcreate` | Create Volume Group | Storage pool |
| `lvcreate` | Create Logical Volume | Virtual partition |
| `pvdisplay` | Display PV details | Storage inventory |
| `vgdisplay` | Display VG details | Capacity planning |
| `lvdisplay` | Display LV details | Volume management |
| `lvextend` | Increase LV size | Online storage expansion |
| `resize2fs` | Resize ext4 filesystem | Match filesystem to LV |
| `xfs_growfs` | Grow XFS filesystem | Online XFS expansion |

---

# Traditional Partitions vs LVM

| Feature | Traditional Partition | LVM |
|----------|----------------------|-----|
| Resize Easily | Limited | ✅ |
| Multiple Disks | Limited | ✅ |
| Snapshots | ❌ | ✅ |
| Flexible Storage | ❌ | ✅ |
| Online Expansion | Limited | ✅ |
| Enterprise Usage | Moderate | Very High |

---

# Common LVM Errors

| Error | Possible Cause |
|--------|----------------|
| `Physical volume not found` | Incorrect device |
| `Volume group not found` | VG missing |
| `Logical volume not found` | Incorrect LV path |
| `Insufficient free space` | Volume Group full |
| `Filesystem resize failed` | Filesystem not resized properly |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A production database server reports:

```text
No space left on device
```

Investigation:

Check storage.

```bash
df -h
```

The database filesystem is full.

Check available space in the Volume Group.

```bash
vgs
```

There is 200 GB of free space.

Extend the Logical Volume.

```bash
sudo lvextend -L +100G /dev/prod_vg/db_lv
```

Grow the filesystem.

```bash
sudo xfs_growfs /database
```

The application immediately gains additional storage without downtime.

---

# Best Practices

- Use LVM for production Linux servers.
- Leave free space in Volume Groups for future expansion.
- Create snapshots before major upgrades.
- Use meaningful names for VGs and LVs.
- Monitor available free space regularly.
- Always back up data before reducing logical volumes.

---

# Common Mistakes

❌ Confusing Physical Volumes with Logical Volumes.

✅ Distinguish clearly between Physical Volumes with Logical Volumes.

---

❌ Forgetting to resize the filesystem after extending the Logical Volume.

✅ Remember to to resize the filesystem after extending the Logical Volume.

---

❌ Reducing Logical Volumes without shrinking the filesystem first.

✅ Avoid this mistake: reducing Logical Volumes without shrinking the filesystem first.

---

❌ Using all available Volume Group space immediately.

✅ Avoid using all available Volume Group space immediately when a safer approach exists.

---

❌ Forgetting to mount newly created Logical Volumes.

✅ Remember to to mount newly created Logical Volumes.

---

# Interview Questions
## Beginner

1. What does LVM stand for?
2. What is a Physical Volume?
3. What is a Volume Group?
4. What is a Logical Volume?

---

## Intermediate

1. Why is LVM preferred over traditional partitions?
2. How do you extend a Logical Volume?
3. What is the purpose of a Volume Group?
4. What is an LVM snapshot?

---

## Architect Level

1. How would you design storage for a production database using LVM?
2. How would you expand storage without downtime?
3. What are the advantages of LVM in cloud environments?

---

# Summary

In this lesson, you learned:

- LVM architecture
- Physical Volumes
- Volume Groups
- Logical Volumes
- Creating and extending storage
- LVM snapshots
- Enterprise storage management
- Production best practices

LVM provides flexible, scalable storage management that overcomes the limitations of traditional disk partitioning. It enables administrators to grow storage dynamically, create snapshots, and efficiently manage enterprise storage across multiple physical devices.

---

## Key Takeaways

- LVM separates physical storage from logical storage.
- Physical Volumes (PV) form the foundation of LVM.
- Volume Groups (VG) combine multiple storage devices into a single pool.
- Logical Volumes (LV) behave like flexible virtual partitions.
- Storage can be expanded online with minimal disruption.
- LVM is the preferred storage management solution for enterprise Linux systems.

---

## What's Next?

**[RAID Concepts — Improving Storage Performance and Reliability](raid-concepts.md)**

You'll explore:

- RAID levels
- RAID 0, RAID 1, RAID 5, RAID 6, and RAID 10
- Software RAID using `mdadm`
- Performance and redundancy
- Disk failure recovery
- Production storage best practices

RAID enhances storage performance and fault tolerance, making it an essential technology for enterprise servers and high-availability systems.
