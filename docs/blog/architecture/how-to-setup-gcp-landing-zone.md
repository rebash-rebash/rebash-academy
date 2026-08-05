---
title: "How to set up a GCP landing zone"
description: "Design and implement a Google Cloud landing zone with real production trade-offs — resource hierarchy, Shared VPC, identity, org policies, logging, and interview-ready decisions."
author: Shaik Basha
date: "2026-08-05"
updated: "2026-08-05"
category: architecture
type: architecture-discussion
difficulty: advanced
estimated_reading_time: "18 min"
learning_paths:
  - cloud-architect
  - cloud-engineer
  - devops-engineer
technologies:
  - gcp
  - terraform
skills:
  - landing-zone
  - shared-vpc
  - iam
  - org-policy
series: null
series_part: null
tags:
  - gcp
  - landing-zone
  - architecture
  - shared-vpc
  - interview
related_tutorials: []
related_labs: []
related_projects: []
related_cheatsheets: []
related_certifications:
  - Professional Cloud Architect
featured: true
comments: false
---

# How to set up a GCP landing zone

A **landing zone** (also called a cloud foundation) is the shared baseline every workload inherits on Google Cloud Platform (GCP): organisation structure, identity, networking, logging, and guardrails. Without it, teams invent one-off projects, public IP habits, and IAM exceptions that become expensive to reverse.

This article is for Cloud Architects, Platform Engineers, and interview candidates who need to design — not just click through — a production landing zone. It follows Google’s [landing zone design](https://docs.cloud.google.com/architecture/landing-zones) guidance and focuses on decisions you must defend in design reviews and interviews.

## What you will be able to explain

- Why a landing zone exists and what “good” looks like in the first 90 days
- How to structure Organisation → Folders → Projects for blast-radius control
- When to use Shared VPC host/service projects versus separate VPCs
- How identity federation, organisation policies, and central logging fit together
- Trade-offs interviewers probe: hub-and-spoke depth, multi-landing-zone cases, quota, and ops ownership

## What a GCP landing zone is (and is not)

A landing zone is **not** a single VPC or a Terraform module name. It is the set of **repeatable foundations** that make onboarding a new application boring:

| Foundation | Typical owners | What it enforces |
|------------|----------------|------------------|
| Resource hierarchy | Cloud foundation / platform | Isolation, policy inheritance, billing alignment |
| Identity | Identity / security | Workforce identity, groups, break-glass |
| Networking | Network / platform | Shared VPC, firewalls, hybrid connectivity, DNS |
| Security guardrails | Security / platform | Organisation Policy, SCC, binary auth later |
| Observability | Platform / SRE | Org-level log sinks, metrics, alerting baselines |
| Automation | Platform | Bootstrap projects, CI for infrastructure as code (IaC) |

**Success criterion:** a new application team can request a project (or folder), attach to the right Shared VPC, ship with private Google access and logging, and never touch organisation-wide IAM or default networks.

## Design before you click

Interviewers and real programmes fail when teams jump into the console. Decide these first:

1. **Who owns the foundation?** Platform team with security and networking as stakeholders — not every product team.
2. **How many environments?** At minimum `nonprod` and `prod`. Many organisations add `sandbox` / `sandbox-expire` with weaker guardrails and automatic cleanup.
3. **Who pays?** Billing account strategy and labels (`env`, `cost-centre`, `app`) before the first project explosion.
4. **What must never happen?** Public SSH on VMs, default VPC use, service account keys in Git, org-wide Owner grants.
5. **How do humans authenticate?** Prefer Workforce Identity Federation or Cloud Identity / Google Workspace groups — avoid long-lived user keys.

Write a one-page architecture decision record (ADR) for hierarchy and network topology. Future auditors will ask why folders look the way they do.

## Resource hierarchy that survives growth

GCP’s hierarchy is: **Organisation → Folders → Projects → Resources**. Prefer **one organisation** unless you have a hard legal or M&A reason for more ([resource hierarchy guidance](https://cloud.google.com/architecture/landing-zones/decide-resource-hierarchy)).

### Recommended starter shape

```text
Organisation
├── Bootstrap                 # seed projects, Terraform state, CI runners for IaC
├── Common                    # security, logging, monitoring, secrets (shared)
├── Networking                # Shared VPC host projects per environment
├── Non-production
│   ├── Shared services
│   └── App folders / projects
└── Production
    ├── Shared services
    └── App folders / projects
```

**Design considerations:**

- Put **Bootstrap** directly under the organisation. It holds the automation that creates everything else — treat it as higher trust than app projects.
- Separate **Production** and **Non-production** at folder level so organisation policies and IAM can differ without hunting project by project.
- Prefer folders for **business unit or domain**, then environment — or environment first if compliance requires a hard prod wall. Document the choice; either can work.
- Keep **depth shallow** (about three to four levels). Deep trees look neat in slides and painful in IAM and Shared VPC admin boundaries.

### Project taxonomy

Create foundational projects early:

| Project role | Example ID pattern | Purpose |
|--------------|--------------------|---------|
| Bootstrap / seed | `prj-seed-bootstrap` | Terraform state bucket, pipeline service accounts |
| Logging | `prj-c-logging` | Org sinks destination (BigQuery / Cloud Storage / Pub/Sub) |
| Security | `prj-c-security` | Security Command Center exports, forensics |
| Network host (prod) | `prj-net-prod` | Shared VPC host for production |
| Network host (nonprod) | `prj-net-nonprod` | Shared VPC host for non-production |
| App service projects | `prj-app-<name>-prod` | Workloads only — attach as Shared VPC service projects |

Delete **default networks** in every project. Never use the default VPC for anything that matters.

## Networking: Shared VPC as the default pattern

For most enterprises, [Shared VPC](https://cloud.google.com/vpc/docs/shared-vpc) is the right default: a **host project** owns the VPC and subnets; **service projects** attach and deploy compute into those subnets.

### Topology that matches production

- **One Shared VPC host project per environment** (prod / nonprod), not one mega-host for everything. Different environments get different firewall posture, peering, and admin blast radius ([VPC design best practices](https://docs.cloud.google.com/architecture/best-practices-vpc-design)).
- **Custom mode VPC** with planned CIDR ranges per region and environment. Avoid overlapping ranges if you will peer or connect hybrid networks later.
- **Subnet-level Network User** grants — give application teams access to specific subnets, not the entire host project.
- **Cloud NAT** for egress without public VM IPs; prefer private Google access for APIs.
- **Cloud DNS private zones** for internal names; forward carefully for hybrid.
- **Hybrid:** Dedicated / Partner Interconnect for stable high throughput; Cloud VPN for lighter or temporary links. Plan on-prem routes so you do not hairpin application traffic through the wrong hub.

### When not to share a VPC

Use a **separate VPC / host** when:

- A workload needs a different trust boundary (PCI / regulated island)
- You are approaching **host project quotas** for the aggregate of all attached projects
- Network admin teams must be fully isolated (IAM for `networkAdmin` is project-scoped)

Google also notes that organisations with unusual scalability or compliance needs may run **more than one landing zone**, sharing identity and billing but splitting network and folder policies ([landing zones overview](https://docs.cloud.google.com/architecture/landing-zones)).

## Identity and access

Landing zones fail quietly when identity is an afterthought.

**Principles:**

- Map humans to **groups** (Cloud Identity / Workspace), then grant groups roles on folders and projects — never grant `Owner` to individuals on the organisation.
- Prefer **Workload Identity Federation** for CI/CD and cloud-to-cloud; ban long-lived JSON keys where possible (organisation policy can help).
- Separate **break-glass** accounts (monitored, rare use) from day-to-day admin groups.
- Align Shared VPC roles: Organisation Admin nominates Shared VPC Admins; Shared VPC Admins attach service projects and delegate subnet access ([Shared VPC IAM model](https://cloud.google.com/vpc/docs/shared-vpc)).

**Interview-ready distinction:** IAM answers “who can do what”; Organisation Policy answers “what is allowed in this tree regardless of who asks”.

## Organisation Policy and security baseline

Apply organisation policies early on the **organisation or environment folders**:

| Control | Typical constraint | Why |
|---------|-------------------|-----|
| Disable service account key creation | `constraints/iam.disableServiceAccountKeyCreation` | Stops key sprawl |
| Restrict public IP on VMs | `constraints/compute.vmExternalIpAccess` | Forces NAT / private design |
| Require OS Login | `constraints/compute.requireOsLogin` | Central SSH identity |
| Restrict resource locations | `constraints/gcp.resourceLocations` | Data residency |
| Skip default network creation | `constraints/compute.skipDefaultNetworkCreation` | Stops new default VPCs |

Pair policies with Security Command Center (SCC) at organisation level, VPC Service Controls for sensitive data planes when justified, and a clear exception process (time-bound, ticketed, reviewed).

## Logging, monitoring, and operations

Centralise first; refine later.

1. Create **organisation-level log sinks** to a dedicated logging project (BigQuery for queryable audit, Cloud Storage for cheap long retention, Pub/Sub for SIEM).
2. Sink **Admin Activity** and critical **Data Access** logs; do not rely on project owners remembering sinks.
3. Baseline alerts: billing anomalies, IAM privilege grants at org/folder, firewall changes on Shared VPC hosts, sink failures.
4. Define who gets paged for **network host** incidents versus **app** incidents — Shared VPC concentrates risk.

## Automation and bootstrap order

Manual landing zones drift. Prefer IaC (Terraform / OpenTofu or Google’s enterprise foundations patterns such as Cloud Foundation Fabric-style stages):

Suggested sequence:

1. **Bootstrap** — state bucket, seed project, pipeline identity  
2. **Resource manager** — folders, organisation policies, foundational projects  
3. **Networking** — host projects, Shared VPC, firewalls, DNS, NAT  
4. **Security & logging** — sinks, SCC, baseline alerts  
5. **App onboarding** — project factory that creates service projects, attaches Shared VPC, applies labels and folder placement  

Do not let product teams create random projects under the organisation root.

## Real-time design considerations (checklist)

Use this in design reviews and whiteboard interviews:

| Topic | Question to answer | Common mistake |
|-------|--------------------|----------------|
| Blast radius | What fails if the prod host project is misconfigured? | One Shared VPC for prod + nonprod |
| IP plan | Can we add three regions without renumbering? | Tiny overlapping CIDRs |
| Team autonomy | Can an app team deploy without a network ticket every time? | Granting host project Editor to everyone |
| Hybrid | Where does return traffic land? | Peering spaghetti with no hub ownership |
| Quotas | What happens at 50 service projects on one host? | Ignoring host project quotas |
| Exceptions | How does a temporary public IP get approved? | Silent org policy overrides |
| Cost | Who pays for NAT, Interconnect, and log retention? | Logging project with no budget alert |
| DR | Is DR a second region in the same landing zone or a second foundation? | Copy-paste projects with no policy parity |

## Anti-patterns to reject

- Using the **default VPC** or leaving it in every project  
- Giving developers **Organisation Admin** “just for setup”  
- One flat project for all environments  
- Public IP on every VM instead of Cloud NAT  
- Service account keys checked into repositories  
- Attaching prod and nonprod to the **same** Shared VPC host “to save money”  
- Deep folder trees that mirror the org chart for politics, not blast radius  

## Interview Q&A

**1. What is a GCP landing zone, and why not start with one project?**

??? success "Reveal answer"
    A landing zone is the shared foundation — hierarchy, identity, network, logging, and guardrails — that every workload inherits. A single project cannot isolate environments, centralise network policy, or apply organisation-wide constraints cleanly. You pay later in migration cost, security exceptions, and unclear ownership.

**2. Why prefer Shared VPC over a VPC in every application project?**

??? success "Reveal answer"
    Shared VPC centralises IP management, firewalls, and hybrid connectivity in a host project while letting teams deploy in service projects. You avoid N copies of peering and Interconnect. Grant Network User at subnet scope so teams stay autonomous without owning the whole network.

**3. How would you separate production and non-production?**

??? success "Reveal answer"
    Separate folders under the organisation, separate Shared VPC host projects, different organisation policies where needed, and distinct IAM groups. Prefer not to share a production host project with non-production service projects.

**4. IAM versus Organisation Policy — how do they differ?**

??? success "Reveal answer"
    IAM grants capabilities to principals. Organisation Policy sets constraints on what is allowed for resources in a part of the hierarchy, even for privileged users. You need both: least privilege for people and hard guardrails for the platform.

**5. When would you create more than one landing zone?**

??? success "Reveal answer"
    When a workload class needs a different network or policy model (strong compliance island, extreme scale, or acquired company isolation). You can still share organisation, billing, and identity while splitting network and folder-level controls.

**6. What belongs in the bootstrap folder?**

??? success "Reveal answer"
    The automation that creates the rest of the foundation: Terraform state, pipeline identities, and seed projects. It sits near the organisation root because it is higher trust and must exist before resource manager and networking stages run.

**7. How do you onboard a new application team safely?**

??? success "Reveal answer"
    Use a project factory: create a service project under the right folder, apply labels and budgets, attach it to the correct Shared VPC host, grant subnet-level Network User to the team group, ensure org sinks already cover the project, and deny default network creation via policy.

**8. What operational risk does Shared VPC introduce?**

??? success "Reveal answer"
    Concentrated blast radius: a bad firewall rule or IAM change on the host affects many apps. Mitigate with change control on host projects, separate prod/nonprod hosts, subnet-scoped grants, and monitoring on host-level changes.

## Key takeaways

- Design hierarchy, identity, and network topology on paper before creating projects.
- Prefer environment-separated Shared VPC hosts and subnet-scoped Network User grants.
- Use Organisation Policy for hard “never” rules; use IAM groups for day-to-day access.
- Centralise logging at the organisation; delete default VPCs everywhere.
- Automate bootstrap → resource manager → network → security → project factory.
- In interviews, talk blast radius, quotas, hybrid routing, and exception process — not only product names.

## Related learning

- [Multi-Cloud Landing Zone Patterns](../../architecture-guides/multi-cloud-landing-zone-patterns.md)
- [Cloud Architect learning path](../../learning-paths/cloud-architect/index.md)
- [Google Cloud course hub](../../gcp/index.md)
- [System Design course](../../system-design/index.md) — capacity and trade-off practice that transfers to cloud foundations

## References

- [Landing zone design in Google Cloud](https://docs.cloud.google.com/architecture/landing-zones) — Cloud Architecture Center  
- [Decide a resource hierarchy for your landing zone](https://cloud.google.com/architecture/landing-zones/decide-resource-hierarchy)  
- [Shared VPC](https://cloud.google.com/vpc/docs/shared-vpc)  
- [Best practices and reference architectures for VPC design](https://docs.cloud.google.com/architecture/best-practices-vpc-design)  
- [Organisation Policy Service](https://cloud.google.com/resource-manager/docs/organization-policy/overview)  
