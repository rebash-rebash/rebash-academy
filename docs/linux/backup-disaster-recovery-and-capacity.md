---
title: "Backup, Disaster Recovery, and Capacity"
description: "Practise backup and restore with tar and rsync, define a simple recovery objective, and check capacity signals on Ubuntu."
difficulty: intermediate
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 16 · Production Linux"
tags:
  - linux
  - backup
  - disaster-recovery
  - capacity
  - rsync
prerequisites:
  - linux/production-linux-hardening-and-performance
related:
  - linux/disk-usage-and-file-attributes
  - linux/lvm-swap-and-disk-monitoring
interview: interview/linux
comments: false
---

# Backup, Disaster Recovery, and Capacity

## Overview

A backup you have never restored is only a hope. **Backup** copies data so you can recover from deletion, corruption, or bad deploys. **Disaster Recovery (DR)** is the plan and practise to restore service after a larger failure (lost VM, lost region, lost disk). **Capacity** planning watches disk, CPU, and memory so you grow before you break.

Two numbers appear in every serious DR conversation: **Recovery Point Objective (RPO)** — how much data you can afford to lose (time since last good backup), and **Recovery Time Objective (RTO)** — how long recovery may take. In this tutorial you will create sample data, back it up with `tar` and `rsync`, destroy the original on purpose, restore, verify checksums, and capture capacity signals under `~/rebash-linux/lab25`.

In production, use platform tools too (cloud snapshots, database native backups, object storage). Host-level `tar`/`rsync` skills still matter for configs, small app trees, and proving you understand restore.

This is **Tutorial 25** in **Module 16: Production Linux** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers.

## Prerequisites

- [Production Hardening and Performance](production-linux-hardening-and-performance.md)
- A **practice Ubuntu 22.04/24.04 VM** with write space under `$HOME`
- Package `rsync` (install if missing)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain RPO and RTO in plain language
- [ ] Create a `tar` archive backup and restore it
- [ ] Mirror a directory with `rsync` and prove a restore after deletion
- [ ] Verify restored data with checksums
- [ ] Capture capacity signals (`df`, `du`) with the backup evidence under `~/rebash-linux/lab25`

## Architecture

Backups copy data to safe storage; DR restores service within RPO/RTO; capacity monitoring prevents “no space for backups” failures.

![Architecture diagram for Backup, Disaster Recovery, and Capacity](../assets/excalidraw/linux-backup-dr.svg)

## Theory

### What it is

| Term | Meaning |
|------|---------|
| Backup | Copy of data for restore |
| Restore test | Proving the copy works |
| RPO | Max acceptable data loss window |
| RTO | Max acceptable downtime to recover |
| Capacity | Headroom for growth and for backup storage |

```bash
tar -czf backup.tgz data/
rsync -aH data/ backup-mirror/
df -hT
```

### Why it matters

Ransomware, bad migrations, and accidental `rm` are normal risks. Cloud snapshots help, but application consistency and restore drills matter. Disks that are 95% full often fail the backup job first.

### How it works

1. Identify critical data and RPO/RTO  
2. Copy off-box when possible  
3. Automate schedules (cron/timer)  
4. **Restore regularly** into a scratch path  
5. Watch capacity of source and backup target  

| Tool | Good for |
|------|----------|
| `tar` | Portable archives of trees |
| `rsync` | Incremental mirrors |
| Snapshots | Whole disk/VM points in time |
| DB dumps | Consistent database recovery |

### Common pitfalls

- Backups on the same disk as the source only.  
- Never testing restore.  
- No room left for the backup target.  
- Backing up without application quiesce when consistency matters.

## Hands-on Lab

### Objective

Create sample app data, back it up with `tar` and `rsync`, delete the live data, restore from both methods, verify checksums, and pack evidence under `~/rebash-linux/lab25`.

### Prerequisites

- Ubuntu with `tar`, `rsync`, `sha256sum`

### Lab environment

Workspace: `~/rebash-linux/lab25`

```bash
mkdir -p ~/rebash-linux/lab25 && cd ~/rebash-linux/lab25
set -euo pipefail
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y rsync
df -hT . | tee df-before.txt
```

**Expected output:** `rsync` available; capacity snapshot stored.

### Real-world scenario

A small app keeps critical config and upload files under one directory. Leadership asks for an RPO of “last hourly backup” and proof that restore works. You rehearse archive + mirror backups, destroy the live tree, restore, and attach checksum proof to the DR document.

### Step-by-step tasks

#### Task 1 – Create data and checksum manifest

```bash
cd ~/rebash-linux/lab25
set -euo pipefail

rm -rf appdata backups restore
mkdir -p appdata/conf appdata/uploads backups restore

printf 'role=api\nversion=1\n' > appdata/conf/app.env
printf 'user-upload-1\n' > appdata/uploads/a.txt
printf 'user-upload-2\n' > appdata/uploads/b.txt
# Stable manifest of contents
( cd appdata && find . -type f -print0 | sort -z | xargs -0 sha256sum ) | tee checksums-before.txt
test -s checksums-before.txt
```

**Expected output:** `checksums-before.txt` lists hashes for the three files.

#### Task 2 – Backup with tar and rsync

```bash
cd ~/rebash-linux/lab25
set -euo pipefail

tar -czf backups/appdata.tgz -C appdata .
rsync -aH --delete appdata/ backups/appdata-mirror/
tar -tzf backups/appdata.tgz | tee tar-listing.txt
find backups/appdata-mirror -type f | sort | tee mirror-listing.txt
test -f backups/appdata.tgz
test -f backups/appdata-mirror/conf/app.env
```

**Expected output:** archive and mirror both contain `conf/app.env`; listings captured.

#### Task 3 – Destroy, restore, verify, capacity + evidence

```bash
cd ~/rebash-linux/lab25
set -euo pipefail

# Disaster: live data wiped
rm -rf appdata
test ! -d appdata

# Restore from tar
mkdir -p restore/from-tar
tar -xzf backups/appdata.tgz -C restore/from-tar
( cd restore/from-tar && find . -type f -print0 | sort -z | xargs -0 sha256sum ) | tee checksums-from-tar.txt
cmp checksums-before.txt checksums-from-tar.txt

# Restore from rsync mirror
mkdir -p restore/from-rsync
rsync -aH backups/appdata-mirror/ restore/from-rsync/
( cd restore/from-rsync && find . -type f -print0 | sort -z | xargs -0 sha256sum ) | tee checksums-from-rsync.txt
cmp checksums-before.txt checksums-from-rsync.txt

# Put live data back from tar (simulating recovery)
mkdir -p appdata
tar -xzf backups/appdata.tgz -C appdata
df -hT . | tee df-after.txt
du -sh appdata backups restore | tee du-trees.txt

# Simple RPO/RTO notes for the ticket
cat > dr-notes.txt << 'EOF'
Lab RPO: since last successful backup in backups/
Lab RTO: time to untar/rsync + checksum verify on this VM
Off-box note: copy backups/ to another disk or object storage in real DR
EOF

tar -czf backup-dr-evidence.tgz \
  df-before.txt df-after.txt du-trees.txt \
  checksums-before.txt checksums-from-tar.txt checksums-from-rsync.txt \
  tar-listing.txt mirror-listing.txt dr-notes.txt
ls -l backup-dr-evidence.tgz | tee evidence-ls.txt
```

**Expected output:** both `cmp` checks succeed; live `appdata` restored; evidence archive exists.

### Validation steps

- [ ] `checksums-before.txt` matches both restore checksum files
- [ ] `backups/appdata.tgz` and `backups/appdata-mirror/` exist
- [ ] Live `appdata` restored after deletion
- [ ] `backup-dr-evidence.tgz` exists under `~/rebash-linux/lab25`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `cmp` fails | Different find order / paths | Use the same `find … sort` pipeline |
| `rsync: command not found` | Package missing | `sudo apt-get install -y rsync` |
| Archive empty | Wrong `-C` path | `tar -tzf` to inspect before delete |
| No space for backups | Capacity ignored | Free space; separate backup disk |

### Challenge exercise

Write `~/rebash-linux/lab25/backup-appdata.sh` that creates a timestamped `backups/appdata-YYYYMMDD-HHMMSS.tgz`, writes `backups/latest-checksums.txt`, and exits non-zero if `df` free space on `.` is under 100M. Run it once and keep the new archive.

### Learning outcomes

- Defined lab RPO/RTO in plain notes
- Backed up with tar and rsync
- Restored after destructive loss and verified hashes
- Linked capacity checks to backup success

### Cleanup

```bash
cd ~/rebash-linux/lab25
set -euo pipefail
# Keep evidence; remove bulky trees if needed:
# rm -rf appdata backups restore
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab25/` with evidence files
- [ ] You can explain RPO vs RTO with an example
- [ ] You treat restore tests as mandatory
- [ ] You watch capacity on both source and backup target

## Code Walkthrough

Production DR habit:

1. Classify data and set RPO/RTO  
2. Automate backups off-box  
3. Schedule restore drills  
4. Monitor backup job success **and** free space  
5. Document who runs DR and where credentials live  

## Security Considerations

- Encrypt backups that contain personal or secret data  
- Restrict who can read backup storage  
- Do not leave world-readable archives in `/tmp`  
- Protect backup credentials like production admin access  
- Test restores in isolated networks when data is sensitive  

## Common Mistakes

!!! warning "Never testing restore"
    Backups can be corrupt or incomplete. **Fix:** restore to a scratch path on a schedule; keep checksum proof.

!!! warning "Backups only on the same disk"
    Disk failure loses source and backup together. **Fix:** copy off-box (another disk, another account, object storage).

!!! warning "Ignoring backup target capacity"
    Jobs fail silently when the target is full. **Fix:** alert on target `df`; retention policies.

!!! warning "Confusing VM snapshot with application backup"
    Snapshots may be crash-consistent only. **Fix:** use DB-native backups / app quiesce when RPO is strict.

## Best Practices

- Write RPO/RTO per service in plain language  
- Automate + alert on backup failures  
- Quarterly restore drills with notes  
- Separate backup accounts and least privilege  
- Keep capacity headroom for growth and backups  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Restore checksum mismatch | Incomplete backup / bitrot | Re-backup; check disk health |
| `tar` permission errors | Not reading all files | Run with appropriate user; note exclusions |
| rsync deleted too much | `--delete` misuse | Dry-run (`-n`) first |
| Backup job OOM/timeout | Huge trees | Incremental strategy; exclude caches |
| Cannot meet RTO | Slow restore path | Parallel restore; warmer standby |

## Summary

Backups matter only when restores work. Practise tar/rsync restore, state RPO/RTO clearly, and watch capacity so backup jobs can succeed. This completes the core Linux production module sequence — return to the [Linux overview](index.md) for related labs and interview prep.

## Interview Questions

**1. What is the difference between RPO and RTO?**

??? success "Reveal answer"
    **RPO (Recovery Point Objective)** is how much data you can afford to lose — tied to backup frequency. **RTO (Recovery Time Objective)** is how long recovery may take before the business accepts the outage. Example: RPO 1 hour, RTO 4 hours.

**2. Why is a restore test more important than “backup success” green checks?**

??? success "Reveal answer"
    Jobs can archive the wrong path, skip files, or write corrupt data while still exiting zero. Only a **restore + verification** (checksums, app start) proves usefulness.

**3. When would you choose `rsync` over `tar` for host backups?**

??? success "Reveal answer"
    **`rsync`** is strong for incremental mirrors and efficient repeats. **`tar`** is strong for portable point-in-time archives. Many designs use both: frequent rsync plus periodic tar/snapshot to object storage.

**4. How does capacity planning relate to backups?**

??? success "Reveal answer"
    Backup targets need free space and retention room. Source disks that are nearly full may also fail snapshots. Monitor `df` on both sides and alert before jobs fail.

**5. Are cloud VM snapshots enough for database DR?**

??? success "Reveal answer"
    Snapshots are useful but may be **crash-consistent** only. Databases often need native dumps/backups or filesystem freeze/agent integration for a stricter RPO. Know your consistency requirements.

**6. What belongs in a one-page DR runbook?**

??? success "Reveal answer"
    Critical systems list, RPO/RTO, where backups live, how to restore (commands/links), who to call, and how to verify success. Keep it short enough to use under stress.

**7. How would you prove backup success in a change ticket for this lab?**

??? success "Reveal answer"
    Show archive/mirror listings, a deliberate delete, restore commands, and matching `sha256sum` manifests before vs after. That is stronger than “tar completed”.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Production Hardening and Performance](production-linux-hardening-and-performance.md) *(previous)*
- [Disk Usage and File Attributes](disk-usage-and-file-attributes.md) *(related)*
- [LVM, Swap, and Disk Monitoring](lvm-swap-and-disk-monitoring.md) *(related)*

## References

- [`tar(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/tar.1.html) — Ubuntu man-pages  
- [`rsync(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/rsync.1.html) — Ubuntu man-pages  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
