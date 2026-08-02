---
title: "Permissions, ACLs, and Special Bits"
description: "Apply chmod, chown, umask, ACLs, and special bits (sticky, SUID, SGID) on a practice Ubuntu VM with proof."
difficulty: intermediate
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 4 · Users & Permissions"
tags:
  - linux
  - chmod
  - chown
  - acl
  - suid
  - sgid
  - sticky
prerequisites:
  - linux/users-groups-and-sudo
next:
  - linux/text-processing-grep-sed-awk
related:
  - labs/linux-users-permissions-lab
labs:
  - labs/linux-users-permissions-lab
interview: interview/linux
comments: false
---

# Permissions, ACLs, and Special Bits

## Overview

Most “Permission denied” tickets are about **mode**, **ownership**, or **umask** — not mysterious kernel bugs. Linux file access starts with three classes: **user (owner)**, **group**, and **other**, each with read (4), write (2), and execute (1). **umask** masks default permissions when new files are created. **Access Control Lists (ACLs)** add named users or groups beyond those three classes. **Special bits** — sticky, setuid (SUID), and setgid (SGID) — change delete rules or the effective identity when a program runs.

Shared deploy folders need group write without opening “other”. `/tmp` needs the sticky bit so users cannot delete each other’s files. Unexpected SUID binaries are a classic hardening finding. In this tutorial you will set modes and ownership, apply an ACL, demonstrate a sticky directory, and save proof under `~/rebash-linux/lab07`.

In production, wrong modes on Secure Shell (SSH) keys, application configs, or CI artefact directories break deployments and create security findings. Prefer group or ACL sharing over world-writable paths. Audit SUID/SGID regularly on jump servers and build agents.

This is **Tutorial 7** in **Module 4: Users & Permissions** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers.

## Prerequisites

- [Users, Groups, and sudo](users-groups-and-sudo.md)
- A **practice Ubuntu 22.04/24.04 VM** with `sudo`
- Package `acl` for `setfacl`/`getfacl` (`sudo apt-get install -y acl` if missing)
- You may create and delete lab users (do **not** run this on a shared production server)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Set and verify POSIX modes with `chmod` and ownership with `chown`/`chgrp`
- [ ] Explain umask and check the current umask
- [ ] Grant a named user access with `setfacl` and prove it with `getfacl`
- [ ] Apply the sticky bit on a shared drop directory and explain why it matters
- [ ] Pack evidence under `~/rebash-linux/lab07`

## Architecture

Permissions sit between identity (UID/GID) and the filesystem. Mode bits, ACLs, and special bits decide whether a process may read, write, traverse, or delete.

![Architecture diagram for Permissions, ACLs, and Special Bits](../assets/excalidraw/linux-permission-model.svg)

## Theory

### What it is

POSIX permissions use three classes. Directories need the execute bit to **traverse** (enter) the path. ACLs add entries such as `user:alice:rwx`. Sticky (`+t`) on a directory restricts unlinking to the file owner (plus root). SUID on an executable runs it as the file owner; SGID runs as the file group. SGID on a directory often makes new files inherit the directory’s group.

```bash
ls -l
stat -c '%A %U %G %n' file
umask
getfacl file
```

### Why it matters

“Permission denied” is rarely mysterious once you inspect mode, owner, group, ACL, and Mandatory Access Control (MAC) such as AppArmor or SELinux. Shared project trees need group write without `o+rwx`. World-writable deploy directories are a common audit failure. Wrong modes on `~/.ssh` (`700`/`600`) lock people out of servers.

### How it works

`chmod` sets mode (octal `640` or symbolic `u=rw,g=r,o=`). Capital `X` in symbolic mode sets execute only on directories or on files that already had execute. `chown`/`chgrp` change ownership (often requiring root). umask `0022` typically yields `644` files and `755` directories; `0027` is tighter. `setfacl`/`getfacl` manage ACLs; default ACLs on directories apply to new children.

| Mechanism | Granularity | Typical use |
|-----------|-------------|-------------|
| POSIX mode | owner/group/other | Default access model |
| ACL | named users/groups | Shared dirs without widening other |
| Sticky | directory delete rules | `/tmp`, shared drop boxes |
| SGID directory | group inheritance | Team project trees |
| SUID/SGID file | effective UID/GID at run | Rare; prefer capabilities |

| umask | Typical file / dir |
|-------|---------------------|
| `0022` | `644` / `755` |
| `0002` | `664` / `775` (group-friendly) |
| `0027` | `640` / `750` (tighter) |

### Common pitfalls

- Widening `o+rwx` instead of using a group or ACL.
- Forgetting execute on directories — path lookup fails.
- Leaving unexpected SUID/SGID binaries after experiments.
- Applying ACLs on filesystems mounted without ACL support.
- Changing ownership of SSH keys and locking yourself out.

## Hands-on Lab

### Objective

On a practice Ubuntu VM, create a shared project directory with correct group modes, grant an ACL to a lab user, demonstrate sticky-bit delete behaviour, and save evidence under `~/rebash-linux/lab07`.

### Prerequisites

- Ubuntu with `sudo`, `chmod`, `chown`, and the `acl` package
- Ability to create temporary users

### Lab environment

Workspace: `~/rebash-linux/lab07`

```bash
mkdir -p ~/rebash-linux/lab07 && cd ~/rebash-linux/lab07
set -euo pipefail
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y acl
umask | tee umask-default.txt
whoami | tee lab-admin.txt
```

**Expected output:** `acl` tools available; `umask-default.txt` shows a value such as `0022`.

### Real-world scenario

Your team shares a deploy drop folder on a practice VM. Security wants: (1) group-writable for deployers, (2) one contractor with read-only ACL access, (3) sticky bit so people cannot delete each other’s artefacts. You implement and prove it before the change ticket closes.

### Step-by-step tasks

#### Task 1 – Group, users, and POSIX modes

```bash
cd ~/rebash-linux/lab07
set -euo pipefail

sudo groupadd rebash-perm || true
if ! id rebash-dev >/dev/null 2>&1; then
  sudo useradd -m -s /bin/bash -G rebash-perm rebash-dev
fi
if ! id rebash-contractor >/dev/null 2>&1; then
  sudo useradd -m -s /bin/bash rebash-contractor
fi
sudo usermod -aG rebash-perm rebash-dev

sudo mkdir -p /opt/rebash-perm/shared
sudo chown root:rebash-perm /opt/rebash-perm/shared
sudo chmod 2770 /opt/rebash-perm/shared

sudo -u rebash-dev bash -c 'echo deploy-artefact > /opt/rebash-perm/shared/app.txt'
sudo -u rebash-dev bash -c 'ls -l /opt/rebash-perm/shared/app.txt' | tee ls-shared-file.txt
stat -c '%A %U %G %n' /opt/rebash-perm/shared /opt/rebash-perm/shared/app.txt | tee stat-shared.txt
getent group rebash-perm | tee group-rebash-perm.txt
```

**Expected output:** directory mode shows `rwx` for group and `s` in the group-execute position (SGID); `app.txt` group is `rebash-perm`.

#### Task 2 – ACL for the contractor (read-only)

```bash
cd ~/rebash-linux/lab07
set -euo pipefail

sudo setfacl -m u:rebash-contractor:rx /opt/rebash-perm/shared
sudo setfacl -m u:rebash-contractor:r /opt/rebash-perm/shared/app.txt
sudo getfacl /opt/rebash-perm/shared /opt/rebash-perm/shared/app.txt | tee getfacl-shared.txt

sudo -u rebash-contractor cat /opt/rebash-perm/shared/app.txt | tee contractor-read.txt
if sudo -u rebash-contractor bash -c 'echo hack > /opt/rebash-perm/shared/app.txt' 2>contractor-write-deny.txt; then
  echo "ERROR: contractor could write" >&2
  exit 1
fi
grep -Ei 'Permission denied|denied' contractor-write-deny.txt
grep -F 'user:rebash-contractor:r' getfacl-shared.txt
```

**Expected output:** `getfacl` lists the contractor ACL; read succeeds; write is denied.

#### Task 3 – Sticky drop box and evidence pack

```bash
cd ~/rebash-linux/lab07
set -euo pipefail

sudo mkdir -p /opt/rebash-perm/drop
sudo chown root:rebash-perm /opt/rebash-perm/drop
sudo chmod 1770 /opt/rebash-perm/drop

sudo -u rebash-dev bash -c 'echo from-dev > /opt/rebash-perm/drop/dev.txt'
if ! id rebash-dev2 >/dev/null 2>&1; then
  sudo useradd -m -s /bin/bash -G rebash-perm rebash-dev2
fi
sudo -u rebash-dev2 bash -c 'echo from-dev2 > /opt/rebash-perm/drop/dev2.txt'

if sudo -u rebash-dev2 rm -f /opt/rebash-perm/drop/dev.txt 2>sticky-deny.txt; then
  echo "ERROR: sticky bit did not block delete" >&2
  exit 1
fi
grep -Ei 'Permission denied|denied|Operation not permitted' sticky-deny.txt
ls -ld /opt/rebash-perm/drop | tee ls-drop.txt
grep -E 't|T' ls-drop.txt

tar -czf permissions-evidence.tgz \
  lab-admin.txt umask-default.txt \
  ls-shared-file.txt stat-shared.txt group-rebash-perm.txt \
  getfacl-shared.txt contractor-read.txt contractor-write-deny.txt \
  sticky-deny.txt ls-drop.txt
ls -l permissions-evidence.tgz | tee evidence-ls.txt
```

**Expected output:** sticky delete is denied; `ls-drop.txt` shows `t` in the mode; evidence archive exists.

### Validation steps

- [ ] `/opt/rebash-perm/shared` is mode `2770` (or equivalent `drwxrws---`)
- [ ] `getfacl` shows `rebash-contractor` with read on the file
- [ ] Contractor write fails; sticky delete fails for the other user
- [ ] `permissions-evidence.tgz` exists under `~/rebash-linux/lab07`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `setfacl: command not found` | `acl` package missing | `sudo apt-get install -y acl` |
| `Operation not supported` | Filesystem without ACL | Use ext4/xfs home/data disk; avoid some network mounts |
| Contractor cannot enter directory | Missing `x` on directory ACL | `setfacl -m u:user:rx` on the directory |
| Sticky test unexpectedly succeeds | Mode not sticky | `chmod +t` / `chmod 1770` and re-check `ls -ld` |

### Challenge exercise

Add a **default ACL** on `/opt/rebash-perm/shared` so new files grant `rebash-contractor` read access automatically (`setfacl -d -m u:rebash-contractor:r`). Create a new file as `rebash-dev`, run `getfacl` on that file, and save output to `default-acl-proof.txt`.

### Learning outcomes

- Applied SGID group-shared directory modes
- Used ACLs for a named user without widening “other”
- Proved sticky-bit delete protection
- Saved permission evidence for a change ticket

### Cleanup

```bash
cd ~/rebash-linux/lab07
set -euo pipefail

sudo rm -rf /opt/rebash-perm
sudo userdel -r rebash-dev 2>/dev/null || true
sudo userdel -r rebash-dev2 2>/dev/null || true
sudo userdel -r rebash-contractor 2>/dev/null || true
sudo groupdel rebash-perm 2>/dev/null || true
# Keep permissions-evidence.tgz if you want it
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab07/` with evidence files
- [ ] You can explain POSIX mode vs ACL vs sticky bit
- [ ] You know why world-writable shared dirs are a bad default
- [ ] You can list when SUID on files is a security finding

## Code Walkthrough

Production permission work usually follows:

1. **Identify** — `ls -l`, `stat`, `namei -l`, `id`
2. **Prefer group or ACL** over `chmod o+rwx`
3. **Prove allow and deny** for the real users
4. **Special bits** — sticky on shared drop dirs; avoid casual SUID
5. **Automate** modes in configuration management, not one-off SSH

## Security Considerations

- Never make secrets world-readable (`o+r` on key material)
- Keep `~/.ssh` at `700` and private keys at `600`
- Audit SUID/SGID binaries (`find / -perm /6000`) on hardened images
- ACLs can hide access — always include `getfacl` in reviews
- Sticky bit on shared directories reduces cross-user deletion attacks

## Common Mistakes

!!! warning "Fixing access with `chmod 777`"
    World-writable paths fail audits and invite tampering. **Fix:** use a group (`2770`) or a named ACL.

!!! warning "Forgetting directory execute"
    Users can “see” a file mode but still get “Permission denied” on the path. **Fix:** ensure `x` on every directory in the path.

!!! warning "Assuming ACL is optional documentation"
    Some NAS/NFS mounts ignore ACLs. **Fix:** verify with `getfacl` after mount; test as the named user.

!!! warning "Shipping SUID binaries for convenience"
    Any bug becomes a privilege escalation path. **Fix:** prefer capabilities, sudo allow-lists, or root helpers with narrow scope.

## Best Practices

- Encode modes and ownership in Ansible/Puppet/cloud-init
- Use SGID directories for team trees; sticky for drop boxes
- Review umask on CI runners that publish artefacts
- Document ACL entries next to the directory purpose
- Re-test access after user leave (remove ACLs and group membership)

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Permission denied | Mode/owner/path `x` missing | `namei -l`, `stat`, fix mode |
| Works for one user only | Group/ACL missing | `id`, `getfacl`, `usermod -aG` |
| New files wrong group | Directory not SGID | `chmod g+s` on the directory |
| Delete others’ files in shared dir | Sticky missing | `chmod +t` |
| ACL “ignored” | Mount options / FS type | Check `mount` options; remount with ACL |

## Summary

Modes, ownership, umask, ACLs, and special bits decide **who can read, write, traverse, and delete**. Prefer least privilege with groups and ACLs, prove allow and deny, and keep SUID rare. Next: [Text Processing with grep, sed, and awk](text-processing-grep-sed-awk.md).

## Interview Questions

**1. What do the three POSIX permission classes mean, and what does execute mean on a directory?**

??? success "Reveal answer"
    The classes are **owner**, **group**, and **other**. On files, execute means run as a program. On directories, execute means **traverse** (enter/search) that directory. Without directory `x`, you cannot reach files inside even if the file mode looks open.

**2. How do ACLs help when two users need access but should not share a primary group?**

??? success "Reveal answer"
    **ACLs** add named-user or named-group entries with `setfacl` without widening “other” or forcing a shared primary group. Prove with `getfacl` and a login/sudo-as that user. Default ACLs on directories apply to new children.

**3. What is the sticky bit for, and how do you recognise it in `ls -ld`?**

??? success "Reveal answer"
    On a directory, sticky (`+t`) means only the **file owner** (or root) can unlink/rename files there — classic for `/tmp`. In `ls -ld`, you see a `t` or `T` in the other-execute position of the mode string (for example `drwxrwxrwt`).

**4. Why is `chmod 777` on a deploy directory a security problem?**

??? success "Reveal answer"
    Any local user (or compromised low-privilege process) can change or replace artefacts. Prefer `2770` with a deploy group, or ACLs for specific users, and keep secrets out of that tree. Auditors flag world-writable paths quickly.

**5. What is the difference between SUID on a file and SGID on a directory?**

??? success "Reveal answer"
    **SUID on a file** runs the program with the file owner’s UID (powerful; audit carefully). **SGID on a directory** typically makes new files inherit the directory’s group, which helps team-shared trees. Do not confuse the two in interviews.

**6. How would you debug “Permission denied” on `/opt/app/bin/start`?**

??? success "Reveal answer"
    Check the full path with `namei -l`, then `stat`/`ls -l` on each component, `id` for the runtime user, `getfacl` if ACLs are in use, and MAC logs (AppArmor/SELinux) if modes look correct. Fix the first component that denies traverse or execute.

**7. How does umask affect files created by CI jobs?**

??? success "Reveal answer"
    umask masks default permissions. A loose umask can create world-readable artefacts (secret leakage); a tight umask can make the next job unable to read outputs. Set umask deliberately in the job environment and verify with `stat` on a created file.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Users, Groups, and sudo](users-groups-and-sudo.md) *(previous)*
- [Text Processing with grep, sed, and awk](text-processing-grep-sed-awk.md) *(next)*
- [Lab — Users, Groups, and Permissions](../labs/linux-users-permissions-lab.md) *(more practice)*

## References

- [`chmod(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/chmod.1.html) — Ubuntu man-pages
- [`acl(5)`](https://manpages.ubuntu.com/manpages/jammy/en/man5/acl.5.html) — Access Control Lists
- [`setfacl(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/setfacl.1.html) — set file ACLs
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
