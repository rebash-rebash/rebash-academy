---
title: "Troubleshooting and Upgrades"
description: "Troubleshoot failed builds and agents, use Pipeline replay, manage plugin issues, and plan Jenkins LTS upgrades."
difficulty: advanced
estimated_time: "45–60 min"
technology: jenkins
category: jenkins
module: "Module 16 · Troubleshooting and Upgrades"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - jenkins
  - troubleshooting
  - upgrades
prerequisites:
  - jenkins/jcasc-scaling-and-operations
next: []
tags:
  - jenkins
  - troubleshooting
  - lts
  - upgrades
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Troubleshooting and Upgrades

## Overview



Diagnose production Jenkins: failed builds, agent issues, Pipeline **replay**, plugin problems, performance symptoms, **LTS upgrade** guides, safe restart, and rollback.

Upgrades are operational procedures — not surprise Friday clicks.

This is a core tutorial in **Module 16 · Troubleshooting and Upgrades** of the REBASH Academy **Jenkins for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites



- Completed prior modules in this track where linked in frontmatter
- [Git](../git/index.md) and [Docker](../docker/index.md) for lab workflows
- Running Jenkins LTS from [Installing Jenkins LTS](installing-jenkins-lts.md) when a live controller is required

## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Triage a failed build from console logs and stage views
- [ ] Use Pipeline replay appropriately (and know its limits)
- [ ] Outline a plugin regression bisect approach
- [ ] Plan an LTS upgrade with backup and rollback

## Architecture



This topic’s control points and relationships are shown below.

![Troubleshooting and upgrades](../assets/excalidraw/jenkins-troubleshooting.svg)

## Theory



### What it is

**Console logs** are the first artefact; **Pipeline Steps** and stage views narrow the failing step. **Replay** re-runs with edited script (admin capability — audit it). Agent issues show as “offline”, “launch failed”, or queue stuck. Plugin problems often appear after updates — binary search disable/update. **LTS upgrades** follow published upgrade guides; backup `JENKINS_HOME`, upgrade test, then production, with a restore rollback path.

### Why it matters

Mean time to recovery depends on disciplined triage. Unplanned upgrades couple plugin binaries to controller core. SRE-owned runbooks beat heroics.

### How it works

1. Capture build URL, Git SHA, agent label, and failing step.
2. Reproduce on a non-prod controller when possible.
3. Check agent connectivity and executor availability.
4. For regressions, identify last good plugin/core versions.
5. Upgrade along LTS: read [LTS upgrade guides](https://www.jenkins.io/doc/upgrade-guide/), snapshot, change window, smoke tests.

System admin topics: [Troubleshooting](https://www.jenkins.io/doc/book/system-administration/) style handbook pages.

### Key concepts and comparisons

| Symptom | First checks |
|---------|--------------|
| Queue forever | Agents online? labels? executors? |
| Git checkout fail | Credentials, SSH host keys |
| Groovy CPS errors | Script security, library versions |
| Slow UI | Heap, plugins, build records retention |

| Upgrade step | Why |
|--------------|-----|
| Backup | Rollback reality |
| Test controller | Plugin surprise |
| Smoke Pipelines | Real validation |
| Safe restart | Clean load |

### Common pitfalls

- Replaying production with ad-hoc scripts and never committing the fix.
- Upgrading core and 50 plugins simultaneously with no notes.
- Deleting `JENKINS_HOME` backups after “successful” upgrade day-of.
- Ignoring agent clock skew and disk-full errors.

## Hands-on Lab



### Objective

Configure a real Jenkins-facing artefact for **Troubleshooting and Upgrades** (Compose controller and/or Jenkinsfile) you can run or import.

### Prerequisites

- Docker Engine for controller labs
- Text editor / shell

### Lab environment

Workspace: `~/rebash-jenkins/module-16`

Local Docker Compose Jenkins LTS where a live UI is needed; file-only Jenkinsfile labs otherwise.

```bash
mkdir -p ~/rebash-jenkins/module-16 && cd ~/rebash-jenkins/module-16
```

### Real-world scenario

Your organisation is standardising **Troubleshooting and Upgrades**. You prototype on a lab controller, keep everything as files, and avoid building on the built-in node in production designs.

### Step-by-step tasks

#### Task 1 – Capture controller/agent mental model files

Document how this topic shows up on a real controller.

```bash
tee scenario.md << 'EOF'
Topic: Troubleshooting and Upgrades
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



- [ ] Lab commands run under `~/rebash-jenkins/module-16/`
- [ ] You can explain each Theory section in your own words
- [ ] You used current Jenkins LTS / Pipeline practices where they apply
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough



Production practice for **Troubleshooting and Upgrades** always combines:

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



!!! warning "Fix only via Replay"
    Commit Jenkinsfile/library fixes; replay is for diagnosis, not configuration management.

!!! warning "Big-bang upgrades"
    Split core and plugin changes; use a test controller.

!!! warning "No rollback path"
    A backup you have never restored is a hope, not a plan.

## Best Practices



- Encode **Troubleshooting and Upgrades** changes as code and review them in pull requests
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



**Troubleshooting and Upgrades** is essential for Cloud and DevOps engineers operating Jenkins. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions



1. How do you triage a red Pipeline build?
2. When is Pipeline replay appropriate?
3. How do you isolate a bad plugin update?
4. What is your LTS upgrade checklist?
5. Agent offline — what do you check first?

!!! tip "Sample answer — question 2"
    Use replay to test a hypothesis quickly, then commit the real fix to SCM; control who has replay permission.

!!! tip "Sample answer — question 4"
    Read the upgrade guide, backup, upgrade test, smoke, production change window, smoke again, keep rollback snapshots.

## Related Tutorials



- [Course overview](index.md)
- [JCasC, Scaling, and Operations](jcasc-scaling-and-operations.md)

## References



- [LTS upgrade guides](https://www.jenkins.io/doc/upgrade-guide/)
- [System administration](https://www.jenkins.io/doc/book/system-administration/)
- [Troubleshooting](https://www.jenkins.io/doc/book/troubleshooting/)
