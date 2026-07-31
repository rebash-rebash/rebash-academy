---
title: "Branching Fundamentals"
description: "Create and switch Git branches, understand HEAD, name branches for DevOps work, and follow safe branching practices."
difficulty: beginner
estimated_time: "40–55 min"
technology: git
category: git
module: "Module 5 · Branching"
career_paths:
  - beginner
  - devops-engineer
  - platform-engineer
skills:
  - git
  - branching
prerequisites:
  - git/gitignore-and-gitattributes
next:
  - git/merging-and-merge-conflicts
related:
  - git/production-git-practices
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - git
  - branches
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Branching Fundamentals

## Overview

Create, switch, and list branches confidently, explain HEAD, and apply naming conventions used in Cloud/DevOps teams.

Branches isolate change. Protected `main` plus short-lived `feature/*` or `fix/*` branches is the default for GitHub Flow.

This is a core tutorial in **Module 5 · Branching** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [gitignore and gitattributes](gitignore-and-gitattributes.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Create/switch branches (`switch`/`checkout`)  
- [ ] Explain HEAD  
- [ ] Name branches consistently  
- [ ] List and delete local branches safely

## Architecture

This topic’s control points and relationships are shown below.

![Branching strategy](../assets/excalidraw/git-branching-strategy.svg)

## Theory

### What

A **branch** is a movable pointer to a commit. Creating a branch does not copy files; it creates a new name for a commit ID. **HEAD** usually points at a branch name; when it points at a raw commit you are in **detached HEAD**. Day-to-day work uses `git switch` (and `git switch -c`) rather than older `checkout` habits.

### Why

Branches isolate experiments, features, and hotfixes without disturbing `main`. Short-lived branches plus pull requests are the default DevOps collaboration model. Long-lived branches exist for release maintenance but raise merge cost — use them deliberately.

### How it works

`git switch -c feature/add-healthcheck` creates a branch at the current commit and checks it out. New commits advance that branch pointer only. `git branch -vv` shows local branches and their upstream tracking. Remote-tracking branches such as `origin/main` are updated by `fetch`. Naming conventions (`feature/…`, `fix/…`, `hotfix/…`, `chore/…`, often with ticket IDs) make automation and CODEOWNERS routing easier.

```bash
git switch -c feature/add-healthcheck
git switch main
git branch -vv
```

### Key concepts

| Idea | Detail |
|------|--------|
| Branch = pointer | Cheap to create and delete |
| Upstream | Local branch linked to `origin/…` |
| Detached HEAD | HEAD points at a commit, not a branch |
| Default branch | Usually `main`; protect it on the host |

Delete merged local branches with `git branch -d`; prune remote-tracking names after fetch with prune enabled.

### Common pitfalls

- Doing real work in detached HEAD and “losing” commits (recover via reflog)  
- Reusing vague names like `fix` or `update` across tickets  
- Letting feature branches live for weeks against a moving `main`  
- Force-deleting (`-D`) shared branches without team agreement

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-05 && cd ~/rebash-git/module-05
```

**Focus:** hands-on practice for Branching Fundamentals

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Branching Fundamentals"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-git/module-05 && cd ~/rebash-git/module-05
git init -b main
git config user.email "lab@rebash.local"; git config user.name "REBASH Lab"
echo base > README.md && git add README.md && git commit -m "chore: init"

git switch -c feature/demo
echo work > app.txt && git add app.txt && git commit -m "feat: add app.txt"
git switch main
git log --oneline --all --graph
git branch
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-git/module-05/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Branching Fundamentals** always combines:

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

!!! warning "Doing real work in detached HEAD and “losing” commits (recover via reflog)  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Reusing vague names like `fix` or `update` across tickets  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Branching Fundamentals changes as code and review them in pull requests
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

**Branching Fundamentals** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Branching Fundamentals** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Merging and Merge Conflicts](merging-and-merge-conflicts.md)

## References

- [Pro Git — Branching](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
