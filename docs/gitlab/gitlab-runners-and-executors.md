---
title: GitLab Runners and Executors
description: "GitLab Runners and Executors is essential for engineers who operate GitLab CI in production — not only the team"
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: gitlab
tags:
  - cicd
  - gitlab
  - gitlab-ci
  - runners
prerequisites:
  - Completed tutorial 4 in this track (or equivalent GitLab CI awareness)
  - Lab repository from prior tutorials or a fresh `git init` workspace
comments: false
---

# GitLab Runners and Executors

## Overview

GitLab Runners and Executors is essential for engineers who operate GitLab CI in production — not only the team
that maintains runners. This lesson covers **GitLab Runner registration, executors (Docker, shell, Kubernetes), and isolation** with practical
`.gitlab-ci.yml` examples you can lint locally and run on GitLab.com free tier.

Other CI platforms exist and are covered in later REBASH tracks; here GitLab CI is the
focus. You will relate concepts to [Git](../git/index.md) merge requests, and prepare for
secure deploy patterns connecting to [Docker](../docker/index.md),
[Kubernetes](../kubernetes/index.md), and
[Terraform](../terraform/terraform-in-ci-cd-pipelines.md).

This is **Tutorial 5** in **Module 2: Runners and Configuration** of the REBASH Academy **GitLab CI/CD** track.

!!! tip "Free-tier and local lab options"
    Use **GitLab.com** free tier for real pipeline runs. Where a cloud runner is optional,
    each lab includes a **lint / dry-run** path with `glab ci lint`, Python YAML parsing, or
    **gitlab-ci-local** so you can validate `.gitlab-ci.yml` without spending CI minutes.



## Prerequisites

- Completed tutorial 4 in this track (or equivalent GitLab CI awareness)
- Lab repository from prior tutorials or a fresh `git init` workspace

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain how gitlab runners and executors applies in GitLab CI production pipelines
- [ ] Author and validate `.gitlab-ci.yml` for the concepts in this tutorial
- [ ] Choose appropriate runners, tags, and variables for the workload
- [ ] Connect this topic to merge request workflows and branch protection
- [ ] Troubleshoot a failed GitLab CI job using logs and lint tools

## Architecture

![Architecture diagram for GitLab Runners and Executors](../assets/images/gitlab-runners-and-executors.svg)

| Layer | Responsibility |
|-------|----------------|
| **Trigger** | Git push, MR, tag, schedule, manual |
| **Pipeline** | `.gitlab-ci.yml` automation definition in Git |
| **Runner** | Isolated compute executing job scripts |
| **Artefacts & cache** | Outputs and dependency acceleration |
| **Deploy target** | GitLab environment, cluster, or cloud account |

## Theory

### GitLab Runner architecture

The **GitLab Runner** is a separate agent process that polls GitLab for jobs, executes them
in an isolated environment, and streams logs back. Shared runners on GitLab.com are managed
by GitLab; self-managed runners register to your instance or project.

### Executors

| Executor | Isolation | Typical use |
|----------|-----------|-------------|
| Docker | Container per job | Most CI workloads |
| Shell | Host filesystem | Bare-metal build agents (use with care) |
| Kubernetes | Pod per job | Large fleets, autoscaling |
| SSH | Remote host | Legacy deploy targets |

### Registration

Register a runner with `gitlab-runner register`, providing the GitLab URL, registration token,
executor type, and default Docker image. Project-specific runners limit blast radius compared
to instance-wide runners with broad tags.

### Security

Runners execute untrusted code from merge requests. Use Docker or Kubernetes executors,
disable privileged mode unless required, and isolate production credentials to protected
runners and protected branches.


        ### Minimal GitLab CI test pipeline

        ```yaml
        stages:
  - test

unit-test:
  stage: test
  image: python:3.12-slim
  script:
    - pip install -r requirements.txt
    - pytest -q
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
        ```


### Production notes for GitLab Runners and Executors

Teams standardise GitLab CI templates but still integrate with external systems — container
registries, Kubernetes clusters, and cloud OIDC roles. Document **GitLab Runner registration, executors (Docker, shell, Kubernetes), and isolation** in your
internal runbook: who approves `.gitlab-ci.yml` changes, which runners touch production
credentials, and how rollbacks interact with [Git](../git/index.md) revert versus forward fix.

### Related tutorials in this module

Module progression builds depth: earlier tutorials establish vocabulary; later ones add security
scanning, environment gates, and cloud deploy identities. If a job fails, read the job trace
top-down and compare `rules:` against `CI_*` predefined variables — avoid deprecated
`only/except` syntax from older examples.

## Hands-on Lab

### Step 1 — Lab workspace

```bash
mkdir -p ~/rebash-cicd/gitlab-runners-and-executors && cd ~/rebash-cicd/gitlab-runners-and-executors
git init -b main
echo "# GitLab Runners and Executors" > README.md
```

### Step 2 — GitLab CI configuration

Add `.gitlab-ci.yml` using the example in Theory. Tailor scripts to a minimal Python project:

```bash
echo 'print("ok")' > app.py
echo 'def test_ok(): assert True' > test_app.py
pip freeze > requirements.txt 2>/dev/null || echo pytest > requirements.txt
```

### Step 3 — Push to GitLab.com or dry-run locally

**GitLab.com (free tier):** create a private project, add the remote, push, and open a merge
request. Confirm pipeline stages in the MR widget.

**Local dry-run:** validate YAML without spending CI minutes (see Lint section below).

### Step 4 — Evidence capture

Save a screenshot or log excerpt to `evidence/notes.md` describing stage order, artefact names,
runner tags used, and any manual approval you configured.


### Step 5 — Runner inspection (optional self-hosted)

If you register a local runner:

```bash
gitlab-runner list
gitlab-runner verify
```

Assign tags in `.gitlab-ci.yml` and confirm the job lands on your runner in job logs
(`Running on ...`).


        ### Lint / dry-run alternative

        Validate pipeline syntax without executing jobs:

        ```bash
        glab ci lint .gitlab-ci.yml 2>/dev/null || python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml'))"
gitlab-ci-local --file .gitlab-ci.yml 2>/dev/null || echo 'Optional: npm i -g gitlab-ci-local'
        ```

        Dry-run paths prove structure and variable references; they do not replace an end-to-end run
        on a real runner when you are learning job isolation and artefact behaviour.

## Validation

| Check | Pass criteria |
|-------|---------------|
| `.gitlab-ci.yml` | Valid YAML; `glab ci lint` or equivalent passes |
| Lint/dry-run | Local validation documented in lab notes |
| Optional CI run | Pipeline green on MR or default branch |
| Notes | `evidence/notes.md` explains stages, runners, and credentials used |

## Code Walkthrough

| Section | GitLab CI detail |
|---------|------------------|
| Entry file | `.gitlab-ci.yml` at repository root |
| Isolation | `image:` keyword and runner executor |
| Conditional execution | `rules:` and `workflow:rules` |
| Manual gate | `when: manual` or protected environment |
| MR integration | Pipeline widget, test reports, coverage |

Read job traces top-down: clone failure, missing variable, script non-zero exit, artefact
upload error, runner tag mismatch.

## Security Considerations

- Never print secrets; verify GitLab masking in job logs after first run
- Scope CI/CD variables to environments and protected branches
- Pin container images to semver or digest
- Run untrusted MR jobs on isolated runners without production credentials
- Rotate tokens used in tutorial labs; they are not production patterns

## Common Mistakes

!!! warning "Using deprecated `only/except`"
    Breaks on upgrade and confuses reviewers. **Fix:** Use `rules:` and `workflow:rules`.

!!! warning "Secrets in Git"
    Credential leak and audit failure. **Fix:** Use GitLab CI/CD variables and OIDC.

!!! warning "Skipping lint locally"
    Wasted runner minutes. **Fix:** Run `glab ci lint` or `gitlab-ci-local` before push.

## Best Practices

- Pin runner images; schedule periodic base image upgrades
- Keep pipelines fast — cache dependencies, split slow integration tests
- Use merge request pipelines for feedback before merging to default branch
- Document rollback: revert commit vs redeploy previous image digest
- Align pipeline changes with [Git](../git/index.md) branch protection rules

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Job skipped | `rules:` mismatch | Log `CI_PIPELINE_SOURCE` and branch variables |
| Permission denied | Wrong variable scope or OIDC trust | Fix protected variable or cloud role |
| Docker daemon error | DinD misconfiguration | Set `DOCKER_TLS_CERTDIR`; verify `services:` |
| Stuck pending | No runner matches tags | Add tagged runner or fix job `tags:` |
| MR pipeline missing | `workflow:rules` too strict | Allow `merge_request_event` source |

## Production Patterns and Deep Dive

        ### How `GitLab Runners and Executors` fits in real environments

        Teams shipping through **Module 2: Runners and Configuration** concepts use these patterns in design reviews, pipeline
        migrations, and incident retrospectives. The lab proves you can author valid GitLab CI
        configuration; this section connects those files to trade-offs you will defend in interviews
        and on-call handovers focused on **GitLab Runner registration, executors (Docker, shell, Kubernetes), and isolation**.

        Production GitLab CI programmes typically document:

        | Artefact | Purpose |
        |----------|---------|
        | Pipeline architecture diagram | Stages, triggers, credentials, and deploy targets |
        | Runbook | How to re-run, roll back, or disable a job safely |
        | Credential rotation procedure | Who rotates tokens, OIDC trust, and protected variables |
        | Cost / minute budget | Runner sizing, cache strategy, and concurrency limits |

        Always pair automation with **least privilege**, **branch protection**, and **auditable**
        deploy gates. The REBASH GitLab CI/CD track uses British English and assumes you completed
        [Git](../git/index.md) fundamentals first.

        ### Extended CLI and validation reference

        The commands below extend the lab — run lint and dry-run variants first, then execute on
        GitLab.com or a self-hosted runner when you need to observe artefacts, caches, and environment
        propagation.

        ```bash
gitlab-runner list 2>/dev/null || echo "Register runner in lab first"
gitlab-runner verify 2>/dev/null || true
grep -E 'tags:|image:' .gitlab-ci.yml
```

        ### Operational scenario (table-top)

        **Scenario:** A teammate merges to `main` and production deploy fails with "permission denied"
        on a step related to **GitLab Runners and Executors**.

        | Step | Action | Why |
        |------|--------|-----|
        | 1 | Open the failed job trace; note stage, image, runner, and identity used | Wrong credential is the top cause |
        | 2 | Compare branch protection and protected environment rules | Protected branches block secrets or deploys |
        | 3 | Re-run the job with `CI_DEBUG_TRACE=true` where appropriate | Surfaces masked variable issues |
        | 4 | Diff `.gitlab-ci.yml` against last green commit | Recent YAML change is likely |
        | 5 | Roll forward with a fix or revert merge | Document in incident ticket |
        | 6 | Add a lint gate so the misconfiguration fails in the MR pipeline | Prevents repeat |

        ### Hardening checklist before production

        - [ ] Short-lived credentials (OIDC) preferred over long-lived PATs or access keys
        - [ ] Secrets in GitLab CI/CD variables — never committed to Git
        - [ ] Untrusted MR pipelines run on runners without production credentials
        - [ ] Deploy jobs require manual approval or protected environments
        - [ ] Container images pinned by digest where feasible
        - [ ] SBOM or vulnerability scan stage on default branch
        - [ ] Cross-links reviewed: [Docker](../docker/index.md), [Kubernetes](../kubernetes/index.md), [Terraform](../terraform/index.md)

        ### Terraform handoff note

        Infrastructure changes belong in [Terraform](../terraform/index.md). After this track,
        reproduce deploy and plan/apply gates using
        [Terraform in CI/CD Pipelines](../terraform/terraform-in-ci-cd-pipelines.md): plan on merge
        requests, apply on protected branches with OIDC, and store remote state with locking.

        ### Review questions (self-check)

        Before moving to the next tutorial, answer without looking at notes:

        1. Which `.gitlab-ci.yml` keywords implement this concept?
        2. What is the least-privilege identity this job should use?
        3. How would you validate YAML locally before pushing?
        4. Where do artefacts and caches differ in retention and security?
        5. Which [Git](../git/index.md) workflow rule prevents broken `main`?

        ### Additional references

        Bookmark official GitLab documentation for **GitLab Runners and Executors**. Note default runner images, quota
        limits, and which pipeline sources consume shared runner minutes so your team can forecast cost
        alongside [Docker](../docker/index.md) build times.

## Summary

- GitLab Runners and Executors is implemented in GitLab CI through `.gitlab-ci.yml`, runners, and merge request workflows
- Validate locally with `glab ci lint` or `gitlab-ci-local` before spending runner minutes
- Security and branch protection are part of pipeline design, not an afterthought
- Continue sequentially or jump to related [Docker](../docker/index.md) and [Terraform](../terraform/index.md) material when ready

## Interview Questions

1. How does GitLab Runners and Executors work in GitLab CI?
2. Where should secrets live in GitLab CI/CD?
3. What triggers merge request pipelines vs branch pipelines?
4. How do artefacts differ from container images in GitLab?
5. Explain least privilege for a GitLab deploy job.
6. What is the blast radius of a compromised runner?
7. How would you roll back a bad deploy in GitLab?
8. When is matrix parallelism worth the runner cost?
9. How do protected environments help in GitLab?
10. What comes after this track in the REBASH curriculum?

!!! tip "Sample answer — question 1"
    GitLab CI expresses GitLab Runners and Executors through `.gitlab-ci.yml` jobs, `stages`, and `rules:`. Merge request pipelines use `CI_PIPELINE_SOURCE=merge_request_event`; default branch pipelines use push sources. Map each concept to the predefined variables GitLab injects.


!!! tip "Sample answer — question 5"
    Deploy jobs should use protected environment-scoped variables and dedicated runners — never a broad admin cloud key on shared MR runners.


## Related Tutorials

- Track overview: [GitLab CI/CD](index.md)
- Previous: [GitLab Merge Requests and Pipeline Triggers](gitlab-merge-requests-and-pipeline-triggers.md)
- Next: [GitLab Runner Tags and Scaling](gitlab-runner-tags-and-scaling.md)

## Cross-track links

- [Git](../git/index.md) — branching, merge requests, and review workflows pipelines depend on
- [Docker](../docker/index.md) — images built and scanned in CI
- [Kubernetes](../kubernetes/index.md) — deploy targets for GitOps and progressive delivery
- [Terraform](../terraform/index.md) — especially [Terraform in CI/CD Pipelines](../terraform/terraform-in-ci-cd-pipelines.md)
- [AWS](../aws/index.md) — cloud credentials, OIDC, and deployment targets

## References

1. [GitLab CI/CD YAML reference](https://docs.gitlab.com/ee/ci/yaml/)
2. [GitLab Runner documentation](https://docs.gitlab.com/runner/)
3. [GitLab CI/CD variables](https://docs.gitlab.com/ee/ci/variables/)
4. [REBASH Terraform in CI/CD](https://rebash.academy/terraform/terraform-in-ci-cd-pipelines/)
