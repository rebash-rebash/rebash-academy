---
title: "Network Automation and Monitoring"
description: "Automate network checks with a bash probe script, write timestamped metrics, and alert when latency or failure thresholds are crossed."
difficulty: intermediate
estimated_time: "45–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: networking
technology: networking
module: "Module 16 · Production Networking"
tags:
  - networking
  - automation
  - monitoring
  - observability
prerequisites:
  - networking/network-segmentation-and-trust-boundaries
next:
  - networking/production-dns-operations
related:
  - networking/network-incident-response-and-observability
  - networking/linux-networking-toolkit
labs: []
interview: interview/networking
comments: false
---

# Network Automation and Monitoring

## Overview

**Network automation** manages connectivity configuration as code — routes, Security Groups, DNS records, load balancer listeners — through pull requests and plan/apply. **Monitoring** watches reachability, errors, latency, and saturation so drift and denials show up before customers open tickets. Together they turn “ping when someone complains” into continuous proof.

In Cloud and DevOps work you encode VPC and firewall intent in Infrastructure as Code (IaC), reject dangerous opens with policy checks, and run synthetic probes against critical URLs. Golden signals still apply: traffic, errors, latency, and saturation — plus correctness checks (DNS and TLS expiry).

In production, automation without monitoring is a green pipeline that misses outages. Monitoring without automation means you see the fire and fix it by hand under stress. Alert noise trains teams to ignore pages; thresholds and runbooks matter as much as the probe itself.

This is **Tutorial 23** in **Module 16: Production Networking** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series. It is written for Cloud, DevOps, Platform, and SRE engineers. By the end you will run a probe script that writes timestamped metrics and raises a simple threshold alert under `~/rebash-networking/lab23`.

## Prerequisites

- [Network Segmentation and Trust Boundaries](network-segmentation-and-trust-boundaries.md)
- Practice Ubuntu/Debian host with `bash`, `curl`, `ping`, `ss`
- Basic IaC familiarity helpful (theory); lab is local probes only

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] List network objects that belong in IaC and pull requests
- [ ] Choose useful signals for path health (not only ICMP)
- [ ] Build a bash probe using `curl`, `ping`, and `ss`
- [ ] Append timestamped metrics to a file
- [ ] Alert when a latency or failure threshold is crossed
- [ ] Avoid noisy alerts without runbooks

## Architecture

Probes and exporters feed metrics and alerts; humans keep runbooks next to thresholds.

![Network observability](../assets/excalidraw/network-observability.svg)

## Theory

### What it is

Automation expresses desired network state in code. Monitoring continuously checks that the live path still matches intent. Synthetics hit a URL or TCP port from outside or from another VPC so you notice DNS, routing, and certificate failures that host CPU metrics miss.

```bash
# Minimal synthetic idea
curl -o /dev/null -sS -w '%{http_code} %{time_total}\n' https://example.com
```

### Why it matters

Click-ops networking drifts and cannot be reviewed. Forgotten open rules become breaches; missing routes become Sev-1s. A probe with a timestamped metrics file is the smallest SRE habit that scales into Prometheus later.

### How it works

1. **Encode intent** — Terraform/OpenTofu or cloud APIs for routes, SG/NSG, DNS, LB.
2. **Review blast radius** — `plan` in PRs; policy-as-code blocks `0.0.0.0/0` on data ports.
3. **Probe** — ICMP for coarse reachability; HTTP/TCP for user paths; `ss` for local listeners.
4. **Record** — timestamp, target, result, latency.
5. **Alert** — threshold on failure count or latency; link a runbook.
6. **Improve** — export the same metrics to a real TSDB when the team is ready.

| Automate in PRs | Why |
|-----------------|-----|
| Routes, SG/NSG | Reviewable blast radius |
| DNS records | TTL and rollback discipline |
| LB listeners / target groups | Safe deploys |
| Probe configs / alert thresholds | Same review as code |

| Signal | Example |
|--------|---------|
| Reachability | ping / TCP connect success |
| Latency | `curl` `time_total` |
| Errors | HTTP 5xx, connect failures |
| Saturation | NAT bytes, conntrack, LB capacity |
| Correctness | DNS answer, TLS `notAfter` |

### Common pitfalls

- Alerting only on ping while HTTPS is broken
- No timestamps — cannot correlate with deploys
- Thresholds copied from another app without baselining
- Automating applies without a dry-run/plan gate
- Pages with no runbook link

## Hands-on Lab

### Objective

Write `net-probe.sh` that probes a target with `ping` and `curl`, records timestamped metrics, and prints an alert when failure or latency crosses a threshold. Save runs under `~/rebash-networking/lab23`.

### Prerequisites

- `bash`, `curl`, `ping`, `ss`, `python3` optional
- Outbound HTTPS to `example.com` (or set your own target)

### Lab environment

Workspace: `~/rebash-networking/lab23`

```bash
mkdir -p ~/rebash-networking/lab23 && cd ~/rebash-networking/lab23
set -euo pipefail
whoami | tee admin-user.txt
command -v curl ping ss | tee tools.txt
```

**Expected output:** tools listed; workspace ready.

### Real-world scenario

Your team lacks Prometheus for a small environment but still needs a cron-friendly probe for the public marketing site and a local listener check on the jump host. You ship a bash probe with a metrics file and a clear alert line that can later feed a proper monitoring stack.

### Step-by-step tasks

#### Task 1 – Create the probe script

```bash
cd ~/rebash-networking/lab23
set -euo pipefail

cat > net-probe.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

TARGET_HOST="${TARGET_HOST:-example.com}"
TARGET_URL="${TARGET_URL:-https://example.com}"
METRICS_FILE="${METRICS_FILE:-metrics.tsv}"
MAX_LATENCY_S="${MAX_LATENCY_S:-2.0}"
PING_COUNT="${PING_COUNT:-2}"

ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
ping_ok=0
http_code="000"
time_total="0"
alert="none"

if ping -c "$PING_COUNT" -W 2 "$TARGET_HOST" >/tmp/net-probe-ping.$$ 2>&1; then
  ping_ok=1
fi

# curl timings; keep going on HTTP errors
set +e
curl_out="$(curl -o /dev/null -sS --max-time 10 \
  -w '%{http_code} %{time_total}' "$TARGET_URL" 2>/tmp/net-probe-curl-err.$$)"
curl_rc=$?
set -e
if [[ "$curl_rc" -eq 0 ]]; then
  http_code="$(awk '{print $1}' <<<"$curl_out")"
  time_total="$(awk '{print $2}' <<<"$curl_out")"
else
  http_code="000"
  time_total="0"
fi

listeners="$(ss -lnt 2>/dev/null | wc -l | tr -d ' ')"

# Thresholds: fail if ping fails, HTTP not 2xx/3xx, or latency high
python3 - "$time_total" "$MAX_LATENCY_S" "$ping_ok" "$http_code" <<'PY' > /tmp/net-probe-alert.$$
import sys
latency, max_lat, ping_ok, code = sys.argv[1:5]
alerts = []
if ping_ok != "1":
    alerts.append("ping_fail")
if not (code.startswith("2") or code.startswith("3")):
    alerts.append(f"http_{code}")
try:
    if float(latency) > float(max_lat):
        alerts.append("latency_high")
except ValueError:
    alerts.append("latency_parse")
print(",".join(alerts) if alerts else "none")
PY
alert="$(cat /tmp/net-probe-alert.$$)"

if [[ ! -f "$METRICS_FILE" ]]; then
  printf 'timestamp\ttarget_host\tping_ok\thttp_code\ttime_total_s\tlisteners\talert\n' > "$METRICS_FILE"
fi
printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
  "$ts" "$TARGET_HOST" "$ping_ok" "$http_code" "$time_total" "$listeners" "$alert" \
  | tee -a "$METRICS_FILE"

if [[ "$alert" != "none" ]]; then
  echo "ALERT: ${alert} target=${TARGET_URL} latency=${time_total}s" | tee -a alert.log
  exit 2
fi
echo "OK: http=${http_code} latency=${time_total}s"
rm -f /tmp/net-probe-ping.$$ /tmp/net-probe-curl-err.$$ /tmp/net-probe-alert.$$
EOF
chmod +x net-probe.sh
```

**Expected output:** executable `net-probe.sh` exists.

#### Task 2 – Run successful probe and inspect metrics

```bash
cd ~/rebash-networking/lab23
set -euo pipefail

TARGET_HOST=example.com TARGET_URL=https://example.com MAX_LATENCY_S=5.0 \
  ./net-probe.sh | tee probe-ok.txt

test -s metrics.tsv
tail -n 3 metrics.tsv | tee metrics-tail.txt
grep -E 'timestamp|example.com' metrics.tsv >/dev/null
```

**Expected output:** metrics row appended; probe prints `OK` (or `ALERT` if the network blocks outbound HTTPS — then note it and continue with Task 3 using a local target).

#### Task 3 – Force a threshold alert

```bash
cd ~/rebash-networking/lab23
set -euo pipefail

# Extremely low latency budget forces latency_high (or http failure if blocked)
set +e
TARGET_HOST=example.com TARGET_URL=https://example.com MAX_LATENCY_S=0.0001 \
  ./net-probe.sh | tee probe-alert.txt
rc=$?
set -e
test "$rc" -eq 2
grep -q 'ALERT:' probe-alert.txt
grep -q 'latency_high\|http_' metrics.tsv
test -s alert.log

tar -czf monitoring-evidence.tgz \
  admin-user.txt tools.txt net-probe.sh metrics.tsv alert.log \
  probe-ok.txt probe-alert.txt metrics-tail.txt
ls -l monitoring-evidence.tgz | tee evidence-ls.txt
```

**Expected output:** exit code `2` with an `ALERT` line; `alert.log` and archive exist.

### Validation steps

- [ ] `metrics.tsv` has a header and at least two data rows
- [ ] Probe exits `0`/`OK` on a sane threshold and `2` on a tight threshold
- [ ] `ss` listener count is recorded in each metrics row
- [ ] Evidence archive under `~/rebash-networking/lab23`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `curl: (6) Could not resolve host` | DNS/network blocked | Use a reachable target or lab HTTP server |
| Always ALERT on HTTP 000 | Egress filtered | Point `TARGET_URL` at a local `python3 -m http.server` |
| `python3: not found` | Minimal image | Install python3 or simplify alert math with `awk` |
| Metrics file grows forever | No rotation | Truncate in lab; use logrotate in production |

### Challenge exercise

Add a `-c` / cron mode note in script comments and a second check: fail if `ss -lnt` does not show a chosen local port (start `python3 -m http.server 18080` and set `REQUIRE_LOCAL_PORT=18080`). Save `challenge-metrics.tsv` from one run.

### Learning outcomes

- Built an executable network probe with metrics and alerts
- Separated reachability, HTTP status, and latency signals
- Packed evidence suitable for an ops handover

### Cleanup

```bash
cd ~/rebash-networking/lab23
set -euo pipefail
# Optional: rm -f monitoring-evidence.tgz metrics.tsv alert.log
pkill -f 'http.server 18080' 2>/dev/null || true
true
```

## Validation

- [ ] Lab finished under `~/rebash-networking/lab23/`
- [ ] You can explain why ping-only monitoring is incomplete
- [ ] You know which network objects belong in IaC
- [ ] You can describe how this probe graduates to Prometheus later

## Code Walkthrough

Production network automation/monitoring usually follows:

1. **Plan in PRs** — never silent console changes for SG/DNS/LB
2. **Probe user paths** — HTTPS and DNS, not only ICMP
3. **Timestamp everything** — correlate with deploys
4. **Alert with thresholds + runbooks** — avoid noise
5. **Least privilege** — automation roles cannot open `0.0.0.0/0` without review

## Security Considerations

- Probe credentials and tokens are privileged — store in a secret manager
- Synthetics should use least privilege accounts
- Metrics may reveal internal URLs — restrict who can read them
- Automation apply roles need strong change control
- Do not scrape secrets from process lists into metrics files

## Common Mistakes

!!! warning "Ping green, customers down"
    ICMP may work while HTTPS or DNS fails. **Fix:** probe the real user URL and record HTTP code + latency.

!!! warning "Alert storms on a bad threshold"
    Teams silence the pager. **Fix:** baseline first; alert on sustained failures; attach a runbook URL.

!!! warning "Automating firewall opens without policy checks"
    Pipelines can ship dangerous rules quickly. **Fix:** OPA/Conftest or provider policies on plans.

!!! warning "No timestamps in homemade scripts"
    You cannot align with deploy times. **Fix:** always write UTC timestamps in metrics rows.

## Best Practices

- Treat probe configs as code next to Terraform
- Separate paging alerts from ticket-only warnings
- Monitor TLS certificate expiry for edge names
- Use Flow Logs when probes fail but routes look fine
- Destroy lab resources; tag cloud monitors with owners

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Probe flapping | Threshold too tight / wifi lab | Raise latency budget; average samples |
| HTTP 000 | Proxy/egress/DNS | Check `curl -v`; fix resolver |
| Metrics missing rows | `set -e` exit before append | Keep append before hard exit; use alert exit after write |
| CI green, prod down | Probe only hits staging | Probe production URLs from an external vantage point |

## Summary

Automate network intent in pull requests and prove live paths with probes, metrics, and thresholds. A small bash probe is a valid starting point for SRE discipline. Next, operate DNS cutovers safely in [Production DNS Operations](production-dns-operations.md).

## Interview Questions

**1. Which network objects should always be managed as code?**

??? success "Reveal answer"
    Routes, Security Groups/NSGs, DNS records, load balancer listeners/target groups, and firewall change requests. These define blast radius and need review, history, and rollback.

**2. Why is ICMP ping alone a weak production check?**

??? success "Reveal answer"
    Many paths allow ping while HTTP, TLS, or DNS is broken — or block ping while the app works. Probe the **user path** (HTTPS status and latency) and keep ping as a coarse signal only.

**3. What are useful golden signals for a load balancer or NAT?**

??? success "Reveal answer"
    Healthy host count, 5xx rate, latency, connection errors, and saturation (bytes/conntrack/port consumption). For NAT: bytes, port allocation errors, and AZ imbalance.

**4. How do you avoid alert noise for network synthetics?**

??? success "Reveal answer"
    Baseline latency, alert on **sustained** failures (not one blip), separate paging from tickets, and link a runbook. Review flapping probes weekly.

**5. What should a network change pipeline verify after apply?**

??? success "Reveal answer"
    Plan/diff before apply, policy checks against dangerous opens, then post-apply probes (reachability + HTTP) and a clear rollback path (previous IaC commit).

**6. How would you explain your lab probe in an interview?**

??? success "Reveal answer"
    Show `metrics.tsv` with UTC timestamps, ping + curl fields, and an alert when latency or HTTP status crosses a threshold. Explain that production would export the same ideas to Prometheus/CloudWatch with dashboards and runbooks.

**7. Automation applied a Security Group rule that opened a data port. How do you prevent a repeat?**

??? success "Reveal answer"
    Add **policy-as-code** on plans (deny `0.0.0.0/0` on data ports), require dual review for firewall modules, and alert on drift between IaC and live rules.

## Related Tutorials

- [Networking for Cloud & DevOps – Overview](index.md)
- [Network Segmentation and Trust Boundaries](network-segmentation-and-trust-boundaries.md) *(previous)*
- [Production DNS Operations](production-dns-operations.md) *(next)*
- [Linux Networking Toolkit](linux-networking-toolkit.md)
- [Network Incident Response and Observability](network-incident-response-and-observability.md)

## References

- [Google SRE — Monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [`curl(1)` write-out variables](https://curl.se/docs/manpage.html)
- Track index: [Networking for Cloud & DevOps Engineers](index.md)
