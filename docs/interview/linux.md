---
title: "Linux Interview Prep"
description: "28 interview questions with tips covering Linux fundamentals, administration, troubleshooting, performance, networking, security, and production scenarios."
difficulty: intermediate
estimated_time: "45–60 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: interview
tags:
  - interview
  - linux
comments: false
---

# Linux Interview Prep

Use this bank after the [Linux for Cloud & DevOps](../learning-paths/linux-for-cloud-devops.md) tutorials and labs. Answer out loud in two minutes, then name the first three debug commands.

!!! tip "How to practise"
    1. Answer without notes  
    2. Draw the diagram (boot, permissions, networking)  
    3. State the failure mode and verification  
    4. Tie the answer to least privilege and blast radius  

## Fundamentals

### 1. Kernel vs distribution — what is the difference?

**Tip:** Kernel = OS core; distribution = kernel + userland + packages + policies (Ubuntu, RHEL, etc.).

### 2. What happens from power-on to a login prompt?

**Tip:** Firmware → bootloader → kernel + initramfs → systemd (PID 1) → targets → getty/SSH.

### 3. Explain the Filesystem Hierarchy Standard (FHS) paths you use daily.

**Tip:** `/etc` config, `/var` variable data/logs, `/home` users, `/usr` programs, `/opt` optional add-ons, `/proc`/`/sys` kernel interfaces.

### 4. Absolute vs relative paths; hard link vs symbolic link?

**Tip:** Hard links share inode (same filesystem); symlinks are path pointers and can cross filesystems.

### 5. What is an inode and why do disks “fill” with free space still showing?

**Tip:** inode exhaustion (`df -i`) vs block exhaustion (`df -h`).

## Administration

### 6. How do you create a service account safely?

**Tip:** System user, nologin shell, dedicated group, least-privilege home/data dirs.

### 7. Explain `chmod 640` and when you would use `2770` on a directory.

**Tip:** Owner rw, group r, others none; `2770` = SGID + group collaboration.

### 8. How do ACLs differ from classic mode bits?

**Tip:** Extra per-user/per-group entries via `setfacl`; still combine with ownership model.

### 9. How do you grant limited sudo?

**Tip:** `/etc/sudoers.d` snippets, `visudo -cf`, command scoping, avoid `NOPASSWD: ALL`.

### 10. apt vs dnf — what do you check before installing on a server?

**Tip:** Update indexes, pinned versions, needrestart/reboot hints, change control.

### 11. How do you schedule a job — cron vs systemd timer?

**Tip:** cron for simple user jobs; timers for dependency-aware, missed-run (`Persistent=`), and journal integration.

## Troubleshooting

### 12. A systemd unit is failed — what is your first five minutes?

**Tip:** `systemctl status`, `journalctl -u --since`, config path/permissions, fix, `daemon-reload`, verify.

### 13. Users report “permission denied” on a shared directory — how do you diagnose?

**Tip:** `namei -l`, ownership, mode, ACL, mount options (`nosuid`/`ro`), LSM (SELinux/AppArmor).

### 14. Disk full — ordered response?

**Tip:** `df -h`/`df -i`, find large dirs (`du`), safe deletion targets, journal vacuum, prevent recurrence.

### 15. Host cannot resolve DNS — what do you check?

**Tip:** `resolvectl`/`/etc/resolv.conf`, `dig`, network routes, cloud DNS settings, split horizon.

### 16. How do you investigate a suspect process?

**Tip:** `ps`, `/proc/<pid>`, open files (`lsof`/`ss`), parent PID, package ownership, recent deploys.

## Performance

### 17. Load average is high — is the host necessarily CPU-bound?

**Tip:** Load includes uninterruptible wait; check `vmstat` (`wa`), `iostat`, CPU idle%.

### 18. Which signals do `vmstat` columns give you?

**Tip:** procs (r/b), memory, swap, io, system, cpu (us/sy/id/wa/st).

### 19. How do you find top memory consumers quickly?

**Tip:** `ps --sort=-pmem`, `free -h`, watch for caches vs anonymous; OOM in `dmesg`/`journalctl -k`.

### 20. Disk latency vs throughput — what tools?

**Tip:** `iostat -xz`, application metrics, filesystem type, noisy neighbours on shared storage.

## Networking

### 21. `ping` works but the application fails — what next?

**Tip:** Port/`ss`, security groups + host firewall, TLS, app bind address (`127.0.0.1` vs `0.0.0.0`).

### 22. How do you list listening sockets and owning processes?

**Tip:** `ss -tulpn` (privileges may be required for process names).

### 23. Explain a minimal SSH hardening baseline.

**Tip:** Keys only, no root login, `sshd -t`, second session, optional allowlists, keep console.

## Security

### 24. UFW vs cloud security groups — how do they interact?

**Tip:** Defence in depth; both must allow traffic; document every public port.

### 25. SELinux/AppArmor — what do you do when a service is denied?

**Tip:** Read audit/journal denials; fix labels/profiles properly; avoid permanent `permissive`/`complain` without ticket.

### 26. What is Fail2Ban’s role vs a firewall allowlist?

**Tip:** Reactive ban on abuse patterns; allowlists reduce exposure a priori.

## Production scenarios

### 27. Walk through bringing a new Ubuntu VM to a production-ready baseline.

**Tip:** Identity, patches, users/SSH, firewall, time sync, monitoring agent, backup, documented golden image/cloud-init.

### 28. Pager: API down on a single VM — your incident narrative?

**Tip:** Impact → host health → unit/journal → recent changes → fix/rollback → verify → RCA note. Use [Incident Triage lab](../labs/linux-production-incident-triage.md) as your story.

### 29. How do you prove a backup works?

**Tip:** Scheduled job + checksum + restore drill to a separate path; measure RTO/RPO assumptions.

### 30. Containers on Linux — what kernel features matter?

**Tip:** namespaces, cgroups, OverlayFS, OCI runtimes; host hardening still applies to nodes.

## Hands-on prompts interviewers love

- Live-fix a failed unit from journal evidence only  
- Draw permission bits for a shared log directory  
- Explain UUID fstab vs device names  
- Compare cron and systemd timers for a health script  

## Related

- Track: [Linux](../linux/index.md)
- Path: [Linux for Cloud & DevOps](../learning-paths/linux-for-cloud-devops.md)
- Cheat sheet: [Linux](../cheatsheets/linux.md)
- Quiz: [Linux for Cloud & DevOps Fundamentals](../quizzes/linux-for-cloud-devops-fundamentals.md)
- Labs: [Labs index](../labs/index.md)
- Projects: [Operations Platform](../projects/linux-production-operations-platform.md)
