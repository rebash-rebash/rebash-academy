---
title: "Capstone Project 1 — Build a Home Lab Network"
description: "Build a production-inspired home lab network — Linux, Docker, DNS, DHCP, firewall, SSH, monitoring, and documented enterprise-style topology."
difficulty: advanced
estimated_time: "6–10 hours"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 15 · Capstone Projects"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - capstone
  - home-lab
  - docker
  - production
  - rebash-networking-mastery
comments: false
status: ready
---

# Capstone Project 1 — Build a Home Lab Network

> In this capstone project, you'll build a **production-inspired home lab network** that simulates a small enterprise environment. You'll create network segments, configure routers, switches, DNS, DHCP, firewalls, VPN access, monitoring, and Linux servers. This project combines everything you've learned throughout the Networking Mastery course and provides a practical environment for experimenting with networking, Linux, cloud technologies, Kubernetes, and DevOps.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 15: Capstone Projects → Project 1</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Advanced</div>

<div markdown>**Estimated Completion Time:** 6–10 Hours</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Capstone Projects</div>

<div markdown>**Project:** 1 of 8</div>

</div>

</div>

---


# Project Objectives

By completing this project, you'll be able to:

- Design a production-style home lab
- Build a multi-device network
- Configure Linux networking
- Implement DHCP and DNS
- Secure network access
- Monitor infrastructure
- Prepare for future networking projects

---

# Skills Covered

This project integrates concepts from:

- TCP/IP
- Routing
- Switching
- DNS
- DHCP
- VLANs
- Firewalls
- VPN
- Linux Networking
- Cloud Networking
- Monitoring
- Troubleshooting

---

# Project Scenario

You have been hired as a Network Engineer.

Your company wants a small enterprise network for:

- Developers
- Servers
- Testing
- Monitoring
- Remote Access

Your task is to design and deploy the environment.

---

# Target Architecture

```text
                 Internet
                     │
               Home Router
                     │
              Linux Firewall
                     │
             Managed Switch
      ┌──────────┬──────────┬──────────┐
      │          │          │
 Linux Server  Workstation  Wi-Fi AP
      │
 Docker
      │
 Kubernetes
```

Later projects will extend this architecture.

---

# Recommended Hardware

Minimum:

- One Laptop/Desktop
- 16 GB RAM
- 100 GB Free Disk

Recommended:

- 32 GB RAM
- SSD Storage
- Gigabit Network
- Second PC (Optional)

---

# Virtualization Options

Choose one:

- VMware Workstation
- VirtualBox
- Proxmox VE
- KVM/QEMU
- Hyper-V

Virtual machines make the lab flexible and repeatable.

---

# Suggested Virtual Machines

| VM | Purpose |
|----|----------|
| Ubuntu Server | Linux Administration |
| Rocky Linux | Enterprise Linux |
| Debian | Networking |
| Windows Server (Optional) | Active Directory |
| Kali Linux (Optional) | Security Testing |

---

# IP Address Plan

Example:

| Network | CIDR |
|----------|------|
| LAN | 192.168.10.0/24 |
| Servers | 192.168.20.0/24 |
| Management | 192.168.30.0/24 |
| VPN | 10.100.0.0/24 |

---

# Network Diagram

```text
Internet
    │
Router
    │
Switch
 ┌──┴─────────────┐
 │                │
Server        Workstation
 │
Monitoring
```

---

# Step 1 — Install Linux Server

Install:

```text
Ubuntu Server LTS
```

Recommended resources:

- 2 vCPU
- 4 GB RAM
- 40 GB Disk

---

# Step 2 — Configure Networking

Check interfaces:

```bash
ip addr
```

Verify routes:

```bash
ip route
```

Test Internet:

```bash
ping google.com
```

---

# Step 3 — Configure Static IP

Example:

```text
192.168.20.10
```

Verify:

```bash
ip addr
```

---

# Step 4 — Configure Hostname

Example:

```bash
sudo hostnamectl set-hostname server01
```

Verify:

```bash
hostname
```

---

# Step 5 — Update System

```bash
sudo apt update

sudo apt upgrade -y
```

---

# Step 6 — Install Essential Tools

```bash
sudo apt install \
curl \
wget \
git \
vim \
net-tools \
tcpdump \
traceroute \
dnsutils \
htop \
iftop \
nmap
```

---

# Step 7 — Verify Connectivity

```bash
ping 8.8.8.8
```

```bash
ping google.com
```

Verify DNS resolution.

---

# Step 8 — Install Docker

```bash
curl -fsSL https://get.docker.com | sh
```

Verify:

```bash
docker version
```

---

# Step 9 — Deploy NGINX

```bash
docker run -d \
-p 80:80 \
nginx
```

Test:

```bash
curl localhost
```

---

# Step 10 — Install Monitoring Tools

Install:

- Prometheus
- Grafana
- Node Exporter

Verify metrics collection.

---

# Step 11 — Enable SSH

```bash
sudo systemctl enable ssh

sudo systemctl start ssh
```

Verify:

```bash
ss -tuln
```

---

# Step 12 — Configure Firewall

Ubuntu:

```bash
sudo ufw allow ssh

sudo ufw allow 80

sudo ufw enable
```

Verify:

```bash
sudo ufw status
```

---

# Step 13 — Create Network Documentation

Document:

- IP Addresses
- Hostnames
- Installed Services
- Network Diagram
- Credentials (stored securely)
- Firewall Rules

Documentation is part of every production environment.

---

# Step 14 — Validate the Environment

Confirm:

- Internet Access
- DNS Resolution
- SSH Access
- Docker Running
- Web Server Available
- Firewall Enabled

---

# Final Architecture

```text
Internet
    │
Router
    │
Firewall
    │
Switch
    │
Ubuntu Server
    │
Docker
    │
NGINX
```

---

# Validation Checklist

| Item | Status |
|------|--------|
| Linux Installed | ☐ |
| Static IP Configured | ☐ |
| Internet Working | ☐ |
| DNS Working | ☐ |
| Docker Installed | ☐ |
| NGINX Running | ☐ |
| SSH Enabled | ☐ |
| Firewall Enabled | ☐ |
| Monitoring Installed | ☐ |
| Documentation Completed | ☐ |

---

# Common Problems

| Problem | Solution |
|----------|----------|
| No Internet | Check Gateway |
| DNS Failure | Verify `/etc/resolv.conf` |
| SSH Not Working | Check Firewall |
| Docker Not Starting | Restart Docker Service |
| Cannot Access NGINX | Verify Port 80 |

---

# Troubleshooting Commands

View interfaces:

```bash
ip addr
```

View routes:

```bash
ip route
```

DNS lookup:

```bash
dig google.com
```

Check listening ports:

```bash
ss -tuln
```

Capture traffic:

```bash
sudo tcpdump
```

---

# Bonus Challenges

Try extending the lab by:

- Adding a second Linux server
- Creating multiple Docker containers
- Installing Kubernetes (k3s or Minikube)
- Configuring a reverse proxy
- Installing Grafana dashboards
- Adding remote VPN access
- Creating automated backups

---

# Learning Outcomes

After completing this project, you'll be able to:

- Build a professional home networking lab
- Configure Linux networking
- Deploy Docker workloads
- Secure servers
- Monitor infrastructure
- Troubleshoot networking issues
- Prepare for enterprise networking projects

---

# Project Deliverables

By the end of this project, you should have:

- A working Linux server
- A documented IP addressing plan
- A secure SSH configuration
- Docker installed and operational
- An NGINX web server
- Basic monitoring tools
- Firewall protection
- Network documentation
- A validated home lab environment

---

# Self-Assessment

Before moving to the next project, confirm:

- [ ] Can you configure a Linux server with a static IP?
- [ ] Can you verify routing and DNS?
- [ ] Can you deploy a Docker application?
- [ ] Can you configure SSH securely?
- [ ] Can you enable a firewall?
- [ ] Can you troubleshoot connectivity issues?
- [ ] Can you document your network architecture?

---

# Summary

In this capstone project, you built a production-inspired home lab that serves as the foundation for all remaining projects. You installed Linux, configured networking, deployed services, enabled security, and created a documented infrastructure that mirrors real-world environments.

This home lab provides a safe place to experiment, troubleshoot, and practice enterprise networking skills without impacting production systems.

---

## Key Takeaways

- Build your lab using **virtualization** for flexibility and repeatability.
- Document every IP address, hostname, and network component.
- Secure the environment with **SSH**, **firewalls**, and strong access controls.
- Validate connectivity, DNS, routing, and application availability before continuing.
- Treat your home lab like a production environment by monitoring, documenting, and maintaining it.
- This lab will serve as the foundation for the remaining capstone projects.

---

## What's Next?

**[Configure VLANs](configure-vlans.md)**

In the next project, you'll learn how to **Configure VLANs**.

You'll build a segmented enterprise network by creating multiple VLANs, configuring trunk and access ports, enabling inter-VLAN routing, and implementing network isolation and security best practices.
