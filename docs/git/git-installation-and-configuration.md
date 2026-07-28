---
title: Git Installation and Configuration
description: Install Git on Linux, macOS, and Windows; configure identity, editors, SSH keys, credential helpers, and production-ready global settings for DevOps workflows.
difficulty: beginner
estimated_time: "25 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: git
tags:
  - git
  - installation
  - configuration
  - ssh
  - devops
prerequisites:
  - Introduction to Git and Version Control
  - A Linux VM, WSL2, or macOS terminal with network access
  - Basic familiarity with the Linux command line
comments: false
---

# Git Installation and Configuration

## Overview

Before your first meaningful commit reaches a CI pipeline, Git must be **installed correctly** and **configured consistently**. Wrong author emails break compliance audits. Missing SSH keys block pushes from automation runners. A misconfigured credential helper leaks tokens into logs. Platform engineers onboarding hundreds of developers standardize Git installation and config the same way they standardize base AMIs and container images.

This tutorial covers installing Git across environments, setting **identity** and **defaults**, configuring **SSH and HTTPS authentication**, tuning **performance settings** for large monorepos, and applying **security-conscious** options used in production DevOps teams.

This is **Tutorial 2** in **Module 1: Foundations** of the REBASH Academy Git series. Complete [Introduction to Git and Version Control](introduction-to-git-and-version-control.md) first. Linux package management and SSH fundamentals from the [Linux track](../linux/index.md) and [Networking track](../networking/index.md) apply directly here.

## Prerequisites

- Completion of [Introduction to Git and Version Control](introduction-to-git-and-version-control.md)
- A Linux environment (Ubuntu 22.04+ recommended) or macOS with terminal access
- `sudo` privileges for package installation on Linux
- Network access to download packages and reach Git hosting providers
- Familiarity with [Essential Linux Commands](../linux/essential-linux-commands.md) — especially editing files and managing permissions

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Install Git on Debian/Ubuntu, RHEL-family, and macOS using official or PPA sources
- [ ] Verify installation and locate the Git binary and system configuration files
- [ ] Configure global and repository-local identity (`user.name`, `user.email`)
- [ ] Set productive defaults: default branch, editor, pull behaviour, and whitespace handling
- [ ] Generate SSH key pairs and register them with GitHub or GitLab
- [ ] Configure HTTPS credential helpers securely for automation and interactive use
- [ ] Understand configuration precedence: system, global, local, and environment variables
- [ ] Apply a production-ready `.gitconfig` baseline for DevOps engineers

## Architecture

Git configuration flows through four layers. Later layers override earlier ones — a common source of "I changed my email but commits still show the old one" confusion.

```d2
direction: down

ENV: "Environment variables\nGIT_AUTHOR_NAME, GIT_DIR, ..."
    SYS: "System config\n/etc/gitconfig"
    GLOBAL: "Global config\n~/.gitconfig"
    LOCAL: "Local config\n.git/config"
    CMD: "Command-line flags\n--author, -c key=value"
    SYS -> GLOBAL
    GLOBAL -> LOCAL
    LOCAL -> ENV
    ENV -> CMD
    EFFECT: "Effective config value"
    CMD -> EFFECT: "wins for this invocation"
    LOCAL -> EFFECT
    GLOBAL -> EFFECT
    SYS -> EFFECT
    ENV -> EFFECT
```

## Theory

### Installation Sources and Version Pinning

Git releases frequently — security fixes and performance improvements land in minor versions. Production teams pin minimum versions in documentation (e.g., "Git ≥ 2.34") and CI base images.

| Platform | Recommended method | Notes |
|----------|-------------------|-------|
| Ubuntu/Debian | `apt` or Git PPA | Distro packages may lag; PPA provides latest stable |
| RHEL/Rocky/Alma | `dnf install git` | AppStream module versions vary by release |
| macOS | Xcode CLT or Homebrew | `git --version` after CLT may be older; Homebrew is newer |
| Windows | Git for Windows installer | Includes Git Bash; use WSL2 for Linux parity in DevOps |
| Containers | Base image + `apt-get install git` | Pin in Dockerfile; avoid `latest` tag drift |

For DevOps CI images, install Git in the Dockerfile layer and verify with `git --version` in a health check step. Alpine uses `apk add git`; ensure OpenSSH client is present if using SSH remotes.

### Identity Configuration

Every commit records **author** and **committer** name and email. These fields are immutable in the object once committed (without history rewrite). Use:

- **Corporate email** for work repositories — enables GitHub/GitLab account linking and audit trails
- **noreply addresses** (e.g., `123456+user@users.noreply.github.com`) when privacy settings require hiding personal email
- **Consistent bot identities** for automation: `ci-bot@company.com` with clear display name `CI Bot`

Never use fake emails like `admin@localhost` in shared repos — they break `git blame` and code ownership tools.

### The Three Configuration Scopes

```bash
git config --system    # /etc/gitconfig — all users on machine (requires root)
git config --global    # ~/.gitconfig — current user's default
git config --local     # .git/config — single repository only
```

**Precedence (highest wins):** command-line → local → global → system → built-in defaults.

Repository-local config overrides global — useful when a contractor uses a personal email globally but a corporate email for one client repo.

### Essential Settings for DevOps

| Setting | Recommended value | Why |
|---------|-------------------|-----|
| `init.defaultBranch` | `main` | Industry standard; avoids renaming later |
| `pull.rebase` | `false` (teams vary) | Document team policy; rebase keeps linear history |
| `fetch.prune` | `true` | Removes stale remote-tracking branches after fetch |
| `core.autocrlf` | `input` (Linux/macOS) | Prevents CRLF corruption in shell scripts and Terraform |
| `core.editor` | `vim`, `nano`, or `code --wait` | Required for interactive rebase and commit amend |
| `colour.ui` | `auto` | Readable diffs in terminal |
| `push.default` | `simple` | Push current branch to matching remote branch only |
| `rebase.autoStash` | `true` | Stash local changes before rebase automatically |

### SSH vs HTTPS Authentication

| Method | Pros | Cons | DevOps use case |
|--------|------|------|-----------------|
| **SSH** | Key-based, no password prompts, works with deploy keys | Key management overhead | Developer laptops, dedicated CI deploy keys |
| **HTTPS** | Firewall-friendly (port 443), PAT/OAuth tokens | Tokens expire; credential storage risk | Corporate proxies, short-lived CI tokens |

**SSH** uses `git@github.com:org/repo.git`. Keys live in `~/.ssh/`; `ssh-agent` holds passphrases during sessions.

**HTTPS** uses `https://github.com/org/repo.git`. Personal Access Tokens (PATs) replace passwords. Store via `credential.helper` — never commit tokens to repos.

For production CI, prefer **short-lived OIDC tokens** (GitHub Actions → AWS) or **machine users** with scoped PATs rotated on schedule.

### Credential Helpers

Git credential helpers cache or store HTTPS credentials:

- **`cache`** — memory cache with timeout (default 15 minutes)
- **`store`** — plaintext file `~/.git-credentials` (avoid on shared machines)
- **`manager`** / **`osxkeychain`** — OS keychain integration (preferred on workstations)
- **Custom helpers** — enterprise secret vault integration

In CI, inject tokens via environment variables and use:

```bash
git config credential.helper '!f() { echo "username=x-access-token"; echo "password=$GITHUB_TOKEN"; }; f'
```

Never echo tokens in pipeline logs — mask variables in GitHub Actions / GitLab CI settings.

### System-Wide and Enterprise Configuration

Large organizations deploy `/etc/gitconfig` via configuration management (Ansible, cloud-init):

```ini
[safe]
    directory = /var/lib/jenkins/workspace
[protocol]
    version = 2
[credential]
    helper = manager
```

The `safe.directory` setting (Git 2.35+) prevents CVE-2022-24765 issues when repos are owned by different users — common on CI runners and shared build hosts.

## Hands-on Lab

Perform these steps on your Linux lab machine. Adjust package commands for your distribution.

### Step 1 – Check if Git is already installed

**Command:**

```bash
git --version 2>/dev/null || echo "Git not installed"
type git 2>/dev/null
```

**Explanation:** Cloud images and developer laptops often ship with Git pre-installed. Record the version for your runbook baseline.

**Expected output:**

```text
git version 2.43.0
git is /usr/bin/git
```

### Step 2 – Install Git on Ubuntu/Debian

**Command:**

```bash
sudo apt update
sudo apt install -y git
git --version
```

**Explanation:** Distro packages are sufficient for learning. For the latest stable on Ubuntu, add the `git-core` PPA only in non-production lab environments.

**Expected output:**

```text
git version 2.x.x
```

### Step 3 – Configure global identity

**Command:**

```bash
git config --global user.name "Shaik Basha"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global --list | grep -E 'user\.|init\.'
```

**Explanation:** Identity applies to all new commits in repos without local overrides. Use your real work email for corporate projects.

**Expected output:**

```text
user.name=Shaik Basha
user.email=you@example.com
init.defaultbranch=main
```

### Step 4 – Set editor and useful defaults

**Command:**

```bash
git config --global core.editor "nano"
git config --global color.ui auto
git config --global fetch.prune true
git config --global pull.rebase false
git config --global push.default simple
git config --global rebase.autoStash true
```

**Explanation:** These defaults match common team policies. Align `pull.rebase` with your organisation's documented workflow.

**Expected output:**

```text
(no output — success is silent)
```

### Step 5 – Generate an SSH key pair

**Command:**

```bash
ssh-keygen -t ed25519 -C "you@example.com" -f ~/.ssh/id_ed25519_git -N ""
ls -la ~/.ssh/id_ed25519_git*
cat ~/.ssh/id_ed25519_git.pub
```

**Explanation:** Ed25519 keys are modern, compact, and secure. In production, use a passphrase (`-N ""` is lab-only). Add the public key to GitHub → Settings → SSH Keys.

**Expected output:**

```text
Generating public/private ed25519 key pair.
...
ssh-ed25519 AAAA... you@example.com
```

### Step 6 – Configure SSH for Git hosting

**Command:**

```bash
cat >> ~/.ssh/config << 'EOF'
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_git
  IdentitiesOnly yes
EOF
chmod 600 ~/.ssh/config
ssh -T git@github.com 2>&1 | head -3
```

**Explanation:** `IdentitiesOnly yes` prevents SSH from offering wrong keys. Test connectivity — expect "Hi username!" or "Permission denied" if key not yet added to GitHub.

**Expected output:**

```text
Hi username! You've successfully authenticated...
```

### Step 7 – Inspect configuration precedence

**Command:**

```bash
mkdir -p /tmp/git-config-lab && cd /tmp/git-config-lab
git init
git config user.email "local-only@example.com"
git config --show-origin --get user.email
git config --show-origin --get user.name
```

**Explanation:** `--show-origin` reveals which file set each value — essential when debugging wrong identity in commits.

**Expected output:**

```text
file:/tmp/git-config-lab/.git/config  local-only@example.com
file:/home/user/.gitconfig  Shaik Basha
```

### Step 8 – Clean up lab directory

**Command:**

```bash
cd /tmp && rm -rf git-config-lab
```

**Explanation:** Remove test repositories after configuration labs.

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
| `git --version` | Verify installation | `git --version` |
| `git config --global KEY VAL` | Set global option | `git config --global user.name "Name"` |
| `git config --list --show-origin` | List all settings with source file | `git config -l --show-origin` |
| `git config --unset KEY` | Remove a setting | `git config --global --unset credential.helper` |
| `ssh-keygen -t ed25519` | Create SSH key pair | `ssh-keygen -t ed25519 -C "email"` |
| `ssh -T git@github.com` | Test SSH auth to GitHub | `ssh -T git@github.com` |
| `git config credential.helper` | Show credential helper | `git config --global credential.helper store` |

### Production baseline `.gitconfig`

Copy to `~/.gitconfig` and customize identity:

```ini
[user]
    name = Shaik Basha
    email = you@company.com

[init]
    defaultBranch = main

[core]
    editor = nano
    autocrlf = input
    whitespace = trailing-space,space-before-tab
    excludesfile = ~/.gitignore_global

[color]
    ui = auto

[fetch]
    prune = true

[push]
    default = simple

[pull]
    rebase = false

[rebase]
    autoStash = true

[diff]
    algorithm = histogram

[merge]
    conflictstyle = zdiff3

[help]
    autocorrect = 10

[credential]
    helper = cache --timeout=3600

[safe]
    directory = *
```

The `safe.directory = *` entry is convenient on trusted personal machines; on shared CI runners, list specific paths instead.

### Global gitignore template

Create `~/.gitignore_global` for OS and editor junk:

```gitignore
# OS
.DS_Store
Thumbs.db

# Editors
*.swp
*~
.idea/
.vscode/

# Secrets — never commit
.env
*.pem
credentials.json
```

Register it: `git config --global core.excludesfile ~/.gitignore_global`

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Using different emails across machines"
    Commits from the same human with different emails fragment `git shortlog` and code ownership reports. Standardize via Ansible/chef and verify with `git config --global user.email`.

!!! warning "Committing with default 'root' identity on servers"
    Running `git commit` as root on production boxes creates useless audit trails. Use deploy keys with bot identity or avoid Git operations on servers entirely — deploy artifacts instead.

!!! warning "Storing PATs in plaintext credential store on shared CI"
    The `store` helper writes credentials to disk unencrypted. On shared runners, use ephemeral environment-injected tokens with masked CI variables.

!!! warning "Skipping SSH host key verification"
    Disabling `StrictHostKeyChecking` opens MITM attacks. Pre-load known hosts in CI: `ssh-keyscan github.com >> ~/.ssh/known_hosts`.

## Best Practices

!!! tip "Pin Git version in CI Dockerfiles"
    Document `git --version` in build logs. Unexpected upgrades have changed default behaviours (e.g., `safe.directory`).

!!! tip "Use separate SSH keys per purpose"
    One key for personal GitHub, one deploy key per repo (read-only for CI), one for production bastion — limits blast radius if a key leaks.

!!! tip "Configure Git once in golden AMI / container base"
    Platform teams bake `/etc/gitconfig` and `safe.directory` into Jenkins agent AMIs and Kubernetes CI pod images.

!!! tip "Align with Linux SSH hardening"
    File permissions matter: `chmod 700 ~/.ssh`, `chmod 600 ~/.ssh/id_*`. See [Linux user management](../linux/user-and-group-management.md) for permission fundamentals.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `git: command not found` after install | PATH not updated in current shell | Open new shell or `hash -r`; verify `/usr/bin/git` |
| Commits show wrong email | Local repo override or env var | `git config --show-origin --get user.email`; check `GIT_AUTHOR_EMAIL` |
| `Permission denied (publickey)` | Key not loaded or not on GitHub | `ssh-add -l`; add pubkey to hosting platform; verify `IdentityFile` |
| `Support for password authentication was removed` | GitHub deprecated password HTTPS | Use PAT or SSH instead |
| `fatal: unsafe repository` | Repo owned by different user (Git 2.35+) | `git config --global --add safe.directory /path/to/repo` |
| Credential helper not caching | Helper not configured or timeout expired | `git config credential.helper 'cache --timeout=86400'` |
| `git commit` opens wrong editor | `core.editor` misconfigured | `git config --global core.editor "vim"` |
| SSL certificate problem | Corporate MITM proxy or outdated CA | Install corporate CA; or use SSH remotes |

## Summary

- Install Git from trusted package sources and record version in runbooks and CI images
- Configure **identity** (`user.name`, `user.email`) before any shared commits — emails are permanent in history unless rewritten
- Settings apply in order: **system → global → local → environment → CLI flags**
- Use **SSH keys** (Ed25519) for developer workflows; **HTTPS + PAT** where firewalls require port 443
- Production teams standardize `.gitconfig`, global gitignore, `safe.directory`, and credential handling across the fleet

## Interview Questions

1. What are the three Git configuration scopes, and which takes precedence?
2. Why must `user.email` be configured correctly before your first commit?
3. Compare SSH and HTTPS authentication for Git remotes.
4. What is `init.defaultBranch`, and why set it to `main`?
5. How do credential helpers work, and what are the security tradeoffs?
6. What is the `safe.directory` configuration introduced in Git 2.35?
7. How would you verify which config file sets a particular Git option?
8. What Git settings would you bake into a CI runner base image?
9. Why should `core.autocrlf` be set to `input` on Linux DevOps workstations?
10. How do you test SSH connectivity to GitHub without cloning a repository?

??? tip "Sample Answers (Questions 1, 3, and 6)"

    **Q1 — Config scopes and precedence:** System (`/etc/gitconfig`) applies to all users. Global (`~/.gitconfig`) applies to the current user. Local (`.git/config`) applies to one repository. Local overrides global, which overrides system. Command-line flags like `-c key=value` override all files for that invocation.

    **Q3 — SSH vs HTTPS:** SSH uses public-key authentication (`git@host:repo.git`). No password prompts once keys are loaded; ideal for developers and deploy keys. HTTPS uses URLs like `https://host/repo.git` with PATs or OAuth tokens — better through strict corporate proxies on port 443. SSH requires key rotation discipline; HTTPS requires secure token storage and rotation.

    **Q6 — safe.directory:** Git 2.35+ refuses to operate on repositories whose directory is owned by a different user than the one running Git, preventing CVE-2022-24765 exploits on shared systems. CI runners and `sudo` workflows hit this often. Fix by explicitly trusting paths with `git config --global --add safe.directory /path` or `*` on trusted personal machines only.

## Related Tutorials

- [Git – Category Overview](index.md)
- [Introduction to Git and Version Control](introduction-to-git-and-version-control.md) *(previous in Module 1)*
- [Understanding the Git Object Model](understanding-the-git-object-model.md) *(next in Module 1)*
- [Introduction to Linux](../linux/introduction-to-linux.md)
- [Introduction to Networking](../networking/introduction-to-networking.md) — SSH and HTTPS connectivity

## References

- [Git – First-Time Git Setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)
- [GitHub – Connecting with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [GitLab – SSH keys](https://docs.gitlab.com/ee/user/ssh.html)
- [Git config manual](https://git-scm.com/docs/git-config)
- [CVE-2022-24765 – safe.directory](https://github.blog/2022-04-12-git-security-vulnerability-announced/)
- [REBASH Academy – Linux Overview](../linux/index.md)
