---
title: "Linux Networking Tools"
description: "Linux ip, ss, DNS, curl, and basic connectivity checks — plain language first, then a network evidence lab."
difficulty: beginner
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
technology: linux
module: "Module 9 · Linux Networking"
tags:
  - linux
  - ip
  - ss
  - dns
  - networking
  - beginners
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

Before you blame the application, prove the network path: addresses, routes, open ports, and DNS.

When an app “cannot connect”, you need a clear order of checks on the **host itself**: Do I have an IP address? Is anything **listening** on the port? Does **Domain Name System (DNS)** resolve the name? Does **TCP** reach the remote service?

**Plain problem:** A junior opens a ticket “site down.” Senior asks: “Can the VM ping the gateway? Does `ss` show nginx on 443? Does `dig` return an A record?” This tutorial teaches that checklist from zero.

This is **Tutorial 14** in **Module 9: Linux Networking** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — practical Linux for Cloud and DevOps work.

## Prerequisites

- [LVM, Swap, and Disk Monitoring](lvm-swap-and-disk-monitoring.md)
- A practice Ubuntu 22.04/24.04 VM with `sudo`
- Outbound DNS and HTTPS allowed (lab uses public resolvers and `example.com`)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain IP address, route, listening socket, and DNS in plain words
- [ ] Inspect interfaces and routes with `ip`
- [ ] List listening ports with `ss` (modern replacement for netstat)
- [ ] Test DNS with `dig` and HTTP with `curl`
- [ ] Build a network evidence pack under `~/rebash-linux/lab14`
- [ ] Answer common fresher interview questions on Linux networking

## Architecture

Applications use sockets. The kernel routes packets via interfaces. DNS resolves names to IPs before TCP connections.

![Linux networking stack — app, socket, kernel, interface](../assets/excalidraw/linux-networking-stack.svg)

## Theory

### The problem (before any jargon)

Your web app returns “connection refused.” Is nginx down? Wrong port? Firewall? Or DNS pointing to a dead IP? Random guessing wastes hours. You follow a **layered checklist** on the host, then escalate to cloud security groups if the host looks healthy.

### Layered checklist (simple words)

**Analogy:** Fixing water flow — check the tap (local IP), the pipes in the house (routes), whether the outlet is open (listening port), whether the address book has the right street (DNS), then whether water reaches the neighbour (TCP/HTTP).

| Step | Question | Tool |
|------|----------|------|
| 1 | Do I have an IP? | `ip addr`, `ip -br a` |
| 2 | Can I reach the gateway? | `ip route`, `ping gateway` |
| 3 | Is my service listening? | `ss -tlnp` |
| 4 | Does the name resolve? | `dig`, `getent hosts` |
| 5 | Does TCP/HTTP work? | `curl`, `nc` |

**What you can say in an interview:** “I go link/IP → route → listen sockets → DNS → application protocol — host first, then cloud firewall.”

### ip — addresses and routes

``` {.bash .ra-terminal title="Terminal"}
ip -br addr show
ip route show
ip link show
```

**Interview line:** “Prefer `ip` over legacy `ifconfig` on modern Ubuntu/RHEL images.”

### ss — sockets and listeners

``` {.bash .ra-terminal title="Terminal"}
ss -tlnp              # TCP listen, numeric, process
ss -unp               # UDP
ss -tan state established | head
```

**Interview line:** “`ss -tlnp` tells me if the app bound to 0.0.0.0:8080 or only 127.0.0.1 — a classic ‘works locally, fails remotely’ bug.”

### DNS — dig and getent

``` {.bash .ra-terminal title="Terminal"}
dig +short example.com A
dig +short google.com A @1.1.1.1
getent hosts example.com
```

**Interview line:** “If `dig @1.1.1.1` works but default fails, suspect `/etc/resolv.conf` or systemd-resolved.”

### curl and nc — application probes

``` {.bash .ra-terminal title="Terminal"}
curl -I --max-time 5 https://example.com
nc -zv 127.0.0.1 22
```

### ping and traceroute caveats

``` {.bash .ra-terminal title="Terminal"}
ping -c 3 1.1.1.1
tracepath example.com
```

Many cloud firewalls **block Internet Control Message Protocol (ICMP)** ping — TCP can still work. Do not treat “ping failed” as definitive proof the host is dead.

### Common pitfalls

- Using deprecated `ifconfig` / `netstat` only — install `iproute2` tools
- Assuming ping failure means total outage
- Ignoring `127.0.0.1` vs `0.0.0.0` bind addresses
- Skipping DNS when curl fails on hostname but works on IP

## Hands-on Lab

### Objective

Collect a standard network evidence pack: IP, routes, listeners, DNS, HTTP header — like an incident ticket attachment.

### Prerequisites

| Item | Notes |
|------|--------|
| Ubuntu VM | Network connected |
| `dnsutils` optional | `dig` — often preinstalled |
| `curl` | Usually preinstalled |

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab14 && cd ~/rebash-linux/lab14
```

### Real-world scenario

Production alert: “API unreachable from load balancer.” Before changing security groups, on-call collects host-side evidence. You practise that pack on your lab VM.

### Step-by-step tasks

#### Task 1 – Link and IP snapshot

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab14
ip -br addr show | tee ip-addr.txt
ip route show | tee ip-route.txt
hostname -I | tee hostname-ips.txt
test -s ip-addr.txt && test -s ip-route.txt
grep -q default ip-route.txt || echo "no default route — note for ticket" | tee route-note.txt
```

!!! example "Expected output"
    `ip-addr.txt` lists interfaces (e.g. `eth0`, `lo`) with IP addresses. `ip-route.txt` usually includes a `default via` line.


#### Task 2 – Listening ports and SSH proof

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab14
ss -tlnp | tee ss-listen.txt
grep -E ':22|:53|:443' ss-listen.txt | tee ss-key-ports.txt || true
ss -tlnp | grep -q ':22' && echo "ssh listening" | tee ssh-listen.txt
test -s ss-listen.txt
```

!!! example "Expected output"
    `ss-listen.txt` shows TCP listeners. On a typical SSH-enabled VM, port 22 appears with `sshd`.


#### Task 3 – DNS resolution

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab14
dig +short example.com A | tee dig-example.txt
getent hosts example.com | tee getent-example.txt
test -s dig-example.txt || test -s getent-example.txt
cat dig-example.txt
```

!!! example "Expected output"
    `dig-example.txt` contains one or more IPv4 addresses for `example.com`.


#### Task 4 – HTTP probe and gateway ping

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab14
curl -I --max-time 10 https://example.com 2>&1 | tee curl-example.txt
GW="$(ip route | awk '/default/ {print $3; exit}')"
if [ -n "$GW" ]; then ping -c 2 -W 2 "$GW" | tee ping-gateway.txt; else echo "no gateway to ping" | tee ping-gateway.txt; fi
grep -qiE 'HTTP/|curl:' curl-example.txt
echo "lab14 network OK" | tee evidence.txt
```

!!! example "Expected output"
    `curl-example.txt` shows HTTP response headers (e.g. `HTTP/2 200` or redirect). Gateway ping may succeed or be blocked — note either way in ticket style.


### Validation steps

- [ ] IP, route, and listener files exist
- [ ] DNS returned addresses for example.com
- [ ] curl returned HTTP headers within timeout
- [ ] You can explain the checklist order without notes

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `dig: command not found` | Package missing | `sudo apt install dnsutils` |
| curl timeout | No outbound HTTPS | Check proxy/firewall; try HTTP test host |
| Empty ss output | Wrong flags | Use `ss -tlnp` with sudo for process names |
| ping 100% loss to gateway | ICMP blocked | Use TCP test (`curl`, `nc`) instead |

### Challenge exercise

Start a temporary Python HTTP server on port 8765, prove listen with `ss`, curl it locally, then stop.

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab14
python3 -m http.server 8765 >/tmp/lab14-http.log 2>&1 &
srv_pid=$!
echo "$srv_pid" | tee http-server.pid
sleep 1
ss -tlnp | grep 8765 | tee ss-lab-server.txt
curl -I --max-time 3 http://127.0.0.1:8765/ | tee curl-local.txt
kill "$srv_pid"
grep -q 8765 ss-lab-server.txt
```

### Learning outcomes

- You built a reusable network evidence pack
- You distinguished listen socket vs remote connectivity
- You know when ping lies but curl tells the truth

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab14
if [ -f http-server.pid ]; then kill "$(cat http-server.pid)" 2>/dev/null || true; rm -f http-server.pid; fi
pkill -f 'python3 -m http.server 8765' 2>/dev/null || true
# Keep evidence txt files for revision
```

## Validation

- [ ] Lab completed under `~/rebash-linux/lab14`
- [ ] Can run the five-step checklist on a new host
- [ ] Ready for SSH and remote access next

## Code Walkthrough

1. **`ip -br a`** — quick interface summary for tickets.
2. **`ss -tlnp`** — listening ports + processes; sudo for full process names.
3. **`dig +short`** — minimal DNS answer; specify `@resolver` to isolate resolver bugs.
4. **`curl -I`** — headers only, fast HTTP sanity check.
5. **Save outputs with `tee`** — attach files to tickets instead of screenshots alone.

## Security Considerations

- `ss -tlnp` may expose internal services — redact in external tickets.
- tcpdump captures may contain credentials — restrict capture files.
- Do not disable host firewalls blindly to “make ping work”.
- Public DNS queries leak looked-up names — acceptable for lab, mind policy in prod.
- Verify you test the correct namespace on containers (network namespace differs).

## Common Mistakes

!!! warning "ifconfig/netstat only"
    Missing modern counters and cgroup-aware data. Fix: learn `ip` and `ss`.

!!! warning "Service bound to 127.0.0.1"
    Works on VM locally, fails from load balancer. Fix: bind `0.0.0.0` or correct interface; confirm with `ss`.

!!! warning "Ping failed = host down"
    ICMP often blocked. Fix: test TCP port and HTTP with curl.

!!! warning "Ignoring DNS"
    curl works on IP but fails on hostname. Fix: compare `dig` vs `getent`; check resolv.conf.

## Best Practices

- Standardise an “network evidence” script in your team runbooks
- Capture before and after firewall or route changes
- Use `curl --resolve` to test virtual hosts without DNS
- Document default gateway and resolver in host inventory
- Escalate to cloud SG/NACL only after host-side checks pass

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Connection refused | Nothing listening on port | Start service; check `ss -tlnp` |
| Connection timed out | Firewall or wrong IP/route | `ip route`; cloud SG; traceroute |
| Name or service not known | DNS failure | `dig`; fix resolv.conf or systemd-resolved |
| Slow HTTP only | App or TLS issue | `curl -v`; check certs and upstream |

## Summary

Use **`ip`** for addresses/routes, **`ss`** for listeners, **`dig`** for DNS, **`curl`** for HTTP — in that order before blaming the cloud firewall. You built an evidence pack for tickets. Next: **SSH and remote access**.

## Interview Questions

**1. What is the first thing you check when a server cannot reach the internet?**

??? success "Reveal answer"
    On the host: **`ip addr`** and **`ip route`** — confirm IP and default gateway exist. Then test gateway or external IP with ping (knowing ICMP may be blocked) and TCP checks like **`curl`**. Only then escalate to cloud firewall or upstream routing.

**2. What is the difference between ip and ifconfig?**

??? success "Reveal answer"
    **`ip`** (iproute2) is the modern tool for addresses, links, routes, and rules — maintained and script-friendly. **`ifconfig`** (net-tools) is legacy; many minimal/cloud images omit it. Prefer `ip` in runbooks and interviews.

**3. How do you see which process listens on port 8080?**

??? success "Reveal answer"
    **`ss -tlnp | grep :8080`** or **`sudo ss -tlnp sport = :8080`**. Shows local address (127.0.0.1 vs 0.0.0.0) and process name/PID. Confirms whether the app is running and bound correctly.

**4. dig works with @1.1.1.1 but not without — what does that suggest?**

??? success "Reveal answer"
    The host’s **configured resolver** (in `/etc/resolv.conf` or **systemd-resolved**) is broken or unreachable, while public DNS is fine. Fix local resolver config or stub listener — not the application.

**5. Why might ping fail but curl succeed?**

??? success "Reveal answer"
    **ICMP** (ping) is often blocked by firewalls or cloud security policies, while **TCP port 443** (HTTPS) is allowed. Ping failure does not prove the remote host is down — test the actual protocol you need.

**6. What does LISTEN 0.0.0.0:22 mean in ss output?**

??? success "Reveal answer"
    A process is **listening on all IPv4 interfaces** on port 22 (typically sshd). **`127.0.0.1:8080`** would mean only local connections — common misconfiguration for services that must accept external load balancer traffic.

**7. How do you test DNS without changing application config?**

??? success "Reveal answer"
    **`dig hostname A`**, **`getent hosts hostname`**, or **`curl --resolve example.com:443:1.2.3.4 https://example.com`** to force an IP while sending the correct Host header/SNI — isolates DNS from HTTP/app layers.

## Related Tutorials

- Prior: [LVM, Swap, and Disk Monitoring](lvm-swap-and-disk-monitoring.md)
- Next: [SSH and Remote Access](ssh-and-remote-access.md)
- Lab: [Linux ops toolkit](../labs/linux-ops-toolkit-lab.md)

## References

- [ip-route(8) documentation](https://man7.org/linux/man-pages/man8/ip-route.8.html)
- [ss(8) man page](https://man7.org/linux/man-pages/man8/ss.8.html)
- [dig(1) man page](https://man7.org/linux/man-pages/man1/dig.1.html)
- [REBASH Linux course index](index.md)
