---
title: "Lab — Python Certificate Expiry Monitor"
description: "Check TLS certificate expiry for hosts or local PEM fixtures and alert when days remaining fall below a threshold."
difficulty: intermediate
estimated_time: "45–55 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - python
  - tls
  - certificates
  - monitoring
comments: false
---

# Lab — Python Certificate Expiry Monitor

## Lab Overview

**Purpose:** Detect certificates nearing expiry before browsers and API clients fail.

**Scenario:** An e-commerce edge cert expired overnight. Leadership wants a Python monitor with days-left reporting.

**Expected outcome:** CLI checks PEM fixtures and optional live TLS endpoints; exits `1` when below threshold.

!!! tip "This is a lab, not a tutorial"
    Apply [REST APIs](../python/rest-apis-requests-auth-and-resilience.md) and [Error Handling](../python/error-handling-and-exceptions.md).

## Business Scenario

Platform runs dozens of public hostnames. Manual calendar reminders failed; you need automation that CI and cron can run.

## Learning Objectives

- [ ] Parse PEM with `cryptography` or `ssl` + `datetime`
- [ ] Compute days remaining in UTC
- [ ] Support `--fixture` PEMs when network is blocked
- [ ] Threshold exit codes for alerting

## Prerequisites

### Knowledge

- [Error Handling and Exceptions](../python/error-handling-and-exceptions.md)
- [Logging and Debugging](../python/logging-and-debugging.md)

### Software

| Tool | Notes |
|------|--------|
| cryptography | recommended |
| openssl | to mint lab PEMs |

**Estimated cost:** £0.

## Environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-lab-python-certs/{fixtures,out}
cd ~/rebash-lab-python-certs
python3 -m venv .venv && source .venv/bin/activate
pip install 'cryptography>=42,<45'
```

## Initial State — create short-lived and long-lived PEMs

``` {.bash .ra-terminal title="Terminal"}
openssl req -x509 -newkey rsa:2048 -keyout fixtures/key.pem -out fixtures/soon.pem \
  -days 5 -nodes -subj "/CN=soon.example.test" 2>/dev/null
openssl req -x509 -newkey rsa:2048 -keyout /tmp/k2.pem -out fixtures/later.pem \
  -days 365 -nodes -subj "/CN=later.example.test" 2>/dev/null
```

## Task

Create `cert_monitor.py`:

- `--pem fixtures/soon.pem` / multiple paths
- `--warn-days 14` — exit `1` if any cert expires within N days
- Write `out/report.json` with `not_after` and `days_left`
- Optional `--host example.com:443` using `ssl.get_server_certificate` (skip if offline)

## Validation

``` {.bash .ra-terminal title="Terminal"}
python cert_monitor.py --pem fixtures/soon.pem --pem fixtures/later.pem --warn-days 14; echo $?  # 1
python -c 'import json; print(json.load(open("out/report.json")))'
```

- [ ] `soon.pem` triggers warning with `--warn-days 14`
- [ ] Report JSON lists both certs when both passed
- [ ] Invalid PEM exits `2`

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| openssl missing | Install or download sample PEMs from course assets |
| Timezone confusion | Always use aware UTC datetimes |

## Cleanup

```bash
deactivate 2>/dev/null || true
rm -rf ~/rebash-lab-python-certs
```

## Production Discussion

Prefer ACME automation (Let’s Encrypt) and cloud-managed certs. This monitor is a safety net, not a replacement for auto-renewal.

## Related

- Next: [Slack Notification Bot](python-slack-notification-bot.md)
