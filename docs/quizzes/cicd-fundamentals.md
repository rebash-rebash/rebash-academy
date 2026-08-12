---
title: "Quiz — CI/CD Fundamentals"
description: "40-question GitLab CI assessment — stages, jobs, rules, runners, variables, artefacts, needs, environments, and security scanning."
difficulty: intermediate
estimated_time: "45–60 min"
passing_score: "70% (28/40)"
author: Shaik Basha
last_updated: "2026-07-28"
category: quizzes
tags:
  - quizzes
  - cicd
  - gitlab
  - assessment
comments: false
---

# Quiz — CI/CD Fundamentals

## Quiz Overview

Assess the REBASH Academy GitLab CI track: pipeline anatomy, runners, secrets, quality gates, and secure deploy patterns.

| Attribute | Value |
|-----------|--------|
| Topic | GitLab CI fundamentals |
| Questions | 40 |
| Passing score | 70% (28 correct) |
| Estimated time | 45–60 minutes |

!!! tip "How to use this quiz"
    Select an answer for each question, then **Submit quiz** for a scored result. Progress is saved in this browser. Explanations unlock after you submit.

!!! note "Other platforms"
    Jenkins and GitHub Actions come later on REBASH Academy — this quiz covers **GitLab CI** only.

## Learning Objectives

- [ ] Explain CI/CD delivery models and pipeline stage ordering
- [ ] Configure GitLab CI stages, jobs, rules, and workflow triggers
- [ ] Apply runner, variable, artefact, and cache patterns safely
- [ ] Design matrix builds, scan gates, and protected deploy approvals
- [ ] Triage failed pipelines using logs, lint, and DAG evidence

## Section 1 — Foundations

### Question 1

What is the primary difference between **continuous delivery** and **continuous deployment**?

**Difficulty:** Beginner

**Options:**

- **A.** Continuous deployment automatically releases every passing change to production; continuous delivery stops before production unless a human approves
- **B.** Continuous delivery only applies to scheduled pipelines; continuous deployment only applies to tags
- **C.** Continuous deployment means manual staging only
- **D.** There is no practical difference — the terms are interchangeable

??? success "Reveal answer"
    **Correct answer: A**

    Delivery keeps production promote as a conscious decision; deployment automates that last step when policy allows.

    **Related concepts**

    - Delivery models
    - Trunk-based flow

### Question 2

Where does GitLab CI read its pipeline definition by default?

**Difficulty:** Beginner

**Options:**

- **A.** `Jenkinsfile` in the repository root
- **B.** `.gitlab-ci.yml` in the repository root
- **C.** `.github/workflows/ci.yml` only
- **D.** GitLab project settings UI exclusively — not in Git

??? success "Reveal answer"
    **Correct answer: B**

    Pipeline-as-code lives in `.gitlab-ci.yml` unless overridden in project settings.

    **Related concepts**

    - GitLab CI configuration
    - Pipeline as code

### Question 3

Which keyword controls whether GitLab creates a pipeline at all for a given push or MR?

**Difficulty:** Intermediate

**Options:**

- **A.** `artifacts:`
- **B.** `pages:`
- **C.** `workflow:rules:`
- **D.** `cache:`

??? success "Reveal answer"
    **Correct answer: C**

    `workflow:rules:` evaluates before jobs; job-level `rules:` decide individual job inclusion.

    **Related concepts**

    - Pipeline triggers
    - Conditional pipelines

### Question 4

A merge request pipeline should run tests but skip deploy. Which pattern is most appropriate?

**Difficulty:** Intermediate

**Options:**

- **A.** Remove the deploy job from `.gitlab-ci.yml` entirely
- **B.** Set `allow_failure: true` on every test job
- **C.** Use `only: [main]` on deploy without rules
- **D.** Deploy job `rules:` with `if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH` only (no MR rule)

??? success "Reveal answer"
    **Correct answer: D**

    Scope deploy jobs to protected/default branch pipelines; MR pipelines run validate and test only.

    **Related concepts**

    - rules:
    - Merge request pipelines

### Question 5

Which GitLab CI keyword defines the ordered list of pipeline phases?

**Difficulty:** Beginner

**Options:**

- **A.** `stages:`
- **B.** `matrix:`
- **C.** `secrets:`
- **D.** `runners:`

??? success "Reveal answer"
    **Correct answer: A**

    Jobs reference a `stage:` value that must appear in `stages:`.

    **Related concepts**

    - Pipeline anatomy
    - Stage ordering

### Question 6

A job references `stage: verify` but `verify` is not listed under top-level `stages:`. What typically happens?

**Difficulty:** Intermediate

**Options:**

- **A.** The job runs in parallel with all other jobs regardless
- **B.** Pipeline validation fails or the job cannot run — stage mismatch
- **C.** GitLab silently maps it to the last stage
- **D.** Only the script section is skipped; the job is marked success

??? success "Reveal answer"
    **Correct answer: B**

    Stage names must be declared — a common triage finding in the pipeline failure lab.

    **Related concepts**

    - YAML validation
    - CI triage

### Question 7

What does `needs:` in GitLab CI primarily enable?

**Difficulty:** Intermediate

**Options:**

- **A.** Encrypting CI variables at rest
- **B.** Running jobs on Windows runners only
- **C.** DAG-style dependencies — start a job when listed jobs finish, not only after entire stage
- **D.** Automatic production deployment

??? success "Reveal answer"
    **Correct answer: C**

    `needs:` builds a directed acyclic graph for faster fan-in/fan-out pipelines.

    **Related concepts**

    - Pipeline DAG
    - Parallelism

### Question 8

Which `rules:` condition runs a job only for merge request pipelines?

**Difficulty:** Intermediate

**Options:**

- **A.** `if: $CI_COMMIT_TAG`
- **B.** `if: $CI_PIPELINE_SOURCE == "schedule"`
- **C.** `if: $CI_COMMIT_BRANCH == "main"` alone on every push
- **D.** `if: $CI_PIPELINE_SOURCE == "merge_request_event"`

??? success "Reveal answer"
    **Correct answer: D**

    MR pipelines set `$CI_PIPELINE_SOURCE` to `merge_request_event` — use in `rules:` for MR-only jobs.

    **Related concepts**

    - Merge request pipelines
    - rules:

### Question 9

Trunk-based development in CI/CD context means?

**Difficulty:** Beginner

**Options:**

- **A.** Short-lived branches merged frequently to main with pipeline gates on every merge
- **B.** One commit per year on a long-lived release branch
- **C.** No use of Git tags ever
- **D.** Disabling all branch protection rules

??? success "Reveal answer"
    **Correct answer: A**

    Small batches + CI on main/MR reduce merge pain and deployment risk.

    **Related concepts**

    - Branch protection
    - Delivery models

### Question 10

First step when a merge pipeline fails unexpectedly?

**Difficulty:** Beginner

**Options:**

- **A.** Disable the failing job permanently
- **B.** Identify the first failed job in stage/DAG order and read its log
- **C.** Delete the pipeline and re-run without cache
- **D.** Force-push to main to bypass checks

??? success "Reveal answer"
    **Correct answer: B**

    Triage starts with the earliest failure and log evidence — not guesswork.

    **Related concepts**

    - Pipeline triage
    - Observability

## Section 2 — Runners, Variables, and Secrets

### Question 11

GitLab CI jobs execute on?

**Difficulty:** Beginner

**Options:**

- **A.** Only the developer laptop
- **B.** AWS Lambda exclusively
- **C.** Runners registered to the GitLab instance
- **D.** The GitLab web UI server process

??? success "Reveal answer"
    **Correct answer: C**

    Runners pick up jobs via the GitLab coordinator; executors define isolation (Docker, shell, Kubernetes).

    **Related concepts**

    - Runners and executors
    - Shared vs self-hosted

### Question 12

A job must run on a runner tagged `gpu`. How do you select it?

**Difficulty:** Beginner

**Options:**

- **A.** Set `image: gpu` only
- **B.** Add `stage: gpu`
- **C.** Set `variables: GPU: "true"` without tags
- **D.** Add `tags: [gpu]` to the job definition

??? success "Reveal answer"
    **Correct answer: D**

    Job `tags:` must match tags registered on the runner.

    **Related concepts**

    - Runner tags
    - Self-hosted runners

### Question 13

Which keyword runs a job inside a specific container image on a Docker executor?

**Difficulty:** Intermediate

**Options:**

- **A.** `image:`
- **B.** `services:` alone without image
- **C.** `pages:`
- **D.** `include:`

??? success "Reveal answer"
    **Correct answer: A**

    `image:` sets the job container; `services:` adds sidecar containers (e.g. DinD, Postgres).

    **Related concepts**

    - Docker executor
    - Job containers

### Question 14

Best practice for AWS credentials in GitLab CI pipelines?

**Difficulty:** Intermediate

**Options:**

- **A.** Long-lived IAM user keys in `.gitlab-ci.yml`
- **B.** OIDC federation — short-lived tokens scoped to the pipeline identity
- **C.** Commit access keys to a private fork only
- **D.** Store keys in README for onboarding

??? success "Reveal answer"
    **Correct answer: B**

    Federated roles beat long-lived keys; rotate and scope per environment.

    **Related concepts**

    - Least privilege
    - OIDC in CI

### Question 15

GitLab **masked** CI/CD variables prevent?

**Difficulty:** Intermediate

**Options:**

- **A.** All network egress from runners
- **B.** Merge requests from forks
- **C.** Variable values appearing in job logs when matched
- **D.** Docker builds entirely

??? success "Reveal answer"
    **Correct answer: C**

    Masking reduces accidental secret exposure in logs — not a substitute for scoping and protected branches.

    **Related concepts**

    - Secrets management
    - Protected variables

### Question 16

Why are fork merge request pipelines a secret-leak risk?

**Difficulty:** Advanced

**Options:**

- **A.** Forks cannot use Git
- **B.** All pipelines are disabled on forks automatically
- **C.** Forks always inherit production kubeconfig by default
- **D.** Malicious MR code may exfiltrate secrets if pipelines run with production variables on untrusted branches

??? success "Reveal answer"
    **Correct answer: D**

    Scope protected variables to protected branches; treat fork MR code as untrusted.

    **Related concepts**

    - Fork MR security
    - Protected variables

### Question 17

Self-hosted GitLab runners are often chosen when?

**Difficulty:** Intermediate

**Options:**

- **A.** Data must stay in a private network, or you need specialised hardware/GPU
- **B.** You need zero maintenance and unlimited free minutes always
- **C.** You never run Docker builds
- **D.** You want to disable all secrets

??? success "Reveal answer"
    **Correct answer: A**

    Trade ops burden for control, residency, and cost at scale.

    **Related concepts**

    - Runner selection
    - Cost vs control

### Question 18

How should a large private key be passed to a GitLab CI job?

**Difficulty:** Intermediate

**Options:**

- **A.** Commit the key to a protected branch
- **B.** CI/CD variable of type **File** — path exposed as `$VAR_NAME`
- **C.** Paste into job `script:` as echo
- **D.** Store in job name for visibility

??? success "Reveal answer"
    **Correct answer: B**

    File-type variables write content to a temp path — safer than inline multiline values in logs.

    **Related concepts**

    - CI/CD variables
    - Secret hygiene

### Question 19

Protected CI variables in GitLab (protected + masked) should be limited to?

**Difficulty:** Intermediate

**Options:**

- **A.** Every feature branch and fork pipeline
- **B.** Public unprotected branches only
- **C.** Protected branches/tags pipelines only
- **D.** Scheduled pipelines on personal repos only

??? success "Reveal answer"
    **Correct answer: C**

    Scope production secrets to protected refs.

    **Related concepts**

    - Protected branches
    - Variable scope

### Question 20

Primary purpose of secret detection in merge pipelines?

**Difficulty:** Beginner

**Options:**

- **A.** Speed up Docker layer caching
- **B.** Replace unit tests
- **C.** Increase runner parallelism automatically
- **D.** Block or warn on committed tokens, keys, or passwords before merge

??? success "Reveal answer"
    **Correct answer: D**

    Catch leaks early — pair with rotation if history contains secrets.

    **Related concepts**

    - Secret detection
    - Supply chain

## Section 3 — Build, Artefacts, Cache, and Matrix

### Question 21

GitLab CI keyword to pass files to later jobs?

**Difficulty:** Beginner

**Options:**

- **A.** `artifacts:`
- **B.** `include:`
- **C.** `workflow:`
- **D.** `pages:`

??? success "Reveal answer"
    **Correct answer: A**

    Artefacts upload job output for downstream consumption or download.

    **Related concepts**

    - Artefacts
    - Job dependencies

### Question 22

Downstream job receives artefacts from only one upstream job in the same stage. Which keyword limits artefact download?

**Difficulty:** Intermediate

**Options:**

- **A.** `cache:` only
- **B.** `dependencies:` listing specific job names
- **C.** `workflow:rules:`
- **D.** `resource_group:`

??? success "Reveal answer"
    **Correct answer: B**

    By default `needs:` jobs may fetch all prior-stage artefacts; `dependencies:` restricts which artefact sets download.

    **Related concepts**

    - Artefacts
    - needs:

### Question 23

Purpose of CI cache (`cache:` in GitLab CI)?

**Difficulty:** Beginner

**Options:**

- **A.** Permanent storage of release binaries for seven years
- **B.** Replace container registries
- **C.** Reuse dependency directories between pipeline runs to reduce duration and cost
- **D.** Store production database backups

??? success "Reveal answer"
    **Correct answer: C**

    Cache is best-effort acceleration — not a durable artefact store.

    **Related concepts**

    - Cache keys
    - Cost optimisation

### Question 24

GitLab CI matrix-style parallel jobs are configured with?

**Difficulty:** Intermediate

**Options:**

- **A.** `only: matrix`
- **B.** `credentials: matrix`
- **C.** `archiveArtifacts matrix`
- **D.** `parallel: matrix:` with variable combinations

??? success "Reveal answer"
    **Correct answer: D**

    `parallel:matrix` generates multiple job instances from variable sets.

    **Related concepts**

    - GitLab matrix
    - Test fan-out

### Question 25

Which variable is commonly used in a cache key to scope per branch?

**Difficulty:** Intermediate

**Options:**

- **A.** `$CI_COMMIT_REF_SLUG`
- **B.** `$CI_JOB_NAME` only on every project
- **C.** `$GITLAB_USER_LOGIN` exclusively
- **D.** `$CI_PIPELINE_ID` alone always

??? success "Reveal answer"
    **Correct answer: A**

    Branch-scoped cache keys reduce cross-branch pollution whilst still allowing reuse on the same branch.

    **Related concepts**

    - Cache keys
    - Branch pipelines

### Question 26

Risk of an unbounded CI matrix (10 OS × 10 Python × 10 Node versions)?

**Difficulty:** Intermediate

**Options:**

- **A.** Zero runner minutes consumed
- **B.** Runner minute explosion and queue delays — cost and feedback latency
- **C.** Automatic merge to production
- **D.** Secrets become unnecessary

??? success "Reveal answer"
    **Correct answer: B**

    Cap matrix dimensions to what the team will actually triage.

    **Related concepts**

    - Cost landmines
    - Matrix design

### Question 27

Docker-in-Docker (DinD) in GitLab CI is commonly used for?

**Difficulty:** Intermediate

**Options:**

- **A.** Linting Markdown only
- **B.** Replacing Git
- **C.** Running `docker build` / `docker push` inside a CI job
- **D.** Disabling container scanning

??? success "Reveal answer"
    **Correct answer: C**

    DinD or alternatives (Kaniko, buildx remote cache) build images in pipeline agents.

    **Related concepts**

    - Building Docker in CI
    - Registry push

### Question 28

Immutable deployment best practice for container promote?

**Difficulty:** Intermediate

**Options:**

- **A.** Rebuild `:latest` on every deploy job
- **B.** Deploy `:latest` without recording SHA
- **C.** Mutate running container filesystem in production
- **D.** Build once, tag with commit SHA, promote the same tag through staging and production

??? success "Reveal answer"
    **Correct answer: D**

    Same bits everywhere — rollback means redeploy previous SHA tag.

    **Related concepts**

    - Immutable artefacts
    - Deploy patterns

### Question 29

GitLab CI report artefact that surfaces test results in the MR UI uses?

**Difficulty:** Intermediate

**Options:**

- **A.** `artifacts:reports:junit:` (or unit test report type)
- **B.** `pages:` only
- **C.** `cache: reports`
- **D.** `include: junit`

??? success "Reveal answer"
    **Correct answer: A**

    Report artefacts integrate test and coverage output into GitLab merge request widgets.

    **Related concepts**

    - Test reports
    - Quality gates

### Question 30

When should `needs:` omit waiting for an entire stage?

**Difficulty:** Intermediate

**Options:**

- **A.** Never — stages are always sufficient
- **B.** When downstream job depends only on specific upstream jobs, not every job in the prior stage
- **C.** Only for manual production deploys
- **D.** When disabling tests

??? success "Reveal answer"
    **Correct answer: B**

    DAG edges shorten critical path when stages contain parallel jobs.

    **Related concepts**

    - needs:
    - Pipeline optimisation

## Section 4 — Security, Environments, and Operations

### Question 31

Container image scanning in CI should run?

**Difficulty:** Intermediate

**Options:**

- **A.** Only once per year
- **B.** After production deploy only
- **C.** After build, before deploy promote — fail or gate on policy severity
- **D.** Never — scanning slows pipelines unacceptably always

??? success "Reveal answer"
    **Correct answer: C**

    Scan before staging/production promote; tune severity thresholds to team SLA.

    **Related concepts**

    - Security scanning
    - Deploy gates

### Question 32

GitLab manual staging deploy is configured with?

**Difficulty:** Intermediate

**Options:**

- **A.** `when: always` on every job
- **B.** `allow_failure: true` on scan
- **C.** Removing the deploy stage
- **D.** `when: manual` on the deploy job (often with `environment:`)

??? success "Reveal answer"
    **Correct answer: D**

    Manual jobs wait for human play — pair with protected environments for RBAC.

    **Related concepts**

    - Protected environments
    - Manual approvals

### Question 33

GitLab **protected environments** restrict?

**Difficulty:** Intermediate

**Options:**

- **A.** Which roles/users may deploy to a named environment
- **B.** Only the number of pipeline stages
- **C.** Whether Docker is allowed globally
- **D.** Fork creation on the project

??? success "Reveal answer"
    **Correct answer: A**

    Protected environments enforce separation of duties on staging and production deploy jobs.

    **Related concepts**

    - Protected environments
    - RBAC

### Question 34

What does `environment: on_stop` enable?

**Difficulty:** Intermediate

**Options:**

- **A.** Automatic production rollback on every push
- **B.** A job that runs when an environment is stopped (e.g. tear down review app)
- **C.** Disabling all manual jobs
- **D.** Skipping scan stages

??? success "Reveal answer"
    **Correct answer: B**

    Review apps and ephemeral environments use `on_stop` for cleanup when the environment ends.

    **Related concepts**

    - Environments
    - Review apps

### Question 35

Setting `allow_failure: true` on a CRITICAL container scan job?

**Difficulty:** Advanced

**Options:**

- **A.** Best practice for all production pipelines
- **B.** Required by GitLab Free tier
- **C.** Generally wrong for policy — vulnerable images may ship unless explicitly waived
- **D.** Automatically fixes CVEs

??? success "Reveal answer"
    **Correct answer: C**

    Use waivers with tickets — do not silently ignore CRITICAL findings.

    **Related concepts**

    - Scan policy
    - Risk acceptance

### Question 36

Team standardises on GitLab with integrated registry, SAST, and container scanning templates. Primary advantage?

**Difficulty:** Intermediate

**Options:**

- **A.** No need for branch protection
- **B.** Eliminates all CVEs automatically
- **C.** Removes requirement for code review
- **D.** SCM, CI, registry, and security scanning in one platform with shared MR context

??? success "Reveal answer"
    **Correct answer: D**

    Integrated DevSecOps reduces context switching and surfaces findings in the merge request.

    **Related concepts**

    - GitLab strengths
    - DevSecOps integration

### Question 37

Air-gapped datacentre with self-managed GitLab and no outbound internet from runners. Likely runner choice?

**Difficulty:** Advanced

**Options:**

- **A.** Self-hosted runners with internal registry mirrors and offline scanner images
- **B.** GitLab.com shared runners exclusively
- **C.** Disable all CI — manual FTP deploys
- **D.** Pull every job image from Docker Hub on each run without mirror

??? success "Reveal answer"
    **Correct answer: A**

    Self-hosted runners with mirrored images and internal tooling suit restricted networks.

    **Related concepts**

    - Self-managed GitLab
    - Runner operations

### Question 38

Built-in GitLab Container Registry is typically addressed in CI as?

**Difficulty:** Intermediate

**Options:**

- **A.** Hard-coded Docker Hub username in script
- **B.** `$CI_REGISTRY`, `$CI_REGISTRY_IMAGE`, and `$CI_REGISTRY_USER` predefined variables
- **C.** `pages:` publish target
- **D.** SSH to developer laptop

??? success "Reveal answer"
    **Correct answer: B**

    GitLab injects registry variables when Container Registry is enabled on the project.

    **Related concepts**

    - Container Registry
    - Docker build in CI

### Question 39

Primary validation tool before pushing `.gitlab-ci.yml`?

**Difficulty:** Beginner

**Options:**

- **A.** `terraform apply`
- **B.** `kubectl delete namespace`
- **C.** GitLab CI Lint (UI or API) / local lint in pre-commit
- **D.** Force merge without checks

??? success "Reveal answer"
    **Correct answer: C**

    Catch schema and stage errors before consuming runner minutes.

    **Related concepts**

    - CI lint
    - Shift-left validation

### Question 40

GitLab CI/CD track capstone integrates which concerns holistically?

**Difficulty:** Advanced

**Options:**

- **A.** Only Markdown linting
- **B.** Git branching only — no deploy
- **C.** Git ignore patterns exclusively
- **D.** Pipeline authoring, scan gates, protected deploys, and Terraform handoff

??? success "Reveal answer"
    **Correct answer: D**

    The track builds from foundations through secure deploy and infrastructure automation.

    **Related concepts**

    - CI/CD capstone
    - DevOps breadth

## Score Summary

| Score | Band | Meaning |
|------:|------|---------|
| 36–40 | Excellent | Ready for advanced labs and CI/CD interviews |
| 28–35 | Good | Pass — revise weak modules |
| 20–27 | Needs improvement | Revisit tutorials and labs before interviews |
| ≤19 | Restart track | Work Modules 1–3 in order |

**Total questions:** 40 · **Passing score:** 28 (70%)

## Recommended Study Areas

- [CI/CD track](../gitlab/index.md)
- [GitLab CI Fundamentals](../gitlab/gitlab-ci-fundamentals.md)
- [GitLab Runners and Executors](../gitlab/gitlab-runners-and-executors.md)
- Lab: [Pipeline Failure Triage](../labs/cicd-pipeline-triage.md)
- Lab: [Docker Build, Scan, and Deploy Gate](../labs/cicd-docker-secure-gate.md)
- Cheat sheet: [GitLab CI/CD](../cheatsheets/cicd.md)
- Interview: [CI/CD](../interview/cicd.md)

## Interview Connection

Expect pipeline triage narratives (stage vs script failures), immutable SHA promote stories, scan gate trade-offs, fork MR secret risks, runner cost control, and protected environment RBAC. Use lab evidence: job logs, CI lint, manual deploy audit.

## References

1. [GitLab CI/CD documentation](https://docs.gitlab.com/ee/ci/)
2. [GitLab CI/CD YAML reference](https://docs.gitlab.com/ee/ci/yaml/)
3. [GitLab Runners documentation](https://docs.gitlab.com/runner/)
4. [GitLab Security scanning](https://docs.gitlab.com/ee/user/application_security/)
