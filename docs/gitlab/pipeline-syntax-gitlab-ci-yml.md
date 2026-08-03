---
title: "Pipeline Syntax (.gitlab-ci.yml)"
description: "Author production .gitlab-ci.yml — variables, rules (prefer over only/except), workflow, needs, and dependencies."
difficulty: intermediate
estimated_time: "40–55 min"
technology: gitlab
category: gitlab
module: "Module 4 · Pipeline Syntax"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - gitlab-ci
  - yaml
  - pipeline-rules
prerequisites:
  - gitlab/gitlab-runners-and-executors
next:
  - gitlab/pipeline-design-dags-and-includes
related:
  - gitlab/gitlab-ci-fundamentals
  - gitlab/artifacts-caches-and-dependencies
labs: []
projects: []
interview: interview/gitlab
certifications:
  - GitLab Certified CI/CD Associate
tags:
  - gitlab
  - gitlab-ci
  - yaml
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---


# Pipeline Syntax (.gitlab-ci.yml)

## Overview








Write clear `.gitlab-ci.yml` using variables, `workflow` and job `rules`, and understand `needs` vs `dependencies` for ordering and artefact flow.

GitLab reads **`.gitlab-ci.yml`** (or an alternate CI config path) to define pipelines. Prefer **`rules`** over legacy `only` / `except`. Use **`workflow:rules`** to decide whether a pipeline is created at all. Use **`needs`** for DAG edges; use **`dependencies`** to control which job artefacts download.

This is a core tutorial in **Module 4 · Pipeline Syntax** of the REBASH Academy **GitLab CI/CD for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites








- [GitLab Runners and Executors](gitlab-runners-and-executors.md)

## Learning Objectives








By the end of this tutorial, you will be able to:

- [ ] Structure stages, default, variables, and jobs  
- [ ] Prefer `rules` over `only`/`except`  
- [ ] Control pipeline creation with `workflow`  
- [ ] Contrast `needs` (ordering) with `dependencies` (artefacts)

## Architecture








This topic’s control points and relationships are shown below.

![Pipeline syntax](../assets/excalidraw/gitlab-pipeline-syntax.svg)

## Theory








### What it is

Top-level keys commonly include `stages`, `default`, `variables`, `workflow`, `include`, and job names. A job needs at least a `script` (or `trigger` / `trigger:include` patterns covered later). Predefined variables such as `$CI_COMMIT_SHA`, `$CI_PIPELINE_SOURCE`, and `$CI_DEFAULT_BRANCH` are injected by GitLab — prefer them over hard-coded branch names where possible.

| Keyword | Role |
|---------|------|
| `variables` | Pipeline or job env (plus UI/group vars) |
| `rules` | When a job is added to the pipeline |
| `workflow:rules` | Whether any pipeline is created |
| `needs` | Start job early; optional artefact download |
| `dependencies` | Which prior jobs’ artefacts to fetch (stage model) |

### Why it matters

Ambiguous YAML creates **ghost pipelines** (double branch + MR pipelines), skipped deploy jobs, or jobs that download every artefact and waste minutes. Precise `rules` and lean `dependencies` cut cost and confusion. Reviewers can reason about production risk from the YAML alone.

### How it works

1. GitLab loads YAML (and includes).
2. `workflow:rules` decide if this event creates a pipeline.
3. For each job, `rules` decide inclusion; variables expand.
4. Default graph: all jobs in a stage finish before the next stage starts.
5. `needs` can start a job as soon as listed jobs finish (DAG), optionally with `artifacts: true/false`.
6. Without `dependencies`, jobs may download all artefacts from previous stages; set `dependencies: []` or an explicit list to stay lean.

Migrate away from `only` / `except` — they still work but compose poorly with complex sources.

### Key concepts and comparisons

| Approach | Prefer when |
|----------|-------------|
| Stage ordering only | Simple linear build → test → deploy |
| `needs` DAG | Long pipelines; parallel fans; skip empty stages |
| `dependencies` | Control artefact download under stage ordering |

| Legacy | Modern |
|--------|--------|
| `only: [main]` | `rules: [{ if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH }]` |
| `except: [schedules]` | `rules` with `when: never` for that source |

### Common pitfalls

- Combining `only` and `rules` on the same job — pick one model (`rules`).
- Forgetting `workflow` and paying for duplicate MR + branch pipelines.
- Using `needs` but still assuming stage barriers apply the same way.
- Putting secrets in YAML `variables:` — use masked/protected UI vars or OIDC (Module 6).

## Hands-on Lab

### Objective

Author a rich `.gitlab-ci.yml` demonstrating `workflow`, `rules`, `variables`, and an artefacts stub — then validate structure offline and simulate job output locally.

### Prerequisites

- Python 3 with PyYAML (`pip install pyyaml`)
- Optional: GitLab project to observe pipeline source variables in job logs

### Lab environment

Workspace: `~/rebash-gitlab/module-04`

File-first lab. Push to GitLab only when you want to inspect `$CI_*` values on a runner.

```bash title="Terminal"
mkdir -p ~/rebash-gitlab/module-04/src && cd ~/rebash-gitlab/module-04
```

### Real-world scenario

Reviewers rejected your team's pipeline because feature branches triggered deploy jobs and secrets appeared in YAML. You rewrite the file with explicit `workflow:rules`, per-job `rules`, non-secret `variables`, and a lint artefact passed to test via `needs`.

### Step-by-step tasks

#### Task 1 – Create the application

Create `src/app.py`:

```python title="app.py"
APP_NAME = "rebash-syntax-lab"
print(APP_NAME)
```

Run locally:

```bash title="Terminal"
cd ~/rebash-gitlab/module-04
python3 src/app.py | tee app-name.txt
grep -q 'rebash-syntax-lab' app-name.txt
```

!!! example "Expected output"
    `app-name.txt` contains `rebash-syntax-lab`.


#### Task 2 – Author the full pipeline syntax file

Create `.gitlab-ci.yml`:

```yaml title=".gitlab-ci.yml"
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

variables:
  APP_NAME: rebash-syntax-lab
  PYTHON_IMAGE: python:3.12-alpine
  LINT_REPORT: lint-report.txt

stages:
  - lint
  - test

lint:
  stage: lint
  image: $PYTHON_IMAGE
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  script:
    - python -m py_compile src/app.py
    - echo "lint ok for $APP_NAME" > "$LINT_REPORT"
  artifacts:
    paths:
      - lint-report.txt
    expire_in: 1 day

test:
  stage: test
  image: $PYTHON_IMAGE
  needs:
    - job: lint
      artifacts: true
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  script:
    - test -f lint-report.txt
    - python src/app.py
```

Validate offline:

```bash title="Terminal"
cd ~/rebash-gitlab/module-04
python3 -c "
import yaml
d = yaml.safe_load(open('.gitlab-ci.yml'))
assert d['variables']['APP_NAME'] == 'rebash-syntax-lab'
assert d['lint']['artifacts']['paths'] == ['lint-report.txt']
assert d['test']['needs'][0]['artifacts'] is True
print('OK syntax lab')
"
```

!!! example "Expected output"
    Prints `OK syntax lab`.


#### Task 3 – Simulate lint artefact and test locally

Reproduce the artefact hand-off without a runner:

```bash title="Terminal"
cd ~/rebash-gitlab/module-04
python3 -m py_compile src/app.py
echo "lint ok for rebash-syntax-lab" > lint-report.txt
test -f lint-report.txt
python3 src/app.py | tee test-out.txt
grep -q 'rebash-syntax-lab' test-out.txt
```

!!! example "Expected output"
    `lint-report.txt` exists; `test-out.txt` contains `rebash-syntax-lab`.


### Validation steps

- [ ] `workflow:rules` limits pipelines to MRs and default branch
- [ ] Non-secret config lives under top-level `variables`
- [ ] `lint` publishes `lint-report.txt` as an artefact
- [ ] `test` uses `needs` with `artifacts: true`
- [ ] Local simulation creates and consumes the lint report

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Duplicate MR + branch pipelines | Missing `workflow:rules` | Add explicit workflow rules before stages |
| `test` cannot find artefact | `needs` missing `artifacts: true` | Add `artifacts: true` under the lint need entry |
| Variable not expanded in `image:` | Wrong key scope | Use `$PYTHON_IMAGE` at job level or `default:` |
| Deploy job on feature branch | Over-broad `rules: - when: always` | Restrict deploy jobs to protected refs |

### Challenge exercise

Add `interruptible: true` to `lint` and `test` so newer pipeline runs cancel outdated MR jobs. Re-validate YAML.

### Learning outcomes

- Combined `workflow`, job `rules`, and `variables` in one reviewable file
- Passed artefacts between jobs with `needs` and explicit artefact download
- Kept secrets out of YAML by using non-secret variables only
- Validated pipeline syntax offline before pushing

### Cleanup

```bash title="Terminal"
rm -f ~/rebash-gitlab/module-04/app-name.txt ~/rebash-gitlab/module-04/lint-report.txt ~/rebash-gitlab/module-04/test-out.txt
# Keep src/ and .gitlab-ci.yml for module 05
```

## Validation








- [ ] Lab commands run under `~/rebash-gitlab/module-04/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough








Production practice for **Pipeline Syntax (.gitlab-ci.yml)** always combines:

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








!!! warning "Combining `only` and `rules` on the same job — pick one model (`rules`)."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Forgetting `workflow` and paying for duplicate MR + branch pipelines."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices








- Encode Pipeline Syntax (.gitlab-ci.yml) changes as code and review them in pull requests
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








**Pipeline Syntax (.gitlab-ci.yml)** is essential for Cloud and DevOps engineers working with gitlab. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions






1. What does needs change compared with stage-only ordering?
2. How do rules differ from only/except, and why prefer rules?
3. When is parallel matrix the right tool?
4. How can a malicious merge request abuse overly broad rules?
5. What is workflow rules for at the pipeline level?

!!! tip "Sample answer — question 2"
    Confirm whether the job was skipped by rules, blocked by needs on a failed dependency, or never created because workflow rules prevented the pipeline.

!!! tip "Sample answer — question 4"
    Prefer least-privilege rules: block pipelines from untrusted forks where secrets are available, keep production deploys manual on the default branch.

## Related Tutorials








- [Course overview](index.md)
- [Pipeline Design: DAGs and Includes](pipeline-design-dags-and-includes.md)

## References








- [CI/CD YAML syntax](https://docs.gitlab.com/ee/ci/yaml/)  
- [Job rules](https://docs.gitlab.com/ee/ci/jobs/job_rules.html)
