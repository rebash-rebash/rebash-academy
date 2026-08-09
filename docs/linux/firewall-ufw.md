---
title: "Firewall (UFW) — Securing Linux Network Access"
description: "Secure Linux with UFW — default deny policies, allow SSH safely, manage ports and app profiles, logging, and production firewall practices."
difficulty: intermediate
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
  - firewall
  - ufw
  - networking
  - rebash-linux-mastery
comments: false
status: ready
---

# Firewall (UFW) — Securing Linux Network Access

> A **Firewall** controls incoming and outgoing network traffic based on predefined security rules. It acts as the first line of defense by allowing legitimate connections while blocking unauthorized access. **UFW (Uncomplicated Firewall)** is a user-friendly firewall management tool for Linux that simplifies configuring `iptables` or `nftables` (depending on the distribution). Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, and Site Reliability Engineer (SRE) should know how to configure UFW to protect production systems.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 11: Linux Security → Lesson 3</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Linux Security</div>

<div markdown>**Lesson:** 3 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand firewall fundamentals
- Install and enable UFW
- Allow and deny network traffic
- Open and close ports
- Configure application profiles
- Monitor firewall rules
- Troubleshoot firewall issues
- Apply production firewall best practices

---

# Prerequisites

Complete:

- Modules 1–10
- Module 11 Lessons 1–2

---

# Why Learn Firewalls?

Imagine a Linux server connected directly to the Internet.

Without a firewall:

```text
Internet

↓

All Ports Open

↓

Attack Surface Increases
```

With a firewall:

```text
Internet

↓

Firewall

↓

Only Approved Ports

↓

Secure Server
```

A firewall significantly reduces the attack surface.

---

# What is UFW?

**UFW (Uncomplicated Firewall)** is a command-line utility that simplifies Linux firewall management.

UFW allows administrators to:

- Allow traffic
- Deny traffic
- Restrict traffic
- Manage ports
- Control protocols
- Configure default security policies

---

# Install UFW

Ubuntu/Debian:

```bash
sudo apt install ufw
```

Verify installation.

```bash
ufw version
```

---

# Check Firewall Status

```bash
sudo ufw status
```

Example:

```text
Status: inactive
```

---

# Enable the Firewall

```bash
sudo ufw enable
```

Example:

```text
Firewall is active and enabled on system startup.
```

---

# Disable the Firewall

```bash
sudo ufw disable
```

Use only when necessary.

---

# Default Firewall Policies

A secure starting point is:

```bash
sudo ufw default deny incoming

sudo ufw default allow outgoing
```

Meaning:

- Block unsolicited incoming connections.
- Allow outbound connections initiated by the server.

---

# Allow SSH

Before enabling the firewall on a remote server, allow SSH access.

```bash
sudo ufw allow ssh
```

Or specify the port.

```bash
sudo ufw allow 22/tcp
```

!!! warning "Important"

    Always allow SSH before enabling UFW on a remote system to avoid locking yourself out.

---

# Allow Specific Ports

Allow HTTP.

```bash
sudo ufw allow 80/tcp
```

Allow HTTPS.

```bash
sudo ufw allow 443/tcp
```

Allow a custom application.

```bash
sudo ufw allow 8080/tcp
```

---

# Deny Traffic

Block a port.

```bash
sudo ufw deny 21/tcp
```

---

# Reject Connections

```bash
sudo ufw reject 23/tcp
```

Unlike `deny`, `reject` informs the client that the connection was refused.

---

# Allow UDP Traffic

Example:

```bash
sudo ufw allow 53/udp
```

Useful for DNS services.

---

# Delete a Rule

Delete by rule.

```bash
sudo ufw delete allow 8080/tcp
```

---

# Numbered Rules

Display numbered rules.

```bash
sudo ufw status numbered
```

Example:

```text
[1] 22/tcp ALLOW IN Anywhere

[2] 80/tcp ALLOW IN Anywhere
```

Delete by number.

```bash
sudo ufw delete 2
```

---

# Application Profiles

View available profiles.

```bash
sudo ufw app list
```

Example:

```text
Apache

OpenSSH

Nginx Full
```

Allow an application profile.

```bash
sudo ufw allow OpenSSH
```

---

# View Firewall Rules

```bash
sudo ufw status verbose
```

Shows:

- Rules
- Default policies
- Logging status

---

# Enable Firewall Logging

```bash
sudo ufw logging on
```

Logging helps monitor blocked and allowed traffic.

---

# Reload Firewall

After making changes:

```bash
sudo ufw reload
```

---

# Reset UFW

Restore default settings.

```bash
sudo ufw reset
```

Use with caution because all custom rules are removed.

---

# Common Commands

Enable firewall.

```bash
sudo ufw enable
```

View status.

```bash
sudo ufw status
```

Allow SSH.

```bash
sudo ufw allow ssh
```

Allow HTTPS.

```bash
sudo ufw allow 443/tcp
```

Reload rules.

```bash
sudo ufw reload
```

---

# Real Production Examples

Secure web server.

```bash
sudo ufw default deny incoming

sudo ufw default allow outgoing

sudo ufw allow OpenSSH

sudo ufw allow 80/tcp

sudo ufw allow 443/tcp
```

Allow Kubernetes API (example).

```bash
sudo ufw allow 6443/tcp
```

Allow application port.

```bash
sudo ufw allow 3000/tcp
```

---

# Production Perspective

Firewalls are essential for:

- Cloud virtual machines
- Web servers
- Database servers
- Bastion hosts
- Kubernetes nodes
- CI/CD servers
- Monitoring systems
- Enterprise infrastructure

A properly configured firewall blocks unnecessary services while allowing only authorized network traffic.

---

# Hands-on Lab

## Task 1

Check firewall status.

```bash
sudo ufw status
```

---

## Task 2

Enable UFW.

```bash
sudo ufw enable
```

---

## Task 3

Allow SSH.

```bash
sudo ufw allow ssh
```

---

## Task 4

Allow HTTP and HTTPS.

```bash
sudo ufw allow 80/tcp

sudo ufw allow 443/tcp
```

---

## Task 5

Allow a custom port.

```bash
sudo ufw allow 8080/tcp
```

---

## Task 6

View numbered rules.

```bash
sudo ufw status numbered
```

---

## Task 7

Enable logging.

```bash
sudo ufw logging on
```

---

## Task 8

Display verbose status.

```bash
sudo ufw status verbose
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `ufw enable` | Enable firewall | Server protection |
| `ufw status` | Display rules | Security verification |
| `ufw allow` | Allow traffic | Service access |
| `ufw deny` | Block traffic | Attack prevention |
| `ufw reload` | Reload configuration | Apply changes |
| `ufw logging on` | Enable logging | Security monitoring |

---

# Common Firewall Mistakes

| Mistake | Solution |
|----------|----------|
| Enabling UFW before allowing SSH | Allow SSH first |
| Allowing unnecessary ports | Open only required ports |
| Forgetting to review firewall rules | Audit rules regularly |
| Disabling the firewall permanently | Keep it enabled unless required |
| Ignoring firewall logs | Monitor blocked connections |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    An administrator enables UFW on a remote server.

Commands:

```bash
sudo ufw enable
```

SSH was never allowed.

Result:

```text
SSH Connection

↓

Blocked

↓

Administrator Locked Out
```

Correct procedure:

```bash
sudo ufw allow ssh

sudo ufw enable

sudo ufw status
```

Always verify SSH connectivity before ending the existing session.

---

# Best Practices

- Apply the principle of least privilege.
- Allow only required ports.
- Set the default policy to deny incoming traffic.
- Allow SSH before enabling UFW.
- Remove unused firewall rules.
- Enable firewall logging.
- Review firewall rules regularly.
- Test connectivity after firewall changes.

---

# Common Mistakes

❌ Allowing all ports unnecessarily.

✅ Do not allow all ports unnecessarily.

---

❌ Forgetting to allow SSH before enabling the firewall.

✅ Remember to to allow SSH before enabling the firewall.

---

❌ Leaving unused ports open.

✅ Do not leave unused ports open.

---

❌ Never reviewing firewall rules.

✅ Always reviewing firewall rules.

---

❌ Disabling the firewall instead of updating rules.

✅ Prefer updating rules rather than disabling the firewall.

---

# Interview Questions
## Beginner

1. What is a firewall?
2. What is UFW?
3. Which command enables UFW?
4. How do you allow SSH access?

---

## Intermediate

1. What is the difference between `allow`, `deny`, and `reject`?
2. Why should incoming traffic be denied by default?
3. How do you delete a firewall rule?
4. How do you view numbered firewall rules?

---

## Architect Level

1. How would you design firewall rules for a production web application?
2. How would you secure cloud virtual machines using UFW?
3. What firewall strategy would you recommend for Kubernetes worker nodes and control plane servers?

---

# Summary

In this lesson, you learned:

- Firewall fundamentals
- Installing and configuring UFW
- Default firewall policies
- Allowing and denying traffic
- Application profiles
- Firewall logging
- Rule management
- Production firewall best practices

A properly configured firewall is a critical layer of Linux security. By allowing only necessary network traffic and blocking everything else, UFW helps reduce the attack surface and protect systems from unauthorized access.

---

## Key Takeaways

- UFW simplifies Linux firewall management.
- Deny incoming traffic by default and allow outgoing traffic.
- Allow SSH before enabling the firewall on remote servers.
- Open only the ports required by your applications.
- Enable logging and review firewall rules regularly.
- Treat the firewall as one layer of a broader defense-in-depth strategy.

---

## What's Next?

**[SELinux Overview — Mandatory Access Control in Linux](selinux-overview.md)**

You'll explore:

- What SELinux is
- SELinux architecture
- Enforcing, Permissive, and Disabled modes
- Security contexts
- SELinux policies
- Common SELinux commands
- Production security practices

By the end of the lesson, you'll understand how SELinux provides mandatory access control (MAC) to strengthen Linux security beyond traditional file permissions.
