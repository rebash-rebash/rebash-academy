---
title: "Lab — Manage Services and Analyse Logs"
description: "Install a lab systemd unit, manage it with systemctl, and triage failures with journalctl and logrotate awareness."
difficulty: intermediate
estimated_time: "50–60 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - linux
  - systemd
  - journalctl
  - logging
comments: false
---

# Lab — Manage Services and Analyse Logs

## Lab Overview

**Purpose:** Operate systemd units and read journals the way on-call engineers do.

**Scenario:** `rebash-heartbeat.service` should emit a heartbeat every minute. It will fail once so you can practise journal triage.

**Expected outcome:** The unit is enabled and healthy; you can extract failure timestamps and a root-cause note from the journal.

!!! tip "This is a lab, not a tutorial"
    Prefer `systemctl` + `journalctl` over editing blindly. Pair with [Linux Production Incident Triage](linux-production-incident-triage.md) for deeper failure modes.

## Business Scenario

Ops needs a tiny heartbeat unit on lab hosts to prove logging and restart policy. You own the unit lifecycle and the first failed deploy.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Write a simple systemd service and timer (or `Type=simple` loop)
- [ ] Use `systemctl status`, `restart`, `enable`
- [ ] Filter journals with `-u`, `--since`, `-p`
- [ ] Distinguish unit failure from application log noise
- [ ] Sketch a logrotate policy for a file-based log

## Prerequisites

### Knowledge

- [systemd Services and journalctl](../linux/systemd-services-and-journalctl.md)
- [systemd Targets, Timers, and Boot](../linux/systemd-targets-timers-and-boot.md)
- [Logging: syslog, journald, logrotate](../linux/logging-syslog-journald-logrotate.md)
- [Process Management](../linux/process-management.md)

### Software

| Tool | Notes |
|------|--------|
| Ubuntu with systemd | required |
| sudo | install units under `/etc/systemd/system` |

**Estimated cost:** £0.

## Environment

```bash
mkdir -p ~/rebash-lab-linux-services/{bin,logs}
cd ~/rebash-lab-linux-services
```

## Initial State

No heartbeat unit installed.

## Lab Tasks

### Task 1 — Heartbeat script

```bash
cat > ~/rebash-lab-linux-services/bin/heartbeat.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
LOG="${HEARTBEAT_LOG:-$HOME/rebash-lab-linux-services/logs/heartbeat.log}"
mkdir -p "$(dirname "$LOG")"
echo "$(date -Is) host=$(hostname) status=ok" | tee -a "$LOG"
EOF
chmod +x ~/rebash-lab-linux-services/bin/heartbeat.sh
./bin/heartbeat.sh
tail -n 2 logs/heartbeat.log
```

### Task 2 — systemd service + timer

```bash
sudo tee /etc/systemd/system/rebash-heartbeat.service >/dev/null <<EOF
[Unit]
Description=REBASH lab heartbeat
After=network.target

[Service]
Type=oneshot
User=$(whoami)
Environment=HEARTBEAT_LOG=%h/rebash-lab-linux-services/logs/heartbeat.log
ExecStart=%h/rebash-lab-linux-services/bin/heartbeat.sh
EOF

sudo tee /etc/systemd/system/rebash-heartbeat.timer >/dev/null <<'EOF'
[Unit]
Description=Run REBASH heartbeat every minute

[Timer]
OnBootSec=30s
OnUnitActiveSec=60s
Unit=rebash-heartbeat.service

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now rebash-heartbeat.timer
systemctl list-timers | grep rebash || true
sudo systemctl start rebash-heartbeat.service
systemctl status rebash-heartbeat.service --no-pager
```

### Task 3 — Journal analysis

```bash
journalctl -u rebash-heartbeat.service -n 20 --no-pager
journalctl -u rebash-heartbeat.timer -n 10 --no-pager
journalctl -u rebash-heartbeat.service --since "10 minutes ago" -o short-iso | tee ~/rebash-lab-linux-services/journal-sample.txt
```

### Task 4 — Induce and fix a failure

Break the script path temporarily:

```bash
mv ~/rebash-lab-linux-services/bin/heartbeat.sh ~/rebash-lab-linux-services/bin/heartbeat.sh.bak
sudo systemctl start rebash-heartbeat.service || true
systemctl status rebash-heartbeat.service --no-pager -l
journalctl -u rebash-heartbeat.service -n 30 --no-pager | tee ~/rebash-lab-linux-services/failure.txt
mv ~/rebash-lab-linux-services/bin/heartbeat.sh.bak ~/rebash-lab-linux-services/bin/heartbeat.sh
sudo systemctl start rebash-heartbeat.service
systemctl is-active rebash-heartbeat.service || systemctl status rebash-heartbeat.service --no-pager
```

Write a three-line root-cause note in `~/rebash-lab-linux-services/rca.txt`.

### Task 5 — logrotate sketch

```bash
sudo tee /etc/logrotate.d/rebash-heartbeat >/dev/null <<EOF
$HOME/rebash-lab-linux-services/logs/*.log {
    weekly
    rotate 4
    compress
    missingok
    notifempty
    copytruncate
}
EOF
sudo logrotate -d /etc/logrotate.d/rebash-heartbeat 2>&1 | tee ~/rebash-lab-linux-services/logrotate-debug.txt
```

## Validation

- [ ] Timer is enabled; service runs successfully
- [ ] `journal-sample.txt` and `failure.txt` captured
- [ ] RCA documents the missing ExecStart path
- [ ] logrotate dry-run does not error fatally

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Timer not listed | `daemon-reload`; `enable --now` |
| Permission denied on log | Check `User=` and directory ownership |
| Empty journal | Ensure service actually started; check `_SYSTEMD_UNIT` |

## Challenge Extensions

- Convert to a long-running `Type=simple` service with `Restart=on-failure`
- Add `StandardOutput=journal` and drop the file log
- Compare `syslog` facility vs journal-only hosts

## Cleanup

```bash
sudo systemctl disable --now rebash-heartbeat.timer 2>/dev/null || true
sudo rm -f /etc/systemd/system/rebash-heartbeat.service /etc/systemd/system/rebash-heartbeat.timer
sudo rm -f /etc/logrotate.d/rebash-heartbeat
sudo systemctl daemon-reload
rm -rf ~/rebash-lab-linux-services
```

## Production Discussion

Prefer journald + central shipping (Fluent Bit, Vector, cloud agents). Units should declare dependencies, restart policy, and resource limits (`MemoryMax=`, etc.).

## Best Practices

- `daemon-reload` after unit edits
- Filter journals by unit and time window
- Keep RCA short and evidence-backed

## Common Mistakes

| Mistake | Correct approach |
|---------|------------------|
| Restarting without reading logs | `journalctl` first |
| Forgetting `daemon-reload` | Reload then restart |
| World-writable log dirs | Owned paths + modes |

## Success Criteria

You can enable a timer, break a unit on purpose, and recover using only journal evidence.

## Reflection Questions

1. When do you use a timer vs a long-running service?
2. What fields matter most in journal JSON output?
3. How does logrotate interact with processes that keep file handles open?

## Interview Connection

“Service won’t start — what do you run first?” → `systemctl status`, then `journalctl -u` with time bounds.

## Related Tutorials

- [systemd Services and journalctl](../linux/systemd-services-and-journalctl.md)
- [Logging: syslog, journald, logrotate](../linux/logging-syslog-journald-logrotate.md)
- Lab: [Production Incident Triage](linux-production-incident-triage.md)

## References

- [systemd documentation](https://systemd.io/)
- `man systemd.timer`, `man journalctl`, `man logrotate`
