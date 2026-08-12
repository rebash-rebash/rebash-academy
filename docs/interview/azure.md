---
title: "Azure Interview Preparation"
description: "34 curated Azure interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: azure
tags:
  - interview
  - azure
comments: false
---

{% raw %}
# Azure Interview Preparation

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

**1. What is the purpose of Azure Monitor, and how does it work with Azure DevOps?**

??? success "Reveal answer"
    **In short:** Azure Monitor is the observability plane; DevOps pipelines emit telemetry and can gate releases on it.
    
    **Key points**
    - **Collect** — metrics, App Insights, Log Analytics
    - **Alert** — action groups to email, ITSM, webhooks
    - **DevOps** — release gates query Monitor / App Insights before promote
    - **Correlate** — deployment markers with error/latency spikes
    
    **Try this**
    - `az monitor metrics list --resource <id> --metric-names "Percentage CPU"`
    
    **Trap**
    - Alerting only on CPU and missing request failures

**2. What is the networking you are using in AKS?**

??? success "Reveal answer"
    **In short:** AKS networking is Azure CNI or CNI Overlay, plus NSGs, egress control, and an ingress choice.
    
    **Key points**
    - **CNI / Overlay** — Pod IPs in the VNet vs overlay to save addresses
    - **Egress** — NAT Gateway or firewall/NVA via UDR
    - **Ingress** — AGIC, nginx, or Gateway patterns
    - **Private cluster** — private API server; reach via VPN/bastion/peering
    
    **Try this**
    - `az aks show -g RG -n CLUSTER --query networkProfile`
    
    **Trap**
    - Azure CNI without enough subnet IPs — scale-out stalls

**3. Difference between stakeholder and admin in azure devops?**

??? success "Reveal answer"
    **In short:** Stakeholder is mostly boards visibility; Project Admin owns project configuration and permissions.
    
    **Key points**
    - **Stakeholder** — limited free access; not a full engineer licence
    - **Project Administrators** — teams, repos, pipeline permissions, settings
    - **Org Admin** — broader org process, billing, extensions
    - **Practice** — least privilege; Admin is not a default developer role
    
    **Trap**
    - Everyone is Project Admin for convenience

**4. What is azure board, what are the things inside it?**

??? success "Reveal answer"
    **In short:** Azure Boards tracks work — epics, features, stories, bugs, sprints, and dashboards.
    
    **Key points**
    - **Backlogs** — portfolio and product hierarchy
    - **Sprints** — iterations, capacity, task boards
    - **Queries** — flow, debt, SLA views
    - **Links** — commits, PRs, and pipelines on work items
    
    **Trap**
    - Ticket graveyard with no sprint hygiene

**5. What are the different types of azure storage?**

??? success "Reveal answer"
    **In short:** Azure Storage = Blob, Files, Queues, Tables (plus managed disks) — pick by access pattern.
    
    **Key points**
    - **Blob** — objects with hot/cool/archive tiers
    - **Files** — SMB/NFS shares for lift-and-shift
    - **Queues** — durable messaging between tiers
    - **Tables** — simple NoSQL key/value
    - **Disks** — persistent volumes for VMs
    
    **Trap**
    - Using Blob as a POSIX filesystem for mutable shared state

**6. What are the different types of subscriptions in azure?**

??? success "Reveal answer"
    **In short:** Subscriptions are billing and RBAC boundaries — EA/MCA, CSP, PAYG, Dev/Test, Free trial, and similar offers.
    
    **Key points**
    - **Billing** — invoices and quotas live at subscription scope
    - **RBAC** — management group to subscription to resource group
    - **Landing zone** — separate prod and non-prod subscriptions
    - **Governance** — Azure Policy at management group level
    
    **Trap**
    - One shared subscription for every workload

**7. What is Infrastructure as Code (IaC) in Azure DevOps?**

??? success "Reveal answer"
    **In short:** IaC in Azure DevOps means Git-reviewed Bicep/ARM/Terraform applied by pipelines — not portal clicks.
    
    **Key points**
    - **Code** — Bicep/ARM/Terraform in repos
    - **Pipeline** — validate/plan on PR; apply with approvals
    - **State** — remote Terraform backend or ARM deployment history
    - **Drift** — detect with plan/what-if
    
    **Trap**
    - Portal change that the next apply silently reverts

**8. What is the significance of using Personal Access Tokens (PAT) in Azure DevOps?**

??? success "Reveal answer"
    **In short:** PATs are personal bearer tokens for Git and APIs — treat them like passwords with short expiry.
    
    **Key points**
    - **Scopes** — least privilege only
    - **Expiry** — short-lived; rotate on a calendar
    - **Prefer** — OAuth, service principals, managed identity when possible
    - **Storage** — pipeline secret store, never the YAML file
    
    **Trap**
    - Org-wide full-access PAT committed to a repo

**9. What are Azure DevOps Extensions, and how do you use them?**

??? success "Reveal answer"
    **In short:** Extensions add Marketplace tasks and hubs; install at org level, then use in projects.
    
    **Key points**
    - **Install** — Organisation settings / Marketplace
    - **Pipeline tasks** — custom steps from trusted publishers
    - **Govern** — approve publishers; pin versions
    - **Build your own** — when you need a controlled custom task
    
    **Trap**
    - Random Marketplace tasks with broad OAuth scopes

**10. What is CI/CD, and how does Azure DevOps support it?**

??? success "Reveal answer"
    **In short:** CI builds and tests every change; CD ships artefacts — Azure Pipelines runs both.
    
    **Key points**
    - **CI** — restore, build, test, publish artefacts/images
    - **CD** — Dev to QA to Prod with approvals and gates
    - **Agents** — Microsoft-hosted or self-hosted pools
    - **Targets** — ACR, AKS, App Service, Functions
    
    **Trap**
    - CD rebuilding from a moving branch instead of a CI artefact

**11. What are Azure DevOps Service Hooks?**

??? success "Reveal answer"
    **In short:** Service Hooks send DevOps events to external systems over webhooks.
    
    **Key points**
    - **Triggers** — builds, git pushes, work item changes, releases
    - **Consumers** — Teams/Slack, Functions, ITSM, custom APIs
    - **Auth** — shared secrets / signed payloads
    - **Ops** — monitor failed deliveries
    
    **Trap**
    - Chatty work-item hooks that flood your chatbot

**12. What is a Release Gate in Azure DevOps?**

??? success "Reveal answer"
    **In short:** A release gate is an automated pass/fail check before a stage continues.
    
    **Key points**
    - **Examples** — Azure Monitor alerts, REST checks, Azure Functions
    - **Sampling** — delay and retry windows before fail
    - **Pair** — with human approvals on production
    - **Purpose** — stop bad builds that approvals alone miss
    
    **Trap**
    - Gates that always pass because the query is wrong

**13. What are the key components of Azure DevOps?**

??? success "Reveal answer"
    **In short:** Azure DevOps components: Boards, Repos, Pipelines, Test Plans, Artifacts.
    
    **Key points**
    - **Boards** — agile planning
    - **Repos** — Git hosting
    - **Pipelines** — CI/CD
    - **Artifacts** — NuGet/npm/Maven/universal packages
    - **Test Plans** — manual and exploratory testing
    
    **Trap**
    - No retention policy on Artifacts — storage grows forever

**14. What is the difference between Classic and YAML pipelines in Azure DevOps?**

??? success "Reveal answer"
    **In short:** YAML pipelines live in Git and are reviewable; Classic is UI-defined and drifts.
    
    **Key points**
    - **YAML** — versioned with the app; templates for reuse
    - **Classic** — click-ops; hard to diff and audit
    - **Multi-stage YAML** — CI and CD in one definition
    - **Migrate** — rebuild Classic as YAML deliberately
    
    **Trap**
    - Prod only in Classic while apps move to YAML

**15. What are the benefits of using Azure DevTest Labs?**

??? success "Reveal answer"
    **In short:** DevTest Labs gives quota-controlled sandbox VMs with schedules and golden images.
    
    **Key points**
    - **Cost** — auto-shutdown and claims
    - **Images** — repeatable lab bases
    - **Policies** — limit SKUs and public IPs
    - **Use** — training, spikes, ephemeral agents
    
    **Trap**
    - Lab VMs with public RDP left on 24/7

**16. What is Azure Monitor Network Insights?**

??? success "Reveal answer"
    **In short:** Network Insights visualises Azure network topology and health inside Azure Monitor.
    
    **Key points**
    - **See** — VNets, gateways, load balancers, connectivity
    - **Diagnose** — VPN/ExpressRoute and drop issues faster
    - **Pair** — Connection Monitor, NSG flow logs, Traffic Analytics
    - **Outcome** — shorter MTTR than raw metrics alone
    
    **Trap**
    - Blaming the network after only looking at VM CPU

**17. What is the purpose of using Approval Gates in Azure DevOps?**

??? success "Reveal answer"
    **In short:** Approval gates are human sign-offs on Environments before a stage deploys.
    
    **Key points**
    - **Change control** — separate duty from the engineer who built it
    - **Timeouts** — auto-reject if nobody acts
    - **Combine** — approvals plus automated health gates
    - **Branch policies** — protect main before the pipeline even runs
    
    **Trap**
    - Self-approving production on a shared account

**18. What is Azure Container Registry (ACR), and how does it integrate with Azure DevOps?**

??? success "Reveal answer"
    **In short:** ACR holds images; Pipelines build/push; AKS pulls with identity or pull secrets.
    
    **Key points**
    - **Tag** — immutable git SHA or digest
    - **Auth** — service connection or managed identity
    - **Scan** — Defender / ACR tasks
    - **Deploy** — pin digest in manifests/Helm
    
    **Trap**
    - Deploying the floating `:latest` tag

**19. What is a build artifact in Azure DevOps?**

??? success "Reveal answer"
    **In short:** A build artefact is the immutable CI output that CD stages consume.
    
    **Key points**
    - **Publish** — pipeline artefacts or an ACR digest
    - **Immutable** — do not rebuild from main at deploy time
    - **Retention** — set policies
    - **Traceability** — artefact links back to commit and work items
    
    **Trap**
    - CD cloning main and rebuilding production bits

## Scenarios and troubleshooting

**20. Write a production-grade Azure Pipeline YAML for a .NET application deployment to AKS. Prepared by Arvind Verma Prepared by Arvind Verma Page 220 of 274 CHAPTER 11: AZURE DEVOPS Page 221 of 274**

??? success "Reveal answer"
    **In short:** Production .NET to AKS YAML: test, publish image digest, deploy with Environment approvals and OIDC.
    
    **Key points**
    - **CI** — restore, test, build image, push to ACR
    - **CD** — Helm/kubectl to AKS pinning digest
    - **Security** — Key Vault secrets; no PAT in YAML
    - **Noise in the question** — PDF page footers are extraction junk, ignore them
    
    **Trap**
    - Pasting subscription keys into the sample pipeline

**21. How do you troubleshoot an application using logs?**

??? success "Reveal answer"
    **In short:** Troubleshoot with App Insights and Log Analytics: symptom, correlation ID, dependencies, then last deploy.
    
    **Key points**
    - **App Insights** — failures, dependencies, exceptions
    - **KQL** — join requests and exceptions
    - **Release** — which pipeline version is live?
    - **Confirm** — error rate and synthetic probe after fix
    
    **Try this**
    - KQL: `requests | where timestamp > ago(1h) | summarize count() by resultCode`
    
    **Trap**
    - Restarting first and wiping forensic evidence

**22. How would you use Azure DevOps REST API to apply a security policy to all repos programmatically?**

??? success "Reveal answer"
    **In short:** Loop the Azure DevOps REST API (or `az devops`) to apply branch policies on every repo.
    
    **Key points**
    - **Auth** — service principal with minimal scopes
    - **Enumerate** — projects and repos
    - **Apply** — required reviewers, build validation, deny force-push
    - **Idempotent** — re-runnable script with per-repo logging
    
    **Trap**
    - Laptop script using an org-wide full PAT

## Practice questions

**23. How can you implement monitoring in Azure DevOps?**

??? success "Reveal answer"
    **In short:** Monitor pipelines and agents as well as the app — failure rate, queue time, flaky tests.
    
    **Key points**
    - **Pipeline analytics** — failed runs and duration
    - **Agents** — disk/CPU on self-hosted pools
    - **Post-deploy** — Azure Monitor / App Insights gates
    - **Dashboards** — deployment frequency and fail rate
    
    **Trap**
    - Green prod dashboards while CI has been red for a week

**24. How do you create and manage Azure DevOps service connections?**

??? success "Reveal answer"
    **In short:** Service connections are reusable project credentials to Azure, Kubernetes, ACR, and Git.
    
    **Key points**
    - **Prefer OIDC** — workload identity federation over long-lived secrets
    - **Scope** — one subscription or resource group when possible
    - **Authorise** — restrict which pipelines may use them
    - **Rotate** — if secret-based, calendar and audit
    
    **Try this**
    - `az devops service-endpoint list --project PROJ -o table`
    
    **Trap**
    - Subscription Owner SP shared by every pipeline

**25. How will you store credentials in azure pipelines?**

??? success "Reveal answer"
    **In short:** Keep credentials in Key Vault or secret pipeline variables — inject at runtime only.
    
    **Key points**
    - **Key Vault tasks / linked variable groups**
    - **OIDC** — pipeline to Azure without stored passwords
    - **Masking** — secret variables; still avoid echo
    - **Scan** — secret scanning and rapid revoke on leak
    
    **Trap**
    - Debugging with `echo` of a secret variable

**26. How will you implement dc/dr in azure – which are the services you will be using it?**

??? success "Reveal answer"
    **In short:** DC/DR uses paired regions, data replication, global routing, and practised failover against RPO/RTO.
    
    **Key points**
    - **Edge** — Front Door or Traffic Manager
    - **Data** — SQL failover groups, Cosmos multi-region, GRS, ASR for VMs
    - **Compute** — redeploy with IaC in the secondary region
    - **Prove** — game-day failover
    
    **Trap**
    - Geo-redundant storage with an app that cannot run cold elsewhere

**27. How do you assess Azure DevOps migration readiness and plan the transition?**

??? success "Reveal answer"
    **In short:** Assess migration by inventorying projects, auth, agents, and custom tasks — then pilot one team.
    
    **Key points**
    - **Discover** — classic releases, custom tasks, service hooks
    - **Identity** — Entra ID, PATs, service principals
    - **Pilot** — one medium project end-to-end
    - **Cutover** — freeze window and read-only archive
    
    **Trap**
    - Big-bang weekend cutover with no Git remote rollback

**28. How do you implement security in Azure DevOps?**

??? success "Reveal answer"
    **In short:** Secure the factory: branch policies, least-privilege RBAC, secret hygiene, restricted pipelines.
    
    **Key points**
    - **Repos** — reviews, deny force-push on main
    - **Pipelines** — environment approvals; locked templates
    - **Secrets** — Key Vault + OIDC
    - **Audit** — remove stale users and PATs
    
    **Trap**
    - Fork PRs running privileged pipelines with secrets

**29. How do you automate tests in Azure DevOps?**

??? success "Reveal answer"
    **In short:** Automate tests in pipeline stages — unit in CI, integration in test env, smoke after prod deploy.
    
    **Key points**
    - **Unit/integration** — fail the build on regressions
    - **UI/API** — Playwright/Postman in CD
    - **Publish results** — visibility and flaky tracking
    - **Manual** — Test Plans only where regulation needs it
    
    **Trap**
    - Skipping tests to save pipeline minutes

**30. How do you manage secrets in Azure DevOps?**

??? success "Reveal answer"
    **In short:** Secrets belong in Key Vault (or secret variable groups), fetched at runtime with managed identity/OIDC.
    
    **Key points**
    - **Link** — variable groups to Key Vault
    - **ACL** — who can read secrets
    - **Rotate** — new versions; recycle apps/pods
    - **Avoid** — plaintext YAML and long-lived secure files
    
    **Trap**
    - Every engineer is Key Vault Secrets Officer on prod

**31. How do you handle environment variables in Azure DevOps Pipelines?**

??? success "Reveal answer"
    **In short:** Use pipeline variables and environment-scoped groups; mark secrets; pass template parameters explicitly.
    
    **Key points**
    - **Plain vs secret** — mark secrets so logs mask them
    - **Groups** — different groups per environment
    - **Templates** — explicit parameters, not mystery globals
    - **Runtime env:** — map into the process for the app
    
    **Trap**
    - One variable group shared by prod and personal sandboxes

**32. Why Dynamic blocks are used in tf and write the skeleton for an azure resource using dynamic block?**

??? success "Reveal answer"
    **In short:** Dynamic blocks build repeating nested Terraform blocks from a list or map — ideal for Azure IP restrictions and similar.
    
    **Key points**
    - **When** — optional or repeating nested blocks
    - **Shape** — `for_each` over `var.allow_ips` inside `dynamic "ip_restriction"`
    - **Readability** — prefer a normal block when there is only one
    - **Validate** — `terraform validate` after clever dynamics
    
    **Trap**
    - Five-level nested dynamics nobody can review

**33. How mysql will interact with azure key vault and it should happen thru privately and should not go anything on public?**

??? success "Reveal answer"
    **In short:** MySQL talks to Key Vault via managed identity over private endpoints — public network access off on both.
    
    **Key points**
    - **Private Endpoint + private DNS** for Key Vault and MySQL
    - **Managed identity** — Secrets User on the vault
    - **Deny public** — firewalls closed
    - **Apps** — fetch secrets at runtime; nothing in Git
    
    **Try this**
    - `az keyvault show -n VAULT --query properties.networkAcls`
    
    **Trap**
    - Key Vault firewall allow `0.0.0.0/0` for the pipeline

**34. How azure key vault is integrated in cicd?**

??? success "Reveal answer"
    **In short:** CI/CD integrates Key Vault with OIDC/service connection and Key Vault tasks — secrets never baked into images.
    
    **Key points**
    - **Auth** — federated credential; get secret only
    - **Tasks** — AzureKeyVault@2 or linked groups
    - **Inject** — env vars or mounted secrets into App Service/AKS
    - **Audit** — Key Vault diagnostics for secret reads
    
    **Trap**
    - Printing Key Vault values in a pipeline script

## Related
- Hub: [Interview Preparation](index.md)
{% endraw %}
