---
title: Remote State and Backends
description: "Configure remote state backends with locking and encryption concepts, using local labs as a stepping stone."
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - backend
  - remote-state
prerequisites:
  - Completed Terraform State Fundamentals
comments: false
---

# Remote State and Backends

## Overview

Local state cannot support teams. Two engineers applying at once can corrupt a file; laptops get wiped; pull requests cannot share a single source of truth. **Remote backends** provide shared durable storage, **locking**, encryption, and access control. This tutorial covers backend concepts, S3 and HCP Terraform patterns, migration ideas, and cautious use of `terraform_remote_state` — with a hands-on lab that uses an explicit **local** backend path and documents remote configuration **without requiring AWS credentials**.

This is **Tutorial 9** in **Module 3: Collaboration and Scale** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain why remote state and locking matter for teams
- [ ] Compare local, S3, and HCP Terraform / `cloud` backends
- [ ] Read a production-shaped S3 backend configuration
- [ ] Describe `terraform init -migrate-state` at a high level
- [ ] Use `terraform_remote_state` cautiously
- [ ] Separate backend configuration from provider credentials

## Prerequisites

- Completed [Terraform State Fundamentals](terraform-state-fundamentals.md)
- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files
- No cloud account required for the lab (remote examples are read-only documentation)

## Architecture

The backend is the storage and locking engine for state. Providers still talk to cloud APIs; the backend talks to the state store.

![Architecture diagram for Remote State and Backends](../assets/images/terraform-remote-backend.svg)

| Concern | Local backend | Remote backend |
|---------|---------------|----------------|
| Storage | Disk file | Object store / HCP Terraform |
| Locking | None (file races) | DynamoDB / native locks / HCP |
| Sharing | Copy files (bad) | IAM / team permissions |
| Encryption | Disk encryption only | Server-side + TLS in transit |

## Theory

### Requirements for team state

| Requirement | Why |
|-------------|-----|
| Shared durable storage | Every apply sees the same bindings |
| Mutual exclusion (locking) | Prevent concurrent writers corrupting state |
| Encryption at rest / in transit | State contains secrets |
| Access control and audit | Who read/wrote state? |
| Versioning / backups | Recover from bad applies |

### Backend block basics

```hcl
terraform {
  required_version = ">= 1.9.0"

  backend "local" {
    path = "state/terraform.tfstate"
  }
}
```

Changing backend type or key requires `terraform init` (often with `-migrate-state` or `-reconfigure`). Backend configuration is **not** interpolated with arbitrary variables the same way resources are — partial configuration and `-backend-config` are common in CI.

### S3 backend (AWS example — do not apply without an account)

```hcl
terraform {
  backend "s3" {
    bucket         = "acme-tf-state"
    key            = "payments/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "acme-tf-locks"
    encrypt        = true
  }
}
```

| Argument | Purpose |
|----------|---------|
| `bucket` | State object bucket (private, versioned, public access blocked) |
| `key` | Object key per root module / stack |
| `region` | Bucket region |
| `dynamodb_table` | Legacy/common locking table (confirm current HashiCorp guidance for your Terraform version — locking mechanisms evolve) |
| `encrypt` | Enable server-side encryption for the object |

Prefer least-privilege IAM: separate read roles for plan-only CI and write roles for apply. Enable bucket versioning and block public access.

### HCP Terraform / `cloud` block

HashiCorp-hosted runs, state, and policy integration. The `cloud` block is mutually exclusive with a `backend` block. Useful when you want remote runs, team UI, and Sentinel/policy as code without operating the state bucket yourself.

### Partial backend config in CI

Omit sensitive or environment-specific values from Git:

```hcl
terraform {
  backend "s3" {
    bucket = "acme-tf-state"
    key    = "payments/terraform.tfstate"
    # region, role_arn, etc. supplied via -backend-config
  }
}
```

```bash
terraform init -input=false \
  -backend-config="region=eu-west-1" \
  -backend-config="dynamodb_table=acme-tf-locks"
```

### Migration concepts (`-migrate-state`)

Moving from local to remote:

1. Add the `backend` block
2. `terraform init` — Terraform offers to migrate existing local state
3. Confirm copy to remote; verify with `state list`
4. Securely delete local copies once remote is authoritative

Never migrate casually on production without a backup and a change window. Use `-reconfigure` when you intentionally change backend settings without migrating.

### `terraform_remote_state`

Data source that reads **outputs** from another state:

```hcl
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "acme-tf-state"
    key    = "network/terraform.tfstate"
    region = "eu-west-1"
  }
}
```

**Trade-offs:** convenient coupling versus brittle stacks. Prefer publishing a few stable outputs, or a real data plane (SSM Parameter Store, cloud service discovery), over deep remote-state webs.

### Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| S3 + locks | Full AWS control | You operate bucket, IAM, locks |
| HCP Terraform | Managed runs + state | Vendor process and cost model |
| Many remote_state links | Quick composition | Hard to untangle blast radius |
| State per tiny stack | Isolation | More backends to manage |

## Hands-on Lab

Demonstrate an **explicit local backend** (custom path), migrate between two local paths conceptually, and keep a documented S3 snippet for production — no AWS credentials required.

### Step 1 – Create directories

**Objective:** Separate configuration from the state file path.

```bash
mkdir -p ~/rebash-tf-backend/state ~/rebash-tf-backend/state-b
cd ~/rebash-tf-backend
```

**Expected:** `state/` and `state-b/` directories exist.

### Step 2 – Root module with local backend

**Objective:** See that “backend” is the state storage strategy.

Create `versions.tf`:

```hcl
terraform {
  required_version = ">= 1.9.0"

  backend "local" {
    path = "state/terraform.tfstate"
  }

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
resource "local_file" "marker" {
  filename        = "${path.module}/out/backend-lab.txt"
  content         = "remote-state-lab\n"
  file_permission = "0644"
}

output "marker_path" {
  description = "Managed file path"
  value       = local_file.marker.filename
}
```

Create `backend-s3.tf.example` (documentation only — not loaded if named `.example`):

```hcl
# Example only — copy into versions.tf when you have a real bucket.
# terraform {
#   backend "s3" {
#     bucket         = "acme-tf-state"
#     key            = "labs/backend/terraform.tfstate"
#     region         = "eu-west-1"
#     dynamodb_table = "acme-tf-locks"
#     encrypt        = true
#   }
# }
```

**Expected:** Lab uses local backend; S3 example remains comments for study.

### Step 3 – Init, apply, and verify state path

**Objective:** Confirm state lands under `state/`, not the default cwd file alone.

```bash
mkdir -p out
terraform init -input=false
terraform apply -input=false -auto-approve
ls -la state/
terraform state list
```

**Expected:** `state/terraform.tfstate` exists. State lists `local_file.marker`. Managed file under `out/`.

### Step 4 – Reconfigure to another local path (migration practice)

**Objective:** Practise backend change safely on local paths.

Edit `versions.tf` so the backend path is `state-b/terraform.tfstate` instead of `state/terraform.tfstate`.

```bash
terraform init -input=false -migrate-state -force-copy
ls -la state-b/
terraform state list
```

**Expected:** Terraform copies state to `state-b/`. `state list` still shows `local_file.marker`. (Exact init prompts may be skipped by `-force-copy` in automation-friendly flows — read the CLI help for your version if flags differ slightly.)

If your Terraform version asks interactively, answer yes to copy; for CI-style labs prefer documented non-interactive flags available on your version.

### Step 5 – Document remote_state pattern (no remote call)

**Objective:** Learn the shape without needing a second real backend.

Create `remote-state-pattern.tf.example`:

```hcl
# Pattern only — requires a real remote state to refresh.
# data "terraform_remote_state" "network" {
#   backend = "local"
#   config = {
#     path = "../network/terraform.tfstate"
#   }
# }
#
# output "upstream_example" {
#   value = data.terraform_remote_state.network.outputs.some_output
# }
```

**Expected:** You understand the API; you do not apply a broken data source against a missing remote.

### Step 6 – Clean up

**Objective:** Destroy resources and remove state copies from the lab folder.

```bash
terraform destroy -input=false -auto-approve
rm -rf state state-b out .terraform
rm -f terraform.tfstate terraform.tfstate.backup tfplan 2>/dev/null || true
cd ~
rm -rf ~/rebash-tf-backend
```

**Expected:** Lab directory gone; no leftover state JSON with lab content.

## Code Walkthrough

### `backend "local"`

| Argument | Purpose |
|----------|---------|
| `path` | Explicit state file location — makes “where is state?” obvious |

Remote backends swap this storage engine for S3/HCP/etc. without changing resource blocks.

### Why resources stay the same

`local_file.marker` does not care where state lives. Backend migration should not rewrite your entire module — only the `terraform` backend configuration.

### S3 example arguments (study)

Encrypt, lock, private bucket, unique `key` per stack. Provider credentials for AWS resources are separate from credentials used to access the state bucket (often the same role in small accounts — split them as you mature).

## Validation

```bash
# Recreate lab briefly:
terraform fmt -check
terraform init -input=false
terraform validate
terraform apply -input=false -auto-approve
test -f state/terraform.tfstate || test -f state-b/terraform.tfstate
terraform state list | grep local_file.marker
terraform destroy -input=false -auto-approve
```

| Check | Pass criteria |
|-------|----------------|
| Custom path | State file under configured `path` |
| List | Address present after apply |
| Example file | S3 snippet present for study without requiring credentials |
| Cleanup | Destroy + delete lab state directories |

## Best Practices

- One state key (or workspace) per blast radius — do not dump the company into one object
- Enable versioning and encryption on state buckets; block public access
- Always configure locking before a second human can apply
- Use partial backend config for regions/roles in CI
- Prefer few, stable cross-stack outputs over deep `terraform_remote_state` graphs
- Document who may `force-unlock` and under what incident process
- Separate plan-only and apply IAM roles where possible

## Security Considerations

- State is a secret store — IAM read access equals potential credential disclosure
- Never leave state buckets world-readable or with loose ACLs
- Encrypt at rest; enforce TLS
- Audit access to state objects and lock tables
- Stuck locks: verify no apply is running before `force-unlock`
- Do not commit backend configs that embed long-lived access keys — use roles/OIDC

## Common Mistakes

!!! warning "Remote state without locking"
    Concurrent apply corruption. **Fix:** Always enable the locking mechanism your backend supports.

!!! warning "Open S3 ACLs on state buckets"
    Data breach. **Fix:** Block public access; encrypt; least-privilege IAM; SCPs where available.

!!! warning "One giant state for all environments"
    Blast radius and lock contention. **Fix:** Split keys/roots by environment and domain.

!!! warning "Migrating production without backup"
    Unrecoverable loss. **Fix:** Versioning + tested restore + change window.

## Troubleshooting

| Issue | Symptoms | Cause | Resolution |
|-------|----------|-------|------------|
| Backend init error | Cannot connect | Wrong bucket/region/creds | Fix IAM and `-backend-config` |
| State lock held | Apply waits/fails | Another run or crash | Wait; then force-unlock per policy |
| Migrate skipped | Still local state | Init without migrate | Re-run `init -migrate-state` |
| remote_state empty | Missing outputs | Wrong key / no outputs | Fix key; publish outputs upstream |
| Access denied on plan | CI role too weak | Read IAM missing | Grant state read for plan roles |

## Interview Questions

1. What problems do remote backends solve?
   *Shared durable state, locking, access control, and usually encryption/audit for teams.*

2. Why is state locking mandatory for teams?
   *Two writers can corrupt state or apply conflicting plans without mutual exclusion.*

3. How does partial backend configuration work with CI?
   *Commit non-secret skeleton; pass region/role/table via `-backend-config` or env at init.*

4. What is terraform_remote_state used for?
   *Reading another state’s outputs; prefer stable contracts or a data plane for loose coupling.*

5. How do you migrate local state to remote safely?
   *Add backend, init with migrate, verify state list, back up, then remove local copies.*

6. What encryption expectations should you set for state storage?
   *Encryption at rest, TLS in transit, and tight IAM — assume secrets inside.*

7. Who should have read access to state?
   *Only roles that need plan/apply or break-glass audit — not the whole company.*

8. What happens if two applies race without locking?
   *Lost updates, corrupted state JSON, or contradictory infrastructure.*

9. How do workspaces relate to backends?
   *Workspaces isolate state within a backend; keys/prefixes still need a clear strategy.*

10. When is the local backend still acceptable?
    *Solo labs and throwaway experiments — not shared production.*

11. How do you break a stuck lock safely?
    *Confirm no active runner, then force-unlock with an incident record.*

12. What belongs in backend config versus provider config?
    *Backend: where state lives; provider: how to call cloud APIs for resources.*

## Summary

- Remote backends add sharing, locking, and security controls local files lack
- Practise backend path changes locally; keep S3/HCP snippets ready for real accounts
- Migrate deliberately with backups; treat state IAM as highly privileged
- Use `terraform_remote_state` sparingly with stable output contracts

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Terraform State Fundamentals](terraform-state-fundamentals.md)
- Next: [Workspaces and Environment Strategies](workspaces-and-environment-strategies.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Backends](https://developer.hashicorp.com/terraform/language/settings/backends/configuration)
2. [Backend Type: s3](https://developer.hashicorp.com/terraform/language/settings/backends/s3)
3. [Backend Type: local](https://developer.hashicorp.com/terraform/language/backend/local)
4. [HCP Terraform](https://developer.hashicorp.com/terraform/cloud-docs)
5. [terraform_remote_state](https://developer.hashicorp.com/terraform/language/state/remote-state-data)
6. [State locking](https://developer.hashicorp.com/terraform/language/state/locking)
7. [hashicorp/local provider](https://registry.terraform.io/providers/hashicorp/local/latest)
