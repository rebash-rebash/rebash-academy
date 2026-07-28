---
title: "Git Cheat Sheet"
description: "Quick-reference commands and patterns for the REBASH Academy Git track."
difficulty: beginner
estimated_time: "10 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: cheatsheets
tags:
  - cheatsheets
  - git
comments: false
---

# Git Cheat Sheet

Scannable commands and patterns for the [Git track](../git/index.md). Prefer the full tutorials when you need *why*, not only *how*.

## Quick reference

| Area | Commands / notes |
|------|------------------|
| Daily | `git status -sb`; `git add -p`; `git commit`; `git push` |
| History | `git log --oneline --graph`; `git show`; `git diff` |
| Branch | `git switch -c`; `git switch`; `git branch -vv` |
| Sync | `git fetch`; `git pull --rebase`; `git push -u` |
| Undo | `git restore`; `git revert`; `git reset` (know soft/mixed/hard) |
| Stash | `git stash -u`; `git stash pop` |
| Remotes | `git remote -v`; `git push --force-with-lease` |
| Bisect | `git bisect start`; good/bad; `git bisect reset` |
| Hooks | `.git/hooks` / `core.hooksPath`; pre-commit pattern |
| Security | Signed commits; protect main; CODEOWNERS |

## Common mistakes

- Copy-pasting without reading expected output
- Skipping cleanup (leftover containers, state, or temp files)
- Mixing production credentials into lab shells

## Related

- Track: [Git](../git/index.md)
- Start: [Git introduction](../git/introduction-to-git-and-version-control.md)
- Interview bank: [Git interview prep](../interview/git.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)
