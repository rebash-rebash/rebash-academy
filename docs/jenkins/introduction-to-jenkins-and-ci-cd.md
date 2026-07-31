---
title: "Introduction to Jenkins and CI/CD"
description: "Learn Continuous Integration (CI) and Continuous Delivery (CD), Jenkins LTS architecture, controllers and agents, and the Guided Tour mental model."
difficulty: beginner
estimated_time: "40–55 min"
technology: jenkins
category: jenkins
module: "Module 1 · Introduction to Jenkins and CI/CD"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - jenkins
  - cicd
  - pipelines
prerequisites:
  - git/index
  - docker/index
next:
  - jenkins/installing-jenkins-lts
tags:
  - jenkins
  - cicd
  - lts
  - controllers
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---

# Introduction to Jenkins and CI/CD

## Overview

Explain what Continuous Integration (CI) and Continuous Delivery (CD) solve, place Jenkins Long-Term Support (LTS) in that model, and describe the controller–agent architecture.

**Continuous Integration (CI)** builds and tests every meaningful change in Git so defects surface in minutes, not at release time. **Continuous Delivery (CD)** keeps every successful build ready to ship with human or automated gates. **Jenkins** is a self-managed automation server that runs those pipelines as jobs, with a **controller** that schedules work and **agents** that execute it.

This course is **Jenkins for Cloud & DevOps Engineers** — production platforms aligned with the [Jenkins User Documentation](https://www.jenkins.io/doc/), not click-ops demos. Blue Ocean appears only as legacy UI; Declarative Pipeline is the learning path.

This is a core tutorial in **Module 1 · Introduction to Jenkins and CI/CD** of the REBASH Academy **Jenkins for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- Completed prior modules in this track where linked in frontmatter
- [Git](../git/index.md) and [Docker](../docker/index.md) for lab workflows
- Running Jenkins LTS from [Installing Jenkins LTS](installing-jenkins-lts.md) when a live controller is required

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Define CI, Continuous Delivery, and how Jenkins implements them
- [ ] Sketch controller, agents, executors, and `JENKINS_HOME`
- [ ] Contrast Jenkins LTS with weekly releases
- [ ] Name when a self-managed controller is a better fit than SaaS CI

## Architecture

This topic’s control points and relationships are shown below.

![Jenkins architecture](../assets/excalidraw/jenkins-architecture.svg)

## Theory

### What it is

**CI** means every push or merge request runs a known script: checkout, build, test, and report status. The goal is a shared automated truth about branch health.

**Continuous Delivery** means the pipeline also produces a releasable artefact and can deploy, with a person or policy deciding *when*. Teams often mix delivery for production with automatic promotion for lower environments.

**Jenkins** is an open-source automation server. A **controller** holds configuration, plugins, credentials metadata, and the job catalogue under **`JENKINS_HOME`**. **Agents** (nodes) provide executors and workspaces where builds actually run. **Plugins** extend SCM, Pipeline, credentials, cloud agents, and reporting. Prefer **Jenkins LTS** for production; weekly releases are for earlier access to features with higher churn.

### Why it matters

SaaS CI is excellent when your source of truth and identity already live there. Many enterprises still need Jenkins because pipelines must reach private networks, custom toolchains, regulated environments, or multi-SCM estates. Platform and Site Reliability Engineering (SRE) teams treat the controller as a product: versioned configuration, agent isolation, and upgrade runbooks. Understanding CI/CD vocabulary first prevents treating Jenkins as “a UI that builds” instead of a scheduled, auditable delivery system.

### How it works

Mental model: **SCM event or schedule → controller selects a job → executor on an agent runs steps → status, artefacts, and logs return to Jenkins**.

1. Source changes land in Git (or another SCM).
2. A trigger (webhook, poll SCM, timer, or manual) starts a build.
3. The controller assigns an executor matching the job’s agent label or Pipeline `agent` directive.
4. The agent checks out code, runs stages/steps, and streams console output.
5. Post actions publish tests, archives, or notifications; build history stays on the controller.

The [Guided Tour](https://www.jenkins.io/doc/pipeline/tour/getting-started/) mental model matches this loop for Pipeline jobs.

### Key concepts and comparisons

| Term | Meaning |
|------|---------|
| Controller | Schedules jobs; stores config and history |
| Agent / node | Machine or container that runs builds |
| Executor | Slot on a node that can run one build |
| LTS | Long-Term Support line for production |
| Plugin | Extension that adds capabilities |

| Without CI/CD | With Jenkins Pipeline |
|---------------|------------------------|
| “Works on my machine” | Same agent image or label every run |
| Unreviewed production changes | Jenkinsfile in the pull request |
| Rebuild from memory after outage | Replay or rebuild from a known SHA |

**Jenkins vs GitHub Actions vs GitLab CI (brief):** Jenkins is self-managed and flexible; you operate the control plane. Actions and GitLab CI pair tightly with their forges. Pick based on where source, identity, and network boundaries already live.

### Common pitfalls

- CI is not “the controller” — the controller schedules; agents execute.
- A green build is not a production release unless you designed deploy stages and approvals that way.
- Building on the built-in node couples untrusted code to the control plane.
- Weekly Jenkins without a test controller is how plugin upgrades become outages.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-jenkins/module-01 && cd ~/rebash-jenkins/module-01
```

**Focus:** document CI/CD terms and sketch a controller–agent layout

### Step 1 – Primary exercise

```bash
cat > cicd-notes.md << 'EOF'
# Jenkins CI/CD notes
- CI: build and test every meaningful change
- CD: always releasable; gates decide when to ship
- Controller: schedules, stores JENKINS_HOME
- Agents: execute builds; prefer labels over built-in node
- LTS: production line; pin image tags in Compose
EOF
test -f cicd-notes.md && wc -l cicd-notes.md
```

### Step 2 – Validate your mental model checklist

```bash
grep -E 'Controller|Agents|LTS|CI:' cicd-notes.md
printf '%s\n' "controller=schedule" "agent=execute" "lts=production" > model.txt
cat model.txt
```

### Final cleanup

```bash
# Keep ~/rebash-jenkins/ for later tutorials; stop Compose only if you are done with the controller
# docker compose -f ~/rebash-jenkins/module-02/docker-compose.yml down   # optional; omit -v to keep JENKINS_HOME
```

## Validation

- [ ] Lab commands run under `~/rebash-jenkins/module-01/`
- [ ] You can explain each Theory section in your own words
- [ ] You used current Jenkins LTS / Pipeline practices where they apply
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Introduction to Jenkins and CI/CD** always combines:

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

!!! warning "Building on the built-in node"
    Untrusted Pipeline steps can reach controller credentials and filesystem. Use agents with labels from the start.

!!! warning "Treating LTS and weekly as interchangeable"
    Pin an LTS image or package channel; upgrade controllers in a test environment first.

!!! warning "Confusing CI green with production release"
    Delivery needs explicit deploy stages, credentials scoping, and approval policy.

## Best Practices

- Encode **Introduction to Jenkins and CI/CD** changes as code and review them in pull requests
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

**Introduction to Jenkins and CI/CD** is essential for Cloud and DevOps engineers operating Jenkins. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. What is the difference between Continuous Integration and Continuous Delivery?
2. What does the Jenkins controller store, and what should agents do instead?
3. Why prefer Jenkins LTS over weekly releases in production?
4. When would you choose Jenkins over a SaaS CI product?
5. What is an executor, and how does it relate to a node?

!!! tip "Sample answer — question 2"
    The controller holds `JENKINS_HOME` (jobs, plugins, credentials metadata, build history). Agents provide workspaces and toolchains so build code does not run on the control plane.

!!! tip "Sample answer — question 3"
    LTS is the supported production line with fewer breaking plugin churn cycles. Weeklies are for earlier features; validate them on a non-production controller.

## Related Tutorials

- [Course overview](index.md)
- [Installing Jenkins LTS](installing-jenkins-lts.md)

## References

- [Jenkins User Documentation](https://www.jenkins.io/doc/)
- [Pipeline Getting Started](https://www.jenkins.io/doc/pipeline/tour/getting-started/)
- [Jenkins LTS](https://www.jenkins.io/download/lts/)
