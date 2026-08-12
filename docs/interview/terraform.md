---
title: "Terraform Interview Preparation"
description: "39 curated Terraform interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
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

<div class="ra-interview-qa" markdown="1">

## Core concepts

**1. Can you explain the difference between Terraform and Ansible?**

??? success "Reveal answer"
    **In short:** Terraform provisions cloud resources (desired state); Ansible configures machines and apps (procedural convergence).
    
    **Key points**
    - **Terraform** — create VPCs, clusters, databases; tracks state
    - **Ansible** — packages, files, services, app config on existing hosts
    - **Together** — Terraform builds the house; Ansible furnishes it
    - **Overlap** — both can touch cloud APIs; pick one source of truth per object
    
    **Trap**
    - Managing the same resource in both tools — perpetual drift fights

**2. Writedown the few terraform commands and explain each cmd?**

??? success "Reveal answer"
    **In short:** Daily toolkit: init, fmt, validate, plan, apply, destroy — plus state and import for surgery.
    
    **Key points**
    - **init** — providers, modules, backend
    - **plan / apply** — preview then mutate
    - **fmt / validate** — style and syntax before PR
    - **state / import / taint(replace)** — reconcile reality with state
    
    **Try this**
    - `terraform init && terraform plan -out=tfplan`
    - `terraform apply tfplan`
    
    **Trap**
    - Blind `apply` without reading the plan in production

**3. Draw and explain your Terraform repository structure. How do your dev, qa, and prod environments consume shared modules like the VPC module?**

??? success "Reveal answer"
    **In short:** Shared modules in a modules repo/registry; each env (dev/qa/prod) is a thin root that pins module versions.
    
    **Key points**
    - **Layout** — `modules/vpc`, `modules/eks`; roots `envs/dev`, `envs/qa`, `envs/prod`
    - **Pin** — module `source` + `version` (or git ref)
    - **State** — separate state per env (and often per component)
    - **Promote** — same module version through envs; change via PR
    
    **Trap**
    - Copy-pasting the VPC module into each env folder

**4. Terraform state file is corrupted or lost. What are your options?**

??? success "Reveal answer"
    **In short:** Recover from remote backups or rebuild state carefully — never invent a state file by hand.
    
    **Key points**
    - **Versioned backend** — S3 versioning / Azure blob soft-delete is your safety net
    - **Restore** — previous state object; unlock if needed
    - **Rebuild** — `import` critical resources into a new state
    - **Prevent** — remote backend + locking + CI-only apply
    
    **Try this**
    - `aws s3api list-object-versions --bucket tfstate --prefix prod/terraform.tfstate`
    
    **Trap**
    - Checking state into Git and losing the only copy of secrets/serials

**5. What are common Terraform anti- i i-patterns you avoid?**

??? success "Reveal answer"
    **In short:** Avoid snowflake roots, giant blast-radius state, hardcoded credentials, and unpinned modules.
    
    **Key points**
    - **No** — one state for the whole company
    - **No** — `count` indexes that reshuffle on delete
    - **No** — access keys in `*.tf` or CI logs
    - **Yes** — modules, workspaces-or-dirs, policy as code, plan reviews
    
    **Trap**
    - `count` on a list of instances then reordering the list — mass recreate

## Scenarios and troubleshooting

**6. How do you structure Terraform code for a large production environment with multiple environments?**

??? success "Reveal answer"
    **In short:** Split by lifecycle and blast radius: foundations, platform, product — each env with its own state.
    
    **Key points**
    - **Layers** — network / IAM / shared data / app stacks
    - **Envs** — separate directories or pipelines, not one giant workspace free-for-all
    - **Modules** — versioned; roots stay thin
    - **Promotion** — artefact = module version + root config
    
    **Trap**
    - One `terraform apply` that can destroy prod DNS and a sandbox VM together

**7. Describe a production failure caused by terraform apply. What guardrails would you implement to prevent it permanently?**

??? success "Reveal answer"
    **In short:** A bad apply usually skipped plan review or lacked policy — fix with mandatory plans, approvals, and guardrails.
    
    **Key points**
    - **CI plan on PR** — humans review destroy/replace lines
    - **OPA/Sentinel/Checkov** — block public buckets, open SG, missing tags
    - **Separate states** — limit blast radius
    - **Break-glass** — audited emergency path, not disabled CI
    
    **Trap**
    - Local apply with admin keys 'just this once'

**8. How to enable Debug logs in Terraform?**

??? success "Reveal answer"
    **In short:** Raise Terraform log verbosity with `TF_LOG` (and optional `TF_LOG_PATH`) for provider/HTTP traces.
    
    **Key points**
    - **Levels** — `TF_LOG=INFO` or `DEBUG` (TRACE is very noisy)
    - **File** — `TF_LOG_PATH=./terraform.log`
    - **Provider logs** — some providers honour their own env vars
    - **Sanitize** — logs can contain secrets; do not paste freely
    
    **Try this**
    - `TF_LOG=DEBUG TF_LOG_PATH=./tf.debug.log terraform plan`
    
    **Trap**
    - Leaving `TF_LOG=TRACE` on in shared CI — credential leakage

**9. Say I created an S3 bucket using Terraform and want to modify the bucket name. Is it possible? How would you do this?**

??? success "Reveal answer"
    **In short:** S3 bucket names are create-time force-new — renaming in place means new bucket + migrate data + update refs.
    
    **Key points**
    - **Plan will show** — destroy/create (or replace)
    - **Data** — replicate/sync objects before cutover
    - **Refs** — apps, policies, CloudFront origins
    - **Prefer** — name prefixes that never need rename
    
    **Trap**
    - Letting Terraform destroy the old bucket before data is copied

**10. 2 Instances are created using terraform. Statefile is located locally and also in remote backend(S3). If a user deletes 1 instance what would happen? How would you handle this?**

??? success "Reveal answer"
    **In short:** Remote state is authoritative; a local copy is a stale cache — delete in cloud shows as drift on next plan.
    
    **Key points**
    - **If someone deletes an instance outside Terraform** — next plan wants to recreate (or you remove from config)
    - **If deleted via Terraform in another clone** — remote state updates; local file is irrelevant
    - **Locking** — DynamoDB/blob lease stops two applies stomping state
    - **Handle** — `plan`, decide recreate vs abandon, never hand-edit state casually
    
    **Try this**
    - `terraform plan` — see the orphaned/missing resource
    
    **Trap**
    - Keeping two backends 'in sync' by copying state files around

**11. What will happen when a IaC managed resource is modified manually, how would you avoid it?**

??? success "Reveal answer"
    **In short:** Manual changes are drift — next apply may overwrite them; prevent with ownership rules and detection.
    
    **Key points**
    - **Detect** — scheduled `plan` / drift tools
    - **Policy** — deny portal writes where possible; break-glass only
    - **Import or code** — either adopt into Terraform or revert
    - **Tags** — `ManagedBy=terraform` for clarity
    
    **Trap**
    - Hotfix in portal that Terraform silently reverts overnight

**12. How would you migrate a Terraform backend from local to a remote backend like S3 with DynamoDB locking?**

??? success "Reveal answer"
    **In short:** Add the remote backend block, run `terraform init -migrate-state`, enable locking — verify before deleting local state.
    
    **Key points**
    - **Backend** — S3 + DynamoDB lock (or Azure blob lease / GCS)
    - **Migrate** — Terraform copies local state remotely
    - **CI** — point all runners at the same backend
    - **Encrypt** — SSE/KMS on the state bucket
    
    **Try this**
    - `terraform init -migrate-state`
    
    **Trap**
    - Migrating twice from different laptops and forking history

**13. What happens if the Terraform state becomes corrupted, and how would you recover from it?**

??? success "Reveal answer"
    **In short:** Corruption recovery = restore a versioned state object, then `plan` until empty of surprises.
    
    **Key points**
    - **Restore** — previous good version from object storage
    - **Unlock** — only if a crashed process left a lock
    - **Import path** — last resort for missing resources
    - **Prevent** — locking, CI-only writes, backups
    
    **Trap**
    - Hand-editing JSON state to 'fix one resource'

**14. In Terraform, how would you create multiple EC2 instances, each with different configurations (for example, different instance types, AMIs, tags, or volumes)?**

??? success "Reveal answer"
    **In short:** Use `for_each` over a map of objects so each instance has a stable key and its own type/AMI/tags.
    
    **Key points**
    - **Map** — `for_each = var.instances` with per-key settings
    - **Avoid count** — deletes shift indices and force replacements
    - **Modules** — wrap instance + volume + IAM into one module
    - **Validate** — variable object schema with `optional()` attrs
    
    **Try this**
    - `for_each = { web = { type = "t3.small" }, api = { type = "t3.medium" } }`
    
    **Trap**
    - `count = length(list)` then sorting the list differently

**15. How would you manage Terraform when multiple teams deploy to the same AWS account but must not overwrite each other’s resources?**

??? success "Reveal answer"
    **In short:** Separate states and naming ownership — teams must not share one root module that can clobber others.
    
    **Key points**
    - **State per team/component** — hard isolation
    - **Account/RG boundaries** — IAM least privilege per pipeline
    - **Naming conventions** — prevent collisions
    - **Code owners** — module ownership in Git
    
    **Trap**
    - One shared state file with everyone as `terraform apply` admin

## Practice questions

**16. How do you handle Terraform state management and prevent state corruption in a team environment?**

??? success "Reveal answer"
    **In short:** Remote state + locking + CI-only apply is how teams avoid corruption and race conditions.
    
    **Key points**
    - **Backend** — shared durable store
    - **Lock** — one apply at a time
    - **PR plans** — visibility before merge
    - **Break-glass** — audited exception process
    
    **Trap**
    - Disabling locks because 'it was stuck'

**17. How do you manage cloud infrastructure with Terraform?**

??? success "Reveal answer"
    **In short:** Define desired infra in HCL modules, review plans, apply via pipeline, observe drift.
    
    **Key points**
    - **Code** — resources + modules + variables
    - **Pipeline** — fmt, validate, plan, apply
    - **Secrets** — env/OIDC to cloud — not in state if avoidable (still protect state)
    - **Docs** — README with blast radius and owners
    
    **Trap**
    - Laptop-as-prod for applies

**18. How do you safely refactor a Terraform monorepo with hundredsgg of state files into a module-based architecture without downtime?**

??? success "Reveal answer"
    **In short:** Refactor with `moved` blocks / state mv, small PRs, and no resource recreation unless planned.
    
    **Key points**
    - **Address moves** — `moved` blocks or `terraform state mv` without destroy
    - **Extract modules** — one component at a time
    - **Plan must be empty** of unexpected replaces
    - **Canaries** — non-prod first
    
    **Trap**
    - Big-bang rewrite that recreates databases

**19. How do you handle versioning in Infrastructure as Code?**

??? success "Reveal answer"
    **In short:** Pin provider and module versions; tag releases; promote the same versions through environments.
    
    **Key points**
    - **required_providers** — version constraints
    - **Module versions** — registry semver or git tags
    - **Lock file** — commit `.terraform.lock.hcl`
    - **Upgrade PRs** — deliberate, tested bumps
    
    **Trap**
    - `version = ">= 1.0"` with no upper bound on a critical provider

**20. If something is created on the cloud platform and it is not present in Terraform, how will you achieve it?**

??? success "Reveal answer"
    **In short:** Import the resource into state (`terraform import` / import blocks) or rewrite config and adopt it.
    
    **Key points**
    - **Write matching config** first
    - **Import** — bind real ID to address
    - **Plan** — should show no change (or only tags)
    - **Then** — manage lifecycle normally
    
    **Try this**
    - `terraform import aws_s3_bucket.logs my-bucket-name`
    
    **Trap**
    - Importing without config — next apply wants to destroy unknowns

**21. You need to create 50 instances in one go. How will you create them in Terraform?**

??? success "Reveal answer"
    **In short:** Create fifty instances with `for_each` (or a module) over a map — not fifty copy-pasted resources.
    
    **Key points**
    - **for_each** — stable keys such as `i-001` or names
    - **Module** — instance + disk + SG rules as one unit
    - **Autoscaling** — prefer ASG/MIG when identical cattle
    - **Limits** — account quotas and API rate limits
    
    **Trap**
    - Fifty individual resources named ec2_1 through ec2_50

**22. How do you handle multiple environments in Terraform?**

??? success "Reveal answer"
    **In short:** One module, many roots (or sparse workspaces): separate state and tfvars per environment.
    
    **Key points**
    - **dirs** — `envs/dev|qa|prod` (clearer than many workspaces)
    - **tfvars** — size, counts, SKUs per env
    - **Backends** — key prefixes per env
    - **Promotion** — same module version everywhere
    
    **Trap**
    - One workspace switching with human memory as the control plane

**23. How do you call a module from root module?**

??? success "Reveal answer"
    **In short:** Call a module with a `module` block: set `source`, pin `version`, pass inputs, read outputs.
    
    **Key points**
    - **Block** — `module "vpc" { source = "app.terraform.io/org/vpc" version = "1.2.3" }`
    - **Inputs** — variables; outputs via `module.vpc.subnet_ids`
    - **Relative source** — `../modules/vpc` in monorepos
    - **Registry** — private module registry at scale
    
    **Trap**
    - Unpinned git module source tracking main

**24. How do you ensure particular AMI image is present in AWS account using terraform?**

??? success "Reveal answer"
    **In short:** Use a data source (`aws_ami`) with owners/filters — fail plan if the AMI disappears.
    
    **Key points**
    - **data "aws_ami"** — filter by name, owner, architecture
    - **Pin** — prefer exact AMI id in prod after promotion
    - **Validate** — `lifecycle` / checks if empty
    - **Pipeline** — bake AMIs separately; Terraform consumes the id
    
    **Try this**
    - `data "aws_ami" "this" { most_recent = true; owners = ["amazon"]; filter { name = "name"; values = ["al2023-*"] } }`
    
    **Trap**
    - Always resolving `latest` AMI in prod apply — surprise replacements

**25. How will you connect your terraform environment from aws and implement CI/CD?**

??? success "Reveal answer"
    **In short:** Authenticate CI with OIDC/roles; pipeline runs fmt/validate/plan/apply with remote state.
    
    **Key points**
    - **OIDC** — GitHub Actions / Azure DevOps / GitLab to cloud roles
    - **Plan on PR** — apply on main with approvals
    - **Backend config** — injected per env
    - **No long-lived access keys** in repo variables if OIDC exists
    
    **Trap**
    - Static AWS keys in pipeline variables shared across repos

**26. How will you write terraform module for EKS?**

??? success "Reveal answer"
    **In short:** EKS module wraps cluster, node groups/Fargate profiles, IAM, and add-on plumbing — keep networking separate.
    
    **Key points**
    - **Inputs** — subnet IDs, version, node sizing, encryption
    - **IAM** — cluster and node roles; IRSA/Pod Identity later
    - **Add-ons** — vpc-cni, core-dns, kube-proxy as code
    - **Outputs** — endpoint, CA, OIDC issuer for IRSA
    
    **Trap**
    - Putting VPC + EKS + apps in one state with a two-hour blast radius

**27. How do you import a resource into Terraform that was created manually in AWS or GCP? What command would you use?**

??? success "Reveal answer"
    **In short:** `terraform import` (or an `import` block) binds an existing cloud ID to a resource address.
    
    **Key points**
    - **Write config** that matches reality
    - **Import** — `terraform import ADDR ID`
    - **Modern** — `import` blocks in config, then plan
    - **Verify** — plan with no unexpected destroys
    
    **Try this**
    - `terraform import aws_instance.web i-0123456789abcdef0`
    
    **Trap**
    - Guessing the import ID format — always check provider docs

**28. How do you manage Terraform state file?**

??? success "Reveal answer"
    **In short:** State is the mapping of config to real IDs — store remotely, lock it, restrict who can read it.
    
    **Key points**
    - **Remote backend** — S3/Azure/GCS/Terraform Cloud
    - **Locking** — prevent concurrent writes
    - **Secrets** — state may contain sensitive values; encrypt + IAM
    - **Operations** — `state list/show/mv/rm` for surgery
    
    **Trap**
    - Emailing `terraform.tfstate` to a colleague

**29. How do you manage the state file in terraform and where do you store it?**

??? success "Reveal answer"
    **In short:** Store state in a remote backend with encryption, versioning, and IAM — never only on a laptop.
    
    **Key points**
    - **S3 + DynamoDB** — common AWS pattern
    - **Azure Storage** — blob + lease lock
    - **TFC/HCP Terraform** — managed state and runs
    - **Backup** — object versioning is mandatory
    
    **Trap**
    - Local state on a shared jump box NFS mount

**30. How will you refer the output of vnet module based subnetid as an input to the VM module?**

??? success "Reveal answer"
    **In short:** Pass module outputs as inputs: `subnet_id = module.vnet.subnet_ids["app"]` into the VM module.
    
    **Key points**
    - **Outputs** — export from VNet module
    - **Inputs** — VM module variable `subnet_id`
    - **Wire** — root module connects them
    - **Sensitive** — mark outputs when needed
    
    **Try this**
    - `subnet_id = module.vnet.subnet_ids["app"]`
    
    **Trap**
    - Hardcoding subnet IDs copied from the portal

**31. Two engineers are working on the same Terraform code. How do you prevent conflicts and handle Terraform state locking or drift?**

??? success "Reveal answer"
    **In short:** Remote locking serialises applies; Git branches + PR plans prevent code conflicts; drift needs process.
    
    **Key points**
    - **State lock** — second apply waits or errors
    - **Code** — small PRs; avoid dual long-lived feature applies
    - **Drift** — agree: Terraform wins or import the change
    - **Communication** — announce prod applies
    
    **Trap**
    - Force-unlocking while a colleague's apply is still running

**32. How do you set up infrastructure for deploying ML models using Terraform?**

??? success "Reveal answer"
    **In short:** ML infra as code: storage, training compute (GPU node pools / Vertex / SageMaker), registries, and networking.
    
    **Key points**
    - **Data** — buckets/datasets with lifecycle and encryption
    - **Train/serve** — GPU node groups, endpoints, feature stores as needed
    - **Identity** — least-privilege roles for pipelines and runtimes
    - **Cost** — schedules/autoscaling; idle GPU is expensive
    
    **Trap**
    - Always-on GPU nodes with no scale-to-zero path

**33. How will you implement multi region Terraform code?**

??? success "Reveal answer"
    **In short:** Multi-region = module reused with region provider aliases and clear failover data ownership.
    
    **Key points**
    - **provider aliases** — `provider "aws" { alias = "eu" }`
    - **Module twice** — `providers = { aws = aws.eu }`
    - **State** — often split per region to limit blast radius
    - **Global** — DNS/CDN outside regional stacks
    
    **Trap**
    - One apply that must succeed in three regions or rolls nothing back cleanly

**34. What AWS resources have you created using Terraform and how do you promote a read replica to primary using Terraform?**

??? success "Reveal answer"
    **In short:** Common resources: VPC, IAM, EKS/ECS, RDS, S3; promoting a replica is a careful failover, not a casual in-place tweak.
    
    **Key points**
    - **Day-to-day** — networks, compute, data, IAM via modules
    - **Replica promote** — usually external failover; then update Terraform to match new primary
    - **State** — may need `import` / address changes after promote
    - **Practice** — rehearse in non-prod
    
    **Trap**
    - Terraform recreate of a promoted DB because IDs diverged from state

**35. Which components or resources are required to create a 3-tier architecture using Terraform?**

??? success "Reveal answer"
    **In short:** Three-tier needs network tiers, compute, data, load balancing, and IAM/secrets — all as modules.
    
    **Key points**
    - **Network** — VPC, public/private subnets, NAT, routes
    - **App** — ASG/ECS/EKS + ALB/NLB
    - **Data** — RDS/ElastiCache in private subnets
    - **Security** — SG/NACL, IAM, KMS, secrets
    
    **Trap**
    - Putting the database in a public subnet for 'easier debugging'

**36. How do you scale a Terraform pipeline that takes 25+ mins?**

??? success "Reveal answer"
    **In short:** Speed up long plans by splitting state, targeted stacks, provider caching, and parallel CI — not by skipping plan.
    
    **Key points**
    - **Split stacks** — smaller graphs plan faster
    - **Refresh control** — careful `-refresh=false` only when safe
    - **Module cache / plugin cache** — speed CI init
    - **Parallelism** — `-parallelism` tune; more stacks in parallel jobs
    
    **Trap**
    - Permanent `-target` applies as the normal workflow

**37. How do you export Azure resources into Terraform code?**

??? success "Reveal answer"
    **In short:** Export Azure into HCL with Azure Export for Terraform / former aztfexport — then clean and import.
    
    **Key points**
    - **Tooling** — Azure Export for Terraform generates config + mapping
    - **Clean** — modules, naming, drop noise
    - **State** — import or use generated mapping
    - **Verify** — empty plan before trust
    
    **Try this**
    - `aztfexport resource -n demo /subscriptions/SUB/resourceGroups/RG`
    
    **Trap**
    - Checking in generated code with secrets still inline

**38. How do you enforce Azure Policies (like tag or location restrictions) using Terraform at scale?**

??? success "Reveal answer"
    **In short:** Define Azure Policy (or initiatives) in Terraform and assign at management group scale.
    
    **Key points**
    - **Resources** — `azurerm_policy_definition` / `assignment`
    - **Scope** — management groups for org-wide tags/locations
    - **Effects** — audit then deny once stable
    - **Exemptions** — time-boxed and reviewed
    
    **Trap**
    - Deny policies without an exemption process — shadow IT explodes

**39. How do you implement state locking in terraform?**

??? success "Reveal answer"
    **In short:** State locking is a backend feature — DynamoDB for S3, blob leases for Azure, or Terraform Cloud runs.
    
    **Key points**
    - **Why** — stops concurrent writers corrupting state
    - **AWS** — `dynamodb_table` in S3 backend config
    - **Azure/GCP** — native leases/locks
    - **Stuck lock** — verify no runner alive before unlock
    
    **Try this**
    - `backend "s3" { bucket = "tfstate"; key = "prod/app.tfstate"; dynamodb_table = "tf-locks" }`
    
    **Trap**
    - Force-unlock as a habit instead of finding the zombie runner

## Related
- Course: [Terraform](../terraform/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
