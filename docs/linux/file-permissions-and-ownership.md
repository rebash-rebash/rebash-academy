---
title: File Permissions and Ownership
description: Master POSIX permissions, chmod, chown, umask, and special bits (setuid, setgid, sticky) for secure Linux administration.
difficulty: beginner
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
  - permissions
  - chmod
  - security
prerequisites:
  - Complete Essential Linux Commands or equivalent experience
  - Familiarity with the Linux filesystem hierarchy
comments: false
---

# File Permissions and Ownership

## Overview

Every file and directory on a Linux system carries three pieces of access metadata: an **owner** (user), a **group**, and a **permission mode** that defines who may read, write, or execute it. Misconfigured permissions are one of the most common causes of "Permission denied" errors in production — and one of the fastest paths to privilege escalation when set too loosely.

This tutorial is part of **Module 2: Users, Groups & Permissions** in the REBASH Academy Linux series. You will learn to inspect permissions with `ls` and `stat`, modify them with `chmod` and `chown`, control defaults with `umask`, and understand special bits (`setuid`, `setgid`, sticky) that underpin core system behaviour like `sudo` and shared directories.

## Prerequisites

- Complete [Essential Linux Commands](essential-linux-commands.md) or equivalent terminal experience
- A Linux VM, cloud instance, or local machine with terminal access
- `sudo` privileges for ownership-change exercises
- A dedicated lab directory (we create one in Step 1)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Read and interpret permission strings and octal modes (e.g., `drwxr-xr-x` / `755`)
- [ ] Change permissions using both symbolic (`u+x`) and octal (`644`) notation with `chmod`
- [ ] Transfer ownership with `chown` and group membership with `chgrp`
- [ ] Configure default permissions for new files using `umask`
- [ ] Explain and safely audit setuid, setgid, and sticky bits on production systems
- [ ] Troubleshoot permission-denied errors using `namei` and `stat`

## Architecture

This topic is primarily procedural. The mental model is a straight line from inputs (commands, config files, or manifests) to observable system state — verify each change with the validation steps later in this tutorial.

## Theory

### The permission model

Linux uses a **discretionary access control (DAC)** model. The file owner decides who can access the file. Each inode stores:

| Field | Description |
|-------|-------------|
| Owner (uid) | User who owns the file |
| Group (gid) | Group associated with the file |
| Mode | 12 permission bits (9 standard + 3 special) |

When a process accesses a file, the kernel checks credentials in order: if the process uid matches the owner, **user** bits apply; else if the process gid (or supplementary groups) matches, **group** bits apply; otherwise **other** bits apply.

### Reading `ls -l` output

```bash
-rwxr-xr-- 1 alice dev 4096 Jul 27 10:00 deploy.sh
drwxrwsr-x 2 root  shared 4096 Jul 27 10:00 /srv/shared
```

| Position | Meaning |
|----------|---------|
| `-` / `d` / `l` | Regular file, directory, or symlink |
| `rwx` | User (owner) permissions |
| `rwx` | Group permissions |
| `r--` | Other permissions |

For directories, **execute (`x`)** means permission to traverse (enter) the directory, not run it as a program.

### Octal notation

Each permission triplet maps to a digit: r=4, w=2, x=1. Sum the bits:

| Octal | Binary | Permissions |
|-------|--------|-------------|
| 7 | 111 | rwx |
| 6 | 110 | rw- |
| 5 | 101 | r-x |
| 4 | 100 | r-- |
| 0 | 000 | --- |

Common modes:

| Mode | Typical use |
|------|-------------|
| 644 | World-readable files (config, docs) |
| 600 | Private files (keys, secrets) |
| 755 | Executable scripts, directories |
| 700 | Private directories |
| 775 | Team-shared directories |

### Symbolic notation

Symbolic changes are additive or subtractive without replacing the entire mode:

```bash
chmod u+x file        # add execute for owner
chmod g-w file        # remove write for group
chmod o=r file        # set others to read-only
chmod a+r file        # add read for all (user, group, other)
chmod u+s,g+s file    # set setuid and setgid
```

### umask — default permissions

When a process creates a file, the kernel applies: `mode = request & ~umask`.

Default umask is often `0022`, producing:

- Files: `666 & ~022` = `644` (rw-r--r--)
- Directories: `777 & ~022` = `755` (rwxr-xr-x)

Set umask in `/etc/profile`, shell rc files, or systemd service units. A umask of `027` is common on servers (group-readable, no world access).

### Special permission bits

| Bit | Octal | On files | On directories |
|-----|-------|----------|----------------|
| setuid | 4000 | Process runs as file owner | (ignored) |
| setgid | 2000 | Process runs as file group | New files inherit directory group |
| sticky | 1000 | (ignored) | Only owner can delete own files |

Examples in the wild:

- `/usr/bin/passwd` is setuid root (`4755`) so users can update their hash in `/etc/shadow`
- `/tmp` has the sticky bit (`1777`) so users cannot delete each other's files
- Shared project dirs often use setgid (`2775`) for consistent group ownership

!!! warning "setuid binaries are high-risk"
    Any setuid root program is a potential privilege-escalation vector. Audit with `find / -perm /6000 -type f 2>/dev/null` regularly.

## Hands-on Lab

Create an isolated lab directory for all exercises:

```bash
mkdir -p ~/lab/permissions && cd ~/lab/permissions
```

### Step 1 – Inspect existing permissions

Compare system files with different security postures:

```bash
ls -l /etc/passwd /etc/shadow
ls -ld /tmp /root
stat -c '%a %n' /etc/passwd /etc/shadow /tmp
```

**Expected output:**

```text
-rw-r--r-- 1 root root  1234 Jul 27 09:00 /etc/passwd
-rw-r----- 1 root shadow 678 Jul 27 09:00 /etc/shadow
drwxrwxrwt  8 root root 4096 Jul 27 10:00 /tmp
drwx------  3 root root 4096 Jul 27 08:00 /root
644 /etc/passwd
640 /etc/shadow
1777 /tmp
```

Note: `/etc/shadow` is group-readable by `shadow` only; `/tmp` shows `t` (sticky bit).

### Step 2 – Create files and observe umask

```bash
umask
touch newfile.txt
mkdir newdir
ls -l newfile.txt
ls -ld newdir
```

**Expected output (umask 0022):**

```text
0022
-rw-r--r-- 1 user user 0 Jul 27 10:05 newfile.txt
drwxr-xr-x 2 user user 4096 Jul 27 10:05 newdir
```

### Step 3 – Change permissions with octal mode

```bash
echo "deploy script" > deploy.sh
chmod 755 deploy.sh
ls -l deploy.sh
chmod 644 deploy.sh
ls -l deploy.sh
```

**Expected output:**

```text
-rwxr-xr-x 1 user user 14 Jul 27 10:06 deploy.sh
-rw-r--r-- 1 user user 14 Jul 27 10:06 deploy.sh
```

### Step 4 – Change permissions with symbolic mode

```bash
chmod u+x deploy.sh          # owner execute
chmod g+w deploy.sh          # group write
chmod o-r deploy.sh          # remove other read
ls -l deploy.sh
chmod a=r deploy.sh          # all read-only
ls -l deploy.sh
```

**Expected output:**

```text
-rwxrwx--- 1 user user 14 Jul 27 10:07 deploy.sh
-r--r--r-- 1 user user 14 Jul 27 10:07 deploy.sh
```

### Step 5 – Change ownership (requires sudo)

```bash
sudo useradd -r -s /usr/sbin/nologin labsvc 2>/dev/null || true
sudo chown labsvc:labsvc deploy.sh
ls -l deploy.sh
sudo chgrp users deploy.sh
ls -l deploy.sh
sudo chown $USER:$USER deploy.sh   # restore for cleanup
```

**Expected output:**

```text
-r--r--r-- 1 labsvc labsvc 14 Jul 27 10:08 deploy.sh
-r--r--r-- 1 labsvc users  14 Jul 27 10:08 deploy.sh
```

Only root (or the current owner with appropriate capabilities) can change ownership.

### Step 6 – Demonstrate setgid on a shared directory

```bash
sudo groupadd devteam 2>/dev/null || true
sudo mkdir -p /srv/devteam
sudo chown root:devteam /srv/devteam
sudo chmod 2775 /srv/devteam
ls -ld /srv/devteam
touch /srv/devteam/test.txt 2>/dev/null || sudo touch /srv/devteam/test.txt
ls -l /srv/devteam/test.txt
```

**Expected output:**

```text
drwxrwsr-x 2 root devteam 4096 Jul 27 10:09 /srv/devteam
-rw-r--r-- 1 user devteam 0 Jul 27 10:09 /srv/devteam/test.txt
```

The `s` in group execute indicates setgid; new files inherit the `devteam` group.

### Step 7 – Demonstrate sticky bit behaviour

```bash
mkdir sticky-demo && chmod 1777 sticky-demo
ls -ld sticky-demo
# In multi-user environments: user A cannot delete user B's file here
```

**Expected output:**

```text
drwxrwxrwt 2 user user 4096 Jul 27 10:10 sticky-demo
```

### Step 8 – Trace permission failures with namei

Simulate a nested path denial:

```bash
mkdir -p blocked/private
chmod 700 blocked
namei -l blocked/private 2>&1 || ls -ld blocked blocked/private
```

**Expected output:** `namei` shows where traversal fails — useful when a script reports "Permission denied" deep in a path.

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
| `ls -l FILE` | List permissions in human-readable form |
| `ls -ld DIR` | List directory itself (not contents) |
| `stat FILE` | Full inode metadata including numeric mode |
| `stat -c '%a %U %G %n' FILE` | Compact permission, owner, group, name |
| `chmod 644 FILE` | Set mode to rw-r--r-- (octal) |
| `chmod u+x FILE` | Add execute for owner (symbolic) |
| `chmod -R g-w DIR/` | Recursively remove group write |
| `chown user:group FILE` | Change owner and group |
| `chown user FILE` | Change owner only |
| `chgrp group FILE` | Change group only |
| `umask` | Display current umask (shell builtin) |
| `umask 027` | Set umask for current session |
| `find / -perm /4000 -type f 2>/dev/null` | Find setuid files |
| `find / -perm /2000 -type f 2>/dev/null` | Find setgid files |
| `find / -perm /1000 -type d 2>/dev/null` | Find sticky directories |
| `namei -l PATH` | Trace path permissions component by component |
| `getfacl FILE` | View POSIX ACLs (when enabled) |
| `id` | Show current uid, gid, and supplementary groups |

## Code Examples

### Secure deployment script permissions

```bash
#!/bin/bash
# secure-deploy-artifact.sh — set safe permissions on release files
set -euo pipefail

ARTIFACT="${1:?Usage: $0 <file>}"

# Owner read/write, group read, no world access
chmod 640 "$ARTIFACT"
chown deploy:deploy "$ARTIFACT"

echo "Set $(stat -c '%a %U:%G' "$ARTIFACT") on $ARTIFACT"
```

### Audit setuid/setgid binaries

```bash
#!/bin/bash
# audit-special-bits.sh — report unexpected special-permission files
set -euo pipefail

echo "=== Setuid files (non-package paths) ==="
find /usr/local /opt /home /tmp -perm /6000 -type f 2>/dev/null \
  | while read -r f; do
      ls -l "$f"
    done

echo "=== World-writable directories without sticky bit ==="
find /tmp /var/tmp /dev/shm -type d -perm -0002 ! -perm -1000 2>/dev/null
```

### Team shared directory bootstrap

```bash
#!/bin/bash
# init-shared-dir.sh — create setgid collaborative workspace
set -euo pipefail

DIR="/srv/shared"
GROUP="devteam"

groupadd "$GROUP" 2>/dev/null || true
mkdir -p "$DIR"
chown root:"$GROUP" "$DIR"
chmod 2775 "$DIR"
echo "Shared directory ready: $(ls -ld "$DIR")"
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Using chmod 777 to fix access problems"
    World-writable files and directories are a security liability. Fix ownership and group membership instead, or use ACLs for fine-grained access.

!!! warning "Recursive chown/chmod on the wrong path"
    `chmod -R 777 /` or `chown -R user /` can brick a system. Always verify paths; use `--reference` to copy modes from a template file.

!!! warning "Forgetting execute on directories"
    Without `x` on a directory, users cannot `cd` into it or access files inside — even if file permissions allow read.

!!! warning "Ignoring supplementary groups"
    A user in group `docker` can access group-owned socket files even if their primary group is `users`. Check `id` and `/etc/group`.

## Best Practices

!!! tip "Follow the principle of least privilege"
    Default to `640` for secrets, `644` for public configs, `750` for team directories. Never grant write to "others" on production systems.

!!! tip "Use version control for permission baselines"
    Document expected modes in Ansible, Terraform, or Puppet. Drift detection catches accidental `chmod` changes after incidents.

!!! tip "Separate service accounts from human users"
    Run applications as dedicated users with minimal filesystem access. Use `chown service:service` on app directories only.

!!! tip "Audit special bits quarterly"
    Unexpected setuid binaries are a classic persistence mechanism. Automate the audit script above in your compliance pipeline.

!!! tip "Set umask in service units"
    `UMask=0027` in systemd unit files ensures daemons create files without world-readable bits.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Permission denied on script | Missing execute bit | `chmod u+x script.sh` or invoke with `bash script.sh` |
| Permission denied on directory | Missing traverse (`x`) on parent dir | `chmod u+x /path/to/dir` or fix parent chain with `namei -l` |
| Cannot write to shared folder | Wrong group or missing setgid | Add user to group: `usermod -aG team user`; re-login; verify with `id` |
| chown: Operation not permitted | Non-root user changing ownership | Use `sudo chown` or have root perform the change |
| New files too open | umask too permissive | Set `umask 027` in profile or systemd unit |
| setuid program behaves unexpectedly | Binary runs as file owner | Expected for `/usr/bin/passwd`; investigate unknown setuid files |
| ACL overrides not working | ACL not mounted/supported | Check `mount \| grep acl`; install `acl` package; use `setfacl` |

## Summary

- Every file has an owner, group, and mode; the kernel enforces access based on the requesting process credentials.
- Use **octal** (`755`) for setting full modes and **symbolic** (`u+x`) for targeted changes with `chmod`.
- `chown` and `chgrp` transfer identity; only root can give away files owned by others.
- **umask** subtracts permissions from newly created files — set it explicitly in production environments.
- **setuid**, **setgid**, and **sticky** bits enable system features but must be audited regularly.
- Use `stat`, `namei`, and permission audits to diagnose "Permission denied" errors quickly.

## Interview Questions

**1. What do the permission bits `rwxr-x---` mean for a regular file?**

*Sample answer:* The owner can read, write, and execute. Group members can read and execute. Others have no permissions. For a regular file, execute means the file can be run as a program.

**2. How do you represent `rw-r-----` in octal?**

*Sample answer:* User rw- = 6, group r-- = 4, other --- = 0, so octal mode is **640**.

**3. What is the difference between `chmod 755` and `chmod 4755`?**

*Sample answer:* `755` is standard rwxr-xr-x. `4755` adds the setuid bit (4 in the leading digit), so executables run with the file owner's privileges instead of the caller's.

**4. Why does `/tmp` have permissions `1777`?**

*Sample answer:* `777` allows anyone to create files. The sticky bit (`1`) ensures only the file owner (or root) can delete or rename files in the directory — preventing users from removing each other's temp files.

**5. How does umask 0027 affect new files and directories?**

*Sample answer:* Files: 666 & ~027 = 640 (rw-r-----). Directories: 777 & ~027 = 750 (rwxr-x---). Group gets read (and traverse for dirs); world gets nothing.

**6. Can a user read a file if they lack read permission but have execute on the directory?**

*Sample answer:* No. Execute on a directory grants traverse access only. Read permission on the file itself is still required to read its contents (unless accessed via root or ACL exceptions).

**7. What is the difference between `chown user:group file` and `chgrp group file`?**

*Sample answer:* `chown` changes owner and optionally group in one command. `chgrp` changes only the group. Both require appropriate privileges (root for files not owned by you).

**8. How would you find all world-writable files on a server?**

*Sample answer:* `find / -type f -perm -0002 2>/dev/null` finds files writable by others. Combine with `-path '/proc' -prune` exclusions for faster scans. Investigate each finding — world-writable files are a security risk.

**9. What does the `s` in `rws` vs `S` indicate in `ls -l` output?**

*Sample answer:* Lowercase `s` means setuid/setgid is set **and** execute is present. Uppercase `S` means the special bit is set but execute is absent — often a misconfiguration worth fixing.

**10. How do you copy permissions from one file to another?**

*Sample answer:* `chmod --reference=source.txt target.txt` copies the mode. For ownership: `chown --reference=source.txt target.txt`.

1. How would you explain file permissions and ownership to a junior engineer in two minutes?
2. What production failure mode appears when teams ignore file permissions and ownership?
3. Which metrics or logs would you check first when file permissions and ownership misbehaves?
4. What is a secure default related to file permissions and ownership?
5. How would you validate a change involving file permissions and ownership in CI or a staging environment?
6. What trade-off would you accept to simplify operations around file permissions and ownership?
7. Describe a common anti-pattern with file permissions and ownership and how you fix it.
8. How does file permissions and ownership interact with networking, identity, or storage in a real system?
9. What would you put on a runbook checklist for file permissions and ownership?
10. When would you intentionally not follow the default approach taught here?

## Related Tutorials

- [Linux – Category Overview](index.md)
- [Essential Linux Commands](essential-linux-commands.md) *(previous)*
- [User and Group Management](user-and-group-management.md) *(next)*
- [Linux Security Hardening Basics](linux-security-hardening-basics.md)
- [Linux Filesystem Hierarchy](linux-filesystem-hierarchy.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)
- Cheat sheet: [Linux Cheat Sheet](../cheatsheets/linux.md)
- Interview prep: [Linux Interview Prep](../interview/linux.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [chmod man page](https://man7.org/linux/man-pages/man1/chmod.1.html)
- [chown man page](https://man7.org/linux/man-pages/man1/chown.1.html)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- [POSIX file permissions overview](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap04.html)
- [REBASH Academy – Linux Overview](index.md)
