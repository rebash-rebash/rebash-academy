---
title: "Lab — Parse JSON with jq"
description: "Query and transform API/config JSON with jq inside Bash automation scripts."
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

# Lab — Parse JSON with jq

## Lab Overview

**Purpose:** Use jq to extract fields and build reports from JSON payloads.

**Scenario:** A status API returns JSON; ops wants a shell summary for Slack paste without Python.

**Expected outcome:** A working script under `~/rebash-lab-shell` with clear exit codes, stderr logging, and validation steps you can re-run.

!!! tip "This is a lab, not a tutorial"
    Apply [Shell Scripting](../shell/index.md) skills. Prefer small verified steps over rewriting everything at once.

## Business Scenario

You parse a sample `status.json` and emit a compact table of service health.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Select fields with jq filters
- [ ] Iterate arrays safely from Bash
- [ ] Handle missing keys without breaking strict mode
- [ ] Produce a CSV or text summary

## Prerequisites

### Knowledge

- [JSON and YAML with jq and yq](../shell/json-and-yaml-with-jq-yq.md)
- [Input/Output Redirection and Pipes](../shell/input-output-redirection-and-pipes.md)

### Software

| Tool | Notes |
|------|--------|
| Bash | required |
| jq | required |

**Estimated cost:** £0.

## Environment

Any host with jq installed.

## Initial State

Create `status.json`:

```json
{
  "env": "lab",
  "services": [
    {"name": "api", "status": "ok", "latency_ms": 42},
    {"name": "worker", "status": "degraded", "latency_ms": 180},
    {"name": "db", "status": "ok", "latency_ms": 15}
  ]
}
```

Run:

```bash
mkdir -p ~/rebash-lab-shell/json
cd ~/rebash-lab-shell/json
```


## Lab Tasks

### Task 1 — Basic queries

```bash
jq -r '.env' status.json
jq -r '.services[] | select(.status!="ok") | .name' status.json
```

### Task 2 — Script `summarise-status.sh`

- Print service name, status, latency
- Exit 2 if any service is not `ok`
- Use `jq -r` and quote variables

### Task 3 — Mapfile pattern (avoid array length macros)

Prefer streaming:

```bash
jq -r '.services[] | [.name,.status,.latency_ms] | @tsv' status.json \
  | while IFS=$'\t' read -r name status latency; do
      printf '%-10s %-10s %s\n' "$name" "$status" "$latency"
    done
```


## Validation

- [ ] Summary prints all services
- [ ] Degraded service causes exit 2
- [ ] Missing file exits non-zero with a clear message

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|----------------|------------|
| jq: command not found | Not installed | Install jq via package manager |
| Strict mode fails on empty | Command substitution empty | Handle empty selects explicitly |

## Cleanup

```bash
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
- [`Input Output Redirection And Pipes`](../shell/input-output-redirection-and-pipes.md)
- [`Text Processing In Shell Scripts`](../shell/text-processing-in-shell-scripts.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Interview: [Shell Scripting](../interview/shell.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
- Track: [Shell Scripting](../shell/index.md)
