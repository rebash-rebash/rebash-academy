---
title: Providers and the Terraform Plugin Model
description: "Providers are plugins that implement resources and data sources for a platform (AWS, Azure,"
difficulty: beginner
estimated_time: "35 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - providers
  - registry
prerequisites:
  - Completed HCL Fundamentals
  - Network access to registry.terraform.io
comments: false
---

# Providers and the Terraform Plugin Model

## Overview

Providers are plugins that implement resources and data sources for a platform (AWS, Azure,
Kubernetes, local files, and hundreds more). Terraform core does not know how to call cloud
APIs — providers do.

This tutorial explains `required_providers`, version constraints, the lock file, provider
configuration, aliases, and how `terraform init` fetches plugins from the Registry.

This is **Tutorial 4** in **Module 1: Foundations** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Declare providers with source addresses and version constraints
- [ ] Explain the role of `.terraform.lock.hcl`
- [ ] Configure provider blocks and describe alias use-cases
- [ ] Run `terraform providers` and interpret the dependency tree
- [ ] Pin providers safely using pessimistic constraints (`~>`)

## Prerequisites

- Completed HCL Fundamentals
- Network access to registry.terraform.io

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Providers and the Terraform Plugin Model](../assets/images/terraform-providers.svg)


## Theory

### Provider addresses

Format: `<namespace>/<name>` on the Registry, e.g. `hashicorp/local`, `hashicorp/aws`.

### Version constraints

| Constraint | Meaning |
|------------|---------|
| `~> 2.9` | >= 2.9.0 and < 3.0.0 |
| `>= 6.0.0, < 7.0.0` | Explicit range |
| `= 2.9.0` | Exact pin |

Root modules should pin with `~>`. As of this writing: `hashicorp/local` **2.9.0**,
`hashicorp/aws` **6.56.0**, `hashicorp/random` **3.9.0** — always re-check the Registry.

### Provider configuration

```hcl
provider "aws" {
  region = "eu-west-1"
}

provider "aws" {
  alias  = "dr"
  region = "eu-central-1"
}
```

Pass aliases into modules with a `providers` map when a child must talk to a non-default
provider instance.

### Built-in provider

`terraform_data` and `terraform_remote_state` use Terraform’s built-in provider — no
`required_providers` entry required for those resources alone.

## Hands-on Lab

```bash
mkdir -p ~/rebash-tf-providers && cd ~/rebash-tf-providers
```

```hcl
# versions.tf
terraform {
  required_version = ">= 1.9.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.9"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.9"
    }
  }
}

# main.tf
resource "random_pet" "server" {
  length = 2
}

resource "local_file" "inventory" {
  filename        = "${path.module}/inventory.txt"
  content         = "hostname = ${random_pet.server.id}\n"
  file_permission = "0644"
}

output "hostname" {
  value = random_pet.server.id
}
```

```bash
terraform init -input=false
terraform providers
terraform apply -input=false -auto-approve
cat inventory.txt
# Deliberate upgrade path awareness (do not blindly upgrade prod):
# terraform init -upgrade
terraform destroy -input=false -auto-approve
```

## Code Walkthrough

### Lock file

After init, `.terraform.lock.hcl` records selected versions and checksums. Commit it so every
engineer and CI runner resolves the same plugins.

### `init -upgrade`

Asks Terraform to reconsider versions within constraints. Review the lockfile diff like any
dependency bump.

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

!!! warning "Omitting `required_providers`"
    Old implicit behavior is gone. **Fix:** Always declare source + version.

!!! warning "Floating on latest with no constraint"
    Surprise breaking upgrades. **Fix:** Use `~>` in root modules.

!!! warning "Hard-coding credentials in provider blocks"
    Secret leakage. **Fix:** Use env vars, OIDC, or shared config files.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider download fails | Network/registry blocked | Check access to registry.terraform.io |
| validate fails before init | Providers not installed | Run `terraform init` |
| Unexpected replace | ForceNew argument change | Read plan carefully; use moved/for_each wisely |
| State locked | Another apply in progress | Wait or follow backend unlock procedures carefully |
| Permission denied writing files | Directory permissions | Ensure workspace is writable |

## Interview Questions

1. What problem does Providers and the Terraform Plugin Model solve in a Terraform workflow?
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

- Providers are plugins that implement resources and data sources for a platform (AWS, Azure,
- Practice the lab until `fmt` / `validate` / `plan` are muscle memory
- Carry forward provider pins, sensitive handling, and plan-before-apply discipline

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [HCL Fundamentals — Blocks, Arguments, and Expressions](hcl-fundamentals-blocks-arguments-and-expressions.md)
- Next: [Variables, Locals, and Outputs](variables-locals-and-outputs.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
