---
title: Terraform in CI/CD Pipelines
description: "Production Terraform is applied by pipelines, not laptops. Build a PR plan / main apply flow with locked state, OIDC cloud auth overview, and automati"
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

Explain every resource argument you introduced in the lab: why it exists, what happens if omitted, and how it appears in state after apply. Keep `required_version` and `required_providers` in every root module you create going forward.

## Validation

```bash
terraform fmt -check
terraform init -input=false
terraform validate
terraform plan -input=false
```

| Check | Pass criteria |
|-------|----------------|
| fmt | Exit code 0 |
| validate | Configuration valid |
| plan/apply | Matches the lab expectations |

## Best Practices

- Keep root modules explicit about `required_version` and `required_providers`
- Prefer readable modules over clever expressions
- Run plans in CI before any production apply
- Document outputs that other stacks consume
- Treat state and plan artifacts as sensitive

## Security Considerations

- Limit who can read remote state
- Do not commit secrets in tfvars or code
- Use least-privilege credentials for providers
- Review plan output for unexpected destroys
- Enable encryption and locking on remote backends when you leave local labs

## Common Mistakes

!!! warning "Apply on every commit to main without review"
    Speed over safety. **Fix:** Require plan review / environments.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider download fails | Network/registry blocked | Check access to registry.terraform.io |
| validate fails before init | Providers not installed | Run `terraform init` |
| Unexpected replace | ForceNew argument change | Read plan carefully; use moved/for_each wisely |
| State locked | Another apply in progress | Wait or follow backend unlock procedures carefully |
| Permission denied writing files | Directory permissions | Ensure workspace is writable |

## Interview Questions

1. What problem does Terraform in CI/CD Pipelines solve in a Terraform workflow?
2. How does this topic change what you put in Git versus what stays local or remote?
3. Which official HashiCorp documentation would you consult before changing production?
4. How would you validate a change related to this topic in CI before apply?
5. What failure mode appears if two engineers ignore this topic on the same state?
6. How does this interact with Terraform state?
7. What is a secure default related to this topic?
8. Describe a common anti-pattern and its fix.
9. How would you explain this topic to a teammate in two minutes?
10. What production checklist item captures this topic?
11. When would you intentionally not use the default approach taught here?
12. How does this topic differ between a root module and a child module?

## Summary

- Production Terraform is applied by pipelines, not laptops. Build a PR plan / main apply flow with locked state, OIDC cloud auth overview, and automation-friendly CLI flags.
- Practice the lab until `fmt` / `validate` / `plan` are muscle memory
- Carry forward provider pins, sensitive handling, and plan-before-apply discipline

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Policy as Code Overview](policy-as-code-overview.md)
- Next: [Production Patterns and Capstone](production-patterns-and-capstone.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
