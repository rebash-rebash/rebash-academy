---
title: "split Command — Splitting Large Files in Linux"
description: "Split large files by lines or size with split — custom prefixes, numeric suffixes, reassembly, and production backup workflows."
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
  - split
  - text-processing
  - backups
  - rebash-linux-mastery
comments: false
status: ready
---

# split Command — Splitting Large Files in Linux

> The `split` command divides a large file into smaller, more manageable pieces. It is commonly used when handling huge log files, database exports, backups, large CSV files, and files that need to be transferred over networks with size limitations.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 3: Text Processing → Lesson 10</p>

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

<div markdown>**Lesson:** 10 of 18</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `split` command
- Split files by number of lines
- Split files by size
- Create custom file prefixes
- Create numeric suffixes
- Reassemble split files
- Process large production files

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 Lessons 1–9

---

# Why Learn split?

Imagine you have a:

- 20 GB log file
- 10 GB database export
- 5 GB CSV report

You cannot easily:

- Email it
- Upload it
- Analyze it
- Transfer it

Instead:

```bash
split
```

breaks the file into smaller pieces.

---

# What is split?

The `split` command divides a large file into multiple smaller files.

Syntax:

```bash
split [OPTIONS] FILE [PREFIX]
```

---

# Sample File

Create a sample file.

```bash
seq 1 20 > numbers.txt
```

Display:

```bash
cat numbers.txt
```

Output:

```text
1
2
3
...
20
```

---

# Split by Number of Lines

Split every five lines.

```bash
split -l 5 numbers.txt
```

Files created:

```text
xaa

xab

xac

xad
```

View:

```bash
cat xaa
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

# Custom Prefix

Instead of:

```text
xaa

xab
```

Use:

```bash
split -l 5 numbers.txt part-
```

Files:

```text
part-aa

part-ab

part-ac

part-ad
```

---

# Numeric Suffixes

Instead of alphabetic suffixes.

```bash
split -d -l 5 numbers.txt chunk-
```

Files:

```text
chunk-00

chunk-01

chunk-02

chunk-03
```

---

# Specify Suffix Length

```bash
split -d -a 3 -l 5 numbers.txt piece-
```

Files:

```text
piece-000

piece-001

piece-002
```

---

# Split by File Size

Split into 1 KB files.

```bash
split -b 1K logfile.log
```

Split into 10 MB files.

```bash
split -b 10M backup.tar
```

Split into 1 GB files.

```bash
split -b 1G database.sql
```

---

# Human-Readable Sizes

Supported units:

| Unit | Meaning |
|------|----------|
| K | Kilobytes |
| M | Megabytes |
| G | Gigabytes |

Example:

```bash
split -b 100M archive.tar
```

---

# Split by Number of Files

Suppose you want exactly four output files.

```bash
split -n 4 numbers.txt
```

The file is divided into four approximately equal parts.

---

# Display Created Files

```bash
ls part-*
```

---

# Reassemble Files

Suppose:

```text
part-aa

part-ab

part-ac
```

Merge:

```bash
cat part-* > complete.txt
```

Verify:

```bash
diff numbers.txt complete.txt
```

No output means the files are identical.

---

# Verify Integrity

Compare original and reconstructed files.

```bash
cmp numbers.txt complete.txt
```

or

```bash
sha256sum numbers.txt complete.txt
```

Matching checksums confirm the files are identical.

---

# Common split Options

| Option | Description |
|----------|-------------|
| `-l` | Split by lines |
| `-b` | Split by bytes/size |
| `-d` | Numeric suffixes |
| `-a` | Suffix length |
| `-n` | Split into N files |
| `--verbose` | Show created files |

---

# Combining with Other Commands

Compress after splitting.

```bash
split -b 500M backup.tar backup-

gzip backup-*
```

Split compressed logs.

```bash
gzip -dc access.log.gz | split -l 100000 - access-
```

Merge again.

```bash
cat backup-* > backup.tar
```

---

# Real Production Examples

Split a database export.

```bash
split -b 2G database.sql db-
```

Split an application log.

```bash
split -l 500000 application.log log-
```

Split a Kubernetes audit log.

```bash
split -b 500M audit.log audit-
```

Split a CSV report.

```bash
split -l 100000 employees.csv emp-
```

---

# Production Perspective

The `split` command is commonly used for:

- Database backups
- Large log analysis
- Data migration
- Cloud uploads
- Secure file transfer
- Batch processing

Many enterprise environments split files before uploading them to cloud storage or transferring them across networks.

---

# Hands-on Lab

## Task 1

Create a sample file.

```bash
seq 1 100 > numbers.txt
```

---

## Task 2

Split into 20-line files.

```bash
split -l 20 numbers.txt
```

---

## Task 3

Use a custom prefix.

```bash
split -l 20 numbers.txt batch-
```

---

## Task 4

Use numeric suffixes.

```bash
split -d -l 20 numbers.txt part-
```

---

## Task 5

Split by size.

```bash
split -b 1K numbers.txt size-
```

---

## Task 6

Merge files.

```bash
cat part-* > merged.txt
```

---

## Task 7

Verify.

```bash
diff numbers.txt merged.txt
```

---

## Task 8

Display generated files.

```bash
ls part-*
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `split -l 1000` | Split by lines | CSV reports |
| `split -b 100M` | Split by size | Log archives |
| `split -d` | Numeric suffixes | Automation |
| `split -a 3` | Three-digit suffix | Large datasets |
| `split -n 5` | Equal parts | Parallel processing |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A DevOps engineer needs to upload a **12 GB** backup to cloud storage, but the storage service only accepts files up to **2 GB**.

Tasks:

1. Split the backup into 2 GB chunks.
2. Verify the generated files.
3. Reassemble the backup after download.
4. Confirm that the reconstructed file matches the original.

Solutions:

```bash
split -b 2G backup.tar backup-

ls backup-*

cat backup-* > backup.tar

sha256sum backup.tar
```

---

# Mini Challenge

Create:

```bash
seq 1 500 > records.txt
```

Perform the following:

- Split into files containing 100 lines each.
- Create numeric suffixes.
- Use the prefix `records-`.
- Merge all files.
- Verify the merged file.
- Count the number of generated files.

---

# Best Practices

- Use meaningful file prefixes.
- Verify reconstructed files using `sha256sum` or `cmp`.
- Split large backups before transferring them over the network.
- Prefer numeric suffixes (`-d`) in automation scripts.
- Remove temporary split files after successful verification.

---

# Performance Tip

For very large files:

```bash
split -b 1G huge-backup.tar backup-
```

Choose a chunk size appropriate for your storage or network limitations.

When transferring files over unreliable networks, smaller chunks are often easier to retry than a single massive file.

---

# Common Mistakes

❌ Forgetting to verify the reconstructed file.

✅ Always compare:

```bash
sha256sum original.file merged.file
```

---

❌ Using alphabetic suffixes when scripts expect numeric ordering.

✅ Prefer:

```bash
split -d
```

---

❌ Choosing chunk sizes that exceed upload limits.

✅ Verify platform restrictions before splitting.

---

# Interview Questions
## Beginner

1. What is the purpose of the `split` command?
2. How do you split a file every 100 lines?
3. How do you split a file by size?
4. What does `-d` do?

---

## Intermediate

1. Explain `split -n`.
2. How do you reassemble split files?
3. Why should you verify reconstructed files?
4. What is the purpose of `-a`?

---

## Architect Level

1. How would you split and transfer a 100 GB database backup?
2. Why is `split` useful in cloud migrations?
3. How would you automate backup splitting, transfer, and verification in a shell script?

---

# Summary

In this lesson, you learned:

- Splitting files by lines
- Splitting files by size
- Creating custom prefixes
- Using numeric suffixes
- Reassembling files
- Verifying file integrity
- Production backup workflows

The `split` command is an essential tool for handling large files in Linux. It simplifies storage, transfer, and processing while making large datasets easier to manage.

---

## Key Takeaways

- `split` divides large files into smaller parts.
- Use `-l` to split by lines.
- Use `-b` to split by size.
- Use `-d` for numeric suffixes.
- Reassemble files using `cat`.
- Always verify reconstructed files using `diff`, `cmp`, or `sha256sum`.

---

## What's Next?

**[fmt Command — Formatting Text in Linux](text-processing-fmt.md)**

In the next lesson, you'll learn:

- Wrapping long lines
- Formatting paragraphs
- Adjusting line width
- Preparing reports and documentation
- Improving text readability
