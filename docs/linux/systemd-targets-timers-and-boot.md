---
title: "systemd Targets, Timers, and Boot"
description: "Inspect boot targets, schedule work with systemd timers, and analyse boot with systemd-analyze on a practice Ubuntu VM."
difficulty: intermediate
estimated_time: "45–55 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 7 · Services & Boot"
tags:
  - linux
  - targets
  - timers
  - boot
prerequisites:
  - linux/systemd-services-and-journalctl
next:
  - linux/storage-disks-partitions-and-filesystems
related:
  - linux/scheduling-cron-at-and-timers
  - linux/boot-process-and-filesystem-hierarchy
interview: interview/linux
comments: false
---

# systemd Targets, Timers, and Boot

## Overview

**Targets** are systemd units that group other units into a desired system state — the modern replacement for old SysV **runlevels**. Common examples are `rescue.target`, `multi-user.target` (typical server), and `graphical.target`. **Timers** activate services on a calendar or after boot, often replacing cron when you already use systemd. Together with **boot analysis** tools, they answer: when does the system become ready, and when does recurring work run?

Wrong default target can pull in a desktop stack you do not want on a server, or leave apps starting before the network is really up. Timers give dependency ordering, optional random delay (jitter), and journal integration — useful on fleets compared with silent cron mail. After package updates, boot regressions show up in `systemd-analyze critical-chain` and failed dependencies.

This tutorial stays **safe**: you inspect targets and boot timing, and you create a **lab timer** you remove in cleanup. You do **not** isolate to rescue or emergency on a remote VM without console access.

This is **Tutorial 11** in **Module 7: Services & Boot** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers.

## Prerequisites

- [systemd Services and journalctl](systemd-services-and-journalctl.md)
- A **practice Ubuntu 22.04/24.04 VM** with `sudo`
- Comfortable with `systemctl` and `journalctl` from the previous tutorial

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain targets vs old runlevels and name common targets
- [ ] Read the default target and list units belonging to it
- [ ] Create a `.timer` + `.service` pair, enable the timer, and verify with `list-timers`
- [ ] Use `systemd-analyze` to reason about boot cost
- [ ] Remove lab timer units cleanly and keep evidence under `~/rebash-linux/lab11`

## Architecture

At boot, systemd pulls in the default target and its dependencies. Timers later activate services on schedule; operators inspect both with systemctl and analyse delay with systemd-analyze.

![Architecture diagram for systemd Targets, Timers, and Boot](../assets/excalidraw/linux-boot-process.svg)

## Theory

### What it is

A **target** is a synchronisation point (a named goal state). A **timer** is a unit that activates another unit (usually a service) when time conditions match.

| Target | Role |
|--------|------|
| `rescue.target` | Minimal recovery environment |
| `emergency.target` | Even smaller; often root shell via sulogin |
| `multi-user.target` | Standard server (no GUI) |
| `graphical.target` | Desktop plus multi-user |
| `network-online.target` | Network configured (as defined by the network stack) |

| Scheduler | Strength |
|-----------|----------|
| cron | Simple per-user tables; ubiquitous |
| systemd timer | Dependencies, journal, jitter, unit hardening |

``` {.bash .ra-terminal title="Terminal"}
systemctl get-default
systemctl list-timers --all
systemd-analyze
```

### Why it matters

Apps that use `After=network.target` may still start before routes and DNS work; many need `network-online.target`. Timers that were never **enabled** never run — a common “cron migration” mistake (people enable the service instead of the timer). Slow boot after an agent install shows up in `systemd-analyze blame` long before users open tickets.

### How it works

1. **Default target** — `systemctl get-default` (often `graphical.target` or `multi-user.target`). Change only with care: `systemctl set-default multi-user.target`.
2. **Boot graph** — systemd activates dependencies of the default target after early sysinit and filesystem work.
3. **Timers** — pair `foo.timer` with `foo.service`. Calendar: `OnCalendar=*-*-* 02:30:00`. Monotonic: `OnBootSec=5min`. Enable the **timer**: `systemctl enable --now foo.timer`.
4. **Inspect** — `systemctl list-timers`, `systemctl status foo.timer`, `journalctl -u foo.service`.
5. **Analyse** — `systemd-analyze`, `systemd-analyze blame`, `systemd-analyze critical-chain`.

`systemctl isolate some.target` switches the running system toward that target — **disruptive**. Do not isolate rescue/emergency on a remote cloud VM without serial/console access planned.

### Key concepts and comparisons

| Timer field | Meaning |
|-------------|---------|
| `OnCalendar=` | Wall-clock schedule |
| `OnBootSec=` | Time after boot |
| `OnUnitActiveSec=` | Time after the unit last activated |
| `RandomizedDelaySec=` | Jitter to avoid thundering herd |
| `Persistent=true` | Catch up missed runs (calendar timers) |

| Pattern | Prefer when | Avoid when |
|---------|-------------|------------|
| systemd timer | Needs deps, journal, hardening | One-off user reminder (cron.d may be enough) |
| cron | Simple user crontab already standard | Complex dependency on other units |
| `network-online.target` | App needs real connectivity | App only needs local sockets |

### Common pitfalls

- Isolating rescue/emergency remotely without console access.
- Using `After=network.target` when the app needs `network-online.target`.
- Enabling the **service** instead of the **timer**.
- Timezone surprises — timers use the system timezone unless configured otherwise.
- Ignoring long `systemd-analyze blame` entries that delay SSH readiness.

## Hands-on Lab

### Objective

Inspect the default target and boot analysis, create a lab oneshot service activated by a timer, prove it with `list-timers` and journal output, and save evidence under `~/rebash-linux/lab11`.

### Prerequisites

- Ubuntu 22.04/24.04 with systemd and sudo
- Do not change the default target permanently on a shared machine

### Lab environment

Workspace: `~/rebash-linux/lab11`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab11 && cd ~/rebash-linux/lab11
set -euo pipefail
whoami | tee lab-user.txt
systemctl get-default | tee default-target.txt
sudo -n true 2>/dev/null || sudo -v
```

!!! example "Expected output"
    `default-target.txt` shows something like `multi-user.target` or `graphical.target`.


### Real-world scenario

Your platform team wants a small housekeeping job every few minutes on app VMs — with journal logs and a clear unit name — instead of an undocumented crontab line. You prototype a timer + oneshot service on a practice VM, show `list-timers` and one successful run, and remove it when the experiment ends.

### Step-by-step tasks

#### Task 1 – Inspect targets and boot analysis

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab11
set -euo pipefail

systemctl get-default | tee default-target.txt
systemctl list-units --type=target --no-pager | tee targets-list.txt
systemctl status multi-user.target --no-pager | tee multi-user-status.txt || true

systemd-analyze | tee analyze.txt
systemd-analyze blame | head -n 20 | tee analyze-blame.txt
systemd-analyze critical-chain | tee analyze-critical-chain.txt || true

grep -E 'Startup finished|multi-user|graphical' analyze.txt default-target.txt || true
test -s analyze-blame.txt
```

!!! example "Expected output"
    default target recorded; `analyze.txt` / blame output non-empty (wording varies by distro version).


#### Task 2 – Create oneshot service + timer

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab11
set -euo pipefail

mkdir -p "$HOME/rebash-linux/lab11/run"
UNIT_USER="$(whoami)"
UNIT_HOME="$HOME"
STAMP="${UNIT_HOME}/rebash-linux/lab11/run/timer-stamp.log"

# Oneshot service: append one line then exit
sudo tee /etc/systemd/system/rebash-lab-timer.service >/dev/null << EOF
[Unit]
Description=REBASH lab timer oneshot

[Service]
Type=oneshot
User=${UNIT_USER}
ExecStart=/bin/bash -c '/bin/echo "\$(date -Is) rebash-lab-timer fired" >> ${STAMP}'
EOF

# Timer: first run soon after enable, then every 2 minutes
sudo tee /etc/systemd/system/rebash-lab-timer.timer >/dev/null << 'EOF'
[Unit]
Description=REBASH lab timer schedule

[Timer]
OnBootSec=1min
OnUnitActiveSec=2min
AccuracySec=1s
Unit=rebash-lab-timer.service

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now rebash-lab-timer.timer
systemctl is-active rebash-lab-timer.timer | tee timer-active.txt
test "$(cat timer-active.txt)" = "active"

systemctl list-timers --all | tee list-timers.txt
grep -q 'rebash-lab-timer.timer' list-timers.txt
```

!!! example "Expected output"
    timer is `active`; `list-timers.txt` includes `rebash-lab-timer.timer`.


#### Task 3 – Trigger once, prove journal, pack evidence

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab11
set -euo pipefail

# Do not wait for the calendar — start the service once now
sudo systemctl start rebash-lab-timer.service
sleep 1
test -s "$HOME/rebash-linux/lab11/run/timer-stamp.log"
cp "$HOME/rebash-linux/lab11/run/timer-stamp.log" timer-stamp-copy.txt
grep -q 'rebash-lab-timer fired' timer-stamp-copy.txt

journalctl -u rebash-lab-timer.service -n 20 --no-pager | tee journal-timer-service.txt
systemctl status rebash-lab-timer.timer --no-pager | tee timer-status.txt

# Show relationship: timer watches the service unit
systemctl cat rebash-lab-timer.timer | tee timer-cat.txt
grep -q 'OnUnitActiveSec' timer-cat.txt

tar -czf targets-timers-evidence.tgz \
  lab-user.txt default-target.txt targets-list.txt \
  analyze.txt analyze-blame.txt analyze-critical-chain.txt \
  timer-active.txt list-timers.txt timer-stamp-copy.txt \
  journal-timer-service.txt timer-status.txt timer-cat.txt
ls -l targets-timers-evidence.tgz | tee evidence-ls.txt
test -s targets-timers-evidence.tgz
```

!!! example "Expected output"
    stamp file has a fired line; archive is non-empty.


### Validation steps

- [ ] `default-target.txt` exists
- [ ] `systemd-analyze` output captured
- [ ] `rebash-lab-timer.timer` appears in `list-timers`
- [ ] Stamp log shows at least one fire
- [ ] `targets-timers-evidence.tgz` exists

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Timer active but stamp empty | Only waited on schedule | `systemctl start rebash-lab-timer.service` as in Task 3 |
| `Unit not found` | No daemon-reload | `sudo systemctl daemon-reload` |
| Enabled service but nothing runs | Enabled `.service` instead of `.timer` | `enable --now …timer` |
| Permission denied writing stamp | Path/user mismatch | Match `User=` and directory ownership |

### Challenge exercise

Add `RandomizedDelaySec=30` to the lab timer via a drop-in directory `rebash-lab-timer.timer.d/10-jitter.conf`, daemon-reload, restart the timer, and save `systemctl cat rebash-lab-timer.timer` to `challenge-timer-cat.txt` showing the jitter. Remove the drop-in in Cleanup.

### Learning outcomes

- Inspected default target and boot analysis
- Created and enabled a systemd timer + oneshot service
- Proved a run with stamp file and journal
- Packaged evidence for a change ticket

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab11
set -euo pipefail

sudo systemctl disable --now rebash-lab-timer.timer 2>/dev/null || true
sudo rm -f /etc/systemd/system/rebash-lab-timer.timer
sudo rm -f /etc/systemd/system/rebash-lab-timer.service
sudo rm -rf /etc/systemd/system/rebash-lab-timer.timer.d
sudo systemctl daemon-reload
sudo systemctl reset-failed rebash-lab-timer.service 2>/dev/null || true

# Optional: rm -rf run *.txt targets-timers-evidence.tgz
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab11/` with evidence files
- [ ] You can explain target vs timer vs service
- [ ] You know to enable the timer, not only the service
- [ ] You understand why remote `isolate rescue.target` is dangerous without console access

## Code Walkthrough

In real servers, boot and schedule work usually follows this order:

1. **Inspect default target and failed units** before changing boot behaviour  
2. **Prefer timers under `/etc`** with clear service oneshots for housekeeping  
3. **Enable the timer**; verify with `list-timers`  
4. **Use journalctl** on the service unit for proof  
5. **Analyse boot** after agent installs (`blame` / `critical-chain`)  

Keep rescue/emergency drills for lab VMs with console access.

## Security Considerations

- Restrict who can change default targets or install timers as root  
- Treat timer-run scripts like any privileged automation — least privilege `User=`  
- Avoid running arbitrary downloaded scripts from timers  
- Remember journal lines from timers may contain sensitive paths  
- On shared hosts, review `list-timers --all` for unexpected schedules  

## Common Mistakes

!!! warning "Enabling the service instead of the timer"
    The job never schedules. **Fix:** `systemctl enable --now name.timer` and check `list-timers`.

!!! warning "Isolating rescue on a remote cloud VM"
    You may lose SSH with no console. **Fix:** use provider serial console first; practise isolate only on disposable VMs.

!!! warning "Assuming `network.target` means connectivity"
    It often means the network stack is up, not that routes/DNS work. **Fix:** order with `network-online.target` when the app needs the network.

!!! warning "Ignoring timezone on OnCalendar"
    Jobs fire at unexpected wall times. **Fix:** confirm `timedatectl` and document timezone in the runbook.

## Best Practices

- Name timers and services as a pair (`app-cleanup.timer` / `.service`)  
- Add `RandomizedDelaySec=` for fleet-wide schedules  
- Prefer oneshot + timer for periodic work; long loops belong in services  
- Capture `systemd-analyze` before/after heavy agents  
- Keep cron only where policy already standardises it — do not mix silently  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Timer never fires | Not enabled / wrong WantedBy | `enable --now`; check `timers.target` |
| Service fails when fired | ExecStart error | `journalctl -u name.service` |
| Boot very slow | Slow units in blame | Investigate top blame entries; consider deferring |
| App starts too early | Wrong After=/Wants= | Use `network-online.target` when needed |
| Missed calendar runs | Host was off; Persistent not set | Consider `Persistent=true` for calendar timers |

## Summary

Targets define system goals; timers schedule unit activation; `systemd-analyze` explains boot cost. Inspect safely, enable timers correctly, and prove runs with journal and stamp files. Next: [Storage — Disks, Partitions, and Filesystems](storage-disks-partitions-and-filesystems.md).

## Interview Questions

**1. What replaced SysV runlevels in systemd, and what is a common server default target?**

??? success "Reveal answer"
    **Targets** replaced runlevels. Many servers use **`multi-user.target`** (non-graphical multi-user). Desktops often use `graphical.target`, which pulls in multi-user plus display services. Check with `systemctl get-default`.

**2. Why enable a `.timer` instead of enabling the `.service` for scheduled work?**

??? success "Reveal answer"
    The **timer** is what triggers the service on schedule. Enabling only the service may start it at boot (if WantedBy is set that way) or do nothing useful for periodic runs. For schedules, `enable --now name.timer` and verify with `systemctl list-timers`.

**3. When would you choose a systemd timer over cron?**

??? success "Reveal answer"
    Choose a **timer** when you need unit dependencies, journal logging, randomised delay, or the same hardening as other systemd services. Cron remains fine for simple per-user jobs where the organisation already standardises crontab.

**4. What is dangerous about `systemctl isolate rescue.target` on a remote VM?**

??? success "Reveal answer"
    Isolate switches the system toward that target and can **stop SSH and normal services**. Without serial/console access you may lock yourself out. Use only with a planned console path, preferably on a practice VM.

**5. How do `network.target` and `network-online.target` differ for application ordering?**

??? success "Reveal answer"
    `network.target` means the network management stack is up; it does **not** guarantee a usable default route or DNS. Apps that need real connectivity should typically order after **`network-online.target`** (understanding that “online” still depends on network configuration quality).

**6. How do you investigate a slower boot after installing a monitoring agent?**

??? success "Reveal answer"
    Run `systemd-analyze`, `systemd-analyze blame`, and `systemd-analyze critical-chain`. Find units that added large delays or failed dependencies, then fix ordering, defer non-critical work, or open a vendor issue — with before/after evidence.

**7. What does `RandomizedDelaySec=` solve on a large fleet?**

??? success "Reveal answer"
    It adds **jitter** so thousands of nodes do not hit the same registry, API, or package mirror at the exact same second (thundering herd). Useful for update and housekeeping timers.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [systemd Services and journalctl](systemd-services-and-journalctl.md) *(previous)*
- [Storage — Disks, Partitions, and Filesystems](storage-disks-partitions-and-filesystems.md) *(next)*
- [Scheduling with cron, at, and timers](scheduling-cron-at-and-timers.md) *(related)*
- [Boot Process and Filesystem Hierarchy](boot-process-and-filesystem-hierarchy.md) *(related)*

## References

- [systemd documentation](https://systemd.io/)  
- [`systemd.timer(5)`](https://manpages.ubuntu.com/manpages/jammy/en/man5/systemd.timer.5.html) — Ubuntu man-pages  
- [`systemd-analyze(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/systemd-analyze.1.html) — Ubuntu man-pages  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
