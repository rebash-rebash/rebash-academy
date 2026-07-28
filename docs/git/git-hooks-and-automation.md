---
title: Git Hooks and Automation
description: Implement client-side and server-side Git hooks for pre-commit linting, commit-msg validation, pre-push tests, and Husky/pre-commit framework integration.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
category: git
tags:
  - git
  - hooks
  - automation
  - pre-commit
prerequisites:
  - Git Bisect and Debugging History
  - Basic Git Workflow — Add, Commit, Push
comments: false
---

# Git Hooks and Automation

## Overview

Git hooks are scripts Git runs automatically at lifecycle events — before commit, after merge, before push. They enforce team standards locally (format, lint, secrets scan) and on the server (reject non-compliant pushes). For DevOps teams, hooks are the first line of defense before CI minutes are spent.

This is **Tutorial 16** in **Module 6: Advanced & DevOps** of the REBASH Academy Git series.

## Prerequisites

- [Git Bisect and Debugging History](git-bisect-and-debugging-history.md)
- [Basic Git Workflow — Add, Commit, Push](basic-git-workflow-add-commit-push.md)
- Shell scripting basics from the Linux track

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Identify client-side vs server-side hooks
- [ ] Install and write hooks in `.git/hooks/`
- [ ] Use the pre-commit framework for shared hook management
- [ ] Implement pre-commit, commit-msg, and pre-push hooks
- [ ] Understand server-side hooks on GitHub, GitLab, and bare repos
- [ ] Bypass hooks safely when necessary (`--no-verify`)
- [ ] Integrate hooks with Terraform, YAML, and secret scanning

## Hook Lifecycle Diagram

```d2
direction: down

COMMIT: "git commit"
    PRE: "pre-commit hook"
    MSG: "commit-msg hook"
    POST: "post-commit hook"
    PUSH: "git push"
    PREPUSH: "pre-push hook"
    SERVER: "server-side\npre-receive / update"
    COMMIT -> PRE
    PRE -> MSG
    MSG -> POST
    PUSH -> PREPUSH
    PREPUSH -> SERVER
```

## Theory

### Hook Basics

Hooks live in `.git/hooks/` (non-bare) or bare repo root hooks directory. Filename is hook name without extension — must be **executable**.

Sample listing:

```text
pre-commit
commit-msg
pre-push
post-merge
pre-receive    (server)
update         (server)
post-receive   (server)
```

Exit **non-zero** to abort the Git operation.

### Client-Side Hooks

Run on developer machine:

| Hook | When | Common use |
|------|------|------------|
| **pre-commit** | Before commit created | Lint, format, secrets scan |
| **commit-msg** | After message entered | Enforce conventional commits |
| **pre-push** | Before push | Run unit tests |
| **post-merge** | After merge | npm install, terraform init |
| **prepare-commit-msg** | Before editor opens | Add ticket prefix |

Not copied on clone — each developer must install.

### Server-Side Hooks

Run on Git server (bare repo or platform equivalent):

| Hook | Purpose |
|------|---------|
| **pre-receive** | Reject entire push if any ref fails |
| **update** | Per-ref check during push |
| **post-receive** | Trigger deploy, mirror, email |

GitHub/GitLab don't expose raw hooks on SaaS — use Actions, CI rules, or push rules instead. Self-hosted GitLab and bare repos support native hooks.

### Sharing Hooks — pre-commit Framework

[pre-commit.com](https://pre-commit.com) manages hook configs in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: check-yaml
      - id: detect-private-key
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.86.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
```

Install:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Version-controlled — entire team gets same hooks on `pre-commit install`.

### Husky (Node.js projects)

JavaScript ecosystems use Husky + lint-staged:

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  }
}
```

Common in full-stack repos alongside DevOps configs.

### Example: commit-msg Hook

```bash
#!/usr/bin/env bash
# .git/hooks/commit-msg
commit_msg_file="$1"
commit_msg=$(cat "$commit_msg_file")
pattern='^(feat|fix|docs|chore|ci|refactor)(\(.+\))?: .{1,72}$'
if ! echo "$commit_msg" | grep -qE "$pattern"; then
  echo "ERROR: Commit message must match conventional format"
  echo "  Example: feat(iam): add bucket policy"
  exit 1
fi
```

### Example: pre-push Hook

```bash
#!/usr/bin/env bash
# .git/hooks/pre-push — run quick tests before push
remote="$1"
url="$2"
while read -r local_ref local_sha remote_ref remote_sha; do
  if [ "$local_sha" = "0000000000000000000000000000000000000000" ]; then
    continue  # branch delete
  fi
  echo "Running tests before push to $remote_ref..."
  make test-quick || exit 1
done
```

### Skipping Hooks

```bash
git commit --no-verify -m "emergency hotfix"
git push --no-verify
```

Emergency only — bypasses all hooks. Audit who uses `--no-verify` via server rules where possible.

### core.hooksPath

Share custom hooks directory:

```bash
git config core.hooksPath .githooks
chmod +x .githooks/*
```

Committed to repo — works without pre-commit framework.

## Hands-on Lab

### Step 1 – Create repo and sample pre-commit hook

**Command:**

```bash
mkdir -p /tmp/git-hooks-lab && cd /tmp/git-hooks-lab
git init -b main
cat > .git/hooks/pre-commit << 'EOF'
#!/usr/bin/env bash
if grep -r "AKIA" --include='*.tf' --include='*.env' . 2>/dev/null; then
  echo "ERROR: Possible AWS key detected"
  exit 1
fi
echo "pre-commit: secret scan passed"
EOF
chmod +x .git/hooks/pre-commit
```

### Step 2 – Test hook blocks bad commit

**Command:**

```bash
echo 'key = "AKIAFAKEKEY123456789"' > bad.tf
git add bad.tf
git commit -m "test: should fail" && echo "UNEXPECTED PASS" || echo "Hook blocked commit"
```

### Step 3 – Test hook allows good commit

**Command:**

```bash
echo 'region = "us-east-1"' > good.tf
git add good.tf
git commit -m "feat: add good terraform"
git log --oneline -1
```

### Step 4 – commit-msg hook

**Command:**

```bash
cat > .git/hooks/commit-msg << 'EOF'
#!/usr/bin/env bash
grep -qE '^(feat|fix|docs|chore): ' "$1" || {
  echo "Bad commit message format"
  exit 1
}
EOF
chmod +x .git/hooks/commit-msg
echo "bad message" > /tmp/msg.txt
.git/hooks/commit-msg /tmp/msg.txt && echo pass || echo blocked
```

### Step 5 – core.hooksPath approach

**Command:**

```bash
mkdir -p .githooks
cp .git/hooks/pre-commit .githooks/
git config core.hooksPath .githooks
git config core.hooksPath
```

### Step 6 – Clean up

**Command:**

```bash
cd /tmp && rm -rf git-hooks-lab
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `pre-commit install` | Install framework hooks | After cloning repo |
| `pre-commit run --all-files` | Run all hooks manually | CI local mirror |
| `git commit --no-verify` | Skip client hooks | Emergency only |
| `git config core.hooksPath DIR` | Shared hooks directory | Team standardization |
| `chmod +x .git/hooks/name` | Make hook executable | Required for hooks |
| `pre-commit autoupdate` | Update hook versions | Maintenance |

### .pre-commit-config.yaml starter for DevOps

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
        args: [--allow-multiple-documents]
      - id: check-merge-conflict
      - id: detect-private-key
      - id: end-of-file-fixer
  - repo: https://github.com/adrienverge/yamllint
    rev: v1.33.0
    hooks:
      - id: yamllint
```

## Common Mistakes

!!! warning "Hooks not executable"
    Git silently skips non-executable hooks. Always `chmod +x`.

!!! warning "Slow hooks on every commit"
    Run heavy tests in pre-push or CI; keep pre-commit fast (<5 seconds).

!!! warning "Relying only on client hooks for security"
    Client hooks are bypassable. Enforce on server via CI and branch protection.

!!! warning "Not versioning shared hook config"
    `.git/hooks` isn't cloned. Use pre-commit or core.hooksPath in repo.

## Best Practices

!!! tip "Fast pre-commit, thorough CI"
    Pre-commit: format + secrets. CI: full test suite + plan.

!!! tip "Pin hook versions in pre-commit config"
    Reproducible runs across developer machines.

!!! tip "Document --no-verify policy"
    Only break-glass incidents; require ticket and post-incident review.

!!! tip "Mirror pre-commit in CI"
    `pre-commit run --all-files` in pipeline catches hook-skipping.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Hook not running | Not executable or wrong name | chmod +x; verify filename |
| pre-commit not found | Not installed | pip install pre-commit |
| Hook passes locally, fails CI | Different versions | Pin rev in config |
| Infinite hook loop | Hook modifies files triggering itself | Use pre-commit file locking |
| Server hook not firing | SaaS platform limitation | Use CI push rules |
| --no-verify abused | No policy | Audit; server-side checks |

## Summary

- **Git hooks** automate validation at commit, push, and receive events
- **Client hooks** enforce local quality; **server hooks** enforce org policy
- **pre-commit framework** shares versioned hook configs across the team
- Exit non-zero to abort; use **--no-verify** only in emergencies
- Combine hooks with CI — never trust client-side alone for security

## Interview Questions

1. What are Git hooks, and where do they live?
2. What is the difference between pre-commit and pre-push hooks?
3. How do you share hooks across a team?
4. What does exit code 1 do in a hook script?
5. What is the pre-commit framework?
6. Why aren't .git/hooks copied on clone?
7. What server-side hooks exist on bare repositories?
8. When is git commit --no-verify appropriate?
9. What hooks would you add for a Terraform repository?
10. How do GitHub Actions relate to server-side hooks?

??? tip "Sample Answers (Questions 3 and 9)"

    **Q3 — Sharing hooks:** Options: (1) pre-commit framework with `.pre-commit-config.yaml` in repo — developers run `pre-commit install`; (2) `git config core.hooksPath .githooks` pointing to committed executable scripts; (3) documentation + installer script. Never rely on manual `.git/hooks` copy.

    **Q9 — Terraform hooks:** terraform_fmt for formatting, terraform_validate for syntax, tflint or checkov for policy, detect-private-key for credentials, check-merge-conflict for markers. Run fmt/validate pre-commit; full plan/checkov in CI.

## Related Tutorials

- [Git Bisect and Debugging History](git-bisect-and-debugging-history.md) *(previous — Module 5)*
- [Advanced Git Workflows](advanced-git-workflows.md) *(next)*
- [gitignore and gitattributes](gitignore-and-gitattributes.md)
- [Git in CI/CD and DevOps](git-in-ci-cd-and-devops.md)
- [Signed Commits and Git Security](signed-commits-and-git-security.md)

## References

- [Pro Git Book – Git Hooks](https://git-scm.com/docs/githooks)
- [pre-commit framework](https://pre-commit.com/)
- [GitLab – Push rules and hooks](https://docs.gitlab.com/ee/user/project/repository/push_rules.html)
- [Husky documentation](https://typicode.github.io/husky/)
- [REBASH Academy – Git Overview](index.md)
