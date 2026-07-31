---
title: "Databases on AWS"
description: "Choose AWS databases with confidence: Amazon RDS, Aurora, DynamoDB, ElastiCache, and DocumentDB — when to use each in Cloud and DevOps architectures."
difficulty: intermediate
estimated_time: "55–70 min"
technology: aws
category: aws
module: "Module 6 · Databases"
career_paths:
  - cloud-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - rds
  - aurora
  - dynamodb
  - elasticache
  - documentdb
prerequisites:
  - aws/storage-s3-ebs-efs
  - aws/vpc-networking-on-aws
next:
  - aws/containers-ecs-eks-ecr
related:
  - aws/storage-s3-ebs-efs
  - aws/compute-ec2-asg-and-load-balancing
labs: []
projects: []
interview: interview/aws
certifications:
  - AWS Certified Solutions Architect – Associate
  - AWS Certified Database – Specialty
tags:
  - aws
  - rds
  - aurora
  - dynamodb
  - elasticache
  - databases
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Databases on AWS

## Overview




Choose and operate the right managed database on AWS: Relational Database Service (RDS), Amazon Aurora, DynamoDB, ElastiCache, and DocumentDB — with clear decision criteria for Cloud, DevOps, and platform work.

Self-managing databases on Amazon Elastic Compute Cloud (EC2) is rarely the first choice: patching, failover, and backups dominate toil. AWS managed services trade some control for Multi-AZ resilience and automation. Picking the wrong engine (or leaving a large RDS instance running) is expensive; this module focuses on **fit** and **safe labs**.

!!! warning "Cost"
    RDS, Aurora, ElastiCache, and DocumentDB bill for instances continuously. Prefer **`db.t3.micro` / Free Tier**, single-AZ for labs, short retention, and **delete with final snapshot skipped** when learning. DynamoDB on-demand is often cheaper for labs than provisioned. Destroy clusters before you finish.

This is a core tutorial in **Module 6 · Databases** of the REBASH Academy **AWS for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites




- [Storage: S3, EBS, and EFS](storage-s3-ebs-efs.md)
- [VPC Networking on AWS](vpc-networking-on-aws.md) — private subnets and security groups
- Basic Structured Query Language (SQL) or NoSQL awareness



## Learning Objectives




By the end of this tutorial, you will be able to:

- [ ] Choose among RDS, Aurora, DynamoDB, ElastiCache, and DocumentDB with clear criteria  
- [ ] Contrast Multi-AZ failover with read replicas  
- [ ] Design DynamoDB partition (and sort) keys around access patterns  
- [ ] Place databases in private subnets with least-privilege security groups  
- [ ] Avoid common cost and connectivity pitfalls



## Architecture




This topic’s control points and relationships are shown below.

![AWS databases](../assets/excalidraw/aws-databases.svg)



## Theory




### What it is

AWS offers managed databases so you spend less time patching engines and orchestrating failover on Amazon Elastic Compute Cloud (EC2). **Amazon Relational Database Service (RDS)** runs familiar relational engines. **Amazon Aurora** is a cloud-native relational engine compatible with MySQL and PostgreSQL. **Amazon DynamoDB** is a managed NoSQL key-value and document store. **Amazon ElastiCache** provides in-memory Redis or Memcached. **Amazon DocumentDB** offers a MongoDB-compatible API with AWS operations. Self-managing databases on EC2 is rarely the first choice for new Cloud and DevOps designs.

### Why it matters

Pipelines need test databases; production needs encryption, parameter groups, and credentials in Secrets Manager or IAM. Platform teams standardise private subnet groups, `PubliclyAccessible=false`, and security groups from the app tier only. SRE tracks Multi-AZ failover, replica lag, storage autoscaling, and restore drills. DevSecOps insists on KMS encryption, TLS, and no passwords in user data. Wrong engine choice — or a leftover large RDS instance — is expensive.

### How it works

**Relational (RDS/Aurora):** DB subnet group across ≥2 AZs → SG allows 5432/3306 from the app SG only → encryption on → app reads secrets inside the VPC. Multi-AZ failovers update DNS to a standby; read replicas scale reads asynchronously and are not the same as Multi-AZ.

**DynamoDB:** Design access patterns first → table with partition (and optional sort) keys → SDK + IAM roles → optional Streams, TTL, or Global Tables. Use a gateway VPC endpoint for private access.

**Cache:** ElastiCache in private subnets → cache-then-DB with careful TTLs to avoid stampedes.

### Concept deep dive

- **RDS** — Managed PostgreSQL, MySQL, MariaDB, SQL Server, Oracle, or Db2. AWS handles provisioning, patching, automated backups, and optional Multi-AZ standby. Choose RDS for standard SQL with straightforward ops and modest scale.
- **Aurora** — MySQL-/PostgreSQL-compatible with distributed shared storage. Faster typical failover, shared-storage replicas, Serverless v2, and Global Database. Choose Aurora for cloud-native scale beyond classic RDS on the same SQL dialect.
- **DynamoDB** — Serverless tables (on-demand or provisioned). Design around **partition keys** (and optional sort keys): every efficient query states the key. Hot partitions throttle throughput. Prefer GetItem/Query over scans. Streams enable event-driven follow-on work.
- **ElastiCache** — Managed Redis (rich structures, replication) or Memcached (simple cache). Use for sessions, rate limits, and hot keys in front of RDS/DynamoDB — not as system of record unless you accept cache semantics.
- **DocumentDB** — MongoDB-compatible API for migrations that want managed ops on AWS. For greenfield work that does not need MongoDB drivers/features, DynamoDB often fits better.
- **When to choose each** — SQL + familiar engines → **RDS**. SQL + higher failover/scale → **Aurora**. Key-value / serverless → **DynamoDB**. Sub-ms hot data → **ElastiCache**. MongoDB-compatible API → **DocumentDB**.
- **Multi-AZ vs read replicas** — **Multi-AZ**: synchronous standby in another AZ for write HA; automatic failover; standby is not for reads. **Read replicas**: asynchronous copies for read scaling (or DR promotion); can lag; do not replace Multi-AZ. Production often uses Multi-AZ **and** optional replicas.
- **Partition keys for DynamoDB** — Partition key drives distribution. High-cardinality keys matching query patterns spread load. Composite keys (partition + sort) enable ranges within a partition. Avoid designs where one key absorbs all traffic without sharding.

### Key concepts and comparisons

| Need | Prefer |
|------|--------|
| SQL + operational simplicity | RDS PostgreSQL/MySQL |
| SQL + cloud-native failover/scale | Aurora |
| Key-value / event scale / serverless | DynamoDB |
| Sub-ms sessions / hot keys | ElastiCache Redis |
| MongoDB-compatible managed API | DocumentDB |
| Write HA in one Region | Multi-AZ (not “replica alone”) |
| Read scaling | Read replicas (watch lag) |
| PubliclyAccessible | `false` for production |
| Hot partition | Anti-pattern — rework key design |

### Common pitfalls

- Leaving `PubliclyAccessible=true` on RDS  
- Single-AZ production database  
- Treating read replicas as synchronous Multi-AZ failover  
- Undersized `max_connections` behind large Auto Scaling groups  
- DynamoDB scan-heavy designs instead of keyed queries  
- Cache without TTL or stampede protection  
- Forgetting to delete lab instances (24×7 billing)  
- Choosing DocumentDB “because Mongo” when DynamoDB fits greenfield



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-aws/module-06 && cd ~/rebash-aws/module-06
```

**Focus:** describe RDS/DynamoDB without creating paid databases

### Step 1 – Read-only database inventory

```bash
aws sts get-caller-identity
aws rds describe-db-instances --query 'DBInstances[].{Id:DBInstanceIdentifier,Engine:Engine,MultiAZ:MultiAZ}' --output table
aws dynamodb list-tables --output table
```

### Step 2 – Design notes instead of creating RDS

```bash
cat > db-notes.md << 'EOF'
- Prefer Multi-AZ for HA; know backup windows
- Do not create RDS in labs without tagging + destroy alarm
- Secrets Manager / IAM auth over passwords in apps
EOF
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```



## Validation




- [ ] Lab commands run under `~/rebash-aws/module-06/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough




Production practice for **Databases on AWS** always combines:

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




!!! warning "Leaving `PubliclyAccessible=true` on RDS  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Single-AZ production database  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices




- Encode Databases on AWS changes as code and review them in pull requests
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




**Databases on AWS** is essential for Cloud and DevOps engineers working with aws. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. Multi-AZ RDS versus read replicas?
2. When is DynamoDB a better fit than RDS?
3. What does PITR give you?
4. How do you rotate database secrets?
5. Why is creating RDS in labs risky for cost?

!!! tip "Sample answer — question 2"
    Check instance/cluster status, subnet groups, and security group rules to the DB port.

!!! tip "Sample answer — question 4"
    Encrypt storage, restrict security groups, and delete lab databases the same day.



## Related Tutorials




- [Course overview](index.md)
- [Containers: ECS, EKS, and ECR](containers-ecs-eks-ecr.md)



## References




- [Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)  
- [Amazon Aurora](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html)  
- [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)  
- [Amazon ElastiCache](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html)  
- [Amazon DocumentDB](https://docs.aws.amazon.com/documentdb/latest/developerguide/what-is.html)
