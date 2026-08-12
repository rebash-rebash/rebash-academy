---
title: "Git Interview Preparation"
description: "39 curated Git interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: git
tags:
  - interview
  - git
comments: false
---

{% raw %}
# Git Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

<div class="ra-interview-qa" markdown="1">

## Core concepts

**1. Explain Git internals — what actually happens when you run git commit?**

??? success "Reveal answer"
    **In short:** A commit stores a snapshot tree plus metadata and points `HEAD` at a new commit object.
    
    **Key points**
    
    - Git hashes blobs (files), trees (directories), and the commit object.
    - `git add` stages content into the index; `git commit` freezes that tree.
    - The commit references parent(s), author, and message.
    
    **Try this**
    
    - `git cat-file -t HEAD`
    - `git log -1 --pretty=raw`
    
    **Trap**
    
    - Thinking commits store diffs only — Git stores snapshots (deltas are pack optimisation).

**2. What are the advantages of Git?**

??? success "Reveal answer"
    **In short:** Git is distributed, fast, and excellent at branching/merging with a full local history.
    
    **Key points**
    
    - Every clone is a full repository — commits work offline.
    - Cheap branches encourage small, reviewable changes.
    - Cryptographic hashes give integrity and traceability.
    - Integrates cleanly with CI and code review.
    
    **Try this**
    
    - `git status`
    - `git log --oneline --graph -10`
    
    **Trap**
    
    - Using Git as a file backup tool without reviews, tests, or branch protection.

**3. What is the difference between Git merge and rebase?**

??? success "Reveal answer"
    **In short:** Merge joins histories with a merge commit; rebase replays your commits onto another tip for a linear history.
    
    **Key points**
    
    - Merge preserves exact branching context — safer for shared branches.
    - Rebase rewrites commits — great for cleaning local work before push.
    - Never rebase commits already shared unless the team agrees.
    
    **Try this**
    
    - `git merge main`
    - `git rebase main`
    
    **Trap**
    
    - Rebasing `main` that others already pulled — force-push pain for everyone.

**4. What is the commit message in Git?**

??? success "Reveal answer"
    **In short:** A commit message explains why the change exists — it is part of the audit trail.
    
    **Key points**
    
    - Subject line short and imperative; body for context and risk.
    - Reference tickets/incidents when relevant.
    - Good messages make `git bisect` and reviews faster.
    
    **Try this**
    
    - `git commit -m "Fix nil pointer in checkout retry path"`
    
    **Trap**
    
    - Messages like `fix` or `updates` that teach future you nothing.

**5. What is a rebase, and when would you use it instead of merging?**

??? success "Reveal answer"
    **In short:** Rebase moves your commit series onto a new base so history stays linear.
    
    **Key points**
    
    - Use on local feature branches before opening a merge request.
    - Prefer merge for long-lived shared branches.
    - Resolve conflicts commit-by-commit during rebase.
    
    **Try this**
    
    - `git fetch origin`
    - `git rebase origin/main`
    
    **Trap**
    
    - Interactive rebase on a branch five people are pushing to.

**6. Write down GIT commands which you use on daily basis and explain the cmds?**

??? success "Reveal answer"
    **In short:** Daily Git is status, branch, add, commit, pull/rebase, push, log, and diff.
    
    **Key points**
    
    - `git status`/`diff` before every commit.
    - `git switch -c feature/…` for work; `git pull --rebase` on personal branches.
    - `git log --oneline --graph` to understand history.
    - `git restore` / `git revert` for safe undos.
    
    **Try this**
    
    - `git status`
    - `git switch -c feature/x`
    - `git pull --rebase`
    - `git push -u origin HEAD`
    
    **Trap**
    
    - Force-pushing to shared branches as a habit.

**7. Explain the concept of tags in GitLab.**

??? success "Reveal answer"
    **In short:** Tags mark immutable points — usually releases — and GitLab surfaces them on pipelines and releases.
    
    **Key points**
    
    - Annotated tags store message/tagger; lightweight tags are just names.
    - CI often builds on `v*` tags for release artefacts.
    - Protect release tags like release branches.
    
    **Try this**
    
    - `git tag -a v1.2.0 -m 'Release 1.2.0'`
    - `git push origin v1.2.0`
    
    **Trap**
    
    - Moving a published tag to a different commit — breaks consumers quietly.

**8. Explain your Git branching strategy. How do you deploy code from different branches to different environments?**

??? success "Reveal answer"
    **In short:** Use trunk-based or GitHub Flow style: short-lived feature branches, protected `main`, environment deploys from tags or release branches.
    
    **Key points**
    
    - Dev deploys from merge to `develop` or auto-deploy previews.
    - Staging/prod deploy from tagged commits or `release/*`.
    - Promote the same artefact — do not rebuild differently per environment.
    
    **Try this**
    
    - Protect main + require PR checks
    - Deploy artefact by Git SHA/tag
    
    **Trap**
    
    - Building a “special prod binary” that never ran in staging.

**9. What is the difference between GitLab and GitHub?**

??? success "Reveal answer"
    **In short:** GitHub and GitLab are both Git hosts with PRs/MRs, CI, and permissions — differing mainly in product packaging.
    
    **Key points**
    
    - GitLab often bundles built-in CI/CD and package registry tightly.
    - GitHub centres Actions + a huge ecosystem of apps.
    - Choose on SSO, compliance, CI model, and where your org already lives.
    
    **Try this**
    
    - Compare: MR/PR checks, runners, package registry, security scanning
    
    **Trap**
    
    - Treating the host as the VCS — Git is the VCS; they are platforms on top.

**10. What is Source Code Management?**

??? success "Reveal answer"
    **In short:** Source Code Management (SCM) is versioning, branching, review, and access control for code.
    
    **Key points**
    
    - Git is the dominant distributed SCM tool.
    - Platforms add PRs, protections, and audit logs.
    - SCM is the backbone of CI/CD and change traceability.
    
    **Try this**
    
    - `git init`
    - `git remote -v`
    
    **Trap**
    
    - Storing production secrets inside the SCM history.

**11. What is Git and why we are using it and what is branching strategy?**

??? success "Reveal answer"
    **In short:** Git tracks snapshots so teams can branch safely; a branching strategy defines how work reaches production.
    
    **Key points**
    
    - Why Git: history, collaboration, bisect, and CI hooks.
    - Strategy examples: trunk-based, GitHub Flow, GitFlow (heavier).
    - Protect release lines; keep feature branches short-lived.
    
    **Try this**
    
    - `git switch -c feature/login`
    - `git merge --no-ff`
    
    **Trap**
    
    - Long-lived feature branches that drift for months.

**12. What is the difference between Git Merge and Git Rebase?**

??? success "Reveal answer"
    **In short:** Merge creates a join commit; rebase rewrites commits onto another base.
    
    **Key points**
    
    - Same technical trade-off as Q3 — say it clearly once.
    - Merge is non-destructive history; rebase is history editing.
    - Team policy decides which is default on `main`.
    
    **Try this**
    
    - `git merge feature`
    - `git rebase main`
    
    **Trap**
    
    - Mixing both randomly with no team convention.

**13. What is git merge conflict?**

??? success "Reveal answer"
    **In short:** A merge conflict means overlapping edits Git cannot auto-combine — humans must choose.
    
    **Key points**
    
    - Markers `<<<<<<<` / `=======` / `>>>>>>>` show both sides.
    - Edit, `git add`, then continue merge/rebase.
    - Reduce conflicts with smaller PRs and frequent integration.
    
    **Try this**
    
    - `git status`
    - `git diff`
    - `git add <file>; git merge --continue`
    
    **Trap**
    
    - Accepting “theirs” blindly without understanding behaviour changes.

**14. What are the advantages of multibranch pipeline?**

??? success "Reveal answer"
    **In short:** A multibranch pipeline discovers branches/PRs and runs the matching Jenkinsfile automatically.
    
    **Key points**
    
    - Each branch gets isolation and its own build history.
    - PR validation runs before merge.
    - Old branches can auto-prune to save executors.
    
    **Try this**
    
    - Jenkins Multibranch → scan repository
    
    **Trap**
    
    - Building every stale branch forever and burning CI capacity.

**15. What is the difference between git push**

??? success "Reveal answer"
    **In short:** `git push` publishes local commits to a remote branch — incomplete interview prompts usually mean push vs pull/fetch.
    
    **Key points**
    
    - Push updates remote refs if fast-forward (or allowed force) rules pass.
    - Upstream tracking (`-u`) links local and remote branches.
    - Protected branches reject direct pushes.
    
    **Try this**
    
    - `git push -u origin HEAD`
    - `git push --dry-run`
    
    **Trap**
    
    - Force-pushing to `main` without recovery notes.

**16. What is the use of Git tags?**

??? success "Reveal answer"
    **In short:** Tags label important commits — usually versioned releases — for humans and CI.
    
    **Key points**
    
    - Prefer annotated tags for releases.
    - CI can gate release jobs on tag patterns.
    - Tags should be immutable once published.
    
    **Try this**
    
    - `git tag -l`
    - `git show v1.2.0`
    
    **Trap**
    
    - Using a branch named `v1.2.0` instead of a tag and letting it drift.

**17. What are the different types of branches in Git?**

??? success "Reveal answer"
    **In short:** Common branch types: long-lived integration (`main`/`develop`), short feature, release, and hotfix.
    
    **Key points**
    
    - Feature branches carry work-in-progress.
    - Release branches freeze scope for hardening.
    - Hotfix branches patch production and merge back.
    
    **Try this**
    
    - `git branch -a`
    
    **Trap**
    
    - Treating every branch as long-lived — review lag explodes.

**18. What is the differences between git pull and git fetch?**

??? success "Reveal answer"
    **In short:** `git fetch` updates remote-tracking refs; `git pull` fetches and then integrates (merge or rebase).
    
    **Key points**
    
    - Fetch is safe inspection; pull changes your working branch.
    - Many teams prefer `fetch` + explicit rebase/merge.
    - Configure `pull.rebase` deliberately.
    
    **Try this**
    
    - `git fetch origin`
    - `git pull --rebase`
    
    **Trap**
    
    - Blind `git pull` on a dirty worktree mid-incident.

**19. What is mean by git stash and pop?**

??? success "Reveal answer"
    **In short:** `git stash` shelves local changes; `stash pop` reapplies and drops that stash entry.
    
    **Key points**
    
    - Useful to switch branches quickly with unfinished work.
    - `stash apply` keeps the stash; `pop` removes it if clean.
    - Include untracked files with `-u` when needed.
    
    **Try this**
    
    - `git stash push -m 'wip'`
    - `git stash list`
    - `git stash pop`
    
    **Trap**
    
    - Popping a stash into the wrong branch and committing the mess.

**20. Explain the difference between Git Merge and Git Rebase?**

??? success "Reveal answer"
    **In short:** Merge preserves parallel history; rebase replays commits for a straight line — pick by collaboration needs.
    
    **Key points**
    
    - Shared branches → merge.
    - Local cleanup before PR → rebase.
    - Say conflict cost and review clarity out loud in interviews.
    
    **Try this**
    
    - `git log --oneline --graph --decorate -15`
    
    **Trap**
    
    - Rewriting published history to “make the graph pretty”.

**21. Difference between git fetch and git pull?**

??? success "Reveal answer"
    **In short:** Fetch downloads objects/refs; pull also merges/rebases into your current branch.
    
    **Key points**
    
    - After fetch, compare with `git log HEAD..origin/main`.
    - Pull is convenience; fetch gives control.
    - Same idea as Q18 — keep the wording crisp.
    
    **Try this**
    
    - `git fetch origin`
    - `git log --oneline HEAD..origin/main`
    
    **Trap**
    
    - Assuming fetch updates your working tree files — it does not.

**22. What is git branching strategy used in your organisation?**

??? success "Reveal answer"
    **In short:** State the strategy you actually use — usually short-lived features into a protected trunk with CI gates.
    
    **Key points**
    
    - Name environments and how artefacts promote.
    - Mention required reviews and status checks.
    - Hotfix path: branch from release tag, patch, deploy, merge back.
    
    **Try this**
    
    - Document: branch → PR → CI → squash/merge → deploy
    
    **Trap**
    
    - Describing GitFlow in detail when your team is trunk-based (or the reverse).

**23. What’s the difference between Git Merge and Rebase?**

??? success "Reveal answer"
    **In short:** Merge creates a join; rebase rewrites onto a new base — same core distinction again.
    
    **Key points**
    
    - Interviewers repeat this to check consistency under pressure.
    - Lead with when you choose each, not only definitions.
    - Call out the never-rebase-public-commits rule.
    
    **Try this**
    
    - `git merge --no-ff feature`
    - `git rebase -i main`
    
    **Trap**
    
    - Force-push after rebase without coordinating with co-authors.

**24. Difference between Git pull and Git clone?**

??? success "Reveal answer"
    **In short:** `git clone` creates a new local repo from a remote; `git pull` updates an existing repo’s current branch.
    
    **Key points**
    
    - Clone once; pull/fetch many times.
    - Clone sets `origin` remotes by default.
    - Shallow clones (`--depth`) trade history for speed in CI.
    
    **Try this**
    
    - `git clone <url>`
    - `git pull --rebase`
    
    **Trap**
    
    - Re-cloning to “fix” conflicts instead of understanding the branch state.

**25. What is the difference between Git pull and Fetch?**

??? success "Reveal answer"
    **In short:** Pull = fetch + integrate; fetch alone updates remote-tracking branches only.
    
    **Key points**
    
    - Use fetch to inspect upstream safely.
    - Integrate deliberately with merge or rebase.
    - Keep worktrees clean before integrating.
    
    **Try this**
    
    - `git fetch -p`
    - `git merge --ff-only origin/main`
    
    **Trap**
    
    - Pulling with local uncommitted changes and creating a tangle.

**26. Can you explain the GitLab branching strategy?**

??? success "Reveal answer"
    **In short:** GitLab branching strategy is usually protected `main`/`master`, short feature branches, MRs with pipelines, and tags for release.
    
    **Key points**
    
    - Environment branches are optional — prefer deploy-by-tag.
    - Use MR approvals + protected branches.
    - Hotfixes branch from the production tag.
    
    **Try this**
    
    - Protect main in GitLab settings
    - Tag release and deploy that SHA
    
    **Trap**
    
    - Pushing straight to `main` because “the pipeline is slow”.

## Scenarios and troubleshooting

**27. Explain the Git branching strategy you use in production environments.**

??? success "Reveal answer"
    **In short:** In production, keep `main` releasable, integrate small MRs, and promote immutable artefacts.
    
    **Key points**
    
    - Feature flags beat long-lived branches for incomplete work.
    - Release from tags; record the SHA in change tickets.
    - Automate rollback to the previous tag.
    
    **Try this**
    
    - `git tag vX.Y.Z`
    - Deploy by digest/SHA, not `latest`
    
    **Trap**
    
    - Deploying directly from a developer laptop outside the pipeline.

**28. What branching strategy do you follow, and how do you handle merges to avoid breaking the release branch? If a bug appears in production, what’s your approach to resolving it?**

??? success "Reveal answer"
    **In short:** Protect the release branch with PR/MR-only merges; for prod bugs, cut a hotfix from the release tag and merge back to trunk.
    
    **Key points**
    
    - Require CI + reviews on release lines.
    - Hotfix → patch → deploy → merge into `main` to avoid reintroducing the bug.
    - Use `git revert` for safe undo on shared history.
    
    **Try this**
    
    - `git switch -c hotfix/pay-timeout v1.4.2`
    - `git revert <sha>`
    
    **Trap**
    
    - Patching prod with an unreviewed commit that never returns to `main`.

## Practice questions

**29. How do you integrate GitHub with CI/CD tools?**

??? success "Reveal answer"
    **In short:** Connect GitHub to CI via webhooks/Apps: push and PR events trigger workflows that build, test, and deploy.
    
    **Key points**
    
    - GitHub Actions reads `.github/workflows/*.yml`.
    - External CI (Jenkins/TeamCity) uses the GitHub App or webhooks + checks API.
    - Store secrets in the platform, not the repo.
    
    **Try this**
    
    - Push a workflow file
    - Require checks before merge
    
    **Trap**
    
    - Personal access tokens in repo variables with broad org scope.

**30. How do you resolve conflicts in Git?**

??? success "Reveal answer"
    **In short:** Resolve conflicts by inspecting both sides, choosing the correct behaviour, then marking files resolved.
    
    **Key points**
    
    - Use `git status` to list unmerged paths.
    - Edit conflict markers carefully; run tests.
    - Prefer smaller PRs and frequent merges to reduce pain.
    
    **Try this**
    
    - `git status`
    - `git add <resolved>`
    - `git merge --continue`
    
    **Trap**
    
    - Resolving markers but forgetting to delete one side’s leftover code.

**31. A developer accidentally pushed a secret to GitHub. What do you do?**

??? success "Reveal answer"
    **In short:** Rotate the secret immediately, revoke it at the provider, then purge it from Git history and caches.
    
    **Key points**
    
    - Treat the secret as burned the moment it was pushed.
    - Use `git filter-repo`/BFG and force-push only with coordinated recovery.
    - Invalidate GitHub caches, forks, and CI logs if they captured it.
    - Add secret scanning and pre-commit hooks afterwards.
    
    **Try this**
    
    - Revoke key at provider first
    - `git filter-repo or BFG to purge history`
    
    **Trap**
    
    - Only deleting the file in a new commit — the secret remains in history.

**32. How do you set up GitHub runners for the application environment?**

??? success "Reveal answer"
    **In short:** Runners are the machines/containers that execute GitHub Actions jobs — hosted or self-hosted per environment needs.
    
    **Key points**
    
    - Self-hosted runners need labels, isolation, and auto-update strategy.
    - Scope registration to the repo/org; lock down network and secrets.
    - Ephemeral runners reduce persistence risk.
    
    **Try this**
    
    - Register runner with a short-lived token
    - Pin labels like env=prod,size=large
    
    **Trap**
    
    - Shared long-lived runners that can reach prod and build untrusted PRs.

**33. How will you resolve the git conflict automatically?**

??? success "Reveal answer"
    **In short:** You generally should not auto-resolve semantic conflicts — automate only mechanical cases with clear rules.
    
    **Key points**
    
    - Automerge bots can resolve lockfile-only or ours/theirs for generated files.
    - Behavioural code conflicts need a human.
    - CI must still validate after any auto-resolution.
    
    **Try this**
    
    - Use CODEOWNERS + required checks
    - Limit auto-resolve to generated paths
    
    **Trap**
    
    - Teaching a bot to always take “ours” on application code.

**34. If someone force-pushed and lost the main branch, how do you recover it?**

??? success "Reveal answer"
    **In short:** Recover a force-pushed `main` from reflogs, remote backups, open MRs, or another clone that still has the old tip.
    
    **Key points**
    
    - `git reflog` on any machine that had the old commits.
    - GitHub may still show the previous SHA in events/checks.
    - Force-push the recovered tip back with team coordination.
    
    **Try this**
    
    - `git reflog`
    - `git push --force-with-lease origin <good-sha>:main`
    
    **Trap**
    
    - Running random resets without capturing the good SHA first.

**35. How do you extract all git commits from last 3 days?**

??? success "Reveal answer"
    **In short:** List recent commits with `git log` bounded by date or relative time.
    
    **Key points**
    
    - `git log --since='3 days ago' --pretty=…`.
    - Add `--author` or path filters as needed.
    - For automation, prefer ISO dates and machine-readable format.
    
    **Try this**
    
    - `git log --since='3 days ago' --pretty=format:'%h %ad %s' --date=short`
    
    **Trap**
    
    - Trusting local timezone defaults when auditors want UTC.

**36. How do you handle merge conflicts in GitLab?**

??? success "Reveal answer"
    **In short:** In GitLab, resolve conflicts locally or in the MR UI, then push the merge commit/rebase result.
    
    **Key points**
    
    - Fetch the source/target branches, merge/rebase, fix, push.
    - Pipelines must go green after resolution.
    - Maintainers can merge when policy allows.
    
    **Try this**
    
    - `git fetch origin`
    - `git merge origin/main`
    - `git push`
    
    **Trap**
    
    - Resolving in the UI without running tests for non-trivial code.

**37. Diff between git fetch and git pull (what happens in background in depth)?**

??? success "Reveal answer"
    **In short:** Fetch updates `refs/remotes` and object DB; pull then merges/rebases those commits into your branch tip.
    
    **Key points**
    
    - Fetch negotiates missing objects and updates remote-tracking refs only.
    - Pull’s second step rewrites your branch pointer and maybe worktree.
    - Fast-forward vs recursive merge vs rebase are the integrate choices.
    
    **Try this**
    
    - `git fetch origin`
    - `git merge --ff-only origin/main`
    
    **Trap**
    
    - Believing fetch and pull are synonyms in production ops.

**38. Diff between github repo and jfrog?**

??? success "Reveal answer"
    **In short:** A GitHub repo stores versioned source and collaboration; JFrog Artifactory stores built artefacts and dependencies.
    
    **Key points**
    
    - Git ≠ binary artefact registry (though Git LFS exists).
    - CI pulls code from Git, pushes images/packages to JFrog/ECR/etc.
    - Promotion policies belong in the artefact registry.
    
    **Try this**
    
    - Code in GitHub; images/packages in Artifactory
    
    **Trap**
    
    - Checking large binaries into Git instead of the registry.

**39. Write a GitHub/GitLab pipeline to deploy a microservice with 3 services running in parallel?**

??? success "Reveal answer"
    **In short:** Run three deploy jobs in parallel after a shared build/test stage, each targeting one microservice.
    
    **Key points**
    
    - GitHub Actions: one workflow with three deploy jobs sharing `needs: build`.
    - GitLab: `parallel` matrix or three jobs with the same stage.
    - Pass the same artefact versions; fail the pipeline if any deploy fails.
    
    **Try this**
    
    - GitHub Actions: jobs.build then jobs.deploy-a/b/c with needs: build
    - GitLab: stage deploy with three jobs, no inter-needs
    
    **Trap**
    
    - Parallel deploys that each rebuild different SHAs — you lose release consistency.

## Related
- Course: [Git](../git/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
