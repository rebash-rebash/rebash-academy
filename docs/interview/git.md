---
title: "Git Interview Preparation"
description: "40 curated interview questions and model answers for Git — concepts, scenarios, troubleshooting, and production trade-offs."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. What is a Pull Request / Merge Request, and how do you structure an effective code review process?**

??? success "Reveal answer"
    A Pull Request (GitHub) or Merge Request (GitLab) is a formal request to merge changes from 
    one branch into another. It's not just a technical operation — it's a communication tool, a quality 
    gate, and a knowledge-sharing mechanism. 
    Anatomy of a good PR: 
    ## Summary 
    Adds Redis-based caching for user profile API responses. 
    Reduces average response time from 450ms to 12ms for repeat requests. 
    ## Changes Made 
    - Added Redis client initialization in `src/cache/redis.go` 
    - Wrapped user profile endpoint with cache middleware 
    - Added cache invalidation on profile updates 
    - Cache TTL: 5 minutes (configurable via env var CACHE_TTL_SECONDS) 
    ## Testing 
    - Unit tests: `go test ./...` (all passing) 
    - Load test: ran k6 against staging, P99 latency dropped 96% 
    - Manual test: verified cache invalidation when profile updated 
    ## Screenshots / Evidence 
    [Screenshot of Grafana showing latency improvement] 
    ## Potential Concerns 
    
     
    - Cache stampede possible under high load — added lock mechanism 
    - Memory usage on Redis will increase ~50MB for 10k active users 
    ##…

**2. Explain Git internals — what actually happens when you run git commit?**

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

**3. Can you explain Git branching strategies (Git Flow, Trunk-Based Development)?**

??? success "Reveal answer"
    Git Flow uses several long-lived branches -- main for production, develop for ongoing work, feature branches for new
    work, release branches cut from develop, and hotfix branches from main for urgent fixes -- which suits teams with
    scheduled releases. Trunk-based development has developers committing small, frequent changes directly to a
    shared trunk with short-lived feature branches, which fits CI/CD-heavy teams shipping continuously. GitHub Flow
    and feature branching are lighter-weight variants in between, emphasizing short-lived branches and pull requests.
    KEY POINTS TO MENTION
    • Git Flow: main/develop/feature/release/hotfix — scheduled releases
    • Trunk-based: frequent small commits to trunk — continuous deployment
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**4. What is Git?**

??? success "Reveal answer"
    Git is one of the Source Code Management tools where we can store any type of code. Git is the most
    advanced tool in the market now. We also call Git a version control system because every update is
    stored as a new version. At any point of time, we can get any previous version. Every version will have
    a unique number called commit-ID. By using this commit ID, we can track each change i.e. who did
    what at what time. For every version, it takes incremental backup instead of taking the whole backup.
    That's why Git occupies less space and is very fast.

**5. What are the advantages of Git?**

??? success "Reveal answer"
    Speed: Git stores every update in the form of versions. For every version, it takes incremental backup
    (Snapshot) instead of taking the whole backup. Since it takes less space, Git is very fast.
    Parallel branching: We can create any number of branches as per our requirement without prior
    permission. Branching is for parallel development.
    Fully Distributed: A backup copy is available in multiple locations on each server (DVCS - Distributed
    Version Control System), so data can be recovered easily even if one server fails.

**6. What are the stages in Git?**

??? success "Reveal answer"
    There are total of 4 stages in Git:
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    • Workspace: Place where we create and modify files physically.
    • Staging area/Indexing area: Buffer zone between workspace and local repository where Git takes
    a snapshot for each version.
    • Local repository: Hidden directory where Git stores all commits locally. Every commit has a
    unique commit ID.
    • Central repository: Place where Git stores all commits centrally (e.g., GitHub). Used for storing
    and sharing code with the team.

**7. What is the difference between Git merge and rebase?**

??? success "Reveal answer"
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    Git merge: One new merge commit is generated which has the history of both development branches.
    It preserves the history of both branches. Everyone can see that two branches were merged.
    Git rebase: Commits in the new branch are applied on top of the base branch tip. There is no merge
    commit. It appears as if you started working in one single branch from the beginning. This operation
    does NOT preserve the history of the new branch.

**8. What are the benefits of using version control systems like Git?**

??? success "Reveal answer"
    Collaboration without overwriting each other's work, a full history of every change with who made it and when,
    branching and merging so features can be developed independently, a remote backup so local loss isn't
    catastrophic, the ability to revert to any previous version, and pull-request-based code review before anything
    merges into the main codebase.
    KEY POINTS TO MENTION
    • Collaboration, tracked history, branching/merging, backup, version rollback, PR-based review

**9. What is the difference between Git and SVN?**

??? success "Reveal answer"
    • SVN: Centralized version control system (CVCS) — backup copy in only one central repository.
    No branching strategy, no parallel development. No local repository — every change must be
    pushed to central repository immediately.
    • Git: Distributed version control system (DVCS) — backup copy available on everyone's machine
    and central repository. Can create any number of branches for parallel development. Has local
    repository — save changes locally and push at the end.

**10. What is GitHub?**

??? success "Reveal answer"
    GitHub is a central Git repository where we can store code centrally. GitHub belongs to Microsoft
    Company. We can create any number of repositories in GitHub. All public repositories are free and
    accessible by everyone. Private repositories restrict public access for security. We can copy a
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    repository from one account to another — this process is called 'Fork'. The default branch is 'Master'.

**11. What is Git hooks?**

??? success "Reveal answer"
    Git hooks (also called web hooks) are configuration files that come by default when you install Git.
    These files are used to set some permissions and notifications. There are two types:
    • Pre-commit hooks: Restrict team members to follow a certain pattern while giving commit
    messages before allowing them to commit.
    • Post-commit hooks: Send email notifications to managers regarding every commit that occurs in a
    central repository.

**12. What is the common branching strategy in Git?**

??? success "Reveal answer"
    • Product is the same, so one repo — but different features
    • Each feature has one separate branch
    • Finally, merge (code) all branches
    • For Parallel development — can create any no of branches
    • Can create one branch on the basis of another branch
    • Changes are personal to that particular branch
    • The default branch is 'Master'
    • Files created in a workspace will be visible in any branch workspace until you commit

**13. What is the commit message in Git?**

??? success "Reveal answer"
    Every time we commit, we must give a commit message to identify each commit. The format differs
    from company to company. We can also use 'Tags' — a meaningful name given to a particular
    commit. Instead of referring to commit ID (40 alphanumeric characters), we refer to the tag, which
    internally points to the respective commit ID.
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    Configuration Management

**14. What is Git Bisect?**

??? success "Reveal answer"
    Git Bisect is used to pick the bad commit out of all good commits. It divides all commits equally into
    two parts (bisecting). Instead of building each commit one by one, we build both parts — where the
    bad commit exists, that part's build will fail. We repeat this operation until we find the bad commit. Git
    bisect allows you to find a bad commit out of good commits automatically.

**15. What is Git merge?**

??? success "Reveal answer"
    By default, we get one branch in git local repository called 'Master'. We create branches for parallel
    development. Finally, we merge code of all branches into Master and push to central repository.
    Sometimes, while merging, conflict occurs — when the same file exists in different branches with
    different code. We need to resolve that conflict manually by rearranging the code.

**16. What is a rebase, and when would you use it instead of merging?**

??? success "Reveal answer"
    Rebase replays your commits on top of another branch's latest commits, producing a clean, linear history instead of
    the extra merge commits a regular merge creates. I use it to bring my feature branch up to date with main before
    opening a PR, but I avoid rebasing anything that's already been pushed and shared, since rewriting shared history
    causes real pain for collaborators.

**17. What is Git Revert?**

??? success "Reveal answer"
    Git Revert command is used to remove changes from all 3 stages (work directory, staging area and
    local repository). We use this command after commit. This operation generates a new commit ID with
    a meaningful message to ignore the previous commit where the mistake is. However, we can't
    completely eliminate the original commit because Git tracks each and every change.

**18. What is Git stash?**

??? success "Reveal answer"
    Git stash is a temporary repository where we can store our content and bring it back whenever we
    want to continue work. It removes content from the working directory and puts it in the stashing store,
    giving a clean working directory to start new work. Later, we can bring back stashed items and
    resume work. Git stash applies to modified files, not new files.

**19. Explain the concept of tags in GitLab.**

??? success "Reveal answer"
    Tags reference specific points in a repository's history, typically marking release versions or milestones. They're
    immutable snapshots of a particular commit, either annotated with extra information or lightweight, and are useful for
    managing releases and deployments.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    2
    7
    PYTHON FOR DEVOPS

**20. What is the difference between GitLab and GitHub?**

??? success "Reveal answer"
    GitLab bundles integrated CI/CD, issue tracking, and project management natively in one platform, making it well
    suited for full DevOps workflows, and offers strong self-hosting support. GitHub is more focused on
    social/open-source coding, with GitHub Actions adding CI/CD capability more recently, and primarily operates as a
    cloud service.

**21. What is Source Code Management?**

??? success "Reveal answer"
    It is a process through which we can store and manage any code. Developers write code, Testers
    write test cases and DevOps engineers write scripts. This code, we can store and manage in Source
    Code Management. Different teams can store code simultaneously. It saves all changes separately.
    We can retrieve this code at any point of time.

**22. What is Git Reset?**

??? success "Reveal answer"
    Git Reset command is used to remove changes from the staging area — bringing back a file from the
    staging area to the work directory. We use this command before commit to undo accidental 'git add'. If
    we add '--hard' flag, the file will be removed from both the staging area and working directory
    simultaneously.

**23. Difference between Git pull and Git clone?**

??? success "Reveal answer"
    Git clone: For the first time if you want the whole central repository in your local server, we use git
    clone. It brings the entire repository to your local server.
    Git pull: Next time onwards you want only changes instead of the whole repository — in this case, we
    use Git pull (Incremental data).

**24. What are the Advantages of Source Code Management?**

??? success "Reveal answer"
    • Helps in Achieving teamwork
    • Can work on different features simultaneously
    • Acts like pipeline b/w offshore & onshore teams
    • Track changes (Minute level)
    • Different people from the same team, as well as different teams, can store code simultaneously
    (Save all changes separately)

**25. What is the difference between Git pull and Fetch?**

??? success "Reveal answer"
    Git fetch: Only brings changes from central repo to local repo, but these changes will NOT be
    integrated/merged to the local repo.
    Git merge: Merges the fetched changes to your local repository so you can see them.
    Git pull = Git fetch + Git merge (both operations happen internally).

**26. What is Git cherry-pick?**

??? success "Reveal answer"
    When you use git merge, all commits from the development branch are merged into the current
    branch. But sometimes you want only one specific commit from the development branch. Git
    cherry-pick picks only one commit that you select and merges it with commits in your current branch.

**27. Can you explain the GitLab branching strategy?**

??? success "Reveal answer"
    A common approach is Git Flow -- Master/Main as the stable production version, Develop as the integration branch,
    feature branches created from Develop for specific work, release branches for preparing production releases, and
    hotfix branches for urgent fixes directly off Master.

**28. What is GitLab's only/rules in CI/CD?**

??? success "Reveal answer"
    only/except (older): basic branch/tag filtering. rules (newer): more expressive conditions 
    using if, changes, exists. 
    rules: 
     - if: '$CI_COMMIT_BRANCH == "main"' 
     - if: '$CI_PIPELINE_SOURCE == "merge_request_event"' 
     changes: ["src/**/*"]

**29. What is git rebase?**

??? success "Reveal answer"
    Rebase moves or reapplies commits onto vebiie
    a new base Commit. O-8“O) — ©)
    What is the difference between merge and rebase ? Merge Rebase
    > Merge preserves branch history, while
    yebase creates a Cleaner linear history. O-O-O by OR On Om Cun)

**30. What is Git squash?**

??? success "Reveal answer"
    Git squash moves multiple commits into its parent so that you end up with one commit. If you repeat
    this process multiple times, you can reduce 'n' number of commits to a single one. We use this
    operation just to reduce the number of commits.

## Scenarios and troubleshooting

**31. Explain the Git branching strategy you use in production environments.**

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

**32. How do you handle Key Points : GA_Insights Failure Handling Plow : failed builds?**

??? success "Reveal answer"
    @ Review Console Logs N
    @ Analyze Failure 7 Q 2 ® bs 2 (aa)
    
    Answer :
    
    ea . @ Check Git Changes Check Identify Check Review Review
    
    I first review the Jenkins Console © Review Logs/Screenshots | Console Output Failure Git Changes Logs Screenshots
    
    Output, identify the build or test ga
    
    i . @ Reproduce Locally
    failures, check Git changes, review eat ae
    logs and screenshots, reproduce the i are Commit | ie | > ya > f > om > Q
    f . kK « . @ Re-run Pipeline KJ
    issue locally if needed, fix it, commit reas Fi Commi Re- Build
    rr @ Verify Success Rensomict * one ae =
    the changes, and re-run the pipeline. Locally Issue Changes Pipeline Successfull
    Pro Tip SAV Remember Goal
    Keep your pipeline simple, | a — Automate more, test ' Faster Delivery
    modular, and version t a s early, and deliver t Better Quality
    controlled. | with confidence! } Happy Users!
    ee ___ee— e —
    
    oe
    id
    Ee CI/CD INTERVIEW (ax 15
    il =
    =) — \H
    UESTIONS & ANSWERS | ime
    J Questions
    == === SPT
    ere
    Beginner —> Intermediate —> ye) Advanced
    r
    Fe *Y (Scenario Based)
    | peng . m.- Key Points : QA_Insights Scenario…

## Practice questions

**33. How to combine multiple commits into single commit?**

??? success "Reveal answer"
    git rebase -i HEAD~n
     36. What is .git folder?
    It stores:
    •
    Repo history
    •
    Branches
    •
    Objects
    •
    Configuration
    
     37. If you lost .git folder — how to restore?
    You cannot fully restore.
    You must reinitialize:
    git init
    git remote add origin <url>
    git fetch
     38. Difference between git pull and git fetch?
    •
    git fetch → downloads but doesn't merge
    •
    git pull → downloads + merges automatically
     39. Where do you store Jenkinsfiles and 
    Dockerfiles?
    Typically in each service repository:
    /app
     Dockerfile
     Jenkinsfile
     40. Docker stops & restarts — data lost. How to 
    fix?
    Use Docker volumes or bind mounts to persist data.
     41. What is CrashLoopBackOff?
    Pod keeps crashing and Kubernetes keeps restarting it.
    Causes:
    •
    App errors
    •
    Wrong configs
    •
    Missing dependencies
    •
    Liveness probe failure
    
     42. How to delete unused Docker containers and 
    images?
    docker system prune -a
     43. What type of Load Balancers have you used?
    •
    ALB
    •
    NLB
    •
    CLB
    In Kubernetes:
    •
    Ingress Controller
    •
    Service LoadBalancer
     44. What are S3 storage classes?
    •
    Standard
    •
    Standard-IA
    •
    One…

**34. What does git stash do?**

??? success "Reveal answer"
    Pes? nis dreteny
    => it temporarily Saves uncommitted changes [ stuh ies 1
    without creating a Commit. -----4
    What does git cherry-pick do? eS ee
    —> It applies a specific commit from one @) 0)
    branch to another.
    What is a pull request ? R a AK
    —> A pull request proposes code changes for i" ad ar v)
    review before merging. Developer Reviewer Merge
    i How do you undo the latest Git commit ? git revert HEAD git reset --hard HEAD~1 r
    le —> Use git revert for a safe reversal or 5
    v O
    "| git reset to move the branch pointer. © @«" W
    S ——. JyothiMulkuntla ——. =
    A) J eee eee? g bs
    
    RR IO,
    ir al
    100 DevOps Engineer Intérview Questioris and Answers
    
    Si Etc 25
    Gt) What is a CI/CD pipeline?
    —> It is an automated workflow that builds, tests, 6)-@- [=| M-a
    and deploys software. CODE BUILD TEST DEPLOY _— PROD
    @2) What are common CI/CD tools?
    > Jenkins, GitHub Actions, GitLab CI/CD, 2» fee ap ro)
    wD
    Azure DevOps, CircleCI, and Argo CD. Jenkins GitHub GitLab Azure Circle Argo CD
    Actions CI/cD DevOps
    G3) What is Jenkins?
    —> Jenkins is an automation server used to g === Ge)
    build,…

**35. How do you integrate GitHub with CI/CD tools?**

??? success "Reveal answer"
    GitHub can fire webhooks to tools like Jenkins or GitLab CI on events like a commit or pull request, or use its native
    GitHub Actions for built-in automation. For third-party tools, I authenticate using a personal access token or a GitHub
    App, and I use Docker images pulled from Docker Hub within pipelines to keep build environments consistent, with
    CI results reported back as PR status checks before a merge is allowed.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    0
    7
    GITHUB ACTIONS

**36. How do you resolve conflicts in Git?**

??? success "Reveal answer"
    Git flags the conflicting files, and I open each one to find the <<<<<<<, =======, >>>>>>> markers showing both
    versions. I edit the file to choose or combine the correct changes, remove the markers, stage the file with git add to
    mark it resolved, then complete the operation with git commit for a merge or git rebase --continue for a rebase, and
    finally push the resolved changes.

**37. A developer accidentally pushed a secret to GitHub. What do you do?**

??? success "Reveal answer"
    1. Immediately revoke the secret at the source (rotate the API key, change the password). 
    2) Remove from current code via new commit. 3) Purge from Git history (git filter-
    repo or BFG Repo Cleaner). 4) Force-push (only on non-protected branches). 5) Audit 
    access logs for unauthorized use during exposure window. 6) Enable secret scanning to 
    prevent recurrence.

**38. Can you elaborate commit in Git?**

??? success "Reveal answer"
    • Storing file permanently in the local repository we call commit
    • For every commit, we get one commit ID
    • It contains 40 long Alpha-numeric characters
    • It uses the concept 'Checksum' (Linux tool that generates binary value equal to the data present
    in file)
    • Even if you change one dot, Commit-ID will get changed
    • Helps in tracking the changes

**39. How do you handle merge conflicts in GitLab?**

??? success "Reveal answer"
    Merge the conflicting branch into the current branch locally, use git merge or git rebase to resolve conflicts in an
    editor, commit the resolved changes, and push back to the repository -- or resolve conflicts directly through GitLab's
    web interface on the merge request.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**40. What do you mean by 'Snapshot' in Git?**

??? success "Reveal answer"
    • It is a backup copy for each version Git stores in a repository
    • Snapshot is an incremental backup copy (only backup for new changes)
    • Snapshot represents data of a particular time so that we can retrieve it
    • This snapshot is taken in the Staging area in Git which is present between Git workspace and Git
    local repository

## Related

- Course: [Git](../git/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
