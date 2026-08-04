---
title: "CI/CD Interview Prep"
description: "Interview themes and practice strategy for GitLab CI — stages, jobs, rules, runners, variables, artefacts, security gates, and deploy approvals."
difficulty: intermediate
estimated_time: "30 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: interview
tags:
  - interview
  - cicd
  - gitlab
comments: false
---

# CI/CD Interview Prep

Use this page as a revision map. Every tutorial in the [CI/CD track](../gitlab/index.md) ends with interview questions — work those first, then stress-test the themes below.

!!! note "Other platforms"
    Jenkins and GitHub Actions come later on REBASH Academy — these themes focus on **GitLab CI**.

## How to practise

1. Answer out loud in two minutes without notes
2. Draw the pipeline DAG: trigger → build → test → scan → deploy
3. Name the first log line you read when a merge pipeline fails
4. Tie each topic to security (secrets, scan gates), cost (runners, cache), and immutability (SHA tags)

## High-yield themes

- CI vs CD vs continuous deployment — trunk-based flow and branch protection
- Stages, jobs, and `script:` — how GitLab orders work in `.gitlab-ci.yml`
- Shared vs self-hosted runners; Docker vs Kubernetes executors; runner tags
- `rules:` and `workflow:rules:` — conditional pipelines on MR vs default branch
- CI/CD variables: masked, protected, file type; OIDC over long-lived keys
- Artefacts vs cache — retention, `needs:`, and `dependencies:`
- `needs:` / DAG vs stage-only ordering — when to shorten the critical path
- `parallel: matrix:` — when fan-out helps vs runner minute explosion
- Docker-in-Docker vs Kaniko vs buildx in CI
- Security scanning gates — fail vs `allow_failure`, CRITICAL policy
- Protected environments and `when: manual` before staging/production
- Immutable image promotion (`$CI_COMMIT_SHA`) vs rebuild on deploy
- GitLab Container Registry integration with build and scan jobs
- Least-privilege CI identities (cloud OIDC, scoped job tokens)
- First-hour failed MR: YAML/schema vs script vs runner capacity

## Hands-on prompts interviewers love

- Walk through [Pipeline Failure Triage](../labs/cicd-pipeline-triage.md) as if narrating a production incident bridge
- Explain [Docker Build, Scan, and Deploy Gate](../labs/cicd-docker-secure-gate.md) — why scan before manual staging
- Defend a trade-off: GitLab integrated registry vs external ECR with OIDC
- How would you stop secrets leaking in fork merge request pipelines?
- When would you use `resource_group:` on a deploy job?
- Explain the difference between `rules:` on a job and `workflow:rules:` at pipeline level

## GitLab-specific questions

| Prompt | Strong answer shape |
|--------|---------------------|
| Stage vs job failure | Invalid `stage:` fails at validation; script errors fail at runtime with exit code |
| Runner selection | Match job `tags:` to runner capabilities; self-host for residency or GPU |
| Protected variables | Scope production secrets to protected branches only |
| MR pipeline triggers | `$CI_PIPELINE_SOURCE == "merge_request_event"` in `rules:` |
| Manual deploy audit | Environments UI shows who clicked play and which SHA deployed |
| CI lint before push | GitLab CI Lint API or UI — catch schema errors before runner minutes |

## Security and compliance angles

- Secret detection in merge pipelines — block vs warn
- Container and dependency scanning — where in the DAG relative to build and deploy
- Separation of duties — who can approve production deploy via protected environments
- Audit trail — who clicked manual deploy and which `$CI_COMMIT_SHA` shipped
- Fork MR risk — untrusted code must not receive production variables

## Related

- Track: [CI/CD](../gitlab/index.md)
- [GitLab CI/CD Fundamentals](../gitlab/gitlab-ci-fundamentals.md)
- [GitLab Projects, Merge Requests, and Releases](../gitlab/gitlab-projects-mrs-and-releases.md)
- [GitLab Runners and Executors](../gitlab/gitlab-runners-and-executors.md)
- [Production Pipelines and Environments](../gitlab/production-pipelines-and-environments.md)
- [Security Scanning and DevSecOps](../gitlab/security-scanning-and-devsecops.md)
- Cheat sheet: [GitLab CI/CD cheat sheet](../cheatsheets/cicd.md)
- Quiz: [CI/CD Fundamentals](../quizzes/cicd-fundamentals.md)
- Lab: [Pipeline Failure Triage](../labs/cicd-pipeline-triage.md)
- Lab: [Docker Build, Scan, and Deploy Gate](../labs/cicd-docker-secure-gate.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer/)
