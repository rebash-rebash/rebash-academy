---
title: Text Processing with grep, sed, and awk
description: Filter, transform, and report on text data from the command line using regex, log parsing, and field processing.
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
  - text-processing
  - grep
  - sed
  - awk
prerequisites:
  - Essential Linux Commands
  - Process Management
comments: false
---

# Text Processing with grep, sed, and awk

## Overview

Every production incident eventually lands in a log file: nginx access logs, application stack traces, syslog entries, or CSV exports from a billing system. Before you reach for Python or a spreadsheet, the Linux text-processing trio — **grep**, **sed**, and **awk** — can filter millions of lines in seconds, right on the server.

This tutorial teaches you to read regex patterns confidently, parse real-world log formats, and build one-liner pipelines that answer operational questions: *Which IPs hit `/login` with 401?* *What is the 95th-percentile response time?* *How many errors per minute during the outage window?*

This is **Module 4, Tutorial 9** in the REBASH Academy Linux series.

## Prerequisites

- Comfort with pipes (`|`), redirection, and basic file navigation from [Essential Linux Commands](essential-linux-commands.md)
- Ability to read `/var/log` files (may require `sudo` on some systems)
- A terminal with GNU grep/sed/awk (default on Ubuntu, RHEL, and macOS with minor flag differences noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Write basic and extended regular expressions for line and field matching
- [ ] Use `grep` to search logs by status code, IP address, and time range
- [ ] Apply `sed` for in-place substitutions, line extraction, and log normalization
- [ ] Process delimited and whitespace-separated fields with `awk` (sums, counts, reports)
- [ ] Chain grep → sed → awk into pipelines for ad-hoc incident analysis
- [ ] Avoid common regex pitfalls (greedy matching, unescaped dots, locale issues)

## Architecture

This topic is primarily procedural. The mental model is a straight line from inputs (commands, config files, or manifests) to observable system state — verify each change with the validation steps later in this tutorial.

## Theory

### Regular expressions — the shared language

All three tools rely on **regular expressions (regex)** to describe patterns:

| Metacharacter | Meaning | Example |
|---------------|---------|---------|
| `.` | Any single character | `a.c` matches `abc`, `a1c` |
| `^` | Start of line | `^ERROR` — lines beginning with ERROR |
| `$` | End of line | `failed$` — lines ending with failed |
| `*` | Zero or more of preceding | `colou*r` matches `color`, `colour` |
| `+` | One or more (ERE with `-E`) | `[0-9]+` — one or more digits |
| `?` | Zero or one (ERE) | `https?` — `http` or `https` |
| `[]` | Character class | `[A-F0-9]{2}` — two hex digits |
| `\|` | Alternation (ERE) | `(error\|warn)` |
| `()` | Grouping (ERE) | `(\d{1,3}\.){3}\d{1,3}` — IPv4 |

**Basic regex (BRE)** is the default for grep and sed. Use `grep -E` / `sed -E` for **extended regex (ERE)**, which treats `+`, `?`, `|`, and `()` as metacharacters without backslashes.

Always escape literal dots in IP addresses and domain names: `192\.168\.1\.1`, not `192.168.1.1` (which matches `192X168X1X1`).

### grep — filter lines

`grep` prints lines that match a pattern. Think of it as a **line-level WHERE clause**.

- `-i` — case-insensitive
- `-v` — invert match (show non-matching lines)
- `-c` — count matches
- `-n` — show line numbers
- `-r` / `-R` — recursive directory search
- `-A/-B/-C N` — context lines after/before/around match
- `-E` — extended regex (`egrep` equivalent)
- `-F` — fixed string (no regex; faster for literal search)
- `-w` — whole word match

For log analysis, grep is your first cut: filter by severity, HTTP status, or error string before passing downstream.

### sed — stream editor

`sed` reads input line-by-line, applies editing commands, and writes to stdout. It does not change the file unless you use `-i`.

Common forms:

- `sed 's/old/new/'` — substitute first match per line
- `sed 's/old/new/g'` — substitute all matches
- `sed -n '10,20p'` — print lines 10–20 only (`-n` suppresses default output)
- `sed '/pattern/d'` — delete matching lines
- `sed -E 's/(.*)/\1/'` — capture groups with ERE

Use sed to **normalize** logs (strip timestamps you do not need), **redact** secrets, or **reshape** one format into another before awk processes fields.

### awk — column-oriented programming

`awk` treats each line as a **record** split into **fields** by a delimiter (default: whitespace). `$0` is the full line; `$1`, `$2`, … are fields; `NF` is field count; `NR` is line number.

Built-in variables and patterns make awk a miniature data language:

- `-F:` — set field separator (e.g., `/etc/passwd`)
- `-F'[, ]+'` — multiple delimiters via regex
- `BEGIN { }` — runs before input; `END { }` — runs after
- `/pattern/ { action }` — pattern-action rules

awk excels at **aggregation**: sums, counts, averages, and grouped reports — tasks grep cannot do alone.

### When to use which tool

| Task | Tool |
|------|------|
| Find lines containing "timeout" | grep |
| Replace `WARN` with `WARNING` in output | sed |
| Sum bytes transferred per IP | awk |
| Extract lines 500–600 of a file | sed |
| Count 5xx responses | grep -c or awk |
| Multi-step: filter → normalize → report | pipeline |

## Hands-on Lab

Create a sample nginx-style access log for the exercises:

```bash
mkdir -p ~/lab/logs
cat > ~/lab/logs/access.log << 'EOF'
192.168.1.10 - - [27/Jul/2026:10:00:01 +0000] "GET /api/users HTTP/1.1" 200 4521 "-" "curl/8.0"
192.168.1.22 - - [27/Jul/2026:10:00:02 +0000] "POST /login HTTP/1.1" 401 892 "-" "Mozilla/5.0"
192.168.1.10 - - [27/Jul/2026:10:00:03 +0000] "GET /api/users HTTP/1.1" 200 4521 "-" "curl/8.0"
203.0.113.5 - - [27/Jul/2026:10:00:04 +0000] "GET /admin HTTP/1.1" 403 1200 "-" "scanner/1.0"
192.168.1.22 - - [27/Jul/2026:10:00:05 +0000] "POST /login HTTP/1.1" 401 892 "-" "Mozilla/5.0"
192.168.1.33 - - [27/Jul/2026:10:00:06 +0000] "GET /health HTTP/1.1" 200 15 "-" "kube-probe/1.0"
192.168.1.10 - - [27/Jul/2026:10:00:07 +0000] "GET /api/orders HTTP/1.1" 500 0 "-" "curl/8.0"
192.168.1.10 - - [27/Jul/2026:10:00:08 +0000] "GET /api/orders HTTP/1.1" 500 0 "-" "curl/8.0"
203.0.113.5 - - [27/Jul/2026:10:00:09 +0000] "GET /wp-admin HTTP/1.1" 404 512 "-" "scanner/1.0"
EOF
```

### Step 1 – grep: find failed login attempts

Filter lines with HTTP status `401` on the `/login` path:

```bash
grep -E 'POST /login.*" 401 ' ~/lab/logs/access.log
```

**Expected output:** two lines from `192.168.1.22` with status 401.

Count total 5xx errors:

```bash
grep -E '" 5[0-9]{2} ' ~/lab/logs/access.log | wc -l
```

**Expected output:** `2`

### Step 2 – grep with context and inversion

Show scanner activity with one line of context after each match:

```bash
grep -E 'scanner' -A 1 ~/lab/logs/access.log
```

List all lines **except** successful 200 responses:

```bash
grep -v '" 200 ' ~/lab/logs/access.log
```

**Expected output:** five lines (401×2, 403, 500×2, 404).

### Step 3 – sed: extract and substitute

Print only lines 3 through 6:

```bash
sed -n '3,6p' ~/lab/logs/access.log
```

Replace the IP `203.0.113.5` with `REDACTED` in the output stream (file unchanged):

```bash
sed 's/203\.0\.113\.5/REDACTED/g' ~/lab/logs/access.log | grep REDACTED
```

**Expected output:** two lines with `REDACTED` instead of the scanner IP.

### Step 4 – sed: delete noise

Remove health-check probe lines from analysis:

```bash
sed '/kube-probe/d' ~/lab/logs/access.log | wc -l
```

**Expected output:** `7` (one line removed from the original 8).

### Step 5 – awk: field extraction from delimited data

Parse `/etc/passwd` (colon-separated):

```bash
awk -F: '{printf "%-16s UID=%s SHELL=%s\n", $1, $3, $7}' /etc/passwd | head -5
```

**Expected output:** formatted username, UID, and shell for the first five accounts.

### Step 6 – awk: parse nginx combined log format

Extract IP, status code, and bytes sent. Nginx combined logs use quoted fields; this awk pattern matches the status as field 9 and bytes as field 10 when splitting on whitespace:

```bash
awk '{print $1, $9, $10}' ~/lab/logs/access.log
```

**Expected output:** eight rows like `192.168.1.10 200 4521`.

### Step 7 – awk: aggregate — requests and bytes per IP

```bash
awk '{ ip=$1; status=$9; bytes=$10; count[ip]++; total[ip]+=bytes; if(status>=400) err[ip]++ }
     END { printf "%-16s %6s %10s %6s\n", "IP", "REQS", "BYTES", "ERRS";
           for(i in count) printf "%-16s %6d %10d %6d\n", i, count[i], total[i], err[i]+0 }' \
  ~/lab/logs/access.log | sort -k2 -nr
```

**Expected output:** a sorted table showing `192.168.1.10` with the most requests and bytes, and error counts per IP.

### Step 8 – Full pipeline: incident mini-report

Build a one-liner that finds 4xx/5xx responses, redacts external IPs, and summarizes by status:

```bash
grep -E '" [45][0-9]{2} ' ~/lab/logs/access.log \
  | sed -E 's/^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/CLIENT_IP/' \
  | awk '{ status=$9; codes[status]++ }
         END { for(s in codes) print "HTTP", s":", codes[s], "occurrences" }' \
  | sort -t' ' -k2 -n
```

**Expected output:**

```
HTTP 401: 2 occurrences
HTTP 403: 1 occurrences
HTTP 404: 1 occurrences
HTTP 500: 2 occurrences
```

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

| Command | Description |
|---------|-------------|
| `grep PATTERN FILE` | Print lines matching PATTERN |
| `grep -E 'regex'` | Extended regular expression mode |
| `grep -i PATTERN` | Case-insensitive search |
| `grep -v PATTERN` | Invert match — show non-matching lines |
| `grep -c PATTERN` | Count matching lines |
| `grep -n PATTERN` | Prefix matches with line numbers |
| `grep -r PATTERN DIR` | Recursively search directory |
| `grep -F 'literal'` | Fixed-string search (no regex) |
| `sed 's/old/new/g'` | Substitute all occurrences on each line |
| `sed -n 'START,ENDp'` | Print line range only |
| `sed '/pat/d'` | Delete lines matching pattern |
| `sed -E 's/(a)(b)/\2\1/'` | ERE with capture groups |
| `sed -i.bak 's/x/y/' FILE` | In-place edit with backup |
| `awk '{print $1}'` | Print first field (whitespace-separated) |
| `awk -F: '{print $1}'` | Print first colon-separated field |
| `awk 'NR==1'` | Print first record (line) |
| `awk '/error/ {c++} END {print c}'` | Count lines matching pattern |
| `awk '{sum+=$3} END {print sum}'` | Sum values in third field |

## Code

### Reusable log analysis functions

Save as `~/lab/logfuncs.sh` and `source` it in scripts:

```bash
#!/bin/bash
# logfuncs.sh — helper functions for log parsing

log_errors() {
  local file="${1:?usage: log_errors FILE [PATTERN]}"
  local pattern="${2:-ERROR|FATAL|CRITICAL}"
  grep -E "$pattern" "$file"
}

http_status_count() {
  local file="${1:?usage: http_status_count FILE}"
  awk '{ codes[$9]++ }
       END { for (c in codes) print c, codes[c] }' "$file" | sort -n
}

top_ips() {
  local file="${1:?usage: top_ips FILE}"
  local n="${2:-10}"
  awk '{ count[$1]++ }
       END { for (ip in count) print count[ip], ip }' "$file" \
    | sort -rn | head -n "$n"
}
```

Usage:

```bash
source ~/lab/logfuncs.sh
http_status_count ~/lab/logs/access.log
top_ips ~/lab/logs/access.log 5
```

### CSV field report with awk

```bash
# Given: name,department,salary CSV
awk -F, 'NR>1 { dept[$2]++; sal[$2]+=$3; n[$2]++ }
         END { for(d in dept) printf "%s: %d people, avg salary %.0f\n", d, n[d], sal[d]/n[d] }' \
  employees.csv
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Forgetting to escape dots in IP addresses"
    `grep 192.168.1.1` matches `192X168X1X1`. Use `grep -E '192\.168\.1\.1'` or `grep -F '192.168.1.1'`.

!!! warning "Using sed -i without a backup on production logs"
    `sed -i` modifies files in place. Always test on a copy first: `cp access.log access.log.bak`.

!!! warning "Assuming awk field numbers match every log format"
    JSON logs, tab-separated values, and quoted strings break naive `$9` assumptions. Inspect with `awk '{for(i=1;i<=NF;i++) print i, $i}' file | head -20`.

!!! warning "Greedy regex on large files without narrowing first"
    Running complex regex on multi-GB logs is slow. Pre-filter with `grep -F` on a literal anchor (status code, hostname) before sed/awk.

## Best Practices

!!! tip "Know your log format before writing awk"
    Run `head -3 /var/log/nginx/access.log` and map field positions. Document the format in your runbook.

!!! tip "Prefer grep -F for fixed strings in hot paths"
    Literal search is faster and avoids accidental regex matches on metacharacters in URLs or JSON.

!!! tip "Use LC_ALL=C for ASCII-only performance"
    `LC_ALL=C grep pattern huge.log` can be significantly faster on English/ASCII logs.

!!! tip "Capture one-liners into scripts"
    Ad-hoc pipelines saved in `~/bin/` with parameters become reusable incident tools.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `grep: Invalid range end` | Unescaped `[` in pattern | Escape brackets or use `-F` for literals |
| awk prints blank status fields | Wrong field separator or quoted fields | Change `-F` or preprocess with sed to normalize |
| sed substitution no effect | Pattern does not match; default prints all lines | Verify with `sed -n 's/pat/repl/p'` to print only changed lines |
| No matches on known data | Case sensitivity or Windows `\r` line endings | Try `grep -i`; run `file log.txt` and `dos2unix` if needed |
| Different output on macOS | BSD grep/sed vs GNU | Install GNU coreutils (`ggrep`, `gsed`) or adjust flags |
| Pipeline returns nothing | Upstream filter too aggressive | Test each stage independently; use `| tee /tmp/stage1` |

## Summary

- **grep** filters lines — start every log investigation here with literal or regex patterns.
- **sed** transforms the stream — substitute, delete, and extract without loading files into an editor.
- **awk** computes on fields — counts, sums, and grouped reports that turn raw logs into metrics.
- Regex basics (`^`, `$`, `[]`, `-E`) are shared across all three; escape literal dots and test patterns on small samples first.
- Production workflows chain tools: filter → normalize → aggregate, then promote proven one-liners into reusable scripts.

## Interview Questions

1. What is the difference between basic regex (BRE) and extended regex (ERE)? When do you use `grep -E`?
2. How would you count the number of HTTP 404 responses in an nginx access log using only grep?
3. Explain what `awk '{sum+=$3} END {print sum}'` does. What do `$3`, `sum`, and `END` represent?
4. How do you print lines 100–200 of a 10 GB file without loading it into memory?
5. What is the difference between `sed 's/a/b/'` and `sed 's/a/b/g'`?
6. Why should you escape dots when matching IP addresses in regex?
7. How would you find the top 10 source IPs by request count from a combined log format?
8. When would you choose `grep -F` over `grep -E`?
9. What does `awk -F:` change, and name a system file where this is commonly used.
10. How can unquoted regex metacharacters in user-supplied grep patterns become a security concern in shell scripts?

## Related Tutorials

- [Linux – Category Overview](index.md)
- [Package Management](package-management.md) *(previous in Module 3)*
- [Shell Scripting Fundamentals](shell-scripting-fundamentals.md) *(next)*
- [Log Management with journalctl](log-management-journalctl.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [GNU grep manual](https://www.gnu.org/software/grep/manual/grep.html)
- [GNU sed manual](https://www.gnu.org/software/sed/manual/sed.html)
- [GNU awk (gawk) manual](https://www.gnu.org/software/gawk/manual/gawk.html)
- [Regular Expressions — quick reference (regex101 wiki)](https://github.com/firasdarwish/regex101/blob/master/REGEX.md)
- [Nginx log format documentation](https://nginx.org/en/docs/http/ngx_http_log_module.html#log_format)
- [REBASH Academy – Linux Overview](index.md)
