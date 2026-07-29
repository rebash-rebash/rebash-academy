---
title: "Git Automation — GitHub and GitLab"
description: "Automate Git with GitPython plus GitHub/GitLab APIs for repos, pull requests, and webhooks."
difficulty: intermediate
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: python
tags:
  - python
  - gitpython
  - github
  - gitlab
prerequisites:
  - Cloud Automation — AWS, Azure, and GCP
  - Python 3.12+ on Linux (WSL2/VM/cloud)
comments: false
---

# Git Automation — GitHub and GitLab

## Overview

Repository hygiene and PR automation are high-leverage DevOps Python tasks — always use tokens with least privilege.

This is **Tutorial 16** in **Module 16: Git Automation** of the REBASH Academy **Python for DevOps Engineers** series — written for DevOps engineers, SREs, platform engineers, and cloud engineers who automate infrastructure with production-quality Python.

## Prerequisites

- Cloud Automation — AWS, Azure, and GCP
- Python 3.12+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Git Automation — GitHub and GitLab” in real ops automation
- [ ] Use a project venv and avoid relying on system site-packages
- [ ] Produce clear stderr diagnostics and meaningful exit codes
- [ ] Prefer safe patterns (pathlib, subprocess list args, dry-run)
- [ ] Relate this topic to day-to-day DevOps and platform work

## Architecture

Ops Python sits between operators/CI and platforms (files, APIs, CLIs, and cloud control planes). This topic’s control points are shown below.

![Architecture diagram for Git Automation — GitHub and GitLab](../assets/images/python-git-automation.svg)

## Theory

### GitPython

Programmatic Git operations (clone, status, commit) when you must. Prefer the `git` CLI via subprocess for simple cases; use GitPython for structured inspection.

### GitHub API

REST/GraphQL via `requests`/`httpx` or PyGithub. List repos, branch protection, and workflow runs. Fixture responses in CI.

### GitLab API

Similar patterns with personal/project access tokens. Normalise fields so one auditor can target either forge.

### Repository Automation

Clone mirrors, enforce README/LICENSE presence, check default branch names, and report drift.

### Pull Requests

Open/list PRs, require reviews, label risk. Never auto-merge from untrusted events without checks.

### Webhooks

Validate signatures, reject replayed events, and keep handlers idempotent. Process asynchronously when work is heavy.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-python/lab16 && cd ~/rebash-python/lab16
```

**Focus:** GitHub repository auditor against recorded JSON fixtures; optional live dry-run

### Step 1 – Skeleton

```bash
cat > lab.py << 'EOF'
#!/usr/bin/env python3
print("lab16 git-automation-github-and-gitlab")
EOF
chmod +x lab.py
python3 lab.py
```

### Step 2 – GitHub repo auditor (fixtures)

```bash
cat > repos.json << 'EOF'
[{"name":"app","default_branch":"main","has_license":true},{"name":"legacy","default_branch":"master","has_license":false}]
EOF
cat > auditor.py << 'EOF'
#!/usr/bin/env python3
import json
from pathlib import Path

repos = json.loads(Path("repos.json").read_text())
findings = []
for r in repos:
    if r["default_branch"] != "main":
        findings.append(f"{r['name']}: default_branch={r['default_branch']}")
    if not r["has_license"]:
        findings.append(f"{r['name']}: missing license")
print("FINDINGS")
print("\n".join(findings) or "none")
print("RESULT ok")
EOF
python3 auditor.py
```

### Final step – Cleanup note

```bash
python3 lab.py
# keep ~/rebash-python for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-python/lab16/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] Dry-run / fixture behaviour is clear for any mutating or cloud action
- [ ] You can relate this topic to a real DevOps or platform task

## Code Walkthrough

Production Python for **Git Automation — GitHub and GitLab** always combines:

1. A clear entry point (`main()` + `if __name__ == "__main__"`)
2. A project virtual environment and pinned dependencies when third-party libs are used
3. Explicit error handling and logging (no silent `except Exception: pass`)
4. Safe I/O: `pathlib`, timeouts on HTTP, `subprocess.run([...])` without `shell=True`
5. Documented exit codes and dry-run defaults for mutating actions

Keep modules short enough to review in a single merge request. Prefer stdlib first; add httpx/requests, Typer, pytest, and platform SDKs when the job needs them.

## Security Considerations

- Treat all external input (args, files, env, API payloads) as untrusted until validated
- Never log secrets or `Authorization` headers; prefer masked CI variables and secret stores
- Prefer least privilege tokens and read-only / dry-run modes by default
- Avoid `shell=True`, unvalidated path deletes, and committing `.env` files
- Pin dependencies; review transitive packages for automation that runs in CI

## Common Mistakes

!!! warning "Using system Python without a venv"
    Global packages drift between laptops and CI. **Fix:** `python3 -m venv .venv` per project and pin dependencies.

!!! warning "Calling subprocess with shell=True"
    Untrusted strings become remote code execution. **Fix:** pass a list of arguments; never build a shell string for the happy path.

!!! warning "Mutating without dry-run"
    Cleanup and apply tools destroy shared environments. **Fix:** default to dry-run; require `--apply` for side effects.

## Best Practices

- One purpose per command; share helpers in a small library package
- Log to stderr; reserve stdout for data or RESULT lines
- Idempotent behaviour where schedulers and CI may retry
- Fixture / mock paths for GitHub, Docker, Kubernetes, Terraform, and cloud SDKs in CI
- Pair every new tool with at least one failing-path test you actually run

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `ModuleNotFoundError` in CI | Missing venv / pins | Recreate venv; install from lock/requirements |
| Works locally, fails in pipeline | Different Python or env | Pin `requires-python`; fingerprint env in the job |
| Hang on HTTP call | No timeout | Set `timeout=` on requests/httpx clients |
| Secrets in logs | Debug printing headers | Redact; never log tokens |
| Accidental prune/delete | No dry-run default | Default dry-run; label lab resources |

## Summary

**Git Automation — GitHub and GitLab** is a core skill for DevOps engineers automating real hosts, APIs, and pipelines with Python. Practise the lab until the failure path and dry-run path are as familiar as the happy path, then continue the track.

## Interview Questions

1. When would you choose Python over Bash for this kind of ops task?
2. What failure mode appears if you skip a venv, pinning, or dry-run here?
3. How would you test this behaviour in CI without live cloud credentials?
4. Where could secrets leak in a naive implementation of this topic?
5. What exit code contract would you document for teammates?

!!! tip "Sample answer — question 2"
    Floating dependencies and missing dry-run defaults create “works on my machine” automation that either breaks overnight or mutates shared infrastructure unexpectedly. Pin versions and default to report-only.

## Related Tutorials

- [Python for DevOps Engineers – Category Overview](index.md)
- [Cloud Automation — AWS, Azure, and GCP](cloud-automation-aws-azure-gcp.md) *(previous)*
- [Docker SDK Automation](docker-sdk-automation.md) *(next)*
- [Shell Scripting for DevOps Engineers](../shell/index.md)
- [Learning Paths](../learning-paths/index.md)

## References

- [Python 3 documentation](https://docs.python.org/3/)
- [requests documentation](https://requests.readthedocs.io/)
- [httpx documentation](https://www.python-httpx.org/)
- Track index: [Python for DevOps Engineers](index.md)
