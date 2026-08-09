---
title: "column Command — Displaying Text in Tabular Format"
description: "Format CSV and command output into aligned tables with column — custom delimiters, separators, and readable production reports."
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
  - column
  - text-processing
  - csv
  - rebash-linux-mastery
comments: false
status: ready
---

# column Command — Displaying Text in Tabular Format

> The `column` command formats text into neatly aligned columns or tables, making command output much easier to read. It is commonly used to display CSV files, reports, configuration data, and command output in a structured, professional format.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 3: Text Processing → Lesson 12</p>

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

<div markdown>**Lesson:** 12 of 18</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `column` command
- Format text into aligned columns
- Display CSV files as tables
- Use custom delimiters
- Create professional-looking reports
- Format command output
- Combine `column` with other Linux utilities

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 Lessons 1–11

---

# Why Learn column?

Suppose you have a CSV file.

```text
Alice,Engineering,85000

Bob,HR,60000

Charlie,Finance,90000

David,DevOps,75000
```

Reading it is possible, but not ideal.

Using:

```bash
column -t -s "," employees.csv
```

Produces:

```text
Alice    Engineering  85000

Bob      HR           60000

Charlie  Finance      90000

David    DevOps       75000
```

Much easier to read.

---

# What is column?

The `column` command aligns text into multiple columns.

It is mainly used to improve readability.

Syntax:

```bash
column [OPTIONS] FILE
```

---

# Sample File

Create:

```bash
cat > employees.csv
```

Contents:

```text
Alice,Engineering,85000

Bob,HR,60000

Charlie,Finance,90000

David,DevOps,75000
```

---

# Display as Table

```bash
column -t -s "," employees.csv
```

Output:

```text
Alice    Engineering  85000

Bob      HR           60000

Charlie  Finance      90000

David    DevOps       75000
```

Explanation:

- `-t` → Create a table
- `-s ","` → Use comma as the delimiter

---

# Space-Separated Data

Create:

```text
server01 Running

server02 Stopped

server03 Running
```

Display:

```bash
column -t servers.txt
```

Output:

```text
server01   Running

server02   Stopped

server03   Running
```

---

# Using Colon Delimiters

Example:

```text
root:x:0:0

basha:x:1000:1000
```

Display:

```bash
column -t -s ":" passwd.txt
```

Output:

```text
root   x     0     0

basha  x  1000  1000
```

---

# Display /etc/passwd

```bash
column -t -s ":" /etc/passwd
```

This makes user account information much easier to read.

---

# Format Command Output

Disk usage.

```bash
df -h | column -t
```

Processes.

```bash
ps -ef | column -t
```

Mounted filesystems.

```bash
mount | column -t
```

Network connections.

```bash
ss -tuln | column -t
```

---

# Combining with Other Commands

Format CSV.

```bash
cat employees.csv | column -t -s ","
```

Display usernames.

```bash
cut -d ":" -f1,7 /etc/passwd | column -t -s ":"
```

Format inventory.

```bash
paste servers.txt ips.txt | column -t
```

---

# Add Headers

Create:

```text
Name,Department,Salary

Alice,Engineering,85000

Bob,HR,60000
```

Display:

```bash
column -t -s "," employees.csv
```

Output:

```text
Name     Department   Salary

Alice    Engineering  85000

Bob      HR           60000
```

---

# Common column Options

| Option | Description |
|----------|-------------|
| `-t` | Create a table |
| `-s` | Specify delimiter |
| `-c` | Set output width |
| `-o` | Set output separator |

---

# Change Output Separator

Default spacing:

```bash
column -t
```

Custom separator:

```bash
column -t -s "," -o " | " employees.csv
```

Output:

```text
Alice | Engineering | 85000

Bob   | HR          | 60000
```

---

# Real Production Examples

Format Kubernetes output.

```bash
kubectl get pods | column -t
```

Format Docker images.

```bash
docker images | column -t
```

Display Linux users.

```bash
column -t -s ":" /etc/passwd
```

Format inventory.

```bash
column -t inventory.csv
```

Display environment variables.

```bash
printenv | column -t -s "="
```

---

# Production Perspective

The `column` command is useful for:

- Reports
- CSV files
- Server inventories
- Configuration reviews
- Log summaries
- Shell script output

It improves readability without modifying the original data.

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

Display as a table.

```bash
column -t -s "," students.csv
```

---

## Task 3

Display `/etc/passwd`.

```bash
column -t -s ":" /etc/passwd
```

---

## Task 4

Format disk usage.

```bash
df -h | column -t
```

---

## Task 5

Format environment variables.

```bash
printenv | column -t -s "="
```

---

## Task 6

Create an inventory.

```text
Server,Status

server01,Running

server02,Stopped
```

Display:

```bash
column -t -s "," inventory.csv
```

---

## Task 7

Use a custom separator.

```bash
column -t -s "," -o " | " students.csv
```

---

## Task 8

Combine with `paste`.

```bash
paste names.txt marks.txt | column -t
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `column -t` | Align text | Reports |
| `column -t -s ","` | Format CSV | Inventory |
| `column -t -s ":"` | Format passwd | User audit |
| `column -o " | "` | Custom separator | Dashboards |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A DevOps engineer receives an inventory file.

```text
Server,Status,IP

server01,Running,10.0.0.10

server02,Stopped,10.0.0.11

server03,Running,10.0.0.12
```

Tasks:

1. Display it as a table.
2. Replace commas with aligned columns.
3. Save formatted output.
4. Display only the Running servers.

Solutions:

```bash
column -t -s "," inventory.csv

column -t -s "," inventory.csv > report.txt

grep Running inventory.csv | column -t -s ","
```

---

# Mini Challenge

Create:

```text
employees.csv
```

```text
Name,Department,Salary

Alice,Engineering,85000

Bob,HR,60000

Charlie,Finance,90000

David,DevOps,75000
```

Perform the following:

- Display as a table.
- Use `|` as the separator.
- Save formatted output.
- Display only Engineering employees.
- Display only Name and Salary using `cut`.
- Format the result using `column`.

---

# Best Practices

- Use `column -t` for better terminal readability.
- Use the correct delimiter with `-s`.
- Format reports before sharing with teammates.
- Combine `column` with `cut`, `paste`, and `grep`.
- Remember that `column` changes only the display, not the original file.

---

# Common Mistakes

❌ Forgetting the delimiter.

✅ Incorrect:

```bash
column -t employees.csv
```

Correct:

```bash
column -t -s "," employees.csv
```

---

❌ Expecting `column` to modify files.

✅ It only formats the displayed output.

---

❌ Using `column` on data with inconsistent delimiters.

✅ Ensure the input is consistently structured.

---

# Interview Questions
## Beginner

1. What is the purpose of the `column` command?
2. What does the `-t` option do?
3. How do you display a CSV file as a table?
4. What does the `-s` option specify?

---

## Intermediate

1. How do you display `/etc/passwd` in aligned columns?
2. Explain the purpose of `-o`.
3. How can `column` improve shell script output?
4. Why doesn't `column` modify the original file?

---

## Architect Level

1. How would you generate professional terminal reports from automation scripts?
2. How can `column` improve operational dashboards?
3. How would you combine `cut`, `grep`, and `column` to build an inventory report?

---

# Summary

In this lesson, you learned:

- Creating aligned tables
- Formatting CSV files
- Working with custom delimiters
- Formatting command output
- Combining `column` with other Linux utilities
- Generating professional reports

The `column` command is a presentation tool that transforms plain text into clean, readable tables. It is especially valuable for displaying reports, inventories, and command output in a format that's easy to understand.

---

## Key Takeaways

- `column` formats text into aligned columns.
- Use `-t` to create tables.
- Use `-s` to specify the input delimiter.
- Use `-o` to customize the output separator.
- `column` improves readability without modifying the source data.

---

## What's Next?

**[strings Command — Extracting Printable Text from Binary Files](text-processing-strings.md)**

In the next lesson, you'll learn:

- Extracting readable text from binaries
- Analyzing executable files
- Inspecting libraries and firmware
- Malware and forensic analysis basics
- Real-world troubleshooting techniques
