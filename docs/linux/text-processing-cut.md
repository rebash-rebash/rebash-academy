---
title: "cut Command — Extracting Columns from Text"
description: "Extract fields and characters with cut — delimiters, CSV, /etc/passwd, --complement, and pipelines for Linux and DevOps text processing."
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
  - cut
  - text-processing
  - csv
  - rebash-linux-mastery
comments: false
status: ready
---

# cut Command — Extracting Columns from Text

> The `cut` command is used to extract specific columns, fields, or characters from text files. It is especially useful when working with structured data such as CSV files, log files, configuration files, and command output. Mastering `cut` helps Linux administrators and DevOps engineers quickly retrieve only the information they need.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 3: Text Processing → Lesson 3</p>

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

<div markdown>**Lesson:** 3 of 18</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `cut` command
- Extract characters from text
- Extract fields using delimiters
- Extract multiple fields
- Work with CSV files
- Process Linux configuration files
- Combine `cut` with pipes

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 Lessons 1–2

---

# Why Learn cut?

Imagine you have the following file:

```text
Alice,Engineering,India

Bob,HR,USA

Charlie,Finance,UK

David,Engineering,Germany
```

You only need:

```text
Engineering

HR

Finance

Engineering
```

Instead of manually editing the file:

```bash
cut -d "," -f2 employees.csv
```

Done in seconds.

---

# What is cut?

The `cut` command extracts selected portions of each line from a file.

It can extract:

- Characters
- Bytes
- Fields

Syntax:

```bash
cut [OPTION] FILE
```

---

# Sample File

Create a file.

```bash
cat > employees.csv
```

Contents:

```text
Alice,Engineering,India

Bob,HR,USA

Charlie,Finance,UK

David,Engineering,Germany
```

Press:

```text
Ctrl + D
```

---

# Extract Fields

Fields are separated by delimiters.

Delimiter:

```text
,
```

Display only names.

```bash
cut -d "," -f1 employees.csv
```

Output:

```text
Alice

Bob

Charlie

David
```

---

# Extract Department

```bash
cut -d "," -f2 employees.csv
```

Output:

```text
Engineering

HR

Finance

Engineering
```

---

# Extract Country

```bash
cut -d "," -f3 employees.csv
```

Output:

```text
India

USA

UK

Germany
```

---

# Extract Multiple Fields

```bash
cut -d "," -f1,2 employees.csv
```

Output:

```text
Alice,Engineering

Bob,HR

Charlie,Finance

David,Engineering
```

---

# Extract Field Range

```bash
cut -d "," -f2-3 employees.csv
```

Output:

```text
Engineering,India

HR,USA

Finance,UK

Engineering,Germany
```

---

# Character Extraction

Suppose:

```text
Linux
```

Extract first three characters.

```bash
echo Linux | cut -c1-3
```

Output:

```text
Lin
```

---

Extract first character.

```bash
echo Linux | cut -c1
```

Output:

```text
L
```

---

Extract characters 3 to 5.

```bash
echo Kubernetes | cut -c3-5
```

Output:

```text
ber
```

---

# Working with /etc/passwd

Linux user information is stored in:

```text
/etc/passwd
```

Example entry:

```text
basha:x:1000:1000:Basha:/home/basha:/bin/bash
```

Display usernames.

```bash
cut -d ":" -f1 /etc/passwd
```

---

Display user IDs.

```bash
cut -d ":" -f3 /etc/passwd
```

---

Display login shells.

```bash
cut -d ":" -f7 /etc/passwd
```

---

# Working with Command Output

Extract only usernames.

```bash
who | cut -d " " -f1
```

Display filesystem names.

```bash
df -h | cut -d " " -f1
```

---

# Combining with Pipes

Search Engineering department.

```bash
cut -d "," -f2 employees.csv | grep Engineering
```

---

Sort countries.

```bash
cut -d "," -f3 employees.csv | sort
```

---

Remove duplicates.

```bash
cut -d "," -f2 employees.csv | sort | uniq
```

---

Count unique departments.

```bash
cut -d "," -f2 employees.csv | sort | uniq | wc -l
```

---

# Common Options

| Option | Description |
|----------|-------------|
| `-d` | Specify delimiter |
| `-f` | Select fields |
| `-c` | Select characters |
| `--complement` | Display everything except selected fields |

---

# Using --complement

Display everything except department.

```bash
cut -d "," -f2 --complement employees.csv
```

Output:

```text
Alice,India

Bob,USA

Charlie,UK

David,Germany
```

---

# Real Production Examples

Extract usernames.

```bash
cut -d ":" -f1 /etc/passwd
```

Extract mounted filesystems.

```bash
mount | cut -d " " -f3
```

Extract pod names.

```bash
kubectl get pods | cut -d " " -f1
```

Extract IP addresses.

```bash
ip addr | grep inet | cut -d " " -f6
```

Extract Docker image names.

```bash
docker images | cut -d " " -f1
```

---

# Production Perspective

The `cut` command is frequently used to:

- Process CSV reports
- Extract usernames
- Analyze logs
- Parse configuration files
- Build shell scripts
- Process Kubernetes and Docker output

It is lightweight, fast, and commonly combined with other text-processing tools.

---

# Hands-on Lab

## Task 1

Create:

```bash
cat > students.csv
```

Contents:

```text
Rahul,CSE,80

Priya,IT,90

Arjun,ECE,85

Neha,CSE,95
```

---

## Task 2

Display names.

```bash
cut -d "," -f1 students.csv
```

---

## Task 3

Display departments.

```bash
cut -d "," -f2 students.csv
```

---

## Task 4

Display marks.

```bash
cut -d "," -f3 students.csv
```

---

## Task 5

Display names and marks.

```bash
cut -d "," -f1,3 students.csv
```

---

## Task 6

Display usernames.

```bash
cut -d ":" -f1 /etc/passwd
```

---

## Task 7

Display login shells.

```bash
cut -d ":" -f7 /etc/passwd
```

---

## Task 8

Count departments.

```bash
cut -d "," -f2 students.csv | sort | uniq | wc -l
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `cut -d "," -f1` | Extract first field | Usernames |
| `cut -d ":" -f7` | Extract login shell | `/etc/passwd` |
| `cut -c1-5` | Extract characters | IDs |
| `cut --complement` | Exclude fields | CSV processing |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A Linux administrator receives a CSV report containing server information.

```text
server01,Running,10.0.0.10

server02,Stopped,10.0.0.11

server03,Running,10.0.0.12

server04,Maintenance,10.0.0.13
```

Tasks:

1. Display server names.
2. Display only IP addresses.
3. Show server names and status.
4. Count running servers.

Solutions:

```bash
cut -d "," -f1 servers.csv

cut -d "," -f3 servers.csv

cut -d "," -f1,2 servers.csv

grep Running servers.csv | wc -l
```

---

# Mini Challenge

Create:

```text
employees.csv
```

```text
Alice,Engineering,India,85000

Bob,HR,USA,60000

Charlie,Finance,UK,75000

David,Engineering,Germany,90000
```

Perform the following:

- Display employee names.
- Display departments.
- Display salaries.
- Display names and salaries.
- Display everything except salary.
- Count unique departments.
- Show only Engineering employees and their names.

---

# Best Practices

- Use `cut` only for consistently delimited data.
- Verify the delimiter before extracting fields.
- Combine `cut` with `grep`, `sort`, `uniq`, and `wc` for advanced processing.
- Use meaningful delimiters such as commas, colons, or tabs.
- For complex data extraction, consider `awk` in later lessons.

---

# Common Mistakes

❌ Forgetting the delimiter.

✅ Incorrect:

```bash
cut -f2 employees.csv
```

Correct:

```bash
cut -d "," -f2 employees.csv
```

---

❌ Using `cut` on irregularly spaced text.

✅ `cut` works best with structured, delimiter-separated files.

---

❌ Expecting `cut` to process variable-width columns.

✅ Use `awk` for more advanced parsing.

---

# Interview Questions
## Beginner

1. What is the purpose of the `cut` command?
2. What does `-d` specify?
3. What does `-f` do?
4. How do you extract the first field?

---

## Intermediate

1. Difference between `-c` and `-f`?
2. Explain `--complement`.
3. Why is `cut` useful for CSV files?
4. When should you use `awk` instead of `cut`?

---

## Architect Level

1. How would you process a large CSV report containing millions of records?
2. Why is `cut` commonly used in shell scripting?
3. How would you combine `cut`, `grep`, and `sort` to analyze production data?

---

# Summary

In this lesson, you learned:

- Extracting fields using delimiters
- Extracting character positions
- Processing CSV files
- Working with `/etc/passwd`
- Combining `cut` with other text-processing tools
- Real-world administration use cases

The `cut` command is a simple yet powerful utility for extracting structured data. It is commonly used in shell scripts, automation, and production environments.

---

## Key Takeaways

- `cut` extracts fields or characters from text.
- `-d` specifies the delimiter.
- `-f` selects fields.
- `-c` selects character positions.
- `cut` works best with consistently structured data.
- Combine `cut` with `grep`, `sort`, `uniq`, and `wc` for efficient text processing.

---

## What's Next?

**[sort Command — Sorting Text in Linux](text-processing-sort.md)**

In the next lesson, you'll learn:

- Alphabetical sorting
- Numeric sorting
- Reverse sorting
- Sorting by specific fields
- Removing duplicates with `sort`
- Practical log and report analysis
