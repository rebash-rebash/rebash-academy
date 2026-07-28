---
title: HCL Fundamentals — Blocks, Arguments, and Expressions
description: "Learn HCL block anatomy, types, expressions, and a clean multi-file root module layout you will reuse for the rest of the track."
difficulty: beginner
estimated_time: "45 min"
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

HashiCorp Configuration Language (HCL) is how you declare infrastructure. Unlike general-purpose languages, HCL is optimised for **blocks of configuration** with arguments, nested blocks, and expressions that reference other objects.

This tutorial builds fluency with block types, labels, types, collections, references, and a multi-file layout. You will compose `local` and `random` so one resource’s attributes feed another — the pattern every real stack depends on.

This is **Tutorial 3** in **Module 1: Foundations** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Identify terraform, variable, resource, data, output, and locals blocks
- [ ] Differentiate arguments (you set) from attributes (provider exports)
- [ ] Write typed expressions for strings, numbers, bools, lists, maps, and objects
- [ ] Reference resources with address syntax like `local_file.demo.content`
- [ ] Organise a root module across `versions.tf`, `variables.tf`, `main.tf`, and `outputs.tf`
- [ ] Use locals and heredocs without unnecessary string interpolation

## Prerequisites

- Completed [Installing Terraform and the CLI Workflow](installing-terraform-and-the-cli-workflow.md)
- Terraform CLI **1.9+** installed (1.15.x recommended)
- Network access for first-time provider downloads
- Ability to create directories and edit files

## Architecture

HCL configuration is a graph of blocks. Values flow from variables and locals into resource arguments; providers export attributes that other resources and outputs consume.

![Architecture diagram for HCL Fundamentals — Blocks, Arguments, and Expressions](../assets/images/terraform-hcl-blocks.svg)

| Construct | Role in the graph |
|-----------|-------------------|
| **Variables** | Inputs from humans, CI, or calling modules |
| **Locals** | Derived values computed once inside the module |
| **Resources** | Managed objects with arguments in and attributes out |
| **Outputs** | Values published after apply |
| **Expressions** | Glue: references, functions, conditionals |

## Theory

### Anatomy of a block

```hcl
resource "local_file" "demo" {
  filename = "${path.module}/hello.txt"
  content  = "hello"
}
```

- **Block type** — `resource`
- **Labels** — provider type `local_file`, local name `demo`
- **Body** — arguments inside `{ }`

The full address becomes `local_file.demo`. Attributes hang off that address after plan/apply, for example `local_file.demo.content_md5`.

### Common block types

| Block | Purpose |
|-------|---------|
| `terraform { }` | CLI version and required providers |
| `variable` | Module input |
| `locals` | Named intermediate expressions |
| `resource` | Something Terraform creates and updates |
| `data` | Read-only lookup of an existing object |
| `output` | Module export |
| `module` | Nested child module call (later tutorials) |
| `provider` | Authentication and regional settings |

### Arguments vs attributes

| Kind | Who sets it | When known | Example |
|------|-------------|------------|---------|
| Argument | You in configuration | At plan time (or from variables) | `filename`, `content` |
| Attribute | Provider after read/apply | Often unknown until apply | `content_md5`, `id` |

Referencing an attribute automatically creates a dependency edge. You do not write “create random_id first” — Terraform’s graph does.

### Types

- **Primitives:** `string`, `number`, `bool`
- **Collections:** `list(T)`, `set(T)`, `map(T)`
- **Structural:** `object({ ... })`, `tuple([ ... ])`
- **Special:** `any` — avoid in module interfaces; prefer precise types so mistakes fail at plan time

Lists preserve order and allow duplicates. Sets are unordered and unique. Maps are string-keyed. Objects group named fields of potentially different types — ideal for structured settings.

### Expressions and references

- Interpolation: `"prefix-${var.name}"` when building larger strings
- Pure references: `var.name`, `local.filename` — no `${}` required when the whole expression is a reference
- Resource attributes: `local_file.notes.content`, `random_id.suffix.hex`
- Paths: `path.module` (this module’s directory), `path.root` (root module), `path.cwd` (process working directory)

Prefer `path.module` for files the module owns. `path.cwd` changes if someone runs Terraform from another directory with `-chdir`, which surprises teams.

### File layout convention

| File | Contents |
|------|----------|
| `versions.tf` | `terraform` + `required_providers` |
| `variables.tf` | input variables |
| `main.tf` / focused `*.tf` | resources and module calls |
| `outputs.tf` | outputs |
| `locals.tf` | local values (optional separate file) |
| `terraform.tfvars` | values (often gitignored if sensitive) |
| `terraform.tfvars.example` | safe sample values committed to Git |

Terraform loads every `*.tf` file in the directory — filenames are convention, not syntax.

### String and heredoc patterns

Prefer direct references over unnecessary interpolation:

```hcl
# Prefer
content = var.message

# Only interpolate when building a larger string
content = "env=${var.environment} message=${var.message}"
```

Heredocs (`<<-EOT` … `EOT`) keep multi-line templates readable. The `<<-` form strips leading indentation matching the closing marker’s indent, which keeps nested HCL tidy under `terraform fmt`.

### Functions, sensitivity, and formatting

Reach for `join`, `length`, and `format` inside `locals` rather than repeating them across resources. Mark secret variables `sensitive = true` when you introduce them; set `nullable = false` when `null` must be rejected. HCL comments use `#`, `//`, or `/* */`. Let `terraform fmt` own whitespace — do not fight the formatter in pull requests.

## Hands-on Lab

You will build a multi-file root module that joins a list of owners, generates a short random suffix, and writes a notes file whose content depends on both.

### Step 1 – Create the working directory

```bash
mkdir -p ~/rebash-tf-hcl && cd ~/rebash-tf-hcl
terraform version
```

**Expected:** Terraform 1.9+ available from the previous tutorial.

### Step 2 – Write `versions.tf`

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
      version = "~> 3.7"
    }
  }
}
```

**Expected:** Both `hashicorp/local` and `hashicorp/random` declared. As of this writing, `local` latest is **2.9.0** and `random` latest is **3.9.0** — `~> 3.7` admits the current 3.9.x line without jumping to 4.x.

### Step 3 – Write `variables.tf`

```hcl
variable "project" {
  description = "Project key used in the generated notes filename"
  type        = string
  default     = "rebash"
}

variable "owners" {
  description = "Team owners recorded in the notes artefact"
  type        = list(string)
  default     = ["platform", "sre"]
}

variable "environment" {
  description = "Short environment label embedded in the notes body"
  type        = string
  default     = "lab"

  validation {
    condition     = contains(["lab", "dev", "staging", "prod"], var.environment)
    error_message = "environment must be one of: lab, dev, staging, prod."
  }
}
```

**Expected:** Typed inputs with descriptions; `environment` rejects arbitrary strings at plan time.

### Step 4 – Write `main.tf` with locals and resources

```hcl
locals {
  owner_line = join(", ", var.owners)
  filename   = "${path.module}/generated/${var.project}-notes.txt"
  header     = "REBASH Academy HCL lab (${var.environment})"
}

resource "random_id" "suffix" {
  byte_length = 2
}

resource "local_file" "notes" {
  filename = local.filename
  content  = <<-EOT
    ${local.header}
    project = ${var.project}
    owners  = ${local.owner_line}
    suffix  = ${random_id.suffix.hex}
  EOT
  file_permission = "0644"
}
```

**Expected:** Locals derive reusable strings; `random_id` feeds `local_file` through `random_id.suffix.hex`.

### Step 5 – Write `outputs.tf`

```hcl
output "notes_path" {
  description = "Path to the managed notes file"
  value       = local_file.notes.filename
}

output "suffix" {
  description = "Hex suffix generated by random_id"
  value       = random_id.suffix.hex
}

output "owner_count" {
  description = "Number of owners recorded in the notes file"
  value       = length(var.owners)
}
```

### Step 6 – Initialise, plan, and apply

```bash
terraform fmt
terraform init -input=false
terraform validate
terraform plan -input=false -out=tfplan
terraform apply -input=false tfplan
cat generated/rebash-notes.txt
terraform output
```

**Expected:** Providers download; plan creates `random_id.suffix` and `local_file.notes`; notes file lists project, owners, and a four-character hex suffix; outputs print path, suffix, and owner count `2`.

### Step 7 – Exercise types (optional)

Set `owners = ["platform", "sre", "security"]` in `terraform.tfvars`, apply, and confirm `owner_count` is `3`. Temporarily set `environment = "qa"` to see the validation error, then revert to `"lab"`.

### Step 8 – Clean up

```bash
terraform destroy -input=false -auto-approve
```

**Expected:** Notes file and random resource removed from state and disk.

## Code Walkthrough

### `required_providers` entries

| Argument | Purpose |
|----------|---------|
| `source` | Registry address (`hashicorp/local`, `hashicorp/random`) |
| `version` | Constraint admitting compatible releases without accidental major bumps |

### `variable` arguments

| Argument | Purpose |
|----------|---------|
| `description` | Human-readable contract for the input |
| `type` | `string` or `list(string)` — rejects wrong shapes early |
| `default` | Lab defaults; omit in production when the value must be supplied |
| `validation.condition` | Boolean expression that must be true |
| `validation.error_message` | Clear failure text for operators |

### `locals` values

`owner_line`, `filename`, and `header` derive reusable strings. Locals are not caller inputs — use them for joins and names you do not want overridden.

### `random_id.suffix`

| Argument | Purpose |
|----------|---------|
| `byte_length` | Number of random bytes; `2` yields four hex characters via `.hex` |

Exported attributes include `hex`, `b64_url`, and `dec`. Referencing any of them creates the dependency edge into `local_file`.

### `local_file.notes`

| Argument | Purpose |
|----------|---------|
| `filename` | Destination path from `local.filename` |
| `content` | Heredoc body mixing locals, variables, and `random_id.suffix.hex` |
| `file_permission` | POSIX mode for the created file |

### `output` blocks

| Output | Value source |
|--------|--------------|
| `notes_path` | Resource attribute `filename` |
| `suffix` | Resource attribute `hex` |
| `owner_count` | Expression `length(var.owners)` — no resource required |

### Locals vs variables

Variables are caller inputs; locals are internal derived values. Do not expose joins callers should never override.

## Validation

```bash
terraform fmt -check
terraform init -input=false
terraform validate
terraform apply -input=false -auto-approve
terraform output
test -f generated/rebash-notes.txt
grep -q "owners" generated/rebash-notes.txt
terraform destroy -input=false -auto-approve
```

| Check | Pass criteria |
|-------|----------------|
| Layout | Separate `versions.tf`, `variables.tf`, `main.tf`, `outputs.tf` |
| Types | `owners` is `list(string)`; validate/plan fails if you pass a bare string |
| Validation block | Invalid `environment` fails with your `error_message` |
| Outputs | `notes_path`, `suffix`, and `owner_count` print after apply |
| Content | Notes file includes header, project, owners, and hex suffix |

## Best Practices

- One concern per file (`variables.tf`, `outputs.tf`) so diffs stay reviewable
- Give every variable a `type` and `description` before the module leaves your laptop
- Prefer precise types over `any` — especially on module input variables
- Use `locals` for derived values; do not make callers pass the same `join` repeatedly
- Prefer pure references over unnecessary `"${...}"` interpolation
- Put `validation` blocks on variables that encode organisation policy

## Security Considerations

- Do not put secrets in defaults or committed `.tfvars`; mark them `sensitive = true`
- Avoid writing credentials into `local_file` content — bad habits transfer
- Constrain filename inputs; remember state stores attribute values including file content

## Common Mistakes

!!! warning "Treating attributes as arguments before apply"
    Values may be unknown until plan/apply. **Fix:** Reference attributes and let Terraform propagate dependencies.

!!! warning "Using `any` everywhere"
    Hides mistakes until runtime in a child module. **Fix:** Type variables and outputs precisely.

!!! warning "One giant `main.tf`"
    Hard reviews and merge conflicts. **Fix:** Split by concern early even for small roots.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Unexpected type error | List vs string mismatch | Match `type` constraints; fix `.tfvars` |
| Invalid reference | Typo in resource name | Check address spelling; use editor autocomplete |
| Heredoc markers in output | Wrong delimiter indent | Use `<<-` and align the closing marker |
| fmt churn in PRs | Mixed editor settings | Run `terraform fmt` before every commit |
| Validation always fails | Over-strict `condition` | Test the expression in `terraform console` |

## Interview Questions

1. What is the difference between an argument and an attribute in HCL?
   *Arguments are values you set in configuration; attributes are values the provider exports after read or apply.*

2. When should you use a local value instead of a variable?
   *Use locals for derived values callers should not override; use variables for tunables supplied from outside.*

3. Why avoid `any` in module input variables?
   *Precise types catch mistakes at plan time instead of failing deep inside nested expressions later.*

4. How does resource address syntax work (`local_file.notes.content`)?
   *Type label, local name, then attribute — forming a graph edge to that resource.*

5. What do `path.module`, `path.root`, and `path.cwd` mean?
   *Module directory, root module directory, and the process working directory respectively.*

6. How would you express a map of tags with a type constraint?
   *`type = map(string)` or an `object({ ... })` when keys and nested types are fixed.*

7. Why split root modules across multiple `.tf` files?
   *Reviews stay focused; Terraform still merges the directory into one module configuration.*

8. What happens if you omit `type` on a variable?
   *Terraform admits more shapes; errors surface later and module contracts become unclear.*

9. How do heredocs help with multi-line templates?
   *They keep readable multi-line content in configuration without awkward escaped newlines.*

10. What is the difference between `list` and `set`?
    *Lists are ordered and may contain duplicates; sets are unique and unordered.*

11. How does `terraform fmt` affect code review quality?
    *It removes style debates so reviewers focus on behaviour and safety.*

12. Give an example of unnecessary string interpolation and the cleaner form.
    *Prefer `content = var.message` over `content = "${var.message}"` when no surrounding text is needed.*

## Summary

- HCL is block-oriented: type, labels, and a body of arguments
- Distinguishing arguments from attributes prevents “where did that value come from?” confusion
- Typed variables, validation blocks, and locals keep modules readable and safe
- A conventional multi-file layout scales from labs to production roots
- Resource references (`random_id.suffix.hex`) are how Terraform composes infrastructure without imperative scripts

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Installing Terraform and the CLI Workflow](installing-terraform-and-the-cli-workflow.md)
- Next: [Providers and the Terraform Plugin Model](providers-and-the-terraform-plugin-model.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Terraform language](https://developer.hashicorp.com/terraform/language)
2. [Expressions](https://developer.hashicorp.com/terraform/language/expressions)
3. [Type constraints](https://developer.hashicorp.com/terraform/language/expressions/type-constraints)
4. [Local values](https://developer.hashicorp.com/terraform/language/values/locals)
5. [hashicorp/random — random_id](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/id)
6. [hashicorp/local — local_file](https://registry.terraform.io/providers/hashicorp/local/latest/docs/resources/file)
7. [Terraform Registry](https://registry.terraform.io/)
