---
title: Google Cloud — Frozen syllabus
description: Canonical frozen syllabus for the Google Cloud course (v1). Do not renumber or rename without an explicit syllabus change.
author: Shaik Basha
category: curriculum
tags:
  - curriculum
  - gcp
  - syllabus
last_updated: "2026-08-04"
status: frozen
version: "1.0"
---

# Google Cloud — Frozen syllabus (v1.0)

**Frozen:** 2026-08-04  
**Status:** Syllabus locked. Implement tutorials against this document. Do not add, remove, rename, or reorder modules without an explicit syllabus revision (bump `version`).

Canonical generation prompt: [`.cursor/prompts/technologies/gcp.md`](../../.cursor/prompts/technologies/gcp.md)  
Course URL prefix: `docs/gcp/`  
Learning paths: `cloud-engineer` · `devops-engineer` · `cloud-architect` · `platform-engineer` · `site-reliability-engineer`

---

## Locked product decisions

| Decision | Freeze |
|----------|--------|
| Module count | **16** modules · **16** tutorials (one tutorial per module) |
| Difficulty | Beginner → Advanced within the track (plain teaching voice) |
| Duration | 12–16 weeks |
| Lab runtime | **Real Google Cloud** preferred (Free Trial / Always Free). Module 1 creates a **budget alert** before later compute labs. Cleanup is mandatory every lab |
| Fallback | If billing or organisation policy blocks a create: document inspect / dry-run / config-only proof so the tutorial still completes |
| Cloud Run | Primary home in **Module 8 (Serverless)**. Module 7 = Google Kubernetes Engine (GKE) + Artifact Registry + when to choose Cloud Run vs GKE |
| IaC (Module 12) | Terraform `google` / `google-beta` provider patterns — not a second full Terraform course |
| Data (Module 9) | Ops-relevant BigQuery, Pub/Sub, Cloud Scheduler — not a full data-engineering track |
| Course nav | Overview (roadmap on page) + Module 1–16 only. No Labs / Quizzes / Projects / Capstone / Cheatsheets / Interview / Certifications / FAQ / Roadmap sidebar hubs |
| Capstone | Embedded in **Module 15** lab (landing-zone sketch). Module 16 = troubleshooting runbook |
| Standalone project / capstone IDs | `gcp-gke-bootstrap` · `gcp-enterprise-platform` (backlog; not course nav) |
| Lab root | `~/rebash-gcp/module-NN` |
| Certifications in v1 | Soft map on Overview only (Cloud Digital Leader, Associate Cloud Engineer, Professional Cloud Architect / DevOps Engineer). No cert hub in course nav |
| Diagrams | Excalidraw under `docs/assets/excalidraw/` |
| AWS parity | Same spine as published AWS course nav; GCP differentiator = Module 9 Data & Analytics (AWS has Reliability as Module 14) |

---

## Positioning

**Title:** Google Cloud for Cloud & DevOps Engineers  
**Promise:** Design, deploy, and operate production workloads on Google Cloud with `gcloud`, Identity and Access Management (IAM), networking, compute, GKE / Cloud Run, Infrastructure as Code (IaC), and ops hygiene.  
**Not in scope:** Vertex AI / MLOps deep dive, full warehouse engineering, Anthos / multi-cloud mesh as required labs.

### Prerequisites

| Required | Nice to have |
|----------|----------------|
| Linux | Docker (before Module 7) |
| Networking | Kubernetes (before Module 7) |
| Git | Terraform (before Module 12) |

### Target roles

Cloud Engineer · DevOps Engineer · Platform Engineer · Site Reliability Engineer (SRE) · DevSecOps Engineer · Cloud Architect · Infrastructure Engineer

---

## Learning roadmap (course Overview)

1. **Foundations (Modules 1–2)** — projects, regions/zones, `gcloud`, cost guardrails, IAM / resource hierarchy  
2. **Network & compute (Modules 3–4)** — Virtual Private Cloud (VPC), Compute Engine  
3. **Data & apps (Modules 5–8)** — storage, databases, GKE / Artifact Registry, serverless  
4. **Data ops & observe (Modules 9–10)** — BigQuery / Pub/Sub lens, monitoring and logging  
5. **Secure & deliver (Modules 11–14)** — security services, Terraform, CI/CD, FinOps  
6. **Operate & triage (Modules 15–16)** — landing zones, troubleshooting under pressure  

---

## Frozen module map

| # | Module title | Tutorial ID | Tutorial title | Lab proof |
|---|--------------|-------------|----------------|-----------|
| 1 | Google Cloud Fundamentals | `gcp/google-cloud-fundamentals-and-global-infrastructure` | Google Cloud Fundamentals and Global Infrastructure | Auth + project set + list regions/zones + **budget alert** |
| 2 | Identity & Access Management | `gcp/iam-identity-access-and-resource-hierarchy` | IAM, Identity Access, and Resource Hierarchy | Service account + role bind + deny-proof |
| 3 | Networking | `gcp/vpc-networking-on-gcp` | VPC Networking on Google Cloud | VPC + subnet + firewall + reachability check |
| 4 | Compute | `gcp/compute-engine-migs-and-load-balancing` | Compute Engine, MIGs, and Load Balancing | VM + startup script + SSH/HTTP prove + **cleanup** |
| 5 | Storage | `gcp/storage-gcs-persistent-disk-and-filestore` | Cloud Storage, Persistent Disk, and Filestore | Bucket + lifecycle + upload/download prove |
| 6 | Databases | `gcp/databases-on-gcp` | Databases on Google Cloud | Cloud SQL (or documented fallback) + connect check |
| 7 | Containers | `gcp/containers-gke-and-artifact-registry` | Containers — GKE and Artifact Registry | Artifact Registry push + small GKE/Autopilot deploy **or** documented alternate |
| 8 | Serverless | `gcp/serverless-on-gcp` | Serverless on Google Cloud | Cloud Run service from container + URL prove |
| 9 | Data & Analytics | `gcp/data-and-analytics-on-gcp` | Data and Analytics on Google Cloud | BigQuery sample query + Pub/Sub topic/subscription |
| 10 | Monitoring & Observability | `gcp/monitoring-and-observability-on-gcp` | Monitoring and Observability on Google Cloud | Metric/uptime alert + log query prove |
| 11 | Security | `gcp/gcp-security-services` | Google Cloud Security Services | Secret Manager secret + IAM grant + read prove |
| 12 | Infrastructure as Code | `gcp/infrastructure-as-code-on-gcp` | Infrastructure as Code on Google Cloud | Terraform apply of VPC/bucket pattern + destroy |
| 13 | CI/CD | `gcp/cicd-on-gcp` | CI/CD on Google Cloud | Cloud Build → Artifact Registry → Cloud Run |
| 14 | Cost Optimisation | `gcp/cost-optimisation-on-gcp` | Cost Optimisation on Google Cloud | Labels + budget review + idle resource hunt |
| 15 | Production GCP | `gcp/production-gcp-landing-zones` | Production GCP Landing Zones | Multi-project / folder sketch + policy + ops runbook |
| 16 | Troubleshooting | `gcp/troubleshooting-gcp` | Troubleshooting Google Cloud | Break/fix triage checklist (IAM, VPC, GKE, Run, cost) |

**Markdown paths:** `docs/gcp/<slug>.md` where `<slug>` is the tutorial ID without the `gcp/` prefix.

---

## Tutorial chain (prerequisites)

```
1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14 → 15 → 16
```

Each tutorial’s `prerequisites` frontmatter points at the previous tutorial ID (Module 1 has Linux / Networking / Git as soft prereqs in prose).

---

## Interview outcomes (end of course)

Learners should defend:

- Project vs folder vs organisation, and why billing lives where it does  
- IAM roles vs service accounts vs Workload Identity Federation  
- Public vs private subnet paths, Cloud NAT, and firewall direction  
- When to choose Compute Engine vs GKE vs Cloud Run  
- How Secret Manager and least privilege stop “keys in Git”  
- Landing-zone shape: Shared VPC sketch, org policies, logging strategy  
- Cost guardrails: budgets, labels, and why cleanup is part of the job  

---

## Delivery conventions

- Topic-first Overview openings (no audience stamp on every page)  
- Teaching pattern: problem → analogy → term → tiny example → interview one-liner → depth → real lab  
- Labs: create → prove → break/fix where useful → **cleanup**  
- Terminal fences: `{.bash .ra-terminal title="Terminal"}`  
- Interview: question outside `??? success "Reveal answer"`  
- British English; explain acronyms on first use  
- Escape template syntax for mkdocs-macros (`{% raw %}`) when needed  
- Cost hygiene callouts on every module that creates billable resources  

---

## Implementation phases (post-freeze)

| Phase | Modules | Outcome |
|-------|---------|---------|
| A | Syllabus freeze, prompt + backlog + curriculum sync, Overview stub note | Structure locked |
| B | 1–4 | Foundations: project, IAM, VPC, Compute Engine + cost hygiene |
| C | 5–8 | Storage → databases → GKE/AR → Cloud Run |
| D | 9–12 | Data ops → monitoring → security → Terraform |
| E | 13–16 | CI/CD → cost → landing zone → troubleshooting; mark course `ready`; update learning paths |

**Phase A:** frozen 2026-08-04.

**Phase B (Modules 1–4):** published 2026-08-04.

**Phase C (Modules 5–8):** published 2026-08-04.

**Phase D (Modules 9–12):** published 2026-08-04.

**Phase E (Modules 13–16):** published 2026-08-04.

**Course status:** complete (v1.0 syllabus fully published).

---

## Out of syllabus (explicit non-goals for v1)

- Vertex AI / MLOps platforms (point to AI for DevOps + Vertex later)  
- Full BigQuery warehouse / Dataproc / Dataflow deep dive  
- Anthos / multi-cloud service mesh as required labs  
- Replacing the Terraform or Kubernetes courses  
- Course-sidebar hub pages (labs / quiz / faq / roadmap as separate nav items)  
- Paid SKUs required for the core path  

---

## Change control

To revise this syllabus: update this file, bump `version`, update `curriculum.yaml`, `tutorial_backlog.md`, `technologies_backlog.md`, `.cursor/prompts/technologies/gcp.md`, and `docs/gcp/index.md` in the same change.
