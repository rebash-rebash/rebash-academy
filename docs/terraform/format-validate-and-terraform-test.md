---
title: Format, Validate, and Terraform Test
description: "Use fmt, validate, and terraform test to catch regressions before apply."
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - testing
  - fmt
prerequisites:
  - Completed Import, Moved, and Safe Refactors
comments: false
---

# Format, Validate, and Terraform Test

## Overview

Quality gates keep infrastructure changes safe. **`terraform fmt`** makes style non-negotiable, **`terraform validate`** catches structural mistakes after providers are initialised, and **`terraform test`** runs plan/apply-style scenarios against modules with assertions on outputs and state. Wire all three into CI before any apply job — formatting alone never proved a module correct.

This tutorial builds a tiny `modules/hello` child module that writes a greeting file, authors a `*.tftest.hcl` file, and runs the same gates you should demand on every pull request.

This is **Tutorial 16** in **Module 5: Quality and Security** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Use `terraform fmt` and `fmt -check` correctly
- [ ] Run `terraform validate` after `init`
- [ ] Author `*.tftest.hcl` tests with `run` and `assert` blocks
- [ ] Integrate formatting, validation, and tests into CI
- [ ] Interpret test failures and keep tests hermetic with local providers

## Prerequisites

- Completed [Import, Moved, and Safe Refactors](import-moved-and-safe-refactors.md)
- Terraform CLI **1.9+** (1.15.x recommended; `terraform test` is available on modern 1.x)
- Ability to create directories and edit files
- No cloud account required

## Architecture

Quality gates sit before human review and apply. Each layer catches a different failure mode: style, schema/config errors, and behavioural regressions.

![Architecture diagram for Format, Validate, and Terraform Test](../assets/images/terraform-test.svg)

| Gate | Catches | Does not catch |
|------|---------|----------------|
| `fmt -check` | Style drift | Wrong logic |
| `validate` | Invalid references, type issues (after init) | “Looks valid but wrong” behaviour |
| `terraform test` | Broken module contracts via asserts | Full production IAM/network reality unless you add integration tests |
| `plan` in CI | Unexpected destroys/creates | Policy intent without policy-as-code |

## Theory

### `terraform fmt`

Rewrites HCL to the canonical style. In CI use:

```bash
terraform fmt -check -recursive
```

Exit non-zero if files would change — fail the PR. Developers run `terraform fmt -recursive` locally before push. Do not bikeshed alignment in review; let the tool own whitespace.

### `terraform validate`

Checks that configuration is internally consistent **with providers installed**. Always `init` first (or `terraform validate` after init in that directory). Validate does not access real APIs for most checks and does not prove the plan is safe.

### `terraform test`

Test files are `*.tftest.hcl` (often under `tests/`). They contain:

- Optional top-level `variables` for defaults
- One or more `run` blocks with `command = plan` or `command = apply`
- `assert` blocks with `condition` and `error_message`
- Optional `expect_failures` for negative tests

```hcl
run "ok" {
  command = apply

  assert {
    condition     = output.path != ""
    error_message = "path should be set"
  }
}
```

Tests create temporary state under the module’s test working directories — keep providers local (`local`, `random`, `terraform_data`) so CI needs no cloud credentials.

### What to assert

| Strong asserts | Weak asserts |
|----------------|--------------|
| Output equals expected contract | “Resource exists” without checking value |
| Length / membership of collections | Brittle absolute paths across OS without normalisation |
| Encoded policy (`starts with`, `contains`) | Exact random IDs |

### CI order

1. `fmt -check`
2. `init -input=false`
3. `validate`
4. `test`
5. `plan` (root modules) with artefact upload

Fail fast — do not plan if fmt or validate failed.

### Practical mental model

1. Format so humans review behaviour
2. Validate so Terraform accepts the graph
3. Test so modules keep their promises
4. Plan so environments stay intentional

## Hands-on Lab

### Step 1 – Module under test

```bash
mkdir -p ~/rebash-tf-test/modules/hello/tests
cd ~/rebash-tf-test
terraform version
```

**Expected:** Terraform 1.9+.

### Step 2 – Write module files

`modules/hello/versions.tf`:

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

`modules/hello/variables.tf`:

```hcl
variable "name" {
  description = "Name embedded in the greeting file and outputs"
  type        = string

  validation {
    condition     = length(trimspace(var.name)) > 0
    error_message = "name must be a non-empty string."
  }
}

variable "prefix" {
  description = "Directory prefix under the module for the greeting file"
  type        = string
  default     = "generated"
}
```

`modules/hello/main.tf`:

```hcl
resource "random_id" "nonce" {
  byte_length = 2
}

resource "local_file" "hello" {
  filename = "${path.module}/${var.prefix}/hello-${var.name}.txt"
  content  = "hello ${var.name}\nnonce=${random_id.nonce.hex}\n"
}

resource "terraform_data" "contract" {
  input = {
    name  = var.name
    path  = local_file.hello.filename
    nonce = random_id.nonce.hex
  }
}

output "path" {
  description = "Path to the greeting file"
  value       = local_file.hello.filename
}

output "name" {
  description = "Echo of the input name"
  value       = var.name
}

output "nonce" {
  description = "Random nonce written into the greeting"
  value       = random_id.nonce.hex
}

output "contract" {
  description = "Structured marker for tests"
  value       = terraform_data.contract.output
}
```

**Expected:** Module writes a greeting, exposes path/name/nonce, and stores a `terraform_data` contract object.

### Step 3 – Write the Terraform test file

`modules/hello/tests/basic.tftest.hcl`:

```hcl
variables {
  name = "rebash"
}

run "creates_greeting" {
  command = apply

  assert {
    condition     = output.name == "rebash"
    error_message = "name output should echo the variable"
  }

  assert {
    condition     = length(output.path) > 0
    error_message = "path output must be non-empty"
  }

  assert {
    condition     = length(output.nonce) == 4
    error_message = "nonce should be four hex characters (byte_length=2)"
  }

  assert {
    condition     = output.contract.name == "rebash"
    error_message = "terraform_data contract should record the name"
  }
}

run "plan_is_noop_after_apply" {
  command = plan

  assert {
    condition     = output.name == "rebash"
    error_message = "name should remain stable on subsequent plan"
  }
}
```

**Expected:** First run applies and asserts; second run plans against the prior test state within the test runner’s sequencing for that file.

### Step 4 – Format, validate, and test

```bash
terraform -chdir=modules/hello fmt -recursive
terraform -chdir=modules/hello init -input=false
terraform -chdir=modules/hello validate
terraform -chdir=modules/hello test
```

**Expected:** `Success! The configuration is valid.` and test runs pass with apply + assertions. Failures print the `error_message` from the failing assert.

### Step 5 – Force a failure (learning drill)

Temporarily change the assert to expect `output.name == "wrong"`, re-run `terraform test`, observe the failure text, then revert. Confirm CI would go red on such a regression.

### Step 6 – fmt-check gate

```bash
# Introduce ugly spacing, then:
terraform -chdir=modules/hello fmt -check
echo "exit=$?"
terraform -chdir=modules/hello fmt
terraform -chdir=modules/hello fmt -check
```

**Expected:** `-check` fails before format and passes after.

### Step 7 – Optional root wrapper

From `~/rebash-tf-test`, a tiny root can call the module — useful later for plan-on-PR demos. Not required for `terraform test`, which targets the module directory directly.

### Step 8 – Clean up test artefacts

```bash
# terraform test cleans ephemeral state; remove leftover greeting files if any
rm -rf modules/hello/generated
```

**Expected:** Working tree tidy; `.terraform` may remain — safe to delete locally with `rm -rf modules/hello/.terraform`.

## Code Walkthrough

### Module contract

| Output | Why test it |
|--------|-------------|
| `name` | Echo contract for callers |
| `path` | Non-empty path proves the file resource ran |
| `nonce` | Length check avoids asserting unstable exact IDs elsewhere |
| `contract` | Structured `terraform_data` payload for richer asserts |

### `run` blocks

| Argument | Purpose |
|----------|---------|
| `command = apply` | Execute apply semantics for the module under test |
| `command = plan` | Assert on plan-time conditions |
| `assert.condition` | Boolean expression (often on `output.*`) |
| `assert.error_message` | Human-readable CI failure |

### Providers in tests

Pinning `local` and `random` in the module under test keeps CI hermetic. Avoid cloud providers in unit-style module tests unless you maintain integration credentials and cleanup rigorously.

### `fmt` versus `validate`

`fmt` never loads providers. `validate` needs plugin schemas from `init`. Both belong in CI; neither replaces tests.

## Validation

```bash
terraform -chdir=modules/hello fmt -check
terraform -chdir=modules/hello init -input=false
terraform -chdir=modules/hello validate
terraform -chdir=modules/hello test
```

| Check | Pass criteria |
|-------|----------------|
| Formatting | `fmt -check` exits 0 |
| Configuration | `validate` succeeds |
| Tests | All `run` blocks pass |
| Assertions | name, path, nonce length, contract.name verified |
| Hermetic | No cloud credentials required |

## Best Practices

- Run `fmt -check`, `validate`, `test`, then `plan` in that order in CI
- Keep module tests fast and local; add separate integration jobs for cloud
- Assert contracts (outputs), not incidental formatting of provider diffs
- Commit `.terraform.lock.hcl` for modules you publish or share
- Use `validation` blocks on variables plus tests — defence in depth
- Name `run` blocks with intent (`creates_greeting`, not `test1`)

## Security Considerations

- Tests that apply still write state and files — exclude secrets from fixtures
- Do not log sensitive variable values in `error_message` strings
- Cache provider plugins in CI carefully; verify lockfile checksums
- Fail closed: a red test job must block merge
- Treat plan artefacts from CI as potentially sensitive even for local providers if variables ever include secrets

## Common Mistakes

!!! warning "Only formatting in CI"
    Invalid configs merge. **Fix:** fmt + validate + test + plan.

!!! warning "Asserting exact random IDs"
    Flaky tests. **Fix:** Assert length, prefix, or patterns — not one-off hex strings unless fixed with a test seed pattern you control.

!!! warning "Running validate before init"
    Confusing errors. **Fix:** Always init in that module/root first.

!!! warning "Cloud credentials in unit tests"
    Slow, costly, flaky. **Fix:** Local providers for unit tests; separate integration pipeline.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `terraform test` not found | Old CLI | Upgrade to Terraform 1.9+ |
| Assert fails on path separators | OS path differences | Assert `endswith` / `contains` instead of full string equality |
| Provider missing in test | Module lacks `required_providers` | Declare providers in the module under test |
| fmt thrash | Mixed tool versions | Standardise Terraform version in CI and local via `required_version` |
| Tests pass but prod fails | Only unit coverage | Add plan policies and staging applies |

## Interview Questions

1. What does `terraform test` add beyond `validate`?
   *Behavioural assertions via plan/apply runs against a module, not just structural validity.*

2. Where do `.tftest.hcl` files live?
   *Commonly under a `tests/` directory inside the module; Terraform discovers `*.tftest.hcl` relative to the module.*

3. How do you run tests in CI?
   *After fmt and init/validate, run `terraform test` in the module directory and fail the job on non-zero exit.*

4. What assertions are useful for a module?
   *Output contracts, invariant lengths, required tag keys, and expected resource counts — not flaky random values.*

5. Why is `fmt -check` valuable in pull requests?
   *It enforces canonical style automatically so reviews focus on behaviour and safety.*

6. What can `validate` not catch?
   *Wrong business logic, unsafe plans, missing cloud permissions, and policy violations.*

7. How do you structure tests for child modules?
   *Colocate `tests/*.tftest.hcl` with the module; keep fixtures hermetic; assert published outputs.*

8. When do integration-style tests need cloud credentials?
   *When asserting real provider APIs; isolate them from unit tests and clean up aggressively.*

9. How do you keep tests hermetic with local providers?
   *Declare `local`/`random` only, avoid network resources, and assert on outputs rather than external side effects.*

10. What is the difference between unit and contract tests here?
    *Unit tests exercise one module quickly; contract tests lock the output API callers rely on.*

11. How do you fail a pipeline on test failure?
    *Do not `continue-on-error`; use non-zero exit from `terraform test` as a required status check.*

12. Why test outputs and not only resources?
    *Outputs are the module’s public API; resources may refactor while the contract stays stable.*

## Summary

- `fmt`, `validate`, and `terraform test` catch different classes of defects — use all three
- Prefer hermetic module tests with local providers in everyday CI
- Assert contracts, not flaky identifiers
- Quality gates belong before apply, never instead of reading the plan
- Treat test failures as merge blockers in production repositories

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Import, Moved, and Safe Refactors](import-moved-and-safe-refactors.md)
- Next: [Secrets and Sensitive Values](secrets-and-sensitive-values.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [terraform test](https://developer.hashicorp.com/terraform/language/tests)
2. [Tests — CLI](https://developer.hashicorp.com/terraform/cli/commands/test)
3. [terraform fmt](https://developer.hashicorp.com/terraform/cli/commands/fmt)
4. [terraform validate](https://developer.hashicorp.com/terraform/cli/commands/validate)
5. [terraform_data resource](https://developer.hashicorp.com/terraform/language/resources/terraform-data)
6. [hashicorp/local provider](https://registry.terraform.io/providers/hashicorp/local/latest)
7. [hashicorp/random provider](https://registry.terraform.io/providers/hashicorp/random/latest)
