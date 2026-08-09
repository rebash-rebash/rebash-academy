---
title: "Pipes (`|`) in Linux"
description: "Connect Linux commands with pipes — filter, search, sort, and analyze data in production-ready pipelines for DevOps and cloud work."
difficulty: intermediate
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
  - pipes
  - bash
  - command-line
  - rebash-linux-mastery
comments: false
status: ready
---

# Pipes (`|`) in Linux

> Pipes are one of the most powerful features of Linux. They allow you to connect multiple commands together, where the output of one command becomes the input of another. Instead of creating temporary files, you can build efficient command pipelines for filtering, searching, analyzing, and processing data.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 2: Linux Command Line Essentials → Lesson 10</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 30 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Linux Command Line Essentials</div>

<div markdown>**Lesson:** 10 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand what a pipe is
- Learn how pipes work internally
- Connect multiple Linux commands
- Filter and process command output
- Build powerful command pipelines
- Use pipes in real-world administration tasks
- Apply pipes in DevOps and Cloud environments

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 Lessons 1–9

---

# Why Learn Pipes?

Suppose you have 5,000 running processes.

You don't want to see all of them.

Instead, you only want to find:

- Docker
- Kubernetes
- NGINX
- SSH

Without pipes, this becomes difficult.

With pipes:

```bash
ps -ef | grep nginx
```

One command.

Instant results.

---

# What is a Pipe?

A **pipe (`|`)** sends the **Standard Output (stdout)** of one command directly to the **Standard Input (stdin)** of another command.

Instead of displaying output on the screen, Linux transfers it directly between commands.

---

# How Pipes Work

```text
Command 1

↓

Standard Output

↓

Pipe (|)

↓

Standard Input

↓

Command 2

↓

Output
```

Example:

```bash
ls | wc -l
```

Workflow:

```text
List Files

↓

Pipe

↓

Count Files

↓

Display Count
```

---

# Basic Pipe Example

Without pipe:

```bash
ls
```

Displays:

```text
Documents

Downloads

Pictures

Videos
```

With pipe:

```bash
ls | wc -l
```

Output:

```text
4
```

---

# Pipe with `grep`

Find running SSH processes.

```bash
ps -ef | grep ssh
```

Pipeline:

```text
ps -ef

↓

grep ssh

↓

Matching Processes
```

---

# Pipe with `head`

Display only the first five files.

```bash
ls -l | head -5
```

---

# Pipe with `tail`

Display the last five files.

```bash
ls -l | tail -5
```

---

# Multiple Pipes

Linux allows unlimited pipelines.

Example:

```bash
cat users.txt | sort | uniq
```

Workflow:

```text
Read File

↓

Sort

↓

Remove Duplicates

↓

Display Result
```

---

# Count Matching Results

Example:

```bash
cat users.txt | grep admin | wc -l
```

Pipeline:

```text
Read File

↓

Find "admin"

↓

Count Matches

↓

Display Total
```

---

# Sort Output

Example:

```bash
cat employees.txt | sort
```

Output:

```text
Alice

Bob

Charlie

David
```

Reverse sort:

```bash
cat employees.txt | sort -r
```

---

# Remove Duplicate Entries

Example:

```bash
sort employees.txt | uniq
```

Count duplicates:

```bash
sort employees.txt | uniq -c
```

Example:

```text
2 Alice

1 Bob

1 Charlie
```

---

# Pipe with `tee`

Display output while saving it.

```bash
ls | tee files.txt
```

Output:

```text
Documents

Downloads

Pictures
```

The same output is saved to:

```text
files.txt
```

---

# Pipe with `less`

Large output:

```bash
journalctl | less
```

Benefits:

- Scroll
- Search
- Navigate

Ideal for production logs.

---

# Pipe with `xargs`

Suppose you have:

```text
file1.txt

file2.txt

file3.txt
```

Delete them:

```bash
find . -name "*.txt" | xargs rm
```

!!! warning "Warning"

    Use carefully.

Preview first:

```bash
find . -name "*.txt"
```

---

# Complex Pipeline Example

Display running Docker containers.

```bash
docker ps | grep nginx | wc -l
```

Workflow:

```text
List Containers

↓

Find nginx

↓

Count Matches
```

---

# Another Example

Count running Kubernetes Pods.

```bash
kubectl get pods | grep Running | wc -l
```

---

# Real Production Examples

Find failed services.

```bash
systemctl --failed | less
```

Search logs.

```bash
journalctl | grep ERROR
```

Find listening ports.

```bash
ss -tuln | grep 443
```

Display top memory consumers.

```bash
ps aux | sort -rk4 | head -10
```

Count active users.

```bash
who | wc -l
```

Find SSH login attempts.

```bash
journalctl | grep ssh
```

---

# Visual Pipeline

```text
Application Logs

↓

grep ERROR

↓

sort

↓

uniq

↓

wc -l

↓

Total Errors
```

---

# Command Summary

| Pipeline | Purpose |
|-----------|----------|
| `ls \| wc -l` | Count files |
| `ps -ef \| grep ssh` | Search process |
| `cat file \| sort` | Sort data |
| `sort file \| uniq` | Remove duplicates |
| `history \| grep docker` | Search history |
| `journalctl \| less` | Read logs |
| `find . \| xargs` | Process search results |

---

# Production Perspective

Pipes are everywhere.

Docker

```bash
docker ps | grep redis
```

Kubernetes

```bash
kubectl get pods | grep Running
```

Git

```bash
git log | head
```

Linux

```bash
ps aux | grep nginx
```

Networking

```bash
ss -tuln | grep 22
```

Monitoring

```bash
journalctl | grep CRITICAL
```

Every DevOps engineer uses pipelines daily.

---

# Hands-on Lab

## Task 1

Count files.

```bash
ls | wc -l
```

---

## Task 2

Display first five entries.

```bash
ls -l | head -5
```

---

## Task 3

Display last five entries.

```bash
ls -l | tail -5
```

---

## Task 4

Create sample file.

```bash
cat > employees.txt
```

Add:

```text
Alice

Bob

Charlie

Alice

David
```

Press:

```text
Ctrl + D
```

---

## Task 5

Sort.

```bash
cat employees.txt | sort
```

---

## Task 6

Remove duplicates.

```bash
sort employees.txt | uniq
```

---

## Task 7

Count duplicates.

```bash
sort employees.txt | uniq -c
```

---

## Task 8

Search history.

```bash
history | grep ls
```

---

## Task 9

Save and display output.

```bash
ls | tee files.txt
```

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    An NGINX server is experiencing intermittent failures.

Tasks:

1. Find the NGINX process.
2. Display only error logs.
3. Count the number of error entries.
4. Save filtered errors to a file.
5. Display and save the output simultaneously.

Solutions:

```bash
ps -ef | grep nginx

journalctl | grep ERROR

journalctl | grep ERROR | wc -l

journalctl | grep ERROR > errors.log

journalctl | grep ERROR | tee errors.log
```

---

# Mini Challenge

Create a file named:

```text
servers.txt
```

Contents:

```text
server01

server03

server02

server01

server04

server02
```

Now:

- Sort the file.
- Remove duplicates.
- Count unique servers.
- Save sorted output.
- Display the first three entries.
- Display the last two entries.

Use only pipes and commands you've learned.

---

# Best Practices

- Use pipes instead of temporary files whenever possible.
- Keep pipelines readable.
- Test each command individually before combining them.
- Use `tee` when you need to both save and view output.
- Filter data early to improve performance.

---

# Common Mistakes

❌ Creating unnecessary temporary files.

✅ Instead of:

```bash
ls > files.txt

cat files.txt
```

Use:

```bash
ls | less
```

---

❌ Building very long pipelines without testing.

✅ Test each stage before combining them.

---

❌ Forgetting that pipes transfer only **stdout**.

✅ If you also need **stderr**, redirect it appropriately.

---

# Interview Questions
## Beginner

1. What is a pipe?
2. What does the `|` symbol do?
3. What is the difference between a pipe and redirection?
4. Which command counts lines?

---

## Intermediate

1. Explain how pipes work internally.
2. Why are pipes preferred over temporary files?
3. Explain `sort | uniq`.
4. What does `tee` do in a pipeline?

---

## Architect Level

1. How do pipes simplify Linux automation?
2. How would you analyze millions of log entries using pipelines?
3. Why are pipelines fundamental to DevOps workflows?

---

# Summary

In this lesson, you learned:

- What pipes are
- How pipelines work
- Combining Linux commands
- Filtering and processing command output
- Using `sort`, `uniq`, `wc`, `grep`, `head`, `tail`, and `tee` with pipes
- Production-ready command pipelines

Pipes are one of Linux's most elegant features. By combining simple commands, you can perform complex tasks efficiently without writing custom programs.

---

## Key Takeaways

- Pipes connect the output of one command to the input of another.
- Pipelines eliminate the need for temporary files.
- Combining simple commands creates powerful workflows.
- Pipes are heavily used in Linux administration, DevOps, and Cloud Engineering.
- Mastering pipelines significantly improves productivity and troubleshooting skills.

---

## What's Next?

**[Module 2 Summary — Linux Command Line Essentials](module-2-linux-command-line-essentials-summary.md)**

In the next lesson, you'll:

- Review all key concepts from Module 2
- Complete a hands-on assessment
- Test your knowledge with quizzes
- Solve production-focused challenges
- Prepare for Module 3: Text Processing
