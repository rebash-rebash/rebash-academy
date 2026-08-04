---
title: "Linux Cheat Sheet"
description: "Production-focused Linux quick reference: commands, permissions, text processing, processes, storage, networking, SSH, systemd, packages, and troubleshooting."
difficulty: beginner
estimated_time: "15 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: cheatsheets
tags:
  - cheatsheets
  - linux
comments: false
---

# Linux Cheat Sheet

Scannable commands for the [Linux for Cloud & DevOps](../learning-paths/linux-administrator/) track. Prefer full tutorials when you need *why*, not only *how*.

## Commands

| Task | Commands |
|------|----------|
| Identity | `uname -a`; `hostnamectl`; `cat /etc/os-release`; `uptime` |
| Navigate | `pwd`; `ls -la`; `cd`; `cd -`; `tree -L 2` |
| Files | `cp -a`; `mv`; `rm -i`; `mkdir -p`; `touch`; `stat`; `file` |
| View | `cat`; `less`; `head -n`; `tail -f`; `wc -l` |
| Find | `find /path -name '*.log'`; `find /path -mtime -1`; `locate` (if indexed) |
| Archive | `tar -czf a.tgz dir`; `tar -xzf a.tgz`; `gzip -d` |
| Help | `man cmd`; `cmd --help`; `type cmd`; `command -v cmd` |

## Permissions

| Task | Commands / notes |
|------|------------------|
| Modes | `chmod 640 file`; `chmod u+x script`; `umask` |
| Ownership | `chown user:group file`; `chgrp group file` |
| Special bits | Sticky `chmod 1777 /tmp`-style; SUID/SGID on binaries/dirs (`chmod u+s` / `g+s` / `2770`) |
| Inspect | `ls -l`; `namei -l /path`; `id`; `groups` |
| ACLs | `getfacl path`; `setfacl -m u:alice:rwx path`; `setfacl -b path` |
| sudo | `sudo -l`; `sudo -u user cmd`; files under `/etc/sudoers.d` (`visudo -cf`) |

## Text processing

| Tool | Pattern |
|------|---------|
| grep | `grep -RIn 'ERROR' /var/log`; `grep -E 'pattern'`; `-v` invert |
| sed | `sed -n '1,20p'`; `sed 's/foo/bar/g'` |
| awk | `awk '{print $1}'`; `awk -F: '{print $1}' /etc/passwd` |
| cut/tr | `cut -d: -f1`; `tr '[:upper:]' '[:lower:]'` |
| sort/uniq | `sort \| uniq -c \| sort -nr` |
| xargs | `find . -name '*.tmp' -print0 \| xargs -0 rm -f` |

## Processes

| Task | Commands |
|------|----------|
| List | `ps aux`; `ps -ef`; `pgrep -a name` |
| Interactive | `top`; `htop` |
| Signals | `kill -TERM <pid>`; `kill -KILL <pid>`; `pkill -f pattern` |
| Priority | `nice -n 10 cmd`; `renice -n 5 -p <pid>` |
| Jobs | `jobs`; `bg`; `fg`; `nohup cmd &`; `disown` |
| Limits | `ulimit -a`; systemd `MemoryMax=` / `CPUQuota=` |

## Storage

| Task | Commands |
|------|----------|
| Inventory | `lsblk -f`; `blkid`; `findmnt` |
| Usage | `df -hT`; `df -i`; `du -sh *`; `du -x -d1 /` |
| Filesystems | `mkfs.ext4`; `mkfs.xfs`; `mount`; `umount` |
| Persist | UUID in `/etc/fstab`; `findmnt --verify` |
| LVM | `pvs`; `vgs`; `lvs`; `lvextend`; `resize2fs` / `xfs_growfs` |
| Swap | `swapon --show`; `free -h` |

## Networking

| Task | Commands |
|------|----------|
| Addresses | `ip -br a`; `ip route`; `ip neigh` |
| Sockets | `ss -tulpn`; `ss -tp` |
| Path | `ping -c 3 host`; `traceroute host`; `tracepath` |
| DNS | `dig +short name`; `resolvectl query name`; `getent hosts` |
| HTTP | `curl -vI https://example`; `wget` |
| Capture | `tcpdump -i any port 443`; `nc` / `ncat` |

## SSH

| Task | Commands / settings |
|------|---------------------|
| Keys | `ssh-keygen -t ed25519`; `ssh-copy-id -i key.pub user@host` |
| Connect | `ssh -i key user@host`; `scp`; `sftp` |
| Config | `~/.ssh/config` `Host` stanzas; `IdentitiesOnly yes` |
| Server | `sshd -t`; `sshd -T`; drop-ins in `/etc/ssh/sshd_config.d/` |
| Hardening | `PasswordAuthentication no`; `PermitRootLogin no`; keep console/out-of-band |

## Systemd

| Task | Commands |
|------|----------|
| Units | `systemctl status name`; `start`/`stop`/`restart`/`reload` |
| Boot | `systemctl enable --now name`; `is-enabled`; `list-unit-files` |
| Failures | `systemctl --failed`; `systemctl reset-failed` |
| Journal | `journalctl -u name -f`; `--since today`; `-p err`; `-o short-iso` |
| Timers | `systemctl list-timers`; `systemctl status name.timer` |
| Analyse | `systemd-analyze blame`; `systemd-analyze critical-chain` |

## Package managers

| Family | Update / install / query |
|--------|---------------------------|
| Debian/Ubuntu | `apt update`; `apt install pkg`; `apt remove`; `dpkg -l`; `apt-cache policy` |
| RHEL/Fedora | `dnf install pkg`; `dnf upgrade`; `rpm -qa`; `dnf info` |
| SUSE | `zypper refresh`; `zypper install` |
| Universal | `snap`; `flatpak` (use sparingly on servers; prefer distro packages) |

## Troubleshooting

| Symptom | First commands |
|---------|----------------|
| Service down | `systemctl status`; `journalctl -u` `--since` |
| High CPU | `uptime`; `ps --sort=-pcpu`; `top`; `vmstat 1` |
| Memory pressure | `free -h`; `ps --sort=-pmem`; check OOM in `journalctl -k` |
| Disk full | `df -h`; `df -i`; `du -x -d1`; clear safe logs/caches |
| Network | `ip r`; `ss -tulpn`; `ping`; `dig`; cloud SG/NSG |
| Slow disk | `iostat -xz 1`; `dmesg -T \| tail` |
| Permissions | `namei -l`; `id`; `getfacl`; compare to expected owner/mode |
| Boot | `journalctl -b`; `systemd-analyze`; rescue/single-user carefully |

## Common mistakes

- Mounting by `/dev/sdX` in fstab instead of UUID
- Enabling UFW before allowing SSH
- `chmod 777` to “fix” shared directories
- Restarting units without reading the journal

## Related

- Track: [Linux](../linux/index.md)
- Path: [Linux for Cloud & DevOps](../learning-paths/linux-administrator/)
- Interview: [Linux interview prep](../interview/linux.md)
- Quiz: [Linux for Cloud & DevOps Fundamentals](../quizzes/linux-for-cloud-devops-fundamentals.md)
- Labs: [Labs index](../labs/index.md)
