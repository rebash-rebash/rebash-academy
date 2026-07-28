---
title: Modules — Creating Reusable Infrastructure
description: "Modules package reusable infrastructure patterns behind a typed input/output API. This tutorial builds a child module and calls it from a root — the f"
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - modules
prerequisites:
  - Completed Workspaces and Environment Strategies
comments: false
---

# Modules — Creating Reusable Infrastructure

## Overview

Modules package reusable infrastructure patterns behind a typed input/output API. This tutorial builds a child module and calls it from a root — the fundamental composition skill for platform teams.

This is **Tutorial 11** in **Module 3: Collaboration and Scale** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Create a child module with variables and outputs
- [ ] Call modules with the module block
- [ ] Use path.module inside child modules
- [ ] Design small, composable modules
- [ ] Avoid leaking unnecessary implementation outputs

## Prerequisites

- Completed Workspaces and Environment Strategies

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Modules — Creating Reusable Infrastructure](../assets/images/terraform-modules.svg)


## Theory

### Module block

```hcl
module "greeting" {
  source     = "./modules/greeting"
  project    = "rebash"
  message    = "hello"
}
```

### Design tips

- One responsibility per module
- Typed variables with descriptions
- Stable outputs only
- Pin external module versions (next tutorial)

## Hands-on Lab

```bash
mkdir -p ~/rebash-tf-mod/modules/greeting
cd ~/rebash-tf-mod
```

`modules/greeting/variables.tf`, `main.tf`, `outputs.tf`, and root `main.tf`:

```hcl
# modules/greeting/variables.tf
variable "project" { type = string }
variable "message" { type = string }

# modules/greeting/main.tf
resource "local_file" "this" {
  filename = "${path.module}/../../generated/${var.project}.txt"
  content  = "${var.message}\n"
}

# modules/greeting/outputs.tf
output "path" { value = local_file.this.filename }

# versions.tf (root)
terraform {
  required_version = ">= 1.9.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.9"
    }
  }
}

# main.tf (root)
module "greeting" {
  source  = "./modules/greeting"
  project = "rebash"
  message = "module-lab"
}

output "greeting_path" {
  value = module.greeting.path
}
```

```bash
mkdir -p generated
terraform init -input=false && terraform apply -input=false -auto-approve
terraform destroy -input=false -auto-approve
```

## Code Walkthrough

The root only depends on the module’s outputs — encapsulation that lets you change module internals safely.

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

!!! warning "Mega-modules that create an entire company"
    Unreviewable. **Fix:** Compose small modules.

!!! warning "Using relative `../` outputs as API"
    Brittle. **Fix:** Export stable IDs/names only.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider download fails | Network/registry blocked | Check access to registry.terraform.io |
| validate fails before init | Providers not installed | Run `terraform init` |
| Unexpected replace | ForceNew argument change | Read plan carefully; use moved/for_each wisely |
| State locked | Another apply in progress | Wait or follow backend unlock procedures carefully |
| Permission denied writing files | Directory permissions | Ensure workspace is writable |

## Interview Questions

1. What problem does Modules — Creating Reusable Infrastructure solve in a Terraform workflow?
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

- Modules package reusable infrastructure patterns behind a typed input/output API. This tutorial builds a child module and calls it from a root — the fundamental composition skill for platform teams.
- Practice the lab until `fmt` / `validate` / `plan` are muscle memory
- Carry forward provider pins, sensitive handling, and plan-before-apply discipline

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Workspaces and Environment Strategies](workspaces-and-environment-strategies.md)
- Next: [Registry Modules and Composition](registry-modules-and-composition.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
