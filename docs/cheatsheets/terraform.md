---
title: "Terraform Cheat Sheet"
description: "Quick-reference commands and patterns for the REBASH Academy Terraform track."
difficulty: beginner
estimated_time: "10 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: cheatsheets
tags:
  - cheatsheets
  - terraform
comments: false
---

# Terraform Cheat Sheet

Scannable commands and patterns for the [Terraform track](../terraform/index.md). Prefer the full tutorials when you need *why*, not only *how*.

## Quick reference

| Area | Commands / notes |
|------|------------------|
| Loop | `fmt` → `init` → `validate` → `plan -out` → `apply` |
| Init | `terraform init -input=false`; `-upgrade` when intentional |
| Plan | `terraform plan -input=false -out=tfplan` |
| Apply | `terraform apply -input=false tfplan` |
| State | `terraform state list`; `show ADDR`; never commit `*.tfstate*` |
| Output | `terraform output`; sensitive outputs redacted in CLI |
| Fmt/CI | `terraform fmt -check`; `TF_IN_AUTOMATION=1` |
| Modules | `source` + version pin; `path.module` |
| Meta | `for_each` over `count`; `lifecycle` sparingly |
| Destroy | `terraform destroy` only for labs / approved teardown |

## Common mistakes

- Copy-pasting without reading expected output
- Skipping cleanup (leftover containers, state, or temp files)
- Mixing production credentials into lab shells

## Related

- Track: [Terraform](../terraform/index.md)
- Start: [Terraform introduction](../terraform/introduction-to-terraform-and-iac.md)
- Interview bank: [Terraform interview prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)
