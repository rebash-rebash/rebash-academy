---
title: "Workspaces and Environment Strategies"
description: "Use Terraform workspaces to separate environment state, compare workspace strategies with directory and branch models, and apply safely across dev, staging, and production."
difficulty: intermediate
estimated_time: "60–70 min"
technology: terraform
category: terraform
module: "Module 12 · Workspaces"
learning_paths:
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
  - terraform/remote-state-and-backends
next:
  - terraform/terraform-cloud-and-hcp-terraform
related:
  - terraform/production-terraform-patterns
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
last_updated: "2026-08-03"
comments: false
---

# Workspaces and Environment Strategies

## Overview

Running dev and production from the same directory without separation is how `terraform destroy` accidents happen. **Terraform workspaces** multiply **state instances** for the same configuration — `dev`, `staging`, and `prod` each get isolated state while code stays identical.

This tutorial covers **`terraform workspace` commands**, **`terraform.workspace`**, **environment separation strategies** (workspaces vs directories vs branches), and production cautions. The lab under `~/rebash-terraform/module-12` creates **dev** and **staging** workspaces with isolated Docker containers and separate state files.

This is **Tutorial 14** in **Module 12: Workspaces** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series.

## Prerequisites

- [Data Sources and Existing Infrastructure](data-sources-and-existing-infrastructure.md)
- [Remote State and Backends](remote-state-and-backends.md)
- Terraform CLI ≥ 1.5

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Create, list, select, and delete Terraform workspaces
- [ ] Use `terraform.workspace` in expressions for environment-specific behaviour
- [ ] Explain isolated state paths under `terraform.tfstate.d/`
- [ ] Compare workspace, directory, and branch environment models
- [ ] Describe when workspaces are insufficient for production isolation

## Architecture

One configuration code path; workspace selection switches which state file Terraform loads under `terraform.tfstate.d/`.

![Terraform workspaces](../assets/excalidraw/terraform-workspaces.svg)

## Theory

### What it is

**Workspaces** are named state instances for a single root module:

``` {.bash .ra-terminal title="Terminal"}
terraform workspace new dev
terraform workspace new staging
terraform workspace select dev
terraform apply
```

In HCL:

```hcl
locals {
  env_config = {
    dev     = { replicas = 1 }
    staging = { replicas = 2 }
    prod    = { replicas = 3 }
  }
  replicas = local.env_config[terraform.workspace].replicas
}
```

**Default workspace** is `default` — many teams create explicit `dev` instead of using `default` for production-adjacent work.

**State storage:** local backend places files in **`terraform.tfstate.d/<workspace>/terraform.tfstate`**. Remote backends use **workspace key prefixes** (S3) or separate workspace objects (Terraform Cloud).

### Why it matters

Workspaces let engineers **reuse one module tree** with different state — fast context switching for smaller teams. Combined with **remote backends**, each workspace can map to different state keys. Understand limits: workspaces **share** the same backend credentials and provider config unless you add logic — they are **not** hard multi-account isolation alone.

### How it works

1. **`terraform workspace list`** — shows current selection (`*`).
2. **`terraform workspace select NAME`** — switches active state.
3. Plan/apply operates only on **current workspace state**.
4. **`terraform.workspace`** interpolates active workspace name in expressions.
5. **`terraform workspace delete NAME`** — removes workspace (must be empty of managed resources or force after destroy).

| Strategy | Isolation | Same code? |
|----------|-----------|------------|
| Workspaces | State only (shared backend config) | Yes |
| Directory per env (`env/dev`, `env/prod`) | State + different var files | Often duplicated root |
| Branch per env | Process isolation | Yes in Git |
| Separate stacks + remote state | Strong ownership boundaries | Partial reuse via modules |

### Key concepts and comparisons

| Model | Good for | Weak for |
|-------|----------|----------|
| Workspaces | Quick env toggles; small teams | Hard multi-account blast walls |
| Directory layout | Different backends per env | Duplication without modules |
| Terraform Cloud workspaces | RBAC, run tasks, policy | Cost; SaaS dependency |
| `-var-file` only (single workspace) | Simple two-tier | Easy to apply wrong tfvars |

### Common pitfalls

- **Applying in wrong workspace** — prod destroy from dev laptop.
- **Using `default` for production** — unclear intent; rename explicitly.
- **Workspace-only prod isolation** — same AWS creds manage all workspaces.
- **Deleting workspace with resources** — fails until destroy in that workspace.
- **Assuming workspaces replace tfvars** — you still need variable values per env.

## Hands-on Lab

### Objective

Create **dev** and **staging** workspaces, apply environment-specific **Docker containers** with different replica labels, prove separate state files and distinct container IDs, and validate with an evidence script under `~/rebash-terraform/module-12`.

### Prerequisites

- Terraform CLI ≥ 1.5
- Docker Engine running (`docker info` succeeds)
- Completed Module 8–11 labs

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-terraform/module-12 && cd ~/rebash-terraform/module-12
```

Local backend — workspace state files appear under `terraform.tfstate.d/`.

### Real-world scenario

A platform team uses one service module for **dev** and **staging**, deploying different container replica counts per workspace. Before promoting workspace patterns to S3 backends, you prove state isolation locally so a staging destroy never removes dev containers.

### Step-by-step tasks

#### Task 1 – Configuration with terraform.workspace and Docker

Create `versions.tf`:

```hcl title="versions.tf"
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}
```

Create `providers.tf`:

```hcl title="providers.tf"
provider "docker" {}
```

Create `variables.tf`:

```hcl title="variables.tf"
variable "owner" {
  type    = string
  default = "platform-team"
}
```

Create `locals.tf`:

```hcl title="locals.tf"
locals {
  workspace_replicas = {
    dev     = 1
    staging = 2
    default = 1
  }

  replicas = lookup(local.workspace_replicas, terraform.workspace, 1)
}
```

Create `main.tf`:

```hcl title="main.tf"
resource "docker_image" "env_marker" {
  name         = "nginx:1.27-alpine"
  keep_locally = true
}

resource "docker_container" "env_marker" {
  count = local.replicas

  name  = "rebash-${terraform.workspace}-${count.index}"
  image = docker_image.env_marker.image_id

  labels = {
    workspace = terraform.workspace
    replica   = tostring(count.index)
    owner     = var.owner
    managed_by = "terraform"
  }
}
```

Create `outputs.tf`:

```hcl title="outputs.tf"
output "active_workspace" {
  value = terraform.workspace
}

output "replica_count" {
  value = local.replicas
}

output "container_ids" {
  value = docker_container.env_marker[*].id
}
```

Run:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-terraform/module-12
terraform init
terraform validate
echo "config OK" | tee config-ok.txt
```

!!! example "Expected output"
    Validate succeeds in default workspace.


#### Task 2 – Create dev workspace and apply

Run:

{% raw %}
``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-terraform/module-12
terraform workspace new dev
terraform workspace select dev
terraform apply -auto-approve
terraform output -raw active_workspace | tee ws-dev.txt
terraform output -raw replica_count | tee replicas-dev.txt
test "$(cat ws-dev.txt)" = "dev"
test "$(cat replicas-dev.txt)" = "1"
docker ps --filter "label=workspace=dev" --format '{{.Names}}' | tee dev-containers.txt
grep -q 'rebash-dev-0' dev-containers.txt
test -f ~/rebash-terraform/module-12/terraform.tfstate.d/dev/terraform.tfstate
echo "dev workspace OK" | tee dev-ws-ok.txt
```
{% endraw %}

!!! example "Expected output"
    Active workspace `dev`; one container `rebash-dev-0`; state file under `terraform.tfstate.d/dev/`.


#### Task 3 – Create staging workspace and apply

Run:

{% raw %}
``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-terraform/module-12
terraform workspace new staging
terraform workspace select staging
terraform apply -auto-approve
terraform output -raw replica_count | tee replicas-staging.txt
test "$(cat replicas-staging.txt)" = "2"
docker ps --filter "label=workspace=staging" --format '{{.Names}}' | tee staging-containers.txt
grep -q 'rebash-staging-0' staging-containers.txt
grep -q 'rebash-staging-1' staging-containers.txt
terraform workspace select dev
docker ps --filter "label=workspace=dev" --format '{{.Names}}' | tee dev-check.txt
grep -q 'rebash-dev-0' dev-check.txt
test -f ~/rebash-terraform/module-12/terraform.tfstate.d/staging/terraform.tfstate
echo "staging workspace OK" | tee staging-ws-ok.txt
```
{% endraw %}

!!! example "Expected output"
    Staging has two containers; dev container still running — states are isolated.


#### Task 4 – Workspace evidence script

Create `workspace-evidence.sh`:

{% raw %}
``` {.bash .ra-terminal title="Terminal"}
#!/usr/bin/env bash
set -euo pipefail
cd ~/rebash-terraform/module-12
terraform workspace select dev
DEV_COUNT="$(docker ps --filter 'label=workspace=dev' --format '{{.ID}}' | wc -l | tr -d ' ')"
terraform workspace select staging
STAGING_COUNT="$(docker ps --filter 'label=workspace=staging' --format '{{.ID}}' | wc -l | tr -d ' ')"
test "$DEV_COUNT" = "1"
test "$STAGING_COUNT" = "2"
terraform workspace list | tee workspace-list.txt
grep -q 'dev' workspace-list.txt
grep -q 'staging' workspace-list.txt
echo "workspace-evidence PASS" | tee workspace-evidence-pass.txt
```
{% endraw %}

Run:

``` {.bash .ra-terminal title="Terminal"}
chmod +x ~/rebash-terraform/module-12/workspace-evidence.sh
~/rebash-terraform/module-12/workspace-evidence.sh
```

!!! example "Expected output"
    Dev has 1 container, staging has 2; evidence script passes.


### Validation steps

- [ ] Created dev and staging workspaces
- [ ] `terraform.workspace` drove replica count via `count`
- [ ] Separate state files under `terraform.tfstate.d/`
- [ ] Switching workspace changes running containers without code edits
- [ ] Evidence script confirms distinct container sets per workspace

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Workspace already exists | Re-run new | Use `select` instead of `new` |
| Cannot delete workspace | Resources remain | `select` workspace; `destroy`; then delete |
| Same output both workspaces | Wrong workspace selected | `terraform workspace show` |
| lookup default missing key | Workspace not in map | Extend `workspace_replicas` map |
| Container name conflict | Leftover container from manual run | `docker rm -f` orphan; re-apply |

### Challenge exercise

Add **`prod`** to `workspace_replicas` with value `3`, create workspace, apply, and verify without touching dev/staging containers:

{% raw %}
``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-terraform/module-12
# Add prod = 3 to locals.workspace_replicas in locals.tf
terraform workspace new prod
terraform workspace select prod
terraform apply -auto-approve
docker ps --filter "label=workspace=prod" --format '{{.Names}}' | wc -l | grep -q '^3$'
terraform workspace select dev
docker ps --filter "label=workspace=dev" --format '{{.Names}}' | wc -l | grep -q '^1$'
echo "prod workspace challenge OK"
```
{% endraw %}

!!! example "Expected output"
    Prod shows 3 containers; dev unchanged at 1.


### Learning outcomes

- Workspace CLI workflow with real infrastructure
- terraform.workspace driving resource count
- Physical state isolation paths
- Safe workspace switching habits with operational proof

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-terraform/module-12
terraform workspace select prod 2>/dev/null && terraform destroy -auto-approve || true
terraform workspace select staging && terraform destroy -auto-approve
terraform workspace select dev && terraform destroy -auto-approve
terraform workspace select default
terraform workspace delete prod 2>/dev/null || true
terraform workspace delete staging
terraform workspace delete dev
rm -f config-ok.txt ws-dev.txt replicas-dev.txt dev-containers.txt dev-ws-ok.txt \
  replicas-staging.txt staging-containers.txt dev-check.txt staging-ws-ok.txt \
  workspace-list.txt workspace-evidence-pass.txt
rm -rf terraform.tfstate.d .terraform .terraform.lock.hcl terraform.tfstate terraform.tfstate.backup
```

## Validation

- [ ] Completed module-12 workspace lab
- [ ] Can list workspace vs directory strategies
- [ ] Know where local workspace state files live
- [ ] Can explain workspace isolation limits

## Code Walkthrough

1. **Explicit workspace names** — avoid unnamed `default` for real envs.
2. **lookup with default** — handle unknown workspace keys safely.
3. **Select before plan** — shell prompt or CI echo current workspace.
4. **Separate state files** — verify path in `terraform.tfstate.d/`.
5. **Pair with var-files** — workspace name + tfvars double confirmation in CI.

## Security Considerations

- Workspaces share provider credentials unless using assume-role per workspace logic.
- Restrict `terraform workspace select prod` via CI-only production applies.
- Remote backend IAM should scope workspace key prefixes per environment.
- Audit workspace deletes — state removal does not destroy resources if skipped.
- Do not rely on workspaces alone for regulatory environment separation.

## Common Mistakes

!!! warning "Wrong workspace during apply"
    Classic source of prod incidents.  
    **Fix:** CI prints `terraform workspace show`; require approval for prod workspace.

!!! warning "Workspaces as multi-account strategy alone"
    Same AWS profile across workspaces — insufficient isolation.  
    **Fix:** Separate accounts + roles; directories or stacks per account.

!!! warning "Deleting workspace before destroy"
    Orphan resources keep running.  
    **Fix:** Destroy in workspace first; then `workspace delete`.

## Best Practices

- Name workspaces after environments (`dev`, `staging`, `prod`).
- Combine workspaces with **per-env tfvars** and remote state key prefixes.
- Document workspace naming in README; ban ad-hoc workspace names.
- CI pipeline parameter selects workspace — not interactive shells for prod.
- For large orgs, prefer **Terraform Cloud workspaces** with RBAC over CLI-only workspaces.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Plan empty wrong env | Selected wrong workspace | `terraform workspace show` |
| Resource already exists | Duplicate apply another ws | Import or destroy other workspace copy |
| workspace delete fails | State has resources | Destroy first |
| Same state two workspaces | Backend misconfigured prefix | Fix remote workspace_key_prefix |
| terraform.workspace empty | Very old Terraform | Upgrade; use terraform 0.12+ |

## Summary

Workspaces isolate **state** for the same configuration — enabling dev/staging/prod toggles with `terraform workspace select`. You applied distinct replica settings per workspace and verified separate state files. Next, [Terraform Cloud and HCP Terraform](terraform-cloud-and-hcp-terraform.md) adds remote runs, RBAC, and policy.

## Interview Questions

**1. What problem do Terraform workspaces solve?**

??? success "Reveal answer"
    They let one **root module code base** maintain **multiple isolated state files** (environments) without duplicating directories. Switching workspace switches state — useful for dev/staging/prod iterations from the same checkout.

**2. How do you reference the current workspace in HCL?**

??? success "Reveal answer"
    Use the **`terraform.workspace`** built-in expression in locals, variables, or resource arguments — for example different CIDR maps or feature flags keyed by workspace name.

**3. Where is workspace state stored locally?**

??? success "Reveal answer"
    Under **`terraform.tfstate.d/<workspace_name>/terraform.tfstate`** when using the local backend. The **`default`** workspace uses **`terraform.tfstate`** in the root module directory (unless configured otherwise).

**4. Compare workspaces vs separate directories per environment.**

??? success "Reveal answer"
    **Workspaces** — same code, isolated state, fast switch; weaker isolation of backend config/credentials. **Directories** (`env/dev`, `env/prod`) — can point to different backends, var files, and provider aliases explicitly; more duplication unless modules extract common code.

**5. Can workspaces replace separate AWS accounts for production isolation?**

??? success "Reveal answer"
    **No** — workspaces only separate **state** by default; **provider credentials** are usually shared unless you wire assume-role maps per `terraform.workspace`. Production typically needs **account-level** isolation plus remote state RBAC.

**6. What happens if you terraform destroy in the wrong workspace?**

??? success "Reveal answer"
    You destroy resources tracked in **that workspace's state** — if prod workspace is selected, prod resources go. Prevention: CI gates, explicit workspace echo, separate AWS roles so dev credentials cannot destroy prod even if workspace wrong.

**7. How do remote S3 backends map workspaces?**

??? success "Reveal answer"
    Backend **`workspace_key_prefix`** (or default behaviour) stores state at different **S3 keys** per workspace — for example `env:/dev/network/terraform.tfstate`. Same bucket, different objects; locking still required.

**8. When should you delete a workspace?**

??? success "Reveal answer"
    After **`terraform destroy`** emptied that workspace's resources and the environment is decommissioned. Deleting a workspace removes its state metadata — do not delete if resources still exist unless you intentionally orphan them (rare, documented).

## Related Tutorials

- [Terraform course index](index.md)
- **Previous:** [Data Sources and Existing Infrastructure](data-sources-and-existing-infrastructure.md)
- **Next:** [Terraform Cloud and HCP Terraform](terraform-cloud-and-hcp-terraform.md)
- [Production Terraform Patterns](production-terraform-patterns.md)
- [Remote State and Backends](remote-state-and-backends.md)

## References

- [Terraform workspaces CLI](https://developer.hashicorp.com/terraform/cli/workspaces)
- [terraform.workspace](https://developer.hashicorp.com/terraform/language/state/workspace)
- [Backend workspace prefixes](https://developer.hashicorp.com/terraform/language/settings/backends/s3)
- [Workspaces vs directories (HashiCorp guidance)](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/run/workspaces)
- [Production environment strategies](https://developer.hashicorp.com/terraform/language/settings/backends)
