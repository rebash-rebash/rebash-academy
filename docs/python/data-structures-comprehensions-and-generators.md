---
title: "Data Structures — Comprehensions and Generators"
description: "Lists, tuples, dictionaries, sets, comprehensions, iterators, and generators for inventory and log processing in DevOps automation."
difficulty: intermediate
estimated_time: "50–65 min"
technology: python
category: python
module: "Module 5 · Data Structures"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - lists
  - dicts
  - generators
prerequisites:
  - python/functions-parameters-and-scope
next:
  - python/modules-packages-and-dependencies
related:
  - python/file-handling-pathlib-json-yaml-csv
  - python/linux-automation-subprocess-and-psutil
labs:
  - labs/python-log-analyser
projects: []
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - lists
  - dicts
  - generators
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Data Structures — Comprehensions and Generators

## Overview

Choose the right collection for inventories and labels, transform data with comprehensions, and stream large logs with generators without loading everything into memory.

Hosts, labels, and log lines are collections. Wrong structure (list vs set vs dict) causes slow lookups and duplicate chaos; loading a 2 GB log into a list OOMs a runner.

Complete [Functions](functions-parameters-and-scope.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 5 · Data Structures** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Functions — Parameters and Scope](functions-parameters-and-scope.md)
- Project venv with Python 3.12+

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Use list, tuple, dict, and set for typical ops data  
- [ ] Write list and dict comprehensions clearly  
- [ ] Explain iterators vs materialised lists  
- [ ] Write a generator that streams lines  
- [ ] Deduplicate and look up inventory efficiently

## Architecture

This topic’s control points and relationships are shown below.

![Data structures](../assets/excalidraw/python-data-structures.svg)

## Theory

### Lists

Ordered, mutable — host lists, CLI argv copies:

```python
hosts = ["web-a", "web-b"]
hosts.append("web-c")
```

### Tuples

Ordered, immutable — fixed records, dict keys:

```python
endpoint = ("api.internal", 443)
```

### Dictionaries

Key → value — inventory, labels, config maps:

```python
inventory = {"web-a": "10.0.1.10", "web-b": "10.0.1.11"}
inventory.get("web-z", "MISSING")
```

### Sets

Unique membership — dedupe tags, fast “is this allowed?”:

```python
regions = {"eu-west-1", "us-east-1"}
"eu-west-1" in regions  # O(1) average
```

### Choosing

| Need | Structure |
|------|-----------|
| Ordered sequence | `list` |
| Fixed record | `tuple` |
| Lookup by name/id | `dict` |
| Unique membership | `set` |

### Comprehensions

```python
ips = [ip for host, ip in inventory.items() if host.startswith("web-")]
by_region = {h: "eu-west-1" for h in hosts}
```

Keep them readable — if you need comments, use a normal loop.

### Iterators and generators

Anything you `for` over is iterable. A **generator** yields values lazily:

```python
def matching_lines(path: str, needle: str):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if needle in line:
                yield line.rstrip("\n")
```

Use generators for large files; use lists when you need len/shuffle/reuse.

## Hands-on Lab

**Focus:** practise the core workflow for Data Structures — Comprehensions and Generators

```bash
mkdir -p ~/rebash-python/module-05
cd ~/rebash-python/module-05

python3 -m venv .venv
source .venv/bin/activate
```

### Step 1 – Inventory dict and set dedupe

```bash
cd ~/rebash-python/module-05
source .venv/bin/activate

python - <<'PY'
raw = ["web-a", "web-b", "web-a", "db-a"]
unique = sorted(set(raw))
inv = {name: f"10.0.1.{i+10}" for i, name in enumerate(unique)}
print(inv)
print("web-a" in inv)
PY
```

### Step 2 – Comprehension filter

```bash
python - <<'PY'
services = [
    {"name": "api", "replicas": 3},
    {"name": "worker", "replicas": 0},
    {"name": "web", "replicas": 2},
]
live = [s["name"] for s in services if s["replicas"] > 0]
print(live)
PY
```

### Step 3 – Generator over a sample log

```bash
printf '%s\n' 'INFO start' 'ERROR timeout' 'INFO ok' 'ERROR 502' > sample.log

cat > scan_log.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections.abc import Iterator
from pathlib import Path


def error_lines(path: Path) -> Iterator[str]:
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            if "ERROR" in line:
                yield line.rstrip("\n")


def main() -> int:
    path = Path("sample.log")
    count = 0
    for line in error_lines(path):
        print(line)
        count += 1
    print(f"errors={count}", file=sys.stderr)
    return 0 if count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python scan_log.py; echo exit=$?
```

### Step 4 – dict lookup vs list scan

```bash
python - <<'PY'
hosts = [f"host-{i}" for i in range(5000)]
as_set = set(hosts)
needle = "host-4200"
print(needle in hosts)   # scans list
print(needle in as_set)  # hash lookup
PY
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-05/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Data Structures — Comprehensions and Generators** always combines:

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

!!! warning "Skipping fundamentals for Data Structures — Comprehensions and Generators"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Data Structures — Comprehensions and Generat"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Data Structures — Comprehensions and Generators changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `KeyError` | Missing dict key | `.get()` or validate |
| Memory blow-up | `readlines()` on huge file | Iterate file / yield |
| Unreadable comprehension | Too much logic | Use a for-loop |

## Summary

- Match structure to access pattern  
- Comprehensions for clear transforms  
- Generators for large streams  
- Sets/dicts for fast membership and lookup

## Interview Questions

1. How does **Data Structures — Comprehensions and Generators** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Modules, Packages, and Dependencies](modules-packages-and-dependencies.md)  
- [Log Analyser lab](../labs/python-log-analyser.md)

## References

- [Data structures tutorial](https://docs.python.org/3/tutorial/datastructures.html)  
- [Generators](https://docs.python.org/3/howto/functional.html#generators)
