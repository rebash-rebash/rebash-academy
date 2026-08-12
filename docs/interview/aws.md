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

## Core concepts

**1. what is the difference between alb and nlb, in which scenario you use alb and nlb?**

??? success "Reveal answer"
    Start with a precise definition in the context of Aws, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**2. What is AWS Lambda and how do you design a serverless application?**

??? success "Reveal answer"
    Start with a precise definition in the context of Aws, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**3. What are the best practices for securing cloud infrastructure?**

??? success "Reveal answer"
    IAM roles and policies following least privilege, encryption for data at rest and in transit, security groups and NACLs
    to control traffic along with AWS WAF for web application protection, CloudTrail and CloudWatch for logging and
    monitoring account activity, and regular security audits to catch vulnerabilities and confirm ongoing compliance.

**4. Explain the AWS architecture shown in the diagram (CodePipeline, CodeBuild, CodeDeploy, CloudFormation, CloudWatch)?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**5. How do you scale EKS? What are the metrics considered and where do you add your inputs and How? Explain how you have done auto-scaling in your project?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

## Scenarios and troubleshooting

**6. What if production rds is growing 95% how do you debug and how do you prevent this in future?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Aws, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**7. Q9: In lambda function, how would you handle failures and how would you set up retries?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Aws, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**8. How do you identify the root cause of a production outage?**

??? success "Reveal answer"
    * Review logs, metrics, traces across all layers. * Systematic troubleshooting
    | + Follow the request flow end-to-end (User + LB —+ App — DB — External). + End-to-end thinking
    | + Correlate events and identify the first point of failure. * Ability to drill down
    | + Use tools: logs, APM, metrics, traces, dashboards. + Strong debugging skills
    | + Reproduce issue in staging if possible to confirm. * Data-driven decisions
    (2)

**9. You want to create an EC2, and while creating the instance, you are getting an error like IP address exceeded. How will you troubleshoot and fix it?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Aws, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**10. Say you need to configure EC2 instances automatically or replace themselves automatically when they fail. How do you implement this?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Aws, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**11. How to spead up s3 upload with files in large size, and client uploaded 10 Gb file but failed after uploading 5 gb how you confirm that 5 gb is uploaded to s3?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Aws, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**12. You are having lambda function and role everything setup perfectly but logs are not coming up in the cw group how to troubleshoot?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Aws, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**13. RDS migration with minimal downtime – how would you approach it?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Aws, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**14. If there is a vendor who provides VPN services for company A, his manager wants to view some dashboard but do not have AWS account. How would you help him?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**15. How would you set up networking in vpc?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**16. Q8: How would you store secure info inside s3?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**17. how would you maintain high availability in ecs + fargate or eks?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**18. What are the security parameters we must consider while we are creating an EC2 instance for production?**

??? success "Reveal answer"
    Start with a precise definition in the context of Aws, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

## Practice questions

**19. How do you design a multi-region active-active deployment on AWS?**

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

**20. How do you implement infrastructure as code on AWS using CloudFormation vs CDK?**

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

**21. Design a highly available backend on AWS – what services and architecture would you use?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**22. How to design an event-driven architecture using S3, Lambda, and SNS for data ingestion?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**23. design an high availability, fault tolerance system in aws?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**24. What cloud platforms and AWS services have you worked with?**

??? success "Reveal answer"
    I've worked extensively with EC2 for scalable compute, S3 for object storage, RDS for managed relational
    databases, Lambda for serverless workloads, VPC for network isolation, CloudFormation and Terraform for
    infrastructure as code, and EKS for managing Kubernetes clusters -- the core services that make up most real-world
    AWS architectures I've built or maintained.

**25. Q8. You found memory pressure on RDS. You cannot resize. What immediate action can you take without downtime?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Aws, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**26. If any service is down for more than 2 weeks and customer is asking for update, what will you tell to customer?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Aws, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**27. EC2 instance is unreachable, and it’s not a security group issue. What’s your next step?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Aws, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**28. What will you do for zero-downtime when eks cluster upgrade?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Aws, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**29. How do you monitor network traffic in AWS?**

??? success "Reveal answer"
    VPC Flow Logs capture accepted and rejected traffic at the ENI level, which is my first stop for understanding
    whether traffic is being blocked and where, and I pair that with CloudWatch metrics and alarms for ongoing visibility
    into network-level health.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    0
    5
    AZURE NETWORKING QUESTIONS

**30. You have RDS and tomorrow, I being your client, will tell you that you need to make the configuration in such a way so that only one user can access the RDS at a time. How will you configure that?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**31. You have an EC2 instance and you would like to migrate it from one region to another. How will you do it?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**32. How do you secure your environments in aws?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**33. How do you restrict access to AWS resources for a specific user?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**34. How do you restrict a user to only EC2 and RDS access?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**35. How do you ensure the least privilege access to the IAM users?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**36. How do you login to the ec2 instance if you've lost the .pem key?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**37. You have created an IAM user in AWS and configured role-based access in EKS. How do you bind the IAM user to the EKS role?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**38. Assume you have 10 AWS accounts. How will you securely log in to them, considering access keys are not used for security reasons?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**39. How do you set up RBAC in Amazon EKS?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**40. how do you make s3 secure which is have client sensitive data?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**41. How do you provide rds ready only access to developer?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**42. An S3 bucket was made public by mistake. How do you secure and audit it?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**43. How do you did cost optimization in AWS?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**44. How do you implement best security policies on AWS?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**45. How do you scan the vulnerabilities specially for AWS instances?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**46. How do you maintain the lifecycle of an S3 bucket?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**47. How do you configure AWS RDS, and what factors do you consider (size, requirements, etc.)?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**48. How do you update the statefile from local to S3 bucket,what will you do if it gets lost?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**49. How do you upgrade your eks?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**50. How do you manage and connect services like DBs, EC2, EKS, or ECS? Include the command to connect to ECS?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Aws components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

## Related

- Course: [AWS](../aws/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
