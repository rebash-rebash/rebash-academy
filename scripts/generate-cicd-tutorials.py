#!/usr/bin/env python3
"""Generate REBASH Academy GitLab CI/CD tutorials 1–20 under docs/gitlab/."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "gitlab"
AUTHOR = "Shaik Basha"
LAST_UPDATED = "2026-07-28"

TUTORIALS: list[dict] = []


def T(**kwargs: object) -> None:
    TUTORIALS.append(kwargs)


def render_mistakes(mistakes: list[tuple[str, str, str]]) -> str:
    return "\n\n".join(
        f'!!! warning "{title}"\n    {why} **Fix:** {fix}' for title, why, fix in mistakes
    )


def render_interview(questions: list[str], tips: list[tuple[int, str]]) -> str:
    lines = [f"{i}. {q}" for i, q in enumerate(questions, 1)]
    body = "\n".join(lines)
    tip_blocks = "\n\n".join(
        dedent(
            f"""\
            !!! tip "Sample answer — question {n}"
                {ans}
            """
        )
        for n, ans in tips
    )
    return f"{body}\n\n{tip_blocks}" if tip_blocks else body


def related_links(num: int, slug: str, extra: list[str] | None = None) -> str:
    slugs = {t["num"]: t for t in TUTORIALS}
    titles = {t["num"]: t["title"] for t in TUTORIALS}
    links = ["- Track overview: [GitLab CI/CD](index.md)"]
    if num > 1 and (num - 1) in titles:
        prev = slugs[num - 1]
        links.append(f"- Previous: [{prev['title']}]({prev['slug']}.md)")
    if num < 20 and (num + 1) in titles:
        nxt = slugs[num + 1]
        links.append(f"- Next: [{nxt['title']}]({nxt['slug']}.md)")
    if extra:
        links.extend(extra)
    return "\n".join(links)


def cross_links_section() -> str:
    return dedent(
        """\
        ## Cross-track links

        - [Git](../git/index.md) — branching, merge requests, and review workflows pipelines depend on
        - [Docker](../docker/index.md) — images built and scanned in CI
        - [Kubernetes](../kubernetes/index.md) — deploy targets for GitOps and progressive delivery
        - [Terraform](../terraform/index.md) — especially [Terraform in CI/CD Pipelines](../terraform/terraform-in-ci-cd-pipelines.md)
        - [AWS](../aws/index.md) — cloud credentials, OIDC, and deployment targets
        """
    )


def free_tier_reminder() -> str:
    return dedent(
        """\
        !!! tip "Free-tier and local lab options"
            Use **GitLab.com** free tier for real pipeline runs. Where a cloud runner is optional,
            each lab includes a **lint / dry-run** path with `glab ci lint`, Python YAML parsing, or
            **gitlab-ci-local** so you can validate `.gitlab-ci.yml` without spending CI minutes.
        """
    )


def dry_run_tip(commands: str) -> str:
    return dedent(
        f"""\
        ### Lint / dry-run alternative

        Validate pipeline syntax without executing jobs:

        ```bash
        {commands.strip()}
        ```

        Dry-run paths prove structure and variable references; they do not replace an end-to-end run
        on a real runner when you are learning job isolation and artefact behaviour.
        """
    )


def gitlab_example(title: str, yaml_body: str) -> str:
    return dedent(
        f"""\
        ### {title}

        ```yaml
        {yaml_body.strip()}
        ```
        """
    )


EXTENDED_BLOCKS: dict[str, str] = {}


def _register_extended(slug: str, body: str) -> None:
    EXTENDED_BLOCKS[slug] = dedent(body).strip()


def extended_deep_dive(t: dict) -> str:
    slug = t["slug"]
    title = t["title"]
    module = t["module"]
    extras = EXTENDED_BLOCKS.get(slug, "")
    platform_note = t.get("platform_focus", "GitLab CI")
    return dedent(
        f"""\
        ## Production Patterns and Deep Dive

        ### How `{title}` fits in real environments

        Teams shipping through **{module}** concepts use these patterns in design reviews, pipeline
        migrations, and incident retrospectives. The lab proves you can author valid GitLab CI
        configuration; this section connects those files to trade-offs you will defend in interviews
        and on-call handovers focused on **{platform_note}**.

        Production GitLab CI programmes typically document:

        | Artefact | Purpose |
        |----------|---------|
        | Pipeline architecture diagram | Stages, triggers, credentials, and deploy targets |
        | Runbook | How to re-run, roll back, or disable a job safely |
        | Credential rotation procedure | Who rotates tokens, OIDC trust, and protected variables |
        | Cost / minute budget | Runner sizing, cache strategy, and concurrency limits |

        Always pair automation with **least privilege**, **branch protection**, and **auditable**
        deploy gates. The REBASH GitLab CI/CD track uses British English and assumes you completed
        [Git](../git/index.md) fundamentals first.

        ### Extended CLI and validation reference

        The commands below extend the lab — run lint and dry-run variants first, then execute on
        GitLab.com or a self-hosted runner when you need to observe artefacts, caches, and environment
        propagation.

        {extras}

        ### Operational scenario (table-top)

        **Scenario:** A teammate merges to `main` and production deploy fails with "permission denied"
        on a step related to **{title}**.

        | Step | Action | Why |
        |------|--------|-----|
        | 1 | Open the failed job trace; note stage, image, runner, and identity used | Wrong credential is the top cause |
        | 2 | Compare branch protection and protected environment rules | Protected branches block secrets or deploys |
        | 3 | Re-run the job with `CI_DEBUG_TRACE=true` where appropriate | Surfaces masked variable issues |
        | 4 | Diff `.gitlab-ci.yml` against last green commit | Recent YAML change is likely |
        | 5 | Roll forward with a fix or revert merge | Document in incident ticket |
        | 6 | Add a lint gate so the misconfiguration fails in the MR pipeline | Prevents repeat |

        ### Hardening checklist before production

        - [ ] Short-lived credentials (OIDC) preferred over long-lived PATs or access keys
        - [ ] Secrets in GitLab CI/CD variables — never committed to Git
        - [ ] Untrusted MR pipelines run on runners without production credentials
        - [ ] Deploy jobs require manual approval or protected environments
        - [ ] Container images pinned by digest where feasible
        - [ ] SBOM or vulnerability scan stage on default branch
        - [ ] Cross-links reviewed: [Docker](../docker/index.md), [Kubernetes](../kubernetes/index.md), [Terraform](../terraform/index.md)

        ### Terraform handoff note

        Infrastructure changes belong in [Terraform](../terraform/index.md). After this track,
        reproduce deploy and plan/apply gates using
        [Terraform in CI/CD Pipelines](../terraform/terraform-in-ci-cd-pipelines.md): plan on merge
        requests, apply on protected branches with OIDC, and store remote state with locking.

        ### Review questions (self-check)

        Before moving to the next tutorial, answer without looking at notes:

        1. Which `.gitlab-ci.yml` keywords implement this concept?
        2. What is the least-privilege identity this job should use?
        3. How would you validate YAML locally before pushing?
        4. Where do artefacts and caches differ in retention and security?
        5. Which [Git](../git/index.md) workflow rule prevents broken `main`?

        ### Additional references

        Bookmark official GitLab documentation for **{title}**. Note default runner images, quota
        limits, and which pipeline sources consume shared runner minutes so your team can forecast cost
        alongside [Docker](../docker/index.md) build times.
        """
    )


def render(t: dict) -> str:
    num = t["num"]
    tags_yaml = "\n".join(f"  - {x}" for x in t["tags"])
    prereq_yaml = "\n".join(f"  - {x}" for x in t["prereq"])
    prereq_body = "\n".join(f"- {x}" for x in t["prereq"])
    objectives = "\n".join(f"- [ ] {x}" for x in t["objectives"])
    mistakes = render_mistakes(t["mistakes"])
    interview = render_interview(t["interview_q"], t.get("interview_tips", []))
    related = related_links(num, t["slug"], t.get("related_extra"))
    refs = "\n".join(f"{i}. [{n}]({u})" for i, (n, u) in enumerate(t["refs"], 1))
    desc = t["overview"].strip().splitlines()[0][:160]
    extra_warnings = t.get("extra_warnings", "")
    deep_dive = extended_deep_dive(t)
    arch_notes = t.get("architecture_notes", "").strip()

    return f"""---
title: {t['title']}
description: "{desc.replace('"', "'")}"
difficulty: {t['difficulty']}
estimated_time: "{t['minutes']}"
author: {AUTHOR}
last_updated: "{LAST_UPDATED}"
category: gitlab
tags:
{tags_yaml}
prerequisites:
{prereq_yaml}
comments: false
---

# {t['title']}

## Overview

{t['overview'].strip()}

This is **Tutorial {num}** in **{t['module']}** of the REBASH Academy **GitLab CI/CD** track.

{free_tier_reminder().strip()}

{extra_warnings.strip()}

## Prerequisites

{prereq_body}

## Learning Objectives

By the end of this tutorial, you will be able to:

{objectives}

## Architecture

![Architecture diagram for {t['title']}](../assets/images/{t['slug']}.svg)

{arch_notes}

## Theory

{t['theory'].strip()}

## Hands-on Lab

{t['lab'].strip()}

## Validation

{t['validation'].strip()}

## Code Walkthrough

{t['walkthrough'].strip()}

## Security Considerations

{t['security'].strip()}

## Common Mistakes

{mistakes}

## Best Practices

{t['best_practices'].strip()}

## Troubleshooting

{t['troubleshooting'].strip()}

{deep_dive.strip()}

## Summary

{t['summary'].strip()}

## Interview Questions

{interview}

## Related Tutorials

{related}

{cross_links_section().strip()}

## References

{refs}
"""


def populate_extended_blocks() -> None:
    _register_extended(
        "introduction-to-cicd-and-delivery-models",
        """
        ```bash
        test -f .gitlab-ci.yml && echo "GitLab CI present"
        git log --oneline -5
        glab ci lint .gitlab-ci.yml 2>/dev/null || true
        ```
        """,
    )
    _register_extended(
        "pipeline-anatomy-stages-jobs-and-artifacts",
        """
        ```bash
        glab ci lint .gitlab-ci.yml 2>/dev/null || echo "Install glab or use GitLab UI CI Lint"
        grep -E '^[a-z0-9_-]+:' .gitlab-ci.yml | head -20
        grep -E 'artifacts:|cache:|needs:' .gitlab-ci.yml
        ```
        """,
    )
    _register_extended(
        "gitlab-ci-fundamentals",
        """
        ```bash
        glab ci lint .gitlab-ci.yml
        glab ci list --per-page 5
        glab ci trace --branch "$(git branch --show-current)" 2>/dev/null | tail -20
        ```
        """,
    )
    _register_extended(
        "gitlab-merge-requests-and-pipeline-triggers",
        """
        ```bash
        glab mr list --per-page 5
        glab ci list --source merge_request_event 2>/dev/null || glab ci list
        grep -E 'workflow:|rules:|CI_PIPELINE_SOURCE' .gitlab-ci.yml
        ```
        """,
    )
    _register_extended(
        "gitlab-runners-and-executors",
        """
        ```bash
        gitlab-runner list 2>/dev/null || echo "Register runner in lab first"
        gitlab-runner verify 2>/dev/null || true
        grep -E 'tags:|image:' .gitlab-ci.yml
        ```
        """,
    )
    _register_extended(
        "gitlab-runner-tags-and-scaling",
        """
        ```bash
        gitlab-runner list 2>/dev/null || true
        grep -E 'tags:|parallel:' .gitlab-ci.yml
        ```
        """,
    )
    _register_extended(
        "variables-secrets-and-credentials",
        """
        ```bash
        grep -R 'password\\|token\\|secret' .gitlab-ci.yml 2>/dev/null | grep -v '\\$' || true
        glab variable list 2>/dev/null | head
        ```
        """,
    )
    _register_extended(
        "triggers-rules-and-branch-protection",
        """
        ```bash
        glab api projects/:id/protected_branches 2>/dev/null | head
        git config --get-regexp 'branch\\.main\\.'
        grep -E 'rules:|workflow:' .gitlab-ci.yml
        ```
        """,
    )
    _register_extended(
        "building-docker-images-in-ci",
        """
        ```bash
        docker build --dry-run . 2>/dev/null || docker buildx build --help | head -5
        docker scout quickview 2>/dev/null || echo "Optional: Docker Scout for image summary"
        syft packages dir:. 2>/dev/null || echo "Optional: Syft SBOM locally"
        ```
        """,
    )
    _register_extended(
        "testing-reports-and-quality-gates",
        """
        ```bash
        pytest --junitxml=report.xml -q 2>/dev/null || echo "Generate JUnit in lab"
        test -f report.xml && xmllint --noout report.xml 2>/dev/null && echo "JUnit XML valid"
        ```
        """,
    )
    _register_extended(
        "artifacts-caches-and-dependencies",
        """
        ```bash
        du -sh .cache 2>/dev/null || true
        ls -la dist/ target/ node_modules/.cache 2>/dev/null | head
        grep -E 'cache:|artifacts:' .gitlab-ci.yml
        ```
        """,
    )
    _register_extended(
        "parallelism-matrix-and-pipeline-dags",
        """
        ```bash
        grep -E 'needs:|parallel:|matrix:' .gitlab-ci.yml
        glab ci lint .gitlab-ci.yml 2>/dev/null || true
        ```
        """,
    )
    _register_extended(
        "least-privilege-ci-identities",
        """
        ```bash
        aws sts get-caller-identity 2>/dev/null || echo "Configure OIDC role for cloud deploy labs"
        glab auth status 2>/dev/null
        grep -E 'id_tokens:|CI_JOB_JWT' .gitlab-ci.yml 2>/dev/null || true
        ```
        """,
    )
    _register_extended(
        "security-scanning-in-pipelines",
        """
        ```bash
        trivy fs --severity HIGH,CRITICAL . 2>/dev/null | tail -15
        semgrep --config auto --error --quiet . 2>/dev/null | tail -10 || echo "Install semgrep for local scan"
        ```
        """,
    )
    _register_extended(
        "secret-detection-and-supply-chain-basics",
        """
        ```bash
        gitleaks detect --source . --no-git -v 2>/dev/null | tail -10 || echo "Install gitleaks"
        pip-audit 2>/dev/null || npm audit --audit-level=high 2>/dev/null | tail -5
        ```
        """,
    )
    _register_extended(
        "protected-environments-and-approvals",
        """
        ```bash
        glab api projects/:id/protected_environments 2>/dev/null | head
        grep -E 'environment:|when: manual' .gitlab-ci.yml
        ```
        """,
    )
    _register_extended(
        "gitlab-deployment-patterns",
        """
        ```bash
        kubectl config current-context 2>/dev/null || echo "Optional K8s context for deploy lab"
        helm list 2>/dev/null || true
        grep -E 'environment:' .gitlab-ci.yml
        ```
        """,
    )
    _register_extended(
        "kubernetes-deploys-from-ci",
        """
        ```bash
        kubectl auth can-i create deployments --namespace=default 2>/dev/null
        kubectl get deploy,svc -A 2>/dev/null | head -10
        helm template ./chart 2>/dev/null | head -30
        ```
        """,
    )
    _register_extended(
        "gitlab-ci-production-patterns",
        """
        ```bash
        grep -E 'include:|component:' .gitlab-ci.yml
        glab ci lint .gitlab-ci.yml 2>/dev/null || true
        ```
        """,
    )
    _register_extended(
        "cicd-capstone-and-terraform-handoff",
        """
        ```bash
        terraform fmt -check -recursive 2>/dev/null || echo "Continue in Terraform track"
        terraform validate 2>/dev/null || true
        glab ci lint .gitlab-ci.yml 2>/dev/null || true
        ```
        """,
    )


def main() -> None:
    populate_extended_blocks()
    OUT.mkdir(parents=True, exist_ok=True)
    for t in TUTORIALS:
        path = OUT / f"{t['slug']}.md"
        text = render(t)
        path.write_text(text, encoding="utf-8")
        size = path.stat().st_size
        status = "OK" if size >= 11_000 else "SHORT"
        print(f"{path.relative_to(ROOT)}\t{size}\t{status}")
    short = [t for t in TUTORIALS if (OUT / f"{t['slug']}.md").stat().st_size < 11_000]
    if short:
        print(f"WARNING: {len(short)} tutorials under 11k bytes")
    print(f"done — {len(TUTORIALS)} tutorials")


def load_tutorials() -> None:
    import importlib.util

    path = Path(__file__).parent / "_build_cicd_registry.py"
    spec = importlib.util.spec_from_file_location("cicd_build", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    build_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build_mod)

    snippets = build_mod.SNIPPETS
    for args in build_mod.TUTORIALS:
        meta = build_mod.emit_tutorial(*args)
        sn = snippets[meta["platform_key"]]
        example = gitlab_example(meta["example_title"], sn["gitlab"])
        theory = dedent(meta["theory_lead"]) + "\n\n" + example + "\n\n" + dedent(meta["theory_tail"])
        lab = dedent(meta["lab"]) + "\n\n" + dry_run_tip(meta["dry_run"])
        T(
            num=meta["num"],
            slug=meta["slug"],
            title=meta["title"],
            module=meta["module"],
            difficulty=meta["difficulty"],
            minutes=meta["minutes"],
            tags=meta["tags"],
            prereq=meta["prereq"],
            overview=dedent(meta["overview"]),
            objectives=meta["objectives"],
            architecture_notes=dedent(meta["architecture_notes"]),
            theory=theory,
            lab=lab,
            validation=dedent(meta["validation"]),
            walkthrough=dedent(meta["walkthrough"]),
            security=dedent(meta["security"]),
            mistakes=meta["mistakes"],
            best_practices=dedent(meta["best_practices"]),
            troubleshooting=dedent(meta["troubleshooting"]),
            summary=dedent(meta["summary"]),
            interview_q=meta["interview_q"],
            interview_tips=meta["interview_tips"],
            refs=meta["refs"],
            related_extra=meta.get("related_extra"),
            platform_focus=meta["platform_focus"],
        )


if __name__ == "__main__":
    load_tutorials()
    main()
