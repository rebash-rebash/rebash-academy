---
title: "Jenkinsfile in SCM"
description: "Store a Jenkinsfile in Git, configure Pipeline from SCM, and use parameters and environment cleanly."
difficulty: intermediate
estimated_time: "45–60 min"
technology: jenkins
category: jenkins
module: "Module 5 · Jenkinsfile in SCM"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - jenkins
  - jenkinsfile
  - git
prerequisites:
  - jenkins/pipeline-fundamentals-declarative
next:
  - jenkins/agents-nodes-and-executors
tags:
  - jenkins
  - scm
  - jenkinsfile
  - git
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Jenkinsfile in SCM

## Overview



Move from inline Pipeline scripts to a **Jenkinsfile** in source control management (SCM).

Pipeline-as-code means reviewers see delivery changes beside application changes. You will structure parameters and environment variables, check out from Git, and prepare for Multibranch later. Follow Pipeline best practices from the User Handbook.

This is a core tutorial in **Module 5 · Jenkinsfile in SCM** of the REBASH Academy **Jenkins for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites



- Completed prior modules in this track where linked in frontmatter
- [Git](../git/index.md) and [Docker](../docker/index.md) for lab workflows
- Running Jenkins LTS from [Installing Jenkins LTS](installing-jenkins-lts.md) when a live controller is required

## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Commit a `Jenkinsfile` and point a job at Pipeline script from SCM
- [ ] Use `parameters` and `environment` appropriately
- [ ] Explain lightweight checkout vs full workspace needs
- [ ] List Pipeline-as-code best practices for pull requests

## Architecture



This topic’s control points and relationships are shown below.

![Jenkinsfile in source control](../assets/excalidraw/jenkinsfile-scm.svg)

## Theory



### What it is

A **Jenkinsfile** is the text file (usually at the repository root) that defines the Pipeline. Jobs can load **Pipeline script from SCM** (Git plugin) instead of storing Groovy in the job config. **Parameters** (`string`, `booleanParam`, `choice`) gather input for `workflow_dispatch`-style manual runs. **Environment** blocks set variables for stages; credentials should still come from the Credentials store, not plaintext env defaults.

### Why it matters

Inline scripts drift between environments and bypass code review. SCM-backed Jenkinsfiles enable Multibranch, pull request builds, and shared ownership. Platform teams can require status checks on the Jenkinsfile the same way they do for application code.

### How it works

1. Place `Jenkinsfile` at the repo root (or a documented path).
2. Create a Pipeline job → Pipeline script from SCM → Git → credentials if private.
3. Set Script Path to `Jenkinsfile`.
4. Add `parameters` and `environment` as needed; avoid secrets in the file.
5. Push a change; confirm the job uses the new revision.

Handbook: [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/).

### Key concepts and comparisons

| Practice | Why |
|----------|-----|
| Root `Jenkinsfile` | Discoverable default for Multibranch |
| Parameters for manual toggles | Safer than editing job config |
| Credential IDs in SCM | Secret values stay in Jenkins store |
| Small stages | Faster feedback, clearer failures |

Multibranch readiness: same Jenkinsfile works across branches when you avoid hard-coded branch names and use `env.BRANCH_NAME` carefully.

### Common pitfalls

- Committing secrets or cloud keys in the Jenkinsfile.
- Different Script Paths per environment without documentation.
- Editing the job’s inline script after moving to SCM (two sources of truth).
- Heavy `checkout` duplication when SCM already provided the workspace.

## Hands-on Lab



### Objective

Configure a real Jenkins-facing artefact for **Jenkinsfile in SCM** (Compose controller and/or Jenkinsfile) you can run or import.

### Prerequisites

- Docker Engine for controller labs
- Text editor / shell

### Lab environment

Workspace: `~/rebash-jenkins/module-05`

Local Docker Compose Jenkins LTS where a live UI is needed; file-only Jenkinsfile labs otherwise.

```bash
mkdir -p ~/rebash-jenkins/module-05 && cd ~/rebash-jenkins/module-05
```

### Real-world scenario

Your organisation is standardising **Jenkinsfile in SCM**. You prototype on a lab controller, keep everything as files, and avoid building on the built-in node in production designs.

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



- [ ] Lab commands run under `~/rebash-jenkins/module-05/`
- [ ] You can explain each Theory section in your own words
- [ ] You used current Jenkins LTS / Pipeline practices where they apply
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough



Production practice for **Jenkinsfile in SCM** always combines:

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



!!! warning "Secrets in Jenkinsfile"
    Reference credential IDs; never commit tokens or kubeconfigs.

!!! warning "Two sources of truth"
    After moving to SCM, remove inline scripts from the job.

!!! warning "Hard-coded branches"
    Prefer Multibranch or parameters over editing jobs per branch.

## Best Practices



- Encode **Jenkinsfile in SCM** changes as code and review them in pull requests
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



**Jenkinsfile in SCM** is essential for Cloud and DevOps engineers operating Jenkins. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions



1. Why store the Jenkinsfile in SCM instead of the job config?
2. What is Script Path in a Pipeline from SCM job?
3. How should secrets be handled in a Jenkinsfile?
4. What are parameters useful for?
5. How does a root Jenkinsfile help Multibranch later?

!!! tip "Sample answer — question 1"
    SCM storage makes Pipeline changes reviewable, branchable, and recoverable — the same as application code.

!!! tip "Sample answer — question 3"
    Store secret material in the Jenkins Credentials store; bind with `withCredentials` or dedicated steps; commit only credential IDs.

## Related Tutorials



- [Course overview](index.md)
- [Pipeline Fundamentals (Declarative)](pipeline-fundamentals-declarative.md)
- [Agents, Nodes, and Executors](agents-nodes-and-executors.md)

## References



- [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
- [Pipeline best practices](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
