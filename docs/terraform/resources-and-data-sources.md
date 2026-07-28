---
title: Resources and Data Sources
description: "Contrast managed resources with data sources, and practise read-only lookups beside managed local files."
difficulty: beginner
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - resources
  - data-sources
prerequisites:
  - Completed Variables, Locals, and Outputs
comments: false
---

# Resources and Data Sources

## Overview

**Resources** are objects Terraform manages — create, update, destroy, and record in state. **Data sources** read existing objects without owning their lifecycle. Mastering both is the difference between “I can create things” and “I can integrate safely with what already exists.”

This tutorial contrasts managed versus read-only objects, resource addresses, create/update/replace behaviour, and when *not* to use a data source. The lab uses `hashicorp/local` only: you seed a file outside Terraform, read it with a data source, and write a managed derivative.

This is **Tutorial 6** in **Module 2: Core Building Blocks** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain manage versus read-only objects in Terraform’s model
- [ ] Use resource and data source addresses in expressions
- [ ] Read files or metadata with data sources during plan/refresh
- [ ] Predict create, update, replace, and destroy behaviours at a high level
- [ ] Avoid using data sources for objects your root should manage
- [ ] Prefer `terraform_data` over legacy `null_resource` when you need a no-cloud trigger object

## Prerequisites

- Completed [Variables, Locals, and Outputs](variables-locals-and-outputs.md)
- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files
- No cloud account required for this lab

## Architecture

Configuration declares resources (write path) and data sources (read path). Both appear in the graph; only resources own lifecycle and full state entries for managed objects.

![Architecture diagram for Resources and Data Sources](../assets/images/terraform-resources-data.svg)

| Kind | Lifecycle | Typical use |
|------|-----------|-------------|
| **Resource** | Terraform creates/updates/deletes | New infrastructure you own |
| **Data source** | Read during plan/refresh | Look up AMI IDs, existing VPCs, files, remote state |
| **State** | Records IDs and attributes | Next plan’s memory of reality |

## Theory

### What a resource is

A resource block tells Terraform: “this object should exist, with these arguments.”

```hcl
resource "local_file" "derived" {
  filename = "${path.module}/derived.txt"
  content  = "hello\n"
}
```

- **Type** — `local_file` (provider resource type)
- **Name** — `derived` (local label)
- **Address** — `local_file.derived`
- **Arguments** — values you set (`filename`, `content`)
- **Attributes** — values the provider exports after apply (`content_md5`, `id`)

Terraform records the result in state so the next plan can compare desired configuration to reality.

### What a data source is

A data source reads something that already exists:

```hcl
data "local_file" "seed" {
  filename = "${path.module}/seed.txt"
}
```

Address: `data.local_file.seed`. Attributes such as `content` are available to expressions. Data sources do **not** create the object; if the file is missing, plan fails.

### When to use which

| Situation | Prefer |
|-----------|--------|
| You own create/update/destroy | **Resource** |
| Object owned by another team or stack | **Data source** (or remote state / SSM) |
| Bootstrap seed committed to the repo | Data source (or `file()` function for simple reads) |
| Same object managed in two places | **Never** — pick one owner |

### Create, update, replace, destroy

During plan, Terraform classifies each action:

| Action | Meaning |
|--------|---------|
| **Create** | Address not in state; will be created |
| **Update in place** | Arguments change; provider can mutate without recreate |
| **Replace** | Arguments that force new identity (ForceNew / recreate) — destroy then create (or create-before-destroy) |
| **Destroy** | Address removed from config, or `terraform destroy` |

Read provider documentation for which arguments force replacement. Changing a ForceNew argument on a database can mean downtime unless you use `create_before_destroy` and careful cutover.

### Data sources and plan-time behaviour

Data sources run during refresh/plan. Consequences:

- Plans can change **without** editing `.tf` if the remote object changed (new AMI, rotated secret metadata)
- Cloud APIs are called often — watch rate limits and permissions
- Avoid data sources that need credentials you do not have in CI “plan-only” roles unless you design for it

### `terraform_data` vs managing nothing

When you need a managed placeholder for triggers or replacement hooks, prefer built-in [`terraform_data`](https://developer.hashicorp.com/terraform/language/resources/terraform-data) (Terraform 1.4+) over `hashicorp/null`’s `null_resource`. No extra provider required.

### Trade-offs

| Choice | Benefit | Risk |
|--------|---------|------|
| Data source for shared VPC | Reuse without owning network | Hidden coupling; VPC deletion breaks you |
| Duplicate config instead of data | Isolation | Drift between copies |
| Import existing into a resource | Single owner | Migration effort; careful state ops |
| Overusing data sources | Flexible reads | Noisy plans, API load, unclear ownership |

## Hands-on Lab

You will create a seed file outside Terraform, read it with `data.local_file`, write a managed `local_file`, and observe that destroy removes only the managed file.

### Step 1 – Create the directory and seed file

**Objective:** Produce an unmanaged object for the data source to read.

**Explanation:** The seed is deliberately outside Terraform’s management so you feel the ownership boundary.

```bash
mkdir -p ~/rebash-tf-res && cd ~/rebash-tf-res
echo "seed-data" > seed.txt
```

**Expected:** `seed.txt` contains `seed-data`.

### Step 2 – Write the root module

**Objective:** Declare data source, resource, and output.

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
data "local_file" "seed" {
  filename = "${path.module}/seed.txt"
}

resource "local_file" "derived" {
  filename        = "${path.module}/derived.txt"
  content         = "derived-from: ${trimspace(data.local_file.seed.content)}\n"
  file_permission = "0644"
}

resource "terraform_data" "seed_fingerprint" {
  input = data.local_file.seed.content_md5
}

output "derived_md5" {
  description = "Checksum of the managed derivative file"
  value       = local_file.derived.content_md5
}

output "seed_md5" {
  description = "Checksum read from the unmanaged seed via data source"
  value       = data.local_file.seed.content_md5
}

output "trigger_input" {
  description = "terraform_data input mirrors the seed checksum"
  value       = terraform_data.seed_fingerprint.output
}
```

**Expected:** Files saved; `hashicorp/local` constraint `~> 2.9` (latest **2.9.0** as of this writing).

### Step 3 – Init, plan, and apply

**Objective:** Confirm the plan creates only the managed objects.

```bash
terraform init -input=false
terraform plan -input=false -out=tfplan
terraform show -no-color tfplan | head -50
terraform apply -input=false tfplan
```

**Expected:** Plan creates `local_file.derived` and `terraform_data.seed_fingerprint`. No create for `seed.txt`. After apply, `derived.txt` contains `derived-from: seed-data`.

### Step 4 – Prove ownership boundaries

**Objective:** See that editing the seed changes the plan, and destroy leaves the seed alone.

```bash
cat derived.txt
terraform output
echo "seed-data-v2" > seed.txt
terraform plan -input=false
```

**Expected:** Plan shows updates/replacements driven by the new seed content (derived content and `terraform_data` input change). `seed.txt` itself is never listed as a managed create/destroy of a resource you own as `local_file.seed`.

Apply if you want, then:

```bash
terraform apply -input=false -auto-approve
terraform destroy -input=false -auto-approve
ls -la seed.txt derived.txt 2>&1 || true
```

**Expected:** After destroy, `derived.txt` is gone; `seed.txt` remains because Terraform never managed it.

### Step 5 – Clean up leftover lab files

**Objective:** Leave the home directory tidy.

```bash
rm -f seed.txt tfplan
cd ~
rm -rf ~/rebash-tf-res
```

**Expected:** Lab directory removed.

## Code Walkthrough

### `data.local_file.seed`

| Argument | Purpose |
|----------|---------|
| `filename` | Path of the existing file to read |

Exported attributes used here: `content`, `content_md5`. The data source fails plan if the path is missing.

### `local_file.derived`

| Argument | Purpose |
|----------|---------|
| `filename` | Managed path Terraform will create/update/delete |
| `content` | Built from the data source — creates an **implicit dependency** |
| `file_permission` | POSIX mode for the managed file |

Changing seed content changes `content` → in-place update for `local_file` when only content changes.

### `terraform_data.seed_fingerprint`

| Argument | Purpose |
|----------|---------|
| `input` | Value stored and compared; changing it replaces this object |

Useful later with `replace_triggered_by` (next tutorials). Here it makes the seed checksum visible as a managed address without an external provider.

### Outputs

`derived_md5` comes from a **resource** attribute; `seed_md5` from a **data** attribute — same expression style, different ownership.

## Validation

```bash
mkdir -p /tmp/rebash-tf-res-check && cd /tmp/rebash-tf-res-check
# recreate versions.tf, main.tf, and seed.txt from the lab, then:
terraform fmt -check
terraform init -input=false
terraform validate
terraform plan -input=false
terraform apply -input=false -auto-approve
test -f derived.txt && test -f seed.txt
terraform destroy -input=false -auto-approve
test -f seed.txt && test ! -f derived.txt
```

| Check | Pass criteria |
|-------|----------------|
| `validate` | Success after init |
| Plan | Creates `local_file.derived` (and `terraform_data`), not the seed as a managed twin |
| Apply | `derived.txt` matches trimmed seed content |
| Destroy | Removes `derived.txt`; leaves `seed.txt` |
| Mental model | You can explain manage vs read for each address |

## Best Practices

- Decide ownership first: if you create it, manage it as a resource; if someone else owns it, read it
- Prefer passing outputs between modules you control over scraping the same objects with data sources
- Document ForceNew / replacement behaviour for critical resources in the module README
- Keep data source filters tight (tags, exact name) to avoid picking the wrong object
- Pin provider versions so data source schemas do not surprise you mid-flight
- Use `moved` blocks when renaming addresses instead of destroy/create
- Prefer `terraform_data` over adding the null provider for triggers

## Security Considerations

- Data sources can read sensitive attributes into state (passwords, private keys) — treat state as secret
- Least-privilege plan roles may lack read permissions some data sources need — design CI roles deliberately
- Do not use data sources to pull secrets into plaintext outputs
- Unmanaged seed files in repos must not contain production credentials
- Review plans when data sources change remote IDs unexpectedly (AMI swap, security group drift)

## Common Mistakes

!!! warning "Managing the same object as both data and resource"
    Two owners fight; plans thrash. **Fix:** Pick one model — import into a resource or read-only data.

!!! warning "Assuming data sources are free"
    Every plan may call APIs. **Fix:** Narrow filters; cache at the platform layer if needed; watch rate limits.

!!! warning "Using a data source because ‘import is hard’"
    Leaves ownership unclear forever. **Fix:** Plan an import/`moved` migration when you should own the object.

!!! warning "Ignoring replace plans"
    “Update” that is actually replace destroys the old object. **Fix:** Read the plan symbols (`-/+`) carefully.

## Troubleshooting

| Issue | Symptoms | Cause | Resolution |
|-------|----------|-------|------------|
| Data source not found | Plan error on missing file/API object | Seed missing or wrong filter | Create seed; fix filename/filter |
| Unexpected replace | `-/+` in plan | ForceNew argument changed | Confirm intent; use lifecycle / blue-green |
| Derived not updating | Stale content | Did not apply after seed edit | Re-plan and apply |
| Destroy deleted too much | Seed gone | Seed was accidentally a resource | Do not manage bootstrap files you want to keep |
| Init provider errors | Cannot download local | Network / constraint | Check Registry access; `~> 2.9` |

## Interview Questions

1. What is the difference between a resource and a data source?
   *Resources are managed (CRUD + state ownership); data sources read existing objects without managing lifecycle.*

2. When is a data source preferable to duplicating configuration?
   *When another system is the source of truth and you only need attributes (AMI ID, VPC ID, file content).*

3. How does Terraform decide to create, update, or replace a resource?
   *By comparing config to state (and refresh); provider schema marks which changes are in-place vs ForceNew.*

4. What is ForceNew behaviour at a high level?
   *Changing certain arguments requires destroying and recreating the object instead of updating it in place.*

5. How do you reference a data source attribute in a resource?
   *`data.<TYPE>.<NAME>.<ATTR>`, for example `data.local_file.seed.content`.*

6. Why can data sources cause plans to change without config edits?
   *They re-read remote or local objects each plan; external changes alter exported attributes.*

7. When should you avoid data sources at plan time?
   *When plan-only CI lacks read permission, or when reads are expensive/unstable — design roles and caching accordingly.*

8. How do count/for_each change resource addressing?
   *Addresses gain indices or keys: `local_file.x[0]` or `local_file.x["a"]`.*

9. What appears in state for a data source?
   *Read results are tracked for the run; they are not “managed” like resources but attributes are available and may be recorded.*

10. How would you import an existing object later in the track?
    *Use `terraform import` or import blocks so Terraform adopts an existing real object under a resource address.*

11. Why pin provider versions when using data sources?
    *Schema and filter behaviour can change across provider majors; pins keep plans reproducible.*

12. Describe a safe pattern for reading remote state outputs.
    *Use `terraform_remote_state` or a dedicated data plane (SSM, Consul) with least privilege; prefer explicit outputs over scraping.*

## Summary

- Resources own lifecycle; data sources read without owning
- Addresses and attributes connect them in expressions and the dependency graph
- Watch replace versus update, and never double-manage the same object
- Lab takeaway: destroy removes `derived.txt` but leaves your unmanaged `seed.txt`

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Variables, Locals, and Outputs](variables-locals-and-outputs.md)
- Next: [Dependencies and the Resource Graph](dependencies-and-the-resource-graph.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Resources](https://developer.hashicorp.com/terraform/language/resources)
2. [Data Sources](https://developer.hashicorp.com/terraform/language/data-sources)
3. [Resource Behaviour](https://developer.hashicorp.com/terraform/language/resources/behavior)
4. [terraform_data](https://developer.hashicorp.com/terraform/language/resources/terraform-data)
5. [hashicorp/local provider](https://registry.terraform.io/providers/hashicorp/local/latest)
6. [Terraform language](https://developer.hashicorp.com/terraform/language)
7. [Terraform Registry](https://registry.terraform.io/)
