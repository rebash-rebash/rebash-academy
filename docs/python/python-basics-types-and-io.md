---
title: "Python Basics — Types and I/O"
description: "Variables, data types, operators, strings, numbers, booleans, input/output, and type conversion for ops scripts."
difficulty: beginner
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: python
tags:
  - python
  - basics
  - types
  - io
prerequisites:
  - Python Fundamentals — Install, venv, and Tooling
  - Python 3.12+ on Linux (WSL2/VM/cloud)
comments: false
---

# Python Basics — Types and I/O

## Overview

Ops scripts fail when types and I/O are sloppy. Master the basics before control flow and APIs.

This is **Tutorial 2** in **Module 2: Python Basics** of the REBASH Academy **Python for DevOps Engineers** series — written for DevOps engineers, SREs, platform engineers, and cloud engineers who automate infrastructure with production-quality Python.

## Prerequisites

- Python Fundamentals — Install, venv, and Tooling
- Python 3.12+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Python Basics — Types and I/O” in real ops automation
- [ ] Use a project venv and avoid relying on system site-packages
- [ ] Produce clear stderr diagnostics and meaningful exit codes
- [ ] Prefer safe patterns (pathlib, subprocess list args, dry-run)
- [ ] Relate this topic to day-to-day DevOps and platform work

## Architecture

Ops Python sits between operators/CI and platforms (files, APIs, CLIs, and cloud control planes). This topic’s control points are shown below.

![Architecture diagram for Python Basics — Types and I/O](../assets/images/python-basics-types.svg)

## Theory

### Variables

Assign with `name = value`. Names are case-sensitive. Prefer `snake_case` for locals and functions; `UPPER_SNAKE` for module-level constants. Avoid single-letter names except short loop indices.

### Data Types

Common ops types: `str`, `int`, `float`, `bool`, `list`, `dict`, `tuple`, `None`. Use `type(x)` sparingly in debugging; prefer type hints on public functions.

### Operators

Arithmetic (`+ - * / // % **`), comparison (`== != < > <= >=`), logical (`and or not`), membership (`in`), identity (`is` / `is not` — use for `None`). Prefer `//` for integer division in counters.

### Strings

Strings are immutable. Prefer f-strings for logs: `f"host={host}"`. Methods: `strip`, `split`, `join`, `startswith`, `endswith`, `replace`. Never build shell commands by concatenating untrusted strings.

### Numbers

`int` for counts and exit codes; `float` for ratios. Beware float equality — compare with tolerances when parsing metrics. Exit codes stay integers 0–255.

### Booleans

`True` / `False`. Truthiness: empty `""`, `[]`, `{}`, `0`, and `None` are false. Prefer explicit checks for ops flags: `if dry_run is True`.

### Input

`input()` reads a line from stdin (interactive labs only). Production tools prefer CLI args (`sys.argv` / argparse) and environment variables — never block a cron job on `input()`.

### Output

`print(...)` writes to stdout. Diagnostics belong on stderr:

```python
print("RESULT ok")
print("progress...", file=sys.stderr)
```

Keep machine-readable results on stdout so pipes stay clean.

### Type Conversion

`int("42")`, `str(3)`, `bool(1)`, `float("1.5")`. Wrap conversions in `try`/`except ValueError` when parsing external text. Prefer `pathlib.Path` over raw strings for filesystem paths (Module 7).

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-python/lab02 && cd ~/rebash-python/lab02
```

**Focus:** types and operators drills; stderr vs stdout; safe int conversion helper

### Step 1 – Skeleton

```bash
cat > lab.py << 'EOF'
#!/usr/bin/env python3
print("lab02 python-basics-types-and-io")
EOF
chmod +x lab.py
python3 lab.py
```

### Step 2 – Types and I/O

```bash
cat > basics.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations
import sys

def to_int(raw: str) -> int:
    try:
        return int(raw.strip())
    except ValueError as exc:
        print(f"invalid int: {raw!r}", file=sys.stderr)
        raise SystemExit(2) from exc

def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(f"usage: {argv[0]} N", file=sys.stderr)
        return 2
    n = to_int(argv[1])
    print(f"RESULT n={n} doubled={n * 2}")
    print("ok", file=sys.stderr)
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
EOF
python3 basics.py 21
python3 basics.py nope || echo "exit=$?"
```

### Final step – Cleanup note

```bash
python3 lab.py
# keep ~/rebash-python for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-python/lab02/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] Dry-run / fixture behaviour is clear for any mutating or cloud action
- [ ] You can relate this topic to a real DevOps or platform task

## Code Walkthrough

Production Python for **Python Basics — Types and I/O** always combines:

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

**Python Basics — Types and I/O** is a core skill for DevOps engineers automating real hosts, APIs, and pipelines with Python. Practise the lab until the failure path and dry-run path are as familiar as the happy path, then continue the track.

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
- [Python Fundamentals — Install, venv, and Tooling](python-fundamentals-install-venv-and-tooling.md) *(previous)*
- [Control Flow — Conditionals and Loops](control-flow-conditionals-and-loops.md) *(next)*
- [Shell Scripting for DevOps Engineers](../shell/index.md)
- [Learning Paths](../learning-paths/index.md)

## References

- [Python 3 documentation](https://docs.python.org/3/)
- [requests documentation](https://requests.readthedocs.io/)
- [httpx documentation](https://www.python-httpx.org/)
- Track index: [Python for DevOps Engineers](index.md)
