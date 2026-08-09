---
title: "Bash Basics"
description: "Bash (Bourne Again SHell) is the most widely used shell in Linux. Learn Bash syntax, variables, quoting, command substitution, PATH, aliases, and exit codes."
difficulty: beginner
estimated_time: "25 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 2 · Linux Command Line Essentials"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - bash
  - shell
  - command-line
  - rebash-linux-mastery
comments: false
status: ready
---

# Bash Basics

> Bash (Bourne Again SHell) is the most widely used shell in Linux. It allows you to interact with the operating system, automate repetitive tasks, and write powerful shell scripts. Every Linux Administrator, DevOps Engineer, Cloud Engineer, and SRE should master Bash.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 2: Linux Command Line Essentials → Lesson 2</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 25 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Linux Command Line Essentials</div>

<div markdown>**Lesson:** 2 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand what Bash is
- Execute commands in Bash
- Understand Bash syntax
- Use variables
- Understand quoting
- Use command substitution
- Work with environment variables
- Customize your Bash prompt
- Learn Bash best practices

---

# Prerequisites

Before starting this lesson, you should complete:

- Module 1 – Linux Fundamentals
- Understanding the Shell

---

# What is Bash?

**Bash** stands for:

> **Bourne Again SHell**

It is the default shell on most Linux distributions.

Bash acts as a command interpreter between the user and the Linux kernel.

```text
User

↓

Bash

↓

Linux Kernel

↓

Hardware
```

Whenever you type a command:

```bash
ls
```

Bash interprets the command and asks the Linux kernel to execute it.

---

# Why Bash is Important

Bash is everywhere.

It is used for:

- Linux Administration
- DevOps Automation
- Cloud Infrastructure
- Kubernetes Management
- CI/CD Pipelines
- Docker Automation
- Server Maintenance

If you know Bash, you can automate almost every Linux task.

---

# Your First Bash Commands

Display current user:

```bash
whoami
```

Display current directory:

```bash
pwd
```

List files:

```bash
ls
```

Create directory:

```bash
mkdir rebash
```

Delete directory:

```bash
rmdir rebash
```

Display date:

```bash
date
```

Every command follows this pattern:

```text
Command

↓

Arguments

↓

Options
```

Example:

```bash
ls -la /home
```

| Part | Description |
|------|-------------|
| ls | Command |
| -la | Options |
| /home | Argument |

---

# Running Multiple Commands

Commands can be chained together.

Run one after another:

```bash
pwd

date

whoami
```

Run on one line:

```bash
pwd && date && whoami
```

Meaning:

- Execute the next command only if the previous one succeeds.

---

Using semicolon:

```bash
pwd ; date ; whoami
```

Meaning:

- Execute every command regardless of success or failure.

---

# Bash Variables

Variables store values.

Create a variable:

```bash
NAME="REBASH"
```

Display:

```bash
echo $NAME
```

Output:

```text
REBASH
```

Another example:

```bash
CITY="Hyderabad"

echo $CITY
```

---

# Rules for Variable Names

Valid:

```bash
NAME

CITY

user_name

PORT
```

Invalid:

```bash
123NAME

my-name

first name
```

---

# Built-in Environment Variables

Display current user:

```bash
echo $USER
```

Home directory:

```bash
echo $HOME
```

Current shell:

```bash
echo $SHELL
```

Current working directory:

```bash
echo $PWD
```

Hostname:

```bash
echo $HOSTNAME
```

PATH variable:

```bash
echo $PATH
```

---

# Understanding PATH

When you type:

```bash
ls
```

Bash searches for the executable inside directories listed in the PATH variable.

View PATH:

```bash
echo $PATH
```

Example:

```text
/usr/local/bin

/usr/bin

/bin

/usr/sbin
```

Search process:

```text
User types:

ls

↓

Bash checks PATH

↓

Finds:

/usr/bin/ls

↓

Executes program
```

---

# Quoting in Bash

Bash supports three types of quotes.

---

## Double Quotes

Variables are expanded.

```bash
NAME="Linux"

echo "Welcome to $NAME"
```

Output:

```text
Welcome to Linux
```

---

## Single Quotes

Variables are **not** expanded.

```bash
echo 'Welcome to $NAME'
```

Output:

```text
Welcome to $NAME
```

---

## No Quotes

```bash
echo Hello
```

Output:

```text
Hello
```

---

# Command Substitution

Store command output inside a variable.

Old style:

```bash
DATE=`date`
```

Recommended:

```bash
DATE=$(date)
```

Display:

```bash
echo $DATE
```

Example:

```bash
HOST=$(hostname)

echo $HOST
```

---

# Command History

Display previous commands:

```bash
history
```

Run a previous command:

```bash
!25
```

Run previous command:

```bash
!!
```

Search history:

```text
Ctrl + R
```

---

# Auto Completion

Press:

```text
Tab
```

Example:

```bash
cd Doc<TAB>
```

Automatically becomes:

```bash
cd Documents/
```

This reduces typing mistakes.

---

# Aliases

Aliases create shortcuts.

Example:

```bash
alias ll="ls -la"
```

Now:

```bash
ll
```

works like:

```bash
ls -la
```

View aliases:

```bash
alias
```

Remove:

```bash
unalias ll
```

---

# Customizing the Prompt

Current prompt:

```text
basha@rebash:~$
```

Temporarily change:

```bash
PS1="REBASH> "
```

Output:

```text
REBASH>
```

Useful for demonstrations and scripting.

---

# Exit Status

Every Linux command returns an exit code.

Display it:

```bash
echo $?
```

Common values:

| Exit Code | Meaning |
|-----------|----------|
| 0 | Success |
| Non-zero | Failure |

Example:

```bash
mkdir demo

echo $?
```

Output:

```text
0
```

---

# Production Perspective

Bash powers many production workflows.

Examples:

```bash
kubectl get pods

docker ps

git pull

terraform apply

ansible-playbook site.yml

systemctl restart nginx
```

Almost every DevOps automation begins with Bash.

---

# Hands-on Lab

## Task 1

Display:

```bash
echo $USER

echo $HOME

echo $PWD

echo $SHELL
```

---

## Task 2

Create variables.

```bash
NAME="REBASH"

CITY="Hyderabad"

echo $NAME

echo $CITY
```

---

## Task 3

Display PATH.

```bash
echo $PATH
```

---

## Task 4

Practice command substitution.

```bash
TODAY=$(date)

echo $TODAY
```

---

## Task 5

Create alias.

```bash
alias ll="ls -la"

ll
```

---

## Task 6

Check exit code.

```bash
mkdir test

echo $?

rm -r test

echo $?
```

---

# Mini Challenge

Without referring to the lesson:

Create variables:

- Your Name
- Company
- City

Print:

```text
Welcome <Name>

You work at <Company>

Current Directory

Today's Date

Hostname
```

Use:

- Variables
- Command substitution
- echo

---

# Best Practices

- Use meaningful variable names.
- Prefer `$(command)` over backticks.
- Use aliases for frequently used commands.
- Understand exit codes before scripting.
- Learn keyboard shortcuts to improve productivity.

---

# Common Mistakes

❌ Forgetting `$` while reading variables.

✅ Use:

```bash
echo NAME
```

Outputs:

```text
NAME
```

Correct:

```bash
echo $NAME
```

---

❌ Using spaces around `=`.

✅ Incorrect:

```bash
NAME = Linux
```

Correct:

```bash
NAME="Linux"
```

---

❌ Using single quotes when variable expansion is required.

✅ Incorrect:

```bash
echo '$USER'
```

Correct:

```bash
echo "$USER"
```

---

# Interview Questions
## Beginner

1. What is Bash?
2. What does Bash stand for?
3. How do you create a variable?
4. What is PATH?
5. What is command substitution?

---

## Intermediate

1. Explain Bash command execution.
2. Difference between single and double quotes.
3. What is an alias?
4. Explain exit codes.
5. Why is PATH important?

---

## Architect Level

1. Why is Bash still relevant in Cloud Computing?
2. How does Bash improve DevOps automation?
3. Why should engineers understand shell environment variables?

---

# Summary

In this lesson, you learned:

- What Bash is
- Running commands
- Variables
- Environment variables
- PATH
- Quoting
- Command substitution
- Aliases
- Exit codes
- Bash productivity tips

These concepts form the foundation for Bash scripting, Linux administration, and DevOps automation.

---

## Key Takeaways

- Bash is the default shell on most Linux systems.
- Variables store values and make scripts reusable.
- Environment variables configure your shell environment.
- PATH determines where Bash looks for executables.
- Command substitution allows commands to be embedded inside other commands.
- Understanding exit codes is essential for writing reliable automation.

---

## What's Next?

**[Navigating the Filesystem](navigating-the-filesystem.md)**

In the next lesson, you'll learn:

- Absolute vs Relative Paths
- `cd`
- `pwd`
- `ls`
- Directory navigation
- Hidden files
- Tab completion
- Efficient filesystem navigation techniques
