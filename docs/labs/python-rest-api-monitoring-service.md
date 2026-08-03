---
title: "Lab — Python REST API Monitoring Service"
description: "Poll HTTP endpoints for availability and latency with concurrency — fixture mode records synthetic results without network."
difficulty: intermediate
estimated_time: "50–60 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - python
  - http
  - monitoring
  - asyncio
comments: false
---

# Lab — Python REST API Monitoring Service

## Lab Overview

**Purpose:** Check a list of HTTP endpoints for status code and latency; emit a summary suitable for alerting.

**Scenario:** Product APIs degrade regionally. You need a small monitor that can run in CI with fixtures and live against staging.

**Expected outcome:** CLI reads targets YAML; `--fixture` synthesises results; live mode uses timeouts and optional concurrency.

!!! tip "This is a lab, not a tutorial"
    Apply [REST APIs](../python/rest-apis-requests-auth-and-resilience.md) and [Concurrency — threads, asyncio, and futures](../python/concurrency-threads-asyncio-and-futures.md).

## Business Scenario

Status page data is manual. Engineering wants automated probes every five minutes with a JSON artefact for Grafana or Slack.

## Learning Objectives

- [ ] Load targets from YAML
- [ ] Enforce connect/read timeouts
- [ ] Use ThreadPoolExecutor or asyncio for concurrent probes
- [ ] Fixture mode for offline CI

## Prerequisites

### Knowledge

- [REST APIs — requests, auth, and resilience](../python/rest-apis-requests-auth-and-resilience.md)
- [Concurrency — threads, asyncio, and futures](../python/concurrency-threads-asyncio-and-futures.md)

### Software

httpx. **Estimated cost:** £0.

## Environment

```bash title="Terminal"
mkdir -p ~/rebash-lab-python-monitor/{fixtures,out}
cd ~/rebash-lab-python-monitor
python3 -m venv .venv && source .venv/bin/activate
pip install 'httpx>=0.27,<1' 'PyYAML>=6.0,<7'
```

## Initial State

Create `targets.yaml`:

```yaml title="targets.yaml"
targets:
  - name: httpbin-get
    url: https://httpbin.org/status/200
    expect: 200
  - name: httpbin-404
    url: https://httpbin.org/status/404
    expect: 200
```

Create `fixtures/results.json`:

```json title="results.json"
[
  {"name": "httpbin-get", "ok": true, "status": 200, "latency_ms": 120},
  {"name": "httpbin-404", "ok": false, "status": 404, "latency_ms": 110}
]
```

## Task

`monitor_apis.py --targets targets.yaml --fixture fixtures/results.json` writes `out/report.json` and exits `1` if any `ok` is false. Live mode without `--fixture` probes URLs concurrently with timeout 5s.

## Validation

```bash title="Terminal"
python monitor_apis.py --targets targets.yaml --fixture fixtures/results.json; echo $?  # 1
```

- [ ] Fixture mode offline
- [ ] Failed expect → non-zero exit
- [ ] Timeouts configured in live code path

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Live probes hang | Missing timeout |
| SSL errors | Document corporate proxies; use fixtures |

## Cleanup

```bash
deactivate 2>/dev/null || true
rm -rf ~/rebash-lab-python-monitor
```

## Production Discussion

Graduate to blackbox exporters / Synthetics. Keep this service for custom business probes and learning concurrency patterns.

## Related

- Next: [Secrets Scanner](python-secrets-scanner.md)
