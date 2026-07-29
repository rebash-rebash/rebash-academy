---
title: "Quiz — Shell Scripting for DevOps Fundamentals"
description: "40-question quiz for Shell Scripting for DevOps Engineers — Bash fundamentals through production troubleshooting across all 18 modules."
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

# Quiz — Shell Scripting for DevOps Fundamentals

## Quiz Overview

Assess Bash automation skills for Linux admins, DevOps engineers, and platform engineers following the rewritten Shell Scripting for DevOps Engineers course.

| Attribute | Value |
|-----------|--------|
| Topic | Shell Scripting for DevOps Engineers |
| Questions | 40 |
| Passing score | 70% (28 correct) |
| Estimated time | 45–60 minutes |
| Format | Multiple choice (single answer) |
| Answer balance | 10 × A, 10 × B, 10 × C, 10 × D |

!!! tip "How to use this quiz"
    Attempt each section without peeking. Use **Reveal answer** only after you commit to a choice.

## Learning Objectives

This quiz assesses whether you can:

- [ ] Explain Bash vs sh and script execution
- [ ] Apply quoting, variables, I/O, and control flow safely
- [ ] Use loops, functions, arrays, and file/text tools
- [ ] Automate Linux admin, networking, jq/yq, and scheduling tasks
- [ ] Debug, harden, and operate production shell scripts


## Section 1 — Fundamentals

### Question 1

What is a shell primarily responsible for on a Linux system?

**Difficulty:** Beginner

**Options:**

- **A.** Interpreting commands and launching processes
- **B.** Replacing the kernel scheduler
- **C.** Storing relational data
- **D.** Rendering GUIs only

??? success "Reveal answer"
    **Correct answer: A**

    The shell is a command interpreter that starts processes and connects pipelines.

    **Why other options are incorrect**

    - **B.** Scheduling is a kernel job.
    - **C.** Databases store relational data.
    - **D.** GUIs are separate; shells often run headless.

    **Related concepts**

    - shell basics

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

    `env` resolves `bash` from PATH across installations.

    **Why other options are incorrect**

    - **A.** Forces zsh.
    - **C.** Python shebang.
    - **D.** Invalid shebang form.

    **Related concepts**

    - shebang

### Question 3

On many Debian/Ubuntu systems, what is /bin/sh often linked to?

**Difficulty:** Beginner

**Options:**

- **A.** Always Bash
- **B.** Always zsh
- **C.** dash (POSIX sh)
- **D.** fish

??? success "Reveal answer"
    **Correct answer: C**

    dash is common; Bashisms fail under it.

    **Why other options are incorrect**

    - **A.** Not guaranteed.
    - **B.** zsh is uncommon as sh.
    - **D.** fish is not POSIX sh.

    **Related concepts**

    - POSIX
    - dash

### Question 4

Which expansion is usually safest for a path that may contain spaces?

**Difficulty:** Beginner

**Options:**

- **A.** $path
- **B.** `$path`
- **C.** Unquoted $path with IFS cleared only
- **D.** "$path"

??? success "Reveal answer"
    **Correct answer: D**

    Double quotes prevent word-splitting and globbing.

    **Why other options are incorrect**

    - **A.** Unquoted splits on spaces.
    - **B.** Backticks still split when used unquoted.
    - **C.** IFS tricks are fragile.

    **Related concepts**

    - quoting

### Question 5

What does set -u do?

**Difficulty:** Beginner

**Options:**

- **A.** Treats unset variable expansions as errors
- **B.** Ignores unset variables
- **C.** Enables Unicode locales only
- **D.** Disables nounset

??? success "Reveal answer"
    **Correct answer: A**

    nounset (`-u`) errors on unset expansions.

    **Why other options are incorrect**

    - **B.** Opposite.
    - **C.** Unrelated.
    - **D.** Opposite wording.

    **Related concepts**

    - strict mode

### Question 6

Which construct is preferred for conditionals in Bash scripts?

**Difficulty:** Beginner

**Options:**

- **A.** goto
- **B.** [[ ... ]]
- **C.** Always eval
- **D.** regex alone without tests

??? success "Reveal answer"
    **Correct answer: B**

    `[[ ]]` is the Bash conditional command.

    **Why other options are incorrect**

    - **A.** Not used in Bash.
    - **C.** eval is dangerous.
    - **D.** Incomplete.

    **Related concepts**

    - conditionals

### Question 7

What is the conventional meaning of exit code 0?

**Difficulty:** Beginner

**Options:**

- **A.** Usage error
- **B.** Permission denied always
- **C.** Success
- **D.** Fatal signal

??? success "Reveal answer"
    **Correct answer: C**

    0 means success by convention.

    **Why other options are incorrect**

    - **A.** Often 2 for usage.
    - **B.** Permission is typically non-zero.
    - **D.** Signals map to 128+n.

    **Related concepts**

    - exit codes

### Question 8

Which statement about interactive vs non-interactive shells is true?

**Difficulty:** Beginner

**Options:**

- **A.** Cron jobs always load your full interactive aliases
- **B.** Non-interactive shells cannot run scripts
- **C.** Login shells never set PATH
- **D.** Non-interactive shells often skip interactive startup customisations

??? success "Reveal answer"
    **Correct answer: D**

    Scripts/cron typically get a leaner environment without interactive aliases.

    **Why other options are incorrect**

    - **A.** Aliases usually absent.
    - **B.** Scripts run non-interactively.
    - **C.** Login shells often set PATH via profiles.

    **Related concepts**

    - execution environment

### Question 9

What does command substitution $(cmd) do?

**Difficulty:** Beginner

**Options:**

- **A.** Runs cmd and substitutes its stdout
- **B.** Deletes cmd from disk
- **C.** Starts a GUI for cmd
- **D.** Disables errexit

??? success "Reveal answer"
    **Correct answer: A**

    It captures stdout of cmd into the command line.

    **Why other options are incorrect**

    - **B.** No.
    - **C.** No.
    - **D.** No.

    **Related concepts**

    - command substitution

### Question 10

Which redirection appends both stdout and stderr to a log file in Bash?

**Difficulty:** Beginner

**Options:**

- **A.** cmd >log
- **B.** cmd >>log 2>&1
- **C.** cmd 2>log
- **D.** cmd <log

??? success "Reveal answer"
    **Correct answer: B**

    Append stdout, then point stderr to the same destination.

    **Why other options are incorrect**

    - **A.** Overwrites stdout only.
    - **C.** stderr only.
    - **D.** stdin from file.

    **Related concepts**

    - redirection

## Section 2 — Practical Knowledge

### Question 11

Which loop reads a file line-by-line safely?

**Difficulty:** Intermediate

**Options:**

- **A.** for line in $(cat file); do
- **B.** while read line; do without -r always
- **C.** while IFS= read -r line; do ...; done <file
- **D.** until cat file

??? success "Reveal answer"
    **Correct answer: C**

    `read -r` with IFS= avoids backslash mangling and preserves control over whitespace.

    **Why other options are incorrect**

    - **A.** Word-splits and globbing.
    - **B.** Missing -r is weaker.
    - **D.** Not a read loop.

    **Related concepts**

    - loops
    - read

### Question 12

How should a Bash function keep a temporary variable from leaking?

**Difficulty:** Intermediate

**Options:**

- **A.** Use global only
- **B.** Export it always
- **C.** Name it RANDOM
- **D.** Declare it with local

??? success "Reveal answer"
    **Correct answer: D**

    `local` scopes the variable to the function.

    **Why other options are incorrect**

    - **A.** Pollutes globals.
    - **B.** Worse.
    - **C.** RANDOM is special.

    **Related concepts**

    - functions
    - local

### Question 13

Which creates an indexed array in Bash?

**Difficulty:** Intermediate

**Options:**

- **A.** a=(x y)
- **B.** declare -A a=(x y)
- **C.** a={{x,y}}
- **D.** set array x y

??? success "Reveal answer"
    **Correct answer: A**

    Parentheses create an indexed array.

    **Why other options are incorrect**

    - **B.** -A is associative and needs keying.
    - **C.** Invalid.
    - **D.** Not Bash array syntax.

    **Related concepts**

    - arrays

### Question 14

Which test checks that a path is a regular file?

**Difficulty:** Intermediate

**Options:**

- **A.** [[ -d $p ]]
- **B.** [[ -f $p ]]
- **C.** [[ -L $p ]]
- **D.** [[ -z $p ]]

??? success "Reveal answer"
    **Correct answer: B**

    `-f` is regular file.

    **Why other options are incorrect**

    - **A.** Directory.
    - **C.** Symlink.
    - **D.** Empty string.

    **Related concepts**

    - file tests

### Question 15

Why enable set -o pipefail in automation?

**Difficulty:** Intermediate

**Options:**

- **A.** It speeds up pipes
- **B.** It disables pipes
- **C.** It makes pipelines fail if any stage fails
- **D.** It only affects stderr

??? success "Reveal answer"
    **Correct answer: C**

    Without it, the last command's status can hide earlier failures.

    **Why other options are incorrect**

    - **A.** Not about speed.
    - **B.** Opposite.
    - **D.** Affects status of pipeline.

    **Related concepts**

    - pipefail

### Question 16

Which openssl-based check helps monitor TLS certificate expiry?

**Difficulty:** Intermediate

**Options:**

- **A.** iptables -L
- **B.** systemctl reboot
- **C.** chmod 777
- **D.** openssl s_client + x509 -enddate

??? success "Reveal answer"
    **Correct answer: D**

    Fetch the cert and parse notAfter / enddate.

    **Why other options are incorrect**

    - **A.** Firewall.
    - **B.** Unrelated.
    - **C.** Permissions anti-pattern.

    **Related concepts**

    - TLS
    - openssl

### Question 17

Which jq filter emits raw strings without JSON quotes?

**Difficulty:** Intermediate

**Options:**

- **A.** jq -r .key
- **B.** jq .key
- **C.** jq -c .key
- **D.** jq --slurp .key

??? success "Reveal answer"
    **Correct answer: A**

    `-r` is raw output.

    **Why other options are incorrect**

    - **B.** Quotes strings.
    - **C.** Compact JSON.
    - **D.** Slurp arrays.

    **Related concepts**

    - jq

### Question 18

What is a key risk of using the wrong yq implementation?

**Difficulty:** Intermediate

**Options:**

- **A.** YAML is illegal on Linux
- **B.** CLI syntax differs between mikefarah/yq and Python wrappers
- **C.** yq cannot read files
- **D.** Bash forbids YAML

??? success "Reveal answer"
    **Correct answer: B**

    Confirm version/flavour; filters differ.

    **Why other options are incorrect**

    - **A.** False.
    - **C.** False.
    - **D.** False.

    **Related concepts**

    - yq

### Question 19

Which cron practice prevents 'works on my machine' failures?

**Difficulty:** Intermediate

**Options:**

- **A.** Rely on interactive aliases
- **B.** Omit redirection so cron emails nothing useful always
- **C.** Set PATH and use absolute script paths
- **D.** Run GUI tools without DISPLAY hacks undocumented

??? success "Reveal answer"
    **Correct answer: C**

    Cron environments are minimal — be explicit.

    **Why other options are incorrect**

    - **A.** Aliases absent.
    - **B.** You want logs.
    - **D.** Avoid GUIs in cron.

    **Related concepts**

    - cron

### Question 20

Which pipeline is a typical shell text-processing approach for counting unique error codes in a log column?

**Difficulty:** Intermediate

**Options:**

- **A.** Only `chmod` on the log file
- **B.** Only `systemctl daemon-reexec`
- **C.** Only `useradd` parsing
- **D.** `awk '{print $NF}' | sort | uniq -c`

??? success "Reveal answer"
    **Correct answer: D**

    `awk`, `sort`, and `uniq` are classic text-processing tools inside shell automation.

    **Why other options are incorrect**

    - **A.** Permissions are unrelated to counting fields.
    - **B.** systemd reload is unrelated to log field frequency.
    - **C.** User creation is unrelated.

    **Related concepts**

    - awk
    - sort
    - uniq
    - text processing

## Section 3 — Scenario-Based Questions

### Question 21

A nightly job deletes paths with spaces incorrectly. First fix?

**Difficulty:** Intermediate

**Options:**

- **A.** Quote expansions and validate path prefixes
- **B.** Disable SELinux permanently
- **C.** chmod 777 the tree
- **D.** Run as root always

??? success "Reveal answer"
    **Correct answer: A**

    Quoting and allowlisting paths prevent blast radius.

    **Why other options are incorrect**

    - **B.** Unrelated/nuclear.
    - **C.** Worsens security.
    - **D.** Increases risk.

    **Related concepts**

    - quoting
    - safety

### Question 22

grep pattern file | wc -l returns 0 lines but the script continues as success without pipefail when pattern missing. Why?

**Difficulty:** Intermediate

**Options:**

- **A.** grep cannot fail
- **B.** wc succeeds even if grep exits non-zero without pipefail
- **C.** wc ignores stdin
- **D.** Kernels ignore exit codes

??? success "Reveal answer"
    **Correct answer: B**

    Pipeline status is normally the last command unless pipefail is set.

    **Why other options are incorrect**

    - **A.** grep can exit 1.
    - **C.** wc reads stdin.
    - **D.** False.

    **Related concepts**

    - pipefail
    - pipelines

### Question 23

You need to fan-out uptime across hosts without password prompts hanging CI. Best SSH options?

**Difficulty:** Intermediate

**Options:**

- **A.** Omit BatchMode so passwords can be typed
- **B.** Disable keys and use telnet
- **C.** BatchMode=yes with ConnectTimeout
- **D.** Enable X11 forwarding

??? success "Reveal answer"
    **Correct answer: C**

    BatchMode fails fast without TTY passwords; timeouts bound hangs.

    **Why other options are incorrect**

    - **A.** Hangs automation.
    - **B.** Insecure/obsolete.
    - **D.** Unrelated.

    **Related concepts**

    - SSH

### Question 24

A deploy should move traffic only after health checks. Which pattern fits?

**Difficulty:** Advanced

**Options:**

- **A.** Overwrite live files in place with no symlink
- **B.** Kill -9 first always
- **C.** scp directly to / without staging
- **D.** Stage release, flip symlink, health-check, rollback on failure

??? success "Reveal answer"
    **Correct answer: D**

    Staged releases with symlink activation and rollback are standard.

    **Why other options are incorrect**

    - **A.** Hard to roll back.
    - **B.** Dangerous.
    - **C.** Risky.

    **Related concepts**

    - deploy

### Question 25

systemd timer vs cron for a hardened host — a fair statement?

**Difficulty:** Intermediate

**Options:**

- **A.** Timers integrate with unit deps and the journal; cron remains simple and ubiquitous
- **B.** Timers cannot replace any cron use cases ever
- **C.** cron cannot run as a user
- **D.** Timers require Kubernetes

??? success "Reveal answer"
    **Correct answer: A**

    Both are valid; timers offer tighter systemd integration.

    **Why other options are incorrect**

    - **B.** Too absolute.
    - **C.** User crontabs exist.
    - **D.** False.

    **Related concepts**

    - systemd timers
    - cron

### Question 26

Parsing API JSON in Bash for a status summary — best approach?

**Difficulty:** Intermediate

**Options:**

- **A.** Regex the whole blob with grep only
- **B.** Use jq filters and exit non-zero on degraded services
- **C.** Convert JSON to XML first mandatorily
- **D.** Ignore structure and count bytes

??? success "Reveal answer"
    **Correct answer: B**

    jq understands structure; couple with exit codes for automation.

    **Why other options are incorrect**

    - **A.** Fragile.
    - **C.** Unnecessary.
    - **D.** Useless.

    **Related concepts**

    - jq

### Question 27

Log rotation script must not remove the active file descriptor blindly on a busy writer. What should you document?

**Difficulty:** Advanced

**Options:**

- **A.** That chmod 777 fixes rotation
- **B.** That killing -9 the app is required nightly
- **C.** That rename vs copytruncate trade-offs matter; prefer proper logrotate in production
- **D.** That rotation never races

??? success "Reveal answer"
    **Correct answer: C**

    Writers with open FDs need an agreed strategy; production often uses logrotate.

    **Why other options are incorrect**

    - **A.** Insecure.
    - **B.** Unacceptable.
    - **D.** False.

    **Related concepts**

    - log rotation

### Question 28

Disk monitor must ignore tmpfs noise. What helps?

**Difficulty:** Beginner

**Options:**

- **A.** df without flags only
- **B.** Always alert on 0%
- **C.** Parse /etc/passwd
- **D.** df -P -x tmpfs -x devtmpfs

??? success "Reveal answer"
    **Correct answer: D**

    Exclude pseudo filesystems explicitly.

    **Why other options are incorrect**

    - **A.** Includes noise.
    - **B.** Nonsense.
    - **C.** Unrelated.

    **Related concepts**

    - df
    - monitoring

### Question 29

Configuration for replicas lives in YAML. Before deploy you should:

**Difficulty:** Intermediate

**Options:**

- **A.** Validate required keys with yq and fail closed
- **B.** Assume keys exist
- **C.** Edit YAML by sed without checks in prod as policy
- **D.** Store secrets in the same committed YAML unencrypted

??? success "Reveal answer"
    **Correct answer: A**

    Fail if required config is missing.

    **Why other options are incorrect**

    - **B.** Fragile.
    - **C.** Risky.
    - **D.** Secret leak.

    **Related concepts**

    - yq
    - config

### Question 30

Overlapping backup cron runs corrupt archives. Fix?

**Difficulty:** Intermediate

**Options:**

- **A.** Remove all backups
- **B.** Serialise with flock (or equivalent)
- **C.** Nice the process to 19 only
- **D.** Disable clocks

??? success "Reveal answer"
    **Correct answer: B**

    Mutual exclusion prevents overlap.

    **Why other options are incorrect**

    - **A.** Destructive.
    - **C.** Insufficient.
    - **D.** Nonsense.

    **Related concepts**

    - flock
    - backup

## Section 4 — Troubleshooting

### Question 31

Symptom: bash -u script fails on empty optional array iteration. Likely cause?

**Difficulty:** Advanced

**Options:**

- **A.** DNS failure
- **B.** SELinux always
- **C.** nounset interacting with empty array expansion patterns
- **D.** jq missing only

??? success "Reveal answer"
    **Correct answer: C**

    Empty array expansions can trip `set -u` depending on pattern; handle carefully.

    **Why other options are incorrect**

    - **A.** Unrelated.
    - **B.** Unrelated.
    - **D.** Might be separate issue.

    **Related concepts**

    - set -u
    - arrays

### Question 32

Symptom: script shebang points to bash but CI runs sh script.sh. What happens?

**Difficulty:** Intermediate

**Options:**

- **A.** Shebang is always honoured for sh script.sh
- **B.** Kernel upgrades automatically
- **C.** Network blocks scripts
- **D.** Bashisms may fail because sh invokes the POSIX shell

??? success "Reveal answer"
    **Correct answer: D**

    Explicit `sh` ignores shebang interpreter selection.

    **Why other options are incorrect**

    - **A.** False for this invocation.
    - **B.** False.
    - **C.** False.

    **Related concepts**

    - shebang
    - CI

### Question 33

Symptom: trap cleanup never runs on CTRL+C. Missing what?

**Difficulty:** Intermediate

**Options:**

- **A.** trap on INT/TERM/EXIT
- **B.** More echo statements
- **C.** Disabling signals permanently
- **D.** Using goto

??? success "Reveal answer"
    **Correct answer: A**

    Register traps for the signals you care about, including EXIT.

    **Why other options are incorrect**

    - **B.** No.
    - **C.** Dangerous.
    - **D.** Not Bash.

    **Related concepts**

    - trap

### Question 34

Symptom: permission denied when executing ./script.sh. First checks?

**Difficulty:** Beginner

**Options:**

- **A.** Reinstall the kernel
- **B.** chmod +x and confirm mount is not noexec
- **C.** Disable quoting
- **D.** Delete PATH

??? success "Reveal answer"
    **Correct answer: B**

    Execute bit and filesystem mount options are the usual causes.

    **Why other options are incorrect**

    - **A.** Excessive.
    - **C.** Unrelated.
    - **D.** Breaks more.

    **Related concepts**

    - permissions

### Question 35

Symptom: openssl check fails intermittently with handshake timeouts. Good mitigation?

**Difficulty:** Intermediate

**Options:**

- **A.** Remove timeouts so jobs hang forever
- **B.** Disable TLS verification globally in production without review
- **C.** Set connection timeouts and treat failures as exit 3 with retries/backoff
- **D.** Open all security groups to 0.0.0.0/0 permanently

??? success "Reveal answer"
    **Correct answer: C**

    Bound waits; classify failures; retry thoughtfully.

    **Why other options are incorrect**

    - **A.** Worse.
    - **B.** Insecure.
    - **D.** Insecure.

    **Related concepts**

    - timeouts
    - TLS

## Section 5 — Architecture

### Question 36

For a modular ops CLI, which layout is most maintainable?

**Difficulty:** Advanced

**Options:**

- **A.** One 5,000-line script with no functions
- **B.** Copy-paste each check with divergent logging
- **C.** Put secrets in the entrypoint
- **D.** bin/entrypoint + lib/common + cmd modules

??? success "Reveal answer"
    **Correct answer: D**

    Shared libraries and modules scale better.

    **Why other options are incorrect**

    - **A.** Hard to test.
    - **B.** Drift.
    - **C.** Insecure.

    **Related concepts**

    - architecture
    - modularity

### Question 37

Logging contract for automation in CI — best practice?

**Difficulty:** Intermediate

**Options:**

- **A.** Humans on stderr; machine RESULT lines on stdout
- **B.** Put secrets on stdout for convenience
- **C.** Disable all logs
- **D.** Log only to wall

??? success "Reveal answer"
    **Correct answer: A**

    Keeps pipelines composable and secrets off default captures when careful.

    **Why other options are incorrect**

    - **B.** Leak risk.
    - **C.** Unoperable.
    - **D.** Inappropriate.

    **Related concepts**

    - logging

### Question 38

When should you move from Bash to Python for automation?

**Difficulty:** Advanced

**Options:**

- **A.** Never
- **B.** Complex JSON/APIs, richer testing, packaged libraries, non-trivial state
- **C.** For a single echo
- **D.** When CPU is idle only

??? success "Reveal answer"
    **Correct answer: B**

    Bash excels at glue; Python fits complexity and maintainability beyond glue.

    **Why other options are incorrect**

    - **A.** Too absolute.
    - **C.** Unnecessary.
    - **D.** Nonsensical.

    **Related concepts**

    - tool choice

### Question 39

Security check modules in a shell framework should default to:

**Difficulty:** Advanced

**Options:**

- **A.** Mutate sshd_config automatically
- **B.** chmod 777 findings away
- **C.** Read-only audits unless --apply
- **D.** Disable auditing

??? success "Reveal answer"
    **Correct answer: C**

    Safe defaults; explicit apply for changes.

    **Why other options are incorrect**

    - **A.** Dangerous default.
    - **B.** Insecure.
    - **D.** Opposite of goal.

    **Related concepts**

    - security
    - dry-run

### Question 40

A production shell framework report module should primarily:

**Difficulty:** Intermediate

**Options:**

- **A.** Replace your metrics backend entirely without discussion
- **B.** Email passwords to the team
- **C.** Skip exit codes
- **D.** Aggregate check results into a dated artefact with clear exit status

??? success "Reveal answer"
    **Correct answer: D**

    Reports summarise evidence; exit status drives automation.

    **Why other options are incorrect**

    - **A.** Overclaim.
    - **B.** Insecure.
    - **C.** Breaks automation.

    **Related concepts**

    - reporting

## Score Summary

| Score | Band | Guidance |
|-------|------|----------|
| 36–40 | Excellent | Ready for advanced labs and the capstone project |
| 28–35 | Good (pass) | Revise weak modules, then retake |
| 20–27 | Needs improvement | Revisit tutorials + cheat sheet before labs |
| ≤19 | Restart foundations | Modules 1–7 first |

**Passing score:** 28/40 (70%).

## Recommended Study Areas

| If you missed… | Revise |
|----------------|--------|
| Q1–Q10 | [Shell Fundamentals](../shell/shell-fundamentals-bash-vs-sh-and-execution.md), [First Script](../shell/writing-your-first-script.md), [Variables](../shell/variables-quoting-and-arithmetic.md), [I/O](../shell/input-output-redirection-and-pipes.md), [Conditionals](../shell/control-flow-conditionals.md) |
| Q11–Q20 | [Loops](../shell/loops-for-while-until.md), [Functions](../shell/functions-parameters-and-locals.md), [Arrays](../shell/arrays-and-string-manipulation.md), [Files](../shell/file-operations-in-shell.md), [Text](../shell/text-processing-in-shell-scripts.md), [jq/yq](../shell/json-and-yaml-with-jq-yq.md), [Cron](../shell/scheduling-cron-at-and-timers.md) |
| Q21–Q30 | [Linux Admin Automation](../shell/linux-admin-automation.md), [Networking](../shell/networking-automation-with-shell.md), [Traps](../shell/process-automation-signals-and-traps.md), [Production Scripting](../shell/production-shell-scripting.md) |
| Q31–Q40 | [Error Handling](../shell/error-handling-logging-and-debugging.md), [Troubleshooting](../shell/troubleshooting-shell-scripts.md) |

Also use the [Shell cheat sheet](../cheatsheets/shell.md) and [Shell labs](../labs/index.md).

## Interview Connection

These items mirror common screening questions: quoting, `pipefail`, cron environments, SSH BatchMode, deploy rollback, and when to leave Bash. Practise aloud with the [Shell interview guide](../interview/shell.md).

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [ShellCheck](https://www.shellcheck.net/)
- [jq manual](https://jqlang.github.io/jq/manual/)
- [mikefarah/yq](https://mikefarah.gitbook.io/yq/)
