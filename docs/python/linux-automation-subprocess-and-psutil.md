---
title: "Linux Automation — subprocess and psutil"
description: "Drive Linux safely with subprocess, os, pathlib, shutil, signal, psutil, process management, and permissions — never shell=True on the happy path."
difficulty: intermediate
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: python
tags:
  - python
  - subprocess
  - psutil
  - linux
prerequisites:
  - CLI Applications — argparse, Click, and Typer
  - Python 3.12+ on Linux (WSL2/VM/cloud)
comments: false
---

# Linux Automation — subprocess and psutil

## Overview

Python should call system tools with argument lists, timeouts, and captured stderr — not by building shell strings.

This is **Tutorial 13** in **Module 13: Linux Automation** of the REBASH Academy **Python for DevOps Engineers** series — written for DevOps engineers, SREs, platform engineers, and cloud engineers who automate infrastructure with production-quality Python.

## Prerequisites

- CLI Applications — argparse, Click, and Typer
- Python 3.12+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Linux Automation — subprocess and psutil” in real ops automation
- [ ] Use a project venv and avoid relying on system site-packages
- [ ] Produce clear stderr diagnostics and meaningful exit codes
- [ ] Prefer safe patterns (pathlib, subprocess list args, dry-run)
- [ ] Relate this topic to day-to-day DevOps and platform work

## Architecture

Ops Python sits between operators/CI and platforms (files, APIs, CLIs, and cloud control planes). This topic’s control points are shown below.

![Architecture diagram for Linux Automation — subprocess and psutil](../assets/images/python-linux-automation.svg)

## Theory

### subprocess

```python
subprocess.run(["systemctl", "is-active", "nginx"], check=False, capture_output=True, text=True, timeout=30)
```

Pass a **list** of args. Set `timeout`. Inspect `returncode`, `stdout`, `stderr`.

### os

Environment, getuid, and low-level helpers. Prefer `pathlib` for paths. Use `os.environ` copies carefully when spawning children.

### pathlib

Resolve and validate paths before mutating. Combine with subprocess for tools that need path arguments.

### shutil

Copy/move/which — wrap deletes behind dry-run. `shutil.which("kubectl")` before assuming binaries exist.

### signal

Handle SIGTERM/SIGINT for graceful shutdown of long pollers. Register handlers that set a stop flag rather than ignoring signals.

### psutil

Cross-platform process and host metrics (CPU, memory, connections). Ideal for Linux health checkers when available; degrade gracefully if missing.

### Process Management

List, inspect, and — carefully — terminate processes. Prefer signalling your own children. Never kill by fuzzy name match in production without allow-lists.

### File Permissions

Inspect with `Path.stat().st_mode`; set with `chmod`. Secret files should be `0o600`. Refuse to run if a private key is group/world-readable.

**CRITICAL:** never use `shell=True` on the happy path. If you must for a legacy one-liner, pass a constant string and never interpolate untrusted input.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-python/lab13 && cd ~/rebash-python/lab13
```

**Focus:** Linux health checker with subprocess list args + optional psutil; prove no shell=True

### Step 1 – Skeleton

```bash
cat > lab.py << 'EOF'
#!/usr/bin/env python3
print("lab13 linux-automation-subprocess-and-psutil")
EOF
chmod +x lab.py
python3 lab.py
```

### Step 2 – Linux health checker

```bash
cat > health.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path

def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=30)

def main() -> int:
    df = run(["df", "-h", "."])
    print(df.stdout.splitlines()[0] if df.stdout else "df failed")
    which_python = shutil.which("python3")
    print(f"python3={which_python}")
    mode = Path(__file__).stat().st_mode & 0o777
    print(f"mode={oct(mode)}")
    try:
        import psutil  # optional
        print(f"cpu_percent={psutil.cpu_percent(interval=0.1)}")
    except ImportError:
        print("psutil optional — skipped", file=sys.stderr)
    # Explicit: never shell=True
    print("RESULT ok")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
EOF
python3 health.py
```

### Final step – Cleanup note

```bash
python3 lab.py
# keep ~/rebash-python for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-python/lab13/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] Dry-run / fixture behaviour is clear for any mutating or cloud action
- [ ] You can relate this topic to a real DevOps or platform task

## Code Walkthrough

Production Python for **Linux Automation — subprocess and psutil** always combines:

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

**Linux Automation — subprocess and psutil** is a core skill for DevOps engineers automating real hosts, APIs, and pipelines with Python. Practise the lab until the failure path and dry-run path are as familiar as the happy path, then continue the track.

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
- [CLI Applications — argparse, Click, and Typer](cli-applications-argparse-click-typer.md) *(previous)*
- [REST APIs — requests, Auth, and Resilience](rest-apis-requests-auth-and-resilience.md) *(next)*
- [Shell Scripting for DevOps Engineers](../shell/index.md)
- [Learning Paths](../learning-paths/index.md)

## References

- [Python 3 documentation](https://docs.python.org/3/)
- [requests documentation](https://requests.readthedocs.io/)
- [httpx documentation](https://www.python-httpx.org/)
- Track index: [Python for DevOps Engineers](index.md)
