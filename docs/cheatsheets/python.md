---
title: "Python for DevOps Cheat Sheet"
description: "Quick-reference Python patterns for DevOps: syntax, data structures, files, exceptions, logging, requests, argparse, Click, Docker SDK, Kubernetes client, boto3, and pytest."
difficulty: beginner
estimated_time: "15 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: cheatsheets
tags:
  - cheatsheets
  - python
  - devops
comments: false
---

# Python for DevOps Cheat Sheet

Scannable Python patterns for the [Python for DevOps track](../python/index.md). Prefer the full tutorials when you need *why*, not only *how*.

## Python syntax

```python
x: int = 1
name = "payments"
f"{name}-{x}"
a, b = 1, 2
# truthiness: empty str/list/dict/None are False
```

| Construct | Example |
|-----------|---------|
| `if` / `elif` / `else` | `if code == 0: ...` |
| `match` | `match status: case 200: ...` |
| `for` | `for line in path.open(): ...` |
| `while` | `while retries: ...` |
| Comprehension | `[x for x in items if x]` |
| Generator | `(parse(l) for l in lines)` |
| f-string | `f"region={region}"` |
| walrus | `if (m := pat.search(line)):` |

## Data structures

| Type | Create | Notes |
|------|--------|-------|
| list | `[1, 2]` | ordered, mutable |
| tuple | `(1, 2)` | immutable |
| dict | `{"a": 1}` | `.get(k, default)` |
| set | `{1, 2}` | unique, unordered |
| `collections.Counter` | `Counter(levels)` | tallies |
| `dataclasses.dataclass` | `@dataclass` | structured records |

```python
hosts = {"api": "10.0.0.1", "db": "10.0.0.2"}
ids = [h for h in hosts if h.startswith("a")]
```

## File handling

```python
from pathlib import Path
import json, csv
import yaml  # PyYAML — safe_load only

p = Path("logs") / "app.log"
text = p.read_text(encoding="utf-8")
for line in p.open(encoding="utf-8"):
    ...
data = json.loads(text)
Path("out.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
cfg = yaml.safe_load(Path("deploy.yaml").read_text(encoding="utf-8"))
```

| Task | API |
|------|-----|
| Join paths | `Path("a") / "b"` |
| Glob | `Path(".").glob("**/*.yaml")` |
| CSV | `csv.DictReader` / `DictWriter` |
| Temp | `tempfile.TemporaryDirectory` |
| Copy/move | `shutil.copy2`, `shutil.move` |

## Exceptions

```python
try:
    cfg = load(path)
except FileNotFoundError as exc:
    raise SystemExit(f"missing: {exc}") from exc
except (json.JSONDecodeError, ValueError) as exc:
    print(exc, file=sys.stderr)
    raise SystemExit(2) from exc
finally:
    cleanup()
```

| Pattern | Use |
|---------|-----|
| `raise X from e` | preserve cause |
| Custom exception | `class ConfigError(Exception): ...` |
| Exit taxonomy | `0` ok · `2` usage/validation · `1` runtime failure |

## Logging

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("rebash.ops")
log.info("inventory_start region=%s", region)  # never log tokens
```

| Level | When |
|-------|------|
| DEBUG | local diagnosis |
| INFO | normal ops events |
| WARNING | degraded but continuing |
| ERROR | failed action |
| CRITICAL | stop the world |

## requests / httpx

```python
import httpx
with httpx.Client(timeout=10.0) as client:
    r = client.get(url, headers={"Authorization": f"Bearer {token}"})
    r.raise_for_status()
    payload = r.json()
```

| Rule | Detail |
|------|--------|
| Always set timeouts | connect + read |
| Retries | idempotent GETs with backoff |
| Auth | env / secret store — not source |
| Pagination | follow `Link` / `next` tokens explicitly |

## argparse

```python
import argparse
p = argparse.ArgumentParser(description="Inventory hosts")
p.add_argument("--region", required=True)
p.add_argument("--json", action="store_true")
p.add_argument("--dry-run", action="store_true", default=True)
args = p.parse_args()
```

## Click

```python
import click

@click.command()
@click.option("--region", required=True)
@click.option("--apply", is_flag=True, default=False)
def main(region: str, apply: bool) -> None:
    click.echo(region)
```

## Typer (related)

```python
import typer
app = typer.Typer()

@app.command()
def collect(fixture: Path | None = None) -> None:
    ...
```

## Docker SDK

```python
import docker
client = docker.from_env()
# Prefer report-first:
for img in client.images.list(filters={"dangling": True}):
    print(img.short_id, img.attrs.get("Size"))
# Delete only behind --apply
```

| Safety | Practice |
|--------|----------|
| Default dry-run | require `--apply` |
| Daemon down | `--fixture` path for labs/CI |
| Labels | filter by `label=...` before prune |

## Kubernetes client

```python
from kubernetes import client, config
config.load_kube_config()  # or load_incluster_config()
v1 = client.CoreV1Api()
pods = v1.list_namespaced_pod("payments")
for pod in pods.items:
    print(pod.metadata.name, pod.status.phase)
```

| Safety | Practice |
|--------|----------|
| Read-only first | list/get before patch/delete |
| Namespace scope | never cluster-admin for scripts |
| Offline | fixture JSON for CI |

## boto3

```python
import boto3
ec2 = boto3.client("ec2", region_name="eu-west-2")
resp = ec2.describe_instances()
# Prefer instance roles / OIDC — never hard-code keys
```

| Pattern | Note |
|---------|------|
| Sessions | `boto3.Session(profile_name=...)` |
| Paginators | `ec2.get_paginator("describe_instances")` |
| Errors | catch `ClientError`; map to exit codes |
| Labs/CI | fixture JSON when credentials absent |

## pytest

```python
import pytest

@pytest.fixture
def sample_log(tmp_path):
    p = tmp_path / "a.log"
    p.write_text("2026-07-28T10:00:00Z ERROR msg=\"x\"\n", encoding="utf-8")
    return p

def test_counts(sample_log):
    assert analyse(sample_log)["levels"]["ERROR"] == 1
```

| Tip | Detail |
|-----|--------|
| Fixtures | tmp_path, monkeypatch |
| Mock HTTP | `respx` / `unittest.mock` |
| No live cloud | gate integration with env marker |
| CLI tests | `CliRunner` (Click/Typer) |

## Tooling quick reference

| Area | Commands / notes |
|------|------------------|
| venv | `python3 -m venv .venv` · `source .venv/bin/activate` |
| pip | `pip install -r requirements.txt` · pin versions |
| uv | `uv venv` · `uv sync` · `uv run pytest` |
| subprocess | `subprocess.run([...], check=True, text=True)` · **list args** |
| env/secrets | `os.environ["KEY"]` · never commit `.env` |
| pyproject | `[project.scripts]` · `pip install -e .` |

## Common mistakes

- `subprocess.run("cmd $var", shell=True)` — injection risk; use list args
- `yaml.load` without a SafeLoader — prefer `safe_load`
- Missing HTTP timeouts — hung jobs and stuck pipelines
- Logging tokens or printing secrets in CI
- Shipping destructive Docker/K8s/cloud actions without a dry-run default
- Hard-coded cloud keys instead of roles / fixtures for tests

## Related

- Track: [Python for DevOps](../python/index.md)
- Lab: [Python Log Analyser](../labs/python-log-analyser.md)
- Interview: [Python interview prep](../interview/python.md)
- Quiz: [Python for DevOps Engineers Fundamentals](../quizzes/python-for-devops-engineers-fundamentals.md)
- Learning path: [Python for DevOps Engineers](../learning-paths/devops-engineer/)
