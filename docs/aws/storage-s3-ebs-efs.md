---
title: "Storage: S3, EBS, and EFS"
description: "Choose and operate AWS storage: Amazon S3, Elastic Block Store (EBS), Elastic File System (EFS), FSx overview, storage classes, lifecycle policies, and encryption."
difficulty: intermediate
estimated_time: "50–65 min"
technology: aws
category: aws
module: "Module 5 · Storage"
career_paths:
  - cloud-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - s3
  - ebs
  - efs
  - storage-classes
  - encryption
prerequisites:
  - aws/compute-ec2-asg-and-load-balancing
next:
  - aws/databases-on-aws
related:
  - aws/compute-ec2-asg-and-load-balancing
  - linux/index
labs: []
projects: []
interview: interview/aws
certifications:
  - AWS Certified Solutions Architect – Associate
  - AWS Certified Cloud Practitioner
tags:
  - aws
  - s3
  - ebs
  - efs
  - storage
  - encryption
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Storage: S3, EBS, and EFS

## Overview






Select the right AWS storage service for each workload — Amazon Simple Storage Service (S3), Elastic Block Store (EBS), Elastic File System (EFS), and a brief Amazon FSx overview — and apply storage classes, lifecycle rules, and encryption correctly.

Cloud storage is not one product. **Block**, **file**, and **object** models solve different problems. Using EBS like a shared drive, or S3 like a POSIX disk, creates outages and surprise bills. This module gives Cloud and DevOps engineers a decision framework used in production architectures.

!!! warning "Cost"
    S3 requests, incomplete multipart uploads, and unused EBS volumes / snapshots cost money. Enable lifecycle rules, abort incomplete multipart uploads, and delete lab buckets/volumes. Prefer Free Tier–friendly sizes and short-lived objects.

This is a core tutorial in **Module 5 · Storage** of the REBASH Academy **AWS for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites






- [Compute: EC2, ASG, and Load Balancing](compute-ec2-asg-and-load-balancing.md)
- Comfortable with Linux filesystems and the AWS CLI

## Learning Objectives






By the end of this tutorial, you will be able to:

- [ ] Contrast object, block, and file storage on AWS (S3, EBS, EFS, FSx)  
- [ ] Apply S3 storage classes, lifecycle policies, and encryption options  
- [ ] Choose EBS volume types and snapshot strategy  
- [ ] Know when EFS or FSx fits shared file access  
- [ ] Enforce encryption at rest (SSE-S3, SSE-KMS, client-side) and in transit

## Architecture






This topic’s control points and relationships are shown below.

![AWS storage](../assets/excalidraw/aws-storage.svg)

## Theory






### What it is

Cloud storage on AWS is not one product. **Object**, **block**, and **file** models solve different problems. **Amazon Simple Storage Service (S3)** is an object store. **Elastic Block Store (EBS)** is durable block volumes for EC2. **Elastic File System (EFS)** is managed Network File System (NFS) shared across instances. **Amazon FSx** covers specialised managed file systems (Windows, Lustre, NetApp, OpenZFS). Using EBS like a shared drive, or S3 like a POSIX disk, creates outages and surprise bills.

### Why it matters

Pipelines push artefacts to S3; Terraform state often sits in S3 with DynamoDB locks. Platform teams enforce block public access, bucket policies, and KMS. SRE sets recovery objectives with versioning, snapshots, and AWS Backup. Wrong storage classes (Glacier for hot logs) add latency and restore fees; orphaned volumes and incomplete multipart uploads waste budget after labs.

### How it works

**S3:** Regional bucket → put/get by key → versioning / replication / Object Lock as needed. Prefer gateway VPC endpoints from private subnets.  
**EBS:** Volume in an AZ → attach to instance in the **same AZ** → format/mount → snapshot; copy snapshots for DR.  
**EFS:** Filesystem + mount targets per AZ → NFSv4 with correct security groups.  
**FSx:** SMB/Windows, Lustre HPC, or NetApp features — not the default for greenfield Linux web apps (prefer EFS or S3).

Lifecycle sketch: Standard → IA (30d) → Glacier Flexible (90d) → expire (365d); abort incomplete multipart after 7 days.

### Concept deep dive

- **S3** — Object storage via HTTP APIs. A **bucket** is a Regional container with a globally unique name. An object **key** is the path-like name inside the bucket. Scale is effectively unbounded for typical application and artefact workloads. Access is by API, not by mounting as a local disk (unless you add a gateway/tooling layer).
- **EBS** — Block volumes attached to EC2. Common types: `gp3` (general-purpose SSD), `io2`/`io2 Block Express` (provisioned IOPS), `st1`/`sc1` (throughput/cold HDD). **Snapshots** are incremental point-in-time backups stored in S3 behind the scenes; restore creates a new volume (optionally in another AZ/Region via copy).
- **EFS** — Elastic, multi-AZ NFS for shared POSIX access across an Auto Scaling group or containers. Pay for storage used and, depending on mode, throughput. Ideal when many instances need the same files concurrently.
- **FSx** — Managed file systems for specialised needs: **FSx for Windows File Server** (SMB, Active Directory), **FSx for Lustre** (high-throughput HPC and machine-learning training), **FSx for NetApp ONTAP** (enterprise NAS features, multiprotocol). Pick FSx when the protocol or performance profile exceeds EFS/S3.
- **Storage classes** — Trade durability access patterns against price: Standard, Intelligent-Tiering, Standard-IA, One Zone-IA, Glacier Instant Retrieval, Glacier Flexible Retrieval, Glacier Deep Archive. Hot paths stay on Standard or Intelligent-Tiering; archives move colder.
- **Lifecycle policies** — Rules that transition objects between classes or expire them, and that abort incomplete multipart uploads. Essential for cost control on logs, dumps, and CI artefacts.
- **Encryption** — **SSE-S3** (AES-256 managed by S3) is the simple default. **SSE-KMS** uses KMS keys for auditability and key policy control. **Client-side encryption** encrypts before upload; you manage keys and cannot rely on S3 to decrypt for you. Also encrypt EBS and EFS at rest, and use HTTPS/TLS in transit.

### Key concepts and comparisons

| Decision | Prefer |
|----------|--------|
| Static assets / dumps / artefacts | S3 |
| Database data directory / boot volume | EBS |
| Shared uploads across ASG members | EFS (or S3 if the app uses the object API) |
| Windows SMB / Lustre HPC / NetApp features | FSx family |
| Infrequent archives | S3 Glacier classes + lifecycle |
| Simple encryption default | SSE-S3 |
| Key policy and audit control | SSE-KMS (customer-managed keys) |
| Encrypt before the wire | Client-side encryption |

### Common pitfalls

- Public buckets “for just a minute”  
- Assuming EBS survives instance terminate without checking `DeleteOnTermination`  
- Trying to attach EBS across AZs — impossible; use snapshots or EFS  
- Leaving incomplete multipart uploads (ongoing storage charges)  
- Using One Zone-IA for critical multi-AZ data  
- Mounting EFS without TLS or the correct security group and blaming “hangs”  
- Choosing FSx for every shared-file need when EFS or S3 would suffice

## Hands-on Lab



!!! warning "Cost and account safety"
    Use a sandbox account. Prefer read-only calls. Destroy anything you create before leaving the lab.

### Objective

Use read-only AWS APIs to inventory and verify aspects of **Storage: S3, EBS, and EFS** in a sandbox account.

### Prerequisites

- AWS CLI v2
- Credentials for a **sandbox** account (SSO or short-lived keys)

### Lab environment

Workspace: `~/rebash-aws/module-05`

Prefer `describe`/`list`/`get` APIs. Create resources only with an explicit destroy path.

```bash
mkdir -p ~/rebash-aws/module-05 && cd ~/rebash-aws/module-05
```

### Real-world scenario

Security asks for evidence that **Storage: S3, EBS, and EFS** is configured correctly. You gather CLI proof without click-ops drift.

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






- [ ] Lab commands run under `~/rebash-aws/module-05/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough






Production practice for **Storage: S3, EBS, and EFS** always combines:

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






!!! warning "Public buckets “for just a minute”  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Assuming EBS survives instance terminate without checking `DeleteOnTermination`  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices






- Encode Storage: S3, EBS, and EFS changes as code and review them in pull requests
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






**Storage: S3, EBS, and EFS** is essential for Cloud and DevOps engineers working with aws. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions




1. S3 consistency model basics you rely on?
2. EBS versus EFS versus S3 for different workloads?
3. How do you prevent accidental public buckets?
4. What is versioning useful for?
5. Unattached EBS volumes — cost impact?

!!! tip "Sample answer — question 2"
    For access issues check bucket policy, Block Public Access, IAM, and the exact object key/region.

!!! tip "Sample answer — question 4"
    Block public access by default, encrypt where required, and delete lab buckets/objects when finished.

## Related Tutorials






- [Course overview](index.md)
- [Databases on AWS](databases-on-aws.md)

## References






- [Amazon S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)  
- [Amazon EBS](https://docs.aws.amazon.com/ebs/latest/userguide/what-is-ebs.html)  
- [Amazon EFS](https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html)  
- [Amazon FSx](https://aws.amazon.com/fsx/)
