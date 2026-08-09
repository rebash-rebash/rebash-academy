---
title: "Environment Variables in Linux — Configuring the Linux Environment"
description: "Configure Linux with environment variables — use env, printenv, export, and PATH for shells, scripts, Docker, Kubernetes, and production apps."
difficulty: intermediate
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 5 · Users and Groups"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - environment-variables
  - path
  - export
  - shell
  - rebash-linux-mastery
comments: false
status: ready
---

# Environment Variables in Linux — Configuring the Linux Environment

> Environment variables are dynamic values maintained by the operating system that influence how programs, shells, and scripts behave. They store information such as user details, executable paths, language settings, application configurations, and runtime parameters. Environment variables are fundamental to Linux administration, shell scripting, DevOps, Docker, Kubernetes, and cloud computing.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 5: Users and Groups → Lesson 5</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 55 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Users and Groups</div>

<div markdown>**Lesson:** 5 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand environment variables
- Differentiate shell variables and environment variables
- View existing variables
- Create environment variables
- Export variables
- Remove variables
- Configure the PATH variable
- Apply environment variables in production

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management and Permissions
- Module 5 Lessons 1–4

---

# Why Learn Environment Variables?

Imagine you install Java.

Instead of running:

```bash
/usr/lib/jvm/java-21/bin/java
```

every time,

you simply run:

```bash
java
```

How does Linux know where Java is installed?

The answer is:

**Environment Variables**, especially the **PATH** variable.

---

# What is an Environment Variable?

An environment variable is a **name-value pair** stored by the shell.

Example:

```text
USER=basha

HOME=/home/basha

SHELL=/bin/bash
```

Applications use these values to determine how they should run.

---

# Shell Variables vs Environment Variables

| Shell Variable | Environment Variable |
|---------------|----------------------|
| Available only in the current shell | Available to child processes |
| Not inherited | Inherited by child processes |
| Created with `VAR=value` | Exported using `export` |

---

# Viewing Environment Variables

Display all environment variables.

```bash
env
```

or

```bash
printenv
```

Example:

```text
HOME=/home/basha

USER=basha

PATH=/usr/bin:/bin

SHELL=/bin/bash
```

---

# Display a Specific Variable

Syntax:

```bash
echo $VARIABLE
```

Examples:

```bash
echo $USER

echo $HOME

echo $PATH

echo $SHELL
```

---

# Common Environment Variables

| Variable | Description |
|----------|-------------|
| `USER` | Current username |
| `HOME` | User's home directory |
| `PATH` | Executable search path |
| `PWD` | Current directory |
| `OLDPWD` | Previous directory |
| `SHELL` | Current shell |
| `HOSTNAME` | System hostname |
| `LANG` | System language |
| `TERM` | Terminal type |
| `LOGNAME` | Login username |

---

# Creating a Shell Variable

```bash
CITY=Hyderabad
```

Verify:

```bash
echo $CITY
```

Output:

```text
Hyderabad
```

This variable exists only in the current shell.

---

# Exporting an Environment Variable

```bash
export CITY=Hyderabad
```

Verify:

```bash
printenv CITY
```

Output:

```text
Hyderabad
```

Now child processes can access it.

---

# Difference Between Shell and Environment Variables

Create a shell variable.

```bash
PROJECT=REBASH
```

Open a new shell.

```bash
bash
```

Check:

```bash
echo $PROJECT
```

Output:

```text

```

The variable is not available.

Now export it.

```bash
export PROJECT=REBASH
```

Open another shell.

```bash
bash
```

Check again.

```bash
echo $PROJECT
```

Output:

```text
REBASH
```

---

# Removing Variables

```bash
unset PROJECT
```

Verify.

```bash
echo $PROJECT
```

Output:

```text

```

---

# Understanding PATH

Display:

```bash
echo $PATH
```

Example:

```text
/usr/local/bin:/usr/bin:/bin:/usr/sbin
```

When you run:

```bash
python
```

Linux searches each directory in `PATH` until it finds the executable.

---

# Adding a Directory to PATH

Temporarily:

```bash
export PATH=$PATH:/opt/tools/bin
```

Verify:

```bash
echo $PATH
```

Now executables inside `/opt/tools/bin` can be run without specifying the full path.

---

# Environment Variables in Scripts

Example:

```bash
#!/bin/bash

echo "User: $USER"

echo "Home: $HOME"

echo "Shell: $SHELL"
```

Run:

```bash
bash info.sh
```

---

# Listing Shell Variables

```bash
set
```

This displays:

- Shell variables
- Environment variables
- Functions

---

# Finding One Variable

```bash
printenv HOME

printenv PATH
```

---

# Common Commands

Display all variables.

```bash
env

printenv
```

Display one variable.

```bash
echo $HOME
```

Create variable.

```bash
PROJECT=REBASH
```

Export variable.

```bash
export PROJECT=REBASH
```

Remove variable.

```bash
unset PROJECT
```

Display all shell variables.

```bash
set
```

---

# Real Production Examples

Set Java Home.

```bash
export JAVA_HOME=/usr/lib/jvm/java-21
```

Configure Python.

```bash
export PYTHONPATH=/opt/python
```

Update PATH.

```bash
export PATH=$PATH:/opt/scripts
```

Configure Kubernetes.

```bash
export KUBECONFIG=~/.kube/config
```

Configure AWS CLI.

```bash
export AWS_PROFILE=production
```

---

# Production Perspective

Environment variables are heavily used in:

- Shell scripting
- Docker containers
- Kubernetes Pods
- Jenkins pipelines
- GitHub Actions
- GitLab CI/CD
- Python applications
- Java applications
- Node.js applications

Most modern applications read configuration from environment variables rather than hardcoded values.

---

# Hands-on Lab

## Task 1

Display all environment variables.

```bash
env
```

---

## Task 2

Display your username.

```bash
echo $USER
```

---

## Task 3

Display your home directory.

```bash
echo $HOME
```

---

## Task 4

Display your PATH.

```bash
echo $PATH
```

---

## Task 5

Create a variable.

```bash
PROJECT=REBASH
```

Display it.

```bash
echo $PROJECT
```

---

## Task 6

Export the variable.

```bash
export PROJECT
```

Verify.

```bash
printenv PROJECT
```

---

## Task 7

Remove the variable.

```bash
unset PROJECT
```

---

## Task 8

List all shell variables.

```bash
set
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `env` | Display environment variables | Troubleshooting |
| `printenv` | Display environment variables | Scripts |
| `echo $VAR` | Display variable value | Verification |
| `export` | Create environment variable | Application configuration |
| `unset` | Remove variable | Cleanup |
| `set` | Display shell variables | Debugging |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A Java application fails to start.

Error:

```text
JAVA_HOME is not set
```

Investigation:

```bash
echo $JAVA_HOME

printenv JAVA_HOME
```

The variable is missing.

Solution:

```bash
export JAVA_HOME=/usr/lib/jvm/java-21

export PATH=$JAVA_HOME/bin:$PATH
```

Verify:

```bash
java -version
```

The application now starts successfully.

---

# Best Practices

- Use uppercase names for environment variables.
- Keep variable names descriptive.
- Avoid storing sensitive information (such as passwords or API keys) directly in environment variables on shared systems unless required and properly protected.
- Use `export` only for variables that child processes need.
- Configure permanent variables in profile files rather than setting them manually every session.

---

# Common Mistakes

❌ Forgetting to export variables.

✅ Shell variables are not inherited by child processes.

---

❌ Overwriting the PATH variable.

✅ Incorrect:

```bash
export PATH=/opt/tools
```

Correct:

```bash
export PATH=$PATH:/opt/tools
```

---

❌ Hardcoding application paths in scripts instead of using environment variables.

✅ Prefer using environment variables rather than hardcoding application paths in scripts.

---

# Interview Questions
## Beginner

1. What is an environment variable?
2. Which command displays all environment variables?
3. What is the purpose of the PATH variable?
4. How do you display the value of an environment variable?

---

## Intermediate

1. Explain the difference between shell variables and environment variables.
2. What does the `export` command do?
3. How do you add a directory to the PATH?
4. How do you remove an environment variable?

---

## Architect Level

1. Why are environment variables widely used in cloud-native applications?
2. How do Docker and Kubernetes use environment variables?
3. What are the security considerations when storing configuration in environment variables?

---

# Summary

In this lesson, you learned:

- Environment variables
- Shell variables
- Viewing variables
- Creating variables
- Exporting variables
- Removing variables
- PATH
- Production use cases

Environment variables are a core part of Linux and modern application deployment. They allow applications and scripts to be configured without changing source code, making them an essential tool for Linux administrators, DevOps engineers, and cloud architects.

---

## Key Takeaways

- Environment variables store configuration values used by the shell and applications.
- Use `env` or `printenv` to display environment variables.
- Use `export` to make variables available to child processes.
- Use `unset` to remove variables.
- The `PATH` variable determines where Linux searches for executable programs.
- Environment variables are widely used in automation, containers, and cloud-native applications.

---

## What's Next?

**[Linux Profiles — Configuring User Login Environments](shell-profiles.md)**

You'll explore:

- Login vs non-login shells
- `/etc/profile`
- `~/.profile`
- `~/.bash_profile`
- `/etc/environment`
- Shell startup sequence
- Configuring persistent environment settings

Understanding profile files will help you make environment variables and shell settings permanent across login sessions.
