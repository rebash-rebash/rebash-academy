---
title: "nice and renice — Managing Process Priorities in Linux"
description: "Control Linux process priorities with nice and renice — understand nice values, CPU scheduling, and tune batch vs critical workloads in production."
difficulty: intermediate
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 6 · Process Management"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - nice
  - renice
  - priority
  - scheduling
  - rebash-linux-mastery
comments: false
status: ready
---

# nice and renice — Managing Process Priorities in Linux

> Linux allows multiple processes to compete for CPU time. The **nice** and **renice** commands help control **process scheduling priority**, allowing administrators to favor important workloads while reducing the impact of less critical tasks. Proper use of process priorities improves system responsiveness and overall performance in production environments.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 6: Process Management → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 55 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Process Management</div>

<div markdown>**Lesson:** 6 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand process priority
- Learn nice values
- Start processes with custom priorities
- Change the priority of running processes
- Understand CPU scheduling
- Improve application performance
- Apply priority management in production

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management and Permissions
- Module 5 – Users and Groups
- Module 6 Lessons 1–5

---

# Why Learn nice?

Imagine a production server running:

- Database
- Web Server
- Backup Job
- Log Compression
- File Synchronization

The backup job suddenly consumes all available CPU.

Users begin experiencing slow application performance.

Should the backup receive the same CPU priority as the database?

No.

Linux allows us to assign different priorities.

---

# What is Process Priority?

Linux schedules CPU time based on process priority.

Higher-priority processes generally receive CPU time before lower-priority processes when CPU resources are limited.

Priority can be adjusted using:

- `nice`
- `renice`

---

# What is a Nice Value?

A **nice value** tells the Linux scheduler how "nice" a process should be to other processes.

A **higher nice value** means the process is more willing to yield CPU time.

A **lower nice value** means the process receives higher scheduling priority.

---

# Nice Value Range

```text
-20  -------------------->  19

Highest Priority          Lowest Priority
```

| Nice Value | Meaning |
|------------|---------|
| -20 | Highest priority |
| 0 | Default priority |
| 19 | Lowest priority |

!!! note "Note"

    Regular users can usually increase the nice value (lower priority) for their own processes. Lowering the nice value (raising priority) generally requires administrative privileges.

---

# View Nice Values

Display running processes.

```bash
ps -el
```

Example:

```text
PID PRI NI CMD

245 20 0 bash

600 20 5 backup.sh
```

Observe:

```text
NI
```

This represents the **nice value**.

---

# Start a Process with a Nice Value

Default:

```bash
python app.py
```

Lower priority:

```bash
nice -n 10 python app.py
```

Verify:

```bash
ps -el
```

---

# Highest User Priority

Administrator only.

```bash
sudo nice -n -10 python app.py
```

This gives the process a higher scheduling priority.

---

# Change Priority of a Running Process

Use:

```bash
renice
```

Example:

```bash
sudo renice 5 -p 1234
```

Meaning:

```text
PID

1234

↓

Nice Value

5
```

---

# Increase Priority

Example:

```bash
sudo renice -10 -p 1234
```

Requires administrative privileges.

---

# Decrease Priority

Example:

```bash
renice 15 -p 1234
```

Regular users can generally lower the priority of their own processes by increasing the nice value.

---

# View Process Priority

```bash
ps -o pid,ni,comm
```

Example:

```text
PID NI COMMAND

1200 0 nginx

2400 10 backup
```

---

# CPU Scheduling Example

```text
Database

NI = -5

↓

Web Server

NI = 0

↓

Backup Job

NI = 15
```

The scheduler generally favors higher-priority processes when CPU resources are constrained.

---

# Common Commands

Start with default priority.

```bash
command
```

Start with custom priority.

```bash
nice -n 10 command
```

Change priority.

```bash
renice 10 -p PID
```

View priority.

```bash
ps -el
```

Display nice values.

```bash
ps -o pid,ni,comm
```

---

# Real Production Examples

Low-priority backup.

```bash
nice -n 15 tar -czf backup.tar.gz /data
```

Database maintenance.

```bash
nice -n 5 vacuumdb
```

Log compression.

```bash
nice -n 19 gzip large.log
```

Long-running reports.

```bash
nice -n 10 python report.py
```

---

# Production Perspective

Process priorities are useful for:

- Database maintenance
- Backup jobs
- Log processing
- File synchronization
- Batch processing
- CI/CD runners
- Data analytics
- Large file compression

They help ensure background workloads don't unnecessarily impact interactive users or critical services.

---

# Hands-on Lab

## Task 1

Start a low-priority process.

```bash
nice -n 10 sleep 300
```

---

## Task 2

Find its PID.

```bash
ps -ef | grep sleep
```

---

## Task 3

Display nice values.

```bash
ps -o pid,ni,comm
```

---

## Task 4

Change the priority.

```bash
renice 15 -p PID
```

Replace `PID` with the process ID from the previous task.

---

## Task 5

Verify the change.

```bash
ps -o pid,ni,comm
```

---

## Task 6

Display detailed process information.

```bash
ps -el
```

---

## Task 7

Start another process with the default priority.

```bash
sleep 300
```

Compare the nice values.

---

## Task 8

Terminate the test processes.

```bash
kill PID
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `nice` | Start a process with a custom priority | Batch jobs |
| `renice` | Change a running process priority | Performance tuning |
| `ps -el` | Display priorities | Monitoring |
| `ps -o pid,ni,comm` | Display nice values | Troubleshooting |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A nightly backup begins at midnight.

Users report:

- Slow application response
- High CPU utilization

Investigation:

```bash
top

ps -el
```

Findings:

The backup process is running with the default priority.

Solution:

Lower its scheduling priority.

```bash
sudo renice 15 -p 3456
```

Result:

- Backup continues running.
- Business applications receive CPU time more quickly.
- Overall system responsiveness improves.

---

# Best Practices

- Run non-critical batch jobs with higher nice values (lower priority).
- Keep critical services at the default priority unless tuning is necessary.
- Increase process priority only when justified.
- Monitor CPU utilization before changing priorities.
- Test priority changes in non-production environments.

---

# Common Mistakes

❌ Assigning the highest priority to every application.

✅ This defeats the purpose of process prioritization.

---

❌ Using negative nice values without understanding their impact.

✅ High-priority processes can reduce CPU availability for other workloads.

---

❌ Assuming `nice` changes process memory usage.

✅ It only influences CPU scheduling priority.

---

# Interview Questions
## Beginner

1. What is a nice value?
2. What is the default nice value?
3. Which command starts a process with a custom priority?
4. Which command changes the priority of a running process?

---

## Intermediate

1. What is the valid range of nice values?
2. Why do lower nice values result in higher priority?
3. When would you use `renice` instead of `nice`?
4. How do you display a process's nice value?

---

## Architect Level

1. How would you prioritize workloads on a busy production server?
2. Which workloads should typically run with lower priority?
3. Why is process priority tuning important for enterprise Linux systems?

---

# Summary

In this lesson, you learned:

- Process priorities
- Nice values
- The `nice` command
- The `renice` command
- CPU scheduling
- Priority management
- Production best practices

Linux process priorities help administrators balance competing workloads by controlling CPU scheduling. Proper use of `nice` and `renice` improves system responsiveness and ensures critical applications receive appropriate CPU resources.

---

## Key Takeaways

- Nice values range from **-20** (highest priority) to **19** (lowest priority).
- The default nice value is **0**.
- Use `nice` to start a process with a custom priority.
- Use `renice` to modify the priority of a running process.
- Lower-priority background jobs should typically have higher nice values.
- Use process priorities carefully to maintain system performance.

---

## What's Next?

**[The kill Command — Terminating Processes in Linux](kill.md)**

You'll explore:

- Terminating processes
- Finding Process IDs (PIDs)
- Graceful vs forceful termination
- Killing multiple processes
- Common termination signals
- Production troubleshooting

Understanding process termination is an essential skill for managing Linux systems safely and effectively.
