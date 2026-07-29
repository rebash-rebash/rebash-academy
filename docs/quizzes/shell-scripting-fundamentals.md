---
title: "Quiz — Shell Scripting Fundamentals"
description: "40-question Bash quiz covering quoting, strict mode, functions, getopts, traps, security, cron/systemd, and CI scripts."
difficulty: intermediate
estimated_time: "45–60 min"
passing_score: "70% (28/40)"
author: Shaik Basha
last_updated: "2026-07-29"
category: quizzes
tags:
  - quizzes
  - shell
  - bash
  - assessment
comments: false
---

# Quiz — Shell Scripting Fundamentals

!!! tip "Updated quiz available"
    For the rewritten **Shell Scripting for DevOps Engineers** course (all 18 modules), take [Shell Scripting for DevOps Fundamentals](shell-scripting-for-devops-fundamentals.md). This page remains as an alternate question bank.

## Quiz Overview

Assess production Bash skills for Linux admins and DevOps engineers.

| Attribute | Value |
|-----------|--------|
| Topic | Shell Scripting (Bash) |
| Questions | 40 |
| Passing score | 70% (28 correct) |
| Estimated time | 45–60 minutes |
| Format | Multiple choice (single answer) |

!!! tip "How to use this quiz"
    Attempt each section without peeking. Use **Reveal answer** only after you commit to a choice.

## Learning Objectives

This quiz assesses whether you can:

- [ ] Quote expansions and use strict mode correctly
- [ ] Write conditionals, loops, and functions safely
- [ ] Parse arguments and use arrays
- [ ] Apply traps, locks, and secure scripting habits
- [ ] Run scripts under cron/systemd and CI fail-fast patterns


## Section 1 — Fundamentals

### Question 1

What is Bash primarily best at in DevOps work?

**Difficulty:** Beginner

**Options:**

- **A.** Orchestrating OS tools and glue automation
- **B.** Long-lived multi-threaded services
- **C.** Replacing relational databases
- **D.** GPU training loops

??? success "Reveal answer"
    **Correct answer: A**

    Bash excels at composing commands and exit codes.

    **Related concepts**

    - Bash role
    - Ops glue

### Question 2

Which shebang is commonly recommended for portable Bash scripts?

**Difficulty:** Beginner

**Options:**

- **A.** #!/bin/zsh
- **B.** #!/usr/bin/env bash
- **C.** #!/usr/bin/python3
- **D.** #!bash

??? success "Reveal answer"
    **Correct answer: B**

    env looks up bash on PATH.

    **Related concepts**

    - shebang

### Question 3

On many Debian/Ubuntu systems, what is /bin/sh often?

**Difficulty:** Beginner

**Options:**

- **A.** Always Bash
- **B.** Always zsh
- **C.** dash (POSIX sh)
- **D.** fish

??? success "Reveal answer"
    **Correct answer: C**

    dash is common; Bashisms fail under it.

    **Related concepts**

    - POSIX
    - dash

### Question 4

Which expansion form is usually safest for a path with spaces?

**Difficulty:** Beginner

**Options:**

- **A.** $path
- **B.** `$path`
- **C.** Single-quoted literal $path
- **D.** "$path"

??? success "Reveal answer"
    **Correct answer: D**

    Double quotes expand but prevent word-splitting.

    **Related concepts**

    - quoting

### Question 5

What does set -u do?

**Difficulty:** Intermediate

**Options:**

- **A.** Treat unset variable expansions as errors
- **B.** Ignore unset variables
- **C.** Enable unicode
- **D.** Disable nounset

??? success "Reveal answer"
    **Correct answer: A**

    -u aborts on unset expansions.

    **Related concepts**

    - strict mode

### Question 6

Why enable pipefail?

**Difficulty:** Intermediate

**Options:**

- **A.** To make pipes faster
- **B.** So any failing stage fails the pipeline
- **C.** So only the last command status counts
- **D.** To disable pipelines

??? success "Reveal answer"
    **Correct answer: B**

    Without pipefail, earlier failures can be hidden.

    **Related concepts**

    - pipefail

### Question 7

Where should diagnostic logs usually go?

**Difficulty:** Beginner

**Options:**

- **A.** stdout only
- **B.** /dev/null always
- **C.** stderr
- **D.** The clipboard

??? success "Reveal answer"
    **Correct answer: C**

    Keep stdout for data; logs on stderr.

    **Related concepts**

    - logging

### Question 8

What exit code conventionally means success?

**Difficulty:** Beginner

**Options:**

- **A.** 1
- **B.** 255
- **C.** -1
- **D.** 0

??? success "Reveal answer"
    **Correct answer: D**

    0 is success for shells and cron.

    **Related concepts**

    - exit status


## Section 2 — Control Flow and Structure

### Question 9

In Bash, which test form is generally preferred?

**Difficulty:** Beginner

**Options:**

- **A.** [[ ... ]]
- **B.** ((( ... )))
- **C.** test without brackets only
- **D.** eval test

??? success "Reveal answer"
    **Correct answer: A**

    [[ is safer and richer in Bash.

    **Related concepts**

    - conditionals

### Question 10

Which test checks for a regular file?

**Difficulty:** Beginner

**Options:**

- **A.** -d
- **B.** -f
- **C.** -L only
- **D.** -z

??? success "Reveal answer"
    **Correct answer: B**

    -f is regular file.

    **Related concepts**

    - file tests

### Question 11

Why include a *) branch in case?

**Difficulty:** Intermediate

**Options:**

- **A.** It is required by POSIX for empty cases only
- **B.** To disable globbing
- **C.** To handle unexpected values and print usage
- **D.** To enable pipefail

??? success "Reveal answer"
    **Correct answer: C**

    Default branch fails closed on typos.

    **Related concepts**

    - case

### Question 12

Which read form is safest for arbitrary lines?

**Difficulty:** Intermediate

**Options:**

- **A.** read line
- **B.** read -a without IFS
- **C.** eval read
- **D.** IFS= read -r line

??? success "Reveal answer"
    **Correct answer: D**

    -r disables backslash escapes.

    **Related concepts**

    - read

### Question 13

What does shopt -s nullglob do?

**Difficulty:** Intermediate

**Options:**

- **A.** Makes unmatched globs expand to nothing
- **B.** Deletes all files
- **C.** Enables globstar only
- **D.** Disables globs

??? success "Reveal answer"
    **Correct answer: A**

    Prevents literal *.log when no matches.

    **Related concepts**

    - nullglob

### Question 14

How should you iterate all arguments safely?

**Difficulty:** Beginner

**Options:**

- **A.** for a in $*
- **B.** for a in "$@"
- **C.** for a in $@
- **D.** for a in "$*" only always

??? success "Reveal answer"
    **Correct answer: B**

    "$@" preserves argument boundaries.

    **Related concepts**

    - "$@"

### Question 15

What does local do in a function?

**Difficulty:** Intermediate

**Options:**

- **A.** Exports a variable
- **B.** Makes a variable readonly globally
- **C.** Scopes a variable to the function
- **D.** Creates an associative array

??? success "Reveal answer"
    **Correct answer: C**

    local avoids clobbering globals.

    **Related concepts**

    - functions

### Question 16

How do you load a library file in Bash?

**Difficulty:** Beginner

**Options:**

- **A.** #include
- **B.** import
- **C.** require
- **D.** source file.sh or . file.sh

??? success "Reveal answer"
    **Correct answer: D**

    source runs the file in the current shell.

    **Related concepts**

    - source


## Section 3 — Script Interfaces

### Question 17

What does getopts parse?

**Difficulty:** Intermediate

**Options:**

- **A.** Short options like -v
- **B.** Only long --options
- **C.** JSON only
- **D.** systemd units

??? success "Reveal answer"
    **Correct answer: A**

    getopts handles short flags.

    **Related concepts**

    - getopts

### Question 18

After getopts, how do you drop parsed flags?

**Difficulty:** Beginner

**Options:**

- **A.** unset all
- **B.** shift $((OPTIND-1))
- **C.** reset
- **D.** getopts -c

??? success "Reveal answer"
    **Correct answer: B**

    OPTIND points past options.

    **Related concepts**

    - getopts

### Question 19

Which Bash version adds associative arrays commonly used on Linux?

**Difficulty:** Intermediate

**Options:**

- **A.** Bash 1.x
- **B.** Bash 2.0 only
- **C.** Bash 4+
- **D.** Only zsh

??? success "Reveal answer"
    **Correct answer: C**

    declare -A needs Bash 4+.

    **Related concepts**

    - arrays

### Question 20

How do you append to an indexed array?

**Difficulty:** Beginner

**Options:**

- **A.** arr.push(x)
- **B.** arr[x]=append
- **C.** append arr x
- **D.** arr+=("x")

??? success "Reveal answer"
    **Correct answer: D**

    += appends elements.

    **Related concepts**

    - arrays

### Question 21

Safe iteration over array elements uses:

**Difficulty:** Intermediate

**Options:**

- **A.** "${arr[@]}"
- **B.** $arr
- **C.** ${arr*}
- **D.** unquoted ${arr[@]}

??? success "Reveal answer"
    **Correct answer: A**

    Quoted [@] preserves elements.

    **Related concepts**

    - arrays

### Question 22

Which tool is preferred for structured JSON in scripts?

**Difficulty:** Beginner

**Options:**

- **A.** only sed
- **B.** jq (or similar)
- **C.** notepad
- **D.** lspci

??? success "Reveal answer"
    **Correct answer: B**

    jq handles JSON reliably.

    **Related concepts**

    - jq

### Question 23

Why avoid parsing ls in scripts?

**Difficulty:** Intermediate

**Options:**

- **A.** ls is too fast
- **B.** ls cannot list files
- **C.** Filenames can contain spaces/newlines; ls is not a stable API
- **D.** ls requires root

??? success "Reveal answer"
    **Correct answer: C**

    Use globs/find -print0 instead.

    **Related concepts**

    - anti-patterns

### Question 24

For presence checks with grep under set -e, prefer:

**Difficulty:** Beginner

**Options:**

- **A.** grep pattern file always bare
- **B.** grep | true | true without if
- **C.** eval grep
- **D.** if grep -q pattern file; then ...; fi

??? success "Reveal answer"
    **Correct answer: D**

    if guards exit status under -e.

    **Related concepts**

    - grep
    - strict mode


## Section 4 — Production Hardening

### Question 25

What does trap ... EXIT do?

**Difficulty:** Intermediate

**Options:**

- **A.** Runs a handler when the shell exits
- **B.** Ignores all signals
- **C.** Disables errexit
- **D.** Starts cron

??? success "Reveal answer"
    **Correct answer: A**

    Useful for cleanup of temp dirs.

    **Related concepts**

    - trap

### Question 26

mktemp is preferred because:

**Difficulty:** Intermediate

**Options:**

- **A.** It creates world-writable /tmp/foo always
- **B.** It creates unique temp paths safely
- **C.** It disables SELinux
- **D.** It replaces flock

??? success "Reveal answer"
    **Correct answer: B**

    Avoid fixed temp names.

    **Related concepts**

    - mktemp

### Question 27

flock -n failing usually means:

**Difficulty:** Intermediate

**Options:**

- **A.** DNS failure
- **B.** Bash is too old
- **C.** Another process holds the lock
- **D.** pipefail is off

??? success "Reveal answer"
    **Correct answer: C**

    Non-blocking lock not acquired.

    **Related concepts**

    - flock

### Question 28

A common secure default for expansions is:

**Difficulty:** Beginner

**Options:**

- **A.** Always unquote
- **B.** Always eval
- **C.** Always use $*
- **D.** Always quote unless you intentionally need splitting

??? success "Reveal answer"
    **Correct answer: D**

    Quoting prevents injection/word-split.

    **Related concepts**

    - security

### Question 29

Why is eval dangerous with untrusted input?

**Difficulty:** Advanced

**Options:**

- **A.** It executes arbitrary shell code
- **B.** It is slow
- **C.** It disables aliases
- **D.** It only works on macOS

??? success "Reveal answer"
    **Correct answer: A**

    Attackers can inject commands.

    **Related concepts**

    - eval

### Question 30

Before rm -rf on a path from input you should:

**Difficulty:** Intermediate

**Options:**

- **A.** Run it as root immediately
- **B.** Validate prefix/realpath and quote
- **C.** Disable set -e
- **D.** Use eval rm

??? success "Reveal answer"
    **Correct answer: B**

    Fail closed on path validation.

    **Related concepts**

    - path validation

### Question 31

Secrets in scripts should be:

**Difficulty:** Beginner

**Options:**

- **A.** Hard-coded and committed
- **B.** Printed in CI logs for debug
- **C.** Injected via env/secret stores and never echoed
- **D.** Stored in world-readable files

??? success "Reveal answer"
    **Correct answer: C**

    Mask and restrict access.

    **Related concepts**

    - secrets

### Question 32

RESULT status=ok on stdout is useful because:

**Difficulty:** Intermediate

**Options:**

- **A.** It replaces exit codes
- **B.** It disables logging
- **C.** It is required by Bash
- **D.** Machines/CI can parse a stable summary line

??? success "Reveal answer"
    **Correct answer: D**

    Pairs with exit codes for automation.

    **Related concepts**

    - logging


## Section 5 — Ops, Schedulers, and CI/CD

### Question 33

Cron scripts often fail because:

**Difficulty:** Intermediate

**Options:**

- **A.** Minimal PATH and non-interactive env
- **B.** Cron forbids Bash
- **C.** Cron cannot redirect
- **D.** Exit codes are ignored always

??? success "Reveal answer"
    **Correct answer: A**

    Set PATH and avoid aliases.

    **Related concepts**

    - cron

### Question 34

systemd Type=oneshot is a good fit when:

**Difficulty:** Intermediate

**Options:**

- **A.** You need a lingering daemon by default
- **B.** The unit runs a finite script and exits
- **C.** You only use SysV init
- **D.** You cannot use timers

??? success "Reveal answer"
    **Correct answer: B**

    Oneshots pair with timers.

    **Related concepts**

    - systemd

### Question 35

In GitLab CI, prefer:

**Difficulty:** Beginner

**Options:**

- **A.** Huge inline scripts with secrets echoed
- **B.** Disabling failures globally
- **C.** Repo scripts invoked with set -euo pipefail
- **D.** Ignoring artefacts

??? success "Reveal answer"
    **Correct answer: C**

    Reviewable scripts and fail-fast.

    **Related concepts**

    - CI

### Question 36

A sensible toolkit layout is:

**Difficulty:** Intermediate

**Options:**

- **A.** One 2,000-line script only
- **B.** Only aliases in bashrc
- **C.** Windows .bat only
- **D.** bin/ CLIs + lib/common.sh

??? success "Reveal answer"
    **Correct answer: D**

    Small binaries sharing helpers.

    **Related concepts**

    - capstone

### Question 37

Idempotent scheduled jobs should:

**Difficulty:** Beginner

**Options:**

- **A.** Be safe/correct if run again
- **B.** Fail if run twice
- **C.** Delete random files
- **D.** Require interactive prompts

??? success "Reveal answer"
    **Correct answer: A**

    Overlap and retries happen.

    **Related concepts**

    - idempotency

### Question 38

When should you leave Bash for Python?

**Difficulty:** Advanced

**Options:**

- **A.** Never
- **B.** Complex data/APIs/typing needs beyond glue
- **C.** Only for printing hello
- **D.** When PATH is set

??? success "Reveal answer"
    **Correct answer: B**

    Bash remains the launcher.

    **Related concepts**

    - language choice

### Question 39

bash -x is used to:

**Difficulty:** Intermediate

**Options:**

- **A.** Cross-compile Bash
- **B.** Encrypt scripts
- **C.** Trace executed commands for debugging
- **D.** Disable nounset

??? success "Reveal answer"
    **Correct answer: C**

    Essential for CI failures.

    **Related concepts**

    - debugging

### Question 40

"$@" expands to:

**Difficulty:** Beginner

**Options:**

- **A.** Only $1
- **B.** The script name only
- **C.** Joined IFS string like unquoted $*
- **D.** All positional parameters safely separated

??? success "Reveal answer"
    **Correct answer: D**

    Correct argv forwarding.

    **Related concepts**

    - "$@"

## Scoring

| Score | Result |
|------:|--------|
| 36–40 | Excellent — ready for production script review |
| 28–35 | Pass — revisit weak sections |
| <28 | Re-work Modules 1–4 labs before Capstone |

## Recommended Study Areas

- [Variables, Quoting, and Expansions](../shell/variables-quoting-and-arithmetic.md)
- [Exit Status, Strict Mode, and Debugging](../shell/error-handling-logging-and-debugging.md)
- [Traps, Signals, Temp Files, and Locking](../shell/process-automation-signals-and-traps.md)
- [Secure Shell Scripting](../shell/production-shell-scripting.md)
- Lab: [Shell Ops Script Hardening](../labs/shell-ops-script-hardening.md)
