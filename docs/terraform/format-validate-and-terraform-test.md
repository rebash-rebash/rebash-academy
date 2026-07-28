---
title: Format, Validate, and Terraform Test
description: "Quality gates keep infrastructure changes safe: canonical formatting, static validation, and `terraform test` for module behavior. Wire them into CI b"
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - testing
  - fmt
prerequisites:
  - Completed Import, Moved, and Safe Refactors
comments: false
---

# Format, Validate, and Terraform Test

## Overview

Quality gates keep infrastructure changes safe: canonical formatting, static validation, and `terraform test` for module behavior. Wire them into CI before any apply job.

This is **Tutorial 16** in **Module 5: Quality and Security** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Use terraform fmt and fmt -check
- [ ] Run terraform validate after init
- [ ] Author *.tftest.hcl tests with assertions
- [ ] Integrate gates into CI
- [ ] Interpret test failures

## Prerequisites

- Completed Import, Moved, and Safe Refactors

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Format, Validate, and Terraform Test](../assets/images/terraform-test.svg)


## Theory

### terraform test

Test files use `run` blocks to execute plans/applies against a module and `assert` conditions on outputs.

```hcl
run "ok" {
  command = apply
  assert {
    condition     = output.path != ""
    error_message = "path should be set"
  }
}
```

## Hands-on Lab

### Step 1 – Module under test

```bash
mkdir -p ~/rebash-tf-test/modules/hello/tests
cd ~/rebash-tf-test
```

`modules/hello/versions.tf`:

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

`modules/hello/variables.tf`:

```hcl
variable "name" {
  type = string
}
```

`modules/hello/main.tf`:

```hcl
resource "local_file" "hello" {
  filename = "${path.module}/hello-${var.name}.txt"
  content  = "hello ${var.name}\n"
}

output "path" {
  value = local_file.hello.filename
}

output "name" {
  value = var.name
}
```

### Step 2 – Terraform test file

`modules/hello/tests/basic.tftest.hcl`:

```hcl
variables {
  name = "rebash"
}

run "creates_greeting" {
  command = apply

  assert {
    condition     = output.name == "rebash"
    error_message = "name output should echo the variable"
  }

  assert {
    condition     = length(output.path) > 0
    error_message = "path output must be non-empty"
  }
}
```

### Step 3 – Run tests and fmt/validate

```bash
terraform -chdir=modules/hello fmt
terraform -chdir=modules/hello init -input=false
terraform -chdir=modules/hello validate
terraform -chdir=modules/hello test
```

**Expected:** test run passes with apply + assertions.

## Code Walkthrough

Tests should be deterministic: avoid random providers unless you assert on patterns, not exact IDs.

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

!!! warning "Only formatting in CI"
    Invalid configs merge. **Fix:** fmt + validate + test + plan.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider download fails | Network/registry blocked | Check access to registry.terraform.io |
| validate fails before init | Providers not installed | Run `terraform init` |
| Unexpected replace | ForceNew argument change | Read plan carefully; use moved/for_each wisely |
| State locked | Another apply in progress | Wait or follow backend unlock procedures carefully |
| Permission denied writing files | Directory permissions | Ensure workspace is writable |

## Interview Questions

1. What problem does Format, Validate, and Terraform Test solve in a Terraform workflow?
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

- Quality gates keep infrastructure changes safe: canonical formatting, static validation, and `terraform test` for module behavior. Wire them into CI before any apply job.
- Practice the lab until `fmt` / `validate` / `plan` are muscle memory
- Carry forward provider pins, sensitive handling, and plan-before-apply discipline

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Import, Moved, and Safe Refactors](import-moved-and-safe-refactors.md)
- Next: [Secrets and Sensitive Values](secrets-and-sensitive-values.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
