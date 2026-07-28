---
title: Docker Architecture and Components
description: Understand Docker client-daemon communication, containerd, runc, image layers, and how components interact in a production container stack.
difficulty: beginner
estimated_time: "35 min"
author: Shaik Basha
category: docker
tags:
  - docker
  - architecture
  - containerd
  - runc
  - devops
prerequisites:
  - Docker Engine installed and verified
  - Completion of Docker Installation and Setup
  - Basic Linux process and filesystem knowledge
comments: false
---

# Docker Architecture and Components

## Overview

When a developer runs `docker run nginx`, a surprising amount happens beneath the CLI output: the **client** sends an API request to **dockerd**, which delegates image management to **containerd**, which invokes **runc** to create an isolated process with namespaces and cgroups. Production incidents — stuck containers, orphaned processes, socket permission failures — make sense only when you understand this stack.

This tutorial maps Docker's **architecture and components**: the client-daemon model, **containerd** and **runc** roles, image layering and storage drivers, networking and volume plugins, and how this design aligns with Kubernetes' **CRI (Container Runtime Interface)**.

This is **Tutorial 3** in **Module 1: Foundations** of the REBASH Academy Docker series. Complete [Docker Installation and Setup](docker-installation-and-setup.md) first. [Linux process and filesystem](../linux/index.md) knowledge helps you interpret what runc creates on the host.

## Prerequisites

- Docker Engine installed and verified (`docker run hello-world` succeeds)
- Non-root or sudo access to Docker on a Linux host
- Completion of [Introduction to Containers and Docker](introduction-to-containers-and-docker.md) and [Docker Installation and Setup](docker-installation-and-setup.md)
- Familiarity with [Introduction to Linux](../linux/introduction-to-linux.md) — processes, systemd, and `/proc`
- Optional: [Introduction to Networking](../networking/introduction-to-networking.md) for bridge network concepts

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Diagram the Docker client, daemon, containerd, and runc interaction
- [ ] Explain how the Docker REST API and Unix socket enable CLI and remote operations
- [ ] Describe containerd's role vs dockerd's role in the container lifecycle
- [ ] Identify how runc creates the actual container process using OCI specs
- [ ] Explain image layers, overlay2 storage, and copy-on-write semantics
- [ ] Relate Docker components to Kubernetes CRI and alternative runtimes (CRI-O, Podman)
- [ ] Use inspection commands to trace component behavior on a live host

## Architecture Diagram

The full stack from user command to running process. Kubernetes often bypasses dockerd and talks directly to containerd via CRI — but the lower layers remain the same.

```d2
direction: down

USER_LAYER: "User Layer" {
      style: {
        fill: "#e3f2fd"
        stroke: "#1976d2"
      }
        CLI: "Docker CLI"
        COMPOSE: "Docker Compose"
        SDK: "Docker SDK / API clients"
    }
    ENGINE: "Docker Engine" {
      style: {
        fill: "#e8f5e9"
        stroke: "#388e3c"
      }
        DOCKERD: "dockerd\\nAPI · images · networks · volumes"
    }
    RUNTIME: "Container Runtime" {
      style: {
        fill: "#fff3e0"
        stroke: "#ef6c00"
      }
        CONTAINERD: "containerd\\nimage pull · snapshot · task"
        SHIM: containerd-shim
        RUNC: "runc\\nOCI runtime"
    }
    KERNEL: "Linux Kernel" {
      style: {
        fill: "#f3e5f5"
        stroke: "#7b1fa2"
      }
        NS: Namespaces
        CG: cgroups
        OFS: OverlayFS
    }
    CONT: "Running Container"
    USER_LAYER.CLI -> ENGINE.DOCKERD
    USER_LAYER.COMPOSE -> ENGINE.DOCKERD
    USER_LAYER.SDK -> ENGINE.DOCKERD
    ENGINE.DOCKERD -> RUNTIME.CONTAINERD
    RUNTIME.CONTAINERD -> RUNTIME.SHIM
    RUNTIME.SHIM -> RUNTIME.RUNC
    RUNTIME.RUNC -> KERNEL.NS
    RUNTIME.RUNC -> KERNEL.CG
    RUNTIME.RUNC -> KERNEL.OFS
    RUNTIME.RUNC -> CONT
```

## Theory

### Client-Daemon Architecture

Docker uses a **client-server** model:

| Component | Binary | Role |
|-----------|--------|------|
| **Client** | `docker` | Sends commands; can run on a different host than the daemon |
| **Daemon** | `dockerd` | Long-running background service managing containers, images, networks, volumes |
| **Socket** | `/var/run/docker.sock` | Unix domain socket for local communication; TCP for remote (TLS required) |

The client does not run containers directly. It serializes requests to the Docker Engine API (REST over HTTP). This is why `DOCKER_HOST=ssh://user@host docker ps` works — the CLI is just an API consumer.

Common API consumers beyond the CLI:

- **Docker Compose** — orchestrates multi-container applications
- **CI/CD plugins** — Jenkins, GitLab Runner, GitHub Actions docker actions
- **Portainer, Lazydocker** — GUI management tools
- **Terraform docker provider** — infrastructure-as-code for containers

### dockerd Responsibilities

**dockerd** is the high-level manager:

- **Images** — build, tag, pull, push (delegates storage to containerd)
- **Containers** — create, start, stop, remove (via containerd)
- **Networks** — bridge, host, overlay, macvlan, none
- **Volumes** — named volumes, bind mounts
- **Plugins** — logging, authorization, volume drivers
- **Swarm mode** — clustering (legacy; Kubernetes dominates orchestration)

When you `docker build`, dockerd (with BuildKit) handles the build pipeline. When you `docker run`, dockerd translates the request into containerd operations.

### containerd — The Industry-Standard Runtime

**containerd** graduated from CNCF in 2019 and is the runtime Docker uses under the hood. It handles:

- **Image distribution** — pull, push, unpack layers
- **Snapshots** — filesystem mounts for containers
- **Task management** — create, start, kill container processes
- **Content store** — blob storage for image layers

containerd exposes a gRPC API. Kubernetes' **kubelet** can call containerd directly through **CRI**, skipping dockerd entirely — this is the default on modern Kubernetes (Docker shim removed since v1.24).

Why containerd exists as a separate layer:

- **Separation of concerns** — dockerd focuses on developer UX; containerd focuses on runtime correctness
- **Shared runtime** — Kubernetes, Docker, and other tools reuse containerd
- **Smaller attack surface** — production nodes run containerd without full Docker Engine

### runc — The OCI Runtime

**runc** is a lightweight CLI that implements the **OCI Runtime Specification**. For each container start:

1. Reads an **OCI bundle** — `config.json` describing namespaces, mounts, cgroups, capabilities
2. Calls Linux primitives to create namespaces and apply cgroup limits
3. Executes the container's entrypoint process (PID 1 inside the container)
4. Exits after start — ongoing supervision is handled by **containerd-shim**

runc is intentionally minimal. It does not manage images or networks — only the process sandbox.

Other OCI runtimes:

| Runtime | Notes |
|---------|-------|
| **runc** | Default; mature, widely tested |
| **crun** | C implementation; fast, used by Podman/CRI-O |
| **kata-runtime** | Lightweight VMs for stronger isolation |

### Image Layers and Storage

Docker images are **stacked read-only layers** plus a **writable container layer**:

```d2
direction: up

RW: "Container Layer\\nread-write · ephemeral"
    L3: "Layer 3 — app code"
    L2: "Layer 2 — dependencies"
    L1: "Layer 1 — base OS"
    RW -> L3
    L3 -> L2
    L2 -> L1
```

| Concept | Description |
|---------|-------------|
| **Layer** | Result of a Dockerfile instruction (`RUN`, `COPY`); cached for rebuild speed |
| **Image** | Ordered stack of layers with metadata (env, cmd, exposed ports) |
| **Container** | Image + writable layer; deleted when container is removed (unless committed) |
| **Storage driver** | Maps layers to disk — **overlay2** on modern Linux |

**Overlay2** merges lower read-only layers with an upper writable layer using OverlayFS. Multiple containers sharing the same base image reuse lower layers — saving disk and memory.

### Networking and Volume Components

dockerd manages pluggable subsystems:

**Networking drivers:**

| Driver | Use case |
|--------|----------|
| **bridge** | Default; isolated network with NAT to host |
| **host** | Container shares host network namespace |
| **none** | No networking |
| **overlay** | Multi-host networking (Swarm) |
| **macvlan** | Container gets MAC address on physical network |

**Volume drivers:**

- **local** — default; stored under `/var/lib/docker/volumes/`
- **NFS, cloud plugins** — persistent storage backends for stateful workloads

We cover networking and volumes in depth in Modules 3 and 4.

### Docker vs Kubernetes Runtime Path

| Path | Flow |
|------|------|
| **Docker CLI** | `docker` → dockerd → containerd → runc |
| **Kubernetes (containerd)** | kubelet → CRI → containerd → runc |
| **Podman** | `podman` → libpod → crun/runc (daemonless) |

Understanding this explains why "Docker was removed from Kubernetes" — Kubernetes never needed dockerd; it needed containerd (or CRI-O). Docker images and Dockerfiles remain universal; only the runtime path changed.

### BuildKit

Modern Docker builds use **BuildKit** (default since Docker 23): parallel stages, cache export/import, multi-platform builds, and secret mounts. `docker buildx` is the CLI interface — covered in later Dockerfile tutorials.

## Hands-on Lab

Explore live component behavior on your Docker host. All commands assume Docker is installed from the previous tutorial.

### Step 1 – Inspect client and server versions

**Command:**

```bash
docker version
docker context ls
```

**Explanation:** Shows client/server version split — they can differ during upgrades. Context defines which daemon the CLI targets.

**Expected output:**

```text
Client: Docker Engine - Community
 Server: Docker Engine - Community
...
default *   unix:///var/run/docker.sock
```

### Step 2 – Examine running processes

**Command:**

```bash
ps aux | grep -E 'dockerd|containerd' | grep -v grep
systemctl status containerd --no-pager | head -10
```

**Explanation:** Both dockerd and containerd run as systemd services. containerd often starts before dockerd.

**Expected output:**

```text
root  ... /usr/bin/containerd
root  ... /usr/bin/dockerd -H fd:// ...
```

### Step 3 – Start a container and trace processes

**Command:**

```bash
docker run -d --name arch-lab nginx:alpine
sleep 2
pstree -p $(pgrep -f 'containerd-shim.*arch-lab' | head -1) 2>/dev/null || \
  ps aux | grep -E 'arch-lab|nginx' | grep -v grep
```

**Explanation:** Each container has a **containerd-shim** parent process. Inside the container, nginx runs as PID 1 in its PID namespace.

**Expected output:**

```text
containerd-shim(12345)───nginx(12346)
```

### Step 4 – Inspect container runtime metadata

**Command:**

```bash
docker inspect arch-lab | grep -A8 '"GraphDriver"'
```

**Explanation:** GraphDriver shows overlay2. The `MergedDir` field is the unified filesystem view the container sees — useful for debugging storage issues.

**Expected output:**

```text
"GraphDriver": {
    "Data": {
        "MergedDir": "/var/lib/docker/overlay2/.../merged",
        ...
    },
    "Name": "overlay2"
}
```

### Step 5 – Explore image layers

**Command:**

```bash
docker image inspect nginx:alpine | grep -A20 RootFS
docker history nginx:alpine --no-trunc | head -8
```

**Explanation:** `RootFS.Layers` lists content-addressable layer hashes. `docker history` maps layers to Dockerfile-equivalent steps.

**Expected output:**

```text
"Layers": [
    "sha256:abc123...",
    "sha256:def456..."
]
```

### Step 6 – Inspect the Docker socket

**Command:**

```bash
ls -la /var/run/docker.sock
curl --unix-socket /var/run/docker.sock http://localhost/version 2>/dev/null | head -c 200
echo
```

**Explanation:** The socket is the API endpoint. `curl --unix-socket` demonstrates that Docker is REST-based — tools integrate without the CLI.

**Expected output:**

```text
srw-rw---- 1 root docker /var/run/docker.sock
{"Platform":{...},"Version":"27.x.x",...}
```

### Step 7 – Check containerd namespaces

**Command:**

```bash
sudo ctr -n moby containers list 2>/dev/null | head -5 || \
  echo "ctr requires root; containerd namespace 'moby' used by Docker"
```

**Explanation:** Docker stores containers in containerd's `moby` namespace. `ctr` is containerd's low-level CLI — useful for advanced debugging.

**Expected output:**

```text
CONTAINER   IMAGE   RUNTIME
...
```

### Step 8 – Clean up lab container

**Command:**

```bash
docker stop arch-lab && docker rm arch-lab
```

**Explanation:** Remove lab resources. The nginx image remains cached for future tutorials.

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `docker version` | Client and server version info | `docker version` |
| `docker info` | System-wide configuration summary | `docker info` |
| `docker inspect` | Detailed object metadata (JSON) | `docker inspect nginx:alpine` |
| `docker history` | Show image layer history | `docker history nginx:alpine` |
| `docker context ls` | List CLI contexts (daemon targets) | `docker context ls` |
| `ctr containers list` | containerd container list (root) | `sudo ctr -n moby containers list` |
| `journalctl -u dockerd` | dockerd service logs | `journalctl -u docker -n 30` |

### Architecture inspection script

Save as `~/bin/docker-arch-inspect.sh`:

```bash
#!/usr/bin/env bash
# docker-arch-inspect.sh — summarize Docker component stack on this host
set -euo pipefail

section() { printf '\n=== %s ===\n' "$1"; }

section "Versions"
docker version 2>/dev/null | grep -E "Version|API version" | head -6

section "Storage Driver"
docker info 2>/dev/null | grep -E "Storage Driver|Logging Driver|Cgroup"

section "Runtime Processes"
ps aux | grep -E 'dockerd|containerd' | grep -v grep | awk '{print $11, $2}'

section "Socket Permissions"
ls -la /var/run/docker.sock 2>/dev/null || echo "Socket not found"

section "Sample Container Tree"
CID=$(docker ps -q | head -1)
if [ -n "$CID" ]; then
  NAME=$(docker ps --filter "id=$CID" --no-trunc | tail -1 | awk '{print $NF}')
  echo "Inspecting: $NAME"
  docker top "$CID"
else
  echo "No running containers — start one with: docker run -d nginx:alpine"
fi
```

Make executable: `chmod +x ~/bin/docker-arch-inspect.sh`

## Common Mistakes

!!! warning "Assuming docker CLI runs containers directly"
    The CLI is an API client. Debugging "Docker is slow" often means inspecting dockerd, containerd, or disk I/O — not reinstalling the CLI.

!!! warning "Confusing dockerd with containerd"
    Restarting containerd affects all containers dockerd manages. On Kubernetes nodes, restarting containerd affects all pods on that node. Plan maintenance windows accordingly.

!!! warning "Ignoring storage driver on non-Linux platforms"
    overlay2 is Linux-specific. Docker Desktop on macOS uses a VM with Linux inside. Production patterns always target Linux hosts.

!!! warning "Using docker inspect format strings in CI docs without escaping"
    Go templates use curly-brace syntax that conflicts with Jinja2/MkDocs. Use grep, JSON parsing, or raw blocks in documentation pipelines.

## Best Practices

!!! tip "Know the CRI path for Kubernetes interviews"
    Modern clusters: kubelet → containerd → runc. Docker Engine is optional for **building** images in CI, not required on worker nodes.

!!! tip "Use docker info as first diagnostic command"
    Storage driver, cgroup version, and root directory appear in one output — faster than guessing from symptoms.

!!! tip "Monitor containerd and dockerd with systemd"
    Alert on `systemctl is-active docker` and `containerd` failures. Node NotReady events often trace to runtime issues.

!!! tip "Version-control daemon.json in Git"
    Track `/etc/docker/daemon.json` changes in [Git](../git/index.md) with the same rigor as application code.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Client/server version mismatch | Partial upgrade | Upgrade both docker-ce and docker-ce-cli together |
| containerd not running | Service crash or failed boot | `systemctl restart containerd`; check logs |
| Orphan shim processes | Container killed uncleanly | Restart containerd/dockerd; investigate OOM kills |
| overlay2 errors | Full disk or inode exhaustion | `df -h` and `df -i` on `/var/lib/docker` |
| API permission denied | User not in docker group | Add to group or use sudo |
| ctr shows no containers | Wrong namespace | Docker uses `-n moby` namespace |

## Summary

- Docker uses a **client-daemon** model: CLI sends REST API requests to **dockerd** via Unix socket or TCP
- **dockerd** manages developer-facing features; **containerd** handles image storage and task lifecycle; **runc** creates OCI-compliant processes
- **containerd-shim** supervises container processes after runc exits
- Images are **layered** and stored with **overlay2**; containers add an ephemeral writable layer
- Kubernetes talks to **containerd via CRI**, not dockerd — but runc and OCI images remain central
- Next: put architecture knowledge into practice with [Running Your First Container](running-your-first-container.md)

## Interview Questions

1. Describe the flow when a user runs `docker run nginx`.
2. What is the difference between dockerd and containerd?
3. What role does runc play in the container stack?
4. What is the OCI Runtime Specification?
5. Explain image layers and the copy-on-write model.
6. Why was Docker shim removed from Kubernetes?
7. What is stored at `/var/run/docker.sock`?
8. What is BuildKit, and how does it differ from legacy docker build?
9. Name two OCI runtimes other than runc.
10. How would you identify the parent process of a running container on the host?

??? tip "Sample Answers (Questions 1, 6, and 7)"

    **Q1 — docker run flow:** The Docker CLI sends a create-and-start request to dockerd. dockerd pulls the image via containerd if missing, prepares a snapshot filesystem, generates an OCI spec, and asks containerd to create a task. containerd invokes runc to set up namespaces, cgroups, and mounts, then starts the container process. containerd-shim supervises the process; dockerd records container metadata for CLI commands like `docker ps`.

    **Q6 — Kubernetes Docker shim removal:** Kubernetes only needed a container runtime implementing CRI — containerd or CRI-O. dockerd was an unnecessary middle layer on worker nodes, adding complexity and an extra daemon to patch. Docker **images and Dockerfiles** remain fully supported; only the runtime on nodes changed. CI systems still use Docker to build images.

    **Q7 — Docker socket:** `/var/run/docker.sock` is a Unix domain socket exposing the Docker Engine HTTP API locally. Clients (CLI, Compose, CI plugins) connect here to manage containers, images, and networks. Access equals root-level control over the host.

## Related Tutorials

- [Docker – Category Overview](index.md)
- [Docker Installation and Setup](docker-installation-and-setup.md) *(previous in Module 1)*
- [Running Your First Container](running-your-first-container.md) *(first in Module 2)*
- [Introduction to Linux](../linux/introduction-to-linux.md)

## References

- [Docker architecture overview](https://docs.docker.com/get-started/docker-overview/#docker-architecture)
- [containerd documentation](https://containerd.io/docs/)
- [OCI Runtime Specification](https://github.com/opencontainers/runtime-spec)
- [Kubernetes CRI](https://kubernetes.io/docs/concepts/architecture/cri/)
- [REBASH Academy – Linux Overview](../linux/index.md)
- [REBASH Academy – Git Overview](../git/index.md)
