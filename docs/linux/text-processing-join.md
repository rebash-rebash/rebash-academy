---
title: "join Command — Joining Files Using a Common Field"
description: "Join sorted files on a common field like SQL INNER JOIN — delimiters, field selection, unmatched records, and production inventory reports."
difficulty: intermediate
estimated_time: "35 min"
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
  - join
  - text-processing
  - csv
  - rebash-linux-mastery
comments: false
status: ready
---

# join Command — Joining Files Using a Common Field

> The `join` command combines lines from two sorted files based on a common field, much like an SQL INNER JOIN. It is commonly used to merge related datasets such as employee records, inventory lists, configuration files, and reports. Understanding `join` is valuable for Linux administrators, DevOps engineers, and anyone working with structured text data.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 3: Text Processing → Lesson 9</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 35 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Text Processing</div>

<div markdown>**Lesson:** 9 of 18</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `join` command
- Join files using a common field
- Join using different columns
- Change field delimiters
- Display selected fields
- Handle unmatched records
- Use `join` in production scenarios

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 Lessons 1–8

---

# Why Learn join?

Suppose you have two files.

**employees.txt**

```text
101 Alice

102 Bob

103 Charlie

104 David
```

**departments.txt**

```text
101 Engineering

102 HR

103 Finance

104 DevOps
```

You want this result:

```text
101 Alice Engineering

102 Bob HR

103 Charlie Finance

104 David DevOps
```

Instead of manually combining them, use:

```bash
join employees.txt departments.txt
```

---

# What is join?

The `join` command combines two files based on a matching field.

It works similarly to an SQL **INNER JOIN**.

Syntax:

```bash
join [OPTIONS] FILE1 FILE2
```

!!! warning "Important"

    Both files must be sorted on the join field before using `join`.

---

# Sample Files

Create:

```bash
cat > employees.txt
```

Contents:

```text
101 Alice

102 Bob

103 Charlie

104 David
```

Create:

```bash
cat > departments.txt
```

Contents:

```text
101 Engineering

102 HR

103 Finance

104 DevOps
```

---

# Verify Sorting

Before joining:

```bash
sort employees.txt

sort departments.txt
```

Or sort in-place.

```bash
sort employees.txt -o employees.txt

sort departments.txt -o departments.txt
```

---

# Basic Join

```bash
join employees.txt departments.txt
```

Output:

```text
101 Alice Engineering

102 Bob HR

103 Charlie Finance

104 David DevOps
```

---

# How join Works

```text
employees.txt

101 Alice

102 Bob

↓

Match on Field 1

↓

departments.txt

101 Engineering

102 HR

↓

Joined Output
```

---

# Join Using a Different Delimiter

Suppose the files are CSV.

**employees.csv**

```text
101,Alice

102,Bob

103,Charlie
```

**departments.csv**

```text
101,Engineering

102,HR

103,Finance
```

Command:

```bash
join -t "," employees.csv departments.csv
```

Output:

```text
101,Alice,Engineering
```

---

# Join on Different Fields

Suppose:

**employees.txt**

```text
Alice 101

Bob 102
```

**departments.txt**

```text
101 Engineering

102 HR
```

Join using:

```bash
join -1 2 -2 1 employees.txt departments.txt
```

Explanation:

- `-1 2` → Use field 2 from File 1
- `-2 1` → Use field 1 from File 2

---

# Display Selected Fields

Default output:

```text
ID Name Department
```

Customize output.

```bash
join -o 1.2,2.2 employees.txt departments.txt
```

Output:

```text
Alice Engineering

Bob HR

Charlie Finance
```

---

# Include Unmatched Records

Normally:

Only matching records appear.

To include unmatched records from File 1:

```bash
join -a1 employees.txt departments.txt
```

Include unmatched from File 2:

```bash
join -a2 employees.txt departments.txt
```

Include all records:

```bash
join -a1 -a2 employees.txt departments.txt
```

---

# Replace Missing Values

Display "N/A" for missing matches.

```bash
join -a1 -e "N/A" employees.txt departments.txt
```

---

# Ignore Case

If the join field differs only by letter case:

```bash
join -i employees.txt departments.txt
```

---

# Common join Options

| Option | Description |
|----------|-------------|
| `-t` | Specify delimiter |
| `-1` | Join field from File 1 |
| `-2` | Join field from File 2 |
| `-o` | Select output fields |
| `-a1` | Include unmatched lines from File 1 |
| `-a2` | Include unmatched lines from File 2 |
| `-e` | Replace missing fields |
| `-i` | Ignore case |

---

# Combining with Other Commands

Sort before joining.

```bash
sort employees.txt -o employees.txt

sort departments.txt -o departments.txt

join employees.txt departments.txt
```

Extract usernames and shells.

```bash
join \
<(cut -d ":" -f1,7 users1.txt | sort) \
<(cut -d ":" -f1,2 users2.txt | sort)
```

---

# Difference Between paste and join

| paste | join |
|--------|------|
| Combines files by line number | Combines files by matching field |
| Files need equal line order | Files must be sorted |
| Similar to ZIP | Similar to SQL JOIN |

---

# Real Production Examples

Merge server inventory.

```text
servers.txt

server01 Linux

server02 Windows
```

```text
ips.txt

server01 10.0.0.10

server02 10.0.0.11
```

Command:

```bash
join servers.txt ips.txt
```

---

Merge user accounts.

```bash
join users.txt departments.txt
```

Merge cloud inventory.

```bash
join instances.txt billing.txt
```

Merge Kubernetes reports.

```bash
join nodes.txt capacity.txt
```

---

# Production Perspective

The `join` command is useful for:

- Combining inventory reports
- Merging user information
- Creating audit reports
- Processing CSV data
- Infrastructure automation
- Reporting and analytics

---

# Hands-on Lab

## Task 1

Create:

```bash
cat > students.txt
```

Contents:

```text
101 Rahul

102 Priya

103 Arjun

104 Neha
```

---

## Task 2

Create:

```bash
cat > marks.txt
```

Contents:

```text
101 80

102 90

103 85

104 95
```

---

## Task 3

Sort both files.

```bash
sort students.txt -o students.txt

sort marks.txt -o marks.txt
```

---

## Task 4

Join them.

```bash
join students.txt marks.txt
```

---

## Task 5

Display only names and marks.

```bash
join -o 1.2,2.2 students.txt marks.txt
```

---

## Task 6

Convert to CSV.

```bash
join students.txt marks.txt | tr ' ' ','
```

---

## Task 7

Add an unmatched record.

```text
105 Ravi
```

Use:

```bash
join -a1 students.txt marks.txt
```

---

## Task 8

Replace missing marks.

```bash
join -a1 -e "Absent" students.txt marks.txt
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `join file1 file2` | Join files | Reports |
| `join -t ","` | CSV files | Inventory |
| `join -1` | Different field | User mapping |
| `join -o` | Custom output | Reports |
| `join -a1` | Include unmatched | Audits |
| `join -e` | Replace missing values | Compliance reports |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A cloud administrator has two reports.

**instances.txt**

```text
vm01 Running

vm02 Stopped

vm03 Running
```

**billing.txt**

```text
vm01 120

vm02 90

vm03 300
```

Tasks:

1. Merge both reports.
2. Display VM names and monthly cost.
3. Include VMs without billing records.
4. Export the final report as CSV.

Solutions:

```bash
join instances.txt billing.txt

join -o 1.1,2.2 instances.txt billing.txt

join -a1 instances.txt billing.txt

join instances.txt billing.txt | tr ' ' ','
```

---

# Mini Challenge

Create:

**employees.txt**

```text
101 Alice

102 Bob

103 Charlie

104 David
```

**salary.txt**

```text
101 85000

102 60000

103 90000

104 75000
```

Perform the following:

- Sort both files.
- Join them.
- Display only names and salaries.
- Add an unmatched employee.
- Replace missing salary with `N/A`.
- Export the report as CSV.

---

# Best Practices

- Always sort files before using `join`.
- Verify that the join field is identical in both files.
- Use `-t` when working with CSV files.
- Use `-o` to generate clean reports.
- Use `-a1` and `-a2` when missing records are important.

---

# Common Mistakes

❌ Joining unsorted files.

✅ Incorrect:

```bash
join employees.txt departments.txt
```

If the files are not sorted, `join` may fail or produce incomplete output.

Correct:

```bash
sort employees.txt -o employees.txt

sort departments.txt -o departments.txt

join employees.txt departments.txt
```

---

❌ Confusing `paste` with `join`.

✅ - `paste` joins by **line number**.
- `join` joins by **matching field**.

---

❌ Using different delimiters.

✅ If one file uses commas and another uses spaces, normalize the data first.

---

# Interview Questions
## Beginner

1. What does the `join` command do?
2. Why must files be sorted before using `join`?
3. What does `-t` specify?
4. What is the purpose of `-o`?

---

## Intermediate

1. Explain `join -1` and `join -2`.
2. What does `join -a1` do?
3. How do you replace missing values?
4. Difference between `join` and `paste`?

---

## Architect Level

1. How would you combine multiple infrastructure reports using `join`?
2. Why is `join` similar to a database JOIN?
3. How would you automate inventory report generation using `sort`, `join`, and `awk`?

---

# Summary

In this lesson, you learned:

- Joining files by a common field
- Working with sorted files
- Joining CSV files
- Selecting output columns
- Handling unmatched records
- Production reporting techniques

The `join` command is a powerful utility for combining structured data from multiple sources. It is especially valuable for generating reports, merging inventories, and automating administrative tasks.

---

## Key Takeaways

- `join` combines files using a matching field.
- Both files should be sorted on the join field.
- Use `-t` for custom delimiters.
- Use `-o` to customize output.
- Use `-a1` and `-a2` to include unmatched records.
- Think of `join` as the Linux equivalent of an SQL **INNER JOIN**.

---

## What's Next?

**[split Command — Splitting Large Files in Linux](text-processing-split.md)**

In the next lesson, you'll learn:

- Splitting files by size
- Splitting files by number of lines
- Custom file prefixes and suffixes
- Reassembling split files
- Handling large log files and backups
