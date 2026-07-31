---
title: "Git Troubleshooting"
description: "Diagnose common Git failures — detached HEAD, divergent branches, rejected pushes, corrupted index, and permission issues — with a DevOps recovery playbook."
difficulty: intermediate
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
  - troubleshooting
prerequisites:
  - git/signed-commits-and-git-security
  - git/cherry-pick-and-reflog
next:
  - git/git-bisect-and-debugging-history
related:
  - git/undoing-changes-reset-revert-stash
  - git/working-with-remotes
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - git
  - troubleshooting
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Git Troubleshooting

## Overview



Diagnose the most common Git failure modes in delivery work and recover without destroying shared history.

Most “Git is broken” moments are state problems: wrong branch, dirty tree, divergent remotes, or detached HEAD. Read status and reflog before rewriting.

This is a core tutorial in **Module 16 · Troubleshooting** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Signed Commits and Git Security](signed-commits-and-git-security.md)
- [Cherry-pick and Reflog](cherry-pick-and-reflog.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Read `git status` / `git remote -v` under pressure  
- [ ] Fix detached HEAD  
- [ ] Recover from rejected non-fast-forward push  
- [ ] Clear a stuck merge/rebase  
- [ ] Use reflog when commits “disappear”



## Architecture



This topic’s control points and relationships are shown below.

![Git workflow](../assets/excalidraw/git-workflow.svg)



## Theory



### What

Git troubleshooting is systematic diagnosis of pointer, conflict, auth, and sync problems. Symptoms look scary (“detached HEAD”, “rejected non-fast-forward”, “unmerged paths”); causes are usually a small set of state mismatches between working tree, index, HEAD, and remotes.

### Why

Panic resets make outages worse. A calm first move — read `status`, `reflog`, and remote tips — recovers work without rewriting shared history. Platform engineers are expected to unblock colleagues safely.

### How it works

Start with `git status` to learn whether a merge/rebase/cherry-pick is in progress. Use `git reflog` when commits seem missing after reset or rebase. For push rejections, `git fetch` then integrate with rebase or merge — do not force-push protected branches. Auth failures need `ssh -T` or credential helper checks, not repository surgery. Detached HEAD after checking out a tag is normal for inspection; create a branch before committing.

| Symptom | Likely cause | First move |
|---------|--------------|------------|
| Detached HEAD | Checked out a SHA/tag | `git switch -c fix/…` or `git switch main` |
| Push rejected | Remote ahead | `fetch` then rebase/merge |
| Merge in progress | Unfinished merge | resolve + `--continue` or `--abort` |
| Rebase conflict | Overlapping edits | fix → `--continue` or `--abort` |
| “Lost” commit | Reset/rebase | `git reflog` |
| Permission denied (publickey) | SSH key / agent | `ssh -T git@github.com` |

### Key concepts

- **Abort vs continue** — know how to leave conflicted states cleanly  
- **Remote ahead/behind** — read `branch -vv` before pushing  
- **Local-only tools** — reflog does not exist on the server as your laptop’s history  
- **Protection rules** — “broken Git” is sometimes intentional policy  

### Common pitfalls

- `reset --hard` on shared `main` to fix a laptop problem  
- Deleting `.git` to “start over” and losing unpushed work  
- Force-push without `--force-with-lease`  
- Ignoring in-progress merge/rebase markers and making new commits on top



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-16 && cd ~/rebash-git/module-16
```

**Focus:** practise Git skills for: Git Troubleshooting

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

### Step 2 – Diagnose divergence

```bash
git switch -c other
echo o > o.txt && git add o.txt && git commit -m 'other'
git switch main
echo m2 > m2.txt && git add m2.txt && git commit -m 'm2'
git merge other || true
git status | tee status.txt
git log --oneline --graph --all | tee graph.txt
```

### Final step – Cleanup note

```bash
# Safe local repo under the lab directory; delete the folder when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-git/module-16/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Git Troubleshooting** always combines:

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



!!! warning "`reset --hard` on shared `main` to fix a laptop problem  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Deleting `.git` to “start over” and losing unpushed work  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Git Troubleshooting changes as code and review them in pull requests
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



**Git Troubleshooting** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. Explain **Git Troubleshooting** as you would in a senior engineer interview.
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
- [Git Bisect and Debugging History](git-bisect-and-debugging-history.md)



## References



- [Git FAQ — undoing](https://git-scm.com/docs/gitfaq#_undoing)
