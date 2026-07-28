---
title: Building Images with Dockerfile
description: Write Dockerfiles from scratch — FROM, COPY, RUN, CMD, ENTRYPOINT, build context, .dockerignore, and hands-on labs building a web app image.
difficulty: beginner
estimated_time: "45 min"
author: Shaik Basha
category: docker
tags:
  - docker
  - dockerfile
  - build
  - images
  - containers
  - devops
prerequisites:
  - Running Your First Container
  - Working with Docker Images
comments: false
---

# Building Images with Dockerfile

## Overview

Running `docker run nginx` pulls a pre-built image. Production workflows require **building your own images** — packaging application code, dependencies, and runtime configuration into an immutable artifact that runs identically on a laptop, CI runner, and production host. A **Dockerfile** is the declarative recipe: a text file of instructions that `docker build` executes layer by layer.

This tutorial is **Tutorial 6** in **Module 2: Images & Dockerfile** of the REBASH Academy Docker series. You will write Dockerfiles from scratch, understand how each instruction affects image layers, use build context and `.dockerignore` efficiently, and build a runnable web application image. For optimization patterns, see [Dockerfile Best Practices and Multi-Stage Builds](dockerfile-best-practices-and-multi-stage-builds.md).

## Prerequisites

- Completed [Running Your First Container](running-your-first-container.md) — you can run and inspect containers
- Completed [Working with Docker Images](working-with-docker-images.md) — you understand layers, tags, and `docker pull`
- Docker Engine installed and running (`docker version` succeeds)
- A text editor and terminal access
- Basic familiarity with any programming language (labs use Python and shell)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain what a Dockerfile is and how `docker build` produces an image
- [ ] Use core instructions: `FROM`, `WORKDIR`, `COPY`, `ADD`, `RUN`, `CMD`, `ENTRYPOINT`, `EXPOSE`, `ENV`, `ARG`, and `LABEL`
- [ ] Understand build context and why `.dockerignore` matters
- [ ] Build images with tags and inspect resulting layers
- [ ] Override container commands at runtime with `docker run`
- [ ] Debug failed builds using build output and layer history

## Architecture Diagram

```d2
direction: right

Host: Host {
        CTX: "Build Context\\ndirectory on disk"
        DF: Dockerfile
        CLI: "docker build"
    }
    Engine: Engine {
        DA: "Docker daemon"
        CACHE: "Layer cache"
    }
    Output: Output {
        IMG: "Local image\\nrepo:tag"
    }
    Host.CTX -> Host.CLI
    Host.DF -> Host.CLI
    Host.CLI -> Engine.DA
    Engine.DA -> Engine.CACHE
    Engine.DA -> Output.IMG
```

Each instruction in the Dockerfile typically creates one **immutable layer**. Cached layers speed rebuilds when inputs unchanged.

## Theory

### Dockerfile vs Image vs Container

| Artifact | What it is | Created by |
|----------|------------|------------|
| **Dockerfile** | Text recipe on disk | You write it |
| **Image** | Read-only stack of layers + metadata | `docker build` |
| **Container** | Writable instance of an image | `docker run` |

Images are the **shippable unit**. Containers are **ephemeral runtime instances** — delete the container; the image remains.

### Build Context

When you run:

```bash
docker build -t myapp:1.0 .
```

The final `.` is the **build context** — the directory sent to the Docker daemon (unless using BuildKit secrets or remote builders). Only files inside the context can be referenced by `COPY` and `ADD`. Large contexts slow builds and leak unintended files into layers if not ignored.

**Best practice:** Keep context minimal. Place Dockerfile at project root or use `-f` to point to Dockerfile while context remains the directory you intend.

### Core Instructions

| Instruction | Purpose | Layer? |
|-------------|---------|--------|
| `FROM` | Base image; required first stage instruction | Yes |
| `WORKDIR` | Set working directory for subsequent instructions | Yes |
| `COPY` | Copy files from context into image | Yes |
| `ADD` | Copy + optional tar extraction and URL fetch | Yes |
| `RUN` | Execute command during build (install packages, compile) | Yes |
| `CMD` | Default command when container starts (overridable) | Yes |
| `ENTRYPOINT` | Main executable; `CMD` args append to it | Yes |
| `EXPOSE` | Document intended listen ports (metadata only) | No |
| `ENV` | Set environment variable at build and runtime | Yes |
| `ARG` | Build-time variable; not present at runtime unless re-exported | No* |
| `LABEL` | Metadata key-value pairs | Yes |
| `USER` | Run subsequent instructions and default runtime as user | Yes |

*ARG values can be passed with `--build-arg` and referenced in `RUN` lines.

### CMD vs ENTRYPOINT

| Pattern | Dockerfile | `docker run image` | `docker run image echo hi` |
|---------|------------|-------------------|---------------------------|
| CMD only | `CMD ["python", "app.py"]` | Runs app.py | Runs `echo hi` (replaces CMD) |
| ENTRYPOINT + CMD | `ENTRYPOINT ["python"]` / `CMD ["app.py"]` | Runs `python app.py` | Runs `python echo hi` |
| ENTRYPOINT exec form | `ENTRYPOINT ["/app/server"]` | Runs server | Appends args to server |

**Exec form** (`["executable", "arg1"]`) avoids shell wrapping and signal-handling issues. Prefer exec form for production images.

### COPY vs ADD

Prefer **`COPY`** for straightforward file transfer. Use **`ADD`** only when you need automatic extraction of local tar archives or fetching remote URLs (discouraged — use multi-stage `curl` in `RUN` with checksum verification instead).

### Layer Caching Behavior

Docker caches each instruction's result. If instruction text **and** all files it depends on are unchanged, Docker reuses the cached layer.

| Change triggers rebuild of | Example |
|----------------------------|---------|
| Instruction text | Edit `RUN apt-get install` line |
| Files copied before instruction | Modify source file before `COPY` |
| Earlier layer invalidated | Any change above invalidates all below |

Order Dockerfile instructions from **least frequently changing** (base image, OS packages) to **most frequently changing** (application source).

### Tags and Naming

```text
registry.example.com/team/myapp:1.2.3
│                      │    │     └── tag (version, branch, digest)
│                      │    └──────── repository name
│                      └───────────── namespace or team
└──────────────────────────────────── registry host (optional for Docker Hub)
```

Local builds commonly use `myapp:dev`, `myapp:1.0.0`, or `myapp:abc1234` (git SHA).

## Hands-on Lab

All steps use a disposable lab directory. Run from a machine with Docker Engine and outbound network for package installs.

### Step 1 – Create project structure

**Command:**

```bash
mkdir -p ~/lab/dockerfile-build/app && cd ~/lab/dockerfile-build
cat > app/app.py << 'PYEOF'
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from Dockerfile lab\n")

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
PYEOF

cat > app/requirements.txt << 'EOF'
# No external deps — stdlib only for this lab
EOF

cat > README.md << 'EOF'
# Dockerfile Lab App
Minimal Python HTTP server for REBASH Academy Docker tutorial.
EOF
```

**Explanation:** A tiny Python HTTP server avoids external dependencies while demonstrating real application packaging.

**Expected output:** Three files under `~/lab/dockerfile-build/`.

### Step 2 – Write a basic Dockerfile

**Command:**

```bash
cat > Dockerfile << 'EOF'
FROM python:3.12-slim

LABEL org.rebash.tutorial="building-images-with-dockerfile"
LABEL maintainer="lab@example.com"

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 8080

ENV APP_ENV=production

CMD ["python", "app.py"]
EOF
```

**Explanation:** `FROM` selects base image. `COPY` requirements before source code so dependency layer caches when only app code changes. `EXPOSE` documents port 8080; you still publish with `-p` at runtime.

**Expected output:** `Dockerfile` created in project root.

### Step 3 – Add .dockerignore

**Command:**

```bash
cat > .dockerignore << 'EOF'
.git
.gitignore
README.md
*.md
__pycache__
*.pyc
.env
.venv
EOF

cat .dockerignore
```

**Explanation:** Excludes documentation and secrets from build context. Prevents accidental inclusion of `.env` files in image layers.

**Expected output:**

```text
.git
.gitignore
README.md
...
```

### Step 4 – Build the image

**Command:**

```bash
docker build -t rebash-lab-web:1.0 .
docker images rebash-lab-web
```

**Explanation:** `-t` names the image. Build context is current directory. Watch output for `Step` lines and `CACHED` indicators on rebuild.

**Expected output:**

```text
Successfully tagged rebash-lab-web:1.0
REPOSITORY        TAG   IMAGE ID       CREATED         SIZE
rebash-lab-web    1.0   abcdef123456   2 seconds ago   ~150MB
```

### Step 5 – Run and verify

**Command:**

```bash
docker run -d --name lab-web -p 8080:8080 rebash-lab-web:1.0
sleep 2
curl -s http://localhost:8080/
docker logs lab-web
```

**Explanation:** `-p 8080:8080` maps host port to container port. `curl` confirms the server responds.

**Expected output:**

```text
Hello from Dockerfile lab
```

### Step 6 – Inspect layers and history

**Command:**

```bash
docker history rebash-lab-web:1.0 --no-trunc | head -15
docker inspect rebash-lab-web:1.0 | grep -A5 '"Cmd"'
```

**Explanation:** `docker history` shows each layer and the instruction that created it. `docker inspect` JSON output includes `"Cmd"` showing the default command array.

**Expected output:** History listing `CMD`, `COPY`, `RUN pip install`, `FROM python:3.12-slim`, etc.

### Step 7 – Override CMD at runtime

**Command:**

```bash
docker run --rm rebash-lab-web:1.0 python -c "print('override works')"
docker stop lab-web
```

**Explanation:** Supplying a command at the end of `docker run` replaces `CMD` but not `ENTRYPOINT` (none set here). Container exits after print; `--rm` removes it.

**Expected output:**

```text
override works
```

### Step 8 – Demonstrate build cache

**Command:**

```bash
echo "# cache bust comment" >> app/app.py
docker build -t rebash-lab-web:1.1 .
```

**Explanation:** After modifying `app/app.py`, layers before final `COPY app/` should show `CACHED`; only later steps rebuild.

**Expected output:** Build completes faster with multiple `CACHED` lines for early steps.

### Step 9 – Use ARG for build-time configuration

**Command:**

```bash
cat >> Dockerfile << 'EOF'

ARG BUILD_VERSION=dev
LABEL org.rebash.version="${BUILD_VERSION}"
EOF

docker build --build-arg BUILD_VERSION=1.1 -t rebash-lab-web:1.1 .
docker inspect rebash-lab-web:1.1 | grep -A2 Labels
```

**Explanation:** `ARG` accepts values at build time via `--build-arg`. Useful for embedding version metadata without hardcoding.

**Expected output:** Label includes `org.rebash.version": "1.1"`.

### Step 10 – Clean up

**Command:**

```bash
docker rm -f lab-web 2>/dev/null || true
docker rmi rebash-lab-web:1.0 rebash-lab-web:1.1 2>/dev/null || true
rm -rf ~/lab/dockerfile-build
```

**Explanation:** Remove containers, images, and lab directory.

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `docker build` | Build image from Dockerfile | `docker build -t app:1.0 .` |
| `docker build -f` | Specify Dockerfile path | `docker build -f docker/Dockerfile .` |
| `docker build --no-cache` | Force full rebuild | `docker build --no-cache -t app .` |
| `docker build --build-arg` | Pass build-time variable | `docker build --build-arg VERSION=2 .` |
| `docker history` | Show image layer history | `docker history myapp:1.0` |
| `docker run` | Start container from image | `docker run -p 8080:8080 myapp` |

### Minimal Dockerfile template

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
```

### ENTRYPOINT pattern for CLI tools

```dockerfile
FROM alpine:3.20
ENTRYPOINT ["echo"]
CMD ["default message"]
```

Run: `docker run myecho` prints `default message`; `docker run myecho hello` prints `hello`.

## Common Mistakes

!!! warning "Using `ADD` when `COPY` suffices"
    `ADD` has surprising tar-extraction behavior. Use `COPY` unless you explicitly need extraction.

!!! warning "Running as root in production images"
    Default user is root. Add a non-root `USER` after installing dependencies — covered in depth in the best practices tutorial.

!!! warning "Large build context without .dockerignore"
    Sending gigabytes of `node_modules` or `.git` slows every build and risks leaking secrets into layers.

!!! warning "Shell form CMD causing signal issues"
    `CMD python app.py` wraps in `/bin/sh -c`, breaking graceful shutdown. Use exec form: `CMD ["python", "app.py"]`.

!!! warning "Forgetting EXPOSE does not publish ports"
    `EXPOSE` is documentation. You must still use `-p` or `-P` with `docker run` for host access.

## Best Practices

!!! tip "Copy dependency manifests before source code"
    Order `COPY requirements.txt` + `RUN pip install` before `COPY . .` so dependency layers cache when only application code changes.

!!! tip "Pin base image tags"
    Use `python:3.12-slim`, not `python:latest`, for reproducible builds.

!!! tip "One concern per container"
    Do not run a web server and background worker in one Dockerfile `CMD` without a proper init process — use separate containers or Compose services.

!!! tip "Use .dockerignore from day one"
    Treat it like `.gitignore` for the build context.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `COPY failed: file not found` | File outside build context or typo | Verify paths relative to context root |
| Build hangs on `RUN apt-get` | Missing `-y` or network blocked | Add `-y`; check proxy/firewall |
| `exec format error` | Wrong architecture base image | Use `--platform linux/amd64` if needed |
| Image unexpectedly large | Dev tools in final layer | Multi-stage builds; slim bases |
| Changes not reflected in container | Old image tag cached | Rebuild with new tag; `--no-cache` once |
| Permission denied at runtime | Files copied as root, app runs non-root | `chown` in build or run as matching user |

## Summary

- A **Dockerfile** defines image layers; **`docker build`** executes instructions against a **build context**
- Core instructions: **`FROM`**, **`WORKDIR`**, **`COPY`**, **`RUN`**, **`CMD`**, **`ENTRYPOINT`**, **`EXPOSE`**, **`ENV`**, **`ARG`**
- **`COPY` before frequent changes** maximizes layer cache hits
- **`.dockerignore`** shrinks context and prevents secret leakage
- **`CMD`** is overridable at `docker run`; **`ENTRYPOINT`** defines the main executable
- Images are immutable artifacts; containers are disposable instances

## Interview Questions

1. What is the difference between a Dockerfile, an image, and a container?
2. Explain Docker layer caching and how instruction order affects rebuild speed.
3. When would you use `ENTRYPOINT` vs `CMD`?
4. What is build context and why does `.dockerignore` matter?
5. What is the difference between `COPY` and `ADD`?
6. Does `EXPOSE 8080` make the port reachable from the host?
7. What is the difference between `ENV` and `ARG`?
8. Why prefer exec form over shell form for `CMD` and `ENTRYPOINT`?
9. How do you pass build-time variables to `docker build`?
10. How would you debug a failing `RUN` instruction during build?

??? tip "Sample Answers (Questions 2, 3, and 7)"

    **Q2 — Layer caching:** Each Dockerfile instruction creates a layer stored in cache. If instruction text and inputs (e.g., copied files) are unchanged, Docker reuses the cached layer. Put slow-changing steps (base image, package installs) before fast-changing steps (application source) so most rebuilds only recreate final layers.

    **Q3 — ENTRYPOINT vs CMD:** `CMD` provides the default command and arguments, fully replaceable by arguments to `docker run`. `ENTRYPOINT` sets the main executable; `docker run` args append to it. Combined pattern: ENTRYPOINT defines the binary, CMD supplies default flags — useful for wrapper images.

    **Q7 — ENV vs ARG:** `ARG` exists only at **build time** and is set with `--build-arg`. `ENV` sets environment variables available at **build time (after declared) and runtime** in containers. Secrets should not use either without proper secret management.

## Related Tutorials

- [Docker – Category Overview](index.md)
- [Working with Docker Images](working-with-docker-images.md) *(previous in Module 2)*
- [Dockerfile Best Practices and Multi-Stage Builds](dockerfile-best-practices-and-multi-stage-builds.md) *(next in Module 3)*
- [Running Your First Container](running-your-first-container.md)
- [Linux – Package Management](../linux/package-management.md)

## References

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Docker build overview](https://docs.docker.com/build/concepts/overview/)
- [.dockerignore file](https://docs.docker.com/build/concepts/context/#dockerignore-files)
- [Best practices for writing Dockerfiles](https://docs.docker.com/build/building/best-practices/)
- [REBASH Academy – Docker Overview](index.md)
