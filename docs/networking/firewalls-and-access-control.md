---
title: "Firewalls and Access Control"
description: "Design least-privilege host firewalls with UFW or nftables, compare cloud security groups and network ACLs, and change rules without locking out SSH."
difficulty: intermediate
estimated_time: "45–55 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: networking
technology: networking
module: "Module 11 · NAT & Firewalls"
tags:
  - networking
  - firewall
  - iptables
  - nftables
  - ufw
  - security-groups
prerequisites:
  - networking/nat-and-port-forwarding
next:
  - networking/linux-networking-toolkit
related:
  - networking/tcp-and-udp-deep-dive
  - networking/network-security-hardening
  - networking/firewall-change-control-and-production-acls
labs:
  - labs/networking-dns-firewall-triage
interview: interview/networking
comments: false
---

# Firewalls and Access Control

## Overview

A **firewall** decides which packets may enter, leave, or cross a host or network boundary. **Access control** here means the allow/deny policy for ports, protocols, and peers — on the Linux host (Uncomplicated Firewall (UFW), nftables, iptables) and in the cloud (security groups, network Access Control Lists (ACLs)).

**Stateful** firewalls remember connection state so return traffic for an allowed outbound session is accepted without a second wide-open rule. **Stateless** filters (many network ACLs) judge each packet alone, so you must allow ephemeral return ports carefully. In this tutorial you will inspect status, add a **temporary localhost** allow, and follow **allow before enable** so you never lock yourself out of Secure Shell (SSH).

Wrong firewalls cause more outages than glamorous attacks: blocked health checks, forgotten return paths on Network ACLs, or `0.0.0.0/0` on a database port. On cloud VMs, the **security group** is often the real edge; the host firewall is a second line. Good practice is least privilege, change tickets, and prove both allow and deny.

This is **Tutorial 2** in **Module 11: NAT & Firewalls** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series. It is written for Cloud, DevOps, SRE, and platform engineers. Evidence goes under `~/rebash-networking/lab14`.

## Prerequisites

- [NAT and Port Forwarding](nat-and-port-forwarding.md)
- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md) — ports and connection states
- A **practice Ubuntu VM** with `sudo` and working SSH (keep a second console or cloud serial access ready)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain stateful vs stateless filtering with one example each
- [ ] Inspect UFW or nftables status without breaking SSH
- [ ] Apply an allow-before-enable pattern for a temporary local rule
- [ ] Compare host firewalls with cloud security groups and network ACLs
- [ ] Remove lab rules cleanly and pack evidence

## Architecture

Policy is evaluated at one or more layers: cloud edge (security group / NACL), host firewall, then the application listen socket. Stateful engines track established flows; operators must still allow the first packet of desired services.

![Architecture diagram for Firewalls and Access Control](../assets/excalidraw/firewalls-access-control.svg)

## Theory

### What it is

A firewall rule matches fields such as direction, protocol, port, and source/destination, then **accepts** or **drops/rejects**. On Ubuntu, **UFW** is a simpler front end over iptables/nftables. **nftables** is the modern Linux packet filter. Cloud **security groups** are usually stateful virtual firewalls on Elastic Network Interfaces; **network ACLs** are often subnet-level and closer to stateless.

```bash
sudo ufw status verbose 2>/dev/null || true
sudo nft list ruleset 2>/dev/null | head -n 40 || true
ss -lntu | head
```

### Why it matters

Open ports invite scanners. Over-tight rules break deploy health checks and monitoring. Least privilege means: allow only what the service needs, from the peers that need it, and document why. In India and global teams alike, change windows and jump-server access make SSH lockouts especially painful — always allow SSH (port 22 or your custom port) **before** enabling a default-deny policy.

### How it works

1. **Inventory** — what listens (`ss -lntu`), what must talk to it.
2. **Allow required paths** — SSH first, then app ports, then monitoring.
3. **Enable / enforce** — only after allows exist (allow before enable).
4. **Prove** — positive test (curl/nc) and negative test (blocked peer/port).
5. **Review** — cloud SG + host firewall + app auth are layers, not duplicates of the same mistake.

```bash
# Pattern (conceptual) — lab uses safer localhost-only steps
# sudo ufw allow OpenSSH
# sudo ufw allow 8080/tcp
# sudo ufw --dry-run enable   # where supported / review status first
```

### Key concepts and comparisons

| Control | Typical scope | Stateful? |
|---------|---------------|-----------|
| UFW / nftables / iptables | One host | Usually yes |
| Cloud security group | Instance / ENI | Usually yes |
| Network ACL | Subnet | Often no |
| Application auth | Process | N/A (different layer) |

| Pattern | Prefer when | Avoid when |
|---------|-------------|------------|
| Default deny + explicit allows | Production hosts | Enabling deny before SSH allow |
| Security group as primary edge | Cloud VMs | Ignoring SG and only tuning UFW |
| Temporary localhost rule for labs | Learning / CI smoke | Leaving lab holes on public interfaces |

### Common pitfalls

- Running `ufw enable` with default deny **before** allowing SSH.
- Opening `0.0.0.0/0` to database ports “for a minute”.
- Fixing only the host firewall while the security group still blocks.
- Forgetting UDP for Domain Name System (DNS) or Virtual Private Network (VPN) paths.
- Using `REJECT` vs `DROP` without understanding client timeout behaviour.

## Hands-on Lab

### Objective

Inspect the host firewall safely, add a **temporary** allow for a localhost-only listener, prove connectivity, and remove the rule. Prefer dry-run/status. **Do not lock out SSH.**

### Prerequisites

- Ubuntu 22.04/24.04 with `sudo`
- Working local shell (and ideally a second SSH session if you are remote)
- `python3` for a tiny localhost server (standard on Ubuntu)

### Lab environment

Workspace: `~/rebash-networking/lab14`

```bash
mkdir -p ~/rebash-networking/lab14 && cd ~/rebash-networking/lab14
set -euo pipefail
whoami | tee admin-user.txt
ss -lntu | tee listen-before.txt
command -v ufw >/dev/null && echo ufw=yes | tee fw-tools.txt || echo ufw=no | tee fw-tools.txt
command -v nft >/dev/null && echo nft=yes | tee -a fw-tools.txt || echo nft=no | tee -a fw-tools.txt
```

**Expected output:** `listen-before.txt` and `fw-tools.txt` exist.

### Real-world scenario

You must open a temporary diagnostics port for a local health probe on a practice VM. Change control says: show current status, allow the port, prove curl works, then remove the hole. SSH must keep working the whole time.

### Step-by-step tasks

#### Task 1 – Status first (and protect SSH)

```bash
cd ~/rebash-networking/lab14
set -euo pipefail

if command -v ufw >/dev/null 2>&1; then
  sudo ufw status verbose 2>&1 | tee ufw-status-before.txt
  # Ensure SSH would be allowed if UFW is (or becomes) active
  sudo ufw allow OpenSSH 2>&1 | tee ufw-allow-ssh.txt || \
    sudo ufw allow 22/tcp 2>&1 | tee ufw-allow-ssh.txt || true
else
  echo "UFW not installed — using nft/iptables status only" | tee ufw-status-before.txt
fi

if command -v nft >/dev/null 2>&1; then
  sudo nft list ruleset 2>&1 | tee nft-before.txt || true
fi

# Record that we can still talk to localhost SSH port if present
ss -lnt '( sport = :22 )' 2>/dev/null | tee ssh-listen.txt || true
```

**Expected output:** Status files exist; SSH allow is recorded when UFW is present. You remain logged in.

#### Task 2 – Temporary localhost service + firewall allow

Use port **18080** so you do not collide with real web servers. Bind to `127.0.0.1` only.

```bash
cd ~/rebash-networking/lab14
set -euo pipefail

# Start a tiny HTTP server on localhost only
python3 - << 'PY' >http-server.log 2>&1 &
import http.server, socketserver
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"rebash-lab14-ok\n")
    def log_message(self, *args):
        pass
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", 18080), H) as s:
    s.handle_request()
PY
echo $! > http-server.pid
sleep 0.3

# Allow the lab port (UFW). This does not disable SSH.
if command -v ufw >/dev/null 2>&1; then
  sudo ufw allow from 127.0.0.1 to any port 18080 proto tcp comment 'rebash-lab14' \
    2>&1 | tee ufw-allow-18080.txt || \
  sudo ufw allow 18080/tcp comment 'rebash-lab14' 2>&1 | tee ufw-allow-18080.txt
  sudo ufw status numbered 2>&1 | tee ufw-status-after-allow.txt
fi

# Prove local access
curl -sS --max-time 3 http://127.0.0.1:18080/ | tee curl-local.txt
grep -q 'rebash-lab14-ok' curl-local.txt
```

**Expected output:** `curl-local.txt` contains `rebash-lab14-ok`. UFW status (if present) shows the lab allow.

#### Task 3 – Remove lab rule and pack evidence

```bash
cd ~/rebash-networking/lab14
set -euo pipefail

# Stop leftover python if still running
if [[ -f http-server.pid ]]; then
  kill "$(cat http-server.pid)" 2>/dev/null || true
  rm -f http-server.pid
fi
pkill -f 'rebash-lab14' 2>/dev/null || true

if command -v ufw >/dev/null 2>&1; then
  # Delete by rule number is interactive; delete by spec instead
  sudo ufw delete allow from 127.0.0.1 to any port 18080 proto tcp 2>&1 | tee ufw-delete.txt || \
    sudo ufw delete allow 18080/tcp 2>&1 | tee ufw-delete.txt || true
  sudo ufw status numbered 2>&1 | tee ufw-status-final.txt
fi

tar -czf firewall-evidence.tgz \
  admin-user.txt listen-before.txt fw-tools.txt \
  ufw-status-before.txt ufw-allow-ssh.txt ssh-listen.txt \
  ufw-allow-18080.txt ufw-status-after-allow.txt curl-local.txt \
  ufw-delete.txt ufw-status-final.txt nft-before.txt http-server.log \
  2>/dev/null || tar -czf firewall-evidence.tgz *.txt *.log 2>/dev/null || true

ls -l firewall-evidence.tgz | tee evidence-ls.txt
test -s firewall-evidence.tgz
```

**Expected output:** Lab port rule removed (or noted); `firewall-evidence.tgz` is non-empty.

### Validation steps

- [ ] SSH session still works after the lab
- [ ] `curl` to `127.0.0.1:18080` succeeded while the server ran
- [ ] Lab UFW rule deleted (check `ufw status`)
- [ ] No leftover python listener on 18080 (`ss -lnt | grep 18080` empty)
- [ ] `firewall-evidence.tgz` under `~/rebash-networking/lab14`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Locked out of SSH | Enabled default deny without allow | Use console/serial; `ufw allow OpenSSH`; reboot recovery |
| `curl` connection refused | Server exited after one request | Re-run Task 2 server block; use `handle_request` timing |
| `ufw delete` fails | Rule text mismatch | `sudo ufw status numbered` then delete the matching number carefully |
| Cloud VM still blocked | Security group | Open the port in SG — host UFW is not enough |

### Challenge exercise

Create script `sg-checklist.sh` that prints a three-line checklist comparing **host firewall**, **security group**, and **network ACL** (what each covers). Save output to `sg-checklist.txt`. No cloud API calls required — this is a design artefact for tickets.

### Learning outcomes

- Inspected firewall status before changing policy
- Used allow-before-enable thinking for SSH safety
- Added and removed a temporary local allow with proof
- Separated host firewall from cloud edge controls

### Cleanup

```bash
cd ~/rebash-networking/lab14
set -euo pipefail

if [[ -f http-server.pid ]]; then
  kill "$(cat http-server.pid)" 2>/dev/null || true
  rm -f http-server.pid
fi
# Ensure lab port is not left open
if command -v ufw >/dev/null 2>&1; then
  sudo ufw delete allow from 127.0.0.1 to any port 18080 proto tcp 2>/dev/null || true
  sudo ufw delete allow 18080/tcp 2>/dev/null || true
fi
# Do NOT run: ufw reset / iptables -F on a shared host
```

## Validation

- [ ] Lab finished under `~/rebash-networking/lab14/`
- [ ] You can explain stateful vs stateless filtering
- [ ] You can describe allow-before-enable for SSH
- [ ] You know host firewall ≠ cloud security group

## Code Walkthrough

Safe firewall changes usually follow:

1. **Second path in** — serial console / second SSH session  
2. **Status** — `ufw status verbose` / `nft list ruleset`  
3. **Allow SSH and required ports**  
4. **Enable or tighten** only after allows exist  
5. **Prove and document** — then remove temporary holes  

Production teams store UFW/nft under configuration management and review security groups in pull requests.

## Security Considerations

- Default deny inbound; explicit allows with comments and owners  
- Never leave lab ports on public interfaces  
- Restrict SSH by source IP or jump host where practical  
- Treat `0.0.0.0/0` on data stores as an incident  
- Log denials where capacity allows; alert on sudden policy changes  

## Common Mistakes

!!! warning "Enabling UFW before allowing SSH"
    You can lose remote access. **Fix:** `ufw allow OpenSSH` (or your SSH port) first; keep console access ready.

!!! warning "Opening the app port only on the host"
    Cloud security groups may still drop traffic. **Fix:** check SG and NACL as well as UFW.

!!! warning "Wide open ‘temporary’ database rules"
    Temporary becomes permanent. **Fix:** time-box, ticket, and delete in Cleanup.

!!! warning "Assuming REJECT and DROP feel the same"
    Clients see quick reset vs long timeout. **Fix:** choose consciously; document for support teams.

## Best Practices

- Allow before enable; deny by default in production  
- Comment every rule with ticket ID  
- Prefer security groups for cloud edge; keep host firewall aligned  
- Test with positive and negative cases  
- Review firewall diffs like code  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| SSH timeout after `ufw enable` | SSH not allowed | Console; allow OpenSSH; reload |
| App timeout from internet | SG/NACL/UFW mismatch | Trace each layer |
| Works on localhost only | Bound to 127.0.0.1 or missing remote allow | Confirm listen address and remote rules |
| Intermittent allow | Stateful vs asymmetric path | Fix routing/return path |
| DNS broken after tighten | UDP/TCP 53 blocked | Allow resolver paths |

## Summary

Firewalls enforce who may talk to which ports. Prefer least privilege, allow SSH before enabling default deny, and remember cloud security groups sit beside host UFW/nftables. Next, practise day-to-day diagnosis with the [Linux Networking Toolkit](linux-networking-toolkit.md).

## Interview Questions

**1. What is the difference between a stateful firewall and a stateless packet filter?**

??? success "Reveal answer"
    A **stateful** firewall tracks connections so return traffic for an allowed session is accepted automatically. A **stateless** filter judges each packet alone, so you must allow ephemeral return ports explicitly (common with some network ACLs). Production designs must know which layer is which.

**2. You must enable UFW on a remote Ubuntu VM. What order of operations keeps SSH safe?**

??? success "Reveal answer"
    Keep a **console/serial** session ready. Run `ufw allow OpenSSH` (or the real SSH port), verify with `ufw status`, then enable. Never enable default deny first. Prove a new SSH login still works before closing the console.

**3. How do cloud security groups differ from Linux UFW on the same VM?**

??? success "Reveal answer"
    **Security groups** filter at the cloud virtual interface (often the primary edge). **UFW** filters on the guest OS. Traffic must pass **both** if both are enforced. Debugging “port open in UFW but still blocked” usually means the SG or NACL is dropping packets.

**4. Why is `0.0.0.0/0` to a database port a problem even inside a VPC?**

??? success "Reveal answer"
    Anyone who reaches that network path (compromised app, wrong peer VPC, malware) can attempt login. Prefer allow-lists of app security groups or private subnets. Broad opens fail audits and increase blast radius (how many systems an attacker can touch).

**5. When would you use REJECT instead of DROP?**

??? success "Reveal answer"
    **REJECT** tells the client quickly that the port is closed (TCP reset / ICMP unreachable). **DROP** is silent and causes timeouts — sometimes preferred to slow scanners, but harder for friendly clients to debug. Choose based on operations needs and document it.

**6. A health check fails after a firewall change, but curl from the box works. What do you check?**

??? success "Reveal answer"
    Health checks often come from **different source IPs** (load balancer subnets, Kubernetes nodes). Localhost success does not prove remote allow rules. Check SG/UFW source CIDRs and that the probe protocol/port match (HTTP vs TCP).

**7. How do you prove least privilege for a firewall change in a ticket?**

??? success "Reveal answer"
    Show before/after `ufw status` or nft listings, the exact allow (port, proto, source), a successful test from the intended peer, and a **negative** test from a disallowed peer/port. Include cleanup of temporary rules.

## Related Tutorials

- [Networking for Cloud & DevOps – Overview](index.md)
- [NAT and Port Forwarding](nat-and-port-forwarding.md) *(previous)*
- [Linux Networking Toolkit](linux-networking-toolkit.md) *(next)*
- [Firewall Change Control and Production ACLs](firewall-change-control-and-production-acls.md)
- [Lab — DNS / firewall triage](../labs/networking-dns-firewall-triage.md)

## References

- [UFW — Community Help Wiki](https://help.ubuntu.com/community/UFW) — Ubuntu  
- [nftables wiki](https://wiki.nftables.org/) — Linux packet filter  
- [AWS security groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html) — cloud parallel  
- Track index: [Networking for Cloud & DevOps Engineers](index.md)
