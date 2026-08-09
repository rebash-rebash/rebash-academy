---
title: "Input — Accepting User Input in Bash Scripts"
description: "Handle Bash input — read prompts, command-line arguments, password input, validation, defaults, and production scripting patterns."
difficulty: intermediate
estimated_time: "80 min"
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
  - input
  - automation
  - rebash-linux-mastery
comments: false
status: ready
---

# Input — Accepting User Input in Bash Scripts

> **Input** allows Bash scripts to interact with users, accept command-line arguments, read data from files, and process information from standard input. Interactive scripts become more flexible because they can work with different values each time they are executed instead of relying on hardcoded data. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, and Site Reliability Engineer (SRE) should understand how to safely collect and validate user input in production scripts.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 10: Bash Scripting → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 80 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Bash Scripting</div>

<div markdown>**Lesson:** 6 of 11</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Read user input
- Use command-line arguments
- Display interactive prompts
- Validate user input
- Read passwords securely
- Use default values
- Process multiple inputs
- Apply input handling in production scripts

---

# Prerequisites

Complete:

- Modules 1–9
- Module 10 Lessons 1–5

---

# Why Learn Input?

Imagine creating a user account script.

Without input:

```bash
useradd basha
```

The script creates only one user.

Using input:

```bash
read -p "Enter username: " USERNAME

useradd "$USERNAME"
```

The same script can create any user.

---

# What is Input?

Input is data provided to a script.

It may come from:

- User keyboard input
- Command-line arguments
- Files
- Pipes
- Other commands

---

# Reading User Input

Basic syntax:

```bash
read VARIABLE
```

Example:

```bash
echo "Enter your name:"

read NAME

echo "Hello $NAME"
```

---

# Reading with a Prompt

Instead of using `echo`, display the prompt directly.

```bash
read -p "Enter your city: " CITY

echo "$CITY"
```

---

# Reading Multiple Values

```bash
read FIRST LAST

echo "$FIRST"

echo "$LAST"
```

Input:

```text
John Doe
```

Output:

```text
John

Doe
```

---

# Reading Passwords

Hide user input while typing.

```bash
read -s -p "Password: " PASSWORD

echo
```

The password is not displayed on the screen.

---

# Command-Line Arguments

Arguments are values passed when running a script.

Example:

```bash
./backup.sh /home
```

Inside the script:

```bash
echo "$1"
```

Output:

```text
/home
```

---

# Special Variables

| Variable | Description |
|----------|-------------|
| `$0` | Script name |
| `$1` | First argument |
| `$2` | Second argument |
| `$@` | All arguments |
| `$#` | Number of arguments |
| `$$` | Current process ID |
| `$?` | Exit status of previous command |

---

# Checking Argument Count

```bash
if [ $# -lt 1 ]
then
    echo "Usage: ./script.sh <directory>"

    exit 1
fi
```

---

# Loop Through Arguments

```bash
for ARG in "$@"
do
    echo "$ARG"
done
```

---

# Using Default Values

```bash
NAME=${1:-Guest}

echo "Hello $NAME"
```

If no argument is supplied:

```text
Hello Guest
```

---

# Input Validation

Example:

```bash
read -p "Enter age: " AGE

if [[ "$AGE" =~ ^[0-9]+$ ]]
then
    echo "Valid"

else
    echo "Invalid"
fi
```

---

# Confirm User Action

```bash
read -p "Continue? (y/n): " ANSWER

if [[ "$ANSWER" == "y" ]]
then
    echo "Continuing..."
else
    echo "Cancelled."
fi
```

---

# Reading a File

```bash
while read LINE
do
    echo "$LINE"
done < users.txt
```

---

# Reading from a Pipe

```bash
echo "Linux" | while read VALUE
do
    echo "$VALUE"
done
```

---

# Common Commands

Read input.

```bash
read NAME
```

Prompt user.

```bash
read -p "Enter value: " VALUE
```

Read password.

```bash
read -s PASSWORD
```

Display arguments.

```bash
echo "$@"
```

Argument count.

```bash
echo "$#"
```

---

# Real Production Examples

Create user.

```bash
read -p "Username: " USER

sudo useradd "$USER"
```

Accept deployment environment.

```bash
ENVIRONMENT=${1:-development}

echo "$ENVIRONMENT"
```

Restart a service.

```bash
read -p "Service: " SERVICE

systemctl restart "$SERVICE"
```

---

# Production Perspective

Input handling is commonly used in:

- Deployment scripts
- Backup automation
- User management
- Cloud provisioning
- Infrastructure automation
- Monitoring tools
- Configuration scripts
- Interactive administration utilities

Proper validation helps prevent errors and improves script reliability.

---

# Hands-on Lab

## Task 1

Read a user's name.

```bash
read -p "Enter your name: " NAME

echo "$NAME"
```

---

## Task 2

Read multiple values.

```bash
read FIRST LAST

echo "$FIRST"

echo "$LAST"
```

---

## Task 3

Read a password.

```bash
read -s -p "Password: " PASSWORD

echo
```

---

## Task 4

Display the first argument.

```bash
echo "$1"
```

Run:

```bash
./script.sh Linux
```

---

## Task 5

Display all arguments.

```bash
echo "$@"
```

---

## Task 6

Display the argument count.

```bash
echo "$#"
```

---

## Task 7

Validate numeric input.

```bash
read AGE

if [[ "$AGE" =~ ^[0-9]+$ ]]
then
    echo "Valid"
else
    echo "Invalid"
fi
```

---

## Task 8

Read a file line by line.

```bash
while read LINE
do
    echo "$LINE"
done < users.txt
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `read` | Read user input | Interactive scripts |
| `read -p` | Display prompt | User-friendly input |
| `read -s` | Read password | Secure authentication |
| `$1`, `$2` | Command-line arguments | Deployment scripts |
| `$@` | All arguments | Batch processing |
| `$#` | Number of arguments | Input validation |

---

# Common Input Mistakes

| Mistake | Solution |
|----------|----------|
| Not validating input | Always validate |
| Assuming arguments exist | Check `$#` |
| Displaying passwords | Use `read -s` |
| Forgetting quotes | Quote variables |
| Hardcoding values | Accept user input |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A deployment script fails because no environment name is supplied.

Before:

```bash
kubectl apply -f "$1"
```

If no argument is passed:

```text
No such file
```

Improved:

```bash
if [ $# -lt 1 ]
then
    echo "Usage: ./deploy.sh <manifest>"

    exit 1
fi
```

The script now validates input before execution.

---

# Best Practices

- Validate all user input.
- Check command-line arguments before use.
- Use secure password input with `read -s`.
- Quote variables to prevent word splitting.
- Provide meaningful prompts.
- Display usage information for missing arguments.
- Handle invalid input gracefully.

---

# Common Mistakes

❌ Assuming users always provide valid input.

✅ Verify users always provide valid input instead of assuming it.

---

❌ Not checking command-line arguments.

✅ Always checking command-line arguments.

---

❌ Displaying passwords on the terminal.

✅ Avoid this mistake: displaying passwords on the terminal.

---

❌ Forgetting to quote input variables.

✅ Remember to to quote input variables.

---

❌ Proceeding without validating required values.

✅ Avoid this mistake: proceeding without validating required values.

---

# Interview Questions
## Beginner

1. What does the `read` command do?
2. What is `$1`?
3. What does `$#` represent?
4. How do you securely read a password?

---

## Intermediate

1. What is the difference between keyboard input and command-line arguments?
2. How do you validate user input?
3. What does `$@` represent?
4. How do you provide default values for missing arguments?

---

## Architect Level

1. How would you design secure interactive Bash scripts?
2. Why is input validation important in production automation?
3. How can improper input handling create security risks?

---

# Summary

In this lesson, you learned:

- Reading user input
- Interactive prompts
- Command-line arguments
- Password input
- Input validation
- Default values
- Reading from files
- Production scripting best practices

Input handling enables Bash scripts to interact with users and accept dynamic data. By validating input and handling errors gracefully, you can build secure, reliable, and production-ready automation scripts.

---

## Key Takeaways

- Use `read` to accept keyboard input.
- Use command-line arguments for script flexibility.
- Validate all user-provided data.
- Use `read -s` for passwords.
- Check `$#` before accessing arguments.
- Provide meaningful prompts and usage messages.

---

## What's Next?

**[Exit Codes — Understanding Command Success and Failure in Bash](bash-exit-codes.md)**

You'll explore:

- What exit codes are
- Standard Linux exit codes
- Using the `exit` command
- Checking command status
- Using `$?`
- Returning exit codes from functions
- Production error handling

By the end of the lesson, you'll be able to use exit codes effectively to build reliable Bash scripts that detect failures, communicate status, and integrate seamlessly with automation tools and CI/CD pipelines.
