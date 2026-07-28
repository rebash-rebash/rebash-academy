---
title: IP Addressing and Subnetting
description: Master IPv4 addressing, CIDR notation, subnet masks, public and private RFC 1918 ranges, subnet calculations, and VLSM for cloud and on-premises design.
difficulty: beginner
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: networking
tags:
  - networking
  - ipv4
  - cidr
  - subnetting
  - rfc1918
prerequisites:
  - Introduction to Networking (Tutorial 1)
  - OSI and TCP/IP Models (Tutorial 2)
  - Basic binary and decimal conversion (powers of 2)
comments: false
---

# IP Addressing and Subnetting

## Overview

Every device on an IP network needs a unique address. Get addressing wrong and you get duplicate IPs, routing black holes, or exhausted subnets that block scaling. **IPv4 addressing** and **subnetting** are the arithmetic backbone of infrastructure design — from carving a `/16` VPC into application tiers to planning Kubernetes pod CIDRs that do not overlap with your corporate network.

This tutorial covers IPv4 structure, **CIDR notation**, **subnet masks**, **public vs private** address space (RFC 1918), manual subnet calculation, **VLSM** (Variable Length Subnet Masking), and hands-on practice with `ipcalc` and Linux networking commands. These skills appear in every cloud certification, Terraform module, and network design review.

This is **Tutorial 3** in **Module 1: Foundations** of the REBASH Academy Networking series. Complete [OSI and TCP/IP Models](osi-and-tcp-ip-models.md) first.

## Prerequisites

- [Introduction to Networking](introduction-to-networking.md) and [OSI and TCP/IP Models](osi-and-tcp-ip-models.md)
- Ability to convert between binary and decimal (or willingness to learn during this tutorial)
- Linux lab environment; install `ipcalc` if not present: `sudo apt install ipcalc` (Debian/Ubuntu) or `sudo dnf install ipcalc` (RHEL/Fedora)
- Optional: paper and pencil for manual calculation practice

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Describe IPv4 address structure (32 bits, dotted decimal, network vs host portions)
- [ ] Read and write CIDR notation and convert to subnet masks
- [ ] Identify RFC 1918 private ranges and explain when public addresses are required
- [ ] Calculate network address, broadcast address, and usable host range for any subnet
- [ ] Apply VLSM to divide a larger block into smaller subnets efficiently
- [ ] Use `ipcalc` and Linux `ip` commands to verify subnet calculations
- [ ] Avoid common cloud design mistakes like overlapping CIDR blocks
- [ ] Plan subnet sizes for typical DevOps tiers (web, app, database, management)

## Architecture

This topic is primarily procedural. The mental model is a straight line from inputs (commands, config files, or manifests) to observable system state — verify each change with the validation steps later in this tutorial.

## Theory

### IPv4 Address Structure

An **IPv4 address** is a 32-bit number, typically written as four decimal octets separated by dots (**dotted decimal**):

```text
192.168.10.50  =  11000000.10101000.00001010.00110010
```

Each octet ranges from 0 to 255 (8 bits). Total address space: 2³² = **4,294,967,296** addresses — far fewer than the number of devices on Earth, which is why NAT, IPv6, and private addressing exist.

Every IP address has two logical parts:

| Part | Determined By | Purpose |
|------|---------------|---------|
| **Network portion** | Subnet mask / prefix length | Identifies which network (subnet) the host belongs to |
| **Host portion** | Remaining bits | Identifies the specific device within that network |

### Subnet Masks and CIDR Notation

A **subnet mask** is a 32-bit value where network bits are `1` and host bits are `0`:

```text
255.255.255.0  =  11111111.11111111.11111111.00000000  =  /24
```

**CIDR notation** (Classless Inter-Domain Routing) appends a slash and the number of network bits:

| CIDR | Subnet Mask | Total Addresses | Usable Hosts |
|------|-------------|-----------------|--------------|
| /32 | 255.255.255.255 | 1 | 1 (single host) |
| /30 | 255.255.255.252 | 4 | 2 (point-to-point links) |
| /29 | 255.255.255.248 | 8 | 6 |
| /28 | 255.255.255.240 | 16 | 14 |
| /27 | 255.255.255.224 | 32 | 30 |
| /26 | 255.255.255.192 | 64 | 62 |
| /25 | 255.255.255.128 | 128 | 126 |
| /24 | 255.255.255.0 | 256 | 254 |
| /23 | 255.255.255.0 | 512 | 510 |
| /22 | 255.255.252.0 | 1,024 | 1,022 |
| /20 | 255.255.240.0 | 4,096 | 4,094 |
| /16 | 255.255.0.0 | 65,536 | 65,534 |
| /8 | 255.0.0.0 | 16,777,216 | 16,777,214 |

**Usable hosts** = total addresses − 2 (network address and broadcast address are reserved).

Quick formula: **usable hosts = 2^(32 − prefix) − 2**

Exception: `/31` (RFC 3021) uses both addresses for point-to-point links; `/32` is a single-host route.

### Calculating a Subnet Manually

Given **192.168.10.50/26**, find the network address, broadcast, and usable range.

**Step 1 — Prefix /26 means 26 network bits, 6 host bits.**

**Step 2 — Calculate block size:** 2^6 = 64 addresses per subnet.

**Step 3 — Find which block .50 falls into:**
Multiples of 64 in the third octet context: ...0, 64, 128, 192. Since 50 < 64, the network is **192.168.10.0/26**.

| Property | Value |
|----------|-------|
| Network address | 192.168.10.0 |
| First usable host | 192.168.10.1 |
| Last usable host | 192.168.10.62 |
| Broadcast address | 192.168.10.63 |
| Next subnet starts | 192.168.10.64 |

**Verification with binary (last octet):**

```text
  50 = 00110010
mask   11000000  (/26 → first 2 bits of octet are network)
net    00000000  = 0  → network 192.168.10.0
bcast  00111111  = 63 → broadcast 192.168.10.63
```

### Public vs Private Address Space (RFC 1918)

Not all IPv4 addresses are routable on the public Internet. **RFC 1918** defines three private ranges reserved for internal use:

| Range | CIDR | Typical Use |
|-------|------|-------------|
| 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 | Large enterprise, AWS VPC default |
| 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 | Docker default bridge, some cloud VPCs |
| 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 | Home networks, office LANs, lab environments |

Private addresses are **not globally unique** and **not routable on the Internet**. NAT (Network Address Translation) translates private IPs to public IPs for outbound traffic — covered in Tutorial 17.

**Special ranges to know:**

| Range | Purpose |
|-------|---------|
| 127.0.0.0/8 | Loopback (127.0.0.1 = localhost) |
| 169.254.0.0/16 | Link-local (APIPA — no DHCP) |
| 224.0.0.0/4 | Multicast |
| 0.0.0.0/8 | "This" network (legacy) |

### VLSM — Variable Length Subnet Masking

**VLSM** allows subnets of different sizes within the same address block — essential for efficient IP allocation. Instead of dividing a /24 into equal /26s, you assign larger subnets where needed and smaller ones where few hosts exist.

**Example:** Divide **10.0.0.0/22** (1,024 addresses) for a three-tier app:

| Subnet | CIDR | Usable Hosts | Purpose |
|--------|------|--------------|---------|
| 10.0.0.0/24 | 254 | Web tier (autoscaling) |
| 10.0.1.0/25 | 126 | App tier |
| 10.0.1.128/26 | 62 | Database tier |
| 10.0.1.192/27 | 30 | Management / bastion |
| 10.0.1.224/28 | 14 | Reserved / future |
| 10.0.2.0/24 – 10.0.3.0/24 | 508 | Remaining space for expansion |

Always allocate from the **top of the block downward** or use a structured scheme to avoid overlap. Document every allocation in your IP Address Management (IPAM) spreadsheet or tool.

### Cloud and DevOps Subnet Planning

When designing VPCs or Kubernetes clusters:

- **Never overlap CIDRs** between VPCs connected by peering, VPN, or Transit Gateway — routing cannot disambiguate
- **Reserve space for growth** — AWS recommends at least /16 per VPC; use /24 or smaller per subnet
- **Account for cloud overhead** — AWS reserves 5 IPs per subnet (network, router, DNS, future, broadcast)
- **Plan pod and service CIDRs** — Kubernetes needs separate ranges for nodes, pods, and services that do not overlap with VPC or on-prem
- **Use consistent naming** — `10.0.10.0/24-prod-web-us-east-1a` in tags and documentation

## Hands-on Lab

### Step 1 – Install and use ipcalc

**Command:**

```bash
# Install if needed
which ipcalc || sudo apt install -y ipcalc 2>/dev/null || sudo dnf install -y ipcalc

ipcalc 192.168.10.50/26
```

**Explanation:** `ipcalc` computes network, broadcast, host range, and wildcard mask instantly. Use it to verify manual calculations.

**Expected output:**

```text
Address:   192.168.10.50          11000000.10101000.00001010.00110010
Netmask:   255.255.255.192 = 26   11111111.11111111.11111111.11000000
Wildcard:  0.0.0.63               00000000.00000000.00000000.00111111
=>
Network:   192.168.10.0/26        11000000.10101000.00001010.00000000
HostMin:   192.168.10.1           11000000.10101000.00001010.00000001
HostMax:   192.168.10.62          11000000.10101000.00001010.00111110
Broadcast: 192.168.10.63          11000000.10101000.00001010.00111111
Hosts/Net: 62                     Class C, Private Internet
```

### Step 2 – Split a /24 into four /26 subnets

**Command:**

```bash
ipcalc 10.0.1.0/24 --split 4
```

**Explanation:** Divides a /24 into 4 equal subnets. Each /26 provides 62 usable hosts.

**Expected output:**

```text
Network:   10.0.1.0/26
Network:   10.0.1.64/26
Network:   10.0.1.128/26
Network:   10.0.1.192/26
```

### Step 3 – VLSM allocation with ipcalc

**Command:**

```bash
echo "=== Web tier: 200 hosts needed → /24 ==="
ipcalc 10.0.0.0/24 | grep -E "Network|HostMin|HostMax|Hosts"

echo "=== DB tier: 30 hosts needed → /27 ==="
ipcalc 10.0.1.0/27 | grep -E "Network|HostMin|HostMax|Hosts"

echo "=== Mgmt tier: 10 hosts needed → /28 ==="
ipcalc 10.0.1.16/28 | grep -E "Network|HostMin|HostMax|Hosts"
```

**Explanation:** Demonstrates VLSM — different prefix lengths for different tier requirements. A /24 gives 254 hosts for web; /27 gives 30 for database; /28 gives 14 for management.

### Step 4 – Inspect your system's IP and subnet

**Command:**

```bash
ip -br addr show
ip route show
```

**Explanation:** Identify your lab machine's IP address and prefix length. The route table shows which destinations are considered "directly connected" (same subnet).

**Expected output:**

```text
eth0             UP             10.0.1.42/24 metric 100 ...
10.0.1.0/24 dev eth0 proto kernel scope link src 10.0.1.42
default via 10.0.1.1 dev eth0
```

The `10.0.1.0/24 dev eth0` route means any IP in 10.0.1.0–10.0.1.255 is reached directly on eth0 (Layer 2 ARP, no gateway).

### Step 5 – Test same-subnet vs remote-subnet logic

**Command:**

```bash
MY_IP=$(ip -4 route get 1.1.1.1 | awk '{print $7; exit}')
MY_DEV=$(ip -4 route get 1.1.1.1 | awk '{print $5; exit}')

echo "My IP: $MY_IP on $MY_DEV"
echo "--- Same subnet (direct) ---"
ip route get "$(echo "$MY_IP" | sed 's/\.[0-9]*$/.1/')" 2>/dev/null
echo "--- Remote (via gateway) ---"
ip route get 8.8.8.8
```

**Explanation:** `ip route get` shows whether traffic goes direct (same subnet, `dev eth0`) or via a gateway (`via 10.0.1.1`). This is the kernel's subnet mask logic in action.

### Step 6 – Manual calculation practice

**Command:**

```bash
# Verify your manual work with ipcalc
ipcalc 172.16.45.200/21
```

**Task (do on paper first):**

Given **172.16.45.200/21**:

1. Block size = 2^(32−21) = 2^11 = 2048 addresses
2. Third octet block boundaries step by 8 (256/8=32... actually for /21, network bits span into third octet: 21-16=5 host bits in third octet, block = 2^5 = 32 in third octet)
3. Multiples of 32 in third octet: 0, 32, 64 — 45 falls in 32–63 block
4. Network: **172.16.32.0/21**, Broadcast: **172.16.63.255**

**Expected ipcalc output:**

```text
Network:   172.16.32.0/21
HostMin:   172.16.32.1
HostMax:   172.16.63.254
Broadcast: 172.16.63.255
Hosts/Net: 2046
```

### Step 7 – Identify private vs public addresses

**Command:**

```bash
for ip in 10.0.0.1 172.16.5.10 192.168.1.1 8.8.8.8 93.184.216.34; do
  result=$(ipcalc "$ip" 2>/dev/null | grep -oP 'Private|Public' || echo "unknown")
  echo "$ip → $result"
done
```

**Explanation:** Quickly classify addresses. Only RFC 1918 ranges are private; everything else is public (or special-use).

**Expected output:**

```text
10.0.0.1 → Private
172.16.5.10 → Private
192.168.1.1 → Private
8.8.8.8 → Public
93.184.216.34 → Public
```

### Step 8 – Plan a mini VPC on paper and validate

**Command:**

```bash
cat << 'EOF' | while read cidr purpose; do
10.0.0.0/24 public-subnet-az-a
10.0.1.0/24 private-app-az-a
10.0.2.0/24 private-db-az-a
10.0.10.0/24 public-subnet-az-b
EOF
  net=$(ipcalc "$cidr" 2>/dev/null | awk -F: '/Network/{print $2}' | tr -d ' ')
  hosts=$(ipcalc "$cidr" 2>/dev/null | awk -F: '/Hosts\/Net/{print $2}' | tr -d ' ')
  printf "%-22s %-28s %s hosts\n" "$cidr" "$purpose" "$hosts"
done
```

**Explanation:** Validates a simple dual-AZ VPC design with non-overlapping /24 subnets inside a /16 VPC block.

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
| `ipcalc CIDR` | Full subnet calculation | `ipcalc 10.0.0.0/24` |
| `ipcalc --split N` | Split network into N equal parts | `ipcalc 10.0.0.0/22 --split 4` |
| `ip -br addr` | Show IP with prefix length | `ip -br addr show eth0` |
| `ip route get IP` | Show route for destination | `ip route get 10.0.2.5` |
| `ipcalc -b` | Brief output mode | `ipcalc -b 192.168.1.0/24` |

### Subnet planning helper script

```bash
#!/usr/bin/env bash
# subnet-plan.sh — validate a list of CIDRs for overlaps
set -euo pipefail

CIDRS=("$@")
if [ "$#" -lt 1 ]; then
  echo "Usage: subnet-plan.sh 10.0.0.0/24 10.0.1.0/24 ..."
  exit 1
fi

echo "Subnet Plan"
echo "==========="
for cidr in "${CIDRS[@]}"; do
  ipcalc -b "$cidr" 2>/dev/null || { echo "Invalid: $cidr"; exit 1; }
done

echo ""
echo "Checking for overlaps..."
python3 - << 'PY' "${CIDRS[@]}"
import sys, ipaddress
nets = [ipaddress.ip_network(c, strict=False) for c in sys.argv[1:]]
for i, a in enumerate(nets):
    for j, b in enumerate(nets):
        if i < j and a.overlaps(b):
            print(f"OVERLAP: {a} and {b}")
            sys.exit(1)
print("No overlaps detected.")
PY
```

Usage: `chmod +x subnet-plan.sh && ./subnet-plan.sh 10.0.0.0/24 10.0.1.0/24 10.0.2.0/24`

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Using the network or broadcast address as a host IP"
    In 192.168.1.0/24, addresses `.0` (network) and `.255` (broadcast) are reserved. Assigning `.0` or `.255` to a host causes connectivity failures that are painful to diagnose.

!!! warning "Overlapping CIDR blocks between connected networks"
    VPC peering between 10.0.0.0/16 and 10.0.0.0/16 in another account with overlapping subnets causes routing conflicts. Always coordinate IPAM before connecting networks.

!!! warning "Choosing subnets too small for autoscaling"
    A /28 (14 hosts) works for a database pair but fails for a Kubernetes node group that scales to 50. AWS also consumes 5 IPs per subnet before you assign any.

!!! warning "Confusing subnet mask with wildcard mask"
    Subnet mask: network bits = 1. Wildcard mask (used in ACLs): network bits = 0. They are inverses. `255.255.255.0` mask = `0.0.0.255` wildcard.

## Best Practices

!!! tip "Standardize on /16 VPCs with /24 subnets in cloud"
    AWS, GCP, and Azure all support this pattern. Use /24 per subnet per AZ for simplicity; grow with additional subnets rather than resizing existing ones.

!!! tip "Maintain an IPAM document from day one"
    Track every CIDR allocation: owner, environment, region, AZ, and purpose. Future you will thank present you when connecting VPN or adding a new region.

!!! tip "Verify calculations with ipcalc, learn manual method for interviews"
    In production, use tools. In interviews, you must calculate /26 host ranges on a whiteboard. Practice until block-size math is automatic.

!!! tip "Reserve 10.0.0.0/8 or 172.16.0.0/12 for cloud, 192.168.0.0/16 for offices"
    This convention reduces overlap risk when connecting on-premises (typically 192.168.x.x) to cloud (10.x.x.x).

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "Cannot assign requested address" | Host IP outside subnet or is network/broadcast | Verify IP is within HostMin–HostMax from `ipcalc` |
| Hosts on same subnet cannot communicate | Different VLAN, wrong mask, or switch issue | Confirm both use same /prefix; check `ip neigh` for ARP |
| Can reach local but not remote hosts | Wrong subnet mask (thinks remote is local) | Fix mask — host may ARP for non-local IPs instead of sending to gateway |
| Duplicate IP conflicts | DHCP overlap or manual misassignment | Scan with `arp-scan` or check DHCP pools; use static reservations |
| VPC peering connection fails | Overlapping CIDR ranges | Redesign one VPC's CIDR block before peering |
| Running out of IPs in subnet | Subnet too small or too many ENIs/pods | Add new larger subnet; migrate workloads; never "resize" in place |
| ipcalc not found | Package not installed | `apt install ipcalc` or `dnf install ipcalc` |

## Summary

- IPv4 addresses are **32 bits** written in dotted decimal; split into **network** and **host** portions by the subnet mask
- **CIDR notation** (/24, /26) defines how many bits belong to the network; usable hosts = 2^(32−prefix) − 2
- **RFC 1918** private ranges (10/8, 172.16/12, 192.168/16) are not Internet-routable; **NAT** provides outbound access
- **VLSM** allocates subnets of different sizes from one block for efficient tier-based design
- Use **ipcalc** to verify calculations; use **ip route get** to see how the kernel applies subnet logic
- Plan cloud subnets with growth, avoid CIDR overlap, and document everything in IPAM

## Interview Questions

1. How many usable host addresses are in a /26 subnet?
2. What are the three RFC 1918 private address ranges?
3. Given 10.0.5.130/25, what are the network address, broadcast, and usable range?
4. What is the difference between CIDR notation and a subnet mask?
5. Explain VLSM and when you would use it.
6. Why can't two hosts with private IP addresses communicate over the Internet directly?
7. How many addresses does AWS reserve in each subnet?
8. What happens if two VPCs with overlapping CIDRs are peered?
9. Convert subnet mask 255.255.240.0 to CIDR notation.
10. A subnet needs to support 100 hosts. What is the smallest prefix that works?

??? tip "Sample Answers (Questions 1, 3, and 10)"

    **Q1 — Usable hosts in /26:** A /26 has 32 − 26 = 6 host bits. Total addresses = 2^6 = 64. Usable = 64 − 2 = **62 hosts** (excluding network and broadcast addresses).

    **Q3 — 10.0.5.130/25:** /25 means 128 addresses per block (2^7). In the fourth octet, blocks are 0–127 and 128–255. Since 130 ≥ 128, network = **10.0.5.128/25**, broadcast = **10.0.5.255**, usable range = **10.0.5.129 – 10.0.5.254**.

    **Q10 — 100 hosts:** Need 2^h − 2 ≥ 100, so 2^h ≥ 102, h ≥ 7 (since 2^7 = 128). Total bits for hosts = 7, network bits = 32 − 7 = 25. Smallest prefix: **/25** (126 usable hosts). A /26 only provides 62 usable — not enough.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [OSI and TCP/IP Models](osi-and-tcp-ip-models.md) *(previous in Module 1)*
- [Ethernet, Switching, and VLANs](ethernet-switching-and-vlans.md) *(next — Module 2)*
- [Introduction to Linux](../linux/introduction-to-linux.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)
- Cheat sheet: [Networking Cheat Sheet](../cheatsheets/networking.md)
- Interview prep: [Networking Interview Prep](../interview/networking.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [RFC 1918 – Address Allocation for Private Internets](https://www.rfc-editor.org/rfc/rfc1918)
- [RFC 4632 – CIDR Address Strategy](https://www.rfc-editor.org/rfc/rfc4632)
- [RFC 3021 – /31 Prefix for Point-to-Point Links](https://www.rfc-editor.org/rfc/rfc3021)
- [ipcalc man page](https://linux.die.net/man/1/ipcalc)
- [AWS VPC CIDR Planning](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html)
- [REBASH Academy – Networking Overview](index.md)
