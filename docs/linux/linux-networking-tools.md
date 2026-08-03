---
title: "Linux Networking Tools"
description: "Troubleshoot host connectivity with ip, ss, ping, dig, curl, netcat, and a short tcpdump capture on a practice Ubuntu VM."
difficulty: intermediate
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 9 · Linux Networking"
tags:
  - linux
  - ip
  - ss
  - dns
  - tcpdump
  - networking
prerequisites:
  - linux/lvm-swap-and-disk-monitoring
next:
  - linux/ssh-and-remote-access
related:
  - labs/linux-ops-toolkit-lab
labs:
  - labs/linux-ops-toolkit-lab
interview: interview/linux
comments: false
---

# Linux Networking Tools

## Overview

When an application “cannot connect”, you need a clear order of checks: **Do I have an IP address?** **Is a process listening?** **Does Domain Name System (DNS) resolve?** **Does Transmission Control Protocol (TCP) reach the port?** Linux networking tools answer those questions on the host itself.

This tutorial teaches the modern stack: **`ip`** for addresses and routes, **`ss`** for sockets (prefer this over old `netstat`), **`ping`** / **`traceroute`** (or `tracepath`) for path checks, **`dig`** / **`host`** for DNS, **`curl`** / **`wget`** for Hypertext Transfer Protocol (HTTP) checks, **`nc` (netcat)** for port probes, and a short **`tcpdump`** capture when you need packet proof. On cloud virtual machines (VMs), jump servers, Continuous Integration (CI) runners, and Kubernetes nodes, these tools separate “host problem” from “security group / firewall problem” from “application bug”.

In production, wrong routes black-hole traffic, broken resolvers make every hostname look dead, and firewalls often block Internet Control Message Protocol (ICMP) even when TCP works. Good engineers collect small evidence files (`ip`, `ss`, `dig`, `curl -I`) before they change security groups or reopen tickets. Prefer `ip`/`ss` on current Ubuntu and Red Hat images — `ifconfig` and `netstat` are legacy.

This is **Tutorial 14** in **Module 9: Linux Networking** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers. By the end, you will have a small network evidence pack you can attach to an incident ticket.

## Prerequisites

- [LVM, Swap, and Disk Monitoring](lvm-swap-and-disk-monitoring.md)
- A **practice Ubuntu 22.04/24.04 VM** with `sudo`
- Outbound DNS and HTTPS allowed (lab uses public DNS and `example.com`)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Read addresses, routes, and neighbours with `ip`
- [ ] List listening sockets with `ss -tulpn` and explain what you see
- [ ] Query DNS with `dig` / `host` and test HTTP with `curl`
- [ ] Probe a TCP port with `nc` and capture a short packet sample with `tcpdump`
- [ ] Build a network evidence pack suitable for an incident ticket

## Architecture

Networking tools sit above the kernel TCP/IP stack. Applications open sockets; the kernel routes packets; host firewalls and the network interface card (NIC) send and receive traffic.

![Architecture diagram for Linux Networking Tools](../assets/excalidraw/linux-networking-stack.svg)

## Theory

### What it is

| Question | Tool |
|----------|------|
| Do I have an address / route? | `ip` |
| Is anything listening? | `ss -tulpn` |
| Can I reach a host (ICMP)? | `ping` |
| Where does the path go? | `traceroute` / `tracepath` |
| Does the name resolve? | `dig`, `host`, `nslookup` |
| Does HTTP/TLS work? | `curl`, `wget` |
| Is the TCP port open? | `nc` (netcat) |
| What packets are on the wire? | `tcpdump` |

`ip` replaces `ifconfig` for addresses, routes, and the neighbour (ARP) cache. `ss` replaces `netstat` for socket state. Keep both ideas: **configuration** (`ip`) and **who is talking** (`ss`).

``` {.bash .ra-terminal title="Terminal"}
ip -br a
ip route
ss -tulpn
```

### Why it matters

Most “app is down” tickets are network or DNS until proven otherwise. Cloud security groups and host firewalls fail closed. A wrong default route or empty resolver list looks like a total outage. Fast, accurate use of `ip`, `ss`, and `dig` saves hours and avoids random reboots.

### How it works

1. **Local stack** — `ip -br a` shows interfaces; `ip route` shows the routing table; `ip neigh` shows ARP/neighbour entries.
2. **Listeners** — `ss -tulpn` lists TCP/UDP listeners with process names when permissions allow.
3. **Reachability** — `ping -c 3` proves ICMP; remember some networks block ICMP while TCP still works.
4. **DNS** — `dig +short example.com A` asks for an A record deliberately; `host example.com` is a short alternative.
5. **Application layer** — `curl -I https://example.com` checks HTTP headers and TLS; `wget` can download files.
6. **Port probe** — `nc -vz host port` checks whether a TCP port accepts a connection.
7. **Capture** — `tcpdump` records packets for a short, targeted window; stop quickly and treat captures as sensitive.

```bash
dig +short example.com A
curl -I --max-time 10 https://example.com
nc -vz 1.1.1.1 53
```

### Key concepts and comparisons

| Modern | Legacy (avoid as first choice) |
|--------|--------------------------------|
| `ip` | `ifconfig` / `route` |
| `ss` | `netstat` |
| `dig` / `host` | only `nslookup` |

| Signal | Means | Next check |
|--------|-------|------------|
| No address on NIC | DHCP / cloud metadata / cable | `ip -br a`, cloud console |
| Address OK, no route | Missing default route | `ip route` |
| DNS fails | Resolver / Network Manager | `/etc/resolv.conf`, `dig @8.8.8.8` |
| DNS OK, TCP fails | Firewall / security group / wrong port | `ss`, `nc`, cloud SG |
| TCP OK, HTTP fails | App / TLS / reverse proxy | `curl -v`, app logs |

### Common pitfalls

- Trusting `ping` alone when ICMP is blocked but HTTPS works.
- Using `ifconfig`/`netstat` on images where they are missing.
- Running long `tcpdump` captures that fill the disk or leak secrets.
- Forgetting that `ss -p` may need root to show process names.
- Changing cloud security groups before proving the host has an address and a listener.

## Hands-on Lab

### Objective

On a practice Ubuntu VM, collect addresses, routes, listeners, DNS, HTTP, a port probe, and a short packet capture under `~/rebash-linux/lab14`, then pack the proof into one archive.

### Prerequisites

- Ubuntu 22.04/24.04 with `sudo`
- Packages: `iproute2`, `iputils-ping`, `dnsutils` (for `dig`/`host`), `curl`, `netcat-openbsd` or `ncat`, `tcpdump` (install if missing)
- Outbound DNS (UDP/TCP 53) and HTTPS (443)

### Lab environment

Workspace: `~/rebash-linux/lab14`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab14 && cd ~/rebash-linux/lab14
set -euo pipefail
whoami | tee admin-user.txt
sudo -n true 2>/dev/null || sudo -v

# Install missing tools (Ubuntu/Debian)
sudo apt-get update -y
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
  iproute2 iputils-ping dnsutils curl netcat-openbsd tcpdump traceroute
```

!!! example "Expected output"
    packages install (or already present); you can run `ip`, `ss`, `dig`, `curl`, `nc`, `tcpdump`.


### Real-world scenario

Users say the portal is slow. Before you touch the load balancer, the on-call engineer asks for host proof: IP and route, listening ports, DNS for the public name, an HTTPS header check, and a short capture showing DNS or TCP. You gather that evidence on the practice VM the same way you would on a bastion or app node.

### Step-by-step tasks

#### Task 1 – Addresses, routes, and listeners

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab14
set -euo pipefail

ip -br a | tee ip-brief.txt
ip route | tee ip-route.txt
ip neigh | tee ip-neigh.txt || true
ss -tulpn | tee ss-listen.txt

# Basic asserts
grep -E 'UP|UNKNOWN' ip-brief.txt
test -s ip-route.txt
grep -E 'LISTEN|UNCONN' ss-listen.txt
```

!!! example "Expected output"
    at least one UP interface with an address; a non-empty route table; `ss` shows listening sockets (for example `ssh` on port 22).


#### Task 2 – DNS and HTTP checks

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab14
set -euo pipefail

# Resolver file (may be a symlink on systemd-resolved systems)
ls -l /etc/resolv.conf | tee resolv-ls.txt
cat /etc/resolv.conf | tee resolv.conf.txt

dig +short example.com A | tee dig-a.txt
host example.com | tee host-example.txt
test -s dig-a.txt

# ICMP may be blocked in some networks — record result, do not fail the lab
ping -c 3 -W 2 1.1.1.1 | tee ping-cloudflare.txt || echo "ping blocked or failed" | tee -a ping-cloudflare.txt

curl -sS -I --max-time 15 https://example.com | tee curl-headers.txt
grep -E 'HTTP/|location:| LocatioN:' -i curl-headers.txt
```

!!! example "Expected output"
    `dig-a.txt` has at least one IPv4 address; `curl-headers.txt` shows an HTTP status line (often `HTTP/2 200` or a redirect).


#### Task 3 – Port probe, short capture, evidence pack

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab14
set -euo pipefail

# TCP probe to a well-known DNS server (port 53)
nc -vz -w 5 1.1.1.1 53 2>&1 | tee nc-dns.txt
grep -Ei 'succeeded|open|connected' nc-dns.txt

# Short tcpdump while generating DNS traffic (needs sudo)
sudo timeout 8 tcpdump -nn -c 20 -i any udp port 53 \
  -w dns-sample.pcap 2>tcpdump-stderr.txt || true
sudo chmod a+r dns-sample.pcap 2>/dev/null || true
test -s dns-sample.pcap
tcpdump -nn -r dns-sample.pcap 2>/dev/null | head -n 20 | tee dns-sample-read.txt || true

tar -czf network-evidence.tgz \
  admin-user.txt ip-brief.txt ip-route.txt ip-neigh.txt ss-listen.txt \
  resolv-ls.txt resolv.conf.txt dig-a.txt host-example.txt \
  ping-cloudflare.txt curl-headers.txt nc-dns.txt \
  dns-sample.pcap dns-sample-read.txt tcpdump-stderr.txt
ls -l network-evidence.tgz | tee evidence-ls.txt
```

!!! example "Expected output"
    `nc` reports success/open to `1.1.1.1:53`; `dns-sample.pcap` is not empty; `network-evidence.tgz` exists.


### Validation steps

- [ ] `ip -br a` shows an UP interface with an address
- [ ] `ss -tulpn` lists listening sockets
- [ ] `dig +short example.com A` returns an address
- [ ] `curl -I https://example.com` returns HTTP headers
- [ ] `network-evidence.tgz` exists under `~/rebash-linux/lab14`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `dig: command not found` | `dnsutils` missing | `sudo apt-get install -y dnsutils` |
| `nc: command not found` | netcat package missing | `sudo apt-get install -y netcat-openbsd` |
| `curl: Could not resolve host` | DNS broken | Check `/etc/resolv.conf`; try `dig @1.1.1.1 example.com` |
| Empty `pcap` | No UDP/53 traffic or wrong interface | Re-run capture; use `-i any`; generate traffic with `dig` in another shell |
| `ss` shows no process names | Not root | Use `sudo ss -tulpn` when you need PIDs |

### Challenge exercise

Start a temporary listener with `nc -l 127.0.0.1 9999` in one terminal (or background), prove it with `ss -tlnp | grep 9999`, then connect with `nc -vz 127.0.0.1 9999`. Save both outputs as `challenge-ss.txt` and `challenge-nc.txt`. Stop the listener when done.

### Learning outcomes

- Collected host IP, route, and socket evidence
- Proved DNS and HTTPS from the VM
- Used `nc` and a short `tcpdump` capture
- Packed evidence for an incident ticket

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab14
set -euo pipefail
# Stop any leftover challenge listener if you started one
pkill -f 'nc -l 127.0.0.1 9999' 2>/dev/null || true
# Keep the evidence archive if you want it; otherwise:
# rm -f network-evidence.tgz *.txt *.pcap
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab14/` with evidence files
- [ ] You can explain when to use `ip` vs `ss` vs `dig` vs `curl`
- [ ] You know why ping success is not the same as TCP/HTTP success
- [ ] You can describe one production failure (wrong route, bad DNS, closed port)

## Code Walkthrough

In real incidents, host networking checks usually follow this order:

1. **Local identity** — `ip -br a`, `ip route`
2. **Listeners** — `ss -tulpn` (is the app even listening?)
3. **Name → address** — `dig` / `host`
4. **Port / HTTP** — `nc`, `curl -I` / `curl -v`
5. **Proof** — short `tcpdump` only when the above is not enough  

Prefer modern tools. Keep captures short. Attach text evidence to the ticket.

## Security Considerations

- Packet captures may contain secrets (cookies, tokens) — store and share carefully  
- Do not run wide `tcpdump` on production without change control  
- Prefer least privilege: many checks work without root; use sudo only for capture / process names  
- Treat public DNS tests as connectivity checks, not as load tests  
- Never disable host firewalls “just to test” without a rollback plan  

## Common Mistakes

!!! warning "Using only ping to declare the network healthy"
    Many clouds block ICMP. **Fix:** also test TCP (`nc`) and HTTP (`curl`).

!!! warning "Relying on ifconfig/netstat"
    They may be missing on minimal images. **Fix:** learn `ip` and `ss` first.

!!! warning "Long tcpdump captures"
    Disk fills; privacy risk rises. **Fix:** use `-c` count or `timeout`, filter ports, stop quickly.

!!! warning "Changing security groups before host proof"
    You may “fix” the wrong layer. **Fix:** collect `ip`/`ss`/`dig` first.

## Best Practices

- Keep a fixed check order: address → route → listen → DNS → port → HTTP  
- Save command output for tickets (`tee`)  
- Prefer `dig +short` for scripts; use `curl -v` when TLS fails  
- Use `ss -tulpn` before restarting services “to fix networking”  
- Document which checks need outbound internet vs private VPC only  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `Network is unreachable` | No default route | Check `ip route`, cloud routing tables |
| `Temporary failure in name resolution` | Broken resolver | Fix `/etc/resolv.conf` / systemd-resolved |
| Connection timed out | Firewall / SG / wrong IP | `nc -vz`, check cloud security group |
| Connection refused | Nothing listening | `ss -tulpn`, start or fix the service |
| HTTP works, ping fails | ICMP filtered | Ignore ping; trust TCP/HTTP |

## Summary

Linux networking tools give you a clear path from **address and route** to **socket**, **DNS**, **port**, and **HTTP**. Prefer `ip` and `ss`, prove each layer with short commands, and save evidence before you change cloud firewalls. Next, learn day-to-day remote access in [SSH and Remote Access](ssh-and-remote-access.md).

## Interview Questions

**1. What is the difference between `ip` and `ss`, and when do you use each in an incident?**

??? success "Reveal answer"
    **`ip`** shows host network configuration: interfaces, addresses, routes, and neighbours. **`ss`** shows socket state: who is listening and who is connected. In an incident, first confirm the host has an address and a route (`ip`), then check whether the application port is listening (`ss`), then test DNS and the remote port.

**2. Ping fails but `curl https://…` works. What does that tell you?**

??? success "Reveal answer"
    ICMP may be blocked by a firewall or security group while TCP 443 is allowed. Ping is useful but not required for “network healthy”. Prefer TCP probes (`nc`) and application checks (`curl`) as proof of service reachability.

**3. How do you prove DNS is the problem versus the application?**

??? success "Reveal answer"
    Run `dig +short name A` (or `host name`). If DNS fails, try `dig @1.1.1.1 name` to see whether a public resolver works. If dig works but the app fails, check the app’s resolver settings, caching, or wrong hostname. If dig fails everywhere, fix resolvers (`/etc/resolv.conf`, systemd-resolved, VPC DNS).

**4. Why prefer `ss` over `netstat` on modern Ubuntu cloud images?**

??? success "Reveal answer"
    `ss` is maintained with `iproute2` and is present on most minimal images. `netstat` often needs the older `net-tools` package. Interviewers expect you to default to `ss -tulpn` for listeners.

**5. How would you use `tcpdump` safely during a production incident?**

??? success "Reveal answer"
    Capture for a short time with a tight filter (`port 53`, `host x.x.x.x`), use `-c` or `timeout`, write to a known path, and treat the file as sensitive. Prefer proving the issue with `ip`/`ss`/`dig`/`curl` first; use packet capture when you need wire proof.

**6. `nc -vz host 443` succeeds but the browser shows a certificate error. Which layer failed?**

??? success "Reveal answer"
    The **TCP port is open**, so routing and firewall likely allow traffic. The failure is at **TLS/certificate** (or hostname mismatch), not basic connectivity. Next use `curl -vI https://host` and inspect the certificate chain.

**7. A new cloud VM has no outbound internet. Which three commands do you run first?**

??? success "Reveal answer"
    (1) `ip -br a` and `ip route` for address and default route; (2) `cat /etc/resolv.conf` and `dig` for DNS; (3) `curl -I` or `nc -vz` to a known endpoint. Then check cloud route tables, NAT gateway, and security groups — but only after host-local proof.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [LVM, Swap, and Disk Monitoring](lvm-swap-and-disk-monitoring.md) *(previous)*
- [SSH and Remote Access](ssh-and-remote-access.md) *(next)*
- [Lab — Linux Ops Toolkit](../labs/linux-ops-toolkit-lab.md) *(more practice)*

## References

- [`ip(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/ip.8.html) — iproute2 address and route management  
- [`ss(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/ss.8.html) — socket statistics  
- [`dig(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/dig.1.html) — DNS lookup  
- [`tcpdump(8)`](https://www.tcpdump.org/manpages/tcpdump.1.html) — packet capture  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
