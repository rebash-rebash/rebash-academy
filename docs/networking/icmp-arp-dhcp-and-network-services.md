---
title: ICMP, ARP, DHCP, and Network Services
description: Master ICMP ping and traceroute, ARP neighbor resolution, the DHCP DORA process, and NTP time synchronization for production network operations.
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: networking
tags:
  - networking
  - icmp
  - arp
  - dhcp
  - ntp
  - ping
  - traceroute
prerequisites:
  - Complete Module 1 networking tutorials or equivalent IP addressing knowledge
  - Linux environment with network access and sudo privileges
  - Familiarity with ip route and basic connectivity testing
comments: false
---

# ICMP, ARP, DHCP, and Network Services

## Overview

Before TCP connections and HTTP requests succeed, hosts must discover neighbors on the local segment, obtain IP configuration, and verify reachability. **ICMP** provides diagnostic messaging, **ARP** maps IP addresses to MAC addresses on Layer 2, **DHCP** automates address assignment, and **NTP** keeps clocks synchronized — failures in any of these services produce symptoms that look like application bugs but are actually infrastructure problems.

This tutorial is **Tutorial 6** in **Module 2: Data Link & Routing** of the REBASH Academy Networking series. You will understand how these protocols work at the packet level, practice inspection with Linux tools, and build troubleshooting workflows used daily by DevOps and SRE teams. For OS-level command overlap, see [Linux Networking Essentials](../linux/linux-networking-essentials.md); here we go deeper on protocol behaviour and production implications.

## Prerequisites

- Complete [Routing Fundamentals](routing-fundamentals.md) or understand default gateways and subnet boundaries
- A Linux VM or cloud instance with outbound network access
- `sudo` privileges for DHCP client inspection and optional packet capture
- Basic comfort with `ip`, `ping`, and reading command output
- Optional: second host on the same L2 segment for ARP observation

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain ICMP message types and why ping/traceroute work (or fail)
- [ ] Read and interpret the ARP/neighbor cache with `ip neigh`
- [ ] Describe the DHCP DORA process and inspect lease files on Linux
- [ ] Configure and verify NTP synchronization with `timedatectl` and `chronyc`
- [ ] Diagnose "works by IP but not hostname" and "cannot reach gateway" scenarios
- [ ] Distinguish protocol-level failures from firewall blocks in production

## Architecture

The diagram below shows how a new host joins a network: DHCP assigns L3 config, ARP resolves the gateway MAC, ICMP verifies reachability, and NTP aligns time with authoritative servers.

```d2
shape: sequence_diagram

Host: Host
Switch: Switch
DHCP: "DHCP Server"
GW: "Default Gateway"
NTP: "NTP Server"
Host -> Switch: "DHCP Discover (broadcast)"
Switch -> DHCP: "Forward broadcast"
DHCP -> Host: "DHCP Offer (IP, mask, GW, DNS)"
Host -> DHCP: "DHCP Request (accept offer)"
DHCP -> Host: "DHCP ACK (lease time)"
Host -> Switch: "ARP Who-has GW IP?"
GW -> Host: "ARP Reply (MAC address)"
Host -> GW: "ICMP Echo Request (ping)"
GW -> Host: "ICMP Echo Reply"
Host -> NTP: "NTP client query (UDP 123)"
NTP -> Host: "Time sync response"
```

## Theory

### ICMP — Internet Control Message Protocol

ICMP operates at **Layer 3** (Network layer in OSI terms) and rides inside IP packets. It is not used for application data transfer — it carries **control and diagnostic messages** between hosts and routers.

| ICMP Type | Code (common) | Purpose |
|-----------|---------------|---------|
| 0 | 0 | Echo Reply (response to ping) |
| 3 | 0–15 | Destination Unreachable (network, host, port, etc.) |
| 8 | 0 | Echo Request (ping) |
| 11 | 0 | Time Exceeded (TTL expired — used by traceroute) |

**ping** sends ICMP Echo Request (type 8); the target responds with Echo Reply (type 0). Round-trip time (RTT) measures latency. Packet loss indicates congestion, filtering, or unreachable paths.

**traceroute** exploits TTL (Time To Live). Each hop decrements TTL; when it reaches zero, the router sends ICMP Time Exceeded back. By incrementing starting TTL, traceroute maps the path hop by hop. On Linux, `traceroute` may use UDP or ICMP depending on flags; `tracepath` uses UDP without requiring root.

!!! note "ICMP is often blocked in production"
    Cloud security groups, corporate firewalls, and load balancers frequently drop ICMP. A failed ping does **not** prove a host is down — always validate with TCP (`curl`, `nc`) when ICMP is filtered.

### ARP — Address Resolution Protocol

On Ethernet networks, frames require **MAC addresses** (Layer 2) even when applications use **IP addresses** (Layer 3). ARP resolves "Who has IP 10.0.0.1? Tell 10.0.0.42" via broadcast on the local segment.

The kernel maintains an **ARP cache** (neighbor table):

- **REACHABLE** — recent confirmation, entry trusted
- **STALE** — aged out but may still be valid until revalidated
- **FAILED** — resolution attempts failed (wrong VLAN, host down, proxy ARP issue)

ARP only works within a **broadcast domain** (same subnet/VLAN). Traffic to remote subnets goes to the **default gateway's MAC**, not the destination's MAC.

**Gratuitous ARP** announces a host's IP-to-MAC mapping without being asked — used after failover (VIP movement) or IP migration. Understanding gratuitous ARP explains why floating IPs work in HA clusters.

### DHCP — Dynamic Host Configuration Protocol

DHCP automates IP assignment. The classic **DORA** exchange:

1. **Discover** — Client broadcasts "I need configuration" (0.0.0.0 → 255.255.255.255)
2. **Offer** — Server proposes IP, subnet mask, gateway, DNS, lease time
3. **Request** — Client broadcasts "I accept this offer" (may inform other servers)
4. **Acknowledge** — Server confirms; client configures interface

| DHCP Option | Typical Value | Purpose |
|-------------|---------------|---------|
| Option 1 | Subnet mask | Defines local network boundary |
| Option 3 | Default router | Gateway for off-subnet traffic |
| Option 6 | DNS servers | Resolver addresses |
| Option 51 | Lease time | How long the IP assignment is valid |
| Option 15 | Domain name | DNS search suffix |

On cloud VMs, DHCP often delivers metadata endpoints (AWS `169.254.169.254`, GCP metadata server). Lease renewal happens at **T1 (50%)** and **T2 (87.5%)** of lease lifetime — understanding renewal prevents surprise address changes during long-running processes that cache IPs incorrectly.

Linux DHCP clients vary by distro: **systemd-networkd**, **NetworkManager**, or **dhclient**. Lease files may appear in `/var/lib/dhcp/` or via `journalctl` on networkd systems.

### NTP — Network Time Protocol

Accurate time is critical for TLS certificate validation, distributed log correlation, Kerberos authentication, and database replication. **NTP** synchronizes clocks to stratum-1/2 reference servers over **UDP port 123**.

| Stratum | Description |
|---------|-------------|
| 0 | Reference clock (GPS, atomic) — not on network |
| 1 | Directly attached to stratum 0 |
| 2–15 | Synchronized to lower stratum |
| 16 | Unsynchronized |

Modern Linux uses **chrony** (RHEL, Ubuntu) or **systemd-timesyncd** (minimal setups). Cloud instances typically sync to provider NTP pools automatically. Clock drift beyond a few seconds breaks JWT validation, SSL handshakes, and `etcd` consensus in Kubernetes.

## Hands-on Lab

Complete these steps on a Linux host. Commands are safe unless noted.

### Step 1 – ICMP ping with options

**Command:**

```bash
ping -c 4 -i 0.5 -W 2 8.8.8.8
ping -c 2 -M do -s 1472 8.8.8.8
```

**Explanation:** First command sends four echoes at 0.5s interval with 2s timeout. Second tests **MTU path** with "don't fragment" (`-M do`) and 1472-byte payload (1472 + 28 byte IP/ICMP header ≈ 1500 MTU).

**Expected output:**

```text
4 packets transmitted, 4 received, 0% packet loss, time 1501ms
rtt min/avg/max/mdev = 12.345/13.456/14.567/0.890 ms
```

If the large ping fails with "Frag needed", an intermediate hop has smaller MTU.

### Step 2 – Traceroute path analysis

**Command:**

```bash
traceroute -n -I 8.8.8.8 2>/dev/null | head -12 \
  || tracepath -n 8.8.8.8 | head -12
```

**Explanation:** `-n` skips DNS lookups for faster output. `-I` uses ICMP echo (may require root). `tracepath` works without root and shows MTU discovery.

**Expected output:**

```text
 1  10.0.0.1  0.412 ms
 2  203.0.113.1  1.234 ms
 3  * * *
 4  8.8.8.8  14.567 ms
```

Asterisks (`*`) indicate no response — common when routers suppress ICMP.

### Step 3 – Inspect ARP/neighbor table

**Command:**

```bash
ip neigh show
ip neigh show dev eth0 2>/dev/null || ip neigh show
GW=$(ip route | awk '/default/ {print $3; exit}')
ping -c 1 "$GW" >/dev/null 2>&1
ip neigh show "$GW"
```

**Explanation:** Lists cached IP-to-MAC mappings. Pinging the gateway populates or refreshes the entry.

**Expected output:**

```text
10.0.0.1 dev eth0 lladdr 00:11:22:33:44:55 REACHABLE
```

If state is `FAILED`, check VLAN, gateway IP, or L2 connectivity.

### Step 4 – Flush and observe ARP refresh (lab caution)

**Command:**

```bash
GW=$(ip route | awk '/default/ {print $3; exit}')
sudo ip neigh flush dev eth0
ip neigh show "$GW"
ping -c 1 "$GW"
ip neigh show "$GW"
```

**Explanation:** Flushing forces re-resolution. In production, only flush during controlled maintenance — brief connectivity blips may occur.

**Expected output:** Entry absent after flush; after ping, MAC address reappears as REACHABLE.

### Step 5 – Examine DHCP lease information

**Command:**

```bash
ip addr show
resolvectl status 2>/dev/null | head -25 || cat /etc/resolv.conf
sudo journalctl -u systemd-networkd --no-pager -n 20 2>/dev/null \
  || sudo cat /var/lib/dhcp/dhclient*.lease 2>/dev/null | head -40
```

**Explanation:** Identifies whether address came from DHCP (`proto dhcp` in `ip route`). Journal or lease files show offered options.

**Expected output:**

```text
inet 10.0.0.42/24 brd 10.0.0.255 scope global dynamic eth0
default via 10.0.0.1 dev eth0 proto dhcp src 10.0.0.42
```

### Step 6 – Simulate DHCP renewal awareness

**Command:**

```bash
sudo dhclient -v eth0 2>/dev/null || \
  sudo networkctl renew eth0 2>/dev/null || \
  echo "Renew command varies by distro — check NetworkManager/networkd"
ip addr show eth0
```

**Explanation:** Forces lease renewal on systems using dhclient or systemd-networkd. Use during maintenance windows only.

### Step 7 – Verify NTP synchronization

**Command:**

```bash
timedatectl status
chronyc tracking 2>/dev/null || timedatectl timesync-status 2>/dev/null
chronyc sources 2>/dev/null | head -10
```

**Explanation:** Confirms NTP is active, shows offset from reference, and lists upstream sources.

**Expected output:**

```text
System clock synchronized: yes
NTP service: active
Reference ID:    A9FEA97B (169.254.169.123)
Stratum:         3
System time:     0.000012345 seconds slow of NTP time
```

### Step 8 – Layered connectivity diagnostic

**Command:**

```bash
bash << 'EOF'
set -euo pipefail
GW=$(ip route | awk '/default/ {print $3; exit}')
echo "=== Gateway ARP ==="
ip neigh show "$GW" 2>/dev/null || echo "No ARP entry"
echo "=== ICMP Gateway ==="
ping -c 2 -W 2 "$GW" && echo OK || echo FAIL
echo "=== ICMP External ==="
ping -c 2 -W 2 8.8.8.8 && echo OK || echo FAIL
echo "=== NTP Sync ==="
timedatectl show -p NTPSynchronized --value
EOF
```

**Expected output:** All layers OK on a healthy host. Isolate failures: no ARP → L2; ARP but no ping → firewall or wrong GW; external fail → routing/NAT.

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
| `ping -c N HOST` | Send N ICMP echo requests | `ping -c 4 gateway` |
| `ping -M do -s SIZE` | MTU discovery test | `ping -M do -s 1472 8.8.8.8` |
| `traceroute -n HOST` | Trace route (numeric hops) | `traceroute -n 1.1.1.1` |
| `tracepath HOST` | Path trace without root | `tracepath 8.8.8.8` |
| `ip neigh show` | Display ARP/neighbor cache | `ip neigh show dev eth0` |
| `ip neigh flush dev IF` | Clear neighbor entries | `sudo ip neigh flush dev eth0` |
| `arp -n` | Legacy ARP table (deprecated) | Prefer `ip neigh` |
| `cat /var/lib/dhcp/*.lease` | DHCP lease details (dhclient) | Inspect options |
| `networkctl status IF` | systemd-networkd DHCP state | `networkctl status eth0` |
| `timedatectl status` | Clock and NTP sync status | `timedatectl status` |
| `chronyc tracking` | NTP offset and stratum | `chronyc tracking` |
| `chronyc sources` | Upstream NTP servers | `chronyc sources -v` |

### Network services health script

Save as `~/bin/l2-l3-services-check.sh` for incident triage:

```bash
#!/usr/bin/env bash
# l2-l3-services-check.sh — ICMP, ARP, DHCP, NTP quick audit
set -euo pipefail

IF="${1:-eth0}"
GW=$(ip route show dev "$IF" 2>/dev/null | awk '/default/ {print $3; exit}')
GW=${GW:-$(ip route | awk '/default/ {print $3; exit}')}

section() { printf '\n=== %s ===\n' "$1"; }

section "Interface & DHCP"
ip -br addr show "$IF" 2>/dev/null || ip -br addr show
ip route show default 2>/dev/null | head -1

section "ARP / Neighbor ($GW)"
if [[ -n "${GW:-}" ]]; then
  ping -c 1 -W 2 "$GW" >/dev/null 2>&1 || true
  ip neigh show "$GW" 2>/dev/null || echo "No neighbor entry for gateway"
else
  echo "No default gateway found"
fi

section "ICMP External"
ping -c 2 -W 3 8.8.8.8 >/dev/null 2>&1 && echo "8.8.8.8: OK" || echo "8.8.8.8: FAIL (may be filtered)"

section "NTP"
timedatectl show -p NTPSynchronized --value 2>/dev/null \
  && timedatectl show -p TimeUSec --value | head -1 \
  || echo "timedatectl unavailable"
command -v chronyc >/dev/null && chronyc tracking 2>/dev/null | grep -E 'Reference|System time' || true
```

Make executable: `chmod +x ~/bin/l2-l3-services-check.sh`

### Capture ARP and DHCP with tcpdump (optional)

```bash
# Terminal 1 — capture DHCP (during renew/reboot)
sudo tcpdump -i eth0 -n port 67 or port 68

# Terminal 2 — capture ARP
sudo tcpdump -i eth0 -n arp
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Treating ping failure as host down"
    Production firewalls routinely block ICMP. Validate with TCP probes (`curl`, `nc -zv`) before declaring outage.

!!! warning "Ignoring STALE or FAILED ARP entries"
    A `FAILED` neighbor entry means L2 resolution broke — often wrong VLAN, unplugged cable, or gateway IP misconfiguration. Flushing DNS won't help.

!!! warning "Hardcoding DHCP-assigned IPs in applications"
    DHCP leases expire and renew. Bind services to `0.0.0.0` or document static reservations in DHCP server config — never assume cloud IPs are permanent without elastic IP / reserved allocation.

!!! warning "Disabling NTP without understanding impact"
    TLS, Kerberos, and distributed databases fail silently or loudly when clocks drift. Always verify `NTPSynchronized=yes` after golden image builds.

!!! warning "Using arp instead of ip neigh"
    The legacy `arp` command shows incomplete information on modern kernels. Standardize on `ip neigh show`.

## Best Practices

!!! tip "Layer diagnostics before escalation"
    For "cannot reach internet": verify ARP to gateway → ICMP to gateway → ICMP to external IP → DNS → application. Document which layer fails in tickets.

!!! tip "Reserve static DHCP leases for servers"
    Infrastructure hosts (databases, load balancers) should have DHCP reservations or static IPs documented in IPAM. Prevents surprise address changes after lease expiry.

!!! tip "Monitor NTP offset in observability stack"
    Alert when `chronyc tracking` reports offset > 100ms on transaction-heavy systems. Include NTP checks in post-deploy smoke tests.

!!! tip "Document ICMP policy per environment"
    Runbooks should state whether ICMP is allowed between tiers. Prevents wasted hours debugging "ping blocked by design."

!!! tip "Use tracepath when traceroute requires root"
    `tracepath` provides hop discovery and PMTUD hints without CAP_NET_RAW — useful in restricted containers.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `ping: Destination Host Unreachable` | No route or ARP failure | Check `ip route`; verify `ip neigh` for gateway; confirm interface UP |
| `ping: 100% packet loss` to external IP | Routing, NAT, or ICMP filter | Ping gateway first; check security groups; test TCP to known port |
| ARP entry `FAILED` | Wrong subnet, VLAN mismatch, GW down | Verify IP/mask; check switch port VLAN; confirm gateway alive |
| No DHCP address (`169.254.x.x` APIPA) | DHCP server unreachable | Check DHCP relay on routers; verify VLAN; inspect `tcpdump port 67` |
| Lease obtained but no internet | Missing option 3 (router) or DNS | Inspect lease options; fix DHCP scope configuration |
| `System clock synchronized: no` | NTP blocked (UDP 123) or misconfigured | Allow outbound UDP 123; set `pool.ntp.org` or cloud NTP; restart chrony |
| Large ping works, small app packets fail | MTU / MSS mismatch | Lower interface MTU; enable TCP MSS clamping on VPN/firewall |
| Traceroute shows `* * *` mid-path | Routers not returning ICMP TTL exceeded | Normal on many networks; use `mtr` or TCP traceroute for clarity |
| Duplicate IP after VM clone | Cloned MAC/IP conflict | Release lease; regenerate machine-id; assign new IP |

## Summary

- **ICMP** enables ping and traceroute diagnostics; blocking ICMP is common — do not rely on it alone for uptime checks
- **ARP** resolves IP to MAC on local segments; the neighbor cache (`ip neigh`) is the first place to look for L2 failures
- **DHCP DORA** assigns IP, mask, gateway, and DNS; understand lease renewal and cloud metadata options
- **NTP** keeps clocks accurate for TLS, logs, and distributed systems — verify with `timedatectl` and `chronyc`
- Troubleshoot bottom-up: link → ARP → ICMP gateway → ICMP external → DNS → application
- These services underpin every TCP connection and HTTP request your applications make

## Interview Questions

1. What ICMP types are used by ping and traceroute?
2. Explain the DHCP DORA process step by step.
3. Why does ARP only work on the local subnet?
4. A host can ping its gateway but not 8.8.8.8. Where is the problem?
5. What does an ARP cache entry in FAILED state indicate?
6. Why is accurate NTP synchronization critical in Kubernetes and TLS environments?
7. How would you test for MTU issues between two hosts?
8. What is gratuitous ARP and when is it used?
9. Ping fails but curl to HTTPS works. Explain.
10. How do you inspect DHCP-assigned DNS servers on a Linux host?

??? tip "Sample Answers (Questions 2, 4, and 9)"

    **Q2 — DHCP DORA:** Discover (client broadcast seeking config) → Offer (server proposes IP and options) → Request (client accepts one offer, broadcasts intent) → Acknowledge (server confirms lease). Client then configures interface with offered IP, mask, gateway (option 3), and DNS (option 6).

    **Q4 — Gateway OK, external fail:** L2 and local L3 to gateway work. Failure is beyond the gateway: missing/incorrect default route (less likely if GW ping works), upstream router ACL, NAT misconfiguration, ISP issue, or firewall blocking outbound to that destination. Verify with `ip route get 8.8.8.8` and tcpdump on gateway if accessible.

    **Q9 — Ping fails, HTTPS works:** ICMP Echo is blocked (local firewall, security group, or upstream network policy) while TCP port 443 is permitted. Common in cloud and enterprise networks. Use TCP-based health checks for monitoring instead of ping-only alerts.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [Routing Fundamentals](routing-fundamentals.md) *(previous in Module 2)*
- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md) *(next — Module 3)*
- [Linux Networking Essentials](../linux/linux-networking-essentials.md)
- [IP Addressing and Subnetting](ip-addressing-and-subnetting.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)
- Cheat sheet: [Networking Cheat Sheet](../cheatsheets/networking.md)
- Interview prep: [Networking Interview Prep](../interview/networking.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [RFC 792 — ICMP](https://www.rfc-editor.org/rfc/rfc792)
- [RFC 826 — ARP](https://www.rfc-editor.org/rfc/rfc826)
- [RFC 2131 — DHCP](https://www.rfc-editor.org/rfc/rfc2131)
- [RFC 5905 — NTP Version 4](https://www.rfc-editor.org/rfc/rfc5905)
- [ip-neighbour man page](https://man7.org/linux/man-pages/man8/ip-neighbour.8.html)
- [chrony documentation](https://chrony-project.org/documentation.html)
- [systemd-timesyncd](https://www.freedesktop.org/software/systemd/man/systemd-timesyncd.service.html)
