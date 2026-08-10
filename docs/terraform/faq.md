---
title: FAQ
description: "Frequently asked questions about the Terraform for Cloud & DevOps Engineers course."
technology_id: terraform
hide:
  - toc
author: Shaik Basha
last_updated: "2026-08-03"
category: terraform
tags:
  - terraform
---

# Terraform — FAQ

## Who is this course for?

Cloud, DevOps, Platform, SRE, and Infrastructure engineers who need production-ready **Terraform** and Infrastructure as Code (IaC) skills — from first `terraform init` through multi-cloud platforms and on-call troubleshooting.

## Do I need a cloud account for labs?

Most module labs use the **`null`** and **`local`** providers so you can complete exercises on a practice VM without AWS, Azure, or GCP credentials. Modules 17–18 discuss cloud and Kubernetes providers; those pages include offline validation paths where possible. When you do use a cloud account, prefer a sandbox subscription with billing alerts.

## Which Terraform version should I install?

Labs assume **Terraform CLI 1.5+** (for `moved` blocks and modern test features). Install from [HashiCorp releases](https://developer.hashicorp.com/terraform/install) or your package manager:

``` {.bash .ra-terminal title="Terminal"}
terraform version
# Terraform v1.9.x or newer recommended
```

Pin the same major/minor in CI and on engineer laptops to avoid provider schema surprises.

## Where is the official documentation?

HashiCorp maintains the source of truth:

- https://developer.hashicorp.com/terraform/docs
- https://registry.terraform.io/

The course index links here; tutorials cite specific language, CLI, and provider pages.

## How do GitHub Actions and `templatefile` work in MkDocs tutorials?

Terraform HCL, GitHub Actions workflow YAML, and `templatefile` templates often contain GitHub Actions expressions (dollar-brace-brace), Jinja tags, or Go-style double-brace placeholders that confuse MkDocs macros during site build. **Tutorial documentation** wraps those code fences in Jinja raw / endraw blocks so the site renders correctly. Files you create on disk for labs use normal syntax — no MkDocs wrapping.

When you copy a workflow from a tutorial into your repo, restore the normal Actions secret expressions (for example `secrets.TF_API_TOKEN` inside an Actions expression). Do not copy the MkDocs raw wrappers into your GitHub repository.

## Modules vs workspaces vs separate directories — which should I use?

| Approach | Best for | Watch out for |
|----------|----------|---------------|
| Separate directories + separate state | Production blast-radius isolation | More boilerplate |
| Workspaces | Quick personal experiments | Easy to select wrong workspace in prod |
| One mega-root | Learning only | Dangerous applies; huge plans |

Module 12 and [Production Terraform Patterns](production-terraform-patterns.md) explain trade-offs. Most enterprises prefer **separate live roots per environment**.

## How should I handle secrets?

Never commit `.tfvars` with passwords, API keys, or cloud tokens. Use environment variables, a secret manager (Vault, AWS SSM, Azure Key Vault), or HCP Terraform variables marked sensitive. See [Terraform Security and Secrets](terraform-security-and-secrets.md).

## What if `terraform plan` wants to destroy production?

Stop. Read every `-/+` and `- destroy` line. Common causes: renamed resource without `moved`, provider upgrade with force-new attributes, or manual console drift. Module 20 walks through triage order.

## Where are the tutorials?

Open **Module 1–20** in the sidebar, or start from the [modules table](index.md#2-modules) on the course homepage.

## How do labs and projects fit in?

Complete module tutorials first — each includes a topic-specific Hands-on Lab. Then use [Labs](../labs/index.md), Quizzes, and Projects for portfolio work.

## Do diagrams use D2 or Mermaid?

No. This course uses **Excalidraw** SVGs under `docs/assets/excalidraw/`. Regenerate with:

``` {.bash .ra-terminal title="Terminal"}
python3 scripts/generate-excalidraw-svg.py
```

## Is progress tracked?

Learner progress tracking is planned — the course structure is ready today.
