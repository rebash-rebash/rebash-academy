---
title: "Creating and Cloning Repositories"
description: "Initialise repositories with git init, create a bare remote, clone it, and verify remotes for DevOps workflows."
difficulty: beginner
estimated_time: "45–60 min"
technology: git
category: git
module: "Module 3 · Git Basics"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - git
  - repositories
prerequisites:
  - git/git-installation-and-configuration
next:
  - git/basic-git-workflow-add-commit-push
related:
  - git/working-with-remotes
tags:
  - git
  - clone
  - init
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---

    # Creating and Cloning Repositories

    ## Overview

    Every delivery pipeline starts from a repository URL. You must know the difference between a working repository and a **bare** remote, how `git init -b main` bootstraps history, and what `git clone` actually copies.

    This is **Tutorial 1** in **Module 3 : Git Basics** of the REBASH Academy **Git & GitHub for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and Site Reliability Engineering (SRE) engineers.

    ## Prerequisites

    - [Git Installation and Configuration](git-installation-and-configuration.md)
- Git 2.x on PATH

    ## Learning Objectives

    By the end of this tutorial, you will be able to:

    - [ ] Create a repository with `git init -b main`
- [ ] Create a bare remote and push an initial commit to it
- [ ] Clone that remote and verify `origin`
- [ ] Inspect `.git` layout at a high level
- [ ] Leave clone evidence under `~/rebash-git/module-03`

    ## Architecture

    A developer working copy pushes to a bare remote; clones fetch objects from that remote as `origin`.

    ![Creating and Cloning Repositories](../assets/excalidraw/git-repository-architecture.svg)

    ## Theory

    ### What it is

    `git init` creates a `.git` directory (object database + refs) in a project folder. A **bare** repository (`git init --bare`) has no working tree — it is the shape servers and `origin` remotes use. `git clone` copies objects and checks out a branch, adding `origin` for you.

    ### Why it matters

    DevOps automation clones cleanly in CI. Confusing a working repo with a bare remote causes 'refusing to update checked out branch' errors and broken hooks layouts.

    ### How it works

    1. `git init -b main` in a project directory.
2. Add files and commit.
3. `git init --bare ../remotes/app.git` as a simulated origin.
4. `git remote add origin …` and `git push -u origin main`.
5. `git clone` into a second directory and inspect `git remote -v`.

    ### Key concepts and comparisons

    | Kind | Working tree? | Typical use |
|------|---------------|-------------|
| Non-bare | Yes | Daily development |
| Bare | No | `origin` / server mirror |

| Command | Result |
|---------|--------|
| `git init -b main` | New repo on `main` |
| `git clone URL` | Copy + `origin` + checkout |

    ### Common pitfalls

    - Pushing to a non-bare repo's checked-out branch
- Cloning with wrong URL scheme (SSH vs HTTPS)
- Initialising inside an existing `.git` parent by accident

    ## Hands-on Lab

    ### Objective

    Create an app repo, a bare remote, push, and clone — proving remotes work without GitHub.

    ### Prerequisites

    - Git 2.x

    ### Lab environment

    Workspace: `~/rebash-git/module-03`

    ```bash
    mkdir -p ~/rebash-git/module-03 && cd ~/rebash-git/module-03
    set -euo pipefail
    ```

    ### Real-world scenario

    CI will clone from an internal bare mirror before GitHub is available. You must prove init → bare → clone locally.

    ### Step-by-step tasks

    #### Task 1 – Init app repo and first commit

Bootstrap a real project history.

```bash title="Terminal"
cd ~/rebash-git/module-03
set -euo pipefail
rm -rf app remotes clone
mkdir -p app remotes
cd app
git init -b main
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
printf '# demo app\n' > README.md
git add README.md
git commit -m 'chore: initial commit'
git log --oneline | tee ../init-log.txt
cd ..
```

!!! example "Expected output"
    `init-log.txt` shows the initial commit.


#### Task 2 – Create bare remote and push

Bare remotes accept pushes like GitHub.

```bash title="Terminal"
cd ~/rebash-git/module-03
set -euo pipefail
git init --bare remotes/app.git
cd app
git remote add origin ../remotes/app.git
git push -u origin main
git remote -v | tee ../remote-v.txt
cd ..
git --git-dir=remotes/app.git log --oneline | tee bare-log.txt
grep -q 'initial commit' bare-log.txt
```

!!! example "Expected output"
    Bare remote contains the commit; `origin` points at it.


#### Task 3 – Clone and verify

CI-style fresh checkout.

```bash title="Terminal"
cd ~/rebash-git/module-03
set -euo pipefail
git clone remotes/app.git clone
cd clone
git remote -v | tee ../clone-remote.txt
git log --oneline | tee ../clone-log.txt
test -f README.md
tar -czf ../module-03-evidence.tgz -C .. init-log.txt remote-v.txt bare-log.txt clone-remote.txt clone-log.txt
ls -l ../module-03-evidence.tgz | tee ../evidence.txt
```

!!! example "Expected output"
    Clone has `origin` and matching history; evidence archived.


    ### Validation steps

    - [ ] Bare log matches app history
- [ ] `clone-remote.txt` lists origin
- [ ] README exists in clone

    ### Common errors and fixes

    | Error | Cause | Fix |
    |-------|-------|-----|
    | remote origin already exists | Re-run after rm -rf | Remove app/remotes/clone and restart |
| denied update | Pushed to non-bare checkout | Use `--bare` remote |
| destination path exists | clone/ left over | rm -rf clone |

    ### Challenge exercise

    Run `find remotes/app.git -maxdepth 2 -type d | tee bare-layout.txt` and note `hooks/` and `refs/` in your evidence notes.

    ### Learning outcomes

    - Created bare remote
- Pushed and cloned successfully
- Verified origin URLs

    ### Cleanup

    ```bash
    ls ~/rebash-git/module-03
    ```

    ## Validation

    - [ ] Lab under `~/rebash-git/module-03/`
- [ ] Explain bare vs non-bare
- [ ] Explain what clone configures
- [ ] Name one CI failure from bad clone URLs

    ## Code Walkthrough

    1. **Inspect remotes** — `git remote -v` after clone
2. **Prefer bare for shared remotes** — avoids checkout conflicts
3. **Pin default branch** — `init -b main`
4. **Treat clone URL as config** — scripts should not hard-code one laptop path
5. **Evidence in CI** — log the SHA after clone

    ## Security Considerations

    - Do not clone untrusted URLs that run smudge filters without review
- Bare remotes still need access control on the server
- Disable risky `uploadpack` options on public hosts
- Keep credentials out of remote URLs
- Verify first clone of internal hosts (SSH known_hosts)

    ## Common Mistakes

    !!! warning "Using a working tree as the team origin"
    Pushes fail or overwrite someone else's checkout. **Fix:** Host a bare repo or use GitHub/GitLab.

!!! warning "Nested git init inside another repo"
    Submodule confusion and wrong roots. **Fix:** Check for parent `.git` with `git rev-parse --show-toplevel`.

    ## Best Practices

    - Standardise `main` as default
- Document clone URLs in README
- Use SSH or HTTPS consistently per org
- Keep monorepo vs polyrepo decision explicit
- Automate bare mirrors for air-gapped CI if needed

    ## Troubleshooting

    | Symptom | Likely cause | Fix |
    |---------|--------------|-----|
    | fatal: not a git repository | Wrong directory | cd into project root |
| refusing to merge unrelated histories | Separate inits | Do not force without understanding |
| Permission denied | Filesystem ACLs on bare repo | Fix ownership on remotes/ |

    ## Summary

    You can initialise, publish to a bare remote, and clone — the same loop GitHub automates as a service. Next: [Basic Git Workflow — Add, Commit, Push](basic-git-workflow-add-commit-push.md).

    ## Interview Questions

**1. What is a bare repository?**

??? success "Reveal answer"
    A Git repo without a working tree, used as a remote/server endpoint that accepts pushes.

**2. What does git clone set up for you?**

??? success "Reveal answer"
    A local copy of objects, a checkout of the default branch, and a remote named origin pointing at the source URL.

**3. Why prefer git init -b main?**

??? success "Reveal answer"
    It creates the repository on main to match modern forge defaults and team scripts.

**4. Can two developers share a non-bare repo over a network folder?**

??? success "Reveal answer"
    It is fragile; the checked-out branch cannot safely receive pushes. Use a bare remote or a forge.

**5. Where do remotes live after clone?**

??? success "Reveal answer"
    In .git/config as remote.origin.url and fetch refspecs; list with git remote -v.

**6. What is copied by clone?**

??? success "Reveal answer"
    Reachable objects and refs from the source; you get full history of fetched branches (by default the default branch checkout).

**7. How do you change origin URL?**

??? success "Reveal answer"
    git remote set-url origin NEWURL

**8. Why might CI clone be shallow?**

??? success "Reveal answer"
    To save time/bandwidth with --depth; beware needing full history for blame/tags.

    ## Related Tutorials

    - [Git Installation and Configuration](git-installation-and-configuration.md)
- [Basic Git Workflow — Add, Commit, Push](basic-git-workflow-add-commit-push.md)
- [Working with Remotes](working-with-remotes.md)

    ## References

    - [git-init](https://git-scm.com/docs/git-init)
- [git-clone](https://git-scm.com/docs/git-clone)
