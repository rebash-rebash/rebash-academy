---
title: "Lab — Install Linux and First Boot"
description: "Stand up an Ubuntu VM, verify boot and FHS layout, capture a baseline identity card, and confirm networking — your first Cloud/DevOps Linux host."
difficulty: beginner
estimated_time: "45–60 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - linux
  - install
  - boot
  - fhs
comments: false
---

# Lab — Install Linux and First Boot

## Lab Overview

**Purpose:** Prove you can bring a Linux host from install (or cloud image) to a verified first-boot baseline.

**Scenario:** Your team needs a disposable Ubuntu lab VM with a documented identity card before any application work.

**Expected outcome:** The host boots, you can log in, and `~/rebash-lab-linux-install/baseline.txt` records OS, kernel, hostname, and network facts.

!!! tip "This is a lab, not a tutorial"
    Apply [Linux Fundamentals](../linux/linux-fundamentals-distributions-and-architecture.md) and [Boot Process and Filesystem Hierarchy](../linux/boot-process-and-filesystem-hierarchy.md). Prefer evidence over screenshots alone.

## Business Scenario

A platform team onboards engineers with a standard Ubuntu 22.04/24.04 image. Before handing the VM to application teams, you must confirm the guest boots cleanly, networking works, and the Filesystem Hierarchy Standard (FHS) layout matches expectations.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Install or launch an Ubuntu VM and complete first boot
- [ ] Verify kernel, distribution, and hostname identity
- [ ] Navigate key FHS paths (`/etc`, `/var`, `/home`, `/usr`)
- [ ] Confirm basic network reachability
- [ ] Record a reusable baseline for later labs

## Prerequisites

### Knowledge

- [Linux Fundamentals: Distributions and Architecture](../linux/linux-fundamentals-distributions-and-architecture.md)
- [Boot Process and Filesystem Hierarchy](../linux/boot-process-and-filesystem-hierarchy.md)
- [Essential Linux Commands](../linux/essential-linux-commands.md)

### Software

| Tool | Notes |
|------|--------|
| Hypervisor or cloud VM | VirtualBox, VMware, UTM, Multipass, AWS/Azure/GCP free tier |
| Ubuntu 22.04 LTS or 24.04 LTS | Server image preferred |
| Console or SSH access | After install |

**Estimated cost:** £0 locally. Small cloud VMs are often free-tier eligible.

## Environment

Work on a host **you own**. Create a workspace:

```bash
mkdir -p ~/rebash-lab-linux-install
cd ~/rebash-lab-linux-install
```

## Initial State

Fresh Ubuntu install or newly launched cloud image. No application packages required yet.

## Lab Tasks

### Task 1 — Install or launch Ubuntu

**Objective:** Obtain a running Ubuntu guest.

**Instructions:**

1. Create a VM with at least 2 GiB RAM and 20 GiB disk (or launch a `t3.micro` / equivalent).
2. Complete the installer (or accept cloud-init defaults).
3. Create a non-root sudo user if the image does not provide one.
4. Reboot once and confirm you can log in at the console or via SSH.

**Validation:**

```bash
whoami
hostnamectl
```

### Task 2 — Capture system identity

**Objective:** Record facts used in every later triage.

```bash
{
  echo "=== OS ==="
  cat /etc/os-release
  echo "=== Kernel ==="
  uname -a
  echo "=== Hostname ==="
  hostnamectl
  echo "=== Uptime ==="
  uptime
} | tee ~/rebash-lab-linux-install/baseline.txt
```

**Expected:** Debian/Ubuntu `ID=` lines, a modern kernel string, and a stable hostname.

### Task 3 — Walk the FHS

**Objective:** Confirm standard directories exist and understand their roles.

```bash
ls -ld / /bin /boot /dev /etc /home /opt /proc /sys /tmp /usr /var
df -hT /
ls /etc | head
ls /var/log | head
```

Add a short note to `baseline.txt` listing which path holds configuration, logs, and user homes.

### Task 4 — First-boot network check

```bash
ip -br a
ip route
ping -c 3 1.1.1.1 || ping -c 3 8.8.8.8
getent hosts google.com || true
```

Append successful `ip -br a` and default route to `baseline.txt`.

### Task 5 — Package index sanity (optional but recommended)

```bash
sudo apt update
sudo apt install -y tree curl
tree -L 1 / | tee -a ~/rebash-lab-linux-install/baseline.txt
```

## Validation

- [ ] Host reboots and you can log in
- [ ] `baseline.txt` contains OS, kernel, hostname, disk, and network facts
- [ ] You can explain `/etc` vs `/var` vs `/home` in one sentence each

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|----------------|------------|
| No network | NAT/bridged misconfigured | Fix hypervisor NIC; check `ip link` |
| Cannot sudo | User not in sudo group | Console as root: `usermod -aG sudo <user>` |
| Slow apt | Mirror or DNS | Check `/etc/resolv.conf`; retry `apt update` |

## Challenge Extensions

- Compare `systemd-analyze blame` on first boot vs after installing packages
- Document UEFI vs BIOS boot path for your hypervisor
- Snapshot the VM before the next lab

## Cleanup

Keep the VM for later labs, or delete it if disposable:

```bash
# Local workspace only — safe to remove
rm -rf ~/rebash-lab-linux-install
```

Destroy the cloud/hypervisor VM if you no longer need it to avoid ongoing cost.

## Production Discussion

Golden images and cloud-init replace manual installers at scale. Still capture identity cards (OS, kernel, AMI/image ID) in runbooks so on-call can compare “known good” to “what changed”.

## Best Practices

- Prefer LTS images for labs and production baselines
- Separate personal and service accounts early
- Snapshot or image before irreversible experiments

## Common Mistakes

| Mistake | Why it happens | Correct approach |
|---------|----------------|------------------|
| Using a shared laptop as “the server” | Convenience | Dedicated VM/cloud instance |
| Skipping baseline notes | Rushing | Write `baseline.txt` every time |
| Running everything as root | Habit | Daily user + sudo |

## Success Criteria

You can hand a teammate `baseline.txt` and they can reconstruct what host you built without asking.

## Reflection Questions

1. What differs between a cloud image and an ISO install for first boot?
2. Which FHS paths would you bind-mount or volume-claim in containers later?
3. How would you prove the host was not tampered with after first boot?

## Interview Connection

Expect: “Walk me through bringing up a Linux VM and what you check first.” Lead with identity, disk, network, then services.

## Related Tutorials

- [Linux Fundamentals: Distributions and Architecture](../linux/linux-fundamentals-distributions-and-architecture.md)
- [Boot Process and Filesystem Hierarchy](../linux/boot-process-and-filesystem-hierarchy.md)
- Cheat sheet: [Linux](../cheatsheets/linux.md)
- Path: [Linux for Cloud & DevOps](../learning-paths/linux-for-cloud-devops.md)

## References

- [Ubuntu Server documentation](https://ubuntu.com/server/docs)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
