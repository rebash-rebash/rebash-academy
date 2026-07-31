---
title: "Routing Fundamentals"
description: "Master routing tables, default gateways, longest prefix match, static routes, IP forwarding, and how Linux and cloud route tables forward packets between subnets."
difficulty: intermediate
estimated_time: "50–65 min"
technology: networking
category: networking
module: "Module 6 · Routing"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - linux-administrator
  - site-reliability-engineer
  - kubernetes-engineer
skills:
  - routing
  - ip-route
  - default-gateway
  - longest-prefix-match
prerequisites:
  - networking/subnetting-and-vlsm
next:
  - networking/ethernet-switching-and-vlans
related:
  - networking/cloud-networking-vpc-and-subnets
  - networking/nat-and-port-forwarding
  - linux/linux-networking-tools
labs: []
projects: []
interview: interview/networking
certifications:
  - CompTIA Network+
  - AWS SAA
  - Azure AZ-104
tags:
  - networking
  - routing
  - ip-route
  - gateway
  - static-routes
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Routing Fundamentals

## Overview

Read and explain a Linux routing table, prove how longest prefix match works, add/remove a lab static route safely, and map the same ideas to cloud VPC route tables.

**Routing** is how packets leave a subnet. When an app talks to a database in another CIDR — or to a public API — the kernel chooses a **next hop** from the **routing table**. Bad routes look like firewall bugs: asymmetric paths, black holes, and “works on the host, fails from elsewhere.”

This is **Module 6 — Routing**. Complete [Subnetting and VLSM](subnetting-and-vlsm.md) first.

This is a core tutorial in **Module 6 · Routing** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Subnetting and VLSM](subnetting-and-vlsm.md)
- [IP Addressing](ip-addressing.md)
- Linux lab host with a default route

### Recommended

- `sudo` for temporary static routes and IP forwarding experiments
- `~/rebash-networking/module-02/` from Tutorial 4

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain on-link vs gateway delivery  
- [ ] Read `ip route` and `ip route get` output  
- [ ] Apply longest prefix match to competing routes  
- [ ] Add and delete a static route in a lab  
- [ ] Describe static vs dynamic routing at a practical level  
- [ ] Enable/verify IP forwarding on Linux for lab router scenarios  
- [ ] Map routes to AWS/GCP/Azure route table concepts  
- [ ] Diagnose common routing failures systematically

## Architecture

Packets move subnet → router → subnet (or Internet). More specific prefixes win.

![Routing fundamentals](../assets/excalidraw/routing-fundamentals.svg)

## Theory

### On-link vs routed delivery

| Destination | Kernel action |
|-------------|---------------|
| Same subnet as an interface | Resolve destination MAC; deliver on-link |
| Different subnet | Resolve **gateway** MAC; send to next hop |

No default route ⇒ most off-subnet traffic fails with `Network is unreachable`.

### Routing table entries

Typical fields you will see:

| Field | Meaning |
|-------|---------|
| Destination prefix | Match (for example `10.0.2.0/24`, `default`) |
| `via` | Next-hop IP |
| `dev` | Egress interface |
| `proto` | Origin (`kernel`, `static`, `dhcp`, …) |
| `metric` | Preference when prefixes tie (lower usually wins) |
| `src` | Preferred source address (when shown) |

### Longest prefix match

When multiple routes match, the **most specific** (longest prefix) wins.

| Destination | Next hop | Notes |
|-------------|----------|-------|
| `10.0.2.0/24` | `10.0.1.1` | Wins for `10.0.2.10` |
| `10.0.0.0/8` | `10.0.1.1` | Broader — loses to `/24` |
| `0.0.0.0/0` | `10.0.1.1` | Default — last resort |

This is why a dangling specific route can black-hole traffic even when the default route looks fine.

### Default gateway

`default` / `0.0.0.0/0` is the route for “everywhere else.” Cloud equivalents: default route to an **Internet Gateway**, **NAT Gateway**, or virtual appliance ENI.

### Static vs dynamic routing

| Style | How routes appear | Where you see it |
|-------|-------------------|------------------|
| **Static** | Admin/IaC installs prefixes | Host `ip route add`, VPC static routes |
| **Dynamic** | Protocols exchange reachability | BGP at the edge, OSPF in DCs |

DevOps daily work is mostly **static** (VPC tables, host routes, CNI). You still need the vocabulary of BGP/OSPF for hybrid and interviews.

### IP forwarding

A Linux host becomes a router when:

1. IP forwarding is enabled (`net.ipv4.ip_forward=1`)  
2. Interfaces exist in multiple networks  
3. Other hosts use it as a gateway  
4. Firewall policy allows transit  

Cloud routers/gateways hide this, but the packet logic is the same.

### Cloud mapping

| Linux idea | AWS | Azure | GCP |
|------------|-----|-------|-----|
| Route table | VPC route table | Route table | Routes in VPC |
| Default to Internet | `igw-…` | Internet gateway | Default Internet gateway |
| Default private egress | NAT Gateway | NAT Gateway | Cloud NAT |
| More specific route | Longer prefix in table | Same | Same |
| `ip route get` | Effective route in console / reachability analyser | Effective routes | Network Intelligence / tests |

## Hands-on Lab

**Focus:** practise the core workflow for Routing Fundamentals

```bash
mkdir -p ~/rebash-networking/module-02
cd ~/rebash-networking/module-02

sudo apt-get update
sudo apt-get install -y iproute2 iputils-ping traceroute
```

Confirm you have a default route:

```bash
ip route show default
ip route get 1.1.1.1
```

### Step 1 — Dump the table

```bash
cd ~/rebash-networking/module-02
ip route
ip -4 route show table main
```

**Expected:** At least one `default via …` line and on-link subnet routes (`proto kernel`).

### Step 2 — Ask the kernel for a decision

```bash
ip route get 1.1.1.1
ip route get 127.0.0.1

# Replace with an address inside your own CIDR
MY_IP=$(ip -4 -o addr show scope global | awk '{print $4; exit}' | cut -d/ -f1)
ip route get "$MY_IP"
```

**Expected:** `ip route get` prints the chosen `via`/`dev`/`src` for that destination.

### Step 3 — Save a routing baseline

```bash
{
  echo "=== ip route ==="
  ip route
  echo
  echo "=== route get 1.1.1.1 ==="
  ip route get 1.1.1.1
  echo
  echo "=== addresses ==="
  ip -4 -br addr
} | tee routing-baseline.txt
```

### Step 4 — Trace the path (best effort)

```bash
traceroute -n 1.1.1.1 | head -n 15
# or: tracepath -n 1.1.1.1
```

**Expected:** A list of hops. `* * *` often means a hop does not reply to probes — not always a failure.

### Step 5 — Temporary static route (safe pattern)

Use a **black-hole test prefix** that you do not need (`203.0.113.0/24` is documentation space — still avoid sending real traffic there). Prefer adding a route only if you understand egress.

```bash
IFACE=$(ip route show default | awk '/default/ {print $5; exit}')
GW=$(ip route show default | awk '/default/ {print $3; exit}')
echo "iface=$IFACE gw=$GW"

# Example: more-specific route via the same default gateway (lab illustration)
sudo ip route add 203.0.113.0/24 via "$GW" dev "$IFACE"
ip route show | grep 203.0.113 || true
ip route get 203.0.113.10

# Always remove when done
sudo ip route del 203.0.113.0/24 || true
ip route show | grep 203.0.113 || echo "lab route removed"
```

**Expected:** While present, `ip route get 203.0.113.10` selects that `/24`. After delete, it falls back to `default`.

!!! warning
    Never add random routes on production hosts. Wrong `via` values create silent black holes.

### Step 6 — Inspect IP forwarding (read-only first)

```bash
sysctl net.ipv4.ip_forward
# Lab-only enable (reverts on reboot unless persisted):
# sudo sysctl -w net.ipv4.ip_forward=1
```

**Expected:** `0` on typical clients; `1` on routers/gateways/NAT instances.

### Step 7 — Failure simulation (mental + command)

```bash
# Show what happens conceptually without a default route (DO NOT delete default in production)
ip route show default
```

Write in your notes: if `default` disappeared, which destinations would still work? (Answer: on-link subnet only.)

## Validation

- [ ] You can explain on-link vs via-gateway delivery  
- [ ] `routing-baseline.txt` exists  
- [ ] `ip route get 1.1.1.1` shows `via` and `dev`  
- [ ] You can explain longest prefix match with one example  
- [ ] Lab static route was added and removed  
- [ ] You can name the cloud object that holds subnet routes  

```bash
test -f ~/rebash-networking/module-02/routing-baseline.txt && echo "routing baseline: OK"
ip route show default | grep -q default && echo "default route: OK"
```

## Code Walkthrough

Production practice for **Routing Fundamentals** always combines:

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

!!! warning "Skipping fundamentals for Routing Fundamentals"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Routing Fundamentals"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Routing Fundamentals changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | Commands | Fix direction |
|---------|--------------|----------|---------------|
| `Network is unreachable` | No matching route | `ip route`, `ip route get` | Restore default / specific route |
| Wrong egress interface | Bad static route / metric | `ip route get D` | Delete conflicting prefix |
| One-way traffic | Asymmetric return path | paths both ways | Align return routes |
| Works on-link only | Missing default | `ip route show default` | DHCP / cloud route table |
| Looks like firewall | Black-hole route | `ip route get` | Remove bad specific route |

Triage order: **address present → route exists → neighbour for next hop → firewall → app port**.

## Summary

- Routing selects a **next hop** when the destination is off-link.  
- **Longest prefix match** decides among overlapping routes.  
- `ip route` and `ip route get` are the source of truth on Linux.  
- Static routes dominate Cloud/DevOps; dynamic protocols matter at edges.  
- Cloud route tables are the same mental model with provider gateways.

## Interview Questions

1. How does **Routing Fundamentals** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - Continue with [Ethernet, Switching, and VLANs](ethernet-switching-and-vlans.md) — MAC forwarding and VLAN segmentation on the local path.

## References

- [RFC 1812 – Requirements for IP Version 4 Routers](https://www.rfc-editor.org/rfc/rfc1812)  
- [ip-route(8)](https://man7.org/linux/man-pages/man8/ip-route.8.html)  
- [AWS VPC route tables](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html)  
- [Azure routing overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-udr-overview)
