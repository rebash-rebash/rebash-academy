---
title: "Containers — Namespaces, cgroups, OverlayFS, and OCI"
description: "Understand Linux container building blocks — namespaces, cgroups, OverlayFS, OCI, and runtime basics."
difficulty: advanced
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - namespaces
  - cgroups
  - overlayfs
  - oci
prerequisites:
  - SELinux, AppArmor, Fail2Ban, Auditd, and PAM
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# Containers — Namespaces, cgroups, OverlayFS, and OCI

## Overview

Kubernetes nodes are Linux. Container isolation is kernel features, not magic.

This is **Tutorial 22** in **Module 14: Containers & Cloud** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- SELinux, AppArmor, Fail2Ban, Auditd, and PAM
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Containers — Namespaces, cgroups, OverlayFS, and OCI” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for Containers — Namespaces, cgroups, OverlayFS, and OCI](../assets/images/linux-container-internals.svg)

## Theory

### Namespaces

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

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab22 && cd ~/rebash-linux/lab22
```

**Focus:** explore lsns/cgroups; sketch OCI stack; inspect a running container if available

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab22 containers-namespaces-cgroups-and-oci on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

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

### Final step – Cleanup note

```bash
./lab.sh
# keep ~/rebash-linux for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab22/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **Containers — Namespaces, cgroups, OverlayFS, and OCI** always combines:

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

**Containers — Namespaces, cgroups, OverlayFS, and OCI** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

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
- [SELinux, AppArmor, Fail2Ban, Auditd, and PAM](selinux-apparmor-fail2ban-auditd-pam.md) *(previous)*
- [Troubleshooting Linux Systems](troubleshooting-linux-systems.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
