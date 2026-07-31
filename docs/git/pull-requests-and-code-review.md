---
title: "Pull Requests and Code Review"
description: "Open pull requests, run code reviews, use branch protection and CODEOWNERS, and follow a DevOps-ready review process."
difficulty: intermediate
estimated_time: "40–55 min"
technology: git
category: git
module: "Module 10 · Collaboration"
career_paths:
  - beginner
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - github
  - pull-requests
  - code-review
prerequisites:
  - git/github-fundamentals
next:
  - git/github-actions-for-devops
related:
  - git/production-git-practices
  - git/signed-commits-and-git-security
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - github
  - pull-request
  - codeowners
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Pull Requests and Code Review

## Overview

Open a PR with a clear description, understand required reviews and CODEOWNERS, and review changes with an ops risk lens (secrets, blast radius, rollback).

PRs are the change-control gate for `main`. Branch protection + required checks beat informal “just push.”

This is a core tutorial in **Module 10 · Collaboration** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [GitHub Fundamentals](github-fundamentals.md)
- [Branching](branching-fundamentals.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Open a PR from a feature branch  
- [ ] Write review-friendly descriptions  
- [ ] Explain branch protection rules  
- [ ] Add a CODEOWNERS file  
- [ ] Review for security and operability

## Architecture

This topic’s control points and relationships are shown below.

![PR lifecycle](../assets/excalidraw/git-pr-lifecycle.svg)

## Theory

### What

A **pull request (PR)** proposes merging one branch into another (often `feature/…` into `main`) with discussion, commits, and CI status attached. **Code review** is the human (and bot) evaluation of that change for correctness, safety, and operability. **Branch protection** and **CODEOWNERS** encode merge policy in the hosting platform.

### Why

Direct pushes to `main` skip peer review and often skip CI. For Terraform, Kubernetes, and pipeline changes, review catches destructive applies, missing alarms, and leaked secrets before they reach production. PRs also leave an audit trail linking discussion to the exact commits deployed.

### How it works

You push a branch, open a PR, and reviewers comment on the diff. Required status checks (tests, lint, security scans) must pass when protection rules say so. CODEOWNERS maps paths such as `/terraform/` to teams that must approve. Reviewers focus on behaviour, tests, secrets, rollback, and monitoring — not only style. Merge strategies (merge commit, squash, rebase) reshape history on the target branch; pick one org standard.

**Branch protection (typical):** require PR, require status checks, dismiss stale reviews, restrict force-push.  
**CODEOWNERS:** auto-request reviewers by path.  
**Review lens:** correctness, tests, secrets, rollback, observability.

### Key concepts

| Control | Purpose |
|---------|---------|
| Required reviews | Human gate |
| Status checks | Automated gate |
| CODEOWNERS | Path-based expertise |
| Draft PRs | Work in progress without review pressure |


Write PR descriptions that state risk, test evidence, and rollback steps — especially for Terraform and Kubernetes changes. Small, focused pull requests merge faster and bisect more cleanly later. Bots can lint and scan, but humans still own blast-radius judgement for production infrastructure.

### Common pitfalls

- Rubber-stamp approvals without reading IaC blast radius  
- Enormous PRs that nobody can review carefully  
- Merging with failing optional checks that were actually important  
- Rewriting PR history mid-review without warning reviewers

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-10 && cd ~/rebash-git/module-10
```

**Focus:** hands-on practice for Pull Requests and Code Review

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-git/module-10 && cd ~/rebash-git/module-10
git init -b main
git config user.email "lab@rebash.local"; git config user.name "REBASH Lab"
echo '# app' > README.md && git add README.md && git commit -m "chore: init"
mkdir -p .github
cat > .github/CODEOWNERS << 'EOF'
* @your-org/platform
/terraform/ @your-org/infra
EOF
git add .github/CODEOWNERS && git commit -m "chore: add CODEOWNERS"
git switch -c feature/docs
echo 'note' >> README.md && git commit -am "docs: add note"
# Push and open PR on GitHub when remote exists
cat > pr-body.md << 'EOF'

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-git/module-10/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Pull Requests and Code Review** always combines:

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

!!! warning "Rubber-stamp approvals without reading IaC blast radius  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Enormous PRs that nobody can review carefully  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Pull Requests and Code Review changes as code and review them in pull requests
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

- Demo doc change

## Interview Questions

1. How does **Pull Requests and Code Review** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [GitHub Actions for DevOps](github-actions-for-devops.md)

## References

- [About pull requests](https://docs.github.com/en/pull-requests) · [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
