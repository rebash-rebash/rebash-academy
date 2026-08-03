---
title: "systemd Services and journalctl"
description: "Create and manage systemd services with systemctl, use drop-ins safely, and query logs with journalctl on Ubuntu."
difficulty: intermediate
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 7 · Services & Boot"
tags:
  - linux
  - systemd
  - systemctl
  - journalctl
prerequisites:
  - linux/process-management
next:
  - linux/systemd-targets-timers-and-boot
related:
  - linux/logging-syslog-journald-logrotate
interview: interview/linux
comments: false
---

# systemd Services and journalctl

## Overview

On almost every modern Linux cloud image, **systemd** is process ID 1 (PID 1). It starts **units** (services, sockets, timers, mounts), tracks dependencies, places processes in control groups (cgroups), and records structured logs through **journald**. Day-to-day you use **systemctl** to control services and **journalctl** to read their logs.

If a service will not start after a deploy, or disappears after reboot because it was never **enabled**, systemd is the control plane you debug. Editing vendor unit files under `/lib/systemd/system` (or `/usr/lib`) loses changes on package upgrade — the supported path is a unit or **drop-in** under `/etc/systemd/system`. The journal is often faster evidence than grepping flat files alone, especially with `-u` and `--since`.

In production, good habits are: `daemon-reload` after unit changes, `systemctl status` + `journalctl -u` before guessing, `enable --now` when you need boot persistence, and hardening directives (`NoNewPrivileges=`, `ProtectSystem=`) where they fit. This tutorial builds a small lab service you can start, log, override, and remove cleanly.

This is **Tutorial 10** in **Module 7: Services & Boot** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers.

## Prerequisites

- [Process Management](process-management.md)
- A **practice Ubuntu 22.04/24.04 VM** where you have `sudo`
- Do **not** run this lab on a shared production server

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain unit files, vendor vs `/etc` locations, and drop-ins
- [ ] Create a simple systemd service, reload, start, and enable it
- [ ] Query logs with `journalctl -u` and time filters
- [ ] Override a setting with a drop-in without editing the vendor/lab unit body incorrectly
- [ ] Remove the lab unit cleanly and save evidence under `~/rebash-linux/lab10`

## Architecture

systemd sits as PID 1: it activates units, supervises processes, and records journal logs that operators query with journalctl.

![Architecture diagram for systemd Services and journalctl](../assets/excalidraw/linux-systemd-architecture.svg)

## Theory

### What it is

A **unit** describes something systemd can manage. A **service** unit usually has an `[Unit]` section (description, ordering), a `[Service]` section (`ExecStart=`, user, restart policy), and an `[Install]` section (`WantedBy=` for boot).

| Action | Effect |
|--------|--------|
| `start` / `stop` | Runtime only |
| `enable` / `disable` | Boot persistence (symlinks) |
| `reload` | Re-read app config if the unit supports it |
| `restart` | Stop then start |
| `edit` / drop-in | Override without rewriting the whole unit |
| `mask` | Make start impossible (stronger than disable) |

```bash title="Terminal"
systemctl status cron.service
systemctl cat cron.service
journalctl -u cron.service -n 20 --no-pager
```

### Why it matters

Cloud VMs boot into a graph of units. Apps that were started only with `nohup` or a manual shell die on reboot or after crash without restart. Wrong working directory, missing `User=`, or a failed `ExecStart` shows up immediately in `systemctl status` and the journal. Teams that treat units as code (reviewed drop-ins) recover faster than teams that hand-edit vendor files.

### How it works

1. **Write** a unit under `/etc/systemd/system/name.service` (local) or add a drop-in under `name.service.d/*.conf`.
2. **`systemctl daemon-reload`** — systemd re-reads unit files.
3. **`systemctl start name`** — start now; **`enable`** — start on boot; **`enable --now`** — both.
4. **Inspect** — `systemctl status`, `systemctl cat`, `systemctl show`.
5. **Logs** — `journalctl -u name -e --no-pager`; add `--since '10 min ago'` or `-p err`.

Persist journals under `/var/log/journal` when you need logs after reboot (many cloud images already do this).

| Query | Example |
|-------|---------|
| Unit | `journalctl -u rebash-lab.service -e` |
| Since | `journalctl --since '1 hour ago'` |
| Priority | `journalctl -p err..alert -b` |
| Follow | `journalctl -f -u rebash-lab.service` |

### Key concepts and comparisons

| Location | Use for |
|----------|---------|
| `/lib/systemd/system` or `/usr/lib/systemd/system` | Vendor/package units — do not edit in place |
| `/etc/systemd/system` | Local units and overrides |
| `/etc/systemd/system/foo.service.d/*.conf` | Drop-in fragments |

| Directive | Typical meaning |
|-----------|-----------------|
| `Type=simple` | Main process is `ExecStart` (default pattern) |
| `Type=oneshot` | Short task; often `RemainAfterExit=yes` |
| `Restart=on-failure` | Restart when the process fails |
| `After=` / `Requires=` | Ordering and hard dependency |

### Common pitfalls

- Editing `/lib/systemd/system` and losing changes on upgrade.
- Forgetting `daemon-reload` after adding or changing units.
- `enable` without noticing the unit is **failed** (`systemctl --failed`).
- Assuming the journal is persistent when the host only keeps a volatile journal.
- Using `restart` when `reload` would be gentler for the application.

## Hands-on Lab

### Objective

Create a local `rebash-lab.service` that writes a heartbeat line on a schedule-friendly loop, manage it with systemctl, read logs with journalctl, add a drop-in, and save evidence under `~/rebash-linux/lab10`.

### Prerequisites

- Ubuntu 22.04/24.04 with systemd and sudo
- Packages: `systemd` (default on Ubuntu)

### Lab environment

Workspace: `~/rebash-linux/lab10`

```bash title="Terminal"
mkdir -p ~/rebash-linux/lab10 && cd ~/rebash-linux/lab10
set -euo pipefail
whoami | tee lab-user.txt
systemctl is-system-running | tee systemd-state.txt || true
test -n "$(command -v systemctl)"
sudo -n true 2>/dev/null || sudo -v
```

!!! example "Expected output"
    `systemctl` works; sudo is available (password once if needed).


### Real-world scenario

Your team needs a tiny “sidecar” style helper on an Ubuntu app VM: a supervised process that appends a heartbeat to a file and appears in the journal. Security asks that it run as a normal service (not a forgotten `nohup`), that you can show logs with `journalctl -u`, and that overrides use a drop-in. You build that on a practice VM and keep proof for the change ticket.

### Step-by-step tasks

#### Task 1 – Install unit and start the service

```bash title="Terminal"
cd ~/rebash-linux/lab10
set -euo pipefail

# Working directory and script owned by your user; service will run as you
mkdir -p "$HOME/rebash-linux/lab10/run"
cat > "$HOME/rebash-linux/lab10/run/heartbeat.sh" << 'EOF'
#!/bin/bash
set -euo pipefail
LOG_DIR="${HOME}/rebash-linux/lab10/run"
mkdir -p "$LOG_DIR"
while true; do
  ts="$(date -Is)"
  echo "${ts} rebash-lab heartbeat ok" | tee -a "${LOG_DIR}/heartbeat.log"
  sleep 15
done
EOF
chmod +x "$HOME/rebash-linux/lab10/run/heartbeat.sh"

UNIT_USER="$(whoami)"
UNIT_HOME="$HOME"

sudo tee /etc/systemd/system/rebash-lab.service >/dev/null << EOF
[Unit]
Description=REBASH lab heartbeat service
After=network.target

[Service]
Type=simple
User=${UNIT_USER}
WorkingDirectory=${UNIT_HOME}/rebash-linux/lab10/run
ExecStart=${UNIT_HOME}/rebash-linux/lab10/run/heartbeat.sh
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now rebash-lab.service
systemctl is-active rebash-lab.service | tee service-active.txt
test "$(cat service-active.txt)" = "active"
systemctl status rebash-lab.service --no-pager | tee service-status.txt
```

!!! example "Expected output"
    `service-active.txt` is `active`; status shows the unit running.


#### Task 2 – journalctl evidence and heartbeat file

```bash title="Terminal"
cd ~/rebash-linux/lab10
set -euo pipefail

# Wait for at least one heartbeat line
for i in 1 2 3 4 5 6; do
  if [[ -s "$HOME/rebash-linux/lab10/run/heartbeat.log" ]]; then
    break
  fi
  sleep 3
done
test -s "$HOME/rebash-linux/lab10/run/heartbeat.log"
cp "$HOME/rebash-linux/lab10/run/heartbeat.log" heartbeat-log-copy.txt

journalctl -u rebash-lab.service -n 50 --no-pager | tee journal-unit.txt
grep -q 'heartbeat ok' journal-unit.txt || grep -q 'heartbeat ok' heartbeat-log-copy.txt

systemctl show rebash-lab.service -p FragmentPath -p DropInPaths -p MainPID \
  | tee service-show.txt
```

!!! example "Expected output"
    heartbeat log has lines; journal or log copy shows `heartbeat ok`; `MainPID` is set.


#### Task 3 – Drop-in override and evidence pack

```bash title="Terminal"
cd ~/rebash-linux/lab10
set -euo pipefail

# Add an environment variable via drop-in (does not edit the main unit file body by hand)
sudo mkdir -p /etc/systemd/system/rebash-lab.service.d
sudo tee /etc/systemd/system/rebash-lab.service.d/10-lab.conf >/dev/null << 'EOF'
[Service]
Environment=REBASH_LAB=1
EOF

sudo systemctl daemon-reload
sudo systemctl restart rebash-lab.service
systemctl is-active rebash-lab.service | tee service-active-after-dropin.txt
test "$(cat service-active-after-dropin.txt)" = "active"

systemctl cat rebash-lab.service | tee service-cat.txt
grep -q 'REBASH_LAB=1' service-cat.txt
systemctl show rebash-lab.service -p Environment | tee service-env.txt
grep -q 'REBASH_LAB=1' service-env.txt

tar -czf systemd-service-evidence.tgz \
  lab-user.txt systemd-state.txt \
  service-active.txt service-status.txt \
  heartbeat-log-copy.txt journal-unit.txt service-show.txt \
  service-active-after-dropin.txt service-cat.txt service-env.txt
ls -l systemd-service-evidence.tgz | tee evidence-ls.txt
test -s systemd-service-evidence.tgz
```

!!! example "Expected output"
    `systemctl cat` includes the drop-in; Environment shows `REBASH_LAB=1`; archive is non-empty.


### Validation steps

- [ ] `systemctl is-active rebash-lab.service` is `active`
- [ ] Heartbeat lines exist under `~/rebash-linux/lab10/run/heartbeat.log`
- [ ] `journalctl -u rebash-lab.service` returns recent entries
- [ ] Drop-in appears in `systemctl cat`
- [ ] `systemd-service-evidence.tgz` exists

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Unit rebash-lab.service not found` | Forgot `daemon-reload` | `sudo systemctl daemon-reload` |
| `activating (auto-restart)` loop | Script path/permissions wrong | `journalctl -u rebash-lab -e`; fix `ExecStart` and `chmod +x` |
| Empty journal lines | Permissions / rate limit / wrong unit name | Confirm `-u rebash-lab.service`; check heartbeat file |
| Drop-in ignored | Wrong directory name | Must be `rebash-lab.service.d/*.conf` then `daemon-reload` |

### Challenge exercise

Add a second drop-in `20-security.conf` that sets `NoNewPrivileges=yes` for `rebash-lab.service`. Reload, restart, and prove with `systemctl show rebash-lab.service -p NoNewPrivileges` saved to `challenge-nnp.txt`. Remove this drop-in in Cleanup if you create it.

### Learning outcomes

- Created and enabled a local systemd service
- Used journalctl and status for evidence
- Applied a drop-in override safely
- Packaged proof for a change ticket

### Cleanup

```bash title="Terminal"
cd ~/rebash-linux/lab10
set -euo pipefail

sudo systemctl disable --now rebash-lab.service 2>/dev/null || true
sudo rm -f /etc/systemd/system/rebash-lab.service
sudo rm -rf /etc/systemd/system/rebash-lab.service.d
sudo systemctl daemon-reload
sudo systemctl reset-failed rebash-lab.service 2>/dev/null || true

# Keep evidence archive if you want; optional:
# rm -rf run *.txt systemd-service-evidence.tgz
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab10/` with evidence files
- [ ] You can explain start vs enable and why drop-ins beat editing vendor units
- [ ] You can gather logs with `journalctl -u` for one service
- [ ] Cleanup removed the lab unit

## Code Walkthrough

In real servers, systemd service work usually follows this order:

1. **Inspect** — `status`, `cat`, `journalctl -u` before changing  
2. **Change under `/etc`** — local unit or drop-in, never vendor files in place  
3. **`daemon-reload`** then start/restart  
4. **Prove** — `is-active`, journal lines, application health check  
5. **Least privilege** — `User=`, hardening directives, narrow sudo for restarts  

Automate units with configuration management when the pattern is stable; still keep a manual recovery path.

## Security Considerations

- Run services as a dedicated user, not root, when possible  
- Prefer drop-ins reviewed in git over improvised production edits  
- Limit who can `systemctl` manage sensitive units via policy / sudo  
- Treat journal access as sensitive — it may contain secrets from apps  
- Use `NoNewPrivileges=`, `ProtectSystem=`, and friends where compatible  

## Common Mistakes

!!! warning "Editing vendor units under `/lib` or `/usr/lib`"
    Package upgrades overwrite your changes. **Fix:** copy to `/etc` or use `systemctl edit` drop-ins.

!!! warning "Forgetting `daemon-reload`"
    systemd still uses the old unit definition. **Fix:** reload, then restart the unit.

!!! warning "Assuming enable means healthy"
    A unit can be enabled and still **failed**. **Fix:** check `systemctl --failed` and the journal after every change.

!!! warning "Using `restart` when `reload` is enough"
    Unnecessary connection drops. **Fix:** use reload when the app supports it; restart when the binary or unit must change.

## Best Practices

- Name units clearly (`app-api.service`) and document `ExecStart`  
- Always pair deploy changes with journal checks  
- Prefer `enable --now` in runbooks when boot persistence is required  
- Keep drop-ins small and commented  
- Alert on failed units (`systemctl --failed`) in monitoring  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `status=203/EXEC` | Bad `ExecStart` path or not executable | Fix path; `chmod +x`; daemon-reload |
| `status=216/GROUP` or user errors | Wrong `User=`/`Group=` | Create user or fix names |
| No logs in journalctl | Wrong unit / permissions / stdout not captured | Confirm unit name; ensure process logs to stdout/stderr or journal |
| Changes ignored | No daemon-reload / wrong drop-in path | Fix path; reload; `systemctl cat` |
| Starts then exits | `Type=` mismatch / oneshot without RemainAfterExit | Match Type to programme behaviour |

## Summary

systemd services give you supervised start, stop, enable-on-boot, and journal logs. Prefer `/etc` units and drop-ins, prove with `systemctl` and `journalctl`, and clean up lab units. Next: [systemd Targets, Timers, and Boot](systemd-targets-timers-and-boot.md).

## Interview Questions

**1. What is the difference between `systemctl start` and `systemctl enable`?**

??? success "Reveal answer"
    **start** affects the **current** boot only (runtime). **enable** creates symlinks so the unit is pulled in on future boots. Use **`enable --now`** when you want both. Interviewers look for this distinction constantly.

**2. Why should you not edit unit files under `/lib/systemd/system`?**

??? success "Reveal answer"
    Those files belong to **packages**. Upgrades overwrite them. Put local units or drop-ins under `/etc/systemd/system` (for example via `systemctl edit`) so changes survive updates and are visible in `systemctl cat`.

**3. A service is in failed state after deploy. What is your first evidence path?**

??? success "Reveal answer"
    `systemctl status name.service` and `journalctl -u name.service -e --no-pager` (optionally `--since`). Read `ExecStart` errors, exit codes, and recent commits/config changes before restarting in a loop.

**4. What is a systemd drop-in, and when do you use one?**

??? success "Reveal answer"
    A drop-in is a fragment under `name.service.d/*.conf` that **overrides or adds** directives without rewriting the whole unit. Use it to change `Environment=`, restart policy, or limits while keeping the vendor unit intact.

**5. How do `restart` and `reload` differ?**

??? success "Reveal answer"
    **restart** stops then starts the service (new process). **reload** asks the process to re-read configuration if the unit defines `ExecReload=` and the app supports it — often gentler for listeners. If reload is not supported, restart is required.

**6. How do you confirm a unit will survive reboot?**

??? success "Reveal answer"
    Check `systemctl is-enabled name` (should be `enabled`), inspect `[Install]` / WantedBy links, and preferably verify on a practice VM with a reboot window. `is-active` alone does not prove enablement.

**7. What security hardening might you add to a simple service unit?**

??? success "Reveal answer"
    Run as a dedicated `User=`, set `NoNewPrivileges=yes`, consider `ProtectSystem=`, `ProtectHome=`, and tight filesystem permissions on `ExecStart`. Prove with `systemctl show` and test that the app still works after hardening.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Process Management](process-management.md) *(previous)*
- [systemd Targets, Timers, and Boot](systemd-targets-timers-and-boot.md) *(next)*
- [Logging with syslog, journald, and logrotate](logging-syslog-journald-logrotate.md) *(related)*

## References

- [systemd documentation](https://systemd.io/)  
- [`systemctl(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/systemctl.1.html) — Ubuntu man-pages  
- [`journalctl(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/journalctl.1.html) — Ubuntu man-pages  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
