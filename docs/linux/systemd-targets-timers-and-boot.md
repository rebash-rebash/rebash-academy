---
title: "systemd Targets, Timers, and Boot"
description: "Linux boot targets, systemd timers, and boot analysis — plain language first, then a safe timer lab."
difficulty: beginner
estimated_time: "45–55 min"
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
technology: linux
module: "Module 7 · Services & Boot"
tags:
  - linux
  - targets
  - timers
  - boot
  - beginners
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

Boot is not magic: **targets** group what should start, and **timers** replace many cron jobs with systemd-native schedules.

When a Linux server boots, something must decide **what state** the system reaches — command-line server, desktop, rescue mode. **Targets** are systemd’s way to group units into that desired state. **Timers** schedule recurring work (like cron, but integrated with systemd logs). **Boot analysis** tools show why startup is slow.

**Plain problem:** A backup should run every night, but cron emails nobody reads. A timer tied to a service gives you `journalctl` evidence and dependency ordering. After a kernel update, boot feels slow — `systemd-analyze` shows which unit delayed you.

This is **Tutorial 11** in **Module 7: Services & Boot** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — practical Linux for Cloud and DevOps work.

## Prerequisites

- [systemd Services and journalctl](systemd-services-and-journalctl.md)
- A practice Ubuntu 22.04/24.04 VM with `sudo`
- Comfortable with `systemctl` and `journalctl` from the previous tutorial

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain targets vs old runlevels and name common targets
- [ ] Read the default target and list units in the boot chain
- [ ] Create a systemd timer + service pair and verify with journalctl
- [ ] Use `systemd-analyze` for boot timing (read-only)
- [ ] Remove the lab timer cleanly and save evidence under `~/rebash-linux/lab11`
- [ ] Answer common fresher interview questions on boot and timers

## Architecture

Boot flows from firmware to PID 1 (systemd), which activates a **default target** (usually `multi-user.target` on servers). Timers trigger **services** on a schedule.

![Boot process — firmware to multi-user target](../assets/excalidraw/linux-boot-process.svg)

## Theory

### The problem (before any jargon)

Old Linux used numbered **runlevels** (0 halt, 1 single-user, 3 multi-user, 5 graphical). systemd replaced that with **targets** — named goals like `multi-user.target` or `graphical.target`.

You also need scheduled jobs. **cron** still exists, but **systemd timers** integrate with units, journals, and randomised delay (jitter) — useful on fleets.

### Targets (simple words)

**Analogy:** A target is a “mode” sign on the building — “server floor open” vs “maintenance only.” Activating a target pulls in the units grouped under it.

| Target | Plain meaning |
|--------|----------------|
| `multi-user.target` | Normal server — network, login, services, no GUI required |
| `graphical.target` | Desktop environment (depends on multi-user) |
| `rescue.target` | Minimal single-user repair shell |
| `emergency.target` | Even more minimal — broken configs |

**Tiny example:**

``` {.bash .ra-terminal title="Terminal"}
systemctl get-default
systemctl list-dependencies multi-user.target --no-pager | head
systemctl isolate multi-user.target   # do NOT run rescue on remote VM without console
```

**What you can say in an interview:** “Targets group boot state; servers usually default to multi-user.target; I inspect with get-default and list-dependencies.”

**Interview line:** “I never `isolate rescue.target` on a remote cloud VM without console access — I can lock myself out of networking.”

### systemd timers vs cron

| Feature | cron | systemd timer |
|---------|------|----------------|
| Logs | Often email or silent | journalctl on linked service |
| Dependencies | Limited | `After=`, `Requires=` on units |
| Random delay | Manual | `RandomizedDelaySec=` built-in |
| Missed run | May skip | `Persistent=true` can catch up |

A timer unit (`.timer`) activates a service unit (`.service`) on calendar or monotonic schedule.

**Tiny example — list timers:**

``` {.bash .ra-terminal title="Terminal"}
systemctl list-timers --all --no-pager | head
```

### Boot analysis

``` {.bash .ra-terminal title="Terminal"}
systemd-analyze time
systemd-analyze blame | head
systemd-analyze critical-chain
```

**Interview line:** “blame lists units by startup duration; critical-chain shows the longest dependency path this boot.”

### Common pitfalls

- Changing default target to graphical on a headless server — wastes resources
- Isolating rescue/emergency on SSH-only hosts — no network, no help
- Timer without matching `.service` — nothing runs
- Forgetting `systemctl enable timer` — timer does not survive reboot

## Hands-on Lab

### Objective

Inspect boot target and timing (read-only), create a lab timer that appends a line to a file every minute, prove runs in journalctl, then remove cleanly.

### Prerequisites

| Item | Notes |
|------|--------|
| Ubuntu VM with systemd | Previous lab completed |
| `sudo` | Install timer units |
| Remote VM safety | Do **not** switch to rescue/emergency targets |

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab11 && cd ~/rebash-linux/lab11
```

### Real-world scenario

Ops wants a nightly disk-usage snapshot. They prefer systemd timers so failures appear in the same journal as other services. You prototype a one-minute timer locally, prove two firings, and attach logs to the change request.

### Step-by-step tasks

#### Task 1 – Boot target and timing (read-only)

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab11
systemctl get-default | tee default-target.txt
systemd-analyze time | tee boot-time.txt
systemd-analyze blame | head -15 | tee boot-blame-head.txt
test -s default-target.txt && test -s boot-time.txt
cat default-target.txt
```

!!! example "Expected output"
    `default-target.txt` usually shows `graphical.target` (desktop/WSL) or `multi-user.target` (server). `boot-time.txt` shows total boot duration.


#### Task 2 – Create timer service script and units

Create `timer-task.sh`:

```bash title="timer-task.sh"
#!/usr/bin/env bash
set -euo pipefail
echo "lab11 timer run $(date -Is)" >> /home/USER/rebash-linux/lab11/timer-runs.log
```

Create `rebash-lab11.service`:

```ini title="rebash-lab11.service"
[Unit]
Description=REBASH lab11 timer task

[Service]
Type=oneshot
ExecStart=/home/USER/rebash-linux/lab11/timer-task.sh
```

Create `rebash-lab11.timer`:

```ini title="rebash-lab11.timer"
[Unit]
Description=REBASH lab11 timer every minute

[Timer]
OnBootSec=30
OnUnitActiveSec=1min
Persistent=true

[Install]
WantedBy=timers.target
```

Prepare local copies with your username:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab11
sed "s|/home/USER|/home/$USER|g" timer-task.sh > timer-task.local.sh
mv timer-task.local.sh timer-task.sh
chmod +x timer-task.sh
sed "s|/home/USER|/home/$USER|g" rebash-lab11.service > rebash-lab11.local.service
sed "s|/home/USER|/home/$USER|g" rebash-lab11.timer > rebash-lab11.local.timer
touch timer-runs.log
test -x timer-task.sh
```

!!! example "Expected output"
    Scripts and unit templates exist; `timer-task.sh` is executable.


#### Task 3 – Install, enable timer, wait for runs

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab11
sudo cp rebash-lab11.local.service /etc/systemd/system/rebash-lab11.service
sudo cp rebash-lab11.local.timer /etc/systemd/system/rebash-lab11.timer
sudo systemctl daemon-reload
sudo systemctl enable --now rebash-lab11.timer
systemctl list-timers rebash-lab11.timer --no-pager | tee timer-list.txt
echo "Waiting ~70s for timer firings..."
sleep 70
wc -l timer-runs.log | tee timer-run-count.txt
test "$(wc -l < timer-runs.log)" -ge 1
```

!!! example "Expected output"
    `timer-list.txt` shows next trigger time. `timer-runs.log` has at least one line after waiting.


#### Task 4 – journalctl proof

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab11
sudo journalctl -u rebash-lab11.service -n 10 --no-pager | tee timer-journal.txt
grep -q 'Finished' timer-journal.txt || grep -q 'lab11' timer-journal.txt
systemctl is-enabled rebash-lab11.timer | tee timer-enabled.txt
echo "lab11 timers OK" | tee evidence.txt
```

!!! example "Expected output"
    Journal shows service start/finish entries. `timer-enabled.txt` prints `enabled`.


### Validation steps

- [ ] Default target and boot time captured without changing boot config
- [ ] Timer fired at least once (`timer-runs.log`)
- [ ] `journalctl -u rebash-lab11.service` shows runs
- [ ] You did **not** isolate rescue/emergency on a remote VM

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Timer listed but log empty | Service path wrong | Run `timer-task.sh` manually; check journal |
| `Failed to create timer-runs.log` | Permissions | Ensure script writes to your home path |
| Timer not enabled at reboot | Only started timer | `systemctl enable rebash-lab11.timer` |
| No second run yet | 1min interval | Wait full 70s; check `list-timers` |

### Challenge exercise

Add `RandomizedDelaySec=15` to the timer, reload, and show the next trigger in `list-timers` (jitter spreads load in production fleets).

Add to timer `[Timer]` section, reinstall, and verify:

```ini title="rebash-lab11.timer"
[Timer]
OnBootSec=30
OnUnitActiveSec=1min
Persistent=true
RandomizedDelaySec=15
```

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab11
grep -q RandomizedDelaySec rebash-lab11.local.timer || echo "RandomizedDelaySec=15" >> rebash-lab11.local.timer
sudo cp rebash-lab11.local.timer /etc/systemd/system/rebash-lab11.timer
sudo systemctl daemon-reload
sudo systemctl restart rebash-lab11.timer
systemctl list-timers rebash-lab11.timer --no-pager | tee challenge-timer.txt
grep -q 'rebash-lab11' challenge-timer.txt
```

### Learning outcomes

- You read default target and boot timing safely
- You created timer + oneshot service with journal evidence
- You understand why timers beat silent cron on managed hosts

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
sudo systemctl disable --now rebash-lab11.timer
sudo rm -f /etc/systemd/system/rebash-lab11.service /etc/systemd/system/rebash-lab11.timer
sudo systemctl daemon-reload
cd ~/rebash-linux/lab11
# Keep evidence and local unit copies for revision
```

## Validation

- [ ] Lab completed under `~/rebash-linux/lab11`
- [ ] Can explain target vs runlevel in one sentence
- [ ] Ready for storage tutorials next

## Code Walkthrough

1. **`get-default`** — know server vs desktop boot goal before changing anything.
2. **Timer + oneshot service** — timer triggers; service does work once per firing.
3. **`Persistent=true`** — catch up missed runs after downtime (backups).
4. **`systemd-analyze blame`** — read-only performance triage after updates.
5. **Never isolate rescue on SSH-only hosts** — keep a console path or use `systemctl restart networking` instead.

## Security Considerations

- Rescue/emergency targets can disable network — use only with out-of-band console.
- Timer scripts run as root unless `User=` is set — prefer least-privilege service user.
- Validate script paths — timers are a common persistence mechanism for attackers.
- Restrict write access to `/etc/systemd/system`.
- Review `systemctl list-timers --all` during audits.

## Common Mistakes

!!! warning "Rescue target over SSH"
    You lose network and may lock the session. Fix: use cloud serial console or avoid isolate on remote VMs.

!!! warning "Enabled service but disabled timer"
    The schedule unit must be enabled: `systemctl enable foo.timer`.

!!! warning "Monolithic cron migration"
    Copying cron lines without `User=` and logging loses audit trail. Fix: one service unit per job with journal.

!!! warning "Ignoring boot regressions"
    Kernel updates can slow boot. Fix: capture `systemd-analyze blame` before/after in change notes.

## Best Practices

- Prefer timers for new scheduled work on systemd hosts
- Use `OnCalendar=*-*-* 02:00:00` for wall-clock schedules in production
- Add `RandomizedDelaySec` on fleet-wide jobs to avoid thundering herd
- Document timer units in Git alongside application code
- Keep default `multi-user.target` on headless servers

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Timer inactive | Not enabled | `systemctl enable --now timer` |
| Service runs once at boot only | Wrong timer directives | Check `OnUnitActiveSec` vs `OnCalendar` |
| Long boot after update | Slow unit in chain | `systemd-analyze critical-chain` |
| Timer runs as root unexpectedly | No User= in service | Drop-in `User=` for job account |

## Summary

**Targets** define boot state; **timers** schedule **services** with journal integration. Use **systemd-analyze** to read boot performance — do not reckless-switch rescue targets on remote VMs. Next you will learn **disks, partitions, and filesystems**.

## Interview Questions

**1. What is a systemd target?**

??? success "Reveal answer"
    A target is a systemd unit that groups other units to reach a system state (like multi-user or graphical). It replaces old SysV runlevels with named goals and dependency graphs.

**2. What is the usual default target on a server?**

??? success "Reveal answer"
    **`multi-user.target`** — multi-user command-line environment with network and services, without requiring a graphical desktop. Desktops often default to **`graphical.target`**, which builds on multi-user.

**3. How does a systemd timer relate to a service?**

??? success "Reveal answer"
    The **`.timer`** unit defines when to trigger; it activates a matching **`.service`** unit that performs the work. Enable the **timer** (not only the service) for scheduling. Logs appear under the service name in journalctl.

**4. Why use timers instead of cron?**

??? success "Reveal answer"
    Timers integrate with systemd dependencies, show runs in **journalctl**, support **`Persistent=`** catch-up, and **`RandomizedDelaySec=`** jitter. Easier to audit on homogeneous fleets than scattered crontabs.

**5. What does systemd-analyze blame show?**

??? success "Reveal answer"
    Time spent starting each unit during boot, sorted slowest first. Helps find which service or mount delayed startup after kernel or package updates — read-only diagnostics.

**6. When is rescue.target dangerous on a cloud VM?**

??? success "Reveal answer"
    **`systemctl isolate rescue.target`** stops most services including networking on many configs. Over SSH you may lose access with no serial console. Use cloud provider console or avoid isolate on remote-only access.

**7. What does Persistent=true on a timer do?**

??? success "Reveal answer"
    If the system was off when a scheduled run was due, systemd runs the missed job soon after boot (catch-up). Important for backups and maintenance windows that must not silently skip.

## Related Tutorials

- Prior: [systemd Services and journalctl](systemd-services-and-journalctl.md)
- Next: [Disks, Partitions, and Filesystems](storage-disks-partitions-and-filesystems.md)
- Related: [Boot Process and Filesystem Hierarchy](boot-process-and-filesystem-hierarchy.md)

## References

- [systemd.target(5)](https://www.freedesktop.org/software/systemd/man/systemd.target.html)
- [systemd.timer(5)](https://www.freedesktop.org/software/systemd/man/systemd.timer.html)
- [systemd-analyze(1)](https://www.freedesktop.org/software/systemd/man/systemd-analyze.html)
- [REBASH Linux course index](index.md)
