---
title: "Lab — CI/CD Pipeline Failure Triage"
description: "Diagnose a failing merge pipeline — read job logs, fix stage, job, and script errors in GitLab CI YAML, and restore a green build."
difficulty: intermediate
estimated_time: "60 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-28"
tags:
  - labs
  - cicd
  - gitlab
  - troubleshooting
comments: false
---

# Lab — CI/CD Pipeline Failure Triage

## Lab Overview

**Purpose:** Combine CI/CD foundations — pipeline anatomy, GitLab CI YAML, log reading, and lint validation — in one realistic failure triage exercise.

**Scenario:** A merge request pipeline for **rebash-status** fails on the first push after a hurried YAML edit. The pipeline UI shows red jobs, but the root cause is buried in job logs. You must read evidence, fix configuration errors (stage, job, script), and get a green pipeline without disabling checks.

**Expected outcome:** All stages pass; you can explain each injected fault with job log excerpts and `gitlab-ci-lint` output.

!!! tip "This is a lab, not a tutorial"
    Prefer job logs and YAML lint over guess-and-push. Document what broke, how you found it, and how you validated recovery.

!!! note "Other platforms"
    Jenkins and GitHub Actions come later on REBASH Academy — this lab uses **GitLab CI** only.

## Business Scenario

The platform team maintains a small Python health-check service. A developer renamed a test directory and edited `.gitlab-ci.yml` in the same commit. CI now fails on every merge request. Stakeholders need the pipeline green before end of day. Your job is to reproduce the faults locally, triage with logs and lint tools, fix the YAML in order, push a corrected commit, and confirm a passing pipeline.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Navigate a failed pipeline and identify which stage and job failed first
- [ ] Read job logs to distinguish script errors from YAML/schema faults
- [ ] Fix common `.gitlab-ci.yml` mistakes: wrong stage, missing script, bad image, typos
- [ ] Validate YAML with `gitlab-ci-lint` before pushing
- [ ] Interpret `rules:` and `needs:` when triaging skipped or blocked jobs

## Prerequisites

### Knowledge

- [GitLab CI/CD Fundamentals](../gitlab/gitlab-ci-fundamentals.md)
- [GitLab Projects, Merge Requests, and Releases](../gitlab/gitlab-projects-mrs-and-releases.md)
- [Pipeline Syntax](../gitlab/pipeline-syntax-gitlab-ci-yml.md)
- [Troubleshooting GitLab CI](../gitlab/troubleshooting-gitlab-ci.md)

### Software

| Tool | Notes |
|------|--------|
| Git | 2.x |
| GitLab.com account (free tier) **or** self-managed GitLab | Project with CI enabled |
| `gitlab-ci-lint` via API **or** GitLab UI CI Lint | Validate before push |
| Python 3.12 (optional) | Local reproduction of test step |
| Docker (optional) | Run `python:3.12-slim` locally to mirror CI image |

**Estimated cost:** £0 on GitLab.com free tier.

## Architecture

![CI/CD pipeline triage: failed job, log evidence, YAML fix, lint, green pipeline](../assets/images/lab-cicd-pipeline-triage.svg)

## Environment

Create a dedicated lab project on GitLab.com (or use a fork). Set a consistent prefix:

```bash
export LAB_PREFIX="rebash-cicd-triage-$(whoami | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9-' | cut -c1-12)"
mkdir -p ~/rebash-lab-cicd && cd ~/rebash-lab-cicd
git init -b main
```

Do **not** run destructive steps against shared production pipeline configuration.

## Initial State

You will create a minimal Python project with a **broken** `.gitlab-ci.yml` containing three injected faults:

1. Job references a **non-existent stage** (`verify` instead of `test`)
2. **Typo in script** — `pytest` run against wrong path (`tests/` vs `test/`)
3. **Missing `script`** on a lint job (empty job definition)

Your job is to prove each layer with logs before fixing it.

## Lab Repository Scaffold

### Task 1 — Create application and tests

**Objective:** Establish a known-good application baseline separate from CI config.

**Instructions:**

```bash
cd ~/rebash-lab-cicd

mkdir -p test app
cat > app/__init__.py <<'EOF'
__version__ = "0.1.0"
EOF

cat > app/health.py <<'EOF'
def is_healthy() -> bool:
    return True
EOF

cat > test/test_health.py <<'EOF'
from app.health import is_healthy

def test_health():
    assert is_healthy() is True
EOF

cat > requirements.txt <<'EOF'
pytest==8.3.4
EOF

python3 -m pytest -q test/ && echo "local tests OK"
```

**Expected output:** `1 passed` locally.

**Validation:**

```bash
python3 -m pytest -q test/ 2>&1 | grep -q "passed" && echo "baseline tests OK"
```

### Task 2 — Commit broken pipeline YAML

**Objective:** Install the failing CI configuration that mimics a rushed MR.

**Instructions:**

```bash
cat > .gitlab-ci.yml <<'EOF'
stages:
  - lint
  - test
  - build

lint-yaml:
  stage: lint
  image: python:3.12-slim
  # Fault 3: missing script block entirely

unit-test:
  stage: verify
  image: python:3.12-slim
  script:
    - pip install -r requirements.txt
    - pytest -q tests/
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

build-artifact:
  stage: build
  image: python:3.12-slim
  script:
    - echo "build ok" > dist.txt
  artifacts:
    paths:
      - dist.txt
  needs:
    - unit-test
EOF

git add .
git commit -m "feat: add rebash-status with initial CI (broken)"
```

**Expected output:** Commit succeeds; pipeline will fail when pushed.

!!! note "Injected faults summary"
    | # | Fault | Symptom |
    |---|-------|---------|
    | 1 | `unit-test` uses `stage: verify` | Job never runs / unknown stage error |
    | 2 | `pytest -q tests/` | Script exit 4 — no tests collected |
    | 3 | `lint-yaml` has no `script` | Job fails immediately — script required |

### Task 3 — Push and observe pipeline failure

**Objective:** Reproduce the failure in GitLab CI (or lint locally if offline).

**Instructions:**

```bash
# Create empty project on GitLab.com, then:
git remote add origin "git@gitlab.com:YOUR_GROUP/${LAB_PREFIX}.git"
git push -u origin main
```

Open **CI/CD → Pipelines** and note:

- Which job failed first
- Whether the pipeline was **invalid** (YAML) vs **failed** (script)

**Local lint alternative:**

```bash
# Replace PROJECT_ID and TOKEN with your values
curl --silent --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --form "content=$(cat .gitlab-ci.yml)" \
  "https://gitlab.com/api/v4/projects/PROJECT_ID/ci/lint" | jq .
```

**Expected output:** Lint or pipeline UI reports stage/script errors.

**Validation:** Capture one log line showing `stage: verify` or `script can't be blank` or `ERROR: Job failed: exit code 4`.

### Task 4 — Triage: invalid stage vs script failure

**Objective:** Distinguish configuration schema errors from test script failures.

**Background:** Operators often treat all red pipelines as "tests failed". Stage typos and missing scripts fail **before** meaningful test output.

**Instructions:**

1. Open the **unit-test** job log (if it ran) or the pipeline **yaml invalid** banner
2. Open **lint-yaml** job log — expect immediate failure
3. Answer in one line each:
   - Is `verify` declared under `stages:`?
   - Does the filesystem contain `tests/` or `test/`?

```bash
ls -la test/ tests/ 2>/dev/null || true
grep -E '^stages:|verify|test' .gitlab-ci.yml
```

**Expected output:**

- `test/` exists; `tests/` does not
- `stages:` lists `lint`, `test`, `build` — not `verify`

**Validation:** Written root cause for fault 1: "Job stage `verify` not in top-level stages list."

### Task 5 — Fix stage name

**Objective:** Align job stage with declared stages.

**Instructions:**

```bash
sed -i.bak 's/stage: verify/stage: test/' .gitlab-ci.yml
grep 'stage: test' .gitlab-ci.yml
```

**Expected output:** `unit-test` now uses `stage: test`.

**Validation:** Re-run CI lint; stage error cleared.

### Task 6 — Fix script path

**Objective:** Point pytest at the correct directory.

**Instructions:**

```bash
sed -i.bak 's|pytest -q tests/|pytest -q test/|' .gitlab-ci.yml
grep pytest .gitlab-ci.yml
```

**Expected output:** `pytest -q test/`

**Validation:**

```bash
docker run --rm -v "$PWD:/app" -w /app python:3.12-slim \
  bash -c 'pip install -q -r requirements.txt && pytest -q test/'
```

### Task 7 — Add missing lint script

**Objective:** Give `lint-yaml` a real script step.

**Instructions:**

```bash
cat > .gitlab-ci.yml <<'EOF'
stages:
  - lint
  - test
  - build

lint-yaml:
  stage: lint
  image: python:3.12-slim
  script:
    - pip install --quiet pyyaml
    - python -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml'))"
    - echo "YAML parse OK"

unit-test:
  stage: test
  image: python:3.12-slim
  script:
    - pip install -r requirements.txt
    - pytest -q test/
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

build-artifact:
  stage: build
  image: python:3.12-slim
  script:
    - echo "build ok" > dist.txt
  artifacts:
    paths:
      - dist.txt
  needs:
    - unit-test
EOF
```

**Expected output:** All three jobs have non-empty `script` blocks.

**Validation:** CI lint passes with no errors.

### Task 8 — Push fix and confirm green pipeline

**Objective:** Validate end-to-end green pipeline on GitLab.

**Instructions:**

```bash
git add .gitlab-ci.yml
git commit -m "fix(ci): correct stage, test path, and lint script"
git push origin main
```

Watch the pipeline until all jobs succeed. Download the **dist.txt** artefact from **build-artifact**.

**Expected output:** Pipeline status **passed**; artefact present.

**Validation:**

```bash
# After downloading artefact from UI:
cat dist.txt | grep -q "build ok" && echo "artefact OK"
```

### Task 9 — Document triage evidence

**Objective:** Capture a concise incident-style summary for each fault.

**Instructions:**

For each of the three faults, write one paragraph covering:

- Job name and stage
- First meaningful log line
- Root cause category (schema vs script)
- Fix applied

**Validation:** Three paragraphs in your notes — reusable as an interview narrative.

## Validation

| Check | Pass criteria |
|-------|----------------|
| Baseline | Local `pytest test/` passes |
| Fault reproduction | Pipeline failed on initial push |
| Stage triage | Identified `verify` vs `stages:` mismatch |
| Script triage | Log shows wrong path or exit code 4 |
| Lint job | `lint-yaml` had no script; now parses YAML |
| Lint tool | `gitlab-ci-lint` returns valid |
| Green pipeline | All jobs passed on fix commit |
| Artefact | `dist.txt` downloadable from build job |

## Troubleshooting

| Symptoms | Causes | Resolution | Verification |
|----------|--------|------------|--------------|
| Pipeline "yaml invalid" | Unknown stage, bad keyword | Read lint output; fix `stages:` | CI lint green |
| Job skipped entirely | `rules:` excluded branch | Check MR vs branch pipeline source | Job appears in graph |
| `script can't be blank` | Empty job | Add `script:` block | Job starts |
| pytest exit 4 | Wrong directory | `ls` repo; fix path | Tests collected |
| `needs` cycle / missing | DAG typo | Verify job names match | Pipeline graph loads |
| Lint API 401 | Bad token | Scoped `api` token | HTTP 200 from lint |

## Challenge Extensions

- Add a **fourth fault**: `needs: [unit-tests]` typo on `build-artifact` — triage DAG errors
- Add `workflow:rules:` so pipelines run only on MRs and default branch — observe skipped branch pipelines
- Add `allow_failure: true` on lint and explain why that hides real failures

## Cleanup

Delete the lab project on GitLab.com when finished, or archive it. Remove local clone if no longer needed:

```bash
cd ~ && rm -rf ~/rebash-lab-cicd
```

## Production Discussion

Production triage starts with **which job failed first** in the DAG, not the last red badge. Schema errors (stages, `needs`, includes) surface in lint and pre-merge checks — wire `gitlab-ci-lint` into pre-commit or MR pipelines. Script failures need log excerpts attached to the incident ticket. Never "fix" CI by disabling tests without a tracked follow-up.

## Best Practices

- Run CI lint locally or in pre-push hooks before opening an MR
- Read logs from the **first failed job** in stage order
- Keep stage names in a single canonical list at the top of YAML
- Mirror directory renames in CI paths in the same commit
- Use `needs:` intentionally — document job dependency graphs

## Common Mistakes

| Mistake | Why | Fix |
|---------|-----|-----|
| Pushing repeatedly without reading logs | Wastes runner minutes | Lint + read first failed job |
| Renaming folders without updating CI | Silent test skip | Same MR updates paths |
| Disabling failing jobs | Hides regressions | Fix root cause |
| Confusing skipped vs failed | Wrong triage path | Check `rules:` and branch |
| Wrong default branch rules | Pipeline never runs | Verify `$CI_DEFAULT_BRANCH` |

## Success Criteria

You reproduced three CI faults, triaged with logs and lint, fixed stage/job/script errors, and pushed a green pipeline with downloadable artefacts.

## Reflection Questions

1. Why does an invalid stage name fail differently from a pytest path error?
2. What is the first tool you run before pushing CI YAML in a team with shared runners?
3. How would `needs:` change triage if `unit-test` never ran but `build-artifact` was manual?
4. Where should CI lint live — developer laptop, MR pipeline, or both?

## Interview Connection

Tell this story: open pipeline graph → first failed job → log excerpt → classify schema vs script → lint → fix → green build. Continue with [CI/CD Interview Prep](../interview/cicd.md).

## Related Tutorials

- [CI/CD](../gitlab/index.md)
- [GitLab CI/CD Fundamentals](../gitlab/gitlab-ci-fundamentals.md)
- [GitLab Projects, Merge Requests, and Releases](../gitlab/gitlab-projects-mrs-and-releases.md)
- [Pipeline Syntax](../gitlab/pipeline-syntax-gitlab-ci-yml.md)
- [Troubleshooting GitLab CI](../gitlab/troubleshooting-gitlab-ci.md)
- Quiz: [CI/CD Fundamentals](../quizzes/cicd-fundamentals.md)
- Cheat sheet: [GitLab CI/CD](../cheatsheets/cicd.md)

## References

1. [GitLab CI/CD YAML reference](https://docs.gitlab.com/ee/ci/yaml/)
2. [GitLab CI Lint API](https://docs.gitlab.com/ee/api/lint.html)
3. [GitLab troubleshooting failed jobs](https://docs.gitlab.com/ee/ci/jobs/job_logs.html)
