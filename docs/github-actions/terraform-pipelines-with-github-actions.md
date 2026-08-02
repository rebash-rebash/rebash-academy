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



### Objective

Author a GitHub Actions workflow that implements **Terraform Pipelines with GitHub Actions** and validate YAML structure locally.

### Prerequisites

- Python 3 with PyYAML
- Optional: GitHub repo to run the workflow

### Lab environment

Workspace: `~/rebash-github-actions/module-09/.github/workflows`

Workflows under `.github/workflows/`. In docs, wrap GitHub Actions expressions in Jinja raw blocks so MkDocs macros do not parse them; use heredocs in the lab.

```bash
mkdir -p ~/rebash-github-actions/module-09/.github/workflows && cd ~/rebash-github-actions/module-09/.github/workflows
```

### Real-world scenario

Platform engineering wants **Terraform Pipelines with GitHub Actions** as a reusable workflow pattern. You prototype YAML that passes review and runs on `ubuntu-latest`.

### Step-by-step tasks

#### Task 1 – Create workflow file

Jobs and steps must be explicit; pin mainstream actions.

```bash
mkdir -p .github/workflows
cat > .github/workflows/lab.yml << 'EOF'
name: lab
on:
  workflow_dispatch:
  push:
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Prove workspace
        run: |
          mkdir -p out
          echo ok > out/marker.txt
          test -s out/marker.txt
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/lab.yml')); print('workflow OK')"
```

**Expected output:** `workflow OK` printed; file exists under `.github/workflows/`.

#### Task 2 – Dry-run the shell steps locally

The `run:` block should work in a normal shell before CI.

```bash
mkdir -p out && echo ok > out/marker.txt
test -s out/marker.txt && cat out/marker.txt
```

**Expected output:** Prints `ok`.

### Validation steps

- [ ] Workflow YAML parses
- [ ] Local run steps succeed

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Invalid workflow file | YAML/indent | Validate with PyYAML / actionlint |
| Action not found | Bad uses ref | Pin `actions/checkout@v4` |
| Permission denied | Missing permissions/OIDC | Set least-privilege `permissions:` |

### Challenge exercise

Add a second job with `needs: build` that uploads `out/` as an artefact (YAML only is fine offline).

### Learning outcomes

- Created a real workflow file
- Validated structure before push

### Cleanup

```bash
# Keep workflow stubs under ~/rebash-github-actions/
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






1. Why apply the exact plan artifact from the same workflow run?
2. What state backend considerations matter in CI?
3. When should apply require a GitHub environment approval?
4. How do you pass cloud credentials to Terraform in Actions?
5. How do you destroy experimental stacks created in labs?

!!! tip "Sample answer — question 2"
    Confirm init backend, matching variables between plan/apply, and that the plan artifact downloaded correctly.

!!! tip "Sample answer — question 4"
    Use OIDC-mapped least-privilege roles, protect state, and never commit tfstate. Destroy lab resources in the same session.

## Related Tutorials








- [Course overview](index.md)
- [Multi-Cloud Deployments with GitHub Actions](multi-cloud-deployments-with-github-actions.md)

## References








- [Terraform GitHub Actions](https://developer.hashicorp.com/terraform/tutorials/automation/github-actions) · [setup-terraform](https://github.com/hashicorp/setup-terraform) · [Automating Terraform](https://developer.hashicorp.com/terraform/cli/run/automating-terraform) · [GitHub Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
