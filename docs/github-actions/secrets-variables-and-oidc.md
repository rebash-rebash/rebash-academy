---
title: "Secrets, Variables, and OIDC"
description: "Manage repository, environment, and organisation secrets and variables, and authenticate to cloud with OpenID Connect (OIDC)."
difficulty: intermediate
estimated_time: "45–60 min"
technology: github-actions
category: github-actions
module: "Module 5 · Secrets & Variables"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - github-actions
  - secrets
  - oidc
prerequisites:
  - github-actions/workflow-syntax-matrix-and-reusable
next:
  - github-actions/artifacts-and-caching
related:
  - github-actions/security-scanning-and-supply-chain
  - terraform/terraform-security-and-secrets
labs: []
projects: []
interview: interview/github-actions
certifications:
  - GitHub Actions
tags:
  - github-actions
  - secrets
  - oidc
  - variables
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Secrets, Variables, and OIDC

## Overview

Place non-secret configuration in variables, scope secrets correctly (repository, environment, organisation), and outline OpenID Connect (OIDC) so jobs obtain short-lived cloud credentials without long-lived access keys.

Pipelines need configuration and credentials. GitHub provides **configuration variables** (`vars.*`) and **secrets** (`secrets.*`) at repository, organisation, and **environment** scopes. Production Cloud and DevOps teams prefer **OIDC federation** to AWS, Azure, or Google Cloud: GitHub mints a JWT for the job; the cloud trusts that JWT and returns temporary credentials. That removes static keys from the Actions UI.

This is a core tutorial in **Module 5 · Secrets & Variables** of the REBASH Academy **GitHub Actions for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Workflow Syntax: Matrix and Reusable Workflows](workflow-syntax-matrix-and-reusable.md)
- Optional: an AWS, Azure, or Google Cloud sandbox for a live OIDC exchange later

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Choose `vars` vs `secrets` vs YAML `env` for a setting  
- [ ] Scope secrets to repository, organisation, and environments  
- [ ] Restrict deploy jobs with `environment:` and protection rules  
- [ ] Describe OIDC trust (issuer, subject, audience) to a cloud role  
- [ ] Request `id-token: write` only when federating

## Architecture

This topic’s control points and relationships are shown below.

![Secrets and OIDC](../assets/excalidraw/gha-secrets-oidc.svg)

## Theory

### What it is

**Variables** are non-secret key/value pairs you set in the GitHub UI (or via API) and read as {% raw %}`${{ vars.NAME }}`{% endraw %}. They suit regions, image names, and feature flags you are willing to show in logs. **Secrets** are encrypted values injected as {% raw %}`${{ secrets.NAME }}`{% endraw %} (and often mapped into `env:` for tools that expect environment variables). GitHub redacts secret values that appear in logs when they match known secret strings — redaction is **log hygiene**, not a security boundary against a malicious workflow.

Scopes:

| Scope | Typical use |
|-------|-------------|
| Repository | App-specific tokens for that repo |
| Organisation | Shared non-prod tooling credentials (limit carefully) |
| Environment (`environment: production`) | Deploy secrets + required reviewers / wait timers |

**Environments** attach protection rules: required reviewers, wait timers, and branch restrictions. A job that declares `environment: production` only receives that environment’s secrets after gates pass.

**OIDC** (OpenID Connect) replaces long-lived cloud keys. You grant `permissions: id-token: write`, the job requests a JWT, and a cloud-specific action (for example `aws-actions/configure-aws-credentials`) exchanges it for temporary credentials. Trust policies bind claims such as `sub` (repository, ref, environment) so a feature-branch job cannot assume the production role.

### Why it matters

Leaked long-lived keys in CI are a top breach path. Feature-branch jobs that see production database passwords violate least privilege. Organisation-wide secrets amplify blast radius when any repo can run arbitrary workflow code. OIDC plus environment-scoped secrets is the modern baseline for DevSecOps: non-secrets in `vars` or YAML, secrets narrowly scoped, cloud access via short-lived tokens tied to `repo:ref:environment` claims. Auditors can reason about *who could have deployed* from workflow history and cloud CloudTrail / Activity logs together.

### How it works

1. Prefer YAML `env:` and `vars.*` for non-secret config (`AWS_REGION`, chart name).
2. Store secrets in the UI at the narrowest scope that works; prefer environment secrets for production deploys.
3. Mark production jobs with `environment:` and enable protection rules on that environment.
4. For cloud API access: create an identity provider trust for `token.actions.githubusercontent.com`, map subject conditions, and grant the job `id-token: write` with minimal other permissions.
5. Exchange the JWT at job start; use credentials; never `echo` them; rely on token expiry.

You can author the workflow without a live cloud account — the OIDC job demonstrates permissions and structure. Wire the cloud role when you have a sandbox.

### Key concepts and comparisons

| Mechanism | Good for | Limit |
|-----------|----------|--------|
| YAML `env` | Defaults in Git | Visible to all readers |
| `vars.*` | Non-secret ops knobs | Not for passwords |
| Repo secret | Simple integrations | Available to all workflows in repo |
| Environment secret | Production deploys | Needs `environment:` on the job |
| Org secret | Shared platform tooling | Broad blast radius if overused |
| OIDC to cloud | Temporary cloud API access | Needs cloud IdP + claim conditions |

| Anti-pattern | Prefer |
|--------------|--------|
| `AWS_ACCESS_KEY_ID` in repo secrets forever | OIDC role assumption |
| Same production secret on all branches | Environment + protected branches |
| {% raw %}`echo ${{ secrets.X }}`{% endraw %} for debugging | Masked logs; temporary elevated support access |

### Common pitfalls

- Believing redaction means secrets cannot leave the job — malicious steps can still exfiltrate over the network.
- Forgetting `id-token: write` (and overly broad `permissions: write-all` as a “fix”).
- Trusting `pull_request_target` with secrets — a separate, dangerous pattern; avoid until you study it carefully.
- Organisation secrets available to all repositories including forks of public templates without review.
- Storing entire `.env` files as one secret with no rotation owner.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-github-actions/module-05/.github/workflows && cd ~/rebash-github-actions/module-05/.github/workflows
```

**Focus:** hands-on practice for Secrets, Variables, and OIDC

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-github-actions/module-05/.github/workflows
cd ~/rebash-github-actions/module-05
```

Set optional repository variables/secrets in the GitHub UI (`DEMO_REGION` as a variable). Do not put real production credentials in learning repos.

```bash
cd ~/rebash-github-actions/module-05
cat > oidc-checklist.md << 'EOF'
- [ ] vars for non-secrets
- [ ] environment: staging|production for deploy secrets
- [ ] permissions: contents: read, id-token: write (OIDC jobs)
- [ ] cloud trust on sub claim (repo + ref + environment)
EOF
```

{% raw %}
```yaml
# .github/workflows/secrets-and-oidc.yml
name: Module 5 secrets and OIDC

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  show-config:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Non-secret configuration
        env:
          DEMO_REGION: ${{ vars.DEMO_REGION }}
        run: |
          test -f oidc-checklist.md
          echo "DEMO_REGION=${DEMO_REGION:-unset-set-vars.DEMO_REGION-in-UI}"
          echo "Do not print secrets"

  staging-shape:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    permissions:
      contents: read
      id-token: write
    steps:
      - name: OIDC-ready placeholder
        run: |
          echo "Add aws-actions/configure-aws-credentials (or Azure/GCP equivalent) here"
          echo "Job has id-token: write for federation"
          # Example (enable when cloud trust exists):
          # - uses: aws-actions/configure-aws-credentials@v4
          #   with:
          #     role-to-assume: arn:aws:iam::123456789012:role/gha-staging
          #     aws-region: eu-west-1
```
{% endraw %}

```bash
# Create GitHub Environment named "staging" (Settings → Environments)
# Optional: gh secret set — never commit secret values
# gh variable set DEMO_REGION --body "eu-west-1"
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-github-actions/module-05/.github/workflows/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Secrets, Variables, and OIDC** always combines:

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

!!! warning "Believing redaction means secrets cannot leave the job — malicious steps can still exfiltr"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Forgetting `id-token: write` (and overly broad `permissions: write-all` as a “fix”)."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Secrets, Variables, and OIDC changes as code and review them in pull requests
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

**Secrets, Variables, and OIDC** is essential for Cloud and DevOps engineers working with github-actions. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Secrets, Variables, and OIDC** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Artifacts and Caching](artifacts-and-caching.md)

## References

- [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)  
- [Variables](https://docs.github.com/en/actions/learn-github-actions/variables)  
- [About security hardening with OpenID Connect](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
