---
title: "Terraform Pipelines in Jenkins"
description: "Run Terraform init, validate, plan, and apply from Jenkins with remote state awareness and approvals."
difficulty: advanced
estimated_time: "50–65 min"
technology: jenkins
category: jenkins
module: "Module 14 · Terraform Pipelines"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - jenkins
  - terraform
  - iac
prerequisites:
  - jenkins/kubernetes-agents-and-deploys
next:
  - jenkins/jcasc-scaling-and-operations
tags:
  - jenkins
  - terraform
  - plan
  - oidc
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Terraform Pipelines in Jenkins

## Overview



Automate Infrastructure as Code (IaC) with Terraform in Jenkins: **init**, **validate**, **plan**, **apply**, remote state, credentials or OpenID Connect (OIDC)-style cloud auth patterns, plan artefacts, and destroy discipline for labs.

Never apply unreviewed plans to production.

This is a core tutorial in **Module 14 · Terraform Pipelines** of the REBASH Academy **Jenkins for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites



- Completed prior modules in this track where linked in frontmatter
- [Git](../git/index.md) and [Docker](../docker/index.md) for lab workflows
- Running Jenkins LTS from [Installing Jenkins LTS](installing-jenkins-lts.md) when a live controller is required

## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Structure a Declarative Pipeline for Terraform stages
- [ ] Archive plan artefacts and require approval before apply
- [ ] Explain remote state and locking awareness
- [ ] Outline safer cloud credential patterns (including OIDC-style)

## Architecture



This topic’s control points and relationships are shown below.

![Terraform Pipelines in Jenkins](../assets/excalidraw/jenkins-terraform-pipeline.svg)

## Theory



### What it is

Terraform Pipelines typically: checkout → `terraform init` (remote backend) → `fmt`/`validate` → `plan -out=tfplan` → archive plan → human approval → `apply tfplan`. State belongs in a remote backend with locking. Cloud credentials should be short-lived where possible (OIDC to AWS/Azure/GCP analogues) rather than long-lived keys in Jenkins.

### Why it matters

Click-ops Terraform on laptops drifts from peer review. Jenkins makes plan/apply auditable. Bad apply without approval is a leading cause of costly incidents.

### How it works

1. Use an agent image with a pinned Terraform version.
2. Authenticate to cloud/state backend via credentials or OIDC plugins/patterns.
3. Split plan and apply into stages; use `input` for approval on production.
4. Archive `tfplan` and logs as artefacts.
5. Lab destroy only with explicit parameter and guardrails.

Align with Terraform track practices and jenkins.io Pipeline steps for `sh` wrappers.

### Key concepts and comparisons

| Stage | Gate |
|-------|------|
| validate | fail on invalid config |
| plan | review artefact |
| apply | approval + same plan file |
| destroy | lab-only parameter |

Remote state + locking prevents two applies clobbering each other.

### Common pitfalls

- `apply` without storing the exact plan file.
- Long-lived access keys in Multibranch PR jobs.
- Destroy from `main` without protections.
- Different Terraform versions, between plan and apply agents.

## Hands-on Lab



### Objective

Configure a real Jenkins-facing artefact for **Terraform Pipelines in Jenkins** (Compose controller and/or Jenkinsfile) you can run or import.

### Prerequisites

- Docker Engine for controller labs
- Text editor / shell

### Lab environment

Workspace: `~/rebash-jenkins/module-14`

Local Docker Compose Jenkins LTS where a live UI is needed; file-only Jenkinsfile labs otherwise.

```bash
mkdir -p ~/rebash-jenkins/module-14 && cd ~/rebash-jenkins/module-14
```

### Real-world scenario

Your organisation is standardising **Terraform Pipelines in Jenkins**. You prototype on a lab controller, keep everything as files, and avoid building on the built-in node in production designs.

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



- [ ] Lab commands run under `~/rebash-jenkins/module-14/`
- [ ] You can explain each Theory section in your own words
- [ ] You used current Jenkins LTS / Pipeline practices where they apply
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough



Production practice for **Terraform Pipelines in Jenkins** always combines:

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



!!! warning "Apply without the saved plan"
    Always `apply` the exact `tfplan` artefact you reviewed.

!!! warning "Long-lived cloud keys on PR builds"
    Prefer OIDC/short-lived creds; deny apply from forks.

!!! warning "Unattended destroy"
    Require human confirmation and environment protection.

## Best Practices



- Encode **Terraform Pipelines in Jenkins** changes as code and review them in pull requests
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



**Terraform Pipelines in Jenkins** is essential for Cloud and DevOps engineers operating Jenkins. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions



1. Why separate plan and apply stages?
2. What belongs in remote state configuration?
3. How do you prevent two applies at once?
4. How should cloud credentials be provided to Jenkins?
5. What is dangerous about auto-apply on every PR?

!!! tip "Sample answer — question 1"
    So humans (or policy) review the plan artefact before mutating infrastructure; apply uses the same binary plan.

!!! tip "Sample answer — question 3"
    Remote state locking (for example S3+DynamoDB, Terraform Cloud, or equivalent) serialises applies.

## Related Tutorials



- [Course overview](index.md)
- [Kubernetes Agents and Deploys](kubernetes-agents-and-deploys.md)
- [JCasC, Scaling, and Operations](jcasc-scaling-and-operations.md)

## References



- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Pipeline best practices](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)
- [Jenkins User Documentation](https://www.jenkins.io/doc/)
