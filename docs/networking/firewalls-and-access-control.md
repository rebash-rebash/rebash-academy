---
title: "Firewalls and Access Control"
description: "Master stateful vs stateless filtering, iptables/nftables and UFW, cloud security groups and network ACLs, and least-privilege network design for DevOps."
difficulty: intermediate
estimated_time: "45–60 min"
technology: networking
category: networking
module: "Module 11 · NAT & Firewalls"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - linux-administrator
  - site-reliability-engineer
  - kubernetes-engineer
skills:
  - firewalls
  - iptables
  - nftables
  - security-groups
  - network-acls
prerequisites:
  - networking/nat-and-port-forwarding
next:
  - networking/linux-networking-toolkit
related:
  - networking/tcp-and-udp-deep-dive
  - networking/network-security-hardening
  - networking/firewall-change-control-and-production-acls
labs:
  - labs/networking-dns-firewall-triage
projects: []
interview: interview/networking
certifications:
  - CompTIA Network+
  - AWS SAA
  - Azure AZ-104
tags:
  - networking
  - firewall
  - iptables
  - nftables
  - ufw
  - security-groups
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Firewalls and Access Control

## Overview

Design and debug least-privilege firewall policy across host firewalls and cloud controls, and explain stateful vs stateless filtering with concrete examples.

Firewalls decide which packets may enter, leave, or cross a boundary. Misconfigured rules cause more outages than glamorous attacks: blocked health checks, forgotten ephemeral returns on NACLs, or `0.0.0.0/0` on database ports.

This is the second tutorial in **Module 11 — NAT & Firewalls**. Complete [NAT and Port Forwarding](nat-and-port-forwarding.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 11 · NAT & Firewalls** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [NAT and Port Forwarding](nat-and-port-forwarding.md)
- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md) — ports and states
- Linux VM with `sudo`

### Recommended

- Cloud account for Security Group / NACL reading (free tier is enough)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Contrast stateful vs stateless packet filtering  
- [ ] Describe iptables chains/tables and why nftables is preferred going forward  
- [ ] Apply a simple UFW policy safely in a lab  
- [ ] Differentiate Security Groups vs Network ACLs  
- [ ] Design least-privilege allow lists for common app tiers  
- [ ] Troubleshoot “timeout” caused by filter drops

## Architecture

Defence in depth: edge NACL/SG style controls plus host firewall in front of the app.

![Firewalls and access control](../assets/excalidraw/firewalls-access-control.svg)

## Theory

### What a firewall matches

Typical rule fields: source/destination IP, protocol, port, interface, and (if stateful) connection state — **new**, **established**, **related**.

Actions: **accept**, **reject** (notify), **drop** (silent). Silent drops look like routing failures (timeouts).

### Stateful vs stateless

| Aspect | Stateless | Stateful |
|--------|-----------|----------|
| Memory | Per packet | Per flow |
| Return traffic | Must allow explicitly | Often automatic |
| Cloud example | AWS Network ACL | AWS Security Group |
| Host example | Simple raw filters | iptables/nft + conntrack, UFW |

### Linux: iptables and nftables

**iptables** uses tables (`filter`, `nat`, `mangle`) and chains (`INPUT`, `FORWARD`, `OUTPUT`). **nftables** is the modern replacement with a unified ruleset. UFW is a simpler frontend for common host policies.

Conceptual filter policy:

```text
default deny inbound
allow established/related
allow SSH from admin CIDR
allow 443 from load balancer CIDR
```

### UFW (lab-friendly)

```bash
# Pattern only — adapt interfaces and CIDRs for your lab
# sudo ufw default deny incoming
# sudo ufw default allow outgoing
# sudo ufw allow OpenSSH
# sudo ufw enable
# sudo ufw status verbose
```

### Cloud: Security Groups vs NACLs

| Control | Scope | State | Rules |
|---------|-------|-------|-------|
| **Security Group** | ENI / instance | Stateful | Allow rules (deny implicit) |
| **Network ACL** | Subnet | Stateless | Numbered allow/deny; need both directions |

Least privilege: SG on the database allows **only** the app tier SG (or CIDR), not `0.0.0.0/0`. NACL changes are coarser and easier to break with missing ephemeral port allows.

### Layered design

1. Edge / subnet controls (NACL, perimeter)  
2. Instance / ENI Security Groups  
3. Host firewall (nft/UFW)  
4. Application authn/authz  

Network allow lists never replace application authentication.

## Hands-on Lab

**Focus:** practise the core workflow for Firewalls and Access Control

```bash
mkdir -p ~/rebash-networking/module-11
cd ~/rebash-networking/module-11

sudo apt-get update
sudo apt-get install -y ufw iptables nftables
```

!!! warning "Do not lock yourself out"
    Keep an active console session. Prefer lab VMs. Never enable UFW on a remote host without allowing SSH first.

### Step 1 – Inventory current host policy

```bash
sudo iptables -L -n -v 2>/dev/null | head -40
sudo nft list ruleset 2>/dev/null | head -40
sudo ufw status verbose 2>/dev/null || true
```

### Step 2 – Prove timeout vs refused (filter mental model)

```bash
# Refused: host reachable, nothing listening (from Module 8)
nc -zv -w 2 127.0.0.1 19999 2>&1 || true
```

A **firewall drop** on a remote IP looks like **timeout**, not refused. Keep that distinction for incidents.

### Step 3 – Sketch a three-tier policy

Document in `~/rebash-networking/module-11/policy.md`:

```text
Web SG: inbound 443 from 0.0.0.0/0 (or CDN only)
App SG: inbound 8080 from Web SG only
DB SG: inbound 5432 from App SG only
Admin: SSH 22 from office/VPN CIDR only
```

### Step 4 – Stateless NACL reminder

Write the return-path rule you would need if NACLs are in use (ephemeral ports for clients). Stateful SGs do not need that mirror for return traffic.

### Step 5 – Optional UFW lab (local VM only)

```bash
sudo ufw status
# If experimenting: allow OpenSSH BEFORE enable
```

### Step 6 – Correlate with NAT

Outbound from private subnets still needs NAT (Module 11 part 1). Firewalls that block ephemeral return or DNS break “NAT looks up but apps fail” incidents — check DNS and filter together.

## Validation

- [ ] Lab commands run under `~/rebash-networking/module-11/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Firewalls and Access Control** always combines:

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

!!! warning "Skipping fundamentals for Firewalls and Access Control"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Firewalls and Access Control"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Firewalls and Access Control changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Connection timed out | Drop / NACL miss / route | Check SG, NACL both ways, routes |
| Connection refused | Reachable, no listener | Not a firewall success — check service |
| Health checks fail | Probe IP/SG missing | Allow LB/health CIDR or SG |
| Works then fails | Rule order / deny later | Read numbered NACL / nft counters |
| SSH lockout | UFW/SG too tight | Console recovery; break-glass CIDR |

## Summary

- **Stateful** tracks flows; **stateless** needs explicit return paths  
- Host (**nft/UFW**) and cloud (**SG/NACL**) are complementary layers  
- Prefer **least privilege** and SG-to-SG references over wide CIDRs  
- **Drops → timeouts**; use that when triage starts

## Interview Questions

1. How does **Firewalls and Access Control** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Linux Networking Toolkit](linux-networking-toolkit.md)  
- [Network Security Hardening](network-security-hardening.md)  
- [Firewall Change Control and Production ACLs](firewall-change-control-and-production-acls.md)

## References

- [nftables wiki](https://wiki.nftables.org/)  
- [UFW](https://help.ubuntu.com/community/UFW)  
- [AWS Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)  
- [AWS Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
