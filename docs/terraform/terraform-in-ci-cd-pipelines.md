---
title: "Terraform in CI/CD Pipelines"
description: "Run Terraform in GitHub Actions, GitLab CI, Azure DevOps, Jenkins, and Atlantis — automated plans, artefacts, and apply gates."
difficulty: advanced
estimated_time: "50–65 min"
technology: terraform
category: terraform
module: "Module 16 · CI/CD"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - cicd
  - github-actions
prerequisites:
  - terraform/terraform-security-and-secrets
next:
  - terraform/multi-cloud-terraform
related:
  - terraform/format-validate-and-terraform-test
  - terraform/remote-state-and-backends
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - cicd
  - github-actions
  - atlantis
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Terraform in CI/CD Pipelines

## Overview



Design PR plan and protected-branch apply pipelines with plan artefacts, least-privilege credentials, and optional Atlantis-style PR automation across common CI systems.

Production Terraform is applied by **pipelines**, not laptops. Pull requests run format, validate, test, and **plan**; protected branches or environments run **apply** of a reviewed plan with short-lived credentials. Store the binary plan as an artefact so apply executes exactly what was reviewed. Atlantis comments plans on pull requests for teams that prefer chatops-style workflows.

This is a core tutorial in **Module 16 · CI/CD** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Terraform Security and Secrets](terraform-security-and-secrets.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Separate PR plan from privileged apply  
- [ ] Use `TF_IN_AUTOMATION` and `-input=false`  
- [ ] Store and consume plan artefacts safely  
- [ ] Sketch GitHub Actions, GitLab CI, Azure DevOps, and Jenkins patterns  
- [ ] Explain when Atlantis fits



## Architecture



This topic’s control points and relationships are shown below.

![Terraform CI/CD pipeline](../assets/excalidraw/terraform-cicd-pipeline.svg)



## Theory



### What it is

**Terraform in CI/CD** means machines run the write → plan → apply loop with auditability. A typical design:

| Stage | Trigger | Privilege |
|-------|---------|-----------|
| fmt / validate / test / lint | Every PR | Low (often no cloud, or read-only) |
| `terraform plan -out=` | Every PR | Read / plan role |
| Review | Humans + policy | — |
| `terraform apply tfplan` | Main / protected env | Apply role |

**GitHub Actions**, **GitLab CI**, **Azure DevOps**, and **Jenkins** all host the same stages with different YAML or job DSLs. **Atlantis** is a pull-request automation server: comment `atlantis plan` / `atlantis apply`, lock projects, and keep plans next to the PR conversation.

Automation flags: `TF_IN_AUTOMATION=true` and `-input=false` keep jobs non-interactive. Pin Terraform versions (binary or Docker image) so CI matches local and HCP runners.

### Why it matters

Laptop apply bypasses review, uses personal credentials, and leaves no consistent audit trail. Pipelines enforce format/test gates, OIDC roles, state locking, and environment protections (required reviewers, wait timers). Plan artefacts prevent “plan yesterday, apply today’s different config” drift between review and merge.

### How it works

1. On PR: checkout → setup Terraform → `fmt -check` → `init` → `validate` → `test` / `tflint` → `plan -out=tfplan` → upload artefact (restricted retention) → optional policy on JSON.  
2. Comment or attach a human-readable plan summary for reviewers.  
3. On merge to the protected branch (or after environment approval): download the **same** plan artefact (or re-plan under strict controls) → `apply -input=false tfplan`.  
4. Credentials via OIDC to AWS/Azure/GCP; never long-lived keys in repository variables if avoidable.  
5. Atlantis alternative: webhook from VCS → Atlantis runs plan/apply in its VPC with project `atlantis.yaml` configuration and concurrency locks.

Prefer apply-of-saved-plan for production; re-plan-on-main only when your change control explicitly allows it and locking prevents races.

### Key concepts and comparisons

| System | Strength | Watch-outs |
|--------|----------|------------|
| GitHub Actions | OIDC to clouds, environments | Protect plan artefacts; fork PR trust |
| GitLab CI | Environments, OIDC | Same artefact discipline |
| Azure DevOps | Enterprise gates | Service connections scope |
| Jenkins | Flexible agents | Credential sprawl if unmanaged |
| Atlantis | PR-native UX, locking | Host security; apply authz |

### Common pitfalls

- Applying from a fresh `plan` on main without tying to the reviewed PR plan.  
- Logging full plans that contain secret attribute values.  
- Using one static admin key for all environments.  
- Letting fork PRs run apply-capable workflows.  
- Skipping state locking so two pipelines apply concurrently.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-terraform/module-16/.github/workflows && cd ~/rebash-terraform/module-16/.github/workflows
```

**Focus:** Simulate a CI plan artefact workflow locally

### Step 1 – Produce a saved plan like CI would

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
terraform fmt -check || terraform fmt
terraform validate
terraform plan -input=false -out=tfplan
terraform show -no-color tfplan | head -n 40
```

### Step 2 – Apply the exact plan file (CI apply job pattern)

```bash
terraform apply -input=false tfplan
terraform state list
echo "In real CI: OIDC to cloud, remote state, plan on PR, apply on main"
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-terraform/module-16/.github/workflows/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Terraform in CI/CD Pipelines** always combines:

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



!!! warning "Applying from a fresh `plan` on main without tying to the reviewed PR plan.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Logging full plans that contain secret attribute values.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Terraform in CI/CD Pipelines changes as code and review them in pull requests
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



**Terraform in CI/CD Pipelines** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. What is a typical PR plan / merge apply pipeline shape?
2. Why apply a saved plan file rather than re-planning on apply?
3. How does OIDC improve cloud authentication from CI?
4. What blast-radius controls belong in Terraform pipelines?
5. How do you prevent unreviewed applies to production?

!!! tip "Sample answer — question 2"
    Re-planning at apply time can pick up drift or new provider behaviour that reviewers never saw. Applying the exact plan artefact preserves intent.

!!! tip "Sample answer — question 4"
    Use environment protections, required reviews, remote state locking, least-privilege roles, and separate prod pipelines with manual approval gates.



## Related Tutorials



- [Course overview](index.md)
- [Multi-Cloud Terraform](multi-cloud-terraform.md)



## References



- [Running Terraform in automation](https://developer.hashicorp.com/terraform/cli/run/automating-terraform) · [Atlantis](https://www.runatlantis.io/) · [setup-terraform](https://github.com/hashicorp/setup-terraform)
