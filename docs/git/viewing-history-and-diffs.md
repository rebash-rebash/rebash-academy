---
title: Viewing History and Diffs
description: Navigate commit history with git log, compare versions with git diff and git show, blame, grep, and audit trails for DevOps compliance.
difficulty: beginner
estimated_time: "35 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: git
tags:
  - git
  - log
  - diff
  - history
prerequisites:
  - Basic Git Workflow — Add, Commit, Push
  - Understanding the Git Object Model
comments: false
---

# Viewing History and Diffs

## Overview

When production breaks after a deploy, you need to know **what changed**, **when**, and **who**. Git's history and diff tools are your audit trail — every Terraform apply, every manifest update, every Dockerfile tweak is traceable. This tutorial teaches `git log`, `git diff`, `git show`, `git blame`, and search techniques used in incident response and compliance reviews.

This is **Tutorial 6** in **Module 2: Essential Workflow** of the REBASH Academy Git series.

## Prerequisites

- [Basic Git Workflow — Add, Commit, Push](basic-git-workflow-add-commit-push.md)
- [Understanding the Git Object Model](understanding-the-git-object-model.md)
- A repository with multiple commits (lab repo or any clone)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Navigate history with `git log` and formatting options
- [ ] Compare commits, branches, and files with `git diff`
- [ ] Inspect single commits with `git show`
- [ ] Use `git blame` to find who last changed a line
- [ ] Search commit messages and code changes with `git log -S` and `-G`
- [ ] Visualize history graphs for merge-heavy repos
- [ ] Export diffs for review and compliance archives

## History Navigation Diagram

```d2
direction: down

HEAD: "HEAD / main"
    C1: "commit N\nlatest fix"
    C2: "commit N-1\nfeature add"
    C3: "commit N-2\ninitial"
    HEAD -> C1
    C1 -> C2
    C2 -> C3
    LOG: "git log"
    LOG -> HEAD
    DIFF: "git diff C2 C1"
    DIFF -> C1
    BLAME: "git blame file"
    BLAME -> C2
    SHOW: "git show C1"
    SHOW -> C1
```

## Architecture

This topic is primarily procedural. The mental model is a straight line from inputs (commands, config files, or manifests) to observable system state — verify each change with the validation steps later in this tutorial.

## Theory

### git log — The History Browser

Basic usage:

```bash
git log
git log --oneline -20
git log --graph --decorate --all
```

**Useful filters:**

| Option | Purpose |
|--------|---------|
| `--author="name"` | Commits by author |
| `--since="2026-01-01"` | Date range |
| `--grep="fix"` | Search commit messages |
| `path/to/file` | History of one file |
| `-p` | Show patch (diff) for each commit |
| `--stat` | Summary of files changed |

### git diff — Comparing States

| Command | Compares |
|---------|----------|
| `git diff` | Working tree vs staging area |
| `git diff --staged` | Staging area vs last commit |
| `git diff HEAD` | Working tree vs last commit |
| `git diff main feature` | Tips of two branches |
| `git diff v1.0 v1.1` | Two tags |
| `git diff main..origin/main` | Local vs remote branch |

Three-dot diff (`main...feature`) shows changes on feature since branching — common for PR review.

### git show — One Commit Detail

```bash
git show HEAD
git show abc1234 --stat
git show v1.2.0:deploy/k8s/deployment.yaml
```

Shows commit metadata plus full diff. The `commit:path` syntax retrieves file content at that commit without checkout.

### git blame — Line-by-Line Attribution

```bash
git blame deploy/terraform/main.tf
git blame -L 40,60 Dockerfile
```

Each line shows commit SHA, author, date. In incidents: "who bumped the replica count to 50?"

Ignore whitespace and move detection:

```bash
git blame -w -M README.md
```

### Pickaxe Search — Finding When Code Changed

```bash
git log -S "replica_count" --oneline
git log -G "password.*=" --oneline
```

`-S` finds commits that changed occurrence count of a string. `-G` uses regex. Essential for tracing when a secret or config value was introduced.

### Follow Renames

```bash
git log --follow -- renames/old-name.tf
```

Tracks file across renames — default `git log path` may miss history before rename.

### Format Strings for Automation

```bash
git log --format='%H|%an|%ae|%s' -5
```

Machine-readable output for scripts parsing audit data.

### Diff Tools and External Review

```bash
git difftool -d main feature
git diff main feature > review.patch
```

Configure `difftool` for vimdiff, meld, or VS Code. Patch files attach to tickets or email review.

### Advanced Log Formatting for Audits

Compliance reviews often require machine-readable exports:

```bash
git log --since="2026-01-01" --until="2026-12-31" \
  --format='{"sha":"%H","author":"%an","email":"%ae","date":"%aI","subject":"%s"}' \
  -- terraform/
```

Filter by path for monorepos — only commits touching infrastructure:

```bash
git log --oneline --follow -- terraform/modules/vpc/
```

Combine with `--first-parent main` on merge-heavy repos to show linear main history without feature branch noise. Store export scripts in `scripts/audit-git-log.sh` and run quarterly for SOC 2 evidence collection.

## Hands-on Lab

### Step 1 – Create repository with history

**Command:**

```bash
mkdir -p /tmp/git-history-lab && cd /tmp/git-history-lab
git init -b main
echo "replicas: 1" > deploy.yaml && git add . && git commit -m "feat: initial deploy config"
echo "replicas: 3" >> deploy.yaml && sed -i '' 's/replicas: 1/replicas: 3/' deploy.yaml 2>/dev/null || sed -i 's/replicas: 1/replicas: 3/' deploy.yaml
git add deploy.yaml && git commit -m "fix: scale replicas to 3"
echo "memory: 512Mi" >> deploy.yaml && git add . && git commit -m "feat: add memory limit"
git log --oneline
```

### Step 2 – Graph and decorated log

**Command:**

```bash
git log --graph --decorate --oneline --all
git log --stat -2
```

### Step 3 – Compare commits

**Command:**

```bash
git diff HEAD~2 HEAD
git diff HEAD~1 HEAD -- deploy.yaml
```

**Explanation:** `HEAD~2` means two commits before HEAD.

### Step 4 – git show and file at commit

**Command:**

```bash
git show HEAD~1 -- deploy.yaml
git show HEAD~2:deploy.yaml
```

### Step 5 – git blame

**Command:**

```bash
git blame deploy.yaml
git blame -L 1,3 deploy.yaml
```

### Step 6 – Pickaxe search

**Command:**

```bash
git log -S "replicas: 3" --oneline
git log --grep="scale" --oneline
```

### Step 7 – Clean up

**Command:**

```bash
cd /tmp && rm -rf git-history-lab
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
| `git log --oneline` | Compact history | `git log --oneline -15` |
| `git log --graph --all` | Branch graph | `git log --graph --decorate --all` |
| `git diff A B` | Diff between refs | `git diff main develop` |
| `git diff --staged` | Staged vs HEAD | `git diff --staged` |
| `git show COMMIT` | Commit details + patch | `git show abc1234` |
| `git blame FILE` | Line attribution | `git blame -w main.tf` |
| `git log -S "string"` | Pickaxe search | `git log -S "API_KEY"` |
| `git log --follow -- FILE` | History through renames | `git log --follow -- old.tf` |

### Audit export script

```bash
#!/usr/bin/env bash
# git-audit-export.sh — export commit log for compliance
set -euo pipefail
REPO="${1:-.}"
SINCE="${2:-2026-01-01}"
cd "$REPO"
git log --since="$SINCE" \
  --format='commit %H%nAuthor: %an <%ae>%nDate: %ad%nSubject: %s%n' \
  --date=iso-strict \
  --name-status
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Using git log without path filter on monorepos"
    Full log on large repos is overwhelming. Scope to directory: `git log -- services/payment/`.

!!! warning "Misreading two-dot vs three-dot diff"
    `A..B` and `A...B` differ. Three-dot shows changes on B since common ancestor — standard for PRs.

!!! warning "Trusting blame on merged code"
    Blame shows last line edit — squash merges may hide intermediate authors. Use `git log -L` for line history.

!!! warning "Shallow clone breaks deep history"
    `git log` stops at shallow boundary. Unshallow before audit investigations.

## Best Practices

!!! tip "Use --stat before full diff in review"
    Stat summary shows scope; full diff when files matter.

!!! tip "Reference commit SHAs in incident tickets"
    Full SHA pins exact code state — branch names move.

!!! tip "Configure log.date iso"
    `git config --global log.date iso` — unambiguous timestamps in global teams.

!!! tip "Combine blame with show for context"
    Blame finds SHA; `git show SHA` explains why the change was made.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Empty git log | No commits or wrong directory | Verify repo; check branch |
| Diff shows nothing | Comparing identical refs | Verify SHAs; check staging state |
| Blame shows wrong author | Line moved or whitespace | Use `-w -M -C` flags |
| `unknown revision` | Invalid ref or shallow history | `git fetch`; verify ref exists |
| Log missing old file history | Rename without --follow | `git log --follow -- path` |
| Huge diff output | Binary or minified files | Exclude paths; use `--stat` first |

## Summary

- **git log** navigates history with filters for author, date, path, and message
- **git diff** compares working tree, staging area, commits, branches, and tags
- **git show** displays one commit; **git blame** attributes lines to authors and commits
- **Pickaxe search** (`-S`, `-G`) finds when specific strings entered or left the codebase
- History tools are essential for incident response, compliance audits, and code review

## Interview Questions

1. What is the difference between `git diff` and `git diff --staged`?
2. How do you show the last 10 commits in one line each?
3. What does `git blame` do, and when would you use it?
4. Explain two-dot vs three-dot diff syntax.
5. How do you find which commit introduced a specific string?
6. What does `git show COMMIT:path/to/file` return?
7. How do you view history of a file that was renamed?
8. What git log options help visualize branch merges?
9. How would you export commit history for a compliance audit?
10. Why might git blame show unexpected authors?

??? tip "Sample Answers (Questions 4 and 5)"

    **Q4 — Two-dot vs three-dot:** `git diff A..B` (two-dot) shows all differences between the tips of A and B. `git diff A...B` (three-dot) shows changes on B since the common ancestor of A and B — what would be merged if B were merged into A. PR reviews typically use three-dot.

    **Q5 — Finding string introduction:** Use pickaxe: `git log -S "search_string" --oneline`. For regex patterns use `-G`. Add `-p` to see the actual patch. Scope with path: `git log -S "replica_count" -- deploy/`.

## Related Tutorials

- [Basic Git Workflow — Add, Commit, Push](basic-git-workflow-add-commit-push.md) *(previous)*
- [Branching Fundamentals](branching-fundamentals.md) *(next — Module 3)*
- [Git Bisect and Debugging History](git-bisect-and-debugging-history.md)
- [Cherry-pick and Reflog](cherry-pick-and-reflog.md)
- [Git – Category Overview](index.md)

## References

- [Pro Git Book – Viewing History](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)
- [git log documentation](https://git-scm.com/docs/git-log)
- [git diff documentation](https://git-scm.com/docs/git-diff)
- [git blame documentation](https://git-scm.com/docs/git-blame)
- [REBASH Academy – Git Overview](index.md)
