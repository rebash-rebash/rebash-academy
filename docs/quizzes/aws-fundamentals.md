---
title: "Quiz — AWS Fundamentals"
description: "40-question assessment on AWS foundations: IAM, billing, VPC, EC2/SSM, S3, load balancing, RDS, CloudWatch, CloudTrail, and shared responsibility."
difficulty: intermediate
estimated_time: "45–60 min"
passing_score: "70% (28/40)"
author: Shaik Basha
last_updated: "2026-07-28"
category: quizzes
tags:
  - quizzes
  - aws
  - assessment
comments: false
---

# Quiz — AWS Fundamentals

## Quiz Overview

Assess the REBASH Academy AWS track through Module 6: identity, networking, compute, storage, edge, data, and operations.

| Attribute | Value |
|-----------|--------|
| Topic | AWS fundamentals and production hygiene |
| Questions | 40 |
| Passing score | 70% (28 correct) |
| Estimated time | 45–60 minutes |

!!! tip "How to use this quiz"
    Select an answer for each question, then **Submit quiz** for a scored result. Progress is saved in this browser. Explanations unlock after you submit.

## Learning Objectives

- [ ] Explain IAM identities, policies, and the shared responsibility model
- [ ] Apply VPC, security group, and routing concepts to reachability problems
- [ ] Choose appropriate EC2 admin patterns (SSM vs SSH) and S3 security controls
- [ ] Compare ALB vs NLB and reason about RDS and Free Tier cost traps
- [ ] Use CloudWatch and CloudTrail in operational triage

## Section 1 — Fundamentals

### Question 1

In the AWS shared responsibility model, which task is **always** the customer's responsibility?

**Difficulty:** Beginner

**Options:**

- **A.** Patching the guest operating system on EC2
- **B.** Physical data centre security
- **C.** Hypervisor maintenance on Nitro hosts
- **D.** Managed RDS engine minor version auto-apply (when enabled)

??? success "Reveal answer"
    **Correct answer: A**

    AWS secures the cloud; customers secure **in** the cloud — including OS patching on EC2 they manage.

    **Related concepts**

    - Shared responsibility
    - EC2 vs managed services

### Question 2

What does `aws sts get-caller-identity` return?

**Difficulty:** Beginner

**Options:**

- **A.** Only the AWS account password expiry date
- **B.** VPC flow log entries for the last hour
- **C.** Account ID, ARN, and UserId for the active credentials
- **D.** S3 bucket policy JSON

??? success "Reveal answer"
    **Correct answer: C**

    Use it first in triage to confirm **who** the CLI is acting as.

    **Related concepts**

    - STS
    - CLI profiles

### Question 3

Which IAM entity should an EC2 application use to call S3 without long-lived access keys on disk?

**Difficulty:** Beginner

**Options:**

- **A.** Root user access key
- **B.** IAM role attached via instance profile
- **C.** IAM user access key in `/etc/environment`
- **D.** Public S3 ACL

??? success "Reveal answer"
    **Correct answer: B**

    Instance profiles deliver temporary credentials via IMDS.

    **Related concepts**

    - Instance profiles
    - Least privilege

### Question 4

AWS Free Tier billing hygiene best practice for labs is?

**Difficulty:** Beginner

**Options:**

- **A.** Leave NAT Gateways running for faster next lab
- **B.** Share root keys in the team wiki
- **C.** Disable all CloudWatch alarms to reduce noise
- **D.** Set a billing alarm and destroy resources the same session

??? success "Reveal answer"
    **Correct answer: D**

    NAT, ALB, RDS, and forgotten EC2 instances are common surprise charges.

    **Related concepts**

    - Free Tier
    - Cost hygiene

### Question 5

Security groups are associated with which resource?

**Difficulty:** Beginner

**Options:**

- **A.** Elastic network interfaces (e.g. on EC2)
- **B.** Route tables only
- **C.** S3 buckets directly
- **D.** IAM users

??? success "Reveal answer"
    **Correct answer: A**

    SGs are stateful firewalls at the ENI level.

    **Related concepts**

    - Security groups
    - Stateful filtering

### Question 6

Network ACLs differ from security groups because NACLs are?

**Difficulty:** Intermediate

**Options:**

- **A.** Stateful and attached to instances
- **B.** Applied only to RDS
- **C.** Stateless and applied at subnet boundary
- **D.** Optional only in us-east-1

??? success "Reveal answer"
    **Correct answer: C**

    NACLs evaluate inbound and outbound rules separately (stateless).

    **Related concepts**

    - NACL vs SG
    - Subnet boundaries

### Question 7

Amazon S3 Block Public Access at account level primarily prevents?

**Difficulty:** Intermediate

**Options:**

- **A.** All encryption requirements
- **B.** Accidental public bucket/object exposure via ACLs and policies
- **C.** Cross-region replication
- **D.** VPC endpoint usage

??? success "Reveal answer"
    **Correct answer: B**

    BPA is a guardrail; you still define intentional access in policies.

    **Related concepts**

    - Block Public Access
    - S3 security

### Question 8

CloudTrail's primary purpose is?

**Difficulty:** Beginner

**Options:**

- **A.** Application APM tracing
- **B.** EC2 CPU autoscaling
- **C.** DNS health checks
- **D.** API audit log of AWS account activity

??? success "Reveal answer"
    **Correct answer: D**

    CloudTrail records management events (and optionally data events) for audit and forensics.

    **Related concepts**

    - CloudTrail
    - AccessDenied investigation

## Section 2 — Practical

### Question 9

Which CLI command lists ingress rules for a security group?

**Difficulty:** Beginner

**Options:**

- **A.** `aws iam list-users`
- **B.** `aws s3 ls`
- **C.** `aws route53 list-hosted-zones`
- **D.** `aws ec2 describe-security-groups`

??? success "Reveal answer"
    **Correct answer: D**

    Use `--group-ids` for a focused view during reachability triage.

    **Related concepts**

    - EC2 CLI
    - SG triage

### Question 10

To open a shell on EC2 without SSH port 22, you typically use?

**Difficulty:** Intermediate

**Options:**

- **A.** `aws ssm start-session` with SSM agent and IAM permissions
- **B.** `aws s3 cp` to the instance
- **C.** Public RDP on 3389
- **D.** Root user console password reset

??? success "Reveal answer"
    **Correct answer: A**

    Session Manager uses outbound HTTPS from the instance to AWS endpoints.

    **Related concepts**

    - SSM Session Manager
    - No bastion SSH

### Question 11

Which managed policy is commonly attached for basic SSM connectivity on EC2?

**Difficulty:** Intermediate

**Options:**

- **A.** `AmazonS3FullAccess`
- **B.** `AmazonSSMManagedInstanceCore`
- **C.** `IAMFullAccess`
- **D.** `CloudFrontFullAccess`

??? success "Reveal answer"
    **Correct answer: B**

    It allows the instance to register and receive Session Manager commands.

    **Related concepts**

    - Managed policies
    - SSM prerequisites

### Question 12

Upload a local file to S3 with the AWS CLI using?

**Difficulty:** Beginner

**Options:**

- **A.** `aws ec2 run-instances`
- **B.** `aws cloudtrail lookup-events`
- **C.** `aws s3 cp ./file.txt s3://bucket/key`
- **D.** `aws rds create-db-instance`

??? success "Reveal answer"
    **Correct answer: C**

    `cp`, `sync`, and `ls` are the core object commands.

    **Related concepts**

    - S3 CLI
    - Object storage

### Question 13

Which command shows whether a route table has a default internet route?

**Difficulty:** Intermediate

**Options:**

- **A.** `aws iam get-user`
- **B.** `aws s3api get-bucket-location`
- **C.** `aws logs describe-log-groups`
- **D.** `aws ec2 describe-route-tables`

??? success "Reveal answer"
    **Correct answer: D**

    Look for `0.0.0.0/0` → `igw-` or `nat-` in Routes.

    **Related concepts**

    - Routing
    - Public subnet egress

### Question 14

CloudWatch alarms are commonly used to?

**Difficulty:** Beginner

**Options:**

- **A.** Trigger actions when a metric crosses a threshold
- **B.** Replace IAM policies
- **C.** Encrypt EBS volumes at rest automatically
- **D.** Create VPC peering connections

??? success "Reveal answer"
    **Correct answer: A**

    Alarms integrate with SNS, Auto Scaling, and EventBridge.

    **Related concepts**

    - CloudWatch alarms
    - Operational signals

### Question 15

An Application Load Balancer (ALB) operates primarily at which layer?

**Difficulty:** Intermediate

**Options:**

- **A.** Layer 2 Ethernet
- **B.** Layer 7 HTTP/HTTPS
- **C.** Layer 1 physical
- **D.** Layer 3 only with no HTTP awareness

??? success "Reveal answer"
    **Correct answer: B**

    ALB understands paths, host headers, and HTTP health checks.

    **Related concepts**

    - ALB
    - L7 load balancing

### Question 16

A Network Load Balancer (NLB) is typically chosen when you need?

**Difficulty:** Intermediate

**Options:**

- **A.** Path-based routing to microservices
- **B.** S3 static website hosting
- **C.** High-performance Layer 4 TCP/UDP with static IP options
- **D.** IAM policy simulation

??? success "Reveal answer"
    **Correct answer: C**

    NLB preserves source IP and handles millions of connections per second.

    **Related concepts**

    - NLB
    - L4 load balancing

## Section 3 — Scenarios

### Question 17

An operator sees `AccessDenied` on `aws ec2 describe-instances` but `curl` to the app URL returns HTTP 200. Most likely explanation?

**Difficulty:** Intermediate

**Options:**

- **A.** The VPC has no internet gateway
- **B.** The operator's IAM principal lacks EC2 describe permission; the app may be healthy
- **C.** All security groups were deleted
- **D.** Route 53 is down globally

??? success "Reveal answer"
    **Correct answer: B**

    Separate **identity** failures from **network** failures.

    **Related concepts**

    - IAM triage
    - Reachability

### Question 18

You launch EC2 in a public subnet with a public IP but no `0.0.0.0/0` route to an IGW. External `curl` will?

**Difficulty:** Intermediate

**Options:**

- **A.** Always succeed because public IP is assigned
- **B.** Succeed via S3 endpoint automatically
- **C.** Return HTTP 403 from IAM
- **D.** Fail to connect — no path to the internet

??? success "Reveal answer"
    **Correct answer: D**

    Public IP alone does not replace a correct route table.

    **Related concepts**

    - Routing
    - Public subnets

### Question 19

A bucket must never be readable anonymously. Minimum controls include?

**Difficulty:** Intermediate

**Options:**

- **A.** Block Public Access enabled and no public bucket policy
- **B.** Disable versioning
- **C.** Use root credentials for all access
- **D.** Open SG port 443 on 0.0.0.0/0

??? success "Reveal answer"
    **Correct answer: A**

    Combine BPA with least-privilege IAM and bucket policies.

    **Related concepts**

    - S3 exposure
    - Defence in depth

### Question 20

Your team needs HTTP path routing (`/api`, `/static`) on one hostname. Best default choice?

**Difficulty:** Intermediate

**Options:**

- **A.** NLB with TCP pass-through only
- **B.** NAT Gateway
- **C.** ALB with listener rules
- **D.** Internet Gateway

??? success "Reveal answer"
    **Correct answer: C**

    ALB supports path- and host-based routing at L7.

    **Related concepts**

    - ALB routing
    - Edge design

### Question 21

An RDS db.t3.micro lab instance left running for a month after Free Tier expires often causes?

**Difficulty:** Beginner

**Options:**

- **A.** Free automatic Multi-AZ upgrade
- **B.** Unexpected compute and storage charges
- **C.** IAM user lockout
- **D.** S3 Block Public Access disablement

??? success "Reveal answer"
    **Correct answer: B**

    RDS is a top lab cost surprise — snapshot and delete when finished.

    **Related concepts**

    - RDS cost
    - Lab hygiene

### Question 22

Private subnet EC2 needs S3 access without NAT. Cost-effective pattern?

**Difficulty:** Advanced

**Options:**

- **A.** Attach public IP to every instance
- **B.** Open NACL 0.0.0.0/0 on all ports
- **C.** Store access keys in user data
- **D.** S3 gateway VPC endpoint

??? success "Reveal answer"
    **Correct answer: D**

    Gateway endpoints for S3/DynamoDB avoid NAT data processing charges.

    **Related concepts**

    - VPC endpoints
    - Private access

### Question 23

Auto Scaling Group health check grace period helps avoid?

**Difficulty:** Intermediate

**Options:**

- **A.** Terminating instances before the app finishes booting
- **B.** S3 replication lag
- **C.** CloudTrail log loss
- **D.** IAM MFA enforcement

??? success "Reveal answer"
    **Correct answer: A**

    Grace period delays unhealthy marking after launch.

    **Related concepts**

    - ASG
    - Health checks

### Question 24

Route 53 alias record to an ALB differs from a CNAME because?

**Difficulty:** Intermediate

**Options:**

- **A.** Alias cannot target AWS resources
- **B.** CNAME is required at zone apex always
- **C.** Alias can be used at zone apex and targets AWS resources without extra lookup charge pattern of external CNAME chains
- **D.** Alias disables health checks

??? success "Reveal answer"
    **Correct answer: C**

    Alias records are Route 53-native integrations to ELB, CloudFront, etc.

    **Related concepts**

    - Route 53
    - DNS alias

## Section 4 — Troubleshooting

### Question 25

First command when two engineers disagree whether "AWS is broken"?

**Difficulty:** Beginner

**Options:**

- **A.** Delete the VPC
- **B.** Rotate root password
- **C.** `aws sts get-caller-identity`
- **D.** Reboot the laptop

??? success "Reveal answer"
    **Correct answer: C**

    Confirm account, role, and profile before deeper triage.

    **Related concepts**

    - Identity first
    - CLI hygiene

### Question 26

EC2 shows `running`, security group allows tcp/80 from your IP, but `curl` times out. Next check?

**Difficulty:** Intermediate

**Options:**

- **A.** IAM password policy
- **B.** Route table for `0.0.0.0/0` to IGW (public subnet) or correct NAT path (private)
- **C.** S3 lifecycle policy
- **D.** CloudFront cache behaviour

??? success "Reveal answer"
    **Correct answer: B**

    After SG, verify routing and subnet type.

    **Related concepts**

    - Reachability triage
    - Route tables

### Question 27

SSM `PingStatus` stays Offline on a new instance. Common causes include?

**Difficulty:** Intermediate

**Options:**

- **A.** Missing instance profile or no outbound path to SSM endpoints
- **B.** S3 Block Public Access
- **C.** RDS backup window
- **D.** ALB idle timeout

??? success "Reveal answer"
    **Correct answer: A**

    SSM agent needs IAM role and network egress to AWS.

    **Related concepts**

    - SSM registration
    - Instance profile

### Question 28

CloudTrail shows repeated `AccessDenied` for `ec2:AuthorizeSecurityGroupIngress` from a CI role. This indicates?

**Difficulty:** Intermediate

**Options:**

- **A.** IAM policy too restrictive for the automation role
- **B.** NAT Gateway failure
- **C.** S3 versioning disabled
- **D.** NLB unhealthy targets

??? success "Reveal answer"
    **Correct answer: A**

    CloudTrail clarifies **permission** denials vs network faults.

    **Related concepts**

    - CloudTrail
    - CI IAM

### Question 29

HTTP health check passes on instance localhost but ALB marks target unhealthy. Likely cause?

**Difficulty:** Advanced

**Options:**

- **A.** Billing alarm misconfigured
- **B.** IGW detached
- **C.** Health check path/port/security group from ALB to target mismatch
- **D.** CloudWatch log retention

??? success "Reveal answer"
    **Correct answer: C**

    ALB must reach the target on the configured path; SG must allow the ALB security group.

    **Related concepts**

    - ALB health checks
    - SG referencing

### Question 30

`aws s3 cp s3://bucket/obj .` returns `AccessDenied` from EC2 with instance profile. First fix to verify?

**Difficulty:** Intermediate

**Options:**

- **A.** Enable public read ACL
- **B.** Inline role policy includes correct bucket ARN and actions (`s3:GetObject`, etc.)
- **C.** Open SSH port 22
- **D.** Delete CloudTrail

??? success "Reveal answer"
    **Correct answer: B**

    Scope IAM to bucket/prefix; no static keys needed.

    **Related concepts**

    - Instance role S3 access
    - Policy resources

### Question 31

NAT Gateway in a lab VPC left over weekend primarily increases?

**Difficulty:** Beginner

**Options:**

- **A.** IAM user count
- **B.** Route 53 query quota
- **C.** SSM session limit
- **D.** Hourly and data processing charges

??? success "Reveal answer"
    **Correct answer: D**

    NAT is a deliberate cost landmine — delete when lab completes.

    **Related concepts**

    - NAT cost
    - Free Tier hygiene

### Question 32

NACL allows all traffic but SG denies tcp/443 from the client. Connection will?

**Difficulty:** Intermediate

**Options:**

- **A.** Fail at the security group (stateful deny)
- **B.** Succeed because NACL is permissive
- **C.** Bypass both via IMDS
- **D.** Route via RDS proxy

??? success "Reveal answer"
    **Correct answer: A**

    Both NACL and SG must allow traffic; SG is evaluated at ENI.

    **Related concepts**

    - SG vs NACL
    - Evaluation order

## Section 5 — Architecture

### Question 33

Three-tier web app: ALB in public subnets, EC2 in private subnets, RDS in private subnets. Internet users reach?

**Difficulty:** Intermediate

**Options:**

- **A.** ALB only; EC2 and RDS not directly internet-facing
- **B.** RDS public endpoint by default
- **C.** EC2 SSH on 0.0.0.0/0 required
- **D.** S3 bucket as web tier

??? success "Reveal answer"
    **Correct answer: A**

    Classic pattern: edge public, app/data private.

    **Related concepts**

    - Three-tier
    - Segmentation

### Question 34

Choosing Multi-AZ RDS for a production database primarily improves?

**Difficulty:** Intermediate

**Options:**

- **A.** Read scaling for analytics queries only
- **B.** S3 transfer speed
- **C.** IAM SSO latency
- **D.** Availability during primary AZ failure (synchronous standby)

??? success "Reveal answer"
    **Correct answer: D**

    Multi-AZ is for high availability, not read scaling (use read replicas for that).

    **Related concepts**

    - RDS Multi-AZ
    - HA vs read scale

### Question 35

Least-privilege IAM for a CI pipeline that uploads artefacts to one S3 prefix should use?

**Difficulty:** Intermediate

**Options:**

- **A.** `AdministratorAccess`
- **B.** Root access keys in GitHub Secrets
- **C.** Role with `s3:PutObject` scoped to `arn:aws:s3:::bucket/prefix/*`
- **D.** Public write bucket policy

??? success "Reveal answer"
    **Correct answer: C**

    Scope actions and resources; prefer OIDC federation to static keys.

    **Related concepts**

    - Least privilege
    - CI IAM

### Question 36

IMDSv2 requires session-oriented token retrieval primarily to mitigate?

**Difficulty:** Advanced

**Options:**

- **A.** S3 replication lag
- **B.** SSRF/credential theft attacks against open metadata service
- **C.** CloudWatch metric gaps
- **D.** Route 53 TTL issues

??? success "Reveal answer"
    **Correct answer: B**

    IMDSv2 adds a session token step; require it on launch templates.

    **Related concepts**

    - IMDSv2
    - Instance metadata security

### Question 37

Organisation with multiple accounts should centralise CloudTrail logs into?

**Difficulty:** Intermediate

**Options:**

- **A.** A dedicated audit/logging account S3 bucket with MFA delete and restricted policy
- **B.** Public S3 website bucket
- **C.** Each developer laptop
- **D.** EC2 instance store volume

??? success "Reveal answer"
    **Correct answer: A**

    Org trails and log aggregation support forensics and compliance.

    **Related concepts**

    - CloudTrail organisation
    - Log integrity

### Question 38

ALB vs NLB for raw TCP gaming traffic on fixed ports with extreme connection count?

**Difficulty:** Advanced

**Options:**

- **A.** ALB with HTTP listener only
- **B.** S3 Transfer Acceleration
- **C.** CloudFront origin failover only
- **D.** NLB — Layer 4 performance and static IP per AZ options

??? success "Reveal answer"
    **Correct answer: D**

    NLB suits TCP/UDP workloads needing low latency and high connection volume.

    **Related concepts**

    - NLB selection
    - Workload fit

### Question 39

CloudWatch Logs subscription filter can send log events to?

**Difficulty:** Intermediate

**Options:**

- **A.** IAM group membership
- **B.** EC2 instance store only
- **C.** Lambda, Kinesis, or Firehose for processing/streaming
- **D.** Route 53 hosted zone

??? success "Reveal answer"
    **Correct answer: C**

    Subscriptions enable near-real-time log processing pipelines.

    **Related concepts**

    - CloudWatch Logs
    - Observability pipelines

### Question 40

AWS track capstone integrates which concerns holistically?

**Difficulty:** Advanced

**Options:**

- **A.** Only S3 static hosting
- **B.** IAM least privilege, VPC segmentation, managed compute/storage, edge routing, observability, and cost-aware cleanup
- **C.** Git rebase workflows only
- **D.** Container image scanning exclusively

??? success "Reveal answer"
    **Correct answer: B**

    The track builds from account foundations through three-tier patterns with ops guardrails.

    **Related concepts**

    - AWS capstone
    - DevOps breadth

## Score Summary

| Score | Band | Meaning |
|------:|------|---------|
| 36–40 | Excellent | Ready for advanced labs and AWS interviews |
| 28–35 | Good | Pass — revise weak modules |
| 20–27 | Needs improvement | Revisit tutorials and labs before interviews |
| ≤19 | Restart track | Work Modules 1–3 in order |

**Total questions:** 40 · **Passing score:** 28 (70%)

## Recommended Study Areas

- [AWS track](../aws/index.md)
- Lab: [IAM and VPC Triage](../labs/aws-iam-vpc-triage.md)
- Lab: [SSM and S3](../labs/aws-ssm-s3.md)
- Cheat sheet: [AWS](../cheatsheets/aws.md)
- Interview: [AWS](../interview/aws.md)

## Interview Connection

Expect IAM vs network triage stories, SSM-over-SSH rationale, S3 exposure controls, ALB vs NLB trade-offs, RDS cost awareness, and CloudTrail `AccessDenied` narratives. Use your lab evidence commands (`sts`, `describe-security-groups`, `describe-route-tables`).

## References

1. [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/)
2. [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
3. [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/)
