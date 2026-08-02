---
title: "CI/CD Fundamentals and GitHub Actions"
description: "Understand Continuous Integration and Delivery, Continuous Delivery vs Deployment, GitHub Actions architecture, and the workflow lifecycle."
difficulty: beginner
estimated_time: "35–50 min"
technology: github-actions
category: github-actions
module: "Module 1 · CI/CD Fundamentals"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - github-actions
  - cicd
  - pipelines
prerequisites:
  - git/index
next:
  - github-actions/github-actions-basics-workflows-jobs-steps
related:
  - git/git-workflows-and-branching
  - docker/introduction-to-docker
labs: []
projects: []
interview: interview/github-actions
certifications:
  - GitHub Foundations
  - GitHub Actions
tags:
  - github-actions
  - cicd
  - workflows
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# CI/CD Fundamentals and GitHub Actions

## Overview








Explain what Continuous Integration (CI) and Continuous Delivery / Deployment (CD) solve, place GitHub Actions in that model, and describe the workflow lifecycle from event to completion.

**Continuous Integration (CI)** builds and tests every meaningful change in Git so defects surface in minutes, not at release time. **Continuous Delivery** keeps every successful build *ready* to ship with human or automated gates. **Continuous Deployment** goes further and promotes to production automatically when those gates pass. **GitHub Actions** implements that automation as YAML workflows under `.github/workflows/`, so review, history, and pull requests share one system with your code.

This course is **GitHub Actions for Cloud & DevOps Engineers** — production pipelines, not toy demos.

This is a core tutorial in **Module 1 · CI/CD Fundamentals** of the REBASH Academy **GitHub Actions for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites








- [Git](../git/index.md) — commits, branches, and pull requests
- Comfortable editing YAML in a terminal editor

## Learning Objectives








By the end of this tutorial, you will be able to:

- [ ] Define CI, Continuous Delivery, and Continuous Deployment  
- [ ] Map GitHub event → workflow → job → step → runner  
- [ ] Sketch the workflow lifecycle from trigger to conclusion  
- [ ] Name when Actions is enough vs when you need dedicated runners or another CI product

## Architecture








This topic’s control points and relationships are shown below.

![GitHub Actions architecture](../assets/excalidraw/gha-architecture.svg)

## Theory








### What it is

**CI** means every push or pull request runs a known script: install dependencies, compile or lint, run tests, and report status back to GitHub. The goal is a shared, automated truth about whether the branch is healthy — not “it worked on my laptop.”

**Continuous Delivery** means the pipeline also produces a *releasable* artefact (image, package, binary) and can deploy to staging or production, but a person or policy still decides *when*. **Continuous Deployment** removes that release button for paths you trust: green main deploys without a manual click. Teams often mix both — delivery for production, deployment for lower environments.

**GitHub Actions** is GitHub’s CI/CD engine. A **workflow** is a YAML file that reacts to **events** (push, `pull_request`, schedule, `workflow_dispatch`, and many more). A workflow contains **jobs**; jobs contain **steps**. Steps run shell commands or reusable **actions**. A **runner** (GitHub-hosted or self-hosted) executes the job.

| Term | Meaning |
|------|---------|
| Workflow | One automation definition (a YAML file) |
| Event | GitHub signal that may start a run |
| Job | Unit of work on one runner (steps share a workspace) |
| Step | Command or action inside a job |
| Runner | Machine that executes the job |

### Why it matters

Manual builds and “SSH and hope” deploys fail at scale: environments drift, rollbacks depend on tribal knowledge, and security reviews cannot inspect a console click. Pipelines make every change **reviewable** (checks on the pull request), **repeatable** (same YAML, different `github.*` context), and **auditable** (job logs and artefacts). Platform and Site Reliability Engineering (SRE) teams standardise reusable workflows so product squads inherit lint, test, scan, and deploy patterns instead of inventing CI per repository. In cloud work, the same mental model later covers OpenID Connect (OIDC) to AWS, Azure, or Google Cloud, container builds, and Infrastructure as Code (IaC) plans — without leaving Git.

### How it works

Mental model: **GitHub event → workflow selected → jobs queued → runners execute steps → status / artefacts back to GitHub**.

1. You push or open a pull request; GitHub evaluates workflows under `.github/workflows/`.
2. Matching `on:` filters create a **workflow run**; jobs that pass `if:` conditions are queued.
3. Available runners (hosted labels such as `ubuntu-latest`, or self-hosted labels) pick up jobs.
4. Each job checks out the repository (usually via `actions/checkout`), runs steps in order, and streams logs.
5. Job conclusions roll up to the workflow; optional artefacts, deployments, and required status checks update the pull request and branch protection.

You do **not** need a paid GitHub plan for early labs: public repositories and free private minutes cover learning. Later modules introduce self-hosted runners when you need private networks, GPUs, or longer jobs.

### Key concepts and comparisons

| Practice | You get | Typical gate |
|----------|---------|--------------|
| Continuous Integration | Fast feedback on every change | Required checks on PRs |
| Continuous Delivery | Always releasable artefact | Manual / environment approval |
| Continuous Deployment | Auto-promote when green | Strong tests + progressive delivery |

| Without CI/CD | With GitHub Actions |
|---------------|---------------------|
| “Works on my machine” | Same runner image for every PR |
| Unreviewed production changes | Workflow YAML in the PR diff |
| Rebuild from memory after outage | Re-run or redeploy from a known SHA |

**Actions vs GitLab CI vs Jenkins (brief):** Actions lives next to GitHub pull requests and OIDC; GitLab CI pairs tightly with GitLab MRs and runners; Jenkins is self-managed and flexible but you operate the control plane. Pick based on where your source of truth and identity already live.

### Common pitfalls

- CI is not “the runner” — GitHub schedules; runners execute.
- A green workflow is not a production release unless you designed deploy jobs and environment gates that way.
- Continuous Delivery and Continuous Deployment are not synonyms — know which one your org actually runs.
- Free-tier minutes are finite on private repos — lint locally and cache dependencies later to save quota.
- Copy-pasting random marketplace actions without pinning versions is a supply-chain risk (covered in security modules).

## Hands-on Lab



### Objective

Author a GitHub Actions workflow that implements **CI/CD Fundamentals and GitHub Actions** and validate YAML structure locally.

### Prerequisites

- Python 3 with PyYAML
- Optional: GitHub repo to run the workflow

### Lab environment

Workspace: `~/rebash-github-actions/module-01`

Workflows under `.github/workflows/`. In docs, wrap GitHub Actions expressions in Jinja raw blocks so MkDocs macros do not parse them; use heredocs in the lab.

```bash
mkdir -p ~/rebash-github-actions/module-01 && cd ~/rebash-github-actions/module-01
```

### Real-world scenario

Platform engineering wants **CI/CD Fundamentals and GitHub Actions** as a reusable workflow pattern. You prototype YAML that passes review and runs on `ubuntu-latest`.

### Step-by-step tasks

#### Task 1 – Create workflow file

Jobs and steps must be explicit; pin mainstream actions.

```bash
mkdir -p .github/workflows
cat > .github/workflows/lab.yml << 'EOF'
name: lab
on:
  workflow_dispatch:
  push:
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Prove workspace
        run: |
          mkdir -p out
          echo ok > out/marker.txt
          test -s out/marker.txt
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/lab.yml')); print('workflow OK')"
```

**Expected output:** `workflow OK` printed; file exists under `.github/workflows/`.

#### Task 2 – Dry-run the shell steps locally

The `run:` block should work in a normal shell before CI.

```bash
mkdir -p out && echo ok > out/marker.txt
test -s out/marker.txt && cat out/marker.txt
```

**Expected output:** Prints `ok`.

### Validation steps

- [ ] Workflow YAML parses
- [ ] Local run steps succeed

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Invalid workflow file | YAML/indent | Validate with PyYAML / actionlint |
| Action not found | Bad uses ref | Pin `actions/checkout@v4` |
| Permission denied | Missing permissions/OIDC | Set least-privilege `permissions:` |

### Challenge exercise

Add a second job with `needs: build` that uploads `out/` as an artefact (YAML only is fine offline).

### Learning outcomes

- Created a real workflow file
- Validated structure before push

### Cleanup

```bash
# Keep workflow stubs under ~/rebash-github-actions/
```

## Validation








- [ ] Lab commands run under `~/rebash-github-actions/module-01/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough








Production practice for **CI/CD Fundamentals and GitHub Actions** always combines:

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








!!! warning "CI is not “the runner” — GitHub schedules; runners execute."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "A green workflow is not a production release unless you designed deploy jobs and environme"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices








- Encode CI/CD Fundamentals and GitHub Actions changes as code and review them in pull requests
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








**CI/CD Fundamentals and GitHub Actions** is essential for Cloud and DevOps engineers working with github-actions. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions






1. What is the relationship between a workflow, a job, and a step?
2. A workflow is not starting on push — what do you verify first?
3. Why set top-level permissions even for simple CI?
4. How should secrets be referenced in GitHub Actions?
5. When do you choose workflow_dispatch over push triggers?

!!! tip "Sample answer — question 2"
    Check the on filters (branches/paths), whether Actions is enabled, and the Actions tab for skipped workflows. YAML indentation errors often prevent registration.

!!! tip "Sample answer — question 4"
    Default to read-only contents and open write permissions only where needed. Store secrets in GitHub Secrets/Environments and never print secret values.

## Related Tutorials








- [Course overview](index.md)
- [GitHub Actions Basics: Workflows, Jobs, and Steps](github-actions-basics-workflows-jobs-steps.md)

## References








- [Understanding GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions)  
- [Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)  
- [About continuous integration](https://docs.github.com/en/actions/automating-builds-and-tests/about-continuous-integration)
