---
title: "Host Monitoring — vmstat, iostat, and sar"
description: "Use vmstat, iostat, and sar from sysstat to read CPU, memory, and disk I/O signals on a practice Ubuntu VM."
difficulty: intermediate
estimated_time: "45–55 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 12 · Logging & Monitoring"
tags:
  - linux
  - vmstat
  - iostat
  - sar
  - sysstat
prerequisites:
  - linux/logging-syslog-journald-logrotate
next:
  - linux/ssh-hardening-and-firewalls
related:
  - linux/process-management
interview: interview/linux
comments: false
---

# Host Monitoring — vmstat, iostat, and sar

## Overview

When a host feels “slow”, you need numbers for **CPU**, **memory**, and **disk Input/Output (I/O)** — not guesses. Classic Linux tools from the **sysstat** package help: **`vmstat`** for processes, memory, swap, and CPU; **`iostat`** for per-disk I/O; **`sar`** for historical samples (when the sysstat collector is enabled).

Cloud consoles show graphs, but SSH-era tools still matter on jump servers, during outages when agents are down, and in interviews. In this tutorial you will install sysstat if needed, capture `vmstat`/`iostat`/`sar` samples, generate a little controlled load, and save proof under `~/rebash-linux/lab19`.

In production, pair these tools with metrics systems (Prometheus node exporter, CloudWatch, and similar). Use CLI tools to validate what dashboards claim and to dig deeper during incidents.

This is **Tutorial 19** in **Module 12: Logging & Monitoring** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers.

## Prerequisites

- [Logging — syslog, journald, and logrotate](logging-syslog-journald-logrotate.md)
- A **practice Ubuntu 22.04/24.04 VM** with `sudo`
- Ability to install `sysstat`

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Read key `vmstat` columns (runnable processes, swap, CPU idle/wait)
- [ ] Use `iostat -xz` to spot high util or await on disks
- [ ] Collect a `sar` sample (or explain when history is empty)
- [ ] Capture before/load/after evidence under `~/rebash-linux/lab19`
- [ ] Relate CLI signals to cloud VM sizing decisions

## Architecture

Host monitoring samples kernel counters for CPU, memory, and block I/O so operators can see pressure quickly.

![Architecture diagram for Host Monitoring](../assets/excalidraw/linux-host-monitoring.svg)

## Theory

### What it is

| Tool | Focus |
|------|--------|
| `vmstat` | Processes, memory, swap, I/O, CPU |
| `iostat` | CPU and per-device disk I/O |
| `sar` | Historical / scheduled activity reports |

```bash
vmstat 1 5
iostat -xz 1 3
sar -u 1 3
```

### Why it matters

High **`wa`** (I/O wait) points to storage. High runnable processes (`r` in vmstat) points to CPU contention. Heavy **swap** (`si`/`so`) points to memory pressure. Wrong diagnosis leads to the wrong fix (adding CPU when the disk is the bottleneck).

### How it works

1. Take a **baseline** when healthy (or at incident start).  
2. Watch a few samples over time (`vmstat 1 10`).  
3. Check disks with `iostat -xz`.  
4. Use `sar` when sysstat’s collector has history (`/var/log/sysstat`).

| Signal | Suggests |
|--------|----------|
| High `r`, low `id` | CPU busy / contention |
| High `wa` | Disk or NFS wait |
| Rising `si`/`so` | Swapping / memory pressure |
| Device `%util` near 100 | Disk saturated |

### Common pitfalls

- Trusting a single sample (look at trends).  
- Ignoring steal time (`st`) on busy hypervisors.  
- Assuming `sar` has history when the collector was never enabled.  
- Generating heavy load on shared production hosts “to test”.

## Hands-on Lab

### Objective

Install sysstat, capture baseline `vmstat`/`iostat`/`sar` output, create a short controlled CPU+disk load, capture again, and pack evidence under `~/rebash-linux/lab19`.

### Prerequisites

- Ubuntu practice VM (not a shared production host)

### Lab environment

Workspace: `~/rebash-linux/lab19`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab19 && cd ~/rebash-linux/lab19
set -euo pipefail
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y sysstat
command -v vmstat; command -v iostat; command -v sar
vmstat -V 2>&1 | head -n 1 | tee sysstat-tools.txt || true
```

!!! example "Expected output"
    `vmstat`, `iostat`, and `sar` are on `PATH`.


### Real-world scenario

Users say a practice API VM is slow. Before you resize the instance, you capture CPU/memory/disk signals with sysstat tools, create a small reproducible load to see how the counters move, and attach the outputs to the ticket.

### Step-by-step tasks

#### Task 1 – Baseline samples

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab19
set -euo pipefail

uptime | tee uptime-before.txt
free -h | tee free-before.txt
vmstat 1 5 | tee vmstat-before.txt
iostat -xz 1 3 | tee iostat-before.txt
sar -u 1 3 | tee sar-u-before.txt
sar -d 1 3 | tee sar-d-before.txt 2>/dev/null || echo 'sar -d unavailable' | tee sar-d-before.txt
```

!!! example "Expected output"
    baseline files exist; `vmstat-before.txt` has a header and several data rows.


#### Task 2 – Controlled load + capture during load

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab19
set -euo pipefail

# Short CPU load in background
(timeout 12s bash -c 'while true; do :; done' & echo $! > cpu-load.pid) || true
# Short disk write load
timeout 12s dd if=/dev/zero of=load.bin bs=1M count=256 conv=fdatasync status=none &
echo $! > dd-load.pid || true

sleep 2
vmstat 1 5 | tee vmstat-during.txt
iostat -xz 1 3 | tee iostat-during.txt

# Wait for loads to finish
wait || true
rm -f load.bin
kill "$(cat cpu-load.pid)" 2>/dev/null || true
```

!!! example "Expected output"
    `vmstat-during.txt` / `iostat-during.txt` captured while load ran; `load.bin` removed.


#### Task 3 – After sample + evidence pack

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab19
set -euo pipefail

sleep 2
vmstat 1 3 | tee vmstat-after.txt
iostat -xz 1 2 | tee iostat-after.txt
# Optional history location
ls -la /var/log/sysstat 2>/dev/null | tee sysstat-log-dir.txt || echo 'no /var/log/sysstat yet' | tee sysstat-log-dir.txt

# Simple asserts: files non-empty
test -s vmstat-before.txt && test -s vmstat-during.txt && test -s iostat-before.txt

tar -czf hostmon-evidence.tgz \
  sysstat-tools.txt uptime-before.txt free-before.txt \
  vmstat-before.txt iostat-before.txt sar-u-before.txt sar-d-before.txt \
  vmstat-during.txt iostat-during.txt \
  vmstat-after.txt iostat-after.txt sysstat-log-dir.txt
ls -l hostmon-evidence.tgz | tee evidence-ls.txt
```

!!! example "Expected output"
    evidence archive exists; during/after samples recorded.


### Validation steps

- [ ] `vmstat` and `iostat` produced before and during files
- [ ] You can point to idle (`id`) / wait (`wa`) columns in `vmstat`
- [ ] `sar -u` produced a sample (even if mostly idle)
- [ ] `hostmon-evidence.tgz` exists under `~/rebash-linux/lab19`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `iostat: command not found` | sysstat missing | `sudo apt-get install -y sysstat` |
| `sar` shows little history | Collector disabled | Enable sysstat cron/timer; still use live `sar -u 1 3` |
| Load made laptop unusable | Loop too aggressive | Shorten `timeout`; skip CPU loop on tiny VMs |
| Permission denied on `/var/log/sysstat` | Restricted perms | Use `sudo ls` or rely on live samples |

### Challenge exercise

Write `~/rebash-linux/lab19/quick-host-check.sh` that prints timestamp, `uptime`, one `vmstat 1 3` block, and one `iostat -xz 1 2` block to `quick-host-check.out`, exiting `0` if both tools succeed.

### Learning outcomes

- Captured baseline and under-load host signals
- Used vmstat/iostat/sar from sysstat
- Separated CPU vs disk pressure clues
- Saved monitoring evidence for a ticket

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab19
set -euo pipefail
rm -f load.bin cpu-load.pid dd-load.pid
# Keep hostmon-evidence.tgz if you want it
# sysstat package may remain installed — that is fine
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab19/` with evidence files
- [ ] You can explain what high `wa` suggests
- [ ] You know `sar` history needs the sysstat collector
- [ ] You would not run stress tests on shared production without approval

## Code Walkthrough

Incident host check:

1. `uptime`, `free -h`, `df -hT`  
2. `vmstat 1 10` — CPU/memory/swap  
3. `iostat -xz 1 5` — disk saturation  
4. `ps`/`pidstat` for top consumers  
5. Compare with cloud metrics; then change capacity or fix the app  

## Security Considerations

- Monitoring data can reveal process names and paths — control access  
- Do not run destructive stress tools on multi-tenant production  
- Protect historical `sar` logs if they include sensitive context  
- Prefer least privilege for monitoring agents  
- Keep accurate time (chrony) so samples align with other systems  

## Common Mistakes

!!! warning "Resizing CPU when `wa` is high"
    The bottleneck may be disk. **Fix:** confirm with `iostat` before changing instance size.

!!! warning "One 1-second sample as truth"
    Spikes mislead. **Fix:** sample over several seconds or minutes.

!!! warning "Ignoring steal time on VMs"
    Noisy neighbours reduce your CPU. **Fix:** watch `st` in `vmstat`/`sar`; consider new host/capacity.

!!! warning "Expecting weeks of `sar` history by default"
    Collector may be off. **Fix:** enable sysstat’s timer/cron or rely on a metrics stack.

## Best Practices

- Keep a small “first 5 commands” host checklist  
- Store baselines for critical VMs  
- Alert on saturation (CPU, memory, disk util/latency)  
- Correlate with app latency and error rates  
- Practise reading vmstat/iostat offline from saved files  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| High load, CPU idle | Uninterruptible I/O / DNS / locks | Check `wa`, `iostat`, app waits |
| High swap activity | RAM too small / leak | Inspect RSS; add RAM; fix app |
| Disk `%util` 100% | Storage bottleneck | Faster disk; reduce I/O; cache |
| Tools missing | Minimal image | Install `sysstat` |
| Metrics disagree with cloud | Agent lag / wrong host | Confirm instance ID; compare timestamps |

## Summary

`vmstat`, `iostat`, and `sar` turn “it feels slow” into CPU, memory, or disk evidence. Sample over time, compare before and during load, and fix the real bottleneck. Next: [SSH Hardening and Firewalls](ssh-hardening-and-firewalls.md).

## Interview Questions

**1. What does a high `wa` value in `vmstat` suggest?**

??? success "Reveal answer"
    High **I/O wait** means CPUs are idle waiting on block I/O (disk or sometimes network filesystems). Next check `iostat -xz` for saturated devices and review what process is doing heavy reads/writes.

**2. How do you use `iostat` to see if a disk is saturated?**

??? success "Reveal answer"
    Run `iostat -xz 1 5` and look at **`%util`**, **await**/latency fields, and throughput. Near-100% util with rising await often means the device is the bottleneck. Confirm which mount sits on that device with `lsblk`/`findmnt`.

**3. What is the difference between live `sar -u 1 3` and historical sar reports?**

??? success "Reveal answer"
    `sar -u 1 3` samples **live** counters now. Historical reports need the sysstat collector writing under `/var/log/sysstat`. If history is empty, enable the collector or use your metrics platform.

**4. Which `vmstat` fields help diagnose memory pressure?**

??? success "Reveal answer"
    Watch swap-in/swap-out (`si`/`so`), free memory, and overall CPU. Pair with `free -h` and process RSS from `ps`. Sustained swapping needs RAM or a leak fix, not only “tune swapiness” as a first answer.

**5. Why capture a baseline before changing instance size?**

??? success "Reveal answer"
    Without before/after numbers you cannot prove the resize helped. Baselines also show whether the problem was CPU, memory, or disk so you pick the right resize dimension.

**6. How does steal time (`st`) affect your reading on a cloud VM?**

??? success "Reveal answer"
    **Steal** means the hypervisor scheduled other work instead of your VM. Your app can look slow even when your process list is modest. Consider moving workload or increasing capacity; do not blame the app alone.

**7. Where do these tools fit next to Prometheus or CloudWatch?**

??? success "Reveal answer"
    Metrics systems are for continuous monitoring and alerting. `vmstat`/`iostat`/`sar` are for **interactive diagnosis**, interviews, and times when agents are broken. Good engineers use both.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Logging — syslog, journald, and logrotate](logging-syslog-journald-logrotate.md) *(previous)*
- [SSH Hardening and Firewalls](ssh-hardening-and-firewalls.md) *(next)*
- [Process Management](process-management.md) *(related)*

## References

- [`vmstat(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/vmstat.8.html) — Ubuntu man-pages  
- [`iostat(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/iostat.1.html) — Ubuntu man-pages  
- [sysstat project](https://github.com/sysstat/sysstat) — upstream  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
