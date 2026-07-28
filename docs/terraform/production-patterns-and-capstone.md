---
title: Production Patterns and Capstone
description: "Capstone: assemble modules, env isolation, tagging, remote-state notes, secrets hygiene, tests, and CI into a production-shaped local project. Leave w"
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

!!! warning "Skipping remote state until ‘later’"
    Painful migrations. **Fix:** Add backend before the second engineer joins.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider download fails | Network/registry blocked | Check access to registry.terraform.io |
| validate fails before init | Providers not installed | Run `terraform init` |
| Unexpected replace | ForceNew argument change | Read plan carefully; use moved/for_each wisely |
| State locked | Another apply in progress | Wait or follow backend unlock procedures carefully |
| Permission denied writing files | Directory permissions | Ensure workspace is writable |

## Interview Questions

1. What problem does Production Patterns and Capstone solve in a Terraform workflow?
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

- Capstone: assemble modules, env isolation, tagging, remote-state notes, secrets hygiene, tests, and CI into a production-shaped local project. Leave with a checklist you can apply to real cloud roots.
- Practice the lab until `fmt` / `validate` / `plan` are muscle memory
- Carry forward provider pins, sensitive handling, and plan-before-apply discipline

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Terraform in CI/CD Pipelines](terraform-in-ci-cd-pipelines.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
