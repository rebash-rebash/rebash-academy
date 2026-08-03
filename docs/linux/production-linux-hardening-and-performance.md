---
title: "Production Hardening and Performance"
description: "Apply practical Linux hardening and performance baselines — sysctl, resource limits, time sync, and audit checks — on a practice Ubuntu VM."
difficulty: advanced
estimated_time: "55–65 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 16 · Production Linux"
tags:
  - linux
  - hardening
  - performance
  - sysctl
  - production
prerequisites:
  - linux/troubleshooting-linux-systems
next:
  - linux/backup-disaster-recovery-and-capacity
related:
  - linux/ssh-hardening-and-firewalls
  - linux/host-monitoring-vmstat-iostat-sar
interview: interview/linux
comments: false
---

# Production Hardening and Performance

## Overview

Production Linux hosts need two habits at once: **hardening** (reduce attack surface and limit blast radius) and **performance baselines** (know normal CPU, memory, disk, and network behaviour). Hardening without observability creates brittle hosts. Performance tuning without security creates fast vulnerable hosts.

Practical baselines include: time sync (chrony), kernel parameters via **sysctl**, user/process **resource limits**, unattended security updates policy, and regular audit of listening ports and failed units. In this tutorial you will inspect current baselines, apply a **lab-scoped** sysctl drop-in and limits drop-in, verify them, and save proof under `~/rebash-linux/lab24`. Changes stay namespaced to REBASH lab files so Cleanup is safe.

In real estates, prefer golden images and configuration management over one-off SSH edits. Test sysctl changes on practice VMs — some settings can break apps if copied blindly from blog posts.

This is **Tutorial 24** in **Module 16: Production Linux** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers.

## Prerequisites

- [Troubleshooting Linux Systems](troubleshooting-linux-systems.md)
- A **practice Ubuntu 22.04/24.04 VM** with `sudo`
- Do **not** apply experimental kernel tuning on shared production without change control

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain a minimal production baseline (time, updates, limits, sysctl, audit)
- [ ] Add a sysctl drop-in and prove it with `sysctl`
- [ ] Add a limits drop-in and prove the configured values
- [ ] Capture listening ports and failed units as an audit snapshot
- [ ] Pack evidence under `~/rebash-linux/lab24`

## Architecture

Hardening and performance controls sit across identity, network exposure, kernel parameters, resource limits, and monitoring feedback loops.

![Architecture diagram for Production Hardening and Performance](../assets/excalidraw/linux-production.svg)

## Theory

### What it is

| Area | Examples |
|------|----------|
| Identity & access | sudo least privilege, SSH keys |
| Network exposure | firewall, few listen ports |
| Kernel/OS | sysctl, chrony, automatic security updates |
| Resources | ulimits, cgroup limits on services |
| Feedback | metrics, logs, failed-unit alerts |

```bash
timedatectl
sysctl net.ipv4.ip_forward
ss -lntu
systemctl --failed
```

### Why it matters

Open SSH with password auth, no time sync, and unlimited processes are common root causes of incidents and audit failures. Performance regressions often start as “we never recorded a baseline”.

### How it works

1. Measure current state  
2. Apply small, named drop-in files  
3. Verify with read-back commands  
4. Monitor impact  
5. Codify in images/config management  

| Knob | Careful note |
|------|----------------|
| `fs.file-max` / nofile limits | Apps may need higher file descriptors |
| `vm.swappiness` | Workload-dependent |
| IP forwarding | Only when the host is a router |
| Automatic reboots | Coordinate maintenance windows |

### Common pitfalls

- Copy-pasting huge sysctl “performance” lists without testing.  
- Raising limits globally instead of per-service.  
- Disabling swap or firewalls “for speed”.  
- No chrony — TLS and logs become confusing.

## Hands-on Lab

### Objective

Capture a production-style audit snapshot, install lab sysctl and limits drop-ins, verify read-back, and save evidence under `~/rebash-linux/lab24`.

### Prerequisites

- Ubuntu practice VM with `sudo`

### Lab environment

Workspace: `~/rebash-linux/lab24`

```bash title="Terminal"
mkdir -p ~/rebash-linux/lab24 && cd ~/rebash-linux/lab24
set -euo pipefail
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y chrony
timedatectl | tee timedatectl.txt
```

!!! example "Expected output"
    chrony present; `timedatectl.txt` shows clock sync fields.


### Real-world scenario

Security and platform teams ask for a baseline on a new Ubuntu app VM: time sync on, a documented sysctl drop-in, higher file descriptor limits for the app user group, and a snapshot of listening ports. You implement lab-scoped files and keep proof for the hardening ticket.

### Step-by-step tasks

#### Task 1 – Audit snapshot

```bash title="Terminal"
cd ~/rebash-linux/lab24
set -euo pipefail

uname -a | tee uname.txt
cat /etc/os-release | tee os-release.txt
timedatectl show | tee timedatectl-show.txt
sysctl fs.file-max net.ipv4.ip_forward vm.swappiness | tee sysctl-before.txt
ulimit -n | tee ulimit-n-before.txt
ss -lntu | tee ss-listen.txt
systemctl --failed --no-pager | tee failed-units.txt || true
df -hT | tee df.txt
free -h | tee free.txt
```

!!! example "Expected output"
    audit files exist; sysctl values captured before change.


#### Task 2 – Lab sysctl drop-in

```bash title="Terminal"
cd ~/rebash-linux/lab24
set -euo pipefail

# Conservative lab-only example: raise file-max modestly and keep ip_forward=0
AFTER_MAX=$(( $(sysctl -n fs.file-max) + 1000 ))
echo "$AFTER_MAX" | tee target-file-max.txt

sudo tee /etc/sysctl.d/99-rebash-lab24.conf >/dev/null << EOF
# REBASH lab24 — remove in cleanup
fs.file-max = ${AFTER_MAX}
net.ipv4.ip_forward = 0
EOF

sudo sysctl --system 2>&1 | tee sysctl-apply.txt
sysctl fs.file-max net.ipv4.ip_forward | tee sysctl-after.txt
test "$(sysctl -n fs.file-max)" -eq "$AFTER_MAX"
test "$(sysctl -n net.ipv4.ip_forward)" -eq 0
```

!!! example "Expected output"
    `sysctl-after.txt` shows the new `fs.file-max` and `ip_forward = 0`.


#### Task 3 – Limits drop-in + evidence pack

```bash title="Terminal"
cd ~/rebash-linux/lab24
set -euo pipefail

sudo tee /etc/security/limits.d/99-rebash-lab24.conf >/dev/null << 'EOF'
# REBASH lab24 — remove in cleanup
* soft nofile 4096
* hard nofile 8192
EOF

# limits.d applies to new login sessions; prove the file content and pam path exist
cat /etc/security/limits.d/99-rebash-lab24.conf | tee limits-file.txt
grep -n 'pam_limits.so' /etc/pam.d/common-session | tee pam-limits.txt || \
  grep -rn 'pam_limits.so' /etc/pam.d | head | tee pam-limits.txt

# Performance-oriented snapshot after changes
vmstat 1 3 | tee vmstat.txt
iostat -xz 1 2 2>/dev/null | tee iostat.txt || echo 'install sysstat for iostat' | tee iostat.txt

tar -czf production-evidence.tgz \
  timedatectl.txt timedatectl-show.txt uname.txt os-release.txt \
  sysctl-before.txt sysctl-after.txt sysctl-apply.txt target-file-max.txt \
  ulimit-n-before.txt limits-file.txt pam-limits.txt \
  ss-listen.txt failed-units.txt df.txt free.txt vmstat.txt iostat.txt
ls -l production-evidence.tgz | tee evidence-ls.txt
```

!!! example "Expected output"
    limits file installed; pam_limits referenced; evidence archive exists.


### Validation steps

- [ ] Time sync status captured with `timedatectl`
- [ ] `/etc/sysctl.d/99-rebash-lab24.conf` applied and verified
- [ ] `/etc/security/limits.d/99-rebash-lab24.conf` exists
- [ ] `production-evidence.tgz` exists under `~/rebash-linux/lab24`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| sysctl did not change | Typo / not loaded | `sysctl --system`; check file under `/etc/sysctl.d/` |
| `ulimit -n` unchanged in current shell | limits apply on new sessions | Open a new login SSH session to see new soft limit |
| chrony not syncing | Network/NTP blocked | Check security groups; `chronyc tracking` |
| `iostat` missing | sysstat not installed | Optional install; not required for pass |

### Challenge exercise

Create a systemd **service drop-in** directory for an existing unit you are allowed to edit in the lab (or a lab unit you create) that sets `LimitNOFILE=8192`, then show `systemctl show -p LimitNOFILE …` in `service-limit.txt`. Remove it in Cleanup.

### Learning outcomes

- Captured a host hardening/performance audit snapshot
- Applied and verified a sysctl drop-in
- Added limits.d configuration with proof files
- Packed production baseline evidence

### Cleanup

```bash title="Terminal"
cd ~/rebash-linux/lab24
set -euo pipefail
sudo rm -f /etc/sysctl.d/99-rebash-lab24.conf
sudo rm -f /etc/security/limits.d/99-rebash-lab24.conf
sudo sysctl --system >/dev/null
# Keep production-evidence.tgz if you want it
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab24/` with evidence files
- [ ] You can explain why drop-in files beat editing primary configs blindly
- [ ] You know limits often need a new login session
- [ ] You treat sysctl changes as change-controlled production work

## Code Walkthrough

Production rollout pattern:

1. Audit current host  
2. Propose small drop-ins in git  
3. Test on a twin VM  
4. Apply via config management  
5. Watch metrics and failed units  

## Security Considerations

- Least privilege sudo and key-only SSH on internet-facing hosts  
- Minimise listening ports; firewall default deny inbound  
- Keep automatic security updates or a patch pipeline  
- Do not disable security modules “for performance” without review  
- Protect sysctl/limits change rights  

## Common Mistakes

!!! warning "Huge blog sysctl packs on day one"
    Untested settings break apps. **Fix:** change one parameter, measure, then keep.

!!! warning "Global ulimit raises for everyone"
    Masks leaks and surprises other users. **Fix:** prefer systemd `LimitNOFILE` on the app unit.

!!! warning "No time synchronisation"
    Certificates and log correlation fail. **Fix:** install/enable chrony; monitor sync.

!!! warning "Calling a host “hardened” after one sysctl"
    Hardening is layered. **Fix:** cover SSH, patches, users, firewall, audit, backups.

## Best Practices

- Golden images + config as code  
- Baselines and alerts for saturation  
- Document every non-default sysctl  
- Separate OS and data disks  
- Regular restore and failover tests (next tutorial)  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| App “too many open files” | nofile too low | Raise unit LimitNOFILE; verify |
| Sysctl reverts after reboot | File not in sysctl.d | Place under `/etc/sysctl.d/` |
| Clock offset | chrony/NTP blocked | Fix network; restart chrony |
| Performance worse after tune | Bad parameter | Roll back drop-in; retest |
| Audit fails on open ports | Unexpected listeners | `ss -lntup`; remove/stop service |

## Summary

Production hosts need layered hardening and honest performance baselines. Use small drop-in files, verify read-back, and codify what works. Next: [Backup, Disaster Recovery, and Capacity](backup-disaster-recovery-and-capacity.md).

## Interview Questions

**1. What belongs in a minimal Linux production baseline?**

??? success "Reveal answer"
    Patch process, time sync, least-privilege access, firewall/SSH hardening, logging/metrics, resource limits for apps, backups/restore tests, and documented kernel/sysctl exceptions. Exact tools vary; the categories should not.

**2. Why prefer `/etc/sysctl.d/` drop-ins over editing `/etc/sysctl.conf` only?**

??? success "Reveal answer"
    Drop-ins are easier to own per team/role, review in git, and remove cleanly. They reduce merge conflicts and make intent obvious (`99-app.conf` vs a giant shared file).

**3. A process still sees the old `ulimit -n` after you edited limits.d. Why?**

??? success "Reveal answer"
    **limits.d** values apply to **new** login sessions (via PAM). Existing shells keep old limits. Systemd services should set `LimitNOFILE=` on the unit for reliable service limits.

**4. How do hardening and performance conflict, and how do you balance them?**

??? success "Reveal answer"
    Example: verbose audit logging adds I/O; very low timeouts can break slow clients. Balance with measured SLOs: keep security defaults, raise specific limits for known apps, and watch metrics after each change.

**5. What sysctl change is dangerous to copy from the internet without context?**

??? success "Reveal answer"
    Anything affecting networking (forwarding, rp_filter, connection tracking) or virtual memory behaviour can break routing or latency. Always test on a practice VM and know the rollback file.

**6. How would you prove a hardening change in a ticket?**

??? success "Reveal answer"
    Show the drop-in contents, `sysctl`/`systemctl show` read-back, listening port snapshot, and that critical services still pass health checks. Before/after matters.

**7. Where does SSH hardening fit relative to this tutorial?**

??? success "Reveal answer"
    SSH and firewalls are a major hardening slice covered in dedicated modules. This tutorial focuses on host baselines (time, sysctl, limits, audit snapshots) that complement network access controls.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Troubleshooting Linux Systems](troubleshooting-linux-systems.md) *(previous)*
- [Backup, Disaster Recovery, and Capacity](backup-disaster-recovery-and-capacity.md) *(next)*
- [SSH Hardening and Firewalls](ssh-hardening-and-firewalls.md) *(related)*

## References

- [`sysctl.d(5)`](https://manpages.ubuntu.com/manpages/jammy/en/man5/sysctl.d.5.html) — sysctl drop-ins  
- [`limits.conf(5)`](https://manpages.ubuntu.com/manpages/jammy/en/man5/limits.conf.5.html) — resource limits  
- [Ubuntu Server documentation](https://documentation.ubuntu.com/server/) — hardening topics  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
