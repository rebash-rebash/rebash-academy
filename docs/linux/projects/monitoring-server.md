---
title: "Capstone Project 4 — Create a Monitoring Server"
description: "Build a production monitoring server with Prometheus, Grafana, and Node Exporter — dashboards, alerts, firewall, backups, and hardening."
difficulty: advanced
estimated_time: "6–8 hours"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 15 · Capstone Projects"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - security-engineer
tags:
  - linux
  - capstone
  - prometheus
  - grafana
  - monitoring
  - production
  - rebash-linux-mastery
comments: false
status: ready
---

# Capstone Project 4 — Create a Monitoring Server

> Monitoring is one of the most critical components of production infrastructure. A **Monitoring Server** continuously collects metrics, visualizes system health, generates alerts, and helps administrators detect issues before they become outages. Modern organizations rely on monitoring platforms such as **Prometheus** and **Grafana** to observe Linux servers, applications, containers, Kubernetes clusters, and cloud infrastructure. In this capstone project, you'll build a production-ready monitoring server capable of collecting metrics from multiple Linux systems and displaying them through interactive dashboards.

---

# Project Overview

## Objective

Build a centralized monitoring server using Prometheus, Grafana, and Node Exporter to monitor multiple Linux servers.

---

## Skills Covered

- Linux Administration
- Prometheus
- Grafana
- Node Exporter
- System Monitoring
- Dashboard Creation
- Alerting
- Firewall Configuration
- Backup
- Logging
- Production Hardening

---

# Estimated Time

**6–8 Hours**

---

# Difficulty

Beginner → Advanced

---

# Project Architecture

```text
                +----------------------+
                |   Monitoring Server  |
                |                      |
                |  Prometheus          |
                |  Grafana             |
                +----------+-----------+
                           │
         Metrics Collection │
                           │
      ┌──────────────┬──────────────┬──────────────┐
      │              │              │
+-------------+ +-------------+ +-------------+
| Linux-01    | | Linux-02    | | Linux-03    |
| NodeExporter| | NodeExporter| | NodeExporter|
+-------------+ +-------------+ +-------------+
```

---

# Learning Outcomes

By completing this project, you'll be able to:

- Deploy Prometheus
- Install Grafana
- Monitor Linux servers
- Configure Node Exporter
- Build dashboards
- Configure alerts
- Monitor infrastructure health
- Validate production monitoring

---

# Project Requirements

## Hardware

Minimum

- 2 vCPU
- 4 GB RAM
- 40 GB Disk

Recommended

- 4 vCPU
- 8 GB RAM
- 80 GB SSD

---

## Operating System

Choose one:

- Ubuntu Server 24.04 LTS
- Ubuntu Server 22.04 LTS
- Rocky Linux 9
- AlmaLinux 9

This project uses **Ubuntu Server**.

---

# Software Stack

- Ubuntu Server
- Prometheus
- Grafana
- Node Exporter
- OpenSSH
- UFW
- rsync

---

# Project Tasks

| Phase | Task |
|---------|------|
| 1 | Install Linux |
| 2 | Install Prometheus |
| 3 | Install Node Exporter |
| 4 | Configure Prometheus |
| 5 | Install Grafana |
| 6 | Build Dashboards |
| 7 | Configure Alerts |
| 8 | Configure Firewall |
| 9 | Configure Backup |
| 10 | Validate Monitoring |
| 11 | Harden Server |
| 12 | Production Review |

---

# Phase 1 — Install Linux

Update packages.

```bash
sudo apt update

sudo apt upgrade -y
```

Verify.

```bash
hostnamectl
```

---

# Phase 2 — Install Prometheus

Create Prometheus user.

```bash
sudo useradd --no-create-home --shell /bin/false prometheus
```

Download Prometheus.

```bash
wget https://github.com/prometheus/prometheus/releases/latest/download/prometheus-linux-amd64.tar.gz
```

Extract.

```bash
tar -xvf prometheus-linux-amd64.tar.gz
```

Verify.

```bash
prometheus --version
```

---

# Phase 3 — Install Node Exporter

Download Node Exporter.

```bash
wget https://github.com/prometheus/node_exporter/releases/latest/download/node_exporter-linux-amd64.tar.gz
```

Extract.

```bash
tar -xvf node_exporter-linux-amd64.tar.gz
```

Start Node Exporter.

```bash
./node_exporter
```

Verify metrics.

```bash
curl http://localhost:9100/metrics
```

---

# Phase 4 — Configure Prometheus

Edit configuration.

```bash
sudo nano /etc/prometheus/prometheus.yml
```

Example:

```yaml
scrape_configs:
  - job_name: linux
    static_configs:
      - targets:
          - localhost:9100
```

Restart Prometheus.

```bash
sudo systemctl restart prometheus
```

Verify targets.

```text
http://server-ip:9090/targets
```

---

# Phase 5 — Install Grafana

Install dependencies.

```bash
sudo apt install grafana
```

Enable service.

```bash
sudo systemctl enable grafana-server

sudo systemctl start grafana-server
```

Verify.

```bash
systemctl status grafana-server
```

Open browser.

```text
http://server-ip:3000
```

Default login:

```text
admin

admin
```

---

# Phase 6 — Build Dashboards

Create dashboards for:

- CPU Usage
- Memory Usage
- Disk Usage
- Filesystem
- Load Average
- Network Traffic
- Running Processes
- System Uptime

Import the **Node Exporter Full** dashboard or create your own custom dashboard.

---

# Phase 7 — Configure Alerts

Create alerts for:

- CPU > 80%
- Memory > 80%
- Disk > 85%
- Server Down
- Filesystem Full
- High Load Average

Verify alerts trigger correctly during testing.

---

# Phase 8 — Configure Firewall

Install UFW.

```bash
sudo apt install ufw
```

Allow required ports.

```bash
sudo ufw allow 22/tcp

sudo ufw allow 3000/tcp

sudo ufw allow 9090/tcp
```

Enable firewall.

```bash
sudo ufw enable
```

Verify.

```bash
sudo ufw status
```

---

# Phase 9 — Configure Backup

Backup Prometheus configuration.

```bash
tar -czf prometheus-config.tar.gz /etc/prometheus
```

Backup Grafana configuration.

```bash
tar -czf grafana-config.tar.gz /etc/grafana
```

Synchronize backups.

```bash
rsync -av /etc/prometheus /backup
```

---

# Phase 10 — Validate Monitoring

Verify Prometheus.

```text
http://server-ip:9090
```

Verify Grafana.

```text
http://server-ip:3000
```

Verify metrics.

```bash
curl localhost:9100/metrics
```

Confirm dashboards display live data.

---

# Phase 11 — Harden Server

Install Fail2Ban.

```bash
sudo apt install fail2ban
```

Enable.

```bash
sudo systemctl enable fail2ban

sudo systemctl start fail2ban
```

Apply updates.

```bash
sudo apt update

sudo apt upgrade
```

Review listening ports.

```bash
ss -tuln
```

---

# Phase 12 — Production Review

Verify:

Prometheus.

```bash
systemctl status prometheus
```

Grafana.

```bash
systemctl status grafana-server
```

Firewall.

```bash
ufw status
```

Disk.

```bash
df -h
```

Logs.

```bash
journalctl
```

---

# Final Project Checklist

| Item | Status |
|--------|--------|
| Linux Installed | ☐ |
| Prometheus Installed | ☐ |
| Node Exporter Installed | ☐ |
| Prometheus Configured | ☐ |
| Grafana Installed | ☐ |
| Dashboards Created | ☐ |
| Alerts Configured | ☐ |
| Firewall Enabled | ☐ |
| Backup Configured | ☐ |
| Monitoring Verified | ☐ |
| Server Hardened | ☐ |
| Production Validation Completed | ☐ |

---

# Production Perspective

Monitoring servers are commonly used to monitor:

- Linux Servers
- Kubernetes Clusters
- Docker Hosts
- Databases
- CI/CD Servers
- Cloud Infrastructure
- Virtual Machines
- Enterprise Applications

Centralized monitoring enables operations teams to identify and resolve issues before they affect users.

---

# Hands-on Lab

## Task 1

Install Prometheus.

---

## Task 2

Install Node Exporter.

---

## Task 3

Connect Prometheus to Node Exporter.

---

## Task 4

Install Grafana.

---

## Task 5

Create a CPU dashboard.

---

## Task 6

Create alerts for CPU, memory, and disk usage.

---

## Task 7

Add two additional Linux servers to Prometheus monitoring.

---

## Task 8

Build a production dashboard displaying:

- CPU
- Memory
- Disk
- Network
- Uptime
- Load Average
- Active Alerts

---

# Production Best Practices

- Monitor every production server.
- Configure meaningful alert thresholds.
- Secure monitoring endpoints.
- Back up monitoring configurations.
- Monitor the monitoring server itself.
- Review alert noise regularly.
- Keep dashboards simple and actionable.
- Test alert notifications periodically.
- Protect Grafana with strong authentication.
- Maintain historical metrics for trend analysis.

---

# Challenge Tasks

Complete these additional tasks to extend the project:

- Configure Alertmanager for email notifications.
- Integrate Slack or Microsoft Teams alerts.
- Enable HTTPS for Grafana.
- Monitor Docker containers.
- Monitor Kubernetes clusters.
- Monitor MySQL or PostgreSQL.
- Configure long-term metric storage.
- Build custom Grafana dashboards.
- Add Blackbox Exporter for website monitoring.
- Configure high availability for Prometheus.

---

# Skills Demonstrated

After completing this project, you will have demonstrated proficiency in:

- Linux Monitoring
- Prometheus Administration
- Grafana Administration
- Metrics Collection
- Dashboard Design
- Alert Configuration
- Firewall Management
- Backup Strategy
- Production Hardening
- Enterprise Monitoring

---

# Congratulations!

You have successfully built a **production-ready Monitoring Server**.

Your monitoring platform now collects metrics from multiple Linux systems, visualizes infrastructure health, and alerts administrators about potential issues before they become outages.

This architecture closely reflects monitoring solutions used by DevOps teams, Platform Engineers, and Site Reliability Engineers in enterprise production environments.

---

## What's Next?

**[Capstone Project 5 — Automate User Provisioning with Bash](automate-user-provisioning-bash.md)**

You'll learn how to:


- Create Bash automation scripts
- Provision Linux users automatically
- Assign groups and permissions
- Generate secure passwords
- Configure home directories
- Produce audit logs
- Automate administrative tasks

By the end of the project, you'll build a reusable Bash automation solution that provisions Linux users consistently, securely, and efficiently in production environments.
