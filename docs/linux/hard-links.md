---
title: "Hard Links in Linux — Understanding Inodes and File Linking"
description: "Create and manage hard links — inodes, link counts, find -samefile, and how Linux deletes files when the last hard link is removed."
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 4 · File Management and Permissions"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - hard-links
  - inodes
  - filesystem
  - rebash-linux-mastery
comments: false
status: ready
---

# Hard Links in Linux — Understanding Inodes and File Linking

> A **Hard Link** is another name for the same file in the filesystem. Unlike a symbolic (soft) link, a hard link points directly to the file's inode, not its pathname. This means all hard links are equal references to the same underlying data. Understanding hard links is essential for Linux administrators, DevOps engineers, and anyone working with Linux filesystems.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 4: File Management and Permissions → Lesson 2</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 40 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** File Management and Permissions</div>

<div markdown>**Lesson:** 2 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand what a hard link is
- Learn how Linux stores files
- Understand inodes
- Create hard links
- Compare hard links and symbolic links
- View inode numbers
- Identify hard links
- Use hard links in production

---

# Prerequisites

Before starting this lesson, complete:

- Module 1 – Linux Fundamentals
- Module 2 – Command Line Essentials
- Module 3 – Text Processing
- Module 4 Lesson 1 – File Types

---

# Why Learn Hard Links?

Imagine this situation:

You have a file:

```text
report.txt
```

Another application needs the same file with a different name:

```text
backup.txt
```

Should you:

- Copy the file?
- Create a symbolic link?
- Create a hard link?

Understanding hard links helps you save disk space and understand how Linux filesystems work internally.

---

# How Linux Stores Files

Linux separates:

```text
Filename
      │
      ▼
 Inode
      │
      ▼
 Actual Data Blocks
```

The filename is **not** the file itself.

Instead:

- Filename → points to an inode.
- Inode → points to the actual file data.

---

# What is an Inode?

An **inode** stores metadata about a file.

It contains:

- File owner
- Group
- Permissions
- File size
- Timestamps
- Link count
- Data block locations

It does **not** store the filename.

---

# Viewing Inodes

Create a file.

```bash
echo "Linux Mastery" > notes.txt
```

Display inode.

```bash
ls -li notes.txt
```

Example:

```text
524288 -rw-r--r-- 1 basha users 15 Jan 10 notes.txt
```

Here:

```text
524288
```

is the inode number.

---

# Creating a Hard Link

Syntax:

```bash
ln source_file hardlink_name
```

Example:

```bash
ln notes.txt backup.txt
```

Display:

```bash
ls -li
```

Output:

```text
524288 -rw-r--r-- 2 basha users 15 Jan 10 notes.txt

524288 -rw-r--r-- 2 basha users 15 Jan 10 backup.txt
```

Notice:

- Same inode
- Same file size
- Link count is now **2**

---

# Understanding Link Count

Example:

```text
524288 notes.txt

524288 backup.txt
```

Both names reference the **same inode**.

The link count indicates how many directory entries point to that inode.

---

# Modifying a Hard Link

Edit:

```bash
echo "Docker" >> backup.txt
```

Read:

```bash
cat notes.txt
```

Output:

```text
Linux Mastery

Docker
```

Both filenames display the same content because they reference the same data.

---

# Deleting One Hard Link

Remove:

```bash
rm backup.txt
```

Check:

```bash
cat notes.txt
```

The file still exists.

Only one directory entry was removed.

---

# When is Data Deleted?

A file's data is removed only when:

- The link count becomes **0**
- No process is keeping the file open

---

# Visual Representation

Before:

```text
notes.txt
      │
      ▼
    Inode
      │
      ▼
   File Data
```

After creating a hard link:

```text
notes.txt ─┐
           │
backup.txt─┘
      │
      ▼
    Inode
      │
      ▼
   File Data
```

---

# Hard Link vs Copy

Copy:

```bash
cp notes.txt copy.txt
```

Results:

- Different inode
- Separate file
- Changes are independent

Hard link:

```bash
ln notes.txt backup.txt
```

Results:

- Same inode
- Same data
- Changes appear in both names

---

# Verify Using ls

```bash
ls -li
```

Example:

```text
524288 notes.txt

524288 backup.txt

524310 copy.txt
```

---

# Find Files with Multiple Hard Links

```bash
find . -samefile notes.txt
```

or

```bash
find . -inum 524288
```

---

# Limitations of Hard Links

Hard links:

!!! failure "Limitation"

    Cannot span different filesystems.

!!! failure "Limitation"

    Cannot normally link directories.

These restrictions help prevent filesystem corruption and directory loops.

---

# Common Commands

Create:

```bash
ln file.txt file-hard
```

Display inode.

```bash
ls -li
```

Find same inode.

```bash
find . -samefile file.txt
```

Count links.

```bash
stat file.txt
```

---

# View Link Count

```bash
stat notes.txt
```

Example:

```text
Links: 2
```

---

# Hard Links vs Symbolic Links

| Hard Link | Symbolic Link |
|------------|---------------|
| Same inode | Different inode |
| Points to file data | Points to pathname |
| Survives original filename deletion | Breaks if target is deleted |
| Cannot span filesystems | Can span filesystems |
| Usually cannot link directories | Can link directories |

---

# Real Production Examples

Package managers use hard links to reduce duplicate storage.

Backup software uses hard links for incremental backups.

Log rotation tools may use hard links internally.

Administrators use hard links to avoid duplicate copies of large files.

---

# Production Perspective

Hard links are useful for:

- Incremental backups
- Saving disk space
- File deduplication
- Package management
- Filesystem understanding
- Advanced troubleshooting

Although many administrators use symbolic links more often, understanding hard links explains how Linux filesystems manage files internally.

---

# Hands-on Lab

## Task 1

Create a file.

```bash
echo "Linux" > linux.txt
```

---

## Task 2

Display inode.

```bash
ls -li linux.txt
```

---

## Task 3

Create a hard link.

```bash
ln linux.txt backup.txt
```

---

## Task 4

Display inode numbers.

```bash
ls -li
```

Verify both files share the same inode.

---

## Task 5

Append data.

```bash
echo "Docker" >> backup.txt
```

---

## Task 6

Read the original file.

```bash
cat linux.txt
```

Notice the appended content.

---

## Task 7

Delete the hard link.

```bash
rm backup.txt
```

Verify the original file still exists.

---

## Task 8

Display metadata.

```bash
stat linux.txt
```

Observe the link count.

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `ln` | Create hard link | Backups |
| `ls -li` | Display inode numbers | Filesystem analysis |
| `stat` | Show metadata | Troubleshooting |
| `find -samefile` | Find hard links | File audits |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A storage administrator notices that deleting a filename does not free disk space.

Investigation:

1. Check the inode.
2. Verify the link count.
3. Find other hard links.
4. Remove unnecessary links.

Commands:

```bash
ls -li report.txt

stat report.txt

find /data -samefile report.txt
```

The investigation reveals that multiple hard links still reference the same inode, so the data remains allocated.

---

# Best Practices

- Use hard links only within the same filesystem.
- Avoid creating hard links for directories.
- Use `ls -li` and `stat` to understand link counts.
- Use hard links for efficient backup strategies.
- Prefer symbolic links when linking across filesystems.

---

# Common Mistakes

❌ Assuming a hard link is a shortcut.

✅ It is **another directory entry for the same file**, not a reference like a symbolic link.

---

❌ Expecting hard links to work across different filesystems.

✅ They cannot.

---

❌ Believing deleting the original filename deletes the file.

✅ The file remains until the last hard link is removed and no process has it open.

---

# Interview Questions
## Beginner

1. What is a hard link?
2. What is an inode?
3. Which command creates a hard link?
4. How do you view inode numbers?

---

## Intermediate

1. Why do hard links share the same inode?
2. Why can't hard links usually be created for directories?
3. What happens when one hard link is deleted?
4. How do you find all hard links to a file?

---

## Architect Level

1. Why are hard links useful for incremental backups?
2. Explain how Linux deletes a file internally.
3. When would you choose a hard link instead of a symbolic link?

---

# Summary

In this lesson, you learned:

- What hard links are
- How Linux stores files using inodes
- Creating and managing hard links
- Viewing inode numbers
- Understanding link counts
- Differences between hard and symbolic links
- Production use cases

Hard links provide multiple names for the same file without duplicating data. Understanding them is essential for mastering Linux filesystems and advanced file management.

---

## Key Takeaways

- A hard link is another name for the same file.
- Hard-linked files share the same inode.
- Deleting one hard link does not delete the underlying data.
- Data is removed only after the last hard link is deleted and no process is using the file.
- Hard links cannot normally span filesystems or link directories.

---

## What's Next?

**[Symbolic (Soft) Links in Linux — Creating Flexible File References](soft-links.md)**

In the next lesson, you'll learn:

- Creating symbolic links
- Relative vs absolute links
- Broken symbolic links
- Symlink management
- Real-world DevOps deployment strategies
