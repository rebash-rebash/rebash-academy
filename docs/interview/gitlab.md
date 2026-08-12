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

## Core concepts

**1. What is the include keyword in .gitlab-ci.yml?**

??? success "Reveal answer"
    Includes pipeline configuration from other YAML files — from the same repo, other repos, or 
    GitLab templates. 
    include: 
     - project: 'company/shared-pipelines' 
     file: '/templates/docker-build.yml' 
     ref: main

**2. What is the purpose of a .gitlab-ci.yml file?**

??? success "Reveal answer"
    It defines the CI/CD pipeline configuration for a project -- stages, jobs, scripts, and the conditions under which jobs
    run -- and is essential for automating build, test, and deployment in GitLab CI/CD.

## Practice questions

**3. How does GitLab CI/CD work?**

??? success "Reveal answer"
    The pipeline is defined in a .gitlab-ci.yml file at the repo root, specifying stages, jobs, and scripts. GitLab Runner
    picks up that configuration and executes the jobs on the configured runner -- shared, group, or project-specific.

## Related

- Course: [GitLab CI/CD](../gitlab/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
