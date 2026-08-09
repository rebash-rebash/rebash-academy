---
title: "Input, Output, Pipes, and Redirection"
description: "Master stdin, stdout, stderr, redirection, pipes, and tee to build Linux command pipelines for automation and troubleshooting."
difficulty: intermediate
estimated_time: "35 min"
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
  - redirection
  - pipes
  - bash
  - command-line
  - rebash-linux-mastery
comments: false
status: ready
---

# Input, Output, Pipes, and Redirection

> One of the most powerful features of Linux is the ability to redirect input and output between commands and files. Redirection and pipes allow you to combine simple commands into powerful workflows, making automation, troubleshooting, and data processing much more efficient.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 2: Linux Command Line Essentials → Lesson 9</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 35 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Linux Command Line Essentials</div>

<div markdown>**Lesson:** 9 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Standard Input, Output, and Error
- Redirect command output to files
- Append output to existing files
- Redirect errors
- Combine commands using pipes
- Use the `tee` command
- Build powerful Linux command pipelines

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 Lessons 1–8

---

# Why Learn Redirection?

Imagine you run a command that produces thousands of lines.

Instead of displaying everything on the screen, you can:

- Save it to a file
- Send it to another command
- Filter the results
- Ignore errors
- Build automation workflows

Almost every shell script and DevOps pipeline uses redirection.

---

# Standard Streams

Every Linux process has three standard data streams.

| Stream | Number | Purpose |
|----------|---------|---------|
| Standard Input | 0 | Receives input |
| Standard Output | 1 | Displays normal output |
| Standard Error | 2 | Displays error messages |

Visual representation:

```text
          Keyboard
             │
             ▼
         Standard Input (0)
             │
             ▼
         Linux Command
          │         │
          ▼         ▼
 Standard Output   Standard Error
      (1)               (2)
```

---

# Standard Output (`stdout`)

Example:

```bash
echo "Hello Linux"
```

Output:

```text
Hello Linux
```

Normally, output is displayed on the terminal.

---

# Redirect Output (`>`)

Save output to a file.

```bash
echo "Linux" > notes.txt
```

Check:

```bash
cat notes.txt
```

Output:

```text
Linux
```

!!! warning "Important"

    If the file already exists:

```bash
echo "Docker" > notes.txt
```

The existing contents are overwritten.

---

# Append Output (`>>`)

Append instead of overwrite.

```bash
echo "Kubernetes" >> notes.txt
```

Now:

```bash
cat notes.txt
```

Output:

```text
Linux
Kubernetes
```

---

# Standard Error (`stderr`)

Example:

```bash
ls file-does-not-exist
```

Output:

```text
ls: cannot access 'file-does-not-exist'
```

This message is sent to **Standard Error (2)**.

---

# Redirect Errors

Save only errors.

```bash
ls missing.txt 2> errors.log
```

View:

```bash
cat errors.log
```

---

Append errors.

```bash
ls missing.txt 2>> errors.log
```

---

# Redirect Output and Errors Together

```bash
command > output.log 2>&1
```

Example:

```bash
ls existing.txt missing.txt > result.log 2>&1
```

Both normal output and errors go into one file.

---

# Discard Output

Linux provides a special device:

```text
/dev/null
```

Anything sent here disappears.

Ignore output.

```bash
ls > /dev/null
```

Ignore errors.

```bash
ls missing.txt 2> /dev/null
```

Ignore everything.

```bash
command > /dev/null 2>&1
```

---

# Standard Input (`stdin`)

Many commands accept input.

Example:

```bash
sort < names.txt
```

Instead of typing manually, the file becomes the command's input.

---

# Pipes (`|`)

A pipe sends the output of one command directly into another command.

Syntax:

```bash
command1 | command2
```

Visual representation:

```text
Command 1

↓

Output

↓

Pipe

↓

Command 2
```

---

# Pipe Example

Display only the first five files.

```bash
ls | head -5
```

---

Count files.

```bash
ls | wc -l
```

---

Search for a process.

```bash
ps -ef | grep ssh
```

---

Sort output.

```bash
cat users.txt | sort
```

---

Count matching lines.

```bash
cat users.txt | grep admin | wc -l
```

---

# The tee Command

Normally:

```bash
echo "Hello"
```

displays output.

Using:

```bash
echo "Hello" | tee output.txt
```

Result:

- Displays output
- Saves output

Append:

```bash
echo "Docker" | tee -a output.txt
```

---

# Combining Multiple Pipes

Linux allows multiple pipes.

Example:

```bash
cat access.log | grep ERROR | sort | uniq | wc -l
```

Workflow:

```text
Read Log

↓

Filter ERROR

↓

Sort

↓

Remove Duplicates

↓

Count
```

This is one of Linux's greatest strengths.

---

# Input and Output Flow

```text
stdin (0)

↓

Command

↓

stdout (1)

↓

Pipe or File

↓

Another Command

↓

Result
```

---

# Real Production Examples

Display running Docker containers.

```bash
docker ps | grep nginx
```

Count Kubernetes Pods.

```bash
kubectl get pods | wc -l
```

Find failed services.

```bash
systemctl --failed | less
```

Search logs.

```bash
cat /var/log/syslog | grep ERROR
```

Save process list.

```bash
ps -ef > processes.txt
```

Monitor logs while saving.

```bash
tail -f app.log | tee app-output.log
```

---

# Production Perspective

Every DevOps engineer uses pipes and redirection.

Examples:

Terraform

```bash
terraform plan > plan.txt
```

Kubernetes

```bash
kubectl get pods | grep Running
```

Docker

```bash
docker logs container | less
```

Git

```bash
git log | head
```

System Administration

```bash
journalctl | grep ssh
```

---

# Hands-on Lab

## Task 1

Redirect output.

```bash
echo "Linux" > linux.txt
```

---

## Task 2

Append.

```bash
echo "Docker" >> linux.txt
```

---

## Task 3

Display.

```bash
cat linux.txt
```

---

## Task 4

Redirect error.

```bash
ls missing.txt 2> error.log
```

---

## Task 5

View errors.

```bash
cat error.log
```

---

## Task 6

Count files.

```bash
ls | wc -l
```

---

## Task 7

Display first five entries.

```bash
ls | head -5
```

---

## Task 8

Use tee.

```bash
date | tee today.txt
```

---

## Task 9

Search.

```bash
history | grep docker
```

---

# Command Deep Dive

| Symbol / Command | Purpose | Example |
|------------------|---------|---------|
| `>` | Overwrite output | `ls > files.txt` |
| `>>` | Append output | `date >> log.txt` |
| `2>` | Redirect errors | `ls missing 2> error.log` |
| `2>>` | Append errors | `ls missing 2>> error.log` |
| `2>&1` | Combine stdout and stderr | `command > all.log 2>&1` |
| `<` | Redirect input | `sort < names.txt` |
| `\|` | Pipe output | `ps -ef \| grep ssh` |
| `tee` | Display and save output | `date \| tee log.txt` |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    An application has stopped working.

Tasks:

1. Save running processes to a file.
2. Search for the application process.
3. Count running services.
4. Save error logs.
5. Monitor logs while writing them to another file.

Solutions:

```bash
ps -ef > processes.txt

ps -ef | grep nginx

systemctl list-units | wc -l

journalctl -p err > errors.log

tail -f app.log | tee monitor.log
```

---

# Mini Challenge

Create a file named:

```text
employees.txt
```

Add:

```text
Alice

Bob

Charlie

David

Alice
```

Perform the following:

- Sort the file.
- Remove duplicate entries.
- Count the number of unique names.
- Save the sorted output to a new file.
- Display the output while saving it.

Hints:

```bash
sort

uniq

wc

tee
```

---

# Best Practices

- Use `>>` when preserving existing data.
- Redirect errors to separate log files during troubleshooting.
- Use pipes instead of creating temporary files whenever possible.
- Use `tee` to monitor output while saving it.
- Understand standard streams before writing shell scripts.

---

# Common Mistakes

❌ Accidentally overwriting files.

✅ Use:

```bash
>
```

Always verify before using.

---

❌ Ignoring error messages.

✅ Redirect errors to a file for analysis.

---

❌ Creating unnecessary temporary files.

✅ Use pipes instead.

---

❌ Forgetting that `2>` redirects only errors.

✅ Use:

```bash
> file 2>&1
```

to capture everything.

---

# Interview Questions
## Beginner

1. What are stdin, stdout, and stderr?
2. What does `>` do?
3. Difference between `>` and `>>`?
4. What is a pipe?

---

## Intermediate

1. Explain `2>` and `2>&1`.
2. What is `/dev/null`?
3. What does the `tee` command do?
4. Why are pipes preferred over temporary files?

---

## Architect Level

1. How do pipes improve Linux automation?
2. How would you capture logs and errors separately in production?
3. Why is understanding standard streams essential for shell scripting?

---

# Summary

In this lesson, you learned:

- Standard Input
- Standard Output
- Standard Error
- Output redirection
- Error redirection
- Pipes
- `tee`
- Linux command pipelines

These concepts are fundamental to Linux automation and shell scripting. Almost every Bash script, CI/CD pipeline, and production troubleshooting workflow relies on redirection and pipes.

---

## Key Takeaways

- Linux uses three standard streams: stdin (0), stdout (1), and stderr (2).
- `>` overwrites a file, while `>>` appends to it.
- `2>` redirects error messages.
- `|` connects the output of one command to another.
- `tee` displays output while simultaneously saving it.
- Combining simple commands with pipes creates powerful automation workflows.

---

## What's Next?

**[Pipes (`|`) in Linux](pipes.md)**

In the final lesson of Module 2, you'll learn:

- What a pipe is
- How pipes work internally
- Connecting multiple Linux commands
- Filtering and processing command output
- Building powerful command pipelines
- Using pipes in real-world administration and DevOps tasks
