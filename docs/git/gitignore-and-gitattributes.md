---
title: "Working with Repositories — gitignore and gitattributes"
description: "Control tracking with .gitignore and .gitattributes — keep secrets and build artefacts out of Git, and set attributes for DevOps repos."
difficulty: beginner
estimated_time: "30–45 min"
technology: git
category: git
module: "Module 4 · Working with Repositories"
career_paths:
  - beginner
  - devops-engineer
  - platform-engineer
skills:
  - git
  - gitignore
  - gitattributes
prerequisites:
  - git/viewing-history-and-diffs
next:
  - git/branching-fundamentals
related:
  - git/signed-commits-and-git-security
  - python/configuration-management-and-secrets
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - git
  - gitignore
  - gitattributes
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Working with Repositories — gitignore and gitattributes

## Overview



Keep secrets, caches, and build outputs out of Git with `.gitignore`, understand `.git/` layout at a practical level, and set useful `.gitattributes`.

Tracked `.env` files and `node_modules` are classic incidents. Ignore early; use secret scanning in CI (Module 15).

This is a core tutorial in **Module 4 · Working with Repositories** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Viewing History and Diffs](viewing-history-and-diffs.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Write a solid `.gitignore` for ops repos  
- [ ] Explain tracking vs ignoring  
- [ ] Use `.gitattributes` for line endings / export  
- [ ] Know key `.git/` directories



## Architecture



This topic’s control points and relationships are shown below.

![Repository architecture](../assets/excalidraw/git-repository-architecture.svg)



## Theory



### What

`.gitignore` tells Git which untracked paths to skip. `.gitattributes` sets per-path attributes such as line endings, diff drivers, and “this is binary”. Together they keep repositories clean and cross-platform safe. The `.git` directory itself holds objects, refs, config, and hooks — you inspect it, you do not casually rewrite it.

### Why

Committed secrets, Terraform state, virtualenvs, and `node_modules` create security and size disasters. Mixed CRLF/LF endings cause noisy diffs on Windows and Linux teams. Attributes make line-ending policy explicit so CI and laptops agree.

### How it works

Ignore rules are path patterns, optionally scoped by directory. Patterns in `.gitignore` apply from that directory downward; global excludes exist but team rules belong in the repo. Already-tracked files are **not** ignored until removed from the index (`git rm --cached`). `git check-ignore -v path` explains which rule matched. Attributes use similar path matching: `text=auto`, `eol=lf`, and `binary` are common for DevOps repos full of shell and YAML.

```gitignore
.env
*.tfstate*
.terraform/
__pycache__/
.venv/
dist/
```

```gitattributes
* text=auto eol=lf
*.sh text eol=lf
*.png binary
```

### Key concepts

| Area | Practical note |
|------|----------------|
| `.git/objects` | Content-addressed store — do not hand-edit |
| `.git/refs` | Branch and tag pointers |
| Ignore vs untrack | Ignore only affects untracked files |
| Attributes | Normalise text; mark binaries |


For Infrastructure as Code (IaC) repositories, ignore rules are a security control as much as a cleanliness tip. Reviewers should reject pull requests that suddenly track state files or credential paths. When onboarding a language or tool, copy ignore patterns from a trusted organisational template rather than inventing them under deadline pressure.

### Common pitfalls

- Adding `.env` to ignore *after* committing it — secret remains in history  
- Ignoring `*.tf` by accident with an overly broad pattern  
- Fighting line endings without a committed `.gitattributes`  
- Committing `.terraform/` or provider plugins and bloating clones



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-04 && cd ~/rebash-git/module-04
```

**Focus:** practise Git skills for: Working with Repositories — gitignore and gitattributes

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

### Step 2 – gitignore

```bash
cat > .gitignore << 'EOF'
*.env
__pycache__/
.DS_Store
EOF
echo SECRET=1 > local.env
git status --ignored | tee status.txt
git check-ignore -v local.env
```

### Final step – Cleanup note

```bash
# Safe local repo under the lab directory; delete the folder when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-git/module-04/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Working with Repositories — gitignore and gitattributes** always combines:

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



!!! warning "Adding `.env` to ignore *after* committing it — secret remains in history  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Ignoring `*.tf` by accident with an overly broad pattern  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Working with Repositories — gitignore and gitattributes changes as code and review them in pull requests
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



**Working with Repositories — gitignore and gitattributes** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. Explain **Working with Repositories — gitignore and gitattributes** as you would in a senior engineer interview.
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
- [Branching Fundamentals](branching-fundamentals.md)



## References



- [gitignore](https://git-scm.com/docs/gitignore) · [gitattributes](https://git-scm.com/docs/gitattributes)
