---
title: Terraform State Fundamentals
description: "Inspect and reason about local state safely: list, show, pull, drift, and what must never be committed."
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - state
prerequisites:
  - Completed Dependencies and the Resource Graph
comments: false
---

# Terraform State Fundamentals

## Overview

**State** is Terraform’s memory: a mapping from configuration addresses to real-world IDs and attributes. Cloud APIs do not know that you called something `local_file.tracked` — state binds that address to the file path and checksum Terraform manages. Understanding state is mandatory before remote backends, workspaces, or team workflows.

This tutorial covers what state stores, how to inspect it safely (`list`, `show`, `pull`), refresh and drift, backup files, and why state is always sensitive — even in a local-file lab.

This is **Tutorial 8** in **Module 2: Core Building Blocks** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Describe what state stores and why it exists
- [ ] Use `terraform state list`, `show`, and `pull` safely
- [ ] Explain refresh and how drift appears in a plan
- [ ] Avoid committing sensitive state to Git
- [ ] Recognise `terraform.tfstate` and `.backup` files
- [ ] Know when *not* to hand-edit state JSON

## Prerequisites

- Completed [Dependencies and the Resource Graph](dependencies-and-the-resource-graph.md)
- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files
- No cloud account required for this lab

## Architecture

After apply, the CLI writes state that maps each address to provider-tracked attributes. The next plan refreshes those attributes (where enabled) and diffs them against configuration.

![Architecture diagram for Terraform State Fundamentals](../assets/images/terraform-state.svg)

| Artefact | Role |
|----------|------|
| **Configuration** | Desired addresses and arguments |
| **State** | Recorded IDs and attributes |
| **Refresh** | Re-read real objects into memory for planning |
| **Plan** | Actions to reconcile config with state (+ reality) |

## Theory

### Why state exists

Without state, Terraform would have to guess which real object corresponds to `aws_instance.web`. State stores:

- Resource mode, type, name, and index/key
- Provider attribution
- Attributes returned by the provider (often including secrets)
- Dependency information used for destroy order
- Serial / lineage metadata for backends

State is not a substitute for Git. Git stores desired configuration; state stores the binding to reality.

### Local backend files

| File | Purpose |
|------|---------|
| `terraform.tfstate` | Current state for the default local backend |
| `terraform.tfstate.backup` | Previous successful write (best-effort recovery aid) |

Both are **sensitive**. Even `local_file` content can land in state. Never commit `*.tfstate*`.

### Essential CLI

| Command | Use |
|---------|-----|
| `terraform state list` | Addresses currently tracked |
| `terraform state show ADDRESS` | Human-readable attributes for one address |
| `terraform state pull` | Full JSON to stdout (pipe carefully) |
| `terraform refresh` / plan refresh | Update state from reality (prefer plan’s refresh) |
| `terraform state rm` | Forget an address without destroying the object (dangerous if misused) |
| `terraform state mv` | Rename addresses (prefer `moved` blocks in config for reviews) |

### Refresh and drift

Before proposing actions, Terraform typically **refreshes** — asks providers what objects look like now. If you edit a managed file by hand, the next plan shows an update to restore desired `content`. That difference is **drift**.

| Drift source | Example |
|--------------|---------|
| Console / manual edit | Someone changed a security group rule |
| Out-of-band automation | Another tool overwrote a file |
| Provider defaults | Remote API normalised a value |

Decide: adopt the drift into config, or re-apply to enforce config as source of truth.

### What must never be in Git

```gitignore
*.tfstate
*.tfstate.*
crash.log
crash.*.log
override.tf
```

Commit configuration and `.terraform.lock.hcl`. Treat state as a secret store that happens to include infrastructure metadata.

### Hand-editing state

Editing JSON by hand corrupts serials, digests, or attribute shapes and can cause orphaned cloud objects or unexpected destroys. Prefer:

- `moved` blocks for renames
- `import` / import blocks for adoption
- `terraform state rm` only with a clear recovery plan
- Remote backend versioning + restore procedures for disasters

### Trade-offs

| Approach | Benefit | Cost |
|----------|---------|------|
| Local state | Simple labs | No locking; easy to lose; not for teams |
| Commit state “for backup” | Feels safe | Secret leak; merge conflicts |
| Disable refresh | Faster plans | Miss real drift |
| Frequent `state rm` | Unblocks errors | Orphans and confusion |

## Hands-on Lab

You will apply a tiny root module, inspect state, induce drift, re-plan, then destroy.

### Step 1 – Create the lab root

**Objective:** Clean directory for local state experiments.

```bash
mkdir -p ~/rebash-tf-state && cd ~/rebash-tf-state
```

**Expected:** Empty directory as cwd.

### Step 2 – Write configuration and gitignore

**Objective:** Manage one file and ignore state artefacts.

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
variable "payload" {
  description = "Content written into the tracked file"
  type        = string
  default     = "state-lab"
}

resource "local_file" "tracked" {
  filename        = "${path.module}/out/tracked.txt"
  content         = "${var.payload}\n"
  file_permission = "0644"
}

resource "terraform_data" "note" {
  input = local_file.tracked.content_md5
}

output "tracked_path" {
  description = "Path of the managed file"
  value       = local_file.tracked.filename
}

output "tracked_md5" {
  description = "Checksum recorded after apply"
  value       = local_file.tracked.content_md5
}
```

Create `.gitignore`:

```gitignore
.terraform/
*.tfstate
*.tfstate.*
tfplan
*.tfplan
crash.log
out/
```

**Expected:** Three files ready; `hashicorp/local` `~> 2.9`.

### Step 3 – Apply and list state

**Objective:** See addresses appear in state after apply.

```bash
mkdir -p out
terraform init -input=false
terraform apply -input=false -auto-approve
terraform state list
```

**Expected:** State lists `local_file.tracked` and `terraform_data.note`. File `out/tracked.txt` contains `state-lab`.

### Step 4 – Show and pull

**Objective:** Inspect attributes and glimpse JSON (truncated).

```bash
terraform state show local_file.tracked
terraform state pull | head -c 500; echo
ls -la terraform.tfstate terraform.tfstate.backup 2>/dev/null || ls -la terraform.tfstate
```

**Expected:** `state show` prints filename, content, and permissions. `state pull` emits JSON including those attributes — proof that even lab content is in state. A `terraform.tfstate` file exists (backup appears after subsequent writes).

### Step 5 – Induce drift and re-plan

**Objective:** Experience drift detection.

```bash
echo "drifted-by-hand" > out/tracked.txt
terraform plan -input=false
```

**Expected:** Plan proposes an **update** to restore `content` to `state-lab\n` (or whatever `var.payload` is). That is refresh + diff against configuration.

Re-apply to heal:

```bash
terraform apply -input=false -auto-approve
cat out/tracked.txt
```

**Expected:** File content restored to the configured payload.

### Step 6 – Change configuration deliberately

**Objective:** Distinguish drift healing from intentional change.

```bash
terraform apply -input=false -auto-approve -var='payload=state-lab-v2'
terraform state show -no-color local_file.tracked | head -20
```

**Expected:** Content becomes `state-lab-v2`; state attributes update; `terraform_data.note` may replace/update because its `input` checksum changed.

### Step 7 – Clean up

**Objective:** Destroy managed objects and remove sensitive state files from disk when finished learning.

```bash
terraform destroy -input=false -auto-approve -var='payload=state-lab-v2'
rm -f tfplan
# Optional: remove state files after destroy if you are done
rm -f terraform.tfstate terraform.tfstate.backup
cd ~
rm -rf ~/rebash-tf-state
```

**Expected:** Managed file gone; lab directory removed. Never email or commit the state files you deleted.

## Code Walkthrough

### `local_file.tracked`

| Argument | Purpose |
|----------|---------|
| `filename` | Real path bound into state after create |
| `content` | Desired body; also stored in state for this provider |
| `file_permission` | Mode tracked for drift |

After apply, `state show` reveals why “local labs are harmless” is false for Git — content is in state JSON.

### `terraform_data.note`

Ties a second address to the file checksum so `state list` shows more than one object and you can see dependency-related updates when content changes.

### Why `.gitignore` is part of the lab

Practising ignore rules before remote backends prevents the most common beginner incident: committing `terraform.tfstate` with secrets to a public repository.

## Validation

```bash
terraform fmt -check
terraform init -input=false
terraform validate
terraform apply -input=false -auto-approve
terraform state list | grep local_file.tracked
terraform state show local_file.tracked >/dev/null
echo "x" > out/tracked.txt
terraform plan -input=false | tee /tmp/plan-drift.txt
grep -E 'updated|update|~' /tmp/plan-drift.txt || true
terraform destroy -input=false -auto-approve
```

| Check | Pass criteria |
|-------|----------------|
| State list | Includes `local_file.tracked` after apply |
| State show | Prints path and content attributes |
| Drift | Plan wants to revert hand edit |
| Git hygiene | `*.tfstate` ignored; not staged |
| Cleanup | Destroy succeeds |

## Best Practices

- Treat every state file as confidential — classify and store accordingly
- Prefer `moved` blocks in PRs over ad-hoc `state mv` for renames
- Use `state list` / `show` before risky operations (rm, import)
- Keep configuration and state responsibilities clear: Git vs backend
- Enable remote state with locking before a second engineer applies (next tutorial)
- Retain backend versioning / backups before major refactors
- Document recovery: what to do if local state is deleted in a lab versus production

## Security Considerations

- State frequently contains passwords, private keys, and connection strings from providers
- Restrict filesystem ACLs on laptop state during labs; use IAM on remote backends in production
- Do not paste `state pull` into tickets or chat
- CI logs should not dump full state JSON
- `TF_LOG=TRACE` can capture sensitive values — use briefly and delete logs
- Losing state without backup risks duplicate creates or manual cleanup of orphans

## Common Mistakes

!!! warning "Hand-editing state JSON"
    Corruption and surprise destroys. **Fix:** Use supported CLI workflows, `moved`, and import.

!!! warning "Emailing or committing tfstate"
    Secret sprawl and merge hell. **Fix:** Remote backends + IAM; gitignore local state.

!!! warning "Deleting state to ‘start clean’ in shared envs"
    Orphaned cloud resources. **Fix:** `destroy` first, or recover from backend versions.

!!! warning "Ignoring backup files"
    Still sensitive. **Fix:** Gitignore `*.tfstate.*` too; wipe labs deliberately.

## Troubleshooting

| Issue | Symptoms | Cause | Resolution |
|-------|----------|-------|------------|
| Empty state list | No addresses | Never applied / wrong directory | Apply from the root module |
| Plan wants recreate everything | State missing | Deleted tfstate | Restore backup/backend; else import or recreate knowingly |
| Drift every plan | Manual changes | Out-of-band edits | Stop manual edits or adopt into config |
| `state show` fails | Unknown address | Typo / wrong workspace | `state list` first |
| Backup out of date | Confusion after crash | Incomplete write | Restore from remote versioning; avoid hand merge |

## Interview Questions

1. What does state store, and why is it required?
   *Bindings from configuration addresses to real IDs/attributes so Terraform can plan updates and destroys.*

2. How do you inspect a resource in state without applying?
   *`terraform state show ADDRESS` or `state pull` after a prior apply.*

3. What is refresh, and when does it run?
   *Re-reading real objects into the working state, typically during plan/apply unless disabled.*

4. Why is state sensitive even for local_file labs?
   *Provider attributes — including file content — are stored in state JSON.*

5. What is terraform.tfstate.backup for?
   *A previous local state write to aid recovery after a failed write.*

6. How does drift appear in a plan?
   *Refresh finds reality differs from state/config; plan proposes actions to converge.*

7. When would you use terraform state rm?
   *To forget an address without destroying the object — only with a clear follow-up (import elsewhere or abandon).*

8. Why is editing state JSON by hand dangerous?
   *Easy to break lineage, attributes, or dependencies; prefer supported commands and config-based moves.*

9. How does state relate to resource addresses?
   *Each tracked object is keyed by its address (`type.name` or indexed forms).*

10. What changes when you move to a remote backend?
    *State lives in shared storage with locking/IAM; local files are no longer the source of truth.*

11. How do you recover from a lost local state file in a lab?
    *Restore backup, recreate from scratch, or import existing objects — production needs backend versioning.*

12. Why exclude *.tfstate* from Git?
    *Secrets, churn, and merge conflicts; Git is for configuration, not live bindings.*

## Summary

- State maps addresses to reality; without it Terraform cannot manage updates safely
- Inspect with `list` / `show` / `pull`; never commit state files
- Drift is normal to detect — decide whether to enforce config or adopt reality
- Hand-edit JSON only as a last resort; prefer `moved`, import, and remote backups

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Dependencies and the Resource Graph](dependencies-and-the-resource-graph.md)
- Next: [Remote State and Backends](remote-state-and-backends.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [State](https://developer.hashicorp.com/terraform/language/state)
2. [State Command](https://developer.hashicorp.com/terraform/cli/commands/state)
3. [Purpose of Terraform State](https://developer.hashicorp.com/terraform/language/state/purpose)
4. [Sensitive Data in State](https://developer.hashicorp.com/terraform/language/state/sensitive-data)
5. [Backend Types: local](https://developer.hashicorp.com/terraform/language/backend/local)
6. [hashicorp/local provider](https://registry.terraform.io/providers/hashicorp/local/latest)
7. [Moved block](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)
