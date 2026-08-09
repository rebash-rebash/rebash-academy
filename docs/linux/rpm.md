---
title: "RPM (Red Hat Package Manager) — Managing RPM Packages in Linux"
description: "Work with local RPM packages — install, upgrade, query, verify integrity, inspect contents, and understand how RPM relates to DNF and YUM."
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
  - rpm
  - packages
  - rhel
  - verification
  - rebash-linux-mastery
comments: false
status: ready
---

# RPM (Red Hat Package Manager) — Managing RPM Packages in Linux

> **RPM (Red Hat Package Manager)** is the low-level package management system used by Red Hat Enterprise Linux (RHEL), Rocky Linux, AlmaLinux, Fedora, Oracle Linux, and other RPM-based distributions. While **DNF** and **YUM** manage software from repositories, **RPM** works directly with local `.rpm` package files. Linux administrators use RPM to install, verify, query, and inspect software packages.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 7: Package Management → Lesson 4</p>

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

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand RPM
- Install local RPM packages
- Upgrade packages
- Remove packages
- Query installed software
- Verify package integrity
- Inspect package contents
- Understand the relationship between RPM, YUM, and DNF

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management and Permissions
- Module 5 – Users and Groups
- Module 6 – Process Management
- Module 7 Lessons 1–3

---

# Why Learn RPM?

Imagine you receive:

```text
docker-ce-28.0.0.rpm
```

or

```text
custom-agent.rpm
```

from your company.

The package isn't available in any repository.

How do you install it?

The answer is:

```bash
rpm
```

---

# What is RPM?

RPM stands for:

> **Red Hat Package Manager**

It is the package management system used by RPM-based Linux distributions.

RPM works directly with package files.

Example:

```text
nginx-1.24.0-1.el9.x86_64.rpm
```

---

# RPM vs DNF/YUM

```text
RPM

↓

Local Package File

↓

Install Package
```

Whereas:

```text
DNF / YUM

↓

Repository

↓

Download Package

↓

Install Package
```

DNF and YUM use RPM internally to install packages.

---

# RPM Package Structure

An RPM package typically contains:

- Executable files
- Libraries
- Configuration files
- Documentation
- Metadata
- Package scripts

---

# Install an RPM Package

```bash
sudo rpm -ivh package.rpm
```

Example:

```bash
sudo rpm -ivh nginx.rpm
```

Options:

| Option | Meaning |
|---------|----------|
| `-i` | Install |
| `-v` | Verbose output |
| `-h` | Display progress bar |

---

# Upgrade an RPM Package

```bash
sudo rpm -Uvh package.rpm
```

Example:

```bash
sudo rpm -Uvh nginx.rpm
```

If the package already exists:

- Upgrade

Otherwise:

- Install

---

# Fresh Install Only

Prevent upgrades.

```bash
sudo rpm -ivh package.rpm
```

Fails if the package is already installed.

---

# Remove a Package

```bash
sudo rpm -e package-name
```

Example:

```bash
sudo rpm -e nginx
```

Use the package name—not the `.rpm` filename.

---

# Query Installed Packages

List all installed packages.

```bash
rpm -qa
```

Example:

```text
bash

git

nginx

vim
```

---

# Search Installed Packages

```bash
rpm -qa | grep nginx
```

---

# Display Package Information

```bash
rpm -qi nginx
```

Displays:

- Version
- Release
- Architecture
- Install date
- Vendor
- Description

---

# List Files Installed by a Package

```bash
rpm -ql nginx
```

Example:

```text
/etc/nginx

/usr/sbin/nginx

/usr/share/doc
```

---

# Find Which Package Owns a File

```bash
rpm -qf /usr/bin/bash
```

Output:

```text
bash
```

Useful when troubleshooting system files.

---

# Verify an Installed Package

```bash
rpm -V nginx
```

RPM compares installed files against package metadata.

If nothing is displayed,

the package matches the expected state.

---

# Query an RPM File

Without installing:

```bash
rpm -qpi package.rpm
```

Display package contents.

```bash
rpm -qpl package.rpm
```

---

# Verify Package Signature

```bash
rpm -K package.rpm
```

This checks package integrity and signature information.

---

# Common Commands

Install package.

```bash
sudo rpm -ivh package.rpm
```

Upgrade package.

```bash
sudo rpm -Uvh package.rpm
```

Remove package.

```bash
sudo rpm -e package-name
```

List packages.

```bash
rpm -qa
```

Package information.

```bash
rpm -qi package-name
```

List package files.

```bash
rpm -ql package-name
```

---

# Real Production Examples

Install a monitoring agent.

```bash
sudo rpm -ivh monitoring-agent.rpm
```

Upgrade Kubernetes tools.

```bash
sudo rpm -Uvh kubectl.rpm
```

Verify Docker installation.

```bash
rpm -qi docker
```

Identify the package that owns a binary.

```bash
rpm -qf /usr/bin/ssh
```

---

# Production Perspective

RPM is commonly used for:

- Installing vendor-provided software
- Offline package installation
- Enterprise software deployment
- Custom internal packages
- Troubleshooting package ownership
- Package verification
- Security auditing

Although DNF is preferred for repository-based installations, RPM is essential when working with standalone package files.

---

# Hands-on Lab

## Task 1

List installed packages.

```bash
rpm -qa
```

---

## Task 2

Search for Bash.

```bash
rpm -qa | grep bash
```

---

## Task 3

View package information.

```bash
rpm -qi bash
```

---

## Task 4

List installed files.

```bash
rpm -ql bash
```

---

## Task 5

Identify which package owns `/usr/bin/bash`.

```bash
rpm -qf /usr/bin/bash
```

---

## Task 6

Verify the Bash package.

```bash
rpm -V bash
```

---

## Task 7

Display information from an RPM file.

```bash
rpm -qpi package.rpm
```

*(Replace `package.rpm` with an actual RPM file.)*

---

## Task 8

Verify an RPM package signature.

```bash
rpm -K package.rpm
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `rpm -ivh` | Install RPM package | Offline installation |
| `rpm -Uvh` | Upgrade package | Software updates |
| `rpm -e` | Remove package | Package cleanup |
| `rpm -qa` | List installed packages | Inventory |
| `rpm -qi` | Package information | Verification |
| `rpm -ql` | List package files | File inspection |
| `rpm -qf` | Identify package owner | Troubleshooting |
| `rpm -V` | Verify package integrity | Security auditing |
| `rpm -K` | Verify RPM signature | Package validation |

---

# RPM vs DNF vs YUM

| Feature | RPM | DNF | YUM |
|----------|-----|-----|-----|
| Package Format | `.rpm` | `.rpm` | `.rpm` |
| Repository Support | ❌ | ✅ | ✅ |
| Dependency Resolution | ❌ | ✅ | ✅ |
| Install Local RPM | ✅ | ✅ | ✅ |
| Package Queries | ✅ | ✅ | ✅ |
| Package Verification | ✅ | Limited | Limited |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A vendor provides:

```text
security-agent.rpm
```

The administrator installs it.

```bash
sudo rpm -ivh security-agent.rpm
```

Installation fails.

Error:

```text
Failed dependencies
```

Investigation:

RPM does not automatically resolve dependencies.

Solution:

Use:

```bash
sudo dnf install ./security-agent.rpm
```

or

```bash
sudo yum localinstall security-agent.rpm
```

These tools automatically download and install required dependencies.

---

# Best Practices

- Prefer DNF or YUM for repository-managed software.
- Use RPM for local or vendor-provided packages.
- Verify package signatures before installation.
- Check package ownership when troubleshooting files.
- Verify installed packages regularly for integrity.

---

# Common Mistakes

❌ Using RPM to install packages with unresolved dependencies.

✅ Avoid using RPM to install packages with unresolved dependencies when a safer approach exists.

---

❌ Removing critical packages without checking dependencies.

✅ Avoid this mistake: removing critical packages without checking dependencies.

---

❌ Installing unsigned packages from untrusted sources.

✅ Avoid this mistake: installing unsigned packages from untrusted sources.

---

❌ Confusing package names with RPM filenames.

✅ Distinguish clearly between package names with RPM filenames.

---

# Interview Questions
## Beginner

1. What does RPM stand for?
2. Which command installs an RPM package?
3. How do you list installed packages?
4. How do you remove an RPM package?

---

## Intermediate

1. What is the difference between `rpm -ivh` and `rpm -Uvh`?
2. How do you determine which package owns a file?
3. How do you verify package integrity?
4. Why do DNF and YUM generally provide a better installation experience than RPM alone?

---

## Architect Level

1. When would you use RPM instead of DNF?
2. How would you securely deploy vendor-provided RPM packages across enterprise servers?
3. How would you validate the authenticity and integrity of an RPM package before deployment?

---

# Summary

In this lesson, you learned:

- RPM package management
- Installing local RPM packages
- Package upgrades
- Package removal
- Package queries
- Package verification
- Package ownership
- Production best practices

RPM is the foundation of package management on RPM-based Linux systems. While DNF and YUM simplify dependency management and repository integration, RPM provides powerful tools for working directly with package files, verifying installations, and troubleshooting package-related issues.

---

## Key Takeaways

- RPM is the low-level package manager for RPM-based distributions.
- Use `rpm -ivh` to install local RPM packages.
- Use `rpm -Uvh` to upgrade existing packages.
- Use `rpm -qa` to list installed packages.
- Use `rpm -qf` to identify the package that owns a file.
- Use `rpm -V` and `rpm -K` to verify package integrity and authenticity.

---

## What's Next?

**[Snap — Universal Package Management for Linux](snap.md)**

You'll explore:

- What Snap packages are
- Installing and removing Snap applications
- Managing Snap channels
- Automatic updates
- Sandboxed applications
- Differences between Snap and traditional package managers
- Production and desktop use cases

Snap provides a universal package format that allows applications to run consistently across multiple Linux distributions.
