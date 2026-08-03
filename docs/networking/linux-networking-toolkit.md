---
title: "Linux Networking Toolkit"
description: "Use ip, ss, dig, traceroute/tracepath, and curl as one diagnostic toolkit, and produce a reusable evidence tarball for networking incidents."
difficulty: intermediate
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: networking
technology: networking
module: "Module 12 · Linux Networking"
tags:
  - networking
  - linux
  - ip
  - ss
  - dig
  - curl
prerequisites:
  - networking/firewalls-and-access-control
next:
  - networking/load-balancing-fundamentals
related:
  - linux/linux-networking-tools
  - networking/packet-analysis-tcpdump-wireshark
  - networking/network-troubleshooting-methodology
interview: interview/networking
comments: false
---

# Linux Networking Toolkit

## Overview

When an application “cannot connect”, the console shows a symptom. The **Linux networking toolkit** shows the truth on the host: addresses, routes, sockets, Domain Name System (DNS), path, and Hypertext Transfer Protocol (HTTP). The core tools are `ip`, `ss`, `dig` (or `host`), `traceroute`/`tracepath`, and `curl`.

Operators who jump randomly between tools waste time. A fixed order — **identity → route → port → DNS → HTTP → path** — turns panic into a checklist. In this tutorial you will run that sequence and wrap it in a small script that builds an **evidence tarball** under `~/rebash-networking/lab15` for tickets and post-incident reviews.

Cloud agents, Kubernetes nodes, and Continuous Integration (CI) runners are still Linux underneath. The same commands work on a practice Ubuntu VM and on a production bastion (with care about captures and secrets). Prefer modern tools (`ip` over deprecated `ifconfig`, `ss` over `netstat` when available).

This is the core tutorial in **Module 12: Linux Networking** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series. It is written for DevOps, Cloud, SRE, and platform engineers.

## Prerequisites

- [Firewalls and Access Control](firewalls-and-access-control.md)
- Comfort with [Routing Fundamentals](routing-fundamentals.md) and [DNS Fundamentals](dns-fundamentals.md)
- Ubuntu practice VM with network access (lab uses public DNS-friendly targets; replace if offline)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Inspect addresses and routes with `ip`
- [ ] List listening and established sockets with `ss`
- [ ] Query DNS with `dig` and explain the answer section
- [ ] Probe reachability with `ping` and path with `traceroute`/`tracepath`
- [ ] Debug HTTP with `curl -v` / `-I`
- [ ] Run a cohesive diagnostic script that produces an evidence tarball

## Architecture

Each tool interrogates a layer of the local stack and the path beyond. Your script collects the same layers into one artefact for humans and tickets.

![Architecture diagram for Linux Networking Toolkit](../assets/excalidraw/linux-networking-stack.svg)

## Theory

### What it is

| Tool | Question it answers |
|------|---------------------|
| `ip addr` / `ip route` | Who am I on the network, and where do packets go next? |
| `ss` | What is listening, and what is connected? |
| `dig` / `host` | Does the name resolve, and to which records? |
| `ping` | Does Internet Control Message Protocol (ICMP) echo work? |
| `traceroute` / `tracepath` | Where does the path fail or slow down? |
| `curl` | Does the application protocol succeed (HTTP status, TLS)? |

``` {.bash .ra-terminal title="Terminal"}
ip -br addr
ip route
ss -lntu
dig +short example.com A
```

### Why it matters

Incidents often mix DNS, firewall, and application failures. Without a toolkit order, teams bounce between “restart the pod” and “flush DNS” with no evidence. A tarball of command output is what on-call and vendors ask for. It also trains juniors to show proof, not guesses.

### How it works

1. **Identity** — hostname, `ip -br addr`, default route.  
2. **Sockets** — `ss -lntup` (needs sudo for process names).  
3. **DNS** — `dig` against a known name; note server and status.  
4. **Path** — `ping -c 3`, then `tracepath` or `traceroute`.  
5. **App** — `curl -I` / `curl -v` to the URL.  
6. **Pack** — tar the text outputs for the ticket.

``` {.bash .ra-terminal title="Terminal"}
curl -sS -o /dev/null -w '%{http_code}\n' https://example.com/
```

### Key concepts and comparisons

| Old habit | Prefer | Why |
|-----------|--------|-----|
| `ifconfig` | `ip addr` | Maintained, scriptable |
| `netstat` | `ss` | Faster, modern |
| `nslookup` only | `dig` | Clear sections, scripting |
| Random `tcpdump` first | Toolkit then capture | Narrow the filter |

### Common pitfalls

- Trusting `ping` alone (ICMP may be blocked while TCP works).  
- Forgetting `sudo` on `ss -p` and misreading process owners.  
- Using `curl` without `-v` when TLS or redirects matter.  
- Pasting secrets from `curl -v` Authorization headers into tickets.  
- Running long `tcpdump` on production without a filter or time limit.

## Hands-on Lab

### Objective

Build and run `netdiag.sh` that collects `ip`, `ss`, `dig`, path, and `curl` evidence into `evidence.tgz` under `~/rebash-networking/lab15`.

### Prerequisites

- Ubuntu with `iproute2`, `iputils-ping`, `curl`
- `dnsutils` (`dig`) recommended: `sudo apt-get update && sudo apt-get install -y dnsutils`
- `iputils-tracepath` or `traceroute` (script falls back gracefully)

### Lab environment

Workspace: `~/rebash-networking/lab15`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-networking/lab15 && cd ~/rebash-networking/lab15
set -euo pipefail
whoami | tee admin-user.txt
uname -a | tee uname.txt
```

!!! example "Expected output"
    workspace exists; identity files written.


### Real-world scenario

A teammate reports “the API is down”. You are on a jump host and must produce a structured evidence pack in five minutes: addresses, sockets, DNS, path, and HTTP headers — without changing production config.

### Step-by-step tasks

#### Task 1 – Manual toolkit pass

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-networking/lab15
set -euo pipefail

ip -br addr | tee 01-ip-addr.txt
ip route show | tee 02-ip-route.txt
ss -lntu | tee 03-ss-listen.txt

if command -v dig >/dev/null 2>&1; then
  dig example.com A +noall +answer | tee 04-dig.txt
else
  getent hosts example.com | tee 04-dig.txt
fi

ping -c 3 example.com 2>&1 | tee 05-ping.txt || true

if command -v tracepath >/dev/null 2>&1; then
  tracepath -n example.com 2>&1 | head -n 20 | tee 06-path.txt || true
elif command -v traceroute >/dev/null 2>&1; then
  traceroute -n -m 10 example.com 2>&1 | tee 06-path.txt || true
else
  echo "no traceroute/tracepath" | tee 06-path.txt
fi

curl -sSI --max-time 10 https://example.com/ 2>&1 | tee 07-curl-headers.txt || true
```

!!! example "Expected output"
    files `01`–`07` exist; dig/curl may vary with network policy but commands must run.


#### Task 2 – Cohesive diagnostic script

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-networking/lab15
set -euo pipefail
```

Create `netdiag.sh`:

```bash title="netdiag.sh"
#!/usr/bin/env bash
set -euo pipefail
TARGET_HOST="${1:-example.com}"
TARGET_URL="${2:-https://example.com/}"
OUT="${3:-./diag-out}"
mkdir -p "$OUT"
{
  echo "ts=$(date -Is)"
  echo "host=$(hostname)"
  echo "target_host=$TARGET_HOST"
  echo "target_url=$TARGET_URL"
} | tee "$OUT/meta.txt"

ip -br addr | tee "$OUT/ip-addr.txt"
ip route | tee "$OUT/ip-route.txt"
ss -lntu | tee "$OUT/ss-listen.txt"
(ss -s 2>/dev/null || true) | tee "$OUT/ss-summary.txt"

if command -v dig >/dev/null 2>&1; then
  dig "$TARGET_HOST" A +noall +answer +stats | tee "$OUT/dig.txt"
else
  getent hosts "$TARGET_HOST" | tee "$OUT/dig.txt"
fi

ping -c 3 "$TARGET_HOST" 2>&1 | tee "$OUT/ping.txt" || true

if command -v tracepath >/dev/null 2>&1; then
  tracepath -n "$TARGET_HOST" 2>&1 | head -n 25 | tee "$OUT/path.txt" || true
elif command -v traceroute >/dev/null 2>&1; then
  traceroute -n -m 12 "$TARGET_HOST" 2>&1 | tee "$OUT/path.txt" || true
else
  echo "path-tool=missing" | tee "$OUT/path.txt"
fi

curl -sSI --max-time 15 "$TARGET_URL" 2>&1 | tee "$OUT/curl-head.txt" || true
curl -sS -o /dev/null -w 'http_code=%{http_code} time=%{time_total}\n' \
  --max-time 15 "$TARGET_URL" 2>&1 | tee "$OUT/curl-timing.txt" || true

tar -czf "$OUT/../evidence.tgz" -C "$OUT" .
ls -l "$OUT/../evidence.tgz"
```

``` {.bash .ra-terminal title="Terminal"}
chmod +x netdiag.sh
./netdiag.sh example.com https://example.com/ ./diag-out
test -s evidence.tgz
ls -l evidence.tgz | tee evidence-ls.txt
```

!!! example "Expected output"
    `netdiag.sh` is executable; `evidence.tgz` is non-empty.


#### Task 3 – Quick asserts on the pack

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-networking/lab15
set -euo pipefail

tar -tzf evidence.tgz | tee evidence-list.txt
grep -E 'ip-addr|ss-listen|dig|curl' evidence-list.txt
test -f netdiag.sh
```

!!! example "Expected output"
    tarball listing includes the core artefact names.


### Validation steps

- [ ] Manual `01`–`07` files exist
- [ ] `./netdiag.sh` runs without syntax errors
- [ ] `evidence.tgz` lists `ip-addr.txt`, `ss-listen.txt`, DNS and curl outputs
- [ ] You can explain the toolkit order from memory

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `dig: command not found` | `dnsutils` missing | `sudo apt-get install -y dnsutils` or use `getent` |
| `ping: Name or service not known` | DNS/offline | Use an IP target or fix resolvers (`resolvectl status`) |
| Empty `curl` output | Proxy/TLS/firewall | Read `curl-head.txt` errors; try `-v` offline notes |
| `ss` shows no process | Need sudo for `-p` | Optional: `sudo ss -lntup` |

### Challenge exercise

Extend `netdiag.sh` to accept `TARGET_HOST` and write an extra `ss -tn state established | head` snapshot to `ss-established.txt` inside the tarball. Re-run and confirm the new file appears in `tar -tzf evidence.tgz`.

### Learning outcomes

- Ran a fixed triage order with modern Linux tools
- Built a reusable `netdiag.sh` evidence producer
- Separated ICMP path checks from HTTP success
- Produced a ticket-ready `evidence.tgz`

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-networking/lab15
# Keep netdiag.sh and evidence.tgz for your notes; remove temp dir if desired:
# rm -rf diag-out
# Optional: rm -f 0*.txt
```

## Validation

- [ ] Lab finished under `~/rebash-networking/lab15/`
- [ ] You can run the toolkit without looking up every flag
- [ ] You know when ping lies and curl tells the truth
- [ ] You redact secrets before sharing tarballs

## Code Walkthrough

Production triage often looks like:

1. **Confirm the host** — right VM/pod node?  
2. **`ip` / route** — wrong interface or missing default route  
3. **`ss`** — nothing listening / wrong port  
4. **`dig`** — wrong answer or SERVFAIL  
5. **`curl`** — TLS, HTTP status, redirects  
6. **Path / capture** — only if still unclear  

Your script should stay **read-only**. Never put passwords in command lines that land in shell history or tarballs.

## Security Considerations

- Redact `Authorization` and cookie headers from `curl -v` before sharing  
- Avoid unrestricted `tcpdump` on production without change control  
- Prefer least privilege: diagnostics rarely need permanent root shells  
- Do not disable firewalls “to test” on shared hosts  
- Store evidence in ticket systems with proper access control  

## Common Mistakes

!!! warning "Declaring the network down because ping failed"
    Many networks block ICMP. **Fix:** test the real TCP/TLS port with `curl` or `nc`.

!!! warning "Skipping DNS when the URL ‘looks fine’"
    Stale or split-horizon DNS is common. **Fix:** always `dig` the exact hostname clients use.

!!! warning "Pasting full `curl -v` with tokens into Slack"
    Secrets leak. **Fix:** scrub headers; share status lines and timings.

!!! warning "Changing sysctl during first triage"
    You destroy evidence and may cause outages. **Fix:** collect first; change only with rollback.

## Best Practices

- Keep a personal `netdiag.sh` and version it in your team’s runbooks  
- Use the same order every time  
- Capture timestamps and hostname in every pack  
- Prefer `ss` and `ip` on modern distros  
- Escalate to packet capture only after toolkit gaps remain  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| No default route | DHCP/VPC misconfig | Fix route/gateway |
| Listen socket missing | App down / wrong ns | Restart app; check netns/containers |
| DNS SERVFAIL | Resolver/policy | Try alternate resolver; check `/etc/resolv.conf` |
| HTTP 502/504 | Upstream/proxy | Move to load balancer / reverse proxy modules |
| Tracepath all `*` | ICMP filtered | Rely on TCP/`curl`; ask network team |

## Summary

The Linux networking toolkit turns vague “network issues” into layered evidence. Master `ip`, `ss`, `dig`, path tools, and `curl`, then automate the pack. Next, apply traffic distribution ideas in [Load Balancing Fundamentals](load-balancing-fundamentals.md).

## Interview Questions

**1. Walk through your first five commands on a host where users say “the site is down”.**

??? success "Reveal answer"
    Typical order: `ip -br addr` and `ip route` (identity/routing), `ss -lntu` (listen ports), `dig` for the hostname, `curl -I` to the URL, then path (`tracepath`/`traceroute`) if still unclear. Interviewers want a **stable method**, not a random tool dump.

**2. Why might `ping` fail while `curl https://service` works?**

??? success "Reveal answer"
    ICMP echo can be **blocked** by firewalls while TCP 443 is allowed. Ping proves only ICMP reachability. Always test the application protocol and port that clients use.

**3. What is the difference between `dig` and `getent hosts` for troubleshooting?**

??? success "Reveal answer"
    **`dig`** queries DNS directly and shows records/status/server. **`getent hosts`** uses the Name Service Switch (NSS) path (`files`, DNS, possibly others) — closer to what some apps resolve, but less detailed. Use both when results disagree.

**4. How do you get the process holding a port on Linux?**

??? success "Reveal answer"
    `sudo ss -lntup` (or `ss -lntup`) shows the process (PID/program) for listening sockets. `lsof -i :port` is an alternative. Without privileges, process columns may be blank.

**5. What belongs in a networking evidence tarball for a vendor ticket?**

??? success "Reveal answer"
    Timestamp, hostname, `ip addr`/`ip route`, `ss` listen/summary, DNS answer for the failing name, ping/path if allowed, and `curl -I`/`-w` timings — **with secrets redacted**. Avoid huge unfiltered packet captures unless requested.

**6. When do you escalate from this toolkit to `tcpdump`?**

??? success "Reveal answer"
    When sockets, DNS, and HTTP still disagree with client reports — for example TCP SYN seen but no ACK, or TLS alerts. Use a **tight filter** and short duration. Toolkit first keeps captures small and purposeful.

**7. `ip route` shows a default via the wrong gateway after a cloud change. What is the user impact?**

??? success "Reveal answer"
    Packets leave via the wrong next hop: blackholes, asymmetric paths, or wrong NAT. Apps may hang or become one-way. Fix the route table/DHCP options/cloud route, then re-validate with `ip route` and `curl`.

## Related Tutorials

- [Networking for Cloud & DevOps – Overview](index.md)
- [Firewalls and Access Control](firewalls-and-access-control.md) *(previous)*
- [Load Balancing Fundamentals](load-balancing-fundamentals.md) *(next)*
- [Packet Analysis with tcpdump and Wireshark](packet-analysis-tcpdump-wireshark.md)
- [Linux networking tools (Linux track)](../linux/linux-networking-tools.md)

## References

- [`ip(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/ip.8.html) — iproute2  
- [`ss(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/ss.8.html) — sockets  
- [dig — BIND9](https://manpages.ubuntu.com/manpages/jammy/en/man1/dig.1.html) — DNS queries  
- Track index: [Networking for Cloud & DevOps Engineers](index.md)
