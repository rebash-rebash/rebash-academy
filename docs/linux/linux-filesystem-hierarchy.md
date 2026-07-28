---
title: Linux Filesystem Hierarchy
description: Master the Filesystem Hierarchy Standard (FHS) — understand every major directory from /etc and /var to /proc and /sys with real paths and production context.
difficulty: beginner
estimated_time: "25 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
  - filesystem
  - fhs
  - directories
  - paths
prerequisites:
  - Complete Introduction to Linux or equivalent understanding of kernel vs distro
  - Terminal access to a Linux system
comments: false
---

# Linux Filesystem Hierarchy

## Overview

On Linux, **everything is a file** — regular files, directories, devices, sockets, and even kernel interfaces. The **Filesystem Hierarchy Standard (FHS)** defines where each type of data lives so administrators, applications, and automation tools can predict paths across distributions. When nginx fails to start, you check `/etc/nginx/`; when disks fill up, you investigate `/var/log/` and `/var/lib/`; when a user's shell misbehaves, you read `~/.bashrc` under `/home/`.

Without FHS literacy, you waste hours searching for configs, accidentally edit the wrong copy of a file, or store application data in paths that break during upgrades. DevOps engineers live in this tree daily — Docker volumes map to `/var/lib/docker`, Kubernetes mounts host paths, Ansible templates target `/etc/`, and log agents tail `/var/log/`. This tutorial maps the entire hierarchy with real examples you will encounter in production.

This is **Tutorial 2** in **Module 1: Foundations** of the REBASH Academy Linux series. It includes theory, hands-on labs, and interview preparation.

## Prerequisites

- Completed [Introduction to Linux](introduction-to-linux.md) or equivalent familiarity with Linux basics
- Terminal access to a Linux VM, WSL2 instance, or cloud server
- Ability to run read-only commands (`ls`, `cat`, `find`) — some steps use `sudo` optionally
- Basic understanding that `/` is the root of the entire filesystem tree

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the purpose of the FHS and why standardized paths matter in multi-server environments
- [ ] Identify the role of every major top-level directory under `/`
- [ ] Distinguish between static config (`/etc`), variable data (`/var`), and executable programs (`/usr/bin`)
- [ ] Navigate virtual filesystems (`/proc`, `/sys`, `/dev`) and understand what they expose
- [ ] Predict where logs, packages, user data, and temporary files are stored on any FHS-compliant distro
- [ ] Use CLI tools to explore and audit filesystem layout on an unfamiliar server

## Architecture

The diagram below is the classic FHS **directory tree** under `/`. Branches show containment (a folder inside its parent) — not execution order.

<figure class="rebash-diagram rebash-tree-diagram" markdown="0">
<p class="rebash-tree-title">/</p>
<ul class="rebash-tree">
  <li>boot/<span class="rebash-tree-note">kernel &amp; bootloader · vmlinuz · initramfs · grub/</span></li>
  <li>etc/<span class="rebash-tree-note">static configuration</span>
    <ul>
      <li>passwd · shadow · hosts</li>
      <li>nginx/nginx.conf</li>
      <li>systemd/system/</li>
    </ul>
  </li>
  <li>home/<span class="rebash-tree-note">user home directories · ubuntu/ · .bashrc · projects/</span></li>
  <li>root/<span class="rebash-tree-note">superuser home</span></li>
  <li>opt/<span class="rebash-tree-note">third-party add-ons</span></li>
  <li>usr/<span class="rebash-tree-note">programs &amp; read-only data</span>
    <ul>
      <li>bin/<span class="rebash-tree-note">ls, grep, python3</span></li>
      <li>lib/<span class="rebash-tree-note">shared libraries</span></li>
      <li>share/<span class="rebash-tree-note">docs, man pages</span></li>
    </ul>
  </li>
  <li>var/<span class="rebash-tree-note">variable data</span>
    <ul>
      <li>log/<span class="rebash-tree-note">syslog · journal/</span></li>
      <li>lib/<span class="rebash-tree-note">docker/ · apt/</span></li>
    </ul>
  </li>
  <li>tmp/<span class="rebash-tree-note">world-writable temp</span></li>
  <li>run/<span class="rebash-tree-note">runtime state since boot</span></li>
  <li>dev/<span class="rebash-tree-note">device nodes (sda, null, tty)</span></li>
  <li>proc/<span class="rebash-tree-note">process &amp; kernel info</span></li>
  <li>sys/<span class="rebash-tree-note">kernel object hierarchy</span></li>
  <li>srv/<span class="rebash-tree-note">service data (web, git, ftp)</span></li>
</ul>
</figure>


## Theory

### What Is the FHS?

The **Filesystem Hierarchy Standard**, maintained by the Linux Foundation, specifies directory names, locations, and minimum contents for Linux and Unix-like systems. FHS ensures that `/etc/passwd` means "user account database" whether you are on Ubuntu, RHEL, or Debian. Configuration management tools, monitoring agents, and security scanners rely on these conventions.

FHS defines three logical categories:

| Category | Meaning | Examples |
|----------|---------|----------|
| **Shareable** | Can be mounted read-only from a network | `/usr`, `/opt` |
| **Static** | Changes infrequently | `/etc`, `/boot` |
| **Variable** | Changes during normal operation | `/var`, `/tmp`, `/run` |

### The Root Directory `/`

`/` is the mount point for the root filesystem. All other paths are descendants. On a typical server, `/` is a separate partition (often 20–50 GB). Filling `/` breaks the entire system — which is why logs and databases live under `/var`, not `/`.

### `/bin` and `/sbin` — Essential Binaries

These directories hold binaries required for **single-user mode** and early boot before `/usr` is mounted. On modern distros, `/bin` and `/sbin` are often **symlinks to `/usr/bin` and `/usr/sbin`** (the merged `/usr` layout).

| Path | Purpose | Real examples |
|------|---------|---------------|
| `/bin` | Core user commands | `bash`, `ls`, `cp`, `cat`, `mkdir` |
| `/sbin` | Core system administration | `ip`, `mkfs.ext4`, `fdisk`, `reboot` |

Verify on your system: `ls -l /bin` — if it shows `bin -> usr/bin`, you have the merged layout.

### `/boot` — Kernel and Bootloader Files

Contains files needed to boot the kernel. Typically a separate small partition (512 MB–1 GB).

| Path | Purpose |
|------|---------|
| `/boot/vmlinuz-*` | Compressed Linux kernel images |
| `/boot/initrd.img-*` or `/boot/initramfs-*` | Initial RAM disk for loading drivers before root mount |
| `/boot/grub/` or `/boot/efi/` | GRUB configuration and EFI boot entries |
| `/boot/config-*` | Kernel build configuration (useful for module debugging) |

**Never store arbitrary files in `/boot`** — a full `/boot` partition prevents kernel updates from installing.

### `/dev` — Device Files

Hardware and pseudo-devices appear as special files:

| Path | Purpose |
|------|---------|
| `/dev/sda`, `/dev/nvme0n1` | Block devices (disks) |
| `/dev/sda1` | Disk partitions |
| `/dev/tty`, `/dev/pts/*` | Terminals |
| `/dev/null` | Bit bucket — discards all writes |
| `/dev/zero` | Infinite stream of zero bytes |
| `/dev/random`, `/dev/urandom` | Entropy sources for cryptography |

Modern systems use **udev** (managed by systemd) to create device nodes dynamically at boot.

### `/etc` — Host-Specific Configuration

**"etc" = editable text configuration.** This is the most visited directory for sysadmins. Files here apply to **this machine only** — they are not shared across `/usr`.

| Path | Purpose |
|------|---------|
| `/etc/passwd` | User account names, UIDs, home dirs, shells |
| `/etc/shadow` | Hashed passwords (root-readable only) |
| `/etc/group` | Group definitions |
| `/etc/hosts` | Static hostname-to-IP mappings |
| `/etc/resolv.conf` | DNS resolver configuration |
| `/etc/fstab` | Filesystem mount table at boot |
| `/etc/ssh/sshd_config` | SSH server settings |
| `/etc/nginx/nginx.conf` | Nginx main config (if installed) |
| `/etc/systemd/system/` | Administrator-defined systemd units |
| `/etc/os-release` | Distribution identity |

**Rule of thumb:** If you are configuring how a service behaves on this server, the file is almost always under `/etc/`.

### `/home` — User Home Directories

Each regular user gets a subdirectory: `/home/alice`, `/home/bob`. User-owned files, SSH keys (`~/.ssh/id_ed25519`), shell configs (`~/.bashrc`), and project code live here. Home directories are often on separate partitions or NFS mounts in enterprises.

The tilde `~` expands to your home directory: `cd ~` → `/home/youruser`.

### `/root` — Superuser Home

The home directory for the **root** account (`/root`), not `/home/root`. Separated so root can log in even if `/home` is corrupted or unmounted. Directories like `/root/.ssh/` store root's SSH keys.

### `/lib`, `/lib64` — Essential Shared Libraries

Kernel modules and shared libraries required for `/bin` and `/sbin` binaries to run. Like `/bin`, often symlinked to `/usr/lib` on merged-`/usr` systems. Contains critical files such as `/lib/x86_64-linux-gnu/libc.so.6` (the C standard library).

### `/media` and `/mnt` — Mount Points

| Path | Purpose |
|------|---------|
| `/mnt` | Temporary mount point for administrators (`mount /dev/sdb1 /mnt/backup`) |
| `/media` | Auto-mount point for removable media (USB drives) — desktop-oriented |

In servers, you will mount volumes under `/mnt` or custom paths like `/data`.

### `/opt` — Optional Third-Party Software

Self-contained packages from vendors install here: `/opt/google/chrome`, `/opt/splunk/`, `/opt/aws/amazon-cloudwatch-agent/`. Each package typically has its own `bin/`, `lib/`, and config subtree. Keeps vendor software isolated from distro packages in `/usr`.

### `/proc` — Process and Kernel Information (Virtual)

A **virtual filesystem** — no disk space used. The kernel exposes runtime information as readable files:

| Path | Purpose |
|------|---------|
| `/proc/cpuinfo` | CPU model, cores, flags |
| `/proc/meminfo` | Memory usage breakdown |
| `/proc/loadavg` | Load averages |
| `/proc/PID/status` | Details about process PID |
| `/proc/sys/net/ipv4/ip_forward` | Kernel tunable (sysctl) |

Tools like `top`, `ps`, and `free` read `/proc` under the hood.

### `/run` — Runtime Variable Data

Created by systemd at boot; holds PID files, sockets, and state that must persist across early boot but not reboots. Examples: `/run/sshd.pid`, `/run/systemd/system/`, `/run/udev/data/`. Replaces much of what historically lived in `/var/run` (now typically a symlink to `/run`).

### `/srv` — Service Data

Data served by this system — site content for web servers, Git repos, FTP roots. Example: `/srv/www/example.com/public_html/`. Less commonly used today (many teams prefer `/var/www` or container volumes), but FHS-compliant and seen in exam questions.

### `/sys` — Kernel Object Hierarchy (Virtual)

Another virtual filesystem (sysfs). Exposes kernel data structures about devices, drivers, and kernel subsystems. Used by udev and low-level tooling. Example: `/sys/class/net/eth0/address` shows the MAC address.

### `/tmp` — Temporary Files

World-writable with sticky bit (`drwxrwxrwt`). Any user can create files; only the owner (or root) can delete their own. Cleared on reboot on many systems (or by `systemd-tmpfiles`). Use for scratch space — **never store secrets here**.

### `/usr` — User Programs and Read-Only Data

The largest directory on most systems. Contains the bulk of installed software:

| Path | Purpose |
|------|---------|
| `/usr/bin` | User commands (`git`, `python3`, `curl`, `vim`) |
| `/usr/sbin` | Non-essential system admin commands (`sshd`, `nginx`) |
| `/usr/lib` | Libraries for `/usr/bin` programs |
| `/usr/share` | Architecture-independent data (man pages, docs, icons) |
| `/usr/local` | Locally compiled software (`make install` default prefix) |
| `/usr/src` | Kernel headers and source (for building modules) |

**Distinction:** `/usr` is often mounted read-only in hardened systems. `/etc` holds local overrides; `/usr` holds packaged software.

### `/var` — Variable Data

Files that **change in size and content** during normal operation:

| Path | Purpose |
|------|---------|
| `/var/log/` | Log files — `syslog`, `auth.log`, `nginx/access.log` |
| `/var/lib/` | Application state — `docker/`, `mysql/`, `apt/` |
| `/var/cache/` | Package manager caches, application caches |
| `/var/spool/` | Queues — mail (`/var/spool/mail/`), cron, print jobs |
| `/var/tmp/` | Temp files that **persist across reboots** (unlike `/tmp`) |
| `/var/www/` | Web document roots (common convention) |

**Production alert:** `/var` filling up stops logging, breaks databases, and can crash services. Monitor disk usage here aggressively.

## Hands-on Lab

### Step 1 – List top-level directories with types and sizes

**Command:**

```bash
ls -la /
df -h /
```

**Explanation:** `ls -la /` shows every top-level entry including symlinks (note `bin -> usr/bin`). `df -h /` shows total disk usage of the root filesystem — context for why `/var` separation matters.

**Expected output:**

```text
lrwxrwxrwx   1 root root     7 ... bin -> usr/bin
drwxr-xr-x   4 root root  4096 ... boot
drwxr-xr-x  18 root root  3880 ... dev
drwxr-xr-x  95 root root  4096 ... etc
...
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        30G  4.2G   24G  15% /
```

### Step 2 – Explore static configuration in /etc

**Command:**

```bash
ls /etc | head -20
cat /etc/hosts
cat /etc/os-release | head -5
```

**Explanation:** `/etc` contains hundreds of config files and directories. `hosts` and `os-release` are safe to read on any system and demonstrate host-specific vs standardized config.

**Expected output:**

```text
adduser.conf
alternatives
apt
bash.bashrc
...
127.0.0.1 localhost
127.0.1.1 ip-172-31-10-42

PRETTY_NAME="Ubuntu 24.04.1 LTS"
NAME="Ubuntu"
...
```

### Step 3 – Inspect variable data and logs in /var

**Command:**

```bash
sudo ls -lah /var/log | head -12
du -sh /var/log /var/lib /var/cache 2>/dev/null
```

**Explanation:** Logs and application state live under `/var`. Disk usage here grows unbounded without log rotation — a top cause of production outages.

**Expected output:**

```text
drwxr-xr-x  11 root syslog 4.0K ... .
-rw-r-----   1 syslog adm    45K ... auth.log
-rw-r-----   1 syslog adm   128K ... syslog
...
120M    /var/log
890M    /var/lib
156M    /var/cache
```

Sizes vary widely by system age and installed services.

### Step 4 – Count installed user programs in /usr/bin

**Command:**

```bash
ls /usr/bin | wc -l
which python3 nginx docker 2>/dev/null
```

**Explanation:** `/usr/bin` holds the command-line tools you use daily. `which` searches `$PATH` — typically including `/usr/bin` and `/usr/local/bin`.

**Expected output:**

```text
1847
/usr/bin/python3
```

Some commands may return nothing if the package is not installed — that is expected.

### Step 5 – Read kernel and process info from /proc

**Command:**

```bash
head -5 /proc/cpuinfo
head -3 /proc/meminfo
cat /proc/loadavg
echo "My PID: $$ — status file: /proc/$$/status"
head -5 /proc/$$/status
```

**Explanation:** `/proc` is a live view into the kernel. Reading these files costs nothing and works in scripts when external tools are unavailable.

**Expected output:**

```text
processor       : 0
vendor_id       : GenuineIntel
model name      : Intel(R) Xeon(R) CPU ...
MemTotal:        8123456 kB
MemFree:         5234567 kB
0.08 0.04 0.01 1/234 45678
My PID: 45678 — status file: /proc/45678/status
Name:   bash
State:  S (sleeping)
Pid:    45678
```

### Step 6 – Examine device nodes in /dev

**Command:**

```bash
ls -l /dev/null /dev/zero /dev/random
lsblk
```

**Explanation:** Special files in `/dev` represent devices. `lsblk` shows block device hierarchy — mapping `/dev/sda1` to mount points like `/`.

**Expected output:**

```text
crw-rw-rw- 1 root root 1, 3 ... /dev/null
crw-rw-rw- 1 root root 1, 5 ... /dev/zero
crw-rw-rw- 1 root root 1, 8 ... /dev/random
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda      8:0    0   30G  0 disk
└─sda1   8:1    0   30G  0 part /
```

### Step 7 – Compare /tmp and /var/tmp permissions

**Command:**

```bash
ls -ld /tmp /var/tmp
```

**Explanation:** Both hold temporary files, but `/tmp` is cleared on reboot while `/var/tmp` persists. The sticky bit (`t` in `drwxrwxrwt`) prevents users from deleting each other's files.

**Expected output:**

```text
drwxrwxrwt  12 root root 4096 ... /tmp
drwxrwxrwt   8 root root 4096 ... /var/tmp
```

The `t` at the end of the permission string is the sticky bit.

### Step 8 – Trace a config file to its package (Debian/Ubuntu)

**Command:**

```bash
dpkg -S /etc/nginx/nginx.conf 2>/dev/null || \
  rpm -qf /etc/ssh/sshd_config 2>/dev/null || \
  echo "Install nginx or use an existing /etc file for this demo"
ls -la /etc/systemd/system/
```

**Explanation:** Knowing which package owns a file prevents accidental manual edits that get overwritten on upgrade. `/etc/systemd/system/` holds admin-created unit overrides — a path you will use constantly in DevOps.

**Expected output:**

```text
nginx: /etc/nginx/nginx.conf
total 16
drwxr-xr-x  2 root root 4096 ... .
lrwxrwxrwx  1 root root   44 ... dbus-org.freedesktop.resolve1.service -> ...
```

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

| Command | Description | Example |
|---------|-------------|---------|
| `ls -la /` | List root directory with details | `ls -la /` |
| `ls -ld` | List directory itself (not contents) | `ls -ld /tmp /var/tmp` |
| `df -h` | Disk free space human-readable | `df -h / /var` |
| `du -sh` | Directory size summary | `du -sh /var/log/*` |
| `find /etc -maxdepth 2 -type d` | Explore config tree | `find /etc -maxdepth 1 -type d` |
| `cat /proc/cpuinfo` | CPU details from virtual fs | `grep -c processor /proc/cpuinfo` |
| `cat /proc/meminfo` | Memory statistics | `head /proc/meminfo` |
| `lsblk` | Block device tree | `lsblk -f` |
| `mount` | Show mounted filesystems | `mount \| grep ^/dev` |
| `readlink -f` | Resolve symlinks to real path | `readlink -f /bin/ls` |
| `file` | Identify file type | `file /dev/null` |
| `stat` | Detailed inode/metadata | `stat /etc/passwd` |
| `which` | Locate command in PATH | `which bash` |
| `dpkg -S` | Which package owns file (Debian) | `dpkg -S /bin/ls` |
| `rpm -qf` | Which package owns file (RHEL) | `rpm -qf /etc/passwd` |
| `tree` | Directory tree view | `tree -L 1 /var` |

## Code

### FHS audit script for onboarding new servers

Run this when inheriting an undocumented server. It reports mount points, largest `/var` consumers, and symlink layout.

```bash
#!/usr/bin/env bash
# fhs-audit.sh — summarize filesystem layout for runbook documentation
set -euo pipefail

section() { printf '\n=== %s ===\n' "$1"; }

section "Root Filesystem Usage"
df -h / /var /home /boot 2>/dev/null || df -h /

section "Top-Level Directories"
ls -la / | awk '{print $1, $9, $10, $11}'

section "Merged /usr Layout?"
for link in /bin /sbin /lib /lib64; do
  if [[ -L "$link" ]]; then
    echo "$link -> $(readlink -f "$link")"
  else
    echo "$link is a real directory (pre-merged layout)"
  fi
done

section "Largest Consumers in /var (top 5)"
du -sh /var/* 2>/dev/null | sort -rh | head -5

section "Critical Config Files Present"
for f in /etc/fstab /etc/hosts /etc/os-release /etc/passwd; do
  [[ -e "$f" ]] && echo "OK  $f" || echo "MISSING  $f"
done

section "Virtual Filesystems Mounted"
mount -t proc,sysfs,tmpfs 2>/dev/null | awk '{print $1, $3}' || \
  grep -E '^(proc|sysfs)' /proc/mounts | awk '{print $2, $3}'
```

### Find misconfigured log paths filling root

```bash
#!/usr/bin/env bash
# find-large-logs.sh — locate log files over 100MB under /var/log
find /var/log -type f -size +100M -exec ls -lh {} \; 2>/dev/null | \
  awk '{print $5, $9}' | sort -rh
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Editing files in /usr instead of /etc"
    Never modify `/usr/lib/systemd/system/nginx.service` directly — package upgrades overwrite it. Copy unit files to `/etc/systemd/system/` and edit there. Configuration belongs in `/etc/`; `/usr/` is managed by the package manager.

!!! warning "Storing application data in /tmp"
    `/tmp` may be cleared on reboot and is world-readable. Databases, uploads, and secrets belong in `/var/lib/yourapp/` or a dedicated mount like `/data` with proper permissions.

!!! warning "Assuming /home is always local disk"
    In enterprises, `/home` may be NFS or LDAP-mounted home directories. Heavy I/O workloads should not default to `$HOME` — use `/var/lib` or a dedicated volume.

!!! warning "Ignoring symlink indirection"
    On merged-`/usr` systems, `/bin/ls` resolves to `/usr/bin/ls`. Scripts hardcoding `/bin/` usually work, but backup tools and security scanners must follow symlinks with `readlink -f` to avoid missing files.

## Best Practices

!!! tip "Separate partitions for /var, /home, and /boot"
    In production, mount `/var` (and optionally `/home`, `/boot`) on separate LVM volumes or cloud disks. A runaway log cannot fill `/` and take down the entire OS.

!!! tip "Use FHS paths in automation and containers"
    Mount host `/var/log/myapp` into containers at a predictable path. Ansible roles should template configs to `/etc/myapp/` — not `/opt/myapp/config` unless the vendor requires it.

!!! tip "Monitor /var/log and /var/lib disk usage"
    Set alerts at 80% and 90% thresholds. Log rotation (`logrotate`) is configured in `/etc/logrotate.d/` — verify it exists for every service you deploy.

!!! tip "Document custom mount points in /etc/fstab"
    Every non-default mount (EBS volume at `/data`, NFS share at `/mnt/backups`) should have an `/etc/fstab` entry with `nofail` where appropriate so boot is not blocked by unavailable network storage.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "No space left on device" but `/` shows free space | `/var` or `/boot` partition full | Run `df -h` on all mount points; `du -sh /var/*` to find culprit |
| Config changes have no effect | Edited file in `/usr` instead of `/etc` | Find vendor override path; use `/etc/systemd/system/` for units |
| Cannot find binary after install | Not in `$PATH` | Check `/usr/local/bin` for manual installs; run `hash -r` |
| `/proc` file shows stale data | Normal — some files are snapshots | Re-read file; use proper tool (`free`, not one-time `/proc/meminfo` parse) |
| Permission denied reading `/etc/shadow` | Expected — root only | Use `sudo`; never `chmod` shadow for convenience |
| Service logs missing | Logs in `/var/log/` vs journald | Check `journalctl -u servicename` and `/var/log/` |
| `/tmp` files disappear after reboot | By design on many distros | Use `/var/tmp` or application-specific dir under `/var/lib` |
| Broken symlinks after migration | Copied files without preserving links | Use `rsync -a` or `cp -a`; verify with `find / -xtype l` |

## Summary

- FHS standardizes directory purposes so configs, logs, programs, and user data have predictable locations
- **`/etc`** = static host-specific configuration; **`/var`** = growing logs and application state; **`/usr`** = packaged programs and libraries
- **`/proc`** and **`/sys`** are virtual filesystems exposing live kernel and process data
- **`/dev`** contains device nodes; **`/boot`** holds kernels — keep it small and monitored
- **`/tmp`** is ephemeral and world-writable; **`/var/tmp`** persists across reboots
- Production reliability depends on separating `/var` from `/` and rotating logs under `/var/log`

## Interview Questions

1. What is the FHS, and why does it matter for DevOps automation?
2. What is the difference between `/etc`, `/usr`, and `/var`?
3. Explain the purpose of `/proc` and name three useful files inside it.
4. Why should application logs be stored under `/var/log` rather than `/opt` or `/home`?
5. What is the sticky bit on `/tmp`, and why is it important?
6. What is the difference between `/bin` and `/usr/bin` on a modern Ubuntu system?
7. Where would you look for systemd service unit overrides?
8. What lives in `/boot`, and what happens if that partition fills up?
9. Explain the difference between `/mnt` and `/media`.
10. How do you determine which package installed a file at `/etc/nginx/nginx.conf`?

??? tip "Sample Answers (Questions 2, 5, and 7)"

    **Q2 — /etc vs /usr vs /var:** `/etc` holds host-specific static configuration that administrators edit — nginx.conf, passwd, fstab. `/usr` holds read-only software installed by the package manager — binaries in `/usr/bin`, libraries in `/usr/lib`, documentation in `/usr/share`. `/var` holds data that changes during operation — logs in `/var/log`, database files in `/var/lib/mysql`, mail queues in `/var/spool`. The mnemonic: **etc** = editable config, **usr** = Unix system resources (programs), **var** = variable.

    **Q5 — Sticky bit on /tmp:** `/tmp` is mode `1777` — world read/write/execute plus sticky bit (`t`). Anyone can create files, but only the file owner (or root) can delete or rename their own files. Without the sticky bit, user A could delete user B's temporary files — a security and stability problem on multi-user systems.

    **Q7 — systemd overrides:** Package-provided units live in `/usr/lib/systemd/system/`. Administrator overrides go in `/etc/systemd/system/` — either as new unit files or drop-in snippets in `/etc/systemd/system/servicename.service.d/override.conf`. After changes, run `systemctl daemon-reload && systemctl restart servicename`. Editing files directly under `/usr/lib/systemd/system/` is wrong because package upgrades will overwrite them.

## Related Tutorials

- [Linux – Category Overview](index.md)
- [Introduction to Linux](introduction-to-linux.md) *(previous in Module 1)*
- [Essential Linux Commands](essential-linux-commands.md) *(next in Module 1)*
- [File Permissions and Ownership](file-permissions-and-ownership.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)
- Cheat sheet: [Linux Cheat Sheet](../cheatsheets/linux.md)
- Interview prep: [Linux Interview Prep](../interview/linux.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [Filesystem Hierarchy Standard (FHS 3.0)](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html) — official specification
- [Linux man pages — hier(7)](https://man7.org/linux/man-pages/man7/hier.7.html) — overview of filesystem hierarchy
- [systemd file hierarchy](https://www.freedesktop.org/software/systemd/man/latest/file-hierarchy.html) — systemd's perspective on FHS
- [Linux man pages online](https://man7.org/linux/man-pages/)
- [REBASH Academy – Linux Overview](index.md)
