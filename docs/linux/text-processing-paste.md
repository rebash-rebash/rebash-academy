---
title: "paste Command — Merging Files Horizontally in Linux"
description: "Merge files side by side with paste — custom delimiters, serial mode, CSV reports, and Bash process substitution for Linux automation."
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
  - paste
  - text-processing
  - csv
  - rebash-linux-mastery
comments: false
status: ready
---

# paste Command — Merging Files Horizontally in Linux

> The `paste` command is used to merge lines from multiple files horizontally. Unlike the `cat` command, which combines files vertically, `paste` joins corresponding lines side by side using a delimiter. It is widely used for combining reports, CSV files, configuration data, and command outputs.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 3: Text Processing → Lesson 8</p>

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

<div markdown>**Lesson:** 8 of 18</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `paste` command
- Merge multiple files horizontally
- Change delimiters
- Merge command outputs
- Work with CSV-like data
- Combine `paste` with other Linux commands
- Process real-world reports

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 Lessons 1–7

---

# Why Learn paste?

Suppose you have two separate files.

**names.txt**

```text
Alice
Bob
Charlie
David
```

**departments.txt**

```text
Engineering
HR
Finance
DevOps
```

Instead of manually combining them:

```text
Alice Engineering

Bob HR

Charlie Finance

David DevOps
```

Use:

```bash
paste names.txt departments.txt
```

Done instantly.

---

# What is paste?

The `paste` command joins corresponding lines from multiple files into a single output.

Syntax:

```bash
paste [OPTIONS] FILE...
```

By default, it separates columns with a **tab**.

---

# Sample Files

Create:

```bash
cat > names.txt
```

```text
Alice

Bob

Charlie

David
```

Create:

```bash
cat > departments.txt
```

```text
Engineering

HR

Finance

DevOps
```

---

# Merge Two Files

```bash
paste names.txt departments.txt
```

Output:

```text
Alice    Engineering

Bob      HR

Charlie  Finance

David    DevOps
```

(Default delimiter: Tab)

---

# Merge Three Files

Create:

**countries.txt**

```text
India

USA

UK

Germany
```

Run:

```bash
paste names.txt departments.txt countries.txt
```

Output:

```text
Alice    Engineering    India

Bob      HR             USA

Charlie  Finance        UK

David    DevOps         Germany
```

---

# Change the Delimiter

Use commas.

```bash
paste -d "," names.txt departments.txt
```

Output:

```text
Alice,Engineering

Bob,HR

Charlie,Finance

David,DevOps
```

---

Use a colon.

```bash
paste -d ":" names.txt departments.txt
```

Output:

```text
Alice:Engineering

Bob:HR

Charlie:Finance

David:DevOps
```

---

# Use Multiple Delimiters

```bash
paste -d ",:" names.txt departments.txt countries.txt
```

Output:

```text
Alice,Engineering:India

Bob,HR:USA

Charlie,Finance:UK

David,DevOps:Germany
```

The delimiters are used in sequence.

---

# Serial Mode

Normally:

```bash
paste names.txt
```

Output:

```text
Alice

Bob

Charlie

David
```

Serial mode:

```bash
paste -s names.txt
```

Output:

```text
Alice    Bob    Charlie    David
```

---

Comma-separated serial output.

```bash
paste -s -d "," names.txt
```

Output:

```text
Alice,Bob,Charlie,David
```

---

# Merge Command Output

Merge usernames and login shells.

```bash
paste \
<(cut -d ":" -f1 /etc/passwd) \
<(cut -d ":" -f7 /etc/passwd)
```

Example:

```text
root     /bin/bash

daemon   /usr/sbin/nologin
```

!!! note "Note"

    The `<(...)` syntax is called **process substitution** and is supported in Bash. We'll cover it in the Shell Scripting module.

---

# Combining with Other Commands

Sort before merging.

```bash
paste <(sort names.txt) <(sort departments.txt)
```

Merge with line numbers.

```bash
paste <(nl names.txt) departments.txt
```

Create a CSV.

```bash
paste -d "," names.txt departments.txt countries.txt > employees.csv
```

---

# Common paste Options

| Option | Description |
|----------|-------------|
| `-d` | Specify delimiter |
| `-s` | Serial mode |
| `--` | End option processing |

---

# Difference Between cat and paste

| Command | Behavior |
|----------|----------|
| `cat` | Combines files vertically |
| `paste` | Combines files horizontally |

Example:

**cat**

```text
Alice

Bob

Engineering

HR
```

**paste**

```text
Alice Engineering

Bob HR
```

---

# Real Production Examples

Merge usernames and user IDs.

```bash
paste \
<(cut -d ":" -f1 /etc/passwd) \
<(cut -d ":" -f3 /etc/passwd)
```

Generate CSV reports.

```bash
paste -d "," names.txt salaries.txt
```

Merge monitoring reports.

```bash
paste cpu.txt memory.txt disk.txt
```

Combine Kubernetes reports.

```bash
paste pods.txt nodes.txt
```

Create inventory files.

```bash
paste hostname.txt ip.txt
```

---

# Production Perspective

The `paste` command is useful for:

- Creating CSV reports
- Combining inventory data
- Joining monitoring outputs
- Merging configuration values
- Building shell automation reports

It is commonly used together with `cut`, `sort`, and shell scripts.

---

# Hands-on Lab

## Task 1

Create:

```bash
cat > names.txt
```

```text
Rahul

Priya

Arjun

Neha
```

---

## Task 2

Create:

```bash
cat > marks.txt
```

```text
80

90

85

95
```

---

## Task 3

Merge.

```bash
paste names.txt marks.txt
```

---

## Task 4

Use commas.

```bash
paste -d "," names.txt marks.txt
```

---

## Task 5

Create departments.

```bash
cat > departments.txt
```

```text
CSE

IT

ECE

CSE
```

---

## Task 6

Merge three files.

```bash
paste names.txt departments.txt marks.txt
```

---

## Task 7

Serial mode.

```bash
paste -s names.txt
```

---

## Task 8

Create CSV.

```bash
paste -d "," names.txt departments.txt marks.txt > students.csv
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `paste file1 file2` | Merge two files | Reports |
| `paste -d ","` | CSV output | Data export |
| `paste -s` | Merge lines serially | One-line output |
| `paste file1 file2 file3` | Merge multiple files | Inventory reports |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    An administrator has three files.

**servers.txt**

```text
server01

server02

server03
```

**status.txt**

```text
Running

Stopped

Running
```

**ip.txt**

```text
10.0.0.10

10.0.0.11

10.0.0.12
```

Tasks:

1. Merge all files.
2. Create a CSV report.
3. Display all servers on one line.
4. Save the report.

Solutions:

```bash
paste servers.txt status.txt ip.txt

paste -d "," servers.txt status.txt ip.txt

paste -s servers.txt

paste -d "," servers.txt status.txt ip.txt > report.csv
```

---

# Mini Challenge

Create:

**employees.txt**

```text
Alice

Bob

Charlie

David
```

**salary.txt**

```text
85000

60000

90000

75000
```

**department.txt**

```text
Engineering

HR

Finance

DevOps
```

Perform the following:

- Merge all files.
- Create a comma-separated report.
- Display employee names in a single line.
- Save the merged output.
- Verify the saved file.

---

# Best Practices

- Ensure all files have the same number of lines.
- Use `-d ","` when generating CSV files.
- Use serial mode (`-s`) for one-line output.
- Combine `paste` with `cut` and `sort` for automation.
- Validate merged output before importing into other systems.

---

# Common Mistakes

❌ Assuming `paste` joins files vertically.

✅ It joins them **horizontally**.

---

❌ Forgetting that the default delimiter is a tab.

✅ Use:

```bash
paste -d ","
```

for CSV files.

---

❌ Merging files with different line counts.

✅ If one file has fewer lines, the corresponding fields will be empty.

---

# Interview Questions
## Beginner

1. What is the purpose of the `paste` command?
2. What delimiter does `paste` use by default?
3. How do you change the delimiter?
4. What does `paste -s` do?

---

## Intermediate

1. What is the difference between `cat` and `paste`?
2. How do you merge three files into a CSV?
3. What happens when files have different numbers of lines?
4. When is `paste` preferable to `join`?

---

## Architect Level

1. How would you generate a combined infrastructure inventory report using `paste`?
2. Why is `paste` useful in shell scripting and automation?
3. How would you combine `cut`, `sort`, and `paste` to prepare deployment reports?

---

# Summary

In this lesson, you learned:

- Merging files horizontally
- Using custom delimiters
- Creating CSV output
- Using serial mode
- Combining command outputs
- Production report generation

The `paste` command is a simple but powerful utility for combining related data from multiple files. It is especially useful in shell scripting, report generation, and automation workflows.

---

## Key Takeaways

- `paste` merges files horizontally.
- The default delimiter is a tab.
- Use `-d` to specify a custom delimiter.
- Use `-s` to combine all lines from a file into a single line.
- `paste` is commonly used to create CSV reports and combine related datasets.

---

## What's Next?

**[join Command — Joining Files Using a Common Field](text-processing-join.md)**

In the next lesson, you'll learn:

- Joining files using a common key
- Working with sorted files
- Customizing join fields
- Producing database-style reports
- Real-world inventory and user management examples
