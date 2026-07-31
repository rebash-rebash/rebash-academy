---
title: "Pipeline Design: DAGs and Includes"
description: "Design multi-stage and DAG pipelines with needs, parent-child and multi-project triggers, dynamic pipelines, and includes/templates."
difficulty: intermediate
estimated_time: "45–60 min"
technology: gitlab
category: gitlab
module: "Module 5 · Pipeline Design"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - gitlab-ci
  - pipeline-design
  - includes
prerequisites:
  - gitlab/pipeline-syntax-gitlab-ci-yml
next:
  - gitlab/variables-secrets-and-oidc
related:
  - gitlab/artifacts-caches-and-dependencies
  - gitlab/production-pipelines-and-environments
labs: []
projects: []
interview: interview/gitlab
certifications:
  - GitLab Certified CI/CD Associate
tags:
  - gitlab
  - dag
  - includes
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Pipeline Design: DAGs and Includes

## Overview

Compose maintainable pipelines with multi-stage flows, `needs` DAGs, parent-child and multi-project pipelines, dynamic child pipelines, and `include` templates.

Linear stages work until feedback time explodes. **DAG pipelines** (`needs`) start independent jobs early. **Includes** share templates across projects. **Parent-child** and **multi-project** pipelines split ownership; **dynamic pipelines** generate YAML when the graph depends on the change set.

This is a core tutorial in **Module 5 · Pipeline Design** of the REBASH Academy **GitLab CI/CD for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Pipeline Syntax (.gitlab-ci.yml)](pipeline-syntax-gitlab-ci-yml.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Design a DAG with `needs` for parallel fans  
- [ ] Use `include` / local templates without copy-paste sprawl  
- [ ] Contrast parent-child vs multi-project triggers  
- [ ] Outline when to generate a dynamic child pipeline

## Architecture

This topic’s control points and relationships are shown below.

![Parent-child pipelines](../assets/excalidraw/gitlab-parent-child.svg)

## Theory

### What it is

**Multi-stage** pipelines group jobs into ordered phases. A **DAG** adds edges with `needs` so job B can start when A finishes even if other stage peers are still running. **`include`** merges external YAML (`local`, `project`, `remote`, `template`, component inputs). A **parent-child** pipeline uses `trigger:include` so a parent job starts a child pipeline in the *same* project. A **multi-project** pipeline triggers a pipeline in another project. A **dynamic** child pipeline writes YAML to an artefact, then triggers it.

| Pattern | Use when |
|---------|----------|
| Stages only | Short, linear CI |
| `needs` DAG | Independent jobs; faster MRs |
| `include` | Shared lint/test/deploy templates |
| Parent-child | Split a large pipeline; keep one project |
| Multi-project | Deploy/infra owned by another repo |
| Dynamic child | Matrix depends on detected files/services |

### Why it matters

Platform teams win by **shipping templates**, not reviewing 200-line bespoke YAML per app. DAGs cut idle waiting. Child and multi-project pipelines enforce ownership (app CI vs platform deploy) without one mega-file.

### How it works

1. Factor common jobs into `templates/*.yml` and `include:local`.
2. Keep entry `.gitlab-ci.yml` thin: workflow, stages, includes, project-specific jobs only.
3. Add `needs` between independent fans; keep deploy needing the right artefacts.
4. For optional heavy work, generate `child-pipeline.yml` as an artefact and `trigger` it (`strategy: depend` when the parent must wait).
5. For cross-repo deploy, use `trigger:project` with clear downstream `rules`.

Lint includes and generated YAML locally — they are frequent schema failures.

### Key concepts and comparisons

| Parent-child | Multi-project |
|--------------|---------------|
| Same project | Downstream project |
| Generated graphs, split stages | Shared deploy / infra repos |
| Shares project variables by default | Pass variables; watch permissions |

Prefer **your** group’s project includes as the golden path; GitLab `include:template` is a starter.

### Common pitfalls

- Circular `needs`, or needing a job excluded by `rules`.
- Including remote YAML from untrusted URLs.
- Dynamic pipelines that regenerate differently every run.
- Triggering downstream deploys from every feature branch.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-gitlab/module-05/{templates,generated} && cd ~/rebash-gitlab/module-05/{templates,generated}
```

**Focus:** hands-on practice for Pipeline Design: DAGs and Includes

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Pipeline Design: DAGs and Includes"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-gitlab/module-05/{templates,generated}
cd ~/rebash-gitlab/module-05
```

```bash
cd ~/rebash-gitlab/module-05

cat > templates/lint.yml << 'EOF'
.lint_base:
  image: alpine:3.20
  script:
    - echo "lint $CI_PROJECT_PATH @ $CI_COMMIT_SHORT_SHA"
EOF

cat > generated/child-pipeline.yml << 'EOF'
stages: [child]
child_job:
  stage: child
  image: alpine:3.20
  script:
    - echo "dynamic child for $CI_COMMIT_SHORT_SHA"
EOF

cat > .gitlab-ci.yml << 'EOF'
include:
  - local: templates/lint.yml

workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

stages: [prep, verify, trigger]

lint:
  extends: .lint_base
  stage: prep

unit:
  stage: verify
  image: alpine:3.20
  needs: [lint]
  script:
    - echo "unit tests"

trigger_child:
  stage: trigger
  needs: [unit]
  trigger:
    include:
      - local: generated/child-pipeline.yml
    strategy: depend
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
EOF

python3 -c "import yaml,pathlib; [yaml.safe_load(pathlib.Path(p).read_text()) for p in ['.gitlab-ci.yml','templates/lint.yml','generated/child-pipeline.yml']]; print('YAML OK')"
# Optional: glab ci lint .gitlab-ci.yml — free tier / gitlab-ci-local also fine
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-gitlab/module-05/{templates,generated}/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Pipeline Design: DAGs and Includes** always combines:

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

!!! warning "Circular `needs`, or needing a job excluded by `rules`."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Including remote YAML from untrusted URLs."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Pipeline Design: DAGs and Includes changes as code and review them in pull requests
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

**Pipeline Design: DAGs and Includes** is essential for Cloud and DevOps engineers working with gitlab. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Pipeline Design: DAGs and Includes** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Variables, Secrets, and OIDC](variables-secrets-and-oidc.md)

## References

- [Parent-child pipelines](https://docs.gitlab.com/ee/ci/pipelines/downstream_pipelines.html)  
- [Includes](https://docs.gitlab.com/ee/ci/yaml/includes.html)
