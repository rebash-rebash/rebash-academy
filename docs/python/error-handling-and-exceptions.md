---
title: "Error Handling and Exceptions"
description: "Master try/except/finally, raise, custom exceptions, and defensive programming patterns for reliable DevOps Python automation."
difficulty: intermediate
estimated_time: "45–60 min"
technology: python
category: python
module: "Module 8 · Error Handling"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - exceptions
  - defensive-programming
prerequisites:
  - python/file-handling-pathlib-json-yaml-csv
next:
  - python/oop-classes-and-dataclasses
related:
  - python/logging-and-debugging
  - python/production-engineering-patterns
labs: []
projects: []
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - exceptions
  - error-handling
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Error Handling and Exceptions

## Overview

Handle failures explicitly with `try`/`except`/`finally`, raise meaningful errors, and map exceptions to clear stderr messages and exit codes for CI and cron.

Silent `except Exception: pass` turns outages into mysteries. Ops tools must fail loudly with context, clean up resources, and leave a useful exit code.

Complete [File Handling](file-handling-pathlib-json-yaml-csv.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 8 · Error Handling** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [File Handling — pathlib, JSON, YAML, CSV](file-handling-pathlib-json-yaml-csv.md)
- Project venv with Python 3.12+

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Use `try` / `except` / `else` / `finally` correctly  
- [ ] Catch specific exceptions (not bare `Exception` by default)  
- [ ] `raise` and chain exceptions with `from`  
- [ ] Define a small custom exception type  
- [ ] Apply defensive checks before risky I/O  
- [ ] Map errors to non-zero exit codes

## Architecture

This topic’s control points and relationships are shown below.

![Error handling flow](../assets/excalidraw/python-error-handling.svg)

## Theory

### try / except / else / finally

```python
try:
    text = path.read_text(encoding="utf-8")
except FileNotFoundError:
    print(f"error: missing {path}", file=sys.stderr)
    return 1
else:
    # runs only if no exception
    process(text)
finally:
    # always runs — close handles, temp cleanup hooks
    ...
```

### Catch specifically

| Catch | When |
|-------|------|
| `FileNotFoundError` | Missing config |
| `ValueError` / `KeyError` | Bad config shape |
| `json.JSONDecodeError` | Corrupt JSON |
| `OSError` | Broader I/O (use carefully) |
| `Exception` | Last-resort boundary in `main` only |

Never swallow errors without logging.

### raise and chaining

```python
try:
    port = int(raw)
except ValueError as exc:
    raise ValueError(f"port must be int, got {raw!r}") from exc
```

### Custom exceptions

```python
class ConfigError(Exception):
    """Invalid operator-facing configuration."""
```

Use for domain failures callers can handle differently from bugs.

### Defensive programming

- Validate early (schema, required keys, ranges)  
- Prefer fail-fast over partial mutation  
- Default mutating tools to dry-run (Module 4)  
- Timeouts on network I/O (Module 14)

## Hands-on Lab

**Focus:** practise the core workflow for Error Handling and Exceptions

```bash
mkdir -p ~/rebash-python/module-08
cd ~/rebash-python/module-08

python3 -m venv .venv
source .venv/bin/activate
```

### Step 1 – Config loader with specific catches

```bash
cd ~/rebash-python/module-08
source .venv/bin/activate

cat > load_json.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


class ConfigError(Exception):
    pass


def load_replicas(path: Path) -> int:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ConfigError(f"missing config: {path}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ConfigError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict) or "replicas" not in data:
        raise ConfigError("config must include integer 'replicas'")
    try:
        replicas = int(data["replicas"])
    except (TypeError, ValueError) as exc:
        raise ConfigError("replicas must be an integer") from exc
    if replicas < 0:
        raise ConfigError("replicas must be >= 0")
    return replicas


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: load_json.py <file>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        replicas = load_replicas(path)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(replicas)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
EOF

echo '{"replicas": 3}' > ok.json
echo '{"replicas": "x"}' > bad.json
python load_json.py ok.json
python load_json.py missing.json || true
python load_json.py bad.json || true
```

### Step 2 – finally cleanup demo

```bash
python - <<'PY'
from pathlib import Path

scratch = Path("scratch.tmp")
try:
    scratch.write_text("demo", encoding="utf-8")
    raise RuntimeError("boom")
except RuntimeError as exc:
    print("caught", exc)
finally:
    if scratch.exists():
        scratch.unlink()
        print("cleaned scratch.tmp")
PY
```

### Step 3 – Anti-pattern (do not copy)

```bash
python - <<'PY'
# Bad — hides the failure
try:
    int("nope")
except Exception:
    pass
print("looks fine but is not")
PY
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-08/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Error Handling and Exceptions** always combines:

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

!!! warning "Skipping fundamentals for Error Handling and Exceptions"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Error Handling and Exceptions"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Error Handling and Exceptions changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Traceback in CI noise | Uncaught exception | Catch at `main`, log, exit |
| Empty catch | Swallowed error | Re-raise or return non-zero |
| Lost cause | `raise New()` without `from` | Chain with `from exc` |

## Summary

- Catch specific errors; map to exit codes  
- Custom exceptions for operator-facing config/domain failures  
- `finally` for cleanup; never silent `pass`  
- Fail fast with clear stderr

## Interview Questions

1. How does **Error Handling and Exceptions** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [OOP — Classes and Dataclasses](oop-classes-and-dataclasses.md)  
- [Logging and Debugging](logging-and-debugging.md)

## References

- [Errors and exceptions](https://docs.python.org/3/tutorial/errors.html)  
- [Exception hierarchy](https://docs.python.org/3/library/exceptions.html)
