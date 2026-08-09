---
title: "grep Command — Searching Text in Linux"
description: "Search text and logs with grep — case-insensitive, recursive, line numbers, invert match, and basic regular expressions for production troubleshooting."
difficulty: intermediate
estimated_time: "35 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 3 · Text Processing"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - grep
  - text-processing
  - logs
  - rebash-linux-mastery
comments: false
status: ready
---

# grep Command — Searching Text in Linux

> The `grep` command is one of the most powerful and frequently used Linux utilities. It searches text for specific patterns, making it indispensable for system administration, DevOps, Cloud Engineering, cybersecurity, and troubleshooting. If you master `grep`, you'll be able to analyze logs, configuration files, and command outputs with incredible speed.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 3: Text Processing → Lesson 2</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 35 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Text Processing</div>

<div markdown>**Lesson:** 2 of 18</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `grep` command
- Search text inside files
- Search multiple files
- Perform case-insensitive searches
- Count matching lines
- Display line numbers
- Search recursively
- Use Basic Regular Expressions
- Analyze production log files

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 Lesson 1 (`cat`)

---

# Why Learn grep?

Imagine you're managing a production server with a log file containing **2 million lines**.

You're looking for:

- ERROR
- WARNING
- nginx
- ssh
- Kubernetes
- Database failures

Instead of manually reading the file, use:

```bash
grep ERROR application.log
```

Instant results.

This is why `grep` is one of the most used Linux commands.

---

# What is grep?

`grep` stands for:

> **Global Regular Expression Print**

It searches files or command output for text that matches a pattern.

Syntax:

```bash
grep [OPTIONS] PATTERN FILE
```

---

# Sample File

Create a sample file.

```bash
cat > employees.txt
```

Contents:

```text
Alice Engineering

Bob HR

Charlie Engineering

David Finance

Eve Engineering
```

Press:

```text
Ctrl + D
```

---

# Basic Search

Search for:

```bash
grep Engineering employees.txt
```

Output:

```text
Alice Engineering

Charlie Engineering

Eve Engineering
```

---

# Case-Insensitive Search

Normally:

```bash
grep linux file.txt
```

does not match:

```text
Linux
```

Use:

```bash
grep -i linux file.txt
```

Matches:

```text
Linux

LINUX

linux
```

---

# Display Line Numbers

```bash
grep -n Engineering employees.txt
```

Output:

```text
1: Alice Engineering

3: Charlie Engineering

5: Eve Engineering
```

---

# Count Matches

```bash
grep -c Engineering employees.txt
```

Output:

```text
3
```

---

# Invert Match

Display everything **except** Engineering.

```bash
grep -v Engineering employees.txt
```

Output:

```text
Bob HR

David Finance
```

---

# Search Multiple Files

```bash
grep ERROR app.log server.log
```

Output:

```text
app.log:ERROR Database Down

server.log:ERROR Connection Failed
```

---

# Recursive Search

Search every file in a directory.

```bash
grep -r nginx /etc
```

Useful for finding configuration values.

---

# Search Whole Words

Suppose:

```text
cat

catalog

category
```

Search:

```bash
grep cat file.txt
```

Matches all three.

Search whole word only:

```bash
grep -w cat file.txt
```

Output:

```text
cat
```

---

# Match Beginning of Line

```bash
grep "^Alice" employees.txt
```

Output:

```text
Alice Engineering
```

---

# Match End of Line

```bash
grep "Engineering$" employees.txt
```

Matches only lines ending with:

```text
Engineering
```

---

# Search Multiple Patterns

```bash
grep -E "ERROR|WARNING" app.log
```

Matches:

```text
ERROR

WARNING
```

---

# Ignore Binary Files

```bash
grep -I ERROR *
```

Useful when searching directories containing binary files.

---

# Search with Color

```bash
grep --color=auto ERROR app.log
```

Matches are highlighted.

---

# Search Command Output

Find SSH process.

```bash
ps -ef | grep ssh
```

Search Docker containers.

```bash
docker ps | grep nginx
```

Search Kubernetes Pods.

```bash
kubectl get pods | grep Running
```

---

# Search Configuration Files

NGINX

```bash
grep server_name /etc/nginx/nginx.conf
```

SSH

```bash
grep PermitRootLogin /etc/ssh/sshd_config
```

Hosts

```bash
grep localhost /etc/hosts
```

---

# Basic Regular Expressions

Match lines starting with "A".

```bash
grep "^A" employees.txt
```

Match lines ending with "HR".

```bash
grep "HR$" employees.txt
```

Match any line containing numbers.

```bash
grep "[0-9]" file.txt
```

Match lowercase letters.

```bash
grep "[a-z]" file.txt
```

---

# Common grep Options

| Option | Description |
|----------|-------------|
| `-i` | Ignore case |
| `-n` | Show line numbers |
| `-v` | Invert match |
| `-c` | Count matches |
| `-r` | Recursive search |
| `-w` | Whole words only |
| `-l` | Display filenames only |
| `-E` | Extended regular expressions |

---

# Real Production Examples

Find failed logins.

```bash
grep "Failed password" /var/log/auth.log
```

Find Kubernetes errors.

```bash
kubectl logs pod-name | grep ERROR
```

Search Docker logs.

```bash
docker logs container | grep Exception
```

Search NGINX errors.

```bash
grep 500 access.log
```

Search system logs.

```bash
journalctl | grep CRITICAL
```

---

# Production Perspective

Engineers use `grep` daily for:

- Searching logs
- Finding configuration values
- Debugging applications
- Monitoring services
- Incident response
- Security investigations

Learning `grep` is one of the fastest ways to improve Linux troubleshooting skills.

---

# Hands-on Lab

## Task 1

Create:

```bash
cat > servers.txt
```

Contents:

```text
server01 Running

server02 Stopped

server03 Running

server04 Failed

server05 Running
```

---

## Task 2

Search:

```bash
grep Running servers.txt
```

---

## Task 3

Ignore case.

```bash
grep -i running servers.txt
```

---

## Task 4

Display line numbers.

```bash
grep -n Running servers.txt
```

---

## Task 5

Count running servers.

```bash
grep -c Running servers.txt
```

---

## Task 6

Display non-running servers.

```bash
grep -v Running servers.txt
```

---

## Task 7

Search beginning of line.

```bash
grep "^server01" servers.txt
```

---

## Task 8

Search end of line.

```bash
grep "Running$" servers.txt
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `grep text file` | Search text | Find configs |
| `grep -i` | Ignore case | Search logs |
| `grep -n` | Line numbers | Debug configs |
| `grep -c` | Count matches | Count errors |
| `grep -v` | Exclude matches | Filter logs |
| `grep -r` | Recursive search | Search `/etc` |
| `grep -w` | Whole words | Match exact values |
| `grep -E` | Multiple patterns | ERROR or WARNING |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    Users report that an application is failing.

Tasks:

1. Find all ERROR messages.
2. Count the number of ERROR entries.
3. Display only WARNING and ERROR messages.
4. Search configuration files for database settings.
5. Find failed SSH login attempts.

Solutions:

```bash
grep ERROR app.log

grep -c ERROR app.log

grep -E "ERROR|WARNING" app.log

grep -r database /etc/myapp

grep "Failed password" /var/log/auth.log
```

---

# Mini Challenge

Create:

```text
application.log
```

Contents:

```text
INFO Server Started

INFO User Login

WARNING High Memory Usage

ERROR Database Connection Failed

INFO Health Check Passed

ERROR API Timeout

WARNING Disk Space Low
```

Perform the following:

- Display all ERROR messages.
- Display all WARNING messages.
- Count ERROR messages.
- Show line numbers for WARNING messages.
- Display everything except INFO.
- Search for both ERROR and WARNING together.

---

# Best Practices

- Use `grep -i` when case doesn't matter.
- Use `grep -n` while editing configuration files.
- Use `grep -c` to count matching lines.
- Combine `grep` with pipes for powerful filtering.
- Learn regular expressions to unlock the full power of `grep`.

---

# Common Mistakes

❌ Searching recursively from the filesystem root.

✅ Use:

```bash
grep -r error /
```

This can be very slow.

Instead:

```bash
grep -r error /var/log
```

---

❌ Forgetting quotes around patterns containing special characters.

✅ Use:

```bash
grep "^ERROR" app.log
```

---

❌ Confusing `grep` with `find`.

✅ - `find` searches **files**
- `grep` searches **inside files**

---

# Interview Questions
## Beginner

1. What does `grep` stand for?
2. How do you search for text in a file?
3. What does `grep -i` do?
4. What does `grep -v` do?

---

## Intermediate

1. Difference between `grep` and `find`?
2. Explain `grep -r`.
3. What is `grep -E`?
4. How do you count matching lines?

---

## Architect Level

1. How would you analyze a 10 GB application log?
2. Why is `grep` one of the most important Linux troubleshooting tools?
3. How can `grep` improve incident response during production outages?

---

# Summary

In this lesson, you learned:

- Searching text with `grep`
- Case-insensitive searches
- Counting matches
- Recursive searches
- Whole-word matching
- Basic regular expressions
- Production log analysis

`grep` is one of the most valuable Linux commands. Combined with pipes, regular expressions, and other text-processing tools, it becomes an essential part of every Linux engineer's toolkit.

---

## Key Takeaways

- `grep` searches text inside files and command output.
- `grep -i` ignores case differences.
- `grep -n` displays line numbers.
- `grep -c` counts matching lines.
- `grep -v` excludes matching lines.
- `grep -r` searches directories recursively.
- Mastering `grep` significantly improves troubleshooting and log analysis.

---

## What's Next?

**[cut Command — Extracting Columns from Text](text-processing-cut.md)**

In the next lesson, you'll learn:

- Extracting fields from structured text
- Working with delimiters
- Selecting multiple columns
- Processing CSV and log files
- Real-world text extraction techniques
