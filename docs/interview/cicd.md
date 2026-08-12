---
title: "CI/CD Interview Preparation"
description: "32 curated CI/CD interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
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

<div class="ra-interview-qa" markdown="1">

## Core concepts

**1. Can you explain the different stages of a CI/CD pipeline?**

??? success "Reveal answer"
    **In short:** Build once, prove quality, then promote the same immutable artefact toward production.
    
    **Key points**
    
    - **Source** — commit/MR webhook starts the pipeline.
    - **Build & unit test** — compile/package and fast feedback.
    - **Security & quality** — SAST, SCA, secrets, Sonar quality gate.
    - **Package** — push image/artefact by digest to a registry.
    - **Deploy & verify** — Dev → staging → prod with smoke tests and observe.
    
    **Trap**
    
    - Rebuilding per environment creates “works in staging” ghosts — promote digests, not rebuilds.

**2. What are the key features of SonarQube?**

??? success "Reveal answer"
    **In short:** SonarQube is a continuous code-quality platform with gates CI can fail on.
    
    **Key points**
    
    - Static analysis for bugs, vulnerabilities, smells, and security hotspots.
    - Branch/PR analysis with IDE decoration and coverage/duplication metrics.
    - Quality gates enforce new-code standards before merge.
    - Trends and portfolios help architects track debt over time.
    
    **Trap**
    
    - Turning on every rule overnight on brownfield code freezes delivery — start with new-code gates.

**3. What is the difference between bugs, vulnerabilities, and code smells in SonarQube?**

??? success "Reveal answer"
    **In short:** Bugs break behaviour; vulnerabilities invite attackers; smells make change expensive.
    
    **Key points**
    
    - **Bugs** — reliability defects likely to fail at runtime.
    - **Vulnerabilities** — exploitable patterns (injection, weak crypto).
    - **Code smells** — maintainability issues (complexity, duplication).
    - Hotspots need human security review, not auto-fail alone.
    
    **Trap**
    
    - Mass “Won’t fix” without review is theatre — remediate, test, or document accepted risk.

**4. What is the SonarQube Scanner, and how is it used?**

??? success "Reveal answer"
    **In short:** The scanner is the CI client that ships source and coverage metadata to the SonarQube server.
    
    **Key points**
    
    - Configure `sonar.host.url`, token, `sonar.projectKey`, and branch/PR params.
    - Generate coverage reports before analysis so gates see real data.
    - Pin scanner versions; use least-privilege tokens over HTTPS.
    - Exclude generated/vendor paths explicitly.
    
    **Try this**
    
    - `sonar-scanner`
    - `mvn sonar:sonar`
    - `dotnet sonarscanner`
    
    **Trap**
    
    - Analysing generated code without exclusions floods false positives and kills the gate’s credibility.

**5. What are some best practices when using SonarQube in a CI/CD pipeline?**

??? success "Reveal answer"
    **In short:** Scan every PR, gate on new code, and never bypass with admin magic.
    
    **Key points**
    
    - Fail the pipeline on quality-gate ERROR.
    - Curate quality profiles; exclude generated code.
    - Shift left with SonarLint in the IDE.
    - Store tokens as CI secrets; publish the dashboard link in logs.
    - Brownfield: tighten new code first, then chip away at legacy.
    
    **Trap**
    
    - Admin “force pass” teaches teams that quality is optional.

**6. What is SonarQube, and why is it used?**

??? success "Reveal answer"
    **In short:** SonarQube continuously inspects code so teams catch bugs and security issues before release.
    
    **Key points**
    
    - Finds bugs, vulnerabilities, smells, and hotspots via static analysis.
    - Tracks coverage, duplication, and complexity trends.
    - Quality gates give CI a clear pass/fail for merge or release.
    - Used to make code review and security reviews evidence-based.
    
    **Trap**
    
    - Treating Sonar as a dashboard only — without failing CI — wastes the investment.

**7. What is maven and explain about repositories?**

??? success "Reveal answer"
    **In short:** Maven builds Java projects from a POM and resolves dependencies from repositories.
    
    **Key points**
    
    - Coordinates: `groupId`, `artefactId`, `version`.
    - Lifecycles: compile → test → package → verify → deploy.
    - **Local** (`~/.m2`), **remote** (Central), and **internal** (Nexus/Artifactory).
    - Proxy/group repos give CI one stable URL and cache upstream.
    
    **Trap**
    
    - Never treat developer laptops as the source of jars — resolve from managed repos only.

**8. What is the role of continuous integration?**

??? success "Reveal answer"
    **In short:** CI merges small changes often and proves each one with automated build and tests.
    
    **Key points**
    
    - Keeps mainline releasable and shortens feedback loops.
    - Surfaces integration bugs in minutes, not at release week.
    - Requires fast tests, trunk-based or short-lived branches, and green builds.
    - CI is the gate before CD promotes artefacts.
    
    **Trap**
    
    - Calling a nightly build “CI” while merging huge feature branches for weeks.

**9. What is the output of sonarqube, how to fix if any smell code/vurnabilities found?**

??? success "Reveal answer"
    **In short:** Sonar outputs issues, metrics, and a quality-gate status — fix by changing code, not silencing rules.
    
    **Key points**
    
    - Dashboard lists bugs, vulnerabilities, smells, and hotspots with rule guidance.
    - CI shows gate pass/fail and a deep link for developers.
    - Fix: read the rule, patch/refactor, add tests, re-scan the PR.
    - Accepted risk needs documented review — especially for security findings.
    
    **Trap**
    
    - Bulk “Won’t fix” on vulnerabilities without security sign-off.

**10. What is pom.xml in maven?**

??? success "Reveal answer"
    **In short:** `pom.xml` is Maven’s Project Object Model — the declarative build definition.
    
    **Key points**
    
    - Declares coordinates, packaging, properties, and dependencies.
    - `dependencyManagement` / BOMs pin versions for multi-module builds.
    - Plugins drive compile, test, package, and deploy phases.
    - `distributionManagement` points releases at Nexus/Artifactory.
    
    **Try this**
    
    - `mvn -q help:effective-pom`
    - `mvn test package`
    
    **Trap**
    
    - Open-ended version ranges make builds non-deterministic across days.

**11. Difference between Continuous Delivery and Continuous Deployment?**

??? success "Reveal answer"
    **In short:** Delivery is always releasable with a human gate; Deployment releases every green change automatically.
    
    **Key points**
    
    - **Continuous Delivery** — artefact ready; prod needs approval/change ticket.
    - **Continuous Deployment** — automated prod release after gates pass.
    - Both need strong tests, observability, and fast rollback.
    - Regulated systems often stop at Delivery; product teams may Deploy.
    
    **Trap**
    
    - Calling auto-deploy to staging “Continuous Deployment” — prod is the distinction.

**12. What are the main features of Nexus Repository Manager?**

??? success "Reveal answer"
    **In short:** Nexus hosts, proxies, and groups artefacts so CI has one controlled supply chain.
    
    **Key points**
    
    - **Hosted** — publish internal libs/images.
    - **Proxy** — cache Central/npm/Docker Hub.
    - **Group** — single URL for consumers.
    - Access control, cleanup policies, search, REST APIs; IQ adds licence/CVE policy.
    
    **Trap**
    
    - Leaving anonymous write on hosted repos turns Nexus into a malware dropbox.

**13. What are SonarQube Quality Gates?**

??? success "Reveal answer"
    **In short:** Quality gates are pass/fail policies Sonar evaluates after each analysis.
    
    **Key points**
    
    - Typical conditions: no new criticals, coverage on new code, duplication caps.
    - CI waits for gate status and fails on ERROR.
    - Focus on new code so brownfield teams can still ship safely.
    - Different gates can apply per project or portfolio risk.
    
    **Trap**
    
    - Release jobs that skip the gate check make the dashboard decorative.

**14. What is Nexus Repository Manager?**

??? success "Reveal answer"
    **In short:** Nexus Repository Manager is Sonatype’s artefact registry for binaries your builds depend on.
    
    **Key points**
    
    - Stores and versions Maven, npm, PyPI, Docker, Helm, and more.
    - Proxies public registries to cut flaky internet and improve auditability.
    - Becomes the system of record for release artefacts and digests.
    - Pairs with CI promote flows: snapshot → staging → release.
    
    **Trap**
    
    - Pointing prod builds at public internet mirrors without a proxy loses reproducibility.

**15. What is SonarLint, and how does it relate to SonarQube?**

??? success "Reveal answer"
    **In short:** SonarLint is the IDE companion that surfaces many Sonar rules before you commit.
    
    **Key points**
    
    - Works in IntelliJ, VS Code, Eclipse, and others.
    - Connected mode syncs quality profiles with SonarQube/SonarCloud.
    - Shifts feedback left — minutes in the IDE beat hours in CI.
    - Does not replace server analysis and quality gates.
    
    **Trap**
    
    - Assuming SonarLint alone equals CI Sonar coverage — PR analysis still required.

**16. What are GitLab CI/CD pipelines?**

??? success "Reveal answer"
    **In short:** GitLab CI/CD pipelines are YAML-defined workflows runners execute on repo events.
    
    **Key points**
    
    - Defined in `.gitlab-ci.yml` with stages, jobs, and optional `needs` DAG.
    - Triggers: push, MR, schedule, API; jobs produce artefacts and reports.
    - Environments and deploy jobs track Dev/UAT/Prod promotions.
    - Includes and parent–child pipelines keep configs modular.
    
    **Try this**
    
    - `.gitlab-ci.yml`
    - `stages:` / `needs:`
    
    **Trap**
    
    - Unscoped `rules: if: $CI_COMMIT_BRANCH` can run deploy jobs on every feature branch.

## Scenarios and troubleshooting

**17. How do you implement a complete production-grade pipeline that incorporates all the tools discussed?**

??? success "Reveal answer"
    **In short:** A production pipeline: build → test → security → package digest → promote environments with verify.
    
    **Key points**
    
    - CI: unit tests, Sonar gate, SCA/SAST/secret scan, container build.
    - Publish immutable image/artefact to Nexus/ECR with SBOM.
    - CD: deploy Dev → UAT → Prod via GitOps or controlled releases.
    - Post-deploy smoke, metrics, and automated rollback hooks.
    - Secrets via vault/OIDC — never in Git.
    
    **Trap**
    
    - Different build flags per environment — you no longer know what you tested.

**18. How do you prioritize and manage multiple critical issues in a CI/CD pipeline failure?**

??? success "Reveal answer"
    **In short:** Triage by blast radius: stop the bleeding, then fix the highest-impact failures first.
    
    **Key points**
    
    - Classify: infra/runner, flaky test, real regression, security gate, deploy.
    - Pause prod promotion if artefact integrity is uncertain.
    - Parallelise: one owner on rollback, one on root cause, one on comms.
    - Re-run only after isolating flakes; don’t burn the queue with blind retries.
    
    **Trap**
    
    - Retrying a failed security gate “to unblock the release” without understanding it.

**19. How would you set up entire CI/CD setup for this application?**

??? success "Reveal answer"
    **In short:** Start from the app’s risk: language, tests, artefact type, environments, and rollback story.
    
    **Key points**
    
    - Repo layout + branch protection + required status checks.
    - CI: build, test, lint, Sonar, dependency and image scans.
    - Registry + versioning (semver or git SHA digest).
    - CD path: Dev auto, UAT gated, Prod with approval/GitOps.
    - Observability and runbooks before the first prod deploy.
    
    **Trap**
    
    - Designing pretty YAML before you know how you will roll back a bad migration.

**20. CI/CD pipeline needs rollback capability. How would you implement it?**

??? success "Reveal answer"
    **In short:** Rollback means re-releasing the last known-good artefact — not rebuilding from memory.
    
    **Key points**
    
    - Keep previous image digests and Helm/GitOps revisions immutable.
    - Automate `rollback` jobs or Argo/ rollout undo on failed smoke/SLO.
    - DB changes must be expand/contract so schema stays compatible.
    - Practice rollback in UAT; measure time-to-recover.
    
    **Trap**
    
    - Mutable `latest` tags make “roll back” impossible — the tag already moved.

**21. Suppose you are implementing a Canary deployment where only 10% of users receive the new version. How would you implement it through your CI/CD pipeline?**

??? success "Reveal answer"
    **In short:** Ship the new digest to a small cohort, measure, then promote or abort.
    
    **Key points**
    
    - Deploy canary pods/tasks alongside stable; shift ~10% traffic.
    - Use mesh/Ingress/ALB weights or feature flags for user targeting.
    - Gate on error rate, latency, and business KPIs via analysis jobs.
    - CI only updates the canary revision; promotion is a separate approve step.
    
    **Trap**
    
    - Canary without metrics is just a partial deploy — you learn nothing until customers shout.

**22. Explain your complete CI/CD pipeline from code commit to production deployment?**

??? success "Reveal answer"
    **In short:** Commit triggers CI; green digest promotes through environments until prod verify passes.
    
    **Key points**
    
    - Commit/PR → build + unit tests + quality/security gates.
    - Publish artefact/image by digest; attach SBOM and provenance.
    - Deploy Dev, run integration/smoke; promote to UAT with approvals.
    - Prod release via GitOps/CD; watch SLOs; rollback path ready.
    
    **Trap**
    
    - Manual “build on the prod server” steps that bypass the artefact you tested.

## Practice questions

**23. How do you implement feature flags in a CI/CD pipeline?**

??? success "Reveal answer"
    **In short:** Feature flags decouple deploy from release so dark code can ship safely.
    
    **Key points**
    
    - Flags in a managed service or config; default off in prod.
    - Pipeline deploys code with flags; product toggles exposure.
    - Use for canary cohorts, kill switches, and gradual rollout.
    - Clean up stale flags — they become technical debt and risk.
    
    **Trap**
    
    - Long-lived flags that leave two code paths forever — eventually both break.

**24. How do Continuous Integration (CI) and Continuous Deployment (CD) work together?**

??? success "Reveal answer"
    **In short:** CI proves every change; CD takes the proven artefact and puts it where users need it.
    
    **Key points**
    
    - CI owns build, test, and package of an immutable artefact.
    - CD owns environment promotion, approvals, and verify.
    - Together they shrink lead time while keeping mainline releasable.
    - Shared contract: digests, gates, and rollback hooks.
    
    **Trap**
    
    - CD that rebuilds from source instead of promoting the CI artefact.

**25. How do you design and implement a complete CI/CD pipeline for ML models?**

??? success "Reveal answer"
    **In short:** Treat models like versioned artefacts: data → train → evaluate → register → deploy → monitor.
    
    **Key points**
    
    - Pipeline stages for data validation, training, and offline metrics.
    - Register model + lineage in a model registry with approval gates.
    - Deploy behind shadow/canary traffic; compare online metrics.
    - Monitor drift, latency, and business KPIs; auto-rollback on regression.
    
    **Trap**
    
    - Deploying a model because training loss looked fine — without a holdout or online gate.

**26. How can you monitor the health and performance of Nexus Repository Manager?**

??? success "Reveal answer"
    **In short:** Watch Nexus like any critical service: availability, disk, latency, and auth failures.
    
    **Key points**
    
    - Metrics: JVM heap, request latency, blob store disk, queue depth.
    - Alert on 5xx rates, disk >80%, and failed blob uploads.
    - Audit logs for anonymous access and privilege changes.
    - Synthetic checks: resolve a known artefact from CI runners.
    
    **Try this**
    
    - Nexus status/metrics endpoints
    - Prometheus JMX exporter pattern
    
    **Trap**
    
    - Ignoring blob-store disk until publishes start failing mid-release.

**27. How do you write in yaml to create a ci/cd pipeline from scratch to test and deploy from Dev to UAT?**

??? success "Reveal answer"
    **In short:** Declare stages for test and progressive deploy; gate UAT with rules and environments.
    
    **Key points**
    
    - YAML stages: `build` → `test` → `deploy_dev` → `deploy_uat`.
    - Use `environment:` names and optional `when: manual` for UAT.
    - Pass the same artefact/image digest between jobs via artefacts/vars.
    - Protect UAT/prod jobs with protected branches and environments.
    
    **Try this**
    
    - GitLab `stages:` / `environment:`
    - GitHub `environment:` + `needs:`
    
    **Trap**
    
    - Hard-coding hostnames per stage instead of promoting one digest.

**28. How do you integrate tools like SonarQube into your pipelines?**

??? success "Reveal answer"
    **In short:** Run the Sonar scanner after tests/coverage, then fail the job on quality-gate ERROR.
    
    **Key points**
    
    - Generate coverage, invoke scanner with project/branch/PR params.
    - Wait for quality gate (webhook or poller plugin).
    - Decorate MRs with issues; link the dashboard in CI logs.
    - Keep token in CI secrets; pin scanner version.
    
    **Trap**
    
    - Scanning without coverage reports — gates look green while tests are thin.

**29. How do you set up quality gates in SonarQube?**

??? success "Reveal answer"
    **In short:** Define gate conditions on new code, attach them to the project, and enforce in CI.
    
    **Key points**
    
    - Create a Quality Gate (coverage, zero new criticals, duplication).
    - Set the project’s default gate; prefer new-code period.
    - CI fails when gate status is ERROR.
    - Review exceptions with security/architecture — not chat approvals.
    
    **Trap**
    
    - A gate with no failing conditions — always Passed is worse than no gate.

**30. How do you configure Nexus Repository Manager?**

??? success "Reveal answer"
    **In short:** Create blob stores and hosted/proxy/group repos, then point CI and developers at the group URL.
    
    **Key points**
    
    - Configure storage, realms, and LDAP/SSO if needed.
    - Hosted for internals; proxy for Central/npm/Docker; group for clients.
    - Cleanup policies for snapshots; content selectors for least privilege.
    - Issue deploy tokens/users for CI only — no shared admin passwords.
    
    **Trap**
    
    - Anonymous read+write “to make CI work” permanently.

**31. How does SonarQube work in a CI/CD pipeline?**

??? success "Reveal answer"
    **In short:** CI builds and tests, then Sonar analyses the PR; a failed gate blocks merge or release.
    
    **Key points**
    
    - Job order: build → test/coverage → sonar-scanner → gate wait.
    - PR decoration shows new issues on the changed lines.
    - Main/release pipelines can use stricter gates than feature branches.
    - Results feed dashboards for debt trends across teams.
    
    **Trap**
    
    - Running Sonar only on nightly main — bugs land in main before anyone sees them.

**32. How do you implement CI/CD using Azure Pipelines?**

??? success "Reveal answer"
    **In short:** Azure Pipelines uses YAML pipelines with stages, jobs, and environments tied to Azure DevOps.
    
    **Key points**
    
    - `azure-pipelines.yml` defines stages for build, test, and deploy.
    - Agents (Microsoft-hosted or self-hosted) run jobs; environments gate prod.
    - Service connections/OIDC authenticate to Azure/ACR/AKS securely.
    - Approvals and checks on environments implement Continuous Delivery gates.
    
    **Try this**
    
    - `trigger:`
    - `stages:` / `jobs:` / `steps:`
    - `environment: production`
    
    **Trap**
    
    - Storing long-lived SP passwords in variable groups instead of workload identity/OIDC.

## Related
- Hub: [Interview Preparation](index.md)
{% endraw %}
