---
title: "Lab — Parse YAML with yq"
description: "Read and validate YAML config with yq, then drive shell automation from values."
difficulty: intermediate
estimated_time: "40–50 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - shell
  - bash
comments: false
---

# Lab — Parse YAML with yq

## Lab Overview

**Purpose:** Drive Bash automation from YAML configuration using yq.

**Scenario:** App config lives in `app.yaml`; a deploy wrapper must read image tag and replica count.

**Expected outcome:** A working script under `~/rebash-lab-shell` with clear exit codes, stderr logging, and validation steps you can re-run.

!!! tip "This is a lab, not a tutorial"
    Apply [Shell Scripting](../shell/index.md) skills. Prefer small verified steps over rewriting everything at once.

## Business Scenario

You validate required keys and export shell variables for a mock deploy step.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Install/use mikefarah yq (v4+) or document distro package
- [ ] Read nested keys
- [ ] Fail if required keys missing
- [ ] Pass values into a downstream command safely

## Prerequisites

### Knowledge

- [JSON and YAML with jq and yq](../shell/json-and-yaml-with-jq-yq.md)
- [Production Shell Scripting](../shell/production-shell-scripting.md)

### Software

| Tool | Notes |
|------|--------|
| Bash | required |
| yq | mikefarah/yq v4 preferred |

**Estimated cost:** £0.

## Environment

Host with yq available.

## Initial State

Create `app.yaml`:

```yaml title="app.yaml"
app:
  name: payments
  image: ghcr.io/example/payments
  tag: "1.4.2"
  replicas: 3
  healthcheck:
    path: /healthz
```

Run:

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-lab-shell/yaml
cd ~/rebash-lab-shell/yaml
```


## Lab Tasks

### Task 1 — Query with yq

``` {.bash .ra-terminal title="Terminal"}
yq -r '.app.name' app.yaml
yq -r '.app.tag' app.yaml
yq -r '.app.replicas' app.yaml
```

### Task 2 — `read-config.sh`

Export or print:

- `APP_NAME`
- `IMAGE` (image:tag)
- `REPLICAS`

Exit 2 if any required key is null/missing (`yq` + test).

### Task 3 — Mock deploy

```bash
./read-config.sh
# prints: deploy payments ghcr.io/example/payments:1.4.2 replicas=3
```


## Validation

- [ ] Required keys validated
- [ ] Image reference includes tag
- [ ] Broken YAML causes non-zero exit

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|----------------|------------|
| Wrong yq (Python yq) | Different CLI | Prefer mikefarah yq; document version |
| Numbers become strings | Quoting | Keep replicas unquoted in YAML if needed |

## Cleanup

``` {.bash .ra-terminal title="Terminal"}
rm -rf ~/rebash-lab-shell
```

## Stretch Goals

- Add a `--dry-run` mode that prints actions without changing the system
- Emit a machine-readable `RESULT status=...` line on stdout for CI
- Schedule the script with cron or a systemd timer

## Production Discussion

In production, wrap scripts with lock files, structured logging, explicit `PATH`, and documented exit codes. Prefer configuration files over hard-coded hosts and thresholds. Never embed secrets in scripts — use environment variables or a secrets manager.

## Best Practices

- Use `#!/usr/bin/env bash` and `set -euo pipefail`
- Quote every expansion that may contain spaces
- Log diagnostics to stderr; keep stdout for data
- Prefer absolute paths in scheduled jobs
- Validate inputs before destructive actions

## Common Mistakes

| Mistake | Why it happens | Correct approach |
|---------|----------------|------------------|
| Unquoted paths | Habit from interactive shell | Always `"$var"` |
| Missing `pipefail` | Default Bash pipeline behaviour | `set -o pipefail` |
| Interactive-only PATH | Cron/systemd minimal env | Set `PATH=` at top |
| Skipping dry-run | Time pressure | Default to dry-run for risky ops |

## Success Criteria

- [ ] Script runs under Bash with strict mode
- [ ] Validation and failure paths are tested
- [ ] Exit codes are documented
- [ ] Cleanup leaves no lab artefacts (or documents what remains)

## Reflection Questions

1. What would break if this ran under `/bin/sh` (dash) instead of Bash?
2. How would you make the script idempotent?
3. How would you secure credentials and host inventories?
4. How would you observe failures in production?

## Interview Connection

Interviewers often ask about quoting, exit codes, cron environment differences, and how you prevent overlapping jobs. Be ready to walk through a small script and explain failure modes.

## Related Tutorials

- [`Json And Yaml With Jq Yq`](../shell/json-and-yaml-with-jq-yq.md)
- [`Production Shell Scripting`](../shell/production-shell-scripting.md)
- [`Variables Quoting And Arithmetic`](../shell/variables-quoting-and-arithmetic.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Interview: [Shell Scripting](../interview/shell.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
- Track: [Shell Scripting](../shell/index.md)
