---
title: Docker Capstone and Next Steps
description: Capstone project — deploy a multi-service voting app with Docker Compose, CI/CD, production patterns, and a migration roadmap to Kubernetes.
difficulty: advanced
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-28"
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



## Architecture



![Production container platform](../assets/excalidraw/docker-production-platform.svg)



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



## Theory



Core ideas for this tutorial appear inline in the lab steps and Code Walkthrough. Read each step explanation before running commands.


### Capstone quality bar

Before you call the VoteStack (or your variant) complete, verify it behaves like a miniature production system: images build reproducibly, Compose (or Kubernetes) brings dependencies up in order, healthchecks gate traffic, resource limits contain faults, and secrets never live in Git. Add a short README that documents ports, required env vars, and teardown commands — future-you and interviewers both care that you can operate what you built.

Use the capstone as a portfolio artefact: push images to a personal registry, attach a CI workflow that builds and scans, and write a one-page architecture note covering failure domains (what happens if Redis dies, if Postgres is slow, if the worker crashes mid-vote).

### Field notes for docker capstone and next steps

Re-read the Architecture diagram alongside the Hands-on Lab: each lab step should map to a box or arrow in that picture. If you cannot point to where a command fits, pause and revisit Theory before continuing — that habit prevents cargo-cult YAML and Compose snippets in production reviews.


### Practice mindset

As you work through this tutorial, narrate *why* each control or command exists — not only *how* to type it. Production incidents are rarely solved by memorising flags; they are solved by connecting symptoms to the architecture (daemon vs kubelet, image vs running container, Service vs Endpoints, volume vs writable layer). After the lab, write three bullet notes in your own words: what you verified, what would break in production if skipped, and what you would monitor next.


### Connecting the lab to production reviews

When a teammate asks “is this ready?”, answer with evidence from this tutorial’s controls: image provenance, privilege level, network exposure, health signals, and teardown/rollback. Copy-pasting a working lab snippet into production without those answers is how quiet misconfigurations become incidents. Prefer small, reviewable changes — one Dockerfile improvement, one RBAC binding, one probe — over large untested stacks.

### Observability while you learn

Get into the habit of watching state while commands run: `docker events` / `kubectl get events`, resource usage, and logs in a second pane. Many failures are timing issues (probes, readiness, volume attach) that disappear if you only look at the final steady state. Capturing a short timeline of what you saw will also make your Troubleshooting section notes far more valuable later.


### Checklist before you leave the lab

1. Resources created in this tutorial are deleted or clearly labelled for retention.
2. No secrets, kubeconfigs, or registry passwords were written into Git.
3. You can explain the Architecture diagram without reading the caption.
4. Validation pass criteria in this page are satisfied on your machine.
5. You noted one question to revisit in the next tutorial of the series.

### Common production failure modes this topic prevents

Misconfiguration here usually shows up as intermittent outages rather than clean errors: restart loops without log shipping, services that listen but never become Ready, volumes that work on one node only, or credentials that leak into image history. Use the Hands-on Lab as a rehearsal for the failure mode — break something on purpose, watch the signal, then apply the fix documented in Troubleshooting.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-docker/docker-capstone-and-next-steps && cd ~/rebash-docker/docker-capstone-and-next-steps
```

**Focus:** production-minded image: non-root, healthcheck, pinned tag

### Step 1 – Prod-shaped Dockerfile

```bash
cat > Dockerfile << 'EOF'
FROM nginx:1.27-alpine
RUN adduser -D -u 10001 appuser || true
HEALTHCHECK CMD wget -qO- http://127.0.0.1/ || exit 1
EOF
docker build -t rebash-lab:local .
docker run -d --name rebash-lab -p 18080:80 rebash-lab:local
sleep 2
curl -sI http://127.0.0.1:18080 | head -n 3
docker inspect rebash-lab --format '{{ "{{" }}json .State.Health{{ "}}" }}' | tee health.json || true
```

### Final step – Cleanup note

```bash
docker rm -f rebash-lab rebash-lab2 2>/dev/null || true
docker network rm rebash-net 2>/dev/null || true
docker volume rm rebash-vol 2>/dev/null || true
docker rmi rebash-lab:local 2>/dev/null || true
```



## Validation



Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Images | api/web/worker images build successfully |
| Stack | Compose stack is healthy including dependencies |
| Patterns | Healthchecks, restarts, and non-root settings present |
| Cleanup | Stack stopped; secrets not committed |



## Code Walkthrough



```bash
# Smoke test (scripts/smoke-test.sh)
curl -sf "$BASE_URL/api/health" | grep -q ok && curl -sf "$BASE_URL/" -o /dev/null

# Logs and health
docker compose logs -f api worker
docker inspect votestack-api-1 | jq -r '.[0].State.Health.Status'
```

See [Container Logging and Monitoring](container-logging-and-monitoring.md) for metrics exporters.



## Security Considerations



- Treat the capstone stack like production: non-root, healthchecks, limits, and no committed secrets
- Use distinct credentials per environment; never reuse lab Postgres passwords in real deployments
- Scan and sign the images you build before any registry push outside your laptop
- Segment database networks from public-facing web services in Compose
- Document break-glass procedures — do not leave `--privileged` “temporary” services in the final compose file
- Tear down or snapshot lab data so the next learner does not inherit your secrets



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
    `docker compose stop redis` — observe api `/ready` and recovery behaviour.

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


1. What production problem does **Docker Capstone and Next Steps** address in container platforms?
2. A container restarts continually — how do you triage?
3. Why are mutable `latest` tags risky in production?
4. Which container security controls do you insist on before prod?
5. How do you keep images small and builds fast in CI?

!!! tip "Sample answer — question 2"
    Check `docker ps -a`, logs, exit code, and `inspect` for OOM/restarts. Confirm command/entrypoint and volume permissions.

!!! tip "Sample answer — question 4"
    Non-root, minimal base, no secrets in layers, scanning, read-only rootfs where possible, and least capabilities.



## Related Tutorials



- [From Docker to Kubernetes](from-docker-to-kubernetes.md) *(previous)*
- [Docker in CI/CD Pipelines](docker-in-ci-cd-pipelines.md)
- [Production Docker Patterns](production-docker-patterns.md)
- [Docker Compose Fundamentals](docker-compose-fundamentals.md)
- [Docker – Category Overview](index.md) — track complete
- [Kubernetes – Category Overview](../kubernetes/index.md) — **next track**
- [GitLab CI/CD Overview](../gitlab/index.md)
- [Learning Paths](../learning-paths/index.md)
- Cheat sheet: [Docker Cheat Sheet](../cheatsheets/docker.md)
- Interview prep: [Docker Interview Prep](../interview/docker.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)



## References



- [Docker – Awesome Compose examples](https://github.com/docker/awesome-compose)
- [Compose – Production guide](https://docs.docker.com/compose/how-tos/production/)
- [The Twelve-Factor App](https://12factor.net/)
- [OWASP – Docker Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [REBASH Academy – Kubernetes Overview](../kubernetes/index.md)
- [REBASH Academy – Roadmap](../roadmap.md)



## Congratulations



You have completed all **20 tutorials** in the REBASH Academy Docker track — from your first container to production CI/CD, Swarm basics, and the bridge to Kubernetes. Return to the [Docker Overview](index.md) to review the curriculum, deploy VoteStack as a portfolio project, and begin the [Kubernetes track](../kubernetes/index.md) when you are ready for cluster-scale orchestration.
