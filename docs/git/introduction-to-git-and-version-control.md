---
title: Introduction to Git and Version Control
description: Understand why version control matters for DevOps, distributed vs centralized VCS, Git's role in IaC and CI/CD, and core terminology for production workflows.
difficulty: beginner
estimated_time: "30 min"
author: Shaik Basha
category: git
tags:
  - git
  - version-control
  - fundamentals
  - devops
  - vcs
prerequisites:
  - Basic computer literacy and comfort using a terminal
  - Completion of or concurrent study of the Linux Foundations track
  - Network access for later tutorials that clone remote repositories
comments: false
---

# Introduction to Git and Version Control

## Overview

Every production deployment, Terraform apply, Kubernetes manifest change, and CI/CD pipeline run depends on **version control**. When an incident postmortem asks "what changed between the last good deploy and the failure?", the answer lives in Git history. When a compliance auditor asks "who approved this infrastructure change and when?", Git blame and signed commits provide the trail. Version control is not a developer-only tool — it is the **system of record** for modern DevOps.

This tutorial establishes your mental model: what **version control** solves, how **distributed** systems like Git differ from legacy **centralized** tools, why Git became the industry standard, and the core vocabulary — repository, commit, branch, remote — you will use daily in infrastructure-as-code, GitOps, and application pipelines.

This is **Tutorial 1** in **Module 1: Foundations** of the REBASH Academy Git series. We recommend completing the [Linux Foundations track](../linux/index.md) first, since all hands-on labs assume a Linux shell. Basic [networking concepts](../networking/index.md) become relevant when you push to remotes in later tutorials. This tutorial follows our [documentation standards](../about.md#documentation-standards).

## Prerequisites

- Basic computer literacy and comfort typing commands in a terminal
- A Linux environment: Ubuntu VM, WSL2, or a free-tier cloud instance (AWS, GCP, Azure)
- Familiarity with the [Introduction to Linux](../linux/introduction-to-linux.md) tutorial — especially navigating directories and running basic CLI commands
- No prior Git experience required — this tutorial starts from zero

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain why version control is essential for DevOps, SRE, and platform engineering roles
- [ ] Describe the problems VCS solves: history, collaboration, rollback, and auditability
- [ ] Compare centralized (SVN, Perforce) and distributed (Git) version control architectures
- [ ] Define repository, commit, branch, merge, remote, and working directory in production context
- [ ] Articulate why Git dominates cloud-native tooling, IaC, and CI/CD pipelines
- [ ] Identify Git's role in GitOps, infrastructure-as-code, and configuration management workflows
- [ ] Recognize common Git hosting platforms and their place in enterprise DevOps stacks

## Architecture Diagram

The diagram below contrasts centralized and distributed version control. Understanding this distinction explains why Git works offline, why every clone is a full backup, and why CI runners only need network access during push/pull — not for every local commit.

```d2
direction: down

CVCS: "Centralized VCS (e.g., SVN)" {
      style: {
        fill: "#e3f2fd"
        stroke: "#1976d2"
      }
        SVN_SRV: "Central Server\\nsingle source of truth"
        DEV_A: "Developer A\\nworking copy only"
        DEV_B: "Developer B\\nworking copy only"
        DEV_A -> SVN_SRV: "commit / update"
        DEV_B -> SVN_SRV: "commit / update"
    }
    DVCS: "Distributed VCS (Git)" {
      style: {
        fill: "#e8f5e9"
        stroke: "#388e3c"
      }
        REMOTE: "Remote — GitHub / GitLab / Bitbucket"
        DEV_C: "Developer C\\nfull local repo"
        DEV_D: "Developer D\\nfull local repo"
        CI: "CI Runner\\nfull clone"
        DEV_C <-> REMOTE: "push / pull"
        DEV_D <-> REMOTE: "push / pull"
        CI <-> REMOTE: "fetch / clone"
        DEV_C -> DEV_C: "local commits\\nno network" {
          style.stroke-dash: 3
        }
    }
```

## Theory

### Why Version Control Matters for DevOps

Before Git, teams copied folders named `app_v2_final_FINAL`. Rollbacks meant restoring from tape backups. Auditors received spreadsheets, not cryptographic proof of who changed what. Version control replaces chaos with a **directed acyclic graph (DAG)** of changes — every modification tracked, attributable, and reversible.

DevOps engineers rely on version control to:

- **Manage infrastructure-as-code** — Terraform modules, Ansible playbooks, Helm charts, and Kubernetes manifests live in Git repositories
- **Enable GitOps** — Argo CD and Flux reconcile cluster state against a Git branch; the repo is the desired-state source of truth
- **Trigger CI/CD pipelines** — push events, pull requests, and tags start builds, tests, security scans, and deployments
- **Support incident response** — `git log`, `git diff`, and `git bisect` identify which commit introduced a regression
- **Meet compliance requirements** — change history, code review records, and signed commits satisfy SOC 2, PCI-DSS, and internal audit trails
- **Collaborate at scale** — branching strategies (trunk-based, GitFlow) coordinate hundreds of engineers without overwriting each other's work

If you deploy anything to production, you need version control. Git is the tool you will encounter in 95% of organizations.

### The Problem Version Control Solves

| Problem without VCS | How Git solves it |
|---------------------|-------------------|
| "Which file is the latest?" | One repository; commits form an ordered history with unique IDs |
| "Who broke production?" | `git blame` and `git log` show author, timestamp, and commit message |
| "We need to roll back" | Checkout a previous commit or tag; revert creates an inverse commit |
| "Two people edited the same file" | Branches isolate work; merge combines changes with conflict markers |
| "We lost the server" | Every clone is a complete backup with full history |
| "What changed in this release?" | `git diff v1.0..v2.0` shows exact file changes between tags |

### Centralized vs Distributed Version Control

**Centralized VCS (CVCS)** — Subversion (SVN), CVS, Perforce — stores the authoritative history on a single server. Clients hold **working copies**: the latest snapshot plus a small metadata cache. Committing requires network access to the server. If the server dies and backups fail, history may be lost.

**Distributed VCS (DVCS)** — Git, Mercurial — gives every user a **full local repository** with complete history. Commits happen locally first; you **push** to share and **pull** to synchronize. You can commit on an airplane, experiment in branches, and push when connected. The remote (GitHub, GitLab, self-hosted Gitea) is a **convenience for collaboration**, not the sole custodian of history.

For DevOps, distribution matters because:

- CI runners clone the full repo and can run deep history analysis
- Edge deployments and air-gapped environments can sync periodically
- Developers can rebase and rewrite local history before sharing (with team agreement)
- Disaster recovery is simpler: any team member's laptop may hold the only copy that saves the project

### A Brief History of Git

**Git** was created by **Linus Torvalds** in 2005 to manage Linux kernel development after a licensing dispute ended access to BitKeeper. Design goals: speed, strong integrity (SHA-1 hashing), and support for distributed workflows with thousands of contributors.

Key milestones for DevOps practitioners:

| Year | Event | DevOps relevance |
|------|-------|------------------|
| 2005 | Git 0.99 released | Distributed model proven at kernel scale |
| 2008 | GitHub launches | Pull requests, code review, social coding |
| 2010 | Git becomes dominant VCS | Default for new projects |
| 2014 | Docker + GitHub | Container images built from Git repos |
| 2016+ | GitOps emerges | Kubernetes state driven from Git |
| 2020+ | Platform engineering | Internal developer portals integrate with Git APIs |

Today Git is bundled with Xcode, pre-installed on most Linux distros, and embedded in every major DevOps platform.

### Core Terminology

#### Repository (Repo)

A **repository** is a directory (project folder) plus Git's hidden metadata in `.git/`. It contains every commit, branch, and tag. In production, repos are organized by team or service: `infra/terraform-modules`, `platform/k8s-manifests`, `app/payment-service`.

#### Working Directory, Staging Area, and Repository

Git manages three trees:

| Tree | Location | Purpose |
|------|----------|---------|
| **Working directory** | Your project files | Where you edit code and configs |
| **Staging area (index)** | `.git/index` | Prepared snapshot for the next commit |
| **Repository** | `.git/objects` | Permanent, hashed object store |

This three-stage model lets you craft precise commits — essential when a single file contains both a bug fix and an unrelated formatting change.

#### Commit

A **commit** is a snapshot of the project at a point in time, identified by a **40-character SHA-1 hash** (e.g., `a1b2c3d4...`). Each commit points to its parent(s), forming history. Commits include author, committer, timestamp, and message. In CI/CD, commit SHAs pin exact artifact versions: `myapp:sha-a1b2c3d4`.

#### Branch

A **branch** is a movable pointer to a commit. The default branch is traditionally `master` or `main`. Feature branches isolate work: `feature/add-waf-rules`, `fix/iam-policy-drift`. Trunk-based development keeps `main` always deployable; long-lived branches accumulate merge debt.

#### Merge

**Merging** combines two branch histories. A merge commit has two parents. Conflicts occur when the same lines changed differently — Git marks them for manual resolution.

#### Remote

A **remote** is a named reference to another repository, typically `origin` pointing to GitHub or GitLab. `git push origin main` uploads local commits; `git pull` fetches and integrates remote changes.

#### Tag

A **tag** marks a specific commit — usually a release: `v1.4.2`, `prod-2026-07-27`. Immutable tags anchor deployments and Docker image tags.

### Git in the DevOps Toolchain

```d2
direction: right

DEV: "Developer / Engineer"
    GIT: "Git Repository"
    PR: "Pull Request / MR"
    CI: "CI Pipeline\\nGitHub Actions / GitLab CI"
    CD: "CD / GitOps\\nArgo CD / Flux"
    PROD: Production
    DEV -> GIT: "commit / push"
    GIT -> PR
    PR -> CI: trigger
    CI -> GIT: "pass + merge"
    GIT -> CD: sync
    CD -> PROD
```

Every arrow depends on Git. Terraform Cloud reads VCS webhooks. Ansible Tower pulls playbooks from Git. Kubernetes operators watch Git branches. Learning Git is prerequisite to every other DevOps skill in this academy.

### Git Hosting Platforms

| Platform | Common use | DevOps integration |
|----------|------------|-------------------|
| **GitHub** | Open source, startups, GitHub Actions | Largest Actions marketplace |
| **GitLab** | Self-hosted enterprise, built-in CI/CD | Single platform for repo + pipeline |
| **Bitbucket** | Atlassian stack (Jira, Bamboo) | Tight Jira integration |
| **AWS CodeCommit** | AWS-native shops | IAM-based access, CodePipeline triggers |
| **Azure DevOps Repos** | Microsoft ecosystem | Azure Pipelines native |
| **Gitea / Forgejo** | Self-hosted lightweight | Air-gapped, on-premises |

The Git **protocol and object model are identical** across platforms. Skills transfer; only authentication and UI differ.

## Hands-on Lab

These steps verify Git availability and explore a repository's structure. If Git is not installed, complete [Git Installation and Configuration](git-installation-and-configuration.md) first.

### Step 1 – Confirm Git is available

**Command:**

```bash
git --version
which git
```

**Explanation:** Confirms Git is installed and shows the binary path. Production servers, CI images, and developer laptops should pin minimum versions in documentation.

**Expected output:**

```text
git version 2.43.0
/usr/bin/git
```

### Step 2 – View built-in help and documentation

**Command:**

```bash
git help
git help glossary
```

**Explanation:** Git ships extensive documentation. `git help glossary` defines terms used throughout this track. In air-gapped environments, local man pages replace web searches.

**Expected output:**

```text
Available git commands in '/usr/lib/git-core':
...
```

### Step 3 – Clone a public repository (read-only exploration)

**Command:**

```bash
cd /tmp
git clone --depth 1 https://github.com/git/git.git git-explore
cd git-explore
ls -la
```

**Explanation:** `--depth 1` creates a **shallow clone** with only the latest commit — common in CI for speed. The `.git` directory holds all metadata; visible files are the **working directory** at HEAD.

**Expected output:**

```text
Cloning into 'git-explore'...
total ...
drwxr-xr-x  ... .git
-rw-r--r--  ... README.md
...
```

### Step 4 – Inspect the `.git` directory structure

**Command:**

```bash
ls -la .git/
ls .git/objects/ | head -5
cat .git/HEAD
```

**Explanation:** `.git/` is the repository database. `objects/` stores commits, trees, and blobs (covered in [Understanding the Git Object Model](understanding-the-git-object-model.md)). `HEAD` points to the current branch.

**Expected output:**

```text
HEAD
config
description
hooks
index
info
logs
objects
refs
...
ref: refs/heads/master
```

### Step 5 – View recent commit history

**Command:**

```bash
git log --oneline -5
git log -1 --format=fuller
```

**Explanation:** `git log` traverses the commit DAG. `--format=fuller` shows author vs committer (relevant when cherry-picking or applying patches from email).

**Expected output:**

```text
a1b2c3d Merge branch '...
d4e5f6a Fix receive-pack bug ...
...
```

### Step 6 – Identify remotes and default branch

**Command:**

```bash
git remote -v
git branch -a
```

**Explanation:** Remotes define where pushes and pulls go. Branch `-a` lists local and remote-tracking branches — the model CI systems use to checkout PR head refs.

**Expected output:**

```text
origin  https://github.com/git/git.git (fetch)
origin  https://github.com/git/git.git (push)
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
```

### Step 7 – Clean up the lab clone

**Command:**

```bash
cd /tmp
rm -rf git-explore
```

**Explanation:** Remove temporary clones after exploration. Never store credentials in world-readable `/tmp` directories.

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `git --version` | Show installed Git version | `git --version` |
| `git help <cmd>` | Display manual for a command | `git help commit` |
| `git clone` | Copy a remote repository locally | `git clone URL repo-name` |
| `git log` | Show commit history | `git log --oneline -10` |
| `git remote -v` | List configured remotes | `git remote -v` |
| `git branch -a` | List all branches | `git branch -a` |
| `git status` | Show working tree state | `git status` |
| `git rev-parse HEAD` | Print current commit SHA | `git rev-parse --short HEAD` |

### Environment check script for CI/CD

Save as `~/bin/git-preflight.sh` — run at the start of pipelines or onboarding docs:

```bash
#!/usr/bin/env bash
# git-preflight.sh — verify Git is ready for DevOps workflows
set -euo pipefail

section() { printf '\n=== %s ===\n' "$1"; }

section "Git Version"
if command -v git >/dev/null 2>&1; then
  git --version
else
  echo "ERROR: git not found in PATH"
  exit 1
fi

section "User Identity (required for commits)"
NAME=$(git config --global user.name 2>/dev/null || echo "")
EMAIL=$(git config --global user.email 2>/dev/null || echo "")
if [ -z "$NAME" ] || [ -z "$EMAIL" ]; then
  echo "WARNING: user.name or user.email not configured globally"
  echo "  Set with: git config --global user.name 'Your Name'"
  echo "            git config --global user.email 'you@example.com'"
else
  echo "Name:  $NAME"
  echo "Email: $EMAIL"
fi

section "Default Branch Name"
INIT_BRANCH=$(git config --global init.defaultBranch 2>/dev/null || echo "not set")
echo "init.defaultBranch: $INIT_BRANCH"

section "Credential Helper"
git config --global credential.helper 2>/dev/null || echo "No credential helper configured"

section "Network Reachability (optional)"
if curl -s --max-time 5 -o /dev/null -w '' https://github.com; then
  echo "HTTPS to github.com: OK"
else
  echo "HTTPS to github.com: FAIL (check proxy/firewall — see Networking track)"
fi
```

Make executable: `chmod +x ~/bin/git-preflight.sh && ~/bin/git-preflight.sh`

## Common Mistakes

!!! warning "Treating Git as 'save' instead of 'commit with intent'"
    Copying files or running `git add .` without reviewing changes produces noisy history that breaks `git bisect` and code review. Stage deliberately; write commit messages that explain **why**, not just **what**.

!!! warning "Assuming the remote is the only backup"
    Git is distributed — but if only one person pushes and their laptop dies before push, work is lost. Push frequently; protect default branches with branch rules.

!!! warning "Using Git without understanding the three trees"
    Editing files does not create a commit. Changes must move from working directory → staging area → repository. Confusion here causes "I committed but the file isn't in the repo" support tickets.

!!! warning "Ignoring `.git` in backups and migration"
    Copying project folders without `.git/` loses all history. For repo migration, use `git clone --mirror` or platform import tools — not `rsync` of working files alone.

## Best Practices

!!! tip "Treat Git as the system of record for all production config"
    Application code, Terraform, Helm charts, and runbooks belong in Git — not shared drives or Slack attachments. If it runs in prod, it should be versioned.

!!! tip "Learn Linux terminal skills alongside Git"
    Git is a CLI-first tool. File permissions, SSH keys, and path navigation from the [Linux track](../linux/index.md) directly accelerate Git proficiency.

!!! tip "Standardize on `main` as the default branch"
    New repositories should use `main`. Configure `git config --global init.defaultBranch main` and set branch protection on hosting platforms.

!!! tip "Understand networking before debugging push failures"
    Clone and push require HTTPS or SSH connectivity. TLS errors, proxy settings, and DNS issues are networking problems — see the [Networking track](../networking/index.md).

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `git: command not found` | Git not installed or not in PATH | Install Git; verify with `which git` |
| `fatal: not a git repository` | Command run outside a repo | `cd` into repo root or run `git init` |
| Clone hangs or times out | Network, firewall, or proxy blocking HTTPS/SSH | Test with `curl -v https://github.com`; configure `http.proxy` |
| Empty `git log` after clone | Shallow clone or orphan branch | Use full clone or `git fetch --unshallow` |
| `Permission denied (publickey)` | SSH key not configured for host | Generate SSH key; add to GitHub/GitLab; test with `ssh -T git@github.com` |
| Wrong author on commits | `user.name` / `user.email` not set | Configure globally or per-repo — see next tutorial |
| `.git` directory missing after copy | Copied files without metadata | Re-clone from remote or restore from backup |

## Summary

- **Version control** tracks every change with history, authorship, and rollback capability — essential for DevOps auditability and collaboration
- **Centralized VCS** depends on a single server; **distributed VCS (Git)** gives every clone a full history and enables offline work
- Core concepts: **repository**, **working directory**, **staging area**, **commit**, **branch**, **merge**, **remote**, and **tag**
- Git powers **CI/CD**, **GitOps**, and **infrastructure-as-code** — it is step 3 in the DevOps learning path after Linux and networking
- Hosting platforms (GitHub, GitLab, etc.) share the same Git protocol; skills transfer across organizations

## Interview Questions

1. Why is version control critical for DevOps and platform engineering?
2. What is the difference between centralized and distributed version control?
3. Explain the three trees in Git: working directory, staging area, and repository.
4. What is a commit, and how is it identified?
5. Why did Git become the dominant version control system?
6. How does Git integrate with CI/CD pipelines?
7. What is GitOps, and what role does Git play?
8. What is the difference between a branch and a tag?
9. Name three Git hosting platforms and one DevOps integration for each.
10. What happens if you copy project files but not the `.git` directory?

??? tip "Sample Answers (Questions 2, 6, and 7)"

    **Q2 — Centralized vs distributed:** Centralized VCS (e.g., SVN) stores the canonical history on one server; clients hold working copies and need network access to commit. Distributed VCS (Git) replicates the full repository to every clone. Commits are local first; push/pull synchronizes with remotes. Distribution enables offline work, faster local operations, and inherent backup across clones.

    **Q6 — Git and CI/CD:** CI systems watch Git events — push, pull request, tag — via webhooks or polling. On trigger, the runner clones the repo at a specific commit SHA, runs build/test/deploy stages, and may push artifacts or update deployment status. Commit SHA pins the exact code under test, enabling reproducible builds and traceability from production back to source.

    **Q7 — GitOps:** GitOps treats a Git repository as the single source of truth for desired infrastructure or application state. Operators like Argo CD or Flux continuously compare live cluster state against the Git branch and reconcile differences. Git provides audit history, review via pull requests, and rollback by reverting or checking out a previous commit.

## Related Tutorials

- [Git – Category Overview](index.md)
- [Introduction to Linux](../linux/introduction-to-linux.md) — recommended prerequisite
- [Introduction to Networking](../networking/introduction-to-networking.md) — connectivity for remotes
- [Git Installation and Configuration](git-installation-and-configuration.md) *(next in Module 1)*
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [Pro Git Book (free online)](https://git-scm.com/book/en/v2) — chapters 1–2
- [Git official documentation](https://git-scm.com/doc)
- [Git glossary](https://git-scm.com/docs/gitglossary)
- [CNCF GitOps Working Group](https://opengitops.dev/)
- [Atlassian Git tutorials](https://www.atlassian.com/git/tutorials)
- [REBASH Academy – Linux Overview](../linux/index.md)
- [REBASH Academy – Networking Overview](../networking/index.md)
