---
title: "Terraform State Fundamentals"
description: "Inspect local Terraform state safely — what it stores, state commands, security, and basic drift detection for Cloud and DevOps teams."
difficulty: intermediate
estimated_time: "45–60 min"
technology: terraform
category: terraform
module: "Module 8 · State Management"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - state
prerequisites:
  - terraform/variables-locals-and-outputs
next:
  - terraform/remote-state-and-backends
related:
  - terraform/troubleshooting-terraform
  - terraform/terraform-security-and-secrets
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - state
  - drift
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Terraform State Fundamentals

## Overview

Explain what Terraform state stores, inspect it with `state list` / `show` / `pull`, treat state as sensitive, and recognise basic drift in a plan.

**State** is Terraform’s memory: a mapping from configuration addresses to real-world IDs and attributes. Cloud APIs do not know you called something `local_file.tracked` — state binds that address to the object Terraform manages. Local state is fine for labs; teams need remote backends next.

This is a core tutorial in **Module 8 · State Management** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Variables, Locals, and Outputs](variables-locals-and-outputs.md)
- Terraform CLI 1.9+ (1.15.x recommended)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Describe what state stores and why it exists  
- [ ] Use `terraform state list`, `show`, and `pull` safely  
- [ ] Explain refresh and how drift appears in a plan  
- [ ] Never commit `*.tfstate*` to Git

## Architecture

This topic’s control points and relationships are shown below.

![Terraform state](../assets/excalidraw/terraform-state.svg)

## Theory

### What it is

Without state, Terraform would guess which real object corresponds to each address. State stores resource type and name, provider attribution, attributes returned by the provider (often including secrets), dependency hints for destroy order, and serial / lineage metadata. Git stores desired configuration; state stores the binding to reality.

Local backend files:

| File | Purpose |
|------|---------|
| `terraform.tfstate` | Current state for the default local backend |
| `terraform.tfstate.backup` | Previous successful write (best-effort recovery) |

Both are **sensitive**. Even `local_file` content lands in state.

### Why it matters

Every plan and apply depends on accurate state. Lost or corrupted state risks duplicate creates, orphaned cloud objects, or surprise destroys. Drift — someone editing a security group in the console — only surfaces when refresh compares reality to state and configuration. Treating state as a secret store (not a Git artefact) is a production hygiene baseline before remote backends and team workflows.

### How it works

1. After apply, the CLI writes state mapping each address to provider-tracked attributes.
2. The next plan typically **refreshes** — asks providers what objects look like now.
3. Terraform diffs refreshed attributes against configuration and proposes create / update / destroy / replace.
4. Inspect with `terraform state list`, `state show ADDRESS`, and `state pull` (full JSON — handle carefully).
5. Prefer `moved` blocks and import workflows over hand-editing JSON or casual `state rm` / `state mv`.

If you edit a managed file by hand, the next plan shows an update to restore desired content — that difference is **drift**. Decide: adopt the drift into config, or re-apply to enforce configuration as source of truth.

### Key concepts and comparisons

| Command | Use |
|---------|-----|
| `terraform state list` | Addresses currently tracked |
| `terraform state show ADDRESS` | Human-readable attributes |
| `terraform state pull` | Full JSON to stdout |
| `terraform state rm` / `mv` | Forget or rename — prefer `moved` / import in reviews |

| Drift source | Example |
|--------------|---------|
| Console / manual edit | Security group rule changed |
| Out-of-band automation | Another tool overwrote a file |
| Provider defaults | Remote API normalised a value |

### Common pitfalls

- Committing `*.tfstate*` — secret leak and merge conflicts.
- Hand-editing state JSON — corrupted serials, orphaned objects, unexpected destroys.
- Deleting state to “start clean” in shared envs — orphans in the cloud.
- Assuming local labs are harmless for Git — file content still sits in state.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-terraform/module-08/state-basics/out && cd ~/rebash-terraform/module-08/state-basics/out
```

**Focus:** hands-on practice for Terraform State Fundamentals

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Terraform State Fundamentals"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-terraform/module-08/state-basics/out
cd ~/rebash-terraform/module-08/state-basics

cat > versions.tf << 'EOF'
terraform {
  required_version = ">= 1.9.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.9"
    }
  }
}
EOF

cat > main.tf << 'EOF'
variable "payload" {
  type    = string
  default = "state-lab"
}

resource "local_file" "tracked" {
  filename        = "${path.module}/out/tracked.txt"
  content         = "${var.payload}\n"
  file_permission = "0644"
}

output "tracked_path" {
  value = local_file.tracked.filename
}
EOF

cat > .gitignore << 'EOF'
.terraform/
*.tfstate
*.tfstate.*
out/
EOF

terraform init -input=false
terraform apply -input=false -auto-approve
terraform state list
terraform state show local_file.tracked
echo "drifted-by-hand" > out/tracked.txt
terraform plan -input=false
terraform apply -input=false -auto-approve
terraform destroy -input=false -auto-approve
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-terraform/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-terraform/module-08/state-basics/out/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Terraform State Fundamentals** always combines:

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

!!! warning "Committing `*.tfstate*` — secret leak and merge conflicts."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Hand-editing state JSON — corrupted serials, orphaned objects, unexpected destroys."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Terraform State Fundamentals changes as code and review them in pull requests
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

**Terraform State Fundamentals** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Terraform State Fundamentals** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Remote State and Backends](remote-state-and-backends.md)

## References

- [State](https://developer.hashicorp.com/terraform/language/state)  
- [State Command](https://developer.hashicorp.com/terraform/cli/commands/state)  
- [Sensitive Data in State](https://developer.hashicorp.com/terraform/language/state/sensitive-data)
