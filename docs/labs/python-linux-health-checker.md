---
title: "Lab — Python Linux Health Checker"
description: "Build a local Linux health checker using subprocess and psutil with JSON output and clear exit codes."
difficulty: beginner
estimated_time: "45–55 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - python
  - linux
  - subprocess
  - psutil
comments: false
---

# Lab — Python Linux Health Checker

## Lab Overview

**Purpose:** Collect host health signals (CPU, memory, disk, load) and emit a machine-readable report for ops automation.

**Scenario:** A platform team wants a lightweight pre-flight check before deploying batch jobs to shared Linux hosts. Shell one-liners differ between distros; they want one Python CLI.

**Expected outcome:** A CLI that reports thresholds and exits `0` (healthy) or `1` (breach), with optional JSON.

!!! tip "This is a lab, not a tutorial"
    Apply [Linux Automation — subprocess and psutil](../python/linux-automation-subprocess-and-psutil.md) and [CLI Applications](../python/cli-applications-argparse-click-typer.md).

## Business Scenario

Before a nightly ETL run, operators need a quick “is this host safe?” signal. Thresholds: disk `/` used ≥ 90%, memory used ≥ 85%, or load1 ≥ CPU count × 2 should fail the check.

## Learning Objectives

- [ ] Use `psutil` (or `/proc` via pathlib) for CPU, memory, and disk
- [ ] Call `subprocess.run` with list args for `uptime` or `df` fallback
- [ ] Emit human and JSON summaries
- [ ] Map breaches to exit code `1`
- [ ] Keep secrets and hostnames out of noisy debug logs

## Prerequisites

### Knowledge

- [Linux Automation — subprocess and psutil](../python/linux-automation-subprocess-and-psutil.md)
- [CLI Applications — argparse, Click, Typer](../python/cli-applications-argparse-click-typer.md)
- [Logging and Debugging](../python/logging-and-debugging.md)
- [Error Handling and Exceptions](../python/error-handling-and-exceptions.md)

### Software

| Tool | Notes |
|------|--------|
| Python 3.12+ | — |
| psutil | `pip install 'psutil>=5.9,<7'` |

**Estimated cost:** £0.

## Architecture

```text
CLI flags --> collect metrics (psutil) --> compare thresholds --> JSON + exit 0|1
```

## Environment

Linux or WSL2 under `~/rebash-lab-python-health`.

```bash title="Terminal"
mkdir -p ~/rebash-lab-python-health/out
cd ~/rebash-lab-python-health
python3 -m venv .venv && source .venv/bin/activate
pip install 'psutil>=5.9,<7'
```

## Initial State

No services required. Confirm baseline:

```bash title="Terminal"
python -c 'import psutil; print(psutil.cpu_count(), round(psutil.virtual_memory().percent,1))'
```

## Task

### Step 1 – CLI skeleton

Create `health_check.py` with argparse flags:

- `--json` — write `out/health.json`
- `--disk-warn` (default 90), `--mem-warn` (default 85), `--load-factor` (default 2.0)

### Step 2 – Collect metrics

Use psutil for:

- `cpu_percent(interval=0.2)`
- `virtual_memory().percent`
- `disk_usage("/").percent`
- `getloadavg()[0]` vs `cpu_count()`

### Step 3 – Evaluate and exit

Build a list of `breaches`. Exit `0` if empty, else `1`. Always print a one-line summary on stdout.

### Step 4 – Optional subprocess fallback

If psutil is missing, fall back to parsing `df -P /` with `subprocess.run([...], check=True, text=True)` — list args only.

## Validation

```bash title="Terminal"
python health_check.py --json
python health_check.py --disk-warn 1   # should exit 1 on almost any host
echo $?
```

- [ ] Healthy run exits `0` with sensible defaults on a normal laptop/VM
- [ ] Forced low thresholds exit `1` and list breaches
- [ ] `out/health.json` is valid JSON when `--json` is set
- [ ] No `shell=True` in your code

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `PermissionError` on disk | Check mount path; use `/` |
| Load average missing | macOS differs; document Linux target or skip load on Darwin |
| Flaky CPU % | Use a short `interval` or sample twice |

## Cleanup

```bash
deactivate 2>/dev/null || true
rm -rf ~/rebash-lab-python-health
```

## Production Discussion

Ship as a systemd timer or Kubernetes CronJob sidecar probe. Expose Prometheus gauges later; keep this lab’s CLI as the local contract. Never run destructive remediation from a health check without an explicit `--apply`.

## Stretch Goals

- Add inode usage via `os.statvfs`
- Emit OpenTelemetry-friendly key=value lines
- Unit-test threshold logic with mocked percentages

## Related

- Track: [Python for DevOps](../python/index.md)
- Previous: [Python Log Analyser](python-log-analyser.md)
- Next: [Python YAML Config Validator](python-yaml-config-validator.md)
- Project: [Python Log Analysis Tool](../projects/python-log-analysis-tool.md)
