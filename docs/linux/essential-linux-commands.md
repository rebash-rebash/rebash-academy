---
title: Essential Linux Commands
description: Master navigation, file operations, pipes, redirection, find, head/tail/wc, and tab completion for productive daily Linux administration.
difficulty: beginner
estimated_time: "40 min"
author: Shaik Basha
category: linux
tags:
  - linux
  - commands
  - cli
  - pipes
  - redirection
  - find
prerequisites:
  - Complete Introduction to Linux and Linux Filesystem Hierarchy
  - Terminal access with a regular user account
comments: false
---

# Essential Linux Commands

## Overview

The Linux command line is the primary interface for DevOps engineers, SREs, and cloud administrators. GUIs exist, but automation, remote administration over SSH, and production debugging all happen in the shell. The power of Linux CLI comes from **composition** — chaining small, focused programs with **pipes** and **redirection** to build complex workflows from simple building blocks.

This tutorial covers the commands you will use dozens of times per day: navigating the filesystem, creating and manipulating files, searching with `find`, slicing output with `head`/`tail`/`wc`, and accelerating input with **tab completion**. These skills form the foundation for everything else in the REBASH Academy Linux track — permissions, processes, systemd, and shell scripting all assume fluency here.

This is **Tutorial 3** in **Module 1: Foundations** of the REBASH Academy Linux series. It includes theory, hands-on labs, and interview preparation.

## Prerequisites

- Completed [Introduction to Linux](introduction-to-linux.md) and [Linux Filesystem Hierarchy](linux-filesystem-hierarchy.md)
- Terminal access to any Linux system (local VM, WSL2, or cloud instance)
- A regular user account — lab steps avoid destructive system-wide operations
- Familiarity with the concept that paths start from `/` (absolute) or the current directory (relative)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Navigate the filesystem using absolute and relative paths with `cd`, `pwd`, and `ls`
- [ ] Create, copy, move, and safely delete files and directories
- [ ] Chain commands with pipes and redirect stdout/stderr to files
- [ ] Search the filesystem by name, type, size, and modification time using `find`
- [ ] Extract portions of output with `head`, `tail`, and count lines/words/bytes with `wc`
- [ ] Use tab completion and command history efficiently to reduce errors and save time

## Theory

### How the Shell Executes Commands

When you type a command and press Enter, the shell (usually **bash**) parses the line into words, expands variables (`$HOME`), globs patterns (`*.log`), and resolves the command name against `$PATH`. It then calls `fork()` to create a child process and `exec()` to replace that child with the target program. The shell waits for foreground commands to finish before showing the next prompt.

Built-in commands (`cd`, `echo`, `export`) run inside the shell process itself — which is why `cd` can change the shell's working directory while external programs cannot.

### Navigation: Absolute vs Relative Paths

| Type | Starts with | Example | Resolves to |
|------|-------------|---------|-------------|
| Absolute | `/` | `/var/log/syslog` | Same path from anywhere |
| Relative | `.` or directory name | `log/syslog` (from `/var`) | Depends on current directory |
| Home | `~` | `~/projects` | `/home/username/projects` |
| Parent | `..` | `cd ..` | One directory up |

Special directories: `.` (current), `..` (parent), `~` (home), `-` (previous directory for `cd -`).

### Listing and Inspecting Files

`ls` reads directory entries. Important flags:

| Flag | Meaning |
|------|---------|
| `-l` | Long format — permissions, owner, size, date |
| `-a` | Show hidden files (names starting with `.`) |
| `-h` | Human-readable sizes (K, M, G) |
| `-t` | Sort by modification time, newest first |
| `-R` | Recurse into subdirectories |

Combine flags: `ls -lah` is the daily default for sysadmins.

### File Operations: Create, Copy, Move, Delete

| Command | Purpose | Key flags |
|---------|---------|-----------|
| `mkdir` | Create directories | `-p` create parent paths |
| `touch` | Create empty file or update timestamp | — |
| `cp` | Copy files/directories | `-r` recursive, `-a` archive (preserve all) |
| `mv` | Move or rename | Works across filesystems on same mount |
| `rm` | Remove files | `-r` recursive, `-f` force (dangerous) |

**Safety rule:** There is no undo for `rm`. Always verify with `ls` before `rm -rf`.

### Pipes and Redirection

| Operator | Meaning |
|----------|---------|
| `\|` | Pipe stdout of left command to stdin of right |
| `>` | Redirect stdout to file (overwrite) |
| `>>` | Redirect stdout to file (append) |
| `2>` | Redirect stderr to file |
| `&>` | Redirect stdout and stderr together |
| `<` | Redirect file to stdin |
| `2>&1` | Merge stderr into stdout |

Example pipeline: `cat /var/log/syslog | grep ssh | wc -l` counts SSH-related log lines.

### The find Command

`find` traverses directory trees recursively. Unlike `ls`, it supports powerful filters:

| Predicate | Meaning |
|-----------|---------|
| `-name 'pattern'` | Match filename (case-sensitive glob) |
| `-iname 'pattern'` | Case-insensitive name match |
| `-type f` / `-type d` | Files only / directories only |
| `-size +100M` | Larger than 100 megabytes |
| `-mtime -7` | Modified within last 7 days |
| `-empty` | Zero-length files or empty directories |
| `-exec cmd {} \;` | Run command on each match |

Always suppress permission errors in home directories: `find ~ -name '*.txt' 2>/dev/null`.

### head, tail, and wc

| Command | Purpose | Common flags |
|---------|---------|--------------|
| `head` | First N lines | `-n 20` (default 10) |
| `tail` | Last N lines | `-n 50`, `-f` follow (live logs) |
| `wc` | Count lines, words, bytes | `-l` lines, `-w` words, `-c` bytes |

`tail -f /var/log/syslog` is the classic live log monitoring command — press `Ctrl+C` to stop.

### Tab Completion and Command History

**Tab completion** is provided by bash's `readline` library. Press **Tab** once to complete a unique match; press **Tab** twice to list all possibilities. Works for commands, paths, and (with `bash-completion` package) flags for common tools.

**History shortcuts:**

| Shortcut | Action |
|----------|--------|
| `Up` / `Down` | Previous/next command |
| `Ctrl+R` | Reverse search history |
| `!!` | Repeat last command |
| `!grep` | Run last command starting with `grep` |
| `history` | List numbered command history |

## Hands-on Lab

Create a dedicated lab workspace. All steps are safe and self-contained.

### Step 1 – Set up the lab directory and verify location

**Command:**

```bash
mkdir -p ~/lab/essential-commands
cd ~/lab/essential-commands
pwd
```

**Explanation:** `mkdir -p` creates the full path, ignoring errors if parents already exist. `pwd` (print working directory) confirms where you are — always verify before destructive operations.

**Expected output:**

```text
/home/youruser/lab/essential-commands
```

Your username will appear instead of `youruser`.

### Step 2 – Create sample files and list with detail

**Command:**

```bash
touch readme.txt config.yaml
echo "REBASH Academy — Essential Linux Commands" > readme.txt
echo "version: 1" >> readme.txt
ls -lah
```

**Explanation:** `touch` creates empty files or updates timestamps. `>` overwrites; `>>` appends. `ls -lah` shows hidden files, human sizes, and long format permissions.

**Expected output:**

```text
total 16K
drwxrwxr-x 2 youruser youruser 4.0K Jul 27 10:00 .
drwxrwxr-x 3 youruser youruser 4.0K Jul 27 10:00 ..
-rw-rw-r-- 1 youruser youruser   12 Jul 27 10:00 config.yaml
-rw-rw-r-- 1 youruser youruser   48 Jul 27 10:00 readme.txt
```

### Step 3 – Copy, move, and rename files

**Command:**

```bash
cp readme.txt readme.bak
ls -l readme*
mv readme.bak archive/readme-backup.txt 2>/dev/null || \
  (mkdir -p archive && mv readme.bak archive/readme-backup.txt)
ls -R
```

**Explanation:** `cp` duplicates; `mv` moves or renames. The `||` fallback creates `archive/` if the first `mv` fails because the directory does not exist yet.

**Expected output:**

```text
-rw-rw-r-- 1 youruser youruser 48 Jul 27 10:00 readme.txt
.:
archive  config.yaml  readme.txt

./archive:
readme-backup.txt
```

### Step 4 – Practice pipes and redirection

**Command:**

```bash
cat readme.txt | wc -l
cat readme.txt | wc -w
ls /var/log/*.log 2>/dev/null | head -5 > ~/lab/essential-commands/log-list.txt
cat ~/lab/essential-commands/log-list.txt
```

**Explanation:** The pipe sends `cat` output to `wc`. Redirecting `2>/dev/null` hides "file not found" errors from glob expansion. `> file` captures stdout to a file for later inspection.

**Expected output:**

```text
2
6
/var/log/alternatives.log
/var/log/auth.log
/var/log/bootstrap.log
/var/log/dpkg.log
/var/log/kern.log
```

Line/word counts and log filenames vary by system.

### Step 5 – Search with find

**Command:**

```bash
find ~/lab -type f -name "*.txt"
find /etc -type f -name "*.conf" 2>/dev/null | head -5
find ~/lab -type f -mtime -1
```

**Explanation:** First command finds all `.txt` files under the lab tree. Second searches system config (requires permission errors suppressed). Third finds files modified within one day — useful for "what changed recently" audits.

**Expected output:**

```text
/home/youruser/lab/essential-commands/readme.txt
/home/youruser/lab/essential-commands/archive/readme-backup.txt
/etc/adduser.conf
/etc/avahi/avahi-daemon.conf
/etc/brltty/brltty.conf
/etc/brltty/ctbrltty.conf
/etc/brltty/ctbltn.conf
/home/youruser/lab/essential-commands/readme.txt
/home/youruser/lab/essential-commands/archive/readme-backup.txt
/home/youruser/lab/essential-commands/log-list.txt
/home/youruser/lab/essential-commands/config.yaml
```

### Step 6 – Slice output with head and tail

**Command:**

```bash
seq 1 100 > numbers.txt
head -5 numbers.txt
tail -5 numbers.txt
head -3 readme.txt
tail -f numbers.txt &
TAIL_PID=$!
sleep 0.5
echo "101" >> numbers.txt
kill $TAIL_PID 2>/dev/null
```

**Explanation:** `seq` generates a sequence for practice. `head`/`tail` extract edges of files. Background `tail -f` demonstrates live following — it prints new lines as they are appended.

**Expected output:**

```text
1
2
3
4
5
96
97
98
99
100
REBASH Academy — Essential Linux Commands
version: 1
101
```

The `101` line appears from `tail -f` detecting the append.

### Step 7 – Count and summarize with wc

**Command:**

```bash
wc numbers.txt
wc -l /etc/passwd
ls -la ~/lab/essential-commands | wc -l
```

**Explanation:** `wc` without flags shows lines, words, and bytes. `-l` counts lines only — common in pipelines: `ps aux | wc -l` for process count.

**Expected output:**

```text
 100  100 291 numbers.txt
46 /etc/passwd
8
```

The `/etc/passwd` line count reflects the number of user entries on your system.

### Step 8 – Tab completion and navigation shortcuts

**Command:**

```bash
cd /v<Tab>          # press Tab to complete to /var/
cd /var/l<Tab>      # complete toward /var/log/ or list options
cd ~/lab/essential-commands
cd -
pwd
history | tail -5
```

**Explanation:** Tab completion reduces typos on long paths. `cd -` jumps back to the previous directory. `history | tail -5` shows recent commands — use `!NNN` to re-run by number.

**Expected output:**

```text
/home/youruser/lab/essential-commands
  998  wc -l /etc/passwd
  999  ls -la ~/lab/essential-commands | wc -l
 1000  cd /var/log
 1001  cd ~/lab/essential-commands
 1002  history | tail -5
```

History numbers will differ on your system.

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `pwd` | Print working directory | `pwd` |
| `cd` | Change directory | `cd /var/log` |
| `cd -` | Return to previous directory | `cd -` |
| `cd ~` | Go to home directory | `cd ~` |
| `ls` | List directory contents | `ls -lah` |
| `mkdir` | Create directory | `mkdir -p ~/lab/demo` |
| `touch` | Create empty file / update mtime | `touch file.txt` |
| `cp` | Copy files | `cp -a src/ dest/` |
| `mv` | Move or rename | `mv old.txt new.txt` |
| `rm` | Remove files | `rm file.txt` |
| `rm -r` | Remove directory recursively | `rm -r ~/lab/old` |
| `cat` | Concatenate and print files | `cat file1 file2` |
| `echo` | Print text | `echo "hello" > file` |
| `>` | Redirect stdout (overwrite) | `ls > listing.txt` |
| `>>` | Redirect stdout (append) | `echo line >> file` |
| `2>` | Redirect stderr | `cmd 2> errors.log` |
| `\|` | Pipe stdout to next command | `grep error log \| wc -l` |
| `find` | Search directory tree | `find / -name '*.log' 2>/dev/null` |
| `head` | First N lines | `head -20 file.log` |
| `tail` | Last N lines | `tail -50 file.log` |
| `tail -f` | Follow file growth (live) | `tail -f /var/log/syslog` |
| `wc` | Count lines, words, bytes | `wc -l file.txt` |
| `history` | Show command history | `history \| grep find` |
| `clear` | Clear terminal screen | `clear` |
| `man` | Manual page | `man find` |

## Code

### Safe batch rename with a loop

Rename all `.log` files in a directory to include today's date — a pattern used in log archival scripts:

```bash
#!/usr/bin/env bash
# archive-logs.sh — append date suffix to log files in a directory
set -euo pipefail

LOG_DIR="${1:-./logs}"
DATE_SUFFIX="$(date +%Y%m%d)"

mkdir -p "$LOG_DIR"

shopt -s nullglob
for file in "$LOG_DIR"/*.log; do
  base="$(basename "$file" .log)"
  mv -v "$file" "$LOG_DIR/${base}-${DATE_SUFFIX}.log"
done
echo "Renamed logs in $LOG_DIR with suffix $DATE_SUFFIX"
```

### Pipeline to find large files modified in the last 7 days

```bash
find /var/log -type f -mtime -7 -size +10M \
  -exec ls -lh {} \; 2>/dev/null | \
  awk '{print $5, $9}' | \
  sort -rh | \
  head -10
```

### Lab cleanup script (run after completing exercises)

```bash
#!/usr/bin/env bash
# cleanup-essential-commands-lab.sh
read -r -p "Remove ~/lab/essential-commands? [y/N] " confirm
if [[ "${confirm,,}" == "y" ]]; then
  rm -rf ~/lab/essential-commands
  echo "Lab directory removed."
else
  echo "Aborted — no files deleted."
fi
```

## Common Mistakes

!!! warning "Using rm -rf with unverified paths"
    A typo like `rm -rf / tmp/old` (space before `tmp`) or `rm -rf ~/ lab` destroys data catastrophically. Use `echo rm -rf ~/lab/old` first to preview, or `trash-cli` if available. Never run `rm -rf` on paths you have not confirmed with `pwd` and `ls`.

!!! warning "Forgetting 2>/dev/null with broad find searches"
    Running `find / -name secret.txt` floods the terminal with "Permission denied" because most directories are root-only. Always redirect stderr: `find / -name secret.txt 2>/dev/null`, or scope the search: `find /home -name secret.txt`.

!!! warning "Overwriting files with single > redirect"
    `echo "debug" > /etc/app.conf` silently destroys the original config. Use `>>` to append, or edit with `vim`/`nano`. In scripts, check if the file exists before writing.

!!! warning "Piping cat unnecessarily"
    `cat file | grep pattern` is a useless use of cat (UUOC). Prefer `grep pattern file` — one fewer process, same result. Pipes are for connecting program output, not for reading static files.

## Best Practices

!!! tip "Use ls -lah and pwd before every rm or mv"
    Build the habit: `pwd && ls -lah target/` immediately before any destructive command. In scripts, use `"$variable"` quoting to prevent word splitting on paths with spaces.

!!! tip "Compose small pipelines instead of monolithic scripts"
    Start with `find ... | head` to validate matches before adding `| xargs rm`. Incremental pipeline building prevents mass deletion of wrong files.

!!! tip "Install bash-completion for flag completion"
    On Ubuntu/Debian: `sudo apt install bash-completion`. Restart the shell, then type `systemctl sta<Tab>` to see available subcommands. Reduces `--stat` vs `--status` typos under pressure.

!!! tip "Use tail -f with journalctl in modern systems"
    For systemd-managed services, prefer `journalctl -u nginx -f` over hunting log file paths. Know both — legacy apps still log to `/var/log/`.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `command not found` | Not in `$PATH` or not installed | Run `which cmd`; install package; check `/usr/local/bin` |
| `No such file or directory` on cd | Typo or path does not exist | Tab-complete path; use `ls` parent directory first |
| `Permission denied` on cp/mv/rm | Insufficient ownership | Check `ls -l`; use `sudo` only when appropriate |
| Empty pipe output | Left command produced nothing or grep too strict | Run left command alone first; loosen grep pattern |
| `find` takes forever | Searching entire `/` | Narrow path: `find /var /home -name ...`; add `-maxdepth` |
| Tab completion not working | bash-completion not installed | Install package; verify shell is bash (`echo $SHELL`) |
| `tail -f` shows nothing | File not growing or wrong path | Verify with `ls -l file`; check app is logging there |
| `wc` counts differ from editor | Binary vs text line endings | Use `wc -l` on same file; check for `\r` with `file` |
| History shows wrong commands | Multiple terminal sessions | Each session appends independently — expected behavior |

## Summary

- Navigation relies on `pwd`, `cd` (absolute, relative, `~`, `-`), and `ls -lah`
- File operations: `mkdir -p`, `touch`, `cp -a`, `mv`, `rm` — verify before deleting
- Pipes (`|`) chain commands; `>`, `>>`, and `2>` redirect output to files or suppress errors
- `find` searches recursively with powerful filters; always scope paths and handle stderr
- `head`, `tail`, and `wc` slice and count output — essential in every pipeline
- Tab completion and `Ctrl+R` history search dramatically reduce CLI errors and save time

## Interview Questions

1. What is the difference between `>` and `>>`?
2. Explain how a pipe (`|`) works at the process level.
3. How do you find all files larger than 500 MB modified in the last 30 days under `/var`?
4. What does `2>/dev/null` do, and when should you use it?
5. What is the difference between `cp -r` and `cp -a`?
6. How would you monitor a log file in real time?
7. Why is `rm -rf /` dangerous even when run as a regular user?
8. What is the purpose of the `-` argument to `cd`?
9. How does tab completion work, and what package enhances it on Debian/Ubuntu?
10. Write a one-liner to count how many `.conf` files exist under `/etc`.

??? tip "Sample Answers (Questions 1, 3, and 6)"

    **Q1 — > vs >>:** `>` redirects stdout to a file, **creating or truncating** it first — existing content is lost. `>>` redirects stdout and **appends** to the end of the file, preserving existing content. Example: `echo "line1" > file` creates the file; `echo "line2" >> file` adds a second line without deleting the first.

    **Q3 — Large recent files under /var:** `find /var -type f -size +500M -mtime -30 2>/dev/null` — `-type f` limits to files, `-size +500M` means larger than 500 megabytes, `-mtime -30` means modified within the last 30 days. Add `-exec ls -lh {} \;` to see sizes, or `-delete` only after validating matches with `-print` first.

    **Q6 — Real-time log monitoring:** `tail -f /var/log/syslog` follows the file, printing new lines as they are written. For systemd services: `journalctl -u servicename -f`. Press `Ctrl+C` to stop. In production, combine with `grep`: `tail -f /var/log/nginx/access.log | grep " 500 "` to filter live for HTTP 500 errors.

## Related Tutorials

- [Linux – Category Overview](index.md)
- [Linux Filesystem Hierarchy](linux-filesystem-hierarchy.md) *(previous in Module 1)*
- [File Permissions and Ownership](file-permissions-and-ownership.md) *(next — Module 2)*
- [Text Processing with grep, sed, and awk](text-processing-grep-sed-awk.md)
- [Shell Scripting Fundamentals](shell-scripting-fundamentals.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/coreutils.html) — official reference for ls, cp, mv, find, head, tail, wc
- [Linux man pages online](https://man7.org/linux/man-pages/) — `man bash`, `man find`, `man xargs`
- [Bash Reference Manual — Redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)
- [Filesystem Hierarchy Standard (FHS 3.0)](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- [bash-completion project](https://github.com/scop/bash-completion)
- [REBASH Academy – Linux Overview](index.md)
