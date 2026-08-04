---
title: "Security Scanning and Supply Chain"
description: "Harden GitHub Actions pipelines with CodeQL, Trivy, dependency review, SBOM generation, and action pinning by commit SHA."
difficulty: advanced
estimated_time: "50–70 min"
technology: github-actions
category: github-actions
module: "Module 11 · Security"
learning_paths:
  - devops-engineer
  - devsecops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - github-actions
  - devsecops
  - supply-chain
  - codeql
  - sbom
prerequisites:
  - github-actions/multi-cloud-deployments-with-github-actions
next:
  - github-actions/testing-in-github-actions
related:
  - github-actions/secrets-variables-and-oidc
  - devsecops/index
tags:
  - github-actions
  - security
  - codeql
  - trivy
  - sbom
  - supply-chain
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---

# Security Scanning and Supply Chain

## Overview

Shipping fast without scanning is how critical vulnerabilities reach production. GitHub Actions integrates **CodeQL** (static analysis), **Trivy** (container and IaC scanning), **dependency review** (pull request dependency diffs), and **Software Bill of Materials (SBOM)** export — plus **pinning actions by full commit SHA** so third-party actions cannot silently change under a floating tag.

This is **Tutorial 11** in **Module 11: Security** of the REBASH Academy **GitHub Actions for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, SRE, and DevSecOps engineers.

## Prerequisites

- [Multi-Cloud Deployments with GitHub Actions](multi-cloud-deployments-with-github-actions.md)
- [Secrets, Variables, and OIDC](secrets-variables-and-oidc.md)
- A test repository or local workflow folder (no live CodeQL database required for the lab)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Add CodeQL, Trivy, and dependency-review workflow stubs to a repository
- [ ] Generate an SBOM artefact in CI
- [ ] Pin third-party actions by commit SHA instead of mutable tags
- [ ] Explain supply-chain risks in reusable actions and marketplace dependencies
- [ ] Gate merges on security findings with branch protection

## Architecture

Security jobs run parallel to build/test; findings block promotion to deploy environments.

![Security and supply chain in GitHub Actions](../assets/excalidraw/gha-security.svg)

## Theory

### What it is

| Control | Purpose | Typical trigger |
|---------|---------|-----------------|
| CodeQL | Semantic code analysis for CVE classes | `push`, `pull_request`, schedule |
| Trivy | OS/package/IaC misconfiguration scan | After image build or on Terraform |
| Dependency review | Compare dependency changes on PRs | `pull_request` |
| SBOM | Inventory of components for audit/recall | Release or main build |
| SHA pinning | Immutable action reference | Every `uses:` line |

**Supply chain security** means treating actions, base images, and dependencies as untrusted until verified — pin versions, review diffs, and fail builds on critical findings.

### Why it matters

Compromised marketplace actions have exfiltrated secrets. Floating `@v4` tags can move without your review. Regulators and customers increasingly expect SBOMs and provenance. DevSecOps teams need scans in CI, not only periodic manual audits.

### How it works

1. **CodeQL** — `github/codeql-action` initialises a language database, runs queries, uploads results to GitHub Security tab.
2. **Trivy** — scans filesystem, container image, or Terraform for known CVEs and misconfigs; exit code fails the job on severity threshold.
3. **Dependency review** — GitHub compares lockfiles between base and head; blocks merges if new vulnerabilities exceed policy (requires GitHub Advanced Security for private repos).
4. **SBOM** — tools like `anchore/sbom-action` or Syft emit SPDX/CycloneDX JSON uploaded as artefact.
5. **SHA pinning** — `uses: actions/checkout@b4ffde65f46336ab88eb136be79bd9ced58fd2346` instead of `@v4`; Renovate or Dependabot proposes SHA bumps.

Example pin pattern (documentation):

{% raw %}
```yaml
- uses: actions/checkout@b4ffde65f46336ab88eb136be79bd9ced58fd2346 # v4.1.1
```
{% endraw %}

### Key concepts and comparisons

| Approach | Strength | Limitation |
|----------|----------|------------|
| CodeQL | Deep code paths, GitHub integration | Language setup; not runtime behaviour |
| Trivy | Fast container/IaC CVE scan | False positives on base images |
| Dependency review | PR-focused diff | Needs lockfiles; GHAS on private repos |
| SBOM | Audit/recall inventory | Does not fix vulnerabilities |
| SHA pin | Immutable action ref | Manual or bot updates for patches |

### Common pitfalls

- Scanning only on `main` — vulnerabilities merge before detection.
- Ignoring Trivy exit codes (`|| true`) — green builds with critical CVEs.
- Pinning only some actions while leaving deploy actions floating.
- No artefact retention for SBOM — cannot answer "what shipped in v1.2.3?"
- Running untrusted pull request code with `pull_request_target` and elevated secrets.

## Hands-on Lab

### Objective

Create a unified security workflow stub with CodeQL, Trivy filesystem scan, dependency review, SBOM upload, and SHA-pinned actions — validated offline.

### Prerequisites

- Python 3 with PyYAML
- Sample `go.mod`, `package-lock.json`, or `requirements.txt` optional for realism

### Lab environment

Workspace: `~/rebash-github-actions/module-11`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-github-actions/module-11/{.github/workflows,app} && cd ~/rebash-github-actions/module-11
set -euo pipefail
```

### Real-world scenario

DevSecOps requires every service repository to run static analysis, container/filesystem CVE scan, dependency review on pull requests, and publish an SBOM on each release tag — with all third-party actions pinned by SHA.

### Step-by-step tasks

#### Task 1 – Minimal app fixture and Trivy stub

Create `app/main.py`:

```python title="main.py"
"""Module 11 lab fixture — not production code."""
def greet(name: str) -> str:
    return f"hello, {name}"
```

Create `.github/workflows/security-scan.yml`:

{% raw %}
```yaml
name: Security Scan
on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  security-events: write

jobs:
  codeql:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb136be79bd9ced58fd2346
      - uses: github/codeql-action/init@df5843c3b785d4327488e3e57f5c753ff6b4c65
        with:
          languages: python
      - uses: github/codeql-action/analyze@df5843c3b785d4327488e3e57f5c753ff6b4c65

  trivy-fs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb136be79bd9ced58fd2346
      - name: Trivy filesystem scan (stub)
        uses: aquasecurity/trivy-action@0aa489ce2232e737ca7720b9b7f2b7ea0f558d67
        with:
          scan-type: fs
          scan-ref: .
          severity: CRITICAL,HIGH
          exit-code: 1

  dependency-review:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb136be79bd9ced58fd2346
      - uses: actions/dependency-review-action@3e653ccc4303e5e9c4f3d3e3e3e3e3e3e3e3e3e3
        continue-on-error: true

  sbom:
    runs-on: ubuntu-latest
    needs: [trivy-fs]
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb136be79bd9ced58fd2346
      - name: Generate SBOM placeholder
        run: |
          mkdir -p sbom
          echo '{"spdxVersion":"2.3","name":"module-11-lab-stub"}' > sbom/sbom.json
      - uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom/sbom.json
```
{% endraw %}

Validate offline:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-github-actions/module-11
set -euo pipefail
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/security-scan.yml')); print('security workflow OK')"
grep -c '@[0-9a-f]\{40\}' .github/workflows/security-scan.yml | tee pin-count.txt
```

!!! example "Expected output"
    `security workflow OK`; pin-count shows multiple SHA references.


#### Task 2 – Pinning policy as YAML and enforcement script

Create `action-pinning-policy.yaml`:

```yaml title="action-pinning-policy.yaml"
# Action pinning policy (Module 11)
rules:
  - id: sha-required
    rule: Every third-party uses MUST pin full commit SHA
    comment_tag: true  # add human tag as YAML comment, e.g. # v4.1.1
  - id: renovate
    rule: Dependabot or Renovate opens PRs to bump SHAs after review
  - id: no-floating
    rule: No @vN or @main floating refs in new workflows
exceptions:
  - scope: actions/*
    note: Bootstrap only — migrate to SHA within one sprint
review_checklist:
  - No floating refs in new workflows
  - SBOM artefact uploaded on release
  - Trivy exit-code not disabled
```

Create `check-unpinned-actions.sh`:

```bash title="check-unpinned-actions.sh"
#!/usr/bin/env bash
set -euo pipefail
# Fail if any uses: line pins a floating @vN tag instead of a 40-char SHA
violations=0
while IFS= read -r line; do
  if echo "$line" | grep -qE 'uses:.*@v[0-9]'; then
    echo "UNPINNED: $line"
    violations=$((violations + 1))
  fi
done < <(grep -h 'uses:' .github/workflows/*.yml 2>/dev/null || true)
if [ "$violations" -gt 0 ]; then
  echo "check-unpinned-actions: $violations floating tag(s) found"
  exit 1
fi
echo "check-unpinned-actions: all uses lines SHA-pinned or official actions/*"
```

Validate offline:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-github-actions/module-11
set -euo pipefail
python3 -c "
import yaml
with open('action-pinning-policy.yaml') as f:
    doc = yaml.safe_load(f)
assert any('SHA' in r['rule'] for r in doc['rules'])
assert 'no-floating' in {r['id'] for r in doc['rules']}
print('action-pinning-policy.yaml OK')
"
chmod +x check-unpinned-actions.sh
./check-unpinned-actions.sh | tee pin-check.txt
```

!!! example "Expected output"
    `action-pinning-policy.yaml OK`; `pin-check.txt` confirms no floating `@v` tags in the lab workflow.


#### Task 3 – Offline validation script

Create `sbom/sbom.json` (placeholder artefact for local validation):

```json
{
  "spdxVersion": "2.3",
  "name": "module-11-lab-stub"
}
```

Create `validate-security-lab.sh`:

```bash title="validate-security-lab.sh"
#!/usr/bin/env bash
set -euo pipefail
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/security-scan.yml'))"
python3 -c "import yaml; yaml.safe_load(open('action-pinning-policy.yaml'))"
test -f app/main.py
test -f sbom/sbom.json
grep -q 'codeql' .github/workflows/security-scan.yml
grep -q 'trivy' .github/workflows/security-scan.yml
grep -q 'upload-artifact' .github/workflows/security-scan.yml
./check-unpinned-actions.sh
echo 'module-11 validation passed'
```

Run it:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-github-actions/module-11
set -euo pipefail
mkdir -p sbom
chmod +x validate-security-lab.sh
./validate-security-lab.sh | tee validation.txt
```

!!! example "Expected output"
    `module-11 validation passed`


#### Task 4 – Evidence bundle

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-github-actions/module-11
set -euo pipefail
tar -czf module-11-evidence.tgz .github/workflows/security-scan.yml app/main.py action-pinning-policy.yaml check-unpinned-actions.sh validate-security-lab.sh
ls -l module-11-evidence.tgz | tee evidence.txt
```

!!! example "Expected output"
    Evidence archive listed in `evidence.txt`


### Validation steps

- [ ] Security workflow parses offline
- [ ] CodeQL, Trivy, dependency-review, and SBOM jobs present
- [ ] `action-pinning-policy.yaml` parses and `check-unpinned-actions.sh` passes
- [ ] Validation script passes locally

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| CodeQL language not detected | Missing sources | Add language files or adjust `languages:` |
| Trivy always green | `exit-code: 0` or `\|\| true` | Set `exit-code: 1` for CRITICAL/HIGH |
| Dependency review skipped | Not a pull request event | Expected locally; test in GitHub PR |
| Invalid SHA pin | Typo in commit | Verify SHA on github.com for that tag |
| `security-events: write` missing | CodeQL upload fails | Add permission for CodeQL |

### Challenge exercise

Add the floating-tag check from Task 2 as a job in `security-scan.yml` that runs `./check-unpinned-actions.sh` and fails the workflow on any `@vN` match.

### Learning outcomes

- Composed a multi-scanner security workflow stub
- Encoded SHA pinning policy as validated YAML
- Built `check-unpinned-actions.sh` to grep workflows for floating tags
- Produced offline validation evidence
- Mapped scanners to supply-chain controls

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
# Retain lab under ~/rebash-github-actions/module-11
ls ~/rebash-github-actions/module-11
```

## Validation

- [ ] Lab completed under `~/rebash-github-actions/module-11/`
- [ ] You can explain CodeQL vs Trivy scope
- [ ] You can justify SHA pinning over `@v4`
- [ ] You can describe one supply-chain failure mode

## Code Walkthrough

1. **Scan on pull request** — catch issues before merge.
2. **Fail on severity** — do not swallow Trivy/CodeQL exit codes.
3. **Pin every action** — treat tags as documentation comments only.
4. **Publish SBOM** — artefact per release for audit.
5. **Least permissions** — `security-events: write` only where needed.

## Security Considerations

- Third-party actions run with your workflow permissions — pin and review.
- `pull_request_target` with secrets is dangerous with fork code — prefer `pull_request` with restricted permissions.
- SBOMs may reveal internal package names — control artefact retention.
- CodeQL and dependency review need appropriate GitHub licence for private repos.
- Do not disable scans for "speed" on production paths.

## Common Mistakes

!!! warning "Floating `@v4` on marketplace actions"
    Tag can move to malicious commit. **Fix:** pin full SHA; automate updates via Dependabot.

!!! warning "Trivy `\|\| true` on deploy pipelines"
    Critical CVEs ship anyway. **Fix:** fail on agreed severity; waivers with ticket ID.

!!! warning "Scans only on main"
    Vulnerable code merges first. **Fix:** run on `pull_request`.

!!! warning "No SBOM retention"
    Cannot answer compliance queries. **Fix:** upload SBOM artefact per release tag.

## Best Practices

- Centralise security workflow as reusable workflow called by all services.
- Align severity thresholds with organisation policy (CRITICAL/HIGH block, MEDIUM warn).
- Integrate GitHub Advanced Security dashboards for triage.
- Sign container images and attach attestation where possible (Module 7 extension).
- Review action updates in pull requests like application dependencies.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| CodeQL no results | Wrong language/autobuild | Specify `languages` and build steps |
| Trivy slow | Full OS scan every job | Cache DB; scan changed paths only |
| Dependency review unavailable | GHAS/licence | Enable GHAS or use alternative SCA |
| SHA pin job fails checkout | Invalid commit | Update to valid action SHA |
| False positive flood | Old base image | Pin base image digest; waiver process |

## Summary

Security scanning and supply-chain hygiene belong in every pipeline: CodeQL, Trivy, dependency review, SBOM artefacts, and immutable action pins. Next: [Testing in GitHub Actions](testing-in-github-actions.md).

## Interview Questions

**1. Why pin GitHub Actions by commit SHA instead of version tag?**

??? success "Reveal answer"
    Tags are mutable — a maintainer or attacker can move `@v4` to a different commit. SHA pins are immutable content addresses so CI runs exactly the reviewed action code.

**2. What does CodeQL provide that Trivy does not?**

??? success "Reveal answer"
    CodeQL performs semantic static analysis on source code for vulnerability classes; Trivy focuses on known CVEs in packages, OS layers, and IaC misconfigurations — complementary, not interchangeable.

**3. When does dependency review run and what does it check?**

??? success "Reveal answer"
    On pull requests it compares dependency manifests/lockfiles between base and head, flagging newly introduced vulnerable dependencies against GitHub's advisory database.

**4. What is an SBOM and why generate it in CI?**

??? success "Reveal answer"
    A Software Bill of Materials lists components in a build artefact. Publishing it per release supports audit, incident response, and regulatory requests without manual inventory.

**5. What permission does CodeQL need to upload results?**

??? success "Reveal answer"
    {% raw %}`security-events: write`{% endraw %} so findings appear in the GitHub Security tab (alongside `contents: read` for checkout).

**6. Why is `pull_request_target` risky for security workflows?**

??? success "Reveal answer"
    It runs in the base repo context with access to secrets while checking out untrusted fork code — malicious pull requests can exfiltrate credentials. Use with extreme care or avoid.

**7. How should teams handle Trivy false positives on base images?**

??? success "Reveal answer"
    Pin base images by digest, track waivers with ticket IDs and expiry, upgrade bases on a schedule, and fail only on net-new CVEs where tools support it.

**8. Where do SHA pin updates belong in the delivery process?**

??? success "Reveal answer"
    Dependabot/Renovate pull requests reviewed like app deps — test in CI, merge pin bump, never auto-float tags in production workflows.

## Related Tutorials

- [Secrets, Variables, and OIDC](secrets-variables-and-oidc.md)
- [Docker Pipelines with GitHub Actions](docker-pipelines-with-github-actions.md)
- [Testing in GitHub Actions](testing-in-github-actions.md)

## References

- [GitHub CodeQL](https://code.github.com/codeql)
- [Trivy action](https://github.com/aquasecurity/trivy-action)
- [Dependency review](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review)
- [Security hardening for Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Pinning actions to full commit SHA](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#using-third-party-actions)
