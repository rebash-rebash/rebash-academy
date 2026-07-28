---
title: Resources and Data Sources
description: "Resources are objects Terraform manages. Data sources read existing objects without owning their lifecycle. Mastering both is the difference between ‘"
difficulty: beginner
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - resources
  - data-sources
prerequisites:
  - Completed Variables, Locals, and Outputs
comments: false
---

# Resources and Data Sources

## Overview

Resources are objects Terraform manages. Data sources read existing objects without owning their lifecycle. Mastering both is the difference between ‘I can create things’ and ‘I can integrate with what already exists’.

This is **Tutorial 6** in **Module 2: Core Building Blocks** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain manage vs read-only objects
- [ ] Use resource addresses in expressions
- [ ] Read files/metadata with data sources
- [ ] Predict create/update/replace/destroy behaviors
- [ ] Avoid using data sources for objects you should manage

## Prerequisites

- Completed Variables, Locals, and Outputs

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Resources and Data Sources](../assets/images/terraform-resources-data.svg)


## Theory

### Resources

Terraform creates/updates/deletes them and records IDs in state.

### Data sources

```hcl
data "local_file" "existing" {
  filename = "${path.module}/seed.txt"
}
```

Data sources run during plan/refresh and export attributes. They do **not** create the object.

### Replace vs update

Some argument changes force **replacement** (destroy+create). Read provider docs for ForceNew behaviors. Prefer `for_each` friendly designs and `moved` blocks when renaming.

## Hands-on Lab

```bash
mkdir -p ~/rebash-tf-res && cd ~/rebash-tf-res
echo "seed-data" > seed.txt
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

data "local_file" "seed" {
  filename = "${path.module}/seed.txt"
}

resource "local_file" "derived" {
  filename = "${path.module}/derived.txt"
  content  = "derived-from: ${trimspace(data.local_file.seed.content)}\n"
}

output "derived_md5" {
  value = local_file.derived.content_md5
}
```

```bash
terraform init -input=false && terraform apply -input=false -auto-approve
cat derived.txt
terraform destroy -input=false -auto-approve
```

## Code Walkthrough

The data source reads `seed.txt` that you created outside Terraform; the resource writes a managed derivative.

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

!!! warning "Managing the same object as both data and resource"
    Fighting ownership. **Fix:** Pick one model.

!!! warning "Assuming data sources are free"
    They call APIs every plan. **Fix:** Cache thoughtfully; watch rate limits on cloud APIs.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider download fails | Network/registry blocked | Check access to registry.terraform.io |
| validate fails before init | Providers not installed | Run `terraform init` |
| Unexpected replace | ForceNew argument change | Read plan carefully; use moved/for_each wisely |
| State locked | Another apply in progress | Wait or follow backend unlock procedures carefully |
| Permission denied writing files | Directory permissions | Ensure workspace is writable |

## Interview Questions

1. What problem does Resources and Data Sources solve in a Terraform workflow?
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

- Resources are objects Terraform manages. Data sources read existing objects without owning their lifecycle. Mastering both is the difference between ‘I can create things’ and ‘I can integrate with what already exists’.
- Practice the lab until `fmt` / `validate` / `plan` are muscle memory
- Carry forward provider pins, sensitive handling, and plan-before-apply discipline

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Variables, Locals, and Outputs](variables-locals-and-outputs.md)
- Next: [Dependencies and the Resource Graph](dependencies-and-the-resource-graph.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
