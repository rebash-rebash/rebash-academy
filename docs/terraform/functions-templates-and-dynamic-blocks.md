---
title: "Functions, Templates, and Dynamic Blocks"
description: "Use Terraform conditionals, for expressions, built-in functions, templatefile, and dynamic blocks without over-abstracting production HCL."
difficulty: intermediate
estimated_time: "45–60 min"
technology: terraform
category: terraform
module: "Module 10 · Expressions & Functions"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - functions
  - expressions
prerequisites:
  - terraform/registry-modules-and-composition
next:
  - terraform/data-sources-and-existing-infrastructure
related:
  - terraform/hcl-fundamentals-blocks-arguments-and-expressions
  - terraform/resources-dependencies-and-meta-arguments
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - functions
  - templates
  - dynamic-blocks
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Functions, Templates, and Dynamic Blocks

## Overview

Apply conditionals, `for` expressions, common built-in functions, `templatefile`, and a controlled `dynamic` block — keeping transforms in `locals` for reviewability.

Terraform expressions include a rich **function library**, collection transforms (`for`), and **`dynamic` blocks** for nested provider schema. Large multi-line artefacts belong in **`templatefile`** so HCL stays readable. Prefer clarity over clever one-liners.

This is a core tutorial in **Module 10 · Expressions & Functions** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Registry Modules and Composition](registry-modules-and-composition.md)
- Terraform CLI 1.9+

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Write conditionals and `for` expressions  
- [ ] Use `join`, `merge`, `try`, `jsonencode`, `templatefile`  
- [ ] Generate nested blocks with `dynamic` when needed  
- [ ] Keep complex transforms in `locals`

## Architecture

This topic’s control points and relationships are shown below.

![Expressions and functions](../assets/excalidraw/terraform-expressions.svg)

## Theory

### What it is

**Functions** transform values at plan time (`join`, `merge`, `coalesce`, `try`, `lookup`, `jsonencode`, `templatefile`, and many more). **Conditionals** use the ternary form `condition ? true_val : false_val`. **`for` expressions** build lists and maps from collections. **`dynamic` blocks** expand repeated nested blocks (for example ingress rules) from a collection when the resource schema requires that shape. **`templatefile(path, vars)`** renders a `.tftpl` file with a variables map — ideal for configs, policies, and userdata.

### Why it matters

Production modules tag resources, build policy documents, and optionalise features per environment. Doing that with readable `locals` beats copying half-edited JSON through six roots. Overusing `dynamic` and nested `for` expressions makes reviews slow and plans hard to reason about — the same failure mode as “clever” Helm templates. Functions are free at plan time; mistakes still become production outages if nobody can explain the expression.

### How it works

1. Compute derived values in `locals` (merged tags, filtered lists, rendered templates).
2. Pass locals into resource arguments — resources stay thin.
3. Use `for` to map/filter: `[for o in var.owners : upper(o)]` or `{ for k, v in var.apps : k => v.port }`.
4. Call `templatefile("${path.module}/app.tftpl", { name = var.name })` for multi-line text.
5. Reach for `dynamic "block_name" { for_each = ... content { ... } }` only when the provider schema needs repeated nested blocks and a static block list would be worse.

Gate optional resources with `count` / `for_each`. Use `try(expr, default)` sparingly so you do not hide real errors.

### Key concepts and comparisons

| Construct | Role |
|-----------|------|
| Ternary | Simple branching of values |
| `for` expression | Build list/map from a collection |
| Built-in function | Encode, merge, join, lookup, … |
| `templatefile` | Multi-line rendered artefacts |
| `dynamic` | Nested schema blocks from `for_each` |

Prefer named locals over nested in-resource pipelines; static blocks when N is tiny; `templatefile` for policies instead of giant heredocs.

### Common pitfalls

- Treating `dynamic` as the default for every optional setting.
- Expressions reviewers cannot explain in thirty seconds.
- Using `try` to silence missing required attributes.
- Template variable names in `.tftpl` not matching the vars map keys.
- Confusing `for` expressions with the `for_each` meta-argument.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-terraform/module-10/expressions/out && cd ~/rebash-terraform/module-10/expressions/out
```

**Focus:** hands-on practice for Functions, Templates, and Dynamic Blocks

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-terraform/module-10/expressions/out
cd ~/rebash-terraform/module-10/expressions

cat > app.tftpl << 'EOF'
# app=${name} env=${env}
owners=${owners_csv}
EOF

cat > versions.tf << 'EOF'
terraform {
  required_version = ">= 1.9.0"
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.9" }
  }
}
EOF

cat > main.tf << 'EOF'
variable "env" {
  type    = string
  default = "dev"
}
variable "owners" {
  type    = list(string)
  default = ["alice", "bob"]
}
variable "extra_tags" {
  type    = map(string)
  default = { team = "platform" }
}

locals {
  is_prod     = var.env == "prod"
  base_tags   = merge({ env = var.env, managed = "terraform" }, var.extra_tags)
  owners_csv  = join(",", [for o in var.owners : upper(o)])
  rendered    = templatefile("${path.module}/app.tftpl", {
    name       = "demo"
    env        = var.env
    owners_csv = local.owners_csv
  })
  markers = { for o in var.owners : o => "owner-${o}" }
}

resource "local_file" "config" {
  filename = "${path.module}/out/app.conf"
  content  = local.rendered
}

resource "terraform_data" "owner" {
  for_each = local.markers
  input    = each.value
}

output "tags"       { value = local.base_tags }
output "owners_csv" { value = local.owners_csv }
output "is_prod"    { value = local.is_prod }
EOF

terraform init -input=false
terraform apply -input=false -auto-approve
cat out/app.conf
terraform output
terraform destroy -input=false -auto-approve
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-terraform/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-terraform/module-10/expressions/out/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Functions, Templates, and Dynamic Blocks** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for terraform as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Treating `dynamic` as the default for every optional setting."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Expressions reviewers cannot explain in thirty seconds."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Functions, Templates, and Dynamic Blocks changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |

## Summary

**Functions, Templates, and Dynamic Blocks** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Functions, Templates, and Dynamic Blocks** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Data Sources and Existing Infrastructure](data-sources-and-existing-infrastructure.md)

## References

- [Functions](https://developer.hashicorp.com/terraform/language/functions)  
- [for Expressions](https://developer.hashicorp.com/terraform/language/expressions/for)  
- [dynamic Blocks](https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks)  
- [templatefile](https://developer.hashicorp.com/terraform/language/functions/templatefile)
