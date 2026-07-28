---
title: File Archiving and Compression
description: Create, extract, and verify archives with tar, gzip, bzip2, and xz for backups and deployment.
difficulty: beginner
estimated_time: "35 min"
author: Shaik Basha
category: linux
tags:
  - linux
  - tar
  - compression
  - backup
prerequisites:
  - Complete Module 5 tutorials or equivalent experience
  - Basic file and directory navigation skills
comments: false
---

# File Archiving and Compression

## Overview

Archiving and compression are daily operations for Linux administrators — backing up configuration, packaging application releases, transferring log bundles to support, and preparing artifacts for CI/CD pipelines. The **`tar`** utility bundles files and directories into a single archive; compression tools like **gzip**, **bzip2**, and **xz** reduce archive size for storage and transfer.

Understanding tar flags, the difference between archiving and compressing, and a safe backup workflow prevents data loss from corrupted archives or premature deletion of source files.

This tutorial is part of **Module 6: Storage, Logs, Networking & Operations** in the REBASH Academy Linux series.

## Prerequisites

- Complete [Essential Linux Commands](essential-linux-commands.md) and [Disk and Filesystem Management](disk-and-filesystem-management.md)
- A Linux system with `tar`, `gzip`, and standard utilities installed
- Write access to home directory or `/tmp` for lab exercises
- Sufficient disk space for sample archives (~50 MB)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Create, list, and extract tar archives with common flag combinations
- [ ] Apply gzip, bzip2, and xz compression and choose the appropriate format
- [ ] Explain tar flags (`-c`, `-x`, `-t`, `-v`, `-f`, `-z`, `-j`, `-J`) confidently
- [ ] Implement a safe backup workflow with verification before deletion
- [ ] Avoid common pitfalls like absolute paths and tarbombs

## Theory

### Archive vs compression

| Concept | Tool | Result |
|---------|------|--------|
| Archive | `tar` | Single file bundling many files (no size reduction) |
| Compress | `gzip`, `bzip2`, `xz` | Reduces byte size of data |

Production pattern combines both: `tar -czf backup.tar.gz /data`

### Essential tar flags

Remember: **c**reate, e**x**tract, lis**t** — always include **f**ile.

| Flag | Long form | Meaning |
|------|-----------|---------|
| `-c` | `--create` | Create new archive |
| `-x` | `--extract` | Extract archive |
| `-t` | `--list` | List contents |
| `-f FILE` | `--file=FILE` | Archive filename (must follow `-f`) |
| `-v` | `--verbose` | Verbose output |
| `-z` | `--gzip` | Filter through gzip (.tar.gz) |
| `-j` | `--bzip2` | Filter through bzip2 (.tar.bz2) |
| `-J` | `--xz` | Filter through xz (.tar.xz) |
| `-C DIR` | `--directory=DIR` | Change to DIR before operation |
| `-p` | `--preserve-permissions` | Preserve permissions (useful for backups) |

Order matters: `tar -czvf archive.tar.gz dir/` not `tar -zcvf` (both work on GNU tar, but `-f` must be last before filename).

### Compression format comparison

| Format | Extension | Speed | Compression | Use case |
|--------|-----------|-------|-------------|----------|
| gzip | `.gz` / `.tar.gz` | Fast | Moderate | Default for most backups |
| bzip2 | `.bz2` / `.tar.bz2` | Slower | Better | Legacy, moderate archives |
| xz | `.xz` / `.tar.xz` | Slowest | Best | Long-term storage, releases |

### Backup workflow best practices

1. **Stop or quiesce** application if consistency required (databases need special handling)
2. **Create archive** with timestamp in filename
3. **Verify** with `tar -tzf` or test extract to temp directory
4. **Copy offsite** (S3, NFS, tape)
5. **Delete old archives** per retention policy — never delete source before verify
6. **Automate** with cron/systemd and log results

### Tar pitfalls

- **Absolute paths:** `tar -czf backup.tar.gz /etc` embeds leading `/` — extract overwrites system paths. Prefer `-C /etc .` or relative paths.
- **Tarbomb:** Archive extracts files into current directory without a top-level folder. Always create archives from parent directory with a named folder.
- **Special files:** Sockets and pipes may warn during archive — usually safe to ignore for config backups.

## Hands-on Lab

### Step 1 – Prepare lab data

```bash
mkdir -p ~/lab-backup/{app,logs,config}
echo "version=1.0" > ~/lab-backup/config/app.conf
echo "db=postgres" >> ~/lab-backup/config/app.conf
echo "2026-07-27 INFO started" > ~/lab-backup/logs/app.log
echo "sample application data" > ~/lab-backup/app/data.txt
tree ~/lab-backup 2>/dev/null || find ~/lab-backup -type f
```

**Expected output:** Directory tree with three subdirectories and sample files.

### Step 2 – Create an uncompressed tar archive

```bash
cd ~
tar -cvf lab-backup.tar lab-backup/
ls -lh lab-backup.tar
tar -tvf lab-backup.tar | head -10
```

**Expected output:** Archive file listed with size; `-t` output shows paths like `lab-backup/config/app.conf` with permissions and sizes.

### Step 3 – Create a gzip-compressed archive

```bash
tar -czvf lab-backup-$(date +%Y%m%d).tar.gz lab-backup/
ls -lh lab-backup-*.tar.gz
```

**Expected output:** `.tar.gz` file smaller than uncompressed `.tar`; verbose listing during creation.

### Step 4 – Extract to a specific directory

```bash
mkdir -p ~/restore-test
tar -xzvf lab-backup-*.tar.gz -C ~/restore-test
diff -r ~/lab-backup ~/restore-test/lab-backup && echo "Extract verified OK"
```

**Expected output:** `Extract verified OK` — extracted content matches source.

### Step 5 – List without extracting

```bash
tar -tzf lab-backup-*.tar.gz
tar -tzf lab-backup-*.tar.gz | wc -l
```

**Expected output:** File listing only; line count matches number of archived files/directories.

### Step 6 – Compare compression formats

```bash
tar -cjf lab-backup.tar.bz2 lab-backup/
tar -cJf lab-backup.tar.xz lab-backup/
ls -lh lab-backup.tar.*
```

**Expected output:** Three compressed files — `.tar.gz` typically smallest time tradeoff; `.tar.xz` often smallest size.

### Step 7 – Production-style backup script

```bash
cat > ~/backup-www.sh << 'EOF'
#!/bin/bash
set -euo pipefail
SRC="$HOME/lab-backup"
DEST="$HOME/backups"
STAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVE="$DEST/lab-backup-$STAMP.tar.gz"
mkdir -p "$DEST"
tar -czf "$ARCHIVE" -C "$HOME" lab-backup
tar -tzf "$ARCHIVE" >/dev/null && echo "Verify OK: $ARCHIVE"
find "$DEST" -name 'lab-backup-*.tar.gz' -mtime +7 -delete
EOF
chmod +x ~/backup-www.sh
~/backup-www.sh
ls -lh ~/backups/
```

**Expected output:** `Verify OK: /home/you/backups/lab-backup-TIMESTAMP.tar.gz`

### Step 8 – Extract a single file from archive

```bash
tar -xzf ~/backups/lab-backup-*.tar.gz -C /tmp \
  lab-backup/config/app.conf --strip-components=1 2>/dev/null || \
  tar -xzf ~/backups/lab-backup-*.tar.gz -O lab-backup/config/app.conf
```

**Expected output:** Contents of `app.conf` printed or extracted to `/tmp`.

## Commands

| Command | Description |
|---------|-------------|
| `tar -cvf arch.tar dir/` | Create uncompressed archive |
| `tar -czvf arch.tar.gz dir/` | Create gzip-compressed archive |
| `tar -cjvf arch.tar.bz2 dir/` | Create bzip2-compressed archive |
| `tar -cJvf arch.tar.xz dir/` | Create xz-compressed archive |
| `tar -xvf arch.tar` | Extract uncompressed archive |
| `tar -xzvf arch.tar.gz` | Extract gzip archive |
| `tar -xjvf arch.tar.bz2` | Extract bzip2 archive |
| `tar -xJvf arch.tar.xz` | Extract xz archive |
| `tar -tvf arch.tar` | List archive contents (verbose) |
| `tar -tzf arch.tar.gz` | List gzip archive (quiet) |
| `tar -xvf arch.tar -C /dest` | Extract to specific directory |
| `tar -xzf arch.tar.gz path/to/file` | Extract single file |
| `gzip file` | Compress single file (replaces original) |
| `gunzip file.gz` | Decompress .gz file |
| `zcat file.tar.gz \| tar -tvf -` | List archive from stdin pipe |
| `du -sh dir/` | Check directory size before backup |

## Code Examples

### Safe /etc backup (requires root)

```bash
#!/bin/bash
# backup-etc.sh — snapshot configuration with verification
set -euo pipefail

DEST="/backups"
STAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVE="$DEST/etc-backup-$STAMP.tar.gz"

sudo mkdir -p "$DEST"
sudo tar -czpf "$ARCHIVE" -C / etc
sudo tar -tzf "$ARCHIVE" >/dev/null
echo "Backup complete: $ARCHIVE ($(du -h "$ARCHIVE" | cut -f1))"
```

### Exclude patterns for large trees

```bash
tar -czvf backup.tar.gz \
  --exclude='*.log' \
  --exclude='node_modules' \
  --exclude='.git' \
  -C /var/www myapp/
```

### Parallel compression with pigz (if installed)

```bash
tar -cvf - /data | pigz > backup-$(date +%F).tar.gz
```

### Restore script with safety check

```bash
#!/bin/bash
set -euo pipefail
ARCHIVE="${1:?Usage: $0 archive.tar.gz}"
DEST="${2:?Usage: $0 archive.tar.gz /restore/path}"

mkdir -p "$DEST"
tar -tzf "$ARCHIVE" >/dev/null || { echo "Archive corrupt"; exit 1; }
tar -xzf "$ARCHIVE" -C "$DEST"
echo "Restored to $DEST"
```

## Common Mistakes

!!! warning "Deleting source before verifying archive"
    Always run `tar -tzf archive.tar.gz` or test extract before removing originals.

!!! warning "Creating archives with absolute paths"
    `tar -czf backup.tar.gz /var/www` extracts to `/` and can overwrite live files. Use `-C /var/www .` instead.

!!! warning "Wrong -f flag position"
    The filename must immediately follow `-f`. `tar -cfvz` is wrong; use `tar -czvf file.tar.gz`.

!!! warning "Extracting untrusted archives as root"
    Malicious tarballs can contain path traversal (`../../etc/passwd`). Inspect with `-t` first; extract as non-root when possible.

!!! warning "Forgetting -C on extract"
    Without `-C`, files extract into the current directory — potential tarbomb mess.

## Best Practices

!!! tip "Timestamp archive filenames"
    Use `backup-$(date +%Y%m%d-%H%M%S).tar.gz` for uniqueness and sortability.

!!! tip "Use -C for clean paths"
    `tar -czf backup.tar.gz -C /var/www .` creates relative paths without leading slash.

!!! tip "Verify after every backup"
    Integrate `tar -tzf "$ARCHIVE" >/dev/null` into backup scripts as a gate before offsite copy.

!!! tip "Match compression to workload"
    gzip for frequent daily backups; xz for monthly long-term archives where size matters more than speed.

!!! tip "Encrypt sensitive backups"
    Use `gpg --symmetric` or restic/borg for backups containing secrets — tar alone provides no encryption.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Cannot open: No such file` | Wrong path or missing `-C` | Verify source path; use absolute paths in scripts |
| `Unexpected EOF` | Incomplete/corrupt archive | Re-transfer file; check disk space during creation |
| `Permission denied` | Insufficient privileges | Use `sudo` for system dirs; check destination permissions |
| Archive larger than source | Already compressed content | Exclude `.gz`, `.zip`, media files; compress less compressible data |
| `File changed as we read it` | Active log files changing | Normal for live logs; use `--warning=no-file-changed` or stop service |
| Extract overwrites files | No confirmation prompt | Extract to empty directory; use `-k` (keep) to skip existing |
| gzip: stdin: unexpected end | Truncated download | Re-download; verify checksum (sha256sum) |
| Out of disk space mid-backup | Destination full | Monitor with `df -h`; use `set -e` in scripts to fail fast |

## Summary

- `tar` archives files; gzip/bzip2/xz compress the result — commonly combined as `.tar.gz`.
- Core flags: **c**reate, e**x**tract, lis**t**, **f**ile — e.g., `tar -czvf backup.tar.gz dir/`.
- Always verify archives with `-t` or test extract before deleting source data.
- Use `-C` to control paths and avoid absolute-path tarbombs on restore.
- Production backups need timestamps, verification, retention, offsite copy, and logging.

## Interview Questions

**1. What is the difference between tar and gzip?**

*Sample answer:* tar bundles multiple files into one archive without compression. gzip compresses a single file or stream. Together, `tar -czf` creates a compressed archive `.tar.gz`.

**2. How do you create a compressed archive of /var/log?**

*Sample answer:* `sudo tar -czvf logs-backup.tar.gz -C /var log` — using `-C /var log` avoids embedding an absolute `/var/log` path that would extract to root.

**3. How do you list contents without extracting?**

*Sample answer:* `tar -tzf archive.tar.gz` for gzip archives, or `tar -tvf archive.tar` for uncompressed.

**4. What does the -v flag do?**

*Sample answer:* Verbose — lists files as they are archived or extracted. Useful for monitoring progress on large backups.

**5. How do you extract an archive to a specific directory?**

*Sample answer:* `tar -xzf archive.tar.gz -C /destination/path`

**6. Which compression format would you choose for daily vs monthly backups?**

*Sample answer:* gzip for daily backups (fast, good enough ratio). xz for monthly long-term archives where minimum size matters and compression time is acceptable.

**7. What is a tarbomb?**

*Sample answer:* An archive that extracts thousands of files into the current directory without a top-level folder, cluttering the working directory. Prevent by inspecting with `-t` and extracting to a dedicated directory.

**8. How do you extract a single file from a tar.gz?**

*Sample answer:* `tar -xzf archive.tar.gz path/to/file` — specify the exact path shown in `tar -tzf` output.

**9. Why should you verify backups before deleting source data?**

*Sample answer:* Archives can be corrupt due to disk errors, full disks, or interrupted writes. Verification with `tar -t` or test restore confirms recoverability.

**10. What flag preserves permissions during backup?**

*Sample answer:* `-p` ( `--preserve-permissions`) on GNU tar, often default for root. Important when backing up `/etc` or application directories with specific ownership.

## Related Tutorials

- [Linux – Category Overview](index.md)
- [Linux Networking Essentials](linux-networking-essentials.md) *(previous)*
- [Linux Security Hardening Basics](linux-security-hardening-basics.md) *(next)*
- [Cron and Task Scheduling](cron-and-task-scheduling.md)
- [Disk and Filesystem Management](disk-and-filesystem-management.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [GNU tar manual](https://www.gnu.org/software/tar/manual/)
- [tar man page](https://man7.org/linux/man-pages/man1/tar.1.html)
- [gzip man page](https://man7.org/linux/man-pages/man1/gzip.1.html)
- [xz man page](https://man7.org/linux/man-pages/man1/xz.1.html)
- [REBASH Academy – Linux Overview](index.md)
