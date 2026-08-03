---
title: "Package Management"
description: "Install, query, hold, and remove packages with apt on Ubuntu, and understand how dnf/yum and zypper fit other distributions."
difficulty: beginner
estimated_time: "45–55 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 10 · Package Management"
tags:
  - linux
  - apt
  - dnf
  - yum
  - packages
prerequisites:
  - linux/ssh-and-remote-access
next:
  - linux/scheduling-cron-at-and-timers
related:
  - labs/linux-ops-toolkit-lab
labs:
  - labs/linux-ops-toolkit-lab
interview: interview/linux
comments: false
---

# Package Management

## Overview

A **package manager** installs, updates, and removes software in a consistent way for your Linux distribution. On Ubuntu and Debian you use **`apt`** (and lower-level **`dpkg`**). On Red Hat Enterprise Linux (RHEL) family systems you use **`dnf`** (or older **`yum`**) with **`rpm`**. On SUSE you use **`zypper`**. Optional tools such as **snap** and **Flatpak** exist mainly for desktop apps and are usually secondary on servers.

Unpatched packages are security debt. Golden images, Continuous Integration (CI) runners, and configuration management all assume a known package state. In this tutorial you will refresh package metadata, install a small tool, query version and files, place an **apt hold** (pin so it does not upgrade by accident), remove a package cleanly, and save proof under `~/rebash-linux/lab16`. The lab uses Ubuntu `apt` because that matches most practice VMs; the Theory tables cover other families so you can work across clouds.

In production, prefer distribution packages for system daemons, reboot after kernel updates, and record critical versions in image builds rather than “hand-installed” binaries that nobody can reproduce. Automate patching carefully (`unattended-upgrades`, `dnf-automatic`) with a maintenance window.

This is **Tutorial 16** in **Module 10: Package Management** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers.

## Prerequisites

- [SSH and Remote Access](ssh-and-remote-access.md)
- A **practice Ubuntu 22.04/24.04 VM** with `sudo` and working `apt` repositories
- Do **not** run experimental holds/removes on a shared production server

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain what a package manager does and name the common tools per distro family
- [ ] Update apt metadata and install a package with `apt-get`
- [ ] Query package policy, files, and status with `apt` / `dpkg`
- [ ] Hold and unhold a package, then remove it cleanly
- [ ] Describe how kernel updates and image builds relate to patching

## Architecture

Repositories publish packages. The package manager resolves dependencies, installs files, and tracks state in a local database (`dpkg` / `rpm`).

![Architecture diagram for Package Management](../assets/excalidraw/linux-package-management.svg)

## Theory

### What it is

| Family | Install / update | Query | Database |
|--------|------------------|-------|----------|
| Debian / Ubuntu | `apt` / `apt-get` | `apt policy`, `dpkg -l` | `dpkg` |
| RHEL / Fedora / Amazon Linux | `dnf` (or `yum`) | `rpm -q`, `dnf list` | `rpm` |
| SUSE | `zypper` | `zypper info`, `rpm -q` | `rpm` |

Packages bring version metadata, dependencies, and a file inventory the OS can verify.

```bash title="Terminal"
sudo apt-get update
apt-cache policy curl
dpkg -l curl
```

### Why it matters

Manual binaries under `/usr/local` drift and are hard to patch. Unpatched kernels and libraries are a major host vulnerability class. Interviewers and hiring managers expect you to install tools the distro way, know how to check versions, and explain holds/pins when a change must wait.

### How it works

1. **Refresh metadata** — `apt-get update`, `dnf check-update`, `zypper refresh`.
2. **Install** — `apt-get install`, `dnf install`, `zypper install`.
3. **Query** — `apt policy`, `dpkg -L package`, `rpm -ql package`.
4. **Upgrade** — apply security and bugfix releases; kernel updates usually need a **reboot**.
5. **Hold / pin** — stop a package from upgrading until you are ready (`apt-mark hold` on Ubuntu).
6. **Remove** — `apt-get remove` (keep config) or `purge` (remove config too); clean unused deps with `autoremove`.

```bash title="Terminal"
sudo apt-get install -y tree
apt-mark showhold
sudo apt-mark hold tree
```

Prefer distro packages for system services. Use containers or language tools (pip, npm) for app runtimes when isolation matters. Snap/Flatpak are optional; many servers disable snap for simplicity.

### Key concepts and comparisons

| Action | apt (Ubuntu) | dnf (RHEL-like) |
|--------|--------------|-----------------|
| Refresh | `apt-get update` | `dnf check-update` / `makecache` |
| Install | `apt-get install pkg` | `dnf install pkg` |
| Remove | `apt-get remove pkg` | `dnf remove pkg` |
| Hold | `apt-mark hold pkg` | `dnf versionlock` (plugin) |
| Files list | `dpkg -L pkg` | `rpm -ql pkg` |

| Pattern | Prefer when | Avoid when |
|---------|-------------|------------|
| Distro package | System tools, daemons | You need a bleeding-edge app version |
| Container image | App runtime isolation | Simple host CLI tools |
| Manual binary in `/usr/local` | Rare emergency | Default for every tool |

### Common pitfalls

- Running `apt-get upgrade` on production without a window or snapshot.
- Forgetting `apt-get update` so installs fail or get stale versions.
- Holding packages forever and missing security fixes.
- Mixing random third-party `.deb` files without trusting the source.
- Assuming the same package name exists on every distro (`apache2` vs `httpd`).

## Hands-on Lab

### Objective

On a practice Ubuntu VM, install `tree`, prove it with queries, place and remove an apt hold, remove the package, and save a package evidence archive under `~/rebash-linux/lab16`.

### Prerequisites

- Ubuntu 22.04/24.04 with `sudo` and working internet/apt mirrors
- Snapshot the VM first if your hypervisor supports it

### Lab environment

Workspace: `~/rebash-linux/lab16`

```bash title="Terminal"
mkdir -p ~/rebash-linux/lab16 && cd ~/rebash-linux/lab16
set -euo pipefail
whoami | tee admin-user.txt
. /etc/os-release
printf '%s\n' "$NAME" "$VERSION_ID" | tee os-release.txt
sudo -n true 2>/dev/null || sudo -v
```

!!! example "Expected output"
    `os-release.txt` shows Ubuntu (or Debian).


### Real-world scenario

Your team standardises a small diagnostic tool on bastion hosts. Change control asks you to install it from the distro repository, record the version, hold it during an application freeze week, then unhold and remove it from a decommissioned practice host — with command output attached to the ticket.

### Step-by-step tasks

#### Task 1 – Update metadata and install `tree`

```bash title="Terminal"
cd ~/rebash-linux/lab16
set -euo pipefail

sudo apt-get update -y | tee apt-update.txt
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tree | tee apt-install-tree.txt

command -v tree | tee tree-path.txt
tree --version | tee tree-version.txt
test -x "$(command -v tree)"
```

!!! example "Expected output"
    `tree` is on `PATH`; `tree-version.txt` shows a version string.


#### Task 2 – Query policy, files, and hold

```bash title="Terminal"
cd ~/rebash-linux/lab16
set -euo pipefail

apt-cache policy tree | tee apt-policy-tree.txt
dpkg -l tree | tee dpkg-l-tree.txt
dpkg -L tree | head -n 40 | tee dpkg-L-tree-head.txt
grep -E '/usr/bin/tree|/bin/tree' dpkg-L-tree-head.txt

sudo apt-mark hold tree | tee apt-hold.txt
apt-mark showhold | tee apt-showhold.txt
grep -qx tree apt-showhold.txt

# Simulate “would upgrade” awareness
apt-get -s upgrade 2>/dev/null | tee apt-sim-upgrade.txt || true
```

!!! example "Expected output"
    policy shows an installed version; `apt-showhold.txt` lists `tree`.


#### Task 3 – Unhold, remove, evidence pack

```bash title="Terminal"
cd ~/rebash-linux/lab16
set -euo pipefail

sudo apt-mark unhold tree | tee apt-unhold.txt
sudo DEBIAN_FRONTEND=noninteractive apt-get remove -y tree | tee apt-remove-tree.txt

# Confirm removed from PATH (or not a regular file)
if command -v tree >/dev/null 2>&1; then
  echo "WARN: tree still on PATH — check other packages" | tee tree-after-remove.txt
else
  echo "tree removed from PATH" | tee tree-after-remove.txt
fi
dpkg -l tree 2>&1 | tee dpkg-after-remove.txt || true

# Optional clean of unused deps (safe on practice VM)
sudo DEBIAN_FRONTEND=noninteractive apt-get autoremove -y | tee apt-autoremove.txt || true

# Note other families for the ticket (documentation only)
cat > other-distros.txt << 'EOF'
RHEL-like: sudo dnf install -y tree && rpm -q tree && sudo dnf remove -y tree
SUSE:      sudo zypper install -y tree && rpm -q tree
EOF

tar -czf package-evidence.tgz \
  admin-user.txt os-release.txt apt-update.txt apt-install-tree.txt \
  tree-path.txt tree-version.txt apt-policy-tree.txt dpkg-l-tree.txt \
  dpkg-L-tree-head.txt apt-hold.txt apt-showhold.txt apt-sim-upgrade.txt \
  apt-unhold.txt apt-remove-tree.txt tree-after-remove.txt \
  dpkg-after-remove.txt apt-autoremove.txt other-distros.txt
ls -l package-evidence.tgz | tee evidence-ls.txt
```

!!! example "Expected output"
    hold removed; package removed (or marked not installed); `package-evidence.tgz` exists.


### Validation steps

- [ ] `apt-get update` completed without repository errors
- [ ] `tree` installed and version recorded, then removed
- [ ] `apt-mark hold` / `unhold` proven in output files
- [ ] `package-evidence.tgz` exists under `~/rebash-linux/lab16`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Unable to locate package` | Stale cache / wrong suite | `sudo apt-get update`; check `/etc/apt/sources.list` |
| `Could not get lock` | Another apt process | Wait for unattended-upgrades; `ps aux \| grep apt` |
| Hold ignored in some tools | Used wrong mark command | Use `apt-mark hold`; verify with `apt-mark showhold` |
| Removed package still “installed” | Config left behind | Use `apt-get purge` if you also want config removed |
| Breaks on production | Broad `upgrade` | Use staged patches and snapshots |

### Challenge exercise

Install `jq`, record `apt-cache policy jq` and `jq --version`, hold `jq`, prove hold with `apt-mark showhold`, then unhold and remove `jq`. Save outputs as `challenge-jq-*.txt` in the lab directory.

### Learning outcomes

- Installed and queried a distro package with apt/dpkg
- Used apt hold/unhold during a simulated freeze
- Removed the package and packed ticket evidence
- Mapped apt actions to dnf/zypper for other distros

### Cleanup

```bash title="Terminal"
cd ~/rebash-linux/lab16
set -euo pipefail
sudo apt-mark unhold tree 2>/dev/null || true
sudo apt-mark unhold jq 2>/dev/null || true
sudo DEBIAN_FRONTEND=noninteractive apt-get remove -y tree jq 2>/dev/null || true
# Keep package-evidence.tgz if you want it
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab16/`
- [ ] You can explain apt vs dnf vs zypper at a high level
- [ ] You know why kernel upgrades often need a reboot
- [ ] You can describe the risk of never patching vs holding forever

## Code Walkthrough

Production package hygiene usually follows:

1. **Refresh** metadata before install  
2. **Install** from trusted distro/repos only  
3. **Record** versions in image builds or tickets  
4. **Hold** only with an expiry plan  
5. **Patch** in windows; reboot for kernel changes  

Configuration management (Ansible, cloud-init) should own desired packages.

## Security Considerations

- Prefer official mirrors and signed repositories  
- Review third-party apt sources before adding them  
- Patch regularly; track Common Vulnerabilities and Exposures (CVE) for critical packages  
- Do not run random install scripts from the internet as root  
- Limit who can run package installs with sudo rules  

## Common Mistakes

!!! warning "Skipping apt-get update"
    You install stale or missing packages. **Fix:** always update metadata first on practice and in automation.

!!! warning "Permanent holds with no review"
    Security fixes never arrive. **Fix:** document holds and remove them after the freeze.

!!! warning "curl \| bash installers for system tools"
    Hard to audit and reverse. **Fix:** prefer distro packages or verified artefacts.

!!! warning "Forgetting reboot after kernel update"
    Host still runs the old kernel. **Fix:** plan reboot; confirm with `uname -r`.

## Best Practices

- Build golden images with required packages baked in  
- Use unattended security updates carefully on servers  
- Keep a short allow-list of approved packages for bastions  
- Prefer `DEBIAN_FRONTEND=noninteractive` in scripts  
- Clean unused packages to shrink attack surface  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Hash sum mismatch | Mirror glitch | Retry `apt-get update`; switch mirror if needed |
| Unmet dependencies | Mixed releases / broken pins | Read apt error; avoid mixing suites |
| `dpkg was interrupted` | Partial upgrade | `sudo dpkg --configure -a` |
| Package held back | Hold or phased updates | `apt-mark showhold`; read apt notes |
| Wrong package name | Distro difference | Search (`apt-cache search`, `dnf search`) |

## Summary

Package managers keep Linux software installable, queryable, and patchable. On Ubuntu, practise `apt-get update`, install, `apt-cache policy`, `apt-mark hold`, and clean removal — then map the same ideas to `dnf` and `zypper`. Next, schedule recurring work in [Scheduling with cron, at, and Timers](scheduling-cron-at-and-timers.md).

## Interview Questions

**1. What problem does a package manager solve compared with copying binaries by hand?**

??? success "Reveal answer"
    It tracks **versions**, **dependencies**, and **installed files**, and it uses signed repositories. That makes installs repeatable, upgrades safer, and removal cleaner than dropping unknown binaries into `/usr/local`.

**2. What is the difference between `apt-get update` and `apt-get upgrade`?**

??? success "Reveal answer"
    **`update`** refreshes package **metadata** (what versions are available). **`upgrade`** installs newer versions of packages already on the system. You usually update first, then upgrade in a planned window.

**3. How do you stop one package from upgrading during a freeze week on Ubuntu?**

??? success "Reveal answer"
    Use `sudo apt-mark hold packagename`, verify with `apt-mark showhold`, and document why. After the freeze, `apt-mark unhold packagename` and patch. Do not hold critical security packages forever without a plan.

**4. Why do kernel package updates often require a reboot?**

??? success "Reveal answer"
    The running kernel is already loaded in memory. Installing a new kernel package updates files on disk, but the host keeps running the old kernel until reboot. Confirm with `uname -r` after reboot.

**5. How would you find which package owns `/usr/bin/curl` on Ubuntu vs RHEL?**

??? success "Reveal answer"
    On Ubuntu/Debian: `dpkg -S /usr/bin/curl`. On RHEL-like systems: `rpm -qf /usr/bin/curl`. This helps when a file is broken or you need to reinstall the correct package.

**6. When are snap or Flatpak appropriate on a server?**

??? success "Reveal answer"
    Rarely for classic server daemons. They are more common for desktop apps. Many production servers prefer apt/dnf packages or containers for isolation. If snap is unused, teams often disable it to reduce complexity.

**7. How do golden images and package management work together in cloud fleets?**

??? success "Reveal answer"
    Bake a known package set into the image (and record versions). Instances launch consistent. Patching then happens via new images or controlled in-place upgrades. This beats unique “snowflake” hosts where someone installed tools by hand months ago.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [SSH and Remote Access](ssh-and-remote-access.md) *(previous)*
- [Scheduling with cron, at, and Timers](scheduling-cron-at-and-timers.md) *(next)*
- [Lab — Linux Ops Toolkit](../labs/linux-ops-toolkit-lab.md) *(more practice)*

## References

- [Ubuntu APT documentation](https://ubuntu.com/server/docs/package-management) — package management overview  
- [`apt-get(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/apt-get.8.html) — apt-get manual  
- [`apt-mark(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/apt-mark.8.html) — hold/unhold  
- [DNF documentation](https://dnf.readthedocs.io/) — RHEL-family package manager  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
