---
title: "SELinux Overview — Mandatory Access Control in Linux"
description: "Understand SELinux — MAC vs DAC, enforcing modes, security contexts, restorecon, booleans, and production troubleshooting practices."
difficulty: advanced
estimated_time: "95 min"
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
  - selinux
  - mac
  - hardening
  - rebash-linux-mastery
comments: false
status: ready
---

# SELinux Overview — Mandatory Access Control in Linux

> **SELinux (Security-Enhanced Linux)** is a Linux security framework that provides **Mandatory Access Control (MAC)**. Unlike traditional Linux permissions, which rely on file ownership and user permissions, SELinux applies security policies that determine what processes are allowed to access specific files, directories, ports, and system resources. Even if a process is running as the root user, SELinux can still restrict its actions according to the defined security policy. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, and Site Reliability Engineer (SRE) should understand SELinux to secure enterprise Linux systems.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 11: Linux Security → Lesson 4</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Advanced</div>

<div markdown>**Reading Time:** 95 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Linux Security</div>

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand SELinux fundamentals
- Learn Mandatory Access Control (MAC)
- Understand SELinux modes
- View and interpret security contexts
- Manage SELinux policies
- Use common SELinux commands
- Troubleshoot SELinux issues
- Apply SELinux best practices

---

# Prerequisites

Complete:

- Modules 1–10
- Module 11 Lessons 1–3

---

# Why Learn SELinux?

Imagine a web server running as the root user.

Without SELinux:

```text
Web Server

↓

Compromised

↓

Access Entire System
```

With SELinux:

```text
Web Server

↓

Compromised

↓

Restricted by SELinux Policy

↓

Limited Damage
```

SELinux reduces the impact of successful attacks.

---

# What is SELinux?

SELinux stands for:

```text
Security-Enhanced Linux
```

It is a security framework that enforces **Mandatory Access Control (MAC)**.

Instead of relying only on:

- User ownership
- File permissions

SELinux also evaluates:

- Security contexts
- Security policies
- Process permissions

---

# DAC vs MAC

Linux normally uses:

```text
DAC

↓

Discretionary Access Control
```

Users control access through:

- Owner
- Group
- Permissions

SELinux introduces:

```text
MAC

↓

Mandatory Access Control
```

System policies decide whether access is allowed.

Even the root user must follow SELinux policies.

---

# How SELinux Works

Every object has a security context.

Example:

```text
Process

↓

SELinux Policy

↓

File

↓

Allow or Deny
```

Both traditional Linux permissions and SELinux policies must allow access.

---

# SELinux Modes

SELinux has three operating modes.

| Mode | Description |
|-------|-------------|
| Enforcing | Policies are enforced |
| Permissive | Violations are logged but not blocked |
| Disabled | SELinux is disabled |

---

# Check SELinux Status

```bash
getenforce
```

Example:

```text
Enforcing
```

Detailed information:

```bash
sestatus
```

Example output:

```text
SELinux status: enabled

Current mode: enforcing
```

---

# Change SELinux Mode

Temporarily switch to permissive mode.

```bash
sudo setenforce 0
```

Return to enforcing mode.

```bash
sudo setenforce 1
```

These changes are temporary and last until the next reboot.

---

# Persistent Configuration

Configuration file:

```text
/etc/selinux/config
```

Example:

```text
SELINUX=enforcing
```

Possible values:

```text
enforcing

permissive

disabled
```

Reboot the system after changing the configuration file.

---

# Security Contexts

Display SELinux contexts.

```bash
ls -Z
```

Example:

```text
-rw-r--r-- root root system_u:object_r:httpd_sys_content_t:s0 index.html
```

---

# Understanding Security Context

Example:

```text
system_u

object_r

httpd_sys_content_t

s0
```

Components:

| Component | Description |
|-----------|-------------|
| User | SELinux user |
| Role | SELinux role |
| Type | Security type |
| Level | Security level |

The **type** is the most commonly used component in policy enforcement.

---

# View Process Contexts

```bash
ps -eZ
```

Example:

```text
system_u:system_r:httpd_t:s0
```

---

# Common SELinux Commands

Check status.

```bash
getenforce
```

Detailed status.

```bash
sestatus
```

Display file contexts.

```bash
ls -Z
```

Display process contexts.

```bash
ps -eZ
```

---

# Restore Default Contexts

Restore the default SELinux context.

```bash
restorecon -Rv /var/www/html
```

Useful after moving or copying files.

---

# Change File Context

Assign a new context.

```bash
sudo chcon -t httpd_sys_content_t index.html
```

!!! note "Note"

    `chcon` changes are temporary and may be lost after a relabel. For permanent changes, use `semanage fcontext` followed by `restorecon`.

---

# Managing Ports

View allowed ports.

```bash
semanage port -l
```

Example:

```text
http_port_t
```

---

# Viewing SELinux Booleans

List booleans.

```bash
getsebool -a
```

Example:

```text
httpd_can_network_connect
```

Enable a boolean permanently.

```bash
sudo setsebool -P httpd_can_network_connect on
```

---

# Common Commands

Check mode.

```bash
getenforce
```

View status.

```bash
sestatus
```

View contexts.

```bash
ls -Z
```

Restore contexts.

```bash
restorecon -Rv /var/www/html
```

Change mode.

```bash
setenforce 0
```

---

# Real Production Examples

Check SELinux status.

```bash
getenforce
```

Restore web content.

```bash
restorecon -Rv /var/www/html
```

View process contexts.

```bash
ps -eZ
```

Enable HTTP network access.

```bash
setsebool -P httpd_can_network_connect on
```

---

# Production Perspective

SELinux is widely used in:

- Red Hat Enterprise Linux
- Rocky Linux
- AlmaLinux
- Oracle Linux
- Enterprise web servers
- Database servers
- Kubernetes worker nodes
- Government and regulated environments

Many security standards recommend keeping SELinux enabled in enforcing mode.

---

# Hands-on Lab

## Task 1

Check SELinux mode.

```bash
getenforce
```

---

## Task 2

Display SELinux status.

```bash
sestatus
```

---

## Task 3

View file contexts.

```bash
ls -Z
```

---

## Task 4

View process contexts.

```bash
ps -eZ
```

---

## Task 5

Switch to permissive mode.

```bash
sudo setenforce 0
```

---

## Task 6

Return to enforcing mode.

```bash
sudo setenforce 1
```

---

## Task 7

Restore file contexts.

```bash
sudo restorecon -Rv /var/www/html
```

---

## Task 8

Display available SELinux booleans.

```bash
getsebool -a
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `getenforce` | Display SELinux mode | System verification |
| `sestatus` | Show SELinux status | Troubleshooting |
| `ls -Z` | View file contexts | Security auditing |
| `ps -eZ` | View process contexts | Process analysis |
| `restorecon` | Restore contexts | File recovery |
| `setsebool` | Configure SELinux booleans | Application configuration |

---

# Common SELinux Mistakes

| Mistake | Solution |
|----------|----------|
| Disabling SELinux permanently | Keep it enabled whenever possible |
| Ignoring SELinux logs | Review audit logs to identify denials |
| Using `chcon` for permanent changes | Use `semanage fcontext` and `restorecon` |
| Switching to permissive mode permanently | Use only for troubleshooting |
| Changing file permissions instead of fixing SELinux contexts | Restore or assign the correct context |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A web server cannot access newly copied website files.

Linux permissions:

```text
Correct
```

Application still fails.

Investigation:

```bash
ls -Z /var/www/html
```

The files have incorrect SELinux contexts.

Solution:

```bash
sudo restorecon -Rv /var/www/html
```

The correct SELinux labels are restored, and the web server can access the files without changing Linux file permissions.

---

# Best Practices

- Keep SELinux in **Enforcing** mode in production.
- Use **Permissive** mode only for troubleshooting.
- Never disable SELinux unless absolutely necessary.
- Restore correct file contexts after moving files.
- Review SELinux denials using audit logs.
- Use `semanage` for permanent policy changes.
- Test policy changes in a non-production environment.

---

# Common Mistakes

❌ Disabling SELinux to bypass configuration issues.

✅ Avoid disabling SELinux to bypass configuration issues; fix the configuration instead.

---

❌ Ignoring SELinux denial messages.

✅ Always review SELinux denial messages.

---

❌ Using `chmod 777` instead of fixing SELinux contexts.

✅ Prefer fixing SELinux contexts rather than using `chmod 777`.

---

❌ Forgetting to restore file contexts after copying application files.

✅ Remember to to restore file contexts after copying application files.

---

❌ Leaving systems in permissive mode permanently.

✅ Do not leave systems in permissive mode permanently.

---

# Interview Questions
## Beginner

1. What is SELinux?
2. What is Mandatory Access Control (MAC)?
3. What are the three SELinux modes?
4. Which command displays the current SELinux mode?

---

## Intermediate

1. What is the difference between DAC and MAC?
2. What is a security context?
3. What does `restorecon` do?
4. Why should SELinux remain in enforcing mode?

---

## Architect Level

1. How would you deploy production web applications with SELinux enabled?
2. How would you troubleshoot an application blocked by SELinux?
3. Why is SELinux considered an important layer in defense-in-depth security?

---

# Summary

In this lesson, you learned:

- SELinux fundamentals
- Mandatory Access Control (MAC)
- SELinux operating modes
- Security contexts
- SELinux commands
- File context management
- SELinux booleans
- Production security best practices

SELinux provides an additional layer of security beyond traditional Linux file permissions by enforcing mandatory access control policies. When configured correctly, it limits what processes can do, helping to contain attacks and protect critical system resources.

---

## Key Takeaways

- SELinux implements Mandatory Access Control (MAC).
- Keep SELinux in **Enforcing** mode for production systems.
- Use `getenforce` and `sestatus` to verify SELinux status.
- Restore correct file contexts with `restorecon`.
- Use `semanage` for permanent SELinux policy changes.
- Treat SELinux as an important layer in a defense-in-depth security strategy.

---

## What's Next?

**[AppArmor — Application-Level Security in Linux](apparmor.md)**

You'll explore:

- What AppArmor is
- AppArmor profiles
- Enforce and Complain modes
- Managing profiles
- Common AppArmor commands
- Monitoring policy violations
- Production security best practices

By the end of the lesson, you'll understand how AppArmor confines applications using security profiles and how it complements Linux security by restricting application capabilities.
