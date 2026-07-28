---
title: Policy as Code Overview
description: "Introduce policy-as-code guardrails for Terraform plans using Sentinel/OPA-style concepts without vendor lock-in thinking."
difficulty: advanced
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - policy
  - opa
prerequisites:
  - Completed Secrets and Sensitive Values
comments: false
---

# Policy as Code Overview

## Overview

Code review catches some mistakes; **policy as code** blocks whole classes of unsafe plans before apply — public security groups, unencrypted state buckets, forbidden destroys, missing tags. Place checks after `plan` and before `apply`: `fmt → validate → test → plan → **policy** → apply`.

This tutorial compares **OPA/Conftest** (fits any CI) with **HashiCorp Sentinel** (HCP Terraform / TFE), generates Terraform plan JSON, and walks a small Rego denial rule against `local_file` changes. You can complete the Terraform portions without OPA installed; evaluating Rego is optional but recommended.

This is **Tutorial 18** in **Module 5: Quality and Security** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain policy-as-code in the Terraform workflow
- [ ] Contrast OPA/Conftest with Sentinel
- [ ] Generate `terraform show -json` plan artefacts
- [ ] Write a basic Rego denial rule against resource changes
- [ ] Place policy checks in CI before apply

## Prerequisites

- Completed [Secrets and Sensitive Values](secrets-and-sensitive-values.md)
- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files
- Optional: [OPA](https://www.openpolicyagent.org/docs/latest/#running-opa) CLI for Rego evaluation
- No cloud account required

## Architecture

Policy engines evaluate a machine-readable plan. They do not replace IAM; they encode organisational guardrails as versioned code reviewed like any other module.

![Architecture diagram for Policy as Code Overview](../assets/images/terraform-policy.svg)

| Stage | Artefact | Gate |
|-------|----------|------|
| Plan | Binary `tfplan` | Human + machine |
| Show | `plan.json` | Policy input |
| Policy | Pass / fail + messages | Block apply on fail |
| Apply | Same binary plan | Only if policy passed |

## Theory

### Why policies exist

Humans miss patterns under time pressure. Policies encode:

- Security baselines (no `0.0.0.0/0` on SSH)
- Cost guards (instance size caps)
- Operational rules (required tags, forbidden destroys in prod)
- Compliance mappings (CIS-inspired controls)

Start narrow: a few **hard-mandatory** rules beat dozens of noisy advisories nobody reads.

### Engines

| Engine | Typical home | Language |
|--------|--------------|----------|
| OPA / Conftest | Any CI (GitHub Actions, GitLab, Jenkins) | Rego |
| Sentinel | HCP Terraform / Terraform Enterprise | Sentinel |
| Cloud-native (AWS SCP, Azure Policy) | Cloud control plane | Varies — complements Terraform policy |

OPA and Sentinel differ in language and hosting, not in **placement**: both should evaluate the proposed plan before apply.

### Plan JSON shape (essentials)

```bash
terraform plan -out=tfplan
terraform show -json tfplan > plan.json
```

Key path for many rules: `resource_changes[*]` with fields like `address`, `type`, `change.actions` (`create`, `update`, `delete`, `no-op`).

Protect `plan.json` — it may contain sensitive attribute values (see previous tutorial).

### Enforcement levels

| Mode | Behaviour |
|------|-----------|
| Advisory | Warn in PR; do not block |
| Soft mandatory | Block with break-glass override |
| Hard mandatory | Block with no override except policy change |

Use hard mandatory for irreversible risk (public data stores, destroy of state backends).

### Policies versus module defaults

| Tool | Best for |
|------|----------|
| Module defaults / validation | Making the right path easy |
| Policy as code | Stopping the wrong path at plan time |

Prefer good modules first; add policies for cross-cutting rules modules cannot guarantee.

### Practical mental model

1. Emit plan JSON in CI
2. Evaluate deny rules
3. Fail the job on deny
4. Only then allow apply of the **same** plan bytes

## Hands-on Lab

### Step 1 – Configuration directory

```bash
mkdir -p ~/rebash-tf-policy/policy && cd ~/rebash-tf-policy
terraform version
```

**Expected:** Terraform 1.9+.

### Step 2 – Write a small root module

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
resource "random_id" "stamp" {
  byte_length = 2
}

resource "local_file" "allow" {
  filename = "${path.module}/allow.txt"
  content  = "ok\nstamp=${random_id.stamp.hex}\n"
}

resource "terraform_data" "policy_lab" {
  input = {
    lesson = "policy-as-code-overview"
    stamp  = random_id.stamp.hex
  }
}

output "allow_path" {
  value = local_file.allow.filename
}
```

### Step 3 – Create and export plan JSON

```bash
terraform fmt
terraform init -input=false
terraform validate
terraform plan -input=false -out=tfplan
terraform show -json tfplan > plan.json
head -c 200 plan.json; echo
python3 -c 'import json; p=json.load(open("plan.json")); print([c["address"] for c in p.get("resource_changes",[])])'
```

**Expected:** `plan.json` is non-empty JSON; addresses include `local_file.allow`, `random_id.stamp`, and `terraform_data.policy_lab`. Create actions present on a fresh root.

### Step 4 – Example Rego policy

`policy/deny_deletes.rego`:

```rego
package terraform.policy

import future.keywords.if
import future.keywords.in

# Deny deleting local_file resources — lab stand-in for "protect durable data"
deny[msg] if {
  some rc in input.resource_changes
  rc.type == "local_file"
  "delete" in rc.change.actions
  msg := sprintf("deleting local_file %s is blocked by lab policy", [rc.address])
}

# Example tag-style rule using terraform_data marker presence (illustrative)
deny[msg] if {
  some rc in input.resource_changes
  rc.type == "terraform_data"
  rc.name == "policy_lab"
  rc.change.actions == ["delete"]
  msg := "terraform_data.policy_lab delete blocked in lab policy"
}
```

**Expected:** Policy package `terraform.policy` with `deny` rules keyed off `resource_changes`.

### Step 5 – Evaluate with OPA (optional)

```bash
# Install from https://www.openpolicyagent.org/docs/latest/#running-opa
opa eval --format pretty -i plan.json -d policy/ 'data.terraform.policy.deny'
```

**Expected:** Empty set (`[]`) for a create-only plan — allowed.

Apply, then create a destroy plan and re-check:

```bash
terraform apply -input=false -auto-approve
terraform plan -input=false -destroy -out=destroy.tfplan
terraform show -json destroy.tfplan > destroy.json
opa eval --format pretty -i destroy.json -d policy/ 'data.terraform.policy.deny'
```

**Expected:** Deny messages for `local_file.allow` (and possibly the `terraform_data` rule). In CI this exit would fail the job before apply.

Without OPA, open `destroy.json` and confirm `change.actions` includes `delete` for `local_file.allow` — that is the signal policies use.

### Step 6 – Conftest-style note

Conftest wraps OPA for directory-based policies:

```bash
# conftest test plan.json -p policy/
```

Same Rego ideas; different CLI UX. Pick one tool per organisation and standardise.

### Step 7 – Sentinel note

On HCP Terraform, Sentinel policies run against the same plan data using HashiCorp’s policy language and enforcement modes (advisory / soft / hard). The **pipeline placement** is identical: after plan, before apply. Teams often mirror critical Sentinel rules as OPA for repos that also run CLI workflows.

### Step 8 – Clean up

```bash
terraform destroy -input=false -auto-approve
rm -f tfplan destroy.tfplan plan.json destroy.json
```

**Expected:** Lab files removed; JSON artefacts deleted (they may contain sensitive data in real stacks).

## Code Walkthrough

### Plan JSON consumption

| Field | Use in policy |
|-------|----------------|
| `resource_changes[].address` | Human-readable target |
| `resource_changes[].type` | Match provider types (`local_file`, `aws_s3_bucket`) |
| `resource_changes[].change.actions` | `create` / `update` / `delete` / `replace` semantics |
| `resource_changes[].change.after` | Proposed attributes (handle absences carefully) |

### Rego `deny` set

Returning messages from `deny` is a common Conftest/OPA pattern: non-empty deny set means failure. Keep messages actionable — include the address and the rule name.

### Lab stand-ins

Blocking `local_file` deletes mimics protecting databases. In production, target high-risk types first (`aws_db_instance`, public SG rules, IAM `*` policies).

### `terraform_data.policy_lab`

Gives the plan a second resource type for richer examples without cloud APIs.

## Validation

```bash
terraform fmt -check
terraform init -input=false
terraform validate
terraform plan -input=false -out=tfplan
terraform show -json tfplan > plan.json
test -s plan.json
# optional: opa eval ... deny == []
```

| Check | Pass criteria |
|-------|----------------|
| Plan JSON | Non-empty, valid JSON with `resource_changes` |
| Create plan | Policy deny set empty (if OPA installed) |
| Destroy plan | Deny messages for protected deletes |
| Placement | You can explain where policy sits in CI |
| Cleanup | Destroy + delete JSON artefacts |

## Best Practices

- Version policies in Git next to or above infrastructure repos
- Test policies with fixture plan JSON (unit-test the rules)
- Prefer a small hard-mandatory set over noisy advisories
- Evaluate the **exact** plan artefact you will apply
- Document break-glass: who can change policies, how emergencies work
- Align module defaults with policies so engineers succeed on the first plan

## Security Considerations

- Plan JSON is sensitive — restrict artefact access and retention
- Policies that only warn do not reduce risk — enforce what matters
- Do not embed secrets inside policy unit-test fixtures
- Guard who can modify policy repos (CODEOWNERS + reviews)
- Remember IAM still matters: policy-as-code complements, not replaces, cloud permissions

## Common Mistakes

!!! warning "Policies only in a wiki"
    Unenforced. **Fix:** Execute in CI on every plan; make the check required.

!!! warning "Policy sprawl"
    Hundreds of low-value rules ignored by humans. **Fix:** Curate; measure false positives.

!!! warning "Evaluating a different plan than apply"
    Bypass. **Fix:** Apply the saved `tfplan` bytes that passed policy.

!!! warning "Blocking all deletes globally"
    Prevents legitimate teardown. **Fix:** Scope by workspace, resource type, or environment tags.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Empty `resource_changes` | Wrong JSON (`state` instead of plan) | Use `terraform show -json tfplan` after `plan -out` |
| OPA deny path wrong | Package/data query mismatch | Query `data.terraform.policy.deny` matching `package` |
| False positives on replace | Actions include delete+create | Match `["delete"]` carefully or handle replace explicitly |
| Policy not running in CI | Optional job / wrong path filter | Required check; trigger on `.tf` and `policy/**` |
| Sentinel vs OPA drift | Two sources of truth | Mirror critical rules or centralise on one engine per workflow |

## Interview Questions

1. What problem does policy as code solve?
   *It enforces organisational guardrails on planned changes automatically before apply.*

2. Where should policies run in a pipeline?
   *After plan (on plan JSON) and before apply of that same plan.*

3. What is the difference between advisory and hard-mandatory policy?
   *Advisory warns; hard-mandatory blocks apply until the plan or policy changes.*

4. Give examples of policies worth enforcing first.
   *No public open security groups, encryption required on data stores, deny unexpected destroys of stateful resources, required tags.*

5. How do policies relate to module defaults?
   *Defaults make good paths easy; policies stop bad paths that bypass modules.*

6. Why evaluate plans rather than only applied state?
   *Plans show intent before damage; state checks are lagging indicators.*

7. How do you test policies themselves?
   *Fixture plan JSON for allow/deny cases in CI alongside policy changes.*

8. What organisational ownership model works for policies?
   *A platform/security team owns the rule set; app teams request changes via PR with justification.*

9. How do exceptions get managed safely?
   *Time-bounded waivers, ticket links, and soft-mandatory with audited overrides — not silent disables.*

10. What is the relationship to CIS / Well-Architected ideas?
    *Policies can encode selected controls as automated checks mapped to those frameworks.*

11. How do you avoid policy sprawl?
    *Measure noise, delete low-value rules, and prefer module guardrails for local concerns.*

12. When is a policy the wrong tool versus a module default?
    *When every consumer should get the safe setting automatically — bake it into the module instead of denying after the fact.*

## Summary

- Policy as code evaluates plan JSON between plan and apply
- OPA/Conftest fits general CI; Sentinel fits HCP Terraform — placement is the same idea
- Start with a few hard-mandatory rules tied to real risk
- Protect plan artefacts; apply only plans that passed policy
- Combine with good modules, tests, and least-privilege IAM

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Secrets and Sensitive Values](secrets-and-sensitive-values.md)
- Next: [Terraform in CI/CD Pipelines](terraform-in-ci-cd-pipelines.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
2. [Inspecting a plan — JSON](https://developer.hashicorp.com/terraform/cli/commands/show)
3. [OPA documentation](https://www.openpolicyagent.org/docs/latest/)
4. [Conftest](https://www.conftest.dev/)
5. [Sentinel for Terraform](https://developer.hashicorp.com/sentinel)
6. [HCP Terraform policy enforcement](https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement)
7. [hashicorp/local provider](https://registry.terraform.io/providers/hashicorp/local/latest)
