---
title: "SSH Hardening — Securing Remote Access to Linux Systems"
description: "Harden OpenSSH for production — disable root login, enforce key authentication, restrict users, validate sshd_config, and avoid lockouts."
difficulty: advanced
estimated_time: "90 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 11 · Linux Security"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - security-engineer
tags:
  - linux
  - security
  - ssh
  - hardening
  - authentication
  - rebash-linux-mastery
comments: false
status: ready
---

# SSH Hardening — Securing Remote Access to Linux Systems

> **SSH Hardening** is the process of securing the Secure Shell (SSH) service to reduce the risk of unauthorized access and attacks. Since SSH is the primary method for remotely administering Linux servers, it is a common target for attackers. Proper SSH hardening involves disabling insecure authentication methods, limiting access, enforcing strong authentication, and monitoring login activity. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, and Site Reliability Engineer (SRE) should understand how to secure SSH in production environments.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 11: Linux Security → Lesson 1</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Advanced</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Linux Security</div>

<div markdown>**Lesson:** 1 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand SSH security risks
- Secure the SSH server configuration
- Disable root login
- Configure key-based authentication
- Disable password authentication
- Change SSH settings securely
- Restrict SSH access
- Apply production SSH hardening best practices

---

# Prerequisites

Complete:

- Modules 1–10 of Linux Mastery

---

# Why Learn SSH Hardening?

Imagine a production server exposed to the Internet.

Default configuration:

```text
SSH Port 22

↓

Root Login Enabled

↓

Password Authentication Enabled

↓

Brute Force Attacks
```

A hardened configuration:

```text
SSH

↓

Key Authentication

↓

Root Login Disabled

↓

Restricted Users

↓

Secure Remote Access
```

Hardening significantly reduces the attack surface.

---

# What is SSH Hardening?

SSH hardening is the process of configuring the SSH service to improve security.

Objectives include:

- Prevent unauthorized access
- Reduce attack surface
- Enforce strong authentication
- Protect administrative accounts
- Improve auditing

---

# SSH Configuration File

The OpenSSH server configuration file is:

```text
/etc/ssh/sshd_config
```

View it:

```bash
sudo cat /etc/ssh/sshd_config
```

Always create a backup before making changes.

```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
```

---

# Disable Root Login

Allow administrators to log in using a regular account and elevate privileges with `sudo`.

Configuration:

```text
PermitRootLogin no
```

Restart SSH.

```bash
sudo systemctl restart ssh
```

or

```bash
sudo systemctl restart sshd
```

(depending on the Linux distribution)

---

# Disable Password Authentication

Use SSH keys instead of passwords.

Configuration:

```text
PasswordAuthentication no
```

This prevents password-based brute-force attacks.

!!! warning "Important"

    Verify SSH key authentication works before disabling password authentication.

---

# Enable Public Key Authentication

Ensure public key authentication is enabled.

```text
PubkeyAuthentication yes
```

---

# Restrict SSH Users

Allow only specific users.

```text
AllowUsers basha admin
```

Or allow specific groups.

```text
AllowGroups sshadmins
```

This limits who can log in through SSH.

---

# Disable Empty Passwords

```text
PermitEmptyPasswords no
```

Never allow accounts without passwords.

---

# Configure Login Grace Time

Limit the time allowed for authentication.

```text
LoginGraceTime 30
```

Example:

```text
30 seconds
```

---

# Limit Authentication Attempts

Reduce brute-force opportunities.

```text
MaxAuthTries 3
```

After three failed attempts, the connection is closed.

---

# Limit Concurrent Sessions

Example:

```text
MaxSessions 5
```

This helps prevent abuse.

---

# Change the Default SSH Port

Default:

```text
22
```

Example:

```text
Port 2222
```

Changing the port may reduce automated scanning but **should not be considered a replacement for proper security controls** such as key-based authentication, firewall rules, and account restrictions.

---

# Use Strong SSH Keys

Generate an Ed25519 key pair.

```bash
ssh-keygen -t ed25519
```

Or generate an RSA key.

```bash
ssh-keygen -t rsa -b 4096
```

Ed25519 is generally recommended for new deployments due to its strong security and smaller key size.

---

# Disable X11 Forwarding

Unless required:

```text
X11Forwarding no
```

---

# Disable TCP Forwarding

If unnecessary:

```text
AllowTcpForwarding no
```

---

# Enable Client Keepalive

Disconnect inactive sessions.

```text
ClientAliveInterval 300

ClientAliveCountMax 2
```

Inactive sessions are automatically closed.

---

# Verify SSH Configuration

Check for syntax errors.

```bash
sudo sshd -t
```

No output indicates the configuration is valid.

---

# Restart the SSH Service

Ubuntu/Debian:

```bash
sudo systemctl restart ssh
```

RHEL/CentOS:

```bash
sudo systemctl restart sshd
```

---

# Test Before Closing Your Session

Always open a **new terminal** and verify that you can log in successfully before closing your existing SSH session. This helps prevent accidentally locking yourself out of the server.

---

# Common Commands

View configuration.

```bash
sudo cat /etc/ssh/sshd_config
```

Validate configuration.

```bash
sudo sshd -t
```

Restart service.

```bash
sudo systemctl restart ssh
```

Generate SSH key.

```bash
ssh-keygen -t ed25519
```

Check SSH service.

```bash
systemctl status ssh
```

---

# Real Production Examples

Disable root login.

```text
PermitRootLogin no
```

Disable password authentication.

```text
PasswordAuthentication no
```

Restrict users.

```text
AllowUsers devops admin
```

Generate SSH keys.

```bash
ssh-keygen -t ed25519
```

---

# Production Perspective

SSH hardening is essential for:

- Linux servers
- Cloud virtual machines
- Kubernetes nodes
- Bastion hosts
- Database servers
- Production web servers
- Enterprise infrastructure
- Remote administration

A hardened SSH configuration significantly reduces the likelihood of unauthorized access.

---

# Hands-on Lab

## Task 1

Backup the SSH configuration.

```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
```

---

## Task 2

View the configuration.

```bash
sudo nano /etc/ssh/sshd_config
```

---

## Task 3

Disable root login.

```text
PermitRootLogin no
```

---

## Task 4

Disable password authentication.

```text
PasswordAuthentication no
```

---

## Task 5

Restrict SSH users.

```text
AllowUsers youruser
```

Replace `youruser` with your actual username.

---

## Task 6

Validate the configuration.

```bash
sudo sshd -t
```

---

## Task 7

Restart the SSH service.

```bash
sudo systemctl restart ssh
```

or

```bash
sudo systemctl restart sshd
```

---

## Task 8

Open a new terminal and verify that SSH login works before closing your current session.

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `ssh-keygen` | Generate SSH keys | Secure authentication |
| `sshd -t` | Validate configuration | Prevent configuration errors |
| `systemctl restart ssh` | Restart SSH service | Apply changes |
| `systemctl status ssh` | Check service status | Troubleshooting |
| `cp` | Backup configuration | Change management |
| `nano` | Edit configuration | Administration |

---

# Common SSH Hardening Mistakes

| Mistake | Solution |
|----------|----------|
| Disabling passwords before configuring SSH keys | Verify key-based login first |
| Forgetting to validate configuration | Run `sshd -t` |
| Locking yourself out | Test in a new session |
| Allowing root login | Disable `PermitRootLogin` |
| Allowing unlimited login attempts | Configure `MaxAuthTries` |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    An administrator disables password authentication but forgets to configure SSH keys.

Result:

```text
SSH Login

↓

Authentication Failed

↓

Administrator Locked Out
```

Correct approach:

1. Generate SSH keys.
2. Copy the public key to the server.
3. Verify key-based login in a new terminal.
4. Disable password authentication.
5. Restart the SSH service.

This sequence ensures uninterrupted administrative access.

---

# Best Practices

- Disable direct root login.
- Use SSH key authentication.
- Disable password authentication after verifying keys.
- Restrict SSH access to authorized users or groups.
- Limit authentication attempts.
- Validate configuration before restarting the service.
- Test changes in a new session before disconnecting.
- Keep OpenSSH updated with security patches.

---

# Common Mistakes

❌ Leaving root login enabled.

✅ Do not leave root login enabled.

---

❌ Using password authentication in production.

✅ Avoid using password authentication in production when a safer approach exists.

---

❌ Not backing up the SSH configuration before editing.

✅ Always backing up the SSH configuration before editing.

---

❌ Restarting SSH without validating the configuration.

✅ Avoid this mistake: restarting SSH without validating the configuration.

---

❌ Closing the active SSH session before testing new settings.

✅ Avoid this mistake: closing the active SSH session before testing new settings.

---

# Interview Questions
## Beginner

1. What is SSH?
2. Why should root login be disabled?
3. What is the purpose of SSH key authentication?
4. Which file stores the SSH server configuration?

---

## Intermediate

1. Why is key-based authentication more secure than passwords?
2. What does `MaxAuthTries` do?
3. Why should `sshd -t` be run before restarting SSH?
4. What is the purpose of `AllowUsers`?

---

## Architect Level

1. How would you securely manage SSH access across hundreds of Linux servers?
2. How would you design a secure bastion host architecture?
3. What SSH hardening controls would you require for production cloud environments?

---

# Summary

In this lesson, you learned:

- SSH hardening fundamentals
- SSH server configuration
- Disabling root login
- Key-based authentication
- Restricting SSH access
- Limiting authentication attempts
- Validating configuration
- Production SSH security best practices

SSH is one of the most critical services on a Linux server and is often the primary entry point for administrators. Properly hardening SSH reduces the attack surface, strengthens authentication, and helps protect production systems from unauthorized access.

---

## Key Takeaways

- Disable direct root login.
- Prefer SSH keys over passwords.
- Restrict SSH access to authorized users.
- Validate configuration before restarting the SSH service.
- Always test changes in a new session.
- Combine SSH hardening with firewalls, monitoring, and regular security updates for a layered defense.

---

## What's Next?

**[File Permissions Review — Securing Files and Directories in Linux](file-permissions-security-review.md)**

You'll explore:

- Linux permission model
- Ownership and permissions
- Numeric and symbolic permissions
- Special permissions (SUID, SGID, Sticky Bit)
- Secure permission practices
- Permission auditing
- Production security examples

By the end of the lesson, you'll be able to review, audit, and secure file permissions to protect Linux systems from unauthorized access and accidental modifications.
