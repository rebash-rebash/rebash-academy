#!/usr/bin/env python3
"""Apply authored model answers onto interview topic pages (ignore crawled text)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTERVIEW_DIR = ROOT / "docs" / "interview"
ANSWERS_DIR = ROOT / "inbox" / "interview-extracted" / "questions-only" / "answers"


def md_escape_indent(text: str, spaces: int = 4) -> str:
    pad = " " * spaces
    lines = (text or "").strip().splitlines() or [""]
    return "\n".join(pad + (line if line else "") for line in lines)


def apply_topic(topic: str) -> tuple[int, int]:
    page = INTERVIEW_DIR / f"{topic}.md"
    answers_path = ANSWERS_DIR / f"{topic}.json"
    if not page.is_file() or not answers_path.is_file():
        return 0, 0

    authored = {int(item["n"]): item for item in json.loads(answers_path.read_text(encoding="utf-8"))}
    text = page.read_text(encoding="utf-8")

    pattern = re.compile(
        r"(\*\*(\d+)\.\s*(.+?)\*\*\s*\n\n\?\?\? success \"Reveal answer\"\n)(.*?)(?=\n\*\*\d+\.|\n## |\Z)",
        re.S,
    )

    replaced = 0
    missing = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal replaced, missing
        n = int(match.group(2))
        item = authored.get(n)
        if not item or not str(item.get("answer", "")).strip():
            missing += 1
            return match.group(0)
        answer = str(item["answer"]).strip()
        # Keep question text from page; only replace answer body
        replaced += 1
        return match.group(1) + md_escape_indent(answer) + "\n"

    new_text = pattern.sub(repl, text)
    # keep / add scannable wrapper
    if 'class="ra-interview-qa"' not in new_text:
        idx = new_text.find('## ')
        related = new_text.find('## Related')
        if idx != -1 and related != -1:
            new_text = (
                new_text[:idx]
                + '<div class="ra-interview-qa" markdown="1">\n\n'
                + new_text[idx:related]
                + '\n</div>\n\n'
                + new_text[related:]
            )
    page.write_text(new_text, encoding="utf-8")
    return replaced, missing


def main() -> None:
    ANSWERS_DIR.mkdir(parents=True, exist_ok=True)
    total_r = total_m = 0
    for path in sorted(ANSWERS_DIR.glob("*.json")):
        topic = path.stem
        r, m = apply_topic(topic)
        total_r += r
        total_m += m
        print(f"{topic}: replaced={r} missing={m}")
    print(f"TOTAL replaced={total_r} missing={total_m}")


if __name__ == "__main__":
    main()
