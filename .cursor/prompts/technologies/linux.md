# Technology Definition

## Course

Linux for Cloud & DevOps Engineers

---

## Description

A production-focused Linux course that prepares learners to confidently administer, troubleshoot, automate and operate Linux systems used in Cloud, DevOps, Platform Engineering and Site Reliability Engineering.

This course focuses on practical engineering rather than certification-only knowledge.

---

## Target Roles

- Linux Administrator
- DevOps Engineer
- Cloud Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)
- DevSecOps Engineer
- Infrastructure Engineer

---

## Difficulty

Beginner → Advanced

---

## Estimated Duration

8–10 Weeks

---

## Prerequisites

None

Basic computer knowledge is sufficient.

---

## MCP Servers

Primary

- Context7
- Filesystem

Optional

- Git
- GitHub
- Kubernetes (for container-related examples)

---

# Modules

## Module 1 — Linux Fundamentals

- What is Linux?
- Linux Distributions
- Linux Architecture
- Kernel
- User Space
- Shell vs Terminal
- Boot Process
- Filesystem Hierarchy Standard (FHS)

---

## Module 2 — Command Line Essentials

- pwd
- ls
- cd
- mkdir
- rm
- cp
- mv
- touch
- cat
- less
- head
- tail
- stat
- file
- history

---

## Module 3 — Linux Filesystem

- Directory Structure
- Absolute vs Relative Paths
- Hard Links
- Symbolic Links
- Mount Points
- File Attributes
- Disk Usage
- inode

---

## Module 4 — Users & Permissions

- Users
- Groups
- sudo
- chmod
- chown
- chgrp
- umask
- ACLs
- Sticky Bit
- SUID
- SGID

---

## Module 5 — Text Processing

- grep
- sed
- awk
- cut
- paste
- tr
- sort
- uniq
- wc
- xargs

---

## Module 6 — Process Management

- ps
- top
- htop
- kill
- pkill
- jobs
- fg
- bg
- nice
- renice
- nohup

---

## Module 7 — Services & Boot

- systemd
- systemctl
- journalctl
- Targets
- Services
- Timers
- Boot Process

---

## Module 8 — Storage Management

- lsblk
- fdisk
- parted
- mkfs
- mount
- umount
- LVM
- Swap
- Disk Monitoring

---

## Module 9 — Linux Networking

- ip
- ss
- ping
- traceroute
- dig
- nslookup
- host
- curl
- wget
- tcpdump
- netcat
- SSH

---

## Module 10 — Package Management

- apt
- dnf
- yum
- zypper
- snap
- flatpak

---

## Module 11 — Scheduling & Automation

- cron
- crontab
- at
- systemd timers

---

## Module 12 — Logging & Monitoring

- syslog
- journald
- logrotate
- vmstat
- iostat
- free
- uptime
- df
- du
- sar

---

## Module 13 — Linux Security

- SSH Hardening
- SSH Keys
- firewalld
- ufw
- SELinux
- AppArmor
- Fail2Ban
- Auditd
- PAM

---

## Module 14 — Containers & Cloud

- Linux Namespaces
- cgroups
- OverlayFS
- OCI Concepts
- Container Runtime Basics

---

## Module 15 — Troubleshooting

- Boot Failures
- High CPU
- High Memory
- Disk Full
- Permission Issues
- Network Problems
- Service Failures
- Log Analysis
- Performance Bottlenecks

---

## Module 16 — Production Linux

- Linux Hardening
- Performance Tuning
- Capacity Planning
- Backup Strategies
- Disaster Recovery
- Monitoring
- Logging
- Operational Excellence

---

# Hands-on Labs

- Install Linux
- Configure SSH
- Create Users & Groups
- Manage Permissions
- Configure Storage
- Manage Services
- Analyse Logs
- Configure Firewall
- Build Monitoring Scripts
- Secure a Linux Server
- Troubleshoot Performance
- Recover a Failed Service
- Configure Cron Jobs
- Monitor System Resources
- Build a Linux Troubleshooting Toolkit

---

# Projects

## Beginner

Linux System Information Utility

---

## Intermediate

Linux Server Health Dashboard

---

## Advanced

Linux Operations Toolkit

---

## Capstone

Production Linux Operations Platform

Features:

- User Management
- Monitoring
- Logging
- Security Hardening
- Backup Automation
- System Health Dashboard
- Performance Monitoring
- Alerting
- Reporting
- Scheduling

---

# Cheat Sheets

Generate:

- Linux Commands
- File Permissions
- Text Processing
- Process Management
- Storage
- Networking
- SSH
- Systemd
- Package Managers
- Troubleshooting

---

# Interview Preparation

Cover:

- Linux Fundamentals
- Administration
- Troubleshooting
- Performance
- Networking
- Security
- Production Scenarios

---

# Excalidraw Diagrams

**Use Excalidraw only** for course diagrams — do not use D2 or Mermaid for Linux tutorials.

Assets live under `docs/assets/excalidraw/` as `.svg` plus editable `.excalidraw` sources. Regenerate with:

```bash
python3 scripts/generate-excalidraw-svg.py
```

Generate diagrams for:

- Linux Architecture
- Boot Process
- Filesystem Hierarchy
- Process Lifecycle
- Storage Layout
- Networking Stack
- systemd Architecture
- Permission Model
- Container Internals
- CLI Workflow
- Text Processing
- SSH Access
- Package Management
- Scheduling
- Logging
- Host Monitoring
- Security Layers
- Troubleshooting
- Backup & DR
- Production Baseline

---

# Certifications

Map modules where appropriate to:

- RHCSA
- RHCE
- LFCS
- LFCE

---

# Capstone Outcome

After completing this course learners should be able to:

- Administer Linux servers confidently
- Troubleshoot production Linux systems
- Secure Linux environments
- Optimise performance
- Support Kubernetes nodes
- Operate cloud virtual machines
- Automate administration tasks
- Prepare Linux systems for DevOps and Platform Engineering