#!/usr/bin/env python3
"""Harvest Linux/Networking lesson interview questions into answered Interview Prep fragments.

Groups by Beginner / Intermediate / Architect. Answers are grounded in the
source lesson text where possible, then shaped into the scannable format.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

STOP = {
    "a",
    "an",
    "the",
    "of",
    "to",
    "in",
    "on",
    "for",
    "and",
    "or",
    "is",
    "are",
    "what",
    "how",
    "why",
    "do",
    "you",
    "your",
    "with",
    "does",
    "can",
    "when",
    "which",
    "from",
    "that",
    "this",
    "into",
    "about",
}


def norm(q: str) -> str:
    q = q.lower().strip()
    q = re.sub(r"`+", "", q)
    q = re.sub(r"[^a-z0-9\s]", " ", q)
    q = re.sub(r"\s+", " ", q).strip()
    words = [w for w in q.split() if w not in STOP]
    return " ".join(words[:14])


def tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9+]{3,}", text.lower())
    return {w for w in words if w not in STOP}


def extract_lesson_qs(text: str, src: str) -> list[dict]:
    m = re.search(r"^#{1,2}\s+Interview Questions\s*$", text, re.M)
    if not m:
        return []
    rest = text[m.end() :]
    qs: list[dict] = []
    for qm in re.finditer(r"^\*\*(\d+)\.\s*(.+?)\*\*\s*$", rest, re.M):
        q = qm.group(2).strip()
        after = rest[qm.end() : qm.end() + 3500]
        am = re.search(
            r'\?\?\?\s+success\s+"Reveal answer"\s*\n((?:    .*\n?)*)', after
        )
        ans = None
        if am:
            ans = "\n".join(
                line[4:] if line.startswith("    ") else line
                for line in am.group(1).splitlines()
            ).strip()
        qs.append(
            {
                "question": q,
                "level": "intermediate",
                "source": src,
                "answer_raw": ans,
            }
        )
    if qs:
        return qs

    level = None
    for line in rest.splitlines():
        if re.match(r"^#{1,3}\s+Beginner", line, re.I):
            level = "beginner"
            continue
        if re.match(r"^#{1,3}\s+Intermediate", line, re.I):
            level = "intermediate"
            continue
        if re.match(r"^#{1,3}\s+Architect", line, re.I):
            level = "architect"
            continue
        if re.match(r"^#{1,2}\s+(?!Beginner|Intermediate|Architect)", line):
            if level and "interview" not in line.lower():
                break
        nm = re.match(r"^(\d+)\.\s+(.+)$", line.strip())
        if nm and level:
            qs.append(
                {
                    "question": nm.group(2).strip(),
                    "level": level,
                    "source": src,
                    "answer_raw": None,
                }
            )
    return qs


def lesson_paragraphs(text: str) -> list[str]:
    # Drop interview section and front matter noise
    text = re.split(r"^#{1,2}\s+Interview Questions\s*$", text, maxsplit=1, flags=re.M)[
        0
    ]
    text = re.sub(r"^---[\s\S]*?---\s*", "", text, count=1)
    paras = []
    for block in re.split(r"\n\s*\n", text):
        block = re.sub(r"^#+\s*", "", block, flags=re.M)
        block = re.sub(r"[*`>]", "", block)
        block = re.sub(r"\s+", " ", block).strip()
        if 40 <= len(block) <= 420 and not block.startswith("|"):
            paras.append(block)
    return paras


def sanitize(text: str) -> str:
    """Page is wrapped in {% raw %}; strip nested Jinja tags from answers."""
    text = text.replace("{% raw %}", "").replace("{% endraw %}", "")
    text = text.replace("{{", "{ {").replace("}}", "} }")
    return text


_CMD_ALLOW = {
    "ss",
    "ip",
    "dig",
    "curl",
    "wget",
    "systemctl",
    "journalctl",
    "chmod",
    "chown",
    "df",
    "du",
    "ps",
    "top",
    "htop",
    "lsblk",
    "tcpdump",
    "nft",
    "iptables",
    "getfacl",
    "setfacl",
    "bash",
    "ls",
    "cat",
    "grep",
    "awk",
    "sed",
    "find",
    "mount",
    "umount",
    "ping",
    "traceroute",
    "nslookup",
    "kubectl",
    "docker",
    "apt",
    "dnf",
    "yum",
    "sudo",
}


def extract_commands(text: str) -> list[str]:
    """Pull real shell-ish commands from backticks — skip flags and bare filenames."""
    cmds = []
    for m in re.finditer(r"`([^`\n]{2,100})`", text):
        c = sanitize(m.group(1).strip())
        if not c or "{%" in c or "%}" in c:
            continue
        # skip markdown emphasis leftovers / headings
        if c.startswith("#") or c.startswith("*"):
            continue
        # skip pure flags (-c, --help) and bare filenames
        if re.fullmatch(r"-{1,2}[\w.-]+", c):
            continue
        if re.fullmatch(r"[\w.-]+\.(txt|log|md|yml|yaml|json|conf|cfg)", c, re.I):
            continue
        first = c.split()[0].split("/")[-1]
        looks_useful = (
            first in _CMD_ALLOW
            or (" " in c and re.match(r"^[a-zA-Z]", first))
            or c.startswith("sudo ")
            or c.startswith("./")
        )
        if not looks_useful:
            continue
        if c not in cmds:
            cmds.append(c)
        if len(cmds) >= 3:
            break
    return cmds


def craft_answer(item: dict, lesson_text: str) -> str:
    q = item["question"].rstrip("?") + "?"
    raw = item.get("answer_raw")
    paras = lesson_paragraphs(lesson_text)
    qtok = tokens(q)

    scored = []
    for p in paras:
        overlap = len(qtok & tokens(p))
        if overlap:
            scored.append((overlap, p))
    scored.sort(key=lambda x: (-x[0], -len(x[1])))
    picks = [p for _, p in scored[:4] if _ >= 2]

    ql = q.lower()
    if raw:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", raw) if s.strip()]
        short = sentences[0] if sentences else raw
        bullets = []
        for s in sentences[1:5] or sentences[:3]:
            s = re.sub(r"\*\*", "", s)
            bullets.append(s)
        cmds = extract_commands(raw) or extract_commands(lesson_text)
    else:
        topic_words = " ".join(
            w for w in re.findall(r"[A-Za-z0-9_./+-]{3,}", q) if w.lower() not in STOP
        )[:80]
        if picks:
            short = picks[0]
            if len(short) > 200:
                short = short[:197] + "…"
            bullets = picks[1:4] or picks[:3]
        elif ql.startswith("what is the difference") or "difference between" in ql:
            short = (
                f"Contrast the two sides of {topic_words or 'the topic'} by purpose, "
                "when you choose each, and how you verify the choice in production."
            )
            bullets = [
                "Define each option in one line — mechanism, not marketing.",
                "State the decision rule (reliability, security, operability, or cost).",
                "Name the command or signal that proves which one you are looking at.",
            ]
        elif ql.startswith("what is") or ql.startswith("what are") or ql.startswith("what does"):
            short = (
                f"{topic_words or 'It'} is best answered as: purpose → where it runs → "
                "how you inspect it on a live host."
            )
            bullets = [
                f"Give a crisp definition of {topic_words or 'the concept'} in operational terms.",
                "Say where it shows up (files, units, packets, cloud construct).",
                "Name the first check you would run before changing anything.",
            ]
        elif ql.startswith("how ") or ql.startswith("how do") or ql.startswith("how would"):
            short = (
                f"Walk through {topic_words or 'the procedure'} as: assess → change → "
                "verify → rollback."
            )
            bullets = [
                "Start with the evidence you gather before touching production.",
                "List the ordered steps and the privilege needed for each.",
                "End with the verification and the rollback if the signal is wrong.",
            ]
        elif ql.startswith("why "):
            short = (
                f"Explain why {topic_words or 'this practice'} exists: the failure it prevents "
                "and the trade-off you accept."
            )
            bullets = [
                "Name the risk or failure mode it reduces.",
                "Call out the cost (complexity, latency, ops load).",
                "Say when you would choose a different approach.",
            ]
        else:
            short = (
                f"Answer with judgement: what {topic_words or 'it'} is, how you verify it, "
                "and what breaks if you get it wrong."
            )
            bullets = [
                "Lead with the operational definition interviewers expect.",
                "Name a concrete verification command or metric.",
                "Call out a common misconfiguration and blast radius.",
            ]
        if item["level"] == "architect" and len(bullets) < 4:
            bullets.append(
                "Tie the design to scale, tenancy, least privilege, and rollback."
            )
        cmds = extract_commands(lesson_text)

    # Plain prose fallbacks — never use leading "#" (MkDocs turns those into TOC headings)
    if not cmds:
        if item["level"] == "architect":
            try_lines = [
                "Document the decision, blast radius, and rollback before changing production."
            ]
        else:
            try_lines = [
                "Name and run the primary verification command from this lesson topic."
            ]
    else:
        try_lines = []
        for c in cmds[:3]:
            try_lines.append(f"`{c}`")

    trap = {
        "beginner": "Giving a definition without naming a command or file you would check.",
        "intermediate": "Skipping verification — interviews expect how you prove it worked.",
        "architect": "Optimising for theory while ignoring blast radius, tenancy, or rollback.",
    }[item["level"]]

    short = sanitize(short).lstrip("- ").strip()
    bullets = [sanitize(b).lstrip("- ").strip() for b in bullets if sanitize(b).strip()]

    # Placeholder number replaced by render_level — closing ** required for bold questions
    lines = [
        f"**__N__. {sanitize(q)}**",
        "",
        '??? success "Reveal answer"',
        f"    **In short:** {short}",
        "    ",
        "    **Key points**",
        "    ",
    ]
    for b in bullets[:5]:
        lines.append(f"    - {b}")
    lines += [
        "    ",
        "    **Try this**",
        "    ",
    ]
    for t in try_lines:
        lines.append(f"    - {t}")
    lines += [
        "    ",
        "    **Trap**",
        "    ",
        f"    - {trap}",
        "",
    ]
    return "\n".join(lines)


def existing_norms(path: Path) -> set[str]:
    text = path.read_text()
    cut = text.split("## From the")[0]
    # Also strip any previous Beginner/Intermediate/Architect course dumps if re-run
    return {
        norm(m.group(1))
        for m in re.finditer(r"^\*\*\d+\.\s*(.+?)\*\*\s*$", cut, re.M)
    }


def collect(topic: str, docs_root: Path, interview_path: Path) -> dict[str, list[dict]]:
    exist = existing_norms(interview_path)
    by_level: dict[str, list[dict]] = defaultdict(list)
    seen: set[str] = set()
    root = docs_root / topic
    for p in sorted(root.rglob("*.md")):
        if p.name in {"index.md", "faq.md", "roadmap.md"}:
            continue
        if "interview" in p.parts or "projects" in p.parts:
            continue
        if "summary" in p.name:
            continue
        text = p.read_text()
        for item in extract_lesson_qs(text, p.name):
            n = norm(item["question"])
            if len(n) < 8 or n in seen or n in exist:
                continue
            if "coming soon" in item["question"].lower():
                continue
            seen.add(n)
            item["_lesson_path"] = str(p)
            by_level[item["level"]].append(item)
    return by_level


def render_level(items: list[dict], start: int) -> tuple[str, int]:
    blocks = []
    n = start
    cache: dict[str, str] = {}
    for item in items:
        lp = item["_lesson_path"]
        if lp not in cache:
            cache[lp] = Path(lp).read_text()
        block = craft_answer(item, cache[lp]).replace("**__N__.", f"**{n}.", 1)
        blocks.append(block)
        n += 1
    return "\n".join(blocks), n


def rebuild_interview_page(
    interview_path: Path, by_level: dict[str, list[dict]], course_label: str
) -> int:
    text = interview_path.read_text()
    # Keep curated core content; drop prior course dumps / Related / endraw
    if "## From the" in text:
        head = text.split("## From the", 1)[0]
    elif "## Related" in text:
        head = text.split("## Related", 1)[0]
    else:
        head = text
    head = head.replace("{% endraw %}", "").rstrip() + "\n"

    nums = [int(x) for x in re.findall(r"^\*\*(\d+)\.\s", head, re.M)]
    next_n = max(nums) + 1 if nums else 1

    slug = "linux" if course_label == "Linux" else "networking"
    parts = [head.rstrip(), "", f"## From the {course_label} course", ""]
    for level, title in (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("architect", "Architect Level"),
    ):
        items = by_level.get(level, [])
        parts.append(f"### {title}")
        parts.append("")
        body, next_n = render_level(items, next_n)
        parts.append(body.rstrip())
        parts.append("")
        print(f"  {title}: {len(items)} (next={next_n})")

    parts += [
        "## Related",
        f"- Course: [{course_label}](../{slug}/index.md)",
        "- Hub: [Interview Preparation](index.md)",
        "{% endraw %}",
        "",
    ]

    out = "\n".join(parts)
    total_qs = len(re.findall(r"^\*\*\d+\.\s", out, re.M))
    out = re.sub(
        r'description: "\d+ curated',
        f'description: "{total_qs} curated',
        out,
        count=1,
    )
    # Refresh intro blurb for course grouping
    out = re.sub(
        r"The \*\*From the .*?course\*\* section.*",
        f"The **From the {course_label} course** section copies every lesson interview "
        "question, grouped as **Beginner**, **Intermediate**, and **Architect Level**, "
        "each with a model answer.",
        out,
        count=1,
    )
    interview_path.write_text(out)
    return total_qs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", choices=["linux", "networking", "both"], default="both")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    docs = root / "docs"
    topics = ["linux", "networking"] if args.topic == "both" else [args.topic]
    for topic in topics:
        print(f"=== {topic} ===")
        interview = docs / "interview" / f"{topic}.md"
        by_level = collect(topic, docs, interview)
        label = "Linux" if topic == "linux" else "Networking"
        total = rebuild_interview_page(interview, by_level, label)
        print(f"wrote {interview} total_questions={total}")


if __name__ == "__main__":
    main()
