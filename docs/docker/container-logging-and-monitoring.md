---
title: Container Logging and Monitoring
description: Capture container logs with logging drivers, inspect resource usage with docker stats, configure log rotation, and preview cAdvisor for host-level container metrics.
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
category: docker
tags:
  - docker
  - logging
  - monitoring
  - cadvisor
  - metrics
  - observability
prerequisites:
  - Completion of Module 1–3 Docker tutorials
  - Basic familiarity with Linux log concepts from the Linux track
  - Docker Engine running on a Linux host for full logging driver support
comments: false
---

# Container Logging and Monitoring

## Overview

Containers are ephemeral, but the **signals they emit** — stdout/stderr logs, exit codes, CPU and memory usage — must be durable and observable for debugging, SLO tracking, and incident response. Without a logging and monitoring strategy, `docker logs` on a single host does not scale to fleets of nodes, and deleted containers take their last hour of stderr with them.

This tutorial covers Docker's **logging drivers**, practical **log rotation**, reading logs with CLI tools, real-time resource metrics with **`docker stats`**, and a preview of **cAdvisor** for per-container CPU, memory, and network metrics on a host. These foundations transfer directly to Kubernetes (Fluent Bit, Prometheus, Grafana) and cloud-managed container services.

This is **Tutorial 13** in **Module 5: Operations** of the REBASH Academy Docker series. Complete [Environment Variables and Secrets](environment-variables-and-secrets.md) before starting Module 5.

## Prerequisites

- Docker Engine on Linux (logging driver behavior differs slightly on Docker Desktop)
- Completion of [Running Your First Container](running-your-first-container.md)
- Familiarity with [Log Management with journalctl](../linux/log-management-journalctl.md) concepts
- Optional: second terminal window to generate load while observing stats

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain how container logs flow from application stdout to storage backends
- [ ] Configure the json-file logging driver with rotation limits
- [ ] Retrieve, follow, and filter logs with `docker logs`
- [ ] Monitor live CPU, memory, and I/O with `docker stats`
- [ ] Run cAdvisor and interpret basic container resource dashboards
- [ ] Describe production logging patterns (centralized aggregation, structured JSON logs)

## Architecture Diagram

Application processes write to stdout/stderr. The container runtime captures streams and forwards them through the configured logging driver.

```mermaid
flowchart LR
    APP["Application<br/>stdout / stderr"]
    ENGINE["Docker Engine<br/>logging driver"]
    LOCAL[json-file on disk]
    SYSLOG[syslog]
    FLUENT["Fluentd / Fluent Bit"]
    CLOUD["CloudWatch / Stackdriver"]
    ELK["Elasticsearch / Loki"]

    APP --> ENGINE
    ENGINE --> LOCAL
    ENGINE --> SYSLOG
    ENGINE --> FLUENT
    FLUENT --> ELK
    FLUENT --> CLOUD```

## Theory

### Container Logs Are Stream Captures

Unlike traditional apps writing to `/var/log/app.log` inside the container, **Twelve-Factor** and cloud-native practice recommend logging to **stdout/stderr**. Docker's containerd/shim captures these streams and hands them to a **logging driver**.

Benefits:

- No volume management for log files inside containers
- Same pattern on Docker, Kubernetes, Cloud Run, and Lambda
- Log shippers attach at the host or cluster level

Trade-off: extremely high-volume debug logging can fill disk if rotation is misconfigured.

### Logging Drivers

Docker supports multiple drivers via `/etc/docker/daemon.json` (default) or per-container `--log-driver`.

| Driver | Default? | Typical use |
|--------|----------|-------------|
| **json-file** | Yes (Linux) | Local files under `/var/lib/docker/containers/` |
| **local** | Alternative local | Optimized binary format, faster rotation |
| **syslog** | No | Forward to syslog daemon |
| **journald** | No | Integrate with systemd journal on host |
| **fluentd** / **gelf** | No | Forward to centralized collectors |
| **awslogs** / **gcplogs** | No | Native cloud log groups (requires plugins/setup) |
| **none** | No | Discard logs (batch jobs with no observability need) |

Check active driver:

```bash
docker info | grep 'Logging Driver'
```

Per-container override example:

```bash
docker run --log-driver=syslog --log-opt syslog-address=udp://127.0.0.1:514 myapp
```

### json-file Rotation

Unbounded json-file logs are a top cause of **disk-full** incidents on Docker hosts. Configure defaults in `/etc/docker/daemon.json`:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

Each container log rotates at 10 MB, keeping three files (~30 MB cap per container). Restart Docker after daemon changes. Existing containers keep their creation-time driver options until recreated.

### docker logs Command

`docker logs` reads from the configured driver (for json-file/local, from disk):

| Flag | Purpose |
|------|---------|
| `-f` | Follow (like `tail -f`) |
| `--tail N` | Show last N lines |
| `--since` | Logs since timestamp or duration |
| `--until` | Logs before timestamp |
| `-t` | Show timestamps |

Logs include both stdout and stderr unless separated by driver features. Exit code and OOM events appear in `docker inspect`, not always in application logs.

### Structured Logging

Plain text logs are hard to query at scale. Production apps emit **JSON lines**:

```json
{"level":"info","msg":"request completed","method":"GET","path":"/health","duration_ms":12}
```

Central systems (Elasticsearch, Loki, CloudWatch Logs Insights) index fields. Docker does not parse JSON — the collector downstream does. Include `request_id`, `service`, and `version` fields for correlation.

### docker stats — Live Resource Metrics

`docker stats` streams container **cgroup** metrics:

- CPU % (relative to host cores)
- Memory usage / limit
- Network I/O
- Block I/O

Single snapshot:

```bash
docker stats --no-stream
```

Limit to specific containers:

```bash
docker stats web db cache
```

**Limitations:** Host-level view only; no historical retention; resets when container restarts. Production uses Prometheus, Datadog, or cloud monitoring for time-series storage.

### cAdvisor Preview

**cAdvisor** (Container Advisor) is a Google open-source tool that exposes per-container resource usage and historical graphs via a web UI. It reads cgroup and filesystem metrics from the host.

Typical deployment: cAdvisor runs as a container with host mounts:

- `/:/rootfs:ro`
- `/var/run:/var/run:ro`
- `/sys:/sys:ro`
- `/var/lib/docker/:/var/lib/docker:ro`

Default UI port: **8080**. In production, Prometheus scrapes cAdvisor's `/metrics` endpoint; Grafana dashboards visualize pod/container usage. Kubernetes users often rely on kubelet/cAdvisor integration built into nodes.

cAdvisor complements `docker stats` with graphs and exportable metrics — it does not replace centralized logging.

### Production Observability Stack (Conceptual)

| Layer | Docker-era tools | Kubernetes-era evolution |
|-------|------------------|--------------------------|
| **Logs** | json-file + Fluent Bit → Loki/ELK | DaemonSet log agents |
| **Metrics** | cAdvisor + Prometheus + Grafana | kube-prometheus-stack |
| **Traces** | OpenTelemetry SDK → Jaeger/Tempo | Same, sidecar or eBPF |
| **Alerts** | Alertmanager, PagerDuty | SLO-based alerting on RED metrics |

**RED method** for services: Rate (requests/sec), Errors, Duration — derived from logs and metrics together.

## Hands-on Lab

### Step 1 – Create a verbose logging container

**Command:**

```bash
docker run -d --name log-lab \
  alpine sh -c 'i=0; while true; do i=$((i+1)); echo "tick number $i"; sleep 2; done'
sleep 3
docker logs log-lab --tail 5
```

**Explanation:** The container writes numbered lines to stdout every two seconds — simulates application logging.

**Expected output:**

```text
tick number 1
tick number 2
...
```

### Step 2 – Follow logs in real time

Open a second terminal for this step, or run with a timeout.

**Command:**

```bash
timeout 8 docker logs -f --timestamps log-lab
```

**Explanation:** `-f` follows new output; `-t` prefixes ISO8601 timestamps from Docker (not necessarily from the app).

### Step 3 – Filter logs by time

**Command:**

```bash
docker logs log-lab --since 5s --tail 10
```

**Explanation:** `--since` accepts durations (`5s`, `2m`) or RFC3339 timestamps — useful during incident triage.

### Step 4 – Inspect logging driver configuration

**Command:**

```bash
docker inspect log-lab | grep -A6 '"LogConfig"'
docker info | grep 'Logging Driver'
```

**Explanation:** Per-container `LogConfig` shows driver and options. Compare with daemon-wide defaults from `docker info`.

### Step 5 – Run a container with log rotation options

**Command:**

```bash
docker run -d --name log-lab-rot \
  --log-driver=json-file \
  --log-opt max-size=1m \
  --log-opt max-file=2 \
  alpine sh -c 'while true; do dd if=/dev/zero bs=1024 count=50 2>/dev/null | base64; sleep 1; done'
sleep 15
docker inspect log-lab-rot | grep -A8 '"LogConfig"'
docker rm -f log-lab-rot
```

**Explanation:** High-volume output triggers rotation at 1 MB with two file retention. Prevents one chatty container from filling the disk.

### Step 6 – Monitor with docker stats

**Command:**

```bash
docker run -d --name stats-lab --memory=128m nginx:1.27-alpine
docker stats stats-lab --no-stream
```

**Explanation:** Memory limit appears in stats output. CPU percentage is relative to one full host core unless limits apply.

**Expected output (columns vary by version):**

```text
CONTAINER ID   NAME       CPU %   MEM USAGE / LIMIT   MEM %   ...
```

Generate load optional:

```bash
docker exec stats-lab sh -c 'while true; do :; done' &
sleep 3
docker stats stats-lab --no-stream
docker rm -f stats-lab
```

### Step 7 – Run cAdvisor (preview)

**Command:**

```bash
docker run -d \
  --name=cadvisor \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  --detach=true \
  gcr.io/cadvisor/cadvisor:v0.49.1
sleep 5
curl -s -o /dev/null -w 'cAdvisor HTTP %{http_code}\n' http://127.0.0.1:8080/containers/
```

**Explanation:** Open `http://127.0.0.1:8080` in a browser to explore per-container graphs. Pin a specific cAdvisor version in production; `latest` tags drift.

**Expected output:**

```text
cAdvisor HTTP 200
```

### Step 8 – cAdvisor metrics endpoint

**Command:**

```bash
curl -s http://127.0.0.1:8080/metrics | head -20
```

**Explanation:** Prometheus scrapes this endpoint. Metric names include `container_cpu_usage_seconds_total`, `container_memory_usage_bytes`, and labels for container name/id.

### Step 9 – Clean up

**Command:**

```bash
docker rm -f log-lab cadvisor 2>/dev/null || true
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `docker logs` | Fetch container logs | `docker logs -f --tail 100 web` |
| `docker events` | Stream Docker daemon events | `docker events --filter container=web` |
| `docker stats` | Live resource usage | `docker stats --no-stream` |
| `docker inspect` | Log config and state | `docker inspect web` |
| `docker info` | Daemon logging defaults | `docker info` |

### daemon.json log rotation template

Apply on Linux hosts running many containers:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "50m",
    "max-file": "5",
    "compress": "true"
  }
}
```

Restart Docker: `sudo systemctl restart docker` — plan maintenance; recreates may be needed for opts on existing containers.

### Minimal Fluent Bit forward (conceptual)

Production hosts often ship json-file logs via Fluent Bit. Illustrative `/fluent-bit/etc/fluent-bit.conf` fragment:

```ini
[INPUT]
    Name              tail
    Path              /var/lib/docker/containers/*/*-json.log
    Parser            docker
    Tag               docker.*

[OUTPUT]
    Name              loki
    Match             docker.*
    Host              loki.example.com
    Port              3100
```

Exact paths depend on your log driver and distribution.

## Common Mistakes

!!! warning "Logging inside the container filesystem only"
    Logs written only to `/var/log/app.log` inside the container are lost on `docker rm` unless mounted. Prefer stdout or mount a volume to the host.

!!! warning "No log rotation on json-file driver"
    Default infinite growth fills `/var/lib/docker`. Always set `max-size` and `max-file` in daemon.json or per container.

!!! warning "Treating docker stats as historical monitoring"
    Stats are point-in-time/live only. Incidents requiring "memory usage last Tuesday" need Prometheus or cloud metrics.

!!! warning "Exposing cAdvisor without authentication"
    cAdvisor reveals container metadata and resource data. Bind to localhost or protect with network policy and auth in production.

## Best Practices

!!! tip "Log to stdout in JSON for production services"
    Structured logs enable high-cardinality search without regex parsing fragile plain text.

!!! tip "Set memory and CPU limits before interpreting stats"
    Unbounded containers can starve the host; stats show usage relative to limits when configured.

!!! tip "Correlate logs with container IDs and image digests"
    Include `container_id` and `image_tag` in deploy logs — maps observability back to registry artifacts from Tutorial 11.

!!! tip "Plan centralized logging before fleet scale"
    json-file on each host works for tens of containers; hundreds require Fluent Bit, Datadog agent, or cloud log drivers.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `docker logs` empty | App logs to file not stdout | Fix app or tail mounted volume |
| Disk full on `/var/lib/docker` | Log rotation missing | Add `max-size`/`max-file`; prune unused containers |
| `docker logs -f` hangs silently | App buffers stdout | Run Python with `PYTHONUNBUFFERED=1`; flush logs in app |
| stats show 0 CPU always | Idle container | Generate load; verify container running |
| cAdvisor UI empty | Wrong mounts or permissions | Verify volume paths; run on Linux host |
| Logs missing after restart | Driver `none` or remote-only | Check `LogConfig`; verify remote collector health |
| Timestamps inconsistent | App vs Docker timestamps | Use `-t` on docker logs; emit ISO8601 in app JSON |

## Summary

- Container logs capture **stdout/stderr** through **logging drivers** — default `json-file` stores JSON lines on the host
- Configure **log rotation** (`max-size`, `max-file`) to prevent disk exhaustion
- **`docker logs`** retrieves and filters historical output; **`docker stats`** shows live CPU/memory/network
- **cAdvisor** exposes per-container metrics and a web UI; Prometheus scrapes `/metrics` in production
- Mature observability combines centralized **logs**, **metrics**, and **traces** — Docker CLI tools are the starting point, not the destination

## Interview Questions

1. Where do container logs go when an app prints to stdout?
2. How do you prevent Docker json-file logs from filling the disk?
3. What is the difference between docker logs and application log files inside the container?
4. What metrics does docker stats provide, and what are its limitations?
5. What is cAdvisor, and how does it relate to Prometheus?
6. Why is structured JSON logging recommended for microservices?
7. How would you forward Docker logs to Elasticsearch or CloudWatch?
8. What logging driver would you use to discard logs entirely, and when?
9. How do cgroup memory limits appear in docker stats output?
10. What is the RED method, and which Docker tools help measure its components?

??? tip "Sample Answers (Questions 1, 4, and 5)"

    **Q1 — stdout destination:** The container runtime attaches to the process stdout/stderr file descriptors. Docker's configured logging driver (default json-file) receives each line and persists or forwards it — typically to `/var/lib/docker/containers/<id>/<id>-json.log` on the host for json-file.

    **Q4 — docker stats:** Provides live CPU%, memory usage/limit, network I/O, and block I/O per container from cgroup statistics. Limitations: no history, host-scoped only, resets on container restart, and CPU% interpretation depends on host core count and limits.

    **Q5 — cAdvisor:** Container Advisor collects resource usage and performance characteristics per container from cgroups and exposes them via web UI and Prometheus metrics. Prometheus scrapes `/metrics` for time-series storage; Grafana visualizes trends — unlike docker stats, enabling alerting and capacity planning.

## Related Tutorials

- [Docker – Category Overview](index.md)
- [Environment Variables and Secrets](environment-variables-and-secrets.md) *(end of Module 4)*
- [Docker Security Hardening](docker-security-hardening.md) *(next in Module 5)*
- [Log Management with journalctl](../linux/log-management-journalctl.md)
- [Monitoring – Category Overview](../monitoring/index.md)

## References

- [Configure logging drivers](https://docs.docker.com/engine/logging/configure/)
- [json-file logging driver](https://docs.docker.com/engine/logging/drivers/json-file/)
- [docker logs reference](https://docs.docker.com/reference/cli/docker/container/logs/)
- [docker stats reference](https://docs.docker.com/reference/cli/docker/container/stats/)
- [cAdvisor GitHub](https://github.com/google/cadvisor)
- [Prometheus cAdvisor exporter](https://prometheus.io/docs/guides/cadvisor/)
- [REBASH Academy – Monitoring Overview](../monitoring/index.md)
