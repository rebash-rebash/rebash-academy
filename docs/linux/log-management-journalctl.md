---
title: Log Management with journalctl
description: Read, filter, persist, and forward logs using the systemd journal and journalctl.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
  - logging
  - systemd
  - journalctl
prerequisites:
  - Complete Module 5 tutorials or equivalent experience
  - Familiarity with systemd service management
comments: false
---

# Log Management with journalctl

## Overview

Modern Linux distributions store most system and service logs in the **systemd journal** — a structured, indexed, binary log managed by `systemd-journald`. The `journalctl` command is the primary interface for querying, filtering, and exporting these logs.

Unlike flat text files in `/var/log`, the journal supports metadata such as unit names, priorities, boot IDs, and process IDs. This makes it far easier to answer production questions like "what failed after the last deploy?" or "show me all errors from nginx in the previous boot."

This tutorial is part of **Module 6: Storage, Logs, Networking & Operations** in the REBASH Academy Linux series. You will learn to filter by priority, follow logs in real time, inspect previous boots, configure persistent storage, and integrate journal data into your operational workflow.

## Prerequisites

- Complete [systemd Service Management](systemd-service-management.md) or equivalent experience
- A Linux VM, cloud instance, or local machine running systemd (Ubuntu 20.04+, RHEL 8+, Debian 11+)
- `sudo` privileges for persistent journal configuration exercises
- SSH or console access to run lab commands

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain how `systemd-journald` collects and stores log data
- [ ] Filter logs by priority, time range, systemd unit, and boot session
- [ ] Follow logs in real time and export entries for analysis or SIEM ingestion
- [ ] Configure persistent journal storage and retention limits
- [ ] Troubleshoot missing logs, permission issues, and disk pressure from journal growth

## Architecture

```d2
direction: down

Sources: Sources {
        K: Kernel
        S: "systemd Units"
        A: "Applications via stdout/stderr"
    }
    journald: journald {
        J: systemd-journald
        R: "Journal Files\n/run/log/journal\n/var/log/journal"
    }
    Consumers: Consumers {
        C: "journalctl CLI"
        F: "Forward to SIEM/syslog"
        M: "Monitoring alerts"
    }
    Sources.K -> journald.J
    Sources.S -> journald.J
    Sources.A -> journald.J
    journald.J -> journald.R
    journald.R -> Consumers.C
    journald.R -> Consumers.F
    journald.R -> Consumers.M
```

## Theory

### The systemd journal

When a service writes to stdout or stderr, or when the kernel emits a message, `systemd-journald` captures it and stores it with metadata fields:

| Field | Meaning |
|-------|---------|
| `_SYSTEMD_UNIT` | Service unit name (e.g., `nginx.service`) |
| `PRIORITY` | Syslog severity level (0–7) |
| `_PID` | Process ID |
| `_BOOT_ID` | Unique identifier for each boot session |
| `_HOSTNAME` | Host that generated the entry |
| `MESSAGE` | Log message text |

Journal files live in `/run/log/journal/` (volatile, cleared on reboot) by default. When persistent storage is enabled, copies are also written to `/var/log/journal/`.

### Log priority levels

`journalctl` uses syslog priority names and numeric shortcuts:

| Priority | Name | Typical use |
|----------|------|-------------|
| 0 | emerg | System unusable |
| 1 | alert | Immediate action required |
| 2 | crit | Critical conditions |
| 3 | err | Error conditions |
| 4 | warning | Warning conditions |
| 5 | notice | Normal but significant |
| 6 | info | Informational |
| 7 | debug | Debug-level messages |

Filter with `-p err` (errors and above) or `-p warning..err` (range syntax).

### Boot sessions and unit filters

Each reboot creates a new boot ID. Use `-b` for the current boot, `-b -1` for the previous boot, and `-b 0` for all boots. Unit filters (`-u nginx.service`) narrow output to a single service — essential when debugging application failures.

### Persistent journal configuration

By default, many cloud images use volatile journals to save disk space. Production servers should enable persistence in `/etc/systemd/journald.conf`:

```ini
[Journal]
Storage=persistent
SystemMaxUse=500M
MaxRetentionSec=30day
```

After changes, restart `systemd-journald` with `sudo systemctl restart systemd-journald`.

### journalctl vs traditional log files

Text logs in `/var/log/syslog` or `/var/log/messages` remain on some systems, but systemd-centric distros increasingly rely on the journal. Use `journalctl` for unified querying; use file-based logs when legacy tools or applications require them.

## Hands-on Lab

### Step 1 – View recent journal entries

Display the last 20 log lines from the current boot:

```bash
journalctl -n 20 --no-pager
```

**Expected output (sample):**

```text
Jul 27 14:02:11 lab-server systemd[1]: Started Daily apt download activities.
Jul 27 14:02:12 lab-server sshd[1240]: Accepted publickey for ubuntu from 10.0.1.5
Jul 27 14:02:15 lab-server kernel: eth0: link up
...
```

### Step 2 – Filter by systemd unit

Inspect logs for the SSH service (unit name varies by distribution):

```bash
journalctl -u ssh -n 10 --no-pager 2>/dev/null \
  || journalctl -u sshd -n 10 --no-pager
```

**Expected output:** Lines prefixed with the unit name showing connection attempts, key auth, or session open/close events.

### Step 3 – Filter by priority and time

Show errors from the last hour, then all warnings and above:

```bash
journalctl --since "1 hour ago" -p err --no-pager | tail -5
journalctl -p warning..emerg -n 10 --no-pager
```

**Expected output:** Only entries at the specified severity; timestamps within your chosen window.

### Step 4 – Follow logs in real time

Start live tailing (like `tail -f`), then generate activity in another terminal:

```bash
journalctl -f
```

In a second terminal:

```bash
logger "REBASH lab test message"
```

**Expected output:** The `-f` session prints the new line immediately with your hostname and the test message.

Press `Ctrl+C` to stop following.

### Step 5 – Inspect previous boots

List available boots and view logs from the last reboot:

```bash
journalctl --list-boots
journalctl -b -1 -n 15 --no-pager
```

**Expected output:**

```text
IDX BOOT ID                          FIRST ENTRY                 LAST ENTRY
 -1 abc123...                         Mon 2026-07-26 09:00:01     Mon 2026-07-27 08:59:58
  0 def456...                         Mon 2026-07-27 09:00:02     Mon 2026-07-27 14:30:00
```

The `-b -1` output shows shutdown events, kernel messages, and service stops from the prior session.

### Step 6 – JSON export for parsing

Export structured JSON for scripting or SIEM pipelines:

```bash
journalctl -u ssh -n 3 -o json --no-pager 2>/dev/null \
  || journalctl -u sshd -n 3 -o json --no-pager
```

**Expected output:** One JSON object per line with fields like `"MESSAGE"`, `"PRIORITY"`, `"_SYSTEMD_UNIT"`.

### Step 7 – Check journal disk usage

```bash
journalctl --disk-usage
sudo ls -lh /var/log/journal/ 2>/dev/null || echo "Persistent journal not enabled"
```

**Expected output:**

```text
Archived and active journals take up 48.0M in the file system.
```

### Step 8 – Enable persistent journal (optional, requires sudo)

```bash
sudo mkdir -p /var/log/journal
sudo sed -i 's/#Storage=auto/Storage=persistent/' /etc/systemd/journald.conf
grep ^Storage= /etc/systemd/journald.conf
sudo systemctl restart systemd-journald
journalctl --disk-usage
```

**Expected output:** `Storage=persistent` in config; disk usage may increase after restart as logs are flushed to `/var/log/journal/`.

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

| Command | Description |
|---------|-------------|
| `journalctl` | Query the systemd journal (default: all entries, pager enabled) |
| `journalctl -n 50` | Show last 50 lines |
| `journalctl -f` | Follow new entries in real time |
| `journalctl -u UNIT` | Filter by systemd unit (e.g., `nginx.service`) |
| `journalctl -p err` | Show priority err and above (emerg, alert, crit, err) |
| `journalctl -p warning..err` | Show entries within a priority range |
| `journalctl --since "2 hours ago"` | Time filter (supports `today`, `yesterday`, ISO dates) |
| `journalctl --until "2026-07-27 12:00"` | Upper time bound |
| `journalctl -b` | Current boot only |
| `journalctl -b -1` | Previous boot |
| `journalctl --list-boots` | List boot sessions with IDs |
| `journalctl -k` | Kernel messages only |
| `journalctl -o json` | JSON output format |
| `journalctl -o cat` | Message text only (no metadata) |
| `journalctl --disk-usage` | Report journal space consumption |
| `journalctl --vacuum-size=200M` | Reduce journal to maximum size |
| `journalctl --vacuum-time=7d` | Remove entries older than 7 days |
| `journalctl -xe` | Recent entries with explanatory hints (useful for errors) |
| `logger "message"` | Write a test entry to the journal from the shell |

## Code Examples

### Service failure investigation script

```bash
#!/bin/bash
# investigate-service.sh — quick journal triage for a failed unit
set -euo pipefail

UNIT="${1:?Usage: $0 <unit.service>}"

echo "=== Status: $UNIT ==="
systemctl status "$UNIT" --no-pager -l || true

echo
echo "=== Last 30 journal lines ==="
journalctl -u "$UNIT" -n 30 --no-pager

echo
echo "=== Errors since last boot ==="
journalctl -u "$UNIT" -b -p err --no-pager
```

### Export logs for a support ticket

```bash
#!/bin/bash
# export-logs.sh — bundle recent errors for offline review
set -euo pipefail

OUT="/tmp/journal-export-$(date +%Y%m%d-%H%M%S).txt"

{
  echo "Host: $(hostname)"
  echo "Date: $(date -Iseconds)"
  echo "=== Errors (current boot) ==="
  journalctl -b -p err --no-pager
  echo "=== Failed units ==="
  systemctl --failed --no-pager
} > "$OUT"

echo "Exported to $OUT"
```

### Cron-friendly log vacuum (maintenance)

```bash
# Run weekly via root crontab to prevent journal bloat
0 3 * * 0 /usr/bin/journalctl --vacuum-size=500M
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Assuming logs survive reboot without persistent storage"
    Default volatile journals in `/run/log/journal/` are lost on reboot. Enable `Storage=persistent` on servers you need to forensically analyse after incidents.

!!! warning "Using grep on binary journal files directly"
    Never `grep` files under `/var/log/journal/` — they are binary. Always use `journalctl` for queries.

!!! warning "Forgetting sudo for other users' private journals"
    Users can read their own session logs, but full system logs require root or membership in the `systemd-journal` group (distribution-dependent).

!!! warning "Overly broad time filters on busy hosts"
    Querying millions of lines without `-n`, `--since`, or unit filters can exhaust memory and I/O. Narrow filters first.

## Best Practices

!!! tip "Start with unit + boot + priority"
    Production triage pattern: `journalctl -u APP -b -p err -n 50 --no-pager`

!!! tip "Set retention limits proactively"
    Configure `SystemMaxUse` and `MaxRetentionSec` before disk fills — especially on small root volumes.

!!! tip "Forward to centralized logging"
    Ship journal data to Elasticsearch, Loki, Splunk, or CloudWatch for correlation across hosts and long-term retention.

!!! tip "Correlate with systemd status"
    Always pair `journalctl -u UNIT` with `systemctl status UNIT` for exit codes and dependency context.

!!! tip "Use JSON in automation"
    Parse `-o json` output with `jq` rather than fragile regex on plain text.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No logs for previous boot | Volatile journal only | Enable `Storage=persistent` in `journald.conf` |
| `Permission denied` | Non-root user querying system logs | Use `sudo journalctl` or add user to `systemd-journal` group |
| Journal consuming too much disk | No vacuum limits configured | Set `SystemMaxUse`; run `journalctl --vacuum-size=500M` |
| Unit filter returns nothing | Wrong unit name | Run `systemctl list-units --type=service`; use exact name with `.service` suffix |
| `-f` shows nothing | No new log activity | Generate test entry with `logger`; verify service is running |
| Timestamps look wrong | Timezone or NTP drift | Check `timedatectl status`; sync with NTP |
| Missing application logs | App writes to file, not stdout | Configure app logging to journal or read app-specific log files |

## Summary

- The systemd journal stores structured, indexed logs with rich metadata for units, priorities, and boots.
- `journalctl` filters by `-u` (unit), `-p` (priority), `-b` (boot), and time ranges — the core production toolkit.
- Use `-f` for live tailing during deploys and incidents; use `-o json` for automation.
- Enable persistent storage and retention limits on production servers to preserve logs across reboots and control disk usage.
- Combine journal queries with `systemctl status` and centralized log forwarding for complete observability.

## Interview Questions

**1. Where does systemd store journal files, and what is the difference between volatile and persistent storage?**

*Sample answer:* Volatile journals live in `/run/log/journal/` and are cleared on reboot. Persistent journals are stored in `/var/log/journal/` when `Storage=persistent` is set in `/etc/systemd/journald.conf`. Production servers use persistent storage for post-incident analysis.

**2. How do you show only error-level messages from the current boot?**

*Sample answer:* `journalctl -b -p err --no-pager`. The `-p err` filter includes emerg, alert, crit, and err priorities.

**3. How do you view logs from the previous boot after a crash?**

*Sample answer:* `journalctl --list-boots` to identify boot indices, then `journalctl -b -1` for the previous session. This requires persistent journaling if the crash prevented clean shutdown flushing.

**4. What is the equivalent of `tail -f` for systemd logs?**

*Sample answer:* `journalctl -f` follows new entries. Add `-u UNIT` to follow a specific service.

**5. How do you investigate why nginx failed to start?**

*Sample answer:* Run `systemctl status nginx`, then `journalctl -u nginx -b -n 50 --no-pager`. Look for configuration syntax errors, port conflicts, or permission issues in the output.

**6. How can you reduce journal disk usage without disabling logging?**

*Sample answer:* Use `journalctl --vacuum-size=500M` or `--vacuum-time=30d`, and set `SystemMaxUse` in `journald.conf` for automatic limits.

**7. Why might an application log appear in `/var/log/app.log` but not in journalctl?**

*Sample answer:* The application writes directly to a file instead of stdout/stderr. Only processes connected to systemd's standard streams or using `sd_journal` API appear in the journal unless configured otherwise.

**8. What output format would you use to ingest logs into a SIEM?**

*Sample answer:* JSON via `journalctl -o json` or `json-pretty`, optionally with time and unit filters. Many forwarders (Fluent Bit, Filebeat with journald input) read the journal natively.

**9. What does `journalctl -xe` show, and when is it useful?**

*Sample answer:* Recent entries with additional explanatory text from systemd — helpful when a service fails and systemd prints suggested diagnostic commands.

**10. How do priority ranges work in journalctl?**

*Sample answer:* `-p warning..err` shows warnings through errors inclusive. You can also use numeric forms like `-p 3` for a single level.

1. How would you explain log management journalctl to a junior engineer in two minutes?
2. What production failure mode appears when teams ignore log management journalctl?
3. Which metrics or logs would you check first when log management journalctl misbehaves?
4. What is a secure default related to log management journalctl?
5. How would you validate a change involving log management journalctl in CI or a staging environment?
6. What trade-off would you accept to simplify operations around log management journalctl?
7. Describe a common anti-pattern with log management journalctl and how you fix it.
8. How does log management journalctl interact with networking, identity, or storage in a real system?
9. What would you put on a runbook checklist for log management journalctl?
10. When would you intentionally not follow the default approach taught here?

## Related Tutorials

- [Linux – Category Overview](index.md)
- [systemd Service Management](systemd-service-management.md)
- [Disk and Filesystem Management](disk-and-filesystem-management.md) *(previous)*
- [Cron and Task Scheduling](cron-and-task-scheduling.md) *(next)*
- [Troubleshooting Linux Systems](troubleshooting-linux-systems.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)
- Cheat sheet: [Linux Cheat Sheet](../cheatsheets/linux.md)
- Interview prep: [Linux Interview Prep](../interview/linux.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [systemd-journald documentation](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html)
- [journalctl man page](https://www.freedesktop.org/software/systemd/man/journalctl.html)
- [Linux man pages online – journalctl](https://man7.org/linux/man-pages/man1/journalctl.1.html)
- [systemd journal configuration](https://www.freedesktop.org/software/systemd/man/journald.conf.html)
- [REBASH Academy – Linux Overview](index.md)
