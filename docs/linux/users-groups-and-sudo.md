---
title: "Users, Groups, and sudo"
description: "Create and manage users and groups, and escalate safely with sudo on Cloud Linux hosts."
difficulty: beginner
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - users
  - groups
  - sudo
  - identity
prerequisites:
  - Disk Usage and File Attributes
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# Users, Groups, and sudo

## Overview

Identity is the first control plane on a shared bastion or jump host. Get users, groups, and sudo right before permissions deep-dives.

This is **Tutorial 6** in **Module 4: Users & Permissions** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- Disk Usage and File Attributes
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Users, Groups, and sudo” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for Users, Groups, and sudo](../assets/images/linux-users-groups-sudo.svg)

## Theory

### Users

Each user has a UID, primary GID, home directory, and login shell — recorded in `/etc/passwd`, secrets in `/etc/shadow`.

```bash
id
getent passwd "$USER"
sudo useradd -m -s /bin/bash appuser
sudo passwd appuser   # or prefer SSH keys only
sudo userdel -r appuser
```

Service accounts often use `nologin`/`false` shells and locked passwords.

### Groups

Groups collect UIDs for shared access. Secondary groups appear in `/etc/group`.

```bash
getent group
sudo groupadd deployers
sudo usermod -aG deployers appuser
```

Cloud images commonly use a wheel/sudo/admin group for the default login user.

### sudo

**sudo** runs a command as another user (usually root) per `/etc/sudoers` and `/etc/sudoers.d/*`.

```bash
sudo -l
sudo -u root id
sudo visudo -f /etc/sudoers.d/99-rebash-lab
```

Prefer least privilege: command allow-lists over `ALL=(ALL) NOPASSWD:ALL` on production. Always edit with `visudo`.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab06 && cd ~/rebash-linux/lab06
```

**Focus:** inspect id/passwd; create lab user/group; practise sudo -l

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab06 users-groups-and-sudo on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Identity inventory

```bash
id | tee id.txt
getent passwd "$USER"
getent group | head
sudo -n -l 2>&1 | tee sudo-l.txt || true
echo "Create users only on disposable lab VMs with sudo."
```

### Final step – Cleanup note

```bash
./lab.sh
# keep ~/rebash-linux for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab06/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **Users, Groups, and sudo** always combines:

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

**Users, Groups, and sudo** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

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
- [Disk Usage and File Attributes](disk-usage-and-file-attributes.md) *(previous)*
- [Permissions, ACLs, and Special Bits](permissions-acls-and-special-bits.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
