---
title: "Ethernet, Switching, and VLANs"
description: "Learn MAC addresses, Ethernet frames, switch forwarding, VLAN segmentation, access vs trunk ports, and ARP/neighbour resolution on Linux for Cloud and DevOps networks."
difficulty: beginner
estimated_time: "45–60 min"
technology: networking
category: networking
module: "Module 7 · Switching"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - linux-administrator
  - site-reliability-engineer
  - kubernetes-engineer
skills:
  - ethernet
  - switching
  - vlans
  - arp
prerequisites:
  - networking/routing-fundamentals
next:
  - networking/icmp-arp-dhcp-and-network-services
related:
  - networking/icmp-arp-dhcp-and-network-services
  - docker/docker-networking-fundamentals
  - linux/linux-networking-tools
labs: []
projects: []
interview: interview/networking
certifications:
  - CompTIA Network+
  - AWS SAA
tags:
  - networking
  - ethernet
  - switching
  - vlan
  - arp
  - mac-address
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Ethernet, Switching, and VLANs

## Overview

Finish with a clear Layer 2 model — MAC forwarding, VLAN segmentation, and ARP/neighbour resolution — and a verified lab snapshot of your interface MAC, neighbour table, and (optional) VLAN sub-interface on Linux.

Before IP packets cross the Internet, they travel as **Ethernet frames** on local segments. **Switches** forward those frames using **MAC addresses**. **VLANs** carve one physical fabric into isolated broadcast domains. Cloud VPC subnets, Docker bridges, and Kubernetes node networks all rest on these ideas — even when you never touch a physical switch.

This is **Module 7 — Switching**. Complete [Routing Fundamentals](routing-fundamentals.md) first.

This is a core tutorial in **Module 7 · Switching** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Routing Fundamentals](routing-fundamentals.md)
- [Subnetting and VLSM](subnetting-and-vlsm.md)
- Linux lab host with at least one Ethernet/Wi‑Fi interface

### Recommended

- `sudo` for VLAN creation and optional packet capture
- Workspace from Module 1: `~/rebash-networking/module-01/`

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain MAC addresses and how they differ from IP addresses
- [ ] Describe Ethernet II frame roles (source/destination MAC, EtherType)
- [ ] Explain how a switch learns MACs and forwards (or floods) frames
- [ ] Define VLANs and contrast access vs trunk (802.1Q) ports
- [ ] Inspect MAC addresses and the neighbour/ARP table on Linux
- [ ] Create and remove a VLAN sub-interface safely in a lab
- [ ] Map Layer 2 ideas to Docker bridges and cloud virtual switches

## Architecture

VLANs isolate broadcast domains; a Layer 3 device routes between them.

| Concept | Job | Cloud / DevOps mapping |
|---------|-----|------------------------|
| MAC address | Host identity on a segment | ENI MAC, veth MAC |
| Switch | Forward frames in a broadcast domain | VPC subnet fabric, Linux bridge |
| VLAN | Logical segment on shared hardware | Often modelled as separate subnets in cloud |
| Trunk (802.1Q) | Carry multiple VLANs on one link | Hypervisor uplinks, DC fabrics |
| ARP / neighbour | Map IP → MAC on-link | Required before first packet to gateway |

![Ethernet switching and VLANs](../assets/excalidraw/switching-vlans.svg)

## Theory

### MAC addresses

A **MAC** is a 48-bit Layer 2 identifier, written as six hex octets: `00:1a:2b:3c:4d:5e`.

| Property | MAC | IP |
|----------|-----|-----|
| OSI layer | 2 | 3 |
| Scope | Local segment | End-to-end (until NAT) |
| Assigned by | Vendor / hypervisor | Admin / DHCP / cloud |
| Per hop | Rewritten at routers | Usually stable end-to-end |
| Format | 48-bit hex | IPv4 32-bit / IPv6 128-bit |

The first three octets are often an **OUI** (vendor id). Virtual environments frequently use **locally administered** MACs — do not assume every MAC is burned into silicon.

### Ethernet frames

Dominant **Ethernet II** layout (conceptual):

| Field | Role |
|-------|------|
| Destination MAC | Who should accept the frame |
| Source MAC | Who sent it |
| EtherType | Payload type (`0x0800` IPv4, `0x0806` ARP, `0x86DD` IPv6) |
| Payload | IP packet, ARP, … |
| FCS | Frame check sequence |

Switches forward using MACs; they do not route by IP.

### How switches forward

1. **Learn** — record source MAC → ingress port  
2. **Forward** — if destination MAC is known, send out that port  
3. **Flood** — if unknown (or broadcast), send to all ports in the VLAN except ingress  
4. **Filter** — do not send a frame back out the port it arrived on  

**Hubs** repeat bits to every port (collision domain). **Switches** isolate ports (each a collision domain). Hubs are obsolete in production.

### Broadcast domains and VLANs

A **broadcast domain** is the set of interfaces that receive Layer 2 broadcasts (including ARP). One VLAN ≈ one broadcast domain ≈ typically one IP subnet.

Why VLANs matter:

| Reason | Effect |
|--------|--------|
| Security | Keep app and data tiers off the same L2 segment |
| Performance | Shrink broadcast noise |
| Design clarity | Map environments / tenants to segments |
| Ops | Fault isolation when storms or loops occur |

### Access vs trunk

| Port type | Carries | Tagging |
|-----------|---------|---------|
| **Access** | One VLAN | Untagged toward the host |
| **Trunk** | Multiple VLANs | **802.1Q** tags on the wire |

Mis-matched VLAN IDs are a classic cause of “IP looks fine, but neighbours never appear.”

### ARP / neighbour resolution (preview)

On Ethernet, a host must know the **MAC** of the next hop (destination if on-link, else the gateway). **ARP** (IPv4) asks “who has this IP?” on the local segment. Linux exposes the cache as the **neighbour table** (`ip neigh`). Tutorial 6 deepens ICMP/ARP/DHCP together.

### Cloud and container mapping

| Classic L2 | Modern equivalent |
|------------|-------------------|
| Access VLAN + subnet | Cloud subnet in a VPC |
| Switch | Hypervisor / cloud fabric / Linux bridge |
| Trunk to router | Edge uplink / ENI attachment model |
| Host NIC | ENI, `veth`, `cni0`, `docker0` |

Cloud providers usually hide 802.1Q from you; you still design **isolation boundaries** the same way VLANs did on-prem.

## Hands-on Lab

**Focus:** practise the core workflow for Ethernet, Switching, and VLANs

```bash
mkdir -p ~/rebash-networking/module-02
cd ~/rebash-networking/module-02

sudo apt-get update
sudo apt-get install -y iproute2 iputils-ping vlan tcpdump
# Ensure 802.1Q module is available (lab VMs)
sudo modprobe 8021q || true
```

Confirm:

```bash
ip -br link
lsmod | grep -i 8021q || echo "8021q module not loaded (VLAN lab may be limited)"
```

### Step 1 — Read interface MACs

```bash
cd ~/rebash-networking/module-02
ip -br link
ip link show
```

**Expected:** Each interface shows a `link/ether` MAC (loopback has no Ethernet MAC).

Record your primary interface name (for example `eth0`, `ens5`, `enp0s3`).

### Step 2 — Capture a Layer 2 snapshot

```bash
{
  echo "=== links ==="
  ip -br link
  echo
  echo "=== mac detail ==="
  ip -o link | awk '{print $2, $0}' | head -n 20
} | tee l2-baseline.txt
```

### Step 3 — Populate and read the neighbour table

```bash
GW=$(ip route show default | awk '/default/ {print $3; exit}')
echo "Gateway: ${GW:-none}"

# Generate traffic so a neighbour entry appears
if [ -n "$GW" ]; then
  ping -c 2 "$GW" || true
fi

ip neigh show
ip -br neigh
```

**Expected:** An entry for the gateway (or other on-link hosts) with a MAC and state such as `REACHABLE` or `STALE`.

!!! note
    Wi‑Fi and some cloud networking paths still use neighbour resolution, but entry names and timing vary. Empty tables usually mean no recent on-link traffic.

### Step 4 — Same-subnet delivery check

```bash
ip -4 -br addr
ip route
```

Interpretation refresh:

- Destination **inside** your CIDR → resolve **destination** MAC  
- Destination **outside** → resolve **gateway** MAC, then route  

### Step 5 — Optional VLAN sub-interface (sudo)

Only on a disposable lab NIC you control. Replace `eth0` with your interface.

```bash
IFACE=$(ip -4 -o addr show scope global | awk '{print $2; exit}')
echo "Using interface: $IFACE"

# Create VLAN 100 sub-interface (lab only)
sudo ip link add link "$IFACE" name "${IFACE}.100" type vlan id 100
sudo ip link set "${IFACE}.100" up
ip -br link | grep "${IFACE}.100"

# Clean up immediately after inspection
sudo ip link delete "${IFACE}.100"
```

**Expected:** `${IFACE}.100` appears, then disappears after delete.

!!! warning
    Do not create VLANs on production uplinks. Wrong tags can isolate a host from its gateway.

### Step 6 — Optional: watch ARP with tcpdump

```bash
# Terminal A
sudo tcpdump -ni any -c 10 arp

# Terminal B (within a few seconds)
ping -c 1 "$GW"
```

**Expected:** ARP request/reply frames when the neighbour was unknown.

### Step 7 — Save lab notes

```bash
{
  echo "primary_iface=$(ip -4 -o addr show scope global | awk '{print $2; exit}')"
  echo "gateway=${GW:-none}"
  echo "neighbours:"
  ip -br neigh
} | tee vlan-lab-notes.txt
```

## Validation

- [ ] You can state MAC vs IP in one sentence each  
- [ ] You can explain learn / forward / flood on a switch  
- [ ] You can define VLAN, access port, and trunk port  
- [ ] `l2-baseline.txt` exists with MAC data  
- [ ] `ip neigh show` lists at least one entry after pinging the gateway (when a gateway exists)  
- [ ] Optional VLAN interface was created and deleted cleanly  

```bash
test -f ~/rebash-networking/module-02/l2-baseline.txt && echo "l2 baseline: OK"
ip neigh show | head -n 5
```

## Code Walkthrough

Production practice for **Ethernet, Switching, and VLANs** always combines:

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

!!! warning "Skipping fundamentals for Ethernet, Switching, and VLANs"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Ethernet, Switching, and VLANs"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Ethernet, Switching, and VLANs changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to run | Fix direction |
|---------|--------------|-------------|---------------|
| No neighbour for gateway | Wrong VLAN / no L2 path | `ip neigh`, `ip link` | Fix VLAN/tag or attachment |
| `Destination Host Unreachable` | ARP failed | `ping`, `ip neigh` | Check same subnet / gateway |
| Duplicate IP warnings | IP conflict | `ip neigh`, switch logs | Renumber host |
| VLAN lab fails | Missing `8021q` | `lsmod \| grep 8021q` | `modprobe 8021q` |
| Works in one subnet only | Missing inter-VLAN router | `ip route` | Add L3 hop (next tutorial) |

## Summary

- Ethernet delivers frames using **MAC** addresses inside a **broadcast domain**.  
- **Switches** learn, forward, and flood; hubs are obsolete.  
- **VLANs** split one fabric into isolated segments; **access** vs **trunk** defines tagging.  
- **ARP/neighbour** resolution binds IP to MAC for on-link delivery.  
- Cloud and containers virtualise the same Layer 2 jobs with bridges, ENIs, and subnets.

## Interview Questions

1. How does **Ethernet, Switching, and VLANs** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - Continue with [ICMP, ARP, DHCP, and Network Services](icmp-arp-dhcp-and-network-services.md) — neighbour resolution and host network services.

## References

- [IEEE 802.3 Ethernet overview](https://www.ieee802.org/3/)  
- [RFC 826 – ARP](https://www.rfc-editor.org/rfc/rfc826)  
- [VLAN (802.1Q) overview](https://en.wikipedia.org/wiki/IEEE_802.1Q)  
- [ip-link(8)](https://man7.org/linux/man-pages/man8/ip-link.8.html)
