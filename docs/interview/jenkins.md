---
title: "Jenkins Interview Preparation"
description: "44 curated Jenkins interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: jenkins
tags:
  - interview
  - jenkins
comments: false
---

{% raw %}
# Jenkins Interview Preparation

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

**1. What is Jenkins, and why is it used in DevOps?**

??? success "Reveal answer"
    **In short:** Jenkins is an automation server that runs CI/CD pipelines as code across agents.
    
    **Key points**
    
    - Orchestrates build, test, scan, and deploy jobs from Git events.
    - Extensible via plugins; Declarative/Scripted Pipelines in Jenkinsfiles.
    - Controller schedules work; agents execute on labelled nodes.
    - Used when teams need self-hosted, highly customisable automation.
    
    **Trap**
    
    - An unpatched controller with anonymous signup is a common breach pattern.

**2. Explain the CI/CD workflow you follow and the kind of pipeline you use. How do you define and invoke pipelines in Jenkins?**

??? success "Reveal answer"
    **In short:** Define pipelines in Jenkinsfiles (often Multibranch) and trigger them from Git or upstream jobs.
    
    **Key points**
    
    - Prefer Declarative Pipeline in SCM over click-ops freestyle jobs.
    - Multibranch Pipeline discovers branches/PRs automatically.
    - Shared libraries hold reusable stages (build, scan, deploy).
    - Invoke via webhook, timer, or `build job:` from another pipeline.
    
    **Try this**
    
    - `pipeline { agent any; stages { ... } }`
    - Multibranch + GitHub/GitLab Branch Source
    
    **Trap**
    
    - Copy-pasting 200-line Jenkinsfiles per repo instead of a shared library.

**3. Describe your typical deployment flow and CI/CD workflow. What stages do you define in your Jenkins pipeline, and how do you ensure full quality checks during deployment?**

??? success "Reveal answer"
    **In short:** Typical flow: checkout → build/test → quality/security → package → deploy with gates.
    
    **Key points**
    
    - Stages mirror risk: unit, integration, Sonar/SCA, image build, promote.
    - Quality: fail on tests, coverage, and Sonar gate before packaging.
    - Deploy Dev automatically; UAT/Prod with approvals or GitOps handoff.
    - Post-actions archive artefacts, notify, and record digests.
    
    **Trap**
    
    - Deploying before quality stages “to save time” — you ship broken digests faster.

**4. How do you use Jenkins shared libraries? Explain their typical structure and how they are integrated into your Jenkinsfiles?**

??? success "Reveal answer"
    **In short:** Shared libraries centralise pipeline code under `vars/`, `src/`, and `resources/`.
    
    **Key points**
    
    - `vars/*.groovy` expose callables like `buildJava()` as steps.
    - `src/` holds supporting Groovy classes; `resources/` holds templates.
    - Configure Global Pipeline Libraries (modern SCM) with version tags.
    - `@Library('my-lib@1.4.0') _` pins a release in the Jenkinsfile.
    
    **Trap**
    
    - Tracking `main` of the library — every merge can break every pipeline overnight.

**5. What are the ways to trigger the pipeline in Jenkins?**

??? success "Reveal answer"
    **In short:** Trigger via SCM webhooks, timers, upstream jobs, API/CLI, or manual Build Now.
    
    **Key points**
    
    - GitHub/GitLab webhooks for push/PR events (preferred).
    - `triggers { cron(...) }` or Parameterized Scheduler plugins.
    - `build job: 'B', wait: true` from pipeline A.
    - Remote Access API / CLI for automation and chatops.
    
    **Trap**
    
    - Polling SCM every minute at scale — use webhooks instead.

**6. What are the different type of Jenkins pipeline?**

??? success "Reveal answer"
    **In short:** Freestyle, Pipeline (Declarative/Scripted), Multibranch, and Organisation folders.
    
    **Key points**
    
    - **Freestyle** — UI steps; avoid for new work.
    - **Pipeline** — Jenkinsfile as code.
    - **Multibranch** — one job per branch/PR from SCM.
    - **Org folder** — discover all repos in a GitHub/GitLab org.
    
    **Trap**
    
    - Staying on freestyle because “it works” — reviews and reuse suffer.

**7. What is the difference between Continuous Delivery and Continuous Deployment, and how do you implement them in Jenkins?**

??? success "Reveal answer"
    **In short:** Delivery stops at an approval before prod; Deployment auto-promotes every green build.
    
    **Key points**
    
    - In Jenkins: `input` steps or environment approvals for Delivery.
    - Deployment: no manual `input` — rely on automated gates and rollback.
    - Both promote the same artefact digest across environments.
    - Choose Delivery for regulated prod; Deployment for mature product teams.
    
    **Trap**
    
    - An `input` that emails everyone and waits days — that is not Continuous anything.

**8. What are shared libraries in Jenkins, and how are they written and defined?**

??? success "Reveal answer"
    **In short:** Shared libraries are versioned Groovy modules loaded into Jenkins pipelines.
    
    **Key points**
    
    - Repo layout: `vars/`, `src/`, `resources/`.
    - Define global library in Jenkins with trusted/untrusted loading rules.
    - Call steps as `myStep(app: 'api')` from Declarative stages.
    - Unit-test library code; release with tags/semver.
    
    **Trap**
    
    - Putting credentials or cluster kubeconfigs inside the library repo.

**9. What is self hosted agent and Microsoft host agent?**

??? success "Reveal answer"
    **In short:** Self-hosted agents are yours; Microsoft-hosted agents are Azure DevOps’ SaaS VMs — not Jenkins terms.
    
    **Key points**
    
    - In Azure DevOps: Microsoft-hosted vs self-hosted agent pools.
    - In Jenkins: analogous ideas are cloud agents vs static nodes you manage.
    - Self-hosted: custom tools, private network, you patch the OS.
    - Hosted: faster start, less ops, limited custom images/time.
    
    **Trap**
    
    - Answering “Jenkins Microsoft agent” literally — clarify Azure DevOps vs Jenkins.

**10. What are Jenkins agents?**

??? success "Reveal answer"
    **In short:** Agents (nodes) are the machines/executors that actually run pipeline steps.
    
    **Key points**
    
    - Controller schedules; agents with labels run `agent { label 'docker' }`.
    - Can be VMs, Kubernetes pods (Kubernetes plugin), or cloud spot nodes.
    - Isolate untrusted builds; keep secrets off shared workspaces.
    - Scale executors carefully — disk and Docker sock sharing are risks.
    
    **Trap**
    
    - Building untrusted PRs on the controller itself.

**11. What are the steps to secure Jenkins?**

??? success "Reveal answer"
    **In short:** Lock down authn/authz, harden the controller, and treat plugins as attack surface.
    
    **Key points**
    
    - Disable signup; use SSO/LDAP; matrix or role-based authz.
    - CSRF protection on; reverse proxy TLS; no anonymous Admin.
    - Credentials plugin + least privilege; audit who can run on which agents.
    - Keep Jenkins and plugins patched; restrict Groovy script approvals.
    
    **Trap**
    
    - Running the controller as root with Docker socket mounted “for convenience”.

**12. What are the different ways to trigger a build in Jenkins?**

??? success "Reveal answer"
    **In short:** SCM webhooks, polling, cron, upstream/downstream, remote API, and manual starts.
    
    **Key points**
    
    - Webhooks are the modern default for Git events.
    - Timers for nightly/regression; avoid for every commit.
    - Upstream triggers for fan-out after a platform build.
    - `Generic Webhook Trigger` for chatops/custom events.
    
    **Trap**
    
    - Chaining 10 freestyle “Trigger other projects” without a clear DAG — debug hell.

**13. What is the difference between a freestyle project and a pipeline project in Jenkins?**

??? success "Reveal answer"
    **In short:** Freestyle is UI-configured; Pipeline is code in a Jenkinsfile you can review.
    
    **Key points**
    
    - Freestyle: easy start, poor reuse, hard PR review.
    - Pipeline: Declarative/Scripted, SCM-versioned, shared libraries.
    - Multibranch Pipeline maps branches/PRs automatically.
    - Prefer Pipeline for anything beyond a toy job.
    
    **Trap**
    
    - Exporting freestyle as XML and calling it “as code”.

## Scenarios and troubleshooting

**14. How can you handle failed builds in Jenkins?**

??? success "Reveal answer"
    **In short:** Fail fast, notify, keep artefacts/logs, and decide retry vs rollback vs fix-forward.
    
    **Key points**
    
    - `post { failure { ... } }` for Slack/email and artefact archival.
    - Mark flaky known tests carefully — don’t hide real regressions.
    - Auto-retry only infra flakes with a cap; never infinite loops.
    - For deploy failures, run the rollback stage using previous digest.
    
    **Trap**
    
    - “Build Now” spam without reading the first failure stack trace.

**15. If a Jenkins job starts but gets stuck, how do you debug?**

??? success "Reveal answer"
    **In short:** A stuck job usually means a hung step, exhausted executor, or waiting on `input`/lock.
    
    **Key points**
    
    - Check Blue Ocean/console for the last line and thread dump.
    - Look for `input`, milestone, or lock steps waiting for humans.
    - Inspect agent connectivity and disk full on the node.
    - Abort, capture thread dump, then fix root cause (hanging test/network).
    
    **Try this**
    
    - Manage Jenkins → script console thread dump
    - Agent log + `ps`/`docker ps` on node
    
    **Trap**
    
    - Deleting the job mid-hang and losing the only evidence.

**16. Your CI/CD pipeline has failed in jenkins. How do you investigate?**

??? success "Reveal answer"
    **In short:** Start from the failed stage console, then walk SCM SHA, agent, and external services.
    
    **Key points**
    
    - Identify which stage failed and whether tests, scans, or deploy broke.
    - Confirm commit SHA and whether the agent label/environment changed.
    - Check credentials, registry, Sonar, and cluster API health.
    - Reproduce locally or on the same agent image when possible.
    
    **Trap**
    
    - Blaming “Jenkins is flaky” before checking the application test that actually failed.

**17. Jenkins – If the controller (master) node goes down, how will you troubleshoot and restore it?**

??? success "Reveal answer"
    **In short:** Restore the controller from backup (JENKINS_HOME), then verify agents and queue.
    
    **Key points**
    
    - Symptoms: UI down, jobs not scheduling; agents show offline.
    - Restore `$JENKINS_HOME` (jobs, credentials IDs, config.xml) from last good backup.
    - Bring controller up, reconnect agents, drain stuck queue carefully.
    - HA/cloud native: run controller with persistent volume and tested restore drills.
    
    **Trap**
    
    - Restoring an old backup without the credentials key — secrets become unreadable.

**18. How would you implement dynamic stages in a Jenkinsfile based on environment variables?**

??? success "Reveal answer"
    **In short:** Build the stage list in Groovy from env vars, then render Declarative stages dynamically.
    
    **Key points**
    
    - Use a Scripted block or `when { expression { ... } }` per optional stage.
    - Or generate stages from `params.ENV.split(',')` in a loop (Scripted).
    - Keep dynamic graphs readable — log which stages were selected.
    - Prefer declarative `when` for simple env toggles.
    
    **Try this**
    
    - `when { expression { return env.RUN_SCAN == 'true' } }`
    
    **Trap**
    
    - Hiding required security stages behind an env flag anyone can set to false.

**19. How can you monitor Jenkins logs and troubleshoot issues?**

??? success "Reveal answer"
    **In short:** Controller logs, agent logs, and pipeline consoles — correlate with system metrics.
    
    **Key points**
    
    - `/var/log/jenkins` or container logs for controller exceptions.
    - Support Bundle / System Log for plugin and Queue issues.
    - Ship logs to ELK/Loki; alert on queue length and executor starvation.
    - For a job: console output + node temporary directories.
    
    **Trap**
    
    - Only watching the UI while the controller disk is full and silent.

**20. How would trigger pipeline B in jenkins automatically after pipeline B?**

??? success "Reveal answer"
    **In short:** Assuming you mean trigger B after A: use a downstream `build` step or a webhook between jobs.
    
    **Key points**
    
    - In A’s success `post`: `build job: 'pipeline-B', wait: false, propagate: false`.
    - Pass the artefact version via parameters.
    - Or have A publish an event B consumes (better at scale).
    - Avoid circular A↔B triggers.
    
    **Trap**
    
    - Hard-coding waits that serialize the whole platform on one flaky job.

**21. How do you mark a build as unstable vs failed in Jenkins?**

??? success "Reveal answer"
    **In short:** Failed means the build broke; Unstable means it completed with quality warnings (e.g. test thresholds).
    
    **Key points**
    
    - `error` / non-zero shell → FAILURE.
    - Test result publishers can mark UNSTABLE on regressions under a threshold.
    - `catchError(buildResult: 'UNSTABLE')` for soft gates you still want visible.
    - Treat UNSTABLE as non-releasable unless policy says otherwise.
    
    **Trap**
    
    - Promoting UNSTABLE builds to prod because “it mostly passed”.

## Practice questions

**22. How does GitLab CI/CD work, and how is it different from Jenkins?**

??? success "Reveal answer"
    **In short:** GitLab CI is YAML-native in the product; Jenkins is a separate automation server with plugins.
    
    **Key points**
    
    - GitLab: `.gitlab-ci.yml`, built-in MR pipelines, runners, environments.
    - Jenkins: Jenkinsfile + controller/agents; extreme plugin flexibility.
    - GitLab shines when Git + CI + security live together.
    - Jenkins shines for complex shared libraries and heterogeneous estates.
    
    **Trap**
    
    - Claiming one is “always better” — pick for org constraints, not fashion.

**23. What if I have 10 FE micro services and 10 BE micro services how do you design the cicd pipeline using jenkins?**

??? success "Reveal answer"
    **In short:** One Multibranch/template pipeline per service, plus a platform library and optional umbrella orchestrator.
    
    **Key points**
    
    - 20 services → 20 pipelines from the same shared library contract.
    - Build/test/scan/push per service on its repo changes only.
    - Optional release train job deploys a version set to an environment.
    - Contract tests and environment promotion boards prevent combo explosions.
    
    **Trap**
    
    - One mega-Jenkinsfile that builds all 20 services on every commit.

**24. If the Jenkins pipeline runs but the build doesn’t happen, what possible issues could be causing it?**

??? success "Reveal answer"
    **In short:** Pipeline “runs” but skips the real build when stages are skipped, agents mislabelled, or SCM empty.
    
    **Key points**
    
    - Check `when` conditions and branch filters skipped the build stage.
    - Wrong `agent` label → job waits or runs a no-op node.
    - Lightweight checkout / sparse checkout missing sources.
    - Caching or `changelog false` misconceptions — read the console.
    
    **Trap**
    
    - Assuming green means compiled — it might have skipped every compile step.

**25. What do you mean by workspace in Jenkins?**

??? success "Reveal answer"
    **In short:** The workspace is the job’s working directory on the agent where checkout and build run.
    
    **Key points**
    
    - Usually under the agent’s Jenkins home `workspace/<job>`.
    - `ws {}` / custom workspace can isolate parallel branches.
    - Clean workspaces (`cleanWs`) avoid stale artefacts between builds.
    - Don’t store secrets in the workspace; it is not a vault.
    
    **Trap**
    
    - Relying on leftover files from the previous build instead of a clean checkout.

**26. Filled — how do you manage this in Jenkins?**

??? success "Reveal answer"
    **In short:** Treat “filled” as resource pressure — disk/executors/queue full — and drain with capacity controls.
    
    **Key points**
    
    - Disk full: clean workspaces, old builds, Docker prune with policy.
    - Executors saturated: add agents or throttle heavy jobs.
    - Queue filled: reduce concurrent Multibranch builds; use `disableConcurrentBuilds`.
    - Alert before “full”; don’t discover it when releases stop.
    
    **Trap**
    
    - Blindly deleting `$JENKINS_HOME` to free space — you delete job history and config.

**27. How do you perform complete backup up of Jenkins including jobs/configurations/authentications?**

??? success "Reveal answer"
    **In short:** Back up all of `JENKINS_HOME` (jobs, config, plugins list, secrets key) on a tested schedule.
    
    **Key points**
    
    - Include `config.xml`, `jobs/`, `users/`, `secrets/`, `credentials.xml`, plugins.
    - ThinBackup/scm-sync help, but full volume snapshots are safest.
    - Store encrypted off-box; test restore on a spare controller.
    - Document plugin versions used at backup time.
    
    **Trap**
    
    - Backing up jobs XML but not `secrets/` — restore boots with useless credentials.

**28. How do you manage concurrent builds in Jenkins and ensure performance doesn’t degrade?**

??? success "Reveal answer"
    **In short:** Throttle concurrency, isolate heavy builds on labelled agents, and cache dependencies wisely.
    
    **Key points**
    
    - `disableConcurrentBuilds` or milestones for deploy jobs.
    - Label GPU/Docker-heavy agents separately from light lint jobs.
    - Reuse caches (Maven/npm) per agent without corrupting parallel builds.
    - Watch queue time and agent CPU/disk; autoscale Kubernetes agents.
    
    **Trap**
    
    - Unlimited Multibranch PR builds that DoS your own CI farm.

**29. How do you manage credentials in Jenkins?**

??? success "Reveal answer"
    **In short:** Store secrets in Credentials (or external vault) and bind them at runtime — never in Jenkinsfiles.
    
    **Key points**
    
    - Username/password, secret text, files, certificates, cloud creds.
    - `withCredentials([...]) { ... }` or Declarative `environment` bindings.
    - Folder/credential domains for least privilege per team.
    - Prefer OIDC/cloud IAM over long-lived static keys.
    
    **Try this**
    
    - `withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')])`
    
    **Trap**
    
    - Echoing credentials into console logs with `set -x` / Groovy printing.

**30. How do you copy the jobs from one jenkins worker node to another worker node?**

??? success "Reveal answer"
    **In short:** You don’t copy jobs between workers — jobs live on the controller; agents only execute workspaces.
    
    **Key points**
    
    - Job definitions are in controller `JENKINS_HOME/jobs`.
    - Move/migrate by exporting job config or using Job DSL/Casc.
    - To change where work runs, retarget `agent { label ... }`.
    - Workspace data on agents is disposable — rebuild from SCM.
    
    **Trap**
    
    - rsync’ing workspaces between agents and calling it a job migration.

**31. How do you call variables in a Jenkins pipeline?**

??? success "Reveal answer"
    **In short:** Use `env`, `params`, and `withEnv` — Groovy string interpolation in steps carefully.
    
    **Key points**
    
    - `env.MY_VAR` / `params.VERSION` in Declarative.
    - `environment { FOO = 'bar' }` block for stage/job scope.
    - Pass into shells as `"${env.FOO}"` with proper quoting.
    - Prefer credentials bindings for secrets, not plain env.
    
    **Trap**
    
    - Groovy double-quoted strings that expand secrets into logs.

**32. How do you deploy python application on aws using jenkins pipeline?**

??? success "Reveal answer"
    **In short:** CI builds and tests the Python app, pushes an artefact/image, then deploys to AWS with IAM-scoped creds.
    
    **Key points**
    
    - Stages: lint/test → build wheel/image → push to ECR → deploy ECS/EKS/Lambda.
    - Use OIDC or short-lived AWS creds — not long-lived keys in Jenkins.
    - Smoke-test the environment URL after deploy.
    - Keep infra (Terraform) separate from app deploy when possible.
    
    **Try this**
    
    - `aws ecr get-login-password`
    - kubectl/helm or ECS update-service
    
    **Trap**
    
    - Baking AWS access keys into the agent AMI.

**33. How do you store sensitive information like passwords in jenkins?**

??? success "Reveal answer"
    **In short:** Use the Credentials store (or Vault) and inject at runtime — never commit passwords.
    
    **Key points**
    
    - Secret text/file credentials with least-privilege IDs.
    - Masking in console; avoid printing env dumps.
    - Rotate regularly; prefer SSO tokens / OIDC.
    - Folder-scoped credentials so teams cannot read each other’s secrets.
    
    **Trap**
    
    - Base64 in a Jenkinsfile is not encryption.

**34. How will you secure your jenkins pipelines?**

??? success "Reveal answer"
    **In short:** Least privilege, trusted libraries, secret hygiene, and no untrusted code on privileged agents.
    
    **Key points**
    
    - Pin shared library versions; review library PRs like prod code.
    - Separate agents for untrusted PR builds.
    - Require signed commits/protected branches for deploy jobs.
    - Script Security / sandbox; disable dangerous plugin features.
    
    **Trap**
    
    - Allowing Multibranch PRs from forks to run with deploy credentials.

**35. How do you integrate Nexus Repository Manager with Jenkins?**

??? success "Reveal answer"
    **In short:** Point build tools at Nexus group URLs and publish releases with CI credentials.
    
    **Key points**
    
    - Maven `settings.xml` / npm registry URL / Docker login to Nexus hosted.
    - CI user with deploy privileges only to snapshot/release repos.
    - Publish after tests/gates; promote artefacts between repos if needed.
    - Fail the job if publish returns non-2xx.
    
    **Trap**
    
    - Using admin Nexus credentials in every Jenkins job.

**36. How do you configure SonarQube in Jenkins?**

??? success "Reveal answer"
    **In short:** Install the SonarQube scanner integration, configure server + token, and fail on gate.
    
    **Key points**
    
    - Manage Jenkins → SonarQube servers with server URL and token credential.
    - `withSonarQubeEnv` + scanner step after tests/coverage.
    - `waitForQualityGate` aborts on ERROR.
    - PR decoration needs proper branch/PR parameters.
    
    **Trap**
    
    - Running Sonar without `waitForQualityGate` — red findings still look green in Jenkins.

**37. How does Jenkins achieve Continuous Integration?**

??? success "Reveal answer"
    **In short:** Jenkins achieves CI by building and testing every change on a shared mainline automatically.
    
    **Key points**
    
    - Webhooks start pipelines on commit/PR.
    - Fast feedback: compile, unit tests, static checks.
    - Broken builds block merge/promotion culture.
    - Artefacts from CI feed CD stages.
    
    **Trap**
    
    - CI that only runs when someone remembers to click Build Now.

**38. Write your jenkins pipeline?**

??? success "Reveal answer"
    **In short:** A minimal Declarative Jenkinsfile: agent, stages for build/test, and post notifications.
    
    **Key points**
    
    - `pipeline { agent any; options { timestamps() }; stages { ... } }`.
    - Checkout SCM, run build/test, archive artefacts.
    - `post { always/success/failure }` for cleanup and alerts.
    - Real projects add tools, credentials, and deploy stages.
    
    **Try this**
    
    - `stage('Test') { steps { sh 'pytest -q' } }`
    - `post { failure { slackSend ... } }`
    
    **Trap**
    
    - Pasting a Scripted novel when interviewers asked for a clear Declarative skeleton.

**39. Write Jenkins script to trigger simultaneous/ parallel execution?**

??? success "Reveal answer"
    **In short:** Use a `parallel` block so independent stages run simultaneously on available executors.
    
    **Key points**
    
    - Declarative: `parallel { stage('A') { ... } stage('B') { ... } }`.
    - Fail-fast vs `failFast false` depending on need.
    - Ensure agents have enough executors/labels.
    - Merge results before deploy stage.
    
    **Try this**
    
    - `parallel {
      stage('Unit') { steps { sh 'make test' } }
      stage('Lint') { steps { sh 'make lint' } }
    }`
    
    **Trap**
    
    - Parallel deploy stages writing the same environment — race conditions.

**40. How does Jenkins handle parallel execution in pipelines?**

??? success "Reveal answer"
    **In short:** Jenkins parallel stages schedule multiple branches of the pipeline graph at once.
    
    **Key points**
    
    - `parallel` step fans out work; controller assigns agents.
    - Use for test matrix, multi-arch builds, or independent scans.
    - Stash/unstash or artefacts to share inputs/outputs.
    - Cap parallelism to protect the farm.
    
    **Trap**
    
    - Unbounded parallel matrix that exhausts every agent and stalls prod deploys.

**41. How can you use Python in Jenkins pipelines?**

??? success "Reveal answer"
    **In short:** Run Python on agents via `sh`/`bat`, virtualenv/poetry, or a Python-enabled container agent.
    
    **Key points**
    
    - Prefer container agents with pinned Python versions.
    - Create venv, install deps, run `pytest`/`ruff` in stages.
    - Use Python for custom glue scripts checked into the repo.
    - Publish coverage and junit for Jenkins test trend graphs.
    
    **Trap**
    
    - Relying on whatever system Python the agent happens to have.

**42. How do you parameterize a Jenkins job?**

??? success "Reveal answer"
    **In short:** Add parameters (`string`, `choice`, `booleanParam`) and read them as `params.*`.
    
    **Key points**
    
    - `parameters { choice(name: 'ENV', choices: ['dev','uat','prod']) }`.
    - Drive `when` conditions and deploy targets from params.
    - Multibranch can use properties step to define params per branch.
    - Validate params early — reject prod without approval.
    
    **Trap**
    
    - A free-text `ENV` param that accepts `prdution` typos into real clusters.

**43. What type of Jenkins job is best?**

??? success "Reveal answer"
    **In short:** Multibranch Pipeline (Jenkinsfile in SCM) is the best default for modern teams.
    
    **Key points**
    
    - Code-reviewed, branch/PR aware, reusable via libraries.
    - Freestyle only for legacy holdouts.
    - Org folders when you standardise many repos.
    - Pair with Configuration as Code for controller setup.
    
    **Trap**
    
    - “Best” meaning most plugins — prefer simplest reliable Pipeline design.

**44. Different plugins for ci/cd in jenkins using aws platform?**

??? success "Reveal answer"
    **In short:** Use AWS-focused plugins carefully — prefer AWS CLI/SDK with OIDC over sprawling plugin stacks.
    
    **Key points**
    
    - Common: Pipeline AWS Steps, EC2 fleet/cloud agents, ECR login helpers.
    - Kubernetes + EKS deploy via official kubectl/helm in containers.
    - Credentials: AWS Credentials / web identity federation.
    - Keep plugin count minimal; pin versions; patch often.
    
    **Trap**
    
    - Installing every AWS plugin “just in case” and never upgrading them.

## Related
- Course: [Jenkins](../jenkins/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
