---
title: Variables, Locals, and Outputs
description: "Design typed variables, locals, and outputs with validation blocks and clear module contracts."
difficulty: beginner
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - variables
  - outputs
prerequisites:
  - Completed Providers and the Terraform Plugin Model
comments: false
---

# Variables, Locals, and Outputs

## Overview

Inputs and outputs are the API of every module. This tutorial covers typed variables, validation, value precedence, locals for derived values, and outputs — including `sensitive` handling.

This is **Tutorial 5** in **Module 2: Core Building Blocks** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Declare typed variables with validation
- [ ] Predict value precedence across tfvars, CLI, and environment
- [ ] Use locals to simplify expressions
- [ ] Export outputs and mark sensitive values
- [ ] Pass values with `TF_VAR_` and `*.auto.tfvars`

## Prerequisites

- Completed Providers and the Terraform Plugin Model

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Variables, Locals, and Outputs](../assets/images/terraform-variables-flow.svg)


## Theory

### Variable precedence (highest wins)

1. `-var` / `-var-file` on the CLI  
2. `*.auto.tfvars` / `*.auto.tfvars.json`  
3. `terraform.tfvars`  
4. Environment `TF_VAR_name`  
5. Default in the `variable` block  

### Validation

```hcl
variable "env" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.env)
    error_message = "env must be dev, staging, or prod."
  }
}
```

### Locals vs variables

Variables are **inputs** (set from outside). Locals are **computed** inside the module.

### Why this topic matters in production

Teams that skip **input validation, locals composition, and output contracts** eventually pay in outages: unreviewable plans, brittle
refactors, or secrets leaking into logs. Treat this tutorial as the minimum bar for merging
Terraform changes on a shared state file.

### Practical mental model

1. Write the smallest config that proves the idea
2. `fmt` / `validate` / `plan` until the diff matches your intent
3. Apply only after you can explain every create/update/replace line
4. Destroy lab resources so the next exercise starts clean

## Hands-on Lab

```bash
mkdir -p ~/rebash-tf-vars && cd ~/rebash-tf-vars
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

variable "env" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.env)
    error_message = "env must be dev, staging, or prod."
  }
}

variable "app_name" {
  type    = string
  default = "payments"
}

variable "db_password" {
  type      = string
  sensitive = true
}

locals {
  name_prefix = "${var.env}-${var.app_name}"
  note        = "Deploy target for ${local.name_prefix}"
}

resource "local_file" "config" {
  filename = "${path.module}/${local.name_prefix}.cfg"
  content  = <<-EOT
    ${local.note}
    # password length (not value): ${length(var.db_password)}
  EOT
}

output "config_path" {
  value = local_file.config.filename
}

output "db_password" {
  value     = var.db_password
  sensitive = true
}
```

```bash
cat > secret.auto.tfvars <<'EOF'
env         = "dev"
db_password = "not-a-real-secret"
EOF
terraform init -input=false
terraform apply -input=false -auto-approve
terraform output
terraform output -raw db_password
terraform destroy -input=false -auto-approve
rm -f secret.auto.tfvars
```

## Code Walkthrough

Sensitive outputs are redacted in normal CLI UI; `output -raw` still prints them — protect your terminal logs.


Re-read every argument in the lab through the lens of **input validation, locals composition, and output contracts**.
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
| Topic focus | You can explain how this lab demonstrates input validation, locals composition, and output contracts |
| Cleanup | Destroy (or documented teardown) left no stray lab files |

## Best Practices

- Keep examples small enough to run without cloud credentials unless the topic requires otherwise
- Document assumptions (CLI version, providers, working directory) at the top of the root module
- Prefer explicitness over cleverness when teaching **input validation, locals composition, and output contracts**
- Add CI checks (`fmt`, `validate`, plan) as soon as a root is shared
- Write outputs that help the next human debug, not just the next machine

## Security Considerations

- Assume state and plan output may contain secrets related to **input validation, locals composition, and output contracts**
- Use least-privilege credentials whenever a provider needs authentication
- Do not commit tfvars with real secrets; use examples with placeholders
- Review plans for unexpected destroys before apply
- Limit who can unlock state and who can approve production applies

## Common Mistakes

!!! warning "Putting secrets in defaults"
    They land in Git. **Fix:** No default for secrets; inject via CI/env.

!!! warning "Forgetting `sensitive = true` on outputs"
    Leaks in logs. **Fix:** Mark both variable and output.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| validate fails | Missing init or syntax error | Run `terraform init`, read the file:line in the error |
| Plan shows replace unexpectedly | ForceNew argument changed | Confirm intent; use moved/lifecycle if refactoring |
| Provider auth errors | Credentials not available | Export the documented env vars for the provider |
| Topic confusion around input validation, locals composition, and output contracts | Skipped theory | Re-read Theory, then re-run the lab from a clean directory |
| Leftover lab files | Destroy skipped | Re-run destroy or delete the lab directory after state cleanup |

## Interview Questions

1. When do you use variable validation blocks?
2. Why might an output be marked sensitive?
3. How do terraform.tfvars and -var-file interact?
4. What is the precedence order for variable assignment?
5. When should a value be a local instead of an output?
6. How do you pass complex objects between modules?
7. What happens if a validation condition fails?
8. Why document variables with descriptions?
9. How do nullable and default interact?
10. When is output value referring to a resource attribute safe?
11. How would you structure tfvars for dev vs prod?
12. What belongs in outputs.tf versus a data file?

## Summary

- Master **input validation, locals composition, and output contracts** before moving to the next tutorial in the track
- Every shared root needs formatting, validation, and a reviewed plan
- Prefer small, reversible labs that you can destroy confidently
- Carry security and state hygiene forward into every later module

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Providers and the Terraform Plugin Model](providers-and-the-terraform-plugin-model.md)
- Next: [Resources and Data Sources](resources-and-data-sources.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
