---
title: "Rebasing and Interactive Rebase"
description: "Rebase branches cleanly, squash with interactive rebase, and know when not to rebase shared history in DevOps teams."
difficulty: intermediate
estimated_time: "45–60 min"
technology: git
category: git
module: "Module 7 · Rebasing & History"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - git
  - rebase
prerequisites:
  - git/merging-and-merge-conflicts
next:
  - git/undoing-changes-reset-revert-stash
related:
  - git/cherry-pick-and-reflog
  - git/production-git-practices
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - git
  - rebase
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Rebasing and Interactive Rebase

## Overview




Rebase a feature onto `main`, squash commits interactively, and follow the rule: do not rebase commits already pushed to shared branches without coordination.

Rebase replays commits onto a new base — cleaner linear history, **new SHAs**. Use on local feature branches; prefer merge commits on protected `main` via PR settings.

This is a core tutorial in **Module 7 · Rebasing & History** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites




- [Merging and Merge Conflicts](merging-and-merge-conflicts.md)



## Learning Objectives




By the end of this tutorial, you will be able to:

- [ ] `git rebase main` on a feature branch  
- [ ] Interactive squash (`rebase -i`)  
- [ ] Abort a rebase  
- [ ] State the shared-history rule



## Architecture




This topic’s control points and relationships are shown below.

![Merge/rebase process](../assets/excalidraw/git-merge-process.svg)



## Theory




### What

**Rebase** replays your commits onto a new base tip, rewriting commit IDs into a linear history. **Interactive rebase** (`git rebase -i`) lets you reorder, squash, reword, or drop commits before sharing. Rebase is a history-editing tool, not a synonym for merge.

### Why

Teams rebase feature branches onto `origin/main` to reduce noisy merge commits and make review diffs cleaner. Interactive rebase tidies “fix typo” commits before a pull request. The cost is rewritten SHAs — anyone else who based work on the old commits must recover carefully.

### How it works

You check out the feature branch, fetch, then `git rebase origin/main`. Git detaches HEAD at the new base and replays each commit as a patch. Conflicts pause the rebase; fix files, `git add`, then `git rebase --continue`, or `git rebase --abort`. Interactive mode opens an editor with `pick`/`squash`/`reword` lines for a commit range such as `HEAD~3`.

```bash
git switch feature/x
git fetch origin
git rebase origin/main
git rebase -i HEAD~3
git rebase --abort
```

### Key concepts

| Practice | Guidance |
|----------|----------|
| Rebase feature onto main | Common before merge |
| Rebase shared `main` | Almost never — coordinate as an incident |
| Squash via `-i` | Clean PR story |
| `--force-with-lease` | Safer than `--force` after rewriting a pushed branch |


After a successful rebase of a feature branch that was already pushed, update the remote with `git push --force-with-lease` so you do not overwrite newer commits another engineer pushed. Prefer rebase for cleaning *your* branch; prefer merge commits when you need to preserve exact integration history for audits.

### Common pitfalls

- Rewriting commits already on protected or shared branches  
- Continuing past conflicts without running tests  
- Confusing rebase “theirs/ours” with merge meanings  
- Using rebase to hide large unfinished work instead of splitting PRs



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-07 && cd ~/rebash-git/module-07
```

**Focus:** rebase a feature branch onto main and inspect reflog

### Step 1 – Create divergent history and rebase

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo base > app.txt
git add app.txt && git commit -m "chore: base"
git switch -c feature/x
echo feature >> app.txt
git add app.txt && git commit -m "feat: feature line"
git switch -
echo main >> app.txt
git add app.txt && git commit -m "fix: main line"
git switch feature/x
git rebase main
git log --oneline --graph --all -n 10
```

### Step 2 – Safety check with reflog

```bash
git reflog -n 10
git status
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```



## Validation




- [ ] Lab commands run under `~/rebash-git/module-07/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough




Production practice for **Rebasing and Interactive Rebase** always combines:

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




!!! warning "Rewriting commits already on protected or shared branches  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Continuing past conflicts without running tests  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices




- Encode Rebasing and Interactive Rebase changes as code and review them in pull requests
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




**Rebasing and Interactive Rebase** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. What does rebase rewrite, and when is that dangerous?
2. Golden rule of rebasing shared history?
3. Interactive rebase uses — squash/fixup/edit/reword?
4. How do you abort a painful rebase?
5. Rebase versus merge for feature branches?

!!! tip "Sample answer — question 2"
    If conflicts explode, git rebase --abort returns you to the pre-rebase state. Use reflog if you already completed a bad rebase.

!!! tip "Sample answer — question 4"
    Do not rebase commits already pushed to shared branches without team agreement.



## Related Tutorials




- [Course overview](index.md)
- [Undoing Changes — Reset, Revert, and Stash](undoing-changes-reset-revert-stash.md)



## References




- [Pro Git — Rewriting History](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)
