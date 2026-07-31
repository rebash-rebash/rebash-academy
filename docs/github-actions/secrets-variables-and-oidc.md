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

**Focus:** OIDC permissions workflow without embedding cloud keys

### Step 1 – OIDC workflow

{% raw %}
```bash
mkdir -p .github/workflows
cat > .github/workflows/oidc.yml << 'EOF'
name: oidc-deploy
on:
  workflow_dispatch:
permissions:
  id-token: write
  contents: read
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Configure cloud creds via OIDC
        run: echo "Use cloud-specific OIDC action; never echo secrets"
EOF
tee oidc-notes.txt << 'EOF'
permissions.id-token: write is required for OIDC. Bind GitHub subject claims to a least-privilege cloud role.
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/oidc.yml')); print('OK')"
cat oidc-notes.txt
```
{% endraw %}

### Final step – Cleanup note

```bash
# No cloud resources
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


1. How does **Secrets, Variables, and OIDC** fit into a GitHub Actions delivery model?
2. A workflow fails only on `pull_request` — what differences do you inspect?
3. Why pin Actions and limit `permissions`?
4. How should production secrets and OIDC cloud access be designed?
5. How do you keep workflows reusable without copy-paste sprawl?

!!! tip "Sample answer — question 2"
    Compare event payloads, checkout ref for fork PRs, secrets availability, and required environments. Read the failing step log and re-run with debug logging if needed.

!!! tip "Sample answer — question 4"
    Use `permissions` least privilege, environment protection for prod, and OIDC (`id-token: write`) instead of long-lived cloud keys.



## Related Tutorials



- [Course overview](index.md)
- [Artifacts and Caching](artifacts-and-caching.md)



## References



- [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)  
- [Variables](https://docs.github.com/en/actions/learn-github-actions/variables)  
- [About security hardening with OpenID Connect](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
