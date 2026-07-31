---
title: "Multi-Cloud Deployments with GitHub Actions"
description: "Deploy to AWS, Azure, and Google Cloud from GitHub Actions using OIDC — IAM/ECS/EKS, service principals/AKS, and Workload Identity/GKE/Cloud Run."
difficulty: advanced
estimated_time: "55–70 min"
technology: github-actions
category: github-actions
module: "Module 10 · Cloud Deployments"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - github-actions
  - aws
  - azure
  - gcp
  - oidc
prerequisites:
  - github-actions/terraform-pipelines-with-github-actions
next:
  - github-actions/security-scanning-and-supply-chain
related:
  - github-actions/secrets-variables-and-oidc
  - aws/aws-fundamentals-and-global-infrastructure
  - terraform/multi-cloud-terraform
labs: []
projects: []
interview: interview/github-actions
certifications:
  - GitHub Actions
tags:
  - github-actions
  - aws
  - azure
  - gcp
  - oidc
  - multi-cloud
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Multi-Cloud Deployments with GitHub Actions

## Overview




Sketch OpenID Connect (OIDC)–oriented GitHub Actions patterns for Amazon Web Services (AWS) Identity and Access Management (IAM) / Elastic Container Service (ECS) / Elastic Kubernetes Service (EKS), Azure service principals / Azure Kubernetes Service (AKS), and Google Cloud Workload Identity Federation / Google Kubernetes Engine (GKE) / Cloud Run — without embedding long-lived cloud keys in the repository.

Modern deploy jobs **federate identity**: the job requests an OIDC token (`id-token: write`); the cloud exchanges it for a short-lived role. That role then updates ECS/EKS, AKS, GKE, or Cloud Run. Patterns differ by cloud, but the Actions shape is the same — authenticate, deploy an immutable artefact from Module 7, protect production with environments.

This is a core tutorial in **Module 10 · Cloud Deployments** of the REBASH Academy **GitHub Actions for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites




- [Terraform Pipelines with GitHub Actions](terraform-pipelines-with-github-actions.md)



## Learning Objectives




By the end of this tutorial, you will be able to:

- [ ] Explain OIDC federation vs static access keys  
- [ ] Map AWS IAM roles to ECS/EKS deploy jobs  
- [ ] Sketch Azure login (federated credentials) + AKS  
- [ ] Sketch GCP Workload Identity + GKE / Cloud Run  
- [ ] Scope identities per environment and branch



## Architecture




This topic’s control points and relationships are shown below.

![Multi-cloud with OIDC](../assets/excalidraw/gha-multi-cloud.svg)



## Theory




### What it is

**Multi-cloud deployment from GitHub Actions** means workflows call cloud APIs with least-privilege, short-lived credentials:

| Cloud | Identity pattern | Common targets |
|-------|------------------|----------------|
| AWS | IAM OIDC provider → `aws-actions/configure-aws-credentials` | ECS `update-service`, EKS kubeconfig |
| Azure | App registration federated credential → `azure/login` | AKS `kubelogin` / kubectl |
| Google Cloud | Workload Identity Federation → `google-github-actions/auth` | GKE, Cloud Run deploy |

GitHub’s OIDC issuer (`https://token.actions.githubusercontent.com`) is trusted by a cloud identity provider you configure once. Trust conditions should include repository, ref, and optionally environment claims so a compromised pull-request job cannot assume production roles.

### Why it matters

Static keys in repository secrets leak, rarely rotate, and are often over-privileged. OIDC binds trust to `sub` / `ref` / environment so fork or feature-branch pipelines cannot deploy production. Multi-cloud teams need one mental model — federate, deploy SHA artefact, gate production — even when CLIs differ. Terraform (Module 9) often creates the OIDC providers and roles; deploy workflows only consume them.

### How it works

1. Configure cloud trust for the GitHub OIDC issuer and subject conditions (`repo:ORG/REPO:ref:refs/heads/main`, or environment subjects).  
2. Job sets `permissions: id-token: write` and runs the cloud’s auth action.  
3. Deploy uses that session: update an ECS task definition, `helm upgrade` / `kubectl` on EKS/AKS/GKE, or `gcloud run deploy` with a digest.  
4. Staging roles allow default-branch (or selected) pipelines; production roles require protected environments and required reviewers.  
5. Never print tokens. Prefer environment variables for account IDs and cluster names; secrets only when federation is not available.

Reuse Module 7 digests across clouds for the same commit — do not rebuild a different image “for Azure” versus “for AWS”.

### Key concepts and comparisons

| Approach | Pros | Cons |
|----------|------|------|
| OIDC / federation | Short-lived, auditable, branch-aware | Initial IdP setup |
| Static keys / PATs | Simple demos | Rotation, leak blast radius |
| Per-cloud jobs | Clear ownership | Duplicate structure — prefer reusable workflows (Module 14) |

### Common pitfalls

- Trusting `*` subjects on the OIDC provider (any repo can assume the role).  
- Giving one role rights to all accounts and clusters.  
- Running production deploy jobs without environment protection.  
- Mixing long-lived keys “just for break-glass” without a separate process.  
- Redeploying different image digests per cloud for the same commit.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-github-actions/module-10/.github/workflows && cd ~/rebash-github-actions/module-10/.github/workflows
```

**Focus:** OIDC-ready jobs for AWS and Azure shapes (file-only)

### Step 1 – Multi-cloud workflow

```bash
mkdir -p .github/workflows
cat > .github/workflows/multi-cloud.yml << 'EOF'
name: Multi-cloud deploy shapes
on: [workflow_dispatch]
permissions:
  contents: read
jobs:
  aws_oidc:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    environment: aws-staging
    steps:
      - run: echo "configure-aws-credentials when trust exists"
  azure_oidc:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    environment: azure-staging
    steps:
      - run: echo "azure/login with OIDC when federated credential exists"
EOF
```

### Step 2 – Confirm separate environments and id-token

```bash
grep -E 'id-token: write|aws-staging|azure-staging' .github/workflows/multi-cloud.yml
```

### Final step – Cleanup note

```bash
# File-only — no cloud calls
# Keep ~/rebash-github-actions/ for later tutorials
```



## Validation




- [ ] Lab commands run under `~/rebash-github-actions/module-10/.github/workflows/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough




Production practice for **Multi-Cloud Deployments with GitHub Actions** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.



## Security Considerations




- Treat credentials and tokens for github-actions as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces



## Common Mistakes




!!! warning "Trusting `*` subjects on the OIDC provider (any repo can assume the role).  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Giving one role rights to all accounts and clusters.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices




- Encode Multi-Cloud Deployments with GitHub Actions changes as code and review them in pull requests
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




**Multi-Cloud Deployments with GitHub Actions** is essential for Cloud and DevOps engineers working with github-actions. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. How do you structure workflows for AWS and Azure without duplication?
2. What OIDC settings differ per cloud provider?
3. When are reusable workflows better than copy-paste jobs?
4. How do you prevent credential mix-ups across clouds?
5. Which checks should every cloud deploy share?

!!! tip "Sample answer — question 2"
    Verify environment names, id-token permissions, and the cloud-specific login action configuration.

!!! tip "Sample answer — question 4"
    Isolate roles per cloud/environment and keep production approvals separate.



## Related Tutorials




- [Course overview](index.md)
- [Security Scanning and Supply Chain](security-scanning-and-supply-chain.md)



## References




- [OIDC with cloud providers](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect) · [AWS configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials) · [Azure login](https://github.com/Azure/login) · [google-github-actions/auth](https://github.com/google-github-actions/auth)
