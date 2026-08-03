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
last_updated: "2026-08-03"
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

### Objective

Split CI into reusable `templates/*.yml` includes, compose a parent `.gitlab-ci.yml` with a `needs` DAG, and validate every YAML file offline.

### Prerequisites

- Python 3 with PyYAML (`pip install pyyaml`)
- Completed module 04 lab (optional reference for variables pattern)

### Lab environment

Workspace: `~/rebash-gitlab/module-05` with `templates/` and `generated/` subdirectories

File-first lab. Push to GitLab only when you want includes resolved on the server.

```bash
mkdir -p ~/rebash-gitlab/module-05/{templates,generated,src} && cd ~/rebash-gitlab/module-05
```

### Real-world scenario

Your platform team maintains shared CI templates. Product repos should `include` lint and test templates and wire a DAG so integration tests start only after unit tests and a build stub finish — without copy-pasting job definitions into every repository.

### Step-by-step tasks

#### Task 1 – Create shared lint template

Create `templates/lint.yml`:

```yaml
.lint_template:
  stage: lint
  image: python:3.12-alpine
  script:
    - python -m py_compile src/app.py
    - mkdir -p generated
    - echo "lint-pass" > generated/lint-status.txt
  artifacts:
    paths:
      - generated/lint-status.txt
    expire_in: 1 day
```

#### Task 2 – Create shared test template

Create `templates/test.yml`:

```yaml
.unit_test_template:
  stage: test
  image: python:3.12-alpine
  script:
    - test -f generated/lint-status.txt
    - python src/app.py

.integration_test_template:
  stage: test
  image: python:3.12-alpine
  script:
    - echo "integration stub" > generated/integration.txt
  artifacts:
    paths:
      - generated/integration.txt
    expire_in: 1 day
```

Validate templates:

```bash
cd ~/rebash-gitlab/module-05
python3 -c "
import yaml, pathlib
for p in pathlib.Path('templates').glob('*.yml'):
    yaml.safe_load(p.read_text())
    print('OK', p)
"
```

**Expected output:** Two lines starting with `OK templates/`.

#### Task 3 – Create app and parent pipeline with includes and needs DAG

Create `src/app.py`:

```python
print("dag-lab ok")
```

Create `.gitlab-ci.yml`:

```yaml
include:
  - local: templates/lint.yml
  - local: templates/test.yml

stages:
  - lint
  - test

lint:
  extends: .lint_template

unit_test:
  extends: .unit_test_template
  needs:
    - job: lint
      artifacts: true

integration_test:
  extends: .integration_test_template
  needs:
    - job: unit_test
    - job: lint
      artifacts: true
```

Validate all YAML:

```bash
cd ~/rebash-gitlab/module-05
python3 -c "
import yaml, pathlib
for f in ['.gitlab-ci.yml', 'templates/lint.yml', 'templates/test.yml']:
    yaml.safe_load(pathlib.Path(f).read_text())
    print('OK', f)
d = yaml.safe_load(open('.gitlab-ci.yml'))
assert d['integration_test']['needs'][0]['job'] == 'unit_test'
print('OK DAG needs chain')
"
```

**Expected output:** Three `OK` lines for files plus `OK DAG needs chain`.

#### Task 4 – Simulate generated artefact paths locally

```bash
cd ~/rebash-gitlab/module-05
mkdir -p generated
python3 -m py_compile src/app.py
echo "lint-pass" > generated/lint-status.txt
test -f generated/lint-status.txt
python3 src/app.py | tee dag-out.txt
echo "integration stub" > generated/integration.txt
test -f generated/integration.txt
grep -q 'dag-lab ok' dag-out.txt
```

**Expected output:** Both files under `generated/` exist; `dag-out.txt` contains `dag-lab ok`.

### Validation steps

- [ ] `templates/lint.yml` and `templates/test.yml` parse independently
- [ ] Parent `.gitlab-ci.yml` includes both templates with `local:` paths
- [ ] `unit_test` needs `lint` with artefacts
- [ ] `integration_test` needs both `unit_test` and `lint`
- [ ] Local simulation populates `generated/` as the jobs would

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Local file `templates/...` does not exist` | Wrong path relative to repo root | Place templates under `templates/` and use `local:` includes |
| `extends` key unknown | Template job missing dot prefix | Hidden templates use `.lint_template` naming |
| Circular `needs` | Jobs depend on each other | Draw the DAG on paper; integration should not block lint |
| Duplicate stage job names | Same job name in include and parent | Override with unique job keys (`unit_test`, not `test`) |

### Challenge exercise

Add `templates/build.yml` with a `.build_template` job that writes `generated/build-id.txt`, include it, and make `integration_test` also `needs` the build job.

### Learning outcomes

- Split reusable job definitions into included template files
- Composed a parent pipeline with `extends` and a `needs` DAG
- Validated every include and parent file offline
- Simulated generated artefact directories locally

### Cleanup

```bash
rm -rf ~/rebash-gitlab/module-05/generated
rm -f ~/rebash-gitlab/module-05/dag-out.txt
# Keep templates/ and .gitlab-ci.yml for module 06
```

## Validation








- [ ] Lab commands run under `~/rebash-gitlab/module-05/`
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






1. When do you choose include local versus project/remote includes?
2. A child job never runs after a refactor — what DAG mistakes are common?
3. How do hidden jobs help reuse?
4. What is the blast radius of a shared include owned by another team?
5. How do you version shared pipeline templates safely?

!!! tip "Sample answer — question 2"
    Trace needs edges and stage membership: a job can be skipped by rules or waiting on a renamed dependency. Confirm includes expanded as expected.

!!! tip "Sample answer — question 4"
    Pin shared templates to tags/SHAs and review changes like application code.

## Related Tutorials








- [Course overview](index.md)
- [Variables, Secrets, and OIDC](variables-secrets-and-oidc.md)

## References








- [Parent-child pipelines](https://docs.gitlab.com/ee/ci/pipelines/downstream_pipelines.html)  
- [Includes](https://docs.gitlab.com/ee/ci/yaml/includes.html)
