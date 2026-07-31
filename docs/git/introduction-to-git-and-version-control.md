---
title: "Introduction to Git and Version Control"
description: "Understand version control for DevOps, local vs centralised vs distributed VCS, why Git dominates IaC and CI/CD, and core Git architecture vocabulary."
difficulty: beginner
estimated_time: "35–50 min"
technology: git
category: git
module: "Module 1 · Version Control Fundamentals"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - git
  - version-control
prerequisites:
  - linux/index
next:
  - git/understanding-the-git-object-model
related:
  - linux/index
  - git/git-installation-and-configuration
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - git
  - version-control
  - devops
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Introduction to Git and Version Control

## Overview



Explain why version control is the system of record for DevOps, compare VCS models, and use Git vocabulary (repo, commit, branch, remote) correctly before installing tools.

Incidents ask “what changed?” Compliance asks “who approved?” Git answers both. This course is **Git & GitHub for Cloud & DevOps Engineers** — workflows for IaC, GitOps, and CI/CD, not Git as trivia.

This is a core tutorial in **Module 1 · Version Control Fundamentals** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



### Required

- [Linux Fundamentals](../linux/index.md)
- Comfort with a terminal



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] State problems VCS solves for ops teams  
- [ ] Compare local, centralised, and distributed VCS  
- [ ] Explain why Git fits cloud-native delivery  
- [ ] Define repository, commit, branch, remote, working tree  
- [ ] Sketch the working → staging → commit → remote flow



## Architecture



Daily Git flow from edits to remotes and pipelines:

![Git workflow](../assets/excalidraw/git-workflow.svg)



## Theory



### What

A **version control system (VCS)** records how files change over time so people can collaborate, audit decisions, and roll back mistakes. Git is a **distributed** VCS: every clone holds a full repository history, not just the latest checkout. For Cloud and DevOps work, that history covers application code **and** infrastructure definitions — Terraform, Kubernetes manifests, Ansible, pipeline YAML, and policy-as-code.

### Why

Without version control, change management collapses into tickets, shared folders, and “who last edited prod?”. Git gives you an append-only trail of snapshots, cheap branching for parallel work, and remotes that coordinate teams. Hosting platforms (GitHub, GitLab, Bitbucket) add pull requests, CI triggers, and access control on top of that core. Treat Git as the **system of record** for anything you expect to deploy or review.

### How it works

You edit files in the **working tree**. Interesting changes move into the **staging area** (index) with `git add`, then become an immutable **commit** — a snapshot plus metadata (author, message, parent). Local commits sit on a **branch** (a movable pointer). `git push` publishes commits to a **remote** such as `origin`. Colleagues `fetch` or `pull` those objects into their clones. Offline work is normal; sync happens when remotes are reachable.

| Model | Idea | Example |
|-------|------|---------|
| Local | History on one machine | Early RCS-style tools |
| Centralised | One server is authority | Subversion (SVN) |
| Distributed | Every clone is a full repo | **Git** |

### Key concepts

| Term | Meaning |
|------|---------|
| Repository | Project history under `.git` |
| Working tree | Files you edit |
| Staging (index) | Snapshot prepared for the next commit |
| Commit | Immutable snapshot + metadata |
| Branch | Movable pointer to a commit |
| Remote | Named URL of another repository |
| HEAD | Current checkout tip |

Terraform modules, Kubernetes manifests, GitHub Actions workflows, and policy all live here. Treat `main` as production-intent unless your branching model says otherwise.

### Common pitfalls

- Treating Git as “backup only” and skipping meaningful commit messages  
- Editing production by hand instead of merging reviewed commits  
- Confusing the working tree with the repository (`.git`)  
- Assuming a clone without a remote is “not real Git” — remotes are optional until you collaborate



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-01 && cd ~/rebash-git/module-01
```

**Focus:** practise Git skills for: Introduction to Git and Version Control

### Step 1 – Init repository

```bash
git init -b main
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
echo '# lab' > README.md
git add README.md
git commit -m 'Initial commit'
git log --oneline
```

### Step 2 – Add commit cycle

```bash
echo 'hello' > app.txt
git status
git add app.txt
git commit -m 'Add app.txt'
git status
git log -1 --stat
```

### Final step – Cleanup note

```bash
# Safe local repo under the lab directory; delete the folder when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-git/module-01/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Introduction to Git and Version Control** always combines:

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



!!! warning "Treating Git as “backup only” and skipping meaningful commit messages  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Editing production by hand instead of merging reviewed commits  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Introduction to Git and Version Control changes as code and review them in pull requests
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



- Git is the DevOps system of record  
- Distributed clones enable offline work and collaboration  
- Next: object model, then install



## Interview Questions


1. Explain **Introduction to Git and Version Control** as you would in a senior engineer interview.
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
- [Understanding the Git Object Model](understanding-the-git-object-model.md)  
- [Git Installation and Configuration](git-installation-and-configuration.md)



## References



- [Pro Git — Getting Started](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
