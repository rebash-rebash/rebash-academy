# Technology Definition

## Course

Docker for Cloud & DevOps Engineers

---

## Description

A production-focused Docker course designed for Cloud Engineers, DevOps Engineers, Platform Engineers and Site Reliability Engineers.

This course teaches containerisation from first principles through production deployment.

The focus is on building, securing, optimising and operating containers in real-world environments.

Learners will understand not only how Docker works, but also why containerisation has become the standard for modern application deployment.

---

## Target Roles

- DevOps Engineer
- Cloud Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)
- DevSecOps Engineer
- Software Engineer
- Infrastructure Engineer

---

## Difficulty

Beginner → Advanced

---

## Estimated Duration

6–8 Weeks

---

## Prerequisites

- Linux Fundamentals
- Shell Scripting
- Basic Python
- Git & GitHub

---

## MCP Servers

Primary

- Context7

Optional

- Kubernetes
- GitHub
- Filesystem

---

# Modules

## Module 1 — Container Fundamentals

- What are Containers?
- Virtual Machines vs Containers
- History of Docker
- OCI Standards
- Container Runtime
- Docker Architecture

---

## Module 2 — Installing Docker

- Docker Engine
- Docker Desktop
- Linux Installation
- Rootless Docker
- Docker Contexts

---

## Module 3 — Docker CLI

- docker version
- docker info
- docker run
- docker ps
- docker stop
- docker rm
- docker exec
- docker logs
- docker inspect

---

## Module 4 — Images

- Docker Images
- Layers
- Image Registry
- Pull Images
- Build Images
- Tag Images
- Push Images
- Save & Load Images

---

## Module 5 — Dockerfile

- Dockerfile Syntax
- FROM
- RUN
- COPY
- ADD
- CMD
- ENTRYPOINT
- ENV
- ARG
- WORKDIR
- EXPOSE
- LABEL
- USER

---

## Module 6 — Image Optimisation

- Multi-stage Builds
- Alpine vs Debian
- Distroless Images
- Layer Caching
- BuildKit
- Image Size Optimisation

---

## Module 7 — Volumes & Storage

- Volumes
- Bind Mounts
- tmpfs
- Volume Drivers
- Backup & Restore

---

## Module 8 — Networking

- Bridge Network
- Host Network
- Overlay Network
- Macvlan
- DNS
- Port Mapping
- Network Troubleshooting

---

## Module 9 — Docker Compose

- Compose File
- Services
- Networks
- Volumes
- Environment Variables
- Profiles
- Health Checks

---

## Module 10 — Registries

- Docker Hub
- Private Registry
- GitHub Container Registry
- Google Artifact Registry
- Azure Container Registry
- Amazon ECR

---

## Module 11 — Security

- Rootless Containers
- Non-root Users
- Capabilities
- Seccomp
- AppArmor
- Read-only Filesystems
- Secrets
- Image Signing

---

## Module 12 — Container Scanning

- Trivy
- Docker Scout
- SBOM
- CVE Analysis
- Image Hardening

---

## Module 13 — Logging & Monitoring

- Docker Logs
- Logging Drivers
- Metrics
- Health Checks
- Prometheus
- Grafana

---

## Module 14 — Performance

- CPU Limits
- Memory Limits
- Storage Drivers
- Resource Optimisation
- Container Lifecycle

---

## Module 15 — Docker in CI/CD

- Build Pipelines
- Multi-Architecture Builds
- Buildx
- GitHub Actions
- GitLab CI
- Image Promotion

---

## Module 16 — Troubleshooting

- Container Won't Start
- CrashLoop
- Image Pull Errors
- Networking Issues
- Permission Problems
- Disk Usage
- Debugging Containers

---

## Module 17 — Production Docker

- Production Best Practices
- Image Versioning
- Registry Strategy
- Backup
- Disaster Recovery
- Scaling
- Operational Excellence

---

# Hands-on Labs

- Install Docker
- Build Your First Image
- Write a Dockerfile
- Optimise an Image
- Multi-stage Build
- Configure Volumes
- Configure Networks
- Deploy with Docker Compose
- Build a Private Registry
- Scan Images with Trivy
- Push Images to Docker Hub
- Push Images to GHCR
- Build Multi-Architecture Images
- Configure Health Checks
- Debug a Broken Container
- Secure a Production Container

---

# Projects

## Beginner

Containerise a Python Application

---

## Intermediate

Multi-Container Web Application

---

## Advanced

Production Docker Platform

---

## Capstone

Production Container Platform

Features:

- Multi-stage Builds
- Docker Compose
- Private Registry
- Image Scanning
- Security Hardening
- Logging
- Monitoring
- CI/CD Integration
- Backup Strategy
- Documentation

---

# Cheat Sheets

Generate:

- Docker CLI
- Dockerfile Instructions
- Docker Compose
- Docker Networking
- Docker Volumes
- Docker BuildKit
- Docker Security
- Trivy
- Registry Commands
- Troubleshooting

---

# Interview Preparation

Cover:

- Docker Architecture
- Dockerfile
- Images
- Containers
- Volumes
- Networking
- Compose
- Security
- CI/CD
- Production Scenarios

---

# Excalidraw Diagrams

**Use Excalidraw only** for course diagrams — do not use D2 or Mermaid for Docker tutorials.

Assets live under `docs/assets/excalidraw/` as `.svg` plus editable `.excalidraw` sources. Regenerate with:

```bash
python3 scripts/generate-excalidraw-svg.py
```

Generate diagrams for:

- Docker Architecture
- Container Lifecycle
- Image Layers
- Docker Networking
- Volume Architecture
- Docker Compose
- Registry Workflow
- CI/CD Pipeline
- Production Container Platform

---

# Certifications

Map modules where appropriate to:

- Docker Certified Associate (concepts)
- CKA (container fundamentals)
- CKAD (application packaging)

---

# Capstone Outcome

After completing this course learners should be able to:

- Build production-quality Docker images
- Optimise container performance
- Secure containerised workloads
- Design multi-container applications
- Troubleshoot Docker environments
- Integrate Docker into CI/CD
- Prepare workloads for Kubernetes
- Operate Docker in production environments