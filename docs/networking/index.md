---
title: Overview
description: "Networking for Cloud & DevOps Engineers — 17 modules from fundamentals through Linux, Kubernetes, multi-cloud, production operations, and troubleshooting."
difficulty: beginner
estimated_time: "8–10 weeks"
author: Shaik Basha
last_updated: "2026-07-31"
category: networking
tags:
  - networking
  - devops
  - cloud
  - course
comments: false
---

# Networking for Cloud & DevOps Engineers

**Duration:** 8–10 weeks · **Difficulty:** Beginner → Advanced
{ .ra-facts }

A practical networking course focused on Linux, Cloud, Kubernetes, and DevOps — design, troubleshoot, and operate production networks.

!!! tip "Course status"
    Curriculum follows the REBASH Networking technology prompt (**17 modules**). Diagrams use **Excalidraw** assets under `docs/assets/excalidraw/` (not D2). Core tutorials for Modules **1–17** are on that standard; regenerate diagrams with `python3 scripts/generate-excalidraw-svg.py`.

## 1. Course overview

### Purpose

Teach networking from an operations, troubleshooting, and cloud engineering perspective so learners can design and operate production networks.

### Target roles

Cloud Engineer · DevOps Engineer · Platform Engineer · SRE · DevSecOps · Kubernetes Administrator · Infrastructure Engineer

### Prerequisites

- Basic Linux knowledge
- Command line familiarity

### Capstone outcome

Design production networks · Troubleshoot connectivity · Configure Linux networking · Understand Kubernetes networking · Build cloud network architectures · Diagnose DNS/routing · Operate secure production networking

## 2. Modules and tutorials

| Module | Focus | Start here |
|-------:|-------|------------|
| 1 | Networking Fundamentals | [What is Networking?](introduction-to-networking.md) |
| 2 | OSI Model | [OSI Model](osi-model.md) |
| 3 | TCP/IP Model | [TCP/IP Model](tcp-ip-model.md) |
| 4 | IP Addressing | [IP Addressing](ip-addressing.md) |
| 5 | Subnetting | [Subnetting and VLSM](subnetting-and-vlsm.md) |
| 6 | Routing | [Routing Fundamentals](routing-fundamentals.md) |
| 7 | Switching | [Ethernet, Switching, and VLANs](ethernet-switching-and-vlans.md) · [ICMP/ARP/DHCP](icmp-arp-dhcp-and-network-services.md) |
| 8 | TCP & UDP | [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md) |
| 9 | DNS | [DNS Fundamentals](dns-fundamentals.md) · [DNS Records](dns-records-and-troubleshooting.md) |
| 10 | HTTP & HTTPS | [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md) |
| 11 | NAT & Firewalls | [NAT](nat-and-port-forwarding.md) · [Firewalls](firewalls-and-access-control.md) |
| 12 | Linux Networking | [Linux Networking Toolkit](linux-networking-toolkit.md) |
| 13 | Load Balancing | [Load Balancing](load-balancing-fundamentals.md) · [Reverse Proxy / Ingress](reverse-proxy-and-ingress-basics.md) |
| 14 | Kubernetes Networking | [Kubernetes Networking Fundamentals](kubernetes-networking-fundamentals.md) |
| 15 | Cloud Networking | [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md) |
| 16 | Production Networking | Segmentation · VPN · Hardening · Automation · DNS/LB/ACL ops |
| 17 | Troubleshooting | Methodology · Packet analysis · Incident response |

## 3. Practice

- Labs: [DNS / firewall triage](../labs/networking-dns-firewall-triage.md) · [Edge failover](../labs/networking-edge-failover.md)
- [Projects](projects/index.md) · [Quizzes](quizzes/index.md) · [Cheat sheets](cheatsheets/index.md) · [Interview](interview/index.md)

## Start here

1. [What is Networking?](introduction-to-networking.md)
2. [OSI Model](osi-model.md)
3. [TCP/IP Model](tcp-ip-model.md)
4. [IP Addressing](ip-addressing.md)
5. [Subnetting and VLSM](subnetting-and-vlsm.md)

## Diagrams

All course diagrams for rewritten modules live in [`docs/assets/excalidraw/`](../assets/excalidraw/) as `.svg` plus editable `.excalidraw` sources. Regenerate with:

```bash
python3 scripts/generate-excalidraw-svg.py
```

## Related

- [Linux](../linux/index.md) · [Docker](../docker/index.md) · [Kubernetes](../kubernetes/index.md) · [AWS](../aws/index.md)
- [DevOps Engineer path](../career-paths/devops-engineer/index.md)
