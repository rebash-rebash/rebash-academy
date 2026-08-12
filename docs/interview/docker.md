---
title: "Docker Interview Preparation"
description: "50 curated Docker interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: docker
tags:
  - interview
  - docker
comments: false
---

{% raw %}
# Docker Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. What is Docker, and how is it different from a virtual machine?**

??? success "Reveal answer"
    Docker is a platform for building, running, and managing containers — lightweight, portable, 
    self-contained units of software that include everything needed to run an application: code, 
    runtime, system libraries, and configuration. 
    The core difference between containers and VMs: 
    A Virtual Machine includes an entire operating system kernel, device drivers, and virtualized 
    hardware. It's like renting an entire apartment building just for yourself. 
    A Docker container shares the host operating system's kernel. It only packages the application 
    and its dependencies. It's like renting just your apartment in a shared building. 
    Virtual Machine Stack: Docker Container Stack: 
    
     
    Practical differences: 
    Feature 
    Virtual Machine 
    Docker Container 
    Startup time 
    Minutes 
    Milliseconds to seconds 
    Size 
    Gigabytes 
    Megabytes 
    OS included 
    Yes (full) 
    No (shares host kernel) 
    Isolation level 
    Strong (hypervisor) 
    Process-level 
    Portability 
    Moderate 
    Excellent 
    Resource overhead 
    High 
    Very low 
    When VMs are still better: When you need strong security isolation…

**2. What is a Dockerfile, and walk me through writing one for a Node.js application.**

??? success "Reveal answer"
    A Dockerfile is a text file containing instructions that Docker follows to build a container image.
    Think of it as a recipe — it describes exactly what goes into your container, layer by layer.
    Here's a production-quality Dockerfile for a Node.js application:
    # Stage 1: Build stage
    # We use a specific version tag (not 'latest') for reproducibility
    FROM node:18-alpine AS builder
    # Set working directory inside the container
    WORKDIR /app
    # Copy dependency files FIRST (before source code)
    # This is a critical optimisation — Docker caches this layer
    # and only re-runs npm install when package files change
    
    COPY package.json package-lock.json ./
    # Install dependencies
    # --ci uses the lockfile exactly (more deterministic than npm install)
    RUN npm ci --only=production
    # Stage 2: Runtime stage
    # Use a minimal base image for the final container
    FROM node:18-alpine AS runtime
    # Security best practice: Don't run as root
    # Create a non-root user
    RUN addgroup -S appgroup && adduser -S appuser -G appgroup
    WORKDIR /app
    # Copy only the installed dependencies from builder…

**3. How does Docker networking work, and what are the different network types?**

??? success "Reveal answer"
    Docker networking is how containers communicate with each other and with the outside world. 
    Getting this right is crucial for multi-container applications. 
    Docker's built-in network drivers: 
    1. Bridge Network (default) When you run a container without specifying a network, it joins the 
    default bridge network. Containers on the same bridge can communicate using IP addresses, but 
    NOT by name (on the default bridge). 
    Creating a custom bridge network (recommended): 
    # Create a custom bridge network 
    docker network create --driver bridge my-app-network 
    # Run containers on this network 
    docker run -d --name postgres --network my-app-network postgres:14 
    docker run -d --name api-server \ 
     --network my-app-network \ 
     -e DB_HOST=postgres \ # Can use container name as hostname! 
     my-api-image 
    On custom bridge networks, containers can resolve each other by name. This is DNS-based 
    service discovery built into Docker. 
    2. Host Network The container shares the host's network namespace — no isolation. The 
    container uses the host's IP address and ports directly. 
    
    …

**4. What are Docker volumes, and how do you persist data in containers?**

??? success "Reveal answer"
    Containers are ephemeral by design — when a container is removed, all data written inside it 
    disappears. Volumes solve this problem by providing persistent storage that exists 
    independently of containers. 
    Three ways to persist data: 
    1. Named Volumes (Recommended) Docker manages the storage location on the host. 
    # Create a named volume 
    docker volume create postgres-data 
    # Mount it when running the container 
    docker run -d \ 
     --name postgres \ 
     -v postgres-data:/var/lib/postgresql/data \ 
     -e POSTGRES_PASSWORD=secret \ 
     postgres:14 
    # Inspect the volume 
    docker volume inspect postgres-data 
    # The data persists even if you remove and recreate the container 
    docker rm -f postgres 
    docker run -d \ 
     --name postgres-new \ 
     -v postgres-data:/var/lib/postgresql/data \ # Same volume, data intact! 
     postgres:14 
    
     
    2. Bind Mounts Mount a specific directory from the host into the container. Useful in 
    development. 
    # Mount current directory into container (live code reload in development) 
    docker run -d \ 
     --name dev-server \ 
     -v $(pwd)/src:/app/src \ # Host…

**5. Explain Docker layer caching and how to optimize Dockerfiles for faster CI/CD builds.**

??? success "Reveal answer"
    Docker builds images in layers, where each instruction (FROM, COPY, RUN, etc.) creates a new layer.
    Docker caches these layers — if nothing has changed in a layer, Docker reuses the cached version
    instead of rebuilding it. Understanding this is what makes the difference between a 30-second
    build and a 15-minute build.
    The golden rule: Order instructions from least-changed to most-changed.
    Bad Dockerfile (cache is invalidated on every code change):
    FROM node:18-alpine
    WORKDIR /app
    # WRONG: Copying all files first means ANY file change
    # invalidates the npm install cache
    COPY . .
    RUN npm install
    CMD ["node", "index.js"]
    Every time you change a single line of application code, Docker has to re-run npm install from
    scratch.
    Optimized Dockerfile:
    FROM node:18-alpine
    WORKDIR /app
    # CORRECT: Copy only dependency files first
    COPY package.json package-lock.json ./
    # This layer is cached unless package.json changes
    
    RUN npm ci
    # Copy source code last — changes here don't invalidate npm cache
    COPY src/ ./src/
    CMD ["node", "src/index.js"]
    Advanced: Multi-stage builds with…

**6. What is Layered file system/Union file system?**

??? success "Reveal answer"
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    Inside a docker container, whatever we do (creating files, directories, installing packages) forms a
    new layer. This is called the Layered File System. Each layer takes less space. When we create a
    docker image from this container, all these layers form unity — that's why we also call it Union File
    System. If we create a container from this docker image, we can see all those files, directories and
    packages (environment replication).

**7. Difference between Docker and VMware?**

??? success "Reveal answer"
    VMware uses a complete OS which is GBs in size. Docker image size is only MBs — it takes less
    space and fewer base machine resources. Docker image is a compressed version of OS.
    VMware has pre-allocation of RAM (blocked whether used or not). Docker has no pre-allocation of
    RAM — it takes RAM during runtime as needed and releases it when done. So you need less RAM for
    Docker compared to VMware.

**8. What is a Dockerfile and why do we use it?**

??? success "Reveal answer"
    A Dockerfile is a normal text file with instructions to build a docker image. It is the automated way of
    creating docker images. In this file, we mention the required OS image and all required software as
    instructions. Once we build the Dockerfile, Docker creates a container in the background, creates the
    image from that container, and then destroys the container automatically.

**9. Explain a typical Docker application workflow.**

??? success "Reveal answer"
    Developers create a Dockerfile and build an image using docker build. The image is
    tested and pushed to a registry. During deployment, the image is pulled and run as a
    container, with networks, volumes, ports, and environment variables configured as required.
    –− Stay Connected:
    Join this account for more useful information:
    Telegram → Join Channel
    Instagram → Follow Page
    □
    ›

**10. You are unable to push docker image to dockerhub due to access issue. What are the sources where you can push your docker image other than dockerhub?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Docker, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**11. What is Registry server in Docker?**

??? success "Reveal answer"
    Registry server is our own Docker Hub created to store private docker images instead of storing in the
    public Docker Hub. Registry server is one of the docker containers created from the 'registry' image
    provided by Docker specifically for creating a private Docker Hub. We can store any number of private
    docker images and grant access to others as needed.

**12. Difference between COPY and ADD commands in a Dockerfile?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**13. Difference between bind mounts and volumes in Docker?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**14. What is the issue with using large file image in dockerfile?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**15. difference between entrypoint and cmd in docker?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**16. what is the difference between copy and run command in docker?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**17. What is Docker and how do you use in your project, Any docker file you have written?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**18. What is difficulties you face while you build a docker image?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**19. what is difference between add and copy in docker file?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**20. What is the purpose of Docker?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**21. What is a multi-stage Docker build? How does it help reduce image size?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**22. What is Docker image layer caching?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**23. what is docker compose depends_on?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**24. What is the role of container runtime and which runtime do you use and why?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**25. What are the layer's you will get in Docker while building?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**26. What is docker file what is inside it?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**27. What is an init container and why do we need to use it?**

??? success "Reveal answer"
    Start with a precise definition in the context of Docker, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

## Scenarios and troubleshooting

**28. How would you use Python in a Dockerized DevOps environment?**

??? success "Reveal answer"
    Python often is the application logic running inside containers, and separately, the Docker SDK for Python lets me
    manage containers programmatically -- pulling images and running containers directly from a script -- which I've used
    to automate deployment or orchestration tasks beyond plain docker CLI commands.
    Closing Note
    This is the exhaustive edition — all 303 questions across every topic in the source question bank, from networking
    and subnetting fundamentals through AWS, Azure, Git, CI/CD, Docker, Kubernetes internals, Terraform, Ansible,
    monitoring, security, Jenkins, Linux, SonarQube, Trivy, Selenium, Nexus, GitLab, and Python for DevOps. Every
    answer is written the way I'd actually say it out loud in an interview, so treat this as a full rehearsal script: adapt the
    specifics to your own project experience before you walk in.
    Compiled and elaborated by Arvind Verma.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**29. Jenkins is failing to push a Docker image to the registry. How do you troubleshoot?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Docker, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**30. If you have 10 layers in a Dockerfile and layer 6 fails, after fixing it, where will the rebuild start from and why?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Docker, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**31. Docker containers stopped suddenly after starting, how do you troubleshoot?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Docker, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**32. How do you debug inside the container ?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Docker, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**33. Why does a container sometimes exit immediately even though the application works perfectly in local testing? Give 3 real production causes?**

??? success "Reveal answer"
    Answer directly for Docker: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

## Practice questions

**34. [ ] How do you design and manage a containerized environment to ensure scalability and high availability?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Docker components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**35. How do you create and manage Docker images and containers?**

??? success "Reveal answer"
    I write a Dockerfile specifying the base image, copying application code, installing dependencies, and setting the
    entry point, then build it with docker build -t my-app:1.0 . and push it to a registry with docker push. To manage
    running containers I use docker run to start one, docker stop/start to control its lifecycle, docker rm to remove it, and
    Docker Compose when I need to define and run multiple containers together.

**36. What do you mean by port mapping in Docker?**

??? success "Reveal answer"
    Docker containers don't have an IP address. To expose a web application running inside a container,
    we use Docker port mapping. We map the host port with the container port, and customers use the
    public IP of the host machine. Their request is routed from the host port to the container's port, loading
    the web page running inside the docker container.
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers

**37. How do you fix security issues in Docker images?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Docker, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**38. What do you mean by docker image?**

??? success "Reveal answer"
    Docker image is a lightweight OS provided by Docker company. We can get any type of docker image
    from Docker Hub. We use these docker images to create docker containers. A docker image may
    contain only OS, or OS + other software. Each software in a docker image is stored in the form of a
    layer. Advantage: we can replicate the same environment any number of times.

**39. How do you reduce docker image size?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Docker components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**40. How do you reduce the size of a Docker image?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Docker components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**41. How do you implement Docker image layer caching?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Docker components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**42. How do you get logs from docker level?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Docker components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**43. How do you check the integrity of a Docker image or file?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Docker components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**44. How do you configure a pipeline with AWS or Docker?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Docker components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**45. If Docker containers are consuming too much disk space, how do you fix it?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Docker components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**46. How do you provide security in docker?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Docker components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**47. Are you aware of security scanning tools? How do you scan Docker images—both during build and at the registry level? Are you using any extensions or tools for image scanning?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Docker components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**48. How do you pass environment variables during Docker build commands? What services do you use for storing Docker images?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Docker components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**49. How do you manage and version Docker images stored in Amazon ECR?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Docker components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**50. Multi stage docker build. In which scenarios it would be useful. Is is suitable for compile based language?**

??? success "Reveal answer"
    Answer directly for Docker: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

## Related

- Course: [Docker](../docker/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
