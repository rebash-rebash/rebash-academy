---
title: "GitHub Actions Interview Preparation"
description: "35 curated GitHub Actions interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: github-actions
tags:
  - interview
  - github-actions
comments: false
---

{% raw %}
# GitHub Actions Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. What is a GitHub Actions workflow, and explain its key components.**

??? success "Reveal answer"
    A GitHub Actions workflow is an automated process defined in a YAML file stored
    in .github/workflows/. It runs on GitHub-managed virtual machines (or your own self-hosted
    runners) in response to events like code pushes, pull requests, or scheduled timers.
    The five core components:
    1. Events (triggers) — what starts the workflow
    2. Jobs — groups of steps that run on the same machine
    3. Steps — individual tasks within a job
    4. Actions — reusable units (from Marketplace or custom)
    5. Runners — the machines where jobs execute
    Complete example — a full CI/CD workflow:
    # .github/workflows/ci-cd.yml
    name: CI/CD Pipeline
    # EVENTS: This workflow triggers on...
    on:
    push:
    branches: [main, develop]
    
    pull_request:
    branches: [main]
    schedule:
    - cron: '0 2 * * *' # Nightly at 2 AM UTC
    # Environment variables available to all jobs
    env:
    PYTHON_VERSION: '3.11'
    ECR_REPOSITORY: my-app
    jobs:
    # JOB 1: Run tests
    test:
    name: Run Tests
    # RUNNER: GitHub-hosted Ubuntu runner
    runs-on: ubuntu-latest
    # Run tests against multiple Python versions
    strategy:
    matrix:
    python-version: ['3.10',…

**2. What is the difference between needs and concurrency in GitHub Actions?**

??? success "Reveal answer"
    Start with a precise definition in the context of Github Actions, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**3. What is GitHub Actions Matrix strategy?**

??? success "Reveal answer"
    Start with a precise definition in the context of Github Actions, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**4. What is a matrix in GitHub Actions?**

??? success "Reveal answer"
    Start with a precise definition in the context of Github Actions, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**5. What is the needs keyword in GitHub Actions?**

??? success "Reveal answer"
    Start with a precise definition in the context of Github Actions, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**6. What are runners in GitHub Actions?**

??? success "Reveal answer"
    Runners are the servers that actually execute a workflow's jobs. GitHub-hosted runners come with common tooling
    pre-installed across Linux, macOS, and Windows, and I'd switch to self-hosted runners when a job needs to reach
    internal infrastructure or requires a specific environment GitHub-hosted runners don't provide.

**7. What are GitHub Actions and how do they work?**

??? success "Reveal answer"
    GitHub Actions is a CI/CD tool that automates tasks directly within a repository, defined through YAML workflows in
    the .github/workflows directory. Workflows trigger on events like push, pull_request, or a schedule, and define jobs
    made up of steps that execute inside a virtual environment GitHub provisions.

**8. What is the jobs.<job_id>.outputs feature?**

??? success "Reveal answer"
    Passes data from one job to another in the same workflow. 
    jobs: 
     build: 
     outputs: 
     image-tag: ${{ steps.build.outputs.tag }} 
     deploy: 
     needs: build 
     steps: 
     - run: echo "Deploying ${{ needs.build.outputs.image-tag }}"

**9. Explain your GitHub Actions pipeline?**

??? success "Reveal answer"
    Answer directly for Github Actions: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**10. What is GitHub Actions concurrency?**

??? success "Reveal answer"
    Prevents multiple workflow runs from executing simultaneously for the same trigger. 
    concurrency: 
     group: production-deploy-${{ github.ref }} 
     cancel-in-progress: false # Don't cancel in-progress; queue instead

**11. What is GitHub Actions OpenID Connect (OIDC)?**

??? success "Reveal answer"
    Allows workflows to authenticate to cloud providers (AWS, Azure, GCP) without storing long-lived 
    credentials. The workflow exchanges a short-lived JWT token for cloud credentials. 
    
     
    DEVSECOPS (25 Questions)

**12. What is a GitHub Actions runner?**

??? success "Reveal answer"
    The machine that executes workflow jobs. GitHub provides hosted runners (ubuntu-latest, 
    windows-latest, macos-latest). Self-hosted runners run on your own infrastructure.

**13. What is actions/upload-artifact and actions/download-artifact?**

??? success "Reveal answer"
    Upload: saves files from a job to GitHub's artifact store. Download: retrieves those files in another 
    job or workflow. Artifacts expire after 90 days by default.

**14. What is the permissions key in GitHub Actions?**

??? success "Reveal answer"
    Controls the permissions granted to GITHUB_TOKEN for a workflow or job. 
    permissions: 
     contents: read 
     packages: write 
     id-token: write # Required for OIDC

**15. What is GitHub Actions timeout-minutes?**

??? success "Reveal answer"
    Sets a maximum runtime for a job or step. Prevents hung workflows from consuming runner 
    minutes indefinitely. 
    
     
    jobs: 
     test: 
     timeout-minutes: 30

**16. What is the push.paths trigger filter?**

??? success "Reveal answer"
    Triggers the workflow only when specific file paths are changed. 
    on: 
     push: 
     paths: 
     - 'src/**' 
     - 'package.json' 
     paths-ignore: 
     - 'docs/**'

**17. What is workflow_run trigger?**

??? success "Reveal answer"
    Triggers a workflow when another workflow completes. 
    on: 
     workflow_run: 
     workflows: ["CI Pipeline"] 
     types: [completed] 
     branches: [main]

**18. What is continue-on-error in GitHub Actions?**

??? success "Reveal answer"
    Allows subsequent steps/jobs to run even if this step fails. 
    - name: Optional lint check 
     run: npm run lint 
     continue-on-error: true

**19. What is the difference between origin and upstream in Git?**

??? success "Reveal answer"
    origin is your fork's remote repository. upstream is the original repository you forked from. 
    Convention in open-source workflows.

## Scenarios and troubleshooting

**20. How would you parameterize a workflow so that downstream jobs know which environment to deploy to?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Github Actions, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**21. You are given a GitHub Actions workflow snippet. How would you identify incorrect steps and suggest improvements or missing steps for a robust CI/CD pipeline?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Github Actions components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

## Practice questions

**22. How do you write a reusable workflow in GitHub Actions?**

??? success "Reveal answer"
    Reusable workflows are GitHub Actions' equivalent of shared libraries. Instead of copying the 
    same YAML across dozens of repositories, you define the workflow once and call it from other 
    workflows. 
    Defining a reusable workflow (in a shared repo): 
    # .github/workflows/reusable-docker-build.yml 
    name: Reusable Docker Build and Push 
    on: 
     workflow_call: # This makes it reusable 
     inputs: 
     ecr-repository: 
     required: true 
     type: string 
     aws-region: 
     required: false 
     type: string 
     default: 'ap-south-1' 
     environment: 
     required: true 
     type: string 
     secrets: 
     aws-role-arn: 
     required: true 
    
     
     outputs: 
     image-uri: 
     description: "The full URI of the pushed Docker image" 
     value: ${{ jobs.build.outputs.image-uri }} 
    jobs: 
     build: 
     runs-on: ubuntu-latest 
     environment: ${{ inputs.environment }} 
     outputs: 
     image-uri: ${{ steps.build-push.outputs.image-uri }} 
     steps: 
     - uses: actions/checkout@v4 
     - name: Configure AWS credentials 
     uses: aws-actions/configure-aws-credentials@v4 
     with: 
     role-to-assume: ${{ secrets.aws-role-arn }} 
     aws-region: ${{…

**23. How do you deploy to EKS through GitHub Actions?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Github Actions components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**24. How do you prevent concurrent executions in GitHub Actions?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Github Actions components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**25. Where do you keep the GitHub Actions workflow file, and how do you upload a JAR artifact?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Github Actions components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**26. About K8's Architecture and tell me the workflow?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Github Actions components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**27. How do you set up a manual trigger in GitHub Actions?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Github Actions components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**28. How do you run jobs in parallel in GitHub Actions?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Github Actions components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**29. 12 .How do you handle parallel execution in CI/CD workflows?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Github Actions components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**30. How do you securely store secrets in GitHub Actions?**

??? success "Reveal answer"
    GitHub's Secrets feature encrypts values like API keys and credentials, accessible in a workflow via ${{
    secrets.MY_SECRET }} with the actual value automatically masked in logs so it never gets echoed out accidentally.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    0
    8
    ARGOCD

**31. How do you create a GitHub Actions workflow?**

??? success "Reveal answer"
    I add a YAML file under .github/workflows/, specifying on for the triggering event, jobs for the units of work, and steps
    within each job for individual actions -- checking out the repo, running a script, or invoking a pre-built action from the
    marketplace.

**32. Do you have experience with GitHub Actions? Suppose I want to build and test a Java Maven application and create an artifact, what steps would you include?**

??? success "Reveal answer"
    Outline the solution first, then give a minimal correct example (commands or config sketch).
    
    Call out the production hardening you would add next (pin versions, least privilege, secrets, health checks) and how you would validate the result.

**33. In GitHub Actions, if one job depends on another job, which parameter do you use?**

??? success "Reveal answer"
    Answer directly for Github Actions: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**34. How caching works in Github Actions?**

??? success "Reveal answer"
    Answer directly for Github Actions: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**35. What steps are included in your GitHub Actions workflow file?**

??? success "Reveal answer"
    Answer directly for Github Actions: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

## Related

- Course: [GitHub Actions](../github-actions/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
