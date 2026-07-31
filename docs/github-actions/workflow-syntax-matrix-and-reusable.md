---
title: "Workflow Syntax: Matrix and Reusable Workflows"
description: "Deepen YAML skills — matrix builds, conditionals, inputs and outputs, and an introduction to reusable workflows."
difficulty: intermediate
estimated_time: "45–60 min"
technology: github-actions
category: github-actions
module: "Module 4 · Workflow Syntax"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - github-actions
  - yaml
  - matrix
  - reusable-workflows
prerequisites:
  - github-actions/github-hosted-and-self-hosted-runners
next:
  - github-actions/secrets-variables-and-oidc
related:
  - github-actions/github-actions-basics-workflows-jobs-steps
  - github-actions/composite-actions-and-reusable-workflows
labs: []
projects: []
interview: interview/github-actions
certifications:
  - GitHub Actions
tags:
  - github-actions
  - matrix
  - reusable-workflows
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Workflow Syntax: Matrix and Reusable Workflows

## Overview

Write maintainable workflow YAML using `strategy.matrix`, job and step `if:` conditionals, job outputs, and a first **reusable workflow** call pattern.

Beyond a single job, production workflows need **fan-out** (test on multiple OS or language versions), **selective execution** (`if:` on jobs and steps), and **reuse** so fifty repositories do not diverge. A **matrix** expands one job definition into many. **Outputs** pass data between jobs. **Reusable workflows** (`workflow_call`) let a platform team own a canonical CI definition that callers invoke with inputs.

This is a core tutorial in **Module 4 · Workflow Syntax** of the REBASH Academy **GitHub Actions for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [GitHub-Hosted and Self-Hosted Runners](github-hosted-and-self-hosted-runners.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Expand jobs with `strategy.matrix` and `fail-fast`  
- [ ] Gate jobs and steps with `if:` expressions  
- [ ] Publish and consume job `outputs`  
- [ ] Sketch a `workflow_call` reusable workflow and a caller  
- [ ] Name when to prefer composite actions vs reusable workflows

## Architecture

This topic’s control points and relationships are shown below.

![Workflow syntax](../assets/excalidraw/gha-workflow-syntax.svg)

## Theory

### What it is

**Workflow syntax** is the YAML contract described in GitHub’s reference: top-level `name`, `on`, `permissions`, `concurrency`, `env`, and `jobs`. Each job may set `needs`, `if`, `runs-on`, `strategy`, `outputs`, `permissions`, and `steps`.

A **matrix** under `strategy:` lists axes such as `python-version: ['3.11', '3.12']` or `os: [ubuntu-latest, windows-latest]`. GitHub creates one job per combination (Cartesian product), injecting `matrix.*` into expressions. Options such as `fail-fast`, `max-parallel`, and `include` / `exclude` refine the set.

**Conditionals** use `if:` at job or step level with expressions over contexts (`github`, `needs`, `matrix`, …). Prefer explicit conditions over duplicated workflow files per branch.

**Inputs and outputs:** reusable workflows and `workflow_dispatch` declare `inputs:`. Jobs declare `outputs:` mapped from step outputs (`echo "name=value" >> "$GITHUB_OUTPUT"`). Downstream jobs read {% raw %}`${{ needs.build.outputs.version }}`{% endraw %}.

**Reusable workflows** live in a workflow file with `on: workflow_call`. Callers use `jobs.<id>.uses: org/repo/.github/workflows/ci.yml@v1` (or a SHA) and pass `with:` / `secrets:`. They are heavier than **composite actions** (which are step bundles) but ideal for whole pipelines (lint → test → scan).

| Construct | Role |
|-----------|------|
| `strategy.matrix` | Fan-out across versions / OSes |
| `if:` | Include or skip job/step |
| `needs` + `outputs` | Ordered jobs with data |
| `workflow_call` | Callable pipeline definition |
| Composite action | Reusable *steps*, not whole jobs graph |

### Why it matters

Matrix builds catch “works on 3.12 only” defects before production. Poor `if:` design creates ghost jobs or skipped deploys that nobody notices until release day. Reusable workflows are how platform engineering productises CI: version the workflow, require callers to bump the ref, and fix a CVE in setup actions once. Without reuse, every repository drifts — different Node versions, missing security scans, inconsistent permissions.

### How it works

1. GitHub expands the matrix into concrete jobs before scheduling.
2. Each matrix job runs independently (subject to `max-parallel`) with its own `matrix` context.
3. Jobs with `needs:` wait for dependencies; they can read outputs and use `if: needs.x.result == 'success'`.
4. A reusable workflow run nests under the caller; inputs become available as {% raw %}`${{ inputs.name }}`{% endraw %} inside the called workflow.
5. Permissions should be least privilege at caller and callee — later security modules tighten `permissions:` and `id-token`.

Author both files in one repository for learning; in production, platform teams often publish reusable workflows from a central `org/workflows` repository and pin tags or SHAs.

### Key concepts and comparisons

| Pattern | Use when |
|---------|----------|
| Matrix | Same steps, many versions/OS |
| Separate jobs | Different graphs or artefacts |
| Reusable workflow | Shared multi-job pipeline |
| Composite action | Shared install/build *steps* |

| Matrix tip | Why |
|------------|-----|
| Keep axes small | Combinatorial explosion burns minutes |
| Use `include` for special cases | Avoid huge Cartesian products |
| Name jobs with {% raw %}`${{ matrix.* }}`{% endraw %} | Readable Actions UI |

### Common pitfalls

- Forgetting that matrix failure fails the workflow when `fail-fast: true` (default).
- Referencing `matrix` outside a matrix job.
- Passing secrets to reusable workflows without `secrets: inherit` or explicit mapping.
- Treating reusable workflow `@main` as a stable contract — pin versions for production.
- Overusing `continue-on-error` so red builds look green in required checks.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-github-actions/module-04/.github/workflows && cd ~/rebash-github-actions/module-04/.github/workflows
```

**Focus:** hands-on practice for Workflow Syntax: Matrix and Reusable Workflows

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-github-actions/module-04/.github/workflows
cd ~/rebash-github-actions/module-04
```

Build a matrix job plus a local reusable workflow pair.

```bash
cd ~/rebash-github-actions/module-04
printf 'demo\n' > README.md
```

{% raw %}
```yaml
# .github/workflows/reusable-ci.yml
name: Reusable CI

on:
  workflow_call:
    inputs:
      app_name:
        description: Application name
        required: true
        type: string
    outputs:
      status_line:
        description: Summary line
        value: ${{ jobs.verify.outputs.status_line }}

jobs:
  verify:
    runs-on: ubuntu-latest
    outputs:
      status_line: ${{ steps.meta.outputs.status_line }}
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Smoke test
        run: |
          python --version
          test -f README.md
          echo "OK ${{ inputs.app_name }} on ${{ matrix.python-version }}"
      - name: Set output once
        id: meta
        if: matrix.python-version == '3.12'
        run: echo "status_line=${{ inputs.app_name }}-ok" >> "$GITHUB_OUTPUT"
```
{% endraw %}

{% raw %}
```yaml
# .github/workflows/caller.yml
name: Module 4 caller

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

jobs:
  call-reusable:
    uses: ./.github/workflows/reusable-ci.yml
    with:
      app_name: rebash-demo

  after:
    needs: call-reusable
    if: needs.call-reusable.result == 'success'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Reusable finished — ${{ needs.call-reusable.outputs.status_line }}"
```
{% endraw %}

```bash
# Push to GitHub and open the Actions tab to see matrix rows under the reusable run
# actionlint .github/workflows/*.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-github-actions/module-04/.github/workflows/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Workflow Syntax: Matrix and Reusable Workflows** always combines:

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

!!! warning "Forgetting that matrix failure fails the workflow when `fail-fast: true` (default)."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Referencing `matrix` outside a matrix job."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Workflow Syntax: Matrix and Reusable Workflows changes as code and review them in pull requests
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

**Workflow Syntax: Matrix and Reusable Workflows** is essential for Cloud and DevOps engineers working with github-actions. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Workflow Syntax: Matrix and Reusable Workflows** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Secrets, Variables, and OIDC](secrets-variables-and-oidc.md)

## References

- [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)  
- [Running a matrix of jobs](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs)  
- [Reusing workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
