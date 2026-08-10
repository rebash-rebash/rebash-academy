---
title: "Capstone Project 1 — Build a Secure Linux Web Server"
description: "Build a production-ready secure Linux web server — SSH hardening, UFW, Nginx, HTTPS, Fail2Ban, logging, monitoring, backups, and production validation."
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
tags:
  - linux
  - capstone
  - nginx
  - security
  - https
  - production
  - rebash-linux-mastery
comments: false
status: ready
---

# Capstone Project 1 — Build a Secure Linux Web Server

> In this capstone project, you'll build a **production-ready secure Linux web server** from scratch. Rather than simply installing a web server, you'll configure networking, users, SSH security, firewalls, web services, TLS, monitoring, logging, backups, and system hardening. This project combines everything learned throughout the Linux Mastery course and closely resembles the tasks performed by Linux System Administrators, DevOps Engineers, Cloud Engineers, and Site Reliability Engineers (SREs) in production environments.

---


# Project Overview

## Objective

Build a secure Linux web server suitable for hosting production web applications.

---

## Skills Covered

- Linux installation
- User management
- File permissions
- SSH Hardening
- Firewall configuration
- Web server installation
- HTTPS configuration
- Process management
- Systemd
- Monitoring
- Logging
- Backup
- Security hardening
- Performance tuning
- Production validation

---

# Estimated Time

**6–8 Hours**

---

# Difficulty

Beginner → Advanced

---

# Project Architecture

```text
                    Internet
                        │
                        │
                HTTPS (443)
                        │
                +----------------+
                |    Firewall    |
                +----------------+
                        │
                        │
                +----------------+
                | Ubuntu Server  |
                +----------------+
                │
        ┌───────┴────────┐
        │                │
     SSH (22)        Nginx (443)
        │                │
        └───────┬────────┘
                │
        Static Website
```

---

# Learning Outcomes

By completing this project, you'll be able to:

- Build a secure Linux server
- Deploy a production-ready web server
- Secure remote administration
- Configure HTTPS
- Protect services with a firewall
- Monitor Linux servers
- Configure backups
- Validate production readiness

---

# Project Requirements

## Hardware

Minimum:

- 2 vCPU
- 2 GB RAM
- 20 GB Disk

Recommended:

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

- Ubuntu Linux
- OpenSSH Server
- Nginx
- UFW Firewall
- Fail2Ban
- Certbot (Let's Encrypt)
- rsync
- logrotate

---

# Project Tasks

| Phase | Task |
|---------|------|
| 1 | Install Linux |
| 2 | Configure Networking |
| 3 | Configure Users |
| 4 | Secure SSH |
| 5 | Configure Firewall |
| 6 | Install Nginx |
| 7 | Deploy Website |
| 8 | Configure HTTPS |
| 9 | Configure Logging |
| 10 | Configure Monitoring |
| 11 | Configure Backup |
| 12 | Harden Server |
| 13 | Production Validation |

---

# Phase 1 — Install Linux

Install Ubuntu Server.

Verify installation.

```bash
hostnamectl
```

Update packages.

```bash
sudo apt update

sudo apt upgrade -y
```

---

# Phase 2 — Configure Networking

Display interfaces.

```bash
ip addr
```

Display routes.

```bash
ip route
```

Test connectivity.

```bash
ping google.com
```

Configure hostname.

```bash
sudo hostnamectl set-hostname web01
```

Verify DNS.

```bash
dig google.com
```

---

# Phase 3 — Configure Users

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

Disable direct root SSH login.

---

# Phase 4 — Secure SSH

Edit configuration.

```bash
sudo nano /etc/ssh/sshd_config
```

Recommended settings:

```text
PermitRootLogin no

PasswordAuthentication no

PubkeyAuthentication yes

X11Forwarding no

MaxAuthTries 3
```

Restart SSH.

```bash
sudo systemctl restart ssh
```

---

# Phase 5 — Configure Firewall

Install UFW.

```bash
sudo apt install ufw
```

Allow SSH.

```bash
sudo ufw allow OpenSSH
```

Allow HTTPS.

```bash
sudo ufw allow 443/tcp
```

Allow HTTP.

```bash
sudo ufw allow 80/tcp
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

# Phase 6 — Install Nginx

Install.

```bash
sudo apt install nginx
```

Start service.

```bash
sudo systemctl enable nginx

sudo systemctl start nginx
```

Verify.

```bash
systemctl status nginx
```

Test.

```bash
curl localhost
```

---

# Phase 7 — Deploy Website

Example page.

```html
<h1>

Linux Mastery

</h1>

<p>

Production Secure Web Server

</p>
```

Copy.

```bash
sudo cp index.html /var/www/html/
```

Verify.

```bash
curl localhost
```

---

# Phase 8 — Configure HTTPS

Install.

```bash
sudo apt install certbot python3-certbot-nginx
```

Obtain certificate.

```bash
sudo certbot --nginx
```

Verify.

```bash
curl https://your-domain
```

Renewal test.

```bash
sudo certbot renew --dry-run
```

---

# Phase 9 — Configure Logging

View logs.

```bash
journalctl -u nginx
```

Access logs.

```bash
tail -f /var/log/nginx/access.log
```

Error logs.

```bash
tail -f /var/log/nginx/error.log
```

Verify log rotation.

```bash
logrotate -d /etc/logrotate.conf
```

---

# Phase 10 — Configure Monitoring

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

Services.

```bash
systemctl status nginx
```

---

# Phase 11 — Configure Backup

Create backup.

```bash
sudo tar -czf nginx-backup.tar.gz /etc/nginx
```

Synchronize.

```bash
rsync -av /var/www /backup
```

Verify.

```bash
ls -lh
```

---

# Phase 12 — Harden Server

Install Fail2Ban.

```bash
sudo apt install fail2ban
```

Start.

```bash
sudo systemctl enable fail2ban

sudo systemctl start fail2ban
```

Verify.

```bash
fail2ban-client status
```

Review listening ports.

```bash
ss -tuln
```

Remove unnecessary packages.

```bash
sudo apt autoremove
```

Apply updates.

```bash
sudo apt update

sudo apt upgrade
```

---

# Phase 13 — Production Validation

Validate:

SSH

```bash
ssh adminuser@server
```

---

Firewall

```bash
ufw status
```

---

HTTPS

```bash
curl https://your-domain
```

---

Nginx

```bash
systemctl status nginx
```

---

Logs

```bash
journalctl -u nginx
```

---

Backup

Verify archive exists.

---

Monitoring

Review CPU, memory, storage.

---

# Final Project Checklist

| Item | Status |
|--------|--------|
| Linux Installed | ☐ |
| Updates Applied | ☐ |
| Hostname Configured | ☐ |
| Admin User Created | ☐ |
| SSH Hardened | ☐ |
| Firewall Enabled | ☐ |
| Nginx Installed | ☐ |
| Website Deployed | ☐ |
| HTTPS Enabled | ☐ |
| Logging Verified | ☐ |
| Monitoring Configured | ☐ |
| Backup Created | ☐ |
| Fail2Ban Enabled | ☐ |
| Production Validation Completed | ☐ |

---

# Project Deliverables

At the end of this project, you should have:

- A secure Ubuntu Server
- A hardened SSH configuration
- A firewall protecting the server
- An Nginx web server serving a website
- HTTPS configured with a valid certificate
- Monitoring and logging in place
- Backup procedures documented
- A production-ready Linux web server

---

# Challenge Tasks

Complete these additional tasks to extend the project:

- Configure automatic security updates.
- Create a custom Nginx virtual host.
- Host two websites using different domain names.
- Configure HTTP-to-HTTPS redirection.
- Enable Nginx rate limiting.
- Configure custom error pages (404 and 500).
- Add system resource monitoring using Prometheus Node Exporter.
- Configure automatic daily website backups using `cron`.
- Create a Bash script to verify web server health.
- Harden the server using CIS Benchmark recommendations.

---

# Skills Demonstrated

After completing this capstone project, you will have demonstrated proficiency in:

- Linux System Administration
- Server Hardening
- User and Permission Management
- SSH Security
- Firewall Configuration
- Web Server Administration
- TLS/HTTPS Configuration
- Monitoring and Logging
- Backup and Recovery
- Production Validation
- Security Best Practices
- Operational Excellence

---

# Congratulations!

You have successfully built a **production-ready Secure Linux Web Server**.

This project closely mirrors the work performed by Linux Administrators, DevOps Engineers, Cloud Engineers, and Site Reliability Engineers in enterprise production environments.

You have applied concepts from nearly every module of the Linux Mastery course, transforming theoretical knowledge into practical, real-world experience.

---

## What's Next?

**[Capstone Project 2 — Configure a Bastion Host](bastion-host.md)**

You'll learn how to:

- Build a secure jump server
- Restrict SSH access
- Configure key-based authentication
- Implement network access controls
- Enable centralized logging
- Audit administrator access
- Protect production infrastructure

By the end of the project, you'll have a production-ready Bastion Host that securely manages administrative access to Linux servers across enterprise environments.
