---
title: "Lab — Python YAML Config Validator"
description: "Build a YAML validator CLI that exits 0 on valid deploy config and 2 on invalid or missing input — with schema checks."
difficulty: beginner
estimated_time: "40–45 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - python
  - yaml
  - cli
  - validation
comments: false
---

# Lab — Python YAML Config Validator

## Lab Overview

**Purpose:** Load infrastructure YAML safely and return automation-friendly exit codes.

**Scenario:** A PR adds `deploy.yaml`. CI should fail fast if the file is missing keys or is not valid YAML, without applying anything.

**Expected outcome:** A CLI that validates one or more YAML files and exits **0** (ok) or **2** (usage / invalid).

!!! tip "This is a lab, not a tutorial"
    Apply [File Handling — pathlib, JSON, YAML, CSV](../python/file-handling-pathlib-json-yaml-csv.md) and [Error Handling and Exceptions](../python/error-handling-and-exceptions.md).

## Business Scenario

Platform requires every service repo to ship `deploy.yaml` with at least `name` (non-empty string) and `replicas` (integer ≥ 1). Your job is a local validator teammates can run before push — and CI can run without kubectl.

## Learning Objectives

- [ ] Install PyYAML in a venv and pin a version
- [ ] Use `yaml.safe_load` (never unsafe `load`)
- [ ] Validate required keys and types
- [ ] Map validation failures to exit code **2**
- [ ] Print human errors on stderr

## Prerequisites

### Knowledge

- [File Handling — pathlib, JSON, YAML, CSV](../python/file-handling-pathlib-json-yaml-csv.md)
- [Error Handling and Exceptions](../python/error-handling-and-exceptions.md)
- [CLI Applications — argparse, Click, Typer](../python/cli-applications-argparse-click-typer.md)
- [Configuration Management and Secrets](../python/configuration-management-and-secrets.md)

### Software

| Tool | Notes |
|------|--------|
| Python 3.12+ | `python3 --version` |
| PyYAML | pin e.g. `PyYAML>=6.0,<7` |

**Estimated cost:** £0.

## Architecture

```text
deploy.yaml  -->  safe_load  -->  schema checks  -->  exit 0 | 2
                      |
                 stderr messages
```

## Environment

```bash
mkdir -p ~/rebash-lab-python/configs
cd ~/rebash-lab-python
python3 -m venv .venv
source .venv/bin/activate
pip install 'PyYAML>=6.0,<7'
```

## Initial State

Create `configs/deploy-ok.yaml`:

```yaml
name: payments-api
replicas: 2
```

Create `configs/deploy-bad.yaml`:

```yaml
name: payments-api
replicas: zero
```

Create `configs/not-yaml.yaml`:

```yaml
::: this is not yaml
```

## Task

### Step 1 – Validator skeleton

Create `validate_config.py`:

- argparse: positional `path` (file)
- `sys.exit(0)` on success
- `sys.exit(2)` on any validation failure

### Step 2 – Load safely

```python
from pathlib import Path
import yaml

text = Path(path).read_text(encoding="utf-8")
data = yaml.safe_load(text)
```

Treat `None` / non-dict roots as invalid.

### Step 3 – Schema checks

Require:

- `name`: `str`, stripped length ≥ 1
- `replicas`: `int`, ≥ 1

Collect all errors (do not stop at the first) and print each on stderr.

### Step 4 – Multi-file mode (stretch)

Accept multiple paths; exit `2` if any file fails.

## Validation

```bash
python validate_config.py configs/deploy-ok.yaml; echo $?   # 0
python validate_config.py configs/deploy-bad.yaml; echo $?  # 2
python validate_config.py configs/not-yaml.yaml; echo $?    # 2
python validate_config.py missing.yaml; echo $?             # 2
```

- [ ] Valid file exits `0`
- [ ] Bad replicas / broken YAML / missing file exit `2`
- [ ] Errors go to stderr; success may be silent or one line on stdout
- [ ] Code uses `safe_load` only

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `YAMLLoadWarning` | You used unsafe `load` — switch to `safe_load` |
| `replicas: "2"` passes | Coerce or reject strings; require `isinstance(..., int)` and not `bool` |
| Relative path fails | Resolve with `Path(path).expanduser().resolve()` |

## Cleanup

```bash
deactivate 2>/dev/null || true
# keep shared ~/rebash-lab-python if used by other labs, or:
rm -rf ~/rebash-lab-python
```

## Production Discussion

Prefer JSON Schema or a typed model (Pydantic) for larger contracts. Keep validators pure (no cluster calls) so CI stays fast and credential-free.

## Stretch Goals

- Validate optional `image` matches `repo:tag`
- Add `--strict` to forbid unknown keys
- Return a JSON report for CI annotations

## Related

- Track: [Python for DevOps](../python/index.md)
- Previous: [Python Linux Health Checker](python-linux-health-checker.md)
- Next: [Python JSON Validator](python-json-validator.md)
- Cheat sheet: [Python](../cheatsheets/python.md)
