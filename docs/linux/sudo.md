---
title: "sudo Command — Running Commands as Another User (Usually Root)"
description: "Use sudo for privileged Linux administration — compare sudo and su, run as another user, inspect privileges, and edit sudoers safely with visudo."
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 5 · Users and Groups"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - sudo
  - root
  - security
  - privilege
  - rebash-linux-mastery
comments: false
status: ready
---

# sudo Command — Running Commands as Another User (Usually Root)

> The `sudo` (**Superuser Do**) command allows authorized users to execute commands with elevated privileges without logging in as the root user. It is one of the most important security features in Linux and is widely used in enterprise environments, cloud platforms, DevOps pipelines, and system administration.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 5: Users and Groups → Lesson 3</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 50 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Users and Groups</div>

<div markdown>**Lesson:** 3 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the purpose of `sudo`
- Differentiate `sudo` and `su`
- Execute commands with elevated privileges
- Run commands as another user
- Understand the sudoers file
- Configure sudo access
- Troubleshoot sudo-related issues
- Apply sudo security best practices

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management and Permissions
- Module 5 Lessons 1–2

---

# Why Learn sudo?

Imagine you're managing a production Linux server.

You need to:

- Install software
- Restart services
- Create users
- Modify system files
- Update packages

Should you log in as:

```text
root
```

No.

Instead:

```bash
sudo command
```

This provides better security, accountability, and auditing.

---

# What is sudo?

`sudo` stands for:

> **Superuser Do**

It allows an authorized user to execute commands as:

- Root (default)
- Another user
- Another group

without logging in as that account.

---

# Why Use sudo?

Without sudo:

```text
Login as root

↓

Perform task

↓

Logout
```

With sudo:

```text
Login as normal user

↓

Run one privileged command

↓

Continue working normally
```

This minimizes the time spent with elevated privileges.

---

# Basic Syntax

```bash
sudo command
```

Example:

```bash
sudo apt update
```

or

```bash
sudo dnf update
```

---

# First-Time Authentication

The first sudo command prompts for **your own password**, not the root password.

Example:

```text
[sudo] password for basha:
```

After successful authentication, sudo remembers your credentials for a short period (the timeout is configurable).

---

# Common sudo Examples

Update packages.

```bash
sudo apt update
```

Install software.

```bash
sudo apt install nginx
```

Restart a service.

```bash
sudo systemctl restart nginx
```

Edit a system file.

```bash
sudo nano /etc/hosts
```

Create a user.

```bash
sudo useradd developer
```

---

# Check Current User

Without sudo.

```bash
whoami
```

Output:

```text
basha
```

Run as root.

```bash
sudo whoami
```

Output:

```text
root
```

---

# Run a Command as Another User

Syntax:

```bash
sudo -u username command
```

Example:

```bash
sudo -u nginx whoami
```

Output:

```text
nginx
```

*(Replace `nginx` with an existing user on your system if necessary.)*

---

# Open a Root Shell

Using sudo.

```bash
sudo -i
```

or

```bash
sudo -s
```

Exit:

```bash
exit
```

Use these only when multiple administrative commands are required.

---

# sudo vs su

| sudo | su |
|------|----|
| Executes a single command | Switches to another user |
| Uses your password | Usually requires the target user's password (often the root password) |
| Logs commands | Limited auditing |
| More secure | Higher risk if used carelessly |
| Preferred for administration | Used when a full user session is required |

---

# View Your sudo Privileges

```bash
sudo -l
```

Example:

```text
User basha may run the following commands...
```

---

# The sudoers File

Configuration file:

```text
/etc/sudoers
```

Never edit it directly with a normal editor.

Instead use:

```bash
sudo visudo
```

`visudo` checks the syntax before saving to help prevent configuration errors.

---

# Example sudoers Entry

```text
basha ALL=(ALL:ALL) ALL
```

Meaning:

- User: `basha`
- On all hosts
- May run commands as any user and group
- Can execute any command

---

# Administrative Groups

Many Linux distributions grant sudo access through a group.

Examples:

Ubuntu/Debian:

```text
sudo
```

RHEL/Rocky/AlmaLinux:

```text
wheel
```

Check your membership.

```bash
groups
```

---

# sudo Authentication Timeout

By default, sudo caches authentication for a limited time.

Re-authenticate immediately.

```bash
sudo -k
```

Invalidate cached credentials completely.

```bash
sudo -K
```

---

# Common sudo Commands

Run as root.

```bash
sudo command
```

Run as another user.

```bash
sudo -u user command
```

Root shell.

```bash
sudo -i
```

List permissions.

```bash
sudo -l
```

Edit sudoers.

```bash
sudo visudo
```

---

# Real Production Examples

Restart NGINX.

```bash
sudo systemctl restart nginx
```

Restart Docker.

```bash
sudo systemctl restart docker
```

View system logs.

```bash
sudo journalctl -xe
```

Edit SSH configuration.

```bash
sudo nano /etc/ssh/sshd_config
```

Create a deployment directory.

```bash
sudo mkdir /opt/app
```

---

# Production Perspective

`sudo` is used daily for:

- System updates
- User management
- Service administration
- Software installation
- Security hardening
- Kubernetes node administration
- Docker administration
- Cloud VM management

It is the standard method for performing privileged tasks while maintaining accountability.

---

# Hands-on Lab

## Task 1

Display your current user.

```bash
whoami
```

---

## Task 2

Run the same command with sudo.

```bash
sudo whoami
```

---

## Task 3

View your sudo permissions.

```bash
sudo -l
```

---

## Task 4

Display your groups.

```bash
groups
```

---

## Task 5

Open a root shell.

```bash
sudo -i
```

Verify:

```bash
whoami
```

Exit:

```bash
exit
```

---

## Task 6

Invalidate cached sudo credentials.

```bash
sudo -k
```

Run another sudo command to observe the password prompt again.

---

## Task 7

View the sudoers file safely.

```bash
sudo visudo
```

Exit without making changes.

---

## Task 8

Run a command as another user (replace `nobody` with an available account if necessary).

```bash
sudo -u nobody whoami
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `sudo` | Run a privileged command | Daily administration |
| `sudo -i` | Root login shell | Maintenance |
| `sudo -s` | Root shell | Troubleshooting |
| `sudo -u` | Run as another user | Testing |
| `sudo -l` | View sudo privileges | Auditing |
| `sudo -k` | Forget cached credentials | Security |
| `visudo` | Safely edit sudoers | Administration |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A DevOps engineer cannot restart a service.

Error:

```text
user is not in the sudoers file
```

Investigation:

```bash
groups

sudo -l
```

The user is not a member of the administrative group.

An administrator grants the appropriate sudo access using the organization's standard process.

After re-authenticating (or starting a new login session if group membership changed), the engineer can successfully manage the service.

---

# Best Practices

- Use `sudo` instead of logging in as `root`.
- Grant only the minimum privileges required.
- Edit the sudoers file only with `visudo`.
- Use administrative groups to manage sudo access.
- Review sudo permissions regularly.
- Use `sudo -i` only when a full root shell is genuinely needed.

---

# Common Mistakes

❌ Logging in directly as `root` for routine tasks.

✅ Use a regular user account with `sudo`.

---

❌ Editing `/etc/sudoers` with a normal text editor.

✅ Always use:

```bash
sudo visudo
```

---

❌ Granting unrestricted sudo access to every user.

✅ Apply the Principle of Least Privilege.

---

# Interview Questions
## Beginner

1. What does `sudo` stand for?
2. Why is `sudo` preferred over logging in as `root`?
3. Which password does `sudo` request?
4. How do you view your sudo privileges?

---

## Intermediate

1. Explain the difference between `sudo` and `su`.
2. What is the purpose of `visudo`?
3. How do you run a command as another user?
4. What does `sudo -k` do?

---

## Architect Level

1. How would you securely manage administrative access across hundreds of Linux servers?
2. Why is command auditing important for privileged operations?
3. How would you design role-based sudo access for DevOps, DBAs, and Security teams?

---

# Summary

In this lesson, you learned:

- What `sudo` is
- Why `sudo` is preferred over direct root logins
- Running commands with elevated privileges
- Running commands as another user
- Viewing sudo permissions
- Understanding the `sudoers` file
- Using `visudo` safely
- Security best practices for administrative access

The `sudo` command is one of the most important security features in Linux. It enables controlled administrative access while maintaining accountability through command logging and minimizing the risks associated with working directly as the `root` user.

---

## Key Takeaways

- `sudo` stands for **Superuser Do**.
- Use `sudo` instead of logging in as the `root` user.
- `sudo` authenticates using your own password.
- Use `sudo -u` to run commands as another user.
- Use `sudo -l` to view your sudo privileges.
- Always edit the `sudoers` file using `visudo`.
- Follow the **Principle of Least Privilege** when granting administrative access.

---

## What's Next?

**[Linux Password Policies — Securing User Authentication](password-policies.md)**

You'll explore:

- Password authentication
- Password aging
- Password expiration
- Password complexity requirements
- Account locking and unlocking
- Password security best practices
- Enterprise compliance and security standards

Understanding password policies is essential for securing Linux systems and enforcing strong authentication practices in enterprise environments.
