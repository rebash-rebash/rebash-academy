---
title: Overview
description: "Linux for Cloud & DevOps Engineers — 16 modules and 25 tutorials covering fundamentals through production operations, containers, security, and troubleshooting."
difficulty: beginner
estimated_time: "8–10 weeks"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - devops
  - cloud
  - course
comments: false
---

# Linux for Cloud & DevOps Engineers

A production-focused Linux course for administering, troubleshooting, automating, and operating Linux systems used in Cloud, DevOps, Platform Engineering, and SRE — practical engineering, not certification-only knowledge.

!!! tip "Course status"
    **Track ready** — **16 modules · 25 tutorials**, labs, quiz, cheat sheet, interview prep, and projects. Start with [Linux Fundamentals — Distributions and Architecture](linux-fundamentals-distributions-and-architecture.md).

!!! tip "Learning path"
    Linux is step 1 on the [DevOps Engineer path](../learning-paths/devops-engineer.md). Next: [Shell Scripting](../shell/index.md) → [Python for DevOps](../python/index.md) → Networking. Dedicated path: [Linux for Cloud & DevOps](../learning-paths/linux-for-cloud-devops.md).

---

## 1. Course overview

### Purpose

Prepare learners to confidently operate Linux on cloud VMs, bastions, CI runners, and container hosts.

### Target roles

Linux Administrator · DevOps · Cloud · Platform · SRE · DevSecOps · Infrastructure Engineer

### Prerequisites

None beyond basic computer knowledge. A disposable Ubuntu 22.04/24.04 (or Rocky/RHEL) lab VM is enough.

### Tools

| Tool | Notes |
|------|--------|
| Ubuntu LTS or RHEL-family | Preferred lab images |
| Terminal + SSH | Local VM, WSL2, or cloud Free Tier |
| `sudo` user | Not daily root |
| Snapshots | Before storage/security labs |

### Duration

**8–10 weeks** (≈ 45–60 hours contact time at a professional pace).

### Capstone outcomes

Administer servers · troubleshoot production · secure environments · optimise performance · support Kubernetes nodes · operate cloud VMs · automate admin tasks · prepare hosts for DevOps/Platform work.

### Certification mapping (light)

| Theme | RHCSA/LFCS | RHCE/LFCE | Modules |
|-------|:----------:|:---------:|---------|
| Users / permissions / ACL | ● | ○ | 4 |
| Storage / LVM | ● | ● | 8 |
| systemd / services | ● | ● | 7 |
| Networking / SSH | ● | ● | 9, 13 |
| Security / firewalls / MAC | ● | ● | 13, 16 |
| Containers host concepts | ○ | ● | 14 |
| Troubleshooting / performance | ● | ● | 12, 15, 16 |

---

## 2. Learning path

```text
M1 Fundamentals → M2 CLI → M3 Filesystem → M4 Users/Permissions
        ↓
M5 Text → M6 Processes → M7 Services/Boot → M8 Storage
        ↓
M9 Networking → M10 Packages → M11 Scheduling → M12 Logging/Monitoring
        ↓
M13 Security → M14 Containers/Cloud → M15 Troubleshooting → M16 Production
        ↓
Projects → Capstone → Shell Scripting track
```

---

## 3. Modules and tutorials

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

## 4. Practice

### Labs

| Lab | Focus |
|-----|--------|
| [Install and first boot](../labs/linux-install-and-first-boot.md) | Lab VM ready |
| [SSH secure access](../labs/linux-ssh-secure-access.md) | Keys and SSH |
| [Users and permissions](../labs/linux-users-permissions-lab.md) | Identity lock-down |
| [Storage lab](../labs/linux-storage-lab.md) | Disks / mounts |
| [Services and logs](../labs/linux-services-and-logs-lab.md) | systemd + journal |
| [Firewall hardening](../labs/linux-firewall-hardening-lab.md) | Secure the host |
| [Performance troubleshooting](../labs/linux-performance-troubleshooting-lab.md) | CPU/memory/service |
| [Ops toolkit](../labs/linux-ops-toolkit-lab.md) | Monitoring + cron toolkit |
| [Production incident triage](../labs/linux-production-incident-triage.md) | Scenario drill |
| [App server from zero](../labs/linux-app-server-from-zero.md) | End-to-end host build |

### Projects

| Level | Project |
|-------|---------|
| Beginner | [System Information Utility](../projects/linux-system-information-utility.md) |
| Intermediate | [Server Health Dashboard](../projects/linux-server-health-dashboard.md) |
| Advanced | [Operations Toolkit](../projects/linux-operations-toolkit.md) |
| Capstone | [Production Linux Operations Platform](../projects/linux-production-operations-platform.md) |

### Assessment & reference

- Quiz: [Linux for Cloud & DevOps Fundamentals](../quizzes/linux-for-cloud-devops-fundamentals.md) (40 Q)
- Also: [Linux Fundamentals](../quizzes/linux-fundamentals.md) · [Linux Servers](../quizzes/linux-servers.md)
- [Cheat sheet](../cheatsheets/linux.md) · [Interview prep](../interview/linux.md)

---

## 5. D2 diagrams

Architecture · Boot process · Filesystem / links · Permission model · Process lifecycle · Storage layout · Networking stack · systemd · Container internals — under `docs/assets/d2/linux-*.d2`.

---

## Start here

1. [Linux Fundamentals — Distributions and Architecture](linux-fundamentals-distributions-and-architecture.md)
2. Lab VM with snapshots
3. After Module 11–12, deepen automation in [Shell Scripting](../shell/index.md)

## Related

- Path: [Linux for Cloud & DevOps](../learning-paths/linux-for-cloud-devops.md)
- Next: [Shell Scripting](../shell/index.md)
- [DevOps Engineer path](../learning-paths/devops-engineer.md)
- [Getting Started](../getting-started/index.md)
