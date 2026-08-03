---
title: "Network Segmentation and Trust Boundaries"
description: "Design tiered segments and trust boundaries, then prove allow and deny paths with a dmz/app/db Linux namespace reachability matrix."
difficulty: intermediate
estimated_time: "50–65 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: networking
technology: networking
module: "Module 16 · Production Networking"
tags:
  - networking
  - segmentation
  - zero-trust
  - trust-boundaries
prerequisites:
  - networking/network-security-hardening
next:
  - networking/network-automation-and-monitoring
related:
  - networking/firewalls-and-access-control
  - networking/kubernetes-networking-fundamentals
labs: []
interview: interview/networking
comments: false
---

# Network Segmentation and Trust Boundaries

## Overview

**Segmentation** splits a network into zones so a problem in one zone cannot freely reach every other zone. A **trust boundary** is the line where traffic must meet a stronger control — firewall rule, Security Group, Kubernetes NetworkPolicy, or identity check. Classic three-tier designs (edge / app / data) still matter; cloud SG graphs and NetworkPolicies are how you enforce them today.

In Cloud and DevOps work you map subnets and filters to those tiers: public edge (DMZ-like), application, and database. After one web tier compromise, the attacker should not open a direct path to the database. Micro-segmentation goes further — allow only the specific service identities that need to talk.

In production, flat networks turn one stolen credential into a wide outage or breach. Over-segmentation without clear allows breaks health checks and deployments. Good design states allowed paths in a matrix, then proves both **allow** and **deny**.

This is **Tutorial 22** in **Module 16: Production Networking** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series. It is written for Cloud, DevOps, Platform, SRE, and DevSecOps engineers. By the end you will run a dmz/app/db namespace lab with a reachability matrix under `~/rebash-networking/lab22`.

## Prerequisites

- [Network Security Hardening](network-security-hardening.md)
- [Firewalls and Access Control](firewalls-and-access-control.md)
- Practice Ubuntu VM with `sudo` and `iproute2` (`ip netns`, `veth`)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Define edge (DMZ), app, data, and admin trust boundaries
- [ ] Map subnets + Security Groups + policies to those boundaries
- [ ] Build a three-tier namespace model with veth links
- [ ] Produce a reachability matrix and prove a deny path
- [ ] Explain blast radius with a concrete failure story
- [ ] Relate micro-segmentation to identity-aware allows

## Architecture

Traffic should cross trust boundaries only on approved paths: edge → app → data, not edge → data directly.

![Network segmentation](../assets/excalidraw/network-segmentation.svg)

## Theory

### What it is

Segmentation places workloads into zones with different trust levels. East-west traffic inside a zone may be freer; north-south across boundaries is filtered. **Blast radius** is how much of the system an attacker or fault can reach after crossing one boundary (plain meaning: how wide the damage can spread).

```bash
# Conceptual allow list (cloud SG style)
# app-sg  -> db-sg :5432
# dmz-sg  -> app-sg :80
# dmz-sg  -X-> db-sg  (deny)
```

### Why it matters

Ransomware and credential theft move sideways on flat networks. Compliance regimes expect separation of data tiers. Kubernetes NetworkPolicies and cloud SG references are the enforcement points engineers actually operate. If you cannot show a deny path, you do not have segmentation — you have a diagram.

### How it works

1. **Name tiers** — edge/DMZ, app, data, admin/management.
2. **Place subnets** — often one subnet (or more) per tier per AZ.
3. **Write the matrix** — who may talk to whom on which port.
4. **Enforce** — SG/NSG, host firewall, NetworkPolicy, service mesh authz.
5. **Prove** — connectivity tests for allow and deny.
6. **Review** — temporary allows expire; IaC prevents silent widenings.

| From \\ To | DMZ/Edge | App | DB |
|------------|----------|-----|-----|
| Internet | Allow 443 (LB) | Deny | Deny |
| DMZ | — | Allow app ports | **Deny** |
| App | Limited | Peer as needed | Allow DB port |
| DB | Deny | Reply to app | Peer backups only |

### Common pitfalls

- Diagram without enforcement (no SG/NetworkPolicy)
- Allowing DMZ straight to DB “temporarily”
- Forgetting health-check / DNS paths in the matrix
- Micro-segmentation so tight that deploys fail without a canary plan
- Treating VLAN alone as enough in cloud (cloud filters are usually SG/policy)

## Hands-on Lab

### Objective

Create three namespaces (`dmz`, `app`, `db`) linked with veth pairs through a tiny router namespace. Allow DMZ→app and app→db; **deny** DMZ→db. Save a reachability matrix under `~/rebash-networking/lab22`.

### Prerequisites

- Ubuntu with `sudo`, `iproute2`, `ping`, `python3` (for a tiny HTTP listener) or `nc`
- Practice VM only — namespaces need root

### Lab environment

Workspace: `~/rebash-networking/lab22`

```bash title="Terminal"
mkdir -p ~/rebash-networking/lab22 && cd ~/rebash-networking/lab22
set -euo pipefail
whoami | tee admin-user.txt
```

!!! example "Expected output"
    workspace ready.


### Real-world scenario

Your platform team wants a simple proof that the edge tier cannot open the database directly. Before changing cloud Security Groups, you build a namespace model that matches the intended matrix and attach the deny evidence to the design review.

### Step-by-step tasks

#### Task 1 – Build dmz / app / db namespaces

```bash title="Terminal"
cd ~/rebash-networking/lab22
set -euo pipefail

for ns in lab22-dmz lab22-app lab22-db lab22-rtr; do
  sudo ip netns del "$ns" 2>/dev/null || true
done
for ns in lab22-dmz lab22-app lab22-db lab22-rtr; do
  sudo ip netns add "$ns"
  sudo ip -n "$ns" link set lo up
done

# dmz 10.22.1.0/24, app 10.22.2.0/24, db 10.22.3.0/24 via router
sudo ip link add v-dmz type veth peer name r-dmz
sudo ip link add v-app type veth peer name r-app
sudo ip link add v-db type veth peer name r-db
sudo ip link set v-dmz netns lab22-dmz
sudo ip link set v-app netns lab22-app
sudo ip link set v-db netns lab22-db
sudo ip link set r-dmz netns lab22-rtr
sudo ip link set r-app netns lab22-rtr
sudo ip link set r-db netns lab22-rtr

sudo ip -n lab22-dmz addr add 10.22.1.10/24 dev v-dmz
sudo ip -n lab22-app addr add 10.22.2.10/24 dev v-app
sudo ip -n lab22-db addr add 10.22.3.10/24 dev v-db
sudo ip -n lab22-rtr addr add 10.22.1.1/24 dev r-dmz
sudo ip -n lab22-rtr addr add 10.22.2.1/24 dev r-app
sudo ip -n lab22-rtr addr add 10.22.3.1/24 dev r-db

for nsdev in "lab22-dmz:v-dmz" "lab22-app:v-app" "lab22-db:v-db" "lab22-rtr:r-dmz" "lab22-rtr:r-app" "lab22-rtr:r-db"; do
  ns="${nsdev%%:*}"; dev="${nsdev##*:}"
  sudo ip -n "$ns" link set "$dev" up
done

sudo ip -n lab22-dmz route add default via 10.22.1.1
sudo ip -n lab22-app route add default via 10.22.2.1
sudo ip -n lab22-db route add default via 10.22.3.1
sudo ip netns exec lab22-rtr sysctl -w net.ipv4.ip_forward=1 >/dev/null

sudo ip -n lab22-rtr addr | tee topology-addrs.txt
```

!!! example "Expected output"
    three tiers addressing through `lab22-rtr`.


#### Task 2 – Enforce deny DMZ→DB with router iptables / nft

```bash title="Terminal"
cd ~/rebash-networking/lab22
set -euo pipefail

# Prefer iptables in the router namespace; flush lab chain first
sudo ip netns exec lab22-rtr iptables -F FORWARD 2>/dev/null || true
sudo ip netns exec lab22-rtr iptables -P FORWARD DROP
# Allow established
sudo ip netns exec lab22-rtr iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
# Allow dmz -> app
sudo ip netns exec lab22-rtr iptables -A FORWARD -s 10.22.1.0/24 -d 10.22.2.0/24 -j ACCEPT
# Allow app -> db
sudo ip netns exec lab22-rtr iptables -A FORWARD -s 10.22.2.0/24 -d 10.22.3.0/24 -j ACCEPT
# Allow app -> dmz replies path already covered by ESTABLISHED; optional app->dmz new:
sudo ip netns exec lab22-rtr iptables -A FORWARD -s 10.22.2.0/24 -d 10.22.1.0/24 -j ACCEPT
# Explicit deny dmz -> db (also covered by policy DROP, but log-friendly reject)
sudo ip netns exec lab22-rtr iptables -A FORWARD -s 10.22.1.0/24 -d 10.22.3.0/24 -j REJECT

sudo ip netns exec lab22-rtr iptables -L FORWARD -n -v | tee forward-rules.txt
```

!!! example "Expected output"
    FORWARD policy DROP with allow dmz→app and app→db; dmz→db rejected.


#### Task 3 – Reachability matrix (allow and deny proof)

```bash title="Terminal"
cd ~/rebash-networking/lab22
set -euo pipefail

probe() {
  local from="$1" to="$2" ip="$3"
  if sudo ip netns exec "$from" ping -c 1 -W 1 "$ip" >/dev/null 2>&1; then
    echo "$from -> $to ($ip): ALLOW"
  else
    echo "$from -> $to ($ip): DENY"
  fi
}

{
  echo "reachability_matrix"
  probe lab22-dmz app 10.22.2.10
  probe lab22-app db 10.22.3.10
  probe lab22-dmz db 10.22.3.10
  probe lab22-db app 10.22.2.10
} | tee matrix.txt

grep -q 'lab22-dmz -> app .*ALLOW' matrix.txt
grep -q 'lab22-app -> db .*ALLOW' matrix.txt
grep -q 'lab22-dmz -> db .*DENY' matrix.txt

tar -czf segmentation-evidence.tgz \
  admin-user.txt topology-addrs.txt forward-rules.txt matrix.txt
ls -l segmentation-evidence.tgz | tee evidence-ls.txt
```

!!! example "Expected output"
    matrix shows ALLOW for dmz→app and app→db, **DENY** for dmz→db.


### Validation steps

- [ ] Namespaces `lab22-dmz`, `lab22-app`, `lab22-db` exist during the lab
- [ ] `matrix.txt` proves deny on dmz→db
- [ ] FORWARD rules documented in `forward-rules.txt`
- [ ] Evidence archive under `~/rebash-networking/lab22`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| All pings DENY | Forwarding off or policy DROP without allows | Re-run Task 1–2; check `ip_forward=1` |
| dmz→db ALLOW | Missing reject / wrong order | Flush FORWARD and re-apply Task 2 |
| `iptables: No chain/target` | iptables not installed | Install `iptables` package on Ubuntu |
| `Cannot open network namespace` | No sudo | Use practice VM with sudo |

### Challenge exercise

Add a tiny HTTP service in `lab22-app` on port `8080` (`python3 -m http.server` bound to `10.22.2.10`) and allow only TCP 8080 from DMZ using an extra iptables rule. Prove `curl` from DMZ works and that DMZ still cannot reach DB. Save `curl-dmz-to-app.txt`.

### Learning outcomes

- Modelled three-tier trust boundaries with namespaces
- Enforced allow and deny at the router
- Produced a matrix suitable for a design review

### Cleanup

```bash title="Terminal"
cd ~/rebash-networking/lab22
set -euo pipefail
for ns in lab22-dmz lab22-app lab22-db lab22-rtr; do
  sudo ip netns del "$ns" 2>/dev/null || true
done
```

## Validation

- [ ] Lab finished under `~/rebash-networking/lab22/`
- [ ] You can draw edge/app/data boundaries and name controls
- [ ] You can explain blast radius in plain language
- [ ] You know how SG/NetworkPolicy maps to the matrix

## Code Walkthrough

Production segmentation usually follows:

1. **Write the matrix** before opening ports
2. **Enforce in IaC** — SG references, NetworkPolicies
3. **Prove allow and deny** with tests in CI or a lab
4. **Prefer identity-aware allows** (SG→SG, service accounts) over wide CIDRs
5. **Expire temporary cross-tier breaks**

## Security Considerations

- Never leave DMZ→DB open for debugging
- Log denies at boundaries during incidents
- Separate admin networks from data planes
- In Kubernetes, default-deny NetworkPolicies carefully with DNS exceptions
- Review peerings and shared services that bypass tier diagrams

## Common Mistakes

!!! warning "Pretty diagram, flat Security Groups"
    Without enforcement, segmentation is fiction. **Fix:** map each arrow to an SG/NetworkPolicy rule and a test.

!!! warning "Temporary DMZ→DB rule left forever"
    Attackers love forgotten allows. **Fix:** expiry dates, IaC review, automated drift detection.

!!! warning "Blocking health checks across tiers"
    Load balancers fail and rollbacks look like outages. **Fix:** include probe paths in the matrix.

!!! warning "Equating VLAN ID with cloud segmentation"
    Cloud routing and SG/NSG decide reachability. **Fix:** design filters explicitly per tier.

## Best Practices

- One matrix per environment (dev/stage/prod may differ)
- SG→SG or namespace selectors instead of `/0` sources
- Prove deny paths in the same ticket as allow paths
- Align Kubernetes NetworkPolicies with the same tier story
- Document shared services (DNS, monitoring) as first-class matrix rows

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| App cannot reach DB | Missing allow / wrong SG | Check matrix vs live rules |
| Edge reaches DB | Over-broad allow | Remove rule; add deny proof |
| Intermittent allow | Asymmetric path / stateful mismatch | Check return path and conntrack |
| K8s DNS breaks after NetworkPolicy | Forgot DNS egress | Allow kube-dns / CoreDNS |

## Summary

Segmentation limits how far damage can spread. Define trust boundaries, enforce them with filters, and prove both allow and deny. Next, automate probes and alerts in [Network Automation and Monitoring](network-automation-and-monitoring.md).

## Interview Questions

**1. What is a trust boundary in networking?**

??? success "Reveal answer"
    A trust boundary is where traffic moves between zones of different trust and must meet a stronger control — for example edge to app, or app to database — enforced by firewalls, Security Groups, or NetworkPolicies.

**2. Why should the DMZ/edge not talk directly to the database tier?**

??? success "Reveal answer"
    If the edge is compromised (common internet-facing risk), a direct path to the database makes data theft or ransomware much easier. The app tier should be the only consumer of the DB port, with its own tighter controls.

**3. How do cloud Security Groups implement segmentation?**

??? success "Reveal answer"
    Attach different SGs to edge, app, and data instances/ENIs. Allow **app SG → db SG on the DB port**, and do **not** allow the edge SG to the DB SG. Prefer SG references over wide CIDR lists.

**4. What is blast radius, in plain language?**

??? success "Reveal answer"
    Blast radius is **how much of the system can be hurt** after one fault or compromise. Segmentation aims to keep that damage inside one tier or service instead of the whole network.

**5. How would you prove segmentation works in an interview or ticket?**

??? success "Reveal answer"
    Show a reachability matrix with an **ALLOW** test for intended paths and a **DENY** test for forbidden paths (for example edge→DB fails). Attach command output. Diagrams alone are not proof.

**6. What is micro-segmentation?**

??? success "Reveal answer"
    Finer allows than big VLAN tiers — often per service or identity (SG pairs, NetworkPolicies, service mesh authorisation). It reduces lateral movement further but needs clear ownership or it becomes an outage generator.

**7. A Kubernetes NetworkPolicy default-deny breaks DNS. What happened?**

??? success "Reveal answer"
    Pods must reach CoreDNS (kube-dns) on UDP/TCP 53. A default-deny without a DNS allow blocks name resolution and looks like a total network failure. Add an explicit DNS egress rule (or equivalent) in the policy design.

## Related Tutorials

- [Networking for Cloud & DevOps – Overview](index.md)
- [Network Security Hardening](network-security-hardening.md) *(previous)*
- [Network Automation and Monitoring](network-automation-and-monitoring.md) *(next)*
- [Firewalls and Access Control](firewalls-and-access-control.md)
- [Kubernetes Networking Fundamentals](kubernetes-networking-fundamentals.md)

## References

- [AWS Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
- [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- Track index: [Networking for Cloud & DevOps Engineers](index.md)
