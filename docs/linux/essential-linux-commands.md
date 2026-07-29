---
title: "Essential Linux Commands"
description: "Master everyday navigation and file commands — pwd, ls, cd, mkdir, rm, cp, mv, touch, cat, less, head, tail, stat, file, and history."
difficulty: beginner
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - cli
  - commands
  - navigation
prerequisites:
  - Boot Process and Filesystem Hierarchy
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# Essential Linux Commands

## Overview

Every SSH session starts here. Fluent use of these tools is the baseline for automation and incident response.

This is **Tutorial 3** in **Module 2: Command Line Essentials** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- Boot Process and Filesystem Hierarchy
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Essential Linux Commands” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for Essential Linux Commands](../assets/images/linux-essential-commands.svg)

## Theory

### Navigation and listing

| Command | Use |
|---------|-----|
| `pwd` | Print working directory |
| `ls` | List directory entries (`-la`, `-lh`, `-lt`, `--color`) |
| `cd` | Change directory (`cd -` previous, `cd` or `cd ~` home) |

### Create, copy, move, remove

| Command | Use |
|---------|-----|
| `mkdir` | Create directories (`-p` parents) |
| `touch` | Create empty file or update mtime |
| `cp` | Copy (`-a` archive, `-r` recursive) |
| `mv` | Move / rename |
| `rm` | Remove (`-r` recursive, `-i` interactive — respect production caution) |

Prefer `rm -I` or trash tools in shared environments. Never `rm -rf /` patterns with unquoted variables.

### Viewing content

| Command | Use |
|---------|-----|
| `cat` | Concatenate / print whole files (small files) |
| `less` | Page through files (`/search`, `q` quit) |
| `head` | First N lines (`-n`) |
| `tail` | Last N lines (`-n`, `-f` follow logs) |

### Metadata and history

| Command | Use |
|---------|-----|
| `stat` | Detailed inode metadata (size, times, mode) |
| `file` | Guess file type from content magic |
| `history` | Shell command history (`!n`, `Ctrl-R` reverse search) |

Combine with redirection (`>`, `>>`, `2>`) and pipes (`|`) — composition is the Linux ops superpower.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab03 && cd ~/rebash-linux/lab03
```

**Focus:** navigate lab tree; practise cp/mv/rm safely; use less/stat/history

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab03 essential-linux-commands on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Command workout

```bash
mkdir -p docs/bin
touch docs/readme.txt
echo 'hello rebash' > docs/readme.txt
cp docs/readme.txt docs/readme.copy
mv docs/readme.copy docs/readme.bak
head -n 1 docs/readme.txt
tail -n 1 docs/readme.txt
cat docs/readme.txt
less -f docs/readme.txt </dev/null || true
stat docs/readme.txt
file docs/readme.txt
history | tail -n 5 || true
ls -la docs
```

### Final step – Cleanup note

```bash
./lab.sh
# keep ~/rebash-linux for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab03/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **Essential Linux Commands** always combines:

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

**Essential Linux Commands** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

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
- [Boot Process and Filesystem Hierarchy](boot-process-and-filesystem-hierarchy.md) *(previous)*
- [Filesystem Paths, Links, Mounts, and Inodes](filesystem-paths-links-mounts-and-inodes.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
