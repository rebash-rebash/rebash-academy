---
title: "Backup, Disaster Recovery, and Capacity"
description: "Design backup strategies and disaster recovery drills, with capacity planning overlapping production ops."
difficulty: advanced
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - backup
  - dr
  - capacity
prerequisites:
  - Production Linux — Hardening and Performance
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# Backup, Disaster Recovery, and Capacity

## Overview

Backups that were never restored are fiction. DR is a practised procedure, not a folder of tar files.

This is **Tutorial 25** in **Module 16: Production Linux** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- Production Linux — Hardening and Performance
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Backup, Disaster Recovery, and Capacity” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for Backup, Disaster Recovery, and Capacity](../assets/excalidraw/linux-backup-dr.svg)

## Theory

### What it is

**Backups** create recoverable copies of data: file-level tools (`tar`, `rsync`, Borg, restic), block/volume snapshots from the cloud provider, and application-aware dumps that quiesce databases. **Disaster recovery (DR)** is the plan and practise to restore service within a Recovery Time Objective (RTO) and Recovery Point Objective (RPO). **Capacity** planning ensures disks, snapshot retention, and restore targets have space and budget before growth or restore day.

### Why it matters

Untested backups are theatre. Ransomware, accidental `rm`, failed migrations, and region issues all demand restore paths that include Identity and Access Management (IAM) and SSH break-glass access — not only data tarballs. Snapshot bills grow quietly; retention without a policy surprises finance. Capacity alerts that fire at 95% leave no time to expand before write failures.

### How it works

Choose patterns per dataset: volume snapshots for whole disks, file-level for selective trees, native DB tools for consistency. Follow **3-2-1** thinking: three copies, two media/types, one offsite or other region. Encrypt backups and control who can restore. Document RTO/RPO and drill: restore to a scratch VM, verify checksums and services, time the exercise. Include how operators regain access if the bastion dies. Watch `df`/`du` trends and snapshot age; expire old restores and unused snapshots. Application-aware steps (flush, snapshot, thaw) beat crashing disks mid-write.

### Key concepts and comparisons

| Pattern | Notes |
|---------|-------|
| File-level | Selective; good for configs and homes |
| Volume snapshot | Fast; watch consistency and cost |
| Application-aware | Required for many databases |
| 3-2-1 | Diversify copies and locations |

| Term | Meaning |
|------|---------|
| RTO | How long restore may take |
| RPO | How much data loss is tolerable |

### Common pitfalls

- Never testing restore — only testing that the backup job exited zero.
- Snapshotting busy databases without flush/quiesce.
- Storing backups on the same disk or same account without separation.
- Ignoring IAM/SSH recovery in the DR runbook.
- Infinite snapshot retention without a capacity or cost review.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab25 && cd ~/rebash-linux/lab25
```

**Focus:** script a local backup+restore drill; document RTO/RPO assumptions

### Step 1 – Backup and restore drill

```bash
mkdir -p data restore
echo 'important' > data/note.txt
tar -czf backup-data.tgz -C data .
rm -rf restore/*
tar -xzf backup-data.tgz -C restore
diff -u data/note.txt restore/note.txt
cat > dr-notes.md << 'EOF'
RPO: 24h (daily snapshot)
RTO: 2h (restore volume + verify service)
Last drill: $(date -I)
EOF
ls -l backup-data.tgz restore
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-linux/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab25/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **Backup, Disaster Recovery, and Capacity** always combines:

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

**Backup, Disaster Recovery, and Capacity** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

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
- [Production Linux — Hardening and Performance](production-linux-hardening-and-performance.md) *(previous)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
