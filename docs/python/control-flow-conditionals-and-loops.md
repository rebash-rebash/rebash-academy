---
title: "Control Flow — Conditionals and Loops"
description: "Branch and iterate with if/elif/else, match, for, while, break, continue, and pass in ops automation."
difficulty: beginner
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: python
tags:
  - python
  - control-flow
  - match
  - loops
prerequisites:
  - Python Basics — Types and I/O
  - Python 3.12+ on Linux (WSL2/VM/cloud)
comments: false
---

# Control Flow — Conditionals and Loops

## Overview

Health checks and CLI verbs are mostly control flow. Get branching and loops right before larger frameworks.

This is **Tutorial 3** in **Module 3: Control Flow** of the REBASH Academy **Python for DevOps Engineers** series — written for DevOps engineers, SREs, platform engineers, and cloud engineers who automate infrastructure with production-quality Python.

## Prerequisites

- Python Basics — Types and I/O
- Python 3.12+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Control Flow — Conditionals and Loops” in real ops automation
- [ ] Use a project venv and avoid relying on system site-packages
- [ ] Produce clear stderr diagnostics and meaningful exit codes
- [ ] Prefer safe patterns (pathlib, subprocess list args, dry-run)
- [ ] Relate this topic to day-to-day DevOps and platform work

## Architecture

Ops Python sits between operators/CI and platforms (files, APIs, CLIs, and cloud control planes). This topic’s control points are shown below.

![Architecture diagram for Control Flow — Conditionals and Loops](../assets/images/python-control-flow.svg)

## Theory

### if

```python
if code != 0:
    print("failed", file=sys.stderr)
    raise SystemExit(code)
```

Use guard clauses early so the happy path stays left-aligned.

### elif

Chain mutually exclusive conditions with `elif`. Prefer dictionaries or `match` when the set of verbs grows.

### else

`else` covers the remaining case. On loops, `for`/`while`…`else` runs only if no `break` — rarely useful in ops scripts; prefer explicit flags.

### match

Python 3.10+ structural pattern matching suits CLI verbs and status enums:

```python
match verb:
    case "check" | "status":
        return check()
    case "apply":
        return apply(dry_run=False)
    case _:
        raise SystemExit(f"unknown verb: {verb}")
```

### for

Iterate collections and ranges: `for host in hosts:`, `for line in path.open():`. Prefer iterating files line-by-line over `read().splitlines()` for large logs.

### while

Use `while` for retries and poll loops with a clear exit:

```python
attempts = 0
while attempts < 3:
    if probe():
        break
    attempts += 1
```

Avoid infinite loops without a timeout.

### break

Exit the nearest loop immediately — useful when a host is healthy or a fatal error appears.

### continue

Skip to the next iteration — skip blank lines, comments, or dry-run-only hosts.

### pass

A no-op placeholder. Prefer real stubs that raise `NotImplementedError` in production code so unfinished paths fail loudly.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-python/lab03 && cd ~/rebash-python/lab03
```

**Focus:** classify log levels with if/match; retry loop with break/continue

### Step 1 – Skeleton

```bash
cat > lab.py << 'EOF'
#!/usr/bin/env python3
print("lab03 control-flow-conditionals-and-loops")
EOF
chmod +x lab.py
python3 lab.py
```

### Step 2 – Control flow

```bash
cat > flow.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations
import sys

def classify(level: str) -> str:
    match level.upper():
        case "INFO" | "DEBUG":
            return "low"
        case "WARN" | "WARNING":
            return "medium"
        case "ERROR" | "CRITICAL":
            return "high"
        case _:
            raise ValueError(level)

def main(argv: list[str]) -> int:
    for raw in argv[1:]:
        if not raw.strip():
            continue
        try:
            print(f"{raw}->{classify(raw)}")
        except ValueError:
            print(f"skip:{raw}", file=sys.stderr)
            continue
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
EOF
python3 flow.py INFO WARN nope ERROR
```

### Final step – Cleanup note

```bash
python3 lab.py
# keep ~/rebash-python for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-python/lab03/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] Dry-run / fixture behaviour is clear for any mutating or cloud action
- [ ] You can relate this topic to a real DevOps or platform task

## Code Walkthrough

Production Python for **Control Flow — Conditionals and Loops** always combines:

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

**Control Flow — Conditionals and Loops** is a core skill for DevOps engineers automating real hosts, APIs, and pipelines with Python. Practise the lab until the failure path and dry-run path are as familiar as the happy path, then continue the track.

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
- [Python Basics — Types and I/O](python-basics-types-and-io.md) *(previous)*
- [Functions — Parameters and Scope](functions-parameters-and-scope.md) *(next)*
- [Shell Scripting for DevOps Engineers](../shell/index.md)
- [Learning Paths](../learning-paths/index.md)

## References

- [Python 3 documentation](https://docs.python.org/3/)
- [requests documentation](https://requests.readthedocs.io/)
- [httpx documentation](https://www.python-httpx.org/)
- Track index: [Python for DevOps Engineers](index.md)
