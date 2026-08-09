---
title: "Linux Directory Structure (Filesystem Hierarchy Standard - FHS)"
description: "Every Linux system follows a standardized directory structure called the Filesystem Hierarchy Standard (FHS). Understanding this structure is essential for Linux administration, DevOps, Cloud Engineering, and troubleshooting production systems."
difficulty: beginner
estimated_time: "20 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 1 · Linux Fundamentals"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - fhs
  - filesystem
  - directories
  - fundamentals
  - rebash-linux-mastery
comments: false
status: ready
---

# Linux Directory Structure (Filesystem Hierarchy Standard - FHS)

> Every Linux system follows a standardized directory structure called the **Filesystem Hierarchy Standard (FHS)**. Understanding this structure is essential for Linux administration, DevOps, Cloud Engineering, and troubleshooting production systems.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 1: Linux Fundamentals → Lesson 9</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 20 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Linux Fundamentals</div>

<div markdown>**Lesson:** 9 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the Linux Filesystem Hierarchy Standard (FHS)
- Navigate important Linux directories
- Know where Linux stores configuration files
- Understand where applications, logs, and user data reside
- Learn directory best practices for production environments

---

# Prerequisites

Before starting this lesson, complete:

- Introduction to Linux
- Linux History and Open Source
- Linux Fundamentals — Distributions and Architecture
- Linux Kernel Explained
- Linux Desktop vs Server Editions
- Linux Installation
- Linux Boot Process
- First Login and Terminal

---

# Why Learn the Linux Directory Structure?

Unlike Windows, Linux does **not** organize files using drive letters like:

```
C:\
D:\
E:\
```

Instead, everything starts from a **single root directory (`/`)**.

Understanding where Linux stores system files, logs, user data, and applications is one of the most important skills for every Linux administrator.

Whether you're:

- Troubleshooting a server
- Deploying applications
- Managing Kubernetes
- Configuring Docker
- Working in the cloud

you'll constantly navigate the Linux filesystem.

---

# What is FHS?

**FHS** stands for **Filesystem Hierarchy Standard**.

It defines where files and directories should be stored in Linux.

Because of FHS:

- Ubuntu
- Debian
- Rocky Linux
- RHEL
- Fedora

all organize their files similarly.

This consistency makes Linux administration easier across different distributions.

---

# Linux Filesystem Overview

```text
                     /

         (Root Directory)

 ├── bin
 ├── boot
 ├── dev
 ├── etc
 ├── home
 ├── lib
 ├── media
 ├── mnt
 ├── opt
 ├── proc
 ├── root
 ├── run
 ├── sbin
 ├── srv
 ├── sys
 ├── tmp
 ├── usr
 └── var
```

Everything begins at the **Root Directory (`/`)**.

---

# Root Directory (/)

The root directory is the top-most directory in Linux.

It contains every file and directory on the system.

```text
/
```

Do not confuse:

```
/

Root Directory
```

with

```
/root

Root User's Home Directory
```

They are different.

---

# /bin

Contains essential user commands.

Examples:

```bash
ls
cp
mv
cat
mkdir
rm
pwd
echo
```

These commands are available even during system recovery.

---

# /boot

Contains files required during the boot process.

Examples:

- Linux Kernel
- GRUB configuration
- Initramfs

Example:

```bash
ls /boot
```

---

# /dev

Contains device files.

Everything in Linux is treated as a file—including hardware devices.

Examples:

```
/dev/sda

Hard Disk
```

```
/dev/null

Null Device
```

```
/dev/random

Random Number Generator
```

---

# /etc

One of the most important directories.

Contains system configuration files.

Examples:

```
/etc/passwd

User Accounts
```

```
/etc/hostname

Hostname
```

```
/etc/fstab

Filesystem Mounts
```

```
/etc/ssh/

SSH Configuration
```

As a Linux administrator, you'll spend a lot of time inside `/etc`.

---

# /home

Contains home directories for normal users.

Example:

```
/home/basha
```

Each user stores:

- Documents
- Downloads
- Scripts
- Projects
- Personal configuration files

---

# /lib

Contains essential shared libraries required by system programs.

Similar to DLL files in Windows.

---

# /media

Used for automatically mounted removable devices.

Examples:

- USB Drives
- DVDs
- External Hard Disks

---

# /mnt

Temporary mount point.

Administrators commonly mount:

- NFS
- SMB
- Temporary disks

Example:

```bash
sudo mount /dev/sdb1 /mnt
```

---

# /opt

Contains optional third-party software.

Examples:

```
Google Chrome

Oracle Database

Custom Applications
```

---

# /proc

A virtual filesystem.

It doesn't store actual files.

Instead, it provides runtime information about:

- Processes
- Memory
- CPU
- Kernel

Example:

```bash
cat /proc/cpuinfo
```

View memory:

```bash
cat /proc/meminfo
```

---

# /root

Home directory of the **root user**.

Example:

```
/root
```

Normal users should never store files here.

---

# /run

Stores temporary runtime information.

Examples:

- Process IDs
- Runtime sockets
- Lock files

Contents are recreated every boot.

---

# /sbin

Contains essential system administration commands.

Examples:

```bash
shutdown
reboot
mount
fsck
iptables
```

These commands are primarily intended for system administrators.

---

# /srv

Stores data served by system services.

Examples:

- Web Content
- FTP Files
- Application Data

Not all distributions use this directory extensively.

---

# /sys

Virtual filesystem providing information about hardware and kernel devices.

Example:

```bash
ls /sys
```

---

# /tmp

Temporary files.

Applications use this directory for temporary storage.

Files may be deleted automatically after reboot.

Example:

```bash
touch /tmp/test.txt
```

---

# /usr

Contains user applications and libraries.

Subdirectories include:

```
/usr/bin

Applications
```

```
/usr/lib

Libraries
```

```
/usr/share

Documentation
```

Most installed software resides under `/usr`.

---

# /var

Stores variable data.

Examples:

- Logs
- Mail
- Databases
- Cache
- Web Content

Examples:

```
/var/log

System Logs
```

```
/var/lib

Databases
```

```
/var/cache

Application Cache
```

---

# Important Directories for DevOps Engineers

| Directory | Why It Matters |
|-----------|----------------|
| /etc | Configuration |
| /var/log | Logs |
| /home | User Files |
| /opt | Third-party Software |
| /usr | Applications |
| /tmp | Temporary Files |
| /proc | System Information |

---

# Visual Directory Hierarchy

```text
/

├── bin      → Essential Commands
├── boot     → Boot Files
├── dev      → Devices
├── etc      → Configuration
├── home     → User Data
├── lib      → Libraries
├── media    → Removable Media
├── mnt      → Temporary Mounts
├── opt      → Optional Software
├── proc     → Process Information
├── root     → Root User Home
├── run      → Runtime Data
├── sbin     → System Commands
├── srv      → Service Data
├── sys      → Kernel Information
├── tmp      → Temporary Files
├── usr      → User Programs
└── var      → Logs & Variable Data
```

---

# Hands-on Lab

Explore your Linux filesystem.

List root directories:

```bash
ls /
```

Display current directory:

```bash
pwd
```

Navigate to configuration files:

```bash
cd /etc
ls
```

View logs:

```bash
cd /var/log
ls
```

Display CPU information:

```bash
cat /proc/cpuinfo
```

Display memory information:

```bash
cat /proc/meminfo
```

Return to home:

```bash
cd ~
```

---

# Production Perspective

Understanding the Linux directory structure is critical when troubleshooting production systems.

Examples:

| Task | Directory |
|------|-----------|
| Check SSH configuration | `/etc/ssh` |
| Investigate system logs | `/var/log` |
| Verify installed applications | `/usr/bin` |
| Inspect mounted filesystems | `/etc/fstab` |
| Analyze hardware | `/proc` and `/sys` |
| Review application data | `/var/lib` |

When responding to incidents, knowing where to look can significantly reduce troubleshooting time.

---

# Best Practices

- Never modify system files without understanding their purpose.
- Store personal files in your home directory.
- Keep application configuration under `/etc`.
- Regularly monitor `/var/log` for system events.
- Avoid storing important data in `/tmp`.

---

# Common Mistakes

❌ Confusing `/` with `/root`.

✅ `/` is the root of the filesystem, while `/root` is the home directory of the root user.

---

❌ Storing application data in system directories.

✅ Store application data in appropriate locations such as `/var` or user directories.

---

❌ Deleting files from `/etc` without backups.

✅ Always back up configuration files before making changes.

---

# Interview Questions
## Beginner

1. What is the root directory in Linux?
2. What does FHS stand for?
3. Which directory stores configuration files?
4. Which directory contains user home directories?
5. Where are Linux logs stored?

---

## Intermediate

1. Explain the purpose of `/proc`.
2. What is the difference between `/media` and `/mnt`?
3. Why does Linux use a single directory hierarchy?

---

## Architect Level

1. How does understanding FHS help in production troubleshooting?
2. Why is maintaining a standard filesystem hierarchy important across Linux distributions?
3. Which directories would you inspect during a production incident involving a web server?

---

# Summary

In this lesson, you learned:

- What the Filesystem Hierarchy Standard (FHS) is
- The purpose of each major Linux directory
- Where Linux stores configuration files, logs, applications, and user data
- How the Linux filesystem supports administration and troubleshooting

Understanding the Linux directory structure is a foundational skill that you'll use throughout your Linux, Cloud, DevOps, and Platform Engineering journey.

---

## Key Takeaways

- Linux uses a single hierarchical filesystem rooted at `/`.
- Configuration files are stored in `/etc`.
- User files are stored in `/home`.
- Logs are stored in `/var/log`.
- Runtime system information is available through `/proc` and `/sys`.
- Mastering FHS makes system administration and troubleshooting much easier.

---

## What's Next?

**[Getting Help in Linux (`man`, `info`, `--help`)](getting-help-man-info.md)**

In the next lesson, you'll learn how to:

- Use the `man` command
- Navigate manual pages
- Use the `info` system
- Understand `--help` output
- Find command documentation efficiently
- Become a self-sufficient Linux learner
