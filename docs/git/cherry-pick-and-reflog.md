---
title: Cherry-pick and Reflog
description: Apply specific commits across branches with cherry-pick, navigate reflog for recovery, and backport hotfixes in DevOps incident workflows.
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
category: git
tags:
  - git
  - cherry-pick
  - reflog
  - recovery
prerequisites:
  - Undoing Changes — Reset, Revert, and Stash
  - Rebasing and Interactive Rebase
comments: false
---

# Cherry-pick and Reflog

## Overview

Production is on `release/2.1` but the fix landed on `main` — cherry-pick copies that commit without merging entire branches. Accidentally ran `git reset --hard` — reflog remembers where HEAD was yesterday. These tools are essential for hotfix backports and disaster recovery.

This is **Tutorial 14** in **Module 5: Recovery & Debugging** of the REBASH Academy Git series.

## Prerequisites

- [Undoing Changes — Reset, Revert, and Stash](undoing-changes-reset-revert-stash.md)
- [Rebasing and Interactive Rebase](rebasing-and-interactive-rebase.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Cherry-pick commits onto another branch
- [ ] Resolve cherry-pick conflicts and continue/abort
- [ ] Cherry-pick ranges and multiple commits
- [ ] Use reflog to find lost commits and branches
- [ ] Recover from reset, rebase, and deleted branch mistakes
- [ ] Backport hotfixes to release branches
- [ ] Understand reflog expiration and limitations

## Cherry-pick and Reflog Diagram

```d2
direction: right

MAIN: "main: commit FIX"
    REL: "release/2.1"
    MAIN -> REL: "git cherry-pick FIX"
    HEAD: "HEAD moves"
    REFLOG: "reflog\n90 day journal"
    HEAD -> REFLOG
    RECOVER: "Recovered state"
    REFLOG -> RECOVER: "git reset --hard SHA"
```

## Theory

### git cherry-pick

Applies the **patch** of a specific commit onto current branch — new commit, new SHA, same diff (usually):

```bash
git switch release/2.1
git cherry-pick abc1234
```

Use cases:

- **Hotfix backport** — fix on main → cherry-pick to release branch
- **Selective feature** — one commit from large feature branch
- **Recover single commit** from abandoned branch

### Cherry-pick vs Merge

| Aspect | Cherry-pick | Merge |
|--------|-------------|-------|
| Scope | Single commit(s) | Entire branch |
| History | Linear add-on | Merge commit or FF |
| Duplicates | Same change, two SHAs | Single integration point |

Cherry-picked commits appear twice in history (different SHAs) — document in release notes.

### Conflict Resolution

Same as merge/rebase:

```bash
# fix conflicts
git add resolved-file
git cherry-pick --continue
git cherry-pick --abort
git cherry-pick --skip
```

### Cherry-pick Range

```bash
git cherry-pick A..B      # commits after A through B (exclusive A)
git cherry-pick A^..B     # include A
```

Order matters — applies oldest first.

### Cherry-pick Merge Commits

Requires `-m` to specify mainline parent — rarely needed; prefer cherry-picking individual commits from feature branch.

### No-commit Cherry-pick

```bash
git cherry-pick -n abc1234   # apply without committing
```

Useful to combine multiple picks into one commit.

### Reflog — Git's Safety Journal

Reflog records when HEAD and branch tips moved:

```bash
git reflog
git reflog show main
```

Format: `SHA HEAD@{n}: action: description`

Entries include commits reachable even after reset — **local only**, not pushed to remote.

### Recovery Scenarios

**Lost after hard reset:**

```bash
git reflog
git reset --hard HEAD@{3}
```

**Deleted branch:**

```bash
git reflog | grep "checkout: moving from feature"
git switch -c feature-recovered SHA
```

**Failed rebase:**

```bash
git reflog
git reset --hard HEAD@{1}   # before rebase started
```

### Reflog Expiration

Default: 90 days for reachable commits, 30 days for unreachable. Configurable via `gc.reflogExpire`. Don't rely on reflog as permanent backup.

### git cherry — Already Applied?

Check if commit exists on branch:

```bash
git cherry main feature-branch
```

`+` means not on main; `-` means equivalent patch present.

## Hands-on Lab

### Step 1 – Build main and release branches

**Command:**

```bash
mkdir -p /tmp/git-cherry-lab && cd /tmp/git-cherry-lab
git init -b main
echo "v2.0" > VERSION && git add . && git commit -m "release: v2.0 baseline"
git switch -c release/2.0
git switch main
echo "fix: critical patch" >> patch.log
git add patch.log && git commit -m "fix: critical security patch"
FIX_SHA=$(git rev-parse HEAD)
git log --oneline --all
```

### Step 2 – Cherry-pick fix to release

**Command:**

```bash
git switch release/2.0
git cherry-pick "$FIX_SHA"
git log --oneline --graph --all
cat patch.log
```

### Step 3 – Simulate disaster and recover

**Command:**

```bash
git switch main
git branch -D release/2.0
git reflog | head -10
RECOVER=$(git rev-parse "$FIX_SHA")
git switch -c release/2.0-recovered HEAD~1
git cherry-pick "$RECOVER"
git log --oneline -3
```

### Step 4 – Reflog after hard reset

**Command:**

```bash
git switch main
TIP=$(git rev-parse HEAD)
git reset --hard HEAD~2
git log --oneline -2
git reset --hard "$TIP"
git log --oneline -3
```

### Step 5 – Cherry-pick conflict

**Command:**

```bash
git switch -c conflict-demo HEAD~2
echo "different" > patch.log && git add . && git commit -m "conflict setup"
git switch main
git cherry-pick HEAD~1 2>/dev/null || git cherry-pick $(git rev-parse conflict-demo) || true
# Manual resolution if conflict:
git status
git cherry-pick --abort 2>/dev/null || true
```

### Step 6 – Clean up

**Command:**

```bash
cd /tmp && rm -rf git-cherry-lab
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `git cherry-pick SHA` | Apply commit | `git cherry-pick abc1234` |
| `git cherry-pick A..B` | Range of commits | `git cherry-pick main~3..main` |
| `git cherry-pick -x SHA` | Append source SHA to message | Audit trail |
| `git cherry-pick --abort` | Cancel cherry-pick | On conflict |
| `git reflog` | Show HEAD history | Recovery first step |
| `git reflog show branch` | Branch-specific reflog | `git reflog show main` |
| `git cherry main feature` | Check if commits applied | Backport verification |

### Hotfix backport script

```bash
#!/usr/bin/env bash
# backport.sh — cherry-pick commit to release branch
set -euo pipefail
COMMIT="${1:?Usage: backport.sh COMMIT_SHA release/x.y}"
RELEASE="${2:?release branch required}"
git fetch origin
git switch "$RELEASE"
git pull --ff-only origin "$RELEASE"
git cherry-pick -x "$COMMIT"
git push origin "$RELEASE"
echo "Backported $COMMIT to $RELEASE"
```

## Common Mistakes

!!! warning "Cherry-picking without -x on release branches"
    `-x` appends `(cherry picked from commit ...)` — audit trail for compliance.

!!! warning "Cherry-picking merge commits without -m"
    Fails or applies wrong diff. Pick individual commits instead.

!!! warning "Assuming reflog exists on remote"
    Reflog is local only. Deleted remote branches need platform recovery or teammate clone.

!!! warning "Cherry-pick order wrong for dependent commits"
    Pick oldest first; dependency failures cause conflicts.

## Best Practices

!!! tip "Tag release branches after backport"
    Annotated tag documents which fixes landed in patch release.

!!! tip "Run git cherry before batch backport"
    Skip already-applied commits.

!!! tip "Document backports in CHANGELOG"
    Link cherry-picked SHAs to CVE or incident tickets.

!!! tip "Increase reflog retention on build machines"
    CI runners doing complex rebases benefit from longer reflogExpire.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Cherry-pick empty | Change already present | Skip with `--skip` or `--continue` |
| Conflict on pick | Diverged files | Resolve; continue or abort |
| Commit not in reflog | Too old or gc pruned | Remote recovery; platform support |
| Wrong commit recovered | Misread reflog | Verify SHA with `git show` before reset |
| Duplicate fix different SHA | Expected with cherry-pick | Document; don't re-pick |
| `fatal: bad object` | Corrupt repo | fsck; re-clone |

## Summary

- **Cherry-pick** applies specific commit(s) to current branch — ideal for hotfix backports
- Use **-x** for audit trail; resolve conflicts like merge/rebase
- **Reflog** records local HEAD movements — primary recovery tool after reset/rebase
- Reflog is **local and time-limited** — not a substitute for remote backup
- **git cherry** verifies whether commits already exist on target branch

## Interview Questions

1. What does git cherry-pick do?
2. When would you cherry-pick instead of merge?
3. How do you recover a commit after git reset --hard?
4. What is reflog, and where is it stored?
5. How long does reflog retain entries?
6. What does cherry-pick -x add to commit messages?
7. How do you cherry-pick a range of commits?
8. Why doesn't reflog help recover deleted remote branches?
9. What is the difference between cherry-pick and revert?
10. How do you abort a failed cherry-pick?

??? tip "Sample Answers (Questions 1 and 3)"

    **Q1 — cherry-pick:** Git computes the diff introduced by a specified commit and applies it to the current branch as a new commit with a new SHA. Metadata (author date) may differ from committer date. Used to port fixes without merging entire branches.

    **Q3 — Recover after hard reset:** Run `git reflog` to find SHA before reset (e.g., HEAD@{1}). Verify with `git show SHA`. Run `git reset --hard SHA` to restore branch tip. Push only if branch is private or coordinate force push.

## Related Tutorials

- [Undoing Changes — Reset, Revert, and Stash](undoing-changes-reset-revert-stash.md) *(previous)*
- [Git Bisect and Debugging History](git-bisect-and-debugging-history.md) *(next)*
- [Rebasing and Interactive Rebase](rebasing-and-interactive-rebase.md)
- [Merging and Merge Conflicts](merging-and-merge-conflicts.md)
- [Git – Category Overview](index.md)

## References

- [Pro Git Book – Rebasing – Cherry-picking](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)
- [git cherry-pick documentation](https://git-scm.com/docs/git-cherry-pick)
- [git reflog documentation](https://git-scm.com/docs/git-reflog)
- [Atlassian – git reflog](https://www.atlassian.com/git/tutorials/rewriting-history/git-reflog)
- [REBASH Academy – Git Overview](index.md)
