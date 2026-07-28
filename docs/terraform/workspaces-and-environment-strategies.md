---
title: Workspaces and Environment Strategies
description: "Workspaces isolate state for the same configuration. They are useful for light isolation, but many teams prefer separate directories or repositories f"
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - workspaces
  - environments
prerequisites:
  - Completed Remote State and Backends
comments: false
---

# Workspaces and Environment Strategies

## Overview

Workspaces isolate state for the same configuration. They are useful for light isolation, but many teams prefer separate directories or repositories for prod. Learn both and choose deliberately.

This is **Tutorial 10** in **Module 3: Collaboration and Scale** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Create and select Terraform workspaces
- [ ] Use terraform.workspace in expressions
- [ ] Explain state isolation per workspace
- [ ] Compare workspaces vs separate root modules
- [ ] Avoid using workspaces as a substitute for proper blast-radius separation

## Prerequisites

- Completed Remote State and Backends

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Workspaces and Environment Strategies](../assets/images/terraform-workspaces.svg)


## Theory

### CLI

```bash
terraform workspace list
terraform workspace new dev
terraform workspace select dev
```

### When workspaces fit

- Same backend, multiple ephemeral review environments
- Homogeneous regions with tiny deltas

### When to prefer separate roots

- Different providers/accounts for prod
- Different teams/approvers
- Strong blast-radius isolation

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

resource "local_file" "env" {
  filename = "${path.module}/env-${terraform.workspace}.txt"
  content  = "workspace = ${terraform.workspace}\n"
}
```

```bash
terraform init -input=false
terraform workspace new dev || terraform workspace select dev
terraform apply -input=false -auto-approve
terraform workspace new staging || terraform workspace select staging
terraform apply -input=false -auto-approve
ls env-*.txt
terraform workspace select default
```

## Code Walkthrough

Each workspace has its own state key; selecting `staging` does not destroy `dev` objects.

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

!!! warning "One workspace for prod and dev in same account without guardrails"
    Easy to apply wrong env. **Fix:** Separate accounts or strong CI protections.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider download fails | Network/registry blocked | Check access to registry.terraform.io |
| validate fails before init | Providers not installed | Run `terraform init` |
| Unexpected replace | ForceNew argument change | Read plan carefully; use moved/for_each wisely |
| State locked | Another apply in progress | Wait or follow backend unlock procedures carefully |
| Permission denied writing files | Directory permissions | Ensure workspace is writable |

## Interview Questions

1. What problem does Workspaces and Environment Strategies solve in a Terraform workflow?
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

- Workspaces isolate state for the same configuration. They are useful for light isolation, but many teams prefer separate directories or repositories for prod. Learn both and choose deliberately.
- Practice the lab until `fmt` / `validate` / `plan` are muscle memory
- Carry forward provider pins, sensitive handling, and plan-before-apply discipline

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Remote State and Backends](remote-state-and-backends.md)
- Next: [Modules — Creating Reusable Infrastructure](modules-creating-reusable-infrastructure.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
