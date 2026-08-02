#!/usr/bin/env python3
"""Rewrite remaining Linux tutorials to the new quality bar."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINUX = ROOT / "docs" / "linux"


def page(
    *,
    title: str,
    desc: str,
    module: str,
    tut_n: int,
    mod_n: int,
    tags: list[str],
    prereq: list[str],
    nxt: list[str],
    diagram: str,
    lab: str,
    overview: str,
    theory_what: str,
    theory_why: str,
    theory_how: str,
    table: str,
    pitfalls: list[str],
    scenario: str,
    tasks: list[tuple[str, str, str, str]],
    challenge: str,
    interview: list[tuple[str, str]],
    related_prev_title: str,
    related_prev: str,
    related_next_title: str,
    related_next: str,
    difficulty: str | None = None,
) -> str:
    diff = difficulty or (
        "beginner" if tut_n <= 7 else "intermediate" if tut_n <= 19 else "advanced"
    )
    tags_yaml = "\n".join(f"  - {t}" for t in tags)
    prereq_yaml = (
        "prerequisites:\n" + "\n".join(f"  - {p}" for p in prereq) + "\n" if prereq else ""
    )
    next_yaml = "next:\n" + "\n".join(f"  - {n}" for n in nxt) + "\n" if nxt else ""
    objs = [
        f"Explain the core ideas of {title} in simple words",
        "Complete the hands-on lab with saved evidence files",
        "Use the main commands for this topic safely on Ubuntu",
        "Describe one production failure mode for this topic",
        "Answer interview-style questions using this tutorial",
    ]
    objs_md = "\n".join(f"- [ ] {o}" for o in objs)
    tasks_md = []
    for i, (tn, why, cmd, exp) in enumerate(tasks, 1):
        tasks_md.append(
            f"#### Task {i} – {tn}\n\n{why}\n\n```bash\ncd ~/rebash-linux/{lab}\nset -euo pipefail\n\n{cmd}\n```\n\n**Expected output:** {exp}\n"
        )
    iq = []
    for i, (q, a) in enumerate(interview, 1):
        iq.append(f'**{i}. {q}**\n\n??? success "Reveal answer"\n    {a}\n')
    prev_line = (
        f"- [{related_prev_title}]({related_prev}) *(previous)*"
        if related_prev
        else ""
    )
    next_line = (
        f"- [{related_next_title}]({related_next}) *(next)*" if related_next else ""
    )
    return f'''---
title: "{title}"
description: "{desc}"
difficulty: {diff}
estimated_time: "45–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "{module}"
tags:
{tags_yaml}
{prereq_yaml}{next_yaml}interview: interview/linux
comments: false
---

# {title}

## Overview

{overview}

This is **Tutorial {tut_n}** in **Module {mod_n}** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for Linux administrators, DevOps engineers, SRE, and platform engineers.

## Prerequisites

- [{related_prev_title}]({related_prev})
- Practice Ubuntu 22.04/24.04 VM (or similar)
- sudo when a task needs it

## Learning Objectives

By the end of this tutorial, you will be able to:

{objs_md}

## Architecture

![Diagram for {title}](../assets/excalidraw/{diagram})

## Theory

### What it is

{theory_what}

### Why it matters

{theory_why}

### How it works

{theory_how}

{table}

### Common pitfalls

{chr(10).join(f"- {p}" for p in pitfalls)}

## Hands-on Lab

### Objective

Complete a real, topic-specific lab for **{title}** and save evidence under `~/rebash-linux/{lab}`.

### Prerequisites

- Ubuntu-like Linux with the commands used in the tasks
- Writable home directory

### Lab environment

```bash
mkdir -p ~/rebash-linux/{lab} && cd ~/rebash-linux/{lab}
set -euo pipefail
```

### Real-world scenario

{scenario}

### Step-by-step tasks

{chr(10).join(tasks_md)}
### Validation steps

- [ ] All task evidence files exist under `~/rebash-linux/{lab}`
- [ ] You can explain each command you ran
- [ ] Challenge completed or consciously skipped

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| command not found | Missing package | Install with `sudo apt-get install -y <package>` |
| Permission denied | Needs root | Re-run that command with sudo |
| Device busy | Resource in use | Follow Cleanup; unmount carefully |

### Challenge exercise

{challenge}

### Learning outcomes

- Practised **{title}** with real commands
- Captured evidence suitable for a change ticket
- Linked the lab to production habits

### Cleanup

```bash
# Keep ~/rebash-linux/{lab} evidence unless you need the space
```

## Validation

- [ ] Lab completed under `~/rebash-linux/{lab}/`
- [ ] Theory points explained in your own words
- [ ] One production risk for this topic identified

## Code Walkthrough

1. Inspect before you change
2. Prefer reversible steps and evidence files
3. Use modern tools for this topic
4. Least privilege — sudo only when required
5. Clean up disposable lab resources

## Security Considerations

- Do not practise destructive steps on production hosts
- Avoid putting secrets in lab files
- Prefer VM snapshots before risky experiments
- Limit sudo to the commands you need
- Keep evidence for privileged changes

## Common Mistakes

!!! warning "Running lab steps on a shared production server"
    Lab changes can disrupt others. **Fix:** use a disposable VM.

!!! warning "Skipping validation checks"
    Silent failures slip through. **Fix:** run the `test`/`grep` lines in each task.

!!! warning "Copying disk commands without reading device names"
    Wrong disk destroys data. **Fix:** use loop files under your lab directory.

## Best Practices

- Keep lab evidence until the module is done
- Automate only after you understand the commands
- Document lasting config in configuration management
- Monitor capacity for paths you care about
- Prefer LTS images for server practice

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Lab command fails immediately | Missing tool or typo | Check `command -v` and spelling |
| No space left | Full disk | `df -h`; clean old evidence |
| sudo denied | Account not in sudo | Use a VM image with sudo configured |

## Summary

**{title}** is a core skill for Cloud and DevOps on Linux. Finish the lab until the commands feel natural, then continue to the next tutorial.

## Interview Questions

{chr(10).join(iq)}
## Related Tutorials

- [Linux Overview](index.md)
{prev_line}
{next_line}

## References

- [Linux man-pages](https://www.kernel.org/doc/man-pages/)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
'''


def main() -> None:
    specs: list[dict] = []

    specs.append(
        dict(
            slug="disk-usage-and-file-attributes.md",
            title="Disk Usage and File Attributes",
            desc="Measure disk and inode usage and inspect file attributes used in day-to-day Linux operations.",
            module="Module 3 · Linux Filesystem",
            tut_n=5,
            mod_n=3,
            tags=["linux", "disk", "df", "du", "attributes"],
            prereq=["linux/filesystem-paths-links-mounts-and-inodes"],
            nxt=["linux/users-groups-and-sudo"],
            diagram="linux-storage-layout.svg",
            lab="lab05",
            overview="Servers fail in boring ways: the disk fills up, or inodes run out while `df -h` still looks fine. This tutorial teaches `df`, `du`, inode checks, and basic file attributes so you can find what is using space before users feel pain.",
            theory_what="`df` shows filesystem capacity. `du` shows space used by files and directories. Inodes are filesystem objects; you can run out of inodes even with free bytes. Attributes such as immutable flags appear with `lsattr`/`chattr` on ext filesystems.",
            theory_why="Full `/` or `/var` stops logs, packages, and containers. Cloud volumes have size limits. Finding which directory grew overnight is a core on-call skill.",
            theory_how="```bash\ndf -h\ndf -i\ndu -sh dir/* 2>/dev/null | sort -h | tail\n```",
            table="| Tool | Question |\n|------|----------|\n| `df -h` | How full is each mount? |\n| `df -i` | Are inodes exhausted? |\n| `du -sh` | How big is this directory? |",
            pitfalls=[
                "Trusting `df -h` alone when inodes are exhausted",
                "Running unbounded `du` on huge network mounts",
                "Deleting open log files without restarting the writer",
            ],
            scenario="Alerts say disk space is critically low. You must find which directory grew and capture proof before you delete anything.",
            tasks=[
                (
                    "Filesystem capacity and inodes",
                    "See bytes and inode usage.",
                    "df -h | tee df-h.txt\ndf -i | tee df-i.txt\ntest -s df-h.txt",
                    "`df-h.txt` and `df-i.txt` contain real mount data.",
                ),
                (
                    "Measure sample directories with du",
                    "Create sample data and compare sizes.",
                    "mkdir -p sample/{a,b}\ndd if=/dev/zero of=sample/a/big.bin bs=1M count=5 status=none\ndd if=/dev/zero of=sample/b/big.bin bs=1M count=2 status=none\ndu -sh sample/* | tee du-sample.txt\ntest -s du-sample.txt",
                    "`du-sample.txt` shows `sample/a` larger than `sample/b`.",
                ),
                (
                    "Stat/attributes and evidence pack",
                    "Inspect a file and archive evidence.",
                    "echo data > sample/note.txt\nstat sample/note.txt | tee stat-note.txt\nlsattr sample/note.txt 2>/dev/null | tee lsattr.txt || echo lsattr-unavailable | tee lsattr.txt\ntar -czf lab05-evidence.tgz df-*.txt du-*.txt stat-note.txt lsattr.txt\nls -l lab05-evidence.tgz",
                    "Evidence archive exists.",
                ),
            ],
            challenge="Create 100 tiny files in `sample/many/` and save `df -i` output to `inode-demo.txt`.",
            interview=[
                (
                    "Difference between `df` and `du`?",
                    "`df` reports mount capacity. `du` sums file sizes under a path. They can disagree because of deleted-but-open files or reserved blocks.",
                ),
                (
                    "How can a disk look free in `df -h` but still reject new files?",
                    "Inodes may be exhausted (`df -i`), or a different mount is full. Check both bytes and inodes.",
                ),
                (
                    "How do you find large directories under `/var`?",
                    "`du -sh /var/* 2>/dev/null | sort -h` and drill into the biggest names.",
                ),
                (
                    "What are deleted-but-open files?",
                    "A process still holds a deleted file open, so space is freed only when it closes. Use `lsof +L1` or restart the writer.",
                ),
                (
                    "Why be careful with `chattr +i`?",
                    "Immutable files cannot be edited until the attribute is removed — helpful for safety, painful in emergencies if forgotten.",
                ),
            ],
            related_prev_title="Paths, Links, Mounts, and Inodes",
            related_prev="filesystem-paths-links-mounts-and-inodes.md",
            related_next_title="Users, Groups, and sudo",
            related_next="users-groups-and-sudo.md",
        )
    )

    specs.append(
        dict(
            slug="permissions-acls-and-special-bits.md",
            title="Permissions, ACLs, and Special Bits",
            desc="Apply chmod, chown, umask, ACLs, and special bits (sticky, SUID, SGID) for least-privilege Linux access.",
            module="Module 4 · Users & Permissions",
            tut_n=7,
            mod_n=4,
            tags=["linux", "permissions", "acl", "chmod"],
            prereq=["linux/users-groups-and-sudo"],
            nxt=["linux/text-processing-grep-sed-awk"],
            diagram="linux-permission-model.svg",
            lab="lab07",
            overview="File modes decide who can read, write, or execute a file. Special bits add sticky directories, setgid sharing, and occasional setuid tools. Access Control Lists (ACLs) grant extra users or groups without changing the basic owner/group model. Together they implement least privilege on shared servers.",
            theory_what="Each file has owner, group, and mode bits (`rwx`). `umask` sets defaults for new files. ACLs (`setfacl`/`getfacl`) add finer rules. Sticky bit on directories like `/tmp` stops users deleting others' files.",
            theory_why="World-writable app directories and `chmod 777` cause breaches and broken multi-user shares. Interviews and production reviews always test this topic.",
            theory_how="```bash\nls -l\nchmod 640 file\nchown user:group file\ngetfacl file 2>/dev/null || true\n```",
            table="| Mode | Meaning |\n|------|---------|\n| 644 | owner rw, group/other r |\n| 755 | owner rwx, others rx |\n| 2700 | setgid directory pattern (example) |\n| sticky `t` | restrict deletes in shared dirs |",
            pitfalls=[
                "Using `chmod 777` to 'make it work'",
                "Forgetting execute bit on directories",
                "ACLs present but ignored because tools not installed",
            ],
            scenario="Two engineers and one service need shared access to `/opt`-style app dirs without opening them to every user on the host.",
            tasks=[
                (
                    "Create tree and apply modes",
                    "Build a shared-style directory with safe modes.",
                    "mkdir -p share/{bin,etc,logs}\necho 'cfg=1' > share/etc/app.conf\nchmod 750 share share/bin share/etc\nchmod 770 share/logs\nchmod 640 share/etc/app.conf\nls -laR share | tee modes.txt\nnamei -l share/etc/app.conf | tee namei.txt",
                    "`modes.txt` shows non-777 modes; config is `640`.",
                ),
                (
                    "Demonstrate sticky behaviour in a lab dir",
                    "Show sticky bit on a directory listing.",
                    "mkdir -p sticky-demo\nchmod 1777 sticky-demo\nls -ld sticky-demo | tee sticky.txt\ngrep -q 't' sticky.txt || grep -q 'sticky' sticky.txt || test -k sticky-demo\nstat -c '%A %a %n' sticky-demo | tee sticky-stat.txt",
                    "`sticky-stat.txt` shows mode containing sticky (such as `1777`).",
                ),
                (
                    "Optional ACL evidence",
                    "Record ACL tools if available.",
                    "if command -v getfacl >/dev/null; then getfacl share/etc/app.conf | tee acl.txt; else echo 'acl-tools-missing' | tee acl.txt; fi\ntar -czf lab07-evidence.tgz modes.txt namei.txt sticky.txt sticky-stat.txt acl.txt\nls -l lab07-evidence.tgz",
                    "Evidence archive exists.",
                ),
            ],
            challenge="Add an ACL granting read to your current user explicitly with `setfacl` (if installed) and save `getfacl` output to `acl-challenge.txt`.",
            interview=[
                (
                    "What do the three permission triples mean in `ls -l`?",
                    "Owner, group, and other — each with read/write/execute bits for that class.",
                ),
                (
                    "Why is `chmod 777` dangerous?",
                    "Every user can read/write/execute. On shared hosts that often means data tampering or privilege escalation paths.",
                ),
                (
                    "What does the sticky bit do on a directory?",
                    "Users can create files, but typically only the file owner (or root) can delete/rename them — like `/tmp`.",
                ),
                (
                    "When do you use ACLs instead of only owner/group?",
                    "When multiple specific users/groups need access that does not fit one group cleanly.",
                ),
                (
                    "Why must directories have execute permission to be usable?",
                    "Execute on a directory means you can traverse into it (`cd` / access children). Without it, path lookup fails.",
                ),
            ],
            related_prev_title="Users, Groups, and sudo",
            related_prev="users-groups-and-sudo.md",
            related_next_title="Text Processing with grep, sed, and awk",
            related_next="text-processing-grep-sed-awk.md",
        )
    )

    # Remaining higher modules
    more = [
        (
            "storage-disks-partitions-and-filesystems.md",
            "Disks, Partitions, and Filesystems",
            "Inspect disks safely and practise a loopback partition/filesystem workflow with full cleanup.",
            "Module 8 · Storage Management",
            12,
            8,
            ["linux", "storage", "lsblk", "mkfs"],
            ["linux/systemd-targets-timers-and-boot"],
            ["linux/lvm-swap-and-disk-monitoring"],
            "linux-storage-layout.svg",
            "lab12",
            "Disks appear as block devices. You partition them, create filesystems, and mount them. On cloud VMs an extra volume is normal. This lab uses a **loop file** so you never touch the system disk.",
            "`lsblk` lists block devices. `parted`/`fdisk` change partitions. `mkfs` creates filesystems. `mount`/`umount` attach them. Always identify the correct device first.",
            "Wrong device names destroy data. Practising on loop devices builds muscle memory without risking the root disk.",
            "```bash\nlsblk -f\nfindmnt /\n```",
            "| Tool | Role |\n|------|------|\n| `lsblk` | List devices |\n| `mkfs.ext4` | Create filesystem |\n| `mount` | Attach filesystem |",
            [
                "Running mkfs on the wrong disk",
                "Forgetting to create a mountpoint",
                "Leaving test mounts after the lab",
            ],
            "You must prove you can create a filesystem on disposable storage and mount it read-write for an app data directory.",
            [
                (
                    "Inspect real disks (read-only)",
                    "List block devices without changing them.",
                    "lsblk -f | tee lsblk.txt\nfindmnt / | tee root-mnt.txt\ntest -s lsblk.txt",
                    "`lsblk.txt` lists devices.",
                ),
                (
                    "Create a loopback filesystem",
                    "Safe disposable disk file.",
                    "dd if=/dev/zero of=disk.img bs=1M count=64 status=none\nsudo losetup -fP --show disk.img | tee loop-dev.txt\nLOOP=$(cat loop-dev.txt)\nsudo mkfs.ext4 -F \"$LOOP\" | tee mkfs.txt\nmkdir -p mnt\nsudo mount \"$LOOP\" mnt\necho ok | sudo tee mnt/hello.txt\nsudo grep -q ok mnt/hello.txt\ndf -h mnt | tee df-mnt.txt",
                    "`mnt/hello.txt` contains ok; mount shows in `df-mnt.txt`.",
                ),
                (
                    "Unmount and detach",
                    "Cleanup loop device.",
                    "sudo umount mnt\nLOOP=$(cat loop-dev.txt)\nsudo losetup -d \"$LOOP\"\necho cleaned | tee cleanup.txt\ntar -czf lab12-evidence.tgz lsblk.txt mkfs.txt df-mnt.txt cleanup.txt\nls -l lab12-evidence.tgz",
                    "Loop detached; evidence archive exists.",
                ),
            ],
            "Recreate the loop filesystem and add an `/etc/fstab`-style line in `fstab.snippet` using the loop file path for documentation (do not install it system-wide).",
            [
                (
                    "What does `lsblk` show?",
                    "Block devices, sizes, and often filesystem/mount info — the first tool before disk changes.",
                ),
                (
                    "Why use a loop device in a lab?",
                    "It simulates a disk with a regular file so mistakes do not wipe the system disk.",
                ),
                (
                    "What is the difference between partitioning and creating a filesystem?",
                    "Partitioning divides a disk. `mkfs` creates a filesystem inside a partition/device so files can be stored.",
                ),
                (
                    "How do you see what is mounted on `/`?",
                    "`findmnt /` or `findmnt -T /`.",
                ),
                (
                    "Name one production safety check before `mkfs`.",
                    "Confirm the device name twice with `lsblk`, ensure it is the new empty volume, and have backups/snapshots.",
                ),
            ],
            "systemd Targets, Timers, and Boot",
            "systemd-targets-timers-and-boot.md",
            "LVM, Swap, and Disk Monitoring",
            "lvm-swap-and-disk-monitoring.md",
            "advanced",
        ),
        (
            "lvm-swap-and-disk-monitoring.md",
            "LVM, Swap, and Disk Monitoring",
            "Build a small LVM layout on a loop device, inspect swap, and monitor disk capacity.",
            "Module 8 · Storage Management",
            13,
            8,
            ["linux", "lvm", "swap"],
            ["linux/storage-disks-partitions-and-filesystems"],
            ["linux/linux-networking-tools"],
            "linux-storage-layout.svg",
            "lab13",
            "Logical Volume Manager (LVM) lets you grow storage more flexibly than fixed partitions. Swap backs memory under pressure. Monitoring disk capacity prevents outages.",
            "Physical volumes (PV), volume groups (VG), and logical volumes (LV) form LVM. `swapon --show` lists swap. `df`/`du` monitor capacity.",
            "Cloud data disks often start small and grow. LVM skills (or cloud volume resize skills) show up in production constantly.",
            "```bash\nsudo pvs; sudo vgs; sudo lvs\nswapon --show || true\n```",
            "| Object | Tool |\n|--------|------|\n| PV | `pvcreate`, `pvs` |\n| VG | `vgcreate`, `vgs` |\n| LV | `lvcreate`, `lvs` |",
            [
                "Forgetting to grow the filesystem after growing an LV",
                "Running LVM commands on the wrong disk",
                "Ignoring inode exhaustion",
            ],
            "You need a disposable LVM stack to prove you can create and remove PV/VG/LV safely.",
            [
                (
                    "Create loop PV/VG/LV",
                    "Disposable LVM lab.",
                    "dd if=/dev/zero of=lvm.img bs=1M count=128 status=none\nsudo losetup -fP --show lvm.img | tee loop.txt\nLOOP=$(cat loop.txt)\nsudo pvcreate -ffy \"$LOOP\" | tee pv.txt\nsudo vgcreate rebash_vg \"$LOOP\" | tee vg.txt\nsudo lvcreate -n rebash_lv -L 64M rebash_vg | tee lv.txt\nsudo mkfs.ext4 -F /dev/rebash_vg/rebash_lv | tee mkfs.txt\nmkdir -p mnt\nsudo mount /dev/rebash_vg/rebash_lv mnt\necho lvm-ok | sudo tee mnt/ok.txt\nsudo lvs | tee lvs.txt",
                    "`lvs.txt` shows `rebash_lv`; `mnt/ok.txt` exists.",
                ),
                (
                    "Swap and capacity signals",
                    "Record swap and df.",
                    "swapon --show | tee swap.txt || echo 'no-swap' | tee swap.txt\ndf -h mnt | tee df-mnt.txt\nfree -h | tee free.txt",
                    "Capacity files saved.",
                ),
                (
                    "Remove LVM lab stack",
                    "Full cleanup.",
                    "sudo umount mnt || true\nsudo lvremove -fy rebash_vg/rebash_lv || true\nsudo vgremove -fy rebash_vg || true\nLOOP=$(cat loop.txt)\nsudo pvremove -ffy \"$LOOP\" || true\nsudo losetup -d \"$LOOP\" || true\necho removed | tee removed.txt\ntar -czf lab13-evidence.tgz pv.txt vg.txt lv.txt lvs.txt df-mnt.txt removed.txt\nls -l lab13-evidence.tgz",
                    "LVM objects removed; evidence kept.",
                ),
            ],
            "Before cleanup, grow the LV by +16M and run `resize2fs`, saving commands/output to `grow.txt` (then still clean up).",
            [
                (
                    "What are PV, VG, and LV?",
                    "Physical volume (disk/loop), volume group (pool), logical volume (allocatable volume you format and mount).",
                ),
                (
                    "Why grow the filesystem after `lvextend`?",
                    "LVM growth does not automatically expand the filesystem; tools like `resize2fs`/`xfs_growfs` are required.",
                ),
                (
                    "How do you list swap?",
                    "`swapon --show` or check `/proc/swaps`.",
                ),
                (
                    "What do you monitor for disk risk?",
                    "Byte usage (`df -h`), inodes (`df -i`), and growth trends under `/var` and app mounts.",
                ),
                (
                    "Is LVM required on every cloud VM?",
                    "No — some teams use cloud volume resize without LVM — but LVM remains common on enterprise images.",
                ),
            ],
            "Disks, Partitions, and Filesystems",
            "storage-disks-partitions-and-filesystems.md",
            "Linux Networking Tools",
            "linux-networking-tools.md",
            "advanced",
        ),
    ]

    for row in more:
        (
            slug,
            title,
            desc,
            module,
            tut_n,
            mod_n,
            tags,
            prereq,
            nxt,
            diagram,
            lab,
            overview,
            theory_what,
            theory_why,
            theory_how,
            table,
            pitfalls,
            scenario,
            tasks,
            challenge,
            interview,
            prev_t,
            prev,
            next_t,
            nxtf,
            difficulty,
        ) = row
        specs.append(
            dict(
                slug=slug,
                title=title,
                desc=desc,
                module=module,
                tut_n=tut_n,
                mod_n=mod_n,
                tags=tags,
                prereq=prereq,
                nxt=nxt,
                diagram=diagram,
                lab=lab,
                overview=overview,
                theory_what=theory_what,
                theory_why=theory_why,
                theory_how=theory_how,
                table=table,
                pitfalls=pitfalls,
                scenario=scenario,
                tasks=tasks,
                challenge=challenge,
                interview=interview,
                related_prev_title=prev_t,
                related_prev=prev,
                related_next_title=next_t,
                related_next=nxtf,
                difficulty=difficulty,
            )
        )

    # Final modules
    finals = [
        dict(
            slug="logging-syslog-journald-logrotate.md",
            title="Logging — syslog, journald, logrotate",
            desc="Query journald, understand syslog paths, and practise logrotate configuration safely.",
            module="Module 12 · Logging & Monitoring",
            tut_n=18,
            mod_n=12,
            tags=["linux", "logging", "journald", "logrotate"],
            prereq=["linux/scheduling-cron-at-and-timers"],
            nxt=["linux/host-monitoring-vmstat-iostat-sar"],
            diagram="linux-logging.svg",
            lab="lab18",
            overview="Logs tell you what the system and apps did. On modern Linux, **journald** stores structured systemd logs. Classic text logs still appear under `/var/log`. **logrotate** prevents log files from filling the disk.",
            theory_what="`journalctl` reads the systemd journal. `/var/log/syslog` or `/var/log/messages` may still receive syslog messages. logrotate renames/compresses logs on a schedule.",
            theory_why="Without log rotation, disks fill. Without journal queries, incidents take longer. This is daily SRE work.",
            theory_how="```bash\njournalctl -xe\njournalctl -u ssh --since '1 hour ago'\nlogger 'rebash lab test'\n```",
            table="| Tool | Use |\n|------|-----|\n| `journalctl` | Query systemd logs |\n| `logger` | Write a test message |\n| `logrotate` | Rotate text logs |",
            pitfalls=[
                "Running unbounded journalctl on busy hosts",
                "Disabling rotation 'temporarily' and forgetting",
                "Ignoring permission on log files",
            ],
            scenario="Disk alerts point at `/var/log`. You must query recent SSH logs and prove logrotate config syntax before changing production.",
            tasks=[
                (
                    "Journal queries",
                    "Capture recent journal evidence.",
                    "journalctl --no-pager -n 50 | tee journal-tail.txt\njournalctl --no-pager -u ssh -n 20 2>/dev/null | tee journal-ssh.txt || journalctl --no-pager -u sshd -n 20 2>/dev/null | tee journal-ssh.txt || echo 'no-ssh-unit' | tee journal-ssh.txt\nlogger -t rebash-lab 'hello from lab18'\nsleep 1\njournalctl --no-pager -t rebash-lab -n 5 | tee journal-logger.txt\ngrep -q 'hello from lab18' journal-logger.txt",
                    "`journal-logger.txt` contains the test message.",
                ),
                (
                    "Classic log paths",
                    "List common log files.",
                    "ls -la /var/log | head -n 40 | tee var-log.txt\ntest -s var-log.txt",
                    "`var-log.txt` lists log directory entries.",
                ),
                (
                    "logrotate dry config",
                    "Write a sample logrotate snippet and validate.",
                    "mkdir -p logdir\necho line > logdir/app.log\ncat > app.logrotate << 'EOF'\n$(pwd)/logdir/app.log {\n  weekly\n  rotate 3\n  missingok\n  notifempty\n  copytruncate\n}\nEOF\n# Expand pwd for logrotate file\nsed -i \"s|\\$(pwd)|$PWD|\" app.logrotate 2>/dev/null || true\npython3 - <<'PY'\nfrom pathlib import Path\np=Path('app.logrotate')\ntext=p.read_text()\ntext=text.replace('$(pwd)', str(Path('.').resolve()))\np.write_text(text)\nprint('wrote', p)\nPY\nsudo logrotate -d app.logrotate 2>&1 | tee logrotate-debug.txt || logrotate -d app.logrotate 2>&1 | tee logrotate-debug.txt\ntar -czf lab18-evidence.tgz journal-*.txt var-log.txt app.logrotate logrotate-debug.txt\nls -l lab18-evidence.tgz",
                    "logrotate debug output saved; evidence archive exists.",
                ),
            ],
            challenge="Export `journalctl --since today` for your user session boot into `journal-today.txt` with a line limit (`-n 100`).",
            interview=[
                (
                    "What is journald?",
                    "systemd's logging service collecting logs from units and the kernel, queried with `journalctl`.",
                ),
                (
                    "Why use logrotate?",
                    "To compress/rotate text logs so they do not fill `/var`.",
                ),
                (
                    "How do you view logs for one service?",
                    "`journalctl -u servicename` with time filters like `--since`.",
                ),
                (
                    "What does `logger` do?",
                    "Sends a message into the system logging pipeline — useful for tests.",
                ),
                (
                    "Name a risk of storing secrets in logs.",
                    "Logs are widely readable in many setups and often shipped centrally — secrets can leak.",
                ),
            ],
            related_prev_title="Scheduling — cron, at, and Timers",
            related_prev="scheduling-cron-at-and-timers.md",
            related_next_title="Host Monitoring — vmstat, iostat, sar",
            related_next="host-monitoring-vmstat-iostat-sar.md",
        ),
        dict(
            slug="host-monitoring-vmstat-iostat-sar.md",
            title="Host Monitoring — vmstat, iostat, sar",
            desc="Collect CPU, memory, and disk performance signals with vmstat, iostat, and related tools.",
            module="Module 12 · Logging & Monitoring",
            tut_n=19,
            mod_n=12,
            tags=["linux", "monitoring", "vmstat", "iostat"],
            prereq=["linux/logging-syslog-journald-logrotate"],
            nxt=["linux/ssh-hardening-and-firewalls"],
            diagram="linux-host-monitoring.svg",
            lab="lab19",
            overview="When a server feels slow, you need numbers: CPU run queue, memory pressure, disk I/O wait. `vmstat`, `iostat`, and `sar` (from sysstat) are classic host monitoring tools still used in incidents.",
            theory_what="`vmstat` samples processes, memory, swap, and CPU. `iostat` shows device utilisation. `sar` can show historical stats when sysstat is enabled.",
            theory_why="Cloud dashboards help, but shell tools work on any broken VM where agents are dead. Interviews expect these basics.",
            theory_how="```bash\nvmstat 1 5\niostat -xz 1 3 2>/dev/null || true\nfree -h\n```",
            table="| Tool | Focus |\n|------|-------|\n| `vmstat` | CPU/memory/swap/io overview |\n| `iostat` | Per-disk I/O |\n| `free` | Memory summary |",
            pitfalls=[
                "Looking at one sample only — always take a few intervals",
                "Ignoring `wa` (I/O wait) when diagnosing slowness",
                "Forgetting to install `sysstat`",
            ],
            scenario="Users report slowness on a VM. Metrics agents are missing. You must capture host performance evidence from the shell.",
            tasks=[
                (
                    "Install sysstat if needed and run vmstat",
                    "Collect CPU/memory samples.",
                    "if ! command -v vmstat >/dev/null; then sudo apt-get update && sudo apt-get install -y sysstat; fi\nvmstat 1 5 | tee vmstat.txt\ntest -s vmstat.txt",
                    "`vmstat.txt` has multiple samples.",
                ),
                (
                    "iostat and memory",
                    "Disk and memory signals.",
                    "iostat -xz 1 3 2>/dev/null | tee iostat.txt || echo 'iostat-unavailable' | tee iostat.txt\nfree -h | tee free.txt\nuptime | tee uptime.txt",
                    "Memory and uptime evidence saved.",
                ),
                (
                    "Pack evidence",
                    "Archive for the ticket.",
                    "tar -czf lab19-evidence.tgz vmstat.txt iostat.txt free.txt uptime.txt\nls -l lab19-evidence.tgz",
                    "Archive exists.",
                ),
            ],
            challenge="Run `sar -u 1 3` (or note unavailability) and save output to `sar.txt`.",
            interview=[
                (
                    "What does a high `r` column in vmstat suggest?",
                    "Runnable processes waiting for CPU — possible CPU saturation.",
                ),
                (
                    "What is I/O wait (`wa`)?",
                    "CPU time waiting on outstanding block I/O — often slow disks or overloaded storage.",
                ),
                (
                    "Why take multiple samples?",
                    "A single second can be noise; trends across intervals are more trustworthy.",
                ),
                (
                    "How does `free -h` help?",
                    "Shows used/available memory and swap — quick pressure check.",
                ),
                (
                    "When is `iostat` more useful than `vmstat`?",
                    "When you need per-device disk utilisation and latency-related counters.",
                ),
            ],
            related_prev_title="Logging — syslog, journald, logrotate",
            related_prev="logging-syslog-journald-logrotate.md",
            related_next_title="SSH Hardening and Firewalls",
            related_next="ssh-hardening-and-firewalls.md",
        ),
        dict(
            slug="troubleshooting-linux-systems.md",
            title="Troubleshooting Linux Systems",
            desc="Use a structured triage checklist for boot, CPU, memory, disk, permissions, network, and service failures.",
            module="Module 15 · Troubleshooting",
            tut_n=23,
            mod_n=15,
            tags=["linux", "troubleshooting", "incident"],
            prereq=["linux/containers-namespaces-cgroups-and-oci"],
            nxt=["linux/production-linux-hardening-and-performance"],
            diagram="linux-troubleshooting.svg",
            lab="lab23",
            overview="Troubleshooting is a method, not guesswork. You gather blast radius, recent changes, and host signals — CPU, memory, disk, failed units, network listeners — then change one thing at a time with evidence.",
            theory_what="A good triage loop: define the symptom, check scope, collect host facts, form a hypothesis, test carefully, record the result.",
            theory_why="On-call engineers who jump to random restarts create bigger outages. Structured checks are what senior interviews look for.",
            theory_how="```bash\nsystemctl --failed\ndf -h\nfree -h\nip -br a\njournalctl -p err -n 50\n```",
            table="| Area | First commands |\n|------|----------------|\n| Services | `systemctl --failed` |\n| Disk | `df -h`, `df -i` |\n| Memory | `free -h`, `vmstat` |\n| Network | `ip -br a`, `ss -lntu` |",
            pitfalls=[
                "Restarting services before collecting logs",
                "Changing many things at once",
                "Ignoring recent deployments",
            ],
            scenario="A VM is 'broken' according to a ticket with little detail. You run a standard triage script and attach the evidence bundle.",
            tasks=[
                (
                    "Service and resource snapshot",
                    "Failed units, disk, memory.",
                    "systemctl --failed --no-pager 2>/dev/null | tee failed-units.txt || echo 'no-systemd' | tee failed-units.txt\ndf -h | tee df.txt\ndf -i | tee dfi.txt\nfree -h | tee free.txt\nuptime | tee uptime.txt",
                    "Snapshot files exist.",
                ),
                (
                    "Network and journal errors",
                    "Listeners and recent errors.",
                    "ip -br a 2>/dev/null | tee ip.txt || true\nss -lntu 2>/dev/null | tee ss.txt || true\njournalctl --no-pager -p err -n 50 2>/dev/null | tee journal-err.txt || echo 'no-journal' | tee journal-err.txt",
                    "Network/journal evidence saved.",
                ),
                (
                    "Build triage bundle",
                    "One archive for the ticket.",
                    "{\n  echo \"# Triage $(date -u +%Y-%m-%dT%H:%M:%SZ)\"\n  echo \"## Hypothesis placeholder\"\n  echo \"Fill after reading evidence.\"\n} | tee triage-notes.md\ntar -czf lab23-triage.tgz failed-units.txt df.txt dfi.txt free.txt uptime.txt ip.txt ss.txt journal-err.txt triage-notes.md\nls -l lab23-triage.tgz",
                    "`lab23-triage.tgz` exists.",
                ),
            ],
            challenge="Add `ps aux --sort=-%mem | head -n 15` output to `top-mem.txt` and rebuild the triage archive.",
            interview=[
                (
                    "What is your first minute on a 'server down' call?",
                    "Confirm scope and access, check recent changes, then gather failed units, disk, memory, and network facts before changing anything.",
                ),
                (
                    "Why collect logs before restart?",
                    "Restart clears volatile state and may destroy evidence needed for root cause.",
                ),
                (
                    "How do disk and inode full conditions differ?",
                    "Bytes full vs inode table full — both block new files; check `df -h` and `df -i`.",
                ),
                (
                    "What does `systemctl --failed` tell you?",
                    "Which units entered failed state — a fast service-layer signal.",
                ),
                (
                    "How do you avoid flailing during incidents?",
                    "One hypothesis at a time, evidence for each step, and a written timeline.",
                ),
            ],
            related_prev_title="Containers — Namespaces, cgroups, and OCI",
            related_prev="containers-namespaces-cgroups-and-oci.md",
            related_next_title="Production Hardening and Performance",
            related_next="production-linux-hardening-and-performance.md",
            difficulty="advanced",
        ),
        dict(
            slug="production-linux-hardening-and-performance.md",
            title="Production Linux — Hardening and Performance",
            desc="Capture a production baseline: update posture, SSH settings summary, sysctl reads, and performance signals — without locking yourself out.",
            module="Module 16 · Production Linux",
            tut_n=24,
            mod_n=16,
            tags=["linux", "hardening", "performance"],
            prereq=["linux/troubleshooting-linux-systems"],
            nxt=["linux/backup-disaster-recovery-and-capacity"],
            diagram="linux-production.svg",
            lab="lab24",
            overview="Production Linux means repeatable hardening and known performance baselines. You verify updates, SSH posture, kernel tunables, and resource signals — carefully, with evidence, never improvising lockout-prone changes on a live bastion without a second path.",
            theory_what="Hardening reduces attack surface (updates, SSH, firewall, least privilege). Performance work starts with baselines (`vmstat`, load, disk). Both need checklists and proof.",
            theory_why="Unpatched hosts get compromised. Untuned hosts fail under load. Audits ask for evidence, not intentions.",
            theory_how="```bash\nuname -a\nsudo sshd -T 2>/dev/null | head\nsysctl net.ipv4.ip_forward\n```",
            table="| Area | Example check |\n|------|----------------|\n| Identity | `uname`, `os-release` |\n| SSH | `sshd -T` subset |\n| Updates | apt/dnf check |\n| Performance | vmstat/free |",
            pitfalls=[
                "Hardening SSH without a second session",
                "Tuning sysctl without measuring",
                "No rollback plan",
            ],
            scenario="Security asks for a baseline report of a new Ubuntu VM before it joins the fleet. You collect read-mostly evidence.",
            tasks=[
                (
                    "Identity and updates posture",
                    "OS identity and pending updates signal.",
                    "uname -a | tee uname.txt\ncat /etc/os-release | tee os-release.txt\nif command -v apt-get >/dev/null; then sudo apt-get update -qq && apt list --upgradable 2>/dev/null | tee upgradable.txt || true; else echo 'non-apt' | tee upgradable.txt; fi",
                    "Identity files exist.",
                ),
                (
                    "SSH and sysctl read-only checks",
                    "Do not change sshd — only read.",
                    "sudo sshd -T 2>/dev/null | egrep 'passwordauthentication|permitrootlogin|pubkeyauthentication' | tee sshd-t.txt || echo 'sshd-T-unavailable' | tee sshd-t.txt\nsysctl net.ipv4.ip_forward kernel.hostname 2>/dev/null | tee sysctl.txt\nvmstat 1 3 | tee vmstat.txt\nfree -h | tee free.txt",
                    "Read-only hardening/performance signals saved.",
                ),
                (
                    "Baseline bundle",
                    "Pack for the audit ticket.",
                    "tar -czf lab24-baseline.tgz uname.txt os-release.txt upgradable.txt sshd-t.txt sysctl.txt vmstat.txt free.txt\nls -l lab24-baseline.tgz",
                    "Baseline archive exists.",
                ),
            ],
            challenge="Add `sudo ufw status verbose` or `sudo firewall-cmd --state` output to `firewall.txt` ( whichever exists) and rebuild the archive.",
            interview=[
                (
                    "What is a safe first step in SSH hardening?",
                    "Open a second session, validate `sshd -t`, prefer drop-in config, and never disable your only access path.",
                ),
                (
                    "Why collect baselines before tuning?",
                    "Without before/after numbers you cannot prove improvement or detect regressions.",
                ),
                (
                    "Name three hardening domains on a Linux VM.",
                    "Patching, access (SSH/sudo), and network exposure (firewall/security groups).",
                ),
                (
                    "What does `sshd -T` do?",
                    "Prints effective sshd configuration — useful for audits without guessing live settings.",
                ),
                (
                    "Why can performance 'fixes' make things worse?",
                    "Blind sysctl changes can break networking or overload disks; measure, change one variable, re-measure.",
                ),
            ],
            related_prev_title="Troubleshooting Linux Systems",
            related_prev="troubleshooting-linux-systems.md",
            related_next_title="Backup, Disaster Recovery, and Capacity",
            related_next="backup-disaster-recovery-and-capacity.md",
            difficulty="advanced",
        ),
        dict(
            slug="backup-disaster-recovery-and-capacity.md",
            title="Backup, Disaster Recovery, and Capacity",
            desc="Practise backup and restore with tar/rsync, and connect capacity planning to real df/du evidence.",
            module="Module 16 · Production Linux",
            tut_n=25,
            mod_n=16,
            tags=["linux", "backup", "dr", "capacity"],
            prereq=["linux/production-linux-hardening-and-performance"],
            nxt=[],
            diagram="linux-backup-dr.svg",
            lab="lab25",
            overview="Backups are useless until you restore them. Disaster recovery (DR) is the plan for that restore under time pressure. Capacity planning watches growth so you do not learn about disk limits during an outage.",
            theory_what="`tar` and `rsync` are common host-level backup tools. Restores must be tested. Capacity uses `df`/`du` trends and alert thresholds.",
            theory_why="Cloud snapshots help, but application-consistent backups and restore drills are still your job. Interviews love restore stories.",
            theory_how="```bash\ntar -czf backup.tgz data\nrsync -a data/ restore/\n```",
            table="| Idea | Practice |\n|------|----------|\n| Backup | Copy data off-box |\n| Restore test | Prove files return |\n| RPO/RTO | How much data/time you can lose |\n| Capacity | Watch growth early |",
            pitfalls=[
                "Never testing restore",
                "Backups on the same disk only",
                "No owner for capacity alerts",
            ],
            scenario="You must show a teammate a working backup/restore of application data and a capacity snapshot for the ticket.",
            tasks=[
                (
                    "Create data and back it up",
                    "Sample dataset + tar backup.",
                    "mkdir -p data\necho 'important' > data/app.txt\nprintf 'v1\\n' > data/version.txt\ntar -czf backup-$(date +%Y%m%d).tgz data\nls -l backup-*.tgz | tee backup-ls.txt\ntest -s backup-ls.txt",
                    "A non-empty `.tgz` backup exists.",
                ),
                (
                    "Restore and verify",
                    "Prove restore works.",
                    "rm -rf restore && mkdir restore\nBK=$(ls -1 backup-*.tgz | head -n1)\ntar -xzf \"$BK\" -C restore\ntest -f restore/data/app.txt\ngrep -q important restore/data/app.txt\nrsync -a data/ restore-rsync/\ntest -f restore-rsync/app.txt\necho restore-ok | tee restore-ok.txt",
                    "`restore-ok.txt` exists; restored files match.",
                ),
                (
                    "Capacity snapshot",
                    "df/du evidence.",
                    "df -h . | tee capacity-df.txt\ndu -sh data backup-*.tgz restore restore-rsync 2>/dev/null | tee capacity-du.txt\ntar -czf lab25-evidence.tgz backup-ls.txt restore-ok.txt capacity-df.txt capacity-du.txt\nls -l lab25-evidence.tgz",
                    "Capacity evidence archived.",
                ),
            ],
            challenge="Write `rpo-rto-notes.txt` stating example RPO/RTO targets for this lab data in your own words (one sentence each).",
            interview=[
                (
                    "Why test restores, not only backups?",
                    "Backups can be corrupt or incomplete; only a restore proves recoverability.",
                ),
                (
                    "What are RPO and RTO?",
                    "Recovery Point Objective (how much data loss is acceptable) and Recovery Time Objective (how fast you must recover).",
                ),
                (
                    "Why is same-disk backup weak?",
                    "Disk failure loses both data and backup. Keep off-system copies.",
                ),
                (
                    "How does capacity planning reduce incidents?",
                    "You expand volumes or clean data before hard failures during peak traffic.",
                ),
                (
                    "When is `rsync` useful versus `tar`?",
                    "`rsync` efficiently syncs trees and can resume; `tar` is handy for point-in-time archives.",
                ),
            ],
            related_prev_title="Production Linux — Hardening and Performance",
            related_prev="production-linux-hardening-and-performance.md",
            related_next_title="Linux Overview",
            related_next="index.md",
            difficulty="advanced",
        ),
    ]

    specs.extend(finals)

    for spec in specs:
        slug = spec.pop("slug")
        text = page(**spec)
        path = LINUX / slug
        path.write_text(text, encoding="utf-8")
        print("wrote", path.relative_to(ROOT), "bytes", len(text))


if __name__ == "__main__":
    main()
