---
title: "DNS Fundamentals"
description: "Understand DNS hierarchy, recursive vs iterative resolution, Linux resolvers, and prove name lookup with dig and resolv.conf comparison."
difficulty: beginner
estimated_time: "40–55 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: networking
technology: networking
module: "Module 9 · DNS"
tags:
  - networking
  - dns
  - dig
  - resolvers
  - nameservers
prerequisites:
  - networking/tcp-and-udp-deep-dive
next:
  - networking/dns-records-and-troubleshooting
related:
  - networking/production-dns-operations
  - networking/http-https-and-application-layer
  - linux/linux-networking-tools
labs:
  - labs/networking-dns-firewall-triage
interview: interview/networking
comments: false
---

# DNS Fundamentals

## Overview

The **Domain Name System (DNS)** maps names to addresses. When DNS fails, applications look like a network outage even if routes and firewalls are healthy. Cloud cutovers, Kubernetes services, and certificate validation all depend on correct resolution and caching.

Linux hosts usually ask a **stub resolver** configured in `/etc/resolv.conf` (often managed by `systemd-resolved` or Dynamic Host Configuration Protocol). That stub talks to a **recursive resolver**, which walks the hierarchy: root → top-level domain (TLD) → authoritative name servers.

This is **Tutorial 10** in **Module 9: DNS** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series. It is written for Cloud, DevOps, Site Reliability Engineering (SRE), and platform engineers. You will prove resolution with `dig` and a small script under `~/rebash-networking/lab10`.

## Prerequisites

- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md) — DNS uses UDP/TCP port 53
- Ubuntu practice host with outbound DNS allowed
- Package: `dnsutils` (`dig`)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the DNS hierarchy and recursive vs iterative resolution
- [ ] Read `/etc/resolv.conf` and relate it to the resolver your host uses
- [ ] Query A, AAAA, and NS records with `dig`
- [ ] Use `dig +trace` (or stepwise queries) to show the resolution path
- [ ] Ship a small script that captures resolver evidence for tickets

## Architecture

Stub resolver → recursive resolver → root / TLD / authoritative servers → answer cached along the path.

![DNS resolution path](../assets/excalidraw/dns-resolution.svg)

## Theory

### What it is

DNS is a distributed database of **resource records**. A **recursive resolver** finds the answer on behalf of the client. **Authoritative** servers hold the data for a zone. Common first queries: **A** (IPv4), **AAAA** (IPv6), **NS** (name servers for a zone).

```bash
dig example.com A +short
cat /etc/resolv.conf
```

### Why it matters

Wrong resolver settings send you to the wrong private zone (split-horizon DNS). Stale cache after a cutover keeps traffic on old IPs until Time To Live (TTL) expires. Kubernetes and cloud load balancers rely on DNS names in almost every deploy. If you cannot prove what answer this host received, you cannot close a Sev-2.

### How it works

1. App calls getaddrinfo → stub reads resolv.conf (or resolved).
2. Recursive resolver asks root for the TLD NS, then the zone NS, then the record.
3. Answers are cached according to TTL.
4. `dig +trace` shows iterative steps from the root (from your dig client’s view).

```bash
dig example.com NS +short
dig example.com A
```

### Key concepts and comparisons

| Role | Job |
|------|-----|
| Stub | On the host; forwards queries |
| Recursive resolver | Walks the tree for the client |
| Authoritative NS | Answers for a zone from its data |

| Tool | Use |
|------|-----|
| `dig` | Detailed DNS query/response |
| `getent hosts` | libc resolution path (includes hosts file) |
| `/etc/hosts` | Static overrides before DNS |

### Common pitfalls

- Editing `/etc/resolv.conf` by hand on systemd-resolved hosts (it may be a symlink).
- Testing only from your laptop while production pods use another resolver.
- Forgetting that `/etc/hosts` can override DNS.
- Treating NXDOMAIN the same as SERVFAIL (covered deeper in the next tutorial).

## Hands-on Lab

### Objective

Query `example.com` with `dig` (A/AAAA/NS and optional `+trace`), compare results with `/etc/resolv.conf`, and write a script that packages resolver evidence under `~/rebash-networking/lab10`.

### Prerequisites

- `dig` installed
- Outbound UDP/TCP 53 allowed (or corporate resolver reachable)

### Lab environment

Workspace: `~/rebash-networking/lab10`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-networking/lab10 && cd ~/rebash-networking/lab10
set -euo pipefail
whoami | tee admin-user.txt
command -v dig >/dev/null || { sudo apt-get update && sudo apt-get install -y dnsutils; }
dig -v 2>&1 | head -n 1 | tee dig-version.txt || true
```

!!! example "Expected output"
    `dig` is available; workspace ready.


### Real-world scenario

After a DNS provider change, one VM still hits the old site. You must show which resolver the VM uses, what A/AAAA/NS answers it gets for a known name, and whether a trace reaches the expected authority — then attach a scripted evidence pack to the change ticket.

### Step-by-step tasks

#### Task 1 – Resolver config vs dig A/AAAA/NS

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-networking/lab10
set -euo pipefail

cp -L /etc/resolv.conf resolv.conf.copy 2>/dev/null || cat /etc/resolv.conf > resolv.conf.copy
cat resolv.conf.copy

dig example.com A +noall +answer +stats | tee dig-a.txt
dig example.com AAAA +noall +answer +stats | tee dig-aaaa.txt
dig example.com NS +noall +answer +stats | tee dig-ns.txt

dig example.com A +short | tee dig-a-short.txt
test -s dig-a-short.txt

# Who answered? (SERVER line in full dig)
dig example.com A | tee dig-a-full.txt
grep -E '^;; (SERVER|Query time)|ANSWER SECTION' dig-a-full.txt || test -s dig-a-full.txt
```

!!! example "Expected output"
    `dig-a-short.txt` has at least one IPv4 address; NS and AAAA files exist (AAAA may be empty on some paths — A must not be).


#### Task 2 – Trace or stepwise path

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-networking/lab10
set -euo pipefail

# +trace needs network to root/TLD; if blocked, fall back to NS then A @ns
if dig example.com +trace +nodnssec 2>trace.err | tee dig-trace.txt | grep -q 'example.com.'; then
  echo "trace: OK" | tee trace-status.txt
else
  echo "trace: fallback" | tee trace-status.txt
  NS="$(dig example.com NS +short | head -n 1)"
  echo "using NS=$NS" | tee -a trace-status.txt
  dig example.com A "@${NS}" +noall +answer | tee dig-from-auth.txt
  test -s dig-from-auth.txt
fi

# Compare libc path
getent hosts example.com | tee getent-example.txt || true
```

!!! example "Expected output"
    either a usable `dig-trace.txt` or a successful query against an authoritative NS in `dig-from-auth.txt`.


#### Task 3 – Evidence script

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-networking/lab10
set -euo pipefail
```

Create `dns-fundamentals-evidence.sh`:

```bash title="dns-fundamentals-evidence.sh"
#!/usr/bin/env bash
set -euo pipefail
OUT_DIR="$(cd "$(dirname "$0")" && pwd)"
{
  echo "=== host ==="
  hostname
  date -Is
  echo "=== resolv.conf ==="
  cat /etc/resolv.conf
  echo "=== dig A/AAAA/NS (short) ==="
  dig example.com A +short
  dig example.com AAAA +short
  dig example.com NS +short
  echo "=== dig SERVER ==="
  dig example.com A | awk '/^;; SERVER/ {print}'
} | tee "$OUT_DIR/evidence-run.txt"
```

``` {.bash .ra-terminal title="Terminal"}
chmod +x dns-fundamentals-evidence.sh
./dns-fundamentals-evidence.sh
test -s evidence-run.txt

tar -czf dns-fundamentals-evidence.tgz \
  admin-user.txt resolv.conf.copy \
  dig-a.txt dig-aaaa.txt dig-ns.txt dig-a-short.txt dig-a-full.txt \
  dig-trace.txt trace-status.txt getent-example.txt evidence-run.txt \
  dns-fundamentals-evidence.sh 2>/dev/null || \
tar -czf dns-fundamentals-evidence.tgz \
  admin-user.txt resolv.conf.copy dig-a-short.txt dig-a-full.txt \
  evidence-run.txt dns-fundamentals-evidence.sh trace-status.txt
ls -l dns-fundamentals-evidence.tgz | tee evidence-ls.txt
```

!!! example "Expected output"
    `dns-fundamentals-evidence.sh` runs and writes `evidence-run.txt`; archive is non-empty.


### Validation steps

- [ ] `dig example.com A +short` returned an address
- [ ] `resolv.conf.copy` captured the stub resolver config
- [ ] Trace or authoritative fallback produced useful output
- [ ] `dns-fundamentals-evidence.sh` is executable and was run
- [ ] Archive exists under `~/rebash-networking/lab10`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `dig: command not found` | Package missing | `sudo apt-get install -y dnsutils` |
| `+trace` hangs / fails | Outbound to root blocked | Use NS + `dig @ns` fallback |
| Empty AAAA | No IPv6 published or filtered | OK if A works; note it |
| resolv.conf is a stub symlink | systemd-resolved | Still copy content; check `resolvectl status` if needed |
| Different answer than laptop | Different resolver / cache | Compare SERVER lines and TTLs |

### Challenge exercise

Extend `dns-fundamentals-evidence.sh` to also print `resolvectl status 2>/dev/null | head -n 40` when `resolvectl` exists, and save that combined run to `evidence-run-v2.txt`. Keep it a shell script artefact.

### Learning outcomes

- Linked resolv.conf to dig’s SERVER line
- Queried A/AAAA/NS for a public name
- Automated an evidence pack for DNS change tickets

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-networking/lab10
# Inspection-only — optional: rm -f dns-fundamentals-evidence.tgz *.txt
```

## Validation

- [ ] Lab finished under `~/rebash-networking/lab10/`
- [ ] You can explain stub vs recursive vs authoritative
- [ ] You know why `/etc/hosts` can hide DNS problems
- [ ] You can describe what `dig +trace` is trying to show

## Code Walkthrough

DNS checks in production usually follow:

1. **What resolver does this host use?** — resolv.conf / resolved  
2. **What answer does dig get?** — A/AAAA + SERVER line  
3. **Is libc seeing the same thing?** — `getent hosts`  
4. **Where is authority?** — NS + query `@ns` or `+trace`  
5. **Least surprise** — change DNS in one controlled place (DHCP option, cloud DNS, CoreDNS)  

Do not flush every cache globally as a first step.

## Security Considerations

- DNS spoofing and cache poisoning are real — prefer DNS Security Extensions (DNSSEC) where operated  
- Do not point production stubs at random public resolvers without a decision record  
- Split-horizon mistakes can leak internal names — review what is published publicly  
- Encrypt DNS where policy requires (DoT/DoH) — know what your platform supports  
- Evidence packs may include internal resolver IPs — keep them inside your ticket system  

## Common Mistakes

!!! warning "Blaming the app when dig already fails"
    If dig cannot resolve the name, the app will not either. **Fix:** repair DNS before restarting pods forever.

!!! warning "Hand-editing resolv.conf on resolved hosts"
    Changes get overwritten. **Fix:** configure systemd-resolved, NetworkManager, or DHCP options properly.

!!! warning "Testing only A records"
    Dual-stack and IPv6-only paths need AAAA awareness. **Fix:** query both A and AAAA.

!!! warning "Ignoring /etc/hosts"
    A bad static line wins over DNS. **Fix:** check hosts file early.

## Best Practices

- Standardise on `dig` output in runbooks (include SERVER and TTL)  
- Compare laptop vs server resolver during cutovers  
- Prefer Infrastructure as Code for public zones  
- Document recursive resolvers used by each environment  
- Keep a known-good name (`example.com`) for path tests, plus your real zone  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| SERVFAIL | Resolver/upstream problem | Try another resolver; check logs |
| NXDOMAIN | Name does not exist | Fix zone or typo |
| Timeout | UDP 53 blocked | Open DNS path; try TCP (`dig +tcp`) |
| Wrong IP | Stale cache / wrong zone | Check TTL, authority, split-horizon |
| Works on laptop only | Different resolvers | Align stub config |

## Summary

DNS turns names into addresses through stub, recursive, and authoritative roles. Prove what *this* host sees with `dig` and resolv.conf before you blame the application. Next: [DNS Records and Troubleshooting](dns-records-and-troubleshooting.md).

## Interview Questions

**1. What is the difference between a recursive resolver and an authoritative name server?**

??? success "Reveal answer"
    A **recursive resolver** finds answers on behalf of clients by walking the DNS tree and caching results. An **authoritative** server answers from the zone data it hosts for a domain. Your laptop usually talks to a recursive resolver; that resolver eventually queries authoritative NS records for `example.com`.

**2. What does `/etc/resolv.conf` control on Linux?**

??? success "Reveal answer"
    It tells the **stub resolver** which upstream DNS servers (and search domains) to query. On many Ubuntu hosts it is managed by **systemd-resolved** or Dynamic Host Configuration Protocol (DHCP). Hand edits may be overwritten. Always confirm with `dig`’s `SERVER` line what was actually used.

**3. Why might `getent hosts` and `dig` disagree?**

??? success "Reveal answer"
    **`getent`** uses the Name Service Switch (NSS) path, which can include **`/etc/hosts`**, mDNS, and other sources. **`dig`** speaks DNS directly to a resolver. A hosts-file override can make getent succeed with an address dig never returns (or the reverse).

**4. What is dig +trace showing you?**

??? success "Reveal answer"
    It performs an **iterative** resolution from the root downward, printing referrals and answers at each step. It helps prove which servers are involved. Some networks block direct root access; then query the zone’s NS with `dig @ns` instead.

**5. How does TTL affect a DNS cutover?**

??? success "Reveal answer"
    **Time To Live (TTL)** tells caches how long they may reuse an answer. A high TTL before cutover means old IPs linger. Operators often lower TTL ahead of time, change the record, then raise TTL after. Without TTL planning, “I changed DNS” does not mean “everyone sees it now.”

**6. Why does DNS failure look like a network outage?**

??? success "Reveal answer"
    Apps connect to **names**. If resolution fails or returns a dead address, TCP never reaches the healthy backend even when routes are fine. Good triage separates “name → IP” from “IP → port” with dig plus curl/`nc`.

**7. In Kubernetes, where does cluster DNS usually fit in this model?**

??? success "Reveal answer"
    Pods typically use **CoreDNS** (or similar) as their recursive/cluster resolver via stub config injected into the pod. Cluster service names are answered authoritatively inside the cluster DNS, while external names are forwarded upstream. Debugging must check the **pod’s** resolvers, not only your laptop.

## Related Tutorials

- [Networking for Cloud & DevOps – Overview](index.md)
- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md) *(previous)*
- [DNS Records and Troubleshooting](dns-records-and-troubleshooting.md) *(next)*
- [Lab — DNS / firewall triage](../labs/networking-dns-firewall-triage.md)

## References

- [RFC 1034 — Domain Concepts](https://www.rfc-editor.org/rfc/rfc1034)  
- [RFC 1035 — DNS Implementation](https://www.rfc-editor.org/rfc/rfc1035)  
- [`dig(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/dig.1.html)  
- Track index: [Networking for Cloud & DevOps Engineers](index.md)
