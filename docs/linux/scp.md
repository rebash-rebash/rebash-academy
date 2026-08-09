---
title: "SCP (Secure Copy Protocol) — Secure File Transfer Between Linux Systems"
description: "Use SCP to securely copy files over SSH — recursive transfers, custom ports, key authentication, compression, and production file transfer practices."
difficulty: intermediate
estimated_time: "60 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 8 · Networking"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - networking
  - scp
  - ssh
  - file-transfer
  - rebash-linux-mastery
comments: false
status: ready
---

# SCP (Secure Copy Protocol) — Secure File Transfer Between Linux Systems

> **SCP (Secure Copy Protocol)** is a command-line utility used to securely transfer files and directories between Linux systems over an **SSH (Secure Shell)** connection. Since SCP uses SSH for authentication and encryption, all transferred data is protected during transmission. Linux administrators, DevOps engineers, Cloud Architects, Platform Engineers, and Site Reliability Engineers (SREs) use SCP to copy configuration files, application packages, backups, logs, and scripts between servers.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 8: Networking → Lesson 12</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 60 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Networking</div>

<div markdown>**Lesson:** 12 of 13</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand SCP
- Transfer files securely
- Copy directories recursively
- Use SSH keys with SCP
- Transfer files between remote systems
- Monitor file transfers
- Apply SCP in production environments

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
- Module 8 Lessons 1–11

---

# Why Learn SCP?

Imagine:

- Copying application packages to a production server.
- Uploading Kubernetes configuration files.
- Downloading log files for troubleshooting.
- Backing up configuration files.
- Deploying scripts to multiple Linux servers.

SCP provides a simple and secure method for transferring files.

---

# What is SCP?

SCP stands for:

```text
Secure Copy Protocol
```

It securely copies files between systems using SSH.

Advantages:

- Encrypted communication
- Simple syntax
- SSH authentication
- Cross-platform support
- Secure file transfers

---

# How SCP Works

```text
Source System
      │
Encrypted SSH Connection
      │
      ▼
Destination System
```

All transferred data is encrypted using SSH.

---

# Basic SCP Syntax

```bash
scp source destination
```

Example:

```bash
scp file.txt admin@192.168.1.100:/home/admin/
```

This copies `file.txt` to the remote server.

---

# Copy File to a Remote Server

```bash
scp report.pdf admin@server:/home/admin/
```

---

# Copy File from a Remote Server

```bash
scp admin@server:/home/admin/report.pdf .
```

The file is copied to the current local directory.

---

# Copy an Entire Directory

Use the recursive option:

```bash
scp -r project/ admin@server:/home/admin/
```

---

# Copy Using a Different SSH Port

If SSH runs on port **2222**:

```bash
scp -P 2222 file.txt admin@server:/tmp/
```

> **Note:** SCP uses an uppercase `-P` for the port option.

---

# Use an SSH Private Key

```bash
scp -i ~/.ssh/id_ed25519 \
file.txt admin@server:/tmp/
```

---

# Preserve File Attributes

Preserve:

- Permissions
- Timestamps
- Modification times

```bash
scp -p file.txt admin@server:/tmp/
```

---

# Enable Compression

Compress data during transfer.

```bash
scp -C largefile.iso admin@server:/backup/
```

Useful for slower network connections.

---

# Copy Between Two Remote Servers

```bash
scp admin@server1:/tmp/file.txt \
admin@server2:/tmp/
```

The local machine coordinates the transfer between the two remote systems.

---

# Display Transfer Progress

SCP displays progress by default.

Example:

```text
file.txt

100%

5 MB

2.5 MB/s
```

---

# Common Commands

Upload file.

```bash
scp file.txt admin@server:/tmp/
```

Download file.

```bash
scp admin@server:/tmp/file.txt .
```

Copy directory.

```bash
scp -r website/ admin@server:/var/www/
```

Use SSH key.

```bash
scp -i ~/.ssh/id_ed25519 file.txt admin@server:/tmp/
```

Use compression.

```bash
scp -C backup.tar.gz admin@server:/backup/
```

---

# Real Production Examples

Deploy an application.

```bash
scp app.jar admin@web01:/opt/apps/
```

Upload Kubernetes configuration.

```bash
scp kubeconfig admin@master:/home/admin/.kube/config
```

Download log files.

```bash
scp admin@server:/var/log/nginx/error.log .
```

Backup configuration.

```bash
scp /etc/nginx/nginx.conf \
admin@backup:/configs/
```

---

# Production Perspective

SCP is commonly used for:

- Application deployments
- Configuration backups
- Log collection
- Cloud server administration
- Kubernetes configuration
- Infrastructure automation
- Disaster recovery

Although SCP is simple and secure, **rsync** is often preferred for large or repeated transfers because it transfers only changed data.

---

# Hands-on Lab

## Task 1

Create a test file.

```bash
echo "Linux Mastery" > test.txt
```

---

## Task 2

Upload the file.

```bash
scp test.txt username@server:/tmp/
```

---

## Task 3

Download the file.

```bash
scp username@server:/tmp/test.txt .
```

---

## Task 4

Copy a directory.

```bash
scp -r project/ username@server:/tmp/
```

---

## Task 5

Transfer using an SSH key.

```bash
scp -i ~/.ssh/id_ed25519 test.txt \
username@server:/tmp/
```

---

## Task 6

Transfer using compression.

```bash
scp -C backup.tar.gz \
username@server:/backup/
```

---

## Task 7

Transfer using a custom SSH port.

```bash
scp -P 2222 test.txt \
username@server:/tmp/
```

---

## Task 8

Verify the copied file.

```bash
ssh username@server

ls -l /tmp/
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `scp file user@host:path` | Upload file | Application deployment |
| `scp user@host:file .` | Download file | Log collection |
| `scp -r` | Copy directory | Website deployment |
| `scp -P` | Use custom SSH port | Hardened servers |
| `scp -i` | Use SSH private key | Secure authentication |
| `scp -p` | Preserve timestamps and permissions | Configuration backup |
| `scp -C` | Compress transfer | Large file transfer |

---

# Common SCP Errors

| Error | Possible Cause |
|--------|----------------|
| `Permission denied` | Incorrect credentials or file permissions |
| `Connection refused` | SSH service unavailable |
| `No such file or directory` | Incorrect source or destination path |
| `Host key verification failed` | SSH host key mismatch |
| `Connection timed out` | Firewall or network issue |

---

# SCP vs FTP vs SFTP

| Feature | SCP | SFTP | FTP |
|----------|-----|------|-----|
| Encryption | ✅ | ✅ | ❌ |
| Uses SSH | ✅ | ✅ | ❌ |
| Interactive File Management | ❌ | ✅ | ✅ |
| Secure | ✅ | ✅ | ❌ |
| Production Ready | ✅ | ✅ | ❌ |

---

# SCP vs rsync

| Feature | SCP | rsync |
|----------|-----|--------|
| Simple File Copy | ✅ | ✅ |
| Incremental Transfer | ❌ | ✅ |
| Synchronization | ❌ | ✅ |
| Compression | ✅ | ✅ |
| Resume Interrupted Transfers | Limited | ✅ |
| Best For | One-time transfers | Repeated synchronization |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A DevOps engineer attempts to deploy an application.

```bash
scp app.jar admin@server:/opt/apps/
```

Error:

```text
Permission denied
```

Investigation:

Verify SSH access.

```bash
ssh admin@server
```

Check destination permissions.

```bash
ls -ld /opt/apps
```

The deployment directory is owned by another user.

Correct the ownership or permissions.

```bash
sudo chown admin:admin /opt/apps
```

Retry:

```bash
scp app.jar admin@server:/opt/apps/
```

The deployment completes successfully.

---

# Best Practices

- Use SSH key-based authentication.
- Verify destination paths before transferring files.
- Use compression (`-C`) for large transfers over slow networks.
- Preserve file attributes when copying configuration files.
- Use SCP for one-time transfers and `rsync` for recurring synchronization tasks.
- Verify transferred files after completion.

---

# Common Mistakes

❌ Forgetting to use uppercase `-P` for the SSH port.

✅ Remember to to use uppercase `-P` for the SSH port.

---

❌ Using password authentication instead of SSH keys.

✅ Prefer SSH keys rather than using password authentication.

---

❌ Copying files to incorrect directories.

✅ Avoid this mistake: copying files to incorrect directories.

---

❌ Assuming SCP can synchronize changed files like `rsync`.

✅ Verify SCP can synchronize changed files like `rsync` instead of assuming it.

---

# Interview Questions
## Beginner

1. What is SCP?
2. Which protocol does SCP use?
3. How do you copy a file to a remote server?
4. Which option copies directories recursively?

---

## Intermediate

1. What is the difference between SCP and SFTP?
2. Why is uppercase `-P` used for specifying the SSH port?
3. How do you transfer files using an SSH key?
4. What does the `-C` option do?

---

## Architect Level

1. How would you securely deploy application packages across production servers?
2. When would you choose SCP instead of `rsync`?
3. How would you automate secure file transfers in a CI/CD pipeline?

---

# Summary

In this lesson, you learned:

- SCP fundamentals
- Secure file transfers
- Directory transfers
- SSH key authentication
- Compression
- File preservation
- Production deployment techniques

SCP provides a secure and straightforward method for transferring files between Linux systems using SSH encryption. It is ideal for one-time file transfers, application deployments, backups, and administrative tasks across production environments.

---

## Key Takeaways

- SCP securely transfers files using SSH.
- Use `scp -r` to copy directories.
- Use `-P` for custom SSH ports.
- Use `-i` for SSH key authentication.
- Use `-C` to compress large transfers.
- Use SCP for simple transfers and `rsync` for efficient synchronization.

---

## What's Next?

**[rsync — Efficient File Synchronization and Backups in Linux](rsync.md)**

You'll explore:

- File synchronization
- Incremental transfers
- Archive mode
- Compression
- Backup automation
- Remote synchronization
- Production deployment strategies

By the end of the lesson, you'll understand why `rsync` is one of the most powerful tools for backups, deployments, and synchronizing data across Linux systems.
