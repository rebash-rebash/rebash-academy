---
title: "Workspaces and Environment Strategies"
description: "Use Terraform workspaces for light isolation, and know when separate state roots beat workspaces for production environment separation."
difficulty: intermediate
estimated_time: "40–55 min"
technology: terraform
category: terraform
module: "Module 12 · Workspaces"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - workspaces
  - environments
prerequisites:
  - terraform/data-sources-and-existing-infrastructure
next:
  - terraform/terraform-cloud-and-hcp-terraform
related:
  - terraform/remote-state-and-backends
  - terraform/terraform-in-ci-cd-pipelines
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - workspaces
  - environments
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Workspaces and Environment Strategies

## Overview



Create and select Terraform workspaces, use `terraform.workspace` carefully, and choose when separate roots (not workspaces) should isolate production.

**Workspaces** isolate state for the same configuration. Selecting `dev` versus `staging` points Terraform at a different state slot while reusing the same `.tf` files. They suit light isolation — review apps, homogeneous clones — but many teams prefer **separate directories, accounts, or repositories** for production. Choose by blast radius, not habit.

This is a core tutorial in **Module 12 · Workspaces** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Data Sources and Existing Infrastructure](data-sources-and-existing-infrastructure.md)
- [Remote State and Backends](remote-state-and-backends.md)
- Terraform CLI 1.9+



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Create and select workspaces with the CLI  
- [ ] Use `terraform.workspace` in expressions safely  
- [ ] Compare workspaces vs separate root modules  
- [ ] Know when *not* to use workspaces for prod



## Architecture



This topic’s control points and relationships are shown below.

![Workspaces](../assets/excalidraw/terraform-workspaces.svg)



## Theory



### What it is

Each workspace has its own state (local subdirectory or remote key suffix / metadata). The default workspace is usually named `default`. CLI: `terraform workspace new`, `list`, `select`, `show`, `delete`. The interpolation `terraform.workspace` returns the current name so you can derive tags or names — not so you can hide an entire production topology behind one boolean.

HCP Terraform / Terraform Cloud also use “workspaces,” but those are richer objects (VCS, variables, run history). Do not confuse CLI workspaces with HCP workspaces until the next module.

### Why it matters

Environment separation protects production from a bad apply aimed at staging. Workspaces alone do **not** give you separate IAM roles, accounts, or approval gates — they only split state. If prod and non-prod share credentials, a wrong `workspace select` is a high-severity incident. Separate roots (for example `envs/dev` and `envs/prod`) with different backends, keys, and cloud accounts make the blast radius obvious in Git and CI.

### How it works

1. Same configuration directory; `workspace select NAME` switches which state Terraform reads and writes.
2. Apply in `dev` does not update state for `prod` — different bindings, same `.tf` tree.
3. Expressions may branch on `terraform.workspace`, but large behavioural forks become unreadable — prefer tfvars per root instead.
4. CI must select the workspace explicitly (or use separate roots) so runners never apply the wrong state by accident.
5. Deleting a workspace does not destroy infrastructure by itself — you must destroy (or abandon) resources first; remote objects can remain.

### Key concepts and comparisons

| Strategy | Pros | Cons |
|----------|------|------|
| CLI workspaces | One config tree; quick clones | Easy to mis-select; shared code for all envs |
| Separate roots + backends | Clear blast radius; different IAM | More directories to maintain |
| Separate accounts / projects | Strong isolation | Higher org overhead |

| Use workspaces when | Prefer separate roots when |
|---------------------|----------------------------|
| Envs are nearly identical | Prod needs different approvals / IAM |
| Short-lived review stacks | Compliance requires account isolation |
| Solo / small team labs | Different module versions per env |

### Common pitfalls

- Using workspaces as the only prod vs non-prod control plane.
- Branching huge graphs on `terraform.workspace` instead of tfvars / roots.
- Forgetting CI must set the workspace — default workspace accidents.
- Deleting a workspace and assuming cloud resources are gone.
- Equating CLI workspaces with HCP Terraform workspaces without reading the docs.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-terraform/module-12/workspaces/out && cd ~/rebash-terraform/module-12/workspaces/out
```

**Focus:** Use workspaces to separate lab environments in one configuration

### Step 1 – Apply in default workspace then create another

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
terraform apply -auto-approve
terraform workspace list
terraform workspace new staging
```

### Step 2 – Apply in staging and contrast state

```bash
terraform apply -auto-approve
terraform workspace show
terraform state list
terraform workspace select default
terraform state list
echo "Workspaces isolate state keys; prefer separate directories/accounts for strong prod isolation"
```

### Final step – Cleanup note

```bash
terraform workspace select staging 2>/dev/null || true
terraform destroy -auto-approve || true
terraform workspace select default
terraform destroy -auto-approve
terraform workspace delete staging 2>/dev/null || true
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-terraform/module-12/workspaces/out/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Workspaces and Environment Strategies** always combines:

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



!!! warning "Using workspaces as the only prod vs non-prod control plane."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Branching huge graphs on `terraform.workspace` instead of tfvars / roots."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Workspaces and Environment Strategies changes as code and review them in pull requests
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



**Workspaces and Environment Strategies** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. What does a Terraform workspace change about state?
2. When are workspaces a good fit versus separate directories or accounts?
3. How can workspace-based prod/staging separation fail as a hard tenancy boundary?
4. What naming strategy helps avoid applying the wrong workspace?
5. How do workspaces interact with remote backends?

!!! tip "Sample answer — question 2"
    Workspaces select different state keys for the same configuration. They are convenient for similar environments but easy to mis-select.

!!! tip "Sample answer — question 4"
    Because code is shared, a variable mistake can affect prod if you select the wrong workspace. Stronger isolation uses separate states, accounts, and pipelines.



## Related Tutorials



- [Course overview](index.md)
- [Terraform Cloud and HCP Terraform](terraform-cloud-and-hcp-terraform.md)



## References



- [Workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces)  
- [CLI: workspace](https://developer.hashicorp.com/terraform/cli/workspaces)  
- [State](https://developer.hashicorp.com/terraform/language/state)
