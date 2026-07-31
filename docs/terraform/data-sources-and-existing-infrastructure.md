---
title: "Data Sources and Existing Infrastructure"
description: "Read existing infrastructure with Terraform data sources — remote lookups, external data patterns, and when not to manage what you only need to reference."
difficulty: intermediate
estimated_time: "45–60 min"
technology: terraform
category: terraform
module: "Module 11 · Data Sources"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - data-sources
prerequisites:
  - terraform/functions-templates-and-dynamic-blocks
next:
  - terraform/workspaces-and-environment-strategies
related:
  - terraform/resources-dependencies-and-meta-arguments
  - terraform/remote-state-and-backends
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - data-sources
  - existing-infrastructure
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Data Sources and Existing Infrastructure

## Overview

Use data sources to read existing objects, contrast them with managed resources, and practise remote / local lookup patterns without taking ownership of lifecycle.

**Data sources** read objects Terraform does not manage. They answer “what already exists?” during plan and refresh — AMI IDs, VPC IDs, shared DNS zones, files seeded outside the root. Pair them with resources that *you* own; do not use a data source as a substitute for managing something your stack should create and destroy.

This is a core tutorial in **Module 11 · Data Sources** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Functions, Templates, and Dynamic Blocks](functions-templates-and-dynamic-blocks.md)
- Terraform CLI 1.9+

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Contrast `resource` vs `data` addresses  
- [ ] Read local / remote existing infrastructure safely  
- [ ] Explain when `terraform_remote_state` or cloud lookups fit  
- [ ] Avoid managing objects you only meant to reference

## Architecture

This topic’s control points and relationships are shown below.

![Data sources](../assets/excalidraw/terraform-data-sources.svg)

## Theory

### What it is

A **data source** is a read-only lookup declared with a `data` block. Address form: `data.TYPE.NAME.ATTRIBUTE`. Providers implement data sources for cloud inventories (for example latest AMI, existing subnet by tag) and utility lookups (`local_file`, `http`, and similar). **Remote data** often means reading another team’s outputs via `terraform_remote_state` or querying shared cloud resources by filter. **External** patterns (for example the `external` provider) shell out to programmes that return JSON — powerful and easy to abuse; prefer native data sources when they exist.

### Why it matters

Real platforms are not greenfield. You attach workloads to an existing VPC, resolve a shared KMS key, or read a landing-zone output. Data sources keep those dependencies explicit in the graph: your apply waits until lookups succeed, and plans fail loudly when the shared object disappears. Misusing them — reading an object your root should own — causes split-brain: nobody knows who may destroy it, and drift becomes invisible to the “wrong” state file.

### How it works

1. Declare `data "local_file" "seed" { filename = ... }` (or a cloud data source with filters).
2. During plan/refresh, the provider reads the object and exposes attributes.
3. Resources reference `data.local_file.seed.content` — creating an implicit dependency edge.
4. Terraform does **not** create, update, or destroy the looked-up object when you destroy the root (unless a separate resource manages it).
5. For cross-stack contracts, prefer a few stable remote outputs or a data plane over deep remote-state webs.

Cloud filters must be unique or plans become non-deterministic. Pin AMI filters carefully unless you intend every new image to trigger churn.

### Key concepts and comparisons

| Construct | Lifecycle | Typical use |
|-----------|-----------|-------------|
| `resource` | Create / update / destroy | Objects you own |
| `data` | Read only | Shared / others’ objects |
| `terraform_remote_state` | Read outputs | Cross-stack contracts |

Prefer a data source for shared VPC/AMI/DNS you must not destroy; import when taking ownership; use tfvars when the value is config, not a live lookup.

### Common pitfalls

- Data source for something this root should manage — ownership confusion.
- Non-unique filters — plans pick different objects over time.
- Assuming destroy removes looked-up cloud objects — it does not.
- `external` programmes that are slow, non-hermetic, or secret-leaky in CI.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-terraform/module-11/data-sources/{seed,out} && cd ~/rebash-terraform/module-11/data-sources/{seed,out}
```

**Focus:** hands-on practice for Data Sources and Existing Infrastructure

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-terraform/module-11/data-sources/{seed,out}
cd ~/rebash-terraform/module-11/data-sources

echo "existing-infra-seed" > seed/source.txt

cat > versions.tf << 'EOF'
terraform {
  required_version = ">= 1.9.0"
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.9" }
  }
}
EOF

cat > main.tf << 'EOF'
data "local_file" "seed" {
  filename = "${path.module}/seed/source.txt"
}

resource "local_file" "derived" {
  filename        = "${path.module}/out/derived.txt"
  content         = "from-data:${trimspace(data.local_file.seed.content)}\n"
  file_permission = "0644"
}

output "seed_content" {
  value = trimspace(data.local_file.seed.content)
}

output "derived_path" {
  value = local_file.derived.filename
}
EOF

terraform init -input=false
terraform apply -input=false -auto-approve
cat out/derived.txt
terraform state list
# Note: data.local_file.seed is read; destroy removes only local_file.derived
terraform destroy -input=false -auto-approve
test -f seed/source.txt && echo "seed preserved (not managed)"
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-terraform/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-terraform/module-11/data-sources/{seed,out}/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Data Sources and Existing Infrastructure** always combines:

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

!!! warning "Data source for something this root should manage — ownership confusion."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Non-unique filters — plans pick different objects over time."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Data Sources and Existing Infrastructure changes as code and review them in pull requests
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

**Data Sources and Existing Infrastructure** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Data Sources and Existing Infrastructure** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Workspaces and Environment Strategies](workspaces-and-environment-strategies.md)

## References

- [Data Sources](https://developer.hashicorp.com/terraform/language/data-sources)  
- [terraform_remote_state](https://developer.hashicorp.com/terraform/language/state/remote-state-data)  
- [hashicorp/local](https://registry.terraform.io/providers/hashicorp/local/latest)
