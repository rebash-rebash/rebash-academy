---
title: Policy as Code Overview
description: "Policy as code blocks unsafe plans before apply. Compare OPA/Conftest with HashiCorp Sentinel, and practice evaluating a Terraform plan JSON against a"
difficulty: advanced
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - policy
  - opa
prerequisites:
  - Completed Secrets and Sensitive Values
comments: false
---

# Policy as Code Overview

## Overview

Policy as code blocks unsafe plans before apply. Compare OPA/Conftest with HashiCorp Sentinel, and practice evaluating a Terraform plan JSON against a simple Rego rule.

This is **Tutorial 18** in **Module 5: Quality and Security** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain policy-as-code in the Terraform workflow
- [ ] Contrast OPA and Sentinel
- [ ] Generate terraform show -json plans
- [ ] Write a basic Rego denial rule
- [ ] Place policy checks in CI before apply

## Prerequisites

- Completed Secrets and Sensitive Values

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Policy as Code Overview](../assets/images/terraform-policy.svg)


## Theory

### Placement

`fmt → validate → plan → **policy** → apply`

### Engines

| Engine | Typical home |
|--------|----------------|
| OPA / Conftest | Any CI |
| Sentinel | HCP Terraform / TFE |

### Plan JSON

```bash
terraform plan -out=tfplan
terraform show -json tfplan > plan.json
```

## Hands-on Lab

### Step 1 – Configuration + plan JSON

```bash
mkdir -p ~/rebash-tf-policy/policy
cd ~/rebash-tf-policy
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

resource "local_file" "allow" {
  filename = "${path.module}/allow.txt"
  content  = "ok\n"
}
```

```bash
terraform init -input=false
terraform plan -input=false -out=tfplan
terraform show -json tfplan > plan.json
head -c 200 plan.json; echo
```

### Step 2 – Example Rego policy

`policy/deny_deletes.rego`:

```rego
package terraform.policy

import future.keywords.if
import future.keywords.in

deny[msg] if {
  some rc in input.resource_changes
  rc.type == "local_file"
  "delete" in rc.change.actions
  msg := sprintf("deleting local_file %s is blocked by lab policy", [rc.address])
}
```

### Step 3 – Evaluate (if OPA installed)

```bash
# Install from https://www.openpolicyagent.org/docs/latest/#running-opa
opa eval --format pretty -i plan.json -d policy/ 'data.terraform.policy.deny'
```

Empty deny set means the plan is allowed. Re-run after a destroy plan to see denials.

### Sentinel note

On HCP Terraform, Sentinel policies run against the same plan data using HashiCorp’s policy language. The **placement** in the pipeline is identical: after plan, before apply.

## Code Walkthrough

Start with deny-by-default for high-risk actions (public SG rules, unencrypted state buckets) and expand gradually.

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

!!! warning "Policies only in wiki"
    Unenforced. **Fix:** Execute in CI on every plan.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider download fails | Network/registry blocked | Check access to registry.terraform.io |
| validate fails before init | Providers not installed | Run `terraform init` |
| Unexpected replace | ForceNew argument change | Read plan carefully; use moved/for_each wisely |
| State locked | Another apply in progress | Wait or follow backend unlock procedures carefully |
| Permission denied writing files | Directory permissions | Ensure workspace is writable |

## Interview Questions

1. What problem does Policy as Code Overview solve in a Terraform workflow?
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

- Policy as code blocks unsafe plans before apply. Compare OPA/Conftest with HashiCorp Sentinel, and practice evaluating a Terraform plan JSON against a simple Rego rule.
- Practice the lab until `fmt` / `validate` / `plan` are muscle memory
- Carry forward provider pins, sensitive handling, and plan-before-apply discipline

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Secrets and Sensitive Values](secrets-and-sensitive-values.md)
- Next: [Terraform in CI/CD Pipelines](terraform-in-ci-cd-pipelines.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
