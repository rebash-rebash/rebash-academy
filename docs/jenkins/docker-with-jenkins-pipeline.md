---
title: "Docker with Jenkins Pipeline"
description: "Run Pipeline stages in Docker agents, build images, and handle registry credentials safely."
difficulty: intermediate
estimated_time: "50–65 min"
technology: jenkins
category: jenkins
module: "Module 8 · Docker with Pipeline"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - jenkins
  - docker
  - pipeline
prerequisites:
  - jenkins/multibranch-pipelines-and-prs
next:
  - jenkins/shared-libraries
tags:
  - jenkins
  - docker
  - agents
  - registry
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Docker with Jenkins Pipeline

## Overview



Use Docker with Jenkins Pipeline: `agent { docker { image '…' } }`, Dockerfile agents, image build/push patterns, and registry credentials.

Understand **Docker-in-Docker (DinD)** versus a **sibling Docker socket** — both have security trade-offs. Prefer least privilege and pinned image digests where practical.

This is a core tutorial in **Module 8 · Docker with Pipeline** of the REBASH Academy **Jenkins for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites



- Completed prior modules in this track where linked in frontmatter
- [Git](../git/index.md) and [Docker](../docker/index.md) for lab workflows
- Running Jenkins LTS from [Installing Jenkins LTS](installing-jenkins-lts.md) when a live controller is required

## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Write a Pipeline that runs on a Docker agent image
- [ ] Contrast DinD vs sibling `docker.sock` mounting
- [ ] Outline build and push with credential IDs
- [ ] Pin base images for reproducibility

## Architecture



This topic’s control points and relationships are shown below.

![Docker with Jenkins Pipeline](../assets/excalidraw/jenkins-docker-pipeline.svg)

## Theory



### What it is

Declarative Pipeline can set `agent { docker { image 'python:3.12-alpine'; args '…' } }` so stages run inside a container on a Docker-capable Jenkins agent. `dockerfile true` builds an agent image from the repo’s Dockerfile. Separately, `docker build` / `docker push` (or Buildah/Kaniko patterns) produce release artefacts. Registry logins must use Credentials bindings, not plaintext passwords in the Jenkinsfile.

### Why it matters

Agent VMs drift; container agents make toolchains reproducible. Cloud and DevOps teams ship the same image they tested. Understanding socket vs DinD avoids cargo-cult Compose mounts that effectively root the agent host.

### How it works

1. Ensure the Jenkins agent has Docker CLI access to a daemon you accept risk for.
2. Use `agent { docker { image 'maven:3.9-eclipse-temurin-17' } }` for build tools.
3. For image publish stages, authenticate with `docker.withRegistry` or `withCredentials`.
4. Tag images with Git SHA; avoid mutable `latest` for production deploys.
5. Document whether you use socket mount or DinD and the threat model.

See Pipeline Docker docs linked from [Pipeline Syntax — agent](https://www.jenkins.io/doc/book/pipeline/syntax/#agent).

### Key concepts and comparisons

| Pattern | Notes |
|---------|-------|
| `agent { docker { … } }` | Tool container per stage/Pipeline |
| Dockerfile agent | Custom toolchain from repo |
| Sibling socket | Powerful; host Docker API exposure |
| DinD | Isolation-ish; privileged often required |

Never bake registry passwords into image layers.

### Common pitfalls

- Mounting `docker.sock` without understanding host takeover risk.
- Using `latest` tags for both agent and release images.
- Storing registry passwords in job env vars visible to every PR.
- Building as root in containers without need.

## Hands-on Lab



### Objective

Configure a real Jenkins-facing artefact for **Docker with Jenkins Pipeline** (Compose controller and/or Jenkinsfile) you can run or import.

### Prerequisites

- Docker Engine for controller labs
- Text editor / shell

### Lab environment

Workspace: `~/rebash-jenkins/module-08`

Local Docker Compose Jenkins LTS where a live UI is needed; file-only Jenkinsfile labs otherwise.

```bash
mkdir -p ~/rebash-jenkins/module-08 && cd ~/rebash-jenkins/module-08
```

### Real-world scenario

Your organisation is standardising **Docker with Jenkins Pipeline**. You prototype on a lab controller, keep everything as files, and avoid building on the built-in node in production designs.

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



- [ ] Lab commands run under `~/rebash-jenkins/module-08/`
- [ ] You can explain each Theory section in your own words
- [ ] You used current Jenkins LTS / Pipeline practices where they apply
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough



Production practice for **Docker with Jenkins Pipeline** always combines:

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



!!! warning "Unrestricted docker.sock mounts"
    A job can control the host Docker daemon — treat as privileged access.

!!! warning "Privileged DinD by default"
    Only enable when justified; prefer rootless or Kaniko-style builds where possible.

!!! warning "latest tags in production"
    Pin agent and release images to digests or immutable tags.

## Best Practices



- Encode **Docker with Jenkins Pipeline** changes as code and review them in pull requests
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



**Docker with Jenkins Pipeline** is essential for Cloud and DevOps engineers operating Jenkins. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions



1. How does `agent { docker { … } }` differ from building an image in a stage?
2. What is the main risk of mounting the host Docker socket?
3. How should registry credentials be supplied to Pipeline?
4. Why pin image tags or digests?
5. When might you choose Kaniko or Buildah over docker CLI?

!!! tip "Sample answer — question 2"
    Socket access is effectively host-level Docker control — any Pipeline can start privileged containers or mount host paths.

!!! tip "Sample answer — question 3"
    Use the Credentials store and binding steps; never commit registry passwords in the Jenkinsfile.

## Related Tutorials



- [Course overview](index.md)
- [Multibranch Pipelines and Pull Requests](multibranch-pipelines-and-prs.md)
- [Shared Libraries](shared-libraries.md)

## References



- [Pipeline Syntax — agent](https://www.jenkins.io/doc/book/pipeline/syntax/#agent)
- [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- [Pipeline Steps](https://www.jenkins.io/doc/pipeline/steps/)
