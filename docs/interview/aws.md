---
title: "AWS Interview Preparation"
description: "50 curated AWS interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: aws
tags:
  - interview
  - aws
comments: false
---

{% raw %}
# AWS Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

<div class="ra-interview-qa" markdown="1">

## Core concepts

**1. What is the difference between alb and nlb, in which scenario you use alb and nlb?**

??? success "Reveal answer"
    **In short:** ALB is Layer 7 HTTP routing; NLB is Layer 4 ultra-fast TCP/UDP — pick by protocol and features, not habit.
    
    **Key points**
    
    - **ALB** — host/path/header routing, TLS terminate, WebSocket/gRPC, auth integrations
    - **NLB** — static IPs/Elastic IPs, extreme performance, TCP/UDP/TLS pass-through
    - **Use ALB** — typical web/API microservices
    - **Use NLB** — game servers, IoT, PrivateLink front-ends, preserving client IP patterns
    
    **Try this**
    
    - `aws elbv2 describe-load-balancers --query 'LoadBalancers[].{N:LoadBalancerName,T:Type}'`
    
    **Trap**
    
    - Putting TLS-heavy HTTP APIs on NLB and reinventing routing in the app

**2. What is AWS Lambda and how do you design a serverless application?**

??? success "Reveal answer"
    **In short:** Lambda runs event-driven code without servers — design around triggers, idempotency, and cold-start budgets.
    
    **Key points**
    
    - **Package** — function + deps; set memory/timeout; least-privilege role
    - **Triggers** — API Gateway, SQS, SNS, EventBridge, S3
    - **Downstream** — prefer async queues over chatty sync chains
    - **Observe** — structured logs, metrics, alarms, X-Ray traces
    
    **Try this**
    
    - `aws lambda invoke --function-name demo --payload '{}' out.json`
    
    **Trap**
    
    - 15-minute timeouts used as a batch scheduler — use Step Functions/ECS instead

**3. What are the best practices for securing cloud infrastructure?**

??? success "Reveal answer"
    **In short:** Identity first: MFA, short-lived roles, Organisations SCPs, then network and data encryption.
    
    **Key points**
    
    - **IAM** — Identity Center, least privilege, permission boundaries
    - **Network** — private subnets, SG default deny, no open `0.0.0.0/0` admin ports
    - **Data** — KMS encryption, Secrets Manager, Block Public Access
    - **Detect** — CloudTrail org trail, GuardDuty, Security Hub, Config
    
    **Trap**
    
    - Long-lived root or admin access keys on laptops

**4. Explain the AWS architecture shown in the diagram (CodePipeline, CodeBuild, CodeDeploy, CloudFormation, CloudWatch)?**

??? success "Reveal answer"
    **In short:** Native CI/CD: source triggers CodePipeline → CodeBuild tests/artefacts → CloudFormation/CodeDeploy → CloudWatch watches it.
    
    **Key points**
    
    - **Source** — CodeCommit/GitHub/S3
    - **Build** — unit tests, image/zip, cfn-lint/security scans
    - **Deploy** — CloudFormation/CDK for infra; CodeDeploy for apps
    - **Observe** — stage failures and post-deploy alarms in CloudWatch
    
    **Trap**
    
    - No approval gate between staging and production

**5. How do you scale EKS? What are the metrics considered and where do you add your inputs and How? Explain how you have done auto-scaling in your project?**

??? success "Reveal answer"
    **In short:** EKS scales in three layers: Pods (HPA), nodes (Cluster Autoscaler/Karpenter), and sometimes vertical sizing.
    
    **Key points**
    
    - **HPA** — CPU/memory/custom metrics via Metrics Server or Prometheus adapter
    - **Nodes** — Cluster Autoscaler or Karpenter on Pending pods / utilisation
    - **Inputs** — requests/limits, PDBs, ASG/Karpenter provisioner constraints
    - **Prove** — load test; watch `kubectl get hpa` and node count
    
    **Try this**
    
    - `kubectl get hpa,nodes`
    - `kubectl describe pod -l app=api | rg -i 'Insufficient|Triggered'`
    
    **Trap**
    
    - Autoscaling on unset resource requests — HPA and scheduler guess wrong

## Scenarios and troubleshooting

**6. What if production rds is growing 95% how do you debug and how do you prevent this in future?**

??? success "Reveal answer"
    **In short:** Treat ~5% free storage as an incident: grow storage now, then find the growth driver and prevent it.
    
    **Key points**
    
    - **Now** — increase allocated storage / confirm autoscaling; Aurora scales storage for you
    - **Find cause** — runaway tables, temp files, binary/WAL growth, bad retention
    - **Prevent** — alarms on FreeStorageSpace, lifecycle/archival, query hygiene
    - **Verify** — free space recovers; apps reconnect cleanly
    
    **Try this**
    
    - `aws cloudwatch get-metric-statistics --namespace AWS/RDS --metric-name FreeStorageSpace`
    
    **Trap**
    
    - Waiting for storage-full before resizing — outage with blocked writes

**7. In lambda function, how would you handle failures and how would you set up retries?**

??? success "Reveal answer"
    **In short:** Retries depend on invoke type: sync clients back off; async/stream sources need DLQs and idempotency.
    
    **Key points**
    
    - **Sync** — clear errors; client retries; idempotency keys for POSTs
    - **Async** — built-in retries; On-Failure destination or DLQ
    - **SQS/Streams** — `maxReceiveCount` then DLQ; bisect poison messages
    - **Code** — make handlers safe to run twice
    
    **Try this**
    
    - Inject a failing event and confirm the DLQ payload lands
    
    **Trap**
    
    - Retrying non-idempotent payments without a dedupe key

**8. How do you identify the root cause of a production outage?**

??? success "Reveal answer"
    **In short:** Start from customer impact and golden signals, then correlate the last change — not random restarts.
    
    **Key points**
    
    - **Impact** — which endpoints, regions, error rates?
    - **Signals** — latency, traffic, errors, saturation (CloudWatch/X-Ray/RUM)
    - **Changes** — deploys, IaC applies, certs, DNS, feature flags
    - **Communicate** — incident commander and status updates early
    
    **Trap**
    
    - Rebooting everything before capturing timelines and logs

**9. You want to create an EC2, and while creating the instance, you are getting an error like IP address exceeded. How will you troubleshoot and fix it?**

??? success "Reveal answer"
    **In short:** Usually the subnet IPv4 pool is exhausted (or you hit ENI/EIP limits) — free ENIs or launch elsewhere.
    
    **Key points**
    
    - **Check** — `AvailableIpAddressCount` on the subnet
    - **ENI leaks** — Lambda-in-VPC, failed ECS/EKS attachments
    - **Fix** — sibling subnet, new larger subnet (cannot resize CIDR in place)
    - **Limits** — Elastic IP / ENI service quotas
    
    **Try this**
    
    - `aws ec2 describe-subnets --query 'Subnets[].{Id:SubnetId,Free:AvailableIpAddressCount,Cidr:CidrBlock}'`
    
    **Trap**
    
    - Picking a /28 'for security' then wondering why ASG cannot scale

**10. Say you need to configure EC2 instances automatically or replace themselves automatically when they fail. How do you implement this?**

??? success "Reveal answer"
    **In short:** Auto Scaling group + launch template + ELB health checks — unhealthy instances get replaced automatically.
    
    **Key points**
    
    - **Launch template** — AMI, user data, IAM instance profile
    - **ASG** — min/desired/max across AZs
    - **Health** — ELB/ALB checks, not only EC2 status
    - **Config** — prefer immutable replace over SSH snowflakes
    
    **Try this**
    
    - Terminate an instance and watch a replacement go `InService`
    
    **Trap**
    
    - ASG using only EC2 status while the app is dead on port 8080

**11. How to spead up s3 upload with files in large size, and client uploaded 10 Gb file but failed after uploading 5 gb how you confirm that 5 gb is uploaded to s3?**

??? success "Reveal answer"
    **In short:** Large uploads use multipart; a failed 10 GB transfer leaves incomplete parts — list them, they are not a finished object.
    
    **Key points**
    
    - **Speed** — multipart parallel parts; tune CLI concurrency/chunk size
    - **Distance** — Transfer Acceleration or upload from same-region compute
    - **Confirm partial** — `list-multipart-uploads` / `list-parts` on the upload ID
    - **Hygiene** — lifecycle abort incomplete uploads; checksums on complete
    
    **Try this**
    
    - `aws s3api list-multipart-uploads --bucket BUCKET`
    - `aws s3 cp big.bin s3://BUCKET/ --expected-size`
    
    **Trap**
    
    - Assuming the 5 GB 'is in S3' because the client progress bar said so

**12. You are having lambda function and role everything setup perfectly but logs are not coming up in the cw group how to troubleshoot?**

??? success "Reveal answer"
    **In short:** No CloudWatch logs usually means missing `logs:*` on the role, wrong log group, or the function never invoked.
    
    **Key points**
    
    - **Permissions** — `CreateLogGroup/Stream` + `PutLogEvents` (basic execution role)
    - **Invoke proof** — Metrics Invocations/Errors first
    - **Name** — group `/aws/lambda/<function-name>` unless custom LoggingConfig
    - **Guardrails** — SCPs/boundaries denying logs
    
    **Try this**
    
    - `aws lambda invoke` then refresh the `/aws/lambda/FUNCTION` log group within a minute
    
    **Trap**
    
    - Blaming VPC routing first — Logs needs IAM more often than routes

**13. RDS migration with minimal downtime – how would you approach it?**

??? success "Reveal answer"
    **In short:** Minimal-downtime RDS moves use replicas or DMS CDC — cut over only when lag is near zero.
    
    **Key points**
    
    - **Homogeneous** — DMS ongoing replication or native replicas
    - **Heterogeneous** — DMS + Schema Conversion Tool
    - **Cutover** — brief freeze/write block; flip endpoints/DNS
    - **Verify** — CDC lag, row counts, app smoke tests
    
    **Trap**
    
    - One-shot dump/restore on a busy primary and hoping for a short outage

**14. If there is a vendor who provides VPN services for company A, his manager wants to view some dashboard but do not have AWS account. How would you help him?**

??? success "Reveal answer"
    **In short:** Do not share IAM users — embed/share a dashboard (QuickSight) or federate read-only via Identity Center.
    
    **Key points**
    
    - **Prefer** — QuickSight embedding or a thin app with corporate SSO
    - **If console needed** — Identity Center permission set, least privilege
    - **Time-box** — access reviews and expiry
    - **Audit** — CloudTrail on what they viewed
    
    **Trap**
    
    - Long-lived access keys emailed to the vendor manager

**15. How would you set up networking in vpc?**

??? success "Reveal answer"
    **In short:** Design VPC from traffic flows: multi-AZ public/private subnets, IGW/NAT, SG-first controls.
    
    **Key points**
    
    - **CIDR plan** — room for growth, peering, and Pod ranges
    - **Tiers** — public LB/ingress; private app; private data
    - **Egress** — NAT per AZ for HA; endpoints for AWS APIs
    - **Prove** — Reachability Analyzer; no public IPs on data tiers
    
    **Try this**
    
    - `aws ec2 describe-route-tables`
    
    **Trap**
    
    - Single-AZ NAT to save money — then that AZ outage kills all egress

**16. How would you store secure info inside s3?**

??? success "Reveal answer"
    **In short:** Encrypt S3 with SSE-KMS, block public access, and tight bucket policies — use Secrets Manager for hot credentials.
    
    **Key points**
    
    - **Block Public Access** — account and bucket
    - **SSE-KMS CMK** — key policies limit decryptors
    - **Access** — IAM roles only; optional Object Lock for WORM
    - **Logging** — access logs / CloudTrail data events for sensitive buckets
    
    **Trap**
    
    - Putting database passwords in a 'private' S3 object as the secret store

**17. How would you maintain high availability in ecs + fargate or eks?**

??? success "Reveal answer"
    **In short:** HA means multi-AZ capacity, health-checked load balancing, and Pod/task disruption budgets.
    
    **Key points**
    
    - **Spread** — tasks/Pods across AZs; multi-AZ ALB/NLB
    - **ECS/Fargate** — desired count >1; circuit breakers / deployments
    - **EKS** — replicas, PDBs, topology spread, multi-AZ nodes
    - **Data** — managed multi-AZ DB; not local disk as truth
    
    **Trap**
    
    - One replica 'to save cost' on a stateful API

**18. What are the security parameters we must consider while we are creating an EC2 instance for production?**

??? success "Reveal answer"
    **In short:** Production EC2: hardened AMI, IMDSv2, least-privilege profile, no SSH from the world, encrypted disks.
    
    **Key points**
    
    - **Identity** — instance profile; prefer SSM Session Manager over open SSH
    - **IMDSv2** — required hop limit
    - **Network** — SG least ports; private subnet when possible
    - **Disk** — EBS encryption; patch via Image Builder/SSM
    
    **Trap**
    
    - SSH `0.0.0.0/0` and long-lived PEM keys shared in chat

## Practice questions

**19. How do you design a multi-region active-active deployment on AWS?**

??? success "Reveal answer"
    **In short:** Active-active needs global traffic steering plus data strategies that tolerate multi-writer or careful partitioning.
    
    **Key points**
    
    - **Edge** — Route 53 latency/geolocation + health checks; Global Accelerator optional
    - **Compute** — identical stacks per region via IaC
    - **Data** — Aurora Global, DynamoDB Global Tables, or partitioned ownership
    - **Fail** — automated health-based steering; practised failover
    
    **Trap**
    
    - Two regions writing the same relational primary without a conflict story

**20. How do you implement infrastructure as code on AWS using CloudFormation vs CDK?**

??? success "Reveal answer"
    **In short:** CloudFormation is declarative templates; CDK is imperative code that synthesises CloudFormation.
    
    **Key points**
    
    - **CFN** — YAML/JSON; change sets; stack policies
    - **CDK** — TypeScript/Python etc.; constructs; still CFN under the hood
    - **Choose CDK** — abstractions and reusable constructs
    - **Choose CFN/SAM** — simple stacks or org standards that mandate templates
    
    **Trap**
    
    - Editing synthesised template by hand while still using CDK

**21. Design a highly available backend on AWS – what services and architecture would you use?**

??? success "Reveal answer"
    **In short:** HA backend: multi-AZ VPC, ALB, autoscaled compute (ECS/EKS/ASG), multi-AZ data, queues for decoupling.
    
    **Key points**
    
    - **Edge** — ALB/API Gateway + WAF
    - **App** — multi-AZ tasks/Pods with health checks
    - **Data** — RDS/Aurora Multi-AZ; ElastiCache; S3
    - **Async** — SQS/SNS/EventBridge to absorb spikes
    
    **Trap**
    
    - Stateful sessions pinned to one instance with no stickiness plan

**22. How to design an event-driven architecture using S3, Lambda, and SNS for data ingestion?**

??? success "Reveal answer"
    **In short:** S3 event → Lambda process → SNS fan-out — keep processing idempotent and failure-visible.
    
    **Key points**
    
    - **Ingest** — S3 Put notifications or EventBridge
    - **Process** — Lambda (or Step Functions for multi-step)
    - **Notify** — SNS to downstream subscribers/SQS
    - **Safety** — DLQ, partial-batch failure, PII handling
    
    **Trap**
    
    - Synchronous Lambda chains that time out on large objects

**23. Design an high availability, fault tolerance system in aws?**

??? success "Reveal answer"
    **In short:** Fault tolerance is redundancy + isolation + graceful degradation — multi-AZ by default, multi-region when RTO demands.
    
    **Key points**
    
    - **Compute/LB** — healthy replacements via ASG/ECS/EKS
    - **Data** — Multi-AZ; backups/PITR tested
    - **Decouple** — queues/buffers between tiers
    - **Chaos** — game days; dependency timeouts and bulkheads
    
    **Trap**
    
    - Calling a single-AZ dependency on the critical path with no fallback

**24. What cloud platforms and AWS services have you worked with?**

??? success "Reveal answer"
    **In short:** Say what you ran in production — VPC, IAM, EC2/ECS/EKS, RDS, S3, Lambda — and one concrete design trade-off.
    
    **Key points**
    
    - **Breadth** — compute, data, networking, security, observability
    - **Depth** — one story: outage, scale event, or cost win
    - **IaC** — Terraform/CDK/CloudFormation experience
    - **Honesty** — name services you have not used yet
    
    **Trap**
    
    - Listing every AWS service logo without a story

**25. You found memory pressure on RDS. You cannot resize. What immediate action can you take without downtime?**

??? success "Reveal answer"
    **In short:** Without a resize: kill heavy sessions/queries, add read offload, raise memory parameters carefully, cache hotter paths.
    
    **Key points**
    
    - **Now** — Performance Insights; terminate runaway queries
    - **Offload** — read replicas for read traffic; cache (ElastiCache)
    - **Tune** — connection pooling; avoid connection storms
    - **Later** — plan a blue/green or maintenance resize window
    
    **Try this**
    
    - `aws rds describe-db-instances --query 'DBInstances[].{Id:DBInstanceIdentifier,Class:DBInstanceClass}'`
    
    **Trap**
    
    - Restarting RDS as the first step and dropping all connections blindly

**26. If any service is down for more than 2 weeks and customer is asking for update, what will you tell to customer?**

??? success "Reveal answer"
    **In short:** Be honest: impact, knowns/unknowns, mitigation, ETA for next update — never invent a fake fix time.
    
    **Key points**
    
    - **Status** — what works vs broken
    - **Actions** — workaround if any; escalation path
    - **Cadence** — commit to the next update time and keep it
    - **Comms** — single spokesperson; no conflicting stories
    
    **Trap**
    
    - Promising 'tomorrow for sure' with no engineering basis

**27. EC2 instance is unreachable, and it’s not a security group issue. What’s your next step?**

??? success "Reveal answer"
    **In short:** If SG is fine: check OS/network path — status checks, routes, NACLs, SSM, console screenshot, volume issues.
    
    **Key points**
    
    - **Status checks** — system vs instance; hypervisor vs OS
    - **Reachability** — NACL, route tables, source/dest check
    - **Access** — SSM Session Manager; serial console
    - **Disk** — full root volume causing hangs
    
    **Try this**
    
    - `aws ec2 describe-instance-status --instance-ids i-0123456789abcdef0`
    - `aws ssm start-session --target i-0123456789abcdef0`
    
    **Trap**
    
    - Replacing the instance before capturing console logs

**28. What will you do for zero-downtime when eks cluster upgrade?**

??? success "Reveal answer"
    **In short:** Zero-downtime EKS upgrades: control plane first (managed), then node pools drained in waves behind PDBs.
    
    **Key points**
    
    - **Control plane** — managed upgrade; watch add-on compatibility
    - **Nodes** — new group or surge upgrade; cordon/drain
    - **Workloads** — PDBs, multiple replicas, topology spread
    - **Validate** — conformance smoke tests after each wave
    
    **Trap**
    
    - Upgrading nodes before APIs/add-ons support that version

**29. How do you monitor network traffic in AWS?**

??? success "Reveal answer"
    **In short:** Use VPC Flow Logs, Traffic Mirroring, CloudWatch metrics on LB/NAT, and Reachability Analyzer for paths.
    
    **Key points**
    
    - **Flow Logs** — accept/reject metadata to S3/CloudWatch
    - **LB metrics** — `ActiveConnectionCount`, `TargetResponseTime`, 5XXs
    - **NAT** — bytes and port allocation errors
    - **Deep dive** — Traffic Mirroring to IDS/tools when needed
    
    **Trap**
    
    - Only watching CPU while NAT is silently dropping ephemeral ports

**30. You have RDS and tomorrow, I being your client, will tell you that you need to make the configuration in such a way so that only one user can access the RDS at a time. How will you configure that?**

??? success "Reveal answer"
    **In short:** Enforce single-session access with IAM auth or DB users plus connection limits — not a shared superuser password.
    
    **Key points**
    
    - **IAM DB auth** — short-lived tokens per person
    - **DB params** — `max_user_connections` / role limits
    - **Proxy** — RDS Proxy with controlled pooling if apps need many conns
    - **Audit** — who connected when
    
    **Trap**
    
    - One shared `admin` password and asking people to 'take turns'

**31. You have an EC2 instance and you would like to migrate it from one region to another. How will you do it?**

??? success "Reveal answer"
    **In short:** Copy the AMI (and encrypted snapshots with KMS grants) to the target region, then launch from a launch template there.
    
    **Key points**
    
    - **AMI copy** — include encrypted snapshots; share KMS keys
    - **Network** — recreate SG/subnets via IaC in the new region
    - **Data** — separate DB/file migration plan
    - **Cutover** — DNS/app config to new region
    
    **Try this**
    
    - `aws ec2 copy-image --source-region eu-west-1 --source-image-id ami-0123456789abcdef0 --name copied`
    
    **Trap**
    
    - Thinking an EC2 instance can be 'moved' like a file between regions

**32. How do you secure your environments in aws?**

??? success "Reveal answer"
    **In short:** Secure environments with account isolation, SCPs, private networking, encryption, and continuous detection.
    
    **Key points**
    
    - **Accounts** — prod/non-prod/security tooling separation
    - **Identity** — SSO roles; no standing admin
    - **Network/data** — private tiers; KMS; secrets manager
    - **Detect/respond** — GuardDuty, Security Hub, automated remediation where safe
    
    **Trap**
    
    - Identical IAM admin in every account 'for speed'

**33. How do you restrict access to AWS resources for a specific user?**

??? success "Reveal answer"
    **In short:** Restrict a user with IAM identity policies (and optional SCPs/permission boundaries) on allowed actions and resources.
    
    **Key points**
    
    - **Identity policy** — Allow only needed actions/ARNs
    - **Deny statements** — explicit denials for dangerous APIs
    - **Boundary/SCP** — ceiling the maximum permissions
    - **Verify** — Access Analyzer and `simulate-principal-policy`
    
    **Try this**
    
    - `aws iam simulate-principal-policy --policy-source-arn USER_ARN --action-names ec2:StopInstances`
    
    **Trap**
    
    - Attach `AdministratorAccess` then try to constrain with tags alone

**34. How do you restrict a user to only EC2 and RDS access?**

??? success "Reveal answer"
    **In short:** Grant only `ec2:*` and `rds:*` (narrower still) on specific resources — prefer group/role over inline user sprawl.
    
    **Key points**
    
    - **Group/role** — attach managed or custom policy
    - **Resource ARNs** — limit to accounts/regions/tags
    - **Avoid wildcards** — especially `*` on sensitive APIs
    - **PassRole** — restrict which roles they can hand to services
    
    **Trap**
    
    - `ec2:*` on `*` including CreateVpc and security-group open-to-world

**35. How do you ensure the least privilege access to the IAM users?**

??? success "Reveal answer"
    **In short:** Least privilege = start from job function policies, use Access Analyzer unused-access findings, and time-bound elevation.
    
    **Key points**
    
    - **Role per task** — CI role ≠ human role ≠ app role
    - **Analyze** — unused permissions; trim quarterly
    - **Elevate** — IAM Identity Center permission sets / PIM-like process
    - **Boundaries** — stop privilege escalation via PassRole
    
    **Trap**
    
    - Copying yesterday's admin policy into a new service role

**36. How do you login to the ec2 instance if you've lost the .pem key?**

??? success "Reveal answer"
    **In short:** Prefer SSM Session Manager; if you must use SSH, use EC2 Instance Connect or replace the key via user data on a recovered volume — not email PEMs.
    
    **Key points**
    
    - **SSM** — no inbound SSH needed if agent + IAM allow
    - **Instance Connect** — push ephemeral SSH key
    - **Recovery** — stop instance, mount root volume elsewhere, fix `authorized_keys`
    - **Prevent** — disable password auth; use fleet-managed access
    
    **Try this**
    
    - `aws ssm start-session --target i-0123456789abcdef0`
    
    **Trap**
    
    - Baking a shared PEM into the AMI

**37. You have created an IAM user in AWS and configured role-based access in EKS. How do you bind the IAM user to the EKS role?**

??? success "Reveal answer"
    **In short:** Map IAM principal to Kubernetes RBAC via EKS access entries (or aws-auth ConfigMap on older clusters).
    
    **Key points**
    
    - **Modern** — EKS access entries + access policies
    - **Legacy** — `aws-auth` ConfigMap `mapUsers` / `mapRoles`
    - **K8s side** — Role/ClusterRoleBinding for the username/group
    - **Verify** — `kubectl auth can-i` as that user
    
    **Try this**
    
    - `aws eks list-access-entries --cluster-name CLUSTER`
    
    **Trap**
    
    - Editing aws-auth by hand and locking yourself out of the cluster

**38. Assume you have 10 AWS accounts. How will you securely log in to them, considering access keys are not used for security reasons?**

??? success "Reveal answer"
    **In short:** Use IAM Identity Center (SSO) into permission sets across Organisation accounts — human users should not hold access keys.
    
    **Key points**
    
    - **Identity Center** — one human identity, many account roles
    - **Permission sets** — least privilege per account
    - **CLI** — short-lived SSO credentials
    - **Break-glass** — audited emergency role
    
    **Trap**
    
    - Ten sets of long-lived access keys in a password manager

**39. How do you set up RBAC in Amazon EKS?**

??? success "Reveal answer"
    **In short:** EKS RBAC is Kubernetes Role/ClusterRole bindings, plus AWS IAM mapping into those subjects.
    
    **Key points**
    
    - **Least privilege** — Role per namespace; ClusterRole only when needed
    - **Bind** — RoleBinding/ClusterRoleBinding to groups/users
    - **AWS map** — access entries or aws-auth to those groups
    - **Audit** — kubectl auth and policy-as-code (OPA/Kyverno)
    
    **Trap**
    
    - Giving every engineer `cluster-admin` via a shared IAM role

**40. How do you make s3 secure which is have client sensitive data?**

??? success "Reveal answer"
    **In short:** Sensitive client data in S3: Block Public Access, SSE-KMS CMK, tight IAM, optional Object Lock, and access logging.
    
    **Key points**
    
    - **Encryption** — SSE-KMS with key policies
    - **Access** — no public ACLs; VPC endpoints for private access
    - **Governance** — Object Lock/legal hold when required
    - **Detect** — Macie for sensitive data discovery where licensed
    
    **Trap**
    
    - Public-read ACL 'temporarily' for a partner integration

**41. How do you provide rds ready only access to developer?**

??? success "Reveal answer"
    **In short:** Give developers IAM auth or a DB user with SELECT-only, preferably through a read replica endpoint.
    
    **Key points**
    
    - **Prefer replica** — keep load off primary
    - **IAM DB auth** or Secrets Manager-rotated read user
    - **Network** — SG allows only from corporate/VPN/bastion
    - **No DDL** — revoke create/drop on that user
    
    **Trap**
    
    - Sharing the primary master password in Slack

**42. An S3 bucket was made public by mistake. How do you secure and audit it?**

??? success "Reveal answer"
    **In short:** Immediately Block Public Access and close the policy/ACL, then audit who accessed what with CloudTrail/Macie.
    
    **Key points**
    
    - **Contain** — BPA on; remove public ACL/policy statements
    - **Rotate** — any data or keys that may have leaked
    - **Audit** — CloudTrail data events; S3 server access logs
    - **Prevent** — SCP/Config rule denying public buckets
    
    **Try this**
    
    - `aws s3api get-public-access-block --bucket BUCKET`
    
    **Trap**
    
    - Only 'fixing the policy' without checking whether objects were downloaded

**43. How do you did cost optimization in AWS?**

??? success "Reveal answer"
    **In short:** Cost wins come from rightsizing, purchasing models, storage lifecycle, and turning off idle — measured in Cost Explorer.
    
    **Key points**
    
    - **Compute** — rightsizing; Spot/Savings Plans/RIs where stable
    - **Storage** — S3 tiers/lifecycle; delete orphan EBS/snapshots
    - **Network** — NAT/data transfer awareness
    - **Hygiene** — budgets, anomaly detection, idle ASG/RDS
    
    **Trap**
    
    - Buying 3-year RIs on a fleet you plan to re-architect next quarter

**44. How do you implement best security policies on AWS?**

??? success "Reveal answer"
    **In short:** Codify baselines: SCPs, Config conformance packs, Security Hub standards, and mandatory encryption tags.
    
    **Key points**
    
    - **Prevent** — SCPs and permission boundaries
    - **Detect** — Security Hub + GuardDuty + Config
    - **Secure SDLC** — IaC scanning in pipelines
    - **Patch** — Inspector + SSM patch policies
    
    **Trap**
    
    - A beautiful policy doc with no technical enforcement

**45. How do you scan the vulnerabilities specially for AWS instances?**

??? success "Reveal answer"
    **In short:** Scan instances with Inspector (CVE), keep SSM patch compliance, and scan AMIs/images in the pipeline.
    
    **Key points**
    
    - **Inspector** — host and ECR image findings
    - **Patch Manager** — baselines and maintenance windows
    - **AMI pipeline** — Image Builder + vuln gate before promote
    - **Runtime** — GuardDuty malware/runtime findings where enabled
    
    **Trap**
    
    - Monthly CVE spreadsheet with no patch SLA

**46. How do you maintain the lifecycle of an S3 bucket?**

??? success "Reveal answer"
    **In short:** S3 lifecycle rules move/expire objects by age/prefix — including aborting incomplete multipart uploads.
    
    **Key points**
    
    - **Transitions** — Standard → IA/Glacier/Deep Archive by pattern
    - **Expire** — logs and temp prefixes on a timer
    - **Versions** — expire noncurrent versions
    - **Multipart** — abort incomplete after N days
    
    **Try this**
    
    - `aws s3api get-bucket-lifecycle-configuration --bucket BUCKET`
    
    **Trap**
    
    - Lifecycle deleting objects still needed for ransomware recovery

**47. How do you configure AWS RDS, and what factors do you consider (size, requirements, etc.)?**

??? success "Reveal answer"
    **In short:** Size RDS from workload: engine, Multi-AZ, storage type/IOPS, connections, backup RPO — then load-test.
    
    **Key points**
    
    - **Class/storage** — CPU/mem and gp3/io1 needs
    - **HA** — Multi-AZ; read replicas for scale-out reads
    - **Security** — private subnet, SG, encryption, IAM auth
    - **Ops** — PITR windows, Parameter/Option groups, monitoring
    
    **Trap**
    
    - Picking db.t3 'because cheaper' for a write-heavy checkout DB

**48. How do you update the statefile from local to S3 bucket,what will you do if it gets lost?**

??? success "Reveal answer"
    **In short:** Migrate Terraform state with `terraform init -migrate-state` to S3 (+ DynamoDB lock); restore from versioning if lost.
    
    **Key points**
    
    - **Move** — configure backend; migrate; verify plan
    - **Protect** — versioning, encryption, tight IAM on state bucket
    - **Lost state** — restore object version or careful re-import
    - **Never** — commit state to Git as the only copy
    
    **Try this**
    
    - `terraform init -migrate-state`
    
    **Trap**
    
    - Deleting the state bucket to 'clean up' without backups

**49. How do you upgrade your eks?**

??? success "Reveal answer"
    **In short:** Upgrade EKS control plane (managed), then node groups/add-ons in waves — respect skew policy.
    
    **Key points**
    
    - **Docs first** — version skew and add-on matrix
    - **Control plane** — update; validate API
    - **Add-ons / nodes** — surge or blue/green node groups
    - **Workloads** — PDBs and smoke tests each wave
    
    **Try this**
    
    - `aws eks update-cluster-version --name CLUSTER --kubernetes-version 1.30`
    
    **Trap**
    
    - Jumping two minor versions on nodes ahead of the control plane

**50. How do you manage and connect services like DBs, EC2, EKS, or ECS? Include the command to connect to ECS?**

??? success "Reveal answer"
    **In short:** Prefer private connectivity and IAM: SG + endpoints for data planes; `aws ecs execute-command` for ECS shells.
    
    **Key points**
    
    - **Data stores** — private subnets; app roles via IAM/Secrets Manager
    - **EKS** — IRSA/Pod Identity to AWS APIs
    - **ECS Exec** — `aws ecs execute-command --interactive --command /bin/sh`
    - **EC2** — SSM Session Manager over SSH bastions when possible
    
    **Try this**
    
    - `aws ecs execute-command --cluster C --task T --container APP --interactive --command "/bin/sh"`
    - `aws ssm start-session --target i-0123456789abcdef0`
    
    **Trap**
    
    - Public RDS 'so developers can connect from home'

## Related
- Course: [AWS](../aws/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
