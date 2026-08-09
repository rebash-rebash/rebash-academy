---
title: "cat Command"
description: "View, create, concatenate, and redirect text files with cat — options for line numbers, hidden characters, and production pipelines."
difficulty: beginner
estimated_time: "20 min"
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
  - cat
  - text-processing
  - command-line
  - rebash-linux-mastery
comments: false
status: ready
---

# cat Command

> The `cat` (concatenate) command is one of the most frequently used Linux utilities for viewing, creating, combining, and redirecting text files. Although simple, it plays an important role in shell scripting, automation, and system administration.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 3: Text Processing → Lesson 1</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 20 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Text Processing</div>

<div markdown>**Lesson:** 1 of 18</div>

</div>

</div>

---

# What You'll Learn

By the end of this lesson, you'll be able to:

- Understand the purpose of the `cat` command
- Display file contents
- Create files using `cat`
- Concatenate multiple files
- Display line numbers
- Redirect output using `cat`
- Use `cat` in command pipelines
- Apply `cat` in real-world administration tasks

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials

---

# What is `cat`?

`cat` stands for:

> **Concatenate**

Originally, it was designed to join multiple files together.

Today, it is commonly used to:

- View file contents
- Create text files
- Merge files
- Redirect output
- Feed data into pipelines

---

# Command Syntax

```bash
cat [OPTIONS] FILE...
```

---

# Display File Contents

Create a file.

```bash
echo "Welcome to REBASH Academy" > notes.txt
```

Display:

```bash
cat notes.txt
```

Output:

```text
Welcome to REBASH Academy
```

---

# Display Multiple Files

```bash
cat file1.txt file2.txt
```

Output:

```text
Contents of file1

Contents of file2
```

---

# Concatenate Files

Merge files into another file.

```bash
cat part1.txt part2.txt > complete.txt
```

View:

```bash
cat complete.txt
```

---

# Create a File Using cat

```bash
cat > users.txt
```

Type:

```text
Alice

Bob

Charlie
```

Press:

```text
Ctrl + D
```

Display:

```bash
cat users.txt
```

---

# Append to a File

```bash
cat >> users.txt
```

Add:

```text
David
```

Press:

```text
Ctrl + D
```

---

# Display Line Numbers

```bash
cat -n users.txt
```

Example:

```text
1 Alice

2 Bob

3 Charlie

4 David
```

---

# Display Non-Blank Line Numbers

```bash
cat -b users.txt
```

Blank lines are ignored.

---

# Show Tabs

```bash
cat -T sample.txt
```

Tabs appear as:

```text
^I
```

Useful for debugging configuration files.

---

# Show End of Line

```bash
cat -E sample.txt
```

Example:

```text
Linux$

Docker$

Kubernetes$
```

---

# Show Hidden Characters

```bash
cat -A sample.txt
```

Displays:

- Tabs
- Line endings
- Non-printable characters

Useful when troubleshooting malformed configuration files.

---

# Number All Lines

```bash
cat -n /etc/passwd
```

---

# Combine with Other Commands

Count lines.

```bash
cat users.txt | wc -l
```

Search.

```bash
cat users.txt | grep Bob
```

Sort.

```bash
cat users.txt | sort
```

Remove duplicates.

```bash
cat users.txt | sort | uniq
```

---

# Production Examples

View SSH configuration.

```bash
cat /etc/ssh/sshd_config
```

Display hosts file.

```bash
cat /etc/hosts
```

View Docker Compose file.

```bash
cat docker-compose.yml
```

View Kubernetes manifest.

```bash
cat deployment.yaml
```

View application configuration.

```bash
cat application.properties
```

---

# Production Perspective

Linux administrators frequently use `cat` to:

- Read configuration files
- Verify deployment manifests
- Display scripts
- Combine configuration fragments
- Feed text into pipelines

Although `cat` is simple, it appears in countless shell scripts and automation workflows.

---

# Hands-on Lab

## Task 1

Create a file.

```bash
cat > linux.txt
```

Add:

```text
Linux

Docker

Kubernetes
```

Press:

```text
Ctrl + D
```

---

## Task 2

Display the file.

```bash
cat linux.txt
```

---

## Task 3

Display line numbers.

```bash
cat -n linux.txt
```

---

## Task 4

Append another line.

```bash
cat >> linux.txt
```

Add:

```text
Terraform
```

---

## Task 5

Create another file.

```bash
echo "Ansible" > tools.txt
```

---

## Task 6

Merge both files.

```bash
cat linux.txt tools.txt > complete.txt
```

---

## Task 7

Count lines.

```bash
cat complete.txt | wc -l
```

---

## Task 8

Search.

```bash
cat complete.txt | grep Docker
```

---

# Command Deep Dive

| Option | Description |
|----------|-------------|
| `cat file` | Display file |
| `-n` | Number all lines |
| `-b` | Number non-empty lines |
| `-E` | Show line endings |
| `-T` | Show tabs |
| `-A` | Show all hidden characters |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A web server is failing after a configuration change.

Tasks:

- View the NGINX configuration.
- Display line numbers.
- Search for the `server` directive.
- Count the number of configuration lines.

Example:

```bash
cat -n /etc/nginx/nginx.conf

cat /etc/nginx/nginx.conf | grep server

cat /etc/nginx/nginx.conf | wc -l
```

---

# Best Practices

- Use `cat` for small files.
- Use `less` for large files.
- Combine `cat` with pipes for text processing.
- Use `cat -n` when discussing configuration files.
- Avoid using `cat` on very large log files.

---

# Common Mistakes

❌ Using `cat` on huge log files.

✅ Instead:

```bash
less logfile.log
```

or

```bash
tail -f logfile.log
```

---

❌ Creating unnecessary pipelines.

✅ Instead of:

```bash
cat file.txt | grep Linux
```

You can simply write:

```bash
grep Linux file.txt
```

This is more efficient.

---

# Interview Questions
## Beginner

1. What does `cat` stand for?
2. How do you display a file?
3. How do you merge two files?
4. Which option shows line numbers?

---

## Intermediate

1. Explain `cat -A`.
2. When should you use `cat` instead of `less`?
3. Why is `grep file.txt` generally preferred over `cat file.txt | grep`?

---

## Architect Level

1. Why is `cat` commonly seen in shell scripts?
2. How would you inspect a production configuration file safely?
3. When does using `cat` become inefficient?

---

# Summary

In this lesson, you learned:

- Viewing files
- Creating files
- Appending text
- Merging files
- Displaying line numbers
- Using `cat` in pipelines
- Production use cases

Although simple, `cat` is one of the most frequently used Linux commands and serves as the foundation for more advanced text-processing techniques.

---

## Key Takeaways

- `cat` stands for **concatenate**.
- It can display, create, append, and combine files.
- `cat -n` displays line numbers.
- `cat` integrates seamlessly with pipes and redirection.
- Prefer `less` for large files.

---

## What's Next?

**[grep Command — Searching Text in Linux](text-processing-grep.md)**

In the next lesson, you'll learn:

- Basic and advanced text searching
- Regular expressions
- Recursive search
- Case-insensitive search
- Counting matches
- Production log analysis
