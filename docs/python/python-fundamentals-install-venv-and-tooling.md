---
title: "Python Fundamentals — Install, venv, and Tooling"
description: "What Python is for DevOps, install and version pinning, IDE setup, virtual environments, and package tools pip, uv, and Poetry."
difficulty: beginner
estimated_time: "50–65 min"
technology: python
category: python
module: "Module 1 · Fundamentals"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - venv
  - pip
  - uv
prerequisites:
  - linux/index
  - shell/index
next:
  - python/python-basics-types-and-io
related:
  - shell/index
  - linux/index
labs: []
projects: []
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - fundamentals
  - venv
  - uv
  - poetry
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Python Fundamentals — Install, venv, and Tooling

## Overview

Install a supported Python, create an isolated project virtual environment, fingerprint the interpreter, and choose between pip, uv, and Poetry for reproducible DevOps tooling.

This course is **Python for DevOps Engineers** — not a general programming degree. You will automate Linux, APIs, cloud, containers, Kubernetes, Terraform, and CI/CD. Module 1 builds the baseline every later lab assumes: a known interpreter, a project **venv**, and pinned dependencies.

This is a core tutorial in **Module 1 · Fundamentals** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Linux Fundamentals](../linux/index.md)
- [Shell Scripting](../shell/index.md)
- A Linux host, WSL2, or cloud VM where you can install packages

### Recommended

- Editor: VS Code or PyCharm
- Optional: [uv](https://github.com/astral-sh/uv) installed for faster installs

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain why DevOps uses Python alongside Bash  
- [ ] Verify Python **3.12+** (academy default **3.13** when available)  
- [ ] Create and activate a project `.venv`  
- [ ] Install packages with `python -m pip` and pin them  
- [ ] Contrast pip, uv, and Poetry for ops repos  
- [ ] Point VS Code / PyCharm at the project interpreter

## Architecture

Source runs through the interpreter into runtime packages, then reaches files, APIs, and CLIs.

Project tools must live in an isolated venv, not the system site-packages.

![Python execution flow](../assets/excalidraw/python-execution-flow.svg)

## Theory

### What is Python (for this course)?

**Python** is a high-level language with a large standard library and SDKs for cloud, Kubernetes, Docker, and HTTP. Bash launches and glues; Python owns structured data (JSON/YAML), APIs, tests, and packaged CLIs.

### Versions

| Target | Notes |
|--------|--------|
| Course minimum | 3.12+ |
| Academy default | 3.13 when the image provides it |
| Avoid | Python 2; unpinned “whatever is on the box” |

Set `requires-python` in `pyproject.toml` later so CI fails early on the wrong interpreter.

### Interpreter habits

Prefer:

```bash
python3 -m venv .venv
python3 -m pip --version
```

Shebang for scripts: `#!/usr/bin/env python3` so `PATH` selects the intended binary after activation.

### IDE setup

**VS Code:** Python extension → select `.venv/bin/python` → format on save (Ruff or Black) → open the lab folder as the workspace root.

**PyCharm:** Project at the lab directory → Virtualenv interpreter from `.venv` → mark `src` as Sources Root when you adopt a package layout.

### Virtual environments

A **venv** isolates project packages from the system:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
which python
```

Commit lock/requirements files; **never** commit `.venv`.

### pip

```bash
python -m pip install 'packaging==24.2'
python -m pip freeze > requirements.txt
```

Always `python -m pip` so you do not hit a mismatched `pip` on `PATH`.

### uv

Fast installer/resolver — excellent in CI:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Keep the same pins as teammates whether you use pip or uv.

### Poetry

Poetry manages `pyproject.toml`, venvs, and lockfiles together. Fine for published internal CLIs. **This course defaults to `venv` + pinned `requirements.txt`** unless a later module says otherwise. Pick **one** tool per repo and document it.

## Hands-on Lab

**Focus:** practise the core workflow for Python Fundamentals — Install, venv, and Tooling

```bash
mkdir -p ~/rebash-python/module-01
cd ~/rebash-python/module-01

python3 --version
command -v python3
```

You need **Python 3.12 or newer**. If the host is older, install via your distro’s supported method (or `pyenv` / deadsnakes) — never overwrite the OS interpreter that package managers depend on.

### Step 1 – Workspace and fingerprint

```bash
cd ~/rebash-python/module-01

python3 - <<'PY'
import platform, sys
print(f"executable={sys.executable}")
print(f"version={platform.python_version()}")
print(f"prefix={sys.prefix}")
assert sys.version_info >= (3, 12), "Need Python 3.12+"
print("OK")
PY
```

### Step 2 – Create and activate a venv

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python - <<'PY'
import sys
assert ".venv" in sys.prefix or "venv" in sys.prefix.lower()
print("venv OK:", sys.executable)
PY
```

### Step 3 – Pin a package

```bash
python -m pip install 'packaging==24.2'
python -m pip freeze | tee requirements.txt
python -c "import packaging; print(packaging.__version__)"
```

### Step 4 – Optional uv compare

```bash
command -v uv >/dev/null && uv --version || echo "uv optional — skip"
# If uv exists:
# uv pip install 'httpx==0.28.1'
```

### Step 5 – Tiny entry point

```bash
cat > fingerprint.py << 'EOF'
#!/usr/bin/env python3
"""Print interpreter facts for CI fingerprinting."""
from __future__ import annotations

import platform
import sys


def main() -> int:
    print(f"executable={sys.executable}", file=sys.stderr)
    print(platform.python_version())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
EOF
chmod +x fingerprint.py
python fingerprint.py
```

### Step 6 – Deactivate awareness

```bash
deactivate
command -v python
source .venv/bin/activate
command -v python
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-01/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Python Fundamentals — Install, venv, and Tooling** always combines:

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

!!! warning "Skipping fundamentals for Python Fundamentals — Install, venv, and Tooling"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Python Fundamentals — Install, venv, and Too"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Python Fundamentals — Install, venv, and Tooling changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `python` not found | Only `python3` on PATH | Use `python3` or activate venv |
| `ModuleNotFoundError` after install | Wrong env / not activated | `which python`; recreate `.venv` |
| Permission errors on install | Installing into system Python | Always use a venv |
| CI differs from laptop | Different minor version | Pin image Python; fingerprint in the job |

## Summary

- Python is the structured automation layer for DevOps  
- Isolate with **venv**; pin with **pip** (or uv/Poetry consistently)  
- Fingerprint the interpreter in CI  
- Next: types and I/O for safe ops scripts

## Interview Questions

1. How does **Python Fundamentals — Install, venv, and Tooling** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Python Basics — Types and I/O](python-basics-types-and-io.md)  
- [Shell Scripting](../shell/index.md)  
- [Python interview prep](../interview/python.md)

## References

- [Python 3 documentation](https://docs.python.org/3/)  
- [venv](https://docs.python.org/3/library/venv.html)  
- [uv](https://docs.astral.sh/uv/)  
- [Poetry](https://python-poetry.org/docs/)
