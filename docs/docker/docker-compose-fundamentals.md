---
title: "Docker Compose Fundamentals"
description: "Define multi-container apps with Compose — services, networks, volumes, env files, profiles, and health checks for DevOps."
difficulty: intermediate
estimated_time: "45–60 min"
technology: docker
category: docker
module: "Module 9 · Docker Compose"
career_paths:
  - devops-engineer
  - platform-engineer
  - software-engineer
skills:
  - docker
  - docker-compose
prerequisites:
  - docker/docker-networking-fundamentals
next:
  - docker/container-registries-and-distribution
related:
  - docker/environment-variables-and-secrets
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
tags:
  - docker
  - compose
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Docker Compose Fundamentals

## Overview







Author a `compose.yaml` with services, a shared network, a volume, environment variables, and a health check — then bring the stack up and down.

**Compose** declares multi-container apps as code. Ideal for local DevOps stacks and simple single-host deploys before Kubernetes.

This is a core tutorial in **Module 9 · Docker Compose** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Docker Networking Fundamentals](docker-networking-fundamentals.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Define services, networks, volumes  
- [ ] Pass env vars / `env_file`  
- [ ] Add health checks  
- [ ] Use profiles for optional services  
- [ ] `compose up` / `down` / `logs`

## Architecture







This topic’s control points and relationships are shown below.

![Docker Compose](../assets/excalidraw/docker-compose.svg)

## Theory







### What

**Docker Compose** defines multi-container applications as YAML (`compose.yaml`). Compose v2 is the `docker compose` CLI plugin (space, not hyphen). Services, networks, and volumes are declared together; `up` creates them as a project. On the default project network, **service names become DNS names**.

### Why

Real systems need an app plus database, cache, or sidecar. Running five independent `docker run` commands is brittle. Compose is the standard local and small-server orchestration file format and a stepping stone to Kubernetes manifests.

### How it works

A Compose file lists `services:` with images or build contexts, environment, ports, volumes, and `depends_on`. `docker compose up -d` creates a project-prefixed network and starts containers. `docker compose logs -f`, `ps`, `exec`, and `down` manage the stack. Profiles and multiple compose files (`-f`) specialise environments. Prefer explicit healthchecks over blind `depends_on` for readiness. Secrets and env files keep configuration out of images.

Compose v2 command shape:

```bash
docker compose version
docker compose -f compose.yaml up -d
```

### Key concepts

| Idea | Detail |
|------|--------|
| Project name | Prefixes resources; set via folder or `-p` |
| Service DNS | `http://api:8080` from another service |
| Build vs image | Local Dockerfile or registry image |
| Override files | `compose.override.yaml` for local deltas |


Keep Compose files readable: one service per concern, explicit image tags or digests, and comments only where behaviour is non-obvious. Use `.env` for local non-secret defaults and never commit production credentials beside `compose.yaml`. When a stack grows beyond a single host, treat Compose as the development contract and plan the Kubernetes translation deliberately.

### Common pitfalls

- Using obsolete `docker-compose` v1 behaviour docs blindly  
- Publishing database ports to the world on shared networks  
- Relying on `depends_on` without health conditions  
- Hard-coding hostpaths that only exist on one laptop

## Hands-on Lab



### Objective

Build or run a real Docker solution for **Docker Compose Fundamentals** and prove it with inspect/logs/HTTP.

### Prerequisites

- Docker Engine or Docker Desktop
- Permission to run containers

### Lab environment

Workspace: `~/rebash-docker/module-09`

Local Docker daemon. Clean up containers/images after the lab.

```bash
mkdir -p ~/rebash-docker/module-09 && cd ~/rebash-docker/module-09
```

### Real-world scenario

You are validating **Docker Compose Fundamentals** before it lands in CI. The change must be reproducible with copy-paste commands and leave no orphan containers.

### Step-by-step tasks

#### Task 1 – Write Compose file and start stack

Compose is how many teams run multi-container apps locally and in CI.

```bash
cat > compose.yaml << 'EOF'
services:
  web:
    image: nginx:alpine
    ports: ["18080:80"]
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1/"]
      interval: 5s
      retries: 5
EOF
docker compose up -d
docker compose ps
curl -sI http://127.0.0.1:18080 | head -n 5 | tee headers.txt
```

**Expected output:** Service healthy/running; headers show HTTP/1.1 200.

#### Task 2 – Inspect and stop cleanly

Always tear down Compose projects so ports and networks do not leak.

```bash
docker compose logs --tail=20 web | tee compose.log
docker compose down
test ! -z "$(cat headers.txt)"
```

**Expected output:** Logs captured; containers removed after down.

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







- [ ] Lab commands run under `~/rebash-docker/module-09/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Docker Compose Fundamentals** always combines:

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







!!! warning "Using obsolete `docker-compose` v1 behaviour docs blindly  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Publishing database ports to the world on shared networks  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Docker Compose Fundamentals changes as code and review them in pull requests
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







**Docker Compose Fundamentals** is essential for Cloud and DevOps engineers working with docker. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions




1. What problem does Compose solve locally?
2. How do you tear down including volumes?
3. Service DNS names in Compose?
4. Compose versus Swarm/Kubernetes for production?
5. How do you override config per environment?

!!! tip "Sample answer — question 2"
    Run docker compose ps and docker compose logs for the failing service.

!!! tip "Sample answer — question 4"
    Do not commit .env secrets.

## Related Tutorials







- [Course overview](index.md)
- [Container Registries and Distribution](container-registries-and-distribution.md)

## References







- [Compose specification](https://docs.docker.com/compose/compose-file/)
