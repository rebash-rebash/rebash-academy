# Technology Definition

> **Content quality:** When generating tutorials for this course, follow `.cursor/prompts/CONTENT_QUALITY.md`, `tutorial-format-linux.md`, and `create_lab.md`. Labs must be topic-specific and copy-paste executable — never a generic host baseline with only the title changed. Prefer Codex until the user changes agents.

## Course

REBASH Linux Mastery — practical Linux for Cloud, DevOps, Kubernetes, and Platform Engineers

---

## Description

A production-focused Linux course (~145 lessons, 40+ labs, 8 capstones) that prepares learners to administer, troubleshoot, automate, and operate Linux systems used in Cloud, DevOps, Kubernetes, Platform Engineering, and Site Reliability Engineering.

This is not a basic-commands course. It trains production engineers. Scaffolded lesson stubs live under `docs/linux/`; fill each tutorial when the author supplies content (follow `tutorial-format-linux.md`).

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

# Modules (REBASH Linux Mastery — 15 modules)

Canonical nav: `docs/linux/.pages`. Scaffold script: `scripts/scaffold_linux_mastery.py`.

## Module 1 — Linux Fundamentals

1. Introduction to Linux
2. Linux History and Open Source
3. Linux Fundamentals — Distributions and Architecture
4. Linux Kernel Explained
5. Linux Desktop vs Server Editions
6. Linux Installation (VirtualBox, VMware, WSL)
7. Linux Boot Process
8. First Login and Terminal
9. Linux Directory Structure (FHS)
10. Getting Help (`man`, `info`, `--help`)

**Lab:** Install Ubuntu Server and explore the filesystem.

## Module 2 — Linux Command Line Essentials

1. Understanding the Shell · 2. Bash Basics · 3. Navigating the Filesystem
4. File and Directory Commands · 5. Viewing File Contents · 6. Searching Files
7. Wildcards and Globbing · 8. Command History · 9. Redirection · 10. Pipes

**Lab:** Build a mini file management toolkit.

## Module 3 — Text Processing

cat · less · head · tail · grep · cut · sort · uniq · tr · sed · awk · xargs

**Mini project:** Analyze web server logs.

## Module 4 — File System

File Types · Hard Links · Soft Links · Permissions · Ownership · umask · ACL · File Attributes · Mount Points · Disk Usage

**Lab:** Create and secure a shared directory.

## Module 5 — Users and Groups

Users · Groups · sudo · Password Policies · Environment Variables · Profiles · Shell Configuration · SSH Keys · PAM Overview · Multi-user Environment

**Project:** Configure a secure multi-user Linux server.

## Module 6 — Process Management

Processes · Foreground/Background Jobs · ps · top · htop · nice · kill · Signals · systemd · Services

**Lab:** Troubleshoot a failing service.

## Module 7 — Package Management

APT · DNF · YUM · RPM · Snap · Flatpak · Repository Management · Updates · Security Patches · Package Troubleshooting

## Module 8 — Networking

TCP/IP · IP Configuration · DNS · Routing · ping · traceroute · ss · netstat · curl · wget · SSH · SCP · rsync

**Project:** Configure SSH access between servers.

## Module 9 — Storage Management

Partitions · Filesystems · mkfs · Mounting · LVM · RAID Concepts · Swap · Quotas · Backup Basics · Restore

## Module 10 — Bash Scripting

Variables · Conditions · Loops · Functions · Arrays · Input · Exit Codes · Error Handling · Logging · Script Best Practices

**Project:** System Health Monitoring Script.

## Module 11 — Linux Security

SSH Hardening · File Permissions Review · Firewall (UFW) · SELinux Overview · AppArmor · Fail2Ban · Audit Logs · Security Updates · Secrets Management · CIS Benchmark Basics

## Module 12 — Monitoring & Logs

journalctl · syslog · dmesg · logrotate · Disk / Memory / CPU Monitoring · Performance Troubleshooting · Crash Investigation · Monitoring Best Practices

## Module 13 — Linux for DevOps

Linux for Docker · Kubernetes · CI/CD · Git · Terraform · Ansible · Jenkins · GitHub Actions · GitLab CI · Cloud Platforms

## Module 14 — Production Linux Administration

Production Checklist · Hardening Checklist · Performance Tuning · Capacity Planning · Backup Strategy · Disaster Recovery · High Availability · Incident Response · Troubleshooting Methodology · Best Practices

## Module 15 — Capstone Projects

1. Build a Secure Linux Web Server
2. Configure a Bastion Host
3. Deploy a Git Server
4. Create a Monitoring Server
5. Automate User Provisioning with Bash
6. Build a Linux Server Baseline
7. Harden an Ubuntu Server
8. Production Linux Troubleshooting Challenge

---

# Hands-on Labs

40+ labs mapped to modules (install Ubuntu, shared directory, failing service, SSH between servers, health script, hardening, log analysis, DR drills, and more). Prefer topic-specific labs via `create_lab.md`.

---

# Projects / Capstones

See Module 15 under `docs/linux/projects/`. Each page needs SEO `description` + tags; site-wide AdSense / Analytics come from `mkdocs.yml` + `overrides/main.html`.

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