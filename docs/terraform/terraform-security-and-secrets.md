---
title: "Terraform Security and Secrets"
description: "Secure Terraform — sensitive variables, Vault/SSM patterns, IAM least privilege, state encryption, and policy as code (OPA/Sentinel)."
difficulty: intermediate
estimated_time: "45–60 min"
technology: terraform
category: terraform
module: "Module 15 · Security"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - security
  - secrets-management
  - policy-as-code
prerequisites:
  - terraform/format-validate-and-terraform-test
next:
  - terraform/terraform-in-ci-cd-pipelines
related:
  - terraform/remote-state-and-backends
  - terraform/troubleshooting-terraform
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - security
  - secrets
  - opa
  - sentinel
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Terraform Security and Secrets

## Overview

Apply a Terraform security baseline: no secrets in Git, marked sensitive outputs, Vault/SSM injection patterns, least-privilege IAM for runners, encrypted remote state, and policy-as-code gates.

Terraform configs often tempt teams to bake passwords into `terraform.tfvars`. Prefer external secret stores. Restrict who can plan and apply. Encrypt state at rest and treat plan artefacts as sensitive. Policy engines (Open Policy Agent / Sentinel) block unsafe changes before apply.

This is a core tutorial in **Module 15 · Security** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Format, Validate, and Terraform Test](format-validate-and-terraform-test.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] List secret anti-patterns in HCL and state  
- [ ] Mark variables/outputs `sensitive` and explain limits  
- [ ] Outline Vault, SSM Parameter Store, and Secrets Manager patterns  
- [ ] Describe IAM least privilege for CI apply roles  
- [ ] Explain state encryption and plan artefact handling  
- [ ] Summarise OPA vs Sentinel policy-as-code

## Architecture

This topic’s control points and relationships are shown below.

![Terraform security](../assets/excalidraw/terraform-security.svg)

## Theory

### What it is

**Terraform security** covers secrets handling, identity used for plan/apply, protection of **state** (which often contains secret attribute values), and **policy as code** that constrains what infrastructure may be created. Marking a variable `sensitive = true` redacts CLI output — it does **not** encrypt values in state. Real secrecy comes from external stores and access control.

| Concern | Secure default |
|---------|----------------|
| Secrets in Git | Never commit plaintext; use CI/OIDC + store |
| Sensitive attrs | `sensitive = true` on vars/outputs; still in state |
| Injection | data sources / ephemeral patterns from Vault, SSM, Secrets Manager |
| Identity | Short-lived OIDC roles; least privilege per root |
| State | Remote backend with encryption + tight IAM |
| Policy | OPA/Conftest or Sentinel on plan JSON |

**HashiCorp Vault**, **AWS Systems Manager (SSM) Parameter Store**, and **AWS Secrets Manager** (plus cloud analogues) are common sources. **Open Policy Agent (OPA)** evaluates Rego against plan JSON; **Sentinel** is HashiCorp’s policy language on HCP Terraform / Enterprise.

### Why it matters

State files and plan artefacts are a high-value target: they can hold database passwords, private keys, and IAM details. A compromised CI role with broad `*` permissions can recreate or destroy entire landing zones. DevSecOps treats Terraform like production code — provenance of modules, pinned providers, encrypted backends, and policy gates — because IaC is a privileged supply-chain and runtime control plane.

### How it works

1. **Secrets:** keep `.tf` / committed tfvars free of passwords; inject via environment variables, CI-masked inputs, or data sources that read Vault/SSM/Secrets Manager at plan/apply time. Prefer managed secret resources created once and referenced by ARN/ID.  
2. **Sensitive:** mark outputs that print secrets; never `terraform output` secrets into logs. Remember state still stores them — lock down backend ACLs and enable encryption.  
3. **IAM:** CI uses OIDC federation to assume a role scoped to that environment’s account/project; separate plan-only vs apply roles when possible.  
4. **State:** S3/GCS/Azure Blob (or HCP Terraform) with encryption, versioning, and no public access; restrict `GetObject`/`PutObject` (or equivalent) to pipeline identities.  
5. **Policy as code:** after `terraform plan -out=tfplan`, export JSON and evaluate rules (for example “no public S3”, “required tags”, “forbidden instance types”). Fail the PR before human approve/apply.

Security is layered: a green policy check that still commits an API key in Git is not secure.

### Key concepts and comparisons

| Anti-pattern | Better pattern |
|--------------|----------------|
| Password in committed tfvars | Vault/SSM/Secrets Manager + reference |
| Long-lived cloud keys in CI | OIDC → short-lived role |
| Unencrypted state bucket | SSE + private ACL / bucket policy |
| Cluster-admin apply role | Env-scoped least privilege |
| “We’ll review plans manually” only | Automated policy + human approve for prod |

| Engine | Where it runs | Language |
|--------|---------------|----------|
| OPA / Conftest | Any CI | Rego |
| Sentinel | HCP Terraform / TFE | Sentinel |

### Common pitfalls

- Believing `sensitive = true` keeps values out of state — it does not.  
- Printing `terraform show` plan files into public CI logs.  
- Storing `terraform.tfstate` in Git “temporarily”.  
- Trusting module provenance while ignoring the IAM policy the module creates.  
- Disabling policy fail-closed so a change “just applies” — fix the config or request a reviewed exception.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-terraform/module-15 && cd ~/rebash-terraform/module-15
```

**Focus:** hands-on practice for Terraform Security and Secrets

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-terraform/module-15 && cd ~/rebash-terraform/module-15

cat > variables.tf << 'EOF'
variable "db_password" {
  type      = string
  sensitive = true
}

variable "environment" {
  type = string
}
EOF

cat > outputs.tf << 'EOF'
output "environment" {
  value = var.environment
}

output "db_password" {
  value     = var.db_password
  sensitive = true
}
EOF

cat > main.tf << 'EOF'
resource "local_file" "env" {
  filename = "${path.module}/env.txt"
  content  = "env=${var.environment}\n"
}
EOF

cat > security-checklist.md << 'EOF'
- [ ] No plaintext secrets in Git (tfvars, backend configs)
- [ ] sensitive = true on secret variables and outputs
- [ ] Secrets from Vault / SSM / Secrets Manager (or CI OIDC)
- [ ] Remote state encrypted; backend IAM least privilege
- [ ] CI uses short-lived credentials (OIDC), not static keys
- [ ] Policy as code (OPA/Sentinel) on plan before apply
- [ ] Plan artefacts treated as sensitive in CI
EOF

terraform init
TF_VAR_db_password='not-a-real-secret' TF_VAR_environment=lab \
  terraform apply -auto-approve
terraform output
# db_password should be redacted in CLI output
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-terraform/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-terraform/module-15/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Terraform Security and Secrets** always combines:

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

!!! warning "Believing `sensitive = true` keeps values out of state — it does not.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Printing `terraform show` plan files into public CI logs.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Terraform Security and Secrets changes as code and review them in pull requests
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

**Terraform Security and Secrets** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Terraform Security and Secrets** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Terraform in CI/CD Pipelines](terraform-in-ci-cd-pipelines.md)

## References

- [Sensitive values](https://developer.hashicorp.com/terraform/language/values/variables#suppressing-values-in-cli-output) · [OPA](https://www.openpolicyagent.org/) · [Sentinel](https://developer.hashicorp.com/sentinel)
