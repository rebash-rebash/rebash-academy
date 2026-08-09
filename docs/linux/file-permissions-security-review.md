---
title: "File Permissions Review — Securing Files and Directories in Linux"
description: "Review Linux file permissions — ownership, chmod, chown, SUID/SGID/sticky bit, auditing insecure files, and production least-privilege practices."
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
  - permissions
  - chmod
  - hardening
  - rebash-linux-mastery
comments: false
status: ready
---

# File Permissions Review — Securing Files and Directories in Linux

> **File Permissions** are one of the most important security mechanisms in Linux. They determine who can read, write, or execute files and directories, preventing unauthorized access and protecting sensitive system resources. Incorrect permissions can expose confidential data, allow unauthorized modifications, or even lead to privilege escalation. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, and Site Reliability Engineer (SRE) must understand how to review, audit, and manage Linux file permissions effectively.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 11: Linux Security → Lesson 2</p>

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

<div markdown>**Lesson:** 2 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Review the Linux permission model
- Understand ownership and groups
- Interpret symbolic and numeric permissions
- Configure file permissions securely
- Understand special permissions
- Audit file permissions
- Identify insecure permissions
- Apply production security best practices

---

# Prerequisites

Complete:

- Modules 1–10
- Module 11 Lesson 1 – SSH Hardening

---

# Why Review File Permissions?

Imagine a configuration file containing database passwords.

Incorrect permissions:

```text
-rwxrwxrwx
```

Anyone can read or modify the file.

Secure permissions:

```text
-rw-------
```

Only the owner has access.

Proper permissions protect systems from unauthorized access and accidental changes.

---

# Linux Permission Model

Every file and directory has:

- Owner
- Group
- Others

Each category has its own permissions.

```text
Owner

↓

Group

↓

Others
```

---

# Viewing Permissions

Use:

```bash
ls -l
```

Example:

```text
-rwxr-xr--
```

---

# Understanding Permission Fields

Example:

```text
-rwxr-xr--
```

Breakdown:

```text
-

File Type

rwx

Owner

r-x

Group

r--

Others
```

---

# Permission Types

| Symbol | Meaning |
|----------|----------|
| `r` | Read |
| `w` | Write |
| `x` | Execute |
| `-` | Permission not granted |

---

# Read Permission

For files:

```text
Open and read contents
```

For directories:

```text
List directory contents
```

---

# Write Permission

For files:

```text
Modify file contents
```

For directories:

```text
Create, delete, or rename files
```

---

# Execute Permission

For files:

```text
Run executable files or scripts
```

For directories:

```text
Access directory contents
```

---

# Numeric Permissions

Each permission has a numeric value.

| Permission | Value |
|------------|-------|
| Read | 4 |
| Write | 2 |
| Execute | 1 |

Examples:

```text
7 = rwx

6 = rw-

5 = r-x

4 = r--

0 = ---
```

---

# Common Permission Values

| Permission | Numeric |
|------------|---------|
| rwxrwxrwx | 777 |
| rwxr-xr-x | 755 |
| rw-r--r-- | 644 |
| rw------- | 600 |
| rwxr----- | 740 |

---

# Changing Permissions

Use:

```bash
chmod
```

Example:

```bash
chmod 644 file.txt
```

Symbolic mode:

```bash
chmod u+x script.sh
```

---

# Changing Ownership

Use:

```bash
sudo chown user file.txt
```

Change owner and group.

```bash
sudo chown user:developers file.txt
```

---

# Changing Group

Use:

```bash
sudo chgrp developers file.txt
```

---

# Special Permissions

Linux supports three special permissions.

- SUID
- SGID
- Sticky Bit

---

# SUID

Numeric:

```text
4
```

Example:

```bash
chmod 4755 program
```

Displayed as:

```text
-rwsr-xr-x
```

The program runs with the permissions of its owner.

---

# SGID

Numeric:

```text
2
```

Example:

```bash
chmod 2755 shared
```

Displayed as:

```text
rwxr-sr-x
```

Files created inside a directory inherit the directory's group ownership.

---

# Sticky Bit

Numeric:

```text
1
```

Example:

```bash
chmod 1777 /shared
```

Displayed as:

```text
drwxrwxrwt
```

Users can delete only their own files within the directory.

Example:

```text
/tmp
```

---

# Finding World-Writable Files

Search:

```bash
find / -type f -perm -002
```

These files should be reviewed carefully.

---

# Finding SUID Files

```bash
find / -perm -4000
```

Review regularly.

---

# Finding SGID Files

```bash
find / -perm -2000
```

---

# Secure File Permissions

Examples:

Private SSH key:

```text
600
```

SSH directory:

```text
700
```

Shell script:

```text
750
```

Configuration file:

```text
640
```

---

# Common Commands

View permissions.

```bash
ls -l
```

Change permissions.

```bash
chmod 644 file.txt
```

Change owner.

```bash
chown user file.txt
```

Change group.

```bash
chgrp developers file.txt
```

Search SUID files.

```bash
find / -perm -4000
```

---

# Real Production Examples

Secure SSH key.

```bash
chmod 600 ~/.ssh/id_ed25519
```

Secure SSH directory.

```bash
chmod 700 ~/.ssh
```

Secure configuration.

```bash
chmod 640 app.conf
```

Assign ownership.

```bash
chown appuser:appgroup app.conf
```

---

# Production Perspective

Permission management is essential for:

- Linux servers
- Cloud virtual machines
- Kubernetes nodes
- Application servers
- Database servers
- Shared storage
- CI/CD environments
- Enterprise security compliance

Regular permission reviews reduce the risk of unauthorized access and privilege escalation.

---

# Hands-on Lab

## Task 1

View file permissions.

```bash
ls -l
```

---

## Task 2

Create a file.

```bash
touch test.txt
```

---

## Task 3

Assign secure permissions.

```bash
chmod 600 test.txt
```

---

## Task 4

Create an executable script.

```bash
chmod 755 script.sh
```

---

## Task 5

Change ownership.

```bash
sudo chown $USER test.txt
```

---

## Task 6

Search for SUID files.

```bash
find / -perm -4000
```

---

## Task 7

Search for world-writable files.

```bash
find / -type f -perm -002
```

---

## Task 8

Review the permissions of your `~/.ssh` directory.

```bash
ls -ld ~/.ssh

ls -l ~/.ssh
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `ls -l` | View permissions | Security auditing |
| `chmod` | Modify permissions | Access control |
| `chown` | Change ownership | User management |
| `chgrp` | Change group | Shared access |
| `find` | Locate insecure files | Security audits |
| `stat` | Display detailed file metadata | Permission verification |

---

# Common Permission Mistakes

| Mistake | Solution |
|----------|----------|
| Using `777` unnecessarily | Apply the principle of least privilege |
| Incorrect file ownership | Assign the correct owner and group |
| World-writable configuration files | Restrict permissions |
| Public SSH private keys | Set permissions to `600` |
| Ignoring SUID files | Audit them regularly |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A web application stores database credentials in a configuration file.

Permissions:

```text
-rw-rw-rw-
```

Any user can modify or read the file.

Secure configuration:

```bash
sudo chown appuser:appgroup app.conf

chmod 640 app.conf
```

Result:

- Only the application owner can modify the file.
- Group members can read it if necessary.
- Other users have no access.

---

# Best Practices

- Follow the principle of least privilege.
- Avoid `777` permissions unless absolutely necessary.
- Assign correct file ownership.
- Protect SSH keys with `600` permissions.
- Audit SUID and SGID files regularly.
- Remove unnecessary execute permissions.
- Review file permissions during security audits.

---

# Common Mistakes

❌ Assigning `777` permissions to application files.

✅ Avoid this mistake: assigning `777` permissions to application files.

---

❌ Leaving SSH private keys publicly readable.

✅ Do not leave SSH private keys publicly readable.

---

❌ Ignoring file ownership.

✅ Always review file ownership.

---

❌ Giving execute permission to non-executable files.

✅ Avoid this mistake: giving execute permission to non-executable files.

---

❌ Never reviewing permission changes.

✅ Always reviewing permission changes.

---

# Interview Questions
## Beginner

1. What do `r`, `w`, and `x` represent?
2. What does permission `755` mean?
3. Which command changes file permissions?
4. Which command changes file ownership?

---

## Intermediate

1. What is the difference between `chmod` and `chown`?
2. What are SUID, SGID, and the Sticky Bit?
3. Why should SSH private keys have `600` permissions?
4. How do you find world-writable files?

---

## Architect Level

1. How would you audit file permissions across hundreds of Linux servers?
2. How would you implement the principle of least privilege in an enterprise environment?
3. What file permission controls would you enforce for production applications?

---

# Summary

In this lesson, you learned:

- Linux permission model
- Ownership and groups
- Numeric and symbolic permissions
- Special permissions
- File ownership
- Permission auditing
- Secure permission practices
- Production security best practices

Proper file permissions are a fundamental layer of Linux security. Reviewing and maintaining correct ownership and permissions helps protect sensitive data, prevents unauthorized access, and reduces the risk of privilege escalation or accidental modifications.

---

## Key Takeaways

- Every Linux file has an owner, group, and permission set.
- Use the principle of least privilege.
- Avoid overly permissive settings such as `777`.
- Protect SSH keys and sensitive files with restrictive permissions.
- Audit SUID, SGID, and world-writable files regularly.
- Review permissions as part of routine security maintenance.

---

## What's Next?

**[Firewall (UFW) — Securing Linux Network Access](firewall-ufw.md)**

You'll explore:

- Firewall fundamentals
- Installing and enabling UFW
- Allowing and denying traffic
- Opening specific ports
- Managing application profiles
- Viewing firewall rules
- Production firewall best practices

By the end of the lesson, you'll be able to configure and manage UFW to secure Linux systems by controlling inbound and outbound network traffic.
