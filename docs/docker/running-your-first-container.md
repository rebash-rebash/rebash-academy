---
title: "Running Your First Container — Docker CLI"
description: "Master essential Docker CLI commands — run, ps, stop, rm, exec, logs, and inspect — for daily DevOps container operations."
difficulty: beginner
estimated_time: "40–55 min"
technology: docker
category: docker
module: "Module 3 · Docker CLI"
career_paths:
  - beginner
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - docker
  - docker-cli
prerequisites:
  - docker/docker-installation-and-setup
next:
  - docker/working-with-docker-images
related:
  - docker/troubleshooting-docker-containers
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
tags:
  - docker
  - cli
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Running Your First Container — Docker CLI

## Overview

Use the core Docker CLI to run, inspect, exec into, log, stop, and remove containers confidently.

Daily ops is CLI fluency: `run`, `ps`, `logs`, `exec`, `stop`, `rm`. Lifecycle awareness prevents orphan containers and surprise disk use.

This is a core tutorial in **Module 3 · Docker CLI** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Docker Installation and Setup](docker-installation-and-setup.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] `docker run` with ports and names  
- [ ] List running/stopped containers  
- [ ] Follow logs and `exec` a shell  
- [ ] Inspect JSON config  
- [ ] Clean up with `stop` / `rm`

## Architecture

This topic’s control points and relationships are shown below.

![Container lifecycle](../assets/excalidraw/docker-container-lifecycle.svg)

## Theory

### What

`docker run` creates and starts a container from an image. Day-one operations also include listing (`ps`), stopping, reading logs, executing a shell in a running container (`exec`), and inspecting low-level metadata. These commands are the foundation of every later Compose and Kubernetes skill.

### Why

If you cannot start a container, read its logs, and confirm the process exit code, you cannot debug CI or production. Learning graceful stop versus kill, and when to use `--rm`, prevents leftover containers filling disks during labs.

### How it works

`docker run [options] image [cmd]` pulls the image if needed, creates a container, and starts it. Common flags publish ports (`-p`), set environment variables (`-e`), mount volumes, and name the container. Foreground vs detached (`-d`) changes whether your terminal attaches to the process. `docker logs` reads the configured logging driver (often json-file capturing stdout/stderr). `docker exec` starts an *additional* process in the same namespaces — useful for debugging, not as the main entrypoint. `docker inspect` prints JSON; Go-template `--format` strings use double braces and must be escaped in MkDocs, for example `{{ "{{" }}.State.Status{{ "}}" }}`.

| Command | Use |
|---------|-----|
| `docker run` | Create + start (often `--rm`) |
| `docker ps -a` | List containers |
| `docker stop` / `kill` | Graceful vs SIGKILL |
| `docker logs -f` | Stdout/stderr |
| `docker exec -it` | Shell in running container |
| `docker inspect` | Low-level details |

### Key concepts

- **PID 1** — the container’s main process; its exit stops the container  
- **Published ports** — host:container mapping is not the same as `EXPOSE`  
- **Ephemeral vs named** — `--rm` for experiments; names for labs you revisit  
- **Exit codes** — distinguish pull failures from app crashes  

### Common pitfalls

- Forgetting `-d` and thinking the container “died” when you closed the terminal wrongly  
- Using `kill` before allowing graceful `stop`  
- `exec` into a crashed container (it must be running)  
- Publishing `0.0.0.0` ports on shared runners without care

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-docker/module-03 && cd ~/rebash-docker/module-03
```

**Focus:** hands-on practice for Running Your First Container — Docker CLI

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Running Your First Container — Docker CLI"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-docker/module-03 && cd ~/rebash-docker/module-03
docker run -d --name rebash-nginx -p 8080:80 nginx:alpine
docker ps
curl -sI http://127.0.0.1:8080 | head -n 5
docker logs rebash-nginx | head
docker exec rebash-nginx nginx -v
docker inspect rebash-nginx --format '{{ "{{" }}.State.Status{{ "}}" }} {{ "{{" }}.NetworkSettings.IPAddress{{ "}}" }}'
docker stop rebash-nginx
docker rm rebash-nginx
docker ps -a | grep rebash-nginx || echo "cleaned"
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-docker/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-docker/module-03/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Running Your First Container — Docker CLI** always combines:

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

!!! warning "Forgetting `-d` and thinking the container “died” when you closed the terminal wrongly  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Using `kill` before allowing graceful `stop`  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Running Your First Container — Docker CLI changes as code and review them in pull requests
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

**Running Your First Container — Docker CLI** is essential for Cloud and DevOps engineers working with docker. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Running Your First Container — Docker CLI** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Working with Docker Images](working-with-docker-images.md)

## References

- [docker run](https://docs.docker.com/reference/cli/docker/container/run/)
