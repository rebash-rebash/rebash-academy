---
title: "Installing Jenkins LTS"
description: "Install Jenkins Long-Term Support (LTS) with Docker Compose, complete the setup wizard, and understand JENKINS_HOME."
difficulty: beginner
estimated_time: "45–60 min"
technology: jenkins
category: jenkins
module: "Module 2 · Installing Jenkins LTS"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - jenkins
  - docker
  - lts
prerequisites:
  - jenkins/introduction-to-jenkins-and-ci-cd
next:
  - jenkins/using-jenkins-jobs-views-and-folders
tags:
  - jenkins
  - install
  - docker-compose
  - lts
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Installing Jenkins LTS

## Overview



Install **Jenkins Long-Term Support (LTS)** for labs using Docker Compose, complete the initial setup wizard, and know what lives under **`JENKINS_HOME`**.

Package and WAR installs exist for bare metal and virtual machines; this course standardises on the official `jenkins/jenkins:lts` image so every learner shares the same controller baseline. You will create an admin user, set the Jenkins URL, and install the suggested plugin set once — then keep the volume for later modules.

This is a core tutorial in **Module 2 · Installing Jenkins LTS** of the REBASH Academy **Jenkins for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites



- Completed prior modules in this track where linked in frontmatter
- [Git](../git/index.md) and [Docker](../docker/index.md) for lab workflows
- Running Jenkins LTS from [Installing Jenkins LTS](installing-jenkins-lts.md) when a live controller is required

## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Bring up Jenkins LTS with Docker Compose and a persistent volume
- [ ] Complete the setup wizard (unlock, plugins, admin, URL)
- [ ] Locate and explain `JENKINS_HOME`
- [ ] Stop and restart the controller without losing configuration

## Architecture



This topic’s control points and relationships are shown below.

![Installing Jenkins LTS](../assets/excalidraw/jenkins-install.svg)

## Theory



### What it is

Jenkins publishes **LTS** and weekly lines. Production controllers should track LTS. The official Docker image `jenkins/jenkins:lts` runs the controller process; you map port `8080` (and optionally `50000` for inbound agents) and mount a volume at `/var/jenkins_home` — that directory is **`JENKINS_HOME`**.

First boot prints an **initialAdminPassword**. The setup wizard unlocks Jenkins, offers **Install suggested plugins**, creates the first admin user, and asks for the instance URL. Alternatives (Debian/RPM packages, generic WAR + Java) follow the same wizard concepts; Compose is the REBASH lab default.

### Why it matters

A disposable container without a volume teaches nothing about upgrades: all jobs vanish on recreate. Persisting `JENKINS_HOME` mirrors how platform teams backup, restore, and migrate controllers. Pinning the LTS tag (or digest) prevents surprise major jumps during a casual `docker compose pull`.

### How it works

1. Write a Compose file with image, ports, and volume.
2. Start the stack; read the unlock password from logs or the volume file.
3. Open `http://localhost:8080`, unlock, install suggested plugins, create admin.
4. Confirm Manage Jenkins → System Information shows a sensible home path.
5. `docker compose down` then `up -d` — configuration and jobs remain.

Official install guides cover packages and WAR; see [Installing Jenkins](https://www.jenkins.io/doc/book/installing/).

### Key concepts and comparisons

| Method | When to use |
|--------|-------------|
| Docker Compose LTS | Labs and many self-hosted starts |
| Package (deb/rpm) | Dedicated VMs with OS lifecycle |
| WAR + JDK | Custom servlet hosting (advanced) |

| Path / item | Role |
|-------------|------|
| `/var/jenkins_home` | `JENKINS_HOME` in the container |
| `secrets/initialAdminPassword` | First unlock only |
| Plugin Manager | Adds features after wizard |

### Common pitfalls

- Exposing `8080` on the public internet without TLS and auth hardening.
- Using `latest` instead of `lts` or a pinned LTS minor tag.
- Deleting the volume thinking “containers are ephemeral” — you delete the controller state.
- Skipping suggested plugins then wondering why Pipeline and Git are missing.

## Hands-on Lab



### Objective

Configure a real Jenkins-facing artefact for **Installing Jenkins LTS** (Compose controller and/or Jenkinsfile) you can run or import.

### Prerequisites

- Docker Engine for controller labs
- Text editor / shell

### Lab environment

Workspace: `~/rebash-jenkins/module-02`

Local Docker Compose Jenkins LTS where a live UI is needed; file-only Jenkinsfile labs otherwise.

```bash
mkdir -p ~/rebash-jenkins/module-02 && cd ~/rebash-jenkins/module-02
```

### Real-world scenario

Your organisation is standardising **Installing Jenkins LTS**. You prototype on a lab controller, keep everything as files, and avoid building on the built-in node in production designs.

### Step-by-step tasks

#### Task 1 – Start Jenkins LTS with Docker Compose

Controllers should be reproducible — Compose pins the LTS image.

```bash
cat > compose.yaml << 'EOF'
services:
  jenkins:
    image: jenkins/jenkins:lts-jdk17
    ports: ["8080:8080", "50000:50000"]
    volumes: ["jenkins_home:/var/jenkins_home"]
volumes:
  jenkins_home:
EOF
docker compose up -d
docker compose ps
docker compose logs --tail=30 jenkins | tee boot.log
```

**Expected output:** Service running; logs show Jenkins starting.

#### Task 2 – Read initial admin password from the container

The setup wizard requires the one-time password from JENKINS_HOME.

```bash
sleep 15
docker compose exec -T jenkins bash -lc 'test -f /var/jenkins_home/secrets/initialAdminPassword && cat /var/jenkins_home/secrets/initialAdminPassword' | tee initialAdminPassword.txt || \
  docker compose logs jenkins | tee boot2.log
ls -l initialAdminPassword.txt boot.log 2>/dev/null || true
```

**Expected output:** Password file present (or logs show Jenkins still warming up — retry once).

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
docker compose down -v
```

## Validation



- [ ] Lab commands run under `~/rebash-jenkins/module-02/`
- [ ] You can explain each Theory section in your own words
- [ ] You used current Jenkins LTS / Pipeline practices where they apply
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough



Production practice for **Installing Jenkins LTS** always combines:

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



!!! warning "Publishing Jenkins on 0.0.0.0 without a reverse proxy"
    Use localhost for labs; production needs TLS termination and network controls.

!!! warning "Losing the volume"
    Never `docker compose down -v` unless you intend to wipe `JENKINS_HOME`.

!!! warning "Leaving the initial admin password in shared logs"
    Rotate after wizard; do not paste unlock secrets into tickets.

## Best Practices



- Encode **Installing Jenkins LTS** changes as code and review them in pull requests
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



**Installing Jenkins LTS** is essential for Cloud and DevOps engineers operating Jenkins. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions



1. What is `JENKINS_HOME` and why must it be persisted?
2. How do you unlock a fresh Jenkins controller?
3. Why pin `jenkins/jenkins:lts` instead of `latest`?
4. Which ports does a typical Docker Jenkins expose and why?
5. What does the setup wizard configure beyond plugins?

!!! tip "Sample answer — question 1"
    `JENKINS_HOME` holds jobs, plugins, credentials metadata, and build history. Without a volume or disk, every container recreate is a factory reset.

!!! tip "Sample answer — question 3"
    `latest` can jump major lines unexpectedly. LTS (or a specific LTS tag/digest) keeps upgrades intentional and testable.

## Related Tutorials



- [Course overview](index.md)
- [Introduction to Jenkins and CI/CD](introduction-to-jenkins-and-ci-cd.md)
- [Using Jenkins — Jobs, Views, and Folders](using-jenkins-jobs-views-and-folders.md)

## References



- [Installing Jenkins](https://www.jenkins.io/doc/book/installing/)
- [Docker install](https://www.jenkins.io/doc/book/installing/docker/)
- [Jenkins LTS download](https://www.jenkins.io/download/lts/)
