---
title: Docker Security Hardening
description: Harden containers with non-root users, read-only root filesystems, dropped Linux capabilities, seccomp profiles, and defense-in-depth runtime constraints.
difficulty: advanced
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: docker
tags:
  - docker
  - security
  - hardening
  - non-root
  - seccomp
  - capabilities
  - devsecops
prerequisites:
  - Completion of Module 1–4 Docker tutorials
  - Basic Linux permissions and process concepts from the Linux track
  - Familiarity with container run and Dockerfile workflows
comments: false
---

# Docker Security Hardening

## Overview

Containers are **not virtual machines**. They share the host kernel and isolate workloads with namespaces, cgroups, and security profiles — but misconfiguration erodes that isolation quickly. Running as root, mounting the Docker socket, granting `CAP_SYS_ADMIN`, or leaving writable root filesystems turns a container escape or RCE into a host compromise.

This tutorial applies **defense in depth** for Docker workloads: **non-root users**, **read-only root filesystems**, dropping **Linux capabilities**, custom **seccomp** profiles, and complementary controls (no new privileges, resource limits, user namespaces overview). You will harden a sample container incrementally and validate each layer.

This is **Tutorial 14** in **Module 5: Operations** of the REBASH Academy Docker series. Pair with [Linux Security Hardening Basics](../linux/linux-security-hardening-basics.md) for host-level controls.

## Prerequisites

- Docker Engine on Linux (security options vary on Docker Desktop)
- Ability to build images — see [Building Images with Dockerfile](building-images-with-dockerfile.md)
- Understanding of [File Permissions and Ownership](../linux/file-permissions-and-ownership.md)
- Lab environment only — aggressive hardening can break applications

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Run containers as non-root UIDs with USER in Dockerfile and runtime overrides
- [ ] Enable read-only root filesystems with tmpfs for writable paths
- [ ] Drop all capabilities and add back only required caps
- [ ] Apply default and custom seccomp profiles to restrict syscalls
- [ ] Combine `--security-opt`, `--cap-drop`, and `--read-only` for layered hardening
- [ ] Explain limits of container security and when to add AppArmor/SELinux or Kubernetes policies

## Architecture

Security layers stack from the host kernel upward. Each runtime flag removes attack surface without replacing host patching or network segmentation.

```d2
direction: down

HOST: "Host kernel + patches"
    SECCOMP: "seccomp profile\nsyscall filter"
    CAPS: "Linux capabilities\nCAP_DROP / CAP_ADD"
    USER: "Non-root UID / GID"
    RO: "Read-only rootfs + tmpfs"
    APP: "Application code"
    HOST -> SECCOMP
    SECCOMP -> CAPS
    CAPS -> USER
    USER -> RO
    RO -> APP
```

## Theory

### Container Threat Model

Assume attackers can:

- Exploit application vulnerabilities (RCE, SSRF, deserialization)
- Read environment variables and mounted secrets if present
- Attempt privilege escalation via misconfigured capabilities
- Probe for Docker socket mounts or host path mounts

Container hardening **reduces blast radius** — it does not replace patching, image scanning, network firewalls, or secrets management.

### Run as Non-Root

By default, many images run as **root (UID 0)** inside the container. Root in a container is not host root, but it can:

- Write to package managers and misconfigured volumes
- Exploit kernel bugs more effectively (historical container escapes)
- Bind privileged ports below 1024 (sometimes needed — use higher ports instead)

**Dockerfile pattern:**

```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

Runtime override (image must support it — files owned correctly):

```bash
docker run --user 10001:10001 myapp
```

Kubernetes equivalent: `securityContext.runAsNonRoot: true` and `runAsUser`.

Ensure application directories are writable by the non-root UID before switching `USER`.

### Read-Only Root Filesystem

`--read-only` mounts the container root filesystem as read-only. Applications that write to `/tmp`, caches, or PID files need **tmpfs** or volume mounts:

```bash
docker run --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --tmpfs /var/run:rw,noexec,nosuid,size=16m \
  myapp
```

Benefits:

- Prevents malware persistence modifying binaries inside the container
- Limits accidental config overwrites
- Forces explicit design of writable paths

Combine with immutable infrastructure — replace containers instead of patching inside them.

### Linux Capabilities

Traditional Unix **root** bundles dozens of privileges. Linux **capabilities** split them (e.g., `CAP_NET_BIND_SERVICE`, `CAP_SYS_TIME`). Docker drops several by default but still grants a subset.

**Drop all, add minimum:**

```bash
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp
```

Common dangerous capabilities to avoid granting:

| Capability | Risk |
|------------|------|
| `CAP_SYS_ADMIN` | Near-root; mount, namespace manipulation |
| `CAP_SYS_PTRACE` | Debug/trace other processes |
| `CAP_NET_RAW` | Raw sockets; packet crafting |
| `CAP_DAC_READ_SEARCH` | Bypass file read permissions |

Default Docker capability set is documented in Docker security docs — treat `--cap-drop=ALL` as the baseline for production services that do not need special caps.

### No New Privileges

`--security-opt no-new-privileges:true` prevents processes from gaining additional privileges via setuid binaries or file capabilities. Essential for multi-process images where you cannot trust every binary.

```bash
docker run --security-opt no-new-privileges:true myapp
```

### seccomp Profiles

**seccomp** (secure computing mode) filters **syscalls** a process may invoke. Docker applies a **default seccomp profile** that blocks dangerous syscalls (e.g., `kexec`, `reboot`, `mount` in many cases).

Options:

- **Default profile** — enabled automatically on most installs
- **Unconfined** — disables seccomp (avoid except debugging): `--security-opt seccomp=unconfined`
- **Custom JSON profile** — whitelist syscalls for minimal apps

Custom profile sketch (illustrative — validate with your app):

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "syscalls": [
    {
      "names": ["read", "write", "exit", "exit_group", "futex", "clock_gettime"],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

Apply:

```bash
docker run --security-opt seccomp=/path/to/profile.json myapp
```

Overly strict profiles break glibc, DNS resolution, and JIT compilers — test thoroughly.

### AppArmor and SELinux (Overview)

On supported distros, Docker applies **AppArmor** (`docker-default`) or **SELinux** labels. Custom profiles confine filesystem and network access beyond seccomp. Kubernetes Pod Security Standards (restricted profile) apply similar constraints at orchestrator level.

### Image and Supply Chain

Hardening runtime without fixing images is incomplete:

- Use minimal bases (`distroless`, `alpine` with caution, `scratch` for static binaries)
- Scan images in CI (Trivy, Grype, ECR/AR scanning)
- Pin base image digests in Dockerfile `FROM`
- Sign images with cosign/notary where supported

See [Container Registries and Distribution](container-registries-and-distribution.md) for digest pinning.

## Hands-on Lab

Harden a simple nginx container step by step.

### Step 1 – Baseline: root nginx

**Command:**

```bash
docker run -d --name sec-lab-base -p 8090:80 nginx:1.27-alpine
docker exec sec-lab-base id
docker exec sec-lab-base touch /test-write 2>&1 || true
docker rm -f sec-lab-base
```

**Explanation:** Stock nginx image runs as root. Writing to `/` succeeds — baseline attack surface.

**Expected output:**

```text
uid=0(root) gid=0(root)
```

### Step 2 – Run nginx as non-root user

Official nginx image includes user `nginx` (UID 101).

**Command:**

```bash
docker run -d --name sec-lab-user \
  --user nginx:nginx \
  -p 8091:8080 \
  nginx:1.27-alpine
docker exec sec-lab-user id
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8091/
docker rm -f sec-lab-user
```

**Explanation:** nginx listens on 8080 in recent images for non-root. Map host 8091 to container 8080.

**Expected output:**

```text
uid=101(nginx) gid=101(nginx)
200
```

### Step 3 – Read-only root filesystem

**Command:**

```bash
docker run -d --name sec-lab-ro \
  --user nginx:nginx \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=32m \
  --tmpfs /var/cache/nginx:rw,noexec,nosuid,size=32m \
  --tmpfs /var/run:rw,noexec,nosuid,size=16m \
  -p 8092:8080 \
  nginx:1.27-alpine
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8092/
docker exec sec-lab-ro sh -c 'touch /etc/test 2>&1' || true
docker rm -f sec-lab-ro
```

**Explanation:** Writable paths nginx needs are tmpfs mounts. Writes to `/etc` fail.

### Step 4 – Drop all capabilities

**Command:**

```bash
docker run -d --name sec-lab-caps \
  --user nginx:nginx \
  --read-only \
  --cap-drop=ALL \
  --tmpfs /tmp:rw,noexec,nosuid,size=32m \
  --tmpfs /var/cache/nginx:rw,noexec,nosuid,size=32m \
  --tmpfs /var/run:rw,noexec,nosuid,size=16m \
  -p 8093:8080 \
  nginx:1.27-alpine
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8093/
docker rm -f sec-lab-caps
```

**Explanation:** nginx does not need extra capabilities when not binding port 80 as root. If curl fails, add back specific caps with `--cap-add`.

### Step 5 – Enable no-new-privileges

**Command:**

```bash
docker run -d --name sec-lab-nnp \
  --user nginx:nginx \
  --read-only \
  --cap-drop=ALL \
  --security-opt no-new-privileges:true \
  --tmpfs /tmp:rw,noexec,nosuid,size=32m \
  --tmpfs /var/cache/nginx:rw,noexec,nosuid,size=32m \
  --tmpfs /var/run:rw,noexec,nosuid,size=16m \
  -p 8094:8080 \
  nginx:1.27-alpine
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8094/
docker rm -f sec-lab-nnp
```

**Explanation:** Blocks setuid escalation paths inside the container.

### Step 6 – Inspect seccomp and security options

**Command:**

```bash
docker run -d --name sec-lab-inspect \
  --user nginx:nginx \
  --cap-drop=ALL \
  --security-opt no-new-privileges:true \
  -p 8095:8080 \
  nginx:1.27-alpine
docker inspect sec-lab-inspect | grep -A20 '"SecurityOpt"'
docker inspect sec-lab-inspect | grep -A10 '"CapDrop"'
docker rm -f sec-lab-inspect
```

**Explanation:** Verify runtime flags persisted in container config — matches deploy manifests in Swarm/Kubernetes translations.

### Step 7 – Build a hardened custom image

Create `/tmp/hardened-lab/Dockerfile`:

```dockerfile
FROM nginx:1.27-alpine
RUN chown -R nginx:nginx /var/cache/nginx /var/log/nginx /etc/nginx/conf.d
USER nginx
EXPOSE 8080
```

**Command:**

```bash
mkdir -p /tmp/hardened-lab && cd /tmp/hardened-lab
docker build -t hardened-nginx:lab .
docker run -d --name sec-lab-built \
  --read-only \
  --cap-drop=ALL \
  --security-opt no-new-privileges:true \
  --tmpfs /tmp:rw,noexec,nosuid,size=32m \
  --tmpfs /var/cache/nginx:rw,noexec,nosuid,size=32m \
  --tmpfs /var/run:rw,noexec,nosuid,size=16m \
  -p 8096:8080 \
  hardened-nginx:lab
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8096/
docker rm -f sec-lab-built
cd /tmp && rm -rf hardened-lab
```

**Explanation:** Embedding `USER nginx` in the image prevents accidental root deploys when operators omit `--user`.

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

| Flag / option | Description | Example |
|---------------|-------------|---------|
| `--user` | Run as UID:GID | `--user 10001:10001` |
| `--read-only` | Read-only root filesystem | With tmpfs for writable dirs |
| `--cap-drop=ALL` | Drop all capabilities | Add back with `--cap-add` |
| `--security-opt no-new-privileges:true` | Block privilege escalation | Recommended default |
| `--security-opt seccomp=` | Custom seccomp JSON | Path to profile file |
| `--pids-limit` | Limit process count | Mitigate fork bombs |
| `--memory` / `--cpus` | Resource limits | Complements security |

### Hardened run template

```bash
docker run -d \
  --name myapp-prod \
  --user 10001:10001 \
  --read-only \
  --cap-drop=ALL \
  --security-opt no-new-privileges:true \
  --pids-limit 100 \
  --memory 512m \
  --cpus 1.0 \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  -p 8080:8080 \
  myregistry.example.com/myapp@sha256:abc123...
```

Adjust tmpfs mounts and capabilities per application requirements.

### Compose security block (Swarm-compatible fields)

```yaml
services:
  web:
    image: myapp:1.0
    read_only: true
    user: "10001:10001"
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=67108864
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
```

Plain `docker compose` on a single node supports most keys; validate with `docker compose config`.

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Running production containers as root"
    Root inside a container simplifies attacks and violates Pod Security Standards. Always set USER in Dockerfile and enforce in orchestrators.

!!! warning "Read-only without tmpfs for app caches"
    Apps crash when they cannot write `/tmp` or cache dirs. Map each required writable path explicitly.

!!! warning "Using --privileged or --cap-add=SYS_ADMIN to fix issues"
    These bypass isolation. Fix the application port binding or mount needs instead of granting admin caps.

!!! warning "Disabling seccomp globally for convenience"
    `seccomp=unconfined` widens syscall surface. Use only during targeted debugging, never as default.

## Best Practices

!!! tip "Apply CIS Docker Benchmark alignment"
    Map controls to non-root, read-only, capability drops, and logging — audit-friendly checklist for compliance.

!!! tip "Scan images and pin digests"
    Runtime hardening cannot fix malware baked into image layers. Scan in CI and deploy by digest.

!!! tip "Never mount /var/run/docker.sock into app containers"
    Socket access equals host-level container control. Use dedicated tooling with RBAC if Docker API access is required.

!!! tip "Test hardened configs in CI"
    Automated smoke tests with production security flags catch breakages before deploy.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Permission denied on startup | Non-root cannot read files | `chown` in Dockerfile or init as root then drop (pattern: gosu/dumb-init) |
| nginx bind to 80 fails | Non-root cannot use port 80 | Listen on 8080+ or use CAP_NET_BIND_SERVICE consciously |
| Read-only container exits immediately | Missing tmpfs for cache/run | Add tmpfs for `/tmp`, `/var/run`, app-specific dirs |
| DNS resolution fails with custom seccomp | Syscalls blocked | Compare against default profile; allow `connect`, `poll`, etc. |
| `--cap-drop=ALL` breaks Java apps | Needs specific syscalls/caps | Test; may need `CHOWN`, `SETGID`, or default profile |
| Cannot write logs | Read-only root | Log to stdout or mount volume for logs |

## Summary

- Containers require **explicit hardening** — default images prioritize compatibility over least privilege
- **Non-root users**, **read-only rootfs**, **capability drops**, and **seccomp** stack to reduce blast radius
- **`no-new-privileges`** blocks setuid escalation; **resource limits** mitigate DoS
- Custom **seccomp** profiles need application-specific testing — default profile is a sensible baseline
- Combine runtime controls with **minimal images**, **scanning**, and **digest pinning** for defense in depth

## Interview Questions

1. Why run containers as non-root even though they are isolated?
2. What does `--read-only` do, and how do apps write temporary files?
3. Explain Linux capabilities vs traditional root.
4. What is seccomp, and what does Docker's default profile block?
5. What does `--security-opt no-new-privileges:true` prevent?
6. Why is mounting the Docker socket dangerous?
7. How would you harden an nginx container for production?
8. What is the difference between AppArmor/SELinux and seccomp?
9. When might you use `--cap-add=NET_BIND_SERVICE`?
10. How do Kubernetes Pod Security Standards relate to Docker run flags?

??? tip "Sample Answers (Questions 1, 4, and 7)"

    **Q1 — Non-root rationale:** Container isolation is defense in depth, not a guarantee. Root in a container can exploit kernel vulnerabilities, modify writable mounts, and access sensitive metadata. Non-root limits damage from RCE and aligns with compliance baselines (PCI, CIS).

    **Q4 — seccomp:** seccomp filters syscalls. Docker's default profile blocks many privileged syscalls (mount, reboot, kexec_load, etc.) while allowing typical application needs. Custom profiles further restrict syscalls for minimal workloads but require testing to avoid breaking libc and DNS.

    **Q7 — nginx hardening:** Use official image with `USER nginx`, listen on 8080, `--read-only` with tmpfs for cache and pid paths, `--cap-drop=ALL`, `no-new-privileges:true`, resource limits, structured logging to stdout, pinned image digest, and network policies restricting egress.

## Related Tutorials

- [Docker – Category Overview](index.md)
- [Container Logging and Monitoring](container-logging-and-monitoring.md) *(previous in Module 5)*
- [Troubleshooting Docker Containers](troubleshooting-docker-containers.md) *(next in Module 5)*
- [Linux Security Hardening Basics](../linux/linux-security-hardening-basics.md)
- [Environment Variables and Secrets](environment-variables-and-secrets.md)
- Cheat sheet: [Docker Cheat Sheet](../cheatsheets/docker.md)
- Interview prep: [Docker Interview Prep](../interview/docker.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [Docker security overview](https://docs.docker.com/engine/security/)
- [Docker seccomp profile](https://docs.docker.com/engine/security/seccomp/)
- [Linux capabilities man page](https://man7.org/linux/man-pages/man7/capabilities.7.html)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [REBASH Academy – DevSecOps Overview](../devsecops/index.md)
