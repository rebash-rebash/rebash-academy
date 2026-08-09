---
title: "Foreground and Background Jobs — Running Multiple Tasks in Linux"
description: "Control Linux foreground and background jobs — use jobs, bg, fg, Ctrl+Z, and nohup for multitasking and long-running terminal sessions."
difficulty: intermediate
estimated_time: "55 min"
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
  - jobs
  - background
  - nohup
  - job-control
  - rebash-linux-mastery
comments: false
status: ready
---

# Foreground and Background Jobs — Running Multiple Tasks in Linux

> Linux allows you to run multiple commands simultaneously by managing processes in the **foreground** and **background**. This feature, known as **Job Control**, enables you to continue using your terminal while long-running tasks execute in the background. It is an essential skill for Linux administrators, DevOps engineers, and system operators.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 6: Process Management → Lesson 2</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 55 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Process Management</div>

<div markdown>**Lesson:** 2 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand foreground and background jobs
- Move jobs between foreground and background
- Use job control commands
- Suspend and resume processes
- Run long-running tasks in the background
- Use `nohup` for persistent execution
- Monitor jobs
- Apply job control in production

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management and Permissions
- Module 5 – Users and Groups
- Module 6 Lesson 1 – Processes

---

# Why Learn Job Control?

Imagine you start copying a huge backup.

```bash
cp -r backup /mnt/storage
```

The copy takes 30 minutes.

Meanwhile, you want to continue working in the same terminal.

Should you wait?

No.

Linux allows you to move long-running tasks to the background.

---

# Foreground Process

A foreground process:

- Runs in the current terminal
- Receives keyboard input
- Blocks the shell until it finishes

Example:

```bash
sleep 30
```

Your terminal remains busy until the command completes.

---

# Background Process

A background process:

- Runs independently
- Does not block the terminal
- Allows you to continue entering commands

Example:

```bash
sleep 300 &
```

Output:

```text
[1] 12345
```

Where:

```text
[1]
```

Job Number

```text
12345
```

Process ID (PID)

---

# Running a Command in the Background

Simply append:

```bash
&
```

Example:

```bash
python app.py &
```

or

```bash
tar -czf backup.tar.gz /data &
```

---

# Viewing Background Jobs

Display jobs.

```bash
jobs
```

Example:

```text
[1]+ Running sleep 300 &
```

---

# Suspend a Foreground Process

Start:

```bash
sleep 300
```

Press:

```text
Ctrl + Z
```

Output:

```text
Stopped
```

The process is suspended.

---

# Resume in Background

```bash
bg
```

Output:

```text
[1]+ sleep 300 &
```

---

# Resume in Foreground

```bash
fg
```

The process returns to the foreground.

---

# Working with Multiple Jobs

Start:

```bash
sleep 100 &

sleep 200 &

sleep 300 &
```

View:

```bash
jobs
```

Example:

```text
[1]

[2]

[3]
```

Bring Job 2 to the foreground.

```bash
fg %2
```

Resume Job 3.

```bash
bg %3
```

---

# Kill a Job

Terminate a background job.

```bash
kill %1
```

or

```bash
kill PID
```

---

# Understanding nohup

Normally:

When you close the terminal,

the process stops.

Example:

```bash
python app.py
```

Close terminal:

```text
Process Ends
```

---

# Running with nohup

```bash
nohup python app.py &
```

Output:

```text
nohup: ignoring input

appending output to nohup.out
```

Now:

- Close terminal
- Process continues running

---

# Redirect Output

Instead of:

```text
nohup.out
```

Redirect manually.

```bash
nohup python app.py > app.log 2>&1 &
```

---

# Check Running Jobs

```bash
jobs
```

Check process.

```bash
ps -ef
```

---

# Common Commands

Run in background.

```bash
command &
```

Display jobs.

```bash
jobs
```

Suspend process.

```text
Ctrl + Z
```

Resume in background.

```bash
bg
```

Resume in foreground.

```bash
fg
```

Persistent execution.

```bash
nohup command &
```

---

# Real Production Examples

Run backup.

```bash
tar -czf backup.tar.gz /var &
```

Database export.

```bash
mysqldump database > backup.sql &
```

Long Python script.

```bash
nohup python migrate.py &
```

Run Ansible.

```bash
ansible-playbook deploy.yml &
```

---

# Production Perspective

Foreground and background jobs are useful for:

- Backup operations
- Log analysis
- Long-running scripts
- Database exports
- File transfers
- Automation
- Remote administration

For long-running production services, however, use a service manager such as **systemd** rather than background jobs. Background jobs are primarily intended for interactive shell sessions.

---

# Hands-on Lab

## Task 1

Run a command in the foreground.

```bash
sleep 30
```

---

## Task 2

Run the same command in the background.

```bash
sleep 300 &
```

---

## Task 3

Display jobs.

```bash
jobs
```

---

## Task 4

Suspend a foreground command.

```bash
sleep 300
```

Press:

```text
Ctrl + Z
```

---

## Task 5

Resume it.

```bash
bg
```

---

## Task 6

Bring it back.

```bash
fg
```

---

## Task 7

Run a persistent process.

```bash
nohup sleep 600 &
```

---

## Task 8

Terminate the background job.

```bash
jobs

kill %1
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `jobs` | Display shell jobs | Job monitoring |
| `bg` | Resume in background | Multitasking |
| `fg` | Bring to foreground | User interaction |
| `nohup` | Continue after logout | Long-running scripts |
| `kill` | Stop a process or job | Administration |
| `&` | Start in background | Automation |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A DevOps engineer starts a database migration.

```bash
python migrate.py
```

The migration takes several hours.

Closing the SSH session would terminate the process.

Solution:

Stop the process and restart it using:

```bash
nohup python migrate.py > migrate.log 2>&1 &
```

Verify:

```bash
ps -ef | grep migrate

tail -f migrate.log
```

The migration continues even after the SSH session disconnects.

!!! note "Note"

    In production, tools such as `screen`, `tmux`, or `systemd` are often preferred for managing long-running interactive or service workloads.

---

# Best Practices

- Use background jobs for long-running interactive commands.
- Use `nohup` if the process must continue after logout.
- Redirect output to log files.
- Monitor background jobs periodically.
- Use `systemd` for production services instead of relying on shell background jobs.

---

# Common Mistakes

❌ Closing the terminal without using `nohup`.

✅ The process may terminate.

---

❌ Forgetting where command output is being written.

✅ Always redirect output to a log file when appropriate.

---

❌ Running production applications as simple background jobs.

✅ Use `systemd` or another service manager for long-running services.

---

# Interview Questions
## Beginner

1. What is a foreground process?
2. What is a background process?
3. Which symbol starts a background job?
4. Which command displays background jobs?

---

## Intermediate

1. What is the difference between `bg` and `fg`?
2. What does `Ctrl + Z` do?
3. Why is `nohup` useful?
4. How do you terminate a background job?

---

## Architect Level

1. Why shouldn't production services be managed as simple background jobs?
2. When would you use `nohup`, `screen`, `tmux`, or `systemd`?
3. How would you safely run a long-running deployment script over SSH?

---

# Summary

In this lesson, you learned:

- Foreground processes
- Background processes
- Job control
- `jobs`
- `bg`
- `fg`
- `nohup`
- Production best practices

Linux job control allows you to multitask efficiently from a terminal by moving processes between the foreground and background. Understanding these concepts improves productivity and helps manage long-running tasks without interrupting your workflow.

---

## Key Takeaways

- Foreground jobs occupy the terminal until they finish.
- Background jobs allow you to continue using the terminal.
- Use `&` to start a process in the background.
- Use `jobs` to list active shell jobs.
- Use `Ctrl + Z`, `bg`, and `fg` to control jobs.
- Use `nohup` to keep a process running after logging out.
- Use `systemd` for long-running production services.

---

## What's Next?

**[The ps Command — Viewing and Analyzing Processes in Linux](ps.md)**

You'll explore:

- Viewing running processes
- Understanding PID and PPID
- Filtering process information
- Customizing `ps` output
- Monitoring application processes
- Troubleshooting production systems

The `ps` command is one of the most frequently used Linux utilities for inspecting and diagnosing running processes.
