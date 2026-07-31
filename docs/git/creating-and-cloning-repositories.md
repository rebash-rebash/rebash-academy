---
title: "Creating and Cloning Repositories"
description: "Create local repos with git init, clone remotes safely, and understand bare vs non-bare repositories for DevOps workflows."
difficulty: beginner
estimated_time: "30–45 min"
technology: git
category: git
module: "Module 3 · Git Basics"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
skills:
  - git
  - clone
  - init
prerequisites:
  - git/git-installation-and-configuration
next:
  - git/basic-git-workflow-add-commit-push
related:
  - git/working-with-remotes
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - git
  - clone
  - init
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Creating and Cloning Repositories

## Overview



Initialise a local repository, clone a remote, and inspect `.git` so you know where history lives before first commits.

`git init` starts history locally; `git clone` copies a remote including objects and remotes. IaC and app work both start here.

This is a core tutorial in **Module 3 · Git Basics** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Git Installation and Configuration](git-installation-and-configuration.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] `git init -b main` a project  
- [ ] Clone via SSH/HTTPS  
- [ ] List remotes after clone  
- [ ] Describe what `.git/` holds



## Architecture



This topic’s control points and relationships are shown below.

![Git workflow](../assets/excalidraw/git-workflow.svg)



## Theory



### What

A **repository** is a project’s working tree plus the `.git` database. You create one with `git init` (new local project) or obtain one with `git clone` (copy of an existing remote, including history and a default remote named `origin`). **Bare** repositories have no working tree and usually act as remotes on servers.

### Why

Choosing `init` versus `clone` sets collaboration shape. Most DevOps work starts from `clone` of an organisation repo or fork. Shallow clones (`--depth 1`) speed CI when full history is unnecessary. Understanding bare remotes clarifies how GitHub and self-hosted Git servers store canonical history.

### How it works

`git init -b main` creates `.git/` with empty object storage, refs, and config, and points HEAD at `main`. You then add files and commit. `git clone <url>` copies objects from the remote, checks out the default branch, and configures `origin`. Optional flags adjust depth, single-branch behaviour, or target directory. Bare repos (`repo.git`) accept pushes and serve fetches without a checked-out tree — developers almost always use non-bare clones on laptops.

```bash
mkdir app && cd app
git init -b main

git clone git@github.com:org/repo.git
git clone --depth 1 <url>   # shallow — common in CI
```

### Key concepts

| Action | Result |
|--------|--------|
| `init` | New empty history on this machine |
| `clone` | Full (or shallow) copy + `origin` remote |
| Bare repo | Remote-style store, no working tree |
| Non-bare | Working tree + `.git` for daily work |

Forks on GitHub are separate remotes you usually name `origin` (your fork) and `upstream` (canonical).

### Common pitfalls

- Running `git init` inside an existing clone and creating a nested repo by accident  
- Cloning with HTTPS then struggling with credentials when SSH was intended  
- Assuming a shallow clone can always rebase or bisect across old history  
- Pushing to a non-bare repo that has a checked-out branch (server rejection)



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-03 && cd ~/rebash-git/module-03
```

**Focus:** create a bare remote and clone it

### Step 1 – Clone workflow

```bash
git init -b main seed && cd seed
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
echo '# seed' > README.md
git add README.md && git commit -m 'seed'
cd ..
git clone --bare seed remote.git
git clone remote.git workspace
cd workspace && git log --oneline && pwd
```

### Final step – Cleanup note

```bash
rm -rf seed remote.git workspace
```



## Validation



- [ ] Lab commands run under `~/rebash-git/module-03/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Creating and Cloning Repositories** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.



## Security Considerations



- Treat credentials and tokens for git as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces



## Common Mistakes



!!! warning "Running `git init` inside an existing clone and creating a nested repo by accident  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Cloning with HTTPS then struggling with credentials when SSH was intended  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Creating and Cloning Repositories changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible



## Troubleshooting



| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |



## Summary



**Creating and Cloning Repositories** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. Explain **Creating and Cloning Repositories** as you would in a senior engineer interview.
2. You rebased a shared branch and teammates are blocked — what now?
3. How do you recover a commit that seems lost?
4. What Git security controls belong in a production org?
5. How should Git history look for Infrastructure as Code (IaC) repos?

!!! tip "Sample answer — question 2"
    Stop force-pushing; communicate; use `reflog` to recover; prefer revert on shared main. Reset/rebase only on private branches.

!!! tip "Sample answer — question 4"
    Signed commits, protected branches, secret scanning, least-privilege tokens, and signed tags for releases.



## Related Tutorials



- [Course overview](index.md)
- [Basic Git Workflow — Add, Commit, Push](basic-git-workflow-add-commit-push.md)



## References



- [git-init](https://git-scm.com/docs/git-init) · [git-clone](https://git-scm.com/docs/git-clone)
