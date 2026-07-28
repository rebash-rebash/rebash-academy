#!/usr/bin/env python3
"""Build GitLab CI-only curriculum metadata for generate-cicd-tutorials.py."""

from __future__ import annotations

from textwrap import dedent

TUTORIALS = [
    (1, "introduction-to-cicd-and-delivery-models", "Introduction to CI/CD and Delivery Models", "Module 1: Foundations", "beginner", "35 min", "hello", "foundations"),
    (2, "pipeline-anatomy-stages-jobs-and-artifacts", "Pipeline Anatomy — Stages, Jobs, and Artifacts", "Module 1: Foundations", "beginner", "40 min", "hello", "anatomy"),
    (3, "gitlab-ci-fundamentals", "GitLab CI Fundamentals", "Module 1: Foundations", "beginner", "50 min", "hello", "gitlab"),
    (4, "gitlab-merge-requests-and-pipeline-triggers", "GitLab Merge Requests and Pipeline Triggers", "Module 1: Foundations", "beginner", "45 min", "hello", "mr-triggers"),
    (5, "gitlab-runners-and-executors", "GitLab Runners and Executors", "Module 2: Runners and Configuration", "intermediate", "50 min", "hello", "runners"),
    (6, "gitlab-runner-tags-and-scaling", "GitLab Runner Tags and Scaling", "Module 2: Runners and Configuration", "intermediate", "45 min", "hello", "runner-tags"),
    (7, "variables-secrets-and-credentials", "Variables, Secrets, and Credentials", "Module 2: Runners and Configuration", "intermediate", "50 min", "hello", "secrets"),
    (8, "triggers-rules-and-branch-protection", "Triggers, Rules, and Branch Protection", "Module 2: Runners and Configuration", "intermediate", "45 min", "hello", "triggers"),
    (9, "building-docker-images-in-ci", "Building Docker Images in CI", "Module 3: Build and Quality", "intermediate", "55 min", "docker", "docker"),
    (10, "testing-reports-and-quality-gates", "Testing, Reports, and Quality Gates", "Module 3: Build and Quality", "intermediate", "45 min", "hello", "testing"),
    (11, "artifacts-caches-and-dependencies", "Artifacts, Caches, and Dependencies", "Module 3: Build and Quality", "intermediate", "45 min", "hello", "cache"),
    (12, "parallelism-matrix-and-pipeline-dags", "Parallelism, Matrix, and Pipeline DAGs", "Module 3: Build and Quality", "intermediate", "50 min", "hello", "dag"),
    (13, "least-privilege-ci-identities", "Least-Privilege CI Identities", "Module 4: Secure Pipelines", "intermediate", "45 min", "k8s", "iam"),
    (14, "security-scanning-in-pipelines", "Security Scanning in Pipelines", "Module 4: Secure Pipelines", "intermediate", "50 min", "docker", "scanning"),
    (15, "secret-detection-and-supply-chain-basics", "Secret Detection and Supply Chain Basics", "Module 4: Secure Pipelines", "intermediate", "45 min", "hello", "supply-chain"),
    (16, "protected-environments-and-approvals", "Protected Environments and Approvals", "Module 4: Secure Pipelines", "intermediate", "45 min", "k8s", "approvals"),
    (17, "gitlab-deployment-patterns", "GitLab Deployment Patterns", "Module 5: Deploy and Capstone", "intermediate", "50 min", "k8s", "deploy"),
    (18, "kubernetes-deploys-from-ci", "Kubernetes Deploys from CI", "Module 5: Deploy and Capstone", "advanced", "55 min", "k8s", "kubernetes"),
    (19, "gitlab-ci-production-patterns", "GitLab CI Production Patterns", "Module 5: Deploy and Capstone", "advanced", "45 min", "hello", "production"),
    (20, "cicd-capstone-and-terraform-handoff", "CI/CD Capstone and Terraform Handoff", "Module 5: Deploy and Capstone", "advanced", "60 min", "k8s", "capstone"),
]

SNIPPETS = {
    "hello": {
        "example_title": "Minimal GitLab CI test pipeline",
        "gitlab": """stages:
  - test

unit-test:
  stage: test
  image: python:3.12-slim
  script:
    - pip install -r requirements.txt
    - pytest -q
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH""",
    },
    "docker": {
        "example_title": "Build and push to GitLab Container Registry",
        "gitlab": """build-image:
  stage: build
  image: docker:27-cli
  services:
    - docker:27-dind
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
  script:
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"
    - docker build -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA" .
    - docker push "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA\"""",
    },
    "k8s": {
        "example_title": "Manual production deploy gate",
        "gitlab": """deploy-prod:
  stage: deploy
  image:
    name: bitnami/kubectl:latest
    entrypoint: [""]
  environment:
    name: production
  script:
    - kubectl set image deploy/api api=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual""",
    },
}

FOCUS = {
    "foundations": "CI/CD vocabulary, delivery models, and pipeline-as-code with GitLab CI",
    "anatomy": "stages, jobs, steps, logs, workspaces, and artefact promotion in GitLab pipelines",
    "gitlab": "`.gitlab-ci.yml` stages, rules, includes, and GitLab.com shared runners",
    "mr-triggers": "merge request pipelines, `CI_PIPELINE_SOURCE`, and branch push triggers",
    "runners": "GitLab Runner registration, executors (Docker, shell, Kubernetes), and isolation",
    "runner-tags": "runner tags, concurrency, autoscaling, and job-to-runner matching",
    "secrets": "CI/CD variables, masked secrets, OIDC, and protected variable scopes",
    "triggers": "push, MR, schedule, tag rules, and branch protection integration",
    "docker": "Docker-in-Docker, Kaniko, registry auth, and layer caching in GitLab CI",
    "testing": "JUnit reports, coverage gates, and failing builds on quality thresholds",
    "cache": "artefact storage, dependency caches, and reproducible builds",
    "dag": "parallel jobs, matrix builds, and `needs:` dependency graphs",
    "iam": "OIDC to cloud providers, scoped tokens, and job-level permissions",
    "scanning": "SAST, container scanning, and policy gates in merge request pipelines",
    "supply-chain": "secret detection, dependency audit, and SBOM basics",
    "approvals": "protected environments, manual jobs, and deployment windows",
    "deploy": "rolling, blue/green, and canary patterns from GitLab deploy jobs",
    "kubernetes": "kubeconfig, Helm, namespaces, and progressive delivery hooks",
    "production": "pipeline templates, includes, observability, and operating GitLab CI at scale",
    "capstone": "end-to-end GitLab pipeline integrating build, scan, deploy, and Terraform handoff",
}

THEORY = {
    "foundations": """\
        ### Continuous Integration and Delivery

        **Continuous Integration** automates build and test on every integration to a shared branch.
        **Continuous Delivery** keeps the default branch always releasable; production promotion may
        remain manual. **Continuous Deployment** automates production promotion when tests pass.

        ### Delivery models

        | Model | Branch pattern | Pipeline trigger |
        |-------|----------------|------------------|
        | Trunk-based | Short-lived feature branches → `main` | MR + merge to `main` |
        | Release train | Scheduled cut from `main` | Tag + release branch |
        | GitFlow-style | `develop` + `release/*` | Multiple long-lived branches |

        Modern GitLab defaults assume trunk-based flow with merge request pipelines. Other CI tools
        exist — Jenkins and GitHub Actions are covered in later REBASH tracks — but this curriculum
        teaches **GitLab CI** as the primary platform.

        ### Pipeline as code

        Storing `.gitlab-ci.yml` in Git gives you diff review, rollback, and audit trail — the same
        properties you expect from application code. Teams that edit pipelines only in the UI drift
        from documented process during incidents.

        ### GitLab CI vocabulary

        | Concept | GitLab CI |
        |---------|-----------|
        | Work unit | Job |
        | Ordering | Stages and `needs:` DAG |
        | Runner | GitLab Runner (shared or self-hosted) |
        | Config | `.gitlab-ci.yml` |
        """,
    "anatomy": """\
        ### Stages and jobs

        A **stage** groups jobs that should complete before the next phase begins. **Jobs** are the
        smallest schedulable unit — each gets a fresh workspace (with exceptions for caches and
        artefacts you explicitly pass).

        GitLab runs jobs in the same stage in parallel unless `needs:` creates a DAG edge. Use stages
        for coarse ordering; use `needs:` when a downstream job can start before the entire stage
        finishes.

        ### Logs and workspaces

        Each job logs stdout/stderr to the GitLab job trace. Secrets must be masked by the platform;
        never `echo` credentials. The workspace path is `$CI_PROJECT_DIR` — checkout → install → test
        → publish artefacts follows the same pattern as any CI platform.

        ### Artefacts

        **Artefacts** are files preserved after a job finishes — test reports, compiled binaries, or
        deployment manifests. They are not a substitute for a container registry or object storage for
        large binaries; they are convenient for passing build outputs to deploy jobs in the same pipeline.

        | Keyword | Typical use |
        |---------|-------------|
        | `artifacts:` | JUnit XML, dist folders, plan files |
        | `artifacts:reports:` | Test and coverage report integration in MR UI |
        """,
    "gitlab": """\
        ### GitLab CI configuration model

        GitLab reads `.gitlab-ci.yml` from the repository root (or path set in project settings).
        Top-level keys include `stages`, `default`, `variables`, `include`, and job names as keys.

        ### Runners and executors

        Jobs run on **runners** registered to your GitLab instance. GitLab.com provides shared runners;
        self-managed teams install `gitlab-runner` on VMs or Kubernetes. The **executor** (Docker, shell,
        Kubernetes) determines isolation — covered in depth in
        [GitLab Runners and Executors](gitlab-runners-and-executors.md).

        ### Rules and workflow

        Use `rules:` (preferred over deprecated `only/except`) to control when jobs run:

        ```yaml
        rules:
          - if: $CI_PIPELINE_SOURCE == "merge_request_event"
          - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
        ```

        `workflow:rules` can suppress entire pipelines for draft MRs or bot commits.

        ### Includes and templates

        Split large pipelines with `include:local`, `include:project`, or CI/CD components. Aligns with
        DRY principles — shared lint job templates across microservices.
        """,
    "mr-triggers": """\
        ### Merge request pipelines

        When you open or update a merge request (MR), GitLab can run a **merge request pipeline**
        with `CI_PIPELINE_SOURCE=merge_request_event`. This is the primary feedback loop for code review:
        lint, unit tests, and security scans run before merge.

        ### Branch pipelines

        Pushes to branches (including `main`) create **branch pipelines** with
        `CI_PIPELINE_SOURCE=push`. After merge, the default branch pipeline often builds releasable
        artefacts and triggers deploy stages.

        ### Combining triggers with rules

        Typical pattern for trunk-based flow:

        ```yaml
        workflow:
          rules:
            - if: $CI_PIPELINE_SOURCE == "merge_request_event"
            - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

        test:
          stage: test
          script: pytest -q
          rules:
            - if: $CI_PIPELINE_SOURCE == "merge_request_event"
            - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
        ```

        ### MR widgets and merge checks

        GitLab surfaces pipeline status on the MR. Combine with **merge request approvals** and
        **protected branches** so green pipelines are required before merge — see
        [Triggers, Rules, and Branch Protection](triggers-rules-and-branch-protection.md).
        """,
    "runners": """\
        ### GitLab Runner architecture

        The **GitLab Runner** is a separate agent process that polls GitLab for jobs, executes them
        in an isolated environment, and streams logs back. Shared runners on GitLab.com are managed
        by GitLab; self-managed runners register to your instance or project.

        ### Executors

        | Executor | Isolation | Typical use |
        |----------|-----------|-------------|
        | Docker | Container per job | Most CI workloads |
        | Shell | Host filesystem | Bare-metal build agents (use with care) |
        | Kubernetes | Pod per job | Large fleets, autoscaling |
        | SSH | Remote host | Legacy deploy targets |

        ### Registration

        Register a runner with `gitlab-runner register`, providing the GitLab URL, registration token,
        executor type, and default Docker image. Project-specific runners limit blast radius compared
        to instance-wide runners with broad tags.

        ### Security

        Runners execute untrusted code from merge requests. Use Docker or Kubernetes executors,
        disable privileged mode unless required, and isolate production credentials to protected
        runners and protected branches.
        """,
    "runner-tags": """\
        ### Runner tags

        Jobs select runners via **tags**:

        ```yaml
        integration-test:
          tags:
            - docker
            - amd64
          script: make integration
        ```

        Only runners with matching tags pick up the job. Use tags to route GPU jobs, ARM builds, or
        jobs that need access to internal networks.

        ### Concurrency and scaling

        Each runner has a **concurrent** job limit. When demand exceeds capacity, jobs queue. For
        self-hosted fleets:

        - Horizontal scaling: add runner VMs or Kubernetes runner deployments
        - Autoscaling executors: Kubernetes executor with cluster autoscaler
        - Separate runner pools for MR vs production deploy workloads

        ### Cost and queue time

        Monitor queue duration in GitLab Admin Area or runner metrics. Long queues often mean too few
        tagged runners or oversized jobs blocking concurrency slots. Right-size images and split slow
        integration tests using `parallel:` — see
        [Parallelism, Matrix, and Pipeline DAGs](parallelism-matrix-and-pipeline-dags.md).
        """,
    "deploy": """\
        ### GitLab environments

        **Environments** map deploy jobs to named targets (`staging`, `production`). GitLab tracks
        deployment history, URLs, and rollback links in the UI.

        ### Deployment strategies

        | Pattern | GitLab CI approach |
        |---------|-------------------|
        | Rolling | Sequential deploy job updates workload in place |
        | Blue/green | Deploy to idle colour; switch traffic via ingress or service |
        | Canary | Progressive traffic shift with manual or metric-driven gates |

        ### `environment:` keyword

        ```yaml
        deploy-staging:
          stage: deploy
          environment:
            name: staging
            url: https://staging.example.com
          script:
            - ./deploy.sh staging
        ```

        Pair with **protected environments** for production — covered in
        [Protected Environments and Approvals](protected-environments-and-approvals.md).
        """,
    "production": """\
        ### Pipeline templates at scale

        Mature GitLab programmes centralise common jobs in **CI/CD components** or `include:project`
        templates. Version templates with tags; pin includes to semver, not floating `main`.

        ### Observability

        - Export pipeline metrics (duration, failure rate, queue time) to your monitoring stack
        - Alert on repeated job failures or deploy stage regressions
        - Use `CI_JOB_TIMEOUT` and stage-level expectations in SLO dashboards

        ### Operating model

        Document who owns runner fleets, who approves `.gitlab-ci.yml` changes, and how incidents
        trigger pipeline freezes. Production GitLab CI is as much process as YAML — align with
        [Git](../git/index.md) branch protection and change management.

        ### What comes next

        Jenkins and GitHub Actions are deferred to dedicated REBASH tracks. This tutorial consolidates
        patterns you need operating GitLab CI in production before the
        [CI/CD Capstone and Terraform Handoff](cicd-capstone-and-terraform-handoff.md).
        """,
}


def theory_for(key: str, title: str) -> str:
    if key in THEORY:
        return THEORY[key]
    return dedent(
        f"""\
        ### Core concepts for {title}

        This tutorial focuses on **{FOCUS.get(key, key)}** in production GitLab CI pipelines. You will
        author and validate `.gitlab-ci.yml` configuration for the validate → build → test → secure →
        publish → deploy lifecycle.

        ### Design principles

        - **Fail fast** — run linters and unit tests before expensive integration work
        - **Immutable artefacts** — promote the same SHA-tagged image from staging to production
        - **Least privilege** — scope tokens and variables to the job that needs them
        - **Observable** — structured logs and test reports in the merge request UI

        ### GitLab CI mapping

        | Capability | GitLab CI syntax |
        |------------|------------------|
        | Conditional run | `rules:` |
        | Secret store | CI/CD variables (masked/protected) |
        | Manual gate | `when: manual` on job or protected environment |
        | Container job | `image:` and optional `services:` |

        Relate this lesson to [Git](../git/index.md) branch protection, [Docker](../docker/index.md)
        images built in CI, and deploy stages that call [Kubernetes](../kubernetes/index.md) or
        [Terraform](../terraform/terraform-in-ci-cd-pipelines.md).
        """
    )


def lab_for(num: int, slug: str, title: str, key: str) -> str:
    base = dedent(
        f"""\
        ### Step 1 — Lab workspace

        ```bash
        mkdir -p ~/rebash-cicd/{slug} && cd ~/rebash-cicd/{slug}
        git init -b main
        echo "# {title}" > README.md
        ```

        ### Step 2 — GitLab CI configuration

        Add `.gitlab-ci.yml` using the example in Theory. Tailor scripts to a minimal Python project:

        ```bash
        echo 'print("ok")' > app.py
        echo 'def test_ok(): assert True' > test_app.py
        pip freeze > requirements.txt 2>/dev/null || echo pytest > requirements.txt
        ```

        ### Step 3 — Push to GitLab.com or dry-run locally

        **GitLab.com (free tier):** create a private project, add the remote, push, and open a merge
        request. Confirm pipeline stages in the MR widget.

        **Local dry-run:** validate YAML without spending CI minutes (see Lint section below).

        ### Step 4 — Evidence capture

        Save a screenshot or log excerpt to `evidence/notes.md` describing stage order, artefact names,
        runner tags used, and any manual approval you configured.
        """
    )
    extras = {
        "mr-triggers": dedent(
            """\
            ### Step 5 — Merge request pipeline lab

            Create a feature branch, push, and open an MR:

            ```bash
            git checkout -b feature/pipeline-demo
            echo "# demo" >> README.md
            git add README.md .gitlab-ci.yml
            git commit -m "Add GitLab CI pipeline"
            git push -u origin feature/pipeline-demo
            ```

            In GitLab, open the MR and confirm a **merge request pipeline** runs. Merge to `main` and
            confirm a **branch pipeline** on the default branch.
            """
        ),
        "runners": dedent(
            """\
            ### Step 5 — Runner inspection (optional self-hosted)

            If you register a local runner:

            ```bash
            gitlab-runner list
            gitlab-runner verify
            ```

            Assign tags in `.gitlab-ci.yml` and confirm the job lands on your runner in job logs
            (`Running on ...`).
            """
        ),
        "runner-tags": dedent(
            """\
            ### Step 5 — Tag routing lab

            Add two jobs with different `tags:` and observe queue behaviour when only one runner
            matches. Document queue time in `evidence/notes.md`.
            """
        ),
        "docker": dedent(
            """\
            ### Step 5 — Docker build lab extension

            Add a `Dockerfile`:

            ```dockerfile
            FROM python:3.12-slim
            WORKDIR /app
            COPY . .
            CMD ["python", "app.py"]
            ```

            Extend `.gitlab-ci.yml` with build/push stages using `$CI_REGISTRY_*` variables —
            never commit passwords.
            """
        ),
        "kubernetes": dedent(
            """\
            ### Step 5 — Kubernetes manifest (dry-run)

            ```bash
            kubectl apply --dry-run=client -f deploy.yaml
            ```

            Deploy jobs should use a dedicated service account with RBAC limited to one namespace —
            see [Kubernetes track](../kubernetes/index.md).
            """
        ),
        "deploy": dedent(
            """\
            ### Step 5 — Environment tracking

            Add `environment: name` and `url` to staging deploy job. After a successful run, open
            **Deployments → Environments** in GitLab and confirm history appears.
            """
        ),
        "capstone": dedent(
            """\
            ### Step 5 — Capstone integration checklist

            Your final GitLab pipeline must include: lint, unit test, container build, vulnerability
            scan, manual production deploy, and a documented handoff to
            [Terraform in CI/CD Pipelines](../terraform/terraform-in-ci-cd-pipelines.md) for
            infrastructure changes.
            """
        ),
    }
    return base + "\n\n" + extras.get(key, "")


def dry_run_for(key: str) -> str:
    cmds = {
        "gitlab": "glab ci lint .gitlab-ci.yml 2>/dev/null || python3 -c \"import yaml; yaml.safe_load(open('.gitlab-ci.yml'))\"",
        "docker": "docker build -f Dockerfile . --check 2>/dev/null || docker buildx build --help | head -3",
        "scanning": "trivy fs --severity HIGH,CRITICAL . 2>/dev/null | tail -5 || echo 'Install trivy locally'",
    }
    default = """glab ci lint .gitlab-ci.yml 2>/dev/null || python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml'))"
gitlab-ci-local --file .gitlab-ci.yml 2>/dev/null || echo 'Optional: npm i -g gitlab-ci-local'"""
    return cmds.get(key, default)


def tags_for(key: str, slug: str) -> list[str]:
    base = ["cicd", "gitlab", "gitlab-ci"]
    extra = {
        "docker": ["docker"],
        "kubernetes": ["kubernetes"],
        "scanning": ["security", "devsecops"],
        "capstone": ["capstone", "terraform"],
        "mr-triggers": ["merge-requests"],
        "runners": ["runners"],
        "runner-tags": ["runners", "scaling"],
        "production": ["production"],
        "deploy": ["deployment"],
    }.get(key, [])
    return base + extra


def prereq_for(num: int) -> list[str]:
    if num == 1:
        return [
            "Completed the [Git](../git/index.md) fundamentals track",
            "Comfortable editing YAML and shell scripts",
            "GitLab.com account (free tier) or local lint tools",
        ]
    if num == 20:
        return [
            "Completed tutorials 1–19 or equivalent GitLab CI experience",
            "Familiarity with [Docker](../docker/index.md) and [Kubernetes](../kubernetes/index.md) basics",
            "Ready to connect pipelines to [Terraform](../terraform/index.md)",
        ]
    return [
        f"Completed tutorial {num - 1} in this track (or equivalent GitLab CI awareness)",
        "Lab repository from prior tutorials or a fresh `git init` workspace",
    ]


def emit_tutorial(num, slug, title, module, difficulty, minutes, snippet_key, focus_key) -> dict:
    sn = SNIPPETS[snippet_key]
    theory = theory_for(focus_key, title)
    theory_tail = dedent(
        f"""\
        ### Production notes for {title}

        Teams standardise GitLab CI templates but still integrate with external systems — container
        registries, Kubernetes clusters, and cloud OIDC roles. Document **{FOCUS[focus_key]}** in your
        internal runbook: who approves `.gitlab-ci.yml` changes, which runners touch production
        credentials, and how rollbacks interact with [Git](../git/index.md) revert versus forward fix.

        ### Related tutorials in this module

        Module progression builds depth: earlier tutorials establish vocabulary; later ones add security
        scanning, environment gates, and cloud deploy identities. If a job fails, read the job trace
        top-down and compare `rules:` against `CI_*` predefined variables — avoid deprecated
        `only/except` syntax from older examples.
        """
    )
    objectives = [
        f"Explain how {title.lower()} applies in GitLab CI production pipelines",
        "Author and validate `.gitlab-ci.yml` for the concepts in this tutorial",
        "Choose appropriate runners, tags, and variables for the workload",
        "Connect this topic to merge request workflows and branch protection",
        "Troubleshoot a failed GitLab CI job using logs and lint tools",
    ]
    if focus_key == "capstone":
        objectives.append("Produce a capstone GitLab pipeline and Terraform handoff checklist")

    mistakes = [
        ("Using deprecated `only/except`", "Breaks on upgrade and confuses reviewers.", "Use `rules:` and `workflow:rules`."),
        ("Secrets in Git", "Credential leak and audit failure.", "Use GitLab CI/CD variables and OIDC."),
        ("Skipping lint locally", "Wasted runner minutes.", "Run `glab ci lint` or `gitlab-ci-local` before push."),
    ]
    interview_q = [
        f"How does {title} work in GitLab CI?",
        "Where should secrets live in GitLab CI/CD?",
        "What triggers merge request pipelines vs branch pipelines?",
        "How do artefacts differ from container images in GitLab?",
        "Explain least privilege for a GitLab deploy job.",
        "What is the blast radius of a compromised runner?",
        "How would you roll back a bad deploy in GitLab?",
        "When is matrix parallelism worth the runner cost?",
        "How do protected environments help in GitLab?",
        "What comes after this track in the REBASH curriculum?",
    ]
    tips = [
        (1, f"GitLab CI expresses {title} through `.gitlab-ci.yml` jobs, `stages`, and `rules:`. Merge request pipelines use `CI_PIPELINE_SOURCE=merge_request_event`; default branch pipelines use push sources. Map each concept to the predefined variables GitLab injects."),
        (5, "Deploy jobs should use protected environment-scoped variables and dedicated runners — never a broad admin cloud key on shared MR runners."),
    ]
    refs = [
        ("GitLab CI/CD YAML reference", "https://docs.gitlab.com/ee/ci/yaml/"),
        ("GitLab Runner documentation", "https://docs.gitlab.com/runner/"),
        ("GitLab CI/CD variables", "https://docs.gitlab.com/ee/ci/variables/"),
        ("REBASH Terraform in CI/CD", "https://rebash.academy/terraform/terraform-in-ci-cd-pipelines/"),
    ]
    if num == 20:
        refs.append(("GitLab OIDC for cloud deploys", "https://docs.gitlab.com/ee/ci/cloud_services/"))

    related_extra = None
    if num == 20:
        related_extra = [
            "- Next track: [Terraform in CI/CD Pipelines](../terraform/terraform-in-ci-cd-pipelines.md)",
            "- [DevOps Engineer learning path](../learning-paths/devops-engineer.md)",
        ]

    return {
        "num": num,
        "slug": slug,
        "title": title,
        "module": module,
        "difficulty": difficulty,
        "minutes": minutes,
        "tags": tags_for(focus_key, slug),
        "prereq": prereq_for(num),
        "overview": dedent(
            f"""\
            {title} is essential for engineers who operate GitLab CI in production — not only the team
            that maintains runners. This lesson covers **{FOCUS[focus_key]}** with practical
            `.gitlab-ci.yml` examples you can lint locally and run on GitLab.com free tier.

            Other CI platforms exist and are covered in later REBASH tracks; here GitLab CI is the
            focus. You will relate concepts to [Git](../git/index.md) merge requests, and prepare for
            secure deploy patterns connecting to [Docker](../docker/index.md),
            [Kubernetes](../kubernetes/index.md), and
            [Terraform](../terraform/terraform-in-ci-cd-pipelines.md).
            """
        ),
        "objectives": objectives,
        "architecture_notes": dedent(
            """\
            | Layer | Responsibility |
            |-------|----------------|
            | **Trigger** | Git push, MR, tag, schedule, manual |
            | **Pipeline** | `.gitlab-ci.yml` automation definition in Git |
            | **Runner** | Isolated compute executing job scripts |
            | **Artefacts & cache** | Outputs and dependency acceleration |
            | **Deploy target** | GitLab environment, cluster, or cloud account |
            """
        ),
        "theory_lead": theory,
        "theory_tail": theory_tail,
        "example_title": sn["example_title"],
        "platform_key": snippet_key,
        "lab": lab_for(num, slug, title, focus_key),
        "dry_run": dry_run_for(focus_key),
        "validation": dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | `.gitlab-ci.yml` | Valid YAML; `glab ci lint` or equivalent passes |
            | Lint/dry-run | Local validation documented in lab notes |
            | Optional CI run | Pipeline green on MR or default branch |
            | Notes | `evidence/notes.md` explains stages, runners, and credentials used |
            """
        ),
        "walkthrough": dedent(
            """\
            | Section | GitLab CI detail |
            |---------|------------------|
            | Entry file | `.gitlab-ci.yml` at repository root |
            | Isolation | `image:` keyword and runner executor |
            | Conditional execution | `rules:` and `workflow:rules` |
            | Manual gate | `when: manual` or protected environment |
            | MR integration | Pipeline widget, test reports, coverage |

            Read job traces top-down: clone failure, missing variable, script non-zero exit, artefact
            upload error, runner tag mismatch.
            """
        ),
        "security": dedent(
            """\
            - Never print secrets; verify GitLab masking in job logs after first run
            - Scope CI/CD variables to environments and protected branches
            - Pin container images to semver or digest
            - Run untrusted MR jobs on isolated runners without production credentials
            - Rotate tokens used in tutorial labs; they are not production patterns
            """
        ),
        "mistakes": mistakes,
        "best_practices": dedent(
            """\
            - Pin runner images; schedule periodic base image upgrades
            - Keep pipelines fast — cache dependencies, split slow integration tests
            - Use merge request pipelines for feedback before merging to default branch
            - Document rollback: revert commit vs redeploy previous image digest
            - Align pipeline changes with [Git](../git/index.md) branch protection rules
            """
        ),
        "troubleshooting": dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | Job skipped | `rules:` mismatch | Log `CI_PIPELINE_SOURCE` and branch variables |
            | Permission denied | Wrong variable scope or OIDC trust | Fix protected variable or cloud role |
            | Docker daemon error | DinD misconfiguration | Set `DOCKER_TLS_CERTDIR`; verify `services:` |
            | Stuck pending | No runner matches tags | Add tagged runner or fix job `tags:` |
            | MR pipeline missing | `workflow:rules` too strict | Allow `merge_request_event` source |
            """
        ),
        "summary": dedent(
            f"""\
            - {title} is implemented in GitLab CI through `.gitlab-ci.yml`, runners, and merge request workflows
            - Validate locally with `glab ci lint` or `gitlab-ci-local` before spending runner minutes
            - Security and branch protection are part of pipeline design, not an afterthought
            - Continue sequentially or jump to related [Docker](../docker/index.md) and [Terraform](../terraform/index.md) material when ready
            """
        ),
        "interview_q": interview_q,
        "interview_tips": tips,
        "refs": refs,
        "related_extra": related_extra,
        "platform_focus": FOCUS[focus_key],
    }
