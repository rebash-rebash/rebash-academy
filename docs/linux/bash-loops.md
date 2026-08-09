---
title: "Loops — Automating Repetitive Tasks in Bash Scripts"
description: "Automate with Bash loops — for, while, until, break, continue, file iteration, and production monitoring patterns."
difficulty: intermediate
estimated_time: "90 min"
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
  - loops
  - automation
  - rebash-linux-mastery
comments: false
status: ready
---

# Loops — Automating Repetitive Tasks in Bash Scripts

> **Loops** allow Bash scripts to execute a block of code repeatedly until a specified condition is met or a collection of items has been processed. Instead of writing the same commands multiple times, loops enable automation with fewer lines of code, making scripts more efficient, scalable, and maintainable. Loops are extensively used in Linux administration, DevOps, cloud automation, infrastructure management, monitoring, and deployment pipelines.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 10: Bash Scripting → Lesson 3</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Bash Scripting</div>

<div markdown>**Lesson:** 3 of 11</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand loops
- Use `for` loops
- Use `while` loops
- Use `until` loops
- Iterate through files and directories
- Read files line by line
- Control loops using `break` and `continue`
- Apply loops in production automation

---

# Prerequisites

Complete:

- Modules 1–9
- Module 10 Lessons 1–2

---

# Why Learn Loops?

Imagine backing up multiple directories.

Without loops:

```bash
tar -czf home.tar.gz /home

tar -czf etc.tar.gz /etc

tar -czf var.tar.gz /var
```

Using a loop:

```bash
for DIR in /home /etc /var
do
    tar -czf "$(basename $DIR).tar.gz" "$DIR"
done
```

The script becomes shorter, reusable, and easier to maintain.

---

# What is a Loop?

A loop repeatedly executes a block of commands.

Example:

```text
Start

↓

Condition

↓

Execute Commands

↓

Repeat

↓

Exit
```

---

# Types of Loops

Bash supports:

- `for`
- `while`
- `until`

Each is useful in different scenarios.

---

# for Loop

The `for` loop is used when iterating over a known list of items.

Syntax:

```bash
for VARIABLE in LIST
do
    commands
done
```

Example:

```bash
for NAME in Alice Bob Charlie
do
    echo "$NAME"
done
```

Output:

```text
Alice

Bob

Charlie
```

---

# Numeric for Loop

Using brace expansion:

```bash
for i in {1..5}
do
    echo $i
done
```

Output:

```text
1

2

3

4

5
```

---

# C-Style for Loop

```bash
for (( i=1; i<=5; i++ ))
do
    echo $i
done
```

---

# Loop Through Files

```bash
for FILE in *.txt
do
    echo "$FILE"
done
```

---

# Loop Through Directories

```bash
for DIR in /home/*/
do
    echo "$DIR"
done
```

---

# while Loop

A `while` loop runs as long as the condition is true.

Syntax:

```bash
while [ condition ]
do
    commands
done
```

Example:

```bash
COUNT=1

while [ $COUNT -le 5 ]
do
    echo $COUNT
    COUNT=$((COUNT+1))
done
```

---

# Reading a File Line by Line

```bash
while read LINE
do
    echo "$LINE"
done < users.txt
```

This technique is widely used for processing configuration files and logs.

---

# until Loop

An `until` loop executes until a condition becomes true.

Syntax:

```bash
until [ condition ]
do
    commands
done
```

Example:

```bash
COUNT=1

until [ $COUNT -gt 5 ]
do
    echo $COUNT
    COUNT=$((COUNT+1))
done
```

---

# break Statement

`break` exits a loop immediately.

Example:

```bash
for i in {1..10}
do
    if [ $i -eq 5 ]
    then
        break
    fi

    echo $i
done
```

Output:

```text
1

2

3

4
```

---

# continue Statement

`continue` skips the current iteration.

Example:

```bash
for i in {1..5}
do
    if [ $i -eq 3 ]
    then
        continue
    fi

    echo $i
done
```

Output:

```text
1

2

4

5
```

---

# Nested Loops

Loops can be placed inside other loops.

```bash
for i in {1..3}
do
    for j in {1..2}
    do
        echo "$i $j"
    done
done
```

---

# Infinite Loop

```bash
while true
do
    echo "Running..."
    sleep 5
done
```

Stop using:

```text
Ctrl + C
```

---

# Common Commands

Simple loop.

```bash
for i in {1..5}
```

While loop.

```bash
while [ condition ]
```

Until loop.

```bash
until [ condition ]
```

Exit loop.

```bash
break
```

Skip iteration.

```bash
continue
```

---

# Real Production Examples

Backup multiple directories.

```bash
for DIR in /home /etc /var
do
    tar -czf "$(basename $DIR).tar.gz" "$DIR"
done
```

Check multiple servers.

```bash
for HOST in server1 server2 server3
do
    ping -c1 "$HOST"
done
```

Process log file.

```bash
while read LINE
do
    echo "$LINE"
done < access.log
```

---

# Production Perspective

Loops are widely used in:

- Backup automation
- Log processing
- CI/CD pipelines
- Infrastructure provisioning
- Cloud automation
- Kubernetes administration
- Server monitoring
- Configuration management

Most production Bash scripts rely on loops to automate repetitive tasks.

---

# Hands-on Lab

## Task 1

Print numbers.

```bash
for i in {1..10}
do
    echo $i
done
```

---

## Task 2

Print file names.

```bash
for FILE in *
do
    echo "$FILE"
done
```

---

## Task 3

Create five directories.

```bash
for i in {1..5}
do
    mkdir "project$i"
done
```

---

## Task 4

Use a while loop.

```bash
COUNT=1

while [ $COUNT -le 5 ]
do
    echo $COUNT
    COUNT=$((COUNT+1))
done
```

---

## Task 5

Read a file.

```bash
while read LINE
do
    echo "$LINE"
done < /etc/passwd
```

---

## Task 6

Use `break`.

```bash
for i in {1..10}
do
    [ $i -eq 6 ] && break
    echo $i
done
```

---

## Task 7

Use `continue`.

```bash
for i in {1..5}
do
    [ $i -eq 3 ] && continue
    echo $i
done
```

---

## Task 8

Create an infinite loop.

```bash
while true
do
    date
    sleep 2
done
```

Stop it with:

```text
Ctrl + C
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `for` | Iterate over items | File processing |
| `while` | Repeat while condition is true | Monitoring |
| `until` | Repeat until condition becomes true | Retry logic |
| `break` | Exit loop | Error handling |
| `continue` | Skip current iteration | Filtering |
| `read` | Read input line by line | Log processing |

---

# Common Loop Mistakes

| Mistake | Solution |
|----------|----------|
| Missing `done` | Close every loop |
| Infinite loop | Update loop condition |
| Forgetting to increment variables | Modify loop counter |
| Using the wrong loop type | Choose the appropriate loop |
| Not quoting filenames | Quote variables containing paths |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A monitoring script should check multiple servers.

Without loops:

```bash
ping server1

ping server2

ping server3
```

Using a loop:

```bash
for HOST in server1 server2 server3
do
    if ping -c1 "$HOST" >/dev/null
    then
        echo "$HOST is reachable"
    else
        echo "$HOST is down"
    fi
done
```

The script is easier to maintain and can scale to hundreds of servers.

---

# Best Practices

- Choose the appropriate loop type.
- Keep loop bodies simple.
- Avoid unnecessary nested loops.
- Quote filenames and variables.
- Use `break` and `continue` to improve readability.
- Test loops with small datasets before running them in production.

---

# Common Mistakes

❌ Forgetting the closing `done`.

✅ Remember to the closing `done`.

---

❌ Creating unintended infinite loops.

✅ Avoid this mistake: creating unintended infinite loops.

---

❌ Not updating loop variables.

✅ Always updating loop variables.

---

❌ Using `for` when `while` is more appropriate.

✅ Avoid using `for` when `while` is more appropriate when a safer approach exists.

---

❌ Processing filenames without quoting variables.

✅ Avoid this mistake: processing filenames without quoting variables.

---

# Interview Questions
## Beginner

1. What is a loop?
2. What are the three loop types in Bash?
3. What is the purpose of a `for` loop?
4. What is the purpose of a `while` loop?

---

## Intermediate

1. What is the difference between `while` and `until`?
2. What does `break` do?
3. What does `continue` do?
4. How do you read a file line by line in Bash?

---

## Architect Level

1. How would you automate server health checks using loops?
2. How would you process thousands of log files efficiently?
3. How can poorly designed loops affect production systems?

---

# Summary

In this lesson, you learned:

- `for` loops
- `while` loops
- `until` loops
- Nested loops
- Reading files line by line
- `break`
- `continue`
- Production automation techniques

Loops are one of the most powerful features of Bash scripting. They eliminate repetitive code, simplify automation, and enable scripts to process files, users, servers, and system resources efficiently. Mastering loops is essential for writing scalable and production-ready Bash scripts.

---

## Key Takeaways

- Loops automate repetitive tasks.
- Use `for` loops when the number of iterations is known.
- Use `while` loops when execution depends on a condition.
- Use `until` loops to repeat until a condition becomes true.
- Use `break` to exit loops and `continue` to skip iterations.
- Keep loops simple, efficient, and easy to read.

---

## What's Next?

**[Functions — Writing Reusable Code in Bash Scripts](bash-functions.md)**

You'll explore:

- Creating functions
- Function parameters
- Returning values
- Variable scope
- Reusable code
- Organizing large scripts
- Production scripting best practices

By the end of the lesson, you'll be able to build modular, reusable Bash scripts using functions, making your automation easier to maintain and scale.
