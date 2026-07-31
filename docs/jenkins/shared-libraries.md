---
title: "Shared Libraries"
description: "Build global and folder shared libraries with vars/ and src/, versioning, and trust boundaries."
difficulty: intermediate
estimated_time: "45–60 min"
technology: jenkins
category: jenkins
module: "Module 9 · Shared Libraries"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - jenkins
  - shared-libraries
  - pipeline
prerequisites:
  - jenkins/docker-with-jenkins-pipeline
next:
  - jenkins/managing-jenkins-plugins-tools-and-cli
tags:
  - jenkins
  - shared-library
  - vars
  - governance
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---

# Shared Libraries

## Overview

Create reusable Pipeline logic with **shared libraries**: global or folder-scoped, `vars/` for global variables/steps, `src/` for class-based helpers, and explicit versioning with `@Library('name@version')`.

Trust and sandbox settings matter — a library can become a supply-chain path into every job.

This is a core tutorial in **Module 9 · Shared Libraries** of the REBASH Academy **Jenkins for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- Completed prior modules in this track where linked in frontmatter
- [Git](../git/index.md) and [Docker](../docker/index.md) for lab workflows
- Running Jenkins LTS from [Installing Jenkins LTS](installing-jenkins-lts.md) when a live controller is required

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Sketch a shared library repo layout (`vars/`, `src/`, `resources/`)
- [ ] Load a library at a pinned version from a Jenkinsfile
- [ ] Contrast global vs folder libraries
- [ ] Explain trust/sandbox implications

## Architecture

This topic’s control points and relationships are shown below.

![Jenkins shared libraries](../assets/excalidraw/jenkins-shared-library.svg)

## Theory

### What it is

A **shared library** is a Git repository retrieved by Jenkins and made available to Pipelines. **`vars/foo.groovy`** defines a global step `foo()` for Declarative/Scripted callers. **`src/org/…`** holds Groovy classes. **`resources/`** stores non-Groovy files. Libraries are configured under Manage Jenkins → System (global) or at folder level. Versions use tags/branches; pin tags in production.

### Why it matters

Without libraries, every Jenkinsfile reinvents checkout, deploy, and notify steps. Libraries encode platform standards. Version pins prevent a broken main branch from failing every product Pipeline overnight.

### How it works

1. Create a library repo with `vars/sayHello.groovy`.
2. Register it in Jenkins (global or folder) with a default version.
3. In a Jenkinsfile: `@Library('my-lib@1.0.0') _` then call `sayHello('rebash')`.
4. Prefer tags over floating `main` for production callers.
5. Restrict who can change trusted libraries.

Tutorial: [Extending with Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/).

### Key concepts and comparisons

| Path | Purpose |
|------|---------|
| `vars/` | Global steps for Jenkinsfiles |
| `src/` | Classes / complex logic |
| `resources/` | Templates, scripts loaded by library |

| Scope | Use |
|-------|-----|
| Global | Company-wide platform steps |
| Folder | Product-line customisations |
| Untrusted | Dynamic library load — careful |

### Common pitfalls

- Floating `@Library('lib')` on `main` without pins.
- Putting secrets inside library resources.
- Over-centralising so product teams cannot ship.
- Granting untrusted Multibranch jobs ability to load arbitrary libraries.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-jenkins/module-09 && cd ~/rebash-jenkins/module-09
```

**Focus:** scaffold a shared library vars/ step and a consuming Jenkinsfile

### Step 1 – Primary exercise

```bash
mkdir -p library/vars app
cat > library/vars/sayHello.groovy << 'EOF'
def call(String name = 'world') {
  echo "Hello, ${name}."
}
EOF
cat > app/Jenkinsfile << 'EOF'
@Library('rebash-lib@main') _
pipeline {
  agent any
  stages {
    stage('Greet') {
      steps {
        script { sayHello('rebash') }
      }
    }
  }
}
EOF
cat > library-notes.md << 'EOF'
# Register in Jenkins
- Name: rebash-lib
- Default version: main (pin tags in prod)
- Modern SCM: Git repo URL to library/
EOF
find library app -type f | sort
grep Library app/Jenkinsfile
```

### Step 2 – Sanity-check vars script

```bash
grep -E 'call|echo' library/vars/sayHello.groovy
```

### Final cleanup

```bash
# Keep ~/rebash-jenkins/ for later tutorials; stop Compose only if you are done with the controller
# docker compose -f ~/rebash-jenkins/module-02/docker-compose.yml down   # optional; omit -v to keep JENKINS_HOME
```

## Validation

- [ ] Lab commands run under `~/rebash-jenkins/module-09/`
- [ ] You can explain each Theory section in your own words
- [ ] You used current Jenkins LTS / Pipeline practices where they apply
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Shared Libraries** always combines:

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

!!! warning "Unpinned library versions"
    Pin tags/SHAs for production Pipelines so library main cannot break everyone.

!!! warning "Secrets in library resources"
    Libraries are cloned widely — keep secrets in Credentials.

!!! warning "Untrusted dynamic libraries"
    Limit who can resolve arbitrary library sources from Multibranch PRs.

## Best Practices

- Encode **Shared Libraries** changes as code and review them in pull requests
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

**Shared Libraries** is essential for Cloud and DevOps engineers operating Jenkins. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. What belongs in `vars/` versus `src/`?
2. How do you pin a shared library version?
3. Global versus folder library — when each?
4. Why is a shared library a trust boundary?
5. How do you test a library change safely?

!!! tip "Sample answer — question 2"
    Use `@Library('name@1.4.0') _` (tag) or a commit hash; avoid relying on mutable defaults for prod.

!!! tip "Sample answer — question 4"
    Library code runs inside Pipelines that may have credentials — treat library Git write access like prod code ownership.

## Related Tutorials

- [Course overview](index.md)
- [Docker with Jenkins Pipeline](docker-with-jenkins-pipeline.md)
- [Managing Jenkins — Plugins, Tools, and CLI](managing-jenkins-plugins-tools-and-cli.md)

## References

- [Extending with Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
- [Pipeline best practices](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
