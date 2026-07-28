---
title: Overview
description: Linux learning track — 25 tutorials from foundations through advanced Linux servers (nginx, TLS, LVM, backups).
difficulty: beginner
estimated_time: "Varies"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
comments: false
---

# Linux

Master the command line, system administration, and shell scripting — from first login to production troubleshooting.

## Overview

The REBASH Academy **Linux** track is the golden foundation for DevOps: a structured curriculum from first login through **production-like app servers** (nginx, TLS, LVM, backups). Each tutorial includes theory, step-by-step labs, commands, best practices, and interview questions.

!!! tip "Learning Path"
    Linux is the first step in the [DevOps Engineer learning path](../learning-paths/index.md).

## Curriculum Plan

Modules and tutorials in order. Use the tables below for links, level, and time estimates.

<figure class="rebash-diagram rebash-tree-diagram" markdown="0">

<p class="rebash-tree-title">Linux Track</p>

<ul class="rebash-tree">
  <li>1 · Foundations
<ul>
  <li>Introduction to Linux</li>
  <li>Linux Filesystem Hierarchy</li>
  <li>Essential Linux Commands</li>
</ul></li>
  <li>2 · Users &amp; Permissions
<ul>
  <li>File Permissions and Ownership</li>
  <li>User and Group Management</li>
</ul></li>
  <li>3 · Processes &amp; Services
<ul>
  <li>Process Management</li>
  <li>systemd Service Management</li>
  <li>Package Management</li>
</ul></li>
  <li>4 · Text &amp; Scripting
<ul>
  <li>Text Processing (grep, sed, awk)</li>
  <li>Shell Scripting Fundamentals</li>
</ul></li>
  <li>5 · Remote Admin
<ul>
  <li>SSH and Remote Administration</li>
  <li>Remote systemd Service Control</li>
</ul></li>
  <li>6 · Storage &amp; Ops
<ul>
  <li>Disk and Filesystem Management</li>
  <li>Log Management with journalctl</li>
  <li>Cron and Task Scheduling</li>
  <li>Environment Variables &amp; Shell Config</li>
  <li>Linux Networking Essentials</li>
  <li>File Archiving and Compression</li>
  <li>Linux Security Hardening Basics</li>
  <li>Troubleshooting Linux Systems</li>
</ul></li>
  <li>7 · Advanced Linux Servers
<ul>
  <li>Linux Server Baseline and Lifecycle</li>
  <li>nginx Web Server and Reverse Proxy</li>
  <li>TLS Certificates on Linux Servers</li>
  <li>Server Storage — LVM and fstab</li>
  <li>Backup, Restore, and Recovery Drills</li>
</ul></li>
</ul>
</figure>



### Module 1 – Foundations

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 1 | [Introduction to Linux](introduction-to-linux.md) | Beginner | 30 min |
| 2 | [Linux Filesystem Hierarchy](linux-filesystem-hierarchy.md) | Beginner | 25 min |
| 3 | [Essential Linux Commands](essential-linux-commands.md) | Beginner | 40 min |

### Module 2 – Users, Groups & Permissions

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 4 | [File Permissions and Ownership](file-permissions-and-ownership.md) | Beginner | 35 min |
| 5 | [User and Group Management](user-and-group-management.md) | Beginner | 35 min |

### Module 3 – Processes, Services & Packages

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 6 | [Process Management](process-management.md) | Intermediate | 40 min |
| 7 | [systemd Service Management](systemd-service-management.md) | Intermediate | 45 min |
| 8 | [Package Management](package-management.md) | Beginner | 35 min |

### Module 4 – Text Processing & Shell Scripting

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 9 | [Text Processing with grep, sed, and awk](text-processing-grep-sed-awk.md) | Intermediate | 50 min |
| 10 | [Shell Scripting Fundamentals](shell-scripting-fundamentals.md) | Intermediate | 60 min |

### Module 5 – Remote Administration

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 11 | [SSH and Remote Administration](ssh-remote-administration.md) | Intermediate | 40 min |
| 12 | [Remote systemd Service Control](remote-systemd-services.md) | Intermediate | 45 min |

### Module 6 – Storage, Logs, Networking & Operations

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 13 | [Disk and Filesystem Management](disk-and-filesystem-management.md) | Intermediate | 45 min |
| 14 | [Log Management with journalctl](log-management-journalctl.md) | Intermediate | 35 min |
| 15 | [Cron and Task Scheduling](cron-and-task-scheduling.md) | Beginner | 30 min |
| 16 | [Environment Variables and Shell Configuration](environment-variables-shell-config.md) | Beginner | 25 min |
| 17 | [Linux Networking Essentials](linux-networking-essentials.md) | Intermediate | 45 min |
| 18 | [File Archiving and Compression](file-archiving-and-compression.md) | Beginner | 25 min |
| 19 | [Linux Security Hardening Basics](linux-security-hardening-basics.md) | Advanced | 55 min |
| 20 | [Troubleshooting Linux Systems](troubleshooting-linux-systems.md) | Advanced | 60 min |

### Module 7 – Advanced Linux Servers

Build and operate a production-like Ubuntu app server: baseline → nginx → TLS → LVM → backups.

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 21 | [Linux Server Baseline and Lifecycle](linux-server-baseline-and-lifecycle.md) | Advanced | 55 min |
| 22 | [nginx Web Server and Reverse Proxy](nginx-web-server-and-reverse-proxy.md) | Advanced | 65 min |
| 23 | [TLS Certificates on Linux Servers](tls-certificates-on-linux-servers.md) | Advanced | 60 min |
| 24 | [Server Storage — LVM and fstab](server-storage-lvm-and-fstab.md) | Advanced | 65 min |
| 25 | [Backup, Restore, and Recovery Drills](backup-restore-and-recovery-drills.md) | Advanced | 55 min |

**Total estimated time:** ~18 hours of hands-on learning (Modules 1–7)

## Learning Objectives

After completing this track, you will be able to:

- [ ] Navigate and administer a Linux server confidently
- [ ] Manage users, permissions, processes, and services
- [ ] Write Bash scripts and process text from the CLI
- [ ] Administer remote servers over SSH and systemd
- [ ] Monitor logs, schedule tasks, and troubleshoot production issues
- [ ] Harden a VM and expose only intended services (SSH/HTTP/HTTPS)
- [ ] Run nginx as a reverse proxy with TLS on a local Ubuntu server
- [ ] Manage LVM storage and prove backup/restore drills

## Who Is This For?

| Audience | Benefit |
|----------|---------|
| **Students** | Build job-ready Linux skills from zero |
| **Developers** | Understand the OS your applications run on |
| **DevOps / SRE** | Foundation for Docker, Kubernetes, and cloud |
| **Sysadmins** | Structured refresher with modern systemd practices |

## Related Sections

- [Networking](../networking/index.md) — next step in the DevOps path
- [Docker](../docker/index.md) — containerize your applications
- [Interview Prep](../interview/index.md) — Linux interview questions

- [Linux Cheat Sheet](../cheatsheets/linux.md)
- [Linux Interview Prep](../interview/linux.md)
- [Linux Fundamentals Quiz](../quizzes/linux-fundamentals.md)
- [Linux Servers Quiz](../quizzes/linux-servers.md)
- [Linux App Server from Zero lab](../labs/linux-app-server-from-zero.md)
- [DevOps Engineer path](../learning-paths/devops-engineer.md)
