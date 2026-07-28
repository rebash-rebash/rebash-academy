---
title: Introduction to Containers and Docker
description: Understand containers vs virtual machines, why Docker became the industry standard, and how containerization fits into modern DevOps workflows.
difficulty: beginner
estimated_time: "30 min"
author: Shaik Basha
category: docker
tags:
  - docker
  - containers
  - fundamentals
  - devops
  - virtualization
prerequisites:
  - Basic computer literacy and comfort using a terminal
  - Completion of or concurrent study of the Linux Foundations track
  - Familiarity with basic networking concepts
comments: false
---

# Introduction to Containers and Docker

## Overview

Every modern deployment pipeline — from a startup's CI/CD workflow to a bank's Kubernetes cluster — runs on **containers**. When a developer says "it works on my machine," containers are the industry answer: package the application, its dependencies, and runtime into a portable unit that behaves the same on a laptop, a CI runner, and a production server. When an SRE scales a microservice from 2 to 200 replicas, containers provide the atomic unit of deployment.

This tutorial establishes your mental model: what **containers** are, how they differ from **virtual machines**, why **Docker** became the de facto standard, and where containerization fits in the DevOps toolchain alongside Linux, Git, and Kubernetes.

This is **Tutorial 1** in **Module 1: Foundations** of the REBASH Academy Docker series. We recommend completing the [Linux Foundations track](../linux/index.md) first — containers are built on Linux kernel features like namespaces and cgroups. Basic [Git](../git/index.md) skills help you version Dockerfiles and Compose files in later tutorials. This tutorial follows our [documentation standards](../about.md#documentation-standards).

## Prerequisites

- Basic computer literacy and comfort typing commands in a terminal
- A Linux environment: Ubuntu VM, WSL2, or a free-tier cloud instance (AWS, GCP, Azure)
- Familiarity with the [Introduction to Linux](../linux/introduction-to-linux.md) tutorial — especially processes, filesystems, and package management
- Basic understanding of [Introduction to Networking](../networking/introduction-to-networking.md) — ports and client-server concepts
- No prior Docker or container experience required — this tutorial starts from zero

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain what a container is and how it differs from a virtual machine
- [ ] Describe the problems containers solve: portability, dependency isolation, and resource efficiency
- [ ] Articulate why Docker became the dominant container platform for DevOps
- [ ] Identify the core components of the container ecosystem: images, containers, registries, and orchestrators
- [ ] Relate containers to Linux kernel features: namespaces, cgroups, and union filesystems
- [ ] Map containerization to CI/CD, microservices, and cloud-native architecture patterns
- [ ] Recognize when containers are the right tool — and when VMs or bare metal still apply

## Architecture Diagram

The diagram below contrasts virtual machines and containers at the infrastructure layer. Understanding this distinction explains why containers start in seconds, use less memory, and share the host kernel — and why VMs still matter for strong isolation and multi-OS workloads.

```d2
direction: down

VM: "Virtual Machine Stack" {
      style: {
        fill: "#e3f2fd"
        stroke: "#1976d2"
      }
        APP_VM: Application
        OS_GUEST: "Guest OS — full kernel"
        HYP: "Hypervisor — KVM / VMware / Hyper-V"
        HOST_OS_VM: "Host OS"
        HW_VM: "Physical Hardware"
        APP_VM -> OS_GUEST
        OS_GUEST -> HYP
        HYP -> HOST_OS_VM
        HOST_OS_VM -> HW_VM
    }
    CONTAINER: "Container Stack" {
      style: {
        fill: "#e8f5e9"
        stroke: "#388e3c"
      }
        APP_C1: "App Container A"
        APP_C2: "App Container B"
        ENGINE: "Container Engine — Docker / containerd"
        HOST_OS_C: "Host OS — shared kernel"
        HW_C: "Physical Hardware"
        APP_C1 -> ENGINE
        APP_C2 -> ENGINE
        ENGINE -> HOST_OS_C
        HOST_OS_C -> HW_C
    }
```

## Theory

### Why Containers Matter for DevOps

Before containers, deploying software meant SSH-ing into servers, installing dependencies by hand, and hoping staging matched production. Configuration drift was the norm. Rollbacks meant restoring entire VMs from snapshots. Scaling meant provisioning new virtual machines — a process measured in minutes, not seconds.

Containers change the deployment unit from **a server** to **an application process with its filesystem**. DevOps engineers rely on containers to:

- **Achieve environment parity** — the same image runs on a developer laptop, CI runner, and production cluster
- **Accelerate CI/CD pipelines** — build once, push to a registry, deploy anywhere
- **Improve resource utilization** — run dozens of services on hardware that previously hosted a handful of VMs
- **Enable microservices** — isolate services with independent release cycles and scaling policies
- **Standardize operations** — one tooling model (`docker run`, health checks, logs) across languages and frameworks
- **Bridge to orchestration** — Kubernetes, ECS, and Nomad all schedule container images

If you deploy software to production in 2026, you will encounter containers. Docker is the most common entry point.

### The Problem Containers Solve

| Problem without containers | How containers solve it |
|----------------------------|---------------------------|
| "Works on my machine" | Image bundles app + dependencies + config; identical everywhere |
| Dependency conflicts on shared servers | Each container has isolated filesystem and process space |
| Slow, heavy VM provisioning | Containers start in seconds; no guest OS boot |
| Inconsistent deploy scripts | Dockerfile is version-controlled, repeatable build recipe |
| Difficult rollbacks | Redeploy previous image tag in seconds |
| Wasted server capacity | Pack many lightweight workloads on one host |

### Containers vs Virtual Machines

Both containers and VMs provide **isolation**, but they achieve it at different layers of the stack.

| Aspect | Virtual Machine | Container |
|--------|-----------------|-----------|
| **Isolation unit** | Entire virtual hardware + guest OS | Process + filesystem namespace |
| **Kernel** | Each VM runs its own kernel | All containers share the host kernel |
| **Startup time** | 30 seconds to several minutes | Sub-second to a few seconds |
| **Size** | Gigabytes (full OS image) | Megabytes to low gigabytes |
| **Density** | 10–50 VMs per host (typical) | 100–1000+ containers per host |
| **OS flexibility** | Run Windows, Linux, BSD on same host | Linux containers on Linux; Windows containers on Windows |
| **Security boundary** | Strong — hypervisor + separate kernel | Weaker — shared kernel; requires hardening |
| **Use case** | Multi-tenant isolation, legacy apps, different OSes | Microservices, CI/CD, cloud-native apps |

**Key insight:** Containers are not "lightweight VMs." They are **isolated processes** on a shared kernel, made possible by Linux features that have existed since the early 2000s but were democratized by Docker's tooling.

### Linux Kernel Foundations

Containers are not magic — they are a clever composition of existing Linux primitives:

#### Namespaces

**Namespaces** isolate kernel resources so a process sees its own view of the system:

| Namespace | Isolates |
|-----------|----------|
| **PID** | Process IDs — container sees PID 1 as its init |
| **NET** | Network interfaces, routes, firewall rules |
| **MNT** | Mount points and filesystem tree |
| **UTS** | Hostname and domain name |
| **IPC** | Inter-process communication |
| **USER** | User and group IDs (root in container ≠ root on host) |

#### Control Groups (cgroups)

**cgroups** limit and account for resource usage — CPU, memory, disk I/O, and network bandwidth. Without cgroups, a runaway container could consume all host memory. Kubernetes pod resource requests and limits map directly to cgroup settings.

#### Union Filesystems

**Union filesystems** (OverlayFS, aufs) layer read-only image layers with a writable container layer. Multiple containers share the same base image layers on disk — saving storage and speeding up pulls. This layering model is central to Docker images.

### What Is Docker?

**Docker** is a platform for building, shipping, and running containers. Created by Solomon Hykes and released in 2013, Docker did not invent containers (LXC existed since 2008), but it made them accessible through:

- **Dockerfile** — a declarative, version-controlled build recipe
- **Docker CLI** — simple commands: `build`, `run`, `push`, `pull`
- **Docker Hub** — a public registry that solved the "how do I share images?" problem
- **Image format (OCI)** — standardized packaging that works across tools and clouds

Today, Docker Inc. maintains Docker Desktop and Docker Engine, while the **Open Container Initiative (OCI)** governs open standards for images and runtimes.

### The Container Ecosystem

```d2
direction: right

DEV: Developer
    DF: Dockerfile
    BUILD: "docker build"
    IMG: Image
    REG: "Registry\\nDocker Hub / ECR / GCR"
    RUN: "docker run"
    CONT: Container
    ORCH: "Orchestrator\\nKubernetes / ECS"
    DEV -> DF
    DF -> BUILD
    BUILD -> IMG
    IMG -> REG
    REG -> RUN
    RUN -> CONT
    CONT -> ORCH
```

| Component | Role | Examples |
|-----------|------|----------|
| **Dockerfile** | Build instructions for an image | `FROM`, `RUN`, `COPY`, `CMD` |
| **Image** | Immutable, layered filesystem snapshot | `nginx:1.25`, `python:3.12-slim` |
| **Container** | Running instance of an image | Your app's live process |
| **Registry** | Image storage and distribution | Docker Hub, Amazon ECR, Google GAR |
| **Orchestrator** | Schedule, scale, and heal containers | Kubernetes, Docker Swarm, ECS |
| **Runtime** | Low-level container execution | runc, containerd, CRI-O |

### Containers in the DevOps Toolchain

Containers sit at the center of modern DevOps workflows:

- **Version control (Git)** — Dockerfiles, Compose files, and Helm charts live in repositories; every image tag traces to a commit SHA
- **CI/CD** — pipelines build images, scan for vulnerabilities, push to registries, and trigger deployments
- **Infrastructure as Code** — Terraform provisions ECR repos; Ansible configures Docker hosts
- **Observability** — Prometheus scrapes container metrics; Fluentd collects container logs
- **Security** — Trivy and Grype scan images; admission controllers block vulnerable tags

Learning containers after [Linux](../linux/index.md) and [Git](../git/index.md) follows the natural DevOps progression: understand the OS, version your config, then package and deploy applications.

### When to Use Containers vs VMs

| Scenario | Recommendation |
|----------|----------------|
| Microservices, APIs, web apps | Containers |
| CI/CD build agents | Containers |
| Batch jobs and data pipelines | Containers |
| Strong multi-tenant isolation (untrusted workloads) | VMs or dedicated bare metal |
| Windows + Linux on same host | VMs (or separate container hosts per OS) |
| Legacy monolith with complex OS dependencies | VM first; containerize incrementally |
| Stateful databases (production) | Often VMs or managed services; containers with care |

Most organizations use **both**: VMs as the host layer, containers as the application layer.

## Hands-on Lab

These steps explore container-related concepts on your Linux system without requiring Docker to be installed yet. If you want a running engine immediately, proceed to [Docker Installation and Setup](docker-installation-and-setup.md) after this lab.

### Step 1 – Confirm Linux kernel version

**Command:**

```bash
uname -r
uname -m
```

**Explanation:** Containers require a modern Linux kernel (3.10+ for basic features; 4.x+ recommended). The architecture (`x86_64`, `aarch64`) determines which pre-built images you can run.

**Expected output:**

```text
6.8.0-45-generic
x86_64
```

### Step 2 – Check if cgroups are available

**Command:**

```bash
mount | grep cgroup
ls /sys/fs/cgroup/ 2>/dev/null | head -5
```

**Explanation:** cgroups are mounted by systemd on modern distros. Container runtimes use cgroups v1 or v2 to enforce memory and CPU limits.

**Expected output:**

```text
cgroup2 on /sys/fs/cgroup type cgroup2 ...
```

### Step 3 – Inspect namespace support

**Command:**

```bash
grep -E 'namespace|pid|net' /proc/self/status | head -6
ls -la /proc/self/ns/
```

**Explanation:** Every process has namespace identifiers. Container runtimes create new namespaces when starting a container, giving it an isolated PID tree and network stack.

**Expected output:**

```text
Pid:    12345
...
dr-x--x--x ... net
dr-x--x--x ... pid
dr-x--x--x ... mnt
```

### Step 4 – Compare process isolation models

**Command:**

```bash
ps aux | head -5
systemd-detect-virt 2>/dev/null || echo "systemd-detect-virt not available"
```

**Explanation:** On a bare-metal or VM host, you see all system processes. Inside a container, you would see only processes in that container's PID namespace. `systemd-detect-virt` reports whether you are already inside a VM — common for cloud lab instances.

**Expected output:**

```text
USER       PID  ... COMMAND
root         1  ... /sbin/init
...
kvm
```

### Step 5 – Check for existing container tools

**Command:**

```bash
command -v docker && docker --version || echo "Docker not installed yet"
command -v podman && podman --version || echo "Podman not installed"
```

**Explanation:** Docker may not be installed on a fresh Linux VM — that is expected. Podman is an alternative OCI-compatible runtime. This course focuses on Docker Engine.

**Expected output:**

```text
Docker not installed yet
Podman not installed
```

### Step 6 – Explore container concepts with chroot (optional)

**Command:**

```bash
mkdir -p /tmp/chroot-lab/{bin,lib,lib64,usr/lib}
cp /bin/ls /tmp/chroot-lab/bin/
ldd /bin/ls
# Note shared libraries — containers bundle these dependencies
```

**Explanation:** `chroot` is an early isolation technique — change the root filesystem for a process. Containers extend this with namespaces, cgroups, and layered images. Understanding `chroot` clarifies why images include specific libraries.

**Expected output:**

```text
linux-vdso.so.1
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
```

### Step 7 – Document your lab environment

**Command:**

```bash
echo "=== Container Lab Baseline ==="
echo "Kernel: $(uname -r)"
echo "Arch:   $(uname -m)"
echo "Distro: $(grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"')"
echo "Cgroups: $(stat -fc %T /sys/fs/cgroup/ 2>/dev/null || echo 'unknown')"
echo "Docker: $(command -v docker >/dev/null && docker --version || echo 'not installed')"
```

**Explanation:** Capture a baseline before installation. Include this in runbooks when troubleshooting container runtime issues later.

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `uname -r` | Show running kernel version | `uname -r` |
| `systemd-detect-virt` | Detect virtualization environment | `systemd-detect-virt` |
| `ls /proc/self/ns/` | List namespace links for current process | `ls -la /proc/self/ns/` |
| `mount \| grep cgroup` | Show cgroup filesystem mounts | `mount \| grep cgroup` |
| `ldd` | List shared library dependencies | `ldd /bin/ls` |
| `chroot` | Run command with altered root directory | `chroot /path/to/root /bin/ls` |

### Container readiness check script

Save as `~/bin/container-preflight.sh` — run before installing Docker or joining a Kubernetes node pool:

```bash
#!/usr/bin/env bash
# container-preflight.sh — verify host is ready for container workloads
set -euo pipefail

section() { printf '\n=== %s ===\n' "$1"; }

section "Kernel"
KERNEL=$(uname -r)
ARCH=$(uname -m)
echo "Kernel: $KERNEL"
echo "Arch:   $ARCH"

MAJOR=$(echo "$KERNEL" | cut -d. -f1)
MINOR=$(echo "$KERNEL" | cut -d. -f2)
if [ "$MAJOR" -lt 4 ]; then
  echo "WARNING: Kernel 4.x+ recommended for production containers"
fi

section "Cgroups"
if [ -d /sys/fs/cgroup ]; then
  echo "Cgroup filesystem: present"
  stat -fc "Type: %T" /sys/fs/cgroup/
else
  echo "ERROR: /sys/fs/cgroup not found"
  exit 1
fi

section "Virtualization"
systemd-detect-virt 2>/dev/null || echo "Unknown or bare metal"

section "Container Runtime"
if command -v docker >/dev/null 2>&1; then
  docker --version
  docker info 2>/dev/null | grep -i "Storage Driver" || true
else
  echo "Docker not installed — proceed to installation tutorial"
fi

section "Disk Space"
df -h / /var/lib 2>/dev/null | tail -n +2
echo "Recommend at least 10 GB free for images and layers"
```

Make executable: `chmod +x ~/bin/container-preflight.sh && ~/bin/container-preflight.sh`

## Common Mistakes

!!! warning "Treating containers as miniature VMs"
    Containers share the host kernel. You cannot run a Windows container on a Linux host (without emulation). Do not expect VM-grade isolation without additional hardening — AppArmor, seccomp, and rootless modes exist for a reason.

!!! warning "Assuming containers eliminate all dependency problems"
    Containers bundle **application** dependencies, not the kernel. A container built on Ubuntu 22.04 requires a compatible host kernel. libc mismatches and CPU architecture differences (arm64 vs amd64) still cause "works here, fails there" incidents.

!!! warning "Ignoring image immutability"
    Changes inside a running container are lost when it is removed — unless you commit (anti-pattern) or use volumes. Treat containers as **cattle**, not **pets**: redeploy from image, do not SSH and apt-get install.

!!! warning "Skipping Linux fundamentals"
    Container debugging requires `ps`, `ip`, `strace`, and filesystem knowledge from the [Linux track](../linux/index.md). Docker abstracts the kernel, but production incidents always reach the OS layer.

## Best Practices

!!! tip "Learn Linux before Docker, Git alongside Docker"
    Namespaces and cgroups are Linux concepts. Version Dockerfiles in [Git](../git/index.md) from day one — treat images as build artifacts traced to source commits.

!!! tip "Think 'image in, container out'"
    The workflow is: write Dockerfile → build image → push to registry → run container. Never configure production servers by hand and then try to containerize later.

!!! tip "Start with official base images"
    Use `python:3.12-slim`, `nginx:alpine`, or `gcr.io/distroless` bases from trusted publishers. Custom base images from unknown sources are a supply-chain risk.

!!! tip "Plan for orchestration early"
    A single `docker run` works for learning. Production needs health checks, restart policies, secrets management, and scaling — design images with Kubernetes or ECS in mind.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Concept confusion: VM vs container | Different isolation models | Re-read comparison table; draw the stack diagram for your environment |
| "Containers are always secure" misconception | Shared kernel attack surface | Apply least privilege, scan images, use non-root users |
| Cannot run image on host | Architecture mismatch (arm64 vs amd64) | Build multi-arch images or match host architecture |
| Kernel too old for modern runtime | Legacy host or long-term support lag | Upgrade kernel or use a supported OS version |
| No cgroups mounted | Misconfigured or minimal host | Verify systemd is PID 1; check `/sys/fs/cgroup` |
| Docker not found | Not installed yet | Complete [Docker Installation and Setup](docker-installation-and-setup.md) |

## Summary

- **Containers** are isolated processes with their own filesystem view, built on Linux **namespaces**, **cgroups**, and **union filesystems**
- **Virtual machines** virtualize hardware and run full guest OSes; **containers** share the host kernel and start in seconds with far less overhead
- **Docker** democratized containers with Dockerfile, CLI, registry workflow, and OCI-standard images
- The ecosystem spans **images**, **containers**, **registries**, and **orchestrators** — Docker is the entry point; Kubernetes is the scale-out layer
- Containers solve **portability**, **dependency isolation**, and **CI/CD acceleration** — essential for DevOps, SRE, and platform engineering roles
- Complete [Linux](../linux/index.md) and [Git](../git/index.md) foundations before diving into hands-on Docker labs

## Interview Questions

1. What is a container, and how does it differ from a virtual machine?
2. Name three Linux kernel features that enable containers and explain each briefly.
3. Why did Docker become popular when LXC already existed?
4. What is the difference between a Docker image and a Docker container?
5. Explain the "works on my machine" problem and how containers address it.
6. When would you choose VMs over containers?
7. What is the Open Container Initiative (OCI), and why does it matter?
8. How do containers fit into a CI/CD pipeline?
9. What is a container registry, and name two examples.
10. Why should DevOps engineers understand Linux before learning Docker?

??? tip "Sample Answers (Questions 1, 4, and 8)"

    **Q1 — Container vs VM:** A virtual machine emulates hardware and runs a full guest operating system with its own kernel, providing strong isolation but heavy resource use and slow startup. A container is an isolated process (or process tree) that shares the host kernel, using namespaces for isolation and cgroups for resource limits. Containers start in seconds and are measured in megabytes; VMs start in minutes and are measured in gigabytes.

    **Q4 — Image vs container:** An image is an immutable, layered template containing the filesystem and metadata needed to run an application. A container is a running instance of an image — a live process with a writable layer on top of the read-only image layers. You can run many containers from one image, just as you can spawn many processes from one binary.

    **Q8 — Containers in CI/CD:** Developers commit code to Git; the CI pipeline builds a Docker image from a Dockerfile, tags it with the commit SHA, runs tests inside the container, scans for vulnerabilities, and pushes the image to a registry. CD deploys that exact image tag to staging or production, ensuring the tested artifact is what runs in prod.

## Related Tutorials

- [Docker – Category Overview](index.md)
- [Introduction to Linux](../linux/introduction-to-linux.md) — recommended prerequisite
- [Introduction to Git and Version Control](../git/introduction-to-git-and-version-control.md) — version Dockerfiles and configs
- [Docker Installation and Setup](docker-installation-and-setup.md) *(next in Module 1)*
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [Docker official documentation — Get started](https://docs.docker.com/get-started/)
- [Open Container Initiative (OCI)](https://opencontainers.org/)
- [Linux namespaces man page](https://man7.org/linux/man-pages/man7/namespaces.7.html)
- [Linux cgroups man page](https://man7.org/linux/man-pages/man7/cgroups.7.html)
- [CNCF Cloud Native Definition](https://github.com/cncf/toc/blob/main/DEFINITION.md)
- [REBASH Academy – Linux Overview](../linux/index.md)
- [REBASH Academy – Git Overview](../git/index.md)
