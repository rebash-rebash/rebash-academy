---
title: "Troubleshooting AWS"
description: "Debug production Amazon Web Services issues with a fixed ladder — EC2, IAM, VPC, DNS, storage, Lambda, EKS, and cost analysis — for Cloud, DevOps, and SRE on-call."
difficulty: expert
estimated_time: "55–75 min"
technology: aws
category: aws
module: "Module 16 · Troubleshooting"
career_paths:
  - cloud-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - aws
  - troubleshooting
  - iam
  - vpc
  - eks
  - lambda
prerequisites:
  - aws/production-aws-landing-zones
next:
  - aws/index
related:
  - aws/compute-ec2-asg-and-load-balancing
  - aws/vpc-networking-on-aws
  - aws/containers-ecs-eks-ecr
  - aws/serverless-on-aws
  - aws/cost-optimisation-on-aws
labs: []
projects: []
interview: interview/aws
certifications:
  - AWS Certified SysOps Administrator – Associate
  - AWS Certified DevOps Engineer – Professional
  - AWS Certified Solutions Architect – Associate
tags:
  - aws
  - troubleshooting
  - ec2
  - iam
  - vpc
  - lambda
  - eks
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Troubleshooting AWS

## Overview






Diagnose Amazon Web Services (AWS) production failures with a fixed order: confirm identity and blast radius, then walk the **EC2 → IAM → VPC → DNS → storage → Lambda → EKS → cost** ladder without random console clicking.

Most “AWS is down” tickets are permission denials, security group / route mistakes, DNS mispoints, or exhausted quotas — not Region-wide outages. Separate **control-plane errors** (API denied, wrong Region) from **data-plane symptoms** (timeouts, 5xx, CrashLoop). Capture evidence before you change anything.

!!! warning "Cost hygiene"
    Debugging can create expensive resources (NAT Gateways, extra load balancers, large CloudWatch Logs Insights queries). Delete temporary helpers and bound log query time ranges.

This is a core tutorial in **Module 16 · Troubleshooting** of the REBASH Academy **AWS for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites






- [Production AWS Landing Zones](production-aws-landing-zones.md)
- Working knowledge of Modules 2–11 (IAM, VPC, compute, storage, containers, serverless, observability)
- AWS CLI v2 and read access to the affected account

## Learning Objectives






By the end of this tutorial, you will be able to:

- [ ] Start every incident with caller identity, Region, and recent CloudTrail  
- [ ] Triage EC2 instance reachability vs application failure  
- [ ] Decode IAM explicit denies and missing `sts:AssumeRole`  
- [ ] Trace VPC path: SG → NACL → route → NAT/IGW → endpoint  
- [ ] Isolate DNS (Route 53) vs target health  
- [ ] Debug Lambda and EKS with logs, events, and auth  
- [ ] Use cost spikes as a signal (runaway resources)

## Architecture






This topic’s control points and relationships are shown below.

![Troubleshooting ladder](../assets/excalidraw/aws-troubleshooting.svg)

## Theory






### What it is

**Troubleshooting AWS** narrows failure domains with a fixed ladder (reorder only when the symptom already proves a layer). Prefer read-only evidence (CloudWatch, CloudTrail, Flow Logs, Health) before mutate.

| Step | Focus | First evidence |
|------|-------|----------------|
| 0 | Context | `sts get-caller-identity`, Region, Health, change window |
| 1 | EC2 | State, status checks, console output, SSM |
| 2 | IAM | Explicit Deny, missing Allow, SCP, resource policy |
| 3 | VPC | SG, NACL, routes, NAT/endpoints, Flow Logs |
| 4 | DNS | Route 53, health checks, resolver, TTL |
| 5 | Storage | EBS attach/KMS; S3 403 vs 404 |
| 6 | Lambda | Timeout, concurrency, VPC, IAM, DLQ |
| 7 | EKS | API / nodes / pods; access entries; CNI |
| 8 | Cost | Spend spike → runaway capacity, transfer, logs |

### Why it matters

MTTR collapses when you confuse IAM with routing. SRE on-call needs a playbook juniors can follow. SysOps/DevOps exams test “next diagnostic API.” Cost belongs on the ladder — “outage” can be five hundred GPUs or an unbounded Logs Insights bill.

### How it works

1. Stabilise: page owners, freeze risky deploys, note start time.
2. Prove identity, account, Region; define the symptom precisely.
3. Walk the ladder; never skip IAM on `AccessDenied`.
4. Compare working vs broken; check last deploy and CloudTrail.
5. Smallest reversible fix; validate; write the timeline.

### Concept deep dive

Method per layer: symptom → evidence → decide → next action.

**EC2 failures.** `describe-instances` → `describe-instance-status` (system vs instance) → console/serial log → SSM reachability → app logs. System check ≈ host/path; instance check ≈ guest OS/disk. Running but unreachable → VPC/IAM (instance profile) before reboot; capture console output first.

**IAM issues.** Reproduce as the same principal → CloudTrail `AccessDenied` → identity policy, boundary, **SCP**, resource policy, session tags → Policy Simulator. **Explicit Deny wins**; AdministratorAccess still fails under SCP. Cross-account: trust (`sts:AssumeRole`) *and* role permissions. Wrong Region often looks like “missing resource.”

**VPC connectivity.** Source ENI → SG egress → dest SG ingress → NACL (ephemeral ports) → route → NAT/IGW/endpoint → Flow Logs. For ALB: listener → target group → `describe-target-health` before changing SGs. Private subnet needs NAT or VPC endpoints for public AWS APIs.

**DNS problems.** `dig` from the client path → public/private zone → record correctness → Route 53 health/failover → resolver/TTL. Separate “wrong target in DNS” from “DNS right, target unhealthy.”

**Storage issues.** EBS: state → attachment → KMS usable? → guest mount/disk full. S3: `NoSuchKey` (404) vs `AccessDenied` (403) vs wrong Region → bucket policy + IAM + SSE-KMS → Block Public Access → lifecycle. Restores need matching Region/AZ and KMS key.

**Lambda failures.** Logs → duration vs timeout → throttling/concurrency → execution role → VPC ENI/subnet/SG → event source + DLQ → X-Ray. “Works locally” ≈ missing IAM, VPC egress, or timeout. Check DLQs for async failures.

**EKS troubleshooting.** Reach API server? → nodes Ready? → `kubectl describe`/events (Pending, ImagePull, CrashLoop) → capacity/AZ → CNI/SGs → IAM (IRSA/Pod Identity/access entries/`aws-auth`) → control-plane logs/CloudTrail. Separate control plane, data plane, and workload. Image pulls need ECR auth *and* network path.

**Cost analysis.** Cost Explorer by service → account/tag → inventory (ASG, NAT, transfer, log ingestion) → CloudTrail Create* bursts → scale down with change control. Spikes are usually misconfig, not a pricing bug.

### Key concepts and comparisons

| Symptom | Likely layer | First checks |
|---------|--------------|--------------|
| SSM fails, app OK | Instance profile / endpoints | SSM + IAM role |
| Timeout to ALB | SG / targets / NACL | Target health, Flow Logs |
| `AccessDenied` | IAM / SCP / resource policy | CloudTrail, simulator |
| NXDOMAIN / wrong IP | DNS | `dig`, Route 53 |
| Lambda OK locally | IAM / VPC / timeout | Logs, concurrency |
| Pods Pending | Capacity / CNI / quotas | `kubectl describe` |
| Bill doubled | Cost / runaway | Cost Explorer |

| Term | Meaning |
|------|---------|
| Explicit Deny | Wins over Allow |
| Status checks | EC2 path vs guest OS |
| Target health | LB view of backends |
| Quotas | Limits that look like random failure |

### Common pitfalls

- Changing SGs before listener/target health.
- Ignoring SCPs when AdministratorAccess “fails.”
- Wrong Region or account.
- Rebooting to “fix” IAM or DNS.
- Unbounded Logs Insights creating a cost incident.
- Calling every timeout an app bug before Flow Logs/Health.
- Mutating before capturing evidence.

## Hands-on Lab



!!! warning "Cost and account safety"
    Use a sandbox account. Prefer read-only calls. Destroy anything you create before leaving the lab.

### Objective

Use read-only AWS APIs to inventory and verify aspects of **Troubleshooting AWS** in a sandbox account.

### Prerequisites

- AWS CLI v2
- Credentials for a **sandbox** account (SSO or short-lived keys)

### Lab environment

Workspace: `~/rebash-aws/module-16`

Prefer `describe`/`list`/`get` APIs. Create resources only with an explicit destroy path.

```bash
mkdir -p ~/rebash-aws/module-16 && cd ~/rebash-aws/module-16
```

### Real-world scenario

Security asks for evidence that **Troubleshooting AWS** is configured correctly. You gather CLI proof without click-ops drift.

### Step-by-step tasks

#### Task 1 – Prove caller identity

Every AWS change starts by knowing which account/role you are.

```bash
aws sts get-caller-identity | tee identity.json
aws configure get region || true
test -s identity.json
```

**Expected output:** JSON includes Account, Arn, and UserId.

#### Task 2 – Collect topic signals

Inventory the service surface related to this module.

```bash
aws ec2 describe-vpcs --query 'Vpcs[].{Id:VpcId,Cidr:CidrBlock}' --output table 2>/dev/null | tee vpcs.txt || true
aws iam get-account-summary 2>/dev/null | tee iam-summary.json || true
tee notes.txt << 'EOF'
Record which APIs apply to this topic and any NotAuthorized errors for follow-up.
EOF
cat notes.txt
```

**Expected output:** Evidence files created even if some APIs are denied.

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






- [ ] Lab commands run under `~/rebash-aws/module-16/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough






Production practice for **Troubleshooting AWS** always combines:

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






!!! warning "Changing SGs before listener/target health."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Ignoring SCPs when AdministratorAccess “fails.”"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices






- Encode Troubleshooting AWS changes as code and review them in pull requests
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






Sixteen modules cover design, security, automation, cost, recovery — and on-call debugging with a shared playbook.

## Interview Questions




1. Your standard AWS incident triage order?
2. How does CloudTrail help API failures?
3. Wrong region symptoms?
4. Throttling versus access denied — how to tell?
5. How do you capture evidence for a post-incident review?

!!! tip "Sample answer — question 2"
    STS identity → region → exact error → CloudTrail/event history → blast radius.

!!! tip "Sample answer — question 4"
    Limit who can disable logging during incidents; use temporary elevated roles with expiry.

## Related Tutorials






- [Course overview](index.md)
- [Course overview](index.md) · [AWS interview prep](../interview/aws.md) · [Cheat sheet](../cheatsheets/aws.md)

## References






- [AWS Health Dashboard](https://health.aws.amazon.com/health/status)  
- [VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)  
- [IAM policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)  
- [Amazon EKS troubleshooting](https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html)
