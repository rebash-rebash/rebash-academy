---
title: "Cloud Networking — VPCs and Subnets"
description: "Design multi-AZ VPCs with public and private subnets, gateways, route tables, and compare AWS, Azure, and Google Cloud networking building blocks."
difficulty: intermediate
estimated_time: "55–70 min"
technology: networking
category: networking
module: "Module 15 · Cloud Networking"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - site-reliability-engineer
  - platform-engineer
  - kubernetes-engineer
skills:
  - vpc
  - subnets
  - route-tables
  - nat-gateway
  - multi-cloud
prerequisites:
  - networking/kubernetes-networking-fundamentals
next:
  - networking/vpn-and-tunneling-basics
related:
  - networking/routing-fundamentals
  - networking/nat-and-port-forwarding
  - networking/firewalls-and-access-control
labs: []
projects: []
interview: interview/networking
certifications:
  - AWS SAA
  - Azure AZ-104
  - Google ACE
tags:
  - networking
  - vpc
  - cloud
  - aws
  - gcp
  - azure
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Cloud Networking — VPCs and Subnets

## Overview

Design a multi-AZ public/private VPC (or VNet), explain IGW/NAT/route tables and SG/NACL (or equivalents), and map the same pattern across AWS, Azure, and Google Cloud.

A **VPC (Virtual Private Cloud)** — Azure **Virtual Network**, GCP **VPC** — is your isolated Layer-3 network in the cloud. Wrong CIDRs, routes, or public/private placement cause outages that look like “the app is down.”

This is **Module 15 — Cloud Networking**. Complete prior modules through Kubernetes networking. Diagrams use Excalidraw only.

This is a core tutorial in **Module 15 · Cloud Networking** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Routing Fundamentals](routing-fundamentals.md)
- [NAT and Port Forwarding](nat-and-port-forwarding.md)
- [Firewalls and Access Control](firewalls-and-access-control.md)
- Comfort with CIDR notation

### Recommended

- Cloud account + CLI (`aws`, `az`, or `gcloud`) for read-only inspection labs

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain VPC isolation and CIDR planning  
- [ ] Design public vs private subnets across AZs  
- [ ] Wire IGW, NAT, and route tables correctly  
- [ ] Compare AWS / Azure / GCP control names  
- [ ] Avoid overlapping CIDRs for hybrid/peering  
- [ ] Validate connectivity with routes and reachability checks

## Architecture

Multi-AZ VPC: public subnets for LB/NAT, private for app/data, IGW for internet.

![Cloud VPC](../assets/excalidraw/cloud-vpc.svg)

## Theory

### VPC essentials

You choose a CIDR (e.g. `10.0.0.0/16`), carve **subnets** (often `/24` per tier per AZ), attach **route tables**, and control access with **Security Groups / NSGs / VPC firewall rules** plus optional **NACLs**.

### Public vs private

| Subnet | Default route | Typical workloads |
|--------|---------------|-------------------|
| Public | `0.0.0.0/0` → **Internet Gateway** | Load balancers, bastion, NAT GW |
| Private | `0.0.0.0/0` → **NAT Gateway** / Cloud NAT | Apps, databases, internal APIs |

Private instances keep private IPs; outbound uses SNAT via NAT. Inbound from internet goes to public LB, not straight to data tiers.

### Multi-AZ

Place subnets in ≥2 AZs. Prefer **NAT per AZ** to avoid cross-AZ SPOF and surprise data charges. Load balancers span AZs; databases use Multi-AZ or regional patterns.

### Provider name map

| Concept | AWS | Azure | GCP |
|---------|-----|-------|-----|
| Network | VPC | Virtual Network | VPC |
| Subnet | Subnet | Subnet | Subnet |
| Internet edge | Internet Gateway | None (default system routes) / Public IP | Internet Gateway (implicit via routes) |
| Outbound NAT | NAT Gateway | NAT Gateway | Cloud NAT |
| Stateful host filter | Security Group | NSG | VPC firewall rules |
| Stateless subnet filter | NACL | — (NSG is primary) | Hierarchical firewall / policies |
| DNS | Route 53 | Azure DNS | Cloud DNS |
| Hub connectivity | Transit Gateway | Virtual WAN / peering | Cloud Router / NCC |
| L7 LB | ALB | Application Gateway | HTTP(S) LB |
| Private service | PrivateLink | Private Link | Private Service Connect |

Exact GCP internet routing differs (routes + Cloud NAT); learn the **pattern**, then the console labels.

### CIDR planning

- Non-overlap with on-prem and peered VPCs  
- Leave headroom for expansion  
- Document reserved ranges for future clusters / shared services

## Hands-on Lab

**Focus:** practise the core workflow for Cloud Networking — VPCs and Subnets

```bash
mkdir -p ~/rebash-networking/module-15
cd ~/rebash-networking/module-15
```

Authenticate at least one cloud CLI if available:

```bash
aws sts get-caller-identity 2>/dev/null || true
az account show 2>/dev/null || true
gcloud config get-value project 2>/dev/null || true
```

### Step 1 – Design on paper

Create `vpc-design.md`:

```text
VPC: 10.20.0.0/16
AZ-a public:  10.20.0.0/24
AZ-a private: 10.20.10.0/24
AZ-b public:  10.20.1.0/24
AZ-b private: 10.20.11.0/24
Public RT: 0.0.0.0/0 → IGW
Private RT: 0.0.0.0/0 → NAT (per AZ)
```

### Step 2 – Route table quiz

For each destination, which gateway?

1. Private app → `pypi.org`  
2. ALB in public subnet → client on internet  
3. Private app → RDS in another private subnet  

### Step 3 – Read-only cloud inspection (if CLI works)

```bash
# AWS example
aws ec2 describe-vpcs --query 'Vpcs[].{Id:VpcId,Cidr:CidrBlock}' --output table 2>/dev/null || true
aws ec2 describe-route-tables --query 'RouteTables[].{Id:RouteTableId,Vpc:VpcId}' --output table 2>/dev/null || true
```

### Step 4 – Security mapping

Reuse Module 11: Web SG / App SG / DB SG. Note where NSG/firewall rules attach (NIC vs subnet).

### Step 5 – Hybrid readiness

List three CIDRs you must not collide with (corporate `10.0.0.0/8` slices, other VPCs, Kubernetes pod CIDRs).

## Validation

- [ ] Lab commands run under `~/rebash-networking/module-15/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Cloud Networking — VPCs and Subnets** always combines:

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

!!! warning "Skipping fundamentals for Cloud Networking — VPCs and Subnets"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Cloud Networking — VPCs and Subnets"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Cloud Networking — VPCs and Subnets changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| No outbound from private | Missing NAT route | Fix private RT → NAT |
| No inbound to app | App in public without LB / SG | Prefer private + public LB |
| Peering fails | Overlapping CIDR | Re-IP or redesign |
| Cross-AZ cost / SPOF | Single NAT | NAT per AZ |
| DNS works, TCP fails | SG/NSG/NACL | Module 11 checklist |

## Summary

- VPC = your cloud L3 boundary + subnets + routes + filters  
- Public for edge; private for compute/data; NAT for outbound  
- Multi-AZ is mandatory for production  
- Same architecture, different product names across clouds

## Interview Questions

1. How does **Cloud Networking — VPCs and Subnets** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [VPN and Tunneling Basics](vpn-and-tunneling-basics.md)  
- [Network Segmentation and Trust Boundaries](network-segmentation-and-trust-boundaries.md)

## References

- [AWS VPC](https://docs.aws.amazon.com/vpc/latest/userguide/)  
- [Azure Virtual Network](https://learn.microsoft.com/azure/virtual-network/)  
- [Google Cloud VPC](https://cloud.google.com/vpc/docs)
