---
title: "Git Bisect and Debugging History"
description: "Use git bisect with a scripted test to find the commit that introduced a regression in pipelines or IaC."
difficulty: advanced
estimated_time: "55–70 min"
technology: git
category: git
module: "Module 16 · Troubleshooting"
career_paths:
  - devops-engineer
  - site-reliability-engineer
  - platform-engineer
  - software-engineer
skills:
  - git
  - bisect
  - debugging
prerequisites:
  - git/git-troubleshooting
next:
  - git/production-git-practices
related:
  - git/viewing-history-and-diffs
  - git/cherry-pick-and-reflog
tags:
  - git
  - bisect
  - debugging
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---

# Git Bisect and Debugging History

## Overview

When CI broke "sometime last week," reading every commit is slow. **`git bisect`** performs a binary search between known good and bad commits, using a test script that returns pass/fail — finding the first bad commit in logarithmic time.

This is **Tutorial 2** in **Module 16: Troubleshooting** of the REBASH Academy **Git & GitHub for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Git Troubleshooting](git-troubleshooting.md)
- [Viewing History and Diffs](viewing-history-and-diffs.md)
- Git 2.x and bash

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Start bisect with good and bad SHAs or tags
- [ ] Automate bisect with `git bisect run` and exit codes
- [ ] Write a test script detecting regression in a config file
- [ ] Reset bisect state after completion
- [ ] Store evidence under `~/rebash-git/module-16`

## Architecture

Bisect checks out middle commit; test script returns 0 (good) or 1 (bad); Git narrows range until first bad commit identified.

![Git object model — commit search](../assets/excalidraw/git-object-model.svg)

## Theory

### What it is

**Git bisect** maintains a search range of commits. You mark ends as **good** and **bad**; Git checks out midpoint; you mark result until one commit remains — the introducer. **`git bisect run ./test.sh`** automates marking using script exit codes: 0 good, 1 bad, 125 skip.

### Why it matters

Pipeline regression from a merged Terraform change might span fifty commits. Bisect finds culprit in ~6 steps. First bad commit informs revert, cherry-pick fix to release branches, and postmortem.

### How it works

1. `git bisect start`
2. `git bisect bad` (current broken HEAD)
3. `git bisect good v1.0.0` (last known good tag)
4. `git bisect run ./test.sh`
5. Git prints first bad commit; `git bisect reset` cleans state.

### Key concepts and comparisons

| Command | Role |
|---------|------|
| bisect start | Begin session |
| bisect good/bad | Mark endpoints |
| bisect run | Automated search |
| bisect reset | End session |
| bisect skip | Untestable commit |

| Exit code (run) | Meaning |
|-----------------|---------|
| 0 | good |
| 1 | bad |
| 125 | skip |

### Common pitfalls

- Flaky test script — wrong commit blamed.
- Too wide range without tagged good baseline.
- Forgetting `bisect reset` — detached confusing state.
- Skipping too many commits — inconclusive result.

## Hands-on Lab

### Objective

Build commit history where commit #5 introduces invalid pipeline timeout; bisect run finds it automatically.

### Prerequisites

- Git 2.x
- bash

### Lab environment

Workspace: `~/rebash-git/module-16/bisect-lab`

```bash
mkdir -p ~/rebash-git/module-16/bisect-lab && cd ~/rebash-git/module-16/bisect-lab
set -euo pipefail
```

### Real-world scenario

Deploy pipeline started timing out after a series of merges. Last green tag `v-good`; current `main` fails — bisect locates commit that set `timeout: 0`.

### Step-by-step tasks

#### Task 1 – History with hidden bad commit

```bash
cd ~/rebash-git/module-16
set -euo pipefail
rm -rf bisect-lab
mkdir bisect-lab && cd bisect-lab
git init -b main
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
for i in 1 2 3 4 5 6 7 8; do
  if [ "$i" -eq 5 ]; then
    printf 'timeout: 0\n' > pipeline.env
  else
    printf 'timeout: 300\n' > pipeline.env
  fi
  git add pipeline.env
  git commit -m "commit $i: pipeline config"
done
git tag v-good HEAD~3
git log --oneline | tee ../bisect-log.txt
grep -q 'commit 8' ../bisect-log.txt
cd ..
```

**Expected output:** Eight commits; commit 5 has timeout 0; v-good on older good commit.

#### Task 2 – Test script and automated bisect

Create `test-timeout.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
val=$(grep -o '[0-9]*' pipeline.env | head -1)
if [ "${val:-0}" -ge 60 ]; then
  exit 0
else
  exit 1
fi
```

Run bisect:

```bash
cd ~/rebash-git/module-16/bisect-lab
set -euo pipefail
chmod +x test-timeout.sh
git bisect start
git bisect bad HEAD
git bisect good v-good
git bisect run ./test-timeout.sh | tee ../bisect-run-out.txt
FIRST_BAD=$(git bisect log 2>/dev/null | tail -5 || git log -1 --oneline)
git bisect reset
grep -q 'commit 5' ../bisect-run-out.txt || grep -q 'pipeline config' ../bisect-run-out.txt
cd ..
```

**Expected output:** Bisect identifies commit 5 as first bad; reset returns to main.

#### Task 3 – Evidence and verification

```bash
cd ~/rebash-git/module-16/bisect-lab
set -euo pipefail
git show HEAD~3:pipeline.env | tee ../good-file.txt
grep -q '300' ../good-file.txt
git log --oneline | head -8 | tee ../full-history.txt
tar -czf ../module-16-bisect-evidence.tgz -C .. bisect-run-out.txt bisect-log.txt
ls -l ../module-16-bisect-evidence.tgz | tee ../bisect-evidence.txt
cd ..
```

**Expected output:** Good tag file shows timeout 300; evidence archived.

### Validation steps

- [ ] Eight-commit history created
- [ ] bisect run completed
- [ ] First bad commit is #5
- [ ] bisect reset succeeded

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| only bad commits | good tag wrong | re-tag known good |
| script not executable | chmod | chmod +x |
| bisect still active | no reset | git bisect reset |
| skip too many | flaky test | fix script determinism |

### Challenge exercise

Introduce skip case: one commit deletes `pipeline.env` — extend script to exit 125 when file missing; rerun bisect.

### Learning outcomes

- Built reproducible good/bad history
- Automated bisect with shell test
- Reset bisect cleanly

### Cleanup

```bash
cd ~/rebash-git/module-16/bisect-lab && git bisect reset 2>/dev/null || true
```

## Validation

- [ ] Lab under module-16/bisect-lab
- [ ] Can explain binary search benefit
- [ ] Know bisect run exit codes
- [ ] Can name CI regression use case

## Code Walkthrough

1. **Tag last green deploy** — bisect needs trustworthy good ref.
2. **Deterministic test** — same result on same commit.
3. **Run in CI sparingly** — expensive; reproduce locally first.
4. **Document first bad SHA** — in incident ticket.
5. **Revert or fix forward** — after identification.

## Security Considerations

- Bisect checks out old commits — ensure test script does not exfiltrate data
- Do not bisect public untrusted repos with arbitrary scripts from repo
- Old commits may contain since-rotated secrets — handle logs carefully
- CI bisect needs clean runner each step
- Verify test does not mutate production

## Common Mistakes

!!! warning "Manual bisect marking wrong"
    Human error mislabels good/bad. **Fix:** Prefer `bisect run` automation.

!!! warning "Good commit not actually good"
    Search fails. **Fix:** Validate tag with test script before start.

!!! warning "Leaving bisect active"
    Confuses later git commands. **Fix:** Always `bisect reset`.

## Best Practices

- Keep test script in repo under `scripts/` for reuse
- Combine bisect with `git show` on result commit
- For flaky CI, bisect on deterministic unit test not e2e
- Record bisect log in postmortem
- Use `--` path limit if only subdirectory relevant

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| bisect inconclusive | all skip | widen good/bad |
| wrong commit blamed | test not tied to bug | improve test |
| cannot checkout | dirty tree | stash |
| slow | huge history | narrow date range first |

## Summary

Bisect turns "when did it break?" into a scripted binary search — essential for regression hunting. Next: [Production Git Practices](production-git-practices.md).

## Interview Questions

**1. How bisect complexity vs linear scan?**

??? success "Reveal answer"
    Bisect is O(log n) commits tested vs O(n) linear — roughly 10 steps for thousand commits.

**2. git bisect run exit codes?**

??? success "Reveal answer"
    0 marks current good, 1 bad, 125 skip untestable commit — script must be deterministic.

**3. When skip a commit?**

??? success "Reveal answer"
    Commit does not build, missing file, or test irrelevant — bisect tries another point; too many skips fail search.

**4. Bisect vs blame?**

??? success "Reveal answer"
    Blame finds who last touched a line; bisect finds which commit introduced failing behaviour using good/bad test — different questions.

**5. Good ref for production regression?**

??? success "Reveal answer"
    Last successful deploy tag or CI-green commit on main — must genuinely pass the same test used in bisect run.

**6. After finding bad commit?**

??? success "Reveal answer"
    Inspect diff with git show, revert or fix, cherry-pick to release branches if needed, improve test coverage to catch earlier.

**7. Bisect on merge commits?**

??? success "Reveal answer"
    Works but complex history — may need first-parent bisect or bisect on linearized main (squash merge repos easier).

**8. Automate in CI?**

??? success "Reveal answer"
    Possible on nightly with known range when local reproduction hard — costly; ensure ephemeral clean checkout each step.

## Related Tutorials

- [Git Troubleshooting](git-troubleshooting.md)
- [Viewing History and Diffs](viewing-history-and-diffs.md)
- [Cherry-pick and Reflog](cherry-pick-and-reflog.md)
- [Course index](index.md)

## References

- [git-bisect](https://git-scm.com/docs/git-bisect)
- [Pro Git — bisect](https://git-scm.com/book/en/v2/Git-Tools-Debugging-with-Git#_binary_search)
