---
title: Environment Variables and Secrets
description: Configure container environment variables, Docker secrets, bind mounts, and external secret managers for secure twelve-factor and production workloads.
difficulty: intermediate
estimated_time: "35 min"
author: Shaik Basha
category: docker
tags:
  - docker
  - environment-variables
  - secrets
  - configuration
  - twelve-factor
  - compose
prerequisites:
  - Completion of Module 2–3 Docker tutorials (Dockerfile and Compose basics)
  - Understanding of Linux environment variables from the Linux track
  - Familiarity with container run and Compose workflows
comments: false
---

# Environment Variables and Secrets

## Overview

Applications need **configuration** — database URLs, API keys, feature flags, log levels — that changes between environments without rebuilding the image. The [Twelve-Factor App](https://12factor.net/config) principle states: store config in the **environment**, not in code. Docker provides several mechanisms to inject configuration at runtime: **environment variables**, **env files**, **secrets**, **bind mounts**, and integration with external **secret managers**.

This tutorial explains when to use each approach, how to avoid leaking credentials into image layers and logs, and how to wire secrets through **Docker Compose** and production patterns. You will configure a sample web application with non-sensitive env vars and sensitive credentials using Docker's recommended secret primitives.

This is **Tutorial 12** in **Module 4: Networking & Registry** of the REBASH Academy Docker series. Complete [Container Registries and Distribution](container-registries-and-distribution.md) before this tutorial.

## Prerequisites

- Docker Engine and Docker Compose plugin installed
- Completion of [Docker Compose Fundamentals](docker-compose-fundamentals.md)
- Familiarity with [Environment Variables and Shell Config](../linux/environment-variables-shell-config.md) on Linux
- A lab directory where you can create test files (no real production credentials)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Inject configuration with `-e`, `--env-file`, and Dockerfile `ENV` vs runtime overrides
- [ ] Distinguish configuration from secrets and apply least-exposure patterns
- [ ] Mount secrets with Docker Swarm secrets and Compose `secrets` blocks
- [ ] Avoid baking credentials into images, layers, and container metadata
- [ ] Integrate external secret managers conceptually (Vault, AWS Secrets Manager, GCP Secret Manager)
- [ ] Debug missing or incorrect environment variables in running containers

## Architecture Diagram

Configuration flows from sources of truth into the container process environment or mounted files — never through rebuilt image layers for secrets.

```mermaid
flowchart TB
    subgraph sources["Configuration Sources"]
        ENVFILE[".env file<br/>non-secrets only"]
        SECRET_MGR["Secret Manager<br/>Vault / AWS / GCP"]
        COMPOSE["Compose / Stack YAML"]
    end

    subgraph docker["Docker Engine"]
        RUN["docker run / compose up"]
        SWARM_SEC["Swarm secrets<br/>tmpfs mount"]
    end

    subgraph container["Container"]
        PROC[Application process]
        MNT["/run/secrets/*"]
    end

    ENVFILE --> COMPOSE
    SECRET_MGR --> COMPOSE
    COMPOSE --> RUN
    RUN -->|environment vars| PROC
    RUN --> SWARM_SEC
    SWARM_SEC --> MNT
    MNT --> PROC```

## Theory

### Configuration vs Secrets

| Type | Examples | Storage approach |
|------|----------|------------------|
| **Configuration** | `LOG_LEVEL`, `PORT`, `FEATURE_X_ENABLED` | Environment variables, ConfigMaps (K8s) |
| **Secrets** | DB passwords, API tokens, TLS private keys | Secret mounts, secret managers — not plain env in prod |
| **Build-time args** | `NODE_ENV` for compile, version stamps | Dockerfile `ARG` — visible in image history |

**Rule:** If losing the value would require rotation (revoking a key), treat it as a secret.

### Dockerfile ENV vs Runtime Environment

Dockerfile `ENV` instructions bake default values into the **image**. They appear in `docker inspect` and image history. Use `ENV` for harmless defaults (`PORT=8080`). Override at runtime with `docker run -e PORT=9090`.

**Dockerfile `ARG`** values exist only at build time. Never pass secrets as build args — they persist in layer metadata and build cache.

```dockerfile
# Good: non-sensitive default
ENV APP_PORT=8080

# Bad: never do this for secrets
# ARG DB_PASSWORD=supersecret
```

### docker run Environment Injection

Three common methods:

1. **Inline:** `docker run -e DATABASE_HOST=db.internal app`
2. **Pass-through:** `docker run -e DATABASE_HOST app` (reads from host shell)
3. **Env file:** `docker run --env-file ./app.env app`

Env files use `KEY=VALUE` lines. Docker Compose automatically loads `.env` from the project directory for **variable substitution** in the Compose file — a separate concern from container environment.

### Docker Compose Environment Blocks

Compose supports multiple env patterns in `docker-compose.yml`:

```yaml
services:
  web:
    image: myapp:1.0
    environment:
      LOG_LEVEL: info
      DATABASE_HOST: db
    env_file:
      - ./config/web.env
```

Order of precedence (highest wins): shell environment → `environment` section → `env_file` → Dockerfile `ENV`.

Compose also supports **variable substitution** with `${VAR}` and defaults `${VAR:-default}` in the YAML file itself — useful for port mappings and image tags, not for secrets committed to Git.

### Docker Secrets (Swarm Mode)

**Docker secrets** are designed for sensitive data in **Swarm mode**. Secrets are:

- Encrypted at rest in the Swarm Raft log
- Mounted as files in `/run/secrets/<secret_name>` inside containers
- Never stored in container env vars or image layers
- Rotated by creating a new secret and updating the service

Standalone `docker run` does not support Swarm secrets natively. Compose v3+ `secrets` top-level block works with **`docker stack deploy`** (Swarm), not plain `docker compose up` on a single node without Swarm — an important distinction.

For local Compose without Swarm, common patterns:

- Bind-mount a read-only secret file from a path outside Git
- Use external secret sync tools before `compose up`
- Enable Swarm on a single node for lab: `docker swarm init`

### Bind Mounts for Secret Files

Mount credentials from the host without putting them in the image:

```bash
docker run -v /secure/path/db-password.txt:/run/secrets/db-password:ro myapp
```

The application reads the file at startup. Restrict host file permissions (`chmod 600`). This pattern works everywhere but places burden on host filesystem security.

### External Secret Managers

Production platforms rarely rely on flat files alone:

| Platform | Typical integration |
|----------|---------------------|
| **HashiCorp Vault** | Sidecar or init container fetches secrets; entrypoint exports or writes files |
| **AWS Secrets Manager** | ECS task `secrets` block injects into env or files via task execution role |
| **GCP Secret Manager** | Cloud Run and GKE mount secrets as env or volumes |
| **Azure Key Vault** | ACI and AKS integrate via managed identities |

Docker containers are ephemeral — secret managers provide rotation, audit logs, and centralized access control. The container receives short-lived values at start, not permanent copies in Git.

### Twelve-Factor and Container Config

The Twelve-Factor **config** factor aligns with containers:

- Strict separation of config from code
- One codebase, many deploys with different env
- Never commit `.env` with secrets to Git — use `.env.example` with placeholder keys

Add `.env` to `.gitignore`. Scan repos with secret detection tools in CI.

## Hands-on Lab

Build a small Python HTTP app that reads config from environment and a secret file.

### Step 1 – Create the lab project

**Command:**

```bash
mkdir -p /tmp/env-secrets-lab/app && cd /tmp/env-secrets-lab
```

Create `app/server.py`:

```python
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        log_level = os.environ.get("LOG_LEVEL", "info")
        secret_path = "/run/secrets/api_token"
        if os.path.isfile(secret_path):
            with open(secret_path, "r", encoding="utf-8") as f:
                token = f.read().strip()
            token_status = "present"
        else:
            token_status = "missing"
        body = f"log_level={log_level} token={token_status}\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

port = int(os.environ.get("APP_PORT", "8080"))
HTTPServer(("0.0.0.0", port), Handler).serve_forever()
```

Create `Dockerfile`:

```dockerfile
FROM python:3.12-alpine
WORKDIR /app
COPY app/server.py .
ENV APP_PORT=8080
ENV LOG_LEVEL=info
EXPOSE 8080
CMD ["python", "server.py"]
```

**Explanation:** The app exposes non-sensitive config via env and checks for a secret file without printing the token value.

### Step 2 – Build the image

**Command:**

```bash
docker build -t env-secrets-lab:1.0 .
```

**Expected output:**

```text
Successfully tagged env-secrets-lab:1.0
```

### Step 3 – Run with inline environment variables

**Command:**

```bash
docker run -d --name env-lab-1 -p 8081:8080 \
  -e LOG_LEVEL=debug \
  -e APP_PORT=8080 \
  env-secrets-lab:1.0
curl -s http://127.0.0.1:8081/
docker rm -f env-lab-1
```

**Explanation:** Runtime `-e` overrides Dockerfile `ENV` defaults. `LOG_LEVEL=debug` appears in output; token remains missing.

**Expected output:**

```text
log_level=debug token=missing
```

### Step 4 – Use an env file for non-secrets

**Command:**

```bash
printf 'LOG_LEVEL=warning\nAPP_PORT=8080\n' > app.env
docker run -d --name env-lab-2 -p 8082:8080 \
  --env-file ./app.env \
  env-secrets-lab:1.0
curl -s http://127.0.0.1:8082/
docker rm -f env-lab-2
```

**Explanation:** Env files group configuration for repeatability. Do not store API keys in files committed to Git.

### Step 5 – Mount a secret file with bind mount

**Command:**

```bash
mkdir -p secrets
printf 'demo-token-not-for-production' > secrets/api_token
chmod 600 secrets/api_token
docker run -d --name env-lab-3 -p 8083:8080 \
  -e LOG_LEVEL=info \
  -v "$(pwd)/secrets/api_token:/run/secrets/api_token:ro" \
  env-secrets-lab:1.0
curl -s http://127.0.0.1:8083/
docker rm -f env-lab-3
```

**Explanation:** Read-only bind mount simulates secret file injection. Production uses secret managers or Swarm secrets instead of host paths when possible.

**Expected output:**

```text
log_level=info token=present
```

### Step 6 – Docker Compose with environment and env_file

Create `docker-compose.yml`:

```yaml
services:
  web:
    image: env-secrets-lab:1.0
    ports:
      - "8084:8080"
    environment:
      LOG_LEVEL: production
    env_file:
      - app.env
    volumes:
      - ./secrets/api_token:/run/secrets/api_token:ro
```

**Command:**

```bash
docker compose up -d
curl -s http://127.0.0.1:8084/
docker compose down
```

**Explanation:** Compose merges `environment`, `env_file`, and volumes. Keys in `environment` override `env_file` when both define the same variable.

### Step 7 – Inspect container environment safely

**Command:**

```bash
docker run -d --name env-lab-4 -e LOG_LEVEL=inspect-test env-secrets-lab:1.0
docker inspect env-lab-4 --format='Env section present'
docker inspect env-lab-4 | grep -A5 '"Env"'
docker rm -f env-lab-4
```

**Explanation:** `docker inspect` shows all environment variables — including secrets if you mistakenly passed them via `-e`. Never put secrets in env vars you plan to inspect or log.

### Step 8 – Clean up

**Command:**

```bash
cd /tmp && rm -rf env-secrets-lab
```

## Commands & Code

| Command / directive | Description | Example |
|---------------------|-------------|---------|
| `docker run -e` | Set environment variable | `docker run -e PORT=8080 app` |
| `docker run --env-file` | Load variables from file | `docker run --env-file prod.env app` |
| `ENV` (Dockerfile) | Default image environment | `ENV NODE_ENV=production` |
| `ARG` (Dockerfile) | Build-time variable only | `ARG VERSION=1.0` |
| Compose `environment` | Service env in YAML | Key-value map under service |
| Compose `env_file` | External env file per service | List of file paths |
| `docker secret create` | Create Swarm secret | `docker secret create db_pass ./pass.txt` |

### Safe entrypoint pattern for secret files

Applications should read secrets from files when available, falling back only in development:

```bash
#!/bin/sh
set -eu
if [ -f /run/secrets/database_url ]; then
  export DATABASE_URL="$(cat /run/secrets/database_url)"
fi
exec python server.py
```

Use `set -eu` without `-o pipefail` for maximum POSIX shell compatibility in minimal images.

### .env.example for teams

Commit a template without real values:

```text
# Copy to .env for local development — never commit .env
LOG_LEVEL=info
APP_PORT=8080
DATABASE_HOST=localhost
# Secrets: mount at /run/secrets/api_token instead of env vars
```

## Common Mistakes

!!! warning "Passing secrets via -e or ENV"
    Environment variables appear in `docker inspect`, process listings (`ps e`), and crash dumps. Use file-based secrets for credentials in production.

!!! warning "Committing .env files to Git"
    One accidental push exposes all keys. Use `.env.example`, `.gitignore`, and pre-commit secret scanning.

!!! warning "Using ARG for credentials at build time"
    Build args are stored in image history. Use runtime injection or multi-stage builds that do not copy secret stages.

!!! warning "Assuming Compose secrets work with docker compose up"
    Top-level `secrets` in Compose require Swarm (`docker stack deploy`) unless you bind-mount files manually on standalone Docker.

## Best Practices

!!! tip "Separate config repos from secret delivery"
    Version Compose and Dockerfiles in Git; deliver secrets from vaults or cloud secret managers at deploy time.

!!! tip "Use read-only mounts for secret files"
    Append `:ro` to volume mounts so compromised containers cannot overwrite credential files.

!!! tip "Rotate secrets without rebuilding images"
    File-based secrets allow rotation by updating the secret source and restarting the container — image digest unchanged.

!!! tip "Validate required variables at startup"
    Fail fast with clear errors when `DATABASE_URL` or secret files are missing — avoids silent misconfiguration in production.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| App sees empty env var | Typo in key name or wrong precedence | Check `docker inspect` Env section; verify Compose override order |
| `--env-file` ignored | Wrong path or CRLF line endings | Use absolute path; convert Windows line endings |
| Secret file not found in container | Mount path mismatch | Align app path with `-v` target; check `:ro` mount |
| Secret visible in logs | App logs full environment | Log only non-sensitive keys; read secrets from files |
| Compose variable substitution empty | `.env` missing for YAML | Add `.env` for `${VAR}` in compose file or export in shell |
| Permission denied on secret mount | Host file permissions too open | `chmod 600` on host; match container user if needed |

## Summary

- **Configuration** belongs in the environment; **secrets** need stronger protection than plain env vars
- Use Dockerfile `ENV` for safe defaults; override at runtime with `-e` and `--env-file`
- **Docker secrets** (Swarm) and **read-only bind mounts** deliver credentials as files under `/run/secrets/`
- Never bake secrets into images, build args, or Git-tracked `.env` files
- Production integrates **external secret managers** for rotation, audit, and least-privilege access
- Compose merges multiple env sources — understand precedence to avoid surprises

## Interview Questions

1. What is the Twelve-Factor App guidance on application configuration?
2. Why should secrets not be passed as environment variables in production?
3. What is the difference between Dockerfile ENV and ARG?
4. How do Docker Swarm secrets differ from bind-mounted secret files?
5. What is the order of precedence for environment variables in Docker Compose?
6. How would you rotate a database password without rebuilding a container image?
7. Why is committing `.env` to Git dangerous even for private repositories?
8. How does AWS ECS inject secrets from Secrets Manager into containers?
9. What appears in `docker inspect` that makes `-e SECRET_KEY=...` risky?
10. How do you document required environment variables for a team without exposing secrets?

??? tip "Sample Answers (Questions 2, 4, and 6)"

    **Q2 — Secrets in env vars:** Environment variables are visible to anyone who can run `docker inspect`, view orchestrator API responses, or read `/proc/PID/environ` on the host. They propagate to child processes and may appear in core dumps and APM tools. File-based secrets with restrictive permissions limit exposure to the application process reading the mount.

    **Q4 — Swarm secrets vs bind mounts:** Swarm secrets are encrypted at rest in the cluster, distributed only to nodes running the service, and mounted in memory (tmpfs) at `/run/secrets/`. Bind mounts read from the host filesystem — simpler but depend on host file security and manual distribution to every node.

    **Q6 — Password rotation:** Store the password in a secret manager or Swarm secret. Update the value in the manager, create a new secret version, and rolling-restart containers to pick up the new file mount. The image unchanged; only runtime secret reference updates. Database side: create new user/password, dual-write period, revoke old credential.

## Related Tutorials

- [Docker – Category Overview](index.md)
- [Docker Compose Fundamentals](docker-compose-fundamentals.md)
- [Container Registries and Distribution](container-registries-and-distribution.md) *(previous in Module 4)*
- [Container Logging and Monitoring](container-logging-and-monitoring.md) *(next — Module 5)*
- [Environment Variables and Shell Config](../linux/environment-variables-shell-config.md)

## References

- [Twelve-Factor App – Config](https://12factor.net/config)
- [Docker run – environment variables](https://docs.docker.com/reference/cli/docker/container/run/#env)
- [Docker Compose environment variables](https://docs.docker.com/compose/environment-variables/)
- [Docker secrets (Swarm)](https://docs.docker.com/engine/swarm/secrets/)
- [Use secrets in Compose](https://docs.docker.com/compose/use-secrets/)
- [REBASH Academy – Linux Environment Variables](../linux/environment-variables-shell-config.md)
