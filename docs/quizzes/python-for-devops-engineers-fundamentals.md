---
title: "Quiz — Python for DevOps Engineers Fundamentals"
description: "40-question quiz covering all 27 modules of Python for DevOps Engineers — foundations through production, cloud, Kubernetes, and security."
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

# Quiz — Python for DevOps Engineers Fundamentals

## Quiz Overview

Assess production-oriented Python skills for DevOps, platform, and SRE engineers across the full course.

| Attribute | Value |
|-----------|--------|
| Topic | Python for DevOps Engineers |
| Questions | 40 |
| Passing score | 70% (28 correct) |
| Estimated time | 45–60 minutes |
| Format | Multiple choice (single answer) |
| Answer key balance | 10 × A · 10 × B · 10 × C · 10 × D |

!!! tip "How to use this quiz"
    Attempt each section without peeking. Use **Reveal answer** only after you commit to a choice. Covers Modules 1–27.

## Learning Objectives

This quiz assesses whether you can:

- [ ] Use venvs, types, control flow, functions, and data structures for ops scripts
- [ ] Handle files, YAML/JSON, exceptions, logging, and configuration safely
- [ ] Build CLIs and call subprocess/HTTP/cloud APIs without common footguns
- [ ] Reason about Docker, Kubernetes, Terraform, and GitHub automation blast radius
- [ ] Apply pytest, packaging, security, concurrency, and production patterns


## Section 1 — Language foundations (Modules 1–5)

### Question 1

In DevOps work, Python is primarily best at:

**Difficulty:** Beginner

**Module focus:** Module 1 — Fundamentals

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

**Module focus:** Module 1 — Fundamentals

**Options:**

- **A.** pip freeze > .venv
- **B.** python3 -m venv .venv
- **C.** virtualenv --system-site-packages /
- **D.** conda init bash only

??? success "Reveal answer"
    **Correct answer: B**

    Stdlib venv is the default teaching path.

    **Related concepts**

    - venv

### Question 3

Why pin dependency versions for ops tooling?

**Difficulty:** Beginner

**Module focus:** Module 1 — Fundamentals

**Options:**

- **A.** To make imports case-insensitive
- **B.** To disable TLS in pip
- **C.** So CI and laptops resolve the same known-good versions
- **D.** To force use of the system site-packages

??? success "Reveal answer"
    **Correct answer: C**

    Reproducible environments reduce “works on my machine” failures.

    **Related concepts**

    - pip
    - uv
    - Poetry

### Question 4

Which built-in converts the string "42" to an integer?

**Difficulty:** Beginner

**Module focus:** Module 2 — Basics

**Options:**

- **A.** str(42)
- **B.** repr("42")
- **C.** ord("42")
- **D.** int("42")

??? success "Reveal answer"
    **Correct answer: D**

    int() parses decimal strings; validate input before converting.

    **Related concepts**

    - types
    - conversion

### Question 5

What does bool("") evaluate to?

**Difficulty:** Beginner

**Module focus:** Module 2 — Basics

**Options:**

- **A.** False
- **B.** True
- **C.** None
- **D.** Raises ValueError

??? success "Reveal answer"
    **Correct answer: A**

    Empty strings are falsy in Python.

    **Related concepts**

    - booleans
    - truthiness

### Question 6

Which keyword skips the rest of the current loop iteration?

**Difficulty:** Beginner

**Module focus:** Module 3 — Control flow

**Options:**

- **A.** break
- **B.** continue
- **C.** pass
- **D.** return

??? success "Reveal answer"
    **Correct answer: B**

    continue moves to the next iteration; break exits the loop.

    **Related concepts**

    - loops

### Question 7

In Python 3.10+, structural pattern matching uses which keyword?

**Difficulty:** Beginner

**Module focus:** Module 3 — Control flow

**Options:**

- **A.** switch
- **B.** select
- **C.** match
- **D.** caseof

??? success "Reveal answer"
    **Correct answer: C**

    match/case is the modern branching form for structured values.

    **Related concepts**

    - match

### Question 8

What does *args collect in a function signature?

**Difficulty:** Beginner

**Module focus:** Module 4 — Functions

**Options:**

- **A.** Keyword-only arguments into a dict
- **B.** Only default argument values
- **C.** Decorators applied to the function
- **D.** Extra positional arguments into a tuple

??? success "Reveal answer"
    **Correct answer: D**

    *args is a tuple of extra positionals; **kwargs is a dict.

    **Related concepts**

    - parameters
    - scope

### Question 9

Why prefer default argument None then assign a new list inside the function?

**Difficulty:** Intermediate

**Module focus:** Module 4 — Functions

**Options:**

- **A.** Mutable defaults are shared across calls if created in the signature
- **B.** None cannot be compared
- **C.** Lists cannot be typed
- **D.** Python forbids empty lists as locals

??? success "Reveal answer"
    **Correct answer: A**

    Classic pitfall: def f(x=[]) mutates the same list.

    **Related concepts**

    - defaults
    - mutability

### Question 10

Which structure stores unique unordered elements?

**Difficulty:** Beginner

**Module focus:** Module 5 — Data structures

**Options:**

- **A.** list
- **B.** set
- **C.** tuple
- **D.** dict

??? success "Reveal answer"
    **Correct answer: B**

    Sets deduplicate membership tests efficiently.

    **Related concepts**

    - set


## Section 2 — Files, errors, OOP, logging, config, CLI (Modules 6–12)

### Question 11

What does (x*x for x in nums) create?

**Difficulty:** Intermediate

**Module focus:** Module 5 — Data structures

**Options:**

- **A.** A list of squares
- **B.** A set of squares
- **C.** A generator object
- **D.** An immediate tuple of squares

??? success "Reveal answer"
    **Correct answer: C**

    Parentheses with a comprehension-like form yield a generator.

    **Related concepts**

    - generators

### Question 12

What does if __name__ == "__main__": guard?

**Difficulty:** Beginner

**Module focus:** Module 6 — Modules

**Options:**

- **A.** Code that runs only inside packages
- **B.** Code that disables imports
- **C.** Code that forces asyncio
- **D.** Code that should run only when the file is executed as a script

??? success "Reveal answer"
    **Correct answer: D**

    Importing the module will not execute the guarded main block.

    **Related concepts**

    - modules

### Question 13

Which pathlib call reads a whole text file as a string?

**Difficulty:** Beginner

**Module focus:** Module 7 — File handling

**Options:**

- **A.** Path.read_text(encoding="utf-8")
- **B.** Path.open_bytes()
- **C.** Path.glob()
- **D.** Path.mkdir()

??? success "Reveal answer"
    **Correct answer: A**

    Prefer explicit encoding for ops scripts.

    **Related concepts**

    - pathlib

### Question 14

Which YAML loader should automation use for untrusted files?

**Difficulty:** Intermediate

**Module focus:** Module 7 — File handling

**Options:**

- **A.** yaml.load with FullLoader only on Fridays
- **B.** yaml.safe_load
- **C.** yaml.unsafe_load
- **D.** yaml.full_load_all without checks

??? success "Reveal answer"
    **Correct answer: B**

    safe_load avoids arbitrary object construction.

    **Related concepts**

    - YAML
    - security

### Question 15

Which block always runs after try whether or not an exception occurred?

**Difficulty:** Beginner

**Module focus:** Module 8 — Errors

**Options:**

- **A.** except
- **B.** else
- **C.** finally
- **D.** raise

??? success "Reveal answer"
    **Correct answer: C**

    finally is for cleanup (close files, release locks).

    **Related concepts**

    - exceptions

### Question 16

What does raise ConfigError("bad") from exc accomplish?

**Difficulty:** Intermediate

**Module focus:** Module 8 — Errors

**Options:**

- **A.** Suppresses the original exception
- **B.** Converts the error to a warning
- **C.** Retries the operation once
- **D.** Chains exceptions preserving the cause

??? success "Reveal answer"
    **Correct answer: D**

    Exception chaining aids debugging in ops tools.

    **Related concepts**

    - raise from

### Question 17

What is a primary benefit of @dataclass for inventory records?

**Difficulty:** Intermediate

**Module focus:** Module 9 — OOP

**Options:**

- **A.** It auto-generates init/repr for declared fields
- **B.** It disables typing
- **C.** It forces inheritance from dict
- **D.** It runs only on PyPy

??? success "Reveal answer"
    **Correct answer: A**

    Less boilerplate for structured ops data.

    **Related concepts**

    - dataclasses

### Question 18

Which logging level is appropriate for a handled, unexpected failure of an API call?

**Difficulty:** Beginner

**Module focus:** Module 10 — Logging

**Options:**

- **A.** DEBUG
- **B.** ERROR
- **C.** INFO
- **D.** NOTSET

??? success "Reveal answer"
    **Correct answer: B**

    ERROR signals failed actions; avoid logging secrets at any level.

    **Related concepts**

    - logging

### Question 19

Where should production secrets for a CLI live?

**Difficulty:** Intermediate

**Module focus:** Module 11 — Configuration

**Options:**

- **A.** Hard-coded in source
- **B.** Committed .env in git
- **C.** Environment variables or a secret store
- **D.** Docstrings

??? success "Reveal answer"
    **Correct answer: C**

    Never commit secrets; load from env/secret managers.

    **Related concepts**

    - secrets
    - dotenv

### Question 20

In argparse, which action stores a boolean flag as True when present?

**Difficulty:** Beginner

**Module focus:** Module 12 — CLI

**Options:**

- **A.** action="append"
- **B.** action="count" only
- **C.** type=bool with default "false" string
- **D.** action="store_true"

??? success "Reveal answer"
    **Correct answer: D**

    store_true is the usual pattern for --json / --apply flags.

    **Related concepts**

    - argparse


## Section 3 — Automation platforms (Modules 13–20)

### Question 21

Click and Typer are mainly used to:

**Difficulty:** Intermediate

**Module focus:** Module 12 — CLI

**Options:**

- **A.** Build friendlier multi-command CLIs with options
- **B.** Compile C extensions
- **C.** Replace systemd
- **D.** Provision VPCs natively

??? success "Reveal answer"
    **Correct answer: A**

    They layer ergonomics on top of argparse-like concepts.

    **Related concepts**

    - Click
    - Typer

### Question 22

What is the safer subprocess pattern?

**Difficulty:** Intermediate

**Module focus:** Module 13 — Linux automation

**Options:**

- **A.** subprocess.run("rm -rf " + path, shell=True)
- **B.** subprocess.run(["rm", "-rf", path], check=True)
- **C.** os.system(f"rm -rf {path}")
- **D.** eval("rm -rf " + path)

??? success "Reveal answer"
    **Correct answer: B**

    List argv avoids shell injection.

    **Related concepts**

    - subprocess

### Question 23

What should every HTTP client used in CI set?

**Difficulty:** Intermediate

**Module focus:** Module 14 — REST APIs

**Options:**

- **A.** Infinite retries with no jitter
- **B.** Verify=False always
- **C.** Timeouts for connect and read
- **D.** Global monkey-patched sockets

??? success "Reveal answer"
    **Correct answer: C**

    Missing timeouts hang pipelines.

    **Related concepts**

    - requests
    - httpx

### Question 24

How should labs/tests inventory EC2 without credentials?

**Difficulty:** Intermediate

**Module focus:** Module 15 — Cloud

**Options:**

- **A.** Embed long-lived access keys in the repo
- **B.** Disable SSL and scrape the console HTML
- **C.** Call the metadata service from GitHub-hosted runners blindly
- **D.** Use fixture JSON shaped like describe_instances

??? success "Reveal answer"
    **Correct answer: D**

    Fixture/dry-run paths keep learning credential-free.

    **Related concepts**

    - boto3
    - fixtures

### Question 25

A GitHub repository auditor in CI should default to:

**Difficulty:** Intermediate

**Module focus:** Module 16 — Git automation

**Options:**

- **A.** Read-only tokens or fixture responses
- **B.** Admin tokens that can delete repos
- **C.** Force-pushing to main for fixes
- **D.** Printing PATs in debug logs

??? success "Reveal answer"
    **Correct answer: A**

    Least privilege and fixtures for offline CI.

    **Related concepts**

    - GitHub API

### Question 26

Before deleting dangling images, a production-safe tool should:

**Difficulty:** Intermediate

**Module focus:** Module 17 — Docker

**Options:**

- **A.** Always prune volumes and networks
- **B.** Report first and require an explicit --apply
- **C.** Require root SSH to every host
- **D.** Run docker system prune -af with no prompts

??? success "Reveal answer"
    **Correct answer: B**

    Dry-run defaults reduce blast radius.

    **Related concepts**

    - Docker SDK

### Question 27

How should unit tests exercise a Kubernetes health checker without a cluster?

**Difficulty:** Intermediate

**Module focus:** Module 18 — Kubernetes

**Options:**

- **A.** Require a live production kubeconfig
- **B.** Skip all tests if kubectl is missing
- **C.** Load fixture Pod/Deployment JSON
- **D.** Hard-code admin credentials in fixtures

??? success "Reveal answer"
    **Correct answer: C**

    Fixture paths keep CI hermetic.

    **Related concepts**

    - kubernetes client

### Question 28

A Python Terraform wrapper for CI should summarise plans by:

**Difficulty:** Intermediate

**Module focus:** Module 19 — Terraform

**Options:**

- **A.** Automatically applying on green builds
- **B.** Scraping coloured ANSI logs only
- **C.** Editing terraform.tfstate in place
- **D.** Parsing terraform show -json / saved plan JSON

??? success "Reveal answer"
    **Correct answer: D**

    Plan JSON is stable for automation; never silent apply.

    **Related concepts**

    - Terraform

### Question 29

When automating remote commands with Paramiko, prefer:

**Difficulty:** Intermediate

**Module focus:** Module 20 — SSH

**Options:**

- **A.** Key-based auth with strict host key policy in production
- **B.** Password auth committed in YAML
- **C.** shell=True local wrappers around ssh
- **D.** Disabling host key checks permanently in production

??? success "Reveal answer"
    **Correct answer: A**

    Keys + verified host keys reduce MitM and secret sprawl.

    **Related concepts**

    - Paramiko

### Question 30

For many independent HTTP health probes, a good default is:

**Difficulty:** Intermediate

**Module focus:** Module 21 — Concurrency

**Options:**

- **A.** One giant GIL-free CPU process per URL always
- **B.** Threads or asyncio with bounded concurrency and timeouts
- **C.** No timeouts so probes can wait forever
- **D.** Multiprocessing for every 1 ms CPU task

??? success "Reveal answer"
    **Correct answer: B**

    I/O-bound work fits threads/asyncio; always bound and time out.

    **Related concepts**

    - asyncio
    - futures


## Section 4 — Concurrency, testing, packaging, production (Modules 21–27)

### Question 31

What does a pytest fixture typically provide?

**Difficulty:** Beginner

**Module focus:** Module 22 — Testing

**Options:**

- **A.** A replacement for virtualenvs
- **B.** Automatic cloud credentials
- **C.** Reusable setup data/resources for tests
- **D.** A Makefile target only

??? success "Reveal answer"
    **Correct answer: C**

    Fixtures inject temp paths, configs, and fakes.

    **Related concepts**

    - pytest

### Question 32

Unit tests for cloud CLIs should:

**Difficulty:** Intermediate

**Module focus:** Module 22 — Testing

**Options:**

- **A.** Always bill real AWS accounts
- **B.** Skip assertions on exit codes
- **C.** Require interactive TTY approval
- **D.** Mock SDKs or use fixtures; gate live tests separately

??? success "Reveal answer"
    **Correct answer: D**

    Keep default CI offline and deterministic.

    **Related concepts**

    - mocking

### Question 33

Where do you declare a console script entry point in modern packaging?

**Difficulty:** Intermediate

**Module focus:** Module 23 — Packaging

**Options:**

- **A.** In pyproject.toml under [project.scripts]
- **B.** Only in a random .bashrc
- **C.** Inside a Dockerfile ENTRYPOINT exclusively
- **D.** In /etc/environment

??? success "Reveal answer"
    **Correct answer: A**

    pip/uv install then exposes the command on PATH.

    **Related concepts**

    - pyproject
    - wheels

### Question 34

Exponential backoff is used to:

**Difficulty:** Intermediate

**Module focus:** Module 24 — Production patterns

**Options:**

- **A.** Speed up successful GETs only
- **B.** Space out retries after transient failures
- **C.** Delete cloud resources faster
- **D.** Compress log files

??? success "Reveal answer"
    **Correct answer: B**

    Backoff + jitter protects APIs and your job.

    **Related concepts**

    - retries

### Question 35

A secrets scanner finding an AKIA… key in git should trigger:

**Difficulty:** Intermediate

**Module focus:** Module 25 — Security

**Options:**

- **A.** Ignoring it if the commit is old
- **B.** Committing the key to a private branch only
- **C.** Immediate rotation and treating it as compromised
- **D.** Printing the full key in Slack for visibility

??? success "Reveal answer"
    **Correct answer: C**

    Assume leak; rotate; purge history if needed.

    **Related concepts**

    - secrets scanning

### Question 36

When using LLMs or MCP clients in ops automation, you should:

**Difficulty:** Beginner

**Module focus:** Module 26 — AI for DevOps

**Options:**

- **A.** Paste production secrets into prompts for context
- **B.** Let the model apply terraform without review
- **C.** Disable all logging around AI tools
- **D.** Treat outputs as untrusted and keep humans/gates on mutations

??? success "Reveal answer"
    **Correct answer: D**

    AI assists; policy and dry-run still own blast radius.

    **Related concepts**

    - OpenAI
    - MCP
    - LangChain

### Question 37

A cron Python job fails with ModuleNotFoundError but works in your shell. Likely cause?

**Difficulty:** Intermediate

**Module focus:** Module 27 — Troubleshooting

**Options:**

- **A.** Cron uses a different interpreter/PATH without the venv
- **B.** Python forbids cron on Linux
- **C.** pytest is required for imports
- **D.** JSON cannot be imported at night

??? success "Reveal answer"
    **Correct answer: A**

    Point cron at the venv’s absolute python path.

    **Related concepts**

    - venv
    - cron

### Question 38

httpx hangs in CI with no response. Best first fix?

**Difficulty:** Advanced

**Module focus:** Module 14/24 — Resilience

**Options:**

- **A.** Remove HTTPS
- **B.** Set explicit client timeouts and fail fast
- **C.** Increase parallelism unboundedly
- **D.** Disable DNS

??? success "Reveal answer"
    **Correct answer: B**

    Timeouts turn hangs into actionable failures.

    **Related concepts**

    - timeouts

### Question 39

Kubernetes automation that can patch Deployments should run as:

**Difficulty:** Advanced

**Module focus:** Module 18/25 — Production

**Options:**

- **A.** cluster-admin for convenience
- **B.** anonymous unauthenticated access
- **C.** A least-privilege ServiceAccount scoped to needed verbs/namespaces
- **D.** root on every node via SSH

??? success "Reveal answer"
    **Correct answer: C**

    RBAC least privilege is mandatory.

    **Related concepts**

    - RBAC
    - ServiceAccount

### Question 40

Default behaviour for a Docker cleanup CLI in shared CI agents should be:

**Difficulty:** Advanced

**Module focus:** Module 17/24 — Production

**Options:**

- **A.** Immediate prune of all unused volumes
- **B.** Delete every image including those in use
- **C.** Restart Docker Engine on each run
- **D.** Dry-run report unless --apply is passed

??? success "Reveal answer"
    **Correct answer: D**

    Report-first protects shared builders.

    **Related concepts**

    - dry-run
    - Docker

## Answer key summary

| Answer | Count | Question numbers |
|--------|-------|------------------|
| A | 10 | 1, 5, 9, 13, 17, 21, 25, 29, 33, 37 |
| B | 10 | 2, 6, 10, 14, 18, 22, 26, 30, 34, 38 |
| C | 10 | 3, 7, 11, 15, 19, 23, 27, 31, 35, 39 |
| D | 10 | 4, 8, 12, 16, 20, 24, 28, 32, 36, 40 |


## Related

- Track: [Python for DevOps](../python/index.md)
- Cheat sheet: [Python](../cheatsheets/python.md)
- Interview: [Python interview prep](../interview/python.md)
- Labs: [Python Log Analyser](../labs/python-log-analyser.md)
- Capstone: [Production DevOps Automation Platform](../projects/python-devops-automation-framework.md)
- Learning path: [Python for DevOps Engineers](../learning-paths/python-for-devops.md)
