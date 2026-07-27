---
title: DNS Records and Troubleshooting
description: Master A, AAAA, CNAME, MX, TXT, NS, SOA, PTR, and SRV records, TTL propagation, dig troubleshooting workflows, and split-horizon DNS.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
category: networking
tags:
  - networking
  - dns
  - records
  - dig
  - cname
  - mx
  - txt
  - troubleshooting
prerequisites:
  - Complete DNS Fundamentals or understand recursive vs iterative resolution
  - Linux environment with dig and nslookup installed
  - Basic understanding of HTTP and mail server concepts
comments: false
---

# DNS Records and Troubleshooting

## Overview

Knowing how DNS resolution works is half the battle — the other half is understanding **record types**, **TTL behavior**, and **zone configuration**. A misconfigured **CNAME at the zone apex**, an expired **MX record**, or a stale **TXT** entry for domain verification can take production offline or block email delivery for hours. DevOps engineers create and debug DNS records constantly: load balancer aliases, ACM certificate validation, SPF/DKIM, Kubernetes Ingress hostnames, and CDN cutovers.

This tutorial is **Tutorial 9** in **Module 3: Transport & DNS** of the REBASH Academy Networking series. You will learn every common record type, query them with **`dig`**, build systematic troubleshooting workflows, and avoid pitfalls that cause propagation delays and split-horizon confusion. Complete [DNS Fundamentals](dns-fundamentals.md) first.

## Prerequisites

- [DNS Fundamentals](dns-fundamentals.md) — hierarchy, resolvers, recursive vs iterative queries
- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md) — UDP/TCP port 53 transport
- Linux host with `dig`, `host`, and optional `delv` for DNSSEC
- Access to a domain you control (optional, for record creation labs)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the purpose of A, AAAA, CNAME, MX, TXT, NS, SOA, PTR, and SRV records
- [ ] Query specific record types with `dig +short` and interpret full responses
- [ ] Describe TTL impact on propagation and plan cutover windows
- [ ] Diagnose CNAME chains, apex alias limitations, and dangling records
- [ ] Troubleshoot email delivery issues related to MX and SPF/DKIM TXT records
- [ ] Identify split-horizon (internal vs external) DNS discrepancies
- [ ] Use `dig +trace`, `@nameserver`, and `+norecurse` for authoritative debugging
- [ ] Build a repeatable DNS troubleshooting checklist for production incidents

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Client
        APP["Application / Browser"]
        RES["Recursive Resolver<br/>8.8.8.8 · 1.1.1.1"]
    end

    subgraph Auth["Authoritative DNS — example.com zone"]
        NS["NS Records<br/>ns1.example.com"]
        SOA["SOA Record<br/>serial · refresh · expire"]
        A["A / AAAA<br/>host → IP"]
        CNAME["CNAME<br/>alias → target"]
        MX["MX<br/>mail priority"]
        TXT["TXT<br/>SPF · DKIM · verify"]
    end

    APP --> RES
    RES --> NS
    NS --> SOA
    NS --> A
    NS --> CNAME
    NS --> MX
    NS --> TXT```

## Theory

### Zone Files and Record Structure

A **DNS zone** is the administrative boundary for a domain (e.g., `example.com`). **Authoritative nameservers** host the zone and answer queries from resolvers. Each record is a tuple:

```
name  TTL  class  type  rdata
```

| Field | Meaning |
|-------|---------|
| **name** | Owner name (FQDN or relative) |
| **TTL** | Time-to-live in seconds — how long resolvers cache |
| **class** | Almost always `IN` (Internet) |
| **type** | Record type (A, CNAME, MX, …) |
| **rdata** | Type-specific data |

### Common Record Types

| Type | Purpose | Example_rdata |
|------|---------|---------------|
| **A** | IPv4 address | `93.184.216.34` |
| **AAAA** | IPv6 address | `2606:2800:220:1:248:1893:25c8:1946` |
| **CNAME** | Alias to another name | `lb.example.com` |
| **MX** | Mail exchange (priority + host) | `10 mail.example.com` |
| **TXT** | Arbitrary text (SPF, DKIM, verification) | `"v=spf1 include:_spf.google.com ~all"` |
| **NS** | Delegates subdomain to nameservers | `ns1.example.com` |
| **SOA** | Zone authority metadata | Serial, refresh, retry, expire, minimum TTL |
| **PTR** | Reverse DNS (IP → name) | `host.example.com` (in reverse zone) |
| **SRV** | Service location (port, priority, weight) | `10 60 8080 server.example.com` |
| **CAA** | Certificate authority authorization | `0 issue "letsencrypt.org"` |

### A and AAAA — Address Records

**A** records map hostnames to **IPv4** addresses. **AAAA** records map to **IPv6**. These are the most common records for web services, APIs, and load balancers.

Multiple A/AAAA records on one name provide **DNS round-robin** — resolvers rotate answers. This is not a substitute for a proper load balancer but appears in simple setups.

### CNAME — Canonical Name

A **CNAME** creates an alias: `www.example.com` → `lb-123.cloudprovider.net`. The alias inherits the target's A/AAAA records.

Critical constraints:

- **CNAME cannot coexist** with other record types on the same name (except DNSSEC records)
- **Zone apex** (`example.com` without subdomain) traditionally cannot be CNAME — use **ALIAS/ANAME** (Route 53) or **A record** at apex
- **CNAME chains** add latency — flatten to A/AAAA when possible

### MX — Mail Exchange

**MX** records direct email to mail servers with a **priority** (lower = preferred):

```
example.com.  3600  IN  MX  10  mail1.example.com.
example.com.  3600  IN  MX  20  mail2.example.com.
```

The mail server hostname must resolve via A/AAAA — MX targets should **not** be CNAMEs (deprecated by RFC 5321, though some providers still work).

### TXT — Text Records

**TXT** records store verification strings and email authentication:

| Use | Example |
|-----|---------|
| **SPF** | `"v=spf1 include:amazonses.com -all"` |
| **DKIM** | `"v=DKIM1; k=rsa; p=MIGfMA0GCS..."` |
| **Domain verification** | `"google-site-verification=abc123"` |
| **DMARC** | `"v=DMARC1; p=reject; rua=mailto:..."` |

Multiple TXT records on one name are valid — each is a separate string in the response.

### NS and SOA — Zone Authority

**NS** records list authoritative nameservers for the zone or delegation. **SOA (Start of Authority)** defines:

- **Serial** — incremented on each zone change (secondary NS sync trigger)
- **Refresh / Retry / Expire** — secondary sync timing
- **Minimum TTL** — default for negative caching (NXDOMAIN)

Check SOA when investigating propagation: `dig SOA example.com +short`.

### PTR — Reverse DNS

**PTR** records live in reverse zones (`in-addr.arpa` for IPv4) and map IP → hostname. Mail servers often reject email from IPs without valid PTR. Cloud providers assign PTR for Elastic IPs when configured.

Query: `dig -x 8.8.8.8 +short` → `dns.google.`

### TTL and Propagation

**TTL** controls how long resolvers cache answers. Lower TTL before migrations speeds cutover; higher TTL reduces query load and improves resilience to resolver outages.

| Scenario | Recommended TTL |
|----------|-----------------|
| Stable production record | 3600 (1 hour) or higher |
| Planned migration in 24h | Drop to 300 (5 min) beforehand |
| Emergency failover | Pre-lowering TTL days ahead is ideal; else wait full old TTL |

Resolvers cache **per record** — changing A record does not flush cached CNAME unless that CNAME's TTL expires.

### Split-Horizon DNS

**Split-horizon** (split-brain) returns different answers based on query source:

- **Internal resolver** → private IP (`10.0.1.50`) for `db.example.com`
- **Public resolver** → public IP or NXDOMAIN

Symptoms: `dig @8.8.8.8` differs from `dig @10.0.0.2` (corporate DNS). Always test from the **same resolver your application uses**.

## Hands-on Lab

Use public domains for read-only labs. Use your own domain for write exercises.

### Step 1 – Query A and AAAA records

**Command:**

```bash
dig +short example.com A
dig +short example.com AAAA
dig example.com A +noall +answer +ttlid
```

**Explanation:** `+short` gives concise output. `+ttlid` shows remaining cache TTL from the resolver.

**Expected output:**

```text
93.184.216.34
example.com.        86400   IN      A       93.184.216.34
```

### Step 2 – Explore CNAME chains

**Command:**

```bash
dig +short www.github.com CNAME
dig +short www.github.com A
dig www.github.com +trace 2>/dev/null | tail -15
```

**Explanation:** Follow alias to final A record. Long chains increase resolution latency.

### Step 3 – Inspect MX and mail routing

**Command:**

```bash
dig +short google.com MX | sort -n
dig +short $(dig +short google.com MX | sort -n | awk '{print $2}' | head -1) A
```

**Explanation:** Lists mail servers by priority, then resolves the primary server's IP.

**Expected output:**

```text
10 smtp.google.com.
142.250.190.10
```

### Step 4 – Read TXT records (SPF and verification)

**Command:**

```bash
dig +short google.com TXT
dig +short _dmarc.google.com TXT
dig TXT google.com +noall +answer
```

**Explanation:** Multiple TXT records return as separate lines. SPF and DMARC are critical for email deliverability.

### Step 5 – Query authoritative nameserver directly

**Command:**

```bash
AUTH_NS=$(dig +short example.com NS | head -1)
echo "Authoritative NS: $AUTH_NS"
dig @$AUTH_NS example.com SOA +noall +answer
dig @$AUTH_NS example.com A +norecurse +noall +answer
```

**Explanation:** Querying authoritative NS bypasses resolver cache — shows current zone data. `+norecurse` ensures iterative behavior.

### Step 6 – Reverse DNS lookup

**Command:**

```bash
dig +short -x 8.8.8.8
dig +short -x 1.1.1.1
```

**Explanation:** `-x` performs reverse lookup. Missing PTR is common for cloud IPs unless explicitly configured.

### Step 7 – Compare resolver answers (split-horizon simulation)

**Command:**

```bash
dig +short example.com A @8.8.8.8
dig +short example.com A @1.1.1.1
dig +short example.com A @208.67.222.222
```

**Explanation:** Public resolvers should agree for public zones. Disagreement suggests propagation in progress or geo/load-balanced DNS.

### Step 8 – Full troubleshooting workflow

**Command:**

```bash
DOMAIN=example.com
echo "=== NS ===" && dig +short $DOMAIN NS
echo "=== SOA ===" && dig +short $DOMAIN SOA
echo "=== A ===" && dig +short $DOMAIN A
echo "=== AAAA ===" && dig +short $DOMAIN AAAA
echo "=== MX ===" && dig +short $DOMAIN MX
echo "=== TXT ===" && dig +short $DOMAIN TXT
echo "=== Trace ===" && dig +trace $DOMAIN A 2>/dev/null | grep -E "^($DOMAIN|[a-z0-9.-]+\t)" | tail -8
```

**Explanation:** Reusable checklist for incident response — run before blaming application code.

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `dig +short NAME TYPE` | Concise record query | `dig +short api.example.com A` |
| `dig @NS NAME TYPE` | Query specific nameserver | `dig @ns1.example.com example.com SOA` |
| `dig +trace NAME` | Full delegation trace | `dig +trace example.com A` |
| `dig -x IP` | Reverse DNS (PTR) | `dig -x 10.0.0.1 +short` |
| `dig +noall +answer` | Suppress question section | Clean answer-only output |
| `dig +ttlid` | Show remaining cache TTL | `dig example.com +ttlid` |
| `host -t MX DOMAIN` | MX lookup (alternative) | `host -t MX example.com` |
| `delv DOMAIN` | DNSSEC validation | `delv example.com A` |

### DNS health check script

```bash
#!/usr/bin/env bash
# dns-check.sh — quick record audit for a domain
set -euo pipefail
DOMAIN="${1:?Usage: dns-check.sh example.com}"

check() {
  local type=$1
  echo "--- $type ---"
  dig +short "$DOMAIN" "$type" || echo "(none)"
}

for t in NS SOA A AAAA MX TXT CAA; do check "$t"; done
echo "--- PTR (if A exists) ---"
IP=$(dig +short "$DOMAIN" A | head -1)
[ -n "$IP" ] && dig +short -x "$IP" || echo "(no A record)"
```

## Common Mistakes

!!! warning "CNAME at zone apex"
    `example.com` cannot be a standard CNAME. Use provider ALIAS/ANAME or A record. Symptom: zone validation failures, certificate issuance errors.

!!! warning "MX pointing to CNAME"
    RFC 5321 discourages MX targets that are CNAMEs. Some MTAs reject mail silently. Use A/AAAA on the mail host directly.

!!! warning "Forgetting to lower TTL before migration"
    Old IP cached for full TTL duration after change. Plan TTL reduction 24–48 hours ahead.

!!! warning "Testing DNS from wrong resolver"
    Laptop uses corporate DNS; production uses Route 53 Resolver. Answers differ — always test from the application's resolver context.

!!! warning "Duplicate SPF TXT records"
    Multiple SPF strings on one domain invalidates SPF. Merge into single TXT record.

## Best Practices

!!! tip "Use CNAME for subdomains, A/ALIAS for apex"
    Standard pattern: `www` → CNAME to LB; apex → ALIAS or A to LB anycast IP.

!!! tip "Automate DNS with IaC"
    Terraform, Pulumi, or provider APIs — manual console edits cause drift and typos.

!!! tip "Monitor authoritative NS and SOA serial"
    Alert on unexpected serial changes — possible unauthorized zone modification.

!!! tip "Document every TXT record's owner"
    SPF, DKIM, verification strings accumulate. Stale TXT records confuse auditors and break email.

!!! tip "Validate with dig @authoritative before closing tickets"
    Resolver cache masks fresh authoritative data during propagation windows.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `NXDOMAIN` | Name doesn't exist in zone | Verify spelling; check zone file; confirm delegation |
| `SERVFAIL` | Auth server error or DNSSEC failure | Check NS health; `delv` for DNSSEC; review serial/logs |
| Old IP still returned | TTL not expired | Wait remaining TTL; flush local cache; query auth NS |
| CNAME and other records conflict | Invalid zone config | Remove conflicting records; CNAME exclusive per name |
| Email not delivered | Missing/wrong MX or SPF | Verify MX priority; merge SPF; add DKIM/DMARC |
| Certificate validation fails | Wrong/missing TXT/CNAME | Match CA exact string; check `_acme-challenge` subdomain |
| Internal works, external fails | Split-horizon misconfiguration | Align internal and external zones; test both resolvers |
| Intermittent resolution | Unstable NS or lame delegation | Verify all NS in glue records respond; fix delegation |
| Slow DNS lookups | Long CNAME chain | Flatten to A/AAAA; reduce hops |
| `dig` differs from app behavior | `/etc/hosts` or nsswitch override | Compare `getent hosts` vs `dig`; inspect nsswitch.conf |

## Summary

- DNS **record types** serve distinct roles: **A/AAAA** for addresses, **CNAME** for aliases, **MX** for mail, **TXT** for verification and email auth
- **TTL** governs cache duration — plan TTL reductions before migrations
- Query **authoritative nameservers** directly with `dig @ns` to bypass resolver cache
- **CNAME at apex** and **MX-to-CNAME** are common misconfiguration patterns
- **Split-horizon DNS** explains different answers from internal vs public resolvers
- Use systematic checklists: NS → SOA → A/AAAA → CNAME → MX → TXT → trace
- **`dig +trace`** reveals delegation problems; **`dig +ttlid`** shows cache state

## Interview Questions

1. What is the difference between A and CNAME records?
2. Why can't you put a CNAME at the zone apex?
3. How does TTL affect DNS propagation during a migration?
4. What is an MX record and how does priority work?
5. What are SPF, DKIM, and DMARC TXT records used for?
6. Explain split-horizon DNS and when it causes confusion.
7. What is the purpose of SOA record fields (serial, refresh, expire)?
8. How do you query an authoritative nameserver directly?
9. What is reverse DNS (PTR) and why do mail servers care?
10. What does `dig +trace` reveal that a simple `dig` does not?

??? tip "Sample Answers (Questions 1, 3, and 5)"

    **Q1 — A vs CNAME:** An A record maps a hostname directly to an IPv4 address. A CNAME maps a hostname to another hostname (alias). The alias inherits the target's A/AAAA resolution. CNAME cannot coexist with other records on the same name.

    **Q3 — TTL and propagation:** TTL is how long resolvers cache a record. After you change an A record, resolvers continue returning the old IP until their cached entry expires (up to the previous TTL). Lower TTL before changes so propagation completes within minutes instead of hours.

    **Q5 — SPF, DKIM, DMARC:** SPF (TXT) lists authorized mail senders for a domain. DKIM (TXT) provides cryptographic signature verification for messages. DMARC (TXT) tells receivers how to handle SPF/DKIM failures and where to send aggregate reports. Together they prevent email spoofing and improve deliverability.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [DNS Fundamentals](dns-fundamentals.md) *(previous)*
- [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md) *(next — Module 4)*
- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md)
- [Load Balancing Fundamentals](load-balancing-fundamentals.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [RFC 1035 — DNS Implementation and Record Types](https://www.rfc-editor.org/rfc/rfc1035)
- [RFC 7208 — SPF](https://www.rfc-editor.org/rfc/rfc7208)
- [RFC 7489 — DMARC](https://www.rfc-editor.org/rfc/rfc7489)
- [RFC 6376 — DKIM](https://www.rfc-editor.org/rfc/rfc6376)
- [dig man page](https://bind9.readthedocs.io/en/latest/manpages.html#dig-1)
- [REBASH Academy – Networking Overview](index.md)
