---
title: Docker Capstone and Next Steps
description: Capstone project — deploy a multi-service voting app with Docker Compose, CI/CD, production patterns, and a migration roadmap to Kubernetes.
difficulty: advanced
estimated_time: "50 min"
author: Shaik Basha
category: docker
tags:
  - docker
  - capstone
  - compose
  - project
  - next-steps
prerequisites:
  - From Docker to Kubernetes
  - Docker in CI/CD Pipelines
  - Production Docker Patterns
  - Docker Compose Fundamentals
comments: false
---

# Docker Capstone and Next Steps

## Overview

You have built images, wired networks, secured containers, integrated CI/CD, and mapped Docker to Kubernetes. This capstone ties it together: deploy a **multi-service voting application** — web frontend, API, worker, Redis, and PostgreSQL — using production Docker patterns, observability hooks, and a documented path to [Kubernetes](../kubernetes/index.md).

This is **Tutorial 20** — the finale of **Module 6: Production & Beyond** and the complete REBASH Academy **Docker track**.

## Prerequisites

- [From Docker to Kubernetes](from-docker-to-kubernetes.md)
- [Docker in CI/CD Pipelines](docker-in-ci-cd-pipelines.md)
- [Production Docker Patterns](production-docker-patterns.md)
- [Docker Compose Fundamentals](docker-compose-fundamentals.md)
- [Container Logging and Monitoring](container-logging-and-monitoring.md)
- Docker Engine 24+ with Compose v2
- Optional: GitHub or GitLab account for CI lab

## Learning Objectives

By the end of this capstone, you will be able to:

- [ ] Architect a multi-tier container application with clear service boundaries
- [ ] Deploy the stack with Compose using health checks, secrets, and resource limits
- [ ] Configure reverse-proxy routing and internal-only database access
- [ ] Wire a CI pipeline that builds, scans, and pushes service images
- [ ] Document operational runbooks for backup, rollback, and scaling
- [ ] Outline a Kubernetes migration plan using the concept map from Tutorial 19

## Architecture Diagram

```mermaid
flowchart TB
    subgraph External
        USER[Browser]
    end

    subgraph Edge
        NGX[nginx reverse proxy :80]
    end

    subgraph Application
        WEB[web frontend :3000]
        API[api service :8080]
        WORK[worker]
    end

    subgraph Data
        REDIS[(redis)]
        PG[(postgres)]
    end

    USER --> NGX
    NGX --> WEB
    NGX --> API
    API --> REDIS
    API --> PG
    WORK --> REDIS
    WORK --> PG
```

## Project Overview — VoteStack

**VoteStack** is a simplified poll application:

| Service | Role | Image base |
|---------|------|------------|
| **web** | React/Vite static UI + server | node:22-alpine |
| **api** | REST API for polls and votes | node:22-alpine |
| **worker** | Aggregates votes from Redis queue | node:22-alpine |
| **redis** | Message queue and cache | redis:7-alpine |
| **postgres** | Persistent vote storage | postgres:16-alpine |
| **nginx** | TLS termination and routing | nginx:1.27-alpine |

You will clone or create the project structure, containerize each service, and run the full stack locally — mirroring how teams ship real products.

## Project Structure

```text
votestack/
├── web/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── api/
│   ├── Dockerfile
│   ├── package.json
│   └── src/server.js
├── worker/
│   ├── Dockerfile
│   └── src/worker.js
├── nginx/
│   └── default.conf
├── compose.yml
├── compose.prod.yml
├── .env.example
├── scripts/
│   ├── backup-db.sh
│   └── smoke-test.sh
└── .github/workflows/ci.yml
```

## Hands-on Lab

### Lab 1 — Scaffold services

Build three application images (`api`, `web`, `worker`) using multi-stage Dockerfiles from [Dockerfile Best Practices](dockerfile-best-practices-and-multi-stage-builds.md). The **api** exposes `/health` and `/ready` (postgres ping), handles SIGTERM, and serves `GET /api/polls`. The **worker** consumes a Redis `votes` queue and writes to Postgres with idempotent vote IDs.

```dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev

FROM node:22-alpine
WORKDIR /app
RUN apk add --no-cache curl
COPY --from=deps /app/node_modules ./node_modules
COPY src ./src
USER node
EXPOSE 8080
HEALTHCHECK CMD curl -sf http://127.0.0.1:8080/health || exit 1
CMD ["node", "src/server.js"]
```

```bash
docker build -t votestack-api:local ./api
docker build -t votestack-web:local ./web
docker build -t votestack-worker:local ./worker
```

### Lab 2 — Compose stack with production patterns

`.env.example`:

```text
POSTGRES_USER=voteapp
POSTGRES_DB=votes
POSTGRES_PASSWORD=change-me-in-prod
```

`compose.yml` (key services — full file in your repo):

```yaml
name: votestack

services:
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - pg-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s

  api:
    image: votestack-api:local
    restart: unless-stopped
    environment:
      DATABASE_URL: postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres: { condition: service_healthy }
      redis: { condition: service_healthy }
    healthcheck:
      test: ["CMD", "curl", "-sf", "http://127.0.0.1:8080/ready"]
      start_period: 20s

  worker:
    image: votestack-worker:local
    restart: unless-stopped
    depends_on:
      api: { condition: service_healthy }

  web:
    image: votestack-web:local
    depends_on:
      api: { condition: service_healthy }

  nginx:
    image: nginx:1.27-alpine
    ports: ["8080:80"]
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro

volumes:
  pg-data:
```

`nginx/default.conf`:

```nginx
upstream api_upstream {
    server api:8080;
}
upstream web_upstream {
    server web:3000;
}

server {
    listen 80;

    location /api/ {
        proxy_pass http://api_upstream/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://web_upstream;
    }
}
```

Deploy:

```bash
cp .env.example .env
docker compose up -d
docker compose ps
./scripts/smoke-test.sh http://localhost:8080
```

### Lab 3 — CI pipeline

Parallel jobs build each service with `$GITHUB_SHA` tags; push only on non-PR events. Pattern (repeat per `./api`, `./web`, `./worker`):

```yaml
      - name: Build and push
        env:
          IMAGE: ghcr.io/org/votestack-api
        run: |
          docker build -t "$IMAGE:$GITHUB_SHA" ./api
          if [ "$GITHUB_EVENT_NAME" != "pull_request" ]; then
            echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_ACTOR" --password-stdin
            docker push "$IMAGE:$GITHUB_SHA"
          fi
```

Add Trivy scan on `main` — see [Docker in CI/CD Pipelines](docker-in-ci-cd-pipelines.md).

### Lab 4 — Production override

Use `compose.prod.yml` to swap local tags for registry images (`APP_VERSION` = commit SHA), mount TLS certs on nginx, and load postgres password from Docker secrets instead of `.env`.

```bash
export APP_VERSION=abc1234
docker compose -f compose.yml -f compose.prod.yml up -d
```

### Lab 5 — Operations runbook

```bash
# Backup
docker compose exec -T postgres pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > "backups/votes-$(date +%Y%m%d).sql"

# Rolling update
export APP_VERSION=newsha
docker compose -f compose.yml -f compose.prod.yml pull api web worker
docker compose -f compose.yml -f compose.prod.yml up -d --no-deps api web worker
./scripts/smoke-test.sh http://localhost:8080

# Rollback — set APP_VERSION to previous SHA and re-run up -d
```

### Lab 6 — Kubernetes migration

Map each VoteStack service to Kubernetes resources using [From Docker to Kubernetes](from-docker-to-kubernetes.md): **web/api/worker** → Deployments; **nginx** → Ingress; **postgres/redis** → StatefulSet or managed services with PVCs. Continue on the [Kubernetes track](../kubernetes/index.md).

## Commands & Code

```bash
# Smoke test (scripts/smoke-test.sh)
curl -sf "$BASE_URL/api/health" | grep -q ok && curl -sf "$BASE_URL/" -o /dev/null

# Logs and health
docker compose logs -f api worker
docker inspect votestack-api-1 | jq -r '.[0].State.Health.Status'
```

See [Container Logging and Monitoring](container-logging-and-monitoring.md) for metrics exporters.

## Common Mistakes

!!! warning "Publishing postgres and redis ports to the host"
    Data stores should stay on internal networks — only nginx exposes 80/443.

!!! warning "Same .env committed to Git"
    Use `.env.example` only; inject secrets via CI or Docker secrets in prod.

!!! warning "No worker idempotency"
    Queue consumers must handle duplicate deliveries — design worker with unique vote IDs.

!!! warning "Skipping smoke tests after update"
    Always run `./scripts/smoke-test.sh` after image updates.

!!! warning "Stopping at Compose for high-traffic prod"
    Single-host Compose hits vertical limits — plan Swarm or [Kubernetes](../kubernetes/index.md).

## Best Practices

!!! tip "One Dockerfile per service"
    Independent build and deploy cycles — matches microservice CI matrices.

!!! tip "Version the whole stack in Git"
    Compose files, nginx config, init SQL, and CI workflows together — reproducible environments.

!!! tip "Treat capstone as portfolio piece"
    Push to GitHub with README architecture diagram for interviews.

!!! tip "Practice failure injection"
    `docker compose stop redis` — observe api `/ready` and recovery behavior.

!!! tip "Continue the learning path"
    Docker completes the container foundation — [Kubernetes](../kubernetes/index.md) is the natural next track.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| api stuck unhealthy | Postgres not ready | Check depends_on; extend start_period |
| 502 from nginx | upstream down | `docker compose logs api web` |
| worker idle | Redis URL wrong | Verify env; test redis-cli |
| Disk full | Unbounded logs/images | Log rotation; docker system prune |
| CI push denied | Registry auth | Configure GITHUB_TOKEN scopes |

## Summary

- The **VoteStack capstone** combines multi-service architecture, Compose orchestration, and production patterns from the full Docker track
- **Edge nginx**, **health-gated depends_on**, **resource limits**, and **secrets** mirror real production stacks
- **CI/CD** builds per-service images with SHA tags — same artifacts deploy to Compose today and Kubernetes tomorrow
- **Runbooks** for backup, update, and rollback complete the operational picture
- You have finished all **20 Docker tutorials** — continue to [Kubernetes](../kubernetes/index.md), [GitLab CI/CD](../gitlab/index.md), and [Learning Paths](../learning-paths/index.md)

## Interview Questions

1. Walk through the VoteStack architecture and data flow for a vote submission.
2. Why should postgres not publish host ports in production Compose?
3. How do health checks enable safe startup order without brittle sleep commands?
4. How would you roll back a bad API deployment on a single Docker host?
5. What changes when moving VoteStack from Compose to Kubernetes?
6. How do you structure CI for a monorepo with multiple Dockerfiles?
7. What metrics would you alert on for this stack?
8. How does the worker differ from the api in scaling characteristics?
9. What backup and restore procedure protects postgres data?
10. What skills from this Docker track transfer directly to Kubernetes?

??? tip "Sample Answers (Questions 1 and 5)"

    **Q1 — Vote flow:** Browser hits nginx on `/api/vote`. nginx proxies to the api service. api validates the request, pushes a job to Redis list `votes`, and returns 202. worker consumes the queue, writes the vote to postgres with idempotency key. web UI reads aggregated results via api `GET /api/polls`. Health checks on api `/ready` ensure postgres and redis are reachable before accepting traffic.

    **Q5 — Compose to K8s:** Same container images and env semantics. Replace Compose `depends_on` with probe-gated Deployments. Replace nginx edge with Ingress. Convert postgres to StatefulSet or external RDS. Replace named volumes with PVCs. Add HPA for api/web. CI unchanged — only deployment manifests and GitOps layer added.

## Related Tutorials

- [From Docker to Kubernetes](from-docker-to-kubernetes.md) *(previous)*
- [Docker in CI/CD Pipelines](docker-in-ci-cd-pipelines.md)
- [Production Docker Patterns](production-docker-patterns.md)
- [Docker Compose Fundamentals](docker-compose-fundamentals.md)
- [Docker – Category Overview](index.md) — track complete
- [Kubernetes – Category Overview](../kubernetes/index.md) — **next track**
- [GitLab CI/CD Overview](../gitlab/index.md)
- [Learning Paths](../learning-paths/index.md)

## References

- [Docker – Awesome Compose examples](https://github.com/docker/awesome-compose)
- [Compose – Production guide](https://docs.docker.com/compose/how-tos/production/)
- [The Twelve-Factor App](https://12factor.net/)
- [OWASP – Docker Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [REBASH Academy – Kubernetes Overview](../kubernetes/index.md)
- [REBASH Academy – Roadmap](../roadmap.md)

## Congratulations

You have completed all **20 tutorials** in the REBASH Academy Docker track — from your first container to production CI/CD, Swarm basics, and the bridge to Kubernetes. Return to the [Docker Overview](index.md) to review the curriculum, deploy VoteStack as a portfolio project, and begin the [Kubernetes track](../kubernetes/index.md) when you are ready for cluster-scale orchestration.
