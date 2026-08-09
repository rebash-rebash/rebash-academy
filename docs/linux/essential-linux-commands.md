---
title: "File and Directory Commands"
description: "Files and directories are the building blocks of every Linux system. Master mkdir, touch, cp, mv, rm, and safe file management for Cloud and DevOps work."
difficulty: beginner
estimated_time: "25 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 2 · Linux Command Line Essentials"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - files
  - directories
  - command-line
  - rebash-linux-mastery
comments: false
status: ready
---

# File and Directory Commands

> Files and directories are the building blocks of every Linux system. Whether you're managing configuration files, application code, logs, or backups, mastering file and directory commands is an essential Linux skill.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 2: Linux Command Line Essentials → Lesson 4</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 25 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Linux Command Line Essentials</div>

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Create files and directories
- Copy files and folders
- Move and rename files
- Delete files safely
- Understand file overwrite behavior
- Work efficiently with multiple files
- Apply file management best practices

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Understanding the Shell
- Bash Basics
- Navigating the Filesystem

---

# Why Learn File Management?

Everything in Linux is stored as a file.

Examples include:

- Configuration files
- Application code
- Log files
- Shell scripts
- Databases
- Docker Compose files
- Kubernetes YAML manifests

As a Linux administrator, you'll manage thousands of files every day.

---

# Creating Directories

Create a new directory.

```bash
mkdir projects
```

Verify:

```bash
ls
```

Output:

```text
projects
```

---

# Create Multiple Directories

```bash
mkdir dev test production
```

---

# Create Nested Directories

Use the `-p` option.

```bash
mkdir -p projects/dev/app
```

Without `-p`, Linux reports an error if parent directories don't exist.

---

# Creating Files

Create an empty file.

```bash
touch notes.txt
```

Verify:

```bash
ls
```

Output:

```text
notes.txt
```

---

# Create Multiple Files

```bash
touch app.py config.yaml README.md
```

---

# Display File Details

```bash
ls -l
```

Example:

```text
-rw-r--r-- 1 basha users 0 Jul 12 notes.txt
```

---

# Copy Files

Syntax:

```bash
cp source destination
```

Example:

```bash
cp notes.txt backup.txt
```

Verify:

```bash
ls
```

---

# Copy Files to Another Directory

```bash
cp notes.txt /tmp
```

---

# Copy Multiple Files

```bash
cp file1 file2 file3 backup/
```

---

# Copy Directories

Use:

```bash
cp -r projects backup
```

The `-r` option copies directories recursively.

---

# Move Files

Syntax:

```bash
mv source destination
```

Example:

```bash
mv notes.txt Documents/
```

---

# Rename Files

Moving and renaming use the same command.

```bash
mv notes.txt linux-notes.txt
```

---

# Rename Directories

```bash
mv projects dev-projects
```

---

# Delete Files

Use:

```bash
rm notes.txt
```

The file is permanently deleted.

---

# Delete Multiple Files

```bash
rm file1 file2 file3
```

---

# Delete Directories

Empty directory:

```bash
rmdir test
```

---

# Delete Non-Empty Directories

```bash
rm -r projects
```

---

# Force Delete

```bash
rm -rf projects
```

!!! warning "Warning"

    `rm -rf` permanently deletes files and directories without asking for confirmation.

    Never use it unless you understand its impact.

---

# Interactive Delete

Prompt before deleting.

```bash
rm -i notes.txt
```

Output:

```text
remove regular file 'notes.txt'?
```

---

# Confirm Before Overwriting

```bash
cp -i file1 file2
```

If the destination exists:

```text
overwrite file2?
```

---

# Verbose Output

Display each operation.

Copy:

```bash
cp -v notes.txt backup.txt
```

Move:

```bash
mv -v backup.txt archive.txt
```

Delete:

```bash
rm -v archive.txt
```

---

# Wildcards

Delete all text files.

```bash
rm *.txt
```

Copy all YAML files.

```bash
cp *.yaml backup/
```

Move all log files.

```bash
mv *.log logs/
```

---

# Command Summary

| Command | Purpose |
|----------|----------|
| mkdir | Create directory |
| mkdir -p | Create nested directories |
| touch | Create empty file |
| cp | Copy files |
| cp -r | Copy directories |
| mv | Move or rename |
| rm | Delete file |
| rm -r | Delete directory |
| rm -rf | Force delete |
| rmdir | Delete empty directory |

---

# Visual Workflow

```text
Create

↓

Copy

↓

Move

↓

Rename

↓

Delete
```

---

# Real Production Example

Imagine you're deploying an NGINX configuration.

Create backup:

```bash
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
```

Edit configuration.

Verify.

Restart service.

If something goes wrong:

```bash
mv /etc/nginx/nginx.conf.bak /etc/nginx/nginx.conf
```

Restart NGINX.

This simple backup strategy prevents downtime.

---

# Production Perspective

Linux engineers constantly perform file operations.

Examples:

Copy configuration:

```bash
cp config.yaml config.yaml.bak
```

Move application:

```bash
mv app /opt/
```

Delete old logs:

```bash
rm old.log
```

Archive data:

```bash
cp -r project project-backup
```

These commands are used daily by:

- Linux Administrators
- Cloud Engineers
- DevOps Engineers
- Platform Engineers
- SREs

---

# Hands-on Lab

## Task 1

Create a lab directory.

```bash
mkdir linux-lab
```

---

## Task 2

Navigate into it.

```bash
cd linux-lab
```

---

## Task 3

Create three files.

```bash
touch notes.txt app.py config.yaml
```

---

## Task 4

Create directories.

```bash
mkdir logs backup
```

---

## Task 5

Copy notes.txt.

```bash
cp notes.txt backup/
```

---

## Task 6

Rename app.py.

```bash
mv app.py main.py
```

---

## Task 7

Move config.yaml.

```bash
mv config.yaml logs/
```

---

## Task 8

Delete notes.txt.

```bash
rm notes.txt
```

---

## Task 9

Display everything.

```bash
ls -R
```

---

# Mini Challenge

Create the following structure.

```text
linux-project

├── app

│   ├── app.py

│   └── config.yaml

├── logs

└── backup
```

Requirements:

- Create directories
- Create files
- Copy config.yaml to backup
- Rename app.py to server.py
- Delete an unused file

---

# Best Practices

- Create backups before modifying important files.
- Use `cp -i` to prevent accidental overwrites.
- Verify your current directory before deleting files.
- Avoid using `rm -rf` unless absolutely necessary.
- Use descriptive file names.

---

# Common Mistakes

❌ Running:

✅ Use:

```bash
rm -rf /
```

This is one of the most dangerous commands in Linux.

Never execute commands you don't fully understand.

---

❌ Forgetting `-r` while copying directories.

✅ Use:

```bash
cp project backup
```

Produces an error.

Correct:

```bash
cp -r project backup
```

---

❌ Using `rmdir` on non-empty directories.

✅ Use:

```bash
rm -r directory
```

instead.

---

# Interview Questions
## Beginner

1. Which command creates a directory?
2. Which command creates an empty file?
3. Difference between `cp` and `mv`?
4. What does `touch` do?
5. Which command deletes a directory?

---

## Intermediate

1. Difference between `rm` and `rmdir`?
2. What does `mkdir -p` do?
3. Explain recursive copy.
4. Why should you use `cp -i`?

---

## Architect Level

1. Why should configuration files always be backed up?
2. How would you safely replace production configuration files?
3. What precautions should engineers take before using `rm -rf`?

---

# Summary

In this lesson, you learned:

- Creating files
- Creating directories
- Copying files
- Moving files
- Renaming files
- Deleting files
- Recursive operations
- Safe file management practices

These commands are fundamental to Linux administration and are used daily in production environments.

---

## Key Takeaways

- `mkdir` creates directories.
- `touch` creates empty files.
- `cp` copies files and directories.
- `mv` moves and renames files.
- `rm` permanently deletes files.
- `rm -rf` is powerful and should be used with extreme caution.
- Always back up important files before modifying them.

---

## What's Next?

**[Viewing File Contents](viewing-file-contents.md)**

In the next lesson, you'll learn:

- `cat`
- `less`
- `more`
- `head`
- `tail`
- `nl`
- `tac`
- Viewing large log files efficiently
- Real-world log analysis
