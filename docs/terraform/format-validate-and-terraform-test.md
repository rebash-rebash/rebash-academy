---
title: "Format, Validate, and Terraform Test"
description: "Gate Terraform changes with fmt, validate, terraform test, Terratest, tflint, and policy checks before apply."
difficulty: intermediate
estimated_time: "45–60 min"
technology: terraform
category: terraform
module: "Module 14 · Testing & Validation"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - testing
  - static-analysis
prerequisites:
  - terraform/terraform-cloud-and-hcp-terraform
next:
  - terraform/terraform-security-and-secrets
related:
  - terraform/troubleshooting-terraform
  - terraform/terraform-in-ci-cd-pipelines
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - testing
  - fmt
  - tflint
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---

# Format, Validate, and Terraform Test

## Overview

Broken Terraform should fail in continuous integration (CI), not during a Friday production apply. **Testing and validation** layers — `terraform fmt`, `terraform validate`, `terraform test`, static analysis, and policy checks — turn infrastructure pull requests into reviewable, assertable artefacts before any privileged apply.

This is **Tutorial 14** in **Module 14: Testing & Validation** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for engineers who own module quality gates.

Beginners learn what each gate catches (and what it cannot). Practitioners wire a gate order into CI. Production judgement covers when Terratest integration tests justify real cloud cost versus native `terraform test` with mock providers.

## Prerequisites

- [Terraform Cloud and HCP Terraform](terraform-cloud-and-hcp-terraform.md)
- Terraform CLI 1.9+ (native `terraform test` requires 1.6+)
- Optional: [tflint](https://github.com/terraform-linters/tflint) installed for static analysis discussion

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Run `terraform fmt -check` and `terraform validate` in CI-safe mode
- [ ] Author a `*.tftest.hcl` file with `run` and `assert` blocks
- [ ] Contrast native `terraform test` with Terratest integration tests
- [ ] Place `tflint` in a validation pipeline
- [ ] Describe where policy validation fits relative to module tests

## Architecture

Validation gates sit between author commit and plan/apply — catching syntax, style, module contracts, and organisational policy.

![Terraform testing](../assets/excalidraw/terraform-testing.svg)

## Theory

### What it is

Terraform validation is a stack of complementary checks:

| Gate | Command / tool | What it catches |
|------|----------------|-----------------|
| Format | `terraform fmt -check -recursive` | Style drift, inconsistent HCL |
| Validate | `terraform validate` | Invalid references, wrong types (after `init`) |
| Static analysis | `tflint` | Provider-aware smells, deprecated arguments, naming |
| Module tests | `terraform test` | Behavioural contracts via plan/apply + asserts |
| Integration | Terratest (Go) | End-to-end checks against real APIs |
| Policy | OPA / Conftest / Sentinel | Organisational must-not rules on plan JSON |

**`terraform fmt`** rewrites Hashi Configuration Language (HCL) to canonical style; CI uses `-check` so unformatted files fail the build. **`terraform validate`** needs providers installed — always run `terraform init` first (often `init -backend=false` in CI when state is not required). **`terraform test`** uses `*.tftest.hcl` files with `run` blocks (`command = plan` or `apply`) and `assert` conditions on outputs or plan attributes.

**Terratest** is a Go library for richer integration suites — spin real cloud resources, assert behaviour, tear down. **Policy validation** evaluates exported plan JSON; it complements module tests rather than replacing them.

### Why it matters

A typo in a module output or a removed variable breaks every consumer at apply time — expensive and stressful. Pipelines that format, validate, lint, and test convert Terraform changes into predictable signals reviewers trust. Static analysis catches classes of mistakes `validate` ignores (for example deprecated Amazon Web Services (AWS) resource arguments). Together these gates reduce mean time to detect packaging defects and protect remote state from merges that would destroy production.

### How it works

Recommended gate order in CI:

1. `terraform fmt -check -recursive`
2. `terraform init -backend=false` then `terraform validate` in each root/module directory
3. `tflint --recursive` (with provider plugins configured)
4. `terraform test` in module directories — asserts on outputs and planned values
5. Optional Terratest job against a sandbox account with strict cleanup
6. Policy check on `terraform show -json plan.tfplan` before apply approval

Treat plan JSON and failed assert messages as first-class review surfaces — reviewers skim destroys, replacements, and test failures the same way they review application tests.

### Key concepts and comparisons

| Layer | Needs cloud credentials? | Typical CI stage |
|-------|---------------------------|------------------|
| `fmt` / `validate` | No (after provider download) | Every PR |
| `tflint` | No | Every PR |
| `terraform test` (Docker/kind) | No | Every PR |
| `terraform test` (real resources) | Often yes | Nightly / pre-release |
| Terratest | Yes (sandbox) | Nightly |
| Policy on plan | Depends on plan source | Before apply |

| Tool | Language | Best for |
|------|----------|----------|
| `terraform test` | HCL | Module contract tests, fast feedback |
| Terratest | Go | Cross-stack integration, cloud smoke tests |
| Conftest / OPA | Rego | Custom policy on plan JSON |
| Sentinel | Sentinel | HCP Terraform / Enterprise policy sets |

### Policy validation

**Policy as code** on plans enforces rules tests may not cover globally — for example “no `0.0.0.0/0` ingress”, “required `Environment` tag”, “forbidden instance types”. Run after `terraform plan -out=tfplan` and evaluate `terraform show -json tfplan`. Module tests assert *your* contract; policy asserts *organisation* rules.

### Common pitfalls

- Relying only on `fmt` — formatting never proved a module correct.
- Running `validate` before `init` — schema checks need provider schemas.
- Assuming `terraform test` replaces policy — different scope and audience.
- Flaky Terratest against shared accounts without cleanup or state locking.
- Skipping lint for “tiny” variable renames that break downstream call sites.

## Hands-on Lab

### Objective

Build a reusable **Docker label** module, gate it with `fmt` and `validate`, and prove behaviour with a real `terraform test` suite that **applies containers** — not null stubs — under `~/rebash-terraform/module-14`.

### Prerequisites

- Terraform CLI ≥ 1.9
- Docker Engine running (`docker info` succeeds)

### Lab environment

Workspace: `~/rebash-terraform/module-14`

```bash
mkdir -p ~/rebash-terraform/module-14/modules/label && cd ~/rebash-terraform/module-14
```

### Real-world scenario

Your platform team publishes an internal `label` module that standardises container naming and tags. Before merging, CI must prove formatting, validation, and output contracts — including failure when an invalid environment is supplied — with tests that actually create Docker resources.

### Step-by-step tasks

#### Task 1 – Create the Docker label module

Create `modules/label/versions.tf`:

```hcl
terraform {
  required_version = ">= 1.9.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}
```

Create `modules/label/variables.tf`:

```hcl
variable "name" {
  type        = string
  description = "Base resource name."
}

variable "environment" {
  type        = string
  description = "Environment segment embedded in the label."

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging, or prod."
  }
}

variable "image" {
  type        = string
  description = "Container image to run."
  default     = "nginx:1.27-alpine"
}
```

Create `modules/label/main.tf`:

```hcl
locals {
  standard_label = "${var.name}-${var.environment}"
}

resource "docker_image" "labelled" {
  name         = var.image
  keep_locally = true
}

resource "docker_container" "labelled" {
  name  = local.standard_label
  image = docker_image.labelled.image_id

  labels = {
    standard_label = local.standard_label
    environment    = var.environment
    managed_by     = "terraform"
  }
}
```

Create `modules/label/outputs.tf`:

```hcl
output "standard_label" {
  description = "Normalised name-environment label."
  value       = local.standard_label
}

output "container_id" {
  description = "Running container ID."
  value       = docker_container.labelled.id
}

output "container_name" {
  description = "Running container name."
  value       = docker_container.labelled.name
}
```

Format and validate the module:

```bash
cd ~/rebash-terraform/module-14/modules/label
terraform fmt -recursive
terraform init -backend=false | tee ../../artefacts/init-label.log
terraform validate | tee ../../artefacts/validate-label.log
```

**Expected output:** `validate-label.log` contains `Success! The configuration is valid.`

#### Task 2 – Author native Terraform tests with real apply

Create `modules/label/tests/label.tftest.hcl`:

```hcl
variables {
  name        = "api"
  environment = "dev"
}

run "plan_ok" {
  command = plan

  assert {
    condition     = output.standard_label == "api-dev"
    error_message = "standard_label must combine name and environment."
  }
}

run "apply_ok" {
  command = apply

  assert {
    condition     = docker_container.labelled.name == "api-dev"
    error_message = "applied container name must match standard_label."
  }

  assert {
    condition     = docker_container.labelled.labels.standard_label == "api-dev"
    error_message = "container label must match standard_label."
  }
}

run "invalid_environment_fails" {
  command = plan

  variables {
    environment = "qa"
  }

  expect_failures = [
    var.environment,
  ]
}
```

Run the test suite:

{% raw %}
```bash
mkdir -p ~/rebash-terraform/module-14/artefacts
cd ~/rebash-terraform/module-14/modules/label
terraform test | tee ../../artefacts/test-results.log
docker ps --filter "name=api-dev" --format '{{.Names}}' | tee ../../artefacts/test-container-ps.txt
grep -q 'api-dev' ../../artefacts/test-container-ps.txt
```
{% endraw %}

**Expected output:** Three test runs pass; `api-dev` container running after apply test.

#### Task 3 – Wire a root module and fmt-check gate

Create `versions.tf` at the lab root:

```hcl
terraform {
  required_version = ">= 1.9.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}
```

Create `providers.tf`:

```hcl
provider "docker" {}
```

Create `main.tf`:

```hcl
module "app_label" {
  source = "./modules/label"

  name        = "payments"
  environment = "staging"
}
```

Create `outputs.tf`:

```hcl
output "app_label" {
  value = module.app_label.standard_label
}

output "container_name" {
  value = module.app_label.container_name
}
```

Simulate CI format check and validate the root:

```bash
cd ~/rebash-terraform/module-14
terraform fmt -check -recursive | tee artefacts/fmt-check.log
terraform init -backend=false | tee artefacts/init-root.log
terraform validate | tee artefacts/validate-root.log
terraform plan -input=false | tee artefacts/plan-root.log
grep -q 'module.app_label.docker_container.labelled' artefacts/plan-root.log
```

**Expected output:** `fmt-check.log` is empty (exit 0); plan shows `payments-staging` container.

#### Task 4 – Author a CI gate script

Create `scripts/ci-gates.sh`:

{% raw %}
```bash
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

terraform fmt -check -recursive
terraform init -backend=false
terraform validate

cd modules/label
terraform init -backend=false
terraform validate
terraform test

docker ps --filter "name=api-dev" --format '{{.Names}}' | grep -q 'api-dev'
echo "ci-gates: OK"
```
{% endraw %}

Run it:

```bash
cd ~/rebash-terraform/module-14
chmod +x scripts/ci-gates.sh
./scripts/ci-gates.sh | tee artefacts/ci-gates.log
grep -q 'ci-gates: OK' artefacts/ci-gates.log
```

**Expected output:** `ci-gates.log` records fmt, validate, test success, and running test container.

### Validation steps

- [ ] `terraform fmt -check -recursive` passes at repo root
- [ ] `modules/label` validates after `init -backend=false`
- [ ] `terraform test` passes three runs including real `apply` with Docker
- [ ] Root module plan references the label module container
- [ ] `scripts/ci-gates.sh` exits 0 with operational container proof

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Module not installed` | Skipped init in module dir | Run `terraform init -backend=false` before validate/test |
| Test apply fails on Docker | Engine not running | Start Docker; verify `docker info` |
| `expect_failures` test fails | Validation not on variable | Add `validation` block to `var.environment` |
| Container name conflict | Prior test container left running | Run `terraform test -destroy`; remove orphans |

### Challenge exercise

Add a fourth test run `plan_prod` with `environment = "prod"` and an assert that `length(output.standard_label) > 5`. Extend `scripts/ci-gates.sh` to fail if `artefacts/test-results.log` is missing after test.

### Learning outcomes

- Created a Docker module with variable validation and standardised outputs
- Authored `*.tftest.hcl` with plan, **real apply**, and negative validation tests
- Simulated CI with `fmt -check`, `validate`, and a reusable gate script
- Proved test containers exist with `docker ps` after apply tests

### Cleanup

```bash
cd ~/rebash-terraform/module-14/modules/label
terraform test -destroy
cd ~/rebash-terraform/module-14
terraform destroy -auto-approve 2>/dev/null || true
docker rm -f api-dev payments-staging 2>/dev/null || true
rm -rf .terraform modules/label/.terraform artefacts
```

## Validation

- [ ] Lab completed under `~/rebash-terraform/module-14`
- [ ] You can explain what `validate` does not catch
- [ ] You ran real `terraform test`, not only plan manually
- [ ] You can name one production failure mode (skipped tests on module bump)

## Code Walkthrough

Production testing habits:

1. **Inspect module contracts** — read outputs and validation blocks before bumping module versions.
2. **Pin provider versions** — tests behave differently across provider major versions.
3. **Capture evidence** — archive `terraform test` JSON/log output in CI artefacts.
4. **Prefer fast native tests** — reserve Terratest for integration paths native tests cannot cover.
5. **Fail closed** — a red test blocks merge; no “apply anyway” for prod.

## Security Considerations

- Test fixtures must not contain real API keys — use Docker or kind in PR gates with placeholder secrets only.
- Terratest jobs need sandbox accounts with cleanup — never reuse production credentials.
- Plan JSON uploaded from tests may include sensitive attributes — restrict artefact retention.
- Do not disable validation to “ unblock ” a release — fix or revert the module.
- Pin tflint rulesets to prevent silently ignored security rules on upgrade.

## Common Mistakes

!!! warning "Running validate without init"
    **Fix:** Always `terraform init -backend=false` in CI before validate and test.

!!! warning "Treating fmt success as test success"
    **Fix:** fmt is hygiene; behavioural asserts live in `terraform test` or Terratest.

!!! warning "Integration tests in every PR against production accounts"
    **Fix:** Scope cloud integration to nightly sandboxes; keep PR gates offline-friendly.

## Best Practices

- Colocate `tests/*.tftest.hcl` inside each published module.
- Run `terraform fmt -check` before validate to keep diffs readable.
- Assert on outputs and critical resource attributes, not entire plans.
- Version-pin tflint AWS/Azure/Google plugins alongside provider pins.
- Export plan JSON for policy only after module tests pass.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Test cannot find module | Wrong working directory | Run tests from module root; check `source` paths |
| Assert on output fails after apply | Output not refreshed | Use `command = apply` run block before output assert |
| tflint false positive | Rule too strict for wrapper module | Document exception or adjust rule in `.tflint.hcl` |
| Terratest timeout | Cloud API slow / quota | Increase timeout; use smaller fixture resources |
| Policy pass but test fail | Different scopes | Fix module contract first; policy is not a unit test |

## Summary

Gate Terraform changes with fmt, validate, lint, native tests, optional Terratest, and policy on plans — fastest checks first. The lab proved a real `terraform test` suite on a label module without cloud credentials. Next, apply a **security baseline** for secrets, state, and IAM.

## Interview Questions

**1. What does `terraform fmt` guarantee?**

??? success "Reveal answer"
    Canonical HCL formatting and consistent style. It does **not** guarantee correctness, security, or that resources will deploy successfully — only readable, standardised syntax.

**2. How does `terraform test` differ from running plan in CI alone?**

??? success "Reveal answer"
    `terraform test` executes declarative `run` blocks with `assert` and `expect_failures`, catching behavioural regressions (wrong outputs, broken validation) that a green plan might miss if nobody inspects values closely.

**3. What belongs in a minimal module test file?**

??? success "Reveal answer"
    At least one successful plan or apply run with asserts on key outputs, plus a negative case (`expect_failures`) for validation or preconditions. Keep tests focused on the module contract, not entire organisation policy.

**4. Why should format and validate gate merges before Terratest?**

??? success "Reveal answer"
    They are fast, credential-free, and catch syntax errors early. Terratest is slower, costlier, and belongs later in the pipeline or on a schedule — not as the first line of defence.

**5. What cannot `validate` catch that plan still might reveal?**

??? success "Reveal answer"
    Provider-side constraints, quota limits, dependency cycles at apply time, and real-world API errors. Validate checks internal consistency of configuration, not live cloud acceptance.

**6. When is Terratest worth the maintenance cost?**

??? success "Reveal answer"
    When you need cross-resource integration proof (network + compute + IAM) that native tests cannot simulate, and you have an isolated sandbox with automated teardown. Not for every module output check.

**7. Where does policy validation sit relative to `terraform test`?**

??? success "Reveal answer"
    After a plan exists and module tests pass. Policy enforces organisation-wide rules on plan JSON; module tests enforce the module author's contract. Both should pass before apply approval.

## Related Tutorials

- [Course overview](index.md)
- [Terraform Cloud and HCP Terraform](terraform-cloud-and-hcp-terraform.md)
- [Terraform Security and Secrets](terraform-security-and-secrets.md)

## References

- [terraform test](https://developer.hashicorp.com/terraform/language/tests)
- [terraform validate](https://developer.hashicorp.com/terraform/cli/commands/validate)
- [terraform fmt](https://developer.hashicorp.com/terraform/cli/commands/fmt)
- [tflint](https://github.com/terraform-linters/tflint)
- [Terratest](https://terratest.gruntwork.io/)
