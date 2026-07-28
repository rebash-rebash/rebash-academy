---
title: Linux Networking Essentials
description: Configure interfaces, routes, DNS, and troubleshoot connectivity with ip, ss, and dig.
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
  - networking
  - dns
  - routing
prerequisites:
  - Complete Module 5 tutorials or equivalent experience
  - Basic understanding of IP addresses and TCP/UDP
comments: false
---

# Linux Networking Essentials

## Overview

Every Linux server — web host, database, Kubernetes node, or CI runner — depends on correct network configuration. You need to verify IP addresses, default routes, DNS resolution, open ports, and end-to-end connectivity before blaming application code for outages.

This tutorial covers the modern **`ip`** command suite (replacing legacy `ifconfig` and `route`), DNS resolution with **`resolvectl`** and `/etc/resolv.conf`, socket inspection with **`ss`**, and connectivity testing with **`ping`** and **`traceroute`**. You will also learn a systematic workflow to resolve common connectivity failures.

This tutorial is part of **Module 6: Storage, Logs, Networking & Operations** in the REBASH Academy Linux series.

## Prerequisites

- Complete [Essential Linux Commands](essential-linux-commands.md) or equivalent experience
- A Linux VM or cloud instance with network access (outbound ICMP/HTTP)
- `sudo` privileges for interface and firewall exercises
- Optional second machine or known external IP for connectivity tests

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Display and interpret IP addresses, interfaces, and link state with `ip`
- [ ] Read and modify routing tables and identify the default gateway
- [ ] Troubleshoot DNS resolution failures using `dig`, `resolvectl`, and resolv.conf
- [ ] List listening and established connections with `ss`
- [ ] Diagnose connectivity issues using ping, traceroute, and a layered troubleshooting model

## Architecture

```d2
direction: down

Host: Host {
        APP: Application
        SS: "ss / netstat"
        IP: "ip command"
    }
    Stack: Stack {
        NIC: "Network Interface eth0"
        RT: "Routing Table"
        DNS: "Resolver / systemd-resolved"
    }
    External: External {
        GW: "Default Gateway"
        DNSS: "DNS Server 8.8.8.8"
        DEST: "Remote Host"
    }
    Host.APP -> Host.SS
    Host.APP -> Stack.NIC
    Host.IP -> Stack.NIC
    Host.IP -> Stack.RT
    Host.APP -> Stack.DNS
    Stack.RT -> External.GW
    Stack.DNS -> External.DNSS
    External.GW -> External.DEST
```

## Theory

### The ip command

`ip` from the **iproute2** package is the modern tool for network configuration and inspection:

| Subcommand | Purpose |
|------------|---------|
| `ip addr` (or `ip a`) | Show IP addresses assigned to interfaces |
| `ip link` (or `ip l`) | Show interface link-layer state (UP/DOWN) |
| `ip route` (or `ip r`) | Show and manage routing table |
| `ip neigh` | Show ARP/neighbor cache |

Legacy tools `ifconfig` and `route` are deprecated on current distributions but may still be installed.

### IP addressing basics

Each interface can have one or more IP addresses. Common patterns:

- **Loopback:** `127.0.0.1` on `lo` — always present for local communication
- **Private RFC1918:** `10.x`, `172.16–31.x`, `192.168.x` — internal networks
- **Public:** Routable on the internet (cloud instances, load balancers)

Cloud providers often assign metadata IPs and use DHCP or cloud-init for configuration.

### Routing

The routing table determines where packets go. The **default route** (`default via GATEWAY`) sends traffic to destinations not matched by more specific routes.

```bash
ip route show
# default via 10.0.0.1 dev eth0 proto dhcp src 10.0.0.42 metric 100
# 10.0.0.0/24 dev eth0 proto kernel scope link src 10.0.0.42
```

Without a default route, the host cannot reach external networks.

### DNS resolution

DNS maps hostnames to IP addresses. Resolution order depends on configuration:

- **Traditional:** `/etc/resolv.conf` lists nameservers
- **systemd-resolved:** `resolvectl status` shows per-link DNS; `/etc/resolv.conf` may be a stub pointing to `127.0.0.53`

Key files:

| File | Purpose |
|------|---------|
| `/etc/resolv.conf` | Nameserver list (may be managed) |
| `/etc/hosts` | Static local overrides |
| `/etc/nsswitch.conf` | Order of lookup (files, dns, etc.) |

### ss — socket statistics

`ss` replaces `netstat` for inspecting sockets:

- `-t` TCP, `-u` UDP, `-l` listening, `-n` numeric (no DNS), `-p` process info (requires root)

Example: `ss -tuln` shows all TCP/UDP listening ports.

### ping and traceroute

- **ping** tests ICMP reachability (may be blocked by firewalls)
- **traceroute** (or `tracepath`) shows the path packets take hop by hop

Layered connectivity test:

1. Ping gateway (L3 local)
2. Ping external IP like `8.8.8.8` (routing/NAT)
3. Resolve and ping hostname (DNS + routing)

### Connectivity troubleshooting model

Work bottom-up through the stack:

1. **Link:** Is the interface UP? (`ip link`)
2. **IP:** Valid address assigned? (`ip addr`)
3. **Route:** Default gateway present? (`ip route`)
4. **DNS:** Hostname resolves? (`dig`, `resolvectl`)
5. **Firewall:** Ports blocked locally or upstream? (`ss`, `ufw`, security groups)
6. **Remote:** Target service listening and reachable?

## Hands-on Lab

### Step 1 – Inspect interfaces and IP addresses

```bash
ip link show
ip addr show
hostname -I
```

**Expected output:**

```text
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
    inet 10.0.0.42/24 brd 10.0.0.255 scope global eth0
```

Interface state `UP` and an `inet` line confirm L3 configuration.

### Step 2 – Examine routing table

```bash
ip route show
ip route get 8.8.8.8
```

**Expected output:**

```text
default via 10.0.0.1 dev eth0
10.0.0.0/24 dev eth0 proto kernel scope link src 10.0.0.42
8.8.8.8 via 10.0.0.1 dev eth0 src 10.0.0.42
```

The second command shows which interface and gateway would carry traffic to Google DNS.

### Step 3 – DNS configuration and resolution

```bash
cat /etc/resolv.conf
resolvectl status 2>/dev/null | head -20 || true
dig +short google.com A
getent hosts google.com
```

**Expected output:** Nameserver entries (e.g., `nameserver 127.0.0.53` or cloud DNS); `dig` returns one or more A records like `142.250.80.78`.

### Step 4 – Test layered connectivity

```bash
GW=$(ip route | awk '/default/ {print $3}')
echo "Gateway: $GW"
ping -c 3 "$GW"
ping -c 3 8.8.8.8
ping -c 3 google.com
```

**Expected output:** All three pings succeed with 0% packet loss. If step 3 fails but step 2 works, suspect DNS.

### Step 5 – Trace the network path

```bash
traceroute -n 8.8.8.8 2>/dev/null | head -10 \
  || tracepath -n 8.8.8.8 | head -10
```

**Expected output:** Hop-by-hop list showing gateway first, then ISP/cloud hops toward destination.

### Step 6 – Inspect listening ports

```bash
ss -tuln
sudo ss -tulpn | head -15
```

**Expected output:**

```text
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:Port
tcp   LISTEN 0      128    0.0.0.0:22           0.0.0.0:*
tcp   LISTEN 0      511    127.0.0.1:6379       0.0.0.0:*
```

Port 22 (SSH) listening on `0.0.0.0` is typical for servers.

### Step 7 – Simulate and fix a DNS failure

```bash
# Backup and break DNS temporarily
sudo cp /etc/resolv.conf /tmp/resolv.conf.bak 2>/dev/null || true
echo "nameserver 127.0.0.1" | sudo tee /etc/resolv.conf
ping -c 1 google.com 2>&1 || echo "DNS failure expected"
dig +time=2 +tries=1 google.com 2>&1 | tail -3
# Restore
sudo cp /tmp/resolv.conf.bak /etc/resolv.conf 2>/dev/null || true
ping -c 1 google.com
```

**Expected output:** Ping by hostname fails during broken DNS; IP ping to `8.8.8.8` still works if routing is intact. Restoration succeeds.

### Step 8 – Connectivity checklist script

Run a consolidated diagnostic:

```bash
bash << 'EOF'
echo "=== Link ==="
ip link show up
echo "=== Route ==="
ip route | head -3
echo "=== DNS ==="
dig +short example.com || echo "DNS failed"
echo "=== External ==="
ping -c 1 -W 2 8.8.8.8 && echo "OK" || echo "FAIL"
EOF
```

**Expected output:** Summary block confirming each layer — all OK on a healthy system.

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

| Command | Description |
|---------|-------------|
| `ip addr show` | Display IP addresses on all interfaces |
| `ip link show` | Show interface link state (UP/DOWN) |
| `ip link set eth0 up` | Bring interface up |
| `ip route show` | Display routing table |
| `ip route get IP` | Show route used to reach destination |
| `ip neigh show` | Display ARP/neighbor table |
| `hostname -I` | Print all IP addresses |
| `ss -tuln` | List TCP/UDP listening ports (numeric) |
| `ss -tulpn` | Include process names (requires sudo) |
| `ping -c 4 HOST` | Send 4 ICMP echo requests |
| `traceroute HOST` | Trace path to destination |
| `tracepath HOST` | Alternative path trace (no root required) |
| `dig HOST` | DNS lookup (detailed) |
| `dig +short HOST A` | Short A record answer |
| `resolvectl status` | systemd-resolved DNS configuration |
| `getent hosts HOST` | Resolution via nsswitch (glibc) |
| `cat /etc/resolv.conf` | View configured nameservers |
| `curl -I https://example.com` | Test HTTP/HTTPS connectivity |
| `nc -zv HOST PORT` | Test TCP port connectivity |

## Code Examples

### Network health check script

```bash
#!/bin/bash
# net-check.sh — quick connectivity diagnostic
set -euo pipefail

GW=$(ip route | awk '/default/ {print $3; exit}')
TARGET="${1:-8.8.8.8}"
HOST="${2:-google.com}"

check() {
  local name="$1" cmd="$2"
  if eval "$cmd" &>/dev/null; then
    echo "[OK]   $name"
  else
    echo "[FAIL] $name"
    return 1
  fi
}

check "Interface UP" "ip link show up | grep -q UP"
check "Default route" "ip route | grep -q default"
check "Gateway $GW" "ping -c1 -W2 $GW"
check "External IP $TARGET" "ping -c1 -W2 $TARGET"
check "DNS $HOST" "getent hosts $HOST"
check "HTTP" "curl -sf --max-time 5 -o /dev/null https://example.com"
```

### Temporary static IP (lab only)

```bash
# Add secondary IP — lost on reboot unless persisted via netplan/NetworkManager
sudo ip addr add 192.168.99.10/24 dev eth0
ip addr show eth0
```

### Test if a remote port is open

```bash
#!/bin/bash
HOST="${1:?host}"
PORT="${2:?port}"
timeout 3 bash -c "echo >/dev/tcp/$HOST/$PORT" 2>/dev/null \
  && echo "Port $PORT open on $HOST" \
  || echo "Port $PORT closed or filtered on $HOST"
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Using ifconfig on modern systems"
    `ifconfig` is deprecated and may not show all addresses or routes. Use `ip addr` and `ip route`.

!!! warning "Assuming ping failure means total outage"
    Many networks block ICMP. A failed ping does not always mean the host is down — test TCP with `curl` or `nc`.

!!! warning "Editing resolv.conf on systemd-resolved systems"
    Changes may be overwritten. Use `resolvectl` or netplan/NetworkManager configuration instead.

!!! warning "Ignoring cloud security groups and NACLs"
    Local `ss` shows a port listening, but cloud firewall rules may still block inbound traffic.

!!! warning "Testing DNS when routing is broken"
    Always test IP connectivity before hostname resolution to isolate the failure layer.

## Best Practices

!!! tip "Use layered diagnostics"
    Test gateway → external IP → DNS hostname in order to pinpoint the failing layer quickly.

!!! tip "Prefer ss over netstat"
    `ss` is faster and maintained; use `ss -tulpn` for service port audits.

!!! tip "Document expected network config"
    Maintain runbooks with expected IP, gateway, DNS, and open ports per environment.

!!! tip "Use dig +trace for DNS delegation issues"
    `dig +trace example.com` reveals authoritative server problems.

!!! tip "Automate checks in monitoring"
    Synthetic checks (HTTP, TCP, DNS) catch issues before users report them.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Network is unreachable` | No route to destination | Check `ip route`; add default gateway |
| IP works, hostname fails | DNS misconfiguration | Fix `/etc/resolv.conf` or `resolvectl`; verify with `dig` |
| Interface DOWN | Cable, driver, admin down | `sudo ip link set eth0 up`; check cloud NIC attachment |
| Cannot bind to port | Address not assigned or port in use | Verify `ip addr`; check `ss -tulpn` for conflicts |
| Connection timeout | Firewall or security group | Check `ufw`, `iptables`, cloud SG rules |
| Intermittent packet loss | Congestion or MTU mismatch | Run `mtr`; try `ping -M do -s 1472` for MTU issues |
| Works locally, not remotely | Service bound to 127.0.0.1 | Reconfigure to `0.0.0.0` or specific interface IP |
| Slow DNS lookups | Slow upstream resolver | Switch nameservers; check `resolvectl statistics` |

## Summary

- Use `ip addr`, `ip link`, and `ip route` as the primary tools for network inspection on modern Linux.
- DNS issues are isolated by comparing ping to IP vs hostname; use `dig` and `resolvectl` for details.
- `ss -tulpn` reveals listening services and owning processes — essential for security audits and debugging.
- Troubleshoot connectivity bottom-up: link → IP → route → DNS → firewall → remote service.
- Cloud environments add security groups and metadata networking — always check both OS and platform layers.

## Interview Questions

**1. What command replaces ifconfig for viewing IP addresses?**

*Sample answer:* `ip addr show` or `ip a`. It shows all addresses, prefixes, and interface state.

**2. How do you find the default gateway on Linux?**

*Sample answer:* `ip route show default` or `ip route | grep default`. The gateway IP appears after `via`.

**3. A server can ping 8.8.8.8 but not google.com. What is wrong?**

*Sample answer:* DNS resolution is failing. Routing works (IP reachable) but nameservers in resolv.conf or systemd-resolved are misconfigured. Verify with `dig google.com`.

**4. What is the difference between ss and netstat?**

*Sample answer:* Both show socket information. `ss` reads data directly from kernel via netlink, is faster, and is the recommended tool on modern Linux. `netstat` is legacy.

**5. How do you list all TCP ports listening on a server?**

*Sample answer:* `ss -tln` or `sudo ss -tulpn` for process details. `-l` filters listening sockets; `-n` shows numeric ports.

**6. What does `ip route get 10.0.0.5` tell you?**

*Sample answer:* It shows the exact route, source IP, and interface the kernel would use to reach that destination — useful for policy routing debugging.

**7. Why might ping fail even when the web service works?**

*Sample answer:* ICMP may be blocked by firewalls (local or upstream) while TCP port 443 remains open. Test with `curl` or `nc` instead.

**8. Explain /etc/hosts vs DNS.**

*Sample answer:* `/etc/hosts` provides static local mappings checked first (per nsswitch.conf). DNS queries upstream nameservers for dynamic resolution. `/etc/hosts` overrides DNS for matching entries.

**9. How do you test if port 443 is open on a remote host?**

*Sample answer:* `nc -zv host 443`, `curl -I https://host`, or `timeout 3 bash -c 'echo >/dev/tcp/host/443'`.

**10. Describe a systematic approach to "server cannot reach the internet."**

*Sample answer:* Check interface UP and IP assigned → verify default route → ping gateway → ping external IP → test DNS → check firewall/NAT/security groups → verify proxy settings if applicable.

1. How would you explain linux networking essentials to a junior engineer in two minutes?
2. What production failure mode appears when teams ignore linux networking essentials?
3. Which metrics or logs would you check first when linux networking essentials misbehaves?
4. What is a secure default related to linux networking essentials?
5. How would you validate a change involving linux networking essentials in CI or a staging environment?
6. What trade-off would you accept to simplify operations around linux networking essentials?
7. Describe a common anti-pattern with linux networking essentials and how you fix it.
8. How does linux networking essentials interact with networking, identity, or storage in a real system?
9. What would you put on a runbook checklist for linux networking essentials?
10. When would you intentionally not follow the default approach taught here?

## Related Tutorials

- [Linux – Category Overview](index.md)
- [Environment Variables and Shell Configuration](environment-variables-shell-config.md) *(previous)*
- [File Archiving and Compression](file-archiving-and-compression.md) *(next)*
- [Linux Security Hardening Basics](linux-security-hardening-basics.md)
- [Troubleshooting Linux Systems](troubleshooting-linux-systems.md)
- [SSH and Remote Administration](ssh-remote-administration.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)
- Cheat sheet: [Linux Cheat Sheet](../cheatsheets/linux.md)
- Interview prep: [Linux Interview Prep](../interview/linux.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [iproute2 documentation](https://wiki.linuxfoundation.org/networking/iproute2)
- [ip command man pages](https://man7.org/linux/man-pages/man8/ip.8.html)
- [ss man page](https://man7.org/linux/man-pages/man8/ss.8.html)
- [systemd-resolved](https://www.freedesktop.org/software/systemd/man/systemd-resolved.service.html)
- [REBASH Academy – Linux Overview](index.md)
