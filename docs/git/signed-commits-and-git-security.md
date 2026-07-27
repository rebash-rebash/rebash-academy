---
title: Signed Commits and Git Security
description: Configure GPG and SSH commit signing, verify signatures, protect branches, manage secrets, and meet compliance requirements for Git repositories.
difficulty: advanced
estimated_time: "40 min"
author: Shaik Basha
category: git
tags:
  - git
  - security
  - gpg
  - signing
prerequisites:
  - Git Submodules and Subtrees
  - Git Installation and Configuration
  - Pull Requests and Code Review
comments: false
---

# Signed Commits and Git Security

## Overview

Compliance frameworks (SOC 2, FedRAMP) increasingly require proof that commits came from authorized developers. **Signed commits** cryptographically bind identity to changes. Combined with branch protection, secret scanning, and access controls, signing forms a defense-in-depth strategy for Git security in DevOps pipelines.

This is **Tutorial 19** in **Module 6: Advanced & DevOps** of the REBASH Academy Git series.

## Prerequisites

- [Git Submodules and Subtrees](git-submodules-and-subtrees.md)
- [Git Installation and Configuration](git-installation-and-configuration.md)
- [Pull Requests and Code Review](pull-requests-and-code-review.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Generate GPG and SSH signing keys
- [ ] Configure Git to sign commits and tags automatically
- [ ] Verify signatures locally and on GitHub/GitLab
- [ ] Enforce signed commits via branch protection
- [ ] Apply Git security best practices for secrets and access
- [ ] Understand Sigstore/gitsign as cloud-native alternative
- [ ] Respond to leaked credential incidents in Git history

## Signing Flow Diagram

```mermaid
flowchart LR
    DEV[Developer]
    KEY["Signing Key<br/>GPG or SSH"]
    COMMIT[Signed Commit]
    REMOTE["GitHub / GitLab"]
    VERIFY[Signature Verification]

    DEV -->|git commit -S| KEY
    KEY --> COMMIT
    COMMIT -->|push| REMOTE
    REMOTE --> VERIFY```

## Theory

### Why Sign Commits?

Git's default author metadata is trivially forgeable — anyone can set `user.email` to another person. **Signing** proves the committer possessed a private key associated with a verified identity.

Benefits:

- **Non-repudiation** — audit trail for compliance
- **Supply chain security** — verify code origin in CI
- **Protected branch enforcement** — reject unsigned commits

### GPG Signing

Traditional approach using OpenPGP:

```bash
gpg --full-generate-key
gpg --list-secret-keys --keyid-format=long
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git commit -S -m "feat: signed commit"
```

Export public key to GitHub/GitLab → Settings → SSH and GPG keys.

Verify:

```bash
git log --show-signature -1
gpg --verify .git/objects/...
```

### SSH Commit Signing (Git 2.34+)

Simpler for teams already using SSH keys:

```bash
ssh-keygen -t ed25519 -C "signing@example.com" -f ~/.ssh/id_ed25519_sign
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519_sign.pub
git config --global commit.gpgsign true
```

Add **signing** public key to GitHub (separate from authentication key).

### Signed Tags

Release tags should be annotated and signed:

```bash
git tag -s v2.0.0 -m "Release 2.0.0"
git push origin v2.0.0
```

Production deploy pipelines should verify tag signature before deploy.

### Platform Verification

GitHub shows **Verified** badge when:

- Signature valid
- Key associated with committer account
- For web commits, GitHub signs on your behalf

GitLab shows similar verification in commit view.

### Enforcing Signed Commits

**Branch protection rules:**

- Require signed commits
- Require linear history
- Require status checks
- Restrict push to specific teams

Combine with **rulesets** (GitHub) or **push rules** (GitLab self-managed).

### Secret Management in Git

**Never commit:**

- API keys, passwords, tokens
- Private keys, kubeconfig with credentials
- `.tfstate` files

**Prevention stack:**

1. `.gitignore` + `.gitattributes`
2. pre-commit `detect-private-key`
3. CI secret scanning (Gitleaks, GitHub secret scanning)
4. Regular audits

**If secret committed:**

1. Revoke credential immediately
2. Remove from history (`git filter-repo` / BFG)
3. Force push coordinated with team
4. Post-incident review

### Access Control

- **Least privilege** — read vs write vs admin
- **SSH deploy keys** — read-only for CI clone
- **PAT rotation** — short-lived tokens
- **2FA enforced** on Git hosting orgs
- **Audit logs** — review anomalous push events

### gitsign / Sigstore

Cloud-native keyless signing using identity from OIDC (GitHub Actions):

```bash
# gitsign signs with ephemeral certificates
gitsign commit -m "signed with sigstore"
```

No long-lived GPG key management — growing adoption in supply chain security.

### Supply Chain Frameworks

- **SLSA** — provenance attestations for builds
- **SBOM** — software bill of materials stored alongside releases
- Git signing is one layer — not sufficient alone

## Hands-on Lab

### Step 1 – Configure SSH signing (if key exists)

**Command:**

```bash
mkdir -p /tmp/git-sign-lab && cd /tmp/git-sign-lab
git init -b main
git config user.name "Sign Lab"
git config user.email "sign@example.com"

# Create signing key for lab
ssh-keygen -t ed25519 -f /tmp/sign_key -N "" -C "sign@example.com"
git config gpg.format ssh
git config user.signingkey /tmp/sign_key.pub
git config commit.gpgsign true
git config tag.gpgsign true
```

### Step 2 – Create signed commit

**Command:**

```bash
echo "secure config" > app.conf
git add app.conf
git commit -m "feat: add config with signing enabled"
git log --show-signature -1 2>&1 | head -15
```

**Explanation:** Without key on GitHub, shows "Good signature" locally but unverified on platform.

### Step 3 – Verify signature status

**Command:**

```bash
git verify-commit HEAD 2>&1 || echo "Verify output above"
git log --format="%H %G? %aN" -1
```

**Explanation:** `%G?` shows signature status: G=good, N=none, B=bad.

### Step 4 – Signed tag

**Command:**

```bash
git tag -s v0.1.0 -m "Signed release 0.1.0"
git tag -v v0.1.0 2>&1 | head -10
```

### Step 5 – Simulate unsigned commit rejection policy

**Command:**

```bash
git config commit.gpgsign false
echo "unsigned" >> app.conf
git commit -am "test: unsigned commit"
git log --format="%H %G?" -2
git config commit.gpgsign true
```

### Step 6 – Clean up

**Command:**

```bash
cd /tmp && rm -rf git-sign-lab sign_key sign_key.pub
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `git commit -S` | Sign single commit | Explicit sign |
| `git config commit.gpgsign true` | Auto-sign all commits | Global policy |
| `git log --show-signature` | Display signatures | Audit commits |
| `git verify-commit SHA` | Verify commit signature | CI gate |
| `git tag -s v1.0.0` | Signed annotated tag | Release |
| `gpg --list-secret-keys` | List GPG keys | Key management |
| `git config gpg.format ssh` | Use SSH signing | Modern alternative |

### CI signature verification

```bash
#!/usr/bin/env bash
# verify-signed-commits.sh — fail if recent commits unsigned
set -euo pipefail
RANGE="${1:-origin/main..HEAD}"
while read -r sha status; do
  if [ "$status" != "G" ]; then
    echo "ERROR: Commit $sha is not signed (status=$status)"
    exit 1
  fi
done < <(git log --format='%H %G?' $RANGE)
echo "All commits in range are signed."
```

## Common Mistakes

!!! warning "Signing key without backup"
    Lost key cannot sign; old signatures become unverifiable after key rotation. Backup securely.

!!! warning "Same key for auth and signing"
    Compromise exposes both. Use separate SSH keys.

!!! warning "Assuming signing replaces secret scanning"
    Signed malicious commits are still malicious. Sign AND scan.

!!! warning "Not revoking leaked secrets immediately"
    History rewrite takes time — revocation is first action.

## Best Practices

!!! tip "Enable commit.gpgsign globally from day one"
    Habits form early; retrofitting signing across team is harder.

!!! tip "Require signed commits on main via branch protection"
    Policy without enforcement gets ignored.

!!! tip "Use SSH signing for simpler developer experience"
    One less GPG agent headache on macOS/Linux.

!!! tip "Integrate secret scanning in CI and platform"
    GitHub Advanced Security, GitLab secret detection, or Gitleaks.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `gpg: signing failed` | Agent not running | Start gpg-agent; pinentry |
| Unverified on GitHub | Key not uploaded | Add GPG/SSH signing key to account |
| Wrong key used | Multiple keys | Set user.signingkey explicitly |
| CI cannot sign | No key in runner | Use bot account or gitsign |
| `error: gpg failed to sign` | Passphrase prompt in CI | Use gpg-agent or SSH signing |
| Secret in history | Committed before hook | filter-repo; revoke secret |

## Summary

- **Signed commits** cryptographically prove authorship — GPG or SSH keys
- Configure **commit.gpgsign** and upload public keys to hosting platform
- **Branch protection** can require signed commits on main
- **Secret scanning** and `.gitignore` complement signing — not substitutes
- **Signed tags** anchor trusted release deployments
- **gitsign/Sigstore** offers keyless signing for CI environments

## Interview Questions

1. Why are signed commits important for compliance?
2. What is the difference between GPG and SSH commit signing?
3. How do you configure Git to sign all commits automatically?
4. How do you verify a commit signature locally?
5. What should you do if a secret is committed to Git?
6. How do branch protection rules enforce signing?
7. What is the difference between author and committer in signed commits?
8. What is gitsign/Sigstore?
9. Why use separate keys for authentication and signing?
10. What layers form Git security defense-in-depth?

??? tip "Sample Answers (Questions 1 and 5)"

    **Q1 — Compliance value:** Signed commits provide cryptographic proof that a specific key holder created the change, supporting non-repudiation requirements in SOC 2 and similar frameworks. Combined with branch protection and audit logs, organizations demonstrate access control and change integrity for production infrastructure code.

    **Q5 — Secret committed:** Immediately revoke/rotate the credential in the target system — this works even before history cleanup. Then remove from Git history using git filter-repo or BFG Repo-Cleaner. Force-push cleaned history with team coordination. Run secret scan to verify removal. Document incident and improve pre-commit/CI scanning.

## Related Tutorials

- [Git Submodules and Subtrees](git-submodules-and-subtrees.md) *(previous)*
- [Git in CI/CD and DevOps](git-in-ci-cd-and-devops.md) *(next — finale)*
- [Git Installation and Configuration](git-installation-and-configuration.md)
- [Git Hooks and Automation](git-hooks-and-automation.md)
- [gitignore and gitattributes](gitignore-and-gitattributes.md)

## References

- [GitHub – Signing commits](https://docs.github.com/en/authentication/managing-commit-signature-verification)
- [GitLab – Signed commits](https://docs.gitlab.com/ee/user/project/repository/signed_commits/)
- [Sigstore gitsign](https://github.com/sigstore/gitsign)
- [git filter-repo](https://github.com/newren/git-filter-repo)
- [SLSA framework](https://slsa.dev/)
- [REBASH Academy – Git Overview](index.md)
