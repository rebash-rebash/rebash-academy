---
title: "Terraform Cloud and HCP Terraform"
description: "Operate HCP Terraform (Terraform Cloud) — workspaces, remote runs, teams, and policy guardrails for collaborative Infrastructure as Code."
difficulty: advanced
estimated_time: "50–70 min"
technology: terraform
category: terraform
module: "Module 13 · Terraform Cloud & Enterprise"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - hcp-terraform
  - remote-operations
prerequisites:
  - terraform/workspaces-and-environment-strategies
next:
  - terraform/format-validate-and-terraform-test
related:
  - terraform/remote-state-and-backends
  - terraform/terraform-security-and-secrets
  - terraform/terraform-in-ci-cd-pipelines
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - hcp-terraform
  - terraform-cloud
  - remote-execution
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Terraform Cloud and HCP Terraform

## Overview

Explain HCP Terraform (formerly Terraform Cloud) workspaces, remote runs, team access, and policy hooks — and sketch a `cloud` block workflow you can adopt when an organisation is ready.

**HCP Terraform** (HashiCorp Cloud Platform Terraform; historically **Terraform Cloud**) hosts state, runs plans/applies remotely, and adds collaboration features: teams, variable sets, VCS-driven runs, and policy enforcement. You trade operating your own state bucket for a managed control plane. Enterprise tiers add deeper governance; the mental model starts the same.

This is a core tutorial in **Module 13 · Terraform Cloud & Enterprise** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Workspaces and Environment Strategies](workspaces-and-environment-strategies.md)
- [Remote State and Backends](remote-state-and-backends.md)
- HashiCorp account optional for the conceptual lab (no paid org required)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Describe HCP Terraform workspaces vs CLI workspaces  
- [ ] Outline remote execution runs (plan / apply)  
- [ ] Map teams, variable sets, and policy stages  
- [ ] Contrast `cloud` block vs self-managed backends

## Architecture

This topic’s control points and relationships are shown below.

![HCP Terraform](../assets/excalidraw/terraform-cloud.svg)

## Theory

### What it is

An HCP Terraform **workspace** is a named managed environment: state, variables, run history, and optional VCS connection. A **run** is a remote plan and (if approved) apply executed on HashiCorp’s runners or agents. **Teams** grant organisation permissions; **variable sets** inject shared TF_VAR / env values; **policies** (Sentinel or OPA-based offerings depending on tier) gate applies. Configuration uses a `cloud` block (mutually exclusive with a `backend` block) to bind the local working directory to an organisation and workspace.

### Why it matters

Self-managed S3 + DynamoDB works, but someone must own IAM, versioning, lock hygiene, and CI runners that hold cloud credentials. HCP Terraform centralises remote execution so credentials can live in the platform, plans appear in a UI for review, and platform teams attach mandatory policies before apply. For regulated orgs, run history and team boundaries support audit stories that laptop applies cannot.

### How it works

1. Create an organisation and workspace (UI, API, or Terraform provider for TFE/HCP).
2. Add a `cloud` block with organisation and workspace name; run `terraform login` / `terraform init`.
3. `terraform plan` / `apply` may execute remotely depending on workspace execution mode (remote vs local).
4. VCS-driven workspaces plan on pull request and apply on merge when configured.
5. Policies evaluate on the plan; failing soft/hard gates block apply.
6. Teams and variable sets scope who can queue runs and which secrets are injected.

CLI workspaces are a thin state switch; HCP workspaces add permissions, history, and run tooling. Name workspaces per environment (`app-prod`) but still prefer account-level isolation for production blast radius.

### Key concepts and comparisons

| Concern | Self-managed backend | HCP Terraform |
|---------|----------------------|---------------|
| State / locks | You operate them | Managed |
| Execution | CI or laptop | Remote runners / agents |
| Policy | DIY (OPA, Conftest, …) | Integrated policy sets |

Workspace = state + runs + variables; run = remote plan/apply; variable sets share values; teams separate plan vs apply; policies gate applies.

### Common pitfalls

- Treating HCP workspaces as a substitute for separate cloud accounts.
- Mixing `cloud` and `backend` blocks in one root — invalid.
- Secrets in Git *and* variable sets — pick one controlled path.
- Local execution while assuming credentials never touch laptops.

## Hands-on Lab
Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-terraform/module-13/hcp-terraform && cd ~/rebash-terraform/module-13/hcp-terraform
```

**Focus:** local Terraform workflow for Terraform Cloud and HCP Terraform (no cloud spend)

### Step 1 – Minimal configuration

```bash
cat > main.tf << 'EOF'
terraform {
  required_version = ">= 1.5.0"
}

resource "null_resource" "lab" {
  triggers = {
    topic = "Terraform Cloud and HCP Terraform"
  }
  provisioner "local-exec" {
    command = "echo lab-ok"
  }
}
EOF
terraform init
terraform validate
terraform plan -out=tfplan
```

### Step 2 – Apply, inspect state, destroy

```bash
terraform apply -auto-approve tfplan
terraform state list
terraform show | sed -n '1,40p'
terraform destroy -auto-approve
```

### Final step – Cleanup note

```bash
rm -f tfplan
# Keep ~/rebash-terraform/ for later tutorials; never leave remote state unlocked
```

## Validation

- [ ] Lab commands run under `~/rebash-terraform/module-13/hcp-terraform/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Terraform Cloud and HCP Terraform** always combines:

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

!!! warning "Treating HCP workspaces as a substitute for separate cloud accounts."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Mixing `cloud` and `backend` blocks in one root — invalid."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Terraform Cloud and HCP Terraform changes as code and review them in pull requests
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

**Terraform Cloud and HCP Terraform** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Terraform Cloud and HCP Terraform** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Format, Validate, and Terraform Test](format-validate-and-terraform-test.md)

## References

- [HCP Terraform](https://developer.hashicorp.com/terraform/cloud-docs)  
- [Cloud block](https://developer.hashicorp.com/terraform/cli/cloud/settings)  
- [Runs](https://developer.hashicorp.com/terraform/cloud-docs/run/remote-operations)
