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

Terraform expressions include a rich function library. `templatefile` keeps large text maintainable, and `dynamic` blocks generate nested blocks from collections when providers require them.

This is **Tutorial 14** in **Module 4: Language Power Tools** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Use common functions (join, merge, try, templatefile)
- [ ] Render files with templatefile and template variables
- [ ] Write a dynamic block safely
- [ ] Prefer clarity over clever one-liners
- [ ] Know where to find the function reference

## Prerequisites

- Completed Meta-Arguments — count, for_each, and lifecycle

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Functions, Templates, and Dynamic Blocks](../assets/images/terraform-functions.svg)


## Theory

### Essential functions

`join`, `split`, `merge`, `lookup`, `try`, `can`, `coalesce`, `length`, `keys`, `values`,
`toset`, `tomap`, `jsonencode`, `yamlencode`, `file`, `templatefile`.

### `templatefile`

```hcl
templatefile("${path.module}/app.tftpl", {
  name = var.name
})
```

### `dynamic`

Use sparingly when a resource expects repeated nested blocks. Overuse harms readability.

### Why this topic matters in production

Teams that skip **functions, templates, and dynamic blocks** eventually pay in outages: unreviewable plans, brittle
refactors, or secrets leaking into logs. Treat this tutorial as the minimum bar for merging
Terraform changes on a shared state file.

### Practical mental model

1. Write the smallest config that proves the idea
2. `fmt` / `validate` / `plan` until the diff matches your intent
3. Apply only after you can explain every create/update/replace line
4. Destroy lab resources so the next exercise starts clean

## Hands-on Lab

```bash
mkdir -p ~/rebash-tf-fn && cd ~/rebash-tf-fn
cat > app.tftpl <<'EOF'
# App config
name=${name}
owners=${owners}
EOF
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

variable "name" { type = string default = "checkout" }
variable "owners" { type = list(string) default = ["platform", "app"] }

locals {
  rendered = templatefile("${path.module}/app.tftpl", {
    name   = var.name
    owners = join(",", var.owners)
  })
}

resource "local_file" "app" {
  filename = "${path.module}/app.conf"
  content  = local.rendered
}
```

```bash
terraform init -input=false && terraform apply -input=false -auto-approve
cat app.conf
terraform destroy -input=false -auto-approve
```

## Code Walkthrough

Templates keep HCL free of giant heredocs and allow reuse across environments.


Re-read every argument in the lab through the lens of **functions, templates, and dynamic blocks**.
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
| Topic focus | You can explain how this lab demonstrates functions, templates, and dynamic blocks |
| Cleanup | Destroy (or documented teardown) left no stray lab files |

## Best Practices

- Keep examples small enough to run without cloud credentials unless the topic requires otherwise
- Document assumptions (CLI version, providers, working directory) at the top of the root module
- Prefer explicitness over cleverness when teaching **functions, templates, and dynamic blocks**
- Add CI checks (`fmt`, `validate`, plan) as soon as a root is shared
- Write outputs that help the next human debug, not just the next machine

## Security Considerations

- Assume state and plan output may contain secrets related to **functions, templates, and dynamic blocks**
- Use least-privilege credentials whenever a provider needs authentication
- Do not commit tfvars with real secrets; use examples with placeholders
- Review plans for unexpected destroys before apply
- Limit who can unlock state and who can approve production applies

## Common Mistakes

!!! warning "Calling file() on missing paths"
    Plan fails. **Fix:** Ensure files exist or use template modules.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| validate fails | Missing init or syntax error | Run `terraform init`, read the file:line in the error |
| Plan shows replace unexpectedly | ForceNew argument changed | Confirm intent; use moved/lifecycle if refactoring |
| Provider auth errors | Credentials not available | Export the documented env vars for the provider |
| Topic confusion around functions, templates, and dynamic blocks | Skipped theory | Re-read Theory, then re-run the lab from a clean directory |
| Leftover lab files | Destroy skipped | Re-run destroy or delete the lab directory after state cleanup |

## Interview Questions

1. Name five functions you use weekly and why.
2. When is templatefile better than inline heredocs?
3. What are the dangers of dynamic blocks?
4. How do you flatten nested collections?
5. When should you prefer a static block over dynamic?
6. How does try() change error behaviour?
7. What is compact() useful for?
8. How do you build a map of tags with merge?
9. When is lookup() appropriate versus direct indexing?
10. How do template directives differ from HCL expressions?
11. Why keep complex transforms in locals?
12. How would you unit-test pure transformations?

## Summary

- Master **functions, templates, and dynamic blocks** before moving to the next tutorial in the track
- Every shared root needs formatting, validation, and a reviewed plan
- Prefer small, reversible labs that you can destroy confidently
- Carry security and state hygiene forward into every later module

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Meta-Arguments — count, for_each, and lifecycle](meta-arguments-count-for-each-and-lifecycle.md)
- Next: [Import, Moved, and Safe Refactors](import-moved-and-safe-refactors.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
