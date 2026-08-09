---
title: "Linux Installation (VirtualBox, VMware & Windows Subsystem for Linux)"
description: "Learn how to install Linux using VirtualBox, VMware Workstation, and Windows Subsystem for Linux (WSL). By the end of this lesson, you'll have a fully functional Linux environment ready for the rest of the REBASH Academy Linux Mastery course."
difficulty: beginner
estimated_time: "25 min"
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
  - installation
  - virtualbox
  - vmware
  - wsl
  - beginners
  - rebash-linux-mastery
comments: false
status: ready
---

# Linux Installation (VirtualBox, VMware & Windows Subsystem for Linux)

> Learn how to install Linux using VirtualBox, VMware Workstation, and Windows Subsystem for Linux (WSL). By the end of this lesson, you'll have a fully functional Linux environment ready for the rest of the REBASH Academy Linux Mastery course.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 1: Linux Fundamentals → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 25 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Linux Fundamentals</div>

<div markdown>**Lesson:** 6 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand different ways to install Linux
- Choose the right installation method
- Install Ubuntu using VirtualBox
- Install Ubuntu using VMware Workstation
- Install Ubuntu using WSL on Windows
- Download official Ubuntu ISO images
- Create your first Linux virtual machine

---

# Prerequisites

Before starting this lesson, you should complete:

- Introduction to Linux
- Linux History and Open Source
- Linux Fundamentals — Distributions and Architecture
- Linux Kernel Explained
- Linux Desktop vs Server Editions

---

# Why Learn Linux Installation?

Before learning Linux commands, administration, networking, or shell scripting, you need a Linux environment to practice.

There are several ways to install Linux, each designed for different use cases.

Choosing the right installation method depends on your goals.

---

# Linux Installation Options

There are four common ways to install Linux.

```text
Linux Installation

├── Virtual Machine
│     ├── VirtualBox
│     └── VMware
│
├── Windows Subsystem for Linux (WSL)
│
├── Dual Boot
│
└── Cloud Virtual Machine
```

In this course, we'll focus on the most beginner-friendly options:

- VirtualBox
- VMware Workstation
- Windows Subsystem for Linux (WSL)

We'll cover Cloud Virtual Machines later in the Cloud Engineering learning path.

---

# Which Installation Method Should You Choose?

| Goal | Recommended Method |
|-------|--------------------|
| Beginner | VirtualBox |
| Windows User | WSL |
| VMware User | VMware Workstation |
| DevOps Practice | Ubuntu Server VM |
| Cloud Engineer | Ubuntu Server VM |
| Production Practice | Ubuntu Server |

---

# Method 1: Install Linux using VirtualBox

VirtualBox is a free virtualization software that allows you to run Linux inside Windows, macOS, or another Linux system.

## Advantages

- Free
- Beginner-friendly
- Easy snapshots
- Safe learning environment
- Multiple virtual machines

---

## Step 1: Download VirtualBox

Download the latest version from the official Oracle VirtualBox website.

Install VirtualBox using the default settings.

---

## Step 2: Download Ubuntu ISO

Download the latest Ubuntu LTS ISO from the official Ubuntu website.

Recommended:

Ubuntu 24.04 LTS (or the latest Long-Term Support version available)

---

## Step 3: Create a New Virtual Machine

Click:

```
New
```

Configuration:

| Setting | Recommended Value |
|----------|------------------|
| Name | Ubuntu Server |
| Type | Linux |
| Version | Ubuntu (64-bit) |
| RAM | 4 GB |
| CPU | 2 vCPUs |
| Disk | 30 GB (VDI, Dynamically Allocated) |

---

## Step 4: Attach ISO

Open:

```
Settings

↓

Storage

↓

Choose Ubuntu ISO
```

---

## Step 5: Start Installation

Power on the VM.

Select:

```
Try or Install Ubuntu
```

Follow the installation wizard.

---

# Method 2: Install Linux using VMware Workstation

VMware Workstation is another popular virtualization platform.

Many enterprises use VMware for development and testing.

---

## Create New VM

```
Create New Virtual Machine

↓

Typical Installation

↓

Select Ubuntu ISO

↓

Ubuntu

↓

20-30 GB Disk

↓

Finish
```

---

## Recommended Resources

| Resource | Value |
|----------|-------|
| CPU | 2 |
| Memory | 4 GB |
| Disk | 30 GB |

---

# Method 3: Install Linux using WSL

Windows Subsystem for Linux allows Linux to run directly inside Windows.

It is one of the easiest ways to learn Linux.

---

## Check WSL Status

Open PowerShell as Administrator.

Run:

```powershell
wsl --status
```

---

## Install WSL

If WSL is not installed:

```powershell
wsl --install
```

Restart your computer.

---

## Install Ubuntu

List available distributions:

```powershell
wsl --list --online
```

Install Ubuntu:

```powershell
wsl --install Ubuntu
```

---

## Verify Installation

Open Ubuntu.

Run:

```bash
uname -a
```

Check OS version:

```bash
cat /etc/os-release
```

---

# Virtual Machine vs WSL

| Feature | Virtual Machine | WSL |
|----------|----------------|-----|
| Complete Linux OS | ✅ | Partial Integration |
| GUI Support | Yes | Limited |
| Performance | Good | Excellent |
| Snapshots | Yes | No |
| Production Simulation | Better | Good |
| Resource Usage | Higher | Lower |

For this course, VirtualBox or VMware is recommended because they simulate a complete Linux server environment.

---

# Recommended VM Configuration

For Ubuntu Server:

| Resource | Recommended |
|----------|-------------|
| CPU | 2 vCPUs |
| RAM | 4 GB |
| Storage | 30 GB |
| Network | NAT |
| Graphics | Default |

---

# Verify Installation

After installation:

Display OS information:

```bash
cat /etc/os-release
```

Display kernel version:

```bash
uname -r
```

Display hostname:

```bash
hostnamectl
```

Check logged-in user:

```bash
whoami
```

Display current directory:

```bash
pwd
```

If these commands work successfully, your Linux installation is ready.

---

# Production Perspective

Enterprise engineers rarely use desktop Linux systems in production.

Instead, they manage:

- Cloud Virtual Machines
- Kubernetes Nodes
- Bare-metal Servers
- Virtual Machines
- Container Hosts

Learning Linux in a virtual machine closely resembles working in production environments.

---

# Hands-on Lab

## Task 1

Install Ubuntu Server using:

- VirtualBox **or**
- VMware

---

## Task 2

Log in to your Linux machine.

Run:

```bash
hostnamectl
```

---

## Task 3

Check your kernel version.

```bash
uname -r
```

---

## Task 4

Display operating system details.

```bash
cat /etc/os-release
```

---

## Task 5

Create your first directory.

```bash
mkdir rebash-labs
```

Verify:

```bash
ls
```

---

# Best Practices

- Use Ubuntu LTS releases for learning.
- Allocate at least 4 GB RAM if possible.
- Keep snapshots before major changes.
- Practice using the terminal instead of GUI tools.
- Avoid logging in as the root user.

---

# Common Mistakes

❌ Allocating too little memory.

✅ Allocate at least 4 GB RAM for a smoother experience.

---

❌ Forgetting to mount the ISO before starting the VM.

✅ Always verify that the Ubuntu ISO is attached.

---

❌ Using Desktop edition for server administration practice.

✅ Prefer Ubuntu Server for learning Cloud and DevOps.

---

❌ Ignoring snapshots.

✅ Create snapshots before experimenting with system configurations.

---

# Interview Questions
## Beginner

1. What is VirtualBox?
2. What is VMware?
3. What is WSL?
4. Which Linux installation method is easiest for Windows users?

---

## Intermediate

1. Compare VirtualBox and VMware.
2. What are the advantages of WSL?
3. Why do DevOps engineers commonly use Ubuntu Server?

---

## Architect Level

1. Why are virtual machines commonly used for learning Linux?
2. When would you recommend WSL over a virtual machine?
3. How would you prepare a Linux lab for a team of engineers?

---

# Summary

In this lesson, you learned:

- Different Linux installation methods
- Installing Linux using VirtualBox
- Installing Linux using VMware
- Installing Linux using WSL
- Recommended virtual machine configuration
- Basic verification commands

You now have a working Linux environment ready for the rest of this course.

---

## Key Takeaways

- VirtualBox is ideal for beginners.
- VMware is widely used in enterprise environments.
- WSL provides an excellent Linux experience on Windows.
- Ubuntu Server is recommended for Cloud and DevOps learning.
- A properly configured Linux lab is essential for hands-on practice.

---

## What's Next?

**[Linux Boot Process](boot-process-and-filesystem-hierarchy.md)**

In the next lesson, you'll learn:

- BIOS vs UEFI
- GRUB Bootloader
- Linux Kernel Loading
- Initramfs
- systemd
- Boot Targets
- Boot Troubleshooting
