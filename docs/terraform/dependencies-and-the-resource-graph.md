---
title: Dependencies and the Resource Graph
description: "Read implicit dependencies from references, use depends_on carefully, and trigger replacements with replace_triggered_by."
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - graph
  - depends_on
prerequisites:
  - Completed Resources and Data Sources
comments: false
---

# Dependencies and the Resource Graph

## Overview

Terraform builds a dependency graph to order operations. Most edges are implicit from references. Explicit `depends_on` is for hidden relationships. Misusing `-target` or ignoring destroy order causes subtle production outages.

This is **Tutorial 7** in **Module 2: Core Building Blocks** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Contrast implicit vs explicit dependencies
- [ ] Predict create and destroy ordering
- [ ] Use depends_on only when required
- [ ] Explain risks of terraform apply -target
- [ ] Trigger replacement with replace_triggered_by and terraform_data

## Prerequisites

- Completed Resources and Data Sources

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Dependencies and the Resource Graph](../assets/images/terraform-resource-graph.svg)


## Theory

### Implicit dependencies

Referencing `local_file.a.content` inside `local_file.b` creates an edge `a → b`.

### Explicit `depends_on`

Use when there is a real ordering need **without** an attribute reference (for example, an API that must exist before a side-effect resource runs). Prefer references when possible — they document data flow.

### `-target`

Limits the graph for emergencies. It can leave infrastructure half-applied. Never make it a habit in CI.

### `replace_triggered_by`

Lifecycle meta-argument that forces replacement when another resource changes — often paired with `terraform_data`.

### Why this topic matters in production

Teams that skip **the resource graph and replacement triggers** eventually pay in outages: unreviewable plans, brittle
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

resource "local_file" "first" {
  filename = "${path.module}/1.txt"
  content  = "first\n"
}

resource "local_file" "second" {
  filename = "${path.module}/2.txt"
  content  = "second depends on ${local_file.first.filename}\n"
}

resource "terraform_data" "after_second" {
  input      = local_file.second.content_md5
  depends_on = [local_file.second]
}
```

```bash
terraform init -input=false
terraform graph | head
terraform apply -input=false -auto-approve
terraform destroy -input=false -auto-approve
```

## Code Walkthrough

`terraform graph` emits DOT. Implicit edges appear because `second` references `first`.


Re-read every argument in the lab through the lens of **the resource graph and replacement triggers**.
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
| Topic focus | You can explain how this lab demonstrates the resource graph and replacement triggers |
| Cleanup | Destroy (or documented teardown) left no stray lab files |

## Best Practices

- Keep examples small enough to run without cloud credentials unless the topic requires otherwise
- Document assumptions (CLI version, providers, working directory) at the top of the root module
- Prefer explicitness over cleverness when teaching **the resource graph and replacement triggers**
- Add CI checks (`fmt`, `validate`, plan) as soon as a root is shared
- Write outputs that help the next human debug, not just the next machine

## Security Considerations

- Assume state and plan output may contain secrets related to **the resource graph and replacement triggers**
- Use least-privilege credentials whenever a provider needs authentication
- Do not commit tfvars with real secrets; use examples with placeholders
- Review plans for unexpected destroys before apply
- Limit who can unlock state and who can approve production applies

## Common Mistakes

!!! warning "Sprinkling depends_on everywhere"
    Opaque graphs. **Fix:** Prefer references.

!!! warning "Routine -target applies"
    Drift and missing resources. **Fix:** Apply the full graph.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| validate fails | Missing init or syntax error | Run `terraform init`, read the file:line in the error |
| Plan shows replace unexpectedly | ForceNew argument changed | Confirm intent; use moved/lifecycle if refactoring |
| Provider auth errors | Credentials not available | Export the documented env vars for the provider |
| Topic confusion around the resource graph and replacement triggers | Skipped theory | Re-read Theory, then re-run the lab from a clean directory |
| Leftover lab files | Destroy skipped | Re-run destroy or delete the lab directory after state cleanup |

## Interview Questions

1. How does Terraform build the dependency graph?
2. When is explicit depends_on necessary?
3. What are the risks of unnecessary depends_on?
4. How does replace_triggered_by work with terraform_data?
5. What is the difference between update in place and replace?
6. How do you read a cycle error?
7. Why might parallelism settings matter?
8. How do module boundaries affect the graph?
9. When do provisioners create hidden dependencies?
10. How does -target affect the graph (and why avoid it)?
11. What is create_before_destroy used for?
12. How would you force replacement of a resource safely?

## Summary

- Master **the resource graph and replacement triggers** before moving to the next tutorial in the track
- Every shared root needs formatting, validation, and a reviewed plan
- Prefer small, reversible labs that you can destroy confidently
- Carry security and state hygiene forward into every later module

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Resources and Data Sources](resources-and-data-sources.md)
- Next: [Terraform State Fundamentals](terraform-state-fundamentals.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
