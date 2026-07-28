---
title: Overview
description: Networking learning track — 20 tutorials from TCP/IP fundamentals to cloud VPCs and troubleshooting.
difficulty: beginner
estimated_time: "Varies"
author: Shaik Basha
category: networking
tags:
  - networking
comments: false
---

# Networking

Understand how data moves across the internet and inside your infrastructure — from IP addressing and DNS to load balancers, firewalls, and cloud VPCs.

## Overview

The REBASH Academy **Networking** track is a structured, 20-tutorial curriculum for DevOps engineers, SREs, and cloud administrators. Each tutorial follows our [documentation standards](../about.md#documentation-standards) with theory, step-by-step labs, commands, best practices, and interview questions.

!!! tip "Learning Path"
    Complete the [Linux](../linux/index.md) track first, then continue here as step 2 in the [DevOps Engineer learning path](../learning-paths/index.md).

## Curriculum Plan

```d2
direction: down

M1: "Module 1: Foundations"
    M2: "Module 2: Data Link & Routing"
    M1 -> M2
    M3: "Module 3: Transport & DNS"
    M2 -> M3
    M4: "Module 4: Application Layer"
    M3 -> M4
    M5: "Module 5: Troubleshooting"
    M4 -> M5
    M6: "Module 6: Cloud & Advanced"
    M5 -> M6
```

### Module 1 – Foundations

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 1 | [Introduction to Networking](introduction-to-networking.md) | Beginner | 30 min |
| 2 | [OSI and TCP/IP Models](osi-and-tcp-ip-models.md) | Beginner | 35 min |
| 3 | [IP Addressing and Subnetting](ip-addressing-and-subnetting.md) | Beginner | 45 min |

### Module 2 – Data Link & Routing

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 4 | [Ethernet, Switching, and VLANs](ethernet-switching-and-vlans.md) | Beginner | 40 min |
| 5 | [Routing Fundamentals](routing-fundamentals.md) | Intermediate | 45 min |
| 6 | [ICMP, ARP, DHCP, and Network Services](icmp-arp-dhcp-and-network-services.md) | Intermediate | 40 min |

### Module 3 – Transport & DNS

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 7 | [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md) | Intermediate | 50 min |
| 8 | [DNS Fundamentals](dns-fundamentals.md) | Beginner | 40 min |
| 9 | [DNS Records and Troubleshooting](dns-records-and-troubleshooting.md) | Intermediate | 45 min |

### Module 4 – Application Layer

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 10 | [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md) | Beginner | 40 min |
| 11 | [Firewalls and Access Control](firewalls-and-access-control.md) | Intermediate | 45 min |
| 12 | [Load Balancing Fundamentals](load-balancing-fundamentals.md) | Intermediate | 45 min |
| 13 | [Reverse Proxy and Ingress Basics](reverse-proxy-and-ingress-basics.md) | Intermediate | 40 min |

### Module 5 – Troubleshooting

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 14 | [Network Troubleshooting Methodology](network-troubleshooting-methodology.md) | Intermediate | 50 min |
| 15 | [Packet Analysis with tcpdump and Wireshark](packet-analysis-tcpdump-wireshark.md) | Intermediate | 55 min |

### Module 6 – Cloud & Advanced

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 16 | [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md) | Intermediate | 50 min |
| 17 | [NAT and Port Forwarding](nat-and-port-forwarding.md) | Intermediate | 40 min |
| 18 | [VPN and Tunneling Basics](vpn-and-tunneling-basics.md) | Intermediate | 45 min |
| 19 | [Network Security Hardening](network-security-hardening.md) | Advanced | 50 min |
| 20 | [Network Automation and Monitoring](network-automation-and-monitoring.md) | Advanced | 50 min |

**Total estimated time:** ~14 hours of hands-on learning

## Learning Objectives

After completing this track, you will be able to:

- [ ] Explain how data flows through the TCP/IP stack from application to wire
- [ ] Design and calculate IP subnets for cloud and on-premises networks
- [ ] Configure and troubleshoot DNS, routing, and firewall rules
- [ ] Understand load balancers, reverse proxies, and ingress patterns
- [ ] Diagnose connectivity issues using layered troubleshooting and packet capture
- [ ] Design VPC architectures with NAT, security groups, and VPN connectivity

## Who Is This For?

| Audience | Benefit |
|----------|---------|
| **DevOps / SRE** | Debug production outages involving DNS, TLS, or routing |
| **Cloud engineers** | Design VPCs, subnets, and security groups confidently |
| **Developers** | Understand why your app can't reach the database |
| **Students** | Build job-ready networking skills for certification and interviews |

## Related Sections

- [Linux](../linux/index.md) — OS-level networking with `ip`, `ss`, and `dig`
- [Docker](../docker/index.md) — container networking overlays and bridge networks
- [AWS](../aws/index.md) — VPC, ALB, and Route 53 in production
- [Interview Prep](../interview/index.md) — networking interview questions
