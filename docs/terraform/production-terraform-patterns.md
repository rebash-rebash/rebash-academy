---
title: "Production Terraform Patterns"
description: "Ship production Terraform — repository layout, environment strategy, modules, versioning, upgrades, cost, DR, and safe import/moved refactors."
difficulty: advanced
estimated_time: "50–65 min"
technology: terraform
category: terraform
module: "Module 19 · Production Terraform"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - production-practices
prerequisites:
  - terraform/kubernetes-infrastructure-with-terraform
next:
  - terraform/troubleshooting-terraform
related:
  - terraform/modules-creating-reusable-infrastructure
  - terraform/workspaces-and-environment-strategies
  - terraform/remote-state-and-backends
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - best-practices
  - modules
  - disaster-recovery
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Production Terraform Patterns

## Overview







Apply production patterns for repository structure, environment blast radius, module strategy, provider/module versioning, upgrades, cost awareness, disaster recovery (DR), and brief import/`moved` discipline.

Production Terraform is boring on purpose: clear repo layout, one state per environment (or tighter), version-pinned modules, CI gates, encrypted remote state, and rehearsed recovery. Treat root modules as release units. Cost and DR are design inputs, not afterthoughts. Use `import` and `moved` for controlled refactors — not as daily firefighting.

This is a core tutorial in **Module 19 · Production Terraform** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Kubernetes Infrastructure with Terraform](kubernetes-infrastructure-with-terraform.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Sketch a production repo layout (modules vs live)  
- [ ] Choose env strategy by blast radius  
- [ ] Version modules and providers with constraints  
- [ ] Outline upgrade, cost, and DR habits  
- [ ] Recall when `import` / `moved` are appropriate

## Architecture







This topic’s control points and relationships are shown below.

![Repository structure](../assets/excalidraw/terraform-repo-structure.svg)

## Theory







### What it is

**Production Terraform patterns** are the engineering habits that keep IaC operable at scale:

| Practice | Outcome |
|----------|---------|
| `modules/` + `live/` (or `envs/`) | Reuse vs instantiation separated |
| State per env/account | Blast radius contained |
| Pinned `required_providers` / module `version` | Reproducible plans |
| CI fmt/validate/test/plan | Broken code never merges |
| Encrypted remote state + lock | Collaboration without corruption |
| DR runbooks | Rebuild from Git + state backup |
| `import` / `moved` | Adopt or rename without destroy |

A common layout: versioned child modules in one repo (or module registry), and thin **live** roots per environment that only call modules with tfvars. Workspaces are optional light isolation — many teams prefer separate directories and backends for production.

### Why it matters

Clever roots that only one author understands become outage multipliers. Enterprises need reviewable upgrades, predictable costs, and a path to recreate networking and platforms after account loss or ransomware. Treating Terraform releases as release engineering — changelog, version bump, plan review, apply window — aligns infrastructure with how you already ship applications.

### How it works

A practical production loop:

1. Change modules or live roots in a PR; CI runs fmt, validate, tests, and plan against the target backend (or a PR sandbox).  
2. Pin providers (`~>`) and Registry modules (`version = "x.y.z"`); read changelogs before major bumps.  
3. Promote: merge → apply via pipeline with environment protections.  
4. **Cost:** tag resources, prefer right-sizing and lifecycle rules in modules, review plan for expensive replaces (NAT, databases, clusters).  
5. **DR:** versioned state backends, cross-region replication where required, documented restore (`state pull` backups, recreate from Git). Separate DR roots if the secondary cloud/region differs.  
6. **Refactors:** `import` brings existing objects under management; `moved` blocks rename addresses without destroy/create. Both require careful plan review.

Upgrade strategy: bump in non-prod first, watch for forced replacements, keep Terraform CLI versions aligned across laptops, CI, and HCP.

### Key concepts and comparisons

| Env strategy | Pros | Cons |
|--------------|------|------|
| Dirs + separate state | Clear blast radius | More boilerplate |
| Workspaces | Less duplication | Easy to mis-select; weaker isolation |
| One mega-root | Fast start | Dangerous applies; huge plans |

| Tool | Role |
|------|------|
| `terraform import` | Adopt existing object into state |
| `moved` block | Rename address safely in modern Terraform |
| `state rm` | Stop managing without destroying (careful) |

### Common pitfalls

- One state file for all environments “for simplicity”.  
- Unpinned `main` module sources in production.  
- Upgrading providers only in prod.  
- Ignoring cost of replace until the invoice arrives.  
- Using `import` casually without documenting the object lifecycle.  
- Treating DR as “we have S3 versioning” without a restore rehearsal.

## Hands-on Lab



### Objective

Run a complete Terraform workflow (init → plan → apply → prove → destroy) for **Production Terraform Patterns** without paid cloud resources.

### Prerequisites

- Terraform CLI ≥ 1.5
- Network access to download the null provider once

### Lab environment

Workspace: `~/rebash-terraform/module-19/{modules/greeting,live/dev}`

Local Terraform only (`null`/`local` providers). No AWS/GCP/Azure credentials required.

```bash
mkdir -p ~/rebash-terraform/module-19/{modules/greeting,live/dev} && cd ~/rebash-terraform/module-19/{modules/greeting,live/dev}
```

### Real-world scenario

You are automating **Production Terraform Patterns** for a platform repo. Reviewers expect a clean plan artefact, applied evidence, and a destroy path before merge.

### Step-by-step tasks

#### Task 1 – Author and initialise configuration

Use local/null providers so the lab never bills a cloud account.

```bash
cat > versions.tf << 'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = { source = "hashicorp/null", version = "~> 3.2" }
  }
}
EOF
cat > main.tf << 'EOF'
resource "null_resource" "lab" {
  triggers = { topic = "rebash-lab" }
  provisioner "local-exec" {
    command = "echo applied > applied.txt"
  }
}
output "note" { value = null_resource.lab.triggers.topic }
EOF
terraform init
terraform validate
```

**Expected output:** `Terraform has been successfully initialized` and validate succeeds.

#### Task 2 – Plan, apply, and prove outputs

Treat the plan as the change ticket — review before apply.

```bash
terraform plan -out=tfplan
terraform show -no-color tfplan | tee plan.txt
terraform apply tfplan
terraform output
test -f applied.txt && cat applied.txt
```

**Expected output:** plan.txt shows create; `applied` written; output prints the note.

### Validation steps

- [ ] terraform validate passes
- [ ] Plan was saved and reviewed before apply
- [ ] Destroy completes with empty state (or resources removed)

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Provider not found | Missing init / network | Run `terraform init` again |
| State locked | Concurrent apply | Wait or coordinate; never force-unlock casually |
| Unexpected destroy in plan | Drift or wrong workspace | Read plan line-by-line before apply |

### Challenge exercise

Add an input variable with a validation block and fail the plan with an illegal value, then fix it.

### Learning outcomes

- Completed a reviewable plan/apply cycle
- Proved outputs/files exist
- Destroyed lab state

### Cleanup

```bash
terraform destroy -auto-approve
rm -rf .terraform tfplan 2>/dev/null || true
```

## Validation







- [ ] Lab commands run under `~/rebash-terraform/module-19/{modules/greeting,live/dev}/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Production Terraform Patterns** always combines:

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







!!! warning "One state file for all environments “for simplicity”.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Unpinned `main` module sources in production.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Production Terraform Patterns changes as code and review them in pull requests
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







**Production Terraform Patterns** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions






1. Which version pinning practices belong in production roots?
2. How do you structure repositories for many environments?
3. What review checklist items matter on every production plan?
4. How do you limit blast radius of a mistaken apply?
5. Why keep modules thin at the edge and shared modules versioned?

!!! tip "Sample answer — question 2"
    Check destroys, replacements, security group openings, and IAM changes carefully. Small unexpected deletes are common incident sources.

!!! tip "Sample answer — question 4"
    Separate states, guardrails on who can apply prod, prevent_destroy on critical data stores, and canary environments reduce blast radius.

## Related Tutorials







- [Course overview](index.md)
- [Troubleshooting Terraform](troubleshooting-terraform.md)

## References







- [Module composition](https://developer.hashicorp.com/terraform/language/modules/develop/composition) · [Refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring) · [State backends](https://developer.hashicorp.com/terraform/language/backend)
