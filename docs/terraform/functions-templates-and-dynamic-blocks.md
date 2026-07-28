---
title: Functions, Templates, and Dynamic Blocks
description: "Apply Terraform functions, templatestring/templatefile, and dynamic blocks without over-abstracting."
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - functions
  - templates
prerequisites:
  - Completed Meta-Arguments — count, for_each, and lifecycle
comments: false
---

# Functions, Templates, and Dynamic Blocks

## Overview

Terraform expressions include a rich **function library** for transforming collections, encoding JSON, and rendering text. Large multi-line artefacts belong in **`templatefile`** (or Terraform 1.9+ `templatestring`) so HCL stays readable. **`dynamic` blocks** generate nested provider blocks from collections when a resource schema requires repetition — use them sparingly so modules remain reviewable.

This tutorial builds a small root that joins owners, merges tags, renders an `app.tftpl` template into a managed file, and shows a controlled `dynamic` pattern using `terraform_data` markers. Prefer clarity over clever one-liners: if a reviewer cannot explain a `for` expression in thirty seconds, simplify it.

This is **Tutorial 14** in **Module 4: Language Power Tools** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Use common functions (`join`, `merge`, `try`, `templatefile`, `jsonencode`)
- [ ] Render files with `templatefile` and template variables
- [ ] Write a `dynamic` block safely and know when a static block is better
- [ ] Keep complex transforms in `locals` for testability
- [ ] Find and read the official function reference

## Prerequisites

- Completed [Meta-Arguments — count, for_each, and lifecycle](meta-arguments-count-for-each-and-lifecycle.md)
- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files
- No cloud account required

## Architecture

Functions and templates transform inputs before they reach resources. Dynamic blocks expand nested schema blocks from collections at plan time. Everything still flows through the same resource graph.

![Architecture diagram for Functions, Templates, and Dynamic Blocks](../assets/images/terraform-functions.svg)

| Layer | Role |
|-------|------|
| **Variables** | Raw inputs from humans or CI |
| **Locals + functions** | Pure transforms (join, merge, encode) |
| **Templates** | Multi-line rendered text |
| **Resources** | Persist results (`local_file`, markers) |
| **Dynamic blocks** | Generate nested blocks when schemas demand them |

## Theory

### Essential functions

| Category | Examples | Typical use |
|----------|----------|-------------|
| Strings | `join`, `split`, `format`, `replace`, `trimspace` | Labels, paths, CSV-ish lists |
| Collections | `merge`, `concat`, `flatten`, `distinct`, `compact`, `chunklist` | Tags, lists of CIDRs |
| Maps | `keys`, `values`, `lookup`, `tomap` | Tag maps, optional keys |
| Types | `tostring`, `tonumber`, `toset`, `tolist` | Coercion at boundaries |
| Encoding | `jsonencode`, `jsondecode`, `yamlencode`, `base64encode` | Config files, user_data |
| Files | `file`, `fileexists`, `templatefile` | Bundled templates |
| Safety | `try`, `can`, `coalesce`, `coalescelist` | Optional attributes |

Always prefer the [Functions reference](https://developer.hashicorp.com/terraform/language/functions) over memory — signatures evolve carefully but behaviour details matter.

### `templatefile`

```hcl
templatefile("${path.module}/app.tftpl", {
  name   = var.name
  owners = join(",", var.owners)
})
```

- First argument: path to a `.tftpl` (convention) file
- Second argument: map of variables visible inside the template
- Templates support `${...}` interpolation and `%{ for }` / `%{ if }` directives

Keep business logic in HCL `locals`; keep presentation in the template. Do not bury critical conditionals only inside templates if operators never open those files.

### `templatestring` (Terraform 1.9+)

Renders a string template without a separate file — useful for short snippets. Prefer `templatefile` when content is multi-line or shared across modules.

### `dynamic` blocks

```hcl
dynamic "setting" {
  for_each = var.settings
  content {
    name  = setting.key
    value = setting.value
  }
}
```

Use when a provider resource expects **repeated nested blocks** and the set is data-driven. Overuse harms readability: three static blocks are often clearer than a clever dynamic. Never use `dynamic` merely to look advanced.

### `try` and `can`

- `try(expr, fallback)` — evaluate `expr`, return fallback on error
- `can(expr)` — boolean success check

Useful for optional object fields. Overuse hides real type errors — prefer precise types and validation blocks when you control the schema.

### Why this topic matters in production

Opaque one-liners become unmaintainable during incidents. Teams that skip disciplined functions and templates pay with unreviewable plans and brittle refactors. Put transforms in named `locals`, assert outputs in tests (next quality tutorials), and keep templates free of secrets.

### Practical mental model

1. Transform in `locals` with named steps
2. Render text with `templatefile` when heredocs grow unwieldy
3. Reach for `dynamic` only when the schema forces repeated blocks
4. `fmt` / `validate` / `plan` until the rendered artefact matches intent

## Hands-on Lab

You will create `app.tftpl`, render it through locals, write `app.conf` with the `local` provider, and attach a `terraform_data` marker that records a content hash.

### Step 1 – Create the working directory and template

```bash
mkdir -p ~/rebash-tf-fn && cd ~/rebash-tf-fn
terraform version
```

Create `app.tftpl`:

```bash
cat > app.tftpl <<'EOF'
# App config — rendered by Terraform templatefile
name=${name}
owners=${owners}
environment=${environment}
tags_json=${tags_json}
suffix=${suffix}
EOF
```

**Expected:** Template file present beside future `.tf` files; placeholders use template variable names, not `var.*`.

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

### Step 3 – Write `variables.tf`

```hcl
variable "name" {
  description = "Application name embedded in the rendered config"
  type        = string
  default     = "checkout"
}

variable "owners" {
  description = "Owning teams listed in the config"
  type        = list(string)
  default     = ["platform", "app"]
}

variable "environment" {
  description = "Environment label"
  type        = string
  default     = "lab"
}

variable "extra_tags" {
  description = "Additional tags merged into the standard set"
  type        = map(string)
  default     = {
    CostCentre = "academy"
  }
}
```

### Step 4 – Write `main.tf`

```hcl
resource "random_id" "suffix" {
  byte_length = 2
}

locals {
  base_tags = {
    Project     = "rebash-academy"
    ManagedBy   = "terraform"
    Environment = var.environment
  }

  tags = merge(local.base_tags, var.extra_tags)

  owners_csv = join(",", var.owners)

  rendered = templatefile("${path.module}/app.tftpl", {
    name        = var.name
    owners      = local.owners_csv
    environment = var.environment
    tags_json   = jsonencode(local.tags)
    suffix      = random_id.suffix.hex
  })

  # Example of try/coalesce style safety for optional maps
  cost_centre = try(local.tags["CostCentre"], "unset")
}

resource "local_file" "app" {
  filename        = "${path.module}/app.conf"
  content         = local.rendered
  file_permission = "0644"
}

resource "terraform_data" "render_marker" {
  input = {
    sha     = sha1(local.rendered)
    app     = var.name
    owners  = length(var.owners)
    centre  = local.cost_centre
  }
}

output "app_path" {
  description = "Path to the rendered application config"
  value       = local_file.app.filename
}

output "tags" {
  description = "Merged tag map used in the template"
  value       = local.tags
}

output "render_marker" {
  description = "Hash and metadata for the rendered content"
  value       = terraform_data.render_marker.output
}
```

**Expected:** Locals derive tags and CSV owners; template receives only primitive/string values; `local_file` persists the render.

### Step 5 – Initialise, apply, and inspect

```bash
terraform fmt
terraform init -input=false
terraform validate
terraform plan -input=false -out=tfplan
terraform apply -input=false tfplan
cat app.conf
terraform output -json tags
terraform output render_marker
```

**Expected:** `app.conf` shows name `checkout`, owners `platform,app`, environment `lab`, a JSON tags object including `CostCentre`, and a four-character hex suffix. Marker output includes a SHA1 and `centre = "academy"`.

### Step 6 – Change inputs and re-plan

Create `terraform.tfvars`:

```hcl
name     = "payments"
owners   = ["platform", "app", "security"]
extra_tags = {
  CostCentre = "payments"
  Tier       = "critical"
}
```

```bash
terraform plan -input=false
```

**Expected:** Update in-place for `local_file.app` and `terraform_data.render_marker` (new hash). Apply and confirm `owners=platform,app,security` and tags include `Tier`.

```bash
terraform apply -input=false -auto-approve
grep owners app.conf
```

### Step 7 – Optional dynamic-block sketch (read and understand)

Dynamic blocks need a resource schema with nested blocks. The `local` provider’s `local_file` has none — so production patterns often appear on cloud resources (security group rules, inline policies). Conceptually:

```hcl
# Illustrative only — not applied in this lab
dynamic "ingress" {
  for_each = var.ingress_rules
  content {
    from_port = ingress.value.port
    protocol  = ingress.value.protocol
  }
}
```

For this lab, treat `merge` + `templatefile` as the practical equivalent of “generate structured content from a collection” without forcing an unnatural dynamic.

### Step 8 – Clean up

```bash
terraform destroy -input=false -auto-approve
```

**Expected:** `app.conf` removed; state cleared.

## Code Walkthrough

### `merge` and tag composition

| Expression | Purpose |
|------------|---------|
| `local.base_tags` | Organisation defaults |
| `merge(local.base_tags, var.extra_tags)` | Caller overrides / extensions win on key conflicts |
| `try(local.tags["CostCentre"], "unset")` | Safe read when a key might be absent |

### `templatefile` arguments

| Template var | Source |
|--------------|--------|
| `name` | `var.name` |
| `owners` | `join(",", var.owners)` via local |
| `tags_json` | `jsonencode(local.tags)` — templates receive strings, not raw objects, unless you use directives carefully |
| `suffix` | `random_id.suffix.hex` |

### `local_file.app`

Persists the rendered string. In shared CI, prefer cloud objects; locally it is perfect for learning template hygiene.

### `terraform_data.render_marker`

Stores a SHA1 of the rendered body so plans show when template inputs change even if you are not grepping the file. Prefer this over `null_resource` + `local-exec`.

### Why not a giant heredoc in `main.tf`?

Templates keep HCL focused on structure, allow reuse across environments, and make diffs of prose/config clearer in Git.

## Validation

```bash
terraform fmt -check
terraform init -input=false
terraform validate
terraform apply -input=false -auto-approve
test -f app.conf
grep -q "name=checkout" app.conf || grep -q "name=payments" app.conf
grep -q "CostCentre" app.conf
terraform output -json render_marker | head
terraform destroy -input=false -auto-approve
```

| Check | Pass criteria |
|-------|----------------|
| Template | `app.tftpl` exists and uses `${name}` style vars |
| Render | `app.conf` matches inputs after apply |
| Tags | JSON in file includes merged keys |
| Marker | `render_marker` output includes `sha` |
| Cleanup | Destroy removes managed file |

## Best Practices

- Name intermediate locals (`owners_csv`, `tags`) instead of nesting five functions inline
- Keep secrets out of templates; mark sensitive variables and avoid writing tokens to disk
- Prefer `templatefile` for multi-line artefacts; heredocs for short strings
- Use `merge` for tags with documented precedence (defaults first, overrides second)
- Reach for `dynamic` only when static blocks would duplicate beyond readability
- Put pure transforms where `terraform test` can assert them (next tutorials)

## Security Considerations

- `templatefile` and `file` read from disk at plan time — do not point them at secret paths in CI logs without redaction
- `jsonencode` of sensitive values still lands in state when assigned to resources
- Never `join` passwords into world-readable `local_file` content
- Review template directives for accidental inclusion of entire secret maps
- Treat plan JSON containing rendered user-data as sensitive artefacts

## Common Mistakes

!!! warning "Calling file() or templatefile() on missing paths"
    Plan fails immediately. **Fix:** Commit templates with the module; use `path.module`; fail CI if files are missing.

!!! warning "Passing complex objects into templates carelessly"
    Confusing render errors. **Fix:** Pass strings/`jsonencode` results; keep loops in HCL or explicit template directives.

!!! warning "Dynamic blocks for everything"
    Unreadable modules. **Fix:** Three static blocks beat an opaque dynamic for small fixed sets.

!!! warning "try() swallowing real type bugs"
    Silent wrong values. **Fix:** Use precise types; reserve `try` for truly optional external shapes.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Invalid template interpolation value` | Non-string passed into template | `tostring` / `jsonencode` / `join` before render |
| Template variable not found | Typo between map key and `${...}` | Align names exactly; re-read `templatefile` second argument |
| `merge` override surprise | Later maps win on duplicate keys | Document precedence; put defaults first |
| Plan always replaces file | Content includes unstable values | Avoid `timestamp()` unless intentional; prefer `random_id` kept in state |
| Functions unknown | Very old Terraform | Upgrade to 1.9+ for this track |

## Interview Questions

1. Name five functions you use weekly and why.
   *Typical set: `merge` for tags, `join` for lists, `jsonencode` for configs, `templatefile` for files, `try` for optional fields.*

2. When is `templatefile` better than inline heredocs?
   *When content is multi-line, reused, or clearer to review as a standalone artefact.*

3. What are the dangers of dynamic blocks?
   *Reduced readability, harder reviews, and subtle for_each mistakes that expand the wrong nested blocks.*

4. How do you flatten nested collections?
   *Use `flatten` on lists of lists, or `for` expressions that project nested structures into a flat list/map.*

5. When should you prefer a static block over dynamic?
   *When the nested set is small, fixed, and clearer written explicitly.*

6. How does `try()` change error behaviour?
   *It returns a fallback instead of failing the plan when the expression errors — useful and easy to abuse.*

7. What is `compact()` useful for?
   *Removing empty strings from a list before joins or resource expansion.*

8. How do you build a map of tags with `merge`?
   *`merge(local.defaults, var.extra_tags)` so caller keys override defaults on conflicts.*

9. When is `lookup()` appropriate versus direct indexing?
   *`lookup(map, key, default)` when absence is normal; `map[key]` when the key must exist.*

10. How do template directives differ from HCL expressions?
    *Directives (`%{ for }`, `%{ if }`) control generation inside the template file; HCL expressions run in `.tf` before render.*

11. Why keep complex transforms in locals?
    *Named steps are reusable, testable, and easier to explain in code review.*

12. How would you unit-test pure transformations?
    *Expose them via outputs or module outputs and assert with `terraform test` run blocks.*

## Summary

- Functions transform data; put them in named locals for clarity
- `templatefile` keeps large text maintainable and reviewable
- Use `dynamic` blocks only when provider schemas require repeated nested blocks
- Prefer explicitness over cleverness — production modules are read under pressure
- Encode tags and ownership with `merge` and typed variables, not copy-paste

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Meta-Arguments — count, for_each, and lifecycle](meta-arguments-count-for-each-and-lifecycle.md)
- Next: [Import, Moved, and Safe Refactors](import-moved-and-safe-refactors.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Functions](https://developer.hashicorp.com/terraform/language/functions)
2. [templatefile](https://developer.hashicorp.com/terraform/language/functions/templatefile)
3. [Dynamic Blocks](https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks)
4. [Strings and Templates](https://developer.hashicorp.com/terraform/language/expressions/strings)
5. [terraform_data resource](https://developer.hashicorp.com/terraform/language/resources/terraform-data)
6. [hashicorp/local provider](https://registry.terraform.io/providers/hashicorp/local/latest)
7. [hashicorp/random provider](https://registry.terraform.io/providers/hashicorp/random/latest)
