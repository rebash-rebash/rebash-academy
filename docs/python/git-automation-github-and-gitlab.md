---
title: "Git Automation — GitHub and GitLab"
description: "Automate Git with GitPython and platform APIs — repositories, pull requests, webhooks, and audit CLIs for DevOps workflows."
difficulty: intermediate
estimated_time: "50–65 min"
technology: python
category: python
module: "Module 16 · Git Automation"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - cloud-engineer
skills:
  - python
  - gitpython
  - github-api
  - gitlab-api
prerequisites:
  - python/cloud-automation-aws-azure-gcp
next:
  - python/docker-sdk-automation
related:
  - python/rest-apis-requests-auth-and-resilience
  - labs/python-github-repository-auditor
labs:
  - labs/python-github-repository-auditor
  - labs/python-cicd-automation-tool
projects: []
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - git
  - github
  - gitlab
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Git Automation — GitHub and GitLab

## Overview

Automate local Git inspection with GitPython (or subprocess git), call GitHub/GitLab HTTP APIs for repo/PR metadata, and design a safe audit CLI that defaults to read-only.

Platform teams audit branch protection, open PRs, and webhook configs in bulk. Use **tokens from env**, paginate API lists, and prefer dry-run reports over auto-merging.

Complete [Cloud Automation](cloud-automation-aws-azure-gcp.md) (and REST module) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 16 · Git Automation** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [REST APIs](rest-apis-requests-auth-and-resilience.md)
- Git installed locally
- Optional: `GITHUB_TOKEN` / `GITLAB_TOKEN` with **read** scopes

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Inspect a local repo with GitPython or `git` subprocess  
- [ ] Call GitHub/GitLab REST for repo metadata  
- [ ] List pull/merge requests with pagination awareness  
- [ ] Describe webhook automation use cases  
- [ ] Keep mutating PR actions behind explicit flags

## Architecture

This topic’s control points and relationships are shown below.

![Git automation](../assets/excalidraw/python-git-automation.svg)

## Theory

### What it is

Git automation has two layers: **local repository facts** (branch, dirty tree, recent commits) via the `git` CLI or GitPython, and **forge APIs** (GitHub, GitLab) for pull/merge requests, protections, and org audit. Webhooks notify your service when events happen. Python glues these for inventory bots, release helpers, and policy checks — not for silent auto-merge in this course.

### Why it matters

Platform work is pull-request-centric. Scripts that list open PRs, verify required checks, or report clone health save hours of console clicking. Tokens with write scope are high-value secrets; treating GitHub/GitLab as just another Hypertext Transfer Protocol (HTTP) API with least privilege prevents a compromised CI job from rewriting `main`.

### How it works

For local facts, `subprocess` + `git status`/`rev-parse` is easy to reason about; GitPython helps when you need a richer object model in-process. For remotes, call REST with a Bearer token (GitHub) or `PRIVATE-TOKEN` (GitLab), paginate, and never log the token or clone URLs with embedded credentials. Webhook receivers must validate signatures, respond quickly (queue work), and not trust payload-supplied hosts blindly. Outbound hook registration uses least-privilege tokens.

```text
Authorization: Bearer $GITHUB_TOKEN
Accept: application/vnd.github+json
GET /repos/{owner}/{repo}/pulls
```

### Key concepts and comparisons

| Approach | Use when |
|----------|----------|
| `git` via subprocess | Simple status/log |
| GitPython | In-process object model |
| Platform REST | PRs, protections, org audit |

| Safety rule | Practice |
|-------------|----------|
| Auditor bots | Read-only tokens |
| Tutorials | No auto-merge |
| Logs | Redact tokens and private URLs |
| Webhooks | Verify signatures; queue work |

### Common pitfalls

- Fine-grained tokens with admin scope “for convenience.”  
- Scraping HTML instead of the API.  
- Logging `git remote -v` that contains embedded credentials.  
- Processing webhook bodies synchronously for minutes (timeouts, retries, duplicates).  
- Assuming GitLab project IDs and path-with-namespace are interchangeable without encoding.

## Hands-on Lab

**Focus:** practise the core workflow for Git Automation — GitHub and GitLab

```bash
mkdir -p ~/rebash-python/module-16
cd ~/rebash-python/module-16

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install 'GitPython==3.1.44' 'requests==2.32.3'
```

### Step 1 – Local repo facts

```bash
cd ~/rebash-python/module-16
source .venv/bin/activate

# Use REPO=/path/to/clone or default to current git root / cwd
REPO="${REPO:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"

cat > local_git.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from git import Repo


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".")
    try:
        repo = Repo(root, search_parent_directories=True)
    except Exception as exc:  # noqa: BLE001
        print(f"error: not a git repo: {exc}", file=sys.stderr)
        return 1
    print(f"bare={repo.bare}")
    print(f"dirty={repo.is_dirty()}")
    print(f"head={repo.head.commit.hexsha[:12]}")
    print(f"branch={repo.active_branch.name if not repo.head.is_detached else 'DETACHED'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
EOF

python local_git.py "$REPO"
```

### Step 2 – GitHub API fixture / live

```bash
mkdir -p fixtures
cat > fixtures/repo.json << 'EOF'
{
  "full_name": "rebash-in/demo",
  "default_branch": "main",
  "private": false,
  "open_issues_count": 2
}
EOF

cat > github_repo.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import requests


def from_fixture(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def from_api(owner: str, repo: str) -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN required for live mode")
    url = f"https://api.github.com/repos/{owner}/{repo}"
    r = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=15,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"GitHub API HTTP {r.status_code}")
    return r.json()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--fixture", type=Path)
    p.add_argument("--owner")
    p.add_argument("--repo")
    args = p.parse_args()
    try:
        data = (
            from_fixture(args.fixture)
            if args.fixture
            else from_api(args.owner, args.repo)
        )
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({
        "full_name": data.get("full_name"),
        "default_branch": data.get("default_branch"),
        "private": data.get("private"),
        "open_issues_count": data.get("open_issues_count"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python github_repo.py --fixture fixtures/repo.json
```

### Step 3 – PR list sketch

```bash
python - <<'PY'
prs = [{"number": 12, "title": "fix: health check", "user": "dev"}]
for pr in prs:
    print(f"#{pr['number']} {pr['title']} (@{pr['user']})")
print("# live: GET /repos/{owner}/{repo}/pulls?state=open")
PY
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-16/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Git Automation — GitHub and GitLab** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for python as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Fine-grained tokens with admin scope “for convenience.”  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Scraping HTML instead of the API.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Git Automation — GitHub and GitLab changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| 401 from GitHub | Bad/missing token | Export `GITHUB_TOKEN`; check scopes |
| `InvalidGitRepositoryError` | Wrong path | Pass repo root |
| Rate limit | Unauthenticated or burst | Auth; backoff (Module 14) |

## Summary

- Local Git for clone state; APIs for platform metadata  
- Fixtures keep CI green without tokens  
- Auditors stay read-only by default  
- Lab: [GitHub Repository Auditor](../labs/python-github-repository-auditor.md)

## Interview Questions

1. How does **Git Automation — GitHub and GitLab** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Docker SDK Automation](docker-sdk-automation.md)  
- [GitHub Repository Auditor lab](../labs/python-github-repository-auditor.md)

## References

- [GitPython](https://gitpython.readthedocs.io/)  
- [GitHub REST API](https://docs.github.com/en/rest)  
- [GitLab REST API](https://docs.gitlab.com/ee/api/)
