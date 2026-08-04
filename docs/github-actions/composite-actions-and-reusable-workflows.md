---
title: "Composite Actions and Reusable Workflows"
description: "Build composite actions and reusable workflows to deduplicate CI/CD logic across repositories with callable workflows and local action metadata."
difficulty: advanced
estimated_time: "50–65 min"
technology: github-actions
category: github-actions
module: "Module 14 · Reusable Components"
learning_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - github-actions
  - composite-actions
  - reusable-workflows
  - platform-engineering
prerequisites:
  - github-actions/release-management-and-versioning
  - github-actions/workflow-syntax-matrix-and-reusable
next:
  - github-actions/production-pipelines-and-environments
related:
  - github-actions/artifacts-and-caching
  - jenkins/shared-libraries
tags:
  - github-actions
  - composite
  - reusable-workflow
  - DRY
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---

# Composite Actions and Reusable Workflows

## Overview

Copy-pasting fifty lines of setup into every repository does not scale. **Composite actions** bundle steps into a local or published action; **reusable workflows** expose entire jobs via `workflow_call` so service repos invoke a standard platform pipeline with inputs and secrets.

This is **Tutorial 14** in **Module 14: Reusable Components** of the REBASH Academy **GitHub Actions for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers building internal developer platforms.

## Prerequisites

- [Release Management and Versioning](release-management-and-versioning.md)
- [Workflow Syntax: Matrix and Reusable Workflows](workflow-syntax-matrix-and-reusable.md)
- Python 3 with PyYAML for offline validation

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Author a composite action with `action.yml` inputs and steps
- [ ] Create a reusable workflow callable via `workflow_call`
- [ ] Wire a caller workflow that uses both components together
- [ ] Pass inputs, secrets, and outputs across reusable boundaries
- [ ] Choose composite action vs reusable workflow for a given problem

## Architecture

Service repositories call reusable workflows; reusable workflows invoke composite actions for shared step bundles.

![Reusable components in GitHub Actions](../assets/excalidraw/gha-reusable-components.svg)

## Theory

### What it is

| Mechanism | Granularity | Defined in | Called via |
|-----------|-------------|------------|------------|
| Composite action | Steps (shell grouped) | `action.yml` in repo path | `uses: ./.github/actions/name` or `org/repo/path@ref` |
| Reusable workflow | Jobs/workflows | `.github/workflows/*.yml` with `on: workflow_call` | `uses: org/repo/.github/workflows/x.yml@ref` |
| JavaScript action | Custom Node logic | `action.yml` + `dist/` | Same as composite |
| Marketplace action | Third-party | Published repo | `uses: owner/action@v4` (pin SHA in prod) |

**Composite actions** cannot call other composite actions recursively in all cases — keep them focused. **Reusable workflows** support `secrets: inherit` and job outputs for platform teams.

### Why it matters

Platform engineering centralises compliance (scanning, pinning, OIDC login) once. Service teams supply inputs (app name, Python version) without forking platform YAML. Updates roll out when callers pin to new `@v2` tag or SHA.

### How it works

1. Platform repo publishes `/.github/actions/setup-python-app/action.yml` (composite).
2. Platform repo publishes `/.github/workflows/ci-reusable.yml` with `workflow_call` inputs.
3. Service repo workflow:

{% raw %}
```yaml
jobs:
  ci:
    uses: my-org/platform/.github/workflows/ci-reusable.yml@v1
    with:
      python-version: '3.12'
    secrets: inherit
```
{% endraw %}

4. Reusable workflow checks out code and `uses: ./.github/actions/setup-python-app` with inputs.
5. Outputs from reusable jobs expose version or artefact names to caller via `jobs.<id>.outputs`.

### Key concepts and comparisons

| Use composite when | Use reusable workflow when |
|--------------------|----------------------------|
| Bundling 3–10 shell steps | Entire CI job graph needed |
| Same repo or lightweight share | Cross-repo standard pipeline |
| Inputs are step parameters | Need job-level `needs`, environments |
| No separate runner job semantics | Caller should stay minimal |

### Common pitfalls

- Putting `runs-on` inside composite action (invalid — composite runs on caller's runner).
- Reusable workflow without documenting required `secrets`.
- Callers pin `@main` — silent breaking changes.
- Circular `workflow_call` dependencies between repos.
- Composite action trying to set job outputs without `outputs` in `action.yml`.

## Hands-on Lab

### Objective

Build a **composite action** (setup + validate marker file) and a **reusable workflow** that calls it, then author a **caller workflow** in the same lab repo — all validated offline.

### Prerequisites

- Python 3 with PyYAML
- Bash

### Lab environment

Workspace: `~/rebash-github-actions/module-14`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-github-actions/module-14/.github/{actions/setup-lab,workflows} && cd ~/rebash-github-actions/module-14
set -euo pipefail
```

### Real-world scenario

Platform team ships `setup-lab` composite action and `ci-reusable.yml` reusable workflow. Application repos only maintain a ten-line caller workflow.

### Step-by-step tasks

#### Task 1 – Composite action

Create `.github/actions/setup-lab/action.yml`:

{% raw %}
```yaml
name: Setup lab workspace
description: Create marker file and validate lab path
inputs:
  lab-name:
    description: Lab identifier
    required: true
outputs:
  marker-path:
    description: Path to marker file
    value: ${{ steps.mk.outputs.path }}
runs:
  using: composite
  steps:
    - id: mk
      shell: bash
      run: |
        set -euo pipefail
        mkdir -p out
        path="out/${{ inputs.lab-name }}.txt"
        echo "lab=${{ inputs.lab-name }}" > "$path"
        echo "path=$path" >> "$GITHUB_OUTPUT"
    - shell: bash
      run: test -s "${{ steps.mk.outputs.path }}"
```
{% endraw %}

Validate offline:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-github-actions/module-14
set -euo pipefail
python3 -c "import yaml; yaml.safe_load(open('.github/actions/setup-lab/action.yml')); print('composite action OK')"
grep -q 'using: composite' .github/actions/setup-lab/action.yml
```

!!! example "Expected output"
    `composite action OK`


Note: The `action.yml` above uses GitHub expressions in the lab file on disk — in MkDocs the tutorial wraps those fences in raw Jinja blocks. For offline simulation, run the shell steps manually:

``` {.bash .ra-terminal title="Terminal"}
mkdir -p out && echo 'lab=module-14' > out/module-14.txt && test -s out/module-14.txt
```

!!! example "Expected output"
    Silent success (exit 0).


#### Task 2 – Reusable workflow

Create `.github/workflows/ci-reusable.yml`:

{% raw %}
```yaml
name: CI Reusable
on:
  workflow_call:
    inputs:
      lab-name:
        required: true
        type: string
    outputs:
      marker-path:
        description: Marker file from setup
        value: ${{ jobs.build.outputs.marker-path }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      marker-path: ${{ steps.setup.outputs.marker-path }}
    steps:
      - uses: actions/checkout@v4
      - id: setup
        uses: ./.github/actions/setup-lab
        with:
          lab-name: ${{ inputs.lab-name }}
      - name: Prove marker
        run: cat "${{ steps.setup.outputs.marker-path }}"
```
{% endraw %}

Validate offline:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-github-actions/module-14
set -euo pipefail
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci-reusable.yml')); print('reusable workflow OK')"
grep -q 'workflow_call' .github/workflows/ci-reusable.yml
```

!!! example "Expected output"
    `reusable workflow OK`


#### Task 3 – Caller workflow (pair)

Create `.github/workflows/caller.yml`:

```yaml title="caller.yml"
name: Caller
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  platform-ci:
    uses: ./.github/workflows/ci-reusable.yml
    with:
      lab-name: module-14
```

Validate offline:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-github-actions/module-14
set -euo pipefail
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/caller.yml')); print('caller workflow OK')"
grep -q 'uses: ./.github/workflows/ci-reusable.yml' .github/workflows/caller.yml
```

!!! example "Expected output"
    `caller workflow OK`


#### Task 4 – Validate pair and export reusable contract

Create `reusable-contract.yaml`:

```yaml title="reusable-contract.yaml"
# Module 14 reusable contract — machine-readable platform API
composite:
  path: .github/actions/setup-lab
  name: setup-lab
  inputs:
    lab-name:
      required: true
      type: string
  outputs:
    marker-path:
      description: Path to marker file
reusable_workflow:
  path: .github/workflows/ci-reusable.yml
  trigger: workflow_call
  inputs:
    lab-name:
      required: true
      type: string
  outputs:
    marker-path:
      from_job: build
caller:
  path: .github/workflows/caller.yml
  invokes: ./.github/workflows/ci-reusable.yml
  with:
    lab-name: module-14
pinning:
  rule: Callers pin reusable ref to tag or SHA when published cross-repo
```

Validate and archive:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-github-actions/module-14
set -euo pipefail
python3 -c "
import yaml
with open('reusable-contract.yaml') as f:
    doc = yaml.safe_load(f)
assert doc['composite']['inputs']['lab-name']['required'] is True
assert doc['reusable_workflow']['trigger'] == 'workflow_call'
assert doc['caller']['with']['lab-name'] == 'module-14'
print('reusable-contract.yaml OK')
"
tar -czf module-14-evidence.tgz .github/actions/setup-lab/action.yml .github/workflows/*.yml reusable-contract.yaml out/module-14.txt 2>/dev/null || \
tar -czf module-14-evidence.tgz .github/actions/setup-lab/action.yml .github/workflows/*.yml reusable-contract.yaml
ls -l module-14-evidence.tgz | tee evidence.txt
```

!!! example "Expected output"
    `reusable-contract.yaml OK`; evidence archive with composite + reusable + caller.


### Validation steps

- [ ] Composite `action.yml` parses
- [ ] Reusable workflow has `workflow_call` and outputs
- [ ] Caller workflow references reusable with `with:` input
- [ ] Contract YAML lists composite inputs/outputs and reusable `workflow_call` inputs

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Composite missing `shell:` | Invalid action.yml | Add `shell: bash` per step |
| Reusable not found | Wrong path/ref | Use `./.github/workflows/x.yml` locally |
| Secret not passed | Caller omitted secrets | Add `secrets: inherit` or explicit map |
| Output empty | Output not in job outputs | Wire job `outputs` to step outputs |
| `uses:` composite in wrong path | Checkout missing | Caller must checkout before local action |

### Challenge exercise

Publish the reusable workflow pattern to a second folder `module-14-consumer/` with only `caller.yml` that references `../module-14` via `workflow_call` path. Add a `validate-consumer.sh` script that greps for the reusable path and exits non-zero if missing.

### Learning outcomes

- Built composite action with inputs/outputs
- Created reusable workflow callable from caller
- Exported platform contract as validated YAML schema
- Validated all YAML offline

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
ls ~/rebash-github-actions/module-14/.github
```

## Validation

- [ ] Lab completed under `~/rebash-github-actions/module-14/`
- [ ] You can choose composite vs reusable for a scenario
- [ ] You can explain `secrets: inherit`
- [ ] You can describe pinning strategy for reusable refs

## Code Walkthrough

1. **Composite for step bundles** — setup, lint, scan snippets.
2. **Reusable for whole CI** — jobs, environments, gates.
3. **Document contract** — inputs, secrets, outputs in README.
4. **Pin refs** — SHA/tag for cross-repo callers.
5. **Checkout first** — local actions need files on disk.

## Security Considerations

- Reusable workflows run in caller context — trust platform repo owners.
- Never pass production secrets to untrusted caller repos without policy.
- Pin reusable refs — `@main` allows supply-chain swap.
- Audit composite actions for credential exfiltration (`curl` with secrets).
- Limit `workflow_call` to trusted repositories via org settings.

## Common Mistakes

!!! warning "Reusable workflow on `@main`"
    Breaking change ships silently. **Fix:** semver tags; callers pin `@v1`.

!!! warning "Composite without documented outputs"
    Callers cannot chain jobs. **Fix:** define `outputs` in `action.yml`.

!!! warning "Duplicating OIDC login in every repo"
    Drift and review burden. **Fix:** composite or reusable login job once.

!!! warning "Mega-composite doing deploy + test + scan"
    Hard to test and reuse. **Fix:** split composites by concern.

## Best Practices

- Version platform components (`v1`, `v2`) with changelog.
- Provide example caller workflow in platform repo.
- Use `workflow_call` inputs with `type:` and defaults.
- Test reusable workflows with `workflow_dispatch` in platform repo.
- Align with Module 11 SHA pinning for any external actions inside reusables.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `workflow was not found` | Path or visibility | Public repo or same org access |
| Composite step not found | Wrong `uses:` path | Relative to repo root |
| Secret empty in reusable | Not mapped | `secrets: inherit` or explicit |
| Output not available to caller | Job output not exported | Set reusable workflow `outputs` |
| Local action fails on fork | Path only on default branch | Document minimum ref |

## Summary

Composite actions bundle steps; reusable workflows bundle jobs — together they form an internal Actions platform. Callers stay thin; platform teams own pins, scans, and OIDC. Next: [Production Pipelines and Environments](production-pipelines-and-environments.md).

## Interview Questions

**1. What is the difference between a composite action and a reusable workflow?**

??? success "Reveal answer"
    Composite actions group steps that run on the caller's job runner; reusable workflows define callable jobs/workflows with their own job graph, `needs`, and environments invokable via `workflow_call`.

**2. When would you choose a composite action over a reusable workflow?**

??? success "Reveal answer"
    When you need a small reusable step bundle (setup, lint script) within a job; reusable workflows fit when standardising entire CI pipelines across repositories.

**3. How do callers pass secrets to reusable workflows?**

??? success "Reveal answer"
    Explicitly map `secrets:` in the caller job or use `secrets: inherit` to pass all available secrets — document required secret names in the platform contract.

**4. Why pin reusable workflow references by tag or SHA?**

??? success "Reveal answer"
    Floating branches (`@main`) let platform changes break all callers without review; pins make upgrades deliberate and auditable.

**5. Can composite actions define `runs-on`?**

??? success "Reveal answer"
    No — composite actions run in the context of the caller job's runner; only reusable workflows and regular jobs specify `runs-on`.

**6. How do reusable workflow outputs reach the caller?**

??? success "Reveal answer"
    Define outputs at the reusable workflow level mapping from job outputs; caller accesses via `needs.<job-id>.outputs.<name>`.

**7. What security risk do third-party reusable workflows carry?**

??? success "Reveal answer"
    They execute with access to caller secrets if passed — only use trusted org/platform repos and pin immutable refs.

**8. How do reusable workflows relate to Jenkins shared libraries?**

??? success "Reveal answer"
    Both centralise pipeline logic: shared libraries supply Groovy steps/functions; reusable workflows supply callable CI graphs — service repos invoke standard behaviour with parameters.

## Related Tutorials

- [Workflow Syntax: Matrix and Reusable Workflows](workflow-syntax-matrix-and-reusable.md)
- [Production Pipelines and Environments](production-pipelines-and-environments.md)
- [Jenkins Shared Libraries](../jenkins/shared-libraries.md)

## References

- [Composite actions](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)
- [Reuse workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Workflow syntax — workflow_call](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onworkflow_call)
