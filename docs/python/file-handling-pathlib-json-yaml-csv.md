---
title: "File Handling — pathlib, JSON, YAML, CSV"
description: "Read and write files safely with pathlib, JSON, YAML, CSV, XML basics, shutil, and temporary files for DevOps automation."
difficulty: intermediate
estimated_time: "50–65 min"
technology: python
category: python
module: "Module 7 · File Handling"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - pathlib
  - json
  - yaml
  - csv
prerequisites:
  - python/modules-packages-and-dependencies
next:
  - python/error-handling-and-exceptions
related:
  - python/configuration-management-and-secrets
  - labs/python-yaml-config-validator
  - labs/python-json-validator
labs:
  - labs/python-yaml-config-validator
  - labs/python-json-validator
  - labs/python-log-analyser
projects:
  - projects/python-log-analysis-tool
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - pathlib
  - json
  - yaml
  - csv
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# File Handling — pathlib, JSON, YAML, CSV

## Overview

Read and write ops artefacts safely with `pathlib`, parse JSON/YAML/CSV, and use temp files and `shutil` without path-injection surprises.

DevOps tools live on files: kubeconfigs, Terraform plans summaries, inventory CSV, Compose YAML, API JSON. Use **pathlib**, explicit encodings, and validate before acting.

Complete [Modules, Packages, and Dependencies](modules-packages-and-dependencies.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 7 · File Handling** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Modules, Packages, and Dependencies](modules-packages-and-dependencies.md)
- Project venv; `PyYAML` from Module 6 lab (or install below)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Build and join paths with `pathlib.Path`  
- [ ] Read/write text with encoding and context managers  
- [ ] Load and dump JSON and YAML  
- [ ] Read/write CSV reports  
- [ ] Use temp files and `shutil` for safe copy/move  
- [ ] State XML’s role (config/SOAP) without overusing it

## Architecture

This topic’s control points and relationships are shown below.

![File handling](../assets/excalidraw/python-file-handling.svg)

## Theory

### What it is

File handling is how automation reads and writes configuration and data on disk: paths via **pathlib**, structured formats (**JSON**, **YAML**, **CSV**, light **XML**), and temporary workspaces via **tempfile** / **shutil**. Almost every later module — kubeconfig-shaped JSON, inventory CSV, Helm values YAML — rests on these primitives.

### Why it matters

Wrong encoding corrupts non-ASCII hostnames. `yaml.load` without a safe loader can execute code. Path traversal (`../../etc/passwd`) turns a “read config” flag into a local file disclosure. Streaming and temp directories keep CI agents from filling disks. Solid file I/O is security and reliability, not just syntax.

### How it works

Join paths with pathlib’s `/` operator; check `exists()` / `is_file()` before assuming content. Open with context managers and `encoding="utf-8"` for text; use `"rb"`/`"wb"` for binaries. JSON via `json.loads` / `dumps`; YAML via **`yaml.safe_load`** only; CSV via `csv.DictReader` with `newline=""`. Prefer JSON/YAML for new tools; keep ElementTree for legacy XML. Copy with `shutil.copy2`; use `TemporaryDirectory` so leftovers disappear even on failure. When accepting user paths, resolve them and confine under an allowed root.

```python
from pathlib import Path
import yaml

cfg = Path.cwd() / "config" / "app.yaml"
doc = yaml.safe_load(cfg.read_text(encoding="utf-8"))
```

### Key concepts and comparisons

| Format | Library | Notes |
|--------|---------|--------|
| JSON | `json` | APIs, kube-shaped fixtures |
| YAML | PyYAML `safe_load` | Human configs; never unsafe load |
| CSV | `csv` | Inventories, exports |
| XML | ElementTree | Legacy only |

| Operation | Prefer |
|-----------|--------|
| Path join | `Path / "name"` |
| Temp work | `TemporaryDirectory` |
| Copy metadata | `shutil.copy2` |

### Common pitfalls

- String-concatenating paths and breaking on Windows or spaces.  
- `yaml.load` without `SafeLoader`.  
- Loading multi-gigabyte files into memory instead of streaming.  
- Leaving secrets in world-readable temp files.  
- Writing JSON without a trailing newline (noisy diffs) or with non-ASCII escaped unexpectedly.

## Hands-on Lab

**Focus:** practise the core workflow for File Handling — pathlib, JSON, YAML, CSV

```bash
mkdir -p ~/rebash-python/module-07
cd ~/rebash-python/module-07

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install 'PyYAML==6.0.2'
```

### Step 1 – Config round-trip (YAML + JSON)

```bash
cd ~/rebash-python/module-07
source .venv/bin/activate

mkdir -p config
cat > config/app.yaml << 'EOF'
env: lab
replicas: 2
regions:
  - eu-west-1
  - us-east-1
EOF

cat > convert_config.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


def main() -> int:
    src = Path("config/app.yaml")
    if not src.is_file():
        print(f"error: missing {src}", file=sys.stderr)
        return 1
    doc = yaml.safe_load(src.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        print("error: root must be a mapping", file=sys.stderr)
        return 1
    out = Path("config/app.json")
    out.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python convert_config.py
cat config/app.json
```

### Step 2 – CSV inventory report

```bash
cat > hosts.csv << 'EOF'
name,ip,role
web-a,10.0.1.10,web
web-b,10.0.1.11,web
db-a,10.0.1.20,db
EOF

python - <<'PY'
import csv
from pathlib import Path
web = []
with Path("hosts.csv").open(newline="", encoding="utf-8") as fh:
    for row in csv.DictReader(fh):
        if row["role"] == "web":
            web.append(row["name"])
print(",".join(web))
PY
```

### Step 3 – Safe copy into temp dir

```bash
python - <<'PY'
import shutil
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory(prefix="rebash-") as tmp:
    dst = Path(tmp) / "hosts.csv"
    shutil.copy2("hosts.csv", dst)
    print(dst.exists(), dst.read_text(encoding="utf-8").splitlines()[0])
print("temp cleaned")
PY
```

### Step 4 – Path validation habit

```bash
python - <<'PY'
from pathlib import Path

def under(root: Path, user_path: str) -> Path:
    target = (root / user_path).resolve()
    root = root.resolve()
    if not str(target).startswith(str(root) + "/") and target != root:
        raise ValueError("path escapes root")
    return target

root = Path("config").resolve()
print(under(root, "app.yaml"))
try:
    under(root, "../hosts.csv")
except ValueError as exc:
    print("blocked:", exc)
PY
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-07/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **File Handling — pathlib, JSON, YAML, CSV** always combines:

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

!!! warning "String-concatenating paths and breaking on Windows or spaces.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "`yaml.load` without `SafeLoader`.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode File Handling — pathlib, JSON, YAML, CSV changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `UnicodeDecodeError` | Wrong encoding | Force `utf-8`; fix source file |
| YAML arbitrary code | Used unsafe loader | `yaml.safe_load` only |
| `FileNotFoundError` | Wrong cwd | Use paths relative to script/`Path.cwd()` clearly |

## Summary

- `pathlib` + UTF-8 + context managers  
- JSON/YAML/CSV are the ops file trio  
- `safe_load` for YAML; validate paths under a root  
- Temp dirs for scratch; `shutil` for copy/move

## Interview Questions

1. How does **File Handling — pathlib, JSON, YAML, CSV** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Error Handling and Exceptions](error-handling-and-exceptions.md)  
- [YAML Validator lab](../labs/python-yaml-config-validator.md)  
- [JSON Validator lab](../labs/python-json-validator.md)

## References

- [pathlib](https://docs.python.org/3/library/pathlib.html)  
- [json](https://docs.python.org/3/library/json.html)  
- [PyYAML](https://yaml.readthedocs.io/)  
- [csv](https://docs.python.org/3/library/csv.html)
