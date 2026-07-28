---
title: Undoing Changes — Reset, Revert, and Stash
description: Discard, reset, revert, and stash changes safely; understand soft, mixed, and hard reset; recover work without breaking shared history.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
category: git
tags:
  - git
  - reset
  - revert
  - stash
  - recovery
prerequisites:
  - gitignore and gitattributes
  - Basic Git Workflow — Add, Commit, Push
comments: false
---

# Undoing Changes — Reset, Revert, and Stash

## Overview

Mistakes happen — wrong commit on main, accidental `git add` of secrets, need to context-switch mid-feature. Git provides reset, revert, restore, and stash to undo work at different levels. Choosing the wrong tool on shared branches causes outages; choosing the right one saves production.

This is **Tutorial 13** in **Module 5: Recovery & Debugging** of the REBASH Academy Git series.

## Prerequisites

- [gitignore and gitattributes](gitignore-and-gitattributes.md)
- [Basic Git Workflow — Add, Commit, Push](basic-git-workflow-add-commit-push.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Distinguish reset, revert, restore, and stash
- [ ] Apply soft, mixed, and hard reset appropriately
- [ ] Revert commits on shared branches safely
- [ ] Stash and restore work-in-progress changes
- [ ] Unstage and discard working directory changes
- [ ] Know when NOT to reset shared history
- [ ] Recover from accidental hard reset using reflog

## Undo Operations Diagram

```d2
direction: down

WT: "Working Tree"
    SA: "Staging Area"
    REPO: "Repository / Commits"
    RESTORE1: "git restore file"
    RESTORE1 -> WT
    RESTORE2: "git restore --staged"
    RESTORE2 -> SA
    RESET: "git reset --soft/mixed/hard"
    RESET -> SA
    RESET -> REPO
    REVERT: "git revert"
    REVERT -> REPO
    STASH: "git stash"
    STASH -> WT
    STASH -> SA
```

## Theory

### Levels of Undo

| Scope | Undo tool |
|-------|-----------|
| Uncommitted file edits | `git restore file` |
| Staged but uncommitted | `git restore --staged file` |
| Last commit (local, unpushed) | `git reset --soft HEAD~1` |
| Published commit on shared branch | `git revert` |
| Temporary context switch | `git stash` |

### git restore (Git 2.23+)

```bash
git restore app.yaml              # discard working changes
git restore --staged app.yaml     # unstage
git restore --source=HEAD~1 file  # restore file from old commit
```

Replaces older `git checkout -- file` pattern.

### git reset — Three Modes

Moves branch pointer; optionally affects staging and working tree:

| Mode | Moves branch | Staging | Working tree |
|------|--------------|---------|--------------|
| `--soft` | Yes | Unchanged | Unchanged |
| `--mixed` (default) | Yes | Reset | Unchanged |
| `--hard` | Yes | Reset | Reset |

```bash
git reset --soft HEAD~1    # undo commit, keep changes staged
git reset HEAD~1           # undo commit, keep changes unstaged
git reset --hard HEAD~1    # destroy commit AND changes — dangerous
```

**Hard reset on shared branches is catastrophic** — use revert instead.

### git revert

Creates a **new commit** that inverse-applies a previous commit:

```bash
git revert abc1234
git revert HEAD
git revert -m 1 MERGE_COMMIT   # revert merge (mainline parent 1)
```

Safe for production — history preserved; audit trail shows explicit undo.

### git stash

Temporarily shelves uncommitted changes:

```bash
git stash push -m "wip: healthcheck"
git stash list
git stash pop                  # apply and remove
git stash apply stash@{0}      # apply keep stash
git stash drop stash@{0}
```

Stash including untracked:

```bash
git stash push -u -m "including new files"
```

### Stash vs Commit

Stash for dirty tree when switching branches; commit for work worth preserving in history.

### Reset vs Revert Decision Tree

- **Unpushed local commits?** → reset OK
- **Already pushed to shared branch?** → revert
- **Need to remove secret from history?** → filter-repo + force push (emergency, coordinated)

### ORIG_HEAD and Reflog

Git saves previous HEAD in `ORIG_HEAD` after destructive operations. **Reflog** records all HEAD movements — recovery safety net (next tutorials expand).

### Production Rollback Scenarios

| Scenario | Recommended tool | Why |
|----------|------------------|-----|
| Bad commit merged to main, already deployed | `git revert` | Preserves audit trail; triggers normal CI/CD |
| Wrong files staged locally, not pushed | `git restore --staged` | No history impact |
| Need to discard local experiment | `git restore .` or `git stash` | Working tree only |
| Catastrophic merge on unpushed branch | `git reset --hard ORIG_HEAD` | Local recovery |
| Context switch mid-Terraform edit | `git stash push -u` | Resume later without commit noise |

In regulated environments, **revert** is preferred because compliance auditors see an explicit undo commit linked to the incident ticket. Reset on shared branches requires force push — almost never approved for `main` or production branches.

### Stash Stack Management

Multiple stashes form a stack — newest first in `git stash list`:

```bash
git stash list
git stash apply stash@{2}    # apply older stash without removing
git stash drop stash@{0}     # remove top stash after manual merge
git stash clear              # delete all stashes — use carefully
```

Name stashes descriptively in team environments so `stash@{0}` is identifiable during incident handoffs.

## Hands-on Lab

### Step 1 – Setup with commits

**Command:**

```bash
mkdir -p /tmp/git-undo-lab && cd /tmp/git-undo-lab
git init -b main
echo "v1" > app.txt && git add . && git commit -m "feat: v1"
echo "v2" >> app.txt && git add . && git commit -m "feat: v2"
echo "v3" >> app.txt && git add . && git commit -m "feat: v3"
git log --oneline
```

### Step 2 – Soft reset

**Command:**

```bash
git reset --soft HEAD~1
git status
git log --oneline -2
git commit -m "feat: v3 improved message"
```

### Step 3 – Mixed reset and restore

**Command:**

```bash
echo "mistake" >> app.txt
git add app.txt
git reset HEAD app.txt
git status
git restore app.txt
cat app.txt
```

### Step 4 – Stash workflow

**Command:**

```bash
echo "wip feature" >> feature.txt
git stash push -u -m "wip feature file"
git status
git stash list
git stash pop
git status
```

### Step 5 – Revert (simulating shared branch)

**Command:**

```bash
BAD=$(git rev-parse HEAD~1)
git revert --no-edit "$BAD"
git log --oneline -5
cat app.txt
```

### Step 6 – Hard reset and reflog recovery

**Command:**

```bash
BEFORE=$(git rev-parse HEAD)
git reset --hard HEAD~2
git log --oneline -3
git reset --hard "$BEFORE"
git log --oneline -3
```

### Step 7 – Clean up

**Command:**

```bash
cd /tmp && rm -rf git-undo-lab
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `git restore file` | Discard working changes | `git restore deploy.yaml` |
| `git restore --staged file` | Unstage | `git restore --staged .` |
| `git reset --soft HEAD~1` | Undo commit, keep staged | Soft reset last commit |
| `git reset --hard HEAD~1` | Undo commit, discard all | **Dangerous** |
| `git revert SHA` | Inverse commit on shared branch | `git revert abc1234` |
| `git stash push -m "msg"` | Shelve WIP | `git stash push -u` |
| `git stash pop` | Apply and remove stash | After context switch |

### Emergency revert script

```bash
#!/usr/bin/env bash
# revert-last-main.sh — safely revert latest commit on main
set -euo pipefail
git switch main
git pull --ff-only origin main
git revert --no-edit HEAD
git push origin main
echo "Reverted $(git rev-parse HEAD~1) on main."
```

## Common Mistakes

!!! warning "git reset --hard on shared main"
    Rewrites history others depend on. Use revert for published commits.

!!! warning "Stashing secrets"
    Stash contents persist in `.git/` — don't stash files with credentials long-term.

!!! warning "Revert merge without -m"
    Reverting merge commits requires specifying mainline parent: `git revert -m 1 SHA`.

!!! warning "Assuming reset is undoable forever"
    Reflog expires (~90 days default). Hard reset + gc may lose recovery path.

## Best Practices

!!! tip "Prefer revert for production rollbacks"
    Creates auditable undo commit; triggers CI same as any push.

!!! tip "Use stash with descriptive messages"
    `git stash push -m "JIRA-123 half-done IAM policy"` — not bare stash.

!!! tip "Soft reset to reword unpushed commits"
    Alternative to amend when multiple commits need message fix.

!!! tip "Document rollback runbooks with revert commands"
    On-call should revert SHA, not force-push main.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Changes lost after hard reset | Hard reset discarded work | `git reflog`; reset to old SHA |
| Revert conflict | Overlapping later changes | Resolve; complete revert commit |
| Stash pop conflict | Diverged branch since stash | Resolve conflicts; drop stash manually |
| Cannot revert merge | Missing -m flag | `git revert -m 1 MERGE_SHA` |
| restore: path not found | Wrong path or deleted | Check `git status` paths |
| Reset doesn't affect remote | Reset is local only | Force push (dangerous) or revert |

## Summary

- **restore** discards unstaged changes; **restore --staged** unstages
- **reset --soft/mixed/hard** moves branch pointer; hard destroys uncommitted work
- **revert** adds inverse commit — safe for shared/production branches
- **stash** temporarily shelves WIP for branch switches
- Unpushed history: reset OK; published history: revert; recovery: reflog

## Interview Questions

1. What is the difference between reset and revert?
2. Explain soft, mixed, and hard reset.
3. When is hard reset appropriate?
4. How does git stash work?
5. How do you unstage a file without losing edits?
6. How do you revert a merge commit?
7. Why should you avoid reset on shared branches?
8. What is ORIG_HEAD?
9. How do you recover after accidental git reset --hard?
10. When use stash vs temporary commit?

??? tip "Sample Answers (Questions 1 and 2)"

    **Q1 — reset vs revert:** Reset moves the branch pointer backward, optionally discarding staging and working tree changes — rewrites local history. Revert creates a new commit applying the inverse patch of a target commit — preserves history. Use reset for unpushed local fixes; revert for shared branches.

    **Q2 — Reset modes:** Soft moves HEAD only — commits become staged changes. Mixed (default) moves HEAD and resets index — commits become unstaged working changes. Hard moves HEAD, resets index, and overwrites working tree to match — discards uncommitted work entirely.

## Related Tutorials

- [gitignore and gitattributes](gitignore-and-gitattributes.md) *(previous — Module 4)*
- [Cherry-pick and Reflog](cherry-pick-and-reflog.md) *(next)*
- [Rebasing and Interactive Rebase](rebasing-and-interactive-rebase.md)
- [Git Bisect and Debugging History](git-bisect-and-debugging-history.md)
- [Git – Category Overview](index.md)

## References

- [Pro Git Book – Undoing Things](https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things)
- [git reset documentation](https://git-scm.com/docs/git-reset)
- [git revert documentation](https://git-scm.com/docs/git-revert)
- [git stash documentation](https://git-scm.com/docs/git-stash)
- [REBASH Academy – Git Overview](index.md)
