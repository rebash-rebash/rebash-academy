---
title: "Linux Interview Preparation"
description: "54 curated Linux interview prompts — model answers plus real interview questions collected across companies (deduplicated by topic)."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. What is LVM, and why is it useful in DevOps?**

??? success "Reveal answer"
    LVM lets me manage disks flexibly by creating logical volumes that can span multiple physical disks, enabling
    dynamic resizing and snapshots -- genuinely useful in environments that need to scale storage needs on the fly, like
    cloud infrastructure.

**2. What is the difference between a process and a thread?**

??? success "Reveal answer"
    A process is an independent program with its own memory space. A thread is a lightweight unit 
    of execution within a process, sharing the same memory. Processes are isolated; threads share 
    resources and communicate faster but risk race conditions.

**3. What is eBPF?**

??? success "Reveal answer"
    Extended Berkeley Packet Filter — a technology for running sandboxed programs in the Linux 
    kernel. Enables high-performance networking, observability, and security without kernel modules. 
    Powers Cilium (Kubernetes networking) and Falco.

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

**8. What is the role of cron in Linux?**

??? success "Reveal answer"
    cron is a time-based job scheduler that runs tasks automatically at specified times or intervals -- I use it for
    scheduling maintenance tasks, backups, and automated scripts that need to run on a recurring schedule.

**9. What is a zombie process?**

??? success "Reveal answer"
    A process that has finished execution but still has an entry in the process table because its parent 
    hasn't read its exit status via wait(). It consumes minimal resources but indicates a bug in the 
    parent process.

**10. Explain how Linux file permissions work (rwx).**

??? success "Reveal answer"
    Permissions split into owner, group, and others, each with read, write, and execute bits -- something like rwxr-xr--
    means the owner has full access, the group can read and execute, and everyone else can only read.

**11. What is a symlink in Linux?**

??? success "Reveal answer"
    A symlink is a file that points to another file or directory, acting as an indirect reference -- if the target moves or is
    deleted, the symlink breaks, which is worth remembering when scripts depend on one.

**12. What is a blameless postmortem?**

??? success "Reveal answer"
    A postmortem that focuses on system and process failures, not individual blame. The goal is 
    learning and improvement, not punishment. Psychological safety is essential for honest reporting.

**13. What is the difference between kill and kill -9?**

??? success "Reveal answer"
    kill sends SIGTERM (15) — a polite request to terminate, allowing cleanup. kill -9 sends 
    SIGKILL — immediately terminates; cannot be caught or ignored by the process.

**14. Explain how you can schedule a one-time task in Linux.**

??? success "Reveal answer"
    The at command schedules a one-time task -- echo "sh backup.sh" | at 02:00 runs backup.sh at 2 AM. atq shows
    pending jobs, and atrm removes them.

**15. Explain the purpose of the chmod command in Linux.**

??? success "Reveal answer"
    chmod changes file or directory permissions, controlling read, write, and execute access separately for the owner,
    group, and others.

**16. What is a CronJob?**

??? success "Reveal answer"
    A Kubernetes resource that creates Jobs on a scheduled basis using standard cron syntax. 
    schedule: "0 2 * * *" # Run at 2 AM daily

## Scenarios and troubleshooting

**17. A service keeps restarting or failing. How do you investigate?**

??? success "Reveal answer"
    + Check systemeth status <service>. + Systemd & logging knowledge
    + Check logs: journaletl -u <service> --no-pager -n 100. a Wolistic. tewestigation approach
    - + Review configuration syntax and recent pei « Dependency awareness
    =) + Check dependencies and ports (ss ~tulnp). + Attention to detail
    + Validate permissions, paths, and environment variables. # Reliability mindect
    + Fix issue and enable restart policy if appropriate.
    wk rer yoo Find and bill @ sembie or defunct, process? 
    ANS: + Check with ps aux | grep Z or top (lock for ‘Z" state). Si irecets/atata enderstenting
    —»9 5 Tass parink coming 16 * Linux internals awareness
    + If parent is dead, zombies files re-parented to init, wait will clean them. # Correct remediation
    ~o + If parent is alive and not reaping, restart the parent service. * Safe troubleshooting
    9 + Use kill -9 only if necessary. * Avoiding blunt-force actions —
    D a: tow de you troubleshoot high number of open file descriptors? 
    = ANS: + Check with sof | we -L and ulimit -n. + Knowledge of system limits
    + Use Lsof | sort -k2 -n | tail to…

**18. How do you troubleshoot 1/0 wait issues on Linux?**

??? success "Reveal answer"
    + Check iostat -x 1 to see Hiowait. Understanding of 1/0 wait
    =) + Use vmstat 1 to confirm (wa column), cat Se sas ae
    + Check which process is causing I/0: pidstat -d 1. eee
    process is causing pidstat 4 -
    9 + Check disk health: smartctl -a /dev/sdX. = Storage performance knowledge
    + Look for large sequential reads /writes or high latency, am Reet cause cenalits
    : ; + Optimize queries, move data, upgrade disk if needed. # Optimisation mindsst |
    @)

**19. What is a kernel panic, and how would you troubleshoot it?**

??? success "Reveal answer"
    A kernel panic is a system crash from an unrecoverable kernel error. I'd check /var/log/kern.log or journalctl for the
    messages leading up to the panic, use dmesg to look for hardware or driver issues, and consider memory testing or
    reviewing recent kernel updates as likely culprits.

**20. How would you troubleshoot a Linux system that is running out of memory?**

??? success "Reveal answer"
    Check memory usage with free -h or vmstat, identify the memory-hogging process with top or htop, review swap
    usage with swapon -s, check for memory leaks with ps aux --sort=-%mem or smem, and analyze dmesg for
    kernel-level memory issues or OOM killer activity.

**21. How would you deal with high CPU usage on a Linux server?**

??? success "Reveal answer"
    Identify the culprit process with top or htop, adjust its priority with nice or renice if appropriate, check whether the load
    is genuinely CPU-bound versus stemming from high I/O or memory pressure, review system logs for related errors,
    and optimize or tune the specific application if it turns out to be the actual root cause.

**22. How would you optimize a Linux system for performance?**

??? success "Reveal answer"
    Disable unnecessary services with systemctl, tune kernel parameters via sysctl, monitor and manage disk I/O with
    iotop and use faster storage where it matters, adjust swappiness to control how aggressively the system swaps, and
    use profiling tools like perf to actually find bottlenecks instead of guessing.

## Practice questions

**23. What does-the chmod command do ?**

??? success "Reveal answer"
    5 >
    | — It changes file and directory permissions. ee ae
    What does the chown command do? ;
    —> It changes the owner and group = = [=| hy” ° hd
    of a file or directory. te ee
    (IT) What is a symbolic link? ABB
    — A symbolic link is a file that points ba he
    to another file or directory. ae "ane. °9
    How do you check listening ports ? Oe” hai tisk evista
    — Use ss -tulpn or netstat -tulpn. the ss kom acd oy
    What is DNS? pena
    —> DNS converts domain names into IP addresses. = — > 43.184. 216.34
    What is the difference between TCP and UDP? TCP ‘UDP
    —> TCP is reliable and connection-oriented , acct . ical |
    while UDP is faster and connectionless. * Slower \. pre ee
    * Uses handshake | + No handshake
    (SYN, ACK) I
    ax JyothiMulkuntla en
    ee AC
    
    ad @eeeeee 02
    = 100 DevOps Engineer Interview Questions and Answers ‘O°
    . >)? Git and Version Control aks, ;
    ° Remote e
    | Gt) What is Git? "
    —> Git is a distributed version- control system Lf nF
    used to track Source- code changes. Se] — Jee}

**24. How do you secure a Linux server?**

??? success "Reveal answer"
    Keep the system patched with regular updates, use a firewall like ufw or iptables to restrict access, enforce SSH
    security by disabling root login and requiring key-based authentication, install fail2ban to block repeated failed login
    attempts, and monitor logs while restricting permissions on sensitive files with chmod and chown.
    KEY POINTS TO MENTION
    • Patch regularly, firewall, SSH hardening, fail2ban, log monitoring, tight file permissions

**25. How do you install a specific version of a package in Linux?**

??? success "Reveal answer"
    On Debian/Ubuntu, apt-cache policy lists available versions and sudo apt-get install = installs a specific one. On Red
    Hat/CentOS, yum --showduplicates list shows available versions and sudo yum install - installs it.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    2
    1
    SONARQUBE

**26. How do you monitor system performance in Linux?**

??? success "Reveal answer"
    top or htop for real-time CPU, memory, and process usage; vmstat for system performance stats; iostat for disk I/O;
    netstat or ss for network connections and traffic; and sar from the sysstat package for comprehensive, historical
    performance data.

**27. How do you find running processes ?**

??? success "Reveal answer"
    $ ps aux | head
    user 1234 0.1 1.2 12345 ? Ss 10:11 0:00 nginx
    => Use ps aux, top, or htop. user 2345 0.0 0.5 6789? $ 10:11 0:00 sshd
    @ How do you stop a Linux process? 7
    —> Use kill <PID> or kill -4 <PID> [su 1206
    when graceful termination fails.

**28. How can you manage software packages in Ubuntu/Debian-based systems?**

??? success "Reveal answer"
    apt commands like apt-get or apt-cache handle installing, removing, updating, or searching for packages -- sudo
    apt-get install being the most common one.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**29. How do you check the free disk space in Linux?**

??? success "Reveal answer"
    df shows disk space usage across mounted filesystems, and df -h gives that same output in a human-readable
    format -- that's the first thing I check when a server is behaving oddly and disk pressure is a suspect.

**30. What does the chmod 755 command do?**

??? success "Reveal answer"
    Sets file permissions: owner gets read+write+execute (7), group gets read+execute (5), others get 
    read+execute (5). The 7 = 4+2+1, 5 = 4+0+1.

**31. How do you create a cron job that runs every 15 minutes?**

??? success "Reveal answer"
    crontab -e 
    # Add: 
    */15 * * * * /path/to/script.sh

## Real interview prompts

Additional questions reported from real DevOps / SRE interviews. Company names are omitted — practise these out loud without notes.

- Write a shell script where you have one virtual machine ubuntu1, auto ssh enabled, ssh -i for private key, directory path /nobackup to be copied in another VM?
- Do you have experience with operating systems — Windows or Linux? What types of file permissions exist in Linux?
- How would you schedule a task to run every 15 minutes in windows using powershell and linux with cron?
- When you run a module like yum or apt and get “command not found,” what’s the reason?
- If vm deployed in private subent how can you do patch updates like apt update?
- How you connect to private instances when the SSH connection is not working?
- how will you troubleshoot if a system goes down in Linux - tell the commands?
- How to troubleshoot the issue and what will be checked during the process?
- Add 50GB to /opt using LVM without any downtime. What are the steps?
- You’re locked out via SSH with no root access. How do you recover?
- How to check linux process without use of ps or top command?
- How do you print the last 15 lines of a file in Linux?
- Whats ur organisation current cicd process and tools?
- In Linux, how do you attach and detach a filesystem?
- How to set a CPU and memory limit in Linux machine?
- How do servers get connected in Linux? explain?
- Diff between mount and directories in Linux?
- how to find the mount point space of linux?
- How to create a user without an SSH access?
- How to check load of linux machine?
- How to kill the running process?
- How to check the linux process?
- What is Iptables in linux?

## Related

- Course: [Linux](../linux/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
