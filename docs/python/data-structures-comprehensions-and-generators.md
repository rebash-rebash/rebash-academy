---
title: "Data Structures — Comprehensions and Generators"
description: "Lists, tuples, dictionaries, sets, comprehensions, iterators, and generators for inventory and log processing."
difficulty: beginner
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: python
tags:
  - python
  - lists
  - dicts
  - generators
prerequisites:
  - Functions — Parameters and Scope
  - Python 3.12+ on Linux (WSL2/VM/cloud)
comments: false
---

# Data Structures — Comprehensions and Generators

## Overview

Inventories, labels, and log streams are collections. Choose the right structure and stream large data with generators.

This is **Tutorial 5** in **Module 5: Data Structures** of the REBASH Academy **Python for DevOps Engineers** series — written for DevOps engineers, SREs, platform engineers, and cloud engineers who automate infrastructure with production-quality Python.

## Prerequisites

- Functions — Parameters and Scope
- Python 3.12+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Data Structures — Comprehensions and Generators” in real ops automation
- [ ] Use a project venv and avoid relying on system site-packages
- [ ] Produce clear stderr diagnostics and meaningful exit codes
- [ ] Prefer safe patterns (pathlib, subprocess list args, dry-run)
- [ ] Relate this topic to day-to-day DevOps and platform work

## Architecture

Ops Python sits between operators/CI and platforms (files, APIs, CLIs, and cloud control planes). This topic’s control points are shown below.

![Architecture diagram for Data Structures — Comprehensions and Generators](../assets/images/python-data-structures.svg)

## Theory

### Lists

Ordered, mutable sequences: `hosts = ["web01", "web02"]`. Methods: `append`, `extend`, `sort`, `pop`. Use lists for ordered inventories and CLI argument lists for `subprocess`.

### Tuples

Immutable sequences — good for fixed records: `("web", 8080)`. Prefer tuples as dict keys when you need composite keys.

### Dictionaries

Key/value maps for JSON-like configs and inventories: `{"name": "api", "replicas": 2}`. Prefer `.get(key, default)` and validate required keys explicitly.

### Sets

Unordered unique membership: useful for comparing desired vs actual host sets (`desired - actual`).

### List Comprehensions

```python
failed = [h for h in hosts if h["status"] != "ok"]
```

Keep them readable; nest sparingly. Prefer generator expressions for large streams.

### Dictionary Comprehensions

```python
by_name = {h["name"]: h for h in hosts}
```

Ideal for indexing inventories after a cloud SDK call.

### Iterators

Objects supporting `__iter__` / `__next__`. Files, `range`, and dict views are iterators — they stream without loading everything into memory.

### Generators

Functions with `yield` produce values lazily — perfect for multi-gigabyte logs:

```python
def lines(path: Path):
    with path.open() as fh:
        for line in fh:
            yield line.rstrip("\n")
```

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-python/lab05 && cd ~/rebash-python/lab05
```

**Focus:** build inventory list/dict/set; stream a log with a generator

### Step 1 – Skeleton

```bash
cat > lab.py << 'EOF'
#!/usr/bin/env python3
print("lab05 data-structures-comprehensions-and-generators")
EOF
chmod +x lab.py
python3 lab.py
```

### Step 2 – Structures and generators

```bash
cat > inventory.json << 'EOF'
[{"name":"web","env":"prod"},{"name":"db","env":"prod"},{"name":"bastion","env":"ops"}]
EOF
printf 'a\nb\na\n' > sample.log
cat > structs.py << 'EOF'
#!/usr/bin/env python3
import json
from pathlib import Path

def lines(path: Path):
    with path.open() as fh:
        for line in fh:
            yield line.rstrip("\n")

hosts = json.loads(Path("inventory.json").read_text())
by_env = {h["name"]: h["env"] for h in hosts}
envs = {h["env"] for h in hosts}
print(by_env)
print(sorted(envs))
print(list(lines(Path("sample.log"))))
EOF
python3 structs.py
```

### Final step – Cleanup note

```bash
python3 lab.py
# keep ~/rebash-python for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-python/lab05/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] Dry-run / fixture behaviour is clear for any mutating or cloud action
- [ ] You can relate this topic to a real DevOps or platform task

## Code Walkthrough

Production Python for **Data Structures — Comprehensions and Generators** always combines:

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

**Data Structures — Comprehensions and Generators** is a core skill for DevOps engineers automating real hosts, APIs, and pipelines with Python. Practise the lab until the failure path and dry-run path are as familiar as the happy path, then continue the track.

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
- [Functions — Parameters and Scope](functions-parameters-and-scope.md) *(previous)*
- [Modules, Packages, and Dependencies](modules-packages-and-dependencies.md) *(next)*
- [Shell Scripting for DevOps Engineers](../shell/index.md)
- [Learning Paths](../learning-paths/index.md)

## References

- [Python 3 documentation](https://docs.python.org/3/)
- [requests documentation](https://requests.readthedocs.io/)
- [httpx documentation](https://www.python-httpx.org/)
- Track index: [Python for DevOps Engineers](index.md)
