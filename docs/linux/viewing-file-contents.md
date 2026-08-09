---
title: "Viewing File Contents"
description: "View, inspect, and monitor Linux file contents with cat, less, more, head, tail, tac, nl, file, and wc — essential for logs and configuration troubleshooting."
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
  - logs
  - command-line
  - rebash-linux-mastery
comments: false
status: ready
---

# Viewing File Contents

> Linux provides powerful commands to view, inspect, and monitor file contents. Whether you're reading configuration files, analyzing application logs, or debugging production issues, mastering these commands is essential for every Linux administrator, DevOps Engineer, and Cloud Engineer.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 2: Linux Command Line Essentials → Lesson 5</p>

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

<div markdown>**Lesson:** 5 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- View file contents efficiently
- Read large log files
- Display specific lines from files
- Monitor files in real time
- Compare different file viewing commands
- Choose the right command for different scenarios

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 Lessons 1–4

---

# Why Learn File Viewing Commands?

Linux systems store everything in files.

Examples include:

- Configuration files
- Application logs
- Shell scripts
- Kubernetes YAML files
- Docker Compose files
- Service logs

As a Linux administrator, reading files is one of the most common daily tasks.

---

# Sample File

Throughout this lesson we'll use the following file.

```text
Line 1: Linux
Line 2: Docker
Line 3: Kubernetes
Line 4: Terraform
Line 5: Ansible
Line 6: GitLab
Line 7: Jenkins
Line 8: Prometheus
Line 9: Grafana
Line 10: REBASH Academy
```

---

# cat

The **cat** command displays the complete contents of a file.

Syntax

```bash
cat filename
```

Example

```bash
cat notes.txt
```

Display multiple files

```bash
cat file1 file2
```

Display line numbers

```bash
cat -n notes.txt
```

Useful when viewing:

- Configuration files
- Small scripts
- README files

---

# less

`less` is one of the most useful Linux commands.

Unlike `cat`, it lets you scroll through large files.

```bash
less logfile.log
```

Navigation

| Key | Action |
|------|--------|
| Space | Next Page |
| b | Previous Page |
| ↑ ↓ | Scroll |
| / | Search |
| n | Next Match |
| q | Quit |

Perfect for:

- System logs
- Large configuration files
- Long text files

---

# more

Older pager command.

```bash
more notes.txt
```

Displays one screen at a time.

Although still available, most Linux administrators prefer `less`.

---

# head

Display the beginning of a file.

```bash
head notes.txt
```

Default:

```text
First 10 lines
```

Display first five lines

```bash
head -5 notes.txt
```

Production example

```bash
head /var/log/syslog
```

---

# tail

Display the end of a file.

```bash
tail notes.txt
```

Display last five lines

```bash
tail -5 notes.txt
```

Production example

```bash
tail /var/log/syslog
```

---

# Real-Time Monitoring

One of the most useful Linux commands.

```bash
tail -f /var/log/syslog
```

Linux continuously displays new lines as they are written.

Widely used for:

- Application logs
- Kubernetes logs
- Web server logs
- Docker logs

Stop monitoring:

```text
Ctrl + C
```

---

# tac

Reverse of `cat`.

```bash
tac notes.txt
```

Displays the file from bottom to top.

Useful when newest information is at the end of the file.

---

# nl

Display line numbers.

```bash
nl notes.txt
```

Output

```text
1 Linux

2 Docker

3 Kubernetes
```

Useful when discussing specific lines in configuration files.

---

# file

Determine the file type.

```bash
file notes.txt
```

Example output

```text
ASCII text
```

Check executable

```bash
file /bin/ls
```

---

# wc

Count lines, words and characters.

```bash
wc notes.txt
```

Example

```text
10 10 90 notes.txt
```

Only count lines

```bash
wc -l notes.txt
```

Count words

```bash
wc -w notes.txt
```

---

# strings

Display printable text from binary files.

```bash
strings binaryfile
```

Useful when investigating executables.

---

# Command Comparison

| Command | Best Used For |
|----------|---------------|
| cat | Small files |
| less | Large files |
| more | Basic paging |
| head | Beginning of file |
| tail | End of file |
| tail -f | Live log monitoring |
| tac | Reverse output |
| nl | Line numbers |
| file | Identify file type |
| wc | Count lines and words |

---

# Production Example

A web application is failing.

Check logs:

```bash
tail -50 /var/log/nginx/error.log
```

Monitor new errors:

```bash
tail -f /var/log/nginx/error.log
```

View configuration:

```bash
less /etc/nginx/nginx.conf
```

Verify line numbers:

```bash
cat -n /etc/nginx/nginx.conf
```

This workflow is common during production troubleshooting.

---

# Production Perspective

These commands are used daily by engineers.

Examples

View Kubernetes YAML

```bash
cat deployment.yaml
```

Read Docker logs

```bash
less docker.log
```

Monitor application

```bash
tail -f application.log
```

Read configuration

```bash
less /etc/ssh/sshd_config
```

Count log entries

```bash
wc -l access.log
```

---

# Hands-on Lab

## Task 1

Create a file.

```bash
cat > commands.txt
```

Add:

```text
Linux
Docker
Kubernetes
Terraform
Ansible
Git
```

Press:

```text
Ctrl + D
```

---

## Task 2

Display file.

```bash
cat commands.txt
```

---

## Task 3

Display first three lines.

```bash
head -3 commands.txt
```

---

## Task 4

Display last two lines.

```bash
tail -2 commands.txt
```

---

## Task 5

Display line numbers.

```bash
nl commands.txt
```

---

## Task 6

Count lines.

```bash
wc -l commands.txt
```

---

## Task 7

Open using less.

```bash
less commands.txt
```

Quit:

```text
q
```

---

## Task 8

Display reverse order.

```bash
tac commands.txt
```

---

# Command Deep Dive

| Command | Purpose | Common Options | Production Example |
|----------|----------|----------------|--------------------|
| cat | Display files | -n | View configuration |
| less | Scroll files | Search `/` | Read logs |
| head | Beginning | -5 | Verify headers |
| tail | End | -10 | View recent logs |
| tail | Live logs | -f | Monitor applications |
| nl | Line numbers | Default | Debug configs |
| wc | Count | -l -w | Count log entries |
| file | File type | Default | Verify downloads |

---

# Mini Challenge

Create a file named:

```text
linux-tools.txt
```

Add at least 10 Linux commands.

Now:

- Display the first 5 lines.
- Display the last 3 lines.
- Count the number of lines.
- Display line numbers.
- View the file using `less`.
- Display the file in reverse order.

---

# Best Practices

- Use `less` instead of `cat` for large files.
- Use `tail -f` for monitoring logs.
- Use `head` to inspect file headers.
- Use `wc` to quickly summarize file contents.
- Learn keyboard shortcuts in `less`.

---

# Common Mistakes

❌ Using `cat` on huge log files.

✅ Use:

```bash
less logfile.log
```

or

```bash
tail logfile.log
```

---

❌ Opening multi-GB log files in editors.

✅ Use:

```bash
tail

head

less
```

---

❌ Forgetting to quit `less`.

✅ Use:

```text
q
```

---

# Interview Questions
## Beginner

1. What does `cat` do?
2. Difference between `head` and `tail`?
3. Which command monitors logs in real time?
4. What is `less` used for?

---

## Intermediate

1. Why is `less` preferred over `cat` for large files?
2. Explain `tail -f`.
3. How do you count the number of lines in a file?
4. What does the `file` command do?

---

## Architect Level

1. How would you investigate a production application that is generating errors?
2. Which commands would you use to analyze a 5 GB log file?
3. Why is `tail -f` essential for production monitoring?

---

# Summary

In this lesson, you learned:

- Displaying file contents
- Reading large files
- Viewing file headers and footers
- Monitoring logs in real time
- Counting lines
- Identifying file types
- Choosing the right command for different situations

These commands form the foundation of Linux troubleshooting and system administration.

---

## Key Takeaways

- `cat` is ideal for small files.
- `less` is the preferred tool for large files.
- `head` displays the beginning of a file.
- `tail` displays the end of a file.
- `tail -f` monitors log files in real time.
- `wc` counts lines, words, and characters.
- Choosing the right command improves productivity and troubleshooting efficiency.

---

## What's Next?

**[Searching Files and Directories](searching-files.md)**

In the next lesson, you'll learn:

- `find`
- `locate`
- `which`
- `whereis`
- `type`
- Searching by name, size, permissions, owner, and modification time
- Real-world search techniques used by Linux administrators
