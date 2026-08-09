---
title: "Disk Quotas — Controlling Storage Usage in Linux"
description: "Configure Linux disk quotas — soft and hard limits, user and group quotas, quotacheck, quotaon, edquota, and production storage policies."
difficulty: intermediate
estimated_time: "75 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 9 · Storage Management"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - storage
  - quotas
  - multi-user
  - capacity
  - rebash-linux-mastery
comments: false
status: ready
---

# Disk Quotas — Controlling Storage Usage in Linux

> **Disk Quotas** allow Linux administrators to control and limit the amount of disk space and the number of files (inodes) that users or groups can consume on a filesystem. Quotas help prevent a single user or application from exhausting available storage, ensuring fair resource allocation and maintaining system stability. Disk quotas are widely used on multi-user systems, universities, enterprise servers, shared hosting platforms, and cloud environments.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 9: Storage Management → Lesson 8</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 75 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Storage Management</div>

<div markdown>**Lesson:** 8 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand disk quotas
- Configure user and group quotas
- Learn soft and hard limits
- Enable quota support
- Monitor quota usage
- Manage quota violations
- Apply quota best practices in production

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management
- Module 5 – Users and Groups
- Module 6 – Process Management
- Module 7 – Package Management
- Module 8 – Networking
- Module 9 Lessons 1–7

---

# Why Learn Disk Quotas?

Imagine:

- One user fills an entire shared server with log files.
- A developer accidentally uploads hundreds of gigabytes of data.
- A web hosting customer consumes all available storage.
- A backup application generates excessive files.

Without quotas:

```text
One User

↓

Consumes All Disk Space

↓

Other Applications Fail
```

With quotas:

```text
User Reaches Limit

↓

Write Operation Denied

↓

System Continues Operating
```

---

# What are Disk Quotas?

Disk quotas allow administrators to limit:

- Disk space usage
- Number of files (inodes)

Quotas can be applied to:

- Individual users
- Groups

---

# Why Use Quotas?

Quotas help:

- Prevent storage exhaustion
- Ensure fair resource allocation
- Protect shared servers
- Improve storage management
- Reduce operational risks

---

# Types of Quotas

Linux supports:

- User Quotas
- Group Quotas

Example:

```text
Filesystem

↓

User Quotas

↓

Group Quotas
```

---

# Soft Limit

A **soft limit** is a warning threshold.

Example:

```text
Limit

100 GB

Current Usage

102 GB
```

The user can temporarily exceed the limit during the configured grace period.

---

# Hard Limit

A **hard limit** is an absolute maximum.

Example:

```text
Hard Limit

110 GB
```

Once reached:

```text
Write Operation

↓

Denied
```

---

# Grace Period

The grace period allows users to temporarily exceed the soft limit.

Example:

```text
Soft Limit

100 GB

↓

Grace Period

7 Days

↓

Hard Enforcement
```

After the grace period expires, the soft limit is enforced as if it were a hard limit until usage is reduced.

---

# Quota Workflow

```text
User Writes File

↓

Quota Check

↓

Below Limit

↓

File Created

OR

Hard Limit Reached

↓

Operation Denied
```

---

# Enable Quotas

Edit:

```text
/etc/fstab
```

Example:

```text
UUID=abcd-1234

/home

ext4

defaults,usrquota,grpquota

0

2
```

Options:

- `usrquota`
- `grpquota`

---

# Remount the Filesystem

```bash
sudo mount -o remount /home
```

---

# Create Quota Database

```bash
sudo quotacheck -cug /home
```

Options:

| Option | Meaning |
|---------|----------|
| `-c` | Create quota files |
| `-u` | User quotas |
| `-g` | Group quotas |

---

# Enable Quotas

```bash
sudo quotaon /home
```

Verify:

```bash
sudo quotaon -p /home
```

---

# Configure User Quota

```bash
sudo edquota username
```

Example:

```text
Soft

100000

Hard

120000
```

---

# Configure Group Quota

```bash
sudo edquota -g developers
```

---

# Copy Quotas

Copy quota settings from one user to another.

```bash
sudo edquota -p user1 user2
```

---

# View User Quota

```bash
quota -u username
```

---

# View Current User Quota

```bash
quota
```

---

# Display Quota Report

```bash
sudo repquota /home
```

Shows:

- Users
- Groups
- Space usage
- Soft limits
- Hard limits

---

# Disable Quotas

```bash
sudo quotaoff /home
```

---

# Common Commands

Create quota database.

```bash
quotacheck -cug /home
```

Enable quotas.

```bash
quotaon /home
```

Edit quotas.

```bash
edquota username
```

View quotas.

```bash
quota
```

Quota report.

```bash
repquota /home
```

---

# Real Production Examples

Set quota for a developer.

```bash
sudo edquota developer1
```

View quota usage.

```bash
quota -u developer1
```

Generate report.

```bash
sudo repquota /home
```

---

# Production Perspective

Disk quotas are commonly used for:

- Multi-user Linux servers
- University computer labs
- Shared hosting platforms
- Development servers
- Cloud virtual machines
- Enterprise storage
- Home directories
- Shared file servers

Quotas help prevent individual users from consuming excessive storage resources.

---

# Hands-on Lab

## Task 1

View mounted filesystems.

```bash
df -Th
```

---

## Task 2

Enable quota support in `/etc/fstab`.

---

## Task 3

Remount the filesystem.

```bash
sudo mount -o remount /home
```

---

## Task 4

Create quota files.

```bash
sudo quotacheck -cug /home
```

---

## Task 5

Enable quotas.

```bash
sudo quotaon /home
```

---

## Task 6

Configure a user quota.

```bash
sudo edquota student1
```

---

## Task 7

View quota usage.

```bash
quota -u student1
```

---

## Task 8

Generate a quota report.

```bash
sudo repquota /home
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `quotacheck` | Create quota database | Initial configuration |
| `quotaon` | Enable quotas | Production servers |
| `quotaoff` | Disable quotas | Maintenance |
| `edquota` | Configure quotas | User management |
| `quota` | View quota usage | User monitoring |
| `repquota` | Generate quota report | Capacity planning |

---

# Soft Limit vs Hard Limit

| Feature | Soft Limit | Hard Limit |
|----------|------------|------------|
| Warning Threshold | Yes | No |
| Temporary Exceeding Allowed | Yes | No |
| Grace Period | Yes | No |
| Absolute Maximum | No | Yes |

---

# Common Quota Errors

| Error | Possible Cause |
|--------|----------------|
| `Quota not enabled` | quotaon not executed |
| `No quota support` | Missing usrquota/grpquota mount options |
| `Permission denied` | Insufficient privileges |
| `Quota exceeded` | Hard limit reached |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A shared development server reports:

```text
No space left on device
```

Investigation:

```bash
df -h
```

The filesystem is full.

Generate a quota report.

```bash
sudo repquota /home
```

The report shows one developer consuming most of the available storage.

The administrator sets appropriate quotas.

```bash
sudo edquota developer1
```

Future storage growth is controlled, preventing one user from impacting others.

---

# Best Practices

- Enable quotas on shared filesystems.
- Configure both soft and hard limits.
- Monitor quota reports regularly.
- Use reasonable grace periods.
- Review quotas periodically as storage needs change.
- Educate users about storage limits.

---

# Common Mistakes

❌ Forgetting to enable quota support in `/etc/fstab`.

✅ Remember to to enable quota support in `/etc/fstab`.

---

❌ Creating quota files but not enabling quotas.

✅ Avoid this mistake: creating quota files but not enabling quotas.

---

❌ Setting hard limits too low for business needs.

✅ Avoid this mistake: setting hard limits too low for business needs.

---

❌ Ignoring quota reports until storage becomes full.

✅ Always review quota reports until storage becomes full.

---

❌ Applying quotas without communicating policies to users.

✅ Test before applying quotas without communicating policies to users.

---

# Interview Questions
## Beginner

1. What is a disk quota?
2. What is the difference between user and group quotas?
3. What is a soft limit?
4. What is a hard limit?

---

## Intermediate

1. How do you enable quotas on a filesystem?
2. What is the purpose of `quotacheck`?
3. How do you configure quotas for a user?
4. What does `repquota` display?

---

## Architect Level

1. How would you implement quotas on a shared enterprise file server?
2. How would you design storage policies for hundreds of developers?
3. How would you monitor quota usage across multiple Linux servers?

---

# Summary

In this lesson, you learned:

- Disk quota fundamentals
- User and group quotas
- Soft and hard limits
- Grace periods
- Enabling quotas
- Managing quota usage
- Production storage policies

Disk quotas are an essential storage management feature that helps administrators control disk usage, ensure fair resource allocation, and prevent storage exhaustion on multi-user Linux systems.

---

## Key Takeaways

- Disk quotas control storage usage for users and groups.
- Soft limits provide warnings and allow temporary overuse.
- Hard limits prevent further storage allocation.
- Enable quota support using `usrquota` and `grpquota`.
- Use `edquota` to configure limits.
- Monitor storage consumption regularly using `quota` and `repquota`.

---

## What's Next?

**[Backup Basics — Protecting Data in Linux](backup-basics.md)**

You'll explore:

- Why backups are essential
- Types of backups (Full, Incremental, and Differential)
- Backup strategies
- Local and remote backups
- Backup tools in Linux
- Backup verification
- Recovery fundamentals
- Backup best practices

By the end of the lesson, you'll understand how to design reliable backup strategies, create backups using common Linux tools, and ensure data can be restored quickly in the event of hardware failures, accidental deletions, or system disasters.
