---
title: Overview
description: "Terraform learning track — 20 tutorials from Infrastructure as Code fundamentals to production modules, state, and CI/CD."
difficulty: beginner
estimated_time: "Varies"
author: Shaik Basha
last_updated: "2026-07-28"
category: terraform
tags:
  - terraform
  - infrastructure-as-code
comments: false
---

# Terraform

Define, plan, and apply cloud infrastructure as code — from your first `.tf` file to modules, remote state, and production pipelines.

## Overview

The REBASH Academy **Terraform** track is a structured, 20-tutorial curriculum for DevOps engineers, SREs, and platform teams. Terraform is the industry standard for multi-cloud Infrastructure as Code. Each tutorial includes theory, hands-on labs, HCL walkthroughs, best practices, and interview questions.

!!! tip "Learning Path"
    Complete [Linux](../linux/index.md) and [Git](../git/index.md) first. [Docker](../docker/index.md) and [Kubernetes](../kubernetes/index.md) help later when you provision clusters and registries with Terraform.

## Curriculum Plan

Modules and tutorials in order. Use the tables below for links, level, and time estimates.

<figure class="rebash-diagram rebash-tree-diagram" markdown="0">
<p class="rebash-tree-title">Terraform Track</p>
<ul class="rebash-tree">
  <li>1 · Foundations
    <ul>
      <li>Introduction to Terraform and IaC</li>
      <li>Installing Terraform and the CLI Workflow</li>
      <li>HCL Fundamentals — Blocks and Expressions</li>
      <li>Providers and the Plugin Model</li>
    </ul>
  </li>
  <li>2 · Core Building Blocks
    <ul>
      <li>Variables, Locals, and Outputs</li>
      <li>Resources and Data Sources</li>
      <li>Dependencies and the Resource Graph</li>
      <li>Terraform State Fundamentals</li>
    </ul>
  </li>
  <li>3 · Collaboration and Scale
    <ul>
      <li>Remote State and Backends</li>
      <li>Workspaces and Environment Strategies</li>
      <li>Modules — Creating Reusable Infrastructure</li>
      <li>Registry Modules and Composition</li>
    </ul>
  </li>
  <li>4 · Language Power Tools
    <ul>
      <li>Meta-Arguments — count, for_each, lifecycle</li>
      <li>Functions, Templates, and Dynamic Blocks</li>
      <li>Import, Moved, and Safe Refactors</li>
    </ul>
  </li>
  <li>5 · Quality and Security
    <ul>
      <li>Format, Validate, and Terraform Test</li>
      <li>Secrets and Sensitive Values</li>
      <li>Policy as Code Overview</li>
    </ul>
  </li>
  <li>6 · Production
    <ul>
      <li>Terraform in CI/CD Pipelines</li>
      <li>Production Patterns and Capstone</li>
    </ul>
  </li>
</ul>
</figure>

### Module 1 – Foundations

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 1 | [Introduction to Terraform and Infrastructure as Code](introduction-to-terraform-and-iac.md) | Beginner | 35 min |
| 2 | [Installing Terraform and the CLI Workflow](installing-terraform-and-the-cli-workflow.md) | Beginner | 30 min |
| 3 | [HCL Fundamentals — Blocks, Arguments, and Expressions](hcl-fundamentals-blocks-arguments-and-expressions.md) | Beginner | 40 min |
| 4 | [Providers and the Terraform Plugin Model](providers-and-the-terraform-plugin-model.md) | Beginner | 35 min |

### Module 2 – Core Building Blocks

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 5 | [Variables, Locals, and Outputs](variables-locals-and-outputs.md) | Beginner | 40 min |
| 6 | [Resources and Data Sources](resources-and-data-sources.md) | Beginner | 45 min |
| 7 | [Dependencies and the Resource Graph](dependencies-and-the-resource-graph.md) | Intermediate | 40 min |
| 8 | [Terraform State Fundamentals](terraform-state-fundamentals.md) | Intermediate | 45 min |

### Module 3 – Collaboration and Scale

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 9 | [Remote State and Backends](remote-state-and-backends.md) | Intermediate | 45 min |
| 10 | [Workspaces and Environment Strategies](workspaces-and-environment-strategies.md) | Intermediate | 40 min |
| 11 | [Modules — Creating Reusable Infrastructure](modules-creating-reusable-infrastructure.md) | Intermediate | 50 min |
| 12 | [Registry Modules and Composition](registry-modules-and-composition.md) | Intermediate | 45 min |

### Module 4 – Language Power Tools

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 13 | [Meta-Arguments — count, for_each, and lifecycle](meta-arguments-count-for-each-and-lifecycle.md) | Intermediate | 50 min |
| 14 | [Functions, Templates, and Dynamic Blocks](functions-templates-and-dynamic-blocks.md) | Intermediate | 45 min |
| 15 | [Import, Moved, and Safe Refactors](import-moved-and-safe-refactors.md) | Intermediate | 45 min |

### Module 5 – Quality and Security

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 16 | [Format, Validate, and Terraform Test](format-validate-and-terraform-test.md) | Intermediate | 45 min |
| 17 | [Secrets and Sensitive Values](secrets-and-sensitive-values.md) | Intermediate | 40 min |
| 18 | [Policy as Code Overview](policy-as-code-overview.md) | Advanced | 40 min |

### Module 6 – Production

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 19 | [Terraform in CI/CD Pipelines](terraform-in-ci-cd-pipelines.md) | Advanced | 50 min |
| 20 | [Production Patterns and Capstone](production-patterns-and-capstone.md) | Advanced | 55 min |

**Total estimated time:** ~14 hours of hands-on learning

## Learning Objectives

After completing this track, you will be able to:

- [ ] Author production-ready Terraform root modules with pinned providers
- [ ] Manage state safely with remote backends and locking
- [ ] Build reusable modules and compose Registry modules
- [ ] Use `for_each`, lifecycle rules, and safe refactor features
- [ ] Integrate Terraform into CI/CD with plan artifacts and reviews
- [ ] Apply security practices for secrets, IAM, and policy as code

## Who Is This For?

| Audience | Benefit |
|----------|---------|
| **DevOps / SRE** | Provision and change infrastructure with reviewable plans |
| **Platform engineers** | Standardize modules and environments |
| **Cloud engineers** | Multi-cloud IaC skills beyond a single console |
| **Students** | Job-ready Terraform for interviews and labs |

## Related Sections

- [Linux](../linux/index.md) — CLI and filesystem fundamentals
- [Git](../git/index.md) — version modules and review plans in PRs
- [Docker](../docker/index.md) — images and registries you may provision
- [Kubernetes](../kubernetes/index.md) — clusters often managed with Terraform
- [Learning Paths](../learning-paths/index.md) — career-shaped roadmaps
