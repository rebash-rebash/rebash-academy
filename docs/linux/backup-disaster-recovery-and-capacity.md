---
title: "Backup, Disaster Recovery, and Capacity"
description: "Linux backup and restore with tar and rsync, simple RPO/RTO, capacity checks — destroy data on purpose and prove restore."
difficulty: intermediate
estimated_time: "50–65 min"
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
technology: linux
module: "Module 16 · Production Linux"
learning_paths:
  - linux-administrator
  - devops-engineer
  - site-reliability-engineer
tags:
  - linux
  - backup
  - disaster-recovery
  - rsync
  - capacity
  - beginners
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

“We have backups” sounds reassuring until someone asks: **“When did you last restore?”** This tutorial uses **`tar`**, **`rsync`**, and honest **Recovery Point Objective (RPO)** / **Recovery Time Objective (RTO)** thinking — not enterprise appliances.

**Plain problem:** A bad deploy deletes config. The team has a tarball somewhere — nobody tested restore. Hours lost. **Capacity** is the sibling problem: disks fill silently until everything stops.

This tutorial: create data, **back up**, **destroy**, **restore**, verify checksums, capture capacity signals — evidence under `~/rebash-linux/lab25`.

This is **Tutorial 16b** in **Module 16: Production Linux** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series.

## Prerequisites

- Ubuntu practice VM with free disk space (~500 MB for lab)
- [Production Hardening and Performance](production-linux-hardening-and-performance.md) or comfort with `df`, `du`
- `sudo` not required for most of this lab

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain backup vs **Disaster Recovery (DR)** in plain language
- [ ] Define **RPO** and **RTO** with a simple example
- [ ] Create and restore **`tar`** and **`rsync`** backups
- [ ] Verify restore with checksums
- [ ] Read basic **capacity** signals (`df`, `du`)
- [ ] Answer fresher interview questions on backup and DR

## Architecture

Backups copy data to secondary storage. DR is the plan and practise to restore **service** after larger failure. Capacity monitoring ensures you grow storage before backups themselves fail.

![Linux backup and DR — source, backup store, restore](../assets/excalidraw/linux-backup-dr.svg)

## Theory

### The problem (before any jargon)

Intern deletes `/etc/nginx` trying to “clean up”. No tested restore. Team rebuilds manually from memory — wrong TLS cert, hours downtime. A 15-minute tested **`tar`** restore would have fixed it.

### Backup vs DR (simple words)

**Analogy:** **Backup** is photocopying important documents to a safe drawer. **DR** is the fire drill — who grabs the copies, how fast the office reopens, which copy is new enough.

| Term | Plain meaning |
|------|----------------|
| **Backup** | Copy of data at a point in time |
| **Restore** | Put data back from backup |
| **DR** | Process + infra to recover after major failure |
| **RPO** | Max acceptable **data loss** (time since last good backup) |
| **RTO** | Max acceptable **downtime** to restore service |

**Example:** Nightly backup at midnight, incident at 09:00 → RPO ≈ 9 hours of changes lost unless incremental/hourly backups exist.

**Interview line:** “I test restores regularly; RPO/RTO drive backup frequency and architecture.”

### tar — archive one directory tree

``` {.bash .ra-terminal title="Terminal"}
tar -czvf backup.tar.gz /path/to/data
tar -xzvf backup.tar.gz -C /restore/destination
```

`-c` create, `-z` gzip, `-v` verbose, `-f` file.

### rsync — efficient sync

**Analogy:** **rsync** is a smart copy — only changed blocks, great for large trees and remote hosts (`user@host:/path`).

``` {.bash .ra-terminal title="Terminal"}
rsync -a --delete /source/ /backup/mirror/
```

`-a` archive mode (perms, times); trailing slashes matter.

### Capacity

``` {.bash .ra-terminal title="Terminal"}
df -h
du -sh /var/log/*
```

Plan growth before 100% full — backups fail when destination has no space.

### Common pitfalls

- Backups on the same disk as source (single point of failure)
- Never tested restore
- Ignoring database consistency (apps need quiesce or native backup)
- Confusing snapshot with backup without off-site copy

## Hands-on Lab

### Objective

Build sample app data, **`tar`** and **`rsync`** backups, **delete** source deliberately, **restore**, verify **checksums**, capture **capacity** — under `~/rebash-linux/lab25`.

### Prerequisites

| Item | Notes |
|------|--------|
| Ubuntu VM | Local disk space |
| `sha256sum` | Usually preinstalled |

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab25/{data,backup-tar,backup-rsync,restore} && cd ~/rebash-linux/lab25
df -h . | tee df-before.txt
```

### Real-world scenario

Ticket: “Prove we can restore `/opt/myapp/config` after accidental deletion. Document RPO if we backup nightly.” You simulate with lab directories and checksum proof.

### Step-by-step tasks

#### Task 1 – Create sample data and checksum baseline

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab25
echo "version=1.0" > data/app.conf
echo "important=$(date -Is)" > data/state.txt
mkdir -p data/sub
echo "nested=ok" > data/sub/nested.txt
sha256sum data/* data/sub/* | tee checksums-before.txt
test -s checksums-before.txt
```

!!! example "Expected output"
    Three files in `data/`; checksums listed in `checksums-before.txt`.


#### Task 2 – tar and rsync backup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab25
tar -czvf backup-tar/app-data.tar.gz -C data . 2>&1 | tee tar-create.log
rsync -a data/ backup-rsync/data-mirror/
diff -qr data backup-rsync/data-mirror | tee rsync-diff.txt
test ! -s rsync-diff.txt
ls -la backup-tar backup-rsync/data-mirror | tee backup-listing.txt
```

!!! example "Expected output"
    `rsync-diff.txt` empty (trees match). Tarball exists under `backup-tar/`.


#### Task 3 – Destroy, restore, prove (break → fix → prove)

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab25
rm -rf data/*
ls data | tee data-after-delete.txt
test ! -s data-after-delete.txt
mkdir -p restore/data
tar -xzvf backup-tar/app-data.tar.gz -C restore/data 2>&1 | tee tar-restore.log
rsync -a backup-rsync/data-mirror/ restore/data/
sha256sum restore/data/* restore/data/sub/* | tee checksums-after-restore.txt
diff checksums-before.txt checksums-after-restore.txt | tee checksum-diff.txt
test ! -s checksum-diff.txt
du -sh data backup-tar backup-rsync | tee du-capacity.txt
df -h . | tee df-after.txt
echo "lab25 backup DR OK" | tee evidence.txt
```

Create `rpo-rto-notes.md`:

```markdown title="rpo-rto-notes.md"
# RPO / RTO — lab25

- If we backup once per lab session, max data loss = changes since last tar/rsync.
- RTO here = time to extract tar + verify checksums (minutes on small data).
- Production would add off-site object storage and automated restore drills.
```

!!! example "Expected output"
    `checksum-diff.txt` empty — restore matches original. Capacity files show disk use.


### Validation steps

- [ ] Data deleted deliberately after backup
- [ ] tar restore + rsync mirror both used
- [ ] Checksums match before and after
- [ ] RPO/RTO notes written in your words

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| tar: empty archive | Wrong `-C` path | Check directory contents before tar |
| rsync copies wrong tree | Trailing slash | `source/` vs `source` changes meaning |
| Checksum mismatch | Partial restore | Re-run tar; verify paths |
| No space for backup | Disk full | `df -h`; clean or expand volume |

### Challenge exercise

Add a deliberate one-byte change to `data/app.conf`, re-rsync, show `diff` detects it — then restore from tar again.

### Learning outcomes

- You performed a full backup/destroy/restore cycle
- You verified integrity with checksums
- You can explain RPO/RTO in an interview

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab25
# Keep evidence for revision; optional:
# rm -rf data restore backup-tar backup-rsync
```

## Validation

- [ ] Evidence under `~/rebash-linux/lab25`
- [ ] Can explain why untested backups fail audits
- [ ] Course production module complete

## Code Walkthrough

1. **`sha256sum` before backup** — baseline for restore proof.
2. **`tar -C data .`** — archive contents, not parent path confusion.
3. **`rsync -a`** — fast incremental sync for large trees.
4. **Deliberate `rm -rf data/*`** — simulates accidental deletion incident.
5. **`diff checksums`** — objective restore success — better than “looks fine”.

## Security Considerations

- Encrypt backups at rest and in transit for sensitive data.
- Restrict backup directory permissions (`chmod 700`).
- Off-site copies protect against site loss — local tarball alone is not DR.
- Secrets should not live in plain tarballs in shared drives.
- Test restore in isolated environment to avoid overwriting production.

# Common Mistakes

❌ Backup on same disk.

✅ Disk failure loses source and backup together — replicate off-host.

---

❌ Never tested restore.

✅ Backups are only as good as last successful restore test.

---

❌ Ignoring app consistency.

✅ Databases need coordinated backup (dump, snapshot, native tool) — not only file copy mid-write.

