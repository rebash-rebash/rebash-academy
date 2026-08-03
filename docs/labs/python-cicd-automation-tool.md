---
title: "Lab — Python CI/CD Automation Tool"
description: "Build a small CI orchestrator CLI that runs lint/test steps from YAML, captures exit codes, and writes a JUnit-like summary — no cloud runners required."
difficulty: advanced
estimated_time: "55–70 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - python
  - cicd
  - pytest
  - automation
comments: false
---

# Lab — Python CI/CD Automation Tool

## Lab Overview

**Purpose:** Model a minimal local CI runner that executes defined steps and aggregates results.

**Scenario:** Before wiring GitHub Actions, the team wants a laptop-friendly `cicd-run` that mirrors pipeline steps for debugging.

**Expected outcome:** CLI reads `pipeline.yaml`, runs steps via subprocess, writes `out/report.json`, exits non-zero if any required step fails.

!!! tip "This is a lab, not a tutorial"
    Apply [Git Automation](../python/git-automation-github-and-gitlab.md), [Testing with pytest](../python/testing-with-pytest.md), and [Production Engineering Patterns](../python/production-engineering-patterns.md).

## Business Scenario

Flaky CI is hard to reproduce. Developers need the same step list locally with clear logs and artefacts.

## Learning Objectives

- [ ] Parse pipeline YAML (stages/steps)
- [ ] Run commands with list argv / `shlex` carefully
- [ ] Capture stdout/stderr to files
- [ ] Fail-fast vs continue flags
- [ ] Summarise for humans and machines

## Prerequisites

### Knowledge

- [Testing with pytest](../python/testing-with-pytest.md)
- [Packaging — pyproject and wheels](../python/packaging-pyproject-and-wheels.md)
- [Troubleshooting Python Automation](../python/troubleshooting-python-automation.md)

### Software

Python 3.12+, PyYAML. **Estimated cost:** £0.

## Environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-lab-python-cicd/{steps,out}
cd ~/rebash-lab-python-cicd
python3 -m venv .venv && source .venv/bin/activate
pip install 'PyYAML>=6.0,<7' pytest
```

## Initial State

Create `pipeline.yaml`:

```yaml title="pipeline.yaml"
name: local-ci
fail_fast: true
steps:
  - name: unit-tests
    run: ["pytest", "-q"]
  - name: version-check
    run: ["python", "-c", "import sys; assert sys.version_info >= (3, 10)"]
```

Create `tests/test_sanity.py`:

```python title="test_sanity.py"
def test_ok():
    assert 1 + 1 == 2
```

Prepare remaining files:

``` {.bash .ra-terminal title="Terminal"}
mkdir -p tests
```

## Task

Create `cicd_run.py --config pipeline.yaml`:

- Execute each step’s `run` list with `subprocess.run`
- On failure with `fail_fast`, stop and exit `1`
- Write `out/report.json` with per-step return codes and durations
- Support `--dry-run` to print steps without executing

## Validation

``` {.bash .ra-terminal title="Terminal"}
python cicd_run.py --config pipeline.yaml --dry-run
python cicd_run.py --config pipeline.yaml; echo $?  # 0 if pytest present
# Break a test and confirm exit 1
```

- [ ] Dry-run prints planned steps
- [ ] Successful pipeline exits `0` and writes report
- [ ] Failed step yields non-zero exit and appears in report
- [ ] No `shell=True`

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| pytest not found | Activate venv; `pip install pytest` |
| Relative paths | `cwd` to lab root |

## Cleanup

```bash
deactivate 2>/dev/null || true
rm -rf ~/rebash-lab-python-cicd
```

## Production Discussion

Real CI belongs in GitHub Actions/GitLab CI with cached deps and OIDC. This local runner is for fidelity while debugging; keep pipeline YAML as the single source of truth where possible.

## Related

- Labs index: [Python for DevOps labs](index.md)
- Capstone: [Production DevOps Automation Platform](../projects/python-devops-automation-framework.md)
- Quiz: [Python for DevOps Engineers Fundamentals](../quizzes/python-for-devops-engineers-fundamentals.md)
