---
title: Overview
description: "REBASH Linux Mastery — practical Linux for Cloud, DevOps, Kubernetes, and Platform Engineers. 15 modules, production labs, and capstone projects."
difficulty: beginner
estimated_time: "8–10 weeks"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
tags:
  - linux
  - devops
  - cloud
  - platform-engineering
  - kubernetes
  - rebash-linux-mastery
comments: false
---

# REBASH Linux Mastery

**Duration:** 8–10 weeks · **Lessons:** ~145 · **Labs / projects:** 40+ planned · **Capstones:** 8

The most practical Linux course for **Cloud, DevOps, Kubernetes, and Platform Engineers**.
Typical Linux courses stop at basic commands — this path trains **production engineers**.

!!! tip "How this course works"
    Modules build in order. Scaffolded lessons show structure and SEO; full tutorials
    (theory + lab + interview) publish as they are completed. Prefer Ubuntu 22.04/24.04 lab VMs.

## Who this is for

Beginners → Linux administrators → DevOps → Cloud → Platform / SRE engineers who need
Linux that transfers to containers, CI/CD, and cloud operations.

## Learning roadmap

1. **Fundamentals & shell** — Modules 1–2  
2. **Text, files, identity** — Modules 3–5  
3. **Runtime & packages** — Modules 6–7  
4. **Network & storage** — Modules 8–9  
5. **Automation & security** — Modules 10–11  
6. **Observability & DevOps** — Modules 12–13  
7. **Production & capstones** — Modules 14–15  

## Modules

### Module 1 · Linux Fundamentals

**Goal:** Build a strong foundation for Cloud and DevOps Linux work.

**Lab / project focus:** Install Ubuntu Server and explore the filesystem.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [Introduction to Linux](introduction-to-linux.md) | Beginner | Ready |
| 2 | [Linux History and Open Source](linux-history-and-open-source.md) | Beginner | Ready |
| 3 | [Linux Fundamentals — Distributions and Architecture](linux-fundamentals-distributions-and-architecture.md) | Beginner | Ready |
| 4 | [Linux Kernel Explained](linux-kernel-explained.md) | Beginner | Ready |
| 5 | [Linux Desktop vs Server Editions](linux-desktop-vs-server.md) | Beginner | Ready |
| 6 | [Linux Installation (VirtualBox, VMware, WSL)](linux-installation-virtualbox-vmware-wsl.md) | Beginner | Ready |
| 7 | [Linux Boot Process](boot-process-and-filesystem-hierarchy.md) | Beginner | Ready |
| 8 | [First Login and Terminal](first-login-and-terminal.md) | Beginner | Ready |
| 9 | [Linux Directory Structure (FHS)](linux-directory-structure-fhs.md) | Beginner | Ready |
| 10 | [Getting Help (man, info, --help)](getting-help-man-info.md) | Beginner | Ready |
| — | [Module 1 Summary — Linux Fundamentals](module-1-linux-fundamentals-summary.md) | Beginner | Ready |

!!! success "Module 1 complete"
    All ten **Linux Fundamentals** tutorials plus the
    [Module 1 summary](module-1-linux-fundamentals-summary.md) are published.
    Continue with [Understanding the Shell](understanding-the-shell.md) (Module 2).

### Module 2 · Linux Command Line Essentials

**Goal:** Operate confidently in the shell every day.

**Lab / project focus:** Build a mini file management toolkit.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [Understanding the Shell](understanding-the-shell.md) | Beginner | Ready |
| 2 | [Bash Basics](bash-basics.md) | Beginner | Ready |
| 3 | [Navigating the Filesystem](navigating-the-filesystem.md) | Beginner | Ready |
| 4 | [File and Directory Commands](essential-linux-commands.md) | Beginner | Ready |
| 5 | [Viewing File Contents](viewing-file-contents.md) | Beginner | Ready |
| 6 | [Searching Files](searching-files.md) | Beginner | Ready |
| 7 | [Wildcards and Globbing](wildcards-and-globbing.md) | Beginner | Ready |
| 8 | [Command History](command-history.md) | Beginner | Ready |
| 9 | [Input, Output, Pipes, and Redirection](redirection.md) | Intermediate | Ready |
| 10 | [Pipes](pipes.md) | Intermediate | Ready |
| — | [Module 2 Summary — Linux Command Line Essentials](module-2-linux-command-line-essentials-summary.md) | Beginner | Ready |

!!! success "Module 2 complete"
    All ten **Linux Command Line Essentials** tutorials plus the
    [Module 2 summary](module-2-linux-command-line-essentials-summary.md) are published.
    Continue with [cat](text-processing-cat.md) (Module 3 · Text Processing).

### Module 3 · Text Processing

**Goal:** Transform logs and configs with classic Unix filters.

**Lab / project focus:** Analyze web server logs (mini project).


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [cat](text-processing-cat.md) | Beginner | Ready |
| 2 | [grep](text-processing-grep.md) | Intermediate | Ready |
| 3 | [cut](text-processing-cut.md) | Intermediate | Ready |
| 4 | [sort](text-processing-sort.md) | Intermediate | Ready |
| 5 | [uniq](text-processing-uniq.md) | Intermediate | Ready |
| 6 | [tr](text-processing-tr.md) | Intermediate | Ready |
| 7 | [wc](text-processing-wc.md) | Intermediate | Ready |
| 8 | [paste](text-processing-paste.md) | Intermediate | Ready |
| 9 | [join](text-processing-join.md) | Intermediate | Ready |
| 10 | [split](text-processing-split.md) | Intermediate | Ready |
| 11 | [fmt](text-processing-fmt.md) | Intermediate | Ready |
| 12 | [column](text-processing-column.md) | Intermediate | Ready |
| 13 | [strings](text-processing-strings.md) | Intermediate | Ready |
| 14 | [tee](text-processing-tee.md) | Intermediate | Ready |
| 15 | [xargs](text-processing-xargs.md) | Intermediate | Ready |
| 16 | [sed](text-processing-sed.md) | Intermediate | Ready |
| 17 | [awk](text-processing-awk.md) | Advanced | Ready |
| 18 | [Regular Expressions](text-processing-regular-expressions.md) | Advanced | Ready |

!!! success "Module 3 complete"
    All eighteen **Text Processing** tutorials are published.
    Continue with [File Types](file-types.md) (Module 4 · File Management and Permissions).

### Module 4 · File Management and Permissions

**Goal:** Understand file types, links, permissions, and secure file operations in production.

**Lab / project focus:** Create and secure a shared directory.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [File Types](file-types.md) | Beginner | Ready |
| 2 | [Hard Links](hard-links.md) | Intermediate | Ready |
| 3 | [Soft Links (Symbolic Links)](soft-links.md) | Intermediate | Ready |
| 4 | [Linux File Permissions](linux-file-permissions.md) | Intermediate | Ready |
| 5 | [Ownership](ownership.md) | Intermediate | Ready |
| 6 | [umask](umask.md) | Intermediate | Ready |
| 7 | [Access Control Lists (ACL)](acl.md) | Advanced | Ready |
| 8 | [File Attributes](file-attributes.md) | Advanced | Ready |
| 9 | [Mount Points](mount-points.md) | Intermediate | Ready |
| 10 | [Disk Usage](disk-usage.md) | Beginner → Intermediate | Ready |
| — | [Module 4 Summary — File Management and Permissions](module-4-file-management-and-permissions-summary.md) | Intermediate | Ready |

!!! success "Module 4 complete"
    All ten **File Management and Permissions** tutorials plus the
    [Module 4 summary](module-4-file-management-and-permissions-summary.md) are published.
    Continue with [Linux Users](linux-users.md) (Module 5 · Users and Groups).

### Module 5 · Users and Groups

**Goal:** Operate multi-user servers with least privilege.

**Lab / project focus:** Configure a secure multi-user Linux server.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [Linux Users](linux-users.md) | Beginner | Ready |
| 2 | [Groups](groups.md) | Beginner | Ready |
| 3 | [sudo](sudo.md) | Beginner → Intermediate | Ready |
| 4 | [Password Policies](password-policies.md) | Beginner → Intermediate | Ready |
| 5 | [Environment Variables](environment-variables.md) | Beginner → Intermediate | Ready |
| 6 | [Profiles](shell-profiles.md) | Beginner → Intermediate | Ready |
| 7 | [Shell Configuration](shell-configuration.md) | Beginner → Intermediate | Ready |
| 8 | [SSH Keys](ssh-keys.md) | Beginner → Intermediate | Ready |
| 9 | [PAM Overview](pam-overview.md) | Advanced | Ready |
| 10 | [Multi-user Environment](multi-user-environment.md) | Beginner → Intermediate | Ready |
| — | [Module 5 Summary — Users and Groups](module-5-users-and-groups-summary.md) | Intermediate | Ready |

!!! success "Module 5 complete"
    All ten **Users and Groups** tutorials plus the
    [Module 5 summary](module-5-users-and-groups-summary.md) are published.
    Continue with [Linux Processes](linux-processes.md) (Module 6 · Process Management).

### Module 6 · Process Management

**Goal:** Control processes and systemd services under load.

**Lab / project focus:** Troubleshoot a failing service.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [Linux Processes](linux-processes.md) | Beginner → Intermediate | Ready |
| 2 | [Foreground and Background Jobs](foreground-background-jobs.md) | Beginner → Intermediate | Ready |
| 3 | [ps](ps.md) | Beginner → Intermediate | Ready |
| 4 | [top](top.md) | Beginner → Intermediate | Ready |
| 5 | [htop](htop.md) | Beginner → Intermediate | Ready |
| 6 | [nice](nice.md) | Beginner → Intermediate | Ready |
| 7 | [kill](kill.md) | Beginner → Intermediate | Ready |
| 8 | [Signals](linux-signals.md) | Beginner → Intermediate | Ready |
| 9 | [systemd](systemd.md) | Beginner → Intermediate | Ready |
| 10 | [Linux Services](linux-services.md) | Beginner → Intermediate | Ready |
| — | [Module 6 Summary — Process Management](module-6-process-management-summary.md) | Intermediate | Ready |

!!! success "Module 6 complete"
    All ten **Process Management** tutorials plus the
    [Module 6 summary](module-6-process-management-summary.md) are published.
    Continue with [APT](apt.md) (Module 7 · Package Management).

### Module 7 · Package Management

**Goal:** Install, patch, and troubleshoot packages safely.

**Lab / project focus:** Apply security patches and verify package provenance.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [APT](apt.md) | Beginner → Intermediate | Ready |
| 2 | [DNF](dnf.md) | Beginner → Intermediate | Ready |
| 3 | [YUM](yum.md) | Beginner → Intermediate | Ready |
| 4 | [RPM](rpm.md) | Beginner → Intermediate | Ready |
| 5 | [Snap](snap.md) | Beginner → Intermediate | Ready |
| 6 | [Flatpak](flatpak.md) | Beginner → Intermediate | Ready |
| 7 | [Repository Management](repository-management.md) | Beginner → Intermediate | Ready |
| 8 | [System Updates](package-updates.md) | Beginner → Intermediate | Ready |
| 9 | [Security Patches](security-patches.md) | Beginner → Intermediate | Ready |
| 10 | [Package Troubleshooting](package-troubleshooting.md) | Beginner → Intermediate | Ready |
| — | [Module 7 Summary — Package Management](module-7-package-management-summary.md) | Intermediate | Ready |

!!! success "Module 7 complete"
    All Module 7 lessons and the
    [Module 7 summary](module-7-package-management-summary.md) are published.
    Continue with [TCP/IP Basics](tcp-ip-basics-for-linux.md) (Module 8 · Networking).

### Module 8 · Networking

**Goal:** Diagnose connectivity and secure remote access.

**Lab / project focus:** Configure SSH access between servers.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [TCP/IP Basics](tcp-ip-basics-for-linux.md) | Beginner → Intermediate | Ready |
| 2 | [IP Configuration](linux-networking-tools.md) | Beginner → Intermediate | Ready |
| 3 | [DNS](dns-on-linux.md) | Beginner → Intermediate | Ready |
| 4 | [Routing](routing-on-linux.md) | Beginner → Intermediate | Ready |
| 5 | [ping](ping.md) | Beginner → Intermediate | Ready |
| 6 | [traceroute](traceroute.md) | Beginner → Intermediate | Ready |
| 7 | [ss](ss.md) | Beginner → Intermediate | Ready |
| 8 | [netstat](netstat.md) | Beginner → Intermediate | Ready |
| 9 | [curl](curl.md) | Beginner → Intermediate | Ready |
| 10 | [wget](wget.md) | Beginner → Intermediate | Ready |
| 11 | [SSH](ssh-and-remote-access.md) | Beginner → Intermediate | Ready |
| 12 | [SCP](scp.md) | Beginner → Intermediate | Ready |
| 13 | [rsync](rsync.md) | Beginner → Intermediate | Ready |
| — | [Module 8 Summary — Networking](module-8-networking-summary.md) | Intermediate | Ready |

!!! success "Module 8 complete"
    All Module 8 lessons and the
    [Module 8 summary](module-8-networking-summary.md) are published.
    Continue with [Partitions](storage-disks-partitions-and-filesystems.md) (Module 9 · Storage Management).

### Module 9 · Storage Management

**Goal:** Partition, mount, and protect data for production hosts.

**Lab / project focus:** Build LVM volumes with a backup and restore drill.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [Partitions](storage-disks-partitions-and-filesystems.md) | Beginner → Intermediate | Ready |
| 2 | [Filesystems](filesystems.md) | Beginner → Intermediate | Ready |
| 3 | [mkfs](mkfs.md) | Beginner → Intermediate | Ready |
| 4 | [Mounting](mounting.md) | Beginner → Intermediate | Ready |
| 5 | [LVM](lvm-swap-and-disk-monitoring.md) | Beginner → Advanced | Ready |
| 6 | [RAID Concepts](raid-concepts.md) | Beginner → Intermediate | Ready |
| 7 | [Swap](swap.md) | Beginner → Intermediate | Ready |
| 8 | [Quotas](quotas.md) | Beginner → Intermediate | Ready |
| 9 | [Backup Basics](backup-basics.md) | Beginner → Intermediate | Ready |
| 10 | [Restore](restore.md) | Beginner → Intermediate | Ready |
| — | [Module 9 Summary — Storage Management](module-9-storage-management-summary.md) | Intermediate | Ready |

!!! success "Module 9 complete"
    All Module 9 lessons and the
    [Module 9 summary](module-9-storage-management-summary.md) are published.
    Continue with [Variables](bash-variables.md) (Module 10 · Bash Scripting).

### Module 10 · Bash Scripting

**Goal:** Automate ops tasks with production-safe Bash.

**Lab / project focus:** System health monitoring script (project).


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [Variables](bash-variables.md) | Beginner | Ready |
| 2 | [Conditions](bash-conditions.md) | Beginner → Intermediate | Ready |
| 3 | [Loops](bash-loops.md) | Beginner → Intermediate | Ready |
| 4 | [Functions](bash-functions.md) | Beginner → Intermediate | Ready |
| 5 | [Arrays](bash-arrays.md) | Beginner → Intermediate | Ready |
| 6 | [Input](bash-input.md) | Beginner → Intermediate | Ready |
| 7 | [Exit Codes](bash-exit-codes.md) | Beginner → Intermediate | Ready |
| 8 | [Error Handling](bash-error-handling.md) | Beginner → Advanced | Ready |
| 9 | [Logging](bash-logging.md) | Beginner → Intermediate | Ready |
| 10 | [Script Best Practices](bash-script-best-practices.md) | Beginner → Advanced | Ready |
| — | [Module 10 Summary — Bash Scripting](module-10-bash-scripting-summary.md) | Intermediate | Ready |

!!! success "Module 10 complete"
    All Module 10 lessons and the
    [Module 10 summary](module-10-bash-scripting-summary.md) are published.
    Continue with [SSH Hardening](ssh-hardening.md) (Module 11 · Linux Security).

### Module 11 · Linux Security

**Goal:** Harden hosts to a production baseline.

**Lab / project focus:** Apply SSH hardening, firewall, and Fail2Ban.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [SSH Hardening](ssh-hardening.md) | Beginner → Advanced | Ready |
| 2 | [File Permissions Review](file-permissions-security-review.md) | Beginner → Intermediate | Ready |
| 3 | [Firewall (UFW)](firewall-ufw.md) | Beginner → Intermediate | Ready |
| 4 | [SELinux Overview](selinux-overview.md) | Beginner → Advanced | Ready |
| 5 | [AppArmor](apparmor.md) | Beginner → Intermediate | Ready |
| 6 | [Fail2Ban](fail2ban.md) | Beginner → Intermediate | Ready |
| 7 | [Audit Logs](audit-logs.md) | Beginner → Advanced | Ready |
| 8 | [Security Updates](security-updates.md) | Beginner → Intermediate | Ready |
| 9 | [Secrets Management](secrets-management-on-linux.md) | Beginner → Advanced | Ready |
| 10 | [CIS Benchmark Basics](cis-benchmark-basics.md) | Beginner → Advanced | Ready |
| — | [Module 11 Summary — Linux Security](module-11-linux-security-summary.md) | Intermediate | Ready |

!!! success "Module 11 complete"
    All Module 11 lessons and the
    [Module 11 summary](module-11-linux-security-summary.md) are published.
    Continue with [journalctl](journalctl.md) (Module 12 · Monitoring and Logs).

### Module 12 · Monitoring and Logs

**Goal:** Investigate incidents with logs and host metrics.

**Lab / project focus:** Trace a crash from journalctl to resource pressure.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [journalctl](journalctl.md) | Beginner → Intermediate | Ready |
| 2 | [syslog](syslog.md) | Beginner → Intermediate | Ready |
| 3 | [dmesg](dmesg.md) | Beginner → Intermediate | Ready |
| 4 | [logrotate](logrotate.md) | Beginner → Intermediate | Ready |
| 5 | [Disk Monitoring](disk-monitoring.md) | Beginner → Intermediate | Ready |
| 6 | [Memory Monitoring](memory-monitoring.md) | Beginner → Intermediate | Ready |
| 7 | [CPU Monitoring](cpu-monitoring.md) | Beginner → Intermediate | Ready |
| 8 | [Performance Troubleshooting](performance-troubleshooting.md) | Beginner → Advanced | Ready |
| 9 | [Crash Investigation](crash-investigation.md) | Beginner → Advanced | Ready |
| 10 | [Monitoring Best Practices](monitoring-best-practices.md) | Beginner → Advanced | Ready |
| — | [Module 12 Summary — Monitoring & Logs](module-12-monitoring-and-logs-summary.md) | Intermediate | Ready |

!!! success "Module 12 complete"
    All Module 12 lessons and the
    [Module 12 summary](module-12-monitoring-and-logs-summary.md) are published.
    Continue with [Linux for Docker](linux-for-docker.md) (Module 13 · Linux for DevOps).

### Module 13 · Linux for DevOps

**Goal:** Connect Linux skills to Docker, Kubernetes, CI/CD, and cloud.

**Lab / project focus:** Trace a container issue back to namespaces, cgroups, and networking.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [Linux for Docker](linux-for-docker.md) | Beginner → Advanced | Ready |
| 2 | [Linux for Kubernetes](linux-for-kubernetes.md) | Beginner → Advanced | Ready |
| 3 | [Linux for CI/CD](linux-for-cicd.md) | Beginner → Advanced | Ready |
| 4 | [Linux for Git](linux-for-git.md) | Beginner → Advanced | Ready |
| 5 | [Linux for Terraform](linux-for-terraform.md) | Beginner → Advanced | Ready |
| 6 | [Linux for Ansible](linux-for-ansible.md) | Beginner → Advanced | Ready |
| 7 | [Linux for Jenkins](linux-for-jenkins.md) | Beginner → Advanced | Ready |
| 8 | [Linux for GitHub Actions](linux-for-github-actions.md) | Beginner → Advanced | Ready |
| 9 | [Linux for GitLab CI](linux-for-gitlab-ci.md) | Beginner → Advanced | Ready |
| 10 | [Linux in Cloud Platforms](linux-in-cloud-platforms.md) | Beginner → Advanced | Ready |
| — | [Module 13 Summary — Linux for DevOps](module-13-linux-for-devops-summary.md) | Intermediate | Ready |

!!! success "Module 13 complete"
    All Module 13 lessons and the
    [Module 13 summary](module-13-linux-for-devops-summary.md) are published.
    Continue with [Production Checklist](production-checklist.md) (Module 14 · Production Linux Administration).

### Module 14 · Production Linux Administration

**Goal:** Run Linux like a platform team in production.

**Lab / project focus:** Complete a production readiness and incident drill.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [Production Checklist](production-checklist.md) | Beginner → Advanced | Ready |
| 2 | [Hardening Checklist](hardening-checklist.md) | Beginner → Advanced | Ready |
| 3 | [Performance Tuning](performance-tuning.md) | Beginner → Advanced | Ready |
| 4 | [Capacity Planning](capacity-planning.md) | Beginner → Advanced | Ready |
| 5 | [Backup Strategy](backup-strategy.md) | Beginner → Advanced | Ready |
| 6 | [Disaster Recovery](disaster-recovery.md) | Beginner → Advanced | Ready |
| 7 | [High Availability Concepts](high-availability-concepts.md) | Beginner → Advanced | Ready |
| 8 | [Incident Response](incident-response.md) | Beginner → Advanced | Ready |
| 9 | [Troubleshooting Methodology](troubleshooting-methodology.md) | Beginner → Advanced | Ready |
| 10 | [Best Practices](production-best-practices.md) | Beginner → Advanced | Ready |
| — | [Module 14 Summary — Production Linux Administration](module-14-production-linux-administration-summary.md) | Intermediate | Ready |

!!! success "Module 14 complete"
    All Module 14 lessons and the
    [Module 14 summary](module-14-production-linux-administration-summary.md) are published.
    Continue with [Build a Secure Linux Web Server](projects/secure-linux-web-server.md) (Module 15 · Capstone Projects).

## Capstone projects (Module 15)

| Project | Status |
|---------|--------|
| [Build a Secure Linux Web Server](projects/secure-linux-web-server.md) | Ready |
| [Configure a Bastion Host](projects/bastion-host.md) | Ready |
| [Deploy a Git Server](projects/deploy-git-server.md) | Ready |
| [Create a Monitoring Server](projects/monitoring-server.md) | Ready |
| [Automate User Provisioning with Bash](projects/automate-user-provisioning-bash.md) | Ready |
| [Build a Linux Server Baseline](projects/linux-server-baseline.md) | Ready |
| [Harden an Ubuntu Server](projects/harden-ubuntu-server.md) | Ready |
| [Production Linux Troubleshooting Challenge](projects/production-linux-troubleshooting-challenge.md) | Ready |

!!! success "Module 15 complete"
    All eight Module 15 capstone projects are published.
    Finish with [Production Linux Troubleshooting Challenge](projects/production-linux-troubleshooting-challenge.md).

## Prerequisites

Basic computer literacy. A disposable Ubuntu LTS (or Rocky/RHEL) VM with snapshots.

## Related

- [Linux Administrator learning path](../learning-paths/linux-administrator/index.md)
- [DevOps Engineer learning path](../learning-paths/devops-engineer/index.md)
- [Linux cheat sheet](../cheatsheets/linux.md)
- [Linux interview prep](../interview/linux.md)
