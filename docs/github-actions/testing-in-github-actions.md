---
title: "Testing in GitHub Actions"
description: "Run unit, integration, and end-to-end tests in GitHub Actions with parallel matrix jobs, artefacts, and quality gates."
difficulty: intermediate
estimated_time: "45–60 min"
technology: github-actions
category: github-actions
module: "Module 12 · Testing"
learning_paths:
  - devops-engineer
  - software-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - github-actions
  - testing
  - ci
  - matrix
prerequisites:
  - github-actions/security-scanning-and-supply-chain
next:
  - github-actions/release-management-and-versioning
related:
  - github-actions/artifacts-and-caching
  - jenkins/testing-reports-and-quality-gates
tags:
  - github-actions
  - testing
  - matrix
  - e2e
  - unit-tests
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---

# Testing in GitHub Actions

## Overview

Continuous Integration (CI) without tests is packaging, not integration. GitHub Actions runs **unit**, **integration**, and **end-to-end (E2E)** jobs — often in **parallel matrix** builds across language versions or browsers — and fails the workflow before deploy when quality gates break.

This is **Tutorial 12** in **Module 12: Testing** of the REBASH Academy **GitHub Actions for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, SRE, and software engineers.

## Prerequisites

- [Security Scanning and Supply Chain](security-scanning-and-supply-chain.md)
- [Artifacts and Caching](artifacts-and-caching.md)
- Python 3 or Node.js for local test execution in the lab

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Structure separate jobs for unit, integration, and E2E tests
- [ ] Use matrix strategy for parallel version/browser coverage
- [ ] Upload test reports and coverage as artefacts
- [ ] Chain jobs with `needs:` so deploy waits on tests
- [ ] Diagnose flaky tests vs infrastructure failures

## Architecture

Build produces artefacts; test jobs run in parallel; deploy depends on all gates passing.

![Testing pipeline in GitHub Actions](../assets/excalidraw/gha-testing.svg)

## Theory

### What it is

| Layer | Scope | Typical tools | Speed |
|-------|-------|---------------|-------|
| Unit | Functions/modules in isolation | pytest, Jest, Go test | Seconds |
| Integration | Services + databases/APIs | pytest + Testcontainers, supertest | Minutes |
| E2E | Full user flows in browser/API | Playwright, Cypress | Minutes–tens of minutes |
| Smoke | Post-deploy health | curl, kubectl, synthetic check | Seconds |

**Matrix builds** run the same job with different `strategy.matrix` values (Python 3.11/3.12, Node 20/22) — failures pinpoint version-specific breaks.

### Why it matters

Deploying without tests shifts failures to production where rollback is expensive. Parallel matrices shorten feedback while increasing coverage. Clear job boundaries (`unit` → `integration` → `e2e`) keep fast tests failing first so developers do not wait twenty minutes for a typo.

### How it works

1. **Unit job** — checkout, install deps, run `pytest tests/unit` or `npm test`.
2. **Integration job** — `needs: unit`, start dependencies (Docker Compose service containers or Testcontainers), run integration suite.
3. **E2E job** — `needs: integration`, run Playwright against staging URL or ephemeral preview.
4. **Matrix** — {% raw %}`strategy.matrix.python-version: ['3.11','3.12']`{% endraw %} generates one runner per version.
5. **Artefacts** — upload JUnit XML, coverage HTML, Playwright traces for debugging failed runs.

Example matrix snippet (documentation):

{% raw %}
```yaml
strategy:
  fail-fast: false
  matrix:
    python-version: ['3.11', '3.12']
runs-on: ubuntu-latest
steps:
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```
{% endraw %}

### Key concepts and comparisons

| Pattern | When to use | Trade-off |
|---------|-------------|-----------|
| Single job all tests | Tiny repos | Slow feedback; hard to parallelise |
| Job per layer | Most services | More YAML; clearer failures |
| Matrix | Multi-version/browser | Runner minutes multiply |
| Reusable test workflow | Many repos | Central policy updates |

### Common pitfalls

- E2E on every pull request without caching browsers — slow and flaky.
- `continue-on-error: true` on test steps — green pipeline with failing tests.
- Integration tests hitting production APIs — data corruption and cost.
- No artefact upload on failure — cannot download Playwright trace.
- Matrix without `fail-fast: false` — one version failure hides others.

## Hands-on Lab

### Objective

Build a Python sample app with unit and integration tests, author a matrix test workflow with job dependencies, and validate tests locally plus YAML offline.

### Prerequisites

- Python 3.11+
- `pip` and `pytest`

### Lab environment

Workspace: `~/rebash-github-actions/module-12`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-github-actions/module-12/{app,tests/unit,tests/integration,.github/workflows} && cd ~/rebash-github-actions/module-12
set -euo pipefail
python3 --version | tee python-version.txt
```

### Real-world scenario

A platform team requires unit tests on every push, integration tests after unit pass, and a Python version matrix (3.11 and 3.12) before merge to `main`.

### Step-by-step tasks

#### Task 1 – Sample app and tests

Create `app/calc.py`:

```python title="calc.py"
def add(a: int, b: int) -> int:
    return a + b
```

Create `tests/unit/test_calc.py`:

```python title="test_calc.py"
from app.calc import add

def test_add():
    assert add(2, 3) == 5
```

Create `tests/integration/test_api_stub.py`:

```python title="test_api_stub.py"
def test_integration_placeholder():
    # Stand-in for HTTP/DB integration
    assert True
```

Create `requirements-dev.txt`:

```text title="requirements-dev.txt"
pytest>=8.0
pytest-cov>=4.0
```

Run tests locally:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-github-actions/module-12
set -euo pipefail
python3 -m pip install -q -r requirements-dev.txt
PYTHONPATH=. pytest tests/unit -q | tee unit-local.txt
PYTHONPATH=. pytest tests/integration -q | tee integration-local.txt
```

!!! example "Expected output"
    Both pytest runs pass; output captured in `unit-local.txt` and `integration-local.txt`.


#### Task 2 – Matrix test workflow with job chain

Create `.github/workflows/test.yml`:

{% raw %}
```yaml
name: Test
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  unit:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements-dev.txt
      - run: PYTHONPATH=. pytest tests/unit --junitxml=unit-junit.xml -q
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: unit-junit-${{ matrix.python-version }}
          path: unit-junit.xml

  integration:
    needs: unit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements-dev.txt
      - run: PYTHONPATH=. pytest tests/integration --junitxml=integration-junit.xml -q
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: integration-junit
          path: integration-junit.xml

  e2e-stub:
    needs: integration
    runs-on: ubuntu-latest
    steps:
      - run: echo "E2E stub — replace with Playwright against preview URL"
      - run: test 0 -eq 0
```
{% endraw %}

Validate offline:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-github-actions/module-12
set -euo pipefail
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/test.yml')); print('test workflow OK')"
grep -q 'matrix:' .github/workflows/test.yml
grep -q 'needs: unit' .github/workflows/test.yml
```

!!! example "Expected output"
    `test workflow OK`; matrix and `needs` present.


#### Task 3 – Local workflow structure checks

Create `validate-tests.sh`:

```bash title="validate-tests.sh"
#!/usr/bin/env bash
set -euo pipefail
PYTHONPATH=. pytest tests/unit tests/integration -q
python3 -c "import yaml; d=yaml.safe_load(open('.github/workflows/test.yml')); assert 'unit' in d['jobs']; assert 'integration' in d['jobs']"
grep -q 'upload-artifact' .github/workflows/test.yml
echo 'module-12 test lab passed'
```

Run it:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-github-actions/module-12
set -euo pipefail
chmod +x validate-tests.sh
./validate-tests.sh | tee validation.txt
```

!!! example "Expected output"
    `module-12 test lab passed`


#### Task 4 – Evidence archive

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-github-actions/module-12
set -euo pipefail
tar -czf module-12-evidence.tgz app tests requirements-dev.txt .github/workflows/test.yml *.txt validate-tests.sh
ls -l module-12-evidence.tgz | tee evidence.txt
```

!!! example "Expected output"
    Evidence tarball listed.


### Validation steps

- [ ] Unit and integration tests pass locally
- [ ] Workflow YAML parses; matrix covers two Python versions
- [ ] Integration job `needs: unit`; E2E stub `needs: integration`
- [ ] JUnit artefacts uploaded with `if: always()`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: app` | PYTHONPATH | Set `PYTHONPATH=.` in test step |
| Matrix job all red | One version incompatible | Use `fail-fast: false`; fix per version |
| Integration cannot reach DB | Service not started | Add `services:` postgres/redis container |
| Flaky E2E | Timing/network | Retries with limits; upload traces |
| Deploy ran despite test fail | Missing `needs:` | Gate deploy job on test jobs |

### Challenge exercise

Add a `services:` block with `postgres:16` and rewrite the integration test to connect with `psycopg` (or document connection string from `services` host). Fail if database is unreachable.

### Learning outcomes

- Created unit/integration tests with local proof
- Authored matrix workflow with job dependencies
- Uploaded test reports as artefacts
- Understood E2E as final gated stage

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
rm -rf ~/rebash-github-actions/module-12/__pycache__ ~/rebash-github-actions/module-12/**/__pycache__ 2>/dev/null || true
ls ~/rebash-github-actions/module-12
```

## Validation

- [ ] Lab completed under `~/rebash-github-actions/module-12/`
- [ ] You can explain unit vs integration vs E2E boundaries
- [ ] You can configure a matrix without fail-fast hiding versions
- [ ] You can describe one flaky-test mitigation

## Code Walkthrough

1. **Fast tests first** — unit before integration before E2E.
2. **Matrix with fail-fast false** — see all version failures.
3. **Artefacts on failure** — `if: always()` for JUnit/traces.
4. **Service containers** — integration deps on localhost ports.
5. **Deploy needs tests** — no shortcut around red jobs.

## Security Considerations

- Do not run untrusted fork code with secrets in test jobs — restrict permissions.
- Integration tests must not use production databases or credentials.
- Sanitise test fixtures — no real Personal Identifiable Information (PII) in CI logs.
- Pin test action versions (Module 11) like deploy actions.
- Limit E2E credentials to ephemeral preview environments.

## Common Mistakes

!!! warning "One giant test job"
    Twenty-minute feedback for typos. **Fix:** split unit/integration/E2E jobs.

!!! warning "`continue-on-error` on pytest"
    Broken main branch. **Fix:** fail the step; waivers only with tracked exceptions.

!!! warning "E2E against production"
    Data loss and audit issues. **Fix:** ephemeral preview or staging with synthetic data.

!!! warning "No test artefacts"
    Cannot debug CI-only failures. **Fix:** upload JUnit, coverage, Playwright traces.

## Best Practices

- Cache dependencies (`actions/cache`) keyed on lockfiles.
- Tag flaky tests; quarantine with ticket, do not silence permanently.
- Require test workflow success in branch protection rules.
- Keep integration tests deterministic — fixed seeds, isolated databases.
- Report test timing trends to catch slow suites early.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Passes locally, fails CI | Version mismatch | Align matrix with local Python |
| Integration timeout | Service not healthy | Add health check wait loop |
| Matrix duplicates work | Too many dimensions | Split smoke vs full matrix nightly |
| Empty JUnit artefact | Wrong output path | Verify `--junitxml` path matches upload |
| E2E flaky on CI only | Resource/time limits | Increase timeout; reduce parallelism |

## Summary

Testing in GitHub Actions layers unit, integration, and E2E jobs with matrices for parallel coverage and artefacts for debugging. Gate deploy on green tests. Next: [Release Management and Versioning](release-management-and-versioning.md).

## Interview Questions

**1. Why split unit, integration, and E2E into separate jobs?**

??? success "Reveal answer"
    Failures surface faster (unit fails in seconds), runner resources match test type, and deploy can depend on explicit gates rather than one opaque job result.

**2. What does `strategy.matrix` do?**

??? success "Reveal answer"
    It expands one job definition into multiple parallel jobs — one per matrix combination (e.g. Python 3.11 and 3.12) — increasing coverage without duplicating YAML.

**3. When should you set `fail-fast: false` on a matrix?**

??? success "Reveal answer"
    When you want all matrix combinations to run even if one fails — so you see every broken version rather than stopping at the first failure.

**4. How do service containers help integration tests?**

??? success "Reveal answer"
    GitHub Actions starts Docker sidecars (e.g. Postgres) on localhost ports for the job, giving real dependencies without external infrastructure.

**5. Why upload test artefacts with `if: always()`?**

??? success "Reveal answer"
    Failed tests still produce JUnit XML or Playwright traces needed for debugging — uploading only on success hides evidence when you need it most.

**6. How should E2E tests relate to deploy jobs?**

??? success "Reveal answer"
    E2E should run against staging or preview after build; deploy to production should `need` E2E (and unit/integration) success unless a documented exception exists.

**7. What is the difference between smoke tests and E2E?**

??? success "Reveal answer"
    Smoke tests are minimal post-deploy health checks (one endpoint up); E2E exercises full user journeys — smoke is faster and runs immediately after deploy.

**8. How do you reduce flaky E2E in Actions?**

??? success "Reveal answer"
    Stable selectors, isolated test data, limited retries with alerting, artefact traces on failure, and not running full E2E on every commit if a nightly job suffices.

## Related Tutorials

- [Artifacts and Caching](artifacts-and-caching.md)
- [Security Scanning and Supply Chain](security-scanning-and-supply-chain.md)
- [Release Management and Versioning](release-management-and-versioning.md)

## References

- [Workflow syntax — jobs matrix](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs)
- [Service containers](https://docs.github.com/en/actions/using-containerized-services/about-service-containers)
- [pytest documentation](https://docs.pytest.org/)
- [Playwright CI](https://playwright.dev/docs/ci)
