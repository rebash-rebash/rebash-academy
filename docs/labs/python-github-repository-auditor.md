---
title: "Lab — Python GitHub Repository Auditor"
description: "Audit GitHub repositories via API or fixture JSON — branch protection, topics, and visibility checks without mutating repos."
difficulty: intermediate
estimated_time: "50–60 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - python
  - github
  - rest
  - httpx
comments: false
---

# Lab — Python GitHub Repository Auditor

## Lab Overview

**Purpose:** Read-only audit of repository metadata using the GitHub REST API — or fixtures when credentials are unavailable.

**Scenario:** Security asks for a weekly report: public repos without branch protection on `main`, missing `CODEOWNERS`, or disabled vulnerability alerts (where visible).

**Expected outcome:** CLI that prints a findings table/JSON and never creates tokens or changes settings.

!!! tip "This is a lab, not a tutorial"
    Apply [Git Automation — GitHub and GitLab](../python/git-automation-github-and-gitlab.md) and [REST APIs — requests, auth, and resilience](../python/rest-apis-requests-auth-and-resilience.md).

## Business Scenario

Platform owns dozens of application repos. Auditors need a dry report for compliance — not live remediations.

## Learning Objectives

- [ ] Call GitHub REST with timeouts and auth from env
- [ ] Fall back to fixture JSON when `GITHUB_TOKEN` is unset (`--fixture`)
- [ ] Classify findings with severities
- [ ] Never log the token

## Prerequisites

### Knowledge

- [REST APIs — requests, auth, and resilience](../python/rest-apis-requests-auth-and-resilience.md)
- [Git Automation — GitHub and GitLab](../python/git-automation-github-and-gitlab.md)
- [Configuration Management and Secrets](../python/configuration-management-and-secrets.md)

### Software

| Tool | Notes |
|------|--------|
| httpx or requests | pin versions |
| Optional | `GITHUB_TOKEN` with **read-only** scopes |

**Estimated cost:** £0.

## Architecture

```text
--fixture OR GitHub API --> normalise repo docs --> rules engine --> findings.json
```

## Environment

```bash
mkdir -p ~/rebash-lab-python-gh/{fixtures,out}
cd ~/rebash-lab-python-gh
python3 -m venv .venv && source .venv/bin/activate
pip install 'httpx>=0.27,<1'
```

## Initial State — fixture path (required)
Create `fixtures/repos.json`:

```json
[
  {"full_name": "acme/payments", "private": false, "default_branch": "main",
   "has_branch_protection": false, "has_codeowners": false, "archived": false},
  {"full_name": "acme/internal-lib", "private": true, "default_branch": "main",
   "has_branch_protection": true, "has_codeowners": true, "archived": false}
]
```

## Task

### Step 1 – Loader

`audit_repos.py --fixture fixtures/repos.json` loads local JSON. Optional: `--org acme` with `GITHUB_TOKEN` fetches live data (read-only).

### Step 2 – Rules

Flag:

- Public + no branch protection → high
- Missing CODEOWNERS → medium
- Archived repos → skip or info

### Step 3 – Output

Write `out/findings.json` and print a short summary. Exit `0` always for audit-only (or `1` if `--fail-on high`).

## Validation

```bash
python audit_repos.py --fixture fixtures/repos.json
python -c 'import json; print(len(json.load(open("out/findings.json"))))'
```

- [ ] Fixture mode works with no network and no token
- [ ] At least one high finding for `acme/payments`
- [ ] Token never printed (grep your logs)
- [ ] Live mode documented as optional

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| 401 from API | Token missing/scopes; use `--fixture` |
| Rate limit | Back off; prefer fixtures in CI |

## Cleanup

```bash
deactivate 2>/dev/null || true
rm -rf ~/rebash-lab-python-gh
unset GITHUB_TOKEN
```

## Production Discussion

Use GitHub Apps with least privilege, store tokens in CI secret stores, and open issues or PRs for remediations instead of silent mutations.

## Related

- Next: [Docker Cleanup Tool](python-docker-cleanup-tool.md)
- Project: [Infrastructure Inventory CLI](../projects/python-infra-inventory-cli.md)
