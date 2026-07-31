---
title: "Modules — Creating Reusable Infrastructure"
description: "Build a Terraform child module with typed inputs and outputs, call it from a root, and design reusable local versioning for DevOps teams."
difficulty: intermediate
estimated_time: "50–70 min"
technology: terraform
category: terraform
module: "Module 9 · Modules"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - modules
prerequisites:
  - terraform/remote-state-and-backends
next:
  - terraform/registry-modules-and-composition
related:
  - terraform/variables-locals-and-outputs
  - terraform/format-validate-and-terraform-test
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - modules
  - reuse
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Modules — Creating Reusable Infrastructure

## Overview



Create a child module with typed variables and outputs, call it twice from a root, and apply a clear input/output contract without leaking internals.

**Modules** package reusable infrastructure patterns behind a typed API. Platform teams publish child modules; application roots call them without copying raw resource blocks. Local `source = "./modules/..."` is the composition skill before Registry modules.

This is a core tutorial in **Module 9 · Modules** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Remote State and Backends](remote-state-and-backends.md)
- Terraform CLI 1.9+



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Create a child module with variables, resources, and outputs  
- [ ] Call modules with a local `source`  
- [ ] Use `path.module` correctly inside children  
- [ ] Design small modules with stable contracts



## Architecture



This topic’s control points and relationships are shown below.

![Terraform modules](../assets/excalidraw/terraform-modules.svg)



## Theory



### What it is

A **module** is a directory of `.tf` files. The **root module** is where you run Terraform; **child modules** are called with a `module` block. Values enter through arguments (mapped to `variable` blocks) and exit through `output` blocks. Reference results as `module.NAME.output_name`. Providers are inherited from the root unless you pass an explicit `providers` map.

Typical child layout: `variables.tf`, `main.tf`, `outputs.tf`, optional `versions.tf` (`required_providers`), and a README. Prefer `path.module` for files the child owns; pass caller paths as inputs instead of hard-coded `../../` escapes.

### Why it matters

Copy-pasted VPC and IAM blocks drift across teams. Modules encode a reviewed pattern once — naming, tags, secure defaults — and roots supply environment-specific inputs. Clear contracts speed code review: reviewers check the module API, not every nested resource address. Local versioning (Git tags on a module repo, or a pinned subdirectory) lets you evolve internals without breaking every consumer on day one.

### How it works

1. Author the child with typed variables (descriptions, validation) and minimal outputs (IDs, names, ARNs — not every attribute).
2. From the root: `module "greeting" { source = "./modules/greeting" ... }`.
3. `terraform init` installs / links the module source; addresses become `module.greeting.local_file.this`.
4. Two `module` blocks with different inputs create two state namespaces — reuse without copy-paste.
5. Change behaviour inside the child; callers that only depend on outputs stay stable.

Design tips: one responsibility per module; sensible defaults for non-secret optionals; avoid mega-modules; declare `required_providers` so callers get clear version errors.

### Key concepts and comparisons

| Layer | Responsibility |
|-------|----------------|
| Root | Backend, providers, composition, env values |
| Child | One reusable pattern |
| Contract | Variables in, outputs out — hide resource addresses |

| Expression | Meaning |
|------------|---------|
| `path.module` | Directory of the **current** module |
| `path.root` | Directory of the root module |

Child module when reused; inline resources for one-offs; wrapper modules to soften a third-party Registry API.

### Common pitfalls

- Mega-modules with unreviewable blast radius.
- Leaking every resource as an output — callers couple to internals.
- Using relative `../` paths as the public API instead of input variables.
- Forgetting `required_providers` or a README with examples.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-terraform/module-09/create-modules/{modules/greeting,generated} && cd ~/rebash-terraform/module-09/create-modules/{modules/greeting,generated}
```

**Focus:** Build and call a local module

### Step 1 – Author a module and root module

```bash
mkdir -p modules/label
cat > modules/label/main.tf <<'EOF'
variable "name" { type = string }
resource "local_file" "out" {
  filename = "${path.root}/${var.name}.label"
  content  = "module-built:${var.name}
"
}
output "path" { value = local_file.out.filename }
EOF
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
}
module "app" {
  source = "./modules/label"
  name   = "checkout"
}
output "label_path" { value = module.app.path }
EOF
terraform init
```

### Step 2 – Apply and inspect module address in state

```bash
terraform apply -auto-approve
terraform state list
cat checkout.label
terraform output
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-terraform/module-09/create-modules/{modules/greeting,generated}/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Modules — Creating Reusable Infrastructure** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.



## Security Considerations



- Treat credentials and tokens for terraform as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces



## Common Mistakes



!!! warning "Mega-modules with unreviewable blast radius."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Leaking every resource as an output — callers couple to internals."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Modules — Creating Reusable Infrastructure changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible



## Troubleshooting



| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |



## Summary



**Modules — Creating Reusable Infrastructure** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. What problem do modules solve?
2. How do module inputs and outputs define a contract?
3. What should you avoid putting inside a general-purpose module?
4. How can a poorly versioned module create blast radius across many stacks?
5. What is the difference between a root module and a child module?

!!! tip "Sample answer — question 2"
    Variables declare required inputs; outputs expose selected results. A clear contract lets callers compose modules without reading every resource inside.

!!! tip "Sample answer — question 4"
    One module change can alter hundreds of workspaces. Version modules, changelog breaking changes, and roll out upgrades gradually with plans reviewed per environment.



## Related Tutorials



- [Course overview](index.md)
- [Registry Modules and Composition](registry-modules-and-composition.md)



## References



- [Modules Overview](https://developer.hashicorp.com/terraform/language/modules)  
- [Module Blocks](https://developer.hashicorp.com/terraform/language/modules/syntax)  
- [Module Composition](https://developer.hashicorp.com/terraform/language/modules/develop/composition)
