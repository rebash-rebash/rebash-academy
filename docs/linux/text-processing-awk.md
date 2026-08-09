---
title: "awk Command — The Ultimate Linux Text Processing Language"
description: "Process structured text with awk — fields, conditions, BEGIN/END, calculations, CSV, printf reports, and production DevOps automation."
difficulty: advanced
estimated_time: "75 min"
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
  - awk
  - text-processing
  - reporting
  - rebash-linux-mastery
comments: false
status: ready
---

# awk Command — The Ultimate Linux Text Processing Language

> `awk` is one of the most powerful text-processing tools available on Linux. Unlike commands such as `grep`, `cut`, or `sed`, `awk` is a complete programming language designed for processing structured text, generating reports, performing calculations, filtering data, and automating repetitive tasks. It is widely used in Linux administration, DevOps, Cloud Engineering, Data Processing, and Security.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 3: Text Processing → Lesson 17</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Advanced</div>

<div markdown>**Reading Time:** 75 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Text Processing</div>

<div markdown>**Lesson:** 17 of 18</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `awk` programming model
- Work with fields and records
- Filter and print data
- Perform calculations
- Use variables
- Apply conditional statements
- Generate reports
- Process CSV files
- Use built-in variables
- Write production-ready automation

---

# Prerequisites

Complete:

- Module 1
- Module 2
- Module 3 Lessons 1–16

---

# Why Learn awk?

Suppose you have:

```text
Alice Engineering 85000

Bob HR 60000

Charlie Finance 90000

David DevOps 75000
```

Questions:

- Show employees earning more than 80,000.
- Calculate total salary.
- Find average salary.
- Display only names.
- Sort departments.
- Generate reports.

All of this can be done using `awk`.

---

# What is awk?

`awk` is a pattern-scanning and text-processing language.

It works line by line.

Each line is automatically divided into **fields**.

Default field separator:

```text
Whitespace
```

Syntax:

```bash
awk 'pattern { action }' file
```

---

# Sample File

Create:

```bash
cat > employees.txt
```

Contents:

```text
Alice Engineering 85000

Bob HR 60000

Charlie Finance 90000

David DevOps 75000

Eve Engineering 92000
```

---

# Print Entire File

```bash
awk '{print}' employees.txt
```

Equivalent to:

```bash
cat employees.txt
```

---

# Print First Column

```bash
awk '{print $1}' employees.txt
```

Output:

```text
Alice

Bob

Charlie

David

Eve
```

---

# Print Multiple Columns

```bash
awk '{print $1, $2}' employees.txt
```

Output:

```text
Alice Engineering

Bob HR

Charlie Finance

David DevOps

Eve Engineering
```

---

# Built-in Variables

| Variable | Description |
|----------|-------------|
| `$1` | First field |
| `$2` | Second field |
| `$NF` | Last field |
| `NR` | Current record number |
| `NF` | Number of fields |
| `FS` | Input field separator |
| `OFS` | Output field separator |

---

# Print Last Column

```bash
awk '{print $NF}' employees.txt
```

Output:

```text
85000

60000

90000

75000

92000
```

---

# Print Record Number

```bash
awk '{print NR, $0}' employees.txt
```

Output:

```text
1 Alice Engineering 85000

2 Bob HR 60000

3 Charlie Finance 90000
```

---

# Conditional Statements

Employees earning more than 80,000.

```bash
awk '$3 > 80000'
```

Output:

```text
Alice Engineering 85000

Charlie Finance 90000

Eve Engineering 92000
```

---

# Exact Match

```bash
awk '$2=="Engineering"'
```

---

# Multiple Conditions

```bash
awk '$2=="Engineering" && $3>90000'
```

---

# BEGIN Block

```bash
awk 'BEGIN {print "Employee Report"}'
```

Output:

```text
Employee Report
```

---

# END Block

```bash
awk 'END {print "Finished"}'
```

---

# BEGIN + END

```bash
awk '
BEGIN {print "Employee Report"}

{print}

END {print "End of Report"}
'
```

---

# Calculations

Total salary.

```bash
awk '{sum += $3}

END {print sum}'
```

Output:

```text
402000
```

---

Average salary.

```bash
awk '{sum+=$3}

END {print sum/NR}'
```

---

Maximum salary.

```bash
awk '

BEGIN {max=0}

$3>max {max=$3}

END {print max}
'
```

---

# Count Records

```bash
awk 'END {print NR}'
```

---

# CSV Files

Create:

```text
Alice,Engineering,85000

Bob,HR,60000

Charlie,Finance,90000
```

Specify delimiter.

```bash
awk -F "," '{print $1}'
```

---

# Output Separator

```bash
awk 'BEGIN{OFS=" | "}

{print $1,$2,$3}'
```

---

# Formatted Reports

```bash
awk '{printf "%-10s %-15s %8d\n",$1,$2,$3}'
```

Output:

```text
Alice      Engineering      85000

Bob        HR               60000
```

---

# Using Variables

```bash
awk -v dept="Engineering" '$2==dept'
```

---

# Using Regular Expressions

Contains "Eng".

```bash
awk '$2~/Eng/'
```

Does not contain HR.

```bash
awk '$2!~/HR/'
```

---

# Common awk Options

| Option | Description |
|----------|-------------|
| `-F` | Input delimiter |
| `-v` | Pass variable |
| `-f` | Run AWK program from file |

---

# Real Production Examples

Display usernames.

```bash
awk -F ":" '{print $1}' /etc/passwd
```

Display login shells.

```bash
awk -F ":" '{print $7}'
```

Disk usage.

```bash
df -h | awk '{print $1,$5}'
```

Docker.

```bash
docker ps | awk '{print $1,$2}'
```

Kubernetes.

```bash
kubectl get pods | awk '{print $1,$3}'
```

Systemd.

```bash
systemctl list-units | awk '{print $1}'
```

---

# Kubernetes Example

Display only Running Pods.

```bash
kubectl get pods | awk '$3=="Running"'
```

---

# Docker Example

Display image names.

```bash
docker images | awk '{print $1}'
```

---

# Terraform Example

Extract resource names.

```bash
terraform state list | awk '{print $1}'
```

---

# Production Perspective

`awk` is heavily used for:

- CSV processing
- Report generation
- Monitoring
- Kubernetes administration
- Log analysis
- CI/CD
- Security auditing
- Automation

---

# Hands-on Lab

## Task 1

Display names.

```bash
awk '{print $1}' employees.txt
```

---

## Task 2

Display salary.

```bash
awk '{print $3}'
```

---

## Task 3

Display Engineering.

```bash
awk '$2=="Engineering"'
```

---

## Task 4

Calculate total salary.

```bash
awk '{sum+=$3}

END{print sum}'
```

---

## Task 5

Average salary.

```bash
awk '{sum+=$3}

END{print sum/NR}'
```

---

## Task 6

Number rows.

```bash
awk '{print NR,$0}'
```

---

## Task 7

CSV processing.

```bash
awk -F "," '{print $2}'
```

---

## Task 8

Pretty report.

```bash
awk '{printf "%-10s %-15s %8d\n",$1,$2,$3}'
```

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A Kubernetes administrator needs to generate a report showing only Running Pods with their node names.

Tasks:

- Filter Running Pods.
- Display Pod Name.
- Display Node.
- Save the report.

```bash
kubectl get pods -o wide | \
awk '$3=="Running" {print $1,$7}' > running-pods.txt
```

---

# Best Practices

- Use `-F` for CSV and colon-separated files.
- Use `printf` for professional reports.
- Prefer `awk` over multiple `cut` commands when performing calculations.
- Keep complex scripts in separate `.awk` files.
- Comment large AWK programs for maintainability.

---

# Performance Tip

`awk` processes input as a stream, making it efficient for large files. It often replaces multiple chained commands (`cut`, `grep`, `sort`) with a single, readable program, reducing process creation overhead.

---

# Common Mistakes

❌ Forgetting field numbering starts at **1**.

✅ Remember to field numbering starts at **1**.

---

❌ Using `cut` when calculations are required.

✅ Use `awk` instead.

---

❌ Not specifying the correct delimiter.

✅ Use:

```bash
awk -F ","
```

---

# Interview Questions
## Beginner

1. What is `awk`?
2. What does `$1` represent?
3. What is `NR`?
4. What is `NF`?

---

## Intermediate

1. Explain `BEGIN` and `END`.
2. Difference between `print` and `printf`.
3. What does `-F` do?
4. How do you calculate averages?

---

## Architect Level

1. Why is `awk` considered a programming language?
2. How would you generate infrastructure reports using `awk`?
3. When would you choose `awk` instead of `sed` or `cut`?

---

# Summary

In this lesson, you learned:

- Field-based processing
- Conditional filtering
- Variables and built-in variables
- Calculations
- CSV processing
- Report generation
- Production automation

`awk` is one of the most powerful tools in Linux. Mastering it enables you to process structured text, generate reports, automate administrative tasks, and build efficient DevOps workflows.

---

## Key Takeaways

- `awk` is a complete text-processing language.
- Fields are referenced using `$1`, `$2`, ..., `$NF`.
- Use `-F` to specify field separators.
- `BEGIN` and `END` are ideal for headers, summaries, and totals.
- `printf` creates professional, aligned reports.
- `awk` is a core skill for Linux administrators, DevOps engineers, SREs, and Cloud Architects.

---

## What's Next?

**[Regular Expressions (Regex) — Pattern Matching in Linux](text-processing-regular-expressions.md)**

In the next lesson, you'll learn pattern matching for `grep`, `sed`, and `awk` — anchors, character classes, quantifiers, and production-ready regex techniques.
