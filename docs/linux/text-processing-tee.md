---
title: "tee Command — Writing Output to Both Screen and File"
description: "Write stdout to the terminal and files with tee — append, multiple files, 2>&1 logging, and DevOps/CI/CD pipeline patterns."
difficulty: intermediate
estimated_time: "30 min"
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
  - tee
  - text-processing
  - pipelines
  - rebash-linux-mastery
comments: false
status: ready
---

# tee Command — Writing Output to Both Screen and File

> The `tee` command reads data from standard input and writes it simultaneously to the terminal and one or more files. It is an essential Linux utility for logging command output, debugging shell scripts, monitoring automation, and building CI/CD pipelines.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 3: Text Processing → Lesson 14</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 30 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Text Processing</div>

<div markdown>**Lesson:** 14 of 18</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `tee` command
- Save command output while displaying it
- Append output to files
- Write to multiple files
- Use `tee` in shell pipelines
- Log automation output
- Apply `tee` in DevOps and CI/CD workflows

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 Lessons 1–13

---

# Why Learn tee?

Normally:

```bash
ls > files.txt
```

Output goes to the file.

Nothing appears on the screen.

Or:

```bash
ls
```

Output appears on the screen.

Nothing is saved.

What if you need **both**?

```bash
ls | tee files.txt
```

Now you can:

- View the output
- Save it to a file

At the same time.

---

# What is tee?

The `tee` command copies its input to:

- Standard Output (Terminal)
- One or more files

Syntax:

```bash
tee [OPTIONS] FILE...
```

Think of it as a **T-junction** in a pipe.

```text
Command
   │
   ▼
  tee
 ┌──┴──┐
 ▼     ▼
Screen File
```

---

# Basic Usage

```bash
echo "Welcome to REBASH Academy" | tee output.txt
```

Output on screen:

```text
Welcome to REBASH Academy
```

File:

```bash
cat output.txt
```

Output:

```text
Welcome to REBASH Academy
```

---

# Save Command Output

```bash
ls -l | tee files.txt
```

You will see the directory listing while also saving it.

---

# Append Instead of Overwrite

Normally:

```bash
tee output.txt
```

overwrites the file.

Append instead:

```bash
echo "Docker" | tee -a output.txt
```

View:

```bash
cat output.txt
```

Output:

```text
Linux

Docker
```

---

# Write to Multiple Files

```bash
echo "Cloud Computing" | tee file1.txt file2.txt file3.txt
```

All files receive the same output.

---

# Use with grep

Save matching lines.

```bash
grep ERROR application.log | tee errors.log
```

Display:

```text
ERROR Database Connection Failed
```

The same output is saved to `errors.log`.

---

# Use with sort

```bash
sort employees.txt | tee sorted.txt
```

---

# Use with wc

```bash
cat access.log | tee backup.log | wc -l
```

Workflow:

```text
access.log
      │
      ▼
     tee
   ↙     ↘
backup.log  wc -l
```

---

# Use with find

```bash
find . -name "*.sh" | tee scripts.txt
```

---

# Logging Script Output

```bash
./backup.sh | tee backup.log
```

You can monitor progress in real time while keeping a log for later review.

---

# Capture Both Standard Output and Errors

Normally, `tee` captures only standard output.

To capture both:

```bash
command 2>&1 | tee output.log
```

Example:

```bash
ls /existing /missing 2>&1 | tee result.log
```

Output on screen:

```text
/existing

ls: cannot access '/missing': No such file or directory
```

The same content is saved to `result.log`.

---

# Ignore Interrupt Signals

Useful for long-running processes.

```bash
tee -i output.log
```

The `-i` option ignores interrupt signals (`Ctrl+C`) sent to `tee`.

---

# Common tee Options

| Option | Description |
|----------|-------------|
| `-a` | Append instead of overwrite |
| `-i` | Ignore interrupt signals |

---

# Combining with Other Commands

Monitor disk usage.

```bash
df -h | tee disk-report.txt
```

Save running processes.

```bash
ps -ef | tee processes.txt
```

Save Kubernetes Pods.

```bash
kubectl get pods | tee pods.txt
```

Save Docker containers.

```bash
docker ps | tee containers.txt
```

Save environment variables.

```bash
printenv | tee env.txt
```

---

# Real Production Examples

Save deployment logs.

```bash
kubectl apply -f deployment.yaml | tee deployment.log
```

Save Terraform output.

```bash
terraform apply | tee terraform.log
```

Save Ansible execution.

```bash
ansible-playbook site.yml | tee ansible.log
```

Save Helm installation.

```bash
helm install myapp chart/ | tee helm.log
```

Save Docker build logs.

```bash
docker build -t app . | tee build.log
```

---

# Production Perspective

The `tee` command is one of the most frequently used utilities in:

- CI/CD pipelines
- DevOps automation
- System administration
- Deployment scripts
- Infrastructure provisioning
- Production troubleshooting

It allows engineers to monitor commands while simultaneously creating logs for auditing and debugging.

---

# Hands-on Lab

## Task 1

Display and save text.

```bash
echo "Linux" | tee linux.txt
```

---

## Task 2

Append another line.

```bash
echo "Docker" | tee -a linux.txt
```

---

## Task 3

Display the file.

```bash
cat linux.txt
```

---

## Task 4

Save directory listing.

```bash
ls -l | tee files.txt
```

---

## Task 5

Save process list.

```bash
ps -ef | tee processes.txt
```

---

## Task 6

Write to multiple files.

```bash
echo "REBASH Academy" | tee file1.txt file2.txt
```

---

## Task 7

Capture both output and errors.

```bash
ls /tmp /invalid 2>&1 | tee errors.log
```

---

## Task 8

Count files while saving the list.

```bash
ls | tee listing.txt | wc -l
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `tee file` | Save output | Reports |
| `tee -a` | Append logs | Automation |
| `tee file1 file2` | Multiple outputs | Backups |
| `2>&1 \| tee` | Capture stdout + stderr | Troubleshooting |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A DevOps engineer is deploying an application to Kubernetes.

Tasks:

1. Watch deployment progress live.
2. Save deployment logs.
3. Capture errors.
4. Share the log with the support team.

Solution:

```bash
kubectl apply -f deployment.yaml 2>&1 | tee deployment.log
```

Benefits:

- Live monitoring
- Permanent log file
- Easier troubleshooting
- Audit trail

---

# Mini Challenge

Perform the following:

- Save the output of `df -h` while displaying it.
- Save the output of `ps -ef`.
- Append a custom message to an existing log.
- Capture errors from an invalid command.
- Save the list of shell scripts in the current directory.
- Write the same output to two different files.

---

# Best Practices

- Use `tee` in deployment and automation scripts.
- Use `-a` for log files that should be preserved.
- Capture both stdout and stderr using `2>&1`.
- Use descriptive log file names.
- Rotate or archive large log files regularly.

---

# Performance Tip

For long-running commands that produce continuous output:

```bash
tail -f application.log | tee live-monitor.log
```

This allows real-time monitoring while creating a persistent copy for later analysis.

---

# Common Mistakes

❌ Forgetting `-a`.

✅ Without `-a`, the file is overwritten.

Incorrect:

```bash
echo "New Entry" | tee log.txt
```

Correct:

```bash
echo "New Entry" | tee -a log.txt
```

---

❌ Assuming `tee` captures error output automatically.

✅ Incorrect:

```bash
command | tee output.log
```

Correct:

```bash
command 2>&1 | tee output.log
```

---

❌ Using `tee` without considering log file growth.

✅ Regularly rotate or clean up logs in long-running systems.

---

# Interview Questions
## Beginner

1. What is the purpose of the `tee` command?
2. How do you append output to a file?
3. How do you write to multiple files?
4. Why is `tee` useful in pipelines?

---

## Intermediate

1. Explain the difference between `>` and `tee`.
2. How do you capture both standard output and standard error?
3. What does the `-i` option do?
4. Why is `tee` commonly used in shell scripts?

---

## Architect Level

1. How would you log a Kubernetes deployment while monitoring it live?
2. Why is `tee` valuable in CI/CD pipelines?
3. How would you design a deployment script that logs every step without hiding console output?

---

# Summary

In this lesson, you learned:

- Displaying and saving output simultaneously
- Appending to log files
- Writing to multiple files
- Capturing errors
- Using `tee` in shell pipelines
- Real-world DevOps and automation use cases

The `tee` command is a simple yet powerful utility that bridges the gap between visibility and logging. It is widely used in Linux administration, automation, CI/CD, and production troubleshooting.

---

## Key Takeaways

- `tee` writes output to both the terminal and files.
- Use `-a` to append instead of overwrite.
- Use `2>&1 | tee` to capture both standard output and errors.
- `tee` integrates naturally with pipelines.
- It is a standard tool for logging deployments, builds, and automation tasks.

---

## What's Next?

**[xargs Command — Building Powerful Command Pipelines in Linux](text-processing-xargs.md)**

In the next lesson, you'll learn:

- Passing input as command arguments
- Running commands on multiple files
- Combining `find` with `xargs`
- Parallel execution
- Production automation examples
