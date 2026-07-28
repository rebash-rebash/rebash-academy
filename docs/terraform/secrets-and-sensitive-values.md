---
title: Secrets and Sensitive Values
description: "Mark sensitive values correctly, keep secrets out of Git, and reduce accidental exposure in plans and state."
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - security
  - secrets
prerequisites:
  - Completed Format, Validate, and Terraform Test
comments: false
---

# Secrets and Sensitive Values

## Overview

Terraform **state** and **plans** can contain secrets: database passwords, API tokens, private keys. Marking a variable `sensitive = true` redacts CLI output — it does **not** remove the value from state. Production practice is layered: keep secrets out of Git, inject them at run time, prefer secret managers and write-only patterns where available, encrypt and lock remote state, and treat plan artefacts as confidential.

This lab uses `local_sensitive_file` and sensitive variables with `TF_VAR_` injection — no cloud account required — so you can see redaction behaviour safely.

This is **Tutorial 17** in **Module 5: Quality and Security** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Mark variables and outputs `sensitive`
- [ ] Prefer `local_sensitive_file` for secret material on disk
- [ ] Keep secrets out of Git and demonstrate `TF_VAR_` injection
- [ ] Explain why state remains a secret store even with redaction
- [ ] Outline CI and secret-manager patterns for production

## Prerequisites

- Completed [Format, Validate, and Terraform Test](format-validate-and-terraform-test.md)
- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files
- No cloud account required for the lab

## Architecture

Secrets enter Terraform through variables, provider credentials, or data sources. They flow into resource arguments, then into state and often into plan files. Sensitivity flags control display — backends and IAM control storage and access.

![Architecture diagram for Secrets and Sensitive Values](../assets/images/terraform-secrets.svg)

| Control | What it does | What it does not do |
|---------|--------------|---------------------|
| `sensitive = true` | Redacts CLI/UI display | Remove values from state |
| `local_sensitive_file` | Avoids casual echo of file resources | Encrypt state |
| Secret manager + data source | Central rotation and audit | Eliminate state copies automatically |
| Encrypted remote state + IAM | Limits who can read secrets at rest | Fix secrets committed to Git history |

## Theory

### Rules of thumb

1. Never commit real `*.tfvars` containing secrets — commit `*.tfvars.example` with placeholders
2. Mark sensitive variables and outputs
3. Encrypt remote state; restrict IAM who can `GetObject` / read state
4. Prefer cloud secret stores (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, HashiCorp Vault) and data sources
5. Assume plan JSON and CI logs may contain values — protect artefacts and scrub logs
6. Prefer short-lived credentials (OIDC) over long-lived access keys in CI

### What `sensitive` changes

- `terraform output` hides values unless `-json` / `-raw` is used carefully in trusted contexts
- Plan UI redacts known sensitive attributes
- Sensitivity propagates through expressions (a sensitive input taints derived values)

What it does **not** change: persistence in `terraform.tfstate`, many provider APIs, or shoulder-surfable `TF_VAR_` environment variables in process listings.

### `local_sensitive_file` versus `local_file`

Use `local_sensitive_file` when content is secret: providers and Terraform treat it with more care in logs. State may still store content — protect the backend. Set `file_permission = "0600"` and keep paths out of world-readable directories.

### Ephemeral values (Terraform 1.10+ conceptual note)

Newer Terraform versions introduce **ephemeral** values for secrets that should not be stored in state. Treat this as an evolving capability: verify your CLI version and provider support before relying on it in production. Until then, assume state may hold secrets and design accordingly.

### Injection patterns

| Pattern | Lab / prod fitness |
|---------|-------------------|
| `TF_VAR_name` env vars | Good for CI secrets and local drills |
| CI secret store → env | Standard for pipelines |
| Provider data source to ASM/Vault | Preferred for runtime fetch |
| Hard-coded default in `variable` | Never for real secrets |
| Committed `secrets.auto.tfvars` | Incident waiting to happen |

### Practical mental model

1. Classify every value: public, internal, secret
2. Secrets: sensitive flags + out-of-band injection + protected state
3. Never print secrets in `local-exec`, provisioners, or debug logs
4. Rotate when exposure is suspected — redaction is not rotation

## Hands-on Lab

### Step 1 – Create the working directory

```bash
mkdir -p ~/rebash-tf-secrets/.secrets && cd ~/rebash-tf-secrets
terraform version
```

**Expected:** Terraform 1.9+.

### Step 2 – Write `versions.tf`

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

### Step 3 – Write `variables.tf` and `main.tf`

`variables.tf`:

```hcl
variable "api_token" {
  description = "Lab-only API token — inject via TF_VAR_api_token"
  type        = string
  sensitive   = true
}

variable "project" {
  description = "Non-sensitive project label"
  type        = string
  default     = "rebash-academy"
}
```

`main.tf`:

```hcl
resource "random_password" "demo" {
  length  = 16
  special = false
}

resource "local_sensitive_file" "token" {
  filename        = "${path.module}/.secrets/token"
  content         = var.api_token
  file_permission = "0600"
}

resource "local_sensitive_file" "generated" {
  filename        = "${path.module}/.secrets/generated-password"
  content         = random_password.demo.result
  file_permission = "0600"
}

resource "terraform_data" "secret_meta" {
  input = {
    project       = var.project
    token_length  = length(var.api_token)
    # Do not store the raw token in terraform_data input
  }
}

output "token_path" {
  description = "Path to the sensitive token file"
  value       = local_sensitive_file.token.filename
}

output "api_token" {
  description = "Echo of the token — sensitive, for redaction demo only"
  value       = var.api_token
  sensitive   = true
}

output "password_length" {
  description = "Length of generated password (safe to show)"
  value       = length(random_password.demo.result)
}

output "meta" {
  description = "Non-secret metadata marker"
  value       = terraform_data.secret_meta.output
}
```

**Expected:** Token and generated password land only under `.secrets/` with mode `0600`; outputs mark the raw token sensitive.

### Step 4 – Inject the secret and apply

```bash
export TF_VAR_api_token='lab-only-token'
terraform fmt
terraform init -input=false
terraform validate
terraform plan -input=false -out=tfplan
terraform apply -input=false tfplan
terraform output
terraform output -raw api_token
ls -la .secrets/
```

**Expected:** `terraform output` redacts `api_token` (shows `(sensitive value)`). `token_path`, `password_length`, and `meta` print. `-raw` reveals the token — use only in trusted shells. Files under `.secrets/` exist with restrictive permissions.

### Step 5 – Prove Git hygiene

```bash
# Do NOT commit real secrets — demonstrate ignore patterns
cat > .gitignore <<'EOF'
.secrets/
*.tfstate
*.tfstate.*
.terraform/
crash.log
override.tf
terraform.tfvars
EOF

# Safe example file for teammates:
cat > secrets.tfvars.example <<'EOF'
# Copy to a gitignored tfvars or use TF_VAR_api_token instead
# api_token = "replace-me"
project = "rebash-academy"
EOF
```

**Expected:** `.gitignore` excludes state and `.secrets/`; only the example file would be committed in a real repo.

### Step 6 – Inspect state caution (read-only lesson)

```bash
# Demonstrates that sensitivity is display-deep, not storage-deep:
grep -o 'lab-only-token' terraform.tfstate && echo "token present in state" || echo "not found"
```

**Expected:** The lab token string appears inside state JSON. Treat this as the core lesson: **protect state**.

### Step 7 – Clean up

```bash
terraform destroy -input=false -auto-approve
unset TF_VAR_api_token
rm -rf .secrets
```

**Expected:** Sensitive files gone; env var cleared so the next shell session does not leak the lab token.

## Code Walkthrough

### `variable.api_token`

| Argument | Purpose |
|----------|---------|
| `sensitive = true` | Redact in CLI plans/outputs |
| No `default` | Forces injection — good habit for secrets |

### `local_sensitive_file`

| Argument | Purpose |
|----------|---------|
| `filename` | Path under `.secrets/` |
| `content` | Secret body from variable or `random_password` |
| `file_permission` | `0600` reduces local exposure |

### `random_password.demo`

Generates a secret inside Terraform. Convenient — and it **will** enter state. For production databases, prefer a secret manager that owns the material and injects references, or ephemeral patterns when your versions support them.

### `terraform_data.secret_meta`

Stores **lengths and labels**, not the token itself — a pattern for markers without duplicating secrets into extra state attributes unnecessarily (the file resources already hold content).

### Sensitive output

Mark outputs sensitive when they expose secrets to callers. Downstream modules inherit sensitivity.

## Validation

```bash
export TF_VAR_api_token='lab-only-token'
terraform fmt -check
terraform init -input=false
terraform validate
terraform apply -input=false -auto-approve
terraform output
test -f .secrets/token
stat -f '%Lp' .secrets/token 2>/dev/null || stat -c '%a' .secrets/token
terraform destroy -input=false -auto-approve
unset TF_VAR_api_token
```

| Check | Pass criteria |
|-------|----------------|
| Redaction | Default `terraform output` hides `api_token` |
| Permissions | Token file mode is `600` |
| State lesson | You understand secrets persist in state |
| Git | `.secrets/` and state gitignored |
| Cleanup | Destroy + unset env completed |

## Best Practices

- Default variables that are secrets: **no default**, `sensitive = true`, documented injection method
- Prefer secret managers for production; use Terraform to wire references/IAM, not to own long-lived passwords when avoidable
- Encrypt remote state (SSE-KMS / customer-managed keys) and enable locking
- Separate plan viewers from apply credentials where possible
- Rotate credentials after accidental commit; rewrite history is not enough for public repos — rotate first
- Add `*.tfvars` with secrets to `.gitignore` before the first commit

## Security Considerations

- Plan files (`tfplan`) can contain plaintext secrets — store as confidential CI artefacts with short retention
- `terraform console` and `-raw` outputs bypass casual redaction — restrict access
- Provisioners that `echo` secrets to logs are incidents
- Least-privilege IAM on state buckets/containers; block public access
- Remember provider credentials themselves are secrets — prefer OIDC federation in CI (next tutorials)

## Common Mistakes

!!! warning "Printing secrets in provisioners"
    Log leakage in CI. **Fix:** Never echo secrets; avoid `local-exec` for secret material.

!!! warning "Committing terraform.tfvars with tokens"
    Permanent Git history exposure. **Fix:** gitignore, rotate, use CI secrets / managers.

!!! warning "Believing sensitive = true clears state"
    False sense of safety. **Fix:** Protect backends; minimise secret material in managed attributes.

!!! warning "World-readable secret files"
    Local compromise. **Fix:** `0600` and directories excluded from backups/sync tools.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `No value for required variable` | `TF_VAR_api_token` unset | Export the variable or pass `-var` in a trusted shell |
| Output always redacted | Expected for sensitive | Use `-raw` only when necessary and authorised |
| State contains secrets after destroy | Local file not deleted / backup state | Remove `terraform.tfstate*` and `.secrets/`; scrub backups |
| CI prints secrets | Debug logging / set -x | Disable xtrace around secret env; mark outputs sensitive |
| Permission denied on `.secrets` | Directory mode | Create dir with `0700`; fix ownership |

## Interview Questions

1. What does `sensitive = true` change in CLI output?
   *It redacts values in plans and outputs; it does not remove them from state.*

2. Why is state still a secret store even with sensitive flags?
   *State JSON persists attribute values needed for future diffs, including secrets.*

3. Where should production secrets live?
   *In a managed secret store (or ephemeral mechanism), injected at runtime — not in Git.*

4. How do you pass secrets into Terraform safely in CI?
   *CI secret stores → environment variables / OIDC-assumed roles; never commit values.*

5. What is the risk of echoing secrets in `local-exec`?
   *They appear in CI logs and shell histories, often retained longer than state access controls.*

6. How do ephemeral values change secret handling (conceptually)?
   *They aim to avoid persisting certain secrets in state; verify version/provider support before relying on them.*

7. Why avoid plaintext tfvars in Git?
   *Git history is durable and widely cloned; exposure requires rotation and possibly breach response.*

8. How do you redaction-check plan logs?
   *Scan artefacts for known secret patterns; treat plan JSON as confidential; limit who can download artefacts.*

9. What IAM controls protect remote state?
   *Least-privilege read/write on the backend, encryption keys, deny public access, and audited access paths.*

10. How should modules declare sensitive outputs?
    *Mark outputs `sensitive = true` whenever they expose secret material to callers.*

11. What is a secure pattern for rotating secrets with Terraform?
    *Rotate in the secret manager, update consumers, then replace references; avoid dual-writing plaintext into multiple states.*

12. Why is write-only thinking useful for passwords?
    *Providers that accept write-only arguments reduce lingering secret attributes in state — prefer them when available.*

## Summary

- Sensitivity redacts display; state and plans may still hold secrets
- Inject secrets at runtime; never commit them
- Use `local_sensitive_file` and tight permissions for lab/disk cases
- Prefer secret managers and short-lived CI credentials in production
- Protect backends and plan artefacts as confidential systems of record

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Format, Validate, and Terraform Test](format-validate-and-terraform-test.md)
- Next: [Policy as Code Overview](policy-as-code-overview.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Sensitive values](https://developer.hashicorp.com/terraform/language/values/variables#suppressing-values-in-cli-output)
2. [Output values — sensitive](https://developer.hashicorp.com/terraform/language/values/outputs#sensitive-suppressing-values-in-cli-output)
3. [local_sensitive_file](https://registry.terraform.io/providers/hashicorp/local/latest/docs/resources/sensitive_file)
4. [random_password](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/password)
5. [State storage and encryption](https://developer.hashicorp.com/terraform/language/state)
6. [Ephemeral values](https://developer.hashicorp.com/terraform/language/values/variables#ephemeral)
7. [hashicorp/local provider](https://registry.terraform.io/providers/hashicorp/local/latest)
