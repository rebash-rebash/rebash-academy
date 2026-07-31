---
title: "Firewall Change Control and Production ACLs"
description: "Manage production firewall and ACL changes with least privilege, peer review, windowed rollout, validation, and rollback for Cloud and Linux filters."
difficulty: intermediate
estimated_time: "35–50 min"
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
  - change-control
  - acls
  - firewall-ops
prerequisites:
  - networking/load-balancer-operations-and-health-checks
next:
  - networking/network-troubleshooting-methodology
related:
  - networking/firewalls-and-access-control
  - networking/network-security-hardening
labs:
  - labs/networking-dns-firewall-triage
projects: []
interview: interview/networking
certifications:
  - CompTIA Network+
tags:
  - networking
  - firewall
  - change-control
  - acls
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Firewall Change Control and Production ACLs

## Overview

Ship firewall/ACL changes with review, blast-radius limits, proof of intent, and a tested rollback — without locking out production.

Most “security” outages are change outages. Treat SG/NSG/nft/UFW/NACL edits like production code: PR, plan, canary, verify, rollback.

This is a core tutorial in **Module 16 · Production Networking** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Firewalls and Access Control](firewalls-and-access-control.md)
- [Load Balancer Operations and Health Checks](load-balancer-operations-and-health-checks.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Write a change request with source, dest, port, justification, expiry  
- [ ] Prefer temporary breaks-glass with automatic expiry  
- [ ] Validate with positive and negative tests  
- [ ] Roll back quickly

## Architecture

This topic’s control points and relationships are shown below.

![Firewalls](../assets/excalidraw/firewalls-access-control.svg)

## Theory

### What it is

Firewall change control is the process that turns “please open port 443” into a reviewed, validated, reversible **Access Control List (ACL)** or security-group change. Production ACLs include cloud security groups, network ACLs, host firewalls, and perimeter rules. The artefact is a **change package**: intent, exact rule, risk, validation, rollback, and expiry for temporary allows.

### Why it matters

Untracked firewall edits cause outages (blocked health checks) and breaches (forgotten `0.0.0.0/0`). Dual control and Infrastructure as Code (IaC) exist because a single fat-finger can expose databases. Auditors ask who approved the rule and when it expires; “someone in Slack” is not an answer.

### How it works

1. Capture **intent** and ticket (who needs what, for how long).  
2. Specify the **exact rule**: source (CIDR or security group), protocol, port, direction.  
3. State **blast radius** (which apps break if wrong).  
4. List **validation** commands (`nc`, `curl`, flow logs) for before/after.  
5. Prepare **rollback** (previous IaC commit or explicit rule delete).  
6. Set **expiry** for break-glass allows and calendar a removal.

Apply in non-production first. Production needs dual review. Policy-as-code (Open Policy Agent, cloud SCPs, CI checks) should reject world-open data ports automatically.

### Key concepts and comparisons

| Package field | Example |
|---------------|---------|
| Intent | App → DB on 5432 from app SG only |
| Risk | Wrong SG → outage; wrong CIDR → exposure |
| Validation | `nc -vz db 5432` from app task |
| Rollback | Revert Terraform / delete rule ID |
| Expiry | Temporary vendor /30 for 72 hours |

| Guardrail | Purpose |
|-----------|---------|
| No `0.0.0.0/0` on data ports | Stop accidental exposure |
| Dual review | Two-person integrity |
| Non-prod first | Catch app breakage early |
| IaC only | No console drift |

### Common pitfalls

- Approving “open 443 to the world” without asking which identity.  
- Leaving temporary vendor access forever.  
- Validating from the wrong source network (your laptop ≠ the app subnet).  
- Changing NACLs and security groups without understanding stateless vs stateful behaviour.  
- No rollback tested before the maintenance window.

## Hands-on Lab

**Focus:** practise the core workflow for Firewall Change Control and Production ACLs

### Step 1 – Draft a change

```text
Allow: App SG → DB SG :5432
Why: new payment service
Validate: connect from app pod; deny from bastion
Rollback: revert PR abc123
```

### Step 2 – Negative test plan

Prove an unauthorised source still times out / is refused per policy.

### Step 3 – Emergency access

Document break-glass: who, how long, who audits after.

## Validation

- [ ] Lab commands run under `~/rebash-networking//`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Firewall Change Control and Production ACLs** always combines:

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

!!! warning "Approving “open 443 to the world” without asking which identity.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Leaving temporary vendor access forever.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Firewall Change Control and Production ACLs changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Change “works” but insecure | Too-broad CIDR | Narrow; prefer SG refs |
| Outage after apply | Denied health/admin | Rollback; add least allow |

## Summary

- Firewall changes need the same discipline as app deploys  
- Prove allow and deny  
- Temporary rules must expire

## Interview Questions

1. How does **Firewall Change Control and Production ACLs** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Network Troubleshooting Methodology](network-troubleshooting-methodology.md)

## References

- [ITIL change enablement (overview)](https://www.axelos.com/certifications/itil-service-management)
