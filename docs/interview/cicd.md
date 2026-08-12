---
title: "CI/CD Interview Preparation"
description: "40 curated interview questions and model answers for CI/CD — concepts, scenarios, troubleshooting, and production trade-offs."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. What is the difference between Continuous Integration, Continuous Delivery, and Continuous Deployment?**

??? success "Reveal answer"
    These three terms are often confused, even by experienced engineers. Here's the clearest way to 
    explain them: 
    Continuous Integration (CI): The practice of automatically building and testing code every time 
    a developer pushes a change. The goal is to detect bugs early, when they are cheap to fix. 
    • 
    Trigger: Code push to repository 
    • 
    Actions: Build → Unit Test → Code Quality Scan 
    • 
    Output: Pass/Fail signal within minutes 
    Continuous Delivery (CD - Delivery): Extends CI by automatically preparing the code for release 
    to production. The key word here is prepared — the deployment to production may still require a 
    human to press a button. 
    • 
    Trigger: Successful CI build 
    • 
    Actions: Integration Tests → Staging Deploy → Smoke Tests 
    • 
    Output: A release-ready artifact that can go to production anytime 
    Continuous Deployment (CD - Deployment): The most aggressive form. Every change that 
    passes all automated tests goes automatically to production without any human intervention. 
    • 
    Trigger: Successful staging tests 
    • 
    Actions: Production Deploy → Health…

**2. What is AWS CodePipeline, and how do you set up a basic CI/CD pipeline?**

??? success "Reveal answer"
    AWS CodePipeline is a fully managed continuous delivery service that automates your release 
    pipelines. It orchestrates the stages of your build, test, and deploy process by connecting AWS 
    services and third-party tools. 
    CodePipeline consists of: 
    • 
    Source stage — where code lives (CodeCommit, GitHub, S3) 
    • 
    Build stage — where code is compiled and tested (CodeBuild) 
    • 
    Deploy stage — where artifacts are deployed (CodeDeploy, ECS, Elastic Beanstalk, 
    CloudFormation) 
    Creating a pipeline using Terraform: 
    # CodePipeline for an ECS application 
    resource "aws_codepipeline" "app_pipeline" { 
     name = "my-app-pipeline" 
     role_arn = aws_iam_role.codepipeline_role.arn 
     artifact_store { 
     location = aws_s3_bucket.pipeline_artifacts.bucket 
     type = "S3" 
    
     
     encryption_key { 
     id = aws_kms_key.pipeline_key.arn 
     type = "KMS" 
     } 
     } 
     # Stage 1: Source — pull from GitHub 
     stage { 
     name = "Source" 
     action { 
     name = "GitHub_Source" 
     category = "Source" 
     owner = "ThirdParty" 
     provider = "GitHub" 
     version = "1" 
     output_artifacts = ["source_output"] 
    …

**3. What is SonarQube, and how do you integrate it into a CI/CD pipeline?**

??? success "Reveal answer"
    SonarQube is a static code analysis platform that scans your code for: 
    • 
    Bugs — potential runtime errors 
    • 
    Code smells — maintainability issues 
    • 
    Security vulnerabilities — SQL injection, XSS, hardcoded passwords 
    • 
    Code coverage — what percentage of your code is tested 
    • 
    Technical debt — estimate of time needed to fix all issues 
    • 
    Duplicate code — copy-paste violations 
    Integration in Jenkins: 
    stage('SonarQube Analysis') { 
     steps { 
     withSonarQubeEnv('SonarQube-Server') { // Configured in Jenkins 
     sh """ 
     mvn sonar:sonar \ 
     -Dsonar.projectKey=my-app \ 
     -Dsonar.projectName='My Application' \ 
    
     
    Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml 
     """ 
     } 
     } 
    } 
    stage('Quality Gate') { 
     steps { 
     // Wait for SonarQube to finish analysis 
     timeout(time: 10, unit: 'MINUTES') { 
     waitForQualityGate abortPipeline: true 
     // Pipeline FAILS if quality gate conditions are not met 
     } 
     } 
    } 
    SonarQube Quality Gate conditions (production standards): 
    Coverage on new code: ≥ 80% 
    Duplicated lines on new code: < 3% 
    Maintainability…

**4. What is Nexus/JFrog Artifactory, and why do you need an artifact repository in CI/CD?**

??? success "Reveal answer"
    An artifact repository is a centralized storage and management system for build artifacts — 
    Docker images, Maven JARs, npm packages, Helm charts, Python wheels, and more. 
    Why you need one: 
    Without an artifact repository, teams typically push Docker images to Docker Hub or store JARs 
    on S3. This works, but creates problems at scale: 
    • 
    No caching of external dependencies — every build re-downloads from the internet 
    (slow, fragile) 
    • 
    No access control on who can pull/push what 
    • 
    No vulnerability scanning of artifacts before they're used 
    • 
    No immutability — anyone can overwrite a published version 
    • 
    No single inventory of what versions are deployed where 
    
     
    Nexus Repository Manager — common operations: 
    # Configure npm to use Nexus as proxy 
    npm config set registry https://nexus.company.com/repository/npm-group/ 
    npm config set //nexus.company.com/repository/npm-group/:_authToken 
    $NEXUS_TOKEN 
    # Configure Maven settings.xml for Nexus 
    cat ~/.m2/settings.xml 
    # <settings> 
    # <mirrors> 
    # <mirror> 
    # <id>nexus</id> 
    # <mirrorOf>*</mirrorOf> 
    #…

**5. What is CI/CD?**

??? success "Reveal answer"
    Key Points : 3 p
    =~) Answer : Developers commit code
    | Continuous Integration (CI) | V Frequent Code Merge es) v
    i i i Push code to Git Reposit
    2 Continuous Delivery (CD) | W Faster Feedback Jenkins Pipeline
    ensures that code is always \ UF J
    = ) in a deployable state. | W Less Manual Work I Buil
    Continuous Deployment (CD) H ~ ests & Build
    a) automatically deploys every | 4% Quick Releases v
    successful build to production : rd Deploy to QA
    =) without manual approval. v Better Quality é
    ; ints : A_Insights E le :
    = 3) Why do we use Jenkins? a tn eee: _
    : ae tt ‘Riioeaitio | Instead of manually executing :
    i] Jenkins eliminates repetitive manual Y Scheduling | Hw Run Maven
    tasks by automating build, testing, Vv rae Run Selenium Suite
    =) deployment, report generation, Notifications
    notifications, and scheduling, Y Reports B Generate Report
    | It improves software quality, ; M4 Sand Enait
    reduces human errors, and speeds v Integrations ’ ;
    up release cycles. S Fostar Rel Jenkins performs everything
    =) CSTE E NERS: \_ automatically after every Git commit!
    (wa £ alae…

**6. What is the difference between a hosted, a proxy, and a group repository in Nexus?**

??? success "Reveal answer"
    A hosted repository stores your own uploaded artifacts, typically for internal projects. A proxy repository caches
    artifacts from a remote source like Maven Central, speeding up builds and reducing internet dependency. A group
    repository aggregates multiple hosted and proxy repositories behind a single URL, simplifying dependency resolution
    for consumers.
    KEY POINTS TO MENTION
    • Hosted: your own artifacts
    • Proxy: cached external dependencies
    • Group: aggregates repos behind one endpoint

**7. What is CI & CD?**

??? success "Reveal answer"
    CI means Continuous Integration and CD means Continuous Delivery/Deploy. Whenever developers
    write code, we integrate all that code at that point of time and we build, test and deliver/deploy to the
    client. Jenkins helps in achieving this. Instead of doing night builds, we build as and when a commit
    occurs by integrating all code in the SCM tool, building, testing and checking quality — this is
    Continuous Integration.
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers

**8. Can you explain the different stages of a CI/CD pipeline?**

??? success "Reveal answer"
    Source stage where code is committed to version control; build stage where source compiles into an executable or
    package; test stage running unit, integration, and performance tests; artifact stage where the build becomes a
    deployable unit stored in a repository; deployment stage pushing to staging and then production after approval; and
    post-deployment monitoring to confirm stability.

**9. What is the role of Selenium in the testing pyramid?**

??? success "Reveal answer"
    Selenium sits in the UI testing layer, handling end-to-end validation of user interactions, and should complement --
    not replace -- unit tests at the base and integration tests in the middle. Using it wisely within that pyramid, rather than
    over-relying on it, optimizes both coverage and test-suite speed.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    2
    4
    NEXUS

**10. What are the key features of SonarQube?**

??? success "Reveal answer"
    Code quality management tracking bugs, vulnerabilities, and code smells; security hotspot detection for risks like
    SQL injection or XSS; technical debt management estimating the time to fix detected issues; CI/CD integration with
    Jenkins, GitHub Actions, GitLab CI; custom quality profiles for project-specific rules; and support for over 25
    programming languages.

**11. What are the advantages of using Trivy?**

??? success "Reveal answer"
    Simple to install and use, fast scanning, comprehensive coverage across multiple artifact types -- images,
    filesystems, Git repos -- a continuously updated vulnerability database, and easy integration into CI/CD for
    automated, repeatable security checks.
    KEY POINTS TO MENTION
    • Simplicity, speed, comprehensive coverage, continuous updates, easy CI/CD integration

**12. Can you explain how you would use Selenium Grid for testing?**

??? success "Reveal answer"
    Start the Selenium Grid Hub as the central control point, register multiple nodes specifying available browsers and
    versions, point test scripts at the Grid Hub instead of a local driver, and run the tests -- the hub distributes them
    across nodes based on requested browser and capabilities.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**13. What is the difference between bugs, vulnerabilities, and code smells in SonarQube?**

??? success "Reveal answer"
    Bugs are issues likely to cause incorrect or unexpected runtime behaviour. Vulnerabilities are security risks like SQL
    injection or XSS that could be exploited. Code smells are maintainability concerns that don't cause immediate errors
    but make the codebase harder to work with over time.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**14. What is the SonarQube Scanner, and how is it used?**

??? success "Reveal answer"
    The SonarQube Scanner analyzes source code and sends results to the SonarQube server, run either manually via
    the sonar-scanner command or as part of a CI/CD pipeline, configured through a sonar-project.properties file with the
    relevant project and server details.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    2
    2
    TRIVY

**15. What are some best practices when using SonarQube in a CI/CD pipeline?**

??? success "Reveal answer"
    Automate quality gate checks so the pipeline actually fails when the gate isn't met, aim for solid test coverage to
    catch untested code paths, analyze frequently -- ideally every commit or pull request -- customize quality profiles to
    the team's actual standards, and prioritize fixing bugs and vulnerabilities over code smells.

**16. What are the different components of Selenium?**

??? success "Reveal answer"
    Selenium WebDriver provides the programming interface for writing and executing test scripts; Selenium IDE is a
    browser extension for recording and playing back tests; Selenium Grid enables parallel test execution across
    machines and browsers; and Selenium RC is the older, largely deprecated component WebDriver has replaced.

**17. What is SonarQube, and why is it used?**

??? success "Reveal answer"
    SonarQube is an open-source platform that continuously inspects code quality, detecting bugs, vulnerabilities, and
    code smells across many languages, integrating tightly with CI/CD pipelines so teams improve code quality through
    consistent static analysis rather than relying on manual review alone.

**18. What are the main features of Nexus Repository Manager?**

??? success "Reveal answer"
    Support for multiple repository formats, proxying and caching remote repositories to speed up builds, straightforward
    artifact upload/storage/retrieval, fine-grained security and access control, seamless CI/CD tool integration, and
    repository health checks for monitoring performance.

**19. What are the ways to do Continuous Integration?**

??? success "Reveal answer"
    There are three ways:
    • Manually: Write code, build, test and deploy all manually
    • Scripts: Write scripts to automate the CI/CD process (complex to write)
    • Tool: Using tools like Jenkins is very handy — everything is pre-configured, less manual
    intervention (most preferred way)

**20. What are SonarQube Quality Gates?**

??? success "Reveal answer"
    A Quality Gate is a set of conditions -- around bugs, vulnerabilities, coverage, duplication -- that a project must meet
    to be considered acceptable. Configuring the pipeline to fail when the gate isn't met is what actually enforces the
    standard rather than just reporting on it.

**21. What is Selenium, and how is it used in DevOps?**

??? success "Reveal answer"
    Selenium is an open-source framework for automating web application testing. In DevOps I integrate it into CI/CD
    pipelines to automatically verify that new code changes don't break existing functionality, maintaining software quality
    while still enabling frequent releases.

**22. What is Trivy?**

??? success "Reveal answer"
    Trivy is an open-source vulnerability scanner for containers and other artifacts, identifying vulnerabilities in OS
    packages and application dependencies across Docker images, filesystems, and Git repositories, checked against a
    continuously updated CVE database.

**23. What is Nexus Repository Manager?**

??? success "Reveal answer"
    Nexus Repository Manager is a repository management tool for storing and sharing software artifacts, supporting
    formats like Maven, npm, NuGet, and Docker. It centralizes binary management, improving dependency
    management and CI/CD integration across teams.

**24. What is SonarLint, and how does it relate to SonarQube?**

??? success "Reveal answer"
    SonarLint is an IDE plugin providing real-time code analysis as developers write code, letting issues get caught and
    fixed locally before a commit even happens -- complementing SonarQube by giving instant feedback rather than
    waiting for a CI-stage scan.

**25. What are GitLab CI/CD pipelines?**

??? success "Reveal answer"
    Pipelines are the automated processes defined in .gitlab-ci.yml that build, test, and deploy code -- made up of stages
    that run sequentially, each containing jobs that run concurrently, ensuring consistent delivery and automating
    repetitive tasks.

## Scenarios and troubleshooting

**26. How do you implement a complete production-grade pipeline that incorporates all the tools discussed?**

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

**27. How would you design a CI/CD pipeline for a project?**

??? success "Reveal answer"
    Code commit triggers the pipeline: build with the right tool for the stack -- Maven, npm, pip -- automated testing
    including unit and integration tests, static code analysis with something like SonarQube or ESLint, packaging into an
    artifact like a JAR or Docker image, storing that artifact in a repository like Nexus or Docker Hub, deploying to staging
    for further testing, an approval gate before production, deployment to production, and post-deployment monitoring
    with Grafana and Prometheus to confirm the release is stable.
    KEY POINTS TO MENTION
    • Commit → build → test → static analysis → package → store artifact → staging → approval → prod → monitor

## Practice questions

**28. How do you implement feature flags in a CI/CD pipeline?**

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

**29. How do you handle database migrations safely in a CI/CD pipeline?**

??? success "Reveal answer"
    Database migrations are one of the highest-risk operations in a pipeline. A bad migration can 
    corrupt data, cause downtime, or leave the database in a partially migrated state that's hard to 
    recover from. 
    The golden rules for safe database migrations: 
    1. Migrations must be backward-compatible — the new code must work with both old 
    and new schema during the deployment window 
    2. Separate migration from deployment — run migrations before deploying new code 
    3. Never drop columns or tables immediately — deprecate first, remove in a later release 
    
     
    4. Test migrations against a production-size dataset — a migration that takes 2 seconds 
    on dev might take 2 hours on production 
    Using Flyway for Java/Spring applications: 
    -- V1__initial_schema.sql 
    CREATE TABLE users ( 
     id BIGSERIAL PRIMARY KEY, 
     email VARCHAR(255) UNIQUE NOT NULL, 
     created_at TIMESTAMP DEFAULT NOW() 
    ); 
    -- V2__add_user_profile.sql 
    -- Safe: adding a nullable column is backward-compatible 
    ALTER TABLE users ADD COLUMN full_name VARCHAR(255); 
    ALTER TABLE users ADD COLUMN phone VARCHAR(20);…

**30. How do Continuous Integration (CI) and Continuous Deployment (CD) work together?**

??? success "Reveal answer"
    CI is about integrating code changes into a shared repository multiple times a day, with each integration verified
    through automated builds and tests so errors are caught as early as possible. CD extends that by automatically
    deploying the tested, integrated code to production, so any change that passes the test suite reaches users with
    minimal manual intervention. Together, CI keeps the codebase stable through frequent verification, while CD makes
    sure that stable code actually reaches production quickly and reliably.

**31. How can you monitor the health and performance of Nexus Repository Manager?**

??? success "Reveal answer"
    The Nexus web UI provides basic usage and performance stats, built-in health check reports monitor repository
    status, and integrating Nexus with external tools like Prometheus or Grafana gives more detailed metrics and alerting
    on performance and usage.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    2
    5
    COMBINED: GITHUB ACTIONS, ARGOCD &
    KUBERNETES

**32. How can you integrate Selenium tests into a CI/CD pipeline?**

??? success "Reveal answer"
    Choose a testing framework like TestNG or JUnit, write automated test scripts with Selenium WebDriver, configure
    the CI/CD tool to run those tests after the application is built and deployed to a test environment, and use Selenium
    Grid or Docker containers to run tests in parallel, isolated environments.

**33. How does Trivy work?**

??? success "Reveal answer"
    It analyzes the image to identify its OS packages and language dependencies, checks those against its vulnerability
    database, and generates a report detailing findings -- severity, description, remediation guidance.
    KEY POINTS TO MENTION
    • Image analysis → vulnerability database check → detailed report

**34. How do you handle exceptions in Selenium?**

??? success "Reveal answer"
    Try-catch blocks around test code to catch exceptions like NoSuchElementException or TimeoutException, logging
    frameworks to capture error messages and stack traces, and capturing screenshots on failure with TakesScreenshot
    for visual evidence of what the app looked like at the time of failure.

**35. How do you configure Nexus Repository Manager?**

??? success "Reveal answer"
    Install Nexus, access the web interface, create the repositories needed -- hosted, proxy, or group -- configure
    security roles and permissions, set up proxy repository remote URLs and caching if needed, and point build tools like
    Maven or npm at the Nexus repository for dependency resolution.

**36. How does SonarQube work in a CI/CD pipeline?**

??? success "Reveal answer"
    The SonarQube Scanner runs during the build phase, analyzing source code and sending results back to the
    SonarQube server, which generates a report of issues. The pipeline can be configured to fail if the defined quality
    gate isn't met, blocking poor-quality code from being released.

**37. What challenges might you face when running Selenium tests in a CI/CD environment?**

??? success "Reveal answer"
    Keeping the test environment consistent with production, browser compatibility differences causing inconsistent
    results, flaky tests undermining trust in pipeline feedback, and resource strain from running tests in parallel if not
    managed carefully, leading to longer execution times.

**38. How do you implement CI/CD using Azure Pipelines?**

??? success "Reveal answer"
    Define a pipeline using YAML or the visual designer, connect it to the source repository, define build steps for
    compiling and testing, set up release pipelines to deploy to various environments, and configure triggers so builds
    kick off automatically on commits or pull requests.

**39. How do you handle synchronization issues in Selenium tests?**

??? success "Reveal answer"
    Implicit waits set a default wait time for elements, explicit waits (WebDriverWait) wait for a specific condition before
    proceeding -- more flexible than implicit waits -- and fluent waits let me define polling frequency and which exceptions
    to ignore during the wait period.

**40. What types of vulnerabilities can Trivy detect?**

??? success "Reveal answer"
    OS package vulnerabilities across distributions like Ubuntu or Alpine, language-specific vulnerabilities in npm,
    Python, or Ruby dependencies, misconfigurations in infrastructure-as-code files, and known vulnerabilities in
    third-party libraries.

## Related

- Hub: [Interview Preparation](index.md)
{% endraw %}
