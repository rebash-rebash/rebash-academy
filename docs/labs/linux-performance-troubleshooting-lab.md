---
title: "Lab — Performance Troubleshooting and Service Recovery"
description: "Induce CPU, memory, and disk pressure safely, use vmstat/iostat/ps to find the culprit, and recover a failed systemd unit under time pressure."
difficulty: intermediate
estimated_time: "55–70 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - linux
  - performance
  - troubleshooting
  - systemd
comments: false
---

# Lab — Performance Troubleshooting and Service Recovery

## Lab Overview

**Purpose:** Practise a structured performance and service recovery workflow: observe → hypothesise → prove → fix → verify.

**Scenario:** A lab host feels “slow” and `rebash-worker.service` has failed. You must find resource pressure and restore the unit.

**Expected outcome:** You identify the stressor with host tools, stop it, recover the service, and write a short incident note.

!!! tip "This is a lab, not a tutorial"
    Do not skip baselines. Capture `uptime`/`vmstat` before and after.

## Business Scenario

On-call gets a vague “API latency” ticket. The host is a single VM. You have twenty minutes to narrow CPU vs memory vs disk vs the failed worker unit.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Collect a quick performance baseline (`uptime`, `vmstat`, `free`, `df`, `iostat`)
- [ ] Find top CPU/memory consumers with `ps`/`top`
- [ ] Recover a failed systemd unit using `systemctl` and `journalctl`
- [ ] Distinguish application failure from host saturation
- [ ] Leave a reproducible timeline in the workspace

## Prerequisites

### Knowledge

- [Host Monitoring: vmstat, iostat, sar](../linux/host-monitoring-vmstat-iostat-sar.md)
- [Process Management](../linux/process-management.md)
- [Troubleshooting Linux Systems](../linux/troubleshooting-linux-systems.md)
- [systemd Services and journalctl](../linux/systemd-services-and-journalctl.md)
- [Production Linux Hardening and Performance](../linux/production-linux-hardening-and-performance.md) (skim)

### Software

| Tool | Notes |
|------|--------|
| Ubuntu | `sysstat` for `iostat`/`sar` optional but recommended |
| sudo | for units and package install |

**Estimated cost:** £0.

## Environment

```bash title="Terminal"
mkdir -p ~/rebash-lab-linux-perf
cd ~/rebash-lab-linux-perf
sudo apt-get update && sudo apt-get install -y sysstat
```

## Initial State

You will create a worker unit and optional stress scripts. Use a disposable VM — stress tools can make the desktop lag.

## Lab Tasks

### Task 1 — Baseline

```bash
{
  date -Is
  uptime
  free -h
  df -hT /
  vmstat 1 5
  iostat -xz 1 3 2>/dev/null || true
} | tee ~/rebash-lab-linux-perf/baseline.txt
```

### Task 2 — Install a flaky worker unit

```bash title="Terminal"
cat > ~/rebash-lab-linux-perf/worker.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
FLAG="${HOME}/rebash-lab-linux-perf/READY"
[[ -f "$FLAG" ]] || { echo "missing READY flag" >&2; exit 1; }
echo "$(date -Is) worker ok" >> "${HOME}/rebash-lab-linux-perf/worker.log"
exec sleep infinity
EOF
chmod +x ~/rebash-lab-linux-perf/worker.sh

sudo tee /etc/systemd/system/rebash-worker.service >/dev/null <<EOF
[Unit]
Description=REBASH lab worker
After=network.target

[Service]
Type=simple
User=$(whoami)
ExecStart=%h/rebash-lab-linux-perf/worker.sh
Restart=no

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl start rebash-worker.service || true
systemctl status rebash-worker.service --no-pager -l | tee ~/rebash-lab-linux-perf/worker-failed.txt
journalctl -u rebash-worker.service -n 20 --no-pager
```

### Task 3 — Recover the service

```bash
touch ~/rebash-lab-linux-perf/READY
sudo systemctl restart rebash-worker.service
systemctl is-active rebash-worker.service
systemctl status rebash-worker.service --no-pager | tee ~/rebash-lab-linux-perf/worker-ok.txt
```

### Task 4 — Induce CPU pressure (controlled)

```bash
# Two busy loops — stop after measurements
( dd if=/dev/zero of=/dev/null & echo $! > ~/rebash-lab-linux-perf/stress.pid )
( dd if=/dev/zero of=/dev/null & echo $! >> ~/rebash-lab-linux-perf/stress.pid )
sleep 2
ps -eo pid,pcpu,pmem,comm --sort=-pcpu | head -n 10 | tee ~/rebash-lab-linux-perf/top-cpu.txt
vmstat 1 5 | tee -a ~/rebash-lab-linux-perf/under-stress.txt
kill $(cat ~/rebash-lab-linux-perf/stress.pid) 2>/dev/null || true
```

### Task 5 — Disk pressure awareness

```bash
dd if=/dev/zero of=~/rebash-lab-linux-perf/blob.bin bs=1M count=256 status=none
iostat -xz 1 3 2>/dev/null | tee ~/rebash-lab-linux-perf/iostat.txt || true
df -h ~ | tee ~/rebash-lab-linux-perf/df.txt
rm -f ~/rebash-lab-linux-perf/blob.bin
```

### Task 6 — Incident note

Write `~/rebash-lab-linux-perf/incident.md` with: timeline, signals, root cause of worker failure, performance observations, verification.

## Validation

- [ ] Worker moved from failed → active with journal evidence
- [ ] Baseline vs stress captures differ meaningfully
- [ ] Stress PIDs were killed
- [ ] Incident note is one screen or less

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `iostat` missing | Install `sysstat`; enable data collection if needed |
| Host too laggy | Kill stress PIDs immediately; reduce loops |
| Unit still failed | `journalctl -xe`; check `READY` path and shebang |

## Challenge Extensions

- Add memory pressure with a controlled allocator; watch OOM killer logs
- Use `perf top` briefly (if available) during CPU stress
- Enable `Restart=on-failure` and show rate-limiting behaviour

## Cleanup

```bash title="Terminal"
sudo systemctl disable --now rebash-worker.service 2>/dev/null || true
sudo rm -f /etc/systemd/system/rebash-worker.service
sudo systemctl daemon-reload
kill $(cat ~/rebash-lab-linux-perf/stress.pid 2>/dev/null) 2>/dev/null || true
rm -rf ~/rebash-lab-linux-perf
```

## Production Discussion

Pair host metrics (node exporter / cloud metrics) with journals. Performance without a timeline is storytelling — always record before/after.

## Best Practices

- Baseline first
- Change one variable at a time
- Kill load generators before you leave the session

## Common Mistakes

| Mistake | Correct approach |
|---------|------------------|
| Rebooting as first step | Measure, then act |
| Ignoring disk latency | Check `iostat`/`await` |
| Fixing the app while CPU is pegged | Relieve saturation first |

## Success Criteria

You can narrate a five-minute triage: host health → top processes → unit journal → fix → verify.

## Reflection Questions

1. How do you tell CPU saturation from disk-bound wait?
2. What does a rising load average with idle CPU suggest?
3. When is reboot acceptable in production?

## Interview Connection

Whiteboard: “host is slow” — ordered checklist with tools and expected signals.

## Related Tutorials

- [Host Monitoring: vmstat, iostat, sar](../linux/host-monitoring-vmstat-iostat-sar.md)
- [Troubleshooting Linux Systems](../linux/troubleshooting-linux-systems.md)
- Lab: [Production Incident Triage](linux-production-incident-triage.md)

## References

- `man vmstat`, `man iostat`, `man systemctl`
