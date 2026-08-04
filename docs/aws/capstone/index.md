---
title: Capstone
description: "Capstone: design a production-minded AWS landing zone with multi-account governance, networking, IAM, observability, and cost controls."
technology_id: aws
hide:
  - toc
author: Shaik Basha
last_updated: "2026-08-03"
category: aws
tags:
  - aws
  - capstone
comments: false
---

# AWS — Capstone

## Goal

Design (and partially implement in a sandbox) a **production AWS landing zone** you can defend in an architecture interview.

## Required outcomes

- [ ] Multi-account sketch: management, identity, log archive, shared services, prod, non-prod  
- [ ] Network: VPC CIDR plan, no overlapping ranges, endpoints vs NAT decision recorded  
- [ ] IAM: Identity Center permission sets **or** documented federation; no long-lived admin keys  
- [ ] Guardrails: sample SCP JSON + tagging standard  
- [ ] Observability: CloudTrail org trail design + CloudWatch alarms for billing and a critical metric  
- [ ] Delivery: IaC layout (Terraform or CloudFormation) and CI OIDC trust notes  
- [ ] Cost: Budgets + “expensive services we deny in sandbox” list  
- [ ] DR: RTO/RPO for one critical data store  

## Suggested build order

1. Complete [Module 15](../production-aws-landing-zones.md) artefacts  
2. Implement one account’s VPC + baseline with [Module 11](../infrastructure-as-code-on-aws.md)  
3. Add identity and logging patterns from Modules 2 and 9–10  
4. Run [troubleshooting](../troubleshooting-aws.md) against your own stack  
5. Present a 10-minute architecture review aloud  

## References

- [Production AWS Landing Zones](../production-aws-landing-zones.md)
- [Reliability and Disaster Recovery](../reliability-and-disaster-recovery.md)
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/)
