---
title: "Troubleshooting Terraform"
description: "Diagnose provider errors, state corruption, dependency cycles, auth failures, drift, locking, and performance — with import, state rm, and moved as recovery tools."
difficulty: advanced
estimated_time: "45–60 min"
technology: terraform
category: terraform
module: "Module 20 · Troubleshooting"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - troubleshooting
prerequisites:
  - terraform/production-terraform-patterns
next:
  - terraform/index
related:
  - terraform/format-validate-and-terraform-test
  - terraform/terraform-state-fundamentals
  - terraform/remote-state-and-backends
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - troubleshooting
  - state
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Troubleshooting Terraform

## Overview







Diagnose common Terraform failures with a fixed order: auth → init/providers → validate/plan → state/lock → drift → graph/performance — using `import`, `state rm`, and `moved` only as deliberate recovery tools.

Most “Terraform is broken” tickets are credentials, provider version skew, state lock contention, or drift from console edits. Separate **configuration** failures from **state** failures from **provider API** failures before changing random flags.

This is a core tutorial in **Module 20 · Troubleshooting** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Production Terraform Patterns](production-terraform-patterns.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Classify provider, auth, state, and graph errors  
- [ ] Clear or wait on state locks safely  
- [ ] Detect and reconcile drift  
- [ ] Use `import`, `state rm`, and `moved` as recovery — not routine hacks  
- [ ] Spot dependency cycles and slow plans

## Architecture







This topic’s control points and relationships are shown below.

![Terraform troubleshooting](../assets/excalidraw/terraform-troubleshooting.svg)

## Theory







### What it is

**Troubleshooting Terraform** is a disciplined split between layers:

| Symptom | First checks |
|---------|----------------|
| Auth / 401 / 403 | Credentials, OIDC, IAM, subscription/project |
| Provider download / schema | `init`, version pins, registry access |
| Validate / reference errors | Typos, wrong module outputs, type mismatches |
| State lock | Who holds the lock; CI overlap; crash mid-apply |
| Drift | Console changes; `refresh`/`plan` unexpected updates |
| Cycle errors | Mutual `depends_on` or references |
| Slow plans | Huge roots, remote data sources, chatty APIs |
| State corruption / object missing | Backend restore; `state` subcommands carefully |

Recovery tools: **`terraform import`** adopts an existing object; **`terraform state rm`** drops an address without destroying; **`moved`** renames addresses across refactors. All require plan review and backups (`state pull`) first.

### Why it matters

Mean time to recovery depends on not confusing a bad variable with a bad backend. Platform on-call needs a fixed order juniors can follow under pressure. The same playbook feeds CI: catch validate/provider issues before apply, and treat force-unlock and state surgery as last resorts with audit notes.

### How it works

Use this order every time:

1. **Auth** — can the runner assume the role / use the subscription? Clock skew? Wrong account?  
2. **Init** — `terraform init` (upgrade only when intentional); confirm provider versions.  
3. **Validate / plan** — read the first error; fix config before touching state.  
4. **Lock** — if lock error, identify the holder; wait or `force-unlock` only when sure the other process is dead.  
5. **Drift** — unexpected updates/deletes → decide re-apply desired state vs update config to match reality.  
6. **Graph** — cycle messages → break mutual dependencies; prefer data flow over blanket `depends_on`.  
7. **State recovery** — restore backend version; then consider `import` / `state rm` / `moved` with a saved plan.  
8. **Performance** — split roots, cache providers, reduce refresh scope, avoid unbounded `for_each` over huge sets.

Separate questions: Does config parse? Does state match reality? Did the API reject the call?

### Key concepts and comparisons

| Failure class | Looks like | Not fixed by |
|---------------|------------|--------------|
| Auth | 403 / invalid token | Reformatting HCL |
| Config | Unknown resource / invalid ref | Force-unlock |
| Lock | state locked by … | Random `state rm` |
| Drift | perpetual plan changes | Ignoring and re-apply blind |
| Cycle | cycle: A, B | More `depends_on` both ways |
| API / provider | retryable 5xx or clear API error | Editing unrelated outputs |

| Recovery tool | Effect |
|---------------|--------|
| `import` | Bind real ID → address |
| `state rm` | Forget address (resource may still exist) |
| `moved` | Rename address without replace |
| Backend version restore | Roll back corrupted state object |

### Common pitfalls

- Jumping to `force-unlock` while another apply is healthy.  
- `state rm` then apply creating duplicates of critical databases.  
- Fixing production with console edits Terraform will fight forever.  
- Assuming `-refresh=false` “fixes” drift — it only hides it temporarily.  
- Expanding one root until plans take thirty minutes instead of splitting state.

## Hands-on Lab



### Objective

Run a complete Terraform workflow (init → plan → apply → prove → destroy) for **Troubleshooting Terraform** without paid cloud resources.

### Prerequisites

- Terraform CLI ≥ 1.5
- Network access to download the null provider once

### Lab environment

Workspace: `~/rebash-terraform/module-20`

Local Terraform only (`null`/`local` providers). No AWS/GCP/Azure credentials required.

```bash
mkdir -p ~/rebash-terraform/module-20 && cd ~/rebash-terraform/module-20
```

### Real-world scenario

You are automating **Troubleshooting Terraform** for a platform repo. Reviewers expect a clean plan artefact, applied evidence, and a destroy path before merge.

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







- [ ] Lab commands run under `~/rebash-terraform/module-20/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Troubleshooting Terraform** always combines:

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







!!! warning "Jumping to `force-unlock` while another apply is healthy.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "`state rm` then apply creating duplicates of critical databases.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Troubleshooting Terraform changes as code and review them in pull requests
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







You can test, secure, automate, multi-cloud, Kubernetes-bootstrap, and operate production Terraform — and troubleshoot failures by layer.

## Interview Questions






1. What are common causes of provider authentication errors?
2. How do you interpret a resource that must be replaced?
3. What does state inconsistency look like after a partial failure?
4. How can TF_LOG help, and what must you avoid when sharing logs?
5. When is `terraform refresh` / plan with refresh useful versus dangerous?

!!! tip "Sample answer — question 2"
    Replacement means Terraform cannot update in place—often from force-new arguments. Expect delete/create and plan for downtime or recreation side effects.

!!! tip "Sample answer — question 4"
    Debug logs may include secrets and tokens. Redact before sharing, and prefer targeted provider logs over dumping full environment variables.

## Related Tutorials







- [Course overview](index.md)
- [Course overview](index.md) · [Production Terraform Patterns](production-terraform-patterns.md) · [Format, Validate, and Terraform Test](format-validate-and-terraform-test.md)

## References







- [Debugging Terraform](https://developer.hashicorp.com/terraform/cli/commands#debugging-terraform) · [State CLI](https://developer.hashicorp.com/terraform/cli/commands/state) · [Import](https://developer.hashicorp.com/terraform/cli/import)
