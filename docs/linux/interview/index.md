---
title: Interview Preparation
description: "Linux interview hub — themes, story bank from labs, and links to module question sets."
technology_id: linux
hide:
  - toc
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
tags:
  - linux
  - interview
comments: false
---

# Linux — Interview Preparation

Every tutorial ends with **seven Interview Questions** (question visible, answer under **Reveal answer**). Practise plain-English explanations, then add one production detail. Prefer **stories with command evidence** over buzzwords.

## High-frequency themes

| Theme | What to practise | Start here |
|-------|------------------|------------|
| Distro vs kernel | `/etc/os-release`, `uname -r` | [Fundamentals](../linux-fundamentals-distributions-and-architecture.md) |
| FHS + boot | Where files live; who starts services | [Boot & FHS](../boot-process-and-filesystem-hierarchy.md) |
| CLI navigation | Paths, find evidence fast | [Essential commands](../essential-linux-commands.md) |
| Users / sudo | Least privilege, `visudo` | [Users & sudo](../users-groups-and-sudo.md) |
| Permissions / ACL | `chmod`, sticky, SGID | [Permissions](../permissions-acls-and-special-bits.md) |
| Processes | Signals, nice, zombies | [Processes](../process-management.md) |
| systemd | unit, journalctl, timers | [systemd](../systemd-services-and-journalctl.md) |
| Storage / LVM | loop labs, `df`/`du` | [Storage](../storage-disks-partitions-and-filesystems.md) |
| SSH / firewall | Keys, hardening safely | [SSH](../ssh-and-remote-access.md) |
| Triage | Break → fix → prove | [Troubleshooting](../troubleshooting-linux-systems.md) |

## Story bank (from course labs)

1. Host identity pack before installing packages  
2. Symlink deploy path vs hard link  
3. `useradd` + sudoers drop-in with allow/deny proof  
4. Sticky bit / ACL deny test  
5. systemd unit failure in journalctl  
6. Loop-backed filesystem create/mount  
7. SSH key login on localhost  
8. OOM / cgroup memory evidence on a container  

## Academy catalog

Browse shared guides in the [Academy interview catalog](../../interview/index.md).
