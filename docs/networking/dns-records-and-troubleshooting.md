---
title: "DNS Records and Troubleshooting"
description: "Master A, AAAA, CNAME, MX, TXT, NS, SOA, PTR, and SRV records, TTL cutovers, dig workflows, and split-horizon DNS for Cloud and DevOps work."
difficulty: intermediate
estimated_time: "45–60 min"
technology: networking
category: networking
module: "Module 9 · DNS"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - linux-administrator
  - site-reliability-engineer
  - kubernetes-engineer
skills:
  - dns
  - dig
  - dns-records
  - ttl
prerequisites:
  - networking/dns-fundamentals
next:
  - networking/http-https-and-application-layer
related:
  - networking/production-dns-operations
  - networking/load-balancing-fundamentals
  - networking/tcp-and-udp-deep-dive
labs:
  - labs/networking-dns-firewall-triage
projects: []
interview: interview/networking
certifications:
  - CompTIA Network+
  - AWS SAA
tags:
  - networking
  - dns
  - records
  - dig
  - cname
  - mx
  - txt
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# DNS Records and Troubleshooting

## Overview

Query and explain every common DNS record type, plan TTL for cutovers, and run a repeatable dig-based troubleshooting checklist.

Resolution knowledge is half the job. Production breaks on bad **CNAME** apex choices, stale **TXT** verification, wrong **MX**, dangling aliases after a load balancer delete, and **split-horizon** mismatches between internal and public DNS.

This is the second tutorial in **Module 9 — DNS**. Complete [DNS Fundamentals](dns-fundamentals.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 9 · DNS** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [DNS Fundamentals](dns-fundamentals.md)
- Linux host with `dig` and `host`
- Comfort with UDP/TCP 53 from [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md)

### Recommended

- A domain you control (optional) for change labs

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain A, AAAA, CNAME, MX, TXT, NS, SOA, PTR, and SRV  
- [ ] Query types with `dig` and read full answers  
- [ ] Plan TTL before migrations  
- [ ] Spot CNAME apex/chain and dangling-record risks  
- [ ] Relate MX/TXT to email authentication basics  
- [ ] Detect split-horizon discrepancies  
- [ ] Use `@nameserver`, `+norecurse`, and `+trace` for authoritative debug

## Architecture

Common record types map names to addresses, aliases, mail, text, and services.

![DNS record types](../assets/excalidraw/dns-records.svg)

## Theory

### Zone and record shape

A **zone** is the administrative cut of the namespace. Authoritative servers answer for it. Each record:

```text
name  TTL  class  type  rdata
```

Class is almost always **IN** (Internet).

### Record types

| Type | Purpose | Example rdata |
|------|---------|---------------|
| **A** | IPv4 | `93.184.216.34` |
| **AAAA** | IPv6 | `2606:2800:220:1:…` |
| **CNAME** | Alias | `lb.example.net` |
| **MX** | Mail (priority + host) | `10 mail.example.com` |
| **TXT** | Text / SPF / verify | `"v=spf1 …"` |
| **NS** | Nameserver delegation | `ns1.example.com` |
| **SOA** | Zone metadata | serial, timers, neg TTL |
| **PTR** | Reverse (IP → name) | `host.example.com` |
| **SRV** | Service location | priority weight port target |
| **CAA** | Allowed CAs | `0 issue "letsencrypt.org"` |

### A / AAAA

Map hostnames to addresses. Multiple answers are DNS round-robin — useful for simple distribution, not a full load balancer.

### CNAME

Alias inherits the target’s addresses.

- Cannot coexist with other data types on the same name (DNSSEC exceptions aside)  
- Zone **apex** traditionally cannot be a CNAME — use provider ALIAS/ANAME or A/AAAA  
- Long CNAME chains add latency; flatten when you can  
- **Dangling CNAME** (target deleted) is a hijack risk  

### MX and TXT

MX directs mail by priority (lower preferred). Targets should resolve with A/AAAA. TXT carries SPF, DKIM, DMARC, and vendor verification strings.

### NS and SOA

NS lists authoritative servers. SOA holds serial and timers — check serial when chasing “did the change publish?”

### PTR

Reverse zones (`in-addr.arpa` / `ip6.arpa`). Mail often requires valid PTR. Query: `dig -x 8.8.8.8 +short`.

### SRV

Service discovery: priority, weight, port, target — used by some SIP, Kerberos, and Kubernetes-related patterns.

### TTL and cutovers

| Scenario | Practical TTL |
|----------|----------------|
| Stable prod | 3600+ |
| Planned migration | Drop to 300 ahead of time |
| Emergency | You may wait out the old TTL |

Lower TTL **before** you need fast change. Changing an A does not flush a still-cached CNAME until that CNAME’s TTL expires.

### Split horizon

Internal resolvers may answer differently from public DNS (private IPs vs public LBs). Always compare:

```bash
dig @internal-dns app.example.com
dig @8.8.8.8 app.example.com
```

## Hands-on Lab

**Focus:** practise the core workflow for DNS Records and Troubleshooting

```bash
mkdir -p ~/rebash-networking/module-09
cd ~/rebash-networking/module-09

sudo apt-get update
sudo apt-get install -y dnsutils
```

### Step 1 – Address and alias records

```bash
dig example.com A +short
dig example.com AAAA +short
dig www.github.com CNAME +short
dig www.github.com A +short
```

### Step 2 – MX, TXT, NS, SOA

```bash
dig example.com MX +noall +answer
dig example.com TXT +short | head -5
dig example.com NS +short
dig example.com SOA +short
```

### Step 3 – PTR

```bash
dig -x 8.8.8.8 +short
```

### Step 4 – Authoritative vs recursive

```bash
NS=$(dig example.com NS +short | head -1)
dig @$NS example.com A +norecurse +noall +answer +authority
dig @8.8.8.8 example.com A +noall +answer
```

### Step 5 – Trace and TTL awareness

```bash
dig +trace example.com A | tail -40
dig example.com A +noall +answer
```

Note the TTL; wait and re-query to see it count down at a recursive resolver.

### Step 6 – Incident checklist (runbook style)

```bash
# 1) Does the name exist?
dig +short broken.example.invalid A || true

# 2) What does public recursive say?
dig @1.1.1.1 app.example.com A +noall +answer

# 3) What do authoritative NS say?
dig app.example.com NS +short
# dig @ns… app.example.com A +norecurse

# 4) CNAME chain?
dig app.example.com CNAME +short
dig +short app.example.com

# 5) Compare internal vs external if split horizon is in play
```

## Validation

- [ ] Lab commands run under `~/rebash-networking/module-09/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **DNS Records and Troubleshooting** always combines:

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

!!! warning "Skipping fundamentals for DNS Records and Troubleshooting"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for DNS Records and Troubleshooting"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode DNS Records and Troubleshooting changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Wrong IP after change | Old TTL cache | Check TTL; query authoritative; wait or flush local cache |
| CNAME at apex fails | Provider/RFC limits | Use ALIAS/ANAME or A/AAAA |
| Cert validation stuck | Wrong TXT / cache | Query `_acme-challenge` at authoritative NS |
| Mail bounce | MX/PTR/SPF | Check MX, `dig -x`, TXT SPF |
| Internal OK, public bad | Split horizon / publish lag | Compare resolvers; check zone sync serial |
| Dangling alias | Target removed | Remove or retarget CNAME; watch for takeover |

## Summary

- Know the **rdata** meaning of each common type  
- **CNAME** rules and dangling targets matter in cloud  
- **TTL** is a cutover control, not an afterthought  
- Debug with **authoritative** answers, not only public recursion  
- Always consider **split horizon** in enterprise and VPC DNS

## Interview Questions

1. How does **DNS Records and Troubleshooting** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md)  
- [Production DNS Operations](production-dns-operations.md)  
- [Load Balancing Fundamentals](load-balancing-fundamentals.md)

## References

- [RFC 1035 — DNS implementation](https://www.rfc-editor.org/rfc/rfc1035)  
- [RFC 1912 — Common DNS operational errors](https://www.rfc-editor.org/rfc/rfc1912)  
- [IANA DNS parameters](https://www.iana.org/assignments/dns-parameters/)
