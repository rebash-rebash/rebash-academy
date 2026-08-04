---
title: Overview
description: "Linux for Cloud & DevOps Engineers — learning roadmap and tutorials from fundamentals through production operations."
difficulty: beginner
estimated_time: "8–10 weeks"
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
tags:
  - linux
  - devops
  - cloud
  - course
comments: false
---

# Linux for Cloud & DevOps Engineers

**Duration:** 8–10 weeks (≈ 45–60 hours contact time at a professional pace)
{ .ra-facts }

Learn Linux the way operators use it: start from a clear problem, build a simple mental model, then practise with a real Hands-on Lab. Suitable if you are new to Linux or revising for Cloud and DevOps interviews.

!!! tip "How to use this course"
    Start with [Fundamentals](linux-fundamentals-distributions-and-architecture.md), work modules in order, and prefer Ubuntu 22.04/24.04 for labs. Practise Interview Questions aloud with command evidence.

---

## Learning roadmap

1. **Foundations** — what Linux is, boot, Filesystem Hierarchy Standard (FHS)
2. **Command line** — navigation, environment, first scripts
3. **Files & identity** — paths, permissions, users, sudo
4. **Ops daily work** — text tools, processes, systemd, packages
5. **Systems** — storage, networking, SSH, scheduling, logs
6. **Secure & scale** — hardening, containers, troubleshooting, production

!!! tip "Checkpoint after Module 4"
    If you can create a user, grant least-privilege sudo, and prove chmod/ACL behaviour, you are ready for junior Linux interview questions — keep going for Cloud and DevOps depth.

### Prerequisites

None beyond basic computer knowledge. A disposable Ubuntu 22.04/24.04 (or Rocky/RHEL) lab VM is enough.

### Tools

| Tool | Notes |
|------|--------|
| Ubuntu LTS or RHEL-family | Preferred lab images |
| Terminal + SSH | Local VM, WSL2, or cloud Free Tier |
| `sudo` user | Not daily root |
| Snapshots | Before storage/security labs |

---

## Modules and tutorials

### Module 1 — Linux Fundamentals

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 1 | [Distributions and Architecture](linux-fundamentals-distributions-and-architecture.md) | Beginner | 45 min |
| 2 | [Boot Process and Filesystem Hierarchy](boot-process-and-filesystem-hierarchy.md) | Beginner | 45 min |

**Topics:** What is Linux · Distros · Architecture · Kernel · User Space · Shell vs Terminal · Boot Process · FHS

### Module 2 — Command Line Essentials

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 3 | [Essential Linux Commands](essential-linux-commands.md) | Beginner | 50 min |

**Topics:** pwd ls cd mkdir rm cp mv touch cat less head tail stat file history

### Module 3 — Linux Filesystem

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 4 | [Paths, Links, Mounts, and Inodes](filesystem-paths-links-mounts-and-inodes.md) | Beginner | 50 min |
| 5 | [Disk Usage and File Attributes](disk-usage-and-file-attributes.md) | Beginner | 40 min |

**Topics:** Directory structure · Absolute/relative paths · Hard/symbolic links · Mount points · File attributes · Disk usage · inode

### Module 4 — Users & Permissions

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 6 | [Users, Groups, and sudo](users-groups-and-sudo.md) | Beginner | 45 min |
| 7 | [Permissions, ACLs, and Special Bits](permissions-acls-and-special-bits.md) | Intermediate | 50 min |

**Topics:** Users · Groups · sudo · chmod · chown · chgrp · umask · ACLs · Sticky · SUID · SGID

### Module 5 — Text Processing

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 8 | [Text Processing with grep, sed, and awk](text-processing-grep-sed-awk.md) | Intermediate | 55 min |

**Topics:** grep sed awk cut paste tr sort uniq wc xargs

### Module 6 — Process Management

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 9 | [Process Management](process-management.md) | Intermediate | 50 min |

**Topics:** ps top htop kill pkill jobs fg bg nice renice nohup

### Module 7 — Services & Boot

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 10 | [systemd Services and journalctl](systemd-services-and-journalctl.md) | Intermediate | 55 min |
| 11 | [systemd Targets, Timers, and Boot](systemd-targets-timers-and-boot.md) | Intermediate | 50 min |

**Topics:** systemd · systemctl · journalctl · Targets · Services · Timers · Boot

### Module 8 — Storage Management

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 12 | [Disks, Partitions, and Filesystems](storage-disks-partitions-and-filesystems.md) | Intermediate | 55 min |
| 13 | [LVM, Swap, and Disk Monitoring](lvm-swap-and-disk-monitoring.md) | Advanced | 55 min |

**Topics:** lsblk fdisk parted mkfs mount umount · LVM · Swap · Disk monitoring

### Module 9 — Linux Networking

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 14 | [Linux Networking Tools](linux-networking-tools.md) | Intermediate | 55 min |
| 15 | [SSH and Remote Access](ssh-and-remote-access.md) | Intermediate | 45 min |

**Topics:** ip ss ping traceroute dig nslookup host curl wget tcpdump netcat · SSH

### Module 10 — Package Management

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 16 | [Package Management](package-management.md) | Beginner | 45 min |

**Topics:** apt dnf yum zypper snap flatpak

### Module 11 — Scheduling & Automation

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 17 | [Scheduling — cron, at, and Timers](scheduling-cron-at-and-timers.md) | Intermediate | 45 min |

**Topics:** cron crontab at systemd timers

### Module 12 — Logging & Monitoring

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 18 | [Logging — syslog, journald, logrotate](logging-syslog-journald-logrotate.md) | Intermediate | 45 min |
| 19 | [Host Monitoring — vmstat, iostat, sar](host-monitoring-vmstat-iostat-sar.md) | Intermediate | 45 min |

**Topics:** syslog journald logrotate · vmstat iostat free uptime df du sar

### Module 13 — Linux Security

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 20 | [SSH Hardening and Firewalls](ssh-hardening-and-firewalls.md) | Advanced | 55 min |
| 21 | [SELinux, AppArmor, Fail2Ban, Auditd, PAM](selinux-apparmor-fail2ban-auditd-pam.md) | Advanced | 55 min |

**Topics:** SSH hardening · SSH keys · firewalld · ufw · SELinux · AppArmor · Fail2Ban · Auditd · PAM

### Module 14 — Containers & Cloud

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 22 | [Containers — Namespaces, cgroups, and OCI](containers-namespaces-cgroups-and-oci.md) | Advanced | 55 min |

**Topics:** Namespaces · cgroups · OverlayFS · OCI · Container runtime basics

### Module 15 — Troubleshooting

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 23 | [Troubleshooting Linux Systems](troubleshooting-linux-systems.md) | Advanced | 60 min |

**Topics:** Boot · High CPU/memory · Disk full · Permissions · Network · Services · Logs · Performance

### Module 16 — Production Linux

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 24 | [Production Hardening and Performance](production-linux-hardening-and-performance.md) | Advanced | 55 min |
| 25 | [Backup, Disaster Recovery, and Capacity](backup-disaster-recovery-and-capacity.md) | Advanced | 55 min |

**Topics:** Hardening · Performance tuning · Capacity · Monitoring · Logging · Operational excellence · Backup · DR

---

## Start here

1. [Linux Fundamentals — Distributions and Architecture](linux-fundamentals-distributions-and-architecture.md)
2. Use a disposable lab VM with snapshots
3. After Module 11–12, deepen automation in [Shell Scripting](../shell/index.md)

## Related

- Next: [Shell Scripting](../shell/index.md)
- [DevOps Engineer path](../career-paths/devops-engineer/index.md)
- [Getting Started](../getting-started/index.md)
