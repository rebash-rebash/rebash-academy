---
title: Troubleshooting Linux Systems
description: Systematic debugging for boot, disk, network, and performance issues using the USE method.
difficulty: advanced
estimated_time: "60 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
  - troubleshooting
  - debugging
  - performance
prerequisites:
  - Completion of Modules 1–5 Linux tutorials
  - Familiarity with systemd, networking, and disk management
comments: false
---

# Troubleshooting Linux Systems

## Overview

Production Linux failures rarely announce their root cause. A web app returns 502, SSH hangs, cron silently stops, or the server reboots overnight — and you must determine whether the problem is disk, memory, network, configuration, or application code. Effective administrators follow a **systematic approach** rather than random command execution.

This tutorial teaches the **USE method** (Utilization, Saturation, Errors) for performance debugging, structured workflows for **boot failures**, **full disks**, **network outages**, and **resource exhaustion**, and habits that turn firefighting into repeatable diagnosis.

This tutorial is part of **Module 6: Storage, Logs, Networking & Operations** in the REBASH Academy Linux series — the capstone operations tutorial.

## Prerequisites

- Complete Modules 1–5 including [systemd Service Management](systemd-service-management.md), [Log Management with journalctl](log-management-journalctl.md), and [Linux Networking Essentials](linux-networking-essentials.md)
- A Linux VM where you can safely simulate issues (disk fill, failed service)
- `sudo` privileges for system-level diagnostics
- Comfort reading logs and command output under pressure

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply a systematic troubleshooting workflow: reproduce, isolate, collect, hypothesize, fix, document
- [ ] Use the USE method to diagnose CPU, memory, disk, and network bottlenecks
- [ ] Diagnose boot failures using journalctl, systemd targets, and rescue mode concepts
- [ ] Resolve full-disk emergencies without data loss
- [ ] Triage network and performance issues with a layered diagnostic model

## Architecture

This topic is primarily procedural. The mental model is a straight line from inputs (commands, config files, or manifests) to observable system state — verify each change with the validation steps later in this tutorial.

## Theory

### The systematic troubleshooting workflow

1. **Reproduce** — Confirm the symptom. Intermittent issues need triggers identified.
2. **Isolate** — One host or all? One service or entire stack? Recent changes?
3. **Collect evidence** — Logs, metrics, configs, timelines. Do not change state yet.
4. **Hypothesize** — Form ranked theories based on evidence.
5. **Test fix** — Change one variable at a time; verify resolution.
6. **Document** — Postmortem, runbook update, monitoring gap closed.

Ask: **What changed?** Deployments, patches, config edits, traffic spikes, and certificate expiry cause most incidents.

### The USE method

From Brendan Gregg's performance methodology — for each resource, check:

| Letter | Question | Example tools |
|--------|----------|---------------|
| **U**tilization | How busy is it? | `mpstat`, `free`, `df`, `ip -s` |
| **S**aturation | Is work queued/waiting? | load average, `iostat`, swap usage, NIC drops |
| **E**rrors | Are errors occurring? | `dmesg`, `journalctl -p err`, `netstat -s`, SMART |

Apply USE to: CPU, memory, disk I/O, network interfaces, and application-specific queues.

### Boot troubleshooting

Boot failures often stem from:

- Filesystem errors (dirty unmount, full disk)
- Failed systemd units blocking target (`default.target`)
- Incorrect `/etc/fstab` entries
- Broken initramfs or kernel updates
- Network dependencies for remote mounts (NFS, iSCSI)

Diagnostic commands (when system is up):

```bash
systemctl --failed
journalctl -b -p err
journalctl -b -1   # previous boot
```

Recovery concepts: **single-user mode**, **rescue.target**, boot with previous kernel from GRUB, init=/bin/bash for emergency shell (advanced).

### Full / full disk issues

When disk fills:

- Writes fail (`No space left on device`)
- Services crash (databases, logs, temp files)
- SSH may fail (cannot write utmp, session files)

Find consumers:

```bash
df -h
du -sh /* 2>/dev/null | sort -hr | head
journalctl --disk-usage
lsof +L1   # deleted files still held open
```

Common culprits: `/var/log`, journal, `/tmp`, core dumps, unrotated logs, Docker overlay2.

### Network troubleshooting

Use the layered model from [Linux Networking Essentials](linux-networking-essentials.md):

1. Link up? (`ip link`)
2. IP assigned? (`ip addr`)
3. Route to destination? (`ip route get`)
4. DNS resolves? (`dig`)
5. Port reachable? (`ss`, `nc`, `curl`)
6. Firewall blocking? (local + cloud SG)

### Performance troubleshooting

High load is not always CPU — check **I/O wait** (`top`, `wa` column), swap thrashing, and blocked processes.

| Symptom | Likely cause | First checks |
|---------|--------------|--------------|
| Slow SSH login | DNS reverse lookup, PAM, disk full | `sshd -ddd`, `df -h`, `/etc/nsswitch.conf` |
| High load, low CPU | Disk I/O saturation | `iostat -x 1`, `iotop` |
| OOM kills | Memory exhaustion | `dmesg \| grep -i oom`, `journalctl -k` |
| Service timeouts | Network, DB, thread pool | `ss -s`, app logs, connection counts |

### What not to do

- Restart services randomly without collecting logs
- Delete files in `/var/log` without identifying cause
- Run `kill -9` on processes without understanding state
- Apply multiple fixes simultaneously — you won't know what worked

## Hands-on Lab

### Step 1 – System health snapshot

Build a baseline "health card" you can run on any server:

```bash
echo "=== Uptime & Load ==="
uptime
echo "=== Memory ==="
free -h
echo "=== Disk ==="
df -h /
echo "=== Failed units ==="
systemctl --failed --no-pager
echo "=== Recent errors ==="
journalctl -b -p err --no-pager | tail -5
```

**Expected output:** Load averages, memory available, root filesystem usage under 80%, ideally no failed units, recent errors if any.

### Step 2 – Apply USE to CPU and memory

```bash
echo "=== CPU utilization ==="
mpstat 1 3 2>/dev/null || top -bn1 | head -5
echo "=== Memory USE ==="
free -h
vmstat 1 3
```

**Expected output:** CPU idle percentage, swap usage (should be 0 or minimal on healthy server), vmstat si/so columns near zero (no swap thrashing).

### Step 3 – Investigate failed services

```bash
systemctl --failed --no-pager
# If a test unit exists, inspect; otherwise review ssh status as example:
systemctl status ssh 2>/dev/null || systemctl status sshd --no-pager | head -15
journalctl -u ssh -u sshd -b -n 10 --no-pager 2>/dev/null | tail -5
```

**Expected output:** Failed unit list (empty on healthy system); status shows active (running) with recent log lines.

### Step 4 – Simulate and diagnose disk pressure

```bash
mkdir -p /tmp/disk-lab
df -h /tmp
# Create a large file (adjust size if needed)
dd if=/dev/zero of=/tmp/disk-lab/fillfile bs=1M count=50 2>/dev/null
du -sh /tmp/disk-lab
df -h /
rm /tmp/disk-lab/fillfile
echo "Cleaned up lab file"
```

**Expected output:** `du` shows ~50M; after cleanup, disk usage returns to prior level.

Find largest directories on a real system:

```bash
sudo du -xh /var 2>/dev/null | sort -hr | head -10
journalctl --disk-usage
```

### Step 5 – Find deleted files still consuming space

```bash
sudo lsof +L1 2>/dev/null | head -5 || echo "No deleted open files (good)"
```

**Expected output:** Empty or list of processes holding deleted log files — restart those services to reclaim space.

### Step 6 – Network layered check

```bash
GW=$(ip route | awk '/default/ {print $3}')
ping -c 2 "$GW" && echo "L3 gateway OK" || echo "Gateway FAIL"
ping -c 2 8.8.8.8 && echo "External IP OK" || echo "Routing FAIL"
getent hosts google.com && echo "DNS OK" || echo "DNS FAIL"
ss -s
```

**Expected output:** All OK lines on healthy network; `ss -s` summary of TCP/UDP socket counts.

### Step 7 – Identify resource-heavy processes

```bash
ps aux --sort=-%mem | head -6
ps aux --sort=-%cpu | head -6
```

**Expected output:** Top memory and CPU consumers with PID, user, and command — useful during performance incidents.

### Step 8 – Boot and kernel message review

```bash
journalctl --list-boots | tail -3
dmesg -T 2>/dev/null | tail -10 || sudo dmesg | tail -10
journalctl -k -b -p warning..emerg --no-pager | tail -10
```

**Expected output:** Recent boot sessions; kernel messages without critical hardware errors on healthy VM.

### Step 9 – Document a mock incident

Create a minimal incident note template:

```bash
cat > /tmp/incident-template.md << 'EOF'
# Incident: [title]
- **Start:** 
- **Impact:** 
- **Symptoms:** 
- **Timeline:** 
- **Root cause:** 
- **Fix:** 
- **Follow-up:** monitoring / runbook / patch
EOF
cat /tmp/incident-template.md
```

**Expected output:** Template ready for post-incident documentation practice.

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
| `uptime` | Load averages and uptime |
| `free -h` | Memory and swap usage |
| `df -h` | Filesystem disk usage |
| `du -sh PATH` | Directory size summary |
| `du -xh / \| sort -hr \| head` | Find large directories |
| `systemctl --failed` | List failed systemd units |
| `journalctl -b -p err` | Errors since boot |
| `journalctl -b -1` | Previous boot logs |
| `journalctl -u UNIT -n 50` | Service-specific logs |
| `dmesg -T` | Kernel ring buffer with timestamps |
| `lsof +L1` | Deleted files still open |
| `vmstat 1 5` | Virtual memory statistics |
| `mpstat -P ALL 1 3` | Per-CPU utilization |
| `iostat -x 1 3` | Disk I/O statistics |
| `top` / `htop` | Interactive process monitor |
| `ps aux --sort=-%mem` | Processes by memory |
| `ss -s` | Socket summary statistics |
| `strace -p PID` | Trace system calls (advanced) |
| `systemd-analyze blame` | Boot time per unit |
| `systemd-analyze critical-chain` | Boot dependency chain |

## Code Examples

### One-liner health check script

```bash
#!/bin/bash
# health-check.sh — run during incidents for quick triage
set -euo pipefail

warn() { echo "[WARN] $*"; }
ok()   { echo "[OK]   $*"; }

load=$(awk '{print $1}' /proc/loadavg)
cpus=$(nproc)
awk -v l="$load" -v c="$cpus" 'BEGIN { exit (l > c * 2) ? 0 : 1 }' \
  && warn "Load high: $load (${cpus} CPUs)" || ok "Load: $load"

avail=$(free -m | awk '/Mem:/ {print $7}')
[ "$avail" -lt 256 ] && warn "Low memory: ${avail}MB avail" || ok "Memory avail: ${avail}MB"

use=$(df -h / | awk 'NR==2 {gsub(/%/,""); print $5}')
[ "$use" -gt 90 ] && warn "Disk / at ${use}%" || ok "Disk / at ${use}%"

failed=$(systemctl --failed --no-legend | wc -l)
[ "$failed" -gt 0 ] && warn "$failed failed units" || ok "No failed units"
```

### Disk emergency cleanup (use with care)

```bash
#!/bin/bash
# disk-emergency.sh — identify top consumers, vacuum journal
set -euo pipefail
echo "=== Top /var consumers ==="
sudo du -xh /var 2>/dev/null | sort -hr | head -15
echo "=== Journal usage ==="
journalctl --disk-usage
echo "=== Vacuum journal to 200M ==="
sudo journalctl --vacuum-size=200M
echo "=== After cleanup ==="
df -h /
```

### Boot failure investigation

```bash
#!/bin/bash
echo "=== Failed units ==="
systemctl --failed --no-pager
echo "=== Boot errors ==="
journalctl -b -p err --no-pager | tail -30
echo "=== Boot time analysis ==="
systemd-analyze blame | head -15
echo "=== Critical chain ==="
systemd-analyze critical-chain default.target | head -20
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Rebooting as the first action"
    Reboot clears ephemeral evidence (memory state, some logs). Collect logs and metrics first unless the system is truly hung.

!!! warning "Deleting logs to free space without fixing the cause"
    Log rotation and journal limits address recurrence. Deleting alone guarantees the problem returns.

!!! warning "Ignoring swap and I/O wait"
    High load with idle CPU often means disk bottleneck — not a CPU problem. Check `iostat` and `wa` in top.

!!! warning "Multiple simultaneous changes"
    Change one variable at a time so you know what fixed the issue and what to rollback if needed.

!!! warning "Skipping the what-changed question"
    Most incidents correlate with recent deploys, config edits, or certificate expiry — check change history first.

## Best Practices

!!! tip "Maintain a standard triage runbook"
    First 5 minutes: uptime, df, free, systemctl --failed, journalctl -p err. Same script on every incident.

!!! tip "Set proactive alerts"
    Alert on disk > 80%, memory pressure, failed systemd units, and elevated error log rates before users notice.

!!! tip "Practice break-fix in staging"
    Simulate full disk, killed services, and DNS failures in non-prod to build muscle memory.

!!! tip "Use USE method consistently"
    Prevents tunnel vision on CPU when the real problem is disk saturation or network errors.

!!! tip "Write postmortems blamelessly"
    Document timeline, root cause, and preventive actions — the best troubleshooting improves future systems.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `No space left on device` | Full filesystem | `df -h`; find with `du`; vacuum journal; rotate logs; extend volume |
| System won't boot | fstab error, failed unit | Boot rescue; check `journalctl -b -1`; comment bad fstab line |
| SSH extremely slow | DNS reverse lookup timeout | Set `UseDNS no` in sshd_config; fix DNS or `/etc/hosts` |
| OOM killer invoked | Memory exhaustion | Identify process with `dmesg`; add swap short-term; fix leak/limit |
| Load average >> CPU count | I/O wait or uninterruptible sleep | `iostat`, `iotop`; check storage and NFS mounts |
| Service active but not responding | App hung, port not bound | `ss -tlnp`; check app logs; restart with journal capture |
| Intermittent failures | Resource limits, timeouts | Check `ulimit -a`, connection pools, cron overlap |
| High journal disk usage | No retention limits | `journalctl --vacuum-size`; configure `SystemMaxUse` |
| Deleted files still using space | Process holds open fd | `lsof +L1`; restart service or send HUP to release |
| After kernel update, boot fails | Incompatible module/driver | Boot previous kernel from GRUB; investigate dkms/modules |

## Summary

- Follow reproduce → isolate → collect → hypothesize → fix → document for every incident.
- USE method (Utilization, Saturation, Errors) applies to CPU, memory, disk, and network resources.
- Boot issues: check `systemctl --failed`, `journalctl -b`, previous boot logs, and fstab.
- Full disk: `df`, `du`, journal vacuum, log rotation, and `lsof +L1` for deleted open files.
- Network and performance problems yield to layered checks — never skip "what changed?" and always collect evidence before rebooting.

## Interview Questions

**1. Describe your systematic approach to troubleshooting a down production server.**

*Sample answer:* Confirm scope and reproduce. Collect uptime, disk, memory, failed units, and error logs without changing state. Form hypotheses ranked by likelihood and recent changes. Test one fix at a time. Verify recovery and document.

**2. What is the USE method?**

*Sample answer:* For each resource, check Utilization (how busy), Saturation (queueing/waiting), and Errors. Applied to CPU, memory, disk, and network to quickly narrow performance bottlenecks.

**3. A server has load average of 50 but CPU shows 95% idle. What do you investigate?**

*Sample answer:* Likely I/O wait or processes in uninterruptible sleep (D state). Check `top` wa column, `iostat -x`, NFS/storage mounts, and `ps aux` for D state processes.

**4. How do you troubleshoot a full root filesystem?**

*Sample answer:* `df -h` confirms; `du -xh` finds large dirs; check journal with `journalctl --disk-usage`; look for deleted open files with `lsof +L1`; rotate or vacuum logs; extend volume if needed.

**5. How do you investigate why a service failed to start at boot?**

*Sample answer:* `systemctl status UNIT`, `journalctl -u UNIT -b`, check dependencies with `systemctl list-dependencies`, verify config syntax, and review `/etc/fstab` if mount-related.

**6. What commands give you a quick health snapshot?**

*Sample answer:* `uptime`, `free -h`, `df -h`, `systemctl --failed`, `journalctl -b -p err -n 20`, `ss -s`.

**7. Why should you avoid rebooting immediately?**

*Sample answer:* Reboot destroys in-memory state and may rotate logs. Collect evidence first unless the system is unresponsive and reboot is the only recovery option.

**8. How do you view logs from the boot before a crash?**

*Sample answer:* `journalctl --list-boots` then `journalctl -b -1`. Requires persistent journaling enabled in journald.conf.

**9. SSH login takes 30 seconds. What are common causes?**

*Sample answer:* DNS reverse lookup timeout (UseDNS), GSSAPI auth delays, PAM modules, or disk full preventing session file creation. Test with `ssh -vvv`.

**10. What is the first question you ask during any incident?**

*Sample answer:* "What changed?" — recent deployments, config changes, patches, traffic spikes, or certificate expirations usually explain sudden failures.

1. How would you explain troubleshooting linux systems to a junior engineer in two minutes?
2. What production failure mode appears when teams ignore troubleshooting linux systems?
3. Which metrics or logs would you check first when troubleshooting linux systems misbehaves?
4. What is a secure default related to troubleshooting linux systems?
5. How would you validate a change involving troubleshooting linux systems in CI or a staging environment?
6. What trade-off would you accept to simplify operations around troubleshooting linux systems?
7. Describe a common anti-pattern with troubleshooting linux systems and how you fix it.
8. How does troubleshooting linux systems interact with networking, identity, or storage in a real system?
9. What would you put on a runbook checklist for troubleshooting linux systems?
10. When would you intentionally not follow the default approach taught here?

## Related Tutorials

- [Linux – Category Overview](index.md)
- [Linux Security Hardening Basics](linux-security-hardening-basics.md) *(previous)*
- [Log Management with journalctl](log-management-journalctl.md)
- [Linux Networking Essentials](linux-networking-essentials.md)
- [Disk and Filesystem Management](disk-and-filesystem-management.md)
- [systemd Service Management](systemd-service-management.md)
- [Process Management](process-management.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [Systems Performance – USE Method (Brendan Gregg)](https://www.brendangregg.com/usemethod.html)
- [systemd troubleshooting](https://www.freedesktop.org/software/systemd/man/systemd.debug-shell.html)
- [journalctl man page](https://www.freedesktop.org/software/systemd/man/journalctl.html)
- [Linux Performance Analysis (Red Hat)](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/monitoring_and_managing_system_status_and_performance/index)
- [SRE Workbook – Managing Incidents](https://sre.google/sre-book/managing-incidents/)
- [REBASH Academy – Linux Overview](index.md)
