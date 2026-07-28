---
title: Volumes and Persistent Storage
description: Master Docker storage — bind mounts, named volumes, tmpfs, volume drivers, backup patterns, and hands-on labs for persistent container data.
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
category: docker
tags:
  - docker
  - volumes
  - storage
  - bind-mounts
  - persistence
  - devops
prerequisites:
  - Running Your First Container
  - Building Images with Dockerfile
comments: false
---

# Volumes and Persistent Storage

## Overview

Containers are ephemeral — when you remove a container, its writable layer disappears. Databases, uploaded files, configuration, and logs must **survive container restarts and replacements**. Docker provides three mount mechanisms: **volumes**, **bind mounts**, and **tmpfs mounts**. Choosing the right type affects portability, performance, backup strategy, and security.

This tutorial is **Tutorial 8** in **Module 3: Storage & Compose** of the REBASH Academy Docker series. You will create and manage named volumes, bind host directories, understand when each type applies, and practice backup and restore workflows. For multi-container stacks using volumes, see [Docker Compose Fundamentals](docker-compose-fundamentals.md).

## Prerequisites

- Completed [Running Your First Container](running-your-first-container.md)
- Completed [Building Images with Dockerfile](building-images-with-dockerfile.md)
- Docker Engine running on Linux (recommended for bind mount permission labs)
- Basic understanding of filesystem paths and permissions

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the difference between volumes, bind mounts, and tmpfs mounts
- [ ] Create, inspect, and remove named volumes with `docker volume`
- [ ] Mount storage with `-v` and `--mount` syntax
- [ ] Understand data lifecycle when containers are recreated
- [ ] Apply permission and SELinux considerations for bind mounts
- [ ] Back up and restore volume data using sidecar containers

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Container
        APP[Application process]
        RW["Container writable layer<br/>ephemeral"]
    end

    subgraph Mounts
        VOL["Named volume<br/>/var/lib/docker/volumes"]
        BIND["Bind mount<br/>host path"]
        TMP["tmpfs<br/>memory only"]
    end

    APP --> RW
    APP --> VOL
    APP --> BIND
    APP --> TMP```

Named volumes are managed by Docker. Bind mounts reference explicit host paths. tmpfs exists only in memory.

## Theory

### Why Persistence Matters

| Scenario | Without persistence | With volume/bind mount |
|----------|--------------------|-----------------------|
| Database container deleted | All data lost | Data remains in volume |
| Application upgrade (new image) | Config inside container lost | Config on volume survives |
| Horizontal scaling | Each replica needs shared or external storage | Shared volume or external DB |
| Log retention | Logs die with container | Logs on bind mount or log driver |

**Stateless containers** (web APIs with external DB) should remain stateless. **Stateful services** (PostgreSQL, Redis with AOF, file uploads) require explicit storage strategy.

### Three Mount Types

| Type | Location | Managed by | Best for |
|------|----------|------------|----------|
| **Volume** | `/var/lib/docker/volumes/` | Docker daemon | Production data, portable across hosts (with driver) |
| **Bind mount** | Any host path | Administrator | Dev config sync, host log access, specific paths |
| **tmpfs** | RAM | Kernel | Secrets, temp files — never written to disk |

### Volume vs Bind Mount

**Named volumes:**

- Created with `docker volume create`
- Docker manages path on host
- Works across platforms without path translation issues
- Preferred for production database data
- Can use volume drivers (NFS, cloud storage plugins)

**Bind mounts:**

- Map host file or directory directly: `-v /host/path:/container/path`
- Absolute host path required
- Host must exist and have correct permissions
- Ideal for live code reload during development
- Tightly couples container to specific host layout

### Mount Syntax: `-v` vs `--mount`

Legacy `-v` syntax:

```bash
docker run -v mydata:/var/lib/postgresql/data postgres:16
docker run -v /home/user/app:/app:ro nginx
```

Modern `--mount` syntax (recommended — explicit keys):

```bash
docker run --mount source=mydata,target=/var/lib/postgresql/data postgres:16
docker run --mount type=bind,source=/home/user/app,target=/app,readonly nginx
docker run --mount type=tmpfs,target=/run/secrets tmpfs-demo
```

| `--mount` key | Meaning |
|---------------|---------|
| `type` | `volume`, `bind`, or `tmpfs` |
| `source` | Volume name or host path |
| `target` | Path inside container |
| `readonly` | Mount read-only |
| `volume-opt` | Driver-specific options |

### Copy-on-Write and the Writable Layer

Every container has a thin **writable layer** on top of the read-only image. File writes go here unless a mount covers the path. Mounts **mask** underlying image directories at the mount point — files in the image at that path become hidden.

### Permissions and Ownership

Bind mount permission issues are common on Linux:

- Container process runs as UID/GID (often root or `999` for postgres)
- Host directory owned by different user → permission denied

Solutions:

- Match ownership: `chown 999:999 /host/data`
- Run container with `--user $(id -u):$(id -g)` for dev bind mounts
- Use named volumes (Docker initializes permissions on first use)

### Volume Lifecycle

```text
docker volume create dbdata
docker run -v dbdata:/data ...     # volume attached
docker rm container                # volume persists
docker volume rm dbdata            # data deleted (if unused)
```

`docker volume prune` removes all unused volumes — dangerous in production without backups.

### Backup Strategies

| Method | Command pattern |
|--------|-----------------|
| **Sidecar tar** | Run busybox container mounting same volume, `tar czf` to bind mount |
| **Database native** | `pg_dump`, `mysqldump` from exec or sidecar |
| **Volume clone** | Copy volume to new volume via intermediate container |
| **Filesystem snapshot** | LVM/ZFS/btrfs snapshot on host (infrastructure level) |

## Hands-on Lab

### Step 1 – Explore default storage location

**Command:**

```bash
docker info | grep -i "docker root dir"
docker system df -v | head -20
```

**Explanation:** Docker Root Dir shows where volumes and image layers live on the host (Linux default: `/var/lib/docker`).

**Expected output:**

```text
Docker Root Dir: /var/lib/docker
```

### Step 2 – Create and inspect a named volume

**Command:**

```bash
docker volume create rebash-lab-data
docker volume inspect rebash-lab-data
docker volume ls | grep rebash
```

**Explanation:** Named volumes receive a unique directory under Docker's volume path. Inspect shows `Mountpoint` on the host.

**Expected output:** JSON with `"Driver": "local"` and a `Mountpoint` path.

### Step 3 – Write data through a container

**Command:**

```bash
docker run --rm \
  --mount source=rebash-lab-data,target=/data \
  alpine:3.20 \
  sh -c 'echo "persisted at $(date -Iseconds)" > /data/timestamp.txt && cat /data/timestamp.txt'
```

**Explanation:** Data written to `/data` inside the container persists in the named volume after container exits.

**Expected output:**

```text
persisted at 2026-07-27T...
```

### Step 4 – Verify data survives container removal

**Command:**

```bash
docker run --rm \
  --mount source=rebash-lab-data,target=/data \
  alpine:3.20 \
  cat /data/timestamp.txt
```

**Explanation:** New container mounts same volume — proves persistence independent of container lifecycle.

**Expected output:** Same timestamp line from Step 3.

### Step 5 – Bind mount lab directory

**Command:**

```bash
mkdir -p ~/lab/volume-lab/host-data
echo "bind mount content" > ~/lab/volume-lab/host-data/config.txt

docker run --rm \
  --mount type=bind,source=$HOME/lab/volume-lab/host-data,target=/config,readonly \
  alpine:3.20 \
  cat /config/config.txt
```

**Explanation:** Bind mount exposes host file directly. `readonly` prevents container from modifying host files.

**Expected output:**

```text
bind mount content
```

### Step 6 – Compare writable layer vs volume

**Command:**

```bash
docker run -d --name vol-demo \
  --mount source=rebash-lab-data,target=/data \
  alpine:3.20 sleep 3600

docker exec vol-demo sh -c 'echo layer-only > /tmp/ephemeral.txt'
docker exec vol-demo sh -c 'echo volume-persist > /data/persist.txt'
docker rm -f vol-demo

docker run --rm \
  --mount source=rebash-lab-data,target=/data \
  alpine:3.20 ls -la /data
```

**Explanation:** After container deletion, `/tmp` content is gone; `/data/persist.txt` remains in volume.

**Expected output:** Lists `timestamp.txt` and `persist.txt`; no `ephemeral.txt`.

### Step 7 – tmpfs for sensitive temp data

**Command:**

```bash
docker run --rm \
  --mount type=tmpfs,target=/run/secrets \
  alpine:3.20 \
  sh -c 'echo secret-token > /run/secrets/token && cat /run/secrets/token'
```

**Explanation:** tmpfs stores data in memory — never hits disk. Suitable for short-lived secrets (still visible to root on host via memory inspection — not a full security solution).

**Expected output:**

```text
secret-token
```

### Step 8 – Backup volume with sidecar pattern

**Command:**

```bash
mkdir -p ~/lab/volume-lab/backups

docker run --rm \
  --mount source=rebash-lab-data,target=/data,readonly \
  --mount type=bind,source=$HOME/lab/volume-lab/backups,target=/backup \
  alpine:3.20 \
  tar czf /backup/rebash-lab-data.tar.gz -C /data .

ls -lh ~/lab/volume-lab/backups/
tar tzf ~/lab/volume-lab/backups/rebash-lab-data.tar.gz
```

**Explanation:** Read-only volume mount prevents backup container from modifying source. Tar archive written to host bind mount.

**Expected output:** Archive listing `timestamp.txt`, `persist.txt`.

### Step 9 – Restore to new volume

**Command:**

```bash
docker volume create rebash-lab-restored

docker run --rm \
  --mount source=rebash-lab-restored,target=/data \
  --mount type=bind,source=$HOME/lab/volume-lab/backups,target=/backup,readonly \
  alpine:3.20 \
  tar xzf /backup/rebash-lab-data.tar.gz -C /data

docker run --rm \
  --mount source=rebash-lab-restored,target=/data \
  alpine:3.20 \
  ls -la /data
```

**Explanation:** Restore pattern for disaster recovery or cloning environments.

**Expected output:** Same files as original volume.

### Step 10 – Clean up

**Command:**

```bash
docker volume rm rebash-lab-data rebash-lab-restored
rm -rf ~/lab/volume-lab
```

**Explanation:** Remove lab volumes and host directories.

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `docker volume create` | Create named volume | `docker volume create dbdata` |
| `docker volume ls` | List volumes | `docker volume ls` |
| `docker volume inspect` | Volume details and mountpoint | `docker volume inspect dbdata` |
| `docker volume rm` | Delete unused volume | `docker volume rm dbdata` |
| `docker volume prune` | Remove all unused volumes | `docker volume prune` |
| `docker run -v` | Mount volume or bind | `docker run -v dbdata:/data app` |
| `docker run --mount` | Explicit mount specification | See lab examples |

### PostgreSQL with named volume

```bash
docker volume create pgdata

docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=devpass \
  --mount source=pgdata,target=/var/lib/postgresql/data \
  postgres:16-alpine
```

### Development bind mount (live reload)

```bash
docker run --rm -it \
  --mount type=bind,source=$(pwd),target=/app \
  -w /app \
  -p 3000:3000 \
  node:22-alpine \
  npm run dev
```

### Read-only root filesystem with writable volume

```bash
docker run -d \
  --read-only \
  --mount source=app-logs,target=/var/log/myapp \
  --tmpfs /tmp \
  myapp:1.0
```

Combines read-only container security with persistent logs and temp scratch space.

## Common Mistakes

!!! warning "Storing database data in container writable layer"
    `docker rm` destroys the layer. Always mount `/var/lib/postgresql/data`, `/var/lib/mysql`, etc.

!!! warning "Blind `docker volume prune` in production"
    Removes all volumes not attached to a running container — can delete backup targets and dormant DB volumes.

!!! warning "Bind mounting over application binaries"
    Mounting host code over `/app` hides image-built files — fine for dev, breaks immutable prod deploys.

!!! warning "Ignoring UID/GID mismatch on bind mounts"
    Postgres fails with "Permission denied" when host directory owned by wrong user.

!!! warning "Assuming tmpfs is secure long-term storage"
    tmpfs is volatile and inspectable — use proper secret management for credentials.

## Best Practices

!!! tip "Use named volumes for production state"
    Decouple data lifecycle from container lifecycle. Bind mounts for dev convenience only.

!!! tip "Prefer --mount over -v for clarity"
    Explicit `type`, `source`, `target`, and `readonly` reduce mount misconfiguration.

!!! tip "Automate backups before upgrades"
    Snapshot or tar volume before `docker run` with new image tag on stateful services.

!!! tip "Document volume names in Compose or IaC"
    Ad-hoc volume names become orphaned assets — label with project and environment.

!!! tip "Separate config from data volumes"
    Config can be bind-mounted or ConfigMaps (K8s); data volumes get backup schedules.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Permission denied on bind mount | UID mismatch | `chown` host dir or `--user` flag |
| Empty directory after mount | Named volume masked image files | Populate via init container or entrypoint |
| Volume not found | Typo or wrong driver | `docker volume ls`; create explicitly |
| Disk full on host | Unchecked log/volume growth | `docker system df`; prune unused; expand disk |
| Data missing after recreate | Used anonymous volume | Use named volume; anonymous volumes removed with container unless `--rm` omitted carefully |
| SELinux blocking bind mount | RHEL/CentOS/Fedora policy | Add `:z` or `:Z` suffix to bind mount (understand security implications) |

## Summary

- Container **writable layers are ephemeral** — use mounts for data that must survive
- **Named volumes** are Docker-managed and preferred for production persistence
- **Bind mounts** tie container paths to host paths — ideal for dev sync
- **tmpfs** keeps data in memory — short-lived, non-persistent scratch
- Use **`--mount`** for explicit, readable mount definitions
- **Backup via sidecar containers** tar-ing volumes is portable and scriptable

## Interview Questions

1. What happens to data in a container's writable layer when the container is removed?
2. Compare volumes, bind mounts, and tmpfs mounts.
3. When would you choose a bind mount over a named volume?
4. What is the difference between `-v` and `--mount`?
5. How do you back up a Docker named volume?
6. Why do permission errors occur with bind mounts?
7. What does `docker volume prune` do and why is it risky?
8. How does mounting a volume affect files baked into the image at that path?
9. What is an anonymous volume and when is it created?
10. How would you run PostgreSQL with persistent storage in Docker?

??? tip "Sample Answers (Questions 1, 2, and 5)"

    **Q1 — Writable layer:** The container's thin writable layer stores changes not covered by mounts. When the container is removed, this layer is deleted and all data in it is lost permanently. Only mounted volumes, bind mounts, or external storage retain data.

    **Q2 — Three mount types:** **Volumes** are Docker-managed storage under `/var/lib/docker/volumes`, portable and preferred for production data. **Bind mounts** map a specific host path into the container — great for dev but host-dependent. **tmpfs** stores data in RAM — fast, non-persistent, suitable for temp secrets or scratch space.

    **Q5 — Volume backup:** Run a temporary container mounting the target volume read-only and a bind mount for backup output. Use `tar czf` to archive volume contents to the host. Restore by creating a new volume and extracting the tar into it with a similar sidecar container.

## Related Tutorials

- [Docker – Category Overview](index.md)
- [Dockerfile Best Practices and Multi-Stage Builds](dockerfile-best-practices-and-multi-stage-builds.md) *(previous)*
- [Docker Compose Fundamentals](docker-compose-fundamentals.md) *(next)*
- [Linux – Disk and Filesystem Management](../linux/disk-and-filesystem-management.md)
- [Production Docker Patterns](production-docker-patterns.md)

## References

- [Docker storage overview](https://docs.docker.com/storage/)
- [Volumes](https://docs.docker.com/storage/volumes/)
- [Bind mounts](https://docs.docker.com/storage/bind-mounts/)
- [tmpfs mounts](https://docs.docker.com/storage/tmpfs/)
- [Backup, restore, or migrate data volumes](https://docs.docker.com/storage/volumes/#back-up-restore-or-migrate-data-volumes)
