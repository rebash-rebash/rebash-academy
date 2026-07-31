---
title: "Signed Commits and Git Security"
description: "Sign commits with SSH or GPG, verify signatures, protect branches, keep secrets out of Git, and harden GitHub for DevOps compliance."
difficulty: advanced
estimated_time: "45–60 min"
technology: git
category: git
module: "Module 15 · Security"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - git
  - commit-signing
  - security
prerequisites:
  - git/repository-management-and-releases
  - git/pull-requests-and-code-review
next:
  - git/git-troubleshooting
related:
  - git/production-git-practices
  - security/index
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Advanced Security
tags:
  - git
  - security
  - signing
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Signed Commits and Git Security

## Overview



Configure commit signing (SSH preferred for simplicity), verify signatures, and apply Git/GitHub security baselines: branch protection, secret hygiene, and least-privilege access.

Author email in Git is forgeable. **Signed commits** prove the committer held a key tied to a verified identity. Pair signing with branch protection, secret scanning, and never committing credentials.

This is a core tutorial in **Module 15 · Security** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Repository Management and Releases](repository-management-and-releases.md)
- [Pull Requests and Code Review](pull-requests-and-code-review.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Configure SSH commit signing  
- [ ] Verify with `git log --show-signature`  
- [ ] Explain required signed commits on protected branches  
- [ ] List secrets that must never enter history  
- [ ] Outline response if a secret is committed



## Architecture



This topic’s control points and relationships are shown below.

![PR / review gate](../assets/excalidraw/git-pr-lifecycle.svg)



## Theory



### What

**Git security** combines cryptography and platform controls. **Signed commits and tags** (GPG, SSH, or X.509 signing) prove authorship integrity. Branch protection, CODEOWNERS, secret scanning, push protection, and least-privilege tokens reduce the chance that bad or spoofed changes reach `main`.

### Why

Unsigned history can be rewritten or attributed falsely in social-engineering scenarios. Secrets in Git are a leading cloud breach pattern — assume anything committed is eventually exfiltrated. DevOps repos that deploy production need stronger defaults than hobby projects.

### How it works

You configure a signing key, enable `commit.gpgsign` or SSH signing, and let the host verify badges on commits. Branch protection blocks direct pushes and requires reviews plus CI. Secret scanning alerts (and push protection blocks) known credential patterns. CI should prefer OIDC federation to cloud roles over long-lived static keys. If a secret is committed: **rotate first**, then scrub history with purpose-built tools (`git filter-repo` / BFG) under an incident process — never “delete the file in a new commit” as the only step.

| Control | Purpose |
|---------|---------|
| Signed commits/tags | Authorship integrity |
| Branch protection | No direct push to `main` |
| CODEOWNERS | Path-based review |
| Secret scanning / push protection | Stop credential leaks |
| Fine-grained PATs / OIDC | Safer CI auth |

### Key concepts

- **Verify signatures** in clone policies for sensitive repos  
- **History rewrite** after leaks is an org-wide coordination event  
- **Deploy keys vs GitHub Apps** — scope automation narrowly  
- **Dependency and Action pinning** — adjacent supply-chain controls  

### Common pitfalls

- Rotating a leaked key but leaving the old commit publicly readable without rewrite/incident notes  
- Signing commits while still allowing unprotected force-pushes  
- Broad classic PATs in shared CI secrets  
- Committing `.env` “temporarily” on a feature branch



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-15 && cd ~/rebash-git/module-15
```

**Focus:** practise Git skills for: Signed Commits and Git Security

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

### Step 2 – Signing readiness

```bash
git config --get user.name
git config --get user.email
tee signing-notes.txt << 'EOF'
Production: enable commit signing (GPG/SSH) and require signed commits on protected branches.
Lab: confirm identity config is correct before enabling signing keys.
EOF
git log -1 --pretty=fuller | tee last.txt
cat signing-notes.txt
```

### Final step – Cleanup note

```bash
# Safe local repo under the lab directory; delete the folder when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-git/module-15/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Signed Commits and Git Security** always combines:

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



!!! warning "Rotating a leaked key but leaving the old commit publicly readable without rewrite/inciden"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Signing commits while still allowing unprotected force-pushes  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Signed Commits and Git Security changes as code and review them in pull requests
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



**Signed Commits and Git Security** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. Explain **Signed Commits and Git Security** as you would in a senior engineer interview.
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
- [Git Troubleshooting](git-troubleshooting.md)



## References



- [About commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification)  
- [git-config signing](https://git-scm.com/docs/git-config#Documentation/git-config.txt-commitgpgsign)
