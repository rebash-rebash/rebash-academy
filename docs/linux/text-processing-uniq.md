---
title: "uniq Command — Removing Duplicate Lines in Linux"
description: "Remove, count, and filter duplicate lines with uniq — always after sort — for log analysis, reports, and Linux data cleanup."
difficulty: intermediate
estimated_time: "25 min"
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
  - uniq
  - text-processing
  - command-line
  - rebash-linux-mastery
comments: false
status: ready
---

# uniq Command — Removing Duplicate Lines in Linux

> The `uniq` command is used to identify, remove, and count duplicate lines in text files. It is commonly used after the `sort` command to clean data, generate reports, analyze logs, and process large datasets. Every Linux Administrator, DevOps Engineer, and Cloud Engineer should know how to use `uniq` effectively.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 3: Text Processing → Lesson 5</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 25 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Text Processing</div>

<div markdown>**Lesson:** 5 of 18</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `uniq` command
- Remove duplicate lines
- Count duplicate entries
- Display only duplicate lines
- Display only unique lines
- Combine `uniq` with `sort`
- Analyze production logs and reports

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 Lessons 1–4

---

# Why Learn uniq?

Imagine you have a log file containing repeated error messages.

```text
ERROR

ERROR

WARNING

INFO

INFO

INFO
```

Instead of manually identifying duplicates:

```bash
sort logfile.txt | uniq
```

Output:

```text
ERROR

INFO

WARNING
```

This is one of the most common Linux data-cleaning operations.

---

# What is uniq?

The `uniq` command filters or reports repeated lines in a text file.

**Important:** `uniq` only works on **adjacent duplicate lines**.

For reliable results, always sort the file first.

Syntax:

```bash
uniq [OPTIONS] FILE
```

---

# Sample File

Create a file.

```bash
cat > fruits.txt
```

Contents:

```text
Apple

Apple

Banana

Banana

Banana

Orange

Orange

Mango
```

Press:

```text
Ctrl + D
```

---

# Remove Duplicate Lines

```bash
uniq fruits.txt
```

Output:

```text
Apple

Banana

Orange

Mango
```

---

# Why sort is Important

Consider:

```text
Apple

Banana

Apple

Orange
```

Command:

```bash
uniq fruits.txt
```

Output:

```text
Apple

Banana

Apple

Orange
```

The duplicate **Apple** is not removed because the duplicate lines are not adjacent.

Correct approach:

```bash
sort fruits.txt | uniq
```

Output:

```text
Apple

Banana

Orange
```

---

# Count Duplicate Lines

```bash
sort fruits.txt | uniq -c
```

Output:

```text
2 Apple

3 Banana

1 Mango

2 Orange
```

The `-c` option prefixes each line with the number of occurrences.

---

# Display Only Duplicate Lines

```bash
sort fruits.txt | uniq -d
```

Output:

```text
Apple

Banana

Orange
```

Only repeated values are displayed.

---

# Display Only Unique Lines

```bash
sort fruits.txt | uniq -u
```

Output:

```text
Mango
```

Only lines that appear once are displayed.

---

# Ignore Case

Create:

```text
Apple

APPLE

apple

Banana
```

Command:

```bash
sort -f fruits.txt | uniq -i
```

Treats uppercase and lowercase letters as identical.

---

# Skip Characters

Suppose:

```text
001 Alice

002 Alice

003 Bob
```

Ignore the first four characters.

```bash
uniq -s 4 users.txt
```

Useful for fixed-width reports.

---

# Skip Fields

Example:

```text
1 Alice

2 Alice

3 Bob
```

Command:

```bash
uniq -f 1 users.txt
```

Ignores the first field while comparing lines.

---

# Combining with Pipes

Remove duplicate users.

```bash
cut -d ":" -f1 /etc/passwd | sort | uniq
```

Count duplicate IP addresses.

```bash
cat access.log | cut -d " " -f1 | sort | uniq -c
```

Display unique departments.

```bash
cut -d "," -f2 employees.csv | sort | uniq
```

---

# Common uniq Options

| Option | Description |
|----------|-------------|
| `-c` | Count duplicate lines |
| `-d` | Display only duplicates |
| `-u` | Display only unique lines |
| `-i` | Ignore case |
| `-f` | Skip fields |
| `-s` | Skip characters |

---

# Real Production Examples

Count failed login attempts.

```bash
grep "Failed password" /var/log/auth.log | sort | uniq -c
```

Find duplicate IP addresses.

```bash
cat access.log | cut -d " " -f1 | sort | uniq -c
```

Display unique Docker images.

```bash
docker images | awk '{print $1}' | sort | uniq
```

Count Kubernetes namespaces.

```bash
kubectl get namespaces | sort | uniq
```

Generate unique usernames.

```bash
cut -d ":" -f1 /etc/passwd | sort | uniq
```

---

# Production Perspective

The `uniq` command is commonly used for:

- Cleaning reports
- Removing duplicate records
- Counting repeated log entries
- Security log analysis
- Audit reporting
- Data preprocessing before scripting

It is almost always used together with `sort`.

---

# Hands-on Lab

## Task 1

Create:

```bash
cat > servers.txt
```

Contents:

```text
server01

server02

server01

server03

server02

server04
```

---

## Task 2

Sort the file.

```bash
sort servers.txt
```

---

## Task 3

Remove duplicates.

```bash
sort servers.txt | uniq
```

---

## Task 4

Count duplicates.

```bash
sort servers.txt | uniq -c
```

---

## Task 5

Display duplicates only.

```bash
sort servers.txt | uniq -d
```

---

## Task 6

Display unique entries only.

```bash
sort servers.txt | uniq -u
```

---

## Task 7

Count unique usernames.

```bash
cut -d ":" -f1 /etc/passwd | sort | uniq | wc -l
```

---

## Task 8

Count duplicate shells.

```bash
cut -d ":" -f7 /etc/passwd | sort | uniq -c
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `uniq` | Remove adjacent duplicates | Reports |
| `uniq -c` | Count duplicates | Log analysis |
| `uniq -d` | Show duplicates | Security audits |
| `uniq -u` | Show unique values | Data validation |
| `uniq -i` | Ignore case | User reports |
| `uniq -f` | Skip fields | Fixed-format reports |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A web server's access log contains repeated client IP addresses.

Tasks:

1. Display unique client IPs.
2. Count how many requests came from each IP.
3. Display only duplicate IP addresses.
4. Identify IPs that appear only once.

Solutions:

```bash
cut -d " " -f1 access.log | sort | uniq

cut -d " " -f1 access.log | sort | uniq -c

cut -d " " -f1 access.log | sort | uniq -d

cut -d " " -f1 access.log | sort | uniq -u
```

---

# Mini Challenge

Create:

```text
employees.txt
```

Contents:

```text
Alice

Bob

Alice

Charlie

David

Charlie

Alice

Eve
```

Perform the following:

- Sort the file.
- Remove duplicate names.
- Count each name.
- Display duplicate names only.
- Display names that appear only once.
- Count the total number of unique employees.

---

# Best Practices

- Always sort data before using `uniq`.
- Use `uniq -c` to generate quick frequency reports.
- Combine `uniq` with `cut` and `grep` for advanced analysis.
- Use `uniq -u` to identify unique records.
- Use `uniq -d` to detect duplicate entries.

---

# Common Mistakes

❌ Using `uniq` on unsorted data.

✅ Incorrect:

```bash
uniq file.txt
```

Correct:

```bash
sort file.txt | uniq
```

---

❌ Assuming `uniq` removes all duplicates automatically.

✅ It only removes **adjacent** duplicate lines.

---

❌ Forgetting to sort before counting duplicates.

✅ Always use:

```bash
sort file.txt | uniq -c
```

---

# Interview Questions
## Beginner

1. What is the purpose of the `uniq` command?
2. Why is `sort` commonly used before `uniq`?
3. What does `uniq -c` do?
4. What is the difference between `uniq -d` and `uniq -u`?

---

## Intermediate

1. Explain why `uniq` only removes adjacent duplicates.
2. How do you count duplicate IP addresses in a log file?
3. What does `uniq -i` do?
4. When would you use `uniq -f`?

---

## Architect Level

1. How would you analyze duplicate log entries in a production environment?
2. Why is `uniq` useful for security and audit reporting?
3. How would you combine `cut`, `sort`, and `uniq` to generate a summary report?

---

# Summary

In this lesson, you learned:

- Removing duplicate lines
- Counting duplicate entries
- Displaying only duplicate or unique lines
- Combining `uniq` with `sort`
- Production log analysis
- Data cleaning techniques

The `uniq` command is a simple but powerful utility for cleaning and summarizing data. When combined with `sort`, it becomes an essential tool for Linux administration and text processing.

---

## Key Takeaways

- `uniq` removes adjacent duplicate lines.
- Always sort data before using `uniq`.
- `uniq -c` counts occurrences.
- `uniq -d` displays only duplicate lines.
- `uniq -u` displays only unique lines.
- `uniq` is commonly used for log analysis, reporting, and data cleanup.

---

## What's Next?

**[tr Command — Translating and Transforming Text in Linux](text-processing-tr.md)**

In the next lesson, you'll learn:

- Character translation
- Converting lowercase to uppercase
- Replacing characters
- Deleting characters
- Squeezing repeated characters
- Real-world text transformation examples
