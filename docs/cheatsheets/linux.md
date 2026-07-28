---
title: "Linux Cheat Sheet"
description: "Quick-reference commands and patterns for the REBASH Academy Linux track."
difficulty: beginner
estimated_time: "10 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: cheatsheets
tags:
  - cheatsheets
  - linux
comments: false
---

# Linux Cheat Sheet

Scannable commands and patterns for the [Linux track](../linux/index.md). Prefer the full tutorials when you need *why*, not only *how*.

## Quick reference

| Area | Commands / notes |
|------|------------------|
| System identity | `uname -a`; `hostnamectl`; `cat /etc/os-release` |
| Navigate | `pwd`; `ls -la`; `cd`; `cd -`; `tree -L 2` |
| Files | `cp -a`; `mv`; `rm -i`; `mkdir -p`; `find . -name '*.log'` |
| Permissions | `chmod 640`; `chown user:group`; `umask`; `id` |
| Processes | `ps aux`; `top`/`htop`; `kill -TERM <pid>`; `systemctl status` |
| Packages | `apt update && apt install`; `dnf install`; `dpkg -l` / `rpm -qa` |
| Logs | `journalctl -u service -f`; `journalctl --since today` |
| Disk | `df -h`; `du -sh *`; `lsblk`; `mount` |
| Network | `ip a`; `ss -tulpn`; `curl -v`; `dig` |
| Archive | `tar -czf a.tgz dir`; `tar -xzf a.tgz`; `gzip -d` |
| nginx | `nginx -t`; `systemctl reload nginx`; sites-available/enabled |
| TLS lab | `openssl x509 -noout -dates -in cert`; `curl -k https://127.0.0.1/` |
| LVM | `pvs`; `vgs`; `lvs`; `lvextend`; `resize2fs` |
| Backup | `tar -czf`; `sha256sum -c`; `rsync -a` |

## Common mistakes

- Copy-pasting without reading expected output
- Skipping cleanup (leftover containers, state, or temp files)
- Mixing production credentials into lab shells

## Related

- Track: [Linux](../linux/index.md)
- Start: [Linux introduction](../linux/introduction-to-linux.md)
- Interview bank: [Linux interview prep](../interview/linux.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)
