---
title: Docker Installation and Setup
description: Install Docker Engine on Linux, configure post-installation steps, add users to the docker group, and verify a production-ready setup.
difficulty: beginner
estimated_time: "25 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: docker
tags:
  - docker
  - installation
  - linux
  - setup
  - devops
prerequisites:
  - Completion of Introduction to Containers and Docker
  - Linux VM or cloud instance with sudo access
  - Basic package management knowledge (apt or dnf)
comments: false
---

# Docker Installation and Setup

## Overview

Installing Docker correctly on day one prevents weeks of permission errors, storage driver mismatches, and "it works on my laptop" CI failures. Production Docker hosts — whether bare-metal build servers, GitLab runners, or Kubernetes worker nodes — all start with the same foundation: **Docker Engine** installed from official packages, configured with a supported **storage driver**, and secured so developers can run containers without logging in as root.

This tutorial walks through **Linux installation** using Docker's official repository, **post-installation** configuration (daemon settings, log rotation, storage), adding your user to the **docker group**, and verification steps that belong in every onboarding runbook.

This is **Tutorial 2** in **Module 1: Foundations** of the REBASH Academy Docker series. Complete [Introduction to Containers and Docker](introduction-to-containers-and-docker.md) first. You should be comfortable with [Linux package management](../linux/index.md) and [Git](../git/index.md) for version-controlling daemon configs in later tutorials.

## Prerequisites

- A Linux VM or cloud instance (Ubuntu 22.04/24.04 LTS recommended for this lab)
- `sudo` privileges on the host
- At least 2 GB RAM and 10 GB free disk space
- Outbound HTTPS access to `download.docker.com` and container registries
- Completion of [Introduction to Containers and Docker](introduction-to-containers-and-docker.md)
- Familiarity with [Introduction to Linux](../linux/introduction-to-linux.md) — especially `systemctl`, users, and groups

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Install Docker Engine from the official Docker repository on Ubuntu/Debian
- [ ] Start, enable, and verify the Docker daemon with `systemctl`
- [ ] Add a non-root user to the `docker` group and understand the security trade-off
- [ ] Run a test container to confirm the installation works end-to-end
- [ ] Configure essential post-install settings: log driver, storage driver, and live-restore
- [ ] Uninstall or upgrade Docker cleanly without orphan volumes or images
- [ ] Document installation steps for reproducible infrastructure provisioning

## Architecture

After installation, your host runs the Docker daemon as a systemd service. The CLI communicates over a Unix socket — understanding this path explains permission errors and remote Docker contexts.

```d2
direction: right

USER: "User — docker group"
    CLI: "Docker CLI\n/usr/bin/docker"
    SOCK: "/var/run/docker.sock"
    DAEMON: "dockerd\nsystemd service"
    CONTAINERD: containerd
    RUNC: runc
    CONT: Containers
    USER -> CLI
    CLI -> SOCK
    SOCK -> DAEMON
    DAEMON -> CONTAINERD
    CONTAINERD -> RUNC
    RUNC -> CONT
```

## Theory

### Installation Methods Compared

| Method | Best for | Pros | Cons |
|--------|----------|------|------|
| **Official Docker repo** | Production Linux servers | Latest stable, supported packages | Requires repo setup |
| **Distro packages** (`apt install docker.io`) | Quick local experiments | One command | Often outdated; not Docker Inc. supported |
| **Convenience script** (`get.docker.com`) | Ephemeral CI agents | Fast automation | Less control; review script in prod |
| **Docker Desktop** | macOS/Windows dev machines | GUI, Kubernetes included | Not for Linux production servers |
| **Rootless Docker** | Shared dev machines, security-sensitive | No root required to run daemon | Limitations on networking and storage |

This tutorial focuses on the **official repository method** for Ubuntu/Debian — the pattern used in production runbooks and Ansible playbooks.

### What Gets Installed

Docker Engine installation typically includes:

| Package | Purpose |
|---------|---------|
| `docker-ce` | Docker Engine (Community Edition) — the daemon |
| `docker-ce-cli` | Docker command-line client |
| `containerd.io` | Container runtime managing image and container lifecycle |
| `docker-buildx-plugin` | Extended build capabilities (multi-platform) |
| `docker-compose-plugin` | Compose v2 as a Docker CLI plugin |

The daemon (`dockerd`) runs as root, listens on `/var/run/docker.sock`, and is managed by systemd.

### The docker Group and Security

By default, only **root** and members of the **docker** group can access the Docker socket. Adding a user to `docker` is convenient but grants **effective root access** on the host — any user who can run Docker can mount host filesystems, escalate privileges, and bypass many security controls.

Production patterns:

- **Developer laptops** — docker group membership is common; accept the risk on single-user machines
- **Shared CI runners** — isolate with dedicated VMs, rootless Docker, or Kubernetes agents
- **Production servers** — restrict docker group membership; use orchestrators (Kubernetes) instead of direct Docker access

### Post-Installation Configuration

Key daemon settings in `/etc/docker/daemon.json`:

| Setting | Purpose |
|---------|---------|
| `log-driver` | Default logging (`json-file` with rotation limits) |
| `storage-driver` | `overlay2` on modern Linux (default) |
| `live-restore` | Keep containers running during daemon restarts |
| `default-address-pools` | Prevent IP exhaustion in large Swarm/bridge networks |
| `registry-mirrors` | Pull acceleration in regions far from Docker Hub |

Always validate JSON syntax after editing: `docker info` should succeed without errors.

### systemd Integration

Docker Engine integrates with systemd:

- **Enable on boot:** `systemctl enable docker`
- **Start/stop/restart:** `systemctl start|stop|restart docker`
- **Logs:** `journalctl -u docker.service -f`
- **Reload config:** edit `daemon.json`, then `systemctl reload docker` or restart

On Kubernetes nodes, containerd may run independently; Docker is increasingly replaced by containerd + CRI. Understanding Docker installation still matters because build pipelines and developer workflows rely on it heavily.

## Hands-on Lab

These steps install Docker Engine on **Ubuntu 24.04 LTS**. Adapt package manager commands for RHEL/Rocky (`dnf`) using [Docker's official docs](https://docs.docker.com/engine/install/).

### Step 1 – Remove conflicting packages (if any)

**Command:**

```bash
sudo apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
dpkg -l | grep -i docker || echo "No legacy Docker packages found"
```

**Explanation:** Old distro packages conflict with Docker CE. Clean removal prevents socket and binary path conflicts.

**Expected output:**

```text
No legacy Docker packages found
```

### Step 2 – Install prerequisites and add Docker GPG key

**Command:**

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

**Explanation:** APT requires a signed repository. The GPG key verifies package integrity — never skip this step in production.

**Expected output:**

```text
(no output on success — key file created at /etc/apt/keyrings/docker.gpg)
```

### Step 3 – Add the Docker APT repository

**Command:**

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

**Explanation:** Pins Docker CE to the **stable** channel. Use `test` channel only in non-production lab environments.

**Expected output:**

```text
Hit:1 https://download.docker.com/linux/ubuntu noble InRelease
...
```

### Step 4 – Install Docker Engine packages

**Command:**

```bash
sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin
```

**Explanation:** Installs the full Engine stack including Buildx and Compose plugins used throughout this track.

**Expected output:**

```text
Setting up docker-ce ...
Created symlink /etc/systemd/system/multi-user.target.wants/docker.service
```

### Step 5 – Verify daemon status and run hello-world

**Command:**

```bash
sudo systemctl status docker --no-pager
sudo docker run --rm hello-world
```

**Explanation:** Confirms the daemon is active and can pull from Docker Hub, create a container, and execute successfully.

**Expected output:**

```text
● docker.service - Docker Application Container Engine
     Active: active (running)
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

### Step 6 – Add your user to the docker group

**Command:**

```bash
sudo usermod -aG docker "$USER"
newgrp docker
docker run --rm alpine echo "Running without sudo"
```

**Explanation:** `usermod -aG` appends the group without removing others. Log out and back in (or `newgrp`) for group membership to take effect.

**Expected output:**

```text
Running without sudo
```

### Step 7 – Configure daemon.json with log rotation

**Command:**

```bash
sudo tee /etc/docker/daemon.json > /dev/null <<'EOF'
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "live-restore": true
}
EOF
sudo systemctl restart docker
docker info 2>/dev/null | grep -E "Logging Driver|Live Restore|Storage Driver"
```

**Explanation:** Unbounded container logs fill disks — a top cause of production outages. `live-restore` keeps containers running during daemon upgrades.

**Expected output:**

```text
Logging Driver: json-file
Live Restore Enabled: true
Storage Driver: overlay2
```

### Step 8 – Capture installation baseline

**Command:**

```bash
docker version
docker info 2>/dev/null | head -20
groups
```

**Explanation:** Document versions in runbooks. `groups` confirms docker group membership.

**Expected output:**

```text
Client: Docker Engine - Community
 Version:           27.x.x
Server: Docker Engine - Community
...
docker
```

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

| Command | Description | Example |
|---------|-------------|---------|
| `systemctl enable docker` | Start Docker on boot | `sudo systemctl enable docker` |
| `systemctl status docker` | Check daemon state | `systemctl status docker` |
| `docker version` | Show client and server versions | `docker version` |
| `docker info` | Display system-wide Docker info | `docker info` |
| `usermod -aG docker USER` | Grant user Docker socket access | `sudo usermod -aG docker alice` |
| `docker run hello-world` | Verify end-to-end installation | `sudo docker run --rm hello-world` |
| `journalctl -u docker` | View daemon logs | `journalctl -u docker.service -n 50` |

### Installation verification script

Save as `~/bin/docker-verify.sh`:

```bash
#!/usr/bin/env bash
# docker-verify.sh — post-install checks for Docker Engine
set -euo pipefail

section() { printf '\n=== %s ===\n' "$1"; }

section "Service Status"
if systemctl is-active --quiet docker; then
  echo "docker.service: active"
else
  echo "ERROR: docker.service not running"
  exit 1
fi

section "Version"
docker version | head -8

section "Hello World"
docker run --rm hello-world | tail -3

section "User Permissions"
if docker info >/dev/null 2>&1; then
  echo "Current user can access Docker socket"
else
  echo "WARNING: Cannot access socket — add user to docker group or use sudo"
fi

section "Storage and Logging"
docker info 2>/dev/null | grep -E "Storage Driver|Logging Driver|Live Restore"

section "Disk Space"
df -h /var/lib/docker 2>/dev/null || df -h /
```

Make executable: `chmod +x ~/bin/docker-verify.sh && ~/bin/docker-verify.sh`

!!! note "MkDocs template safety"
    The `docker version --format` flag uses Go templates with double-brace syntax. In MkDocs pages processed by Jinja macros, prefer `jq` or plain `docker version` output instead of embedding those braces in markdown.

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Installing docker.io from default Ubuntu repos for production"
    The distro package is often outdated and lacks Docker Inc. support. Use the official repository for production and CI images.

!!! warning "Adding every user to the docker group on shared servers"
    Docker socket access equals root privileges. On multi-tenant hosts, use rootless Docker, separate VMs, or Kubernetes with RBAC.

!!! warning "Skipping log rotation in daemon.json"
    Default json-file logs grow without bound. Always set `max-size` and `max-file` on production hosts.

!!! warning "Forgetting to restart the daemon after daemon.json changes"
    Invalid JSON in `/etc/docker/daemon.json` prevents Docker from starting. Validate with `python3 -m json.tool /etc/docker/daemon.json` before restart.

## Best Practices

!!! tip "Pin Docker versions in production"
    Document the exact Engine version in Ansible/Terraform. Test upgrades in staging before rolling to build farms and worker nodes.

!!! tip "Automate installation with IaC"
    Store installation steps as Ansible roles or cloud-init scripts in [Git](../git/index.md). Manual installs drift; automated installs are reproducible.

!!! tip "Monitor /var/lib/docker disk usage"
    Images and layers accumulate. Schedule `docker system prune` policies carefully — never prune production nodes without understanding impact.

!!! tip "Use official docs for RHEL/Rocky and ARM"
    Package names and repo URLs differ by distribution. Always reference [Docker Engine install docs](https://docs.docker.com/engine/install/) for your OS.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Cannot connect to the Docker daemon` | Daemon not running or user lacks socket access | `sudo systemctl start docker`; add user to docker group |
| `permission denied while trying to connect` | User not in docker group | `sudo usermod -aG docker $USER`; re-login |
| `docker: command not found` | CLI not installed or PATH issue | Reinstall `docker-ce-cli`; check `/usr/bin/docker` |
| Daemon fails after daemon.json edit | Invalid JSON syntax | Validate JSON; check `journalctl -u docker` |
| `hello-world` pull timeout | Network/firewall blocking registry | Test `curl -I https://registry-1.docker.io`; configure proxy |
| Wrong storage driver | Old kernel or misconfiguration | Use overlay2 on modern kernels; check `docker info` |
| Group change not effective | Session cached old groups | Log out/in or run `newgrp docker` |

## Summary

- Install Docker Engine from the **official Docker repository** — not outdated distro packages — for supported, current releases
- The stack includes **dockerd**, **containerd**, **CLI**, **Buildx**, and **Compose** plugins
- The **docker group** grants socket access without sudo but is equivalent to root — use carefully on shared systems
- Post-install essentials: **log rotation**, **overlay2 storage**, **live-restore**, and documented versions
- Verify with `systemctl status docker`, `docker version`, and `docker run hello-world`
- Next: understand what you installed in [Docker Architecture and Components](docker-architecture-and-components.md)

## Interview Questions

1. What packages are installed when you set up Docker Engine from the official repository?
2. Why does adding a user to the docker group have security implications?
3. What is the purpose of `/etc/docker/daemon.json`?
4. How do you enable Docker to start automatically on boot?
5. What is the difference between Docker CE and Docker Desktop?
6. Why should container log rotation be configured on production hosts?
7. What does `live-restore` do in the Docker daemon configuration?
8. How would you verify a Docker installation without relying on GUI tools?
9. What is rootless Docker, and when would you choose it?
10. How do you troubleshoot "Cannot connect to the Docker daemon" errors?

??? tip "Sample Answers (Questions 2, 6, and 9)"

    **Q2 — docker group security:** The Docker daemon runs as root and exposes a Unix socket at `/var/run/docker.sock`. Members of the docker group can send API requests to this socket, including mounting host paths into containers and running privileged containers. An attacker with docker group access can mount `/` and escalate to full root on the host.

    **Q6 — Log rotation:** The default json-file log driver writes container stdout/stderr to files under `/var/lib/docker/containers/`. Without max-size and max-file limits, busy containers can generate gigabytes of logs, filling the disk and causing daemon and application failures.

    **Q9 — Rootless Docker:** Rootless mode runs the Docker daemon and containers as a non-root user using user namespaces. It reduces the blast radius on shared machines but has limitations: restricted networking features, different socket path, and some storage driver constraints. Choose it for developer workstations or security-sensitive environments where sudo access is restricted.

## Related Tutorials

- [Docker – Category Overview](index.md)
- [Introduction to Containers and Docker](introduction-to-containers-and-docker.md) *(previous in Module 1)*
- [Docker Architecture and Components](docker-architecture-and-components.md) *(next in Module 1)*
- [Introduction to Linux](../linux/introduction-to-linux.md)
- [Git Installation and Configuration](../git/git-installation-and-configuration.md)

## References

- [Docker Engine install — Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Docker Engine install — RHEL](https://docs.docker.com/engine/install/rhel/)
- [Docker daemon configuration](https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file)
- [Rootless mode documentation](https://docs.docker.com/engine/security/rootless/)
- [REBASH Academy – Linux Overview](../linux/index.md)
- [REBASH Academy – Git Overview](../git/index.md)
