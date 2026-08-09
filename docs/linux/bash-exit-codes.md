---
title: "Exit Codes — Understanding Command Success and Failure in Bash"
description: "Use Bash exit codes — $?, exit, return, standard status values, and CI/CD-friendly failure handling in production scripts."
difficulty: intermediate
estimated_time: "75 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 10 · Bash Scripting"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - bash
  - scripting
  - exit-codes
  - automation
  - rebash-linux-mastery
comments: false
status: ready
---

# Exit Codes — Understanding Command Success and Failure in Bash

> **Exit Codes** are numeric values returned by commands, scripts, and functions to indicate whether an operation succeeded or failed. Every Linux command returns an exit code when it finishes execution. Bash scripts use these codes to detect failures, make decisions, trigger error handling, and integrate with automation tools such as Jenkins, GitLab CI/CD, GitHub Actions, Kubernetes Jobs, and Ansible. Understanding exit codes is essential for writing reliable, production-ready Bash scripts.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 10: Bash Scripting → Lesson 7</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 75 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Bash Scripting</div>

<div markdown>**Lesson:** 7 of 11</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand exit codes
- Interpret command status
- Use the `exit` command
- Check exit codes using `$?`
- Return exit codes from functions
- Use exit codes in conditional statements
- Apply exit codes in production automation

---

# Prerequisites

Complete:

- Modules 1–9
- Module 10 Lessons 1–6

---

# Why Learn Exit Codes?

Imagine deploying an application.

Without checking the exit code:

```bash
kubectl apply -f deployment.yaml

echo "Deployment Successful"
```

Even if the deployment fails, the script reports success.

Using exit codes:

```bash
kubectl apply -f deployment.yaml

if [ $? -eq 0 ]
then
    echo "Deployment Successful"
else
    echo "Deployment Failed"
fi
```

The script accurately reports the outcome.

---

# What is an Exit Code?

An exit code is a numeric value returned by a command after execution.

```text
Command

↓

Execution

↓

Exit Code
```

The shell stores the exit code of the most recently executed command.

---

# Standard Exit Codes

| Exit Code | Meaning |
|-----------|---------|
| `0` | Success |
| Non-zero | Failure |
| `1` | General error |
| `2` | Incorrect command usage |
| `126` | Command cannot execute |
| `127` | Command not found |
| `130` | Script terminated by Ctrl+C |

---

# Viewing the Exit Code

Use the special variable:

```bash
$?
```

Example:

```bash
ls

echo $?
```

Output:

```text
0
```

---

# Successful Command

```bash
mkdir demo

echo $?
```

Output:

```text
0
```

---

# Failed Command

```bash
ls nonexistent

echo $?
```

Output:

```text
2
```

---

# Using Exit Codes in Conditions

```bash
mkdir project

if [ $? -eq 0 ]
then
    echo "Directory Created"
else
    echo "Creation Failed"
fi
```

---

# Better Approach

Instead of checking `$?` separately:

```bash
if mkdir project
then
    echo "Directory Created"
else
    echo "Creation Failed"
fi
```

This is cleaner and more readable.

---

# Using the exit Command

Terminate a script with a specific exit code.

```bash
exit 0
```

Success.

```bash
exit 1
```

Failure.

---

# Example Script

```bash
#!/bin/bash

if [ ! -f "/etc/passwd" ]
then
    echo "File Missing"

    exit 1
fi

echo "File Found"

exit 0
```

---

# Custom Exit Codes

You may define custom exit codes for different situations.

Example:

```bash
exit 10
```

```bash
exit 20
```

```bash
exit 50
```

Document custom exit codes clearly so other users understand their meaning.

---

# Exit Codes in Functions

Functions return status codes.

```bash
check_file() {

    [ -f "$1" ]

    return $?
}
```

Call the function.

```bash
check_file file.txt

echo $?
```

---

# Common Commands

View exit code.

```bash
echo $?
```

Exit successfully.

```bash
exit 0
```

Exit with failure.

```bash
exit 1
```

Return from function.

```bash
return 0
```

---

# Real Production Examples

Check deployment.

```bash
kubectl apply -f app.yaml

if [ $? -eq 0 ]
then
    echo "Deployment Successful"
else
    echo "Deployment Failed"
fi
```

Check backup.

```bash
tar -czf backup.tar.gz /data

if [ $? -ne 0 ]
then
    exit 1
fi
```

Restart service.

```bash
systemctl restart nginx

if systemctl is-active --quiet nginx
then
    echo "Service Running"
else
    exit 1
fi
```

---

# Production Perspective

Exit codes are heavily used in:

- Bash automation
- CI/CD pipelines
- Kubernetes Jobs
- Ansible playbooks
- Jenkins pipelines
- GitLab CI/CD
- Monitoring scripts
- Deployment automation

Most automation platforms rely on exit codes to determine whether a task succeeded or failed.

---

# Hands-on Lab

## Task 1

Run a successful command.

```bash
pwd
```

Display the exit code.

```bash
echo $?
```

---

## Task 2

Run a failed command.

```bash
ls missing-file
```

Display the exit code.

```bash
echo $?
```

---

## Task 3

Create a script.

```bash
#!/bin/bash

echo "Success"

exit 0
```

Run it.

```bash
echo $?
```

---

## Task 4

Create a script that fails.

```bash
#!/bin/bash

echo "Failure"

exit 1
```

---

## Task 5

Check command success.

```bash
if mkdir demo
then
    echo "Created"
else
    echo "Failed"
fi
```

---

## Task 6

Create a function.

```bash
check() {

    return 0
}

check

echo $?
```

---

## Task 7

Return a failure code.

```bash
return 1
```

---

## Task 8

Exit the script when a required file is missing.

```bash
if [ ! -f config.yaml ]
then
    exit 1
fi
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `echo $?` | Display last exit code | Troubleshooting |
| `exit` | Exit script | Automation |
| `return` | Return function status | Modular scripts |
| `if` | Check command success | Deployment validation |
| `&&` | Execute next command on success | Chained automation |
| `||` | Execute next command on failure | Error recovery |

---

# Common Exit Code Mistakes

| Mistake | Solution |
|----------|----------|
| Ignoring exit codes | Always check critical commands |
| Checking `$?` too late | Check immediately after the command |
| Using `return` outside a function | Use `exit` in scripts |
| Returning strings with `return` | Return only numeric values |
| Assuming every non-zero code has the same meaning | Understand common exit codes |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A CI/CD pipeline reports a successful deployment, but the application is unavailable.

Investigation:

The deployment command failed.

```bash
kubectl apply -f deployment.yaml
```

The script ignored the exit code and continued.

Solution:

```bash
if kubectl apply -f deployment.yaml
then
    echo "Deployment Successful"
else
    echo "Deployment Failed"

    exit 1
fi
```

The pipeline now correctly reports failures and stops further execution.

---

# Best Practices

- Check the exit status of important commands.
- Exit immediately when critical operations fail.
- Use meaningful exit codes.
- Return status codes from functions.
- Prefer `if command` over checking `$?` separately.
- Document custom exit codes.

---

# Common Mistakes

❌ Ignoring failed commands.

✅ Always review failed commands.

---

❌ Checking `$?` after executing another command.

✅ Avoid this mistake: checking `$?` after executing another command.

---

❌ Using `return` instead of `exit` in the main script.

✅ Prefer `exit` in the main script rather than using `return`.

---

❌ Returning text instead of numeric status codes.

✅ Prefer numeric status codes rather than returning text.

---

❌ Continuing execution after critical failures.

✅ Do not continue execution after critical failures.

---

# Interview Questions
## Beginner

1. What is an exit code?
2. What does exit code `0` mean?
3. How do you display the last exit code?
4. What does the `exit` command do?

---

## Intermediate

1. What is the difference between `exit` and `return`?
2. Why should you check exit codes in scripts?
3. Why is `if command` preferred over checking `$?` separately?
4. What does exit code `127` indicate?

---

## Architect Level

1. How do exit codes improve CI/CD pipeline reliability?
2. How would you design Bash scripts to fail safely?
3. How should custom exit codes be used in enterprise automation?

---

# Summary

In this lesson, you learned:

- Exit codes
- Standard Linux exit codes
- The `exit` command
- The `$?` variable
- Returning status codes from functions
- Using exit codes in conditions
- Production scripting best practices

Exit codes provide a standardized way for commands, functions, and scripts to communicate success or failure. Proper use of exit codes allows automation tools and other scripts to make informed decisions, improving the reliability and maintainability of production systems.

---

## Key Takeaways

- Every Linux command returns an exit code.
- `0` indicates success; non-zero values indicate failure.
- Use `echo $?` to view the last exit code.
- Use `exit` to terminate scripts with a status.
- Use `return` to return status codes from functions.
- Always check exit codes for critical operations.

---

## What's Next?

**[Error Handling — Building Reliable Bash Scripts](bash-error-handling.md)**

You'll explore:

- Handling runtime errors
- Using `set` options (`-e`, `-u`, `-o pipefail`)
- Error messages
- Cleanup operations with `trap`
- Defensive scripting techniques
- Debugging failures
- Production error handling best practices

By the end of the lesson, you'll be able to build resilient Bash scripts that detect errors, recover gracefully where appropriate, and fail safely when necessary.
