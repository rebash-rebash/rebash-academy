---
title: Branching Fundamentals
description: Create, switch, list, and delete branches; understand branch pointers, detached HEAD, and branching strategies for DevOps teams.
difficulty: beginner
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: git
tags:
  - git
  - branching
  - checkout
  - switch
prerequisites:
  - Viewing History and Diffs
  - Basic Git Workflow — Add, Commit, Push
comments: false
---

# Branching Fundamentals

## Overview

Branches are Git's killer feature — lightweight movable pointers that let teams work in parallel without stepping on each other. Feature branches for application code, environment branches for Terraform, hotfix branches for production incidents — all use the same mechanics. This tutorial teaches branch creation, switching, listing, deletion, and the mental model behind branch pointers.

This is **Tutorial 7** in **Module 3: Branching** of the REBASH Academy Git series.

## Prerequisites

- [Viewing History and Diffs](viewing-history-and-diffs.md)
- [Basic Git Workflow — Add, Commit, Push](basic-git-workflow-add-commit-push.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Create branches with `git branch` and `git switch -c`
- [ ] Switch branches safely with `git switch` / `git checkout`
- [ ] List local and remote branches with tracking info
- [ ] Delete merged and unmerged branches
- [ ] Understand detached HEAD state and recovery
- [ ] Name branches following team conventions
- [ ] Relate branches to CI/CD environment promotion

## Branch Pointer Model

```d2
direction: right

MAIN: "main → commit C3"
    FEAT: "feature/waf → commit C2"
    HOT: "hotfix/ssl → commit C3"
    C1: "commit C1"
    C2: C2
    C1 -> C2
    C3: C3
    C2 -> C3
    FEAT -> C2: {
      style.stroke-dash: 3
    }
    MAIN -> C3
    HOT -> C3
```

## Architecture

This topic is primarily procedural. The mental model is a straight line from inputs (commands, config files, or manifests) to observable system state — verify each change with the validation steps later in this tutorial.

## Theory

### Branches Are Pointers

A branch is a file in `.git/refs/heads/` containing a 40-character commit SHA. When you commit on a branch, Git moves the pointer forward. Branches cost almost nothing — create liberally.

Default branch is typically `main` (formerly `master`). Protected branches on GitHub/GitLab enforce review rules and CI gates.

### Creating Branches

**Modern (Git 2.23+):**

```bash
git switch -c feature/add-monitoring
```

**Classic:**

```bash
git checkout -b feature/add-monitoring
git branch feature/add-monitoring
git switch feature/add-monitoring
```

Create from a specific starting point:

```bash
git switch -c hotfix/patch-1.2.1 v1.2.0
git switch -c experiment/main origin/main
```

### Switching Branches

```bash
git switch main
git switch feature/add-monitoring
```

Git requires a clean working tree (or forces stash) before switching if changes would be overwritten. Uncommitted changes on tracked files block the switch.

**Restore pattern (Git 2.23+):**

```bash
git restore --staged file
git restore file
```

### Listing Branches

```bash
git branch              # local
git branch -r           # remote-tracking
git branch -a           # all
git branch -vv          # with upstream and last commit
```

`-vv` shows tracking relationship — essential for knowing if you're ahead/behind remote.

### Deleting Branches

```bash
git branch -d feature/done    # safe delete (merged)
git branch -D feature/abandon # force delete
git push origin --delete feature/done  # remote delete
```

After merge, delete feature branches to reduce clutter. Many teams automate stale branch cleanup.

### Detached HEAD

Checking out a commit SHA or tag directly puts you in **detached HEAD**:

```bash
git switch --detach v1.0.0
```

You can look around and commit, but commits aren't on any branch until you create one:

```bash
git switch -c fix-from-v1.0.0
```

Detached HEAD is normal for CI checkout of specific SHAs and for bisect.

### Branch Naming Conventions

| Pattern | Example | Use |
|---------|---------|-----|
| `feature/description` | `feature/ingress-tls` | New capability |
| `fix/description` | `fix/memory-leak` | Bug fix |
| `hotfix/description` | `hotfix/cve-2026-1234` | Urgent prod fix |
| `release/x.y` | `release/2.4.0` | Release stabilization |
| `env/name` | `env/staging` | Environment-specific IaC (GitOps) |

Avoid slashes-only names that confuse tooling; keep names lowercase with hyphens.

### Branching and CI/CD

- **Feature branches** → PR triggers CI on branch push
- **Main branch** → deploy to staging after merge
- **Tags on main** → deploy to production
- **Long-lived env branches** → GitOps sync per environment (less common with trunk-based)

### Branch Housekeeping

Schedule weekly cleanup on shared repos:

```bash
git fetch --prune
git branch --merged main | grep -v 'main' | xargs -r git branch -d
```

Hosting platforms offer stale branch auto-delete after merge — enable in repository settings to prevent hundreds of orphaned `feature/` branches from cluttering branch lists and confusing new team members.

## Hands-on Lab

### Step 1 – Initialize repo with base commits

**Command:**

```bash
mkdir -p /tmp/git-branch-lab && cd /tmp/git-branch-lab
git init -b main
echo "v1" > app.txt && git add . && git commit -m "feat: v1 baseline"
echo "v2" >> app.txt && git add . && git commit -m "feat: v2 update"
git log --oneline
```

### Step 2 – Create and switch to feature branch

**Command:**

```bash
git switch -c feature/logging
echo "log=enabled" >> app.txt && git add . && git commit -m "feat: enable logging"
git log --oneline --all --graph
```

### Step 3 – Switch back to main

**Command:**

```bash
git switch main
cat app.txt
git log --oneline -1
```

**Explanation:** Main does not include logging commit — branches diverged.

### Step 4 – List branches with tracking

**Command:**

```bash
git branch -vv
git branch -a
```

### Step 5 – Detached HEAD experiment

**Command:**

```bash
git switch --detach HEAD~1
git status
echo "detached edit" >> app.txt
git commit -am "wip: detached commit"
git switch -c recover-detached
git log --oneline -3
```

### Step 6 – Merge feature (preview for next tutorial)

**Command:**

```bash
git switch main
git merge feature/logging
git branch -d feature/logging
git branch -d recover-detached
git log --oneline --graph
```

### Step 7 – Clean up

**Command:**

```bash
cd /tmp && rm -rf git-branch-lab
```

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

| Command | Description | Example |
|---------|-------------|---------|
| `git branch name` | Create branch at HEAD | `git branch feature/x` |
| `git switch -c name` | Create and switch | `git switch -c feature/x` |
| `git switch branch` | Switch branch | `git switch main` |
| `git branch -d name` | Delete merged branch | `git branch -d feature/x` |
| `git branch -a` | List all branches | `git branch -a` |
| `git branch -vv` | Verbose with upstream | `git branch -vv` |
| `git switch --detach REF` | Detached HEAD | `git switch --detach v1.0` |

### Branch cleanup script

```bash
#!/usr/bin/env bash
# git-prune-merged.sh — delete local branches merged into main
set -euo pipefail
git fetch --prune
git switch main
git pull --ff-only
git branch --merged main | grep -v '^\* main$' | while read -r b; do
  git branch -d "$b"
done
echo "Merged branches cleaned."
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Working on main directly"
    Unprotected main commits skip review and CI gates. Use feature branches unless trunk-based with feature flags.

!!! warning "Forgetting to pull before creating branch"
    Branch from stale main causes unnecessary merge conflicts later. `git pull` on main first.

!!! warning "Leaving hundreds of stale branches"
    Clutter confuses reviewers. Delete after merge; use platform auto-delete settings.

!!! warning "Losing detached HEAD commits"
    Commits in detached state disappear when switching away without creating a branch. Name branch immediately.

## Best Practices

!!! tip "Keep branches short-lived"
    Target merge within days, not months. Long-lived branches accumulate merge debt.

!!! tip "One branch per ticket"
    Map `feature/JIRA-1234-add-waf` to traceability in audit logs.

!!! tip "Use git switch over checkout for clarity"
    `switch` handles branches; `checkout` also restores files — separate concerns reduce errors.

!!! tip "Protect main and production branches"
    Require PR, CI pass, and code review on hosting platform.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Cannot switch branch | Uncommitted changes conflict | Commit, stash, or discard changes |
| Branch already exists | Name collision | Choose new name or delete old |
| `-d` refuses delete | Unmerged commits | Merge first or use `-D` if intentional |
| Detached HEAD warning | Checked out commit/tag | `git switch main` or create branch |
| Remote branch not listed | Not fetched | `git fetch --all` |
| Wrong base commit | Created branch from wrong ref | Recreate from correct base |

## Summary

- **Branches** are lightweight pointers to commits — cheap to create and delete
- Use **git switch -c** to create branches; **git switch** to move between them
- **Detached HEAD** occurs when checking out a commit directly — create a branch to keep work
- Follow **naming conventions** (`feature/`, `fix/`, `hotfix/`) for team clarity
- Delete merged branches locally and remotely to keep repositories manageable

## Interview Questions

1. What is a Git branch at the implementation level?
2. What is the difference between `git switch` and `git checkout`?
3. What is detached HEAD, and how do you recover from it?
4. How do you list all branches including remotes?
5. What is the difference between `git branch -d` and `-D`?
6. Why should feature branches be short-lived?
7. What branch naming conventions work well for DevOps teams?
8. How do branches relate to CI/CD pipeline triggers?
9. How do you create a branch from a specific tag or commit?
10. What happens to commits made in detached HEAD if you switch away without creating a branch?

??? tip "Sample Answers (Questions 1 and 3)"

    **Q1 — Branch implementation:** A branch is a named reference (ref) stored as a file under `.git/refs/heads/` containing the SHA-1 of the tip commit. Creating a branch only adds this pointer — no file copy occurs. Commits on the branch advance the pointer.

    **Q3 — Detached HEAD:** HEAD points directly to a commit instead of a branch ref. You can read and commit, but new commits aren't on any branch. Recovery: create a branch with `git switch -c new-branch` or merge/cherry-pick commits onto an existing branch before switching away.

## Related Tutorials

- [Viewing History and Diffs](viewing-history-and-diffs.md) *(previous — Module 2)*
- [Merging and Merge Conflicts](merging-and-merge-conflicts.md) *(next)*
- [Advanced Git Workflows](advanced-git-workflows.md)
- [Working with Remotes](working-with-remotes.md)
- [Git – Category Overview](index.md)
- Cheat sheet: [Git Cheat Sheet](../cheatsheets/git.md)
- Interview prep: [Git Interview Prep](../interview/git.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [Pro Git Book – Branching](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [git switch documentation](https://git-scm.com/docs/git-switch)
- [git branch documentation](https://git-scm.com/docs/git-branch)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [REBASH Academy – Git Overview](index.md)
