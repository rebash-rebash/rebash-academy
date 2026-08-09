---
title: "Linux Services — Managing Background Applications"
description: "Manage Linux services with systemctl — start, stop, restart, enable at boot, check failed units, and troubleshoot with journalctl."
difficulty: intermediate
estimated_time: "60 min"
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
  - services
  - systemd
  - systemctl
  - daemons
  - rebash-linux-mastery
comments: false
status: ready
---

# Linux Services — Managing Background Applications

> A **service** is a long-running background process that performs a specific function for the operating system or applications. Services start automatically during system boot or on demand and continue running without user interaction. Web servers, databases, SSH servers, Docker, Kubernetes, and monitoring agents all run as Linux services. Understanding services is essential for Linux administrators, DevOps engineers, Cloud Architects, and Site Reliability Engineers (SREs).

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 6: Process Management → Lesson 10</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 60 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Process Management</div>

<div markdown>**Lesson:** 10 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Linux services
- Differentiate services and regular processes
- Manage services using `systemctl`
- Understand service lifecycle
- Monitor service health
- Troubleshoot failed services
- Apply service management in production

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management and Permissions
- Module 5 – Users and Groups
- Module 6 Lessons 1–9

---

# Why Learn Services?

Imagine a production server running:

- NGINX
- Apache
- MySQL
- PostgreSQL
- Docker
- Kubernetes
- SSH

These applications must:

- Start automatically after boot
- Run continuously
- Restart if they fail
- Be monitored

Linux manages these long-running applications as **services**.

---

# What is a Service?

A service is a background process (also called a **daemon**) that performs a specific task without requiring direct user interaction.

Examples include:

- Web servers
- Database servers
- DNS servers
- SSH servers
- Monitoring agents
- Container runtimes

---

# Service vs Process

| Process | Service |
|----------|----------|
| Any running program | Long-running background program |
| May be temporary | Usually runs continuously |
| Often started manually | Usually managed by `systemd` |
| Can exit after completing a task | Typically waits for requests |

---

# Common Linux Services

| Service | Purpose |
|----------|---------|
| `sshd` | Secure remote access |
| `nginx` | Web server |
| `apache2` / `httpd` | Web server |
| `docker` | Container runtime |
| `kubelet` | Kubernetes node agent |
| `postgresql` | PostgreSQL database |
| `mysql` | MySQL database |

---

# Service Lifecycle

```text
Installed
     │
     ▼
Started
     │
     ▼
Running
     │
     ▼
Stopped
     │
     ▼
Restarted
     │
     ▼
Disabled or Removed
```

---

# Check Service Status

```bash
systemctl status sshd
```

Example:

```text
● sshd.service

Active: active (running)
```

---

# Start a Service

```bash
sudo systemctl start nginx
```

---

# Stop a Service

```bash
sudo systemctl stop nginx
```

---

# Restart a Service

```bash
sudo systemctl restart nginx
```

---

# Reload a Service

If supported:

```bash
sudo systemctl reload nginx
```

This reloads configuration without fully restarting the service.

---

# Enable at Boot

```bash
sudo systemctl enable nginx
```

---

# Disable at Boot

```bash
sudo systemctl disable nginx
```

---

# Verify Service State

Check if running.

```bash
systemctl is-active nginx
```

Check if enabled.

```bash
systemctl is-enabled nginx
```

---

# List Running Services

```bash
systemctl list-units --type=service
```

List all installed services.

```bash
systemctl list-unit-files --type=service
```

---

# View Service Logs

Display logs.

```bash
journalctl -u nginx
```

Show recent entries.

```bash
journalctl -u nginx -n 20
```

Follow logs live.

```bash
journalctl -u nginx -f
```

---

# Check Failed Services

```bash
systemctl --failed
```

Useful for identifying services that failed during boot or runtime.

---

# Common Commands

Check status.

```bash
systemctl status nginx
```

Start.

```bash
sudo systemctl start nginx
```

Stop.

```bash
sudo systemctl stop nginx
```

Restart.

```bash
sudo systemctl restart nginx
```

Reload.

```bash
sudo systemctl reload nginx
```

View logs.

```bash
journalctl -u nginx
```

---

# Real Production Examples

Restart Docker.

```bash
sudo systemctl restart docker
```

Check Kubernetes node.

```bash
systemctl status kubelet
```

View PostgreSQL logs.

```bash
journalctl -u postgresql
```

Check SSH service.

```bash
systemctl status sshd
```

---

# Production Perspective

Linux services power almost every enterprise workload, including:

- Web applications
- Databases
- Kubernetes clusters
- Docker hosts
- Monitoring systems
- CI/CD platforms
- Messaging systems

Effective service management is a core responsibility of Linux administrators and DevOps engineers.

---

# Hands-on Lab

## Task 1

List running services.

```bash
systemctl list-units --type=service
```

---

## Task 2

Check the SSH service.

```bash
systemctl status sshd
```

!!! note "Note"

    On Ubuntu, use `ssh` instead of `sshd` if applicable.

---

## Task 3

Check if the service is active.

```bash
systemctl is-active sshd
```

---

## Task 4

Check if it starts automatically.

```bash
systemctl is-enabled sshd
```

---

## Task 5

View recent logs.

```bash
journalctl -u sshd -n 20
```

---

## Task 6

List failed services.

```bash
systemctl --failed
```

---

## Task 7

View all installed service unit files.

```bash
systemctl list-unit-files --type=service
```

---

## Task 8

Identify the process associated with a service.

```bash
systemctl status sshd
```

Observe the **Main PID** field.

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `systemctl status` | Service status | Troubleshooting |
| `systemctl start` | Start service | Maintenance |
| `systemctl stop` | Stop service | Administration |
| `systemctl restart` | Restart service | Deployments |
| `systemctl reload` | Reload configuration | Configuration updates |
| `systemctl --failed` | View failed services | Incident response |
| `journalctl -u` | View service logs | Root cause analysis |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    Users report they cannot connect to a web application.

Investigation:

```bash
systemctl status nginx
```

Output:

```text
Active: failed
```

Review logs.

```bash
journalctl -u nginx -n 50
```

The logs reveal a syntax error in the NGINX configuration.

After correcting the configuration:

```bash
sudo systemctl restart nginx
```

Verify:

```bash
systemctl status nginx
```

The service is now running successfully and users regain access.

---

# Best Practices

- Manage services using `systemctl`.
- Check service status before restarting.
- Review logs before making configuration changes.
- Enable only required services at boot.
- Monitor failed services regularly.
- Test configuration changes before restarting production services.

---

# Common Mistakes

❌ Restarting services without checking logs.

✅ Avoid this mistake: restarting services without checking logs.

---

❌ Disabling critical services accidentally.

✅ Avoid disabling critical services accidentally; fix the configuration instead.

---

❌ Running long-lived applications manually instead of as services.

✅ Prefer as services rather than running long-lived applications manually.

---

❌ Ignoring failed services after system boot.

✅ Always review failed services after system boot.

---

# Interview Questions
## Beginner

1. What is a Linux service?
2. What is the difference between a service and a process?
3. Which command checks service status?
4. How do you restart a service?

---

## Intermediate

1. What is the difference between restarting and reloading a service?
2. How do you list failed services?
3. How do you view logs for a service?
4. Why are services managed by `systemd`?

---

## Architect Level

1. How would you troubleshoot a production service that repeatedly fails to start?
2. How would you ensure critical services start automatically after a reboot?
3. What monitoring strategy would you implement for essential production services?

---

# Summary

In this lesson, you learned:

- Linux services
- Service lifecycle
- Managing services with `systemctl`
- Monitoring service health
- Viewing service logs
- Troubleshooting failed services
- Production best practices

Services are the backbone of Linux systems, providing continuous functionality for applications, networking, databases, and infrastructure. Mastering service management enables you to deploy, maintain, and troubleshoot production workloads with confidence.

---

## Key Takeaways

- Services are long-running background applications.
- Most modern Linux services are managed by `systemd`.
- Use `systemctl` to start, stop, restart, and monitor services.
- Use `journalctl` to investigate service issues.
- Monitor failed services regularly.
- Always review logs before restarting production services.

---

# Module 6 Completed! 🎉

Congratulations! You have successfully completed **Module 6 – Process Management**.

You now understand:

- Linux processes
- Foreground and background jobs
- Process monitoring (`ps`, `top`, `htop`)
- Process priorities (`nice`, `renice`)
- Process termination (`kill`)
- Linux signals
- `systemd`
- Service management

These are essential skills used daily by Linux administrators, DevOps engineers, Cloud Architects, Platform Engineers, and SREs to manage production Linux systems.

---

## What's Next?

**[Module 6 Summary — Process Management](module-6-process-management-summary.md)**

Review the module, complete the mini project and assessment, then continue to **Module 7 – Package Management**.
