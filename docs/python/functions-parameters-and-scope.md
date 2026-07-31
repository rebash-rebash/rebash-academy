---
title: "Functions — Parameters and Scope"
description: "Define reusable DevOps helpers with parameters, returns, default/keyword/variable arguments, lambdas, and scope rules."
difficulty: beginner
estimated_time: "45–60 min"
technology: python
category: python
module: "Module 4 · Functions"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - functions
  - scope
prerequisites:
  - python/control-flow-conditionals-and-loops
next:
  - python/data-structures-comprehensions-and-generators
related:
  - python/cli-applications-argparse-click-typer
  - python/error-handling-and-exceptions
labs: []
projects: []
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - functions
  - lambda
  - scope
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Functions — Parameters and Scope

## Overview

Write small, testable ops helpers with clear parameters, return values, and scope — so automation stays reviewable in a single merge request.

Readable automation is **functions with contracts**: inputs, return value, side effects (stderr, files, exit). Avoid 200-line `main` scripts; extract helpers early.

Complete [Control Flow](control-flow-conditionals-and-loops.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 4 · Functions** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Control Flow — Conditionals and Loops](control-flow-conditionals-and-loops.md)
- Project venv with Python 3.12+

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Define functions with type hints and docstrings  
- [ ] Use positional, keyword, and default arguments safely  
- [ ] Pack/unpack with `*args` and `**kwargs` when needed  
- [ ] Return values (and use `None` intentionally)  
- [ ] Explain LEGB scope and avoid mutable default traps  
- [ ] Use lambdas sparingly for short callbacks

## Architecture

Caller passes arguments; the function uses locals and may return a value or cause side effects.

![Functions and scope](../assets/excalidraw/python-functions-scope.svg)

## Theory

### Defining a function

```python
def check_port(port: int, host: str = "127.0.0.1") -> str:
    """Return a short status label for a TCP port check placeholder."""
    if not 1 <= port <= 65535:
        raise ValueError(f"invalid port: {port}")
    return f"{host}:{port}"
```

Prefer **type hints** and a one-line docstring. Raise on bad input; let callers decide exit codes.

### Parameters and returns

| Style | Example | Notes |
|-------|---------|--------|
| Positional | `check_port(8080)` | Order matters |
| Keyword | `check_port(port=8080, host="db")` | Clear at call site |
| Default | `host="127.0.0.1"` | Defaults evaluated once |
| Return | `return label` | Prefer data over printing inside helpers |

### `*args` and `**kwargs`

```python
def tag_line(service: str, *labels: str, **meta: str) -> str:
    bits = [service, *labels]
    extra = " ".join(f"{k}={v}" for k, v in sorted(meta.items()))
    return " ".join(bits) + (f" {extra}" if extra else "")
```

Use for thin wrappers; do not hide required parameters inside `**kwargs` in public APIs.

### Lambda

```python
names = ["web-b", "web-a"]
names.sort(key=lambda n: n)
```

Keep lambdas to one expression. Named `def` wins for anything with logic or a name in stack traces.

### Scope (LEGB)

Python resolves names: **Local → Enclosing → Global → Built-in**. Prefer passing values as arguments over mutating globals.

### Mutable default trap

```python
# Bad — shared list across calls
def add_host(host: str, bucket: list[str] = []) -> list[str]:
    bucket.append(host)
    return bucket

# Good
def add_host(host: str, bucket: list[str] | None = None) -> list[str]:
    if bucket is None:
        bucket = []
    bucket.append(host)
    return bucket
```

### `main()` pattern

```python
def main() -> int:
    ...
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

Helpers return data; `main` owns exit codes and stderr.

## Hands-on Lab

**Focus:** practise the core workflow for Functions — Parameters and Scope

```bash
mkdir -p ~/rebash-python/module-04
cd ~/rebash-python/module-04

python3 -m venv .venv
source .venv/bin/activate
```

### Step 1 – Severity helper

```bash
cd ~/rebash-python/module-04
source .venv/bin/activate

cat > severity.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import sys


def severity_rank(status: str) -> int:
    ranks = {"healthy": 0, "degraded": 1, "down": 2}
    if status not in ranks:
        raise ValueError(f"unknown status: {status!r}")
    return ranks[status]


def worst(statuses: list[str]) -> int:
    return max((severity_rank(s) for s in statuses), default=0)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: severity.py <status> [status...]", file=sys.stderr)
        return 2
    try:
        code = worst(argv[1:])
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(code)
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
EOF

python severity.py healthy degraded; echo exit=$?
python severity.py healthy down; echo exit=$?
```

### Step 2 – Keyword defaults and dry-run

```bash
python - <<'PY'
def delete_volume(volume_id: str, *, dry_run: bool = True) -> str:
    if dry_run:
        return f"DRY-RUN delete {volume_id}"
    return f"DELETED {volume_id}"

print(delete_volume("vol-1"))
print(delete_volume("vol-1", dry_run=False))
PY
```

Keyword-only `dry_run` after `*` prevents accidental positional mistakes.

### Step 3 – Prove mutable default bug (read-only lesson)

```bash
python - <<'PY'
def bad(item, bucket=[]):
    bucket.append(item)
    return bucket

print(bad("a"))
print(bad("b"))  # surprises: ['a', 'b']
PY
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-04/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Functions — Parameters and Scope** always combines:

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

!!! warning "Skipping fundamentals for Functions — Parameters and Scope"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Functions — Parameters and Scope"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Functions — Parameters and Scope changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `UnboundLocalError` | Assigning to name also read as global | Use parameter or `nonlocal` carefully |
| Shared list across calls | Mutable default | Use `None` sentinel |
| Hard to test | Prints inside helpers | Return strings; print in `main` |

## Summary

- Small functions with hints and clear returns  
- Keyword-only flags for dangerous options (`dry_run`)  
- No mutable defaults; no hidden globals  
- `main()` owns process exit codes

## Interview Questions

1. How does **Functions — Parameters and Scope** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Data Structures — Comprehensions and Generators](data-structures-comprehensions-and-generators.md)

## References

- [Defining functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)  
- [Typing](https://docs.python.org/3/library/typing.html)
