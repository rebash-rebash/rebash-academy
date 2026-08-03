---
title: "Disk Usage and File Attributes"
description: "Measure disk and inode usage with df and du, inspect file metadata with stat, and find what filled a filesystem on Ubuntu."
difficulty: beginner
estimated_time: "40–50 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 3 · Linux Filesystem"
tags:
  - linux
  - df
  - du
  - attributes
  - stat
prerequisites:
  - linux/filesystem-paths-links-mounts-and-inodes
next:
  - linux/users-groups-and-sudo
related:
  - linux/storage-disks-partitions-and-filesystems
interview: interview/linux
comments: false
---

# Disk Usage and File Attributes

## Overview

When a server cannot write files, you need two answers quickly: **which filesystem is full**, and **which directory tree used the space**. **`df`** answers the first (free space and free inodes per mount). **`du`** answers the second (space used under a path). **File attributes** are the metadata you see with `ls -l` and `stat`: mode, owner, size, and timestamps.

On cloud virtual machines (VMs), container hosts, and Continuous Integration (CI) runners, disks fill from logs, package caches, and image layers. Sometimes `df` shows full while `du` on `/` looks smaller — often a deleted file is still held open by a process, or another mount (for example `/var`) is the one that filled. In this tutorial you will create a sample tree, measure it with `du`, compare mounts with `df`, inspect attributes with `stat`, and save proof under `~/rebash-linux/lab05`.

In production, Site Reliability Engineering (SRE) runbooks almost always start with `df -h`, `df -i`, then `du` on the hot mount. Attribute checks separate “disk full” from “permission denied” or “wrong owner”. Extended flags such as `chattr +i` (immutable) can protect critical configs — and can also block deploys if someone forgets to clear them.

This is **Tutorial 5** in **Module 3: Linux Filesystem** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, SREs, and platform engineers.

## Prerequisites

- [Paths, Links, Mounts, and Inodes](filesystem-paths-links-mounts-and-inodes.md)
- A **practice Ubuntu 22.04/24.04 VM** (or similar) with write access under your home directory
- Optional: `sudo` if you want to inspect deleted-open files system-wide later

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the difference between `df` (per mount) and `du` (per directory tree)
- [ ] Check both block space and inode capacity with `df -h` and `df -i`
- [ ] Find large directories with `du` and sort human-readable sizes
- [ ] Read mode, owner, size, and timestamps with `stat`
- [ ] Pack evidence under `~/rebash-linux/lab05` for a capacity ticket

## Architecture

Disk capacity is per **mount**. File attributes live on the **inode**. Tools report different layers of the same storage story.

![Architecture diagram for Disk Usage and File Attributes](../assets/excalidraw/linux-filesystem-hierarchy.svg)

## Theory

### What it is

**File attributes** are metadata: permissions, owner, group, size, timestamps (atime/mtime/ctime), inode number, and device. Extended attributes (xattrs) and filesystem flags (`chattr`/`lsattr` on ext4) add extra behaviour such as immutability.

**Disk usage** has two views:

| Tool | Answers |
|------|---------|
| `df` | How much free space / free inodes does this **mount** have? |
| `du` | How much space does this **directory tree** use? |
| `stat` / `ls -l` | Who owns it, what mode, what size and times? |

``` {.bash .ra-terminal title="Terminal"}
df -hT
df -i
du -sh ~
stat /etc/passwd
```

### Why it matters

Disk-full incidents are among the most common production pages. Container hosts fill `/var/lib/docker` or `/var/lib/containerd`. Log directories grow without rotation. Millions of small files can exhaust **inodes** while `df -h` still shows free blocks. Getting attributes wrong causes `Permission denied` that looks like a storage problem until you check `stat` and `namei -l`.

### How it works

1. **Find the full mount** — `df -hT` and `df -i`. Note the **Mounted on** column, not only `/`.
2. **Find the hot directory** — `du -h --max-depth=1 /path | sort -h` (may need `sudo` outside your home).
3. **Inspect a file** — `stat -c '%n %A %U %G %s' file` for scripts; full `stat` for humans.
4. **When `df` and `du` disagree** — look for other mounts and for deleted-but-open files (`sudo lsof +L1` when available).

| Symptom | Likely cause |
|---------|--------------|
| `df` full, `du` on `/` smaller | Other mount full, or deleted-open files |
| `df -h` free, create fails | Inode exhaustion (`df -i`) |
| Permission denied | Mode/owner/ACL — not “disk full” |

### Common pitfalls

- Checking only `/` while `/var` or a data volume is full.
- Ignoring inodes — many tiny files exhaust them first.
- Restarting nothing when `du` and `df` disagree; the process holding a deleted file must exit or close it.
- Leaving `chattr +i` on files and wondering why deploys cannot overwrite them.
- Sorting `du` wrong — use `sort -h` with human-readable sizes.

## Hands-on Lab

### Objective

On a practice Ubuntu VM, build a sample directory tree, measure it with `du`, compare mounts with `df`, inspect attributes with `stat`, and save an evidence pack under `~/rebash-linux/lab05`.

### Prerequisites

- Ubuntu 22.04/24.04 (or Debian) with `df`, `du`, `stat` (from `coreutils` / `util-linux`)
- Write access under `$HOME`

### Lab environment

Workspace: `~/rebash-linux/lab05`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab05 && cd ~/rebash-linux/lab05
set -euo pipefail
whoami | tee lab-user.txt
df -hT . | tee df-workspace.txt
```

!!! example "Expected output"
    `lab-user.txt` and `df-workspace.txt` exist; workspace is on a real mount.


### Real-world scenario

On-call reports “disk almost full” on a practice app VM. Before you expand the volume, you must prove **which mount** is tight, **which folder** grew, and whether a sample file’s attributes look normal. You create a controlled sample tree, measure it, and attach command output to the ticket.

### Step-by-step tasks

#### Task 1 – Build a sample tree and measure with `du`

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab05
set -euo pipefail

rm -rf sample-tree
mkdir -p sample-tree/{logs,cache,data}

dd if=/dev/zero of=sample-tree/logs/app.log bs=1M count=8 status=none
dd if=/dev/zero of=sample-tree/cache/pkg.bin bs=1M count=4 status=none
printf 'config=ok\n' > sample-tree/data/app.conf
for i in $(seq 1 50); do
  printf 'x' > "sample-tree/cache/tiny-$i.dat"
done

du -sh sample-tree | tee du-total.txt
du -h --max-depth=1 sample-tree | sort -h | tee du-depth1.txt
du -ah sample-tree | sort -h | tail -n 8 | tee du-largest.txt

test "$(du -sb sample-tree/logs | awk '{print $1}')" -gt "$(du -sb sample-tree/data | awk '{print $1}')"
```

!!! example "Expected output"
    `du-total.txt` shows roughly 12M+ for the tree; `du-depth1.txt` lists `logs`, `cache`, and `data`; `logs` is larger than `data`.


#### Task 2 – Mount capacity with `df` (blocks and inodes)

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab05
set -euo pipefail

df -hT | tee df-hT.txt
df -i | tee df-i.txt
df -hT . / | tee df-here-and-root.txt
findmnt -T . | tee findmnt-here.txt || true

find sample-tree -printf '.' | wc -c | tee inode-ish-count.txt
test -s df-hT.txt
test -s df-i.txt
```

!!! example "Expected output"
    `df-hT.txt` shows filesystem type and free space; `df-i.txt` shows inode use; workspace mount appears in `df-here-and-root.txt`.


#### Task 3 – File attributes with `stat` and evidence pack

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab05
set -euo pipefail

stat sample-tree/data/app.conf | tee stat-app.conf.txt
stat -c 'name=%n mode=%A owner=%U group=%G size=%s inode=%i' \
  sample-tree/data/app.conf sample-tree/logs/app.log | tee stat-summary.txt
ls -l sample-tree/data/app.conf | tee ls-app.conf.txt

stat -c '%s' sample-tree/logs/app.log | tee log-bytes.txt
test "$(cat log-bytes.txt)" -eq $((8 * 1024 * 1024))

tar -czf disk-usage-evidence.tgz \
  lab-user.txt df-workspace.txt \
  du-total.txt du-depth1.txt du-largest.txt \
  df-hT.txt df-i.txt df-here-and-root.txt \
  stat-app.conf.txt stat-summary.txt ls-app.conf.txt log-bytes.txt
ls -l disk-usage-evidence.tgz | tee evidence-ls.txt
```

!!! example "Expected output"
    `stat-summary.txt` shows mode/owner/size; `log-bytes.txt` is `8388608`; evidence archive is not empty.


### Validation steps

- [ ] `du -sh sample-tree` reports a size consistent with the `dd` files (~12M+)
- [ ] `df -hT` and `df -i` both produced output files
- [ ] `stat` shows owner and mode for `app.conf`
- [ ] `disk-usage-evidence.tgz` exists under `~/rebash-linux/lab05`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `du: cannot read directory` | Permission on system paths | Stay under `$HOME` for this lab; use `sudo` only when needed |
| `sort: invalid option` for `-h` | Very old `sort` | Install coreutils, or sort by `du -k` numeric column |
| `df` looks fine but writes fail | Wrong mount or inode full | Check `df -i` and `findmnt -T path` |
| Sizes look “wrong” after delete | File still open | Find holders with `lsof` / restart the process |

### Challenge exercise

Write `~/rebash-linux/lab05/capacity-scan.sh` that: (1) prints `df -hT` for `.`, (2) prints the three largest entries under `sample-tree` using `du`, and (3) exits `0` only if free space on `.` is above 100M (parse `df` carefully). Save a sample run to `capacity-scan.out`.

### Learning outcomes

- Separated mount capacity (`df`) from tree usage (`du`)
- Checked inode capacity
- Inspected file attributes with `stat`
- Saved ticket-ready evidence

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab05
set -euo pipefail
rm -rf sample-tree
# Keep evidence if you want it:
# rm -f disk-usage-evidence.tgz *.txt capacity-scan.sh capacity-scan.out
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab05/` with evidence files
- [ ] You can explain when `df` and `du` disagree
- [ ] You know to check `df -i` on “no space left” errors
- [ ] You can read mode/owner/size from `stat` without guessing

## Code Walkthrough

In production capacity work for **Disk Usage and File Attributes**:

1. **Identify the mount** — `df -hT`, `df -i`, `findmnt`
2. **Find the growth** — `du` on that mount (not always on `/`)
3. **Confirm attributes** — `stat` / `ls -l` before blaming “disk” for permission errors
4. **Check deleted-open files** when numbers disagree
5. **Fix forward** — rotate logs, prune caches, expand volume, then re-measure

Automate the boring checks; keep humans for “is this safe to delete?”

## Security Considerations

- Do not run destructive `rm -rf` on production paths from a capacity ticket without a second check
- Restrict who can read application log trees that may contain secrets
- Treat `sudo lsof` output carefully — it can expose paths with credentials
- Immutable flags (`chattr +i`) are a security control; document them
- Prefer least privilege: measure under the app user’s directories when possible

## Common Mistakes

!!! warning "Checking only the root filesystem"
    `/var` or a data disk can be full while `/` looks fine. **Fix:** read the Mounted on column from `df -hT` for the path that failed.

!!! warning "Ignoring inodes"
    Creates fail with “No space left” even when `df -h` shows free megabytes. **Fix:** always run `df -i`.

!!! warning "Deleting large files that are still open"
    Space does not return until the process closes the file. **Fix:** find the process (`lsof`), restart or reopen logs, then confirm with `df`.

!!! warning "Using `du` without knowing the mount"
    Summarising `/` includes other mounts and confuses the picture. **Fix:** `du` the specific mount path from `findmnt` / `df`.

## Best Practices

- Alert on filesystem use **and** inode use for busy mounts
- Separate OS and data volumes on cloud VMs
- Keep log rotation and container prune jobs on a schedule
- Record `df`/`du` output in incident tickets before and after cleanup
- Document any `chattr` usage in configuration management

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `No space left on device` | Blocks or inodes full | `df -hT`, `df -i`, then `du` |
| `df` full, `du` smaller | Deleted-open or other mount | `lsof +L1`, check all mounts |
| Permission denied on write | Mode/owner/ACL | `stat`, `namei -l`, not `df` |
| Deploy cannot overwrite config | Immutable attribute | `lsattr`; clear with `chattr -i` if intended |
| `du` very slow on huge trees | Millions of files | Limit depth; exclude mounts; use offline reporting |

## Summary

`df` tells you about **mounts**; `du` tells you about **directories**; `stat` tells you about **one file**. Use all three before you expand a disk or delete data. Next, learn identity controls in [Users, Groups, and sudo](users-groups-and-sudo.md).

## Interview Questions

**1. What is the difference between `df` and `du`, and when would you trust each?**

??? success "Reveal answer"
    **`df`** reports free space and inodes for a **mounted filesystem**. **`du`** reports how much space a **directory tree** uses. Trust `df` for “can I write on this mount?” and `du` for “which folder grew?”. When they disagree, check other mounts and deleted-but-open files.

**2. A create fails with “No space left on device” but `df -h` shows free space. What do you check next?**

??? success "Reveal answer"
    Run **`df -i`**. The filesystem may be out of **inodes** (common with many tiny files). Also confirm you are looking at the correct mount for the path (`findmnt -T path`).

**3. Why can deleting a large log file not free space immediately?**

??? success "Reveal answer"
    If a process still has the file open, the kernel keeps the space allocated until the last file descriptor closes. Use tools such as `lsof +L1` (with appropriate privilege), restart or reopen the logging process, then re-check `df`.

**4. How do you find the largest directories under `/var` in an interview-style answer?**

??? success "Reveal answer"
    Prefer something like `sudo du -h --max-depth=1 /var | sort -h`, then drill into the largest child. Mention that you first confirm `/var` is its own mount or part of `/` with `df`/`findmnt`, so you clean the right place.

**5. Which file attributes does `stat` show that matter in a “permission denied” ticket?**

??? success "Reveal answer"
    Mode (permissions), owner, group, and whether the path components are traversable (execute on directories). Size and timestamps help for “who changed it when”, but mode/owner/group (plus ACL/MAC on hardened hosts) decide access.

**6. How would you prove in a change ticket that a cleanup worked?**

??? success "Reveal answer"
    Attach **before and after** `df -hT` (and `df -i` if relevant) for the affected mount, plus a `du` summary of the cleaned tree. Show the commands and timestamps. Capacity work without before/after numbers is incomplete.

**7. When might you use `chattr +i`, and what is the operational risk?**

??? success "Reveal answer"
    Use immutability for critical files that must not change accidentally (for example a golden config). The risk is forgotten flags blocking deploys or emergency fixes. Always document the flag and know how to clear it (`chattr -i`) during an incident.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Paths, Links, Mounts, and Inodes](filesystem-paths-links-mounts-and-inodes.md) *(previous)*
- [Users, Groups, and sudo](users-groups-and-sudo.md) *(next)*
- [Disks, Partitions, and Filesystems](storage-disks-partitions-and-filesystems.md) *(related)*

## References

- [`df(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/df.1.html) — Ubuntu man-pages
- [`du(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/du.1.html) — Ubuntu man-pages
- [`stat(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/stat.1.html) — Ubuntu man-pages
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
