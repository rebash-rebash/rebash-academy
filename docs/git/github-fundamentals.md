---
title: "GitHub Fundamentals"
description: "Navigate GitHub repositories, settings, Issues, Discussions, Wikis, and Releases for Cloud and DevOps collaboration."
difficulty: beginner
estimated_time: "35–50 min"
technology: git
category: git
module: "Module 9 · GitHub Fundamentals"
career_paths:
  - beginner
  - devops-engineer
  - platform-engineer
skills:
  - github
  - git
prerequisites:
  - git/working-with-remotes
next:
  - git/pull-requests-and-code-review
related:
  - git/github-actions-for-devops
  - git/repository-management-and-releases
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - github
  - git
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# GitHub Fundamentals

## Overview



Use GitHub as the collaboration hub: repos, settings, Issues, Releases — and know where security and Actions settings live.

Git is the tool; **GitHub** (or GitLab) is where teams review, track work, and ship. DevOps owns templates, permissions, and release artefacts.

This is a core tutorial in **Module 9 · GitHub Fundamentals** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Working with Remotes](working-with-remotes.md)
- GitHub account (free tier OK)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Create/configure a repository  
- [ ] Distinguish Issues vs Discussions  
- [ ] Find Settings → Branches / Actions / Secrets  
- [ ] Publish a Release from a tag  
- [ ] Use Wikis carefully (prefer docs-as-code in-repo)



## Architecture



This topic’s control points and relationships are shown below.

![PR lifecycle](../assets/excalidraw/git-pr-lifecycle.svg)



## Theory



### What

**GitHub** hosts Git repositories and adds collaboration features: issues, pull requests, Discussions, Releases, Actions, Packages, and organisation security controls. For DevOps, a GitHub repository is often the home of application code, Infrastructure as Code (IaC), and workflow definitions together.

### Why

Raw Git has no built-in code review UI, permissions model, or CI. GitHub (or GitLab/Bitbucket) supplies those. Learning the product surface — especially settings for the default branch, Actions, and secret scanning — is part of professional Git practice, not optional polish.

### How it works

Repositories live under a user or organisation. The **default branch** (usually `main`) is what clones check out. Issues track work; Releases attach notes and artefacts to Git tags; Settings control collaborators, branch protection, and integrations. Authentication uses SSH keys, personal access tokens (PATs), or GitHub Apps / OIDC for automation. Fine-grained PATs and least-privilege App permissions reduce blast radius compared with classic tokens.

| Feature | Ops use |
|---------|---------|
| Repositories | Code + IaC |
| Issues | Work tracking, incident links |
| Discussions | Open Q&A (optional) |
| Releases | Versioned artefacts and notes |
| Settings | Protection, access, Actions |

### Key concepts

- **Organisation vs user repos** — prefer org ownership for production systems  
- **Visibility** — private by default for internal infra  
- **Secret scanning / push protection** — enable where available  
- **Topics and README** — discoverability for platform teams  

### Common pitfalls

- Personal forks as the only copy of production IaC  
- Classic PATs with broad `repo` scope checked into CI logs  
- Leaving Actions enabled on repos that should not run untrusted workflows  
- Ignoring organisation-required two-factor authentication (2FA)



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-09 && cd ~/rebash-git/module-09
```

**Focus:** practise Git skills for: GitHub Fundamentals

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

### Step 2 – GitHub collaboration notes

```bash
tee github-notes.txt << 'EOF'
Issues + PRs + Actions form the collaboration loop.
Protect default branch; use CODEOWNERS for critical paths.
EOF
mkdir -p .github
echo '* @platform-team' > .github/CODEOWNERS
git add .github github-notes.txt
git commit -m 'Add CODEOWNERS scaffold'
cat github-notes.txt
```

### Final step – Cleanup note

```bash
# Safe local repo under the lab directory; delete the folder when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-git/module-09/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **GitHub Fundamentals** always combines:

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



!!! warning "Personal forks as the only copy of production IaC  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Classic PATs with broad `repo` scope checked into CI logs  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode GitHub Fundamentals changes as code and review them in pull requests
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



**GitHub Fundamentals** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. Explain **GitHub Fundamentals** as you would in a senior engineer interview.
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
- [Pull Requests and Code Review](pull-requests-and-code-review.md)



## References



- [GitHub Docs — Repositories](https://docs.github.com/en/repositories)
