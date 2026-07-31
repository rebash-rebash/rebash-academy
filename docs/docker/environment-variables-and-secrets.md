---
title: Environment Variables and Secrets
description: Configure container environment variables, Docker secrets, bind mounts, and external secret managers for secure twelve-factor and production workloads.
difficulty: intermediate
estimated_time: "35 min"
author: Shaik Basha
last_updated: "2026-07-28"
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



## Architecture



Configuration flows from sources of truth into the container process environment or mounted files — never through rebuilt image layers for secrets.

![Compose and configuration](../assets/excalidraw/docker-compose.svg)



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


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-docker/environment-variables-and-secrets && cd ~/rebash-docker/environment-variables-and-secrets
```

**Focus:** pass env files without baking secrets into the image

### Step 1 – Env file run

```bash
cat > app.env << 'EOF'
APP_MODE=lab
EOF
docker run --rm --env-file app.env alpine:3.20 sh -c 'echo APP_MODE=$APP_MODE' | tee env-out.txt
tee secrets-notes.txt << 'EOF'
Never COPY .env with production secrets into images. Prefer runtime injection / orchestrator secrets.
EOF
cat secrets-notes.txt
```

### Final step – Cleanup note

```bash
rm -f app.env
```



## Validation



Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Env injection | Container sees expected non-secret configuration via env |
| Secret handling | Lab secret is supplied without committing real credentials to Git |
| Inspect awareness | You can show where env values appear in `docker inspect` |
| Cleanup | Containers and any local `.env` lab files handled safely |



## Code Walkthrough



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



## Security Considerations



- Never commit `.env` files containing real credentials; provide `.env.example` with placeholders only
- Prefer Docker secrets / external secret managers over plain `environment:` for production
- Remember environment variables are visible via `docker inspect` to anyone who can talk to the daemon
- Rotate lab credentials after demos; treat shared lab passwords as compromised
- Avoid passing secrets on the CLI (`docker run -e PASS=…`) where shell history retains them
- Scrub CI logs — echo and debug printing commonly leak secrets from env blocks



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


1. What production problem does **Environment Variables and Secrets** address in container platforms?
2. A container restarts continually — how do you triage?
3. Why are mutable `latest` tags risky in production?
4. Which container security controls do you insist on before prod?
5. How do you keep images small and builds fast in CI?

!!! tip "Sample answer — question 2"
    Check `docker ps -a`, logs, exit code, and `inspect` for OOM/restarts. Confirm command/entrypoint and volume permissions.

!!! tip "Sample answer — question 4"
    Non-root, minimal base, no secrets in layers, scanning, read-only rootfs where possible, and least capabilities.



## Related Tutorials



- [Docker – Category Overview](index.md)
- [Docker Compose Fundamentals](docker-compose-fundamentals.md)
- [Container Registries and Distribution](container-registries-and-distribution.md) *(previous in Module 4)*
- [Container Logging and Monitoring](container-logging-and-monitoring.md) *(next — Module 5)*
- [Environment Variables and Shell Config](../linux/environment-variables-shell-config.md)
- Cheat sheet: [Docker Cheat Sheet](../cheatsheets/docker.md)
- Interview prep: [Docker Interview Prep](../interview/docker.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)



## References



- [Twelve-Factor App – Config](https://12factor.net/config)
- [Docker run – environment variables](https://docs.docker.com/reference/cli/docker/container/run/#env)
- [Docker Compose environment variables](https://docs.docker.com/compose/environment-variables/)
- [Docker secrets (Swarm)](https://docs.docker.com/engine/swarm/secrets/)
- [Use secrets in Compose](https://docs.docker.com/compose/use-secrets/)
- [REBASH Academy – Linux Environment Variables](../linux/environment-variables-shell-config.md)
