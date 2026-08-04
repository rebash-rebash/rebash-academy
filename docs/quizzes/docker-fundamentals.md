---
title: "Quiz — Docker Fundamentals"
description: "40-question Docker quiz covering images, containers, Dockerfile, Compose networking, security, and production operations."
difficulty: intermediate
estimated_time: "45–60 min"
passing_score: "70% (28/40)"
author: Shaik Basha
last_updated: "2026-07-28"
category: quizzes
tags:
  - quizzes
  - docker
  - assessment
comments: false
---

# Quiz — Docker Fundamentals

## Quiz Overview

Assess practical Docker skills: images and containers, Dockerfile layering, volumes, Compose networking, healthchecks, and secure operational defaults.

| Attribute | Value |
|-----------|--------|
| Topic | Docker |
| Questions | 40 |
| Passing score | 70% (28 correct) |
| Estimated time | 45–60 minutes |
| Format | Multiple choice (single answer) |

!!! tip "How to use this quiz"
    Attempt each section without peeking. Use **Reveal answer** only after you commit to a choice. Score yourself honestly — gaps are the point.

## Learning Objectives

This quiz assesses whether you can:

- [ ] Explain images, containers, and Docker architecture basics
- [ ] Author and optimise Dockerfiles including multi-stage builds
- [ ] Use Compose networking, volumes, and health-gated dependencies
- [ ] Troubleshoot exits, port conflicts, and permission issues
- [ ] Apply production hardening and CI image promotion judgement

## Section 1 — Fundamentals

### Question 1

What is the main difference between a container and a traditional virtual machine?

**Difficulty:** Beginner

**Options:**

- **A.** Containers share the host kernel and isolate processes; VMs typically include a guest OS on a hypervisor
- **B.** Containers virtualise hardware; VMs share the host kernel only
- **C.** VMs cannot run Linux
- **D.** Containers always include a full hypervisor

??? success "Reveal answer"
    **Correct answer: A**

    Containers are process-level isolation on a shared kernel. VMs virtualise hardware with a guest OS.

    **Related concepts**

    - Containers vs VMs
    - Namespaces
    - cgroups

### Question 2

Which component is the long-running Docker daemon on Linux?

**Difficulty:** Beginner

**Options:**

- **A.** containerd-shim only without dockerd
- **B.** kubectl
- **C.** dockerd
- **D.** systemd-resolved

??? success "Reveal answer"
    **Correct answer: C**

    `dockerd` is the Docker daemon. containerd is often used underneath; kubectl is Kubernetes.

    **Related concepts**

    - dockerd
    - Docker architecture

### Question 3

What does a Docker image contain conceptually?

**Difficulty:** Beginner

**Options:**

- **A.** A running process table only
- **B.** Only the host kernel modules
- **C.** A Kubernetes PodSpec
- **D.** A layered, immutable filesystem snapshot plus metadata/config to start containers

??? success "Reveal answer"
    **Correct answer: D**

    Images are layered artefacts used as templates for containers.

    **Related concepts**

    - Images
    - Layers
    - OCI

### Question 4

Which command starts an interactive shell in a new Ubuntu container and removes it on exit?

**Difficulty:** Beginner

**Options:**

- **A.** docker build -t ubuntu
- **B.** docker run --rm -it ubuntu:24.04 bash
- **C.** docker compose down
- **D.** docker system prune -a

??? success "Reveal answer"
    **Correct answer: B**

    `run --rm -it` creates an interactive container and cleans up on exit.

    **Related concepts**

    - docker run

### Question 5

What is the default bridge network behaviour for published ports?

**Difficulty:** Beginner

**Options:**

- **A.** You publish specific ports with -p/--publish; otherwise they stay on the container network namespace
- **B.** All container ports are exposed to the world automatically
- **C.** Docker disables networking by default
- **D.** Bridge mode requires Kubernetes

??? success "Reveal answer"
    **Correct answer: A**

    Publishing maps host ports to container ports intentionally.

    **Related concepts**

    - Port publishing
    - Bridge network

### Question 6

Which Dockerfile instruction creates a new image layer from filesystem changes of a command?

**Difficulty:** Beginner

**Options:**

- **A.** LABEL
- **B.** EXPOSE
- **C.** RUN
- **D.** MAINTAINER (legacy)

??? success "Reveal answer"
    **Correct answer: C**

    `RUN` executes build steps and commits a layer. `EXPOSE` is documentation metadata.

    **Related concepts**

    - Dockerfile
    - RUN

### Question 7

What is a Docker volume best used for?

**Difficulty:** Beginner

**Options:**

- **A.** Storing ephemeral container CPU shares
- **B.** Compiling the kernel
- **C.** Replacing TLS certificates on the host CA store automatically
- **D.** Persisting data beyond container lifecycle

??? success "Reveal answer"
    **Correct answer: D**

    Volumes persist data independent of container recreate.

    **Related concepts**

    - Volumes
    - Persistence

### Question 8

In Compose, how do services typically resolve each other by name?

**Difficulty:** Beginner

**Options:**

- **A.** They cannot
- **B.** Via the Compose project network DNS using service names
- **C.** Only via public Internet DNS
- **D.** Only via /etc/hosts on the laptop, never in containers

??? success "Reveal answer"
    **Correct answer: B**

    Compose creates a user-defined network where service names resolve to containers.

    **Related concepts**

    - Compose DNS

### Question 9

What does `HEALTHCHECK` in a Dockerfile define?

**Difficulty:** Beginner

**Options:**

- **A.** A command Docker runs to mark the container healthy/unhealthy
- **B.** Kubernetes probes
- **C.** Host antivirus policy
- **D.** Image signing identity

??? success "Reveal answer"
    **Correct answer: A**

    Docker healthchecks update container health status used by Compose and operators.

    **Related concepts**

    - HEALTHCHECK

### Question 10

Why pin image tags like `1.2.3` or digests instead of `:latest` in production?

**Difficulty:** Beginner

**Options:**

- **A.** latest is always immutable
- **B.** Digests prevent networking
- **C.** Pinned references make builds and rollbacks reproducible
- **D.** Tags are illegal in OCI

??? success "Reveal answer"
    **Correct answer: C**

    `:latest` moves; digests/tags pin what you run.

    **Related concepts**

    - Image pinning
    - Supply chain

## Section 2 — Practical Knowledge

### Question 11

Which practice reduces final image size most effectively?

**Difficulty:** Intermediate

**Options:**

- **A.** Using fat base images and copying build toolchains into runtime
- **B.** Adding more ADD instructions
- **C.** Running apt-get upgrade in every layer without cleanup
- **D.** Multi-stage builds: compile in a builder stage, copy artefacts into a slim runtime stage

??? success "Reveal answer"
    **Correct answer: D**

    Multi-stage builds leave compilers out of the runtime image.

    **Related concepts**

    - Multi-stage builds

### Question 12

You need a container’s logs for service `api` in Compose. Best command?

**Difficulty:** Beginner

**Options:**

- **A.** kubectl logs api
- **B.** docker compose logs api
- **C.** journalctl -u docker-compose
- **D.** cat /var/lib/docker randomly

??? success "Reveal answer"
    **Correct answer: B**

    Compose aggregates container logs per service.

    **Related concepts**

    - docker compose logs

### Question 13

Bind mount vs named volume — which statement is correct?

**Difficulty:** Intermediate

**Options:**

- **A.** Bind mounts map a host path; named volumes are managed by Docker and often preferred for portability
- **B.** Named volumes always delete host home directories
- **C.** Bind mounts cannot be read-only
- **D.** Volumes only work on Windows

??? success "Reveal answer"
    **Correct answer: A**

    Bind mounts are host-path coupled; named volumes are Docker-managed.

    **Related concepts**

    - Bind mounts
    - Named volumes

### Question 14

Which flag runs a container with a read-only root filesystem (where supported)?

**Difficulty:** Intermediate

**Options:**

- **A.** --privileged
- **B.** --net=host
- **C.** --read-only
- **D.** --pid=host

??? success "Reveal answer"
    **Correct answer: C**

    `--read-only` hardens the container filesystem; privileged/host namespaces widen attack surface.

    **Related concepts**

    - Security hardening

### Question 15

An app inside Compose must call service `db` on port 5432. Correct URL hostname from another service?

**Difficulty:** Beginner

**Options:**

- **A.** localhost
- **B.** 127.0.0.1 on the laptop only
- **C.** host.docker.internal is always required
- **D.** db (the service name)

??? success "Reveal answer"
    **Correct answer: D**

    Inside the Compose network, use the service name. `localhost` is the container itself.

    **Related concepts**

    - Compose networking

### Question 16

What does `docker build --pull` help with?

**Difficulty:** Intermediate

**Options:**

- **A.** Deleting all images
- **B.** Refreshing base images from the registry before build
- **C.** Pushing secrets to Docker Hub
- **D.** Disabling BuildKit

??? success "Reveal answer"
    **Correct answer: B**

    `--pull` reduces surprise from stale cached base tags.

    **Related concepts**

    - docker build

### Question 17

Which statement about secrets in images is true?

**Difficulty:** Intermediate

**Options:**

- **A.** Prefer runtime secrets (env at deploy, secret mounts); never commit secrets into layers
- **B.** Baking API keys into ENV in the image is safe if the image is private forever
- **C.** Secrets in layers cannot be extracted
- **D.** LABEL is the standard secret store

??? success "Reveal answer"
    **Correct answer: A**

    Image layers and history leak secrets. Use runtime injection.

    **Related concepts**

    - Secrets
    - Image layers

### Question 18

`docker system prune` mainly removes what?

**Difficulty:** Intermediate

**Options:**

- **A.** Only running containers
- **B.** The host operating system
- **C.** Unused data (stopped containers, dangling images/networks — depending on flags)
- **D.** Kubernetes etcd

??? success "Reveal answer"
    **Correct answer: C**

    Prune reclaims unused Docker objects; be careful with `-a` and volumes flags.

    **Related concepts**

    - prune

### Question 19

EXPOSE 8080 in a Dockerfile means:

**Difficulty:** Beginner

**Options:**

- **A.** The port is published to the host automatically
- **B.** Firewall rules are opened on the host
- **C.** TLS is enabled
- **D.** Metadata documenting the intended listen port; publishing still needs -p or Compose ports

??? success "Reveal answer"
    **Correct answer: D**

    EXPOSE does not publish ports by itself.

    **Related concepts**

    - EXPOSE

### Question 20

Which Compose pattern waits until a dependency is healthy before starting a service?

**Difficulty:** Intermediate

**Options:**

- **A.** links: (legacy) alone guarantees health
- **B.** depends_on with condition: service_healthy
- **C.** restart: always
- **D.** stdin_open: true

??? success "Reveal answer"
    **Correct answer: B**

    Modern Compose can wait on health conditions via depends_on.

    **Related concepts**

    - depends_on
    - Healthchecks

## Section 3 — Scenario-Based Questions

### Question 21

Staging: `web` returns 502. `api` runs. `API_URL=http://api.internal:8080` but Compose service is `api`. Likely fix?

**Difficulty:** Intermediate

**Options:**

- **A.** Use http://api:8080 (service DNS name) and matching ports
- **B.** Reboot the laptop twice
- **C.** Delete all volumes immediately
- **D.** Switch to :latest everywhere

??? success "Reveal answer"
    **Correct answer: A**

    Compose DNS uses service names, not invented hostnames unless you add aliases.

    **Related concepts**

    - Compose DNS
    - 502 upstream

### Question 22

Container exits immediately with code 0. What do you check first?

**Difficulty:** Intermediate

**Options:**

- **A.** Buy a new SSD
- **B.** Disable IPv6 globally
- **C.** Whether the main process exited (CMD/ENTRYPOINT finished) — inspect logs and command
- **D.** Remove HEALTHCHECK only

??? success "Reveal answer"
    **Correct answer: C**

    Exit 0 means the PID 1 process ended successfully — often a mis-set command.

    **Related concepts**

    - PID 1
    - CMD vs ENTRYPOINT

### Question 23

Image build is slow every CI run. Highest-impact improvement?

**Difficulty:** Intermediate

**Options:**

- **A.** Disable BuildKit permanently
- **B.** Copy the entire repo before any RUN apt
- **C.** Use --no-cache always
- **D.** Put rarely changing dependency installs before frequently changing COPY of app code; use cache mounts where appropriate

??? success "Reveal answer"
    **Correct answer: D**

    Layer ordering maximises cache hits.

    **Related concepts**

    - Build cache
    - CI performance

### Question 24

You must run a one-off migration using the same image/env as `api` in Compose.

**Difficulty:** Intermediate

**Options:**

- **A.** Edit production DB from a browser extension
- **B.** docker compose run --rm api <migration command>
- **C.** docker kill -9 $(docker ps -q)
- **D.** Rebuild without network forever

??? success "Reveal answer"
    **Correct answer: B**

    `compose run` starts a one-off container with service config.

    **Related concepts**

    - compose run

### Question 25

Registry push fails with authentication error. First checks?

**Difficulty:** Beginner

**Options:**

- **A.** docker login and correct image name/registry host
- **B.** Disable TLS on the public Internet
- **C.** Use telnet to port 80 only
- **D.** Delete local Docker Desktop settings blindly

??? success "Reveal answer"
    **Correct answer: A**

    Auth and repository naming are the usual causes.

    **Related concepts**

    - Registries
    - docker login

### Question 26

Container TLS errors with skewed clocks. Least bad approach?

**Difficulty:** Advanced

**Options:**

- **A.** Disable TLS verification permanently
- **B.** Set date inside every container manually each hour
- **C.** Ensure host clock/NTP is correct; avoid privileged time hacks unless required
- **D.** Use HTTP only in production

??? success "Reveal answer"
    **Correct answer: C**

    Fix host time; do not disable TLS verification.

    **Related concepts**

    - TLS
    - NTP

### Question 27

Security review: container runs as root and mounts docker.sock. Risk?

**Difficulty:** Advanced

**Options:**

- **A.** Low — docker.sock is read-only by nature
- **B.** None if the image is alpine
- **C.** Only a problem on Windows
- **D.** High — docker.sock access can equate to host root control

??? success "Reveal answer"
    **Correct answer: D**

    Mounting docker.sock is near-equivalent to root on the host.

    **Related concepts**

    - docker.sock
    - Container escape

### Question 28

You changed compose.yaml env vars but behaviour is unchanged. Likely?

**Difficulty:** Intermediate

**Options:**

- **A.** Env vars never apply in Compose
- **B.** Need recreate: docker compose up -d --force-recreate (or up after change)
- **C.** Must reboot BIOS
- **D.** Only kubectl apply works

??? success "Reveal answer"
    **Correct answer: B**

    Existing containers keep old config until recreated.

    **Related concepts**

    - Recreate containers

### Question 29

Final stage is distroless/scratch and a dynamic binary misses libc. Symptom?

**Difficulty:** Advanced

**Options:**

- **A.** Runtime failures loading dynamic libraries — use static build or matching runtime base
- **B.** Faster DNS
- **C.** Automatic Kubernetes deploy
- **D.** Larger attack surface always

??? success "Reveal answer"
    **Correct answer: A**

    Dynamic binaries need compatible libs; static or proper base images fix this.

    **Related concepts**

    - Distroless
    - Static linking

### Question 30

Team wants identical images from laptop and CI. What helps most?

**Difficulty:** Intermediate

**Options:**

- **A.** Always build from :latest on Fridays
- **B.** Disable checksums
- **C.** Pin bases by digest, lock dependency versions, use consistent BuildKit behaviour
- **D.** Commit node_modules into the image randomly

??? success "Reveal answer"
    **Correct answer: C**

    Reproducibility comes from pinning and consistent build tooling.

    **Related concepts**

    - Reproducible builds

## Section 4 — Troubleshooting

### Question 31

`api` unhealthy; logs show connection refused to DB still starting. Best direction?

**Difficulty:** Intermediate

**Options:**

- **A.** Remove DB entirely
- **B.** Use host networking for everything always
- **C.** Ignore health and hope
- **D.** Add healthcheck on DB and depends_on condition service_healthy; fix race

??? success "Reveal answer"
    **Correct answer: D**

    Startup races are fixed with health-gated dependencies.

    **Related concepts**

    - Healthchecks
    - Race conditions

### Question 32

`docker run` fails: port is already allocated. Check with?

**Difficulty:** Beginner

**Options:**

- **A.** kubectl drain
- **B.** ss/lsof on the host port; change mapping or stop the conflicting process
- **C.** terraform destroy blindly
- **D.** rm -rf /

??? success "Reveal answer"
    **Correct answer: B**

    Host port conflicts are diagnosed with socket tools.

    **Related concepts**

    - Port conflicts

### Question 33

Build fails: `COPY package.json` not found. Cause?

**Difficulty:** Beginner

**Options:**

- **A.** Build context does not include the file (wrong path/context directory)
- **B.** Docker Hub is offline always
- **C.** YAML indentation in Compose only
- **D.** Missing Kubernetes Secret

??? success "Reveal answer"
    **Correct answer: A**

    COPY paths are relative to the build context.

    **Related concepts**

    - Build context
    - COPY

### Question 34

Container cannot resolve external DNS. Host browsing works. Likely Docker area?

**Difficulty:** Advanced

**Options:**

- **A.** Missing CPU shares
- **B.** Wrong Dockerfile LABEL
- **C.** Daemon DNS config / embedded DNS / network mode issues
- **D.** Absent HEALTHCHECK only

??? success "Reveal answer"
    **Correct answer: C**

    Container DNS is controlled by Docker networking configuration.

    **Related concepts**

    - Docker DNS

### Question 35

`permission denied` writing to a mounted volume on Linux. Common cause?

**Difficulty:** Intermediate

**Options:**

- **A.** Image name too short
- **B.** JSON logs disabled
- **C.** Compose version key aesthetic
- **D.** UID/GID inside container differs from host directory ownership

??? success "Reveal answer"
    **Correct answer: D**

    Align user IDs or ownership on bind mounts.

    **Related concepts**

    - UIDs
    - Volume permissions

## Section 5 — Architecture

### Question 36

For production containers, which default is best?

**Difficulty:** Intermediate

**Options:**

- **A.** Run as root with --privileged
- **B.** Non-root user, drop capabilities, read-only rootfs where possible, pin digests
- **C.** Mount docker.sock into every app
- **D.** Use :latest and hope

??? success "Reveal answer"
    **Correct answer: B**

    Least privilege and pinned artefacts are baseline production hygiene.

    **Related concepts**

    - Container security

### Question 37

When is Docker Compose appropriate vs Kubernetes?

**Difficulty:** Intermediate

**Options:**

- **A.** Compose for local/dev and simple single-host stacks; Kubernetes for multi-node orchestration and richer scheduling/self-healing
- **B.** Compose always replaces Kubernetes in global scale SaaS
- **C.** Kubernetes cannot run containers
- **D.** They are identical products

??? success "Reveal answer"
    **Correct answer: A**

    Choose orchestration complexity to match operational needs.

    **Related concepts**

    - Compose vs Kubernetes

### Question 38

CI builds images. Where should promotion to production registry happen?

**Difficulty:** Advanced

**Options:**

- **A.** From unverified developer laptops only
- **B.** By emailing tar files of images
- **C.** Through CI with scans/signing policies, promoting immutable digests
- **D.** By rewriting history on main with force

??? success "Reveal answer"
    **Correct answer: C**

    Controlled CI promotion with scanning is the norm.

    **Related concepts**

    - CI/CD
    - Image promotion

### Question 39

Logging strategy for containers?

**Difficulty:** Intermediate

**Options:**

- **A.** Write only inside ephemeral container layers and never collect
- **B.** SSH and tail files only, forever
- **C.** Disable all logs in production
- **D.** Log to stdout/stderr; collect via Docker logging drivers / platform agents

??? success "Reveal answer"
    **Correct answer: D**

    Twelve-factor style logging to stdout enables central collection.

    **Related concepts**

    - Logging drivers

### Question 40

Resource control on a noisy neighbour host?

**Difficulty:** Intermediate

**Options:**

- **A.** Ignore cgroups
- **B.** Set memory/CPU limits (compose deploy.resources / run flags) appropriate to SLOs
- **C.** Always --network host
- **D.** Remove healthchecks to free CPU

??? success "Reveal answer"
    **Correct answer: B**

    cgroup limits protect hosts and colocated workloads.

    **Related concepts**

    - cgroups
    - Resource limits

## Score Summary

| Score | Band | Meaning |
|------:|------|---------|
| 36–40 | Excellent | Ready for interviews and labs at this track level |
| 28–35 | Good | Pass — revise weak sections, then retry |
| 20–27 | Needs improvement | Revisit tutorials for missed topics before labs |
| ≤19 | Restart foundations | Work the track in order, then retake |

**Total questions:** 40 · **Passing score:** 28 (70%)

## Recommended Study Areas

Weak on Dockerfile/Compose → Docker track modules 2–4. Weak on failures → Troubleshooting tutorial + Compose stack recovery lab. Weak on hardening → Docker security tutorial.

- Track: [Docker](../docker/index.md)
- Lab: [Docker Compose Stack Recovery](../labs/docker-compose-stack-recovery.md)
- Cheat sheet: [Docker](../cheatsheets/docker.md)
- Interview prep: [Docker](../interview/docker.md)
- Path: [DevOps Engineer](../learning-paths/devops-engineer/)

## Interview Connection

Expect containers vs VMs, layer caching, Compose DNS (`localhost` vs service name), volumes vs bind mounts, and why `:latest` and baked secrets are dangerous.

## References

1. [Docker documentation](https://docs.docker.com/)
2. [Compose specification](https://docs.docker.com/compose/compose-file/)
3. [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
