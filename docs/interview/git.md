---
title: "Git Interview Preparation"
description: "40 curated Git interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
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

## Core concepts

**1. Explain Git internals — what actually happens when you run git commit?**

??? success "Reveal answer"
    This question separates engineers who use Git from engineers who understand Git. The answer 
    reveals whether you truly know how Git works under the hood. 
    Git's object model: 
    Git stores everything as objects in the .git/objects/ directory. There are four types: 
    1. Blob — stores file content 
    2. Tree — stores directory structure (lists of blobs and trees) 
    3. Commit — stores a snapshot with metadata (author, timestamp, parent commit, tree) 
    4. Tag — stores an annotated reference to a commit 
    What happens on git commit: 
    git add src/app.py 
    git commit -m "feat: add user authentication" 
    Step 1: git add creates a blob object for src/app.py: 
    
     
    # Git hashes the content and stores it 
    echo "def authenticate(user): ..." | git hash-object -w --stdin 
    # Returns: a3f9b2c... (SHA-1 hash of content) 
    Step 2: git commit creates a tree object representing the directory structure: 
    tree abc123... 
    blob a3f9b2c... src/app.py 
    blob d8e4f1a... src/models.py 
    tree 9c3b2d1... tests/ 
    Step 3: Git creates a commit object: 
    commit 7e4a1b3... 
    tree abc123... (the root tree) 
    parent…

**2. What are the advantages of Git?**

??? success "Reveal answer"
    Speed: Git stores every update in the form of versions. For every version, it takes incremental backup
    (Snapshot) instead of taking the whole backup. Since it takes less space, Git is very fast.
    Parallel branching: We can create any number of branches as per our requirement without prior
    permission. Branching is for parallel development.
    Fully Distributed: A backup copy is available in multiple locations on each server (DVCS - Distributed
    Version Control System), so data can be recovered easily even if one server fails.

**3. What is the difference between Git merge and rebase?**

??? success "Reveal answer"
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    Git merge: One new merge commit is generated which has the history of both development branches.
    It preserves the history of both branches. Everyone can see that two branches were merged.
    Git rebase: Commits in the new branch are applied on top of the base branch tip. There is no merge
    commit. It appears as if you started working in one single branch from the beginning. This operation
    does NOT preserve the history of the new branch.

**4. What is the commit message in Git?**

??? success "Reveal answer"
    Every time we commit, we must give a commit message to identify each commit. The format differs
    from company to company. We can also use 'Tags' — a meaningful name given to a particular
    commit. Instead of referring to commit ID (40 alphanumeric characters), we refer to the tag, which
    internally points to the respective commit ID.
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    Configuration Management

**5. What is a rebase, and when would you use it instead of merging?**

??? success "Reveal answer"
    Rebase replays your commits on top of another branch's latest commits, producing a clean, linear history instead of
    the extra merge commits a regular merge creates. I use it to bring my feature branch up to date with main before
    opening a PR, but I avoid rebasing anything that's already been pushed and shared, since rewriting shared history
    causes real pain for collaborators.

**6. write down GIT commands which you use on daily basis and explain the cmds?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Git, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**7. Explain the concept of tags in GitLab.**

??? success "Reveal answer"
    Tags reference specific points in a repository's history, typically marking release versions or milestones. They're
    immutable snapshots of a particular commit, either annotated with extra information or lightweight, and are useful for
    managing releases and deployments.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    2
    7
    PYTHON FOR DEVOPS

**8. Explain your Git branching strategy. How do you deploy code from different branches to different environments?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Git components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**9. What is the difference between GitLab and GitHub?**

??? success "Reveal answer"
    GitLab bundles integrated CI/CD, issue tracking, and project management natively in one platform, making it well
    suited for full DevOps workflows, and offers strong self-hosting support. GitHub is more focused on
    social/open-source coding, with GitHub Actions adding CI/CD capability more recently, and primarily operates as a
    cloud service.

**10. What is Source Code Management?**

??? success "Reveal answer"
    It is a process through which we can store and manage any code. Developers write code, Testers
    write test cases and DevOps engineers write scripts. This code, we can store and manage in Source
    Code Management. Different teams can store code simultaneously. It saves all changes separately.
    We can retrieve this code at any point of time.

**11. What is Git and why we are using it and what is branching strategy?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**12. What is the difference between Git Merge and Git Rebase?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**13. what is git merge conflict?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**14. what are the types of branching stratergy u r using?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**15. What are the advantages of multibranch pipeline?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**16. What is the difference between git push --force-with-lease vs --force?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**17. What is the use of Git tags?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**18. What are the different types of branches in Git?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**19. what is the differences between git pull and git fetch?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**20. what is mean by git stash and pop?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**21. Explain the difference between Git Merge and Git Rebase?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**22. difference between git fetch and git pull?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**23. What is git branching strategy used in your organisation?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**24. What’s the difference between Git Merge and Rebase?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**25. Difference between Git pull and Git clone?**

??? success "Reveal answer"
    Git clone: For the first time if you want the whole central repository in your local server, we use git
    clone. It brings the entire repository to your local server.
    Git pull: Next time onwards you want only changes instead of the whole repository — in this case, we
    use Git pull (Incremental data).

**26. What is the difference between Git pull and Fetch?**

??? success "Reveal answer"
    Git fetch: Only brings changes from central repo to local repo, but these changes will NOT be
    integrated/merged to the local repo.
    Git merge: Merges the fetched changes to your local repository so you can see them.
    Git pull = Git fetch + Git merge (both operations happen internally).

**27. Can you explain the GitLab branching strategy?**

??? success "Reveal answer"
    A common approach is Git Flow -- Master/Main as the stable production version, Develop as the integration branch,
    feature branches created from Develop for specific work, release branches for preparing production releases, and
    hotfix branches for urgent fixes directly off Master.

## Scenarios and troubleshooting

**28. Explain the Git branching strategy you use in production environments.**

??? success "Reveal answer"
    A branching strategy is a set of rules about how your team creates, names, and merges branches.
    Without a clear strategy, teams end up with hundreds of mysterious branches, unclear release
    processes, and constant merge conflicts.
    The most commonly used strategies:
    1. Gitflow (Traditional, popular for versioned releases)
    main (production code — tagged releases only)
    develop (integration branch — all features merge here)
    |--- feature/user-login (developer A's work)
    |--- feature/payment-gateway (developer B's work)
    |--- release/v2.1 (release preparation)
    |--- hotfix/critical-bug (emergency production fix)
    # Creating a feature branch
    git checkout develop
    git checkout -b feature/user-authentication
    # Working on the feature...
    git add .
    
    git commit -m "feat: add JWT token validation"
    git commit -m "test: add unit tests for auth middleware"
    # Merge back to develop via Pull Request
    git checkout develop
    git merge --no-ff feature/user-authentication
    git branch -d feature/user-authentication
    # Create release branch when ready
    git checkout -b release/v2.1 develop
    # Bug fixes…

**29. What branching strategy do you follow, and how do you handle merges to avoid breaking the release branch? If a bug appears in production, what’s your approach to resolving it?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Git components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

## Practice questions

**30. How do you integrate GitHub with CI/CD tools?**

??? success "Reveal answer"
    GitHub can fire webhooks to tools like Jenkins or GitLab CI on events like a commit or pull request, or use its native
    GitHub Actions for built-in automation. For third-party tools, I authenticate using a personal access token or a GitHub
    App, and I use Docker images pulled from Docker Hub within pipelines to keep build environments consistent, with
    CI results reported back as PR status checks before a merge is allowed.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    0
    7
    GITHUB ACTIONS

**31. How do you resolve conflicts in Git?**

??? success "Reveal answer"
    Git flags the conflicting files, and I open each one to find the <<<<<<<, =======, >>>>>>> markers showing both
    versions. I edit the file to choose or combine the correct changes, remove the markers, stage the file with git add to
    mark it resolved, then complete the operation with git commit for a merge or git rebase --continue for a rebase, and
    finally push the resolved changes.

**32. A developer accidentally pushed a secret to GitHub. What do you do?**

??? success "Reveal answer"
    1. Immediately revoke the secret at the source (rotate the API key, change the password). 
    2) Remove from current code via new commit. 3) Purge from Git history (git filter-
    repo or BFG Repo Cleaner). 4) Force-push (only on non-protected branches). 5) Audit 
    access logs for unauthorized use during exposure window. 6) Enable secret scanning to 
    prevent recurrence.

**33. How do you set up GitHub runners for the application environment?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Git components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**34. How will you resolve the git conflict automatically?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Git components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**35. If someone force-pushed and lost the main branch, how do you recover it?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Git components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**36. How do you extract all git commits from last 3 days?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Git components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**37. How do you handle merge conflicts in GitLab?**

??? success "Reveal answer"
    Merge the conflicting branch into the current branch locally, use git merge or git rebase to resolve conflicts in an
    editor, commit the resolved changes, and push back to the repository -- or resolve conflicts directly through GitLab's
    web interface on the merge request.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**38. Diff between git fetch and git pull (what happens in background in depth)?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**39. diff between github repo and jfrog?**

??? success "Reveal answer"
    Start with a precise definition in the context of Git, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**40. Write a GitHub/GitLab pipeline to deploy a microservice with 3 services running in parallel?**

??? success "Reveal answer"
    Outline the solution first, then give a minimal correct example (commands or config sketch).
    
    Call out the production hardening you would add next (pin versions, least privilege, secrets, health checks) and how you would validate the result.

## Related

- Course: [Git](../git/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
