---
title: Lab frontmatter schema
description: Required YAML frontmatter and body sections for every REBASH Academy lab.
---

# Lab frontmatter schema

Every lab under `docs/labs/` must include this frontmatter. Values should align with [`curriculum.yaml`](../../curriculum.yaml).

```yaml
---
title: "Lab — Human-readable title"
description: "One or two sentences for SEO and search."
difficulty: intermediate          # beginner | intermediate | advanced | expert
estimated_time: "60 min"
lab_level: guided                 # guided | practice | challenge | production
lab_type: scenario                # quick | guided | scenario | troubleshooting | challenge | migration | performance | security | automation | architecture | capstone
technology: linux                 # curriculum technology id
module: "Module 3 · Services"
career_paths:
  - devops-engineer
  - linux-administrator
skills:
  - systemd-troubleshooting
prerequisites:
  - linux/linux-systemd-services
related_tutorials:
  - linux/linux-journalctl-logs
related_projects:
  - projects/status-api-portfolio
environment:
  - local
  - docker
cloud_provider: null              # aws | azure | gcp | null
cost: free                        # free | low | moderate — with cleanup note in body
tags:
  - labs
  - linux
  - troubleshooting
author: Shaik Basha
last_updated: "2026-07-29"
comments: false
---
```

## Body template

Every lab page follows this structure:

1. **Lab overview** — purpose, scenario, expected outcome
2. **Business scenario** — realistic context and constraints
3. **Learning objectives**
4. **Prerequisites** — tutorials and tools required
5. **Architecture** — D2 diagram when topology helps
6. **Environment setup** — what to provision and how
7. **Tasks** — guided steps or open problem by `lab_level`
8. **Expected outcome**
9. **Validation steps** — commands, checklists, success criteria
10. **Troubleshooting** — common mistakes
11. **Best practices**
12. **Security considerations**
13. **Cleanup steps**
14. **References** — official docs first

## Lab levels

| Level | `lab_level` | Learner experience |
|-------|-------------|-------------------|
| 1 | `guided` | Follow explicit instructions |
| 2 | `practice` | Partial guidance — hints and checkpoints |
| 3 | `challenge` | Problem statement only |
| 4 | `production` | Real-world on-call scenario |

## Lab types

| Type | When to use |
|------|-------------|
| `quick` | Single concept, 15–30 minutes |
| `guided` | Step-by-step with validation gates |
| `scenario` | Business context and outcome |
| `troubleshooting` | Broken system — find and fix root cause |
| `challenge` | Minimal hints |
| `migration` | Move workloads with rollback plan |
| `performance` | Measure and tune |
| `security` | Hardening, scanning, secrets |
| `automation` | Script or pipeline replaces manual work |
| `architecture` | Design and trade-off decisions |
| `capstone` | Multi-tool end-to-end proof |

## Environments

Declare one or more values under `environment`:

- `local` — learner machine
- `docker` — containers on the host
- `vm` — virtual machine
- `kind`, `minikube`, `k3d` — local Kubernetes
- `kubernetes` — shared or cloud cluster
- `aws`, `azure`, `gcp` — cloud accounts (set `cloud_provider`)
- `codespaces`, `devcontainer` — remote dev environments

## Validation

Every lab must include a **Validation** section with:

- Commands to run and expected output (or acceptable ranges)
- A checklist the learner can tick off
- Clear success criteria before cleanup

Automated verification scripts are optional but encouraged for repeatable labs.

## Career path mapping

`career_paths` must use ids from `curriculum.yaml`. Labs typically map to one or more paths — for example a Kubernetes networking lab may serve DevOps Engineer, Platform Engineer, and SRE paths.

## Project mapping

Use `related_projects` to link labs that feed portfolio builds. Progression example:

**Terraform tutorial** → **Terraform plan review lab** → **Terraform project** → **Cloud landing zone capstone**

## Navigation

- Public browse experience: [Labs overview](../labs/index.md) (`template: labs.html`)
- Individual labs stay at `docs/labs/<slug>.md` — do not move lab URLs when adding categories
- Sidebar structure: `docs/labs/.pages` groups labs by technology

## Repository scale path

Future growth can add technology subfolders without breaking URLs:

```
docs/labs/
  index.md              # labs.html overview
  .pages                # nav grouped by technology
  linux/                # optional future grouping
    guided/
    practice/
    challenge/
    production/
```

Until subfolders exist, flat slugs with technology prefixes (`linux-*`, `shell-*`) remain the canonical pattern.
