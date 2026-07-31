---
title: "Testing with pytest"
description: "Test DevOps Python with pytest — fixtures, mocking, coverage, unittest interop, and integration-test patterns for CLIs and APIs."
difficulty: intermediate
estimated_time: "50–65 min"
technology: python
category: python
module: "Module 22 · Testing"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - pytest
  - mocking
  - testing
prerequisites:
  - python/concurrency-threads-asyncio-and-futures
next:
  - python/packaging-pyproject-and-wheels
related:
  - python/cli-applications-argparse-click-typer
  - python/error-handling-and-exceptions
labs: []
projects: []
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - pytest
  - testing
  - mocking
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Testing with pytest

## Overview

Write pytest unit tests with fixtures and mocks so ops CLIs stay reliable in CI without live cloud/Kubernetes credentials.

Untested automation breaks on Fridays. Prefer **pytest** for new work; keep `unittest` interop when needed. Mock SDKs; use fixtures for files and env.

Diagrams use Excalidraw only.

This is a core tutorial in **Module 22 · Testing** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Functions](functions-parameters-and-scope.md) and [Error Handling](error-handling-and-exceptions.md)
- Project venv

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Write pytest functions and assertions  
- [ ] Use fixtures for temp paths and sample data  
- [ ] Mock HTTP/SDK calls  
- [ ] Run coverage reports  
- [ ] Separate unit vs integration tests  
- [ ] Map unittest-style tests into pytest

## Architecture

This topic’s control points and relationships are shown below.

![pytest testing](../assets/excalidraw/python-pytest-testing.svg)

## Theory

### What it is

**pytest** is the dominant Python test runner for libraries and automation. You write functions named `test_*`, use plain `assert`, and share setup via **fixtures**. For DevOps code, tests prove parsers, exit codes, and “given this API JSON, we classify healthy” — without needing a live cluster on every commit.

### Why it matters

Automation without tests is tribal knowledge. A one-line change to severity mapping can open a Sev-1 alert path or hide outages. Unit tests with mocked HTTP/cloud clients run in seconds on every pull request. Integration tests (Docker, kind) run in dedicated jobs. Coverage reports show which branches of CLI exit codes you never exercised — the ones that fail at 02:00.

### How it works

pytest collects tests from files matching `test_*.py`. Fixtures inject temporary paths (`tmp_path`), sample configs, or fake clients. `monkeypatch` / `unittest.mock.patch` replace `requests.get` or boto3 so tests return fixture JSON and assert call arguments. Markers such as `@pytest.mark.integration` skip unless `RUN_INTEGRATION=1`. Coverage (`pytest --cov`) should focus on parsers and failure paths, not chasing 100% for theatre. pytest can still collect `unittest.TestCase` classes; prefer plain functions for new code.

```python
def test_add() -> None:
    assert add(2, 3) == 5

@pytest.fixture
def sample_json(tmp_path: Path) -> Path:
    p = tmp_path / "cfg.json"
    p.write_text('{"replicas": 2}\n', encoding="utf-8")
    return p
```

### Key concepts and comparisons

| Layer | Talks to | When |
|-------|----------|------|
| Unit | Mocks / fixtures | Every PR |
| Integration | Real Docker / kind / API sandbox | Nightly or labelled jobs |
| End-to-end | Full stack | Sparse; expensive |

| Tool | Role |
|------|------|
| Fixtures | Reusable setup/teardown |
| monkeypatch / mock | Fake I/O and SDKs |
| Markers | Opt-in slow tests |
| Coverage | Find untested exit branches |

### Common pitfalls

- Hitting real cloud APIs in unit tests (flaky, costly, credential-dependent).  
- Asserting exact log strings that change every refactor.  
- Skipping tests for “the hard error paths” that matter most.  
- Sharing mutable global state between tests.  
- Requiring network for collection time (imports that call home).

## Hands-on Lab

**Focus:** practise the core workflow for Testing with pytest

```bash
mkdir -p ~/rebash-python/module-22
cd ~/rebash-python/module-22

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install 'pytest==8.3.4' 'pytest-cov==6.0.0'
```

### Step 1 – Package under test

```bash
cd ~/rebash-python/module-22
source .venv/bin/activate

mkdir -p healthlib tests
cat > healthlib/__init__.py << 'EOF'
from __future__ import annotations

def severity(status: str) -> int:
    ranks = {"healthy": 0, "degraded": 1, "down": 2}
    if status not in ranks:
        raise ValueError(status)
    return ranks[status]


def worst(statuses: list[str]) -> int:
    return max((severity(s) for s in statuses), default=0)
EOF

export PYTHONPATH=.
```

### Step 2 – Unit tests

```bash
cat > tests/test_severity.py << 'EOF'
import pytest

from healthlib import severity, worst


def test_severity_ok() -> None:
    assert severity("healthy") == 0


def test_severity_bad() -> None:
    with pytest.raises(ValueError):
        severity("nope")


def test_worst() -> None:
    assert worst(["healthy", "down"]) == 2


def test_tmp_fixture(tmp_path) -> None:
    p = tmp_path / "a.txt"
    p.write_text("x", encoding="utf-8")
    assert p.read_text(encoding="utf-8") == "x"
EOF

pytest -q
```

### Step 3 – Mock HTTP

```bash
cat > tests/test_http.py << 'EOF'
from unittest.mock import Mock, patch

import requests


def fetch_status(url: str) -> int:
    r = requests.get(url, timeout=5)
    return r.status_code


@patch("requests.get")
def test_fetch_status(mock_get: Mock) -> None:
    mock_get.return_value = Mock(status_code=200)
    assert fetch_status("https://example.invalid") == 200
    mock_get.assert_called_once()
EOF

pytest -q tests/test_http.py
```

### Step 4 – Coverage

```bash
pytest --cov=healthlib --cov-report=term-missing
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-22/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Testing with pytest** always combines:

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

!!! warning "Hitting real cloud APIs in unit tests (flaky, costly, credential-dependent).  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Asserting exact log strings that change every refactor.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Testing with pytest changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Import errors | PYTHONPATH / package layout | Install editable or set path |
| Tests hit network | Forgot mock | Patch where used |
| Flaky integration | Shared cluster state | Isolate namespaces; mark/skip |

## Summary

- pytest + fixtures + mocks for ops CLIs  
- Coverage on critical branches  
- Integration tests optional and gated  
- CI should run unit tests on every PR

## Interview Questions

1. How does **Testing with pytest** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Packaging — pyproject.toml and Wheels](packaging-pyproject-and-wheels.md)

## References

- [pytest](https://docs.pytest.org/)  
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
