---
title: "IP Addressing"
description: "IPv4 and IPv6 addressing for Cloud and DevOps — binary basics, CIDR, public vs private, loopback, reserved ranges, and broadcast."
difficulty: beginner
estimated_time: "50–65 min"
technology: networking
category: networking
module: "Module 4 · IP Addressing"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - linux-administrator
  - site-reliability-engineer
skills:
  - ipv4
  - ipv6
  - cidr
prerequisites:
  - networking/tcp-ip-model
next:
  - networking/subnetting-and-vlsm
related:
  - networking/cloud-networking-vpc-and-subnets
interview: interview/networking
certifications:
  - CompTIA Network+
  - AWS SAA
tags:
  - networking
  - ipv4
  - ipv6
  - cidr
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# IP Addressing

## Overview

Read and classify IPv4/IPv6 addresses, explain CIDR notation, and identify private, public, loopback, and reserved ranges used in Cloud and DevOps designs.

Every route, security group, and Kubernetes Service starts with an address plan. This module builds addressing literacy before Module 5’s subnet math.

This is a core tutorial in **Module 4 · IP Addressing** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [TCP/IP Model](tcp-ip-model.md)
- Linux lab with `ip` and `ipcalc`

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain IPv4 (32-bit) and IPv6 (128-bit) forms  
- [ ] Convert between dotted masks and CIDR prefixes  
- [ ] Identify RFC 1918 private space  
- [ ] Recognise loopback, link-local, and documentation ranges  
- [ ] Inspect your host’s addresses and classify them

## Architecture

This topic’s control points and relationships are shown below.

![IP addressing concepts](../assets/excalidraw/ip-addressing.svg)

## Theory

### IPv4

32-bit addresses written as four octets: `10.0.1.15`. With a mask, bits split into **network** and **host** parts.

### IPv6 (first-class, not optional trivia)

128-bit addresses, hex, often shortened (`2001:db8::1`). Cloud networks increasingly dual-stack. Remember:

| IPv6 idea | Example |
|-----------|---------|
| Loopback | `::1` |
| Link-local | `fe80::/10` |
| Documentation | `2001:db8::/32` |
| DNS | `AAAA` records |

### Binary basics

Powers of two drive sizing: `/24` → 8 host bits → 256 addresses. You will use this constantly in Module 5.

### CIDR and subnet masks

| CIDR | Mask | Host bits | Addresses |
|------|------|----------:|----------:|
| /32 | 255.255.255.255 | 0 | 1 |
| /24 | 255.255.255.0 | 8 | 256 |
| /20 | 255.255.240.0 | 12 | 4096 |
| /16 | 255.255.0.0 | 16 | 65536 |

### Public vs private (RFC 1918)

| Block | Range |
|-------|-------|
| `10.0.0.0/8` | 10.0.0.0 – 10.255.255.255 |
| `172.16.0.0/12` | 172.16.0.0 – 172.31.255.255 |
| `192.168.0.0/16` | 192.168.0.0 – 192.168.255.255 |

### Special addresses

| Range | Role |
|-------|------|
| `127.0.0.0/8` | Loopback |
| `169.254.0.0/16` | Link-local; AWS metadata `169.254.169.254` |
| `0.0.0.0/0` | Default route (all destinations) |
| Broadcast | All-hosts on a subnet (IPv4), e.g. `.255` on `/24` |

## Hands-on Lab

**Focus:** practise the core workflow for IP Addressing

```bash
mkdir -p ~/rebash-networking/module-04
cd ~/rebash-networking/module-04
sudo apt-get update && sudo apt-get install -y ipcalc iproute2
```

### Step 1 — Read host addresses

```bash
ip -4 -br addr
ip -6 -br addr
```

### Step 2 — Classify with ipcalc

```bash
ipcalc 10.0.1.15/24
ipcalc 192.168.0.10/24
ipcalc 8.8.8.8/32
```

### Step 3 — Private vs public script

```bash
classify() {
  case "$1" in
    10.*|192.168.*|172.1[6-9].*|172.2[0-9].*|172.3[0-1].*) echo "$1 PRIVATE" ;;
    127.*) echo "$1 LOOPBACK" ;;
    169.254.*) echo "$1 LINK-LOCAL" ;;
    *) echo "$1 PUBLIC_OR_OTHER" ;;
  esac
}
classify 10.0.1.5
classify 8.8.8.8
classify 169.254.169.254
```

### Step 4 — IPv6 awareness

```bash
ip -6 addr show scope link | head
ip -6 addr show scope global | head
```

### Step 5 — Save notes

```bash
ip -br addr | tee addressing-baseline.txt
```

## Validation

- [ ] List three RFC 1918 blocks  
- [ ] Explain `/24` vs `/16`  
- [ ] Identify loopback and link-local examples  
- [ ] Baseline file saved

## Code Walkthrough

Production practice for **IP Addressing** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for networking as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Skipping fundamentals for IP Addressing"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for IP Addressing"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode IP Addressing changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |

## Summary

IPv4/IPv6 identify nodes. CIDR expresses network size. Private space is the default for Cloud/DevOps workloads; public addresses are deliberate edges.

## Interview Questions

1. How does **IP Addressing** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Subnetting and VLSM](subnetting-and-vlsm.md)

## References

- [RFC 791](https://www.rfc-editor.org/rfc/rfc791) · [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) · [RFC 4291 IPv6](https://www.rfc-editor.org/rfc/rfc4291)
