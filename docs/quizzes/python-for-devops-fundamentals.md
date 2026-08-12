---
title: "Quiz — Python for DevOps Fundamentals"
description: "40-question Python for DevOps quiz covering foundations, data/config, subprocess and APIs, platform automation, and production patterns."
difficulty: intermediate
estimated_time: "45–60 min"
passing_score: "70% (28/40)"
author: Shaik Basha
last_updated: "2026-07-29"
category: quizzes
tags:
  - quizzes
  - python
  - devops
  - assessment
comments: false
---

# Quiz — Python for DevOps Fundamentals

!!! tip "Updated quiz"
    Prefer the current course assessment: [Python for DevOps Engineers Fundamentals](python-for-devops-engineers-fundamentals.md) (27-module curriculum).


## Quiz Overview

Assess production-oriented Python skills for DevOps, platform, and SRE engineers.

| Attribute | Value |
|-----------|--------|
| Topic | Python for DevOps |
| Questions | 40 |
| Passing score | 70% (28 correct) |
| Estimated time | 45–60 minutes |
| Format | Multiple choice (single answer) |

!!! tip "Updated quiz available"
    Prefer the rewritten course assessment: **[Quiz — Python for DevOps Engineers Fundamentals](python-for-devops-engineers-fundamentals.md)** (40 questions covering all 27 modules). This page remains as a legacy practice set.

!!! tip "How to use this quiz"
    Select an answer for each question, then **Submit quiz** for a scored result. Progress is saved in this browser. Explanations unlock after you submit.

## Learning Objectives

This quiz assesses whether you can:

- [ ] Choose Python vs Bash appropriately and use venvs safely
- [ ] Work with pathlib, JSON/YAML, regex, and secrets hygiene
- [ ] Call subprocess and HTTP APIs without common footguns
- [ ] Reason about Docker/K8s/GitHub automation blast radius
- [ ] Apply pytest, packaging, and dry-run production patterns


## Section 1 — Module 1 Foundations

### Question 1

In DevOps work, Python is primarily best at:

**Difficulty:** Beginner

**Options:**

- **A.** Structured data, APIs, tests, and packaged CLIs
- **B.** Replacing the Linux kernel
- **C.** GPU training as a first-class ops tool
- **D.** Editing binary firmware images

??? success "Reveal answer"
    **Correct answer: A**

    Bash remains strong for glue; Python owns structure and libraries.

    **Related concepts**

    - Python vs Bash
    - Ops automation

### Question 2

Which command creates a virtual environment in the current directory?

**Difficulty:** Beginner

**Options:**

- **A.** `pip freeze > .venv`
- **B.** `python3 -m venv .venv`
- **C.** `virtualenv --system-site-packages /`
- **D.** `conda init bash` only

??? success "Reveal answer"
    **Correct answer: B**

    Stdlib `venv` is the default teaching path on REBASH Academy.

    **Related concepts**

    - venv

### Question 3

Why pin dependency versions for ops tooling?

**Difficulty:** Beginner

**Options:**

- **A.** To make `import` case-insensitive
- **B.** To disable HTTPS
- **C.** So CI and laptops resolve the same packages
- **D.** To avoid writing README files

??? success "Reveal answer"
    **Correct answer: C**

    Reproducibility beats “latest” for automation.

    **Related concepts**

    - dependency pinning

### Question 4

A function should signal a usage error to shell callers by:

**Difficulty:** Intermediate

**Options:**

- **A.** Printing only to stdout and exiting 0
- **B.** Raising `BaseException` with no handling
- **C.** Hanging until timeout
- **D.** Mapping to a documented non-zero exit code (e.g. 2)

??? success "Reveal answer"
    **Correct answer: D**

    Automation’s API is exit status plus clear stderr.

    **Related concepts**

    - exceptions vs exit codes

### Question 5

Which logging habit is safest for ops scripts?

**Difficulty:** Beginner

**Options:**

- **A.** Log levels and messages without secrets or tokens
- **B.** Log every environment variable at DEBUG
- **C.** Print API keys to help “debug auth”
- **D.** Disable logging in production always

??? success "Reveal answer"
    **Correct answer: A**

    Secrets in logs become incidents.

    **Related concepts**

    - logging
    - secrets

### Question 6

`if __name__ == "__main__":` is used to:

**Difficulty:** Beginner

**Options:**

- **A.** Force multiprocessing
- **B.** Run CLI entry code only when the file is executed as a script
- **C.** Disable imports permanently
- **D.** Compile to C automatically

??? success "Reveal answer"
    **Correct answer: B**

    Keeps modules importable for tests.

    **Related concepts**

    - project layout

### Question 7

What does activating a venv primarily change?

**Difficulty:** Beginner

**Options:**

- **A.** The system package manager
- **B.** DNS resolution
- **C.** Which `python`/`pip` are first on PATH for that shell
- **D.** Kubernetes contexts

??? success "Reveal answer"
    **Correct answer: C**

    Isolation is per environment, not magic global safety.

    **Related concepts**

    - venv

### Question 8

Prefer catching which exception type for expected operational failures?

**Difficulty:** Intermediate

**Options:**

- **A.** `KeyboardInterrupt` only
- **B.** Bare `except:`
- **C.** `BaseException`
- **D.** Specific exceptions (e.g. `ValueError`, `OSError`) then map to exit codes

??? success "Reveal answer"
    **Correct answer: D**

    Bare `except` hides bugs and Ctrl-C issues.

    **Related concepts**

    - error handling


## Section 2 — Module 2 Data and Configuration

### Question 9

`Path("logs") / "app.log"` demonstrates:

**Difficulty:** Beginner

**Options:**

- **A.** Joining path parts with pathlib in an OS-safe way
- **B.** Opening a network socket
- **C.** Compiling regex
- **D.** Installing PyYAML

??? success "Reveal answer"
    **Correct answer: A**

    Prefer pathlib over string concatenation.

    **Related concepts**

    - pathlib

### Question 10

Which YAML loader should DevOps tooling use by default?

**Difficulty:** Beginner

**Options:**

- **A.** `yaml.load` with no Loader
- **B.** `yaml.safe_load`
- **C.** `eval` on the file text
- **D.** `pickle.load`

??? success "Reveal answer"
    **Correct answer: B**

    Unsafe loaders can execute objects.

    **Related concepts**

    - YAML safety

### Question 11

Named groups in regex help because they:

**Difficulty:** Intermediate

**Options:**

- **A.** Disable Unicode
- **B.** Require shell=True
- **C.** Make captures readable via `groupdict()` / names
- **D.** Encrypt log lines

??? success "Reveal answer"
    **Correct answer: C**

    Clearer than opaque group numbers.

    **Related concepts**

    - re

### Question 12

Where should production API tokens live?

**Difficulty:** Intermediate

**Options:**

- **A.** Hard-coded in source
- **B.** Committed `.env` in Git
- **C.** Tutorial screenshots
- **D.** Environment variables or a secret store — never the repo

??? success "Reveal answer"
    **Correct answer: D**

    Rotate anything that was ever committed.

    **Related concepts**

    - secrets hygiene

### Question 13

`json.dumps(obj, indent=2)` is useful to:

**Difficulty:** Beginner

**Options:**

- **A.** Serialise a Python object to a readable JSON string
- **B.** Start a Kubernetes cluster
- **C.** Validate TLS certificates
- **D.** Pin pip packages

??? success "Reveal answer"
    **Correct answer: A**

    Pair with `json.dump` for files.

    **Related concepts**

    - JSON

### Question 14

Config precedence commonly taught for CLIs is:

**Difficulty:** Intermediate

**Options:**

- **A.** Random each run
- **B.** Defaults, then file, then env, then CLI flags (highest wins)
- **C.** CLI flags ignored when a file exists
- **D.** Env always loses to hard-coded constants

??? success "Reveal answer"
    **Correct answer: B**

    Document precedence for operators.

    **Related concepts**

    - configuration patterns

### Question 15

Reading untrusted log/config input safely means:

**Difficulty:** Intermediate

**Options:**

- **A.** Assuming all files are trusted root
- **B.** Running `exec` on each line
- **C.** Bounding size, validating schema, and avoiding code execution loaders
- **D.** Disabling all error handling

??? success "Reveal answer"
    **Correct answer: C**

    Treat inputs as hostile by default.

    **Related concepts**

    - parsing untrusted input

### Question 16

`pathlib.Path.glob("*.log")` returns:

**Difficulty:** Beginner

**Options:**

- **A.** A single string path always
- **B.** Kubernetes Pods
- **C.** Compiled regex objects
- **D.** An iterator of matching Path objects

??? success "Reveal answer"
    **Correct answer: D**

    Ideal for multi-file analysers.

    **Related concepts**

    - pathlib


## Section 3 — Module 3 System and Network

### Question 17

The safest common `subprocess` pattern is:

**Difficulty:** Intermediate

**Options:**

- **A.** `subprocess.run(["tool", arg], check=True, text=True)` with list args
- **B.** `os.system(user_input)`
- **C.** `subprocess.run(user_input, shell=True)`
- **D.** Ignoring return codes always

??? success "Reveal answer"
    **Correct answer: A**

    List argv avoids shell injection.

    **Related concepts**

    - subprocess

### Question 18

Why avoid `shell=True` with untrusted input?

**Difficulty:** Intermediate

**Options:**

- **A.** It makes Python faster
- **B.** Metacharacters can inject extra shell commands
- **C.** It disables networking
- **D.** It is required by POSIX forever

??? success "Reveal answer"
    **Correct answer: B**

    Classic interview footgun.

    **Related concepts**

    - shell=True

### Question 19

httpx (or requests) calls in automation should:

**Difficulty:** Intermediate

**Options:**

- **A.** Never set timeouts
- **B.** Retry infinitely without backoff
- **C.** Always set timeouts (and sensible retries)
- **D.** Log full Authorization headers

??? success "Reveal answer"
    **Correct answer: C**

    Hung HTTP is a common CI failure mode.

    **Related concepts**

    - httpx timeouts

### Question 20

`argparse` primarily helps you:

**Difficulty:** Beginner

**Options:**

- **A.** Render SVG diagrams
- **B.** Manage kubeconfig encryption
- **C.** Train ML models
- **D.** Define CLI flags and parse `sys.argv` into structured options

??? success "Reveal answer"
    **Correct answer: D**

    Typer/Click build on the same idea with less boilerplate.

    **Related concepts**

    - argparse

### Question 21

A dry-run flag for destructive automation should:

**Difficulty:** Intermediate

**Options:**

- **A.** Default to on (simulate) until an explicit apply/force
- **B.** Default to deleting resources immediately
- **C.** Be undocumented
- **D.** Only exist in Bash, never Python

??? success "Reveal answer"
    **Correct answer: A**

    Reduce blast radius by default.

    **Related concepts**

    - dry-run
    - production patterns

### Question 22

Paramiko is typically used to:

**Difficulty:** Intermediate

**Options:**

- **A.** Parse YAML only
- **B.** Automate SSH sessions from Python
- **C.** Replace TLS entirely
- **D.** Build Docker images without a daemon

??? success "Reveal answer"
    **Correct answer: B**

    Prefer keys/agents; never hard-code passwords in repos.

    **Related concepts**

    - SSH automation

### Question 23

When an HTTP API returns 401, automation should:

**Difficulty:** Intermediate

**Options:**

- **A.** Print the token and retry
- **B.** Treat it as success
- **C.** Fail clearly (auth/config error) without leaking secrets
- **D.** Disable HTTPS

??? success "Reveal answer"
    **Correct answer: C**

    Distinguish auth failures from transient 5xx.

    **Related concepts**

    - API authentication

### Question 24

Typer/Click are preferred over raw `sys.argv` splits when:

**Difficulty:** Beginner

**Options:**

- **A.** You need no help text
- **B.** You only ever have one flag
- **C.** You want to avoid type hints
- **D.** You want structured multi-command CLIs with less boilerplate

??? success "Reveal answer"
    **Correct answer: D**

    Still keep exit codes and logging consistent.

    **Related concepts**

    - Typer
    - Click


## Section 4 — Module 4 Platform Automation

### Question 25

A GitHub personal access token in CI should be:

**Difficulty:** Intermediate

**Options:**

- **A.** Stored as a masked/secret CI variable with least scopes
- **B.** Echoed in job logs for debugging
- **C.** Committed under `secrets/token.txt`
- **D.** Shared in Slack screenshots

??? success "Reveal answer"
    **Correct answer: A**

    Fine-grained, rotatable, minimal scopes.

    **Related concepts**

    - GitHub API
    - secrets

### Question 26

Docker cleanup automation should default to:

**Difficulty:** Intermediate

**Options:**

- **A.** `prune -af` without prompts on every run
- **B.** Listing / dry-run first; mutate only with an explicit apply flag
- **C.** Deleting all volumes nightly without inventory
- **D.** Running as root over NFS home directories blindly

??? success "Reveal answer"
    **Correct answer: B**

    Blast radius control is the interview answer.

    **Related concepts**

    - Docker SDK
    - dry-run

### Question 27

Kubernetes Python clients in beginner ops tools should usually:

**Difficulty:** Advanced

**Options:**

- **A.** Default to cluster-admin writes
- **B.** Skip namespaces for convenience
- **C.** Prefer read/list health checks with explicit namespace scope
- **D.** Embed kubeconfig private keys in the repo

??? success "Reveal answer"
    **Correct answer: C**

    Least privilege and clear scope.

    **Related concepts**

    - Kubernetes client
    - blast radius

### Question 28

Wrapping Terraform with Python is most useful to:

**Difficulty:** Intermediate

**Options:**

- **A.** Replace the Terraform binary entirely
- **B.** Avoid state files forever
- **C.** Disable plan in CI
- **D.** Orchestrate validate/plan, parse JSON output, and report safely

??? success "Reveal answer"
    **Correct answer: D**

    Keep Terraform as source of truth for IaC.

    **Related concepts**

    - Terraform automation

### Question 29

Idempotent inventory collection means:

**Difficulty:** Intermediate

**Options:**

- **A.** Re-running the collector does not mutate infrastructure by itself
- **B.** Every run deletes and recreates clusters
- **C.** Results must be non-deterministic
- **D.** Tests are forbidden

??? success "Reveal answer"
    **Correct answer: A**

    Reads and reports should be safe to schedule.

    **Related concepts**

    - idempotency

### Question 30

Python in CI/CD pipelines should:

**Difficulty:** Intermediate

**Options:**

- **A.** Rely on interactive prompts
- **B.** Fail fast with non-zero exits and pinned deps in the job image/venv
- **C.** Download random wheels without hashes forever
- **D.** Disable test jobs to save minutes always

??? success "Reveal answer"
    **Correct answer: B**

    Same rules as production scripts — automated and deterministic.

    **Related concepts**

    - Python in CI

### Question 31

A high blast-radius risk is:

**Difficulty:** Advanced

**Options:**

- **A.** Printing help text
- **B.** Reading a ConfigMap
- **C.** A script that deletes namespaces or prunes volumes without dry-run or scope checks
- **D.** Listing Docker images

??? success "Reveal answer"
    **Correct answer: C**

    Interviewers look for safety design, not only SDKs.

    **Related concepts**

    - blast radius

### Question 32

For platform automation tests in CI, prefer:

**Difficulty:** Intermediate

**Options:**

- **A.** Live production clusters as the only suite
- **B.** Real cloud bills on every commit
- **C.** Unbounded `sleep` flakiness
- **D.** Mocked clients/fixtures offline, with optional gated integration jobs

??? success "Reveal answer"
    **Correct answer: D**

    Fast feedback without credentials.

    **Related concepts**

    - pytest strategy


## Section 5 — Module 5 Production Engineering

### Question 33

Async Python is most justified in ops tools when:

**Difficulty:** Advanced

**Options:**

- **A.** You have many concurrent I/O-bound calls (HTTP/SSH)
- **B.** You need to sort a 10-element list
- **C.** You want to avoid type hints
- **D.** You must disable logging

??? success "Reveal answer"
    **Correct answer: A**

    Do not async everything by default.

    **Related concepts**

    - async I/O

### Question 34

A solid pytest strategy for DevOps CLIs starts with:

**Difficulty:** Intermediate

**Options:**

- **A.** Only manual clicks in production
- **B.** Unit tests for parsers/flags with fixtures; mock external systems
- **C.** Skipping assertions
- **D.** Requiring AWS root keys in every developer laptop

??? success "Reveal answer"
    **Correct answer: B**

    Test behaviour you own; gate live integrations.

    **Related concepts**

    - pytest

### Question 35

`[project.scripts]` in `pyproject.toml` defines:

**Difficulty:** Intermediate

**Options:**

- **A.** Docker base images
- **B.** Kubernetes CRDs
- **C.** Console entry points so a command installs on PATH
- **D.** DNS records

??? success "Reveal answer"
    **Correct answer: C**

    Packaging makes tools shareable.

    **Related concepts**

    - packaging
    - entry points

### Question 36

`uv sync` (or Poetry install) in a project primarily:

**Difficulty:** Intermediate

**Options:**

- **A.** Formats Markdown only
- **B.** Creates cloud VPCs
- **C.** Publishes to PyPI automatically always
- **D.** Installs the locked/declared environment reproducibly

??? success "Reveal answer"
    **Correct answer: D**

    Pair with CI using the same lock.

    **Related concepts**

    - uv
    - Poetry

### Question 37

Production patterns for destructive commands emphasise:

**Difficulty:** Advanced

**Options:**

- **A.** Dry-run defaults, least privilege, structured logging, and clear exit codes
- **B.** Silent failures
- **C.** Global mutable state with no tests
- **D.** Committing credentials “for convenience”

??? success "Reveal answer"
    **Correct answer: A**

    Matches the course capstone bar.

    **Related concepts**

    - production patterns

### Question 38

Capstone frameworks should include CI that runs:

**Difficulty:** Intermediate

**Options:**

- **A.** Only `echo success`
- **B.** Lint + pytest (no live cloud required)
- **C.** Manual SSH to prod as the test
- **D.** `terraform destroy` on every PR

??? success "Reveal answer"
    **Correct answer: B**

    See course §10 success criteria.

    **Related concepts**

    - capstone
    - CI

### Question 39

Shared libraries in a DevOps framework typically provide:

**Difficulty:** Intermediate

**Options:**

- **A.** A full operating system
- **B.** Unrelated frontend CSS
- **C.** Logging, config, secrets loading, and an HTTP client with retries
- **D.** Hard-coded production passwords

??? success "Reveal answer"
    **Correct answer: C**

    Avoid copy-paste across plugins.

    **Related concepts**

    - framework skeleton

### Question 40

After `pip install -e .` (or `uv sync`), operators should be able to:

**Difficulty:** Beginner

**Options:**

- **A.** Only run code by pasting into a REPL forever
- **B.** Edit `/usr/bin` by hand each time
- **C.** Avoid README instructions entirely
- **D.** Invoke the console script from PATH for dry-run commands quickly

??? success "Reveal answer"
    **Correct answer: D**

    Capstone onboarding target: clone → sync → test → dry-run in minutes.

    **Related concepts**

    - packaging
    - operator experience

## Scoring

| Score | Result |
|------:|--------|
| 36–40 | Excellent — ready for platform automation review |
| 28–35 | Pass — revisit weak sections |
| <28 | Re-work Modules 1–3 labs and the log analyser before projects |

## Recommended Study Areas

- [Install, venv, and Tooling](../python/python-fundamentals-install-venv-and-tooling.md)
- [Virtual Environments and Dependency Pinning](../python/python-fundamentals-install-venv-and-tooling.md)
- [subprocess — Calling CLI Tools Safely](../python/linux-automation-subprocess-and-psutil.md)
- [Environment Variables, dotenv, and Secrets Hygiene](../python/configuration-management-and-secrets.md)
- [Production Patterns for DevOps Python](../python/production-engineering-patterns.md)
- Lab: [Python Log Analyser](../labs/python-log-analyser.md)
- Cheat sheet: [Python](../cheatsheets/python.md)
