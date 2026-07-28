---
title: Docker Compose Fundamentals
description: Define multi-container applications with Compose — services, networks, volumes, environment files, and hands-on labs for web plus database stacks.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
category: docker
tags:
  - docker
  - docker-compose
  - orchestration
  - multi-container
  - devops
  - yaml
prerequisites:
  - Volumes and Persistent Storage
  - Building Images with Dockerfile
  - Running Your First Container
comments: false
---

# Docker Compose Fundamentals

## Overview

Real applications rarely run as a single container. A web API needs a database, a cache, and maybe a reverse proxy. Running each with long `docker run` commands becomes unmaintainable. **Docker Compose** defines multi-container applications in a declarative YAML file and manages their lifecycle with one command: **`docker compose up`**.

This tutorial is **Tutorial 9** in **Module 3: Storage & Compose** of the REBASH Academy Docker series. You will write `compose.yaml` files, connect services over user-defined networks, persist data with volumes, and manage environment configuration. For networking details, see [Docker Networking Fundamentals](docker-networking-fundamentals.md).

## Prerequisites

- Completed [Volumes and Persistent Storage](volumes-and-persistent-storage.md)
- Completed [Building Images with Dockerfile](building-images-with-dockerfile.md)
- Completed [Running Your First Container](running-your-first-container.md)
- Docker Compose V2 plugin installed (`docker compose version`)
- Basic YAML syntax familiarity

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain Compose's role vs raw `docker run` and Kubernetes
- [ ] Write `compose.yaml` with services, networks, volumes, and environment variables
- [ ] Build images inline and reference published images
- [ ] Start, stop, scale, and tear down stacks with Compose commands
- [ ] Use service names for DNS-based service discovery
- [ ] Override configuration for development with multiple Compose files

## Architecture Diagram

```d2
direction: down

Compose: Project {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        WEB: "web service\nnginx:alpine"
        API: "api service\ncustom build"
        DB: "db service\npostgres:16"
        VOL: "named volume\npgdata"
        NET: "user-defined network\napp-net"
    }
    USER: "Browser / curl"
    USER -> Compose.WEB: "port 8080"
    Compose.WEB -> Compose.API: "proxy /api"
    Compose.API -> Compose.DB: "postgres:5432"
    Compose.DB -> Compose.VOL
    Compose.WEB -> Compose.NET
    Compose.API -> Compose.NET
    Compose.DB -> Compose.NET
```

Compose creates a project-scoped network. Services resolve each other by **service name**.

## Theory

### What Compose Solves

| Problem with manual `docker run` | Compose solution |
|----------------------------------|------------------|
| Long, error-prone command lines | Declarative YAML |
| Manual network creation and attachment | Automatic project network |
| Remembering volume names and env vars | Defined once in file |
| Startup order guesswork | `depends_on` (with limitations) |
| Reproducibility across teammates | Version-controlled stack definition |

Compose targets **single-host** development and small deployments. For multi-node orchestration, use Kubernetes or Docker Swarm.

### File Naming and Versions

Modern Compose uses **`compose.yaml`** (also accepts `compose.yml`, `docker-compose.yaml`). The legacy `version: "3.8"` top-level key is **obsolete** with Compose Specification — omit it in new files.

Project name defaults to directory name; override with `-p` or `COMPOSE_PROJECT_NAME`.

### Services

Each service maps to one container (by default). Key fields:

| Field | Purpose |
|-------|---------|
| `image` | Use pre-built image |
| `build` | Build from Dockerfile (context path or build config with `args`) |
| `ports` | Publish ports (`host:container`) |
| `environment` / `env_file` | Inline or file-based env vars |
| `volumes` | Mount volumes or bind paths |
| `networks` | Attach to networks |
| `depends_on` | Start order (use with `condition: service_healthy` for readiness) |
| `restart` | Restart policy (`unless-stopped`, `on-failure`) |
| `healthcheck` | Container health probe |

`build` creates the image; optional `image` tags the result for reuse and registry push.

### Networking in Compose

Compose creates a **default network** per project. All services join it unless configured otherwise. DNS names match **service names** — the `api` service is reachable at hostname `api` from sibling containers.

Custom networks segment traffic:

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    internal: true   # no external routing
```

### Volumes in Compose

Top-level `volumes:` declares named volumes. Services reference them as `pgdata:/var/lib/postgresql/data`. Bind mounts (`./src:/app`) suit local development hot-reload.

### Environment Variables

| Method | Example |
|--------|---------|
| Inline | `environment: POSTGRES_PASSWORD: secret` |
| List form | `environment: - POSTGRES_PASSWORD=secret` |
| Env file | `env_file: - .env` |
| Shell interpolation | `image: myapp:${TAG:-latest}` |

**Never commit `.env` with secrets** — add to `.gitignore`. Use `.env.example` for documentation.

### depends_on and Startup Order

`depends_on` ensures **start order**, not **readiness**. Database may accept TCP before accepting queries. For production-like local dev, add **healthcheck** and `depends_on` with `condition: service_healthy` (Compose v2 syntax):

```yaml
services:
  api:
    depends_on:
      db:
        condition: service_healthy
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5
```

### Compose Commands Overview

| Command | Action |
|---------|--------|
| `docker compose up` | Create and start services |
| `docker compose up -d` | Detached mode |
| `docker compose down` | Stop and remove containers, networks |
| `docker compose down -v` | Also remove named volumes |
| `docker compose ps` | List project containers |
| `docker compose logs` | Aggregate logs |
| `docker compose exec` | Run command in running service |
| `docker compose build` | Build or rebuild images |
| `docker compose config` | Validate and render final config |

### Override Files

`compose.override.yaml` merges automatically with `compose.yaml` for local dev differences. Explicit merge:

```bash
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

Later files override earlier ones for conflicting keys.

## Hands-on Lab

Build a two-tier stack: Flask API + PostgreSQL.

### Step 1 – Create project structure

**Command:**

```bash
mkdir -p ~/lab/compose-lab/api && cd ~/lab/compose-lab

cat > api/app.py << 'PYEOF'
import os
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/visits")
def visits():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY)")
    cur.execute("INSERT INTO visits DEFAULT VALUES")
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM visits")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify(visits=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
PYEOF

cat > api/requirements.txt << 'EOF'
flask==3.0.3
psycopg2-binary==2.9.9
EOF

cat > api/Dockerfile << 'EOF'
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
EOF
```

**Explanation:** Minimal Flask API counting visits in PostgreSQL — demonstrates service discovery and persistence.

**Expected output:** API source and Dockerfile under `~/lab/compose-lab/api/`.

### Step 2 – Write compose.yaml

**Command:**

```bash
cat > compose.yaml << 'EOF'
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: devpass
      POSTGRES_DB: appdb
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 5s
      timeout: 3s
      retries: 5

  api:
    build: ./api
    image: rebash-compose-api:lab
    environment:
      DB_HOST: db
      DB_NAME: appdb
      DB_USER: appuser
      DB_PASSWORD: devpass
    ports:
      - "5000:5000"
    networks:
      - backend
    depends_on:
      db:
        condition: service_healthy

networks:
  backend:
    driver: bridge

volumes:
  pgdata:
EOF
```

**Explanation:** API connects to hostname `db` — Compose DNS. Health check gates API start until Postgres ready.

**Expected output:** Valid `compose.yaml` in project root.

### Step 3 – Validate configuration

**Command:**

```bash
docker compose config
```

**Explanation:** Renders merged configuration and catches YAML errors before starting containers.

**Expected output:** Full resolved YAML with environment variables expanded.

### Step 4 – Start the stack

**Command:**

```bash
docker compose up -d --build
docker compose ps
```

**Explanation:** `--build` builds API image. `-d` runs detached. `ps` shows service status and published ports.

**Expected output:**

```text
NAME                STATUS          PORTS
compose-lab-api-1   running         0.0.0.0:5000->5000/tcp
compose-lab-db-1    running (healthy)
```

### Step 5 – Test API and persistence

**Command:**

```bash
curl -s http://localhost:5000/health
curl -s http://localhost:5000/visits
curl -s http://localhost:5000/visits
curl -s http://localhost:5000/visits
```

**Explanation:** Each `/visits` call increments counter stored in PostgreSQL volume.

**Expected output:** Visit counts increment: 1, 2, 3.

### Step 6 – Verify service DNS internally

**Command:**

```bash
docker compose exec api python -c "import socket; print(socket.gethostbyname('db'))"
```

**Explanation:** Compose embeds DNS resolver — service name `db` resolves to database container IP on backend network.

**Expected output:** An IP address like `172.x.x.x`.

### Step 7 – Recreate stack and confirm data persists

**Command:**

```bash
docker compose down
docker compose up -d
curl -s http://localhost:5000/visits
```

**Explanation:** `down` removes containers but not named volume `pgdata`. Visit count should continue from previous value.

**Expected output:** Visit count is 4 (or higher), not reset to 1.

### Step 8 – View logs and exec into service

**Command:**

```bash
docker compose logs api --tail 20
docker compose exec db psql -U appuser -d appdb -c "SELECT COUNT(*) FROM visits;"
```

**Explanation:** Logs aggregate stdout from services. Exec runs interactive commands inside running containers.

**Expected output:** SQL count matches API visit counter.

### Step 9 – Clean up

**Command:**

```bash
docker compose down -v --rmi local
rm -rf ~/lab/compose-lab
```

**Explanation:** `-v` removes named volumes; `--rmi local` removes built images.

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `docker compose up` | Start stack | `docker compose up -d` |
| `docker compose down` | Stop and remove | `docker compose down -v` |
| `docker compose ps` | Service status | `docker compose ps -a` |
| `docker compose logs` | Stream logs | `docker compose logs -f api` |
| `docker compose exec` | Shell into service | `docker compose exec db sh` |
| `docker compose build` | Build images | `docker compose build --no-cache` |
| `docker compose config` | Validate YAML | `docker compose config` |
| `docker compose pull` | Pull service images | `docker compose pull` |

## Common Mistakes

!!! warning "Assuming depends_on waits for database readiness"
    Without healthcheck conditions, API crashes on startup while DB initializes. Add `pg_isready` or equivalent.

!!! warning "Publishing ports on every replica when scaling"
    Host port conflicts when scaling services with `ports` — use a reverse proxy or internal-only networking.

!!! warning "Committing .env with production secrets"
    Use `.env.example` template; inject secrets via CI or secret managers in production.

!!! warning "Using latest tag in compose for production"
    Pin image digests or semver tags for reproducible deploys.

!!! warning "docker compose down -v in production"
    Destroys database volumes irreversibly without backup.

## Best Practices

!!! tip "One service per concern"
    Separate web, API, worker, and database — mirrors Kubernetes deployment model.

!!! tip "Name volumes and networks explicitly"
    Avoid relying on auto-generated names in documentation and backup scripts.

!!! tip "Use health checks for dependencies"
    `condition: service_healthy` prevents cascading startup failures.

!!! tip "Keep compose files in version control"
    Treat infrastructure definition as code — review changes like application code.

!!! tip "Use docker compose config in CI"
    Validate YAML on every pull request before deploy pipelines run.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `port is already allocated` | Host port in use | Change host port or stop conflicting service |
| API cannot connect to db | Wrong hostname or network | Use service name; verify shared network |
| Build context not found | Wrong `build:` path | Path relative to compose file location |
| Empty env vars | Missing `.env` or wrong key | Check `docker compose config` output |
| Volume permission errors | Postgres UID mismatch | Named volume usually avoids; check bind mounts |
| Stale containers after edit | Old containers not recreated | `docker compose up -d --force-recreate` |
| YAML parse error | Indentation or tabs | Use spaces only; run `docker compose config` |

## Summary

- **Docker Compose** defines multi-container apps declaratively in **`compose.yaml`**
- Services discover each other by **name** on project networks
- **Named volumes** persist data across `docker compose down`
- **`depends_on` + healthcheck** handles startup ordering more reliably
- **Override files** separate dev and production configuration
- Core workflow: **`config` → `up` → test → `logs` → `down`**

## Interview Questions

1. What problem does Docker Compose solve compared to `docker run`?
2. How do containers in the same Compose project find each other?
3. What is the difference between `ports` and `expose`?
4. Does `depends_on` wait for a service to be ready?
5. How do you persist database data in Compose?
6. What happens when you run `docker compose down -v`?
7. How would you override Compose settings for local development?
8. Can you scale services with Compose? What are the limitations?
9. What is the purpose of `docker compose config`?
10. When would you move from Compose to Kubernetes?

??? tip "Sample Answers (Questions 2, 4, and 6)"

    **Q2 — Service discovery:** Compose attaches services to shared networks and provides embedded DNS. Each service is reachable by its **service name** as hostname — e.g., `db` resolves to the database container IP from the `api` container.

    **Q4 — depends_on:** By default, `depends_on` only controls **start order**, not readiness. The dependent container may start before Postgres accepts connections. Use `depends_on` with `condition: service_healthy` and a proper `healthcheck` on the database service.

    **Q6 — down -v:** Stops and removes containers and project networks, and **deletes named volumes** declared in the compose file. All data in those volumes is permanently lost unless backed up externally.

## Related Tutorials

- [Docker – Category Overview](index.md)
- [Volumes and Persistent Storage](volumes-and-persistent-storage.md) *(previous)*
- [Docker Networking Fundamentals](docker-networking-fundamentals.md) *(next in Module 4)*
- [Environment Variables and Secrets](environment-variables-and-secrets.md)
- [From Docker to Kubernetes](from-docker-to-kubernetes.md)

## References

- [Compose Specification](https://docs.docker.com/compose/compose-file/)
- [Docker Compose CLI reference](https://docs.docker.com/compose/reference/)
- [Networking in Compose](https://docs.docker.com/compose/networking/)
- [Compose file reference – depends_on](https://docs.docker.com/compose/compose-file/depends_on/)
- [REBASH Academy – Volumes Tutorial](volumes-and-persistent-storage.md)
