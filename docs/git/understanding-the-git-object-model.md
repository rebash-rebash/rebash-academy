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


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-01 && cd ~/rebash-git/module-01
```

**Focus:** practise Git skills for: Understanding the Git Object Model

### Step 1 – Init repository

```bash
git init -b main
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
echo '# lab' > README.md
git add README.md
git commit -m 'Initial commit'
git log --oneline
```

### Step 2 – Inspect objects

```bash
echo 'payload' > blob.txt
git add blob.txt
git commit -m 'blob'
git rev-parse HEAD
git cat-file -t HEAD
git cat-file -p HEAD | tee commit-obj.txt
git rev-list --objects --all | head
```

### Final step – Cleanup note

```bash
# Safe local repo under the lab directory; delete the folder when finished
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


1. Explain **Understanding the Git Object Model** as you would in a senior engineer interview.
2. You rebased a shared branch and teammates are blocked — what now?
3. How do you recover a commit that seems lost?
4. What Git security controls belong in a production org?
5. How should Git history look for Infrastructure as Code (IaC) repos?

!!! tip "Sample answer — question 2"
    Stop force-pushing; communicate; use `reflog` to recover; prefer revert on shared main. Reset/rebase only on private branches.

!!! tip "Sample answer — question 4"
    Signed commits, protected branches, secret scanning, least-privilege tokens, and signed tags for releases.



## Related Tutorials



- [Course overview](index.md)
- [Git Installation and Configuration](git-installation-and-configuration.md)



## References



- [Pro Git — Git Internals](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)
