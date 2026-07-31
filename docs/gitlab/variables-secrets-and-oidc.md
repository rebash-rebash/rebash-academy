---
title: "Variables, Secrets, and OIDC"
description: "Manage GitLab CI variables (masked, protected), environment scoping, Vault-style patterns, and OIDC federation to cloud providers."
difficulty: intermediate
estimated_time: "40–55 min"
technology: gitlab
category: gitlab
module: "Module 6 · Variables & Secrets"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - gitlab-ci
  - secrets
  - oidc
prerequisites:
  - gitlab/pipeline-design-dags-and-includes
next:
  - gitlab/artifacts-caches-and-dependencies
related:
  - gitlab/security-scanning-and-devsecops
  - terraform/terraform-security-and-secrets
labs: []
projects: []
interview: interview/gitlab
certifications:
  - GitLab Certified CI/CD Associate
tags:
  - gitlab
  - secrets
  - oidc
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Variables, Secrets, and OIDC

## Overview

Use CI/CD variables correctly (masked, protected, environment-scoped), avoid long-lived cloud keys where possible, and outline OIDC and Vault-style secret patterns for production.

Pipelines need configuration and credentials. GitLab provides **CI/CD variables** at project, group, and instance levels, plus predefined `$CI_*` variables. Production teams prefer **short-lived cloud credentials via OpenID Connect (OIDC)** and external secret managers over static keys in the UI.

This is a core tutorial in **Module 6 · Variables & Secrets** of the REBASH Academy **GitLab CI/CD for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Pipeline Design: DAGs and Includes](pipeline-design-dags-and-includes.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Choose YAML vs UI variables for non-secret config  
- [ ] Apply masked and protected variable flags correctly  
- [ ] Scope variables to environments  
- [ ] Describe OIDC to AWS/GCP/Azure and Vault-style fetch patterns

## Architecture

This topic’s control points and relationships are shown below.

![Variables and secrets](../assets/excalidraw/gitlab-variables-secrets.svg)

## Theory

### What it is

**CI/CD variables** become environment variables in the job. Sources: predefined (`$CI_JOB_TOKEN`, `$CI_REGISTRY`, …), `.gitlab-ci.yml` `variables:`, and UI/API variables (optionally **masked**, **protected**, **expanded**, environment-scoped). **Masked** variables are redacted from job logs when they match masking rules. **Protected** variables are only available on protected branches and tags. **Environments** (`environment:name`) further scope deploy-time secrets.

**OIDC** lets GitLab mint a JWT for the job; the cloud provider trusts that JWT and returns temporary credentials — no static access key in GitLab. **Vault** (or cloud secret stores) patterns fetch secrets at job start using that identity or an authenticated agent.

### Why it matters

Leaked long-lived keys are a top CI breach path. Feature-branch jobs that see production secrets violate least privilege. Masking is not encryption — it is log hygiene. Platform and DevSecOps standards: non-secrets in YAML, secrets in protected UI vars or external managers, cloud access via OIDC roles tied to `project_path` / `ref` claims.

### How it works

1. Prefer `$CI_*` and UI/project variables for non-secret config (`AWS_REGION`, image names).
2. Store secrets in the GitLab UI (or external store); mark **protected** and **masked** when compatible.
3. Restrict deploy jobs with `rules` + `environment` so only protected refs see production scopes.
4. For cloud: trust GitLab as an OIDC IdP; jobs mint a JWT via `id_tokens`; STS / Workload Identity returns temporary creds.
5. For Vault: login with JWT/OIDC, fetch, use — never `echo` secrets.

No paid GitLab or live cloud account is required to author the YAML; enable OIDC in a sandbox when ready.

### Key concepts and comparisons

| Mechanism | Good for | Limit |
|-----------|----------|--------|
| YAML `variables` | Non-secret defaults | Visible in Git |
| UI variable (masked) | Simple secrets | Masking rules; still stored in GitLab |
| Protected + environment | Production deploy secrets | Unprotected branches cannot read |
| OIDC to cloud | Temporary cloud API access | Needs cloud IdP config |
| Vault / secret manager | Central rotation, dynamic secrets | Extra runtime dependency |

| Anti-pattern | Prefer |
|--------------|--------|
| Cloud access keys in YAML | OIDC role assumption |
| Same secret on all branches | Protected + environment scope |
| `echo $SECRET` for debugging | Job traces with masking; short-lived tokens |

### Common pitfalls

- Believing masked variables cannot be exfiltrated — a malicious job can still send them outbound.
- Unprotected runners + protected variables — understand runner privilege models.
- Forgetting `id_tokens` / audience config when migrating to OIDC.
- Storing entire `.env` files as a single variable without rotation owners.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-gitlab/module-06 && cd ~/rebash-gitlab/module-06
```

**Focus:** hands-on practice for Variables, Secrets, and OIDC

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Variables, Secrets, and OIDC"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-gitlab/module-06
cd ~/rebash-gitlab/module-06
```

```bash
cd ~/rebash-gitlab/module-06
cat > .gitlab-ci.yml << 'EOF'
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

stages: [verify, deploy]

variables:
  APP_ENV: "ci"
  # Non-secrets only in YAML. Create MASKED_DEMO in project CI/CD settings (optional).

show_predefined:
  stage: verify
  image: alpine:3.20
  script:
    - echo "Project=$CI_PROJECT_PATH ref=$CI_COMMIT_REF_NAME protected=$CI_COMMIT_REF_PROTECTED"
    - echo "APP_ENV=$APP_ENV (do not echo secrets)"
    - test -z "${MASKED_DEMO:-}" && echo "Optional: set masked MASKED_DEMO in UI" || echo "MASKED_DEMO is set"

oidc_ready_deploy:
  stage: deploy
  image: alpine:3.20
  id_tokens:
    GITLAB_OIDC_TOKEN:
      aud: https://gitlab.com
  environment:
    name: staging
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
  script:
    - echo "OIDC JWT received — exchange via STS / Workload Identity / Vault JWT auth"
EOF

python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml')); print('YAML parse OK')"
# Optional: glab ci lint .gitlab-ci.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-gitlab/module-06/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Variables, Secrets, and OIDC** always combines:

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

!!! warning "Believing masked variables cannot be exfiltrated — a malicious job can still send them out"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Unprotected runners + protected variables — understand runner privilege models."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Variables, Secrets, and OIDC changes as code and review them in pull requests
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

**Variables, Secrets, and OIDC** is essential for Cloud and DevOps engineers working with gitlab. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Variables, Secrets, and OIDC** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Artifacts, Caches, and Dependencies](artifacts-caches-and-dependencies.md)

## References

- [CI/CD variables](https://docs.gitlab.com/ee/ci/variables/)  
- [OIDC with GitLab CI/CD](https://docs.gitlab.com/ee/ci/cloud_services/)
