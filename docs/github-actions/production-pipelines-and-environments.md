---
title: "Production Pipelines and Environments"
description: "Promote immutable artefacts through multi-environment GitHub Actions pipelines with protected environments, approvals, rollback, blue/green, and canary."
difficulty: advanced
estimated_time: "50–65 min"
technology: github-actions
category: github-actions
module: "Module 15 · Production Pipelines"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - github-actions
  - environments
  - progressive-delivery
  - approvals
prerequisites:
  - github-actions/composite-actions-and-reusable-workflows
next:
  - github-actions/troubleshooting-github-actions
related:
  - github-actions/kubernetes-deployments-with-github-actions
  - github-actions/security-scanning-and-supply-chain
labs: []
projects: []
interview: interview/github-actions
certifications:
  - GitHub Actions
  - GitHub Administration
tags:
  - github-actions
  - production
  - environments
  - progressive-delivery
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Production Pipelines and Environments

## Overview




Design environment promotion (dev → staging → production) with protected environments, required reviewers, rollback paths, and progressive delivery patterns (blue/green and canary).

Production CI/CD is controlled promotion of an **immutable artefact** through named **environments**, not “deploy on every push to main”. GitHub **Environments** encode wait timers, required reviewers, and environment secrets so only approved identities promote to production.

This is a core tutorial in **Module 15 · Production Pipelines** of the REBASH Academy **GitHub Actions for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites




- [Composite Actions and Reusable Workflows](composite-actions-and-reusable-workflows.md)
- Deploy awareness from Kubernetes or multi-cloud modules (or equivalent)



## Learning Objectives




By the end of this tutorial, you will be able to:

- [ ] Model env promotion with `environment:` and job `needs`  
- [ ] Protect production with required reviewers and deployment branches  
- [ ] Document rollback to a previous digest / release  
- [ ] Outline blue/green and canary versus all-at-once



## Architecture




This topic’s control points and relationships are shown below.

![Production pipelines](../assets/excalidraw/gha-production.svg)



## Theory




### What it is

A **production pipeline** promotes the same build (image digest, package version) across **environments** — logical targets such as `development`, `staging`, and `production`. In GitHub Actions, `jobs.<id>.environment` binds a job to an Environment that can require reviewers, restrict which branches may deploy, and hold environment-scoped secrets. **Progressive delivery** reduces blast radius: **blue/green** switches traffic between two complete stacks; **canary** sends a fraction of traffic to the new revision before full rollout. Feature flags (application-level) further decouple *deploy* from *release*.

| Control | Intent |
|---------|--------|
| Environment name | Track URL, history, protection rules |
| Required reviewers | Human promote / confirm |
| Deployment branches | Only `main` / release tags may deploy |
| Immutable artefact | Same SHA/digest every stage |
| Wait timer | Soak before production unlock |

### Why it matters

Auto-deploying every merge to production maximises speed and incident rate. Enterprises need auditable promotion: who approved, which digest is live, and how to roll back in minutes. Progressive delivery lets platform teams ship continuously while limiting blast radius — essential for multi-tenant cloud services and regulated workloads.

### How it works

1. **Build once** — tag image/package with commit SHA or SemVer; never rebuild for prod.  
2. **Deploy to non-prod** automatically after tests; run smoke checks.  
3. **Staging** — optional auto or short wait; acceptance tests against staging URLs.  
4. **Production** — job with `environment: production` and required reviewers; deploy the same digest.  
5. **Verify** — health checks, dashboards, error budgets; keep the previous revision ready.  
6. **Rollback** — redeploy previous digest / shift traffic / Helm rollback; keep a manual workflow job or runbook.  
7. **Progressive patterns** — blue/green cutover after smoke on green; canary ramp (mesh, Ingress weights, or cloud slots) with abort criteria.

Keep production secrets on the Environment — not in repository secrets shared with pull-request workflows. Prefer OpenID Connect (OIDC) roles scoped per environment.

### Key concepts and comparisons

| Pattern | Blast radius | Notes |
|---------|--------------|-------|
| All-at-once | High | Simple; largest risk |
| Blue/green | Medium | Cutover after green smoke |
| Canary | Low | Ramp traffic; define abort metrics |
| Feature flags | Behaviour | Decouple deploy from release |

**Continuous Delivery** keeps artefacts ready with a human gate; **Continuous Deployment** promotes automatically when green.

### Common pitfalls

- Rebuilding the image in production — digests diverge from staging.  
- Unprotected `production` — any writer can deploy.  
- Rollback untested until an outage — practice in staging.  
- Canary without abort metrics (error rate, latency).



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-github-actions/module-15/.github/workflows && cd ~/rebash-github-actions/module-15/.github/workflows
```

**Focus:** staging auto-deploy and production environment with concurrency gate

### Step 1 – Environment promotion workflow

```bash
mkdir -p .github/workflows
cat > .github/workflows/production.yml << 'EOF'
name: Production pipelines
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: prod-deploy
  cancel-in-progress: false
jobs:
  deploy_staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - run: echo "deploy staging"
  deploy_production:
    needs: deploy_staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - run: echo "production requires environment reviewers"
EOF
```

### Step 2 – Validate concurrency and environments

```bash
grep -E 'concurrency:|environment: production|needs: deploy_staging' .github/workflows/production.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials
```



## Validation




- [ ] Lab commands run under `~/rebash-github-actions/module-15/.github/workflows/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough




Production practice for **Production Pipelines and Environments** always combines:

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




!!! warning "Rebuilding the image in production — digests diverge from staging.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Unprotected `production` — any writer can deploy.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices




- Encode Production Pipelines and Environments changes as code and review them in pull requests
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




**Production Pipelines and Environments** is essential for Cloud and DevOps engineers working with github-actions. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. What protections do GitHub Environments provide?
2. Why use concurrency groups for production deploys?
3. How do you model staging then production promotion?
4. What evidence should a production deploy leave behind?
5. How do wait timers / reviewers change change management?

!!! tip "Sample answer — question 2"
    Check environment protection rules, required reviewers, and whether the job targeted the intended environment.

!!! tip "Sample answer — question 4"
    Store production secrets only on the production environment and require reviews.



## Related Tutorials




- [Course overview](index.md)
- [Troubleshooting GitHub Actions](troubleshooting-github-actions.md)



## References




- [Using environments for deployment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)  
- [Protected environments / reviewers](https://docs.github.com/en/actions/deployment/targeting-different-environments/managing-environments-for-deployment)  
- [Deployment best practices](https://docs.github.com/en/actions/deployment/about-deployments/deploying-with-github-actions)
