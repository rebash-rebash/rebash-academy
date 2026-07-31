---
title: "Subnetting and VLSM"
description: "Master CIDR calculations, network/broadcast addresses, usable hosts, and Variable Length Subnet Masking (VLSM) for Cloud VPC design."
difficulty: beginner
estimated_time: "60–75 min"
technology: networking
category: networking
module: "Module 5 · Subnetting"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - linux-administrator
  - site-reliability-engineer
skills:
  - subnetting
  - vlsm
  - cidr
prerequisites:
  - networking/ip-addressing
next:
  - networking/routing-fundamentals
related:
  - networking/cloud-networking-vpc-and-subnets
interview: interview/networking
certifications:
  - CompTIA Network+
  - AWS SAA
  - Azure AZ-104
tags:
  - networking
  - subnetting
  - vlsm
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Subnetting and VLSM

## Overview

Calculate network address, broadcast, and usable hosts for any IPv4 CIDR, then split a parent block with VLSM into non-overlapping Cloud-style tiers.

Subnetting turns a large address block into smaller segments. **VLSM** lets each segment be a different size — exactly how you size public, private, and data subnets in a VPC.

This is a core tutorial in **Module 5 · Subnetting** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [IP Addressing](ip-addressing.md)
- `ipcalc` installed

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Calculate network and broadcast for a CIDR  
- [ ] Compute usable host counts  
- [ ] Split a `/24` into equal `/26` subnets  
- [ ] Apply VLSM without overlaps  
- [ ] Draft a mini VPC subnet plan

## Architecture

This topic’s control points and relationships are shown below.

![VLSM from a parent prefix](../assets/excalidraw/subnetting-vlsm.svg)

## Theory

### What it is

Subnetting splits an Internet Protocol version 4 (IPv4) network into smaller Classless Inter-Domain Routing (CIDR) blocks. **Variable Length Subnet Masking (VLSM)** means those children need not be equal size — edge, app, and data tiers get only the addresses they need. Formulae tell you block size, network, broadcast, and usable ranges; cloud platforms add reserved addresses on top.

### Why it matters

Wrong sizing forces painful renumbering later. Overlaps break Virtual Private Cloud (VPC) peering, transit gateways, and Virtual Private Network (VPN) routes. Undersized subnets stall autoscaling; oversized ones waste space and widen blast radius. DevOps engineers who can compute CIDRs design landing zones that still fit in two years.

### How it works

IPv4 addresses are 32 bits. A prefix `/p` leaves `32 − p` **host bits**. Total addresses in the block = `2^(32 − p)`. In classic Ethernet on-link subnets, usable hosts ≈ total − 2 (network and broadcast). Cloud providers also reserve gateway, DNS, and other addresses — always check their docs when sizing (a `/28` may yield fewer usable IPs than the classic formula). Align child blocks on their natural boundaries (a `/26` starts on multiples of 64). With VLSM, carve unequally from one parent without overlaps; verify with `ipcalc` or equivalent before applying Infrastructure as Code.

**Manual pattern (`192.168.10.0/26`):** host bits = 6 → size 64; network `192.168.10.0`, broadcast `192.168.10.63`; classic usable `192.168.10.1`–`62`.

### Key concepts and comparisons

| Idea | Formula / rule |
|------|----------------|
| Total addresses | `2^(32 − prefix)` |
| Classic usable | total − 2 (network + broadcast) |
| Cloud usable | total − platform reservations |
| Alignment | Block start must match size |

Example parent `10.1.0.0/24`:

| Tier | CIDR | Why that size |
|------|------|----------------|
| Edge | `10.1.0.0/28` | Few LBs / NAT |
| Data | `10.1.0.32/27` | Modest DB tier |
| App | `10.1.0.64/26` | Larger workload pool |

### Common pitfalls

- Counting usable hosts with the classic −2 formula in AWS/Azure/GCP subnets.  
- Overlapping children (`10.1.0.0/26` and `10.1.0.32/27`).  
- Choosing `/16` everywhere “for simplicity” and exhausting transit/VPN uniqueness.  
- Forgetting future AZ splits — paint yourself into a corner with one huge subnet.  
- Mental maths without `ipcalc` on production PRs.

## Hands-on Lab

**Focus:** practise the core workflow for Subnetting and VLSM

```bash
mkdir -p ~/rebash-networking/module-05
cd ~/rebash-networking/module-05
sudo apt-get install -y ipcalc
```

### Step 1 — Equal split

```bash
for n in 10.0.0.0/26 10.0.0.64/26 10.0.0.128/26 10.0.0.192/26; do
  echo "==== $n ===="; ipcalc "$n" | sed -n '1,10p'; echo
done
```

### Step 2 — VLSM verify

```bash
ipcalc 10.1.0.0/28
ipcalc 10.1.0.32/27
ipcalc 10.1.0.64/26
```

### Step 3 — Mini VPC plan

Plan `10.20.0.0/16` with `public-a/b`, `private-a/b`, `data-a` as `/24`s. Validate:

```bash
./../module-01/../module-05/subnet-plan-check.sh 2>/dev/null || true
for c in 10.20.0.0/16 10.20.0.0/24 10.20.1.0/24 10.20.10.0/24 10.20.11.0/24 10.20.20.0/24; do
  echo "==== $c ===="; ipcalc "$c" | sed -n '1,8p'; echo
done | tee vpc-plan.txt
```

### Step 4 — Host CIDR practice

```bash
IP_CIDR=$(ip -4 -o addr show scope global | awk '{print $4; exit}')
ipcalc "$IP_CIDR"
```

## Validation

- [ ] Compute `/26` usable hosts (62 classic)  
- [ ] Non-overlapping VLSM example written  
- [ ] `vpc-plan.txt` saved

## Code Walkthrough

Production practice for **Subnetting and VLSM** always combines:

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

!!! warning "Counting usable hosts with the classic −2 formula in AWS/Azure/GCP subnets.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Overlapping children (`10.1.0.0/26` and `10.1.0.32/27`).  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Subnetting and VLSM changes as code and review them in pull requests
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

Subnetting sizes segments. VLSM sizes them efficiently. Cloud VPC design is subnetting with availability zones and reserved addresses.

## Interview Questions

1. How does **Subnetting and VLSM** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Routing Fundamentals](routing-fundamentals.md)

## References

- [RFC 4632 CIDR](https://www.rfc-editor.org/rfc/rfc4632)  
- [AWS VPC CIDR blocks](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html)
