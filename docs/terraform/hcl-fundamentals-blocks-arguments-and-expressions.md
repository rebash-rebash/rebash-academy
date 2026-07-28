---
title: HCL Fundamentals — Blocks, Arguments, and Expressions
description: "HashiCorp Configuration Language (HCL) is how you declare infrastructure. Unlike general-purpose"
difficulty: beginner
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - hcl
  - language
prerequisites:
  - Completed Installing Terraform and the CLI Workflow
  - Terraform 1.9+ installed
comments: false
---

# HCL Fundamentals — Blocks, Arguments, and Expressions

## Overview

HashiCorp Configuration Language (HCL) is how you declare infrastructure. Unlike general-purpose
languages, HCL is optimized for **blocks of configuration** with arguments, nested blocks, and
expressions that reference other objects.

This tutorial builds fluency: block types, labels, types, strings, collections, references, and
a clean multi-file layout you will reuse for the rest of the track.

This is **Tutorial 3** in **Module 1: Foundations** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Identify terraform, variable, resource, data, output, and locals blocks
- [ ] Differentiate arguments (you set) from attributes (provider exports)
- [ ] Write typed expressions for strings, numbers, bools, lists, maps, and objects
- [ ] Reference resources with address syntax like local_file.demo.content
- [ ] Organize a root module across versions.tf, variables.tf, main.tf, outputs.tf

## Prerequisites

- Completed Installing Terraform and the CLI Workflow
- Terraform 1.9+ installed

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for HCL Fundamentals — Blocks, Arguments, and Expressions](../assets/images/terraform-hcl-blocks.svg)


## Theory

### Anatomy of a block

```hcl
resource "local_file" "demo" {
  filename = "${path.module}/hello.txt"
  content  = "hello"
}
```

- **Block type** — `resource`
- **Labels** — provider type `local_file`, name `demo`
- **Body** — arguments inside `{ }`

### Arguments vs attributes

| Kind | Who sets it | Example |
|------|-------------|---------|
| Argument | You in config | `filename`, `content` |
| Attribute | Provider after apply | `content_md5`, `id` |

### Types

- Primitives: `string`, `number`, `bool`
- Collections: `list(T)`, `set(T)`, `map(T)`
- Structural: `object({...})`, `tuple([...])`
- Special: `any` (avoid in modules — prefer precise types)

### Expressions and references

- Interpolation: `"prefix-${var.name}"` (often unnecessary for pure references)
- References: `var.x`, `local.y`, `local_file.demo.content`, `module.vpc.vpc_id`
- Paths: `path.module`, `path.root`, `path.cwd`

### File layout convention

| File | Contents |
|------|----------|
| `versions.tf` | `terraform` + `required_providers` |
| `variables.tf` | input variables |
| `main.tf` / `*.tf` | resources and modules |
| `outputs.tf` | outputs |
| `locals.tf` | local values (optional) |
| `terraform.tfvars` | values (often gitignored if sensitive) |

## Hands-on Lab

```bash
mkdir -p ~/rebash-tf-hcl && cd ~/rebash-tf-hcl
```

`versions.tf`:

```hcl
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
```

`variables.tf`:

```hcl
variable "project" {
  type        = string
  description = "Project key used in filenames"
  default     = "rebash"
}

variable "owners" {
  type        = list(string)
  description = "Team owners recorded in the artifact"
  default     = ["platform", "sre"]
}
```

`main.tf`:

```hcl
locals {
  owner_line = join(", ", var.owners)
  filename   = "${path.module}/generated/${var.project}-notes.txt"
}

resource "random_id" "suffix" {
  byte_length = 2
}

resource "local_file" "notes" {
  filename = local.filename
  content  = <<-EOT
    project = ${var.project}
    owners  = ${local.owner_line}
    suffix  = ${random_id.suffix.hex}
  EOT
  file_permission = "0644"
}
```

`outputs.tf`:

```hcl
output "notes_path" {
  value = local_file.notes.filename
}

output "suffix" {
  value = random_id.suffix.hex
}
```

```bash
terraform init -input=false
terraform apply -input=false -auto-approve
cat generated/rebash-notes.txt
terraform destroy -input=false -auto-approve
```

## Code Walkthrough

### `locals`

Locals derive values once and reuse them — clearer than repeating `join(...)` everywhere.

### `random_id`

Demonstrates a managed resource that exports attributes (`hex`) consumed by another resource —
the core of Terraform composition.

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

!!! warning "Treating attributes as arguments before apply"
    Unknown values until plan/apply. **Fix:** Reference attributes; let Terraform propagate dependencies.

!!! warning "Using `any` everywhere"
    Hides mistakes. **Fix:** Type variables and outputs precisely.

!!! warning "One giant `main.tf`"
    Hard reviews. **Fix:** Split by concern early.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider download fails | Network/registry blocked | Check access to registry.terraform.io |
| validate fails before init | Providers not installed | Run `terraform init` |
| Unexpected replace | ForceNew argument change | Read plan carefully; use moved/for_each wisely |
| State locked | Another apply in progress | Wait or follow backend unlock procedures carefully |
| Permission denied writing files | Directory permissions | Ensure workspace is writable |

## Interview Questions

1. What problem does HCL Fundamentals — Blocks, Arguments, and Expressions solve in a Terraform workflow?
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

- HashiCorp Configuration Language (HCL) is how you declare infrastructure. Unlike general-purpose
- Practice the lab until `fmt` / `validate` / `plan` are muscle memory
- Carry forward provider pins, sensitive handling, and plan-before-apply discipline

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Installing Terraform and the CLI Workflow](installing-terraform-and-the-cli-workflow.md)
- Next: [Providers and the Terraform Plugin Model](providers-and-the-terraform-plugin-model.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
