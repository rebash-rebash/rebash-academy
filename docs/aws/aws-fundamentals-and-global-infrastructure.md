---
title: "AWS Fundamentals and Global Infrastructure"
description: "Learn what Amazon Web Services (AWS) is, how Regions, Availability Zones and edge locations work, the shared responsibility model, and how to use the AWS CLI and CloudShell safely."
difficulty: beginner
estimated_time: "40–55 min"
technology: aws
category: aws
module: "Module 1 · AWS Fundamentals"
career_paths:
  - cloud-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - aws
  - regions
  - availability-zones
  - shared-responsibility
  - aws-cli
prerequisites:
  - linux/index
  - networking/index
next:
  - aws/iam-identity-access-and-organizations
related:
  - networking/index
  - linux/index
labs: []
projects: []
interview: interview/aws
certifications:
  - AWS Certified Cloud Practitioner
  - AWS Certified Solutions Architect – Associate
tags:
  - aws
  - regions
  - availability-zones
  - edge-locations
  - shared-responsibility
  - aws-cli
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# AWS Fundamentals and Global Infrastructure

## Overview






Build a clear mental map of Amazon Web Services (AWS): Regions, Availability Zones (AZs), edge locations, the shared responsibility model, and safe first use of the AWS Command Line Interface (CLI) and CloudShell.

AWS is a global public cloud platform. Before you launch compute or open a Virtual Private Cloud (VPC), you need to know **where** resources live, **who** is responsible for security, and **how** you authenticate to the Application Programming Interface (API). Wrong Region choices create latency, compliance, and cost surprises; misunderstanding shared responsibility creates security gaps.

This course is **AWS for Cloud & DevOps Engineers** — production habits from day one, not console tourism.

!!! warning "Cost hygiene"
    Prefer **read-only** and **`--dry-run`** where supported. Tear down anything you create. Set a billing alarm before Module 4 labs. Optional [LocalStack](https://localstack.cloud/) can mirror CLI-shaped drills offline.

This is a core tutorial in **Module 1 · AWS Fundamentals** of the REBASH Academy **AWS for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites






- [Linux Fundamentals](../linux/index.md) — terminal comfort
- [Networking Fundamentals](../networking/index.md) — IP, DNS, HTTPS basics
- An AWS account (Free Tier eligible) or read-only access for discovery commands

## Learning Objectives






By the end of this tutorial, you will be able to:

- [ ] Explain what AWS is and which roles use it daily  
- [ ] Distinguish Regions, Availability Zones, edge locations, and specialised extensions  
- [ ] Apply the shared responsibility model in plain language  
- [ ] Choose a sensible home Region for labs  
- [ ] Decide when to use the AWS CLI versus CloudShell, and run read-only discovery

## Architecture






This topic’s control points and relationships are shown below.

![AWS global infrastructure](../assets/excalidraw/aws-global-infrastructure.svg)

## Theory






### What it is

**Amazon Web Services (AWS)** is a global public cloud: on-demand compute, storage, databases, networking, identity, and operations services that you consume through the Management Console, the **AWS Command Line Interface (CLI)**, Software Development Kits (SDKs), Infrastructure as Code (IaC), or browser-based **CloudShell**. You rent capacity and managed control planes; you do not buy racks. Billing is mostly usage-based, so every resource you leave running becomes a standing cost.

### Why it matters

Cloud and DevOps work is Regional by default. Pipelines, Terraform state, EC2, and VPC designs assume a home Region. SRE and platform teams choose Regions for latency, data residency, service coverage, and price. Misplacing a resource wastes time in the console; misunderstanding the **shared responsibility model** creates security gaps — blind trust in AWS or reinventing controls AWS already operates.

### How it works

1. Open an **account** (later an organisation). IAM is *global*; most data-plane services are Regional.  
2. Set a **default Region** (`AWS_DEFAULT_REGION` or `aws configure`).  
3. API calls hit Regional endpoints unless the service is global (IAM, Route 53, CloudFront, Organizations).  
4. Production workloads span **≥2 Availability Zones**; multi-Region is deliberate disaster recovery (DR).  
5. Authenticate with roles or Identity Center (Module 2) — not root or long-lived human access keys.

### Concept deep dive

- **What is AWS** — A collection of APIs and regional data centres that deliver infrastructure and platform services. Cloud Engineers provision; DevOps and platform teams automate; SRE operates reliability and cost. You interact via console, CLI, SDK, or IaC — the same APIs underneath.
- **Global Infrastructure** — The physical and logical footprint: Regions, Availability Zones, edge locations, and specialised extensions (Local Zones, Wavelength). Design for failure domains, not “the cloud” as one magic place.
- **Regions** — Named geographies such as `eu-west-1` or `us-east-1`. Most resources are Regional and do **not** auto-replicate elsewhere. Pick one home Region for labs; change only when latency, compliance, or service coverage requires it.
- **Availability Zones (AZs)** — Discrete data-centre complexes inside a Region with independent power and networking. Multi-AZ survives an AZ outage without a full Region failover. Production apps and databases should span at least two AZs.
- **Edge Locations** — Points of Presence used by CloudFront, Route 53, and Global Accelerator to serve content and DNS close to users. Edge reduces latency; it is **not** a substitute for multi-AZ application design.
- **Shared Responsibility Model** — AWS secures *of* the cloud (facilities, hardware, hypervisor, managed control planes). You secure *in* the cloud: identity, network config, encryption, guest operating systems, application code, and data classification. Managed services shift more to AWS; EC2 leaves more with you.
- **AWS CLI** — Local terminal tool for scripting, CI/CD, and IaC workflows. Install once, configure profiles, and reuse credentials (or SSO). **When to use the CLI:** automation, versioned scripts, CI runners, and day-to-day ops from your laptop.
- **CloudShell** — Browser shell with the CLI preinstalled, credentials tied to your console session. **When to use CloudShell:** quick discovery with no local install, or short console-adjacent checks. Prefer the CLI over CloudShell for pipelines and repeatable production automation.

### Key concepts and comparisons

| Concept | Scope | Production note |
|---------|-------|-----------------|
| Region | Geographic | One home Region for early labs |
| Availability Zone | Inside a Region | ≥2 AZs for production apps |
| Edge location | Global PoPs | Latency aid, not sole HA strategy |
| Shared responsibility | Always | Secure *in* vs *of* the cloud |
| AWS CLI | Local / CI | Automation and repeatable ops |
| CloudShell | Browser | Fast discovery; session-bound |
| Global services | IAM, Route 53, CloudFront, Organizations | Affect Regional workloads |
| Regional services | EC2, VPC, S3 data*, RDS | Create where you need them |

\*S3 bucket *names* are globally unique; object data and config are Regional.

### Common pitfalls

- Creating resources in the wrong Region and “losing” them in the console filter  
- Treating one AZ as highly available; assuming IAM is per-Region  
- Leaving Elastic IPs, NAT Gateways, or load balancers running after labs  
- Daily use of the root user; skipping billing alarms before compute labs  
- Assuming CloudShell replaces a proper CLI/SSO setup for production automation  
- Believing edge locations alone make an application multi-AZ resilient

## Hands-on Lab



!!! warning "Cost and account safety"
    Use a sandbox account. Prefer read-only calls. Destroy anything you create before leaving the lab.

### Objective

Use read-only AWS APIs to inventory and verify aspects of **AWS Fundamentals and Global Infrastructure** in a sandbox account.

### Prerequisites

- AWS CLI v2
- Credentials for a **sandbox** account (SSO or short-lived keys)

### Lab environment

Workspace: `~/rebash-aws/module-01`

Prefer `describe`/`list`/`get` APIs. Create resources only with an explicit destroy path.

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-aws/module-01 && cd ~/rebash-aws/module-01
```

### Real-world scenario

Security asks for evidence that **AWS Fundamentals and Global Infrastructure** is configured correctly. You gather CLI proof without click-ops drift.

### Step-by-step tasks

#### Task 1 – Prove caller identity

Every AWS change starts by knowing which account/role you are.

``` {.bash .ra-terminal title="Terminal"}
aws sts get-caller-identity | tee identity.json
aws configure get region || true
test -s identity.json
```

!!! example "Expected output"
    JSON includes Account, Arn, and UserId.


#### Task 2 – Collect topic signals

Inventory the service surface related to this module.

``` {.bash .ra-terminal title="Terminal"}
aws ec2 describe-vpcs --query 'Vpcs[].{Id:VpcId,Cidr:CidrBlock}' --output table 2>/dev/null | tee vpcs.txt || true
aws iam get-account-summary 2>/dev/null | tee iam-summary.json || true
tee notes.txt << 'EOF'
Record which APIs apply to this topic and any NotAuthorized errors for follow-up.
EOF
cat notes.txt
```

!!! example "Expected output"
    Evidence files created even if some APIs are denied.


### Validation steps

- [ ] identity.json present
- [ ] No long-lived keys committed to the repo

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Unable to locate credentials | No profile/SSO | Run `aws sso login` or export sandbox keys |
| AccessDenied | Least privilege | Use a role that can read the service — or document the deny |
| UnauthorizedOperation | Wrong region/account | Check `AWS_REGION` and account id |

### Challenge exercise

Enable a cost budget alarm in the sandbox (or document the console clicks) and screenshot/CLI-describe it.

### Learning outcomes

- Authenticated safely
- Captured read-only evidence
- Avoided unmanaged spend

### Cleanup

```bash
# Revoke/lab-expire any temporary keys you exported
# Do not leave EC2/ELB/NAT running
```

## Validation






- [ ] Lab commands run under `~/rebash-aws/module-01/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough






Production practice for **AWS Fundamentals and Global Infrastructure** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations






- Treat credentials and tokens for aws as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes






!!! warning "Creating resources in the wrong Region and “losing” them in the console filter  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating one AZ as highly available; assuming IAM is per-Region  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices






- Encode AWS Fundamentals and Global Infrastructure changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting






| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |

## Summary






**AWS Fundamentals and Global Infrastructure** is essential for Cloud and DevOps engineers working with aws. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions




1. Region versus Availability Zone versus Local Zone?
2. How do you choose a region for a new workload?
3. What does sts get-caller-identity prove?
4. Why are AZ names account-specific?
5. How does global infrastructure affect DR design?

!!! tip "Sample answer — question 2"
    Confirm identity/region with STS and CLI config first — many “outages” are wrong account/region.

!!! tip "Sample answer — question 4"
    Prefer short-lived credentials (SSO/OIDC). Limit allowed regions via SCP where appropriate.

## Related Tutorials






- [Course overview](index.md)
- [IAM, Identity Access, and Organizations](iam-identity-access-and-organizations.md)

## References






- [AWS Global Infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/)  
- [Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/)  
- [AWS CLI getting started](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)  
- [AWS CloudShell](https://docs.aws.amazon.com/cloudshell/latest/userguide/welcome.html)
