---
title: "Registry Modules and Composition"
description: "Consume Terraform Registry modules with version constraints, compose roots, and decide when to wrap upstream modules for production."
difficulty: intermediate
estimated_time: "45–60 min"
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
  - registry
  - modules
prerequisites:
  - terraform/modules-creating-reusable-infrastructure
next:
  - terraform/functions-templates-and-dynamic-blocks
related:
  - terraform/format-validate-and-terraform-test
  - terraform/production-terraform-patterns
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - registry
  - composition
  - versioning
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Registry Modules and Composition

## Overview



Address Registry-style modules with version pins, compose multiple modules in one root, and decide when to wrap upstream versus call it directly.

The **Terraform Registry** distributes versioned modules the same way it distributes providers. Production roots pin `source` and `version`, read changelogs before upgrades, and wire outputs of one module into inputs of another. This lab stays local while mirroring Registry consumption patterns.

This is a core tutorial in **Module 9 · Modules** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Modules — Creating Reusable Infrastructure](modules-creating-reusable-infrastructure.md)
- Terraform CLI 1.9+



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Address Registry modules with version constraints  
- [ ] Compare local, Git, and Registry sources  
- [ ] Compose modules by wiring outputs to inputs  
- [ ] Decide when to wrap an upstream module



## Architecture



This topic’s control points and relationships are shown below.

![Module composition](../assets/excalidraw/terraform-modules.svg)



## Theory



### What it is

A Registry module address looks like `source = "terraform-aws-modules/vpc/aws"` with `version = "~> 5.0"` (example shape). Sources also include local paths, Git URLs with `?ref=`, and private registries. **Composition** means a root orchestrates several modules so network outputs feed application inputs without duplicating resource graphs. A **wrapper** (facade) module sits between a public module and many internal callers — you pin upstream once and expose a narrower, org-approved API.

### Why it matters

Unpinned modules are a supply-chain risk: a floating `latest` can change between plan and apply. Version constraints make upgrades intentional. Composition keeps blast radius clear — network team owns the VPC module contract; app teams consume subnet IDs. Wrappers encode company defaults (tags, logging, encryption) so product squads cannot accidentally deploy “raw” public modules with insecure knobs left open.

### How it works

1. Read the module’s docs: required inputs, outputs, provider versions, and known caveats.
2. Pin `source` + `version` (or Git `ref`) in the caller.
3. Pass only the inputs you understand; ignore optional knobs until needed.
4. Wire `module.network.subnet_ids` style outputs into the next module’s variables.
5. Upgrade by reading the changelog, widening the constraint carefully, and reviewing the plan for unexpected replaces.

Before adoption: maintained releases, sensible defaults, least-privilege examples, and fit with your landing zone. Review modules like application dependencies.

### Key concepts and comparisons

| Source | Pinning | Fit |
|--------|---------|-----|
| Local path | Directory / commit | Fast monorepo iteration |
| Git URL + `ref` | Tag or commit SHA | Private modules |
| Public / private Registry | `version` constraint | Shared / approved catalogue |

Call upstream directly when the API is stable and defaults fit; wrap when many callers need org defaults; write your own when upstream fights your platform model. Prefer `~> 1.2`-style constraints; pin tighter on critical paths.

### Common pitfalls

- Omitting `version` on Registry modules in production.
- Upgrading majors without reading breaking-change notes.
- Over-wrapping — a facade that re-exposes every upstream input.
- Treating community Registry modules as “official HashiCorp.”



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-terraform/module-09/registry-compose/{modules/label,modules/app,out} && cd ~/rebash-terraform/module-09/registry-compose/{modules/label,modules/app,out}
```

**Focus:** Compose multiple local modules as you would Registry modules

### Step 1 – Create two small modules and compose them

```bash
mkdir -p modules/network modules/app
cat > modules/network/main.tf <<'EOF'
resource "local_file" "net" {
  filename = "${path.root}/network.txt"
  content  = "cidr=10.0.0.0/16
"
}
output "net_file" { value = local_file.net.filename }
EOF
cat > modules/app/main.tf <<'EOF'
variable "network_file" { type = string }
resource "local_file" "app" {
  filename = "${path.root}/app.txt"
  content  = "uses:${var.network_file}
"
}
EOF
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
}
module "network" { source = "./modules/network" }
module "app" {
  source        = "./modules/app"
  network_file  = module.network.net_file
}
EOF
terraform init
```

### Step 2 – Apply composition and verify wiring

```bash
terraform apply -auto-approve
cat network.txt app.txt
terraform state list
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-terraform/module-09/registry-compose/{modules/label,modules/app,out}/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Registry Modules and Composition** always combines:

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



!!! warning "Omitting `version` on Registry modules in production."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Upgrading majors without reading breaking-change notes."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Registry Modules and Composition changes as code and review them in pull requests
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



**Registry Modules and Composition** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. What is the Terraform Registry used for?
2. Why pin module versions from the Registry?
3. How does composition of small modules differ from one giant module?
4. What supply-chain risks exist when consuming third-party modules?
5. How do you evaluate whether a Registry module is trustworthy?

!!! tip "Sample answer — question 2"
    Composition keeps networking, compute, and app layers separable and testable. Giant modules become hard to change and review.

!!! tip "Sample answer — question 4"
    Third-party modules can run unexpected resources or exfiltrate data via provisioners. Prefer verified sources, pinned versions, code review, and least-privilege credentials.



## Related Tutorials



- [Course overview](index.md)
- [Functions, Templates, and Dynamic Blocks](functions-templates-and-dynamic-blocks.md)



## References



- [Terraform Registry](https://registry.terraform.io/)  
- [Module Sources](https://developer.hashicorp.com/terraform/language/modules/sources)  
- [Publishing Modules](https://developer.hashicorp.com/terraform/registry/modules/publish)
