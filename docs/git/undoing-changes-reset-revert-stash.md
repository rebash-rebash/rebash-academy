---
title: "Undoing Changes — Reset, Revert, and Stash"
description: "Undo safely with restore, reset, revert, and stash — choose the right tool for local vs published history in DevOps workflows."
difficulty: intermediate
estimated_time: "40–55 min"
technology: git
category: git
module: "Module 7 · Rebasing & History"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - git
  - reset
  - revert
  - stash
prerequisites:
  - git/rebasing-and-interactive-rebase
next:
  - git/cherry-pick-and-reflog
related:
  - git/git-troubleshooting
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - git
  - reset
  - revert
  - stash
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Undoing Changes — Reset, Revert, and Stash

## Overview



Pick the correct undo tool: `restore` for files, `stash` for WIP, `reset` for local history, `revert` for published commits.

**Reset** moves branch pointers (dangerous if pushed). **Revert** adds a new commit that undoes a previous one — safe on `main`. **Stash** shelves WIP.

This is a core tutorial in **Module 7 · Rebasing & History** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Rebasing and Interactive Rebase](rebasing-and-interactive-rebase.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] `git restore` / `restore --staged`  
- [ ] `stash` / `stash pop`  
- [ ] Soft/mixed/hard reset differences  
- [ ] `git revert` on shared branches



## Architecture



This topic’s control points and relationships are shown below.

![Architecture diagram for Undoing Changes — Reset, Revert, and Stash](../assets/excalidraw/git-workflow.svg)



## Theory



### What

Git offers several “undo” tools with different safety profiles. `git restore` fixes the working tree or unstages paths. `git stash` shelves work in progress. `git reset` moves a branch pointer (and optionally the index/working tree). `git revert` creates a *new* commit that undoes an earlier one — preferred on shared branches.

### Why

Choosing the wrong undo destroys collaboration. Resetting `main` after others pulled rewrites public history. Revert keeps history honest for audit and GitOps. Stash prevents dirty-tree blockers when you must hot-fix another branch.

### How it works

Unstaged edits to a tracked file can be discarded with `git restore file`. Staged-but-unwanted paths use `git restore --staged`. Stash (`git stash -u` to include untracked) records a WIP commit-like object you can `pop` or `apply` later. `reset --soft` moves HEAD and keeps the index; `--mixed` (default) moves HEAD and resets the index; `--hard` also resets the working tree — destructive. On `main`, prefer `git revert <sha>` so the undo is reviewable.

| Situation | Tool |
|-----------|------|
| Discard unstaged edits | `git restore file` |
| Unstage | `git restore --staged file` |
| WIP switch branch | `git stash -u` |
| Rewrite *local* commits | `git reset` |
| Undo on shared `main` | `git revert <sha>` |

### Key concepts

- **Safe vs destructive** — revert and restore are usually safer than hard reset  
- **Reflog** still remembers pre-reset positions for a while  
- **Stash is local** — it is not a backup strategy for a team  
- **Recoverability** — hard reset does not immediately delete objects  

### Common pitfalls

- `reset --hard` on the wrong branch  
- Stashing secrets then sharing a patch from the stash  
- Reverting a merge commit without understanding `-m` parent selection  
- Using reset to “clean” a laptop problem on a shared remote branch



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-07-undo && cd ~/rebash-git/module-07-undo
```

**Focus:** practise Git skills for: Undoing Changes — Reset, Revert, and Stash

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

### Step 2 – Reset / stash / revert

```bash
echo dirty > wip.txt
git stash push -m 'wip' -- wip.txt
git stash list
echo bad > bad.txt && git add bad.txt && git commit -m 'bad'
git revert --no-edit HEAD
git log --oneline | tee undo.txt
```

### Final step – Cleanup note

```bash
# Safe local repo under the lab directory; delete the folder when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-git/module-07-undo/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Undoing Changes — Reset, Revert, and Stash** always combines:

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



!!! warning "`reset --hard` on the wrong branch  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Stashing secrets then sharing a patch from the stash  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Undoing Changes — Reset, Revert, and Stash changes as code and review them in pull requests
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



**Undoing Changes — Reset, Revert, and Stash** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. Explain **Undoing Changes — Reset, Revert, and Stash** as you would in a senior engineer interview.
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
- [Cherry-pick and Reflog](cherry-pick-and-reflog.md)



## References



- [git-reset](https://git-scm.com/docs/git-reset) · [git-revert](https://git-scm.com/docs/git-revert)
