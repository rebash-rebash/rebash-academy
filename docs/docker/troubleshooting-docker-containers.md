---
title: "Troubleshooting Docker Containers"
description: "Debug containers that will not start, CrashLoop-style exits, pull errors, networking, permissions, and disk usage for DevOps."
difficulty: intermediate
estimated_time: "45–60 min"
technology: docker
category: docker
module: "Module 16 · Troubleshooting"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - docker
  - troubleshooting
prerequisites:
  - docker/docker-in-ci-cd-pipelines
next:
  - docker/production-docker-patterns
related:
  - docker/docker-networking-fundamentals
  - docker/running-your-first-container
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
tags:
  - docker
  - troubleshooting
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Troubleshooting Docker Containers

## Overview



Apply a systematic playbook: status → logs → inspect → exec → host resources — for the common Docker failure modes.

Most incidents are config or resource issues, not “Docker is broken.” Reproduce locally with the same image digest when possible.

This is a core tutorial in **Module 16 · Troubleshooting** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Docker in CI/CD Pipelines](docker-in-ci-cd-pipelines.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Diagnose exit codes and restart loops  
- [ ] Fix image pull / auth errors  
- [ ] Debug port and DNS issues  
- [ ] Spot permission / volume UID problems  
- [ ] Free disk with informed prune



## Architecture



This topic’s control points and relationships are shown below.

![Container lifecycle](../assets/excalidraw/docker-container-lifecycle.svg)



## Theory



### What

Container troubleshooting follows a log-first, state-second method: read exit codes and logs, inspect configuration, verify networks and mounts, then check host resources. Symptoms include crash loops, pull failures, connection refusals, and permission errors on volumes.

### Why

Guessing wastes time. The same patterns appear from laptop Docker to Kubernetes CrashLoopBackOff — the process failed, the image failed to pull, or the environment is wrong. A repeatable checklist makes on-call work calmer.

### How it works

If a container will not stay up, `docker logs` and `docker inspect` (ExitCode, Error, OOMKilled) come first. Instant exit often means the main process crashed — override the command with a sleep/shell to explore the filesystem when appropriate. Pull errors point at auth, tag typos, or rate limits. Connection issues need published ports, network membership, and host firewall checks. Permission denied on mounted files usually means UID mismatch with `USER`. Disk-full failures show in daemon errors; `docker system df` confirms.

| Symptom | Checks |
|---------|--------|
| Won't start | Logs, ExitCode, CMD |
| Instant exit | App crash — override command |
| Pull errors | Auth, tag, rate limit |
| Can't connect | `-p`, network, firewall |
| Permission denied | Volume UID vs `USER` |
| No space | `docker system df`, prune |

### Key concepts

- **Exit code literacy** — 137 often means SIGKILL/OOM  
- **Layer the problem** — app vs image vs runtime vs host  
- **Reproduce minimally** — smallest `docker run` that fails  
- **Time correlation** — deploys, pulls, and node pressure  

### Common pitfalls

- Deleting the failed container before reading logs  
- Fixing the host when the CMD is wrong  
- Ignoring registry rate limits and “random” pull failures  
- Restarting endlessly without a health/backoff strategy



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-docker/module-16 && cd ~/rebash-docker/module-16
```

**Focus:** debug a failing container with logs and inspect

### Step 1 – Broken CMD

```bash
docker run --name rebash-lab alpine:3.20 /bin/does-not-exist || true
docker ps -a --filter name=rebash-lab
docker logs rebash-lab 2>&1 | tee boom.log || true
docker inspect rebash-lab --format '{{ "{{" }}.State.Status{{ "}}" }} {{ "{{" }}.State.ExitCode{{ "}}" }} {{ "{{" }}.State.Error{{ "}}" }}'
docker rm rebash-lab
docker run --rm --name rebash-lab alpine:3.20 echo recovered
```

### Final step – Cleanup note

```bash
docker rm -f rebash-lab rebash-lab2 2>/dev/null || true
docker network rm rebash-net 2>/dev/null || true
docker volume rm rebash-vol 2>/dev/null || true
docker rmi rebash-lab:local 2>/dev/null || true
```



## Validation



- [ ] Lab commands run under `~/rebash-docker/module-16/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Troubleshooting Docker Containers** always combines:

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



!!! warning "Deleting the failed container before reading logs  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Fixing the host when the CMD is wrong  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Troubleshooting Docker Containers changes as code and review them in pull requests
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



**Troubleshooting Docker Containers** is essential for Cloud and DevOps engineers working with docker. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. What production problem does **Troubleshooting Docker Containers** address in container platforms?
2. A container restarts continually — how do you triage?
3. Why are mutable `latest` tags risky in production?
4. Which container security controls do you insist on before prod?
5. How do you keep images small and builds fast in CI?

!!! tip "Sample answer — question 2"
    Check `docker ps -a`, logs, exit code, and `inspect` for OOM/restarts. Confirm command/entrypoint and volume permissions.

!!! tip "Sample answer — question 4"
    Non-root, minimal base, no secrets in layers, scanning, read-only rootfs where possible, and least capabilities.



## Related Tutorials



- [Course overview](index.md)
- [Production Docker Patterns](production-docker-patterns.md)



## References



- [Docker debug](https://docs.docker.com/reference/cli/docker/debug/)
