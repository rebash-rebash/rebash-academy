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

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-jenkins/module-12 && cd ~/rebash-jenkins/module-12
```

**Focus:** generate JUnit XML and a Pipeline that publishes and gates

### Step 1 – Primary exercise

```bash
mkdir -p reports
cat > reports/TEST-sample.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="sample" tests="2" failures="0" errors="0" skipped="0">
  <testcase classname="demo.A" name="ok"/>
  <testcase classname="demo.B" name="also_ok"/>
</testsuite>
EOF
cat > Jenkinsfile << 'EOF'
pipeline {
  agent any
  stages {
    stage('Unit') {
      steps {
        sh 'mkdir -p reports && cp reports/TEST-sample.xml reports/ 2>/dev/null || true'
        sh 'test -f reports/TEST-sample.xml'
      }
    }
    stage('Quality gate') {
      steps {
        junit 'reports/TEST-*.xml'
      }
    }
    stage('Deploy') {
      when { expression { currentBuild.currentResult == 'SUCCESS' } }
      steps { echo 'Deploy would run only if tests passed' }
    }
  }
}
EOF
# Local proof without controller junit step:
xmllint --noout reports/TEST-sample.xml 2>/dev/null || python3 -c "import xml.etree.ElementTree as E; E.parse('reports/TEST-sample.xml'); print('junit-xml-ok')"
grep -E 'junit|Quality gate|Deploy' Jenkinsfile
```

### Step 2 – Parallel sketch

```bash
cat > parallel-snippet.txt << 'EOF'
parallel unit: { stage('Unit') { steps { sh 'echo unit' } } },
         lint: { stage('Lint') { steps { sh 'echo lint' } } }
EOF
grep parallel parallel-snippet.txt
```

### Final cleanup

```bash
# Keep ~/rebash-jenkins/ for later tutorials; stop Compose only if you are done with the controller
# docker compose -f ~/rebash-jenkins/module-02/docker-compose.yml down   # optional; omit -v to keep JENKINS_HOME
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
