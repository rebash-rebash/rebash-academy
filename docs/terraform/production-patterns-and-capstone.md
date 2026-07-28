---
title: Production Patterns and Capstone
description: "Assemble production patterns: remote state, modules, CI, secrets, and a capstone root that ties the track together."
difficulty: advanced
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - production
  - capstone
prerequisites:
  - Completed Terraform in CI/CD Pipelines
  - All prior Terraform tutorials recommended
comments: false
---

# Production Patterns and Capstone

## Overview

Capstone: assemble modules, env isolation, tagging, remote-state notes, secrets hygiene, tests, and CI into a production-shaped local project. Leave with a checklist you can apply to real cloud roots.

This is **Tutorial 20** in **Module 6: Production** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Structure envs/ and modules/ cleanly
- [ ] Compose multiple modules with shared locals/tags
- [ ] Apply production checklists (state, secrets, CI, policy)
- [ ] Document outputs and upgrade strategy
- [ ] Demonstrate end-to-end validate/plan/apply locally

## Prerequisites

- Completed Terraform in CI/CD Pipelines
- All prior Terraform tutorials recommended

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Production Patterns and Capstone](../assets/images/terraform-capstone.svg)


## Theory

### Suggested layout

```text
modules/
  network/
  app/
envs/
  dev/
  prod/
.github/workflows/terraform.yml
```

Each env root pins providers, configures backend, and calls modules with env-specific tfvars.

### Production checklist

- [ ] required_version + required_providers + lockfile  
- [ ] Remote state + locking + encryption  
- [ ] No secrets in Git  
- [ ] CI plan/apply with OIDC  
- [ ] Policy checks  
- [ ] Module tests  
- [ ] Tagging/label standards  
- [ ] Drift review cadence

### Why this topic matters in production

Teams that skip **production Terraform patterns and the capstone lab** eventually pay in outages: unreviewable plans, brittle
refactors, or secrets leaking into logs. Treat this tutorial as the minimum bar for merging
Terraform changes on a shared state file.

### Practical mental model

1. Write the smallest config that proves the idea
2. `fmt` / `validate` / `plan` until the diff matches your intent
3. Apply only after you can explain every create/update/replace line
4. Destroy lab resources so the next exercise starts clean

## Hands-on Lab

### Step 1 – Repository layout

```bash
mkdir -p ~/rebash-tf-capstone/{modules/network,modules/app,envs/dev,generated}
cd ~/rebash-tf-capstone
```

### Step 2 – Network module

`modules/network/variables.tf`:

```hcl
variable "name" { type = string }
variable "tags" { type = map(string) }
```

`modules/network/main.tf`:

```hcl
resource "local_file" "vpc" {
  filename = "${path.module}/../../generated/${var.name}-vpc.txt"
  content  = <<-EOT
    name=${var.name}
    tags=${jsonencode(var.tags)}
  EOT
}

output "vpc_file" { value = local_file.vpc.filename }
```

### Step 3 – App module

`modules/app/variables.tf`:

```hcl
variable "name" { type = string }
variable "vpc_file" { type = string }
variable "tags" { type = map(string) }
```

`modules/app/main.tf`:

```hcl
resource "local_file" "app" {
  filename = "${path.module}/../../generated/${var.name}-app.txt"
  content  = <<-EOT
    app=${var.name}
    vpc_file=${var.vpc_file}
    tags=${jsonencode(var.tags)}
  EOT
}

output "app_file" { value = local_file.app.filename }
```

### Step 4 – Dev environment root

`envs/dev/versions.tf`:

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
```

`envs/dev/main.tf`:

```hcl
locals {
  tags = {
    Project = "rebash-academy"
    Env     = "dev"
    Managed = "terraform"
  }
}

module "network" {
  source = "../../modules/network"
  name   = "capstone"
  tags   = local.tags
}

module "app" {
  source   = "../../modules/app"
  name     = "capstone-api"
  vpc_file = module.network.vpc_file
  tags     = local.tags
}

output "stack" {
  value = {
    vpc = module.network.vpc_file
    app = module.app.app_file
    tags = local.tags
  }
}
```

### Step 5 – Apply the stack

```bash
cd ~/rebash-tf-capstone/envs/dev
terraform fmt -recursive ../..
terraform init -input=false
terraform validate
terraform apply -input=false -auto-approve
cat ../../generated/*.txt
terraform destroy -input=false -auto-approve
```

### Production checklist (carry forward)

- [ ] Remote state + locking + encryption
- [ ] Provider pins + committed lockfile
- [ ] CI plan on PR / apply on main
- [ ] Secrets via CI/OIDC/secret manager
- [ ] Policy checks on plan JSON
- [ ] Module tests for shared modules
- [ ] Tagging standard in locals

## Code Walkthrough

Even with local_file stand-ins, the **structure** matches production cloud stacks — swap module bodies for AWS/Azure resources later without redesigning the repo.


Re-read every argument in the lab through the lens of **production Terraform patterns and the capstone lab**.
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
| Topic focus | You can explain how this lab demonstrates production Terraform patterns and the capstone lab |
| Cleanup | Destroy (or documented teardown) left no stray lab files |

## Best Practices

- Keep examples small enough to run without cloud credentials unless the topic requires otherwise
- Document assumptions (CLI version, providers, working directory) at the top of the root module
- Prefer explicitness over cleverness when teaching **production Terraform patterns and the capstone lab**
- Add CI checks (`fmt`, `validate`, plan) as soon as a root is shared
- Write outputs that help the next human debug, not just the next machine

## Security Considerations

- Assume state and plan output may contain secrets related to **production Terraform patterns and the capstone lab**
- Use least-privilege credentials whenever a provider needs authentication
- Do not commit tfvars with real secrets; use examples with placeholders
- Review plans for unexpected destroys before apply
- Limit who can unlock state and who can approve production applies

## Common Mistakes

!!! warning "Skipping remote state until ‘later’"
    Painful migrations. **Fix:** Add backend before the second engineer joins.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| validate fails | Missing init or syntax error | Run `terraform init`, read the file:line in the error |
| Plan shows replace unexpectedly | ForceNew argument changed | Confirm intent; use moved/lifecycle if refactoring |
| Provider auth errors | Credentials not available | Export the documented env vars for the provider |
| Topic confusion around production Terraform patterns and the capstone lab | Skipped theory | Re-read Theory, then re-run the lab from a clean directory |
| Leftover lab files | Destroy skipped | Re-run destroy or delete the lab directory after state cleanup |

## Interview Questions

1. List five production checklist items before first apply.
2. How do you structure repos for many teams?
3. When do you split state files?
4. How do you handle blast radius in modules?
5. What observability surrounds Terraform changes?
6. How do you roll back a bad apply?
7. What documentation must every root module include?
8. How do you onboard a new engineer to a Terraform mono-repo?
9. What is the relationship between GitOps and Terraform?
10. How do you measure Terraform delivery lead time?
11. What anti-patterns appear in long-lived state?
12. How would you extend this capstone to a real cloud provider?

## Summary

- Master **production Terraform patterns and the capstone lab** before moving to the next tutorial in the track
- Every shared root needs formatting, validation, and a reviewed plan
- Prefer small, reversible labs that you can destroy confidently
- Carry security and state hygiene forward into every later module

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Terraform in CI/CD Pipelines](terraform-in-ci-cd-pipelines.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
