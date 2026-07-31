---
title: "Container Logging and Monitoring"
description: "Collect Docker logs, choose logging drivers, add health checks, and expose metrics for Prometheus and Grafana in DevOps environments."
difficulty: intermediate
estimated_time: "40–55 min"
technology: docker
category: docker
module: "Module 13 · Logging & Monitoring"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - docker
  - logging
  - monitoring
prerequisites:
  - docker/container-scanning-and-sbom
next:
  - docker/docker-performance-and-resource-limits
related:
  - monitoring/index
  - prometheus/index
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
tags:
  - docker
  - logging
  - healthcheck
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Container Logging and Monitoring

## Overview

Follow container logs, configure a logging mindset for production, add HEALTHCHECK, and know how metrics reach Prometheus/Grafana.

Stdout/stderr is the default log stream. Drivers ship logs to journald, Fluentd, cloud sinks. Health checks and metrics tell you when to restart or scale.

This is a core tutorial in **Module 13 · Logging & Monitoring** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Container Scanning and SBOM](container-scanning-and-sbom.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Use `docker logs` effectively  
- [ ] Name common logging drivers  
- [ ] Add Dockerfile/`compose` health checks  
- [ ] Outline cAdvisor / Prometheus scrape path

## Architecture

This topic’s control points and relationships are shown below.

![Production observability](../assets/excalidraw/docker-production-platform.svg)

## Theory

### What

Containers emit **logs** (usually stdout/stderr), expose **health** signals, and should produce **metrics** for resources and application golden signals. Docker logging drivers ship container output; healthchecks tell orchestrators whether to restart; metrics come from exporters, cAdvisor-style collectors, or the app’s `/metrics` endpoint.

### Why

When a container exits, logs are often the only explanation. Without healthchecks, load balancers send traffic to dead processes. Without resource metrics, you learn about memory limits from the out-of-memory (OOM) killer. DevOps operability starts at the container boundary.

### How it works

Prefer structured JSON logs on stdout; sidecars or agents ship to a central platform. Avoid logging secrets and high-cardinality noise. `HEALTHCHECK` in Dockerfiles or Compose `healthcheck:` run a command that exits non-zero when unhealthy. Monitor CPU, memory, restart counts, and application latency/error rate. Locally, `docker logs` and `docker stats` are first tools; in production, integrate with the platform’s observability stack.

| Signal | Source |
|--------|--------|
| Logs | App stdout → logging driver |
| Health | `HEALTHCHECK` / Compose `healthcheck` |
| Metrics | cAdvisor, exporters, app `/metrics` |

### Key concepts

- **Twelve-factor logging** — treat logs as event streams  
- **Driver choice** — json-file defaults vs journald/fluentd in enterprises  
- **Cardinality** — labels/tags that explode metric series  
- **Correlation** — request IDs across services  


Define a minimum dashboard per service: restart rate, CPU/memory against limits, error log rate, and latency if applicable. On shared Docker hosts, also watch disk usage for log drivers that default to unbounded json-file growth — set `max-size` and `max-file` options. Practice reading logs from a failed container during game days, not for the first time in an outage.

### Common pitfalls

- Writing logs only inside the container filesystem  
- Healthchecks that always succeed (testing the shell, not the app)  
- Logging passwords or tokens  
- Alerting solely on container “running” without app metrics

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-docker/module-13 && cd ~/rebash-docker/module-13
```

**Focus:** hands-on practice for Container Logging and Monitoring

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-docker/module-13 && cd ~/rebash-docker/module-13
docker run -d --name rebash-log nginx:alpine
docker logs rebash-log --tail 20
docker inspect --format '{{ "{{" }}.State.Health{{ "}}" }}' rebash-log || true

cat > Dockerfile << 'EOF'
FROM nginx:alpine
HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
  CMD wget -qO- http://127.0.0.1/ || exit 1
EOF
docker build -t rebash-hc:0.1.0 .
docker run -d --name rebash-hc rebash-hc:0.1.0
sleep 6
docker inspect --format '{{ "{{" }}.State.Health.Status{{ "}}" }}' rebash-hc
docker rm -f rebash-log rebash-hc
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-docker/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-docker/module-13/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Container Logging and Monitoring** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for docker as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Writing logs only inside the container filesystem  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Healthchecks that always succeed (testing the shell, not the app)  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Container Logging and Monitoring changes as code and review them in pull requests
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

**Container Logging and Monitoring** is essential for Cloud and DevOps engineers working with docker. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Container Logging and Monitoring** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Docker Performance and Resource Limits](docker-performance-and-resource-limits.md)

## References

- [Configure logging drivers](https://docs.docker.com/engine/logging/) · [HEALTHCHECK](https://docs.docker.com/reference/dockerfile/#healthcheck)
