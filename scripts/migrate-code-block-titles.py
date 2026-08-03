#!/usr/bin/env python3
"""Add Material fence titles + Expected output admonitions across docs.

Conventions:
  - Create `file.ext`: → next fence gets title="file.ext" (basename)
  - Untitled bash/sh/shell/console/zsh fences → title="Terminal"
  - **Expected output:** … → !!! example "Expected output" admonition

Skips books/ and leaves already-titled fences alone.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

FENCE_RE = re.compile(
    r"(^|\n)(```([a-zA-Z0-9_+-]*)([^\n]*)\n)(.*?)(\n```)",
    re.S | re.M,
)
CREATE_RE = re.compile(
    r"(?is)(?:create|update|edit|author)\s+`([^`]+)`\s*:?\s*$"
)
EXPECTED_RE = re.compile(
    r"(?m)^\*\*Expected output:\*\*\s*(.+?)(?=\n\n|\n#### |\n### |\n## |\n!!! |\n\| |\n- \[ |\Z)",
    re.S,
)
SHELL_LANGS = {"bash", "sh", "shell", "console", "zsh", "shell-session", "text"}


def basename_title(path: str) -> str:
    p = path.strip().strip("/")
    # Drop leading ./ or absolute lab paths → leaf name when clearly a file
    name = Path(p).name
    return name if name else p


def looks_like_commands(body: str) -> bool:
    first = ""
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        first = s
        break
    if not first:
        return False
    # Script shebang → treat as file unless titled via Create
    if first.startswith("#!"):
        return False
    cmd_starts = (
        "cd ",
        "mkdir ",
        "terraform ",
        "docker ",
        "kubectl ",
        "helm ",
        "ansible",
        "aws ",
        "gcloud ",
        "az ",
        "curl ",
        "git ",
        "npm ",
        "pip ",
        "uv ",
        "python",
        "pytest",
        "systemctl ",
        "journalctl ",
        "ss ",
        "ip ",
        "sudo ",
        "apt ",
        "dnf ",
        "yum ",
        "brew ",
        "kind ",
        "argocd ",
        "mkdocs ",
        "export ",
        "source ",
        "set ",
        "test ",
        "grep ",
        "tee ",
        "chmod ",
        "chown ",
        "rm ",
        "cp ",
        "mv ",
        "ls ",
        "cat ",
        "printf ",
        "echo ",
        "for ",
        "while ",
        "if ",
        "true",
        "false",
        "command ",
        "type ",
        "which ",
        "jq ",
        "yq ",
        "ssh ",
        "scp ",
        "rsync ",
        "openssl ",
        "nginx ",
        "podman ",
        "compose ",
        "docker-compose ",
        "gh ",
        "make ",
        "cargo ",
        "go ",
        "node ",
        "pnpm ",
        "yarn ",
        "bundle ",
        "ruby ",
        "perl ",
        "awk ",
        "sed ",
        "find ",
        "xargs ",
        "nohup ",
        "pkill ",
        "kill ",
        "sleep ",
        "wait ",
        "diff ",
        "patch ",
        "tar ",
        "unzip ",
        "wget ",
        "http ",
        "nc ",
        "nmap ",
        "tcpdump ",
        "iptables ",
        "ufw ",
        "firewall-cmd ",
        "useradm ",
        "visudo ",
        "id ",
        "getent ",
        "passwd ",
        "usermod ",
        "useradd ",
        "groupadd ",
        "crontab ",
        "timedatectl ",
        "hostnamectl ",
        "uname ",
        "df ",
        "du ",
        "free ",
        "top ",
        "htop ",
        "ps ",
        "lsof ",
        "strace ",
        "openssl ",
    )
    if first.startswith(cmd_starts):
        return True
    if first in {"cd", "pwd", "terraform", "docker", "kubectl", "helm", "ansible-playbook"}:
        return True
    # pipelines / env assigns common in labs
    if first.startswith(("TF_", "AWS_", "KUBECONFIG=", "PATH=", "export")):
        return True
    return False


def migrate_fences(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    # Work on full text with regex but track preceding non-empty line for Create `
    changes = 0

    def repl(m: re.Match) -> str:
        nonlocal changes
        prefix, open_line, lang, rest, body, close = (
            m.group(1),
            m.group(2),
            (m.group(3) or "").strip(),
            m.group(4) or "",
            m.group(5),
            m.group(6),
        )
        # Already has title=
        if re.search(r'\btitle\s*=', rest):
            return m.group(0)

        # Find preceding content line before this fence
        start = m.start()
        before = text[:start].rstrip()
        prev_line = before.splitlines()[-1].strip() if before else ""

        create = CREATE_RE.search(prev_line)
        new_rest = rest
        title = None

        if create:
            title = basename_title(create.group(1))
        elif lang.lower() in SHELL_LANGS or lang == "":
            # untitled shell-like: Terminal if commands, else leave (might be output)
            if looks_like_commands(body):
                title = "Terminal"
            elif lang.lower() in {"bash", "sh", "shell", "zsh", "console"} and looks_like_commands(body):
                title = "Terminal"

        if not title:
            return m.group(0)

        # Preserve other attrs; inject title
        attrs = rest.strip()
        if attrs:
            new_open = f"```{lang} title=\"{title}\" {attrs}\n" if lang else f"``` title=\"{title}\" {attrs}\n"
        else:
            new_open = f"```{lang} title=\"{title}\"\n" if lang else f"``` title=\"{title}\"\n"
        # clean double spaces
        new_open = re.sub(r"  +", " ", new_open)
        changes += 1
        return f"{prefix}{new_open}{body}{close}"

    new_text = FENCE_RE.sub(repl, text)
    return new_text, changes


def migrate_expected(text: str) -> tuple[str, int]:
    changes = 0

    def repl(m: re.Match) -> str:
        nonlocal changes
        body = m.group(1).strip()
        # Skip if already an admonition nearby / multi-line weirdness with code
        if body.startswith("!!!") or "```" in body:
            return m.group(0)
        changes += 1
        # Indent admonition body
        if "\n" in body:
            indented = "\n".join(("    " + line if line.strip() else "") for line in body.splitlines())
            return f'!!! example "Expected output"\n{indented}\n'
        return f'!!! example "Expected output"\n    {body}\n'

    return EXPECTED_RE.sub(repl, text), changes


def process_file(path: Path, dry_run: bool = False) -> tuple[int, int]:
    original = path.read_text(encoding="utf-8")
    text, c1 = migrate_fences(original)
    text, c2 = migrate_expected(text)
    if (c1 or c2) and not dry_run and text != original:
        path.write_text(text, encoding="utf-8")
    return c1, c2


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--path", type=Path, default=DOCS)
    args = ap.parse_args()
    root: Path = args.path
    fence_total = exp_total = files = 0
    for path in sorted(root.rglob("*.md")):
        if "_curriculum" in path.parts or "includes" in path.parts:
            continue
        c1, c2 = process_file(path, dry_run=args.dry_run)
        if c1 or c2:
            files += 1
            fence_total += c1
            exp_total += c2
            print(f"{path.relative_to(ROOT)}  titles=+{c1} expected=+{c2}")
    print(f"\nFiles touched: {files}  fence titles: {fence_total}  expected blocks: {exp_total}")


if __name__ == "__main__":
    main()
