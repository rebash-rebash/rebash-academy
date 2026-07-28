---
title: Basic Git Workflow — Add, Commit, Push
description: Master the daily Git cycle — status, add, commit, push, and pull — with staging strategies, commit messages, upstream tracking, and DevOps CI/CD integration patterns.
difficulty: beginner
estimated_time: "35 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: git
tags:
  - git
  - workflow
  - commit
  - push
  - staging
  - devops
prerequisites:
  - Creating and Cloning Repositories
  - Git Installation and Configuration
  - Understanding the Git Object Model
comments: false
---

# Basic Git Workflow — Add, Commit, Push

## Overview

The daily DevOps rhythm is **`git pull` → edit → `git status` → `git add` → `git commit` → `git push`**. Whether you are updating a Kubernetes manifest, fixing a Terraform variable, or patching an Ansible role, this cycle is identical. Mastery of the **three trees** (working directory, staging area, repository), deliberate **staging**, and **meaningful commit messages** separates clean audit trails from unsearchable history that breaks automated changelogs and code review.

This tutorial walks through the complete workflow, partial staging, commit message conventions, pushing to remotes with upstream tracking, pulling safely before push, and how this cycle triggers CI/CD pipelines in production environments.

This is **Tutorial 5** in **Module 2: Essential Workflow** of the REBASH Academy Git series. Complete [Creating and Cloning Repositories](creating-and-cloning-repositories.md) first. Network connectivity for push/pull is covered in the [Networking track](../networking/index.md).

## Prerequisites

- [Creating and Cloning Repositories](creating-and-cloning-repositories.md) — you can init or clone a repo
- [Git Installation and Configuration](git-installation-and-configuration.md) — identity configured
- [Understanding the Git Object Model](understanding-the-git-object-model.md) — three trees mental model
- A cloned or initialized repository with a configured remote (GitHub/GitLab test repo recommended)
- SSH or HTTPS authentication working

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Execute the full workflow: status → add → commit → push → pull
- [ ] Explain the difference between working directory, staging area, and repository
- [ ] Stage changes selectively using files, directories, patches, and interactive mode
- [ ] Write commit messages that satisfy team conventions and automated tooling
- [ ] Push commits to remotes and set upstream tracking branches
- [ ] Pull remote changes safely before pushing to shared branches
- [ ] Inspect staged and unstaged diffs before committing
- [ ] Relate local commits to CI/CD pipeline triggers and deployment traceability

## Architecture

The workflow moves changes through three trees before reaching the remote server where CI/CD watches for events.

```d2
direction: right

WD: "Working Directory\nedited files"
    SA: "Staging Area\nindex"
    REPO: "Local Repository\n.git/objects"
    REMOTE: "Remote\norigin/main"
    CI: "CI Pipeline"
    WD -> SA: "git add"
    SA -> REPO: "git commit"
    REPO -> REMOTE: "git push"
    REMOTE -> CI: webhook
    REMOTE -> REPO: "git pull / fetch"
    REPO -> WD: checkout
```

## Theory

### The Three Trees Revisited

| Tree | Command to inspect | Modified by |
|------|-------------------|-------------|
| Working directory | `git status`, `git diff` | File editors, build tools |
| Staging area (index) | `git diff --staged` | `git add`, `git reset` |
| Repository | `git log`, `git show` | `git commit` |

**Unstaged changes** — modified in working directory but not in index.
**Staged changes** — marked for next commit.
**Committed changes** — permanent objects in `.git/objects/`.

`git status -s` provides porcelain short format used by scripts:

```text
 M README.md      # modified, unstaged
M  main.tf        # modified, staged
A  new.yaml       # added, staged
?? secret.env     # untracked
```

### `git add` Strategies

| Command | Effect |
|---------|--------|
| `git add file.txt` | Stage specific file |
| `git add directory/` | Stage all changes under directory |
| `git add .` | Stage all changes in current tree (careful!) |
| `git add -p` | Interactive patch staging — split hunks |
| `git add -u` | Stage modifications and deletions (not new files) |
| `git add -A` | Stage everything including deletions repo-wide |

DevOps best practice: **never** `git add .` without reviewing `git status` first. Terraform plans and kubeconfig backups must not enter commits.

### Writing Commit Messages

**Conventional Commits** format — widely used for automated changelogs and semantic release:

```text
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `ci`, `build`, `test`.

Examples for infrastructure:

```text
feat(terraform): add WAF module for production ALB

Enable AWS WAFv2 with managed rule groups on the public
load balancer. Closes PLATFORM-442.

fix(k8s): correct resource limits for api deployment

Memory limit was 128Mi causing OOMKills under load.
Increased to 512Mi based on Prometheus metrics.

ci(github-actions): pin terraform to 1.8.4
```

Subject line rules:

- Imperative mood: "Add feature" not "Added feature"
- ≤ 50 characters for subject (72 max for tools)
- Body explains **why**, not just what diff shows
- Reference ticket IDs for traceability

### `git commit` Options

| Command | Use case |
|---------|----------|
| `git commit -m "msg"` | Single-line message |
| `git commit` | Opens editor for full message |
| `git commit -a` | Stage all **tracked** modifications, skip new files |
| `git commit --amend` | Modify last commit (before push!) |
| `git commit --no-verify` | Skip hooks (avoid unless emergency) |

Pre-commit hooks (lint, secrets scan) run before commit completes — covered in Module 6.

### `git push` and Upstream Tracking

```bash
git push origin main           # Push local main to remote main
git push -u origin feature/x   # Push and set upstream for new branch
git push                       # Push current branch to tracked upstream
```

Push sends local commits to remote. Remote rejects if you lack permissions or if remote has commits you don't have (non-fast-forward).

**Protected branches** (GitHub/GitLab) block direct push to `main` — require pull requests. DevOps engineers push feature branches; merge via review.

### `git pull` Before Push

```bash
git pull origin main    # fetch + merge
git pull --rebase origin main   # fetch + rebase (cleaner history)
```

Always pull (or fetch + rebase) before pushing to shared branches to incorporate teammates' commits. Merge conflicts surface here — resolved in working directory, staged, and committed.

### How Commits Trigger CI/CD

| Event | Typical pipeline action |
|-------|---------------------------|
| Push to feature branch | Run tests, lint, plan (Terraform) |
| Open pull request | Full validation + review gates |
| Merge to `main` | Build artifact, deploy to staging |
| Tag push `v*` | Production release, signed images |

Commit SHA becomes the correlation ID across logs, Docker tags, and deployment records.

## Hands-on Lab

Use a test repository — create one on GitHub/GitLab or work locally with a bare remote simulation.

### Step 1 – Clone or initialize lab repository

**Command:**

```bash
mkdir -p ~/lab/git-workflow && cd ~/lab/git-workflow
git init
git config user.email "lab@example.com"
git config user.name "Lab User"
echo "# Workflow Lab" > README.md
git add README.md
git commit -m "docs: initial README"
git log --oneline
```

**Explanation:** Start with one commit baseline. Per-repo config overrides global for isolated lab identity.

**Expected output:**

```text
abc1234 docs: initial README
```

### Step 2 – Make changes and inspect status

**Command:**

```bash
echo "replica_count = 2" >> terraform.tfvars.example
echo "debug = true" >> .env.local
git status
git status -s
```

**Explanation:** `.env.local` should be untracked — we'll add it to `.gitignore` before committing other files.

**Expected output:**

```text
Untracked files:
  .env.local
  terraform.tfvars.example
```

### Step 3 – Create .gitignore and stage selectively

**Command:**

```bash
echo ".env.local" >> .gitignore
git add .gitignore terraform.tfvars.example
git status
git diff --staged
```

**Explanation:** Stage only intended files. `git diff --staged` reviews index vs last commit before committing.

**Expected output:**

```text
Changes to be committed:
  new file:   .gitignore
  new file:   terraform.tfvars.example
```

### Step 4 – Commit with conventional message

**Command:**

```bash
git commit -m "feat(terraform): add example tfvars and gitignore

Add terraform.tfvars.example documenting replica_count.
Ignore .env.local to prevent accidental secret commits."
git log -1 --format=fuller
```

**Explanation:** Multi-line `-m` accepts `\n\n` for body. Fuller format shows author vs committer.

**Expected output:**

```text
def5678 feat(terraform): add example tfvars and gitignore
Author:     Lab User <lab@example.com>
Commit:     Lab User <lab@example.com>
...
```

### Step 5 – Commit second change and view history

**Command:**

```bash
echo 'instance_type = "t3.micro"' >> terraform.tfvars.example
git add terraform.tfvars.example
git commit -m "feat(terraform): add instance_type to example tfvars"
git log --oneline --graph
git show HEAD --stat
```

**Explanation:** `--stat` summarizes files changed per commit — quick review before push.

**Expected output:**

```text
* ghi9012 feat(terraform): add instance_type to example tfvars
* def5678 feat(terraform): add example tfvars and gitignore
* abc1234 docs: initial README
```

### Step 6 – Simulate remote with bare repo and push

**Command:**

```bash
cd ~/lab
git clone --bare git-workflow workflow-remote.git
cd ~/lab/git-workflow
git remote add origin ~/lab/workflow-remote.git
git push -u origin main
git branch -vv
```

**Explanation:** Local bare repo simulates `origin` without network. `-u` sets upstream — enables bare `git push` / `git pull`.

**Expected output:**

```text
To ~/lab/workflow-remote.git
 * [new branch]      main -> main
* main abc1234 [origin/main] docs: initial README
```

Note: push sends **all** commits not on remote — three commits total after push completes.

### Step 7 – Pull, modify, push again

**Command:**

```bash
echo "## Lab complete" >> README.md
git add README.md
git commit -m "docs: mark lab section complete"
git pull --rebase origin main
git push origin main
git log --oneline origin/main
```

**Explanation:** Pull before push integrates remote changes. `--rebase` replays your commit atop remote tip for linear history.

**Expected output:**

```text
Successfully rebased and updated refs/heads/main.
...
jkl3456 docs: mark lab section complete
```

### Step 8 – Clean up

**Command:**

```bash
rm -rf ~/lab/git-workflow ~/lab/workflow-remote.git
```

**Explanation:** Remove lab artifacts.

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
| `git status` | Show working tree and staging state | `git status -s` |
| `git diff` | Unstaged changes | `git diff` |
| `git diff --staged` | Staged changes vs HEAD | `git diff --staged` |
| `git add` | Stage changes | `git add -p file` |
| `git commit` | Create commit from index | `git commit -m "fix: ..."` |
| `git push` | Send commits to remote | `git push -u origin main` |
| `git pull` | Fetch and integrate remote | `git pull --rebase` |
| `git log` | View commit history | `git log --oneline -5` |

### Terraform CI-friendly commit check

```bash
#!/usr/bin/env bash
# verify-no-tfstate.sh — block tfstate from commits
set -euo pipefail

if git diff --cached --name-only | grep -E '\.tfstate($|\.)'; then
  echo "ERROR: Terraform state file staged — unstage immediately"
  exit 1
fi

echo "OK: no tfstate in staged files"
```

Install as pre-commit hook: `cp verify-no-tfstate.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit`

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Committing without reviewing staged diff"
    `git add .` followed by immediate commit has leaked production credentials into public repos countless times. Always run `git diff --staged` before commit.

!!! warning "Vague commit messages like 'fix' or 'update'"
    Messages must stand alone in `git log` years later. Include scope and reason: `fix(alb): increase idle timeout for long-running reports`.

!!! warning "Push without pull on shared branches"
    Causes non-fast-forward rejections or accidental merge commits. Pull or rebase first; resolve conflicts locally.

!!! warning "Amending commits already pushed to shared branches"
    Amend creates new SHA; teammates' history diverges. Only amend unpushed local commits unless team agrees on force push protocol.

!!! warning "Using `git commit -a` and expecting new files included"
    `-a` skips untracked files. New files require explicit `git add`.

## Best Practices

!!! tip "One logical change per commit"
    Separate Terraform module addition from unrelated README typo fix. Enables clean reverts and accurate `git bisect`.

!!! tip "Pull with rebase on feature branches"
    `git pull --rebase` keeps history linear before opening pull requests — easier review for senior engineers.

!!! tip "Reference tickets in commit footers"
    `Closes PLATFORM-442` links VCS history to Jira/Linear — essential for change management audits.

!!! tip "Let CI validate before merging — not instead of local review"
    Run `terraform fmt`, `ansible-lint`, or `kubectl dry-run` locally; CI confirms in clean environment.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `nothing to commit, working tree clean` | No changes or all already committed | Verify edits saved; run `git status` |
| `Changes not staged for commit` | Modified but not added | `git add` the files |
| `rejected – non-fast-forward` | Remote has commits you lack | `git pull --rebase` then push |
| `Permission denied` on push | Auth failure or branch protection | Check SSH/PAT; use feature branch + PR |
| Wrong files in commit | Over-broad `git add` | `git reset HEAD~1` (if not pushed); recommit selectively |
| Merge conflict on pull | Same lines edited remotely and locally | Edit conflict markers; `git add`; `git commit` |
| Empty commit message abort | Editor closed without message | Re-run commit with `-m` |
| Pre-commit hook failed | Lint or secrets scan blocked commit | Fix issues; never `--no-verify` in production repos |

## Summary

- Daily workflow: **edit → status → add → commit → pull → push**
- Changes flow through **working directory → staging area → repository → remote**
- Stage deliberately with `git add -p`; review with `git diff --staged`
- Write **conventional commit messages** with type, scope, and ticket references
- **`git push -u`** sets upstream tracking; **`git pull --rebase`** integrates remote changes cleanly
- Each push to tracked branches can **trigger CI/CD** — commit SHA links code to pipeline runs and deployments

## Interview Questions

1. Explain the three trees in Git and how changes move between them.
2. What is the difference between `git diff` and `git diff --staged`?
3. When would you use `git add -p` instead of `git add .`?
4. Describe the Conventional Commits format with an infrastructure example.
5. What does `git push -u origin feature/x` do?
6. Why should you pull before pushing to a shared branch?
7. What happens when a pre-commit hook fails?
8. How do commits on `main` relate to CI/CD pipeline triggers?
9. What is the difference between `git commit -a` and `git add -A && git commit`?
10. Why should you avoid amending commits that have been pushed?

??? tip "Sample Answers (Questions 1, 5, and 8)"

    **Q1 — Three trees:** The **working directory** holds files you edit. The **staging area (index)** holds changes selected for the next commit via `git add`. The **repository** stores committed snapshots as objects via `git commit`. Changes flow: edit files (working dir) → `git add` (stage) → `git commit` (persist). `git checkout` or `git restore` can move data from repository/index back to working directory.

    **Q5 — push -u:** Pushes local branch `feature/x` to remote `origin` and sets upstream tracking. Future `git push` and `git pull` without arguments use this remote branch. Required once for new branches; subsequent pushes need only `git push`.

    **Q8 — Commits and CI/CD:** Hosting platforms fire webhooks on push events. CI systems clone at the pushed commit SHA, run defined stages (test, build, scan, deploy), and report status back to the PR or commit. On merge to protected `main`, deployment pipelines promote artifacts tagged with that SHA — enabling traceability from production back to exact source state.

## Related Tutorials

- [Git – Category Overview](index.md)
- [Creating and Cloning Repositories](creating-and-cloning-repositories.md) *(previous in Module 2)*
- [Viewing History and Diffs](viewing-history-and-diffs.md) *(next in Module 2)*
- [Understanding the Git Object Model](understanding-the-git-object-model.md)
- [Introduction to Networking](../networking/introduction-to-networking.md)

## References

- [Pro Git – Recording Changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)
- [Conventional Commits specification](https://www.conventionalcommits.org/)
- [Git push documentation](https://git-scm.com/docs/git-push)
- [GitHub Actions – Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
- [GitLab CI – Pipeline triggers](https://docs.gitlab.com/ee/ci/pipelines/)
- [REBASH Academy – Networking Overview](../networking/index.md)
