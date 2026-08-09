---
title: "Variables — Storing and Managing Data in Bash Scripts"
description: "Master Bash variables — assignment rules, quoting, command substitution, environment variables, export, and production scripting practices."
difficulty: beginner
estimated_time: "70 min"
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
  - variables
  - automation
  - rebash-linux-mastery
comments: false
status: ready
---

# Variables — Storing and Managing Data in Bash Scripts

> **Variables** are the foundation of every Bash script. A variable stores a value that can be reused throughout a script, making automation flexible, reusable, and easier to maintain. Instead of hardcoding values, scripts use variables to store filenames, user input, command output, configuration values, and system information. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, and Site Reliability Engineer (SRE) should master variables to write efficient and production-ready Bash scripts.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 10: Bash Scripting → Lesson 1</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 70 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Bash Scripting</div>

<div markdown>**Lesson:** 1 of 11</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Bash variables
- Create and use variables
- Follow variable naming rules
- Work with environment variables
- Store command output in variables
- Read user input into variables
- Understand variable scope
- Apply variable best practices

---

# Prerequisites

Complete:

- Modules 1–9 of Linux Mastery

---

# Why Learn Variables?

Imagine writing a backup script.

Without variables:

```bash
cp /home/basha/data.txt /backup/

tar -czf /backup/data.tar.gz /backup/

echo "Backup stored in /backup"
```

If the backup location changes, every occurrence must be updated.

Using variables:

```bash
BACKUP_DIR="/backup"

cp /home/basha/data.txt $BACKUP_DIR

tar -czf $BACKUP_DIR/data.tar.gz $BACKUP_DIR

echo "Backup stored in $BACKUP_DIR"
```

Only one value needs to change.

---

# What is a Variable?

A variable is a named container that stores data.

Example:

```text
USERNAME

↓

basha
```

Whenever the script references `USERNAME`, Bash substitutes the stored value.

---

# Creating Variables

Syntax:

```bash
VARIABLE=value
```

Example:

```bash
NAME="Basha"
```

Display the value.

```bash
echo $NAME
```

Output:

```text
Basha
```

---

# Important Syntax Rules

Correct:

```bash
CITY="Hyderabad"
```

Incorrect:

```bash
CITY = "Hyderabad"
```

Spaces around `=` are **not allowed**.

---

# Variable Naming Rules

Variable names:

- May contain letters
- May contain numbers
- May contain underscores (`_`)
- Cannot begin with a number
- Cannot contain spaces

Valid:

```bash
USERNAME

server_ip

BACKUP_DIR
```

Invalid:

```text
2user

server-ip

backup dir
```

---

# Using Variables

Reference a variable using `$`.

Example:

```bash
USER="linux"

echo $USER
```

Output:

```text
linux
```

---

# Using Curly Braces

Curly braces improve readability.

```bash
FILE="backup"

echo "${FILE}.tar.gz"
```

Output:

```text
backup.tar.gz
```

---

# String Variables

```bash
GREETING="Hello"

NAME="Basha"

echo "$GREETING $NAME"
```

Output:

```text
Hello Basha
```

---

# Numeric Variables

```bash
COUNT=10

echo $COUNT
```

Output:

```text
10
```

---

# Arithmetic Operations

Use arithmetic expansion.

```bash
A=20

B=10

echo $((A+B))
```

Output:

```text
30
```

Other operations:

```bash
echo $((A-B))

echo $((A*B))

echo $((A/B))
```

---

# Command Substitution

Store command output.

```bash
DATE=$(date)
```

Display:

```bash
echo $DATE
```

Another example:

```bash
HOST=$(hostname)

echo $HOST
```

---

# Reading User Input

```bash
read NAME

echo "Hello $NAME"
```

Prompt the user.

```bash
read -p "Enter your name: " NAME
```

---

# Environment Variables

Environment variables are available to the shell and child processes.

View one variable.

```bash
echo $HOME
```

Common environment variables:

| Variable | Description |
|----------|-------------|
| `HOME` | User's home directory |
| `USER` | Current username |
| `PATH` | Executable search path |
| `PWD` | Current working directory |
| `SHELL` | Current shell |
| `HOSTNAME` | System hostname |

View all environment variables.

```bash
env
```

---

# Export Variables

Make a variable available to child processes.

```bash
export APP_ENV=production
```

Verify.

```bash
echo $APP_ENV
```

---

# Unset Variables

Remove a variable.

```bash
unset APP_ENV
```

---

# Quotes in Variables

Double quotes allow variable expansion.

```bash
NAME="Linux"

echo "Hello $NAME"
```

Single quotes prevent expansion.

```bash
echo 'Hello $NAME'
```

Output:

```text
Hello $NAME
```

---

# Common Commands

Create variable.

```bash
NAME="Linux"
```

Display variable.

```bash
echo $NAME
```

Read input.

```bash
read NAME
```

Export variable.

```bash
export APP_ENV=production
```

Remove variable.

```bash
unset APP_ENV
```

Display environment variables.

```bash
env
```

---

# Real Production Examples

Store backup directory.

```bash
BACKUP_DIR="/backup"
```

Store hostname.

```bash
HOST=$(hostname)
```

Store current date.

```bash
DATE=$(date +%F)
```

Generate backup filename.

```bash
FILE="backup-$DATE.tar.gz"
```

---

# Production Perspective

Variables are used extensively in:

- Backup automation
- Deployment scripts
- CI/CD pipelines
- Kubernetes automation
- Infrastructure provisioning
- Monitoring scripts
- Cloud automation
- Configuration management

Well-designed scripts avoid hardcoded values and rely on variables for flexibility.

---

# Hands-on Lab

## Task 1

Create a variable.

```bash
NAME="Linux"
```

Display it.

```bash
echo $NAME
```

---

## Task 2

Store your username.

```bash
USER_NAME=$USER

echo $USER_NAME
```

---

## Task 3

Store today's date.

```bash
TODAY=$(date +%F)

echo $TODAY
```

---

## Task 4

Perform arithmetic.

```bash
A=25

B=15

echo $((A+B))
```

---

## Task 5

Read user input.

```bash
read -p "Enter your city: " CITY

echo $CITY
```

---

## Task 6

Display environment variables.

```bash
env
```

---

## Task 7

Export a variable.

```bash
export ENVIRONMENT=development
```

---

## Task 8

Remove the variable.

```bash
unset ENVIRONMENT
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `echo` | Display variable value | Debugging |
| `read` | Read user input | Interactive scripts |
| `export` | Export variable | Environment configuration |
| `unset` | Remove variable | Cleanup |
| `env` | Display environment variables | Troubleshooting |
| `$(command)` | Store command output | Dynamic values |

---

# Common Variable Mistakes

| Mistake | Solution |
|----------|----------|
| Spaces around `=` | Remove spaces |
| Missing `$` | Use `$VARIABLE` |
| Invalid variable names | Follow naming rules |
| Forgetting quotes | Quote strings containing spaces |
| Hardcoding values | Use variables instead |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A backup script suddenly begins writing backups to the wrong directory.

Investigation:

```bash
echo $BACKUP_DIR
```

Output:

```text
(empty)
```

The variable was never initialized.

Solution:

```bash
BACKUP_DIR="/backup"

echo $BACKUP_DIR
```

The script now writes backups to the correct location.

---

# Best Practices

- Use descriptive variable names.
- Follow uppercase naming for constants.
- Quote variables when appropriate.
- Avoid hardcoded values.
- Use command substitution for dynamic values.
- Export variables only when necessary.

---

# Common Mistakes

❌ Adding spaces around `=`.

✅ Avoid this mistake: adding spaces around `=`.

---

❌ Forgetting `$` when referencing variables.

✅ Remember to `$` when referencing variables.

---

❌ Using invalid variable names.

✅ Avoid using invalid variable names when a safer approach exists.

---

❌ Hardcoding paths and configuration values.

✅ Avoid this mistake: hardcoding paths and configuration values.

---

❌ Not quoting variables containing spaces.

✅ Always quoting variables containing spaces.

---

# Interview Questions
## Beginner

1. What is a variable?
2. How do you create a variable in Bash?
3. How do you display a variable?
4. What does `$HOME` represent?

---

## Intermediate

1. What is command substitution?
2. What is the difference between local and environment variables?
3. Why is `export` used?
4. What is the difference between single and double quotes?

---

## Architect Level

1. How would you design reusable Bash scripts using variables?
2. Why should configuration values be stored in variables instead of hardcoded?
3. How would you securely manage sensitive values in Bash scripts?

---

# Summary

In this lesson, you learned:

- Variables
- Variable naming rules
- Variable expansion
- Environment variables
- Command substitution
- User input
- Arithmetic operations
- Production scripting best practices

Variables are the building blocks of Bash scripting. They make scripts reusable, maintainable, and dynamic by allowing values to be stored, modified, and reused throughout the script. Mastering variables is the first step toward writing professional automation scripts.

---

## Key Takeaways

- Variables store reusable data in Bash scripts.
- Variable assignment does not allow spaces around `=`.
- Use `$` to access variable values.
- Use `$(command)` to capture command output.
- Use `export` to make variables available to child processes.
- Avoid hardcoding values by using descriptive variables.

---

## What's Next?

**[Conditions — Making Decisions in Bash Scripts](bash-conditions.md)**

You'll explore:

- `if` statements
- `if-else` and `elif`
- Comparison operators
- File test operators
- String and numeric comparisons
- Logical operators
- Nested conditions
- Production scripting examples

By the end of the lesson, you'll be able to make intelligent decisions in Bash scripts based on user input, file states, command results, and system conditions.
