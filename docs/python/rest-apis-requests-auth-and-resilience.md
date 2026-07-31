---
title: "REST APIs — requests, Auth, and Resilience"
description: "Call HTTP APIs with requests — methods, authentication, tokens, pagination, rate limits, timeouts, and error handling for DevOps automation."
difficulty: intermediate
estimated_time: "55–70 min"
technology: python
category: python
module: "Module 14 · REST APIs"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - requests
  - rest
  - http
prerequisites:
  - python/linux-automation-subprocess-and-psutil
next:
  - python/cloud-automation-aws-azure-gcp
related:
  - networking/http-https-and-application-layer
  - labs/python-rest-api-monitoring-service
labs:
  - labs/python-rest-api-monitoring-service
  - labs/python-certificate-expiry-monitor
  - labs/python-slack-notification-bot
projects: []
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - requests
  - rest
  - http
  - auth
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# REST APIs — requests, Auth, and Resilience

## Overview

Call REST APIs with `requests` using timeouts, auth headers, pagination loops, and basic retry/backoff for 429/5xx — without leaking tokens in logs.

Cloud control planes, GitHub, Slack, and internal platforms speak HTTP. Automation that forgets timeouts hangs runners; automation that ignores 429 burns quotas.

Complete [Linux Automation](linux-automation-subprocess-and-psutil.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 14 · REST APIs** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Linux Automation](linux-automation-subprocess-and-psutil.md)
- [Configuration and Secrets](configuration-management-and-secrets.md) — tokens via env
- Outbound HTTPS from the lab host

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Perform GET/POST with `requests` and JSON  
- [ ] Set timeouts on every call  
- [ ] Pass Bearer/token auth via headers from env  
- [ ] Paginate common list APIs  
- [ ] React to 401/403/404/429/5xx deliberately  
- [ ] Sketch exponential backoff (full patterns in Module 24)

## Architecture

This topic’s control points and relationships are shown below.

![REST API flow](../assets/excalidraw/python-rest-api-flow.svg)

## Theory

### What it is

Most cloud and platform control planes are Hypertext Transfer Protocol (HTTP) Application Programming Interfaces (APIs). The `requests` library (and similar clients) send methods (GET, POST, …), headers, and bodies, then parse JSON responses. **Resilience** means timeouts, careful retries, pagination, and treating status codes as signals — not hoping the network is perfect.

### Why it matters

DevOps scripts that call GitHub, cloud providers, or internal gateways will hit rate limits, blips, and expired tokens. Without timeouts, a hung socket blocks CI forever. Without backoff, a 429 storm can lock you out. Without auth hygiene, Bearer tokens end up in logs. Mastering HTTP clients is the foundation for every later SDK module (they are thin wrappers over the same ideas).

### How it works

Build a request with method, URL, headers, and optional JSON body. Always set **`timeout`** (connect and read, or a single float). Call `raise_for_status()` when failure should abort, or branch on status for probes. Authenticate with `Authorization: Bearer …` (or provider-specific headers) loaded from the environment — never hard-coded. Paginate with link headers or page tokens; cap max pages. On 429, honour `Retry-After` when present; on 5xx, retry with a small cap; on 401/403, fail fast.

```python
import os
import requests

r = requests.get(
    "https://httpbin.org/get",
    headers={"Authorization": f"Bearer {os.environ['API_TOKEN']}"},
    timeout=(3, 10),
)
r.raise_for_status()
data = r.json()
```

### Key concepts and comparisons

| Method | Ops use |
|--------|---------|
| GET | Inventory, status |
| POST | Create webhook / event |
| PUT / PATCH | Update resources |
| DELETE | Tear down (dry-run first) |

| Status | Action |
|--------|--------|
| 401 / 403 | Fail fast — credentials or permissions |
| 404 | Often expected for existence probes |
| 429 | Backoff and retry |
| 5xx | Retry with cap; then fail |

OAuth device/code flows vary by provider: obtain a token, then use Bearer like any other API.

### Common pitfalls

- Omitting `timeout` (default is “wait forever”).  
- Retrying non-idempotent POST without idempotency keys.  
- Logging full response bodies that contain secrets.  
- Following unbounded pagination until memory or rate limits explode.  
- Treating every exception as retryable (DNS failures vs 403).

## Hands-on Lab

**Focus:** practise the core workflow for REST APIs — requests, Auth, and Resilience

```bash
mkdir -p ~/rebash-python/module-14
cd ~/rebash-python/module-14

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install 'requests==2.32.3'
```

### Step 1 – GET with timeout

```bash
cd ~/rebash-python/module-14
source .venv/bin/activate

cat > fetch.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import sys

import requests


def main() -> int:
    url = "https://httpbin.org/get"
    try:
        r = requests.get(url, timeout=10)
    except requests.RequestException as exc:
        print(f"error: request failed: {exc}", file=sys.stderr)
        return 1
    if r.status_code >= 400:
        print(f"error: HTTP {r.status_code}", file=sys.stderr)
        return 1
    data = r.json()
    print(data.get("url", url))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python fetch.py
```

### Step 2 – Auth header pattern (no real secret printed)

```bash
python - <<'PY'
import os, requests
token = os.environ.get("API_TOKEN", "dummy-lab-token")
r = requests.get(
    "https://httpbin.org/headers",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)
# httpbin echoes headers — redact in real tools!
auth = r.json()["headers"].get("Authorization", "")
print("auth_present=", auth.startswith("Bearer "))
print("do_not_log_token_in_production")
PY
```

### Step 3 – Status handling

```bash
python - <<'PY'
import requests
for code in (200, 404, 500):
    r = requests.get(f"https://httpbin.org/status/{code}", timeout=10)
    print(code, r.status_code)
PY
```

### Step 4 – Tiny retry on 503

```bash
cat > retry_get.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import sys
import time

import requests


def get_with_retry(url: str, attempts: int = 3) -> requests.Response:
    last: requests.Response | None = None
    for i in range(1, attempts + 1):
        last = requests.get(url, timeout=10)
        if last.status_code < 500 and last.status_code != 429:
            return last
        sleep = 2 ** (i - 1)
        print(f"retry {i} sleep={sleep}s status={last.status_code}", file=sys.stderr)
        time.sleep(sleep)
    assert last is not None
    return last


def main() -> int:
    r = get_with_retry("https://httpbin.org/status/200")
    print(r.status_code)
    return 0 if r.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python retry_get.py
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-14/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **REST APIs — requests, Auth, and Resilience** always combines:

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

!!! warning "Omitting `timeout` (default is “wait forever”).  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Retrying non-idempotent POST without idempotency keys.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode REST APIs — requests, Auth, and Resilience changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Hang forever | No timeout | Add `timeout=` |
| 401 loop | Bad/expired token | Refresh; check scopes |
| SSL errors | Corporate proxy/MITM | Install corp CA; document |

## Summary

- `requests` + timeouts + explicit status handling  
- Tokens from env; never log Authorization  
- Paginate with caps; backoff on 429/5xx  
- Labs: monitoring, certs, Slack bots

## Interview Questions

1. How does **REST APIs — requests, Auth, and Resilience** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Cloud Automation — AWS, Azure, and GCP](cloud-automation-aws-azure-gcp.md)  
- [REST API Monitoring lab](../labs/python-rest-api-monitoring-service.md)

## References

- [requests](https://requests.readthedocs.io/)  
- [RFC 9110 HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110)
