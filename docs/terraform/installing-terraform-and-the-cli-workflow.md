---
title: Installing Terraform and the CLI Workflow
description: "Terraform is a single static binary. Getting it onto your PATH correctly — and learning the"
difficulty: beginner
estimated_time: "30 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - cli
  - install
  - workflow
prerequisites:
  - Completed Introduction to Terraform and Infrastructure as Code
  - Terminal access with permission to install software (or use a package manager)
  - Network access to download Terraform and providers
comments: false
---

# Installing Terraform and the CLI Workflow

## Overview

Terraform is a single static binary. Getting it onto your PATH correctly — and learning the
exact order of CLI commands — prevents hours of “works on my machine” confusion later.

This tutorial covers install options on Linux/macOS/Windows (WSL), version managers, and the
daily workflow: `fmt` → `init` → `validate` → `plan` → `apply` → `destroy`. You will also learn
what belongs in Git (`.terraform.lock.hcl`) versus what never should (`.terraform/` provider
plugins and local state with secrets).

This is **Tutorial 2** in **Module 1: Foundations** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Install Terraform 1.9+ and verify with `terraform version`
- [ ] Explain when to use package installs vs tfenv/asdf vs direct binaries
- [ ] Run the standard CLI loop with non-interactive flags suitable for CI
- [ ] Distinguish `.terraform/`, `.terraform.lock.hcl`, and `terraform.tfstate`
- [ ] Use `terraform plan -out` and `terraform apply <planfile>` safely

## Prerequisites

- Completed Introduction to Terraform and Infrastructure as Code
- Terminal access with permission to install software (or use a package manager)
- Network access to download Terraform and providers

- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files

## Architecture

![Architecture diagram for Installing Terraform and the CLI Workflow](../assets/images/terraform-cli-workflow.svg)


## Theory

### Installation options

| Method | Best for | Notes |
|--------|----------|-------|
| HashiCorp apt/yum packages | Persistent Linux workstations/servers | Signed packages; easy upgrades |
| Official zip binary | Air-gapped or minimal images | Verify checksums/GPG |
| Homebrew (`brew install terraform`) | macOS / Linuxbrew | Convenient; pin version in team docs |
| **tfenv** / **asdf** | Teams juggling many versions | Per-directory `.terraform-version` |
| Container image | CI only | Mount credentials carefully |

Prefer a **version manager** when you contribute to multiple repos that pin different
`required_version` constraints.

### The CLI loop

1. **`terraform fmt`** — canonical formatting (diff-friendly)
2. **`terraform init`** — download providers/modules; configure backend
3. **`terraform validate`** — syntax/consistency checks (needs init)
4. **`terraform plan`** — show actions; optionally `-out=tfplan`
5. **`terraform apply`** — execute; prefer applying a saved plan in CI
6. **`terraform destroy`** — remove managed objects (labs / ephemeral envs)

### Important flags

- `-input=false` — never prompt (CI mandatory)
- `-chdir=DIR` — run as if DIR were the working directory
- `-auto-approve` — skip apply confirmation (use only when plan was reviewed)
- `TF_IN_AUTOMATION=1` — friendlier automation messaging
- `TF_LOG=INFO` / `TF_LOG_PATH` — debug provider/CLI issues

### What to commit

| Path | Commit? |
|------|---------|
| `*.tf`, `*.tfvars.example` | Yes |
| `.terraform.lock.hcl` | Yes (root modules) |
| `.terraform/` | **No** |
| `*.tfstate*` | **No** (use remote state + secrets handling) |
| `crash.log` | **No** |

## Hands-on Lab

### Step 1 – Verify installation

```bash
terraform version
which terraform
```

**Expected:** Terraform v1.9+ (1.15.x ideal). If missing, install from
[HashiCorp Install](https://developer.hashicorp.com/terraform/install) or:

```bash
# Example: tfenv
tfenv install 1.15.8
tfenv use 1.15.8
```

### Step 2 – Project skeleton

```bash
mkdir -p ~/rebash-tf-cli && cd ~/rebash-tf-cli
```

Create `versions.tf`:

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
```

Create `main.tf`:

```hcl
variable "stage" {
  type    = string
  default = "cli-lab"
}

resource "local_file" "marker" {
  filename        = "${path.module}/out/${var.stage}.txt"
  content         = "Terraform CLI workflow OK\n"
  file_permission = "0644"
}

output "path" {
  value = local_file.marker.filename
}
```

### Step 3 – Non-interactive workflow

```bash
terraform fmt
terraform init -input=false
terraform validate
terraform plan -input=false -out=tfplan
terraform apply -input=false tfplan
cat out/cli-lab.txt
terraform output
```

### Step 4 – Inspect artifacts

```bash
ls -la .terraform/providers | head
test -f .terraform.lock.hcl && echo "lockfile present"
terraform providers
```

### Step 5 – Clean up

```bash
terraform destroy -input=false -auto-approve
```

## Code Walkthrough

### `terraform init`

Reads `required_providers`, contacts the Registry, writes the dependency lock file, and
caches plugins under `.terraform/providers/...`.

### Saved plans

`plan -out=tfplan` produces a binary plan. Applying that file ensures CI applies **exactly**
what was reviewed — not a newly computed plan that might differ if state changed.

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

!!! warning "Installing random Terraform forks without checksums"
    Supply-chain risk. **Fix:** Use official HashiCorp distributions or verified package repos.

!!! warning "Committing `.terraform/`"
    Huge binaries; OS-specific. **Fix:** Gitignore `.terraform/`; commit only the lock file.

!!! warning "Using `-auto-approve` without a reviewed plan"
    Accidental destroys. **Fix:** In CI: plan artifact → human review → apply that artifact.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider download fails | Network/registry blocked | Check access to registry.terraform.io |
| validate fails before init | Providers not installed | Run `terraform init` |
| Unexpected replace | ForceNew argument change | Read plan carefully; use moved/for_each wisely |
| State locked | Another apply in progress | Wait or follow backend unlock procedures carefully |
| Permission denied writing files | Directory permissions | Ensure workspace is writable |

## Interview Questions

1. What problem does Installing Terraform and the CLI Workflow solve in a Terraform workflow?
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

- Terraform is a single static binary. Getting it onto your PATH correctly — and learning the
- Practice the lab until `fmt` / `validate` / `plan` are muscle memory
- Carry forward provider pins, sensitive handling, and plan-before-apply discipline

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Introduction to Terraform and Infrastructure as Code](introduction-to-terraform-and-iac.md)
- Next: [HCL Fundamentals — Blocks, Arguments, and Expressions](hcl-fundamentals-blocks-arguments-and-expressions.md)

## References

1. [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Terraform language](https://developer.hashicorp.com/terraform/language)
4. [Terraform Registry](https://registry.terraform.io/)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
