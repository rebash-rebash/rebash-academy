---
title: "Lab — Python Slack Notification Bot"
description: "Send formatted ops alerts to Slack via webhook — dry-run prints the payload when no webhook URL is configured."
difficulty: intermediate
estimated_time: "40–50 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - python
  - slack
  - webhooks
  - notifications
comments: false
---

# Lab — Python Slack Notification Bot

## Lab Overview

**Purpose:** Post structured operational alerts to Slack Incoming Webhooks with dry-run safety.

**Scenario:** Cert monitor and health checks need a shared notifier. Tokens must never be committed.

**Expected outcome:** CLI builds a Slack payload; `--dry-run` (default) prints JSON; `--send` posts only if `SLACK_WEBHOOK_URL` is set.

!!! tip "This is a lab, not a tutorial"
    Apply [REST APIs — requests, auth, and resilience](../python/rest-apis-requests-auth-and-resilience.md) and [Configuration Management and Secrets](../python/configuration-management-and-secrets.md).

## Business Scenario

On-call misses email. Slack `#ops-alerts` is the team inbox — but pasting secrets into scripts caused an incident.

## Learning Objectives

- [ ] Build Block Kit or simple text payloads
- [ ] Default dry-run; explicit `--send`
- [ ] Read webhook from env only
- [ ] Timeouts on HTTP POST

## Prerequisites

### Knowledge

- [REST APIs — requests, auth, and resilience](../python/rest-apis-requests-auth-and-resilience.md)
- [Configuration Management and Secrets](../python/configuration-management-and-secrets.md)

### Software

httpx/requests. Optional real webhook. **Estimated cost:** £0.

## Environment

```bash
mkdir -p ~/rebash-lab-python-slack/out
cd ~/rebash-lab-python-slack
python3 -m venv .venv && source .venv/bin/activate
pip install 'httpx>=0.27,<1'
```

## Initial State

No webhook required. Optionally export a test webhook for live send.

## Task

Create `slack_notify.py`:

```bash
python slack_notify.py --title "Disk warning" --text "/ at 92%" --severity warning
# default dry-run writes out/payload.json
python slack_notify.py --title "Disk warning" --text "/ at 92%" --send  # needs SLACK_WEBHOOK_URL
```

Refuse `--send` without env var (exit `2`). Redact webhook in logs (show only last 4 chars if you must log).

## Validation

```bash
python slack_notify.py --title "Test" --text "hello"
test -f out/payload.json
SLACK_WEBHOOK_URL= python slack_notify.py --title t --text x --send; echo $?  # 2
```

- [ ] Dry-run writes payload without network
- [ ] `--send` without URL exits `2`
- [ ] HTTP client uses a timeout

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| 403 from Slack | Webhook revoked — rotate; stay on dry-run for the lab |
| Leaked URL in git | Use env; add secret scanning (next labs) |

## Cleanup

```bash
deactivate 2>/dev/null || true
rm -rf ~/rebash-lab-python-slack
unset SLACK_WEBHOOK_URL
```

## Production Discussion

Prefer Slack apps with granular scopes over immortal webhooks where possible; rate-limit noisy alerts; route by severity.

## Related

- Next: [REST API Monitoring Service](python-rest-api-monitoring-service.md)
