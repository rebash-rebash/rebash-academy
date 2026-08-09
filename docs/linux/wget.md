---
title: "wget — Downloading Files from the Command Line"
description: "Use wget to download files on Linux — resume transfers, background downloads, mirror websites, authenticate, and automate reliable non-interactive downloads."
difficulty: intermediate
estimated_time: "65 min"
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
  - wget
  - downloads
  - automation
  - rebash-linux-mastery
comments: false
status: ready
---

# wget — Downloading Files from the Command Line

> **wget (Web Get)** is a powerful command-line utility used to download files from web servers using HTTP, HTTPS, and FTP. It is designed for reliable, non-interactive downloading, making it ideal for automation, scripts, software installation, backups, and mirroring websites. Linux administrators, DevOps engineers, Cloud Architects, and Site Reliability Engineers (SREs) frequently use `wget` to retrieve files and automate downloads.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 8: Networking → Lesson 10</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 65 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Networking</div>

<div markdown>**Lesson:** 10 of 13</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `wget` command
- Download files from the Internet
- Resume interrupted downloads
- Download files in the background
- Mirror websites
- Authenticate downloads
- Automate file downloads
- Troubleshoot download issues

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
- Module 8 Lessons 1–9

---

# Why Learn wget?

Imagine:

- Downloading an ISO image.
- Fetching application binaries.
- Downloading backup files.
- Mirroring a documentation website.
- Automating software installation.

`wget` is the preferred tool for these tasks because it is reliable and script-friendly.

---

# What is wget?

`wget` stands for:

```text
Web Get
```

It is a non-interactive download utility that supports:

- HTTP
- HTTPS
- FTP

It is commonly used for:

- Downloading files
- Automation scripts
- Software installation
- Website mirroring
- Scheduled downloads

---

# How wget Works

```text
Client
   │
   ▼
HTTP Request
   │
   ▼
Web Server
   │
   ▼
File Download
   │
   ▼
Local System
```

---

# Basic Download

Download a file.

```bash
wget https://example.com/file.zip
```

The file is saved using its original filename.

---

# Save with a Different Name

```bash
wget -O backup.zip \
https://example.com/file.zip
```

---

# Resume an Interrupted Download

```bash
wget -c https://example.com/file.zip
```

The `-c` option resumes downloading from where it stopped.

---

# Download in the Background

```bash
wget -b https://example.com/file.zip
```

Check the log:

```bash
tail -f wget-log
```

---

# Limit Download Speed

```bash
wget --limit-rate=500k \
https://example.com/file.zip
```

Useful when sharing network bandwidth.

---

# Download Multiple Files

Create a file named `urls.txt`:

```text
https://example.com/file1.zip
https://example.com/file2.zip
https://example.com/file3.zip
```

Download all files.

```bash
wget -i urls.txt
```

---

# Mirror a Website

```bash
wget --mirror \
https://example.com
```

Commonly used for:

- Documentation
- Static websites
- Offline browsing

---

# Recursive Download

```bash
wget -r \
https://example.com/docs
```

Downloads linked content recursively.

---

# Download Without Parent Directories

```bash
wget -np -r \
https://example.com/docs
```

The `-np` option prevents ascending to parent directories.

---

# Download with Authentication

Basic Authentication:

```bash
wget \
--user=username \
--password=password \
https://example.com/file.zip
```

> Avoid placing passwords directly on the command line in shared or production environments because they may be visible in process listings.

---

# Ignore Certificate Validation

```bash
wget --no-check-certificate \
https://example.com
```

> **Warning:** Use this only for testing. It disables TLS certificate validation and should not be used in production.

---

# Continue Existing Downloads

If a file already exists:

```bash
wget -c \
https://example.com/file.iso
```

This prevents restarting large downloads from the beginning.

---

# Common Commands

Basic download.

```bash
wget https://example.com/file.zip
```

Resume download.

```bash
wget -c https://example.com/file.zip
```

Background download.

```bash
wget -b https://example.com/file.zip
```

Mirror website.

```bash
wget --mirror https://example.com
```

Download list of files.

```bash
wget -i urls.txt
```

---

# Real Production Examples

Download Kubernetes CLI.

```bash
wget https://dl.k8s.io/release/<version>/bin/linux/amd64/kubectl
```

Download Terraform.

```bash
wget https://releases.hashicorp.com/terraform/<version>/terraform_<version>_linux_amd64.zip
```

Download an application backup.

```bash
wget https://backup.example.com/db.sql.gz
```

Mirror documentation.

```bash
wget --mirror https://docs.example.com
```

---

# Production Perspective

`wget` is commonly used for:

- Software deployment
- CI/CD pipelines
- Backup retrieval
- Infrastructure automation
- Cloud provisioning
- Configuration downloads
- Offline documentation
- Scheduled maintenance

It is a reliable tool for unattended downloads in production environments.

---

# Hands-on Lab

## Task 1

Download a web page.

```bash
wget https://example.com
```

---

## Task 2

Save the file with a custom name.

```bash
wget -O homepage.html \
https://example.com
```

---

## Task 3

Resume a download.

```bash
wget -c \
https://example.com/file.zip
```

---

## Task 4

Download in the background.

```bash
wget -b \
https://example.com/file.zip
```

Monitor progress.

```bash
tail -f wget-log
```

---

## Task 5

Create a download list.

```text
https://example.com/file1.zip
https://example.com/file2.zip
```

Download all files.

```bash
wget -i urls.txt
```

---

## Task 6

Limit download speed.

```bash
wget --limit-rate=1m \
https://example.com/file.zip
```

---

## Task 7

Mirror a website.

```bash
wget --mirror \
https://example.com
```

---

## Task 8

Download recursively.

```bash
wget -r \
https://example.com/docs
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `wget URL` | Download file | Software installation |
| `wget -O` | Save with custom filename | Backup download |
| `wget -c` | Resume download | Large ISO files |
| `wget -b` | Background download | Automation |
| `wget -i` | Download file list | Batch downloads |
| `wget --mirror` | Mirror website | Documentation backup |
| `wget -r` | Recursive download | Static website retrieval |
| `wget --limit-rate` | Limit bandwidth | Shared networks |

---

# wget vs curl

| Feature | wget | curl |
|----------|------|------|
| Download Files | ✅ Excellent | ✅ |
| Resume Downloads | ✅ Excellent | Basic |
| Recursive Downloads | ✅ | ❌ |
| Website Mirroring | ✅ | ❌ |
| REST API Testing | Limited | ✅ Excellent |
| Multiple HTTP Methods | Limited | ✅ |

Use:

- **wget** for downloading files and websites.
- **curl** for APIs, HTTP requests, and web service testing.

---

# Common wget Errors

| Error | Possible Cause |
|--------|----------------|
| `Unable to resolve host` | DNS problem |
| `Connection refused` | Service unavailable |
| `404 Not Found` | File does not exist |
| `403 Forbidden` | Access denied |
| `SSL certificate error` | Certificate validation failed |
| `Connection timed out` | Network or firewall issue |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A CI/CD pipeline fails while downloading a deployment package.

Command:

```bash
wget https://repo.example.com/app.tar.gz
```

Error:

```text
Unable to resolve host
```

Investigation:

Verify DNS.

```bash
ping repo.example.com
```

Check DNS resolution.

```bash
getent hosts repo.example.com
```

After correcting the DNS configuration:

```bash
wget https://repo.example.com/app.tar.gz
```

The package downloads successfully, allowing the deployment to continue.

---

# Best Practices

- Use `-c` when downloading large files.
- Use `-O` to save files with meaningful names.
- Use `-b` for long-running downloads.
- Limit download speed when sharing bandwidth.
- Verify downloaded files using checksums when available.
- Avoid exposing credentials on the command line.
- Use HTTPS whenever possible.

---

# Common Mistakes

❌ Restarting large downloads instead of resuming them.

✅ Prefer resuming them rather than restarting large downloads.

---

❌ Downloading files without verifying their integrity.

✅ Avoid this mistake: downloading files without verifying their integrity.

---

❌ Using `--no-check-certificate` in production.

✅ Avoid using `--no-check-certificate` in production when a safer approach exists.

---

❌ Storing passwords directly in scripts.

✅ Avoid this mistake: storing passwords directly in scripts.

---

# Interview Questions
## Beginner

1. What is `wget` used for?
2. How do you resume an interrupted download?
3. Which option saves a file with a custom name?
4. How do you download files in the background?

---

## Intermediate

1. What is the difference between `wget` and `curl`?
2. How do you mirror a website?
3. How do you download multiple files using `wget`?
4. How do you limit download speed?

---

## Architect Level

1. How would you automate software downloads in a CI/CD pipeline?
2. Why is `wget` preferred for unattended downloads?
3. How would you securely download software packages in production?

---

# Summary

In this lesson, you learned:

- The `wget` command
- Downloading files
- Background downloads
- Resuming interrupted downloads
- Recursive downloads
- Website mirroring
- Authentication
- Production download automation

`wget` is one of the most reliable tools for downloading files in Linux. Its ability to resume downloads, work in the background, and automate file retrieval makes it indispensable for system administration, DevOps workflows, and infrastructure automation.

---

## Key Takeaways

- `wget` is optimized for downloading files.
- Use `-c` to resume interrupted downloads.
- Use `-O` to save files with custom names.
- Use `-b` for background downloads.
- Use `--mirror` to mirror websites.
- Use `wget` for unattended and automated download tasks.

---

## What's Next?

**[SSH (Secure Shell) — Secure Remote Access to Linux Systems](ssh-and-remote-access.md)**

You'll explore:

- Secure remote login
- SSH architecture
- SSH client and server
- Authentication methods
- SSH configuration
- Port forwarding
- Production security best practices

SSH is one of the most important tools for securely managing Linux systems remotely.
