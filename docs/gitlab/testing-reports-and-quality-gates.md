---
title: "Testing, Reports, and Quality Gates"
description: "Run unit, integration, e2e, and performance tests in GitLab CI — parallel jobs, JUnit reports, coverage, and quality gates that block merge."
difficulty: intermediate
estimated_time: "45–60 min"
technology: gitlab
category: gitlab
module: "Module 13 · Testing"
learning_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - gitlab-ci
  - testing
  - quality-gates
  - junit
prerequisites:
  - gitlab/security-scanning-and-devsecops
next:
  - gitlab/release-management-and-versioning
related:
  - gitlab/artifacts-caches-and-dependencies
  - gitlab/pipeline-design-dags-and-includes
labs: []
projects: []
interview: interview/gitlab
certifications:
  - GitLab Certified CI/CD Associate
  - GitLab Certified DevOps Professional
tags:
  - gitlab
  - testing
  - junit
  - quality-gates
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---


# Testing, Reports, and Quality Gates

## Overview








Design a test pyramid in GitLab CI with parallel jobs, JUnit and coverage reports in merge requests, and quality gates that fail the pipeline when thresholds are missed.

Tests are the cheapest production incident you never ship. GitLab CI runs **unit**, **integration**, **end-to-end (e2e)**, and optional **performance** jobs; publishes **JUnit** and coverage artefacts into the merge request (MR); and enforces **quality gates** so red tests block merge.

This is a core tutorial in **Module 13 · Testing** of the REBASH Academy **GitLab CI/CD for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites








- [Security Scanning and DevSecOps](security-scanning-and-devsecops.md)
- Comfortable with stages, `needs`, and artefacts from earlier modules

## Learning Objectives








By the end of this tutorial, you will be able to:

- [ ] Map unit / integration / e2e / performance to CI stages or `needs`  
- [ ] Parallelise suites with `parallel` or `parallel:matrix`  
- [ ] Publish JUnit reports and coverage for MR widgets  
- [ ] Fail the pipeline on failed tests or coverage thresholds

## Architecture








This topic’s control points and relationships are shown below.

![GitLab testing](../assets/excalidraw/gitlab-testing.svg)

## Theory








### What it is

**Testing in GitLab CI** means every change runs automated checks before it reaches a deployable environment. Jobs execute your test runners (pytest, Jest, Go `testing`, and so on), collect machine-readable reports, and attach them with `artifacts:reports`. A **quality gate** is any rule that turns a soft signal into a hard failure — non-zero exit codes, coverage below a floor, or required jobs that must succeed before merge.

| Layer | Typical scope | CI cost |
|-------|---------------|---------|
| Unit | Functions / packages, mocked I/O | Fast, run always |
| Integration | Service + DB / API contracts | Medium |
| E2E | Browser or full path | Slow, selective |
| Performance | Latency / throughput smoke | Scheduled or nightly |

### Why it matters

Cloud services fail in integration, not in unit isolation. Pipelines that only “build the image” ship regressions at promotion time. MR-visible JUnit and coverage make review concrete: reviewers see which cases failed and whether coverage slipped. Quality gates protect trunk — flaky or missing tests become a platform problem, not a Friday surprise in production.

### How it works

Recommended shape:

1. **Fail fast** — lint and unit tests before expensive builds.
2. **Parallelise** — split unit/integration with `parallel: 4` or a matrix of OS/runtime variants.
3. **Report** — write JUnit XML; set `artifacts:reports:junit` (and `coverage_report` / `coverage` regex as needed).
4. **Gate** — job exit code non-zero on failure; optional script that compares coverage to `$COVERAGE_MIN`.
5. **Select e2e** — run full e2e on `main` / nightly; smoke e2e on MRs with `rules`.

Use `needs` so unit jobs start as soon as their build artefact exists, without waiting for unrelated stages. Keep report paths stable so the MR widget always finds them.

### Key concepts and comparisons

| Mechanism | Purpose |
|-----------|---------|
| Job exit code | Primary gate (failed tests → failed job) |
| `artifacts:reports:junit` | MR test summary UI |
| Coverage regex / report | Coverage widget and trends |
| `allow_failure: true` | Soft signal only — use sparingly |
| Required pipeline success | Project setting / protected branch |

Unit tests prove logic; integration proves wiring; e2e proves the user path. Performance belongs after functional green, usually on a schedule.

### Common pitfalls

- Publishing JUnit but using `allow_failure: true` on the test job — the report appears while the pipeline stays green.
- One monolithic e2e job on every commit — burns minutes and creates flaky noise.
- Coverage gates without excluding generated code — false negatives block good changes.
- Forgetting `when: always` on report artefacts — failed suites never upload XML for debugging.

## Hands-on Lab



### Objective

Create pytest tests with JUnit XML output, configure GitLab CI to publish test reports as artefacts, and prove the report format locally.

### Prerequisites

- Python 3 with PyYAML and pytest (`pip install pyyaml pytest`)
- Optional: GitLab project with a runner

### Lab environment

Workspace: `~/rebash-gitlab/module-13`

File-first lab. Test reports upload on GitLab runners; this lab validates XML and pipeline structure locally.

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-gitlab/module-13 && cd ~/rebash-gitlab/module-13
set -euo pipefail
```

### Real-world scenario

Quality engineering requires unit tests on every merge request with JUnit reports visible in the merge request UI — failed suites must still upload XML for debugging. You deliver tests, sample report XML, and pipeline YAML for review.

### Step-by-step tasks

#### Task 1 – Sample tests and requirements

Create `app/calc.py`:

```python title="calc.py"
def add(a: int, b: int) -> int:
    return a + b
```

Create `tests/test_calc.py`:

```python title="test_calc.py"
from app.calc import add

def test_add():
    assert add(2, 3) == 5

def test_add_zero():
    assert add(0, 0) == 0
```

Create `requirements-dev.txt`:

```text title="requirements-dev.txt"
pytest>=8.0
```

Run tests locally with JUnit output:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-gitlab/module-13
set -euo pipefail
python3 -m pip install -q -r requirements-dev.txt
PYTHONPATH=. pytest tests/ --junitxml=report.xml -q | tee pytest-local.txt
test -f report.xml
grep -q 'testsuite' report.xml
```

!!! example "Expected output"
    Pytest passes; `report.xml` contains a `testsuite` element.


#### Task 2 – Sample JUnit XML (reference fixture)

Create `fixtures/sample-junit.xml`:

```xml title="sample-junit.xml"
<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="module-13-fixture" tests="2" failures="0" errors="0" time="0.01">
  <testsuite name="tests.test_calc" tests="2" failures="0" errors="0" skipped="0" time="0.01">
    <testcase classname="tests.test_calc" name="test_add" time="0.005"/>
    <testcase classname="tests.test_calc" name="test_add_zero" time="0.005"/>
  </testsuite>
</testsuites>
```

Validate the fixture:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-gitlab/module-13
set -euo pipefail
grep -q 'test_add' fixtures/sample-junit.xml
python3 -c "
import xml.etree.ElementTree as ET
root = ET.parse('fixtures/sample-junit.xml').getroot()
assert root.tag == 'testsuites'
assert int(root.attrib['tests']) == 2
print('sample-junit.xml OK')
"
```

!!! example "Expected output"
    `sample-junit.xml OK`


#### Task 3 – GitLab CI with JUnit report artefacts

Create `.gitlab-ci.yml`:

{% raw %}
```yaml
stages:
  - test

variables:
  PIP_CACHE_DIR: "${CI_PROJECT_DIR}/.cache/pip"

unit-tests:
  stage: test
  image: python:3.12-alpine
  before_script:
    - pip install -r requirements-dev.txt
  script:
    - PYTHONPATH=. pytest tests/ --junitxml=junit-report.xml -q
  artifacts:
    when: always
    reports:
      junit: junit-report.xml
    paths:
      - junit-report.xml
    expire_in: 7 days
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```
{% endraw %}

Validate offline:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-gitlab/module-13
set -euo pipefail
python3 -c "
import yaml
d = yaml.safe_load(open('.gitlab-ci.yml'))
j = d['unit-tests']
assert j['artifacts']['when'] == 'always'
assert j['artifacts']['reports']['junit'] == 'junit-report.xml'
print('gitlab-ci OK')
"
grep -q 'python:3.12-alpine' .gitlab-ci.yml
```

!!! example "Expected output"
    `gitlab-ci OK`; pinned Python image and `when: always` on artefacts.


#### Task 4 – Local validation script

Create `validate-tests.sh`:

```bash title="validate-tests.sh"
#!/usr/bin/env bash
set -euo pipefail
PYTHONPATH=. pytest tests/ --junitxml=junit-report.xml -q
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml'))"
grep -q 'reports:' .gitlab-ci.yml
test -s junit-report.xml
echo 'module-13 testing lab passed'
```

Run it:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-gitlab/module-13
set -euo pipefail
chmod +x validate-tests.sh
./validate-tests.sh | tee validation.txt
```

!!! example "Expected output"
    `module-13 testing lab passed`


### Validation steps

- [ ] Pytest generates valid JUnit XML locally
- [ ] Pipeline publishes `junit-report.xml` with `artifacts.reports.junit`
- [ ] `when: always` ensures reports upload on failure
- [ ] Pinned image `python:3.12-alpine` present
- [ ] Sample fixture XML parses with Python ElementTree

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Empty report in MR UI | Missing `reports: junit` | Add under `artifacts.reports` |
| No XML on failed job | Missing `when: always` | Set on artefacts block |
| `ModuleNotFoundError: app` | PYTHONPATH not set | Export `PYTHONPATH=.` in script |
| Flaky tests block merge | No retry policy | Fix root cause; avoid blind retry |
| Coverage gate without config | Wrong pytest plugin | Add `pytest-cov` and document threshold |

### Challenge exercise

Add an integration test job that `needs: [unit-tests]` and publishes a second JUnit file `integration-junit.xml`. Gate a deploy stub on both jobs succeeding.

### Learning outcomes

- Generated JUnit XML from pytest locally
- Configured GitLab CI test report artefacts with `when: always`
- Validated report structure before pushing to GitLab
- Understood quality gates tied to test evidence

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
rm -rf ~/rebash-gitlab/module-13/.pytest_cache ~/rebash-gitlab/module-13/**/__pycache__ 2>/dev/null || true
ls ~/rebash-gitlab/module-13
```

## Validation








- [ ] Lab commands run under `~/rebash-gitlab/module-13/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough








Production practice for **Testing, Reports, and Quality Gates** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations








- Treat credentials and tokens for gitlab as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes








!!! warning "Publishing JUnit but using `allow_failure: true` on the test job — the report appears whil"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "One monolithic e2e job on every commit — burns minutes and creates flaky noise."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices








- Encode Testing, Reports, and Quality Gates changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting








| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |

## Summary








**Testing, Reports, and Quality Gates** is essential for Cloud and DevOps engineers working with gitlab. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions






1. How do JUnit report artifacts improve merge request feedback?
2. A quality gate flakes intermittently — what evidence do you gather?
3. Where should coverage thresholds live: CI job or shared policy?
4. Why keep allow_failure rare on security/unit gates?
5. How do you prevent skipped tests from counting as green?

!!! tip "Sample answer — question 2"
    Open the JUnit report and job log together: distinguish assertion failures from environment errors. Quarantine flakes with an owner rather than silently allow_failure.

!!! tip "Sample answer — question 4"
    Gates that protect production should fail closed. Ensure forks cannot skip required jobs while consuming protected variables.

## Related Tutorials








- [Course overview](index.md)
- [Release Management and Versioning](release-management-and-versioning.md)

## References








- [Unit test reports](https://docs.gitlab.com/ee/ci/testing/unit_test_reports.html)  
- [Code coverage](https://docs.gitlab.com/ee/ci/testing/code_coverage.html)  
- [Parallel jobs](https://docs.gitlab.com/ee/ci/yaml/#parallel)
