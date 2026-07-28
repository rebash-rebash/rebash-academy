---
title: Meta-Arguments — count, for_each, and lifecycle
description: "Meta-arguments change how resources are instantiated and updated. Prefer `for_each` over `count` for most cases, and use `lifecycle` to control create"
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

Meta-arguments change how resources are instantiated and updated. Prefer `for_each` over `count` for most cases, and use `lifecycle` to control create/destroy behavior safely.

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

!!! warning "Using count with unordered lists that change"
    Mass replacement. **Fix:** Use for_each with maps/sets.

!!! warning "ignore_changes on everything"
    Drift blindness. **Fix:** Ignore only externally mutated attributes.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider download fails | Network/registry blocked | Check access to registry.terraform.io |
| validate fails before init | Providers not installed | Run `terraform init` |
| Unexpected replace | ForceNew argument change | Read plan carefully; use moved/for_each wisely |
| State locked | Another apply in progress | Wait or follow backend unlock procedures carefully |
| Permission denied writing files | Directory permissions | Ensure workspace is writable |

## Interview Questions

1. What problem does Meta-Arguments — count, for_each, and lifecycle solve in a Terraform workflow?
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

- Meta-arguments change how resources are instantiated and updated. Prefer `for_each` over `count` for most cases, and use `lifecycle` to control create/destroy behavior safely.
- Practice the lab until `fmt` / `validate` / `plan` are muscle memory
- Carry forward provider pins, sensitive handling, and plan-before-apply discipline

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Registry Modules and Composition](registry-modules-and-composition.md)
- Next: [Functions, Templates, and Dynamic Blocks](functions-templates-and-dynamic-blocks.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
