---
title: Dockerfile Best Practices and Multi-Stage Builds
description: Optimise Dockerfiles with layer caching, slim bases, non-root users, health checks, and multi-stage builds for production-ready images.
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: docker
tags:
  - docker
  - dockerfile
  - multi-stage
  - optimisation
  - security
  - devops
prerequisites:
  - Building Images with Dockerfile
  - Working with Docker Images
comments: false
---

# Dockerfile Best Practices and Multi-Stage Builds

## Overview

A working Dockerfile is not the same as a **production-ready** Dockerfile. Bloated images slow pulls and increase attack surface. Poor layer ordering wastes CI minutes. Running as root inside containers violates least privilege. **Multi-stage builds** solve the classic problem: you need compilers and dev dependencies to build, but only the compiled artifact should ship to production.

This tutorial is **Tutorial 7** in **Module 3: Storage & Compose** of the REBASH Academy Docker series. You will apply industry best practices, shrink images dramatically with multi-stage patterns, add health checks, and run workloads as non-root users. For persistent data patterns, continue to [Volumes and Persistent Storage](volumes-and-persistent-storage.md).

## Prerequisites

- Completed [Building Images with Dockerfile](building-images-with-dockerfile.md)
- Completed [Working with Docker Images](working-with-docker-images.md)
- Docker Engine with BuildKit enabled (default in Docker 23+)
- Comfort reading basic shell and Dockerfile syntax

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply layer ordering and caching strategies to speed CI builds
- [ ] Choose appropriate base images (distroless, alpine, slim variants)
- [ ] Write multi-stage Dockerfiles separating build and runtime
- [ ] Run containers as non-root users with correct file permissions
- [ ] Add `HEALTHCHECK` instructions for orchestrator integration
- [ ] Compare image sizes and explain trade-offs of each optimisation

## Architecture

```d2
direction: down

Stage1: "Stage 1: builder" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        B1: "FROM golang:1.22 AS builder"
        B2: "COPY source"
        B3: "RUN go build"
    }
    Stage2: "Stage 2: runtime" {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        R1: "FROM gcr.io/distroless/static"
        R2: "COPY --from=builder /app/binary"
        R3: "USER nonroot"
    }
    Stage1.B1 -> Stage1.B2
    Stage1.B2 -> Stage1.B3
    Stage1.B3 -> Stage2.R2: "artifact only"
    Stage2.R1 -> Stage2.R2
    Stage2.R2 -> Stage2.R3
    IMG: "Final image ~10MB"
    Stage2.R3 -> IMG
```

Only the runtime stage becomes the final image. Build tools never ship to production.

## Theory

### Why Image Size and Shape Matter

| Factor | Impact of large images |
|--------|------------------------|
| **Pull time** | Slower deploys, cold starts, and node scaling |
| **Storage** | Higher registry and host disk costs |
| **Attack surface** | More packages = more CVEs to patch |
| **Build time** | Inefficient layers increase CI duration |

Production images should contain **only what runs the application** — not compilers, headers, or shell utilities unless explicitly required.

### Layer Ordering for Cache Efficiency

Docker rebuilds from the first changed layer downward. Optimal order:

1. `FROM` — pinned tag or digest
2. OS package installs (`RUN apt-get`) — change rarely
3. Dependency manifests (`COPY package.json`, `requirements.txt`) + install
4. Application source (`COPY src/`) — changes frequently
5. Runtime config (`CMD`, `USER`, `HEALTHCHECK`)

Combine related `RUN` commands to reduce layer count:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*
```

The cleanup in the **same layer** prevents deleted files from persisting in intermediate layers.

### Base Image Selection

| Base | Size (approx) | Shell | Best for |
|------|---------------|-------|----------|
| `ubuntu:24.04` | ~80 MB | Yes | General purpose, apt packages |
| `python:3.12-slim` | ~150 MB | Yes | Python apps with pip |
| `node:22-alpine` | ~180 MB | Yes | Node.js with musl libc |
| `gcr.io/distroless/static` | ~2 MB | No | Static Go binaries |
| `gcr.io/distroless/python3` | ~50 MB | No | Python without shell |

**Distroless** images contain minimal runtime — excellent for security, harder to debug (use debug variants or sidecar tools).

### Multi-Stage Builds

Syntax uses multiple `FROM` statements with stage names:

```dockerfile
FROM golang:1.22 AS builder
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /app/server .

FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/server /server
ENTRYPOINT ["/server"]
```

`COPY --from=builder` pulls artifacts from a previous stage. Final image excludes Go toolchain entirely.

Common patterns:

| Language | Builder stage | Runtime stage |
|----------|---------------|---------------|
| Go | `golang` | `distroless/static` or `scratch` |
| Node.js | `node` (build) | `node:slim` or `distroless/nodejs` |
| Java | `maven` or `gradle` | `eclipse-temurin` JRE only |
| Rust | `rust` | `debian:slim` or `distroless/cc` |

### Non-Root Users

Running as root inside a container is dangerous — container breakout or misconfigured volume mounts amplify privileges.

```dockerfile
RUN groupadd -r appuser && useradd -r -g appuser appuser
COPY --chown=appuser:appuser . /app
USER appuser
WORKDIR /app
```

Ensure application listen ports are **above 1024** (non-privileged) or use capabilities instead of root.

### HEALTHCHECK

Docker and orchestrators use health status for routing and restart decisions:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
```

For distroless images without `curl`, use application-native checks or HTTP probes at orchestrator level (Kubernetes liveness probes).

### BuildKit Features

BuildKit (default builder) provides:

- Parallel stage execution
- Cache mounts: `RUN --mount=type=cache,target=/go/pkg/mod go mod download`
- Secret mounts: avoid secrets in layers
- Improved `.dockerignore` handling

Enable explicitly if needed: `DOCKER_BUILDKIT=1 docker build ...`

### Labels and Metadata

Use [OCI image spec](https://github.com/opencontainers/image-spec/blob/main/annotations.md) labels:

```dockerfile
LABEL org.opencontainers.image.source="https://github.com/org/repo"
LABEL org.opencontainers.image.version="1.2.3"
```

Supports supply-chain tooling and registry UI.

## Hands-on Lab

Build a Go HTTP server using single-stage vs multi-stage comparison.

### Step 1 – Create Go application

**Command:**

```bash
mkdir -p ~/lab/multistage/app && cd ~/lab/multistage
cat > app/main.go << 'GOEOF'
package main

import (
    "fmt"
    "net/http"
)

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprint(w, "Multi-stage lab OK\n")
    })
    http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
        fmt.Fprint(w, "healthy\n")
    })
    http.ListenAndServe(":8080", nil)
}
GOEOF

cat > app/go.mod << 'EOF'
module rebash-lab

go 1.22
EOF
```

**Explanation:** Minimal HTTP server with `/health` endpoint for health check demonstration.

**Expected output:** Go module and source under `~/lab/multistage/app/`.

### Step 2 – Build single-stage (baseline)

**Command:**

```bash
cat > Dockerfile.single << 'EOF'
FROM golang:1.22-bookworm
WORKDIR /src
COPY app/ .
RUN CGO_ENABLED=0 go build -o /server main.go
EXPOSE 8080
CMD ["/server"]
EOF

docker build -f Dockerfile.single -t rebash-go:single .
docker images rebash-go:single
```

**Explanation:** Single-stage keeps entire Go toolchain in final image — simple but large.

**Expected output:** Image size approximately 800 MB–1 GB.

### Step 3 – Build multi-stage optimised image

**Command:**

```bash
cat > Dockerfile << 'EOF'
# Stage 1: build
FROM golang:1.22-bookworm AS builder
WORKDIR /src
COPY app/go.mod ./
RUN go mod download
COPY app/ .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /server main.go

# Stage 2: runtime
FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && groupadd -r appuser && useradd -r -g appuser -u 10001 appuser

COPY --from=builder --chown=appuser:appuser /server /server

USER appuser
EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:8080/health || exit 1

ENTRYPOINT ["/server"]
EOF
```

**Explanation:** Builder compiles binary; runtime stage copies only the binary. Non-root user and health check included. Note: simplified health check uses `wget` from slim image.

**Expected output:** `Dockerfile` created.

### Step 4 – Compare image sizes

**Command:**

```bash
docker build -t rebash-go:multi .
docker images rebash-go
```

**Explanation:** Multi-stage image should be dramatically smaller than single-stage.

**Expected output:**

```text
REPOSITORY   TAG      SIZE
rebash-go    multi    ~80-120 MB
rebash-go    single   ~800+ MB
```

### Step 5 – Run and verify non-root

**Command:**

```bash
docker run -d --name go-multi -p 8080:8080 rebash-go:multi
sleep 3
curl -s http://localhost:8080/
curl -s http://localhost:8080/health
docker exec go-multi id
```

**Explanation:** Verify application responds and process runs as `appuser` (uid 10001), not root.

**Expected output:**

```text
Multi-stage lab OK
healthy
uid=10001(appuser) gid=10001(appuser) groups=10001(appuser)
```

### Step 6 – Inspect final image layers

**Command:**

```bash
docker history rebash-go:multi --no-trunc | head -10
```

**Explanation:** Confirm no `golang` packages appear in final image history beyond copied binary.

**Expected output:** Small layers; no `go build` in runtime stage.

### Step 7 – Clean up

**Command:**

```bash
docker rm -f go-multi 2>/dev/null || true
docker rmi rebash-go:single rebash-go:multi 2>/dev/null || true
rm -rf ~/lab/multistage
```

**Explanation:** Remove lab containers and images.

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
| `docker build -f` | Build with specific Dockerfile | `docker build -f Dockerfile.prod .` |
| `docker images` | List images with sizes | `docker images myapp` |
| `docker history` | Layer sizes and commands | `docker history myapp:1.0` |
| `docker scout quickview` | CVE summary (if enabled) | `docker scout quickview myapp` |
| `docker build --target` | Build specific stage | `docker build --target builder .` |

### Python multi-stage example

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels

FROM python:3.12-slim
RUN groupadd -r app && useradd -r -g app app
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels
COPY --chown=app:app . .
USER app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:application"]
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Installing dev dependencies in final stage"
    Keep compilers and test frameworks in builder stages only. Copy artifacts, not toolchains.

!!! warning "Forgetting to pin base image versions"
    `latest` tags change without notice. Pin major.minor or use digest for reproducibility.

!!! warning "Running as root because app needs port 80"
    Bind to 8080 internally; map with `-p 80:8080` or grant `CAP_NET_BIND_SERVICE` selectively.

!!! warning "Separate RUN apt-get update and install"
    Stale cache can cause install failures. Combine update, install, and cleanup in one RUN.

!!! warning "Copying entire context with secrets"
    Use `.dockerignore` and BuildKit secret mounts — never `COPY .env` into layers.

## Best Practices

!!! tip "Use multi-stage builds for compiled languages"
    Go, Rust, Java, and TypeScript builds benefit most — runtime images shrink 90%+.

!!! tip "Prefer slim or distroless runtime bases"
    Match runtime to artifact: static binary → distroless/static; dynamic linking → slim + ca-certificates.

!!! tip "Set USER before CMD"
    Ensure runtime process never starts as root even if someone overrides entrypoint carelessly.

!!! tip "Add HEALTHCHECK for stateful services"
    Enables Docker health status and prepares for Kubernetes/orchestrator migration.

!!! tip "Document build args for version stamping"
    Pass git SHA and build date via `--build-arg` for observability without editing Dockerfile per release.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `COPY --from=builder: not found` | Stage name typo or stage skipped | Verify `AS builder` name matches |
| Permission denied on bind mount | Non-root UID mismatch with host volume | Match UID/GID or use named volumes |
| Health check always unhealthy | Wrong port or missing curl/wget | Align probe with actual listen port |
| Binary not found at runtime | Wrong COPY path or architecture | Verify `GOOS=linux`; check COPY destination |
| Larger image than expected | Single-stage Dockerfile used | Confirm multi-stage; inspect `docker history` |
| musl vs glibc errors (Alpine) | Binary linked against wrong libc | Build with matching base or use static linking |

## Summary

- **Layer order** determines cache efficiency — dependencies before application source
- **Multi-stage builds** separate build tools from runtime artifacts, shrinking images and attack surface
- **Non-root USER**, pinned bases, and combined RUN layers are production essentials
- **HEALTHCHECK** enables automated recovery and load-balancer integration
- **BuildKit cache mounts** speed CI without adding layer bloat
- Compare **`docker images`** and **`docker history`** to validate optimizations

## Interview Questions

1. Why does Dockerfile instruction order matter for build caching?
2. Explain multi-stage builds and when you would use them.
3. What are distroless images and what trade-offs do they introduce?
4. How do you run a container as a non-root user?
5. What is the purpose of HEALTHCHECK?
6. Why combine `apt-get update` and `install` in a single RUN layer?
7. What is the difference between `COPY` and `COPY --from=stage`?
8. How would you avoid baking secrets into image layers?
9. When would you choose Alpine over Debian slim?
10. How do BuildKit cache mounts differ from regular layers?

??? tip "Sample Answers (Questions 1, 2, and 8)"

    **Q1 — Instruction order:** Docker invalidates cache from the first changed instruction onward. Placing slow-changing steps (base image, OS packages, dependency install) before frequently edited source means most rebuilds only recreate final layers, saving CI time.

    **Q2 — Multi-stage builds:** Multiple `FROM` statements define stages. Build stages compile or install dependencies; the final stage copies only runtime artifacts via `COPY --from`. Build tools never appear in the shipped image — smaller, more secure, faster to deploy.

    **Q8 — Avoid secret layers:** Never `COPY` credential files. Use BuildKit `RUN --mount=type=secret` for build-time secrets, runtime secret injection via orchestrators, and `.dockerignore` for `.env`. Secrets in layers persist in image history even after deletion.

## Related Tutorials

- [Docker – Category Overview](index.md)
- [Building Images with Dockerfile](building-images-with-dockerfile.md) *(previous)*
- [Volumes and Persistent Storage](volumes-and-persistent-storage.md) *(next)*
- [Docker Security Hardening](docker-security-hardening.md)
- [Production Docker Patterns](production-docker-patterns.md)
- Cheat sheet: [Docker Cheat Sheet](../cheatsheets/docker.md)
- Interview prep: [Docker Interview Prep](../interview/docker.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/build/building/best-practices/)
- [Google distroless images](https://github.com/GoogleContainerTools/distroless)
- [BuildKit cache mounts](https://docs.docker.com/build/cache/optimise/)
- [OCI image annotations](https://github.com/opencontainers/image-spec/blob/main/annotations.md)
