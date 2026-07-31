---
title: "Agents, Nodes, and Executors"
description: "Configure agents, labels, and executors; keep builds off the Jenkins controller."
difficulty: intermediate
estimated_time: "45–60 min"
technology: jenkins
category: jenkins
module: "Module 6 · Agents, Nodes, and Executors"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - jenkins
  - agents
  - executors
prerequisites:
  - jenkins/jenkinsfile-in-scm
next:
  - jenkins/multibranch-pipelines-and-prs
tags:
  - jenkins
  - agents
  - nodes
  - labels
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---

# Agents, Nodes, and Executors

## Overview

Design a safe agent topology: **nodes**, **labels**, **executors**, and tool installations.

The built-in node (controller) must not run untrusted builds. Static agents, inbound agents, and later Docker/Kubernetes agents provide isolation. Understand connectivity basics and why workspaces live on agents.

This is a core tutorial in **Module 6 · Agents, Nodes, and Executors** of the REBASH Academy **Jenkins for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- Completed prior modules in this track where linked in frontmatter
- [Git](../git/index.md) and [Docker](../docker/index.md) for lab workflows
- Running Jenkins LTS from [Installing Jenkins LTS](installing-jenkins-lts.md) when a live controller is required

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain why builds must not run on the built-in node
- [ ] Define labels and bind a Pipeline `agent { label '…' }`
- [ ] Relate executors to concurrency and disk/CPU pressure
- [ ] Describe tool installations versus installing tools on the agent image

## Architecture

This topic’s control points and relationships are shown below.

![Controller and agents](../assets/excalidraw/jenkins-controller-agents.svg)

## Theory

### What it is

A **node** is a machine (or container) registered with Jenkins. Each node has one or more **executors** — parallel build slots. **Labels** are tags (`linux`, `docker`, `gpu`) that Pipelines select with `agent { label 'linux' }`. **Tool installations** (JDK, Maven, Gradle) can be managed globally and auto-installed on agents, but immutable agent images are often cleaner in cloud-native setups.

Agent connectivity: inbound agents dial out to the controller (port `50000` in classic JNLP setups) or use WebSocket; outbound SSH agents are started by the controller.

### Why it matters

A compromised build on the controller can read credentials files, change jobs, or encrypt-lock `JENKINS_HOME`. Isolation is a security control, not just scaling. Labels also keep Windows, macOS, and Linux toolchains from colliding on one host.

### How it works

1. In Manage Jenkins → Nodes, inspect the built-in node; set its executors to `0` in production-like labs when you have another agent.
2. Add an agent (SSH or inbound) with labels, or simulate policy in notes if you lack a second VM.
3. Point Pipeline `agent { label 'linux' }` at that label.
4. Observe the workspace path on the agent, not under the controller’s job config alone.
5. Prefer baking tools into agent images over snowflake installs.

See [Distributed builds](https://www.jenkins.io/doc/book/using/using-agents/) style guidance in the handbook under using/scaling topics.

### Key concepts and comparisons

| Policy | Rationale |
|--------|-----------|
| Executors on built-in = 0 | Protect control plane |
| Labels per capability | Correct toolchain selection |
| One heavy job type per pool | Predictable capacity |
| Ephemeral agents later | Clean workspaces each run |

| Approach | Trade-off |
|----------|-----------|
| Static VMs | Simple, always-on cost |
| Docker agent | Reproducible tools |
| Kubernetes pods | Elastic, needs cluster |

### Common pitfalls

- Leaving built-in executors at 2 “just for convenience”.
- Oversubscribing executors on a small VM (thrashing).
- No disk cleanup — workspaces fill the agent.
- Mixing trusted release jobs and untrusted PR builds on the same writable agent without isolation.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-jenkins/module-06 && cd ~/rebash-jenkins/module-06
```

**Focus:** document a zero-executor controller policy and labelled agent Pipeline

### Step 1 – Primary exercise

```bash
cat > agent-policy.md << 'EOF'
# Agent policy (lab)
- Built-in node executors: 0 in production
- Required labels: linux, docker
- Pipeline snippet:
  agent { label 'linux' }
- Tools: prefer image-baked JDK/Maven over global auto-install when possible
EOF
cat > Jenkinsfile << 'EOF'
pipeline {
  agent { label 'linux' }
  stages {
    stage('Where am I') {
      steps {
        sh 'uname -a; pwd; echo "Run on labelled agent, not controller"'
      }
    }
  }
}
EOF
grep -E "label|executors|Built-in" agent-policy.md Jenkinsfile
```

### Step 2 – Validate label directive

```bash
grep -A1 'agent' Jenkinsfile
test -f agent-policy.md && echo 'policy-ok'
```

### Final cleanup

```bash
# Keep ~/rebash-jenkins/ for later tutorials; stop Compose only if you are done with the controller
# docker compose -f ~/rebash-jenkins/module-02/docker-compose.yml down   # optional; omit -v to keep JENKINS_HOME
```

## Validation

- [ ] Lab commands run under `~/rebash-jenkins/module-06/`
- [ ] You can explain each Theory section in your own words
- [ ] You used current Jenkins LTS / Pipeline practices where they apply
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Agents, Nodes, and Executors** always combines:

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

!!! warning "Builds on the built-in node"
    Set built-in executors to zero once agents exist; treat violations as severity-one security debt.

!!! warning "Unlimited executors"
    Match executor count to CPU/memory; watch queue time versus host thrash.

!!! warning "Shared mutable agents for PRs"
    Untrusted branches need isolation (ephemeral containers/pods).

## Best Practices

- Encode **Agents, Nodes, and Executors** changes as code and review them in pull requests
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

**Agents, Nodes, and Executors** is essential for Cloud and DevOps engineers operating Jenkins. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. Why set the built-in node’s executors to zero?
2. What is a label and how does a Pipeline select it?
3. How do executors affect throughput?
4. Inbound versus SSH agents — what differs?
5. When do global tool installations hurt more than they help?

!!! tip "Sample answer — question 1"
    So untrusted build steps cannot run on the controller host that holds `JENKINS_HOME` and credential material.

!!! tip "Sample answer — question 2"
    Labels are tags on nodes; `agent { label 'docker' }` schedules only matching agents.

## Related Tutorials

- [Course overview](index.md)
- [Jenkinsfile in SCM](jenkinsfile-in-scm.md)
- [Multibranch Pipelines and Pull Requests](multibranch-pipelines-and-prs.md)

## References

- [Using Jenkins](https://www.jenkins.io/doc/book/using/)
- [Scaling Jenkins](https://www.jenkins.io/doc/book/scaling/)
- [Pipeline Syntax — agent](https://www.jenkins.io/doc/book/pipeline/syntax/#agent)
