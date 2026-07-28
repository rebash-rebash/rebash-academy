---
title: Registry Modules and Composition
description: "Consume Terraform Registry modules with version pins and compose them into a maintainable root."
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - registry
  - modules
prerequisites:
  - Completed Modules — Creating Reusable Infrastructure
comments: false
---

# Registry Modules and Composition

## Overview

The **Terraform Registry** distributes versioned modules the same way it distributes providers. Production roots pin `source` and `version`, read changelogs before upgrades, and compose modules so network outputs feed application inputs. This tutorial teaches Registry addresses, pinning, evaluation criteria, and composition patterns. The hands-on lab stays **local** (no AWS credentials) while mirroring how you would consume something like `terraform-aws-modules/vpc/aws` at version **6.6.1**.

This is **Tutorial 12** in **Module 3: Collaboration and Scale** of the REBASH Academy Terraform track.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Address Registry modules with version constraints
- [ ] Compare local, Git, and Registry sources
- [ ] Compose multiple modules in one root with output wiring
- [ ] Read module documentation before adoption
- [ ] Avoid unpinned module sources in production
- [ ] Decide when to wrap a public module behind an internal facade

## Prerequisites

- Completed [Modules — Creating Reusable Infrastructure](modules-creating-reusable-infrastructure.md)
- Terraform CLI **1.9+** (1.15.x recommended)
- Ability to create directories and edit files
- Network access only if you later try a real Registry download; the lab uses local sources
- No cloud account required for this lab

## Architecture

A root composes versioned building blocks. Each module has its own inputs/outputs; edges form when one module’s outputs feed another’s inputs.

![Architecture diagram for Registry Modules and Composition](../assets/images/terraform-registry.svg)

| Source kind | Example | Pin with |
|-------------|---------|----------|
| **Local** | `./modules/network` | Path in repo (version via Git) |
| **Registry** | `terraform-aws-modules/vpc/aws` | `version` argument |
| **Git** | `git::https://example.com/vpc.git?ref=v1.2.0` | `ref` query / tag |

## Theory

### Registry addressing

Public modules use `<NAMESPACE>/<NAME>/<PROVIDER>`:

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "6.6.1"

  name = "example"
  cidr = "10.0.0.0/16"
  # See module docs for required inputs (AZs, subnets, etc.)
}
```

As of this writing, latest `terraform-aws-modules/vpc/aws` is **6.6.1** — re-check the Registry before production pins. Do **not** apply the snippet above without AWS credentials and a reviewed plan.

### Why version pins matter

| Unpinned | Pinned |
|----------|--------|
| Next `init -upgrade` may jump majors | Reproducible plans across laptops and CI |
| Surprise breaking changes | Deliberate upgrade PRs with changelog review |

Prefer exact versions or carefully chosen pessimistic constraints for modules your team controls; many teams pin exact Registry versions and renovate intentionally.

### Evaluating a public module

Before adoption, check:

- Recent commits and open issues
- Terraform / provider version requirements
- Licence compatibility
- Whether examples match your region and compliance needs
- Provisioners or external scripts (supply-chain risk)
- Whether an official `hashicorp` / cloud-provider module exists instead

### Wrapper (facade) modules

When a public module’s API is broad or unstable for your org, wrap it:

```text
modules/company_vpc/   # your stable inputs
  main.tf              # calls terraform-aws-modules/vpc/aws with pinned version
```

Callers depend on `company_vpc` only. You upgrade the inner pin in one place.

### Composition patterns

| Pattern | Description |
|---------|-------------|
| **Network → app** | App module receives subnet IDs from network outputs |
| **Data → many** | Shared data module feeds multiple apps (careful coupling) |
| **Stack roots** | Thin roots per env compose the same modules with different tfvars |

Prefer **explicit outputs** over remote state spaghetti for sibling modules in the same root.

### Git sources

```hcl
module "internal" {
  source = "git::https://github.com/org/terraform-modules.git//network?ref=v1.4.0"
}
```

Use tags, not mutable branches, for production. Private Git needs CI credentials (SSH or HTTPS tokens) — prefer OIDC/short-lived tokens.

### Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| Public Registry module | Speed, community fixes | External dependency risk |
| Fully internal rewrite | Control | Maintenance burden |
| Wrapper module | Stable internal API | Extra layer |
| Many fine modules | Clear graphs | More wiring |

## Hands-on Lab

Scaffold **registry-style** local modules (`network` + `app`), compose them in a root, and compare the pin-and-compose pattern to a documented Registry call.

### Step 1 – Scaffold directories

**Objective:** Mirror a small internal module set.

```bash
mkdir -p ~/rebash-tf-reg/{modules/network,modules/app,generated}
cd ~/rebash-tf-reg
```

**Expected:** Three paths under `~/rebash-tf-reg`.

### Step 2 – Network module

**Objective:** Fake a VPC artefact with `local_file` outputs.

Create `modules/network/variables.tf`:

```hcl
variable "name" {
  description = "Logical network name"
  type        = string
}

variable "cidr" {
  description = "CIDR recorded in the lab artefact (not a real VPC)"
  type        = string

  validation {
    condition     = can(cidrnetmask(var.cidr))
    error_message = "cidr must be a valid IPv4 CIDR notation."
  }
}
```

Create `modules/network/main.tf`:

```hcl
resource "local_file" "vpc" {
  filename        = "${path.module}/../../generated/${var.name}-vpc.txt"
  content         = "vpc_name=${var.name}\ncidr=${var.cidr}\n"
  file_permission = "0644"
}

resource "terraform_data" "network_ready" {
  input = local_file.vpc.content_md5
}
```

Create `modules/network/outputs.tf`:

```hcl
output "vpc_id" {
  description = "Lab stand-in for a VPC identifier"
  value       = local_file.vpc.id
}

output "vpc_file" {
  description = "Path of the network artefact consumed by app modules"
  value       = local_file.vpc.filename
}

output "cidr" {
  description = "Echo of the configured CIDR"
  value       = var.cidr
}
```

**Expected:** Network module validates CIDR and exports `vpc_file`.

### Step 3 – App module

**Objective:** Depend on network outputs only — not on network internals.

Create `modules/app/variables.tf`:

```hcl
variable "name" {
  description = "Application name"
  type        = string
}

variable "vpc_file" {
  description = "Path to the network artefact from the network module"
  type        = string
}

variable "vpc_id" {
  description = "Network identifier from the network module"
  type        = string
}
```

Create `modules/app/main.tf`:

```hcl
resource "local_file" "app" {
  filename        = "${path.module}/../../generated/${var.name}-app.txt"
  content         = <<-EOT
    app=${var.name}
    vpc_id=${var.vpc_id}
    depends_on_vpc_file=${var.vpc_file}
  EOT
  file_permission = "0644"
}
```

Create `modules/app/outputs.tf`:

```hcl
output "app_file" {
  description = "Path of the application artefact"
  value       = local_file.app.filename
}
```

**Expected:** App module has no knowledge of how the network file was created.

### Step 4 – Root composition

**Objective:** Wire modules like a production root; document Registry pinning alongside.

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
module "network" {
  source = "./modules/network"
  name   = "payments"
  cidr   = "10.20.0.0/16"
}

module "app" {
  source  = "./modules/app"
  name    = "payments-api"
  vpc_file = module.network.vpc_file
  vpc_id   = module.network.vpc_id
}

output "artifacts" {
  description = "Composed artefact paths"
  value = {
    vpc = module.network.vpc_file
    app = module.app.app_file
    cidr = module.network.cidr
  }
}
```

Create `registry-example.tf.example` (not applied):

```hcl
# Example only — requires AWS credentials and full VPC inputs from the module README.
# module "vpc" {
#   source  = "terraform-aws-modules/vpc/aws"
#   version = "6.6.1"
#
#   name = "payments"
#   cidr = "10.20.0.0/16"
#   # azs, private_subnets, public_subnets, ...
# }
```

**Expected:** Root wires outputs → inputs; Registry example remains documentation.

### Step 5 – Apply and verify composition

**Objective:** Prove dependency order and artefacts.

```bash
terraform init -input=false
terraform plan -input=false -out=tfplan
terraform apply -input=false tfplan
cat generated/payments-vpc.txt generated/payments-api-app.txt
terraform output -json
```

**Expected:** Both files exist. App file references the VPC file path and id. Plan created `module.network` resources before `module.app` via implicit edges.

### Step 6 – Simulate a controlled “module upgrade”

**Objective:** Change network output content and see app update.

Edit `modules/network/main.tf` to add a `managed_by=terraform` line in `content`, then:

```bash
terraform apply -input=false -auto-approve
cat generated/payments-vpc.txt
cat generated/payments-api-app.txt
```

**Expected:** Network artefact changes; app may update because it embeds `vpc_file` path (same path) — if only VPC file content changes, app content might be unchanged unless it references checksums. Optionally pass `module.network.vpc_id` only; content drift in VPC file still shows composition ownership boundaries.

To force app refresh on network content changes, you could pass `content_md5` as an input — a good extension exercise.

### Step 7 – Clean up

**Objective:** Destroy and remove the lab tree.

```bash
terraform destroy -input=false -auto-approve
rm -f tfplan
cd ~
rm -rf ~/rebash-tf-reg
```

**Expected:** Generated files removed; directory gone.

## Code Walkthrough

### CIDR validation

`can(cidrnetmask(var.cidr))` rejects nonsense strings at plan time — the same class of guard you want on real network modules.

### Output wiring

```hcl
vpc_file = module.network.vpc_file
vpc_id   = module.network.vpc_id
```

This is the composition heart: **addresses stay inside modules**; only outputs cross the boundary. The same pattern applies when `module.network` is replaced by a pinned Registry VPC module — the app still receives subnet IDs/outputs.

### Registry example arguments

| Argument | Purpose |
|----------|---------|
| `source` | Registry address `terraform-aws-modules/vpc/aws` |
| `version` | Exact pin `6.6.1` for reproducibility |

Never omit `version` on Registry modules in production roots.

### Why local stand-ins

Downloading and applying a real VPC module needs credentials, cost, and cleanup. Local modules teach composition and pinning discipline without that overhead; swap `source`/`version` when you graduate to AWS labs.

## Validation

```bash
terraform fmt -recursive -check
terraform init -input=false
terraform validate
terraform apply -input=false -auto-approve
test -f generated/payments-vpc.txt
test -f generated/payments-api-app.txt
grep '10.20.0.0/16' generated/payments-vpc.txt
terraform state list | grep module.app
terraform destroy -input=false -auto-approve
```

| Check | Pass criteria |
|-------|----------------|
| validate | Success including CIDR validation |
| Composition | App artefact references network outputs |
| State | Addresses under `module.network` and `module.app` |
| Docs | `registry-example.tf.example` present with pinned version |
| Cleanup | Destroy removes managed files |

## Best Practices

- Always set `version` on Registry modules; review changelogs on upgrade PRs
- Prefer exact pins for third-party modules; automate upgrades with a bot and tests
- Wrap wide public APIs behind internal modules with company defaults (tags, encryption)
- Compose with outputs in the same root before reaching for remote state
- Vendor or mirror modules for air-gapped environments
- Run `terraform init -upgrade` only in dedicated upgrade branches
- Keep an allow-list of approved module sources for regulated environments
- Document why each external module was chosen (ticket / ADR)

## Security Considerations

- Treat module source as supply chain — pin, verify, and review diffs on upgrade
- Prefer HTTPS Git with verified tags; protect against tag move where possible
- Scan third-party modules for provisioners executing remote scripts
- Do not pass secrets as plain module inputs in CI logs; mark sensitive
- Least-privilege: a VPC module should not demand admin keys broader than needed
- Private Registry / HCP private modules for internal intellectual property

## Common Mistakes

!!! warning "`source` without `version` for Registry modules"
    Unexpected upgrades. **Fix:** Always pin; upgrade in reviewed PRs.

!!! warning "Copy-pasting Registry examples into prod unchanged"
    Wrong AZs, open CIDRs, missing flow logs. **Fix:** Read every input; align with your standards.

!!! warning "Deep remote_state instead of composition"
    Spaghetti coupling. **Fix:** Compose in one root or publish a thin data contract.

!!! warning "Pinning to a moving branch ref"
    Non-reproducible applies. **Fix:** Immutable tags / release versions.

## Troubleshooting

| Issue | Symptoms | Cause | Resolution |
|-------|----------|-------|------------|
| Could not download module | Init fails | Network / bad source | Check Registry URL and credentials |
| Version not found | Init error | Yanked or typo | Verify version on Registry |
| Circular module dependency | Cycle error | A↔B outputs | Introduce a third module or lift shared data |
| App missing network values | Empty inputs | Forgot to pass outputs | Wire `module.network.*` explicitly |
| Surprise resource churn on upgrade | Large replace plan | Module major change | Read upgrade guide; stage in non-prod |

## Interview Questions

1. How do you pin a Registry module version?
   *Set `version` on the `module` block to an exact or constrained release.*

2. What is the risk of source without a version?
   *Non-reproducible infrastructure and surprise breaking changes on init/upgrade.*

3. How do you evaluate a public module before adopting it?
   *Licence, maintenance signals, requirements, examples, and security posture.*

4. When should you wrap a Registry module in an internal module?
   *When you need a stable org API, forced defaults, or to absorb upstream churn.*

5. How do module outputs feed other modules?
   *Pass `module.a.out` into `module.b` input arguments — creating graph edges.*

6. What is the difference between count and for_each on modules?
   *for_each uses stable keys; count uses indices that shift — prefer for_each.*

7. How do you upgrade a module version in a controlled way?
   *Bump pin in a PR, plan in non-prod, read changelog, then promote.*

8. Where do you find module documentation?
   *Terraform Registry pages, linked GitHub README, and `examples/` folders.*

9. How do provisioners in third-party modules increase risk?
   *Arbitrary local/remote execution expands supply-chain and security review scope.*

10. What licence and maintenance signals matter?
    *Compatible licence, recent releases, responsive maintainers, clear ownership.*

11. How do you mirror modules for air-gapped use?
    *Private Registry, Git mirrors, or vendored copies with verified versions.*

12. Describe a composition pattern for network + app modules.
    *Network exports subnet/VPC IDs; app receives them as variables — single root apply.*

## Summary

- Pin Registry modules; treat them as supply-chain dependencies
- Compose through outputs in the root; wrap public modules when you need a stable internal API
- Local network+app labs teach the same wiring you will use with real VPC modules
- Upgrade deliberately with plans and changelogs — never rely on floating sources

## Related Tutorials

- Track overview: [Terraform](index.md)
- Previous: [Modules — Creating Reusable Infrastructure](modules-creating-reusable-infrastructure.md)
- Next: [Meta-Arguments — count, for_each, and lifecycle](meta-arguments-count-for-each-and-lifecycle.md)
- Cheat sheet: [Terraform Cheat Sheet](../cheatsheets/terraform.md)
- Interview prep: [Terraform Interview Prep](../interview/terraform.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

1. [Terraform Registry](https://registry.terraform.io/)
2. [Module Sources](https://developer.hashicorp.com/terraform/language/modules/sources)
3. [Module Versions](https://developer.hashicorp.com/terraform/language/modules/syntax#version)
4. [Module Composition](https://developer.hashicorp.com/terraform/language/modules/develop/composition)
5. [terraform-aws-modules/vpc/aws](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest)
6. [Publishing Modules](https://developer.hashicorp.com/terraform/registry/modules/publish)
7. [hashicorp/local provider](https://registry.terraform.io/providers/hashicorp/local/latest)
