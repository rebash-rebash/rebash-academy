---
title: "Terraform Workflow: Init, Plan, and Apply"
description: "Deep dive into terraform init, plan, apply, destroy, validate, and fmt — the daily CLI loop for safe Infrastructure as Code."
difficulty: intermediate
estimated_time: "40–55 min"
technology: terraform
category: terraform
module: "Module 3 · Terraform Basics"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - cli-workflow
prerequisites:
  - terraform/installing-terraform-and-the-cli-workflow
next:
  - terraform/hcl-fundamentals-blocks-arguments-and-expressions
related:
  - terraform/terraform-state-fundamentals
  - terraform/format-validate-and-terraform-test
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - plan
  - apply
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Terraform Workflow: Init, Plan, and Apply

## Overview







Run the full local lifecycle — `fmt`, `validate`, `init`, `plan`, `apply`, `destroy` — and explain what each command does to configuration, state, and providers.

Every production change follows the same loop: format and validate, initialise the working directory, review a plan, apply deliberately, and destroy when a lab or environment should go away. Master these verbs before writing complex HCL.

This is a core tutorial in **Module 3 · Terraform Basics** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Installing Terraform and the CLI Workflow](installing-terraform-and-the-cli-workflow.md)
- Working `terraform` 1.x binary

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] State what `init`, `plan`, `apply`, and `destroy` change  
- [ ] Use `fmt` and `validate` before planning  
- [ ] Read a plan summary (add / change / destroy)  
- [ ] Apply and tear down a local `local_file` resource safely

## Architecture







This topic’s control points and relationships are shown below.

![Terraform workflow](../assets/excalidraw/terraform-workflow.svg)

## Theory







### What it is

The Terraform CLI workflow is a disciplined sequence of commands around one **root module** (a directory of `.tf` files):

| Command | Role |
|---------|------|
| `terraform fmt` | Rewrites HCL to canonical style |
| `terraform validate` | Checks configuration syntax and basic consistency |
| `terraform init` | Downloads providers/modules; configures backend |
| `terraform plan` | Shows the proposed delta vs current state |
| `terraform apply` | Executes a plan (or plans then applies interactively) |
| `terraform destroy` | Plans and applies deletion of managed resources |

State (often `terraform.tfstate` locally) is updated on successful apply/destroy so the next plan starts from reality Terraform last knew.

### Why it matters

Skipping plan review is how teams ship accidental destroys. Pipelines should run `fmt` (check mode), `validate`, and `plan` on every pull request, and apply only from an approved plan artefact or a controlled environment. Understanding each command prevents treating Terraform as a vague “deploy button”.

### How it works

1. **`fmt`** — normalises indentation and argument alignment; no API calls.
2. **`validate`** — parses HCL and checks references; needs init for provider schemas in most setups.
3. **`init`** — reads `required_providers`, fetches plugins, initialises the backend, installs modules.
4. **`plan`** — refreshes state (unless disabled), walks the graph, prints create/update/delete actions.
5. **`apply`** — runs the same planning logic (unless given a saved plan file), prompts for approval, then calls providers and writes state.
6. **`destroy`** — special apply that targets removal of all (or selected) managed objects.

Saved plans (`terraform plan -out=tfplan` then `terraform apply tfplan`) freeze the reviewed change set for CI — prefer that pattern in production pipelines.

### Key concepts and comparisons

| Command | Touches APIs? | Updates state? |
|---------|---------------|----------------|
| `fmt` / `validate` | No | No |
| `init` | Registry / module sources | No (configures backend) |
| `plan` | Often refresh reads | No (unless you use exotic flags) |
| `apply` / `destroy` | Yes | Yes on success |

### Common pitfalls

- Running `apply` without reading the plan summary.
- Re-running `init` as if it were deploy — init prepares; apply changes infrastructure.
- Editing state by hand instead of using supported commands.
- Forgetting that `destroy` is still an apply of deletions — review it like any other plan.
- Committing local `terraform.tfstate` with secrets — use remote state later; never publish state files.

## Hands-on Lab



### Objective

Run a complete Terraform workflow (init → plan → apply → prove → destroy) for **Terraform Workflow: Init, Plan, and Apply** without paid cloud resources.

### Prerequisites

- Terraform CLI ≥ 1.5
- Network access to download the null provider once

### Lab environment

Workspace: `~/rebash-terraform/module-03`

Local Terraform only (`null`/`local` providers). No AWS/GCP/Azure credentials required.

```bash
mkdir -p ~/rebash-terraform/module-03 && cd ~/rebash-terraform/module-03
```

### Real-world scenario

You are automating **Terraform Workflow: Init, Plan, and Apply** for a platform repo. Reviewers expect a clean plan artefact, applied evidence, and a destroy path before merge.

### Step-by-step tasks

#### Task 1 – Author and initialise configuration

Use local/null providers so the lab never bills a cloud account.

```bash
cat > versions.tf << 'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = { source = "hashicorp/null", version = "~> 3.2" }
  }
}
EOF
cat > main.tf << 'EOF'
resource "null_resource" "lab" {
  triggers = { topic = "rebash-lab" }
  provisioner "local-exec" {
    command = "echo applied > applied.txt"
  }
}
output "note" { value = null_resource.lab.triggers.topic }
EOF
terraform init
terraform validate
```

**Expected output:** `Terraform has been successfully initialized` and validate succeeds.

#### Task 2 – Plan, apply, and prove outputs

Treat the plan as the change ticket — review before apply.

```bash
terraform plan -out=tfplan
terraform show -no-color tfplan | tee plan.txt
terraform apply tfplan
terraform output
test -f applied.txt && cat applied.txt
```

**Expected output:** plan.txt shows create; `applied` written; output prints the note.

### Validation steps

- [ ] terraform validate passes
- [ ] Plan was saved and reviewed before apply
- [ ] Destroy completes with empty state (or resources removed)

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Provider not found | Missing init / network | Run `terraform init` again |
| State locked | Concurrent apply | Wait or coordinate; never force-unlock casually |
| Unexpected destroy in plan | Drift or wrong workspace | Read plan line-by-line before apply |

### Challenge exercise

Add an input variable with a validation block and fail the plan with an illegal value, then fix it.

### Learning outcomes

- Completed a reviewable plan/apply cycle
- Proved outputs/files exist
- Destroyed lab state

### Cleanup

```bash
terraform destroy -auto-approve
rm -rf .terraform tfplan 2>/dev/null || true
```

## Validation







- [ ] Lab commands run under `~/rebash-terraform/module-03/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Terraform Workflow: Init, Plan, and Apply** always combines:

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







!!! warning "Running `apply` without reading the plan summary."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Re-running `init` as if it were deploy — init prepares; apply changes infrastructure."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Terraform Workflow: Init, Plan, and Apply changes as code and review them in pull requests
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







**Terraform Workflow: Init, Plan, and Apply** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions






1. What is the purpose of each stage: init, plan, and apply?
2. Why save a plan with `-out` before applying?
3. What does a subsequent plan with no changes tell you?
4. What can go wrong if someone applies while another engineer plans against stale state?
5. How should interactive approval differ between laptops and CI?

!!! tip "Sample answer — question 2"
    A saved plan freezes the changeset reviewers approved. Applying that file avoids a newer unexpected plan. It is the usual pattern for CI apply jobs.

!!! tip "Sample answer — question 4"
    Without locking, two operators can race and corrupt state or apply conflicting changes. Remote backends with locking serialise applies and reduce this risk.

## Related Tutorials







- [Course overview](index.md)
- [HCL Fundamentals: Blocks, Arguments, and Expressions](hcl-fundamentals-blocks-arguments-and-expressions.md)

## References







- [Terraform CLI commands](https://developer.hashicorp.com/terraform/cli/commands)  
- [The core Terraform workflow](https://developer.hashicorp.com/terraform/cli/run)
