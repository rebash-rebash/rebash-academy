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

<div class="ra-interview-qa" markdown="1">

## Core concepts

**1. What is Docker, and how is it different from a virtual machine?**

??? success "Reveal answer"
    **In short:** Docker packages apps as containers—isolated processes that share the host Linux kernel, unlike VMs that boot a full guest OS.
    
    **Key points**
    - Containers share the host kernel; VMs virtualise hardware and run a guest OS.
    - Containers start in seconds and pack denser; VMs give stronger isolation and their own kernel.
    - Images bundle app + libs + config so the same artefact runs from laptop to CI to production.
    - In production you often run containers on VMs (nodes) for defence in depth.
    
    **Try this**
    - `docker run --rm -it alpine uname -r`
    - `docker version`
    
    **Trap**
    - Do not claim containers fully replace VMs—escape risk targets the host kernel, not a hypervisor.

**2. What is a Dockerfile, and walk me through writing one for a Node.js application.**

??? success "Reveal answer"
    **In short:** A Dockerfile is a layer-by-layer recipe; for Node.js, pin a slim base, cache deps, then run as non-root.
    
    **Key points**
    - Copy package manifests before source so dependency layers stay cached.
    - Prefer multi-stage builds so build tools never ship in the final image.
    - Pin base tags or digests; set WORKDIR, EXPOSE, USER, and a clear CMD/ENTRYPOINT.
    - Use .dockerignore so node_modules and .git never enter the build context.
    
    **Try this**
    - `docker build -t myapp:dev .`
    - `docker run --rm -p 3000:3000 myapp:dev`
    
    **Trap**
    - Putting COPY . . before npm install busts the cache on every code change.

**3. How does Docker networking work, and what are the different network types?**

??? success "Reveal answer"
    **In short:** Docker attaches containers to virtual networks; bridge, host, none, and overlay cover most day-to-day cases.
    
    **Key points**
    - Default bridge gives private IPs and NAT to the outside world.
    - User-defined bridges add DNS by container name between attached containers.
    - host shares the host network stack; none has no networking; overlay spans Swarm/multi-host.
    - Publish ports with -p host:container; inspect with docker network inspect.
    
    **Try this**
    - `docker network ls`
    - `docker network create appnet`
    - `docker network inspect bridge`
    
    **Trap**
    - In Kubernetes you rarely manage Docker networks—the CNI plugin owns Pod networking.

**4. What are Docker volumes, and how do you persist data in containers?**

??? success "Reveal answer"
    **In short:** Volumes keep data outside the container writable layer so recreate does not wipe state.
    
    **Key points**
    - Named volumes are Docker-managed and move cleanly between containers on one host.
    - Bind mounts map a host path—great for local code, fragile for production paths/permissions.
    - Put databases and queues on volumes; never rely on the writable layer for persistence.
    - Back up with app-native tools (pg_dump) plus volume snapshots where available.
    
    **Try this**
    - `docker volume create pgdata`
    - `docker run -v pgdata:/var/lib/postgresql/data postgres:16`
    - `docker volume ls`
    
    **Trap**
    - Anonymous volumes and docker rm -v can silently delete data you thought was safe.

**5. Explain Docker layer caching and how to optimize Dockerfiles for faster CI/CD builds.**

??? success "Reveal answer"
    **In short:** Each Dockerfile instruction can produce a cached layer; order instructions so the expensive layers change least often.
    
    **Key points**
    - A cache miss rebuilds that layer and every layer after it.
    - Install deps before copying app source; keep RUN steps small and ordered by change frequency.
    - Use BuildKit cache mounts for package managers in CI.
    - Push/pull remote cache with buildx --cache-from/--cache-to when runners are ephemeral.
    
    **Try this**
    - `docker buildx build --cache-from type=registry,ref=myreg/app:cache -t myapp:ci .`
    
    **Trap**
    - COPY . . early invalidates almost every following layer on each commit.

**6. What is Layered file system/Union file system?**

??? success "Reveal answer"
    **In short:** A layered (union) filesystem stacks read-only image layers under one writable container layer as a single tree.
    
    **Key points**
    - Reads walk top-down; writes use copy-on-write into the container layer.
    - Shared layers across images save disk and pull time.
    - On modern Linux Docker, overlay2 is the usual storage driver.
    - Keep mutable state on volumes—writable-layer growth hurts performance and cleanup.
    
    **Try this**
    - `docker history <image>`
    - `docker image inspect <image> --format '{{.GraphDriver.Name}}'`
    
    **Trap**
    - docker commit of a dirty writable layer creates unreproducible snowflake images.

**7. Difference between Docker and VMware?**

??? success "Reveal answer"
    **In short:** Docker isolates processes with namespaces and cgroups on a shared kernel; VMware runs full guest OSes on a hypervisor.
    
    **Key points**
    - Containers are lighter and faster to start; VMs isolate kernels and device models.
    - Docker images are built from Dockerfiles and run via a runtime (often containerd/runc).
    - Escape models differ: container escape → host kernel; VM escape → hypervisor.
    - Many estates use both: VMs for nodes, containers for apps.
    
    **Try this**
    - `docker info | grep -i runtime`
    
    **Trap**
    - Saying “containers are always more secure than VMs” is a common interview fail.

**8. What is a Dockerfile and why do we use it?**

??? success "Reveal answer"
    **In short:** A Dockerfile is a version-controlled build script (FROM, RUN, COPY, USER, CMD…) so images are reproducible and reviewable.
    
    **Key points**
    - Same file builds the same way on a laptop and in CI.
    - Pull requests can review image changes, not just app code.
    - Pin bases, run non-root, and keep the final image minimal.
    - Validate with lint, plain-progress builds, and a smoke run under docker stop.
    
    **Try this**
    - `docker build -t registry.example.com/app:<gitsha> .`
    
    **Trap**
    - Embedding secrets in RUN/ENV layers leaves them in image history forever.

**9. Explain a typical Docker application workflow.**

??? success "Reveal answer"
    **In short:** Typical flow: code → Dockerfile → build → test locally → push digest → deploy → observe → next Git SHA.
    
    **Key points**
    - CI builds and scans on merge; GitOps or a pipeline rolls the digest into the cluster.
    - Prefer immutable digests over floating tags for deploy.
    - Compose helps local multi-service stacks; production often uses Kubernetes or ECS.
    - Rollback means redeploying a known-good digest, not rebuilding from memory.
    
    **Try this**
    - `docker build -t app:$(git rev-parse --short HEAD) .`
    - `docker push <registry>/app@sha256:<digest>`
    
    **Trap**
    - Deploying :latest makes rollbacks and unplanned upgrades guesswork.

**10. You are unable to push docker image to dockerhub due to access issue. What are the sources where you can push your docker image other than dockerhub?**

??? success "Reveal answer"
    **In short:** Push to any OCI-compatible registry—ECR, Artifact Registry, ACR, GHCR, GitLab, Quay, Harbor, or self-hosted registry:2.
    
    **Key points**
    - Prefer private registries for proprietary images with scanning and IAM.
    - Authenticate with cloud CLIs or registry tokens, then tag and push.
    - Failures are usually IAM scope, missing repo, wrong region, or TLS/proxy—not “Docker is broken”.
    - Mirror approved bases inward for air-gapped or regulated estates.
    
    **Try this**
    - `aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com`
    - `docker tag app:1 <account>.dkr.ecr.<region>.amazonaws.com/app:1`
    - `docker push <account>.dkr.ecr.<region>.amazonaws.com/app:1`
    
    **Trap**
    - Leaving images on a laptop registry “for now” breaks every other environment.

**11. What is Registry server in Docker?**

??? success "Reveal answer"
    **In short:** A registry stores and serves image manifests and layer blobs over HTTPS—an artefact store, not a runtime.
    
    **Key points**
    - docker pull/push talk to a registry; Docker Hub is one public option.
    - Enterprises use ECR, ACR, Artifact Registry, Harbor, or Distribution.
    - Harden with auth, immutable tags, retention policies, and vulnerability scanning.
    - Prefer digest pulls (repo/app@sha256:…) for reproducible deploys.
    
    **Try this**
    - `docker pull nginx:alpine`
    - `docker push <registry>/app:1.2.3`
    
    **Trap**
    - Treating the registry as “just storage” without lifecycle policies blows cost and attack surface.

**12. Difference between COPY and ADD commands in a Dockerfile?**

??? success "Reveal answer"
    **In short:** Prefer COPY for predictable file copies; ADD adds magic (tar auto-extract, historically remote URLs) that hurts review and cache clarity.
    
    **Key points**
    - COPY copies from the build context into the image—use it for source and config.
    - ADD can auto-extract local tarballs; that surprise often breaks cache expectations.
    - Fetch remote artefacts with an explicit RUN curl/wget when you must.
    - Interview default: COPY unless you deliberately need ADD’s extract behaviour.
    
    **Try this**
    - `# COPY package.json .`
    - `# ADD app.tar.gz /opt/app`
    
    **Trap**
    - Using ADD for every file invites unnoticed tar extraction and harder supply-chain review.

**13. Difference between bind mounts and volumes in Docker?**

??? success "Reveal answer"
    **In short:** Named volumes are Docker-managed storage; bind mounts point at an exact host path you choose.
    
    **Key points**
    - Volumes suit production data on a single Docker host without hard-coding host dirs.
    - Bind mounts suit live code in development and one-off host file injection.
    - Bind mounts inherit host path permissions and break when paths differ between machines.
    - Inspect Mounts to prove what is attached before blaming the app.
    
    **Try this**
    - `docker volume create data`
    - `docker run -v data:/data alpine`
    - `docker inspect <container> --format '{{json .Mounts}}'`
    
    **Trap**
    - Confusing bind mounts with volumes leads to “works on my laptop” data loss in CI/prod.

**14. What is the issue with using large file image in dockerfile?**

??? success "Reveal answer"
    **In short:** Large files in an image inflate every pull, slow CI, raise registry cost, and worsen cold starts.
    
    **Key points**
    - Multi-stage builds copy only the final binary or assets.
    - Aggressive .dockerignore and slim bases cut context and layers.
    - Serve huge static assets from object storage, not the image.
    - Audit with docker history and tools like dive.
    
    **Try this**
    - `docker history <image>`
    - `du -sh .`
    
    **Trap**
    - Leaving build caches, SDKs, or test data in the final stage is the usual bloat source.

**15. Difference between entrypoint and cmd in docker?**

??? success "Reveal answer"
    **In short:** CMD sets default args you can override easily; ENTRYPOINT sets the main executable that args append to.
    
    **Key points**
    - Common pattern: ENTRYPOINT ["myapp"] plus CMD ["--serve"].
    - Prefer JSON exec form so the app is PID 1 and gets SIGTERM.
    - Override entrypoint only with --entrypoint when you must.
    - Shell form hides signals behind /bin/sh and breaks graceful shutdown.
    
    **Try this**
    - `docker run --rm myapp --help`
    - `docker run --entrypoint sh myapp -c 'id'`
    
    **Trap**
    - Shell-form ENTRYPOINT/CMD is why many containers ignore docker stop grace periods.

**16. What is the difference between copy and run command in docker?**

??? success "Reveal answer"
    **In short:** COPY adds files from the build context; RUN executes a build-time command and commits a new layer.
    
    **Key points**
    - COPY does not execute what it copies.
    - RUN installs packages, compiles, or prepares the filesystem.
    - Order COPY of manifests before RUN install for cache wins.
    - Never use RUN to “echo secrets into files” that survive in layers.
    
    **Try this**
    - `# COPY requirements.txt .`
    - `# RUN pip install -r requirements.txt`
    
    **Trap**
    - RUN with secrets without BuildKit secret mounts leaks credentials into image history.

**17. What is Docker and how do you use in your project, Any docker file you have written?**

??? success "Reveal answer"
    **In short:** Docker is how I package and run services consistently; I write Dockerfiles for apps and sidecars used from CI to prod.
    
    **Key points**
    - Typical Dockerfile: pinned base, non-root USER, healthcheck-friendly CMD, multi-stage for compiled apps.
    - Locally I use Compose for app + DB; CI builds, scans, and pushes digests.
    - Deploy consumes the digest via Kubernetes, ECS, or Compose—not a laptop tag.
    - I treat .dockerignore and image scanning as part of the definition of done.
    
    **Try this**
    - `docker compose up --build`
    - `docker images`
    
    **Trap**
    - “I only use Docker on my laptop” signals you have not closed the loop to deploy.

**18. What is difficulties you face while you build a docker image?**

??? success "Reveal answer"
    **In short:** Build pain usually comes from cache busts, fat contexts, flaky network installs, and architecture mismatches—not mystery Docker bugs.
    
    **Key points**
    - Huge contexts (.git, node_modules) slow every build—fix with .dockerignore.
    - Unpinned bases or “latest” deps make CI non-reproducible.
    - amd64 vs arm64 mismatches fail on Apple Silicon or Graviton nodes.
    - Private registry auth and TLS interception break pulls mid-build.
    
    **Try this**
    - `docker build --progress=plain -t app:debug .`
    - `docker buildx ls`
    
    **Trap**
    - Retrying without --progress=plain hides the real failing RUN line.

**19. What is difference between add and copy in docker file?**

??? success "Reveal answer"
    **In short:** Same as COPY vs ADD: use COPY by default; ADD only when you want its tar-extract behaviour on purpose.
    
    **Key points**
    - COPY is explicit and cache-friendly for source and config.
    - ADD may auto-extract archives—easy to misuse.
    - Prefer RUN + curl for remote downloads with checksums.
    - Consistency across Dockerfiles beats clever ADD shortcuts.
    
    **Trap**
    - Interviewers often use this question to see if you blindly recite “ADD is bad” without knowing why.

**20. What is the purpose of Docker?**

??? success "Reveal answer"
    **In short:** Docker’s purpose is to package, ship, and run applications with predictable dependencies and isolation on a shared kernel.
    
    **Key points**
    - Eliminates “works on my machine” library drift.
    - Enables immutable artefacts for CI/CD and rollbacks.
    - Improves density versus one VM per app.
    - Pairs with orchestrators for scale, health, and scheduling.
    
    **Try this**
    - `docker run --rm hello-world`
    
    **Trap**
    - Docker alone is not an orchestrator—HA and scheduling need Compose Swarm, Kubernetes, or a cloud service.

**21. What is a multi-stage Docker build? How does it help reduce image size?**

??? success "Reveal answer"
    **In short:** Multi-stage builds compile or install in one stage, then copy only runtime artefacts into a slim final image.
    
    **Key points**
    - Final image drops compilers, caches, and test toolchains.
    - Smaller attack surface and faster pulls/cold starts.
    - Ideal for Go, Java, .NET, Rust, and Node build pipelines.
    - Name stages (AS build) and COPY --from=build for clarity.
    
    **Try this**
    - `docker build -t app:slim .`
    - `docker image ls app`
    
    **Trap**
    - Copying the whole build directory into the final stage undoes the size win.

**22. What is Docker image layer caching?**

??? success "Reveal answer"
    **In short:** Image layer caching reuses unchanged instruction results so rebuilds skip work until the first changed layer.
    
    **Key points**
    - Cache key includes instruction text and parent layer identity.
    - Stable early layers (OS packages, deps) speed CI dramatically.
    - BuildKit improves caching with mounts and remote caches.
    - Changing a base digest invalidates everything below it—pin deliberately.
    
    **Try this**
    - `docker builder prune -f`
    - `docker build --no-cache -t app:nocache .`
    
    **Trap**
    - --no-cache everywhere “to be safe” destroys CI speed without improving correctness.

**23. What is docker compose depends_on?**

??? success "Reveal answer"
    **In short:** depends_on controls start order in Compose; it does not wait for the dependency to be ready unless you add health conditions.
    
    **Key points**
    - Classic depends_on only starts containers in order.
    - Compose healthcheck + condition: service_healthy waits for readiness.
    - Apps should still retry DB connections—order alone is not enough.
    - In Kubernetes, use probes and init containers instead of Compose depends_on.
    
    **Try this**
    - `docker compose up`
    - `docker compose ps`
    
    **Trap**
    - Assuming depends_on means “Postgres is accepting queries” causes flaky startup races.

**24. What is the role of container runtime and which runtime do you use and why?**

??? success "Reveal answer"
    **In short:** The container runtime actually creates and runs containers; Docker Engine today usually talks to containerd, which uses runc (or similar).
    
    **Key points**
    - Runtime implements OCI runtime specs: namespaces, cgroups, filesystem.
    - Kubernetes often uses containerd or CRI-O via the CRI—not the Docker CLI.
    - I use containerd/runc in production clusters for simplicity and CRI support.
    - Know which runtime your nodes use when debugging pull/start failures.
    
    **Try this**
    - `docker info | grep -i runtime`
    - `crictl version`
    
    **Trap**
    - Saying “Kubernetes needs Docker Desktop” is outdated for most production clusters.

**25. What are the layer's you will get in Docker while building?**

??? success "Reveal answer"
    **In short:** Build layers mirror Dockerfile instructions—typically base FROM, then each RUN/COPY/ADD—plus the final config metadata.
    
    **Key points**
    - docker history shows the instruction stack and approximate sizes.
    - Empty or tiny layers still exist when instructions only change metadata.
    - Shared base layers are reused across images on the same host/registry.
    - Optimise by merging noisy RUN steps carefully without hurting cache.
    
    **Try this**
    - `docker history --no-trunc <image>`
    
    **Trap**
    - Counting “10 layers” from memory without history output is guesswork.

**26. What is docker file what is inside it?**

??? success "Reveal answer"
    **In short:** A Dockerfile lists instructions that build an image: base image, packages, files, env, user, ports, and start command.
    
    **Key points**
    - Core instructions: FROM, RUN, COPY, ENV, EXPOSE, USER, ENTRYPOINT, CMD.
    - Optional: ARG, HEALTHCHECK, WORKDIR, LABEL, VOLUME.
    - Keep one concern per stage in multi-stage files.
    - Comments and labels should document provenance, not hide secrets.
    
    **Try this**
    - `docker build -t demo .`
    
    **Trap**
    - A Dockerfile without USER (runs as root) is a common security finding.

**27. What is an init container and why do we need to use it?**

??? success "Reveal answer"
    **In short:** Init containers (Kubernetes) run to completion before app containers start—use them for setup, waits, and permission fixes.
    
    **Key points**
    - They share volumes with the Pod but run sequentially first.
    - Good for waiting on dependencies, migrating schemas (carefully), or templating config.
    - Failing init containers block the Pod from becoming Ready.
    - Docker Compose has no native init containers—use entrypoint scripts or health waits.
    
    **Try this**
    - `kubectl describe pod <pod>`
    - `kubectl logs <pod> -c <init-container>`
    
    **Trap**
    - Long or flaky init work without timeouts leaves Pods stuck Pending/Init forever.

## Scenarios and troubleshooting

**28. How would you use Python in a Dockerized DevOps environment?**

??? success "Reveal answer"
    **In short:** Use Python images to run automation, CLIs, and services with pinned deps; prefer slim/multi-stage and non-root.
    
    **Key points**
    - Pin python:3.x-slim and requirements with hashes where practical.
    - Separate build (pip wheel) and runtime stages for smaller images.
    - Mount config/secrets at runtime; do not bake credentials into layers.
    - In DevOps, containerise lint/test/deploy tools for reproducible pipelines.
    
    **Try this**
    - `docker build -t pytools:1 .`
    - `docker run --rm -v "$PWD":/work -w /work pytools:1 pytest`
    
    **Trap**
    - Copying a host virtualenv into the image breaks across architectures and glibc versions.

**29. Jenkins is failing to push a Docker image to the registry. How do you troubleshoot?**

??? success "Reveal answer"
    **In short:** Treat a failed Jenkins push as auth, tag, network, or registry policy—verify login and the exact docker/buildah error first.
    
    **Key points**
    - Confirm registry URL, credentials (IAM/token), and that the repository exists.
    - Check tag format and whether the job pushes the image it just built.
    - Inspect agent disk, proxy/TLS, and rate limits.
    - Re-run a manual login/push from the same agent identity to isolate Jenkins vs registry.
    
    **Try this**
    - `docker login <registry>`
    - `docker push <registry>/<repo>:<tag>`
    
    **Trap**
    - Rotating registry passwords in the UI but not in the Jenkins credential store causes silent auth loops.

**30. If you have 10 layers in a Dockerfile and layer 6 fails, after fixing it, where will the rebuild start from and why?**

??? success "Reveal answer"
    **In short:** After fixing layer 6, the rebuild reuses cache for layers 1–5 and rebuilds from layer 6 onward.
    
    **Key points**
    - Cache hits require identical instruction text and parent layer.
    - Changing layer 6 invalidates 6 through 10 even if 7–10 look unchanged.
    - BuildKit remote cache follows the same invalidation idea across runners.
    - Reorder stable steps earlier so fixes lower in the file hurt less.
    
    **Try this**
    - `docker build -t app:rebuild .`
    
    **Trap**
    - Editing an ARG used early can invalidate far more than the line you “fixed”.

**31. Docker containers stopped suddenly after starting, how do you troubleshoot?**

??? success "Reveal answer"
    **In short:** Sudden stops usually mean the main process exited—read exit code and logs before restarting in a loop.
    
    **Key points**
    - docker ps -a shows STATUS and exit codes (137 ≈ OOM/SIGKILL, 143 ≈ SIGTERM).
    - Check logs, inspect RestartPolicy, and resource limits.
    - Bad CMD, missing env, failing healthcheck, or dependency race are common.
    - Reproduce with docker run --rm and the same env/mounts.
    
    **Try this**
    - `docker ps -a`
    - `docker logs <container>`
    - `docker inspect <container> --format '{{.State.ExitCode}} {{.State.OOMKilled}}'`
    
    **Trap**
    - Restarting without reading OOMKilled hides memory-limit kills as “flaky app”.

**32. How do you debug inside the container?**

??? success "Reveal answer"
    **In short:** Debug with logs first, then exec into a running container—or a debug sidecar/ephemeral container when distroless.
    
    **Key points**
    - docker logs / kubectl logs for stdout/stderr.
    - docker exec -it <ctr> sh (or bash) when a shell exists.
    - Inspect env, mounts, DNS, and listening ports from inside.
    - Prefer ephemeral debug containers over baking shells into production images.
    
    **Try this**
    - `docker exec -it <container> sh`
    - `docker logs --tail 200 -f <container>`
    
    **Trap**
    - Installing debug tools permanently in every production image expands attack surface.

**33. Why does a container sometimes exit immediately even though the application works perfectly in local testing? Give 3 real production causes?**

??? success "Reveal answer"
    **In short:** Immediate exits often come from wrong CMD, missing runtime config, or signal/PID 1 issues—even when local non-container runs work.
    
    **Key points**
    - CMD/ENTRYPOINT points at a script that is not executable or uses Windows CRLF.
    - Required env/files/secrets exist on the laptop but not in the container.
    - App expects a TTY or interactive stdin that docker run -d does not provide.
    - Bonus: binding to 127.0.0.1 inside the container makes healthchecks and publishes look “dead”.
    
    **Try this**
    - `docker run --rm -it --entrypoint sh <image>`
    - `docker logs <container>`
    
    **Trap**
    - Blaming Docker networking first when the process never stayed up wastes time.

## Practice questions

**34. How do you design and manage a containerized environment to ensure scalability and high availability?**

??? success "Reveal answer"
    **In short:** Scale and HA come from multiple replicas behind a load balancer, health probes, and capacity planning—not one long-lived container.
    
    **Key points**
    - Run N replicas across nodes/AZs with an orchestrator (Kubernetes/ECS).
    - Stateless app tiers; externalise state to managed DB/cache/object storage.
    - Readiness gates traffic; liveness restarts stuck processes carefully.
    - Autoscaling on saturation metrics plus PodDisruptionBudgets for drains.
    
    **Try this**
    - `kubectl get deploy,pods -o wide`
    - `docker compose up --scale web=3`
    
    **Trap**
    - Single-replica “HA” with a host volume is still a single point of failure.

**35. How do you create and manage Docker images and containers?**

??? success "Reveal answer"
    **In short:** Build images from Dockerfiles, tag/push to a registry, then create containers with run/Compose and manage lifecycle via stop/rm/logs.
    
    **Key points**
    - Build: docker build / buildx; tag with Git SHA or semver.
    - Run: publish ports, mounts, env, and restart policies as needed.
    - Inspect and clean with ps, logs, inspect, and system prune carefully.
    - In teams, CI owns build/push; runtime platforms own scheduling.
    
    **Try this**
    - `docker build -t app:1.0.0 .`
    - `docker run -d --name app -p 8080:8080 app:1.0.0`
    - `docker rm -f app`
    
    **Trap**
    - Manual docker commit workflows bypass review and break reproducibility.

**36. What do you mean by port mapping in Docker?**

??? success "Reveal answer"
    **In short:** Port mapping publishes a container port on the host (or load balancer) so external clients can reach the service.
    
    **Key points**
    - -p 8080:80 maps host 8080 to container 80.
    - Without publish/expose routing, the service stays on the container network only.
    - In Kubernetes, Services/Ingress replace ad-hoc -p on nodes.
    - Conflicts occur when two containers bind the same host port.
    
    **Try this**
    - `docker run -d -p 8080:80 nginx:alpine`
    - `ss -lntp | grep 8080`
    
    **Trap**
    - Mapping 0.0.0.0 on a laptop demo can accidentally expose admin UIs on shared networks.

**37. How do you fix security issues in Docker images?**

??? success "Reveal answer"
    **In short:** Fix image security by shrinking and scanning images, running non-root, and patching bases on a cadence.
    
    **Key points**
    - Use minimal/distroless bases and multi-stage builds.
    - Scan in CI (Trivy/Grype) and fail on critical CVEs with a fix path.
    - Drop capabilities, read-only rootfs where possible, and no secrets in layers.
    - Rebuild regularly—stale bases accumulate vulnerabilities even if app code is unchanged.
    
    **Try this**
    - `trivy image <image>`
    - `docker scout cves <image>`
    
    **Trap**
    - Suppressing CVE gates forever without tracking exceptions is not a security programme.

**38. What do you mean by docker image?**

??? success "Reveal answer"
    **In short:** A Docker image is an immutable packaged filesystem plus metadata (config, exposed ports, default command) stored as layered blobs.
    
    **Key points**
    - Built from a Dockerfile or imported; addressed by name:tag or digest.
    - Containers are running (or created) instances of an image.
    - Images are pushed/pulled via registries.
    - Digests identify exact content; tags can move.
    
    **Try this**
    - `docker image ls`
    - `docker image inspect <image>`
    
    **Trap**
    - Equating “image” with “container” confuses debugging and rollback talk.

**39. How do you reduce docker image size?**

??? success "Reveal answer"
    **In short:** Shrink images with slim bases, multi-stage copies, aggressive .dockerignore, and fewer package installs in the final stage.
    
    **Key points**
    - Prefer alpine/distroless/chainguard where compatible.
    - Delete build caches in the same RUN that installs them if single-stage.
    - Avoid shipping docs, tests, and SDKs to production.
    - Measure before/after with docker images and history.
    
    **Try this**
    - `docker images app`
    - `docker history app:latest`
    
    **Trap**
    - Microdnf/apk “cleanup” in a later layer does not shrink earlier layers—you must combine RUN steps or multi-stage.

**40. How do you reduce the size of a Docker image?**

??? success "Reveal answer"
    **In short:** Same discipline as size reduction: multi-stage, minimal base, no leftover package caches, and only runtime files in the final image.
    
    **Key points**
    - COPY --from=build the binary or built assets only.
    - Pin and prune OS packages; avoid debug tools in prod tags.
    - Compress static assets outside the image when possible.
    - Automate size budgets in CI so regressions fail the build.
    
    **Try this**
    - `docker build -t app:small .`
    - `docker image ls app:small`
    
    **Trap**
    - Squashing layers for vanity size numbers can destroy useful cache and provenance.

**41. How do you implement Docker image layer caching?**

??? success "Reveal answer"
    **In short:** Implement caching by ordering Dockerfile instructions for stability and enabling BuildKit cache backends in CI.
    
    **Key points**
    - Deps before source; pin bases; avoid bouncing ARG values early.
    - Use --mount=type=cache for package managers.
    - Registry cache export/import across ephemeral runners.
    - Keep .dockerignore tight so context hashes stay stable.
    
    **Try this**
    - `DOCKER_BUILDKIT=1 docker build -t app:ci .`
    - `docker buildx build --cache-to type=inline -t app:ci --push .`
    
    **Trap**
    - Caching mount contents that include secrets can leak into later jobs on shared runners.

**42. How do you get logs from docker level?**

??? success "Reveal answer"
    **In short:** Container logs are the process stdout/stderr—fetch with docker logs (or the platform’s log driver / cluster agent).
    
    **Key points**
    - docker logs -f/--tail for local Engine containers.
    - json-file is common locally; production often uses journald or a shipper.
    - On Kubernetes, use kubectl logs or the cluster logging stack.
    - Structure logs as JSON and avoid secrets in stdout.
    
    **Try this**
    - `docker logs --tail 100 -f <container>`
    - `docker inspect <container> --format '{{.HostConfig.LogConfig.Type}}'`
    
    **Trap**
    - docker logs vanishes if the container was removed and the logging driver did not ship elsewhere.

**43. How do you check the integrity of a Docker image or file?**

??? success "Reveal answer"
    **In short:** Verify integrity with content digests, checksums of artefacts, and signature/provenance tooling—not just a tag name.
    
    **Key points**
    - Compare registry digest (sha256) to what you deployed.
    - Checksum downloaded files before ADD/COPY into builds.
    - Use signing (cosign) and admission policy in stricter estates.
    - docker pull by digest pins exact bits.
    
    **Try this**
    - `docker buildx imagetools inspect <image>`
    - `sha256sum <file>`
    
    **Trap**
    - Trusting a mutable :latest tag is not an integrity check.

**44. How do you configure a pipeline with AWS or Docker?**

??? success "Reveal answer"
    **In short:** A typical pipeline builds and scans an image, pushes to a registry (often ECR), then deploys a digest to the target environment.
    
    **Key points**
    - Build on Git commit; tag with SHA; scan; push to ECR/GHCR/etc.
    - Deploy via kubectl/Helm/Argo CD or ECS task definition update.
    - Store credentials in the CI secret store / IAM roles—not in the Dockerfile.
    - Promote digests across envs instead of rebuilding per environment when possible.
    
    **Try this**
    - `aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com`
    
    **Trap**
    - Building differently per environment (“prod Dockerfile”) creates untested artefacts.

**45. If Docker containers are consuming too much disk space, how do you fix it?**

??? success "Reveal answer"
    **In short:** Reclaim Docker disk with targeted prune of unused images, build cache, and volumes—after confirming nothing still needs them.
    
    **Key points**
    - docker system df shows where space went.
    - Prune dangling images and build cache regularly in CI agents.
    - Remove unused volumes only when data is disposable.
    - Cap log size for json-file drivers on busy hosts.
    
    **Try this**
    - `docker system df`
    - `docker system prune -af`
    - `docker volume prune`
    
    **Trap**
    - docker volume prune on a shared host can delete persistent DB volumes you still need.

**46. How do you provide security in docker?**

??? success "Reveal answer"
    **In short:** Secure Docker by least privilege in images and runtime: non-root, minimal capabilities, scanned bases, and secrets at runtime.
    
    **Key points**
    - USER non-root; drop Linux capabilities; read-only rootfs when feasible.
    - No secrets in ENV/layers; use runtime mounts or secret managers.
    - Keep Engine/socket access tightly controlled—socket access is root-equivalent.
    - Scan and patch continuously; network only what the app needs.
    
    **Try this**
    - `docker run --read-only --cap-drop=ALL --security-opt=no-new-privileges ...`
    
    **Trap**
    - Exposing /var/run/docker.sock to random containers is a common privilege-escalation gift.

**47. How do you scan Docker images—both during build and at the registry level? Are you using any extensions or tools for image scanning?**

??? success "Reveal answer"
    **In short:** Scan in CI on every build and again at the registry; gate merges on severity with a tracked exception process.
    
    **Key points**
    - CI tools: Trivy, Grype, Docker Scout, Snyk—fail the pipeline on criticals.
    - Registry scanning (ECR/ACR/Harbor/Artifact Registry) catches drift after push.
    - Rebuild bases on a schedule; do not only scan app layers.
    - Admission controllers can block unscanned or critical images at deploy time.
    
    **Try this**
    - `trivy image --severity HIGH,CRITICAL <image>`
    - `aws ecr describe-image-scan-findings --repository-name <repo> --image-id imageTag=<tag>`
    
    **Trap**
    - Scanning only locally once never covers the image that actually runs in production.

**48. How do you pass environment variables during Docker build commands? What services do you use for storing Docker images?**

??? success "Reveal answer"
    **In short:** Pass build-time values with --build-arg (non-secrets); store images in ECR/GHCR/ACR/Harbor—not with secrets baked into ARG/ENV.
    
    **Key points**
    - ARG for version pins and feature toggles that are not confidential.
    - Use BuildKit secret mounts for tokens needed at build time.
    - Runtime config belongs in env/files injected at run/orchestrator time.
    - Image stores: Amazon ECR, GHCR, ACR, Artifact Registry, Harbor.
    
    **Try this**
    - `docker build --build-arg APP_VERSION=1.2.3 -t app:1.2.3 .`
    - `docker buildx build --secret id=npm,src=$HOME/.npmrc -t app .`
    
    **Trap**
    - --build-arg PASSWORD=... still lands in image history and build logs.

**49. How do you manage and version Docker images stored in Amazon ECR?**

??? success "Reveal answer"
    **In short:** In ECR, version with immutable Git SHA tags plus optional semver; promote digests and apply lifecycle policies for cleanup.
    
    **Key points**
    - Tag every build with Git SHA; optionally also vMAJOR.MINOR.PATCH.
    - Prefer deploy-by-digest; keep mutable tags like staging for humans only.
    - Lifecycle policies expire untagged and old feature tags.
    - Scan on push and require IAM least privilege for push/pull.
    
    **Try this**
    - `aws ecr put-lifecycle-policy --repository-name app --lifecycle-policy-text file://policy.json`
    - `docker push <account>.dkr.ecr.<region>.amazonaws.com/app:<gitsha>`
    
    **Trap**
    - Overwriting the same floating tag in ECR without immutability makes rollbacks dishonest.

**50. Multi stage docker build. In which scenarios it would be useful. Is is suitable for compile based language?**

??? success "Reveal answer"
    **In short:** Multi-stage builds shine for compiled languages (Go, Java, .NET, Rust, C/C++) and heavy front-end builds—copy only the runtime output forward.
    
    **Key points**
    - Build stage has SDK/compiler; final stage has JRE/static binary/nginx assets.
    - Also useful for Node when you need npm build but not npm tooling at runtime.
    - Cuts size, CVE surface, and pull time.
    - Less critical for tiny interpreted scripts with no build step—but still fine for consistency.
    
    **Try this**
    - `docker build -t svc:1 .`
    
    **Trap**
    - Using multi-stage but copying the entire /build tree into the final image wastes the pattern.

## Related
- Course: [Docker](../docker/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
