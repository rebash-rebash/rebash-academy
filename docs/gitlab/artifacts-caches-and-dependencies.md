---
title: "Artifacts, Caches, and Dependencies"
description: "Use GitLab CI artefacts, reports, dependency cache, build cache, expiration, and job-to-job sharing for reproducible pipelines."
difficulty: intermediate
estimated_time: "40–55 min"
technology: gitlab
category: gitlab
module: "Module 7 · Artifacts & Cache"
learning_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - gitlab-ci
  - artifacts
  - cache
prerequisites:
  - gitlab/variables-secrets-and-oidc
next:
  - gitlab/building-docker-images-in-ci
related:
  - gitlab/pipeline-syntax-gitlab-ci-yml
  - gitlab/testing-reports-and-quality-gates
labs: []
projects: []
interview: interview/gitlab
certifications:
  - GitLab Certified CI/CD Associate
tags:
  - gitlab
  - cicd
  - artifacts
  - cache
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---


# Artifacts, Caches, and Dependencies

## Overview








Configure `artifacts:` and `cache:` so a build job produces a shareable package, a test job consumes it, and dependency installs reuse a keyed cache without treating cache as a correctness guarantee.

**Artefacts** are job outputs GitLab stores and can pass to later jobs or attach to merge requests (packages, JUnit reports, coverage). **Cache** speeds installs by restoring files between pipelines; it is best-effort and must not replace pinned lockfiles. Reports (`junit`, `coverage_report`, and similar) surface quality signals in the MR UI.

This is a core tutorial in **Module 7 · Artifacts & Cache** of the REBASH Academy **GitLab CI/CD for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites








- [Variables, Secrets, and OIDC](variables-secrets-and-oidc.md)

## Learning Objectives








By the end of this tutorial, you will be able to:

- [ ] Declare `artifacts:paths` with `expire_in`  
- [ ] Share artefacts across jobs with `dependencies` / `needs`  
- [ ] Configure a dependency cache with a lockfile-based `key`  
- [ ] Distinguish artefacts from cache and from container images  
- [ ] Attach a simple report artefact for the MR widget

## Architecture








This topic’s control points and relationships are shown below.

![GitLab artefacts and cache](../assets/excalidraw/gitlab-artifacts-cache.svg)

## Theory








### What it is

GitLab CI separates **what you ship between jobs** from **what you hope to reuse for speed**:

| Mechanism | Purpose | Guaranteed? |
|-----------|---------|-------------|
| `artifacts:` | Persist outputs for later jobs / download / MR | Yes (within retention) |
| `cache:` | Speed dependency or build dirs | No — may miss or be empty |
| Reports | Structured UI feedback (tests, coverage) | Via `artifacts:reports` |

Artefacts can expire (`expire_in`), be limited to certain jobs (`dependencies`), or ride DAG edges (`needs`). Cache keys often hash `package-lock.json`, `poetry.lock`, or `go.sum` so installs invalidate when dependencies change.

### Why it matters

Slow pipelines waste runner minutes and delay review. Wrong cache design causes flaky “works on my branch” builds when a stale cache hides a missing lockfile. Artefacts make builds auditable: the same tarball or binary that passed tests can be promoted. Reports turn CI into a review surface instead of a log scrape.

### How it works

1. A **build** job writes files under a path (for example `dist/`) and lists them in `artifacts:paths` with `expire_in`.  
2. A **test** job declares `needs: [build]` (or `dependencies`) so GitLab downloads those artefacts before `script`.  
3. An optional **cache** restores `node_modules/` or `.cache/pip` using a key derived from the lockfile; the job still runs install if the cache is cold.  
4. Test jobs may set `artifacts:reports:junit` so failures appear on the merge request.  
5. Expired artefacts disappear; cache may be cleared by runners or policy — never assume either is permanent storage.

Prefer short retention for intermediate binaries; keep release artefacts on tags or push immutable images to a registry.

### Key concepts and comparisons

| Concern | Artefacts | Cache |
|---------|-----------|-------|
| Correctness | Part of the pipeline contract | Optimisation only |
| Cross-job | Explicit download | Same key / same project scope |
| Security | Can contain secrets — scope carefully | Same risk if you cache credentials |
| UI | Downloadable; reports in MR | Opaque speed-up |

### Common pitfalls

- Treating cache as a substitute for committing lockfiles.  
- Omitting `expire_in` and filling storage with huge trees.  
- Caching the entire workspace including secrets or `.env`.  
- Expecting artefacts without listing paths or after a failed job (`when: on_success` default).  
- Confusing job artefacts with Container Registry images.

## Hands-on Lab

### Objective

Create a pipeline with cache keys and job artefacts, simulate cache and artefact directories locally, and validate YAML offline.

### Prerequisites

- Python 3 with PyYAML (`pip install pyyaml`)
- Optional: GitLab runner to observe cache restore in job logs

### Lab environment

Workspace: `~/rebash-gitlab/module-07`

File-first lab. Local directories mimic runner cache and artefact paths.

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-gitlab/module-07/src && cd ~/rebash-gitlab/module-07
```

### Real-world scenario

Your Node/Python monorepo rebuilds dependencies on every job, wasting minutes. Platform engineering asks for a lockfile-keyed cache on the install job and build artefacts passed to deploy. You model both patterns and prove directory layout locally before pushing.

### Step-by-step tasks

#### Task 1 – Create dependency manifest and app

Create `requirements.txt`:

```text title="requirements.txt"
# minimal lab dependency file — no external install required offline
```

Create `src/app.py`:

```python title="app.py"
print("artifacts-cache ok")
```

#### Task 2 – Author cache and artefact jobs

Create `.gitlab-ci.yml`:

```yaml title=".gitlab-ci.yml"
variables:
  PIP_CACHE_DIR: .cache/pip

stages:
  - prepare
  - build
  - deploy

install_deps:
  stage: prepare
  image: python:3.12-alpine
  cache:
    key:
      files:
        - requirements.txt
    paths:
      - .cache/pip
  script:
    - mkdir -p .cache/pip dist
    - echo "deps-ready" > dist/deps-status.txt
  artifacts:
    paths:
      - dist/deps-status.txt
    expire_in: 1 day

build_app:
  stage: build
  image: python:3.12-alpine
  needs:
    - job: install_deps
      artifacts: true
  cache:
    key:
      files:
        - requirements.txt
    paths:
      - .cache/pip
    policy: pull
  script:
    - test -f dist/deps-status.txt
    - mkdir -p dist
    - python src/app.py | tee dist/build-output.txt
  artifacts:
    paths:
      - dist/build-output.txt
    expire_in: 1 day

deploy_stub:
  stage: deploy
  image: alpine:3.20
  needs:
    - job: build_app
      artifacts: true
  script:
    - test -f dist/build-output.txt
    - cat dist/build-output.txt
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

Validate offline:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-gitlab/module-07
python3 -c "
import yaml
d = yaml.safe_load(open('.gitlab-ci.yml'))
assert d['install_deps']['cache']['key']['files'] == ['requirements.txt']
assert d['build_app']['needs'][0]['artifacts'] is True
print('OK cache and artifacts')
"
```

!!! example "Expected output"
    Prints `OK cache and artifacts`.


#### Task 3 – Simulate cache paths and artefact hand-off locally

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-gitlab/module-07
mkdir -p .cache/pip dist
echo "deps-ready" > dist/deps-status.txt
echo "simulated pip cache" > .cache/pip/lab-marker.txt
test -f dist/deps-status.txt
test -f .cache/pip/lab-marker.txt
python3 src/app.py | tee dist/build-output.txt
grep -q 'artifacts-cache ok' dist/build-output.txt
cat dist/build-output.txt
```

!!! example "Expected output"
    Terminal shows `artifacts-cache ok`; cache marker and dist files exist.


### Validation steps

- [ ] Cache key references `requirements.txt`
- [ ] `install_deps` publishes `dist/deps-status.txt`
- [ ] `build_app` pulls cache with `policy: pull` and needs install artefacts
- [ ] `deploy_stub` consumes `dist/build-output.txt`
- [ ] Local `.cache/pip` and `dist/` mirror runner paths

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Cache never hits | Key changes every commit | Key on lockfile (`requirements.txt`) not commit SHA alone |
| Empty artefact in later job | Missing `needs` artefacts | Set `artifacts: true` on the need entry |
| Huge cache uploads | Caching build outputs | Cache dependencies; artefact final binaries separately |
| Deploy job runs on MR | Missing branch rule | Gate `deploy_stub` to default branch |

### Challenge exercise

Add a `cache:policy: push` only on `install_deps` and document in a comment why `build_app` uses `pull`. Re-validate YAML.

### Learning outcomes

- Keyed caches to dependency files instead of rebuilding every job
- Passed build artefacts downstream with `needs`
- Simulated cache and dist directories locally
- Validated pipeline YAML offline

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
rm -rf ~/rebash-gitlab/module-07/.cache ~/rebash-gitlab/module-07/dist
# Keep src/, requirements.txt, and .gitlab-ci.yml for module 08
```

## Validation








- [ ] Lab commands run under `~/rebash-gitlab/module-07/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough








Production practice for **Artifacts, Caches, and Dependencies** always combines:

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








!!! warning "Treating cache as a substitute for committing lockfiles.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Omitting `expire_in` and filling storage with huge trees.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices








- Encode Artifacts, Caches, and Dependencies changes as code and review them in pull requests
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








**Artifacts, Caches, and Dependencies** is essential for Cloud and DevOps engineers working with gitlab. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions






1. What is the difference between cache and artifacts in GitLab CI?
2. A later job cannot find a file produced earlier — how do you diagnose it?
3. When should cache keys include a lockfile hash?
4. What security issue arises from caching world-writable directories?
5. How does expire_in help control storage cost?

!!! tip "Sample answer — question 2"
    Confirm the producer declared artifacts paths, the consumer needs/dependencies includes that job, and paths match. Cache is best-effort and must not be the only way to pass build outputs.

!!! tip "Sample answer — question 4"
    Treat caches as untrusted acceleration: pin keys, avoid storing secrets, and keep artifact retention short.

## Related Tutorials








- [Course overview](index.md)
- [Building Docker Images in CI](building-docker-images-in-ci.md)

## References








- [Job artefacts](https://docs.gitlab.com/ee/ci/yaml/#artifacts) · [Caching](https://docs.gitlab.com/ee/ci/caching/) · [Reports](https://docs.gitlab.com/ee/ci/yaml/artifacts_reports.html)
