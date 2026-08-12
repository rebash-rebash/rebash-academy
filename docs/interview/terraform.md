---
title: "Terraform Interview Preparation"
description: "40 curated Terraform interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: terraform
tags:
  - interview
  - terraform
comments: false
---

{% raw %}
# Terraform Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. Can you explain the difference between Terraform and Ansible?**

??? success "Reveal answer"
    Terraform focuses on provisioning and managing infrastructure lifecycle end to end -- create, modify, delete -- using
    declarative HCL configuration across cloud providers. Ansible is primarily a configuration management tool,
    automating software deployment and configuration on servers that already exist, using procedural YAML playbooks,
    and it doesn't manage infrastructure provisioning the way Terraform does.

**2. writedown the few terraform commands and explain each cmd?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Terraform, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**3. Draw and explain your Terraform repository structure. How do your dev, qa, and prod environments consume shared modules like the VPC module?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**4. Terraform state file is corrupted or lost. What are your options?**

??? success "Reveal answer"
    + Check if there is a backup in remote backend (S3/versioning). * Knowledge of state backends
    + Recover the state from backup if available. * Disaster think
    i bee r rec inki
    | If no backup, import existing resources using “terraform import”. * Resource ews ai 5
    + Recreate state by mapping real infrastructure to Terraform. * Prevention mindset
    6)

**5. What are common Terraform anti- i i-patterns you avoid?**

??? success "Reveal answer"
    + Hardcoding values (use variables, tfvars, or ter ar i ore a
    i: : parameter store). * Best practices awareness
    : Pe thi ged: " * Experience from past issues
    or everything. * Scalable archi inki
    i ate co : st architecture thinking
    2 ee dg renal selec halen pe cane
    it Rae ho using remote state ing. . C * Opinionated but tical mindset
    @

## Scenarios and troubleshooting

**6. How do you structure Terraform code for a large production environment with multiple environments?**

??? success "Reveal answer"
    Structuring Terraform for multiple environments is where many teams make mistakes. The goal is 
    to avoid code duplication while maintaining environment isolation. 
    Recommended: Terraform Workspaces + modules (or separate state per environment) 
    The module-based approach (most production-grade): 
    terraform/ 
    ├── modules/ ← reusable building blocks 
    │ ├── vpc/ 
    │ │ ├── main.tf 
    │ │ ├── variables.tf 
    │ │ └── outputs.tf 
    │ ├── ecs-service/ 
    
     
    │ │ ├── main.tf 
    │ │ ├── variables.tf 
    │ │ └── outputs.tf 
    │ └── rds/ 
    │ ├── main.tf 
    │ ├── variables.tf 
    │ └── outputs.tf 
    │ 
    ├── environments/ 
    │ ├── dev/ 
    │ │ ├── main.tf ← calls modules with dev values 
    │ │ ├── variables.tf 
    │ │ └── terraform.tfvars ← dev-specific values 
    │ ├── staging/ 
    │ │ ├── main.tf 
    │ │ ├── variables.tf 
    │ │ └── terraform.tfvars 
    │ └── prod/ 
    │ ├── main.tf 
    │ ├── variables.tf 
    │ └── terraform.tfvars 
    │ 
    └── global/ 
     ├── iam/ ← IAM roles (shared across envs) 
     └── route53/ ← DNS (shared) 
    The ECS service module: 
    # modules/ecs-service/main.tf 
    variable "service_name" { type = string } 
    variable…

**7. Describe a production failure caused by terraform apply. What guardrails would you implement to prevent it permanently?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Terraform, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**8. How to enable Debug logs in Terraform?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Terraform, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**9. Say I created an S3 bucket using Terraform and want to modify the bucket name. Is it possible? How would you do this?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**10. 2 Instances are created using terraform. Statefile is located locally and also in remote backend(S3). If a user deletes 1 instance what would happen? How would you handle this?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**11. What will happen when a IaC managed resource is modified manually, how would you avoid it?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**12. How would you migrate a Terraform backend from local to a remote backend like S3 with DynamoDB locking?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**13. What happens if the Terraform state becomes corrupted, and how would you recover from it?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**14. In Terraform, how would you create multiple EC2 instances, each with different configurations (for example, different instance types, AMIs, tags, or volumes)?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**15. How would you manage Terraform when multiple teams deploy to the same AWS account but must not overwrite each other’s resources?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

## Practice questions

**16. How do you handle Terraform state management and prevent state corruption in a team environment?**

??? success "Reveal answer"
    Terraform state is the file that maps your configuration to real-world resources. Corrupting or 
    losing this file is one of the most painful experiences in infrastructure management. 
    Remote state with S3 + DynamoDB locking: 
    # Setting up the S3 backend (done once) 
    terraform { 
     backend "s3" { 
     bucket = "company-terraform-state" 
     key = "services/api/production/terraform.tfstate" 
     region = "ap-south-1" 
     encrypt = true 
     kms_key_id = "arn:aws:kms:ap-south-1:123456789:key/abc123" 
     # DynamoDB table for state locking 
     # Prevents two people from running terraform apply simultaneously 
     dynamodb_table = "terraform-state-locks" 
     } 
    } 
    Creating the S3 bucket and DynamoDB table (bootstrap): 
    # bootstrap/main.tf — run this ONCE manually before using remote state 
    resource "aws_s3_bucket" "terraform_state" { 
     bucket = "company-terraform-state" 
    } 
    resource "aws_s3_bucket_versioning" "terraform_state" { 
     bucket = aws_s3_bucket.terraform_state.id 
    
     
     versioning_configuration { 
     status = "Enabled" # Enables recovery from accidental state changes 
     } 
    } 
    resource…

**17. How do you manage cloud infrastructure with Terraform?**

??? success "Reveal answer"
    I define infrastructure in .tf configuration files describing the desired resource state, run terraform init to set up the
    working directory and download providers, terraform plan to preview exactly what will change, and terraform apply to
    provision it. Updates are just changing the config and running apply again, and terraform destroy tears resources
    down cleanly when they're no longer needed.

**18. How do you safely refactor a Terraform monorepo with hundredsgg of state files into a module-based architecture without downtime?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Terraform, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**19. How do you handle versioning in Infrastructure as Code?**

??? success "Reveal answer"
    I store all IaC files in Git, use meaningful commit messages and tags to mark meaningful changes and versions, use
    release branches or tags to manage configuration differences across environments, and integrate that versioned IaC
    with CI/CD pipelines so testing, deployment, and rollback are automated based on the versioned configuration rather
    than manual application.

**20. If something is created on the cloud platform and it is not present in Terraform, how will you achieve it?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**21. You need to create 50 instances in one go. How will you create them in Terraform?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**22. How do you handle multiple environments in Terraform?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**23. How do you call a module from root module?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**24. How do you ensure particular AMI image is present in AWS account using terraform?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**25. How will you connect your terraform environment from aws and implement CI/CD?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**26. How will you write terraform module for EKS?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**27. Question : How do you import a resource into Terraform that was created manually in AWS or GCP? What command would you use?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**28. How do you manage terrform state file?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**29. How do you manage the state file in terraform and where do you store it?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**30. How will you refer the output of vnet module based subnetid as an input to the VM module?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**31. Two engineers are working on the same Terraform code. How do you prevent conflicts and handle Terraform state locking or drift?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**32. How do you set up infrastructure for deploying ML models using Terraform?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**33. How will you implement multi region Terraform code?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**34. What AWS resources have you created using Terraform and how do you promote a read replica to primary using Terraform?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**35. Which components or resources are required to create a 3-tier architecture using Terraform?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**36. How do you scale a Terraform pipeline that takes 25+ mins?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**37. How do you export Azure resources into Terraform code?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**38. How do you enforce Azure Policies (like tag or location restrictions) using Terraform at scale?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**39. How do you implement state locking in terraform?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Terraform components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**40. [ ] Can you describe a real-time scenario where you used Terraform to provision a highly scalable infrastructure?**

??? success "Reveal answer"
    Answer directly for Terraform: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

## Related

- Course: [Terraform](../terraform/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
