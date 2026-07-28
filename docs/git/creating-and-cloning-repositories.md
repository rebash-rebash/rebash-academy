---
title: Creating and Cloning Repositories
description: Initialize local repos, clone from remotes, understand bare vs non-bare repositories, mirror clones, and DevOps patterns for IaC and CI/CD project setup.
difficulty: beginner
estimated_time: "30 min"
author: Shaik Basha
category: git
tags:
  - git
  - clone
  - init
  - repository
  - remote
  - devops
prerequisites:
  - Module 1 Git Foundations tutorials (1–3)
  - Git installed and configured with user identity
  - Network access for cloning remote repositories
comments: false
---

# Creating and Cloning Repositories

## Overview

Every Terraform module, Helm chart collection, Ansible role, and microservice starts as a **Git repository**. Platform teams create hundreds of repos from golden templates; CI runners **clone** them on every pipeline run; disaster recovery **mirrors** them to secondary hosts. Knowing when to `git init` locally versus `git clone` from a remote — and the difference between **bare** and **non-bare** repositories — prevents the most common onboarding mistakes in DevOps organizations.

This tutorial covers creating repositories from scratch, cloning with depth and branch options, configuring remotes, using bare repos for server-side Git hosting, and production patterns for infrastructure-as-code bootstrap and CI workspace setup.

This is **Tutorial 4** in **Module 2: Essential Workflow** of the REBASH Academy Git series. Complete Module 1 first. SSH/HTTPS connectivity depends on [Networking fundamentals](../networking/index.md); file operations assume [Linux CLI skills](../linux/index.md).

## Prerequisites

- [Introduction to Git and Version Control](introduction-to-git-and-version-control.md)
- [Git Installation and Configuration](git-installation-and-configuration.md)
- [Understanding the Git Object Model](understanding-the-git-object-model.md)
- Git configured with `user.name` and `user.email`
- SSH key or HTTPS credentials for GitHub/GitLab (for remote clone steps)
- Network access to a Git hosting provider

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Initialize a new repository with `git init` and understand what `.git/` contains
- [ ] Clone repositories using HTTPS and SSH URLs with appropriate options
- [ ] Differentiate bare and non-bare repositories and when each is used
- [ ] Add, rename, and remove remotes; understand `origin` conventions
- [ ] Create mirror clones for backup and migration scenarios
- [ ] Use shallow and single-branch clones to optimize CI performance
- [ ] Bootstrap an infrastructure-as-code repository with sensible initial structure
- [ ] Troubleshoot common clone and permission failures in enterprise environments

## Architecture Diagram

DevOps workflows typically flow from a hosted remote to local clones and CI runners. Bare repositories on servers act as intermediaries in self-hosted Git deployments.

```d2
direction: down

HOSTING: "Git Hosting Platform" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        REMOTE: "origin\nGitHub / GitLab / Gitea"
    }
    DEV: "Developer Workstations" {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        CLONE1: "non-bare clone\nworking directory + .git"
        CLONE2: "non-bare clone"
    }
    CI: "CI/CD Infrastructure" {
      style: {
        fill: "#ffedd5"
        stroke: "#ea580c"
      }
        RUNNER: "Pipeline runner\nshallow clone depth=1"
    }
    SELF: "Self-Hosted (optional)" {
      style: {
        fill: "#f3e8ff"
        stroke: "#9333ea"
      }
        BARE: "bare repo on server\n/srv/git/project.git"
    }
    HOSTING.REMOTE <-> DEV.CLONE1: "push / fetch"
    HOSTING.REMOTE <-> DEV.CLONE2: "push / fetch"
    HOSTING.REMOTE -> CI.RUNNER: "webhook trigger"
    CI.RUNNER -> HOSTING.REMOTE: "clone / fetch"
    SELF.BARE <-> HOSTING.REMOTE: "push mirror"
```

## Theory

### Creating a Repository: `git init`

`git init` creates a new `.git/` subdirectory in the current folder, initializing an empty object database and default branch (usually `main` if `init.defaultBranch` is set).

```bash
mkdir my-terraform-module && cd my-terraform-module
git init
```

What happens:

1. `.git/HEAD` points to `refs/heads/main` (or `master` on older defaults)
2. `.git/objects/` and `.git/refs/` are created empty
3. No commits exist yet — first commit requires staged files

Use `git init` when starting a greenfield project locally before pushing to a hosting platform. Many teams create the empty repo on GitHub first, then clone — both paths converge.

**`git init --bare`** creates a repository **without a working directory** — only `.git` contents at the root. Used for:

- Central repos on self-hosted Git servers (`/srv/git/infra.git`)
- Server-side push targets
- Mirror destinations

Never run `git init --bare` in a directory where you also edit files — you cannot commit from a bare repo's directory directly.

### Cloning: `git clone`

`git clone URL [directory]` copies an entire repository (or a subset) to a new location:

1. Creates directory
2. Initializes `.git/`
3. Fetches objects from remote
4. Checks out default branch into working directory
5. Sets `origin` remote automatically

| URL format | Example | Auth |
|------------|---------|------|
| HTTPS | `https://github.com/org/repo.git` | PAT, OAuth, credential helper |
| SSH | `git@github.com:org/repo.git` | SSH key |
| Git protocol | `git://github.com/org/repo.git` | Rare; often blocked |
| Local file | `/srv/git/repo.git` or `file:///srv/git/repo.git` | Filesystem permissions |

### Bare vs Non-Bare Repositories

| Aspect | Non-bare (default) | Bare |
|--------|-------------------|------|
| Working directory | Yes — editable files | No — `.git` data only |
| `git status` | Works | Not applicable |
| Typical location | Developer laptop, CI workspace | Git server, mirror target |
| Clone target | Yes | Yes |
| Push target | Yes (discouraged for non-bare unless receiving work) | Yes (standard for servers) |

When you `git push` to a bare repo on a server, hooks can trigger CI (e.g., post-receive deploy to staging). This pattern predates GitHub Actions but remains in air-gapped environments.

### Remotes

A **remote** is a named bookmark for another repository URL. Default name: **`origin`** (the clone source).

```bash
git remote -v
git remote add upstream https://github.com/original/project.git
git remote rename origin old-origin
git remote remove upstream
```

DevOps patterns:

- **origin** — your fork or primary repo
- **upstream** — open-source original you sync from
- **deploy** — bare repo on deployment server (legacy push-to-deploy)

`git remote set-url origin NEW_URL` migrates from HTTPS to SSH without recloning.

### Clone Options for DevOps

| Option | Purpose | Example |
|--------|---------|---------|
| `--depth N` | Shallow clone — last N commits | `git clone --depth 1 URL` |
| `--branch BR` | Clone specific branch only | `git clone --branch release-2.0 URL` |
| `--single-branch` | Fetch one branch ref | Combined with `--branch` |
| `--mirror` | Full mirror for backup/migration | `git clone --mirror URL` |
| `--recurse-submodules` | Initialize submodules | Monorepos with embedded deps |
| `--filter=blob:none` | Partial clone (Git 2.19+) | Huge repos, lazy blob fetch |

CI pipelines almost always use `--depth 1` for speed. Release engineering uses full or mirror clones for backups.

### Mirror Clones

`git clone --mirror` creates a bare repo with all refs (branches, tags, notes) — exact replica for:

- Migrating GitLab → GitHub
- Air-gapped replica sync
- Disaster recovery cold standby

Update mirror: `cd repo.git && git remote update --prune`

Push mirror to new host: `git push --mirror new-origin`

### Bootstrap Patterns for IaC Repositories

Standard initial structure for Terraform/Kubernetes repos:

```text
infra-platform/
├── .gitignore
├── README.md
├── Makefile
├── terraform/
│   ├── environments/
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   └── modules/
├── .github/
│   └── workflows/
│       └── terraform-plan.yml
└── docs/
    └── runbooks/
```

First commit should include `.gitignore` **before** any secrets accidentally land — Terraform `.tfstate` files and `.env` must never be committed.

### Hosting Platform Repository Creation

Modern workflow:

1. Create empty repo on GitHub/GitLab (with README/license optional)
2. Clone locally OR connect local `git init` repo via `git remote add origin URL`
3. Push initial commit: `git push -u origin main`

The `-u` flag sets upstream tracking — future `git push` and `git pull` know which remote branch to use.

## Hands-on Lab

Complete these steps on your Linux lab machine. Replace URLs with your own test repository when pushing.

### Step 1 – Create a repository from scratch

**Command:**

```bash
mkdir -p ~/lab/infra-bootstrap && cd ~/lab/infra-bootstrap
git init
git status
ls -la
```

**Explanation:** Empty repo — `git status` reports "No commits yet on main". No `.git` visible in `ls` listing but it exists as hidden directory.

**Expected output:**

```text
Initialized empty Git repository in .../infra-bootstrap/.git/
On branch main
No commits yet
nothing to commit
```

### Step 2 – Add initial IaC-style files

**Command:**

```bash
cat > .gitignore << 'EOF'
*.tfstate
*.tfstate.*
.terraform/
.env
*.pem
EOF

cat > README.md << 'EOF'
# Infra Bootstrap

Terraform modules for REBASH Academy lab environment.
EOF

mkdir -p terraform/environments/dev
echo 'instance_type = "t3.micro"' > terraform/environments/dev/terraform.tfvars.example
git status
```

**Explanation:** Always create `.gitignore` before first commit. The `.example` suffix documents expected variables without secrets.

**Expected output:**

```text
Untracked files:
  .gitignore
  README.md
  terraform/
```

### Step 3 – Create the initial commit

**Command:**

```bash
git add .
git commit -m "Initial commit: bootstrap IaC repository structure"
git log --oneline
git rev-parse HEAD
```

**Explanation:** First commit creates root tree and establishes `main` branch history. Record SHA — it becomes the baseline for all future work.

**Expected output:**

```text
abc1234 Initial commit: bootstrap IaC repository structure
abc1234def5678...
```

### Step 4 – Clone a public repository (HTTPS, shallow)

**Command:**

```bash
cd ~/lab
git clone --depth 1 --branch master https://github.com/git/git.git git-shallow-clone
cd git-shallow-clone
git log --oneline | wc -l
git remote -v
```

**Explanation:** Shallow clone fetches minimal history — typical CI pattern. `--branch` selects default branch name on upstream (git project uses `master`).

**Expected output:**

```text
Cloning into 'git-shallow-clone'...
1
origin  https://github.com/git/git.git (fetch)
origin  https://github.com/git/git.git (push)
```

### Step 5 – Add a second remote and inspect

**Command:**

```bash
git remote add backup https://github.com/octocat/Hello-World.git
git remote -v
git remote show origin 2>/dev/null | head -10
```

**Explanation:** Multiple remotes support mirror workflows. `git remote show` lists tracked branches and fetch/push URLs.

**Expected output:**

```text
backup  https://github.com/octocat/Hello-World.git (fetch)
backup  https://github.com/octocat/Hello-World.git (push)
origin  https://github.com/octocat/Hello-World.git (fetch)
origin  https://github.com/octocat/Hello-World.git (push)
```

### Step 6 – Simulate bare repository setup

**Command:**

```bash
cd ~/lab
git clone --bare hello-world hello-world.git
ls hello-world.git/
git --git-dir=hello-world.git log --oneline -3
```

**Explanation:** Bare repo ends in `.git` convention (`repo.git`). No working files — only object database. Server-side Git hosting uses this layout.

**Expected output:**

```text
HEAD  branches  config  description  hooks  info  objects  refs
...
```

### Step 7 – Clean up lab directories

**Command:**

```bash
rm -rf ~/lab/git-shallow-clone ~/lab/hello-world ~/lab/hello-world.git ~/lab/infra-bootstrap
```

**Explanation:** Remove practice repos. Never delete unpushed work — verify with `git log origin/main..main` before cleanup in real projects.

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `git init` | Create new repository | `git init` |
| `git init --bare` | Create bare repository | `git init --bare repo.git` |
| `git clone URL` | Clone remote repository | `git clone git@github.com:org/repo.git` |
| `git clone --depth 1` | Shallow clone | `git clone --depth 1 URL` |
| `git clone --mirror` | Mirror clone for backup | `git clone --mirror URL` |
| `git remote add` | Add remote | `git remote add origin URL` |
| `git remote -v` | List remotes | `git remote -v` |
| `git push -u origin main` | Push and set upstream | `git push -u origin main` |

### Connect local init to new GitHub repo

After creating empty repo on GitHub:

```bash
cd my-project
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:ORG/my-project.git
git push -u origin main
```

## Common Mistakes

!!! warning "Committing secrets in the first commit"
    `.gitignore` must exist **before** `git add .`. Terraform state, kubeconfig, and `.env` files in initial commits require history rewriting to remove — painful and visible in forks.

!!! warning "Cloning into an non-empty directory"
    `git clone` requires empty or non-existent target directory. Use `git init` + `git remote add` + `git pull` to adopt existing files.

!!! warning "Using non-bare repo as server push target"
    Pushing to a checked-out branch on a non-bare server repo causes working directory desync. Use `--bare` or hosting platform APIs.

!!! warning "Shallow clone then expecting full history commands"
    `git log` beyond depth, `git bisect`, and some merges fail on shallow repos. Run `git fetch --unshallow` when full history is needed.

## Best Practices

!!! tip "Create repos from organizational templates"
    GitHub/GitLab template repos include `.gitignore`, CI skeleton, CODEOWNERS, and branch protection defaults — enforce consistency across hundreds of microservices.

!!! tip "Use SSH for developer clones, scoped tokens for CI"
    Developers use SSH keys. CI uses fine-grained PATs or OIDC with minimal permissions — read for build, write only for release bots.

!!! tip "Document clone URL and branch strategy in README"
    Every internal repo README should state: canonical URL, default branch, whether to use `--recurse-submodules`, and required Git version.

!!! tip "Verify network path before blaming Git"
    Clone failures are often DNS, proxy, or firewall issues — use [Networking troubleshooting](../networking/introduction-to-networking.md#troubleshooting) patterns.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `fatal: destination path already exists` | Target directory not empty | Remove directory or choose new name |
| `Repository not found` | Wrong URL, no access, or private repo | Verify URL spelling; check auth; confirm org membership |
| `Permission denied (publickey)` | SSH key not configured | See [Git Installation and Configuration](git-installation-and-configuration.md) |
| `fatal: refusing to merge unrelated histories` | Local init + remote with commits | `git pull origin main --allow-unrelated-histories` (once, carefully) |
| Clone extremely slow | Large repo or no shallow depth | Use `--depth 1`, partial clone, or Git LFS |
| `error: RPC failed; HTTP 413` | Push too large for HTTP buffer | Increase `http.postBuffer`; use SSH; split commits |
| Bare repo push updates no files | Expected — bare has no working tree | Clone from bare to inspect; bare is object store only |
| Wrong default branch after clone | Remote uses `master` vs `main` | `git branch -a`; checkout correct branch |

## Summary

- **`git init`** creates a new repo locally; **`git clone`** copies an existing remote repository with `origin` preconfigured
- **Bare repositories** have no working directory — used for servers, mirrors, and push targets; **non-bare** repos are for daily development
- **Shallow clones** (`--depth 1`) optimize CI; **mirror clones** preserve all refs for backup and migration
- Bootstrap IaC repos with `.gitignore`, README, and directory structure **before** the first commit
- **Remotes** name collaboration endpoints; `git push -u origin main` establishes upstream tracking
- Clone failures are often authentication or networking issues — verify SSH, PAT, and connectivity first

## Interview Questions

1. What is the difference between `git init` and `git clone`?
2. Explain bare vs non-bare repositories and when to use each.
3. What does `git clone --depth 1` do, and why is it common in CI?
4. What is a mirror clone, and when would you use one?
5. What is the purpose of the `origin` remote?
6. How do you connect a locally initialized repo to a new GitHub repository?
7. What files should be in `.gitignore` before an IaC repository's first commit?
8. What does `git push -u origin main` accomplish beyond a regular push?
9. Why should you not push directly to a non-bare repository on a server?
10. How would you migrate a repository from GitLab to GitHub preserving all branches and tags?

??? tip "Sample Answers (Questions 2, 3, and 10)"

    **Q2 — Bare vs non-bare:** A non-bare repository has a working directory where you edit files and a `.git/` metadata directory. A bare repository contains only Git object data (like `.git` contents) with no checked-out files. Bare repos serve as central push targets on self-hosted Git servers and mirror destinations. Non-bare repos are for developers and CI workspaces where you read and modify files.

    **Q3 — Shallow clone:** `--depth 1` fetches only the most recent commit (per branch), omitting full history. CI pipelines use it to minimize network transfer and disk usage since builds typically need only the latest source snapshot. Tradeoff: history-dependent operations (`git bisect`, full log, some merges) require `git fetch --unshallow`.

    **Q10 — GitLab to GitHub migration:** Run `git clone --mirror git@gitlab.com:org/repo.git` to get a bare mirror with all refs. Create empty repo on GitHub. Push with `git push --mirror git@github.com:org/repo.git`. Verify branches and tags. Update CI webhooks, deploy keys, and team remote URLs. `--mirror` ensures tags and all branch refs transfer completely.

## Related Tutorials

- [Git – Category Overview](index.md)
- [Understanding the Git Object Model](understanding-the-git-object-model.md) *(previous — Module 1)*
- [Basic Git Workflow — Add, Commit, Push](basic-git-workflow-add-commit-push.md) *(next in Module 2)*
- [Git Installation and Configuration](git-installation-and-configuration.md)
- [Introduction to Networking](../networking/introduction-to-networking.md)

## References

- [Pro Git – Getting a Git Repository](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)
- [Git clone documentation](https://git-scm.com/docs/git-clone)
- [GitHub – Creating a new repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [GitLab – Create a project](https://docs.gitlab.com/ee/user/project/index.html)
- [Partial clone (filter)](https://git-scm.com/docs/partial-clone)
- [REBASH Academy – Linux Overview](../linux/index.md)
