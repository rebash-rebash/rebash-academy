---
title: Running Your First Container
description: Run, inspect, log into, and manage containers with docker run, ps, logs, exec, stop, and rm — hands-on fundamentals for DevOps workflows.
difficulty: beginner
estimated_time: "30 min"
author: Shaik Basha
category: docker
tags:
  - docker
  - containers
  - docker-run
  - hands-on
  - devops
prerequisites:
  - Docker Engine installed and verified
  - Completion of Module 1 Docker Foundations tutorials
  - Basic Linux command-line skills
comments: false
---

# Running Your First Container

## Overview

`docker run` is the command that turns a static image into a live process — and it is the foundation of every container workflow you will build as a DevOps engineer. Whether you are smoke-testing an image in CI, debugging a microservice locally, or reproducing a production bug, the lifecycle commands — **run**, **ps**, **logs**, **exec**, **stop**, **rm** — are your daily toolkit.

This tutorial takes you from zero to confident: run interactive and detached containers, publish ports, inspect state, stream logs, open shells inside running containers, and clean up resources without leaving orphaned processes or disk-consuming layers.

This is **Tutorial 4** in **Module 2: Images & Dockerfile** of the REBASH Academy Docker series. Complete [Module 1](../docker/index.md) first — especially [Docker Architecture and Components](docker-architecture-and-components.md). [Linux process management](../linux/index.md) and [Git](../git/index.md) skills help you interpret container behavior and version lab scripts.

## Prerequisites

- Docker Engine installed and working (`docker run hello-world` succeeds)
- User in the `docker` group or sudo access
- Completion of [Docker Installation and Setup](docker-installation-and-setup.md) and [Docker Architecture and Components](docker-architecture-and-components.md)
- Familiarity with [Introduction to Linux](../linux/introduction-to-linux.md) — processes, signals, and basic networking
- Port 8080 available on your lab host (or adjust examples)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Run containers in foreground (interactive) and background (detached) modes
- [ ] List running and stopped containers with `docker ps` and filter output
- [ ] Publish host ports to expose container services
- [ ] Stream and tail container logs with `docker logs`
- [ ] Execute commands inside running containers with `docker exec`
- [ ] Stop and remove containers gracefully using signals and flags
- [ ] Apply restart policies and name containers for operational clarity
- [ ] Clean up lab containers and avoid common resource leaks

## Architecture Diagram

A single `docker run` creates a container with an isolated process tree, optional port mapping, and captured stdout/stderr streams.

```mermaid
flowchart LR
    HOST["Host :8080"]
    BRIDGE[docker0 bridge]
    CONT["Container<br/>nginx :80"]
    LOGS["json-file logs<br/>/var/lib/docker"]

    HOST -->|NAT publish| BRIDGE
    BRIDGE --> CONT
    CONT -->|stdout/stderr| LOGS```

## Theory

### docker run Anatomy

`docker run` combines **create** and **start** in one command. Equivalent two-step form:

```bash
docker create --name myapp nginx:alpine
docker start myapp
```

Key flags you will use daily:

| Flag | Long form | Purpose |
|------|-----------|---------|
| `-d` | `--detach` | Run in background |
| `-it` | `--interactive --tty` | Interactive shell session |
| `--name` | | Human-readable container name |
| `-p` | `--publish` | Map host port to container port |
| `-e` | `--env` | Set environment variable |
| `--rm` | | Auto-remove container on exit |
| `--restart` | | Restart policy (no, on-failure, always, unless-stopped) |
| `-v` | `--volume` | Mount host path or named volume |
| `--network` | | Attach to custom network |

**Image pull behavior:** If the image is not local, Docker pulls it from the configured registry (default: Docker Hub) before creating the container.

### Foreground vs Detached Mode

| Mode | Flags | Behavior | Use case |
|------|-------|----------|----------|
| **Foreground** | (default) | Blocks terminal; logs to stdout | Quick tests, debugging |
| **Detached** | `-d` | Returns container ID; runs in background | Servers, long-running services |
| **Interactive** | `-it` | Allocates TTY + stdin | Shells, REPLs, installers |

Combine `-dit` for a detached container that still has a TTY available for later `docker exec`.

### Container Lifecycle States

```mermaid
stateDiagram-v2
    [*] --> Created: docker create
    Created --> Running: docker start / docker run
    Running --> Paused: docker pause
    Paused --> Running: docker unpause
    Running --> Stopped: docker stop / exit
    Stopped --> Running: docker start
    Stopped --> Removed: docker rm
    Running --> Removed: docker rm -f```

| State | Description |
|-------|-------------|
| **created** | Container exists but process not started |
| **running** | Main process is active |
| **paused** | Process frozen (cgroups freezer) |
| **exited** | Process terminated; container remains until removed |
| **dead** | Unrecoverable state (rare; indicates runtime issue) |

### Port Publishing

Containers on the default bridge network get private IPs (e.g., `172.17.0.2`). External access requires **port publishing**:

```bash
docker run -p 8080:80 nginx:alpine
```

Format: `host_port:container_port`. Docker sets up iptables NAT rules on the host. Multiple containers cannot bind the same host port.

| Variant | Example | Meaning |
|---------|---------|---------|
| Explicit mapping | `-p 8080:80` | Host 8080 → container 80 |
| Random host port | `-p 80` | Docker picks ephemeral host port |
| Bind to interface | `-p 127.0.0.1:8080:80` | Localhost only |
| UDP | `-p 53:53/udp` | UDP port mapping |

For production, prefer reverse proxies (Traefik, nginx) or orchestrator Ingress over ad-hoc port mappings.

### Logs and stdout/stderr

Container processes write to stdout and stderr. Docker captures these streams via the configured log driver (default: **json-file**). Logs persist until the container is removed — another reason to configure log rotation in `daemon.json`.

`docker logs` reads captured output. It does not require a shell inside the container — essential when the container has no `/bin/bash`.

### docker exec vs docker attach

| Command | Behavior |
|---------|----------|
| `docker exec` | Starts **new process** inside running container (e.g., shell, debug command) |
| `docker attach` | Connects to **main process** stdin/stdout (can accidentally stop app with Ctrl+C) |

Prefer `docker exec` for debugging. Use `attach` only when you understand the implications.

### Signals and docker stop

`docker stop` sends **SIGTERM** to PID 1 inside the container, waits (default 10 seconds), then sends **SIGKILL**. Well-behaved applications trap SIGTERM and shut down cleanly.

| Command | Signal | Effect |
|---------|--------|--------|
| `docker stop` | SIGTERM → SIGKILL | Graceful shutdown with timeout |
| `docker kill` | SIGKILL (default) | Immediate termination |
| `docker kill -s HUP` | Custom signal | Reload configs (app-dependent) |

If PID 1 is a shell script that does not forward signals, graceful shutdown fails — a common production bug addressed in later Dockerfile tutorials.

### Naming, Labels, and Restart Policies

Operational teams rely on consistent naming:

```bash
docker run -d --name web-prod-01 -l env=prod -l team=platform nginx:alpine
```

Labels enable filtering: `docker ps --filter label=env=prod`. Names must be unique per host.

| Policy | Flag | Behavior |
|--------|------|----------|
| **no** | default | Never restart automatically |
| **on-failure** | `--restart on-failure:3` | Restart on non-zero exit (max retries) |
| **always** | `--restart always` | Always restart unless explicitly stopped |
| **unless-stopped** | `--restart unless-stopped` | Like always, but not after manual stop |

### Ephemeral Writable Layer

Changes inside a running container (files written to `/tmp`, packages installed with apt) live in the container's **writable layer**. When the container is removed, those changes are lost unless you use volumes. Treat containers as disposable — redeploy from image, do not mutate in place.

## Hands-on Lab

Complete all steps on your Docker host. Commands are safe for learning environments.

### Step 1 – Run an interactive container

**Command:**

```bash
docker run --rm -it alpine:3.19 sh -c 'echo "Hello from Alpine"; cat /etc/os-release | head -2'
```

**Explanation:** `--rm` removes the container on exit. `-it` allocates a TTY. `alpine:3.19` is a minimal base image ideal for labs.

**Expected output:**

```text
Hello from Alpine
NAME="Alpine Linux"
ID=alpine
```

### Step 2 – Run nginx in detached mode with port mapping

**Command:**

```bash
docker run -d --name first-web -p 8080:80 nginx:alpine
docker ps --filter name=first-web
```

**Explanation:** `-d` detaches. `-p 8080:80` maps host port 8080 to container port 80. Verify with `curl localhost:8080`.

**Expected output:**

```text
CONTAINER ID   IMAGE          STATUS         PORTS                  NAMES
abc123def456   nginx:alpine   Up 2 seconds   0.0.0.0:8080->80/tcp   first-web
```

### Step 3 – Test the published service

**Command:**

```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8080/
curl -s http://localhost:8080/ | head -5
```

**Explanation:** Confirms NAT port mapping works. HTTP 200 means nginx serves content from inside the container.

**Expected output:**

```text
HTTP 200
<!DOCTYPE html>
<html>
...
```

### Step 4 – View container logs

**Command:**

```bash
docker logs first-web
docker logs --tail 5 --timestamps first-web
```

**Explanation:** nginx access logs appear in `docker logs` because they write to stdout/stderr in the official image.

**Expected output:**

```text
/docker-entrypoint.sh: Configuration complete; ready for start up
...
127.0.0.1 - - [...] "GET / HTTP/1.1" 200 ...
```

### Step 5 – Execute commands inside the running container

**Command:**

```bash
docker exec first-web nginx -v
docker exec -it first-web sh -c 'wget -qO- localhost | head -3'
```

**Explanation:** `docker exec` runs processes in the container's namespaces without restarting it. `-it` enables interactive sessions when needed.

**Expected output:**

```text
nginx version: nginx/1.25.x
<!DOCTYPE html>
<html>
<head>
```

### Step 6 – Inspect container details

**Command:**

```bash
docker inspect first-web | grep -E '"Status"|"8080"' | head -6
docker stats first-web --no-stream
docker port first-web
```

**Explanation:** `inspect` returns full JSON metadata. `stats` shows live CPU/memory. `docker port` lists published port mappings without parsing JSON.

**Expected output:**

```text
"Status": "running",
"8080/tcp": [{ "HostPort": "8080" ...
CPU %   MEM USAGE / LIMIT   MEM %
0.00%   4MiB / 7.7GiB       0.05%
80/tcp -> 0.0.0.0:8080
```

### Step 7 – Stop and restart the container

**Command:**

```bash
docker stop first-web
docker ps -a --filter name=first-web
docker start first-web
docker ps --filter name=first-web
```

**Explanation:** `stop` sends SIGTERM. Container remains in **exited** state until removed. `start` resumes the same container — same filesystem layer, same name.

**Expected output:**

```text
first-web   Exited (0) 2 seconds ago
first-web   Up Less than a second
```

### Step 8 – Run with restart policy, then clean up

**Command:**

```bash
docker run -d --name echo-lab --restart unless-stopped \
  -e MESSAGE="REBASH Academy" \
  alpine sh -c 'while true; do echo "$MESSAGE"; sleep 10; done'
docker logs echo-lab
docker rm -f first-web echo-lab
docker ps -a --filter name=first-web
```

**Explanation:** Demonstrates restart policy and environment variables. `docker rm -f` stops and removes in one step. The nginx **image** remains cached.

**Expected output:**

```text
REBASH Academy
first-web
(no rows — containers removed)
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `docker run` | Create and start a container | `docker run -d nginx:alpine` |
| `docker ps` | List containers | `docker ps -a` |
| `docker logs` | Fetch container logs | `docker logs -f myapp` |
| `docker exec` | Run command in running container | `docker exec -it myapp sh` |
| `docker stop` | Graceful stop (SIGTERM) | `docker stop myapp` |
| `docker start` | Start stopped container | `docker start myapp` |
| `docker rm` | Remove stopped container | `docker rm myapp` |
| `docker port` | List port mappings | `docker port myapp` |
| `docker stats` | Live resource usage | `docker stats --no-stream` |
| `docker top` | List processes in container | `docker top myapp` |

### Container lifecycle helper script

Save as `~/bin/docker-lifecycle-demo.sh`:

```bash
#!/usr/bin/env bash
# docker-lifecycle-demo.sh — demonstrate run/ps/logs/exec/stop/rm workflow
set -euo pipefail

NAME="lifecycle-lab-$$"
IMAGE="nginx:alpine"
PORT="8099"

cleanup() {
  docker rm -f "$NAME" 2>/dev/null || true
}
trap cleanup EXIT

echo "=== docker run ==="
docker run -d --name "$NAME" -p "${PORT}:80" "$IMAGE"

echo "=== docker ps ==="
docker ps --filter "name=$NAME"

echo "=== curl test ==="
sleep 1
curl -s -o /dev/null -w "HTTP %{http_code}\n" "http://localhost:${PORT}/"

echo "=== docker logs (last 3 lines) ==="
docker logs --tail 3 "$NAME"

echo "=== docker exec ==="
docker exec "$NAME" nginx -v

echo "=== docker stop ==="
docker stop "$NAME"
docker ps -a --filter "name=$NAME" | grep -q Exited && echo "State: exited"

echo "=== docker rm ==="
docker rm "$NAME"
trap - EXIT
echo "Done — container removed"
```

Make executable: `chmod +x ~/bin/docker-lifecycle-demo.sh && ~/bin/docker-lifecycle-demo.sh`

## Common Mistakes

!!! warning "Using docker run without --rm for one-off tasks"
    Ephemeral test containers accumulate in `docker ps -a` and consume disk. Use `--rm` for CI jobs and quick tests.

!!! warning "Binding privileged ports without understanding impact"
    `-p 80:80` requires root or `CAP_NET_BIND_SERVICE` on the host. Use high ports (8080) in dev; use load balancers in prod.

!!! warning "Running docker attach and pressing Ctrl+C"
    Ctrl+C sends SIGINT to the **main process**, potentially killing your application. Use `docker exec` for debugging.

!!! warning "Assuming docker stop always succeeds in 10 seconds"
    Stuck processes need `--time` adjustment or investigation. Java apps and shell-wrapped PID 1 scripts often ignore SIGTERM.

## Best Practices

!!! tip "Name containers meaningfully in shared environments"
    Use names like `payment-api-staging-01` instead of random strings. Names appear in logs, monitoring, and incident tickets.

!!! tip "Always set restart policy for long-running services"
    `--restart unless-stopped` survives daemon restarts on single-host deployments. Kubernetes replaces this with pod restart policies.

!!! tip "Use docker logs -f during development, centralized logging in production"
    `-f` follows logs locally. Production ships logs to ELK, Loki, or CloudWatch via log drivers or sidecars.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `port is already allocated` | Another process uses host port | Change host port or stop conflicting container |
| `Unable to find image locally` then slow start | Normal first-time pull | Wait for pull; pre-pull in CI with `docker pull` |
| Empty `docker logs` output | App logs to file inside container | Exec in and check paths; fix app to log to stdout |
| `Error response from daemon: container already exists` | Duplicate `--name` | Remove old container or choose new name |
| `OCI runtime create failed` | Invalid mount, missing binary, or bad flag | Check `docker logs` and run `docker inspect` |
| Cannot curl published port | Wrong mapping or firewall | Verify PORTS column; check `ufw`/security groups |

## Summary

- **`docker run`** creates and starts containers; combine flags for detached (`-d`), interactive (`-it`), port publish (`-p`), and auto-remove (`--rm`) behavior
- **`docker ps`** lists containers; `-a` includes stopped; filters narrow by name, status, and labels
- **`docker logs`** reads stdout/stderr; **`docker exec`** runs new processes inside running containers
- **`docker stop`** gracefully terminates with SIGTERM; **`docker rm`** removes stopped containers and their writable layers
- Port publishing maps host ports to container services via NAT on the bridge network
- Next: understand the images behind your containers in [Working with Docker Images](working-with-docker-images.md)

## Interview Questions

1. What is the difference between `docker run` and `docker start`?
2. Explain foreground vs detached container execution.
3. How does port publishing work with `-p 8080:80`?
4. What is the difference between `docker exec` and `docker attach`?
5. What signals does `docker stop` send, and in what order?
6. Why should applications log to stdout instead of files inside containers?
7. What happens to container data when you `docker rm` a container?
8. What does the `--restart unless-stopped` policy do?
9. How do you view only running containers vs all containers including exited ones?
10. Why is `--rm` recommended for CI pipeline containers?

??? tip "Sample Answers (Questions 3, 5, and 7)"

    **Q3 — Port publishing:** The `-p 8080:80` flag tells dockerd to listen on port 8080 on the host and forward TCP traffic via iptables NAT to port 80 on the container's IP on the docker bridge network. Clients connect to `host:8080`; Docker routes to `container_ip:80`.

    **Q5 — docker stop signals:** docker stop first sends SIGTERM to PID 1 inside the container, allowing graceful shutdown. If the process has not exited within the grace period (default 10 seconds), Docker sends SIGKILL to force termination.

    **Q7 — Data after docker rm:** Removing a container deletes its writable layer — any changes made inside the container that were not stored in a volume or bind mount are lost. Named volumes and the underlying image layers survive. This is why stateful data belongs in volumes, not container filesystems.

## Related Tutorials

- [Docker – Category Overview](index.md)
- [Docker Architecture and Components](docker-architecture-and-components.md) *(Module 1)*
- [Working with Docker Images](working-with-docker-images.md) *(next in Module 2)*
- [Introduction to Linux](../linux/introduction-to-linux.md)
- [Introduction to Git and Version Control](../git/introduction-to-git-and-version-control.md)

## References

- [Docker run reference](https://docs.docker.com/engine/reference/run/)
- [docker ps reference](https://docs.docker.com/engine/reference/commandline/ps/)
- [docker logs reference](https://docs.docker.com/engine/reference/commandline/logs/)
- [docker exec reference](https://docs.docker.com/engine/reference/commandline/exec/)
- [REBASH Academy – Linux Overview](../linux/index.md)
- [REBASH Academy – Git Overview](../git/index.md)
