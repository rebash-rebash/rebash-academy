---
title: Registry Modules and Composition
description: "Consume Terraform Registry modules with version pins and compose them into a maintainable root."
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - registry
  - modules
prerequisites:
  - Completed Modules — Creating Reusable Infrastructure
comments: false
---

# Registry Modules and Composition

## Overview

The Terraform Registry distributes versioned modules. Learn source addresses, version pins, and composition patterns. Labs stay local while showing how a Registry module such as terraform-aws-modules/vpc/aws (v6.6.1) would be consumed.

This is **Tutorial 12** in **Module 3: Collaboration and Scale** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Address Registry modules with version constraints
- [ ] Compare local, git, and registry sources
- [ ] Compose multiple modules in one root
- [ ] Read module documentation before adoption
- [ ] Avoid unpinned module sources in production

## Prerequisites

- Completed Modules — Creating Reusable Infrastructure

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Registry Modules and Composition](../assets/images/terraform-registry.svg)


## Theory

### Sources

| Source | Example |
|--------|---------|
| Local | `./modules/vpc` |
| Registry | `terraform-aws-modules/vpc/aws` |
| Git | `git::https://example.com/vpc.git?ref=v1.2.0` |

### Registry example (do not apply without AWS creds)

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "6.6.1"

  name = "example"
  cidr = "10.0.0.0/16"
  # ... see module docs for required inputs
}
```

### Why this topic matters in production

Teams that skip **Registry modules and composition** eventually pay in outages: unreviewable plans, brittle
refactors, or secrets leaking into logs. Treat this tutorial as the minimum bar for merging
Terraform changes on a shared state file.

### Practical mental model

1. Write the smallest config that proves the idea
2. `fmt` / `validate` / `plan` until the diff matches your intent
3. Apply only after you can explain every create/update/replace line
4. Destroy lab resources so the next exercise starts clean

## Hands-on Lab

### Step 1 – Scaffold registry-style local modules

```bash
mkdir -p ~/rebash-tf-reg/{modules/network,modules/app,generated}
cd ~/rebash-tf-reg
```

`modules/network/variables.tf`:

```hcl
variable "name" {
  type = string
}

variable "cidr" {
  type = string
}
```

`modules/network/main.tf`:

```hcl
resource "local_file" "vpc" {
  filename        = "${path.module}/../../generated/${var.name}-vpc.txt"
  content         = "vpc_name=${var.name}\ncidr=${var.cidr}\n"
  file_permission = "0644"
}
```

`modules/network/outputs.tf`:

```hcl
output "vpc_id" {
  value = local_file.vpc.id
}

output "vpc_file" {
  value = local_file.vpc.filename
}
```

`modules/app/variables.tf`:

```hcl
variable "name" {
  type = string
}

variable "vpc_file" {
  type = string
}
```

`modules/app/main.tf`:

```hcl
resource "local_file" "app" {
  filename = "${path.module}/../../generated/${var.name}-app.txt"
  content  = <<-EOT
    app=${var.name}
    depends_on_vpc_file=${var.vpc_file}
  EOT
}
```

`modules/app/outputs.tf`:

```hcl
output "app_file" {
  value = local_file.app.filename
}
```

### Step 2 – Root composition (mirrors Registry usage)

`versions.tf`:

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

`main.tf`:

```hcl
module "network" {
  source = "./modules/network"
  name   = "payments"
  cidr   = "10.20.0.0/16"
}

module "app" {
  source   = "./modules/app"
  name     = "payments-api"
  vpc_file = module.network.vpc_file
}

output "artifacts" {
  value = {
    vpc = module.network.vpc_file
    app = module.app.app_file
  }
}
```

### Step 3 – Apply

```bash
terraform init -input=false
terraform apply -input=false -auto-approve
cat generated/payments-vpc.txt generated/payments-api-app.txt
terraform destroy -input=false -auto-approve
```

Compare this pin-and-compose pattern to a Registry call:

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "6.6.1"
  # inputs from module docs...
}
```

## Code Walkthrough

Treat every external module like a dependency: pin versions, read changelogs, and wrap behind your own thin module if you need a stable internal API.


Re-read every argument in the lab through the lens of **Registry modules and composition**.
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
| Topic focus | You can explain how this lab demonstrates Registry modules and composition |
| Cleanup | Destroy (or documented teardown) left no stray lab files |

## Best Practices

- Keep examples small enough to run without cloud credentials unless the topic requires otherwise
- Document assumptions (CLI version, providers, working directory) at the top of the root module
- Prefer explicitness over cleverness when teaching **Registry modules and composition**
- Add CI checks (`fmt`, `validate`, plan) as soon as a root is shared
- Write outputs that help the next human debug, not just the next machine

## Security Considerations

- Assume state and plan output may contain secrets related to **Registry modules and composition**
- Use least-privilege credentials whenever a provider needs authentication
- Do not commit tfvars with real secrets; use examples with placeholders
- Review plans for unexpected destroys before apply
- Limit who can unlock state and who can approve production applies

## Common Mistakes

!!! warning "`source` without `version` for Registry modules"
    Unexpected upgrades. **Fix:** Always pin.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| validate fails | Missing init or syntax error | Run `terraform init`, read the file:line in the error |
| Plan shows replace unexpectedly | ForceNew argument changed | Confirm intent; use moved/lifecycle if refactoring |
| Provider auth errors | Credentials not available | Export the documented env vars for the provider |
| Topic confusion around Registry modules and composition | Skipped theory | Re-read Theory, then re-run the lab from a clean directory |
| Leftover lab files | Destroy skipped | Re-run destroy or delete the lab directory after state cleanup |

## Interview Questions

1. How do you pin a Registry module version?
2. What is the risk of source = ref without a version?
3. How do you evaluate a public module before adopting it?
4. When should you wrap a Registry module in an internal module?
5. How do module outputs feed other modules?
6. What is the difference between count and for_each on modules?
7. How do you upgrade a module version in a controlled way?
8. Where do you find module documentation?
9. How do provisioners in third-party modules increase risk?
10. What licence and maintenance signals matter?
11. How do you mirror modules for air-gapped use?
12. Describe a composition pattern for network + app modules.

## Summary

- Master **Registry modules and composition** before moving to the next tutorial in the track
- Every shared root needs formatting, validation, and a reviewed plan
- Prefer small, reversible labs that you can destroy confidently
- Carry security and state hygiene forward into every later module

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Modules — Creating Reusable Infrastructure](modules-creating-reusable-infrastructure.md)
- Next: [Meta-Arguments — count, for_each, and lifecycle](meta-arguments-count-for-each-and-lifecycle.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
