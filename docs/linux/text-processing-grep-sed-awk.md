---
title: "Text Processing with grep, sed, and awk"
description: "Filter and transform logs and configs with grep, sed, awk, cut, paste, tr, sort, uniq, wc, and xargs."
difficulty: intermediate
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - grep
  - sed
  - awk
  - pipelines
prerequisites:
  - Permissions, ACLs, and Special Bits
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# Text Processing with grep, sed, and awk

## Overview

Ops is text: logs, configs, CSV exports. These tools are your incident and automation toolkit.

This is **Tutorial 8** in **Module 5: Text Processing** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- Permissions, ACLs, and Special Bits
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Text Processing with grep, sed, and awk” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for Text Processing with grep, sed, and awk](../assets/images/linux-text-processing.svg)

## Theory

### grep

Search lines by pattern:

```bash
grep -RIn --exclude-dir=.git ERROR /var/log 2>/dev/null | head
grep -E '^(error|warn)' app.log
grep -v '^#' /etc/ssh/sshd_config
```

### sed

Stream editor for substitutions and deletes:

```bash
sed -n '1,20p' file
sed 's/foo/bar/g' file
sed -i.bak 's/Enable=false/Enable=true/' config.ini
```

### awk

Field-oriented reporting:

```bash
awk '{print $1,$3}' access.log
awk -F: '{print $1}' /etc/passwd
awk '{sum+=$1} END {print sum}' nums.txt
```

### cut, paste, tr

```bash
cut -d: -f1,7 /etc/passwd | head
paste -d',' a.txt b.txt
tr '[:upper:]' '[:lower:]' < mixed.txt
```

### sort, uniq, wc

```bash
sort file | uniq -c | sort -nr | head
wc -l file
```

### xargs

Build command lines from stdin (prefer `-0` with `find -print0`):

```bash
find . -name '*.log' -print0 | xargs -0 grep -l ERROR
```

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab08 && cd ~/rebash-linux/lab08
```

**Focus:** build a log pipeline with grep/sed/awk/sort/uniq/xargs

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab08 text-processing-grep-sed-awk on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Log pipeline

```bash
cat > sample.log << 'EOF'
INFO start
ERROR disk full
WARN retry
ERROR timeout
INFO done
EOF
grep ERROR sample.log | tee errors.txt
sed 's/ERROR/ERR/g' sample.log | tee sed-out.txt
awk '/ERR|ERROR/{c++} END{print c+0}' sample.log | tee count.txt
cut -d' ' -f1 sample.log | sort | uniq -c
printf 'a\nb\n' | tr 'a-z' 'A-Z'
echo errors.txt | xargs wc -l
```

### Final step – Cleanup note

```bash
./lab.sh
# keep ~/rebash-linux for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab08/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **Text Processing with grep, sed, and awk** always combines:

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

**Text Processing with grep, sed, and awk** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

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
- [Permissions, ACLs, and Special Bits](permissions-acls-and-special-bits.md) *(previous)*
- [Process Management](process-management.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
