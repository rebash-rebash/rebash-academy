---
title: "Terraform Pipelines in GitLab"
description: "Run Terraform init, validate, plan, and apply in GitLab CI with remote state, plan artefacts on merge requests, and protected apply."
difficulty: advanced
estimated_time: "50–65 min"
technology: gitlab
category: gitlab
module: "Module 10 · Terraform Pipelines"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - gitlab-ci
  - terraform
  - infrastructure-as-code
prerequisites:
  - gitlab/kubernetes-deploys-and-gitlab-agent
next:
  - gitlab/multi-cloud-deployments-with-gitlab
related:
  - terraform/terraform-in-ci-cd-pipelines
  - terraform/remote-state-and-backends
  - gitlab/production-pipelines-and-environments
labs: []
projects: []
interview: interview/gitlab
certifications:
  - GitLab Certified CI/CD Associate
  - GitLab Certified DevOps Professional
tags:
  - gitlab
  - terraform
  - iac
  - plan
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---


# Terraform Pipelines in GitLab

## Overview








Design a GitLab pipeline that runs `init` → `validate` → `plan` on merge requests (with a plan artefact) and a protected `apply` on the default branch — with remote state outside the runner workspace.

Terraform in GitLab CI automates Infrastructure as Code (IaC): every change is planned in review, then applied under gates. Store **remote state** with locking. Attach the binary **plan** as a job artefact so apply executes what reviewers saw. Never leave state only on the runner disk.

This is a core tutorial in **Module 10 · Terraform Pipelines** of the REBASH Academy **GitLab CI/CD for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites








- [Kubernetes Deploys and GitLab Agent](kubernetes-deploys-and-gitlab-agent.md)

## Learning Objectives








By the end of this tutorial, you will be able to:

- [ ] Sequence init, validate, plan, apply, and optional destroy  
- [ ] Store plan output as a GitLab artefact for MR review  
- [ ] Gate apply with a protected environment  
- [ ] Explain remote state + locking in CI  
- [ ] Use `TF_IN_AUTOMATION` and non-interactive flags

## Architecture








This topic’s control points and relationships are shown below.

![Terraform pipeline in GitLab](../assets/excalidraw/gitlab-terraform-pipeline.svg)

## Theory








### What it is

A **Terraform pipeline** maps CLI phases onto GitLab stages: `fmt`/`validate` and `plan -out=` on every MR (low / plan privilege); reviewed **apply** of the saved plan on the default branch or a protected environment; rare, heavily gated **destroy**. State lives in a **remote backend** with locking. CI uses short-lived credentials (often OIDC — Module 11). `TF_IN_AUTOMATION=true` and `-input=false` keep jobs non-interactive.

### Why it matters

Laptop apply bypasses review and uses personal cloud keys. MR plans give reviewers a concrete diff; protected apply prevents unreviewed infrastructure changes. Plan artefacts stop “plan on Tuesday, apply Thursday’s different config.” State locking prevents two pipelines from corrupting the same workspace.

### How it works

1. On MR: pin Terraform → `init` → `validate` → `plan -out=tfplan` → upload artefact (short `expire_in`).  
2. Job log shows `terraform show` summary for reviewers.  
3. On merge (or after environment approval): download the same artefact → `apply -input=false tfplan`.  
4. Destroy jobs are manual and environment-protected.  
5. Backend config comes from CI variables or a committed backend block — no secrets in Git.

Prefer apply-of-saved-plan for production.

### Key concepts and comparisons

| Concern | Good practice | Risk |
|---------|---------------|------|
| State | Remote + lock | Local state on runner |
| Plan | Artefact tied to MR SHA | Fresh plan at apply with drift |
| Apply | Protected environment | Auto-apply on every push |
| Secrets | OIDC / masked vars | Static admin keys |

### Common pitfalls

- Committing `.terraform/` or `terraform.tfstate` to Git.  
- Applying without the reviewed plan artefact.  
- Logging plans that include secret attribute values.  
- One shared state key for all environments; fork MRs with apply roles.

## Hands-on Lab



### Objective

Author a Docker-backed Terraform module, run **init → plan → apply → destroy** locally against the Docker provider, and wire a GitLab CI pipeline with **fmt**, **validate**, and **plan** jobs plus plan artefacts for merge request review.

### Prerequisites

- Docker Engine running (`docker info`)
- Terraform CLI 1.5+ (`terraform version`)
- Python 3 with PyYAML (`pip install pyyaml`)
- Optional: GitLab project with a runner to execute jobs (local simulation proves the module first)

### Lab environment

Workspace: `~/rebash-gitlab/module-10`

File-first lab. Push to GitLab only when you want a runner to execute jobs.

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-gitlab/module-10 && cd ~/rebash-gitlab/module-10
set -euo pipefail
```

### Real-world scenario

Platform engineering requires every Infrastructure as Code (IaC) merge request to show a reviewed Terraform plan artefact before anyone can apply on the default branch. You deliver the module and pipeline YAML for review before cloud credentials are wired.

### Step-by-step tasks

#### Task 1 – Docker-backed Terraform module

Create `main.tf`:

{% raw %}
```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "nginx" {
  name         = "nginx:1.25-alpine"
  keep_locally = false
}

resource "docker_container" "rebash_lab" {
  name  = "rebash-gitlab-tf-lab"
  image = docker_image.nginx.image_id

  ports {
    internal = 80
    external = 8080
  }
}

output "container_id" {
  value = docker_container.rebash_lab.id
}

output "url" {
  value = "http://127.0.0.1:8080"
}
```
{% endraw %}

Init, validate, and plan against the Docker provider:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-gitlab/module-10
set -euo pipefail
docker info >/dev/null
terraform init | tee init.txt
terraform fmt -check -recursive | tee fmt.txt
terraform validate | tee validate.txt
terraform plan -out=tfplan -input=false | tee plan.txt
test -f tfplan
grep -q 'docker_container.rebash_lab' plan.txt
```

!!! example "Expected output"
    `plan.txt` shows `docker_container.rebash_lab` will be created; `tfplan` exists.


#### Task 2 – GitLab CI pipeline (fmt / validate / plan)

Create `.gitlab-ci.yml`:

{% raw %}
```yaml
stages:
  - fmt
  - validate
  - plan

variables:
  TF_IN_AUTOMATION: "true"
  TF_ROOT: "${CI_PROJECT_DIR}"

.terraform_base:
  image:
    name: hashicorp/terraform:1.5.7
    entrypoint: [""]
  before_script:
    - cd "${TF_ROOT}"
    - terraform --version

terraform-fmt:
  extends: .terraform_base
  stage: fmt
  script:
    - terraform fmt -check -recursive -diff
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

terraform-validate:
  extends: .terraform_base
  stage: validate
  needs: [terraform-fmt]
  script:
    - terraform init -input=false
    - terraform validate
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

terraform-plan:
  extends: .terraform_base
  stage: plan
  needs: [terraform-validate]
  script:
    - terraform plan -input=false -out=tfplan
    - terraform show -no-color tfplan > plan.txt
  artifacts:
    paths:
      - tfplan
      - plan.txt
    expire_in: 7 days
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```
{% endraw %}

Validate offline:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-gitlab/module-10
set -euo pipefail
python3 -c "
import yaml
d = yaml.safe_load(open('.gitlab-ci.yml'))
assert d['stages'] == ['fmt', 'validate', 'plan']
assert 'terraform-plan' in d
assert d['terraform-plan']['artifacts']['paths'] == ['tfplan', 'plan.txt']
print('gitlab-ci OK', list(d))
"
grep -q 'hashicorp/terraform:1.5.7' .gitlab-ci.yml
```

!!! example "Expected output"
    `gitlab-ci OK` with job keys; pinned Terraform image present.


#### Task 3 – Apply, prove the container, and destroy locally

Create `pipeline-simulate.sh`:

{% raw %}
``` {.bash .ra-terminal title="Terminal"}
#!/usr/bin/env bash
set -euo pipefail
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml'))"
grep -q 'TF_IN_AUTOMATION' .gitlab-ci.yml
docker info >/dev/null
terraform init -input=false
terraform validate
terraform plan -input=false -out=tfplan
terraform show -no-color tfplan > plan.txt
terraform apply -input=false -auto-approve tfplan
docker ps --filter name=rebash-gitlab-tf-lab --format '{{.Names}} {{.Status}}' | tee container-proof.txt
grep -q 'rebash-gitlab-tf-lab' container-proof.txt
curl -sf http://127.0.0.1:8080 >/dev/null
terraform destroy -input=false -auto-approve
echo 'module-10 terraform lab passed'
```
{% endraw %}

Run it:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-gitlab/module-10
set -euo pipefail
chmod +x pipeline-simulate.sh
./pipeline-simulate.sh | tee validation.txt
```

!!! example "Expected output"
    `container-proof.txt` shows `rebash-gitlab-tf-lab` running; script ends with `module-10 terraform lab passed`.


### Validation steps

- [ ] `main.tf` uses the Docker provider (no cloud credentials)
- [ ] `pipeline-simulate.sh` applies, curls port 8080, and destroys the container
- [ ] `.gitlab-ci.yml` parses; stages are fmt → validate → plan
- [ ] Plan job uploads `tfplan` and `plan.txt` artefacts with `expire_in: 7 days`
- [ ] Pinned image `hashicorp/terraform:1.5.7` present

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `terraform init` fails offline | Provider download blocked | Run locally with network once, or validate YAML only |
| fmt job red | Unformatted `.tf` files | Run `terraform fmt -recursive` before push |
| Empty plan artefact | Plan job skipped by `rules` | Confirm MR or default-branch pipeline |
| Apply without reviewed plan | Missing apply gate | Add manual apply job consuming the same `tfplan` artefact |
| State on runner disk | No remote backend | Configure S3/GCS/Azure backend before production |

### Challenge exercise

Add a manual `terraform-apply` job on the default branch that downloads the plan artefact from the same pipeline and runs `terraform apply -input=false tfplan`. Gate it with a protected `production` environment.

### Learning outcomes

- Authored a Docker-provider Terraform module with real apply/destroy proof
- Mapped Terraform phases to GitLab CI stages with `needs`
- Attached plan artefacts for merge request review
- Simulated the full plan → apply → destroy loop locally before pushing pipeline YAML

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-gitlab/module-10
terraform destroy -input=false -auto-approve 2>/dev/null || true
docker rm -f rebash-gitlab-tf-lab 2>/dev/null || true
rm -rf .terraform terraform.tfstate terraform.tfstate.backup tfplan plan.txt container-proof.txt 2>/dev/null || true
ls ~/rebash-gitlab/module-10
```

## Validation








- [ ] Lab commands run under `~/rebash-gitlab/module-10/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough








Production practice for **Terraform Pipelines in GitLab** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations








- Treat credentials and tokens for gitlab as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes








!!! warning "Committing `.terraform/` or `terraform.tfstate` to Git.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Applying without the reviewed plan artefact.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices








- Encode Terraform Pipelines in GitLab changes as code and review them in pull requests
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








**Terraform Pipelines in GitLab** is essential for Cloud and DevOps engineers working with gitlab. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions






1. Why store terraform plan as an artifact before apply?
2. What does TF_IN_AUTOMATION change about Terraform CLI behaviour?
3. How do you keep state safe when plans run in CI?
4. Why is apply usually manual on the default branch?
5. How do you destroy lab infrastructure created in a pipeline experiment?

!!! tip "Sample answer — question 2"
    Confirm init backend config and that apply uses the exact plan artifact from the same pipeline. Drift and different variable sets between plan/apply are common.

!!! tip "Sample answer — question 4"
    Protect state with remote backends and restricted IAM/OIDC roles. Destroy experimental stacks in the same change window.

## Related Tutorials








- [Course overview](index.md)
- [Multi-Cloud Deployments with GitLab](multi-cloud-deployments-with-gitlab.md)

## References








- [Terraform and GitLab](https://docs.gitlab.com/ee/user/infrastructure/iac/) · [Automating Terraform](https://developer.hashicorp.com/terraform/cli/run/automating-terraform) · [Environments](https://docs.gitlab.com/ee/ci/environments/)
