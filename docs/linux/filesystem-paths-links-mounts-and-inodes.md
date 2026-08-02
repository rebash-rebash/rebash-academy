---
title: "Filesystem Paths, Links, Mounts, and Inodes"
description: "Understand directory structure, absolute versus relative paths, hard links, symbolic links, mount points, and inodes on Linux."
difficulty: beginner
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 3 · Linux Filesystem"
tags:
  - linux
  - filesystem
  - inodes
  - links
  - mounts
  - paths
prerequisites:
  - linux/essential-linux-commands
next:
  - linux/disk-usage-and-file-attributes
related:
  - labs/linux-ops-toolkit-lab
labs:
  - labs/linux-ops-toolkit-lab
interview: interview/linux
comments: false
---

# Filesystem Paths, Links, Mounts, and Inodes

## Overview

Broken symbolic links after a deploy, “disk full” with free space still showing, and bind mounts that hide a directory under the same path are everyday operations problems. They all come from how Linux names files: **paths**, **inodes**, **links**, and **mounts**.

Linux presents storage as a **single tree** starting at `/`. A **path** names a place in that tree. An **inode** holds metadata and points to data blocks. Directory entries map names to inode numbers. A **hard link** is another name for the same inode on one filesystem. A **symbolic link (symlink)** stores a path string and can cross filesystems. A **mount** attaches another filesystem onto a directory (mount point). In this tutorial you will create hard links and symlinks, inspect inode numbers, list mounts with `findmnt`, and save proof under `~/rebash-linux/lab04`.

Scripts that use relative paths fail under cron when the working directory changes. Symlinks that point at versioned release directories are a common deploy pattern — until someone deletes the target. Inode exhaustion can deny new files while `df -h` still shows space. In production you prefer absolute paths in automation, check mounts after attaching cloud disks, and monitor both space and inodes.

This is **Tutorial 4** in **Module 3: Linux Filesystem** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers. By the end, you will have a small “release symlink” layout you can explain in an interview.

## Prerequisites

- [Essential Linux Commands](essential-linux-commands.md)
- A **practice Ubuntu 22.04/24.04 VM** with write access under your home directory
- Ability to run `findmnt` (package `util-linux`, present on Ubuntu)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain absolute paths, relative paths, and why cron jobs prefer absolute paths
- [ ] Show inode numbers with `ls -i` and relate them to hard links
- [ ] Create and resolve symbolic links with `ln -s` and `readlink -f`
- [ ] List mounts with `findmnt` and explain what a mount point is
- [ ] Build a versioned app directory with a `current` symlink as deploy-style practice

## Architecture

Names in directories point to inodes. Hard links share one inode. Symlinks store a path. Mounts graft other filesystems into the tree so disks and pseudo-filesystems appear as ordinary paths.

![Architecture diagram for Filesystem Paths, Links, Mounts, and Inodes](../assets/excalidraw/linux-filesystem-hierarchy.svg)

## Theory

### What it is

| Idea | Meaning |
|------|---------|
| Absolute path | Starts at `/` (example: `/home/ubuntu/app`) |
| Relative path | Depends on current directory (example: `../logs`) |
| Inode | Metadata + data pointers; identified by number on a filesystem |
| Hard link | Extra name for the same inode (same filesystem only) |
| Symlink | Special file holding a path string |
| Mount point | Directory where another filesystem is attached |

```bash
ls -li
ln file hardlink
ln -s /etc/hosts hosts.link
readlink -f hosts.link
findmnt /
```

### Why it matters

Deploy tools often create `current` → `releases/2026-08-02`. If the symlink breaks, the site goes down even though files still exist. Bind mounts can hide old files under a path until unmount — confusing backups and deletes. Inode exhaustion appears as `No space left on device` while `df -h` looks fine; you need `df -i`. Understanding paths prevents “works in my SSH session, fails in systemd/cron” bugs.

### How it works

1. Creating a file allocates an inode and one directory entry (link count 1).
2. `ln` without `-s` adds another name; `ls -i` shows the same inode; data remains until link count is 0 and no process holds it open.
3. `ln -s target name` creates a symlink; if the target is missing, the link is **dangling**.
4. `readlink` / `readlink -f` show or fully resolve the target.
5. `mount` / `findmnt` show how devices and bind mounts attach to directories; persist with `/etc/fstab` or systemd `.mount` units (by UUID preferred).

```bash
echo hello > a.txt
ln a.txt b.txt
ls -li a.txt b.txt
ln -s a.txt a.sym
findmnt -T .
```

### Key concepts and comparisons

| Type | Same inode? | Cross filesystem? | Typical use |
|------|-------------|-------------------|-------------|
| Hard link | Yes | No | Extra name for a file |
| Symlink | No (stores path) | Yes | Stable path to a versioned target |

| Path style | Prefer when | Risk |
|------------|-------------|------|
| Absolute | cron, systemd, scripts | Longer; must stay valid if homes move |
| Relative | Interactive short work | Breaks when cwd changes |

| Tool | Shows |
|------|-------|
| `ls -i` | Inode numbers |
| `stat` | Inode, links, size, mode |
| `findmnt` | Mount table (readable) |
| `df -i` | Inode capacity per mount |

### Common pitfalls

- Creating a symlink with a relative target and then moving the link file.
- Using hard links for directories (normally not allowed) or across mounts (fails).
- Assuming deleting one hard-linked name deletes the data immediately (other names remain).
- Forgetting that a mount can hide previous contents of a directory until unmount.
- Ignoring inode limits on filesystems with millions of tiny files.

## Hands-on Lab

### Objective

On a practice Ubuntu VM, prove path types, hard links, symlinks, and mounts with a small versioned “release” layout under `~/rebash-linux/lab04`, and pack evidence.

### Prerequisites

- Ubuntu 22.04/24.04
- Commands: `ln`, `readlink`, `findmnt`, `stat`, `df`
- Work only under your home lab path

### Lab environment

Workspace: `~/rebash-linux/lab04`

```bash
mkdir -p ~/rebash-linux/lab04 && cd ~/rebash-linux/lab04
set -euo pipefail
rm -rf pathlab
mkdir -p pathlab && cd pathlab
pwd | tee ../pwd-pathlab.txt
```

**Expected output:** `pwd-pathlab.txt` ends with `pathlab`.

### Real-world scenario

Your team deploys an app by unpacking a release directory and flipping a `current` symlink. You must practise that pattern, prove inode behaviour with a hard link, and document mounts for the lab filesystem so on-call knows how to read `findmnt` during a disk incident.

### Step-by-step tasks

#### Task 1 – Absolute vs relative paths

```bash
cd ~/rebash-linux/lab04/pathlab
set -euo pipefail

mkdir -p releases/v1
echo 'v1 app' > releases/v1/app.txt

# Relative path from pathlab
cat releases/v1/app.txt | tee ../read-relative.txt

# Absolute path
ABS="$(pwd)/releases/v1/app.txt"
echo "$ABS" | tee ../abs-path.txt
cat "$ABS" | tee ../read-absolute.txt

# Show that relative fails if cwd is wrong
cd /tmp
if cat releases/v1/app.txt 2>~/rebash-linux/lab04/relative-fail.txt; then
  echo 'ERROR: relative path should fail from /tmp' >&2
  exit 1
fi
cd ~/rebash-linux/lab04/pathlab
grep -Ei 'No such file|cannot' ~/rebash-linux/lab04/relative-fail.txt
test -s ~/rebash-linux/lab04/abs-path.txt
```

**Expected output:** relative and absolute reads succeed from `pathlab`; from `/tmp` the relative read fails and is recorded in `relative-fail.txt`.

#### Task 2 – Inodes, hard links, and symlinks

```bash
cd ~/rebash-linux/lab04/pathlab
set -euo pipefail

echo 'payload' > releases/v1/data.bin
ln releases/v1/data.bin releases/v1/data-hard.bin
ln -s data.bin releases/v1/data.sym
ln -s "$(pwd)/releases/v1" current-release

ls -li releases/v1/data.bin releases/v1/data-hard.bin | tee ../inode-hardlinks.txt
# Same inode number on both hard-linked names
INO1=$(stat -c '%i' releases/v1/data.bin)
INO2=$(stat -c '%i' releases/v1/data-hard.bin)
test "$INO1" = "$INO2"
stat -c 'links=%h inode=%i name=%n' releases/v1/data.bin | tee ../stat-hard.txt

readlink releases/v1/data.sym | tee ../symlink-target.txt
readlink -f current-release | tee ../current-resolved.txt
ls -l current-release | tee ../current-ls.txt

test "$(readlink releases/v1/data.sym)" = "data.bin"
grep -q 'payload' releases/v1/data-hard.bin
```

**Expected output:** `inode-hardlinks.txt` shows the same inode for both hard links; `stat-hard.txt` shows link count ≥ 2; `current-resolved.txt` points at `…/releases/v1`.

#### Task 3 – Mounts, inode capacity, evidence pack

```bash
cd ~/rebash-linux/lab04
set -euo pipefail

findmnt -T "$HOME" | tee findmnt-home.txt
findmnt -o TARGET,SOURCE,FSTYPE,OPTIONS / | tee findmnt-root.txt
df -hT . | tee df-pathlab.txt
df -i . | tee dfi-pathlab.txt

# Dangling symlink demo (safe, inside lab)
ln -sf /no/such/target pathlab/dangling.sym
readlink pathlab/dangling.sym | tee dangling-target.txt
if [ -e pathlab/dangling.sym ]; then
  # symlink exists as a name; target may not
  ls -l pathlab/dangling.sym | tee dangling-ls.txt
fi
test ! -e /no/such/target

tar -czf paths-links-evidence.tgz \
  pwd-pathlab.txt read-relative.txt abs-path.txt read-absolute.txt relative-fail.txt \
  inode-hardlinks.txt stat-hard.txt symlink-target.txt current-resolved.txt current-ls.txt \
  findmnt-home.txt findmnt-root.txt df-pathlab.txt dfi-pathlab.txt \
  dangling-target.txt dangling-ls.txt pathlab
ls -l paths-links-evidence.tgz | tee evidence-ls.txt
test -s paths-links-evidence.tgz
```

**Expected output:** `findmnt-home.txt` shows the mount that holds your home; `dfi-pathlab.txt` shows inode use; evidence archive is non-empty.

### Validation steps

- [ ] Absolute read works; relative read from `/tmp` fails as shown
- [ ] Hard links share one inode (`test` in Task 2 passed)
- [ ] `current-release` resolves with `readlink -f`
- [ ] `findmnt` and `df -i` outputs exist
- [ ] `paths-links-evidence.tgz` exists under `~/rebash-linux/lab04`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ln: failed to create hard link: Invalid cross-device link` | Target on another mount | Use a symlink, or keep both names on one filesystem |
| Symlink points at wrong place | Relative target + moved link | Prefer absolute targets for system links, or careful relative layout |
| `findmnt: command not found` | Minimal image | Install `util-linux` |
| Confused by dangling symlink | Target deleted | Recreate target or fix link with `ln -sfn` |

### Challenge exercise

Create `pathlab/releases/v2/app.txt` with content `v2 app`, then atomically repoint `pathlab/current-release` to `releases/v2` using `ln -sfn` (or `ln -s` + `mv -T` pattern). Prove with `readlink -f pathlab/current-release` and save `current-v2.txt`. Keep the v1 and v2 directories as your deploy-style artefact.

### Learning outcomes

- Proved why absolute paths matter when cwd changes
- Created hard links and symlinks and inspected inodes
- Listed mounts and inode capacity for the lab path
- Practised a `current` → release directory layout

### Cleanup

```bash
cd ~/rebash-linux/lab04
# rm -rf pathlab *.txt paths-links-evidence.tgz
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab04/` with evidence files
- [ ] You can explain inode vs filename vs symlink
- [ ] You can explain hard link vs symlink trade-offs
- [ ] You know mounts can hide directory contents and that `df -i` matters

## Code Walkthrough

In production, filesystem identity checks usually follow this order:

1. **Resolve the path** — `pwd`, absolute paths in scripts  
2. **See what the name is** — `ls -l` (symlink?) + `readlink -f`  
3. **See the inode** — `ls -i`, `stat`  
4. **See the mount** — `findmnt -T path`, `df -hT`, `df -i`  
5. **Change carefully** — `ln -sfn` for flips; never delete the only copy of data blindly  

Deploy symlink flips should be atomic (`ln -sfn` or `mv -T` of a prepared link).

## Security Considerations

- Symlinks in world-writable directories can be abused (symlink races) — be careful in `/tmp`  
- Do not follow untrusted symlinks in privileged scripts without checks  
- Mount options (`nosuid`, `nodev`, `noexec`) matter on user-writable volumes  
- Hide mounts and bind mounts can confuse audits — document them  
- Restrict who can `mount` / edit `fstab`  

## Common Mistakes

!!! warning "Using relative paths in cron or systemd units"
    Working directory is not your SSH home. **Fix:** use absolute paths; set `WorkingDirectory=` deliberately in units.

!!! warning "Deleting a symlink target and leaving a dangling link"
    Services keep failing with “No such file”. **Fix:** update the symlink when you remove old releases; monitor with deploy checks.

!!! warning "Assuming `df -h` is enough"
    Inodes can be exhausted. **Fix:** always check `df -i` in capacity incidents.

!!! warning "Creating hard links across mounts"
    The kernel rejects cross-device hard links. **Fix:** use symlinks for cross-filesystem references.

## Best Practices

- Prefer absolute paths in automation  
- Use versioned directories + `current` symlink for releases  
- Document bind mounts and extra disks in the runbook  
- Monitor disk space **and** inodes  
- Clean old releases with a policy so disks and inodes stay healthy  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `No such file` but `ls` shows a symlink | Dangling symlink | `readlink -f`; restore target or fix link |
| `Invalid cross-device link` | Hard link across mounts | Use `ln -s` |
| Files vanished under a directory | Mount covered the path | `findmnt`; unmount or use the correct mount point |
| Cannot create files; `df -h` OK | Inode exhaustion | `df -i`; delete tiny-file trees; raise limits if appropriate |
| cron script fails | Relative paths | Switch to absolute paths |

## Summary

Paths name locations; inodes hold the real file; hard links share inodes; symlinks store paths; mounts attach filesystems into the tree. Practise deploy-style symlinks and always check mounts and inodes during capacity issues. Next, measure usage in [Disk Usage and File Attributes](disk-usage-and-file-attributes.md).

## Interview Questions

**1. What is an inode, and what does a filename have to do with it?**

??? success "Reveal answer"
    An **inode** stores file metadata and pointers to data on a filesystem. A **filename** is a directory entry that points to an inode number. Several names (hard links) can point to the same inode. Deleting a name reduces the link count; data can remain until the last link is gone and no process has the file open.

**2. Compare hard links and symbolic links.**

??? success "Reveal answer"
    **Hard links** share the same inode, must stay on one filesystem, and the file survives until all hard names are removed. **Symlinks** store a path string, can cross filesystems, and can dangle if the target is missing. Deploys often use symlinks for a stable `current` name.

**3. Why do cron jobs often break with relative paths that worked over SSH?**

??? success "Reveal answer"
    Interactive SSH sessions start in a home directory; cron’s working directory is usually different (often `/` or a service home). Relative paths resolve against that cwd and fail. Use **absolute paths** (and explicit `cd` only when intentional).

**4. How can a directory look empty after you mount a disk on it?**

??? success "Reveal answer"
    Mounting attaches a filesystem **over** the mount-point directory. Previous files under that directory are hidden until unmount (they still exist on the underlying filesystem). Operators sometimes “lose” files this way. Check with `findmnt` before and after attaching disks.

**5. `df -h` shows free space but creating a file fails with “No space left on device”. What else do you check?**

??? success "Reveal answer"
    Check **`df -i`** for inode exhaustion. Also check whether you are on the mount you think (`findmnt -T .`), and whether quotas apply. Millions of tiny files can exhaust inodes while byte space remains.

**6. How would you flip a release symlink safely in production?**

??? success "Reveal answer"
    Prepare `releases/new`, then repoint atomically with **`ln -sfn releases/new current`** (or create a new link name and `mv -T` it over `current`). Verify with `readlink -f`. Keep previous releases until health checks pass so you can roll back by flipping again.

**7. When would you choose a hard link over a symlink?**

??? success "Reveal answer"
    Choose a **hard link** when you want two names for the same file data on one filesystem without depending on a path string (and you accept that tools must understand link counts). Choose a **symlink** for cross-filesystem pointers, versioned release directories, and optional targets. Hard links to directories are not a normal operator tool.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Essential Linux Commands](essential-linux-commands.md) *(previous)*
- [Disk Usage and File Attributes](disk-usage-and-file-attributes.md) *(next)*

## References

- [`ln(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/ln.1.html) — hard links and symlinks  
- [`findmnt(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/findmnt.8.html) — list mounts  
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html) — layout context  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
