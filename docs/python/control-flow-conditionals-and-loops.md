---
title: "Control Flow — Conditionals and Loops"
description: "Master if/elif/else, match, for/while loops, and break/continue/pass for DevOps automation scripts and inventory tools."
difficulty: beginner
estimated_time: "45–60 min"
technology: python
category: python
module: "Module 3 · Control Flow"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - control-flow
  - loops
prerequisites:
  - python/python-basics-types-and-io
next:
  - python/functions-parameters-and-scope
related:
  - python/data-structures-comprehensions-and-generators
  - python/error-handling-and-exceptions
labs: []
projects: []
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - control-flow
  - loops
  - match
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Control Flow — Conditionals and Loops

## Overview

Branch and iterate confidently with `if`/`match`, `for`/`while`, and loop control so inventory, health-check, and remediation scripts stay readable and correct.

Automation is mostly “for each host/resource, if unhealthy then alert.” This module makes that structure explicit before functions and data structures.

Complete [Python Basics](python-basics-types-and-io.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 3 · Control Flow** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Python Basics — Types and I/O](python-basics-types-and-io.md)
- Project venv from Module 1–2

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Write `if` / `elif` / `else` branches for ops decisions  
- [ ] Use `match` for multi-way status or action dispatch (3.10+)  
- [ ] Iterate with `for` over sequences and `range`  
- [ ] Use `while` for retry-style loops carefully  
- [ ] Apply `break`, `continue`, and `pass` intentionally

## Architecture

This topic’s control points and relationships are shown below.

![Control flow](../assets/excalidraw/python-control-flow.svg)

## Theory

### if / elif / else

```python
status = "degraded"
if status == "healthy":
    action = "noop"
elif status == "degraded":
    action = "page_secondary"
else:
    action = "page_primary"
```

Keep conditions boolean-clear. Prefer early returns in functions (Module 4) over deep nesting.

### match (structural pattern matching)

Useful for status codes and command verbs:

```python
code = 503
match code:
    case 200 | 204:
        level = "ok"
    case 404:
        level = "missing"
    case 500 | 502 | 503 | 504:
        level = "upstream"
    case _:
        level = "other"
```

Requires Python 3.10+. This course assumes 3.12+.

### for loops

```python
hosts = ["web-a", "web-b", "web-c"]
for host in hosts:
    print(f"check {host}")

for i in range(3):
    print(f"attempt {i + 1}")
```

Iterate dict keys/items when you reach Module 5:

```python
# for name, ip in inventory.items():
#     ...
```

### while loops

Use for retries with a **hard cap**:

```python
attempts = 0
while attempts < 5:
    attempts += 1
    # try connect...
    break  # on success
else:
    # while-else: ran out without break
    raise SystemExit("error: retries exhausted")
```

Unbounded `while True` without a break condition hangs CI and cron jobs.

### break, continue, pass

| Keyword | Meaning |
|---------|---------|
| `break` | Leave the loop |
| `continue` | Skip to next iteration |
| `pass` | Empty body placeholder |

```python
for host in hosts:
    if host.startswith("lab-"):
        continue
    if host == "bastion":
        break
```

## Hands-on Lab

**Focus:** practise the core workflow for Control Flow — Conditionals and Loops

```bash
mkdir -p ~/rebash-python/module-03
cd ~/rebash-python/module-03

python3 -m venv .venv
source .venv/bin/activate
```

### Step 1 – Health triage script

```bash
cd ~/rebash-python/module-03
source .venv/bin/activate

cat > triage.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import sys

HOSTS = [
    ("web-a", "healthy"),
    ("web-b", "degraded"),
    ("web-c", "down"),
    ("lab-1", "healthy"),
]


def action_for(status: str) -> str:
    match status:
        case "healthy":
            return "noop"
        case "degraded":
            return "warn"
        case "down":
            return "page"
        case _:
            return "unknown"


def main() -> int:
    worst = 0
    for host, status in HOSTS:
        if host.startswith("lab-"):
            continue
        act = action_for(status)
        print(f"host={host} status={status} action={act}")
        if act == "page":
            worst = max(worst, 2)
        elif act == "warn":
            worst = max(worst, 1)
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python triage.py; echo "exit=$?"
```

### Step 2 – Retry with while

```bash
cat > retry_demo.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import sys


def main() -> int:
    target_success_on = 3
    attempt = 0
    while attempt < 5:
        attempt += 1
        print(f"attempt={attempt}", file=sys.stderr)
        if attempt == target_success_on:
            print("ok")
            return 0
    print("error: retries exhausted", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python retry_demo.py
```

### Step 3 – range inventory numbering

```bash
python - <<'PY'
for idx, name in enumerate(["db-a", "db-b"], start=1):
    print(f"{idx}. {name}")
PY
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-03/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Control Flow — Conditionals and Loops** always combines:

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

!!! warning "Skipping fundamentals for Control Flow — Conditionals and Loops"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Control Flow — Conditionals and Loops"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Control Flow — Conditionals and Loops changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Infinite loop | `while True` without break | Add max attempts |
| `SyntaxError` on match | Python &lt; 3.10 | Upgrade interpreter |
| Nested if soup | Too many branches | Use `match` or dict dispatch |

## Summary

- Branch with `if`/`match`; iterate with `for`; retry with capped `while`  
- `continue`/`break` keep inventory loops clear  
- Exit codes should reflect worst severity for CI

## Interview Questions

1. How does **Control Flow — Conditionals and Loops** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Functions — Parameters and Scope](functions-parameters-and-scope.md)  
- [Data Structures](data-structures-comprehensions-and-generators.md)

## References

- [Control flow tutorial](https://docs.python.org/3/tutorial/controlflow.html)  
- [match statement](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement)
