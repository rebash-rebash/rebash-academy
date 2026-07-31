---
title: "SELinux, AppArmor, Fail2Ban, Auditd, and PAM"
description: "Apply Mandatory Access Control, intrusion prevention, audit trails, and PAM authentication stacks."
difficulty: advanced
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - selinux
  - apparmor
  - fail2ban
  - auditd
  - pam
prerequisites:
  - SSH Hardening and Firewalls
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# SELinux, AppArmor, Fail2Ban, Auditd, and PAM

## Overview

Permissions are DAC; production hosts also need MAC, auditing, and sane authentication policy.

This is **Tutorial 21** in **Module 13: Linux Security** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- SSH Hardening and Firewalls
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “SELinux, AppArmor, Fail2Ban, Auditd, and PAM” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for SELinux, AppArmor, Fail2Ban, Auditd, and PAM](../assets/excalidraw/linux-security-layers.svg)

## Theory

### What it is

This tutorial covers complementary host security controls. **SELinux** (common on RHEL-family) and **AppArmor** (common on Ubuntu/SUSE) are Mandatory Access Control (MAC) systems that confine processes beyond Discretionary Access Control (DAC) permissions. **Fail2Ban** bans addresses after repeated authentication failures. **auditd** records security-relevant events for compliance. **Pluggable Authentication Modules (PAM)** stacks define how login, sudo, and SSH authentication behave.

### Why it matters

MAC denials often look like mysterious permission errors after a correct `chmod`. Disabling SELinux to “make it work” removes a major control — fix labels instead. Failed SSH brute force without Fail2Ban or equivalent wastes resources and risks success. Broken PAM can lock out every user. Audit trails matter for regulated environments and for proving what changed during an incident.

### How it works

SELinux modes: Enforcing, Permissive, Disabled (`getenforce`). File labels appear in `ls -Z`; restore with `restorecon`. AppArmor profiles confine programmes (`aa-status`); complain mode aids tuning before enforce. Fail2Ban watches logs and updates firewall rules for jails such as `sshd`. auditd rules (`auditctl`) and searches (`ausearch`) retrieve events like `USER_LOGIN`. PAM files under `/etc/pam.d/` chain modules for account, auth, password, and session — edit carefully with a root break-glass session available. These tools layer: PAM authenticates, MAC confines, audit records, Fail2Ban reacts to abuse.

### Key concepts and comparisons

| Control | Primary job |
|---------|-------------|
| SELinux / AppArmor | Confine processes (MAC) |
| DAC (chmod/ACL) | Owner-managed access |
| Fail2Ban | Reactive IP bans on abuse |
| auditd | Compliance / forensic trail |
| PAM | Auth stack behaviour |

| Distro tendency | MAC |
|-----------------|-----|
| RHEL, Rocky, Alma | SELinux |
| Ubuntu | AppArmor |
| Many containers | Often unconfined unless configured |

### Common pitfalls

- Setting SELinux to Disabled permanently instead of fixing contexts.
- Misreading DAC success as “not SELinux” when AVC denials are in the audit log.
- Editing PAM and testing only after all sessions disconnect.
- Fail2Ban jails that never match your log path or journal config.
- Assuming MAC in the guest equals isolation for containers — runtime config matters.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab21 && cd ~/rebash-linux/lab21
```

**Focus:** check MAC status; inspect pam.d/sshd; review fail2ban/audit if present

### Step 1 – MAC / PAM / audit probe

```bash
{
  command -v getenforce && getenforce
  command -v aa-status && sudo aa-status 2>/dev/null | head
  command -v fail2ban-client && sudo fail2ban-client status 2>/dev/null
  ls /etc/pam.d | head
  head -n 20 /etc/pam.d/sshd 2>/dev/null || head -n 20 /etc/pam.d/login
} 2>&1 | tee mac-pam.txt
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-linux/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab21/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **SELinux, AppArmor, Fail2Ban, Auditd, and PAM** always combines:

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

**SELinux, AppArmor, Fail2Ban, Auditd, and PAM** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

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
- [SSH Hardening and Firewalls](ssh-hardening-and-firewalls.md) *(previous)*
- [Containers — Namespaces, cgroups, OverlayFS, and OCI](containers-namespaces-cgroups-and-oci.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
