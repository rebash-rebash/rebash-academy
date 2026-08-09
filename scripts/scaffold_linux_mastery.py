#!/usr/bin/env python3
"""Scaffold REBASH Linux Mastery (15 modules) — stubs + nav + curriculum wiring.

Existing full tutorials are reused as anchors when titles/slugs align.
New lessons get SEO-ready stub pages. Bodies are filled when tutorials are supplied.
"""

from __future__ import annotations

from pathlib import Path
import re
import textwrap

ROOT = Path(__file__).resolve().parent.parent
LINUX = ROOT / "docs" / "linux"
CURRICULUM = ROOT / "curriculum.yaml"

# Existing file → keep as this lesson slug (do not overwrite body)
REUSE: dict[str, str] = {
    "linux-fundamentals-distributions-and-architecture": "linux-fundamentals-distributions-and-architecture.md",
    "linux-boot-process": "boot-process-and-filesystem-hierarchy.md",
    "essential-linux-commands": "essential-linux-commands.md",
    "environment-variables-and-profiles": "environment-variables-shell-config.md",
    "disk-usage": "disk-usage-and-file-attributes.md",
    "users": "users-groups-and-sudo.md",
    "permissions": "permissions-acls-and-special-bits.md",
    "filesystem-file-types": "filesystem-paths-links-mounts-and-inodes.md",
    "processes": "process-management.md",
    "systemd-services": "systemd-services-and-journalctl.md",
    "linux-services": "systemd-targets-timers-and-boot.md",
    "apt": "package-management.md",
    "ssh": "ssh-and-remote-access.md",
    "partitions": "storage-disks-partitions-and-filesystems.md",
    "lvm": "lvm-swap-and-disk-monitoring.md",
    "ssh-hardening": "ssh-hardening-and-firewalls.md",
    "selinux-overview": "selinux-apparmor-fail2ban-auditd-pam.md",
    "journalctl": "logging-syslog-journald-logrotate.md",
    "disk-monitoring": "host-monitoring-vmstat-iostat-sar.md",
    "linux-for-docker": "containers-namespaces-cgroups-and-oci.md",
    "troubleshooting-methodology": "troubleshooting-linux-systems.md",
    "production-checklist": "production-linux-hardening-and-performance.md",
    "backup-strategy": "backup-disaster-recovery-and-capacity.md",
    "bash-variables": "shell-scripting-fundamentals.md",
    "ip-configuration": "linux-networking-tools.md",
}

MODULES: list[dict] = [
    {
        "id": "linux-m1",
        "title": "Module 1 · Linux Fundamentals",
        "goal": "Build a strong foundation for Cloud and DevOps Linux work.",
        "lab": "Install Ubuntu Server and explore the filesystem.",
        "lessons": [
            ("introduction-to-linux", "Introduction to Linux", "beginner"),
            ("linux-history-and-open-source", "Linux History and Open Source", "beginner"),
            ("linux-fundamentals-distributions-and-architecture", "Linux Fundamentals — Distributions and Architecture", "beginner"),
            ("linux-kernel-explained", "Linux Kernel Explained", "beginner"),
            ("linux-desktop-vs-server", "Linux Desktop vs Server Editions", "beginner"),
            ("linux-installation-virtualbox-vmware-wsl", "Linux Installation (VirtualBox, VMware, WSL)", "beginner"),
            ("linux-boot-process", "Linux Boot Process", "beginner"),
            ("first-login-and-terminal", "First Login and Terminal", "beginner"),
            ("linux-directory-structure-fhs", "Linux Directory Structure (FHS)", "beginner"),
            ("getting-help-man-info", "Getting Help (man, info, --help)", "beginner"),
        ],
    },
    {
        "id": "linux-m2",
        "title": "Module 2 · Linux Command Line Essentials",
        "goal": "Operate confidently in the shell every day.",
        "lab": "Build a mini file management toolkit.",
        "lessons": [
            ("understanding-the-shell", "Understanding the Shell", "beginner"),
            ("bash-basics", "Bash Basics", "beginner"),
            ("navigating-the-filesystem", "Navigating the Filesystem", "beginner"),
            ("essential-linux-commands", "File and Directory Commands", "beginner"),
            ("viewing-file-contents", "Viewing File Contents", "beginner"),
            ("searching-files", "Searching Files", "beginner"),
            ("wildcards-and-globbing", "Wildcards and Globbing", "beginner"),
            ("command-history", "Command History", "beginner"),
            ("redirection", "Redirection", "beginner"),
            ("pipes", "Pipes", "beginner"),
        ],
    },
    {
        "id": "linux-m3",
        "title": "Module 3 · Text Processing",
        "goal": "Transform logs and configs with classic Unix filters.",
        "lab": "Analyze web server logs (mini project).",
        "lessons": [
            ("text-processing-cat", "cat (Quick Review)", "beginner"),
            ("text-processing-grep", "grep", "beginner"),
            ("text-processing-cut", "cut", "beginner"),
            ("text-processing-sort", "sort", "beginner"),
            ("text-processing-uniq", "uniq", "beginner"),
            ("text-processing-tr", "tr", "beginner"),
            ("text-processing-wc", "wc", "beginner"),
            ("text-processing-paste", "paste", "beginner"),
            ("text-processing-join", "join", "intermediate"),
            ("text-processing-split", "split", "beginner"),
            ("text-processing-fmt", "fmt", "beginner"),
            ("text-processing-column", "column", "beginner"),
            ("text-processing-strings", "strings", "beginner"),
            ("text-processing-tee", "tee", "beginner"),
            ("text-processing-xargs", "xargs", "intermediate"),
            ("text-processing-sed", "sed", "intermediate"),
            ("text-processing-awk", "awk", "intermediate"),
            ("text-processing-regular-expressions", "Regular Expressions", "intermediate"),
        ],
    },
    {
        "id": "linux-m4",
        "title": "Module 4 · File System",
        "goal": "Understand files, links, permissions, and mounts in production.",
        "lab": "Create and secure a shared directory.",
        "lessons": [
            ("filesystem-file-types", "File Types", "beginner"),
            ("hard-links", "Hard Links", "beginner"),
            ("soft-links", "Soft Links (Symbolic Links)", "beginner"),
            ("permissions", "Permissions", "beginner"),
            ("ownership", "Ownership", "beginner"),
            ("umask", "umask", "beginner"),
            ("acl", "Access Control Lists (ACL)", "intermediate"),
            ("file-attributes", "File Attributes", "intermediate"),
            ("mount-points", "Mount Points", "intermediate"),
            ("disk-usage", "Disk Usage", "beginner"),
        ],
    },
    {
        "id": "linux-m5",
        "title": "Module 5 · Users and Groups",
        "goal": "Operate multi-user servers with least privilege.",
        "lab": "Configure a secure multi-user Linux server.",
        "lessons": [
            ("users", "Users", "beginner"),
            ("groups", "Groups", "beginner"),
            ("sudo", "sudo", "beginner"),
            ("password-policies", "Password Policies", "intermediate"),
            ("environment-variables-and-profiles", "Environment Variables", "beginner"),
            ("shell-profiles", "Profiles", "beginner"),
            ("shell-configuration", "Shell Configuration", "beginner"),
            ("ssh-keys", "SSH Keys", "intermediate"),
            ("pam-overview", "PAM Overview", "intermediate"),
            ("multi-user-environment", "Multi-user Environment", "intermediate"),
        ],
    },
    {
        "id": "linux-m6",
        "title": "Module 6 · Process Management",
        "goal": "Control processes and systemd services under load.",
        "lab": "Troubleshoot a failing service.",
        "lessons": [
            ("processes", "Processes", "beginner"),
            ("foreground-background-jobs", "Foreground and Background Jobs", "beginner"),
            ("ps", "ps", "beginner"),
            ("top", "top", "beginner"),
            ("htop", "htop", "beginner"),
            ("nice", "nice", "intermediate"),
            ("kill", "kill", "beginner"),
            ("linux-signals", "Signals", "intermediate"),
            ("systemd-services", "systemd", "intermediate"),
            ("linux-services", "Services", "intermediate"),
        ],
    },
    {
        "id": "linux-m7",
        "title": "Module 7 · Package Management",
        "goal": "Install, patch, and troubleshoot packages safely.",
        "lab": "Apply security patches and verify package provenance.",
        "lessons": [
            ("apt", "APT", "beginner"),
            ("dnf", "DNF", "beginner"),
            ("yum", "YUM", "beginner"),
            ("rpm", "RPM", "intermediate"),
            ("snap", "Snap", "beginner"),
            ("flatpak", "Flatpak", "beginner"),
            ("repository-management", "Repository Management", "intermediate"),
            ("package-updates", "Updates", "beginner"),
            ("security-patches", "Security Patches", "intermediate"),
            ("package-troubleshooting", "Package Troubleshooting", "intermediate"),
        ],
    },
    {
        "id": "linux-m8",
        "title": "Module 8 · Networking",
        "goal": "Diagnose connectivity and secure remote access.",
        "lab": "Configure SSH access between servers.",
        "lessons": [
            ("tcp-ip-basics-for-linux", "TCP/IP Basics", "beginner"),
            ("ip-configuration", "IP Configuration", "beginner"),
            ("dns-on-linux", "DNS", "beginner"),
            ("routing-on-linux", "Routing", "intermediate"),
            ("ping", "ping", "beginner"),
            ("traceroute", "traceroute", "beginner"),
            ("ss", "ss", "beginner"),
            ("netstat", "netstat", "beginner"),
            ("curl", "curl", "beginner"),
            ("wget", "wget", "beginner"),
            ("ssh", "SSH", "beginner"),
            ("scp", "SCP", "beginner"),
            ("rsync", "rsync", "intermediate"),
        ],
    },
    {
        "id": "linux-m9",
        "title": "Module 9 · Storage Management",
        "goal": "Partition, mount, and protect data for production hosts.",
        "lab": "Build LVM volumes with a backup and restore drill.",
        "lessons": [
            ("partitions", "Partitions", "intermediate"),
            ("filesystems", "Filesystems", "intermediate"),
            ("mkfs", "mkfs", "intermediate"),
            ("mounting", "Mounting", "intermediate"),
            ("lvm", "LVM", "intermediate"),
            ("raid-concepts", "RAID Concepts", "intermediate"),
            ("swap", "Swap", "beginner"),
            ("quotas", "Quotas", "intermediate"),
            ("backup-basics", "Backup Basics", "intermediate"),
            ("restore", "Restore", "intermediate"),
        ],
    },
    {
        "id": "linux-m10",
        "title": "Module 10 · Bash Scripting",
        "goal": "Automate ops tasks with production-safe Bash.",
        "lab": "System health monitoring script (project).",
        "lessons": [
            ("bash-variables", "Variables", "beginner"),
            ("bash-conditions", "Conditions", "beginner"),
            ("bash-loops", "Loops", "beginner"),
            ("bash-functions", "Functions", "beginner"),
            ("bash-arrays", "Arrays", "intermediate"),
            ("bash-input", "Input", "beginner"),
            ("bash-exit-codes", "Exit Codes", "beginner"),
            ("bash-error-handling", "Error Handling", "intermediate"),
            ("bash-logging", "Logging", "intermediate"),
            ("bash-script-best-practices", "Script Best Practices", "intermediate"),
        ],
    },
    {
        "id": "linux-m11",
        "title": "Module 11 · Linux Security",
        "goal": "Harden hosts to a production baseline.",
        "lab": "Apply SSH hardening, firewall, and Fail2Ban.",
        "lessons": [
            ("ssh-hardening", "SSH Hardening", "intermediate"),
            ("file-permissions-security-review", "File Permissions Review", "beginner"),
            ("firewall-ufw", "Firewall (UFW)", "intermediate"),
            ("selinux-overview", "SELinux Overview", "advanced"),
            ("apparmor", "AppArmor", "intermediate"),
            ("fail2ban", "Fail2Ban", "intermediate"),
            ("audit-logs", "Audit Logs", "intermediate"),
            ("security-updates", "Security Updates", "intermediate"),
            ("secrets-management-on-linux", "Secrets Management", "intermediate"),
            ("cis-benchmark-basics", "CIS Benchmark Basics", "advanced"),
        ],
    },
    {
        "id": "linux-m12",
        "title": "Module 12 · Monitoring and Logs",
        "goal": "Investigate incidents with logs and host metrics.",
        "lab": "Trace a crash from journalctl to resource pressure.",
        "lessons": [
            ("journalctl", "journalctl", "intermediate"),
            ("syslog", "syslog", "beginner"),
            ("dmesg", "dmesg", "beginner"),
            ("logrotate", "logrotate", "intermediate"),
            ("disk-monitoring", "Disk Monitoring", "intermediate"),
            ("memory-monitoring", "Memory Monitoring", "intermediate"),
            ("cpu-monitoring", "CPU Monitoring", "intermediate"),
            ("performance-troubleshooting", "Performance Troubleshooting", "advanced"),
            ("crash-investigation", "Crash Investigation", "advanced"),
            ("monitoring-best-practices", "Monitoring Best Practices", "intermediate"),
        ],
    },
    {
        "id": "linux-m13",
        "title": "Module 13 · Linux for DevOps",
        "goal": "Connect Linux skills to Docker, Kubernetes, CI/CD, and cloud.",
        "lab": "Trace a container issue back to namespaces, cgroups, and networking.",
        "lessons": [
            ("linux-for-docker", "Linux for Docker", "intermediate"),
            ("linux-for-kubernetes", "Linux for Kubernetes", "intermediate"),
            ("linux-for-cicd", "Linux for CI/CD", "intermediate"),
            ("linux-for-git", "Linux for Git", "beginner"),
            ("linux-for-terraform", "Linux for Terraform", "intermediate"),
            ("linux-for-ansible", "Linux for Ansible", "intermediate"),
            ("linux-for-jenkins", "Linux for Jenkins", "intermediate"),
            ("linux-for-github-actions", "Linux for GitHub Actions", "intermediate"),
            ("linux-for-gitlab-ci", "Linux for GitLab CI", "intermediate"),
            ("linux-in-cloud-platforms", "Linux in Cloud Platforms", "intermediate"),
        ],
    },
    {
        "id": "linux-m14",
        "title": "Module 14 · Production Linux Administration",
        "goal": "Run Linux like a platform team in production.",
        "lab": "Complete a production readiness and incident drill.",
        "lessons": [
            ("production-checklist", "Production Checklist", "advanced"),
            ("hardening-checklist", "Hardening Checklist", "advanced"),
            ("performance-tuning", "Performance Tuning", "advanced"),
            ("capacity-planning", "Capacity Planning", "advanced"),
            ("backup-strategy", "Backup Strategy", "advanced"),
            ("disaster-recovery", "Disaster Recovery", "advanced"),
            ("high-availability-concepts", "High Availability Concepts", "advanced"),
            ("incident-response", "Incident Response", "advanced"),
            ("troubleshooting-methodology", "Troubleshooting Methodology", "advanced"),
            ("production-best-practices", "Best Practices", "advanced"),
        ],
    },
]

CAPSTONES = [
    ("secure-linux-web-server", "Build a Secure Linux Web Server"),
    ("bastion-host", "Configure a Bastion Host"),
    ("deploy-git-server", "Deploy a Git Server"),
    ("monitoring-server", "Create a Monitoring Server"),
    ("automate-user-provisioning-bash", "Automate User Provisioning with Bash"),
    ("linux-server-baseline", "Build a Linux Server Baseline"),
    ("harden-ubuntu-server", "Harden an Ubuntu Server"),
    ("production-linux-troubleshooting-challenge", "Production Linux Troubleshooting Challenge"),
]


def slug_to_title_fallback(slug: str) -> str:
    return slug.replace("-", " ").title()


def stub_body(title: str, module: str, goal: str, difficulty: str, est: str, desc: str, status: str) -> str:
    return textwrap.dedent(
        f"""\
        ---
        title: "{title}"
        description: "{desc}"
        difficulty: {difficulty}
        estimated_time: "{est}"
        technology: linux
        module: "{module}"
        learning_paths:
          - linux-administrator
          - devops-engineer
          - cloud-engineer
          - site-reliability-engineer
        skills:
          - linux-fundamentals
        tags:
          - linux
          - devops
          - cloud
          - rebash-linux-mastery
        author: Shaik Basha
        last_updated: "2026-08-09"
        comments: false
        status: {status}
        ---

        # {title}

        !!! note "Tutorial status"
            This lesson is scaffolded for **REBASH Linux Mastery**. Full tutorial content
            (theory, lab, interview questions) will be published next — structure and SEO are ready.

        ## Overview

        {desc}

        **Module goal:** {goal}

        ## Prerequisites

        - A disposable Ubuntu 22.04/24.04 (or RHEL-family) lab VM
        - Completion of earlier lessons in this module (unless this is lesson 1)

        ## Learning Objectives

        - [ ] Explain the core idea of **{title}** in a production Cloud/DevOps context
        - [ ] Run the hands-on checks for this lesson in a lab VM
        - [ ] Relate the topic to Kubernetes, CI/CD, or cloud operations where relevant

        ## Architecture

        _Diagram and mental model — forthcoming._

        ## Theory

        _Production-focused theory — forthcoming._

        ## Hands-on Lab

        _Lab steps — forthcoming._

        ## Validation

        _How you know it worked — forthcoming._

        ## Best Practices

        _Coming soon._

        ## Security Considerations

        _Coming soon._

        ## Troubleshooting

        _Coming soon._

        ## Interview Questions

        _Coming soon._

        ## Summary

        Scaffold ready for the full **{title}** tutorial.

        ## References

        - [Linux course overview](index.md)
        - [Ubuntu Server documentation](https://documentation.ubuntu.com/server/)
        """
    )


def capstone_stub(slug: str, title: str) -> str:
    desc = (
        f"Capstone project: {title} — production-style Linux build for Cloud, DevOps, "
        "and platform engineers."
    )
    return textwrap.dedent(
        f"""\
        ---
        title: "{title}"
        description: "{desc}"
        difficulty: advanced
        estimated_time: "4–8 hours"
        technology: linux
        module: "Module 15 · Capstone Projects"
        learning_paths:
          - linux-administrator
          - devops-engineer
          - cloud-engineer
        tags:
          - linux
          - capstone
          - project
          - devops
        author: Shaik Basha
        last_updated: "2026-08-09"
        comments: false
        status: planned
        ---

        # {title}

        !!! note "Capstone status"
            Scaffolded for **REBASH Linux Mastery**. Full project brief, acceptance criteria,
            and validation checklist will be published with the tutorial series.

        ## Overview

        {desc}

        ## Goals

        - [ ] Design and implement the solution on a disposable lab VM
        - [ ] Document commands and configuration as portfolio evidence
        - [ ] Apply hardening, logging, and recovery habits from Modules 11–14

        ## Deliverables

        _Coming soon._

        ## Acceptance criteria

        _Coming soon._

        ## References

        - [Linux course overview](../index.md)
        """
    )


def ensure_stub(slug: str, title: str, module_title: str, goal: str, difficulty: str) -> tuple[str, str]:
    """Return (filename, status) where status is ready|planned."""
    if slug in REUSE:
        src = LINUX / REUSE[slug]
        if src.exists():
            # Optionally copy to canonical slug if different
            dest_name = f"{slug}.md"
            dest = LINUX / dest_name
            if REUSE[slug] != dest_name and not dest.exists():
                # Keep using existing filename for nav to avoid duplicating content
                return REUSE[slug], "ready"
            return REUSE[slug], "ready"

    path = LINUX / f"{slug}.md"
    if path.exists() and path.stat().st_size > 2000:
        return path.name, "ready"

    desc = (
        f"Learn {title} for Cloud, DevOps, Kubernetes, and platform engineering — "
        f"part of REBASH Linux Mastery ({module_title})."
    ).replace('"', "'")
    est = "35–55 min" if difficulty == "beginner" else "45–70 min" if difficulty != "advanced" else "55–80 min"
    status = "planned"
    path.write_text(stub_body(title, module_title, goal, difficulty, est, desc, status), encoding="utf-8")
    return path.name, status


def write_pages(lesson_nav: list[tuple[str, list[tuple[str, str]]]]) -> None:
    lines = [
        "title: Linux",
        "icon: material/linux",
        "",
        "nav:",
        "  - Overview: index.md",
        "  - Glossary: glossary.md",
    ]
    for module_title, items in lesson_nav:
        lines.append(f'  - "{module_title}":')
        for filename, title in items:
            lines.append(f'    - {title}: {filename}')
        if module_title.startswith("Module 1 ·"):
            lines.append(
                "    - Module 1 Summary — Linux Fundamentals: "
                "module-1-linux-fundamentals-summary.md"
            )
    lines.append('  - "Module 15 · Capstone Projects":')
    for slug, title in CAPSTONES:
        lines.append(f"    - {title}: projects/{slug}.md")
    (LINUX / ".pages").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_index(modules_meta: list[dict], counts: dict) -> None:
    rows = []
    for m in modules_meta:
        rows.append(f"### {m['title']}\n")
        rows.append(f"**Goal:** {m['goal']}\n")
        if m.get("lab"):
            rows.append(f"**Lab / project focus:** {m['lab']}\n")
        rows.append("")
        rows.append("| # | Lesson | Level | Status |")
        rows.append("|---|--------|-------|--------|")
        for i, (fn, title, diff, st) in enumerate(m["rows"], 1):
            link = f"[{title}]({fn})"
            badge = "Ready" if st == "ready" else "Scaffolded"
            rows.append(f"| {i} | {link} | {diff.title()} | {badge} |")
        rows.append("")

    body = f"""---
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

**Duration:** 8–10 weeks · **Lessons:** ~{counts['lessons']} · **Labs / projects:** 40+ planned · **Capstones:** {counts['capstones']}

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

{chr(10).join(rows)}

## Capstone projects (Module 15)

| Project | Status |
|---------|--------|
"""
    for slug, title in CAPSTONES:
        body += f"| [{title}](projects/{slug}.md) | Scaffolded |\n"

    body += """
## Prerequisites

Basic computer literacy. A disposable Ubuntu LTS (or Rocky/RHEL) VM with snapshots.

## Related

- [Linux Administrator learning path](../learning-paths/linux-administrator/index.md)
- [DevOps Engineer learning path](../learning-paths/devops-engineer/index.md)
- [Linux cheat sheet](../cheatsheets/linux.md)
- [Linux interview prep](../interview/linux.md)
"""
    (LINUX / "index.md").write_text(body, encoding="utf-8")


def patch_curriculum(module_blocks: list[dict], tutorial_count: int) -> None:
    text = CURRICULUM.read_text(encoding="utf-8")
    # Replace linux technology modules block through tutorial_count
    pattern = re.compile(
        r"(- id: linux\n  title: Linux\n  status: ready\n  path_prefix: linux/\n  difficulty: beginner\n  modules:\n)"
        r"(?:.*?)"
        r"(  tutorial_count: )\d+(\n- id: shell\n)",
        re.DOTALL,
    )
    modules_yaml = ""
    for m in module_blocks:
        modules_yaml += f"  - id: {m['id']}\n    title: {m['title']}\n    tutorials:\n"
        for tid in m["tutorial_ids"]:
            modules_yaml += f"    - {tid}\n"
    repl = rf"\g<1>{modules_yaml}\g<2>{tutorial_count}\g<3>"
    new_text, n = pattern.subn(repl, text, count=1)
    if n != 1:
        raise SystemExit(f"curriculum.yaml linux block replace failed (matches={n})")
    CURRICULUM.write_text(new_text, encoding="utf-8")


def main() -> None:
    LINUX.mkdir(parents=True, exist_ok=True)
    (LINUX / "projects").mkdir(exist_ok=True)

    lesson_nav: list[tuple[str, list[tuple[str, str]]]] = []
    modules_meta: list[dict] = []
    curriculum_modules: list[dict] = []
    ready = planned = 0

    for mod in MODULES:
        nav_items: list[tuple[str, str]] = []
        rows = []
        tutorial_ids = []
        for slug, title, difficulty in mod["lessons"]:
            filename, status = ensure_stub(slug, title, mod["title"], mod["goal"], difficulty)
            if status == "ready":
                ready += 1
            else:
                planned += 1
            nav_items.append((filename, title))
            rows.append((filename, title, difficulty, status))
            tutorial_ids.append(f"linux/{Path(filename).stem}")
        lesson_nav.append((mod["title"], nav_items))
        modules_meta.append({**mod, "rows": rows})
        curriculum_modules.append(
            {"id": mod["id"], "title": mod["title"], "tutorial_ids": tutorial_ids}
        )

    for slug, title in CAPSTONES:
        path = LINUX / "projects" / f"{slug}.md"
        if not path.exists():
            path.write_text(capstone_stub(slug, title), encoding="utf-8")
            planned += 1

    lesson_count = sum(len(m["tutorial_ids"]) for m in curriculum_modules)
    cap_ids = [f"linux/projects/{slug}" for slug, _ in CAPSTONES]
    curriculum_modules.append(
        {
            "id": "linux-m15",
            "title": "Module 15 · Capstone Projects",
            "tutorial_ids": cap_ids,
        }
    )

    write_pages(lesson_nav)
    write_index(
        modules_meta,
        {"lessons": lesson_count, "capstones": len(CAPSTONES)},
    )
    patch_curriculum(curriculum_modules, lesson_count)

    display = ROOT / "docs" / "_curriculum" / "course-display.yaml"
    dtext = display.read_text(encoding="utf-8")
    dtext = re.sub(
        r"(linux:\n(?:  .*\n)*?  tagline: ).*",
        r'\1Master practical Linux for Cloud, DevOps, Kubernetes, and Platform Engineers — REBASH Linux Mastery.',
        dtext,
        count=1,
    )
    dtext = re.sub(r"(linux:\n(?:  .*\n)*?  labs: )\d+", r"\g<1>40", dtext, count=1)
    dtext = re.sub(r"(linux:\n(?:  .*\n)*?  projects: )\d+", r"\g<1>8", dtext, count=1)
    dtext = re.sub(r"(linux:\n(?:  .*\n)*?  capstones: )\d+", r"\g<1>8", dtext, count=1)
    display.write_text(dtext, encoding="utf-8")

    print(f"ready_anchor={ready} stubs_or_capstones={planned} lessons={lesson_count}")
    print(f"wrote {LINUX / '.pages'}")
    print(f"wrote {LINUX / 'index.md'}")
    print("updated curriculum.yaml linux modules")
    print("updated course-display.yaml linux stats")


if __name__ == "__main__":
    main()
