---
title: "Remote State and Backends"
description: "Configure remote Terraform state with locking and encryption — S3, Azure, GCS patterns, and team collaboration for production IaC."
difficulty: intermediate
estimated_time: "45–60 min"
technology: terraform
category: terraform
module: "Module 8 · State Management"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - remote-state
  - backends
prerequisites:
  - terraform/terraform-state-fundamentals
next:
  - terraform/modules-creating-reusable-infrastructure
related:
  - terraform/workspaces-and-environment-strategies
  - terraform/terraform-cloud-and-hcp-terraform
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - backend
  - remote-state
  - locking
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Remote State and Backends

## Overview







Explain why remote state and locking matter, compare S3 / Azure / GCS and HCP Terraform patterns, and practise an explicit local backend path as a safe stepping stone.

Local state cannot support teams. Concurrent applies corrupt files; laptops get wiped; pull requests lack a single source of truth. **Remote backends** provide shared durable storage, **locking**, encryption, and access control. Providers still talk to cloud APIs; the backend stores state.

This is a core tutorial in **Module 8 · State Management** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Terraform State Fundamentals](terraform-state-fundamentals.md)
- Terraform CLI 1.9+ (no cloud account required for the lab)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Explain shared storage, locking, and encryption for team state  
- [ ] Compare local, S3, Azure, GCS, and HCP Terraform / `cloud` backends  
- [ ] Describe `terraform init -migrate-state` and partial `-backend-config`  
- [ ] Use `terraform_remote_state` cautiously

## Architecture







This topic’s control points and relationships are shown below.

![Remote backends](../assets/excalidraw/terraform-remote-backend.svg)

## Theory







### What it is

A **backend** is the storage and locking engine for state. The default is `local` (a file on disk). Remote backends move that file into object storage or a managed service so every engineer and CI runner sees the same bindings. Team requirements: shared durable storage, mutual exclusion (locking), encryption at rest and in transit, access control and audit, and versioning / backups for recovery.

### Why it matters

Two engineers applying without locks can corrupt state or apply conflicting plans. An open state bucket is a credential disclosure waiting to happen — state often holds passwords, keys, and connection strings. Platform teams standardise one backend pattern (bucket + lock table, or HCP Terraform) so product roots inherit security defaults instead of inventing them per project.

### How it works

1. Declare a `backend` block inside `terraform { }` (or a `cloud` block for HCP Terraform — mutually exclusive with `backend`).
2. `terraform init` configures the backend; changing type or key often needs `-migrate-state` or `-reconfigure`.
3. Plans and applies read/write remote state under a lock for the duration of the operation.
4. CI commonly uses **partial backend config**: commit a skeleton; pass region, role, or table via `-backend-config`.
5. `data "terraform_remote_state"` reads **outputs** from another state’s key — convenient but coupling; prefer few stable outputs or a real data plane (Parameter Store, service discovery).

Cloud patterns (study shape — wire credentials only with a real account): **S3** (versioned bucket + lock table / native locks, `encrypt = true`), **AzureRM** (storage container + blob lease), **GCS** (bucket + prefix), **HCP Terraform** (managed state and locks).

### Key concepts and comparisons

| Concern | Local | Remote |
|---------|-------|--------|
| Storage | Disk file | Object store / HCP |
| Locking | None (file races) | Native / DynamoDB / platform |
| Sharing | Copy files (bad) | IAM / team permissions |
| Fit | Solo labs | Teams and CI |

Migrate deliberately: add backend → `init -migrate-state` → verify `state list` → delete local copies only after remote is authoritative.

### Common pitfalls

- Remote state without locking — concurrent apply corruption.
- World-readable state buckets or loose ACLs.
- One giant state for all environments — blast radius and lock contention.
- Deep `terraform_remote_state` webs instead of stable contracts.
- Embedding long-lived access keys in backend config — use roles / OIDC.

## Hands-on Lab



### Objective

Run a complete Terraform workflow (init → plan → apply → prove → destroy) for **Remote State and Backends** without paid cloud resources.

### Prerequisites

- Terraform CLI ≥ 1.5
- Network access to download the null provider once

### Lab environment

Workspace: `~/rebash-terraform/module-08/remote-backends/{state,state-b,out}`

Local Terraform only (`null`/`local` providers). No AWS/GCP/Azure credentials required.

```bash
mkdir -p ~/rebash-terraform/module-08/remote-backends/{state,state-b,out} && cd ~/rebash-terraform/module-08/remote-backends/{state,state-b,out}
```

### Real-world scenario

You are automating **Remote State and Backends** for a platform repo. Reviewers expect a clean plan artefact, applied evidence, and a destroy path before merge.

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

#### Task 3 – Inspect state safely

State is the source of truth — list and show without hand-editing.

```bash
terraform state list | tee state-list.txt
terraform state show null_resource.lab | tee state-show.txt
```

**Expected output:** state-list.txt contains `null_resource.lab`.

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







- [ ] Lab commands run under `~/rebash-terraform/module-08/remote-backends/{state,state-b,out}/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Remote State and Backends** always combines:

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







!!! warning "Remote state without locking — concurrent apply corruption."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "World-readable state buckets or loose ACLs."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Remote State and Backends changes as code and review them in pull requests
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







**Remote State and Backends** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions






1. What problems do remote backends solve?
2. What is state locking and why does it matter?
3. How does partial apply failure interact with remote state?
4. What security controls belong on a remote state bucket?
5. When might you split state across multiple backends/workspaces?

!!! tip "Sample answer — question 2"
    Locking prevents two applies from corrupting state or racing changes. Without locks, concurrent runs can overwrite each other’s state snapshots.

!!! tip "Sample answer — question 4"
    Encrypt the bucket, block public access, limit IAM to CI roles, enable versioning, and audit access. State is as sensitive as production config.

## Related Tutorials







- [Course overview](index.md)
- [Modules — Creating Reusable Infrastructure](modules-creating-reusable-infrastructure.md)

## References







- [Backends](https://developer.hashicorp.com/terraform/language/settings/backends/configuration)  
- [Backend: s3](https://developer.hashicorp.com/terraform/language/settings/backends/s3)  
- [State locking](https://developer.hashicorp.com/terraform/language/state/locking)
