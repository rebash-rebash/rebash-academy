---
title: Modules — Creating Reusable Infrastructure
description: "Build a child module with typed inputs and outputs, then call it from a root module with a clear contract."
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - modules
prerequisites:
  - Completed Workspaces and Environment Strategies
comments: false
---

# Modules — Creating Reusable Infrastructure

## Overview

**Modules** package reusable infrastructure patterns behind a typed input/output API. Platform teams publish child modules; application teams call them from root modules without copying raw resource blocks. This tutorial builds a local child module and calls it from a root — the fundamental composition skill before consuming Registry modules.

This is **Tutorial 11** in **Module 3: Collaboration and Scale** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Create a child module with variables, resources, and outputs
- [ ] Call modules with the `module` block and a local `source`
- [ ] Use `path.module` correctly inside child modules
- [ ] Design small, composable modules with clear contracts
- [ ] Avoid leaking unnecessary implementation outputs
- [ ] Explain how providers are inherited by child modules

## Prerequisites

- Completed [Workspaces and Environment Strategies](workspaces-and-environment-strategies.md)
- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files
- No cloud account required for this lab

## Architecture

The root module orchestrates; child modules encapsulate implementation. Values enter through module arguments (mapped to variables) and exit through outputs.

![Architecture diagram for Modules — Creating Reusable Infrastructure](../assets/images/terraform-modules.svg)

| Layer | Responsibility |
|-------|----------------|
| **Root** | Backend, providers, composition, env-specific values |
| **Child module** | One reusable pattern (greeting file, VPC, RDS wrapper) |
| **Contract** | Variables in, outputs out — hide resource addresses |

## Theory

### Module block

```hcl
module "greeting" {
  source  = "./modules/greeting"
  project = "rebash"
  message = "hello"
}
```

| Argument | Purpose |
|----------|---------|
| `source` | Local path, Registry address, or Git URL |
| Input labels | Must match child `variable` names |
| Meta-arguments | `count`, `for_each`, `providers`, `depends_on` |

Reference outputs as `module.greeting.path`.

### File layout

```text
modules/greeting/
  versions.tf   # optional required_providers for the module
  variables.tf
  main.tf
  outputs.tf
  README.md
```

Root:

```text
versions.tf
main.tf
outputs.tf
modules/
```

### `path.module` vs `path.root`

| Expression | Meaning |
|------------|---------|
| `path.module` | Directory of the **current** module |
| `path.root` | Directory of the root module |
| `path.cwd` | Process working directory |

Child modules should prefer `path.module` for files they own. Writing into `path.root` couples the module to caller layout — sometimes useful, often brittle.

### Design tips

- **One responsibility** per module (network, secrets wrapper, “greeting file”)
- Typed variables with descriptions and validation
- Stable outputs only (IDs, names, ARNs) — not every attribute
- Sensible defaults for non-secret optional inputs
- Pin external module versions (next tutorial)
- Avoid mega-modules that create an entire company

### Provider inheritance

Child modules inherit provider configurations from the root unless you pass an explicit `providers` map. Declare `required_providers` in modules that need minimum versions so callers get clear errors.

### Composition vs copy-paste

| Approach | When |
|----------|------|
| Child module | Pattern reused across roots or teams |
| Inline resources | One-off, unlikely to reuse |
| Wrapper module | Soften a third-party Registry module’s API |

### Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| Many tiny modules | Reuse, clear reviews | Indirection overhead |
| One mega-module | Fast first demo | Unreviewable, rigid |
| Deep nesting | DRY | Hard graphs and outputs |
| Export everything | Flexible callers | Breaks encapsulation |

## Hands-on Lab

You will create `modules/greeting`, call it from the root, apply, and read the output path.

### Step 1 – Scaffold directories

**Objective:** Standard module folder layout.

```bash
mkdir -p ~/rebash-tf-mod/modules/greeting ~/rebash-tf-mod/generated
cd ~/rebash-tf-mod
```

**Expected:** `modules/greeting` and `generated` exist.

### Step 2 – Author the child module

**Objective:** Typed inputs, one resource, one output.

Create `modules/greeting/variables.tf`:

```hcl
variable "project" {
  description = "Short project name used in the generated filename"
  type        = string

  validation {
    condition     = length(var.project) > 0 && length(var.project) < 32
    error_message = "project must be a non-empty string under 32 characters."
  }
}

variable "message" {
  description = "Body written into the greeting file"
  type        = string
}

variable "file_permission" {
  description = "POSIX file mode for the managed greeting file"
  type        = string
  default     = "0644"
}
```

Create `modules/greeting/main.tf`:

```hcl
resource "local_file" "this" {
  filename        = "${path.module}/../../generated/${var.project}.txt"
  content         = "${var.message}\n"
  file_permission = var.file_permission
}

resource "terraform_data" "fingerprint" {
  input = local_file.this.content_md5
}
```

Create `modules/greeting/outputs.tf`:

```hcl
output "path" {
  description = "Absolute path of the greeting file"
  value       = local_file.this.filename
}

output "md5" {
  description = "Content checksum of the greeting file"
  value       = local_file.this.content_md5
}
```

Create `modules/greeting/versions.tf`:

```hcl
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = ">= 2.9.0"
    }
  }
}
```

**Expected:** Child module is self-contained with a clear API.

### Step 3 – Author the root module

**Objective:** Call the child; re-export only what callers need.

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
module "greeting" {
  source  = "./modules/greeting"
  project = "rebash"
  message = "module-lab"
}

module "greeting_alt" {
  source  = "./modules/greeting"
  project = "rebash-alt"
  message = "second-instance"
}

output "greeting_path" {
  description = "Path from the primary greeting module"
  value       = module.greeting.path
}

output "all_paths" {
  description = "Paths from both module instances"
  value = {
    primary = module.greeting.path
    alt     = module.greeting_alt.path
  }
}
```

**Expected:** Two instances prove modules are reusable like functions.

### Step 4 – Init, plan, apply

**Objective:** Install the module and create both files.

```bash
terraform init -input=false
terraform plan -input=false -out=tfplan
terraform apply -input=false tfplan
cat generated/rebash.txt generated/rebash-alt.txt
terraform output
```

**Expected:** Init installs `./modules/greeting`. Apply creates two files. Outputs show both paths. Addresses look like `module.greeting.local_file.this`.

### Step 5 – Change the module contract carefully

**Objective:** See that callers only depend on outputs.

```bash
# Edit modules/greeting/main.tf content to append a header line, then:
terraform apply -input=false -auto-approve
cat generated/rebash.txt
```

**Expected:** Root `main.tf` unchanged; behaviour updates through the module. That is encapsulation.

### Step 6 – Clean up

**Objective:** Destroy module resources and remove the lab.

```bash
terraform destroy -input=false -auto-approve
rm -f tfplan
cd ~
rm -rf ~/rebash-tf-mod
```

**Expected:** Generated files removed via destroy; directory deleted.

## Code Walkthrough

### Child variables

| Variable | Role |
|----------|------|
| `project` | Validated name segment for the filename |
| `message` | Required body — no default |
| `file_permission` | Optional with safe default |

### `path.module` in the child

Resolves under `modules/greeting/`, so `../../generated` reaches the repo’s `generated/` folder. In production modules, prefer writing only inside a path the caller passes as an input (for example `var.output_dir`) instead of assuming `../../generated`.

### Root `module` blocks

Two instances with different inputs → two state namespaces: `module.greeting.*` and `module.greeting_alt.*`.

### Outputs

Root exports `module.greeting.path` rather than `module.greeting.local_file.this.filename` — callers should not rely on internal resource addresses.

## Validation

```bash
terraform fmt -recursive -check
terraform init -input=false
terraform validate
terraform apply -input=false -auto-approve
test -f generated/rebash.txt && test -f generated/rebash-alt.txt
terraform state list | grep 'module.greeting'
terraform destroy -input=false -auto-approve
```

| Check | Pass criteria |
|-------|----------------|
| fmt | Recursive check passes |
| validate | Success |
| Apply | Two generated files |
| State | Addresses prefixed with `module.` |
| Cleanup | Destroy removes managed files |

## Best Practices

- Write a module README with inputs, outputs, and examples
- Validate inputs at the module boundary
- Keep outputs minimal and stable across minor versions
- Use `terraform-docs` or equivalent in CI for module repos
- Prefer composition of small modules over one monolith
- Version modules when shared across repositories (Git tags / Registry)
- Pass `output_dir` or similar instead of hard-coded relative escapes when possible
- Add examples/ as a tiny root that calls the module for smoke tests

## Security Considerations

- Do not accept raw IAM policies as free-form strings without review patterns
- Sensitive module variables/outputs must be marked — still land in state
- Review child modules like dependencies: supply chain risk applies to internal Git too
- Avoid shelling out via provisioners inside shared modules
- Limit who can merge to module repositories that production roots pin

## Common Mistakes

!!! warning "Mega-modules that create an entire company"
    Unreviewable blast radius. **Fix:** Compose small modules with clear ownership.

!!! warning "Using relative `../` paths as the public API"
    Callers break when layout changes. **Fix:** Pass paths as variables; export stable IDs.

!!! warning "Leaking every resource as an output"
    Tight coupling to internals. **Fix:** Export only what consumers need.

!!! warning "No required_providers in shared modules"
    Confusing version errors at the root. **Fix:** Declare minimum provider needs in the module.

## Troubleshooting

| Issue | Symptoms | Cause | Resolution |
|-------|----------|-------|------------|
| Module not found | Init error | Wrong `source` path | Fix relative path from root |
| Unknown variable | Validate fails | Input name mismatch | Align module args with variables |
| Files in wrong place | Unexpected path | `path.module` relative escape | Pass `output_dir` input |
| Duplicate object | Provider conflict | Two instances same name | Ensure unique `project` values |
| State address confusion | Hard to `state show` | Forgot `module.` prefix | Use `state list` |

## Interview Questions

1. What makes a good module boundary?
   *A single responsibility, typed inputs/outputs, and hidden internals.*

2. How do you version modules for consumers?
   *Git tags or Registry versions; pin in the caller’s `module` block.*

3. Why avoid leaking too many outputs?
   *Callers couple to internals; refactors become breaking changes.*

4. What is path.module inside a child module?
   *The filesystem path of that module’s directory.*

5. How do providers pass into modules?
   *Inherited from the root by default, or via the `providers` meta-argument.*

6. When should a module use count or for_each?
   *When the caller needs N instances driven by a list or map — prefer for_each for stable keys.*

7. How do you test a module locally with a source path?
   *`source = "../.."` or `./modules/...` from an examples root; init/plan/apply.*

8. What belongs in the module README?
   *Purpose, examples, inputs, outputs, and requirements (Terraform/provider versions).*

9. How do input validations protect callers?
   *Fail fast at plan with clear errors before providers mutate anything.*

10. Why pin module sources in production?
    *Unpinned sources can change under you between plans.*

11. What is compositional nesting versus a megamodule?
    *Nesting small modules versus one module that does everything — prefer composition.*

12. How do you refactor a root into modules safely?
    *Extract with `moved` blocks so state addresses follow resources without destroy/create.*

## Summary

- Modules are reusable functions for infrastructure with typed contracts
- Roots compose modules; children hide resource details behind outputs
- Use `path.module` carefully; prefer caller-provided paths in production modules
- Two instances in the lab prove reuse without copy-paste

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Workspaces and Environment Strategies](workspaces-and-environment-strategies.md)
- Next: [Registry Modules and Composition](registry-modules-and-composition.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Modules Overview](https://developer.hashicorp.com/terraform/language/modules)
2. [Module Blocks](https://developer.hashicorp.com/terraform/language/modules/syntax)
3. [Module Composition](https://developer.hashicorp.com/terraform/language/modules/develop/composition)
4. [Publishing Modules](https://developer.hashicorp.com/terraform/registry/modules/publish)
5. [Refactoring with moved](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)
6. [hashicorp/local provider](https://registry.terraform.io/providers/hashicorp/local/latest)
7. [Terraform Registry](https://registry.terraform.io/)
