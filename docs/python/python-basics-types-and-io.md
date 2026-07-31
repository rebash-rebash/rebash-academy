---
title: "Python Basics — Types and I/O"
description: "Variables, data types, operators, strings, numbers, booleans, input/output, and type conversion for reliable DevOps automation scripts."
difficulty: beginner
estimated_time: "45–60 min"
technology: python
category: python
module: "Module 2 · Basics"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - types
  - strings
  - io
prerequisites:
  - python/python-fundamentals-install-venv-and-tooling
next:
  - python/control-flow-conditionals-and-loops
related:
  - python/file-handling-pathlib-json-yaml-csv
  - python/error-handling-and-exceptions
labs: []
projects: []
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - basics
  - types
  - io
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Python Basics — Types and I/O

## Overview

Use variables, core types, operators, and safe I/O/conversion patterns so ops scripts do not fail on sloppy types or silent bad input.

Inventory scripts, health checkers, and CLIs all start with names, numbers, and strings. This module makes those basics reliable for automation — with clear stderr messages and exit codes.

Complete [Module 1](python-fundamentals-install-venv-and-tooling.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 2 · Basics** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Python Fundamentals — Install, venv, and Tooling](python-fundamentals-install-venv-and-tooling.md)
- Active project venv with Python 3.12+

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Declare and name variables for ops scripts  
- [ ] Use `str`, `int`, `float`, `bool`, and `None` appropriately  
- [ ] Apply arithmetic, comparison, and logical operators  
- [ ] Format strings for logs and CLI output  
- [ ] Convert types safely with clear failure messages  
- [ ] Separate stdout (data) from stderr (diagnostics)

## Architecture

This topic’s control points and relationships are shown below.

![Python basics — types and I/O](../assets/excalidraw/python-basics-types.svg)

## Theory

### Variables and names

Names bind to objects. Prefer descriptive names: `region`, `replica_count`, `dry_run` — not `x`, `data2`.

```python
region = "eu-west-1"
replica_count = 3
dry_run = True
```

### Core types

| Type | Example | Ops use |
|------|---------|---------|
| `str` | `"prod"` | Names, paths, messages |
| `int` | `8080` | Ports, counts, exit codes |
| `float` | `99.5` | Ratios, latencies |
| `bool` | `True` | Flags (`dry_run`) |
| `None` | `None` | Missing optional value |

Check with `type(x)` or `isinstance(x, int)` when validating config.

### Operators

- Arithmetic: `+ - * / // % **`  
- Comparison: `== != < <= > >=`  
- Logical: `and or not`  

Use `//` for integer division when you need whole counts (e.g. shard sizes).

### Strings

```python
name = "api"
msg = f"checking {name} in {region}"
path = "logs/" + name + ".log"
```

Prefer **f-strings** for readability. For paths, later modules use `pathlib` — avoid hand-rolled slash bugs.

### Booleans and truthiness

Empty string, `0`, `None`, and empty collections are falsy. Be explicit when reading env flags:

```python
dry_run = os.environ.get("DRY_RUN", "1") not in {"0", "false", "False"}
```

(You will formalise env parsing in Module 11.)

### Input and output

- **`print(...)`** → stdout (data, RESULT lines)  
- **Diagnostics** → `print(..., file=sys.stderr)`  
- **`input()`** → interactive only; automation prefers CLI args (Module 12)

### Type conversion

```python
port = int("8080")       # OK
# int("8080/tcp")        # ValueError — catch and explain
flag = bool("False")     # True! non-empty string — avoid for flags
```

For flags, compare strings explicitly. For numbers, wrap `int()`/`float()` in `try/except` (Module 8) or validate before convert.

## Hands-on Lab

**Focus:** practise the core workflow for Python Basics — Types and I/O

```bash
mkdir -p ~/rebash-python/module-02
cd ~/rebash-python/module-02

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Step 1 – Types fingerprint

```bash
cd ~/rebash-python/module-02
source .venv/bin/activate

python - <<'PY'
region = "eu-west-1"
port = 8080
healthy = True
latency_ms = 12.5
print(type(region).__name__, type(port).__name__, type(healthy).__name__)
print(f"{region}:{port} healthy={healthy} latency={latency_ms}ms")
PY
```

### Step 2 – Safe port parsing helper

```bash
cat > parse_port.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import sys


def parse_port(raw: str) -> int:
    try:
        port = int(raw)
    except ValueError as exc:
        raise SystemExit(f"error: port must be an integer, got {raw!r}") from exc
    if not 1 <= port <= 65535:
        raise SystemExit(f"error: port out of range: {port}")
    return port


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: parse_port.py <port>", file=sys.stderr)
        return 2
    port = parse_port(argv[1])
    print(port)  # stdout = data
    print(f"parsed port={port}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
EOF

python parse_port.py 8080
python parse_port.py 99999 || true
python parse_port.py abc || true
```

### Step 3 – Operators for a simple SLO check

```bash
python - <<'PY'
success = 980
total = 1000
ratio = success / total
slo = 0.99
ok = ratio >= slo
print(f"success_ratio={ratio:.4f} meets_slo={ok}")
raise SystemExit(0 if ok else 1)
PY
```

### Step 4 – String hygiene for logs

```bash
python - <<'PY'
service = "checkout"
env = "prod"
# Prefer structured-looking lines early — Module 10 adds logging
print(f"service={service} env={env} event=start", file=__import__("sys").stderr)
PY
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-02/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Python Basics — Types and I/O** always combines:

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

!!! warning "Skipping fundamentals for Python Basics — Types and I/O"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Python Basics — Types and I/O"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Python Basics — Types and I/O changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `ValueError: invalid literal` | Bad `int()` input | Validate; clear stderr message |
| `bool("False")` is True | Non-empty string | Compare to `"true"`/`"1"` explicitly |
| Logs mixed with JSON | Everything on stdout | Put diagnostics on stderr |

## Summary

- Names and types are the foundation of safe automation  
- Convert carefully; never trust raw strings from env/CLI  
- stdout for data, stderr for humans and CI logs

## Interview Questions

1. How does **Python Basics — Types and I/O** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Control Flow — Conditionals and Loops](control-flow-conditionals-and-loops.md)  
- [File Handling](file-handling-pathlib-json-yaml-csv.md)

## References

- [Built-in types](https://docs.python.org/3/library/stdtypes.html)  
- [str.format / f-strings](https://docs.python.org/3/tutorial/inputoutput.html)
