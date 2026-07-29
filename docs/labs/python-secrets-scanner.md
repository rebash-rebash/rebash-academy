---
title: "Lab — Python Secrets Scanner"
description: "Scan a repository tree for high-risk secret patterns (API keys, tokens, private keys) and fail CI when findings exist."
difficulty: intermediate
estimated_time: "45–55 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - python
  - security
  - secrets
  - scanning
comments: false
---

# Lab — Python Secrets Scanner

## Lab Overview

**Purpose:** Detect accidental secrets in source trees before push.

**Scenario:** A webhook URL and AWS-like key were committed last quarter. You need a lightweight scanner for pre-commit and CI.

**Expected outcome:** CLI walks files with pathlib, matches regex rules, exits `1` on findings; allowlist support.

!!! tip "This is a lab, not a tutorial"
    Apply [Security for DevOps Python](../python/security-for-devops-python.md) and [File Handling](../python/file-handling-pathlib-json-yaml-csv.md).

## Business Scenario

Secret scanning SaaS is coming next quarter. Until then, a focused Python scanner covers the top patterns.

## Learning Objectives

- [ ] Walk trees with pathlib; skip `.git`, `.venv`, binaries
- [ ] Compile secret regexes (AKIA…, PEM headers, Slack webhooks)
- [ ] Support allowlist file for false positives
- [ ] Never print full secret values (truncate)

## Prerequisites

### Knowledge

- [Security for DevOps Python](../python/security-for-devops-python.md)
- [File Handling — pathlib, JSON, YAML, CSV](../python/file-handling-pathlib-json-yaml-csv.md)

### Software

Python stdlib. **Estimated cost:** £0.

## Environment

```bash
mkdir -p ~/rebash-lab-python-secrets/{sample/{ok,bad},out}
cd ~/rebash-lab-python-secrets
python3 -m venv .venv && source .venv/bin/activate
```

## Initial State

```bash
echo 'api_url: https://example.com' > sample/ok/config.yaml
printf 'AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE\n' > sample/bad/leaked.env
printf '-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----\n' > sample/bad/id_rsa
```

## Task

Create `secrets_scan.py --path sample` writing `out/findings.json`. Exit `0` on clean, `1` on findings. Redact matches to first/last 4 characters.

## Validation

```bash
python secrets_scan.py --path sample/ok; echo $?    # 0
python secrets_scan.py --path sample/bad; echo $?   # 1
```

- [ ] Detects AKIA pattern and PEM header
- [ ] Findings redact secret bodies
- [ ] Skips itself if you point at `.venv`

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Binary noise | Skip non-text via charset / extension allowlist |
| False positive | `--allowlist allowlist.txt` with path substrings |

## Cleanup

```bash
deactivate 2>/dev/null || true
rm -rf ~/rebash-lab-python-secrets
```

## Production Discussion

Use gitleaks/trufflehog for depth; keep custom rules for org-specific tokens. Rotate any secret the scanner finds — assume compromise.

## Related

- Next: [CI/CD Automation Tool](python-cicd-automation-tool.md)
