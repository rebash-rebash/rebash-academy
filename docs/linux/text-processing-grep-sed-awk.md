---
title: "Text Processing with grep, sed, and awk"
description: "Filter and transform logs and configs with grep, sed, awk, cut, paste, tr, sort, uniq, wc, and xargs — with a real incident-style pipeline lab."
difficulty: intermediate
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 5 · Text Processing"
tags:
  - linux
  - grep
  - sed
  - awk
  - pipelines
prerequisites:
  - linux/permissions-acls-and-special-bits
next:
  - linux/process-management
related:
  - linux/shell-scripting-fundamentals
interview: interview/linux
comments: false
---

# Text Processing with grep, sed, and awk

## Overview

In Cloud and DevOps work, most day-to-day evidence is **text**: application logs, Nginx or load-balancer access lines, Continuous Integration (CI) job output, Kubernetes events exported to a file, and configuration dumps. You rarely open a spreadsheet. You **search**, **edit**, and **summarise** streams of lines with classic Unix tools.

**grep** finds (or excludes) lines that match a pattern. **sed** edits a stream — substitute text, delete lines, print ranges. **awk** splits each line into fields and builds small reports (counts, totals, column extracts). Helpers such as `cut`, `tr`, `sort`, `uniq`, `wc`, and `xargs` complete the toolkit. Together they turn a noisy log into a clear answer in minutes during an incident or a change ticket.

On cloud virtual machines (VMs), jump servers, build agents, and nodes, these tools appear in runbooks and in automation. A junior engineer who can only open an editor is slow at 03:00. A professional who can write a safe pipeline (`grep` → `awk` → `sort | uniq -c`) finds the failing host, the top error code, or the bad config key without guessing. Production judgement means: keep a backup before `sed -i`, avoid recursive greps through huge binary trees, set field separators on purpose, and use `find … -print0 | xargs -0` when file names may contain spaces.

This is **Tutorial 8** in **Module 5: Text Processing** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers. By the end, you will have a small evidence pack from a realistic log that you can explain in an interview.

## Prerequisites

- [Permissions, ACLs, and Special Bits](permissions-acls-and-special-bits.md)
- A **practice Ubuntu 22.04/24.04 VM** (or similar) with a normal user account
- Basic shell skills: redirect with `>`, pipes `|`, and `tee`

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Choose grep, sed, or awk for a given log or config task
- [ ] Filter and invert matches with `grep`, including useful flags (`-E`, `-v`, `-n`, `-I`)
- [ ] Edit text safely with `sed` (stream edit and backup before in-place change)
- [ ] Build a field report with `awk` and rank frequencies with `sort | uniq -c`
- [ ] Package a copy-paste pipeline and evidence files under `~/rebash-linux/lab08`

## Architecture

Text tools sit between raw files or streams and the answers you need for ops: filter → transform → summarise → feed the next command.

![Architecture diagram for Text Processing with grep, sed, and awk](../assets/excalidraw/linux-text-processing.svg)

## Theory

### What it is

**Text processing** means working on line-oriented data without loading everything into a graphical tool.

| Tool | Plain meaning | Typical job |
|------|---------------|-------------|
| `grep` | “Show me matching lines” | Find `ERROR`, exclude noise with `-v` |
| `sed` | “Edit the stream” | Replace a config value, strip prefixes |
| `awk` | “Split fields and report” | Column extract, counts, simple maths |
| `cut` / `tr` | Slice characters or change sets | Fixed delimiters, lowercase |
| `sort` / `uniq` / `wc` | Order, unique, count | Top-N errors, line counts |
| `xargs` | Turn lines into command arguments | Run a command on many files |

```bash title="Terminal"
grep -n ERROR app.log
sed 's/DEBUG/INFO/g' app.log
awk -F: '{print $1}' /etc/passwd | head
```

### Why it matters

Incidents are mostly reading text under time pressure. Engineers who can filter with `grep -E`, extract with `awk -F`, and rank with `sort | uniq -c | sort -nr` resolve tickets faster. The same patterns appear in CI checks (fail the build if a pattern appears) and in configuration management validation. On shared logs, wrong regex or a recursive grep through `/var` can waste CPU and flood your terminal — so precision matters as much as speed.

### How it works

1. **Find** — `grep -RIn --exclude-dir=.git PATTERN dir` (or search one file). `-E` enables extended Regular Expressions (regex). `-v` inverts. `-I` skips binary files.
2. **Edit** — `sed 's/old/new/g'` prints a changed stream. For files, prefer `sed -i.bak '…' file` so you keep a backup, then validate the result.
3. **Report** — `awk` splits on whitespace by default, or use `-F':'` / `-F','`. Fields are `$1`, `$2`, …; `NF` is field count; an `END { … }` block runs after the last line.
4. **Compose** — pipes chain tools: `grep ERROR file | awk '{print $1}' | sort | uniq -c | sort -nr`.
5. **Safe xargs** — `find . -name '*.log' -print0 | xargs -0 grep -H ERROR` so spaces in names do not break the command.

```bash title="Terminal"
# Rank status codes from a space-separated sample access log (field 9 often holds the code)
awk '{print $9}' access.log | sort | uniq -c | sort -nr | head
```

Set `LC_ALL=C` when you need byte-order sort that does not depend on locale.

### Key concepts and comparisons

| Need | Prefer | Avoid when |
|------|--------|------------|
| Locate error lines | `grep -n` / `grep -E` | Opening a multi-GB file in a GUI editor |
| One substitution across many lines | `sed` | Hand-editing hundreds of lines |
| Column report / count | `awk` | Fragile `cut` on irregular spaces |
| Fixed delimiter columns | `cut -d: -f1` | Logs with quoted commas (use awk carefully) |
| Run a command per file | `find … -print0 \| xargs -0` | Plain `xargs` on names with spaces |

| Flag / pattern | Meaning |
|----------------|---------|
| `grep -v` | Exclude matching lines |
| `grep -E` | Extended regex |
| `sed -i.bak` | In-place edit with backup |
| `awk -F:` | Field separator is colon |
| `uniq -c` | Count adjacent identical lines (sort first) |

### Common pitfalls

- Using `sed -i` on production configs with **no backup** and no syntax check.
- Recursive `grep -R` through container image layers or binary directories without excludes.
- Forgetting `-F` in awk when fields are colon- or comma-separated.
- Using `xargs` without `-0` when names may contain spaces or newlines.
- Assuming locale sort order — set `LC_ALL=C` for stable, script-friendly ordering.

## Hands-on Lab

### Objective

Build a small incident-style pipeline on sample logs: filter errors with grep, clean a field with sed, rank top messages with awk/`sort`/`uniq`, and save proof under `~/rebash-linux/lab08`.

### Prerequisites

- Ubuntu 22.04/24.04 (or Debian) with bash
- Packages: `grep`, `sed`, `gawk` or `mawk`, `coreutils` (normally already installed)
- No sudo required for this lab

### Lab environment

Workspace: `~/rebash-linux/lab08`

```bash title="Terminal"
mkdir -p ~/rebash-linux/lab08 && cd ~/rebash-linux/lab08
set -euo pipefail
whoami | tee lab-user.txt
```

!!! example "Expected output"
    directory exists; `lab-user.txt` contains your username.


### Real-world scenario

A payment API on a practice VM is throwing errors after a deploy. You have a copied application log and a small access log. The on-call engineer asks: which error strings are most common, which HTTP status codes appear, and can you produce a one-command summary for the change ticket? You answer with a pipeline and saved output — not with screenshots of an editor.

### Step-by-step tasks

#### Task 1 – Create sample logs

Create realistic sample files you can re-run the lab against.

```bash title="Terminal"
cd ~/rebash-linux/lab08
set -euo pipefail

cat > app.log << 'EOF'
2026-08-02T10:01:01Z INFO  worker=1 started
2026-08-02T10:01:02Z ERROR worker=1 code=TIMEOUT msg=upstream_timeout host=api-1
2026-08-02T10:01:03Z WARN  worker=2 code=RETRY msg=retrying host=api-1
2026-08-02T10:01:04Z ERROR worker=1 code=TIMEOUT msg=upstream_timeout host=api-1
2026-08-02T10:01:05Z ERROR worker=3 code=AUTH msg=token_expired host=api-2
2026-08-02T10:01:06Z INFO  worker=2 request_ok host=api-1
2026-08-02T10:01:07Z ERROR worker=3 code=AUTH msg=token_expired host=api-2
2026-08-02T10:01:08Z ERROR worker=1 code=TIMEOUT msg=upstream_timeout host=api-1
2026-08-02T10:01:09Z DEBUG worker=4 ping host=api-3
2026-08-02T10:01:10Z ERROR worker=2 code=DB msg=connection_reset host=api-1
EOF

cat > access.log << 'EOF'
10.0.0.11 - - [02/Aug/2026:10:01:01 +0000] "GET /health HTTP/1.1" 200 12
10.0.0.22 - - [02/Aug/2026:10:01:02 +0000] "POST /pay HTTP/1.1" 502 34
10.0.0.33 - - [02/Aug/2026:10:01:03 +0000] "POST /pay HTTP/1.1" 502 34
10.0.0.22 - - [02/Aug/2026:10:01:04 +0000] "GET /health HTTP/1.1" 200 12
10.0.0.44 - - [02/Aug/2026:10:01:05 +0000] "POST /pay HTTP/1.1" 500 40
10.0.0.55 - - [02/Aug/2026:10:01:06 +0000] "GET /ready HTTP/1.1" 200 8
10.0.0.22 - - [02/Aug/2026:10:01:07 +0000] "POST /pay HTTP/1.1" 502 34
EOF

wc -l app.log access.log | tee wc-samples.txt
test "$(wc -l < app.log)" -eq 10
test "$(wc -l < access.log)" -eq 7
```

!!! example "Expected output"
    `wc-samples.txt` shows 10 and 7 lines for the two files.


#### Task 2 – grep filter and sed cleanup

Extract ERROR lines, then build a clean `code=…` column with sed.

```bash title="Terminal"
cd ~/rebash-linux/lab08
set -euo pipefail

grep -n 'ERROR' app.log | tee errors-raw.txt
test -s errors-raw.txt
grep -c 'ERROR' app.log | tee errors-count.txt
test "$(cat errors-count.txt)" -eq 5

# Keep only the code=VALUE token from each ERROR line
grep 'ERROR' app.log \
  | sed -E 's/.*code=([A-Z_]+).*/\1/' \
  | tee error-codes.txt

grep -E '^(TIMEOUT|AUTH|DB)$' error-codes.txt | tee error-codes-check.txt
test "$(wc -l < error-codes.txt)" -eq 5
```

!!! example "Expected output"
    five ERROR lines; `error-codes.txt` lists codes such as `TIMEOUT`, `AUTH`, `DB` (one per line).


#### Task 3 – awk reports and frequency ranking

Rank error codes and HTTP status codes; pack evidence.

```bash title="Terminal"
cd ~/rebash-linux/lab08
set -euo pipefail

# Top error codes from the cleaned list
sort error-codes.txt | uniq -c | sort -nr | tee top-error-codes.txt
grep -q 'TIMEOUT' top-error-codes.txt

# HTTP status codes from access.log (field 9 in this Combined-like format)
awk '{print $9}' access.log | sort | uniq -c | sort -nr | tee top-status-codes.txt
grep -q '502' top-status-codes.txt

# Hosts that saw ERROR in app.log
awk '/ERROR/ {
  for (i = 1; i <= NF; i++) {
    if ($i ~ /^host=/) {
      split($i, a, "=")
      print a[2]
    }
  }
}' app.log | sort | uniq -c | sort -nr | tee error-hosts.txt
grep -q 'api-1' error-hosts.txt

tar -czf text-processing-evidence.tgz \
  lab-user.txt wc-samples.txt \
  errors-raw.txt errors-count.txt error-codes.txt \
  top-error-codes.txt top-status-codes.txt error-hosts.txt
ls -l text-processing-evidence.tgz | tee evidence-ls.txt
test -s text-processing-evidence.tgz
```

!!! example "Expected output"
    `TIMEOUT` ranks highest among error codes; `502` appears in status ranks; `text-processing-evidence.tgz` is non-empty.


### Validation steps

- [ ] `errors-count.txt` is `5`
- [ ] `top-error-codes.txt` shows `TIMEOUT` with the highest count
- [ ] `top-status-codes.txt` includes `502` and `200`
- [ ] `error-hosts.txt` mentions `api-1`
- [ ] `text-processing-evidence.tgz` exists under `~/rebash-linux/lab08`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `sed` outputs whole lines, not codes | Regex did not match | Use the exact `sed -E` from Task 2; check sample log spelling |
| Wrong status field in awk | Different log format | Count fields with `awk '{print NF; exit}' access.log` and adjust `$9` |
| `uniq -c` shows all counts as 1 | Forgot to `sort` first | Always `sort` before `uniq` |
| Empty `errors-raw.txt` | Pattern case mismatch | Sample uses `ERROR` in uppercase — match that |

### Challenge exercise

Write an executable script `~/rebash-linux/lab08/incident-summary.sh` that takes a log path as `$1`, prints (1) ERROR count, (2) top three `code=` values, and (3) top three `host=` values for ERROR lines. Run it on `app.log`, save stdout to `challenge-summary.txt`, and `chmod +x` the script. Keep it under 40 lines.

### Learning outcomes

- Filtered and counted ERROR lines with grep
- Extracted fields with sed and awk
- Ranked frequencies with sort/uniq
- Built an evidence archive suitable for a change ticket

### Cleanup

```bash title="Terminal"
cd ~/rebash-linux/lab08
# Keep the evidence archive if you want it; otherwise remove lab artefacts:
# rm -f app.log access.log *.txt incident-summary.sh text-processing-evidence.tgz
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab08/` with evidence files
- [ ] You can explain when to use grep vs sed vs awk
- [ ] You know why `sort` must come before `uniq -c`
- [ ] You can describe the risk of `sed -i` without a backup on a real config

## Code Walkthrough

In real servers, text work for ops usually follows this order:

1. **Sample first** — `head`, `tail`, or a time-bounded export; do not pipe multi-GB files blindly  
2. **Filter early** — `grep`/`grep -v` to cut noise before heavier tools  
3. **Set separators** — `-F` in awk, `-d` in cut; do not guess columns  
4. **Keep backups** — `sed -i.bak` or write to a new file, then validate  
5. **Save evidence** — `tee` or redirect into ticket attachments  

Later you may wrap pipelines in scripts or CI jobs. People still review the regex and the field numbers.

## Security Considerations

- Do not paste secrets from logs into tickets or chat — redact tokens and passwords  
- Restrict who can read production log directories (`/var/log`, journal)  
- Prefer read-only copies of logs in the lab; avoid editing live configs with ad-hoc sed  
- Be careful with `sudo grep` over home directories of other users  
- In CI, fail closed on secret-like patterns (API keys) rather than only on ERROR strings  

## Common Mistakes

!!! warning "Running `sed -i` with no backup on a live config"
    A bad substitute can break SSH or the application on the next reload. **Fix:** use `sed -i.bak`, test on a copy, and keep a console session open when changing remote access configs.

!!! warning "Forgetting to sort before `uniq -c`"
    `uniq` only collapses **adjacent** duplicate lines. **Fix:** `sort file | uniq -c | sort -nr`.

!!! warning "Using plain `xargs` on file names from `find`"
    Names with spaces split into wrong arguments. **Fix:** `find … -print0 | xargs -0 …`.

!!! warning "Recursive grep through huge trees"
    You waste time and I/O. **Fix:** narrow the path, add `--exclude-dir`, and prefer known log files.

## Best Practices

- Prefer `grep -E` / `sed -E` when extended regex makes the pattern clearer  
- Use `LC_ALL=C` in scripts for stable sorting  
- Name evidence files by intent (`top-error-codes.txt`), not `out1.txt`  
- Put reusable pipelines in small scripts with `"$1"` arguments  
- Document the field numbers you assumed for each log format  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| No matches for a pattern you see in the file | Wrong case or Windows CRLF | Try `grep -i`; strip `\r` with `tr -d '\r'` |
| awk prints wrong column | Different whitespace / quoted fields | Inspect with `awk '{print NF,$0}' \| head` |
| `sed` changes nothing | Pattern does not match | Test one line with `echo … \| sed …` |
| Pipeline hangs | Waiting on stdin | Pass a file argument or end of input |
| Permission denied on `/var/log` | Not in the right group | Use a copied log, or ask for read access — do not chmod production logs casually |

## Summary

grep, sed, and awk turn logs and configs into answers: find, edit, and report. Practise composing short pipelines, keep backups for edits, and save command output as ticket evidence. Next, learn how to inspect and control running programmes in [Process Management](process-management.md).

## Interview Questions

**1. When would you use grep, when sed, and when awk? Give one example each from production ops.**

??? success "Reveal answer"
    Use **grep** to select or exclude lines (`grep -n ERROR app.log`). Use **sed** to transform text in a stream or file (`sed -i.bak 's/old/new/'`). Use **awk** when you need fields or a small report (`awk '{print $9}' access.log | sort | uniq -c`). Interviewers want clear job fit, not tool loyalty.

**2. Why must you sort before `uniq -c`, and how do you get a top-N list?**

??? success "Reveal answer"
    `uniq` only merges **neighbouring** duplicate lines. Without `sort`, counts are wrong. Top-N pattern: `sort file | uniq -c | sort -nr | head -n 10`. This is a standard incident summary for error codes or status codes.

**3. A junior engineer runs `sed -i 's/…/…/' /etc/nginx/nginx.conf` and Nginx fails to start. What went wrong in process, and how do you prevent it?**

??? success "Reveal answer"
    They edited in place with **no backup** and no config test. Recover from backup or package reinstall / version control, then `nginx -t` before reload. Prevent with `sed -i.bak`, edit a copy, validate syntax, and prefer configuration management for lasting changes.

**4. How do you safely run grep over many files whose names may contain spaces?**

??? success "Reveal answer"
    Use null-delimited paths: `find dir -type f -name '*.log' -print0 | xargs -0 grep -H PATTERN`. Without `-print0`/`-0`, spaces split into fake arguments and you miss files or hit the wrong ones.

**5. Access log field numbers differ between formats. How do you avoid hard-coding the wrong column in awk?**

??? success "Reveal answer"
    Inspect first: `head -n 1 access.log` and `awk '{print NF; exit}'`. Prefer formats with clear delimiters (`-F`), or match labelled tokens (`host=`) instead of only `$N` when the line is irregular. Document the assumed format next to the one-liner in the runbook.

**6. What is a production risk of `grep -R` from `/` or from a large container layer directory?**

??? success "Reveal answer"
    High I/O and CPU, long delays, and accidental matches inside binaries or secrets files. Narrow the search path, skip binaries (`-I`), exclude noisy directories, and search known log locations first.

**7. How would you prove in a change ticket that TIMEOUT was the top application error after a deploy?**

??? success "Reveal answer"
    Attach pipeline output: ERROR filter, extracted `code=` values, and `sort | uniq -c | sort -nr` showing TIMEOUT first — plus the time range of the log sample. Evidence beats “we think it was timeouts”.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Permissions, ACLs, and Special Bits](permissions-acls-and-special-bits.md) *(previous)*
- [Process Management](process-management.md) *(next)*
- [Shell Scripting Fundamentals](shell-scripting-fundamentals.md) *(related)*

## References

- [`grep(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/grep.1.html) — Ubuntu man-pages  
- [`sed(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/sed.1.html) — Ubuntu man-pages  
- [`awk(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/awk.1.html) — Ubuntu man-pages  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
