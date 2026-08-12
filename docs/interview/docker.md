---
title: "Docker Interview Preparation"
description: "50 curated interview questions and model answers for Docker — concepts, scenarios, troubleshooting, and production trade-offs."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

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

**6. What is Trivy, and how do you scan Docker images for vulnerabilities in a pipeline?**

??? success "Reveal answer"
    Trivy is an open-source vulnerability scanner that scans: 
    • 
    Container images (OS packages, language dependencies) 
    • 
    Filesystems and Git repositories 
    • 
    Kubernetes clusters 
    • 
    Infrastructure as Code (Terraform, CloudFormation) 
    
     
    # GitHub Actions — Trivy image scanning 
    - name: Run Trivy vulnerability scanner 
     uses: aquasecurity/trivy-action@master 
     with: 
     image-ref: '${{ env.ECR_REGISTRY }}/${{ env.ECR_REPOSITORY }}:${{ 
    github.sha }}' 
     format: 'sarif' 
     output: 'trivy-results.sarif' 
     severity: 'CRITICAL,HIGH' 
     exit-code: '1' # Fail the pipeline if CRITICAL or HIGH vulnerabilities 
    found 
     ignore-unfixed: true # Ignore if no fix is available yet 
    - name: Upload Trivy scan results to GitHub Security 
     uses: github/codeql-action/upload-sarif@v3 
     if: always() 
     with: 
     sarif_file: 'trivy-results.sarif' 
    Running Trivy locally: 
    # Scan a Docker image 
    trivy image --severity CRITICAL,HIGH nginx:latest 
    # Scan a local filesystem 
    trivy fs --security-checks vuln,secret . 
    # Scan a running Kubernetes cluster 
    trivy k8s --report summary cluster 
    # Scan…

**7. What is Layered file system/Union file system?**

??? success "Reveal answer"
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    Inside a docker container, whatever we do (creating files, directories, installing packages) forms a
    new layer. This is called the Layered File System. Each layer takes less space. When we create a
    docker image from this container, all these layers form unity — that's why we also call it Union File
    System. If we create a container from this docker image, we can see all those files, directories and
    packages (environment replication).

**8. What is OS-Level Virtualization?**

??? success "Reveal answer"
    It is the unique feature of Docker not available in other virtualization software. Docker takes most
    UNIX features from the host machine OS and only takes extra layers of the required OS as a docker
    image. For the core UNIX kernel, it depends on host OS (since UNIX kernel is the same across UNIX
    and Linux flavors). Docker takes host OS virtually — that's why we call this concept OS-Level
    Virtualization.

**9. What is the importance of volumes in Docker?**

??? success "Reveal answer"
    • Volume is a directory inside your container
    • First declare directory as a volume and then share volume
    • Even if we stop the container, still we can access the volume
    • Volume will be created in one container
    • You can share one volume across any number of containers
    • Volume will not be included when you update an image
    • Map volumes in two ways: Share host-container or Share container-container

**10. Difference between Docker and VMware?**

??? success "Reveal answer"
    VMware uses a complete OS which is GBs in size. Docker image size is only MBs — it takes less
    space and fewer base machine resources. Docker image is a compressed version of OS.
    VMware has pre-allocation of RAM (blocked whether used or not). Docker has no pre-allocation of
    RAM — it takes RAM during runtime as needed and releases it when done. So you need less RAM for
    Docker compared to VMware.

**11. What is a Dockerfile and why do we use it?**

??? success "Reveal answer"
    A Dockerfile is a normal text file with instructions to build a docker image. It is the automated way of
    creating docker images. In this file, we mention the required OS image and all required software as
    instructions. Once we build the Dockerfile, Docker creates a container in the background, creates the
    image from that container, and then destroys the container automatically.

**12. What is a container?**

??? success "Reveal answer"
    The container is like a virtual machine in which we can deploy any type of applications, software and
    libraries. It is a lightweight virtual machine which uses OS in the form of an image, which is much
    smaller in size compared to traditional VMware and Oracle VirtualBox OS images. Container word has
    been taken from shipping containers. It has everything to run an application.

**13. Explain a typical Docker application workflow.**

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

**14. What is Registry server in Docker?**

??? success "Reveal answer"
    Registry server is our own Docker Hub created to store private docker images instead of storing in the
    public Docker Hub. Registry server is one of the docker containers created from the 'registry' image
    provided by Docker specifically for creating a private Docker Hub. We can store any number of private
    docker images and grant access to others as needed.

**15. What are the ways to create docker images?**

??? success "Reveal answer"
    There are three ways to create docker images:
    • Directly from Docker Hub — provided by Docker company and community
    • From your own docker containers — create container from base image, install required software
    inside, then create image from that container
    • From a Dockerfile — the most preferred way of creating docker images

**16. What is Docker?**

??? success "Reveal answer"
    Docker is a tool using which we create containers in less time. Docker uses lightweight OS in the form
    of docker images obtained from Docker Hub. Docker is open source and became very popular
    because of its unique virtualization concept called 'Containerization'. We can use Docker in both
    Windows and Linux machines.

**17. What is Docker workflow?**

??? success "Reveal answer"
    First we create a Dockerfile with instructions to build a docker image. From this docker image, we
    create docker containers. This docker image can also be pushed to Docker Hub and pulled by others
    to create containers. We can create docker images from docker containers as well. This is the
    workflow of Docker.

**18. What is Docker Security?**

??? success "Reveal answer"
    Docker provides isolation between containers, but containers are not the same as 
    complete virtual machines. Security can be improved by using minimal images, non-root 
    users, trusted images, and regularly updated dependencies. Secrets should also be handled 
    securely rather than hardcoded in images.

**19. What are the benefits of Docker?**

??? success "Reveal answer"
    • Containerization (OS level virtualization) — No need for guest OS
    • No pre-allocation of RAM
    • Can replicate same environment
    • Less cost
    • Less weight (MBs in size)
    • Fast to fire up
    • Can run on physical/virtual/cloud
    • Can re-use (same image)
    • Can create containers in less time

**20. What is the difference between COPY and ADD in Dockerfile?**

??? success "Reveal answer"
    Both can copy files from the build context into an image. COPY is simpler and is 
    generally preferred for normal file copying. ADD has additional features such as extracting 
    local tar archives and supporting URLs, though URLs are generally better handled with other 
    tools.

**21. What is an ECR lifecycle policy?**

??? success "Reveal answer"
    Automatically removes old Docker images based on rules. 
    { 
     "rules": [{ 
     "rulePriority": 1, 
     "selection": { 
    
     
     "tagStatus": "untagged", 
     "countType": "sinceImagePushed", 
     "countUnit": "days", 
     "countNumber": 7 
     }, 
     "action": { "type": "expire" } 
     }] 
    }

**22. What is containerd?**

??? success "Reveal answer"
    A lightweight container runtime that manages the complete container lifecycle (pulling images, 
    creating containers, managing storage). Docker Engine uses containerd internally. Kubernetes 
    defaults to containerd directly via CRI (Container Runtime Interface).

**23. What is Docker Compose?**

??? success "Reveal answer"
    Docker Compose is used to define and run multiple containers as a single application. 
    Services, networks, volumes, and configurations are defined in a YAML file. It is commonly 
    used for applications containing frontend, backend, and database services.

**24. What is a Docker Health Check?**

??? success "Reveal answer"
    A health check allows Docker to determine whether a containerized application is 
    working correctly. It can be defined using the HEALTHCHECK instruction in a Dockerfile. This 
    is useful for monitoring application health and service dependencies.

**25. What is the difference between Docker and Virtual Machine?**

??? success "Reveal answer"
    A virtual machine includes a complete guest operating system, while containers share 
    the host OS kernel. Containers are generally lighter and start faster. VMs provide stronger 
    OS-level isolation but usually require more resources.

**26. What is docker-compose.override.yml?**

??? success "Reveal answer"
    An automatically merged override file for docker-compose.yml. Used to customize 
    configurations for local development without modifying the base compose file. Useful for adding 
    debug ports or changing environment variables locally.

**27. What is a Docker Environment Variable?**

??? success "Reveal answer"
    Environment variables are used to pass configuration values to containers without 
    hardcoding them into the image. They can be provided using -e or Compose files. Examples 
    include database URLs, usernames, and application settings.

**28. What is a Docker Container?**

??? success "Reveal answer"
    A container is a lightweight, isolated environment where an application runs. It contains 
    the application and its required dependencies. Containers share the host OS kernel, making 
    them faster and lighter than virtual machines.

**29. What is Docker Network?**

??? success "Reveal answer"
    Docker networking allows containers to communicate with each other and with external 
    systems. Containers on the same network can communicate using container or service 
    names. Common network types include bridge, host, and none.

**30. What is a Multi-stage Docker Build?**

??? success "Reveal answer"
    Multi-stage builds use multiple FROM instructions in one Dockerfile. One stage can build 
    the application, while another contains only the required runtime files. This helps create 
    smaller and more secure production images.

**31. What is a Docker .dockerignore file?**

??? success "Reveal answer"
    .dockerignore specifies files and directories that should not be sent to the Docker build 
    context. It can exclude files such as .git, logs, and unnecessary dependencies. This makes 
    builds faster and keeps images cleaner.

**32. What is Azure Container Registry (ACR), and how does it integrate with Azure DevOps?**

??? success "Reveal answer"
    ACR is a managed private Docker registry, and it integrates with Azure Pipelines so container images are built,
    pushed, and pulled as part of CI/CD -- a pipeline typically publishes to ACR right after a successful build.

**33. What is Dockerfile?**

??? success "Reveal answer"
    A Dockerfile is a text file containing instructions for building a Docker image. It defines 
    the base image, application files, dependencies, and commands. Common instructions 
    include FROM, COPY, RUN, CMD, and EXPOSE.

**34. What is a Docker volume vs a bind mount?**

??? success "Reveal answer"
    A volume is managed by Docker (stored in /var/lib/docker/volumes/), portable, and the 
    recommended way for persistent data. A bind mount links a specific host path to a container 
    path — tighter coupling to the host.

**35. What is the difference between CMD and ENTRYPOINT in a Dockerfile?**

??? success "Reveal answer"
    ENTRYPOINT defines the executable that always runs; it cannot be overridden (only 
    appended). CMD provides default arguments that can be overridden at docker run. 
    Together: ENTRYPOINT ["python"] + CMD ["app.py"].

**36. What is a distroless image?**

??? success "Reveal answer"
    A minimal container image that contains only the application and its runtime dependencies — no 
    shell, no package manager, no OS utilities. Reduces attack surface significantly. 
    Example: gcr.io/distroless/java.

**37. What is a database connection string best practice in containerized environments?**

??? success "Reveal answer"
    Store in Secrets Manager or Vault, inject at runtime via environment variable or volume mount. 
    Never hardcode in application code or Docker image. Use connection pooling to handle multiple 
    container instances.

**38. What is Docker's garbage collection?**

??? success "Reveal answer"
    Docker doesn't automatically delete unused images, containers, or volumes. You run docker 
    system prune manually or schedule it as a cron job. Kubernetes 
    uses imageGCHighThresholdPercent for automatic cleanup.

## Scenarios and troubleshooting

**39. How would you use Python in a Dockerized DevOps environment?**

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

**40. How do you optimize Docker images for production?**

??? success "Reveal answer"
    Smaller base images like alpine to cut size and reduce attack surface, multi-stage builds so build tools and
    dependencies never make it into the final image, minimizing layers by combining commands where it makes sense, a
    .dockerignore file to keep unnecessary files out of the build context, and ordering Dockerfile instructions to take
    advantage of layer caching -- rarely-changing steps like dependency installation before frequently-changing ones like
    copying source code.
    KEY POINTS TO MENTION
    • Small base images, multi-stage builds, minimal layers, .dockerignore, cache-aware instruction ordering

## Practice questions

**41. How do you create and manage Docker images and containers?**

??? success "Reveal answer"
    I write a Dockerfile specifying the base image, copying application code, installing dependencies, and setting the
    entry point, then build it with docker build -t my-app:1.0 . and push it to a registry with docker push. To manage
    running containers I use docker run to start one, docker stop/start to control its lifecycle, docker rm to remove it, and
    Docker Compose when I need to define and run multiple containers together.

**42. Important docker commands?**

??? success "Reveal answer"
    • docker ps — to see list of running containers
    • docker ps -a — to see list of all containers
    • docker images — to see list of all images
    • docker run — to create docker container
    • docker attach — to go inside container
    • docker stop — to stop container
    • docker start — to start container
    • docker commit — to create image out of docker container
    • docker rm — to delete container
    • docker rmi — to delete image
    Ansible

**43. What do you mean by port mapping in Docker?**

??? success "Reveal answer"
    Docker containers don't have an IP address. To expose a web application running inside a container,
    we use Docker port mapping. We map the host port with the container port, and customers use the
    public IP of the host machine. Their request is routed from the host port to the container's port, loading
    the web page running inside the docker container.
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers

**44. What do you mean by docker image?**

??? success "Reveal answer"
    Docker image is a lightweight OS provided by Docker company. We can get any type of docker image
    from Docker Hub. We use these docker images to create docker containers. A docker image may
    contain only OS, or OS + other software. Each software in a docker image is stored in the form of a
    layer. Advantage: we can replicate the same environment any number of times.

**45. How do you tag and push a Docker image to ECR?**

??? success "Reveal answer"
    aws ecr get-login-password --region ap-south-1 | \ 
     docker login --username AWS --password-stdin 123456789.dkr.ecr.ap-south-
    1.amazonaws.com 
    docker tag myapp:latest 123456789.dkr.ecr.ap-south-
    1.amazonaws.com/myapp:latest 
    docker push 123456789.dkr.ecr.ap-south-1.amazonaws.com/myapp:latest

**46. List of Docker components?**

??? success "Reveal answer"
    • Docker image: Contains OS (very small) + software
    • Docker Container: Machine created from Docker image
    • Dockerfile: Describes steps to create a docker image
    • Docker hub/registry: Stores all docker images publicly
    • Docker daemon: Docker service running at the backend

**47. How is Docker used in CI/CD?**

??? success "Reveal answer"
    Docker can package an application into the same environment used for testing and 
    deployment. A CI/CD pipeline can build an image, run tests, push the image to a registry, and 
    deploy it to a server. This makes application deployment more consistent and repeatable.

**48. Your Docker image build takes 20 minutes. How do you reduce it?**

??? success "Reveal answer"
    1. Add .dockerignore. 2) Reorder layers — copy package.json before source code. 3) Use 
    multi-stage builds. 4) Enable BuildKit cache mounts. 5) Use layer caching in CI (--cache-
    from). 6) Use a smaller base image (alpine). Target: under 5 minutes.

**49. How do you update a running container's image without downtime?**

??? success "Reveal answer"
    You don't update containers in-place. The correct approach is: pull new image, start new 
    container, redirect traffic, stop old container. Orchestrators (Docker Swarm, Kubernetes) handle 
    this automatically via rolling updates.

**50. How can you integrate Jenkins with other tools like Git, Maven, or Docker?**

??? success "Reveal answer"
    Through plugins -- the Git plugin to pull code from a repository, the Maven plugin for building Java projects, and the
    Docker plugin for building and deploying containers, all configured within a job or pipeline.

## Related

- Course: [Docker](../docker/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
