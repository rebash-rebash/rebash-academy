---
title: DNS Fundamentals
description: Understand DNS hierarchy, recursive vs iterative resolution, resolvers, /etc/hosts overrides, and hands-on labs with dig and nslookup.
difficulty: beginner
estimated_time: "40 min"
author: Shaik Basha
category: networking
tags:
  - networking
  - dns
  - dig
  - nslookup
  - resolvers
  - nameservers
prerequisites:
  - Complete TCP and UDP Deep Dive or understand ports and UDP transport
  - Linux environment with outbound UDP/TCP 53 access
  - Basic understanding of IP addresses and hostnames
comments: false
---

# DNS Fundamentals

## Overview

**DNS (Domain Name System)** is the distributed phone book of the internet. Every `curl`, browser request, database connection string, and Kubernetes service lookup depends on translating human-readable names like `api.example.com` into IP addresses. When DNS breaks, everything looks like a network outage — even when routing and firewalls are fine.

This tutorial is **Tutorial 8** in **Module 3: Transport & DNS** of the REBASH Academy Networking series. You will learn the hierarchical namespace, the difference between recursive and iterative queries, how Linux resolves names, and how to debug with **`dig`** and **`nslookup`**. For Linux resolver configuration overlap, see [Linux Networking Essentials](../linux/linux-networking-essentials.md); here we focus on DNS architecture and query mechanics.

## Prerequisites

- Complete [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md) or understand UDP/TCP port 53
- Linux VM or cloud instance with network access
- `dig` and `nslookup` installed (`sudo apt install dnsutils` on Debian/Ubuntu)
- Optional: access to modify `/etc/hosts` for lab exercises

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the DNS hierarchy from root to authoritative nameservers
- [ ] Distinguish recursive vs iterative DNS queries
- [ ] Describe the role of stub resolvers, recursive resolvers, and caching
- [ ] Configure and inspect `/etc/hosts`, `/etc/resolv.conf`, and systemd-resolved
- [ ] Perform lookups with `dig` and interpret query flags and sections
- [ ] Trace resolution paths with `dig +trace` for delegation debugging

## Architecture Diagram

```d2
direction: down

Client: Client {
        APP: Application
        STUB: "Stub Resolver\nglibc / systemd-resolved"
    }
    Resolver: Resolver {
        REC: "Recursive Resolver\n8.8.8.8 / corporate DNS"
        CACHE: "Local Cache"
    }
    Authoritative: Authoritative {
        ROOT: "Root ."
        TLD: "TLD .com"
        AUTH: "Auth NS\nexample.com"
    }
    Client.APP -> Client.STUB
    Client.STUB -> Resolver.REC
    Resolver.REC -> Resolver.CACHE
    Resolver.REC -> Authoritative.ROOT: iterative
    Authoritative.ROOT -> Authoritative.TLD: referral
    Authoritative.TLD -> Authoritative.AUTH: referral
    Authoritative.AUTH -> Resolver.REC: answer
    Resolver.REC -> Client.STUB
    Client.STUB -> Client.APP
```

## Theory

### Why DNS Exists

IP addresses change — load balancers fail over, CDNs rotate edges, autoscaling adds nodes. DNS provides a **stable name** that maps to current addresses. Applications call `getaddrinfo()`; the resolver handles the rest.

DNS messages are typically **UDP port 53** for queries under 512 bytes (4096 with EDNS0). Large responses or zone transfers use **TCP 53**.

### The DNS Namespace Hierarchy

Domains are read **right to left**, ending with the implicit root `.`:

```text
www.api.example.com.
│   │   │       │   └── root (usually omitted)
│   │   │       └────── TLD: com
│   │   └────────────── domain: example
│   └────────────────── subdomain: api
└────────────────────── host: www
```

| Level | Example | Operator |
|-------|---------|----------|
| Root | `.` | Root server operators (13 logical clusters) |
| TLD | `.com`, `.org`, `.io` | Registries (Verisign, etc.) |
| Domain | `example.com` | Registrant / organization |
| Subdomain | `api.example.com` | Domain owner via NS delegation |

**Delegation** happens through **NS records** at each level. Parent zone says "ask these nameservers for child zone."

### Query Types: Recursive vs Iterative

| Type | Who performs | Behavior |
|------|--------------|----------|
| **Recursive** | Resolver on client's behalf | Client asks resolver; resolver chases referrals until final answer or NXDOMAIN |
| **Iterative** | Each server in chain | Server returns best answer or referral to next level; querier continues |

Your laptop's configured nameserver (8.8.8.8, corporate DNS, `127.0.0.53`) is typically a **recursive resolver**. Root and TLD servers respond **iteratively** — they don't chase queries for clients.

**Stub resolver** (in glibc, musl, or systemd-resolved) forwards queries to the recursive resolver listed in `/etc/resolv.conf`. It does not implement full recursion itself.

### Caching and TTL

Resolvers cache answers based on **TTL (Time To Live)** from records. Short TTL (60s) enables fast failover; long TTL (86400s) reduces query load but slows propagation after changes.

Negative answers (NXDOMAIN — name doesn't exist) also cache with **negative TTL** from SOA record.

### Linux Name Resolution Order

`/etc/nsswitch.conf` controls lookup order:

```text
hosts: files dns myhostname
```

1. **`files`** — check `/etc/hosts` first
2. **`dns`** — query resolver via `/etc/resolv.conf`
3. **`myhostname`** — systemd local hostname resolution

This explains why a stale `/etc/hosts` entry breaks DNS testing even when `dig` returns correct answers — `dig` bypasses nsswitch and talks directly to DNS servers.

### Key Configuration Files

| File | Purpose |
|------|---------|
| `/etc/hosts` | Static name-to-IP overrides |
| `/etc/resolv.conf` | Nameserver list, search domains, options |
| `/etc/nsswitch.conf` | Resolution order (`files`, `dns`) |
| `/run/systemd/resolve/stub-resolv.conf` | systemd-resolved stub (127.0.0.53) |

On systemd systems, `/etc/resolv.conf` may be a symlink — edit via **netplan**, **NetworkManager**, or **`resolvectl`**, not manual overwrite.

### dig Output Sections

```text
;; QUESTION SECTION:   — what was asked
;; ANSWER SECTION:     — direct answer records
;; AUTHORITY SECTION:  — nameservers for the zone
;; ADDITIONAL SECTION: — glue records (A/AAAA for NS hostnames)
```

Flags: **`qr`** query/response, **`aa`** authoritative answer, **`rd`** recursion desired, **`ra`** recursion available, **`ad`** authenticated data (DNSSEC).

## Hands-on Lab

### Step 1 – Basic lookup with dig

**Command:**

```bash
dig example.com A +noall +answer
dig example.com AAAA +short
```

**Explanation:** `+noall +answer` shows only answer section. `+short` returns IP only — good for scripts.

**Expected output:**

```text
example.com.    3600    IN    A    93.184.216.34
```

### Step 2 – Full dig output interpretation

**Command:**

```bash
dig example.com
```

**Explanation:** Study HEADER flags, QUESTION, ANSWER, AUTHORITY sections. Note TTL and IN (Internet) class.

**Expected output:**

```text
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12345
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; QUESTION SECTION:
;example.com.                   IN      A
;; ANSWER SECTION:
example.com.    3600    IN      A       93.184.216.34
```

### Step 3 – Query specific nameserver

**Command:**

```bash
dig @8.8.8.8 example.com A +short
dig @1.1.1.1 example.com A +short
dig @ns1.example.com example.com A 2>&1 | tail -5
```

**Explanation:** `@server` targets a specific resolver or authoritative NS. Last command may fail if `ns1.example.com` isn't real — demonstrates syntax.

**Expected output:**

```text
93.184.216.34
93.184.216.34
```

### Step 4 – Trace delegation chain

**Command:**

```bash
dig +trace example.com A | tail -30
```

**Explanation:** Simulates iterative resolution from root downward. Essential for "works in one region, not another" debugging.

**Expected output:**

```text
.                       518400  IN      NS      a.root-servers.net.
...
com.                    172800  IN      NS      a.gtld-servers.net.
...
example.com.            3600    IN      A       93.184.216.34
```

### Step 5 – nslookup comparison

**Command:**

```bash
nslookup example.com
nslookup -type=MX example.com 8.8.8.8
```

**Explanation:** `nslookup` is interactive and legacy but still common. `-type` selects record type.

**Expected output:**

```text
Server:     127.0.0.53
Address:    127.0.0.53#53

Name:   example.com
Address: 93.184.216.34
```

### Step 6 – /etc/hosts override lab

**Command:**

```bash
grep example.com /etc/hosts || true
echo "127.0.0.99 example.com" | sudo tee -a /etc/hosts
getent hosts example.com
dig +short example.com A
curl -s -o /dev/null -w "%{http_code}\n" --connect-timeout 2 http://example.com || true
sudo sed -i '/127.0.0.99 example.com/d' /etc/hosts
```

**Explanation:** `getent` uses nsswitch (sees hosts file); `dig` queries DNS directly. Demonstrates split behavior.

**Expected output:**

```text
127.0.0.99      example.com
93.184.216.34
000  (or connection failure — curl tried 127.0.0.99)
```

### Step 7 – Inspect resolver configuration

**Command:**

```bash
cat /etc/resolv.conf
resolvectl status 2>/dev/null | head -30
cat /etc/nsswitch.conf | grep ^hosts
```

**Explanation:** Identifies upstream DNS, search domains, and lookup order.

**Expected output:**

```text
nameserver 127.0.0.53
options edns0 trust-ad
search ec2.internal us-west-2.compute.internal
hosts: files dns myhostname
```

### Step 8 – Reverse lookup intro

**Command:**

```bash
dig +short -x 8.8.8.8
dig +short -x 93.184.216.34
```

**Explanation:** `-x` performs reverse PTR lookup (IP → name). Requires PTR records in `in-addr.arpa` zones.

**Expected output:**

```text
dns.google.
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `dig DOMAIN TYPE` | Standard DNS lookup | `dig example.com A` |
| `dig +short DOMAIN` | Answer only | `dig +short google.com` |
| `dig @NS DOMAIN` | Query specific server | `dig @8.8.8.8 example.com` |
| `dig +trace DOMAIN` | Trace delegation from root | `dig +trace example.com` |
| `dig -x IP` | Reverse PTR lookup | `dig -x 10.0.0.1` |
| `dig +noall +answer` | Minimal output | Script-friendly |
| `nslookup DOMAIN` | Legacy lookup | `nslookup example.com` |
| `getent hosts NAME` | glibc resolution path | Includes /etc/hosts |
| `resolvectl query NAME` | systemd-resolved lookup | `resolvectl query example.com` |
| `resolvectl status` | Per-link DNS config | Shows DNS servers |
| `host DOMAIN` | Simple lookup utility | `host example.com` |

### DNS resolution diagnostic script

```bash
#!/usr/bin/env bash
# dns-check.sh — compare nsswitch vs direct DNS
set -euo pipefail

NAME="${1:?usage: dns-check.sh hostname}"
echo "=== nsswitch (getent) ==="
getent hosts "$NAME" || echo "getent: no entry"

echo ""
echo "=== dig +short (direct DNS) ==="
dig +short "$NAME" A || echo "dig A: no answer"
dig +short "$NAME" AAAA 2>/dev/null | head -3 || true

echo ""
echo "=== Resolver config ==="
grep -E '^nameserver|^search' /etc/resolv.conf 2>/dev/null | head -5

echo ""
echo "=== resolvectl (if available) ==="
resolvectl query "$NAME" 2>/dev/null | head -10 || echo "resolvectl not available"
```

### Batch lookup from file

```bash
#!/usr/bin/env bash
# bulk-dig.sh — resolve hostnames from list
while read -r host; do
  [[ -z "$host" || "$host" =~ ^# ]] && continue
  ip=$(dig +short "$host" A | head -1)
  printf "%-40s %s\n" "$host" "${ip:-NXDOMAIN/empty}"
done < "${1:?hostfile}"
```

## Common Mistakes

!!! warning "Trusting dig when apps fail"
    Applications use nsswitch — `/etc/hosts` or LDAP may override DNS. Always compare `getent hosts` with `dig`.

!!! warning "Manually editing resolv.conf on cloud images"
    cloud-init, NetworkManager, or systemd-resolved overwrite manual edits. Configure DNS at the source (netplan, NM, DHCP).

!!! warning "Assuming NXDOMAIN means typo only"
    NXDOMAIN can mean DNS hijacking, split-horizon misconfiguration, or wrong search domain appended.

!!! warning "Ignoring search domain behavior"
    With `search example.com`, querying `api` may resolve `api.example.com`. Unexpected suffixes cause "works on my laptop" bugs.

!!! warning "Using nslookup in scripts"
    Output format varies; `dig +short` is script-safe and consistent.

## Best Practices

!!! tip "Use dig +trace for delegation issues"
    When records are wrong after zone changes, trace shows whether root, TLD, or authoritative server returns stale data.

!!! tip "Specify record type explicitly"
    Default is A; modern dual-stack services need AAAA. Use `dig AAAA` and `dig A` separately.

!!! tip "Document internal vs external resolvers"
    Corporate split-horizon DNS returns different answers inside vs outside. Runbooks should list which resolver to test from each zone.

!!! tip "Prefer systemd-resolved or dedicated caching forwarder"
    Local caching reduces latency and upstream load — important for high-churn microservices.

!!! tip "Set reasonable TTL before migrations"
    Lower TTL 24–48 hours before IP changes to speed propagation.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `dig` works, app fails | `/etc/hosts` override or nsswitch | Compare `getent` vs `dig`; inspect hosts file |
| Intermittent resolution | Flaky upstream resolver | Switch to reliable DNS; check `resolvectl statistics` |
| Wrong IP returned | Split-horizon or stale cache | Query authoritative NS directly; flush local cache |
| `SERVFAIL` | Auth server error or DNSSEC failure | Check auth NS health; `dig +dnssec` for validation errors |
| `NXDOMAIN` | Name doesn't exist or wrong domain | Verify spelling; check search domain suffix |
| Slow lookups | High latency to resolver | Use local cache; pick geographically close DNS |
| No reverse DNS | Missing PTR record | PTR is optional; create in IP owner zone if needed |
| TCP 53 timeouts | Large response needs TCP | Normal for big zones; ensure firewall allows TCP 53 |
| `connection timed out; no servers could be reached` | No route to resolver | Fix routing; verify `/etc/resolv.conf` nameservers |

## Summary

- DNS is a **hierarchical, distributed** system delegating authority from root through TLD to domain owners
- **Recursive resolvers** chase queries for clients; **iterative** servers return referrals or answers
- Linux resolves via **nsswitch** (`files` then `dns`) — `/etc/hosts` can override DNS for applications
- **`dig`** is the primary diagnostic tool; **`+trace`** reveals delegation problems
- Understand **TTL**, caching, and search domains before blaming application code for name failures
- UDP 53 is default transport; TCP 53 used for large responses and zone transfers

## Interview Questions

1. Explain the DNS hierarchy from root to authoritative nameserver.
2. What is the difference between recursive and iterative DNS queries?
3. Why might `dig example.com` and `ping example.com` resolve differently?
4. What does `dig +trace` show and when would you use it?
5. What is the purpose of `/etc/hosts` and nsswitch.conf?
6. Why do resolvers cache DNS answers and what is TTL?
7. What ports does DNS use and when does it switch to TCP?
8. What is a stub resolver?
9. Explain the difference between forward and reverse DNS.
10. What does NXDOMAIN mean?

??? tip "Sample Answers (Questions 3, 4, and 7)"

    **Q3 — dig vs ping difference:** `dig` queries DNS servers directly. `ping` calls the system resolver via nsswitch, which checks `/etc/hosts` first, then DNS. A hosts file entry can redirect ping while dig still shows the public IP.

    **Q4 — dig +trace:** Performs iterative queries starting at root servers, following NS referrals through TLD to authoritative nameservers. Use when propagation issues occur, when validating zone delegation, or when different resolvers return conflicting answers.

    **Q7 — DNS ports:** Most queries use UDP 53. TCP 53 is used when response exceeds 512 bytes (or EDNS buffer), for zone transfers (AXFR/IXFR), and when truncation (TC bit) forces retry over TCP.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md) *(previous)*
- [DNS Records and Troubleshooting](dns-records-and-troubleshooting.md) *(next)*
- [Linux Networking Essentials](../linux/linux-networking-essentials.md)
- [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [RFC 1034 — Domain Names Concepts](https://www.rfc-editor.org/rfc/rfc1034)
- [RFC 1035 — Domain Names Implementation](https://www.rfc-editor.org/rfc/rfc1035)
- [dig man page](https://bind9.readthedocs.io/en/latest/manpages.html#dig-1)
- [systemd-resolved documentation](https://www.freedesktop.org/software/systemd/man/systemd-resolved.service.html)
- [ICANN Root Server](https://www.iana.org/domains/root/servers)
- [REBASH Academy – Networking Overview](index.md)
