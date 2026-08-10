---
title: "Linux wget Command"
description: "Learn Linux wget — download files, resume transfers, mirror websites, run recursive and background downloads, and automate software retrieval."
difficulty: beginner
estimated_time: "130 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 9 · Linux Networking"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - linux
  - wget
  - downloads
  - rebash-networking-mastery
comments: false
status: ready
---

# Linux `wget` Command — Downloading Files and Automating File Retrieval

> **`wget` (World Wide Web Get)** is a command-line utility used to **download files from web servers** using protocols such as **HTTP, HTTPS, and FTP**. It is designed for reliable, non-interactive downloads and supports features such as **resume downloads, recursive downloads, website mirroring, background downloads, authentication, bandwidth limiting, and automation**. `wget` is widely used by Linux administrators, DevOps engineers, Cloud Architects, Platform Engineers, Site Reliability Engineers (SRE), and System Engineers for downloading software, backups, configuration files, datasets, and application artifacts.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 9: Linux Networking → Lesson 9</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 130 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Linux Networking</div>

<div markdown>**Lesson:** 9 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `wget` command
- Download files from the Internet
- Resume interrupted downloads
- Mirror websites
- Perform recursive downloads
- Download files in the background
- Automate software downloads

---

# Prerequisites

Complete:

- [Linux `ip` Command](linux-networking-toolkit.md)
- [Linux `ss` Command](ss.md)
- [Linux `netstat` Command](netstat.md)
- [Linux `tcpdump` Command](packet-analysis-tcpdump-wireshark.md)
- [Linux `traceroute` Command](traceroute.md)
- [Linux `dig` Command](dig.md)
- [Linux `nslookup` Command](nslookup.md)
- [Linux `curl` Command](curl.md)

Basic understanding of:

- HTTP
- HTTPS
- URLs
- Linux File System

---

# Why Learn `wget`?

Imagine you need to:

- Download an ISO image
- Download Kubernetes binaries
- Download Terraform
- Retrieve backup files
- Download logs
- Mirror documentation

Instead of opening a browser, Linux engineers use:

```bash
wget
```

because it supports:

- Automation
- Resume Downloads
- Background Downloads
- Recursive Downloads

---

# What is `wget`?

`wget` stands for:

```text
World Wide Web Get
```

It retrieves files from remote servers.

Supported protocols include:

- HTTP
- HTTPS
- FTP

Unlike `curl`, `wget` is primarily designed for downloading files.

---

# Basic Syntax

```bash
wget URL
```

Example:

```bash
wget https://example.com/file.txt
```

The file is downloaded into the current directory.

---

# Download a File

```bash
wget https://example.com/file.txt
```

Output:

```text
Saving to:

file.txt
```

---

# Save with a Different Filename

```bash
wget -O report.txt \
https://example.com/file.txt
```

---

# Resume Interrupted Download

```bash
wget -c \
https://example.com/file.iso
```

This continues downloading from where it stopped.

Useful for:

- Large ISO Files
- VM Images
- Backups

---

# Download in Background

```bash
wget -b \
https://example.com/file.iso
```

The download continues even after you close the terminal session (subject to system conditions).

Log file:

```text
wget-log
```

---

# Limit Download Speed

```bash
wget --limit-rate=500k \
https://example.com/file.iso
```

Useful to reduce bandwidth consumption.

---

# Retry Failed Downloads

```bash
wget --tries=10 \
https://example.com/file.iso
```

Retries ten times before giving up.

---

# Set Download Timeout

```bash
wget --timeout=20 \
https://example.com/file.iso
```

Stops waiting after twenty seconds.

---

# Download Multiple Files

Create:

```text
files.txt
```

Contents:

```text
https://example.com/file1.txt

https://example.com/file2.txt
```

Download:

```bash
wget -i files.txt
```

---

# Recursive Download

```bash
wget -r \
https://example.com/docs/
```

Downloads linked files recursively.

---

# Mirror a Website

```bash
wget -m \
https://example.com
```

Mirror mode enables options suitable for creating a local copy of a website.

Useful for:

- Documentation
- Static Websites
- Offline Viewing

---

# Download Only Specific File Types

Example:

```bash
wget -r -A pdf \
https://example.com
```

Downloads only PDF files.

---

# Reject File Types

Example:

```bash
wget -r -R jpg,png \
https://example.com
```

Skips image files.

---

# Continue Recursive Download

```bash
wget -c -r \
https://example.com
```

---

# Download Using Authentication

Basic authentication.

```bash
wget \
--user=username \
--password=password \
https://example.com
```

---

# Ignore TLS Certificate Validation

```bash
wget --no-check-certificate \
https://example.com
```

> **Warning:** Use this option only in trusted testing environments. Avoid disabling certificate validation in production.

---

# Download via FTP

```bash
wget ftp://ftp.example.com/file.txt
```

---

# Enterprise Example

Download application package.

```bash
wget \
https://downloads.company.com/app.tar.gz
```

Verify checksum.

Extract.

Deploy.

---

# Cloud Perspective

Cloud engineers use `wget` to download:

- CLI Tools
- Terraform
- Kubernetes Binaries
- Backup Files
- Deployment Packages
- Cloud Agent Software

---

# Kubernetes Perspective

Common downloads include:

```bash
wget https://dl.k8s.io/release/.../kubectl
```

Other examples:

- Helm
- Container Network Interface (CNI) Plugins
- YAML Files
- Operators
- Container Runtime Packages

---

# Linux Perspective

Download file.

```bash
wget https://example.com/file.txt
```

Resume download.

```bash
wget -c https://example.com/file.iso
```

Mirror website.

```bash
wget -m https://example.com
```

Download in background.

```bash
wget -b https://example.com/file.iso
```

---

# Common wget Options

| Option | Purpose |
|----------|----------|
| `-O` | Save with custom filename |
| `-c` | Resume download |
| `-b` | Background download |
| `-i` | Read URLs from file |
| `-r` | Recursive download |
| `-m` | Mirror website |
| `--limit-rate` | Limit bandwidth |
| `--tries` | Retry failed downloads |
| `--timeout` | Set timeout |
| `--user` | Username |
| `--password` | Password |

---

# Hands-on Lab

## Task 1

Download a file.

```bash
wget https://example.com/file.txt
```

---

## Task 2

Save using another filename.

```bash
wget -O sample.txt \
https://example.com/file.txt
```

---

## Task 3

Resume a download.

```bash
wget -c \
https://example.com/file.iso
```

---

## Task 4

Download in background.

```bash
wget -b \
https://example.com/file.iso
```

---

## Task 5

Download multiple files.

```bash
wget -i files.txt
```

---

## Task 6

Mirror a website.

```bash
wget -m \
https://example.com
```

---

## Task 7

Download only PDF documents from a documentation site.

```bash
wget -r -A pdf \
https://example.com/docs/
```

---

## Task 8

Compare downloading a large file using:

- `wget`
- `curl`

Identify which tool is more appropriate for different use cases.

---

# Production Troubleshooting

Problem:

```text
Large Download

Keeps

Failing
```

Solution:

```bash
wget -c \
--tries=20 \
--timeout=30 \
https://example.com/file.iso
```

This:

- Resumes interrupted downloads
- Retries failures
- Uses a longer timeout

Ideal for unstable network connections.

---

# wget vs curl

| wget | curl |
|------|------|
| Optimized for Downloads | Optimized for Data Transfer |
| Resume Downloads | API Testing |
| Website Mirroring | REST API Requests |
| Recursive Downloads | Custom HTTP Methods |
| Background Downloads | Debugging HTTP Traffic |

---

# Common Mistakes

❌ Restarting large downloads after interruption.

✅ Use `-c` to resume.

---

❌ Ignoring checksum verification.

✅ Verify downloaded files before deployment.

---

❌ Disabling certificate validation unnecessarily.

✅ Keep Transport Layer Security (TLS) verification enabled in production.

---

❌ Using `wget` for complex API testing.

✅ Use `curl` for API interactions.

---

❌ Running recursive downloads without limits.

✅ Restrict recursion depth and file types.

---

# Best Practices

- Resume interrupted downloads using `-c`.
- Verify checksums for downloaded software.
- Use HTTPS whenever available.
- Mirror only websites you are authorised to copy.
- Limit recursive downloads to avoid unnecessary traffic.
- Store downloads in organised directories.
- Automate recurring downloads with scripts and schedulers.

---

# Interview Questions

## Beginner

1. What is `wget`?
2. How do you resume a download?
3. How do you save a file with a different name?
4. What does `wget -b` do?

---

## Intermediate

1. Compare `wget` and `curl`.
2. How do you mirror a website?
3. How do you limit download speed?
4. How do you download multiple files automatically?

---

## Architect Level

1. Design an automated software distribution workflow using `wget`.
2. Explain how you would securely download deployment artifacts in production.
3. How would you optimize large-scale file distribution across multiple Linux servers?

---

# Summary

In this lesson, you learned:

- The `wget` command
- File Downloads
- Resume Downloads
- Recursive Downloads
- Website Mirroring
- Background Downloads
- Authentication
- Enterprise File Distribution

`wget` is one of the most reliable file downloading tools available on Linux. It excels at downloading large files, resuming interrupted transfers, mirroring websites, and automating software retrieval. Mastering `wget` is essential for Linux system administration, DevOps automation, cloud deployments, and infrastructure management.

---

## Key Takeaways

- `wget` is optimized for **reliable file downloads**.
- Use **`-c`** to resume interrupted downloads.
- Use **`-O`** to save files with a custom filename.
- Use **`-r`** for recursive downloads and **`-m`** for website mirroring.
- `wget` is widely used for **software distribution, automation, and infrastructure provisioning**.
- Use `curl` for APIs and `wget` for downloading files and websites.

---

## What's Next?

**[Network Namespaces](network-namespaces.md)**

In the next lesson, you'll learn about **Network Namespaces**.

You'll explore:

- What Network Namespaces are
- Linux Network Isolation
- Virtual Network Interfaces
- veth Pairs
- Bridges
- Container Networking
- Kubernetes Networking Fundamentals

By the end of the lesson, you'll understand how Linux isolates networking between processes, how containers communicate, and how technologies like Docker and Kubernetes build virtual networks using network namespaces.
