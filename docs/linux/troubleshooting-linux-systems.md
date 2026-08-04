---
title: "Troubleshooting Linux Systems"
description: "Linux a repeatable troubleshoot method — gather facts, narrow scope, break and fix a systemd unit, prove recovery with evidence."
difficulty: intermediate
estimated_time: "50–65 min"
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
technology: linux
module: "Module 15 · Troubleshooting"
learning_paths:
  - linux-administrator
  - devops-engineer
  - site-reliability-engineer
tags:
  - linux
  - troubleshooting
  - systemd
  - journalctl
  - beginners
prerequisites:
  - linux/containers-namespaces-cgroups-and-oci
next:
  - linux/production-linux-hardening-and-performance
related:
  - linux/systemd-services-and-journalctl
  - linux/host-monitoring-vmstat-iostat-sar
interview: interview/linux
comments: false
---

# Troubleshooting Linux Systems

## Overview

Panic looks like random command typing. Good troubleshooting looks like detective work: symptom → facts → one hypothesis → one change → proof. This tutorial builds that method on a real break-and-fix lab.

**Plain problem:** “The API is down.” Is it the app, the service unit, disk full, out of memory, or a bad deploy? Without order, you restart everything and hope — extending the outage.

This tutorial teaches a **repeatable loop** and a lab where you **break** a systemd unit, **diagnose** with logs and status commands, **fix** it, and **prove** recovery.

This is **Tutorial 15** in **Module 15: Troubleshooting** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series.

## Prerequisites

- Ubuntu VM with systemd
- [systemd Services and journalctl](systemd-services-and-journalctl.md) or equivalent comfort
- `sudo` for unit files under `/etc/systemd/system/`

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] State a troubleshooting method in plain language
- [ ] Gather first facts: time, change, disk, memory, failed units, logs
- [ ] Diagnose a failed **systemd** unit with `systemctl` and `journalctl`
- [ ] Break and fix a misconfigured unit on purpose
- [ ] Write a short incident evidence pack
- [ ] Answer fresher interview questions on Linux troubleshooting

## Architecture

Incidents flow from user-visible symptom down through service state, resources, and logs. Your job is narrowing which layer failed before changing production.

![Linux troubleshooting flow — symptom to evidence](../assets/excalidraw/linux-troubleshooting.svg)

## Theory

### The problem (before any jargon)

3 am page: “Site unreachable.” Junior restarts nginx three times. Disk was 100% full from logs — nginx was innocent. **Gather facts first** would have shown `df -h` at 0 bytes free in thirty seconds.

### The method (simple words)

**Analogy:** Doctor visit — symptoms, vitals, one test, one treatment, follow-up. Not random medicine.

| Step | Action |
|------|--------|
| 1. Symptom | What fails, for whom, since when? |
| 2. Timeline | Deploys, cron, config changes? |
| 3. Scope | One host or many? One service? |
| 4. Facts | `uptime`, `df -h`, `free -h`, failed units, logs |
| 5. Hypothesis | One likely cause |
| 6. Change | One fix at a time |
| 7. Proof | Metric/log showing recovery |
| 8. Document | What broke, why, how you fixed |

**Interview line:** “I never restart without checking `systemctl status`, `journalctl -u`, disk, and recent changes.”

### First-fact commands

``` {.bash .ra-terminal title="Terminal"}
uptime
df -h
free -h
systemctl --failed
journalctl -p err -b --no-pager | tail -30
ss -tlnp
```

### systemd failure patterns

| Signal | Tool |
|--------|------|
| Unit failed | `systemctl status app.service` |
| Why exit code | `journalctl -u app.service -b` |
| Config syntax | `systemd-analyze verify unit.file` |
| Dependency order | `systemctl list-dependencies` |

### Common pitfalls

- Restarting before reading logs (loses evidence)
- Multiple changes at once (cannot tell what worked)
- Ignoring disk/memory until late
- No written timeline for post-incident review

## Hands-on Lab

### Objective

Deploy a small **systemd** app unit, **break** it with a bad `ExecStart`, **diagnose** and **fix**, prove recovery — evidence under `~/rebash-linux/lab23`.

### Prerequisites

| Item | Notes |
|------|--------|
| Ubuntu VM | systemd |
| `sudo` | Install unit to `/etc/systemd/system/` |

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab23/bin && cd ~/rebash-linux/lab23
```

### Real-world scenario

Ticket: “`rebash-report.service` failed after deploy.” You have no prior context — only SSH. Follow the method and attach an evidence pack.

### Step-by-step tasks

#### Task 1 – Working unit and baseline

Create `report.sh`:

```bash title="report.sh"
#!/usr/bin/env bash
set -euo pipefail
echo "$(date -Is) report OK" >> /tmp/rebash-report.log
```

Create `rebash-report.service`:

```ini title="rebash-report.service"
[Unit]
Description=REBASH lab23 report oneshot

[Service]
Type=oneshot
ExecStart=/home/USER_PLACEHOLDER/rebash-linux/lab23/bin/report.sh

[Install]
WantedBy=multi-user.target
```

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab23
mkdir -p bin
cp report.sh bin/
chmod +x bin/report.sh
sed "s/USER_PLACEHOLDER/$USER/" rebash-report.service | sudo tee /etc/systemd/system/rebash-report.service >/dev/null
sudo systemctl daemon-reload
sudo systemctl enable --now rebash-report.service
systemctl status rebash-report.service --no-pager | tee status-ok.txt
test -f /tmp/rebash-report.log
tail -1 /tmp/rebash-report.log | tee log-ok.txt
```

!!! example "Expected output"
    Unit active/exited successfully; log line with timestamp in `log-ok.txt`.


#### Task 2 – Break (bad ExecStart), diagnose

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab23
sudo sed -i 's|report.sh|report-MISSING.sh|' /etc/systemd/system/rebash-report.service
sudo systemctl daemon-reload
sudo systemctl start rebash-report.service 2>&1 | tee start-broken.txt || true
systemctl status rebash-report.service --no-pager | tee status-broken.txt
journalctl -u rebash-report.service -b --no-pager | tail -15 | tee journal-broken.txt
grep -i 'failed\|error\|not found' journal-broken.txt status-broken.txt | tee diagnosis.txt
```

!!! example "Expected output"
    Status shows failed state; journal mentions missing script or exit code failure.


#### Task 3 – Fix and prove recovery

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab23
sudo sed -i 's|report-MISSING.sh|report.sh|' /etc/systemd/system/rebash-report.service
sudo systemctl daemon-reload
sudo systemctl start rebash-report.service
systemctl status rebash-report.service --no-pager | tee status-fixed.txt
journalctl -u rebash-report.service -b --no-pager | tail -5 | tee journal-fixed.txt
grep -q 'report OK' /tmp/rebash-report.log
echo "lab23 troubleshoot OK" | tee evidence.txt
```

Create `incident-summary.md`:

```markdown title="incident-summary.md"
# Incident summary — lab23

- Symptom: rebash-report.service failed after change
- Cause: ExecStart pointed to missing script path
- Fix: restored correct path, daemon-reload, start
- Proof: status-fixed.txt and new log line in /tmp/rebash-report.log
```

!!! example "Expected output"
    Service succeeds again; incident summary documents break→fix→prove.


### Validation steps

- [ ] Baseline success captured before break
- [ ] Diagnosis used `systemctl` + `journalctl` (not blind restart)
- [ ] Fix restored service with evidence files
- [ ] `incident-summary.md` completed

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Unit not found | Not daemon-reload | `sudo systemctl daemon-reload` |
| Permission denied in script | Path or perms | `chmod +x`; absolute paths |
| Empty journal | Wrong unit name | Match `-u` to unit file |
| Fix does not apply | Forgot reload | Always reload after unit edit |

### Challenge exercise

Add `systemctl --failed` output before and after fix to `failed-units.txt`.

### Learning outcomes

- You followed a structured troubleshoot loop
- You broke and fixed a real systemd unit
- You produced interview-ready incident notes

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
sudo systemctl disable --now rebash-report.service 2>/dev/null || true
sudo rm -f /etc/systemd/system/rebash-report.service
sudo systemctl daemon-reload
rm -f /tmp/rebash-report.log
```

## Validation

- [ ] Evidence under `~/rebash-linux/lab23`
- [ ] Can recite first-fact commands from memory
- [ ] Ready for production hardening next

## Code Walkthrough

1. **`Type=oneshot`** — runs script once per start; good for report/cron-style tasks.
2. **Break via ExecStart typo** — mirrors real deploy typo incidents.
3. **`journalctl -u -b`** — this boot’s unit story only.
4. **One change fix** — restore path, reload, start — scientific method.
5. **`incident-summary.md`** — habit hiring managers like in postmortems.

## Security Considerations

- Preserve logs before restart during real incidents (audit trail).
- Do not paste production secrets into ticket evidence.
- Verify you are on the correct host (`hostname`, `ip`) before fixes.
- Use sudo deliberately; document privileged changes.
- Blameless postmortems focus on process, not individuals.

## Common Mistakes

!!! warning "Restart without logs"
    Read `journalctl` first — restarting may clear transient clues (still check after too).

!!! warning "Many changes at once"
    One hypothesis, one change — otherwise you cannot explain what fixed it.

!!! warning "Skipping disk and memory"
    `df -h` and `free -h` belong in the first two minutes.

## Best Practices

- Keep a personal incident checklist (this lab)
- Correlate deploy timestamps with `journalctl --since`
- Use `systemd-analyze critical-chain` for boot delays
- Communicate status to stakeholders during long incidents
- Write timeline bullets as you go, not from memory later

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Service fails immediately | Bad ExecStart, perms | status + journal; fix path |
| Intermittent failures | OOM, disk full | `free -h`; `df -h`; dmesg OOM |
| Works manually, not in unit | Different env/user | `User=`, `Environment=`, absolute paths |
| All services slow | Host resource | vmstat/iostat from prior tutorial |

## Summary

**Troubleshooting** is a method: define symptom, gather facts (`systemctl --failed`, `journalctl`, disk, memory), change one thing, prove recovery. The lab broke a **systemd** unit on purpose — the same class of failure you will see after bad deploys. Document evidence; interviews and postmortems reward this discipline.

## Interview Questions

**1. Describe your Linux troubleshooting approach.**

??? success "Reveal answer"
    Clarify symptom and scope → check recent changes → gather facts (`uptime`, disk, memory, failed units, logs) → one hypothesis → one change → verify recovery → document timeline. Avoid random restarts without evidence.

**2. First five commands on a slow/unreachable Linux server?**

??? success "Reveal answer"
    `uptime`, `df -h`, `free -h`, `systemctl --failed`, `journalctl -p err -b` (plus `ss -tlnp` if network/service). Then narrow to the failing unit or resource.

**3. Service fails — how do you use journalctl?**

??? success "Reveal answer"
    `systemctl status unit.service` for exit code and hint, then `journalctl -u unit.service -b` (this boot), optionally `--since` around incident time. Read ExecStart failures, permissions, missing files.

**4. Why change one thing at a time?**

??? success "Reveal answer"
    Multiple simultaneous changes hide root cause and complicate rollback. Scientific method: one hypothesis, one fix, observe result — required for postmortems and safe production work.

**5. Disk full — how does it break unrelated services?**

??? success "Reveal answer"
    Many services need to write logs, temp files, or sockets under `/var` or `/tmp`. No free space → writes fail → database, web server, or systemd units fail with varied errors. Always check `df -h` early.

**6. Difference between restart and reload for diagnosis?**

??? success "Reveal answer"
    **Restart** stops and starts process (may clear in-memory state). **Reload** often re-reads config with less disruption. For diagnosis, read logs **before** restart to preserve failure evidence; restart after you understand or to verify fix.

**7. What goes in an incident evidence pack?**

??? success "Reveal answer"
    Symptom, timeline, commands run (outputs), root cause, fix applied, proof of recovery (status, log line, metric), follow-up actions. Redact secrets. Shows operational maturity in interviews.

## Related Tutorials

- Previous: [Containers — Namespaces, cgroups, and OCI](containers-namespaces-cgroups-and-oci.md)
- Next: [Production Hardening and Performance](production-linux-hardening-and-performance.md)
- Related: [systemd Services and journalctl](systemd-services-and-journalctl.md)

## References

- [systemd.service man page](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html)
- [journalctl man page](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html)
- [Google SRE incident management](https://sre.google/sre-book/managing-incidents/)
