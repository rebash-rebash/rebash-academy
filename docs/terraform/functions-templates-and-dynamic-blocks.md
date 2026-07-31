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

**Focus:** Use functions, templatestring/templatefile patterns, and dynamic blocks

### Step 1 – Build dynamic content

```bash
cat > greeting.tftpl <<'EOF'
Hello, ${name}!
EOF
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
}
variable "names" {
  type    = list(string)
  default = ["alpha", "beta"]
}
resource "local_file" "greetings" {
  for_each = toset(var.names)
  filename = "${path.module}/hi-${each.key}.txt"
  content  = templatefile("${path.module}/greeting.tftpl", { name = each.key })
}
locals {
  upper_names = [for n in var.names : upper(n)]
}
output "upper_names" { value = local.upper_names }
EOF
terraform init
```

### Step 2 – Apply and verify rendered files

```bash
terraform apply -auto-approve
cat hi-alpha.txt hi-beta.txt
terraform output
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
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


1. What is `templatefile` useful for?
2. How does `for_each` differ from `dynamic` blocks?
3. When should you prefer explicit resources over dynamic blocks?
4. What readability trade-offs do nested functions create in reviews?
5. Give an example of a safe use of `tonumber` or `try`.

!!! tip "Sample answer — question 2"
    `for_each` creates multiple resource instances; `dynamic` generates nested blocks inside one resource. Use dynamic for repeated nested arguments like ingress rules.

!!! tip "Sample answer — question 4"
    Heavy nesting hides intent. Prefer locals with names, smaller templates, and tests so security-relevant values stay reviewable.



## Related Tutorials



- [Course overview](index.md)
- [Data Sources and Existing Infrastructure](data-sources-and-existing-infrastructure.md)



## References



- [Functions](https://developer.hashicorp.com/terraform/language/functions)  
- [for Expressions](https://developer.hashicorp.com/terraform/language/expressions/for)  
- [dynamic Blocks](https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks)  
- [templatefile](https://developer.hashicorp.com/terraform/language/functions/templatefile)
