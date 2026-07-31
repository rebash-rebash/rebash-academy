---
title: "Understanding the Git Object Model"
description: "Master Git blobs, trees, commits, and tags — content-addressed storage, hashes, and how commits form history for DevOps debugging."
difficulty: beginner
estimated_time: "40–55 min"
technology: git
category: git
module: "Module 1 · Version Control Fundamentals"
career_paths:
  - beginner
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - git
  - git-internals
prerequisites:
  - git/introduction-to-git-and-version-control
next:
  - git/git-installation-and-configuration
related:
  - git/cherry-pick-and-reflog
  - git/git-troubleshooting
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - git
  - objects
  - internals
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Understanding the Git Object Model

## Overview

Explain blobs, trees, commits, and tags, and use `git cat-file` / `rev-parse` to inspect how history is stored — so reset, rebase, and recovery later make sense.

Git is a **content-addressed** object database. Commands move pointers; objects are rarely rewritten in place. That mental model unlocks reflog recovery and “detached HEAD” incidents.

Complete [Introduction](introduction-to-git-and-version-control.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 1 · Version Control Fundamentals** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Introduction to Git and Version Control](introduction-to-git-and-version-control.md)
- Git installed (Module 2 can be done in parallel if needed)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Name the four object types  
- [ ] Relate commits → trees → blobs  
- [ ] Explain content-addressed SHA hashes  
- [ ] Inspect objects with plumbing commands  
- [ ] Connect branches to commit pointers

## Architecture

This topic’s control points and relationships are shown below.

![Git object model](../assets/excalidraw/git-object-model.svg)

## Theory

### What

Git stores history as a **content-addressed object database**. The four object types are **blob** (file contents), **tree** (directory listing of names to blobs/trees), **commit** (a tree plus parent commit(s), author, and message), and **tag** (a named pointer, often annotated). Commands mostly move **refs** (branch and tag names); objects themselves are rarely rewritten in place.

### Why

Ops incidents often look like “where did that commit go?” or “why did rebase break my SHA?”. Once you see that commits are immutable objects linked into a directed acyclic graph (DAG), reset, rebase, cherry-pick, and reflog stop feeling magical. Content addressing also gives integrity: change a byte and the object ID changes.

### How it works

Object ID is essentially a hash of type plus content. Identical content yields the same hash, which is why Git deduplicates efficiently. A commit points at one root tree; that tree points at blobs and nested trees. Each commit (except the first) points at one or more **parents**, forming the DAG. Branches and tags are tiny files under `.git/refs` that store a commit ID. **HEAD** names the current branch, or a raw commit when you are in detached HEAD.

| Type | Stores |
|------|--------|
| **blob** | File contents |
| **tree** | Directory entries (name → blob/tree) |
| **commit** | Tree + parent(s) + author/message |
| **tag** | Named pointer (lightweight or annotated) |

Plumbing tools such as `git cat-file` and `git rev-parse` let you inspect these objects directly when debugging.

### Key concepts

- **Immutable objects** — rebase creates *new* commits with new IDs  
- **Refs are cheap** — `git reset` moves a branch pointer; objects linger until garbage collection  
- **Reflog** remembers where HEAD pointed locally, even after “lost” commits  
- **Annotated tags** store their own objects; lightweight tags are just refs  

### Common pitfalls

- Equating a branch name with a permanent identity — only the commit ID is durable  
- Assuming deleted commits vanish immediately — they often remain until `gc`  
- Hand-editing files under `.git/objects`  
- Ignoring detached HEAD when checking out a tag or SHA for inspection

## Hands-on Lab

**Focus:** practise the core workflow for Understanding the Git Object Model

```bash
mkdir -p ~/rebash-git/module-01
cd ~/rebash-git/module-01

git --version
```

### Step 1 – Tiny repo

```bash
cd ~/rebash-git/module-01
rm -rf object-lab && mkdir object-lab && cd object-lab
git init -b main
echo 'hello' > app.txt
git add app.txt
git config user.email "lab@rebash.local"
git config user.name "REBASH Lab"
git commit -m "feat: add app.txt"
```

### Step 2 – Inspect commit and tree

```bash
git rev-parse HEAD
git cat-file -t HEAD
git cat-file -p HEAD
TREE=$(git rev-parse HEAD^{tree})
git cat-file -p "$TREE"
```

### Step 3 – Blob contents

```bash
BLOB=$(git rev-parse HEAD:app.txt)
git cat-file -p "$BLOB"
```

### Step 4 – Show refs

```bash
git show-ref
cat .git/HEAD
```

## Validation

- [ ] Lab commands run under `~/rebash-git/module-01/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Understanding the Git Object Model** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for git as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Equating a branch name with a permanent identity — only the commit ID is durable  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Assuming deleted commits vanish immediately — they often remain until `gc`  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Understanding the Git Object Model changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `cat-file` fails | Wrong ID | Use `git rev-parse` |
| Empty repo | No commit yet | Create initial commit |

## Summary

- Objects are immutable and hashed  
- Branches are pointers; commits are snapshots  
- Plumbing commands reveal the real model

## Interview Questions

1. How does **Understanding the Git Object Model** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Git Installation and Configuration](git-installation-and-configuration.md)

## References

- [Pro Git — Git Internals](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)
