---
title: "Git Troubleshooting"
description: "Diagnose detached HEAD, authentication failures, and merge conflict recovery with repeatable drills for production Git incidents."
difficulty: intermediate
estimated_time: "55–70 min"
technology: git
category: git
module: "Module 16 · Troubleshooting"
learning_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - git
  - troubleshooting
  - recovery
prerequisites:
  - git/signed-commits-and-git-security
next:
  - git/git-bisect-and-debugging-history
related:
  - git/cherry-pick-and-reflog
  - git/merging-and-merge-conflicts
tags:
  - git
  - troubleshooting
  - detached-head
  - authentication
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---

# Git Troubleshooting

## Overview

Production Git incidents include **detached HEAD** after checking out a tag, **authentication failures** blocking CI push, half-finished **merges**, and **conflict recovery** after bad resolution. Systematic drills turn panic into checklists — the same mindset as SRE incident response.

This is **Tutorial 1** in **Module 16: Troubleshooting** of the REBASH Academy **Git & GitHub for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Signed Commits and Git Security](signed-commits-and-git-security.md)
- [Cherry-pick and Reflog](cherry-pick-and-reflog.md)
- [Merging and Merge Conflicts](merging-and-merge-conflicts.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Recognise and fix detached HEAD safely
- [ ] Diagnose SSH vs HTTPS authentication errors
- [ ] Abort or complete stuck merges and rebases
- [ ] Recover from bad conflict resolution using reflog
- [ ] Complete drills under `~/rebash-git/module-16`

## Architecture

HEAD may point to branch or raw commit; remotes require auth; merge/rebase state stored in `.git/MERGE_HEAD` etc.; reflog enables local recovery.

![Git workflow recovery paths](../assets/excalidraw/git-workflow.svg)

## Theory

### What it is

**Detached HEAD** means HEAD points directly to a commit, not a branch — new commits are unreachable unless you create a branch. **Authentication errors** stem from wrong keys, expired PATs, or missing `known_hosts`. **Stuck operations** leave MERGE_HEAD or rebase directories until `--continue`, `--abort`, or `--skip`. **Conflict recovery** may require aborting merge and restarting after fetching latest.

### Why it matters

CI jobs checking out tags for deploy often detach HEAD — scripts must not commit there. Midnight `git pull` failures block releases. Bad merge on `values.yaml` can take production offline — knowing abort/reset paths saves minutes in incidents.

### How it works

1. `git status` first — always.
2. Detached: `git switch -c rescue` or `git switch main`.
3. Auth: `ssh -T git@github.com`; check credential helper.
4. Merge stuck: `git merge --abort` or resolve + `git commit`.
5. Lost work: `git reflog` → `git reset --hard <good>`.

### Key concepts and comparisons

| Symptom | First command |
|---------|---------------|
| detached HEAD | git status |
| auth failed | ssh -T / gh auth status |
| merge conflict | git status; git diff |
| lost commits | git reflog |

| State file | Meaning |
|------------|---------|
| MERGE_HEAD | Merge in progress |
| rebase-merge/ | Rebase in progress |
| CHERRY_PICK_HEAD | Cherry-pick in progress |

### Common pitfalls

- Committing on detached HEAD without branch — commits orphaned until reflog rescue.
- `git push` after wrong merge resolution — deploys bad config.
- Repeated failed auth with same expired PAT — lockouts.
- Deleting `.git` as "fix" — nuclear data loss.

## Hands-on Lab

### Objective

Run three drills: detached HEAD rescue, auth diagnostics script, merge abort and redo — with evidence files.

### Prerequisites

- Git 2.x

### Lab environment

Workspace: `~/rebash-git/module-16`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-git/module-16 && cd ~/rebash-git/module-16
set -euo pipefail
```

### Real-world scenario

On-call runbook requires engineers to prove they can recover from common Git failure modes without calling senior help.

### Step-by-step tasks

#### Task 1 – Detached HEAD drill

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-git/module-16
set -euo pipefail
rm -rf trouble-lab
mkdir trouble-lab && cd trouble-lab
git init -b main
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
printf 'v1\n' > app.txt && git add app.txt && git commit -m 'v1'
git tag v1.0.0
git checkout v1.0.0
git status | tee ../detached-status.txt
grep -q 'detached HEAD' ../detached-status.txt
echo 'hotfix on tag' >> app.txt
git commit -am 'fix: hotfix on detached'
git switch -c hotfix/from-tag
git log --oneline -1 | tee ../detached-rescue.txt
grep -q 'hotfix on detached' ../detached-rescue.txt
cd ..
```

!!! example "Expected output"
    Detached state detected; branch `hotfix/from-tag` preserves commit.


#### Task 2 – Auth diagnostics script

Create `auth-diagnose.sh`:

```bash title="auth-diagnose.sh"
#!/usr/bin/env bash
set -euo pipefail
echo '=== git version ==='
git --version
echo '=== remote (if any) ==='
git -C trouble-lab remote -v 2>/dev/null || echo 'no_remote_configured'
echo '=== credential helper ==='
git config --global --get credential.helper 2>/dev/null || echo 'credential_helper=unset'
echo '=== ssh keys loaded ==='
ssh-add -l 2>/dev/null || echo 'ssh_agent=no_keys_or_agent'
echo '=== github ssh probe (may fail offline) ==='
ssh -T -o BatchMode=yes -o ConnectTimeout=5 git@github.com 2>&1 || true
echo 'diagnose_complete'
```

Run the script:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-git/module-16
set -euo pipefail
chmod +x auth-diagnose.sh
./auth-diagnose.sh | tee auth-diagnose.txt
grep -q 'diagnose_complete' auth-diagnose.txt
test "$(wc -l < auth-diagnose.txt)" -ge 8
cd ..
```

!!! example "Expected output"
    `auth-diagnose.txt` with Git version, credential, and SSH probe results.


#### Task 3 – Merge abort and recovery drill

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-git/module-16/trouble-lab
set -euo pipefail
git switch main
printf 'v2-main\n' > app.txt && git commit -am 'main advance'
git switch -c feature/conflict
printf 'v2-feature\n' > app.txt && git commit -am 'feature change'
git switch main
git merge feature/conflict || true
grep -q '<<<<<<<' app.txt
git merge --abort
grep -qv '<<<<<<<' app.txt || ! grep -q '<<<<<<<' app.txt
git show main:app.txt | tee ../post-abort-main.txt
grep -q 'v2-main' ../post-abort-main.txt
tar -czf ../module-16-trouble-evidence.tgz -C .. detached-status.txt post-abort-main.txt auth-diagnose.txt auth-diagnose.sh
ls -l ../module-16-trouble-evidence.tgz | tee ../trouble-evidence.txt
cd ..
```

!!! example "Expected output"
    Merge aborted; main content unchanged from bad merge.


### Validation steps

- [ ] Detached HEAD recognised and branched
- [ ] `auth-diagnose.sh` produced `auth-diagnose.txt`
- [ ] merge --abort restored clean main
- [ ] Evidence tarball exists

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| cannot switch branch | uncommitted changes | stash or commit |
| merge --abort fails | no merge | check MERGE_HEAD |
| orphan commit | detached no branch | reflog + branch |
| ssh permission denied | wrong key | fix ssh config |

### Challenge exercise

Start rebase, cause conflict, run `git rebase --abort`, verify original branch tip — capture `git log -1 --oneline` output in `REBASE_ABORT.txt`.

### Learning outcomes

- Rescued detached HEAD work on branch
- Ran auth diagnostics script with captured output
- Aborted bad merge safely

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
ls ~/rebash-git/module-16/
```

## Validation

- [ ] Lab under module-16
- [ ] Can explain detached HEAD
- [ ] Can list SSH auth checks
- [ ] Know merge --abort vs --continue

## Code Walkthrough

1. **git status** — every incident step zero.
2. **Never force-push main** — revert instead.
3. **reflog before panic** — local undo journal.
4. **Test SSH outside Git** — isolates auth vs repo issues.
5. **Document merge abort** — in incident ticket.

## Security Considerations

- Do not paste PATs into tickets while debugging auth
- Verify remote URL before push after auth fix
- Stolen credentials during incident — rotate immediately
- Recovery commits still need review before merge
- Limit break-glass force-push to named admins

## Common Mistakes

!!! warning "Commits on detached HEAD during tag deploy job"
    CI loses commits after job ends. **Fix:** checkout branch or create one in script.

!!! warning "Continuing merge with conflict markers"
    Broken YAML reaches prod. **Fix:** abort; fix properly; re-merge.

!!! warning "Deleting branch before merge abort"
    Harder to retry. **Fix:** abort first; reset state.

## Best Practices

- Pin runbooks in wiki linking `auth-diagnose.sh` output
- CI templates checkout branches not tags for build jobs needing commits
- Practice drills quarterly
- `git config --global merge.conflictstyle diff3` for clearer conflicts
- Alias `git undo` documented for team (reflog helper)

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| HEAD detached at vX.Y.Z | Tag checkout | switch -c or main |
| Permission denied publickey | SSH | ssh-add; config |
| HTTP 403 | PAT scope | regen token |
| MERGE_HEAD exists | Incomplete merge | abort or finish |
| rebase in progress | Interrupted | continue/abort |

## Summary

Most Git incidents yield to status, abort/continue discipline, and reflog — practise drills before production pressure. Next: [Git Bisect and Debugging History](git-bisect-and-debugging-history.md).

## Interview Questions

**1. What is detached HEAD?**

??? success "Reveal answer"
    HEAD references a commit directly rather than a branch name — commits made in this state are not on any branch until you create one or switch to existing branch.

**2. Fix detached HEAD after accidental tag checkout?**

??? success "Reveal answer"
    `git switch -c branch-name` to keep commits, or `git switch main` if no work to keep — use reflog if commits seem lost.

**3. merge --abort vs reset --hard during merge?**

??? success "Reveal answer"
    `--abort` safely cancels merge restoring pre-merge state; `--hard` is broader destructive reset — abort is preferred for in-progress merge only.

**4. SSH auth works locally but CI fails?**

??? success "Reveal answer"
    CI uses different credentials — check deploy keys, secrets, OIDC trust policy, and whether fork PR has secret access.

**5. How find if merge in progress?**

??? success "Reveal answer"
    `git status` says merging; existence of `.git/MERGE_HEAD`; unmerged paths listed.

**6. Recovery after bad conflict resolution pushed?**

??? success "Reveal answer"
    Revert merge commit on main or reset feature and redo merge after fetch — never force-push shared main; use forward fix revert.

**7. git fsck when?**

??? success "Reveal answer"
    Suspected repository corruption, shallow clone issues, or missing objects — low-level integrity check before reclone.

**8. Prevent detached HEAD in CI?**

??? success "Reveal answer"
    Checkout ref as branch (`ref: refs/heads/main`) or explicit `git switch -c ci-build` before commits needed for versioning.

## Related Tutorials

- [Cherry-pick and Reflog](cherry-pick-and-reflog.md)
- [Merging and Merge Conflicts](merging-and-merge-conflicts.md)
- [Git Bisect and Debugging History](git-bisect-and-debugging-history.md)
- [Course index](index.md)

## References

- [git-status](https://git-scm.com/docs/git-status)
- [GitHub SSH troubleshooting](https://docs.github.com/en/authentication/troubleshooting-ssh)
- [Pro Git — debugging](https://git-scm.com/book/en/v2/Git-Tools-Debugging-with-Git)
