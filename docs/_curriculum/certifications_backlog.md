---
title: Certifications backlog
description: Certification mapping backlog for REBASH Academy — ordered foundational to expert.
---

# Certifications backlog

Master backlog for certification mapping pages. Align with [`certification-frontmatter-schema.md`](certification-frontmatter-schema.md) and [`certification_mapping.md`](certification_mapping.md).

**Status values:** `mapped` · `draft` · `planned`

**Mapped** = tutorial-level mapping exists in `certification_mapping.md`. **Planned** = framework slot; content not yet mapped.

## Mapped — active Academy alignment

| Certification ID | Vendor | Certification | Level | Difficulty | Career paths | Technologies | Tutorials | Labs | Priority | Status |
|------------------|--------|---------------|-------|------------|--------------|--------------|-----------|------|----------|--------|
| `rhcsa` | redhat | RHCSA | associate | intermediate | linux-administrator | linux | ~25 | linux labs | P1 | mapped |
| `rhce` | redhat | RHCE | professional | advanced | linux-administrator | linux, shell | ~43 | linux, shell labs | P1 | mapped |
| `cka` | cncf | CKA | associate | advanced | kubernetes-engineer, devops-engineer | kubernetes, docker | ~40 | k8s, docker labs | P1 | mapped |
| `ckad` | cncf | CKAD | associate | advanced | kubernetes-engineer | kubernetes, docker | ~40 | k8s labs | P1 | mapped |
| `cks` | cncf | CKS | specialty | expert | devsecops-engineer, kubernetes-engineer | kubernetes, devsecops | ~20 | k8s, security labs | P1 | mapped |
| `terraform-associate` | hashicorp | Terraform Associate | associate | intermediate | devops-engineer, cloud-engineer | terraform | ~20 | terraform labs | P1 | mapped |
| `aws-saa` | aws | Solutions Architect Associate | associate | intermediate | cloud-engineer, cloud-architect | aws, networking | ~45 | aws, networking labs | P1 | mapped |
| `aws-security-specialty` | aws | Security Specialty | specialty | expert | devsecops-engineer, cloud-engineer | aws, devsecops | ~20 | aws labs | P2 | mapped |

## Planned — Red Hat & Linux Foundation

| Certification ID | Vendor | Certification | Level | Career paths | Priority | Status |
|------------------|--------|---------------|-------|--------------|----------|--------|
| `kcna` | cncf | KCNA | foundational | kubernetes-engineer, beginner | P2 | planned |

## Planned — AWS

| Certification ID | Vendor | Certification | Level | Career paths | Priority | Status |
|------------------|--------|---------------|-------|--------------|----------|--------|
| `aws-cloud-practitioner` | aws | Cloud Practitioner | foundational | cloud-engineer, beginner | P2 | planned |
| `aws-developer-associate` | aws | Developer Associate | associate | devops-engineer, cloud-engineer | P2 | planned |
| `aws-sysops-associate` | aws | SysOps Administrator | associate | cloud-engineer, site-reliability-engineer | P2 | planned |
| `aws-devops-pro` | aws | DevOps Engineer Professional | professional | devops-engineer | P1 | planned |

## Planned — Azure

| Certification ID | Vendor | Certification | Level | Career paths | Priority | Status |
|------------------|--------|---------------|-------|--------------|----------|--------|
| `az-900` | azure | AZ-900 | foundational | cloud-engineer, beginner | P2 | planned |
| `az-104` | azure | AZ-104 | associate | cloud-engineer | P1 | planned |
| `az-305` | azure | AZ-305 | professional | cloud-architect | P1 | planned |
| `az-400` | azure | AZ-400 | professional | devops-engineer | P2 | planned |

## Planned — Google Cloud

| Certification ID | Vendor | Certification | Level | Career paths | Priority | Status |
|------------------|--------|---------------|-------|--------------|----------|--------|
| `gcp-cdl` | gcp | Cloud Digital Leader | foundational | cloud-engineer, beginner | P3 | planned |
| `gcp-ace` | gcp | Associate Cloud Engineer | associate | cloud-engineer | P1 | planned |
| `gcp-pca` | gcp | Professional Cloud Architect | professional | cloud-architect | P1 | planned |
| `gcp-pcdoe` | gcp | Professional Cloud DevOps Engineer | professional | devops-engineer, site-reliability-engineer | P2 | planned |

## Planned — GitHub, Docker & observability

| Certification ID | Vendor | Certification | Level | Career paths | Priority | Status |
|------------------|--------|---------------|-------|--------------|----------|--------|
| `github-foundations` | github | GitHub Foundations | foundational | devops-engineer, beginner | P3 | planned |
| `github-actions` | github | GitHub Actions | associate | devops-engineer | P2 | planned |
| `docker-dca` | docker | Docker Certified Associate | associate | devops-engineer | P3 | planned |
| `prometheus-pca` | prometheus | Prometheus Certified Associate | associate | site-reliability-engineer | P2 | planned |

## Career path → certification matrix

| Career path | Recommended certifications (in order) |
|-------------|--------------------------------------|
| Linux Administrator | RHCSA → RHCE |
| Cloud Engineer | AWS SAA or AZ-104 or GCP ACE → specialty |
| DevOps Engineer | Terraform Associate → CKA → AWS DevOps Pro |
| Kubernetes Engineer | KCNA → CKA → CKAD → CKS |
| Platform Engineer | CKA → CKS → Terraform Associate |
| DevSecOps Engineer | CKS → AWS Security Specialty |
| Site Reliability Engineer | CKA → Prometheus PCA → GCP PCDOE |
| Cloud Architect | AWS SAA → AZ-305 or GCP PCA |

## Progress tracking (framework)

Future `docs/certifications/progress/index.md` dashboard columns:

| Column | Description |
|--------|-------------|
| Certification | Name and vendor |
| Tutorial % | Mapped tutorials completed |
| Lab % | Mapped labs completed |
| Quiz % | Mapped quizzes passed |
| Project % | Mapped projects built |
| Readiness | Weighted estimate |
| Next step | First incomplete mapped asset |

Weights default: tutorials 30%, labs 25%, quizzes 20%, projects 15%, interview 10% until capstone mapping completes.

## Navigation structure

```
Certifications
  Overview
  Red Hat (RHCSA, RHCE)
  Kubernetes / CNCF (KCNA, CKA, CKAD, CKS)
  Terraform
  AWS
  Azure
  Google Cloud
  GitHub
  Observability
  Learning Progress (future)
```

## Authoring order

1. Publish dedicated pages for **mapped** certifications (RHCSA, CKA, Terraform Associate, AWS SAA first)
2. Expand objective tables from `certification_mapping.md` into each page
3. Add `certifications:` tags to tutorial/lab/quiz frontmatter for reverse links
4. Azure and GCP pages when tutorial tracks ship
5. Progress dashboard when structured completion tracking is implemented
