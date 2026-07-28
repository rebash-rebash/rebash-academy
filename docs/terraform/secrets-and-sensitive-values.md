---
title: Secrets and Sensitive Values
description: "Terraform state and plans can contain secrets. Learn sensitive flags, redaction, local_sensitive_file, CI injection patterns, and why secret managers"
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - security
  - secrets
prerequisites:
  - Completed Format, Validate, and Terraform Test
comments: false
---

# Secrets and Sensitive Values

## Overview

Terraform state and plans can contain secrets. Learn sensitive flags, redaction, local_sensitive_file, CI injection patterns, and why secret managers beat plaintext tfvars.

This is **Tutorial 17** in **Module 5: Quality and Security** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Mark variables and outputs sensitive
- [ ] Prefer local_sensitive_file for secret material on disk
- [ ] Keep secrets out of Git
- [ ] Understand state exposure risks
- [ ] Inject secrets via env / CI secret stores

## Prerequisites

- Completed Format, Validate, and Terraform Test

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Secrets and Sensitive Values](../assets/images/terraform-secrets.svg)


## Theory

### Rules

1. Never commit real `*.tfvars` containing secrets  
2. Mark sensitive variables/outputs  
3. Encrypt remote state; restrict IAM  
4. Prefer cloud secret stores (ASM, Vault) and data sources  
5. Assume plan JSON may contain values — protect artifacts

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

variable "api_token" {
  type      = string
  sensitive = true
}

resource "local_sensitive_file" "token" {
  filename        = "${path.module}/.secrets/token"
  content         = var.api_token
  file_permission = "0600"
}

output "token_path" {
  value = local_sensitive_file.token.filename
}
```

```bash
export TF_VAR_api_token='lab-only-token'
mkdir -p .secrets
terraform init -input=false && terraform apply -input=false -auto-approve
terraform output
terraform destroy -input=false -auto-approve
unset TF_VAR_api_token
```

## Code Walkthrough

`local_sensitive_file` reduces accidental echo in logs compared to ordinary files; state may still store content — protect state.

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

!!! warning "Printing secrets in provisioners"
    Log leakage. **Fix:** Never echo secrets.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider download fails | Network/registry blocked | Check access to registry.terraform.io |
| validate fails before init | Providers not installed | Run `terraform init` |
| Unexpected replace | ForceNew argument change | Read plan carefully; use moved/for_each wisely |
| State locked | Another apply in progress | Wait or follow backend unlock procedures carefully |
| Permission denied writing files | Directory permissions | Ensure workspace is writable |

## Interview Questions

1. What problem does Secrets and Sensitive Values solve in a Terraform workflow?
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

- Terraform state and plans can contain secrets. Learn sensitive flags, redaction, local_sensitive_file, CI injection patterns, and why secret managers beat plaintext tfvars.
- Practice the lab until `fmt` / `validate` / `plan` are muscle memory
- Carry forward provider pins, sensitive handling, and plan-before-apply discipline

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Format, Validate, and Terraform Test](format-validate-and-terraform-test.md)
- Next: [Policy as Code Overview](policy-as-code-overview.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
