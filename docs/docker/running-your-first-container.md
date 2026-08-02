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



### Objective

Build or run a real Docker solution for **Running Your First Container — Docker CLI** and prove it with inspect/logs/HTTP.

### Prerequisites

- Docker Engine or Docker Desktop
- Permission to run containers

### Lab environment

Workspace: `~/rebash-docker/module-03`

Local Docker daemon. Clean up containers/images after the lab.

```bash
mkdir -p ~/rebash-docker/module-03 && cd ~/rebash-docker/module-03
```

### Real-world scenario

You are validating **Running Your First Container — Docker CLI** before it lands in CI. The change must be reproducible with copy-paste commands and leave no orphan containers.

### Step-by-step tasks

#### Task 1 – Run and inspect a container

Start from a known image, publish a port, and verify HTTP.

```bash
docker run -d --name rebash-lab -p 18080:80 nginx:alpine
docker ps --filter name=rebash-lab
curl -sI http://127.0.0.1:18080 | head -n 5 | tee headers.txt
docker logs rebash-lab 2>&1 | head -n 10 | tee logs.txt
```

**Expected output:** Container Up; HTTP 200 in headers.txt.

#### Task 2 – Inspect runtime config

Use inspect for status — production debugging rarely starts with guesswork.

```bash
docker inspect rebash-lab --format '{{ "{{" }}.State.Status{{ "}}" }} {{ "{{" }}.Config.Image{{ "}}" }}' | tee inspect.txt
test -s inspect.txt
```

**Expected output:** inspect.txt shows `running` and the nginx image.

### Validation steps

- [ ] Container or image behaves as Expected output describes
- [ ] Ports respond or command output matches
- [ ] Cleanup removes lab resources

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| port is already allocated | Previous lab left a container | `docker rm -f` the old name or change port |
| permission denied | User not in docker group | Use rootless Docker or fix group membership |
| manifest unknown | Bad tag | Pin a real tag such as `nginx:alpine` |

### Challenge exercise

Add a non-root USER (or Compose healthcheck) and prove it with inspect.

### Learning outcomes

- Executed a real Docker workflow
- Captured evidence files
- Removed disposable resources

### Cleanup

```bash
docker rm -f rebash-lab 2>/dev/null || true
docker rmi rebash-lab:local 2>/dev/null || true
docker compose down -v 2>/dev/null || true
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




1. What do -d, --name, and -p do?
2. Port publish fails — typical causes?
3. How do you get a shell in a running container?
4. Difference between stop and rm?
5. Why prefer --rm for ephemeral experiments?

!!! tip "Sample answer — question 2"
    Confirm the container is running, the published port mapping, and that nothing else bound the host port.

!!! tip "Sample answer — question 4"
    Do not publish administrative ports to 0.0.0.0 on untrusted networks.

## Related Tutorials







- [Course overview](index.md)
- [Working with Docker Images](working-with-docker-images.md)

## References







- [docker run](https://docs.docker.com/reference/cli/docker/container/run/)
