---
title: "tr Command — Translating and Transforming Text in Linux"
description: "Transform text with tr — case conversion, character delete/replace, squeeze repeats, and POSIX classes in Linux pipelines."
difficulty: intermediate
estimated_time: "30 min"
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
  - tr
  - text-processing
  - command-line
  - rebash-linux-mastery
comments: false
status: ready
---

# tr Command — Translating and Transforming Text in Linux

> The `tr` (translate) command is used to transform, replace, delete, and compress characters from standard input. It is one of the most useful Linux text-processing utilities for formatting data, cleaning text, converting letter cases, and preparing data for scripts and automation.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 3: Text Processing → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 30 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Text Processing</div>

<div markdown>**Lesson:** 6 of 18</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `tr` command
- Replace characters
- Convert lowercase to uppercase
- Convert uppercase to lowercase
- Delete characters
- Remove repeated characters
- Process command output
- Use `tr` in shell pipelines

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 Lessons 1–5

---

# Why Learn tr?

Imagine you receive inconsistent user input.

```text
linux
Linux
LINUX
LiNuX
```

You want everything in uppercase.

Instead of editing manually:

```bash
echo "linux" | tr 'a-z' 'A-Z'
```

Output:

```text
LINUX
```

This is a common task in automation and shell scripting.

---

# What is tr?

`tr` stands for:

> **Translate**

It reads text from **Standard Input (stdin)** and transforms it.

Unlike commands such as `cat` or `grep`, `tr` **does not read files directly**.

Syntax:

```bash
tr [OPTIONS] SET1 [SET2]
```

Most commonly used with pipes:

```bash
cat file.txt | tr ...
```

or

```bash
echo "text" | tr ...
```

---

# Character Translation

Replace one character with another.

```bash
echo "Linux" | tr 'L' 'W'
```

Output:

```text
Winux
```

---

Replace spaces with underscores.

```bash
echo "REBASH Academy" | tr ' ' '_'
```

Output:

```text
REBASH_Academy
```

---

# Convert Lowercase to Uppercase

```bash
echo "linux" | tr 'a-z' 'A-Z'
```

Output:

```text
LINUX
```

---

Another example:

```bash
echo "docker kubernetes" | tr 'a-z' 'A-Z'
```

Output:

```text
DOCKER KUBERNETES
```

---

# Convert Uppercase to Lowercase

```bash
echo "LINUX" | tr 'A-Z' 'a-z'
```

Output:

```text
linux
```

---

# Using POSIX Character Classes

Instead of ranges:

```bash
tr 'a-z' 'A-Z'
```

Use:

```bash
tr '[:lower:]' '[:upper:]'
```

Convert to lowercase:

```bash
tr '[:upper:]' '[:lower:]'
```

POSIX character classes are more portable across different locales.

---

# Delete Characters

Remove vowels.

```bash
echo "Linux Administration" | tr -d 'aeiouAEIOU'
```

Output:

```text
Lnx dmnstrtn
```

---

Remove spaces.

```bash
echo "Hello World" | tr -d ' '
```

Output:

```text
HelloWorld
```

---

Remove digits.

```bash
echo "Server123" | tr -d '0-9'
```

Output:

```text
Server
```

---

# Squeeze Repeated Characters

Suppose:

```text
Linux     Docker      Kubernetes
```

Compress repeated spaces.

```bash
echo "Linux     Docker      Kubernetes" | tr -s ' '
```

Output:

```text
Linux Docker Kubernetes
```

---

Compress repeated blank lines.

```bash
cat file.txt | tr -s '\n'
```

---

# Replace Tabs

Convert tabs to spaces.

```bash
cat file.txt | tr '\t' ' '
```

---

# Replace Colons

Example:

```text
basha:x:1000:1000
```

Command:

```bash
echo "basha:x:1000:1000" | tr ':' ','
```

Output:

```text
basha,x,1000,1000
```

---

# One Character Per Line

Display every character on its own line.

```bash
echo "Linux" | tr '' '\n'
```

A more common approach is:

```bash
echo "Linux" | fold -w1
```

---

# Combining with Pipes

Convert usernames to uppercase.

```bash
cut -d ":" -f1 /etc/passwd | tr 'a-z' 'A-Z'
```

Remove spaces.

```bash
cat names.txt | tr -d ' '
```

Count words.

```bash
cat file.txt | tr ' ' '\n' | wc -l
```

Convert log entries.

```bash
grep ERROR app.log | tr '[:lower:]' '[:upper:]'
```

---

# Common tr Options

| Option | Description |
|----------|-------------|
| `-d` | Delete characters |
| `-s` | Squeeze repeated characters |
| `-c` | Complement character set |
| `-t` | Truncate SET1 to match SET2 |

---

# Real Production Examples

Convert usernames.

```bash
cut -d ":" -f1 /etc/passwd | tr '[:lower:]' '[:upper:]'
```

Remove spaces from configuration values.

```bash
cat config.txt | tr -d ' '
```

Normalize CSV delimiters.

```bash
cat data.csv | tr ';' ','
```

Clean log output.

```bash
journalctl | tr '[:upper:]' '[:lower:]'
```

Prepare environment variables.

```bash
echo "production" | tr '[:lower:]' '[:upper:]'
```

---

# Production Perspective

The `tr` command is commonly used for:

- Data cleanup
- Case conversion
- Formatting reports
- Removing unwanted characters
- Normalizing input
- Preparing text for shell scripts

It is lightweight, fast, and works exceptionally well in command pipelines.

---

# Hands-on Lab

## Task 1

Convert to uppercase.

```bash
echo "linux" | tr 'a-z' 'A-Z'
```

---

## Task 2

Convert to lowercase.

```bash
echo "LINUX" | tr 'A-Z' 'a-z'
```

---

## Task 3

Replace spaces.

```bash
echo "REBASH Academy" | tr ' ' '_'
```

---

## Task 4

Delete vowels.

```bash
echo "Cloud Computing" | tr -d 'aeiouAEIOU'
```

---

## Task 5

Remove digits.

```bash
echo "Server2026" | tr -d '0-9'
```

---

## Task 6

Compress spaces.

```bash
echo "Linux     Docker     Kubernetes" | tr -s ' '
```

---

## Task 7

Convert usernames.

```bash
cut -d ":" -f1 /etc/passwd | tr '[:lower:]' '[:upper:]'
```

---

## Task 8

Replace commas.

```bash
echo "A,B,C,D" | tr ',' ';'
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `tr 'a-z' 'A-Z'` | Uppercase conversion | Normalize input |
| `tr 'A-Z' 'a-z'` | Lowercase conversion | Standardize logs |
| `tr -d` | Delete characters | Remove spaces or digits |
| `tr -s` | Compress repeats | Clean formatted reports |
| `tr ':' ','` | Replace delimiters | Convert data formats |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    An operations team receives a user report with inconsistent formatting.

```text
alice

BOB

Charlie

david
```

Tasks:

1. Convert all names to uppercase.
2. Remove blank spaces.
3. Replace commas with semicolons.
4. Compress multiple spaces into one.
5. Remove numeric characters from usernames.

Solutions:

```bash
cat users.txt | tr '[:lower:]' '[:upper:]'

cat users.txt | tr -d ' '

cat users.txt | tr ',' ';'

cat users.txt | tr -s ' '

cat users.txt | tr -d '0-9'
```

---

# Mini Challenge

Create:

```text
users.txt
```

Contents:

```text
alice

BOB

Charlie

David123

Dev Ops Team
```

Perform the following:

- Convert all text to uppercase.
- Convert all text to lowercase.
- Remove digits.
- Replace spaces with underscores.
- Remove repeated spaces.
- Replace underscores back with spaces.

---

# Best Practices

- Remember that `tr` reads from **standard input**, not directly from files.
- Prefer POSIX character classes (`[:upper:]`, `[:lower:]`) for portability.
- Use `tr -s` to clean repeated delimiters.
- Combine `tr` with `cut`, `grep`, `sort`, and `awk` for efficient text processing.
- Test transformations on sample data before using them in production scripts.

---

# Common Mistakes

❌ Trying to use `tr` directly on a file.

✅ Incorrect:

```bash
tr 'a-z' 'A-Z' file.txt
```

Correct:

```bash
cat file.txt | tr 'a-z' 'A-Z'
```

or

```bash
tr 'a-z' 'A-Z' < file.txt
```

---

❌ Expecting `tr` to replace words.

✅ `tr` works on **individual characters**, not words.

Use `sed` for word replacement.

---

❌ Forgetting that `tr` preserves line structure.

✅ It transforms characters but does not rearrange lines.

---

# Interview Questions
## Beginner

1. What does the `tr` command do?
2. How do you convert lowercase to uppercase?
3. Which option deletes characters?
4. What does `tr -s` do?

---

## Intermediate

1. Why does `tr` work with standard input instead of files?
2. What is the advantage of using POSIX character classes?
3. How do you replace commas with tabs?
4. When should you use `tr` instead of `sed`?

---

## Architect Level

1. How would you normalize inconsistent log data before analysis?
2. Why is `tr` frequently used in shell scripts and CI/CD pipelines?
3. How can `tr` improve data quality in automation workflows?

---

# Summary

In this lesson, you learned:

- Character translation
- Case conversion
- Character deletion
- Character replacement
- Squeezing repeated characters
- Using `tr` in command pipelines
- Production text transformation techniques

The `tr` command is a fast and efficient tool for character-level transformations. It is widely used in Linux administration, automation, and shell scripting to clean and normalize text.

---

## Key Takeaways

- `tr` performs **character-by-character** transformations.
- It reads input from **stdin**.
- Use `-d` to delete characters.
- Use `-s` to squeeze repeated characters.
- Prefer POSIX character classes for portability.
- Use `sed` when you need to replace words or patterns instead of individual characters.

---

## What's Next?

**[wc Command — Counting Lines, Words, Characters, and Bytes in Linux](text-processing-wc.md)**

In the next lesson, you'll learn:

- Counting lines
- Counting words
- Counting characters
- Counting bytes
- Combining `wc` with pipes
- Real-world reporting and log analysis
