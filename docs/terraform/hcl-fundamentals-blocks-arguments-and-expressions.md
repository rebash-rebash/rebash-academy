---
title: "HCL Fundamentals: Blocks, Arguments, and Expressions"
description: "Learn HashiCorp Configuration Language structure — blocks, arguments, expressions, variables, locals, outputs, and built-in functions."
difficulty: intermediate
estimated_time: "40–55 min"
technology: terraform
category: terraform
module: "Module 4 · HCL Fundamentals"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - hcl
prerequisites:
  - terraform/terraform-workflow-init-plan-apply
next:
  - terraform/providers-and-the-terraform-plugin-model
related:
  - terraform/variables-locals-and-outputs
  - terraform/functions-templates-and-dynamic-blocks
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - hcl
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# HCL Fundamentals: Blocks, Arguments, and Expressions

## Overview

Read and write clear HCL: blocks and labels, arguments, expressions, a first variable and output, locals, and common built-in functions.

**HashiCorp Configuration Language (HCL)** is Terraform’s configuration language. Almost everything is a **block** with **arguments**. Values come from literals, references, and **expressions** — including functions such as `join` and `format`.

This is a core tutorial in **Module 4 · HCL Fundamentals** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Terraform Workflow: Init, Plan, and Apply](terraform-workflow-init-plan-apply.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Identify block types and labels in a root module  
- [ ] Distinguish arguments from nested blocks  
- [ ] Use a variable, local, and output together  
- [ ] Apply a simple function in an expression

## Architecture

This topic’s control points and relationships are shown below.

![Terraform HCL blocks](../assets/excalidraw/terraform-hcl-blocks.svg)

## Theory

### What it is

HCL is block-oriented. A block has a **type**, optional **labels**, and a body of **arguments** (assignments) and nested blocks:

```hcl
resource "local_file" "readme" {
  filename = "${path.module}/README.txt"
  content  = var.message
}
```

Here `resource` is the block type; `"local_file"` and `"readme"` are labels; `filename` and `content` are arguments. **Expressions** produce values: string templates (`"${…}"`), references (`var.message`, `local.name`, `local_file.readme.content`), and function calls (`upper(var.message)`).

Core block types you will use constantly: `terraform`, `provider`, `resource`, `data`, `variable`, `output`, `locals`, and later `module`.

### Why it matters

Readable HCL is operational safety. Dense one-liners and unexplained magic locals slow reviews and hide blast radius. Consistent structure — inputs at the edge (`variable` / `output`), computed values in `locals`, resources in between — is how production modules stay maintainable across teams.

### How it works

1. Terraform parses `.tf` files into a configuration graph.
2. Variables supply input values (defaults, `tfvars`, environment — covered in Module 7).
3. Locals hold named expressions reused in the module.
4. Resource and data arguments evaluate expressions once dependencies are known.
5. Outputs export values for CLI display or parent modules.

**Functions** are built into the language (`length`, `join`, `coalesce`, `lookup`, `tonumber`, and many more). They run during planning/apply evaluation — they are not shell commands.

### Key concepts and comparisons

| Construct | Role |
|-----------|------|
| Block | Unit of configuration (`resource`, `variable`, …) |
| Argument | Named value inside a block |
| Expression | How a value is computed |
| `variable` | Module input |
| `locals` | Internal named values |
| `output` | Module export |

| Syntax | Example |
|--------|---------|
| Literal | `filename = "app.txt"` |
| Reference | `content = var.message` |
| Template | `filename = "${path.module}/app.txt"` |
| Function | `content = upper(var.message)` |

### Common pitfalls

- Treating HCL like a general-purpose programming language — prefer data and composition over clever loops early on.
- Confusing `path.module` (this module’s directory) with the process working directory.
- Putting secrets in plain locals committed to Git.
- Using string templates where a direct reference is clearer (`var.x` vs `"${var.x}"`).

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-terraform/module-04 && cd ~/rebash-terraform/module-04
```

**Focus:** hands-on practice for HCL Fundamentals: Blocks, Arguments, and Expressions

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: HCL Fundamentals: Blocks, Arguments, and Expressions"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-terraform/module-04 && cd ~/rebash-terraform/module-04

cat > versions.tf << 'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}
EOF

cat > variables.tf << 'EOF'
variable "project" {
  type        = string
  description = "Short project name for file content"
  default     = "rebash"
}
EOF

cat > main.tf << 'EOF'
locals {
  greeting = upper("hello ${var.project}")
}

resource "local_file" "note" {
  filename = "${path.module}/note.txt"
  content  = "${local.greeting}\n"
}

output "note_path" {
  value = local_file.note.filename
}
EOF

terraform fmt
terraform init
terraform apply -auto-approve
cat note.txt
terraform output
terraform destroy -auto-approve
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-terraform/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-terraform/module-04/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **HCL Fundamentals: Blocks, Arguments, and Expressions** always combines:

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

!!! warning "Treating HCL like a general-purpose programming language — prefer data and composition ove"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Confusing `path.module` (this module’s directory) with the process working directory."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode HCL Fundamentals: Blocks, Arguments, and Expressions changes as code and review them in pull requests
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

**HCL Fundamentals: Blocks, Arguments, and Expressions** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **HCL Fundamentals: Blocks, Arguments, and Expressions** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Providers and the Terraform Plugin Model](providers-and-the-terraform-plugin-model.md)

## References

- [Configuration language](https://developer.hashicorp.com/terraform/language)  
- [Functions](https://developer.hashicorp.com/terraform/language/functions)
