---
title: "GitLab CI/CD Cheat Sheet"
description: "Quick-reference patterns for GitLab CI — stages, jobs, rules, runners, variables, artefacts, matrix builds, security gates, and cost traps."
difficulty: beginner
estimated_time: "10 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: cheatsheets
tags:
  - cheatsheets
  - cicd
  - gitlab
comments: false
---

# GitLab CI/CD Cheat Sheet

Scannable patterns for the [CI/CD track](../gitlab/index.md). Use full tutorials when you need *why*, not only *how*.

!!! note "Other platforms"
    Jenkins and GitHub Actions come later on REBASH Academy — this sheet covers **GitLab CI** only.

## Core concepts

| Concept | GitLab CI keyword / location |
|---------|------------------------------|
| Pipeline config | `.gitlab-ci.yml` (repository root) |
| Phase ordering | `stages:` — jobs declare `stage:` |
| Job definition | Named job with `script:` (required) |
| Conditional run | `rules:` or `workflow:rules:` |
| DAG dependencies | `needs:` |
| Job container | `image:` |
| Runner selection | `tags:` on job; runner registration tags |
| Secrets | CI/CD variables (masked, protected, file type) |
| Manual gate | `when: manual` |
| Matrix fan-out | `parallel: matrix:` |
| Artefacts | `artifacts:` |
| Cache | `cache:` |
| Deploy target | `environment:` |

## Pipeline anatomy

| Stage | Typical jobs |
|-------|----------------|
| Validate | Lint YAML, SAST config, secret detection |
| Test | Unit, integration (fail fast) |
| Build | Compile, Docker build, package |
| Scan | Container, dependency, secret detection |
| Deploy | Staging (manual), production (protected) |

## Quick commands and lint

| Task | Command / tool |
|------|----------------|
| CI lint (UI) | **Build → Pipeline editor → Validate** |
| CI lint (API) | `curl --form "content=@.gitlab-ci.yml" .../ci/lint` |
| Runner register | `gitlab-runner register` |
| Runner verify | `gitlab-runner verify` |
| Local YAML parse | `python -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml'))"` |

## Stages, jobs, and rules

```yaml
stages:
  - test
  - build

unit-test:
  stage: test
  image: python:3.12-slim
  script:
    - pytest -q
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

| Keyword | Purpose |
|---------|---------|
| `stages:` | Ordered list — every `stage:` on a job must appear here |
| `rules:` | Per-job when to create/skip (replaces legacy `only`/`except`) |
| `workflow:rules:` | Whether to create a pipeline at all |
| `when: manual` | Job waits for play button |
| `allow_failure: true` | Job can fail without failing pipeline — use sparingly on gates |

## Runners and executors

| Topic | Notes |
|-------|-------|
| Shared vs self-hosted | Shared = ops-free; self-hosted = data residency, GPU, cost control |
| Docker executor | Isolated job container via `image:` |
| Kubernetes executor | Pod per job; watch cluster autoscaler lag |
| Runner tags | Job `tags:` must match runner tags |
| DinD | `docker:*-cli` image + `docker:*-dind` service for image builds |

## Variables and secrets

| Rule | Detail |
|------|--------|
| Never in Git | Use **Settings → CI/CD → Variables** |
| Masked | Values hidden in job logs when matched |
| Protected | Available only on protected branches/tags |
| File type | Written to temp file; path in `$VAR_NAME` |
| OIDC > long-lived keys | Federated cloud roles from CI job token |
| Scope by environment | Staging creds ≠ production creds |
| Rotate on leak | Invalidate token; audit pipeline history |

## Artifacts, cache, dependencies

| Pattern | Pitfall |
|---------|---------|
| Pass build output via `artifacts:` | Expiry too short — downstream job fails |
| `needs:` + artefacts | Use `dependencies:` to limit which artefacts download |
| Cache `key: $CI_COMMIT_REF_SLUG` | Wrong key → cold cache every run |
| Huge artefacts | Minutes + storage cost — publish reports, not full `node_modules` |

```yaml
build:
  script:
    - make dist
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

deploy:
  needs:
    - build
  script:
    - deploy dist/
```

## Matrix and parallelism

```yaml
unit-test:
  parallel:
    matrix:
      - PYTHON: ["3.11", "3.12"]
  image: python:${PYTHON}-slim
  script:
    - pytest -q
```

| Pattern | When to use |
|---------|-------------|
| `parallel: matrix:` | Test fan-out across versions or OS labels |
| `parallel: 4` | Split test suite by index |
| `needs:` | Skip waiting for entire stage when only one upstream job matters |

## Security gates

| Gate | When |
|------|------|
| Secret detection | Every MR (`secret_detection` template) |
| SAST / dependency scan | Before merge to default branch |
| Container scan | After build, before deploy |
| Manual approval | Staging/production promote (`when: manual`) |
| Protected environment | RBAC on deploy jobs |

```yaml
scan-image:
  stage: scan
  needs: [build-image]
  script:
    - trivy image --exit-code 1 --severity CRITICAL "$IMAGE_TAG"

deploy-staging:
  stage: deploy
  needs: [scan-image]
  environment:
    name: staging
  when: manual
  script:
    - deploy "$IMAGE_TAG"
```

## Environments and deploy

| Keyword | Purpose |
|---------|---------|
| `environment: name` | Tracks deployment history per environment |
| `environment: url` | Link in MR and Environments UI |
| `environment: on_stop` | Job to tear down review apps |
| Protected environments | Restrict who may deploy |
| `resource_group:` | Serialise deploys to same target |

## Docker build in CI

```yaml
variables:
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

build-image:
  image: docker:27-cli
  services:
    - docker:27-dind
  before_script:
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"
  script:
    - docker build -t "$IMAGE_TAG" .
    - docker push "$IMAGE_TAG"
```

## Cost and secret landmines

| Landmine | Mitigation |
|----------|------------|
| Shared runner minutes exhaustion | Cache deps; matrix only what you need; self-host heavy jobs |
| DinD layer cache disabled | Registry cache / buildx |
| Unbounded matrix | Cap OS × version combinations |
| Artefact storage growth | Retention policy; don't artefact `target/` |
| Fork MR pipelines with prod secrets | Restrict protected variables; use merge request pipelines carefully |
| `:latest` deploy tags | Immutable SHA tags for promote |
| Skipping scan with `allow_failure` | Policy waiver only with ticket |

## Common mistakes

- Fixing CI by disabling tests or scan jobs
- Wrong stage name not in top-level `stages:` list
- Rebuilding image on deploy instead of promoting SHA tag
- Production secrets available to unprotected branch pipelines
- No CI lint in pre-merge checks
- Confusing `cache:` (acceleration) with `artifacts:` (required handoff)

## Related

- Track: [CI/CD](../gitlab/index.md)
- Start: [Introduction to CI/CD](../gitlab/introduction-to-cicd-and-delivery-models.md)
- [GitLab CI Fundamentals](../gitlab/gitlab-ci-fundamentals.md)
- [GitLab Runners and Executors](../gitlab/gitlab-runners-and-executors.md)
- Lab: [Pipeline Failure Triage](../labs/cicd-pipeline-triage.md)
- Lab: [Docker Build, Scan, and Deploy Gate](../labs/cicd-docker-secure-gate.md)
- Quiz: [CI/CD Fundamentals](../quizzes/cicd-fundamentals.md)
- Interview bank: [CI/CD interview prep](../interview/cicd.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)
