---
title: "Production Git Practices"
description: "Adopt production Git standards — trunk-based or GitHub Flow, protected main, conventional commits, CODEOWNERS, and operational hygiene for DevOps teams."
difficulty: advanced
estimated_time: "50–70 min"
technology: git
category: git
module: "Module 17 · Production Git Practices"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - cloud-engineer
skills:
  - git
  - github
  - gitops
  - production-practices
prerequisites:
  - git/git-bisect-and-debugging-history
  - git/gitops-fundamentals
next:
  - git/advanced-git-workflows
related:
  - git/pull-requests-and-code-review
  - git/github-actions-for-devops
  - git/signed-commits-and-git-security
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
  - GitHub Actions
tags:
  - git
  - production
  - github-flow
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Production Git Practices

## Overview






Define a team-ready Git operating model: branching strategy, protected `main`, PR quality bar, release tags, and GitOps-friendly repo layout.

Production Git is less about clever commands and more about **defaults that keep delivery safe**: short-lived branches, required checks, signed commits where policy demands, and IaC/GitOps paths owned by the right teams.

This is a core tutorial in **Module 17 · Production Git Practices** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites






- Modules 9–16 (GitHub through troubleshooting)
- [GitOps Fundamentals](gitops-fundamentals.md)

## Learning Objectives






By the end of this tutorial, you will be able to:

- [ ] Choose GitHub Flow / trunk-based vs long-lived release branches  
- [ ] Document branch protection and required checks  
- [ ] Apply conventional commit messages for changelogs  
- [ ] Assemble a production readiness checklist for a repo  
- [ ] Know when not to rewrite shared history

## Architecture






This topic’s control points and relationships are shown below.

![Branching strategy](../assets/excalidraw/git-branching-strategy.svg)

## Theory






### What

**Production Git practices** are the conventions that keep shared history safe: branching model, protection rules, secret hygiene, CI gates, ownership, and rollback strategy. They turn individual Git skill into a reliable delivery system for Cloud and DevOps teams.

### Why

A single force-push to `main` or a committed cloud key can outage or breach more than any fancy rebase skill can save. Agreeing defaults — usually trunk-based or GitHub Flow — reduces ceremony while preserving auditability. Practices must match reality: long-lived release branches are valid when you patch older versions in the field, but they need documented merge-back of hotfixes.

### How it works

Most product teams keep **`main` always deployable**, use short-lived feature branches, merge via pull request, and tag releases. CI must pass before merge. CODEOWNERS covers critical paths such as `prod/` and `terraform/`. Rollback is a revert commit and/or redeploy of a previous tag that GitOps reconciles. Secrets never enter Git; scanning and push protection backstop humans. Force-push to default branches is forbidden.

### Key concepts

| Practice | Default stance |
|----------|----------------|
| Branching | GitHub Flow / trunk-based |
| Release branches | Only when supporting old lines |
| Force-push to `main` | Forbidden |
| Secrets in Git | Never |
| CI before merge | Required |
| Rollback | Revert and/or previous tag |

### Common pitfalls

- “We will add branch protection later” on repos that already deploy  
- Hotfixing only on a release branch and forgetting to merge back to `main`  
- Equating green CI on a stale branch with safe merge to a moved `main`  
- Using personal forks as the production source of truth

## Hands-on Lab



### Objective

Complete a real Git workflow for **Production Git Practices** with commits you can inspect and recover.

### Prerequisites

- Git 2.x installed

### Lab environment

Workspace: `~/rebash-git/module-17`

Local Git repository only (no required remote).

```bash
mkdir -p ~/rebash-git/module-17 && cd ~/rebash-git/module-17
```

### Real-world scenario

A delivery team is standardising **Production Git Practices**. You prototype the workflow in a throwaway repo and capture log evidence for the playbook.

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






- [ ] Lab commands run under `~/rebash-git/module-17/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough






Production practice for **Production Git Practices** always combines:

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






!!! warning "“We will add branch protection later” on repos that already deploy  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Hotfixing only on a release branch and forgetting to merge back to `main`  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices






- Encode Production Git Practices changes as code and review them in pull requests
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






You can stand up a repository that matches how Cloud and DevOps teams ship: protected trunk, automated checks, clear ownership, and GitOps-friendly history.

## Interview Questions




1. List branch protection settings you enable on main.
2. How do you handle hotfixes under protected branches?
3. Why ban force-push on production branches?
4. What audit trail should a production change leave in git?
5. How do you onboard contractors with least privilege?

!!! tip "Sample answer — question 2"
    Confirm protection rules, required checks, and that the merge used the expected strategy.

!!! tip "Sample answer — question 4"
    Enforce SSO, 2FA, CODEOWNERS on sensitive paths, and short-lived access.

## Related Tutorials






- [Course overview](index.md)
- - Related depth: [Advanced Git Workflows](advanced-git-workflows.md) · [Git Hooks](git-hooks-and-automation.md)  
- Capstone ideas on the [course overview](index.md)

## References






- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)  
- [Conventional Commits](https://www.conventionalcommits.org/)
