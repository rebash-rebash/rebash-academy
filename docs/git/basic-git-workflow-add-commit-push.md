---
title: "Basic Git Workflow — Add, Commit, Push"
description: "Practise the core Git loop — status, add, commit, log, and push — with clear commit messages for DevOps and IaC changes."
difficulty: beginner
estimated_time: "35–50 min"
technology: git
category: git
module: "Module 3 · Git Basics"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - platform-engineer
skills:
  - git
  - commit
  - push
prerequisites:
  - git/creating-and-cloning-repositories
next:
  - git/viewing-history-and-diffs
related:
  - git/working-with-remotes
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - git
  - commit
  - workflow
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Basic Git Workflow — Add, Commit, Push

## Overview




Run the daily loop: edit → `status` → `add` → `commit` → `log` → `push`, with Conventional-style messages suitable for IaC and apps.

Staging lets you craft commits intentionally. Push publishes history to the remote for CI and teammates.

This is a core tutorial in **Module 3 · Git Basics** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites




- [Creating and Cloning Repositories](creating-and-cloning-repositories.md)



## Learning Objectives




By the end of this tutorial, you will be able to:

- [ ] Read `git status` and `git diff`  
- [ ] Stage with `git add`  
- [ ] Commit with a clear message  
- [ ] View `git log`  
- [ ] Push to `origin` when a remote exists



## Architecture




This topic’s control points and relationships are shown below.

![Git workflow](../assets/excalidraw/git-workflow.svg)



## Theory




### What

The everyday Git loop is **edit → stage → commit → push**. `git status` shows what changed; `git add` selects content for the next snapshot; `git commit` records that snapshot; `git log` reviews history; `git push` publishes commits to a remote so CI and teammates can see them.

### Why

Staging exists so a commit can be a **coherent unit of work**, not “everything dirty on disk”. In DevOps, a good commit might be one Terraform module change or one pipeline fix — small enough to review and revert. Pushing without committing leaves work trapped on one laptop; committing without reviewing `status` risks secrets and debug junk.

### How it works

The working tree holds edits. `git add` copies file content into the **index**. `git commit` freezes the index as a new commit object on the current branch and advances the branch pointer. Messages should use an imperative summary (`fix: pin terraform provider`) with an optional body explaining *why*. After local commits exist, `git push` sends missing objects and updates the remote branch. First push of a branch often uses `-u` to set upstream tracking.

| Command | Role |
|---------|------|
| `status` | What changed |
| `add` | Stage |
| `commit` | Record snapshot |
| `log` | History |
| `push` | Publish to remote |

### Key concepts

- **Atomic commits** beat giant “WIP” dumps for review and `git bisect` later  
- **Upstream tracking** lets bare `git push` / `git pull` know which remote branch to use  
- **Hooks** (pre-commit, commit-msg) may reject bad messages or secrets — fix the cause, do not bypass casually  
- Conventional prefixes (`feat:`, `fix:`, `chore:`) help changelogs and automation  

### Common pitfalls

- `git add .` blindly — stage secrets, build artefacts, or unrelated files  
- Empty or joke commit messages that waste reviewers  
- Committing on the wrong branch then force-pushing to “fix” it  
- Pushing to `main` when policy requires a pull request



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-03/workflow && cd ~/rebash-git/module-03/workflow
```

**Focus:** practise status → add → commit → log

### Step 1 – Edit, stage, commit

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo "service: api" > app.yaml
git add app.yaml
git commit -m "feat: add app.yaml skeleton"
echo "replicas: 2" >> app.yaml
git status
git diff
git add app.yaml
git commit -m "feat: set replicas to 2"
git log --oneline --decorate -n 5
```

### Step 2 – Partial staging awareness

```bash
echo "debug: true" >> app.yaml
echo "notes" > NOTES.txt
git add NOTES.txt
git status
git restore --staged NOTES.txt
git checkout -- app.yaml
git status
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```



## Validation




- [ ] Lab commands run under `~/rebash-git/module-03/workflow/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough




Production practice for **Basic Git Workflow — Add, Commit, Push** always combines:

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




!!! warning "`git add .` blindly — stage secrets, build artefacts, or unrelated files  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Empty or joke commit messages that waste reviewers  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices




- Encode Basic Git Workflow — Add, Commit, Push changes as code and review them in pull requests
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




**Basic Git Workflow — Add, Commit, Push** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. What does the staging area allow you to do?
2. You committed the wrong file — how do you fix it safely before push?
3. What makes a good commit message for IaC changes?
4. Why review git status before every commit?
5. When should you amend versus make a new commit?

!!! tip "Sample answer — question 2"
    If not pushed, restore --staged / soft reset can reshape the commit. If pushed and shared, prefer a follow-up commit.

!!! tip "Sample answer — question 4"
    Never amend commits that others have based work on. Keep secrets out with status/diff review.



## Related Tutorials




- [Course overview](index.md)
- [Viewing History and Diffs](viewing-history-and-diffs.md)



## References




- [Pro Git — Recording Changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)
