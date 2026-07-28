---
title: Workspaces and Environment Strategies
description: "Compare Terraform workspaces with separate state roots and choose environment strategies that match blast radius."
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

**Workspaces** isolate state for the same configuration. Selecting `dev` versus `staging` points Terraform at a different state key (or local directory) while reusing the same `.tf` files. They are useful for light isolation — review apps, homogeneous regional clones — but many teams prefer **separate directories, accounts, or repositories** for production. The skill is choosing deliberately based on blast radius, not habit.

This tutorial covers workspace CLI, `terraform.workspace` in expressions, state isolation, and when separate roots win.

This is **Tutorial 10** in **Module 3: Collaboration and Scale** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Create and select Terraform workspaces
- [ ] Use `terraform.workspace` in expressions safely
- [ ] Explain state isolation per workspace
- [ ] Compare workspaces versus separate root modules
- [ ] Avoid using workspaces as a substitute for proper blast-radius separation
- [ ] Describe how CI should select environments

## Prerequisites

- Completed [Remote State and Backends](remote-state-and-backends.md)
- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files
- No cloud account required for this lab

## Architecture

One configuration, multiple state slots. Switching workspace changes which state file (or remote key) Terraform reads and writes — not the `.tf` source tree.

![Architecture diagram for Workspaces and Environment Strategies](../assets/images/terraform-workspaces.svg)

| Approach | Isolation | Typical fit |
|----------|-----------|-------------|
| **Workspaces** | State only | Similar envs, same account pattern |
| **Directory per env** | State + optional config deltas | Clear promotion paths |
| **Account / subscription per env** | Hard blast radius | Production-grade separation |

## Theory

### Workspace CLI

```bash
terraform workspace list
terraform workspace new dev
terraform workspace select dev
terraform workspace show
```

The `default` workspace always exists. Local backends store non-default workspaces under `terraform.tfstate.d/<name>/`. Remote backends map workspaces to separate state keys/prefixes according to the backend type.

### `terraform.workspace`

Interpolations can branch on the current name:

```hcl
resource "local_file" "env" {
  filename = "${path.module}/env-${terraform.workspace}.txt"
  content  = "workspace = ${terraform.workspace}\n"
}
```

**Risks:** embedding workspace names in cloud resource names couples identity to an operational switch. A wrong `workspace select` in production is a classic incident. Prefer passing `var.environment` explicitly in high-risk roots so CI must set the value deliberately.

### When workspaces fit

- Same backend, multiple ephemeral review environments
- Homogeneous stacks with tiny deltas (name prefixes, sizes)
- Solo developers managing several parallel sandboxes

### When to prefer separate roots

| Signal | Prefer separate roots / accounts |
|--------|----------------------------------|
| Different AWS accounts or Azure subscriptions for prod | Yes |
| Different approvers / change windows | Yes |
| Different provider versions or modules | Often |
| Strong need to prevent “apply prod by mistake” | Yes |
| Completely different topologies | Yes |

Directory layout example:

```text
envs/
  dev/main.tf
  staging/main.tf
  prod/main.tf
modules/
  network/
  app/
```

Each env root calls shared modules with different tfvars and backends.

### Promotion model

Workspaces do not “promote” code by themselves. Promotion is a **pipeline** concern: merge to main, run plan against staging state, then apply prod with the same commit SHA and different variables/backend. Whether that uses workspaces or separate roots, the reviewed artefact should be the same configuration revision.

### HCP Terraform note

HCP Terraform “workspaces” are a product concept (runs, variables, state) related to but not identical to CLI workspaces. Read product docs when you adopt remote runs — naming overlap confuses interviews and runbooks.

### Trade-offs

| Strategy | Pros | Cons |
|----------|------|------|
| CLI workspaces | DRY config, quick | Easy to select wrong; weak hard isolation |
| Env directories | Explicit; easy PR review per env | Some duplication of wiring |
| Account-per-env | Strong blast radius | More accounts to operate |

## Hands-on Lab

You will create `dev` and `staging` workspaces, apply in each, and observe separate files and state.

### Step 1 – Create the lab

**Objective:** Fresh root for workspace experiments.

```bash
mkdir -p ~/rebash-tf-ws && cd ~/rebash-tf-ws
```

**Expected:** Empty lab directory.

### Step 2 – Write configuration

**Objective:** Name artefacts from `terraform.workspace` and pin providers.

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
variable "owner" {
  description = "Tag-like owner string embedded in the file body"
  type        = string
  default     = "rebash-academy"
}

locals {
  # Prefer var.environment in production; workspace demo is intentional here.
  env_name = terraform.workspace
}

resource "local_file" "env" {
  filename        = "${path.module}/out/env-${local.env_name}.txt"
  content         = <<-EOT
    workspace = ${local.env_name}
    owner     = ${var.owner}
  EOT
  file_permission = "0644"
}

resource "terraform_data" "ws" {
  input = local.env_name
}

output "workspace" {
  description = "Active Terraform workspace name"
  value       = terraform.workspace
}

output "env_file" {
  description = "Path of the per-workspace managed file"
  value       = local_file.env.filename
}
```

**Expected:** Files saved.

### Step 3 – Init and apply in `dev`

**Objective:** Create the first isolated state slot.

```bash
mkdir -p out
terraform init -input=false
terraform workspace new dev || terraform workspace select dev
terraform workspace show
terraform apply -input=false -auto-approve
cat out/env-dev.txt
terraform state list
```

**Expected:** Current workspace `dev`. File `out/env-dev.txt` exists. State lists `local_file.env`.

### Step 4 – Apply in `staging` without destroying `dev`

**Objective:** Prove isolation — selecting staging does not destroy dev objects.

```bash
terraform workspace new staging || terraform workspace select staging
terraform apply -input=false -auto-approve
ls -la out/env-*.txt
terraform state list
```

**Expected:** Both `out/env-dev.txt` and `out/env-staging.txt` exist. Staging state lists its own `local_file.env` (separate state).

### Step 5 – Switch back and inspect

**Objective:** See that `default` / `dev` state is unchanged.

```bash
terraform workspace select dev
terraform state list
terraform output
ls terraform.tfstate.d 2>/dev/null || echo "local workspace dirs may vary; state still isolated"
```

**Expected:** Dev state still tracks the dev file. Workspace directories under `terraform.tfstate.d` appear for non-default local workspaces.

### Step 6 – Clean up each workspace

**Objective:** Destroy per workspace, then remove the lab.

```bash
terraform workspace select staging
terraform destroy -input=false -auto-approve
terraform workspace select dev
terraform destroy -input=false -auto-approve
terraform workspace select default
# optional: terraform workspace delete staging; terraform workspace delete dev
cd ~
rm -rf ~/rebash-tf-ws
```

**Expected:** Managed files removed; lab directory deleted. Delete empty workspaces only after destroy.

## Code Walkthrough

### `terraform.workspace`

Evaluates to the selected workspace name (`dev`, `staging`, `default`, …). Using it in `filename` makes isolation visible on disk for the lab.

### `local.env_name`

A single place to swap later for `var.environment` without rewriting every resource — good production habit even when demos use the workspace interpolator.

### `terraform_data.ws`

Tracks the workspace name as managed input so `state list` shows more than the file and you see replace behaviour if you rename strategies later.

### Why destroy per workspace

Each workspace has its own state. Destroying in `staging` does not remove `dev` resources. Forgetting to destroy all workspaces leaves orphan managed files — same class of mistake as forgetting an environment in the cloud.

## Validation

```bash
terraform fmt -check
terraform init -input=false
terraform validate
terraform workspace new dev || terraform workspace select dev
terraform apply -input=false -auto-approve
test -f out/env-dev.txt
terraform workspace new staging || terraform workspace select staging
terraform apply -input=false -auto-approve
test -f out/env-dev.txt && test -f out/env-staging.txt
terraform workspace select staging && terraform destroy -input=false -auto-approve
terraform workspace select dev && terraform destroy -input=false -auto-approve
```

| Check | Pass criteria |
|-------|----------------|
| Two files | `env-dev.txt` and `env-staging.txt` both present after both applies |
| Isolation | Destroy staging leaves `env-dev.txt` until you destroy dev |
| Output | `workspace` matches `terraform workspace show` |
| Cleanup | Both workspaces destroyed |

## Best Practices

- Name workspaces consistently (`dev`, `staging`, `prod`) — no ad-hoc typos
- Prefer explicit `var.environment` for cloud resource naming in production
- Document whether your team uses workspaces or env directories — do not mix silently
- Gate prod applies with separate credentials and approvals regardless of strategy
- In CI, set workspace from the job definition — never rely on a sticky agent workspace
- Destroy or expire ephemeral review workspaces automatically
- Align backend key design with workspace strategy so state objects are obvious in the console

## Security Considerations

- Wrong workspace + shared credentials = prod incident; separate accounts beat clever naming
- Limit who can create workspaces in remote backends
- Do not put secrets in workspace names or in files derived only from workspace
- Audit which workspace CI applied; include workspace name in change tickets
- Deleting a workspace with remote state can delete state — destroy resources first, follow vendor docs

## Common Mistakes

!!! warning "One workspace for prod and dev in the same account without guardrails"
    Easy to apply the wrong env. **Fix:** Separate accounts or strong CI protections and explicit env variables.

!!! warning "Using terraform.workspace as the only prod safety rail"
    Humans select wrong. **Fix:** Separate backends/accounts; require `-var=environment=prod` checks.

!!! warning "Forgetting to destroy non-default workspaces"
    Orphan resources and cost. **Fix:** Cleanup jobs; list workspaces in runbooks.

!!! warning "Assuming HCP ‘workspace’ equals CLI workspace"
    Confused automation. **Fix:** Learn both models; map them explicitly in docs.

## Troubleshooting

| Issue | Symptoms | Cause | Resolution |
|-------|----------|-------|------------|
| Wrong file updated | Unexpected path | Wrong workspace selected | `workspace show`; select correct one |
| State empty after select | No addresses | Never applied in that workspace | Apply in the intended workspace |
| Cannot delete workspace | CLI error | State not empty / current selected | Destroy; select another; then delete |
| CI applies default | Resources in wrong slot | Workspace not set in job | Export/select workspace in pipeline |
| Name collisions in cloud | Already exists | Same names across workspaces in one account | Include env in names *and* separate accounts |

## Interview Questions

1. What does a Terraform workspace switch under the hood?
   *It selects a different state slot for the same configuration.*

2. When are workspaces a poor fit for prod isolation?
   *When you need hard account/subscription separation or different approvers and blast radius.*

3. How do you name workspaces consistently?
   *Short fixed vocabulary (dev/staging/prod) documented for the team and enforced in CI.*

4. What is the alternative directory-per-env layout?
   *Separate root modules per environment calling shared modules with different backends/tfvars.*

5. How do backends interact with workspaces?
   *Remote backends map each workspace to a distinct state key/prefix.*

6. How would you promote a change from dev to prod?
   *Same commit through pipeline stages with different state/vars — not ‘copy workspace’.*

7. What risks come from using terraform.workspace in resource names?
   *Wrong selection renames/replaces critical objects; prefer explicit variables for naming.*

8. When is a single workspace multi-account design wrong?
   *When provider aliases and complexity hide which account you are changing — split roots instead.*

9. How do CI pipelines select workspaces?
   *`terraform workspace select` or equivalent remote workspace binding in the job definition.*

10. What happens to state if you delete a workspace?
    *You remove that state slot — ensure resources are destroyed or intentionally orphaned first.*

11. How do modules stay environment-agnostic?
    *Accept variables for names/sizes; do not hard-code workspace checks inside shared modules.*

12. Compare workspaces with Terragrunt-style roots at a high level.
    *Both isolate state; directory/tooling roots make env differences more explicit at the cost of more wiring.*

## Summary

- Workspaces isolate state for one configuration — powerful and easy to misuse
- Prefer separate accounts/roots when blast radius matters more than DRY
- Use explicit environment variables for high-risk naming
- Always destroy each workspace you create in labs and ephemeral environments

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Remote State and Backends](remote-state-and-backends.md)
- Next: [Modules — Creating Reusable Infrastructure](modules-creating-reusable-infrastructure.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces)
2. [terraform workspace CLI](https://developer.hashicorp.com/terraform/cli/commands/workspace)
3. [State](https://developer.hashicorp.com/terraform/language/state)
4. [Backends](https://developer.hashicorp.com/terraform/language/settings/backends/configuration)
5. [HCP Terraform workspaces](https://developer.hashicorp.com/terraform/cloud-docs/workspaces)
6. [Modules](https://developer.hashicorp.com/terraform/language/modules)
7. [hashicorp/local provider](https://registry.terraform.io/providers/hashicorp/local/latest)
