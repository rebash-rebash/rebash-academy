---
title: "Conditions — Making Decisions in Bash Scripts"
description: "Write Bash conditional logic — if, else, elif, numeric and string comparisons, file tests, logical operators, and production validation patterns."
difficulty: intermediate
estimated_time: "85 min"
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
  - conditions
  - automation
  - rebash-linux-mastery
comments: false
status: ready
---

# Conditions — Making Decisions in Bash Scripts

> **Conditions** allow Bash scripts to make decisions based on user input, command results, file existence, variable values, or system state. Instead of executing every command sequentially, a script can choose different execution paths depending on whether a condition is true or false. Conditional statements are one of the most important features of Bash scripting and are used extensively in automation, DevOps, cloud infrastructure, monitoring, deployment pipelines, and Linux system administration.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 10: Bash Scripting → Lesson 2</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 85 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Bash Scripting</div>

<div markdown>**Lesson:** 2 of 11</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand conditional statements
- Write `if`, `else`, and `elif` statements
- Compare numbers and strings
- Test files and directories
- Use logical operators
- Check command exit status
- Write nested conditions
- Apply conditions in production scripts

---

# Prerequisites

Complete:

- Modules 1–9
- Module 10 Lesson 1 – Variables

---

# Why Learn Conditions?

Imagine writing a backup script.

Without conditions:

```bash
cp /data/* /backup/
```

If `/backup` doesn't exist, the script fails.

With conditions:

```bash
if [ -d "/backup" ]; then
    cp /data/* /backup/
else
    echo "Backup directory not found."
fi
```

The script behaves intelligently.

---

# What is a Condition?

A condition evaluates whether something is:

- True
- False

Based on the result, Bash executes different code.

Example:

```text
Is User Root?

↓

Yes

↓

Run Administrative Tasks

OR

No

↓

Display Error
```

---

# Basic if Statement

Syntax:

```bash
if [ condition ]
then
    commands
fi
```

Example:

```bash
AGE=20

if [ $AGE -ge 18 ]
then
    echo "Adult"
fi
```

Output:

```text
Adult
```

---

# if...else

Syntax:

```bash
if [ condition ]
then
    commands
else
    commands
fi
```

Example:

```bash
AGE=16

if [ $AGE -ge 18 ]
then
    echo "Adult"
else
    echo "Minor"
fi
```

---

# if...elif...else

Useful for multiple decisions.

```bash
MARKS=75

if [ $MARKS -ge 90 ]
then
    echo "Grade A"

elif [ $MARKS -ge 75 ]
then
    echo "Grade B"

else
    echo "Grade C"
fi
```

---

# Numeric Comparison Operators

| Operator | Meaning |
|----------|---------|
| `-eq` | Equal |
| `-ne` | Not Equal |
| `-gt` | Greater Than |
| `-ge` | Greater Than or Equal |
| `-lt` | Less Than |
| `-le` | Less Than or Equal |

Example:

```bash
if [ $A -gt $B ]
then
    echo "A is larger"
fi
```

---

# String Comparison Operators

| Operator | Meaning |
|----------|---------|
| `=` | Equal |
| `!=` | Not Equal |
| `-z` | Empty String |
| `-n` | Not Empty |

Example:

```bash
NAME="Linux"

if [ "$NAME" = "Linux" ]
then
    echo "Matched"
fi
```

---

# File Test Operators

| Operator | Description |
|----------|-------------|
| `-f` | Regular file exists |
| `-d` | Directory exists |
| `-e` | File or directory exists |
| `-r` | Readable |
| `-w` | Writable |
| `-x` | Executable |
| `-s` | File is not empty |

Example:

```bash
if [ -f "/etc/passwd" ]
then
    echo "File exists"
fi
```

---

# Checking Directories

```bash
if [ -d "/backup" ]
then
    echo "Directory exists"
fi
```

---

# Checking Empty Strings

```bash
if [ -z "$USERNAME" ]
then
    echo "Username missing"
fi
```

---

# Logical AND

Using `&&` inside `[[ ]]`.

```bash
AGE=25

if [[ $AGE -ge 18 && $AGE -le 60 ]]
then
    echo "Working Age"
fi
```

---

# Logical OR

```bash
if [[ "$ROLE" = "admin" || "$ROLE" = "root" ]]
then
    echo "Administrator"
fi
```

---

# Logical NOT

```bash
if [ ! -f "/tmp/test.txt" ]
then
    echo "File not found"
fi
```

---

# Nested Conditions

```bash
if [ $AGE -ge 18 ]
then
    if [ "$COUNTRY" = "India" ]
    then
        echo "Eligible"
    fi
fi
```

---

# Checking Command Success

Every Linux command returns an exit code.

Example:

```bash
mkdir test

if [ $? -eq 0 ]
then
    echo "Directory created successfully"
fi
```

A better approach:

```bash
if mkdir test
then
    echo "Directory created"
else
    echo "Creation failed"
fi
```

---

# Common Commands

Check file.

```bash
if [ -f file.txt ]
```

Check directory.

```bash
if [ -d backup ]
```

Check equality.

```bash
if [ $A -eq $B ]
```

Check string.

```bash
if [ "$NAME" = "Linux" ]
```

---

# Real Production Examples

Verify backup directory.

```bash
if [ -d "/backup" ]
then
    echo "Backup directory found"
fi
```

Check configuration file.

```bash
if [ -f "/etc/nginx/nginx.conf" ]
then
    echo "Configuration exists"
fi
```

Verify root user.

```bash
if [ "$EUID" -eq 0 ]
then
    echo "Running as root"
fi
```

---

# Production Perspective

Conditions are widely used in:

- Backup scripts
- Deployment automation
- CI/CD pipelines
- Kubernetes automation
- Monitoring scripts
- Cloud provisioning
- Infrastructure validation
- Security checks

Nearly every production Bash script contains conditional logic.

---

# Hands-on Lab

## Task 1

Check a number.

```bash
NUMBER=10

if [ $NUMBER -gt 5 ]
then
    echo "Greater"
fi
```

---

## Task 2

Compare strings.

```bash
NAME="Linux"

if [ "$NAME" = "Linux" ]
then
    echo "Correct"
fi
```

---

## Task 3

Check file existence.

```bash
if [ -f "/etc/passwd" ]
then
    echo "Found"
fi
```

---

## Task 4

Check directory.

```bash
if [ -d "/tmp" ]
then
    echo "Directory exists"
fi
```

---

## Task 5

Use `if...else`.

```bash
AGE=15

if [ $AGE -ge 18 ]
then
    echo "Adult"
else
    echo "Minor"
fi
```

---

## Task 6

Use logical AND.

```bash
if [[ $AGE -ge 18 && $AGE -le 60 ]]
then
    echo "Working Age"
fi
```

---

## Task 7

Use `elif`.

```bash
MARKS=82

if [ $MARKS -ge 90 ]
then
    echo "A"
elif [ $MARKS -ge 75 ]
then
    echo "B"
else
    echo "C"
fi
```

---

## Task 8

Check command success.

```bash
if mkdir demo
then
    echo "Success"
else
    echo "Failed"
fi
```

---

# Command Deep Dive

| Command/Operator | Purpose | Production Example |
|------------------|----------|--------------------|
| `if` | Execute conditionally | Automation |
| `else` | Alternate execution | Error handling |
| `elif` | Multiple conditions | Decision making |
| `-f` | File exists | Config validation |
| `-d` | Directory exists | Backup verification |
| `$?` | Previous command status | Deployment validation |

---

# Common Condition Mistakes

| Mistake | Solution |
|----------|----------|
| Missing spaces around `[` and `]` | Add spaces |
| Missing `fi` | Close every `if` block |
| Using `=` for numeric comparison | Use `-eq`, `-gt`, etc. |
| Forgetting quotes around strings | Quote string variables |
| Ignoring command exit codes | Check command success |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A deployment script fails because the configuration file is missing.

Solution:

```bash
if [ -f "/etc/myapp/config.yaml" ]
then
    echo "Configuration found"
else
    echo "Configuration missing"
    exit 1
fi
```

The script exits safely before attempting deployment.

---

# Best Practices

- Keep conditions simple and readable.
- Quote string variables.
- Check file existence before using files.
- Validate command success.
- Use descriptive variable names.
- Handle unexpected conditions gracefully.

---

# Common Mistakes

❌ Forgetting the closing `fi`.

✅ Remember to the closing `fi`.

---

❌ Using incorrect comparison operators.

✅ Avoid using incorrect comparison operators when a safer approach exists.

---

❌ Not quoting string variables.

✅ Always quoting string variables.

---

❌ Ignoring failed commands.

✅ Always review failed commands.

---

❌ Creating deeply nested conditions instead of simplifying logic.

✅ Prefer simplifying logic rather than creating deeply nested conditions.

---

# Interview Questions
## Beginner

1. What is an `if` statement?
2. What is the purpose of `else`?
3. What does `-f` check?
4. What does `-d` check?

---

## Intermediate

1. What is the difference between `=` and `-eq`?
2. What is the purpose of `elif`?
3. How do you check whether a command succeeded?
4. What is the difference between `-z` and `-n`?

---

## Architect Level

1. How would you design defensive Bash scripts using conditions?
2. How would you validate production configuration before deployment?
3. Why should production scripts check every critical operation before continuing?

---

# Summary

In this lesson, you learned:

- Conditional statements
- `if`, `else`, and `elif`
- Numeric comparisons
- String comparisons
- File tests
- Logical operators
- Nested conditions
- Command exit status
- Production scripting best practices

Conditions allow Bash scripts to make intelligent decisions based on system state, user input, command results, and file availability. They are fundamental to building reliable, flexible, and production-ready automation.

---

## Key Takeaways

- Conditions enable decision-making in Bash scripts.
- Use `if`, `else`, and `elif` for branching logic.
- Use appropriate operators for numeric, string, and file comparisons.
- Check command success before proceeding.
- Quote string variables to avoid unexpected behavior.
- Validate inputs and system state before performing critical operations.

---

## What's Next?

**[Loops — Automating Repetitive Tasks in Bash Scripts](bash-loops.md)**

You'll explore:

- `for` loops
- `while` loops
- `until` loops
- Loop control statements (`break` and `continue`)
- Iterating through files and directories
- Reading files line by line
- Production automation examples

By the end of the lesson, you'll be able to automate repetitive tasks efficiently using loops, making your Bash scripts more powerful and scalable.
