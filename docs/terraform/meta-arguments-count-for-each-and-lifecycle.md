---
title: Meta-Arguments — count, for_each, and lifecycle
description: "Use count and for_each correctly, manage lifecycle rules, and avoid indexed address traps."
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - for_each
  - lifecycle
prerequisites:
  - Completed Registry Modules and Composition
comments: false
---

# Meta-Arguments — count, for_each, and lifecycle

## Overview

Meta-arguments change how resources are instantiated and updated. Prefer `for_each` over `count` for most cases, and use `lifecycle` to control create/destroy behaviour safely.

This is **Tutorial 13** in **Module 4: Language Power Tools** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Choose for_each vs count correctly
- [ ] Reference each.key / each.value
- [ ] Apply lifecycle create_before_destroy and ignore_changes judiciously
- [ ] Explain prevent_destroy blast-radius effects
- [ ] Avoid count index churn when lists reorder

## Prerequisites

- Completed Registry Modules and Composition

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Meta-Arguments — count, for_each, and lifecycle](../assets/images/terraform-meta-arguments.svg)


## Theory

### `for_each` (preferred)

```hcl
for_each = toset(["a", "b"])
# each.key, each.value
```

Maps/sets give stable addresses (`resource["a"]`) unlike `count` indices.

### `lifecycle`

- `create_before_destroy`
- `prevent_destroy`
- `ignore_changes`
- `replace_triggered_by`
- `precondition` / `postcondition`

### Why this topic matters in production

Teams that skip **meta-arguments count, for_each, and lifecycle** eventually pay in outages: unreviewable plans, brittle
refactors, or secrets leaking into logs. Treat this tutorial as the minimum bar for merging
Terraform changes on a shared state file.

### Practical mental model

1. Write the smallest config that proves the idea
2. `fmt` / `validate` / `plan` until the diff matches your intent
3. Apply only after you can explain every create/update/replace line
4. Destroy lab resources so the next exercise starts clean

## Hands-on Lab

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

variable "files" {
  type    = map(string)
  default = {
    alpha = "content-a"
    beta  = "content-b"
  }
}

resource "local_file" "set" {
  for_each = var.files
  filename = "${path.module}/out/${each.key}.txt"
  content  = "${each.value}\n"

  lifecycle {
    ignore_changes = [file_permission]
  }
}
```

```bash
mkdir -p out
terraform init -input=false && terraform apply -input=false -auto-approve
terraform state list
terraform destroy -input=false -auto-approve
```

## Code Walkthrough

Removing a map key destroys only that instance — the core advantage over count indices.


Re-read every argument in the lab through the lens of **meta-arguments count, for_each, and lifecycle**.
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
| Topic focus | You can explain how this lab demonstrates meta-arguments count, for_each, and lifecycle |
| Cleanup | Destroy (or documented teardown) left no stray lab files |

## Best Practices

- Keep examples small enough to run without cloud credentials unless the topic requires otherwise
- Document assumptions (CLI version, providers, working directory) at the top of the root module
- Prefer explicitness over cleverness when teaching **meta-arguments count, for_each, and lifecycle**
- Add CI checks (`fmt`, `validate`, plan) as soon as a root is shared
- Write outputs that help the next human debug, not just the next machine

## Security Considerations

- Assume state and plan output may contain secrets related to **meta-arguments count, for_each, and lifecycle**
- Use least-privilege credentials whenever a provider needs authentication
- Do not commit tfvars with real secrets; use examples with placeholders
- Review plans for unexpected destroys before apply
- Limit who can unlock state and who can approve production applies

## Common Mistakes

!!! warning "Using count with unordered lists that change"
    Mass replacement. **Fix:** Use for_each with maps/sets.

!!! warning "ignore_changes on everything"
    Drift blindness. **Fix:** Ignore only externally mutated attributes.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| validate fails | Missing init or syntax error | Run `terraform init`, read the file:line in the error |
| Plan shows replace unexpectedly | ForceNew argument changed | Confirm intent; use moved/lifecycle if refactoring |
| Provider auth errors | Credentials not available | Export the documented env vars for the provider |
| Topic confusion around meta-arguments count, for_each, and lifecycle | Skipped theory | Re-read Theory, then re-run the lab from a clean directory |
| Leftover lab files | Destroy skipped | Re-run destroy or delete the lab directory after state cleanup |

## Interview Questions

1. When is for_each preferable to count?
2. Why are count index addresses fragile when lists shrink?
3. How do you migrate from count to for_each?
4. What does ignore_changes do, and when is it a smell?
5. How does create_before_destroy help zero downtime?
6. What is prevent_destroy used for?
7. How do lifecycle blocks interact with replacements?
8. How do you set for_each over a set of strings?
9. What is each.key versus each.value?
10. How does count = 0 disable a resource?
11. Why avoid splat expressions on resources that use for_each?
12. How would you add a lifecycle rule safely in production?

## Summary

- Master **meta-arguments count, for_each, and lifecycle** before moving to the next tutorial in the track
- Every shared root needs formatting, validation, and a reviewed plan
- Prefer small, reversible labs that you can destroy confidently
- Carry security and state hygiene forward into every later module

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Registry Modules and Composition](registry-modules-and-composition.md)
- Next: [Functions, Templates, and Dynamic Blocks](functions-templates-and-dynamic-blocks.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
