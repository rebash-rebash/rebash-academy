---
title: "Troubleshooting GitHub Actions"
description: "Debug failed jobs, runners, authentication, cache, deploy failures, and slow workflows with a fixed GitHub Actions playbook."
difficulty: expert
estimated_time: "45–60 min"
technology: github-actions
category: github-actions
module: "Module 16 · Troubleshooting"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - github-actions
  - troubleshooting
  - runners
  - performance
prerequisites:
  - github-actions/production-pipelines-and-environments
next:
  - github-actions/index
related:
  - github-actions/github-hosted-and-self-hosted-runners
  - github-actions/secrets-variables-and-oidc
  - github-actions/artifacts-and-caching
labs: []
projects: []
interview: interview/github-actions
certifications:
  - GitHub Actions
  - GitHub Administration
tags:
  - github-actions
  - troubleshooting
  - debugging
  - performance
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Troubleshooting GitHub Actions

## Overview




Diagnose failed jobs, runner problems, authentication errors, cache misses, deploy failures, and slow workflows with a fixed order: trigger → permissions → runner → credentials → cache → deploy target → performance.

Most “Actions is broken” tickets are skipped jobs, missing permissions, offline self-hosted runners, expired OIDC trust, or poisoned caches — not mysterious GitHub bugs. Separate **definition** failures (workflow never ran the job you expected) from **execution** failures before changing production secrets.

This is a core tutorial in **Module 16 · Troubleshooting** of the REBASH Academy **GitHub Actions for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites




- [Production Pipelines and Environments](production-pipelines-and-environments.md)
- Runner, secrets/OIDC, and cache modules completed (or equivalent)



## Learning Objectives




By the end of this tutorial, you will be able to:

- [ ] Classify trigger / permissions / runner / auth / cache / deploy failures  
- [ ] Use job logs, `CONTEXT` dumps, and `act`-free local YAML checks systematically  
- [ ] Recover from queued jobs and self-hosted executor errors  
- [ ] Apply a performance triage for slow workflows



## Architecture




This topic’s control points and relationships are shown below.

![Troubleshooting ladder](../assets/excalidraw/gha-troubleshooting.svg)



## Theory




### What it is

**Troubleshooting GitHub Actions** locates which layer failed: trigger/`if`, `permissions`, runner capacity, step runtime, secrets/OIDC, cache/artefacts, or the deploy target. A red step log is necessary but not sufficient — **queued** jobs never produce script output.

| Symptom | First checks |
|---------|----------------|
| Workflow not listed | `on:` / paths / workflow enabled |
| Job skipped | Job `if`, failed/skipped `needs` |
| Queued forever | Labels, concurrency, self-hosted online |
| Step exit ≠ 0 | Failing command, tool/image version |
| 401 / forbidden | `permissions`, secrets, OIDC, environments |
| Flaky / slow | Cache keys, cold images, serial `needs` |

### Why it matters

Delivery recovery depends on CI as much as apps. Platform on-call needs a playbook juniors can follow under pressure. Shift-left YAML checks and action-pin review catch definition errors before they burn hosted minutes.

### How it works

1. **Trigger** — Did `on:` match?  
2. **Graph** — Skipped via `needs` / `if`?  
3. **Permissions** — Least privilege (`contents`, `id-token`, `packages`)?  
4. **Runner** — Labels match? Self-hosted up, disk, Docker?  
5. **Log** — Read the failing step; use step debug only in safe repos.  
6. **Auth** — Secrets/OIDC/environment gates/registry login?  
7. **Cache** — Wrong key, missing `needs`, or corrupt restore?  
8. **Deploy / perf** — Target RBAC/probes/approvals; then longest jobs and serial chains.

Prefer root-cause fixes over retry-as-strategy. Reproduce with a minimal workflow when stuck.

### Key concepts and comparisons

| Failure class | Looks like | Not fixed by |
|---------------|------------|--------------|
| Definition | Job absent / skipped | Restarting runners |
| Capacity | Queued, no runners | Editing script only |
| Runtime | Red step | Adding runners alone |
| Auth | 401/403 | Clearing cache |
| Cache / deploy | Missing files / target reject | Blind re-run |

### Common pitfalls

- Blaming GitHub.com when no runner matches `runs-on` labels.  
- Clearing all caches first — hides bad key design.  
- Echoing secrets into logs on shared runners.  
- `continue-on-error: true` as a permanent broken gate.  
- Re-running while an Environment still awaits approval.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-github-actions/module-16/.github/workflows && cd ~/rebash-github-actions/module-16/.github/workflows
```

**Focus:** capture a failing step pattern and local reproduction

### Step 1 – Broken vs fixed workflow pair

```bash
mkdir -p .github/workflows
cat > triage.md << 'EOF'
1. Open the failed step log — first error
2. Confirm action version
3. Check permissions for GITHUB_TOKEN
4. Re-run failed jobs; debug logging only in private forks
5. Reproduce steps in a clean container
EOF
cat > .github/workflows/troubleshoot.yml << 'EOF'
name: Troubleshoot
on: [workflow_dispatch]
permissions:
  contents: read
jobs:
  broken_shape:
    runs-on: ubuntu-latest
    continue-on-error: true
    steps:
      - run: curl --fail https://example.invalid/missing
  fixed_shape:
    runs-on: ubuntu-latest
    steps:
      - run: curl --fail -I https://example.com | head -n 5
EOF
```

### Step 2 – Reproduce with Docker

```bash
docker run --rm curlimages/curl:8.10.1 curl --fail -I https://example.com | head -n 5
test -f triage.md
docker rmi curlimages/curl:8.10.1 2>/dev/null || true
```

### Final step – Cleanup note

```bash
docker rmi curlimages/curl:8.10.1 2>/dev/null || true
# Keep ~/rebash-github-actions/ for later tutorials
```



## Validation




- [ ] Lab commands run under `~/rebash-github-actions/module-16/.github/workflows/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough




Production practice for **Troubleshooting GitHub Actions** always combines:

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




!!! warning "Blaming GitHub.com when no runner matches `runs-on` labels.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Clearing all caches first — hides bad key design.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices




- Encode Troubleshooting GitHub Actions changes as code and review them in pull requests
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




You can design, secure, promote, and troubleshoot production GitHub Actions pipelines end to end.



## Interview Questions


1. Give a step-by-step triage for a red workflow.
2. When is Actions debug logging appropriate?
3. How do expression evaluation bugs show up?
4. What local tools help reproduce workflows?
5. How do you handle a compromised third-party action?

!!! tip "Sample answer — question 2"
    Open the failed step log first, confirm action versions and permissions, then re-run a single job after fixing.

!!! tip "Sample answer — question 4"
    Debug logs can leak secrets — enable briefly on private repos only and rotate credentials if exposure is possible.



## Related Tutorials




- [Course overview](index.md)
- [Course overview](index.md) · [GitLab CI/CD](../gitlab/index.md) · [DevOps Engineer path](../career-paths/devops-engineer/index.md)



## References




- [About monitoring and troubleshooting](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/about-monitoring-and-troubleshooting)  
- [Enabling debug logging](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/enabling-debug-logging)  
- [Self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)
