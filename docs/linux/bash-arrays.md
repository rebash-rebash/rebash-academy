---
title: "Arrays — Managing Collections of Data in Bash Scripts"
description: "Manage Bash arrays — indexed and associative arrays, iteration, length, add/remove elements, and production automation patterns."
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
  - arrays
  - automation
  - rebash-linux-mastery
comments: false
status: ready
---

# Arrays — Managing Collections of Data in Bash Scripts

> **Arrays** allow Bash scripts to store multiple values under a single variable name. Instead of creating many individual variables, arrays organize related data into indexed collections, making scripts cleaner, easier to maintain, and more scalable. Arrays are commonly used in automation scripts, server management, cloud provisioning, deployment pipelines, and system administration to process lists of servers, files, users, packages, and other collections of data.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 10: Bash Scripting → Lesson 5</p>

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

<div markdown>**Lesson:** 5 of 11</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Bash arrays
- Create indexed arrays
- Access array elements
- Iterate through arrays
- Add and remove elements
- Determine array length
- Use associative arrays
- Apply arrays in production scripts

---

# Prerequisites

Complete:

- Modules 1–9
- Module 10 Lessons 1–4

---

# Why Learn Arrays?

Imagine checking the status of multiple servers.

Without arrays:

```bash
SERVER1="web01"

SERVER2="web02"

SERVER3="db01"
```

Managing many variables becomes difficult.

Using an array:

```bash
SERVERS=("web01" "web02" "db01")
```

The script becomes much cleaner and easier to scale.

---

# What is an Array?

An array stores multiple values inside a single variable.

Example:

```text
SERVERS

↓

[0] web01

[1] web02

[2] db01
```

Each item has an index.

---

# Creating an Array

Syntax:

```bash
ARRAY=(value1 value2 value3)
```

Example:

```bash
COLORS=("Red" "Green" "Blue")
```

---

# Accessing Array Elements

Display the first element.

```bash
echo ${COLORS[0]}
```

Output:

```text
Red
```

Display another element.

```bash
echo ${COLORS[2]}
```

Output:

```text
Blue
```

---

# Display All Elements

```bash
echo ${COLORS[@]}
```

Output:

```text
Red Green Blue
```

---

# Array Indexes

Bash arrays begin at index **0**.

Example:

```text
Index

0 → Red

1 → Green

2 → Blue
```

---

# Array Length

Display the number of elements.

{% raw %}
```bash
echo ${#COLORS[@]}
```
{% endraw %}

Output:

```text
3
```

---

# Length of One Element

{% raw %}
```bash
echo ${#COLORS[0]}
```
{% endraw %}

Output:

```text
3
```

Because:

```text
Red
```

contains three characters.

---

# Add Elements

Append a new value.

```bash
COLORS+=("Yellow")
```

Display:

```bash
echo ${COLORS[@]}
```

---

# Modify Elements

```bash
COLORS[1]="Black"
```

Display:

```bash
echo ${COLORS[@]}
```

---

# Remove Elements

```bash
unset COLORS[2]
```

Display:

```bash
echo ${COLORS[@]}
```

---

# Loop Through an Array

```bash
for COLOR in "${COLORS[@]}"
do
    echo "$COLOR"
done
```

Output:

```text
Red

Black

Yellow
```

---

# Loop Using Indexes

{% raw %}
```bash
for (( i=0; i<${#COLORS[@]}; i++ ))
do
    echo "${COLORS[$i]}"
done
```
{% endraw %}

---

# Reading User Input into an Array

```bash
read -a NAMES
```

Example input:

```text
Alice Bob Charlie
```

Display:

```bash
echo ${NAMES[@]}
```

---

# Associative Arrays

Associative arrays use keys instead of numeric indexes.

Enable:

```bash
declare -A SERVER_IP
```

Assign values.

```bash
SERVER_IP[web01]="192.168.1.10"

SERVER_IP[db01]="192.168.1.20"
```

Retrieve values.

```bash
echo ${SERVER_IP[web01]}
```

Output:

```text
192.168.1.10
```

---

# Display Keys

```bash
echo ${!SERVER_IP[@]}
```

---

# Display Values

```bash
echo ${SERVER_IP[@]}
```

---

# Common Commands

Create array.

```bash
ARRAY=("A" "B" "C")
```

Display all elements.

```bash
echo ${ARRAY[@]}
```

Display one element.

```bash
echo ${ARRAY[0]}
```

Display length.

{% raw %}
```bash
echo ${#ARRAY[@]}
```
{% endraw %}

Remove element.

```bash
unset ARRAY[1]
```

---

# Real Production Examples

Store servers.

```bash
SERVERS=("web01" "web02" "db01")
```

Restart services.

```bash
for SERVER in "${SERVERS[@]}"
do
    echo "Checking $SERVER"
done
```

Package installation.

```bash
PACKAGES=("git" "curl" "vim")

for PACKAGE in "${PACKAGES[@]}"
do
    echo "Installing $PACKAGE"
done
```

---

# Production Perspective

Arrays are widely used in:

- Server automation
- Cloud deployments
- Kubernetes administration
- Backup automation
- Configuration management
- Package installation
- Monitoring scripts
- CI/CD pipelines

Arrays simplify the management of large collections of related data.

---

# Hands-on Lab

## Task 1

Create an array.

```bash
FRUITS=("Apple" "Banana" "Orange")
```

---

## Task 2

Display all elements.

```bash
echo ${FRUITS[@]}
```

---

## Task 3

Display the first element.

```bash
echo ${FRUITS[0]}
```

---

## Task 4

Display the array length.

{% raw %}
```bash
echo ${#FRUITS[@]}
```
{% endraw %}

---

## Task 5

Add an element.

```bash
FRUITS+=("Mango")
```

---

## Task 6

Loop through the array.

```bash
for FRUIT in "${FRUITS[@]}"
do
    echo "$FRUIT"
done
```

---

## Task 7

Create an associative array.

```bash
declare -A USERS

USERS[admin]="Linux"

USERS[guest]="Visitor"
```

---

## Task 8

Display associative array values.

```bash
echo ${USERS[admin]}
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `ARRAY=()` | Create array | Store data |
| `${ARRAY[@]}` | Display all elements | Reporting |
| `${ARRAY[index]}` | Access one element | Configuration |
| `{% raw %}${#ARRAY[@]}{% endraw %}` | Array length | Validation |
| `unset` | Remove element | Cleanup |
| `declare -A` | Create associative array | Key-value configuration |

---

# Common Array Mistakes

| Mistake | Solution |
|----------|----------|
| Starting indexes at 1 | Bash arrays start at 0 |
| Forgetting quotes around `"${ARRAY[@]}"` | Quote array expansion |
| Using associative arrays without `declare -A` | Declare first |
| Confusing array length with string length | Use the correct syntax |
| Treating arrays like strings | Access individual elements properly |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A monitoring script checks multiple servers.

Without arrays:

```bash
ping web01

ping web02

ping db01
```

Improved:

```bash
SERVERS=("web01" "web02" "db01")

for SERVER in "${SERVERS[@]}"
do
    if ping -c1 "$SERVER" >/dev/null
    then
        echo "$SERVER is reachable"
    else
        echo "$SERVER is unreachable"
    fi
done
```

Adding a new server requires changing only one line in the array.

---

# Best Practices

- Use arrays for related collections of data.
- Quote `"${ARRAY[@]}"` when iterating.
- Use descriptive array names.
- Prefer associative arrays for key-value mappings.
- Keep array operations simple and readable.
- Validate array contents before processing.

---

# Common Mistakes

❌ Starting array indexes at 1 instead of 0.

✅ Prefer 0 rather than starting array indexes at 1.

---

❌ Forgetting quotes around array expansion.

✅ Remember to quotes around array expansion.

---

❌ Accessing elements that do not exist.

✅ Avoid this mistake: accessing elements that do not exist.

---

❌ Using multiple variables instead of arrays.

✅ Prefer arrays rather than using multiple variables.

---

❌ Forgetting to declare associative arrays.

✅ Remember to to declare associative arrays.

---

# Interview Questions
## Beginner

1. What is an array?
2. How do you create an array in Bash?
3. How do you access the first element?
4. How do you display all array elements?

---

## Intermediate

1. How do you determine the length of an array?
2. What is the difference between indexed and associative arrays?
3. How do you iterate through an array?
4. How do you remove an array element?

---

## Architect Level

1. How would you use arrays to automate deployments across multiple servers?
2. Why are associative arrays useful in infrastructure automation?
3. How do arrays improve the maintainability of large Bash scripts?

---

# Summary

In this lesson, you learned:

- Indexed arrays
- Associative arrays
- Accessing array elements
- Looping through arrays
- Adding and removing elements
- Array length
- Production scripting techniques

Arrays allow Bash scripts to efficiently manage collections of related data. They reduce repetitive code, improve readability, and simplify automation tasks involving multiple files, users, servers, or configuration values.

---

## Key Takeaways

- Arrays store multiple values in a single variable.
- Bash array indexes start at **0**.
- Use `${ARRAY[@]}` to access all elements.
- Use `{% raw %}${#ARRAY[@]}{% endraw %}` to determine array length.
- Use `declare -A` for associative arrays.
- Arrays make Bash scripts more scalable and easier to maintain.

---

## What's Next?

**[Input — Accepting User Input in Bash Scripts](bash-input.md)**

You'll explore:

- Reading user input
- Command-line arguments
- Interactive prompts
- Input validation
- Password input
- Default values
- Production scripting examples

By the end of the lesson, you'll be able to build interactive Bash scripts that safely accept, validate, and process user input for real-world automation tasks.
