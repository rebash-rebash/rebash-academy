---
title: "fmt Command — Formatting Text in Linux"
description: "Reformat and wrap paragraphs with fmt — custom line widths, preserve prefixes, uniform spacing, and documentation-ready output."
difficulty: intermediate
estimated_time: "20 min"
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
  - fmt
  - text-processing
  - documentation
  - rebash-linux-mastery
comments: false
status: ready
---

# fmt Command — Formatting Text in Linux

> The `fmt` command is used to reformat and wrap text into neatly formatted paragraphs. It is especially useful for preparing documentation, README files, reports, emails, configuration notes, and other text files where readability matters.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 3: Text Processing → Lesson 11</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 20 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Text Processing</div>

<div markdown>**Lesson:** 11 of 18</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `fmt` command
- Format long paragraphs
- Set custom line widths
- Preserve indentation
- Format multiple files
- Use `fmt` in command pipelines
- Prepare professional text documents

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 Lessons 1–10

---

# Why Learn fmt?

Imagine someone sends you a text file like this:

```text
Linux is an open-source operating system that powers servers, cloud infrastructure, supercomputers, embedded systems, and millions of devices around the world. Reading long lines without proper formatting is difficult.
```

It's hard to read.

Use:

```bash
fmt document.txt
```

Output:

```text
Linux is an open-source operating system that powers
servers, cloud infrastructure, supercomputers,
embedded systems, and millions of devices around the
world. Reading long lines without proper formatting is
difficult.
```

---

# What is fmt?

The `fmt` command reformats text by wrapping long lines into paragraphs of a specified width.

Syntax:

```bash
fmt [OPTIONS] FILE
```

---

# Sample File

Create:

```bash
cat > article.txt
```

Paste:

```text
Linux is one of the most powerful operating systems available today. It is widely used in cloud computing, DevOps, cybersecurity, networking, embedded systems, artificial intelligence, and enterprise infrastructure.
```

Press:

```text
Ctrl + D
```

---

# Basic Formatting

```bash
fmt article.txt
```

Output:

```text
Linux is one of the most powerful operating systems
available today. It is widely used in cloud computing,
DevOps, cybersecurity, networking, embedded systems,
artificial intelligence, and enterprise infrastructure.
```

---

# Specify Line Width

Wrap text at 40 characters.

```bash
fmt -w 40 article.txt
```

Output:

```text
Linux is one of the most powerful
operating systems available today.
It is widely used in cloud
computing, DevOps,
cybersecurity, networking,
embedded systems, artificial
intelligence, and enterprise
infrastructure.
```

---

Wrap text at 80 characters.

```bash
fmt -w 80 article.txt
```

80 characters is a common width for documentation and terminal output.

---

# Format Standard Input

```bash
echo "Linux is amazing for cloud computing and automation." | fmt
```

Output:

```text
Linux is amazing for cloud computing and automation.
```

---

# Save Formatted Output

```bash
fmt article.txt > formatted.txt
```

Display:

```bash
cat formatted.txt
```

---

# Format Multiple Files

```bash
fmt file1.txt file2.txt
```

---

# Preserve Prefixes

Suppose a file contains comments.

```text
# Linux is a powerful operating system used in many environments.
# It supports servers, desktops, and cloud platforms.
```

Format while preserving the comment prefix.

```bash
fmt -p "#" comments.txt
```

Output:

```text
# Linux is a powerful operating system used in many
# environments. It supports servers, desktops, and
# cloud platforms.
```

The `-p` option is useful when formatting source code comments or documentation.

---

# Combine with Other Commands

Format command output.

```bash
cat article.txt | fmt
```

Format log summaries.

```bash
grep ERROR application.log | fmt
```

Wrap text before saving.

```bash
cat notes.txt | fmt > report.txt
```

---

# Common fmt Options

| Option | Description |
|----------|-------------|
| `-w` | Set line width |
| `-p` | Preserve line prefix |
| `-u` | Uniform spacing |

---

# Uniform Spacing

Remove extra spaces between words.

Example:

```text
Linux    is     powerful.
```

Command:

```bash
fmt -u file.txt
```

Output:

```text
Linux is powerful.
```

---

# Real Production Examples

Format release notes.

```bash
fmt release-notes.txt
```

Prepare documentation.

```bash
fmt README.md
```

Format email templates.

```bash
fmt email.txt
```

Wrap generated reports.

```bash
cat report.txt | fmt -w 80
```

Format code comments.

```bash
fmt -p "#" script-comments.txt
```

---

# Production Perspective

Although `fmt` is not used as frequently as `grep` or `awk`, it is valuable for:

- Technical documentation
- README files
- Release notes
- Email templates
- Script comments
- Text report formatting

It improves readability and ensures consistent formatting.

---

# Hands-on Lab

## Task 1

Create:

```bash
cat > notes.txt
```

Paste a long paragraph.

---

## Task 2

Format it.

```bash
fmt notes.txt
```

---

## Task 3

Wrap at 50 characters.

```bash
fmt -w 50 notes.txt
```

---

## Task 4

Save formatted output.

```bash
fmt notes.txt > output.txt
```

---

## Task 5

Display output.

```bash
cat output.txt
```

---

## Task 6

Format using standard input.

```bash
echo "Linux powers the cloud." | fmt
```

---

## Task 7

Create a comment file.

```text
# Linux is secure and scalable.
# It powers modern cloud platforms.
```

Format:

```bash
fmt -p "#" comments.txt
```

---

## Task 8

Remove extra spaces.

```bash
fmt -u notes.txt
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `fmt file.txt` | Format text | Documentation |
| `fmt -w 60` | Wrap at 60 columns | Reports |
| `fmt -p "#"` | Preserve comments | Source code |
| `fmt -u` | Normalize spacing | Email templates |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A DevOps engineer generates a deployment report from a script.

    The report contains long, unreadable lines.

Tasks:

1. Wrap the report at 80 columns.
2. Preserve comment lines.
3. Save the formatted report.
4. Verify the output.

Solutions:

```bash
fmt -w 80 deployment-report.txt

fmt -p "#" deployment-report.txt

fmt deployment-report.txt > deployment-report-formatted.txt

cat deployment-report-formatted.txt
```

---

# Mini Challenge

Create:

```text
guide.txt
```

Paste a long paragraph describing Linux.

Perform the following:

- Format the text.
- Wrap at 60 columns.
- Wrap at 100 columns.
- Save the formatted version.
- Create a comment file and preserve comment prefixes.
- Normalize multiple spaces.

---

# Best Practices

- Use 80-character line widths for terminal-friendly documentation.
- Preserve prefixes when formatting comments.
- Keep documentation consistently formatted.
- Review formatted output before publishing.
- Use `fmt` for plain text, not structured formats such as JSON or YAML.

---

# Common Mistakes

❌ Using `fmt` on structured data.

✅ Avoid formatting:

```text
JSON

YAML

XML
```

It may break the structure.

---

❌ Assuming `fmt` preserves every line exactly.

✅ It is designed to **reflow paragraphs**, not preserve manual line breaks.

---

❌ Using `fmt` on Markdown tables.

✅ Tables may become misaligned.

---

# Interview Questions
## Beginner

1. What is the purpose of the `fmt` command?
2. What does the `-w` option do?
3. How do you save formatted output to another file?
4. What is the default behavior of `fmt`?

---

## Intermediate

1. Explain the `-p` option.
2. What does `fmt -u` do?
3. Why shouldn't `fmt` be used on YAML files?
4. When is `fmt` useful in shell scripting?

---

## Architect Level

1. How would you automatically format generated documentation in a CI/CD pipeline?
2. Why is consistent text formatting important in technical documentation?
3. How can `fmt` improve the readability of generated reports?

---

# Summary

In this lesson, you learned:

- Formatting paragraphs
- Wrapping long lines
- Setting custom line widths
- Preserving prefixes
- Formatting standard input
- Preparing documentation

The `fmt` command is a lightweight utility that makes plain-text documents more readable. While it isn't used as frequently as commands like `grep` or `awk`, it is valuable for documentation, reports, and automation workflows that generate human-readable text.

---

## Key Takeaways

- `fmt` wraps long lines into readable paragraphs.
- Use `-w` to specify line width.
- Use `-p` to preserve prefixes such as comment markers.
- Use `-u` to normalize spacing.
- Avoid using `fmt` on structured data formats like JSON, YAML, or Markdown tables.

---

## What's Next?

**[column Command — Displaying Text in Tabular Format](text-processing-column.md)**

In the next lesson, you'll learn:

- Aligning text into columns
- Formatting CSV files
- Creating readable tables
- Working with command output
- Generating professional terminal reports
