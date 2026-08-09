---
title: "Capstone Project 3 — Deploy a Git Server"
description: "Build a production self-hosted Git server — SSH auth, bare repositories, permissions, UFW, Fail2Ban, backups, monitoring, and hardening."
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
  - git
  - ssh
  - security
  - production
  - rebash-linux-mastery
comments: false
status: ready
---

# Capstone Project 3 — Deploy a Git Server

> Git is the industry-standard version control system used to manage source code, Infrastructure as Code (IaC), documentation, automation scripts, and configuration files. While cloud-hosted Git platforms such as GitHub and GitLab are widely used, many organizations deploy **self-hosted Git servers** for greater control, security, compliance, and integration with internal infrastructure. In this capstone project, you'll build a secure production-ready Git server using SSH authentication, repository permissions, backups, monitoring, and system hardening.

---

# Project Overview

## Objective

Build and secure a production-ready self-hosted Git server for team collaboration.

---

## Skills Covered

- Linux Administration
- Git Installation
- Git Repository Management
- SSH Authentication
- User Management
- File Permissions
- Backup Strategy
- Monitoring
- Logging
- Firewall Configuration
- Production Hardening

---

# Estimated Time

**5–7 Hours**

---

# Difficulty

Beginner → Advanced

---

# Project Architecture

```text
             Developers
                  │
           Git Push / Pull
                  │
              SSH (22)
                  │
        +----------------------+
        |     Git Server       |
        | Ubuntu Linux         |
        +----------------------+
                  │
          Git Repositories
                  │
      +------------------------+
      | /home/git/repos/*.git  |
      +------------------------+
```

---

# Learning Outcomes

By completing this project, you'll be able to:

- Deploy a Git server
- Configure secure SSH access
- Create Git repositories
- Manage repository permissions
- Secure Git administration
- Configure backups
- Monitor Git services
- Validate production readiness

---

# Project Requirements

## Hardware

Minimum

- 2 vCPU
- 2 GB RAM
- 20 GB Disk

Recommended

- 4 vCPU
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
- Git
- OpenSSH Server
- UFW
- Fail2Ban
- rsync
- auditd

---

# Project Tasks

| Phase | Task |
|---------|------|
| 1 | Install Linux |
| 2 | Install Git |
| 3 | Create Git User |
| 4 | Configure SSH |
| 5 | Create Repositories |
| 6 | Clone & Test Repository |
| 7 | Configure Firewall |
| 8 | Configure Backups |
| 9 | Configure Monitoring |
| 10 | Harden Server |
| 11 | Validate Git Operations |
| 12 | Production Review |

---

# Phase 1 — Install Linux

Update packages.

```bash
sudo apt update

sudo apt upgrade -y
```

Verify.

```bash
hostnamectl
```

---

# Phase 2 — Install Git

Install Git.

```bash
sudo apt install git
```

Verify version.

```bash
git --version
```

Configure global settings.

```bash
git config --global user.name "Administrator"

git config --global user.email "admin@example.com"
```

Verify configuration.

```bash
git config --list
```

---

# Phase 3 — Create Git User

Create dedicated Git account.

```bash
sudo adduser git
```

Create repository directory.

```bash
sudo mkdir -p /home/git/repos
```

Assign ownership.

```bash
sudo chown -R git:git /home/git/repos
```

---

# Phase 4 — Configure SSH

Generate SSH key.

```bash
ssh-keygen
```

Copy public key.

```bash
ssh-copy-id git@server-ip
```

Test SSH login.

```bash
ssh git@server-ip
```

Disable password authentication.

```text
PasswordAuthentication no
```

Restart SSH.

```bash
sudo systemctl restart ssh
```

---

# Phase 5 — Create Repository

Create a bare repository.

```bash
cd /home/git/repos

git init --bare demo.git
```

Verify.

```bash
ls -l
```

Expected:

```text
demo.git
```

---

# Phase 6 — Clone Repository

Clone repository.

```bash
git clone git@server-ip:/home/git/repos/demo.git
```

Create README.

```bash
echo "# Demo Project" > README.md
```

Commit.

```bash
git add .

git commit -m "Initial Commit"
```

Push.

```bash
git push origin main
```

---

# Phase 7 — Configure Firewall

Install UFW.

```bash
sudo apt install ufw
```

Allow SSH.

```bash
sudo ufw allow OpenSSH
```

Enable.

```bash
sudo ufw enable
```

Verify.

```bash
sudo ufw status
```

---

# Phase 8 — Configure Backups

Backup repositories.

```bash
tar -czf git-backup.tar.gz /home/git/repos
```

Synchronize backups.

```bash
rsync -av /home/git/repos /backup
```

Verify.

```bash
ls -lh
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

Processes.

```bash
ps aux
```

SSH service.

```bash
systemctl status ssh
```

---

# Phase 10 — Harden Server

Install Fail2Ban.

```bash
sudo apt install fail2ban
```

Enable.

```bash
sudo systemctl enable fail2ban

sudo systemctl start fail2ban
```

Install auditd.

```bash
sudo apt install auditd
```

Enable.

```bash
sudo systemctl enable auditd

sudo systemctl start auditd
```

Review ports.

```bash
ss -tuln
```

---

# Phase 11 — Validate Git Operations

Clone repository.

```bash
git clone git@server-ip:/home/git/repos/demo.git
```

Push changes.

```bash
git push
```

Pull changes.

```bash
git pull
```

Verify repository.

```bash
git log
```

---

# Phase 12 — Production Review

Validate:

Git.

```bash
git --version
```

SSH.

```bash
systemctl status ssh
```

Firewall.

```bash
ufw status
```

Disk.

```bash
df -h
```

Logs.

```bash
journalctl
```

Backup.

Verify archive exists.

---

# Repository Structure

Example:

```text
/home/git/repos

├── demo.git

├── project1.git

├── terraform.git

├── ansible.git

└── scripts.git
```

---

# Final Project Checklist

| Item | Status |
|--------|--------|
| Linux Installed | ☐ |
| Git Installed | ☐ |
| Git User Created | ☐ |
| SSH Keys Configured | ☐ |
| Git Repository Created | ☐ |
| Repository Cloned | ☐ |
| Push & Pull Verified | ☐ |
| Firewall Enabled | ☐ |
| Backup Configured | ☐ |
| Monitoring Verified | ☐ |
| Server Hardened | ☐ |
| Production Validation Completed | ☐ |

---

# Production Perspective

Self-hosted Git servers are commonly used for:

- Source code management
- Infrastructure as Code
- CI/CD pipelines
- Configuration repositories
- Documentation
- Automation scripts
- Air-gapped environments
- Enterprise software development

---

# Hands-on Lab

## Task 1

Install Git.

---

## Task 2

Create Git administrator.

---

## Task 3

Generate SSH keys.

---

## Task 4

Create three bare repositories.

---

## Task 5

Clone one repository.

---

## Task 6

Push initial project.

---

## Task 7

Configure repository backup.

---

## Task 8

Add a second developer account and verify collaborative Git operations using SSH authentication.

---

# Production Best Practices

- Use SSH key authentication only.
- Create dedicated Git accounts.
- Restrict repository permissions.
- Backup repositories regularly.
- Enable audit logging.
- Protect the server using a firewall.
- Monitor storage utilization.
- Keep Git updated.
- Review access logs periodically.
- Document repository ownership and access policies.

---

# Challenge Tasks

Complete these additional tasks to extend the project:

- Configure Git hooks for commit validation.
- Host multiple development teams.
- Configure repository access using Linux groups.
- Implement repository backup automation with cron.
- Mirror repositories to a secondary Git server.
- Configure automatic security updates.
- Install Prometheus Node Exporter.
- Build a repository usage dashboard.
- Integrate the Git server with Jenkins or GitLab CI.
- Deploy Git over HTTPS using Nginx and TLS.

---

# Skills Demonstrated

After completing this project, you will have demonstrated proficiency in:

- Git Administration
- Linux Security
- SSH Authentication
- Repository Management
- User Management
- Backup Strategy
- Monitoring
- Production Hardening
- Enterprise Linux Administration

---

# Congratulations!

You have successfully deployed a **production-ready Git Server**.

Your Git server now provides secure version control for developers while protecting repositories through SSH authentication, proper permissions, backups, monitoring, and system hardening.

This project reflects how many organizations manage internal source code repositories for software development, Infrastructure as Code, and automation.

---

## What's Next?

**[Capstone Project 4 — Create a Monitoring Server](monitoring-server.md)**

You'll learn how to:


- Install Prometheus
- Configure Node Exporter
- Install Grafana
- Build monitoring dashboards
- Configure alerting
- Monitor Linux servers
- Visualize infrastructure health

By the end of the project, you'll have a centralized monitoring server capable of collecting metrics, displaying dashboards, and monitoring the health of multiple Linux systems in a production environment.
