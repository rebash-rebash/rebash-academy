---
title: Understanding the Git Object Model
description: Deep dive into Git blobs, trees, commits, and tags; SHA-1 hashing, content-addressable storage, and plumbing commands for DevOps debugging.
difficulty: beginner
estimated_time: "40 min"
author: Shaik Basha
category: git
tags:
  - git
  - object-model
  - internals
  - plumbing
prerequisites:
  - Introduction to Git and Version Control
  - Git Installation and Configuration
comments: false
---

# Understanding the Git Object Model

## Overview

Git is not a simple file backup system — it is a **content-addressable object database**. Every commit, directory snapshot, and file version is stored as an immutable object identified by a cryptographic hash. Understanding blobs, trees, commits, and tags explains why Git is fast, why `git add` works the way it does, and how to recover corrupted repositories in production.

This tutorial covers Git's four object types, the `.git/objects` store, refs, and plumbing commands that power advanced debugging.

This is **Tutorial 3** in **Module 1: Foundations** of the REBASH Academy Git series.

## Prerequisites

- [Introduction to Git and Version Control](introduction-to-git-and-version-control.md)
- [Git Installation and Configuration](git-installation-and-configuration.md)
- Comfort reading hex hashes and navigating `.git` directories

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the four Git object types: blob, tree, commit, tag
- [ ] Describe content-addressable storage and SHA-1 hashing
- [ ] Trace how a file path resolves to a blob through trees
- [ ] Use plumbing commands: `hash-object`, `cat-file`, `write-tree`
- [ ] Read and interpret commit object contents
- [ ] Understand loose objects vs packfiles
- [ ] Relate the object model to everyday porcelain commands

## Object Model Diagram

```mermaid
flowchart TB
    COMMIT["Commit Object<br/>author · message · tree · parent"]
    TREE["Tree Object<br/>directory listing"]
    BLOB["Blob Object<br/>file content"]
    TAG["Tag Object<br/>annotated release"]

    COMMIT -->|points to| TREE
    TREE -->|name → blob| BLOB
    TREE -->|name → tree| TREE
    TAG -->|points to| COMMIT
    COMMIT -->|parent| COMMIT```

## Theory

### Content-Addressable Storage

Git names objects by the **SHA-1 hash** of their contents (Git is transitioning to SHA-256 in newer versions). If two files have identical content, they share one blob — deduplication is automatic. Change one byte and you get a completely different hash.

This design makes Git:

- **Immutable** — objects never change; new content creates new objects
- **Verifiable** — hash tampering is detectable
- **Efficient** — unchanged files reference existing blobs

### Blob Objects

A **blob** (binary large object) stores raw file content — no filename, no permissions. The filename lives in the **tree** that references the blob.

```bash
echo "hello git" | git hash-object -w --stdin
# outputs: 8d0e41234f14b0591dd233b0e8a4951398565f9f
```

The `-w` flag writes the object to `.git/objects/`. Objects are stored under `objects/ab/cdef123...` using the first two hex digits as directory name.

### Tree Objects

A **tree** represents a directory. Each entry contains:

| Field | Meaning |
|-------|---------|
| Mode | File type and permissions (e.g., `100644` regular file) |
| Name | Filename or subdirectory name |
| SHA-1 | Hash of blob or subtree |

A commit's tree captures the entire project snapshot at that moment. Subdirectories are nested trees.

### Commit Objects

A **commit** object contains:

- **Tree** — root tree SHA for this snapshot
- **Parent(s)** — zero (initial), one (linear), or two+ (merge)
- **Author / Committer** — name, email, timestamp
- **Message** — commit description

Commits form a **directed acyclic graph (DAG)** — branches are pointers into this graph, not separate histories.

### Tag Objects

**Lightweight tags** are refs pointing to commits — no separate object.

**Annotated tags** are tag objects with tagger info, message, and optional GPG signature — used for releases (`v1.0.0`).

### Refs: Branches and HEAD

**Refs** are pointers to commits:

- `refs/heads/main` — branch tip
- `refs/tags/v1.0` — tag
- `refs/remotes/origin/main` — remote-tracking branch
- `HEAD` — current branch (usually `ref: refs/heads/main`)

Branches move forward with each commit; tags (annotated) typically stay fixed.

### Index (Staging Area)

The **index** (`.git/index`) is a flat list of path → blob mappings for the next commit. `git add` updates the index; `git commit` creates a tree from the index and a commit pointing to it.

### Packfiles and Garbage Collection

Loose objects accumulate over time. `git gc` packs them into `.git/objects/pack/*.pack` for efficiency. `git count-objects -v` reports loose vs packed object counts — useful when diagnosing bloated repositories.

### Plumbing vs Porcelain

| Porcelain (daily use) | Plumbing (internals) |
|-----------------------|----------------------|
| `git commit` | `git commit-tree` |
| `git add` | `git update-index`, `git hash-object` |
| `git log` | `git rev-parse`, `git cat-file` |
| `git checkout` | `git read-tree`, `git update-ref` |

DevOps engineers use plumbing commands when debugging corrupted repos or building custom Git tooling.

## Hands-on Lab

### Step 1 – Create a bare repository for object exploration

**Command:**

```bash
mkdir -p /tmp/git-objects-lab && cd /tmp/git-objects-lab
git init
echo "version=1.0" > app.conf
echo "# README" > README.md
mkdir config && echo "port=8080" > config/server.conf
```

**Explanation:** We will manually trace how these files become Git objects.

### Step 2 – Hash and store blobs manually

**Command:**

```bash
git hash-object -w app.conf
git hash-object -w README.md
git hash-object -w config/server.conf
ls .git/objects/*/*  | head -5
```

**Explanation:** Each file becomes a blob. Note the object paths under `.git/objects/`.

### Step 3 – Inspect object types with cat-file

**Command:**

```bash
BLOB=$(git hash-object app.conf)
git cat-file -t "$BLOB"
git cat-file -p "$BLOB"
git cat-file -s "$BLOB"
```

**Expected output:**

```text
blob
version=1.0
9
```

**Explanation:** `-t` type, `-p` pretty-print content, `-s` size in bytes.

### Step 4 – Stage, commit, and inspect the commit object

**Command:**

```bash
git add .
git commit -m "Initial commit with config files"
COMMIT=$(git rev-parse HEAD)
git cat-file -t "$COMMIT"
git cat-file -p "$COMMIT"
```

**Explanation:** The commit object lists tree SHA, parent (none for initial), author, and message.

### Step 5 – Walk from commit to files

**Command:**

```bash
TREE=$(git cat-file -p HEAD | head -1 | awk '{print $2}')
git cat-file -p "$TREE"
git ls-tree -r HEAD
```

**Explanation:** `git ls-tree -r HEAD` recursively lists every blob in the commit — the same data `git archive` would export.

### Step 6 – Compare duplicate content deduplication

**Command:**

```bash
echo "duplicate" > file1.txt
echo "duplicate" > file2.txt
git add file1.txt file2.txt
BLOB1=$(git hash-object file1.txt)
BLOB2=$(git hash-object file2.txt)
echo "BLOB1=$BLOB1 BLOB2=$BLOB2"
test "$BLOB1" = "$BLOB2" && echo "Same blob — deduplicated"
```

**Explanation:** Identical content produces identical hashes — Git stores one blob for both files.

### Step 7 – Clean up

**Command:**

```bash
cd /tmp && rm -rf git-objects-lab
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `git hash-object -w file` | Write file as blob, print SHA | `git hash-object -w README.md` |
| `git cat-file -t SHA` | Show object type | `git cat-file -t HEAD` |
| `git cat-file -p SHA` | Pretty-print object | `git cat-file -p HEAD` |
| `git ls-tree SHA` | List tree contents | `git ls-tree -r HEAD` |
| `git rev-parse HEAD` | Resolve ref to SHA | `git rev-parse main` |
| `git count-objects -v` | Object store statistics | `git count-objects -vH` |
| `git verify-pack -v` | Inspect packfile contents | `git verify-pack -v .git/objects/pack/*.idx` |

### Object inspection script

```bash
#!/usr/bin/env bash
# git-object-inspect.sh — summarize repository object store
set -euo pipefail
cd "${1:-.}"
echo "=== Object counts ==="
git count-objects -vH
echo ""
echo "=== HEAD commit ==="
git cat-file -p HEAD
echo ""
echo "=== Files at HEAD ==="
git ls-tree -r HEAD --name-only
```

## Common Mistakes

!!! warning "Assuming Git stores diffs"
    Git stores **snapshots** (trees + blobs), not diffs. Diffs are computed at display time. This is why storing large binaries bloats repos.

!!! warning "Editing files in .git/objects"
    Objects are immutable and zlib-compressed. Never manually edit — corruption breaks hash integrity.

!!! warning "Confusing author and committer"
    They differ during cherry-pick, rebase, and patch application. Audit logs may track both separately.

!!! warning "Ignoring packfile corruption"
    If `git fsck` reports bad objects, restore from remote clone or backup — do not delete random pack files.

## Best Practices

!!! tip "Run git fsck periodically on critical mirrors"
    Bare mirrors and CI caches should pass `git fsck --full` in maintenance jobs.

!!! tip "Use git cat-file when log is confusing"
    When history looks wrong, inspect raw commit objects to verify parents and tree SHAs.

!!! tip "Understand blobs before blaming LFS"
    Large files inflate blob count. Know what's in `.git/objects` before reaching for Git LFS.

!!! tip "Pin Git version for SHA-256 transition awareness"
    New repos may use `objectFormat=sha256`. Mixed teams should align Git versions during transition.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `fatal: bad object` | Corrupt or missing object | `git fsck`; re-clone from remote |
| Repository huge | Many large blobs in history | `git rev-list --objects --all`; consider BFG or filter-repo |
| `git cat-file` empty for tag | Lightweight tag (ref only) | Use `git show` or check if annotated |
| Slow clone | No packfiles; millions of loose objects | Run `git gc` on server mirror |
| Wrong file content at commit | Tree points to different blob than expected | `git ls-tree -r COMMIT -- path/to/file` |

## Summary

- Git stores four object types: **blob** (content), **tree** (directory), **commit** (snapshot + metadata), **tag** (annotated release)
- Objects are **content-addressed** by SHA-1 hash — identical content shares storage
- **Commits** point to trees; trees point to blobs and subtrees; commits link to parents forming a DAG
- **Refs** (branches, tags, HEAD) are movable pointers into the object graph
- **Plumbing commands** expose internals for debugging; **porcelain** commands build on them

## Interview Questions

1. What are the four types of Git objects?
2. How does content-addressable storage work in Git?
3. What is the difference between a blob and a tree?
4. What fields does a commit object contain?
5. Explain the difference between lightweight and annotated tags.
6. What is the staging area (index), and how does it relate to trees?
7. Why does Git store snapshots instead of diffs?
8. What are packfiles, and when does Git create them?
9. What is the difference between plumbing and porcelain commands?
10. How would you inspect the raw contents of a commit?

??? tip "Sample Answers (Questions 1 and 7)"

    **Q1 — Four object types:** Blobs store file content. Trees store directory listings mapping names to blob or tree SHAs. Commits store metadata (author, message, timestamp), a pointer to a root tree, and parent commit(s). Annotated tags store a pointer to a commit plus tagger info and optional signature.

    **Q7 — Snapshots vs diffs:** Storing full snapshots makes checkout, branching, and merge algorithms simpler and faster — Git reads one tree per commit. Diffs are computed on demand for display. Snapshot storage also enables efficient deduplication via shared blobs across commits.

## Related Tutorials

- [Git Installation and Configuration](git-installation-and-configuration.md) *(previous)*
- [Creating and Cloning Repositories](creating-and-cloning-repositories.md) *(next — Module 2)*
- [Git – Category Overview](index.md)
- [Viewing History and Diffs](viewing-history-and-diffs.md)
- [Cherry-pick and Reflog](cherry-pick-and-reflog.md)

## References

- [Pro Git Book – Git Internals](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain)
- [Git cat-file documentation](https://git-scm.com/docs/git-cat-file)
- [Git hash-object documentation](https://git-scm.com/docs/git-hash-object)
- [Git fsck documentation](https://git-scm.com/docs/git-fsck)
- [GitHub – Git object library](https://github.com/git/git/blob/master/Documentation/user-manual.txt)
- [REBASH Academy – Git Overview](index.md)
