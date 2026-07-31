---
title: "OSI Model"
description: "Master the seven OSI layers for Cloud and DevOps — Physical through Application — with encapsulation, tool mapping, and layered troubleshooting."
difficulty: beginner
estimated_time: "50–65 min"
technology: networking
category: networking
module: "Module 2 · OSI Model"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - linux-administrator
  - site-reliability-engineer
  - kubernetes-engineer
  - platform-engineer
skills:
  - osi-model
  - layered-troubleshooting
prerequisites:
  - networking/introduction-to-networking
next:
  - networking/tcp-ip-model
related:
  - networking/tcp-ip-model
  - networking/network-troubleshooting-methodology
  - interview/networking
labs: []
projects: []
interview: interview/networking
certifications:
  - CompTIA Network+
  - CCNA
tags:
  - networking
  - osi
  - layers
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# OSI Model

## Overview

Use the seven OSI layers as a shared language: name the layer, pick the tool, and stop at the first failing layer during an incident.

The **OSI model** (Open Systems Interconnection) is a seven-layer reference model. Cloud consoles and load-balancer docs still say “Layer 4” and “Layer 7” because of it. This module covers each layer with Cloud/DevOps examples — not abstract memorisation alone.

This is a core tutorial in **Module 2 · OSI Model** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [What is Networking?](introduction-to-networking.md)
- Linux lab with `curl`, `ss`, `ip`, `ping`

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Name OSI layers 1–7 with one protocol or example each  
- [ ] Explain encapsulation and PDU names (frame, packet, segment)  
- [ ] Map common Linux tools to layers  
- [ ] Run a top-down troubleshooting checklist  
- [ ] Explain L4 vs L7 load balancing vocabulary

## Architecture

This topic’s control points and relationships are shown below.

![OSI model and encapsulation](../assets/excalidraw/osi-model.svg)

## Theory

### Why layers exist

| Benefit | Practice |
|---------|----------|
| Shared vocabulary | “L4 timeout” vs “L7 502” |
| Tool selection | `curl` vs `ss` vs `ip link` |
| Interoperability | IP over Ethernet or Wi‑Fi |
| Faster incidents | Stop at first failing layer |

### Layer 1 — Physical

Bits on media: copper, fibre, radio. Symptoms: cable unplugged, NIC down, wrong speed.

**Tools:** `ip link`, `ethtool`, cloud “interface attached?” checks.

### Layer 2 — Data Link

Frames and MAC addresses. Ethernet switching, VLANs, ARP live here.

**Tools:** `ip link`, `ip neigh`, switch/cloud L2 fabric.

### Layer 3 — Network

Logical addressing and routing: IPv4/IPv6, ICMP, route tables.

**Tools:** `ip addr`, `ip route`, `ping`, `traceroute`.

### Layer 4 — Transport

End-to-end: TCP/UDP, ports, reliability choices.

**Tools:** `ss`, `nc`, NACL/security-group port rules, L4 load balancers.

### Layer 5 — Session

Session semantics (often folded into apps/TLS in practice).

**Examples:** TLS sessions, RPC sessions, managed connection pools.

### Layer 6 — Presentation

Encoding and encryption: TLS, JSON, Protobuf, character sets.

**Tools:** `openssl s_client`, certificate inspectors.

### Layer 7 — Application

User protocols: HTTP, DNS, SSH, SMTP, gRPC.

**Tools:** `curl`, `dig`, API clients, L7 load balancers / Ingress.

### Encapsulation

HTTP request → TCP segment → IP packet → Ethernet frame → bits.

Routers rewrite Layer 2 headers each hop; IP addresses usually stay end-to-end until NAT.

### Tool-to-layer map

| Tool | Layer focus |
|------|-------------|
| `curl` / `dig` | 7 |
| `openssl s_client` | 6–7 |
| `ss` / `nc` | 4 |
| `ping` / `ip route` | 3 |
| `ip neigh` | 2–3 edge |
| `ip link` | 1–2 |
| `tcpdump` | 2–7 |

## Hands-on Lab

**Focus:** practise the core workflow for OSI Model

```bash
mkdir -p ~/rebash-networking/module-02
cd ~/rebash-networking/module-02
sudo apt-get update
sudo apt-get install -y curl iproute2 iputils-ping dnsutils netcat-openbsd
```

### Step 1 — Layer 7

```bash
curl -sI --max-time 10 https://example.com/ | head -n 10
```

### Step 2 — Layer 4

```bash
ss -tulpn | head -n 15
nc -vz example.com 443
```

### Step 3 — Layer 3

```bash
ip route get 1.1.1.1
ping -c 3 1.1.1.1 || echo "ICMP filtered"
```

### Step 4 — Layer 2 edge

```bash
ip -br link
GW=$(ip route show default | awk '/default/ {print $3; exit}')
ping -c 1 "$GW" 2>/dev/null || true
ip neigh show | head
```

### Step 5 — Layered checklist script

```bash
cat > osi-check.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
host="${1:-example.com}"
echo "L7 HTTP"; curl -sI --max-time 10 "https://$host/" | head -n 3
echo "L7 DNS"; dig +short "$host" A | head -n 2
echo "L4 TCP"; nc -vz -w 5 "$host" 443
echo "L3 route"; ip route get "$(dig +short "$host" A | head -n 1)"
EOF
chmod +x osi-check.sh
./osi-check.sh example.com
```

## Validation

- [ ] Recite layers 7→1 with one example each  
- [ ] Explain frame vs packet vs segment  
- [ ] `./osi-check.sh` runs or fails at a named layer you can explain

## Code Walkthrough

Production practice for **OSI Model** always combines:

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

!!! warning "Skipping fundamentals for OSI Model"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for OSI Model"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode OSI Model changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

Work **top-down** for app outages: L7 → DNS → L4 → L3 → L2 → L1. Stop at the first failure.

## Summary

OSI gives Cloud and DevOps a precise vocabulary. Encapsulation wraps data for the wire. Tools map to layers. Top-down checks beat random packet captures.

## Interview Questions

1. How does **OSI Model** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [TCP/IP Model](tcp-ip-model.md) — how the Internet stack maps onto OSI.

## References

- [ISO/IEC 7498 / OSI model](https://en.wikipedia.org/wiki/OSI_model)  
- [RFC 1122](https://www.rfc-editor.org/rfc/rfc1122)
