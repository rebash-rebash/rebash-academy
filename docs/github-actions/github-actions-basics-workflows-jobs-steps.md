---
title: "GitHub Actions Basics: Workflows, Jobs, and Steps"
description: "Author your first real workflow — files, events, jobs, steps, actions, expressions, and variables."
difficulty: beginner
estimated_time: "40–55 min"
technology: github-actions
category: github-actions
module: "Module 2 · GitHub Actions Basics"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - github-actions
  - workflows
  - yaml
prerequisites:
  - github-actions/cicd-fundamentals-and-github-actions
next:
  - github-actions/github-hosted-and-self-hosted-runners
related:
  - git/git-workflows-and-branching
  - github-actions/workflow-syntax-matrix-and-reusable
labs: []
projects: []
interview: interview/github-actions
certifications:
  - GitHub Foundations
  - GitHub Actions
tags:
  - github-actions
  - workflows
  - jobs
  - steps
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# GitHub Actions Basics: Workflows, Jobs, and Steps

## Overview

Write a working workflow that checks out code, uses an action, sets a variable, evaluates an expression, and prints useful run context — the building blocks of every later module.

Workflow files live in **`.github/workflows/`**. Each file defines **`on:`** (when it runs), **`jobs:`** (what runs where), and under each job a list of **`steps:`**. Steps are either **`run:`** shell commands or **`uses:`** references to actions. **Expressions** ({% raw %}`${{ … }}`{% endraw %}) and **contexts** (`github`, `env`, `vars`, `secrets`) parameterise behaviour without hard-coding every branch name.

This is a core tutorial in **Module 2 · GitHub Actions Basics** of the REBASH Academy **GitHub Actions for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [CI/CD Fundamentals and GitHub Actions](cicd-fundamentals-and-github-actions.md)
- A GitHub repository you can push to (public is fine for learning)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Place a workflow under `.github/workflows/` and choose events  
- [ ] Structure jobs with `runs-on` and ordered steps  
- [ ] Use `actions/checkout` and at least one other official action  
- [ ] Read `github` / `env` contexts and write a simple expression  
- [ ] Distinguish workflow `env`, job `env`, and step `env`

## Architecture

This topic’s control points and relationships are shown below.

![GitHub Actions basics](../assets/excalidraw/gha-basics.svg)

## Theory

### What it is

A **workflow file** is YAML GitHub loads when events fire. Common events for application CI are `push`, `pull_request`, and `workflow_dispatch` (manual). You can filter by branches, paths, and activity types so a docs-only change does not rebuild everything.

A **job** runs on one runner image (`runs-on: ubuntu-latest` is the default learning choice). Jobs in the same workflow are **independent by default** and may run in parallel; you connect them later with `needs:`. Inside a job, **steps** share a working directory and environment unless you deliberately isolate them.

An **action** is a reusable unit published in a repository (or a local `./.github/actions/…` composite). Official actions such as `actions/checkout` and `actions/setup-node` save you from reinventing clone and toolchain setup. **Expressions** wrap dynamic values: {% raw %}`${{ github.sha }}`{% endraw %}, {% raw %}`${{ env.APP_NAME }}`{% endraw %}, conditionals such as {% raw %}`${{ github.ref == 'refs/heads/main' }}`{% endraw %}. **Variables** appear as `env:` blocks (workflow, job, or step scope) or as repository/organisation **configuration variables** (`vars.*`) set in the GitHub UI.

| Piece | You write | Runner sees |
|-------|-----------|-------------|
| `on:` | Events and filters | Whether the run starts |
| `jobs.*.runs-on` | Label set | Which machine claims the job |
| `steps[].run` | Shell | Exit code fails the step |
| `steps[].uses` | Action ref | Action’s entrypoint |
| {% raw %}`${{ }}`{% endraw %} | Expression | Evaluated string/boolean |

### Why it matters

Almost every production pipeline — lint, test, Docker build, Terraform plan, Kubernetes deploy — is a composition of these primitives. Teams that skip the basics end up with copy-pasted mega-YAML, unclear `if:` conditions, and secrets leaked via `echo`. Learning scopes (`env` vs `vars` vs `secrets`), pinning action versions (`@v4` or preferably a commit SHA later), and reading the **Actions** tab logs are core DevOps skills. Pull request status checks also depend on job names staying stable so branch protection rules keep working when you refactor.

### How it works

1. GitHub parses the workflow and matches `on:` to the incoming event.
2. For each eligible job, a runner starts (or is reused from a warm pool on hosted runners).
3. Default steps often begin with checkout so the workspace contains your commit.
4. Subsequent steps run in order; a failed step fails the job unless `continue-on-error` is set.
5. Expressions are evaluated by the Actions runtime before the step runs; contexts such as `github`, `env`, `vars`, `secrets`, `needs`, and `matrix` supply data.
6. Job status rolls up; required checks (configured in branch protection) block merge when red.

For local authoring without burning minutes, write YAML first, validate structure, then push. Tools such as `actionlint` catch many mistakes before CI.

### Key concepts and comparisons

| Scope | Keyword | Visibility |
|-------|---------|------------|
| Workflow | top-level `env:` | All jobs |
| Job | `jobs.<id>.env` | All steps in that job |
| Step | `steps[].env` | That step only |
| Repo/org config | `vars.NAME` | Non-secret settings from UI |
| Secrets | `secrets.NAME` | Sensitive; never print |

| `run:` | `uses:` |
|--------|---------|
| Inline shell you own | Shared action logic |
| Good for one-liners and repo scripts | Good for checkout, setup-*, marketplace tools |

**Concurrency note:** multiple pushes can start overlapping runs; later modules cover `concurrency:` groups. For now, know that the newest commit is not always the only run still executing.

### Common pitfalls

- Putting workflow files outside `.github/workflows/` — GitHub will ignore them.
- Using `master` in filters when the default branch is `main`.
- Forgetting `actions/checkout` then wondering why files are missing.
- Printing {% raw %}`${{ secrets.* }}`{% endraw %} “to debug” — logs may redact, but exfiltration is still possible.
- Treating `@v4` as immutable forever — tags can move; production often pins SHAs.
- Confusing job-level failure with workflow cancellation of sibling jobs (default: other jobs still run).

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-github-actions/module-02/.github/workflows && cd ~/rebash-github-actions/module-02/.github/workflows
```

**Focus:** hands-on practice for GitHub Actions Basics: Workflows, Jobs, and Steps

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: GitHub Actions Basics: Workflows, Jobs, and Steps"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-github-actions/module-02/.github/workflows
cd ~/rebash-github-actions/module-02
```

Create a first real workflow. Push to a GitHub remote when ready.

```bash
cd ~/rebash-github-actions/module-02
printf 'ok\n' > app.txt
```

{% raw %}
```yaml
# .github/workflows/basics.yml
name: Module 2 basics

on:
  push:
    branches: [main, master]
  pull_request:
  workflow_dispatch:

env:
  APP_NAME: rebash-demo

jobs:
  build-and-verify:
    runs-on: ubuntu-latest
    env:
      STAGE: ci
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Show GitHub context
        run: |
          echo "Repository=${{ github.repository }}"
          echo "Event=${{ github.event_name }}"
          echo "Actor=${{ github.actor }}"
          echo "SHA=${{ github.sha }}"

      - name: Use env scopes
        env:
          STEP_NOTE: "step-local"
        run: |
          echo "APP_NAME=${APP_NAME}"
          echo "STAGE=${STAGE}"
          echo "STEP_NOTE=${STEP_NOTE}"

      - name: Conditional on default branch tip
        if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master'
        run: echo "Running on default-branch tip"

      - name: Validate workspace file
        run: |
          test -f app.txt
          echo "Module 2 workflow OK for ${{ env.APP_NAME }}"
```
{% endraw %}

```bash
# Copy the YAML into .github/workflows/basics.yml, then:
# git init && git add . && git commit -m "Module 2 basics workflow"
# gh repo create rebash-gha-module-02 --private --source=. --remote=origin --push
# gh run list
actionlint .github/workflows/basics.yml 2>/dev/null || echo "Install actionlint later; YAML is ready to push"
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-github-actions/module-02/.github/workflows/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **GitHub Actions Basics: Workflows, Jobs, and Steps** always combines:

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

!!! warning "Putting workflow files outside `.github/workflows/` — GitHub will ignore them."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Using `master` in filters when the default branch is `main`."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode GitHub Actions Basics: Workflows, Jobs, and Steps changes as code and review them in pull requests
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

**GitHub Actions Basics: Workflows, Jobs, and Steps** is essential for Cloud and DevOps engineers working with github-actions. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **GitHub Actions Basics: Workflows, Jobs, and Steps** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [GitHub-Hosted and Self-Hosted Runners](github-hosted-and-self-hosted-runners.md)

## References

- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)  
- [Contexts and expressions](https://docs.github.com/en/actions/learn-github-actions/contexts)  
- [Essential features of GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/essential-features-of-github-actions)
