---
title: "Pipeline Monitoring and Observability"
description: "Use GitLab pipeline analytics, job logs, runner metrics, and notifications to observe CI/CD health for Cloud & DevOps teams."
difficulty: intermediate
estimated_time: "40–55 min"
technology: gitlab
category: gitlab
module: "Module 16 · Monitoring & Observability"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - gitlab-ci
  - observability
  - pipeline-analytics
  - metrics
prerequisites:
  - gitlab/production-pipelines-and-environments
next:
  - gitlab/troubleshooting-gitlab-ci
related:
  - gitlab/gitlab-runners-and-executors
  - prometheus-grafana/index
labs: []
projects: []
interview: interview/gitlab
certifications:
  - GitLab Certified CI/CD Associate
  - GitLab Certified DevOps Professional
tags:
  - gitlab
  - monitoring
  - observability
  - analytics
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Pipeline Monitoring and Observability

## Overview

Observe pipeline health with analytics, job logs, runner and pipeline metrics, and actionable notifications — without drowning the team in noise.

CI/CD is a production system. **Observability** means you can answer: Are pipelines slower? Which jobs fail most? Are runners saturated? GitLab provides pipeline analytics and logs; runners and external metrics complete the picture.

This is a core tutorial in **Module 16 · Monitoring & Observability** of the REBASH Academy **GitLab CI/CD for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Production Pipelines and Environments](production-pipelines-and-environments.md)
- [GitLab Runners and Executors](gitlab-runners-and-executors.md) (runner capacity awareness)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Read pipeline duration and failure trends  
- [ ] Use job logs and artefacts for diagnosis  
- [ ] Identify runner queue / capacity signals  
- [ ] Configure useful notifications (MR, Slack, email)

## Architecture

This topic’s control points and relationships are shown below.

![GitLab monitoring](../assets/excalidraw/gitlab-monitoring.svg)

## Theory

### What it is

**Pipeline monitoring** watches CI as a service: success rate, duration, queue time, and flaky jobs. **Observability** adds context — job logs, artefacts, runner host metrics, and correlation with deploy outcomes. GitLab surfaces **pipeline analytics**, per-job timing, and failure reasons; notifications push status to humans and chat ops.

| Signal | Question it answers |
|--------|---------------------|
| Success rate | Are we shipping or stuck? |
| Duration / p95 | Is feedback too slow? |
| Queue time | Runner capacity enough? |
| Job failure taxonomy | Test vs infra vs auth? |
| Notifications | Who must act now? |

### Why it matters

Slow or flaky CI is a platform outage for developers. Without metrics you scale runners blindly or ignore a single job that causes half of MR delays. SRE-style error budgets apply to pipelines: treat “time to green on main” as a service level indicator (SLI). Notifications that fire on every retry create alert fatigue; notifications that miss production deploy failures create silence risk.

### How it works

1. **Baseline** — note median and p95 pipeline duration for `main` and MRs weekly.
2. **Analytics** — use GitLab’s CI/CD analytics (and Value Stream where licensed) to find slowest jobs.
3. **Logs** — failed job → raw log → last error; keep artefacts (`when: always`) for reports.
4. **Runners** — watch concurrency, executor errors, disk, and image pull latency; scale or retag workloads.
5. **Export** — optional Prometheus metrics from GitLab / runners for Grafana dashboards.
6. **Notify** — pipeline emails, Slack/Teams integrations, or `after_script` webhooks on deploy stages only.

Separate **developer feedback** (MR failed tests) from **platform pages** (shared runners down). Correlate deploy jobs with application SLOs after promotion.

### Key concepts and comparisons

| Layer | Primary tool |
|-------|----------------|
| Pipeline UX | GitLab job log + analytics |
| Runner health | Runner metrics / host monitoring |
| Org trends | CI minutes, queue, flaky rate |
| ChatOps | Webhooks / integrations |

| Good alert | Poor alert |
|------------|------------|
| Production deploy failed | Any job retried |
| Runner fleet < N idle for 15m | Single flaky unit test once |

### Common pitfalls

- Equating “green pipeline rate” with product quality — skipped tests inflate success.
- Logging secrets into job output — observability must not leak credentials.
- Alerting on every `allow_failure` job — reserve pages for customer-impacting stages.
- Ignoring queue time while chasing script micro-optimisations.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-gitlab/module-16 && cd ~/rebash-gitlab/module-16
```

**Focus:** hands-on practice for Pipeline Monitoring and Observability

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-gitlab/module-16 && cd ~/rebash-gitlab/module-16
cat > .gitlab-ci.yml << 'EOF'
stages:
  - observe

# Demo job that emits timing-friendly markers for log review
measure:
  stage: observe
  image: alpine:3.20
  script:
    - START=$(date +%s)
    - echo "START_TS=$START"
    - sleep 1
    - END=$(date +%s)
    - echo "END_TS=$END"
    - echo "DURATION_SEC=$((END-START))"
  artifacts:
    when: always
    paths:
      - metrics.txt
    expire_in: 1 day
  after_script:
    - echo "DURATION_SEC markers above → scrape into your metrics store if needed" | tee metrics.txt

# Notification pattern (configure project integrations in GitLab UI):
# Settings → Integrations → Slack / Teams / email on pipeline failed
EOF

cat > observability-checklist.md << 'EOF'
- [ ] Know p95 pipeline duration for main (last 14 days)
- [ ] Top 3 slowest jobs identified
- [ ] Runner queue time checked under load
- [ ] Production deploy failure notifies on-call
- [ ] MR test failures notify author (not whole company)
- [ ] No secrets in job logs (sample review)
EOF

python3 - << 'PY'
import yaml
yaml.safe_load(open(".gitlab-ci.yml"))
print("YAML parse OK")
PY
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-gitlab/module-16/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Pipeline Monitoring and Observability** always combines:

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

!!! warning "Equating “green pipeline rate” with product quality — skipped tests inflate success."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Logging secrets into job output — observability must not leak credentials."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Pipeline Monitoring and Observability changes as code and review them in pull requests
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

**Pipeline Monitoring and Observability** is essential for Cloud and DevOps engineers working with gitlab. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Pipeline Monitoring and Observability** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Troubleshooting GitLab CI](troubleshooting-gitlab-ci.md)

## References

- [CI/CD analytics](https://docs.gitlab.com/ee/user/analytics/ci_cd_analytics.html)  
- [Pipeline efficiency](https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency.html)  
- [GitLab Runner monitoring](https://docs.gitlab.com/runner/monitoring/)
