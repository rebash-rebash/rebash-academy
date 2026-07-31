---
title: "Docker SDK Automation"
description: "Automate Docker with the Python SDK — images, containers, networks, volumes, and registry cleanup patterns with dry-run defaults."
difficulty: intermediate
estimated_time: "50–65 min"
technology: python
category: python
module: "Module 17 · Docker Automation"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - cloud-engineer
skills:
  - python
  - docker-sdk
  - containers
prerequisites:
  - python/git-automation-github-and-gitlab
next:
  - python/kubernetes-python-client-automation
related:
  - docker/index
  - labs/python-docker-cleanup-tool
labs:
  - labs/python-docker-cleanup-tool
projects: []
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - docker
  - containers
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Docker SDK Automation

## Overview

Drive the Docker Engine API from Python to list images/containers, sketch cleanup safely with `--apply`, and understand networks, volumes, and registry automation boundaries.

The **Docker SDK for Python** talks to the same API as the Docker CLI. Use it for inventory and controlled cleanup — not for surprise `prune` in production without dry-run.

Complete [Git Automation](git-automation-github-and-gitlab.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 17 · Docker Automation** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Linux Automation](linux-automation-subprocess-and-psutil.md) habits (timeouts, exit codes)
- Docker Engine available **or** use the offline fixture path below

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Connect with `docker.from_env()`  
- [ ] List containers and images  
- [ ] Explain networks and volumes at an ops level  
- [ ] Design prune/cleanup with dry-run  
- [ ] Note registry auth as a separate concern

## Architecture

This topic’s control points and relationships are shown below.

![Docker SDK workflow](../assets/excalidraw/python-docker-sdk-workflow.svg)

## Theory

### What it is

The Docker SDK for Python (`docker` package) talks to the Docker Engine API the same way the `docker` CLI does — usually over the Unix socket `unix:///var/run/docker.sock`, or via `DOCKER_HOST` for remote daemons. You get objects for containers, images, networks, and volumes: list, inspect, build, run, stop, and prune, without shelling out and scraping text.

### Why it matters

DevOps automation invents containers for tests, cleans stale images on builders, and audits what is running on a host. Subprocess wrappers break when CLI output changes; the SDK returns structured attributes (`status`, tags, labels). In Continuous Integration / Continuous Delivery (CI/CD), Python jobs can assert “only expected containers exist” or pull pinned digests before a deploy smoke test — with the same safety flags you use for kubectl-style tools.

### How it works

`docker.from_env()` builds a client from environment and default socket paths. `client.ping()` confirms the daemon is reachable. Listing containers with `all=True` includes stopped ones; images expose tags and IDs. Networks and volumes are separate namespaces — list first, delete only unused resources. Registry operations (login, pull, push) need credentials from the environment or credential helpers; never embed tokens in code. Production promotion should pin by digest (`image@sha256:…`), not only by floating tags like `latest`.

```python
import docker
client = docker.from_env()
client.ping()
for c in client.containers.list(all=True):
    print(c.short_id, c.status, c.image.tags)
```

### Key concepts and comparisons

| Resource | SDK entry | Typical automation |
|----------|-----------|--------------------|
| Containers | `client.containers` | Inventory, stop/remove with `--apply` |
| Images | `client.images` | List, pull, prune dangling |
| Networks / volumes | `client.networks` / `volumes` | Cleanup unused lab resources |
| Swarm / Compose | Separate APIs / tools | Prefer Compose CLI for stacks |

| Action | Tutorial default |
|--------|------------------|
| List / inspect / ping | Allowed |
| Stop / remove / prune | Require `--apply` |
| Force remove | Extra confirmation in real tools |

### Common pitfalls

- Assuming the script’s user can access the Docker socket (group/`sudo` issues).  
- Pruning aggressively on shared builders and deleting in-use layers.  
- Logging registry passwords or auth configs.  
- Treating tag `latest` as immutable.  
- Mutating production hosts without dry-run and an allow-list of names.

## Hands-on Lab

**Focus:** practise the core workflow for Docker SDK Automation

```bash
mkdir -p ~/rebash-python/module-17
cd ~/rebash-python/module-17

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install 'docker==7.1.0'
```

### Step 1 – Fixture inventory (offline)

```bash
cd ~/rebash-python/module-17
source .venv/bin/activate

mkdir -p fixtures
cat > fixtures/containers.json << 'EOF'
[
  {"id": "abc123", "status": "exited", "image": "nginx:1.27"},
  {"id": "def456", "status": "running", "image": "redis:7"}
]
EOF

cat > docker_inventory.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def from_fixture(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def from_docker() -> list[dict]:
    import docker

    client = docker.from_env()
    client.ping()
    rows = []
    for c in client.containers.list(all=True):
        tags = c.image.tags or [""]
        rows.append({"id": c.short_id, "status": c.status, "image": tags[0]})
    return rows


def main() -> int:
    p = argparse.ArgumentParser(description="Docker container inventory")
    p.add_argument("--fixture", type=Path)
    p.add_argument("--apply-prune-exited", action="store_true", help="dangerous lab flag")
    args = p.parse_args()
    try:
        rows = from_fixture(args.fixture) if args.fixture else from_docker()
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        print("hint: use --fixture fixtures/containers.json", file=sys.stderr)
        return 1
    print(json.dumps(rows, indent=2))
    exited = [r for r in rows if r["status"] == "exited"]
    print(f"exited_count={len(exited)}", file=sys.stderr)
    if args.apply_prune_exited:
        print("error: prune not implemented in tutorial — use dedicated cleanup lab", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python docker_inventory.py --fixture fixtures/containers.json
```

### Step 2 – Live ping (optional)

```bash
python - <<'PY'
try:
    import docker
    print("ping", docker.from_env().ping())
except Exception as exc:
    print("docker unavailable:", exc)
PY
```

### Step 3 – Cleanup policy notes

Write `cleanup-policy.md`: age threshold, exclude labels (`keep=true`), dry-run JSON plan, then `--apply`.

## Validation

- [ ] Lab commands run under `~/rebash-python/module-17/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Docker SDK Automation** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for python as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Assuming the script’s user can access the Docker socket (group/`sudo` issues).  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Pruning aggressively on shared builders and deleting in-use layers.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Docker SDK Automation changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Permission denied on socket | User not in `docker` group | Rootless or group membership |
| API version errors | Old engine/SDK mismatch | Align versions |
| Accidental wipe | Prune without filter | Labels + dry-run |

## Summary

- SDK mirrors CLI capabilities over the Engine API  
- Inventory first; prune only with explicit apply  
- Lab: [Docker Cleanup Tool](../labs/python-docker-cleanup-tool.md)

## Interview Questions

1. How does **Docker SDK Automation** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Kubernetes Python Client Automation](kubernetes-python-client-automation.md)  
- [Docker Cleanup Tool lab](../labs/python-docker-cleanup-tool.md)

## References

- [docker-py](https://docker-py.readthedocs.io/)
