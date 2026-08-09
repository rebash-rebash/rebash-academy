---
title: "Searching Files and Directories"
description: "Search Linux files and directories with find, locate, which, whereis, and type — by name, size, owner, permissions, and modification time."
difficulty: beginner
estimated_time: "30 min"
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
  - find
  - search
  - command-line
  - rebash-linux-mastery
comments: false
status: ready
---

# Searching Files and Directories

> Linux provides powerful tools to search for files, directories, commands, and executables. Whether you're locating configuration files, troubleshooting applications, or managing production servers, mastering file search commands is an essential Linux skill.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 2: Linux Command Line Essentials → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 30 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Linux Command Line Essentials</div>

<div markdown>**Lesson:** 6 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Search files and directories
- Search by name
- Search by type
- Search by size
- Search by owner
- Search by permissions
- Search by modification time
- Locate executables
- Search efficiently in production systems

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 Lessons 1–5

---

# Why Learn File Searching?

Imagine you're working on a production server.

You need to find:

- NGINX configuration
- Docker Compose file
- Kubernetes manifests
- SSH configuration
- Log files
- Recently modified files

Instead of manually browsing thousands of directories, Linux provides commands that can find them in seconds.

---

# Linux Search Commands

Linux offers several search utilities.

| Command | Purpose |
|----------|----------|
| find | Search files and directories |
| locate | Fast filename search |
| which | Find executable in PATH |
| whereis | Locate binary, source and man pages |
| type | Identify command type |

Each command solves a different problem.

---

# The find Command

`find` is the most powerful file search command.

Syntax

```bash
find <path> <expression>
```

Search from current directory:

```bash
find .
```

Search entire filesystem:

```bash
find /
```

---

# Search by File Name

Find a file named:

```bash
find . -name "notes.txt"
```

Example output:

```text
./Documents/notes.txt
```

---

# Case-Insensitive Search

```bash
find . -iname "notes.txt"
```

Matches:

```text
Notes.txt

NOTES.TXT

notes.txt
```

---

# Search Directories

```bash
find . -type d
```

Output:

```text
.

./projects

./logs

./backup
```

---

# Search Regular Files

```bash
find . -type f
```

---

# Search Hidden Files

```bash
find . -name ".*"
```

---

# Search Using Wildcards

Find all text files.

```bash
find . -name "*.txt"
```

Find all YAML files.

```bash
find . -name "*.yaml"
```

Find shell scripts.

```bash
find . -name "*.sh"
```

---

# Search by Size

Files larger than 100 MB

```bash
find . -size +100M
```

Files smaller than 10 KB

```bash
find . -size -10k
```

Exactly 50 MB

```bash
find . -size 50M
```

---

# Search by Owner

```bash
find /home -user basha
```

---

# Search by Group

```bash
find /home -group developers
```

---

# Search by Permissions

Example:

```bash
find . -perm 644
```

Find executable files.

```bash
find . -perm /111
```

---

# Search by Modification Time

Modified today

```bash
find . -mtime 0
```

Modified within last 7 days

```bash
find . -mtime -7
```

Older than 30 days

```bash
find . -mtime +30
```

---

# Search Empty Files

```bash
find . -empty
```

---

# Execute Commands on Search Results

Delete log files.

```bash
find . -name "*.log" -delete
```

Display file details.

```bash
find . -name "*.txt" -exec ls -l {} \;
```

!!! warning "Warning"

    Always verify search results before using `-delete`.

---

# The locate Command

`locate` searches a pre-built database.

Example:

```bash
locate sshd_config
```

Much faster than `find`.

---

# Update locate Database

Ubuntu

```bash
sudo updatedb
```

Now:

```bash
locate nginx.conf
```

---

# which

Find executable location.

```bash
which python3
```

Example

```text
/usr/bin/python3
```

Useful for verifying installed commands.

---

# whereis

Displays:

- Binary
- Source
- Manual page

Example:

```bash
whereis ssh
```

Output

```text
ssh:
/usr/bin/ssh
/usr/share/man/man1/ssh.1.gz
```

---

# type

Identify command type.

```bash
type ls
```

Output

```text
ls is /usr/bin/ls
```

Example

```bash
type cd
```

Output

```text
cd is a shell builtin
```

---

# Command Comparison

| Command | Best For |
|----------|-----------|
| find | Powerful searches |
| locate | Fast filename search |
| which | Executables |
| whereis | Binary + Man Page |
| type | Built-in vs External |

---

# Real Production Examples

Find NGINX configuration.

```bash
find /etc -name nginx.conf
```

Find Docker Compose files.

```bash
find /opt -name docker-compose.yml
```

Find Kubernetes YAML.

```bash
find . -name "*.yaml"
```

Find large log files.

```bash
find /var/log -size +500M
```

Find recently modified files.

```bash
find /etc -mtime -1
```

Find executable shell scripts.

```bash
find . -name "*.sh" -perm /111
```

---

# Production Perspective

System administrators frequently search for:

- Configuration files
- Log files
- Core dumps
- Backup archives
- SSL certificates
- Shell scripts
- Kubernetes manifests
- Docker files

Knowing how to search efficiently can significantly reduce troubleshooting time.

---

# Hands-on Lab

## Task 1

Create a lab.

```bash
mkdir search-lab

cd search-lab
```

---

## Task 2

Create files.

```bash
touch app.py

touch config.yaml

touch nginx.conf

touch notes.txt

touch script.sh
```

---

## Task 3

Search YAML.

```bash
find . -name "*.yaml"
```

---

## Task 4

Search shell scripts.

```bash
find . -name "*.sh"
```

---

## Task 5

Search files only.

```bash
find . -type f
```

---

## Task 6

Search directories.

```bash
find . -type d
```

---

## Task 7

Locate Python.

```bash
which python3
```

---

## Task 8

Find SSH.

```bash
whereis ssh
```

---

## Task 9

Identify command type.

```bash
type cd

type ls
```

---

# Command Deep Dive

| Command | Purpose | Common Options | Production Example |
|----------|----------|----------------|--------------------|
| find | Search filesystem | `-name`, `-type`, `-size`, `-mtime` | Find configs and logs |
| locate | Fast filename search | `-i` | Locate SSH configs |
| which | Find executable | Default | Verify installed tools |
| whereis | Binary + docs | Default | Find binaries |
| type | Command type | `-a` | Check shell built-ins |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A web application has stopped working after a configuration change.

Your tasks:

1. Find the NGINX configuration file.
2. Locate all backup configuration files.
3. Identify recently modified configuration files.
4. Find log files larger than 100 MB.
5. Verify where the `nginx` executable is installed.

Example commands:

```bash
find /etc -name "nginx.conf"

find /etc -name "*.bak"

find /etc -mtime -1

find /var/log -size +100M

which nginx
```

---

# Mini Challenge

Create the following structure.

```text
project/

├── app.py

├── config/

│   ├── app.yaml

│   ├── db.yaml

│   └── nginx.conf

├── logs/

│   ├── access.log

│   └── error.log

└── scripts/

    ├── deploy.sh

    └── backup.sh
```

Complete these tasks:

- Find all `.yaml` files.
- Find all shell scripts.
- Find all log files.
- Display only directories.
- Find all files modified today.
- Locate the `bash` executable.

---

# Best Practices

- Use `find` for comprehensive searches.
- Use `locate` when speed is important.
- Limit searches to specific directories instead of searching the entire filesystem.
- Verify results before deleting files.
- Combine search criteria for more precise results.

---

# Common Mistakes

❌ Searching the entire filesystem unnecessarily.

✅ Use:

```bash
find /
```

This can be slow.

Instead:

```bash
find /etc
```

---

❌ Using `rm` immediately after `find`.

✅ Always inspect results first.

---

❌ Forgetting quotes around wildcards.

✅ Correct:

```bash
find . -name "*.log"
```

---

# Interview Questions
## Beginner

1. What is the difference between `find` and `locate`?
2. Which command finds executables?
3. How do you search for directories only?
4. Which command identifies built-in commands?

---

## Intermediate

1. Explain `find -exec`.
2. How do you search files modified within the last seven days?
3. How do you search by permissions?
4. Why is `locate` faster than `find`?

---

## Architect Level

1. How would you locate configuration files during a production outage?
2. How would you identify large log files consuming disk space?
3. How can efficient file searching reduce Mean Time to Resolution (MTTR)?

---

# Summary

In this lesson, you learned:

- Searching files and directories
- Searching by name, type, size, owner, permissions, and modification time
- Using `find`, `locate`, `which`, `whereis`, and `type`
- Real-world search techniques used in production environments

Mastering these commands will make troubleshooting, automation, and system administration significantly faster and more efficient.

---

## Key Takeaways

- `find` is the most powerful Linux search command.
- `locate` provides fast filename searches using an indexed database.
- `which` finds executables in your `PATH`.
- `whereis` locates binaries, source files, and manual pages.
- `type` identifies whether a command is built-in or external.
- Always verify search results before performing destructive actions.

---

## What's Next?

**[Wildcards and Globbing](wildcards-and-globbing.md)**

In the next lesson, you'll learn:

- What wildcards are
- Globbing patterns
- `*`, `?`, and `[]`
- Character ranges
- Brace expansion
- Real-world file selection techniques
- Using wildcards safely in production
