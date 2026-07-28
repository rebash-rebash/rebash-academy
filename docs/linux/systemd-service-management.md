---
title: systemd Service Management
description: Manage Linux services with systemctl, write custom unit files, and troubleshoot with journalctl.
difficulty: intermediate
estimated_time: "55 min"
author: Shaik Basha
category: linux
tags:
  - linux
  - systemd
  - systemctl
  - services
prerequisites:
  - Complete Process Management or equivalent experience
  - sudo privileges on a systemd-based distribution
comments: false
---

# systemd Service Management

## Overview

**systemd** is the init system and service manager on virtually all modern Linux distributions. It starts the boot sequence, manages dependencies between services, applies resource limits, and integrates logging through journald. Administrators interact with systemd primarily through **unit files** (declarative service definitions) and the **`systemctl`** command.

This tutorial is part of **Module 3: Processes, Services & Packages** in the REBASH Academy Linux series. You will inspect and control service lifecycle, enable services at boot, write a custom unit file, understand masking vs disabling, and tie service failures to **journalctl** logs.

## Prerequisites

- Complete [Process Management](process-management.md) or equivalent experience
- A systemd-based Linux system (Ubuntu 20.04+, RHEL 8+, Debian 11+)
- `sudo` privileges for service control and unit file creation
- Basic text editor access (`nano`, `vim`, or `editor`)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain systemd unit types and the sections of a `.service` unit file
- [ ] Control service lifecycle with `systemctl start/stop/restart/reload`
- [ ] Enable, disable, and mask services for boot-time behavior
- [ ] Write and install a custom systemd service unit
- [ ] Reload unit definitions with `daemon-reload` after configuration changes
- [ ] Diagnose failed services using `systemctl status` and `journalctl`

## Architecture Diagram

```d2
direction: down

Boot: Boot {
        FW: "Firmware/Kernel"
        S1: "systemd PID 1"
    }
    Units: Units {
        SVC: ".service units"
        SOCK: ".socket units"
        TMR: ".timer units"
        TGT: ".target units"
    }
    Paths: Paths {
        PKG: "/usr/lib/systemd/system/"
        ETC: "/etc/systemd/system/"
        RUN: "/run/systemd/system/"
    }
    CLI: CLI {
        CTL: systemctl
        JRN: journalctl
    }
    Boot.FW -> Boot.S1
    Boot.S1 -> Units.TGT
    Units.TGT -> Units.SVC
    Units.TGT -> Units.SOCK
    Units.TGT -> Units.TMR
    Paths.PKG -> Units.SVC
    Paths.ETC -> Units.SVC
    Paths.RUN -> Units.SVC
    CLI.CTL -> Boot.S1
    Units.SVC -> CLI.JRN
    Units.SOCK -> CLI.JRN
```

## Theory

### Unit types

| Extension | Purpose | Example |
|-----------|---------|---------|
| `.service` | Daemon or one-shot task | `nginx.service`, `sshd.service` |
| `.socket` | Socket activation | `docker.socket` |
| `.timer` | Scheduled execution (cron-like) | `apt-daily.timer` |
| `.target` | Group of units (boot milestone) | `multi-user.target` |
| `.mount` | Filesystem mount | `var-lib-docker.mount` |

This tutorial focuses on **service units**.

### Unit file locations and precedence

| Path | Purpose |
|------|---------|
| `/usr/lib/systemd/system/` | Package-installed units (do not edit) |
| `/etc/systemd/system/` | Administrator overrides and custom units |
| `/run/systemd/system/` | Runtime-generated units |

Drop overrides in `/etc/systemd/system/unitname.service.d/override.conf` rather than editing vendor files.

### Anatomy of a service unit

```ini
[Unit]
Description=My Application
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=appuser
ExecStart=/usr/local/bin/myapp --config /etc/myapp/config.yml
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

| Section | Key directives | Meaning |
|---------|----------------|---------|
| Unit | `After`, `Before` | Ordering dependencies |
| Unit | `Requires`, `Wants` | Hard vs soft dependencies |
| Service | `Type` | `simple`, `forking`, `oneshot`, `notify` |
| Service | `ExecStart` | Command to launch |
| Service | `Restart` | Policy on exit (`always`, `on-failure`, `no`) |
| Install | `WantedBy` | Target for `enable` (symlink creation) |

### systemctl lifecycle states

| Command | Effect |
|---------|--------|
| `start` | Start unit now |
| `stop` | Stop running unit |
| `restart` | Stop then start |
| `reload` | Send SIGHUP or exec `ExecReload` |
| `enable` | Create symlinks for boot-time start |
| `disable` | Remove boot-time symlinks |
| `mask` | Symlink unit to `/dev/null` — cannot start even manually* |
| `unmask` | Remove mask symlink |

*Masked units are fully blocked until unmasked.

### Active vs enabled

- **Active**: Currently running (runtime state)
- **Enabled**: Configured to start at boot (symlink in `.wants/` directory)

A service can be enabled but inactive (will start on next boot), or active but disabled (running now, won't survive reboot).

### daemon-reload

After creating or modifying unit files, run:

```bash
sudo systemctl daemon-reload
```

systemd re-reads unit definitions. Without this, changes are ignored.

### journalctl integration

Service stdout/stderr and systemd messages are captured by journald. Primary triage commands:

```bash
systemctl status UNIT
journalctl -u UNIT -b -n 50 --no-pager
journalctl -u UNIT -p err --since "1 hour ago"
```

## Hands-on Lab

### Step 1 – Explore running services

```bash
systemctl list-units --type=service --state=running | head -15
systemctl list-unit-files --type=service --state=enabled | head -10
```

**Expected output:**

```
UNIT                          LOAD   ACTIVE SUB     DESCRIPTION
ssh.service                   loaded active running OpenBSD Secure Shell server
systemd-journald.service      loaded active running Journal Service
...
UNIT FILE                     STATE   PRESET
ssh.service                   enabled enabled
systemd-journald.service      enabled enabled
...
```

Unit names vary: `ssh.service` on Ubuntu, `sshd.service` on RHEL.

### Step 2 – Inspect a service status

```bash
systemctl status ssh 2>/dev/null || systemctl status sshd
systemctl is-active ssh 2>/dev/null || systemctl is-active sshd
systemctl is-enabled ssh 2>/dev/null || systemctl is-enabled sshd
```

**Expected output:**

```
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/usr/lib/systemd/system/ssh.service; enabled; preset: enabled)
     Active: active (running) since Mon 2026-07-27 09:00:01 UTC; 5h ago
   Main PID: 890 (sshd)
      Tasks: 1
     Memory: 4.2M
        CPU: 120ms
active
enabled
```

### Step 3 – View unit file contents

```bash
systemctl cat ssh 2>/dev/null || systemctl cat sshd
```

**Expected output:** Full unit file with `[Unit]`, `[Service]`, and `[Install]` sections, including `#` comments from the vendor.

### Step 4 – Control service lifecycle (nginx example)

Install nginx if not present, then practice lifecycle commands:

```bash
sudo apt install -y nginx 2>/dev/null || sudo dnf install -y nginx 2>/dev/null || true
sudo systemctl stop nginx 2>/dev/null && echo "Stopped" || echo "nginx not installed"
sudo systemctl start nginx 2>/dev/null && echo "Started"
sudo systemctl restart nginx 2>/dev/null && echo "Restarted"
sudo systemctl reload nginx 2>/dev/null && echo "Reloaded"
systemctl is-active nginx 2>/dev/null
```

**Expected output:**

```
Stopped
Started
Restarted
Reloaded
active
```

If nginx is not installed, skip gracefully — the commands demonstrate the pattern.

### Step 5 – Enable and disable at boot

```bash
sudo systemctl disable nginx 2>/dev/null
systemctl is-enabled nginx 2>/dev/null
sudo systemctl enable nginx 2>/dev/null
systemctl is-enabled nginx 2>/dev/null
```

**Expected output:**

```
disabled
enabled
```

`enable` creates a symlink in `/etc/systemd/system/multi-user.target.wants/`.

### Step 6 – Create a custom service unit

Build a simple long-running script and unit file:

```bash
sudo useradd -r -s /usr/sbin/nologin labdaemon 2>/dev/null || true
sudo tee /usr/local/bin/labdaemon.sh > /dev/null << 'EOF'
#!/bin/bash
while true; do
  echo "$(date -Iseconds) labdaemon heartbeat" >> /var/log/labdaemon.log
  sleep 30
done
EOF
sudo chmod +x /usr/local/bin/labdaemon.sh
sudo touch /var/log/labdaemon.log
sudo chown labdaemon:labdaemon /var/log/labdaemon.log

sudo tee /etc/systemd/system/labdaemon.service > /dev/null << 'EOF'
[Unit]
Description=REBASH Lab Daemon
After=network.target

[Service]
Type=simple
User=labdaemon
ExecStart=/usr/local/bin/labdaemon.sh
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now labdaemon.service
systemctl status labdaemon.service --no-pager
```

**Expected output:**

```
Created symlink .../multi-user.target.wants/labdaemon.service → ...
● labdaemon.service - REBASH Lab Daemon
     Loaded: loaded (/etc/systemd/system/labdaemon.service; enabled; ...)
     Active: active (running) since ...
   Main PID: 6010 (labdaemon.sh)
```

### Step 7 – Tie service logs to journalctl

```bash
journalctl -u labdaemon.service -n 5 --no-pager
tail -3 /var/log/labdaemon.log
```

**Expected output:**

```
Jul 27 14:45:01 hostname labdaemon.sh[6010]: (no stdout — app logs to file)
```

The unit logs lifecycle events to journald; application output goes to `/var/log/labdaemon.log` because the script writes there directly. For journal capture, log to stdout:

```bash
# Alternative: ExecStart script using echo without file redirect
# stdout/stderr automatically appear in journalctl -u UNIT
```

Verify journal captures systemd messages:

```bash
journalctl -u labdaemon.service -b --no-pager | tail -5
```

### Step 8 – Mask, unmask, and clean up

```bash
sudo systemctl stop labdaemon.service
sudo systemctl mask labdaemon.service
systemctl status labdaemon.service --no-pager | head -5
sudo systemctl start labdaemon.service 2>&1 | head -1
sudo systemctl unmask labdaemon.service
sudo systemctl disable labdaemon.service
sudo rm /etc/systemd/system/labdaemon.service
sudo systemctl daemon-reload
```

**Expected output:**

```
○ labdaemon.service
     Loaded: masked (/dev/null; masked)
     Active: inactive (dead)
Failed to start labdaemon.service: Access denied
```

Masking prevents accidental starts during maintenance.

## Commands

| Command | Description |
|---------|-------------|
| `systemctl start UNIT` | Start a unit immediately |
| `systemctl stop UNIT` | Stop a running unit |
| `systemctl restart UNIT` | Stop and start unit |
| `systemctl reload UNIT` | Reload configuration without full restart |
| `systemctl status UNIT` | Show runtime status and recent log lines |
| `systemctl enable UNIT` | Enable unit to start at boot |
| `systemctl disable UNIT` | Disable boot-time start |
| `systemctl enable --now UNIT` | Enable and start in one command |
| `systemctl mask UNIT` | Block unit from being started (even manually) |
| `systemctl unmask UNIT` | Remove mask |
| `systemctl is-active UNIT` | Print `active`, `inactive`, or `failed` |
| `systemctl is-enabled UNIT` | Print `enabled`, `disabled`, or `masked` |
| `systemctl list-units --type=service` | List loaded service units |
| `systemctl list-unit-files --type=service` | List all unit files and enable state |
| `systemctl cat UNIT` | Show unit file contents (with overrides) |
| `systemctl edit UNIT` | Create drop-in override interactively |
| `systemctl daemon-reload` | Reload unit definitions after file changes |
| `systemctl reset-failed` | Clear failed state for all units |
| `systemctl --failed` | List units in failed state |
| `journalctl -u UNIT -n 50` | Last 50 log lines for a unit |
| `journalctl -u UNIT -b -p err` | Errors for unit in current boot |

## Code Examples

### Production-grade application unit

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application API
Documentation=https://docs.example.com/myapp
After=network-online.target postgresql.service
Wants=network-online.target
Requires=postgresql.service

[Service]
Type=simple
User=myapp
Group=myapp
WorkingDirectory=/var/lib/myapp
EnvironmentFile=/etc/myapp/environment
ExecStart=/usr/local/bin/myapp serve
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5
LimitNOFILE=65535
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Drop-in override for environment variable

```ini
# /etc/systemd/system/myapp.service.d/override.conf
[Service]
Environment=LOG_LEVEL=debug
Environment=APP_ENV=staging
```

Apply with: `systemctl daemon-reload && systemctl restart myapp`.

### Service health check script

```bash
#!/bin/bash
# check-service.sh — verify unit is active and enabled
set -euo pipefail

UNIT="${1:?Usage: $0 <unit.service>}"

STATE=$(systemctl is-active "$UNIT" 2>/dev/null || echo "inactive")
ENABLED=$(systemctl is-enabled "$UNIT" 2>/dev/null || echo "unknown")

echo "Unit: $UNIT"
echo "Active: $STATE"
echo "Enabled: $ENABLED"

if [[ "$STATE" != "active" ]]; then
  echo "=== Recent journal ==="
  journalctl -u "$UNIT" -n 20 --no-pager
  exit 1
fi
```

## Common Mistakes

!!! warning "Forgetting daemon-reload after unit changes"
    Editing unit files without `systemctl daemon-reload` leaves systemd using stale definitions. Always reload before start/restart.

!!! warning "Editing files in /usr/lib/systemd/system directly"
    Package manager updates overwrite vendor units. Place custom units in `/etc/systemd/system/` or use drop-in overrides.

!!! warning "Using Type=simple for forking daemons"
    Traditional daemons that double-fork need `Type=forking` and often `PIDFile=`. Wrong type causes systemd to think the service failed immediately.

!!! warning "Confusing disable with mask"
    `disable` prevents boot start but allows manual `start`. `mask` blocks all starts until `unmask`.

## Best Practices

!!! tip "Always use Type=notify when supported"
    Applications using sd_notify report readiness accurately — systemd waits before marking dependent units started.

!!! tip "Set Restart=on-failure with RestartSec"
    Automatic recovery from transient errors without tight restart loops hammering the system.

!!! tip "Use EnvironmentFile for secrets"
    Keep secrets out of unit files; reference `/etc/myapp/environment` with restrictive permissions (600).

!!! tip "Pair status with journalctl during incidents"
    `systemctl status UNIT -l --no-pager` plus `journalctl -u UNIT -b -p err -n 100` is the standard triage pattern.

!!! tip "Test with systemd-analyze"
    `systemd-analyze verify /etc/systemd/system/myapp.service` catches unit syntax errors before deployment.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Unit fails immediately (code=exited) | Wrong ExecStart path or permissions | Check `journalctl -u UNIT`; verify binary exists and User can execute |
| Job failed because the control process exited with error code | Type mismatch (forking vs simple) | Adjust `Type=`; add `PIDFile=` for forking daemons |
| Address already in use | Port conflict with another process | `ss -tlnp \| grep PORT`; stop conflicting service |
| daemon-reload not enough | Missing restart after reload | `daemon-reload` then `restart UNIT` |
| Service active but not enabled | Started manually, not configured for boot | `systemctl enable UNIT` |
| Cannot start masked unit | Unit was masked for maintenance | `systemctl unmask UNIT` |
| Dependency failed | Required unit not running | `systemctl list-dependencies UNIT`; start dependency first |

## Summary

- systemd manages services through **unit files** with `[Unit]`, `[Service]`, and `[Install]` sections.
- Use **systemctl** for lifecycle (`start/stop/restart`), boot policy (`enable/disable`), and blocking (`mask/unmask`).
- Custom units belong in `/etc/systemd/system/`; always run **daemon-reload** after changes.
- **Active** vs **enabled** are independent — verify both for production services.
- Combine **systemctl status** with **journalctl -u UNIT** for complete failure diagnosis.

## Interview Questions

**1. What is the difference between systemctl enable and systemctl start?**

*Sample answer:* `start` activates the unit immediately in the current session. `enable` creates symlinks so the unit starts automatically at boot. You often use `enable --now` for both.

**2. Where should custom unit files be placed?**

*Sample answer:* `/etc/systemd/system/` for administrator-created units. Package-installed units live in `/usr/lib/systemd/system/` and should not be edited directly — use drop-in overrides instead.

**3. What does systemctl daemon-reload do?**

*Sample answer:* It tells systemd to re-read all unit files from disk. Required after creating, modifying, or deleting unit files before changes take effect.

**4. How is masking different from disabling a service?**

*Sample answer:* `disable` removes boot symlinks but allows manual `start`. `mask` symlinks the unit to `/dev/null`, preventing any start attempt until `unmask`.

**5. What are the main sections of a .service unit file?**

*Sample answer:* `[Unit]` for metadata and dependencies, `[Service]` for execution directives (ExecStart, User, Restart), and `[Install]` for enable targets (WantedBy).

**6. How do you view logs for a failed nginx service?**

*Sample answer:* `systemctl status nginx` for summary and exit code, then `journalctl -u nginx -b -n 50 --no-pager` for detailed logs. Add `-p err` to filter errors.

**7. What is Type=simple vs Type=forking?**

*Sample answer:* `simple` (default) assumes ExecStart is the main process. `forking` is for traditional daemons that double-fork and exit the parent — systemd tracks the PID file instead.

**8. What does Restart=on-failure do?**

*Sample answer:* systemd automatically restarts the service if it exits with a non-zero code, is killed by a signal, or times out. It does not restart on clean exit (code 0).

**9. How do you override a vendor unit without editing the original file?**

*Sample answer:* Create `/etc/systemd/system/UNIT.service.d/override.conf` with changed directives, or use `systemctl edit UNIT`. Run `daemon-reload` and restart.

**10. What is multi-user.target?**

*Sample answer:* The standard boot target for multi-user server mode (equivalent to runlevel 3). Services with `WantedBy=multi-user.target` start when the system reaches normal operation.

## Related Tutorials

- [Linux – Category Overview](index.md)
- [Process Management](process-management.md) *(previous)*
- [Package Management](package-management.md) *(next)*
- [Log Management with journalctl](log-management-journalctl.md)
- [Remote systemd Services](remote-systemd-services.md)
- [Cron and Task Scheduling](cron-and-task-scheduling.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [systemd.service man page](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [systemctl man page](https://www.freedesktop.org/software/systemd/man/systemctl.html)
- [systemd unit file structure](https://www.freedesktop.org/software/systemd/man/systemd.unit.html)
- [Red Hat – Managing services with systemd](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_basic_system_settings/assembly_managing-system-services-with-systemd_configuring-basic-system-settings)
- [REBASH Academy – Linux Overview](index.md)
