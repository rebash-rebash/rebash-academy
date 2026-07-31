---
title: "Git for Infrastructure as Code"
description: "Version Terraform, Ansible, and policy-as-code with Git — layouts, reviews, secrets hygiene, and plan-on-PR workflows."
difficulty: intermediate
estimated_time: "45–60 min"
technology: git
category: git
module: "Module 13 · Git for IaC"
career_paths:
  - devops-engineer
  - platform-engineer
  - cloud-engineer
skills:
  - git
  - infrastructure-as-code
  - terraform
prerequisites:
  - git/gitops-fundamentals
next:
  - git/repository-management-and-releases
related:
  - terraform/index
  - git/signed-commits-and-git-security
labs: []
projects: []
interview: interview/git
certifications:
  - HashiCorp Terraform Associate
tags:
  - git
  - terraform
  - iac
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Git for Infrastructure as Code

## Overview



Structure an Infrastructure as Code (IaC) repository for safe Git reviews: clear modules, `.gitignore` for state/secrets, and plan-on-PR as the change process.

IaC without Git discipline is risky. Treat Terraform/Ansible like production code: small PRs, CODEOWNERS on `prod/`, never commit `.tfstate` or secrets.

This is a core tutorial in **Module 13 · Git for IaC** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [GitOps Fundamentals](gitops-fundamentals.md)
- [gitignore and gitattributes](gitignore-and-gitattributes.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Layout env folders (`dev` / `prod`) or workspaces intentionally  
- [ ] Ignore state, `.terraform/`, keys  
- [ ] Require review for production paths  
- [ ] Pair Git with CI plan (no apply from laptop as policy)



## Architecture



This topic’s control points and relationships are shown below.

![Repository architecture](../assets/excalidraw/git-repository-architecture.svg)



## Theory



### What

**Infrastructure as Code (IaC)** stores infrastructure definitions as files reviewed and versioned like application code. Git is the collaboration layer for Terraform, Ansible, cloud templates, Kubernetes manifests, and policy (Open Policy Agent / Conftest). Remote state and secrets stay **out** of the repository.

### Why

Infrastructure changes are high blast-radius. Git history plus pull requests provide peer review, CI plan checks, and a path to roll forward or back. Without Git discipline, teams copy credentials into repos and lose track of which module version produced production.

### How it works

Keep declarative definitions, modules, tests, and runbooks in Git. Run `terraform plan` (or equivalent) in CI against proposed commits. Apply from controlled pipelines or break-glass procedures — not from unmanaged laptops when policy forbids it. State files (`*.tfstate*`), provider plugin caches, private keys, and `.env` files with secrets must be ignored and stored in appropriate backends (for example S3 with locking, Terraform Cloud).

| Keep in Git | Never in Git |
|-------------|--------------|
| `.tf` / modules | `*.tfstate*` |
| Ansible playbooks | Private keys, `.pem` |
| Policy (OPA/Conftest) | Cloud credentials |
| README / runbooks | `.env` with secrets |

### Key concepts

- **Module versioning** — pin module refs; avoid floating `main` in production roots  
- **Environment layout** — directories or workspaces with clear blast radius  
- **Policy as code** — same PR process as Terraform  
- **Plan artefacts** — store plans safely; do not commit them with secrets  

### Common pitfalls

- Committing state “just once” for convenience  
- Copy-pasting access keys into variable files  
- Applying unreviewed local changes that never land in Git  
- One giant root module with no ownership boundaries



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-13/{modules/network,envs/dev} && cd ~/rebash-git/module-13/{modules/network,envs/dev}
```

**Focus:** practise Git skills for: Git for Infrastructure as Code

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

### Step 2 – IaC repo hygiene

```bash
mkdir -p infra
echo 'resource "null_resource" "x" {}' > infra/main.tf
cat > .gitignore << 'EOF'
.terraform/
*.tfstate*
.terraform.lock.hcl
EOF
git add infra .gitignore
git commit -m 'Add infra scaffold'
git status --ignored | tee ignored.txt
```

### Final step – Cleanup note

```bash
# Safe local repo under the lab directory; delete the folder when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-git/module-13/{modules/network,envs/dev}/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Git for Infrastructure as Code** always combines:

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



!!! warning "Committing state “just once” for convenience  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Copy-pasting access keys into variable files  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Git for Infrastructure as Code changes as code and review them in pull requests
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



**Git for Infrastructure as Code** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. Explain **Git for Infrastructure as Code** as you would in a senior engineer interview.
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
- [Repository Management and Releases](repository-management-and-releases.md)



## References



- [Terraform style / VCS](https://developer.hashicorp.com/terraform/language/style)
