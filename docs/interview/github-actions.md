---
title: "GitHub Actions Interview Preparation"
description: "27 curated interview questions and model answers for GitHub Actions — concepts, scenarios, troubleshooting, and production trade-offs."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

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

**2. What are runners in GitHub Actions?**

??? success "Reveal answer"
    Runners are the servers that actually execute a workflow's jobs. GitHub-hosted runners come with common tooling
    pre-installed across Linux, macOS, and Windows, and I'd switch to self-hosted runners when a job needs to reach
    internal infrastructure or requires a specific environment GitHub-hosted runners don't provide.

**3. What are GitHub Actions and how do they work?**

??? success "Reveal answer"
    GitHub Actions is a CI/CD tool that automates tasks directly within a repository, defined through YAML workflows in
    the .github/workflows directory. Workflows trigger on events like push, pull_request, or a schedule, and define jobs
    made up of steps that execute inside a virtual environment GitHub provisions.

**4. What is the jobs.<job_id>.outputs feature?**

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

**5. What is GitHub Actions concurrency?**

??? success "Reveal answer"
    Prevents multiple workflow runs from executing simultaneously for the same trigger. 
    concurrency: 
     group: production-deploy-${{ github.ref }} 
     cancel-in-progress: false # Don't cancel in-progress; queue instead

**6. What is GitHub Actions OpenID Connect (OIDC)?**

??? success "Reveal answer"
    Allows workflows to authenticate to cloud providers (AWS, Azure, GCP) without storing long-lived 
    credentials. The workflow exchanges a short-lived JWT token for cloud credentials. 
    
     
    DEVSECOPS (25 Questions)

**7. What is GitHub Actions' cache action?**

??? success "Reveal answer"
    - uses: actions/cache@v4 
     with: 
     path: ~/.npm 
     key: ${{ runner.os }}-npm-${{ hashFiles('package-lock.json') }} 
    Caches dependencies between workflow runs, dramatically speeding up builds.

**8. What is Tilt?**

??? success "Reveal answer"
    A local Kubernetes development environment tool. Watches source code, rebuilds/syncs changes 
    to running containers without full rebuilds. Faster iteration than Skaffold for some workflows.

**9. What is a GitHub Actions runner?**

??? success "Reveal answer"
    The machine that executes workflow jobs. GitHub provides hosted runners (ubuntu-latest, 
    windows-latest, macos-latest). Self-hosted runners run on your own infrastructure.

**10. What is actions/upload-artifact and actions/download-artifact?**

??? success "Reveal answer"
    Upload: saves files from a job to GitHub's artifact store. Download: retrieves those files in another 
    job or workflow. Artifacts expire after 90 days by default.

**11. What is the permissions key in GitHub Actions?**

??? success "Reveal answer"
    Controls the permissions granted to GITHUB_TOKEN for a workflow or job. 
    permissions: 
     contents: read 
     packages: write 
     id-token: write # Required for OIDC

**12. What is act?**

??? success "Reveal answer"
    A tool that runs GitHub Actions workflows locally using Docker. Test your workflows without 
    pushing to GitHub. 
    
     
    act -j build # Run the 'build' job locally

**13. What is GitHub Actions timeout-minutes?**

??? success "Reveal answer"
    Sets a maximum runtime for a job or step. Prevents hung workflows from consuming runner 
    minutes indefinitely. 
    
     
    jobs: 
     test: 
     timeout-minutes: 30

**14. What is the push.paths trigger filter?**

??? success "Reveal answer"
    Triggers the workflow only when specific file paths are changed. 
    on: 
     push: 
     paths: 
     - 'src/**' 
     - 'package.json' 
     paths-ignore: 
     - 'docs/**'

**15. What is workflow_run trigger?**

??? success "Reveal answer"
    Triggers a workflow when another workflow completes. 
    on: 
     workflow_run: 
     workflows: ["CI Pipeline"] 
     types: [completed] 
     branches: [main]

**16. What is continue-on-error in GitHub Actions?**

??? success "Reveal answer"
    Allows subsequent steps/jobs to run even if this step fails. 
    - name: Optional lint check 
     run: npm run lint 
     continue-on-error: true

**17. What is the difference between origin and upstream in Git?**

??? success "Reveal answer"
    origin is your fork's remote repository. upstream is the original repository you forked from. 
    Convention in open-source workflows.

**18. What are GitHub Actions and their advantages?**

??? success "Reveal answer"
    o A CI/CD automation tool integrated with GitHub. 
    o Advantages: Easy setup, built-in marketplace, YAML-based workflows.

**19. What is a composite action?**

??? success "Reveal answer"
    A reusable action made of multiple steps defined in an action.yml file. Shareable across 
    workflows and repositories.

**20. What is the GitHub Actions runner.os context?**

??? success "Reveal answer"
    Returns the operating system of the runner (Linux, Windows, macOS). Used in cross-platform 
    workflows.

**21. What is a workflow_dispatch trigger?**

??? success "Reveal answer"
    Allows manually triggering a workflow from the GitHub UI or API, optionally with input 
    parameters.

**22. What is fromJSON() in GitHub Actions expressions?**

??? success "Reveal answer"
    Parses a JSON string into an object in expressions. 
    ${{ fromJSON(steps.build.outputs.matrix) }}

## Scenarios and troubleshooting

**23. > to make a shenge. @ critical production environment. ‘ you ensure it’s safe?**

??? success "Reveal answer"
    + Review the change and impact using “terraform plan”. ee
    ing plan’ * Change management process
    + Get peer/architect review for high-risk changes. i 2
    > + Use featuee branches and CI validati namie
    validation. * Approval
    proval. workflow
    Apply during low-traffic windows. * Safe deployment mindset
    © + Monitor after apply and have rollback plan. * Monitoring & rollback
    re awareness

## Practice questions

**24. How do you secure secrets and manage environments in GitHub Actions?**

??? success "Reveal answer"
    GitHub Actions has a layered secrets management system. Understanding the difference between 
    repository secrets, environment secrets, and organization secrets is important for enterprise 
    setups. 
    Levels of secrets: 
    Organization Secrets → Available to all repos in the organization 
    Repository Secrets → Available to all workflows in one repo 
    Environment Secrets → Available only to jobs targeting a specific 
    environment 
    Setting up environment protection rules (critical for production): 
    In GitHub: Settings → Environments → New environment → production 
    • 
    Required reviewers: at least 2 senior engineers 
    • 
    Wait timer: 5 minutes (gives time to cancel if something looks wrong) 
    • 
    Deployment branches: main only 
    Using environment secrets in a workflow: 
    jobs: 
     deploy-production: 
     runs-on: ubuntu-latest 
     environment: production # Triggers protection rules 
     steps: 
     - name: Deploy 
     env: 
     DATABASE_URL: ${{ secrets.DATABASE_URL }} # Environment secret 
     API_KEY: ${{ secrets.API_KEY }} # Environment secret 
     run: ./deploy.sh 
    Using OIDC for AWS authentication…

**25. How do you write a reusable workflow in GitHub Actions?**

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

**26. How do you securely store secrets in GitHub Actions?**

??? success "Reveal answer"
    GitHub's Secrets feature encrypts values like API keys and credentials, accessible in a workflow via ${{
    secrets.MY_SECRET }} with the actual value automatically masked in logs so it never gets echoed out accidentally.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    0
    8
    ARGOCD

**27. How do you create a GitHub Actions workflow?**

??? success "Reveal answer"
    I add a YAML file under .github/workflows/, specifying on for the triggering event, jobs for the units of work, and steps
    within each job for individual actions -- checking out the repo, running a script, or invoking a pre-built action from the
    marketplace.

## Related

- Course: [GitHub Actions](../github-actions/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
