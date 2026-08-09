---
title: "Capstone Project 7 — Harden an Ubuntu Server"
description: "Harden Ubuntu Server for production — SSH, UFW, Fail2Ban, auditd, AppArmor, file permissions, unattended upgrades, and security validation."
difficulty: advanced
estimated_time: "6–8 hours"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 15 · Capstone Projects"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - security-engineer
tags:
  - linux
  - capstone
  - ubuntu
  - hardening
  - security
  - production
  - rebash-linux-mastery
comments: false
status: ready
---

# Capstone Project 7 — Harden an Ubuntu Server

> A default Ubuntu installation is designed to be functional, but it is **not fully optimized for production security**. Before deploying a server into production, organizations apply security hardening to reduce the attack surface, enforce strong authentication, secure network access, enable auditing, and implement continuous monitoring. In this capstone project, you'll transform a default Ubuntu Server into a **production-ready hardened server** by applying industry best practices inspired by CIS Benchmarks and enterprise security standards.

---

# Project Overview

## Objective

Harden an Ubuntu Server using production security best practices and validate its readiness for deployment.

---

## Skills Covered

- Ubuntu Administration
- Linux Security
- SSH Hardening
- User Management
- File Permissions
- Firewall Configuration
- Fail2Ban
- auditd
- Logging
- System Updates
- Security Validation
- Production Hardening

---

# Estimated Time

**6–8 Hours**

---

# Difficulty

Beginner → Advanced

---

# Project Architecture

```text
          Fresh Ubuntu Server
                  │
                  ▼
         Apply Security Hardening
                  │
      ┌───────────┼───────────┐
      │           │           │
 SSH      Firewall      User Security
      │           │           │
      └───────────┼───────────┘
                  │
        Logging & Monitoring
                  │
                  ▼
      Production Ready Ubuntu Server
```

---

# Learning Outcomes

By completing this project, you'll be able to:

- Secure an Ubuntu server
- Harden SSH access
- Configure firewall protection
- Enable auditing and monitoring
- Apply least privilege
- Reduce the attack surface
- Validate server security
- Build a production-ready Linux system

---

# Project Requirements

## Hardware

Minimum

- 2 vCPU
- 2 GB RAM
- 20 GB Disk

Recommended

- 2–4 vCPU
- 4 GB RAM
- 40 GB SSD

---

## Operating System

- Ubuntu Server 24.04 LTS
- Ubuntu Server 22.04 LTS

---

# Software Stack

- Ubuntu Server
- OpenSSH Server
- UFW
- Fail2Ban
- auditd
- rsyslog
- logrotate
- AppArmor
- Bash

---

# Project Tasks

| Phase | Task |
|---------|------|
| 1 | Update Ubuntu |
| 2 | Secure User Accounts |
| 3 | Harden SSH |
| 4 | Configure Firewall |
| 5 | Configure File Permissions |
| 6 | Install Fail2Ban |
| 7 | Enable Audit Logging |
| 8 | Verify AppArmor |
| 9 | Remove Unnecessary Services |
| 10 | Configure Automatic Updates |
| 11 | Validate Security |
| 12 | Production Review |

---

# Phase 1 — Update Ubuntu

Update package lists.

```bash
sudo apt update
```

Upgrade installed packages.

```bash
sudo apt full-upgrade -y
```

Remove unused packages.

```bash
sudo apt autoremove -y
```

Verify OS version.

```bash
hostnamectl
```

---

# Phase 2 — Secure User Accounts

Create an administrator account.

```bash
sudo adduser adminuser
```

Grant sudo access.

```bash
sudo usermod -aG sudo adminuser
```

Lock unused accounts if applicable.

```bash
sudo passwd -l username
```

Review users.

```bash
getent passwd
```

---

# Phase 3 — Harden SSH

Edit SSH configuration.

```bash
sudo nano /etc/ssh/sshd_config
```

Recommended configuration:

```text
PermitRootLogin no

PasswordAuthentication no

PubkeyAuthentication yes

PermitEmptyPasswords no

MaxAuthTries 3

ClientAliveInterval 300

ClientAliveCountMax 2

X11Forwarding no

AllowTcpForwarding no
```

Restart SSH.

```bash
sudo systemctl restart ssh
```

Verify.

```bash
systemctl status ssh
```

---

# Phase 4 — Configure Firewall

Install UFW.

```bash
sudo apt install ufw
```

Allow SSH.

```bash
sudo ufw allow OpenSSH
```

Allow HTTP.

```bash
sudo ufw allow 80/tcp
```

Allow HTTPS.

```bash
sudo ufw allow 443/tcp
```

Enable firewall.

```bash
sudo ufw enable
```

Verify.

```bash
sudo ufw status verbose
```

---

# Phase 5 — Configure File Permissions

Review sensitive files.

```bash
ls -l /etc/passwd

ls -l /etc/shadow
```

Review world-writable files.

```bash
find / -type f -perm -002
```

Review SUID files.

```bash
find / -perm -4000
```

Correct permissions where required.

```bash
chmod

chown
```

---

# Phase 6 — Install Fail2Ban

Install.

```bash
sudo apt install fail2ban
```

Enable.

```bash
sudo systemctl enable fail2ban

sudo systemctl start fail2ban
```

Verify.

```bash
fail2ban-client status
```

---

# Phase 7 — Enable Audit Logging

Install auditd.

```bash
sudo apt install auditd
```

Enable.

```bash
sudo systemctl enable auditd

sudo systemctl start auditd
```

Verify.

```bash
systemctl status auditd
```

Review logs.

```bash
ausearch
```

---

# Phase 8 — Verify AppArmor

Check status.

```bash
sudo aa-status
```

Verify AppArmor service.

```bash
systemctl status apparmor
```

Ensure AppArmor is enabled and enforcing profiles where applicable.

---

# Phase 9 — Remove Unnecessary Services

Review running services.

```bash
systemctl list-units --type=service
```

Disable unused services.

```bash
sudo systemctl disable service-name
```

Stop unused services.

```bash
sudo systemctl stop service-name
```

Review listening ports.

```bash
ss -tuln
```

---

# Phase 10 — Configure Automatic Updates

Install unattended upgrades.

```bash
sudo apt install unattended-upgrades
```

Enable.

```bash
sudo dpkg-reconfigure unattended-upgrades
```

Verify configuration.

```bash
cat /etc/apt/apt.conf.d/50unattended-upgrades
```

---

# Phase 11 — Validate Security

Verify:

SSH.

```bash
systemctl status ssh
```

Firewall.

```bash
ufw status
```

Fail2Ban.

```bash
systemctl status fail2ban
```

Audit.

```bash
systemctl status auditd
```

AppArmor.

```bash
aa-status
```

Listening ports.

```bash
ss -tuln
```

Recent security logs.

```bash
journalctl -p warning
```

---

# Phase 12 — Production Review

Perform a complete security review covering:

- Users
- SSH configuration
- Firewall
- Running services
- Open ports
- Installed packages
- Logging
- Monitoring
- Audit configuration
- Backup readiness

Document all findings.

---

# Security Checklist

```text
Ubuntu Installed

↓

System Updated

↓

SSH Hardened

↓

Firewall Enabled

↓

Fail2Ban Enabled

↓

auditd Enabled

↓

AppArmor Enabled

↓

Unused Services Removed

↓

Automatic Updates Enabled

↓

Security Validation Complete
```

---

# Final Project Checklist

| Item | Status |
|--------|--------|
| Ubuntu Updated | ☐ |
| Administrator Created | ☐ |
| SSH Hardened | ☐ |
| Firewall Enabled | ☐ |
| File Permissions Reviewed | ☐ |
| Fail2Ban Installed | ☐ |
| auditd Enabled | ☐ |
| AppArmor Verified | ☐ |
| Unused Services Removed | ☐ |
| Automatic Updates Enabled | ☐ |
| Security Validation Completed | ☐ |
| Documentation Completed | ☐ |

---

# Production Perspective

Ubuntu hardening is essential for:

- Cloud Virtual Machines
- Kubernetes Nodes
- Web Servers
- Database Servers
- Bastion Hosts
- CI/CD Servers
- Enterprise Linux Deployments
- Financial and Government Systems

Many organizations align their hardening process with CIS Benchmarks, internal security policies, and compliance requirements.

---

# Hands-on Lab

## Task 1

Update Ubuntu and install security patches.

---

## Task 2

Create a secure administrator account.

---

## Task 3

Disable root SSH login and password authentication.

---

## Task 4

Enable UFW and allow only required ports.

---

## Task 5

Install and configure Fail2Ban.

---

## Task 6

Enable auditd and verify audit logging.

---

## Task 7

Review all listening ports and disable unnecessary services.

---

## Task 8

Perform a complete security audit and produce a hardening report including:

- SSH settings
- Firewall rules
- Running services
- Open ports
- Installed security tools
- User accounts
- Security recommendations

---

# Production Best Practices

- Keep Ubuntu fully updated.
- Use SSH key authentication only.
- Disable direct root login.
- Enable UFW with a default deny policy.
- Enable AppArmor and auditd.
- Install only required software.
- Remove unnecessary services.
- Monitor authentication logs regularly.
- Automate security updates.
- Periodically review system security against organizational standards.

---

# Challenge Tasks

Complete these additional tasks to extend the project:

- Apply CIS Ubuntu Benchmark recommendations.
- Configure Multi-Factor Authentication (MFA) for SSH.
- Restrict SSH access by source IP address.
- Configure centralized log forwarding.
- Install Prometheus Node Exporter for security monitoring.
- Configure AIDE for file integrity monitoring.
- Create a Bash hardening automation script.
- Generate an HTML security compliance report.
- Integrate hardening into an Ansible playbook.
- Build a reusable hardened Ubuntu VM template.

---

# Skills Demonstrated

After completing this project, you will have demonstrated proficiency in:

- Ubuntu Administration
- Linux Security
- SSH Hardening
- Firewall Administration
- Security Auditing
- AppArmor
- Fail2Ban
- System Hardening
- Production Validation
- Enterprise Linux Operations

---

# Congratulations!

You have successfully hardened an **Ubuntu Server** for production use.

Your server now follows industry security best practices by enforcing secure authentication, restricting network access, enabling auditing, reducing the attack surface, and improving operational security.

These hardening techniques are commonly applied by enterprise IT teams, cloud providers, and security engineers before deploying Ubuntu systems into production environments.

---

## What's Next?

**[Capstone Project 8 — Production Linux Troubleshooting Challenge](production-linux-troubleshooting-challenge.md)**

You'll learn how to:


- Investigate complex production issues
- Analyze logs and system metrics
- Identify root causes
- Resolve multiple failures
- Validate system recovery
- Document troubleshooting findings
- Apply everything you've learned throughout the Linux Mastery course

By the end of the challenge, you'll demonstrate the practical skills required to troubleshoot and recover production Linux systems like an experienced Linux Administrator or Site Reliability Engineer.
