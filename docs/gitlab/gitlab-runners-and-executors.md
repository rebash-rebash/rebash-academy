---
title: "GitLab Runners and Executors"
description: "Choose shared, group, and project runners; compare shell, Docker, and Kubernetes executors; and use tags and autoscaling safely."
difficulty: intermediate
estimated_time: "40–55 min"
technology: gitlab
category: gitlab
module: "Module 3 · GitLab Runners"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - gitlab-runner
  - executors
  - autoscaling
prerequisites:
  - gitlab/gitlab-projects-mrs-and-releases
next:
  - gitlab/pipeline-syntax-gitlab-ci-yml
related:
  - docker/introduction-to-docker
  - kubernetes/introduction-to-kubernetes
labs: []
projects: []
interview: interview/gitlab
certifications:
  - GitLab Certified CI/CD Associate
tags:
  - gitlab
  - runners
  - executors
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# GitLab Runners and Executors

## Overview



Distinguish shared, group, and project runners; pick an executor for isolation; and use job tags so the right capacity picks up production work.

A **GitLab Runner** is the agent that executes jobs. The **executor** decides *how* isolation works (host shell, Docker container, Kubernetes Pod, and others). Scope (instance/shared, group, project) decides *who* can use the runner. Tags bind jobs to capable fleets.

This is a core tutorial in **Module 3 · GitLab Runners** of the REBASH Academy **GitLab CI/CD for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [GitLab Projects, Merge Requests, and Releases](gitlab-projects-mrs-and-releases.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Contrast shared vs group vs project runners  
- [ ] Choose shell, Docker, or Kubernetes executors for a workload  
- [ ] Use `tags` so jobs land on the right fleet  
- [ ] Outline why autoscaling exists (cost and queue depth)



## Architecture



This topic’s control points and relationships are shown below.

![Runner architecture](../assets/excalidraw/gitlab-runner-architecture.svg)



## Theory



### What it is

GitLab schedules jobs; **runners** claim them over the Runner API. Registration associates a runner with an instance, group, or project (modern registration uses authentication tokens and runner types). The **executor** plugin runs the job:

| Executor | Isolation | Typical use |
|----------|-----------|-------------|
| Shell | Process on the runner host | Legacy / carefully locked hosts |
| Docker | Container per job | Most SaaS and self-managed CI |
| Kubernetes | Pod per job | Cluster-backed platforms |
| Docker Machine / autoscaler | Ephemeral VMs | Burst capacity (evolving tooling) |

**Shared (instance) runners** serve many projects (GitLab.com shared runners). **Group runners** serve all projects in a group. **Project runners** are scoped to one project — useful for privileged or regulated workloads.

### Why it matters

Wrong executor choices create security and reliability debt: shell executors share a host filesystem; untagged “any runner” jobs can land on laptops registered as runners; missing capacity creates hour-long queues. Platform teams treat runners as **product infrastructure** — sized, tagged, monitored, and patched like any other fleet.

### How it works

1. Admin registers a runner with GitLab (token / runner authentication).
2. Runner polls for jobs that match its tags and access scope.
3. For Docker: pull `image:` (or default), mount the build directory, run `script`.
4. For Kubernetes: create a build Pod in a configured namespace, stream logs, clean up.
5. Status and artefacts return to GitLab; autoscalers add/remove runner capacity from queue metrics.

Job authors select capacity with `tags: [docker, linux]` (example). Without tags, any untagged runner in scope may take the job — usually undesirable in production.

You can study YAML without owning runners: GitLab.com free tier provides shared runners; **gitlab-ci-local** runs many jobs on your laptop; `glab ci lint` validates syntax.

### Key concepts and comparisons

| Scope | Who can use it | Ops note |
|-------|----------------|----------|
| Shared / instance | Broad set of projects | Minute quotas, noisy neighbour |
| Group | Projects under the group | Standard platform fleet |
| Project | One project | Privileged / air-gapped builds |

**Autoscaling overview:** idle VMs or cluster nodes cost money; static fleets waste capacity. Autoscaling adds runners when the pending queue grows and removes them when idle — design for warm pools if cold starts hurt MR feedback.

### Common pitfalls

- Registering a personal laptop as an unprotected shared runner.
- Using the shell executor for untrusted open-source MRs.
- Forgetting tags so GPU or privileged jobs never run (or run everywhere).
- Equating “Docker executor” with “Docker-in-Docker” — DinD is a separate, higher-risk pattern.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-gitlab/module-03 && cd ~/rebash-gitlab/module-03
```

**Focus:** document runner/executor choices and a tags-based job

### Step 1 – Runner tags

```bash
cat > .gitlab-ci.yml << 'EOF'
build:
  tags: [docker, linux]
  image: alpine:3.20
  script:
    - uname -a
    - echo "Job expects a runner with tags docker+linux"
EOF
tee runner-notes.txt << 'EOF'
Shell vs Docker vs Kubernetes executors trade isolation, speed, and ops cost.
Register runners with least privilege and ephemeral environments where possible.
EOF
cat runner-notes.txt
```

### Final step – Cleanup note

```bash
# File-only
```



## Validation



- [ ] Lab commands run under `~/rebash-gitlab/module-03/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **GitLab Runners and Executors** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.



## Security Considerations



- Treat credentials and tokens for gitlab as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces



## Common Mistakes



!!! warning "Registering a personal laptop as an unprotected shared runner."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Using the shell executor for untrusted open-source MRs."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode GitLab Runners and Executors changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible



## Troubleshooting



| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |



## Summary



**GitLab Runners and Executors** is essential for Cloud and DevOps engineers working with gitlab. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. How does **GitLab Runners and Executors** show up in a real GitLab delivery workflow?
2. A pipeline is stuck / red — what do you check first?
3. How do `needs`, stages, and artefacts interact?
4. How should secrets and cloud credentials be handled in GitLab CI?
5. How would you keep merge-request pipelines fast but still safe?

!!! tip "Sample answer — question 2"
    Open the failing job log, confirm runner tags/executor, then validate `.gitlab-ci.yml` with CI Lint. Check rules that skipped jobs and artefact dependencies.

!!! tip "Sample answer — question 4"
    Prefer masked/protected variables and OIDC (`id_tokens`) over long-lived keys. Limit who can run protected-branch pipelines.



## Related Tutorials



- [Course overview](index.md)
- [Pipeline Syntax (.gitlab-ci.yml)](pipeline-syntax-gitlab-ci-yml.md)



## References



- [GitLab Runner](https://docs.gitlab.com/runner/)  
- [Executors](https://docs.gitlab.com/runner/executors/)
