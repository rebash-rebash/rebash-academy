---
title: Learning Roadmap
description: "Structured 17-module learning roadmap for Docker for Cloud & DevOps Engineers."
technology_id: docker
hide:
  - toc
author: Shaik Basha
category: docker
tags:
  - docker
  - roadmap
last_updated: "2026-08-03"
---

# Docker — Learning Roadmap

Follow the course in order:

1. **Course overview** — scope, prerequisites, outcomes  
2. **Modules 1–17** — tutorials in sequence  
3. **Labs / quizzes / projects** — practice  
4. **Capstone** — production container platform  
5. **Interview & certifications** — DCA concepts · CKA/CKAD container basics  

![Docker architecture](../assets/excalidraw/docker-architecture.svg)

![CI/CD pipeline](../assets/excalidraw/docker-cicd-pipeline.svg)

## Modules

| # | Focus | Tutorials |
|---|-------|-----------|
| 1 | Container fundamentals | [Introduction](introduction-to-containers-and-docker.md) · [Architecture](docker-architecture-and-components.md) |
| 2 | Installing Docker | [Install and setup](docker-installation-and-setup.md) |
| 3 | Docker CLI | [First container](running-your-first-container.md) |
| 4 | Images | [Working with images](working-with-docker-images.md) |
| 5 | Dockerfile | [Building with Dockerfile](building-images-with-dockerfile.md) |
| 6 | Optimisation | [Multi-stage builds](dockerfile-best-practices-and-multi-stage-builds.md) |
| 7 | Volumes | [Persistent storage](volumes-and-persistent-storage.md) |
| 8 | Networking | [Networking fundamentals](docker-networking-fundamentals.md) |
| 9 | Compose | [Compose fundamentals](docker-compose-fundamentals.md) |
| 10 | Registries | [Registries](container-registries-and-distribution.md) |
| 11 | Security | [Hardening](docker-security-hardening.md) |
| 12 | Scanning | [Scanning & SBOM](container-scanning-and-sbom.md) |
| 13 | Observability | [Logging & monitoring](container-logging-and-monitoring.md) |
| 14 | Performance | [Resource limits](docker-performance-and-resource-limits.md) |
| 15 | CI/CD | [CI/CD pipelines](docker-in-ci-cd-pipelines.md) |
| 16 | Troubleshooting | [Troubleshooting](troubleshooting-docker-containers.md) |
| 17 | Production | [Production patterns](production-docker-patterns.md) |

## Related depth

- [Env vars & secrets](environment-variables-and-secrets.md) · [Swarm basics](docker-swarm-orchestration-basics.md) · [Docker → Kubernetes](from-docker-to-kubernetes.md) · [Capstone](docker-capstone-and-next-steps.md)

## Diagrams

```bash
python3 scripts/generate-excalidraw-svg.py
```
