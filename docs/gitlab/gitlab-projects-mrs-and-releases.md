---
title: "GitLab Projects, Merge Requests, and Releases"
description: "Operate GitLab repositories, branches, merge requests, protected branches, tags, and releases as the backbone of CI/CD."
difficulty: intermediate
estimated_time: "35–50 min"
technology: gitlab
category: gitlab
module: "Module 2 · GitLab Projects"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - gitlab
  - merge-requests
  - releases
prerequisites:
  - gitlab/gitlab-ci-fundamentals
next:
  - gitlab/gitlab-runners-and-executors
related:
  - git/git-workflows-and-branching
  - git/pull-requests-and-code-review
labs: []
projects: []
interview: interview/gitlab
certifications:
  - GitLab Certified CI/CD Associate
tags:
  - gitlab
  - merge-requests
  - releases
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# GitLab Projects, Merge Requests, and Releases

## Overview



Connect repositories, branches, merge requests, protected branches, tags, and releases to how pipelines start and what they are allowed to change.

GitLab CI/CD is useless without a clear **project** model. A project owns the Git repository, CI settings, protected branches, variables, and release records. Merge requests (MRs) are the review surface; tags and **Releases** mark shippable versions.

This is a core tutorial in **Module 2 · GitLab Projects** of the REBASH Academy **GitLab CI/CD for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [GitLab CI/CD Fundamentals](gitlab-ci-fundamentals.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Describe project vs group vs repository settings that affect CI  
- [ ] Explain MR pipelines vs branch pipelines  
- [ ] Configure protected branches and protected tags mentally  
- [ ] Relate Git tags to GitLab Releases



## Architecture



This topic’s control points and relationships are shown below.

![Projects and merge requests](../assets/excalidraw/gitlab-projects-mr.svg)



## Theory



### What it is

A **GitLab project** wraps a Git repository plus integrations (CI/CD, issues, packages, environments). **Branches** hold work in progress; **merge requests** propose integrating a source branch into a target (often `main`). **Protected branches** restrict who can push or merge and which runners / variables apply. A **tag** marks a commit; a **Release** is a GitLab object that attaches notes, assets, and often a changelog to that tag.

| Concept | CI impact |
|---------|-----------|
| Branch push | May start a branch pipeline |
| Merge request | Often starts an MR pipeline (`merge_request_event`) |
| Protected branch | Can unlock protected variables / environments |
| Tag / Release | Common trigger for publish and deploy jobs |

### Why it matters

Production mistakes usually start as process gaps: anyone can push to `main`, deploy jobs run on every feature branch, or release tags are created without CI. Protected branches plus MR-required pipelines give you **reviewable change** before production. Release tags give ops a stable handle for rollbacks and artefact promotion.

### How it works

Typical flow:

1. Developer pushes a feature branch; optional branch pipeline runs lint/tests.
2. They open an MR; GitLab runs an MR pipeline (prefer `rules` on `merge_request_event`).
3. Reviewers approve; protected-branch rules require a successful pipeline before merge.
4. Merge to `main` may run a post-merge pipeline (build, publish).
5. Cutting `v1.2.3` (and optionally creating a GitLab Release) triggers release/publish jobs.

Predefined variables such as `$CI_MERGE_REQUEST_IID`, `$CI_COMMIT_BRANCH`, `$CI_COMMIT_TAG`, and `$CI_COMMIT_REF_PROTECTED` tell jobs which context they are in.

### Key concepts and comparisons

| Trigger | Typical use |
|---------|-------------|
| Branch pipeline | Fast feedback on every push |
| MR pipeline | Required checks before merge |
| Tag pipeline | Versioned publish / deploy |
| Schedule / manual | Nightly scans, promotions |

**Protected branch vs protected variable:** protecting `main` alone is incomplete — pair it with **protected CI/CD variables** and **protected environments** so secrets never appear on unprotected feature branches.

### Common pitfalls

- Assuming “pipeline on push” equals “pipeline on MR” — configure `rules` explicitly.
- Creating Releases without tags (or tags without CI) — keep one SemVer tag → one Release.
- Leaving `main` unprotected on shared projects.
- Treating GitLab Releases as a replacement for artefact registries — Releases point at assets; registries store images/packages.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-gitlab/module-02 && cd ~/rebash-gitlab/module-02
```

**Focus:** model release/version jobs with a changelog stub

### Step 1 – Release metadata

```bash
echo '# Changelog

## 0.1.0
- Lab release' > CHANGELOG.md
cat > .gitlab-ci.yml << 'EOF'
release:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/release-cli:latest
  script:
    - echo "Create GitLab Release for $CI_COMMIT_TAG"
  rules:
    - if: $CI_COMMIT_TAG
EOF
cat CHANGELOG.md
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml')); print('OK')"
```

### Final step – Cleanup note

```bash
# File-only
```



## 0.1.0

- Lab release' > CHANGELOG.md
cat > .gitlab-ci.yml << 'EOF'
release:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/release-cli:latest
  script:
    - echo "Create GitLab Release for $CI_COMMIT_TAG"
  rules:
    - if: $CI_COMMIT_TAG
EOF
cat CHANGELOG.md
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml')); print('OK')"
```

### Final step – Cleanup note

```bash
# File-only
```



## Validation



- [ ] Lab commands run under `~/rebash-gitlab/module-02/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **GitLab Projects, Merge Requests, and Releases** always combines:

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



!!! warning "Assuming “pipeline on push” equals “pipeline on MR” — configure `rules` explicitly."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Creating Releases without tags (or tags without CI) — keep one SemVer tag → one Release."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode GitLab Projects, Merge Requests, and Releases changes as code and review them in pull requests
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



**GitLab Projects, Merge Requests, and Releases** is essential for Cloud and DevOps engineers working with gitlab. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. How does **GitLab Projects, Merge Requests, and Releases** show up in a real GitLab delivery workflow?
2. A pipeline is stuck / red — what do you check first?
3. How do `needs`, stages, and artefacts interact?
4. How should secrets and cloud credentials be handled in GitLab CI?
5. How would you keep merge-request pipelines fast but still safe?

!!! tip "Sample answer — question 2"
    Open the failing job log, confirm runner tags/executor, then validate `.gitlab-ci.yml` with CI Lint. Check rules that skipped jobs and artefact dependencies.

!!! tip "Sample answer — question 4"
    Prefer masked/protected variables and OIDC (`id_tokens`) over long-lived keys. Limit who can run protected-branch pipelines.



## Related Tutorials



- [Course overview](index.md)
- [GitLab Runners and Executors](gitlab-runners-and-executors.md)



## References



- [Merge request pipelines](https://docs.gitlab.com/ee/ci/pipelines/merge_request_pipelines.html)  
- [Releases](https://docs.gitlab.com/ee/user/project/releases/)
