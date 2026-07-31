---
title: "Merging and Merge Conflicts"
description: "Perform fast-forward and three-way merges, resolve conflicts safely, and choose merge strategies for DevOps repositories."
difficulty: intermediate
estimated_time: "45–60 min"
technology: git
category: git
module: "Module 6 · Merging"
career_paths:
  - beginner
  - devops-engineer
  - platform-engineer
skills:
  - git
  - merge
  - conflicts
prerequisites:
  - git/branching-fundamentals
next:
  - git/rebasing-and-interactive-rebase
related:
  - git/pull-requests-and-code-review
  - git/git-troubleshooting
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - git
  - merge
  - conflicts
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Merging and Merge Conflicts

## Overview

Merge branches with fast-forward and three-way merges, resolve a conflict deliberately, and abort cleanly when needed.

Merges integrate history. Conflicts are normal — resolve with intent, test, then commit.

This is a core tutorial in **Module 6 · Merging** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Branching Fundamentals](branching-fundamentals.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Fast-forward vs three-way merge  
- [ ] Resolve conflict markers  
- [ ] Use `merge --abort`  
- [ ] Prefer PR merges in teams

## Architecture

This topic’s control points and relationships are shown below.

![Merge process](../assets/excalidraw/git-merge-process.svg)

## Theory

### What

**Merging** joins histories. A **fast-forward** move happens when your branch tip is a direct ancestor of the other — Git simply advances the pointer. When histories **diverged**, Git performs a **three-way merge** using the merge base and may create a merge commit. Overlapping edits produce **conflicts** you must resolve in the working tree.

### Why

Teams need a controlled way to integrate feature work into `main`. Understanding fast-forward versus merge commits explains why pull request settings matter (merge commit, squash, or rebase-and-merge). Conflict literacy is mandatory for Infrastructure as Code (IaC), where the same YAML keys often change on parallel branches.

### How it works

Git finds the best common ancestor (merge base), compares both tips to that base, and applies combined changes. Non-overlapping hunks auto-merge. Conflicting regions are marked with conflict markers; you edit, `git add`, then `git merge --continue` (or commit). Abort with `git merge --abort` if needed. Default strategy on modern Git is `ort`; ours/theirs strategies exist but are easy to misuse on whole-tree “wins”.

| Outcome | Meaning |
|---------|---------|
| Fast-forward | Pointer moves; no merge commit |
| Merge commit | Two parents; histories joined |
| Squash merge | Hosting UI folds commits into one on target |
| Conflict | Manual resolution required |

### Key concepts

- **Merge base** — shared ancestor used for three-way merge  
- **Conflict markers** — `<<<<<<<`, `=======`, `>>>>>>>`  
- **Ours/theirs** — depend on merge vs rebase direction; verify before trusting  
- **CI after merge** — green on the branch is not always green on `main`  

### Common pitfalls

- Resolving conflicts by blindly taking “theirs” on Terraform without reading  
- Leaving conflict markers in committed files  
- Merging broken WIP into `main` to “deal with it later”  
- Using ours/theirs strategies to hide real design disagreements

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-06 && cd ~/rebash-git/module-06
```

**Focus:** hands-on practice for Merging and Merge Conflicts

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-git/module-06 && cd ~/rebash-git/module-06
git init -b main
git config user.email "lab@rebash.local"; git config user.name "REBASH Lab"
echo 'v1' > cfg.txt && git add cfg.txt && git commit -m "chore: v1"

git switch -c feature/conflict
echo 'feature' > cfg.txt && git add cfg.txt && git commit -m "feat: feature edit"

git switch main
echo 'mainline' > cfg.txt && git add cfg.txt && git commit -m "fix: main edit"

git merge feature/conflict || true
# resolve:
cat > cfg.txt << 'EOF'
resolved
EOF
git add cfg.txt
git commit -m "merge: resolve cfg.txt"
git log --oneline --graph
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-git/module-06/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Merging and Merge Conflicts** always combines:

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

!!! warning "Resolving conflicts by blindly taking “theirs” on Terraform without reading  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Leaving conflict markers in committed files  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Merging and Merge Conflicts changes as code and review them in pull requests
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

**Merging and Merge Conflicts** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Merging and Merge Conflicts** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Rebasing and Interactive Rebase](rebasing-and-interactive-rebase.md)

## References

- [Pro Git — Basic Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
