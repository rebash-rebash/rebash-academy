---
title: "Flatpak — Universal Package Management for Linux Applications"
description: "Install and manage Flatpak apps — add Flathub, work with runtimes, update and uninstall, override permissions, and compare Flatpak with Snap."
difficulty: intermediate
estimated_time: "55 min"
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
  - flatpak
  - flathub
  - packages
  - sandboxing
  - rebash-linux-mastery
comments: false
status: ready
---

# Flatpak — Universal Package Management for Linux Applications

> **Flatpak** is a universal package management system designed to distribute Linux desktop applications across different Linux distributions. It packages applications with their required runtimes, runs them in isolated sandboxes, and enables developers to distribute software independently of the underlying operating system. Flatpak is widely used on desktop Linux systems and is an excellent alternative to Snap for cross-distribution software deployment.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 7: Package Management → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 55 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Package Management</div>

<div markdown>**Lesson:** 6 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Flatpak
- Install Flatpak
- Configure Flatpak repositories
- Install applications
- Update and remove applications
- Understand Flatpak runtimes
- Compare Flatpak with Snap
- Apply Flatpak in real-world environments

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management and Permissions
- Module 5 – Users and Groups
- Module 6 – Process Management
- Module 7 Lessons 1–5

---

# Why Learn Flatpak?

Imagine you want to install:

- Visual Studio Code
- Discord
- Spotify
- LibreOffice
- OBS Studio
- GIMP

Different Linux distributions have different package managers.

Wouldn't it be useful if one package worked on all of them?

That's exactly what Flatpak provides.

---

# What is Flatpak?

Flatpak is a universal package management system that enables applications to run consistently across multiple Linux distributions.

Each Flatpak application includes:

- Application binaries
- Required libraries
- Metadata
- Permissions
- Runtime information

Applications execute inside isolated sandboxes.

---

# How Flatpak Works

```text
Flatpak Repository
        │
        ▼
Download Application
        │
        ▼
Install Runtime
        │
        ▼
Install Application
        │
        ▼
Run Inside Sandbox
```

---

# What is a Runtime?

Unlike Snap,

Flatpak separates:

```text
Application

↓

Runtime
```

A **runtime** is a shared collection of libraries used by multiple Flatpak applications.

Benefits:

- Reduced disk usage
- Faster downloads
- Shared dependencies
- Easier updates

---

# Install Flatpak

Ubuntu/Debian:

```bash
sudo apt install flatpak
```

RHEL/Rocky/AlmaLinux:

```bash
sudo dnf install flatpak
```

Fedora:

```bash
sudo dnf install flatpak
```

---

# Add the Flathub Repository

Flathub is the most popular Flatpak application repository.

```bash
flatpak remote-add --if-not-exists flathub \
https://flathub.org/repo/flathub.flatpakrepo
```

---

# View Configured Repositories

```bash
flatpak remotes
```

Example:

```text
flathub
```

---

# Search for Applications

Search for VLC.

```bash
flatpak search vlc
```

Example:

```text
VLC

Media Player
```

---

# Install an Application

Install VLC.

```bash
flatpak install flathub org.videolan.VLC
```

Install GIMP.

```bash
flatpak install flathub org.gimp.GIMP
```

Install LibreOffice.

```bash
flatpak install flathub org.libreoffice.LibreOffice
```

---

# Run an Application

```bash
flatpak run org.videolan.VLC
```

---

# List Installed Applications

```bash
flatpak list
```

Example:

```text
Application

Version

Runtime
```

---

# Update Applications

Update all installed Flatpak applications.

```bash
flatpak update
```

Update a specific application.

```bash
flatpak update org.videolan.VLC
```

---

# Remove an Application

```bash
flatpak uninstall org.videolan.VLC
```

---

# Remove Unused Runtimes

```bash
flatpak uninstall --unused
```

This removes runtimes that are no longer required.

---

# View Application Information

```bash
flatpak info org.videolan.VLC
```

Displays:

- Version
- Runtime
- Installation location
- Permissions

---

# List Installed Runtimes

```bash
flatpak list --runtime
```

---

# View Permissions

Display application permissions.

```bash
flatpak info --show-permissions org.videolan.VLC
```

---

# Override Permissions

Grant access to the Downloads directory.

```bash
flatpak override \
--filesystem=~/Downloads \
org.videolan.VLC
```

---

# Common Commands

Search applications.

```bash
flatpak search gimp
```

Install application.

```bash
flatpak install flathub org.gimp.GIMP
```

Run application.

```bash
flatpak run org.gimp.GIMP
```

Update applications.

```bash
flatpak update
```

Remove application.

```bash
flatpak uninstall org.gimp.GIMP
```

---

# Real Production Examples

Install Visual Studio Code.

```bash
flatpak install flathub com.visualstudio.code
```

Install OBS Studio.

```bash
flatpak install flathub com.obsproject.Studio
```

Install Discord.

```bash
flatpak install flathub com.discordapp.Discord
```

Install GIMP.

```bash
flatpak install flathub org.gimp.GIMP
```

---

# Production Perspective

Flatpak is commonly used for:

- Linux desktop systems
- Developer workstations
- Cross-distribution software deployment
- GUI applications
- Open-source desktop software
- Educational environments

Traditional package managers remain the preferred choice for core operating system packages and server software.

---

# Hands-on Lab

## Task 1

Install Flatpak.

```bash
sudo apt install flatpak
```

---

## Task 2

Add the Flathub repository.

```bash
flatpak remote-add --if-not-exists flathub \
https://flathub.org/repo/flathub.flatpakrepo
```

---

## Task 3

Verify configured repositories.

```bash
flatpak remotes
```

---

## Task 4

Search for VLC.

```bash
flatpak search vlc
```

---

## Task 5

Install VLC.

```bash
flatpak install flathub org.videolan.VLC
```

---

## Task 6

List installed applications.

```bash
flatpak list
```

---

## Task 7

Update installed applications.

```bash
flatpak update
```

---

## Task 8

Remove VLC.

```bash
flatpak uninstall org.videolan.VLC
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `flatpak search` | Search applications | Software discovery |
| `flatpak install` | Install application | Deployment |
| `flatpak run` | Launch application | Daily usage |
| `flatpak update` | Update applications | Maintenance |
| `flatpak uninstall` | Remove application | Cleanup |
| `flatpak list` | List installed applications | Inventory |
| `flatpak remotes` | List repositories | Repository management |
| `flatpak info` | Display application details | Verification |

---

# Flatpak vs Snap

| Feature | Flatpak | Snap |
|----------|----------|------|
| Universal Package Format | ✅ | ✅ |
| Sandboxed Applications | ✅ | ✅ |
| Automatic Updates | Manual (`flatpak update`) by default | Automatic by default |
| Shared Runtimes | ✅ | ❌ (bundled dependencies) |
| Primary Focus | Desktop applications | Desktop and server applications |
| Popular Repository | Flathub | Snap Store |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A developer installs GIMP using Flatpak.

```bash
flatpak install flathub org.gimp.GIMP
```

The application cannot access files in the user's Documents folder.

Investigation:

```bash
flatpak info --show-permissions org.gimp.GIMP
```

The required filesystem permission is missing.

Solution:

```bash
flatpak override \
--filesystem=~/Documents \
org.gimp.GIMP
```

The application can now access the required files.

---

# Best Practices

- Use **Flathub** as the primary Flatpak repository.
- Keep applications and runtimes updated.
- Remove unused runtimes periodically.
- Review application permissions before granting additional access.
- Use Flatpak primarily for desktop applications rather than core operating system components.

---

# Common Mistakes

❌ Forgetting to add the Flathub repository.

✅ Remember to to add the Flathub repository.

---

❌ Leaving unused runtimes installed.

✅ Do not leave unused runtimes installed.

---

❌ Granting excessive filesystem permissions to applications.

✅ Avoid this mistake: granting excessive filesystem permissions to applications.

---

❌ Using Flatpak for packages better managed by the system package manager.

✅ Avoid using Flatpak for packages better managed by the system package manager when a safer approach exists.

---

# Interview Questions
## Beginner

1. What is Flatpak?
2. What is Flathub?
3. Which command installs a Flatpak application?
4. How do you list installed Flatpak applications?

---

## Intermediate

1. What is a Flatpak runtime?
2. How do you update Flatpak applications?
3. How do you remove unused runtimes?
4. How do you view application permissions?

---

## Architect Level

1. When would you choose Flatpak over Snap?
2. Why are shared runtimes beneficial?
3. How does Flatpak improve application security?

---

# Summary

In this lesson, you learned:

- Flatpak package management
- Installing applications
- Flathub repositories
- Shared runtimes
- Application permissions
- Updating applications
- Sandboxing
- Production best practices

Flatpak provides a secure and portable method for distributing desktop applications across Linux distributions. By separating runtimes from applications and using sandboxing, Flatpak delivers efficient software management while improving compatibility and security.

---

## Key Takeaways

- Flatpak is a universal package management system.
- Flathub is the primary repository for Flatpak applications.
- Flatpak uses shared runtimes to reduce duplication.
- Applications run inside secure sandboxes.
- Use `flatpak install` to install applications.
- Use `flatpak update` to keep applications current.

---

## What's Next?

**[Repository Management — Managing Software Sources in Linux](repository-management.md)**

You'll explore:

- What software repositories are
- Repository configuration
- Adding and removing repositories
- GPG keys and package verification
- Repository priorities
- Enterprise repository management
- Best practices for production systems

Understanding repository management is essential for securely controlling where your Linux systems obtain software updates and packages.
