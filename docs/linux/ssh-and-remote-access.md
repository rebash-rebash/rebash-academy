---
title: "SSH and Remote Access"
description: "Use SSH for remote administration — config, keys basics, tunnels, and scp/rsync — before hardening deep-dives."
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - ssh
  - remote
  - keys
prerequisites:
  - Linux Networking Tools
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# SSH and Remote Access

## Overview

SSH is how you reach Cloud VMs. Master access fundamentals here; Module 13 covers hardening.

This is **Tutorial 15** in **Module 9: Linux Networking** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- Linux Networking Tools
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “SSH and Remote Access” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for SSH and Remote Access](../assets/excalidraw/linux-ssh-access.svg)

## Theory

### What it is

**Secure Shell (SSH)** is the standard encrypted remote login and command channel for Linux servers. Clients authenticate with keys (preferred) or passwords; the server process `sshd` enforces configuration from `/etc/ssh/sshd_config`. Day-to-day ops also use SSH for file copy (`scp`, `rsync` over SSH) and local port forwarding to reach private services through a bastion.

### Why it matters

Almost every cloud VM, bastion, and jump host interaction starts with SSH. Weak key hygiene, agent forwarding to untrusted hosts, or ad-hoc `StrictHostKeyChecking=no` habits create lasting security debt. Fluent client configuration (`~/.ssh/config`) reduces errors under pressure and makes automation (`ssh host 'cmd'`) reliable for deploys and incident checks.

### How it works

`ssh user@host` opens a session; `-i` selects an identity file. Generate keys with `ssh-keygen` (Ed25519 is a strong default), install the public key in `~/.ssh/authorized_keys` on the server (`ssh-copy-id` helps). Client `Host` stanzas set hostname aliases, users, and keys. Host key verification protects against impersonation — accept new keys deliberately. `scp`/`rsync -avz` copy files; `ssh -L local:host:port` forwards a local port through the tunnel. Remote one-liners (`ssh host 'hostname; uptime'`) are the basis of many orchestration wrappers. Hardening (disable passwords, restrict users) is covered later; here the goal is correct, key-based access.

### Key concepts and comparisons

| Method | Use |
|--------|-----|
| Password auth | Avoid on internet-facing hosts |
| Public-key auth | Default for production |
| Certificate auth | Short-lived access at scale (advanced) |

| Tool | Role |
|------|------|
| `ssh` | Interactive / remote command |
| `scp` | Simple file copy |
| `rsync` over SSH | Efficient sync and resumes |
| Local forward `-L` | Reach private HTTP/admin ports |

### Common pitfalls

- Disabling host key checks globally “to make CI pass”.
- Forwarding the agent to hosts you do not fully trust.
- Leaving private keys world-readable or checking them into git.
- Confusing bastion access with direct VPC connectivity — routes still matter after login.
- Editing `sshd_config` and reloading without keeping a second session open.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab15 && cd ~/rebash-linux/lab15
```

**Focus:** generate lab keypair; write SSH config Host entry; test remote command

### Step 1 – SSH client prep

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

### Final step – Cleanup note

```bash
# Keep ~/rebash-linux/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab15/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **SSH and Remote Access** always combines:

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

**SSH and Remote Access** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

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
- [Linux Networking Tools](linux-networking-tools.md) *(previous)*
- [Package Management](package-management.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
