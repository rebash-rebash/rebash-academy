---
title: "Using Jenkins — Jobs, Views, and Folders"
description: "Navigate the Jenkins dashboard, contrast Freestyle with Pipeline jobs, and organise work with views and folders."
difficulty: beginner
estimated_time: "40–55 min"
technology: jenkins
category: jenkins
module: "Module 3 · Using Jenkins"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - jenkins
  - jobs
  - folders
prerequisites:
  - jenkins/installing-jenkins-lts
next:
  - jenkins/pipeline-fundamentals-declarative
tags:
  - jenkins
  - dashboard
  - views
  - folders
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---

# Using Jenkins — Jobs, Views, and Folders

## Overview

Learn the Jenkins user interface: dashboard, jobs, build history, views, folders, and where credentials appear.

**Freestyle** jobs are classic click-configured projects. **Pipeline** jobs (especially Pipeline-as-code) are the modern default for Cloud and DevOps teams. Views filter the dashboard; folders group jobs for teams or products. This module orients you before Declarative Pipeline deep dives.

This is a core tutorial in **Module 3 · Using Jenkins** of the REBASH Academy **Jenkins for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- Completed prior modules in this track where linked in frontmatter
- [Git](../git/index.md) and [Docker](../docker/index.md) for lab workflows
- Running Jenkins LTS from [Installing Jenkins LTS](installing-jenkins-lts.md) when a live controller is required

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Navigate the dashboard, job pages, and build history
- [ ] Contrast Freestyle vs Pipeline job types for new work
- [ ] Create a view and explain when folders help multi-team controllers
- [ ] Locate credentials entry points without storing secrets in job config text

## Architecture

This topic’s control points and relationships are shown below.

![Jenkins UI — jobs, views, folders](../assets/excalidraw/jenkins-ui.svg)

## Theory

### What it is

The **dashboard** lists jobs (and folders). Each job has configuration, build history, and console output per build. **Views** (list, my view) filter what you see. **Folders** (Folders plugin, usually installed with suggested plugins) nest jobs and can hold folder-scoped credentials and shared library configuration later.

**Freestyle** jobs bind SCM, build steps, and post-actions in the UI. **Pipeline** jobs run a Jenkinsfile (inline or from SCM). New greenfield work should be Pipeline; Freestyle remains for legacy understanding only.

### Why it matters

A flat list of hundreds of jobs becomes unusable. Folders mirror org structure (product, environment, team). Views give individuals a focused dashboard. Knowing where credentials are managed prevents pasting tokens into Freestyle shell steps — a common audit finding.

### How it works

1. Open the dashboard after login; note New Item, Manage Jenkins, and People.
2. Create a simple Pipeline job with an inline `echo` stage (or wait for Module 4’s fuller example).
3. Run a build; open Console Output and build history.
4. Create a List View that includes your job.
5. Optionally create a folder and move the job — observe the URL path change.

See [Using Jenkins](https://www.jenkins.io/doc/book/using/) in the User Handbook.

### Key concepts and comparisons

| Concept | Use |
|---------|-----|
| Freestyle | Legacy / simple UI builds |
| Pipeline | Jenkinsfile; reviewable as code |
| View | Personal or team dashboard filter |
| Folder | Namespace jobs; scope credentials |
| Build history | Audit trail of runs |

Credentials appear under Manage Jenkins → Credentials (and folder credentials). Prefer credential IDs referenced from Pipeline over plaintext.

### Common pitfalls

- Creating every job at the root of a shared controller.
- Storing secrets in Freestyle shell steps or job descriptions.
- Assuming Blue Ocean is required — classic UI + Pipeline is enough.
- Ignoring failed builds in history when diagnosing “it worked yesterday”.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-jenkins/module-03 && cd ~/rebash-jenkins/module-03
```

**Focus:** create a folder, a Pipeline job stub, and a list view

### Step 1 – Primary exercise

```bash
# Document UI checklist while controller from module-02 runs
cat > ui-checklist.md << 'EOF'
# Using Jenkins checklist
- [ ] Dashboard loads
- [ ] New Item → Folder `rebash-labs`
- [ ] New Item → Pipeline `hello-pipeline` inside folder
- [ ] Build once; open Console Output
- [ ] Create List View including hello-pipeline
- [ ] Credentials link found under Manage Jenkins (do not store secrets yet)
EOF
# Optional: use jenkins-cli later; for now validate notes
grep -E 'Folder|Pipeline|Credentials' ui-checklist.md
test -f ui-checklist.md
```

### Step 2 – Capture job URL pattern

```bash
cat > url-pattern.txt << 'EOF'
Root job:   /job/hello-pipeline/
Folder job: /job/rebash-labs/job/hello-pipeline/
View:       /view/my-labs/
EOF
cat url-pattern.txt
```

### Final cleanup

```bash
# Keep ~/rebash-jenkins/ for later tutorials; stop Compose only if you are done with the controller
# docker compose -f ~/rebash-jenkins/module-02/docker-compose.yml down   # optional; omit -v to keep JENKINS_HOME
```

## Validation

- [ ] Lab commands run under `~/rebash-jenkins/module-03/`
- [ ] You can explain each Theory section in your own words
- [ ] You used current Jenkins LTS / Pipeline practices where they apply
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Using Jenkins — Jobs, Views, and Folders** always combines:

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

!!! warning "Secrets in Freestyle shell"
    Use the Credentials store and bind credentials in Pipeline; never paste tokens into build steps.

!!! warning "Unbounded root-level jobs"
    Use folders early so permissions and libraries can scope later.

!!! warning "Relying on Blue Ocean"
    Treat Blue Ocean as legacy; learn classic UI and Pipeline stages.

## Best Practices

- Encode **Using Jenkins — Jobs, Views, and Folders** changes as code and review them in pull requests
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

**Using Jenkins — Jobs, Views, and Folders** is essential for Cloud and DevOps engineers operating Jenkins. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. When would you still see Freestyle jobs in an enterprise?
2. How do folders help multi-team Jenkins controllers?
3. Where should credentials live instead of job shell steps?
4. What does build history give you during an incident?
5. What is the difference between a view and a folder?

!!! tip "Sample answer — question 2"
    Folders namespace jobs, can hold folder credentials and library config, and make authorization matrices manageable per team.

!!! tip "Sample answer — question 3"
    Use Manage Jenkins → Credentials (or folder credentials) and reference credential IDs from Pipeline steps such as `withCredentials`.

## Related Tutorials

- [Course overview](index.md)
- [Installing Jenkins LTS](installing-jenkins-lts.md)
- [Pipeline Fundamentals (Declarative)](pipeline-fundamentals-declarative.md)

## References

- [Using Jenkins](https://www.jenkins.io/doc/book/using/)
- [Pipeline Getting Started](https://www.jenkins.io/doc/pipeline/tour/getting-started/)
- [Managing Credentials](https://www.jenkins.io/doc/book/using/using-credentials/)
