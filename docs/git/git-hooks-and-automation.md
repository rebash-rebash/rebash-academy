---
title: Git Hooks and Automation
description: Implement client-side and server-side Git hooks for pre-commit linting, commit-msg validation, pre-push tests, and Husky/pre-commit framework integration.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
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



## Architecture



Hooks run scripts around Git events so teams can enforce policy locally and on the server before history is accepted.

![Git workflow and hooks around commit](../assets/excalidraw/git-workflow.svg)



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


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/git-hooks-and-automation && cd ~/rebash-git/git-hooks-and-automation
```

**Focus:** practise Git skills for: Git Hooks and Automation

### Step 1 – Init repository

```bash
git init -b main
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
echo '# lab' > README.md
git add README.md
git commit -m 'Initial commit'
git log --oneline
```

### Step 2 – Client hook

```bash
mkdir -p .git/hooks
cat > .git/hooks/pre-commit << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
! grep -RniE 'AKIA[0-9A-Z]{16}' --exclude-dir=.git . || { echo 'Blocked potential AWS key'; exit 1; }
EOF
chmod +x .git/hooks/pre-commit
echo 'safe' > ok.txt && git add ok.txt && git commit -m 'hook ok'
echo 'Hook installed for this lab repo only.'
```

### Final step – Cleanup note

```bash
# Safe local repo under the lab directory; delete the folder when finished
```



## Validation



Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Hook fires | Client hook blocks or messages as designed on commit/push |
| Bypass awareness | You know `--no-verify` risks and did not leave risky hooks installed |
| Sample script | Hook script is executable and path is correct |
| Cleanup | Lab hooks removed or disabled |



## Code Walkthrough



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



## Security Considerations



- Never install hooks from untrusted repos without reading them — hooks run as your user
- Prefer managed hook frameworks (pre-commit) with pinned versions over ad-hoc curl installs
- Do not put secrets in hook scripts; read them from the environment or a vault at runtime
- Server-side hooks must validate, not silently mutate, pushed content
- Fail closed on secret detection — do not allow `--no-verify` in CI



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


1. Explain **Git Hooks and Automation** as you would in a senior engineer interview.
2. You rebased a shared branch and teammates are blocked — what now?
3. How do you recover a commit that seems lost?
4. What Git security controls belong in a production org?
5. How should Git history look for Infrastructure as Code (IaC) repos?

!!! tip "Sample answer — question 2"
    Stop force-pushing; communicate; use `reflog` to recover; prefer revert on shared main. Reset/rebase only on private branches.

!!! tip "Sample answer — question 4"
    Signed commits, protected branches, secret scanning, least-privilege tokens, and signed tags for releases.



## Related Tutorials



- [Git Bisect and Debugging History](git-bisect-and-debugging-history.md) *(previous — Module 5)*
- [Advanced Git Workflows](advanced-git-workflows.md) *(next)*
- [gitignore and gitattributes](gitignore-and-gitattributes.md)
- [Git in CI/CD and DevOps](git-in-ci-cd-and-devops.md)
- [Signed Commits and Git Security](signed-commits-and-git-security.md)
- Cheat sheet: [Git Cheat Sheet](../cheatsheets/git.md)
- Interview prep: [Git Interview Prep](../interview/git.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)



## References



- [Pro Git Book – Git Hooks](https://git-scm.com/docs/githooks)
- [pre-commit framework](https://pre-commit.com/)
- [GitLab – Push rules and hooks](https://docs.gitlab.com/ee/user/project/repository/push_rules.html)
- [Husky documentation](https://typicode.github.io/husky/)
- [REBASH Academy – Git Overview](index.md)
