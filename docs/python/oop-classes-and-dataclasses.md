---
title: "OOP — Classes and Dataclasses"
description: "Classes, objects, methods, constructors, inheritance, encapsulation, polymorphism, and dataclasses for DevOps configuration and check models."
difficulty: intermediate
estimated_time: "50–65 min"
technology: python
category: python
module: "Module 9 · OOP"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - oop
  - dataclasses
prerequisites:
  - python/error-handling-and-exceptions
next:
  - python/logging-and-debugging
related:
  - python/configuration-management-and-secrets
  - python/cli-applications-argparse-click-typer
labs: []
projects: []
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - oop
  - dataclasses
  - classes
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# OOP — Classes and Dataclasses

## Overview

Model ops concepts with classes and dataclasses — configuration records, health checks, and small plugin-style interfaces — without over-engineering.

You do not need enterprise OOP hierarchies for a shell script. You do need clear types when a tool grows: a `ServiceCheck`, a `CloudAccount`, a dataclass loaded from YAML. Prefer **dataclasses** for data; classes with methods for behaviour.

Complete [Error Handling](error-handling-and-exceptions.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 9 · OOP** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Error Handling and Exceptions](error-handling-and-exceptions.md)
- Functions and data structures modules

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Define a class with `__init__` and methods  
- [ ] Use inheritance for shared check behaviour  
- [ ] Apply encapsulation with clear public APIs  
- [ ] Rely on duck typing / polymorphism for runners  
- [ ] Model config with `@dataclass`  
- [ ] Know when a function is enough

## Architecture

This topic’s control points and relationships are shown below.

![Classes and dataclasses](../assets/excalidraw/python-oop-dataclasses.svg)

## Theory

### Classes and objects

```python
class ServiceCheck:
    def __init__(self, name: str, endpoint: str) -> None:
        self.name = name
        self.endpoint = endpoint

    def label(self) -> str:
        return f"{self.name}->{self.endpoint}"
```

### Constructors and methods

`__init__` initialises instance state. Instance methods take `self`. Prefer explicit parameters over hidden globals.

### Inheritance

```python
class HttpCheck(ServiceCheck):
    def __init__(self, name: str, endpoint: str, timeout: float = 5.0) -> None:
        super().__init__(name, endpoint)
        self.timeout = timeout
```

Keep hierarchies shallow (one or two levels) in ops tools.

### Encapsulation

Public attributes are fine for simple records. Use a leading underscore for internal helpers (`_parse`). Properties when validation on set matters.

### Polymorphism

A runner can call `.run()` on any check object that implements it — no formal interface required (duck typing). Protocols/`typing.Protocol` optional for larger codebases.

### Dataclasses

```python
from dataclasses import dataclass

@dataclass(slots=True)
class AppConfig:
    env: str
    replicas: int
    dry_run: bool = True
```

Great for YAML/JSON-shaped config. Add methods only when behaviour belongs with the data.

### When not to use classes

A pure function that formats a string does not need a class. Start with functions; promote to classes when state + multiple operations cluster together.

## Hands-on Lab

**Focus:** practise the core workflow for OOP — Classes and Dataclasses

```bash
mkdir -p ~/rebash-python/module-09
cd ~/rebash-python/module-09

python3 -m venv .venv
source .venv/bin/activate
```

### Step 1 – Dataclass config

```bash
cd ~/rebash-python/module-09
source .venv/bin/activate

cat > models.py << 'EOF'
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AppConfig:
    env: str
    replicas: int
    dry_run: bool = True

    def validate(self) -> None:
        if self.replicas < 0:
            raise ValueError("replicas must be >= 0")
        if not self.env:
            raise ValueError("env required")
EOF

python - <<'PY'
from models import AppConfig
cfg = AppConfig(env="lab", replicas=2)
cfg.validate()
print(cfg)
PY
```

### Step 2 – Check hierarchy

```bash
cat > checks.py << 'EOF'
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CheckResult:
    name: str
    ok: bool
    detail: str


class BaseCheck:
    name: str

    def run(self) -> CheckResult:
        raise NotImplementedError


class StaticCheck(BaseCheck):
    def __init__(self, name: str, ok: bool, detail: str = "") -> None:
        self.name = name
        self._ok = ok
        self._detail = detail

    def run(self) -> CheckResult:
        return CheckResult(self.name, self._ok, self._detail)


def run_all(checks: list[BaseCheck]) -> int:
    worst = 0
    for check in checks:
        result = check.run()
        print(f"{result.name}: {'ok' if result.ok else 'FAIL'} {result.detail}")
        if not result.ok:
            worst = 1
    return worst
EOF

python - <<'PY'
from checks import StaticCheck, run_all
raise SystemExit(run_all([
    StaticCheck("dns", True, "resolved"),
    StaticCheck("disk", False, "90% used"),
]))
PY
```

### Step 3 – Polymorphism in a loop

Confirm `run_all` only needs objects with `.run()` — add another check class inline if you like.

## Validation

- [ ] Lab commands run under `~/rebash-python/module-09/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **OOP — Classes and Dataclasses** always combines:

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

!!! warning "Skipping fundamentals for OOP — Classes and Dataclasses"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for OOP — Classes and Dataclasses"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode OOP — Classes and Dataclasses changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Forgot `super().__init__` | Incomplete subclass init | Call super with required args |
| Mutable dataclass default | Shared list/dict | `field(default_factory=list)` |
| God class | Too many responsibilities | Split data vs runner vs I/O |

## Summary

- Classes for behaviour + state; dataclasses for records  
- Shallow inheritance; duck-typed runners  
- Validate on models; keep I/O at the edges  
- Functions first; classes when they earn their keep

## Interview Questions

1. How does **OOP — Classes and Dataclasses** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Logging and Debugging](logging-and-debugging.md)

## References

- [Classes tutorial](https://docs.python.org/3/tutorial/classes.html)  
- [dataclasses](https://docs.python.org/3/library/dataclasses.html)
