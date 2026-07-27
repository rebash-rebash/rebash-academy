---
title: Merging and Merge Conflicts
description: Merge branches with fast-forward and three-way merges, resolve conflicts, use merge tools, and understand merge strategies for team workflows.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
category: git
tags:
  - git
  - merge
  - conflicts
  - collaboration
prerequisites:
  - Branching Fundamentals
  - Viewing History and Diffs
comments: false
---

# Merging and Merge Conflicts

## Overview

Merging integrates work from one branch into another — the moment feature branches meet main and CI validates the combined result. Merge conflicts happen when two branches edit the same lines; resolving them correctly is a core DevOps skill for IaC repos where multiple engineers touch shared modules.

This tutorial covers fast-forward merges, three-way merges, conflict markers, resolution workflow, and merge strategies.

This is **Tutorial 8** in **Module 3: Branching** of the REBASH Academy Git series.

## Prerequisites

- [Branching Fundamentals](branching-fundamentals.md)
- [Viewing History and Diffs](viewing-history-and-diffs.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Perform fast-forward and three-way merges
- [ ] Identify and interpret conflict markers
- [ ] Resolve conflicts manually and with merge tools
- [ ] Abort merges safely with `git merge --abort`
- [ ] Choose merge vs squash merge for pull requests
- [ ] Use `git log --merges` to audit merge history
- [ ] Prevent unnecessary conflicts with communication and small PRs

## Merge Types Diagram

```mermaid
flowchart TB
    subgraph FF["Fast-Forward Merge"]
        M1[main] --> C1 --> C2
        F1[feature] --> C2
    end

    subgraph TW["Three-Way Merge"]
        M2[main] --> A --> B
        F2[feature] --> A --> C
        B --> Merged[Merge commit M]
        C --> Merged
    end```

## Theory

### Fast-Forward Merge

When main has not diverged since the feature branch was created, Git moves the main pointer forward — no merge commit:

```bash
git switch main
git merge feature/quick-fix
```

History remains linear. `git log --oneline` shows no merge commit.

Use `--no-ff` to force a merge commit even when fast-forward is possible — preserves branch context in history:

```bash
git merge --no-ff feature/quick-fix -m "Merge feature/quick-fix"
```

### Three-Way Merge

When both branches have new commits since divergence, Git creates a **merge commit** with two parents:

```bash
git merge feature/complex-change
```

Git finds the **merge base** (common ancestor) and combines changes from both sides.

### Merge Conflicts

Conflicts occur when:

- Same lines changed differently on both branches
- One branch deleted a file the other modified
- Binary file conflicts (Git cannot merge automatically)

Conflict markers in files:

```text
<<<<<<< HEAD
replicas: 3
=======
replicas: 5
>>>>>>> feature/scale-up
```

`HEAD` is current branch (usually main); the other side is incoming branch.

### Resolution Workflow

1. Run merge — Git pauses on conflicts
2. `git status` — lists unmerged paths
3. Edit files — remove markers, keep correct content
4. `git add` resolved files
5. `git commit` — completes merge (or merge continues if more files)

Abort if needed:

```bash
git merge --abort
```

### Merge Tools

```bash
git mergetool
git config --global merge.tool vimdiff
```

VS Code, meld, and kdiff3 provide visual three-pane views. Configure once globally.

### Squash Merge

Platforms offer squash merge on PR — all feature commits become one commit on main:

```bash
git merge --squash feature/big-change
git commit -m "feat: combined feature work"
```

Cleaner main history; loses individual commit granularity on main.

### Merge Strategies

| Strategy | Behavior |
|----------|----------|
| `recursive` (default) | Three-way merge for two branches |
| `ours` | Keep our version entirely |
| `theirs` | Prefer their version (rare, dangerous) |
| `octopus` | Merge multiple branches |

```bash
git merge -X ours feature/config-tweak
```

`-X` passes options to strategy — `ours`/`theirs` for conflict hunks only, not whole files.

### Merging in DevOps Context

- **Terraform modules** — conflicts in shared variables need human judgment
- **K8s manifests** — YAML conflicts often duplicate keys
- **Lock files** — regenerate after merge rather than manual edit

## Hands-on Lab

### Step 1 – Create divergent branches

**Command:**

```bash
mkdir -p /tmp/git-merge-lab && cd /tmp/git-merge-lab
git init -b main
echo "replicas: 2" > deploy.yaml
echo "team: platform" > metadata.yaml
git add . && git commit -m "feat: initial config"
git switch -c feature/scale
echo "replicas: 5" > deploy.yaml
git add deploy.yaml && git commit -m "feat: scale to 5 replicas"
git switch main
echo "team: sre" > metadata.yaml
git add metadata.yaml && git commit -m "chore: update team metadata"
```

### Step 2 – Merge without conflict

**Command:**

```bash
git merge feature/scale --no-edit
cat deploy.yaml metadata.yaml
git log --oneline --graph
```

**Explanation:** Different files changed — clean three-way merge.

### Step 3 – Create intentional conflict

**Command:**

```bash
git switch -c feature/conflict main~1 2>/dev/null || git reset --hard HEAD~1
git switch main
git switch -c feature/conflict
echo "replicas: 10" > deploy.yaml && git add . && git commit -m "feat: scale to 10"
git switch main
echo "replicas: 1" > deploy.yaml && git add . && git commit -m "fix: scale down to 1"
git merge feature/conflict || true
git status
```

### Step 4 – Resolve conflict

**Command:**

```bash
cat deploy.yaml
# Edit to resolved content:
echo "replicas: 3" > deploy.yaml
git add deploy.yaml
git commit -m "merge: resolve replica count — compromise at 3"
git log --oneline --graph -5
```

### Step 5 – Practice abort

**Command:**

```bash
git switch -c test-abort HEAD~1
echo "conflict again" >> deploy.yaml && git commit -am "wip"
git switch main
echo "main change" >> deploy.yaml && git commit -am "main wip"
git merge test-abort || true
git merge --abort
git status
```

### Step 6 – Clean up

**Command:**

```bash
cd /tmp && rm -rf git-merge-lab
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `git merge branch` | Merge branch into current | `git merge feature/x` |
| `git merge --no-ff` | Force merge commit | `git merge --no-ff feature/x` |
| `git merge --abort` | Cancel in-progress merge | `git merge --abort` |
| `git merge --squash` | Squash all commits | `git merge --squash feature/x` |
| `git mergetool` | Launch merge tool | `git mergetool` |
| `git log --merges` | Show merge commits only | `git log --merges --oneline` |
| `git diff --name-only --diff-filter=U` | List unmerged files | During conflict resolution |

### Conflict resolution helper

```bash
#!/usr/bin/env bash
# list-conflicts.sh — show files needing merge resolution
set -euo pipefail
git diff --name-only --diff-filter=U
echo "---"
git status -sb
```

## Common Mistakes

!!! warning "Leaving conflict markers in files"
    `<<<<<<<` markers committed to main break YAML/Terraform parsers and deploy pipelines. Always grep for markers before commit.

!!! warning "Accepting ours/theirs blindly"
    `-X ours` without reading loses teammate's critical fixes. Review every hunk.

!!! warning "Merging without pulling latest main first"
    Update main before merging feature into it — reduces surprise conflicts.

!!! warning "Manual merge of lock files"
    Regenerate `package-lock.json`, `Gemfile.lock`, `.terraform.lock.hcl` after resolving source conflicts.

## Best Practices

!!! tip "Pull main into feature branch before PR"
    `git switch feature/x && git merge main` — resolve conflicts on feature branch, not at merge time on platform.

!!! tip "Keep PRs small"
    Small changes = fewer conflicts and faster review.

!!! tip "Communicate on shared files"
    Platform team owns `deploy/base/` — announce changes in Slack before editing.

!!! tip "Use protected branch merge queues"
    GitHub merge queue serializes merges to main — prevents semantic conflicts from parallel merges.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `CONFLICT (content)` | Same lines edited | Manual resolve; git add; commit |
| Merge stuck | Unresolved files | `git status`; resolve all; or `--abort` |
| Accidental merge commit | Unwanted merge | `git reset --hard ORIG_HEAD` if not pushed |
| Binary conflict | Git cannot merge binary | Choose one version; replace file |
| Recursive merge failed | Too complex history | Rebase feature onto main first |
| Wrong merge parent | Merged wrong branch | Revert merge commit |

## Summary

- **Fast-forward** merges advance pointer linearly; **three-way** merges create a merge commit with two parents
- **Conflicts** require manual resolution — remove markers, stage, commit
- **git merge --abort** safely cancels failed merges
- **Squash merge** collapses feature commits; **--no-ff** preserves branch topology
- Small PRs, frequent integration, and lock file regeneration prevent merge pain

## Interview Questions

1. What is the difference between fast-forward and three-way merge?
2. What do conflict markers mean in a merged file?
3. How do you abort a merge in progress?
4. When would you use `git merge --no-ff`?
5. What is the difference between merge and squash merge?
6. What is a merge base?
7. How do you list files with unresolved conflicts?
8. What does `-X ours` do during merge?
9. Why should lock files be regenerated after merge conflicts?
10. How do merge queues help on busy main branches?

??? tip "Sample Answers (Questions 1 and 5)"

    **Q1 — FF vs three-way:** Fast-forward occurs when the target branch tip is a direct ancestor of the source branch — Git moves the pointer forward with no merge commit. Three-way merge occurs when branches diverged — Git uses the common ancestor plus both tips to compute a combined result, creating a merge commit with two parents.

    **Q5 — Merge vs squash:** Regular merge preserves all individual commits from the feature branch and adds a merge commit (unless FF). Squash merge applies all feature changes as staged diff against main and requires one new commit — feature commits don't appear on main history, simplifying log at cost of granularity.

## Related Tutorials

- [Branching Fundamentals](branching-fundamentals.md) *(previous)*
- [Rebasing and Interactive Rebase](rebasing-and-interactive-rebase.md) *(next)*
- [Pull Requests and Code Review](pull-requests-and-code-review.md)
- [Advanced Git Workflows](advanced-git-workflows.md)
- [Git – Category Overview](index.md)

## References

- [Pro Git Book – Basic Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
- [git merge documentation](https://git-scm.com/docs/git-merge)
- [GitHub – Resolving merge conflicts](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts)
- [REBASH Academy – Git Overview](index.md)
