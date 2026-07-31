---
title: "Terraform Pipelines with GitHub Actions"
description: "Run Terraform init, validate, plan on pull requests, and gated apply on main with remote state and plan artefacts in GitHub Actions."
difficulty: advanced
estimated_time: "50–65 min"
technology: github-actions
category: github-actions
module: "Module 9 · Terraform Pipelines"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - github-actions
  - terraform
  - infrastructure-as-code
prerequisites:
  - github-actions/kubernetes-deployments-with-github-actions
next:
  - github-actions/multi-cloud-deployments-with-github-actions
related:
  - terraform/terraform-in-ci-cd-pipelines
  - terraform/remote-state-and-backends
  - github-actions/secrets-variables-and-oidc
labs: []
projects: []
interview: interview/github-actions
certifications:
  - GitHub Actions
tags:
  - github-actions
  - terraform
  - iac
  - plan
  - remote-state
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Terraform Pipelines with GitHub Actions

## Overview

Design a GitHub Actions pipeline that runs `init` → `validate` → `plan` on pull requests (with a plan artefact) and a protected `apply` on `main` — with remote state outside the runner workspace and clear notes on destroy.

Terraform in Actions automates Infrastructure as Code (IaC): every change is planned in review, then applied under gates. Store **remote state** with locking (for example Amazon Simple Storage Service (S3) + DynamoDB, Azure Storage, or Google Cloud Storage). Upload the binary **plan** as a workflow artefact so apply executes what reviewers saw. Never leave state only on the runner disk. Prefer OpenID Connect (OIDC) cloud roles (Modules 5 and 10) over static access keys.

This is a core tutorial in **Module 9 · Terraform Pipelines** of the REBASH Academy **GitHub Actions for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Kubernetes Deployments with GitHub Actions](kubernetes-deployments-with-github-actions.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Sequence init, validate, plan, apply, and optional destroy  
- [ ] Store plan output as a GitHub Actions artefact for PR review  
- [ ] Gate apply with a protected environment  
- [ ] Explain remote state + locking in CI  
- [ ] Use `TF_IN_AUTOMATION` and non-interactive flags

## Architecture

This topic’s control points and relationships are shown below.

![Terraform pipeline](../assets/excalidraw/gha-terraform-pipeline.svg)

## Theory

### What it is

A **Terraform pipeline** maps CLI phases onto workflow jobs: `fmt`/`validate` and `plan -out=` on every pull request (read-only / plan privilege); reviewed **apply** of the saved plan on the default branch behind a protected environment; rare, heavily gated **destroy**. State lives in a **remote backend** with locking. Set `TF_IN_AUTOMATION=true` and `-input=false` so jobs never prompt. Pin the Terraform CLI version (`hashicorp/setup-terraform`) so plan and apply use the same binary.

| Concern | Good practice | Risk |
|---------|---------------|------|
| State | Remote + lock | Local state on runner |
| Plan | Artefact tied to commit SHA | Fresh plan at apply with drift |
| Apply | Protected environment + reviewers | Auto-apply on every push |
| Secrets | OIDC / environment secrets | Static admin keys in repository secrets |

### Why it matters

Laptop apply bypasses review and uses personal cloud keys. Pull-request plans give reviewers a concrete diff; protected apply prevents unreviewed infrastructure changes. Plan artefacts stop “plan on Tuesday, apply Thursday’s different config.” State locking prevents two workflows from corrupting the same workspace. Destroy without dual control can erase production in minutes.

### How it works

1. On pull request: pin Terraform → `init` → `validate` → `plan -out=tfplan` → upload artefact (short retention).  
2. Post a human-readable summary (`terraform show` or a plan comment action) for reviewers.  
3. On merge to `main` (after environment approval): download the same artefact → `apply -input=false tfplan`.  
4. **Destroy** jobs are `workflow_dispatch` only, environment-protected, and ideally dual-controlled.  
5. Backend config comes from OIDC cloud roles or environment variables — no secrets in Git.

Prefer apply-of-saved-plan for production. If you must re-plan at apply time, document why and still gate on the new plan.

### Key concepts and comparisons

| Phase | Trigger | Privilege |
|-------|---------|-----------|
| validate / plan | Pull request + `main` | Read / plan role |
| apply | `main` + environment | Write role, scoped |
| destroy | Manual dispatch | Break-glass, dual control |

### Common pitfalls

- Committing `.terraform/` or `terraform.tfstate` to Git.  
- Applying without the reviewed plan artefact.  
- Logging plans that include secret attribute values.  
- One shared state key for all environments.  
- Fork pull requests with write-level cloud roles (use `pull_request_target` carefully — prefer OIDC subject conditions that exclude forks).

## Hands-on Lab
Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-github-actions/module-09/.github/workflows && cd ~/rebash-github-actions/module-09/.github/workflows
git init -q
```

**Focus:** author and validate CI config for Terraform Pipelines with GitHub Actions

### Step 1 – Write a minimal pipeline

```bash
mkdir -p .github/workflows
cat > .github/workflows/lab.yml << 'EOF'
name: lab
on: workflow_dispatch
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "workflow ok"
EOF
ls -la
sed -n '1,80p' .github/workflows/lab.yml
```

### Step 2 – Static checks before push

```bash
# Syntax / structure sanity (no runner required)
test -s .github/workflows/lab.yml
grep -E 'script:|runs-on:|steps:' .github/workflows/lab.yml
# When a runner is available, push a branch and confirm the job is green
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials; delete remote test branches when finished
```

## Validation

- [ ] Lab commands run under `~/rebash-github-actions/module-09/.github/workflows/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Terraform Pipelines with GitHub Actions** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for github-actions as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Committing `.terraform/` or `terraform.tfstate` to Git.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Applying without the reviewed plan artefact.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Terraform Pipelines with GitHub Actions changes as code and review them in pull requests
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

**Terraform Pipelines with GitHub Actions** is essential for Cloud and DevOps engineers working with github-actions. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Terraform Pipelines with GitHub Actions** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Multi-Cloud Deployments with GitHub Actions](multi-cloud-deployments-with-github-actions.md)

## References

- [Terraform GitHub Actions](https://developer.hashicorp.com/terraform/tutorials/automation/github-actions) · [setup-terraform](https://github.com/hashicorp/setup-terraform) · [Automating Terraform](https://developer.hashicorp.com/terraform/cli/run/automating-terraform) · [GitHub Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
