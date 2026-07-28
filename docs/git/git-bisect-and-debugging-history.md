---
title: Git Bisect and Debugging History
description: Binary search commit history with git bisect to find regression-introducing commits; automate with test scripts for DevOps debugging.
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: git
tags:
  - git
  - bisect
  - debugging
  - regression
prerequisites:
  - Cherry-pick and Reflog
  - Viewing History and Diffs
comments: false
---

# Git Bisect and Debugging History

## Overview

Production worked in v1.4.0 but fails in v1.5.0 — which of 200 commits broke it? Manual search is impractical. `git bisect` performs binary search through history, halving the candidate set with each test. Combined with automated test scripts, bisect finds regression commits in logarithmic time.

This is **Tutorial 15** in **Module 5: Recovery & Debugging** of the REBASH Academy Git series.

## Prerequisites

- [Cherry-pick and Reflog](cherry-pick-and-reflog.md)
- [Viewing History and Diffs](viewing-history-and-diffs.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Start and run manual git bisect sessions
- [ ] Automate bisect with test scripts (`git bisect run`)
- [ ] Mark commits good/bad/skip appropriately
- [ ] Bisect across merge commits and tags
- [ ] Visualize bisect progress and results
- [ ] Integrate bisect into CI debugging workflows
- [ ] Reset cleanly after bisect with `git bisect reset`

## Bisect Process Diagram

```d2
direction: down

START: "Start bisect\nbad=HEAD good=v1.4.0"
    MID: "Checkout middle commit"
    TEST: "Test passes?" {
      shape: diamond
    }
    GOOD: "Mark good\nsearch upper half"
    BAD: "Mark bad\nsearch lower half"
    FOUND: "First bad commit found"
    START -> MID
    MID -> TEST
    TEST -> GOOD: yes
    GOOD -> MID
    TEST -> BAD: no
    BAD -> MID
    GOOD -> FOUND
    BAD -> FOUND
```

## Architecture

This topic is primarily procedural. The mental model is a straight line from inputs (commands, config files, or manifests) to observable system state — verify each change with the validation steps later in this tutorial.

## Theory

### Binary Search Concept

Given known **good** commit (works) and **bad** commit (broken), bisect checks out midpoint and asks: good or bad? Each answer eliminates half the remaining commits.

For N commits, ~log₂(N) steps — 1024 commits need ~10 tests.

### Starting Bisect

```bash
git bisect start
git bisect bad                    # current HEAD is broken
git bisect good v1.4.0            # tag known good
```

Git checks out middle commit. You test manually:

```bash
make test
git bisect good    # if pass
git bisect bad     # if fail
```

Repeat until first bad commit identified.

### Automated Bisect

```bash
git bisect start HEAD v1.4.0
git bisect run ./test.sh
```

Script exit codes:

- **0** — good
- **1–124, 126–127** — bad
- **125** — skip (untestable commit)

```bash
#!/usr/bin/env bash
# test.sh for bisect
make build && ./run-integration-test.sh
```

Automation enables overnight bisect on large histories.

### Skip Commits

Non-buildable commits (missing dependency, broken CI):

```bash
git bisect skip
```

Too many skips may fail to find exact commit — bisect warns.

### Bisect and Merges

Bisect walks first-parent chain by default on merge-heavy repos. Use `--first-parent` explicitly when appropriate:

```bash
git bisect start --first-parent
```

### Finding Good/Bad Boundaries

| Reference | Example |
|-----------|---------|
| Tag | `v1.4.0` |
| Commit SHA | `abc1234` |
| Relative | `HEAD~50` |
| Branch tip | `origin/main` |

Document good/bad boundaries in incident tickets.

### After Bisect

```bash
git bisect reset    # return to original branch
```

Always reset — bisect leaves you in detached HEAD.

### DevOps Use Cases

- **Terraform plan regression** — which commit changed module source?
- **Docker build failure** — which Dockerfile layer change broke build?
- **Flaky test introduction** — bisect with probabilistic test (harder)
- **Performance regression** — script comparing response time threshold

### git bisect log and replay

```bash
git bisect log > bisect.log
git bisect replay bisect.log
```

Share bisect session with teammates.

### Limitations

- Requires reproducible good/bad test
- Shallow clones may lack commits — unshallow first
- Flaky tests produce wrong results
- Submodule repos need extra care

## Hands-on Lab

### Step 1 – Create history with intentional bug

**Command:**

```bash
mkdir -p /tmp/git-bisect-lab && cd /tmp/git-bisect-lab
git init -b main

good_test() { test "$(cat counter.txt 2>/dev/null)" -lt 5; }

for i in 1 2 3 4 5 6 7 8; do
  echo "$i" > counter.txt
  git add counter.txt
  if [ "$i" -le 4 ]; then
    git commit -m "feat: increment to $i (good)"
  else
    git commit -m "feat: increment to $i (bad region)"
  fi
done
git log --oneline
```

**Explanation:** Commits 5-8 are "bad" when threshold is `< 5`.

### Step 2 – Manual bisect

**Command:**

```bash
git bisect start
git bisect bad HEAD
git bisect good HEAD~7
# Test current counter
VAL=$(cat counter.txt)
if [ "$VAL" -lt 5 ]; then git bisect good; else git bisect bad; fi
# Repeat until found — or use run script below
git bisect reset
```

### Step 3 – Automated bisect

**Command:**

```bash
cat > test.sh << 'EOF'
#!/usr/bin/env bash
val=$(cat counter.txt)
test "$val" -lt 5
EOF
chmod +x test.sh
git bisect start HEAD HEAD~7
git bisect run ./test.sh
git bisect reset
```

**Expected:** First bad commit is when counter reaches 5.

### Step 4 – Inspect culprit commit

**Command:**

```bash
git log --oneline | head -5
git show HEAD~4 --stat
```

### Step 5 – Clean up

**Command:**

```bash
cd /tmp && rm -rf git-bisect-lab
```

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

| Command | Description | Example |
|---------|-------------|---------|
| `git bisect start` | Begin session | `git bisect start bad good` |
| `git bisect good` | Mark current good | After successful test |
| `git bisect bad` | Mark current bad | After failed test |
| `git bisect skip` | Skip untestable | Broken build commit |
| `git bisect run script` | Automated bisect | `git bisect run ./test.sh` |
| `git bisect reset` | End and restore | Always run when done |
| `git bisect log` | Export session | Share with team |

### Terraform plan bisect test

```bash
#!/usr/bin/env bash
# tf-plan-bisect.sh — exit 0 if plan succeeds without errors
set -euo pipefail
terraform init -backend=false -input=false >/dev/null 2>&1
terraform validate
terraform plan -detailed-exitcode -input=false >/dev/null 2>&1
rc=$?
# 0 = no changes (good), 2 = changes (good), 1 = error (bad)
test "$rc" -ne 1
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Forgetting git bisect reset"
    Leaves repo in detached HEAD — confusing subsequent work.

!!! warning "Wrong good/bad boundaries"
    If good is actually bad, bisect returns wrong commit. Verify boundaries first.

!!! warning "Bisect with flaky tests"
    Random failures mislead binary search. Stabilize test or run multiple times.

!!! warning "Shallow clone missing commits"
    `git fetch --unshallow` before bisect across long history.

## Best Practices

!!! tip "Automate with git bisect run"
    Manual bisect error-prone on >20 steps. Script the test.

!!! tip "Use tags for release boundaries"
    `git bisect good v1.4.0` clearer than SHA in incident docs.

!!! tip "Document bisect result in postmortem"
    Link first-bad commit to fix PR and root cause.

!!! tip "Add bisect helper to Makefile"
    `make bisect-good-release` standardizes test command for team.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Bisect cannot find commit | Too many skips | Reduce skips; widen good/bad range |
| Wrong commit identified | Flaky or wrong test | Fix test; re-run bisect |
| `fatal: Needed a single revision` | Invalid ref | Verify tag/SHA exists |
| Bisect stuck in loop | Inconsistent good/bad | Reset; verify test logic |
| Script always exits 125 | Misconfigured skip | Fix script exit codes |
| No commits to bisect | Good and bad adjacent | Already found; inspect good..bad |

## Summary

- **git bisect** binary-searches history between known good and bad commits
- Manual mode: mark **good**/**bad** after each test; automated: **git bisect run**
- Exit code **125** skips untestable commits; **0** good, non-zero bad for scripts
- Always **git bisect reset** when finished
- Essential for regression hunting in IaC, builds, and integration tests

## Interview Questions

1. How does git bisect work algorithmically?
2. What exit codes should a bisect test script use?
3. When would you use git bisect skip?
4. How many steps to bisect 1000 commits approximately?
5. What is git bisect run?
6. Why must you run git bisect reset after finishing?
7. What are limitations of bisect with flaky tests?
8. How do tags help bisect in release debugging?
9. How does shallow clone affect bisect?
10. Give a DevOps scenario where bisect saves significant time.

??? tip "Sample Answers (Questions 1 and 10)"

    **Q1 — Algorithm:** Bisect maintains a range of commits between known good and bad boundaries. It checks out the midpoint commit. If test passes, the bad commit must be later — shrink range to upper half. If fails, bad is in lower half. Repeat until the first bad commit is isolated. Complexity O(log n).

    **Q10 — DevOps scenario:** After weekly deploy, Terraform plan suddenly wants to destroy production RDS. Good state is last week's tag v2.3.0; bad is current main. Bisect with `terraform plan` exit code script finds the exact commit that changed module version or removed lifecycle block — hours of manual log review reduced to ~10 automated tests.

## Related Tutorials

- [Cherry-pick and Reflog](cherry-pick-and-reflog.md) *(previous)*
- [Git Hooks and Automation](git-hooks-and-automation.md) *(next — Module 6)*
- [Viewing History and Diffs](viewing-history-and-diffs.md)
- [Undoing Changes — Reset, Revert, and Stash](undoing-changes-reset-revert-stash.md)
- [Git – Category Overview](index.md)
- Cheat sheet: [Git Cheat Sheet](../cheatsheets/git.md)
- Interview prep: [Git Interview Prep](../interview/git.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [Pro Git Book – Debugging with Git](https://git-scm.com/book/en/v2/Git-Tools-Debugging-with-Git)
- [git bisect documentation](https://git-scm.com/docs/git-bisect)
- [Kernel.org – Bisecting regressions](https://www.kernel.org/doc/html/latest/process/debugging/gdb-kernel-debugging.html)
- [REBASH Academy – Git Overview](index.md)
