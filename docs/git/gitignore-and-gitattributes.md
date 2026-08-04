---
title: ".gitignore and .gitattributes"
description: "Exclude secrets and build artefacts with .gitignore; normalise line endings and diffs with .gitattributes for cross-platform DevOps repos."
difficulty: beginner
estimated_time: "45–60 min"
technology: git
category: git
module: "Module 4 · Working with Repositories"
learning_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - devsecops-engineer
skills:
  - git
  - gitignore
  - gitattributes
prerequisites:
  - git/viewing-history-and-diffs
next:
  - git/branching-fundamentals
related:
  - git/signed-commits-and-git-security
  - git/git-for-infrastructure-as-code
tags:
  - git
  - gitignore
  - gitattributes
  - security
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---

# .gitignore and .gitattributes

## Overview

A Terraform repo that commits `.env` files or `*.tfstate` has already lost the security battle. **`.gitignore`** tells Git which paths never to track; **`.gitattributes`** controls how Git stores and displays files — line endings, diff behaviour, and merge strategies — so Linux CI and Windows laptops produce consistent commits.

This is **Tutorial 1** in **Module 4: Working with Repositories** of the REBASH Academy **Git & GitHub for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers. You will configure ignores for secrets and state files and enforce `eol=lf` for IaC text.

## Prerequisites

- [Viewing History and Diffs](viewing-history-and-diffs.md)
- Git 2.x
- Basic understanding of Terraform state (local files must not be shared)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Write `.gitignore` rules for `.env`, `*.tfstate`, and build output
- [ ] Verify ignored files never appear in `git status`
- [ ] Configure `.gitattributes` with `* text=auto eol=lf`
- [ ] Prove line-ending normalisation with `git check-attr`
- [ ] Leave evidence under `~/rebash-git/module-04`

## Architecture

Ignore rules filter untracked paths before they enter the object database; attributes apply on checkout, commit, and diff — shaping cross-platform IaC repos.

![Repository architecture — working tree, .git, and config](../assets/excalidraw/git-repository-architecture.svg)

## Theory

### What it is

**`.gitignore`** is a list of patterns (globs) Git skips when scanning for untracked files. Patterns can be global (`~/.config/git/ignore`), per-repo (`.gitignore`), or per-directory (nested files). **`.gitattributes`** assigns attributes to paths — commonly `text=auto`, `eol=lf`, `linguist-generated`, or custom merge drivers — stored in the index and applied on checkout.

### Why it matters

DevOps repos mix shell scripts, YAML, HCL, and generated JSON. Without ignores, engineers commit `.terraform/`, kubeconfig copies, and `.env` with API keys. Without attributes, Windows checkouts introduce CRLF and break Linux shebangs or Terraform plans in CI. Secret scanning helps after the fact; ignores prevent the leak at source.

### How it works

1. Git checks ignore patterns (last matching rule wins) before listing untracked files.
2. Already-tracked files stay tracked until removed with `git rm --cached`.
3. On add/commit, `.gitattributes` may normalise line endings to LF in the object store.
4. `git check-attr` reports effective attributes for a path.
5. CI should clone with the same attributes as developers — committed in repo root.

### Key concepts and comparisons

| Pattern | Matches |
|---------|---------|
| `.env` | File named `.env` in any directory |
| `*.tfstate` | Terraform state files |
| `!.env.example` | Negation — track example env |
| `/dist/` | Only root-level `dist/` |

| Attribute | Effect |
|-----------|--------|
| `text=auto` | Git detects text; normalise line endings |
| `eol=lf` | Store and checkout LF |
| `-diff` | Binary-like — skip textual diff |
| `merge=union` | Custom merge for specific files |

### Common pitfalls

- Adding `.env` to ignore after it was already committed — it remains tracked until `git rm --cached`.
- Copy-pasting ignore templates without `-lock.hcl` / `.terraform/` for Terraform.
- Relying on `core.autocrlf` alone instead of committed `.gitattributes`.
- Negation patterns (`!`) that do not match because a parent directory is ignored.

## Hands-on Lab

### Objective

Bootstrap an IaC-style repo where secrets and state are ignored, shell scripts use LF, and verification scripts prove Git never tracks forbidden files.

### Prerequisites

- Git 2.x

### Lab environment

Workspace: `~/rebash-git/module-04`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-git/module-04 && cd ~/rebash-git/module-04
set -euo pipefail
```

### Real-world scenario

Your team onboards a Terraform module repo. Security requires `.env` and `*.tfstate` never enter Git; platform requires LF line endings for all shell and HCL files consumed by Linux CI.

### Step-by-step tasks

#### Task 1 – Create repo with .gitignore for secrets and state

Write ignore rules and verify untracked secrets stay invisible to `git add .`.

Create `.gitignore`:

```gitignore title=".gitignore"
.env
*.tfstate
*.tfstate.*
.terraform/
dist/
```

Bootstrap the repo and verify ignores:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-git/module-04
set -euo pipefail
rm -rf iac-repo
mkdir iac-repo && cd iac-repo
git init -b main
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
printf 'variable "region" { default = "eu-west-1" }\n' > main.tf
printf 'SECRET=changeme\n' > .env
printf '{"version":4}' > terraform.tfstate
mkdir -p dist && echo 'built' > dist/out.bin
git add .
git status --short | tee ../ignore-status.txt
grep -q 'main.tf' ../ignore-status.txt
grep -qv '.env' ../ignore-status.txt || test ! $(grep -c '.env' ../ignore-status.txt) -gt 0
! grep -q '.env' ../ignore-status.txt
! grep -q 'tfstate' ../ignore-status.txt
git commit -m 'chore: add Terraform stub and gitignore'
cd ..
```

!!! example "Expected output"
    Only `main.tf` and `.gitignore` staged; `.env`, state, and `dist/` absent from status.


#### Task 2 – Add .gitattributes for LF normalisation

Enforce LF on text IaC files.

Create `.gitattributes`:

```gitattributes title=".gitattributes"
* text=auto eol=lf
*.sh text eol=lf
*.tf text eol=lf
*.yaml text eol=lf
dist/** -diff
```

Create `deploy.sh`:

```bash title="deploy.sh"
#!/bin/sh
echo ok
```

Commit and verify attributes:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-git/module-04/iac-repo
set -euo pipefail
git add .gitattributes deploy.sh
git commit -m 'chore: enforce LF via gitattributes'
git check-attr eol deploy.sh | tee ../attr-eol.txt
grep -q 'deploy.sh: eol: lf' ../attr-eol.txt
git check-attr diff dist/out.bin 2>/dev/null | tee ../attr-diff.txt || true
cd ..
```

!!! example "Expected output"
    `check-attr` reports `eol: lf` for `deploy.sh`.


#### Task 3 – Simulate tracked secret removal and evidence pack

If a secret was tracked, remove from index without deleting locally.

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-git/module-04/iac-repo
set -euo pipefail
# Simulate mistake: force-add then fix
git add -f .env 2>/dev/null || true
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  git rm --cached .env
  git commit -m 'fix: stop tracking .env secret file'
fi
git ls-files | tee ../tracked-files.txt
! grep -q '^\.env$' ../tracked-files.txt
git check-ignore -v .env | tee ../ignore-rule.txt
grep -q '.gitignore' ../ignore-rule.txt
tar -czf ../module-04-ignore-evidence.tgz -C .. \
  ignore-status.txt attr-eol.txt tracked-files.txt ignore-rule.txt
ls -l ../module-04-ignore-evidence.tgz | tee ../ignore-evidence.txt
cd ..
```

!!! example "Expected output"
    `.env` not in tracked list; `check-ignore` cites `.gitignore` rule.


### Validation steps

- [ ] `.env` and `*.tfstate` never committed
- [ ] `deploy.sh` has `eol: lf` attribute
- [ ] Evidence tarball created
- [ ] `git ls-files` lists no secret paths

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Secret still in history | Committed before ignore | `git rm --cached`; rotate secret; consider BFG |
| Ignore rule ignored | Wrong pattern | Test with `git check-ignore -v path` |
| CRLF in CI | Missing attributes | Add `.gitattributes`; renormalise |
| `git add .` still adds file | Negated or forced | Remove `-f`; fix pattern order |

### Challenge exercise

Add `!.env.example` with safe placeholder values, track it, and prove `git check-ignore` does not match `.env.example` while still matching `.env`.

### Learning outcomes

- Protected Terraform state and env files from tracking
- Enforced LF for shell and HCL
- Recovered from accidental staging with `git rm --cached`

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
ls ~/rebash-git/module-04/
```

## Validation

- [ ] Lab under `~/rebash-git/module-04`
- [ ] Can explain ignore vs untrack
- [ ] Can read `git check-attr` output
- [ ] Can name one secret that must never be in Git

## Code Walkthrough

1. **Ignore first** — add `.gitignore` before first commit in new repos.
2. **Template from org** — reuse approved DevSecOps ignore snippets.
3. **Attributes in repo** — not only local `core.autocrlf`.
4. **Verify with check-ignore** — automate in pre-commit hooks.
5. **Renormalise once** — `git add --renormalize .` after attribute policy changes.

## Security Considerations

- Never commit `.env`, kubeconfig, `id_rsa`, or cloud credential JSON.
- Terraform state contains secrets — use remote backend; ignore local state files.
- Ignore files do not remove history — rotate leaked secrets immediately.
- Review `.gitignore` in security audits alongside CODEOWNERS.
- Enable secret scanning on GitHub even with good ignores.

## Common Mistakes

!!! warning "Ignoring after commit"
    `.gitignore` does not untrack files. **Fix:** `git rm --cached <file>` and commit; rotate secrets.

!!! warning "Checking in .terraform/"
    Provider binaries bloat repo and hide supply-chain risk. **Fix:** Ignore `.terraform/`; use lock file `.terraform.lock.hcl` tracked intentionally.

!!! warning "CRLF on Linux shebang scripts"
    `#!/bin/sh\r` breaks execution. **Fix:** `eol=lf` in `.gitattributes` for `*.sh`.

## Best Practices

- Commit `.env.example` with dummy values only
- Track `.terraform.lock.hcl` for reproducible provider versions
- Use global ignore for editor swap files (`~/.config/git/ignore`)
- Document required env vars in README, not in `.env`
- Run `git secrets` or org scanners in CI

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| File still shows modified | Line-ending normalisation | `git add --renormalize` |
| Pattern does not match | Path relative to file location | Test with `check-ignore -v` |
| Binary diff noise | Missing `-diff` attribute | Add to `.gitattributes` |
| Submodule not ignored | Submodule rules differ | See submodules tutorial |

## Summary

You configured repository hygiene: ignores for secrets and Terraform state, attributes for consistent LF text. Next: [Branching Fundamentals](branching-fundamentals.md) for parallel delivery work.

## Interview Questions

**1. Does .gitignore affect already-tracked files?**

??? success "Reveal answer"
    No. Ignore rules only prevent untracked files from being added. Tracked files need `git rm --cached` and a commit to stop tracking while keeping the local copy.

**2. Why ignore *.tfstate?**

??? success "Reveal answer"
    State files contain resource IDs, sometimes secrets, and are environment-specific. Teams use remote backends (S3, GCS, Terraform Cloud) with locking instead of sharing state via Git.

**3. What does text=auto eol=lf do?**

??? success "Reveal answer"
    Git treats files as text when detected, normalises line endings to LF in the repository, and checks out LF — keeping Linux CI and containers consistent regardless of developer OS.

**4. How do you debug why a file is ignored?**

??? success "Reveal answer"
    Run `git check-ignore -v <path>` — it prints the matching pattern and which ignore file defined it.

**5. Difference between global and repo gitignore?**

??? success "Reveal answer"
    Global (`core.excludesfile`) applies to all repos on a machine (editor cruft). Repo `.gitignore` is shared with the team and versioned — required for IaC policy.

**6. When would you use -diff in gitattributes?**

??? success "Reveal answer"
    For generated binaries or large artefacts still stored in Git but not useful in textual diffs — reduces noise in pull requests and blame.

**7. What if .env was pushed to GitHub?**

??? success "Reveal answer"
    Rotate all secrets immediately, remove from history with approved tooling if policy requires, enable secret scanning, and fix process with pre-commit hooks — ignore alone is insufficient.

**8. Should you commit .terraform.lock.hcl?**

??? success "Reveal answer"
    Yes for provider version pinning — it is not secret state. It ensures CI and teammates resolve the same provider checksums.

## Related Tutorials

- [Viewing History and Diffs](viewing-history-and-diffs.md)
- [Signed Commits and Git Security](signed-commits-and-git-security.md)
- [Git for Infrastructure as Code](git-for-infrastructure-as-code.md)
- [Course index](index.md)

## References

- [gitignore documentation](https://git-scm.com/docs/gitignore)
- [gitattributes documentation](https://git-scm.com/docs/gitattributes)
- [GitHub gitignore templates](https://github.com/github/gitignore)
