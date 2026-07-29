#!/usr/bin/env python3
"""Generate REBASH Academy Linux for Cloud & DevOps tutorials 1–25 under docs/linux/."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "linux"
D2_DIR = ROOT / "docs" / "assets" / "d2"
IMG_DIR = ROOT / "docs" / "assets" / "images"
AUTHOR = "Shaik Basha"
DATE = "2026-07-29"

# (num, slug, title, module, difficulty, minutes, diagram, tag_extra, desc, overview, theory, lab_focus)
SPEC: list[tuple] = [
    (
        1,
        "linux-fundamentals-distributions-and-architecture",
        "Linux Fundamentals — Distributions and Architecture",
        "Module 1: Linux Fundamentals",
        "beginner",
        "45 min",
        "linux-architecture",
        ["fundamentals", "kernel", "distros"],
        "What Linux is, how distributions differ, and how kernel, user space, shell and terminal fit together for Cloud and DevOps work.",
        "Cloud VMs, Kubernetes nodes, and CI runners are almost always Linux. This tutorial builds the mental model you need before touching files, services, or networking.",
        """### What is Linux?

**Linux** is a free, open-source **kernel** — the core that manages CPU, memory, devices, and process isolation. A complete system also needs user-space tools (GNU coreutils, systemd, package managers, shells). People say “a Linux server” to mean that whole stack.

For Cloud and DevOps engineers, Linux is the default OS for:

- Virtual machines on AWS, Azure, GCP, and on-prem
- Container hosts and Kubernetes worker nodes
- CI/CD runners and build agents
- Network appliances and bastion hosts

### Linux distributions

A **distribution** (distro) packages the kernel with userspace, an installer, a package manager, and a release policy.

| Family | Examples | Package tool | Typical Cloud use |
|--------|----------|--------------|-------------------|
| Debian | Debian, Ubuntu | `apt` | Popular cloud images, docs, CI |
| RHEL | RHEL, Rocky, Alma, Fedora | `dnf`/`yum` | Enterprise, OpenShift, compliance |
| SUSE | SLES, openSUSE | `zypper` | Enterprise SAP/cloud niches |
| Minimal | Alpine, Amazon Linux | `apk` / `dnf` | Containers, AWS-tuned hosts |

Choose for support windows, package freshness, and organisational standards — not fashion. Cloud images pin a known AMI/image version so fleets stay reproducible.

### Linux architecture

Layers (bottom to top):

1. **Hardware** — CPU, RAM, disks, NICs (or virtual equivalents)
2. **Kernel** — drivers, scheduling, memory, networking stack, namespaces/cgroups
3. **User space** — daemons, libraries, CLI tools, containers
4. **Shell / applications** — Bash, Python, nginx, kubelet

System calls (`open`, `read`, `fork`, `exec`, `socket`) are the contract between user space and the kernel.

### Kernel

The kernel:

- Schedules processes and threads
- Manages virtual memory and page cache
- Mediates block and network I/O
- Enforces permissions, capabilities, and Mandatory Access Control (MAC) hooks (SELinux/AppArmor)

Inspect with `uname -r`, `hostnamectl`, and `/proc` (`/proc/cpuinfo`, `/proc/meminfo`).

### User space

Everything that is not the kernel: `systemd`, `sshd`, package managers, shells, libraries under `/usr`, application binaries. Failures here are often recoverable without a reboot; kernel panics are not.

### Shell versus terminal

| Concept | Role |
|---------|------|
| **Terminal** (emulator) | UI that accepts keystrokes and displays text (GNOME Terminal, Windows Terminal, `tmux`) |
| **Shell** | Program that interprets commands (`bash`, `zsh`, `sh`) |
| **TTY / PTY** | Kernel device pairing the terminal to a login session |

You SSH into a PTY running a shell. Scripts skip the interactive terminal but still need a shell interpreter via the shebang.
""",
        "fingerprint distro/kernel; map layers; prove shell vs terminal",
    ),
    (
        2,
        "boot-process-and-filesystem-hierarchy",
        "Boot Process and Filesystem Hierarchy",
        "Module 1: Linux Fundamentals",
        "beginner",
        "50 min",
        "linux-boot-process",
        ["boot", "fhs", "systemd"],
        "Follow the Linux boot path from firmware to multi-user target and learn the Filesystem Hierarchy Standard (FHS) used on Cloud VMs.",
        "When a cloud instance fails to come up, you need the boot chain and FHS landmarks. This tutorial maps both.",
        """### Boot process (Cloud VM view)

Typical order:

1. **Firmware** — BIOS or UEFI initialises hardware / hypervisor presents a virtual firmware
2. **Bootloader** — GRUB (or cloud-init friendly alternatives) loads the kernel and initramfs
3. **Kernel** — mounts root (often via initramfs), starts PID 1
4. **PID 1 (systemd)** — mounts filesystems, starts units, reaches a **target** (e.g. `multi-user.target`)
5. **cloud-init** (on cloud images) — applies instance metadata, SSH keys, hostname, packages

Useful commands:

```bash
systemd-analyze
systemd-analyze blame | head
systemctl get-default
systemctl list-units --type=target
```

Emergency recovery often means GRUB → rescue/emergency target → remount root `rw` → fix `/etc` or disk.

### Filesystem Hierarchy Standard (FHS)

The **Filesystem Hierarchy Standard (FHS)** defines where things live so scripts and packages stay portable.

| Path | Purpose |
|------|---------|
| `/` | Root of the tree |
| `/bin`, `/sbin`, `/usr/bin`, `/usr/sbin` | Essential and user commands (merged `/usr` is common) |
| `/etc` | Host configuration |
| `/home` | User home directories |
| `/var` | Variable data — logs, caches, spools |
| `/var/log` | Traditional log files |
| `/tmp`, `/var/tmp` | Temporary files (reboot-cleared vs preserved) |
| `/opt` | Optional add-on software |
| `/srv` | Site-specific served data |
| `/proc`, `/sys` | Kernel/process interfaces (pseudo-filesystems) |
| `/dev` | Device nodes |
| `/boot` | Kernel, initramfs, bootloader configs |
| `/mnt`, `/media` | Temporary / removable mounts |
| `/run` | Runtime state since boot (tmpfs) |

Cloud tip: separate disks often mount at `/var`, `/data`, or `/mnt/data` — never assume a single root disk has infinite space.
""",
        "trace boot with systemd-analyze; map FHS directories; document mounts",
    ),
    (
        3,
        "essential-linux-commands",
        "Essential Linux Commands",
        "Module 2: Command Line Essentials",
        "beginner",
        "50 min",
        "linux-essential-commands",
        ["cli", "commands", "navigation"],
        "Master everyday navigation and file commands — pwd, ls, cd, mkdir, rm, cp, mv, touch, cat, less, head, tail, stat, file, and history.",
        "Every SSH session starts here. Fluent use of these tools is the baseline for automation and incident response.",
        """### Navigation and listing

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
""",
        "navigate lab tree; practise cp/mv/rm safely; use less/stat/history",
    ),
    (
        4,
        "filesystem-paths-links-mounts-and-inodes",
        "Filesystem Paths, Links, Mounts, and Inodes",
        "Module 3: Linux Filesystem",
        "beginner",
        "50 min",
        "linux-filesystem-links",
        ["filesystem", "inodes", "links", "mounts"],
        "Understand directory structure, absolute versus relative paths, hard links, symbolic links, mount points, and inodes.",
        "Broken symlinks, surprise bind mounts, and inode exhaustion look like “disk full” until you know the model.",
        """### Directory structure

A Linux filesystem is a single rooted tree. Devices appear as **mount points** grafted into that tree — not as drive letters.

### Absolute versus relative paths

| Type | Example | Notes |
|------|---------|-------|
| Absolute | `/var/log/nginx/error.log` | Starts at `/`; stable from any cwd |
| Relative | `../configs/app.toml` | Depends on current directory |
| Home-relative | `~/rebash-linux` | Expanded by the shell |

Scripts should prefer absolute paths or resolve from a known base directory.

### Inodes

An **inode** stores metadata (owner, mode, timestamps, size, data block pointers) — not the filename. A directory entry maps a name → inode number.

```bash
ls -i file.txt
stat -c '%i %n' file.txt
df -i   # inode capacity
```

You can run out of inodes while `df -h` still shows free space (many tiny files).

### Hard links

A **hard link** is another directory entry pointing at the same inode (same filesystem only). Deleting one name decrements the link count; data remains until count reaches zero.

```bash
ln original.txt hardlink.txt
```

### Symbolic links (symlinks)

A **symlink** is a special file storing a path string. It can cross filesystems and point at directories.

```bash
ln -s /etc/os-release os-release.link
readlink -f os-release.link
```

Broken symlinks are common after moves — validate with `test -e` / `readlink`.

### Mount points

`mount` attaches a filesystem at a directory. `findmnt` and `/proc/mounts` show the live table; `/etc/fstab` (or systemd `.mount` units) persists mounts across reboot.

```bash
findmnt
lsblk -f
```
""",
        "create hard/symlink pairs; inspect inodes; explore findmnt",
    ),
    (
        5,
        "disk-usage-and-file-attributes",
        "Disk Usage and File Attributes",
        "Module 3: Linux Filesystem",
        "beginner",
        "40 min",
        "linux-disk-usage-attrs",
        ["df", "du", "attributes", "stat"],
        "Measure disk usage with df and du, and inspect file attributes and timestamps with ls and stat.",
        "Capacity incidents dominate on-call. Learn to read df/du correctly and interpret file attributes under pressure.",
        """### File attributes

`ls -l` shows mode, link count, owner, group, size, mtime, name. `stat` exposes atime/mtime/ctime, inode, and device.

Extended attributes (xattrs) and flags (`chattr`/`lsattr` on ext4) appear in hardening and immutable-file scenarios:

```bash
lsattr file.txt 2>/dev/null || true
getfattr -d file.txt 2>/dev/null || true
```

### Disk usage — `df`

`df` reports **filesystem** free space (what the mount can still accept):

```bash
df -h
df -hT
df -i
```

Watch mount points, not just `/` — `/var` or `/var/lib/docker` often fill first on container hosts.

### Disk usage — `du`

`du` reports **directory tree** consumption:

```bash
du -sh ~/rebash-linux
du -h --max-depth=1 /var 2>/dev/null | sort -h
```

`df` vs `du` mismatches usually mean deleted-but-open files (restart the holding process) or bind mounts.

### `stat` for attributes

```bash
stat file.txt
stat -c '%a %U:%G %s %n' file.txt
```

Use size, ownership, and mode together when diagnosing permission-denied versus missing-file errors.
""",
        "compare df vs du; find largest dirs; capture stat attributes",
    ),
    (
        6,
        "users-groups-and-sudo",
        "Users, Groups, and sudo",
        "Module 4: Users & Permissions",
        "beginner",
        "45 min",
        "linux-users-groups-sudo",
        ["users", "groups", "sudo", "identity"],
        "Create and manage users and groups, and escalate safely with sudo on Cloud Linux hosts.",
        "Identity is the first control plane on a shared bastion or jump host. Get users, groups, and sudo right before permissions deep-dives.",
        """### Users

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
""",
        "inspect id/passwd; create lab user/group; practise sudo -l",
    ),
    (
        7,
        "permissions-acls-and-special-bits",
        "Permissions, ACLs, and Special Bits",
        "Module 4: Users & Permissions",
        "intermediate",
        "55 min",
        "linux-permission-model",
        ["chmod", "chown", "acl", "suid", "sgid", "sticky"],
        "Apply chmod, chown, chgrp, umask, ACLs, and special bits (sticky, SUID, SGID) correctly.",
        "Most “permission denied” tickets are mode, ownership, or umask mistakes — not mysterious kernel bugs.",
        """### chmod, chown, chgrp

POSIX modes: user / group / other × read(4) write(2) execute(1).

```bash
chmod 640 file.conf
chmod u=rwX,g=rX,o= dir/
chown user:group file
chgrp group file
```

Capital `X` sets execute only on directories or files that already had execute.

### umask

**umask** masks permissions at creation time. Common: `0022` (files `644`, dirs `755`) or `0002` for collaborative groups.

```bash
umask
umask 0027
```

### ACLs

**Access Control Lists (ACLs)** add named-user/named-group entries beyond owner/group/other.

```bash
setfacl -m u:appuser:rw file.txt
getfacl file.txt
setfacl -x u:appuser file.txt
```

Useful for shared deploy directories without widening “other”.

### Sticky bit, SUID, SGID

| Bit | On files | On directories |
|-----|----------|----------------|
| **Sticky** (`+t`) | (rare) | Only owner can delete their files (`/tmp`) |
| **SUID** (`+s` user) | Runs as file owner | — |
| **SGID** (`+s` group) | Runs as file group | New files inherit directory group |

```bash
chmod +t shared_dir
chmod u+s /usr/bin/passwd   # example — do not invent SUID binaries
chmod g+s team_dir
```

Audit unexpected SUID/SGID binaries on hardened hosts.
""",
        "set modes/umask; ACL grant; sticky/SGID directory demo",
    ),
    (
        8,
        "text-processing-grep-sed-awk",
        "Text Processing with grep, sed, and awk",
        "Module 5: Text Processing",
        "intermediate",
        "55 min",
        "linux-text-processing",
        ["grep", "sed", "awk", "pipelines"],
        "Filter and transform logs and configs with grep, sed, awk, cut, paste, tr, sort, uniq, wc, and xargs.",
        "Ops is text: logs, configs, CSV exports. These tools are your incident and automation toolkit.",
        """### grep

Search lines by pattern:

```bash
grep -RIn --exclude-dir=.git ERROR /var/log 2>/dev/null | head
grep -E '^(error|warn)' app.log
grep -v '^#' /etc/ssh/sshd_config
```

### sed

Stream editor for substitutions and deletes:

```bash
sed -n '1,20p' file
sed 's/foo/bar/g' file
sed -i.bak 's/Enable=false/Enable=true/' config.ini
```

### awk

Field-oriented reporting:

```bash
awk '{print $1,$3}' access.log
awk -F: '{print $1}' /etc/passwd
awk '{sum+=$1} END {print sum}' nums.txt
```

### cut, paste, tr

```bash
cut -d: -f1,7 /etc/passwd | head
paste -d',' a.txt b.txt
tr '[:upper:]' '[:lower:]' < mixed.txt
```

### sort, uniq, wc

```bash
sort file | uniq -c | sort -nr | head
wc -l file
```

### xargs

Build command lines from stdin (prefer `-0` with `find -print0`):

```bash
find . -name '*.log' -print0 | xargs -0 grep -l ERROR
```
""",
        "build a log pipeline with grep/sed/awk/sort/uniq/xargs",
    ),
    (
        9,
        "process-management",
        "Process Management",
        "Module 6: Process Management",
        "intermediate",
        "50 min",
        "linux-process-lifecycle",
        ["ps", "top", "kill", "nice", "jobs"],
        "Monitor and control processes with ps, top, htop, kill, pkill, jobs, fg, bg, nice, renice, and nohup.",
        "Runaway processes burn CPU budgets on cloud VMs. Lifecycle control is core SRE hygiene.",
        """### Viewing processes

| Tool | Role |
|------|------|
| `ps` | Snapshot (`ps aux`, `ps -ef`, `ps -p PID`) |
| `top` | Interactive live view |
| `htop` | Friendlier interactive view (if installed) |

```bash
ps aux --sort=-%cpu | head
ps -ef | grep '[s]shd'
```

### Signals — kill and pkill

```bash
kill -TERM PID
kill -KILL PID    # last resort
pkill -f 'pattern'
killall -TERM name  # where available
```

Prefer `TERM` then wait; `KILL` skips cleanup.

### Job control

| Command | Role |
|---------|------|
| `jobs` | List shell jobs |
| `fg` | Foreground a job |
| `bg` | Background a stopped job |
| `Ctrl-Z` | Suspend | 

```bash
sleep 300 &
jobs
fg %1
```

### Priority — nice / renice

Lower niceness → higher priority (range typically -20..19). Non-root can only increase niceness.

```bash
nice -n 10 ./batch.sh
renice -n 15 -p PID
```

### nohup

Survive hangup when the terminal closes:

```bash
nohup ./long-job.sh > long-job.out 2>&1 &
```

Prefer `systemd --user` services or timers for production longevity over raw nohup.
""",
        "inspect ps/top; job control; nice/nohup a background task",
    ),
    (
        10,
        "systemd-services-and-journalctl",
        "systemd Services and journalctl",
        "Module 7: Services & Boot",
        "intermediate",
        "55 min",
        "linux-systemd-architecture",
        ["systemd", "systemctl", "journalctl"],
        "Manage services with systemd and systemctl, and query logs with journalctl.",
        "Almost every Linux Cloud image uses systemd as PID 1. Service control and journal queries are daily ops.",
        """### systemd architecture

**systemd** is the init system and service manager: units (`.service`, `.socket`, `.timer`, `.mount`, …), dependencies, cgroups, and the journal.

### systemctl

```bash
systemctl status ssh
systemctl is-active nginx
systemctl start|stop|restart|reload UNIT
systemctl enable|--now UNIT
systemctl disable UNIT
systemctl list-units --type=service --state=failed
systemctl cat UNIT
systemctl edit UNIT   # drop-in overrides
```

Unit files live under `/lib/systemd/system` or `/etc/systemd/system`. Prefer drop-ins over editing vendor units.

### Services

A `.service` unit defines `ExecStart`, user, restart policy, dependencies (`After=`, `Requires=`), and hardening directives (`ProtectSystem=`, `NoNewPrivileges=`).

### journalctl

**journald** stores structured logs:

```bash
journalctl -u ssh -e
journalctl -u nginx --since '1 hour ago'
journalctl -p err..alert -b
journalctl -f
```

`-b` current boot; `_PID=` / `_UID=` match fields. Persist journal on disk for post-reboot forensics (`/var/log/journal`).
""",
        "inspect units; read journal; create a simple user service",
    ),
    (
        11,
        "systemd-targets-timers-and-boot",
        "systemd Targets, Timers, and Boot",
        "Module 7: Services & Boot",
        "intermediate",
        "50 min",
        "linux-systemd-targets",
        ["targets", "timers", "boot"],
        "Control boot targets, schedule work with systemd timers, and reason about the service-side boot process.",
        "Targets replace runlevels; timers replace many cron jobs with better logging and dependencies.",
        """### Targets

**Targets** group units (like runlevels):

| Target | Role |
|--------|------|
| `rescue.target` | Single-user recovery |
| `multi-user.target` | Standard server (no GUI) |
| `graphical.target` | Desktop |
| `network-online.target` | Network is configured |

```bash
systemctl get-default
systemctl set-default multi-user.target
systemctl isolate rescue.target   # disruptive — know before using
```

### Timers

`.timer` units activate `.service` units on calendar or monotonic schedules.

```bash
systemctl list-timers --all
systemctl status logrotate.timer
```

Example calendar: `OnCalendar=*-*-* 02:30:00`. Prefer timers when you need dependency ordering, jitter, or unified journals.

### Boot process (service side)

After the kernel starts PID 1:

1. systemd loads units
2. `sysinit` / local-fs / network targets activate
3. Default target pulls in enabled services
4. `cloud-init` stages may still be running on first boot

```bash
systemd-analyze critical-chain
systemctl list-dependencies multi-user.target
```
""",
        "list timers/targets; write a oneshot+timer pair; analyse boot chain",
    ),
    (
        12,
        "storage-disks-partitions-and-filesystems",
        "Storage — Disks, Partitions, and Filesystems",
        "Module 8: Storage Management",
        "intermediate",
        "55 min",
        "linux-storage-layout",
        ["lsblk", "fdisk", "parted", "mkfs", "mount"],
        "Discover disks with lsblk, partition with fdisk/parted, create filesystems with mkfs, and mount/umount safely.",
        "Attaching an EBS/Azure disk is useless until you partition, format, mount, and persist it.",
        """### Discover — lsblk

```bash
lsblk -f
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,UUID
```

### Partition — fdisk and parted

```bash
sudo fdisk -l
# sudo fdisk /dev/sdX     # interactive — lab VMs only
# sudo parted /dev/sdX print
```

GPT is standard for modern cloud disks. Always confirm the device name — wrong disk destroys data.

### Filesystems — mkfs

```bash
# sudo mkfs.ext4 /dev/sdX1
# sudo mkfs.xfs /dev/sdX1
```

Choose ext4 (ubiquitous) or XFS (common on RHEL large volumes). Record UUID from `blkid`.

### mount and umount

```bash
sudo mount UUID=... /mnt/data
findmnt /mnt/data
sudo umount /mnt/data
```

Persist via `/etc/fstab` or systemd `.mount` units. Use `nofail` for secondary data disks on cloud images so boot continues if the volume is detached.
""",
        "map lsblk; practise mount options on a loop file; draft fstab line",
    ),
    (
        13,
        "lvm-swap-and-disk-monitoring",
        "LVM, Swap, and Disk Monitoring",
        "Module 8: Storage Management",
        "intermediate",
        "50 min",
        "linux-lvm-swap",
        ["lvm", "swap", "monitoring"],
        "Grow storage with LVM, manage swap, and monitor disks before they page or fill.",
        "LVM turns “we need 50 GiB more” into an online extend instead of a migration weekend.",
        """### LVM basics

**Logical Volume Manager (LVM)** layers:

- **PV** — physical volume on a disk/partition
- **VG** — volume group pool
- **LV** — logical volume (formatted and mounted)

```bash
sudo pvs; sudo vgs; sudo lvs
# pvcreate → vgcreate → lvcreate → mkfs → mount
# lvextend -L +10G /dev/vg/lv && resize2fs|xfs_growfs
```

### Swap

Swap backs memory pressure. On cloud VMs, sizing is a policy choice (often small or none on large RAM nodes; required for some hibernate features).

```bash
swapon --show
free -h
# fallocate / mkswap / swapon / fstab entry
```

Watch swap-in/out with `vmstat` — heavy swapping kills latency.

### Disk monitoring

| Signal | Tool |
|--------|------|
| Capacity | `df -h`, `df -i` |
| Hot directories | `du` |
| I/O pressure | `iostat`, `iotop` |
| SMART / cloud metrics | vendor agents, `lsblk` |

Alert on mount utilisation (e.g. 80/90%) and inode use, not only root filesystem size.
""",
        "inspect pvs/vgs/lvs if present; review swap; script a df alert stub",
    ),
    (
        14,
        "linux-networking-tools",
        "Linux Networking Tools",
        "Module 9: Linux Networking",
        "intermediate",
        "55 min",
        "linux-networking-stack",
        ["ip", "ss", "dns", "tcpdump"],
        "Troubleshoot connectivity with ip, ss, ping, traceroute, dig, nslookup, host, curl, wget, tcpdump, and netcat.",
        "Prefer the modern `ip`/`ss` stack — ifconfig/netstat are legacy on current Cloud images.",
        """### Interfaces and routes — ip

```bash
ip -br a
ip route
ip neigh
```

### Sockets — ss

```bash
ss -tulpn
ss -tp | head
```

### Path checks — ping / traceroute

```bash
ping -c 3 1.1.1.1
traceroute -n example.com   # or tracepath
```

### DNS — dig / nslookup / host

```bash
dig +short example.com A
host example.com
nslookup example.com
```

### HTTP clients — curl / wget

```bash
curl -I https://example.com
curl -fsS -o /dev/null -w '%{http_code}\\n' https://example.com
wget -qO- https://example.com | head
```

### Capture and raw TCP — tcpdump / netcat

```bash
sudo tcpdump -ni any port 443 -c 20
nc -vz example.com 443
```

Use captures briefly and with privacy in mind — payloads may contain secrets.
""",
        "fingerprint ip/ss; DNS checks; curl health; nc port probe",
    ),
    (
        15,
        "ssh-and-remote-access",
        "SSH and Remote Access",
        "Module 9: Linux Networking",
        "intermediate",
        "45 min",
        "linux-ssh-access",
        ["ssh", "remote", "keys"],
        "Use SSH for remote administration — config, keys basics, tunnels, and scp/rsync — before hardening deep-dives.",
        "SSH is how you reach Cloud VMs. Master access fundamentals here; Module 13 covers hardening.",
        """### SSH basics

```bash
ssh user@host
ssh -i ~/.ssh/id_ed25519 user@host
ssh -o StrictHostKeyChecking=accept-new user@host
```

Client config (`~/.ssh/config`):

```text
Host bastion
  HostName bastion.example.com
  User ubuntu
  IdentityFile ~/.ssh/id_ed25519
```

### Keys (access fundamentals)

```bash
ssh-keygen -t ed25519 -a 100 -f ~/.ssh/id_ed25519_lab -C 'rebash-lab'
ssh-copy-id -i ~/.ssh/id_ed25519_lab.pub user@host
```

Prefer keys over passwords. Agent forwarding is convenient and risky — avoid on untrusted hosts.

### Copy and tunnels

```bash
scp file user@host:/tmp/
rsync -avz ./dir/ user@host:/tmp/dir/
ssh -L 8080:127.0.0.1:80 user@host
```

### Server side (preview)

`sshd` reads `/etc/ssh/sshd_config`. Hardening (disable password auth, restrict users, AllowUsers) is covered in Module 13 — here, verify you can log in and run remote commands:

```bash
ssh user@host 'hostname; uptime'
```
""",
        "generate lab keypair; write SSH config Host entry; test remote command",
    ),
    (
        16,
        "package-management",
        "Package Management",
        "Module 10: Package Management",
        "beginner",
        "45 min",
        "linux-package-management",
        ["apt", "dnf", "yum", "zypper", "snap", "flatpak"],
        "Install and maintain software with apt, dnf, yum, zypper, and understand snap/flatpak on Linux hosts.",
        "Unpatched packages are vulnerability debt. Fluent package ops keep fleets consistent.",
        """### Debian / Ubuntu — apt

```bash
sudo apt update
sudo apt install -y curl jq
apt policy curl
sudo apt upgrade
dpkg -l | head
```

### RHEL family — dnf / yum

```bash
sudo dnf install -y curl jq    # Fedora/RHEL8+
sudo yum install -y curl       # older RHEL/CentOS
rpm -q curl
```

### SUSE — zypper

```bash
sudo zypper refresh
sudo zypper install curl
```

### Universal / desktop-oriented — snap / flatpak

```bash
snap list 2>/dev/null || true
flatpak list 2>/dev/null || true
```

Snaps/Flatpaks sandbox desktop apps; servers usually stick to distro packages or containers. Prefer distro packages for system daemons.

### Ops hygiene

- Pin critical versions in golden images
- Use unattended-upgrades / dnf-automatic thoughtfully
- Remove unused packages; reboot when kernel updates require it
""",
        "detect package manager; install a CLI tool; query package metadata",
    ),
    (
        17,
        "scheduling-cron-at-and-timers",
        "Scheduling with cron, at, and Timers",
        "Module 11: Scheduling & Automation",
        "intermediate",
        "45 min",
        "linux-scheduling",
        ["cron", "crontab", "at", "timers"],
        "Schedule recurring and one-shot jobs with cron, crontab, at, and systemd timers.",
        "Backups, reports, and cleanup need reliable schedules with visible logs.",
        """### cron and crontab

```bash
crontab -l
crontab -e
```

Format: `minute hour dom month dow command`

```cron
*/15 * * * * /usr/local/bin/healthcheck.sh >>/var/log/healthcheck.log 2>&1
```

System crontabs: `/etc/crontab`, `/etc/cron.d/`. Set `PATH` or use absolute paths — cron’s environment is minimal.

### at

One-shot jobs:

```bash
echo 'echo hello' | at now + 2 minutes
atq
atrm JOB
```

### systemd timers

Prefer for services you already manage with systemd:

```bash
systemctl list-timers
# pair foo.service + foo.timer; systemctl enable --now foo.timer
```

Timers integrate with `journalctl -u foo.service` and dependency ordering — better observability than silent cron mail.
""",
        "add a user crontab entry; queue an at job; inspect systemd timers",
    ),
    (
        18,
        "logging-syslog-journald-logrotate",
        "Logging — syslog, journald, and logrotate",
        "Module 12: Logging & Monitoring",
        "intermediate",
        "45 min",
        "linux-logging",
        ["syslog", "journald", "logrotate"],
        "Follow the logging stack — syslog, journald, and logrotate — on modern Linux servers.",
        "If it is not logged, it did not happen during the incident review.",
        """### syslog

Traditional syslog (`rsyslog` / `syslog-ng`) writes text logs under `/var/log` (`syslog`, `auth.log`, `messages`). Apps may still log via syslog API.

```bash
ls /var/log | head
tail -n 50 /var/log/syslog 2>/dev/null || tail -n 50 /var/log/messages
```

### journald

systemd’s journal stores structured, indexed logs:

```bash
journalctl -b -p err
journalctl -u ssh --since today
```

Forwarding to rsyslog/SIEM is common in enterprises.

### logrotate

Prevents disks filling from growing log files via `/etc/logrotate.conf` and `/etc/logrotate.d/*`:

```bash
sudo logrotate -d /etc/logrotate.conf
```

Policies set rotation frequency, compress, delaycompress, and postrotate hooks (signal nginx/rsyslog).
""",
        "query journal and /var/log; dry-run logrotate; draft a rotate stanza",
    ),
    (
        19,
        "host-monitoring-vmstat-iostat-sar",
        "Host Monitoring with vmstat, iostat, and sar",
        "Module 12: Logging & Monitoring",
        "intermediate",
        "45 min",
        "linux-host-monitoring",
        ["vmstat", "iostat", "sar", "capacity"],
        "Read host health with vmstat, iostat, free, uptime, df, du, and sar.",
        "Before installing a heavyweight agent, know what the classic tools already tell you.",
        """### Instant signals

| Tool | Shows |
|------|-------|
| `uptime` | Load averages, users |
| `free -h` | Memory / swap |
| `df -h` / `du` | Disk capacity / tree usage |

### vmstat

```bash
vmstat 1 5
```

Watch `r` (run queue), `si`/`so` (swap), `wa` (I/O wait).

### iostat

```bash
iostat -xz 1 5   # sysstat package
```

Util%, await, and saturation expose disk bottlenecks.

### sar

**System Activity Reporter** (sysstat) retains historical samples:

```bash
sar -u 1 5
sar -r 1 5
sar -d 1 5
```

Enable collection via `sysstat` timer/cron for post-incident graphs.
""",
        "capture uptime/free/df; run vmstat/iostat/sar samples; summarise",
    ),
    (
        20,
        "ssh-hardening-and-firewalls",
        "SSH Hardening and Firewalls",
        "Module 13: Linux Security",
        "advanced",
        "55 min",
        "linux-ssh-hardening",
        ["ssh", "firewalld", "ufw", "hardening"],
        "Harden SSH with keys and sshd_config, and control exposure with firewalld or ufw.",
        "Most internet-facing Linux breaches start with weak SSH or open management ports.",
        """### SSH keys and hardening

```bash
# sshd_config (edit carefully; keep a session open)
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
AllowUsers deploy
KbdInteractiveAuthentication no
```

```bash
sudo sshd -t && sudo systemctl reload ssh
```

Use fail2ban or cloud security groups as defence in depth. Rotate keys; prefer hardware-backed or short-lived certs where available.

### firewalld (RHEL family)

```bash
sudo firewall-cmd --state
sudo firewall-cmd --list-all
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

### ufw (Ubuntu)

```bash
sudo ufw status verbose
sudo ufw allow OpenSSH
sudo ufw enable
```

Default deny incoming; allow only required service ports. Align host firewalls with cloud security groups — do not rely on one alone.
""",
        "audit sshd settings; review ufw/firewalld; draft hardened snippets",
    ),
    (
        21,
        "selinux-apparmor-fail2ban-auditd-pam",
        "SELinux, AppArmor, Fail2Ban, Auditd, and PAM",
        "Module 13: Linux Security",
        "advanced",
        "55 min",
        "linux-mac-security",
        ["selinux", "apparmor", "fail2ban", "auditd", "pam"],
        "Apply Mandatory Access Control, intrusion prevention, audit trails, and PAM authentication stacks.",
        "Permissions are DAC; production hosts also need MAC, auditing, and sane authentication policy.",
        """### SELinux (RHEL family)

```bash
getenforce
sudo setenforce 0   # temporary permissive — not a production fix
ls -Z file
```

Modes: Enforcing, Permissive, Disabled. Fix labels (`restorecon`) rather than disabling.

### AppArmor (Ubuntu/SUSE)

```bash
sudo aa-status
```

Profiles confine programmes; complain vs enforce modes aid tuning.

### Fail2Ban

Bans IPs after repeated auth failures (SSH, etc.):

```bash
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

### Auditd

Kernel audit framework for compliance trails:

```bash
sudo ausearch -m USER_LOGIN -ts recent 2>/dev/null | tail
sudo auditctl -l 2>/dev/null | head
```

### PAM

**Pluggable Authentication Modules** stack controls login, sudo, and SSH auth (`/etc/pam.d/*`). Mis-edited PAM can lock everyone out — always keep a root session and test carefully.
""",
        "check MAC status; inspect pam.d/sshd; review fail2ban/audit if present",
    ),
    (
        22,
        "containers-namespaces-cgroups-and-oci",
        "Containers — Namespaces, cgroups, OverlayFS, and OCI",
        "Module 14: Containers & Cloud",
        "advanced",
        "55 min",
        "linux-container-internals",
        ["namespaces", "cgroups", "overlayfs", "oci"],
        "Understand Linux container building blocks — namespaces, cgroups, OverlayFS, OCI, and runtime basics.",
        "Kubernetes nodes are Linux. Container isolation is kernel features, not magic.",
        """### Namespaces

Namespaces isolate views of the system: PID, NET, MNT, UTS, IPC, USER, CGROUP, TIME.

```bash
lsns
ps -o pid,ns,cmd
```

A container is usually a process (tree) in multiple namespaces.

### cgroups

**Control groups** limit/account CPU, memory, I/O, PIDs (v2 unified hierarchy under `/sys/fs/cgroup`).

```bash
systemd-cgls | head
cat /proc/self/cgroup
```

### OverlayFS

Union filesystem: lower image layers + upper writable layer = container rootfs. Explains thin image pulls and copy-on-write.

### OCI concepts

The **Open Container Initiative (OCI)** defines image and runtime specs. Images are tarball layers + config; runtimes (runc, crun) create namespaces/cgroups and start the entrypoint.

### Container runtime basics

High level: container engine (Docker/containerd/CRi-O) → OCI runtime → kernel. On Kubernetes: kubelet → CRI → runtime.

```bash
command -v docker containerd crictl 2>/dev/null
```
""",
        "explore lsns/cgroups; sketch OCI stack; inspect a running container if available",
    ),
    (
        23,
        "troubleshooting-linux-systems",
        "Troubleshooting Linux Systems",
        "Module 15: Troubleshooting",
        "advanced",
        "60 min",
        "linux-troubleshooting",
        ["troubleshooting", "incidents", "performance"],
        "Systematically debug boot failures, high CPU/memory, disk full, permissions, network, service failures, logs, and bottlenecks.",
        "Incidents reward a checklist over panic. Build a repeatable troubleshooting path.",
        """### Method

1. Define blast radius and recent changes
2. Check urgency signals: `uptime`, `free`, `df`, `systemctl --failed`
3. Narrow domain: boot / CPU / memory / disk / perms / net / service
4. Confirm with logs (`journalctl`, app logs)
5. Change one variable; write down what you tried

### Boot failures

GRUB → rescue → `journalctl -b -p err`, `systemctl list-units --failed`, filesystem checks, fstab `nofail`, cloud-init status.

### High CPU

`top`/`ps` → identify PID → `perf`/`strace` sparingly → restart or scale → fix root cause (loop, noisy neighbour).

### High memory

`free -h`, `ps --sort=-%mem`, OOM killer (`dmesg`/`journalctl -k`), leak vs undersized VM.

### Disk full

`df -h` + `df -i` → `du` → deleted-open files (`lsof +L1`) → logrotate → expand volume/LVM.

### Permission issues

`namei -l path`, `id`, ACLs (`getfacl`), MAC denials (`ausearch`/`journalctl` for SELinux).

### Network problems

`ip route`, `ss`, DNS (`dig`), security groups/firewalls, `curl -v`, `tcpdump`.

### Service failures

`systemctl status -l`, `journalctl -u`, config test (`nginx -t`, `sshd -t`), dependency targets.

### Log analysis

Time-box: since deploy / since alert. Correlate host journal + app + load balancer.

### Performance bottlenecks

USE method (utilisation, saturation, errors) with `vmstat`, `iostat`, `sar`, application metrics.
""",
        "build a troubleshooting toolkit script; run failed-unit and df/cpu checks",
    ),
    (
        24,
        "production-linux-hardening-and-performance",
        "Production Linux — Hardening and Performance",
        "Module 16: Production Linux",
        "advanced",
        "55 min",
        "linux-production-hardening",
        ["hardening", "performance", "ops"],
        "Apply production hardening, performance tuning, capacity planning, monitoring, logging, and operational excellence.",
        "Shipping a VM is easy; running it safely under load is the job.",
        """### Linux hardening

- Patch cadence and reboot windows
- SSH hardening + host firewall + cloud SG
- Minimal packages; no compilers on prod if policy says so
- MAC (SELinux/AppArmor) enforcing
- Auditd / central logs; time sync (chrony)
- Separate disks for data; encrypted volumes where required

### Performance tuning

Tune only with evidence: sysctl (`vm.swappiness`, network buffers), CPU governor (cloud usually managed), application pools, disk IOPS classes. Document every sysctl in config management.

### Capacity planning

Track trends: CPU, memory, disk, inodes, network. Right-size instances; prefer horizontal scale for stateless tiers.

### Monitoring and logging

Host metrics + logs + alerts with runbooks. SLOs beat vanity dashboards.

### Operational excellence

Immutable golden images, config as code, change tickets, blameless postmortems, game days for failure modes.
""",
        "audit hardening checklist; capture baseline metrics; draft sysctl notes",
    ),
    (
        25,
        "backup-disaster-recovery-and-capacity",
        "Backup, Disaster Recovery, and Capacity",
        "Module 16: Production Linux",
        "advanced",
        "50 min",
        "linux-backup-dr",
        ["backup", "dr", "capacity"],
        "Design backup strategies and disaster recovery drills, with capacity planning overlapping production ops.",
        "Backups that were never restored are fiction. DR is a practised procedure, not a folder of tar files.",
        """### Backup strategies

| Pattern | Notes |
|---------|-------|
| File-level | `tar`, `rsync`, Borg, restic |
| Block/volume | Cloud snapshots (EBS, Managed Disks) |
| Application-aware | Quiesce DB; use native dump tools |
| 3-2-1 | 3 copies, 2 media, 1 offsite |

Encrypt backups; test permissions on restore paths.

### Disaster recovery

Define RTO/RPO. Document restore steps. Drill: restore to a scratch VM, verify checksums/services, measure time. Include IAM/SSH access recovery in the plan.

### Capacity (overlap with tutorial 24)

Forecast growth from `sar`/metrics history. Alert before full disks. Plan snapshot retention costs — backups have a bill.

```bash
df -h
du -sh /var /home 2>/dev/null
```
""",
        "script a local backup+restore drill; document RTO/RPO assumptions",
    ),
]

assert len(SPEC) == 25, len(SPEC)

OBSOLETE = [
    "introduction-to-linux.md",
    "linux-filesystem-hierarchy.md",
    "file-permissions-and-ownership.md",
    "user-and-group-management.md",
    "systemd-service-management.md",
    "shell-scripting-fundamentals.md",
    "ssh-remote-administration.md",
    "remote-systemd-services.md",
    "disk-and-filesystem-management.md",
    "log-management-journalctl.md",
    "cron-and-task-scheduling.md",
    "environment-variables-shell-config.md",
    "linux-networking-essentials.md",
    "file-archiving-and-compression.md",
    "linux-security-hardening-basics.md",
    "linux-server-baseline-and-lifecycle.md",
    "nginx-web-server-and-reverse-proxy.md",
    "tls-certificates-on-linux-servers.md",
    "server-storage-lvm-and-fstab.md",
    "backup-restore-and-recovery-drills.md",
]

STYLE = (
    '*: { style: { border-radius: 14; font-size: 14; bold: true; '
    'shadow: true; stroke-width: 2 } }\n'
    "direction: right\n"
)


def _flow(a: str, b: str, c: str, d: str, ca="#dbeafe", cb="#dcfce7", cc="#ffedd5", cd="#fce7f3",
          sa="#2563eb", sb="#16a34a", sc="#ea580c", sd="#db2777") -> str:
    return dedent(
        f"""\
        {STYLE}A: "{a}" {{ style.fill: "{ca}"; style.stroke: "{sa}" }}
        B: "{b}" {{ style.fill: "{cb}"; style.stroke: "{sb}" }}
        C: "{c}" {{ style.fill: "{cc}"; style.stroke: "{sc}" }}
        D: "{d}" {{ style.fill: "{cd}"; style.stroke: "{sd}" }}
        A -> B -> C -> D
        """
    )


DIAGRAMS: dict[str, str] = {
    "linux-architecture": _flow("Hardware", "Kernel", "User space", "Shell / apps"),
    "linux-boot-process": _flow("Firmware", "Bootloader", "Kernel + initramfs", "systemd targets"),
    "linux-essential-commands": _flow("pwd / ls / cd", "mkdir cp mv rm", "cat less head tail", "stat file history"),
    "linux-filesystem-links": _flow("Path / name", "Directory entry", "inode", "Data blocks"),
    "linux-disk-usage-attrs": _flow("stat attrs", "du tree", "df mounts", "Capacity alert"),
    "linux-users-groups-sudo": _flow("Users", "Groups", "sudoers", "Effective UID"),
    "linux-permission-model": _flow("Owner/group/other", "chmod umask", "ACLs", "SUID SGID sticky"),
    "linux-text-processing": _flow("Text / logs", "grep filter", "sed / awk", "sort uniq xargs"),
    "linux-process-lifecycle": _flow("fork / exec", "Running", "Signals", "Exit / reaper"),
    "linux-systemd-architecture": _flow("Unit files", "systemd PID 1", "cgroups", "journald"),
    "linux-systemd-targets": _flow("sysinit", "basic.target", "multi-user", "Timers / services"),
    "linux-storage-layout": _flow("Disk", "Partition", "Filesystem", "Mount point"),
    "linux-lvm-swap": _flow("PV", "VG", "LV + fs", "Swap / monitor"),
    "linux-networking-stack": _flow("App / curl", "Sockets ss", "ip routing", "NIC / wire"),
    "linux-ssh-access": _flow("Client config", "SSH keys", "sshd", "Remote shell"),
    "linux-package-management": _flow("Repos", "apt dnf zypper", "Packages", "snap / flatpak"),
    "linux-scheduling": _flow("crontab", "at queue", "systemd timer", "Job + logs"),
    "linux-logging": _flow("Apps / syslog", "journald", "logrotate", "SIEM / files"),
    "linux-host-monitoring": _flow("uptime free df", "vmstat", "iostat", "sar history"),
    "linux-ssh-hardening": _flow("sshd_config", "SSH keys only", "firewalld / ufw", "Cloud SG"),
    "linux-mac-security": _flow("PAM stack", "SELinux / AppArmor", "Fail2Ban", "Auditd"),
    "linux-container-internals": _flow("Namespaces", "cgroups", "OverlayFS", "OCI runtime"),
    "linux-troubleshooting": _flow("Signals", "Narrow domain", "Logs", "Fix + verify"),
    "linux-production-hardening": _flow("Harden", "Tune", "Monitor", "Operate"),
    "linux-backup-dr": _flow("Backup", "Offsite copy", "Restore drill", "RTO / RPO"),
}

LAB_EXTRA: dict[int, str] = {
    1: dedent(
        """\
        ### Step 2 – Fingerprint the host

        ```bash
        cat > fingerprint.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        echo "=== OS ==="
        cat /etc/os-release | head -n 8
        echo "=== Kernel ==="
        uname -srm
        echo "=== Shell / TTY ==="
        echo "SHELL=$SHELL"
        tty || true
        ps -p $$ -o args=
        EOF
        chmod +x fingerprint.sh
        ./fingerprint.sh | tee fingerprint.txt
        ```
        """
    ),
    2: dedent(
        """\
        ### Step 2 – Boot and FHS map

        ```bash
        systemd-analyze 2>/dev/null || true
        systemctl get-default
        {
          echo "# FHS landmarks"
          for d in / /etc /var /var/log /home /usr /opt /boot /proc /sys /run; do
            printf '%s -> ' "$d"
            readlink -f "$d" 2>/dev/null || echo missing
          done
        } | tee fhs-map.txt
        findmnt -T / | tee root-mount.txt
        ```
        """
    ),
    3: dedent(
        """\
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
        """
    ),
    4: dedent(
        """\
        ### Step 2 – Links and inodes

        ```bash
        echo payload > original.txt
        ln original.txt hard.txt
        ln -s original.txt soft.txt
        ls -li original.txt hard.txt soft.txt | tee links.txt
        stat -c '%i %h %n' original.txt hard.txt
        readlink soft.txt
        findmnt | head | tee mounts.txt
        ```
        """
    ),
    5: dedent(
        """\
        ### Step 2 – Usage and attributes

        ```bash
        dd if=/dev/zero of=blob.bin bs=1M count=5 status=none
        df -h . | tee df.txt
        du -sh . blob.bin | tee du.txt
        stat blob.bin | tee stat.txt
        ls -l blob.bin
        ```
        """
    ),
    6: dedent(
        """\
        ### Step 2 – Identity inventory

        ```bash
        id | tee id.txt
        getent passwd "$USER"
        getent group | head
        sudo -n -l 2>&1 | tee sudo-l.txt || true
        echo "Create users only on disposable lab VMs with sudo."
        ```
        """
    ),
    7: dedent(
        """\
        ### Step 2 – Modes and ACL demo

        ```bash
        umask 0027
        echo secret > secret.txt
        chmod 640 secret.txt
        stat -c '%a %A %n' secret.txt | tee mode.txt
        if command -v setfacl >/dev/null; then
          setfacl -m u:"$USER":rw secret.txt || true
          getfacl secret.txt | tee acl.txt
        fi
        mkdir -p shared
        chmod 1777 shared
        ls -ld shared | tee sticky.txt
        ```
        """
    ),
    8: dedent(
        """\
        ### Step 2 – Log pipeline

        ```bash
        cat > sample.log << 'EOF'
        INFO start
        ERROR disk full
        WARN retry
        ERROR timeout
        INFO done
        EOF
        grep ERROR sample.log | tee errors.txt
        sed 's/ERROR/ERR/g' sample.log | tee sed-out.txt
        awk '/ERR|ERROR/{c++} END{print c+0}' sample.log | tee count.txt
        cut -d' ' -f1 sample.log | sort | uniq -c
        printf 'a\\nb\\n' | tr 'a-z' 'A-Z'
        echo errors.txt | xargs wc -l
        ```
        """
    ),
    9: dedent(
        """\
        ### Step 2 – Process control

        ```bash
        ps aux --sort=-%cpu | head -n 8 | tee top-cpu.txt
        sleep 120 &
        SPID=$!
        jobs
        renice -n 10 -p "$SPID" || true
        kill -TERM "$SPID"
        wait "$SPID" 2>/dev/null || true
        nohup bash -c 'echo nohup-ok; sleep 2' > nohup-lab.out 2>&1 &
        wait || true
        cat nohup-lab.out
        ```
        """
    ),
    10: dedent(
        """\
        ### Step 2 – systemd and journal

        ```bash
        systemctl list-units --type=service --state=running | head | tee services.txt
        systemctl status ssh 2>/dev/null || systemctl status sshd 2>/dev/null || true
        journalctl -b -p err -n 20 --no-pager 2>/dev/null | tee journal-err.txt || true
        mkdir -p ~/.config/systemd/user
        cat > ~/.config/systemd/user/rebash-lab.service << 'EOF'
        [Unit]
        Description=REBASH lab oneshot
        [Service]
        Type=oneshot
        ExecStart=/bin/echo rebash-lab-ok
        EOF
        systemctl --user daemon-reload 2>/dev/null || true
        systemctl --user start rebash-lab.service 2>/dev/null || true
        ```
        """
    ),
    11: dedent(
        """\
        ### Step 2 – Targets and timers

        ```bash
        systemctl get-default | tee default-target.txt
        systemctl list-timers --all | head | tee timers.txt
        systemd-analyze critical-chain 2>/dev/null | head | tee boot-chain.txt || true
        cat > ~/.config/systemd/user/rebash-tick.service << 'EOF'
        [Unit]
        Description=REBASH tick
        [Service]
        Type=oneshot
        ExecStart=/bin/date
        EOF
        cat > ~/.config/systemd/user/rebash-tick.timer << 'EOF'
        [Unit]
        Description=REBASH tick timer
        [Timer]
        OnCalendar=*:0/30
        Persistent=true
        [Install]
        WantedBy=timers.target
        EOF
        systemctl --user daemon-reload 2>/dev/null || true
        systemctl --user list-timers 2>/dev/null | head || true
        ```
        """
    ),
    12: dedent(
        """\
        ### Step 2 – Loopback filesystem drill

        ```bash
        lsblk -f | tee lsblk.txt
        dd if=/dev/zero of=disk.img bs=1M count=64 status=none
        mkfs.ext4 -F disk.img
        mkdir -p mnt
        sudo mount -o loop disk.img mnt
        echo hello | sudo tee mnt/hello.txt
        findmnt mnt | tee mount.txt
        sudo umount mnt
        blkid disk.img | tee blkid.txt || true
        ```
        """
    ),
    13: dedent(
        """\
        ### Step 2 – LVM/swap/monitor snapshot

        ```bash
        {
          echo '=== LVM ==='
          sudo pvs 2>/dev/null || echo 'no PVs'
          sudo vgs 2>/dev/null || true
          sudo lvs 2>/dev/null || true
          echo '=== Swap ==='
          swapon --show || true
          free -h
          echo '=== Disk ==='
          df -h
        } | tee storage-health.txt
        ```
        """
    ),
    14: dedent(
        """\
        ### Step 2 – Network toolkit

        ```bash
        ip -br a | tee ip.txt
        ip route | tee route.txt
        ss -tulpn | head | tee ss.txt
        ping -c 2 1.1.1.1 | tee ping.txt || true
        dig +short example.com A | tee dig.txt || true
        curl -fsSI https://example.com | head | tee curl.txt || true
        nc -vz example.com 443 2>&1 | tee nc.txt || true
        ```
        """
    ),
    15: dedent(
        """\
        ### Step 2 – SSH client prep

        ```bash
        mkdir -p ~/.ssh
        chmod 700 ~/.ssh
        ssh-keygen -t ed25519 -a 64 -f ./id_ed25519_lab -N '' -C 'rebash-lab'
        cat > ssh_config.snippet << 'EOF'
        Host rebash-lab
          HostName 127.0.0.1
          User REPLACE_ME
          IdentityFile ~/.ssh/id_ed25519_lab
          IdentitiesOnly yes
        EOF
        ls -l id_ed25519_lab*
        ssh -G -F ssh_config.snippet rebash-lab | egrep 'user |hostname |identityfile ' | tee ssh-g.txt
        ```
        """
    ),
    16: dedent(
        """\
        ### Step 2 – Package manager detect

        ```bash
        {
          command -v apt && echo PM=apt
          command -v dnf && echo PM=dnf
          command -v yum && echo PM=yum
          command -v zypper && echo PM=zypper
          command -v snap && snap version | head -n 1
          command -v flatpak && flatpak --version
        } | tee pkg-tools.txt
        # Non-mutating query examples:
        (apt-cache policy bash 2>/dev/null || dnf info bash 2>/dev/null || true) | head | tee pkg-info.txt
        ```
        """
    ),
    17: dedent(
        """\
        ### Step 2 – Schedule safely

        ```bash
        crontab -l 2>/dev/null | tee crontab-before.txt || true
        echo "# lab only — remove after class" > cron.line
        echo "*/30 * * * * date >> $HOME/rebash-linux/lab17/cron-tick.log" >> cron.line
        cat cron.line
        systemctl list-timers --all 2>/dev/null | head | tee timers.txt || true
        command -v at && echo 'echo lab-at | at now + 1 minute' || echo 'at not installed'
        ```
        """
    ),
    18: dedent(
        """\
        ### Step 2 – Logging paths

        ```bash
        journalctl -b -n 10 --no-pager 2>/dev/null | tee journal.txt || true
        ls /var/log | head | tee var-log.txt
        sudo logrotate -d /etc/logrotate.conf 2>&1 | head -n 40 | tee logrotate-debug.txt || true
        cat > app.logrotate.example << 'EOF'
        /var/log/rebash-app/*.log {
          weekly
          rotate 4
          compress
          missingok
          notifempty
        }
        EOF
        ```
        """
    ),
    19: dedent(
        """\
        ### Step 2 – Host sample

        ```bash
        {
          uptime
          free -h
          df -h
          du -sh . 2>/dev/null
          vmstat 1 3
          command -v iostat && iostat -xz 1 2
          command -v sar && sar -u 1 2
        } | tee host-sample.txt
        ```
        """
    ),
    20: dedent(
        """\
        ### Step 2 – SSH and firewall audit

        ```bash
        {
          echo '=== sshd effective (safe reads) ==='
          sshd -T 2>/dev/null | egrep 'passwordauthentication|permitrootlogin|pubkeyauthentication' || true
          echo '=== firewall ==='
          command -v ufw && sudo ufw status verbose
          command -v firewall-cmd && sudo firewall-cmd --list-all
        } 2>&1 | tee harden-audit.txt || true
        cat > sshd-hardening.snippet << 'EOF'
        PasswordAuthentication no
        PermitRootLogin no
        PubkeyAuthentication yes
        EOF
        ```
        """
    ),
    21: dedent(
        """\
        ### Step 2 – MAC / PAM / audit probe

        ```bash
        {
          command -v getenforce && getenforce
          command -v aa-status && sudo aa-status 2>/dev/null | head
          command -v fail2ban-client && sudo fail2ban-client status 2>/dev/null
          ls /etc/pam.d | head
          head -n 20 /etc/pam.d/sshd 2>/dev/null || head -n 20 /etc/pam.d/login
        } 2>&1 | tee mac-pam.txt
        ```
        """
    ),
    22: dedent(
        """\
        ### Step 2 – Container internals

        ```bash
        {
          lsns | head
          cat /proc/self/cgroup
          echo '=== OCI / runtime ==='
          command -v docker && docker info 2>/dev/null | head -n 15
          command -v podman && podman info 2>/dev/null | head -n 10
          command -v crictl && crictl version 2>/dev/null
        } 2>&1 | tee container-internals.txt
        ```
        """
    ),
    23: dedent(
        """\
        ### Step 2 – Troubleshooting toolkit

        ```bash
        cat > toolkit.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        echo "== failed units =="; systemctl --failed --no-pager || true
        echo "== load/mem/disk =="; uptime; free -h; df -h
        echo "== top cpu =="; ps aux --sort=-%cpu | head -n 6
        echo "== journal err =="; journalctl -b -p err -n 15 --no-pager 2>/dev/null || true
        echo "== listeners =="; ss -tulpn | head
        EOF
        chmod +x toolkit.sh
        ./toolkit.sh | tee toolkit-out.txt
        ```
        """
    ),
    24: dedent(
        """\
        ### Step 2 – Production baseline

        ```bash
        cat > harden-checklist.md << 'EOF'
        - [ ] SSH keys only / PermitRootLogin no
        - [ ] Host firewall + cloud SG aligned
        - [ ] Automatic security updates policy
        - [ ] MAC enforcing where supported
        - [ ] Journal/syslog shipped
        - [ ] Disk/inode alerts
        - [ ] Documented reboot window
        EOF
        {
          uptime
          free -h
          df -h
          sysctl vm.swappiness net.ipv4.ip_forward 2>/dev/null || true
        } | tee baseline.txt
        ```
        """
    ),
    25: dedent(
        """\
        ### Step 2 – Backup and restore drill

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
        """
    ),
}


def related(num: int) -> str:
    links = ["- [Linux for Cloud & DevOps – Category Overview](index.md)"]
    if num > 1:
        prev = SPEC[num - 2]
        links.append(f"- [{prev[2]}]({prev[1]}.md) *(previous)*")
    if num < len(SPEC):
        nxt = SPEC[num]
        links.append(f"- [{nxt[2]}]({nxt[1]}.md) *(next)*")
    links.append("- [Learning Paths](../learning-paths/index.md)")
    return "\n".join(links)


def lab_block(num: int, slug: str, focus: str) -> str:
    """Build Hands-on Lab markdown without accidental leading indentation."""
    extra = LAB_EXTRA.get(num, "").rstrip()
    parts = [
        "Create a workspace for this tutorial.",
        "",
        "```bash",
        f"mkdir -p ~/rebash-linux/lab{num:02d} && cd ~/rebash-linux/lab{num:02d}",
        "```",
        "",
        f"**Focus:** {focus}",
        "",
        "### Step 1 – Skeleton",
        "",
        "```bash",
        "cat > lab.sh << 'EOF'",
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        f'echo "lab{num:02d} {slug} on $(hostname -s)"',
        "EOF",
        "chmod +x lab.sh",
        "./lab.sh",
        "```",
    ]
    if extra:
        parts.extend(["", extra])
    parts.extend(
        [
            "",
            "### Final step – Cleanup note",
            "",
            "```bash",
            "./lab.sh",
            "# keep ~/rebash-linux for later labs",
            "```",
        ]
    )
    return "\n".join(parts)


def render(sp: tuple) -> str:
    (
        num,
        slug,
        title,
        module,
        difficulty,
        minutes,
        diagram,
        tag_extra,
        desc,
        overview,
        theory,
        lab_focus,
    ) = sp
    tags = ["linux", *tag_extra]
    tag_yaml = "\n".join(f"  - {t}" for t in tags)
    prev_title = SPEC[num - 2][2] if num > 1 else "Basic computer literacy"
    prereq = [
        prev_title if num > 1 else "Basic computer knowledge; a Linux VM, WSL2, or cloud instance",
        "Terminal access with a regular user account (sudo where noted)",
    ]
    objectives = [
        f"Apply the core ideas of “{title}” on a real Linux host",
        "Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply",
        "Complete the lab under `~/rebash-linux/` with clear outputs",
        "Relate this topic to Cloud, DevOps, and production operations",
        "Explain the failure modes you would check first in an incident",
    ]
    obj = "\n".join(f"- [ ] {o}" for o in objectives)
    pr = "\n".join(f"- {p}" for p in prereq)
    pr_yaml = "\n".join(f"  - {p}" for p in prereq)

    return f"""---
title: "{title}"
description: "{desc}"
difficulty: {difficulty}
estimated_time: "{minutes}"
author: {AUTHOR}
last_updated: "{DATE}"
category: linux
tags:
{tag_yaml}
prerequisites:
{pr_yaml}
comments: false
---

# {title}

## Overview

{overview}

This is **Tutorial {num}** in **{module}** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

{pr}

## Learning Objectives

By the end of this tutorial, you will be able to:

{obj}

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for {title}](../assets/images/{diagram}.svg)

## Theory

{theory.strip()}

## Hands-on Lab

{lab_block(num, slug, lab_focus).rstrip()}

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab{num:02d}/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **{title}** always combines:

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

**{title}** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

## Interview Questions

1. How does this topic show up when operating Cloud VMs or Kubernetes nodes?
2. What would you check first if this area misbehaves in production?
3. Which modern Linux tools replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI or a cron/timer job?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, then gather host signals (`systemctl --failed`, `df`, `ip`/`ss`, `journalctl`) before making changes. Fix forward with evidence, not guesswork.

## Related Tutorials

{related(num)}

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
"""


def write_diagrams() -> tuple[int, int, list[str]]:
    """Write D2 sources and render SVGs when d2 is available."""
    D2_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    d2_count = 0
    svg_count = 0
    errors: list[str] = []
    d2_bin = shutil.which("d2")
    for name, source in DIAGRAMS.items():
        d2_path = D2_DIR / f"{name}.d2"
        d2_path.write_text(source.lstrip("\n"), encoding="utf-8")
        d2_count += 1
        print(f"wrote {d2_path.relative_to(ROOT)}")
        svg_path = IMG_DIR / f"{name}.svg"
        if not d2_bin:
            errors.append(f"d2 not found; skipped SVG for {name}")
            continue
        try:
            subprocess.run(
                [
                    d2_bin,
                    "--theme",
                    "3",
                    "--layout",
                    "dagre",
                    "--pad",
                    "48",
                    str(d2_path),
                    str(svg_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            svg_count += 1
            print(f"wrote {svg_path.relative_to(ROOT)}")
        except subprocess.CalledProcessError as exc:
            err = (exc.stderr or exc.stdout or str(exc)).strip()
            errors.append(f"d2 failed for {name}: {err}")
    return d2_count, svg_count, errors


def delete_obsolete() -> list[str]:
    keep = {f"{sp[1]}.md" for sp in SPEC} | {"index.md"}
    deleted: list[str] = []
    for name in OBSOLETE:
        if name in keep:
            continue
        path = OUT / name
        if path.exists():
            path.unlink()
            deleted.append(name)
            print(f"deleted {path.relative_to(ROOT)}")
    return deleted


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assert len(SPEC) == 25, len(SPEC)
    assert len(DIAGRAMS) == 25, len(DIAGRAMS)
    for sp in SPEC:
        diagram = sp[6]
        assert diagram in DIAGRAMS, diagram
        path = OUT / f"{sp[1]}.md"
        path.write_text(render(sp), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")
    print(f"done: {len(SPEC)} tutorials")
    d2_count, svg_count, errors = write_diagrams()
    print(f"diagrams: d2={d2_count} svg={svg_count}")
    deleted = delete_obsolete()
    print(f"deleted_obsolete: {len(deleted)}")
    for e in errors:
        print(f"ERROR: {e}")
    # Summary line for the operator
    print(
        f"SUMMARY md={len(SPEC)} d2={d2_count} svg={svg_count} "
        f"deleted={len(deleted)} errors={len(errors)}"
    )


if __name__ == "__main__":
    main()
