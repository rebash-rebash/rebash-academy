---
title: Variables, Locals, and Outputs
description: "Design typed variables, locals, and outputs with validation blocks and clear module contracts."
difficulty: beginner
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - variables
  - outputs
prerequisites:
  - Completed Providers and the Terraform Plugin Model
comments: false
---

# Variables, Locals, and Outputs

## Overview

Inputs and outputs are the **API of every module**. Callers should not need to read your resource graph to know what to pass in or what comes out. Typed variables, validation blocks, locals for derived values, and carefully marked outputs turn a pile of `.tf` files into a contract other engineers (and CI) can trust.

This tutorial covers variable types and precedence, when to use locals versus variables, sensitive handling, and how `TF_VAR_` / `*.auto.tfvars` fit production pipelines — then you will run a complete local lab with validation that rejects bad environment names.

This is **Tutorial 5** in **Module 2: Core Building Blocks** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Declare typed variables with `description`, `type`, `default`, and `validation`
- [ ] Predict value precedence across CLI flags, tfvars files, and environment variables
- [ ] Use locals to simplify expressions without exposing internal details
- [ ] Export outputs and mark sensitive values so CLI and logs redact them
- [ ] Pass values with `TF_VAR_`, `terraform.tfvars`, and `*.auto.tfvars`
- [ ] Explain why secrets must never have defaults committed to Git

## Prerequisites

- Completed [Providers and the Terraform Plugin Model](providers-and-the-terraform-plugin-model.md)
- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files
- No cloud account required for this lab

## Architecture

Values flow inward through variables (and optional tfvars), are composed in locals, drive resource arguments, and flow outward through outputs. Sensitive flags suppress display — they do not remove values from state.

![Architecture diagram for Variables, Locals, and Outputs](../assets/images/terraform-variables-flow.svg)

| Construct | Role |
|-----------|------|
| **Variables** | Public inputs to the module |
| **tfvars / CLI / env** | How callers supply those inputs |
| **Locals** | Private derived values |
| **Resources** | Consumers of `var.*` and `local.*` |
| **Outputs** | Public results after apply |

## Theory

### Why typed inputs matter

Without types and validation, every root module becomes a guessing game: is `env` `"prod"` or `"production"`? Is `count` a string that happened to look like a number? Production failures from typos are expensive; catching them at `plan` is cheap.

Variables are the **module contract**. Treat them like function parameters: name them clearly, document them, constrain them, and omit defaults when the caller must decide.

### Variable block anatomy

```hcl
variable "env" {
  description = "Deployment environment label"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.env)
    error_message = "env must be one of: dev, staging, prod."
  }
}
```

| Argument | Purpose |
|----------|---------|
| `description` | Human-readable contract for docs and Registry |
| `type` | `string`, `number`, `bool`, `list`, `map`, `set`, `object`, `tuple`, or combinations |
| `default` | Optional; omit for required secrets and env-specific values |
| `sensitive` | Redacts the value in CLI UI (still stored in state) |
| `nullable` | Whether `null` is allowed when a default exists (Terraform 1.1+) |
| `validation` | One or more blocks; `condition` must be `true` |

### Variable precedence (highest wins)

When the same variable is set in multiple places, Terraform picks the highest source:

1. `-var` / `-var-file` on the CLI (later `-var-file` overrides earlier ones for the same key)
2. `*.auto.tfvars` / `*.auto.tfvars.json` (alphabetical among auto files)
3. `terraform.tfvars` / `terraform.tfvars.json`
4. Environment `TF_VAR_name` (for `variable "name"`)
5. Default in the `variable` block

**When to use each:**

| Mechanism | Best for |
|-----------|----------|
| `terraform.tfvars` | Local defaults for a personal sandbox (often gitignored if secrets) |
| `*.auto.tfvars` | Machine-local overrides that always load |
| `-var-file=prod.tfvars` | Explicit environment selection in CI |
| `TF_VAR_*` | Secrets and ephemeral values from a vault or pipeline |
| `-var` | One-off overrides while debugging |

### Locals vs variables vs outputs

| Concept | Direction | Visible to callers? | Use when |
|---------|-----------|---------------------|----------|
| **Variable** | In | Yes (API) | Value must be supplied or defaulted from outside |
| **Local** | Internal | No | Derived names, tags maps, joined strings, conditionals |
| **Output** | Out | Yes (API) | Other modules, humans, or remote state consumers need the value |

Locals keep expressions DRY. Prefer:

```hcl
locals {
  name_prefix = "${var.env}-${var.app_name}"
  common_tags = {
    Environment = var.env
    ManagedBy   = "terraform"
  }
}
```

over repeating `"${var.env}-${var.app_name}"` in five resources. Do **not** put secrets in locals “for convenience” if those locals feed non-sensitive outputs.

### Sensitive variables and outputs

Mark both ends when a value is secret:

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}

output "db_password" {
  value     = var.db_password
  sensitive = true
}
```

Sensitive outputs are redacted in normal `terraform output` and plan UI. `terraform output -raw db_password` still prints them — protect CI logs. Sensitivity is a **display** control; state and plan files may still contain the plaintext. Never commit real secrets in tfvars.

### Complex types and module boundaries

Object and map types document structure:

```hcl
variable "database" {
  type = object({
    engine  = string
    version = string
    multi_az = bool
  })
}
```

Pass objects between modules as whole values rather than dozens of flat strings. Validate nested fields with `validation` blocks that inspect `var.database.engine`.

### Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| Many required variables | Forces explicit environments | Noisy CLI for labs |
| Generous defaults | Fast local iteration | Silent wrong values in prod |
| Strict validation | Fails fast | Must evolve allow-lists |
| Sensitive everywhere | Safer logs | Harder debugging; still in state |

Production roots: required variables for environment and secrets, validated enums for stages, locals for naming, minimal sensitive outputs.

## Hands-on Lab

You will build a root module that validates `env`, composes a name prefix in locals, writes a config file with `hashicorp/local`, and demonstrates a sensitive output — without cloud credentials.

### Step 1 – Create the working directory

**Objective:** Start from a clean lab root.

**Explanation:** Isolating each tutorial directory avoids state collisions with earlier labs.

```bash
mkdir -p ~/rebash-tf-vars && cd ~/rebash-tf-vars
```

**Expected:** Shell prompt is inside `~/rebash-tf-vars`.

### Step 2 – Write `versions.tf`

**Objective:** Pin Terraform and the local provider.

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

**Expected:** File saved; as of this writing `hashicorp/local` latest is **2.9.0**.

### Step 3 – Write variables, locals, resource, and outputs

**Objective:** Express the full input → local → resource → output path.

Create `main.tf`:

```hcl
variable "env" {
  description = "Deployment environment label"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.env)
    error_message = "env must be one of: dev, staging, prod."
  }
}

variable "app_name" {
  description = "Short application name used in filenames"
  type        = string
  default     = "payments"
}

variable "db_password" {
  description = "Lab-only secret to demonstrate sensitive handling"
  type        = string
  sensitive   = true
}

locals {
  name_prefix = "${var.env}-${var.app_name}"
  note        = "Deploy target for ${local.name_prefix}"
}

resource "local_file" "config" {
  filename        = "${path.module}/out/${local.name_prefix}.cfg"
  content         = <<-EOT
    ${local.note}
    # password length (not value): ${length(var.db_password)}
  EOT
  file_permission = "0644"
}

output "config_path" {
  description = "Path of the generated configuration file"
  value       = local_file.config.filename
}

output "name_prefix" {
  description = "Computed naming prefix from locals"
  value       = local.name_prefix
}

output "db_password" {
  description = "Echo of the sensitive input (redacted in normal CLI UI)"
  value       = var.db_password
  sensitive   = true
}
```

**Expected:** One file containing variables, locals, resource, and outputs (fine for a lab; production often splits files).

### Step 4 – Supply values via auto tfvars

**Objective:** Load inputs without typing `-var` every time.

```bash
mkdir -p out
cat > secret.auto.tfvars <<'EOF'
env         = "dev"
db_password = "not-a-real-secret"
EOF
```

**Expected:** `secret.auto.tfvars` present. **Do not commit** files like this with real passwords — use `.gitignore` and examples with placeholders.

### Step 5 – Init, plan, and apply

**Objective:** Prove validation passes and the file is created.

```bash
terraform init -input=false
terraform plan -input=false -out=tfplan
terraform apply -input=false tfplan
```

**Expected:** Plan creates `local_file.config`. Apply writes `out/dev-payments.cfg`. Outputs show `config_path` and `name_prefix`; `db_password` appears as `(sensitive)`.

### Step 6 – Inspect outputs and validation failure

**Objective:** See redaction and a failed validation.

```bash
terraform output
terraform output -raw db_password
cat out/dev-payments.cfg
terraform plan -input=false -var='env=qa' 2>&1 | head -40
```

**Expected:** Normal `output` redacts the password; `-raw` prints it. Config file shows length, not the secret. Plan with `env=qa` fails validation with your error message.

### Step 7 – Clean up

**Objective:** Remove managed artefacts and local secrets from the lab folder.

```bash
terraform destroy -input=false -auto-approve
rm -f secret.auto.tfvars tfplan
```

**Expected:** Managed file gone; tfvars and plan file deleted so secrets and planned values are not left behind.

## Code Walkthrough

### Variable arguments

| Argument / block | Role in this lab |
|------------------|------------------|
| `variable.env` without default | Forces an explicit environment via tfvars |
| `validation.condition` | Restricts to an allow-list before any provider call |
| `variable.db_password.sensitive` | Redacts in CLI; still recorded in state |
| `app_name` default | Safe non-secret default for labs |

### Locals

`name_prefix` and `note` are derived once. Changing `env` or `app_name` updates the filename and content together — one place to reason about naming.

### `local_file.config`

| Argument | Purpose |
|----------|---------|
| `filename` | Uses `path.module` and the local prefix so paths stay portable |
| `content` | Heredoc embeds the note and **length** of the password only |
| `file_permission` | `0644` is a sensible lab default |

Never write the raw password into a non-sensitive file or output.

### Outputs

`config_path` and `name_prefix` are safe to share. `db_password` is marked sensitive so casual `terraform output` and many CI log scrapers do not dump it — remember `-raw` and state still can.

## Validation

From a fresh copy of the lab (or after re-creating files):

```bash
terraform fmt -check
terraform init -input=false
terraform validate
# with secret.auto.tfvars present:
terraform plan -input=false
# expect failure:
terraform plan -input=false -var='env=qa'; true
test ! -f out/dev-payments.cfg || echo "destroy first if leftover"
```

| Check | Pass criteria |
|-------|----------------|
| Formatting | `fmt -check` exits 0 |
| Configuration | `validate` succeeds after init |
| Happy path | Plan proposes create for `local_file.config` with `env=dev` |
| Validation | `env=qa` fails with the custom error message |
| Sensitivity | `terraform output` redacts `db_password` |
| Cleanup | Destroy removed the managed file; tfvars deleted |

## Best Practices

- Always set `description` and `type` on variables; treat missing descriptions as incomplete APIs
- Prefer validation allow-lists for environments, regions, and instance size enums
- Omit defaults for secrets and for any value that must differ per environment
- Put derived tags, names, and ARNs in locals — not in duplicated string literals
- Keep outputs small: IDs, names, endpoints callers need — not entire resource objects
- Use `*.tfvars.example` in Git; real tfvars with secrets stay out of the repository
- In CI, prefer `-var-file` for non-secrets and a secret store → `TF_VAR_` for passwords
- Document precedence for your team so nobody wonders why a laptop `auto.tfvars` overrode CI

## Security Considerations

- Sensitive flags do **not** encrypt state; remote backends and IAM still matter
- Never put production passwords in `default = "..."` — they land in Git forever
- Plan files and `terraform.tfstate` may contain secret values; gitignore them
- Restrict who can run `terraform output -raw` and who can read state in the backend
- Avoid echoing secrets in `local-exec` provisioners or debug `TF_LOG` traces
- Review pull requests for accidental `secret.auto.tfvars` or hardcoded tokens

## Common Mistakes

!!! warning "Putting secrets in defaults"
    They land in Git history. **Fix:** No default for secrets; inject via CI or a secret manager into `TF_VAR_`.

!!! warning "Forgetting `sensitive = true` on outputs"
    Passwords appear in logs and chat paste-backs. **Fix:** Mark both the variable and the output; still assume state is sensitive.

!!! warning "Using locals as a secret store"
    Locals feeding non-sensitive outputs leak. **Fix:** Trace every path from secret input to output and file content.

!!! warning "Relying on undocumented precedence"
    A forgotten `*.auto.tfvars` on a laptop overrides CI values. **Fix:** Document and gitignore personal auto files; use explicit `-var-file` in pipelines.

## Troubleshooting

| Issue | Symptoms | Cause | Resolution |
|-------|----------|-------|------------|
| Validation error on plan | Custom `error_message` | Value outside allow-list | Fix tfvars or widen validation deliberately |
| “No value for required variable” | Plan aborts early | Missing tfvars / `TF_VAR_` / `-var` | Supply `env` and `db_password` |
| Sensitive value visible | Appears in logs | Used `-raw` or logged state | Stop logging raw outputs; scrub CI |
| Wrong env applied | Filename uses unexpected prefix | Precedence: auto.tfvars vs `-var` | Print effective values with a non-sensitive output; check load order |
| `validate` fails | Syntax / type errors | Typo in type or expression | Read file:line; run `terraform fmt` |
| Leftover cfg file | File still on disk after destroy | Destroy skipped or wrong directory | Re-run destroy from the lab root |

## Interview Questions

1. When do you use variable validation blocks?
   *To reject invalid inputs at plan time — enums, ranges, and format checks — before providers run.*

2. Why might an output be marked sensitive?
   *So CLI and many UIs redact it; the value may still exist in state and plan files.*

3. How do `terraform.tfvars` and `-var-file` interact?
   *CLI `-var-file` overrides `terraform.tfvars` for the same keys; later `-var-file` wins over earlier ones.*

4. What is the precedence order for variable assignment?
   *CLI `-var`/`-var-file`, then `*.auto.tfvars`, then `terraform.tfvars`, then `TF_VAR_`, then defaults.*

5. When should a value be a local instead of an output?
   *When only this module needs the derived value; export only what callers require.*

6. How do you pass complex objects between modules?
   *Declare `object({...})` or map types on variables/outputs and pass the whole object as a module argument.*

7. What happens if a validation condition fails?
   *Plan/apply aborts with `error_message`; no provider mutations from that run.*

8. Why document variables with descriptions?
   *Descriptions are the human API — Registry docs, IDE hints, and onboarding depend on them.*

9. How do nullable and default interact?
   *With a default, `nullable = false` (default behaviour in modern Terraform) rejects explicit `null` unless configured otherwise — know your version’s rules.*

10. When is an output referring to a resource attribute safe?
    *When the attribute is non-secret (IDs, names, ARNs that are not credentials) and needed by callers.*

11. How would you structure tfvars for dev vs prod?
    *Separate `dev.tfvars` / `prod.tfvars` (or CI variable sets), select with `-var-file`, keep secrets out of Git.*

12. What belongs in `outputs.tf` versus a data file?
    *Outputs publish computed infrastructure results; static reference data belongs in locals, files, or a config service — not fake outputs.*

## Summary

- Variables, locals, and outputs form the module contract — type and validate inputs, compute privately, export sparingly
- Learn precedence so CI and laptops do not silently disagree
- Mark secrets sensitive at both ends; never default them in Git
- Prefer small reversible labs: apply, inspect redaction and validation failure, then destroy

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Providers and the Terraform Plugin Model](providers-and-the-terraform-plugin-model.md)
- Next: [Resources and Data Sources](resources-and-data-sources.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Input Variables](https://developer.hashicorp.com/terraform/language/values/variables)
2. [Local Values](https://developer.hashicorp.com/terraform/language/values/locals)
3. [Output Values](https://developer.hashicorp.com/terraform/language/values/outputs)
4. [Variable Validation](https://developer.hashicorp.com/terraform/language/values/variables#custom-validation-rules)
5. [Sensitive Values](https://developer.hashicorp.com/terraform/language/values/outputs#suppressing-values-in-cli-output)
6. [hashicorp/local provider](https://registry.terraform.io/providers/hashicorp/local/latest)
7. [Terraform Registry](https://registry.terraform.io/)
