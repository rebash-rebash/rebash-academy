---
title: "Troubleshooting Linux Systems"
description: "Use a repeatable Linux troubleshooting method — gather facts, narrow scope, fix forward — with a hands-on broken-service lab on Ubuntu."
difficulty: intermediate
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 15 · Troubleshooting"
tags:
  - linux
  - troubleshooting
  - incident
  - journalctl
prerequisites:
  - linux/containers-namespaces-cgroups-and-oci
next:
  - linux/production-linux-hardening-and-performance
related:
  - linux/systemd-services-and-journalctl
  - linux/host-monitoring-vmstat-iostat-sar
interview: interview/linux
comments: false
---

# Troubleshooting Linux Systems

## Overview

Troubleshooting is not random command typing. It is a **method**: define the symptom, gather facts, narrow the scope, make one change at a time, and prove recovery with evidence. On Linux hosts the first facts usually come from **time**, **recent changes**, **failed units**, **disk**, **memory**, **network listen ports**, and **logs**.

In Cloud and DevOps work you troubleshoot jump servers, Continuous Integration (CI) runners, Kubernetes nodes, and application VMs. The tools differ slightly; the method stays the same. In this tutorial you will practise a checklist, break and fix a small systemd unit on purpose, and save an incident-style evidence pack under `~/rebash-linux/lab23`.

In production, communicate blast radius (how much is affected) in plain language, avoid untracked changes, and write down what you tried. Guessing without evidence extends outages.

This is **Tutorial 23** in **Module 15: Troubleshooting** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers.

## Prerequisites

- [Containers — Namespaces, cgroups, and OCI](containers-namespaces-cgroups-and-oci.md)
- Comfort with [systemd Services and journalctl](systemd-services-and-journalctl.md)
- A **practice Ubuntu 22.04/24.04 VM** with `sudo`

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply a fact-first troubleshooting checklist on a Linux host
- [ ] Use `systemctl --failed`, `journalctl`, `df`, and `ss` as early signals
- [ ] Diagnose a broken systemd unit from status + journal
- [ ] Fix forward with a reversible change and prove recovery
- [ ] Pack incident evidence under `~/rebash-linux/lab23`

## Architecture

Troubleshooting walks from user symptom → host signals → component logs → targeted fix → validation.

![Architecture diagram for Troubleshooting Linux Systems](../assets/excalidraw/linux-troubleshooting.svg)

## Theory

### What it is

A practical loop:

1. **Symptom** — what fails, since when, for whom?  
2. **Scope** — one host, one service, or many?  
3. **Facts** — status, logs, resources, recent changes  
4. **Hypothesis** — one likely cause  
5. **Action** — smallest safe change  
6. **Proof** — symptom gone; evidence saved  

```bash
systemctl --failed
journalctl -xe --no-pager | tail
df -hT
ss -lntu
```

### Why it matters

Unstructured troubleshooting causes longer outages and new failures. Interviewers and incident commanders look for method and evidence, not memorised trivia.

### How it works

| Area | First commands |
|------|----------------|
| Services | `systemctl status`, `--failed`, `journalctl -u` |
| Capacity | `df -hT`, `df -i`, `free -h` |
| CPU/I/O | `vmstat`, `iostat` |
| Network | `ip -br a`, `ss -lntu` |
| Auth/SSH | `journalctl -u ssh`, auth logs |

### Common pitfalls

- Changing three things at once.  
- Rebooting as the first step without capturing logs.  
- Fixing a symptom on the wrong host.  
- No before/after proof in the ticket.

## Hands-on Lab

### Objective

Run a host fact pack, deploy a systemd unit that fails on purpose, diagnose it with `systemctl`/`journalctl`, fix it, prove it is active, and save evidence under `~/rebash-linux/lab23`.

### Prerequisites

- Ubuntu with `sudo` and systemd

### Lab environment

Workspace: `~/rebash-linux/lab23`

```bash
mkdir -p ~/rebash-linux/lab23 && cd ~/rebash-linux/lab23
set -euo pipefail
date -Is | tee incident-start.txt
whoami | tee operator.txt
```

**Expected output:** timestamp and operator files exist.

### Real-world scenario

A practice “health writer” service should create `/var/tmp/rebash-lab23.ok` every time it runs. After a bad config change it fails. You are on call: gather host facts, find the failed unit, fix the ExecStart path, and attach proof that the unit is active again.

### Step-by-step tasks

#### Task 1 – Host fact pack

```bash
cd ~/rebash-linux/lab23
set -euo pipefail

uname -a | tee uname.txt
cat /etc/os-release | tee os-release.txt
uptime | tee uptime.txt
df -hT | tee df.txt
free -h | tee free.txt
systemctl is-system-running | tee systemd-state.txt || true
systemctl --failed --no-pager | tee failed-before.txt || true
ss -lntu | head -n 30 | tee ss.txt
ip -br a | tee ip.txt
```

**Expected output:** fact files created; systemd state captured (may be `running` or `degraded`).

#### Task 2 – Break a unit on purpose and diagnose

```bash
cd ~/rebash-linux/lab23
set -euo pipefail

# Broken unit: ExecStart points to a missing script
sudo tee /etc/systemd/system/rebash-lab23.service >/dev/null << 'EOF'
[Unit]
Description=REBASH lab23 health writer (intentionally broken first)
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/rebash-lab23-missing.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
set +e
sudo systemctl start rebash-lab23.service
set -e
systemctl status rebash-lab23.service --no-pager -l | tee status-broken.txt || true
journalctl -u rebash-lab23.service -n 30 --no-pager | tee journal-broken.txt
grep -Ei 'No such file|failed|status=' journal-broken.txt status-broken.txt
systemctl is-failed rebash-lab23.service | tee is-failed.txt
test "$(cat is-failed.txt)" = "failed"
```

**Expected output:** unit is `failed`; journal/status mention the missing ExecStart path.

#### Task 3 – Fix forward, prove recovery, pack evidence

```bash
cd ~/rebash-linux/lab23
set -euo pipefail

sudo tee /usr/local/bin/rebash-lab23-health.sh >/dev/null << 'EOF'
#!/bin/bash
set -euo pipefail
date -Is > /var/tmp/rebash-lab23.ok
EOF
sudo chmod 755 /usr/local/bin/rebash-lab23-health.sh

sudo tee /etc/systemd/system/rebash-lab23.service >/dev/null << 'EOF'
[Unit]
Description=REBASH lab23 health writer
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/rebash-lab23-health.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl reset-failed rebash-lab23.service || true
sudo systemctl start rebash-lab23.service
systemctl is-active rebash-lab23.service | tee is-active.txt
test "$(cat is-active.txt)" = "active"
test -f /var/tmp/rebash-lab23.ok
cat /var/tmp/rebash-lab23.ok | tee health-ok.txt
systemctl status rebash-lab23.service --no-pager -l | tee status-fixed.txt
journalctl -u rebash-lab23.service -n 20 --no-pager | tee journal-fixed.txt

tar -czf troubleshooting-evidence.tgz \
  incident-start.txt operator.txt uname.txt os-release.txt \
  uptime.txt df.txt free.txt systemd-state.txt failed-before.txt ss.txt ip.txt \
  status-broken.txt journal-broken.txt is-failed.txt \
  is-active.txt health-ok.txt status-fixed.txt journal-fixed.txt
ls -l troubleshooting-evidence.tgz | tee evidence-ls.txt
```

**Expected output:** unit `active`; `/var/tmp/rebash-lab23.ok` exists; evidence archive not empty.

### Validation steps

- [ ] Fact pack files exist under `~/rebash-linux/lab23`
- [ ] Broken state showed `failed` with a clear journal reason
- [ ] Fixed unit is `active` and wrote the ok file
- [ ] `troubleshooting-evidence.tgz` exists

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Unit not found` | Forgot `daemon-reload` | `sudo systemctl daemon-reload` |
| Still failed after fix | Old failure cached / wrong path | `reset-failed`; verify ExecStart exists |
| Cannot write `/etc/systemd/system` | No sudo | Use a practice VM with admin rights |
| `is-active` is `inactive` | oneshot without RemainAfterExit | Keep `RemainAfterExit=yes` as in the lab |

### Challenge exercise

Extend the unit into a simple **restarting service** (`Type=simple`) that loops `sleep 30` after rewriting the ok file, enable it, prove `active (running)`, then stop and disable it. Save `systemctl status` to `challenge-status.txt`.

### Learning outcomes

- Ran a repeatable host fact pack
- Diagnosed a failed unit from status + journal
- Fixed forward and proved recovery
- Built an incident evidence archive

### Cleanup

```bash
cd ~/rebash-linux/lab23
set -euo pipefail
sudo systemctl disable --now rebash-lab23.service 2>/dev/null || true
sudo rm -f /etc/systemd/system/rebash-lab23.service
sudo rm -f /usr/local/bin/rebash-lab23-health.sh
sudo systemctl daemon-reload
sudo rm -f /var/tmp/rebash-lab23.ok
# Keep troubleshooting-evidence.tgz if you want it
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab23/` with evidence files
- [ ] You can list the first five fact commands you run on a sick host
- [ ] You know why rebooting first can destroy evidence
- [ ] You can explain failed → fixed with journal proof

## Code Walkthrough

Production incident habit:

1. Announce symptom and scope  
2. Capture facts (do not reboot yet)  
3. Form one hypothesis  
4. Change one thing; watch logs  
5. Confirm user symptom cleared; attach evidence  

## Security Considerations

- Prefer read-only gathering before privileged changes  
- Do not paste secrets from logs into tickets  
- Use break-glass admin accounts carefully (emergency admin)  
- Record who changed what during the incident  
- Limit SSH access while you work on internet-facing hosts  

## Common Mistakes

!!! warning "Rebooting before collecting logs"
    Volatile evidence disappears. **Fix:** `journalctl`, `systemctl status`, and resource snapshots first.

!!! warning "Changing config and restarting three services at once"
    You cannot tell what fixed it. **Fix:** one change, then re-check.

!!! warning "Troubleshooting the wrong machine"
    Load balancers hide targets. **Fix:** confirm hostname/IP/instance ID with the reporter.

!!! warning "Declaring victory without a user-visible check"
    Unit active ≠ feature works. **Fix:** hit the real health URL or canary file users care about.

## Best Practices

- Keep a personal one-page checklist  
- Prefer reversible changes and feature flags  
- Use configuration management after emergency hotfixes  
- Write a short timeline in the ticket  
- Practise failure drills on lab VMs  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Service failed | Bad ExecStart/config | status + journal; fix path/config |
| Disk full | Logs/containers | `df`/`du`; rotate; expand |
| No listen port | App/crash/firewall | `ss`, journal, security groups |
| High load | CPU/I/O/memory | vmstat/iostat/free; top PIDs |
| Intermittent failure | Race/deps/time | journals across boots; chrony |

## Summary

Method beats memory. Gather facts, narrow scope, fix forward, prove recovery, and keep evidence. Next: [Production Hardening and Performance](production-linux-hardening-and-performance.md).

## Interview Questions

**1. What are the first five commands you run on an unfamiliar sick Linux VM?**

??? success "Reveal answer"
    A solid set is: `uptime` (load/time since boot), `df -hT` (+ `df -i`), `free -h`, `systemctl --failed`, and `journalctl -xe` / `journalctl -u <service>`. Add `ss -lntu` and `ip -br a` when the symptom is network. Explain *why* each command, not only the names.

**2. A service is `failed`. How do you proceed?**

??? success "Reveal answer"
    `systemctl status name -l`, then `journalctl -u name --since …`, fix the root cause (path, permissions, config), `daemon-reload` if units changed, `reset-failed` if needed, start, and prove with `is-active` plus an application check. Avoid reboot as step one.

**3. Why is “reboot the server” a weak first answer in interviews?**

??? success "Reveal answer"
    Reboot may clear symptoms without understanding cause, destroy volatile evidence, and hide recurring bugs. Prefer capturing logs and status first; reboot only when justified (kernel deadlock, exhausted resources with a plan).

**4. How do you decide if the problem is disk vs memory vs CPU?**

??? success "Reveal answer"
    Use `df`/`df -i` for disk, `free`/`vmstat` swap fields for memory, and `vmstat`/`top` runnable vs idle for CPU. High `wa` points to I/O. Correlate with the application symptom and recent changes.

**5. What evidence belongs in an incident ticket?**

??? success "Reveal answer"
    Timeline, scope, commands run, key outputs (`status`, journal snippets, `df`), changes made, and proof of recovery. Redact secrets. Before/after is stronger than “we restarted it”.

**6. How does troubleshooting a Kubernetes node differ from an app VM?**

??? success "Reveal answer"
    You still use host facts (`df`, journal for kubelet/runtime), but you also check node conditions, pods on the node, and cluster events. Decide whether the failure is node-level (disk pressure) or workload-level. Do not apply random `kubectl delete` without scope.

**7. What does “fix forward” mean?**

??? success "Reveal answer"
    Make the smallest safe change that restores service (correct config, free disk, restart one unit) while recording evidence — rather than only rolling back blindly or changing many things. Rollback is still valid when it is the safest path; either way, prove the user symptom is gone.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Containers — Namespaces, cgroups, and OCI](containers-namespaces-cgroups-and-oci.md) *(previous)*
- [Production Hardening and Performance](production-linux-hardening-and-performance.md) *(next)*
- [systemd Services and journalctl](systemd-services-and-journalctl.md) *(related)*

## References

- [`systemctl(1)`](https://www.freedesktop.org/software/systemd/man/systemctl.html) — systemd control  
- [`journalctl(1)`](https://www.freedesktop.org/software/systemd/man/journalctl.html) — journal queries  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
