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

## Core concepts

**1. Add 50GB to /opt using LVM without any downtime. What are the steps?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Linux, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**2. What is LVM, and why is it useful in DevOps?**

??? success "Reveal answer"
    LVM lets me manage disks flexibly by creating logical volumes that can span multiple physical disks, enabling
    dynamic resizing and snapshots -- genuinely useful in environments that need to scale storage needs on the fly, like
    cloud infrastructure.

**3. What is the difference between a process and a thread?**

??? success "Reveal answer"
    A process is an independent program with its own memory space. A thread is a lightweight unit 
    of execution within a process, sharing the same memory. Processes are isolated; threads share 
    resources and communicate faster but risk race conditions.

**4. What are runlevels in Linux, and how do they affect system startup?**

??? success "Reveal answer"
    Runlevels define which services run in a given operational mode -- single-user, multi-user, reboot/shutdown. Modern
    systemd-based systems have largely replaced runlevels with targets like multi-user.target and graphical.target
    instead.

**5. Explain the difference between a process and a daemon in Linux.**

??? success "Reveal answer"
    A process is a running instance of a program identified by a unique PID. A daemon is a background process, typically
    started at boot, that runs continuously performing a specific ongoing task -- things like sshd or cron.

**6. What is the purpose of iptables in Linux?**

??? success "Reveal answer"
    iptables is a command-line firewall utility for configuring packet filtering, NAT, and routing rules -- used in DevOps to
    secure systems by controlling exactly what traffic is allowed in and out based on defined rules.

**7. What is SSH and how is it useful in a DevOps context?**

??? success "Reveal answer"
    SSH is a cryptographic protocol for secure communication between machines, and it's fundamental to DevOps work
    -- remote server access, executing commands remotely, and securely transferring files all run through it.

**8. How do servers get connected in Linux? explain?**

??? success "Reveal answer"
    Answer directly for Linux: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**9. What is the role of cron in Linux?**

??? success "Reveal answer"
    cron is a time-based job scheduler that runs tasks automatically at specified times or intervals -- I use it for
    scheduling maintenance tasks, backups, and automated scripts that need to run on a recurring schedule.

**10. Explain how Linux file permissions work (rwx).**

??? success "Reveal answer"
    Permissions split into owner, group, and others, each with read, write, and execute bits -- something like rwxr-xr--
    means the owner has full access, the group can read and execute, and everyone else can only read.

**11. What is the difference between kill and kill -9?**

??? success "Reveal answer"
    kill sends SIGTERM (15) — a polite request to terminate, allowing cleanup. kill -9 sends 
    SIGKILL — immediately terminates; cannot be caught or ignored by the process.

**12. Explain how you can schedule a one-time task in Linux.**

??? success "Reveal answer"
    The at command schedules a one-time task -- echo "sh backup.sh" | at 02:00 runs backup.sh at 2 AM. atq shows
    pending jobs, and atrm removes them.

**13. Explain the purpose of the chmod command in Linux.**

??? success "Reveal answer"
    chmod changes file or directory permissions, controlling read, write, and execute access separately for the owner,
    group, and others.

## Scenarios and troubleshooting

**14. How do you troubleshoot 1/0 wait issues on Linux?**

??? success "Reveal answer"
    + Check iostat -x 1 to see Hiowait. Understanding of 1/0 wait
    =) + Use vmstat 1 to confirm (wa column), cat Se sas ae
    + Check which process is causing I/0: pidstat -d 1. eee
    process is causing pidstat 4 -
    9 + Check disk health: smartctl -a /dev/sdX. = Storage performance knowledge
    + Look for large sequential reads /writes or high latency, am Reet cause cenalits
    : ; + Optimize queries, move data, upgrade disk if needed. # Optimisation mindsst |
    @)

**15. What is a kernel panic, and how would you troubleshoot it?**

??? success "Reveal answer"
    A kernel panic is a system crash from an unrecoverable kernel error. I'd check /var/log/kern.log or journalctl for the
    messages leading up to the panic, use dmesg to look for hardware or driver issues, and consider memory testing or
    reviewing recent kernel updates as likely culprits.

**16. How would you troubleshoot a Linux system that is running out of memory?**

??? success "Reveal answer"
    Check memory usage with free -h or vmstat, identify the memory-hogging process with top or htop, review swap
    usage with swapon -s, check for memory leaks with ps aux --sort=-%mem or smem, and analyze dmesg for
    kernel-level memory issues or OOM killer activity.

**17. How to troubleshoot the issue and what will be checked during the process?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Linux, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**18. how will you troubleshoot if a system goes down in Linux - tell the commands?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Linux, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**19. How would you schedule a task to run every 15 minutes in windows using powershell and linux with cron?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Linux components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**20. How would you deal with high CPU usage on a Linux server?**

??? success "Reveal answer"
    Identify the culprit process with top or htop, adjust its priority with nice or renice if appropriate, check whether the load
    is genuinely CPU-bound versus stemming from high I/O or memory pressure, review system logs for related errors,
    and optimize or tune the specific application if it turns out to be the actual root cause.

**21. How would you optimize a Linux system for performance?**

??? success "Reveal answer"
    Disable unnecessary services with systemctl, tune kernel parameters via sysctl, monitor and manage disk I/O with
    iotop and use faster storage where it matters, adjust swappiness to control how aggressively the system swaps, and
    use profiling tools like perf to actually find bottlenecks instead of guessing.

## Practice questions

**22. How you connect to private instances when the SSH connection is not working?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Linux, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**23. You’re locked out via SSH with no root access. How do you recover?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Linux components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**24. In Linux, how do you attach and detach a filesystem?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Linux components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**25. How do you print the last 15 lines of a file in Linux?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Linux components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**26. Diff between mount and directories in Linux?**

??? success "Reveal answer"
    Start with a precise definition in the context of Linux, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**27. How do you install a specific version of a package in Linux?**

??? success "Reveal answer"
    On Debian/Ubuntu, apt-cache policy lists available versions and sudo apt-get install = installs a specific one. On Red
    Hat/CentOS, yum --showduplicates list shows available versions and sudo yum install - installs it.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    2
    1
    SONARQUBE

**28. How do you monitor system performance in Linux?**

??? success "Reveal answer"
    top or htop for real-time CPU, memory, and process usage; vmstat for system performance stats; iostat for disk I/O;
    netstat or ss for network connections and traffic; and sar from the sysstat package for comprehensive, historical
    performance data.

**29. How do you find running processes ?**

??? success "Reveal answer"
    $ ps aux | head
    user 1234 0.1 1.2 12345 ? Ss 10:11 0:00 nginx
    => Use ps aux, top, or htop. user 2345 0.0 0.5 6789? $ 10:11 0:00 sshd
    @ How do you stop a Linux process? 7
    —> Use kill <PID> or kill -4 <PID> [su 1206
    when graceful termination fails.

**30. How to create a user without an SSH access?**

??? success "Reveal answer"
    Outline the solution first, then give a minimal correct example (commands or config sketch).
    
    Call out the production hardening you would add next (pin versions, least privilege, secrets, health checks) and how you would validate the result.

**31. Write a shell script where you have one virtual machine ubuntu1, auto ssh enabled, ssh -i for private key, directory path /nobackup to be copied in another VM?**

??? success "Reveal answer"
    Outline the solution first, then give a minimal correct example (commands or config sketch).
    
    Call out the production hardening you would add next (pin versions, least privilege, secrets, health checks) and how you would validate the result.

**32. How can you manage software packages in Ubuntu/Debian-based systems?**

??? success "Reveal answer"
    apt commands like apt-get or apt-cache handle installing, removing, updating, or searching for packages -- sudo
    apt-get install being the most common one.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**33. How to set a CPU and memory limit in Linux machine?**

??? success "Reveal answer"
    Answer directly for Linux: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**34. When you run a module like yum or apt and get “command not found,” what’s the reason?**

??? success "Reveal answer"
    Answer directly for Linux: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**35. Do you have experience with operating systems — Windows or Linux? What types of file permissions exist in Linux?**

??? success "Reveal answer"
    Answer directly for Linux: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**36. how to find the mount point space of linux?**

??? success "Reveal answer"
    Answer directly for Linux: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**37. If vm deployed in private subent how can you do patch updates like apt update?**

??? success "Reveal answer"
    Answer directly for Linux: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**38. Whats ur organisation current cicd process and tools?**

??? success "Reveal answer"
    Answer directly for Linux: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**39. How to check the linux process?**

??? success "Reveal answer"
    Answer directly for Linux: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**40. How to check load of linux machine?**

??? success "Reveal answer"
    Answer directly for Linux: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**41. How to kill the running process?**

??? success "Reveal answer"
    Answer directly for Linux: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**42. How to check linux process without use of ps or top command?**

??? success "Reveal answer"
    Answer directly for Linux: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**43. How do you check the free disk space in Linux?**

??? success "Reveal answer"
    df shows disk space usage across mounted filesystems, and df -h gives that same output in a human-readable
    format -- that's the first thing I check when a server is behaving oddly and disk pressure is a suspect.

**44. What does the chmod 755 command do?**

??? success "Reveal answer"
    Sets file permissions: owner gets read+write+execute (7), group gets read+execute (5), others get 
    read+execute (5). The 7 = 4+2+1, 5 = 4+0+1.

## Related

- Course: [Linux](../linux/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
