---
title: "SSH Hardening and Firewalls"
description: "Harden SSH with keys and sshd_config, and control exposure with firewalld or ufw."
difficulty: advanced
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - ssh
  - firewalld
  - ufw
  - hardening
prerequisites:
  - Host Monitoring with vmstat, iostat, and sar
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# SSH Hardening and Firewalls

## Overview

Most internet-facing Linux breaches start with weak SSH or open management ports.

This is **Tutorial 20** in **Module 13: Linux Security** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- Host Monitoring with vmstat, iostat, and sar
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “SSH Hardening and Firewalls” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for SSH Hardening and Firewalls](../assets/images/linux-ssh-hardening.svg)

## Theory

### SSH keys and hardening

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

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab20 && cd ~/rebash-linux/lab20
```

**Focus:** audit sshd settings; review ufw/firewalld; draft hardened snippets

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab20 ssh-hardening-and-firewalls on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

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

### Final step – Cleanup note

```bash
./lab.sh
# keep ~/rebash-linux for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab20/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **SSH Hardening and Firewalls** always combines:

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

**SSH Hardening and Firewalls** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

## Interview Questions

1. How does this topic show up when operating Cloud VMs or Kubernetes nodes?
2. What would you check first if this area misbehaves in production?
3. Which modern Linux tools replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI or a cron/timer job?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, then gather host signals (`systemctl --failed`, `df`, `ip`/`ss`, `journalctl`) before making changes. Fix forward with evidence, not guesswork.

## Related Tutorials

- [Linux for Cloud & DevOps – Category Overview](index.md)
- [Host Monitoring with vmstat, iostat, and sar](host-monitoring-vmstat-iostat-sar.md) *(previous)*
- [SELinux, AppArmor, Fail2Ban, Auditd, and PAM](selinux-apparmor-fail2ban-auditd-pam.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
