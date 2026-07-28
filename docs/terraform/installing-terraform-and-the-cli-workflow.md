---
title: Installing Terraform and the CLI Workflow
description: "Install Terraform 1.9+, choose a version manager, and practise the non-interactive CLI loop with saved plan files."
difficulty: beginner
estimated_time: "40 min"
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

Terraform is a single static binary. Getting it onto your `PATH` correctly — and learning the exact order of CLI commands — prevents hours of “works on my machine” confusion later.

This tutorial covers install options on Linux, macOS, and Windows (WSL), version managers, and the daily workflow: `fmt` → `init` → `validate` → `plan` → `apply` → `destroy`. You will learn what belongs in Git (`.terraform.lock.hcl`) versus what never should (`.terraform/` and local state).

This is **Tutorial 2** in **Module 1: Foundations** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Install Terraform 1.9+ and verify with `terraform version`
- [ ] Explain when to use package installs vs tfenv/asdf vs direct binaries
- [ ] Run the standard CLI loop with non-interactive flags suitable for CI
- [ ] Distinguish `.terraform/`, `.terraform.lock.hcl`, and `terraform.tfstate`
- [ ] Use `terraform plan -out` and `terraform apply <planfile>` safely
- [ ] Add a sensible `.gitignore` for Terraform root modules

## Prerequisites

- Completed [Introduction to Terraform and Infrastructure as Code](introduction-to-terraform-and-iac.md)
- Terminal access with permission to install software (or use a package manager)
- Network access to download Terraform and providers from HashiCorp and the [Terraform Registry](https://registry.terraform.io/)
- Ability to create directories and edit text files
- Terraform CLI **1.9+** is the goal of this tutorial (1.15.x recommended once installed)

## Architecture

The CLI is the control plane for every root module: it formats configuration, initialises providers, compares desired state to recorded state, and applies an approved plan.

![Architecture diagram for Installing Terraform and the CLI Workflow](../assets/images/terraform-cli-workflow.svg)

| Artefact | Role |
|----------|------|
| **Terraform binary** | Parses HCL, builds the graph, drives providers |
| **Working directory** | Root module `.tf` files and optional `.tfvars` |
| **`.terraform/`** | Local provider/module cache — machine-specific |
| **`.terraform.lock.hcl`** | Selected provider versions and checksums |
| **Plan file** | Binary snapshot of intended create/update/destroy actions |
| **State** | Mapping from configuration addresses to real object IDs |

## Theory

### Installation options

| Method | Best for | Notes |
|--------|----------|-------|
| HashiCorp apt/yum packages | Persistent Linux workstations and servers | Signed packages; straightforward upgrades |
| Official zip binary | Air-gapped hosts or minimal images | Verify SHA256 checksums and GPG signatures |
| Homebrew (`brew install terraform`) | macOS / Linuxbrew | Convenient; still document the pinned team version |
| **tfenv** / **asdf** | Teams juggling many `required_version` floors | Per-directory `.terraform-version` |
| Container image | CI runners | Mount credentials carefully; pin the image digest |

Prefer a **version manager** when repos pin different `required_version` floors. **tfenv** or **asdf** switch binaries via `.terraform-version` — commit it next to `versions.tf`. Prefer **WSL2** on Windows; on Linux use HashiCorp packages or the official zip with checksums; on macOS document the Homebrew-pinned version.

### The CLI loop

1. **`terraform fmt`** — canonical formatting (diff-friendly reviews)
2. **`terraform init`** — download providers/modules; configure the backend
3. **`terraform validate`** — syntax and consistency checks (requires a prior successful `init`)
4. **`terraform plan`** — show actions; optionally `-out=tfplan`
5. **`terraform apply`** — execute; prefer applying a saved plan in CI
6. **`terraform destroy`** — remove managed objects (labs and ephemeral environments)

Skipping `fmt` creates noisy diffs; skipping `validate` wastes plans against broken HCL; skipping saved plans in CI invites unreviewed applies.

### Important flags and environment variables

| Flag / variable | Effect |
|-----------------|--------|
| `-input=false` | Never prompt (CI mandatory) |
| `-chdir=DIR` | Run as if `DIR` were the working directory |
| `-auto-approve` | Skip apply confirmation (only after a reviewed plan) |
| `-detailed-exitcode` on plan | Exit `2` when changes are present — useful in PR checks |
| `TF_IN_AUTOMATION=1` | Clearer messaging for automation logs |
| `TF_INPUT=0` | Equivalent to `-input=false` for many commands |
| `TF_LOG` / `TF_LOG_PATH` | Debug traces (never commit logs that may contain secrets) |

### What to commit

| Path | Commit? |
|------|---------|
| `*.tf`, `*.tfvars.example` | Yes |
| `.terraform.lock.hcl` | Yes (root modules) |
| `.terraform-version` | Yes (if you use a version manager) |
| `.terraform/` | **No** |
| `*.tfstate*` | **No** (use remote state and treat state as sensitive) |
| `tfplan`, `*.tfplan` | **No** (often contain sensitive planned values) |
| `crash.log` | **No** |

### Why plan files matter

A saved plan is a **snapshot of intent**. Between plan and apply, another process can change remote state. Applying the plan file still applies that snapshot; if state moved incompatibly, apply fails safely rather than silently computing a different plan. That is the point of `plan -out` in pull-request workflows and release pipelines.

Interactive `apply` without a plan file re-plans immediately — fine for personal labs after you read the screen, wrong for shared production accounts.

### Local backend behaviour in this lab

This lab uses the default local backend (`terraform.tfstate`). Later tutorials cover remote backends with locking — never commit local state.

## Hands-on Lab

You will install or verify Terraform, create a tiny root module with `hashicorp/local`, and practise the non-interactive loop with a saved plan file.

### Step 1 – Verify or install the CLI

```bash
terraform version
which terraform
```

**Expected:** Terraform v1.9 or newer (1.15.x is ideal). If the command is missing, install from [HashiCorp Install](https://developer.hashicorp.com/terraform/install) or use a version manager:

```bash
# Example: tfenv
tfenv install 1.15.8
tfenv use 1.15.8
terraform version
```

**Expected:** The selected version prints and matches `.terraform-version` if you create one next.

### Step 2 – Create the project skeleton

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
  description = "Short label embedded in the managed marker filename"
  type        = string
  default     = "cli-lab"
}

variable "marker_message" {
  description = "Body written into the local marker file"
  type        = string
  default     = "Terraform CLI workflow OK"
}

resource "local_file" "marker" {
  filename        = "${path.module}/out/${var.stage}.txt"
  content         = "${var.marker_message}\n"
  file_permission = "0644"
}

output "marker_path" {
  description = "Absolute path of the managed marker file"
  value       = local_file.marker.filename
}

output "marker_md5" {
  description = "MD5 checksum of the marker content"
  value       = local_file.marker.content_md5
}
```

Create `.gitignore`:

```gitignore
.terraform/
*.tfstate
*.tfstate.*
crash.log
crash.*.log
tfplan
*.tfplan
override.tf
override.tf.json
*_override.tf
*_override.tf.json
```

**Expected:** Root module files plus `.gitignore` in `~/rebash-tf-cli`.

### Step 3 – Format, initialise, and validate

```bash
terraform fmt
terraform init -input=false
terraform validate
```

**Expected:** `fmt` rewrites nothing material (or only whitespace). `init` downloads `hashicorp/local` into `.terraform/providers/...` and writes `.terraform.lock.hcl`. `validate` prints `Success! The configuration is valid.`

### Step 4 – Plan to a file and inspect it

```bash
terraform plan -input=false -out=tfplan
terraform show -no-color tfplan | head -40
```

**Expected:** Plan proposes **create** for `local_file.marker`. `terraform show` prints a human-readable summary of that binary plan. The file `tfplan` exists in the working directory.

### Step 5 – Apply the saved plan

```bash
terraform apply -input=false tfplan
cat out/cli-lab.txt
terraform output
```

**Expected:** Apply reports one added resource. `out/cli-lab.txt` contains `Terraform CLI workflow OK`. Outputs show `marker_path` and `marker_md5`.

### Step 6 – Inspect artefacts and provider selection

```bash
ls -la .terraform/providers | head
test -f .terraform.lock.hcl && echo "lockfile present"
terraform providers
```

**Expected:** Provider plugins under `.terraform/providers`. Lockfile present. `terraform providers` lists `hashicorp/local` required by the root module.

### Step 7 – Clean up

```bash
terraform destroy -input=false -auto-approve
rm -f tfplan
```

**Expected:** Managed file removed; state no longer lists `local_file.marker`. Plan file deleted so it cannot be reapplied by mistake.

## Code Walkthrough

### `terraform` block in `versions.tf`

| Argument | Purpose |
|----------|---------|
| `required_version` | Reject unsupported CLI versions before providers download |
| `required_providers.local.source` | Registry address `hashicorp/local` |
| `required_providers.local.version` | Pessimistic constraint `~> 2.9` — allow 2.9.x, not 3.x |

As of this writing, `hashicorp/local` latest is **2.9.0**. Re-check the Registry before production pins.

### `variable` blocks

`description`, `type`, and `default` form the input API — always set the first two; omit defaults in production when the value must be supplied explicitly.

### `local_file.marker` arguments

| Argument | Purpose |
|----------|---------|
| `filename` | Destination path; parent directories are created by the provider |
| `content` | Desired UTF-8 body; changing it updates the managed file |
| `file_permission` | POSIX mode string (`0644` is a sensible lab default) |

After apply, state stores the path and content checksum so the next plan detects drift if you edit the file by hand.

### Outputs and saved plans

Outputs publish `filename` and `content_md5` after apply. 

### Why `plan -out` then `apply tfplan`

`plan -out=tfplan` serialises reviewed actions; `apply tfplan` executes that artefact without re-planning. In CI, store the plan, require a review gate, then apply the same bytes with write credentials.

## Validation

Confirm the CLI workflow end-to-end in a fresh copy of the lab directory (or after re-creating the files):

```bash
terraform version | head -1
terraform fmt -check
terraform init -input=false
terraform validate
terraform plan -input=false -out=tfplan
terraform show -no-color tfplan | head -40
terraform apply -input=false tfplan
test -f out/cli-lab.txt
terraform output -json
terraform destroy -input=false -auto-approve
```

| Check | Pass criteria |
|-------|----------------|
| Version | Terraform 1.9+ reported |
| `fmt -check` | Exit 0 |
| Lockfile | `.terraform.lock.hcl` created after init |
| Plan file | `tfplan` exists; `show` prints a create/update for `local_file.marker` |
| Apply | Marker file exists and matches `marker_message` |
| Outputs | `marker_path` and `marker_md5` present |
| Cleanup | Destroy removes the managed file |

## Best Practices

- Pin CLI versions per repository with tfenv/asdf and document the floor in `required_version`
- Always run `fmt` before commit; enable `fmt -check` in CI so style never blocks late
- Prefer `plan -out` plus apply of that artefact over `apply -auto-approve` on a live re-plan
- Commit `.terraform.lock.hcl` for root modules so every engineer and CI runner get the same providers
- Set `TF_IN_AUTOMATION=1` and `-input=false` in every pipeline job
- Keep a root-module `.gitignore` from day one — do not invent it after the first accidental state commit
- Use `-chdir` in wrappers when scripts target nested roots

## Security Considerations

- Download only from HashiCorp releases or signed packages; verify checksums for air-gapped installs
- Never commit `crash.log`, production plan files, or local state
- Restrict who can apply against shared state — CLI write access equals change authority
- Treat `TF_LOG_PATH` as sensitive; prefer short-lived CI credentials (OIDC) over long-lived laptop keys

## Common Mistakes

!!! warning "Installing random Terraform forks without checksums"
    Supply-chain risk. **Fix:** Use official HashiCorp distributions or verified package repositories and verify SHA256 sums.

!!! warning "Committing `.terraform/`"
    Huge binaries; OS-specific. **Fix:** Gitignore `.terraform/`; commit only the lock file.

!!! warning "Using `-auto-approve` without a reviewed plan"
    Accidental destroys. **Fix:** In CI: plan artefact → human or policy review → apply that artefact.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `terraform: command not found` | Binary not on `PATH` | Reload shell; fix PATH; re-check `which terraform` |
| Wrong version in CI | Image/binary drift | Pin version; mirror `.terraform-version` in the job |
| `init` hangs or TLS fails | Proxy / firewall | Allow `registry.terraform.io`; set HTTPS proxy |
| Apply differs from review | Re-planned instead of `-out` | Apply the saved plan file only |
| Permission denied under `out/` | Directory not writable | Fix permissions or let the provider create parents |
| Inconsistent lock file | Constraint changed without upgrade | `terraform init -upgrade`, review lockfile diff |

## Interview Questions

1. Why commit `.terraform.lock.hcl` but gitignore `.terraform/`?
   *The lockfile pins versions and checksums for reproducibility; `.terraform/` holds machine-specific provider binaries that do not belong in Git.*

2. What does `terraform plan -out=tfplan` protect you from in CI?
   *It freezes the reviewed set of actions so apply does not silently re-plan against a moved state or changed config.*

3. When is `-auto-approve` acceptable, and when is it dangerous?
   *Acceptable after a reviewed saved plan in automation; dangerous on an interactive re-plan against production.*

4. How do `required_version` and a version manager work together?
   *`required_version` rejects unsupported binaries; tfenv/asdf selects the binary that satisfies that floor per repository.*

5. What is the difference between `validate` and `plan`?
   *`validate` checks configuration consistency after init; `plan` compares desired config to state and proposes real API actions.*

6. Why should production applies use a saved plan artefact?
   *So the exact change set reviewed in the pull request is what mutates infrastructure.*

7. How would you install Terraform on an air-gapped bastion?
   *Copy the official zip and checksums from a trusted transfer path, verify SHA256/GPG, install the binary, and mirror providers if Registry access is blocked.*

8. What environment variables make Terraform safer in automation?
   *`TF_IN_AUTOMATION=1` and `TF_INPUT=0` (or `-input=false`) avoid prompts and clarify CI logs.*

9. Why is `fmt -check` useful in pull requests?
   *It fails the build on formatting drift so reviews focus on behaviour, not whitespace.*

10. What belongs in Git for a root module on day one?
    *`.tf` files, `.tfvars.example`, `.terraform.lock.hcl`, `.gitignore`, and optionally `.terraform-version` — not state or `.terraform/`.*

11. How does `terraform providers` help debug version skew?
    *It shows which modules require which providers and versions, revealing constraint conflicts quickly.*

12. Describe a secure download and verification flow for the Terraform binary.
    *Fetch only from HashiCorp, verify published checksums (and signatures where used), then install to a controlled PATH.*

## Summary

- Install an official Terraform binary and prefer a version manager for multi-repo work
- Memorise the loop: fmt → init → validate → plan (`-out`) → apply → destroy
- Commit the lockfile; never commit provider caches, plan files, or local state
- Use non-interactive flags and saved plans for CI-grade discipline from the first lab

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Introduction to Terraform and Infrastructure as Code](introduction-to-terraform-and-iac.md)
- Next: [HCL Fundamentals — Blocks, Arguments, and Expressions](hcl-fundamentals-blocks-arguments-and-expressions.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Install Terraform](https://developer.hashicorp.com/terraform/install)
2. [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)
3. [Running Terraform in automation](https://developer.hashicorp.com/terraform/cli/run)
4. [Dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock)
5. [Version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
6. [hashicorp/local provider](https://registry.terraform.io/providers/hashicorp/local/latest)
7. [Terraform Registry](https://registry.terraform.io/)
