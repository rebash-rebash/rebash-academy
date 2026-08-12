---
title: "AWS Interview Preparation"
description: "50 curated interview questions and model answers for AWS — concepts, scenarios, troubleshooting, and production trade-offs."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. Can you explain how to set up auto-scaling for an application?**

??? success "Reveal answer"
    Launch and configure an EC2 instance as the template, create a Launch Template or Configuration capturing the
    AMI, instance type, security groups, and user data, create an Auto Scaling Group referencing that template across
    chosen subnets and AZs, define scaling policies -- target tracking, step scaling, or scheduled -- based on metrics like
    CPU utilization, attach a load balancer if traffic needs to be distributed across instances, and monitor with
    CloudWatch to fine-tune the policies over time.
    KEY POINTS TO MENTION
    • Launch template → ASG → scaling policy (target tracking/step/scheduled) → attach LB → monitor & tune
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**2. What is the difference between IaaS, PaaS, and SaaS?**

??? success "Reveal answer"
    IaaS, like EC2, gives virtualized compute and networking while I manage the OS, runtime, and application myself.
    PaaS, like Elastic Beanstalk, manages the OS and runtime for me so I just deploy application code. SaaS, like
    Salesforce or Office 365, is fully managed software I simply use, with no infrastructure or platform management on
    my end at all.
    KEY POINTS TO MENTION
    • IaaS: EC2 — full control, most responsibility
    • PaaS: Elastic Beanstalk — deploy code only
    • SaaS: fully managed application, no infra/platform responsibility
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    1
    6
    CLOUD COMPUTING & AZURE DEVOPS

**3. What is infrastructure drift i fa cd rastructure drift and how do you detect and fix it?**

??? success "Reveal answer"
    + Store state in a remote backend (S3 + Dynamol i
    + DB locking). Te Llaborati i
    + Enable state locking to avoid concurrent writes. , <a tas na oe dane
    4 + Use workspaces or multiple state files per environment. * Securit a ee F
    4 + Restrict access using IAM policies. * ee
    + Follow least privilege & audit access to state. ® Scale & mai sais
    é maint ili
    -9 ®

**4. What are the best practices for securing cloud infrastructure?**

??? success "Reveal answer"
    IAM roles and policies following least privilege, encryption for data at rest and in transit, security groups and NACLs
    to control traffic along with AWS WAF for web application protection, CloudTrail and CloudWatch for logging and
    monitoring account activity, and regular security audits to catch vulnerabilities and confirm ongoing compliance.

**5. What is AWS PrivateLink?**

??? success "Reveal answer"
    PrivateLink provides private connectivity between VPCs and AWS services without that traffic ever traversing the
    public internet -- I've used it to expose an internal service to another team's VPC securely, without a full VPC peering
    connection or public exposure.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**6. What is AWS Global Accelerator?**

??? success "Reveal answer"
    Global Accelerator routes traffic through AWS's global backbone network instead of the public internet's variable
    path, reducing latency and improving performance and availability for globally distributed users hitting an application.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**7. What is AWS Direct Connect?**

??? success "Reveal answer"
    Direct Connect provides a dedicated, private, low-latency physical connection between on-prem data centres and
    AWS, bypassing the public internet entirely -- I'd recommend it for consistent high-bandwidth needs or strict
    compliance requirements around data never touching the public internet.

**8. What is VPC Peering?**

??? success "Reveal answer"
    VPC Peering creates a direct network connection between two VPCs so resources in each can communicate as if
    they were on the same network. It's simple to set up but doesn't scale well past a handful of VPCs since it isn't
    transitive -- each pair needs its own dedicated peering connection.

**9. What is the role of DNS A and CNAME Records in DevOps?**

??? success "Reveal answer"
    An A record maps a domain directly to an IP address, while a CNAME record maps a domain to another domain
    name. I use A records for root domains pointing at a fixed IP and CNAMEs for subdomains pointing at services like a
    load balancer or CDN endpoint whose underlying IP might change.

**10. What is a Transit Gateway?**

??? success "Reveal answer"
    Transit Gateway acts as a central hub connecting multiple VPCs and on-prem networks, which dramatically simplifies
    networking once you have more than a couple of VPCs that need to talk to each other, replacing what would
    otherwise be a messy mesh of individual VPC peering connections.

**11. What is AWS ECS vs EKS?**

??? success "Reveal answer"
    ECS (Elastic Container Service): AWS-native orchestrator, simpler to operate, tightly integrated 
    with AWS services. EKS (Elastic Kubernetes Service): Managed Kubernetes, industry-standard API, 
    more complex but portable. Choose ECS for simplicity, EKS for Kubernetes compatibility.

**12. What is pg_dump and how do you automate database backups?**

??? success "Reveal answer"
    pg_dump -h $DB_HOST -U $DB_USER -d mydb -Fc > backup-$(date +%Y%m%d).dump 
    # Upload to S3 
    aws s3 cp backup-$(date +%Y%m%d).dump s3://my-backups/postgres/ 
    # Automate as Kubernetes CronJob: 
    # schedule: "0 2 * * *" # Daily at 2 AM 
     
     
    
     
    BEHAVIORAL QUESTIONS

**13. What is an Application Security Group (ASG)?**

??? success "Reveal answer"
    ASGs let me group VMs logically for simplified NSG rule management -- instead of writing rules against individual
    IPs, I can write a rule against an application tier's ASG and add or remove VMs from that group without touching the
    NSG rules themselves.

**14. What is a VPC in AWS?**

??? success "Reveal answer"
    A VPC is a private, logically isolated network within AWS where I control the IP address range, subnets, route tables,
    and gateways -- it's the foundational building block for every piece of AWS infrastructure I provision.

**15. What is Route 53?**

??? success "Reveal answer"
    Route 53 is AWS's DNS service, and I use it for more than basic hosting -- health-check-based failover routing and
    weighted routing policies let it actively contribute to application availability, not just resolve names.

**16. What is a Security Group vs NACL?**

??? success "Reveal answer"
    Security Group: stateful, instance-level firewall (return traffic automatically allowed). NACL 
    (Network ACL): stateless, subnet-level firewall (return traffic must be explicitly allowed). Use both 
    in defense-in-depth.

**17. Can you explain the role of Azure Boards in Agile development?**

??? success "Reveal answer"
    Azure Boards provides Kanban boards, backlogs, sprint planning, and reporting for Agile teams, letting them manage
    user stories, tasks, and bugs collaboratively with full visibility throughout the development process.

**18. What is an Internet Gateway in AWS?**

??? success "Reveal answer"
    An Internet Gateway attaches to a VPC and enables two-way internet connectivity for resources in public subnets,
    which is the piece that actually makes a subnet "public" once paired with the right route table entry.

**19. What is an IAM Role vs IAM User?**

??? success "Reveal answer"
    An IAM User has permanent credentials (access key + secret). An IAM Role has temporary 
    credentials obtained via STS AssumeRole. Use roles for EC2 instances, Lambda, and CI/CD systems 
    — never long-lived users.

**20. What is AWS Secrets Manager?**

??? success "Reveal answer"
    A secrets management service with automatic rotation, cross-account access, and fine-grained 
    IAM policies. More expensive than Parameter Store but supports native rotation for RDS, 
    Redshift, and DocumentDB.

**21. What is a read replica?**

??? success "Reveal answer"
    A copy of the primary database that handles read-only queries. Reduces load on the primary, 
    improves read performance, and provides a standby for failover. AWS RDS Multi-AZ provides 
    automatic failover.

**22. What is an Egress-Only Internet Gateway?**

??? success "Reveal answer"
    It's specifically for IPv6 traffic -- it allows outbound connectivity from a VPC while blocking any unsolicited inbound
    traffic, functioning as the IPv6 equivalent of what a NAT Gateway does for IPv4.

**23. What is irate() vs rate() in PromQL?**

??? success "Reveal answer"
    rate() calculates the per-second average over the time window — more stable. irate() uses 
    only the last two data points — more responsive to spikes. Use rate() for alerting, irate() for 
    dashboards.

**24. What is an AWS Lambda function?**

??? success "Reveal answer"
    A serverless compute service that runs code in response to events without provisioning servers. 
    Executes in 15 minutes maximum. Used for data processing, API backends, and event-driven 
    automation.

**25. What is AWS CodeCommit?**

??? success "Reveal answer"
    A fully managed private Git repository service. Secure, highly available, and integrated with IAM 
    for access control. It's being deprecated — AWS announced end of new customer onboarding in 
    2024.

**26. What is IRSA (IAM Roles for Service Accounts)?**

??? success "Reveal answer"
    An EKS feature that allows Pods to assume IAM roles using Kubernetes ServiceAccounts, via OIDC 
    federation. Replaces storing AWS credentials in secrets — fine-grained, pod-level AWS 
    permissions.

**27. What is AWS CDK?**

??? success "Reveal answer"
    Cloud Development Kit — define AWS infrastructure using Python, TypeScript, Java, or C#. CDK 
    synthesizes to CloudFormation templates. Provides high-level constructs that encode best 
    practices.

**28. What is EventBridge?**

??? success "Reveal answer"
    A serverless event bus that connects AWS services, SaaS applications, and custom applications. 
    Replaces CloudWatch Events with more features including schema registry and cross-account 
    events.

**29. What is AWS CloudWatch?**

??? success "Reveal answer"
    A monitoring service for collecting metrics, logs, and events. Supports dashboards, alarms, 
    anomaly detection, and log insights queries. The default observability service for all AWS services.

**30. What is AWS X-Ray?**

??? success "Reveal answer"
    A distributed tracing service for analyzing and debugging distributed applications. Instruments 
    requests as they flow through microservices and shows performance bottlenecks in a service 
    map.

**31. What is AWS Elastic Beanstalk?**

??? success "Reveal answer"
    A PaaS service that handles infrastructure provisioning, load balancing, auto scaling, and 
    monitoring for web applications. You upload code; Beanstalk manages the rest. Good for simple 
    apps.

**32. What is Redis Sentinel vs Redis Cluster?**

??? success "Reveal answer"
    Sentinel: high availability for a single Redis instance — automatic failover but no horizontal 
    scaling. Cluster: horizontally shards data across multiple nodes — both HA and scalability.

**33. What is AWS Lightsail?**

??? success "Reveal answer"
    A simplified cloud platform for small workloads — virtual servers, databases, containers, and CDN 
    with predictable pricing. Targeted at developers who don't need full AWS complexity.

**34. What is AWS Shield?**

??? success "Reveal answer"
    A DDoS protection service. Shield Standard (free) provides automatic protection against common 
    DDoS attacks. Shield Advanced ($3,000/month) provides 24/7 DDoS response team support.

**35. What is the difference between ECS Task Role and Execution Role?**

??? success "Reveal answer"
    Execution Role: used by ECS agent to pull images from ECR and write logs to CloudWatch. Task 
    Role: assumed by the application container to access AWS services (S3, DynamoDB, etc.).

**36. What is AWS Step Functions?**

??? success "Reveal answer"
    A serverless workflow orchestration service for coordinating Lambda functions and AWS services 
    into complex workflows. Supports sequential, parallel, conditional, and retry logic.

**37. What is RDS IAM authentication?**

??? success "Reveal answer"
    Authenticate to RDS using IAM tokens instead of database passwords. The application 
    calls generate-db-auth-token and uses the token as the password — tokens expire in 15 
    minutes.

**38. What is AWS Systems Manager Parameter Store?**

??? success "Reveal answer"
    A service for storing configuration data and secrets as key-value pairs. Supports plain strings and 
    SecureString (KMS-encrypted). Cheaper than Secrets Manager but fewer features.

**39. What is AWS Auto Scaling?**

??? success "Reveal answer"
    Automatically adjusts the number of EC2 instances or ECS tasks based on demand. Types: Target 
    Tracking (maintain a metric), Step Scaling (scale by increments), Scheduled Scaling.

## Scenarios and troubleshooting

**40. Your EC2 i questions. Real . a v¥ Load balancer i o* “ear iatindba de banrine. bs production scenarios N ote issues Ow * —)?**

??? success "Reveal answer"
    “2. Check a troubleshoot? ing but your. application ‘snot: accessible v vec eee
    ai Mest status sible. \ 5
    Verify security & system status (AWS H ae hooting
    8 = yt gp i and id ie a
    —3 ee traffic. : INTERVIEWER
    : ee a ar ep subnet level. # Layered —S
    2 ce aE Sp higulletioay” (netstat. -t eet Sans aes
    3 ~ Revier spy os sod, cnfen. sor ; lee): standing of net
    = fest from inside & Rem service is runni + Ability to isola flow
    3/6 Sipeoyesr +g
    Q:_Users ‘are. getting 5 ple omg Hevelidebingas
    z. *
    ine ee ar loge thing
    -o ANS: ee ed gfe
    i. + Review target as: (unhealthy > it? %
    ; Analyze ALB ae a 7h health checks, port INTERVIEWER L
    ad Check backend applicat 7 target logs. , protocol. ee OOKS FOR:
    md ® a a a a a rae grey S health: check
    GO Noa, Sarmak = , timeout) and delay. og analysis skills knowledge
    ” SSH into ensure auto-healin: a Problem isolad
    ~~ ANS Wak: do goa check an EC2 instance that was work ‘ * Ownershi te
    : + Verify ki BSS working earlier. ip of resolution
    —> Cue Bre, and =. (ec2-user/ubuntu/admin). ? :
    . ck NAI inbound rule ‘ z =
    — > Py SE eu rales (inbound…

**41. How do you monitor the health of a system in production?**

??? success "Reveal answer"
    I track key metrics like CPU, memory, disk, response times, error rates, and throughput, run uptime checks against
    real application endpoints rather than shallow pings, continuously review logs for warnings and errors, set
    threshold-based alerts to get notified in real time, and keep dashboards that show overall system health at a glance.
    KEY POINTS TO MENTION
    • Key metrics, uptime checks, log review, threshold alerts, dashboards

**42. How do you identify the root cause of a production outage?**

??? success "Reveal answer"
    * Review logs, metrics, traces across all layers. * Systematic troubleshooting
    | + Follow the request flow end-to-end (User + LB —+ App — DB — External). + End-to-end thinking
    | + Correlate events and identify the first point of failure. * Ability to drill down
    | + Use tools: logs, APM, metrics, traces, dashboards. + Strong debugging skills
    | + Reproduce issue in staging if possible to confirm. * Data-driven decisions
    (2)

## Practice questions

**43. How do you design a multi-region active-active deployment on AWS?**

??? success "Reveal answer"
    Multi-region active-active means users in every region are served by their local infrastructure 
    simultaneously — it's not failover, it's parallel serving. This is the highest complexity in cloud 
    architecture. 
    Architecture overview: 
     Route 53 (Latency-based routing) 
     / \ 
     ap-south-1 (Mumbai) us-east-1 (Virginia) 
     ───────────────── ───────────────────── 
     ALB ALB 
     │ │ 
     EKS Cluster EKS Cluster 
     │ │ 
     RDS Aurora RDS Aurora 
     └──── Global Cluster ──────────┘ 
     (Replication) 
     │ │ 
     ElastiCache ElastiCache 
     (Region-local) (Region-local) 
    Key components: 
    1. Route 53 Latency-Based Routing: 
    resource "aws_route53_record" "api" { 
     zone_id = var.hosted_zone_id 
     name = "api.myapp.com" 
    
     
     type = "A" 
     # Mumbai record 
     set_identifier = "ap-south-1" 
     latency_routing_policy { 
     region = "ap-south-1" 
     } 
     alias { 
     name = aws_alb.mumbai.dns_name 
     zone_id = aws_alb.mumbai.zone_id 
     evaluate_target_health = true 
     } 
    } 
    resource "aws_route53_record" "api_us" { 
     zone_id = var.hosted_zone_id 
     name = "api.myapp.com" 
     type = "A" 
     set_identifier = "us-east-1" 
    …

**44. How do you implement infrastructure as code on AWS using CloudFormation vs CDK?**

??? success "Reveal answer"
    What are the tradeoffs? 
    Answer: 
    AWS offers two first-party IaC approaches: CloudFormation (declarative JSON/YAML templates) 
    and CDK (Cloud Development Kit — write infrastructure in Python, TypeScript, Java, etc.). 
    CloudFormation — Writing an ECS Service: 
    # cloudformation/ecs-service.yaml 
    AWSTemplateFormatVersion: '2010-09-09' 
    Description: ECS Service with ALB 
    Parameters: 
     Environment: 
    
     
     Type: String 
     AllowedValues: [dev, staging, prod] 
     ContainerImage: 
     Type: String 
     Description: Docker image URI from ECR 
    Conditions: 
     IsProduction: !Equals [!Ref Environment, prod] 
    Resources: 
     # ECS Task Definition 
     TaskDefinition: 
     Type: AWS::ECS::TaskDefinition 
     Properties: 
     Family: !Sub 'my-app-${Environment}' 
     NetworkMode: awsvpc 
     RequiresCompatibilities: [FARGATE] 
     Cpu: !If [IsProduction, '1024', '256'] 
     Memory: !If [IsProduction, '2048', '512'] 
     ExecutionRoleArn: !GetAtt TaskExecutionRole.Arn 
     ContainerDefinitions: 
     - Name: app 
     Image: !Ref ContainerImage 
     PortMappings: 
     - ContainerPort: 8080 
     LogConfiguration: 
     LogDriver: awslogs 
    …

**45. How do reduce s while ke the architecture reliable?**

??? success "Reveal answer"
    + Right-size resources. Cook optimisation mindast 1 4 1 1
    + Use managed services # Use of cloud native services
    =) + Auto Sealing (scale down when not needed) # Auteccaling & efficiency G-GD- tid
    + Use Spot/Reserved Instances where applicable. - Roe Rightrsise Ue managed Auto oecla) «Usa right = Mondter &
    + Implement lifecycle policies (S3, EBS snapshots). mn s 8 - resources services pricing model optimize
    -9 + Monitor & optimize continuously. bs zs —— *
    SIGN THINKING
    CD) lenges pat Water data loud alianond INTERVIEWER LOOKS FOR hs eg A =
    - 9 ANS: + What are the business goals and constraints? 4 . skills
    + What is the expected load and gronth? a eRe ES or ve
    + What are the availability and performance requirements? shea cz! cate a %
    - 9 + What are the compliance and security requirements? ge paar ina seoped ‘ An bs
    + What are the recovery and backup requirements? aed tc L 08 Bestey Moke |
    (a KEY TAKEAWAY: } fae eS Sa
    Fr | - Y Great cloud architectures are built on | ‘ Loup. —= s pF Tin | VERIQTA.
    L lon, for, fallaen-: Onstgn for Saale: J {__ Automated.…

**46. How do you ensure high availability and scalability in the cloud?**

??? success "Reveal answer"
    For high availability: deploying across multiple availability zones for redundancy, Elastic Load Balancing to distribute
    traffic, and Auto Scaling Groups to automatically adjust instance count based on demand. For scalability: horizontal
    scaling by adding or removing instances, leveraging managed services like RDS read replicas or DynamoDB for
    database scalability, and caching with ElastiCache to reduce database load and improve response times.
    KEY POINTS TO MENTION
    • HA: Multi-AZ, ELB, Auto Scaling Groups
    • Scalability: horizontal scaling, RDS read replicas/DynamoDB, ElastiCache

**47. What cloud platforms and AWS services have you worked with?**

??? success "Reveal answer"
    I've worked extensively with EC2 for scalable compute, S3 for object storage, RDS for managed relational
    databases, Lambda for serverless workloads, VPC for network isolation, CloudFormation and Terraform for
    infrastructure as code, and EKS for managing Kubernetes clusters -- the core services that make up most real-world
    AWS architectures I've built or maintained.

**48. How do you monitor network traffic in AWS?**

??? success "Reveal answer"
    VPC Flow Logs capture accepted and rejected traffic at the ENI level, which is my first stop for understanding
    whether traffic is being blocked and where, and I pair that with CloudWatch metrics and alarms for ongoing visibility
    into network-level health.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    0
    5
    AZURE NETWORKING QUESTIONS

**49. How are DNS MX Records used in DevOps?**

??? success "Reveal answer"
    MX records specify the mail servers responsible for receiving email for a domain -- as a DevOps engineer, I make
    sure these are configured correctly whenever we're setting up email services or notification systems that depend on
    outbound or inbound mail actually routing to the right place.

**50. How do Security Groups work in AWS?**

??? success "Reveal answer"
    Security Groups are stateful, instance-level virtual firewalls -- I define allow rules for inbound and outbound traffic,
    and because they're stateful, a response to an allowed inbound request is automatically permitted outbound without
    needing a matching explicit rule.

## Related

- Course: [AWS](../aws/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
