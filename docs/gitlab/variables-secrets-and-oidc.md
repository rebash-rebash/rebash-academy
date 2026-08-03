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
last_updated: "2026-08-03"
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

### Objective

Separate non-secret CI variables from masked secret placeholders in `.gitlab-ci.yml`, document OIDC trust configuration in `oidc-notes.yaml`, and validate that no real secrets appear in the repository.

### Prerequisites

- Python 3 with PyYAML (`pip install pyyaml`)
- Optional: GitLab project with masked/protected variables configured in the UI

### Lab environment

Workspace: `~/rebash-gitlab/module-06`

File-first lab. Never commit real tokens — use placeholders only.

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-gitlab/module-06 && cd ~/rebash-gitlab/module-06
```

### Real-world scenario

Security review flagged cloud access keys committed in YAML. You refactor the pipeline to keep configuration in file variables, reference secrets via GitLab UI placeholders, and capture OIDC trust settings in machine-readable YAML for the cloud team — without storing credentials in Git.

### Step-by-step tasks

#### Task 1 – Author CI with file vars and secret placeholders

Create `src/deploy_check.py`:

```python title="deploy_check.py"
import os
print("region", os.environ.get("AWS_REGION", "unset"))
print("deploy ok")
```

Create `.gitlab-ci.yml`:

```yaml title=".gitlab-ci.yml"
variables:
  AWS_REGION: ap-south-1
  APP_ENV: staging
  # Non-secret defaults only — never put real keys here

stages:
  - validate
  - deploy

validate_config:
  stage: validate
  image: python:3.12-alpine
  script:
    - test -n "$AWS_REGION"
    - test "$APP_ENV" = "staging"
    - python -m py_compile src/deploy_check.py

deploy_staging:
  stage: deploy
  image: python:3.12-alpine
  environment:
    name: staging
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  variables:
    # Set in GitLab UI: masked + protected
    DB_PASSWORD: "$DB_PASSWORD"
  script:
    - test -n "$DB_PASSWORD"
    - python src/deploy_check.py
  # Production deploy would use id_tokens + cloud OIDC — see oidc-notes.yaml
```

Validate offline:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-gitlab/module-06
python3 -c "
import yaml
d = yaml.safe_load(open('.gitlab-ci.yml'))
assert d['variables']['AWS_REGION'] == 'ap-south-1'
assert 'AKIA' not in open('.gitlab-ci.yml').read()
print('OK no static keys in YAML')
"
```

!!! example "Expected output"
    Prints `OK no static keys in YAML`.


#### Task 2 – Document OIDC trust configuration

Create `oidc-notes.yaml` — machine-readable notes for the cloud administrator:

```yaml
oidc_provider:
  gitlab_url: https://gitlab.com
  audience: https://gitlab.com
aws_role_trust_example:
  provider: aws
  role_arn: arn:aws:iam::123456789012:role/gitlab-ci-staging
  trust_condition:
    StringEquals:
      gitlab.com:sub: project_path:my-group/rebash-gitlab-module-06:ref_type:branch:ref:main
  job_config:
    id_token_name: GITLAB_OIDC_TOKEN
    cloud_command: aws sts assume-role-with-web-identity
secret_handling:
  never_in_git:
    - long_lived_access_keys
    - database_passwords
  gitlab_ui_only:
    - name: DB_PASSWORD
      masked: true
      protected: true
      environment_scope: staging
local_simulation:
  export_placeholder: export DB_PASSWORD='replace-in-ui-not-git'
```

Validate:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-gitlab/module-06
python3 -c "
import yaml
o = yaml.safe_load(open('oidc-notes.yaml'))
assert o['secret_handling']['gitlab_ui_only'][0]['name'] == 'DB_PASSWORD'
assert 'never_in_git' in o['secret_handling']
print('OK oidc-notes', o['oidc_provider']['audience'])
"
```

!!! example "Expected output"
    Prints `OK oidc-notes https://gitlab.com`.


#### Task 3 – Simulate staging deploy with a local placeholder

Prove the script path without a real secret:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-gitlab/module-06
export AWS_REGION=ap-south-1
export APP_ENV=staging
export DB_PASSWORD='lab-placeholder-not-a-real-secret'
python3 -m py_compile src/deploy_check.py
python3 src/deploy_check.py | tee vars-out.txt
grep -q 'region ap-south-1' vars-out.txt
grep -q 'deploy ok' vars-out.txt
```

!!! example "Expected output"
    `vars-out.txt` contains both `region ap-south-1` and `deploy ok`.


### Validation steps

- [ ] Non-secret config uses top-level `variables` in `.gitlab-ci.yml`
- [ ] No access keys or passwords are hard-coded in any file
- [ ] `oidc-notes.yaml` documents trust conditions and UI secret settings
- [ ] `deploy_staging` references `$DB_PASSWORD` as a UI variable placeholder
- [ ] Local simulation runs with an exported placeholder only

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Secret visible in job log | Echoed variable or missing mask | Never print secrets; enable masked variables in GitLab UI |
| Feature branch reads production secret | Variable not protected | Mark sensitive variables protected and scope to environment |
| OIDC assume-role fails | Wrong audience or subject claim | Align `oidc-notes.yaml` trust `sub` with project path and ref |
| Masked variable empty on MR | Protected variable on unprotected branch | Expected behaviour — test on protected default branch |

### Challenge exercise

Add an `id_tokens` block to `deploy_staging` with `GITLAB_OIDC_TOKEN` and audience `https://gitlab.com`. Extend `oidc-notes.yaml` with the matching `id_token_name`. Re-validate YAML — still no real secrets in Git.

### Learning outcomes

- Separated non-secret configuration from secret placeholders
- Documented OIDC trust mapping in version-controlled YAML
- Understood masked and protected variable behaviour
- Validated files offline without committing credentials

### Cleanup

```bash
unset DB_PASSWORD AWS_REGION APP_ENV 2>/dev/null || true
rm -f ~/rebash-gitlab/module-06/vars-out.txt
# Keep .gitlab-ci.yml and oidc-notes.yaml for module 07
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






1. Where should non-secret configuration live versus secret values?
2. OIDC job cannot assume a cloud role — what claims and settings do you verify?
3. What does masking actually guarantee in GitLab job logs?
4. Why prefer OIDC over long-lived cloud access keys in CI?
5. How do protected variables change merge request pipeline behaviour?

!!! tip "Sample answer — question 2"
    Verify id_tokens audience, the cloud identity provider trust policy (subject/ref/project), and that the job context may receive the token. Claim mismatches dominate.

!!! tip "Sample answer — question 4"
    OIDC issues short-lived credentials scoped by trust conditions, removing standing keys from GitLab variables. Never print the JWT.

## Related Tutorials








- [Course overview](index.md)
- [Artifacts, Caches, and Dependencies](artifacts-caches-and-dependencies.md)

## References








- [CI/CD variables](https://docs.gitlab.com/ee/ci/variables/)  
- [OIDC with GitLab CI/CD](https://docs.gitlab.com/ee/ci/cloud_services/)
