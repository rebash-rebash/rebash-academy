---
title: "umask Command — Controlling Default File and Directory Permissions"
description: "Control default permissions with umask — calculate 022/027/077 results, set temporary and permanent masks, and harden production file creation."
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 4 · File Management and Permissions"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - umask
  - permissions
  - security
  - rebash-linux-mastery
comments: false
status: ready
---

# umask Command — Controlling Default File and Directory Permissions

> The `umask` (User File Creation Mask) command determines the **default permissions** assigned to newly created files and directories. Instead of adding permissions, `umask` removes permissions from the system defaults. Understanding `umask` is essential for Linux security, DevOps automation, cloud infrastructure, and production system administration.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 4: File Management and Permissions → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 45 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** File Management and Permissions</div>

<div markdown>**Lesson:** 6 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the purpose of `umask`
- View the current umask value
- Calculate default permissions
- Change the umask temporarily
- Configure permanent umask values
- Apply security best practices
- Troubleshoot permission-related issues

---

# Prerequisites

Complete:

- Module 1
- Module 2
- Module 3
- Module 4 Lessons 1–5

---

# Why Learn umask?

Imagine you're deploying an application.

A configuration file is created automatically.

Instead of:

```text
rw-------
```

it becomes:

```text
rw-rw-rw-
```

Now every user on the system can modify it.

This is a serious security risk.

The default permissions are controlled by **umask**.

---

# What is umask?

`umask` stands for:

> **User File Creation Mask**

It defines which permissions should **NOT** be assigned when creating new files and directories.

Important:

> **umask removes permissions—it does not grant permissions.**

---

# How Default Permissions Work

Linux starts with these defaults:

### Files

```text
666

rw-rw-rw-
```

Why not 777?

Regular files are **not executable by default** for security reasons.

---

### Directories

```text
777

rwxrwxrwx
```

Directories require execute permission for traversal.

---

# The Permission Formula

```text
Default Permission

        -

     umask

----------------

Final Permission
```

---

# Example: umask 022

Current mask:

```bash
umask
```

Output:

```text
0022
```

For files:

```text
666

-022

----

644
```

Result:

```text
rw-r--r--
```

For directories:

```text
777

-022

----

755
```

Result:

```text
rwxr-xr-x
```

---

# Example: umask 027

Files:

```text
666

-027

----

640
```

Directories:

```text
777

-027

----

750
```

---

# Example: umask 077

Files:

```text
666

-077

----

600
```

Directories:

```text
777

-077

----

700
```

This is commonly used for sensitive environments.

---

# Viewing Current umask

```bash
umask
```

Example:

```text
0022
```

Display symbolic format:

```bash
umask -S
```

Output:

```text
u=rwx,g=rx,o=rx
```

---

# Changing umask Temporarily

Set:

```bash
umask 027
```

Verify:

```bash
umask
```

Create a file:

```bash
touch test.txt
```

Check:

```bash
ls -l test.txt
```

Output:

```text
-rw-r-----
```

---

# Changing umask Permanently

User-specific:

```bash
~/.bashrc

~/.profile

~/.bash_profile
```

Example:

```bash
umask 027
```

Reload:

```bash
source ~/.bashrc
```

---

System-wide:

Depending on the Linux distribution:

```text
/etc/profile

/etc/bash.bashrc

/etc/login.defs
```

!!! note "Note"

    Always verify your distribution's documentation before changing system-wide defaults.

---

# Common umask Values

| umask | Files | Directories | Typical Use |
|--------|--------|-------------|-------------|
| 000 | 666 | 777 | Testing only |
| 002 | 664 | 775 | Team collaboration |
| 022 | 644 | 755 | Default on many Linux systems |
| 027 | 640 | 750 | Shared production environments |
| 077 | 600 | 700 | High-security systems |

---

# Demonstration

Current:

```bash
umask 022
```

Create:

```bash
touch file1

mkdir dir1
```

Check:

```bash
ls -ld file1 dir1
```

Output:

```text
-rw-r--r--

drwxr-xr-x
```

---

Change:

```bash
umask 077
```

Create:

```bash
touch secret.txt

mkdir secrets
```

Output:

```text
-rw-------

drwx------
```

---

# Understanding the Calculation

Example:

```text
Default File

666

umask

022

Final

644
```

Notice:

```text
6 = rw-

2 removes write permission

Result:

r--
```

Think of `umask` as **blocking permissions**, not assigning them.

---

# Common Commands

Display:

```bash
umask
```

Symbolic format:

```bash
umask -S
```

Set:

```bash
umask 027
```

Create a file:

```bash
touch file.txt
```

Verify:

```bash
ls -l file.txt
```

---

# Real Production Examples

Secure deployment.

```bash
umask 027
```

SSH key generation.

```bash
umask 077
```

Application configuration.

```bash
umask 027
```

Shared development environment.

```bash
umask 002
```

CI/CD runner.

```bash
umask 022
```

---

# Production Perspective

`umask` is commonly configured for:

- Linux servers
- Kubernetes worker nodes
- Docker containers
- Jenkins agents
- GitLab Runners
- Application deployments
- Shared development environments
- Security-hardened systems

A secure `umask` helps prevent accidental exposure of newly created files.

---

# Hands-on Lab

## Task 1

Display the current umask.

```bash
umask
```

---

## Task 2

Display symbolic format.

```bash
umask -S
```

---

## Task 3

Create a file.

```bash
touch file1
```

Inspect:

```bash
ls -l file1
```

---

## Task 4

Set:

```bash
umask 027
```

---

## Task 5

Create another file.

```bash
touch file2
```

Compare permissions.

---

## Task 6

Create a directory.

```bash
mkdir project
```

Check:

```bash
ls -ld project
```

---

## Task 7

Set:

```bash
umask 077
```

Create:

```bash
touch secret.txt
```

Inspect permissions.

---

## Task 8

Restore your previous umask.

```bash
umask 022
```

*(Or restore the value that was originally configured on your system.)*

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `umask` | Display current mask | Security audits |
| `umask -S` | Symbolic view | Learning & troubleshooting |
| `umask 027` | Restrict defaults | Production servers |
| `touch` | Create test files | Verification |
| `mkdir` | Create test directories | Permission testing |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A DevOps engineer discovers that newly created configuration files are world-readable.

Investigation:

```bash
umask

touch app.conf

ls -l app.conf
```

Output:

```text
-rw-r--r--
```

The application stores sensitive credentials.

Solution:

```bash
umask 077

touch app.conf
```

New permissions:

```text
-rw-------
```

Sensitive configuration files are now accessible only to the owner.

---

# Best Practices

- Use `022` for general-purpose Linux systems.
- Use `027` for production application servers.
- Use `077` for sensitive environments and secrets.
- Verify file permissions after changing the umask.
- Configure permanent umask values through appropriate shell initialization files when required.

---

# Common Mistakes

❌ Thinking `umask` adds permissions.

✅ It **removes** permissions from the default values.

---

❌ Expecting `umask` to change existing files.

✅ `umask` affects **only newly created** files and directories.

---

❌ Setting `000` on production servers.

✅ This can make newly created files writable by everyone, creating a significant security risk.

---

# Interview Questions
## Beginner

1. What is `umask`?
2. What are the default permissions for new files?
3. What are the default permissions for new directories?
4. How do you display the current umask?

---

## Intermediate

1. Calculate the resulting permissions for files and directories with `umask 027`.
2. Why are regular files created with a base permission of `666` instead of `777`?
3. How do you configure a persistent umask for your user?
4. Does changing the umask affect existing files?

---

## Architect Level

1. Which umask would you configure for a production application server, and why?
2. How does an incorrect umask create security risks?
3. How would you standardize umask settings across hundreds of Linux servers?

---

# Summary

In this lesson, you learned:

- What `umask` is
- How default permissions are calculated
- Viewing and modifying the umask
- Temporary vs permanent configuration
- Secure umask values
- Production security practices

`umask` is one of Linux's most important preventive security mechanisms. By controlling the default permissions of newly created files and directories, it helps protect sensitive data and supports secure system administration.

---

## Key Takeaways

- `umask` removes permissions from default values.
- Default file permissions start at `666`.
- Default directory permissions start at `777`.
- `umask 022` results in `644` for files and `755` for directories.
- `umask 077` is recommended for sensitive files and private environments.
- `umask` affects only newly created files and directories.

---

## What's Next?

**[Access Control Lists (ACL) in Linux — Fine-Grained File Permissions](acl.md)**

In the next lesson, you'll learn:

- What ACLs are and why they exist
- Viewing and modifying ACLs with `getfacl` and `setfacl`
- Default and recursive ACLs
- The ACL mask and the `+` indicator in `ls -l`
- Production troubleshooting for shared access
