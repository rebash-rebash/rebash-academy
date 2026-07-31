---
title: "Security Scanning and Supply Chain"
description: "Harden GitHub Actions delivery with secret scanning, dependency review, CodeQL, Trivy, SBOM, and supply-chain controls including pinning actions by SHA."
difficulty: advanced
estimated_time: "50–65 min"
technology: github-actions
category: github-actions
module: "Module 11 · Security"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - github-actions
  - appsec
  - supply-chain-security
  - codeql
  - trivy
prerequisites:
  - github-actions/multi-cloud-deployments-with-github-actions
next:
  - github-actions/testing-in-github-actions
related:
  - github-actions/secrets-variables-and-oidc
  - github-actions/docker-pipelines-with-github-actions
  - docker/container-scanning-and-sbom
labs: []
projects: []
interview: interview/github-actions
certifications:
  - GitHub Foundations
  - GitHub Actions
tags:
  - github-actions
  - security
  - codeql
  - trivy
  - sbom
  - supply-chain
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Security Scanning and Supply Chain

## Overview




Assemble a security stage that runs secret scanning and Dependency Review early, CodeQL for Static Application Security Testing (SAST), Trivy on container images, publishes a Software Bill of Materials (SBOM), and hardens the supply chain by pinning third-party Actions to commit SHAs.

**DevSecOps** embeds scanners into the same workflows that build and deploy. GitHub provides secret scanning, Dependency Review (for pull requests), CodeQL, and ecosystem tooling for container scanning (for example Trivy) and SBOM export (CycloneDX / SPDX). Fail the pipeline on policy severity — do not treat scanners as optional decoration. Pin marketplace Actions by full commit SHA so a tagged release cannot silently change under you.

This is a core tutorial in **Module 11 · Security** of the REBASH Academy **GitHub Actions for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites




- [Multi-Cloud Deployments with GitHub Actions](multi-cloud-deployments-with-github-actions.md)



## Learning Objectives




By the end of this tutorial, you will be able to:

- [ ] Place secret scanning and Dependency Review before expensive builds  
- [ ] Run CodeQL and Trivy against source and Module 7 images  
- [ ] Outline SBOM output tied to a release digest  
- [ ] Pin Actions by commit SHA and explain why  
- [ ] Gate merges on severity thresholds



## Architecture




This topic’s control points and relationships are shown below.

![Security and supply chain](../assets/excalidraw/gha-security.svg)



## Theory




### What it is

Security jobs produce findings in the pull request and Security tab:

| Control | Looks at | When |
|---------|----------|------|
| Secret scanning / push protection | Commits and diffs | Earliest — every change |
| Dependency Review | Lockfile / manifest diffs on PRs | Before merge |
| CodeQL | Source / data-flow queries | Early on PR + default branch |
| Trivy (or equivalent) | Built image / filesystem | After Module 7 build |
| SBOM | Dependencies and image layers | Attach to release / attestation |

**Supply-chain hardening** also includes least-privilege `permissions`, OIDC over long-lived keys (Modules 5 and 10), immutable image digests, and **pinning Actions** to SHAs rather than movable tags such as `@v4`.

### Why it matters

Vulnerabilities found after production are incidents. Secrets in Git are credentials for attackers. Compromised marketplace Actions can exfiltrate tokens from every consumer workflow. Dependency and container Common Vulnerabilities and Exposures (CVEs) dominate modern findings; SBOM data answers “what did we ship?” for auditors. Pipelines that only deploy without scanning train teams to ignore risk.

### How it works

1. Enable secret scanning and push protection at organisation or repository level; block on verified leaks.  
2. On pull request: run **Dependency Review** and fail on disallowed licences or high-severity new deps.  
3. Run **CodeQL** (`github/codeql-action`) in parallel with unit tests where possible.  
4. After image build: **Trivy** (or cloud scanner) against the SHA artefact; fail on Critical/High per policy.  
5. Generate an **SBOM** (for example `anchore/sbom-action` or Trivy SBOM) and attach it to the release or attestation for that digest.  
6. In every workflow: pin third-party Actions to full commit SHAs; restrict `permissions`; avoid `pull_request_target` with untrusted checkout.

Treat false positives with tracked allowlists — not by disabling scanners globally. Rotate secrets on confirmed leak; never only suppress the alert.

### Key concepts and comparisons

| Control | Strength | Limit |
|---------|----------|-------|
| Secret scanning | Stops key commits | Still rotate if already leaked |
| Dependency Review | Blocks bad new deps on PR | Needs lockfiles |
| CodeQL | Deep SAST | Query pack tuning / noise |
| Container scan | Matches what you ship | Base-image debt accumulates |
| Pin Actions by SHA | Stops tag moves | Update discipline required |
| SBOM | Inventory for response | Must tie to release digest |

### Common pitfalls

- Enabling scanners but never failing on Critical/High.  
- Scanning `latest` while deploying a different tag.  
- Using `@v4` everywhere and calling it “secure enough”.  
- Allowlisting secrets instead of rotating them.  
- Generating an SBOM not attached to the released digest.  
- Broad `permissions: write-all` on every workflow.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-github-actions/module-11/.github/workflows && cd ~/rebash-github-actions/module-11/.github/workflows
```

**Focus:** secret hygiene job and supply-chain checklist

### Step 1 – Security workflow skeleton

```bash
mkdir -p .github/workflows
cat > SECURITY-CI.md << 'EOF'
- Enable secret scanning / push protection
- Pin actions to SHAs for high-assurance repos
- Least privilege permissions on workflows
- Review Dependabot PRs weekly
EOF
cat > .github/workflows/security.yml << 'EOF'
name: Security scanning
on:
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read
  security-events: write
jobs:
  secret_hygiene:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Basic secret grep
        run: |
          if grep -RInE '(AKIA[0-9A-Z]{16}|BEGIN (RSA |OPENSSH )?PRIVATE KEY)' .; then
            echo "Potential secret pattern found"; exit 1
          fi
          test -f SECURITY-CI.md
EOF
```

### Step 2 – Run local secret grep

```bash
grep -RInE '(AKIA[0-9A-Z]{16}|BEGIN (RSA |OPENSSH )?PRIVATE KEY)' . || echo "clean"
grep -E 'security-events|secret_hygiene' .github/workflows/security.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials
```



## Validation




- [ ] Lab commands run under `~/rebash-github-actions/module-11/.github/workflows/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough




Production practice for **Security Scanning and Supply Chain** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.



## Security Considerations




- Treat credentials and tokens for github-actions as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces



## Common Mistakes




!!! warning "Enabling scanners but never failing on Critical/High.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Scanning `latest` while deploying a different tag.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices




- Encode Security Scanning and Supply Chain changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible



## Troubleshooting




| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |



## Summary




**Security Scanning and Supply Chain** is essential for Cloud and DevOps engineers working with github-actions. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. Why pin third-party actions to commit SHAs?
2. What does dependency review add on pull requests?
3. How should teams handle a critical CVE in a base action/image?
4. What repository settings help prevent secret leaks?
5. How do workflow permissions reduce supply-chain impact?

!!! tip "Sample answer — question 2"
    Identify whether the finding is in direct dependencies, transitive packages, or the Action itself. Prefer patched versions and temporary exceptions with expiry.

!!! tip "Sample answer — question 4"
    Enable push protection/secret scanning and least-privilege permissions. Treat workflow YAML as production code.



## Related Tutorials




- [Course overview](index.md)
- [Testing in GitHub Actions](testing-in-github-actions.md)



## References




- [Secure use of Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions) · [CodeQL](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql) · [Dependency review](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review) · [Secret scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning) · [Trivy](https://aquasecurity.github.io/trivy/)
