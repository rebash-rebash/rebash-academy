---
title: Import, Moved, and Safe Refactors
description: "Refactoring should not mean recreate-the-world. Modern Terraform supports `import` blocks and `moved` blocks so you can adopt existing objects and ren"
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - import
  - moved
prerequisites:
  - Completed Functions, Templates, and Dynamic Blocks
comments: false
---

# Import, Moved, and Safe Refactors

## Overview

Refactoring should not mean recreate-the-world. Modern Terraform supports `import` blocks and `moved` blocks so you can adopt existing objects and rename addresses without destroy/create.

This is **Tutorial 15** in **Module 4: Language Power Tools** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Import existing objects into state
- [ ] Rename addresses with moved blocks
- [ ] Read plans to confirm no destructive changes
- [ ] Describe removed blocks at a high level
- [ ] Refactor modules without downtime where possible

## Prerequisites

- Completed Functions, Templates, and Dynamic Blocks

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Import, Moved, and Safe Refactors](../assets/images/terraform-refactor.svg)


## Theory

### `import` block

```hcl
import {
  to = local_file.adopted
  id = "/absolute/or/provider-specific/id"
}
```

### `moved` block

```hcl
moved {
  from = local_file.old
  to   = local_file.new
}
```

Plan should show **move** / no-op rather than destroy+create.

## Hands-on Lab

```bash
mkdir -p ~/rebash-tf-move && cd ~/rebash-tf-move
```

First apply as `local_file.old`, then add a `moved` block to `local_file.new` and change the resource name accordingly. Confirm:

```bash
terraform plan
# expect: move / update in-place, not destroy
```

Full starter:

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

resource "local_file" "new" {
  filename = "${path.module}/moved.txt"
  content  = "safe-refactor\n"
}

moved {
  from = local_file.old
  to   = local_file.new
}
```

(Create `old` first without the moved block, apply, then rename.)

## Code Walkthrough

moved updates state addresses; the real file is untouched when filename arguments stay equal.

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

!!! warning "Renaming without moved"
    Destroy+create. **Fix:** Always add moved when changing addresses.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider download fails | Network/registry blocked | Check access to registry.terraform.io |
| validate fails before init | Providers not installed | Run `terraform init` |
| Unexpected replace | ForceNew argument change | Read plan carefully; use moved/for_each wisely |
| State locked | Another apply in progress | Wait or follow backend unlock procedures carefully |
| Permission denied writing files | Directory permissions | Ensure workspace is writable |

## Interview Questions

1. What problem does Import, Moved, and Safe Refactors solve in a Terraform workflow?
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

- Refactoring should not mean recreate-the-world. Modern Terraform supports `import` blocks and `moved` blocks so you can adopt existing objects and rename addresses without destroy/create.
- Practice the lab until `fmt` / `validate` / `plan` are muscle memory
- Carry forward provider pins, sensitive handling, and plan-before-apply discipline

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Functions, Templates, and Dynamic Blocks](functions-templates-and-dynamic-blocks.md)
- Next: [Format, Validate, and Terraform Test](format-validate-and-terraform-test.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
