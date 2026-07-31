---
title: "Introduction to Terraform and Infrastructure as Code"
description: "Understand Infrastructure as Code, declarative vs imperative approaches, why teams choose Terraform, and the core workflow architecture."
difficulty: beginner
estimated_time: "30–45 min"
technology: terraform
category: terraform
module: "Module 1 · IaC Fundamentals"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - infrastructure-as-code
prerequisites:
  - linux/index
  - git/index
next:
  - terraform/installing-terraform-and-the-cli-workflow
related:
  - terraform/terraform-state-fundamentals
  - docker/introduction-to-docker
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - iac
  - infrastructure-as-code
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Introduction to Terraform and Infrastructure as Code

## Overview



Explain what Infrastructure as Code (IaC) solves, contrast imperative and declarative models, and outline Terraform’s write → plan → apply workflow and architecture mental model.

**Infrastructure as Code** treats infrastructure the same way we treat application code: versioned files, peer review, and repeatable applies. **Terraform** is a declarative IaC tool — you describe the desired end state in HashiCorp Configuration Language (HCL); Terraform computes a plan and calls provider APIs to create, update, or destroy real resources.

This course is **Terraform for Cloud & DevOps Engineers** — production IaC, not toy demos.

This is a core tutorial in **Module 1 · IaC Fundamentals** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Linux](../linux/index.md) — comfortable terminal and file editing
- [Git](../git/index.md) — commits and pull requests (helpful)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Define Infrastructure as Code and why it beats click-ops  
- [ ] Contrast imperative scripts vs declarative desired state  
- [ ] Name why teams choose Terraform for multi-cloud ops  
- [ ] Sketch write → init → plan → apply → state



## Architecture



This topic’s control points and relationships are shown below.

![Terraform workflow](../assets/excalidraw/terraform-workflow.svg)



## Theory



### What it is

**Infrastructure as Code (IaC)** means describing networks, compute, identity, and platforms in files that live in Git — not in console click trails. An **imperative** approach lists steps (“create VPC, then subnet, then route”). A **declarative** approach states the end state (“these resources should exist with these attributes”); the tool works out create, update, or delete.

**Terraform** is HashiCorp’s declarative IaC engine. You write `.tf` files; the CLI builds a dependency graph, shows a **plan**, and **applies** changes through **providers** (plugins for AWS, Azure, Google Cloud, Kubernetes, local files, and more). **State** maps configuration addresses to real object IDs so Terraform can update and destroy safely later.

### Why it matters

Manual infrastructure fails at scale: environments drift, disaster recovery depends on tribal knowledge, and pull requests cannot review a console click. Terraform makes changes **reviewable** (`terraform plan` in CI), **repeatable** (same modules, different variables), and **auditable** (Git history plus state). Platform and SRE teams standardise landing zones and shared modules so product squads do not reinvent VPCs and IAM from scratch.

### How it works

Architecture mental model: **HCL configuration → Terraform CLI → state → providers → real infrastructure**.

1. You write desired state in HCL (resources, variables, outputs).
2. `terraform init` downloads providers and prepares the working directory.
3. `terraform plan` compares configuration to state and produces a change set.
4. `terraform apply` executes that plan via provider APIs.
5. State records what Terraform manages so the next plan is accurate.

You will install the CLI and run this loop in the next modules. For now, own the mental model.

### Key concepts and comparisons

| Approach | You specify | Tool responsibility |
|----------|-------------|---------------------|
| Imperative (scripts, click-ops) | Ordered steps | You sequence every create/update |
| Declarative (Terraform) | Desired end state | Plan/apply computes the delta |

| Pain without IaC | Terraform answer |
|------------------|------------------|
| Environment parity guesses | Same modules, different tfvars |
| Unreviewed production changes | Plan in pull request / pipeline |
| Rebuild from memory after outage | Re-apply from Git |

### Common pitfalls

- IaC does not remove architecture skill — it makes architecture reviewable.
- Terraform is not a cloud; providers talk to clouds and other APIs.
- A plan is not a guarantee forever — state drift and out-of-band console edits still matter.
- “Declarative” does not mean “no order”; Terraform’s graph still sequences dependent creates.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-terraform/module-01 && cd ~/rebash-terraform/module-01
```

**Focus:** Apply your first Terraform configuration with local and null providers

### Step 1 – Write a minimal configuration

```bash
cat > main.tf <<'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

resource "null_resource" "lab" {
  triggers = {
    note = "rebash-lab"
  }
}

resource "local_file" "marker" {
  content  = "managed-by-terraform
"
  filename = "${path.module}/marker.txt"
}
EOF
terraform init
terraform plan
```

### Step 2 – Apply and inspect state

```bash
terraform apply -auto-approve
terraform state list
cat marker.txt
terraform show | head -n 40
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-terraform/module-01/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Introduction to Terraform and Infrastructure as Code** always combines:

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



!!! warning "IaC does not remove architecture skill — it makes architecture reviewable."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Terraform is not a cloud; providers talk to clouds and other APIs."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Introduction to Terraform and Infrastructure as Code changes as code and review them in pull requests
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



**Introduction to Terraform and Infrastructure as Code** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. What problem does Infrastructure as Code solve compared with ClickOps?
2. What does Terraform’s desired-state model mean in practice?
3. What is the role of providers in Terraform?
4. What risks remain even when infrastructure is coded?
5. How does Terraform differ conceptually from a pure configuration management tool?

!!! tip "Sample answer — question 2"
    You declare the end state; Terraform plans creates/updates/deletes to converge. Re-running apply should move reality toward the configuration rather than blindly re-running imperative scripts.

!!! tip "Sample answer — question 4"
    IaC can still destroy production if plans are unreviewed, state is corrupt, or credentials are overly broad. Code review, policy checks, and least-privilege credentials remain essential.



## Related Tutorials



- [Course overview](index.md)
- [Installing Terraform and the CLI Workflow](installing-terraform-and-the-cli-workflow.md)



## References



- [What is Terraform?](https://developer.hashicorp.com/terraform/intro)  
- [Infrastructure as Code](https://developer.hashicorp.com/terraform/intro#infrastructure-as-code)
