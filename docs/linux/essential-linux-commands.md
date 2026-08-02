---
title: "Essential Linux Commands"
description: "Practise everyday navigation and file commands — pwd, ls, cd, mkdir, rm, cp, mv, touch, cat, less, head, tail, stat, file, and history."
difficulty: beginner
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 2 · Command Line Essentials"
tags:
  - linux
  - cli
  - commands
  - files
  - navigation
prerequisites:
  - linux/boot-process-and-filesystem-hierarchy
next:
  - linux/filesystem-paths-links-mounts-and-inodes
related:
  - labs/linux-ops-toolkit-lab
labs:
  - labs/linux-ops-toolkit-lab
interview: interview/linux
comments: false
---

# Essential Linux Commands

## Overview

Every Secure Shell (SSH) session starts with the same basics: where am I, what files exist, how do I create or move them safely, and how do I read content without breaking a production host. These **essential Linux commands** are the tools you will use every day in Cloud, DevOps, and Site Reliability Engineering (SRE) work.

Navigation commands (`pwd`, `ls`, `cd`) tell you your place in the tree. Mutation commands (`mkdir`, `touch`, `cp`, `mv`, `rm`) create and change files. Viewing commands (`cat`, `less`, `head`, `tail`) show content. Inspection commands (`stat`, `file`, `history`) explain metadata and what you ran before. Redirection (`>`, `>>`) and pipes (`|`) combine small tools into short workflows. In this tutorial you will build a real directory tree, copy and move files, inspect them, and save proof under `~/rebash-linux/lab03`.

Incidents go wrong when people guess paths or run destructive `rm -rf` patterns without checking. Operators who can page logs with `less`, follow growth with `tail -f`, and confirm type with `file`/`stat` move faster and with less risk. The same commands appear inside containers and Continuous Integration (CI) runners, so this fluency transfers across hosts.

This is **Tutorial 3** in **Module 2: Command Line Essentials** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, SRE, and platform engineers. By the end, you will have a small project tree and an evidence archive you can show as CLI practice.

## Prerequisites

- [Boot Process and Filesystem Hierarchy](boot-process-and-filesystem-hierarchy.md)
- A **practice Ubuntu 22.04/24.04 VM** with a normal user account
- Willingness to create and delete files only under your lab directory

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Navigate with `pwd`, `ls`, and `cd` using absolute and relative paths
- [ ] Create, copy, move, and remove files and directories safely
- [ ] View file content with `cat`, `head`, `tail`, and `less` (when appropriate)
- [ ] Inspect metadata with `stat` and `file`, and use shell `history`
- [ ] Build a small directory tree and prove each operation with saved output

## Architecture

The shell keeps a **current working directory**. Commands resolve relative paths against it. File operations create or change directory entries; viewers and inspectors read content and metadata without needing a graphical file manager.

![Architecture diagram for Essential Linux Commands](../assets/excalidraw/linux-cli-workflow.svg)

## Theory

### What it is

| Need | Commands |
|------|----------|
| Where am I / list / move | `pwd`, `ls`, `cd` |
| Create empty file / dirs | `touch`, `mkdir` |
| Copy / rename-move / delete | `cp`, `mv`, `rm` |
| View content | `cat`, `less`, `head`, `tail` |
| Inspect | `stat`, `file`, `history` |

```bash
pwd
ls -la
mkdir -p project/src
touch project/README.md
```

### Why it matters

Automation, deploys, and incident response all assume you can navigate and change files without surprises. A wrong `rm` or `mv` on a production path causes outages. Clear use of `cp -a`, careful `rm`, and checking with `ls`/`stat` before destructive steps is professional baseline skill — not “beginner only”.

### How it works

1. The shell stores the current directory; `pwd` prints it.
2. `ls` lists names; `-a` includes hidden (dot) files; `-l` long format; `-h` human sizes with `-l`.
3. `cd` changes directory; `cd -` returns to the previous directory; `cd` alone goes to `$HOME`.
4. `mkdir -p` creates parent paths; `touch` creates empty files or updates timestamps.
5. `cp` copies; `cp -a` archives (mode/timestamps/links as documented); `mv` renames or relocates; `rm` unlinks names (`-r` for directories — dangerous).
6. `cat` dumps a whole file; `less` pages; `head`/`tail` show ends (`tail -f` follows).
7. `stat` shows inode metadata; `file` guesses content type; `history` lists past commands.

```bash
cp -a src dest
mv oldname newname
head -n 20 app.log
stat -c '%n %s %A' app.log
file app.log
```

### Key concepts and comparisons

| Need | Prefer | Avoid |
|------|--------|-------|
| Whole small file | `cat` | `cat` on multi-gigabyte logs |
| Browse / search large file | `less` | Dumping huge files to SSH |
| First or last lines | `head` / `tail` | Opening binary files as text |
| Preserve mode/timestamps | `cp -a` | Blind `cp` when attributes matter |
| Delete directory tree | `rm -r` only after `ls` | `rm -rf /` patterns and unquoted globs |

| Redirection | Meaning |
|-------------|---------|
| `>` | Overwrite stdout to a file |
| `>>` | Append stdout |
| `2>` | Redirect stderr |
| `\|` | Pipe stdout to next command |

### Common pitfalls

- Running `rm -rf` with a variable that expands empty (deletes unexpected paths).
- Using `cat file | less` instead of `less file`.
- Forgetting that `mv` across filesystems copies-then-deletes (attributes/space matter).
- Editing production files in place with no backup copy.
- Trusting `history` for secrets — never put passwords on the command line.

## Hands-on Lab

### Objective

Build a real mini project tree with copy/move/view/inspect operations, prove each step with files under `~/rebash-linux/lab03`, and package evidence. This lab is **file operations**, not a generic host baseline.

### Prerequisites

- Ubuntu 22.04/24.04 practice VM
- Write access to your home directory
- No sudo required for the main tasks

### Lab environment

Workspace: `~/rebash-linux/lab03`

```bash
mkdir -p ~/rebash-linux/lab03 && cd ~/rebash-linux/lab03
set -euo pipefail
pwd | tee pwd-start.txt
rm -rf demo-app
```

**Expected output:** `pwd-start.txt` ends with `lab03`; clean slate for `demo-app`.

### Real-world scenario

You are preparing a small application directory on a jump host: README, config sample, logs folder, and a scripts folder. You must create the layout, populate files, reorganise with `mv`/`cp`, and leave proof for a teammate who will automate the same layout later.

### Step-by-step tasks

#### Task 1 – Create a project tree and files

```bash
cd ~/rebash-linux/lab03
set -euo pipefail

mkdir -p demo-app/{src,scripts,logs,config}
touch demo-app/README.md
touch demo-app/src/main.sh demo-app/scripts/run.sh
touch demo-app/config/app.env.sample

cat > demo-app/README.md << 'EOF'
# demo-app
REBASH lab sample application tree.
EOF

cat > demo-app/src/main.sh << 'EOF'
#!/usr/bin/env bash
echo "demo-app start"
EOF

cat > demo-app/logs/app.log << 'EOF'
INFO start
INFO ready
WARN retry
INFO ok
EOF

find demo-app -print | sort | tee tree-created.txt
test -f demo-app/README.md
test -d demo-app/logs
```

**Expected output:** `tree-created.txt` lists `demo-app` paths including `README.md`, `src/main.sh`, and `logs/app.log`.

#### Task 2 – Copy, move, view, and inspect

```bash
cd ~/rebash-linux/lab03
set -euo pipefail

cp -a demo-app/config/app.env.sample demo-app/config/app.env
cp demo-app/logs/app.log demo-app/logs/app.log.bak
mv demo-app/scripts/run.sh demo-app/scripts/start.sh

# Viewing (small files — safe to cat)
cat demo-app/README.md | tee readme-cat.txt
head -n 2 demo-app/logs/app.log | tee log-head.txt
tail -n 2 demo-app/logs/app.log | tee log-tail.txt

# Metadata
stat demo-app/src/main.sh | tee stat-main.txt
stat -c '%n size=%s mode=%A' demo-app/src/main.sh | tee stat-short.txt
file demo-app/README.md demo-app/src/main.sh demo-app/logs/app.log | tee file-types.txt

ls -laR demo-app | tee ls-after-ops.txt
test -f demo-app/scripts/start.sh
test ! -e demo-app/scripts/run.sh
grep -q 'demo-app' readme-cat.txt
```

**Expected output:** `run.sh` is gone and `start.sh` exists; `file-types.txt` shows text types; `stat-short.txt` has size and mode.

#### Task 3 – Safe delete proof, history snippet, evidence pack

```bash
cd ~/rebash-linux/lab03
set -euo pipefail

# Create a disposable file, then remove it deliberately (not rm -rf /)
echo 'temp' > demo-app/logs/temp.scratch
test -f demo-app/logs/temp.scratch
rm -f demo-app/logs/temp.scratch
test ! -e demo-app/logs/temp.scratch
echo 'removed temp.scratch OK' | tee rm-proof.txt

# history may be empty in some non-interactive shells — still capture what we can
history 20 2>/dev/null | tee history-snip.txt || \
  fc -l -20 2>/dev/null | tee history-snip.txt || \
  echo 'history-unavailable-in-this-shell' | tee history-snip.txt

# less is interactive — demonstrate non-interactive page count instead with wc
wc -l demo-app/logs/app.log | tee log-wc.txt

tar -czf cli-fileops-evidence.tgz \
  pwd-start.txt tree-created.txt readme-cat.txt log-head.txt log-tail.txt \
  stat-main.txt stat-short.txt file-types.txt ls-after-ops.txt \
  rm-proof.txt history-snip.txt log-wc.txt demo-app
ls -l cli-fileops-evidence.tgz | tee evidence-ls.txt
test -s cli-fileops-evidence.tgz
```

**Expected output:** `rm-proof.txt` confirms scratch removal; archive includes the `demo-app` tree and is non-empty.

### Validation steps

- [ ] `demo-app/` contains `src`, `scripts`, `logs`, `config`
- [ ] `scripts/start.sh` exists (renamed from `run.sh`)
- [ ] `config/app.env` is a copy of the sample
- [ ] `stat-short.txt` and `file-types.txt` exist
- [ ] `cli-fileops-evidence.tgz` exists under `~/rebash-linux/lab03`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `mkdir: cannot create directory` | Parent missing without `-p` | Use `mkdir -p` |
| `mv: cannot stat` | Wrong path | `ls` the parent; fix spelling |
| Accidental overwrite with `cp` | Destination existed | Use distinct names; consider `cp -i` while learning |
| `history` empty | Non-interactive shell | Run in interactive bash; note unavailable in evidence |

### Challenge exercise

Write an executable script `~/rebash-linux/lab03/organise-logs.sh` that:

1. Creates `demo-app/logs/archive/` if needed  
2. Copies `demo-app/logs/app.log` to `demo-app/logs/archive/app-$(date +%Y%m%d).log`  
3. Appends one line `INFO archived-by-organise-logs` to `demo-app/logs/app.log`  
4. Prints the archived file path  

Run it once and keep the script as your stretch artefact.

### Learning outcomes

- Created a real directory tree with `mkdir` and `touch`
- Used `cp`, `mv`, and careful `rm` with proof
- Viewed and inspected files with `cat`/`head`/`tail`/`stat`/`file`
- Packaged a CLI evidence archive

### Cleanup

```bash
cd ~/rebash-linux/lab03
# Keep cli-fileops-evidence.tgz if you want it.
# rm -rf demo-app *.txt cli-fileops-evidence.tgz
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab03/` with a real `demo-app` tree
- [ ] You can explain when to use `cat` vs `less` vs `tail`
- [ ] You know why `rm -rf` needs extreme care
- [ ] You can inspect a file with `stat` and `file` before changing it

## Code Walkthrough

In production, everyday file work usually follows this order:

1. **Orient** — `pwd`, `ls -la`  
2. **Read before write** — `head`/`less`/`stat`  
3. **Change with copies** — `cp` backup, then edit or `mv`  
4. **Prove** — `ls`, `stat`, or a checksum when it matters  
5. **Avoid secrets on the CLI** — do not put passwords in `history`  

Scripts should use `set -euo pipefail`, quote variables, and prefer `--` before path arguments when names can start with `-`.

## Security Considerations

- Never run destructive `rm` patterns from untrusted input  
- Do not put tokens or passwords on the command line (visible in `history` and process lists)  
- Prefer editing copies of production config, then replace deliberately  
- Be careful with shell globs (`*`) in directories that contain unexpected names  
- Restrict write access to deploy directories (permissions covered in Module 4)

## Common Mistakes

!!! warning "Using `rm -rf` without listing first"
    Typos delete the wrong tree. **Fix:** `ls` the path, prefer trash/backup on shared hosts, quote variables, avoid root-level globs.

!!! warning "`cat` on huge log files over SSH"
    Floods your terminal and session. **Fix:** use `less`, `head`, `tail`, or remote grep tools.

!!! warning "Assuming `cp` keeps permissions you care about"
    Default `cp` may not preserve everything you expect. **Fix:** use `cp -a` (or explicit `--preserve`) when modes/timestamps matter.

!!! warning "Relying on `history` as documentation"
    History is local and may contain secrets. **Fix:** keep deliberate evidence files or scripts in git — not password-bearing history lines.

## Best Practices

- Prefer `mkdir -p` and explicit paths in scripts  
- Use `cp -a` for config backups before edits  
- Page with `less`; follow with `tail -f` during live incidents  
- Check type with `file` before treating a file as text  
- Keep lab and production data in clearly named directories  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `No such file or directory` | Wrong cwd or path | `pwd`; use absolute path |
| `Permission denied` | Mode/owner | Check `ls -l`; fix later with chmod/chown (Module 4) |
| `Is a directory` on `cat` | Path is a directory | `ls` it; cat a file inside |
| `cp` overwrote a file | Destination existed | Restore from backup; use unique names |
| Binary garbage in terminal | Viewed binary with `cat` | Use `file` first; use `less`/`xxd` carefully |

## Summary

Essential commands are how you navigate, change, view, and inspect files on every Linux host. Practise safe file operations with proof — not only memorising names. Next, deepen the filesystem model in [Filesystem Paths, Links, Mounts, and Inodes](filesystem-paths-links-mounts-and-inodes.md).

## Interview Questions

**1. What is the difference between `pwd` and `ls`, and when do you need both?**

??? success "Reveal answer"
    **`pwd`** prints the current working directory path. **`ls`** lists entries in a directory. You need both when a relative path fails: confirm where you are (`pwd`), then see what names exist (`ls`) before you `cd` or run a destructive command.

**2. When do you use `cat`, `less`, `head`, and `tail`?**

??? success "Reveal answer"
    Use **`cat`** for small files you want entirely. Use **`less`** to browse or search large text. Use **`head`**/`**tail**` for the start or end; **`tail -f`** follows a growing log during an incident. Avoid `cat` on huge logs over SSH.

**3. Why is `rm -rf` dangerous in scripts, and how do you reduce risk?**

??? success "Reveal answer"
    A wrong variable or unquoted path can delete far more than intended. Reduce risk with `set -u`, quote variables, assert paths (`[[ -d $dir ]]`), avoid running as root for app cleanup, and never build paths like `"$ROOT/$REL"` when `$REL` can be empty without checks.

**4. What does `cp -a` give you that plain `cp` may not?**

??? success "Reveal answer"
    **`cp -a`** (archive) aims to preserve permissions, timestamps, and other attributes (and copies directories recursively). Plain `cp` is fine for simple content copies but may not keep the metadata you need for config backups or deploy artefacts.

**5. How do `stat` and `file` help before you edit a “config” file?**

??? success "Reveal answer"
    **`stat`** shows size, mode, owner, and timestamps (inode metadata). **`file`** guesses whether content is text, binary, or empty. Together they stop you from treating a binary or a directory like a text config, and they document state before a change.

**6. A junior engineer runs `mv /var/log/app.log /tmp/` on a production host to “make space”. What can go wrong?**

??? success "Reveal answer"
    The app may still write to the old path or reopen the file; `/tmp` may be emptied on reboot; you may break log shipping that expects `/var/log`. Better: rotate/compress logs, fix retention, or expand the volume — and coordinate with the service owner.

**7. How would you prove in a ticket that you reorganised a directory safely?**

??? success "Reveal answer"
    Save `find`/`ls -laR` before and after, show the exact `mv`/`cp` commands, keep a backup copy (`cp -a`), and attach a small archive or listing. Proof is listings and hashes when needed — not “I think it worked”.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Boot Process and Filesystem Hierarchy](boot-process-and-filesystem-hierarchy.md) *(previous)*
- [Filesystem Paths, Links, Mounts, and Inodes](filesystem-paths-links-mounts-and-inodes.md) *(next)*
- [Lab — Ops Toolkit](../labs/linux-ops-toolkit-lab.md) *(more practice)*

## References

- [GNU Coreutils documentation](https://www.gnu.org/software/coreutils/manual/) — `ls`, `cp`, `mv`, `rm`, …  
- [`bash(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/bash.1.html) — shell, history, redirection  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
