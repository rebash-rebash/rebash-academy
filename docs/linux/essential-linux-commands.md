---
title: "Essential Linux Commands"
description: "CLI navigate, create, copy, move, view, and inspect files — plain language first, then a real project-tree lab."
difficulty: beginner
estimated_time: "55–70 min"
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
technology: linux
module: "Module 2 · Command Line Essentials"
career_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - cli
  - commands
  - files
  - navigation
  - beginners
prerequisites:
  - linux/boot-process-and-filesystem-hierarchy
next:
  - linux/environment-variables-shell-config
related:
  - labs/linux-ops-toolkit-lab
labs:
  - labs/linux-ops-toolkit-lab
interview: interview/linux
comments: false
---

# Essential Linux Commands

## Overview

These commands show up on day one of almost every Linux role:

**Where am I? What files exist? How do I create, copy, move, or read them safely?**

Every Secure Shell (SSH) session, Continuous Integration (CI) runner, and Kubernetes debug pod starts here. Navigation (`pwd`, `ls`, `cd`), file operations (`mkdir`, `touch`, `cp`, `mv`, `rm`), viewing (`cat`, `head`, `tail`, `less`), and inspection (`stat`, `file`, `history`) are the vocabulary of Linux operations.

**Plain problem:** Incidents go wrong when people guess paths, run destructive `rm -rf` without checking, or dump multi-gigabyte logs with `cat` over a slow SSH link. Operators who can **list before delete**, **page with less**, and **inspect with stat** move faster and with less risk.

This tutorial answers, in order:

1. How does the shell know “where you are”?
2. Which commands create, copy, move, and remove files?
3. When do you use `cat` vs `head` vs `less`?
4. How do you prove file metadata before you change production paths?

This is **Tutorial 3** in **Module 2: Command Line Essentials** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — practical Linux for Cloud and DevOps work.

## Prerequisites

- [Boot Process and Filesystem Hierarchy](boot-process-and-filesystem-hierarchy.md) — you know basic paths like `/etc` and `/home`
- A **practice Ubuntu 22.04/24.04 VM** with a normal user account
- Willingness to create and delete files **only** under your lab directory

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Navigate with `pwd`, `ls`, and `cd` using absolute and relative paths
- [ ] Create, copy, move, and remove files and directories safely
- [ ] View file content with `cat`, `head`, `tail`, and know when to use `less`
- [ ] Inspect metadata with `stat` and `file`, and understand shell `history`
- [ ] Build a small project tree and prove each operation with saved output

## Architecture

The shell keeps a **current working directory**. Commands resolve relative paths against it. File operations change directory entries; viewers read content; inspectors read metadata — all without a graphical file manager.

![Linux CLI workflow — navigate, mutate, view, inspect](../assets/excalidraw/linux-cli-workflow.svg)

## Theory

### The problem (before any jargon)

You SSH to a server for the first time. A teammate says: *“Check `demo-app/logs/app.log` and copy the config sample to `app.env`.”* You type commands and get `No such file or directory`. You were in the wrong folder — and you almost ran `rm -rf` on the wrong path because you did not `ls` first.

This section teaches the command groups that prevent that mistake.

### Navigation — where am I?

**Analogy:** The filesystem is a building. **`pwd`** is the “You are here” sign. **`ls`** is looking at names on the current floor. **`cd`** is walking to another floor.

| Command | Plain meaning |
|---------|----------------|
| **`pwd`** | Print working directory — full path of where you stand |
| **`ls`** | List names in a directory |
| **`cd path`** | Change directory |
| **`cd`** (no args) | Go to your home directory |
| **`cd -`** | Go back to the previous directory |

**What you can say in an interview:** “Before any destructive command I run `pwd` and `ls` to confirm I am in the right place.”

**Tiny example:**

``` {.bash .ra-terminal title="Terminal"}
pwd
ls -la
cd /tmp
pwd
cd -
pwd
```

### Create, copy, move, delete

**Analogy:** **`mkdir`** builds rooms. **`touch`** places an empty box (or updates its “last touched” time). **`cp`** photocopies. **`mv`** relocates or renames. **`rm`** throws items away — there is often no recycle bin.

| Command | Plain meaning | Safety note |
|---------|---------------|-------------|
| **`mkdir -p a/b/c`** | Create nested directories | `-p` creates parents |
| **`touch file`** | Create empty file or update timestamp | Does not add content |
| **`cp src dest`** | Copy file | Overwrites dest silently |
| **`cp -a src dest`** | Archive copy — keeps modes/times | Prefer for config backups |
| **`mv old new`** | Rename or move | Across disks may copy-then-delete |
| **`rm file`** | Delete one file | No undo |
| **`rm -r dir`** | Delete directory tree | **Dangerous** — list first |

**What you can say in an interview:** “I use `cp -a` for config backups, `mv` for renames, and I never run `rm -rf` without listing the path first.”

**Tiny example:**

``` {.bash .ra-terminal title="Terminal"}
mkdir -p project/src
touch project/README.md
cp -a project/README.md project/README.bak
mv project/README.bak project/README.old
ls -la project/
```

### View content — read without breaking SSH

| Command | Use when | Avoid when |
|---------|----------|------------|
| **`cat file`** | Small text file, whole content needed | Multi-GB logs over SSH |
| **`head -n 20 file`** | First lines | You need the middle of a huge file |
| **`tail -n 20 file`** | Last lines | Same |
| **`tail -f file`** | Follow a growing log live | Binary files |
| **`less file`** | Browse/search large text | You only need one line (use `grep` later) |

**What you can say in an interview:** “`cat` for small files; `less` or `tail` for logs; never `cat` a huge file over SSH.”

**Tiny example:**

``` {.bash .ra-terminal title="Terminal"}
head -n 3 /etc/os-release
tail -n 2 /etc/os-release
```

### Inspect — metadata before you edit

| Command | Shows |
|---------|-------|
| **`stat file`** | Size, mode, owner, timestamps, inode |
| **`file file`** | Guessed content type (text, binary, …) |
| **`history`** | Recent commands in this shell session |

**What you can say in an interview:** “`stat` and `file` tell me if something is really a text config before I open it with an editor.”

**Tiny example:**

``` {.bash .ra-terminal title="Terminal"}
stat -c '%n size=%s mode=%A' /etc/passwd
file /etc/passwd
```

### Redirection and pipes (preview)

| Syntax | Plain meaning |
|--------|---------------|
| **`cmd > file`** | Send stdout to file (overwrite) |
| **`cmd >> file`** | Append stdout to file |
| **`cmd 2> file`** | Send errors to file |
| **`cmd1 \| cmd2`** | Pipe stdout of first command into second |

You will use these heavily in the Shell track; here they explain why `cat file | less` is redundant — use `less file` directly.

### Common pitfalls

- Running `rm -rf $DIR` when `$DIR` is empty — deletes unexpected paths
- Using `cat` on huge logs and freezing the SSH session
- Forgetting that `cp` overwrites without asking (unless `-i`)
- Putting passwords on the command line — they appear in `history` and process lists
- Using relative paths in scripts when the working directory changes (cron, systemd)

## Hands-on Lab

### Objective

Build a real mini **application directory tree**, perform copy/move/view/inspect operations, prove each step with files under `~/rebash-linux/lab03`, and package evidence — the same layout a teammate might automate later.

### Prerequisites

| Item | Notes |
|------|--------|
| Ubuntu practice VM | Normal user, write access under `$HOME` |
| No sudo | Main tasks run as your user |

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab03 && cd ~/rebash-linux/lab03
set -euo pipefail
pwd | tee pwd-start.txt
rm -rf demo-app
```

!!! example "Expected output"
    `pwd-start.txt` ends with `lab03`.


### Real-world scenario

You prepare a jump-host folder for a small app: README, config sample, logs, and scripts. You create the layout, reorganise with `mv`/`cp`, inspect with `stat`/`file`, and leave proof for a change ticket.

### Step-by-step tasks

#### Task 1 – Create the project tree with real file content

Create each file in a **file fence** first, then run commands to build the tree.

Create `demo-app/README.md`:

```markdown title="demo-app/README.md"
# demo-app
REBASH lab sample application tree.
```

Create `demo-app/src/main.sh`:

```bash title="demo-app/src/main.sh"
#!/usr/bin/env bash
echo "demo-app start"
```

Create `demo-app/logs/app.log`:

```text title="demo-app/logs/app.log"
INFO start
INFO ready
WARN retry
INFO ok
```

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab03
set -euo pipefail

mkdir -p demo-app/{src,scripts,logs,config}
touch demo-app/config/app.env.sample demo-app/scripts/run.sh

# Create the three file-fence contents above (same text as the green file blocks)
printf '%s\n' '# demo-app' 'REBASH lab sample application tree.' > demo-app/README.md
printf '%s\n' '#!/usr/bin/env bash' 'echo "demo-app start"' > demo-app/src/main.sh
chmod +x demo-app/src/main.sh
printf '%s\n' 'INFO start' 'INFO ready' 'WARN retry' 'INFO ok' > demo-app/logs/app.log

find demo-app -print | sort | tee tree-created.txt
test -d demo-app/logs && test -f demo-app/README.md
```

!!! example "Expected output"
    `tree-created.txt` lists `demo-app/README.md`, `demo-app/src/main.sh`, `demo-app/logs/app.log`, and other paths.


#### Task 2 – Copy, move, view, and inspect

Prove **mutation and inspection** — not just that directories exist.

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab03
set -euo pipefail

cp demo-app/config/app.env.sample demo-app/config/app.env
cp demo-app/logs/app.log demo-app/logs/app.log.bak
mv demo-app/scripts/run.sh demo-app/scripts/start.sh

cat demo-app/README.md | tee readme-cat.txt
head -n 2 demo-app/logs/app.log | tee log-head.txt
tail -n 2 demo-app/logs/app.log | tee log-tail.txt

stat demo-app/src/main.sh | tee stat-main.txt
stat -c '%n size=%s mode=%A' demo-app/src/main.sh | tee stat-short.txt
file demo-app/README.md demo-app/src/main.sh demo-app/logs/app.log | tee file-types.txt

ls -laR demo-app | tee ls-after-ops.txt
test -f demo-app/scripts/start.sh
test ! -e demo-app/scripts/run.sh
grep -q 'demo-app' readme-cat.txt
```

!!! example "Expected output"
    `run.sh` is gone; `start.sh` exists. `file-types.txt` shows text types. `stat-short.txt` has size and mode.


#### Task 3 – Safe delete, history snippet, evidence pack

Prove **careful removal** and package everything.

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab03
set -euo pipefail

echo 'temp' > demo-app/logs/temp.scratch
test -f demo-app/logs/temp.scratch
rm -f demo-app/logs/temp.scratch
test ! -e demo-app/logs/temp.scratch
echo 'removed temp.scratch OK' | tee rm-proof.txt

history 20 2>/dev/null | tee history-snip.txt || \
  fc -l -20 2>/dev/null | tee history-snip.txt || \
  echo 'history-unavailable-in-this-shell' | tee history-snip.txt

wc -l demo-app/logs/app.log | tee log-wc.txt

tar -czf cli-fileops-evidence.tgz \
  pwd-start.txt tree-created.txt readme-cat.txt log-head.txt log-tail.txt \
  stat-main.txt stat-short.txt file-types.txt ls-after-ops.txt \
  rm-proof.txt history-snip.txt log-wc.txt demo-app
ls -l cli-fileops-evidence.tgz | tee evidence-ls.txt
test -s cli-fileops-evidence.tgz
```

!!! example "Expected output"
    `rm-proof.txt` confirms scratch removal. Archive includes `demo-app/` and is non-empty.


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
| Accidental overwrite with `cp` | Destination existed | Use distinct names; try `cp -i` while learning |
| `history` empty | Non-interactive shell | Run lab in interactive bash |

### Challenge exercise

Create `organise-logs.sh`:

```bash title="organise-logs.sh"
#!/usr/bin/env bash
set -euo pipefail
ARCHIVE="demo-app/logs/archive"
mkdir -p "$ARCHIVE"
STAMP="$(date +%Y%m%d)"
DEST="$ARCHIVE/app-${STAMP}.log"
cp demo-app/logs/app.log "$DEST"
echo 'INFO archived-by-organise-logs' >> demo-app/logs/app.log
echo "$DEST"
```

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab03
chmod +x organise-logs.sh
./organise-logs.sh | tee organise-run.txt
test -f "$(cat organise-run.txt)"
grep -q 'archived-by-organise-logs' demo-app/logs/app.log
```

!!! example "Expected output"
    Script prints archived path. New line appears in `app.log`.


### Learning outcomes

- Built a real directory tree with meaningful file content
- Used `cp`, `mv`, and careful `rm` with proof
- Viewed and inspected files with `cat`/`head`/`tail`/`stat`/`file`
- Packaged CLI evidence for a ticket or interview

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab03
# rm -rf demo-app *.txt cli-fileops-evidence.tgz organise-logs.sh
```

## Validation

- [ ] Lab completed under `~/rebash-linux/lab03`
- [ ] Can explain `cat` vs `less` vs `tail` without notes
- [ ] Know why `rm -rf` needs extreme care
- [ ] Can read mode and size from `stat` before editing a file

## Code Walkthrough

1. **`pwd` + `ls` before write** — orient before any change.
2. **`cp -a` for backups** — preserve modes when config matters.
3. **`head`/`less` before edit** — read before you overwrite.
4. **`stat`/`file` on unknown paths** — avoid treating binary as text.
5. **Quote variables in scripts** — empty `$DIR` + `rm -rf` is a career-limiting move.

## Security Considerations

- Never run destructive `rm` from untrusted input or empty variables
- Do not put tokens or passwords on the command line — visible in `history` and `ps`
- Prefer editing copies of production config, then replacing deliberately
- Be careful with shell globs (`*`) in directories with unexpected names
- Restrict write access to deploy directories (permissions in Module 4)

## Common Mistakes

!!! warning "Using `rm -rf` without listing first"
    Typos delete the wrong tree. **Fix:** `ls` the path; quote variables; use `set -u` in scripts.

!!! warning "`cat` on huge log files over SSH"
    Floods your terminal. **Fix:** use `less`, `head`, or `tail`.

!!! warning "Assuming `cp` keeps permissions you care about"
    Default `cp` may not preserve everything. **Fix:** use `cp -a` for config backups.

!!! warning "Passwords in `history`"
    Anyone with shell access may see them. **Fix:** use environment files or secret managers — not CLI passwords.

## Best Practices

- Prefer `mkdir -p` and explicit paths in scripts
- Use `cp -a` before editing important config
- Page with `less`; follow live logs with `tail -f`
- Check type with `file` before treating a path as text
- Keep lab and production data in clearly named directories

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `No such file or directory` | Wrong cwd or path | `pwd`; use absolute path |
| `Permission denied` | Mode/owner | `ls -l`; fix in Module 4 |
| `Is a directory` on `cat` | Path is a directory | `ls` it; cat a file inside |
| `cp` overwrote a file | Destination existed | Restore from backup |
| Binary garbage in terminal | Viewed binary with `cat` | Use `file` first; use `less` carefully |

## Summary

Essential commands are how you **navigate**, **change**, **view**, and **inspect** files on every Linux host. Practise safe operations with proof — not only memorising names. Next: [Filesystem Paths, Links, Mounts, and Inodes](filesystem-paths-links-mounts-and-inodes.md).

## Interview Questions

**1. What is the difference between `pwd` and `ls`, and when do you need both?**

??? success "Reveal answer"
    **`pwd`** prints your current working directory. **`ls`** lists entries in a directory. Use both when a relative path fails: confirm where you are, then see what names exist, before `cd` or a destructive command.

**2. When do you use `cat`, `less`, `head`, and `tail`?**

??? success "Reveal answer"
    **`cat`** for small files you want entirely. **`less`** to browse or search large text. **`head`**/**`tail`** for the start or end; **`tail -f`** follows a growing log during an incident. Avoid `cat` on huge logs over SSH.

**3. Why is `rm -rf` dangerous in scripts, and how do you reduce risk?**

??? success "Reveal answer"
    A wrong or empty variable can delete far more than intended. Reduce risk with `set -u`, quoted variables, path checks (`[[ -d $dir ]]`), and never building paths like `"$ROOT/$REL"` when `$REL` can be empty without checks.

**4. What does `cp -a` give you that plain `cp` may not?**

??? success "Reveal answer"
    **`cp -a`** (archive) preserves permissions, timestamps, and other attributes while copying recursively. Plain `cp` is fine for simple content but may not keep metadata needed for config backups.

**5. How do `stat` and `file` help before you edit a config file?**

??? success "Reveal answer"
    **`stat`** shows size, mode, owner, and timestamps. **`file`** guesses whether content is text or binary. Together they stop you from treating a binary or directory like a text config.

**6. A junior moves `/var/log/app.log` to `/tmp/` to “make space”. What can go wrong?**

??? success "Reveal answer"
    The app may still write to the old inode; `/tmp` may be cleared on reboot; log shipping may break. Better: rotate/compress logs, fix retention, or expand the volume — coordinate with the service owner.

**7. How would you prove you reorganised a directory safely in a ticket?**

??? success "Reveal answer"
    Save `find`/`ls -laR` before and after, show exact `mv`/`cp` commands, keep a backup (`cp -a`), and attach a small archive or listing. Proof is evidence files — not “I think it worked”.

## Related Tutorials

- Previous: [Boot Process and Filesystem Hierarchy](boot-process-and-filesystem-hierarchy.md)
- Next: [Filesystem Paths, Links, Mounts, and Inodes](filesystem-paths-links-mounts-and-inodes.md)
- Lab: [Ops Toolkit](../labs/linux-ops-toolkit-lab.md)

## References

- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/)
- [`bash(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/bash.1.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
