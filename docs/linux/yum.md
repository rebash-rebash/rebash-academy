---
title: "YUM (Yellowdog Updater Modified) — Package Management for Legacy RHEL Systems"
description: "Manage legacy RPM packages with YUM — install, update, search, clean cache, review history, and compare YUM with DNF on RHEL 7 and CentOS 7."
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 7 · Package Management"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - yum
  - rpm
  - rhel
  - packages
  - rebash-linux-mastery
comments: false
status: ready
---

# YUM (Yellowdog Updater Modified) — Package Management for Legacy RHEL Systems

> **YUM (Yellowdog Updater Modified)** is the traditional package manager used by older versions of Red Hat Enterprise Linux (RHEL), CentOS, Oracle Linux, and other RPM-based Linux distributions. Although modern distributions use **DNF** as the default package manager, YUM remains important because many enterprise environments continue to run legacy Linux servers. Understanding YUM is essential for maintaining older production systems and supporting enterprise infrastructure.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 7: Package Management → Lesson 3</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 50 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Package Management</div>

<div markdown>**Lesson:** 3 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand YUM
- Install and remove packages
- Update software
- Search package repositories
- Manage repositories
- View package history
- Compare YUM and DNF
- Maintain legacy Linux systems

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management and Permissions
- Module 5 – Users and Groups
- Module 6 – Process Management
- Module 7 Lessons 1–2

---

# Why Learn YUM?

Although DNF has replaced YUM on modern systems, many organizations still run:

- RHEL 7
- CentOS 7
- Oracle Linux 7
- Legacy enterprise servers

As a Linux administrator or DevOps engineer, you'll often encounter environments where YUM is still the standard package manager.

---

# What is YUM?

YUM stands for:

> **Yellowdog Updater Modified**

It is a package manager for RPM-based Linux distributions.

YUM works with:

```text
.rpm
```

packages and automatically:

- Resolves dependencies
- Downloads packages
- Installs software
- Removes packages
- Updates software

---

# Package Management Workflow

```text
YUM Command
      │
      ▼
Repository
      │
      ▼
Download Package
      │
      ▼
Resolve Dependencies
      │
      ▼
Install Package
      │
      ▼
Ready to Use
```

---

# Check for Available Updates

```bash
sudo yum check-update
```

This refreshes package metadata and displays available package updates.

---

# Install a Package

Install NGINX.

```bash
sudo yum install nginx
```

Install multiple packages.

```bash
sudo yum install git curl vim
```

YUM automatically installs required dependencies.

---

# Update Packages

Update all installed packages.

```bash
sudo yum update
```

Update a specific package.

```bash
sudo yum update nginx
```

---

# Remove a Package

```bash
sudo yum remove nginx
```

Unused dependencies may remain and should be reviewed separately.

---

# Search for Packages

```bash
yum search nginx
```

Example:

```text
nginx

nginx-all-modules

nginx-filesystem
```

---

# View Package Information

```bash
yum info nginx
```

Displays:

- Version
- Repository
- Description
- Size
- Architecture

---

# List Installed Packages

```bash
yum list installed
```

Find a package.

```bash
yum list installed | grep nginx
```

---

# List Enabled Repositories

```bash
yum repolist
```

Example:

```text
base

extras

updates
```

---

# Clean Package Cache

Remove cached packages.

```bash
sudo yum clean packages
```

Remove all cached metadata and packages.

```bash
sudo yum clean all
```

Rebuild the cache.

```bash
sudo yum makecache
```

---

# View Package History

Display transaction history.

```bash
yum history
```

View a specific transaction.

```bash
yum history info <ID>
```

Undo a transaction.

```bash
sudo yum history undo <ID>
```

---

# Common Commands

Install package.

```bash
sudo yum install nginx
```

Update packages.

```bash
sudo yum update
```

Remove package.

```bash
sudo yum remove nginx
```

Search package.

```bash
yum search nginx
```

Package information.

```bash
yum info nginx
```

List repositories.

```bash
yum repolist
```

---

# Real Production Examples

Install Git.

```bash
sudo yum install git
```

Install Apache.

```bash
sudo yum install httpd
```

Update production server.

```bash
sudo yum update
```

Install Docker.

```bash
sudo yum install docker
```

---

# Production Perspective

YUM is commonly found on:

- RHEL 7
- CentOS 7
- Oracle Linux 7
- Older enterprise Linux servers
- Legacy production environments

Although DNF is now the default package manager on newer releases, many enterprise systems continue to rely on YUM.

---

# Hands-on Lab

## Task 1

List enabled repositories.

```bash
yum repolist
```

---

## Task 2

Search for Git.

```bash
yum search git
```

---

## Task 3

View package details.

```bash
yum info git
```

---

## Task 4

Check for updates.

```bash
sudo yum check-update
```

---

## Task 5

Install Git (if not already installed).

```bash
sudo yum install git
```

---

## Task 6

Verify installation.

```bash
git --version
```

---

## Task 7

View package history.

```bash
yum history
```

---

## Task 8

Clean the package cache.

```bash
sudo yum clean all
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `yum install` | Install packages | Software deployment |
| `yum update` | Update packages | Security patching |
| `yum remove` | Remove packages | Cleanup |
| `yum search` | Search packages | Package discovery |
| `yum info` | Package details | Verification |
| `yum repolist` | View repositories | Repository management |
| `yum history` | View transactions | Auditing |
| `yum clean all` | Clear cache | Maintenance |

---

# YUM vs DNF

| Feature | YUM | DNF |
|----------|-----|-----|
| Default On | RHEL/CentOS 7 | RHEL/Rocky/AlmaLinux 8+ and Fedora |
| Package Format | `.rpm` | `.rpm` |
| Dependency Resolution | Good | Improved |
| Performance | Good | Faster and more efficient |
| Transaction History | ✅ | ✅ |
| Active Development | Maintenance only | Active development |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A system administrator attempts to install Docker.

```bash
sudo yum install docker
```

Error:

```text
No package docker available.
```

Investigation:

```bash
yum repolist
```

The required repository is not enabled.

After enabling the correct repository:

```bash
sudo yum makecache

sudo yum install docker
```

The installation completes successfully.

---

# Best Practices

- Apply package updates regularly.
- Use only trusted repositories.
- Clean the package cache periodically.
- Review package dependencies before installation.
- Plan migrations from YUM-based systems to DNF-supported platforms where appropriate.

---

# Common Mistakes

❌ Using outdated repositories.

✅ Avoid using outdated repositories when a safer approach exists.

---

❌ Ignoring security updates.

✅ Always review security updates.

---

❌ Installing packages from untrusted sources.

✅ Avoid this mistake: installing packages from untrusted sources.

---

❌ Assuming every RPM-based distribution uses DNF.

✅ Older enterprise systems may still rely on YUM.

---

# Interview Questions
## Beginner

1. What does YUM stand for?
2. Which Linux distributions traditionally use YUM?
3. Which command installs a package?
4. How do you search for a package?

---

## Intermediate

1. What is the difference between `yum update` and `yum check-update`?
2. How do you view enabled repositories?
3. How do you view package history?
4. How do you remove a package?

---

## Architect Level

1. Why is YUM still relevant in enterprise environments?
2. How would you manage package updates across legacy RHEL servers?
3. What factors would you consider when migrating from YUM to DNF?

---

# Summary

In this lesson, you learned:

- YUM package management
- Package installation
- Package updates
- Repository management
- Package history
- Cache management
- Legacy enterprise Linux administration

YUM remains an important tool for maintaining older RPM-based Linux systems. While DNF has become the standard package manager on modern Red Hat-based distributions, understanding YUM enables you to support legacy enterprise environments and smoothly transition to newer platforms.

---

## Key Takeaways

- YUM is the traditional package manager for older RPM-based Linux distributions.
- Use `yum install` to install software.
- Use `yum update` to apply package updates.
- Use `yum search` and `yum info` to discover packages.
- Use `yum repolist` to view configured repositories.
- Many enterprise environments continue to use YUM on legacy systems.

---

## What's Next?

**[RPM (Red Hat Package Manager) — Managing RPM Packages in Linux](rpm.md)**

You'll explore:

- What RPM is
- Installing local RPM packages
- Querying installed packages
- Verifying package integrity
- Viewing package contents
- Differences between RPM and YUM/DNF
- Production package management using RPM

Understanding RPM will help you work directly with package files and troubleshoot package-related issues on RPM-based Linux systems.
