---
title: "Shell Scripting Interview Prep"
description: "25–30 interview questions for Bash scripting — fundamentals, automation, processes, text processing, debugging, and production scenarios."
difficulty: intermediate
estimated_time: "45–60 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: interview
tags:
  - interview
  - shell
  - bash
  - devops
comments: false
---

# Shell Scripting Interview Prep

Practice answers for Linux admin, DevOps, SRE, and platform engineering interviews. Prefer concrete examples from the [Shell Scripting track](../shell/index.md).

## Overview

| Item | Detail |
|------|--------|
| Who | Engineers who automate Linux with Bash |
| Level | Junior → mid DevOps / platform |
| Companies | Product startups, SaaS, consultancies, cloud-native teams |

## Skills being evaluated

- Quoting, expansions, and Bash vs POSIX sh
- Exit codes, strict mode, and defensive scripting
- Process control, signals, and traps
- Text pipelines, jq/yq for config/API data
- Cron/systemd environment differences
- Security habits (secrets, `rm`, SSH BatchMode)
- Clear communication under troubleshooting pressure

## Bash fundamentals (Q1–Q5)

### Q1 — Why do teams still write Bash?

**Expected answer:** Ubiquitous on Linux servers and CI images; excellent for glue, packaging CLI calls, and cron. Poor fit for large applications, complex data models, or rich HTTP clients.

**Common mistake:** Claiming Bash replaces Python/Go for services.

**Follow-up:** When would you rewrite a Bash tool in Python?

### Q2 — Bash vs `sh`?

**Expected answer:** Bash is a shell with extensions; `/bin/sh` is often dash (POSIX) on Debian/Ubuntu. Bashisms (`[[ ]]`, arrays, `source` nuances) fail under dash.

**Follow-up:** How do you detect the executing shell in a script?

### Q3 — What does `set -euo pipefail` do?

**Expected answer:**

- `-e` — exit on command failure
- `-u` — treat unset variables as errors
- `-o pipefail` — pipeline fails if any stage fails

**Common mistake:** Forgetting `pipefail` so `grep | wc` hides grep failures.

### Q4 — Why quote `"$var"` and `"$@"`?

**Expected answer:** Prevent word-splitting and globbing. `"$@"` preserves argument boundaries; `"$*"` joins into one word.

### Q5 — `[[ ]]` vs `[ ]`?

**Expected answer:** `[[ ]]` is Bash (safer parsing, `=~`, no word-split surprises with vars inside). `[` is POSIX `test`. Prefer `[[` in Bash scripts.

## Shell scripting (Q6–Q10)

### Q6 — How do you structure a maintainable script?

**Expected answer:** Shebang, strict mode, `usage`, functions with `local`, clear exit taxonomy, logging to stderr, optional `lib/common.sh`.

### Q7 — How do functions return data vs status?

**Expected answer:** Status via `return`/`exit`; data via stdout (captured with `$( )`). Avoid globals when `local` suffices.

### Q8 — Indexed vs associative arrays?

**Expected answer:** Indexed for lists; associative (`declare -A`) for maps. Associative arrays need Bash 4+ (macOS system Bash may be 3.2).

### Q9 — Safe line reading pattern?

**Expected answer:** `while IFS= read -r line; do ...; done <file` or `read -r -d ''` for NUL-delimited input with `find -print0`.

### Q10 — How do you parse CLI args?

**Expected answer:** `getopts` for short options; `case` for subcommands; document `--help` exiting `2`.

## Linux automation (Q11–Q15)

### Q11 — Idempotent package install?

**Expected answer:** Detect package manager; skip if already installed (`dpkg -s` / `rpm -q`); support dry-run; log actions.

### Q12 — User management automation risks?

**Expected answer:** Validate usernames; refuse destructive ops without flags; never log passwords; prefer dry-run; audit log every change.

### Q13 — Backup script essentials?

**Expected answer:** Staging + `trap` cleanup, retention, `flock`, checksums/size checks, restore test drill, path prefix validation.

### Q14 — Service health checks?

**Expected answer:** Combine `systemctl is-active` with HTTP probes (`curl` timeouts). Aggregate worst exit code; keep checks read-only.

### Q15 — Scheduling: cron vs systemd timers?

**Expected answer:** Cron is ubiquitous and simple; systemd timers integrate with journald, calendars, and unit dependencies. Both need absolute paths and explicit environments.

## Process management (Q16–Q18)

### Q16 — What is `trap` for?

**Expected answer:** Run cleanup on `EXIT`/`INT`/`TERM` — remove temp dirs, release locks, restore state.

### Q17 — How do you prevent overlapping cron jobs?

**Expected answer:** `flock` on a lock file (or systemd `Conflict=` / `flock` in `ExecStart`). Decide whether contention is exit `0` or an error.

### Q18 — `kill` vs `pkill` / signals?

**Expected answer:** Prefer signalling a known PID from a pidfile you own. Understand `TERM` then `KILL`. Avoid broad `pkill` patterns in production without safeguards.

## Text processing (Q19–Q21)

### Q19 — When `grep`/`awk` vs `jq`?

**Expected answer:** Line-oriented logs → grep/awk/sed. Structured JSON → jq. Mixing both is fine; do not regex-parse JSON if jq is available.

### Q20 — Useful jq patterns in interviews?

**Expected answer:** `select()`, `@tsv`, `-r`, handling missing keys, exiting non-zero on failed assertions (`jq -e`).

### Q21 — YAML in shell?

**Expected answer:** Use yq (confirm mikefarah vs Python wrapper). Validate required keys before deploy. Prefer YAML for config, JSON for APIs.

## Debugging (Q22–Q24)

### Q22 — Script works interactively but fails in cron?

**Expected answer:** Minimal `PATH`, no aliases, different cwd, missing env vars/secrets. Fingerprint env; set `PATH`; use absolute paths.

### Q23 — How do you debug a failing pipeline?

**Expected answer:** `bash -x`, `pipefail`, split stages, log intermediate files, ShellCheck, `bash -n`.

### Q24 — Common expansion bugs?

**Expected answer:** Unquoted globs, unintended empty arrays with `set -u`, assuming Linux `date` flags on macOS, Windows CRLF shebang issues.

## Production scenarios (Q25–Q28)

### Q25 — Unsafe `rm -rf $TARGET` in a shared script — what do you do?

**Expected answer:** Stop the job; rewrite with quotes; require absolute path under an allowed prefix (`realpath` check); add dry-run; add tests; review blast radius in logs.

### Q26 — Deploy script failed mid-way — design expectations?

**Expected answer:** Stages + symlink flip, health check, automatic rollback, flock, clear exit codes, artefacts retained for forensics.

### Q27 — Certificate expired overnight — prevention?

**Expected answer:** Scheduled openssl expiry checks with warn window; alert routing; inventory of SANs; prefer automated renewal (ACME) where possible.

### Q28 — CI job leaked a token in logs — response?

**Expected answer:** Rotate credentials immediately; scrub CI logs; never `echo` secrets; use masked variables; fail closed; add ShellCheck/review rules.

## Rapid fire (optional)

| Prompt | One-line answer |
|--------|-----------------|
| Shebang recommendation? | `#!/usr/bin/env bash` |
| Exit code for usage errors? | Often `2` |
| Where should logs go? | stderr |
| Disable password SSH prompts in scripts? | `BatchMode=yes` |
| Static analysis tool? | ShellCheck |

## Interview tips

- Narrate failure modes, not only happy paths
- Mention quoting and exit codes early — interviewers listen for them
- Prefer small, testable scripts over clever one-liners
- Be honest about Bash limits (JSON/APIs → Python)

## Evaluation rubric (1–5)

| Category | Look for |
|----------|----------|
| Technical accuracy | Correct Bash semantics |
| Defensive scripting | Quotes, `pipefail`, validation |
| Operations | Cron/env, locks, traps |
| Security | Secrets, path safety, SSH |
| Communication | Structured, concise answers |

## Related

- Track: [Shell Scripting](../shell/index.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Labs: [Ops Script Hardening](../labs/shell-ops-script-hardening.md), [Linux Operations Toolkit](../labs/shell-linux-operations-toolkit.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
