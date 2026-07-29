---
title: "OOP — Classes and Dataclasses"
description: "Classes, objects, methods, constructors, inheritance, encapsulation, polymorphism, and dataclasses for ops models."
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: python
tags:
  - python
  - oop
  - dataclasses
prerequisites:
  - Error Handling and Exceptions
  - Python 3.12+ on Linux (WSL2/VM/cloud)
comments: false
---

# OOP — Classes and Dataclasses

## Overview

Inventories and clients benefit from small typed models — not deep inheritance trees.

This is **Tutorial 9** in **Module 9: Object-Oriented Programming** of the REBASH Academy **Python for DevOps Engineers** series — written for DevOps engineers, SREs, platform engineers, and cloud engineers who automate infrastructure with production-quality Python.

## Prerequisites

- Error Handling and Exceptions
- Python 3.12+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “OOP — Classes and Dataclasses” in real ops automation
- [ ] Use a project venv and avoid relying on system site-packages
- [ ] Produce clear stderr diagnostics and meaningful exit codes
- [ ] Prefer safe patterns (pathlib, subprocess list args, dry-run)
- [ ] Relate this topic to day-to-day DevOps and platform work

## Architecture

Ops Python sits between operators/CI and platforms (files, APIs, CLIs, and cloud control planes). This topic’s control points are shown below.

![Architecture diagram for OOP — Classes and Dataclasses](../assets/images/python-oop-dataclasses.svg)

## Theory

### Classes

A **class** defines a blueprint. Prefer composition over deep hierarchies for automation clients.

### Objects

An **object** is an instance. Keep instances immutable when they represent snapshots (inventory rows).

### Methods

Instance methods take `self`. Use `@staticmethod` / `@classmethod` sparingly. Keep methods short and side-effect explicit.

### Constructors

`__init__` validates and stores state. Fail in `__init__` if required config is missing rather than failing later in obscure methods.

### Inheritance

Share behaviour carefully (`BaseClient` → `GitHubClient`). Prefer protocols/duck typing when a single method is shared.

### Encapsulation

Prefix internal helpers with `_`. Do not expose raw tokens as public attributes — store and redact.

### Polymorphism

Call the same method name across client types (`inventory()`, `health()`). Useful for multi-cloud inventory CLIs.

### Dataclasses

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Host:
    name: str
    env: str
    healthy: bool
```

Prefer dataclasses for structured records you serialise to JSON.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-python/lab09 && cd ~/rebash-python/lab09
```

**Focus:** Host dataclass; small Client class with dry_run; JSON serialise hosts

### Step 1 – Skeleton

```bash
cat > lab.py << 'EOF'
#!/usr/bin/env python3
print("lab09 oop-classes-and-dataclasses")
EOF
chmod +x lab.py
python3 lab.py
```

### Step 2 – Dataclass inventory

```bash
cat > oop.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import asdict, dataclass
import json

@dataclass(frozen=True)
class Host:
    name: str
    env: str
    healthy: bool

class Inventory:
    def __init__(self, dry_run: bool = True) -> None:
        self.dry_run = dry_run
        self._hosts: list[Host] = []

    def add(self, host: Host) -> None:
        self._hosts.append(host)

    def report(self) -> list[dict]:
        return [asdict(h) for h in self._hosts]

inv = Inventory()
inv.add(Host("web01", "prod", True))
print(json.dumps(inv.report(), indent=2))
EOF
python3 oop.py
```

### Final step – Cleanup note

```bash
python3 lab.py
# keep ~/rebash-python for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-python/lab09/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] Dry-run / fixture behaviour is clear for any mutating or cloud action
- [ ] You can relate this topic to a real DevOps or platform task

## Code Walkthrough

Production Python for **OOP — Classes and Dataclasses** always combines:

1. A clear entry point (`main()` + `if __name__ == "__main__"`)
2. A project virtual environment and pinned dependencies when third-party libs are used
3. Explicit error handling and logging (no silent `except Exception: pass`)
4. Safe I/O: `pathlib`, timeouts on HTTP, `subprocess.run([...])` without `shell=True`
5. Documented exit codes and dry-run defaults for mutating actions

Keep modules short enough to review in a single merge request. Prefer stdlib first; add httpx/requests, Typer, pytest, and platform SDKs when the job needs them.

## Security Considerations

- Treat all external input (args, files, env, API payloads) as untrusted until validated
- Never log secrets or `Authorization` headers; prefer masked CI variables and secret stores
- Prefer least privilege tokens and read-only / dry-run modes by default
- Avoid `shell=True`, unvalidated path deletes, and committing `.env` files
- Pin dependencies; review transitive packages for automation that runs in CI

## Common Mistakes

!!! warning "Using system Python without a venv"
    Global packages drift between laptops and CI. **Fix:** `python3 -m venv .venv` per project and pin dependencies.

!!! warning "Calling subprocess with shell=True"
    Untrusted strings become remote code execution. **Fix:** pass a list of arguments; never build a shell string for the happy path.

!!! warning "Mutating without dry-run"
    Cleanup and apply tools destroy shared environments. **Fix:** default to dry-run; require `--apply` for side effects.

## Best Practices

- One purpose per command; share helpers in a small library package
- Log to stderr; reserve stdout for data or RESULT lines
- Idempotent behaviour where schedulers and CI may retry
- Fixture / mock paths for GitHub, Docker, Kubernetes, Terraform, and cloud SDKs in CI
- Pair every new tool with at least one failing-path test you actually run

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `ModuleNotFoundError` in CI | Missing venv / pins | Recreate venv; install from lock/requirements |
| Works locally, fails in pipeline | Different Python or env | Pin `requires-python`; fingerprint env in the job |
| Hang on HTTP call | No timeout | Set `timeout=` on requests/httpx clients |
| Secrets in logs | Debug printing headers | Redact; never log tokens |
| Accidental prune/delete | No dry-run default | Default dry-run; label lab resources |

## Summary

**OOP — Classes and Dataclasses** is a core skill for DevOps engineers automating real hosts, APIs, and pipelines with Python. Practise the lab until the failure path and dry-run path are as familiar as the happy path, then continue the track.

## Interview Questions

1. When would you choose Python over Bash for this kind of ops task?
2. What failure mode appears if you skip a venv, pinning, or dry-run here?
3. How would you test this behaviour in CI without live cloud credentials?
4. Where could secrets leak in a naive implementation of this topic?
5. What exit code contract would you document for teammates?

!!! tip "Sample answer — question 2"
    Floating dependencies and missing dry-run defaults create “works on my machine” automation that either breaks overnight or mutates shared infrastructure unexpectedly. Pin versions and default to report-only.

## Related Tutorials

- [Python for DevOps Engineers – Category Overview](index.md)
- [Error Handling and Exceptions](error-handling-and-exceptions.md) *(previous)*
- [Logging and Debugging](logging-and-debugging.md) *(next)*
- [Shell Scripting for DevOps Engineers](../shell/index.md)
- [Learning Paths](../learning-paths/index.md)

## References

- [Python 3 documentation](https://docs.python.org/3/)
- [requests documentation](https://requests.readthedocs.io/)
- [httpx documentation](https://www.python-httpx.org/)
- Track index: [Python for DevOps Engineers](index.md)
