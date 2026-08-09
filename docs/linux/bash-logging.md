---
title: "Logging — Recording Events in Bash Scripts"
description: "Add logging to Bash scripts — timestamps, log levels, file redirection, tee, logger, and production observability practices."
difficulty: intermediate
estimated_time: "80 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 10 · Bash Scripting"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - bash
  - scripting
  - logging
  - automation
  - rebash-linux-mastery
comments: false
status: ready
---

# Logging — Recording Events in Bash Scripts

> **Logging** is the process of recording important events, actions, warnings, and errors while a script is running. Good logging helps administrators understand what happened during script execution, troubleshoot failures, monitor automation, and maintain production systems. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, and Site Reliability Engineer (SRE) should implement proper logging in Bash scripts to improve observability and simplify troubleshooting.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 10: Bash Scripting → Lesson 9</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 80 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Bash Scripting</div>

<div markdown>**Lesson:** 9 of 11</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand logging
- Write log messages
- Add timestamps
- Use logging levels
- Write logs to files
- Log command output
- Use the `logger` command
- Apply production logging best practices

---

# Prerequisites

Complete:

- Modules 1–9
- Module 10 Lessons 1–8

---

# Why Learn Logging?

Imagine a backup script.

Without logging:

```bash
tar -czf backup.tar.gz /data
```

If the backup fails, there is no information about what happened.

With logging:

```bash
echo "$(date) Backup started." >> backup.log

tar -czf backup.tar.gz /data

echo "$(date) Backup completed." >> backup.log
```

Every important event is recorded.

---

# What is Logging?

Logging is the process of recording events while a program executes.

Example:

```text
Script Starts

↓

Operations

↓

Success / Failure

↓

Log File
```

Logs provide valuable information for troubleshooting and auditing.

---

# Why Logging Matters

Logging helps:

- Troubleshoot failures
- Monitor automation
- Audit script execution
- Track user actions
- Diagnose production issues
- Improve system reliability

---

# Writing to a Log File

Append text to a log file.

```bash
echo "Backup Started" >> backup.log
```

View the log.

```bash
cat backup.log
```

---

# Adding Timestamps

Include the current date and time.

```bash
echo "$(date) Backup Started" >> backup.log
```

Example output:

```text
Tue Aug 18 10:30:15 UTC 2026 Backup Started
```

---

# Custom Timestamp Format

```bash
echo "$(date '+%Y-%m-%d %H:%M:%S') Backup Started"
```

Example:

```text
2026-08-18 10:30:15 Backup Started
```

---

# Logging Levels

Production scripts often classify log messages by severity.

Common levels:

- INFO
- WARNING
- ERROR
- DEBUG

Example:

```text
INFO

Application Started

WARNING

Disk Usage High

ERROR

Backup Failed
```

---

# INFO Messages

```bash
echo "$(date) [INFO] Backup Started" >> backup.log
```

---

# WARNING Messages

```bash
echo "$(date) [WARNING] Disk Usage Above 80%" >> backup.log
```

---

# ERROR Messages

```bash
echo "$(date) [ERROR] Backup Failed" >> backup.log
```

---

# DEBUG Messages

Useful during development.

```bash
echo "$(date) [DEBUG] Variable VALUE=$VALUE" >> backup.log
```

---

# Logging Command Output

Redirect command output.

```bash
ls -l >> backup.log
```

Capture errors.

```bash
ls missing-file 2>> backup.log
```

Capture both standard output and errors.

```bash
ls /tmp >> backup.log 2>&1
```

---

# Logging with tee

Display output and save it simultaneously.

```bash
echo "Backup Started" | tee -a backup.log
```

---

# Using the logger Command

Send messages to the system log.

```bash
logger "Backup Started"
```

Example:

```bash
logger "Deployment Completed Successfully"
```

Depending on the Linux distribution, these messages are stored in the system logging service (such as syslog or journald).

---

# Create a Logging Function

```bash
log() {

    echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $1" >> backup.log
}
```

Use it.

```bash
log "Backup Started"

log "Backup Completed"
```

---

# Common Commands

Append log.

```bash
echo "Message" >> app.log
```

Timestamp.

```bash
date
```

Display log.

```bash
cat app.log
```

View live log.

```bash
tail -f app.log
```

System log.

```bash
logger "Application Started"
```

---

# Real Production Examples

Application deployment.

```bash
echo "$(date) [INFO] Deployment Started" >> deploy.log
```

Log backup.

```bash
tar -czf backup.tar.gz /data >> backup.log 2>&1
```

Restart service.

```bash
systemctl restart nginx >> deploy.log 2>&1
```

Log monitoring.

```bash
tail -f deploy.log
```

---

# Production Perspective

Logging is essential for:

- CI/CD pipelines
- Backup automation
- Monitoring scripts
- Deployment tools
- Kubernetes automation
- Cloud infrastructure
- Security auditing
- Troubleshooting production incidents

Well-structured logs significantly reduce the time required to diagnose production issues.

---

# Hands-on Lab

## Task 1

Create a log file.

```bash
echo "Script Started" >> script.log
```

---

## Task 2

Add timestamps.

```bash
echo "$(date) Running Backup" >> script.log
```

---

## Task 3

Log an INFO message.

```bash
echo "$(date) [INFO] Backup Started" >> script.log
```

---

## Task 4

Log an ERROR message.

```bash
echo "$(date) [ERROR] Backup Failed" >> script.log
```

---

## Task 5

Redirect command output.

```bash
ls -l >> script.log
```

---

## Task 6

Redirect errors.

```bash
ls missing-file >> script.log 2>&1
```

---

## Task 7

Monitor the log.

```bash
tail -f script.log
```

---

## Task 8

Create a logging function.

```bash
log() {

    echo "$(date '+%F %T') [INFO] $1" >> script.log
}

log "Script Finished"
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `echo` | Write log messages | Script logging |
| `date` | Add timestamps | Event tracking |
| `tee` | Display and save output | Interactive logging |
| `logger` | Write to system logs | System auditing |
| `tail -f` | Monitor logs | Real-time troubleshooting |
| `2>&1` | Redirect errors | Complete logging |

---

# Common Logging Mistakes

| Mistake | Solution |
|----------|----------|
| No timestamps | Always log time |
| Logging only errors | Log important events |
| Overwriting logs | Use `>>` to append |
| No log levels | Classify messages |
| Logging sensitive information | Never log passwords or secrets |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A nightly backup fails, but no one knows why.

Without logging:

```text
Backup Failed
```

No additional information is available.

Improved script:

```bash
log() {

    echo "$(date '+%F %T') [INFO] $1" >> backup.log
}

log "Backup Started"

tar -czf backup.tar.gz /data >> backup.log 2>&1

log "Backup Completed"
```

The log now records the complete execution history, making troubleshooting much easier.

---

# Best Practices

- Include timestamps in every log entry.
- Use consistent logging levels.
- Log significant events and errors.
- Redirect command output to log files when appropriate.
- Never log passwords, API keys, or other sensitive information.
- Rotate or archive large log files regularly.
- Use descriptive and consistent log messages.

---

# Common Mistakes

❌ Logging without timestamps.

✅ Avoid this mistake: logging without timestamps.

---

❌ Overwriting logs instead of appending.

✅ Prefer appending rather than overwriting logs.

---

❌ Logging sensitive credentials.

✅ Avoid this mistake: logging sensitive credentials.

---

❌ Writing unclear or inconsistent log messages.

✅ Avoid this mistake: writing unclear or inconsistent log messages.

---

❌ Ignoring log file growth over time.

✅ Always review log file growth over time.

---

# Interview Questions
## Beginner

1. What is logging?
2. Why is logging important?
3. How do you append text to a log file?
4. How do you view a log file in real time?

---

## Intermediate

1. What are common logging levels?
2. What does `2>&1` do?
3. What is the purpose of the `logger` command?
4. Why should timestamps be included in logs?

---

## Architect Level

1. How would you design logging for production automation scripts?
2. How would you prevent sensitive information from appearing in logs?
3. What logging practices improve troubleshooting in CI/CD pipelines?

---

# Summary

In this lesson, you learned:

- Logging fundamentals
- Writing log messages
- Adding timestamps
- Logging levels
- Redirecting command output
- Using `tee`
- Using the `logger` command
- Production logging best practices

Logging is an essential part of production-quality Bash scripting. Well-designed logs provide visibility into script execution, simplify troubleshooting, support auditing, and help administrators quickly identify and resolve issues in automated systems.

---

## Key Takeaways

- Log important events during script execution.
- Include timestamps in every log entry.
- Use logging levels such as INFO, WARNING, and ERROR.
- Redirect command output and errors to log files.
- Avoid logging sensitive information.
- Monitor and manage log files as part of routine system administration.

---

## What's Next?

**[Script Best Practices — Writing Professional Bash Scripts](bash-script-best-practices.md)**

You'll explore:

- Writing clean and readable scripts
- Consistent naming conventions
- Code organization
- Documentation and comments
- Input validation
- Security considerations
- Performance optimization
- Production scripting standards

By the end of the lesson, you'll be able to write professional, maintainable, secure, and production-ready Bash scripts that follow industry best practices.
