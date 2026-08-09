---
title: "Capstone Project 6 — Build a Linux Server Baseline"
description: "Build a production Linux Server Baseline — packages, SSH hardening, UFW, Fail2Ban, auditd, logging, monitoring, and a reusable baseline script."
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
  - baseline
  - hardening
  - automation
  - production
  - rebash-linux-mastery
comments: false
status: ready
---

# Capstone Project 6 — Build a Linux Server Baseline

> A **Linux Server Baseline** is a standardized operating system configuration that serves as the foundation for all production Linux servers. Instead of configuring every server manually, organizations create a baseline containing approved security settings, system packages, user accounts, logging, monitoring, networking, and operational standards. Every new server starts from this baseline, ensuring consistency, security, compliance, and easier maintenance. In this capstone project, you'll build a production-ready Linux Server Baseline suitable for enterprise environments.

---

# Project Overview

## Objective

Build a standardized Linux Server Baseline that can be used as the starting point for all production servers.

---

## Skills Covered

- Linux Administration
- Server Standardization
- Package Management
- User Management
- SSH Hardening
- Firewall Configuration
- Monitoring
- Logging
- Security Hardening
- Bash Automation
- Production Validation

---

# Estimated Time

**6–8 Hours**

---

# Difficulty

Beginner → Advanced

---

# Project Architecture

```text
             Fresh Linux Installation
                       │
                       ▼
            Baseline Configuration
                       │
      ┌────────────────┼────────────────┐
      │                │                │
 Security         Monitoring      Logging
      │                │                │
      └────────────────┼────────────────┘
                       │
               Production Validation
                       │
                       ▼
            Production Ready Server
```

---

# Learning Outcomes

By completing this project, you'll be able to:

- Standardize Linux servers
- Configure production security
- Build reusable server templates
- Configure monitoring and logging
- Apply enterprise operational standards
- Automate baseline configuration
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
- OpenSSH Server
- UFW
- Fail2Ban
- auditd
- rsyslog
- logrotate
- cron
- Bash

---

# Project Tasks

| Phase | Task |
|---------|------|
| 1 | Install Linux |
| 2 | Update System |
| 3 | Install Standard Packages |
| 4 | Configure Users |
| 5 | Secure SSH |
| 6 | Configure Firewall |
| 7 | Configure Logging |
| 8 | Configure Monitoring |
| 9 | Configure Security |
| 10 | Create Baseline Script |
| 11 | Validate Configuration |
| 12 | Document Baseline |

---

# Phase 1 — Install Linux

Update packages.

```bash
sudo apt update

sudo apt upgrade -y
```

Verify installation.

```bash
hostnamectl
```

---

# Phase 2 — Update System

Install latest security updates.

```bash
sudo apt full-upgrade -y
```

Remove unused packages.

```bash
sudo apt autoremove -y
```

Clean package cache.

```bash
sudo apt clean
```

---

# Phase 3 — Install Standard Packages

Install commonly required packages.

```bash
sudo apt install -y \
git \
curl \
wget \
vim \
htop \
tree \
zip \
unzip \
net-tools \
dnsutils \
rsync \
jq \
fail2ban \
auditd
```

Verify.

```bash
dpkg -l
```

---

# Phase 4 — Configure Users

Create administrator.

```bash
sudo adduser adminuser
```

Grant sudo.

```bash
sudo usermod -aG sudo adminuser
```

Verify.

```bash
id adminuser
```

Remove unused accounts.

```bash
getent passwd
```

---

# Phase 5 — Secure SSH

Edit configuration.

```bash
sudo nano /etc/ssh/sshd_config
```

Recommended settings.

```text
PermitRootLogin no

PasswordAuthentication no

PubkeyAuthentication yes

MaxAuthTries 3

ClientAliveInterval 300

X11Forwarding no
```

Restart SSH.

```bash
sudo systemctl restart ssh
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

# Phase 7 — Configure Logging

Verify system logs.

```bash
journalctl
```

Check rsyslog.

```bash
systemctl status rsyslog
```

Verify log rotation.

```bash
logrotate -d /etc/logrotate.conf
```

---

# Phase 8 — Configure Monitoring

Review CPU.

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

Services.

```bash
systemctl
```

---

# Phase 9 — Configure Security

Install Fail2Ban.

```bash
sudo systemctl enable fail2ban

sudo systemctl start fail2ban
```

Install auditd.

```bash
sudo systemctl enable auditd

sudo systemctl start auditd
```

Review listening ports.

```bash
ss -tuln
```

Review failed services.

```bash
systemctl --failed
```

---

# Phase 10 — Create Baseline Script

Create automation script.

```bash
touch baseline.sh

chmod +x baseline.sh
```

The script should:

- Update the system
- Install standard packages
- Configure SSH
- Enable firewall
- Install monitoring tools
- Configure logging
- Enable security services
- Generate a completion report

Run.

```bash
sudo ./baseline.sh
```

---

# Phase 11 — Validate Configuration

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

Storage.

```bash
df -h
```

Logs.

```bash
journalctl -p err
```

---

# Phase 12 — Document Baseline

Create documentation including:

- Installed packages
- Security configuration
- Firewall rules
- SSH configuration
- Monitoring tools
- Logging configuration
- Backup procedures
- Validation checklist

Store documentation in Git for version control.

---

# Example Baseline Structure

```text
Linux Server

├── Updates Applied

├── Standard Packages

├── SSH Hardened

├── Firewall Enabled

├── Monitoring Configured

├── Logging Enabled

├── Fail2Ban Enabled

├── auditd Enabled

└── Validation Complete
```

---

# Final Project Checklist

| Item | Status |
|--------|--------|
| Linux Installed | ☐ |
| Updates Applied | ☐ |
| Standard Packages Installed | ☐ |
| Administrator Created | ☐ |
| SSH Hardened | ☐ |
| Firewall Enabled | ☐ |
| Logging Configured | ☐ |
| Monitoring Configured | ☐ |
| Security Services Enabled | ☐ |
| Baseline Script Created | ☐ |
| Validation Completed | ☐ |
| Documentation Completed | ☐ |

---

# Production Perspective

Linux Server Baselines are widely used for:

- Cloud Virtual Machines
- Kubernetes Worker Nodes
- Database Servers
- CI/CD Servers
- Web Servers
- Application Servers
- Enterprise Linux Deployments
- Government and Financial Infrastructure

Organizations often build server baselines into golden images, VM templates, or Infrastructure as Code pipelines.

---

# Hands-on Lab

## Task 1

Install standard administration tools.

---

## Task 2

Create an administrator account.

---

## Task 3

Secure SSH configuration.

---

## Task 4

Enable the firewall.

---

## Task 5

Install and enable Fail2Ban.

---

## Task 6

Install and enable auditd.

---

## Task 7

Create a Bash script that automates the complete server baseline configuration.

---

## Task 8

Validate the server using a checklist and generate a baseline report containing:

- Installed packages
- Running services
- Open ports
- Security configuration
- Monitoring status
- Validation results

---

# Production Best Practices

- Standardize every production server.
- Apply security updates before deployment.
- Use SSH keys instead of passwords.
- Install only required packages.
- Enable logging and auditing.
- Protect servers with firewalls.
- Automate baseline creation.
- Store baseline scripts in Git.
- Review and update the baseline regularly.
- Validate every server before production deployment.

---

# Challenge Tasks

Complete these additional tasks to extend the project:

- Build a golden VM image from the baseline.
- Convert the baseline script into an Ansible playbook.
- Implement CIS Benchmark recommendations.
- Configure automatic security updates.
- Install Prometheus Node Exporter.
- Generate HTML baseline reports.
- Integrate baseline validation into a CI/CD pipeline.
- Build compliance checks using Bash.
- Create a rollback script.
- Package the baseline as a reusable server template.

---

# Skills Demonstrated

After completing this project, you will have demonstrated proficiency in:

- Linux Administration
- Server Standardization
- Security Hardening
- Bash Automation
- Logging
- Monitoring
- Firewall Administration
- SSH Administration
- Production Validation
- Enterprise Linux Operations

---

# Congratulations!

You have successfully built a **production-ready Linux Server Baseline**.

Your baseline now provides a standardized, secure, and repeatable foundation for deploying Linux servers across development, testing, and production environments.

This approach is widely adopted by enterprise IT teams, cloud providers, and DevOps organizations to ensure every server starts from a consistent, secure, and maintainable configuration.

---

## What's Next?

**[Capstone Project 7 — Harden an Ubuntu Server](harden-ubuntu-server.md)**

You'll learn how to:


- Apply CIS-inspired security hardening
- Secure SSH and user authentication
- Strengthen file permissions
- Configure UFW and Fail2Ban
- Enable auditing and logging
- Reduce the attack surface
- Perform a complete production security review

By the end of the project, you'll transform a default Ubuntu installation into a hardened production server that follows industry security best practices.
