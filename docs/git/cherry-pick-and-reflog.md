---
title: "Cherry-pick and Reflog"
description: "Cherry-pick commits onto another branch and recover work with reflog — essential DevOps recovery skills."
difficulty: intermediate
estimated_time: "35–50 min"
technology: git
category: git
module: "Module 7 · Rebasing & History"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - git
  - cherry-pick
  - reflog
prerequisites:
  - git/undoing-changes-reset-revert-stash
next:
  - git/working-with-remotes
related:
  - git/git-troubleshooting
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - git
  - cherry-pick
  - reflog
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Cherry-pick and Reflog

## Overview



Cherry-pick a hotfix commit onto another branch and use `reflog` to find a “lost” commit after a reset.

This is a core tutorial in **Module 7 · Rebasing & History** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Undoing Changes](undoing-changes-reset-revert-stash.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] `git cherry-pick <sha>`  
- [ ] Read `git reflog`  
- [ ] Recover a reset commit



## Architecture



This topic’s control points and relationships are shown below.

![Architecture diagram for Cherry-pick and Reflog](../assets/excalidraw/git-object-model.svg)



## Theory



### What

**Cherry-pick** copies the changes from an existing commit onto your current HEAD as a *new* commit (new SHA, usually same message/patch). **Reflog** is a local diary of where HEAD and branch tips pointed — a recovery tool after reset, rebase, or detached-HEAD mistakes.

### Why

Hotfixes sometimes land on a release branch and must be copied to `main` (or the reverse) without merging the whole branch. Reflog saves “lost” commits that still exist as objects after a bad reset. Together they are essential production safety nets.

### How it works

`git cherry-pick <sha>` applies that commit’s diff to the current tree and creates a new commit. Conflicts pause the operation like merge/rebase. Ranges and `-x` (note the source SHA in the message) appear in advanced workflows. Reflog entries live under `.git/logs` and expire eventually; `git reflog` then `git switch -c recover/<name> <sha>` resurrects work. Reflog is **not** pushed to remotes — recovery is per clone.

### Key concepts

| Tool | Mental model |
|------|----------------|
| Cherry-pick | Duplicate a patch as a new commit |
| Reflog | Local pointer history |
| GC grace | Objects linger until garbage collection |
| Duplicate commits | Same change, different SHAs after pick |


In release engineering, cherry-pick is common when a single fix must land on `main` and on a maintained release branch without merging unrelated commits. Document the source SHA in the commit message (or use `-x`) so future readers can see the lineage. Teach every on-call engineer `git reflog` before they need it in an incident.

### Common pitfalls

- Cherry-picking merge commits without understanding parent selection  
- Assuming reflog on a CI runner will save laptop mistakes  
- Cherry-picking large unrelated commits instead of merging/rebase  
- Waiting weeks to recover — expired reflog entries vanish



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-07-cherry && cd ~/rebash-git/module-07-cherry
```

**Focus:** practise Git skills for: Cherry-pick and Reflog

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

### Step 2 – Reflog recovery

```bash
echo x > x.txt && git add x.txt && git commit -m 'x'
git reset --hard HEAD~1
git reflog | tee reflog.txt
git checkout -b recovered HEAD@{1}
git log --oneline | tee recovered.txt
```

### Final step – Cleanup note

```bash
# Safe local repo under the lab directory; delete the folder when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-git/module-07-cherry/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Cherry-pick and Reflog** always combines:

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



!!! warning "Cherry-picking merge commits without understanding parent selection  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Assuming reflog on a CI runner will save laptop mistakes  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Cherry-pick and Reflog changes as code and review them in pull requests
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



**Cherry-pick and Reflog** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. Explain **Cherry-pick and Reflog** as you would in a senior engineer interview.
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
- [Working with Remotes](working-with-remotes.md)  
- [Git Troubleshooting](git-troubleshooting.md)



## References



- [git-cherry-pick](https://git-scm.com/docs/git-cherry-pick) · [git-reflog](https://git-scm.com/docs/git-reflog)
