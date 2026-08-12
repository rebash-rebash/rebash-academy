#!/usr/bin/env python3
"""
Reformat interview model answers into a scannable structure:

  **In short:** …
  **Key points**
  - …
  **Try this** (optional)
  **Trap** (optional)

Apply to authored JSON and/or markdown pages.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANSWERS_DIR = ROOT / "inbox" / "interview-extracted" / "questions-only" / "answers"
INTERVIEW_DIR = ROOT / "docs" / "interview"

ALREADY = re.compile(r"^\*\*(In short|Quick take|Key points):?\*\*", re.I)
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z`*(\[])")
TRAP_HINT = re.compile(
    r"(?i)\b(failure mode|watch out|trap|avoid|never |risk|classic interview|common mistake|do not |don't |stale |silent )\b"
)
TRY_HINT = re.compile(
    r"(?i)\b(verify|check with|troubleshoot|commands?:|lab check|run `|curl |kubectl |ss |dig |tcpdump |systemctl |terraform |ansible-|docker |aws |\bnc )\b"
)


def _sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    parts = SENT_SPLIT.split(text)
    return [p.strip() for p in parts if p.strip()]


def _bulletize(sentences: list[str], limit: int = 5) -> list[str]:
    out: list[str] = []
    for s in sentences:
        s = s.strip().rstrip(".")
        if not s:
            continue
        # Keep bullets short-ish
        if len(s) > 160:
            s = s[:157].rstrip() + "…"
        out.append(s)
        if len(out) >= limit:
            break
    return out


def reformat_answer(answer: str) -> str:
    raw = (answer or "").strip()
    if not raw:
        return raw
    if ALREADY.search(raw):
        return raw

    # Preserve fenced code blocks
    codes: list[str] = []

    def _park_code(m: re.Match[str]) -> str:
        codes.append(m.group(0).strip())
        return f"\n@@CODE{len(codes) - 1}@@\n"

    body = re.sub(r"```[\s\S]*?```", _park_code, raw)
    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip() and not p.strip().startswith("@@CODE")]

    all_sents: list[str] = []
    for p in paras:
        # Skip pure code placeholders
        if re.fullmatch(r"@@CODE\d+@@", p.strip()):
            continue
        all_sents.extend(_sentences(p))

    if not all_sents:
        return raw

    in_short = all_sents[0]
    if len(in_short) < 50 and len(all_sents) > 1:
        in_short = f"{all_sents[0]} {all_sents[1]}"
        rest = all_sents[2:]
    else:
        rest = all_sents[1:]

    traps: list[str] = []
    tries: list[str] = []
    points: list[str] = []
    for s in rest:
        if TRAP_HINT.search(s):
            traps.append(s)
        elif TRY_HINT.search(s) or (s.count("`") >= 2 and len(s) < 180):
            # Pull backticked commands into Try this when possible
            cmds = re.findall(r"`([^`]+)`", s)
            if cmds and len(s) < 140:
                for c in cmds[:3]:
                    if len(c) < 80 and not c.startswith("http"):
                        tries.append(c)
            else:
                tries.append(s.rstrip("."))
        else:
            points.append(s)

    points = _bulletize(points, 5)
    traps = _bulletize(traps, 2)
    # Dedupe try lines
    seen = set()
    try_clean: list[str] = []
    for t in tries:
        k = t.lower()
        if k in seen:
            continue
        seen.add(k)
        try_clean.append(t)
        if len(try_clean) >= 4:
            break

    lines = [f"**In short:** {in_short}", "", "**Key points**", ""]
    if points:
        for p in points:
            lines.append(f"- {p}")
    else:
        # Ensure we always have some bullets from the short itself if needed
        extra = _bulletize(rest[:3], 3)
        for p in extra:
            lines.append(f"- {p}")

    if try_clean or codes:
        lines.extend(["", "**Try this**", ""])
        if codes:
            for c in codes[:2]:
                lines.append(c)
                lines.append("")
        for t in try_clean:
            if t.startswith("```") or t.startswith("`"):
                lines.append(f"- {t.strip('`')}" if not t.startswith("```") else t)
            else:
                # Prefer monospace for command-like tokens
                if re.match(r"^[a-z0-9_./|-]+\s", t) or " " in t and len(t) < 70:
                    lines.append(f"- `{t}`" if not t.startswith("`") else f"- {t}")
                else:
                    lines.append(f"- {t}")

    if traps:
        lines.extend(["", "**Trap**", ""])
        for t in traps:
            lines.append(f"- {t}")

    text = "\n".join(lines).strip() + "\n"
    # Restore any code placeholders that leaked
    for i, c in enumerate(codes):
        text = text.replace(f"@@CODE{i}@@", c)
    return text.strip()


def md_escape_indent(text: str, spaces: int = 4) -> str:
    pad = " " * spaces
    return "\n".join(pad + (line if line else "") for line in text.splitlines())


def wrap_page_with_class(text: str) -> str:
    """Ensure interview pages wrap Q&A in .ra-interview-qa for CSS."""
    if 'class="ra-interview-qa"' in text or "class='ra-interview-qa'" in text:
        return text
    # Insert after practise tip / before first ##
    marker = "## "
    idx = text.find(marker)
    if idx < 0:
        return text
    # Close before Related or endraw
    related = text.find("## Related")
    endraw = text.find("{% endraw %}")
    close_at = related if related != -1 else endraw
    if close_at == -1:
        return text
    return (
        text[:idx]
        + '<div class="ra-interview-qa" markdown="1">\n\n'
        + text[idx:close_at]
        + "\n</div>\n\n"
        + text[close_at:]
    )


def apply_to_pages() -> None:
    for path in sorted(INTERVIEW_DIR.glob("*.md")):
        if path.name == "index.md":
            continue
        answers_path = ANSWERS_DIR / f"{path.stem}.json"
        if not answers_path.is_file():
            continue
        authored = {int(x["n"]): x for x in json.loads(answers_path.read_text(encoding="utf-8"))}
        text = path.read_text(encoding="utf-8")
        pattern = re.compile(
            r"(\*\*(\d+)\.\s*(.+?)\*\*\s*\n\n\?\?\? success \"Reveal answer\"\n)(.*?)(?=\n\*\*\d+\.|\n## |\n</div>|\Z)",
            re.S,
        )

        def repl(m: re.Match[str]) -> str:
            n = int(m.group(2))
            item = authored.get(n)
            if not item:
                return m.group(0)
            ans = reformat_answer(str(item.get("answer", "")))
            item["answer"] = ans
            return m.group(1) + md_escape_indent(ans) + "\n"

        new_text = pattern.sub(repl, text)
        new_text = wrap_page_with_class(new_text)
        path.write_text(new_text, encoding="utf-8")
        answers_path.write_text(json.dumps(list(authored.values()), indent=2) + "\n", encoding="utf-8")
        print(f"updated {path.name}")


def main() -> None:
    # Reformat JSON first
    for path in sorted(ANSWERS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in data:
            item["answer"] = reformat_answer(str(item.get("answer", "")))
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"json {path.name}: {len(data)}")
    apply_to_pages()


if __name__ == "__main__":
    main()
