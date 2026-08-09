---
title: "sed Command — Stream Editor for Text Processing and Automation"
description: "Search, replace, insert, delete, and edit files with sed — in-place backups, regex, and production DevOps configuration automation."
difficulty: intermediate
estimated_time: "60 min"
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
  - sed
  - text-processing
  - automation
  - rebash-linux-mastery
comments: false
status: ready
---

# sed Command — Stream Editor for Text Processing and Automation

> The `sed` (Stream Editor) command is one of the most powerful text-processing tools in Linux. It allows you to search, replace, insert, delete, transform, and manipulate text without opening a text editor. `sed` is heavily used in Linux administration, DevOps, CI/CD pipelines, automation scripts, and production environments.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 3: Text Processing → Lesson 16</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate → Advanced</div>

<div markdown>**Reading Time:** 60 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Text Processing</div>

<div markdown>**Lesson:** 16 of 18</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand how `sed` works
- Print specific lines
- Search and replace text
- Replace globally
- Edit files in-place
- Delete lines
- Insert and append lines
- Replace using regular expressions
- Process configuration files
- Automate text transformations
- Use `sed` in production DevOps workflows

---

# Prerequisites

Complete:

- Module 1
- Module 2
- Module 3 Lessons 1–15

---

# Why Learn sed?

Imagine you have a configuration file containing **10,000 lines**.

You need to replace:

```text
dev.example.com
```

with

```text
prod.example.com
```

Opening the file manually isn't practical.

Instead:

```bash
sed 's/dev.example.com/prod.example.com/' config.txt
```

Done instantly.

---

# What is sed?

`sed` stands for:

> **Stream Editor**

Unlike editors such as **vim** or **nano**, `sed` processes text **line by line**.

It can:

- Search
- Replace
- Delete
- Insert
- Append
- Print
- Transform

without modifying the original file unless requested.

---

# Command Syntax

```bash
sed [OPTIONS] 'COMMAND' FILE
```

---

# Sample File

Create:

```bash
cat > employees.txt
```

Contents:

```text
Alice Engineering

Bob HR

Charlie Finance

David DevOps

Eve Engineering
```

---

# Display File

```bash
sed '' employees.txt
```

Equivalent to:

```bash
cat employees.txt
```

---

# Print Specific Line

Display line 3.

```bash
sed -n '3p' employees.txt
```

Output:

```text
Charlie Finance
```

---

Display lines 2–4.

```bash
sed -n '2,4p' employees.txt
```

---

# Search and Replace

Replace first occurrence.

```bash
sed 's/Engineering/Cloud/' employees.txt
```

Output:

```text
Alice Cloud

Bob HR

Charlie Finance

David DevOps

Eve Engineering
```

Only the **first occurrence per line** is replaced.

---

# Global Replacement

Replace every occurrence.

```bash
sed 's/Linux/Ubuntu/g'
```

The `g` flag means:

> Global

---

# Replace Only Line 2

```bash
sed '2 s/HR/Human-Resources/' employees.txt
```

---

# Replace Between Lines

```bash
sed '2,4 s/DevOps/SRE/'
```

---

# Ignore Case

```bash
sed 's/linux/ubuntu/i'
```

---

# Edit File In-Place

Normally:

```bash
sed 's/HR/Human Resources/' employees.txt
```

does not change the file.

Modify the file permanently.

```bash
sed -i 's/HR/Human Resources/' employees.txt
```

---

# Create Backup Before Editing

Highly recommended.

```bash
sed -i.bak 's/HR/Human Resources/' employees.txt
```

Creates:

```text
employees.txt

employees.txt.bak
```

---

# Delete Line

Delete line 3.

```bash
sed '3d' employees.txt
```

---

Delete lines 2–4.

```bash
sed '2,4d' employees.txt
```

---

Delete blank lines.

```bash
sed '/^$/d' file.txt
```

---

# Insert Line

Insert before line 2.

```bash
sed '2i\
Department List
' employees.txt
```

---

# Append Line

Append after line 2.

```bash
sed '2a\
Cloud Team
' employees.txt
```

---

# Replace Entire Line

```bash
sed '3c\
Charlie Security
' employees.txt
```

---

# Print Matching Lines

```bash
sed -n '/Engineering/p' employees.txt
```

---

# Delete Matching Lines

```bash
sed '/HR/d' employees.txt
```

---

# Using Regular Expressions

Replace all digits.

```bash
sed 's/[0-9]/X/g'
```

Remove extra spaces.

```bash
sed 's/  */ /g'
```

Replace multiple spaces with one.

---

# Replace Tabs

```bash
sed 's/\t/ /g'
```

---

# Remove Trailing Spaces

```bash
sed 's/[[:space:]]*$//'
```

---

# Number Lines

```bash
sed = employees.txt
```

---

# Using Multiple Commands

```bash
sed -e 's/Linux/Ubuntu/' \
    -e 's/Docker/Podman/'
```

---

# Common sed Options

| Option | Description |
|---------|-------------|
| `-n` | Suppress automatic printing |
| `-i` | Edit file in place |
| `-e` | Multiple expressions |
| `-f` | Read commands from file |

---

# Real Production Examples

Replace image tag.

```bash
sed -i 's/v1.2.0/v1.3.0/' deployment.yaml
```

Update namespace.

```bash
sed -i 's/dev/prod/' deployment.yaml
```

Replace environment.

```bash
sed -i 's/ENV=dev/ENV=prod/'
```

Update Terraform variables.

```bash
sed -i 's/us-central1/us-east1/'
```

Modify NGINX config.

```bash
sed -i 's/listen 80/listen 8080/'
```

---

# Kubernetes Example

Update image.

```bash
sed -i 's/nginx:1.24/nginx:1.27/' deployment.yaml
```

---

# Docker Example

Replace base image.

```bash
sed -i 's/python:3.10/python:3.12/'
```

---

# CI/CD Example

GitLab pipeline.

```bash
sed -i "s/IMAGE_TAG/$CI_COMMIT_SHA/"
```

---

# Production Perspective

Every DevOps engineer uses `sed`.

Typical use cases:

- CI/CD
- Configuration management
- YAML editing
- Log cleanup
- Kubernetes manifests
- Terraform variables
- Helm templates
- Automation scripts

---

# Hands-on Lab

## Task 1

Replace Engineering.

```bash
sed 's/Engineering/Cloud/' employees.txt
```

---

## Task 2

Replace globally.

```bash
sed 's/e/E/g'
```

---

## Task 3

Delete line 2.

```bash
sed '2d' employees.txt
```

---

## Task 4

Print line 4.

```bash
sed -n '4p' employees.txt
```

---

## Task 5

Insert header.

```bash
sed '1i\
Employee Report
'
```

---

## Task 6

Append footer.

```bash
sed '$a\
End of Report
'
```

---

## Task 7

Edit file.

```bash
sed -i 's/HR/Human Resources/'
```

---

## Task 8

Create backup.

```bash
sed -i.bak 's/DevOps/SRE/'
```

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A company has **500 Kubernetes Deployment YAML files** that still reference an old container image:

```yaml
image: nginx:1.24
```

The new approved version is:

```yaml
image: nginx:1.27
```

Update all deployment files safely while keeping backups.

```bash
find . -name "*.yaml" -print0 | \
xargs -0 sed -i.bak 's/nginx:1.24/nginx:1.27/g'
```

---

# Performance Tip

Use `sed` for **stream processing**.

It processes files line by line without loading the entire file into memory, making it suitable for very large log files and configuration files.

---

# Best Practices

- Always test before using `-i`.
- Create backups with `-i.bak`.
- Use regular expressions carefully.
- Validate YAML/JSON after modifications.
- Combine `sed` with `grep`, `find`, and `xargs`.

---

# Common Mistakes

❌ Editing production files without backups.

✅ Always use:

```bash
sed -i.bak
```

---

❌ Forgetting the `g` flag.

✅ Use:

```bash
sed 's/a/b/'
```

Only replaces the first match on each line.

---

❌ Confusing `sed` with `tr`.

✅ - `tr` → Character replacement
- `sed` → Pattern and line-based editing

---

# Interview Questions
## Beginner

1. What does `sed` stand for?
2. How do you replace text?
3. What does `-i` do?
4. What does the `g` flag mean?

---

## Intermediate

1. Explain `sed -n`.
2. Difference between `sed` and `tr`.
3. How do you delete blank lines?
4. How do you create backups before editing?

---

## Architect Level

1. How would you update thousands of Kubernetes manifests automatically?
2. Why is `sed` preferred over manual editing in CI/CD pipelines?
3. How would you safely update configuration files across hundreds of servers?

---

# Summary

In this lesson, you learned:

- Search and replace
- Global replacement
- In-place editing
- Line deletion
- Line insertion
- Appending text
- Regular expressions
- Production automation

`sed` is one of the most important Linux commands for automation and configuration management. It is used extensively in DevOps, cloud engineering, CI/CD, and system administration.

---

## Key Takeaways

- `sed` is a **Stream Editor**.
- It edits text without opening a text editor.
- Use `-i` for in-place editing.
- Use `-i.bak` to create backups.
- `g` performs global replacement.
- `sed` is indispensable for DevOps and automation.

---

## What's Next?

**[awk Command — The Ultimate Linux Text Processing Language](text-processing-awk.md)**

In the next lesson, you'll master field-based processing, calculations, reporting, filtering, and advanced text manipulation using `awk`.
