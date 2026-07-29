---
title: Certification frontmatter schema
description: Required YAML frontmatter and body sections for every REBASH Academy certification mapping page.
---

# Certification frontmatter schema

Every certification page under `docs/certifications/` must include this frontmatter. Objective mappings should align with [`certification_mapping.md`](certification_mapping.md) and [`curriculum.yaml`](../../curriculum.yaml).

```yaml
---
title: "Certification — Human-readable name"
description: "One or two sentences — maps Academy content to this exam, not a study guide."
certification_id: cka                    # stable slug
vendor: cncf                             # linux-foundation | redhat | hashicorp | aws | azure | gcp | cncf | docker | github | prometheus | other
name: "Certified Kubernetes Administrator (CKA)"
level: associate                         # foundational | associate | professional | specialty | expert
difficulty: advanced
estimated_duration: "8–12 weeks"
recommended_experience: "6 months hands-on Kubernetes"
career_paths:
  - kubernetes-engineer
  - devops-engineer
technologies:
  - kubernetes
  - docker
tutorials: []                            # tutorial ids — populated from mapping
labs: []
quizzes: []
projects: []
capstones: []
skills:
  - kubernetes-administration
official_url: "https://www.cncf.io/certification/cka/"
last_reviewed: "2026-07-29"
tags:
  - certifications
  - kubernetes
author: Shaik Basha
last_updated: "2026-07-29"
comments: false
---
```

## Body template

Every certification page follows this structure:

1. **Certification overview** — what the exam validates; link to official vendor page
2. **Target audience** — role and experience level
3. **Recommended experience** — vendor requirements in plain language
4. **Difficulty and preparation time** — honest estimate using Academy content
5. **Exam objectives** — vendor objective domains as headings
6. **Objective mapping** — table linking each domain to Academy content (see model below)
7. **Recommended learning path** — career path link and module order
8. **Required tutorials** — checklist with links
9. **Required labs** — hands-on proof points
10. **Required quizzes** — self-assessment gates
11. **Required projects** — portfolio builds that cover exam domains
12. **Recommended capstone** — path-ending build when applicable
13. **Interview preparation** — related interview guide links
14. **Practice checklist** — pre-exam readiness gates
15. **Recommended resources** — cheat sheets, official docs, vendor practice exams
16. **Official certification page** — primary external link

Certification pages **map** Academy content — they do not replace vendor study materials or teach exam dumps.

## Objective mapping model

Every exam objective chains to Academy assets:

```
Exam objective
  → Technology (curriculum id)
    → Tutorial(s)
      → Lab(s)
        → Quiz(es)
          → Project(s)
            → Interview prep
              → Capstone (optional)
```

| Mapping field | Purpose |
|---------------|---------|
| `objective_id` | Vendor domain or sub-domain id |
| `objective_title` | Human-readable objective |
| `technology` | Primary curriculum technology |
| `tutorials` | Tutorial slugs that cover the objective |
| `labs` | Labs that prove hands-on skill |
| `quizzes` | Quizzes that validate knowledge |
| `projects` | Projects applying the objective |
| `interview` | Interview guide sections |
| `capstone` | Capstone if path-ending |
| `coverage` | none · partial · good · complete |

Update [`certification_mapping.md`](certification_mapping.md) when tutorial-level tagging changes; certification pages import or mirror summary tables.

## Certification levels

| Level | `level` | Typical exams |
|-------|---------|---------------|
| Foundational | `foundational` | AWS Cloud Practitioner, AZ-900, KCNA |
| Associate | `associate` | RHCSA, CKA, CKAD, Terraform Associate, AWS SAA |
| Professional | `professional` | RHCE, AWS DevOps Pro, AZ-305, GCP PCA |
| Specialty | `specialty` | CKS, AWS Security Specialty |
| Expert | `expert` | Multi-cert portfolios, architect paths |

## Vendor categories

| Vendor | `vendor` | Certifications in framework |
|--------|----------|----------------------------|
| Red Hat | `redhat` | RHCSA, RHCE |
| CNCF / Linux Foundation | `cncf` | KCNA, CKA, CKAD, CKS |
| HashiCorp | `hashicorp` | Terraform Associate |
| AWS | `aws` | Cloud Practitioner, SAA, Developer, SysOps, DevOps Pro, Security Specialty |
| Microsoft | `azure` | AZ-900, AZ-104, AZ-305, AZ-400 |
| Google | `gcp` | Cloud Digital Leader, ACE, PCA, PCDOE |
| GitHub | `github` | GitHub Foundations, GitHub Actions |
| Prometheus | `prometheus` | Prometheus Certified Associate |
| Docker | `docker` | Docker Certified Associate (historical reference) |

## Career path mapping

| Career path | Primary certifications |
|-------------|------------------------|
| `linux-administrator` | RHCSA, RHCE |
| `cloud-engineer` | AWS SAA, AZ-104, Google ACE |
| `devops-engineer` | Terraform Associate, CKA, AWS DevOps Pro |
| `kubernetes-engineer` | CKA, CKAD, CKS |
| `platform-engineer` | CKA, CKS, Terraform Associate |
| `devsecops-engineer` | CKS, AWS Security Specialty |
| `site-reliability-engineer` | CKA, Prometheus Certified Associate, GCP PCDOE |
| `cloud-architect` | AZ-305, GCP PCA, AWS SAA |
| `ai-for-devops` | (future — no primary cert yet) |

## Progress tracking framework

Each certification page should eventually expose readiness (manual checklist today; structured tracking future):

| Signal | Source |
|--------|--------|
| Tutorial completion | Tutorials listed in mapping marked complete by learner |
| Lab completion | Related labs finished with validation |
| Quiz completion | Quizzes passed at 70%+ |
| Project completion | Portfolio project built |
| Capstone completion | Path-ending capstone delivered |
| Readiness % | Weighted average of mapped content completion |
| Recommended next step | First incomplete item in objective order |

Dashboard concept (`docs/certifications/progress/` future): one row per certification with progress bars per content type and estimated readiness.

## Study roadmap

Standard progression for any certification:

1. Choose **career path** aligned to the cert
2. Complete **tutorials** for mapped technologies
3. Pass **labs** for hands-on domains
4. Pass **quizzes** at 70%+
5. Build **projects** covering weak domains
6. Drill **interview prep** for scenario domains
7. Complete **capstone** if on a path-ending track
8. Run **practice checklist** → certification ready

## Repository layout

```
docs/certifications/
  index.md                    # landing (certifications.html)
  redhat/
    rhcsa.md
    rhce.md
  kubernetes/
    cka.md
    ckad.md
    cks.md
  terraform/
    associate.md
  aws/
    saa.md
  azure/
  google-cloud/
  github/
  observability/
  progress/                   # future dashboard
```

Nav groups by vendor in `.pages` as pages ship. Until detail pages exist, the landing page links to career paths and technology tracks with live mapping.

## Cross-reference model

Every certification page links outward:

- **Career path** — primary study sequence
- **Technology index** — tutorial catalogue
- **Labs / quizzes / projects** — filtered by `certifications` frontmatter tag
- **Interview prep** — exam-adjacent scenarios
- **Cheat sheets** — exam-day command recall
- **Official vendor URL** — always present

Tutorial, lab, quiz, and project frontmatter should include `certifications: [CKA]` (or slug) for reverse lookup.
