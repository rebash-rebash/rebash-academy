---
title: "Linux File Permissions — Understanding Read, Write, and Execute"
description: "Read Linux permission strings and octal modes — User/Group/Others, rwx values, directory permissions, and production security patterns."
difficulty: intermediate
estimated_time: "50 min"
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
  - permissions
  - security
  - chmod
  - rebash-linux-mastery
comments: false
status: ready
---

# Linux File Permissions — Understanding Read, Write, and Execute

> Linux file permissions are one of the most important security features of the operating system. They determine **who can read, modify, or execute files and directories**. Every Linux administrator, DevOps engineer, Cloud Architect, and Security professional must understand permissions to secure systems, troubleshoot access issues, and manage production environments.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 4: File Management and Permissions → Lesson 4</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 50 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** File Management and Permissions</div>

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Linux permissions
- Read permission strings
- Understand User, Group, and Others
- Learn Read, Write, and Execute permissions
- Understand numeric (octal) permissions
- Verify permissions
- Understand directory permissions
- Troubleshoot permission issues

---

# Prerequisites

Complete:

- Module 1
- Module 2
- Module 3
- Module 4 Lessons 1–3

---

# Why Learn Permissions?

Imagine you're deploying a web application.

Suddenly users receive:

```text
Permission denied
```

Questions:

- Does the application have permission to read the file?
- Can the web server execute the script?
- Is the configuration file writable?
- Which user owns the file?

Almost every Linux administrator encounters permission-related issues daily.

---

# Viewing Permissions

Use:

```bash
ls -l
```

Example:

```text
-rwxr-xr-- 1 basha developers 1520 Jan 10 deploy.sh
```

The first part represents the permissions.

```text
-rwxr-xr--
```

Let's break it down.

---

# Permission Structure

```text
-rwxr-xr--
│││ │││ │││
│││ │││ │└── Others
│││ │││ └── Others
│││ ││└──── Others
│││ └────── Group
││└──────── Group
│└───────── Group
└────────── User
```

Or visually:

```text
-rwxr-xr--
 ↑   ↑   ↑
User Group Others
```

---

# File Type

The first character indicates the file type.

| Symbol | Meaning |
|---------|---------|
| `-` | Regular File |
| `d` | Directory |
| `l` | Symbolic Link |
| `c` | Character Device |
| `b` | Block Device |
| `p` | Named Pipe |
| `s` | Socket |

---

# The Three Permission Sets

Every file has permissions for:

1. User (Owner)
2. Group
3. Others

Example:

```text
-rwxr-xr--
```

```text
User   rwx

Group  r-x

Others r--
```

---

# Read Permission (r)

Symbol:

```text
r
```

Value:

```text
4
```

Allows:

- View file contents
- Open files
- Copy files

Example:

```bash
cat notes.txt
```

---

For directories:

Allows:

- List directory contents

Example:

```bash
ls Documents
```

---

# Write Permission (w)

Symbol:

```text
w
```

Value:

```text
2
```

Allows:

- Modify files
- Save changes
- Delete contents

Example:

```bash
echo "Linux" >> notes.txt
```

---

For directories:

Allows:

- Create files
- Delete files
- Rename files

---

# Execute Permission (x)

Symbol:

```text
x
```

Value:

```text
1
```

Allows:

Execute programs.

Example:

```bash
./backup.sh
```

Without execute permission:

```text
Permission denied
```

---

For directories:

Allows entering the directory.

```bash
cd projects
```

Without execute permission:

```text
Permission denied
```

---

# Permission Values

| Permission | Value |
|-------------|------:|
| Read | 4 |
| Write | 2 |
| Execute | 1 |

---

# Combining Permissions

| Symbol | Value |
|---------|------:|
| `---` | 0 |
| `--x` | 1 |
| `-w-` | 2 |
| `-wx` | 3 |
| `r--` | 4 |
| `r-x` | 5 |
| `rw-` | 6 |
| `rwx` | 7 |

---

# Understanding 755

```text
755
```

Means:

```text
User  7 = rwx

Group 5 = r-x

Others 5 = r-x
```

Equivalent:

```text
rwxr-xr-x
```

---

# Understanding 644

```text
644
```

Means:

```text
User  rw-

Group r--

Others r--
```

Equivalent:

```text
rw-r--r--
```

---

# Understanding 700

```text
700
```

Equivalent:

```text
rwx------
```

Only the owner has access.

---

# Common Permission Modes

| Numeric | Symbolic | Common Use |
|----------|----------|------------|
| 777 | `rwxrwxrwx` | Testing only (avoid in production) |
| 755 | `rwxr-xr-x` | Scripts and directories |
| 750 | `rwxr-x---` | Team collaboration |
| 700 | `rwx------` | Private files |
| 644 | `rw-r--r--` | Configuration and text files |
| 640 | `rw-r-----` | Sensitive configuration |
| 600 | `rw-------` | SSH keys, secrets |

---

# Directory Permissions

Directory permissions behave differently.

Suppose:

```text
drwxr-x---
```

Read (`r`):

- List directory contents

Write (`w`):

- Create
- Delete
- Rename files

Execute (`x`):

- Enter the directory
- Access files inside

---

# Viewing Permissions

```bash
ls -l

ls -ld directory
```

Display numeric mode.

```bash
stat file.txt
```

Example:

```text
Access: (0644/-rw-r--r--)
```

---

# Permission Examples

Executable script.

```text
-rwxr-xr-x
```

Configuration file.

```text
-rw-r--r--
```

SSH private key.

```text
-rw-------
```

Directory.

```text
drwxr-xr-x
```

---

# Real Production Examples

Application script.

```text
-rwxr-xr-x deploy.sh
```

NGINX configuration.

```text
-rw-r--r-- nginx.conf
```

SSH private key.

```text
-rw-------
id_rsa
```

Kubernetes kubeconfig.

```text
-rw-------
config
```

---

# Production Perspective

Permissions are critical for:

- Linux servers
- Web servers
- Kubernetes
- Docker
- SSH
- Cloud infrastructure
- Databases
- CI/CD pipelines

Incorrect permissions can lead to:

- Application failures
- Security vulnerabilities
- Unauthorized access
- Production outages

---

# Hands-on Lab

## Task 1

Create a file.

```bash
touch report.txt
```

---

## Task 2

Display permissions.

```bash
ls -l report.txt
```

---

## Task 3

Create a directory.

```bash
mkdir projects
```

---

## Task 4

View directory permissions.

```bash
ls -ld projects
```

---

## Task 5

Inspect file metadata.

```bash
stat report.txt
```

---

## Task 6

Create a shell script.

```bash
echo 'echo Hello Linux' > hello.sh
```

Display permissions.

```bash
ls -l hello.sh
```

---

## Task 7

Try executing the script.

```bash
./hello.sh
```

Observe the permission error (until execute permission is granted in the next lesson).

---

## Task 8

Compare permissions of:

```bash
ls -l /etc/passwd

ls -l ~/.ssh
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `ls -l` | View permissions | Daily administration |
| `ls -ld` | View directory permissions | Troubleshooting |
| `stat` | Detailed file metadata | Auditing |
| `file` | Identify file type | Verification |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A deployment script fails with:

```text
Permission denied
```

Investigation:

```bash
ls -l deploy.sh

stat deploy.sh

whoami
```

The script lacks execute permission.

This issue is commonly encountered during deployments, CI/CD runs, and script migrations.

---

# Best Practices

- Follow the **Principle of Least Privilege**.
- Avoid `777` permissions in production.
- Use `600` for private keys and secrets.
- Use `644` for configuration files.
- Regularly audit file permissions.
- Understand directory permissions before changing them.

---

# Common Mistakes

❌ Granting `777` permissions to solve every issue.

✅ This creates serious security risks.

---

❌ Forgetting that directory execute permission controls access.

✅ Without `x`, users cannot enter the directory even if they have read permission.

---

❌ Confusing file permissions with ownership.

✅ Permissions and ownership work together but are managed separately.

---

# Interview Questions
## Beginner

1. What are Linux file permissions?
2. What do `r`, `w`, and `x` represent?
3. What are the three permission classes?
4. What does `755` mean?

---

## Intermediate

1. Explain the difference between file and directory execute permissions.
2. Why is `644` commonly used for configuration files?
3. Why should private keys use `600`?
4. What information does `stat` provide?

---

## Architect Level

1. How would you secure sensitive configuration files on a production server?
2. Why is the Principle of Least Privilege important?
3. How would you audit permissions across thousands of servers?

---

# Summary

In this lesson, you learned:

- Linux permission structure
- User, Group, and Others
- Read, Write, and Execute permissions
- Numeric permission values
- Directory permissions
- Permission inspection
- Production security considerations

Linux permissions are one of the core security mechanisms of the operating system. A strong understanding of permissions helps you build secure systems, troubleshoot access problems, and manage production environments confidently.

---

## Key Takeaways

- Every file has permissions for User, Group, and Others.
- Read = 4, Write = 2, Execute = 1.
- `755` is common for executable scripts and directories.
- `644` is common for regular files.
- `600` is recommended for sensitive files such as SSH private keys.
- Avoid using `777` in production unless absolutely necessary.

---

## What's Next?

**[Linux File Ownership — Understanding Users, Groups, and File Ownership](ownership.md)**

In the next lesson, you'll learn:

- File owners and groups
- Viewing ownership with `ls`, `id`, and `stat`
- Changing ownership with `chown` and `chgrp`
- Recursive ownership changes
- Production ownership troubleshooting
