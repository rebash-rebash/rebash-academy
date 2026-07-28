---
title: Ethernet, Switching, and VLANs
description: Understand MAC addresses, Ethernet frames, switch operation, VLAN segmentation, trunk and access ports, and ARP resolution on Linux.
difficulty: beginner
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: networking
tags:
  - networking
  - ethernet
  - switching
  - vlan
  - arp
  - mac-address
prerequisites:
  - IP Addressing and Subnetting (Tutorial 3)
  - OSI and TCP/IP Models (Tutorial 2)
  - Linux CLI familiarity
comments: false
---

# Ethernet, Switching, and VLANs

## Overview

Before IP packets can cross the Internet, they travel as **Ethernet frames** on local networks. **Switches** forward these frames using **MAC addresses**, and **VLANs** logically segment a physical switch into multiple isolated broadcast domains. Every cloud VPC subnet, Docker bridge, and Kubernetes node network relies on these Layer 2 concepts — even when you never touch a physical switch.

This tutorial covers Ethernet framing, how switches differ from obsolete hubs, **VLAN** design with trunk and access ports, and a preview of **ARP** (Address Resolution Protocol) that maps IP addresses to MAC addresses. Mastering Layer 2 explains why hosts on the same subnet communicate directly, why misconfigured VLANs cause "host unreachable" errors, and how container networking bridges work under the hood.

This is **Tutorial 4** in **Module 2: Data Link & Routing** of the REBASH Academy Networking series. Complete [IP Addressing and Subnetting](ip-addressing-and-subnetting.md) first.

## Prerequisites

- [IP Addressing and Subnetting](ip-addressing-and-subnetting.md) — CIDR, subnet masks, and same-subnet vs remote delivery
- [OSI and TCP/IP Models](osi-and-tcp-ip-models.md) — Layer 2 vs Layer 3 distinction
- Linux lab environment with at least one Ethernet interface
- Optional: `sudo` access for VLAN creation and packet capture

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the structure of an Ethernet frame and the role of source/destination MAC addresses
- [ ] Describe how a switch learns MAC addresses and forwards frames selectively
- [ ] Compare switches and hubs and explain why hubs are obsolete
- [ ] Define VLANs and explain why segmentation improves security and performance
- [ ] Distinguish access ports (single VLAN) from trunk ports (multiple VLANs with 802.1Q tags)
- [ ] Inspect MAC addresses and the ARP/neighbor table on Linux
- [ ] Create a VLAN sub-interface on Linux for hands-on practice
- [ ] Relate Layer 2 concepts to Docker bridge networks and cloud virtual switches

## Architecture

```d2
direction: down

VLAN10: "VLAN 10 — Web (10.0.1.0/24)" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        S1: "Server A\nMAC aa:bb:cc:01"
        S2: "Server B\nMAC aa:bb:cc:02"
    }
    VLAN20: "VLAN 20 — DB (10.0.20.0/24)" {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        S3: "DB Server\nMAC ee:ff:00:01"
    }
    SW: "Managed Switch\n802.1Q trunk to router"
    RTR: "L3 Switch / Router\nInter-VLAN routing"
    VLAN10.S1 -> SW
    VLAN10.S2 -> SW
    VLAN20.S3 -> SW
    SW -> RTR: "trunk: VLAN 10, 20"
```

Traffic within VLAN 10 stays on the same broadcast domain. Cross-VLAN communication requires Layer 3 routing through the router.

## Theory

### MAC Addresses

A **MAC (Media Access Control) address** is a 48-bit identifier assigned to each network interface, written as six hexadecimal octets: `00:1a:2b:3c:4d:5e`.

| Property | MAC Address | IP Address |
|----------|-------------|------------|
| OSI Layer | 2 (Data Link) | 3 (Network) |
| Scope | Local segment only | End-to-end (typically) |
| Assigned by | Manufacturer (OUI) + optional override | Administrator or DHCP |
| Changes per hop | Yes — rewritten at each router | No — source/dest usually unchanged |
| Format | 48-bit hex (6 octets) | 32-bit IPv4 or 128-bit IPv6 |

The first three octets (**OUI — Organizationally Unique Identifier**) identify the vendor. Cloud hypervisors assign virtual MACs to VM ENIs. Docker and Kubernetes create virtual MACs on **veth** pairs and bridge interfaces.

**Locally administered addresses** (second-least bit of first octet set to 1) appear in virtualized environments — do not assume all MACs are hardware-burned.

### Ethernet Frame Structure

The dominant **Ethernet II (DIX)** frame layout:

```text
| Preamble | Dest MAC (6) | Src MAC (6) | EtherType (2) | Payload (46–1500) | FCS (4) |
```

| Field | Purpose |
|-------|---------|
| **Destination MAC** | Next-hop Layer 2 address (final host or gateway) |
| **Source MAC** | Sending interface's MAC |
| **EtherType** | Protocol in payload — `0x0800` = IPv4, `0x86DD` = IPv6, `0x8100` = 802.1Q VLAN tag |
| **Payload** | IP packet (typically) |
| **FCS** | Frame Check Sequence — CRC error detection |

**MTU (Maximum Transmission Unit)** for standard Ethernet is **1500 bytes** payload. Jumbo frames (9000 bytes) appear in data center storage networks — mismatched MTU causes fragmentation or black holes.

### How Switches Forward Frames

A **switch** maintains a **MAC address table** (CAM table) mapping MAC → port:

1. **Learning:** When a frame arrives, the switch records source MAC and ingress port
2. **Forwarding:** For unicast dest MAC, forward only to the known port
3. **Flooding:** Unknown unicast, broadcast (`ff:ff:ff:ff:ff:ff`), and multicast flood to all ports in the VLAN
4. **Aging:** Entries expire after inactivity (default 300 seconds on many switches)

This eliminates the collision problems of legacy **hubs**, which repeated every frame to every port.

| Device | Layer | Behaviour | Status |
|--------|-------|----------|--------|
| **Hub** | 1 | Repeats to all ports — single collision domain | Obsolete |
| **Switch** | 2 | Forwards by destination MAC — per-port collision domain | Standard |
| **Router** | 3 | Routes by IP between networks | L3 boundary |

### VLANs — Virtual LANs

A **VLAN** logically partitions one physical switch into multiple isolated broadcast domains. Frames tagged with **VLAN ID** (1–4094) stay within their VLAN unless routed at Layer 3.

Benefits:

- **Security isolation** — DB servers cannot ARP web servers directly
- **Broadcast containment** — ARP storms and DHCP broadcasts stay local
- **Operational flexibility** — reassign VLAN by config, not rewiring
- **Compliance** — separate PCI, management, and production traffic

**802.1Q** inserts a 4-byte VLAN tag into frames on **trunk** links:

| Port Type | VLAN Tagging | Typical Use |
|-----------|--------------|-------------|
| **Access** | Untagged — single VLAN assigned to port | Server, workstation, AP |
| **Trunk** | Tagged — carries multiple VLANs | Switch-to-switch, switch-to-router |
| **Native VLAN** | Untagged traffic on trunk — must match both ends | Legacy compatibility — document carefully |

!!! warning "Native VLAN mismatch"
    If switch A sends untagged traffic as VLAN 10 and switch B expects native VLAN 1, traffic leaks or is dropped silently. Always match native VLAN on both trunk ends.

### Spanning Tree Protocol (STP) — Brief Overview

Redundant switch links create **loops** — frames circulate forever, saturating bandwidth. **STP (802.1D)** and **RSTP** block redundant paths while maintaining failover. Cloud virtual networks handle this internally; on-premises switch misconfiguration (disabled STP + loop) causes total LAN outages.

### ARP — Address Resolution Protocol

Hosts on the same subnet deliver IP packets by encapsulating them in Ethernet frames destined for the target's **MAC address**. **ARP** resolves IP → MAC via broadcast:

```text
Who has 10.0.1.1? Tell 10.0.1.42
```

The kernel caches results in the **neighbor table** (`ip neigh`). ARP only works within a **broadcast domain** (same VLAN/subnet). Remote subnets use the **default gateway's MAC**, not the final destination's MAC.

See [ICMP, ARP, DHCP, and Network Services](icmp-arp-dhcp-and-network-services.md) for full ARP, gratuitous ARP, and proxy ARP coverage.

### Layer 2 in Cloud and Containers

| Environment | Layer 2 Equivalent |
|-------------|------------------|
| **AWS VPC** | Virtual switch per AZ; ENIs with MAC addresses |
| **Docker bridge** | `docker0` bridge, veth pairs, MAC per container |
| **Kubernetes** | CNI plugin creates pod veth + bridge/overlay |
| **VMware/Hyper-V** | Virtual switch with port groups (VLAN analog) |

You rarely configure physical VLANs in pure cloud SaaS, but understanding MAC learning and broadcast domains explains Docker network isolation and why security groups operate at L3/L4 while switches operate at L2.

## Hands-on Lab

Complete these steps on a Linux host. VLAN creation requires root.

### Step 1 – Inspect interface MAC addresses

**Command:**

```bash
ip link show
ip link show eth0 2>/dev/null || ip link show $(ip route | awk '/default/ {print $5; exit}')
```

**Explanation:** Each interface has a `link/ether` MAC address. `state UP` means the interface is active.

**Expected output:**

```text
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff
```

### Step 2 – View and populate ARP/neighbor table

**Command:**

```bash
ip neigh show
GW=$(ip route | awk '/default/ {print $3; exit}')
ping -c 2 "$GW"
ip neigh show "$GW"
```

**Explanation:** ARP cache maps IP to MAC. After ping, gateway entry shows `REACHABLE` or `STALE`.

**Expected output:**

```text
10.0.0.1 dev eth0 lladdr 00:11:22:33:44:55 REACHABLE
```

### Step 3 – Calculate broadcast address

**Command:**

```bash
ip -4 addr show scope global | awk '/inet/ {print $2; exit}' | while read cidr; do
  python3 -c "
import ipaddress
net = ipaddress.ip_interface('$cidr').network
print(f'Subnet:   {net}')
print(f'Network:  {net.network_address}')
print(f'Broadcast:{net.broadcast_address}')
"
done
```

**Explanation:** All hosts in the same subnet share a broadcast domain — frames to broadcast MAC reach all members.

### Step 4 – Monitor ARP traffic

**Command:**

```bash
sudo timeout 10 tcpdump -i any arp -nn -c 5 2>/dev/null &
sleep 1
ping -c 2 8.8.8.8 >/dev/null 2>&1
wait
```

**Explanation:** ARP requests broadcast "who has X?" on the local segment. Requires sudo for packet capture.

**Expected output:**

```text
ARP, Request who-has 10.0.0.1 tell 10.0.0.42
ARP, Reply 10.0.0.1 is-at 00:11:22:33:44:55
```

### Step 5 – Create VLAN sub-interface (lab)

**Command:**

```bash
IFACE=$(ip route | awk '/default/ {print $5; exit}')
sudo ip link add link "$IFACE" name "${IFACE}.100" type vlan id 100
ip link show "${IFACE}.100"
sudo ip link del "${IFACE}.100" 2>/dev/null
```

**Explanation:** Linux supports 802.1Q VLAN sub-interfaces. Production configs persist in netplan or NetworkManager. Remove after lab.

**Expected output:**

```text
3: eth0.100@eth0: <BROADCAST,MULTICAST> mtu 1500
```

### Step 6 – Inspect bridge (Docker/Kubernetes nodes)

**Command:**

```bash
bridge link 2>/dev/null | head -10 || ip link show type bridge 2>/dev/null
docker network ls 2>/dev/null | head -5 || echo "(Docker not installed — skip)"
```

**Explanation:** Bridges connect virtual interfaces at Layer 2 — same MAC learning behaviour as physical switches.

### Step 7 – Document three-tier VLAN design

Create a table for a sample application:

| VLAN ID | Name | Subnet | Attached Devices |
|---------|------|--------|------------------|
| 10 | web | 10.0.1.0/24 | Load balancer, nginx |
| 20 | app | 10.0.10.0/24 | API servers |
| 30 | db | 10.0.20.0/24 | PostgreSQL cluster |
| 99 | mgmt | 10.0.99.0/24 | Bastion, switch admin |

Inter-VLAN traffic flows only through the firewall/router — no direct L2 path between web and db.

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

| Command | Description | Example |
|---------|-------------|---------|
| `ip link show` | Interface MAC and state | `ip link show eth0` |
| `ip neigh show` | ARP/neighbor cache | `ip neigh show` |
| `ip neigh del` | Remove stale ARP entry | `sudo ip neigh del 10.0.0.5 dev eth0` |
| `ip link add type vlan` | Create VLAN sub-interface | `sudo ip link add link eth0 name eth0.10 type vlan id 10` |
| `bridge link` | Show bridge port mappings | `bridge link` |
| `tcpdump arp` | Capture ARP traffic | `sudo tcpdump -i eth0 arp -nn` |
| `cat /sys/class/net/*/address` | List all interface MACs | Quick MAC audit |

### MAC and neighbor audit script

```bash
#!/usr/bin/env bash
# l2-audit.sh — Layer 2 interface and neighbor summary
set -euo pipefail

echo "=== Interface MAC Addresses ==="
ip -br link show

echo ""
echo "=== Neighbor Table (ARP cache) ==="
ip neigh show | head -20

echo ""
echo "=== Default Gateway ==="
ip route show default
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Native VLAN mismatch on trunks"
    Mismatched native VLAN between switches causes subtle leaks or black-holed traffic. Always match both ends and document in network diagrams.

!!! warning "Assuming VLAN equals subnet automatically"
    One VLAN typically maps to one IP subnet, but L3 switches can host multiple subnets per VLAN. Document your design explicitly.

!!! warning "Ignoring MAC flapping alerts"
    Duplicate MACs on two ports cause unstable connectivity — common after VM clone, misconfigured NIC teaming, or container MAC collision.

!!! warning "Disabling STP with redundant links"
    Creates broadcast storms that take down entire LAN segments. Only disable STP with absolute certainty of loop-free topology.

!!! warning "VLAN 1 default on access ports"
    Leaving servers on default VLAN 1 exposes them to management broadcast traffic. Assign explicit VLANs per tier.

## Best Practices

!!! tip "Separate management VLAN"
    Out-of-band management (IPMI, iDRAC, switch admin) on dedicated VLAN — never exposed to application traffic.

!!! tip "Document VLAN-to-subnet mapping in IaC"
    Include in Terraform, network diagrams, and runbooks — prevents routing errors during incidents.

!!! tip "Use /30 or /31 for point-to-point router links"
    Conserves IP space on router-to-router connections. See [IP Addressing and Subnetting](ip-addressing-and-subnetting.md).

!!! tip "Monitor CAM table utilization on physical switches"
    MAC table overflow causes flooding — rare but catastrophic on large flat networks.

!!! tip "Match MTU end-to-end for storage and overlay networks"
    Jumbo frames or VXLAN overlays need consistent MTU — mismatches cause silent TCP hangs.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Host unreachable on same subnet | ARP failure, wrong VLAN | `ip neigh`; verify switch port VLAN assignment |
| Intermittent connectivity | MAC flapping, STP loop | Check switch logs; disable unused ports; verify STP |
| Can ping gateway, not remote VLAN | Missing inter-VLAN route | Configure L3 switch or router; check firewall rules |
| Duplicate MAC warnings | VM clone, bonding misconfig | Assign unique MAC; fix NIC teaming config |
| Container cannot reach host | Bridge/isolation misconfig | Inspect `docker network inspect`; verify iptables FORWARD |
| VLAN tag visible but no connectivity | Wrong VLAN ID on access port | Match VLAN ID on switch port to host subnet |
| ARP entry INCOMPLETE | Target down or wrong subnet | Verify IP on same subnet; check target host UP |
| High broadcast traffic | Storm, loop, or misconfigured device | Enable STP; identify source with `tcpdump`; isolate port |

## Summary

- **MAC addresses** identify devices on a local Layer 2 segment; **IP addresses** identify endpoints at Layer 3
- **Switches** learn MAC → port mappings and forward unicast frames selectively; hubs are obsolete
- **VLANs** segment broadcast domains using 802.1Q tags on trunks and single VLANs on access ports
- **ARP** resolves IP to MAC within a subnet — prerequisite for local Ethernet delivery
- **Native VLAN** and **trunk** configuration must match on both ends to avoid leaks
- Cloud and container networking emulate Layer 2 with virtual switches, bridges, and ENIs
- Use **`ip link`** and **`ip neigh`** as primary Linux Layer 2 diagnostic tools

## Interview Questions

1. What is the difference between a MAC address and an IP address?
2. How does a switch learn where to forward frames?
3. What problem do VLANs solve?
4. What is an 802.1Q trunk port vs an access port?
5. What is a broadcast domain?
6. Why is a hub inferior to a switch?
7. What happens when a switch receives a frame with an unknown destination MAC?
8. How does ARP relate to Ethernet?
9. What is the native VLAN and why does mismatch cause problems?
10. What is MAC flapping and what causes it?

??? tip "Sample Answers (Questions 1, 3, and 7)"

    **Q1 — MAC vs IP:** MAC is a Layer 2 hardware identifier scoped to the local segment — changed at each router hop. IP is a Layer 3 logical address used end-to-end for routing. ARP bridges the two on local subnets.

    **Q3 — VLAN purpose:** VLANs logically separate broadcast domains on one physical switch. They improve security (isolate tiers), contain broadcast traffic (ARP, DHCP), and simplify network changes without rewiring.

    **Q7 — Unknown destination MAC:** The switch floods the frame to all ports in the same VLAN except the ingress port. When the destination responds, the switch learns its MAC → port mapping for future unicast forwarding.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [IP Addressing and Subnetting](ip-addressing-and-subnetting.md) *(Module 1)*
- [Routing Fundamentals](routing-fundamentals.md) *(next)*
- [ICMP, ARP, DHCP, and Network Services](icmp-arp-dhcp-and-network-services.md)
- [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)
- Cheat sheet: [Networking Cheat Sheet](../cheatsheets/networking.md)
- Interview prep: [Networking Interview Prep](../interview/networking.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [IEEE 802.1Q — VLAN Tagging](https://standards.ieee.org/standard/802_1Q-2018.html)
- [IEEE 802.3 — Ethernet](https://standards.ieee.org/standard/802_3-2022.html)
- [Wireshark — Ethernet](https://wiki.wireshark.org/Ethernet)
- [Linux VLAN documentation](https://www.kernel.org/doc/Documentation/networking/vlan.txt)
- [REBASH Academy – Networking Overview](index.md)
