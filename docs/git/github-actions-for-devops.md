---
title: "GitHub Actions for DevOps"
description: "Build CI workflows with GitHub Actions — checkout, runners, secrets, and a DevOps pipeline skeleton for Git repositories."
difficulty: intermediate
estimated_time: "50–70 min"
technology: git
category: git
module: "Module 11 · GitHub Actions"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - github-actions
  - ci-cd
  - git
prerequisites:
  - git/pull-requests-and-code-review
next:
  - git/gitops-fundamentals
related:
  - git/git-in-ci-cd
  - github-actions/index
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Actions
tags:
  - github-actions
  - ci
  - git
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# GitHub Actions for DevOps

## Overview






Author a minimal GitHub Actions workflow that runs on pull requests: checkout, validate, and report status — the CI gate for Git-based delivery.

**GitHub Actions** runs workflows on events (`push`, `pull_request`). Jobs use runners; secrets never belong in Git history.

This is a core tutorial in **Module 11 · GitHub Actions** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites






- [Pull Requests and Code Review](pull-requests-and-code-review.md)
- GitHub repository with Actions enabled

## Learning Objectives






By the end of this tutorial, you will be able to:

- [ ] Structure `.github/workflows/*.yml`  
- [ ] Use `actions/checkout`  
- [ ] Gate PRs with required checks  
- [ ] Store secrets in repository settings (not in Git)  
- [ ] Distinguish workflow vs job vs step

## Architecture






This topic’s control points and relationships are shown below.

![GitHub Actions flow](../assets/excalidraw/git-github-actions.svg)

## Theory






### What

**GitHub Actions** is CI/CD built into GitHub. A **workflow** is a YAML file under `.github/workflows/` triggered by events (push, pull_request, schedule, workflow_dispatch). Workflows contain **jobs** that run on **runners**; jobs contain **steps** that execute shell commands or reusable **actions**. **Secrets** inject sensitive values at runtime.

### Why

DevOps pipelines should live next to the code they validate. Actions can lint Terraform, build container images, run tests, and deploy — with permissions tied to the repository. Understanding workflow structure prevents insecure `pull_request_target` mistakes and overly privileged tokens.

### How it works

On a matching event, GitHub schedules jobs. Jobs run in parallel unless `needs:` creates a dependency graph. Steps share a workspace on the runner. The expression syntax uses double curly braces — in MkDocs/Jinja documentation you must escape them. Example pattern for docs: {% raw %}`${{ secrets.NAME }}`{% endraw %} or `{{ "{{" }} secrets.NAME {{ "}}" }}`. Third-party actions should be pinned by commit SHA when policy requires supply-chain caution. Environments and OIDC cloud login replace long-lived cloud keys.

| Concept | Meaning |
|---------|---------|
| Workflow | YAML triggered by events |
| Job | Unit of work on a runner |
| Step | Shell or action |
| Secret | Encrypted value injected at runtime |

### Key concepts

- **Least privilege** — `permissions:` at workflow/job level  
- **Fork PRs** — secrets usually unavailable; never blindly trust PR code with privileged workflows  
- **Caching and artefacts** — speed builds without hiding non-determinism  
- **Reusable workflows** — share org standards  

### Common pitfalls

- Logging secrets with `echo`  
- Using latest floating action tags in production  
- Over-broad `write` repository tokens on every job  
- Skipping status checks that the branch protection was meant to enforce

## Hands-on Lab



### Objective

Complete a real Git workflow for **GitHub Actions for DevOps** with commits you can inspect and recover.

### Prerequisites

- Git 2.x installed

### Lab environment

Workspace: `~/rebash-git/module-11/.github/workflows`

Local Git repository only (no required remote).

```bash
mkdir -p ~/rebash-git/module-11/.github/workflows && cd ~/rebash-git/module-11/.github/workflows
```

### Real-world scenario

A delivery team is standardising **GitHub Actions for DevOps**. You prototype the workflow in a throwaway repo and capture log evidence for the playbook.

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






- [ ] Lab commands run under `~/rebash-git/module-11/.github/workflows/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough






Production practice for **GitHub Actions for DevOps** always combines:

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






!!! warning "Logging secrets with `echo`  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Using latest floating action tags in production  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices






- Encode GitHub Actions for DevOps changes as code and review them in pull requests
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






**GitHub Actions for DevOps** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions




1. How does a git push start CI on GitHub?
2. Why keep workflow YAML in the same repo as code?
3. What permissions should a basic CI workflow use?
4. How do required status checks relate to branch protection?
5. Where do you look when CI is green but deploy failed?

!!! tip "Sample answer — question 2"
    Open the Actions run for the commit SHA and confirm the workflow file path. Required checks must match actual job names.

!!! tip "Sample answer — question 4"
    Least-privilege permissions, pinned actions, and no secrets in forks.

## Related Tutorials






- [Course overview](index.md)
- [GitOps Fundamentals](gitops-fundamentals.md)
- Deeper track: [GitHub Actions](../github-actions/index.md)

## References






- [GitHub Actions documentation](https://docs.github.com/en/actions)
