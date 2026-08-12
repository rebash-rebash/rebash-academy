---
title: "CI/CD Interview Preparation"
description: "40 curated CI/CD interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: cicd
tags:
  - interview
  - cicd
comments: false
---

{% raw %}
# CI/CD Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. Can you explain the different stages of a CI/CD pipeline?**

??? success "Reveal answer"
    Source stage where code is committed to version control; build stage where source compiles into an executable or
    package; test stage running unit, integration, and performance tests; artifact stage where the build becomes a
    deployable unit stored in a repository; deployment stage pushing to staging and then production after approval; and
    post-deployment monitoring to confirm stability.

**2. What is the role of Selenium in the testing pyramid?**

??? success "Reveal answer"
    Selenium sits in the UI testing layer, handling end-to-end validation of user interactions, and should complement --
    not replace -- unit tests at the base and integration tests in the middle. Using it wisely within that pyramid, rather than
    over-relying on it, optimizes both coverage and test-suite speed.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    2
    4
    NEXUS

**3. What are the key features of SonarQube?**

??? success "Reveal answer"
    Code quality management tracking bugs, vulnerabilities, and code smells; security hotspot detection for risks like
    SQL injection or XSS; technical debt management estimating the time to fix detected issues; CI/CD integration with
    Jenkins, GitHub Actions, GitLab CI; custom quality profiles for project-specific rules; and support for over 25
    programming languages.

**4. Can you explain how you would use Selenium Grid for testing?**

??? success "Reveal answer"
    Start the Selenium Grid Hub as the central control point, register multiple nodes specifying available browsers and
    versions, point test scripts at the Grid Hub instead of a local driver, and run the tests -- the hub distributes them
    across nodes based on requested browser and capabilities.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**5. What is the difference between bugs, vulnerabilities, and code smells in SonarQube?**

??? success "Reveal answer"
    Bugs are issues likely to cause incorrect or unexpected runtime behaviour. Vulnerabilities are security risks like SQL
    injection or XSS that could be exploited. Code smells are maintainability concerns that don't cause immediate errors
    but make the codebase harder to work with over time.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**6. What is the SonarQube Scanner, and how is it used?**

??? success "Reveal answer"
    The SonarQube Scanner analyzes source code and sends results to the SonarQube server, run either manually via
    the sonar-scanner command or as part of a CI/CD pipeline, configured through a sonar-project.properties file with the
    relevant project and server details.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    2
    2
    TRIVY

**7. What are some best practices when using SonarQube in a CI/CD pipeline?**

??? success "Reveal answer"
    Automate quality gate checks so the pipeline actually fails when the gate isn't met, aim for solid test coverage to
    catch untested code paths, analyze frequently -- ideally every commit or pull request -- customize quality profiles to
    the team's actual standards, and prioritize fixing bugs and vulnerabilities over code smells.

**8. What are the different components of Selenium?**

??? success "Reveal answer"
    Selenium WebDriver provides the programming interface for writing and executing test scripts; Selenium IDE is a
    browser extension for recording and playing back tests; Selenium Grid enables parallel test execution across
    machines and browsers; and Selenium RC is the older, largely deprecated component WebDriver has replaced.

**9. What is SonarQube, and why is it used?**

??? success "Reveal answer"
    Start with a precise definition in the context of Cicd, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**10. what is maven and explain about repositories?**

??? success "Reveal answer"
    Start with a precise definition in the context of Cicd, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**11. What is the role of continuous integration?**

??? success "Reveal answer"
    Start with a precise definition in the context of Cicd, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**12. What is the output of sonarqube, how to fix if any smell code/vurnabilities found?**

??? success "Reveal answer"
    Start with a precise definition in the context of Cicd, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**13. What is pom.xml in maven?**

??? success "Reveal answer"
    Start with a precise definition in the context of Cicd, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**14. Difference between Continuous Delivery and Continuous Deployment?**

??? success "Reveal answer"
    Start with a precise definition in the context of Cicd, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**15. What are the main features of Nexus Repository Manager?**

??? success "Reveal answer"
    Support for multiple repository formats, proxying and caching remote repositories to speed up builds, straightforward
    artifact upload/storage/retrieval, fine-grained security and access control, seamless CI/CD tool integration, and
    repository health checks for monitoring performance.

**16. What are SonarQube Quality Gates?**

??? success "Reveal answer"
    A Quality Gate is a set of conditions -- around bugs, vulnerabilities, coverage, duplication -- that a project must meet
    to be considered acceptable. Configuring the pipeline to fail when the gate isn't met is what actually enforces the
    standard rather than just reporting on it.

**17. What is Selenium, and how is it used in DevOps?**

??? success "Reveal answer"
    Selenium is an open-source framework for automating web application testing. In DevOps I integrate it into CI/CD
    pipelines to automatically verify that new code changes don't break existing functionality, maintaining software quality
    while still enabling frequent releases.

**18. What is Nexus Repository Manager?**

??? success "Reveal answer"
    Nexus Repository Manager is a repository management tool for storing and sharing software artifacts, supporting
    formats like Maven, npm, NuGet, and Docker. It centralizes binary management, improving dependency
    management and CI/CD integration across teams.

**19. What is SonarLint, and how does it relate to SonarQube?**

??? success "Reveal answer"
    SonarLint is an IDE plugin providing real-time code analysis as developers write code, letting issues get caught and
    fixed locally before a commit even happens -- complementing SonarQube by giving instant feedback rather than
    waiting for a CI-stage scan.

**20. What are GitLab CI/CD pipelines?**

??? success "Reveal answer"
    Pipelines are the automated processes defined in .gitlab-ci.yml that build, test, and deploy code -- made up of stages
    that run sequentially, each containing jobs that run concurrently, ensuring consistent delivery and automating
    repetitive tasks.

## Scenarios and troubleshooting

**21. How do you implement a complete production-grade pipeline that incorporates all the tools discussed?**

??? success "Reveal answer"
    Answer: 
    Here is a holistic view of what a mature, production-grade pipeline looks like, integrating all the 
    tools we've discussed: 
    Developer pushes code 
     ↓ 
    [GitHub] ← PR opens → Branch protection rules trigger 
     ↓ 
    [GitHub Actions / Jenkins] ← Webhook trigger 
     ↓ 
    Stage 1: CODE QUALITY 
     ├── SonarQube static analysis (code smells, bugs, coverage) 
     ├── ESLint / flake8 / golangci-lint (language-specific linting) 
     └── terraform fmt / validate (for IaC changes) 
     ↓ 
    Stage 2: BUILD 
     ├── Compile / package application 
     ├── Build Docker image (multi-stage, minimal) 
     └── Push to ECR / ACR / Docker Hub 
     ↓ 
    Stage 3: SECURITY SCAN 
     ├── Trivy — scan Docker image for CVEs 
     ├── Snyk — scan dependencies (npm, pip, maven) 
     ├── OWASP Dependency Check — Java/Maven specific 
     └── Checkov — scan Terraform/K8s manifests for misconfigurations 
     ↓ 
    Stage 4: TEST 
     ├── Unit tests (fast, run in parallel) 
     ├── Integration tests (with real DB via Docker Compose / K8s job) 
     └── Contract tests (Pact — API contract validation) 
     ↓ 
    Stage 5: DEPLOY TO STAGING 
     ├── Terraform…

**22. How do you prioritize and manage multiple critical issues in a CI/CD pipeline failure?,?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Cicd, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**23. How would you set up entire CI/CD setup for this application?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Cicd components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**24. CI/CD pipeline needs rollback capability. How would you implement it?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Cicd components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**25. Suppose you are implementing a Canary deployment where only 10% of users receive the new version. How would you implement it through your CI/CD pipeline?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Cicd components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**26. Explain your complete CI/CD pipeline from code commit to production deployment?**

??? success "Reveal answer"
    Answer directly for Cicd: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

## Practice questions

**27. How do you implement feature flags in a CI/CD pipeline?**

??? success "Reveal answer"
    Use a feature flag service (LaunchDarkly, Unleash, or custom Redis-backed). In the pipeline: 1) 
    Merge incomplete features behind a false flag. 2) Deploy to production — feature is inactive. 3) 
    Enable flag for internal users (dogfooding). 4) Gradually roll out by user percentage. 5) Full 
    rollout. 6) Remove flag and code once stable. This separates deployment from release. 
    Pro Tip for Interviews: Don't just memorize answers — understand the why behind each tool. 
    The best interviews are conversations, not recitations. When you say "we chose X over Y because 
    of Z constraint," you demonstrate real-world judgment that no amount of memorization can 
    fake. 
     
     
    
     
     
    ADVANCE 
    SECTION: 
    HAVING 
    HANDS-ON 
    QUESTIONS 
     
     
    
     
    Introduction to Jenkins 
    Jenkins is the grandfather of CI/CD automation. Released in 2011 as a fork of Hudson, it has 
    become the most widely deployed open-source automation server in the world. When someone 
    says "we have a pipeline," there's a good chance Jenkins is somewhere in that picture. 
    Understanding Jenkins deeply — not just its UI, but…

**28. How do Continuous Integration (CI) and Continuous Deployment (CD) work together?**

??? success "Reveal answer"
    CI is about integrating code changes into a shared repository multiple times a day, with each integration verified
    through automated builds and tests so errors are caught as early as possible. CD extends that by automatically
    deploying the tested, integrated code to production, so any change that passes the test suite reaches users with
    minimal manual intervention. Together, CI keeps the codebase stable through frequent verification, while CD makes
    sure that stable code actually reaches production quickly and reliably.

**29. How do you design and implement a complete CI/CD pipeline for ML models?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Cicd components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**30. How can you monitor the health and performance of Nexus Repository Manager?**

??? success "Reveal answer"
    The Nexus web UI provides basic usage and performance stats, built-in health check reports monitor repository
    status, and integrating Nexus with external tools like Prometheus or Grafana gives more detailed metrics and alerting
    on performance and usage.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    2
    5
    COMBINED: GITHUB ACTIONS, ARGOCD &
    KUBERNETES

**31. How do you write in yaml to create a ci/cd pipeline from scratch to test and deploy from Dev to UAT?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Cicd components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**32. [ ] How do you integrate tools like SonarQube into your pipelines?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Cicd components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**33. How do you set up quality gates in SonarQube?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Cicd components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**34. How can you integrate Selenium tests into a CI/CD pipeline?**

??? success "Reveal answer"
    Choose a testing framework like TestNG or JUnit, write automated test scripts with Selenium WebDriver, configure
    the CI/CD tool to run those tests after the application is built and deployed to a test environment, and use Selenium
    Grid or Docker containers to run tests in parallel, isolated environments.

**35. How do you handle exceptions in Selenium?**

??? success "Reveal answer"
    Try-catch blocks around test code to catch exceptions like NoSuchElementException or TimeoutException, logging
    frameworks to capture error messages and stack traces, and capturing screenshots on failure with TakesScreenshot
    for visual evidence of what the app looked like at the time of failure.

**36. How do you configure Nexus Repository Manager?**

??? success "Reveal answer"
    Install Nexus, access the web interface, create the repositories needed -- hosted, proxy, or group -- configure
    security roles and permissions, set up proxy repository remote URLs and caching if needed, and point build tools like
    Maven or npm at the Nexus repository for dependency resolution.

**37. How does SonarQube work in a CI/CD pipeline?**

??? success "Reveal answer"
    The SonarQube Scanner runs during the build phase, analyzing source code and sending results back to the
    SonarQube server, which generates a report of issues. The pipeline can be configured to fail if the defined quality
    gate isn't met, blocking poor-quality code from being released.

**38. What challenges might you face when running Selenium tests in a CI/CD environment?**

??? success "Reveal answer"
    Keeping the test environment consistent with production, browser compatibility differences causing inconsistent
    results, flaky tests undermining trust in pipeline feedback, and resource strain from running tests in parallel if not
    managed carefully, leading to longer execution times.

**39. How do you implement CI/CD using Azure Pipelines?**

??? success "Reveal answer"
    Define a pipeline using YAML or the visual designer, connect it to the source repository, define build steps for
    compiling and testing, set up release pipelines to deploy to various environments, and configure triggers so builds
    kick off automatically on commits or pull requests.

**40. How do you handle synchronization issues in Selenium tests?**

??? success "Reveal answer"
    Implicit waits set a default wait time for elements, explicit waits (WebDriverWait) wait for a specific condition before
    proceeding -- more flexible than implicit waits -- and fluent waits let me define polling frequency and which exceptions
    to ignore during the wait period.

## Related

- Hub: [Interview Preparation](index.md)
{% endraw %}
