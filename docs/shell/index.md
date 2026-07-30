---
title: Overview
description: "Shell Scripting for DevOps Engineers — 18 modules covering Bash fundamentals through production automation, jq/yq, scheduling, and troubleshooting."
difficulty: beginner
estimated_time: "6–8 weeks"
author: Shaik Basha
last_updated: "2026-07-29"
category: shell
tags:
  - shell
  - bash
  - devops
  - course
comments: false
---

# Shell Scripting for DevOps Engineers

**Duration:** 6–8 weeks (≈ 30–45 hours contact time)
{ .ra-facts }

Practical Bash for Linux administration, cloud automation, DevOps, and Platform Engineering — real-world automation, not academic scripting.

!!! tip "Course status"
    **Track ready** — **18 modules · 18 tutorials**, labs, quiz, cheat sheet, interview prep, and projects. Start with [Shell Fundamentals — Bash vs sh and Execution](shell-fundamentals-bash-vs-sh-and-execution.md).

---

## 1. Course overview

### Purpose

Automate repetitive operational tasks, ship production-ready shell scripts, and troubleshoot Linux systems efficiently.

### Target roles

Linux Administrator · DevOps · Cloud · Platform · SRE · DevSecOps · Infrastructure Engineer

### Prerequisites

- [Linux Fundamentals](../linux/index.md) (Modules 1–4 recommended)
- Bash 4.2+ on Linux (WSL2/VM/cloud)

### Capstone outcomes

Write production-quality Bash · automate Linux admin · build reusable tools · debug efficiently · process JSON/YAML · schedule jobs · secure scripts · support DevOps/Platform workflows.

### Certification mapping (light)

| Theme | RHCSA/LFCS | RHCE/LFCE | Modules |
|-------|:----------:|:---------:|---------|
| Shell basics / scripting | ● | ○ | 1–7 |
| Text / files | ● | ○ | 9–10 |
| Processes / services | ● | ● | 11–12 |
| Networking / SSH | ● | ● | 13 |
| Scheduling | ● | ● | 15 |
| Hardening / production | ○ | ● | 16–18 |

---

## 2. Modules and tutorials

### Module 1 — Shell Fundamentals

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 1 | [Shell Fundamentals — Bash vs sh and Execution](shell-fundamentals-bash-vs-sh-and-execution.md) | Beginner | 45 min |

**Topics:** What is a Shell · Bash vs sh · Shell Execution · Interactive vs Non-interactive · Login Shell · Environment Variables

### Module 2 — Writing Your First Script

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 2 | [Writing Your First Script](writing-your-first-script.md) | Beginner | 45 min |

**Topics:** Shebang · Executable Files · Running Scripts · Exit Codes · Comments · Script Structure

### Module 3 — Variables

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 3 | [Variables, Quoting, and Arithmetic](variables-quoting-and-arithmetic.md) | Beginner | 50 min |

**Topics:** Variables · Constants · Environment Variables · Command Substitution · Arithmetic · Quoting Rules

### Module 4 — Input & Output

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 4 | [Input, Output, Redirection, and Pipes](input-output-redirection-and-pipes.md) | Beginner | 50 min |

**Topics:** echo · printf · read · stdin · stdout · stderr · Redirection · Pipes

### Module 5 — Control Flow

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 5 | [Control Flow — Conditionals](control-flow-conditionals.md) | Intermediate | 50 min |

**Topics:** if · elif · else · case · test · `[[ ]]` · Logical Operators

### Module 6 — Loops

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 6 | [Loops — for, while, until](loops-for-while-until.md) | Intermediate | 50 min |

**Topics:** for · while · until · break · continue · Nested Loops

### Module 7 — Functions

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 7 | [Functions, Parameters, and Locals](functions-parameters-and-locals.md) | Intermediate | 50 min |

**Topics:** Function Declaration · Parameters · Return Values · Local Variables · Reusable Functions

### Module 8 — Arrays & Strings

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 8 | [Arrays and String Manipulation](arrays-and-string-manipulation.md) | Intermediate | 50 min |

**Topics:** Indexed Arrays · Associative Arrays · String Manipulation · Pattern Matching

### Module 9 — File Operations

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 9 | [File Operations in Shell](file-operations-in-shell.md) | Intermediate | 50 min |

**Topics:** Reading Files · Writing Files · Temporary Files · File Tests · Directory Operations

### Module 10 — Text Processing

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 10 | [Text Processing in Shell Scripts](text-processing-in-shell-scripts.md) | Intermediate | 55 min |

**Topics:** grep · sed · awk · cut · tr · sort · uniq · paste · xargs

### Module 11 — Process Automation

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 11 | [Process Automation — Signals and Traps](process-automation-signals-and-traps.md) | Intermediate | 55 min |

**Topics:** ps · kill · pkill · nohup · jobs · wait · Signals · Trap

### Module 12 — Linux Administration

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 12 | [Linux Admin Automation](linux-admin-automation.md) | Intermediate | 55 min |

**Topics:** User Management · Package Management · Service Management · Log Rotation · Disk Usage · Backup Automation

### Module 13 — Networking Automation

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 13 | [Networking Automation with Shell](networking-automation-with-shell.md) | Intermediate | 55 min |

**Topics:** ping · curl · wget · nc · dig · SSH · SCP · rsync

### Module 14 — JSON & YAML

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 14 | [JSON and YAML with jq and yq](json-and-yaml-with-jq-yq.md) | Intermediate | 50 min |

**Topics:** jq · yq · Parsing JSON · Parsing YAML · Configuration Files

### Module 15 — Scheduling

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 15 | [Scheduling — cron, at, and Timers](scheduling-cron-at-and-timers.md) | Intermediate | 50 min |

**Topics:** cron · crontab · at · systemd Timers

### Module 16 — Error Handling

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 16 | [Error Handling, Logging, and Debugging](error-handling-logging-and-debugging.md) | Advanced | 55 min |

**Topics:** Exit Codes · Trap · Defensive Programming · Logging · Debugging

### Module 17 — Production Shell Scripting

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 17 | [Production Shell Scripting](production-shell-scripting.md) | Advanced | 60 min |

**Topics:** ShellCheck · Idempotent Scripts · Secure Scripting · Logging · Retry Logic · Lock Files · Configuration Management

### Module 18 — Troubleshooting

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 18 | [Troubleshooting Shell Scripts](troubleshooting-shell-scripts.md) | Advanced | 55 min |

**Topics:** Debugging Bash · Common Errors · Permission Problems · Cron Issues · Variable Expansion Problems · Performance Optimisation

---

## 3. Practice

### Labs

Browse **Labs → Shell Scripting** in the sidebar, or:

| Lab | Focus |
|-----|--------|
| [Create Your First Script](../labs/shell-first-script.md) | First script |
| [User Management Script](../labs/shell-user-management-script.md) | Users |
| [Automate Software Installation](../labs/shell-automate-software-installation.md) | Packages |
| [Backup Utility](../labs/shell-backup-utility.md) | Backups |
| [Rotate Logs](../labs/shell-rotate-logs.md) | logrotate-style |
| [Monitor Disk Usage](../labs/shell-monitor-disk-usage.md) | Disk |
| [Monitor CPU & Memory](../labs/shell-monitor-cpu-memory.md) | Metrics |
| [Service Health Checker](../labs/shell-service-health-checker.md) | systemd |
| [SSL Certificate Monitor](../labs/shell-ssl-certificate-monitor.md) | TLS expiry |
| [Parse JSON with jq](../labs/shell-parse-json-jq.md) | jq |
| [Parse YAML with yq](../labs/shell-parse-yaml-yq.md) | yq |
| [Automate SSH Tasks](../labs/shell-automate-ssh-tasks.md) | SSH |
| [Deployment Script](../labs/shell-deployment-script.md) | Deploy |
| [Linux Operations Toolkit](../labs/shell-linux-operations-toolkit.md) | Toolkit |
| [Shell Ops Script Hardening](../labs/shell-ops-script-hardening.md) | Hardening |

### Projects

| Level | Project |
|-------|---------|
| Beginner | [Linux Automation Scripts](../projects/shell-linux-automation-scripts.md) |
| Intermediate | [Linux Administration Toolkit](../projects/shell-linux-administration-toolkit.md) |
| Advanced | [Production Operations Toolkit](../projects/shell-production-operations-toolkit.md) |
| Capstone | [Production Shell Automation Framework](../projects/shell-production-automation-framework.md) |

### Assessment & reference

- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md) (40 Q)
- [Cheat sheet](../cheatsheets/shell.md) · [Interview prep](../interview/shell.md)

---

## Start here

1. [Shell Fundamentals — Bash vs sh and Execution](shell-fundamentals-bash-vs-sh-and-execution.md)
2. Use `set -euo pipefail` from your first real script onward
3. After Module 14–17, continue to [Python for DevOps](../python/index.md) for APIs and packaged CLIs

## Related

- Prerequisite: [Linux](../linux/index.md)
- Next: [Python for DevOps](../python/index.md)
- [DevOps Engineer path](../career-paths/devops-engineer/index.md)
- [Getting Started](../getting-started/index.md)
- [Labs](../labs/index.md)
