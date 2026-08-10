---
title: "Capstone Project 2 — Configure a Bastion Host"
description: "Build a production Bastion Host — SSH hardening, key authentication, UFW, Fail2Ban, auditd, monitoring, backups, and secure jump-server access."
difficulty: advanced
estimated_time: "5–7 hours"
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
  - bastion
  - ssh
  - security
  - production
  - rebash-linux-mastery
comments: false
status: ready
---

# Capstone Project 2 — Configure a Bastion Host

> A **Bastion Host** (also called a **Jump Server** or **Jump Box**) is a hardened Linux server that acts as the single secure entry point for administrators to access private infrastructure. Instead of exposing every production server to the Internet, only the Bastion Host is publicly accessible, while all other servers remain inside a private network. In this capstone project, you'll build a production-ready Bastion Host with SSH hardening, firewall protection, user management, auditing, monitoring, and logging.

---


# Project Overview

## Objective

Build a secure Bastion Host that provides controlled administrative access to private Linux servers.

---

## Skills Covered

- Linux Administration
- SSH Hardening
- Public Key Authentication
- User Management
- Firewall Configuration
- Network Security
- Audit Logging
- Fail2Ban
- Monitoring
- System Hardening
- Access Control
- Production Validation

---

# Estimated Time

**5–7 Hours**

---

# Difficulty

Beginner → Advanced

---

# Project Architecture

```text
                Internet
                    │
                    │
              SSH (22)
                    │
        +----------------------+
        |    Bastion Host      |
        |  Public IP Address   |
        +----------------------+
                    │
          Private Network
                    │
      ┌─────────────┼─────────────┐
      │             │             │
+-------------+ +-------------+ +-------------+
| App Server  | | DB Server   | | K8s Node    |
| Private IP  | | Private IP  | | Private IP  |
+-------------+ +-------------+ +-------------+
```

---

# Learning Outcomes

By completing this project, you'll be able to:

- Build a Bastion Host
- Secure SSH access
- Configure key-based authentication
- Restrict administrative access
- Protect servers with firewalls
- Enable audit logging
- Monitor administrative activity
- Validate production readiness

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

Choose one:

- Ubuntu Server 24.04 LTS
- Ubuntu Server 22.04 LTS
- Rocky Linux 9
- AlmaLinux 9

This project uses **Ubuntu Server**.

---

# Software Stack

- Ubuntu Server
- OpenSSH Server
- UFW
- Fail2Ban
- rsyslog
- auditd
- rsync

---

# Project Tasks

| Phase | Task |
|---------|------|
| 1 | Install Linux |
| 2 | Configure Networking |
| 3 | Create Administrator Accounts |
| 4 | Configure SSH Keys |
| 5 | Harden SSH |
| 6 | Configure Firewall |
| 7 | Install Fail2Ban |
| 8 | Configure Audit Logging |
| 9 | Configure Monitoring |
| 10 | Configure Backup |
| 11 | Validate Access |
| 12 | Production Hardening |

---

# Phase 1 — Install Linux

Update the server.

```bash
sudo apt update

sudo apt upgrade -y
```

Verify OS.

```bash
hostnamectl
```

---

# Phase 2 — Configure Networking

Configure hostname.

```bash
sudo hostnamectl set-hostname bastion01
```

Verify networking.

```bash
ip addr

ip route
```

Verify connectivity.

```bash
ping google.com
```

---

# Phase 3 — Create Administrator Accounts

Create administrator.

```bash
sudo adduser admin1
```

Grant sudo.

```bash
sudo usermod -aG sudo admin1
```

Verify.

```bash
id admin1
```

Create separate accounts for every administrator.

Never share administrator accounts.

---

# Phase 4 — Configure SSH Keys

Generate key pair on administrator workstation.

```bash
ssh-keygen
```

Copy public key.

```bash
ssh-copy-id admin1@bastion-ip
```

Test login.

```bash
ssh admin1@bastion-ip
```

---

# Phase 5 — Harden SSH

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

X11Forwarding no

AllowUsers admin1
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

# Phase 6 — Configure Firewall

Install UFW.

```bash
sudo apt install ufw
```

Allow SSH.

```bash
sudo ufw allow OpenSSH
```

Enable firewall.

```bash
sudo ufw enable
```

Verify.

```bash
sudo ufw status
```

---

# Phase 7 — Install Fail2Ban

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

# Phase 8 — Configure Audit Logging

Install auditd.

```bash
sudo apt install auditd
```

Enable service.

```bash
sudo systemctl enable auditd

sudo systemctl start auditd
```

Verify.

```bash
systemctl status auditd
```

Review audit logs.

```bash
ausearch
```

---

# Phase 9 — Configure Monitoring

CPU.

```bash
top
```

Memory.

```bash
free -h
```

Disk.

```bash
df -h
```

Services.

```bash
systemctl
```

Logs.

```bash
journalctl
```

---

# Phase 10 — Configure Backup

Backup SSH configuration.

```bash
sudo tar -czf ssh-backup.tar.gz /etc/ssh
```

Backup administrator home.

```bash
rsync -av /home /backup
```

Verify.

```bash
ls -lh
```

---

# Phase 11 — Validate Administrative Access

Verify SSH login.

```bash
ssh admin1@bastion-ip
```

Verify SSH keys.

```bash
ls ~/.ssh
```

Display active users.

```bash
who

w
```

Review login history.

```bash
last
```

---

# Phase 12 — Production Hardening

Review listening ports.

```bash
ss -tuln
```

Review running services.

```bash
systemctl --type=service
```

Remove unused packages.

```bash
sudo apt autoremove
```

Install updates.

```bash
sudo apt update

sudo apt upgrade
```

---

# Final Project Checklist

| Item | Status |
|--------|--------|
| Linux Installed | ☐ |
| Updates Applied | ☐ |
| Hostname Configured | ☐ |
| Administrator Accounts Created | ☐ |
| SSH Keys Configured | ☐ |
| Root Login Disabled | ☐ |
| Password Authentication Disabled | ☐ |
| Firewall Enabled | ☐ |
| Fail2Ban Configured | ☐ |
| Audit Logging Enabled | ☐ |
| Monitoring Verified | ☐ |
| Backup Created | ☐ |
| Production Validation Completed | ☐ |

---

# Security Validation

Verify:

SSH

```bash
systemctl status ssh
```

Firewall

```bash
ufw status
```

Fail2Ban

```bash
fail2ban-client status
```

Audit

```bash
systemctl status auditd
```

Listening ports

```bash
ss -tuln
```

---

# Production Perspective

Bastion Hosts are commonly used in:

- AWS
- Microsoft Azure
- Google Cloud
- Oracle Cloud
- Kubernetes clusters
- Enterprise data centers
- Financial institutions
- Government infrastructure

Modern cloud environments often place Bastion Hosts inside dedicated management subnets protected by strict firewall rules.

---

# Hands-on Lab

## Task 1

Create two administrator accounts.

---

## Task 2

Configure SSH key authentication.

---

## Task 3

Disable password authentication.

---

## Task 4

Enable UFW and allow only SSH.

---

## Task 5

Install and configure Fail2Ban.

---

## Task 6

Install auditd and verify audit logging.

---

## Task 7

Review authentication logs.

```bash
journalctl -u ssh
```

---

## Task 8

Connect through the Bastion Host and SSH into a private Linux server using key-based authentication.

---

# Production Best Practices

- Never allow direct SSH access to private production servers.
- Use unique administrator accounts.
- Require SSH key authentication.
- Disable root login.
- Restrict firewall access.
- Enable auditing.
- Monitor login activity.
- Rotate SSH keys periodically.
- Keep the Bastion Host fully patched.
- Review access logs regularly.

---

# Challenge Tasks

Complete these additional tasks to extend the project:

- Configure SSH Agent Forwarding securely.
- Restrict SSH access by source IP address.
- Configure Multi-Factor Authentication (MFA) for SSH.
- Forward audit logs to a centralized logging server.
- Install Prometheus Node Exporter for monitoring.
- Configure automatic security updates.
- Implement SSH login banners.
- Configure session timeout for inactive users.
- Restrict administrator access using Linux groups.
- Build a secondary Bastion Host for High Availability.

---

# Skills Demonstrated

After completing this project, you will have demonstrated proficiency in:

- Linux Security
- SSH Administration
- Bastion Host Design
- Access Control
- Firewall Management
- Audit Logging
- Production Hardening
- Monitoring
- Backup
- Enterprise Linux Administration

---

# Congratulations!

You have successfully built a **production-ready Bastion Host**.

Your Bastion Host now provides a secure, centralized, and auditable entry point for administering private Linux infrastructure while minimizing the attack surface of your production environment.

This architecture is widely used in enterprise data centers and cloud platforms to protect critical infrastructure from unauthorized access.

---

## What's Next?

**[Capstone Project 3 — Deploy a Git Server](deploy-git-server.md)**

You'll learn how to:

- Install and configure Git
- Create Git repositories
- Manage SSH-based Git access
- Configure repository permissions
- Secure Git server access
- Enable backups
- Monitor repository services

By the end of the project, you'll have a production-ready Git server that supports secure version control and collaboration for development teams.
