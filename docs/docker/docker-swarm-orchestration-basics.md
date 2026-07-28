---
title: Docker Swarm Orchestration Basics
description: Initialize a Swarm cluster, deploy replicated services, roll updates, manage secrets and configs, and understand when Swarm fits vs Kubernetes.
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
category: docker
tags:
  - docker
  - swarm
  - orchestration
  - clustering
prerequisites:
  - Production Docker Patterns
  - Docker Compose Fundamentals
  - Docker Networking Fundamentals
comments: false
---

# Docker Swarm Orchestration Basics

## Overview

**Docker Swarm** turns a pool of Docker engines into a single virtual cluster. You declare desired state — which image, how many replicas, which network — and Swarm schedules tasks, restarts failures, and rolling-updates services. Swarm is built into Docker Engine, simpler than Kubernetes, and ideal for small-to-medium deployments or edge clusters.

This is **Tutorial 18** in **Module 6: Production & Beyond** of the REBASH Academy Docker track.

## Prerequisites

- [Production Docker Patterns](production-docker-patterns.md)
- [Docker Compose Fundamentals](docker-compose-fundamentals.md)
- [Docker Networking Fundamentals](docker-networking-fundamentals.md)
- Three Linux VMs or local machines with Docker Engine 24+ (one manager, two workers minimum for lab)
- Open ports: TCP 2377 (cluster management), 7946 TCP/UDP (node communication), 4789 UDP (overlay network)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Initialize a Swarm and join worker nodes securely
- [ ] Deploy replicated and global services with `docker service`
- [ ] Configure overlay networks, published ports, and service discovery
- [ ] Perform rolling updates and rollbacks
- [ ] Manage secrets and configs in Swarm
- [ ] Deploy a multi-service stack from a Compose file with `docker stack deploy`

## Architecture Diagram

```d2
direction: down

Managers: Managers {
        M1: "Manager 1 - Leader"
        M2: "Manager 2"
    }
    Workers: Workers {
        W1: "Worker 1"
        W2: "Worker 2"
    }
    Swarm: Objects {
      style: {
        fill: "#e3f2fd"
        stroke: "#1976d2"
      }
        SVC: "Service api:3 replicas"
        T1: Task
        T2: Task
        T3: Task
        NET: "Overlay network"
        SEC: "Secrets / Configs"
    }
    Managers.M1 -> Managers.M2
    Managers.M1 -> Workers.W1
    Managers.M1 -> Workers.W2
    Swarm.SVC -> Swarm.T1
    Swarm.SVC -> Swarm.T2
    Swarm.SVC -> Swarm.T3
    Swarm.T1 -> Workers.W1
    Swarm.T2 -> Workers.W2
    Swarm.T3 -> Workers.W1
    Swarm.NET -> Swarm.T1
    Swarm.SEC -> Swarm.SVC
```

## Theory

### Swarm vs single-host Docker

| Capability | Single host | Swarm cluster |
|------------|-------------|---------------|
| Scheduling | Manual | Automatic across nodes |
| Failover | Restart policy only | Reschedule tasks on healthy nodes |
| Scaling | Manual duplicate runs | `docker service scale api=5` |
| Updates | Stop/start manually | Rolling update with parallelism |
| Secrets | Files/env on host | Encrypted raft store, mounted in tasks |
| Networking | Bridge per host | Multi-host overlay networks |

### Core terminology

| Term | Definition |
|------|------------|
| **Node** | A Docker engine participating in the Swarm (manager or worker) |
| **Manager** | Runs raft consensus; schedules services; typically 3 or 5 for HA |
| **Worker** | Executes tasks assigned by managers |
| **Service** | Desired state: image, replicas, update policy |
| **Task** | A running container slot assigned to a node |
| **Stack** | Group of services deployed from a Compose file |

### Service modes

| Mode | Behavior | Example |
|------|----------|---------|
| **replicated** | N identical tasks across cluster | Web API with 3 replicas |
| **global** | One task per node | Log agent, monitoring exporter |

### Raft and manager quorum

Swarm managers use **Raft** for cluster state. Loss of quorum (majority of managers) halts scheduling.

| Managers | Tolerated failures |
|----------|-------------------|
| 1 | 0 (dev/lab only) |
| 3 | 1 |
| 5 | 2 |

Never run an even number of managers — use 1, 3, or 5.

### Overlay networks

**Overlay** driver creates a VXLAN network spanning all Swarm nodes. Services on the same overlay resolve each other by **service name** via embedded DNS.

```bash
docker network create -d overlay mynet
```

Attach services to `mynet`; tasks communicate without publishing host ports internally.

### Secrets and configs

| Object | Mutable | Use case |
|--------|---------|----------|
| **Secret** | No (immutable) | Passwords, TLS keys, API tokens |
| **Config** | Version by replace | nginx.conf, app.yml |

Secrets mount as files in `/run/secrets/` inside tasks — never in image layers or env vars for sensitive data.

### Compose vs stack deploy

`docker compose up` targets one host. **`docker stack deploy`** targets Swarm — interprets Compose v3 `deploy:` keys (replicas, placement, update_config). Not all Compose features work in stacks (e.g., `build:` is ignored — push images to a registry first).

## Hands-on Lab

### Lab 1 — Bootstrap a Swarm cluster

On the first manager node:

```bash
# Initialize Swarm — note the join token output
docker swarm init --advertise-addr 192.168.1.10

# Save tokens
docker swarm join-token worker
docker swarm join-token manager
```

On each worker:

```bash
docker swarm join --token SWMTKN-1-xxx... 192.168.1.10:2377
```

Verify from manager:

```bash
docker node ls
```

Expected columns: HOSTNAME, STATUS, AVAILABILITY, MANAGER STATUS, ENGINE VERSION.

Label a node for placement:

```bash
docker node update --label-add role=db node-worker-1
```

### Lab 2 — Deploy a replicated service

```bash
docker service create \
  --name web \
  --replicas 3 \
  --publish published=8080,target=80 \
  --network webnet \
  nginx:1.27-alpine

docker network create -d overlay webnet   # if not exists

docker service ls
docker service ps web
curl http://192.168.1.10:8080   # any manager/worker IP with published port
```

Scale:

```bash
docker service scale web=5
docker service ps web --no-trunc
```

Inspect service spec:

```bash
docker service inspect web --pretty
```

### Lab 3 — Rolling update and rollback

Deploy versioned service:

```bash
docker service create --name api --replicas 4 --publish 3000:3000 myapi:1.0.0

# Update image with controlled rollout
docker service update \
  --image myapi:1.1.0 \
  --update-parallelism 1 \
  --update-delay 10s \
  --update-failure-action rollback \
  api

# Monitor update progress
docker service ps api

# Manual rollback if needed
docker service rollback api
```

| Update flag | Purpose |
|-------------|---------|
| `--update-parallelism` | Tasks updated at once |
| `--update-delay` | Pause between batches |
| `--update-failure-action rollback` | Auto rollback on failure |

### Lab 4 — Secrets and configs

```bash
echo "supersecret-db-pass" | docker secret create db_password -
echo "server { listen 80; location / { return 200 'ok'; } }" | docker config create nginx_cfg -

docker service create \
  --name secure-api \
  --secret db_password \
  --config source=nginx_cfg,target=/etc/nginx/conf.d/default.conf \
  --replicas 2 \
  myapi:1.1.0

# Verify secret mount inside task
TASK_ID=$(docker ps -q --filter name=secure-api | head -1)
docker exec "$TASK_ID" ls -la /run/secrets/
```

Secrets are only available to services granted access at create/update time.

### Lab 5 — Stack deploy from Compose

`stack-api.yml`:

```yaml
services:
  api:
    image: myapi:1.1.0
    ports:
      - "3000:3000"
    networks:
      - backend
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          cpus: "0.50"
          memory: 256M
    secrets:
      - db_password
    environment:
      DB_HOST: db

  db:
    image: postgres:16-alpine
    networks:
      - backend
    deploy:
      placement:
        constraints:
          - node.labels.role == db
      replicas: 1
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - db-data:/var/lib/postgresql/data

networks:
  backend:
    driver: overlay

secrets:
  db_password:
    external: true

volumes:
  db-data:
```

Deploy:

```bash
docker stack deploy -c stack-api.yml myapp
docker stack services myapp
docker stack ps myapp
```

Remove stack:

```bash
docker stack rm myapp
```

## Commands & Code

### Essential Swarm commands

```bash
# Cluster
docker swarm init | join | leave
docker node ls | inspect | update | rm

# Services
docker service create | ls | ps | inspect | update | scale | rm | logs

# Stacks
docker stack deploy | ls | ps | services | rm

# Secrets & configs
docker secret create | ls | rm
docker config create | ls | rm

# Networks
docker network create -d overlay NAME
```

### Drain a node for maintenance

```bash
docker node update --availability drain node-worker-2
docker node ps node-worker-2    # tasks rescheduled elsewhere
# perform maintenance
docker node update --availability active node-worker-2
```

### Service discovery test

From any task on the overlay network:

```bash
docker exec -it TASK_ID sh
wget -qO- http://api:3000/health
```

Service name `api` resolves to all healthy task IPs (VIP load balancing).

## Common Mistakes

!!! warning "Single manager in production"
    Manager loss means no orchestration. Run 3 managers across failure domains.

!!! warning "Using docker compose up on Swarm nodes"
    Compose ignores `deploy:` keys without Swarm mode. Use `docker stack deploy`.

!!! warning "Building images in stack files"
    Stack deploy ignores `build:`. CI must push images; stack references registry tags.

!!! warning "Publishing every service port"
    Only edge services need published ports. Internal services use overlay DNS.

!!! warning "Ignoring placement constraints"
    Stateful workloads (DB) on random nodes lose data on reschedule. Use labels and volumes with backup strategy.

## Best Practices

!!! tip "Odd number of managers"
    Maintain raft quorum — 3 managers for most production Swarm clusters.

!!! tip "Pin images by tag or digest"
    Same discipline as CI/CD — avoid `latest` in service specs.

!!! tip "Use health checks in service definition"
    Unhealthy tasks are replaced automatically during updates and runtime.

!!! tip "Centralize logs and metrics"
    Swarm does not include full observability. Integrate Prometheus, Loki, or ELK.

!!! tip "Plan exit strategy"
    Swarm maintenance mode is real — know when to migrate to [Kubernetes](from-docker-to-kubernetes.md).

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `docker swarm init` fails | Wrong advertise-addr | Use reachable IP, not 127.0.0.1 |
| Tasks pending | No worker capacity | Add nodes; check `docker node ls` |
| Overlay network isolated | Firewall blocks 4789/7946 | Open UDP 4789, TCP/UDP 7946 |
| Service not reachable | Wrong publish mode | Use `ingress` mode; verify port |
| Secret not mounted | Service not updated after secret create | Recreate service with `--secret` |
| Quorum lost | Too many managers down | Restore from backup or rebuild cluster |

## Summary

- **Docker Swarm** provides native clustering with services, tasks, and overlay networking
- **Managers** run Raft consensus; use **3 or 5** for production quorum
- **`docker service`** declares replicated or global workloads with rolling updates
- **Secrets and configs** distribute sensitive and static data without baking into images
- **`docker stack deploy`** maps Compose files to Swarm with `deploy:` semantics
- Swarm bridges single-host Docker and full orchestration — next step: [From Docker to Kubernetes](from-docker-to-kubernetes.md)

## Interview Questions

1. What is the difference between a Docker service and a container?
2. How does Swarm achieve multi-host networking?
3. Why should production Swarm clusters have an odd number of managers?
4. What happens during a rolling update with `--update-failure-action rollback`?
5. How are Swarm secrets delivered to containers?
6. What is the difference between `docker compose up` and `docker stack deploy`?
7. When would you choose Swarm over Kubernetes?
8. How do you safely drain a node for maintenance?
9. What ports must be open between Swarm nodes?
10. How does service discovery work for Swarm services?

??? tip "Sample Answers (Questions 1 and 7)"

    **Q1 — Service vs container:** A container is a single running instance on one host. A Swarm **service** is the desired state (image, replicas, networks, update policy). Swarm schedules **tasks** — each task runs one container on a chosen node. Scaling a service to 5 means 5 tasks across the cluster, managed as a unit.

    **Q7 — Swarm vs Kubernetes:** Choose Swarm when teams already know Docker, cluster size is modest (tens of nodes), requirements fit built-in primitives, and operational simplicity matters. Choose Kubernetes when you need a rich ecosystem (CRDs, operators, service mesh), massive scale, multi-cloud portability, or long-term vendor-neutral skills demand.

## Related Tutorials

- [Production Docker Patterns](production-docker-patterns.md) *(previous)*
- [From Docker to Kubernetes](from-docker-to-kubernetes.md) *(next)*
- [Docker Compose Fundamentals](docker-compose-fundamentals.md)
- [Docker Networking Fundamentals](docker-networking-fundamentals.md)
- [Environment Variables and Secrets](environment-variables-and-secrets.md)
- [Docker – Category Overview](index.md)

## References

- [Docker – Swarm mode overview](https://docs.docker.com/engine/swarm/)
- [Docker – Create a service](https://docs.docker.com/engine/swarm/services/)
- [Docker – Manage swarm security](https://docs.docker.com/engine/swarm/swarm_manager_locking/)
- [Docker – Secrets](https://docs.docker.com/engine/swarm/secrets/)
- [Docker – Stack deploy](https://docs.docker.com/engine/swarm/stack_deploy/)
- [Compose – Deploy specification](https://docs.docker.com/compose/compose-file/deploy/)
