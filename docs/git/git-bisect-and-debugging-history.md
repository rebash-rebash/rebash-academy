---
title: "Git Bisect and Debugging History"
description: "Use git bisect to find the commit that introduced a bug, and read history with blame and pickaxe searches for DevOps debugging."
difficulty: advanced
estimated_time: "40–55 min"
technology: git
category: git
module: "Module 16 · Troubleshooting"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - git
  - bisect
  - debugging
prerequisites:
  - git/git-troubleshooting
next:
  - git/production-git-practices
related:
  - git/viewing-history-and-diffs
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - git
  - bisect
  - blame
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Git Bisect and Debugging History

## Overview






Run `git bisect` to binary-search history for the first bad commit, and use `blame` / pickaxe (`-S`) when you know the change shape.

When “it worked last week,” bisect beats scrolling `git log`. Mark a known good and known bad commit; Git checks out midpoints until the culprit is found.

This is a core tutorial in **Module 16 · Troubleshooting** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites






- [Git Troubleshooting](git-troubleshooting.md)

## Learning Objectives






By the end of this tutorial, you will be able to:

- [ ] Start/end a bisect session  
- [ ] Automate with `git bisect run` when a script returns exit codes  
- [ ] Use `git blame` for line ownership  
- [ ] Search history with `git log -S`

## Architecture






This topic’s control points and relationships are shown below.

![Object model / history](../assets/excalidraw/git-object-model.svg)

## Theory






### What

`git bisect` performs a binary search across history to find the commit that introduced a bug. You mark a known **good** revision and a known **bad** revision; Git checks out midpoints until the first bad commit remains. Automation uses a script that exits `0` for good and non-zero for bad.

### Why

Linear “guess and rebuild” wastes hours on long histories. Bisect is ideal for regressions in pipelines, Terraform modules, or application behaviour when you can test each checkout quickly. It turns vague “it broke last month” into a precise SHA for revert or fix-forward.

### How it works

Start with a clean working tree: `git bisect start`, `git bisect bad` (current), `git bisect good <oldsha>`. Git picks a midpoint commit; you run your test and mark `good` or `bad` (or `skip` if untestable). Repeat until Git prints the culprit. `git bisect reset` returns you to the original branch. Scripted mode: `git bisect run ./test.sh` drives the loop. Avoid committing new fixes mid-bisect unless you know you are branching off a midpoint on purpose.

### Key concepts

| Need | Detail |
|------|--------|
| Reproducible test | Same input → same exit code |
| Clean tree | Dirty files confuse results |
| Skip | Untestable commits (broken build mid-range) |
| Outcome | First bad commit SHA |


Prepare a script that builds or configures just enough to reproduce the failure — for example a targeted pytest, a `terraform validate`, or a curl against a local binary. If old commits need different tool versions, document that limitation and skip those revisions rather than marking them randomly. Once you find the culprit, write a regression test so bisect is unnecessary next time.

### Common pitfalls

- Using flaky tests that randomly mark good/bad  
- Bisecting without enough disk/tooling for old revisions  
- Forgetting `bisect reset` and staying on a detached midpoint  
- Marking the newest commit good by mistake and getting nonsense ranges

## Hands-on Lab



### Objective

Complete a real Git workflow for **Git Bisect and Debugging History** with commits you can inspect and recover.

### Prerequisites

- Git 2.x installed

### Lab environment

Workspace: `~/rebash-git/module-16-bisect`

Local Git repository only (no required remote).

```bash
mkdir -p ~/rebash-git/module-16-bisect && cd ~/rebash-git/module-16-bisect
```

### Real-world scenario

A delivery team is standardising **Git Bisect and Debugging History**. You prototype the workflow in a throwaway repo and capture log evidence for the playbook.

### Step-by-step tasks

#### Task 1 – Initialise a repository and first commit

Every production change starts as a commit with clear identity config.

```bash
git init -b main
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
echo '# lab' > README.md
git add README.md
git commit -m 'Initial commit'
git log --oneline | tee log.txt
```

**Expected output:** log.txt shows the initial commit on `main`.

#### Task 2 – Inspect status and diff discipline

Clean working trees prevent accidental commits of secrets.

```bash
echo 'work' > work.txt
git status
git add work.txt
git commit -m 'Add work.txt'
git show --stat HEAD | tee show.txt
```

**Expected output:** show.txt lists work.txt in the commit.

### Validation steps

- [ ] Repository has at least two commits or a merge as designed
- [ ] log/graph evidence files exist

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Author identity unknown | Missing user.name/email | Set local `git config user.*` as in Task 1 |
| merge conflict | Overlapping edits | Edit file, `git add`, complete merge |
| detached HEAD | Checked out a raw SHA | `git switch -c` a branch before committing |

### Challenge exercise

Use `git reflog` to recover a commit after a hard reset on a private branch.

### Learning outcomes

- Performed real Git operations
- Left auditable history
- Understood recovery basics

### Cleanup

```bash
# Safe local repo — delete the lab directory when finished:
# rm -rf "$(pwd)"
```

## Validation






- [ ] Lab commands run under `~/rebash-git/module-16-bisect/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough






Production practice for **Git Bisect and Debugging History** always combines:

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






!!! warning "Using flaky tests that randomly mark good/bad  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Bisecting without enough disk/tooling for old revisions  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices






- Encode Git Bisect and Debugging History changes as code and review them in pull requests
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






**Git Bisect and Debugging History** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions




1. How does bisect find a bad commit?
2. What makes a good automated bisect run script?
3. Limitations of bisect with flaky tests?
4. How do you mark skip commits?
5. What do you do after bisect names a commit?

!!! tip "Sample answer — question 2"
    Ensure you can script a deterministic good/bad test, then git bisect reset after collecting the SHA.

!!! tip "Sample answer — question 4"
    Do not bisect on production data stores. Keep repro scripts free of credentials.

## Related Tutorials






- [Course overview](index.md)
- [Production Git Practices](production-git-practices.md)

## References






- [git-bisect](https://git-scm.com/docs/git-bisect)
