---
title: "Network Segmentation and Trust Boundaries"
description: "Design tiered network segments, trust boundaries, micro-segmentation ideas, and blast-radius reduction for production Cloud and Kubernetes environments."
difficulty: intermediate
estimated_time: "40–55 min"
technology: networking
category: networking
module: "Module 16 · Production Networking"
career_paths:
  - devops-engineer
  - cloud-engineer
  - site-reliability-engineer
  - platform-engineer
  - devsecops-engineer
skills:
  - segmentation
  - trust-boundaries
  - microsegmentation
prerequisites:
  - networking/network-security-hardening
next:
  - networking/network-automation-and-monitoring
related:
  - networking/firewalls-and-access-control
  - networking/kubernetes-networking-fundamentals
labs: []
projects: []
interview: interview/networking
certifications:
  - CompTIA Network+
  - AWS SAA
tags:
  - networking
  - segmentation
  - zero-trust
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Network Segmentation and Trust Boundaries

## Overview

Draw clear trust boundaries (edge, app, data, admin) and justify controls that stop lateral movement after a single tier is compromised.

**Segmentation** splits networks so a breach in one zone cannot freely reach others. Classic three-tier designs still matter; Kubernetes **NetworkPolicies** and cloud SG graphs are the modern enforcement points.

This is a core tutorial in **Module 16 · Production Networking** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Network Security Hardening](network-security-hardening.md)
- [Firewalls and Access Control](firewalls-and-access-control.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Define edge / app / data / admin boundaries  
- [ ] Map subnets + SGs + policies to those boundaries  
- [ ] Explain blast radius with a concrete failure story  
- [ ] Relate micro-segmentation to identity-aware allows

## Architecture

This topic’s control points and relationships are shown below.

![Network segmentation](../assets/excalidraw/network-segmentation.svg)

## Theory

### What it is

Network segmentation divides systems into **zones** with different trust levels and controlled paths between them. A **trust boundary** is any place policy must be enforced — security group, network access control list (NACL), firewall, Kubernetes NetworkPolicy, API gateway, or service mesh authorisation. The goal is not “more VLANs for decoration”; it is limiting blast radius when a host or token is compromised.

### Why it matters

Flat networks turn one phishing foothold into lateral movement across data stores. Compliance regimes expect separation of admin planes and customer data. Cloud Virtual Private Clouds (VPCs) that are merely “private” are still flat inside unless security groups and identity enforce who may talk to whom. Segmentation is how DevOps designs failure and breach containment before the incident.

### How it works

Define zones (public edge, application, data, admin). Place only load balancers and Web Application Firewalls (WAFs) on the untrusted edge. Application tiers accept traffic from the edge or mesh, not from the internet. Data tiers accept only from app identities/security groups. Admin access arrives via Virtual Private Network (VPN) or bastion with break-glass controls — not from app subnets by default. Prefer **micro-segmentation**: security-group-to-security-group or workload identity over trusting an entire Classless Inter-Domain Routing (CIDR). Document every boundary and the control that enforces it.

### Key concepts and comparisons

| Zone | Trust | Allows |
|------|-------|--------|
| Public edge | Untrusted clients | LB / WAF only |
| App | Semi-trusted | From edge / mesh |
| Data | High value | From app only |
| Admin | Break-glass | VPN / bastion only |

| Control | Typical layer |
|---------|----------------|
| Security group / NSG | Cloud instance/ENI |
| NACL / firewall | Subnet / perimeter |
| NetworkPolicy | Kubernetes Pod |
| Identity-aware proxy | Human / service authz |

### Common pitfalls

- Equating “private IP” with “trusted.”  
- Wide `0.0.0.0/0` on data ports “temporarily.”  
- Skipping egress controls so malware phones home freely.  
- Overlapping CIDRs that block future VPC peering or VPN.  
- Policies in diagrams that were never applied in IaC.

## Hands-on Lab

**Focus:** practise the core workflow for Network Segmentation and Trust Boundaries

### Step 1 – Draw zones

In `segments.md`, list CIDRs or SG names per zone for a sample 3-tier app.

### Step 2 – Lateral movement story

Assume web tier RCE: which rules stop SSH to DB? Which allow east-west you should remove?

### Step 3 – Kubernetes note

Map: namespace + NetworkPolicy default deny ingress; allow from ingress controller and peer app labels only.

## Validation

- [ ] Lab commands run under `~/rebash-networking//`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Network Segmentation and Trust Boundaries** always combines:

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

!!! warning "Equating “private IP” with “trusted.”  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Wide `0.0.0.0/0` on data ports “temporarily.”  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Network Segmentation and Trust Boundaries changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| App cannot reach DB | Over-segmentation | Add least-privilege allow; verify labels/SGs |
| Flat network | Everything in one SG | Split SGs; default deny |

## Summary

- Segments exist to bound blast radius  
- Enforce at every trust boundary, not only the edge  
- Private ≠ trusted

## Interview Questions

1. How does **Network Segmentation and Trust Boundaries** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Network Automation and Monitoring](network-automation-and-monitoring.md)

## References

- [NIST Zero Trust architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final)
