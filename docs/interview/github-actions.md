---
title: "GitHub Actions Interview Preparation"
description: "34 curated GitHub Actions interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: github-actions
tags:
  - interview
  - github-actions
comments: false
---

{% raw %}
# GitHub Actions Interview Preparation

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

**1. What is a GitHub Actions workflow, and explain its key components.**

??? success "Reveal answer"
    **In short:** A workflow is a YAML automation in `.github/workflows` triggered by events and run as jobs on runners.
    
    **Key points**
    - **on** — events like `push`, `pull_request`, `workflow_dispatch`.
    - **jobs** — units of work; each runs on a runner (`runs-on`).
    - **steps** — shell commands or actions (`uses:`).
    - Permissions, env, secrets, and environments control what the workflow can touch.
    
    **Trap**
    - Wide `permissions: write-all` on every workflow — least privilege instead.

**2. What is the difference between needs and concurrency in GitHub Actions?**

??? success "Reveal answer"
    **In short:** `needs` orders jobs in a DAG; `concurrency` limits overlapping runs of a group.
    
    **Key points**
    - **needs** — job B waits for A; can also read A’s outputs.
    - **concurrency** — cancels or queues runs sharing a group key.
    - Use `needs` for correctness; `concurrency` for resource/race control.
    - Together: ordered deploys without two prod deploys racing.
    
    **Trap**
    - Using only `concurrency` and assuming it creates job dependencies — it does not.

**3. What is GitHub Actions Matrix strategy?**

??? success "Reveal answer"
    **In short:** A matrix fans one job definition into many combinations (OS, version, arch).
    
    **Key points**
    - `strategy.matrix` expands jobs across dimensions.
    - Great for test matrices: Node 18/20 × ubuntu/windows.
    - `include`/`exclude` tunes combinations; `fail-fast` controls abort.
    - Each matrix cell is a separate job with its own runner.
    
    **Try this**
    - `strategy: { matrix: { python-version: ['3.11','3.12'] } }`
    
    **Trap**
    - Huge matrices that burn Actions minutes and hide the one real failure.

**4. What is a matrix in GitHub Actions?**

??? success "Reveal answer"
    **In short:** A matrix is the set of variable dimensions that multiply a job into parallel variants.
    
    **Key points**
    - Defined under `jobs.<id>.strategy.matrix`.
    - Each combination gets a unique job name and context (`matrix.*`).
    - Share setup via reusable actions; keep cells independent.
    - Cap max-parallel if the farm or flaky tests need it.
    
    **Trap**
    - Sharing mutable remote state between matrix cells without locking.

**5. What is the needs keyword in GitHub Actions?**

??? success "Reveal answer"
    **In short:** `needs` declares that a job depends on one or more upstream jobs succeeding (by default).
    
    **Key points**
    - Creates a DAG: test needs build; deploy needs test.
    - Access upstream outputs via `needs.build.outputs.tag`.
    - `if: always()` / `if: failure()` can run cleanup after needs.
    - Skipped upstreams affect downstream `needs` evaluation — know the rules.
    
    **Trap**
    - Forgetting `needs` and assuming file order in YAML defines execution order.

**6. What are runners in GitHub Actions?**

??? success "Reveal answer"
    **In short:** Runners are the VMs or self-hosted machines that execute workflow jobs.
    
    **Key points**
    - GitHub-hosted: `ubuntu-latest`, Windows, macOS images.
    - Self-hosted: your hardware/network, your patching burden.
    - Jobs pick runners with `runs-on` labels.
    - Ephemeral runners reduce persistence risk for untrusted code.
    
    **Trap**
    - Self-hosted runners for public fork PRs — a classic crypto-mining vector.

**7. What are GitHub Actions and how do they work?**

??? success "Reveal answer"
    **In short:** GitHub Actions is GitHub’s CI/CD: events trigger workflows that run jobs as steps/actions.
    
    **Key points**
    - YAML in the repo describes automation next to the code.
    - Marketplace actions encapsulate reusable steps.
    - Secrets, environments, and OIDC connect to clouds securely.
    - Logs and checks appear on PRs for required status checks.
    
    **Trap**
    - Pinning actions to floating `@main` — supply-chain roulette.

**8. What is the jobs.<job_id>.outputs feature?**

??? success "Reveal answer"
    **In short:** Job outputs let an upstream job export values downstream jobs can read via `needs`.
    
    **Key points**
    - Set outputs in a step (`GITHUB_OUTPUT`) and map them under `jobs.<id>.outputs`.
    - Downstream: `${{ needs.build.outputs.version }}`.
    - Useful for image digests, version numbers, and change flags.
    - Outputs are strings — keep them small and non-secret.
    
    **Try this**
    - `echo "tag=${SHA}" >> "$GITHUB_OUTPUT"`
    
    **Trap**
    - Putting secrets in outputs — they can leak into logs and dependent jobs.

**9. Explain your GitHub Actions pipeline?**

??? success "Reveal answer"
    **In short:** My pipeline: CI on PR (build/test/scan), publish on main, deploy via environment gates.
    
    **Key points**
    - PR: lint, unit tests, SAST/SCA, build image (optional).
    - Main: publish digest to registry with SBOM attestation.
    - Deploy jobs use `environment:` with approvals for prod.
    - Concurrency group per environment prevents overlapping deploys.
    
    **Trap**
    - Deploying from every feature branch because `push` was too broad.

**10. What is GitHub Actions concurrency?**

??? success "Reveal answer"
    **In short:** Concurrency groups ensure only one run in a group executes (optionally cancelling older ones).
    
    **Key points**
    - `concurrency: { group: ..., cancel-in-progress: true }`.
    - Common group: `${{ github.workflow }}-${{ github.ref }}`.
    - Stops stacked deploys fighting for the same environment.
    - Use `cancel-in-progress: false` when mid-run work must finish.
    
    **Trap**
    - One global concurrency group for all workflows — serialises the entire org.

**11. What is GitHub Actions OpenID Connect (OIDC)?**

??? success "Reveal answer"
    **In short:** OIDC lets workflows mint short-lived cloud credentials without storing long-lived cloud keys in GitHub.
    
    **Key points**
    - GitHub is the identity provider; AWS/Azure/GCP trust the token.
    - `permissions: id-token: write` plus cloud role assumption.
    - Scope trust to repo, branch, and environment claims.
    - Eliminates static access keys in Actions secrets for cloud deploy.
    
    **Trap**
    - Trusting `repo:*` in the cloud role — any workflow in the repo can then deploy.

**12. What is a GitHub Actions runner?**

??? success "Reveal answer"
    **In short:** A runner is the execution host for a single job’s steps.
    
    **Key points**
    - GitHub-hosted images come preloaded with common tools.
    - Self-hosted runners register with labels you target in `runs-on`.
    - One job ↔ one runner assignment; matrix jobs use many runners.
    - Keep runners patched; prefer ephemeral for untrusted code.
    
    **Trap**
    - Reusing a dirty self-hosted workspace across jobs without cleanup.

**13. What is actions/upload-artifact and actions/download-artifact?**

??? success "Reveal answer"
    **In short:** Upload/download-artefact share files between jobs in the same workflow run.
    
    **Key points**
    - `actions/upload-artifact` stores build outputs from job A.
    - `actions/download-artifact` retrieves them in job B.
    - Use for jars, reports, and coverage — not for huge Docker layers.
    - Set retention days; avoid storing secrets in artefacts.
    
    **Try this**
    - `actions/upload-artifact@v4`
    - `actions/download-artifact@v4`
    
    **Trap**
    - Uploading `node_modules` or whole `.git` — slow, costly, and pointless.

**14. What is the permissions key in GitHub Actions?**

??? success "Reveal answer"
    **In short:** `permissions` sets the `GITHUB_TOKEN`’s least-privilege scopes for the workflow or job.
    
    **Key points**
    - Default token permissions should be read-only where possible.
    - Grant `contents: write` or `packages: write` only when needed.
    - Job-level permissions override workflow defaults.
    - Pair with environment protection rules for deploys.
    
    **Trap**
    - Omitting `permissions` on older defaults that were overly broad.

**15. What is GitHub Actions timeout-minutes?**

??? success "Reveal answer"
    **In short:** `timeout-minutes` kills a job (or step) that runs too long — protects minutes and stuck processes.
    
    **Key points**
    - Set at job or step level based on SLO for CI duration.
    - Fails the job when exceeded — good for hung tests.
    - Workflow max run time also applies on GitHub-hosted.
    - Tune with data, not guesswork.
    
    **Trap**
    - Timeouts so short that legitimate integration suites always fail on cold caches.

**16. What is the push.paths trigger filter?**

??? success "Reveal answer"
    **In short:** `push.paths` limits which file changes trigger the workflow — path filters save CI time.
    
    **Key points**
    - `on.push.paths` / `paths-ignore` select relevant changes.
    - Useful in monorepos: run service A only when `services/a/**` changes.
    - PR equivalents exist under `pull_request.paths`.
    - Remember: path filters can skip critical security workflows — design carefully.
    
    **Trap**
    - Path-filtering the security scan workflow so dependency changes skip SCA.

**17. What is workflow_run trigger?**

??? success "Reveal answer"
    **In short:** `workflow_run` triggers a workflow after another workflow completes (success/failure).
    
    **Key points**
    - Useful to separate privileged deploy workflows from untrusted PR CI.
    - Filter on `workflows:`, `types: [completed]`, and branch.
    - Downstream should re-validate artefacts — don’t trust blindly.
    - Requires careful permissions between workflows.
    
    **Trap**
    - Using `workflow_run` on fork PRs without artefact provenance checks.

**18. What is continue-on-error in GitHub Actions?**

??? success "Reveal answer"
    **In short:** `continue-on-error: true` lets a step/job fail without failing the whole job/workflow outcome.
    
    **Key points**
    - Use for optional linters or best-effort notifications.
    - Still visible as a warning in the UI.
    - Do not use on security gates or unit tests.
    - Prefer explicit `if` conditions over silencing real failures.
    
    **Trap**
    - Marking Sonar/SCA `continue-on-error` to “keep shipping”.

## Scenarios and troubleshooting

**19. How would you parameterize a workflow so that downstream jobs know which environment to deploy to?**

??? success "Reveal answer"
    **In short:** Pass environment via inputs, outputs, or `environment:` so deploy jobs know the target.
    
    **Key points**
    - `workflow_dispatch` inputs for manual choice of env.
    - Map branch → env (`main`→prod, `develop`→dev) in job `if`.
    - Job outputs carry the chosen env/digest to deploy jobs via `needs`.
    - GitHub Environments bind secrets/approvals per target.
    
    **Trap**
    - A free-text env input with no allow-list — typo deploys to nowhere (or worse).

**20. You are given a GitHub Actions workflow snippet. How would you identify incorrect steps and suggest improvements or missing steps for a robust CI/CD pipeline?**

??? success "Reveal answer"
    **In short:** Review triggers, permissions, pin actions, add tests/scans, and ensure deploy uses digests + gates.
    
    **Key points**
    - Missing: checkout, cache, test, scan, upload artefact, OIDC login.
    - Red flags: `pull_request_target` abuse, unpinned actions, secrets in logs.
    - Improve: `permissions`, concurrency, environment approvals, timeouts.
    - Ensure failure of tests fails the workflow — no `continue-on-error` on gates.
    
    **Trap**
    - “Looks fine” without checking whether required status checks are actually enforced.

## Practice questions

**21. How do you write a reusable workflow in GitHub Actions?**

??? success "Reveal answer"
    **In short:** Reusable workflows are called with `uses: org/repo/.github/workflows/foo.yml@ref` and typed inputs.
    
    **Key points**
    - Callee defines `on.workflow_call` inputs/outputs/secrets.
    - Caller passes `with:` / `secrets:` and pins a tag or SHA.
    - Centralise build/deploy standards across many repos.
    - Version the reusable workflow like a library.
    
    **Try this**
    - `uses: my-org/ci/.github/workflows/node-ci.yml@v2`
    
    **Trap**
    - Calling `@main` of a reusable workflow — uncontrolled change for every consumer.

**22. How do you deploy to EKS through GitHub Actions?**

??? success "Reveal answer"
    **In short:** Authenticate with OIDC to AWS, update EKS manifests/Helm with an immutable image digest, then verify.
    
    **Key points**
    - Configure AWS role trust for GitHub OIDC; assume role in the job.
    - `aws eks update-kubeconfig` then `kubectl`/`helm`/`helmfile`.
    - Prefer GitOps (PR to deploy repo) over direct prod kubectl from CI.
    - Smoke-check rollout status and roll back on failure.
    
    **Trap**
    - Long-lived `AWS_ACCESS_KEY_ID` in repo secrets with `kubectl` cluster-admin.

**23. How do you prevent concurrent executions in GitHub Actions?**

??? success "Reveal answer"
    **In short:** Set a `concurrency` group (often per branch/environment) and cancel or queue overlapping runs.
    
    **Key points**
    - `concurrency.group` + `cancel-in-progress` for CI on the same PR.
    - For prod, cancel-in-progress false may be safer — queue instead.
    - Combine with environment protection rules.
    - Document who can bypass locks.
    
    **Trap**
    - No concurrency on deploy workflows — two SHAs fight in prod.

**24. Where do you keep the GitHub Actions workflow file, and how do you upload a JAR artifact?**

??? success "Reveal answer"
    **In short:** Workflows live under `.github/workflows/`; upload JARs with `actions/upload-artifact` (or publish to a registry).
    
    **Key points**
    - Commit YAML under `.github/workflows/*.yml`.
    - Build with Maven/Gradle; path to `target/*.jar`.
    - `upload-artifact` for CI sharing; Nexus/Maven registry for real releases.
    - Name artefacts with version/SHA for traceability.
    
    **Try this**
    - `actions/upload-artifact@v4` with `path: target/*.jar`
    
    **Trap**
    - Committing JARs into Git instead of using artefacts/registries.

**25. About K8's Architecture and tell me the workflow?**

??? success "Reveal answer"
    **In short:** Kubernetes: control plane + workers; a typical Actions workflow builds an image and rolls out a Deployment.
    
    **Key points**
    - Control plane: API server, etcd, scheduler, controllers.
    - Workers: kubelet, runtime, kube-proxy run Pods.
    - Workflow: test → build/push image → update Deployment/Helm → wait Ready.
    - Better: workflow opens a GitOps PR; Argo CD syncs the cluster.
    
    **Trap**
    - Explaining only Pods and forgetting how CI actually reaches the cluster securely.

**26. How do you set up a manual trigger in GitHub Actions?**

??? success "Reveal answer"
    **In short:** Use `workflow_dispatch` (and optionally `workflow_call`) for manual runs with inputs.
    
    **Key points**
    - `on: workflow_dispatch` with typed inputs for env/version.
    - Run from Actions UI or GitHub CLI (`gh workflow run`).
    - Gate prod with environment reviewers even on manual runs.
    - Log who triggered what for audit.
    
    **Try this**
    - `gh workflow run deploy.yml -f environment=uat`
    
    **Trap**
    - Manual prod deploy without recording the artefact digest that was released.

**27. How do you run jobs in parallel in GitHub Actions?**

??? success "Reveal answer"
    **In short:** Independent jobs without mutual `needs` run in parallel; matrices multiply parallel cells.
    
    **Key points**
    - Default: jobs start together unless `needs` serialises them.
    - Matrix strategy parallelises test variants.
    - Watch Actions minute costs and flake rates.
    - Use `max-parallel` to throttle.
    
    **Trap**
    - Assuming steps inside one job are parallel — steps are sequential.

**28. 12 .How do you handle parallel execution in CI/CD workflows?**

??? success "Reveal answer"
    **In short:** Parallelism comes from independent jobs, matrices, and reusable fan-out — with caps.
    
    **Key points**
    - Split lint/test/build into parallel jobs.
    - Matrix for versions/OS; gather artefacts before deploy.
    - Concurrency controls prevent deploy races.
    - Measure wall-clock vs cost trade-offs.
    
    **Trap**
    - Parallelising everything including mutually dependent DB migrations.

**29. How do you securely store secrets in GitHub Actions?**

??? success "Reveal answer"
    **In short:** Store secrets in GitHub Actions secrets/environments (or OIDC) — never in YAML or logs.
    
    **Key points**
    - Repo/org/environment secrets with least privilege.
    - Environment secrets + required reviewers for prod.
    - Prefer OIDC over static cloud keys.
    - Rotate on incident; avoid printing `${{ secrets.* }}`.
    
    **Trap**
    - Echoing secrets to “debug” — masking is not perfect for all encodings.

**30. How do you create a GitHub Actions workflow?**

??? success "Reveal answer"
    **In short:** Add a YAML file under `.github/workflows`, define `on`/`jobs`/`steps`, push, and watch the run.
    
    **Key points**
    - Start with `workflow_dispatch` or `push` to a branch.
    - Use `actions/checkout`, then build/test steps.
    - Enable required checks on the protected branch.
    - Iterate with act or small PRs.
    
    **Try this**
    - `.github/workflows/ci.yml`
    - `actions/checkout@v4`
    
    **Trap**
    - Creating the workflow only on `main` without testing on a branch first.

**31. Suppose I want to build and test a Java Maven application and create an artifact, what steps would you include?**

??? success "Reveal answer"
    **In short:** Checkout → set up JDK → cache Maven → test → package → upload artefact → optional scan.
    
    **Key points**
    - `actions/setup-java` with Temurin and Maven cache.
    - `mvn -B test package`; publish junit/coverage.
    - Upload JAR artefact; run Sonar/SCA if required.
    - For releases, deploy to Nexus/GitHub Packages with pinned versions.
    
    **Try this**
    - `mvn -B verify`
    - `actions/upload-artifact@v4`
    
    **Trap**
    - Skipping tests with `mvn package -DskipTests` in CI “to go faster”.

**32. In GitHub Actions, if one job depends on another job, which parameter do you use?**

??? success "Reveal answer"
    **In short:** Use `needs:` on the downstream job to depend on the upstream job.
    
    **Key points**
    - `needs: [build]` waits for `build` to succeed.
    - Read outputs via `needs.build.outputs.*`.
    - Multiple needs create a join point.
    - Combine with `if:` for conditional deploy after needs.
    
    **Trap**
    - Confusing `needs` with `concurrency` or step `id` ordering.

**33. How caching works in Github Actions?**

??? success "Reveal answer"
    **In short:** Caching restores keyed files (deps) between runs so installs skip cold downloads.
    
    **Key points**
    - `actions/cache` or setup-* actions with built-in caches.
    - Key on lockfile hashes (`pom.xml`, `package-lock.json`).
    - Restore-keys allow partial hits.
    - Don’t cache build outputs you should rebuild for correctness.
    
    **Try this**
    - `actions/cache@v4` keyed on `${{ hashFiles('**/pom.xml') }}`
    
    **Trap**
    - Caching mutable credentials or entire `$HOME` by accident.

**34. What steps are included in your GitHub Actions workflow file?**

??? success "Reveal answer"
    **In short:** Typical steps: checkout, setup toolchain, cache, lint/test, build, scan, publish, deploy.
    
    **Key points**
    - CI jobs first for fast feedback on PRs.
    - Security scanning before publish.
    - Publish immutable artefacts/digests.
    - Deploy with environment protections and post-verify.
    
    **Trap**
    - A workflow that only builds — no tests, no scans, no provenance.

## Related
- Course: [GitHub Actions](../github-actions/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
