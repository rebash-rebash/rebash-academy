---
title: "Command History"
description: "View, search, reuse, and manage Bash command history with history, !!, Ctrl+R, HISTSIZE, and production-safe shortcuts."
difficulty: beginner
estimated_time: "20 min"
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
  - history
  - command-line
  - rebash-linux-mastery
comments: false
status: ready
---

# Command History

> Every command you execute in the Linux shell is recorded in your command history. Learning how to view, search, reuse, and manage command history can dramatically improve your productivity and help you work faster on Linux systems.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 2: Linux Command Line Essentials → Lesson 8</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 20 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Linux Command Line Essentials</div>

<div markdown>**Lesson:** 8 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand how Bash stores command history
- View and search previous commands
- Re-execute commands from history
- Customize history behavior
- Clear and manage history safely
- Improve productivity using history shortcuts

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 Lessons 1–7

---

# Why Learn Command History?

Imagine you previously executed a complex command like:

```bash
kubectl get pods --all-namespaces --sort-by=.metadata.creationTimestamp
```

Instead of typing it again, Linux allows you to retrieve it instantly.

Command history helps you:

- Save time
- Reduce typing errors
- Repeat complex commands
- Troubleshoot efficiently
- Learn from previously executed commands

---

# What is Command History?

Bash automatically records the commands you execute during a session.

Example:

```bash
pwd

ls -la

cd /etc

cat hosts

history
```

Each command is assigned a unique history number.

---

# Display Command History

```bash
history
```

Example output:

```text
1 pwd

2 ls -la

3 cd /etc

4 cat hosts

5 history
```

---

# Display Last Few Commands

Display the last five commands:

```bash
history 5
```

Example:

```text
96 ls

97 pwd

98 whoami

99 date

100 history
```

---

# Execute Previous Commands

Run a command by its history number.

Example:

```bash
!98
```

Executes command number **98**.

---

# Execute the Last Command

Run the previous command again.

```bash
!!
```

Example:

```bash
sudo !!
```

Scenario:

```bash
apt update
```

Permission denied.

Instead of typing again:

```bash
sudo !!
```

Bash automatically executes:

```bash
sudo apt update
```

This is one of the most useful Bash shortcuts.

---

# Execute Commands by Prefix

Run the most recent command starting with:

```bash
!git
```

If your previous command was:

```bash
git status
```

It runs automatically.

Other examples:

```bash
!kubectl

!docker

!terraform
```

---

# Search Command History

One of Bash's most powerful features.

Press:

```text
Ctrl + R
```

Example:

Search:

```text
docker
```

Output:

```text
(reverse-i-search)`docker':
docker ps -a
```

Press:

- **Ctrl + R** again for older matches
- **Enter** to execute
- **Esc** to edit before execution

---

# Search Using grep

Display commands containing a keyword.

```bash
history | grep docker
```

Example:

```text
15 docker ps

18 docker images

20 docker logs
```

Another example:

```bash
history | grep kubectl
```

---

# History File

Bash stores history in:

```text
~/.bash_history
```

View it:

```bash
cat ~/.bash_history
```

---

# History Variables

Display history size.

```bash
echo $HISTSIZE
```

Example:

```text
1000
```

Display history file size.

```bash
echo $HISTFILESIZE
```

Example:

```text
2000
```

View history file location.

```bash
echo $HISTFILE
```

Output:

```text
/home/basha/.bash_history
```

---

# Customize History Size

Temporary change:

```bash
HISTSIZE=5000
```

Persistent change:

Edit:

```bash
nano ~/.bashrc
```

Add:

```bash
HISTSIZE=5000

HISTFILESIZE=10000
```

Apply changes:

```bash
source ~/.bashrc
```

---

# Ignore Duplicate Commands

Prevent consecutive duplicate commands.

```bash
export HISTCONTROL=ignoredups
```

Ignore duplicates and commands beginning with a space.

```bash
export HISTCONTROL=ignoreboth
```

---

# Ignore Specific Commands

Example:

```bash
export HISTIGNORE="ls:pwd:history"
```

These commands won't be saved.

---

# Clear Command History

Clear the current session.

```bash
history -c
```

Clear and save.

```bash
history -c

history -w
```

---

# Delete a Specific Entry

Delete history entry number 45.

```bash
history -d 45
```

---

# Append Current Session

Write current session to history file.

```bash
history -a
```

Read history file.

```bash
history -r
```

Rewrite history file.

```bash
history -w
```

---

# Useful Keyboard Shortcuts

| Shortcut | Purpose |
|-----------|----------|
| ↑ | Previous command |
| ↓ | Next command |
| Ctrl + R | Reverse search |
| Ctrl + P | Previous command |
| Ctrl + N | Next command |
| !! | Previous command |
| !number | Execute command by number |
| !string | Execute last command starting with string |

---

# Command Summary

| Command | Purpose |
|----------|----------|
| history | Display history |
| history 10 | Last 10 commands |
| !! | Previous command |
| !25 | Execute command 25 |
| !git | Execute last git command |
| history -c | Clear history |
| history -d | Delete entry |
| history \| grep | Search history |

---

# Production Perspective

Command history is extremely useful for:

- Recovering previously used commands
- Debugging production issues
- Repeating deployment commands
- Auditing troubleshooting steps
- Learning from experienced administrators

Example:

```bash
history | grep kubectl

history | grep docker

history | grep terraform

history | grep ansible
```

During an incident, engineers often search history to reuse working commands quickly.

---

# Hands-on Lab

## Task 1

View command history.

```bash
history
```

---

## Task 2

Display the last 10 commands.

```bash
history 10
```

---

## Task 3

Search for `ls`.

```bash
history | grep ls
```

---

## Task 4

Run the previous command.

```bash
!!
```

---

## Task 5

Display history file.

```bash
cat ~/.bash_history
```

---

## Task 6

Display history variables.

```bash
echo $HISTSIZE

echo $HISTFILESIZE
```

---

## Task 7

Try reverse search.

```text
Ctrl + R
```

Search for:

```text
history
```

---

# Command Deep Dive

| Command | Purpose | Common Options | Production Example |
|----------|----------|----------------|--------------------|
| history | Display command history | `-c`, `-d`, `-a`, `-w` | Review previous troubleshooting steps |
| !! | Execute previous command | Default | Retry failed command with `sudo` |
| !number | Execute by history number | Default | Repeat deployment command |
| Ctrl + R | Search history | Interactive | Find previous `kubectl` commands |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    An application stopped responding after a deployment.

    You need to determine what commands were executed earlier.

Tasks:

1. Display recent history.
2. Search for `kubectl` commands.
3. Search for `docker` commands.
4. Re-run the last `systemctl` command.
5. Save the current session history.

Example:

```bash
history

history | grep kubectl

history | grep docker

!systemctl

history -a
```

---

# Mini Challenge

Perform the following:

1. Execute at least 10 Linux commands.
2. Display your command history.
3. Search for `ls`.
4. Search for `cd`.
5. Execute the last `pwd` command using history.
6. Display your history file.
7. Delete one history entry.
8. Clear the current session history.

---

# Best Practices

- Use **Ctrl + R** instead of retyping long commands.
- Increase `HISTSIZE` for larger command history.
- Ignore duplicate commands to keep history clean.
- Avoid storing sensitive commands containing passwords.
- Review history during troubleshooting to retrace your steps.

---

# Common Mistakes

❌ Re-typing long commands repeatedly.

✅ Use:

```text
Ctrl + R
```

---

❌ Clearing history without understanding the consequences.

✅ Use:

```bash
history -c
```

This removes the current session history.

---

❌ Assuming history is shared across all users.

✅ Each user has their own history file.

---

# Interview Questions
## Beginner

1. What command displays Bash history?
2. What does `!!` do?
3. How do you search command history?
4. Where is Bash history stored?

---

## Intermediate

1. Explain `HISTSIZE` and `HISTFILESIZE`.
2. How do you ignore duplicate commands?
3. What is the purpose of `history -a` and `history -w`?
4. How do you execute a command by its history number?

---

## Architect Level

1. How can command history improve incident response?
2. What are the security considerations when storing command history?
3. How would you configure history for administrators on production servers?

---

# Summary

In this lesson, you learned:

- Viewing command history
- Searching history
- Re-executing previous commands
- Managing history files
- Customizing history behavior
- Productivity shortcuts

Command history is one of Bash's most valuable features. Mastering it will help you work faster, avoid repetitive typing, and troubleshoot systems more efficiently.

---

## Key Takeaways

- `history` displays previously executed commands.
- `Ctrl + R` is the fastest way to search command history.
- `!!` repeats the last command.
- `!number` executes a command by its history number.
- `HISTSIZE` and `HISTFILESIZE` control history storage.
- Command history can significantly improve productivity and troubleshooting.

---

## What's Next?

**[Input, Output, Pipes, and Redirection](redirection.md)**

In the next lesson, you'll learn:

- Standard Input (`stdin`)
- Standard Output (`stdout`)
- Standard Error (`stderr`)
- Output redirection (`>`, `>>`)
- Input redirection (`<`)
- Pipes (`|`)
- The `tee` command
- Building powerful Linux command pipelines
