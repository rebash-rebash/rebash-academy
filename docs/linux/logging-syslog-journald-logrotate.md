---
title: "Logging — syslog, journald, and logrotate"
description: "Follow the logging stack — syslog, journald, and logrotate — on modern Linux servers."
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - syslog
  - journald
  - logrotate
prerequisites:
  - Scheduling with cron, at, and Timers
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# Logging — syslog, journald, and logrotate

## Overview

If it is not logged, it did not happen during the incident review.

This is **Tutorial 18** in **Module 12: Logging & Monitoring** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- Scheduling with cron, at, and Timers
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Logging — syslog, journald, and logrotate” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for Logging — syslog, journald, and logrotate](../assets/excalidraw/linux-logging.svg)

## Theory

### What it is

Linux logging typically combines three layers: **syslog** daemons (`rsyslog` or `syslog-ng`) writing classic text files under `/var/log`; **journald** storing structured, indexed logs for systemd units; and **logrotate** preventing those files from filling disks by rotating, compressing, and eventually deleting them. Applications may log via the syslog API, directly to files, or to stdout collected by a supervisor.

### Why it matters

Without logs you cannot reconstruct incidents; without rotation you create the incident (disk full). Enterprises forward both journal and syslog streams to a Security Information and Event Management (SIEM) or central store. Knowing where authentication events land (`auth.log`/`secure` versus `journalctl -u ssh`) speeds investigation. Mis-tuned `postrotate` hooks leave nginx or rsyslog writing to deleted inodes.

### How it works

Traditional files include `syslog`/`messages`, `auth.log`/`secure`, and application files under `/var/log`. `tail` and `grep` still matter for quick checks. journald is queried with `journalctl` by boot (`-b`), unit (`-u`), priority (`-p`), and time. Persistence requires `/var/log/journal` (and adequate disk). logrotate reads `/etc/logrotate.conf` and `/etc/logrotate.d/*`; policies set frequency, `compress`, `delaycompress`, retention, and scripts that signal writers to reopen files. Test with `logrotate -d` (debug, no changes). Forwarding configs ship selected facilities to remote collectors over TLS where required.

### Key concepts and comparisons

| System | Strength |
|--------|----------|
| syslog files | Simple, widely parsed, easy to tail |
| journald | Structured fields, unit correlation |
| Central SIEM | Fleet search, retention, alerting |
| logrotate | Local disk hygiene for file logs |

| Policy knob | Effect |
|-------------|--------|
| rotate / weekly | How often a new file starts |
| compress | Saves space after rotation |
| postrotate | Reload the writer safely |
| maxsize | Rotate early if growth spikes |

### Common pitfalls

- Assuming the journal survives reboot when it is volatile-only.
- Rotating files without signalling the daemon — space not freed correctly.
- Keeping verbose debug logs forever on small cloud root disks.
- Grepping only `/var/log/syslog` while the service only logs to the journal.
- Shipping logs without redacting secrets or access tokens.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab18 && cd ~/rebash-linux/lab18
```

**Focus:** query journal and /var/log; dry-run logrotate; draft a rotate stanza

### Step 1 – Logging paths

```bash
journalctl -b -n 10 --no-pager 2>/dev/null | tee journal.txt || true
ls /var/log | head | tee var-log.txt
sudo logrotate -d /etc/logrotate.conf 2>&1 | head -n 40 | tee logrotate-debug.txt || true
cat > app.logrotate.example << 'EOF'
/var/log/rebash-app/*.log {
  weekly
  rotate 4
  compress
  missingok
  notifempty
}
EOF
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-linux/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab18/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **Logging — syslog, journald, and logrotate** always combines:

1. Inspect before you change (`status`, `df`, `ip`, logs)
2. Prefer reversible, documented changes (config management, drop-ins)
3. Capture evidence (command output, journal snippets) for handovers
4. Prefer `systemctl`/`journalctl` and `ip`/`ss` over legacy tools
5. Least privilege — escalate with `sudo` only when required

Keep runbooks short enough to follow at 03:00. Automate the boring checks; keep humans for judgement.

## Security Considerations

- Treat host access and sudo as privileged — audit who can do what
- Never paste secrets into shell history, tickets, or screenshots
- Validate device names and paths before destructive disk or `rm` operations
- Prefer key-based SSH and deny password auth on internet-facing hosts
- Collect logs centrally; restrict who can read authentication and audit trails

## Common Mistakes

!!! warning "Using legacy networking tools by default"
    `ifconfig`/`netstat` are missing or incomplete on modern images. **Fix:** use `ip` and `ss`.

!!! warning "Editing vendor unit files in place"
    Package upgrades overwrite `/lib/systemd/system`. **Fix:** `systemctl edit` drop-ins under `/etc`.

!!! warning "Trusting df without checking inodes and mounts"
    A full `/var` or exhausted inodes looks different from root. **Fix:** `df -h`, `df -i`, and `findmnt`.

## Best Practices

- Golden images + config as code over snowflake hosts
- Alert on symptoms (failed units, disk, load) with runbooks attached
- Time-sync (chrony) everywhere — logs and TLS depend on it
- Separate OS and data volumes on Cloud VMs
- Practise restore and rescue paths before you need them

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Permission denied | Mode/owner/ACL/MAC | `namei -l`, `id`, `getfacl`, SELinux/AppArmor logs |
| No route / timeout | Routing, DNS, firewall | `ip route`, `dig`, `ss`, security groups |
| Service won’t start | Unit/config/deps | `systemctl status`, `journalctl -u`, config `-t` |
| Disk full | Logs, containers, deleted-open | `df`/`du`, `lsof +L1`, rotate/expand |
| High load | CPU, I/O wait, thrash | `vmstat`, `iostat`, `ps` |

## Summary

**Logging — syslog, journald, and logrotate** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

## Interview Questions

1. How does this topic show up when operating Cloud VMs or Kubernetes nodes?
2. What would you check first if this area misbehaves in production?
3. Which modern Linux tools replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI or a cron/timer job?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, then gather host signals (`systemctl --failed`, `df`, `ip`/`ss`, `journalctl`) before making changes. Fix forward with evidence, not guesswork.

## Related Tutorials

- [Linux for Cloud & DevOps – Category Overview](index.md)
- [Scheduling with cron, at, and Timers](scheduling-cron-at-and-timers.md) *(previous)*
- [Host Monitoring with vmstat, iostat, and sar](host-monitoring-vmstat-iostat-sar.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
