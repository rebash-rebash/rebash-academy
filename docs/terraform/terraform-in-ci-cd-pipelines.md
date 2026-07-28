---
title: Terraform in CI/CD Pipelines
description: "Run Terraform in CI with plan artifacts, reviews, least-privilege credentials, and apply gates."
difficulty: advanced
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - cicd
  - github-actions
prerequisites:
  - Completed Policy as Code Overview
  - Familiarity with GitHub Actions or GitLab CI
comments: false
---

# Terraform in CI/CD Pipelines

## Overview

Production Terraform is applied by pipelines, not laptops. Build a PR plan / main apply flow with locked state, OIDC cloud auth overview, and automation-friendly CLI flags.

This is **Tutorial 19** in **Module 6: Production** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Design PR plan and main apply pipelines
- [ ] Use TF_IN_AUTOMATION and -input=false
- [ ] Store and apply plan artifacts
- [ ] Outline OIDC to cloud providers
- [ ] Author a complete GitHub Actions workflow example

## Prerequisites

- Completed Policy as Code Overview
- Familiarity with GitHub Actions or GitLab CI

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Terraform in CI/CD Pipelines](../assets/images/terraform-cicd.svg)


## Theory

### Recommended flow

1. PR: fmt-check, validate, test, plan, publish plan  
2. Reviewers read plan  
3. Main: apply saved plan or re-plan with protections  

### Auth

Prefer short-lived OIDC roles over long-lived access keys in CI.

### Why this topic matters in production

Teams that skip **Terraform in CI/CD pipelines** eventually pay in outages: unreviewable plans, brittle
refactors, or secrets leaking into logs. Treat this tutorial as the minimum bar for merging
Terraform changes on a shared state file.

### Practical mental model

1. Write the smallest config that proves the idea
2. `fmt` / `validate` / `plan` until the diff matches your intent
3. Apply only after you can explain every create/update/replace line
4. Destroy lab resources so the next exercise starts clean

## Hands-on Lab

### Step 1 – Tiny root for CI simulation

```bash
mkdir -p ~/rebash-tf-ci && cd ~/rebash-tf-ci
```

```hcl
terraform {
  required_version = ">= 1.9.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.9"
    }
  }
}

resource "local_file" "ci" {
  filename = "${path.module}/ci-marker.txt"
  content  = "planned-by-ci\n"
}

output "marker" {
  value = local_file.ci.filename
}
```

### Step 2 – Simulate pipeline stages locally

```bash
export TF_IN_AUTOMATION=1
terraform fmt -check
terraform init -input=false
terraform validate
terraform plan -input=false -out=tfplan
# On main only:
# terraform apply -input=false tfplan
terraform destroy -input=false -auto-approve || true
```

### Step 3 – Example GitHub Actions workflow

Save as `.github/workflows/terraform.yml` in a real repo:

```yaml
name: Terraform

on:
  pull_request:
    paths: ["**/*.tf", ".github/workflows/terraform.yml"]
  push:
    branches: [main]
    paths: ["**/*.tf", ".github/workflows/terraform.yml"]

permissions:
  contents: read
  pull-requests: write
  id-token: write

jobs:
  plan:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: infra
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.15.8"
      - run: terraform fmt -check -recursive
      - run: terraform init -input=false
      - run: terraform validate
      - run: terraform plan -input=false -out=tfplan
      - uses: actions/upload-artifact@v4
        with:
          name: tfplan
          path: infra/tfplan

  apply:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: production
    defaults:
      run:
        working-directory: infra
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.15.8"
      - run: terraform init -input=false
      - run: terraform apply -input=false -auto-approve
```

Wire OIDC cloud credentials in the `apply` job for real AWS/Azure/GCP backends — never store long-lived keys in GitHub secrets when OIDC is available.

## Code Walkthrough

Never apply from developer laptops to production when CI exists — the pipeline is the control point for audit.


Re-read every argument in the lab through the lens of **Terraform in CI/CD pipelines**.
For each resource address, ask: what happens on the next plan if I change this value?
Update in place, replace, or no-op? That habit is how you avoid surprise destroys.

## Validation

Run the lab to completion, then confirm:

```bash
terraform fmt -check
terraform init -input=false
terraform validate
terraform plan -input=false
```

| Check | Pass criteria |
|-------|----------------|
| Formatting | `fmt -check` exits 0 |
| Configuration | `validate` succeeds after init |
| Intent | Plan matches the tutorial’s expected creates/updates only |
| Topic focus | You can explain how this lab demonstrates Terraform in CI/CD pipelines |
| Cleanup | Destroy (or documented teardown) left no stray lab files |

## Best Practices

- Keep examples small enough to run without cloud credentials unless the topic requires otherwise
- Document assumptions (CLI version, providers, working directory) at the top of the root module
- Prefer explicitness over cleverness when teaching **Terraform in CI/CD pipelines**
- Add CI checks (`fmt`, `validate`, plan) as soon as a root is shared
- Write outputs that help the next human debug, not just the next machine

## Security Considerations

- Assume state and plan output may contain secrets related to **Terraform in CI/CD pipelines**
- Use least-privilege credentials whenever a provider needs authentication
- Do not commit tfvars with real secrets; use examples with placeholders
- Review plans for unexpected destroys before apply
- Limit who can unlock state and who can approve production applies

## Common Mistakes

!!! warning "Apply on every commit to main without review"
    Speed over safety. **Fix:** Require plan review / environments.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| validate fails | Missing init or syntax error | Run `terraform init`, read the file:line in the error |
| Plan shows replace unexpectedly | ForceNew argument changed | Confirm intent; use moved/lifecycle if refactoring |
| Provider auth errors | Credentials not available | Export the documented env vars for the provider |
| Topic confusion around Terraform in CI/CD pipelines | Skipped theory | Re-read Theory, then re-run the lab from a clean directory |
| Leftover lab files | Destroy skipped | Re-run destroy or delete the lab directory after state cleanup |

## Interview Questions

1. What stages belong in a Terraform pipeline?
2. How do you pass plan artifacts between jobs?
3. Why separate plan and apply permissions?
4. How does OIDC improve cloud auth from CI?
5. What should block a merge?
6. How do you handle manual approval for production?
7. Where do you store backend config in CI?
8. How do you prevent concurrent applies?
9. What logs must you treat as sensitive?
10. How do matrix builds work for many roots?
11. What is a safe destroy policy in CI?
12. How do you promote the same commit across environments?

## Summary

- Master **Terraform in CI/CD pipelines** before moving to the next tutorial in the track
- Every shared root needs formatting, validation, and a reviewed plan
- Prefer small, reversible labs that you can destroy confidently
- Carry security and state hygiene forward into every later module

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Policy as Code Overview](policy-as-code-overview.md)
- Next: [Production Patterns and Capstone](production-patterns-and-capstone.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
