# Technology Definition

> **Syllabus frozen:** Follow [`docs/_curriculum/gcp-syllabus.md`](../../../docs/_curriculum/gcp-syllabus.md) (v1.0). Do not renumber or rename modules without a syllabus revision.
>
> **Content quality:** Follow `.cursor/prompts/CONTENT_QUALITY.md`, `tutorial-format-linux.md`, `create_lab.md`, and `create_interview_questions.md`. Labs: topic-specific, copy-paste executable, real GCP preferred with budget + cleanup. Prefer Codex until the user changes agents.

## Course

Google Cloud for Cloud & DevOps Engineers

---

## Description

A production-focused Google Cloud course for Cloud Engineers, DevOps Engineers, Platform Engineers, and Site Reliability Engineers (SREs).

Teach Google Cloud from fundamentals through production architecture: Identity and Access Management (IAM), networking, compute, storage, Google Kubernetes Engine (GKE), Cloud Run, automation, security, monitoring, and cost optimisation.

Learners finish able to design, deploy, and operate production workloads on Google Cloud with `gcloud` and professional cleanup habits.

---

## Target Roles

- Cloud Engineer
- DevOps Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)
- DevSecOps Engineer
- Infrastructure Engineer
- Cloud Architect

---

## Difficulty

Beginner → Advanced (plain language; prerequisites carry foundations)

---

## Estimated Duration

12–16 weeks

---

## Prerequisites

| Required | Nice to have |
|----------|----------------|
| Linux | Docker (before Module 7) |
| Networking | Kubernetes (before Module 7) |
| Git | Terraform (before Module 12) |

---

## Lab conventions

- Lab root: `~/rebash-gcp/module-NN`
- Real Google Cloud preferred (Free Trial / Always Free)
- Module 1: budget alert before later compute
- Every lab: create → prove → break/fix where useful → **cleanup**
- Fallback if billing/org policy blocks: inspect / dry-run / config-only proof

---

## MCP Servers

Primary

- Google Cloud

Optional

- Terraform
- Kubernetes
- Context7
- GitHub

---

# Modules (frozen — one tutorial each)

| # | Tutorial ID | Title |
|---|-------------|-------|
| 1 | `gcp/google-cloud-fundamentals-and-global-infrastructure` | Google Cloud Fundamentals and Global Infrastructure |
| 2 | `gcp/iam-identity-access-and-resource-hierarchy` | IAM, Identity Access, and Resource Hierarchy |
| 3 | `gcp/vpc-networking-on-gcp` | VPC Networking on Google Cloud |
| 4 | `gcp/compute-engine-migs-and-load-balancing` | Compute Engine, MIGs, and Load Balancing |
| 5 | `gcp/storage-gcs-persistent-disk-and-filestore` | Cloud Storage, Persistent Disk, and Filestore |
| 6 | `gcp/databases-on-gcp` | Databases on Google Cloud |
| 7 | `gcp/containers-gke-and-artifact-registry` | Containers — GKE and Artifact Registry |
| 8 | `gcp/serverless-on-gcp` | Serverless on Google Cloud |
| 9 | `gcp/data-and-analytics-on-gcp` | Data and Analytics on Google Cloud |
| 10 | `gcp/monitoring-and-observability-on-gcp` | Monitoring and Observability on Google Cloud |
| 11 | `gcp/gcp-security-services` | Google Cloud Security Services |
| 12 | `gcp/infrastructure-as-code-on-gcp` | Infrastructure as Code on Google Cloud |
| 13 | `gcp/cicd-on-gcp` | CI/CD on Google Cloud |
| 14 | `gcp/cost-optimisation-on-gcp` | Cost Optimisation on Google Cloud |
| 15 | `gcp/production-gcp-landing-zones` | Production GCP Landing Zones |
| 16 | `gcp/troubleshooting-gcp` | Troubleshooting Google Cloud |

## Module 1 — Google Cloud Fundamentals

- What is Google Cloud?
- Global infrastructure, regions, zones
- Projects, organisations, folders, billing accounts
- Cloud Console, Cloud Shell, `gcloud` CLI
- **Lab proof:** auth + project set + list regions/zones + budget alert

## Module 2 — Identity & Access Management

- IAM roles and permissions
- Service accounts
- Workload Identity / federation (intro)
- Organisation policies (intro)
- Resource hierarchy
- **Lab proof:** service account + role bind + deny-proof

## Module 3 — Networking

- VPC, subnets, routes, firewall rules
- Cloud Router, Cloud NAT, Cloud DNS
- Cloud Load Balancing (intro)
- Private Service Connect, Shared VPC, VPC peering (concepts)
- **Lab proof:** VPC + subnet + firewall + reachability

## Module 4 — Compute

- Compute Engine
- Instance templates, Managed Instance Groups (MIGs)
- Autoscaling, startup scripts
- **Lab proof:** VM + startup script + prove + cleanup

## Module 5 — Storage

- Cloud Storage classes and lifecycle
- Persistent Disks, Filestore (overview)
- Snapshots
- **Lab proof:** bucket + lifecycle + upload/download

## Module 6 — Databases

- Cloud SQL (primary lab path)
- AlloyDB, Spanner, Firestore, Bigtable, Memorystore (compare)
- **Lab proof:** Cloud SQL or documented fallback + connect check

## Module 7 — Containers

- GKE Standard vs Autopilot
- Artifact Registry
- When Cloud Run vs GKE
- Cloud Build mention (detail in Module 13)
- **Lab proof:** registry push + small GKE/Autopilot deploy or alternate

## Module 8 — Serverless

- Cloud Run (primary)
- Cloud Functions, Eventarc, Pub/Sub, Workflows, API Gateway (overview)
- **Lab proof:** Cloud Run from container + URL prove

## Module 9 — Data & Analytics

- BigQuery (ops lens)
- Pub/Sub, Cloud Scheduler
- Dataflow / Dataproc (awareness only)
- **Lab proof:** BigQuery sample query + Pub/Sub topic/subscription

## Module 10 — Monitoring & Observability

- Cloud Monitoring, Cloud Logging
- Error Reporting, Trace, Profiler
- Managed Prometheus (intro)
- **Lab proof:** alert + log query

## Module 11 — Security

- Secret Manager, Cloud KMS
- Security Command Center, Binary Authorization (overview)
- IAM best practices, organisation policies
- **Lab proof:** secret + IAM grant + read prove

## Module 12 — Infrastructure as Code

- Terraform google provider (primary)
- Deployment Manager (legacy overview)
- Infrastructure Manager (awareness)
- **Lab proof:** Terraform apply VPC/bucket + destroy

## Module 13 — CI/CD

- Cloud Build, Cloud Deploy
- Artifact Registry
- GitHub Actions note for multi-cloud
- **Lab proof:** build → push → deploy Cloud Run

## Module 14 — Cost Optimisation

- Billing reports, budgets, labels
- Recommender, committed / sustained use (overview)
- **Lab proof:** labels + budget review + idle hunt

## Module 15 — Production GCP

- Landing zone, multi-project architecture
- Shared VPC sketch, organisation policies
- Logging and monitoring strategy
- **Lab proof:** multi-project/folder sketch + policy + runbook (capstone)

## Module 16 — Troubleshooting

- IAM, GKE, Cloud Run, VPC, DNS, Pub/Sub, BigQuery, cost
- **Lab proof:** break/fix triage checklist

---

# Course navigation (v1)

Overview + Modules 1–16 only. No Labs / Quizzes / Projects / Capstone / Cheatsheets / Interview / Certifications / FAQ / Roadmap sidebar hubs. Roadmap lives on the course Overview.

---

# Standalone backlog (not course nav)

- Projects: static site on Cloud Storage · three-tier app · production GKE platform  
- Capstone ID: `gcp-enterprise-platform`  
- Cheatsheets: `gcloud`, IAM, VPC, GKE, Cloud Run, BigQuery, Cloud Storage, Terraform on GCP, Cloud Monitoring, Troubleshooting  
- Cert soft-map: Cloud Digital Leader · Associate Cloud Engineer · Professional Cloud Architect · Professional Cloud DevOps Engineer · Professional Cloud Security Engineer  

---

# Out of syllabus (v1)

- Vertex AI / MLOps deep dive  
- Full warehouse / Spark-on-Dataproc track  
- Anthos / multi-cloud mesh as required labs  
- Replacing Terraform or Kubernetes courses  

---

# Capstone outcome

After the course learners should be able to:

- Design production Google Cloud architectures  
- Deploy and operate GKE and Cloud Run workloads  
- Automate with Terraform on the google provider  
- Build CI/CD with Cloud Build and Artifact Registry  
- Apply budgets, labels, and cleanup discipline  
- Troubleshoot IAM, networking, and workload failures  
- Apply Google Cloud Architecture Framework habits  
