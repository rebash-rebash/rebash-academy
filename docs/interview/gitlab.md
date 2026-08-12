---
title: "GitLab CI/CD Interview Preparation"
description: "3 curated GitLab CI/CD interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: gitlab
tags:
  - interview
  - gitlab
comments: false
robots: noindex, follow
search:
  exclude: true
---

{% raw %}
# GitLab CI/CD Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

<div class="ra-interview-qa" markdown="1">

## Core concepts

**1. What is the include keyword in .gitlab-ci.yml?**

??? success "Reveal answer"
    **In short:** Compose pipelines from reusable YAML instead of one giant `.gitlab-ci.yml`.
    
    **Key points**
    
    - **include:local** — pull templates from the same repo.
    - **include:project** — share standards across teams with a `ref`.
    - **include:remote / template** — HTTP YAML or GitLab-managed templates.
    - Expands before jobs run; keep includes small and versioned.
    
    **Try this**
    
    - `include:`
    - `- local: '/templates/build.yml'`
    - `- project: 'platform/ci-templates'`
    
    **Trap**
    
    - Pin `ref` on project includes — floating `main` makes pipelines non-reproducible.

**2. What is the purpose of a .gitlab-ci.yml file?**

??? success "Reveal answer"
    **In short:** `.gitlab-ci.yml` is the versioned contract for how GitLab builds, tests, and deploys your project.
    
    **Key points**
    
    - Defines stages, jobs, images, rules, artefacts, and environments.
    - Lives in the repo (or a configured custom path) so reviews cover CI changes.
    - Runners pick jobs; GitLab orchestrates pipeline state and MR feedback.
    - Compose with `include` and `extends` for DRY standards.
    
    **Trap**
    
    - A missing or invalid YAML silently skips expected jobs — validate with the CI Lint UI.

## Practice questions

**3. How does GitLab CI/CD work?**

??? success "Reveal answer"
    **In short:** Event → YAML evaluation → jobs on runners → artefacts/environments back into GitLab.
    
    **Key points**
    
    - Triggers: push, merge request, schedule, web, API, or pipeline trigger tokens.
    - GitLab expands includes, creates a pipeline graph, and assigns jobs to runners.
    - Jobs use `script`, caches, artefacts, and optional deploy environments.
    - Security/report artefacts decorate MRs; protected branches gate secrets and prod jobs.
    
    **Try this**
    
    - `gitlab-ci-local` or CI Lint for dry-runs
    - `needs:` for DAG parallelism
    
    **Trap**
    
    - Forgetting `rules:` on expensive jobs burns minutes on every branch push.

## Related
- Course: [GitLab CI/CD](../gitlab/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
