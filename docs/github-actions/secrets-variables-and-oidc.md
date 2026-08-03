---
title: "Secrets, Variables, and OIDC"
description: "Configure repository, environment, and organisation secrets; use variables for non-sensitive config; sketch OIDC trust policies for cloud authentication without long-lived keys."
difficulty: intermediate
estimated_time: "55–65 min"
technology: github-actions
category: github-actions
module: "Module 5 · Secrets & Variables"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - devsecops-engineer
skills:
  - github-actions
  - secrets
  - oidc
  - security
prerequisites:
  - github-actions/workflow-syntax-matrix-and-reusable
next:
  - github-actions/artifacts-and-caching
related:
  - github-actions/multi-cloud-deployments-with-github-actions
  - github-actions/security-scanning-and-supply-chain
tags:
  - github-actions
  - secrets
  - oidc
  - variables
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---

# Secrets, Variables, and OIDC

## Overview

Pipelines need credentials — registry passwords, API tokens, cloud role assumptions. Storing them in workflow YAML is an instant incident. GitHub provides **secrets** (encrypted, masked in logs) and **variables** (non-sensitive configuration). **OpenID Connect (OIDC)** goes further: workflows exchange a short-lived token with AWS, Azure, or Google Cloud — no static access keys in GitHub at all.

This module maps the secrets hierarchy (repository → environment → organisation), shows safe reference patterns in workflows, and sketches an OIDC trust policy you can validate offline.

This is **Tutorial 5** in **Module 5: Secrets & Variables** of the REBASH Academy **GitHub Actions for Cloud & DevOps Engineers** series.

## Prerequisites

- [Workflow Syntax: Matrix and Reusable Workflows](workflow-syntax-matrix-and-reusable.md)
- Basic cloud Identity and Access Management (IAM) concepts
- Python 3 with PyYAML

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Choose repository, environment, and organisation secrets appropriately
- [ ] Use `vars` for non-sensitive configuration in workflows
- [ ] Reference secrets in jobs without leaking them in logs
- [ ] Sketch an OIDC trust relationship between GitHub and a cloud provider
- [ ] Validate workflow permission blocks required for OIDC (`id-token: write`)

## Architecture

Secrets and variables flow from GitHub settings into job environments; OIDC exchanges a JWT for cloud credentials at runtime.

![GitHub Actions secrets, variables, and OIDC](../assets/excalidraw/gha-secrets-oidc.svg)

## Theory

### What it is

**Secrets** store sensitive values — API keys, passwords, private tokens. GitHub encrypts them at rest and masks known secret values in logs when possible. Reference in workflows:

{% raw %}
```yaml
env:
  REGISTRY_TOKEN: ${{ secrets.GHCR_TOKEN }}
```
{% endraw %}

**Variables** store non-sensitive configuration — region names, account IDs, feature toggles:

{% raw %}
```yaml
env:
  AWS_REGION: ${{ vars.AWS_REGION }}
```
{% endraw %}

**Hierarchy (most specific wins where applicable):**

| Level | Scope | Typical content |
|-------|-------|-----------------|
| Repository secret | One repo | Repo-specific deploy token |
| Environment secret | Repo + named environment | Production kubeconfig reference |
| Organisation secret | Many repos | Shared read-only package token |
| Repository / org variable | Same scopes | Region, cluster name, URL |

**Environments** (`production`, `staging`) add optional protection rules — required reviewers, wait timers, deployment branches — and environment-scoped secrets.

**OIDC** lets GitHub Actions mint a short-lived JSON Web Token (JWT) identifying the repository, ref, and environment. Cloud providers trust GitHub as an identity provider and exchange the JWT for temporary credentials.

### Why it matters

Long-lived cloud access keys in GitHub Secrets rotate poorly and leak through logs, forks, and compromised actions. OIDC binds credentials to a **specific workflow run** — the cloud session expires quickly and includes auditable claims (`sub`, `repository`, `ref`).

Regulated environments require evidence that production credentials cannot be used from feature branches. Environment protection plus OIDC condition keys (`StringEquals` on `sub` or `aud`) enforce that policy in cloud IAM — not just in YAML comments.

### How it works

**Referencing secrets safely:**

{% raw %}
```yaml
permissions:
  contents: read
jobs:
  deploy:
    environment: production
    runs-on: ubuntu-latest
    steps:
      - name: Use secret (never echo)
        env:
          TOKEN: ${{ secrets.DEPLOY_TOKEN }}
        run: |
          set -euo pipefail
          # Use $TOKEN via tool flags — never print
          curl -sf -H "Authorization: Bearer ${TOKEN}" "$URL/status" > /dev/null
```
{% endraw %}

**OIDC to AWS (conceptual flow):**

1. Workflow sets `permissions: id-token: write`.
2. Step uses `aws-actions/configure-aws-credentials` with `role-to-assume` — no access key inputs.
3. GitHub issues OIDC JWT; AWS Security Token Service (STS) validates trust policy; returns temporary credentials.

**AWS trust policy sketch (offline — no real account IDs required in lab):**

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com" },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
      },
      "StringLike": {
        "token.actions.githubusercontent.com:sub": "repo:ORG/REPO:ref:refs/heads/main"
      }
    }
  }]
}
```

Replace `ORG/REPO` and tighten `sub` for environment-based deploys (`environment:production` in subject).

### Key concepts and comparisons

| Store | Sensitive? | Masked in logs? | Rotation |
|-------|------------|-----------------|----------|
| Secret | Yes | Attempted | Manual or automation |
| Variable | No | No | Edit in Settings |
| OIDC role | N/A (temporary) | N/A | Automatic expiry |

| Auth method | Risk profile |
|-------------|--------------|
| Long-lived access key in secret | High — broad blast radius |
| OIDC role assumption | Lower — scoped, short-lived |
| Environment secret + approval | Medium — gated human review |

### Common pitfalls

- Printing secrets — base64 encoding or JSON wrapping does not bypass masking reliably; exfiltration still possible.
- Fork pull requests receiving secrets — default deny for forks; never use `pull_request_target` to “fix” without security review.
- Missing `id-token: write` — OIDC steps fail silently or with opaque errors.
- Over-broad trust policy (`repo:*/*`) — any repository in the org assumes production role.
- Storing non-sensitive data as secrets — makes debugging harder; use variables.

## Hands-on Lab

### Objective

Encode the secrets hierarchy as YAML, write workflows referencing secrets and variables safely, and produce an OIDC trust policy sketch validated offline under `~/rebash-github-actions/module-05`.

### Prerequisites

- Modules 1–4
- Python 3 with PyYAML

### Lab environment

```bash title="Terminal"
mkdir -p ~/rebash-github-actions/module-05/.github/workflows ~/rebash-github-actions/module-05/oidc && cd ~/rebash-github-actions/module-05
set -euo pipefail
```

### Real-world scenario

Security review blocked deploy workflows until you encode where secrets live, prove logs will not echo tokens, and show an OIDC trust policy scoped to `main` — no long-lived AWS keys in GitHub.

### Step-by-step tasks

#### Task 1 – Encode secrets hierarchy

Create `secrets-hierarchy.yaml`:

```yaml title="secrets-hierarchy.yaml"
# Secrets and variables hierarchy
levels:
  - scope: repository_secret
    example: SLACK_WEBHOOK
    use_case: Repo-specific notifications
  - scope: environment_secret
    example: KUBE_CONFIG_PROD
    use_case: Production deploy only
  - scope: organisation_secret
    example: SHARED_READ_TOKEN
    use_case: Read packages across repos
  - scope: repository_variable
    example: AWS_REGION
    use_case: Non-sensitive region config
  - scope: organisation_variable
    example: COMPANY_DOMAIN
    use_case: Shared DNS suffix
rules:
  - id: no-commit
    rule: Never commit secrets — use Settings or sealed automation
  - id: no-echo
    rule: Never echo secrets in run steps or artefact names
  - id: env-prod
    rule: Production secrets live in environment production only
  - id: prefer-oidc
    rule: Prefer OIDC over static cloud keys for AWS, Azure, and GCP
```

Validate offline:

```bash title="Terminal"
cd ~/rebash-github-actions/module-05
set -euo pipefail
python3 -c "
import yaml
with open('secrets-hierarchy.yaml') as f:
    doc = yaml.safe_load(f)
scopes = {l['scope'] for l in doc['levels']}
assert 'environment_secret' in scopes
assert any('OIDC' in r['rule'] for r in doc['rules'])
print('secrets-hierarchy.yaml OK')
"
```

!!! example "Expected output"
    `secrets-hierarchy.yaml OK`


#### Task 2 – Workflow with vars and secret references (stub values)

Create `.github/workflows/deploy-with-secrets.yml`:

{% raw %}
```yaml
name: Deploy with secrets stub
on:
  workflow_dispatch:
permissions:
  contents: read
  id-token: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: staging
    env:
      AWS_REGION: ${{ vars.AWS_REGION }}
    steps:
      - uses: actions/checkout@v4
      - name: Validate config without printing secrets
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
        run: |
          set -euo pipefail
          test -n "${AWS_REGION:-us-east-1}" || AWS_REGION=us-east-1
          echo "region=${AWS_REGION}" > config.txt
          test -n "${DEPLOY_TOKEN:-stub-token-for-offline-lab}" 
          echo "token-present=yes" >> config.txt
          grep -q 'token-present=yes' config.txt
          # NEVER: echo "$DEPLOY_TOKEN"
```
{% endraw %}

Validate offline:

```bash title="Terminal"
cd ~/rebash-github-actions/module-05
set -euo pipefail
grep -q 'vars.AWS_REGION' .github/workflows/deploy-with-secrets.yml
grep -q 'secrets.DEPLOY_TOKEN' .github/workflows/deploy-with-secrets.yml
grep -q 'id-token: write' .github/workflows/deploy-with-secrets.yml
python3 -c "import yaml; d=yaml.safe_load(open('.github/workflows/deploy-with-secrets.yml')); assert d['permissions']['id-token']=='write'; print('secrets workflow OK')"
```

!!! example "Expected output"
    `secrets workflow OK`


#### Task 3 – OIDC trust policy sketch

Create `oidc/aws-trust-policy.json`:

```json title="aws-trust-policy.json"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "GitHubActionsOIDC",
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:rebash-academy/demo-app:ref:refs/heads/main"
        }
      }
    }
  ]
}
```

Validate offline:

```bash title="Terminal"
cd ~/rebash-github-actions/module-05
set -euo pipefail
python3 -c "import json; d=json.load(open('oidc/aws-trust-policy.json')); assert d['Statement'][0]['Action']=='sts:AssumeRoleWithWebIdentity'; print('trust policy JSON OK')"
grep -q 'token.actions.githubusercontent.com' oidc/aws-trust-policy.json
```

!!! example "Expected output"
    `trust policy JSON OK`


#### Task 4 – Simulate offline deploy check and archive

```bash title="Terminal"
cd ~/rebash-github-actions/module-05
set -euo pipefail

AWS_REGION=us-east-1
echo "region=${AWS_REGION}" > config.txt
echo "token-present=yes" >> config.txt
grep -q 'token-present=yes' config.txt
grep -q 'region=us-east-1' config.txt

tar -czf module-05-evidence.tgz secrets-hierarchy.yaml .github/workflows/deploy-with-secrets.yml oidc/aws-trust-policy.json config.txt
ls -l module-05-evidence.tgz | tee evidence.txt
```

!!! example "Expected output"
    Tarball created.


**Optional — configure OIDC on AWS:**

Use [GitHub docs](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) and `aws-actions/configure-aws-credentials@v4` with your role ARN — no access keys stored.

### Validation steps

- [ ] `secrets-hierarchy.yaml` covers repo, environment, and org levels and parses with Python
- [ ] Workflow sets `id-token: write` for OIDC readiness
- [ ] Workflow references `vars.*` and `secrets.*` without echo
- [ ] Trust policy JSON parses and scopes `sub` to a repository ref
- [ ] Offline simulation writes `config.txt` evidence

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| OIDC step fails | Missing `id-token: write` | Add under `permissions:` |
| Secret empty in fork PR | Expected security behaviour | Use environments + internal PRs only |
| Trust policy too broad | Wildcard `sub` | Restrict to `repo:ORG/REPO:environment:production` |
| Variable not found | Not defined in Settings | Provide default in lab shell; define in repo for live runs |

### Challenge exercise

Add an `environments/production.yaml` stub listing three required reviewers and a workflow job that only runs when `github.ref == 'refs/heads/main'` **and** `environment: production`. Validate YAML parses.

### Learning outcomes

- Mapped secrets versus variables across hierarchy levels
- Wrote workflow referencing secrets without log exposure
- Produced OIDC trust policy sketch scoped to repository and branch
- Confirmed `id-token: write` permission requirement

### Cleanup

```bash
# Retain module-05 — remove stub tokens from shell history if any
```

## Validation

- [ ] Lab completed under `~/rebash-github-actions/module-05/`
- [ ] You can explain why OIDC beats long-lived access keys
- [ ] You can name three places secrets can be stored in GitHub
- [ ] You can describe fork PR secret isolation

## Code Walkthrough

1. **Classify data** — secret versus variable before storing.
2. **Scope narrowly** — environment secrets for production; org secrets only when truly shared.
3. **OIDC first** — cloud modules assume role, not key.
4. **Permissions** — `id-token: write` only on jobs that need federation.
5. **Audit** — log who deployed via cloud trail; GitHub environments record approvals.

## Security Considerations

- Never print secrets; avoid passing secrets as command-line args visible in `ps`.
- Restrict OIDC trust `sub` to specific repositories, refs, or environments.
- Rotate compromised secrets immediately; prefer OIDC to reduce rotation toil.
- Use environment protection rules for production — required reviewers and branch limits.
- Audit organisation secret visibility — which repositories can read each secret.

## Common Mistakes

!!! warning "Echoing secrets in debug output"
    `echo "$TOKEN"` or `set -x` exposes credentials. **Fix:** Use masked env vars; disable xtrace; pass via stdin or secret files.

!!! warning "Trust policy allowing any repository"
    `"sub": "repo:*/*:*"` lets any repo in the org assume the role. **Fix:** Pin `repo:ORG/REPO:ref:refs/heads/main` or environment-specific subjects.

!!! warning "Using pull_request_target to expose secrets to forks"
    Runs in base repo context with secrets — dangerous with untrusted code. **Fix:** Avoid unless maintainers fully control checkout ref and commands.

## Best Practices

- Separate staging and production secrets by environment name.
- Use organisation variables for shared non-sensitive defaults (region, domain).
- Document OIDC role mapping in a central security runbook.
- Automate secret rotation with External Secrets Operator where possible.
- Test trust policies in a sandbox account before production IAM update.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `Not authorized to perform sts:AssumeRoleWithWebIdentity` | Trust policy mismatch | Align `sub`, `aud`, and provider ARN |
| Secret shows empty | Wrong scope or fork PR | Check environment; verify secret name spelling |
| Variable not substituted | Name typo or org vs repo level | Confirm `vars.NAME` exists at expected level |
| OIDC token missing | Permissions or old action version | Add `id-token: write`; update credential action |
| Masked secret still leaked | Encoded or split across outputs | Never transform secrets into logs or artefacts |

## Summary

**Secrets** and **variables** separate sensitive credentials from configuration; **environments** gate production access; **OIDC** eliminates long-lived cloud keys. Module 5’s lab documents hierarchy and trust policy sketches you can refine in cloud modules. Next: [Artifacts and Caching](artifacts-and-caching.md).

## Interview Questions

**1. What is the difference between a repository secret and an environment secret?**

??? success "Reveal answer"
    A **repository secret** is available to workflows in that repository (subject to branch and fork rules). An **environment secret** is scoped to a named environment (`staging`, `production`) and only exposed when a job declares `environment: production`, enabling protection rules and separate credential pools per stage.

**2. Why prefer OIDC over storing AWS access keys in GitHub Secrets?**

??? success "Reveal answer"
    OIDC provides **short-lived** credentials tied to a specific workflow run with auditable claims. Access keys are long-lived, rotate manually, and grant broad access if leaked. OIDC trust policies restrict which repositories and refs can assume a role — shrinking blast radius.

**3. What permission does a job need to request an OIDC token?**

??? success "Reveal answer"
    `permissions: id-token: write` at workflow or job level. Without it, GitHub does not mint the JWT for federation steps such as `aws-actions/configure-aws-credentials` or `google-github-actions/auth`.

**4. How should you reference a secret in a shell step without leaking it?**

??? success "Reveal answer"
    Map to an environment variable via `env: TOKEN: {% raw %}${{ secrets.NAME }}{% endraw %}` and use the variable in tool flags or stdin — never `echo`, `printf`, or artefact upload of the value. Avoid `set -x` while the secret is in scope.

**5. When would you use an organisation secret versus a repository secret?**

??? success "Reveal answer"
    Organisation secrets when many repositories need the same credential (read-only package registry, shared Slack webhook) and InfoSec approves shared access. Repository secrets when blast radius must stay isolated to one service. Environment secrets when only production deploy jobs should access production credentials.

**6. Explain a trust policy condition on token.actions.githubusercontent.com:sub.**

??? success "Reveal answer"
    The `sub` claim identifies the GitHub subject — typically `repo:ORG/REPO:ref:refs/heads/main` or `repo:ORG/REPO:environment:production`. IAM `StringLike` or `StringEquals` conditions ensure only matching workflow runs can assume the cloud role — preventing feature-branch workflows from gaining production access.

**7. Why are secrets not available to workflows from fork pull requests?**

??? success "Reveal answer"
    External contributors could exfiltrate secrets through malicious workflow code. GitHub withholds secrets on fork PR workflows by default. Maintainers must use manual approval workflows or run CI without secrets for untrusted forks.

## Related Tutorials

- [Workflow Syntax: Matrix and Reusable Workflows](workflow-syntax-matrix-and-reusable.md)
- [Artifacts and Caching](artifacts-and-caching.md)
- [Multi-Cloud Deployments with GitHub Actions](multi-cloud-deployments-with-github-actions.md)

## References

- [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- [Variables](https://docs.github.com/en/actions/learn-github-actions/variables)
- [OpenID Connect](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [Configuring OIDC in AWS](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
