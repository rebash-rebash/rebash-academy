---
title: "Logging and Debugging"
description: "Configure the logging module, log levels, structured logs, pdb, and traceback reading for DevOps Python automation."
difficulty: intermediate
estimated_time: "45–60 min"
technology: python
category: python
module: "Module 10 · Logging & Debugging"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - logging
  - debugging
  - pdb
prerequisites:
  - python/oop-classes-and-dataclasses
next:
  - python/configuration-management-and-secrets
related:
  - python/error-handling-and-exceptions
  - python/production-engineering-patterns
labs:
  - labs/python-log-analyser
projects: []
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - logging
  - pdb
  - debugging
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Logging and Debugging

## Overview

Emit useful logs at the right levels (including structured JSON for aggregators), read tracebacks quickly, and use `pdb` when a failing path is unclear.

`print` is fine in Module 2 labs. Production automation needs **logging**: levels, correlation fields, no secrets, and stderr by default so stdout stays for data.

Complete [OOP](oop-classes-and-dataclasses.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 10 · Logging & Debugging** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [OOP — Classes and Dataclasses](oop-classes-and-dataclasses.md)
- [Error Handling and Exceptions](error-handling-and-exceptions.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Configure `logging` with a basic stderr handler  
- [ ] Choose DEBUG / INFO / WARNING / ERROR / CRITICAL  
- [ ] Emit structured key=value or JSON log lines  
- [ ] Read a traceback to the failing line  
- [ ] Break into `pdb` on a stubborn bug  
- [ ] Avoid logging secrets

## Architecture

This topic’s control points and relationships are shown below.

![Logging and debugging](../assets/excalidraw/python-logging-debug.svg)

## Theory

### logging basics

```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger("inventory")
log.info("start env=%s", "lab")
```

Use `%s` lazy formatting (not f-strings in hot DEBUG loops) so expensive messages are skipped when filtered.

### Levels

| Level | Ops meaning |
|-------|-------------|
| DEBUG | Detail for authors |
| INFO | Normal milestones |
| WARNING | Degraded but continuing |
| ERROR | Failed operation |
| CRITICAL | About to exit / page |

### Structured logging

Prefer stable fields for Loki/CloudWatch/ELK:

```python
log.info("check_done name=%s ok=%s duration_ms=%d", name, ok, ms)
# or json.dumps({"event": "check_done", "name": name, "ok": ok})
```

### Tracebacks

Unread tracebacks waste incidents. Read **bottom frame first** (your file:line), then causes. `logging.exception("...")` inside `except` attaches the traceback.

### pdb

```python
breakpoint()  # Python 3.7+
# or: python -m pdb script.py
```

Commands: `l` list, `n` next, `s` step, `c` continue, `p expr`, `q` quit. Remove breakpoints before committing.

### Debugging techniques

1. Reproduce with a fixture  
2. Add one INFO/DEBUG at the boundary  
3. Binary-search the failing branch  
4. `pdb` only when state is unclear  
5. Fix + add a regression test (Module 22)

## Hands-on Lab

**Focus:** practise the core workflow for Logging and Debugging

```bash
mkdir -p ~/rebash-python/module-10
cd ~/rebash-python/module-10

python3 -m venv .venv
source .venv/bin/activate
```

### Step 1 – Configure a module logger

```bash
cd ~/rebash-python/module-10
source .venv/bin/activate

cat > app_log.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import logging
import sys


def setup(level: str = "INFO") -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(levelname)s %(name)s %(message)s",
        stream=sys.stderr,
    )
    return logging.getLogger("healthcheck")


def main() -> int:
    log = setup("INFO")
    log.info("event=start")
    try:
        int("nope")
    except ValueError:
        log.exception("event=parse_failed field=replicas")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python app_log.py || true
```

### Step 2 – Structured fields

```bash
python - <<'PY'
import logging, sys
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(message)s")
log = logging.getLogger("inv")
for host, ok in [("web-a", True), ("web-b", False)]:
    log.info("event=host_check host=%s ok=%s", host, str(ok).lower())
PY
```

### Step 3 – Traceback reading

```bash
python - <<'PY'
def inner():
    return 1 / 0

def outer():
    return inner()

outer()
PY
```

Note the bottom frame pointing at `1 / 0`.

### Step 4 – Optional pdb (interactive)

```bash
# Run only if you can interact with the terminal:
# python - <<'PY'
# x = 1
# breakpoint()
# print(x)
# PY
echo "Use breakpoint() locally when you need a REPL on a frozen value"
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-10/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Logging and Debugging** always combines:

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

!!! warning "Skipping fundamentals for Logging and Debugging"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Logging and Debugging"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Logging and Debugging changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| No log output | Level too high / wrong logger | Set root/basicConfig; check name |
| Logs on stdout | Handler stream | Use `stream=sys.stderr` |
| Secret leak | Logged env/headers | Redact; never log `Authorization` |

## Summary

- `logging` to stderr with levels and stable fields  
- `exception()` on unexpected failures  
- Tracebacks: read the bottom frame first  
- `pdb` for hard state; tests for regressions

## Interview Questions

1. How does **Logging and Debugging** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Configuration Management and Secrets](configuration-management-and-secrets.md)

## References

- [logging](https://docs.python.org/3/library/logging.html)  
- [pdb](https://docs.python.org/3/library/pdb.html)
