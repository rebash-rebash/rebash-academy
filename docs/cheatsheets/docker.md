    ---
    title: "Docker Cheat Sheet"
    description: "Quick-reference commands and patterns for the REBASH Academy Docker track."
    difficulty: beginner
    estimated_time: "10 min"
    author: Shaik Basha
    last_updated: "2026-07-28"
    category: cheatsheets
    tags:
      - cheatsheets
      - docker
    comments: false
    ---

    # Docker Cheat Sheet

    Scannable commands and patterns for the [Docker track](../docker/index.md). Prefer the full tutorials when you need *why*, not only *how*.

    ## Quick reference

    | Area | Commands / notes |
    |------|------------------|
    | Run | `docker run --rm -it image sh`; `-p`; `-e`; `-v` |
| Images | `docker build -t`; `docker images`; `docker rmi` |
| Containers | `docker ps -a`; `docker logs -f`; `docker exec -it` |
| Dockerfile | Multi-stage; non-root USER; `.dockerignore` |
| Compose | `docker compose up -d`; `logs`; `down -v` |
| Network | `docker network ls`; bridge vs host vs none |
| Volume | named volumes vs bind mounts; backup patterns |
| Registry | `docker login`; `push`/`pull`; digests vs tags |
| Debug | `docker inspect`; `stats`; healthchecks |
| Security | rootless; read-only rootfs; secrets not in ENV |

    ## Common mistakes

    - Copy-pasting without reading expected output
    - Skipping cleanup (leftover containers, state, or temp files)
    - Mixing production credentials into lab shells

    ## Related

    - Track: [Docker](../docker/index.md)
    - Start: [Docker introduction](../docker/introduction-to-containers-and-docker.md)
    - Interview bank: [Docker interview prep](../interview/docker.md)
    - Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)
