---
title: "The ps Command — Viewing and Analyzing Processes in Linux"
description: "Use the Linux ps command — view PIDs, ownership, process trees, custom columns, and filter processes for production troubleshooting."
difficulty: intermediate
estimated_time: "60 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 6 · Process Management"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - ps
  - processes
  - monitoring
  - troubleshooting
  - rebash-linux-mastery
comments: false
status: ready
---

# The `ps` Command — Viewing and Analyzing Processes in Linux

> The `ps` (**Process Status**) command is one of the most important Linux utilities for viewing running processes. It provides detailed information about process IDs (PIDs), users, CPU usage, memory consumption, parent-child relationships, process states, and running commands. Every Linux administrator, DevOps engineer, SRE, and Cloud Architect uses `ps` daily for troubleshooting and system monitoring.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 6: Process Management → Lesson 3</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 60 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Process Management</div>

<div markdown>**Lesson:** 3 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `ps` command
- Display running processes
- Interpret `ps` output
- View process ownership
- Filter processes
- Display process hierarchy
- Customize process information
- Troubleshoot production applications

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management and Permissions
- Module 5 – Users and Groups
- Module 6 Lessons 1–2

---

# Why Learn the ps Command?

Imagine a production application stops responding.

Questions:

- Is the application running?
- What is its PID?
- Who owns the process?
- How much CPU is it using?
- Is it stuck?

The first command most Linux administrators use is:

```bash
ps
```

---

# What is ps?

`ps` stands for:

> **Process Status**

It displays information about running processes.

Unlike `top`, `ps` shows a **snapshot** of the processes at the moment you execute the command.

---

# Basic Usage

```bash
ps
```

Example:

```text
PID TTY          TIME CMD

3241 pts/0 00:00:00 bash

3410 pts/0 00:00:00 ps
```

By default, it displays processes associated with the current terminal.

---

# Display All Processes

```bash
ps -e
```

or

```bash
ps -A
```

Example:

```text
PID TTY TIME CMD

1 ? 00:00:03 systemd

645 ? 00:00:01 sshd

1200 ? 00:00:04 nginx
```

---

# Full Process List

```bash
ps -ef
```

Example:

```text
UID PID PPID C STIME TTY TIME CMD

root 1 0 0 systemd

root 642 1 0 sshd

basha 2501 642 0 bash
```

---

# BSD Style Output

Linux also supports BSD-style options.

```bash
ps aux
```

Example:

```text
USER PID %CPU %MEM COMMAND
```

Unlike `ps -ef`, BSD-style options omit the leading hyphen.

---

# Understanding ps -ef Output

| Column | Description |
|----------|-------------|
| UID | Process owner |
| PID | Process ID |
| PPID | Parent Process ID |
| C | CPU scheduling value |
| STIME | Start time |
| TTY | Terminal |
| TIME | CPU time used |
| CMD | Command |

---

# Display Process Tree

```bash
ps -ejH
```

or

```bash
pstree
```

Example:

```text
systemd

└── sshd

     └── bash

          └── python
```

---

# Display Process State

```bash
ps -eo pid,state,comm
```

Example:

```text
PID S COMMAND

1 S systemd

245 R bash

300 S sshd
```

---

# Display Specific Process

Using a PID.

```bash
ps -p 1
```

Example:

```text
PID COMMAND

1 systemd
```

Multiple PIDs.

```bash
ps -p 1,100,500
```

---

# Display Processes by User

```bash
ps -u basha
```

Example:

```text
PID CMD

321 bash

550 python
```

Display all processes owned by root.

```bash
ps -U root
```

---

# Filter Using grep

Example:

```bash
ps -ef | grep nginx
```

Find Docker.

```bash
ps -ef | grep docker
```

Find Java.

```bash
ps -ef | grep java
```

---

# Custom Output

Show PID, user, and command.

```bash
ps -eo pid,user,comm
```

Show CPU and memory usage.

```bash
ps -eo pid,%cpu,%mem,comm
```

Show elapsed running time.

```bash
ps -eo pid,etime,comm
```

---

# Sort Processes

Sort by CPU.

```bash
ps -eo pid,%cpu,comm --sort=-%cpu
```

Sort by memory.

```bash
ps -eo pid,%mem,comm --sort=-%mem
```

Display the top 10 CPU consumers.

```bash
ps -eo pid,%cpu,comm --sort=-%cpu | head
```

---

# View Parent-Child Relationship

```bash
ps -f
```

Observe:

```text
PID

PPID
```

This helps identify process hierarchies.

---

# Common Commands

Basic process list.

```bash
ps
```

All processes.

```bash
ps -e
```

Detailed view.

```bash
ps -ef
```

BSD format.

```bash
ps aux
```

Single process.

```bash
ps -p PID
```

By user.

```bash
ps -u username
```

---

# Real Production Examples

Check NGINX.

```bash
ps -ef | grep nginx
```

Check Kubernetes.

```bash
ps -ef | grep kubelet
```

Check Docker.

```bash
ps -ef | grep docker
```

Check PostgreSQL.

```bash
ps -ef | grep postgres
```

Check Java application.

```bash
ps -ef | grep java
```

---

# Production Perspective

The `ps` command is used extensively for:

- Troubleshooting applications
- Identifying running services
- Monitoring process ownership
- Finding PIDs
- Preparing to terminate processes
- Capacity planning
- Performance analysis

It is one of the first commands used during production incident investigations.

---

# Hands-on Lab

## Task 1

Display your terminal processes.

```bash
ps
```

---

## Task 2

Display all processes.

```bash
ps -ef
```

---

## Task 3

Display BSD format.

```bash
ps aux
```

---

## Task 4

Display PID 1.

```bash
ps -p 1
```

---

## Task 5

Display process states.

```bash
ps -eo pid,state,comm
```

---

## Task 6

Display your own processes.

```bash
ps -u $USER
```

---

## Task 7

Search for SSH.

```bash
ps -ef | grep ssh
```

---

## Task 8

Display the top CPU-consuming processes.

```bash
ps -eo pid,%cpu,comm --sort=-%cpu | head
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `ps` | Current terminal processes | Daily usage |
| `ps -ef` | Full process list | Troubleshooting |
| `ps aux` | BSD-style process list | Monitoring |
| `ps -p` | Specific PID | Process verification |
| `ps -u` | User processes | User audits |
| `ps -eo` | Custom output | Reporting |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    Users report that the company web application is unavailable.

Investigation:

```bash
ps -ef | grep nginx

ps -ef | grep java

ps -ef | grep node
```

Findings:

- NGINX is running.
- The backend Java application is missing.

Next steps:

- Review application logs.
- Restart the backend service if appropriate.
- Investigate why the process terminated unexpectedly.

The `ps` command quickly confirms whether critical services are running before deeper troubleshooting begins.

---

# Best Practices

- Use `ps -ef` for detailed process information.
- Use `grep` to locate specific processes.
- Verify the process owner before taking action.
- Use custom output (`ps -eo`) when creating reports.
- Combine `ps` with other monitoring tools such as `top` and `systemctl` for comprehensive diagnostics.

---

# Common Mistakes

❌ Assuming a service is running without verifying it.

✅ Verify a service is running without verifying it instead of assuming it.

---

❌ Killing the wrong process because the PID was not checked carefully.

✅ Avoid this mistake: killing the wrong process because the PID was not checked carefully.

---

❌ Forgetting that `ps` displays a snapshot, not a live view.

✅ Use `top` or `htop` for real-time monitoring.

---

# Interview Questions
## Beginner

1. What does `ps` stand for?
2. What is the difference between `ps` and `ps -ef`?
3. Which command displays all running processes?
4. How do you display a specific PID?

---

## Intermediate

1. What is the difference between `ps -ef` and `ps aux`?
2. How do you display processes owned by a specific user?
3. How do you sort processes by CPU usage?
4. Why is the PPID important?

---

## Architect Level

1. How would you investigate whether an application is still running?
2. How do you identify orphaned or unexpected processes?
3. Why is `ps` an important tool during production incident response?

---

# Summary

In this lesson, you learned:

- The `ps` command
- Viewing running processes
- Understanding PID and PPID
- Process ownership
- Filtering processes
- Custom output
- Process hierarchy
- Production troubleshooting

The `ps` command is one of the most fundamental Linux administration tools. It provides a detailed snapshot of the system's running processes and is indispensable for troubleshooting, monitoring, and managing production workloads.

---

## Key Takeaways

- `ps` displays a snapshot of running processes.
- Use `ps -ef` for detailed process information.
- Use `ps aux` for BSD-style output.
- Use `ps -p` to inspect a specific process.
- Use `ps -u` to display processes for a user.
- Combine `ps` with `grep` to quickly locate specific applications.

---

## What's Next?

**[The top Command — Real-Time Process Monitoring in Linux](top.md)**

You'll explore:

- Real-time process monitoring
- CPU and memory utilization
- System load
- Interactive process management
- Sorting processes
- Performance troubleshooting

The `top` command provides a live view of your Linux system and is one of the most valuable tools for diagnosing performance issues in production environments.
