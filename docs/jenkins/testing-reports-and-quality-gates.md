---
title: "Testing, Reports, and Quality Gates"
description: "Publish JUnit and HTML reports, run parallel stages, notify teams, and gate deploys on quality."
difficulty: intermediate
estimated_time: "45–60 min"
technology: jenkins
category: jenkins
module: "Module 12 · Testing and Quality Gates"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - jenkins
  - testing
  - quality-gates
prerequisites:
  - jenkins/securing-jenkins
next:
  - jenkins/kubernetes-agents-and-deploys
tags:
  - jenkins
  - junit
  - reports
  - parallel
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Testing, Reports, and Quality Gates

## Overview



Turn Pipelines into quality signals: **`junit`** test publishing, HTML reports, **parallel** stages, notifications, and **quality gates** before deploy.

A green compile is not enough — trends and gates keep Continuous Delivery honest.

This is a core tutorial in **Module 12 · Testing and Quality Gates** of the REBASH Academy **Jenkins for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites



- Completed prior modules in this track where linked in frontmatter
- [Git](../git/index.md) and [Docker](../docker/index.md) for lab workflows
- Running Jenkins LTS from [Installing Jenkins LTS](installing-jenkins-lts.md) when a live controller is required

## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Publish JUnit results from a Pipeline
- [ ] Outline HTML Publisher usage for reports
- [ ] Write parallel stages for independent test suites
- [ ] Define a quality gate that blocks deploy

## Architecture



This topic’s control points and relationships are shown below.

![Testing and quality gates](../assets/excalidraw/jenkins-testing.svg)

## Theory



### What it is

The **`junit`** step ingests XML test reports and paints trends on the job. **HTML Publisher** archives browsable reports (coverage, lint). **`parallel`** runs stages concurrently on available executors. Notifications (email, Slack, etc. via plugins) belong in `post`. A **quality gate** is policy: fail the build or skip deploy stages when tests/coverage/security scans fail.

### Why it matters

Without published tests, failures hide in console logs. Parallelism shortens feedback. Gates prevent “deploy anyway” culture. Platform teams standardise report steps in shared libraries.

### How it works

1. Run tests that emit JUnit XML.
2. Call `junit '**/surefire-reports/*.xml'` (or your path) in `post` or a stage.
3. Optionally publish HTML reports with the HTML Publisher plugin.
4. Split unit/integration tests with `parallel`.
5. Structure deploy stages with `when` / conditional logic so failed tests never deploy.

See Pipeline Steps for `junit` and related publishers.

### Key concepts and comparisons

| Signal | Mechanism |
|--------|-----------|
| Test trends | `junit` |
| Browseable report | HTML Publisher |
| Speed | `parallel` stages |
| Gate | fail build / skip deploy |

Keep test XML and HTML as build artefacts for incident review.

### Common pitfalls

- Ignoring skipped tests that hide broken suites.
- Parallel stages that share a writable workspace unsafely.
- Deploy stage not gated on previous stage result.
- Enormous HTML reports blowing artefact storage.

## Hands-on Lab



### Objective

Configure a real Jenkins-facing artefact for **Testing, Reports, and Quality Gates** (Compose controller and/or Jenkinsfile) you can run or import.

### Prerequisites

- Docker Engine for controller labs
- Text editor / shell

### Lab environment

Workspace: `~/rebash-jenkins/module-12`

Local Docker Compose Jenkins LTS where a live UI is needed; file-only Jenkinsfile labs otherwise.

```bash
mkdir -p ~/rebash-jenkins/module-12 && cd ~/rebash-jenkins/module-12
```

### Real-world scenario

Your organisation is standardising **Testing, Reports, and Quality Gates**. You prototype on a lab controller, keep everything as files, and avoid building on the built-in node in production designs.

### Step-by-step tasks

#### Task 1 – Capture controller/agent mental model files

Document how this topic shows up on a real controller.

```bash
tee scenario.md << 'EOF'
Topic: Testing, Reports, and Quality Gates
- Controller owns config and orchestration
- Agents execute untrusted build steps
- Prefer Jenkinsfile in SCM over click-ops jobs
EOF
cat scenario.md
mkdir -p jobs && echo 'pipelineJob stub' > jobs/README.txt
```

**Expected output:** scenario.md and jobs/README.txt exist.

#### Task 2 – Write a minimal Declarative stub

Even management topics should leave a Pipeline artefact.

```bash
cat > Jenkinsfile << 'EOF'
pipeline {
  agent any
  stages { stage('OK') { steps { echo 'lab' } } }
}
EOF
grep -n agent Jenkinsfile
```

**Expected output:** Jenkinsfile present with an agent directive.

### Validation steps

- [ ] Artefacts from tasks exist
- [ ] No secrets committed
- [ ] Compose stack stopped if started

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| port 8080 in use | Another Jenkins/lab | Change host port or stop the other container |
| permission denied on volume | Podman/rootless path | Fix volume ownership or use named volumes |
| agent any hangs | No executors | Attach an agent or enable a lab executor carefully |

### Challenge exercise

Disable builds on the built-in node in your notes and document the agent label you would require instead.

### Learning outcomes

- Produced runnable Jenkins artefacts
- Practised safe lab controller hygiene

### Cleanup

```bash
# Keep lab notes under ~/rebash-jenkins/
```

## Validation



- [ ] Lab commands run under `~/rebash-jenkins/module-12/`
- [ ] You can explain each Theory section in your own words
- [ ] You used current Jenkins LTS / Pipeline practices where they apply
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough



Production practice for **Testing, Reports, and Quality Gates** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, Jenkinsfile, JCasC)
3. Capture evidence (console logs, plan artefacts) for handovers
4. Prefer current LTS and supported plugins over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations



- Treat Jenkins credentials and cloud tokens as privileged — never commit them
- Keep builds off the built-in node; isolate untrusted pull requests
- Prefer short-lived auth (OIDC-style patterns, scoped RBAC) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Collect audit logs; limit who can administer the controller

## Common Mistakes



!!! warning "Deploy not gated on tests"
    Structure stages so deploy cannot run when `junit` fails the build.

!!! warning "Swallowing test XML paths"
    Wrong globs silently publish zero tests — check “no test results” warnings.

!!! warning "Unbounded parallel"
    Too much parallelism saturates agents; size against executors.

## Best Practices



- Encode **Testing, Reports, and Quality Gates** changes as code and review them in pull requests
- Prefer Jenkins LTS and pinned agent/tool versions
- Keep builds off the controller; use labelled agents
- Least privilege for credentials and cluster/cloud access
- Destroy or stop lab resources; keep `~/rebash-jenkins/` notes for the track

## Troubleshooting



| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Job stuck in queue | No matching agent/label or executors busy | Check nodes, labels, and executor counts |
| Checkout / SCM failure | Credentials, URL, or permissions | Verify credential ID and repository access |
| Pipeline CPS / script error | Syntax, sandbox, or library mismatch | Read error line; validate Jenkinsfile; pin library version |
| Plugin / UI broken after update | Incompatible plugin set | Restore backup; disable suspect plugin on test controller |
| Disk full on agent/controller | Workspaces or old builds | Clean workspaces; trim build retention |

## Summary



**Testing, Reports, and Quality Gates** is essential for Cloud and DevOps engineers operating Jenkins. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions



1. What does the `junit` step give you beyond console output?
2. How do you stop a deploy when tests fail in Declarative Pipeline?
3. When is `parallel` appropriate?
4. Why publish HTML reports as artefacts?
5. What is a quality gate in a CI/CD Pipeline?

!!! tip "Sample answer — question 1"
    It records pass/fail trends, flaky visibility, and fails the build on test failures according to options.

!!! tip "Sample answer — question 5"
    A policy checkpoint — tests, coverage, or scans must pass before promotion/deploy stages run.

## Related Tutorials



- [Course overview](index.md)
- [Securing Jenkins](securing-jenkins.md)
- [Kubernetes Agents and Deploys](kubernetes-agents-and-deploys.md)

## References



- [junit step](https://www.jenkins.io/doc/pipeline/steps/junit/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Pipeline chapter](https://www.jenkins.io/doc/book/pipeline/)
