---
title: FAQ
description: "Frequently asked questions about the GitHub Actions for Cloud & DevOps Engineers course."
technology_id: github-actions
hide:
  - toc
author: Shaik Basha
category: github-actions
tags:
  - github-actions
last_updated: "2026-08-03"
---

# GitHub Actions — FAQ

## Who is this course for?

DevOps, Cloud, Platform, Site Reliability Engineering (SRE), DevSecOps, and software engineers who need production GitHub Actions skills — from first workflow through enterprise CI/CD, OIDC, Terraform, security scanning, and operations.

## Do I need prior experience?

Complete [Git](../git/index.md) first. Modules 1–2 assume beginner Continuous Integration (CI) knowledge. [Docker](../docker/index.md), [Kubernetes](../kubernetes/index.md), and [Terraform](../terraform/index.md) are required from Module 7 onward. Basic cloud familiarity helps from Module 10.

## Where are the tutorials?

Open **Module 1–16** in the sidebar, or use the [modules table](index.md#2-modules).

## How do labs work?

Labs live under `~/rebash-github-actions/module-NN` (for example `module-09` for Terraform, `module-14` for composite actions). Each tutorial includes copy-paste tasks you can validate **offline** with local CLI tools (Terraform, pytest, PyYAML) before pushing to a test repository. Later modules include OIDC and cloud deploy **stubs** — replace placeholders with your sandbox trust policies; never commit real credentials.

## Do I need a paid GitHub plan?

Public repositories include generous Actions minutes. Private repositories need a plan with Actions minutes; some security features (dependency review on private repos) require GitHub Advanced Security. Labs are designed to pass local validation without spending minutes where possible.

## How does OIDC work in this course?

Module 5 introduces OpenID Connect (OIDC) concepts; Module 10 provides AWS, Azure, and Google Cloud YAML stubs. GitHub mints a short-lived JSON Web Token (JWT) per job when {% raw %}`permissions: id-token: write`{% endraw %} is set; your cloud trust policy maps repository, ref, and environment to a role. Prefer OIDC over static access keys in repository secrets.

## Can I use self-hosted runners?

Yes — Module 3 covers hosted vs self-hosted runners, labels, and groups. Production teams use self-hosted pools for larger builds, private network access, or GPU workloads. Keep runner VMs patched and isolate untrusted pull request jobs.

## Why wrap Actions expressions in docs?

This site uses MkDocs macros (Jinja). GitHub Actions expressions (dollar-brace-brace) look like macro syntax and break the docs build unless tutorial fences wrap them in raw Jinja blocks. Lab workflow YAML examples use that wrapping; tutorial prose should describe expressions in words or keep them inside those blocks.

## Do diagrams use D2 or Mermaid?

No. This course uses **Excalidraw** SVGs under `docs/assets/excalidraw/`. Regenerate with:

``` {.bash .ra-terminal title="Terminal"}
python3 scripts/generate-excalidraw-svg.py
```

## How do interview questions work?

In-tutorial sections include **6–8 topic-specific questions**, each with a collapsible `??? success "Reveal answer"` block. Standalone interview prep lives under Interview.

## What changed in the 2026-08-03 rewrite?

Modules 9–16 and hub pages were rewritten to the Linux/Jenkins quality bar: full tutorial sections (Overview through References), topic-specific labs, Excalidraw architecture diagrams, British English, and production judgement (environment gates, SHA pinning, plan-before-apply).

## Is progress tracked?

Learner progress tracking is planned — the course structure and labs are ready today.

## Where should I start after finishing the course?

Build the Capstone platform (reusable workflows, OIDC, multi-cloud stubs, security scanning, releases), then compare with [Jenkins](../jenkins/index.md) or [GitLab CI/CD](../gitlab/index.md) for interview breadth.
