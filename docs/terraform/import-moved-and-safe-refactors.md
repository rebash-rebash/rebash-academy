---
title: Import, Moved, and Safe Refactors
description: "Import existing objects, use moved blocks for renames, and refactor addresses without destroying infrastructure."
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - import
  - moved
prerequisites:
  - Completed Functions, Templates, and Dynamic Blocks
comments: false
---

# Import, Moved, and Safe Refactors

## Overview

Refactoring Terraform must not mean **recreate-the-world**. Renaming a resource address without guidance destroys the old object and creates a new one — disastrous for databases, networks, and anything with durable identity. Modern Terraform supports **`import` blocks** to adopt existing objects into state and **`moved` blocks** to rename addresses so plans show a **move** (or no-op) instead of destroy/create.

This lab stays on the `local` provider: you create a file as `local_file.old`, rename it with `moved`, then practise an `import` of an unmanaged file. The workflow matches production cloud refactors — only the provider IDs differ.

This is **Tutorial 15** in **Module 4: Language Power Tools** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Import existing objects into state with `import` blocks and the CLI
- [ ] Rename addresses with `moved` blocks
- [ ] Read plans to confirm no destructive changes
- [ ] Describe `removed` blocks at a high level
- [ ] Refactor modules without unnecessary downtime

## Prerequisites

- Completed [Functions, Templates, and Dynamic Blocks](functions-templates-and-dynamic-blocks.md)
- Terraform CLI **1.9+** (1.15.x recommended; `import` blocks and `moved` are stable on modern 1.x)
- Ability to create directories and edit files
- No cloud account required

## Architecture

Safe refactors adjust the mapping between **configuration addresses** and **real objects** without changing the objects themselves. Import attaches an existing ID to an address; moved rewrites addresses inside state.

![Architecture diagram for Import, Moved, and Safe Refactors](../assets/images/terraform-refactor.svg)

| Tool | Question it answers |
|------|---------------------|
| `import` | “This object already exists — track it under address X” |
| `moved` | “Address A is now called B — rewrite state, keep the object” |
| `removed` | “Stop managing this object without destroying it” (Terraform 1.7+) |
| `terraform state mv` | Legacy/imperative cousin of `moved` — prefer blocks in Git |

## Theory

### Why refactors go wrong

Terraform identity is the **address** in state (`local_file.old`), not the filename alone. Change the address without telling Terraform and it assumes: destroy old address, create new address — often the same path or a ForceNew attribute — causing outages.

### `moved` block

```hcl
moved {
  from = local_file.old
  to   = local_file.new
}
```

After apply, state stores the object under `local_file.new`. Keep resource arguments equivalent (especially ForceNew fields) so the plan is move/no-op, not replace.

You can move:

- Resource to resource
- `count`/`for_each` index remaps (carefully)
- Resources into modules (`module.x.local_file.y`)

Commit `moved` blocks, apply once across all environments, then remove the blocks in a follow-up PR once every state has absorbed the rename (optional cleanup; leaving them is usually harmless).

### `import` block (Terraform 1.5+)

```hcl
import {
  to = local_file.adopted
  id = "/absolute/path/to/file"
}
```

Plan includes an import action, then reconciles configuration with the real object. After a successful apply, remove the `import` block — the object is now tracked like any other resource.

CLI equivalent:

```bash
terraform import local_file.adopted /absolute/path/to/file
```

Prefer **import blocks in Git** for reviewable, repeatable adoption. CLI import is fine for emergencies and exploration.

### `removed` block (Terraform 1.7+)

```hcl
removed {
  from = local_file.legacy

  lifecycle {
    destroy = false
  }
}
```

Drops an address from state **without** destroying the real object — useful when another system takes ownership. Confirm with plan before apply.

### Reading the plan

| Plan language | Meaning |
|---------------|---------|
| `will be moved` | Address rewrite — good for renames |
| `# ... will be imported` | Adoption into state |
| `must be replaced` | Destroy+create — investigate ForceNew diffs |
| `will be destroyed` + `will be created` | Likely missing `moved` |

Always save `terraform plan -out=tfplan` for production refactors and apply that exact plan.

### State CLI vs config

| Approach | Pros | Cons |
|----------|------|------|
| `moved` / `import` blocks | Reviewed in PRs, repeatable | Requires Terraform version support |
| `terraform state mv` | Immediate | Easy to forget documentation; not in Git history as intent |

### Practical mental model

1. Write the target configuration first
2. Add `moved` / `import` so state matches intent
3. Plan until there are **no unexpected destroys**
4. Apply once; verify; only then delete temporary import blocks

## Hands-on Lab

### Step 1 – Create the working directory

```bash
mkdir -p ~/rebash-tf-move && cd ~/rebash-tf-move
terraform version
```

**Expected:** Terraform 1.9+.

### Step 2 – Write the initial root as `local_file.old`

`versions.tf`:

```hcl
terraform {
  required_version = ">= 1.9.0"

  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.9"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.7"
    }
  }
}
```

`main.tf`:

```hcl
resource "random_id" "token" {
  byte_length = 2
}

resource "local_file" "old" {
  filename = "${path.module}/moved.txt"
  content  = "safe-refactor\ntoken=${random_id.token.hex}\n"
}

resource "terraform_data" "phase" {
  input = "phase-1-old-address"
}

output "file_path" {
  value = local_file.old.filename
}

output "token" {
  value = random_id.token.hex
}
```

### Step 3 – Apply phase 1

```bash
terraform fmt
terraform init -input=false
terraform validate
terraform apply -input=false -auto-approve
terraform state list
cat moved.txt
```

**Expected:** State contains `local_file.old`, `random_id.token`, `terraform_data.phase`. File `moved.txt` exists with a token line.

### Step 4 – Rename with a `moved` block

Replace `main.tf` with:

```hcl
resource "random_id" "token" {
  byte_length = 2
}

resource "local_file" "new" {
  filename = "${path.module}/moved.txt"
  content  = "safe-refactor\ntoken=${random_id.token.hex}\n"
}

moved {
  from = local_file.old
  to   = local_file.new
}

resource "terraform_data" "phase" {
  input = "phase-2-moved-address"
}

output "file_path" {
  value = local_file.new.filename
}

output "token" {
  value = random_id.token.hex
}
```

```bash
terraform plan -input=false
```

**Expected:** Plan reports a **move** from `local_file.old` to `local_file.new` (and an update to `terraform_data.phase`). It must **not** destroy `moved.txt` solely due to the rename. Token resource should remain (no replace unless you changed `byte_length`).

```bash
terraform apply -input=false -auto-approve
terraform state list
```

**Expected:** State lists `local_file.new` — not `local_file.old`. File content still present.

### Step 5 – Import an unmanaged file

Create a file Terraform does not yet manage:

```bash
mkdir -p adopted
echo "preexisting" > adopted/notes.txt
realpath adopted/notes.txt
```

Add to `main.tf` (keep existing resources):

```hcl
resource "local_file" "adopted" {
  filename = "${path.module}/adopted/notes.txt"
  content  = "preexisting\n"
}

import {
  to = local_file.adopted
  id = "${path.module}/adopted/notes.txt"
}
```

!!! note "Import id format"
    For `hashicorp/local` `local_file`, the import ID is the file path. Cloud resources use provider-specific IDs (ARN, resource ID). Always check the provider docs.

Because `path.module` in the `id` may need an absolute path depending on version/provider expectations, prefer the absolute path from `realpath` if plan complains:

```hcl
import {
  to = local_file.adopted
  id = "/Users/you/rebash-tf-move/adopted/notes.txt" # use your realpath
}
```

```bash
terraform plan -input=false
```

**Expected:** Import of `local_file.adopted`, then likely **no content change** if configuration matches the file (or a small in-place update if trailing newlines differ — align `content` to match).

```bash
terraform apply -input=false -auto-approve
```

Remove the `import` block after success so future plans do not re-import.

### Step 6 – Negative demo (do not apply)

Mentally rename `local_file.new` → `local_file.renamed` **without** a `moved` block and imagine the plan: destroy `new`, create `renamed` — often rewriting the same path. That is the failure mode `moved` prevents.

### Step 7 – Clean up

```bash
terraform destroy -input=false -auto-approve
rm -rf adopted
```

**Expected:** Managed files removed; lab directory tidy.

## Code Walkthrough

### `moved` block

| Argument | Purpose |
|----------|---------|
| `from` | Previous resource address in state |
| `to` | New address matching current configuration |

Terraform rewrites state; the provider is not asked to delete the object when the move succeeds and attributes align.

### Resource rename hygiene

Keep **ForceNew** arguments identical across the rename (`filename` for `local_file`). Changing `filename` while moving may still force a replace — that is an attribute change, not a pure rename.

### `import` block

| Argument | Purpose |
|----------|---------|
| `to` | Address that must exist in configuration |
| `id` | Provider-specific identifier of the real object |

After import, Terraform refreshes and plans updates so config and reality converge.

### `terraform_data.phase`

Lab-only marker so you can see a deliberate update alongside a move — teaches reading mixed plans (move + update) without panic.

### `random_id.token`

Proves that unrelated resources stay put during a file address move when you do not change their configuration.

## Validation

```bash
terraform fmt -check
terraform init -input=false
terraform validate
# After phase 1+2:
terraform state list | grep 'local_file.new'
test -f moved.txt
terraform plan -input=false -detailed-exitcode; echo "exit=$?"
```

| Check | Pass criteria |
|-------|----------------|
| Move plan | Shows move / no destroy of the file for rename-only |
| State | Address is `local_file.new` after apply |
| Import | Preexisting file tracked without unnecessary recreate |
| Token | `random_id.token` not replaced by the move |
| Cleanup | Destroy succeeds when intended |

## Best Practices

- Put `moved` and `import` in the same PR as the rename/adoption for reviewers
- Require `plan -out` artefacts for production refactors
- One logical rename wave per PR — avoid mixing refactors with feature work
- After all workspaces applied the move, optionally delete obsolete `moved` blocks
- Prefer import blocks over tribal “run this state mv” wiki pages
- Document provider-specific import IDs in module READMEs

## Security Considerations

- Imports can pull sensitive attributes into state — protect state and plan logs
- Do not import production objects into a scratch backend by mistake
- Limit who can apply refactors; a bad move is still a state rewrite
- Review plans for unexpected destroys that look like “cleanup”
- Treat `removed` with `destroy = false` carefully — orphaned cloud resources still cost money

## Common Mistakes

!!! warning "Renaming without moved"
    Destroy+create of critical resources. **Fix:** Always add `moved` when changing addresses for existing objects.

!!! warning "Changing ForceNew attributes in the same PR as a move"
    Plan shows replace despite moved. **Fix:** Split attribute changes from renames when possible.

!!! warning "Leaving import blocks forever"
    Confusing no-ops or re-import attempts. **Fix:** Remove after successful apply.

!!! warning "Importing into the wrong workspace/state"
    Managing prod objects from a dev state. **Fix:** Verify backend and workspace before apply.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Plan destroys after rename | Missing `moved` or wrong `from` address | Fix addresses; re-plan before apply |
| Import ID invalid | Wrong provider ID format | Check provider import docs; use absolute paths for local_file |
| Replace on move | ForceNew argument changed | Align attributes; move first, change later |
| State lock during refactor | Concurrent apply | Wait or coordinate; never force-unlock casually |
| `moved` from address not in state | Already moved or never existed | Remove obsolete moved or correct `from` |

## Interview Questions

1. What does `terraform import` do to state?
   *It binds an existing real-world object ID to a configuration address in state without necessarily creating the object.*

2. How do import blocks differ from the CLI import command?
   *Blocks are declarative, reviewable in Git, and applied via plan/apply; CLI is imperative and easy to forget to document.*

3. When do you use a `moved` block?
   *When renaming or relocating addresses so Terraform rewrites state instead of destroy/create.*

4. What happens if you rename a resource without `moved`?
   *Terraform plans to destroy the old address and create the new one, risking outages.*

5. How do you plan a zero-downtime refactor?
   *Keep ForceNew attributes stable, use moved/import, and apply only when the plan shows moves/updates — not replaces.*

6. What is `state mv`, and when prefer `moved` blocks?
   *`state mv` rewrites state imperatively; prefer `moved` blocks for audited, repeatable refactors in code review.*

7. How do you verify a refactor before apply?
   *Read `terraform plan` (saved with `-out`) for moves only; reject unexpected destroys/replaces.*

8. What risks remain after a successful import?
   *Config may still drift from reality; next plans update attributes — and state now holds whatever the refresh read.*

9. How do `for_each` address changes complicate moves?
   *You must move each instance key explicitly (or carefully) when keys change; missing keys still destroy.*

10. When should you destroy and recreate instead?
    *When identity cannot be preserved, or replacement is safer than fighting irreversible drift.*

11. How do you document a refactor for reviewers?
    *PR description listing moved/import blocks, expected plan shape, and rollback notes.*

12. What CI checks catch accidental destroys?
    *Policy-as-code on plan JSON, `terraform plan` diffs in PRs, and approval gates on apply jobs.*

## Summary

- Refactors change addresses; `moved` and `import` keep real objects alive
- Always demand a plan that shows moves/imports — not surprise destroys
- Align ForceNew attributes when renaming; split risky changes across PRs
- Prefer declarative blocks in Git over undocumented state CLI rituals
- Practise on local providers before touching production cloud state

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Functions, Templates, and Dynamic Blocks](functions-templates-and-dynamic-blocks.md)
- Next: [Format, Validate, and Terraform Test](format-validate-and-terraform-test.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)
2. [moved block](https://developer.hashicorp.com/terraform/language/block/moved)
3. [import block](https://developer.hashicorp.com/terraform/language/import)
4. [removed block](https://developer.hashicorp.com/terraform/language/block/removed)
5. [Import command](https://developer.hashicorp.com/terraform/cli/commands/import)
6. [hashicorp/local — local_file](https://registry.terraform.io/providers/hashicorp/local/latest/docs/resources/file)
7. [Terraform language](https://developer.hashicorp.com/terraform/language)
