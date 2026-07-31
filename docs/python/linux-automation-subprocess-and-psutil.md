---
title: "Linux Automation — subprocess and psutil"
description: "Automate Linux with subprocess, os, pathlib, shutil, signals, and psutil — safe process management and permissions for DevOps Python."
difficulty: intermediate
estimated_time: "50–65 min"
technology: python
category: python
module: "Module 13 · Linux Automation"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - linux-administrator
  - site-reliability-engineer
  - platform-engineer
skills:
  - python
  - subprocess
  - psutil
  - linux-automation
prerequisites:
  - python/cli-applications-argparse-click-typer
next:
  - python/rest-apis-requests-auth-and-resilience
related:
  - linux/linux-networking-tools
  - labs/python-linux-health-checker
labs:
  - labs/python-linux-health-checker
projects: []
interview: interview/python
certifications:
  - RHCSA
  - PCAP
tags:
  - python
  - subprocess
  - psutil
  - linux
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Linux Automation — subprocess and psutil

## Overview

Run host commands safely with `subprocess` (no `shell=True` on the happy path), inspect processes with `psutil`, and combine pathlib/shutil for file automation.

Python orchestrates Linux: package checks, disk thresholds, service restarts (carefully), and wrapping CLIs. Prefer list args, timeouts, and captured output.

Complete [CLI Applications](cli-applications-argparse-click-typer.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 13 · Linux Automation** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [CLI Applications](cli-applications-argparse-click-typer.md)
- Linux lab host with Python 3.12+

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Call `subprocess.run` with list args and timeout  
- [ ] Handle non-zero return codes explicitly  
- [ ] Use pathlib/shutil for file ops  
- [ ] Inspect CPU/memory/process lists with psutil  
- [ ] Avoid `shell=True` unless strictly justified  
- [ ] Note signal handling for graceful shutdown

## Architecture

This topic’s control points and relationships are shown below.

![Linux automation](../assets/excalidraw/python-linux-automation.svg)

## Theory

### What it is

Linux automation in Python means driving the host safely: run commands via **`subprocess`**, inspect the process and environment with **`os`** / **pathlib** / **shutil**, sample resources with **`psutil`**, and shut down cleanly on **signals**. You are not rewriting systemd — you are wrapping the same tools operators already trust, with timeouts and structured exit handling.

### Why it matters

Cloud SDKs do not replace “is nginx active?”, disk pressure, or collecting `uname` across bastions. Shell scripts grow fragile; Python wrappers add parsing, retries, and tests. Done badly (`shell=True`, no timeout, assume root), they become injection bugs and hung Continuous Integration (CI) jobs. Done well, they are the backbone of agentless host checks.

### How it works

Pass **argument lists** to `subprocess.run` — never build a shell string from untrusted input. Always set **`timeout`**. Use `capture_output=True` and `text=True` when you need to parse stdout. `check=True` raises on non-zero when failure is exceptional; otherwise inspect `returncode`. Read `os.environ` and `os.getuid()` for context; use pathlib for paths and shutil for copy/move/`disk_usage`. **psutil** samples CPU, memory, and disk without scraping `/proc` by hand. Register short handlers for `SIGINT`/`SIGTERM` to flush and clean temp files. Do not assume root — check access and fail with a clear message.

```python
import subprocess
r = subprocess.run(
    ["uname", "-a"],
    check=False,
    capture_output=True,
    text=True,
    timeout=10,
)
```

### Key concepts and comparisons

| Tool | Job |
|------|-----|
| subprocess | Run CLIs with timeout and captured output |
| pathlib / shutil | Paths, copy, disk usage |
| psutil | CPU, memory, process tables |
| Signals | Cooperative shutdown |

| Practice | Prefer | Avoid |
|----------|--------|--------|
| Invocation | Argv list | `shell=True` + user input |
| Permissions | Fail closed | `chmod 0777` |
| Long jobs | SIGTERM handler | Ignore signals |

### Common pitfalls

- Omitting `timeout` on mounts or remote CLIs.  
- Parsing locale-dependent human output instead of machine flags.  
- Running as root “to make CI green.”  
- Heavy work inside signal handlers.  
- Treating `returncode == 0` as “healthy” when stdout says degraded.

## Hands-on Lab

**Focus:** practise the core workflow for Linux Automation — subprocess and psutil

```bash
mkdir -p ~/rebash-python/module-13
cd ~/rebash-python/module-13

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install 'psutil==6.1.1'
```

### Step 1 – Safe command wrapper

```bash
cd ~/rebash-python/module-13
source .venv/bin/activate

cat > run_cmd.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys


def run(cmd: list[str], timeout: float = 15) -> int:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"error: timeout running {cmd!r}", file=sys.stderr)
        return 124
    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    return proc.returncode


def main() -> int:
    return run(["uname", "-s"])


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python run_cmd.py
```

### Step 2 – Health snapshot with psutil

```bash
cat > health.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys

import psutil


def main() -> int:
    cpu = psutil.cpu_percent(interval=0.2)
    mem = psutil.virtual_memory().percent
    disk = shutil.disk_usage("/").used / shutil.disk_usage("/").total * 100
    print(f"cpu_percent={cpu:.1f}")
    print(f"mem_percent={mem:.1f}")
    print(f"disk_percent={disk:.1f}")
    # exit 1 if any over lab thresholds
    if cpu > 95 or mem > 95 or disk > 95:
        print("error: threshold exceeded", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python health.py
```

### Step 3 – Anti-pattern reminder

```bash
python - <<'PY'
# Never do this with untrusted input:
# subprocess.run(f"echo {user}", shell=True)
print("use list args: subprocess.run(['echo', user])")
PY
```

### Step 4 – Process list peek

```bash
python - <<'PY'
import psutil
for p in psutil.process_iter(["pid", "name"]):
    if p.info["name"] and "python" in p.info["name"]:
        print(p.info)
        break
PY
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-13/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Linux Automation — subprocess and psutil** always combines:

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

!!! warning "Omitting `timeout` on mounts or remote CLIs.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Parsing locale-dependent human output instead of machine flags.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Linux Automation — subprocess and psutil changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `FileNotFoundError` | Binary not on PATH | Full path or document dependency |
| Hang | Missing timeout | Always set timeout |
| Permission denied | Non-root | Drop privilege needs; clearer errors |

## Summary

- `subprocess` with lists + timeouts  
- psutil for host signals in health checks  
- pathlib/shutil for files; no casual `shell=True`  
- Pair with the [Linux Health Checker](../labs/python-linux-health-checker.md) lab

## Interview Questions

1. How does **Linux Automation — subprocess and psutil** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [REST APIs — requests, Auth, and Resilience](rest-apis-requests-auth-and-resilience.md)  
- [Linux Health Checker lab](../labs/python-linux-health-checker.md)

## References

- [subprocess](https://docs.python.org/3/library/subprocess.html)  
- [psutil](https://psutil.readthedocs.io/)
