---
title: "Lab — Python JSON Validator"
description: "Validate infrastructure JSON documents against required keys and types with CI-friendly exit codes."
difficulty: beginner
estimated_time: "35–45 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - python
  - json
  - validation
  - cli
comments: false
---

# Lab — Python JSON Validator

## Lab Overview

**Purpose:** Validate JSON config/payloads used by automation without calling external APIs.

**Scenario:** A webhook payload and a `service.json` manifest must pass schema checks before a pipeline continues.

**Expected outcome:** CLI exits `0` on valid JSON matching rules, `2` on parse or schema failure.

!!! tip "This is a lab, not a tutorial"
    Apply [File Handling — pathlib, JSON, YAML, CSV](../python/file-handling-pathlib-json-yaml-csv.md).

## Business Scenario

CI receives `service.json`:

```json
{"name": "checkout", "port": 8080, "replicas": 2}
```

Rules: `name` non-empty string, `port` int 1–65535, `replicas` int ≥ 1.

## Learning Objectives

- [ ] Parse JSON with `json.load` / `json.loads` and handle `JSONDecodeError`
- [ ] Validate types and ranges defensively
- [ ] Use pathlib for file I/O
- [ ] Exit `0` / `2` consistently with YAML lab conventions

## Prerequisites

### Knowledge

- [File Handling — pathlib, JSON, YAML, CSV](../python/file-handling-pathlib-json-yaml-csv.md)
- [Error Handling and Exceptions](../python/error-handling-and-exceptions.md)
- [CLI Applications — argparse, Click, Typer](../python/cli-applications-argparse-click-typer.md)

### Software

Python 3.12+ (stdlib `json` only). **Estimated cost:** £0.

## Environment

```bash
mkdir -p ~/rebash-lab-python-json/{ok,bad}
cd ~/rebash-lab-python-json
python3 -m venv .venv && source .venv/bin/activate
```

## Initial State

Create `ok/service.json`:

```json
{"name": "checkout", "port": 8080, "replicas": 2}
```

Create `bad/service.json`:

```json
{"name": "", "port": 99999, "replicas": 0}
```

Prepare remaining files:

```bash
echo 'not-json' > bad/broken.json
```

## Task

Create `validate_json.py` with positional path(s). Load JSON, collect all schema errors, print to stderr, exit `2` on any failure.

## Validation

```bash
python validate_json.py ok/service.json; echo $?      # 0
python validate_json.py bad/service.json; echo $?     # 2
python validate_json.py bad/broken.json; echo $?      # 2
```

- [ ] Valid exits `0`
- [ ] Schema and parse failures exit `2`
- [ ] Multiple errors reported when possible

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `True` accepted as int | Reject `bool` explicitly (`isinstance(x, bool)`) |
| Unicode errors | Open with `encoding="utf-8"` |

## Cleanup

```bash
deactivate 2>/dev/null || true
rm -rf ~/rebash-lab-python-json
```

## Production Discussion

For evolving contracts, prefer JSON Schema (Draft 2020-12) or Pydantic models shared between producers and consumers.

## Related

- Previous: [YAML Config Validator](python-yaml-config-validator.md)
- Next: [GitHub Repository Auditor](python-github-repository-auditor.md)
