---
title: "GitLab CI/CD Fundamentals"
description: "Understand CI/CD concepts, GitLab architecture, pipelines, stages, jobs, runners overview, and Free/Premium/Ultimate editions."
difficulty: beginner
estimated_time: "35–50 min"
technology: gitlab
category: gitlab
module: "Module 1 · GitLab CI/CD Fundamentals"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - gitlab-ci
  - cicd
  - pipelines
prerequisites:
  - git/index
  - linux/index
next:
  - gitlab/gitlab-projects-mrs-and-releases
related:
  - docker/introduction-to-docker
  - git/git-workflows-and-branching
labs: []
projects: []
interview: interview/gitlab
certifications:
  - GitLab Certified CI/CD Associate
tags:
  - gitlab
  - cicd
  - pipelines
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# GitLab CI/CD Fundamentals

## Overview

Explain what CI/CD solves, map GitLab’s architecture to pipelines and runners, and define stage, job, and pipeline in ops language.

**Continuous Integration (CI)** builds and tests every change in Git. **Continuous Delivery / Deployment (CD)** promotes those builds toward production with gates you control. **GitLab CI/CD** stores the automation definition as `.gitlab-ci.yml` next to the application code, so review, history, and merge requests share one system.

This course is **GitLab CI/CD for Cloud & DevOps Engineers** — production pipelines, not toy demos.

This is a core tutorial in **Module 1 · GitLab CI/CD Fundamentals** of the REBASH Academy **GitLab CI/CD for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Git](../git/index.md) — commits, branches, and merge requests
- [Linux](../linux/index.md) — comfortable terminal and YAML editing

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Define CI, CD, pipeline, stage, and job  
- [ ] Sketch GitLab → Runner → job execution  
- [ ] Contrast Free / Premium / Ultimate and SaaS vs self-managed  
- [ ] Name when shared runners are enough vs when you need dedicated ones

## Architecture

This topic’s control points and relationships are shown below.

![GitLab architecture](../assets/excalidraw/gitlab-architecture.svg)

## Theory

### What it is

A **pipeline** is one run of your CI/CD definition for a commit, merge request, tag, or schedule. Pipelines contain **stages** (ordered phases such as `build`, `test`, `deploy`). Each stage holds **jobs** — isolated units of work with a `script` that a **runner** executes. GitLab coordinates: the GitLab instance schedules jobs; runners pick them up and report status and logs.

| Term | Meaning |
|------|---------|
| Pipeline | One automation run for a Git event |
| Stage | Ordered group of jobs (next stage waits by default) |
| Job | Single unit of work (`script`, image, tags) |
| Runner | Agent that executes jobs |

### Why it matters

Manual builds and “works on my laptop” deploys fail at scale. Pipelines make every change **reviewable** (MR pipeline), **repeatable** (same YAML, different `$CI_*` context), and **auditable** (job logs and artefacts). Platform and SRE teams standardise templates so product squads inherit lint, test, and deploy patterns instead of inventing CI per repo.

### How it works

Mental model: **Git event → GitLab creates pipeline → jobs queued → runners execute → artefacts / status back to GitLab**.

1. You push or open a merge request; GitLab reads `.gitlab-ci.yml`.
2. GitLab expands includes, evaluates `rules` / `workflow`, and builds the job graph.
3. Eligible runners (shared, group, or project) claim jobs matching tags and capacity.
4. The executor (Docker, shell, Kubernetes, …) runs the job script and streams logs.
5. Job status rolls up to the pipeline; optional artefacts and environments update the UI.

You do **not** need a paid GitLab instance for early labs: use **GitLab.com free tier**, or lint locally with `glab ci lint` / **gitlab-ci-local**.

### Key concepts and comparisons

| Edition | Typical CI/CD focus |
|---------|---------------------|
| Free | Core pipelines, shared runners (minutes limits on SaaS) |
| Premium | Deeper compliance, approvals, advanced environments |
| Ultimate | Security scanning suites and governance at scale |

| Hosting | You operate |
|---------|-------------|
| GitLab.com (SaaS) | Projects and CI; GitLab runs the control plane |
| Self-managed | Full stack — GitLab, runners, upgrades, HA |

### Common pitfalls

- CI is not “the runner” — GitLab schedules; runners execute.
- A green pipeline is not a production release unless you designed deploy jobs and gates that way.
- Free-tier minutes are finite on SaaS — lint and local runners save quota.
- Stages are not the only ordering model; later modules cover `needs` DAGs.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-gitlab/module-01 && cd ~/rebash-gitlab/module-01
```

**Focus:** hands-on practice for GitLab CI/CD Fundamentals

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: GitLab CI/CD Fundamentals"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-gitlab/module-01
cd ~/rebash-gitlab/module-01
```

```bash
cd ~/rebash-gitlab/module-01
cat > .gitlab-ci.yml << 'EOF'
stages:
  - build
  - test

variables:
  APP_NAME: rebash-demo

build_job:
  stage: build
  script:
    - echo "Building $APP_NAME on $CI_COMMIT_SHORT_SHA"
    - echo "build-ok" > build.txt
  artifacts:
    paths:
      - build.txt
    expire_in: 1 hour

test_job:
  stage: test
  script:
    - test -f build.txt
    - echo "Pipeline $CI_PIPELINE_ID OK"
EOF

# Optional: lint without spending CI minutes
# glab ci lint .gitlab-ci.yml
# npx gitlab-ci-local --list   # if installed
python3 - << 'PY'
import yaml
yaml.safe_load(open(".gitlab-ci.yml"))
print("YAML parse OK")
PY
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-gitlab/module-01/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **GitLab CI/CD Fundamentals** always combines:

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

!!! warning "CI is not “the runner” — GitLab schedules; runners execute."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "A green pipeline is not a production release unless you designed deploy jobs and gates tha"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode GitLab CI/CD Fundamentals changes as code and review them in pull requests
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

**GitLab CI/CD Fundamentals** is essential for Cloud and DevOps engineers working with gitlab. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **GitLab CI/CD Fundamentals** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [GitLab Projects, Merge Requests, and Releases](gitlab-projects-mrs-and-releases.md)

## References

- [GitLab CI/CD concepts](https://docs.gitlab.com/ee/ci/)  
- [Pipelines](https://docs.gitlab.com/ee/ci/pipelines/)
