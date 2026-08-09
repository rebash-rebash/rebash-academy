---
title: "Wildcards and Globbing"
description: "Use Bash wildcards and globbing — *, ?, character sets, ranges, and brace expansion — safely for Linux administration and DevOps automation."
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
  - wildcards
  - globbing
  - bash
  - command-line
  - rebash-linux-mastery
comments: false
status: ready
---

# Wildcards and Globbing

> Wildcards and globbing allow you to work with multiple files using simple patterns instead of typing each filename individually. They are essential for Linux administration, shell scripting, DevOps automation, and production operations.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 2: Linux Command Line Essentials → Lesson 7</p>

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

<div markdown>**Lesson:** 7 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand what wildcards are
- Learn how Bash performs globbing
- Use `*`, `?`, and `[]`
- Match files using character ranges
- Use brace expansion
- Combine wildcard patterns
- Use wildcards safely in production

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 Lessons 1–6

---

# Why Learn Wildcards?

Imagine you have thousands of files.

Instead of typing:

```bash
rm app1.log

rm app2.log

rm app3.log

rm app4.log
```

You simply type:

```bash
rm *.log
```

One command.

Thousands of files.

This is the power of wildcards.

---

# What is Globbing?

**Globbing** is the process performed by the Bash shell to expand wildcard patterns into matching filenames.

Example:

You type:

```bash
ls *.txt
```

Bash converts it to:

```text
ls notes.txt report.txt users.txt
```

before executing the command.

Notice:

The **shell** expands the pattern, not the `ls` command.

---

# Common Wildcards

| Wildcard | Meaning |
|-----------|---------|
| `*` | Zero or more characters |
| `?` | Exactly one character |
| `[]` | Match one character from a set |
| `{}` | Brace expansion |
| `[a-z]` | Character range |

---

# The `*` Wildcard

Matches **zero or more characters**.

Example files:

```text
notes.txt

report.txt

linux.txt

config.yaml

backup.log
```

Display all text files:

```bash
ls *.txt
```

Output:

```text
linux.txt

notes.txt

report.txt
```

---

Display all log files.

```bash
ls *.log
```

---

Display every file.

```bash
ls *
```

---

# The `?` Wildcard

Matches **exactly one character**.

Example files:

```text
a.txt

b.txt

ab.txt

abc.txt
```

Command:

```bash
ls ?.txt
```

Matches:

```text
a.txt

b.txt
```

Does NOT match:

```text
ab.txt
```

---

# Character Sets

Use square brackets.

Example:

```text
app1.log

app2.log

app3.log

app4.log
```

Command:

```bash
ls app[12].log
```

Output:

```text
app1.log

app2.log
```

---

# Character Ranges

Example:

```bash
ls file[1-5].txt
```

Matches:

```text
file1.txt

file2.txt

file3.txt

file4.txt

file5.txt
```

---

Alphabet range:

```bash
ls [a-f]*
```

Matches:

```text
apple.txt

config.txt

docker.txt
```

---

# Negation

Exclude characters.

```bash
ls [!0-9]*
```

Matches files **not** starting with numbers.

---

# Brace Expansion

Brace expansion is **not** globbing.

It generates multiple strings.

Example:

```bash
mkdir project{1,2,3}
```

Creates:

```text
project1

project2

project3
```

---

Create files:

```bash
touch server{1..5}.log
```

Creates:

```text
server1.log

server2.log

server3.log

server4.log

server5.log
```

---

Alphabet expansion:

```bash
touch file{A..E}.txt
```

Creates:

```text
fileA.txt

fileB.txt

fileC.txt

fileD.txt

fileE.txt
```

---

# Combining Wildcards

Example:

```bash
ls project*.txt
```

Matches:

```text
project1.txt

project_backup.txt

project-final.txt
```

---

Another example:

```bash
ls server?.log
```

Matches:

```text
server1.log

server2.log

server3.log
```

Does NOT match:

```text
server10.log
```

---

# Hidden Files

Remember:

```bash
*
```

does **not** match hidden files.

Hidden files begin with:

```text
.
```

Display hidden files.

```bash
ls -a
```

Match hidden files.

```bash
ls .*
```

---

# Using Wildcards with Commands

Copy all YAML files.

```bash
cp *.yaml backup/
```

Delete all log files.

```bash
rm *.log
```

Move all shell scripts.

```bash
mv *.sh scripts/
```

Count all text files.

```bash
wc -l *.txt
```

---

# Preview Before Deleting

Never run:

```bash
rm *.log
```

without checking.

Preview first:

```bash
ls *.log
```

Then:

```bash
rm *.log
```

This simple habit prevents accidental deletions.

---

# Wildcards vs Regular Expressions

Many beginners confuse them.

| Wildcards | Regular Expressions |
|------------|--------------------|
| Used by Shell | Used by Programs |
| Expand filenames | Match text patterns |
| `*.txt` | `.*\.txt` |
| Simple | More Powerful |

We'll cover Regular Expressions later in the course.

---

# Real Production Example

Backup Kubernetes YAML files.

```bash
cp *.yaml backup/
```

Delete old logs.

```bash
rm *.old
```

Archive reports.

```bash
tar -czf reports.tar.gz *.csv
```

Move certificates.

```bash
mv *.crt certificates/
```

---

# Production Perspective

DevOps engineers frequently use wildcards.

Examples:

Docker:

```bash
docker cp *.sql database:/
```

Git:

```bash
git add *.yaml
```

Terraform:

```bash
ls *.tf
```

Kubernetes:

```bash
kubectl apply -f *.yaml
```

Automation becomes much easier with wildcard patterns.

---

# Hands-on Lab

## Task 1

Create a practice directory.

```bash
mkdir wildcard-lab

cd wildcard-lab
```

---

## Task 2

Create files.

```bash
touch app.py

touch app.js

touch app.java

touch notes.txt

touch report.txt

touch server1.log

touch server2.log

touch config.yaml
```

---

## Task 3

List text files.

```bash
ls *.txt
```

---

## Task 4

List log files.

```bash
ls *.log
```

---

## Task 5

Match single character.

```bash
ls server?.log
```

---

## Task 6

Create multiple files.

```bash
touch backup{1..5}.sql
```

---

## Task 7

List SQL files.

```bash
ls *.sql
```

---

## Task 8

Create alphabet files.

```bash
touch demo{A..D}.txt
```

---

## Task 9

Display only demo files.

```bash
ls demo*
```

---

# Command Deep Dive

| Pattern | Description | Example |
|-----------|-------------|----------|
| `*` | Any number of characters | `*.txt` |
| `?` | One character | `file?.txt` |
| `[]` | Character set | `file[12].txt` |
| `[a-z]` | Character range | `[a-f]*` |
| `[!a-z]` | Negation | `[!0-9]*` |
| `{}` | Brace expansion | `file{1..5}.txt` |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A server contains:

```text
app1.log

app2.log

app3.log

error.log

backup.tar.gz

config.yaml

config-old.yaml

deployment.yaml
```

Tasks:

1. Display all YAML files.
2. Display only application logs.
3. Delete only backup files.
4. Copy all YAML files to a backup directory.
5. Display files beginning with "config".

Possible solutions:

```bash
ls *.yaml

ls app*.log

rm *.tar.gz

cp *.yaml backup/

ls config*
```

---

# Mini Challenge

Create the following files.

```text
project1.txt

project2.txt

project3.txt

server1.log

server2.log

server3.log

config.yaml

docker-compose.yml

deploy.sh
```

Now perform the following:

- List all `.txt` files.
- List all `.log` files.
- Display only `project1.txt` to `project3.txt`.
- List files beginning with `server`.
- Create `backup1` to `backup5` directories using a single command.
- Copy all YAML files into a new directory named `configs`.

---

# Best Practices

- Preview wildcard matches with `ls` before using destructive commands.
- Use quotes when you want to prevent shell expansion.
- Prefer specific patterns over broad ones.
- Combine wildcards with other commands for automation.
- Test wildcard commands in a lab before running them in production.

---

# Common Mistakes

❌ Running:

✅ Use:

```bash
rm *
```

without checking the current directory.

Always verify first:

```bash
pwd

ls
```

---

❌ Assuming `*` matches hidden files.

✅ It does not.

Use:

```bash
ls -a

ls .*
```

---

❌ Confusing brace expansion with globbing.

✅ Brace expansion creates filenames.

Globbing matches existing filenames.

---

# Interview Questions
## Beginner

1. What is a wildcard?
2. What does `*` match?
3. What does `?` match?
4. What is brace expansion?

---

## Intermediate

1. Explain globbing.
2. Why is brace expansion different from globbing?
3. How do you match files beginning with "config"?
4. How do you match files ending with `.yaml`?

---

## Architect Level

1. How can wildcard misuse cause production incidents?
2. Why should engineers preview wildcard matches before deleting files?
3. How do wildcards simplify DevOps automation?

---

# Summary

In this lesson, you learned:

- Wildcards
- Globbing
- `*`
- `?`
- Character sets
- Character ranges
- Brace expansion
- Production-safe wildcard usage

Wildcards are one of the most powerful features of the Linux shell. Mastering them will help you work faster, write cleaner scripts, and automate repetitive tasks with confidence.

---

## Key Takeaways

- Bash performs wildcard expansion before executing commands.
- `*` matches zero or more characters.
- `?` matches exactly one character.
- `[]` matches characters from a specified set or range.
- Brace expansion generates multiple filenames.
- Always preview wildcard matches before performing destructive operations.

---

## What's Next?

**[Command History](command-history.md)**

In the next lesson, you'll learn:

- Standard Input (stdin)
- Standard Output (stdout)
- Standard Error (stderr)
- `>`
- `>>`
- `<`
- `|`
- `tee`
- Redirecting command output
- Building powerful command pipelines
