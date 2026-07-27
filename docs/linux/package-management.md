---
title: Package Management
description: Install, update, and pin software on Debian/Ubuntu (apt) and RHEL/Fedora (dnf) with repository management and version holding.
difficulty: beginner
estimated_time: "50 min"
author: Shaik Basha
category: linux
tags:
  - linux
  - packages
  - apt
  - dnf
  - repositories
prerequisites:
  - Complete systemd Service Management or equivalent experience
  - sudo privileges on a Debian or RHEL-family system
comments: false
---

# Package Management

## Overview

Linux distributions ship software as **packages** — archives bundled with binaries, configuration files, metadata, and dependency declarations. Package managers resolve dependencies, verify signatures, and maintain a consistent system state. The two dominant families are **Debian/Ubuntu** (`.deb`, `apt`) and **RHEL/Fedora** (`.rpm`, `dnf`).

This tutorial is part of **Module 3: Processes, Services & Packages** in the REBASH Academy Linux series. You will update package indexes, install and remove software, search repositories, add third-party repos safely, and **hold/pin** package versions for production stability.

## Prerequisites

- Complete [systemd Service Management](systemd-service-management.md) or equivalent experience
- A Linux VM running Ubuntu/Debian **or** RHEL/Fedora (labs show both where commands differ)
- `sudo` privileges for install/remove operations
- Network access to distribution mirrors

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Update package indexes and apply system upgrades with apt and dnf
- [ ] Install, remove, and query packages including dependencies
- [ ] Search repositories and inspect package metadata before installation
- [ ] Add and manage third-party repositories with proper signing keys
- [ ] Hold or pin package versions to prevent unintended upgrades
- [ ] Troubleshoot broken dependencies, cache corruption, and GPG key errors


## Theory

### Package manager responsibilities

| Function | Description |
|----------|-------------|
| Dependency resolution | Install required libraries automatically |
| Integrity verification | Check GPG signatures and checksums |
| Upgrade path | Replace old versions while preserving config |
| Removal tracking | Remove files owned by package; optional config purge |
| Index caching | Local copy of available packages and versions |

### apt vs dnf comparison

| Task | Debian/Ubuntu (apt) | RHEL/Fedora (dnf) |
|------|---------------------|-------------------|
| Update index | `apt update` | `dnf check-update` |
| Upgrade all | `apt upgrade` | `dnf upgrade` |
| Install | `apt install PKG` | `dnf install PKG` |
| Remove | `apt remove PKG` | `dnf remove PKG` |
| Search | `apt search TERM` | `dnf search TERM` |
| Info | `apt show PKG` | `dnf info PKG` |
| List installed | `apt list --installed` | `dnf list installed` |
| Local install | `dpkg -i file.deb` | `dnf install file.rpm` |
| Hold version | `apt-mark hold PKG` | `dnf versionlock add PKG` |

### Repository configuration

**Debian/Ubuntu** — files in `/etc/apt/sources.list` and `/etc/apt/sources.list.d/`:

```
deb http://archive.ubuntu.com/ubuntu noble main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu noble-security main restricted universe multiverse
```

**RHEL/Fedora** — files in `/etc/yum.repos.d/*.repo`:

```ini
[baseos]
name=BaseOS
baseurl=https://cdn.redhat.com/...
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
```

Always verify GPG keys when adding third-party repositories.

### Version holding in production

Uncontrolled upgrades cause the classic "it worked yesterday" failure. Strategies:

| Family | Hold command | Release hold |
|--------|--------------|--------------|
| apt | `apt-mark hold nginx` | `apt-mark unhold nginx` |
| apt (pin) | `/etc/apt/preferences.d/` pin file | Remove pin file |
| dnf | `dnf versionlock add nginx` | `dnf versionlock delete nginx` |

Combine holds with staging environments that test upgrades before production rollout.

### Low-level tools

Package managers wrap lower-level tools:

- **dpkg** / **rpm**: Direct install/remove of individual packages
- **apt** / **dnf**: Dependency resolution and repository access

Use low-level tools only when the high-level manager cannot resolve a conflict — and document the exception.

## Hands-on Lab

Use the tabbed sections matching your distribution.

### Step 1 – Update the package index

=== "Ubuntu / Debian"

    ```bash
    sudo apt update
    apt list --upgradable 2>/dev/null | head -8
    ```

    **Expected output:**

    ```
    Hit:1 http://archive.ubuntu.com/ubuntu noble InRelease
    Reading package lists... Done
    Listing... Done
    curl/noble-updates 8.5.0-2ubuntu10.2 amd64 [upgradable from: 8.5.0-2ubuntu10.1]
    ...
    ```

=== "RHEL / Fedora"

    ```bash
    sudo dnf check-update 2>/dev/null | head -8
    sudo dnf makecache
    ```

    **Expected output:**

    ```
    Last metadata expiration check: 0:00:01 ago on Mon 27 Jul 2026 02:00:00 PM UTC.
    curl.x86_64    8.5.0-1.fc40    updates
    ...
    Metadata cache created.
    ```

### Step 2 – Install a package and verify

=== "Ubuntu / Debian"

    ```bash
    sudo apt install -y tree
    tree --version
    dpkg -l tree | tail -1
    ```

    **Expected output:**

    ```
    tree v2.1.1 © 1996-2023 by Steve Baker, Florian Sesser, Kyosuke Tokoro
    ii  tree  2.1.1-2ubuntu3  amd64  displays an indented directory tree
    ```

=== "RHEL / Fedora"

    ```bash
    sudo dnf install -y tree
    tree --version
    rpm -q tree
    ```

    **Expected output:**

    ```
    tree v2.1.1 ...
    tree-2.1.1-1.fc40.x86_64
    ```

### Step 3 – Search and inspect package metadata

=== "Ubuntu / Debian"

    ```bash
    apt search "^nginx$" 2>/dev/null | head -5
    apt show nginx 2>/dev/null | head -15
    ```

    **Expected output:**

    ```
    Sorting... Done
    nginx/noble-updates 1.24.0-2ubuntu7.3 amd64
      small, powerful, scalable web/proxy server
    Package: nginx
    Version: 1.24.0-2ubuntu7.3
    Priority: optional
    ...
    ```

=== "RHEL / Fedora"

    ```bash
    dnf search nginx 2>/dev/null | head -5
    dnf info nginx 2>/dev/null | head -15
    ```

    **Expected output:**

    ```
    nginx.x86_64 : A high performance web server
    Available Packages
    nginx.x86_64    1:1.24.0-4.fc40    fedora
    Name         : nginx
    Version      : 1.24.0
    ...
    ```

### Step 4 – Remove a package (keep configs vs purge)

=== "Ubuntu / Debian"

    ```bash
    sudo apt remove -y tree
    dpkg -l tree 2>/dev/null | tail -1 || echo "tree not installed"
    sudo apt install -y tree
    sudo apt purge -y tree
    dpkg -l tree 2>/dev/null | tail -1 || echo "tree fully removed"
    ```

    **Expected output:**

    ```
    rc  tree  2.1.1-2ubuntu3  amd64  (config files remain after remove)
    tree fully removed
    ```

    `rc` status means removed but config files remain; `purge` deletes configs.

=== "RHEL / Fedora"

    ```bash
    sudo dnf remove -y tree
    rpm -q tree 2>&1 || echo "tree not installed"
    ```

    **Expected output:**

    ```
    package tree is not installed
    tree not installed
    ```

### Step 5 – List installed packages and find file owner

=== "Ubuntu / Debian"

    ```bash
    apt list --installed 2>/dev/null | wc -l
    dpkg -S /bin/ls
    ```

    **Expected output:**

    ```
    612
    coreutils: /bin/ls
    ```

=== "RHEL / Fedora"

    ```bash
    dnf list installed 2>/dev/null | wc -l
    rpm -qf /bin/ls
    ```

    **Expected output:**

    ```
    580
    coreutils-9.4-2.fc40.x86_64
    ```

### Step 6 – Hold a package version

=== "Ubuntu / Debian"

    ```bash
    sudo apt install -y curl
    CURL_VER=$(apt list --installed curl 2>/dev/null | cut -d/ -f2 | cut -d' ' -f1)
    echo "Installed curl version: $CURL_VER"
    sudo apt-mark hold curl
    apt-mark showhold
    sudo apt-mark unhold curl
    ```

    **Expected output:**

    ```
    Installed curl version: 8.5.0-2ubuntu10.1
    curl
    Canceled hold on curl.
    ```

=== "RHEL / Fedora"

    ```bash
    sudo dnf install -y python3-dnf-plugin-versionlock 2>/dev/null || true
    sudo dnf install -y curl
    sudo dnf versionlock add curl
    dnf versionlock list
    sudo dnf versionlock delete curl
    ```

    **Expected output:**

    ```
    Added versionlock on: curl-0:8.5.0-...
    curl-0:8.5.0-1.fc40.*
    Deleted versionlock on: curl-0:8.5.0-...
    ```

### Step 7 – Inspect repository configuration

=== "Ubuntu / Debian"

    ```bash
    ls /etc/apt/sources.list.d/
    grep -r ^deb /etc/apt/sources.list /etc/apt/sources.list.d/ 2>/dev/null | head -5
    apt-cache policy nginx 2>/dev/null | head -10
    ```

    **Expected output:**

    ```
    ubuntu.sources
    /etc/apt/sources.list.d/ubuntu.sources: ...
    nginx:
      Installed: (none)
      Candidate: 1.24.0-2ubuntu7.3
         500 http://archive.ubuntu.com/ubuntu noble-updates/universe amd64 Packages
    ```

=== "RHEL / Fedora"

    ```bash
    ls /etc/yum.repos.d/
    grep -E "^\[|^baseurl" /etc/yum.repos.d/fedora.repo 2>/dev/null | head -6
    dnf info nginx 2>/dev/null | grep -E "Repo|Version"
    ```

    **Expected output:**

    ```
    fedora.repo
    fedora-updates.repo
    [fedora]
    baseurl=https://mirrors.fedoraproject.org/...
    Repo         : fedora
    Version      : 1.24.0
    ```

### Step 8 – Clean caches and verify disk recovery

=== "Ubuntu / Debian"

    ```bash
    du -sh /var/cache/apt/archives/
    sudo apt clean
    du -sh /var/cache/apt/archives/
    sudo apt autoremove -y
    ```

    **Expected output:**

    ```
    45M /var/cache/apt/archives/
    28K /var/cache/apt/archives/
    0 upgraded, 0 newly installed, 2 to remove
    ```

=== "RHEL / Fedora"

    ```bash
    sudo dnf clean all
    sudo dnf autoremove -y
    ```

    **Expected output:**

    ```
    17 files removed
    Nothing to do.
    ```

## Commands

| Command | Description |
|---------|-------------|
| `apt update` | Refresh package index from repositories |
| `apt upgrade` | Install available upgrades for installed packages |
| `apt install PKG` | Install package and dependencies |
| `apt remove PKG` | Remove package, keep config files |
| `apt purge PKG` | Remove package and configuration files |
| `apt search TERM` | Search package names and descriptions |
| `apt show PKG` | Display detailed package metadata |
| `apt list --installed` | List all installed packages |
| `apt-mark hold PKG` | Prevent package from being upgraded |
| `apt-mark unhold PKG` | Release version hold |
| `apt-cache policy PKG` | Show installed and candidate versions |
| `dpkg -l PKG` | List package status (ii, rc, etc.) |
| `dpkg -S /path/file` | Find which package owns a file |
| `dnf check-update` | Check for available updates |
| `dnf install PKG` | Install package and dependencies |
| `dnf remove PKG` | Remove package |
| `dnf search TERM` | Search repositories |
| `dnf info PKG` | Show package details |
| `dnf list installed` | List installed packages |
| `dnf versionlock add PKG` | Pin package version (plugin required) |
| `rpm -qf /path/file` | Query which package owns a file |
| `rpm -q PKG` | Query installed package version |

## Code Examples

### apt pin file for version lock

```
# /etc/apt/preferences.d/nginx-pin
Package: nginx
Pin: version 1.24.0-2ubuntu7.3
Pin-Priority: 1001
```

Priority above 1000 prevents downgrade protection from blocking the pin.

### Pre-flight upgrade script (apt)

```bash
#!/bin/bash
# safe-apt-upgrade.sh — update, hold check, upgrade with logging
set -euo pipefail

LOG="/var/log/apt-upgrade-$(date +%Y%m%d).log"

{
  echo "=== $(date -Iseconds) Starting upgrade ==="
  apt update
  echo "=== Held packages ==="
  apt-mark showhold
  echo "=== Upgradable ==="
  apt list --upgradable
  DEBIAN_FRONTEND=noninteractive apt upgrade -y
  echo "=== Complete ==="
} >> "$LOG" 2>&1

echo "Upgrade log: $LOG"
```

### Install from local package with dependency fix (apt)

```bash
#!/bin/bash
# install-local-deb.sh — install .deb and resolve deps
set -euo pipefail

DEB="${1:?Usage: $0 package.deb}"

dpkg -i "$DEB" || true
apt-get install -f -y   # fix broken dependencies
dpkg -l "$(dpkg-deb -f "$DEB" Package)" | tail -1
```

### dnf exclude in repo config

```ini
# Prevent kernel updates on sensitive production nodes
[updates]
exclude=kernel* linux-firmware
```

## Common Mistakes

!!! warning "Running dist-upgrade blindly in production"
    `apt dist-upgrade` and `dnf upgrade --refresh` may remove packages or change dependencies. Test in staging; review the change list.

!!! warning "Adding unsigned or untrusted repositories"
    Disabling GPG check (`gpgcheck=0`) or `--allow-unauthenticated` exposes systems to supply-chain attacks.

!!! warning "Mixing dpkg -i without apt-get install -f"
    Manual `dpkg -i` can leave broken dependencies. Always follow with `apt-get install -f`.

!!! warning "Forgetting to unhold before needed security patch"
    Held packages skip security updates. Document holds in configuration management and review quarterly.

## Best Practices

!!! tip "Automate with idempotent configuration management"
    Use Ansible (`apt`/`dnf` modules), Puppet, or cloud-init for reproducible package state across fleets.

!!! tip "Pin critical infrastructure packages"
    Hold nginx, docker, kernel, or database client versions until tested in staging.

!!! tip "Schedule updates during maintenance windows"
    Combine `unattended-upgrades` (Debian) or `dnf-automatic` (RHEL) with reboot policies for kernel patches.

!!! tip "Verify before install"
    Always `apt show` or `dnf info` to confirm version, origin repo, and dependencies.

!!! tip "Snapshot or backup before major upgrades"
    VM snapshot, LVM snapshot, or AMI backup before kernel/glibc upgrades enables fast rollback.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Unable to locate package` | Wrong name, disabled repo, or outdated index | Run `apt update` / `dnf makecache`; check repo config |
| `GPG error` / signature failure | Missing or expired repository key | Import key: `apt-key` or `/etc/apt/keyrings/`; verify repo docs |
| Broken dependencies | Partial install or mixed repos | `apt-get install -f` or `dnf distro-sync` |
| `Held packages` block upgrade | apt-mark hold active | Review `apt-mark showhold`; unhold if patch needed |
| Disk full during install | `/var/cache` bloated | `apt clean` or `dnf clean all`; expand disk |
| Wrong package version installed | Multiple repos with different priorities | `apt-cache policy PKG`; adjust pin or repo priority |
| dnf versionlock not found | Plugin not installed | `dnf install python3-dnf-plugin-versionlock` |

## Summary

- **apt** (Debian/Ubuntu) and **dnf** (RHEL/Fedora) manage `.deb` and `.rpm` packages with dependency resolution.
- Always **update the index** before install or upgrade; review upgradable packages first.
- Use **search** and **show/info** to inspect packages before installation.
- **Hold/pin** critical package versions in production; test upgrades in staging.
- Repository configuration lives in `/etc/apt/sources.list.d/` and `/etc/yum.repos.d/` — verify GPG signatures on all third-party repos.

## Interview Questions

**1. What is the difference between apt remove and apt purge?**

*Sample answer:* `remove` uninstalls the package but leaves configuration files in `/etc`. `purge` removes the package and its configuration files. `dpkg -l` shows `rc` status after remove (removed, config remains).

**2. How do you prevent a package from being upgraded on Ubuntu?**

*Sample answer:* `sudo apt-mark hold packagename`. Verify with `apt-mark showhold`. Release with `apt-mark unhold`. Alternative: apt preference pin file in `/etc/apt/preferences.d/`.

**3. What does apt update do vs apt upgrade?**

*Sample answer:* `update` refreshes the local package index from repositories — no packages are installed. `upgrade` installs newer versions of currently installed packages based on the updated index.

**4. How do you find which package owns a specific file?**

*Sample answer:* On Debian: `dpkg -S /path/to/file`. On RHEL: `rpm -qf /path/to/file`.

**5. How do you add a third-party apt repository safely?**

*Sample answer:* Download and store the GPG key in `/etc/apt/keyrings/`, create a `sources.list.d` entry referencing the signed-by keyring, run `apt update`, and verify with `apt-cache policy`.

**6. What is dnf versionlock used for?**

*Sample answer:* It pins installed packages to their current version, preventing `dnf upgrade` from updating them. Requires the versionlock plugin. Used for production stability on critical packages.

**7. What happens when you run dpkg -i on a .deb with unmet dependencies?**

*Sample answer:* dpkg installs the package but may leave the system in a broken state. Run `apt-get install -f` to resolve and install missing dependencies automatically.

**8. How do you list all available updates without installing them?**

*Sample answer:* Debian: `apt list --upgradable` after `apt update`. RHEL: `dnf check-update` (exit code 100 means updates available).

**9. What is the purpose of GPG checking on repositories?**

*Sample answer:* GPG signatures verify packages come from the trusted repository maintainer and have not been tampered with in transit. Never disable GPG check in production.

**10. How would you roll back a bad package upgrade?**

*Sample answer:* Debian: install specific older version with `apt install package=version` if still in cache/repo. RHEL: `dnf downgrade package` or `dnf history undo LAST`. Best practice: restore from snapshot/backup.

## Related Tutorials

- [Linux – Category Overview](index.md)
- [systemd Service Management](systemd-service-management.md) *(previous)*
- [Text Processing with grep, sed, and awk](text-processing-grep-sed-awk.md) *(next)*
- [Essential Linux Commands](essential-linux-commands.md)
- [Troubleshooting Linux Systems](troubleshooting-linux-systems.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [Debian apt documentation](https://wiki.debian.org/Apt)
- [Ubuntu manpages – apt](https://manpages.ubuntu.com/manpages/noble/man8/apt.8.html)
- [Red Hat – Managing software with dnf](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/managing_software/index)
- [dnf man page](https://man7.org/linux/man-pages/man8/dnf.8.html)
- [REBASH Academy – Linux Overview](index.md)
