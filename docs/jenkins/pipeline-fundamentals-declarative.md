---
title: "Pipeline Fundamentals (Declarative)"
description: "Author Declarative Pipelines with agent, stages, steps, and post; contrast Declarative vs Scripted."
difficulty: intermediate
estimated_time: "45–60 min"
technology: jenkins
category: jenkins
module: "Module 4 · Pipeline Fundamentals"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - jenkins
  - pipeline
  - declarative
prerequisites:
  - jenkins/using-jenkins-jobs-views-and-folders
next:
  - jenkins/jenkinsfile-in-scm
tags:
  - jenkins
  - pipeline
  - declarative
  - jenkinsfile
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Pipeline Fundamentals (Declarative)

## Overview



Master **Declarative Pipeline** — the structured `pipeline { }` syntax recommended for most teams.

A Pipeline is a user-defined automation: **agent** chooses where it runs, **stages** group work, **steps** do the work, and **post** handles success, failure, and cleanup. Pipeline-as-code makes delivery reviewable in Git. Scripted Pipeline (`node { }`) remains powerful but is not the default learning path.

This is a core tutorial in **Module 4 · Pipeline Fundamentals** of the REBASH Academy **Jenkins for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites



- Completed prior modules in this track where linked in frontmatter
- [Git](../git/index.md) and [Docker](../docker/index.md) for lab workflows
- Running Jenkins LTS from [Installing Jenkins LTS](installing-jenkins-lts.md) when a live controller is required

## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Write a Declarative Pipeline with `agent`, `stages`, `steps`, and `post`
- [ ] Explain Pipeline, stage, step, and node concepts
- [ ] Contrast Declarative vs Scripted Pipeline
- [ ] Use Pipeline Syntax references when discovering steps

## Architecture



This topic’s control points and relationships are shown below.

![Declarative Pipeline lifecycle](../assets/excalidraw/jenkins-pipeline-lifecycle.svg)

## Theory



### What it is

**Pipeline** is both a job type and a Groovy Domain-Specific Language (DSL) executed by the Pipeline engine. **Declarative Pipeline** enforces a clear structure: `pipeline { agent …; stages { stage(…) { steps { … } } } post { … } }`. **Scripted Pipeline** uses imperative Groovy inside `node` blocks.

Core ideas from the handbook: a **node** (agent) allocates an executor and workspace; a **stage** is a logical phase shown in Blue Ocean historically and in stage views; a **step** is an individual task (`sh`, `echo`, `checkout`).

### Why it matters

Click-configured Freestyle jobs do not review cleanly in pull requests. Declarative Pipeline keeps the happy path readable for platform and product engineers while still allowing `script { }` escapes when needed. Consistent stages (Build, Test, Package) make failure signals obvious in the UI.

### How it works

1. Create a Pipeline job (or use “Pipeline script” in the job config).
2. Paste a minimal Declarative script with `agent any` (lab only) or a label.
3. Add stages with `sh` steps; add `post { always { cleanWs() } }` when the plugin allows.
4. Run the job; inspect stage view and console log.
5. Open **Pipeline Syntax** (snippet generator) from the job sidebar to discover step parameters.

See [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/).

### Key concepts and comparisons

| Directive | Role |
|-----------|------|
| `agent` | Where the Pipeline runs |
| `stages` / `stage` | Ordered phases |
| `steps` | Commands inside a stage |
| `post` | `always`, `success`, `failure`, etc. |
| `environment` | Env vars for the Pipeline |
| `options` | Timeouts, timestamps, durability |

| Declarative | Scripted |
|-------------|----------|
| Structured, validated | Imperative Groovy |
| Best default | Complex dynamic flows |
| `script { }` escape hatch | Full control inside `node` |

### Common pitfalls

- Using `agent any` on the controller in production.
- Huge Scripted blocks when Declarative would suffice.
- Ignoring `post` cleanup and filling disks with workspaces.
- Copying steps without checking [Pipeline Steps reference](https://www.jenkins.io/doc/pipeline/steps/).

## Hands-on Lab



### Objective

Configure a real Jenkins-facing artefact for **Pipeline Fundamentals (Declarative)** (Compose controller and/or Jenkinsfile) you can run or import.

### Prerequisites

- Docker Engine for controller labs
- Text editor / shell

### Lab environment

Workspace: `~/rebash-jenkins/module-04`

Local Docker Compose Jenkins LTS where a live UI is needed; file-only Jenkinsfile labs otherwise.

```bash
mkdir -p ~/rebash-jenkins/module-04 && cd ~/rebash-jenkins/module-04
```

### Real-world scenario

Your organisation is standardising **Pipeline Fundamentals (Declarative)**. You prototype on a lab controller, keep everything as files, and avoid building on the built-in node in production designs.

### Step-by-step tasks

#### Task 1 – Author a Declarative Jenkinsfile

Pipeline-as-code is the production default — Declarative first.

```bash
cat > Jenkinsfile << 'EOF'
pipeline {
  agent any
  options { timestamps() }
  stages {
    stage('Build') {
      steps {
        sh 'mkdir -p dist && echo ok > dist/status.txt'
      }
    }
    stage('Test') {
      steps {
        sh 'test -f dist/status.txt && grep -q ok dist/status.txt'
      }
    }
  }
  post {
    always { archiveArtifacts artifacts: 'dist/**', allowEmptyArchive: true }
  }
}
EOF
test -f Jenkinsfile && grep -n 'pipeline\|stages\|post' Jenkinsfile
```

**Expected output:** Jenkinsfile contains pipeline/stages/post blocks.

#### Task 2 – Validate structure locally

Run the shell steps the Pipeline will execute so failures are cheap.

```bash
mkdir -p dist && echo ok > dist/status.txt
test -f dist/status.txt && grep -q ok dist/status.txt
tar -cf evidence.tar Jenkinsfile dist
ls -l evidence.tar
```

**Expected output:** Shell checks pass; evidence.tar created for the job upload story.

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
rm -f evidence.tar
# Keep Jenkinsfile for SCM modules
```

## Validation



- [ ] Lab commands run under `~/rebash-jenkins/module-04/`
- [ ] You can explain each Theory section in your own words
- [ ] You used current Jenkins LTS / Pipeline practices where they apply
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough



Production practice for **Pipeline Fundamentals (Declarative)** always combines:

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



!!! warning "`agent any` on production controllers"
    Bind Pipelines to labelled agents so build code does not share the controller JVM host.

!!! warning "Skipping post cleanup"
    Workspaces and temp files accumulate; use `cleanWs` or agent ephemerality.

!!! warning "Scripted-first for new teams"
    Start Declarative; add Scripted only where structure blocks you.

## Best Practices



- Encode **Pipeline Fundamentals (Declarative)** changes as code and review them in pull requests
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



**Pipeline Fundamentals (Declarative)** is essential for Cloud and DevOps engineers operating Jenkins. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions



1. What are the required top-level sections of a Declarative Pipeline?
2. How does Declarative differ from Scripted Pipeline?
3. What is the purpose of the `post` block?
4. Why is Pipeline-as-code preferable to Freestyle for teams?
5. Where do you look up parameters for a Pipeline step?

!!! tip "Sample answer — question 1"
    At minimum: `pipeline { agent …; stages { … } }`. Most production files also use `options`, `environment`, and `post`.

!!! tip "Sample answer — question 5"
    Use the job’s Pipeline Syntax snippet generator and the online Pipeline Steps reference on jenkins.io.

## Related Tutorials



- [Course overview](index.md)
- [Using Jenkins — Jobs, Views, and Folders](using-jenkins-jobs-views-and-folders.md)
- [Jenkinsfile in SCM](jenkinsfile-in-scm.md)

## References



- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Pipeline Steps](https://www.jenkins.io/doc/pipeline/steps/)
- [Pipeline chapter](https://www.jenkins.io/doc/book/pipeline/)
