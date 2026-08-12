---
title: "Linux Interview Preparation"
description: "44 curated Linux interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: linux
tags:
  - interview
  - linux
comments: false
---

{% raw %}
# Linux Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

<div class="ra-interview-qa" markdown="1">

## Core concepts

**1. Add 50GB to /opt using LVM without any downtime. What are the steps?**

??? success "Reveal answer"
    **In short:** Grow the LVM volume that backs `/opt` online — add capacity, extend the LV, then grow the filesystem without unmounting.
    
    **Key points**
    
    - Confirm filesystem and LV with `df -hT /opt`, `lsblk`, and `lvs`.
    - If needed: `pvcreate` a new disk, `vgextend`, then `lvextend -L +50G`.
    - Grow online: XFS → `xfs_growfs /opt`; ext4 → `resize2fs`.
    - Verify with `df -h /opt`.
    
    **Try this**
    
    - lsblk
    - `sudo lvs`
    - `sudo lvextend -L +50G /dev/<vg>/<lv>`
    - `sudo xfs_growfs /opt`
    
    **Trap**
    
    - Extending the wrong LV — or shrinking without shrinking the filesystem first — destroys data.

**2. What is LVM, and why is it useful in DevOps?**

??? success "Reveal answer"
    **In short:** Logical Volume Manager (LVM) pools disks so you can resize volumes without repartitioning.
    
    **Key points**
    
    - Physical Volumes feed a Volume Group; Logical Volumes are carved from the VG.
    - DevOps value: grow data volumes during incidents without rebuilding hosts.
    - Snapshots help short rollback windows before risky changes.
    - Daily tools: `pvs`, `vgs`, `lvs`, `lvextend`.
    
    **Try this**
    
    - `sudo pvs && sudo vgs && sudo lvs`
    
    **Trap**
    
    - Never shrink an LV before shrinking the filesystem — order matters.

**3. What is the difference between a process and a thread?**

??? success "Reveal answer"
    **In short:** A process owns its address space and credentials; a thread shares that space with sibling threads.
    
    **Key points**
    
    - Threads keep their own stack/registers but share memory and file descriptors.
    - Threads are cheaper; shared memory needs locks to avoid races.
    - Containers isolate processes — threads alone are not a security boundary.
    
    **Try this**
    
    - `ps -eLf | head`
    
    **Trap**
    
    - Claiming threads provide isolation like processes or containers.

**4. What are runlevels in Linux, and how do they affect system startup?**

??? success "Reveal answer"
    **In short:** Classic SysV runlevels were numbered boot states; systemd maps them to targets.
    
    **Key points**
    
    - Common map: 0 halt, 1 rescue, 3 multi-user text, 5 graphical, 6 reboot.
    - Today: `multi-user.target` ≈ 3, `graphical.target` ≈ 5.
    - The default target decides what starts after boot.
    
    **Try this**
    
    - `systemctl get-default`
    - `systemctl list-units --type=target`
    
    **Trap**
    
    - Changing the default target without console/serial access can strand the host.

**5. Explain the difference between a process and a daemon in Linux.**

??? success "Reveal answer"
    **In short:** Every running program is a process; a daemon is a long-running background process, usually under systemd.
    
    **Key points**
    
    - Daemons typically start at boot with no controlling terminal.
    - Prefer unit files (`Type=simple`/`notify`) over legacy double-fork PID files.
    - Examples: `sshd`, `chronyd`, `containerd`.
    
    **Try this**
    
    - `systemctl status ssh`
    
    **Trap**
    
    - Calling every background job a daemon without saying what restarts it on crash.

**6. What is the purpose of iptables in Linux?**

??? success "Reveal answer"
    **In short:** `iptables` configures Netfilter packet filter rules in the kernel.
    
    **Key points**
    
    - Used to allow SSH, block ranges, and DNAT service ports.
    - Many hosts now use `nftables`, `firewalld`, or `ufw` as the front end.
    - Cloud security groups sit in front — host firewall is still defence in depth.
    
    **Try this**
    
    - `sudo iptables -S`
    - `sudo nft list ruleset`
    
    **Trap**
    
    - Flushing firewall rules over SSH without a safe allow for your session.

**7. What is SSH and how is it useful in a DevOps context?**

??? success "Reveal answer"
    **In short:** Secure Shell (SSH) provides encrypted remote login, commands, and file copy — bootstrap and break-glass access.
    
    **Key points**
    
    - Prefer key-based auth (`ed25519`) and jump hosts / Session Manager.
    - Harden with `PasswordAuthentication no` and `PermitRootLogin no`.
    - Always run `sshd -t` before reload.
    
    **Try this**
    
    - `sudo sshd -t`
    - `journalctl -u ssh -e`
    
    **Trap**
    
    - Baking private keys into images or committing them to Git.

**8. How do servers get connected in Linux? explain?**

??? success "Reveal answer"
    **In short:** Servers connect over IP: addresses on interfaces, routes for next hops, sockets for listeners.
    
    **Key points**
    
    - Check `ip addr`, `ip route`, then `ss -lntp`.
    - Security groups and host firewalls must allow the port.
    - Private subnets need correct routes and peering/VPN design.
    
    **Try this**
    
    - `ip addr`
    - `ip route`
    - `ss -lntp`
    
    **Trap**
    
    - Opening more firewall ports when the real issue is nothing listening.

**9. What is the role of cron in Linux?**

??? success "Reveal answer"
    **In short:** `cron` runs commands on a calendar schedule for the system or a user.
    
    **Key points**
    
    - Common uses: backups, cert helpers, log cleanup.
    - Use absolute paths — cron’s environment is minimal.
    - systemd timers are often clearer for modern services.
    
    **Try this**
    
    - `crontab -e`
    - `*/15 * * * * /usr/local/bin/backup.sh >>/var/log/backup.log 2>&1`
    
    **Trap**
    
    - Scripts that work interactively fail in cron for missing `PATH` or wrong timezone.

**10. Explain how Linux file permissions work (rwx).**

??? success "Reveal answer"
    **In short:** Permissions are owner/group/others triples: read (`r`=4), write (`w`=2), execute (`x`=1).
    
    **Key points**
    
    - `rwxr-xr-x` is mode `755`.
    - On directories, `x` means traverse — needed for `cd`.
    - Know setuid, setgid, and the sticky bit on `/tmp`.
    
    **Try this**
    
    - `ls -l file`
    - `stat -c '%a %A %n' file`
    
    **Trap**
    
    - World-writable secrets or scripts (`777`).

**11. What is the difference between kill and kill -9?**

??? success "Reveal answer"
    **In short:** `kill` sends `SIGTERM` by default; `kill -9` sends `SIGKILL`, which cannot be caught.
    
    **Key points**
    
    - TERM lets the process clean up; KILL tears it down immediately.
    - Prefer TERM → wait → escalate.
    - Confirm PID and blast radius first.
    
    **Try this**
    
    - `kill <pid>`
    - `kill <pid>; sleep 5; kill -9 <pid>`
    
    **Trap**
    
    - Reaching for `-9` first and leaving half-written state behind.

**12. Explain how you can schedule a one-time task in Linux.**

??? success "Reveal answer"
    **In short:** For a one-time delayed job use `at`, not cron.
    
    **Key points**
    
    - `echo cmd | at now + 2 hours` or `at 23:30`.
    - Use absolute paths; environment is limited.
    - Cloud teams often prefer SSM maintenance windows or CI for audit trails.
    
    **Try this**
    
    - `echo '/usr/local/bin/patch.sh' | at now + 2 hours`
    - atq
    
    **Trap**
    
    - Assuming `atd` is installed and enabled on every image.

**13. Explain the purpose of the chmod command in Linux.**

??? success "Reveal answer"
    **In short:** `chmod` changes who can read, write, or execute a path.
    
    **Key points**
    
    - Symbolic (`u+x`) or numeric (`600`, `755`) forms both work.
    - Set modes after unpacking artefacts in pipelines.
    - `umask` affects new files; `chmod` fixes existing ones.
    
    **Try this**
    
    - `chmod u+x deploy.sh`
    - `chmod 600 secrets.env`
    
    **Trap**
    
    - `chmod -R 777` as a troubleshooting step.

## Scenarios and troubleshooting

**14. How do you troubleshoot 1/0 wait issues on Linux?**

??? success "Reveal answer"
    **In short:** High I/O wait means CPUs are idle waiting on disks — find the hot device and noisy process.
    
    **Key points**
    
    - Confirm with `vmstat 1` and `iostat -xz 1`.
    - Use `iotop -o` to see who is writing.
    - Mitigate with IOPS, quieter jobs, or less memory thrashing.
    
    **Try this**
    
    - vmstat 1
    - `iostat -xz 1`
    - `sudo iotop -o`
    
    **Trap**
    
    - Tuning CPU when steal/iowait are the real bottleneck.

**15. What is a kernel panic, and how would you troubleshoot it?**

??? success "Reveal answer"
    **In short:** A kernel panic is an unrecoverable kernel fault; collect evidence before you reboot again.
    
    **Key points**
    
    - Capture serial/console output and prior boot logs.
    - Check tainted flags and recent driver/kernel changes.
    - Boot a previous kernel; enable kdump for next time.
    
    **Try this**
    
    - `journalctl -k -b -1`
    - kdumpctl status
    
    **Trap**
    
    - Rebooting without saving console output — you lose the smoking gun.

**16. How would you troubleshoot a Linux system that is running out of memory?**

??? success "Reveal answer"
    **In short:** Treat out-of-memory as evidence: find top consumers, check cgroup limits, then fix leak or capacity.
    
    **Key points**
    
    - Search OOM killer lines in `dmesg`/`journalctl -k`.
    - Focus on available memory — page cache is normal.
    - Capture process list before restarting the offender.
    
    **Try this**
    
    - `free -h`
    - `ps aux --sort=-%mem | head`
    - `journalctl -k | grep -i oom`
    
    **Trap**
    
    - Adding huge swap as the only fix — latency collapses before stability returns.

**17. How to troubleshoot the issue and what will be checked during the process?**

??? success "Reveal answer"
    **In short:** Use a structured loop: symptom → blast radius → recent change → one hypothesis → verify.
    
    **Key points**
    
    - Define impact: who, what error, since when.
    - Check CPU, memory, disk, network, failed units, recent deploys.
    - Change one thing at a time and keep a timeline.
    
    **Try this**
    
    - uptime; free -h; df -h
    - `systemctl --failed`
    - `journalctl -p err -b --no-pager | tail -50`
    
    **Trap**
    
    - Changing three things at once so you never know what fixed it.

**18. How will you troubleshoot if a system goes down in Linux - tell the commands?**

??? success "Reveal answer"
    **In short:** If the host is unreachable, start out-of-band: cloud status, serial/SSM, then OS recovery.
    
    **Key points**
    
    - Verify power and status checks before chasing SSH.
    - Use serial console or Session Manager; GRUB previous kernel if looping.
    - With a shell: previous boot logs, failed units, network, listeners.
    
    **Try this**
    
    - `journalctl -b -1`
    - `systemctl --failed`
    - `ip a; ss -lntp`
    
    **Trap**
    
    - Opening SSH to `0.0.0.0/0` as the recovery plan.

**19. How would you schedule a task to run every 15 minutes in windows using powershell and linux with cron?**

??? success "Reveal answer"
    **In short:** Linux: cron `*/15 * * * *`; Windows: a Scheduled Task with a 15-minute repetition.
    
    **Key points**
    
    - Linux: absolute paths and redirected logs in crontab or `/etc/cron.d/`.
    - Windows: `Register-ScheduledTask` with a repeating trigger.
    - Call out timezone and least-privilege run-as account.
    
    **Try this**
    
    - `*/15 * * * * /usr/local/bin/task.sh >>/var/log/task.log 2>&1`
    - `Register-ScheduledTask with a 15-minute RepetitionInterval`
    
    **Trap**
    
    - Relative paths and interactive-only environment variables on either platform.

**20. How would you deal with high CPU usage on a Linux server?**

??? success "Reveal answer"
    **In short:** Prove high CPU with `top`/`htop`, split user/system/iowait/steal, then profile the hot PID.
    
    **Key points**
    
    - Sort processes by CPU; inspect threads with `top -H -p <pid>`.
    - Steal time often means noisy neighbours or an undersized instance.
    - Capture stacks before restarting.
    
    **Try this**
    
    - `ps aux --sort=-%cpu | head`
    - `top -H -p <pid>`
    
    **Trap**
    
    - Killing the top PID without knowing blast radius.

**21. How would you optimize a Linux system for performance?**

??? success "Reveal answer"
    **In short:** Optimise from a measured bottleneck — CPU, memory, disk, or network — not random sysctl lore.
    
    **Key points**
    
    - Fix the application before exotic kernel knobs.
    - Keep systems patched; use sensible mount options and `tuned` where relevant.
    - Disable unused services; right-size disk IOPS.
    
    **Try this**
    
    - `sar -u 1 5`
    - `iostat -xz 1`
    
    **Trap**
    
    - Copy-pasting “performance sysctl” packs without baseline and rollback.

## Practice questions

**22. How you connect to private instances when the SSH connection is not working?**

??? success "Reveal answer"
    **In short:** When SSH to a private instance fails, use Session Manager, serial console, or a jump host.
    
    **Key points**
    
    - AWS: SSM, EC2 serial console, or bastion with `ProxyJump`.
    - GCP IAP / Azure Bastion are the usual equivalents.
    - Fix security groups, routes, and `sshd` from the console.
    
    **Try this**
    
    - `aws ssm start-session --target i-...`
    - `ssh -J bastion user@private`
    
    **Trap**
    
    - Leaving a temporary world-open SSH rule after the incident.

**23. You’re locked out via SSH with no root access. How do you recover?**

??? success "Reveal answer"
    **In short:** Without SSH or root, recover via rescue: attach the root volume to a healthy helper VM and fix files.
    
    **Key points**
    
    - Stop the instance, detach root, attach to rescue, mount, repair keys/`sshd_config`.
    - Sync, detach, reattach, boot, verify.
    - Prefer SSM/serial patterns so this is rare.
    
    **Try this**
    
    - `sudo mount /dev/xvdf1 /mnt`
    - `sudo chroot /mnt`
    
    **Trap**
    
    - Editing the wrong volume or reattaching before a clean unmount.

**24. In Linux, how do you attach and detach a filesystem?**

??? success "Reveal answer"
    **In short:** Attach with `mount` (persist via UUID in `/etc/fstab`); detach with `umount` when idle.
    
    **Key points**
    
    - Cloud: attach the block device at the API, then mount in the guest.
    - If busy, find holders with `lsof`/`fuser` before forcing.
    - `findmnt` shows the live picture.
    
    **Try this**
    
    - `sudo mount /dev/nvme1n1p1 /mnt/data`
    - `sudo umount /mnt/data`
    
    **Trap**
    
    - Unmounting a volume the application is still writing to.

**25. How do you print the last 15 lines of a file in Linux?**

??? success "Reveal answer"
    **In short:** Print the last 15 lines with `tail -n 15 file`.
    
    **Key points**
    
    - `tail -f` follows a growing log.
    - Prefer `tail` over loading huge files into editors.
    - `head` reads from the start instead.
    
    **Try this**
    
    - `tail -n 15 /var/log/syslog`
    - `tail -f /var/log/syslog`
    
    **Trap**
    
    - `cat file | tail` — useless use of cat on large logs.

**26. Diff between mount and directories in Linux?**

??? success "Reveal answer"
    **In short:** `mount` attaches a filesystem at a path; a directory is only a name until something is mounted there.
    
    **Key points**
    
    - After mount, `/mnt/data` shows the other filesystem’s root.
    - `findmnt`/`df` show what sits where.
    - Bind mounts and tmpfs are mounts too.
    
    **Try this**
    
    - findmnt
    - `df -hT`
    
    **Trap**
    
    - Writing into a mount point while the volume is unmounted — data vanishes when you mount later.

**27. How do you install a specific version of a package in Linux?**

??? success "Reveal answer"
    **In short:** Pin the version in the package manager: `apt install pkg=version` or `dnf install pkg-version`.
    
    **Key points**
    
    - List candidates with `apt-cache policy` or `dnf list --showduplicates`.
    - Lock versions in images and config management.
    - Use distro hold/versionlock features for critical packages.
    
    **Try this**
    
    - `apt-cache policy nginx`
    - `sudo apt-get install nginx=1.24.*`
    
    **Trap**
    
    - Pinning one package while letting dependencies float wildly.

**28. How do you monitor system performance in Linux?**

??? success "Reveal answer"
    **In short:** Watch CPU, memory, disk, and network — plus saturation and errors, not just averages.
    
    **Key points**
    
    - Live tools: `top`, `vmstat`, `iostat`, `ss`, `sar`.
    - Long-term: node exporter + Prometheus/Grafana or cloud agents.
    - Alert on user-visible latency and errors.
    
    **Try this**
    
    - uptime
    - `free -h`
    - `iostat -xz 1`
    
    **Trap**
    
    - Alerting only on CPU% while disks are saturated.

**29. How do you find running processes?**

??? success "Reveal answer"
    **In short:** List processes with `ps`, `pgrep`, or interactive `top`/`htop`.
    
    **Key points**
    
    - `ps aux` / `ps -ef` for snapshots.
    - `systemctl status` for supervised services.
    - Use `lsof` when you need open files/sockets.
    
    **Try this**
    
    - `ps aux --sort=-%cpu | head`
    - pgrep -a nginx
    
    **Trap**
    
    - Killing lookalike PIDs from a careless grep.

**30. How to create a user without an SSH access?**

??? success "Reveal answer"
    **In short:** Create a system user with a non-login shell and no SSH authorized keys.
    
    **Key points**
    
    - `useradd --system --shell /usr/sbin/nologin …` (flags vary by distro).
    - Do not create `authorized_keys` for that account.
    - Grant only the groups/ACLs the service needs.
    
    **Try this**
    
    - `sudo useradd --system --shell /usr/sbin/nologin appuser`
    - `getent passwd appuser`
    
    **Trap**
    
    - Giving service accounts `/bin/bash` “for convenience”.

**31. Write a shell script where you have one virtual machine ubuntu1, auto ssh enabled, ssh -i for private key, directory path /nobackup to be copied in another VM?**

??? success "Reveal answer"
    **In short:** Copy `/nobackup` with `rsync` over SSH using an identity file and automation-friendly SSH options.
    
    **Key points**
    
    - Prefer `rsync -aHAX` over ad-hoc recursive `scp`.
    - Pin `ssh -i` and log exit codes.
    - Schedule with cron/systemd using absolute paths.
    
    **Try this**
    
    - `rsync -aHAX -e 'ssh -i /path/key' /nobackup/ user@vm2:/nobackup/`
    
    **Trap**
    
    - Disabling host-key checks permanently or embedding passwords in scripts.

**32. How can you manage software packages in Ubuntu/Debian-based systems?**

??? success "Reveal answer"
    **In short:** On Ubuntu/Debian, use Advanced Package Tool (APT) to update indexes and install/remove packages.
    
    **Key points**
    
    - `apt update` then `apt install`/`remove`/`purge`.
    - Prefer configuration management for desired state.
    - Use unattended upgrades carefully with change control.
    
    **Try this**
    
    - `sudo apt update`
    - `sudo apt install -y curl`
    
    **Trap**
    
    - Blind `apt upgrade` on production without a rollback path.

**33. How to set a CPU and memory limit in Linux machine?**

??? success "Reveal answer"
    **In short:** Limit CPU/memory with cgroups — usually systemd unit settings or container limits.
    
    **Key points**
    
    - systemd: `CPUQuota=` and `MemoryMax=` in a drop-in.
    - `ulimit` is easy to lose; prefer unit/cgroup limits.
    - In Kubernetes/Docker, set workload requests/limits.
    
    **Try this**
    
    - `systemctl show <unit> -p MemoryMax -p CPUQuota`
    
    **Trap**
    
    - Limits so low the service OOM-loops forever.

**34. When you run a module like yum or apt and get “command not found,” what’s the reason?**

??? success "Reveal answer"
    **In short:** `yum`/`apt` “command not found” means the wrong package manager for that OS — or a minimal image without one.
    
    **Key points**
    
    - Debian-like → `apt`; RHEL-like → `dnf`/`yum`.
    - Many containers omit package managers on purpose.
    - In Ansible, branch on OS facts instead of hard-coding `yum`.
    
    **Try this**
    
    - `command -v apt-get yum dnf`
    - `cat /etc/os-release`
    
    **Trap**
    
    - Installing `yum` on Ubuntu to paper over a bad playbook.

**35. What types of file permissions exist in Linux?**

??? success "Reveal answer"
    **In short:** Linux has standard rwx mode bits plus setuid, setgid, sticky — and optional Access Control Lists (ACLs).
    
    **Key points**
    
    - Files and directories interpret execute differently.
    - `getfacl`/`setfacl` extend the basic triad.
    - `chattr` attributes are a separate mechanism.
    
    **Try this**
    
    - `ls -l`
    - getfacl file
    
    **Trap**
    
    - Misreading ACL masks as simple `chmod` failures.

**36. How to find the mount point space of linux?**

??? success "Reveal answer"
    **In short:** Check mount-point space with `df -h /path` (and `df -i` for inodes).
    
    **Key points**
    
    - `df -hT` shows filesystem type and capacity.
    - `du -xh` finds heavy directories inside the mount.
    - Bind mounts can make “where is my space?” confusing — use `findmnt`.
    
    **Try this**
    
    - `df -hT`
    - `df -h /var`
    - `df -i`
    
    **Trap**
    
    - Cleaning the wrong mount because a bind mount hid the real disk.

**37. If vm deployed in private subent how can you do patch updates like apt update?**

??? success "Reveal answer"
    **In short:** Private-subnet VMs patch via NAT, proxy, VPC endpoints, or an internal package mirror — not a public IP.
    
    **Key points**
    
    - Ensure egress to repositories or a pull-through cache.
    - Use patch manager / Ansible for controlled windows.
    - Air-gapped sites need an internal mirror.
    
    **Try this**
    
    - `curl -I https://archive.ubuntu.com`
    - `sudo apt update`
    
    **Trap**
    
    - Attaching a public IP “just for patching” and forgetting to remove it.

**38. Whats ur organisation current cicd process and tools?**

??? success "Reveal answer"
    **In short:** Describe your real flow: Git → CI build/test/scan → artefact → deploy → verify, with the tools you actually run.
    
    **Key points**
    
    - Name VCS, CI, artefact store, and deploy mechanism (GitOps/Helm/Terraform).
    - Mention environments, approvals, and rollback.
    - Call out quality gates: tests and security scans.
    
    **Try this**
    
    - Sketch: commit → CI → artefact → deploy → verify
    
    **Trap**
    
    - Listing every buzzword tool you have never operated end-to-end.

**39. How to check the linux process?**

??? success "Reveal answer"
    **In short:** Inspect Linux processes with `ps`, `pgrep`, or `systemctl status` for units.
    
    **Key points**
    
    - `ps -ef` for a full table; sort when triage needs it.
    - Follow child processes under supervisors.
    - Use `/proc/<pid>` for deep detail.
    
    **Try this**
    
    - `ps -ef | grep [n]ginx`
    - `systemctl status nginx`
    
    **Trap**
    
    - Trusting a fuzzy grep that matches the wrong process.

**40. How to check load of linux machine?**

??? success "Reveal answer"
    **In short:** Load average is runnable + uninterruptible tasks — always compare it with CPU count.
    
    **Key points**
    
    - `uptime` + `nproc` give the first ratio.
    - High load with low CPU often means I/O wait.
    - Cross-check memory pressure and steal time in the cloud.
    
    **Try this**
    
    - uptime
    - `nproc`
    - vmstat 1 5
    
    **Trap**
    
    - Panicking at load `4` on an 8-vCPU machine without context.

**41. How to kill the running process?**

??? success "Reveal answer"
    **In short:** Stop a process with `SIGTERM` first; use `SIGKILL` only if it ignores you.
    
    **Key points**
    
    - Prefer `systemctl stop` for supervised services.
    - Confirm PID ownership before signalling.
    - Escalate only after a short wait.
    
    **Try this**
    
    - pgrep -a myapp
    - `kill <pid>`
    - `systemctl stop myapp`
    
    **Trap**
    
    - Killing the supervisor/runtime instead of the worker.

**42. How to check linux process without use of ps or top command?**

??? success "Reveal answer"
    **In short:** Without `ps`/`top`, enumerate `/proc/[0-9]*` and read `cmdline`/`status`.
    
    **Key points**
    
    - Each PID is a directory under `/proc`.
    - `cmdline` is null-separated — translate with `tr`.
    - `/proc/loadavg` still works for load.
    
    **Try this**
    
    - `ls /proc | grep -E '^[0-9]+$'`
    - `tr '\0' ' ' < /proc/1/cmdline; echo`
    
    **Trap**
    
    - Forgetting PID namespaces — inside a container `/proc` is a different view.

**43. How do you check the free disk space in Linux?**

??? success "Reveal answer"
    **In short:** Free disk space: `df -h` for mounts, `du` to find what used it.
    
    **Key points**
    
    - Check inodes with `df -i` when bytes remain but creates fail.
    - `du -xh /path | sort -h | tail` finds heavy dirs.
    - Watch open-deleted files holding space until restart.
    
    **Try this**
    
    - `df -h`
    - `df -i`
    - `du -xh /var | sort -h | tail`
    
    **Trap**
    
    - Deleting logs still held open by a process — space does not return yet.

**44. What does the chmod 755 command do?**

??? success "Reveal answer"
    **In short:** `chmod 755` sets `rwxr-xr-x`: owner full; group and others read+execute.
    
    **Key points**
    
    - Common for directories and shared scripts.
    - Wrong for secrets — use `600`/`640`.
    - Octal: 7=rwx, 5=r-x.
    
    **Try this**
    
    - `chmod 755 deploy.sh`
    - `stat -c '%a %A' deploy.sh`
    
    **Trap**
    
    - Using `755` on private keys or `.env` files.

## Related
- Course: [Linux](../linux/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
