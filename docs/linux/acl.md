---
title: "Access Control Lists (ACL) in Linux — Fine-Grained File Permissions"
description: "Use Linux ACLs with getfacl and setfacl — grant named user and group access, set default and recursive ACLs, and troubleshoot enterprise shared directories."
difficulty: advanced
estimated_time: "55 min"
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
  - acl
  - permissions
  - setfacl
  - getfacl
  - security
  - rebash-linux-mastery
comments: false
status: ready
---

# Access Control Lists (ACL) in Linux — Fine-Grained File Permissions

> Traditional Linux permissions allow access control for **Owner**, **Group**, and **Others**. However, in many real-world scenarios, you need to grant permissions to **specific users or groups** without changing ownership or creating new groups. **Access Control Lists (ACLs)** provide this fine-grained permission management and are widely used in enterprise Linux environments.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 4: File Management and Permissions → Lesson 7</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Advanced</div>

<div markdown>**Reading Time:** 55 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** File Management and Permissions</div>

<div markdown>**Lesson:** 7 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Access Control Lists (ACLs)
- Configure user-specific permissions
- Configure group-specific permissions
- Set default ACLs
- View ACL entries
- Remove ACLs
- Troubleshoot ACL issues
- Apply ACLs in production environments

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Command Line Essentials
- Module 3 – Text Processing
- Module 4 Lessons 1–6

---

# Why Learn ACL?

Imagine a shared project directory.

```text
project/
```

Owner:

```text
alice
```

Group:

```text
developers
```

Now you need to give **Bob** read-only access without:

- Changing ownership
- Changing the group
- Giving everyone access

Traditional permissions cannot solve this.

ACLs can.

---

# What is ACL?

ACL stands for:

> **Access Control List**

ACL extends standard Linux permissions by allowing:

- Individual user permissions
- Individual group permissions
- Default permissions for new files

Think of ACL as an additional permission layer on top of the traditional Owner/Group/Others model.

---

# Traditional Permissions

```text
Owner

Group

Others
```

---

# ACL Permissions

```text
Owner

Group

Others

↓

Additional Users

Additional Groups

Default Permissions
```

---

# Verify ACL Support

Check filesystem mount options.

```bash
mount | grep acl
```

On most modern Linux distributions (such as Ubuntu, RHEL, Rocky Linux, AlmaLinux, Debian, and SUSE), ACL support is enabled by default for common filesystems like ext4 and XFS.

You can also verify by creating a test ACL.

---

# Required Commands

ACL management uses:

```bash
getfacl

setfacl
```

Check availability.

```bash
which getfacl

which setfacl
```

If missing:

Ubuntu/Debian:

```bash
sudo apt install acl
```

RHEL/Rocky/AlmaLinux:

```bash
sudo dnf install acl
```

---

# View ACL

Create a file.

```bash
touch report.txt
```

View ACL.

```bash
getfacl report.txt
```

Output:

```text
# file: report.txt

# owner: basha

# group: developers

user::rw-

group::r--

other::r--
```

Initially, ACL reflects the standard permissions.

---

# Grant Permission to a User

Give Bob read access.

```bash
setfacl -m u:bob:r report.txt
```

View:

```bash
getfacl report.txt
```

Output:

```text
user::rw-

user:bob:r--

group::r--

mask::r--

other::r--
```

Bob now has read permission even though he is neither the owner nor necessarily in the owning group.

---

# Grant Read/Write Access

```bash
setfacl -m u:bob:rw report.txt
```

---

# Grant Execute Permission

```bash
setfacl -m u:bob:rwx script.sh
```

---

# Grant Permissions to a Group

```bash
setfacl -m g:qa:r project.txt
```

---

# Remove an ACL Entry

Remove Bob's ACL.

```bash
setfacl -x u:bob report.txt
```

Verify:

```bash
getfacl report.txt
```

---

# Remove All ACL Entries

```bash
setfacl -b report.txt
```

This removes all extended ACL entries while leaving the standard permissions intact.

---

# Default ACLs

Suppose you have:

```text
shared/
```

Every new file should automatically grant access to Bob.

Set a default ACL.

```bash
setfacl -d -m u:bob:rwx shared/
```

Verify:

```bash
getfacl shared/
```

Output:

```text
default:user:bob:rwx
```

Now every new file created inside `shared/` inherits this ACL.

---

# Recursive ACL

Apply ACL to an entire directory tree.

```bash
setfacl -R -m g:developers:rwx project/
```

---

# Copy ACL

Save ACLs.

```bash
getfacl project > acl-backup.txt
```

Restore ACLs.

```bash
setfacl --restore=acl-backup.txt
```

Useful during migrations and backups.

---

# Understanding the ACL Mask

Example:

```text
mask::r--
```

The ACL mask defines the **maximum effective permissions** for:

- Named users
- Named groups
- The owning group

Even if an ACL grants `rwx`, the effective permissions cannot exceed the mask.

View effective permissions:

```bash
getfacl report.txt
```

Look for entries marked with:

```text
#effective:
```

---

# View ACL Indicator

Run:

```bash
ls -l
```

Example:

```text
-rw-rw-r--+
```

Notice:

```text
+
```

The plus sign indicates that extended ACL entries exist.

---

# Common ACL Commands

View ACL.

```bash
getfacl file.txt
```

Grant permission.

```bash
setfacl -m u:bob:rw file.txt
```

Remove user ACL.

```bash
setfacl -x u:bob file.txt
```

Remove all ACLs.

```bash
setfacl -b file.txt
```

Recursive ACL.

```bash
setfacl -R
```

Default ACL.

```bash
setfacl -d
```

---

# ACL vs Traditional Permissions

| Traditional Permissions | ACL |
|--------------------------|-----|
| Owner, Group, Others | Multiple users and groups |
| One group only | Multiple groups |
| Simple | Fine-grained |
| Limited | Flexible |
| Default Linux permissions | Enterprise environments |

---

# Real Production Examples

Shared development directory.

```bash
setfacl -m g:developers:rwx project/
```

Grant QA read access.

```bash
setfacl -m g:qa:r reports/
```

Grant Jenkins access.

```bash
setfacl -m u:jenkins:rwx build/
```

Grant backup service access.

```bash
setfacl -m u:backup:r backups/
```

---

# Production Perspective

ACLs are widely used in:

- Enterprise file servers
- NFS shares
- Samba shares
- CI/CD pipelines
- Shared development environments
- Application deployment directories
- Backup systems

ACLs provide flexibility without changing ownership or reorganizing groups.

---

# Hands-on Lab

## Task 1

Create a file.

```bash
touch project.txt
```

---

## Task 2

View ACL.

```bash
getfacl project.txt
```

---

## Task 3

Grant read access to another user (replace `bob` with an existing username on your system).

```bash
sudo setfacl -m u:bob:r project.txt
```

---

## Task 4

Verify.

```bash
getfacl project.txt
```

---

## Task 5

Remove the ACL entry.

```bash
sudo setfacl -x u:bob project.txt
```

---

## Task 6

Create a shared directory.

```bash
mkdir shared
```

---

## Task 7

Set a default ACL.

```bash
sudo setfacl -d -m u:bob:rwx shared
```

---

## Task 8

Check the ACL.

```bash
getfacl shared
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `getfacl` | View ACL | Security audits |
| `setfacl -m` | Add/modify ACL | Shared access |
| `setfacl -x` | Remove ACL entry | Cleanup |
| `setfacl -b` | Remove all ACLs | Reset permissions |
| `setfacl -R` | Recursive ACL | Deployment directories |
| `setfacl -d` | Default ACL | Shared workspaces |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A CI/CD pipeline fails because Jenkins cannot write to the deployment directory.

Investigation:

```bash
ls -l deploy/

getfacl deploy/

id jenkins
```

Permissions appear correct, but Jenkins is not the owner and is not in the owning group.

Solution:

```bash
sudo setfacl -m u:jenkins:rwx deploy/
```

The pipeline now has the required access without changing ownership or broadening permissions for other users.

---

# Best Practices

- Use ACLs only when traditional permissions are insufficient.
- Keep ACL configurations simple and well-documented.
- Review ACLs regularly during security audits.
- Use default ACLs for shared project directories.
- Back up ACLs before large migrations.

---

# Common Mistakes

❌ Forgetting to verify the ACL mask.

✅ The mask may reduce effective permissions.

---

❌ Assuming `chmod` preserves ACL behavior.

✅ Changing standard permissions with `chmod` can modify the ACL mask and affect effective permissions.

---

❌ Using ACLs where normal groups are sufficient.

✅ Prefer the simplest permission model that meets your requirements.

---

# Interview Questions
## Beginner

1. What is an ACL?
2. Why do ACLs exist?
3. Which command displays ACL entries?
4. Which command adds an ACL?

---

## Intermediate

1. Explain the difference between ACLs and traditional permissions.
2. What is a default ACL?
3. What is the ACL mask?
4. What does the `+` symbol in `ls -l` indicate?

---

## Architect Level

1. How would you design permissions for a shared development environment?
2. When would you choose ACLs over Linux groups?
3. How would you migrate ACLs between Linux servers while preserving permissions?

---

# Summary

In this lesson, you learned:

- What ACLs are
- Viewing ACLs
- Adding and removing ACL entries
- Default ACLs
- Recursive ACLs
- ACL masks
- Enterprise use cases
- Production troubleshooting

ACLs extend Linux's traditional permission model by allowing fine-grained access control for individual users and groups. They are a powerful feature for enterprise environments where standard ownership and permission models are not flexible enough.

---

## Key Takeaways

- ACLs provide fine-grained permissions beyond Owner, Group, and Others.
- Use `getfacl` to view ACL entries.
- Use `setfacl` to add, modify, or remove ACLs.
- Default ACLs are inherited by newly created files and directories.
- The `+` in `ls -l` indicates extended ACLs.
- Use ACLs when traditional permissions cannot meet your access control requirements.

---

## What's Next?

**[Linux File Attributes — Protecting Files Beyond Permissions](file-attributes.md)**

In the next lesson, you'll learn:

- Viewing and modifying attributes with `lsattr` and `chattr`
- Immutable (`+i`) and append-only (`+a`) protection
- Recursive attribute management
- Securing configs and logs in production
- Troubleshooting “Operation not permitted” as root
