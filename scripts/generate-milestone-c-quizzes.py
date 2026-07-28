#!/usr/bin/env python3
"""Generate Milestone C quiz pages (Linux, Docker, Kubernetes)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "docs" / "quizzes"


def render_q(
    num: int,
    prompt: str,
    difficulty: str,
    options: dict[str, str],
    correct: str,
    explanation: str,
    concepts: list[str],
) -> str:
    opts = "\n".join(f"- **{k}.** {v}" for k, v in options.items())
    concepts_lines = "\n".join(f"    - {c}" for c in concepts)
    return f"""### Question {num}

{prompt}

**Difficulty:** {difficulty}

**Options:**

{opts}

??? success "Reveal answer"
    **Correct answer: {correct}**

    {explanation}

    **Related concepts**

{concepts_lines}
"""


def wrap_quiz(
    *,
    title: str,
    description: str,
    track_name: str,
    tag: str,
    overview: str,
    objectives: list[str],
    sections: list[tuple[str, list[dict]]],
    study: str,
    interview: str,
    refs: list[str],
    lab_link: str,
    cheat: str,
    interview_link: str,
    track_index: str,
) -> str:
    obj = "\n".join(f"- [ ] {o}" for o in objectives)
    body_sections: list[str] = []
    for section_title, questions in sections:
        body_sections.append(f"## {section_title}\n")
        for q in questions:
            body_sections.append(render_q(**q))
    sections_md = "\n".join(body_sections)
    refs_md = "\n".join(f"{i}. {r}" for i, r in enumerate(refs, 1))
    return f"""---
title: "{title}"
description: "{description}"
difficulty: intermediate
estimated_time: "45–60 min"
passing_score: "70% (28/40)"
author: Shaik Basha
last_updated: "2026-07-28"
category: quizzes
tags:
  - quizzes
  - {tag}
  - assessment
comments: false
---

# {title}

## Quiz Overview

{overview}

| Attribute | Value |
|-----------|--------|
| Topic | {track_name} |
| Questions | 40 |
| Passing score | 70% (28 correct) |
| Estimated time | 45–60 minutes |
| Format | Multiple choice (single answer) |

!!! tip "How to use this quiz"
    Attempt each section without peeking. Use **Reveal answer** only after you commit to a choice. Score yourself honestly — gaps are the point.

## Learning Objectives

This quiz assesses whether you can:

{obj}

{sections_md}
## Score Summary

| Score | Band | Meaning |
|------:|------|---------|
| 36–40 | Excellent | Ready for interviews and labs at this track level |
| 28–35 | Good | Pass — revise weak sections, then retry |
| 20–27 | Needs improvement | Revisit tutorials for missed topics before labs |
| ≤19 | Restart foundations | Work the track in order, then retake |

**Total questions:** 40 · **Passing score:** 28 (70%)

## Recommended Study Areas

{study}

- Track: [{track_name}]({track_index})
- Lab: {lab_link}
- Cheat sheet: [{track_name}]({cheat})
- Interview prep: [{track_name}]({interview_link})
- Path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## Interview Connection

{interview}

## References

{refs_md}
"""


def Q(num, prompt, difficulty, options, correct, explanation, concepts):
    return dict(
        num=num,
        prompt=prompt,
        difficulty=difficulty,
        options=options,
        correct=correct,
        explanation=explanation,
        concepts=concepts,
    )


def linux() -> str:
    s1 = [
        Q(1, "What is the primary role of the Linux kernel?", "Beginner",
          {"A": "Provide a graphical desktop environment", "B": "Manage hardware, processes, memory, and system calls for user space", "C": "Replace Bash as the default shell", "D": "Store user documents in /home only"},
          "B", "The kernel is the core of the OS: hardware abstraction, scheduling, memory, and the system-call interface. Desktops and shells are user-space components.",
          ["Kernel vs user space", "System calls", "Process scheduling"]),
        Q(2, "Which path is the conventional location for third-party or locally installed software trees on many Linux systems?", "Beginner",
          {"A": "/var/log", "B": "/opt", "C": "/proc", "D": "/dev"},
          "B", "`/opt` is commonly used for optional/add-on application packages. `/var/log` is logs, `/proc` is process/kernel info, `/dev` is device nodes.",
          ["FHS", "/opt", "Filesystem hierarchy"]),
        Q(3, "What does the execute bit on a directory allow a user to do?", "Beginner",
          {"A": "List all filenames without reading them", "B": "Traverse into the directory (access files by known name if other permissions allow)", "C": "Delete the directory itself without write on the parent", "D": "Change ownership of every file inside"},
          "B", "On directories, execute means search/traverse. Listing needs read; creating/deleting entries needs write on the directory.",
          ["Directory permissions", "rwx on directories"]),
        Q(4, "Which command shows your effective user id, groups, and supplementary groups?", "Beginner",
          {"A": "whoami only", "B": "id", "C": "uname -a", "D": "pwd"},
          "B", "`id` prints uid, gid, and groups. `whoami` is only the username; `uname` is kernel/system identity.",
          ["Users and groups", "id"]),
        Q(5, "What is the difference between a hard link and a symbolic link?", "Beginner",
          {"A": "Hard links can cross filesystems; symlinks cannot", "B": "A hard link is another directory entry to the same inode; a symlink is a special file pointing to a path", "C": "Symlinks only work for directories; hard links only for devices", "D": "They are identical on ext4"},
          "B", "Hard links share an inode (same filesystem). Symlinks store a path and can cross filesystems.",
          ["Inodes", "ln", "ln -s"]),
        Q(6, "Which signal is the default sent by `kill <pid>` when no signal is specified?", "Beginner",
          {"A": "SIGKILL (9)", "B": "SIGTERM (15)", "C": "SIGSTOP", "D": "SIGHUP"},
          "B", "Default is SIGTERM, allowing graceful shutdown. SIGKILL cannot be caught and should be a last resort.",
          ["Signals", "kill"]),
        Q(7, "What does systemd use as the primary unit type for long-running daemons?", "Beginner",
          {"A": ".timer units only", "B": ".service units", "C": ".mount units exclusively", "D": ".socket units replace all services"},
          "B", "Daemons are typically managed as `.service` units. Timers, mounts, and sockets are other unit types.",
          ["systemd", "Unit files"]),
        Q(8, "Which command is the modern preferred way to follow logs for a systemd service named `nginx`?", "Beginner",
          {"A": "tail -f /var/log/messages only", "B": "journalctl -u nginx -f", "C": "dmesg -w", "D": "cat /proc/nginx"},
          "B", "`journalctl -u <unit> -f` follows that unit’s journal entries.",
          ["journalctl", "Logging"]),
        Q(9, "In a classic Unix permission string `-rwxr-xr--`, what can “others” do?", "Beginner",
          {"A": "Read, write, and execute", "B": "Read only", "C": "Read and execute", "D": "Nothing"},
          "B", "The last triad is `r--` → others may read only.",
          ["chmod", "Permission triads"]),
        Q(10, "What is the purpose of `/etc/sudoers` (or files under `/etc/sudoers.d`)?", "Beginner",
          {"A": "Store user passwords in plaintext", "B": "Define which users/groups may run commands as root or others via sudo", "C": "Configure SSH host keys", "D": "Set the default shell for root only"},
          "B", "sudoers controls privilege elevation policy. Edit with `visudo` to avoid syntax lockouts.",
          ["sudo", "Least privilege", "visudo"]),
    ]
    s2 = [
        Q(11, "You need to find all world-writable files under `/var/www` for a hardening review. Which approach is most appropriate?", "Intermediate",
          {"A": "ls -la /var/www", "B": "find /var/www -type f -perm -0002", "C": "chmod -R 777 /var/www", "D": "cat /etc/passwd"},
          "B", "`find … -perm -0002` locates files with the others-write bit.",
          ["find", "Permissions audit"]),
        Q(12, "A service fails immediately after `systemctl start`. What should you run first for evidence?", "Intermediate",
          {"A": "reboot", "B": "systemctl status <unit> and journalctl -u <unit> -e", "C": "rm -rf /etc/systemd", "D": "kill -9 1"},
          "B", "Status and journal give exit codes, paths, and permission errors.",
          ["Incident triage", "journalctl", "systemctl"]),
        Q(13, "Which `chmod` symbolic mode adds execute for user and group on `deploy.sh`?", "Intermediate",
          {"A": "chmod a+s deploy.sh", "B": "chmod ug+x deploy.sh", "C": "chmod o+w deploy.sh", "D": "chmod 000 deploy.sh"},
          "B", "`ug+x` adds execute for user and group without forcing a full octal mode.",
          ["chmod symbolic mode"]),
        Q(14, "Which command helps identify large directories under `/var`?", "Intermediate",
          {"A": "du -h --max-depth=1 /var | sort -h", "B": "ps aux", "C": "ip addr", "D": "systemctl list-timers"},
          "A", "`du` summarises disk usage by directory.",
          ["du", "Disk pressure"]),
        Q(15, "What does `systemctl enable nginx` do?", "Intermediate",
          {"A": "Starts nginx once and disables it on reboot", "B": "Creates the wants/ symlinks so nginx starts on boot (per unit install section)", "C": "Upgrades the nginx package", "D": "Opens port 80 in the firewall"},
          "B", "enable configures boot-time start via unit WantedBy relationships.",
          ["systemctl enable"]),
        Q(16, "Which crontab field set runs a job at 02:30 every day?", "Intermediate",
          {"A": "30 2 * * *", "B": "2 30 * * *", "C": "* * 2 30 *", "D": "30 * 2 * *"},
          "A", "Order is minute hour day-of-month month day-of-week → `30 2 * * *`.",
          ["cron"]),
        Q(17, "You need lines containing `ERROR` in `app.log`, case-insensitive. Best simple command?", "Beginner",
          {"A": "grep -i ERROR app.log", "B": "rm app.log", "C": "chmod 777 app.log", "D": "ln -s app.log"},
          "A", "`grep -i` matches case-insensitively.",
          ["grep", "Log analysis"]),
        Q(18, "What is a reliable way to see which process holds TCP port 8080?", "Intermediate",
          {"A": "ss -ltnp | grep 8080 (or lsof -iTCP:8080)", "B": "cat /etc/services only", "C": "echo 8080", "D": "uname -r"},
          "A", "`ss`/`lsof` show listeners and owning processes.",
          ["ss", "lsof"]),
        Q(19, "A script must fail fast if any command fails. Which Bash option helps?", "Intermediate",
          {"A": "set -e (and often set -u -o pipefail)", "B": "set +x only", "C": "alias rm=rm", "D": "ulimit -n 1"},
          "A", "`set -e` exits on failure; combining with `-u` and `pipefail` is common.",
          ["Bash", "set -e"]),
        Q(20, "Which permission bit on a directory makes files deletable only by their owner (or root) — classic `/tmp` behaviour?", "Intermediate",
          {"A": "setuid", "B": "setgid", "C": "sticky bit (t)", "D": "immutable attribute only"},
          "C", "The sticky bit on directories restricts unlinking to file owner/root.",
          ["Sticky bit", "/tmp"]),
    ]
    s3 = [
        Q(21, "PagerDuty: `rebash-api` failed. journalctl reports `Permission denied` opening the ExecStart script. Best next step?", "Intermediate",
          {"A": "Open all firewall ports", "B": "Check ownership/mode of the script and the user the unit runs as (User=)", "C": "Delete the unit file", "D": "Disable SELinux permanently without investigation"},
          "B", "Permission denied on the executable path implicates ownership/mode vs the service user.",
          ["systemd User=", "Permissions"]),
        Q(22, "Disk is 100% on `/`. `du` shows `/var/log` huge. Safest immediate mitigation while preserving evidence?", "Intermediate",
          {"A": "rm -rf /", "B": "Rotate/compress old logs, truncate only after copying critical evidence, fix retention", "C": "dd if=/dev/zero of=/var/log/big", "D": "chmod -R 777 /var/log"},
          "B", "Free space via log rotation/cleanup with care for forensics.",
          ["Disk full", "logrotate"]),
        Q(23, "A timer-based job did not run. `systemctl list-timers` shows the timer inactive. Likely check?", "Intermediate",
          {"A": "Whether the `.timer` unit is enabled/started and OnCalendar= is valid", "B": "Whether Docker is installed", "C": "Whether /etc/hosts contains google.com", "D": "Whether the GPU driver exists"},
          "A", "Timers must be enabled/started; calendar expressions and related service units matter.",
          ["systemd timers"]),
        Q(24, "SSH works from your laptop but CI fails with `Permission denied (publickey)`. Most likely?", "Intermediate",
          {"A": "The server has no SSH daemon", "B": "The runner lacks the authorised private key or uses the wrong user", "C": "iptables blocks ICMP only", "D": "DNS TTL is 86400"},
          "B", "Publickey failures usually mean missing/incorrect key material or wrong account.",
          ["SSH keys", "CI authentication"]),
        Q(25, "`htop` shows one process at 100% CPU after a release. Sound first step?", "Intermediate",
          {"A": "kill -9 -1", "B": "Identify PID, inspect command line/logs, thread state; consider SIGTERM after evidence", "C": "Disable the NIC", "D": "Format /home"},
          "B", "Diagnose before killing broadly.",
          ["CPU saturation", "Process triage"]),
        Q(26, "A junior proposes `chmod -R 777 /var/www` to fix the site. What do you recommend?", "Beginner",
          {"A": "Agree — 777 is fine in production", "B": "Set owner/group correctly and use the least mode that works (often 755 dirs / 644 files)", "C": "World-writable is required for nginx", "D": "Put the site in /proc"},
          "B", "777 is a common anti-pattern. Fix ownership and minimal modes.",
          ["Least privilege"]),
        Q(27, "You need elevation but policy forbids sharing the root password. Appropriate tool?", "Beginner",
          {"A": "sudo -i (if authorised) or sudo for specific commands", "B": "Write the root password to Slack", "C": "Disable PAM", "D": "chmod 777 /etc/shadow"},
          "A", "sudo provides audited, policy-controlled elevation.",
          ["sudo", "Access control"]),
        Q(28, "Application writes to `/var/lib/myapp` but the unit uses `ProtectSystem=strict`. What happens?", "Advanced",
          {"A": "Nothing — ProtectSystem is cosmetic", "B": "Writes outside allowed paths fail; use ReadWritePaths= (or relax carefully)", "C": "The kernel panics", "D": "SELinux is disabled"},
          "B", "systemd sandboxing restricts filesystem writes.",
          ["systemd hardening", "ProtectSystem"]),
        Q(29, "SSH latency is fine but authentication takes ~10s. A common cause?", "Advanced",
          {"A": "MTU 9000 only", "B": "Reverse DNS / GSSAPI / UseDNS delays in sshd", "C": "Missing /etc/hostname always blocks forever", "D": "Too much free RAM"},
          "B", "SSH can stall on reverse DNS or auth method negotiation.",
          ["sshd", "UseDNS"]),
        Q(30, "Prove a package is installed and which version on Debian/Ubuntu. Best pair?", "Intermediate",
          {"A": "dpkg -l | grep pkg ; apt-cache policy pkg", "B": "brew list", "C": "systemctl reboot", "D": "tar -tzf"},
          "A", "dpkg/apt query package state on Debian family systems.",
          ["Package management", "dpkg"]),
    ]
    s4 = [
        Q(31, "Unit is `active (running)` but curl fails; `ss` shows nothing listening. Likely category?", "Intermediate",
          {"A": "Process is up but bound to a different address/port or crashed child listener", "B": "The moon phase", "C": "ext4 fragmentation only", "D": "Missing swap always"},
          "A", "A parent can be running while the listener failed or binds elsewhere.",
          ["Listen address", "Health checks vs process state"]),
        Q(32, "`journalctl -u app` shows ExecStart path not found. Fix?", "Beginner",
          {"A": "Correct the path in the unit, daemon-reload, restart", "B": "chmod 777 /", "C": "Delete journald", "D": "Disable the unit forever without fixing"},
          "A", "Broken ExecStart paths are fixed in the unit file followed by reload/restart.",
          ["Unit files", "daemon-reload"]),
        Q(33, "After `apt upgrade`, a service will not start due to a missing shared library. What helps confirm?", "Advanced",
          {"A": "ldd on the binary / checking package dependencies", "B": "ping 8.8.8.8 only", "C": "changing wallpaper", "D": "increasing nice value randomly"},
          "A", "`ldd` and dependency packages reveal missing libs after upgrades.",
          ["Shared libraries", "ldd"]),
        Q(34, "`df -h` shows space free but `touch` fails with “No space left”. Likely?", "Advanced",
          {"A": "Inode exhaustion (`df -i`)", "B": "DNS failure", "C": "Wrong timezone", "D": "Caps Lock"},
          "A", "Exhausted inodes can block new files while byte space remains.",
          ["Inodes", "df -i"]),
        Q(35, "A privileged port bind fails for a non-root service. Modern approach besides running as root?", "Advanced",
          {"A": "Use capabilities (e.g. CAP_NET_BIND_SERVICE), authbind, or reverse proxy on 80/443", "B": "Always chmod 777 the binary", "C": "Disable the firewall globally", "D": "Bind to port 22"},
          "A", "Prefer capabilities or a front proxy over running full root.",
          ["Capabilities", "Privilege separation"]),
    ]
    s5 = [
        Q(36, "For a single Linux VM hosting a public HTTPS API, which layering is most sound?", "Intermediate",
          {"A": "App as root on :443 with 777 configs", "B": "TLS terminator/reverse proxy + unprivileged app on localhost + firewall allow 80/443 only", "C": "Disable SSH and hope", "D": "Store secrets in a world-readable gist"},
          "B", "Terminate TLS at a hardened edge, run the app with least privilege, restrict exposure.",
          ["Defence in depth", "Reverse proxy"]),
        Q(37, "Why separate `/var` (or a dedicated log volume) on production servers?", "Intermediate",
          {"A": "Aesthetic reasons only", "B": "Contain log growth so a runaway log cannot fill the root filesystem as easily", "C": "Makes kernel upgrades impossible", "D": "Required by PCI to use XFS only"},
          "B", "Filesystem separation limits blast radius of growth and simplifies backups.",
          ["Filesystem layout", "Capacity isolation"]),
        Q(38, "Which backup statement is most accurate for Linux system state?", "Intermediate",
          {"A": "RAID is a backup", "B": "Backups need retention, restore tests, and off-box copies — RAID is availability not backup", "C": "Snapshots without restore tests are enough forever", "D": "Only back up /tmp"},
          "B", "RAID/redundancy is not a backup. Test restores.",
          ["Backup", "Disaster recovery"]),
        Q(39, "For SSH administration at scale, which design is preferable?", "Advanced",
          {"A": "Shared root password on a wiki", "B": "Per-user keys or SSO/cert auth, sudo for elevation, bastion/session recording as needed", "C": "Telnet with OTP sticky notes", "D": "FTP to edit /etc"},
          "B", "Key/cert auth, individual accounts, and audited sudo are baseline.",
          ["SSH hardening", "Bastion"]),
        Q(40, "A cost-conscious team runs batch jobs nightly on systemd hosts. Best approach?", "Intermediate",
          {"A": "Busy-loop in a screen session", "B": "systemd `.timer` + `.service` with clear logs and failure alerts", "C": "Manual login each night", "D": "Disable NTP so cron drifts"},
          "B", "Timers integrate with journald and dependency management.",
          ["Timers", "Batch jobs"]),
    ]
    return wrap_quiz(
        title="Quiz — Linux Fundamentals",
        description="40-question Linux fundamentals quiz covering FHS, permissions, systemd, logs, triage, and production hardening judgement.",
        track_name="Linux",
        tag="linux",
        overview="Validate core Linux administration skills used daily by DevOps and SRE engineers: filesystem layout, permissions, processes, systemd, logging, and incident judgement.",
        objectives=[
            "Explain kernel vs user space and FHS basics",
            "Apply permissions, ownership, and sudo safely",
            "Operate systemd units and journald",
            "Triage failed services, disk pressure, and port conflicts",
            "Choose hardening and backup patterns that match production norms",
        ],
        sections=[
            ("Section 1 — Fundamentals", s1),
            ("Section 2 — Practical Knowledge", s2),
            ("Section 3 — Scenario-Based Questions", s3),
            ("Section 4 — Troubleshooting", s4),
            ("Section 5 — Architecture", s5),
        ],
        study="Misses in Sections 1–2 → revisit early Linux tutorials. Misses in 3–4 → practise the Linux production incident lab. Misses in 5 → re-read security hardening and troubleshooting tutorials.",
        interview="Interviewers often ask permission bits on directories, systemd failure triage, journalctl workflows, and “disk full but df looks fine” (inodes). Be ready to narrate a service-down incident end-to-end.",
        refs=[
            "[systemd documentation](https://www.freedesktop.org/software/systemd/man/)",
            "[Linux man-pages project](https://www.kernel.org/doc/man-pages/)",
            "[Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html)",
        ],
        lab_link="[Linux Production Incident Triage](../labs/linux-production-incident-triage.md)",
        cheat="../cheatsheets/linux.md",
        interview_link="../interview/linux.md",
        track_index="../linux/index.md",
    )


def docker() -> str:
    s1 = [
        Q(1, "What is the main difference between a container and a traditional virtual machine?", "Beginner",
          {"A": "Containers virtualise hardware; VMs share the host kernel only", "B": "Containers share the host kernel and isolate processes; VMs typically include a guest OS on a hypervisor", "C": "VMs cannot run Linux", "D": "Containers always include a full hypervisor"},
          "B", "Containers are process-level isolation on a shared kernel. VMs virtualise hardware with a guest OS.",
          ["Containers vs VMs", "Namespaces", "cgroups"]),
        Q(2, "Which component is the long-running Docker daemon on Linux?", "Beginner",
          {"A": "dockerd", "B": "containerd-shim only without dockerd", "C": "kubectl", "D": "systemd-resolved"},
          "A", "`dockerd` is the Docker daemon. containerd is often used underneath; kubectl is Kubernetes.",
          ["dockerd", "Docker architecture"]),
        Q(3, "What does a Docker image contain conceptually?", "Beginner",
          {"A": "A running process table only", "B": "A layered, immutable filesystem snapshot plus metadata/config to start containers", "C": "Only the host kernel modules", "D": "A Kubernetes PodSpec"},
          "B", "Images are layered artefacts used as templates for containers.",
          ["Images", "Layers", "OCI"]),
        Q(4, "Which command starts an interactive shell in a new Ubuntu container and removes it on exit?", "Beginner",
          {"A": "docker run --rm -it ubuntu:24.04 bash", "B": "docker build -t ubuntu", "C": "docker compose down", "D": "docker system prune -a"},
          "A", "`run --rm -it` creates an interactive container and cleans up on exit.",
          ["docker run"]),
        Q(5, "What is the default bridge network behaviour for published ports?", "Beginner",
          {"A": "All container ports are exposed to the world automatically", "B": "You publish specific ports with -p/--publish; otherwise they stay on the container network namespace", "C": "Docker disables networking by default", "D": "Bridge mode requires Kubernetes"},
          "B", "Publishing maps host ports to container ports intentionally.",
          ["Port publishing", "Bridge network"]),
        Q(6, "Which Dockerfile instruction creates a new image layer from filesystem changes of a command?", "Beginner",
          {"A": "LABEL", "B": "RUN", "C": "EXPOSE", "D": "MAINTAINER (legacy)"},
          "B", "`RUN` executes build steps and commits a layer. `EXPOSE` is documentation metadata.",
          ["Dockerfile", "RUN"]),
        Q(7, "What is a Docker volume best used for?", "Beginner",
          {"A": "Storing ephemeral container CPU shares", "B": "Persisting data beyond container lifecycle", "C": "Compiling the kernel", "D": "Replacing TLS certificates on the host CA store automatically"},
          "B", "Volumes persist data independent of container recreate.",
          ["Volumes", "Persistence"]),
        Q(8, "In Compose, how do services typically resolve each other by name?", "Beginner",
          {"A": "They cannot", "B": "Via the Compose project network DNS using service names", "C": "Only via public Internet DNS", "D": "Only via /etc/hosts on the laptop, never in containers"},
          "B", "Compose creates a user-defined network where service names resolve to containers.",
          ["Compose DNS"]),
        Q(9, "What does `HEALTHCHECK` in a Dockerfile define?", "Beginner",
          {"A": "Kubernetes probes", "B": "A command Docker runs to mark the container healthy/unhealthy", "C": "Host antivirus policy", "D": "Image signing identity"},
          "B", "Docker healthchecks update container health status used by Compose and operators.",
          ["HEALTHCHECK"]),
        Q(10, "Why pin image tags like `1.2.3` or digests instead of `:latest` in production?", "Beginner",
          {"A": "latest is always immutable", "B": "Pinned references make builds and rollbacks reproducible", "C": "Digests prevent networking", "D": "Tags are illegal in OCI"},
          "B", "`:latest` moves; digests/tags pin what you run.",
          ["Image pinning", "Supply chain"]),
    ]
    s2 = [
        Q(11, "Which practice reduces final image size most effectively?", "Intermediate",
          {"A": "Using fat base images and copying build toolchains into runtime", "B": "Multi-stage builds: compile in a builder stage, copy artefacts into a slim runtime stage", "C": "Adding more ADD instructions", "D": "Running apt-get upgrade in every layer without cleanup"},
          "B", "Multi-stage builds leave compilers out of the runtime image.",
          ["Multi-stage builds"]),
        Q(12, "You need a container’s logs for service `api` in Compose. Best command?", "Beginner",
          {"A": "docker compose logs api", "B": "kubectl logs api", "C": "journalctl -u docker-compose", "D": "cat /var/lib/docker randomly"},
          "A", "Compose aggregates container logs per service.",
          ["docker compose logs"]),
        Q(13, "Bind mount vs named volume — which statement is correct?", "Intermediate",
          {"A": "Bind mounts map a host path; named volumes are managed by Docker and often preferred for portability", "B": "Named volumes always delete host home directories", "C": "Bind mounts cannot be read-only", "D": "Volumes only work on Windows"},
          "A", "Bind mounts are host-path coupled; named volumes are Docker-managed.",
          ["Bind mounts", "Named volumes"]),
        Q(14, "Which flag runs a container with a read-only root filesystem (where supported)?", "Intermediate",
          {"A": "--read-only", "B": "--privileged", "C": "--net=host", "D": "--pid=host"},
          "A", "`--read-only` hardens the container filesystem; privileged/host namespaces widen attack surface.",
          ["Security hardening"]),
        Q(15, "An app inside Compose must call service `db` on port 5432. Correct URL hostname from another service?", "Beginner",
          {"A": "localhost", "B": "db (the service name)", "C": "127.0.0.1 on the laptop only", "D": "host.docker.internal is always required"},
          "B", "Inside the Compose network, use the service name. `localhost` is the container itself.",
          ["Compose networking"]),
        Q(16, "What does `docker build --pull` help with?", "Intermediate",
          {"A": "Deleting all images", "B": "Refreshing base images from the registry before build", "C": "Pushing secrets to Docker Hub", "D": "Disabling BuildKit"},
          "B", "`--pull` reduces surprise from stale cached base tags.",
          ["docker build"]),
        Q(17, "Which statement about secrets in images is true?", "Intermediate",
          {"A": "Baking API keys into ENV in the image is safe if the image is private forever", "B": "Prefer runtime secrets (env at deploy, secret mounts); never commit secrets into layers", "C": "Secrets in layers cannot be extracted", "D": "LABEL is the standard secret store"},
          "B", "Image layers and history leak secrets. Use runtime injection.",
          ["Secrets", "Image layers"]),
        Q(18, "`docker system prune` mainly removes what?", "Intermediate",
          {"A": "Only running containers", "B": "Unused data (stopped containers, dangling images/networks — depending on flags)", "C": "The host operating system", "D": "Kubernetes etcd"},
          "B", "Prune reclaims unused Docker objects; be careful with `-a` and volumes flags.",
          ["prune"]),
        Q(19, "EXPOSE 8080 in a Dockerfile means:", "Beginner",
          {"A": "The port is published to the host automatically", "B": "Metadata documenting the intended listen port; publishing still needs -p or Compose ports", "C": "Firewall rules are opened on the host", "D": "TLS is enabled"},
          "B", "EXPOSE does not publish ports by itself.",
          ["EXPOSE"]),
        Q(20, "Which Compose pattern waits until a dependency is healthy before starting a service?", "Intermediate",
          {"A": "depends_on with condition: service_healthy", "B": "links: (legacy) alone guarantees health", "C": "restart: always", "D": "stdin_open: true"},
          "A", "Modern Compose can wait on health conditions via depends_on.",
          ["depends_on", "Healthchecks"]),
    ]
    s3 = [
        Q(21, "Staging: `web` returns 502. `api` runs. `API_URL=http://api.internal:8080` but Compose service is `api`. Likely fix?", "Intermediate",
          {"A": "Use http://api:8080 (service DNS name) and matching ports", "B": "Reboot the laptop twice", "C": "Delete all volumes immediately", "D": "Switch to :latest everywhere"},
          "A", "Compose DNS uses service names, not invented hostnames unless you add aliases.",
          ["Compose DNS", "502 upstream"]),
        Q(22, "Container exits immediately with code 0. What do you check first?", "Intermediate",
          {"A": "Whether the main process exited (CMD/ENTRYPOINT finished) — inspect logs and command", "B": "Buy a new SSD", "C": "Disable IPv6 globally", "D": "Remove HEALTHCHECK only"},
          "A", "Exit 0 means the PID 1 process ended successfully — often a mis-set command.",
          ["PID 1", "CMD vs ENTRYPOINT"]),
        Q(23, "Image build is slow every CI run. Highest-impact improvement?", "Intermediate",
          {"A": "Put rarely changing dependency installs before frequently changing COPY of app code; use cache mounts where appropriate", "B": "Disable BuildKit permanently", "C": "Copy the entire repo before any RUN apt", "D": "Use --no-cache always"},
          "A", "Layer ordering maximises cache hits.",
          ["Build cache", "CI performance"]),
        Q(24, "You must run a one-off migration using the same image/env as `api` in Compose.", "Intermediate",
          {"A": "docker compose run --rm api <migration command>", "B": "Edit production DB from a browser extension", "C": "docker kill -9 $(docker ps -q)", "D": "Rebuild without network forever"},
          "A", "`compose run` starts a one-off container with service config.",
          ["compose run"]),
        Q(25, "Registry push fails with authentication error. First checks?", "Beginner",
          {"A": "docker login and correct image name/registry host", "B": "Disable TLS on the public Internet", "C": "Use telnet to port 80 only", "D": "Delete local Docker Desktop settings blindly"},
          "A", "Auth and repository naming are the usual causes.",
          ["Registries", "docker login"]),
        Q(26, "Container TLS errors with skewed clocks. Least bad approach?", "Advanced",
          {"A": "Ensure host clock/NTP is correct; avoid privileged time hacks unless required", "B": "Disable TLS verification permanently", "C": "Set date inside every container manually each hour", "D": "Use HTTP only in production"},
          "A", "Fix host time; do not disable TLS verification.",
          ["TLS", "NTP"]),
        Q(27, "Security review: container runs as root and mounts docker.sock. Risk?", "Advanced",
          {"A": "Low — docker.sock is read-only by nature", "B": "High — docker.sock access can equate to host root control", "C": "None if the image is alpine", "D": "Only a problem on Windows"},
          "B", "Mounting docker.sock is near-equivalent to root on the host.",
          ["docker.sock", "Container escape"]),
        Q(28, "You changed compose.yaml env vars but behaviour is unchanged. Likely?", "Intermediate",
          {"A": "Need recreate: docker compose up -d --force-recreate (or up after change)", "B": "Env vars never apply in Compose", "C": "Must reboot BIOS", "D": "Only kubectl apply works"},
          "A", "Existing containers keep old config until recreated.",
          ["Recreate containers"]),
        Q(29, "Final stage is distroless/scratch and a dynamic binary misses libc. Symptom?", "Advanced",
          {"A": "Runtime failures loading dynamic libraries — use static build or matching runtime base", "B": "Faster DNS", "C": "Automatic Kubernetes deploy", "D": "Larger attack surface always"},
          "A", "Dynamic binaries need compatible libs; static or proper base images fix this.",
          ["Distroless", "Static linking"]),
        Q(30, "Team wants identical images from laptop and CI. What helps most?", "Intermediate",
          {"A": "Pin bases by digest, lock dependency versions, use consistent BuildKit behaviour", "B": "Always build from :latest on Fridays", "C": "Disable checksums", "D": "Commit node_modules into the image randomly"},
          "A", "Reproducibility comes from pinning and consistent build tooling.",
          ["Reproducible builds"]),
    ]
    s4 = [
        Q(31, "`api` unhealthy; logs show connection refused to DB still starting. Best direction?", "Intermediate",
          {"A": "Add healthcheck on DB and depends_on condition service_healthy; fix race", "B": "Remove DB entirely", "C": "Use host networking for everything always", "D": "Ignore health and hope"},
          "A", "Startup races are fixed with health-gated dependencies.",
          ["Healthchecks", "Race conditions"]),
        Q(32, "`docker run` fails: port is already allocated. Check with?", "Beginner",
          {"A": "ss/lsof on the host port; change mapping or stop the conflicting process", "B": "kubectl drain", "C": "terraform destroy blindly", "D": "rm -rf /"},
          "A", "Host port conflicts are diagnosed with socket tools.",
          ["Port conflicts"]),
        Q(33, "Build fails: `COPY package.json` not found. Cause?", "Beginner",
          {"A": "Build context does not include the file (wrong path/context directory)", "B": "Docker Hub is offline always", "C": "YAML indentation in Compose only", "D": "Missing Kubernetes Secret"},
          "A", "COPY paths are relative to the build context.",
          ["Build context", "COPY"]),
        Q(34, "Container cannot resolve external DNS. Host browsing works. Likely Docker area?", "Advanced",
          {"A": "Daemon DNS config / embedded DNS / network mode issues", "B": "Missing CPU shares", "C": "Wrong Dockerfile LABEL", "D": "Absent HEALTHCHECK only"},
          "A", "Container DNS is controlled by Docker networking configuration.",
          ["Docker DNS"]),
        Q(35, "`permission denied` writing to a mounted volume on Linux. Common cause?", "Intermediate",
          {"A": "UID/GID inside container differs from host directory ownership", "B": "Image name too short", "C": "JSON logs disabled", "D": "Compose version key aesthetic"},
          "A", "Align user IDs or ownership on bind mounts.",
          ["UIDs", "Volume permissions"]),
    ]
    s5 = [
        Q(36, "For production containers, which default is best?", "Intermediate",
          {"A": "Run as root with --privileged", "B": "Non-root user, drop capabilities, read-only rootfs where possible, pin digests", "C": "Mount docker.sock into every app", "D": "Use :latest and hope"},
          "B", "Least privilege and pinned artefacts are baseline production hygiene.",
          ["Container security"]),
        Q(37, "When is Docker Compose appropriate vs Kubernetes?", "Intermediate",
          {"A": "Compose for local/dev and simple single-host stacks; Kubernetes for multi-node orchestration and richer scheduling/self-healing", "B": "Compose always replaces Kubernetes in global scale SaaS", "C": "Kubernetes cannot run containers", "D": "They are identical products"},
          "A", "Choose orchestration complexity to match operational needs.",
          ["Compose vs Kubernetes"]),
        Q(38, "CI builds images. Where should promotion to production registry happen?", "Advanced",
          {"A": "From unverified developer laptops only", "B": "Through CI with scans/signing policies, promoting immutable digests", "C": "By emailing tar files of images", "D": "By rewriting history on main with force"},
          "B", "Controlled CI promotion with scanning is the norm.",
          ["CI/CD", "Image promotion"]),
        Q(39, "Logging strategy for containers?", "Intermediate",
          {"A": "Write only inside ephemeral container layers and never collect", "B": "Log to stdout/stderr; collect via Docker logging drivers / platform agents", "C": "SSH and tail files only, forever", "D": "Disable all logs in production"},
          "B", "Twelve-factor style logging to stdout enables central collection.",
          ["Logging drivers"]),
        Q(40, "Resource control on a noisy neighbour host?", "Intermediate",
          {"A": "Ignore cgroups", "B": "Set memory/CPU limits (compose deploy.resources / run flags) appropriate to SLOs", "C": "Always --network host", "D": "Remove healthchecks to free CPU"},
          "B", "cgroup limits protect hosts and colocated workloads.",
          ["cgroups", "Resource limits"]),
    ]
    return wrap_quiz(
        title="Quiz — Docker Fundamentals",
        description="40-question Docker quiz covering images, containers, Dockerfile, Compose networking, security, and production operations.",
        track_name="Docker",
        tag="docker",
        overview="Assess practical Docker skills: images and containers, Dockerfile layering, volumes, Compose networking, healthchecks, and secure operational defaults.",
        objectives=[
            "Explain images, containers, and Docker architecture basics",
            "Author and optimise Dockerfiles including multi-stage builds",
            "Use Compose networking, volumes, and health-gated dependencies",
            "Troubleshoot exits, port conflicts, and permission issues",
            "Apply production hardening and CI image promotion judgement",
        ],
        sections=[
            ("Section 1 — Fundamentals", s1),
            ("Section 2 — Practical Knowledge", s2),
            ("Section 3 — Scenario-Based Questions", s3),
            ("Section 4 — Troubleshooting", s4),
            ("Section 5 — Architecture", s5),
        ],
        study="Weak on Dockerfile/Compose → Docker track modules 2–4. Weak on failures → Troubleshooting tutorial + Compose stack recovery lab. Weak on hardening → Docker security tutorial.",
        interview="Expect containers vs VMs, layer caching, Compose DNS (`localhost` vs service name), volumes vs bind mounts, and why `:latest` and baked secrets are dangerous.",
        refs=[
            "[Docker documentation](https://docs.docker.com/)",
            "[Compose specification](https://docs.docker.com/compose/compose-file/)",
            "[Dockerfile reference](https://docs.docker.com/reference/dockerfile/)",
        ],
        lab_link="[Docker Compose Stack Recovery](../labs/docker-compose-stack-recovery.md)",
        cheat="../cheatsheets/docker.md",
        interview_link="../interview/docker.md",
        track_index="../docker/index.md",
    )


def kubernetes() -> str:
    s1 = [
        Q(1, "What is a Pod in Kubernetes?", "Beginner",
          {"A": "A physical rack", "B": "The smallest deployable unit: one or more containers sharing network namespace and volumes", "C": "A cloud region", "D": "A Helm repository only"},
          "B", "Pods group containers with shared networking/storage abstractions.",
          ["Pods"]),
        Q(2, "Which control plane component schedules Pods onto nodes?", "Beginner",
          {"A": "kube-scheduler", "B": "CoreDNS only", "C": "etcd alone", "D": "Ingress controller"},
          "A", "kube-scheduler assigns Pods to nodes.",
          ["Control plane", "kube-scheduler"]),
        Q(3, "What does a Deployment manage?", "Beginner",
          {"A": "PersistentVolumes directly", "B": "ReplicaSets/Pods for declarative, rolling updates of stateless workloads", "C": "Only Nodes", "D": "etcd snapshots"},
          "B", "Deployments own ReplicaSets and provide rollout strategies.",
          ["Deployment", "ReplicaSet"]),
        Q(4, "A ClusterIP Service provides:", "Beginner",
          {"A": "A public load balancer on every cloud by default", "B": "A stable virtual IP/DNS name for Pods inside the cluster", "C": "Physical disk attachment", "D": "TLS certificates automatically"},
          "B", "ClusterIP is internal service discovery and load balancing.",
          ["Service", "ClusterIP"]),
        Q(5, "What happens when a liveness probe fails repeatedly?", "Beginner",
          {"A": "Pod is removed from Service endpoints only", "B": "kubelet restarts the container", "C": "The node is cordoned automatically", "D": "etcd is compacted"},
          "B", "Failed liveness → container restart. Failed readiness → remove from endpoints.",
          ["livenessProbe"]),
        Q(6, "What happens when a readiness probe fails?", "Beginner",
          {"A": "Container is always killed immediately", "B": "Pod is taken out of Service endpoints until ready again", "C": "Namespace is deleted", "D": "API server restarts"},
          "B", "Readiness controls whether the Pod receives traffic via Services.",
          ["readinessProbe", "Endpoints"]),
        Q(7, "ConfigMaps are primarily for:", "Beginner",
          {"A": "Storing non-sensitive configuration data", "B": "Storing private keys as best practice", "C": "Replacing etcd", "D": "Billing data only"},
          "A", "Non-sensitive config belongs in ConfigMaps; use Secrets for sensitive material.",
          ["ConfigMap"]),
        Q(8, "kubectl apply is associated with which management style?", "Beginner",
          {"A": "Imperative only", "B": "Declarative configuration applied to the cluster", "C": "SSH into nodes to edit binaries", "D": "Manual etcd edits"},
          "B", "apply reconciles desired manifests with live objects.",
          ["kubectl apply"]),
        Q(9, "Namespaces are used to:", "Beginner",
          {"A": "Partition cluster resources and scope names for multi-tenancy/environments", "B": "Replace VPCs in all clouds", "C": "Store container images", "D": "Disable RBAC"},
          "A", "Namespaces scope objects and policies within a cluster.",
          ["Namespaces"]),
        Q(10, "Which object requests durable storage for a Pod?", "Beginner",
          {"A": "Ingress", "B": "PersistentVolumeClaim (bound to a PersistentVolume)", "C": "ServiceAccount token only", "D": "HorizontalPodAutoscaler"},
          "B", "PVCs request storage; PVs are the provisioned volumes.",
          ["PVC", "PV"]),
    ]
    s2 = [
        Q(11, "Which command tails logs from a Pod named `api-x` in namespace `prod`?", "Beginner",
          {"A": "kubectl logs -n prod api-x -f", "B": "docker compose logs", "C": "journalctl -u api-x", "D": "helm uninstall api-x"},
          "A", "kubectl logs with -n and -f follows Pod logs.",
          ["kubectl logs"]),
        Q(12, "You need to open a shell in a running container:", "Beginner",
          {"A": "kubectl exec -it -n <ns> <pod> -- sh", "B": "kubectl delete pod", "C": "kubectl cordon", "D": "kubectl proxy only"},
          "A", "exec attaches a command/shell into the container.",
          ["kubectl exec"]),
        Q(13, "ImagePullBackOff most often means:", "Intermediate",
          {"A": "The scheduler is missing", "B": "kubelet cannot pull the image (name/tag/auth/registry/network)", "C": "The Service CIDR is wrong", "D": "HPA is disabled"},
          "B", "Check image reference and pull secrets/registry connectivity.",
          ["ImagePullBackOff"]),
        Q(14, "CrashLoopBackOff indicates:", "Intermediate",
          {"A": "Pod starts then the container exits repeatedly", "B": "Node memory is always healthy", "C": "DNS is perfect", "D": "RBAC is unused"},
          "A", "Investigate logs, probes, and command failures.",
          ["CrashLoopBackOff"]),
        Q(15, "Which field sets CPU/memory requests and limits on a container?", "Intermediate",
          {"A": "resources.requests / resources.limits", "B": "replicas only", "C": "hostNetwork: true", "D": "strategy.type"},
          "A", "requests affect scheduling; limits cap usage.",
          ["Resources", "QoS"]),
        Q(16, "A Deployment rolling update should keep capacity. Which helps?", "Intermediate",
          {"A": "maxUnavailable / maxSurge settings appropriate to SLO", "B": "delete the namespace mid-rollout", "C": "set replicas to 0 first always", "D": "disable readiness probes permanently"},
          "A", "RollingUpdate parameters control surge and unavailability.",
          ["RollingUpdate"]),
        Q(17, "RBAC: a Role is scoped to:", "Intermediate",
          {"A": "A namespace (Role) vs cluster-wide (ClusterRole)", "B": "Only etcd", "C": "Only Ingress", "D": "Only container images"},
          "A", "Role is namespaced; ClusterRole is cluster-scoped.",
          ["RBAC", "Role", "ClusterRole"]),
        Q(18, "Helm primarily helps you:", "Intermediate",
          {"A": "Package, templatise, and release Kubernetes manifests as charts", "B": "Replace container runtimes", "C": "Compile the Linux kernel", "D": "Provision bare metal only"},
          "A", "Helm is the common package manager for Kubernetes apps.",
          ["Helm"]),
        Q(19, "HPA scales Pods based on:", "Intermediate",
          {"A": "Metrics such as CPU/memory/custom metrics (when metrics pipeline exists)", "B": "Git commit messages", "C": "Docker Hub stars", "D": "Manual /etc/hosts edits"},
          "A", "Horizontal Pod Autoscaler uses resource/custom metrics.",
          ["HPA"]),
        Q(20, "PodDisruptionBudget (PDB) is meant to:", "Advanced",
          {"A": "Limit voluntary disruptions so a minimum number/percentage of Pods stay available", "B": "Encrypt etcd automatically", "C": "Replace NetworkPolicies", "D": "Disable node upgrades forever"},
          "A", "PDBs protect availability during drains/upgrades.",
          ["PDB"]),
    ]
    s3 = [
        Q(21, "Intermittent 503s during deploy. Readiness path `/healthz` 404 while `/` works. Effect?", "Intermediate",
          {"A": "Pods may never become Ready, so Services send no traffic (or only to old pods) — fix probe to a real path", "B": "Nodes reboot", "C": "etcd loses quorum always", "D": "Images become unsigned"},
          "A", "Bad readiness blocks endpoints. Align probes with the app contract.",
          ["Readiness", "Probes"]),
        Q(22, "Deployment stuck. describe shows FailedScheduling / Insufficient cpu. Fix direction?", "Intermediate",
          {"A": "Reduce requests, add nodes, or free capacity — scheduling cannot place the Pod", "B": "Delete kube-apiserver", "C": "Change the app language", "D": "Disable all Services"},
          "A", "Scheduler needs fitting node resources.",
          ["Scheduling", "Requests"]),
        Q(23, "Secret mounted as env still shows old value after you apply a new Secret.", "Advanced",
          {"A": "Pods do not automatically reload env from updated Secrets — rollout restart / redesign for dynamic reload", "B": "Kubernetes never mounts Secrets", "C": "Only Helm can update Secrets", "D": "Need to reboot every node"},
          "A", "Env-injected secrets are fixed at process start for typical apps.",
          ["Secrets rotation"]),
        Q(24, "GitOps reports drift: live Deployment differs from Git. Correct response?", "Advanced",
          {"A": "Change Git (or allowlisted sync) — avoid long-lived kubectl edit that fights the reconciler", "B": "Always kubectl edit and ignore Git", "C": "Turn off the cluster", "D": "Delete Git history"},
          "A", "Git is the source of truth; reconcile toward desired state.",
          ["GitOps", "Drift"]),
        Q(25, "Ingress returns 404 but Service curl from inside cluster works. Likely layer?", "Intermediate",
          {"A": "Ingress rules/host/path or Ingress controller config", "B": "Container runtime missing", "C": "PVC pending only", "D": "HPA minReplicas"},
          "A", "Ingress is the external HTTP routing layer.",
          ["Ingress"]),
        Q(26, "You need zero-downtime drain of a node. Useful sequence?", "Intermediate",
          {"A": "cordon + drain (respecting PDBs), ensure replicas elsewhere, then maintain", "B": "power off the node immediately", "C": "delete the Deployment", "D": "remove CoreDNS first"},
          "A", "cordon/drain is the supported maintenance workflow.",
          ["kubectl drain", "PDB"]),
        Q(27, "NetworkPolicy default-deny in a namespace means new Pods:", "Advanced",
          {"A": "May be isolated until explicit allow policies select them", "B": "Automatically get Internet without rules", "C": "Bypass Services", "D": "Ignore DNS"},
          "A", "Default-deny requires careful allowlists for expected traffic.",
          ["NetworkPolicy"]),
        Q(28, "Init container fails; app container never starts. Why?", "Intermediate",
          {"A": "Init containers must succeed before app containers start", "B": "Init containers run after the app", "C": "Init containers replace the scheduler", "D": "Init containers only run on Windows"},
          "A", "Init sequence gates startup.",
          ["Init containers"]),
        Q(29, "type LoadBalancer on bare metal without cloud integration. What happens?", "Advanced",
          {"A": "EXTERNAL-IP may stay pending unless MetalLB/equivalent provides IPs", "B": "Kubernetes invents a public IP always", "C": "The Pod becomes a Node", "D": "RBAC is disabled"},
          "A", "LoadBalancer needs an implementation to allocate addresses.",
          ["LoadBalancer", "MetalLB"]),
        Q(30, "Liveness probe too aggressive on a slow-starting JVM. Symptom?", "Intermediate",
          {"A": "Container killed/restarted before it becomes healthy — use startupProbe or retune thresholds", "B": "Faster cold starts magically", "C": "More endpoints join early", "D": "etcd grows slower"},
          "A", "startupProbe or longer delays prevent premature liveness kills.",
          ["startupProbe"]),
    ]
    s4 = [
        Q(31, "Pod Pending; events: failed to pull image `myapp:latst` (typo). Root cause?", "Beginner",
          {"A": "Wrong image reference/tag", "B": "CoreDNS crash only", "C": "Missing Deployment name", "D": "PDB conflict"},
          "A", "Typos in image names cause pull failures.",
          ["Image references"]),
        Q(32, "Service selects app=api but Pods are labelled app=backend. Effect?", "Beginner",
          {"A": "Endpoints empty — no traffic to Pods", "B": "Automatic label rewrite", "C": "Nodes cordon", "D": "HPA scales to zero always"},
          "A", "Selector/label mismatch yields empty Endpoints.",
          ["Selectors", "Endpoints"]),
        Q(33, "OOMKilled in container status. Meaning?", "Intermediate",
          {"A": "Exceeded memory limit (or node pressure killing)", "B": "CPU throttle only", "C": "DNS NXDOMAIN", "D": "Successful probe"},
          "A", "OOMKilled is a memory kill signal outcome.",
          ["OOMKilled"]),
        Q(34, "`kubectl auth can-i delete deployments -n prod` returns no. Next?", "Intermediate",
          {"A": "Check RoleBindings/ClusterRoleBindings for your identity; request least privilege access", "B": "Disable RBAC cluster-wide", "C": "Use --force on API server flags casually", "D": "Store kubeconfig in a public gist"},
          "A", "Fix RBAC bindings appropriately; do not disable RBAC.",
          ["RBAC troubleshooting"]),
        Q(35, "PVC Pending forever in a cluster without default StorageClass. Likely?", "Intermediate",
          {"A": "No provisioner/StorageClass to satisfy the claim", "B": "Ingress misconfigured", "C": "HPA missing", "D": "Too many ConfigMaps"},
          "A", "Dynamic provisioning needs a StorageClass; otherwise bind a matching PV.",
          ["StorageClass", "PVC Pending"]),
    ]
    s5 = [
        Q(36, "For a stateless HTTP API, which pairing is most typical?", "Intermediate",
          {"A": "Deployment + ClusterIP/Ingress + HPA + PDB", "B": "one naked Pod on a specific node name forever without probes", "C": "hostNetwork for every Pod", "D": "Privileged DaemonSet as the web tier"},
          "A", "Stateless HTTP commonly uses Deployment, Service/Ingress, and availability controls.",
          ["Workload design"]),
        Q(37, "Why prefer requests+limits over unlimited containers?", "Intermediate",
          {"A": "Predictable scheduling and noisy-neighbour protection", "B": "They slow the API server only", "C": "Required to use ConfigMaps", "D": "Disable metrics"},
          "A", "Resources enable fair scheduling and containment.",
          ["Capacity planning"]),
        Q(38, "Multi-tenant cluster security baseline includes:", "Advanced",
          {"A": "Namespaces, RBAC least privilege, NetworkPolicies, admission controls, non-root images", "B": "A single cluster-admin kubeconfig for everyone", "C": "Privileged pods by default", "D": "No audit logs"},
          "A", "Defence in depth across identity, network, and workload controls.",
          ["Multi-tenancy", "Hardening"]),
        Q(39, "Blue/green vs rolling update — trade-off summary?", "Advanced",
          {"A": "Blue/green shifts traffic between versions with more capacity cost; rolling gradually replaces replicas in one Deployment", "B": "They are identical", "C": "Rolling always needs two clusters", "D": "Blue/green forbids Services"},
          "A", "Choose based on risk, capacity, and traffic switching needs.",
          ["Deployment strategies"]),
        Q(40, "Where should cluster state backups focus first?", "Advanced",
          {"A": "etcd (or control plane backup strategy) plus application data volumes", "B": "Only worker node /tmp", "C": "Only container stdout", "D": "Only CNI IPAM files on one node"},
          "A", "Control plane state and persistent app data are critical.",
          ["Disaster recovery", "etcd"]),
    ]
    return wrap_quiz(
        title="Quiz — Kubernetes Fundamentals",
        description="40-question Kubernetes quiz covering Pods, Deployments, Services, probes, RBAC, storage, troubleshooting, and production design.",
        track_name="Kubernetes",
        tag="kubernetes",
        overview="Validate Kubernetes fundamentals used on the job: workload APIs, networking abstractions, probes, config/storage, RBAC, and production operations judgement.",
        objectives=[
            "Explain Pods, Deployments, Services, and Namespaces",
            "Distinguish liveness vs readiness failure behaviour",
            "Use kubectl for logs, exec, and describe-driven triage",
            "Diagnose ImagePullBackOff, CrashLoopBackOff, scheduling, and probe mistakes",
            "Choose sensible production patterns (HPA, PDB, security baselines)",
        ],
        sections=[
            ("Section 1 — Fundamentals", s1),
            ("Section 2 — Practical Knowledge", s2),
            ("Section 3 — Scenario-Based Questions", s3),
            ("Section 4 — Troubleshooting", s4),
            ("Section 5 — Architecture", s5),
        ],
        study="Weak on API objects → early Kubernetes tutorials. Weak on probes/rollouts → Health Checks tutorial + Deployment triage lab. Weak on RBAC/security → RBAC and hardening tutorials.",
        interview="Be ready to explain probes, CrashLoopBackOff vs ImagePullBackOff, Service selectors, requests vs limits, and a drain/PDB story.",
        refs=[
            "[Kubernetes documentation](https://kubernetes.io/docs/home/)",
            "[Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)",
            "[Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)",
        ],
        lab_link="[Kubernetes Deployment Triage](../labs/kubernetes-deployment-triage.md)",
        cheat="../cheatsheets/kubernetes.md",
        interview_link="../interview/kubernetes.md",
        track_index="../kubernetes/index.md",
    )


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    files = {
        "linux-fundamentals.md": linux(),
        "docker-fundamentals.md": docker(),
        "kubernetes-fundamentals.md": kubernetes(),
    }
    for name, content in files.items():
        path = ROOT / name
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path} ({len(content)} bytes)")


if __name__ == "__main__":
    main()
