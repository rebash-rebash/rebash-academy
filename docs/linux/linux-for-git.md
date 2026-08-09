---
title: "Linux for Git — Version Control in Linux Environments"
description: "Use Git on Linux — install and configure Git, SSH authentication, branches, remotes, permissions, .gitignore, and production Git practices."
difficulty: advanced
estimated_time: "120 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 13 · Linux for DevOps"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - git
  - version-control
  - ssh
  - devops
  - rebash-linux-mastery
comments: false
status: ready
---

# Linux for Git — Version Control in Linux Environments

> **Git** is the world's most widely used distributed version control system and is deeply integrated into Linux-based development and DevOps workflows. From writing source code to deploying applications through CI/CD pipelines, Git enables teams to collaborate efficiently while maintaining a complete history of every change. Since Git was originally developed for the Linux kernel, it integrates naturally with Linux filesystems, permissions, SSH authentication, and shell environments. Every DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Software Engineer should master Git on Linux.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 13: Linux for DevOps → Lesson 4</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Advanced</div>

<div markdown>**Reading Time:** 120 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Linux for DevOps</div>

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Git on Linux
- Configure Git for development
- Use SSH authentication
- Manage repositories
- Work with branches and merges
- Troubleshoot Git issues
- Secure Git access
- Apply Git best practices in production

---

# Prerequisites

Complete:

- Modules 1–12
- Module 13 Lessons 1–3

---

# Why Learn Git on Linux?

Modern software development revolves around Git.

```text
Developer

↓

Git Commit

↓

Remote Repository

↓

CI/CD Pipeline

↓

Deployment
```

Linux provides the environment where most Git repositories are developed, tested, and deployed.

---

# What is Git?

Git is a distributed version control system that allows developers to:

- Track changes
- Collaborate with teams
- Manage source code
- Create branches
- Merge changes
- Roll back previous versions

Every clone of a repository contains the complete project history.

---

# Git Workflow

```text
Working Directory

↓

Staging Area

↓

Local Repository

↓

Remote Repository
```

---

# Install Git

Ubuntu

```bash
sudo apt install git
```

RHEL

```bash
sudo dnf install git
```

Verify installation.

```bash
git --version
```

---

# Configure Git

Configure your identity.

```bash
git config --global user.name "John Doe"
```

```bash
git config --global user.email "john@example.com"
```

View configuration.

```bash
git config --list
```

---

# Create a Repository

Create a directory.

```bash
mkdir demo
```

Enter it.

```bash
cd demo
```

Initialize Git.

```bash
git init
```

---

# Clone a Repository

HTTPS

```bash
git clone https://example.com/project.git
```

SSH

```bash
git clone git@example.com:project.git
```

---

# Repository Status

Check repository status.

```bash
git status
```

Shows:

- Modified files
- Untracked files
- Staged changes
- Branch information

---

# Add Files

Stage a file.

```bash
git add file.txt
```

Stage everything.

```bash
git add .
```

---

# Commit Changes

Create a commit.

```bash
git commit -m "Initial commit"
```

---

# View History

Display commit history.

```bash
git log
```

Compact view.

```bash
git log --oneline
```

---

# Branches

Create a branch.

```bash
git branch feature-login
```

Switch branches.

```bash
git switch feature-login
```

Or:

```bash
git checkout feature-login
```

List branches.

```bash
git branch
```

---

# Merge Branches

Merge into the current branch.

```bash
git merge feature-login
```

---

# Remote Repositories

View remotes.

```bash
git remote -v
```

Add remote.

```bash
git remote add origin git@example.com:project.git
```

Push code.

```bash
git push origin main
```

Pull changes.

```bash
git pull origin main
```

---

# SSH Authentication

Generate an SSH key.

```bash
ssh-keygen -t ed25519
```

Start the SSH agent.

```bash
eval "$(ssh-agent -s)"
```

Add the key.

```bash
ssh-add ~/.ssh/id_ed25519
```

Test connectivity.

```bash
ssh -T git@example.com
```

SSH provides secure authentication without repeatedly entering passwords.

---

# Linux File Permissions

Git tracks file contents but relies on Linux for filesystem permissions.

Check permissions.

```bash
ls -l
```

Make a script executable.

```bash
chmod +x deploy.sh
```

Git records the executable permission for tracked files.

---

# Ignore Files

Create:

```text
.gitignore
```

Example:

```text
*.log

node_modules/

.env

*.tmp
```

Ignore build artifacts, secrets, and temporary files.

---

# Git Tags

Create a release tag.

```bash
git tag v1.0.0
```

List tags.

```bash
git tag
```

Push tags.

```bash
git push origin --tags
```

---

# Troubleshooting Git

Check current branch.

```bash
git branch
```

Review differences.

```bash
git diff
```

Inspect commits.

```bash
git log --oneline
```

Verify remote.

```bash
git remote -v
```

---

# Useful Linux Commands

Current directory.

```bash
pwd
```

Files.

```bash
ls
```

Permissions.

```bash
ls -l
```

SSH keys.

```bash
ls ~/.ssh
```

Processes.

```bash
ps aux
```

---

# Real Production Examples

Clone repository.

```bash
git clone git@example.com:project.git
```

View status.

```bash
git status
```

Commit changes.

```bash
git commit -m "Bug fix"
```

Push changes.

```bash
git push origin main
```

---

# Production Perspective

Git is used across:

- GitHub
- GitLab
- Bitbucket
- Azure Repos
- CI/CD pipelines
- Kubernetes deployments
- Infrastructure as Code
- Cloud-native applications

Linux and Git together form the backbone of modern software development.

---

# Hands-on Lab

## Task 1

Verify Git installation.

```bash
git --version
```

---

## Task 2

Configure your Git identity.

```bash
git config --global user.name "Your Name"

git config --global user.email "you@example.com"
```

---

## Task 3

Create a repository.

```bash
mkdir demo

cd demo

git init
```

---

## Task 4

Create a file and commit it.

```bash
echo "Hello Git" > README.md

git add README.md

git commit -m "Initial commit"
```

---

## Task 5

Create a new branch.

```bash
git switch -c feature-demo
```

---

## Task 6

Generate an SSH key.

```bash
ssh-keygen -t ed25519
```

---

## Task 7

Display Git history.

```bash
git log --oneline
```

---

## Task 8

Create a `.gitignore` file that ignores:

- Log files
- Temporary files
- Build directories
- Environment files

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `git init` | Initialize repository | New project |
| `git status` | View repository state | Development workflow |
| `git add` | Stage changes | Code review |
| `git commit` | Save changes | Version control |
| `git push` | Upload changes | CI/CD integration |
| `git pull` | Synchronize repository | Team collaboration |

---

# Common Git Mistakes

| Mistake | Solution |
|----------|----------|
| Committing secrets | Use `.gitignore` and secret scanning |
| Working directly on the main branch | Use feature branches |
| Forgetting to pull before pushing | Synchronize frequently |
| Ignoring merge conflicts | Resolve conflicts carefully |
| Not using SSH keys | Configure secure authentication |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A developer cannot push code to the remote repository.

Investigation:

```bash
git remote -v
```

Remote is correct.

Next:

```bash
ssh -T git@example.com
```

Authentication fails.

Further investigation:

```bash
ls ~/.ssh
```

No SSH key exists.

The administrator generates a new SSH key, adds the public key to the Git hosting platform, and loads the private key into the SSH agent.

Verification:

```bash
ssh -T git@example.com
```

Authentication succeeds.

Root cause:

```text
Missing SSH Authentication
```

---

# Best Practices

- Configure Git with your identity.
- Use SSH authentication instead of passwords.
- Create feature branches for new work.
- Write meaningful commit messages.
- Keep repositories clean using `.gitignore`.
- Never commit credentials or secrets.
- Pull frequently to reduce merge conflicts.
- Tag production releases.

---

# Common Mistakes

❌ Committing passwords or API keys.

✅ Avoid this mistake: committing passwords or API keys.

---

❌ Working directly on the production branch.

✅ Avoid this mistake: working directly on the production branch.

---

❌ Ignoring merge conflicts.

✅ Always review merge conflicts.

---

❌ Forgetting executable permissions for scripts.

✅ Remember to executable permissions for scripts.

---

❌ Using vague commit messages like "update" or "fix".

✅ Avoid using vague commit messages like "update" or "fix" when a safer approach exists.

---

# Interview Questions
## Beginner

1. What is Git?
2. What is the purpose of `git init`?
3. What does `git status` display?
4. Why is `.gitignore` used?

---

## Intermediate

1. What is the difference between `git fetch` and `git pull`?
2. Why is SSH authentication preferred?
3. How do Linux file permissions affect Git repositories?
4. How would you resolve a merge conflict?

---

## Architect Level

1. How would you design a Git branching strategy for a large DevOps team?
2. How would you secure enterprise Git repositories?
3. How would you integrate Git with CI/CD and Infrastructure as Code workflows?

---

# Summary

In this lesson, you learned:

- Git fundamentals on Linux
- Repository management
- Git configuration
- SSH authentication
- Branching and merging
- File permissions
- Repository security
- Production Git best practices

Git and Linux work together to provide a powerful platform for version control and collaboration. By mastering Git on Linux, you can manage source code efficiently, collaborate with development teams, automate software delivery, and support modern DevOps workflows with confidence.

---

## Key Takeaways

- Git was originally developed for Linux and integrates naturally with Linux systems.
- Configure Git properly before collaborating with others.
- Use SSH keys for secure authentication.
- Follow a branching strategy instead of committing directly to the main branch.
- Protect repositories by avoiding committed secrets and using `.gitignore`.
- Strong Git skills are fundamental for every DevOps engineer.

---

## What's Next?

**[Linux for Terraform — Infrastructure as Code on Linux](linux-for-terraform.md)**

You'll explore:

- Running Terraform on Linux
- Managing Infrastructure as Code (IaC)
- Environment variables
- State management
- SSH authentication
- Automation with shell scripts
- Production Terraform best practices

By the end of the lesson, you'll understand how Linux provides the ideal environment for developing, automating, and managing infrastructure using Terraform.
