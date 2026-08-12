---
title: "Terraform Interview Preparation"
description: "65 curated Terraform interview prompts — model answers plus real interview questions collected across companies (deduplicated by topic)."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. What is Ansible, and how does it differ from Terraform?**

??? success "Reveal answer"
    This is a very common interview question, and the key is understanding that Ansible and 
    Terraform solve different problems — they're complementary, not competing. 
    Ansible is a configuration management tool: 
    • 
    Installs software, configures services, manages files 
    • 
    Procedural — you define how to get to the desired state 
    • 
    Agentless — uses SSH 
    • 
    Good for: Server setup, application deployment, ad-hoc task automation 
    • 
    State management: Stateless (runs tasks top-to-bottom; no state file) 
    Terraform is an infrastructure provisioning tool: 
    • 
    Creates, modifies, and destroys cloud resources (EC2 instances, VPCs, RDS databases) 
    • 
    Declarative — you define what the desired state is 
    • 
    API-based — communicates with cloud APIs 
    • 
    Good for: Provisioning cloud infrastructure 
    • 
    State management: Maintains a state file (terraform.tfstate) 
    Typical combined workflow: 
    
     
    Terraform provisions: Ansible configures: 
    → EC2 instances → Installs Nginx on EC2 
    → Security groups → Deploys application code 
    → RDS database → Configures application settings 
    → VPC/subnets…

**2. Explain Terraform's core workflow: init, plan, apply, destroy.**

??? success "Reveal answer"
    Terraform follows a three-command workflow for all infrastructure changes. Understanding what
    each command does — and does not do — is fundamental.
    # 1. terraform init
    # Downloads providers, initializes backend, prepares working directory
    terraform init
    # What it does:
    # - Downloads provider plugins (aws, kubernetes, etc.) to .terraform/
    # - Initializes the backend (where state file is stored)
    # - Downloads modules referenced in configuration
    # - Does NOT connect to your infrastructure or make any changes
    # 2. terraform plan
    # Shows what changes Terraform will make — without making them
    terraform plan -out=tfplan
    # Output symbols:
    # + = resource will be CREATED
    # - = resource will be DESTROYED
    # ~ = resource will be MODIFIED IN-PLACE
    # -/+ = resource will be DESTROYED and RECREATED
    # 3. terraform apply
    # Makes the actual changes
    terraform apply tfplan # Use the saved plan file
    
    # OR (interactive):
    terraform apply # Shows plan again and asks for confirmation
    # 4. terraform destroy
    # Destroys all resources managed by this configuration
    terraform destroy
    # DANGER:…

**3. What is Infrastructure as Code?**

??? success "Reveal answer"
    N pt
    [i ae a ee a ee resource “aws_instance” “web”
    —> Infrastructure as Code manages infrastructure through | ami = “ami 123456" ;
    version-controlled configuration files. — } eae Eye > ieee
    3
    What is configuration management ? Toe
    > Configuration management keeps servers and systems — Z\ =
    in a consistent, desired state. V)
    What is immutable infrastructure ?
    —> Immutable infrastructure replaces servers or containers tw ll ditt
    instead of modifying them after deployment.
    What is shift-left testing ? Pee pei ee
    > Shift-left testing performs testing earlier in the [an Cae) Build ) Tet) Rete) Deply )
    software development lifecycle. Plan ) Code) Build) Test ) Release)» Deploy »
    ee JyothiMulkuntla ae Page 1
    
    Ce
    22 Ne
    no Dirthe Fratoteh Sots ies, Series ond Apbaes
    
    Linux and Networking
    (it) How do you check disk usage in Linux? = fees
    $ df -h
    a Use df -h for Filesystem usage and Filesystem Size Used Avail Use% Mounted on
    Ay ek, ber directory usage. =e 50G 20G 28G 42% /

**4. What is Infrastructure as Code (IaC), and how does it benefit a DevOps environment?**

??? success "Reveal answer"
    IaC manages and provisions infrastructure through machine-readable configuration files instead of manual,
    interactive setup. It gives consistency across environments, efficiency through automation instead of manual
    intervention, easy scalability by replicating components, version control and audit trails for infrastructure just like
    application code, and a shared language for collaboration between teams.
    KEY POINTS TO MENTION
    • Consistency, efficiency, scalability, version control, collaboration

**5. What is IAC?**

??? success "Reveal answer"
    IAC means Infrastructure As Code. It is the process through which we automate all admin tasks. We
    write code (e.g., Ruby script in Chef). When you apply this code, it is automatically converted into
    Infrastructure. Advantages:
    • Code is Testable (Testing code is easier than testing Infrastructure)
    • Code is Repeatable (Can re-use the same code again and again)
    • Code is Versionable (Can store in versions and retrieve any previous version at any time)

**6. Can you explain the difference between Terraform and Ansible?**

??? success "Reveal answer"
    Terraform focuses on provisioning and managing infrastructure lifecycle end to end -- create, modify, delete -- using
    declarative HCL configuration across cloud providers. Ansible is primarily a configuration management tool,
    automating software deployment and configuration on servers that already exist, using procedural YAML playbooks,
    and it doesn't manage infrastructure provisioning the way Terraform does.

**7. Terraform state file is corrupted or lost. What are your options?**

??? success "Reveal answer"
    + Check if there is a backup in remote backend (S3/versioning). * Knowledge of state backends
    + Recover the state from backup if available. * Disaster think
    i bee r rec inki
    | If no backup, import existing resources using “terraform import”. * Resource ews ai 5
    + Recreate state by mapping real infrastructure to Terraform. * Prevention mindset
    6)

**8. What are common Terraform anti- i i-patterns you avoid?**

??? success "Reveal answer"
    + Hardcoding values (use variables, tfvars, or ter ar i ore a
    i: : parameter store). * Best practices awareness
    : Pe thi ged: " * Experience from past issues
    or everything. * Scalable archi inki
    i ate co : st architecture thinking
    2 ee dg renal selec halen pe cane
    it Rae ho using remote state ing. . C * Opinionated but tical mindset
    @

**9. What is Bicep?**

??? success "Reveal answer"
    A domain-specific language for Azure infrastructure as code. Compiles to ARM templates. Much 
    cleaner syntax than JSON ARM templates. 
    resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = { 
     name: 'mystorageaccount' 
     location: 'eastus' 
     sku: { name: 'Standard_LRS' } 
     kind: 'StorageV2' 
    }

**10. What is a Terraform data source?**

??? success "Reveal answer"
    Reads existing infrastructure information without managing it. 
    data "aws_ami" "ubuntu" { 
     most_recent = true 
     owners = ["099720109477"] # Canonical 
     filter { 
     name = "name" 
     values = ["ubuntu/images/hvm-ssd/ubuntu-*-22.04-amd64-server-*"] 
     } 
    }

**11. What is the assert module?**

??? success "Reveal answer"
    Validates conditions and fails with a custom message if they're not met. Used for input validation 
    at the start of playbooks. 
    - assert: 
     that: 
     - app_version is defined 
     - app_version | length > 0 
     fail_msg: "app_version must be provided"

**12. What is terraform import?**

??? success "Reveal answer"
    Brings existing infrastructure under Terraform management without recreating it. 
    terraform import aws_s3_bucket.my_bucket my-existing-bucket 
    Note: import only updates state — you still need to write the matching HCL configuration.

**13. What is the template module?**

??? success "Reveal answer"
    Renders a Jinja2 template file and copies it to the target host. Variables from Ansible are available 
    in the template. 
    - template: 
     src: nginx.conf.j2 
     dest: /etc/nginx/nginx.conf 
     mode: '0644' 
    
     
     validate: nginx -t -c %s

**14. What is Terraform's precondition and postcondition?**

??? success "Reveal answer"
    Validation checks on resource attributes. 
    lifecycle { 
     precondition { 
     condition = var.instance_type != "t2.micro" || var.environment == 
    "dev" 
     error_message = "t2.micro is only allowed in dev environment" 
     } 
    
     
    }

**15. What is Pact (contract testing)?**

??? success "Reveal answer"
    A framework for consumer-driven contract testing between microservices. The consumer defines 
    what it expects from the provider; the provider verifies it can meet those expectations without a 
    running environment.

**16. What is Terraform count vs for_each?**

??? success "Reveal answer"
    count creates N identical resources by index. for_each creates one resource per map key or set 
    element — resources have stable identifiers based on keys, not index positions. 
    Prefer for_each for most cases.

**17. What is terraform output?**

??? success "Reveal answer"
    Displays output values defined in outputs.tf. Used to extract resource attributes (IP addresses, 
    ARNs) after apply. 
    terraform output instance_public_ip 
    terraform output -json # Machine-readable format

**18. What is terraform workspace?**

??? success "Reveal answer"
    Manages multiple state files from the same configuration. Use for simple multi-environment 
    setups. 
    terraform workspace new staging 
    terraform workspace select production 
    
     
    terraform workspace list

**19. What is Terratest?**

??? success "Reveal answer"
    A Go library for writing automated tests for Terraform modules. Deploys real infrastructure, runs 
    assertions, then destroys it. The gold standard for infrastructure testing. 
     
     
    
     
    Questions)

**20. What is a Terraform backend?**

??? success "Reveal answer"
    Defines where and how state is stored and operations are performed. Backends: S3, GCS, Azure 
    Blob (remote state), Terraform Cloud, local (default). Remote backends enable team 
    collaboration.

**21. What is checkov for Terraform?**

??? success "Reveal answer"
    A static analysis tool that scans Terraform, CloudFormation, and Kubernetes manifests for security 
    misconfigurations and compliance violations. 
    checkov -d terraform/ --framework terraform

**22. What is terraform apply -target?**

??? success "Reveal answer"
    Applies changes only to a specific resource and its dependencies. Use cautiously — can cause 
    state drift if dependencies aren't considered. 
    terraform apply -target=aws_instance.web_server

**23. What is the templatefile() function?**

??? success "Reveal answer"
    Renders a template file with variable substitution. 
    user_data = templatefile("${path.module}/user_data.sh.tpl", { 
     app_name = var.app_name 
     db_host = aws_db_instance.main.endpoint 
    })

**24. What is the lineinfile module?**

??? success "Reveal answer"
    Ensures a specific line is present or absent in a file. Uses regex to find the line. 
    - lineinfile: 
     path: /etc/ssh/sshd_config 
     regexp: '^#MaxAuthTries' 
     line: 'MaxAuthTries 3'

**25. What is Terragrunt?**

??? success "Reveal answer"
    A thin wrapper around Terraform that adds DRY configurations, remote state management, and 
    module dependency management. Used in large multi-account, multi-region setups.

**26. What is the copy module vs synchronize?**

??? success "Reveal answer"
    copy transfers files via SSH — suitable for small files. synchronize uses rsync — much faster for 
    large files or directories. synchronize requires rsync on both ends.

**27. What are Terraform local values?**

??? success "Reveal answer"
    Named expressions that can be reused within a module. 
    locals { 
     common_tags = { 
     Environment = var.environment 
     ManagedBy = "Terraform" 
     Team = "platform" 
     } 
    }

**28. What is a Terraform module source?**

??? success "Reveal answer"
    Where a module is loaded from: local path (./modules/vpc), Terraform Registry 
    (hashicorp/vpc/aws), Git (git::https://github.com/org/modules.git//vpc?ref=v1.2.0).

**29. What is Atlantis?**

??? success "Reveal answer"
    An open-source Terraform pull request automation tool. Runs terraform plan on PR open 
    and terraform apply on PR merge. Provides PR comments with plan output.

**30. What is terraform.tfvars?**

??? success "Reveal answer"
    A file that automatically populates variable values. Avoid committing this file if it contains 
    sensitive values. Use terraform.tfvars.example as a template.

**31. What is a null_resource in Terraform?**

??? success "Reveal answer"
    A resource that does nothing by default but can trigger local-exec or remote-exec provisioners. 
    Used for running scripts as part of the Terraform workflow.

**32. What is a Terraform provider?**

??? success "Reveal answer"
    A plugin that interacts with a cloud platform or service API (AWS, Azure, GCP, Kubernetes, 
    GitHub). Providers define available resources and data sources.

## Scenarios and troubleshooting

**33. How do you structure Terraform code for a large production environment with multiple environments?**

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

**34. — apply failed halfway through. How do you recover and ; ing environment back to a consistent state?**

??? success "Reveal answer"
    + Check the error and identify the failed resource. oa ee
    . e
    + Run sterreforns state list” to see what is actually created. * Ability to a aa vi
    ~9 + Run “terraform plan* to understand the current state vs desired state. ® Risk aware: = od
    ® + Fix the issue and re-run “terraform apply”. = 9 apis
    f : yay ee ee
    + If needed, use ~target carefully for specific resources (last resort). — Fes’
    + Verify the infrastructure and test before preceeding. eat Ge aided
    @

## Practice questions

**35. How do you handle Terraform state management and prevent state corruption in a team environment?**

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

**36. How do you handle disasters and ensure business tinuity:?**

??? success "Reveal answer"
    + Define RPO (Recovery Point Objective) and RTO (Recovery Time Objective). [4 RPO/RTO understanding (pam REGION) (DR _RESION
    oe i
    -9 + Automated backups and regular restores. + Backup & restore strategy | | Replication | \
    + Multi-AZ for high availability, # DR planning a ~ G oaeager | OBE!
    ~» + Grose-region backups / replication. + Automation & Tat usage Nee ey Mi }
    + Infrastructure as Code for quick rebuild. + Testing & documentation + }
    + Documented runbooks & regular DR drills. La Failover when required ——-— J
    -@
    ®

**37. How do you manage cloud infrastructure with Terraform?**

??? success "Reveal answer"
    I define infrastructure in .tf configuration files describing the desired resource state, run terraform init to set up the
    working directory and download providers, terraform plan to preview exactly what will change, and terraform apply to
    provision it. Updates are just changing the config and running apply again, and terraform destroy tears resources
    down cleanly when they're no longer needed.

**38. How do you handle versioning in Infrastructure as Code?**

??? success "Reveal answer"
    I store all IaC files in Git, use meaningful commit messages and tags to mark meaningful changes and versions, use
    release branches or tags to manage configuration differences across environments, and integrate that versioned IaC
    with CI/CD pipelines so testing, deployment, and rollback are automated based on the versioned configuration rather
    than manual application.

**39. Terraform plan shows a resource will be destroyed unexpectedly. What do you do?**

??? success "Reveal answer"
    1. Read the plan carefully — understand why it's being destroyed. 2) Check if it's a force 
    replace due to immutable field change. 3) Use terraform state mv if it's a rename. 4) 
    Check lifecycle.create_before_destroy. 5) Never apply without understanding the 
    cause.

**40. How do you structure Terraform code for c?**

??? success "Reveal answer"
    - C . : ve 2
    5 heck cont = =
    et tainer healt , | 7 .
    + Cheel containe: rT i 7
    Py k doc! ion insi : ! | |
    -8 Verify resource * docker har Fes des pace = : | z
    é tainer: : , 3
    Exec ae amt ‘abel pect < ker log cement — = =.
    2 2 to aor ? =

## Real interview prompts

Additional questions reported from real DevOps / SRE interviews. Company names are omitted — practise these out loud without notes.

- I have created an EC2 instance through Terraform. I don't have a backup of the Terraform state file, it is not in the remote state and locally not available. Now when I do apply, what can I do?
- Could you elaborate your experience with automating and optimizing the deployment over large infrastructure using AWS and other tools like Terraform and Ansible from your previous roles?
- 2 Instances are created using terraform. Statefile is located locally and also in remote backend(S3). If a user deletes 1 instance what would happen? How would you handle this?
- Question : Set up the nodes and everything. what do you write inside a terraform code basically now what will be inside your provider file provided ATF in your main dotf?
- For example, if someone modifies a security group in Terraform and opens it to 0.0.0.0/0, what mechanisms can we use in Terraform to stop such changes from being applied?
- In Terraform, how would you create multiple EC2 instances, each with different configurations (for example, different instance types, AMIs, tags, or volumes)?
- Difference between Iam users.. GitHub Oidc role and terraform io role.. which is secured and when to use use GitHub Oidc and when to use terraform io role?
- You have defined a multi-region Terraform configuration (region1, region2, region3). If you create an EC2 instance, in which region will it be deployed?
- Suppose you have created an EC2 instance by logging into the AWS console. And now you would like to manage it using Terraform. How shall you do it?
- Draw and explain your Terraform repository structure. How do your dev, qa, and prod environments consume shared modules like the VPC module?
- In which file you will define where Terraform state file should be generated and where it has to be maintained (which config file)?
- If we can use terraform import for existing AWS resources which are not created by Terraform, then what is the use of data source?
- How do you safely refactor a Terraform monorepo with hundredsgg of state files into a module-based architecture without downtime?
- How would you manage Terraform when multiple teams deploy to the same AWS account but must not overwrite each other’s resources?
- Two engineers are working on the same Terraform code. How do you prevent conflicts and handle Terraform state locking or drift?
- Question : How do you import a resource into Terraform that was created manually in AWS or GCP? What command would you use?
- Terraform provisioned resource should not delete by deleteing resource configuration in terraform code how can you do it?
- Explain how Terraform handles dependency graphs internally. How can circular dependencies still appear in real projects?
- Describe a production failure caused by terraform apply. What guardrails would you implement to prevent it permanently?
- Say I created an S3 bucket using Terraform and want to modify the bucket name. Is it possible? How would you do this?
- What AWS resources have you created using Terraform and how do you promote a read replica to primary using Terraform?
- [ ] Can you describe a real-time scenario where you used Terraform to provision a highly scalable infrastructure?
- If something is created on the cloud platform and it is not present in Terraform, how will you achieve it?
- What is Terraform and how do you use terraform in your project and what all resources have you provisioned?
- How would you migrate a Terraform backend from local to a remote backend like S3 with DynamoDB locking?

## Related

- Course: [Terraform](../terraform/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
