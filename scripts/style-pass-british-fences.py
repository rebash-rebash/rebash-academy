#!/usr/bin/env python3
"""British English spelling outside code fences; type untyped opening fences; ensure last_updated."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TODAY = "2026-07-28"

# Order matters for longer phrases first
REPLACEMENTS = [
    (r"\boptimization\b", "optimisation"),
    (r"\bOptimization\b", "Optimisation"),
    (r"\boptimize\b", "optimise"),
    (r"\bOptimize\b", "Optimise"),
    (r"\boptimized\b", "optimised"),
    (r"\bOptimized\b", "Optimised"),
    (r"\boptimizing\b", "optimising"),
    (r"\borganization\b", "organisation"),
    (r"\bOrganization\b", "Organisation"),
    (r"\borganize\b", "organise"),
    (r"\bOrganize\b", "Organise"),
    (r"\borganized\b", "organised"),
    (r"\banalyze\b", "analyse"),
    (r"\bAnalyze\b", "Analyse"),
    (r"\banalyzed\b", "analysed"),
    (r"\banalyzing\b", "analysing"),
    (r"\banalyzer\b", "analyser"),
    (r"\bbehavior\b", "behaviour"),
    (r"\bBehavior\b", "Behaviour"),
    (r"\bbehaviors\b", "behaviours"),
    (r"\bBehaviors\b", "Behaviours"),
    (r"\bfavor\b", "favour"),
    (r"\bFavor\b", "Favour"),
    (r"\bfavored\b", "favoured"),
    (r"\bcolor\b", "colour"),
    (r"\bColor\b", "Colour"),
    (r"\bcolors\b", "colours"),
    (r"\bcustomizable\b", "customisable"),
    (r"\bmodeling\b", "modelling"),
    (r"\bModeling\b", "Modelling"),
]

# Do not rewrite these inside prose either (product / API names)
SKIP_WHOLE = {
    "Color",  # CSS / API sometimes — still convert in prose; ok
}


def split_fence_aware(text: str) -> list[tuple[str, bool]]:
    """Return (chunk, is_code) segments."""
    parts: list[tuple[str, bool]] = []
    idx = 0
    in_code = False
    for m in re.finditer(r"^```.*$", text, re.M):
        if m.start() > idx:
            parts.append((text[idx : m.start()], in_code))
        line = m.group(0)
        if not in_code:
            parts.append((line + "\n", True))
            in_code = True
        else:
            parts.append((line + "\n", True))
            in_code = False
        idx = m.end()
        if idx < len(text) and text[idx] == "\n":
            idx += 1
    if idx < len(text):
        parts.append((text[idx:], in_code))
    return parts


def britishize(text: str) -> str:
    out = []
    for chunk, is_code in split_fence_aware(text):
        if is_code:
            out.append(chunk)
            continue
        for pat, repl in REPLACEMENTS:
            chunk = re.sub(pat, repl, chunk)
        out.append(chunk)
    return "".join(out)


def type_opening_fences(text: str) -> str:
    lines = text.splitlines(keepends=True)
    in_code = False
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^```(\w*)\s*\n?$", line)
        if m:
            lang = m.group(1)
            if not in_code:
                if lang == "":
                    # Heuristic language from following content
                    preview = "".join(lines[i + 1 : i + 6])
                    guessed = guess_lang(preview)
                    line = f"```{guessed}\n" if line.endswith("\n") else f"```{guessed}"
                in_code = True
            else:
                in_code = False
        result.append(line)
        i += 1
    return "".join(result)


def guess_lang(preview: str) -> str:
    p = preview.strip()
    if p.startswith("apiVersion:") or p.startswith("kind:") or re.search(r"^---\n.*apiVersion:", preview, re.S):
        return "yaml"
    if "resource \"" in p or "variable \"" in p or "provider \"" in p or "terraform {" in p:
        return "hcl"
    if p.startswith("{") or p.startswith("["):
        return "json"
    if "package main" in p or "func " in p:
        return "go"
    if "def " in p or "import " in p and "from " in p:
        return "python"
    if p.startswith("FROM ") or p.startswith("# syntax="):
        return "dockerfile"
    if re.match(r"^(sudo |apt |yum |dnf |systemctl |kubectl |docker |git |curl |chmod |chown |ls |cat |echo |export |cd )", p):
        return "bash"
    if p.startswith("$ ") or p.startswith("# "):
        return "bash"
    if "SELECT " in p.upper() or "CREATE TABLE" in p.upper():
        return "sql"
    if p.startswith("<"):
        return "html"
    return "text"


def ensure_last_updated(text: str) -> str:
    if not text.startswith("---"):
        return text
    if re.search(r"^last_updated:", text, re.M):
        return text
    return re.sub(
        r"^(author:.*)$",
        rf'\1\nlast_updated: "{TODAY}"',
        text,
        count=1,
        flags=re.M,
    )


def main() -> None:
    changed = 0
    for path in DOCS.rglob("*.md"):
        if "assets" in path.parts or "includes" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        text = original
        text = ensure_last_updated(text)
        text = britishize(text)
        text = type_opening_fences(text)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print("updated", path.relative_to(ROOT))
    print("done", changed)


if __name__ == "__main__":
    main()
