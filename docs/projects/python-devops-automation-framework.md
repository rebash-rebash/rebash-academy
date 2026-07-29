---
title: "Project — Production DevOps Automation Platform (Capstone)"
description: "Capstone: production DevOps automation platform with CLI, plugins, cloud inventory, Kubernetes, Terraform, GitHub, monitoring, notifications, config, logging, testing, packaging, and docs."
difficulty: advanced
estimated_time: "24–40 hours"
category: projects
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - projects
  - python
  - capstone
  - framework
  - platform
comments: false
---

# Project — Production DevOps Automation Platform (Capstone)

Capstone for [Python for DevOps](../python/index.md) — a production-minded automation platform teammates can extend.

## Project Overview

**Goal:** Ship a packaged automation platform with shared libraries and plugin commands that default to dry-run for anything destructive.

**Must include:**

1. **CLI interface** — installable console script (`rebash-ops` or similar)
2. **Plugin architecture** — discoverable commands
3. **Cloud inventory** — AWS/Azure/GCP via fixtures + optional live read-only
4. **Kubernetes automation** — health / validate (read-only)
5. **Terraform automation** — plan summary wrapper (no apply)
6. **GitHub automation** — repository auditor (read-only)
7. **Monitoring** — REST probe command
8. **Notifications** — Slack dry-run / optional send
9. **Configuration management** — YAML + env overlay
10. **Logging** — structured, redacting secrets
11. **Testing** — pytest with fixtures (no live cloud in CI)
12. **Packaging** — pyproject.toml, versioning
13. **Documentation** — README runbook + architecture

**Success criteria:** Another engineer can clone, `uv sync` or `pip install -e .`, run tests, and execute dry-run commands in under 15 minutes.

**Estimated cost:** £0 (mocks in CI; optional local Docker/kind for demos).

## Goals

- [ ] One installable console script
- [ ] Plugins covering the feature list above
- [ ] Shared HTTP client (timeouts + retries)
- [ ] Secrets from env / files — never logged
- [ ] CI green on lint + pytest without cloud credentials

## Stack

| Piece | Choice |
|-------|--------|
| Packaging | pyproject.toml + uv or Poetry |
| CLI | Typer (recommended) or Click |
| HTTP | httpx |
| Platforms | kubernetes client, Docker SDK, Terraform CLI via subprocess |
| Cloud | boto3 / Azure / GCP optional |
| Test | pytest |
| CI | GitHub Actions or GitLab CI |

## Prerequisites

- Expert: [Platform Engineering Framework](python-platform-engineering-framework.md) (recommended)
- Tutorials across modules 12–27, especially [Production Engineering Patterns](../python/production-engineering-patterns.md) and [Security for DevOps Python](../python/security-for-devops-python.md)
- Capstone-oriented labs: CI/CD tool, secrets scanner, cloud inventories

## Milestones

### Milestone 1 — Package skeleton

`pyproject.toml`, `[project.scripts]`, `src/` layout, `--help`, logging helper.

### Milestone 2 — Shared libraries

Config loader (YAML + env), secrets helper, httpx client wrapper with timeouts/retries.

### Milestone 3 — Plugins (dry-run first)

| Command | Behaviour |
|---------|-----------|
| `logs analyse` | pathlib/re summary |
| `inventory cloud` | fixture/live read-only |
| `k8s health` | read-only readiness summary |
| `tf plan-summary` | fixture or `terraform show -json` |
| `gh audit` | fixture or GitHub API |
| `monitor http` | probes / fixtures |
| `notify slack` | dry-run default |
| `docker dangling` | dry-run default |

### Milestone 4 — Hardening

Secrets scanner in CI, coverage gate, operator runbook, architecture diagram.

## Validation

```bash
uv sync   # or pip install -e ".[dev]"
pytest -q
rebash-ops --help
rebash-ops inventory cloud --fixture tests/fixtures/aws.json
rebash-ops notify slack --dry-run --title "capstone" --text "ok"
```

## Production Discussion

Treat the platform as an internal product: semver, CHANGELOG, CODEOWNERS, least-privilege tokens, and explicit `--apply` for mutations. Prefer OIDC federated credentials over long-lived keys.

## Related

- Course: [Python for DevOps](../python/index.md)
- Interview: [Python interview prep](../interview/python.md)
- Quiz: [Python for DevOps Engineers Fundamentals](../quizzes/python-for-devops-engineers-fundamentals.md)
