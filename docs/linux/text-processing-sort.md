---
title: "sort Command — Sorting Text in Linux"
description: "Sort text alphabetically, numerically, by field, and by human-readable size — with reverse, unique, and month options for Linux report analysis."
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
  - sort
  - text-processing
  - command-line
  - rebash-linux-mastery
comments: false
status: ready
---

# sort Command — Sorting Text in Linux

> The `sort` command is used to arrange lines of text in alphabetical, numerical, or custom order. It is one of the most commonly used Linux text-processing utilities and is frequently combined with commands like `grep`, `cut`, `uniq`, and `awk` to analyze logs, reports, and structured data.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 3: Text Processing → Lesson 4</p>

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

<div markdown>**Lesson:** 4 of 18</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `sort` command
- Sort text alphabetically
- Sort numbers
- Sort in reverse order
- Sort using specific columns
- Remove duplicate entries
- Perform case-insensitive sorting
- Analyze real-world log and report files

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 Lessons 1–3

---

# Why Learn sort?

Imagine you receive a report with thousands of employee records.

```text
Charlie

Alice

David

Bob
```

Instead of manually rearranging the data:

```bash
sort employees.txt
```

Output:

```text
Alice

Bob

Charlie

David
```

Sorting data is a common task in Linux administration, DevOps, and data analysis.

---

# What is sort?

The `sort` command reads lines from one or more files and arranges them in a specified order.

Syntax:

```bash
sort [OPTIONS] FILE
```

---

# Sample File

Create a sample file.

```bash
cat > employees.txt
```

Contents:

```text
Charlie

Alice

David

Bob
```

Press:

```text
Ctrl + D
```

---

# Alphabetical Sorting

```bash
sort employees.txt
```

Output:

```text
Alice

Bob

Charlie

David
```

---

# Reverse Sorting

Use the `-r` option.

```bash
sort -r employees.txt
```

Output:

```text
David

Charlie

Bob

Alice
```

---

# Numeric Sorting

Create:

```bash
cat > numbers.txt
```

Contents:

```text
25

8

100

50

10
```

Default sort:

```bash
sort numbers.txt
```

Output:

```text
10

100

25

50

8
```

Numeric sort:

```bash
sort -n numbers.txt
```

Output:

```text
8

10

25

50

100
```

---

# Sort Unique Values

Remove duplicate entries.

Create:

```text
Alice

Bob

Alice

David

Bob
```

Command:

```bash
sort -u employees.txt
```

Output:

```text
Alice

Bob

David
```

---

# Ignore Case

Create:

```text
apple

Banana

APPLE

banana
```

Command:

```bash
sort -f fruits.txt
```

The `-f` option ignores case while sorting.

---

# Sort by Month

Useful for log files.

Create:

```text
Jan

Mar

Feb

Dec
```

Command:

```bash
sort -M months.txt
```

Output:

```text
Jan

Feb

Mar

Dec
```

---

# Sort Human-Readable Sizes

Create:

```text
5K

100M

2G

500K
```

Command:

```bash
sort -h sizes.txt
```

Output:

```text
5K

500K

100M

2G
```

---

# Sort CSV Files by Column

Create:

```bash
cat > employees.csv
```

Contents:

```text
Alice,85000

Bob,60000

Charlie,90000

David,75000
```

Sort by salary.

```bash
sort -t "," -k2 -n employees.csv
```

Output:

```text
Bob,60000

David,75000

Alice,85000

Charlie,90000
```

Explanation:

- `-t ","` → Delimiter
- `-k2` → Second column
- `-n` → Numeric sort

---

# Remove Duplicates with uniq

```bash
sort employees.txt | uniq
```

Count duplicates.

```bash
sort employees.txt | uniq -c
```

---

# Sort Command Output

Sort users.

```bash
cut -d ":" -f1 /etc/passwd | sort
```

Sort processes.

```bash
ps -ef | sort
```

Sort mounted filesystems.

```bash
mount | sort
```

---

# Combining with Pipes

Count unique departments.

```bash
cut -d "," -f2 employees.csv | sort | uniq | wc -l
```

Sort running processes.

```bash
ps -ef | grep nginx | sort
```

Sort log entries.

```bash
grep ERROR application.log | sort
```

---

# Common sort Options

| Option | Description |
|----------|-------------|
| `-r` | Reverse order |
| `-n` | Numeric sort |
| `-u` | Unique values |
| `-f` | Ignore case |
| `-M` | Month names |
| `-h` | Human-readable sizes |
| `-t` | Field delimiter |
| `-k` | Sort by column |

---

# Real Production Examples

Sort system users.

```bash
cut -d ":" -f1 /etc/passwd | sort
```

Sort log entries.

```bash
grep ERROR app.log | sort
```

Sort Docker images.

```bash
docker images | sort
```

Sort Kubernetes namespaces.

```bash
kubectl get namespaces | sort
```

Sort disk usage.

```bash
du -sh * | sort -h
```

---

# Production Perspective

The `sort` command is commonly used to:

- Organize reports
- Sort log entries
- Process CSV files
- Prepare data for `uniq`
- Analyze command output
- Generate readable reports

Nearly every Linux engineer uses `sort` as part of daily workflows.

---

# Hands-on Lab

## Task 1

Create:

```bash
cat > students.txt
```

Contents:

```text
Rahul

Anita

Vijay

Deepa
```

---

## Task 2

Sort alphabetically.

```bash
sort students.txt
```

---

## Task 3

Reverse sort.

```bash
sort -r students.txt
```

---

## Task 4

Create numbers.

```bash
cat > marks.txt
```

Contents:

```text
95

80

100

70

85
```

---

## Task 5

Sort numerically.

```bash
sort -n marks.txt
```

---

## Task 6

Remove duplicates.

```bash
sort -u students.txt
```

---

## Task 7

Sort usernames.

```bash
cut -d ":" -f1 /etc/passwd | sort
```

---

## Task 8

Sort salaries.

```bash
sort -t "," -k2 -n employees.csv
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `sort file` | Alphabetical sort | Reports |
| `sort -n` | Numeric sort | CPU usage |
| `sort -r` | Reverse sort | Latest entries |
| `sort -u` | Unique values | User lists |
| `sort -k2` | Sort by column | CSV reports |
| `sort -h` | Human-readable sizes | Disk usage |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    You receive a report showing disk usage across multiple servers.

```text
server01 500M

server02 2G

server03 250M

server04 1G
```

Tasks:

1. Sort servers by disk usage.
2. Display the largest server.
3. Remove duplicate entries.
4. Generate a sorted report.

Solutions:

```bash
sort -k2 -h servers.txt

sort -k2 -h servers.txt | tail -1

sort -u servers.txt

sort servers.txt > sorted-report.txt
```

---

# Mini Challenge

Create:

```text
employees.csv
```

```text
Alice,85000

Bob,60000

Charlie,90000

David,75000

Bob,60000
```

Perform the following:

- Sort alphabetically.
- Sort by salary.
- Sort in reverse order.
- Remove duplicate entries.
- Count unique employees.
- Display the employee with the highest salary.

---

# Best Practices

- Use `sort -n` for numbers instead of default sorting.
- Use `sort -h` for file sizes.
- Always sort before using `uniq`.
- Use field-based sorting for CSV files.
- Combine `sort` with `grep`, `cut`, and `awk` for powerful text processing.

---

# Common Mistakes

❌ Sorting numbers without `-n`.

✅ Incorrect:

```bash
sort numbers.txt
```

Correct:

```bash
sort -n numbers.txt
```

---

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

❌ Forgetting the delimiter when sorting CSV files.

✅ Correct:

```bash
sort -t "," -k2 employees.csv
```

---

# Interview Questions
## Beginner

1. What does the `sort` command do?
2. What is the purpose of `-n`?
3. What does `-r` do?
4. How do you remove duplicate entries?

---

## Intermediate

1. Why should data be sorted before using `uniq`?
2. Explain `sort -k`.
3. What does `sort -h` do?
4. How do you sort CSV data by a specific column?

---

## Architect Level

1. How would you sort a report containing millions of records efficiently?
2. Why is `sort` commonly used before `uniq` in shell pipelines?
3. How can `sort` improve automation and reporting in DevOps workflows?

---

# Summary

In this lesson, you learned:

- Alphabetical sorting
- Numeric sorting
- Reverse sorting
- Field-based sorting
- Case-insensitive sorting
- Human-readable size sorting
- Removing duplicates
- Real-world production use cases

The `sort` command is one of the most essential Linux text-processing tools. It is frequently combined with `cut`, `grep`, `uniq`, `awk`, and `sed` to organize and analyze data efficiently.

---

## Key Takeaways

- `sort` arranges text in ascending order by default.
- Use `-n` for numeric values.
- Use `-r` for reverse order.
- Use `-u` to remove duplicates.
- Use `-k` and `-t` to sort by specific columns.
- Always sort data before using `uniq`.

---

## What's Next?

**[uniq Command — Removing Duplicate Lines in Linux](text-processing-uniq.md)**

In the next lesson, you'll learn:

- Removing duplicate lines
- Counting duplicate entries
- Displaying unique and repeated lines
- Combining `uniq` with `sort`
- Production log and report analysis
