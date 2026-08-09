---
title: "DNF (Dandified YUM) — Package Management in RHEL, Rocky, AlmaLinux, and Fedora"
description: "Manage RPM packages with DNF — install, upgrade, search, clean cache, review history, and compare DNF with APT for RHEL-based systems."
difficulty: intermediate
estimated_time: "60 min"
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
  - dnf
  - rpm
  - rhel
  - packages
  - rebash-linux-mastery
comments: false
status: ready
---

# DNF (Dandified YUM) — Package Management in RHEL, Rocky, AlmaLinux, and Fedora

> **DNF (Dandified YUM)** is the modern package manager used by Fedora, Red Hat Enterprise Linux (RHEL), Rocky Linux, AlmaLinux, and other RPM-based distributions. It simplifies installing, updating, removing, and managing software packages while providing better dependency resolution, improved performance, and enhanced security compared to its predecessor, YUM.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 7: Package Management → Lesson 2</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 60 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Package Management</div>

<div markdown>**Lesson:** 2 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand DNF
- Install and remove software packages
- Search package repositories
- Update installed software
- Manage dependencies
- View package information
- Clean package cache
- Apply package management in production

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management and Permissions
- Module 5 – Users and Groups
- Module 6 – Process Management
- Module 7 Lesson 1 – APT

---

# Why Learn DNF?

Imagine you're managing:

- Red Hat Enterprise Linux servers
- Rocky Linux production systems
- AlmaLinux cloud instances
- Fedora developer workstations

You need to:

- Install Docker
- Update Kubernetes tools
- Patch security vulnerabilities
- Remove unused software

DNF makes these tasks simple and reliable.

---

# What is DNF?

DNF stands for:

> **Dandified YUM**

It is the default package manager for modern RPM-based Linux distributions.

DNF works with:

```text
.rpm
```

packages and automatically:

- Resolves dependencies
- Downloads packages
- Verifies package signatures
- Installs software
- Manages updates

---

# Package Management Workflow

```text
DNF Command
      │
      ▼
Software Repository
      │
      ▼
Download Packages
      │
      ▼
Resolve Dependencies
      │
      ▼
Install Software
      │
      ▼
Ready to Use
```

---

# What is an RPM Package?

An RPM package contains:

- Executable binaries
- Libraries
- Configuration files
- Documentation
- Metadata

Example:

```text
nginx-1.24.0-1.el9.x86_64.rpm
```

---

# Refresh Repository Metadata

Before installing packages:

```bash
sudo dnf check-update
```

This checks repositories for available updates and refreshes package metadata if needed.

---

# Install a Package

Example:

```bash
sudo dnf install nginx
```

Install multiple packages.

```bash
sudo dnf install git curl vim
```

DNF automatically resolves dependencies.

---

# Upgrade Installed Packages

Upgrade all installed packages.

```bash
sudo dnf upgrade
```

or

```bash
sudo dnf update
```

Both commands are equivalent in modern DNF.

---

# Upgrade a Specific Package

```bash
sudo dnf upgrade nginx
```

---

# Remove a Package

```bash
sudo dnf remove nginx
```

Unused dependencies are removed when appropriate.

---

# Search for Packages

```bash
dnf search nginx
```

Example:

```text
nginx

nginx-core

nginx-filesystem
```

---

# View Package Information

```bash
dnf info nginx
```

Displays:

- Version
- Repository
- Size
- Description
- Architecture

---

# List Installed Packages

```bash
dnf list installed
```

Search for a package.

```bash
dnf list installed | grep nginx
```

---

# Check Available Updates

```bash
dnf check-update
```

Displays packages that have newer versions available.

---

# Display Package Repositories

```bash
dnf repolist
```

Example:

```text
AppStream

BaseOS

Extras
```

---

# Clean Package Cache

Remove cached packages.

```bash
sudo dnf clean packages
```

Remove all cached metadata and packages.

```bash
sudo dnf clean all
```

Rebuild the cache.

```bash
sudo dnf makecache
```

---

# Download a Package Without Installing

```bash
sudo dnf download nginx
```

!!! note "Note"

    The `dnf download` command is provided by the **dnf-plugins-core** package on many distributions.

---

# View Package History

Display transaction history.

```bash
dnf history
```

Example:

```text
ID

Command

Date

Action
```

View details of a transaction.

```bash
dnf history info <ID>
```

---

# Undo a Transaction

```bash
sudo dnf history undo <ID>
```

This attempts to reverse a previous package transaction.

---

# Common Commands

Install package.

```bash
sudo dnf install nginx
```

Upgrade packages.

```bash
sudo dnf upgrade
```

Remove package.

```bash
sudo dnf remove nginx
```

Search package.

```bash
dnf search nginx
```

Display package information.

```bash
dnf info nginx
```

List repositories.

```bash
dnf repolist
```

---

# Real Production Examples

Install Git.

```bash
sudo dnf install git
```

Install Docker.

```bash
sudo dnf install docker
```

Update production server.

```bash
sudo dnf upgrade
```

Install Kubernetes CLI.

```bash
sudo dnf install kubectl
```

---

# Production Perspective

DNF is widely used for:

- Red Hat Enterprise Linux
- Rocky Linux
- AlmaLinux
- Fedora
- Cloud Virtual Machines
- Kubernetes Nodes
- Enterprise Servers
- Production Infrastructure

Keeping packages updated is essential for security and stability.

---

# Hands-on Lab

## Task 1

List enabled repositories.

```bash
dnf repolist
```

---

## Task 2

Search for Git.

```bash
dnf search git
```

---

## Task 3

View package details.

```bash
dnf info git
```

---

## Task 4

Check for updates.

```bash
sudo dnf check-update
```

---

## Task 5

Install Git (if not already installed).

```bash
sudo dnf install git
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
dnf history
```

---

## Task 8

Clean the package cache.

```bash
sudo dnf clean all
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `dnf install` | Install packages | Software deployment |
| `dnf upgrade` | Upgrade installed packages | Security patching |
| `dnf remove` | Remove software | Cleanup |
| `dnf search` | Search repositories | Package discovery |
| `dnf info` | Display package information | Verification |
| `dnf repolist` | List repositories | Repository management |
| `dnf history` | View transaction history | Auditing |
| `dnf clean all` | Clear cache | Maintenance |

---

# DNF vs APT

| Feature | APT | DNF |
|----------|-----|-----|
| Package Format | `.deb` | `.rpm` |
| Primary Distributions | Debian, Ubuntu | RHEL, Rocky, AlmaLinux, Fedora |
| Install | `apt install` | `dnf install` |
| Update Metadata | `apt update` | `dnf check-update` / `dnf makecache` |
| Upgrade | `apt upgrade` | `dnf upgrade` |
| Package Info | `apt show` | `dnf info` |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A system administrator attempts to install NGINX.

```bash
sudo dnf install nginx
```

Error:

```text
No match for argument: nginx
```

Investigation:

```bash
dnf repolist
```

The required repository is disabled.

After enabling the correct repository:

```bash
sudo dnf makecache

sudo dnf install nginx
```

The package installs successfully.

---

# Best Practices

- Keep repositories enabled and synchronized.
- Apply security updates regularly.
- Review package changes before upgrading production systems.
- Remove unused software.
- Clean the package cache periodically.
- Use only trusted repositories.

---

# Common Mistakes

❌ Installing packages from untrusted repositories.

✅ Avoid this mistake: installing packages from untrusted repositories.

---

❌ Ignoring available security updates.

✅ Always review available security updates.

---

❌ Cleaning metadata without rebuilding the cache when required.

✅ Avoid this mistake: cleaning metadata without rebuilding the cache when required.

---

❌ Upgrading production servers without testing critical applications.

✅ Avoid this mistake: upgrading production servers without testing critical applications.

---

# Interview Questions
## Beginner

1. What does DNF stand for?
2. Which Linux distributions use DNF?
3. Which command installs a package?
4. How do you search for a package?

---

## Intermediate

1. What is the difference between `dnf upgrade` and `dnf check-update`?
2. How do you list enabled repositories?
3. How do you remove a package?
4. What is the purpose of `dnf history`?

---

## Architect Level

1. How would you manage package updates across hundreds of RHEL servers?
2. Why should production systems use trusted repositories?
3. How would you implement a package update strategy that minimizes downtime?

---

# Summary

In this lesson, you learned:

- DNF package management
- Package installation
- Package upgrades
- Repository management
- Package history
- Package cleanup
- Production best practices

DNF is the modern package manager for RPM-based Linux distributions. It simplifies software management by automatically resolving dependencies, managing repositories, and tracking package transactions. Mastering DNF is essential for administering Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, and Fedora systems.

---

## Key Takeaways

- DNF is the default package manager for modern RPM-based distributions.
- Use `dnf install` to install software.
- Use `dnf upgrade` to apply updates.
- Use `dnf search` and `dnf info` to explore packages.
- Use `dnf history` to review package transactions.
- Use trusted repositories and apply updates regularly.

---

## What's Next?

**[YUM (Yellowdog Updater Modified) — Package Management for Legacy RHEL Systems](yum.md)**

You'll explore:

- What YUM is
- How YUM differs from DNF
- Installing and updating packages
- Repository management
- Legacy RHEL systems
- Migration from YUM to DNF
- Production package management for older enterprise Linux systems
