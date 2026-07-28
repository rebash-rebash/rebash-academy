#!/usr/bin/env python3
"""DEPRECATED: Linux tutorials are hand-authored in docs/linux/.

This script generated shallow template content and must not be re-run
without overwriting production-quality tutorials. Kept for reference only.
"""

import sys

print("ERROR: This generator is deprecated. Linux tutorials are manually authored.", file=sys.stderr)
sys.exit(1)

# Legacy generator code removed — see git history if needed.

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

DOCS_LINUX = Path(__file__).resolve().parent.parent / "docs" / "linux"
AUTHOR = "Shaik Basha"

# (slug, title, description, difficulty, time, tag, module)
CURRICULUM = [
    ("introduction-to-linux", "Introduction to Linux", "Understand Linux history, architecture, distributions, and the boot process.", "beginner", "30 min", "fundamentals", 1),
    ("linux-filesystem-hierarchy", "Linux Filesystem Hierarchy", "Navigate the FHS — /etc, /var, /home, /usr, and where everything lives.", "beginner", "25 min", "filesystem", 1),
    ("essential-linux-commands", "Essential Linux Commands", "Master ls, cd, cp, mv, rm, find, and everyday CLI workflows.", "beginner", "40 min", "commands", 1),
    ("file-permissions-and-ownership", "File Permissions and Ownership", "Learn chmod, chown, umask, and POSIX permission models.", "beginner", "35 min", "permissions", 2),
    ("user-and-group-management", "User and Group Management", "Create and manage users, groups, sudo, and login policies.", "beginner", "35 min", "users", 2),
    ("process-management", "Process Management", "Monitor and control processes with ps, top, kill, nice, and signals.", "intermediate", "40 min", "processes", 3),
    ("systemd-service-management", "systemd Service Management", "Manage services with systemctl — start, stop, enable, and unit files.", "intermediate", "45 min", "systemd", 3),
    ("package-management", "Package Management", "Install and manage software with apt, dnf, and rpm.", "beginner", "35 min", "packages", 3),
    ("text-processing-grep-sed-awk", "Text Processing with grep, sed, and awk", "Filter, transform, and report on text data from the command line.", "intermediate", "50 min", "text-processing", 4),
    ("shell-scripting-fundamentals", "Shell Scripting Fundamentals", "Write Bash scripts with variables, loops, conditionals, and functions.", "intermediate", "60 min", "shell-scripting", 4),
    ("ssh-remote-administration", "SSH and Remote Administration", "Secure remote access with SSH keys, config, and tunneling.", "intermediate", "40 min", "ssh", 5),
    ("remote-systemd-services", "Remote systemd Service Control", "Manage systemd units on remote servers with systemctl --host and polkit.", "intermediate", "45 min", "systemd", 5),
    ("disk-and-filesystem-management", "Disk and Filesystem Management", "Manage partitions, mounts, LVM basics, df, du, and fstab.", "intermediate", "45 min", "storage", 6),
    ("log-management-journalctl", "Log Management with journalctl", "Read, filter, and persist logs using systemd journal.", "intermediate", "35 min", "logging", 6),
    ("cron-and-task-scheduling", "Cron and Task Scheduling", "Schedule jobs with cron, at, and systemd timers.", "beginner", "30 min", "scheduling", 6),
    ("environment-variables-shell-config", "Environment Variables and Shell Configuration", "Configure shells with .bashrc, PATH, and export.", "beginner", "25 min", "shell", 6),
    ("linux-networking-essentials", "Linux Networking Essentials", "Configure interfaces, DNS, routing, and troubleshoot connectivity.", "intermediate", "45 min", "networking", 6),
    ("file-archiving-and-compression", "File Archiving and Compression", "Archive and compress files with tar, gzip, and zip.", "beginner", "25 min", "archives", 6),
    ("linux-security-hardening-basics", "Linux Security Hardening Basics", "Apply baseline hardening — firewalls, SSH, updates, and auditing.", "advanced", "50 min", "security", 6),
    ("troubleshooting-linux-systems", "Troubleshooting Linux Systems", "Systematic debugging for boot, disk, network, and performance issues.", "advanced", "55 min", "troubleshooting", 6),
]

MODULES = {
    1: "Foundations",
    2: "Users, Groups & Permissions",
    3: "Processes, Services & Packages",
    4: "Text Processing & Shell Scripting",
    5: "Remote Administration",
    6: "Storage, Logs, Networking & Operations",
}


def related_links(slug: str) -> str:
    idx = next(i for i, t in enumerate(CURRICULUM) if t[0] == slug)
    links = ["- [Linux – Category Overview](index.md)"]
    if idx > 0:
        prev = CURRICULUM[idx - 1]
        links.append(f"- [{prev[1]}]({prev[0]}.md) *(previous)*")
    if idx < len(CURRICULUM) - 1:
        nxt = CURRICULUM[idx + 1]
        links.append(f"- [{nxt[1]}]({nxt[0]}.md) *(next)*")
    links.append("- [Learning Paths – DevOps Engineer](../learning-paths/index.md)")
    return "\n".join(links)


def lab_steps(slug: str) -> str:
    """Return topic-specific hands-on lab content."""
    labs: dict[str, str] = {
        "introduction-to-linux": dedent("""
            ### Step 1 – Identify your distribution

            ```bash
            cat /etc/os-release
            uname -a
            hostnamectl
            ```

            ### Step 2 – Explore the boot process

            ```bash
            systemd-analyze
            systemd-analyze blame | head -10
            ```

            ### Step 3 – Locate key directories

            ```bash
            ls -la /
            ls /etc /var /home /usr
            ```
        """),
        "linux-filesystem-hierarchy": dedent("""
            ### Step 1 – Explore root directories

            ```bash
            ls -l /
            tree -L 1 / 2>/dev/null || ls -la /
            ```

            ### Step 2 – Inspect configuration and logs

            ```bash
            ls /etc | head -20
            ls -la /var/log | head -10
            ```

            ### Step 3 – Find user and application data

            ```bash
            echo $HOME
            ls -la ~
            ls /usr/bin | wc -l
            ```
        """),
        "essential-linux-commands": dedent("""
            ### Step 1 – Navigation and listing

            ```bash
            pwd
            cd /tmp && ls -lah
            cd ~ && ls -lt | head
            ```

            ### Step 2 – Create, copy, move, delete

            ```bash
            mkdir -p ~/lab/demo && cd ~/lab/demo
            echo "REBASH Academy" > readme.txt
            cp readme.txt readme.bak
            mv readme.bak backup.txt
            ```

            ### Step 3 – Search the filesystem

            ```bash
            find ~ -name "*.txt" 2>/dev/null
            find /etc -type f -name "*.conf" 2>/dev/null | head -5
            ```
        """),
        "file-permissions-and-ownership": dedent("""
            ### Step 1 – Inspect permissions

            ```bash
            ls -l /etc/passwd
            ls -ld /tmp /root
            stat /etc/shadow
            ```

            ### Step 2 – Change permissions

            ```bash
            cd ~/lab/demo
            chmod 644 readme.txt
            chmod u+x readme.txt
            ls -l readme.txt
            ```

            ### Step 3 – Change ownership (requires sudo)

            ```bash
            sudo chown $USER:$USER ~/lab/demo/readme.txt
            umask
            umask 022
            ```
        """),
        "user-and-group-management": dedent("""
            ### Step 1 – View users and groups

            ```bash
            id
            getent passwd | tail -5
            getent group | grep -E "sudo|wheel"
            ```

            ### Step 2 – Create a test user (requires sudo)

            ```bash
            sudo useradd -m -s /bin/bash labuser
            sudo passwd labuser
            id labuser
            ```

            ### Step 3 – Manage group membership

            ```bash
            sudo usermod -aG users labuser
            groups labuser
            sudo userdel -r labuser
            ```
        """),
        "process-management": dedent("""
            ### Step 1 – List processes

            ```bash
            ps aux | head -10
            ps -ef | grep ssh
            top -b -n 1 | head -20
            ```

            ### Step 2 – Monitor in real time

            ```bash
            htop  # or top
            pgrep -l bash
            ```

            ### Step 3 – Send signals

            ```bash
            sleep 300 &
            kill -0 $!
            kill $!
            ```
        """),
        "systemd-service-management": dedent("""
            ### Step 1 – Inspect services

            ```bash
            systemctl list-units --type=service --state=running | head
            systemctl status ssh 2>/dev/null || systemctl status sshd
            ```

            ### Step 2 – Control a service (nginx example)

            ```bash
            sudo systemctl status nginx 2>/dev/null || echo "Install nginx to practice"
            sudo systemctl is-enabled nginx 2>/dev/null
            ```

            ### Step 3 – View unit files

            ```bash
            systemctl cat ssh 2>/dev/null || systemctl cat sshd
            systemctl list-unit-files --type=service | head -10
            ```
        """),
        "package-management": dedent("""
            ### Step 1 – Update package index

            === "Ubuntu / Debian"

                ```bash
                sudo apt update
                apt list --upgradable 2>/dev/null | head -5
                ```

            === "RHEL / Fedora"

                ```bash
                sudo dnf check-update 2>/dev/null | head -5
                ```

            ### Step 2 – Install and remove packages

            === "Ubuntu / Debian"

                ```bash
                sudo apt install -y tree
                tree --version
                sudo apt remove -y tree
                ```

            ### Step 3 – Search packages

            === "Ubuntu / Debian"

                ```bash
                apt search nginx 2>/dev/null | head -5
                ```
        """),
        "text-processing-grep-sed-awk": dedent("""
            ### Step 1 – grep patterns

            ```bash
            grep -r "root" /etc/passwd
            grep -E "^[a-z]" /etc/passwd | head -5
            ```

            ### Step 2 – sed transformations

            ```bash
            echo "hello world" | sed 's/world/REBASH/'
            sed -n '1,5p' /etc/passwd
            ```

            ### Step 3 – awk reporting

            ```bash
            awk -F: '{print $1, $3}' /etc/passwd | head -5
            awk '/bash/{print $1}' /etc/passwd
            ```
        """),
        "shell-scripting-fundamentals": dedent("""
            ### Step 1 – Create a simple script

            ```bash
            cat > ~/lab/hello.sh << 'EOF'
            #!/bin/bash
            echo "Hello, $USER"
            echo "Hostname: $(hostname)"
            EOF
            chmod +x ~/lab/hello.sh
            ~/lab/hello.sh
            ```

            ### Step 2 – Variables and conditionals

            ```bash
            cat > ~/lab/check_disk.sh << 'EOF'
            #!/bin/bash
            USAGE=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
            if [ "$USAGE" -gt 80 ]; then
              echo "WARNING: Disk usage is ${USAGE}%"
            else
              echo "OK: Disk usage is ${USAGE}%"
            fi
            EOF
            chmod +x ~/lab/check_disk.sh && ~/lab/check_disk.sh
            ```

            ### Step 3 – Loop through files

            ```bash
            for f in ~/lab/demo/*; do
              [ -f "$f" ] && echo "File: $f"
            done
            ```
        """),
        "ssh-remote-administration": dedent("""
            ### Step 1 – Generate SSH keys

            ```bash
            ssh-keygen -t ed25519 -C "rebash-lab" -f ~/.ssh/rebash_ed25519 -N ""
            ls -la ~/.ssh/rebash_ed25519*
            ```

            ### Step 2 – Configure SSH client

            ```bash
            cat >> ~/.ssh/config << 'EOF'
            Host lab-server
                HostName 127.0.0.1
                User $USER
                IdentityFile ~/.ssh/rebash_ed25519
            EOF
            chmod 600 ~/.ssh/config
            ```

            ### Step 3 – Test connection

            ```bash
            ssh -o BatchMode=yes localhost echo "SSH OK" 2>/dev/null || echo "Configure keys for localhost"
            ```
        """),
        "remote-systemd-services": dedent("""
            ### Step 1 – Create management user (remote server)

            ```bash
            sudo useradd --create-home systemd-manager
            sudo mkdir -p /home/systemd-manager/.ssh
            sudo chmod 700 /home/systemd-manager/.ssh
            ```

            ### Step 2 – Configure SSH keys

            ```bash
            ssh-copy-id -i ~/.ssh/rebash_ed25519.pub systemd-manager@YOUR_SERVER
            ```

            ### Step 3 – Remote status check

            ```bash
            systemctl --host systemd-manager@YOUR_SERVER status sshd
            systemctl --host systemd-manager@YOUR_SERVER --failed
            ```
        """),
        "disk-and-filesystem-management": dedent("""
            ### Step 1 – Check disk usage

            ```bash
            df -h
            df -hT /
            du -sh ~/*
            ```

            ### Step 2 – List block devices

            ```bash
            lsblk
            lsblk -f
            ```

            ### Step 3 – Inspect mounts

            ```bash
            mount | column -t
            cat /etc/fstab
            findmnt /
            ```
        """),
        "log-management-journalctl": dedent("""
            ### Step 1 – View recent logs

            ```bash
            journalctl -n 20 --no-pager
            journalctl -u ssh -n 10 --no-pager 2>/dev/null || journalctl -u sshd -n 10 --no-pager
            ```

            ### Step 2 – Filter by time and priority

            ```bash
            journalctl --since "1 hour ago" --no-pager | tail -10
            journalctl -p err -n 10 --no-pager
            ```

            ### Step 3 – Follow logs live

            ```bash
            journalctl -f &
            sleep 2 && kill $!
            ```
        """),
        "cron-and-task-scheduling": dedent("""
            ### Step 1 – View crontab

            ```bash
            crontab -l 2>/dev/null || echo "No crontab for current user"
            ls -la /etc/cron.*
            ```

            ### Step 2 – Add a test cron job

            ```bash
            (crontab -l 2>/dev/null; echo "*/5 * * * * echo cron-ok >> /tmp/cron-test.log") | crontab -
            crontab -l
            ```

            ### Step 3 – systemd timers

            ```bash
            systemctl list-timers --all | head -10
            ```
        """),
        "environment-variables-shell-config": dedent("""
            ### Step 1 – Inspect environment

            ```bash
            env | sort | head -20
            echo $PATH
            echo $SHELL
            ```

            ### Step 2 – Set variables

            ```bash
            export REBASH_ENV="lab"
            echo $REBASH_ENV
            unset REBASH_ENV
            ```

            ### Step 3 – Shell configuration

            ```bash
            grep -n "PATH" ~/.bashrc 2>/dev/null | head -5
            source ~/.bashrc
            ```
        """),
        "linux-networking-essentials": dedent("""
            ### Step 1 – Interface and IP info

            ```bash
            ip addr show
            ip link show
            hostname -I
            ```

            ### Step 2 – Routing and DNS

            ```bash
            ip route show
            cat /etc/resolv.conf
            ```

            ### Step 3 – Connectivity tests

            ```bash
            ping -c 3 8.8.8.8
            ss -tuln | head -10
            ```
        """),
        "file-archiving-and-compression": dedent("""
            ### Step 1 – Create a tar archive

            ```bash
            cd ~/lab && tar -cvf demo.tar demo/
            ls -lh demo.tar
            ```

            ### Step 2 – Compress with gzip

            ```bash
            tar -czvf demo.tar.gz demo/
            ls -lh demo.tar.gz
            ```

            ### Step 3 – Extract archives

            ```bash
            mkdir -p ~/lab/extract && tar -xzvf demo.tar.gz -C ~/lab/extract
            ls ~/lab/extract
            ```
        """),
        "linux-security-hardening-basics": dedent("""
            ### Step 1 – Check for updates

            ```bash
            sudo apt update 2>/dev/null || sudo dnf check-update 2>/dev/null
            ```

            ### Step 2 – Review SSH configuration

            ```bash
            grep -E "^(PermitRootLogin|PasswordAuthentication|PubkeyAuthentication)" /etc/ssh/sshd_config
            ```

            ### Step 3 – Firewall status

            ```bash
            sudo ufw status 2>/dev/null || sudo firewall-cmd --state 2>/dev/null || echo "Check your firewall tool"
            ```
        """),
        "troubleshooting-linux-systems": dedent("""
            ### Step 1 – System health snapshot

            ```bash
            uptime
            free -h
            df -h
            dmesg | tail -10
            ```

            ### Step 2 – Failed services

            ```bash
            systemctl --failed
            journalctl -p err -b --no-pager | tail -15
            ```

            ### Step 3 – Resource hogs

            ```bash
            ps aux --sort=-%mem | head -5
            ps aux --sort=-%cpu | head -5
            ```
        """),
    }
    return labs.get(slug, "### Step 1 – Practice\n\n```bash\necho \"Complete the lab for this topic\"\n```")


def theory(slug: str, title: str) -> str:
    theories: dict[str, str] = {
        "introduction-to-linux": "Linux is an open-source Unix-like kernel created by Linus Torvalds (1991). Combined with GNU utilities and a package manager, it forms a **Linux distribution** (Ubuntu, RHEL, Debian). The **kernel** manages hardware; **systemd** is PID 1 on most distros and handles boot and services.",
        "linux-filesystem-hierarchy": "The **Filesystem Hierarchy Standard (FHS)** defines where files live. `/etc` holds configuration, `/var` holds variable data (logs, caches), `/home` holds user directories, `/usr` holds user programs, and `/tmp` holds temporary files.",
        "essential-linux-commands": "The Linux CLI is composable — small tools chained with pipes. Master navigation (`cd`, `pwd`), inspection (`ls`, `cat`, `less`), manipulation (`cp`, `mv`, `rm`), and search (`find`, `grep`) first.",
        "file-permissions-and-ownership": "Every file has an **owner**, **group**, and **mode** (read/write/execute for user, group, others). Octal notation (755, 644) maps to rwx bits. **umask** sets default permissions for new files.",
        "user-and-group-management": "Linux is multi-user. `/etc/passwd` stores user accounts; `/etc/group` stores groups. **sudo** grants elevated privileges via `/etc/sudoers`. Principle of least privilege applies in production.",
        "process-management": "A **process** is a running program with a PID. **Signals** (SIGTERM, SIGKILL) control lifecycle. Parent processes spawn children; PID 1 (systemd) adopts orphans.",
        "systemd-service-management": "**systemd** manages units: `.service`, `.socket`, `.timer`, `.mount`. Unit files live in `/usr/lib/systemd/system/` and `/etc/systemd/system/`. Use `systemctl` to control state and `journalctl` for logs.",
        "package-management": "Packages bundle software with metadata and dependencies. **Debian/Ubuntu** use `.deb` and `apt`; **RHEL/Fedora** use `.rpm` and `dnf`. Always pin versions in production and test upgrades in staging.",
        "text-processing-grep-sed-awk": "**grep** filters lines; **sed** streams edits; **awk** is a column-oriented language. Together they replace many spreadsheet tasks on logs and CSV exports.",
        "shell-scripting-fundamentals": "Bash scripts automate repeatable tasks. Start with shebang (`#!/bin/bash`), quote variables, check exit codes (`$?`), and use `set -euo pipefail` in production scripts.",
        "ssh-remote-administration": "**SSH** encrypts remote shell and file transfer. Key-based auth eliminates password brute-force risk. `~/.ssh/config` simplifies multi-host workflows.",
        "remote-systemd-services": "`systemctl --host user@server` runs commands over SSH. **PolicyKit (polkit)** authorizes non-root users to manage specific systemd actions safely.",
        "disk-and-filesystem-management": "Block devices (`/dev/sda1`) are formatted with filesystems (ext4, xfs) and mounted at mount points. **LVM** adds flexibility for resizing volumes. Monitor with `df` and `du`.",
        "log-management-journalctl": "systemd stores logs in the **journal** (binary, structured). `journalctl` queries by unit, time, and priority. Forward to SIEM in production for retention and search.",
        "cron-and-task-scheduling": "**cron** runs commands on schedules (`minute hour day month weekday`). **systemd timers** are the modern alternative with dependency awareness and logging.",
        "environment-variables-shell-config": "Environment variables configure process behavior (`PATH`, `HOME`, `LANG`). Login shells read `/etc/profile`; interactive shells read `~/.bashrc`. Export variables to pass them to child processes.",
        "linux-networking-essentials": "The **ip** command replaces legacy `ifconfig`. DNS resolves names via `/etc/resolv.conf`. **ss** shows listening ports; **ping** and **traceroute** test connectivity.",
        "file-archiving-and-compression": "**tar** bundles files; **gzip** compresses. Common pattern: `tar -czvf archive.tar.gz directory/`. Always verify archives before deleting sources.",
        "linux-security-hardening-basics": "Hardening layers: patch management, minimal services, firewall rules, SSH hardening, audit logging, and file integrity monitoring. CIS benchmarks provide checklists.",
        "troubleshooting-linux-systems": "Use a systematic approach: reproduce → isolate → collect evidence (logs, metrics) → hypothesize → test fix → document. The **USE method** (Utilization, Saturation, Errors) helps performance debugging.",
    }
    return theories.get(slug, f"Core concepts for **{title}** in Linux administration.")


def commands_table(slug: str) -> str:
    tables: dict[str, str] = {
        "introduction-to-linux": "| `uname -a` | Kernel and architecture info |\n| `cat /etc/os-release` | Distribution details |\n| `systemd-analyze` | Boot time analysis |",
        "essential-linux-commands": "| `ls -lah` | Detailed listing |\n| `find /path -name '*.log'` | Search by name |\n| `man cmd` | Manual page |",
        "systemd-service-management": "| `systemctl start UNIT` | Start service |\n| `systemctl enable UNIT` | Enable at boot |\n| `systemctl daemon-reload` | Reload unit files |",
        "process-management": "| `ps aux` | All processes |\n| `kill -15 PID` | Graceful terminate |\n| `nice -n 10 cmd` | Lower priority |",
    }
    default = "| `man <topic>` | Official documentation |\n| `--help` | Command quick help |"
    return tables.get(slug, default)


def interview_questions(slug: str, title: str) -> str:
    common = [
        f"What is the purpose of **{title.lower()}** in Linux administration?",
        "Which log files or commands would you use to verify this works correctly?",
        "What security considerations apply in a production environment?",
        "How does this topic relate to the DevOps engineer learning path?",
    ]
    return "\n".join(f"{i}. {q}" for i, q in enumerate(common, 1))


def architecture_diagram(slug: str) -> str:
    if slug == "introduction-to-linux":
        return dedent("""
            ```d2
            direction: down
            A: "Bootloader GRUB"
            B: "Linux Kernel"
            C: "systemd PID 1"
            D: Services
            E: "Login / Shell"
            F: "User Applications"
            A -> B
            B -> C
            C -> D
            C -> E
            E -> F
            ```
        """)
    if slug == "linux-filesystem-hierarchy":
        return dedent("""
            ```d2
            direction: down
            R: "/ Root"
            etc: "/etc Config"
            var: "/var Logs & Data"
            home: "/home Users"
            usr: "/usr Programs"
            tmp: "/tmp Temporary"
            R -> etc
            R -> var
            R -> home
            R -> usr
            R -> tmp
            ```
        """)
    if slug == "systemd-service-management":
        return dedent("""
            ```d2
            direction: right
            A: systemctl
            B: systemd
            C: "Unit Files"
            D: "Running Services"
            E: "journald Logs"
            A -> B
            B -> C
            B -> D
            B -> E
            ```
        """)
    if slug == "remote-systemd-services":
        return dedent("""
            ```d2
            direction: right
            A: "Local systemctl --host"
            B: "Remote Server"
            C: "polkit Auth"
            D: systemd
            E: Services
            A -> B: SSH
            B -> C
            C -> D
            D -> E
            ```
        """)
    return dedent("""
        ```d2
        direction: right
        A: Admin
        B: "Linux CLI"
        C: "System Resources"
        D: "Logs & Monitoring"
        A -> B
        B -> C
        C -> D
        ```
    """)


def render_tutorial(entry: tuple) -> str:
    slug, title, description, difficulty, time, tag, module = entry
    mod_name = MODULES[module]
    prereq = "Basic computer literacy"
    if module > 1:
        prereq = f"Complete Module {module - 1} tutorials or equivalent experience"
    if difficulty == "advanced":
        prereq = "Completion of Modules 1–5 Linux tutorials"

    body = f"""---
title: {title}
description: {description}
difficulty: {difficulty}
estimated_time: "{time}"
author: {AUTHOR}
category: linux
tags:
  - linux
  - {tag}
prerequisites:
  - {prereq}
comments: false
---

# {title}

## Overview

{description}

This tutorial is part of **Module {module}: {mod_name}** in the REBASH Academy Linux series.
It follows our [documentation standards](../about.md#documentation-standards) with theory,
hands-on labs, and interview preparation.

## Prerequisites

- {prereq}
- A Linux VM, cloud instance, or local machine with terminal access
- `sudo` privileges for lab exercises marked accordingly

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the core concepts of {title.lower()}
- [ ] Run essential commands in a hands-on lab environment
- [ ] Apply best practices suitable for production systems
- [ ] Troubleshoot common issues related to this topic

## Architecture Diagram

{architecture_diagram(slug).strip()}

## Theory

{theory(slug, title)}

## Hands-on Lab

{lab_steps(slug).strip()}

## Commands

| Command | Description |
|---------|-------------|
{commands_table(slug)}

## Code

```bash
# Quick reference script — customize for your environment
#!/bin/bash
set -euo pipefail
echo "=== {title} ==="
echo "Host: $(hostname)"
echo "User: $(whoami)"
echo "Date: $(date -Iseconds)"
```

## Common Mistakes

!!! warning "Skipping manual pages"
    Always read `man <command>` — flags differ between distributions.

!!! warning "Running destructive commands as root"
    Double-check `rm -rf`, disk operations, and user deletion commands before executing.

## Best Practices

!!! tip "Test in staging first"
    Validate changes on a non-production system before applying to live servers.

!!! tip "Automate repeat tasks"
    Once you master the manual steps, capture them in scripts or configuration management.

!!! tip "Document changes"
    Maintain runbooks for operations your team performs regularly.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Permission denied | Insufficient privileges | Use `sudo` or switch to appropriate user |
| Command not found | Package not installed | Install via apt/dnf; check `$PATH` |
| Service failed | Config error or dependency | Run `journalctl -u UNIT -n 30` |
| Changes not persistent | Edited wrong file or no reload | Verify path; restart service or re-login |

## Summary

- You completed **{title}** in the REBASH Academy Linux curriculum
- Module {module} ({mod_name}) builds job-ready Linux administration skills
- Continue with the next tutorial in sequence for structured progress

## Interview Questions

{interview_questions(slug, title)}

## Related Tutorials

{related_links(slug)}

## References

- [Linux man pages online](https://man7.org/linux/man-pages/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- [systemd documentation](https://www.freedesktop.org/wiki/Software/systemd/)
- [REBASH Academy – Linux Overview](index.md)
"""
    return body


def main() -> None:
    DOCS_LINUX.mkdir(parents=True, exist_ok=True)
    nav_lines = ["title: Linux", "icon: material/linux", "nav:", "  - index.md"]

    for entry in CURRICULUM:
        slug = entry[0]
        path = DOCS_LINUX / f"{slug}.md"
        path.write_text(render_tutorial(entry), encoding="utf-8")
        nav_lines.append(f"  - {slug}.md")
        print(f"Created: {path.name}")

    pages = DOCS_LINUX / ".pages"
    pages.write_text("\n".join(nav_lines) + "\n", encoding="utf-8")
    print(f"Updated: {pages}")


if __name__ == "__main__":
    main()
