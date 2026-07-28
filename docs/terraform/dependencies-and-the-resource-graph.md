---
title: Dependencies and the Resource Graph
description: "Terraform builds a dependency graph to order operations. Most edges are implicit from references. Explicit `depends_on` is for hidden relationships. M"
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

!!! warning "Sprinkling depends_on everywhere"
    Opaque graphs. **Fix:** Prefer references.

!!! warning "Routine -target applies"
    Drift and missing resources. **Fix:** Apply the full graph.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider download fails | Network/registry blocked | Check access to registry.terraform.io |
| validate fails before init | Providers not installed | Run `terraform init` |
| Unexpected replace | ForceNew argument change | Read plan carefully; use moved/for_each wisely |
| State locked | Another apply in progress | Wait or follow backend unlock procedures carefully |
| Permission denied writing files | Directory permissions | Ensure workspace is writable |

## Interview Questions

1. What problem does Dependencies and the Resource Graph solve in a Terraform workflow?
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

- Terraform builds a dependency graph to order operations. Most edges are implicit from references. Explicit `depends_on` is for hidden relationships. Misusing `-target` or ignoring destroy order causes subtle production outages.
- Practice the lab until `fmt` / `validate` / `plan` are muscle memory
- Carry forward provider pins, sensitive handling, and plan-before-apply discipline

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Resources and Data Sources](resources-and-data-sources.md)
- Next: [Terraform State Fundamentals](terraform-state-fundamentals.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
