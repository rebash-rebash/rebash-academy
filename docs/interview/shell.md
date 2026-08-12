---
title: "Shell Interview Preparation"
description: "20 curated Shell interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: shell
tags:
  - interview
  - shell
comments: false
---

{% raw %}
# Shell Interview Preparation

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

**1. What is the purpose of `#!/bin/bash` (the shebang)?**

??? success "Reveal answer"
    **In short:** The shebang selects the interpreter used when you execute a script directly.
    
    **Key points**
    
    - `#!/bin/bash` pins an absolute Bash path.
    - `#!/usr/bin/env bash` is more portable across hosts.
    - The script still needs execute permission.
    
    **Try this**
    
    - `head -1 script.sh`
    - `chmod +x script.sh`
    
    **Trap**
    
    - Writing a Bash shebang then running `sh script.sh` — different interpreter.

**2. What is the difference between `&` and `&&` in shell scripting?**

??? success "Reveal answer"
    **In short:** `&` backgrounds a command; `&&` runs the next command only on success.
    
    **Key points**
    
    - `long_job &` returns immediately.
    - `make build && make test` stops if build fails.
    - `||` runs on failure instead.
    
    **Try this**
    
    - `make build && make test`
    - `sleep 30 &`
    
    **Trap**
    
    - Backgrounding without redirecting output and wondering why the session looks hung.

**3. How do you assign and print a variable in Bash?**

??? success "Reveal answer"
    **In short:** Assign with `name=value` (no spaces) and print with `echo "${name}"`.
    
    **Key points**
    
    - Quote expansions unless you want word-splitting.
    - `export` when child processes need the value.
    - Fail fast: `: "${REGION:?REGION is required}"`.
    
    **Try this**
    
    - `name=rebash; echo "${name}"`
    - `: "${REGION:?REGION is required}"`
    
    **Trap**
    
    - `name = value` with spaces — Bash treats `name` as a command.

**4. What does `$?` mean, and why do exit codes matter?**

??? success "Reveal answer"
    **In short:** `$?` is the last foreground exit code: `0` success, non-zero failure.
    
    **Key points**
    
    - CI and scripts branch on it.
    - Save it immediately: `rc=$?`.
    - `set -e` aborts early on failures.
    
    **Try this**
    
    - `false; echo $?`
    - `true; echo $?`
    
    **Trap**
    
    - Checking `$?` after a debug `echo` and trusting the wrong status.

**5. What is `set -euo pipefail` and why do interviewers expect it?**

??? success "Reveal answer"
    **In short:** `set -euo pipefail` hardens Bash automation: exit on errors, unset vars, and pipeline failures.
    
    **Key points**
    
    - `-e` stop on failure; `-u` catch unset variables.
    - `pipefail` fails if any pipeline stage fails.
    - Default it in deploy/backup scripts.
    
    **Try this**
    
    - `set -euo pipefail`
    - `false | true; echo $?`
    
    **Trap**
    
    - Without `pipefail`, a failing `grep` in the middle can still look green.

**6. Explain the purpose of `grep`. What does `grep -r "error" /var/log` do?**

??? success "Reveal answer"
    **In short:** `grep` finds matching lines; `grep -r "error" /var/log` searches that tree recursively.
    
    **Key points**
    
    - Handy flags: `-i`, `-n`, `-E`.
    - Use `rg` when installed; keep `grep` for minimal hosts.
    - Pair with `journalctl` for systemd services.
    
    **Try this**
    
    - `grep -RIn "error" /var/log/nginx`
    
    **Trap**
    
    - Recursing into huge binary trees without filtering — slow and noisy.

**7. What is the difference between `find` and `sed`?**

??? success "Reveal answer"
    **In short:** `find` selects files by metadata; `sed` transforms text streams.
    
    **Key points**
    
    - `find` answers “which files?”; `sed` answers “change this text”.
    - They compose via `-print0` and `xargs -0`.
    - Content search is `grep`/`rg`, not `find`.
    
    **Try this**
    
    - `find . -type f -name '*.conf'`
    - sed -n '1,5p' file
    
    **Trap**
    
    - Using `find` when you meant a content search.

**8. How do you get the total number of lines in a file from the shell?**

??? success "Reveal answer"
    **In short:** Count lines with `wc -l file`.
    
    **Key points**
    
    - `wc -l < file` omits the filename in output.
    - `awk 'END{print NR}'` is an alternative.
    - `grep -c` counts matches, not total lines.
    
    **Try this**
    
    - `wc -l /var/log/syslog`
    
    **Trap**
    
    - `cat file | wc -l` — unnecessary pipeline.

## Scenarios and troubleshooting

**9. Write a shell approach to delete log files older than 30 days.**

??? success "Reveal answer"
    **In short:** Delete logs older than 30 days with `find -mtime +30` after a dry-run print.
    
    **Key points**
    
    - Preview with `-print` before `-delete`.
    - Prefer null-delimited delete for odd names.
    - logrotate is better for ongoing retention.
    
    **Try this**
    
    - `find /var/log/myapp -type f -name '*.log' -mtime +30 -print`
    
    **Trap**
    
    - Destructive `rm -rf` without a preview on production.

**10. Write a shell script outline to back up logs from the last 7 days and remove older ones.**

??? success "Reveal answer"
    **In short:** Archive the last 7 days first, verify the tarball, then delete older files.
    
    **Key points**
    
    - Use `find -mtime -7` + `tar`, with `set -euo pipefail`.
    - Only delete after the archive succeeds.
    - Log start/end for auditability.
    
    **Try this**
    
    - `find /var/log/myapp -mtime -7 -type f -print0 | tar -czf /backup/logs-$(date +%F).tgz --null -T -`
    
    **Trap**
    
    - Deleting before the archive finishes successfully.

**11. Write a script pattern that checks if a service is running, restarts it if not, and logs the event.**

??? success "Reveal answer"
    **In short:** If `systemctl is-active` fails, restart the unit and append a timestamped log line.
    
    **Key points**
    
    - systemd should be the primary supervisor; a watchdog is backup.
    - Avoid restart storms — alert on repeated flips.
    - Capture status output for handoff.
    
    **Try this**
    
    - `if ! systemctl is-active --quiet myapp; then systemctl restart myapp; echo "$(date -Is) restarted" >>/var/log/myapp-watchdog.log; fi`
    
    **Trap**
    
    - Silent restarts forever with no page — the outage becomes invisible.

**12. How would you debug a Bash script that works interactively but fails in cron?**

??? success "Reveal answer"
    **In short:** Interactive-vs-cron failures are almost always environment: `PATH`, cwd, or missing variables.
    
    **Key points**
    
    - Redirect cron stdout/stderr to a log file.
    - Use absolute paths everywhere.
    - Reproduce as the cron user with a clean env.
    
    **Try this**
    
    - `*/5 * * * * /usr/local/bin/job.sh >>/var/log/job.log 2>&1`
    
    **Trap**
    
    - Assuming `~/.bashrc` aliases exist under cron.

**13. What is the difference between `$*`, `$@`, and `"$@"` when passing arguments?**

??? success "Reveal answer"
    **In short:** `"$@"` keeps argument boundaries; unquoted `$*`/`$@` break on spaces.
    
    **Key points**
    
    - Wrappers should always forward `"$@"`.
    - `"$*"` joins into one string — rarely desired for exec.
    - Test with arguments that contain spaces.
    
    **Try this**
    
    - `set -- "a b" c; printf "<%s>\n" "$@"`
    
    **Trap**
    
    - Unquoted `$@` when handling filenames.

**14. How do you safely read lines from a file in Bash without word-splitting issues?**

??? success "Reveal answer"
    **In short:** Read lines safely with `while IFS= read -r line`.
    
    **Key points**
    
    - `-r` preserves backslashes.
    - Use null-delimited reads with `find -print0`.
    - Avoid `for line in $(cat file)`.
    
    **Try this**
    
    - `while IFS= read -r line; do printf '%s\n' "$line"; done < file`
    
    **Trap**
    
    - Word-splitting filenames that contain spaces.

## Practice questions

**15. What does `chmod 755` do?**

??? success "Reveal answer"
    **In short:** `chmod 755` means owner rwx; group and others r-x.
    
    **Key points**
    
    - Fine for shared scripts/directories.
    - Wrong for secrets — prefer `600`/`640`.
    - Symbolic equivalent: `u=rwx,go=rx`.
    
    **Try this**
    
    - `chmod 755 script.sh`
    
    **Trap**
    
    - Recursive `755` across a tree with private config.

**16. How do you sum integers from 1 to 100 in Bash?**

??? success "Reveal answer"
    **In short:** Sum 1..100 with a loop or `seq | awk`; the answer is `5050`.
    
    **Key points**
    
    - `seq 1 100 | awk '{s+=$1} END{print s}'`.
    - Or a Bash arithmetic loop.
    - Sanity-check with `n(n+1)/2`.
    
    **Try this**
    
    - `seq 1 100 | awk '{s+=$1} END{print s}'`
    
    **Trap**
    
    - Off-by-one errors in C-style `for` loops.

**17. How do pipes work, and what does `pipefail` change?**

??? success "Reveal answer"
    **In short:** Pipes connect stdout→stdin; `pipefail` makes any stage failure fail the pipeline.
    
    **Key points**
    
    - Default status comes from the last command only.
    - `set -o pipefail` catches middle-stage failures.
    - `tee` observes a stream without breaking the pipe.
    
    **Try this**
    
    - `set -o pipefail`
    - `false | true; echo $?`
    
    **Trap**
    
    - Ignoring `grep`’s exit code 1 for “no match” in strict scripts.

**18. How do you use `xargs`, and when is `-print0` important?**

??? success "Reveal answer"
    **In short:** `xargs` builds commands from stdin; pair with `-print0`/`-0` for safe path handling.
    
    **Key points**
    
    - `find … -print0 | xargs -0 …` survives spaces.
    - `-n` and `-P` control batches and parallelism.
    - Default splitting is unsafe for arbitrary filenames.
    
    **Try this**
    
    - `find . -name '*.tmp' -print0 | xargs -0 rm -f`
    
    **Trap**
    
    - Deleting paths split on spaces — silent data loss.

**19. What is command substitution, and what is the difference between `` `cmd` `` and `$(cmd)`?**

??? success "Reveal answer"
    **In short:** Command substitution captures output; prefer `$(cmd)` over backticks.
    
    **Key points**
    
    - `$(…)` nests cleanly and reads better.
    - Quote carefully; prefer arrays/`mapfile` for lists.
    - Trailing newlines are stripped — know the edge case.
    
    **Try this**
    
    - `today="$(date +%F)"; echo "$today"`
    
    **Trap**
    
    - Unquoted `$(ls)` on filenames with spaces.

**20. How would you write a small Bash CLI that requires an environment name and fails clearly if it is missing?**

??? success "Reveal answer"
    **In short:** Require the environment name up front and exit with a clear usage error if missing.
    
    **Key points**
    
    - Use `: "${ENV:?ENV is required (dev|staging|prod)}"`.
    - Validate allowed values with `case`.
    - Start with `set -euo pipefail`.
    
    **Try this**
    
    - `: "${ENV:?ENV is required (dev|staging|prod)}"`
    - `set -euo pipefail`
    
    **Trap**
    
    - Defaulting missing `ENV` to `prod`.

## Related
- Course: [Shell](../shell/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
